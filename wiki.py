"""wiki - a personal wiki CLI backed by a local Gemma model.

Usage:
  python wiki.py help
  python wiki.py chat
  python wiki.py ask "question"
  python wiki.py search "query" [-k 5] [--scope all|source|note]
  python wiki.py ingest <file-or-folder>... [--force] [--replace]
  python wiki.py status
"""
import argparse
import json
import platform
import socket
import sys
import textwrap

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from wikicli import config                       # noqa: E402
from wikicli.harness import Harness               # noqa: E402
from wikicli.llm import HarnessError              # noqa: E402

HELP = f"""\
wiki - personal wiki assistant running on local Gemma ({config.CHAT_MODEL} via Ollama)

MODES
  chat                 Talk with Atlas, your assistant. Keeps conversation context and
                       handles casual questions and drafting. It only looks at your notes
                       when you mention them ("in my notes...") or type /notes.
  ask "question"       Neutral factual answer built ONLY from retrieved wiki passages,
                       with [S#] citations, or an explicit insufficient-evidence reply.
                       Stateless: never sees chat history.
  search "query"       Returns the original passages and file paths. No model answer.
  ingest <path>...     Preserve a source (.md/.txt/.pdf) in vault/Sources, draft linked
                       concept notes with Gemma, and rebuild the index. Re-ingesting an
                       unchanged file is a no-op; --force redrafts the source's notes in place.
  rebuild              Re-apply naming rules and curation.json (renames, topic folders),
                       re-render notes, links and index pages, and reindex. No model calls.
  status               Show the model, runtime, index size and network state.
  help                 Show this message.

CHAT COMMANDS
  /ask <question>      Run ask mode from inside chat (chat history is NOT passed to it)
  /search <query>      Run search mode from inside chat
  /notes <message>     Chat, and include the top wiki passages as optional context
  /reset               Clear the conversation        /exit   Leave chat

Everything runs locally: models via Ollama at {config.OLLAMA_URL}, index in .index/,
saved outputs in outputs/. There is no cloud fallback.
"""


def wrap(text: str, indent: str = "  ") -> str:
    return "\n".join(textwrap.fill(p, 96, initial_indent=indent, subsequent_indent=indent)
                     if p.strip() else "" for p in text.splitlines())


def print_search(result: dict) -> None:
    print(f"Top {len(result['passages'])} passages for: {result['query']}  ({result['seconds']}s)\n")
    for p in result["passages"]:
        print(f"[{p['tag']}] {p['path']}")
        print(f"     section: {p['section'] or '(intro)'} | {p['kind']} | "
              f"cosine {p['cosine']} | bm25 {p['bm25']}")
        print(wrap(p["text"], "     "))
        print()
    print(f"saved: {result['saved_to']}")


def print_ask(r) -> None:
    print(f"Q: {r.question}\n")
    print(wrap(r.answer, ""))
    print()
    if r.cited:
        print("Sources:")
        for i in r.cited:
            p = r.passages[i - 1]
            print(f"  [S{i}] {p['path']} › {p['section'] or '(intro)'}")
    else:
        print("Retrieved (none cited):")
        for p in r.passages[:3]:
            print(f"  [{p['tag']}] {p['path']} › {p['section'] or '(intro)'} (cosine {p['cosine']})")
    t = r.timing
    print(f"\n[{r.status} | {r.model} | total {t.get('total_s')}s, "
          f"generation {t.get('generation_s', 0)}s, {t.get('tokens_per_second') or '-'} tok/s]")
    print(f"saved: {r.saved_to}")


def internet_state() -> str:
    try:
        socket.create_connection(("1.1.1.1", 443), timeout=2).close()
        return "online (internet reachable)"
    except OSError:
        return "OFFLINE (no internet connection)"


