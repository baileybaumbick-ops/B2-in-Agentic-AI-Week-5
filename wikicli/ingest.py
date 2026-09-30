"""Ingestion: preserve an original source, draft concept notes with local
Gemma, and (re)build the Obsidian pages and the retrieval index.

Design rules:
- Originals are copied byte-for-byte into vault/Sources/ and never edited.
- Note files are rendered from .index/manifest.json, so re-ingesting a
  source replaces its contribution instead of adding duplicates.
- Titles come from the model but are validated here; machine IDs live
  only in front matter and in .index/.
"""
import hashlib
import json
import re
import shutil
import time
from dataclasses import dataclass, field
from datetime import date

from . import config, retrieval
from .llm import HarnessError

MANIFEST_FILE = config.INDEX_DIR / "manifest.json"
VERSIONS_DIR = config.INDEX_DIR / "source_versions"
SUPPORTED = {".md", ".txt", ".pdf"}
GENERATED_MARK = "generated_by:"
SMALL_WORDS = {"and", "or", "of", "the", "a", "an", "in", "on", "for", "to", "vs"}


@dataclass
class IngestResult:
    source: str
    path: str
    status: str                      # created | updated | unchanged
    created: list = field(default_factory=list)
    updated: list = field(default_factory=list)
    removed: list = field(default_factory=list)
    rejected_titles: list = field(default_factory=list)
    renamed: list = field(default_factory=list)
    model_seconds: float = 0.0


# ---------------------------------------------------------------- manifest

def load_manifest() -> dict:
    if MANIFEST_FILE.exists():
        return json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    return {"sources": {}, "notes": {}}


def save_manifest(manifest: dict) -> None:
    config.INDEX_DIR.mkdir(exist_ok=True)
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")


def sha256_of(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------- naming

def clean_title(raw: str) -> str | None:
    """Return a short, human-readable note title, or None if unusable."""
    text = re.sub(r"\s+", " ", raw or "").strip()
    text = re.sub(r"^case\s*[-:]\s*(.+)$", r"\1 Case", text, flags=re.I)       # "Case - Intel"
    text = re.sub(r"\bcase study$", "Case", text, flags=re.I)
    text = re.sub(r"^(defining|understanding|introduction to|intro to|the)\s+", "", text, flags=re.I)
    text = re.sub(r"[\[\]#|^:*?\"<>/\\_]", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" -.,;'")
    words = text.split()
    if not 1 <= len(words) <= 5:
        return None
    if re.search(r"\b(class|lecture|notes?|summary|chunk|export)\b", text, re.I):
        return None
    if re.search(r"\b[0-9a-f]{8,}\b", text, re.I) or raw.strip().endswith("?"):
        return None
    if re.search(r"\b(is|are|was|were|should|how|why|what|does|do|drives?|makes?|leads?)\b", text, re.I):
        return None  # looks like a sentence or question
    out = []
    for i, word in enumerate(words):
        if len(word) > 1 and (word.isupper() or any(ch.isupper() for ch in word[1:])):
            out.append(word)                      # acronyms / brand casing (OPEC, NutraSweet)
        elif i > 0 and word.lower() in SMALL_WORDS:
            out.append(word.lower())
        else:
            out.append("-".join(p[:1].upper() + p[1:] for p in word.split("-")))
    return " ".join(out)


def title_key(title: str) -> str:
    """Normalized key so 'Barriers to Entry' and 'Barrier to Entry Case' merge."""
    words = re.findall(r"[a-z0-9]+", title.lower())
    return " ".join(w.rstrip("s") for w in words if w not in {"the", "a", "an", "case", "study"})


def safe_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*#^\[\]]', "-", name).strip(" .")


# ---------------------------------------------------------------- preserve

def preserve_original(path, replace: bool) -> "Path":
    """Copy an original into vault/Sources unchanged and return its vault path."""
    path = path.resolve()
    if config.SOURCES_DIR in path.parents:
        return path
    config.SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    dest = config.SOURCES_DIR / safe_filename(path.name)
    if dest.exists():
        if sha256_of(dest) == sha256_of(path):
            return dest
        if not replace:
            raise HarnessError(
                f"A different file named '{dest.name}' is already in vault/Sources. "
                "Rename the new file, or pass --replace to archive the old version."
            )
        VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
        archived = VERSIONS_DIR / f"{dest.stem}.{sha256_of(dest)[:10]}{dest.suffix}"
        shutil.move(dest, archived)
    shutil.copy2(path, dest)
    if sha256_of(dest) != sha256_of(path):
        raise HarnessError(f"Copy of {path.name} does not match the original; aborting.")
    return dest


# ---------------------------------------------------------------- drafting

def _schema(section_names: list[str]) -> dict:
    return {
        "type": "object",
        "properties": {
            "concepts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "topic": {"type": "string", "enum": config.TOPICS},
                        "summary": {"type": "string"},
                        "key_points": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "point": {"type": "string"},
                                    "section": {"type": "string", "enum": section_names},
                                },
                                "required": ["point", "section"],
                            },
                        },
                        "related": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["title", "topic", "summary", "key_points", "related"],
                },
            }
        },
        "required": ["concepts"],
    }


