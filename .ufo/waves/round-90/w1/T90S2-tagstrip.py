#!/usr/bin/env python3
"""T90S2 tag-strip: derive the tag-stripped text the located quotes are counted in.

Input : the saved gnu.org node page (.html)
Output: the tag-stripped text (.txt), one entry per non-empty line

Algorithm (fixed, so the L1 can re-derive the same line numbers):
  1. drop <script>...</script> and <style>...</style> blocks (non-greedy, DOTALL)
  2. replace every remaining tag with a single space
  3. decode HTML entities (html.unescape)
  4. split on newlines; collapse runs of spaces/tabs to one space; strip
  5. drop empty lines; number the survivors from 1

Usage: T90S2-tagstrip.py <page.html> <out.txt>
"""
import html
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
raw = open(src, encoding="utf-8", errors="replace").read()
text = re.sub(r"(?s)<(script|style).*?</\1>", "", raw)
text = re.sub(r"(?s)<[^>]+>", " ", text)
text = html.unescape(text)
lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in text.split("\n")]
lines = [ln for ln in lines if ln]
with open(dst, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
print(f"{dst}: {len(lines)} lines")
