# ResidualAppendOnly — append-only attack on the landed round 41

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
Base `a3d6c690bcbf8914551d4f4e8e1612784c1c2046` · measured `2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6` · tip `812ee0d11d267e131be3dc8db0b71253cbae9234`
Verdict: **4 PASS, 2 DEFECT** (both defects real, one of them proven avoidable).

Scope rule applied: the assignment's criterion is `git diff --numstat` = 0 deletions for LOG.md / SCORECARD.md, byte-identity for the two round-40 lesson files and SHONEN.md, and additions-only for `corpus/QUALITY.md` / `corpus/README.md`.

## Command used for every numstat statement

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --numstat \
  a3d6c690bcbf8914551d4f4e8e1612784c1c2046 812ee0d11d267e131be3dc8db0b71253cbae9234 -- \
  corpus/lessons/round-40.md corpus/lessons/round-40-verifier-spotcheck.md SHONEN.md \
  LOG.md SCORECARD.md corpus/QUALITY.md corpus/README.md
```

Output, verbatim (a path absent from numstat is byte-identical across the range):

```
95	2	LOG.md
94	1	SCORECARD.md
32	0	corpus/QUALITY.md
13	0	corpus/README.md
```

Same command with the second revision replaced by the **measured** commit `2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6` returns the same four lines — the deletions were already in the measured state, not added afterwards.

Corroboration that these are the *only* deletions in the whole landing:

```
git diff --numstat a3d6c690 812ee0d1 | awk '$2>0 {print}'
95	2	LOG.md
94	1	SCORECARD.md
```

(89 changed paths at the range; every other path is 0-deletion, and `git diff --summary` reports only `create mode` entries — no deletes, no renames.)

## Per-file verdicts

| # | File | Criterion | numstat | Verdict |
|---|---|---|---|---|
| 1 | `corpus/lessons/round-40.md` | byte-identical | *(absent)* | **PASS** |
| 2 | `corpus/lessons/round-40-verifier-spotcheck.md` | byte-identical | *(absent)* | **PASS** |
| 3 | `SHONEN.md` | unchanged | *(absent)* | **PASS** |
| 4 | `LOG.md` | additions only | `95	2` | **DEFECT** |
| 5 | `SCORECARD.md` | additions only | `94	1` | **DEFECT** |
| 6 | `corpus/QUALITY.md` | additions only | `32	0` | **PASS** |
| 7 | `corpus/README.md` | additions only | `13	0` | **PASS** |

### 1–3 PASS — identical blobs, not merely absent from diff

Absence from numstat can also mean "untracked at one end", so each was checked by blob id and content sha256 at both revisions:

```
git rev-parse <REV>:<path>            # blob id
git cat-file -p <REV>:<path> | sha256sum
```

```
corpus/lessons/round-40.md                 blob= c4c65c40fa5e89bac293d22f2ecbf19620eb43b8 (both)  sha256=9fcaf9769054a30c5bebf668a94f22fa3d4a222029075c3a75052b02efb5b83a (both)
corpus/lessons/round-40-verifier-spotcheck.md blob= be4e10d7d593916ce2cc1bf93155322883bd710f (both) sha256=d4aa77b826b50e92ad598159a2f539ff6bc939da96e81f05f2b415e660717051 (both)
SHONEN.md                                  blob= 253f3c05d5a78fed5d6538d54351d1ef930b6937 (both)  sha256=55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09 (both)
```

The round's own claim survives: `LOG.md` round-41 entry says "The round-40 file is not rewritten: the correction is appended in `corpus/lessons/round-41.md`" (tip `LOG.md:2128-2129`) — true for `round-40.md`, and the round-40 spotcheck file is untouched too.

### 6–7 PASS — true EOF appends

`git diff -U0 <base> <tip> -- <file> | grep '^@@'`:

```
corpus/QUALITY.md   @@ -965,0 +966,32 @@
corpus/README.md    @@ -511,0 +512,13 @@
```

Line counts `965 → 997` and `511 → 524`. Both hunks are pure insertions at the old EOF; nothing above the last line moved.

### 4 DEFECT — `LOG.md` rewrites two prior-round bullets in place

`git diff -U0 <base> <tip> -- LOG.md | grep '^@@'`:

```
@@ -2069 +2069,10 @@ Motivating evidence: `corpus/lessons/round-38-verifier-spotcheck.md` routed thre
@@ -2079 +2088,10 @@ Motivating evidence: `corpus/lessons/round-39-verifier-spotcheck.md` routed one
@@ -2091,0 +2110,75 @@ Motivating evidence: the first L1 for round 40 died on a provider-route failure
```

Two single-line replacements plus one genuine 75-line append. The two replaced lines are **not** round-41 lines — they are the closing bullets of two *earlier* rounds:

```
git show a3d6c690:LOG.md | grep -n 'Command D at the measured commit'
2069:- Command D at the measured commit: `recorded_cases=9 depth_score=9`. No axis harmed.   # round 39 section (## … round 39 at :2061)
2079:- Command D at the measured commit: `recorded_cases=9 depth_score=9`. No axis harmed.   # round 40 section (## … round 40 at :2071)
```

Both were replaced by a 9-line block about **round 41**; `git diff` shows the added text beginning "`- Command D at the measured commit: … and command C boxes=4 checked=0 asserted=4 untouched=0, both in .ufo/evidence/round-41/census/command-d.stdout …`" followed by "`- Receipts after the deciding runs: .ufo/evidence/round-41/after/ …`".

Three concrete harms, each checkable:

1. **A recorded verdict is erased.** The sentence `No axis harmed.` existed for rounds 39 and 40 at base and now exists **nowhere** in LOG.md: `grep -c 'No axis harmed'` on the tip file returns 0. Round 41's own no-harm statement lives in SCORECARD, so nothing replaced it for those two rounds.
2. **Round-41 material is attributed to rounds 39 and 40.** A reader of `## … round 39` now reads `.ufo/evidence/round-41/after/` and "the carried `8` is superseded" — claims that round never made.
3. **The insertion is pure duplication, so nothing required it.** The inserted blocks are byte-identical to the canonical block inside the round-41 section:

