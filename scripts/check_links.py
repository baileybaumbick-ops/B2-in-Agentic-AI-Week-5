"""Check that every [[wikilink]] in the vault resolves to a page (and heading).

Also reports orphan notes (no incoming links) and notes with no source link.
  python scripts/check_links.py
"""
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
VAULT = Path(__file__).resolve().parent.parent / "vault"
LINK = re.compile(r"\[\[([^\]|#]+)(?:#([^\]|]+))?(?:\|[^\]]+)?\]\]")

pages = {p.stem: p for p in VAULT.rglob("*.md") if ".obsidian" not in p.parts}
dupes = [name for name, n in Counter(p.stem for p in VAULT.rglob("*.md")).items() if n > 1]
headings = {
    stem: {m.strip() for m in re.findall(r"^#{1,6} (.+)$", p.read_text(encoding="utf-8"), re.M)}
    for stem, p in pages.items()
}

total, broken, incoming = 0, [], Counter()
for stem, path in pages.items():
    for target, heading in LINK.findall(path.read_text(encoding="utf-8")):
        total += 1
        target = target.strip()
        if target not in pages:
            broken.append(f"{path.relative_to(VAULT)} -> [[{target}]] (missing page)")
        elif heading and heading.strip() not in headings[target]:
            broken.append(f"{path.relative_to(VAULT)} -> [[{target}#{heading}]] (missing heading)")
        elif target != stem:
            incoming[target] += 1

concepts = [s for s, p in pages.items() if p.parent.name not in ("Sources", "vault")]
orphans = [s for s in concepts if incoming[s] == 0]
no_source = [s for s in concepts if "[[Class " not in pages[s].read_text(encoding="utf-8")]

print(f"pages: {len(pages)} ({len(concepts)} concept notes)")
print(f"links checked: {total}, broken: {len(broken)}")
for b in broken:
    print(f"  BROKEN {b}")
print(f"duplicate filenames: {dupes or 'none'}")
print(f"concept notes with no incoming links: {orphans or 'none'}")
print(f"concept notes without a source link: {no_source or 'none'}")
sys.exit(1 if broken or dupes else 0)
