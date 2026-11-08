#!/usr/bin/env python3
"""R94SC1 probe: locate the S320/S321/S322 quotes in the round-94 snapshots.

Read-only on the lane: every byte is read with `git cat-file` from a named
revision; nothing is written into the lane and no git mutating command runs.

It reproduces the counter's own rule (`located_quotes` + `norm_text` +
the SOURCE_ROWS snapshots at .ufo/evidence/round-94/sources/*.html) so the
located quotes this seat cites in the case-note status block are the exact
sentences the counter's `source` conjunct is satisfied by, and it prints the
file:line pointer for each.

Usage: R94SC1-quote-locations.py [lane] [rev]
"""
import os
import re
import subprocess
import sys

LANE = sys.argv[1] if len(sys.argv) > 1 else "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = sys.argv[2] if len(sys.argv) > 2 else "7084358c732ebe1334c2eb9a352c3ed96b547f7c"
# "r94" (default) or "r93": the round whose reader, lesson and snapshots are read.
ROUND = sys.argv[3] if len(sys.argv) > 3 else "r94"

if ROUND == "r93":
    SOURCE_ROWS = {
        "S320": ".ufo/evidence/round-93/sources/s320.html",
        "S321": ".ufo/evidence/round-93/sources/s321.html",
        "S322": ".ufo/evidence/round-93/sources/s322.html",
    }
    LESSON_PATH = "corpus/lessons/round-93.md"
else:
    SOURCE_ROWS = {
        "S320": ".ufo/evidence/round-94/sources/s320.html",
        "S321": ".ufo/evidence/round-94/sources/s321.html",
        "S322": ".ufo/evidence/round-94/sources/s322.html",
    }
    LESSON_PATH = "corpus/lessons/round-94.md"


def blob(rev, path):
    p = subprocess.run(["git", "-C", LANE, "cat-file", "blob", "%s:%s" % (rev, path)],
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None


def norm_text(s):
    """Byte-identical to measure-v94.py's norm_text."""
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    import html as htmlmod
    s = htmlmod.unescape(s)
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2014", "-").replace("\u2013", "-").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).strip()


def located_quotes(lesson_text):
    """Byte-identical to measure-v94.py's located_quotes."""
    out = {sid: [] for sid in SOURCE_ROWS}
    for line in lesson_text.split("\n"):
        quoted = re.findall(r'"([^"\n]{3,300})"', line)
        if not quoted:
            continue
        for sid in SOURCE_ROWS:
            if sid in line:
                for q in quoted:
                    if 1 <= len(q.split()) <= 25:
                        out[sid].append(q)
    return out


def html_lines(snap_bytes):
    """Line numbers (1-based) of the raw html lines whose text contains a token."""
    return snap_bytes.decode("utf-8", errors="replace").split("\n")


def locate(snap_bytes, quote):
    """The html line numbers that carry the quote (tags stripped per line)."""
    hits = []
    for i, raw in enumerate(html_lines(snap_bytes), 1):
        if norm_text(raw) and norm_text(raw) in norm_text(quote):
            hits.append(i)
    if hits:
        return hits
    # the sentence may wrap across html lines: report the contiguous run
    lines = html_lines(snap_bytes)
    for i in range(len(lines)):
        for j in range(i + 1, min(i + 4, len(lines)) + 1):
            span = norm_text("\n".join(lines[i - 1:j]))
            if span and norm_text(quote) in span:
                hits.append((i, j))
                break
        if hits:
            break
    return hits


def main():
    print("LANE %s" % LANE)
    print("REV  %s" % REV)
    lesson_b = blob(REV, LESSON_PATH)
    lesson = lesson_b.decode("utf-8", errors="replace") if lesson_b else ""
    quotes = located_quotes(lesson)
    accepted_total = 0
    for sid, snap in sorted(SOURCE_ROWS.items()):
        sb = blob(REV, snap)
        print("== %s  %s  bytes=%s  sha256=%s" % (
            sid, snap, len(sb) if sb else "-",
            __import__("hashlib").sha256(sb).hexdigest() if sb else "-"))
        if sb is None:
            continue
        text = norm_text(sb.decode("utf-8", errors="replace"))
        for q in quotes.get(sid, []):
            ok = norm_text(q) in text
            if ok:
                accepted_total += 1
            where = locate(sb, q) if ok else "-"
            print("  %-6s words=%-3d %s  %s" % (
                "ACCEPT" if ok else "reject", len(q.split()),
                where if ok else "", q))
    print("ACCEPTED %d" % accepted_total)


if __name__ == "__main__":
    main()
