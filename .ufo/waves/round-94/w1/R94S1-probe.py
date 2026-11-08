#!/usr/bin/env python3
"""R94S1 independent source verification probe (read-only).

Fetches (or reads from scratch) the GFM spec and the CommonMark 0.31.2 spec,
tag-strips both bodies, locates the three quotes the round-94 lesson Gate
records, reports their line numbers in the stripped text and their word
counts, parses the S321/S322 registry rows out of corpus/SOURCES.md, and
checks the GFM spec's own statement that the header row's cell count must
match the delimiter row's cell count.

No writes outside this seat's scratch dir and its own deliverable path.
"""
import argparse
import hashlib
import html
import os
import re
import subprocess
import sys
import unicodedata

SCRATCH = "/fast/scratch/hyaku/tameshi-r94/R94S1"
LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"

SOURCES = {
    "S321-gfm": {
        "url": "https://github.github.com/gfm/",
        "snapshot": f"{LANE}/.ufo/evidence/round-94/sources/s321.html",
        "fetched": f"{SCRATCH}/gfm.body",
        "expected_sha": "b153d814fdfc8624bb6da7449162c1cd707a637f7d1c1b636eb44b9cf63fa220",
        "expected_size": 508310,
    },
    "S322-commonmark": {
        "url": "https://spec.commonmark.org/0.31.2/",
        "snapshot": f"{LANE}/.ufo/evidence/round-94/sources/s322.html",
        "fetched": f"{SCRATCH}/cm.body",
        "expected_sha": "c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d",
        "expected_size": 514698,
    },
}

QUOTES = [
    ("S321-gfm", "The table is broken at the first empty line, or beginning of another block-level structure"),
    ("S321-gfm", "a single header row, a delimiter row separating the header from the data"),
    ("S322-commonmark", "A fenced code block begins with a code fence, preceded by up to three spaces of indentation."),
]

TAG_RE = re.compile(r"<[^>]+>")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tag_strip(text):
    """Strip HTML tags, decode entities, normalize whitespace per line."""
    out = []
    in_script = 0
    for line in text.split("\n"):
        # remove script/style blocks' content
        line = TAG_RE.sub("", line)
        line = html.unescape(line)
        line = line.replace("\u00a0", " ")
        out.append(line)
    return "\n".join(out)


def norm(s):
    """NFKC + whitespace-collapse for quote comparison."""
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"\s+", " ", s).strip()


def words(s):
    return len([w for w in norm(s).split(" ") if w])


def find_quote(stripped_lines, quote):
    """Return (line_number_1based, matched_line, collapsed_line) for the first
    line whose normalized form contains the normalized quote."""
    q = norm(quote)
    for i, line in enumerate(stripped_lines, 1):
        n = norm(line)
        if q in n:
            return i, line.strip(), n
    # try joining consecutive lines (spec wraps paragraphs)
    for i in range(len(stripped_lines)):
        for span in (2, 3):
            chunk = norm(" ".join(l for l in stripped_lines[i:i + span]))
            if q in chunk:
                return i + 1, " ".join(l.strip() for l in stripped_lines[i:i + span]), chunk
    return None, None, None


def parse_registry_row(text, key):
    """Find the SOURCES.md table row whose first cell is `key`; return the split cells."""
    for line in text.split("\n"):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cells and cells[0] == key:
            return cells, s
    return None, None


