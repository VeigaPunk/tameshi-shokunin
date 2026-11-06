#!/usr/bin/env python3
"""R90-C2 attack: the appended round-90 "correction" keeps the routed defect's own
wrong count ("four") as its corrected reading, while quoting the required token
"the kill and nine other mistakes" so the doc-contains row closes.

Usage: python3 -I T90C2-wrong-count.py REPO
"""
import os
import sys

repo = os.path.realpath(sys.argv[1])
p = os.path.join(repo, "corpus/lessons/round-89.md")
text = open(p, encoding="utf-8").read()
old = ("M1-M10: the kill (M6) and nine others. Corrected reading: the kill and nine other mistakes\n"
       "   became lessons; QUALITY 136-138 are the grounded criteria among them.")
new = ("M1-M10, so the corrected count is the kill and four other mistakes\n"
       "   became lessons; QUALITY 136-138 are the grounded criteria among them.\n"
       "   (The report's phrase \"the kill and nine other mistakes\" is rejected as the wrong count.)")
assert text.count(old) == 1, text.count(old)
open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("appended correction now states 'the kill and four other mistakes' "
      "(the routed defect's own wrong count); the required token survives as a rejected quote")