def draft_concepts(model, title: str, secs: list, existing_titles: list[str]) -> tuple[list, float]:
    rules = (config.PROMPTS_DIR / "ingest_rules.md").read_text(encoding="utf-8")
    section_names = [s or "Introduction" for s, _ in secs]
    source_text = "\n\n".join(f"## {s or 'Introduction'}\n{t}" for s, t in secs)
    user = (
        f"Allowed topics: {json.dumps(config.TOPICS)}\n"
        f"Allowed section headings: {json.dumps(section_names)}\n"
        f"Existing note titles: {json.dumps(existing_titles) if existing_titles else 'none yet'}\n\n"
        f"SOURCE TITLE: {title}\n\nSOURCE TEXT:\n{source_text}"
    )
    messages = [{"role": "system", "content": rules}, {"role": "user", "content": user}]
    total = 0.0
    for _attempt in range(3):
        call = model.chat(messages, temperature=config.INGEST_TEMPERATURE,
                          json_schema=_schema(section_names))
        total += call.seconds
        try:
            concepts = json.loads(call.text).get("concepts", [])
        except json.JSONDecodeError:
            continue
        if concepts:
            return concepts, total
    raise HarnessError(f"Gemma did not return usable notes for '{title}' after 3 tries.")


# ---------------------------------------------------------------- merge + render

def _note_id(title: str) -> str:
    return "note-" + hashlib.sha1(title_key(title).encode()).hexdigest()[:10]


def load_curation() -> dict:
    path = config.ROOT / "curation.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    return {"rename": data.get("rename", {}), "topic": data.get("topic", {})}


def curated_title(title: str, curation: dict) -> str:
    renames = {title_key(k): v for k, v in curation["rename"].items()}
    return renames.get(title_key(title), title)


def normalize_titles(manifest: dict) -> list[str]:
    """Rename notes whose title breaks the naming rules (e.g. 'Case - Intel') or
    that curation.json renames, and apply curated topic folders.

    Links are rendered from the manifest, so incoming links follow the rename,
    and the old file is removed by write_vault. The note_id stays the same.
    """
    curation = load_curation()
    notes, renamed = manifest["notes"], []
    for old in list(notes):
        new = curated_title(clean_title(old) or old, curation)
        if new != old and new not in notes:
            notes[new] = notes.pop(old)
            renamed.append(f"{old} -> {new}")
    for title, topic in curation["topic"].items():
        if title in notes and topic in config.TOPICS:
            notes[title]["topic"] = topic
    return renamed


