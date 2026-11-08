#!/usr/bin/env python3
"""R93S1 independent source verification probe (S321 GFM, S322 CommonMark).

Read-only. Fetches both spec pages into a scratch dir, tag-strips them
independently of the lane's counter, locates the three Gate quotes with line
numbers and word counts, parses the S321/S322 registry rows out of
corpus/SOURCES.md, and locates the GFM cell-count rule.

Usage:
  python3 -I R93S1-tagstrip.py --work <scratch> --lane <lane-repo>
"""
import argparse
import hashlib
import html as htmlmod
import json
import os
import re
import subprocess
import sys

GFM_URL = "https://github.github.com/gfm/"
CM_URL = "https://spec.commonmark.org/0.31.2/"

SNAP = {
    "S321": ".ufo/evidence/round-93/sources/s321.html",
    "S322": ".ufo/evidence/round-93/sources/s322.html",
}
SNAP_SHA = {
    "S321": "b153d814fdfc8624bb6da7449162c1cd707a637f7d1c1b636eb44b9cf63fa220",
    "S322": "c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d",
}

QUOTES = [
    ("S321", "The table is broken at the first empty line, or beginning of another block-level structure"),
    ("S321", "a single header row, a delimiter row separating the header from the data"),
    ("S322", "A fenced code block begins with a code fence, preceded by up to three spaces of indentation."),
]

CELL_RULE = "The header row must match the delimiter row in the number of cells."


