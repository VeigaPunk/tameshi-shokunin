#!/usr/bin/env python3
# Test single-line numbers: canonical start minus 1..5 as "off-by-N" check: none matches all?
# Test: author may have used D1's own 'correct' values from a DIFFERENT primer: R95S1 quotes 88/4496/4395/2618/2356
# R95S1 4395 vs Gate 4393: R95S1 says 4395-4396 for *13-word* quote; Gate cites 4393 for *19-word* quote (adds ", and zero or more data rows")
# D1 says: gate 4393 -> actual 4396 for that quote's start? Let's check: D1 text line 177: S321 `a single header row, ...` -> 4396 (Gate 4393). But canonical span is 4395-4397 and R95S1 says 4395-4396 for 13-word version.
# Why would D1 say 4396? Because "a single..." tokens: first word "a" is at 4396 line (4395 ends with "of a"). R95S1 line 157: 'a single header row' cited at 4395-4396 (start of SENTENCE). Tool's first-word rule: start="a" line 4396 for ... wait tool observed=4395-4397. Which is right per locate?
# Here locate returns (4395,4397) for the 19-word quote because first word is "a" ... verify: canonical 4395 'A table is an arrangement... consisting of a' -> tokens: ..., 'a' is last token of 4395, so locate start=4395. D1 maybe reported the line where "single" starts? 4396. Tool reports 4395. R96 lesson writes 4395-4396 vs tool 4395-4397.
# Document all this.
import html, re
ns={}
src=open("/fast/scratch/hyaku/tameshi-r100/R100RV1/R93S1-tagstrip.py").read()
exec(compile(src,"R93S1","exec"),ns)
strip_tags=ns["strip_tags"]; locate=ns["locate"]
E="/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence"
raw=open(f"{E}/round-95/sources/s321.html",encoding="utf-8").read()
t=strip_tags(raw)
for q in ["a single header row, a delimiter row separating the header from the data", # 13w
          "a single header row, a delimiter row separating the header from the data, and zero or more data rows", # 19w
          "single header row"]:
    print(f"q={q[:40]!r}... words={len(q.split())} locate={locate(t,q)}")
for i in [4395,4396,4397]:
    print(i, repr(t[i-1]))
