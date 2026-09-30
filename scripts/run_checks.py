"""Run the assignment's test suite through the real CLI and save evidence.

Each check launches `python wiki.py ...` as a fresh process (so the CLI is
restarted), records the exact command, its full output and wall time, and
samples the memory of the local Ollama processes in the background.

  python scripts/run_checks.py --label offline --ingest "inbox/Class 8 - Strategic and Repeated Interactions.md"
"""
import argparse
import json
import platform
import socket
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

import psutil

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

ASK_TESTS = [
    ("Q1 answerable", "In the joint venture exercise, what is Firm A's added value, and what range of payoffs should Firm A expect?"),
    ("Q2 answerable", "Why did the incumbents retaliate against Ryanair's first entry even though accommodating looked more profitable in the short run?"),
    ("Q3 answerable", "What major mistake did Holland Sweetener Company make with Coke and Pepsi, and what should it have done instead?"),
    ("Q4 unsupported", "What did the course conclude about Disney's boundaries of the firm?"),
]
SEARCH_TESTS = ["counter-positioning incumbent retaliate", "Enterprise referrals body shops insurance"]
CHAT_SCRIPT = [
    "Hey Atlas! I have a strategy exam next week and I'm a bit nervous. Any quick tips for staying calm?",
    "Can you draft a short message to my study group proposing we meet Thursday at 6pm to review?",
    "Make it more casual and add that I'll bring snacks.",
    "By the way, my favorite company is Patagonia.",
    "/ask What is my favorite company?",
    "What's my favorite company again?",
    "/notes In my notes, what is counter-positioning? One or two sentences.",
    "/exit",
]


class MemorySampler(threading.Thread):
    """Samples memory of the local runtime (ollama + its llama-server runners) every 0.5 s."""

    def __init__(self):
        super().__init__(daemon=True)
        self.peak_gb = 0.0          # working set (resident)
        self.peak_private_gb = 0.0  # private committed bytes
        self.peak_system_used_gb = 0.0
        self.running = True

    def run(self):
        while self.running:
            rss = private = 0
            for p in psutil.process_iter(["name", "memory_info"]):
                try:
                    name = (p.info["name"] or "").lower()
                    if name.startswith(("ollama", "llama")):
                        mem = p.info["memory_info"]
                        rss += mem.rss
                        private += getattr(mem, "private", mem.rss)
                except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError):
                    pass
            self.peak_gb = max(self.peak_gb, rss / 2**30)
            self.peak_private_gb = max(self.peak_private_gb, private / 2**30)
            self.peak_system_used_gb = max(self.peak_system_used_gb, psutil.virtual_memory().used / 2**30)
            time.sleep(0.5)


def ollama_reported() -> list[dict]:
    try:
        import ollama
        return [{"model": m.model, "allocated_gb": round(m.size / 1e9, 2),
                 "gpu_gb": round((m.size_vram or 0) / 1e9, 2)} for m in ollama.ps().models]
    except Exception as exc:  # best-effort evidence only
        return [{"error": str(exc)}]


def network_state() -> str:
    try:
        socket.create_connection(("1.1.1.1", 443), timeout=2).close()
        return "ONLINE"
    except OSError:
        return "OFFLINE"


def run(args: list[str], stdin: str | None = None) -> dict:
    cmd = [PY, "wiki.py", *args]
    start = time.perf_counter()
    proc = subprocess.run(cmd, cwd=ROOT, input=stdin, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=3600)
    seconds = time.perf_counter() - start
    shown = "python wiki.py " + " ".join(f'"{a}"' if " " in a else a for a in args)
    return {"command": shown, "stdin": stdin, "seconds": round(seconds, 1),
            "exit": proc.returncode, "output": (proc.stdout + proc.stderr).rstrip()}


