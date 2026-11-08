#!/usr/bin/env python3
"""Round 100 C2 control: do the six round-95 Gate pointers hit under the round-95 Gate's OWN
stated rendering ("each tag replaced by one space, entities unescaped, lines right-trimmed", no
script/style removal named) — i.e. is the canonical-renderer miss an artefact of renderer choice?
Reads the round-95 snapshots and the R93S1 renderer as blobs at REV.
Usage: python3 -I r95-stated-renderer.py <lane> <rev>"""
import html, re, subprocess, sys
L, R = sys.argv[1], sys.argv[2]
def blob(p):
    return subprocess.run(["/usr/bin/git", "-C", L, "cat-file", "blob", "%s:%s" % (R, p)],
                          capture_output=True, check=True).stdout.decode("utf-8")
ns = {}
exec(compile(blob(".ufo/waves/round-93/w1/R93S1-tagstrip.py"), "R93S1", "exec"), ns)
def stated(raw):
    s = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    return [l.rstrip() for l in s.split("\n")]
Q = [("s320", "Print or check SHA256 (256-bit) checksums.", 84),
     ("s321", "The delimiter row consists of cells whose only content are hyphens", 4399),
     ("s321", "a single header row, a delimiter row separating the header from the data, and zero or more data rows", 4393),
     ("s321", "The table is broken at the first empty line, or beginning of another block-level structure", 4493),
     ("s322", "A fenced code block begins with a code fence, preceded by up to three spaces of indentation.", 2615),
     ("s323", "An indented code block is composed of one or more indented chunks separated by blank lines.", 2355)]
hits = 0
for s, q, c in Q:
    raw = blob(".ufo/evidence/round-95/sources/%s.html" % s)
    a = ns["locate"](stated(raw), q)
    b = ns["locate"](ns["strip_tags"](raw), q)
    h = any(x == c for x, _ in a)
    hits += h
    print("R95_STATED %s cited=%d stated_renderer=%s canonical=%s %s" % (s, c, a, b, "hit" if h else "miss"))
print("R95_STATED pointers=%d hit_under_stated=%d" % (len(Q), hits))
