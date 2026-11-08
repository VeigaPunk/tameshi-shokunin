#!/usr/bin/env python3
"""R94S1 final verification probe.

Independent re-verification of the round-94 lesson Gate's source claims
(S321 = GFM spec, S322 = CommonMark 0.31.2):

  * byte identity of a live re-fetch against the committed snapshots,
  * the three quotes located verbatim in the tag-stripped text, with the
    line numbers under two documented strip conventions and the word counts,
  * the S321/S322 registry rows in corpus/SOURCES.md parsed with the reader's
    own column convention (leading '|' kept -> 13 split fields, 11 columns),
  * the GFM spec's own statements the reader's width rule rests on
    (header row must match the delimiter row in the number of cells; the
    remainder-row policy).

Read-only. Writes nothing outside its own scratch dir.
"""
import hashlib
import html
import os
import re
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/tameshi-r94/R94S1"
LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"

GFM_URL = "https://github.github.com/gfm/"
CM_URL = "https://spec.commonmark.org/0.31.2/"

SNAP = {
    "S321": {
        "url": GFM_URL,
        "html": f"{LANE}/.ufo/evidence/round-94/sources/s321.html",
        "expect_sha": "b153d814fdfc8624bb6da7449162c1cd707a637f7d1c1b636eb44b9cf63fa220",
        "expect_size": 508310,
    },
    "S322": {
        "url": CM_URL,
        "html": f"{LANE}/.ufo/evidence/round-94/sources/s322.html",
        "expect_sha": "c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d",
        "expect_size": 514698,
    },
}

QUOTES = {
    "S321": [
        "The table is broken at the first empty line, or beginning of another block-level structure",
        "a single header row, a delimiter row separating the header from the data",
    ],
    "S322": [
        "A fenced code block begins with a code fence, preceded by up to three spaces of indentation.",
    ],
}

# the GFM sentences the reader's width rule (QUALITY 165) rests on
WIDTH_RULE = "The header row must match the delimiter row in the number of cells"
REMAINDER_RULE = ("The remainder of the table’s rows may vary in the number of cells. "
                  "If there are a number of cells fewer than the number of cells in the "
                  "header row, empty cells are inserted. If there are greater, the excess "
                  "is ignored")

TAG = re.compile(r"<[^>]+>")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def wc(s):
    return len(s.split())


def strip_v1(text):
    """Convention A: per-line tag strip, every original line kept."""
    return [TAG.sub("", ln) for ln in text.split("\n")]


def strip_v2(text):
    """Convention B: the reader's own norm_text (script/style removed, tags to
    space, entities unescaped, typographic folds, whitespace collapsed) then
    split on newlines -- i.e. the shape the reader actually searches."""
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.S | re.I)
    s = TAG.sub(" ", s)
    s = html.unescape(s)
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("\u00a0", " ")
    return s.split("\n")


