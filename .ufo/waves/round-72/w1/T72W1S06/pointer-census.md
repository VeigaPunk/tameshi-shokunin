# Pointer census — T72W1S06 (read-only reconnaissance)

Scope: line-pointer tokens in the lane's own records, resolved against the
worktree; stale-citation risk only. No tracked file was edited.

## State measured

- Lane HEAD `b7b983754b81931b5ba22f0441d9772a1a0585a7` at
  `2026-11-04T00:31:54Z` (UTC), worktree with uncommitted appends to
  `corpus/lessons/round-72.md` and `.ufo/evidence/round-72/*.out`.
- The lane was live during the census: HEAD moved
  `dfb534ca` → `93cae77b` → `b611e763` → `b7b98375`, and `SCORECARD.md`
  grew 4347 → 4376 lines, `PROVINCE.md` 160 → 170 lines. Every number below
  is from the final snapshot only; earlier snapshots were discarded.
- Final line counts and hashes (`wc -l`, `sha256sum`):

| file | lines | sha256 (first 16) |
|---|---|---|
| PROVINCE.md | 170 | 985d295610fbc0e4 |
| SCORECARD.md | 4376 | 46ef4866e692732b |
| LOG.md | 3741 | 78d26eab2e5521b1 |
| corpus/SOURCES.md | 562 | 7743b52d8c75c13f |
| tools/mutate-and-run.sh | 2159 | 977de47034cbe52b |
| tools/repeat-control.py | 947 | a8fad68fcbb87d03 |
| tools/registry-check.py | 1996 | (state-sha.txt) |

## Grammar and surfaces

Token grammar (two forms, both enumerated):

1. path-qualified: `<path>.<ext>:L?<start>(-<end>)?`, with comma
   continuations (`PROTOCOL.md:63-73,340-343`); `ext` ∈
   {md,py,sh,json,txt,html,yml,yaml,toml,jsonl,out,diff}.
2. backticked bare span: `` `:<start>(-<end>)?` `` — includes the
   `:8[0-9]-9[0-9]`-style family named in the assignment.