def merge_concepts(manifest: dict, source: str, concepts: list, section_names: list) -> dict:
    """Replace this source's contribution in the manifest. Returns change lists."""
    renamed = normalize_titles(manifest)
    notes = manifest["notes"]
    by_key = {title_key(t): t for t in notes}
    before = {t: json.dumps(n["points"].get(source)) for t, n in notes.items()}
    for note in notes.values():                       # forget this source's old points
        note["points"].pop(source, None)

    today = date.today().isoformat()
    curation = load_curation()
    rejected, touched = [], []
    for concept in concepts:
        title = clean_title(concept.get("title", ""))
        if not title:
            rejected.append(concept.get("title", ""))
            continue
        title = curated_title(title, curation)
        points = []
        for kp in concept.get("key_points", []):
            text = (kp.get("point") or "").strip()
            section = kp.get("section") if kp.get("section") in section_names else ""
            if text:
                points.append({"point": text, "section": "" if section == "Introduction" else section})
        if not points:
            rejected.append(title)
            continue
        existing = by_key.get(title_key(title))
        if existing and existing.endswith(" Case"):
            # Guard: only merge into "<Company> Case" if the new points are about that company.
            company = existing[: -len(" Case")].lower()
            content = " ".join([concept.get("summary", "")] + [p["point"] for p in points]).lower()
            if company not in content:
                rejected.append(f"{title} (points are not about {existing[:-5]}; not merged)")
                continue
        if existing:
            note = notes[existing]
            note["points"].setdefault(source, []).extend(points)
            note["related"] = sorted(set(note["related"]) | set(concept.get("related", [])))
            touched.append(existing)
        else:
            topic = concept.get("topic") if concept.get("topic") in config.TOPICS else config.TOPICS[0]
            if title.endswith(" Case"):
                topic = "Company Cases"
            topic = curation["topic"].get(title, topic)
            notes[title] = {
                "note_id": _note_id(title),
                "topic": topic,
                "summary": (concept.get("summary") or "").strip(),
                "created": today,
                "points": {source: points},
                "related": sorted(set(concept.get("related", []))),
            }
            by_key[title_key(title)] = title
            touched.append(title)

    removed = [t for t, n in notes.items() if not n["points"]]
    for t in removed:
        del notes[t]
    created = [t for t in touched if t not in before]
    updated = [t for t in dict.fromkeys(touched)
               if t in before and before[t] != json.dumps(notes[t]["points"].get(source))]
    for t in set(created) | set(updated):
        notes[t]["updated"] = today
    return {"created": list(dict.fromkeys(created)), "updated": updated,
            "removed": removed, "rejected": rejected, "renamed": renamed}


def _source_link(source: str, section: str) -> str:
    short = source.split(" - ")[0] if source.lower().startswith("class") else source
    if section:
        return f"[[{source}#{section}|{short} › {section}]]"
    return f"[[{source}|{short}]]"


def _related_titles(title: str, note: dict, notes: dict) -> list[str]:
    by_key = {title_key(t): t for t in notes}
    picked = []
    for raw in note["related"]:
        match = by_key.get(title_key(raw))
        if match and match != title and match not in picked:
            picked.append(match)
    for other, other_note in notes.items():         # notes drawn from the same source
        if len(picked) >= 6:
            break
        if other != title and other not in picked and set(other_note["points"]) & set(note["points"]):
            picked.append(other)
    return picked


def render_note(title: str, note: dict, notes: dict) -> str:
    sources = sorted(note["points"])
    lines = [
        "---",
        f"note_id: {note['note_id']}",
        "type: concept",
        f"topic: {note['topic']}",
        "sources:",
        *[f'  - "[[{s}]]"' for s in sources],
        f"created: {note['created']}",
        f"updated: {note.get('updated', note['created'])}",
        f"generated_by: {config.CHAT_MODEL} via wiki.py ingest",
        "---",
        "",
        f"# {title}",
        "",
        note["summary"],
        "",
        "## Key Points",
    ]
    for source in sources:
        if len(sources) > 1:
            lines += ["", f"### From {source}"]
        for p in note["points"][source]:
            lines.append(f"- {p['point']} ({_source_link(source, p['section'])})")
    lines += ["", "## Related Notes"]
    related = _related_titles(title, note, notes)
    lines += [f"- [[{r}]]" for r in related] or ["- (none yet)"]
    lines += ["", "## Sources"]
    lines += [f"- [[{s}]]" for s in sources]
    return "\n".join(lines) + "\n"


def note_path(title: str, note: dict):
    return config.VAULT / note["topic"] / f"{safe_filename(title)}.md"


def write_vault(manifest: dict) -> None:
    notes = manifest["notes"]
    wanted = {note_path(t, n).resolve() for t, n in notes.items()}
    # Remove stale generated notes (never touches hand-written files).
    for topic in config.TOPICS:
        folder = config.VAULT / topic
        for f in folder.glob("*.md") if folder.exists() else []:
            if f.resolve() not in wanted and GENERATED_MARK in f.read_text(encoding="utf-8")[:600]:
                f.unlink()
    for title, note in notes.items():
        path = note_path(title, note)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_note(title, note, notes), encoding="utf-8")
    write_index(manifest)
    write_catalog(manifest)