def cmd_status(h: Harness) -> None:
    import psutil
    from wikicli import retrieval
    meta = json.loads(retrieval.META_FILE.read_text()) if retrieval.META_FILE.exists() else {}
    vm = psutil.virtual_memory()
    print(f"model:       {config.CHAT_MODEL} (chat/ask/ingest), {config.EMBED_MODEL} (embeddings)")
    print(f"runtime:     Ollama {h.model.version()} at {config.OLLAMA_URL}")
    print(f"device:      {platform.platform()} | {platform.processor()} | "
          f"RAM {vm.total / 2**30:.1f} GB, {vm.available / 2**30:.1f} GB available")
    print(f"index:       {meta or 'not built yet'}")
    print(f"loaded:      {h.model.memory() or 'no model loaded right now'}")
    print(f"network:     {internet_state()}")


def chat_loop(h: Harness) -> None:
    print(f"Atlas (local {config.CHAT_MODEL}). Type /help for commands, /exit to quit.")
    while True:
        try:
            line = input("\nyou> ").lstrip("﻿").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if not sys.stdin.isatty():
            print(line)  # echo piped input so saved terminal logs read like a session
        cmd, _, rest = line.partition(" ")
        try:
            if cmd in ("/exit", "/quit"):
                break
            elif cmd == "/help":
                print(HELP)
            elif cmd == "/reset":
                h.reset_chat()
                print("(conversation cleared)")
            elif cmd == "/ask":
                print_ask(h.ask(rest))
            elif cmd == "/search":
                print_search(h.search(rest))
            else:
                use_notes = True if cmd == "/notes" else None
                message = rest if cmd == "/notes" else line
                turn = h.chat(message, use_notes=use_notes)
                print(f"\natlas> {turn['reply']}")
                extra = f" | notes: {', '.join(turn['used_notes'])}" if turn["used_notes"] else ""
                print(f"       ({turn['seconds']}s, history msgs sent: {turn['history_messages_sent']}{extra})")
        except HarnessError as exc:
            print(f"error: {exc}")
    print(f"transcript saved: outputs/chat/{h.session}.md")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="wiki", add_help=False)
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("help")
    sub.add_parser("chat")
    sub.add_parser("status")
    sub.add_parser("rebuild")
    p_ask = sub.add_parser("ask")
    p_ask.add_argument("question", nargs="+")
    p_search = sub.add_parser("search")
    p_search.add_argument("query", nargs="+")
    p_search.add_argument("-k", type=int, default=config.SEARCH_TOP_K)
    p_search.add_argument("--scope", choices=["all", "source", "note"], default="all")
    p_ingest = sub.add_parser("ingest")
    p_ingest.add_argument("paths", nargs="+")
    p_ingest.add_argument("--force", action="store_true", help="redraft notes even if unchanged")
    p_ingest.add_argument("--replace", action="store_true", help="archive and replace a same-named source")
    args = parser.parse_args(argv)

    if args.command in (None, "help"):
        print(HELP)
        return 0
    try:
        h = Harness()
        if args.command == "chat":
            chat_loop(h)
        elif args.command == "status":
            cmd_status(h)
        elif args.command == "rebuild":
            from wikicli import ingest as ingest_mod
            renamed, meta = ingest_mod.rebuild(h.model)
            print("renamed: " + (", ".join(renamed) or "nothing"))
            print(f"index: {meta['chunks']} chunks from {meta['sources']} sources and "
                  f"{meta['notes']} notes ({meta['newly_embedded']} newly embedded)")
        elif args.command == "ask":
            print_ask(h.ask(" ".join(args.question)))
        elif args.command == "search":
            print_search(h.search(" ".join(args.query), k=args.k, scope=args.scope))
        elif args.command == "ingest":
            from pathlib import Path
            results, meta, saved = h.ingest([Path(p) for p in args.paths], args.force, args.replace)
            print()
            for r in results:
                print(f"{r.source}: {r.status}")
                for label, items in (("created", r.created), ("updated", r.updated),
                                     ("renamed", r.renamed), ("removed", r.removed),
                                     ("rejected titles", r.rejected_titles)):
                    if items:
                        print(f"  {label}: {', '.join(items)}")
            print(f"index: {meta['chunks']} chunks from {meta['sources']} sources and "
                  f"{meta['notes']} notes ({meta['newly_embedded']} newly embedded)")
            print(f"saved: {saved}")
    except HarnessError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
