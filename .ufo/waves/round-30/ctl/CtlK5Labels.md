# CONTROL CtlK5Labels — meets=false C1_R30_PASS=false

Seat: TameshiR30.CtlK5Labels (leaf). Class: **K5 — shortcut keyed on labels** (contract.json
`controls_required_before_data`: "a selftest that checks the tally loop's operand names or count as
text"). Counter: frozen v2, sha256 `5ed4e663ff16556d0bfef68a9fc1e3cf820ab8bc2b620169e800da914f0c8719`,
**unchanged**. Scored on a sandbox clone, never on the lane.

## Summary line (verbatim from the counter)

```
C1_R30: rev=d28614b1c4670b82256a5f95ae211f3dbf7ccc18 pristine_selftest=1 harness=19/19 refused_drops=9/9 killed=9/13 equiv_pass=4/4 heldout_killed=5/12 heldout_equiv=4/4
PREDICATE: C1_R30_PASS=false
exit=1
```

Full receipt: `.ufo/evidence/round-30/ctl/CtlK5Labels.stdout` (33 `C1_R30_ROW` lines + the summary
+ `exit=1`). Diff: `.ufo/evidence/round-30/ctl/CtlK5Labels.diff`.

## The control (what was built)

Two additions to `tools/mutate-and-run.sh`, 27 inserted lines, nothing deleted, no pinned line
touched (loop line, three arm lines, FAIL check, tally-block start line, PASS printf all verbatim):

1. **K4 runtime guard**, copied from `.ufo/waves/round-29/w1/MutateLegSum.md` lines 183-189, placed
   after the SETUP branch and immediately before the PASS printf:
   `if (( npass + nfail + nsetup != nlegs )); then … REGRESSION: SETUP (case-tally mismatch …); exit 2; fi`.
2. **Label-keyed textual selftest case** (one new `st` case, "tally loop operand labels"), reading
   `"$SELF"` only — it never executes the tally block. Made as strong as a purely textual check on
   operand labels can be: exactly one `for st in …` line in the file; exactly nine quoted
   `"$st_*"` operands on it; names distinct; the name **set** equals the nine expected labels
   (`st_js st_kagi st_tsu st_mado st_checklist st_claims st_roundgate st_sourcescheck st_citecheck`,
   compared order-insensitively so the semantics-preserving reorder rewrites still pass); and each
   label also appears as its own `  <label>=$?` status assignment in the same file.

Pristine selftest after the change: `MUTATE_SELFTEST: 98/98 pass` / `VERDICT: PASS`, exit 0
(one case added to the existing 97; no case-count assertion elsewhere in the runner).

## Diff summary

```
 tools/mutate-and-run.sh | 27 +++++++++++++++++++++++++++
 1 file changed, 27 insertions(+)
```

Commit `d28614b1c4670b82256a5f95ae211f3dbf7ccc18` on base `e59728df5ebb053c9810049c05fd4e9d59d82dee`.

## Mutant rows

Killed (9/13 family, 5/12 held-out) — the drops only, because a drop changes the loop line's
operand set/count:

- `D1-drop-st_js` … `D9-drop-st_citecheck`: `selftest_exit=1 verdict_pass=0`
- `H01-drop`, `H02-drop`, `H03-drop`, `H04-drop`, `H12-drop`: `selftest_exit=1 verdict_pass=0`

**Surviving rows (the finding), all `selftest_exit=0 verdict_pass=1`:**

- family: `A1-pass-arm-noop`, `A2-fail-arm-as-pass`, `A3-fail-threshold`, `A4-setup-arm-as-pass`
- held-out: `H05-arm-noop`, `H06-arm-double`, `H07-fail-as-pass`, `H08-setup-as-pass`,
  `H09-fail-as-setup`, `H10-fail-thresh`, `H11-setup-thresh`

Equivalents all survive as required: `E1-reorder-operands`, `E2-arith-commuted`,
`E3-comment-in-block`, `E4-noop-before-pass`, `HE1..HE4-equiv` (4/4 and 4/4).

## What this says about the counter

- **The counter is not fooled by a label-keyed shortcut.** The shortcut kills every drop mutant by
  reading the operand list, but the arm mutants and their seven held-out respellings change only the
  case-arm lines / FAIL-SETUP thresholds, which no check on the loop line's operand labels can see.
  `killed=9/13` and `heldout_killed=5/12` hold the predicate at `false`. This is the intended
  separation: the counter's condition (d)/(f) measure detection of the tally's *arithmetic*, not its
  spelling, and v2's held-out generator (which shuffles operand order and respells arms) keeps that
  separation intact even for a check that hard-codes the nine names.
- **The K4 runtime guard is real and sufficient for (c) only.** With the guard present,
  `refused_drops=9/9` and `harness=19/19` (the guard sits after the FAIL/SETUP branches, so all 19
  pristine vectors keep their exact exit/word contract, and every drop refuses with
  `REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)` instead of a false PASS). But the
  guard is invisible to `--selftest` — condition (d) still requires the *detector* to notice arm
  mutations, and this control has no behavioral detector, so `killed` stays at 9/13.
- **No regression is introduced.** `pristine_selftest=1`, `equiv_pass=4/4`, `heldout_equiv=4/4`: the
  order-insensitive set comparison is the strongest form that does not falsely kill the
  semantics-preserving reorder rewrites (an order-sensitive variant would have failed `E1` and the
  shuffled held-out equivalents — a false-kill, i.e. a different and worse control).
- **Smallest safe correction implied for the *fix* (not for the counter):** a label check alone, even
  at maximum strength, cannot reach `C1_R30_PASS=true`; the fix needs the behavioral selftest
  (extracted tally block under fixed statuses) that the contract's reachability witness names. No
  counter, predicate, mutant-family or rewrite change is warranted by this control.

## Axes (godspeed framing)

Axes kept separate: (1) detector coverage of the tally's arithmetic (killed / heldout_killed);
(2) runtime refusal of incomplete tallies (refused_drops); (3) non-false-kill of equivalent rewrites
(equiv_pass / heldout_equiv); (4) pristine health (pristine_selftest, harness 19/19). Moves kept:
runtime guard (improves 2, harms none), order-insensitive nine-name set + count + distinctness +
per-label assignment check (improves 1 for drops, keeps 3 intact). Moves rejected: order-sensitive
name list and verbatim arm-line greps (harm axis 3, and would drift into K6 territory).

## Receipts and bounds

- Sandbox: `/fast/scratch/hyaku/tameshi-r30/ctl/CtlK5Labels/clone`, base `e59728d…`, control
  `d28614b…`. All git write commands ran there only, with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`
  unset. No `jj` command ran anywhere. Nothing written in the lane except the three receipt paths
  (this report, `ctl/CtlK5Labels.diff`, `ctl/CtlK5Labels.stdout`); the `ctl` directories were created
  for them.
- Every process bounded by `timeout` (counter 900 s, local selftest 600 s, probes 20 s-class); no
  background jobs, no subagents, no process left running; scratch probe files under `/tmp` removed.
- Tooling: **no installs or upgrades** (python3, bash, git, coreutils already sufficient). The one
  local `--selftest` run was 6.4 s; the counter run 43 s.
- Counter file was read, never edited; its sha256 was not re-derived here (it is frozen and recorded
  in `contract-amendment-1.json`).