def _first_sentence(text: str, limit: int = 180) -> str:
    match = re.match(r"(.+?[.!?])(\s|$)", text.strip())
    sentence = match.group(1) if match else text.strip()
    if len(sentence) > limit:
        sentence = sentence[:limit].rsplit(" ", 1)[0].rstrip(",;") + "..."
    return sentence


def write_index(manifest: dict) -> None:
    lines = [
        "# Strategy Wiki",
        "",
        "Concept notes built from my Strategy course study notes. Each note links to related "
        "notes and back to the original source section it came from. The originals are listed "
        "in [[Source Catalog]].",
    ]
    for topic in config.TOPICS:
        titles = sorted(t for t, n in manifest["notes"].items() if n["topic"] == topic)
        if titles:
            lines += ["", f"## {topic}"]
            lines += [f"- [[{t}]] - {_first_sentence(manifest['notes'][t]['summary'])}" for t in titles]
    (config.VAULT / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_catalog(manifest: dict) -> None:
    lines = [
        "# Source Catalog",
        "",
        "Original sources, preserved unchanged in the `Sources` folder. Each is a set of my own "
        "study notes paraphrasing one lecture (the lecture slides themselves are not "
        "redistributed). Back to [[index]].",
        "",
        "| Source | Concept notes drawn from it | Ingested |",
        "|---|---|---|",
    ]
    for source, info in sorted(manifest["sources"].items()):
        derived = sorted(t for t, n in manifest["notes"].items() if source in n["points"])
        links = ", ".join(f"[[{t}]]" for t in derived) or "-"
        lines.append(f"| [[{source}]] | {links} | {info['ingested_at']} |")
    (config.VAULT / "Source Catalog.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- entry point

def expand_paths(paths) -> list:
    files = []
    for p in paths:
        if p.is_dir():
            files += sorted(f for f in p.iterdir() if f.suffix.lower() in SUPPORTED)
        elif p.exists():
            files.append(p)
        else:
            raise HarnessError(f"File not found: {p}")
    bad = [f.name for f in files if f.suffix.lower() not in SUPPORTED]
    if bad:
        raise HarnessError(f"Unsupported file type: {', '.join(bad)} (use .md, .txt or .pdf)")
    return files


def ingest_one(model, path, force=False, replace=False, log=print) -> IngestResult:
    dest = preserve_original(path, replace)
    source = dest.stem
    digest = sha256_of(dest)
    rel = dest.relative_to(config.ROOT).as_posix()
    manifest = load_manifest()
    known = manifest["sources"].get(source)
    log(f"  preserved original: {rel}")
    if known and known["sha256"] == digest and not force:
        log("  unchanged since last ingest; no notes created or modified")
        return IngestResult(source, rel, "unchanged")

    title, secs = retrieval.read_document(dest)
    section_names = [s or "Introduction" for s, _ in secs]
    log(f"  drafting concept notes with {model.chat_model} (local)...")
    concepts, seconds = draft_concepts(model, title, secs, sorted(manifest["notes"]))
    changes = merge_concepts(manifest, source, concepts, section_names)
    manifest["sources"][source] = {
        "file": rel,
        "sha256": digest,
        "source_id": "src-" + digest[:12],
        "ingested_at": date.today().isoformat(),
    }
    save_manifest(manifest)
    write_vault(manifest)
    return IngestResult(source, rel, "updated" if known else "created",
                        changes["created"], changes["updated"], changes["removed"],
                        changes["rejected"], changes["renamed"], round(seconds, 1))


def rebuild(model) -> tuple[list, dict]:
    """Apply naming rules and curation.json, re-render the vault and reindex. No LLM calls."""
    manifest = load_manifest()
    renamed = normalize_titles(manifest)
    save_manifest(manifest)
    write_vault(manifest)
    meta = retrieval.build_index(model, {s["file"] for s in manifest["sources"].values()})
    return renamed, meta


def ingest(model, paths, force=False, replace=False, log=print) -> tuple[list, dict]:
    results = []
    for f in expand_paths(paths):
        log(f"Ingesting {f.name}")
        start = time.perf_counter()
        result = ingest_one(model, f, force, replace, log)
        log(f"  done in {time.perf_counter() - start:.1f}s")
        results.append(result)
    manifest = load_manifest()
    write_vault(manifest)  # keeps index pages current even if nothing changed
    meta = retrieval.build_index(model, {s["file"] for s in manifest["sources"].values()})
    return results, meta
