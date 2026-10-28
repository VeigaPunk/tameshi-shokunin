#!/usr/bin/env python3
"""T55W3Connector4 receipt — class B reproduced on tameshi's own C0 bytes.

Class B (tameshi round-55, second mined class): "a predicate that counted a
document as stating a rule when a line break had split it."

This does not touch the lane: it reads SKILL.md at C0 through `git show` and
compares the same facts under (a) a raw-substring predicate and (b) the
whitespace-collapsed predicate amendments 2/3 installed.
"""
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
C0 = "9cf0146b94ddba12d454ebf7288ce6e5c5d535bb"

text = subprocess.run(
    ["git", "-C", LANE, "show", f"{C0}:SKILL.md"],
    capture_output=True, text=True, check=True,
).stdout
collapsed = re.sub(r"\s+", " ", text)

# The two arms tameshi's round-55 lesson names (corpus/lessons/round-55.md:37-41
# in that lesson's Mistakes section): the grammar marker, and the selftest label.
cases = [
    ("grammar marker",
     "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory"),
    ("selftest label",
     "bash-witness-study selftest"),
]

print(f"rev={C0} file=SKILL.md bytes={len(text)} lines={text.count(chr(10))}")
print(f"collapsed_bytes={len(collapsed)}")
print()
print(f"{'arm':16} {'raw':>6} {'collapsed':>10}   verdict")
for name, needle in cases:
    raw_hit = needle in text
    col_hit = needle in collapsed
    verdict = ("class B PRESENT: raw reads absent, collapsed reads present"
               if (not raw_hit and col_hit) else
               "no wrap between the needle's words" if col_hit else
               "needle not in the document at all")
    print(f"{name:16} {str(raw_hit):>6} {str(col_hit):>10}   {verdict}")

# How much of the standing-rules scratch bullet is exposed to the same failure:
# count words-internal newlines inside that bullet.
start = text.index("- **The scratch root has three arms.**")
end = text.index("\n\n", text.index("cells).", start))
bullet = text[start:end]
intra = re.findall(r"[A-Za-z0-9`'<>:_-]\n\s+[A-Za-z0-9`'<>:_-]", bullet)
print()
print(f"scratch bullet: chars={len(bullet)} lines={bullet.count(chr(10)) + 1} "
      f"word-splitting newlines={len(intra)}")
print("=> every one of those is a place a raw-substring marker can read as absent.")
sys.exit(0 if all((n in text) == (n in collapsed) for _, n in cases) else 0)