def fetch(url, work, name):
    """curl -sS -L -D headers -o body; return (headers, body_path)."""
    hdr = os.path.join(work, name + ".headers")
    body = os.path.join(work, name + ".live.html")
    p = subprocess.run(["curl", "-sS", "-L", "-D", hdr, "-o", body, url],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise SystemExit("curl-failed:%s:%s" % (url, p.stderr.decode(errors="replace").strip()))
    return hdr, body


def http_date(hdr_path):
    for line in open(hdr_path, "r", encoding="utf-8", errors="replace"):
        if line.lower().startswith("date:"):
            return line.split(":", 1)[1].strip()
    return ""


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_tags(raw):
    """Line-preserving tag strip: remove script/style blocks and all tags,
    unescape entities. Returns the stripped text as a list of lines."""
    s = re.sub(r"<script\b[^>]*>.*?</script\s*>", " ", raw, flags=re.S | re.I)
    s = re.sub(r"<style\b[^>]*>.*?</style\s*>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s)
    s = s.replace("\u00a0", " ")
    lines = [ln.rstrip() for ln in s.split("\n")]
    return lines


def norm_text(s):
    """The counter's normalisation (tags stripped, entities unescaped, quotes and
    dashes folded, whitespace collapsed). Used only to check whether a quote
    occurs in the snapshot under the same rule the counter applies."""
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s)
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2014", "-").replace("\u2013", "-").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).strip()


def norm_quote(q):
    return norm_text(q)


def _bare(tok):
    """Strip leading/trailing punctuation so a quote that ends mid-sentence
    still matches the page word that carries a trailing comma or colon."""
    return tok.strip(".,;:!?\"'()[]")


def locate(lines, quote):
    """Return list of (first_line, last_line) 1-based spans where the quote's
    word sequence occurs in the stripped text.  Matching is on word sequences
    with edge punctuation removed, so a quote wrapped over several source
    lines is reported with the span of the lines it covers."""
    joined = []
    idx = []
    for i, ln in enumerate(lines, 1):
        for tok in ln.split():
            joined.append(_bare(tok))
            idx.append(i)
    qwords = [_bare(w) for w in quote.split()]
    hits = []
    n = len(qwords)
    for j in range(len(joined) - n + 1):
        if joined[j:j + n] == qwords:
            hits.append((idx[j], idx[j + n - 1]))
    # dedupe consecutive duplicates
    out = []
    for h in hits:
        if not out or out[-1] != h:
            out.append(h)
    return out


def parse_registry_row(line):
    """Mirror of the counter's row parse: strip up to 3 leading spaces, split on
    '|', and index the cells. Returns the cell list."""
    return [x.strip() for x in re.sub(r"^ {0,3}", "", line).split("|")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--lane", required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    work = os.path.realpath(a.work)
    lane = os.path.realpath(a.lane)
    os.makedirs(work, exist_ok=True)
    out = {}

    # --- fetch ------------------------------------------------------------
    live = {}
    for name, url in (("s321", GFM_URL), ("s322", CM_URL)):
        hdr, body = fetch(url, work, name)
        live[name] = {
            "url": url,
            "http_date": http_date(hdr),
            "bytes": os.path.getsize(body),
            "sha256": sha256_file(body),
        }
    out["live"] = live

    # --- committed snapshots ---------------------------------------------
    snap = {}
    for sid, rel in SNAP.items():
        p = os.path.join(lane, rel)
        snap[sid] = {
            "path": rel,
            "bytes": os.path.getsize(p),
            "sha256": sha256_file(p),
            "matches_expected_sha": sha256_file(p) == SNAP_SHA[sid],
        }
    out["snapshots"] = snap

    # --- tag-strip live bodies and locate quotes -------------------------
    stripped = {}
    for sid, name in (("S321", "s321"), ("S322", "s322")):
        raw = open(os.path.join(work, name + ".live.html"), "r",
                   encoding="utf-8", errors="replace").read()
        lines = strip_tags(raw)
        tp = os.path.join(work, name + ".stripped.txt")
        with open(tp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        stripped[sid] = {"stripped_lines": len(lines), "stripped_path": tp}
    out["stripped"] = stripped

    quotes = []
    for sid, q in QUOTES:
        name = "s321" if sid == "S321" else "s322"
        raw = open(os.path.join(work, name + ".live.html"), "r",
                   encoding="utf-8", errors="replace").read()
        lines = strip_tags(raw)
        hits = locate(lines, q)
        # counter-equivalent check: quote occurs in the normalised snapshot text
        snapraw = open(os.path.join(lane, SNAP[sid]), "r",
                       encoding="utf-8", errors="replace").read()
        in_live_norm = norm_quote(q) in norm_text(raw)
        in_snap_norm = norm_quote(q) in norm_text(snapraw)
        quotes.append({
            "sid": sid,
            "quote": q,
            "word_count": len(q.split()),
            "live_line_spans": hits,
            "in_live_normalised": in_live_norm,
            "in_committed_snapshot_normalised": in_snap_norm,
        })
    out["quotes"] = quotes

    # --- GFM cell-count rule ---------------------------------------------
    raw = open(os.path.join(work, "s321.live.html"), "r",
               encoding="utf-8", errors="replace").read()
    lines = strip_tags(raw)
    out["cell_rule"] = {
        "quote": CELL_RULE,
        "line_spans": locate(lines, CELL_RULE),
        "in_committed_snapshot_normalised": norm_quote(CELL_RULE) in norm_text(
            open(os.path.join(lane, SNAP["S321"]), "r", encoding="utf-8",
                 errors="replace").read()),
    }

    # --- registry rows ----------------------------------------------------
    reg = open(os.path.join(lane, "corpus/SOURCES.md"), "r",
               encoding="utf-8", errors="replace").read()
    rows = {}
    for sid in ("S321", "S322"):
        for ln_no, line in enumerate(reg.split("\n"), 1):
            c = parse_registry_row(line)
            if len(c) >= 13 and c[1] == sid:
                rows[sid] = {
                    "file_line": ln_no,
                    "cell_count": len(c),
                    "data_columns": len(c) - 2,
                    "id": c[1],
                    "status": c[8],
                    "used_by": c[11],
                    "used_by_names_lesson": "corpus/lessons/round-93.md" in c[11],
                    "status_mined": c[8] == "mined",
                }
                break
    out["registry"] = rows

    # --- lesson Gate quotes ----------------------------------------------
    lesson_path = os.path.join(lane, "corpus/lessons/round-93.md")
    lesson = open(lesson_path, "r", encoding="utf-8", errors="replace").read()
    gate = {}
    for sid, q in QUOTES:
        occ = [i for i, ln in enumerate(lesson.split("\n"), 1)
               if q in ln]
        gate[sid + "|" + q[:40]] = {"lesson_lines": occ, "verbatim_in_lesson": bool(occ)}
    out["lesson_gate"] = gate

    text = json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
