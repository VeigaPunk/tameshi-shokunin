#!/usr/bin/env python3
"""R94S1 part 4 — exact line-model characterisation.

Establishes, for each of the three quotes and for the two width-rule sentences:
  * the line span under each documented strip convention,
  * the line span in the lane's committed round-93 .txt snapshots (the files the
    registry anchor and the round-93 lesson cite),
  * whether the reader's own `norm_text` (fully collapsed, one line) can be
    sensitive to line numbers at all.

Read-only.
"""
import html as htmlmod
import importlib.util
import re

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
spec = importlib.util.spec_from_file_location("m94", f"{LANE}/.ufo/evidence/round-94/c1/measure-v94.py")
m94 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m94)


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def strip_A(text):
    """per-line tag strip (tags removed, no space), every original line kept"""
    return [re.sub(r"<[^>]+>", "", ln) for ln in text.split("\n")]


def strip_B(text):
    """reader normalisation applied per line, line structure kept"""
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s)
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("\u00a0", " ")
    return s.split("\n")


def strip_C(text):
    """script/style removed, tags removed without space, all lines kept"""
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", text, flags=re.S | re.I)
    return [re.sub(r"<[^>]+>", "", ln) for ln in s.split("\n")]


def span(lines, quote):
    q = norm(quote)
    for i in range(len(lines)):
        for w in (1, 2, 3, 4):
            if i + w > len(lines):
                break
            if q in norm(" ".join(lines[i:i + w])):
                return i + 1, i + w
    return None, None


CASES = [
    ("S321", "s321.html", "s321.txt",
     "The table is broken at the first empty line, or beginning of another block-level structure"),
    ("S321", "s321.html", "s321.txt",
     "a single header row, a delimiter row separating the header from the data"),
    ("S322", "s322.html", "s322.txt",
     "A fenced code block begins with a code fence, preceded by up to three spaces of indentation."),
    ("S321", "s321.html", "s321.txt",
     "The header row must match the delimiter row in the number of cells"),
    ("S321", "s321.html", "s321.txt",
     "The remainder of the table’s rows may vary in the number of cells"),
]

print("== per-model line spans ==")
for sid, html, txt, q in CASES:
    raw = open(f"{LANE}/.ufo/evidence/round-94/sources/{html}", encoding="utf-8").read()
    r93 = open(f"{LANE}/.ufo/evidence/round-93/sources/{txt}", encoding="utf-8").read().split("\n")
    a = span(strip_A(raw), q)
    b = span(strip_B(raw), q)
    c = span(strip_C(raw), q)
    t = span(r93, q)
    print(f"\n  {sid} {q[:78]!r}")
    print(f"    A (strip tags, keep lines)      : {a}")
    print(f"    B (reader norm per line)        : {b}")
    print(f"    C (drop script/style, strip)    : {c}")
    print(f"    round-93 .txt (cited by lane)   : {t}")
    if t[0]:
        for ln in range(t[0], t[1] + 1):
            print(f"        .txt:{ln}: {r93[ln-1][:120]!r}")

print("\n== the reader's norm_text is line-insensitive ==")
for sid, html in (("S321", "s321.html"), ("S322", "s322.html")):
    t = m94.norm_text(open(f"{LANE}/.ufo/evidence/round-94/sources/{html}", encoding="utf-8").read())
    print(f"  {sid}: norm_text -> {t.count(chr(10))+1} line(s), {len(t)} chars")

print("\n== registry anchor lines reproduce in the round-93 .txt? ==")
reg = open(f"{LANE}/corpus/SOURCES.md", encoding="utf-8").read()
for sid in ("S321", "S322"):
    for line in reg.split("\n"):
        c = [x.strip() for x in re.sub(r"^ {0,3}", "", line).split("|")]
        if len(c) >= 13 and c[1] == sid:
            anchor = c[6]
            m = re.search(r"line (\d+)", anchor)
            ln = int(m.group(1))
            fn = "s321.txt" if sid == "S321" else "s322.txt"
            lines = open(f"{LANE}/.ufo/evidence/round-93/sources/{fn}", encoding="utf-8").read().split("\n")
            print(f"  {sid} anchor line {ln} -> {lines[ln-1][:120]!r}")
            break

print("\n== lesson-recorded quote anchors (round-93 lesson) reproduce? ==")
for fn, ln in (("s321.txt", 4496), ("s321.txt", 4396), ("s322.txt", 2619)):
    lines = open(f"{LANE}/.ufo/evidence/round-93/sources/{fn}", encoding="utf-8").read().split("\n")
    prev = lines[ln - 2][:100] if ln >= 2 else ""
    print(f"  {fn}:{ln} -> {lines[ln-1][:120]!r}   (prev line: {prev!r})")