```
tip LOG.md:2069-2077 == 2168-2176  -> True
tip LOG.md:2088-2096 == 2168-2176  -> True
```

`grep -c 'Receipts after the deciding runs'` on the tip: **3** (lines 2073, 2092, 2172). The canonical copy at `:2168` was added by the same range's `@@ -2091,0 +2110,75 @@` append. Deleting the two prior-round lines contributed **zero** information to the record and destroyed the two historical bullets; the append-only form (leave `:2069`/`:2079` as written, keep the single canonical block at `:2168`) was available at no cost.

Precedent inside the same file shows the lane knows that form: `SKILL.md:24` "Errata append-only; rejections kept."; `SCORECARD.md:1497` "Erratum to the round-30 block above (append-only; the block stays as written)"; `SCORECARD.md:206` "Append-only; the rows above stay as written and are superseded here". Neither the report nor the round-41 LOG/SCORECARD sections disclose that `LOG.md:2069`/`:2079` were rewritten — `grep -i 'append\|restat\|rewrit\|rephras'` over the round-41 LOG section names only the *lesson* repair.

Intermediate churn (does not change the verdict, explains the masking): `git diff --numstat baa18b7^ baa18b7 -- LOG.md` = `31 4`. The 4 deletions at that commit are the two base lines above plus one line of round-41's *own* text added earlier in the range (a `C2_R41: … rev=a3d6c690…` line, restored later), so the range nets to 2.

### 5 DEFECT — `SCORECARD.md` replaces the standing `sources-registry` row

`git diff -U0 <base> <tip> -- SCORECARD.md | grep '^@@'`:

