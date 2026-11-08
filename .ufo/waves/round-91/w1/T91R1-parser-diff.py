#!/usr/bin/env python3
"""T91R1 parser-differential probe for the sealed C1 counter.

Reads the counter at the contracted freeze rev and at HEAD from git objects
(read-only), loads both parse_note implementations, and runs the note shapes
that decide whether a committed note is refused or accepted for the wrong
column. Output is the evidence cited in T91R1.md.

Usage: python3 -I T91R1-parser-diff.py <lane-repo> <freeze-rev>
"""
import importlib.util, os, subprocess, sys, tempfile

LANE = sys.argv[1]
FREEZE = sys.argv[2] if len(sys.argv) > 2 else "50e59d59a5b0fffffe7a0e99da9a39397f2f94fc"
PATH_IN_REPO = ".ufo/evidence/round-91/c1/measure-v91.py"
NOTE = "corpus/knowledge/mutation-case-fleet-sources-census.md"
DERIVED = {"C01": "KILLED", "C02": "SURVIVED", "C03": "SURVIVED", "C04": "KILLED",
           "C05": "KILLED", "C06": "SURVIVED", "C07": "KILLED", "C08": "SURVIVED",
           "C09": "SURVIVED", "C10": "SURVIVED", "C11": "KILLED", "C12": "SURVIVED"}


def show(rev, path):
    p = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None


def load(tag, src):
    d = tempfile.mkdtemp(prefix="T91R1-")
    f = os.path.join(d, "m.py")
    with open(f, "wb") as fh:
        fh.write(src)
    s = importlib.util.spec_from_file_location("m_" + tag, f)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


frozen_src = show(FREEZE, PATH_IN_REPO)
head_src = show("HEAD", PATH_IN_REPO)
print("FREEZE_REV", FREEZE, "bytes", len(frozen_src or b""))
print("HEAD bytes", len(head_src or b""))
F = load("frozen", frozen_src)
H = load("head", head_src)


def call(m, nt):
    try:
        return m.parse_note(nt)
    except TypeError:
        return m.parse_note(nt, None)


# 1. the committed note (as landed by round 90) through both parsers
real = show("HEAD", NOTE).decode("utf-8")
fr, fa = call(F, real)
hr, ha = call(H, real)
print("COMMITTED_NOTE frozen rows=%d ambiguous=%d" % (len(fr), len(fa)))
print("COMMITTED_NOTE head   rows=%d ambiguous=%d match=%s"
      % (len(hr), len(ha), hr == DERIVED))

# 2. false-green shape: the human-read `verdict` column is false, the column
#    after it carries the derived verdicts.
def table(verdict_cell, next_cell):
    out = ["| id | arm | verdict | witness |", "|---|---|---|---|"]
    for k, v in DERIVED.items():
        out.append("| %s | arm | %s | %s |" % (k, verdict_cell, next_cell(k, v)))
    return "\n".join(out) + "\n"

fg = table("SURVIVED", lambda k, v: v)
fr, fa = call(F, fg)
hr, ha = call(H, fg)
print("FALSE_GREEN frozen rows=%d ambiguous=%d equals_derived=%s"
      % (len(fr), len(fa), fr == DERIVED))
print("FALSE_GREEN head   rows=%d ambiguous=%d mismatches=%d"
      % (len(hr), len(ha), sum(1 for k, v in DERIVED.items() if hr.get(k) != v)))

# 3. honest shape with the verdict in the header-named column
def honest(truth=True):
    out = ["| id | arm | verdict | witness |", "|---|---|---|---|"]
    for k, v in DERIVED.items():
        out.append("| %s | arm | %s | %s |" % (k, v if truth else "SURVIVED", "differs"))
    return "\n".join(out) + "\n"

hon = honest()
fr, fa = call(F, hon)
hr, ha = call(H, hon)
print("HONEST frozen rows=%d ambiguous=%d" % (len(fr), len(fa)))
print("HONEST head   rows=%d ambiguous=%d match=%s" % (len(hr), len(ha), hr == DERIVED))

# 4. gate-legal 0-3 space indentation on the whole table
ind = "\n".join("   " + l for l in hon.split("\n"))
fr, fa = call(F, ind)
hr, ha = call(H, ind)
print("INDENTED_3SP frozen rows=%d ambiguous=%d | head rows=%d ambiguous=%d"
      % (len(fr), len(fa), len(hr), len(ha)))

# 5. forest of verdict-looking tables the note body already carries
for label, text in [
        ("survivor-table-row", "| C02 \u00b7 W02 thin-reject length | x | y | z | w |\n"),
        ("impact-row", "| C12 used-by trim | 20 | effect |\n"),
        ("comma-row", "| C02, C06, C08 | 0 | effect |\n")]:
    hdr = "| id | arm | verdict | witness |\n|---|---|---|---|\n"
    hr, ha = call(H, hdr + text)
    print("TABLE_SHAPE %-20s rows=%d ambiguous=%s" % (label, len(hr), ha))

# 6. fence parity of the committed note (shipped parser skips fenced rows)
fence = sum(1 for l in real.split("\n") if l.strip().startswith("```"))
print("COMMITTED_NOTE fence_lines=%d balanced=%s" % (fence, fence % 2 == 0))

# 7. the CTL14-pos control note shape (controls-v91.py note_text) through the
#    frozen parser: the committed PASS receipt must be impossible under it.
def ctl_note():
    out = ["source: S318 fixture row (positive control only)", "", "# fixture note", "",
           "measured: 5/12 killed", "", "| id | arm | verdict | witness |", "|---|---|---|---|"]
    for k, v in DERIVED.items():
        out.append("| %s | fixture arm | %s | differs |" % (k, v))
    return "\n".join(out) + "\n"

cn = ctl_note()
fr, fa = call(F, cn)
hr, ha = call(H, cn)
print("CTL14_NOTE frozen rows=%d ambiguous=%d | head rows=%d ambiguous=%d"
      % (len(fr), len(fa), len(hr), len(ha)))

# 8. one extra gate-legal, 3-space-indented contradictory row next to the honest
#    table: shipped parser never sees it, so no duplicate is flagged.
extra = hon.rstrip("\n") + "\n   | C02 | arm | KILLED | invisible |\n"
hr, ha = call(H, extra)
print("INDENTED_FALSE_ROW head rows=%d ambiguous=%s C02=%s equals_derived=%s"
      % (len(hr), ha, hr.get("C02"), hr == DERIVED))
fr, fa = call(F, extra)
print("INDENTED_FALSE_ROW frozen rows=%d ambiguous=%s" % (len(fr), fa))

# 9. a prose line with two pipes and a bare `verdict` cell before the table
#    binds vcol for the whole file (first match wins, not a table header).
poison = "see the | verdict | column above\n" + hon
hr, ha = call(H, poison)
print("PROSE_BINDS_HEADER head rows=%d ambiguous=%d" % (len(hr), len(ha)))