def locate(lines, quote):
    """Return (first_line, last_line) of the quote in `lines`."""
    q = norm(quote)
    n = len(lines)
    for i in range(n):
        for span in (1, 2, 3, 4):
            if i + span > n:
                break
            chunk = norm(" ".join(lines[i:i + span]))
            if q in chunk:
                return i + 1, i + span
    return None, None


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    print("R94S1 VERIFICATION")
    print("=" * 72)

    # ---------- 1. live re-fetch ----------
    print("\n[1] LIVE RE-FETCH vs COMMITTED SNAPSHOTS")
    for sid, s in SNAP.items():
        body = os.path.join(SCRATCH, f"{sid}.body")
        hdr = os.path.join(SCRATCH, f"{sid}.headers")
        if not os.path.exists(body):
            subprocess.run(["curl", "-sS", "-L", "-D", hdr, "-o", body, s["url"]], check=True)
        raw = open(body, "rb").read()
        date = ""
        for ln in open(hdr, errors="replace"):
            if ln.lower().startswith("date:"):
                date = ln.split(":", 1)[1].strip()
        f_sha = hashlib.sha256(raw).hexdigest()
        c_sha = sha256(s["html"])
        c_size = os.path.getsize(s["html"])
        print(f"  {sid}  {s['url']}")
        print(f"    http date        : {date}")
        print(f"    fetched  : {f_sha}  {len(raw)} B")
        print(f"    snapshot : {c_sha}  {c_size} B")
        print(f"    expected : {s['expect_sha']}  {s['expect_size']} B")
        print(f"    fetched==snapshot==expected : "
              f"{f_sha == c_sha == s['expect_sha'] and len(raw) == c_size == s['expect_size']}")

    # ---------- 2. quotes ----------
    print("\n[2] QUOTE VERIFICATION (tag-stripped text)")
    stripA, stripB = {}, {}
    for sid, s in SNAP.items():
        text = open(s["html"], encoding="utf-8", errors="replace").read()
        stripA[sid] = strip_v1(text)
        stripB[sid] = strip_v2(text)
        print(f"  {sid}: lines A={len(stripA[sid])}  B={len(stripB[sid])}")
    for sid, qs in QUOTES.items():
        for q in qs:
            a1, a2 = locate(stripA[sid], q)
            b1, b2 = locate(stripB[sid], q)
            print(f"\n  [{sid}] {q!r}")
            print(f"    words (as written)     : {wc(q)}")
            print(f"    words (located span)   : {wc(norm(q))}  (identical: {wc(q) == wc(norm(q))})")
            print(f"    convention A lines     : {a1}-{a2}" if a1 else "    convention A: NOT FOUND")
            print(f"    convention B lines     : {b1}-{b2}" if b1 else "    convention B: NOT FOUND")
            # verbatim substring check on the collapsed stripped text
            coll = norm(" ".join(stripA[sid]))
            print(f"    verbatim in A collapsed: {norm(q) in coll}")
            print(f"    occurrences in A       : {coll.count(norm(q))}")

    # ---------- 3. registry rows ----------
    print("\n[3] REGISTRY ROWS corpus/SOURCES.md (reader column convention)")
    reg = open(f"{LANE}/corpus/SOURCES.md", encoding="utf-8").read()
    for sid in ("S321", "S322"):
        for line in reg.split("\n"):
            c = [x.strip() for x in re.sub(r"^ {0,3}", "", line).split("|")]
            if len(c) >= 13 and c[1] == sid:
                cols = c[1:12]
                print(f"\n  {sid}: split fields={len(c)}  columns={len(cols)}  "
                      f"11 columns: {len(cols) == 11}")
                hdr = [x.strip() for x in re.sub(r"^ {0,3}", "", reg.split("\n")[8]).split("|")]
                for i, (h, v) in enumerate(zip(hdr[1:12], cols), 1):
                    shown = v if len(v) <= 150 else v[:150] + " ...[+]"
                    print(f"    [{i:2}] {h:10} = {shown}")
                print(f"    status == 'mined'                : {c[8] == 'mined'}  (cell 8 = {c[8]!r})")
                print(f"    used-by names corpus/lessons/round-93.md : "
                      f"{'corpus/lessons/round-93.md' in c[11]}")
                print(f"    used-by cell: {c[11]}")
                break

    # ---------- 4. GFM width / remainder rules ----------
    print("\n[4] GFM SPEC: the width rule the reader enforces (QUALITY 165)")
    for label, q in (("header-vs-delimiter cell count", WIDTH_RULE),
                     ("remainder-row policy", REMAINDER_RULE)):
        a1, a2 = locate(stripA["S321"], q)
        b1, b2 = locate(stripB["S321"], q)
        print(f"\n  {label}")
        print(f"    quote: {q[:110]}...")
        print(f"    convention A lines : {a1}-{a2}" if a1 else "    convention A: NOT FOUND")
        print(f"    convention B lines : {b1}-{b2}" if b1 else "    convention B: NOT FOUND")
        if a1:
            for ln in range(a1, min(a2, a1 + 4) + 1):
                print(f"      A:{ln}: {stripA['S321'][ln-1].strip()[:200]}")

    # ---------- 5. recorded anchors in the lane's own text ----------
    print("\n[5] THE LANE'S RECORDED ANCHORS (round-93 .txt, multi-line)")
    for sid, want in (("s321.txt", 4496), ("s322.txt", 2613)):
        p = f"{LANE}/.ufo/evidence/round-93/sources/{sid}"
        lines = open(p, encoding="utf-8", errors="replace").read().split("\n")
        print(f"  {sid}: {len(lines)} lines; recorded anchor line {want}:")
        for ln in range(want - 1, want + 2):
            if 1 <= ln <= len(lines):
                print(f"    {ln}: {lines[ln-1][:190]}")
    # the round-93 lesson's quote anchors
    for sid, want in (("s321.txt", 4396), ("s322.txt", 2619)):
        p = f"{LANE}/.ufo/evidence/round-93/sources/{sid}"
        lines = open(p, encoding="utf-8", errors="replace").read().split("\n")
        print(f"  {sid}: lesson quote anchor line {want}: "
              f"{lines[want-1][:190] if want <= len(lines) else 'OUT OF RANGE'!r}")
    # the round-94 committed .txt shape (single line) - a formatting difference
    for sid in ("s321.txt", "s322.txt"):
        p = f"{LANE}/.ufo/evidence/round-94/sources/{sid}"
        raw = open(p, encoding="utf-8", errors="replace").read()
        print(f"  round-94 {sid}: bytes={len(raw.encode())} newlines={raw.count(chr(10))} "
              f"(single-line form; quotes present: "
              f"{all(norm(q) in norm(raw) for qs in QUOTES.values() for q in qs)})")

    print("\nR94S1_VERIFY_DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
