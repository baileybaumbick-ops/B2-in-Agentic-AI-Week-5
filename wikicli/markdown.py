"""Small Markdown helpers: front matter, headings and sections."""
import re

FRONT_MATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.S)


def split_front_matter(text: str) -> tuple[dict, str]:
    """Return (flat key/value dict, body). Only simple `key: value` lines are parsed."""
    match = FRONT_MATTER.match(text)
    if not match:
        return {}, text
    meta = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "-")):
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta, text[match.end():]


def title_of(body: str, fallback: str) -> str:
    match = re.search(r"^# (.+)$", body, re.M)
    return match.group(1).strip() if match else fallback


def sections(body: str) -> list[tuple[str, str]]:
    """Split a body into (heading, text) pairs on level-2 headings.

    Text before the first `## ` heading is returned under heading "".
    """
    parts: list[tuple[str, str]] = []
    heading, buf = "", []
    for line in body.splitlines():
        if line.startswith("## "):
            parts.append((heading, "\n".join(buf).strip()))
            heading, buf = line[3:].strip(), []
        elif line.startswith("# "):
            continue  # the page title
        else:
            buf.append(line)
    parts.append((heading, "\n".join(buf).strip()))
    return [(h, t) for h, t in parts if t]
