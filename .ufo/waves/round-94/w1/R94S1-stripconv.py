#!/usr/bin/env python3
"""R94S1 part 2 — determine which tag-strip convention reproduces the line
numbers the round-93/94 lesson records, and locate the GFM width rule.

Read-only over scratch copies of the committed snapshots.
"""
import html
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
SCRATCH = "/fast/scratch/hyaku/tameshi-r94/R94S1"

GFM = open(f"{SCRATCH}/gfm.body", encoding="utf-8", errors="replace").read()
CM = open(f"{SCRATCH}/cm.body", encoding="utf-8", errors="replace").read()

Q1 = "The table is broken at the first empty line, or beginning of another block-level structure"
Q2 = "a single header row, a delimiter row separating the header from the data"
Q3 = "A fenced code block begins with a code fence, preceded by up to three spaces of indentation."
WIDTH = "The header row must match the delimiter row in the number of cells"
REMAINDER = "The remainder of the table's rows may vary in the number of cells"

TARGET = {  # what the lane's lesson records
    "gfm_Q1_broken": (GFM, Q1, 4496),
    "gfm_Q2_header": (GFM, Q2, 4396),
    "cm_Q3_fence": (CM, Q3, 2619),
}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def variants(text):
    """Yield (name, lines) for several plausible tag-strip conventions."""
    # v1: per-line tag strip, keep every line
    lines = [re.sub(r"<[^>]+>", "", ln) for ln in text.split("\n")]
    yield "v1_strip_keep_all_lines", lines

    # v2: strip, then drop lines that became empty
    yield "v2_strip_drop_empty_lines", [ln for ln in lines if ln.strip() != ""]

    # v3: remove script/style blocks entirely (content included), then strip
    t = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", text)
    lines3 = [re.sub(r"<[^>]+>", "", ln) for ln in t.split("\n")]
    yield "v3_drop_script_style", lines3
    yield "v4_drop_script_style_drop_empty", [ln for ln in lines3 if ln.strip() != ""]

    # v5: strip, drop empty, then collapse consecutive whitespace within a line
    lines5 = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", ln)).strip()
              for ln in text.split("\n")]
    yield "v5_strip_trim", [ln for ln in lines5 if ln != ""]

    # v6: remove HTML comments and script/style, strip, drop empty
    t = re.sub(r"(?is)<!--.*?-->", "", text)
    t = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", t)
    lines6 = [re.sub(r"<[^>]+>", "", ln) for ln in t.split("\n")]
    yield "v6_nocomment_noscript_drop_empty", [ln for ln in lines6 if ln.strip() != ""]

    # v7: same as v6 but keep all lines
    yield "v7_nocomment_noscript_keep_all", lines6

    # v8: strip tags then unescape entities, drop empty
    lines8 = [html.unescape(re.sub(r"<[^>]+>", "", ln)) for ln in text.split("\n")]
    yield "v8_unescape_drop_empty", [ln for ln in lines8 if ln.strip() != ""]

    # v9: whole doc collapsed to one line (the committed .txt convention)
    yield "v9_single_line", [norm(re.sub(r"<[^>]+>", " ", text))]


def find(lines, quote):
    q = norm(quote)
    for i, ln in enumerate(lines, 1):
        if q in norm(ln):
            return i
    # multi-line join
    for i in range(len(lines)):
        for span in (2, 3, 4):
            chunk = norm(" ".join(lines[i:i + span]))
            if q in chunk:
                return i + 1
    return None


def find_join_start(lines, quote):
    """Line number where the *quoted span* starts (may span lines)."""
    q = norm(quote)
    for i in range(len(lines)):
        for span in (1, 2, 3, 4):
            chunk = norm(" ".join(lines[i:i + span]))
            if q in chunk:
                return i + 1
    return None


print("=== convention search: which strip yields the lane-recorded line? ===")
for name, (text, quote, want) in TARGET.items():
    print(f"\n-- {name}: recorded line {want} --")
    for vname, lines in variants(text):
        ln = find(lines, quote)
        flag = "  <== MATCH" if ln == want else ""
        print(f"   {vname:42} -> line {ln}{flag}")

print("\n=== GFM width rule + remainder rule, per convention (v1) ===")
lines = list(variants(GFM))[0][1]
for label, q in (("width", WIDTH), ("remainder", REMAINDER), ("Q1", Q1), ("Q2", Q2)):
    ln = find(lines, q)
    print(f"  {label:10} line {ln}: {norm(lines[ln - 1])[:200] if ln else 'NOT FOUND'}")

print("\n=== committed .txt files: shape ===")
for f in ("s321.txt", "s322.txt"):
    p = f"{LANE}/.ufo/evidence/round-94/sources/{f}"
    raw = open(p, encoding="utf-8", errors="replace").read()
    print(f"  {f}: bytes={len(raw.encode())} newlines={raw.count(chr(10))} lines={len(raw.split(chr(10)))}")
    print(f"     quote Q present? ", end="")
    for label, q in (("Q1", Q1), ("Q2", Q2), ("Q3", Q3)):
        if norm(q) in norm(raw):
            print(f"{label}=yes ", end="")
    print()
    # does the committed txt contain the width rule?
    for label, q in (("width", WIDTH), ("remainder", REMAINDER)):
        print(f"     {label} present in committed txt: {norm(q) in norm(raw)}")
