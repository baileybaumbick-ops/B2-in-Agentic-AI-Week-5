"""The harness: decides what each mode sends to local Gemma and what it keeps.

- chat:   assistant persona + rolling conversation history; retrieval is
          optional (only when the user asks about their notes).
- ask:    stateless; retrieval is mandatory; research rules; citation
          checking; insufficient-evidence refusal. Never sees chat history.
- search: retrieval only; returns original passages, no model generation.
Every result is saved under outputs/.
"""
import json
import re
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime

from . import config, ingest as ingest_mod
from .llm import HarnessError, LocalModel
from .retrieval import Hit, Retriever, tokenize

INSUFFICIENT = "INSUFFICIENT_EVIDENCE"
ANSWERABILITY_TASK = (
    "Do NOT answer yet. First judge: do the passages contain the answer to this specific "
    "question, about the specific company, case, or topic it names? Passages that are only on a "
    "related topic do not count. Return JSON with: answerable ('yes', 'partly', or 'no'), "
    "passages (tags that contain the answer), reason (one short sentence)."
)
ANSWERABILITY_SCHEMA = {
    "type": "object",
    "properties": {
        "answerable": {"type": "string", "enum": ["yes", "partly", "no"]},
        "passages": {"type": "array", "items": {"type": "string"}},
        "reason": {"type": "string"},
    },
    "required": ["answerable", "passages", "reason"],
}
GENERIC_QUESTION_WORDS = {
    "course", "class", "lecture", "notes", "wiki", "conclude", "concluded", "conclusion",
    "explain", "describe", "according", "main", "example", "examples", "mean", "means",
    "happened", "happen", "instead", "reason", "reasons", "look", "looked",
}
NOTES_TRIGGER = re.compile(
    r"\b(my notes|the notes|in (the |my )?(wiki|class|lecture|course)|lecture|wiki|according to)\b", re.I
)


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:48] or "query"


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


@dataclass
class AskResult:
    question: str
    answer: str
    status: str                      # answered | insufficient_evidence
    passages: list                   # [{tag, path, section, kind, text, cosine, bm25}]
    cited: list = field(default_factory=list)
    checks: dict = field(default_factory=dict)
    timing: dict = field(default_factory=dict)
    memory: list = field(default_factory=list)
    model: str = config.CHAT_MODEL
    saved_to: str = ""