def gfm_width_rule(stripped_lines):
    """Find GFM's own statement that the header row must match the delimiter
    row in cell count."""
    pats = [
        r"number of cells in the header row",
        r"must match the number of cells",
        r"delimiter row must match",
        r"header row.*cell count",
        r"cell count.*header row",
    ]
    hits = []
    for i, line in enumerate(stripped_lines, 1):
        low = norm(line).lower()
        for p in pats:
            if re.search(p, low):
                hits.append((i, line.strip()))
                break
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=SCRATCH)
    args = ap.parse_args()

    print("=" * 78)
    print("R94S1 PROBE — independent source verification (S321 / S322)")
    print("=" * 78)

    # ---------- fetch (if not already fetched) ----------
    for key, s in SOURCES.items():
        if not os.path.exists(s["fetched"]):
            subprocess.run(
                ["curl", "-sS", "-L", "-D", os.path.join(args.work, key + ".headers"),
                 "-o", s["fetched"], s["url"]],
                check=True,
            )

    # ---------- hashes / sizes / http date ----------
    print("\n-- FETCH + SNAPSHOT IDENTITY --")
    for key, s in SOURCES.items():
        hdr = os.path.join(args.work, key + ".headers")
        date = ""
        status = ""
        if os.path.exists(hdr):
            for ln in open(hdr, errors="replace"):
                if ln.lower().startswith("date:"):
                    date = ln.split(":", 1)[1].strip()
                elif ln.startswith("HTTP/"):
                    status = ln.strip()
        f_sha = sha256(s["fetched"])
        f_size = os.path.getsize(s["fetched"])
        s_sha = sha256(s["snapshot"])
        s_size = os.path.getsize(s["snapshot"])
        print(f"{key}")
        print(f"  url            : {s['url']}")
        print(f"  http status    : {status}")
        print(f"  http date      : {date}")
        print(f"  fetched  sha256: {f_sha}  ({f_size} B)")
        print(f"  snapshot sha256: {s_sha}  ({s_size} B)")
        print(f"  expected sha256: {s['expected_sha']}  ({s['expected_size']} B)")
        print(f"  fetched == expected sha : {f_sha == s['expected_sha']}")
        print(f"  snapshot == expected sha: {s_sha == s['expected_sha']}")
        print(f"  fetched == snapshot     : {f_sha == s_sha}")
        print(f"  fetched == snapshot size: {f_size == s_size}")

    # ---------- tag-strip + quotes ----------
    stripped = {}
    print("\n-- QUOTE LOCATIONS (in tag-stripped text) --")
    for key, s in SOURCES.items():
        raw = open(s["fetched"], encoding="utf-8", errors="replace").read()
        st = tag_strip(raw)
        stripped[key] = st.split("\n")
        print(f"{key}: raw lines={len(raw.split(chr(10)))} stripped lines={len(stripped[key])}")

    for key, quote in QUOTES:
        ln, matched, collapsed = find_quote(stripped[key], quote)
        wc = words(quote)
        print(f"\n[{key}] {quote!r}")
        print(f"  quoted word count : {wc}")
        if ln is None:
            print("  LOCATED            : NO")
            continue
        print(f"  stripped line no. : {ln}")
        print(f"  matched line      : {matched[:300]}")
        # word count measured on the located text span (the quote as it appears)
        n = norm(collapsed)
        qn = norm(quote)
        idx = n.find(qn)
        span = n[idx:idx + len(qn)] if idx >= 0 else qn
        print(f"  located span words: {words(span)}")
        # count pipes on the raw source line (is it a table row in the original?)
        raw_lines = open(SOURCES[key]["fetched"], encoding="utf-8", errors="replace").read().split("\n")
        print(f"  note: line number is in the STRIPPED text, not the raw HTML")

    # ---------- registry rows ----------
    print("\n-- REGISTRY ROWS (corpus/SOURCES.md) --")
    reg = open(f"{LANE}/corpus/SOURCES.md", encoding="utf-8").read()
    for key in ("S321", "S322"):
        cells, raw_row = parse_registry_row(reg, key)
        if cells is None:
            print(f"{key}: NOT FOUND")
            continue
        print(f"\n{key}: columns={len(cells)}")
        for i, c in enumerate(cells, 1):
            print(f"  [{i:2}] {c}")
        print(f"  raw: {raw_row}")
        status = cells[3] if len(cells) > 3 else ""
        usedby = " ".join(cells[5:]) if len(cells) > 5 else ""
        print(f"  status cell[3] == 'mined' : {status == 'mined'}  (got {status!r})")
        print(f"  used-by names corpus/lessons/round-93.md : "
              f"{'corpus/lessons/round-93.md' in usedby}  (got {usedby!r})")
        print(f"  11 columns : {len(cells) == 11}")

    # ---------- GFM width rule ----------
    print("\n-- GFM SPEC: header-row/delimiter-row cell-count rule --")
    hits = gfm_width_rule(stripped["S321-gfm"])
    if not hits:
        print("  NO HIT")
    for ln, txt in hits[:12]:
        print(f"  line {ln}: {txt[:320]}")

    print("\nR94S1_PROBE_DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
