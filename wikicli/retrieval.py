"""The retrieval tool: chunk the vault, index it, and search it.

Hybrid search = BM25 keyword ranking + EmbeddingGemma cosine ranking,
merged with reciprocal rank fusion. Everything runs locally; the index
lives in .index/ (outside the Obsidian vault).
"""
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime

import numpy as np
from rank_bm25 import BM25Okapi

from . import config
from .markdown import sections, split_front_matter, title_of

CHUNKS_FILE = config.INDEX_DIR / "chunks.jsonl"
VECTORS_FILE = config.INDEX_DIR / "embeddings.npy"
META_FILE = config.INDEX_DIR / "index_meta.json"
CACHE_FILE = config.INDEX_DIR / "embed_cache.npz"

STOPWORDS = set(
    "a an and are as at be by did do does for from had has have how i in is it its of on or "
    "that the their them they this to was were what when where which who why will with "
    "would you your about into than then there these those can could should my me we our".split()
)
# Sections of generated notes that are navigation, not content.
SKIP_SECTIONS = {"Related Notes", "Sources"}


@dataclass
class Chunk:
    id: str
    path: str        # relative to the project root, e.g. vault/Sources/Class 3 - ....md
    title: str       # page title
    section: str     # section heading ("" for the intro)
    kind: str        # "source" (original evidence) or "note" (generated wiki page)
    text: str

    @property
    def label(self) -> str:
        return f"{self.title} › {self.section}" if self.section else self.title


@dataclass
class Hit:
    chunk: Chunk
    score: float     # fused RRF score
    bm25: float
    cosine: float


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9$%£]+(?:[-'][a-z0-9]+)*", text.lower())
    return [w for w in words if w not in STOPWORDS]


def _pdf_text(path) -> str:
    from pypdf import PdfReader
    return "\n\n".join(page.extract_text() or "" for page in PdfReader(path).pages)


def read_document(path) -> tuple[str, list[tuple[str, str]]]:
    """Return (title, [(section, text)]) for a Markdown, text or PDF file."""
    if path.suffix.lower() == ".pdf":
        return path.stem, [("", _pdf_text(path))]
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".md":
        _, body = split_front_matter(raw)
        return title_of(body, path.stem), sections(body)
    return path.stem, [("", raw)]


def _split_long(text: str, limit: int) -> list[str]:
    if len(text) <= limit:
        return [text]
    pieces, current = [], ""
    for para in re.split(r"\n\s*\n", text):
        if current and len(current) + len(para) > limit:
            pieces.append(current.strip())
            current = ""
        current += para + "\n\n"
    if current.strip():
        pieces.append(current.strip())
    return pieces


def chunk_vault(source_files: set[str]) -> list[Chunk]:
    """Chunk ingested sources (paths relative to ROOT) and all generated notes."""
    chunks = []
    for path in sorted(config.VAULT.rglob("*")):
        if path.suffix.lower() not in {".md", ".txt", ".pdf"} or path.name in config.NAV_PAGES:
            continue
        if any(part.startswith(".") for part in path.relative_to(config.VAULT).parts):
            continue  # .obsidian and other hidden folders
        kind = "source" if config.SOURCES_DIR in path.parents else "note"
        rel = path.relative_to(config.ROOT).as_posix()
        if kind == "source" and rel not in source_files:
            continue  # sitting in Sources but not ingested yet
        title, secs = read_document(path)
        for section, text in secs:
            if section in SKIP_SECTIONS:
                continue
            for n, piece in enumerate(_split_long(text, config.CHUNK_MAX_CHARS)):
                chunks.append(Chunk(f"{rel}#{section}#{n}", rel, title, section, kind, piece))
    return chunks


def _doc_string(c: Chunk) -> str:
    return f"{c.title}\t{c.section}\n{c.text}"


def build_index(model, source_files: set[str]) -> dict:
    """Chunk ingested sources and notes, embed changed chunks, and save the index."""
    config.INDEX_DIR.mkdir(exist_ok=True)
    chunks = chunk_vault(source_files)
    keys = [hashlib.sha256(_doc_string(c).encode()).hexdigest() for c in chunks]

    cache = {}
    if CACHE_FILE.exists():
        data = np.load(CACHE_FILE)
        cache = dict(zip(data["keys"].tolist(), data["vectors"]))
    missing = [i for i, k in enumerate(keys) if k not in cache]
    if missing:
        fresh = model.embed([_doc_string(chunks[i]) for i in missing], kind="document")
        for i, vec in zip(missing, fresh):
            cache[keys[i]] = vec
    vectors = np.stack([cache[k] for k in keys]) if chunks else np.zeros((0, 768), np.float32)

    with CHUNKS_FILE.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(asdict(c), ensure_ascii=False) + "\n")
    np.save(VECTORS_FILE, vectors)
    np.savez(CACHE_FILE, keys=np.array(keys), vectors=vectors)
    meta = {
        "built_at": datetime.now().isoformat(timespec="seconds"),
        "embed_model": model.embed_model,
        "chunks": len(chunks),
        "sources": len({c.path for c in chunks if c.kind == "source"}),
        "notes": len({c.path for c in chunks if c.kind == "note"}),
        "newly_embedded": len(missing),
    }
    META_FILE.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


class Retriever:
    def __init__(self, model):
        if not CHUNKS_FILE.exists():
            raise FileNotFoundError("No index yet. Run: python wiki.py ingest <file>")
        self.model = model
        with CHUNKS_FILE.open(encoding="utf-8") as f:
            self.chunks = [Chunk(**json.loads(line)) for line in f]
        self.vectors = np.load(VECTORS_FILE)
        self.bm25 = BM25Okapi([tokenize(f"{c.title} {c.section} {c.text}") for c in self.chunks])
        self.meta = json.loads(META_FILE.read_text(encoding="utf-8"))

    def search(self, query: str, k: int = 5, scope: str = "all") -> list[Hit]:
        allowed = np.array([scope == "all" or c.kind == scope for c in self.chunks])
        bm25 = np.asarray(self.bm25.get_scores(tokenize(query)))
        cosine = self.vectors @ self.model.embed([query], kind="query")[0]

        def ranks(scores):
            order = [i for i in np.argsort(-scores) if allowed[i]]
            return {i: r for r, i in enumerate(order)}

        bm25_rank, cos_rank = ranks(bm25), ranks(cosine)
        fused = {}
        for i in bm25_rank:
            fused[i] = 1 / (60 + cos_rank[i])
            if bm25[i] > 0:  # a keyword rank only counts if a keyword matched
                fused[i] += 1 / (60 + bm25_rank[i])
        best = sorted(fused, key=fused.get, reverse=True)[:k]
        return [Hit(self.chunks[i], fused[i], float(bm25[i]), float(cosine[i])) for i in best]