class Harness:
    def __init__(self):
        self.model = LocalModel()
        self._retriever = None
        self.assistant_prompt = (config.PROMPTS_DIR / "assistant.md").read_text(encoding="utf-8")
        self.research_rules = (config.PROMPTS_DIR / "research_rules.md").read_text(encoding="utf-8")
        self.history: list[dict] = []          # chat mode only
        self.session = _stamp()

    @property
    def retriever(self) -> Retriever:
        if self._retriever is None:
            try:
                self._retriever = Retriever(self.model)
            except FileNotFoundError as exc:
                raise HarnessError(str(exc)) from exc
        return self._retriever

    # ------------------------------------------------------------ saving
    def _save(self, mode: str, name: str, record: dict, markdown: str) -> str:
        folder = config.OUTPUTS_DIR / mode
        folder.mkdir(parents=True, exist_ok=True)
        base = folder / f"{_stamp()}-{_slug(name)}"
        base.with_suffix(".json").write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
        base.with_suffix(".md").write_text(markdown, encoding="utf-8")
        return base.with_suffix(".md").relative_to(config.ROOT).as_posix()

    @staticmethod
    def _passage_dicts(hits: list[Hit], prefix: str) -> list[dict]:
        return [
            {
                "tag": f"{prefix}{i}",
                "path": h.chunk.path,
                "section": h.chunk.section,
                "kind": h.chunk.kind,
                "text": h.chunk.text,
                "cosine": round(h.cosine, 3),
                "bm25": round(h.bm25, 2),
            }
            for i, h in enumerate(hits, 1)
        ]

    # ------------------------------------------------------------ search
    def search(self, query: str, k: int = config.SEARCH_TOP_K, scope: str = "all") -> dict:
        start = time.perf_counter()
        hits = self.retriever.search(query, k=k, scope=scope)
        result = {
            "mode": "search",
            "query": query,
            "scope": scope,
            "passages": self._passage_dicts(hits, "R"),
            "seconds": round(time.perf_counter() - start, 2),
        }
        md = [f"# Search: {query}", ""]
        for p in result["passages"]:
            md += [f"## [{p['tag']}] {p['path']} › {p['section'] or '(intro)'}",
                   f"kind={p['kind']} cosine={p['cosine']} bm25={p['bm25']}", "", p["text"], ""]
        result["saved_to"] = self._save("search", query, result, "\n".join(md))
        return result

    # ------------------------------------------------------------ ask
    def ask(self, question: str, k: int = config.ASK_TOP_K) -> AskResult:
        """Standalone factual answer from retrieved evidence. Ignores chat history by design."""
        t0 = time.perf_counter()
        hits = self.retriever.search(question, k=k)
        t_retrieval = time.perf_counter() - t0
        passages = self._passage_dicts(hits, "S")
        result = AskResult(question, "", "answered", passages)
        result.timing["retrieval_s"] = round(t_retrieval, 2)

        # Evidence gate: nothing even loosely related -> refuse without generating.
        q_terms = set(tokenize(question))
        overlap = any(q_terms & set(tokenize(p["text"] + " " + p["section"])) for p in passages)
        best = max((p["cosine"] for p in passages), default=0.0)
        result.checks.update({"best_cosine": best, "keyword_overlap": overlap})
        if not passages or (best < config.ASK_MIN_COSINE and not overlap):
            result.status = "insufficient_evidence"
            result.answer = "Insufficient evidence: no passage in the wiki is related to this question."
            result.checks["gate"] = "refused before generation (retrieval too weak)"
            return self._finish_ask(result, t0)

        evidence = "\n\n".join(
            f"[{p['tag']}] ({p['path']} › {p['section'] or 'intro'})\n{p['text']}" for p in passages
        )
        # Shared prefix for both calls, so Ollama can reuse the processed prompt.
        prefix = f"Evidence passages:\n\n{evidence}\n\nQuestion: {question}\n\n"
        calls = []

        # Step 1: answerability check. Do the passages answer THIS question?
        missing = self._missing_terms(question, passages)
        result.checks["question_terms_absent_from_passages"] = missing
        hint = (f"Note: these question terms appear in none of the passages: {', '.join(missing)}.\n"
                if missing else "")
        check = self.model.chat(
            [{"role": "system", "content": self.research_rules},
             {"role": "user", "content": prefix + hint + ANSWERABILITY_TASK}],
            temperature=0.0, json_schema=ANSWERABILITY_SCHEMA,
        )
        calls.append(check)
        try:
            verdict = json.loads(check.text)
        except json.JSONDecodeError:
            verdict = {"answerable": "partly", "reason": "unparseable check; continuing to answer step"}
        result.checks["answerability"] = verdict
        # Refuse early only when the model says "no" AND retrieval is weak. With a strong
        # match, the answer step still runs and can refuse on its own under the research rules.
        if verdict.get("answerable") == "no" and best < config.ASK_STRONG_MATCH:
            result.status = "insufficient_evidence"
            result.answer = f"Insufficient evidence: {verdict.get('reason') or 'the passages do not answer this.'}"
            result.checks["gate"] = "answerability 'no' with weak retrieval (best cosine below threshold)"
            return self._finish_ask(result, t0, calls)
        if verdict.get("answerable") == "no":
            result.checks["gate"] = "answerability 'no' overridden by strong retrieval match; answer step decides"

        # Step 2: grounded answer with citations.
        messages = [{"role": "system", "content": self.research_rules},
                    {"role": "user", "content": prefix +
                     "Answer the question following the rules. Cite passages like [S1]."}]
        for attempt in range(2):
            call = self.model.chat(messages, temperature=config.ASK_TEMPERATURE)
            calls.append(call)
            text = call.text.strip()
            if INSUFFICIENT in text:
                result.status = "insufficient_evidence"
                reason = text.split(INSUFFICIENT, 1)[1].lstrip(" :").strip()
                result.answer = f"Insufficient evidence: {reason or 'the retrieved passages do not answer this.'}"
                break
            cited, invalid = self._citations(text, len(passages))
            uncited = self._uncited_sentences(text)
            result.checks.update({"attempt": attempt + 1, "invalid_citations": invalid,
                                  "uncited_sentences": uncited})
            if cited and not invalid:
                result.answer, result.cited = text, cited
                break
            # One retry with explicit feedback, then refuse rather than show an uncited answer.
            messages += [
                {"role": "assistant", "content": text},
                {"role": "user", "content": "Your answer must cite the passages with tags like [S1] "
                 f"(valid tags: S1-S{len(passages)}), or reply with {INSUFFICIENT}: <reason>."},
            ]
        else:
            result.status = "insufficient_evidence"
            result.answer = ("Insufficient evidence: the model could not produce an answer "
                             "supported by citations to the retrieved passages.")
            result.checks["gate"] = "citation check failed twice"
        return self._finish_ask(result, t0, calls)

    @staticmethod
    def _missing_terms(question: str, passages: list[dict]) -> list[str]:
        """Specific question words that occur in no retrieved passage (a hint, not a verdict)."""
        text = " ".join(p["text"] + " " + p["section"] for p in passages).lower()
        terms = [t for t in tokenize(question) if len(t) > 3 and t not in GENERIC_QUESTION_WORDS]
        stem = lambda w: w[:-3] if w.endswith("ies") else w.rstrip("s")[:max(4, len(w) - 2)]
        return [t for t in dict.fromkeys(terms) if stem(t) not in text]

    @staticmethod
    def _citations(text: str, n: int) -> tuple[list[int], list[str]]:
        tags = re.findall(r"S(\d+)", " ".join(re.findall(r"\[([^\]]+)\]", text)))
        nums = [int(t) for t in tags]
        valid = sorted({x for x in nums if 1 <= x <= n})
        invalid = sorted({f"S{x}" for x in nums if not 1 <= x <= n})
        return valid, invalid

    @staticmethod
    def _uncited_sentences(text: str) -> list[str]:
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text.strip())
        return [s for s in sentences if len(s.split()) > 4 and not re.search(r"\[S\d", s)]

    def _finish_ask(self, result: AskResult, t0: float, calls=()) -> AskResult:
        if calls:
            result.timing.update({
                "generation_s": round(sum(c.seconds for c in calls), 2),
                "model_load_s": round(sum(c.load_seconds for c in calls), 2),
                "prompt_tokens": sum(c.prompt_tokens for c in calls),
                "output_tokens": sum(c.output_tokens for c in calls),
                "tokens_per_second": calls[-1].stats.get("tokens_per_second"),
                "model_calls": len(calls),
            })
        result.timing["total_s"] = round(time.perf_counter() - t0, 2)
        result.memory = self.model.memory()
        md = [f"# Ask: {result.question}", "", f"**Status:** {result.status}", "", result.answer, ""]
        if result.cited:
            md += ["## Cited sources"]
            for i in result.cited:
                p = result.passages[i - 1]
                md.append(f"- [S{i}] {p['path']} › {p['section'] or '(intro)'}")
            md.append("")
        md += ["## Retrieved passages"]
        for p in result.passages:
            md += [f"### [{p['tag']}] {p['path']} › {p['section'] or '(intro)'}",
                   f"kind={p['kind']} cosine={p['cosine']} bm25={p['bm25']}", "", p["text"], ""]
        md += ["## Checks and timing", "```json",
               json.dumps({"checks": result.checks, "timing": result.timing,
                           "memory": result.memory, "model": result.model}, indent=2),
               "```"]
        result.saved_to = self._save("ask", result.question, asdict(result), "\n".join(md))
        return result

    # ------------------------------------------------------------ chat
    def chat(self, message: str, use_notes: bool | None = None) -> dict:
        t0 = time.perf_counter()
        if use_notes is None:
            use_notes = bool(NOTES_TRIGGER.search(message))
        messages = [{"role": "system", "content": self.assistant_prompt}]
        recent = self.history[-config.CHAT_HISTORY_MESSAGES:]
        messages += recent
        notes = []
        if use_notes:
            hits = self.retriever.search(message, k=config.CHAT_NOTES_TOP_K)
            notes = self._passage_dicts(hits, "N")
            context = "\n\n".join(f"[{n['tag']}] ({n['path']} › {n['section'] or 'intro'})\n{n['text']}"
                                  for n in notes)
            messages.append({"role": "system", "content": f"Optional notes context:\n\n{context}"})
        messages.append({"role": "user", "content": message})
        call = self.model.chat(messages, temperature=config.CHAT_TEMPERATURE)
        reply = call.text.strip()
        self.history += [{"role": "user", "content": message},
                         {"role": "assistant", "content": reply}]
        turn = {
            "mode": "chat",
            "session": self.session,
            "message": message,
            "reply": reply,
            "used_notes": [f"{n['tag']} {n['path']} › {n['section'] or '(intro)'}" for n in notes],
            "history_messages_sent": len(recent),
            "seconds": round(time.perf_counter() - t0, 2),
            "tokens_per_second": call.stats.get("tokens_per_second"),
        }
        self._append_transcript(turn)
        return turn

    def reset_chat(self) -> None:
        self.history.clear()
        self.session = _stamp()

    def _append_transcript(self, turn: dict) -> None:
        folder = config.OUTPUTS_DIR / "chat"
        folder.mkdir(parents=True, exist_ok=True)
        with (folder / f"{self.session}.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(turn, ensure_ascii=False) + "\n")
        with (folder / f"{self.session}.md").open("a", encoding="utf-8") as f:
            notes = f"\n\n_notes consulted: {', '.join(turn['used_notes'])}_" if turn["used_notes"] else ""
            f.write(f"**You:** {turn['message']}\n\n**Atlas:** {turn['reply']}{notes}\n\n"
                    f"_({turn['seconds']}s)_\n\n---\n\n")

    # ------------------------------------------------------------ ingest
    def ingest(self, paths, force=False, replace=False, log=print):
        results, meta = ingest_mod.ingest(self.model, paths, force, replace, log)
        self._retriever = None      # reload the rebuilt index on next use
        record = {"mode": "ingest", "results": [asdict(r) for r in results], "index": meta}
        md = ["# Ingest", ""] + [
            f"- {r.source}: {r.status}; created {r.created}; updated {r.updated}; "
            f"removed {r.removed}; rejected titles {r.rejected_titles}; model {r.model_seconds}s"
            for r in results
        ] + ["", f"Index: {meta}"]
        saved = self._save("ingest", "_".join(r.source for r in results)[:40], record, "\n".join(md))
        return results, meta, saved
