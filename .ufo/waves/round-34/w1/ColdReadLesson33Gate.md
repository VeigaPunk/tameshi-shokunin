# ColdReadLesson33Gate — r34 w1 cold-read re-crediting (round-33.md)

Seat: `tameshi-r34-w1-ColdReadLesson33Gate` · 2026-10-23 · lane tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` (verified: `git rev-parse HEAD` after detach, worktree `status --porcelain` = 0 lines). Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/ColdReadLesson33Gate/`. Verdict: **no drift — all three routed claims agree with the lane bytes at tip.** No tooling installed or updated (git/sha256sum/cmp/grep sufficient; pacman untouched per 2026-10-20 pause).

## Setup (exit codes captured to rc files, never `&&`)

```
mkdir -p $S                                    ; echo $? > 01_mkdir.rc        # 0
git clone -q --no-hardlinks <lane> $S/lane     ; echo $? > 02_clone.rc        # 0
git -C $S/lane checkout -q --detach 0b99d48e…  ; echo $? > 03_checkout.rc     # 0
```

## Check 1 — pinned-byte fidelity (tool + runner)

```
git -C $L show 0b99d48e…:tools/tally-audit-v2.py > tool.py     ; rc → 10_tool_extract.rc = 0
git -C $L show 0b99d48e…:tools/mutate-and-run.sh > pristine.sh ; rc → 11_runner_extract.rc = 0
sha256sum tool.py pristine.sh
```

- `tool.py` → `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` — **equals the frozen pin**.
- `pristine.sh` → `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` — **equals the frozen pin**.

Tip `tools/tally-audit-v2.py` is byte-identical to the tool the deciding run pinned at `c17e593b…`.

## Check 2 — r34 append to corpus/lessons/round-33.md is append-only

Pre-image object: `051c1e65` = commit `051c1e65c033aa28046487d533d2563e4da3cb7d` ("round-33: record RevengerWitness witness-semantics hardening in Holds"), `git cat-file -t` → `commit`, `git show 051c1e65:corpus/lessons/round-33.md` rc=0 → 11141 bytes, sha256 `3d23c06696cf92c6cbd3d8b4059a1efec49fca38170d0392857c27c2a40621c0`. Tip file: 12841 bytes, sha256 `e4001d161c02759b4d9a2528cc75c57418838bf7b7af474416b210cf3e277d0b`.

```
cmp -n 11141 lesson_at_051c1e65.md lane/corpus/lessons/round-33.md ; echo $? > 20_prefix_cmp.rc   # 0
head -c 11141 lane/corpus/lessons/round-33.md | sha256sum
# → 3d23c06696cf92c6cbd3d8b4059a1efec49fca38170d0392857c27c2a40621c0  (identical to old blob)
tail -c 1 lesson_at_051c1e65.md | od -c   # \n — append begins on a fresh line
```

**Earlier bytes unchanged** (prefix sha equal, cmp rc=0); delta is exactly **1700 appended bytes** (tip lines 138–158, header `## R34 append — closure-routed corrections (append-only; author TameshiR34)`). `grep -c 7b11ba25 lesson_at_051c1e65.md` → 0: the pre-append bytes never name the new pin, so the correction genuinely introduces it.

## Check 3 — S100 Gate digest matches the committed snapshot

Lesson line 19 (pre-append region): `sha256 217edd573ef328316ac2410e5d046c5ad3a2df522270e5868bc5e5e5eb744899`, 216574 bytes, committed snapshot `.ufo/evidence/round-33/c2/doctest-snapshot.html`.

```
sha256sum $L/.ufo/evidence/round-33/c2/doctest-snapshot.html
# → 217edd573ef328316ac2410e5d046c5ad3a2df522270e5868bc5e5e5eb744899   (size 216574 — matches the row)
git -C $L merge-base --is-ancestor f6d8a891f1d966c5c3cdda385090da3a6e804675 0b99d48e…  # rc=0
```

**Match.** The snapshot's last-touch commit (`f6d8a89`, "freeze C1 … and C2 …") is an ancestor of tip, so the verified bytes are the committed snapshot, not a later drift. Per the row's own rule the pin is the committed bytes, never a live re-fetch.

## Check 4 — stale-pin correction names 7b11ba25…8d10

Appended block, Routed defect 1 (tip lines 140–143), exact token bytes (`od -c`):

```
7 b 1 1 b a 2 5 342 200 246 8 d 1 0     →  7b11ba25 + U+2026 (…, e2 80 a6) + 8d10
```

Prefix `7b11ba25` = first 8 hex of the full pin `7b11ba25…3598d10`; suffix `8d10` = last 4. **The correction names the frozen pin.** Both byte sides of the correction:

- stale side (pre-append, tip line 128): ``author the sealed held-out set against tool sha `7a59f576…8833` (amendment 3)`` — present in the 051c1e65 blob;
- corrected side (append, tip lines 141–143): names `7b11ba25…8d10` per amendment 5 (`ee398492`), matching the frozen pin and the byte-exact tip tool.

## Bonus cross-checks (append-block internal honesty)

- Defect 4 word count: the Gate quote `"The doctest module searches for pieces of text that look like interactive Python sessions"` is **14 words** (python3 split) — the append's "14, not 17" correction is true; the stale "17 words" at line 22 is left untouched exactly as the append discloses.
- Counter identity: `git show 6aaad5b389e…:.ufo/evidence/round-33/c1/c1-measure.py | sha256sum` → `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` — equals the frozen counter sha; byte-identical at tip (`git show 0b99d48e…:…` same digest); `6aaad5b` is an ancestor of tip (rc=0); `ho_witness_ok` present (2 hits).
- Amendment 6 disclosure: `.ufo/evidence/round-33/contract-amendments.json` (list of 6) records "SET-AWARE pre-authoring (r34; routed RevengerWitness Q1b/Q3/Q3b …) adopted BEFORE any sealed held-out authoring" — matches the append's amendment-6 paragraph.

## Findings

None. No byte-side drift on any routed claim: append-only holds, the S100 Gate digest matches the committed snapshot, and the stale-pin correction names the frozen `7b11ba25…8d10`.

## Residual risk / gaps

- Kill rule consumed: the deciding measurement was not re-run; counter functions were not imported (no counter execution was in scope for this seat).
- The snapshot digest is verified against the tip-committed bytes only; no live re-fetch was performed (by the row's own pin rule this is the correct target, so no gap in the claim itself).
- Defect 2 (post-report commit ordering) and defect 4's "Gate row untouched" are accepted from the append's own disclosure plus the append-only proof; I did not re-audit r33 seat-report tracking state.