Surfaces (96 files): `corpus/lessons/round-6*.md` and `round-7*.md`
(25 files; the literal glob also matches `round-71.md` and `round-72.md`),
`PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `corpus/knowledge/*.md` (68).

Resolution order per token: exact lane-relative path; then
`.ufo/` prefix for `ufo/…`; then canonical basename locations
(`corpus/knowledge/`, `corpus/lessons/`, `corpus/`, `tools/fixtures/`,
`tools/`, `plans/`, `reports/`, root); then a unique basename anywhere in
the lane; else `target-missing` / `ambiguous`. Bare spans are attributed to
the nearest preceding path token on the same line, else the nearest path
token in the same paragraph (≤8 lines back), else `unattributed`.

Commands (scratch scripts, deleted after the run per seat discipline; the
grammar above is the reproducible part):

```
python3 -I -X utf8 /fast/scratch/hyaku/tameshi-r72/T72W1S06/census2.py > census-final2.json
python3 -I -X utf8 /fast/scratch/hyaku/tameshi-r72/T72W1S06/final.py   > final2.json
python3 -I -X utf8 tools/pointer-recheck.py --repo . --manifest tools/pointer-recheck.json
python3 -I -X utf8 tools/pointer-recheck.py --repo . --manifest .ufo/evidence/round-72/control-manifest.json
wc -l PROVINCE.md SCORECARD.md LOG.md corpus/SOURCES.md tools/mutate-and-run.sh tools/repeat-control.py
```

## Counts (census-final2.json)

| measure | count |
|---|---|
| files scanned | 96 |
| tokens total | 2310 |
| path-qualified tokens | 1106 |
| bare spans | 1204 |
| resolvable (lane target, in range) | 995 |
| out-of-range (lane target, span past EOF) | 30 |
| target-missing (lane scope) | 302 |
| ambiguous (lane scope, multiple basenames) | 53 total: 44 lane + 9 external |
| external target-missing | 19 |
| unattributed bare spans | 911 |
| `:8x-9x`-style bare spans | 37 |

Calibration on the 302 "lane" target-missing: 270 are bare basenames
(`claim-ledger.sh` 71, `surface-census.sh` 46, `scope-gate.sh` 31,
`op-ref-probe.sh` 25, `drift-pins.sh` 21, `checklist-run.sh` 14) that name
sibling-lane scripts, not lane files; only 32 are path-shaped, and most of
those are `.ufo/…` paths written without the leading dot or sibling-lane
paths. The 302 is therefore an upper bound on genuine lane-file misses, not
a defect count.

## Per-surface counts

Columns: path tokens, bare spans, lane-resolvable, lane-out-of-range,
lane-target-missing, lane-ambiguous. Surfaces with zero tokens are omitted.

| surface | path | bare | res | oor | miss | amb |
|---|---|---|---|---|---|---|
| corpus/knowledge/gates-survey-kagi.md | 126 | 55 | 12 | 4 | 156 | 0 |
| corpus/knowledge/verification-patterns-fleet.md | 143 | 7 | 51 | 5 | 68 | 18 |
| corpus/knowledge/arm-class-matrix.md | 2 | 279 | 1 | 0 | 2 | 0 |
| corpus/knowledge/operator-runbook.md | 94 | 56 | 117 | 0 | 0 | 0 |
| corpus/knowledge/service-limits.md | 75 | 65 | 119 | 3 | 4 | 0 |
| corpus/knowledge/fleet-suite-census.md | 34 | 180 | 37 | 8 | 3 | 0 |
| corpus/knowledge/guard-kill-closure.md | 99 | 4 | 100 | 2 | 0 | 0 |
| corpus/knowledge/service-standing-state.md | 65 | 29 | 91 | 0 | 0 | 0 |
| corpus/knowledge/closeout-r11.md | 54 | 36 | 55 | 0 | 6 | 0 |
| SCORECARD.md | 59 | 14 | 67 | 1 | 0 | 1 |
| LOG.md | 44 | 14 | 49 | 1 | 2 | 0 |
| corpus/knowledge/service-optin-protocol.md | 52 | 0 | 43 | 1 | 0 | 0 |
| corpus/knowledge/mutation-score-semantics.md | 45 | 0 | 43 | 0 | 2 | 0 |
| corpus/knowledge/fleet-kill-rate-ledger.md | 25 | 32 | 26 | 0 | 1 | 0 |
| corpus/knowledge/mutation-case-kagi-census.md | 16 | 29 | 4 | 1 | 30 | 0 |
| corpus/knowledge/flaky-aware-verdict-evidence.md | 3 | 55 | 17 | 0 | 0 | 0 |
| corpus/knowledge/mutation-case-tsukuroi-census.md | 11 | 51 | 0 | 1 | 10 | 0 |
| corpus/knowledge/mutation-case-kagi-checklist.md | 10 | 46 | 9 | 0 | 3 | 0 |
| corpus/knowledge/mutation-case-kumitate-claims.md | 0 | 64 | 0 | 0 | 0 | 0 |
| corpus/knowledge/incremental-pin-disposition.md | 13 | 17 | 18 | 3 | 0 | 0 |
| corpus/knowledge/repeated-control-precondition.md | 13 | 16 | 16 | 0 | 0 | 2 |
| corpus/knowledge/mutation-case-mado-verify.md | 1 | 41 | 1 | 0 | 0 | 0 |
| corpus/knowledge/mutation-case-kagi-drift-pins.md | 10 | 15 | 8 | 0 | 9 | 0 |
| corpus/knowledge/regression-tally-completeness.md | 19 | 0 | 9 | 0 | 0 | 10 |
| corpus/knowledge/mutation-case-kumitate-sources-check.md | 11 | 10 | 13 | 0 | 0 | 0 |
| PROVINCE.md | 9 | 8 | 10 | 0 | 0 | 3 |
| corpus/knowledge/mte-report-interop.md | 6 | 13 | 10 | 0 | 0 | 0 |
| corpus/knowledge/r5-undetected-flaky-failures.md | 11 | 1 | 12 | 0 | 0 | 0 |
| corpus/knowledge/r8-gtest-order-and-seed.md | 1 | 20 | 3 | 0 | 0 | 0 |
| corpus/knowledge/input-keyed-coldread-credit.md | 10 | 0 | 0 | 0 | 0 | 10 |
| corpus/knowledge/r42-attribute-and-outflag-destinations.md | 3 | 7 | 10 | 0 | 0 | 0 |
| corpus/lessons/round-71.md | 4 | 4 | 5 | 0 | 1 | 0 |
| corpus/knowledge/witness-scoped-kill-verdict.md | 6 | 0 | 6 | 0 | 0 | 0 |
| corpus/lessons/round-72.md | 1 | 6 | 3 | 0 | 0 | 0 |
| corpus/knowledge/r41-variable-destination-writes.md | 2 | 4 | 3 | 0 | 0 | 0 |
| corpus/knowledge/gates-survey-kumitate.md | 4 | 0 | 4 | 0 | 0 | 0 |
| corpus/knowledge/pit-outcome-vocabulary.md | 3 | 1 | 4 | 0 | 0 | 0 |
| corpus/knowledge/mutation-case-kimi-census.md | 1 | 5 | 1 | 0 | 0 | 0 |
| corpus/knowledge/delta-debugging-minimization-contract.md | 3 | 0 | 3 | 0 | 0 | 0 |
| corpus/knowledge/mutation-case-kumitate-cite-check.md | 1 | 4 | 1 | 0 | 0 | 0 |
| corpus/lessons/round-71-verifier-spotcheck.md | 0 | 6 | 0 | 0 | 0 | 0 |
| corpus/lessons/round-62-verifier-spotcheck.md | 1 | 3 | 1 | 0 | 0 | 0 |
| corpus/knowledge/oracle-anchored-survivors.md | 1 | 2 | 0 | 0 | 1 | 0 |
| corpus/knowledge/receipt-revision-binding.md | 1 | 1 | 2 | 0 | 0 | 0 |
| corpus/knowledge/survivor-fixture-minimization.md | 1 | 1 | 0 | 0 | 2 | 0 |
| corpus/lessons/round-60-verifier-spotcheck.md | 2 | 0 | 0 | 0 | 2 | 0 |
| corpus/lessons/round-60.md | 2 | 0 | 2 | 0 | 0 | 0 |
| corpus/knowledge/mutation-case-kumitate-round-gate.md | 1 | 1 | 1 | 0 | 0 | 0 |
| corpus/knowledge/callback-authoritative-accounting.md | 1 | 0 | 1 | 0 | 0 | 0 |
| corpus/knowledge/fixture-shrinking-pilot.md | 1 | 0 | 1 | 0 | 0 | 0 |
| corpus/knowledge/gate-row-exit-map.md | 1 | 0 | 1 | 0 | 0 | 0 |
| corpus/knowledge/r6-flaky-failures-cluster.md | 1 | 0 | 1 | 0 | 0 | 0 |
| corpus/knowledge/r9-false-red-rate.md | 1 | 0 | 1 | 0 | 0 | 0 |
| corpus/knowledge/required-command-binding.md | 1 | 0 | 1 | 0 | 0 | 0 |
| corpus/knowledge/self-hardening-r6.md | 0 | 2 | 0 | 0 | 0 | 0 |
| corpus/lessons/round-67-verifier-spotcheck.md | 1 | 0 | 1 | 0 | 0 | 0 |
| corpus/lessons/round-69-verifier-spotcheck.md | 1 | 0 | 1 | 0 | 0 | 0 |

## Out-of-range lane tokens (30)

By target (`wc -l` on the resolved path): `SHONEN.md` 7 (file 12 lines;
`SHONEN.md:5-34`, `:14`, `:36`), `corpus/knowledge/gates-survey-kumitate.md`
5, `README.md` 4 (lane README 14 lines — several of these are almost
certainly fleet/kagi READMEs mis-resolved by basename), `arm-class-matrix.md`
3, `.ufo/waves/round-18/w1/X03DefectProbes.md` 2, `plans/round-10-record-draft.md`
2, `plans/round-5-record-draft.md` 2, `mutation-case-mado-verify.md` 2, and
1 each for `mutation-case-kagi-census.md`, `mutation-case-kimi-census.md`,
`fleet-kill-rate-ledger.md`.

Two are self-documented: `corpus/knowledge/verification-patterns-fleet.md:283`
says the `SHONEN.md:14` parenthetical "no longer resolves", and line 287
records that `SHONEN.md:36` carries the text now. These are disclosed drift,
not hidden defects.

## `:8x-9x`-style spans (37)

LOG.md 8, PROVINCE.md 7, `corpus/lessons/round-72.md` 6, SCORECARD.md 5,
`round-71-verifier-spotcheck.md` 4, `round-71.md` 3, `closeout-r11.md` 2,
`incremental-pin-disposition.md` 1, `repeated-control-precondition.md` 1.
The PROVINCE/LOG/SCORECARD/round-71/72 occurrences are the round-16
`mutate-and-run.sh:85-91` family (the red arm and its correction), not
independent targets. `closeout-r11.md:89` `:85-97` is a sibling-lane script
(`js-claims-check`), unattributed.

## Coverage against the eight frozen rows

Manifest run at the pre-C2 state (HEAD `dfb534ca`, 8 rows):
`POINTER_RECHECK: rows=8 met=8 unexpected=0`, exit 0. At the final state the
manifest has 11 rows and prints `rows=11 met=11 unexpected=0`; the three new
rows (`sources-s303-sed-4-2`, `province-r72-tenleg-88-97`,
`province-r72-sevenleg-cut-88-94`) are the round-72 C2 rows.

| frozen row | record in my surfaces? | exact discovered tokens | same-target citations elsewhere |
|---|---|---|---|
| lesson-r48-s267-pointer-140 | no (round-48) | 0 | LOG, SCORECARD, round-71 |
| lesson-r48-s268-pointer-141 | no (round-48) | 0 | LOG, SCORECARD, round-71 |
| lesson-r48-erratum-s267-142 | no | 0 | none |
| lesson-r48-erratum-s268-143 | no | 0 | none |
| spotcheck-r48-rows-142-143 | no | 0 | none |
| province-r16-sevenleg-85-91 | yes (PROVINCE.md) | 1: `PROVINCE.md:57` `` `:85-91` `` | SCORECARD, incremental-pin-disposition, mutation-score-semantics, operator-runbook, repeated-control-precondition |
| scorecard-r1-verdicttable-13-14 | yes (SCORECARD.md) | 2: `SCORECARD.md:43`, `:4210` | LOG, closeout-r11, round-71 |
| scorecard-r1-verdicttable-log68 | yes (SCORECARD.md) | 2: `SCORECARD.md:43`, `:4211` | LOG, closeout-r11, round-71 |

So 5 of 8 frozen records lie outside the assigned surfaces, and the 3 that
are inside contribute 5 exact tokens. Coverage of the assigned surfaces is
therefore thin by construction; the ranked list below is the uncovered set.

Churn backing the ranking (`git log --oneline -- <path> | wc -l`; last
commit date `git log -1 --format=%cs`): SCORECARD.md 158 / 2026-11-03,
LOG.md 159 / 2026-11-03, corpus/SOURCES.md 82 / 2026-11-03,
PROVINCE.md 12 / 2026-11-03, tools/mutate-and-run.sh 12 / 2026-10-26,
tools/registry-check.py 10 / 2026-10-28, tools/repeat-control.py 4 /
2026-10-28. Every row of the per-surface table comes from the single census
run named above; no row was hand-edited.

## Ranked uncovered candidates (top 10)

Score = churn weight (SOURCES/SCORECARD 5; LOG/mutate-and-run/repeat-control 4)
+ needle specificity (2 named symbol/formula/count, 1 generic)
+ drift evidence (3 verified correct at an earlier rev; 2 verified wrong at
the record's own rev) + 1 if the record is a spotcheck/verdict claim.
Every row below was hand-checked against the target bytes at the final
snapshot; "first line" is the first line in the target carrying the needle.

| # | record:line | token | target lines | needle | first line | rev check | class | score |
|---|---|---|---|---|---|---|---|---|
| 1 | corpus/lessons/round-62-verifier-spotcheck.md:88 | corpus/SOURCES.md:539 | 562 | `12 words` | 178 (also 551, 553) | correct at `ed3a66c2` (line 539 carried it) | drift | 11 |
| 2 | SCORECARD.md:1557 (also 2219, 2311, 2375) | tools/mutate-and-run.sh:87-95 | 2159 | "nine legs" | — (tip span holds 8 leg lines) | nine legs sat at 87-95 at round 31; the round-51 edit inserted the header line and a tenth leg | drift | 9 |
| 3 | corpus/knowledge/fleet-kill-rate-ledger.md:86 | tools/mutate-and-run.sh:482-483 | 2159 | `PIN_JS`, `PIN_BASH` | 614, 616 | correct at round 6 (`44947154`: 482/483); stale at its own round-7 rev (511/513) | drift | 9 |
| 4 | corpus/knowledge/mutation-case-kagi-drift-pins.md:49 | tools/mutate-and-run.sh:545-551 | 2159 | `KILLED` = exit not in `{0,124,126,127}` | case at 554, KILLED at 559, literal set at 982 | case block was 545-551 at round 30; shifted by the round-51 edit | drift | 9 |
| 5 | SCORECARD.md:1904 and LOG.md:2088 | tools/repeat-control.py:807-823 | 947 | `expected.json`, `os.symlink` | 51, 852 | correct at round-40 rev (`9df9212d`: os.symlink at 820) | drift | 9 |
| 6 | corpus/knowledge/mutation-score-semantics.md:53 | tools/mutate-and-run.sh:84-92 | 2159 | six-leg rates `8/10, 8/10, 6/10, 4/10, 7/15, 7/10` | legs 88-92 only (5 legs) | six legs sat at 84-89 at `606716f7` (its verified rev) | drift | 9 |
| 7 | corpus/knowledge/mte-report-interop.md:113 | tools/mutate-and-run.sh:562 | 2159 | `pct=$(( (200 * killed + total) / (2 * total) ))` | 579 | at its verified rev `a08e85c5` the formula was 568 (already off by 6) | wrong at write | 8 |
| 8 | corpus/knowledge/repeated-control-precondition.md:49 | tools/repeat-control.py:191-205 | 947 | `controls_mismatch` precedence | classify at 238, return at 249 | at its rev `9df9212d` classify started 206, return 217 (span stops at 205) | wrong at write | 8 |
| 9 | corpus/knowledge/mutation-case-kagi-drift-pins.md:182 | tools/mutate-and-run.sh:1418-1428 | 2159 | `sandbox-$DEFECT_ID` | 1491 | at its own rev the span is usage validation; sandbox at 1491 | wrong at write | 8 |
| 10 | corpus/knowledge/repeated-control-precondition.md:51 | tools/repeat-control.py:185-188 | 947 | `setup_error` | 222 (`def setup_failure`) | at its rev setup_failure was 200-203; span is `write_new`/`finish` | wrong at write | 8 |

Next uncovered (not in the top 10): `mutation-case-kagi-drift-pins.md:192`
→ `mutate-and-run.sh:452-456` (`DEFECT_ID`), same class and score 8.

Evidence notes for the top rows (all commands read-only, final snapshot):

1. `grep -n "12 words" corpus/SOURCES.md` → 178, 551, 553; line 539 is the
   Round 53 note. `git show ed3a66c2:corpus/SOURCES.md | sed -n '539p' |
   grep -o "12 words"` → `12 words`. The pointer was correct at its rev and
   drifted when rows were inserted above it.
2. `sed -n '87,95p' tools/mutate-and-run.sh | grep -c "^#   [a-z]"` → 8 at
   the tip; `git show bb681566:tools/mutate-and-run.sh | nl -ba | sed -n
   '84,97p'` → the nine legs sat at 87-95 at round 31. The round-51 edit
   (header line 84 + tenth leg) moved the ledger to 88-97, so the same span
   now covers eight legs. `grep -n "nine legs" tools/mutate-and-run.sh` → no
   hit (the count word lives in SCORECARD, not the tool).
3. `git show 44947154:tools/mutate-and-run.sh | grep -n "PIN_JS=\|PIN_BASH="`
   → 482/483; `git show 9f1d3c33:…` → 511/513; tip → 614/616.
4. `git show bb681566:tools/mutate-and-run.sh | sed -n '540,560p'` shows
   `case $RC in` at 545 and `*) v=KILLED` at 551; tip has `case` at 554 and
   `KILLED` at 559.
5. `git show 9df9212d:tools/repeat-control.py | grep -n "os.symlink"` →
   820; tip → 852 and 866.
6. `git show 606716f7:tools/mutate-and-run.sh | sed -n '84,92p'` → six leg
   lines at 84-89; tip → legs at 88-97.
7. `git show a08e85c5:tools/mutate-and-run.sh | grep -n "200 \* killed"` →
   568; note says 562; tip → 579.
8. `git show 9df9212d:tools/repeat-control.py | grep -n '^def classify\|return "controls_mismatch"'` →
   `def classify` 206, `return "controls_mismatch"` 217.
9. `git show 6d8c11e3:tools/mutate-and-run.sh | sed -n '1418,1428p'` →
   usage validation; `sandbox-$DEFECT_ID` at 1491.
10. `git show 9df9212d:tools/repeat-control.py | sed -n '180,210p'` →
    `def setup_failure` 200; span 185-188 is `write_new`/`finish`.

## Calibration: excluded and false positives

- **Rev-scoped, not defects.** `corpus/knowledge/guard-kill-closure.md`
  defines `[lane:P:L]` as `P` at line `L` **at 183f87b**. Its five `[lane:`
  pointers were checked at that rev and all verify: `registry-check.py:281`
  = `json.loads`, `:306` = `def _kill_group`, `:313`/`:321` = `os.killpg`,
  `evidence-disposition.py:450` = `merge-base`, `:518` = `tree_entry(…,
  "HEAD", …)`. They read out-of-content against the tip but are correct
  where the record binds them.
- **Needle-generic false positives.** Exact-string needles falsely flag
  `round-60.md:244` (`blob_bytes()` vs `blob_bytes(repo, oid, env)` at 251),
  `round-67-verifier-spotcheck.md:84` (`rev-list --reverse base..tip` vs the
  `run(repo, "rev-list", "--reverse", …)` form at 144), and
  `mutation-score-semantics.md:53`'s composite rate string. These are
  plausible and are not ranked.
- **Mis-resolution by bare basename.** `mutation-case-kumitate-sources-check.md:237`
  cites `SOURCES.md:8` for a *fixture* (`S_DUP_LINE` duplicate-id fixture),
  not `corpus/SOURCES.md`; `ID_DUPLICATE` occurs nowhere in the lane file.
  `README.md:43` and several `gates-survey-kumitate.md` spans are likely
  fleet READMEs. The census resolves these mechanically and therefore
  over-reports out-of-range/missing; they are excluded from the ranking.
- **Bare-span attribution is a heuristic.** Nearest-preceding-path
  mis-assigns two known cases: `corpus/lessons/round-71.md:109` and
  `SCORECARD.md:4205` cite `` `:85-91` `` with `corpus/SOURCES.md` as the
  nearest path, but the span belongs to `tools/mutate-and-run.sh` (the
  context names `js-round-gate` at 94). The ranked list was corrected by
  hand; the 911 unattributed bare spans are reported as counts only.
- **Live worktree.** Line numbers moved during the census (SCORECARD
  4347→4376, PROVINCE 160→170, HEAD four times). A reader must re-run at the
  commit they are judging; the snapshot hash above is the only claim.

## Instrument observations (for the L1, not verdicts)

1. **Control-manifest row count vs the frozen plan.** The plan's C2 counter
   says the control manifest holds "the same three rows … `rows=3 met=3`".
   The committed `.ufo/evidence/round-72/control-manifest.json` has **2**
   rows (`sources-s303-control-base`, `province-r72-control-stale-85-91`),
   and the tool prints `POINTER_RECHECK: rows=2 met=2 unexpected=0`. The two
   rows present read `miss ok`; the third frozen row is absent.
2. **Main manifest.** `tools/pointer-recheck.json` has 11 rows at the final
   state; `rows=11 met=11 unexpected=0`, exit 0 — matching the plan's frozen
   `rows=11 met=11`. The 8-row frozen set read `rows=8 met=8` at the pre-C2
   commit.
3. **The red arm is measured, not corrected.** `province-r16-sevenleg-85-91`
   still reads `miss ok`; the PROVINCE append at lines 149-160 carries the
   correction (`:88-94` seven-leg cut, `:88-97` ten-leg ledger), and the two
   new rows read `hit ok`. Direct check: legs sit at 88-97; leg 7
   `js-round-gate` at 94; leg 10 `bash-drift-pins` at 97.
