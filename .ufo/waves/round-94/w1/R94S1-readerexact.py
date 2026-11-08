#!/usr/bin/env python3
"""R94S1 part 3 — run the reader's OWN source check against the committed
bytes, without running the counter (the counter is another seat's scope).

Reimplements measure-v94.py's `norm_text` and `located_quotes` verbatim
(imported from the committed instrument where importable) and evaluates the
`source` conjunct's two halves on the committed snapshots + lesson + registry:

    row_ok  : a corpus/SOURCES.md line whose 8th split field is 'mined',
              1st is the sid, 11th names corpus/lessons/round-93.md
    quote_ok: a quoted span of <=25 words on a lesson line naming the sid,
              occurring in norm_text(snapshot_html)

Also reports the per-file quote presence in the round-94 .txt snapshots.

Read-only.
"""
import html as htmlmod
import importlib.util
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
INST = f"{LANE}/.ufo/evidence/round-94/c1/measure-v94.py"

spec = importlib.util.spec_from_file_location("m94", INST)
m94 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m94)

print("== reader constants ==")
print("  SOURCE_ROWS:", m94.SOURCE_ROWS)
print("  LESSON_PATH:", m94.LESSON_PATH)
print("  NOTE_PATH  :", m94.NOTE_PATH)

norm_text = m94.norm_text
located_quotes = m94.located_quotes

# ---------- registry half ----------
sreg = open(f"{LANE}/corpus/SOURCES.md", encoding="utf-8").read()
print("\n== registry half (reader-exact) ==")
for sid in m94.SOURCE_ROWS:
    row_ok = False
    for line in sreg.split("\n"):
        c = [x.strip() for x in re.sub(r"^ {0,3}", "", line).split("|")]
        if len(c) >= 13 and c[1] == sid and c[8] == "mined" and m94.LESSON_PATH in c[11]:
            row_ok = True
            break
    print(f"  {sid}: row_ok={row_ok}")

# ---------- lesson quote half, for both lessons ----------
for lesson_path in (m94.LESSON_PATH, "corpus/lessons/round-93.md"):
    print(f"\n== quote half, lesson {lesson_path} ==")
    lesson = open(f"{LANE}/{lesson_path}", encoding="utf-8").read()
    quotes = located_quotes(lesson)
    for sid, snap in m94.SOURCE_ROWS.items():
        text = norm_text(open(f"{LANE}/{snap}", encoding="utf-8").read())
        hits = []
        for q in quotes.get(sid, []):
            hits.append((norm_text(q) in text, len(q.split()), q))
        print(f"  {sid}: {len(quotes.get(sid, []))} candidate quote(s) on lines naming {sid}")
        for ok, n, q in hits:
            print(f"     {'HIT ' if ok else 'MISS'} ({n} words) {q[:110]!r}")

# ---------- round-94 .txt snapshots, per file ----------
print("\n== round-94 .txt snapshots: quote presence ==")
QS = {
    "s321.txt": [
        "The table is broken at the first empty line, or beginning of another block-level structure",
        "a single header row, a delimiter row separating the header from the data",
    ],
    "s322.txt": [
        "A fenced code block begins with a code fence, preceded by up to three spaces of indentation.",
    ],
}
for fn, qs in QS.items():
    raw = open(f"{LANE}/.ufo/evidence/round-94/sources/{fn}", encoding="utf-8").read()
    coll = re.sub(r"\s+", " ", raw).strip()
    print(f"  {fn}: bytes={len(raw.encode())} newlines={raw.count(chr(10))}")
    for q in qs:
        print(f"     {'HIT ' if re.sub(chr(92)+'s+',' ',q) in coll else 'MISS'} {q[:90]!r}")

# ---------- round-93 .txt (the registry's cited snapshots) ----------
print("\n== round-93 .txt (registry-cited): quote presence + anchors ==")
for fn, qs in QS.items():
    raw = open(f"{LANE}/.ufo/evidence/round-93/sources/{fn}", encoding="utf-8").read()
    coll = re.sub(r"\s+", " ", raw).strip()
    lines = raw.split("\n")
    print(f"  {fn}: bytes={len(raw.encode())} lines={len(lines)}")
    for q in qs:
        qq = re.sub(r"\s+", " ", q).strip()
        ln = next((i for i, l in enumerate(lines, 1) if qq in re.sub(r"\s+", " ", l)), None)
        print(f"     {'HIT ' if qq in coll else 'MISS'} line={ln}  {q[:80]!r}")

# ---------- width rule present in the round-94 snapshot ----------
print("\n== GFM width-rule sentences in the round-94 snapshot ==")
g = norm_text(open(f"{LANE}/.ufo/evidence/round-94/sources/s321.html", encoding="utf-8").read())
for label, q in (
    ("width", "The header row must match the delimiter row in the number of cells."),
    ("remainder", "The remainder of the table's rows may vary in the number of cells."),
    ("excess", "If there are greater, the excess is ignored"),
    ("empty cells", "If there are a number of cells fewer than the number of cells in the header row, empty cells are inserted."),
):
    print(f"  {label:12} present={q in g}  {q[:95]!r}")

print("\nR94S1_PART3_DONE")
