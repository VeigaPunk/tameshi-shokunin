#!/usr/bin/env python3
"""R100E2 independent Gate line-pointer re-derivation (round 100, C2).

Independent of tools/gate-line-recheck.py: nothing here imports or copies that
tool. The renderer below is re-implemented from the R93S1 description in the
seat spec (script/style blocks and comments removed, each tag -> one space,
entities unescaped, NBSP -> space, lines right-trimmed). Pointers, quotes and
snapshot bindings were extracted by hand-reading the five `## Gate` sections
of corpus/lessons/round-95..99.md at FREEZE; snapshot bytes are read from
local files fetched with `git show FREEZE:<path>`, never via the tool.

Usage: python3 -I R100E2-indep.py --snap-root DIR --rec-root DIR --tool-out FILE
  --snap-root holds files at the same relative paths as the lane blobs.
  --rec-root holds round-95.md .. round-99.md.
  --tool-out is the captured stdout of the tool run (for the comparison table).
"""
import argparse
import hashlib
import html as htmlmod
import re
import sys

# ---- independent renderer (from the R93S1 description, re-implemented) ----

def strip_tags(raw):
    s = re.sub(r"<script\b[^>]*>.*?</script\s*>", " ", raw, flags=re.S | re.I)
    s = re.sub(r"<style\b[^>]*>.*?</style\s*>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s).replace("\u00a0", " ")
    return [ln.rstrip() for ln in s.split("\n")]

def _bare(tok):
    return tok.strip(".,;:!?\"'()[]")

def locate_spans(lines, quote):
    """Word-sequence locate: return [(first_line, last_line), ...] 1-based."""
    words, owners = [], []
    for i, ln in enumerate(lines, 1):
        for tok in ln.split():
            words.append(_bare(tok)); owners.append(i)
    q = [_bare(w) for w in quote.split()]
    n = len(q)
    out = []
    for j in range(len(words) - n + 1):
        if words[j:j + n] == q:
            h = (owners[j], owners[j + n - 1])
            if not out or out[-1] != h:
                out.append(h)
    return out

# ---- hand-read pointer table (every `line N`/`lines N-M` in the five Gates) ----
# mdline = line number within the record file where the pointer occurs,
# verified against the freeze records by hand-reading the Gate sections.
# cite = (N, None) or (N, M).  snap = lane-relative snapshot path, or None.
# extra = second quote also present in the same segment (r97:24), if any.
POINTERS = [
    # round-95 (6)
    dict(rec="round-95.md", md=17, sid="S320", cite=(84, None),
         quote="Print or check SHA256 (256-bit) checksums.",
         snap=".ufo/evidence/round-95/sources/s320.html"),
    dict(rec="round-95.md", md=18, sid="S321", cite=(4399, None),
         quote="The delimiter row consists of cells whose only content are hyphens",
         snap=".ufo/evidence/round-95/sources/s321.html"),
    dict(rec="round-95.md", md=19, sid="S321", cite=(4393, None),
         quote="a single header row, a delimiter row separating the header from the data, and zero or more data rows",
         snap=".ufo/evidence/round-95/sources/s321.html"),
    dict(rec="round-95.md", md=20, sid="S321", cite=(4493, None),
         quote="The table is broken at the first empty line, or beginning of another block-level structure",
         snap=".ufo/evidence/round-95/sources/s321.html"),
    dict(rec="round-95.md", md=21, sid="S322", cite=(2615, None),
         quote="A fenced code block begins with a code fence, preceded by up to three spaces of indentation.",
         snap=".ufo/evidence/round-95/sources/s322.html"),
    dict(rec="round-95.md", md=22, sid="S323", cite=(2355, None),
         quote="An indented code block is composed of one or more indented chunks separated by blank lines.",
         snap=".ufo/evidence/round-95/sources/s323.html"),
    # round-96 (7; incl. one unresolved)
    dict(rec="round-96.md", md=18, sid="S320", cite=(88, None),
         quote="Print or check SHA256 (256-bit) checksums.",
         snap=".ufo/evidence/round-96/sources/s320.html"),
    dict(rec="round-96.md", md=19, sid="S320", cite=(116, None),
         quote="don't output anything, status code shows success",
         snap=".ufo/evidence/round-96/sources/s320.html"),
    dict(rec="round-96.md", md=20, sid="S321", cite=(4403, None),
         quote="The delimiter row consists of cells whose only content are hyphens",
         snap=".ufo/evidence/round-96/sources/s321.html"),
    dict(rec="round-96.md", md=21, sid="S321", cite=(4496, 4497),
         quote="The table is broken at the first empty line, or beginning of another block-level structure",
         snap=".ufo/evidence/round-96/sources/s321.html"),
    dict(rec="round-96.md", md=22, sid="S322", cite=(2618, 2619),
         quote="A fenced code block begins with a code fence, preceded by up to three spaces of indentation.",
         snap=".ufo/evidence/round-96/sources/s322.html"),
    dict(rec="round-96.md", md=23, sid="S323", cite=(2358, 2359),
         quote="An indented code block is composed of one or more indented chunks separated by blank lines.",
         snap=".ufo/evidence/round-96/sources/s323.html"),
    dict(rec="round-96.md", md=27, sid="S091", cite=(733, None),
         quote="Returns the commit's SHA-1 hash. You can use this endpoint to check if a remote reference's SHA-1 hash is the same as your local reference's SHA-1 hash",
         snap=None),  # no snapshot named in this block; unresolved by hand
    # round-97 (2)
    dict(rec="round-97.md", md=17, sid="S159", cite=(762, None),
         quote="Equivalent mutants detection is one of the biggest obstacles to practical usage of mutation testing.",
         snap=".ufo/evidence/round-97/sources/s159.html"),
    dict(rec="round-97.md", md=24, sid="S006", cite=(490, 492),
         quote="A row whose old literal occurs more than once in its target there is refused: the rewrite takes the first copy, which might not be the one the row means.",
         snap=".ufo/evidence/round-97/sources/s006.html",
         extra="A row whose old literal occurs more than once in its target there is refused"),
    # round-98 (4; incl. two no-quote anchor lines, and one sha-bound snapshot)
    dict(rec="round-98.md", md=19, sid="S012", cite=(112, None),
         quote="A test oracle that obtains its expected value from the system it is judging cannot fail.",
         snap=".ufo/evidence/round-98/sources/s012.html"),
    dict(rec="round-98.md", md=29, sid="S009", cite=(413, None),
         quote="Identifying equivalent mutants remains the largest impediment to the widespread uptake of mutation testing.",
         snap=".ufo/waves/round-98/w1/SC1-s009.html"),  # bound by the block's full sha256 be3f85db...
    dict(rec="round-98.md", md=52, sid="S006", cite=(490, 492), quote=None, snap=None),
    dict(rec="round-98.md", md=59, sid="S159", cite=(762, None), quote=None, snap=None),
    # round-99 (2)
    dict(rec="round-99.md", md=29, sid="S325", cite=(135, 137),
         quote='statcheck is a "spellchecker" for statistics. It checks whether your p -values match their accompanying test statistic and degrees of freedom.',
         snap=".ufo/evidence/round-99/sources/s325.html"),
    dict(rec="round-99.md", md=31, sid="S325", cite=(163, None),
         quote="Statcheck usually can't find statistics in tables.",
         snap=".ufo/evidence/round-99/sources/s325.html"),
]

def parse_tool_out(path):
    """Parse captured tool stdout into {(record_basename, mdline): (verdict, cited, observed)}."""
    rows = {}
    try:
        with open(path) as fh:
            for ln in fh:
                ln = ln.rstrip("\n")
                if not ln.startswith("GATE_LINE "):
                    continue
                # GATE_LINE <verdict> <record>:<line> sid=.. cited=.. observed=.. ...
                f = ln.split()
                verdict = f[1]
                rl = f[2]
                rec, md = rl.rsplit(":", 1)
                d = dict(x.split("=", 1) for x in f[3:] if "=" in x)
                rows[(rec.split("/")[-1], int(md))] = (verdict, d.get("cited"), d.get("observed"), d.get("snapshot"))
    except OSError as e:
        print("INDEP-ERROR tool-out unreadable: %s" % e)
    return rows

def verdict_of(spans, cite):
    n1, n2 = cite
    if not spans:
        return "absent"
    if n2 is None:
        return "hit" if any(a == n1 for a, _ in spans) else "miss"
    return "hit" if (n1, n2) in spans else "miss"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snap-root", required=True)
    ap.add_argument("--rec-root", required=True)
    ap.add_argument("--tool-out", required=True)
    ap.add_argument("--snap-rev", default="56f247da25a0252fcdb8e04a61675e0d73aae9ab",
                    help="freeze rev the snapshot bytes were fetched at")
    a = ap.parse_args()

    tool = parse_tool_out(a.tool_out)
    render_cache = {}
    n_agree = n_false_green = n_diff = 0

    print("INDEP records_root=%s snap_root=%s snap_rev=%s hand_pointers=%d"
          % (a.rec_root, a.snap_root, a.snap_rev, len(POINTERS)))
    print("INDEP pointer | cited | observed(indep) | my verdict | tool verdict | agree? | note")
    for p in POINTERS:
        key = (p["rec"], p["md"])
        tverdict, tcited, tobserved, tsnap = tool.get(key, ("MISSING", "-", "-", "-"))
        note = ""
        if p["quote"] is None:
            mine = "unbound:no-quote"
            observed = "-"
        elif p["snap"] is None:
            mine = "unbound:snapshot-unresolved"
            observed = "-"
        else:
            if p["snap"] not in render_cache:
                path = a.snap_root + "/" + p["snap"]
                try:
                    with open(path, encoding="utf-8") as fh:
                        raw = fh.read()
                except (OSError, UnicodeDecodeError) as e:
                    raw = None
                    note = "read-fail:%s" % e
                render_cache[p["snap"]] = strip_tags(raw) if raw is not None else None
            lines = render_cache[p["snap"]]
            if lines is None:
                mine, observed = "unbound:snapshot-unreadable", "-"
            else:
                spans = locate_spans(lines, " ".join(p["quote"].split()))
                observed = ",".join("%d-%d" % s for s in spans) if spans else "-"
                mine = verdict_of(spans, p["cite"])
                if "extra" in p:
                    xs = locate_spans(lines, " ".join(p["extra"].split()))
                    note = "extra-quote spans=" + (",".join("%d-%d" % s for s in xs) or "-")
                if tsnap not in ("-", p["snap"]):
                    note = (note + " " if note else "") + "snap-diff tool=%s mine=%s" % (tsnap, p["snap"])
        agree = "YES" if mine == tverdict else "NO"
        if agree == "YES":
            n_agree += 1
        else:
            n_diff += 1
            if tverdict == "hit" and mine != "hit":
                n_false_green += 1
        ptr = "%s:%d sid=%s cited=%s" % (p["rec"], p["md"], p["sid"],
                                         "%d" % p["cite"][0] if p["cite"][1] is None else "%d-%d" % p["cite"])
        print("%s | cited=%s | observed=%s | mine=%s | tool=%s | agree=%s%s"
              % (ptr, tcited, observed, mine, tverdict, agree,
                 (" | " + note) if note else ""))
    # sha-binding spot check for round-98:29 (block carries full sha256 be3f85db...)
    sp = a.snap_root + "/.ufo/waves/round-98/w1/SC1-s009.html"
    try:
        with open(sp, "rb") as fh:
            h = hashlib.sha256(fh.read()).hexdigest()
        print("SHA-CHECK round-98:29 s009 blob sha256=%s expected=be3f85dbdb766ab8d1935145099d77b3888915e0220183511253b5c1fa29ed7c match=%s"
              % (h, h == "be3f85dbdb766ab8d1935145099d77b3888915e0220183511253b5c1fa29ed7c"))
    except OSError as e:
        print("SHA-CHECK round-98:29 unreadable: %s" % e)
    # coverage: every tool-listed pointer accounted for?
    tool_keys = set(tool.keys())
    hand_keys = set((p["rec"], p["md"]) for p in POINTERS)
    missing_from_tool = sorted(hand_keys - tool_keys)
    extra_in_tool = sorted(tool_keys - hand_keys)
    print("INDEP-COVERAGE hand=%d tool=%d missing_from_tool=%s extra_in_tool=%s"
          % (len(hand_keys), len(tool_keys), missing_from_tool, extra_in_tool))
    print("INDEP-SUMMARY hand=%d agree=%d differ=%d false_greens=%d"
          % (len(POINTERS), n_agree, n_diff, n_false_green))
    print("INDEP-VERDICT false_greens=%d coverage_gap=%s"
          % (n_false_green, "NONE" if not (missing_from_tool or extra_in_tool) else "PRESENT"))
    return 0 if n_false_green == 0 and not missing_from_tool and not extra_in_tool else 1

if __name__ == "__main__":
    sys.exit(main())