def note_files() -> list[str]:
    vault = ROOT / "vault"
    return sorted(p.relative_to(vault).as_posix() for p in vault.rglob("*.md")
                  if not p.relative_to(vault).parts[0].startswith("."))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True, help="e.g. online or offline")
    ap.add_argument("--ingest", help="a new source to ingest at the start of the run")
    opts = ap.parse_args()

    if "offline" in opts.label and network_state() == "ONLINE":
        sys.exit("The internet is still reachable. Turn on Airplane mode (or disconnect Wi-Fi "
                 "and Ethernet), wait a few seconds, and run this again.")
    out_dir = ROOT / "evidence" / opts.label
    out_dir.mkdir(parents=True, exist_ok=True)
    sampler = MemorySampler()
    sampler.start()
    vm = psutil.virtual_memory()
    net = network_state()
    started = datetime.now().isoformat(timespec="seconds")
    steps = []

    def step(title, args, stdin=None):
        print(f"-> {title}", flush=True)
        net_before = network_state()
        result = run(args, stdin)
        result["network"] = f"{net_before} -> {network_state()}"
        result["title"] = title
        result["peak_runtime_gb_so_far"] = round(sampler.peak_gb, 2)
        steps.append(result)
        return result

    step("Status (model, runtime, device, network)", ["status"])
    step("Help", ["help"])
    if opts.ingest:
        before = note_files()
        step(f"Ingest new source: {opts.ingest}", ["ingest", opts.ingest])
        after = note_files()
        steps[-1]["files_added"] = sorted(set(after) - set(before))
    before = note_files()
    target = opts.ingest or "vault/Sources/Class 3 - Added Value and Irreplaceability.md"
    step(f"Re-ingest the same source (duplicate check): {target}", ["ingest", target])
    after = note_files()
    steps[-1]["duplicate_check"] = {"files_before": len(before), "files_after": len(after),
                                    "new_files": sorted(set(after) - set(before))}
    for q in SEARCH_TESTS:
        step(f"Search: {q}", ["search", q])
    for label, q in ASK_TESTS:
        step(f"Ask {label}", ["ask", q])
    step("Chat session: casual, drafting, follow-up, ask/chat separation, notes",
         ["chat"], stdin="\n".join(CHAT_SCRIPT) + "\n")
    step("Status after tests (loaded model memory)", ["status"])

    sampler.running = False
    finished = datetime.now().isoformat(timespec="seconds")
    summary = {
        "label": opts.label,
        "network_at_start": net,
        "network_at_end": network_state(),
        "started": started,
        "finished": finished,
        "device": {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "ram_total_gb": round(vm.total / 2**30, 1),
            "ram_available_at_start_gb": round(vm.available / 2**30, 1),
        },
        "peak_runtime_working_set_gb": round(sampler.peak_gb, 2),
        "peak_runtime_private_gb": round(sampler.peak_private_gb, 2),
        "peak_system_ram_used_gb": round(sampler.peak_system_used_gb, 2),
        "ollama_reported_models": ollama_reported(),
        "steps": [{k: s[k] for k in ("title", "command", "seconds", "exit", "network")} for s in steps],
    }
    summary["offline_throughout"] = all(s["network"] == "OFFLINE -> OFFLINE" for s in steps)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = [f"# Test run: {opts.label}", "",
          f"- Started {started}, finished {finished}",
          f"- Network at start: **{net}**, at end: **{summary['network_at_end']}** "
          "(TCP check to 1.1.1.1:443, repeated before and after every step)",
          f"- Offline for every step: **{summary['offline_throughout']}**",
          f"- Device: {summary['device']['platform']}, {summary['device']['processor']}, "
          f"{summary['device']['ram_total_gb']} GB RAM "
          f"({summary['device']['ram_available_at_start_gb']} GB available at start)",
          f"- Peak memory of the local runtime (ollama + llama-server) during the run: "
          f"**{summary['peak_runtime_working_set_gb']} GB working set, "
          f"{summary['peak_runtime_private_gb']} GB private**; peak system RAM in use "
          f"{summary['peak_system_ram_used_gb']} GB of {summary['device']['ram_total_gb']} GB",
          f"- Ollama-reported model allocations at end: `{json.dumps(summary['ollama_reported_models'])}`",
          "",
          "| Step | Wall time (s) | Exit | Network before -> after |", "|---|---|---|---|"]
    md += [f"| {s['title']} | {s['seconds']} | {s['exit']} | {s['network']} |" for s in steps]
    for s in steps:
        md += ["", f"## {s['title']}", "", "```text", f"> {s['command']}"]
        if s["stdin"]:
            md += ["(stdin:)"] + [f"  {line}" for line in s["stdin"].splitlines()]
        md += [s["output"], "```"]
        for key in ("files_added", "duplicate_check"):
            if key in s:
                md += ["", f"**{key}:** `{json.dumps(s[key])}`"]
    (out_dir / "transcript.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"evidence written to {out_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