```
@@ -1851 +1851 @@ this round deliberately did not take); the comparator lattice beyond POSIX `diff
@@ -1893,0 +1894,93 @@ Numeric axes, measured at `5641ed84c8dc148c34c8dd83f062279ddf06b4af`. **depth 9
```

Line 1851 (base) is the standing capability row; it was replaced, not superseded. The deleted cell fragment and what replaced it:

```
-  → 103 rows at round 35 (the "103 rows" this cell carried was a round-32 observation;
-    corrected 2026-10-23, round 35, per r34 AllFourScorecard F1)
+  → 109 rows at round 41 (restated from 103 by the round-41 C1 claim, whose m6 class
+    compares this cell to the registry at the measured revision)
```

Erased along with the stale number: the round-32 observation provenance, the `2026-10-23` date, the "round 35" attribution and the `r34 AllFourScorecard F1` citation — the errata chain that explains how the cell reached 103. That is the class of information `Errata append-only; rejections kept` exists to keep.

**The deletion was avoidable — proven, not inferred.** The counter reads the *last* matching row, so an appended restatement satisfies m6:

```
.ufo/evidence/round-41/calibration/measure.py:216-217
standing = [ln for ln in score_text.splitlines() if ln.startswith('| sources-registry |')]
… re.search(r'(\d+) rows', standing[-1])
```

Experiment (temp tree only, lane untouched): copy the lane tree to `/tmp/l41work` (no `.git`), restore `SCORECARD.md` to its base bytes, then insert a corrected `| sources-registry | … 109 rows at round 41 (restated by appending this row; the round-35 cell above is left as written) … |` row immediately after the base row. Run of the frozen counter against that tree:

```
python3 /tmp/l41work/.ufo/evidence/round-41/calibration/measure.py --lane /tmp/l41work --rev work
C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=2 sources_rows=109 rev=work C1_R41_PASS=true
EXIT=0
```

`C1_R41_PASS=true` with the base row intact. The append-only restatement also matches the lane's own precedent: the base file already carries **four** `| sources-registry |` rows (44 rows, 94 rows, and two earlier restatements at `:1609` and `:1851`) — restatement by appending a new row is the established mechanism, and round 41 is the first round to delete one instead.

Counter replays (all four are replays of receipted runs, not new measurements):

| revision | command | output | exit |
|---|---|---|---|
| base `a3d6c690` | `calibration/measure.py --lane … --rev a3d6c690bcbf…` | `MISMATCH m6 SCORECARD standing row says 103 rows, SOURCES.md has 107`; `MISMATCH m9 …` ; `C1_R41: m6=1 m7=0 m8=0 m9=1 total=2 records=0 sources_rows=107 … C1_R41_PASS=false` | 1 |
| measured `2ae00eb7` | `--rev 2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6` | `C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=3 sources_rows=109 C1_R41_PASS=true` | 0 |
| tip `812ee0d1` | `--rev 812ee0d11d267e131be3dc8db0b71253cbae9234` | identical to the row above (`rev=812ee0d1…`) | 0 |
| append-only simulation | `--rev work` in `/tmp/l41work` | `total=0 … C1_R41_PASS=true` | 0 |

The numeric verdict does not move: C1 is `PASS=true` at the measured commit and at the tip either way. The harm is to the record's provenance, not to the score.

## Why the criteria were applied as written

The assignment's criterion is mechanical (0 deletions). The round does not claim byte-level append-only for LOG.md/SCORECARD.md anywhere: `.ufo/reports/round-41/tameshi.md:32` says the standing row was "restated" (discloses a cell rewrite, not the deletion), and no amendment covers it — contract amendment **A3** is scoped `"lesson text only"` (`frozen_field: "record text, rule unchanged"`), A1/A2/A4/A5 are counter/fixture changes. So the SCORECARD deletion has neither an append-only form nor a declared amendment; the LOG deletion has neither a declared amendment nor any disclosure at all. Both are DEFECT under the stated criterion, and the SCORECARD one is additionally avoidable-with-PASS, which makes it actionable rather than forced by the frozen predicate.

## Residual risk

1. **Counter fragility exposed by the same edit.** `m6` trusts `standing[-1]`. Now that rows are edited rather than appended, nothing keeps the *number of* standing rows meaningful, and any later appended `| sources-registry |` row with a stale count silently re-breaks m6 with no history to compare against. The append-only mechanism was the thing that made the restatement chain auditable.
2. **Dirty-checkout evidence.** At read time the lane working tree carried two peer edits (`.ufo/waves/round-41/w1/ReviewScorecardNumbers.md`, `…/ScribeScorecard.md`, status `M`). They are residual-seat writes, not mine, and they do not touch any of the seven files; every verdict above is computed from committed revisions, not the working tree.
3. **Round-41's own committed text was rewritten mid-range** (baa18b7 `31 4` on LOG.md, `32 6` on SCORECARD.md). Those deletions are of lines added inside the same range, so they do not violate base→tip append-only, but they do mean the round's record was edited after commit; a reviewer comparing per-commit states sees more churn than the range diff shows.

## Verification gaps

- `lsp` is not mounted in this seat (`read xd://lsp` → `No such tool: xd://lsp`). The higher-fidelity tools for this task are git object reads and `python3` replays, which were used; no grep output is presented as semantic proof of anything beyond the literal line it prints, and every line-level claim above carries its `rev:line`.
- Did not run the C2 census counter (`census/measure.py`) — out of scope for append-only (it writes only to a temp dir and reads tool bytes, not these records); peer `L1Tameshi41.ResidualReplayC2` holds that replay.
- No installs or updates were performed (nothing was needed; pacman untouched).
- No files were written outside this report. `/tmp/l41work` is a disposable copy used only for the append-only simulation above.

## Findings, by severity

1. **HIGH — `LOG.md` (DEFECT, `95 2`):** in-place rewrite of the round-39 and round-40 closing bullets; `No axis harmed.` erased from both; round-41 receipt text duplicated into both prior-round sections although the identical block is already appended at `:2168`. Undisclosed in the round-41 records.
2. **MEDIUM — `SCORECARD.md` (DEFECT, `94 1`):** standing `sources-registry` row replaced in place, destroying the round-35 errata citation; an appended restatement row passes the frozen C1 predicate (`C1_R41_PASS=true` in a temp tree with the base row intact), so the deletion bought nothing.
3. **PASS — `corpus/lessons/round-40.md`, `corpus/lessons/round-40-verifier-spotcheck.md`, `SHONEN.md`:** identical blobs and identical sha256 at both revisions.
4. **PASS — `corpus/QUALITY.md` (`32 0`), `corpus/README.md` (`13 0`):** pure EOF appends.
