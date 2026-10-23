source: S087 — mutation-testing-metrics 3.9.0, `package/src/calculateMetrics.ts` and `package/src/model/metrics.ts` (external metric arithmetic, not tameshi's own kill-rate formula; re-opened round 30, `.ufo/waves/round-30/wA/ReopenS087.md`); S093 — bwrap(1), bubblewrap 0.13.1 `bwrap.xml` (the sandbox the v4 counter runs each selftest in); S094 — Dwork et al., arXiv:1411.2664v3 §1 (a held-out test kept from the candidate)
verified-at: 2026-10-23 — sources re-opened by round-30 wave-A seats; fix, counters, amendments 1-4 and pre-data control receipts inspected; this entry records no lane-head measurement
recheck: `bash tools/mutate-and-run.sh --selftest` in a clone (the tally harness cases); counter recipe, not a result: `timeout 900 python3 .ufo/evidence/round-30/c1-measure-v4.py --repo CLONE --rev REV --sealed .ufo/evidence/round-30/v4/c1-sealed.json --jobs 4`; re-open S087, S093, S094

# Regression tally completeness: a local invariant and behavioral detector

Round 30 claim C1 is on the **operability** axis and is **exploratory** (`.ufo/evidence/round-30/contract-amendment-4.json`): a control met the frozen counter v4 before data, so the claim carries no counting command and is judged by a named non-author reviewer. Its surface is the `--regression` case-tally block in `tools/mutate-and-run.sh` and the runner's own `--selftest` as its detector. The contract routes it from `corpus/lessons/round-29-verifier-spotcheck.md` item 7 and `corpus/lessons/round-29.md` item 4.6 (`.ufo/evidence/round-30/contract.json:10-14`). This page explains the local defect and the pre-data measuring design; it does not report a lane-head result.

## The original gap

The Round 29 `MutateLegSum` report removed only `"$st_citecheck"` from the tally operand list in an isolated clone. The runner still declared nine legs, while the mutant summed eight operands. With its ninth status fixed to 0, 1, or 2, the extracted tally printed `REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)` and exited 0 each time. The same mutant's existing selftest remained green at 97/97. This was a one-line test mutation, not a claim that the pristine Round 29 runner had already lost a leg (`.ufo/waves/round-29/w1/MutateLegSum.md:9-17,28-38,90-114,135-156`).

The gap was local: the aggregation did not verify that its status counts equaled `nlegs`, and the old selftest did not execute the tally block under statuses that would expose an omitted operand.

## Frozen fix witness

`witness/fix.diff` records a candidate fix in a sandbox, not evidence that the lane head contains it. In `run_regression`, the diff adds a guard after the existing FAIL and SETUP decisions and before PASS. If `npass + nfail + nsetup != nlegs`, it prints `REGRESSION: SETUP (case-tally mismatch: cases=N counted=M)`, keeps the work directory, and exits 2 (`.ufo/evidence/round-30/witness/fix.diff:9-20`). This is a runner-local completeness invariant; S087 is not the authority for requiring it.

The same diff adds a behavioral case to `--selftest`. It extracts the tally block from the runner using the literal block-start marker, obtains the nine status variable names from the function's `st_*=$?` assignments, and requires exactly nine names (`fix.diff:25-33`). It invokes the extracted block in separate Bash processes under 19 fixed vectors: all nine zero statuses; then one status 1 at each position; then one status 2 at each position. The cases expect PASS/exit 0, FAIL/exit 1, and SETUP/exit 2 respectively (`fix.diff:34-57`). This adds four `st` assertions at execution time (97 → 101 cases in the witness).

After the counter freeze, wave-A seat MutateTallyExtra (`.ufo/waves/round-30/wA/MutateTallyExtra.md`) found witness survivors outside the 19 single-leg vectors: two failing legs, two setup legs, setup checked before fail (mixed precedence), an arm that counts status 3 as a pass, and a guard weakened to `>` or removed (the 19 vectors never reach the guard, because the pristine loop always counts nine). The landed runner adds five more selftest cases outside the tally block: the vectors `1 1 0…`, `2 2 0…`, `1 2 0…` and `3 0 0…`, each by exact first line and exit, and a guard stress case that runs the block with the loop's last operand removed and requires `REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)`, exit 2 (101 → 106 cases). The tally block itself is unchanged, byte for byte, from the witness.

The detector runs the extracted tally block, not the nine regression legs. Its expected line and exit checks cover those fixed vectors; they are not evidence that the actual leg commands produce correct statuses. Nor does passing a finite set of rewrites establish that every possible behaviorally equivalent spelling is accepted.

## What S087 does and does not support

S087's library code counts the eight named mutant status buckets, passes them to `toMetrics`, and derives fields including `totalMutants` from the metric counts. In `calculateMetrics.ts`, `totalMutants` is `totalValid + totalInvalid + ignored + pending`; `totalValid`, in turn, is `totalUndetected + totalDetected`. The implementation does not compare that derived value with an independent population count or refuse a mismatch (`.ufo/evidence/round-30/sources/S087-mutation-testing-metrics-3.9.0.tgz:package/src/calculateMetrics.ts:187-198,234-255`; the same line-level source review is recorded in `.ufo/waves/round-30/wA/ReopenS087.md:38-64`).

The model comment for `totalMutants` is shorter than the implementation: it says invalid plus valid and omits `ignored` and `pending` (`package/src/model/metrics.ts:60-62`; `calculateMetrics.ts:253-255`). The library's computed metric is not a rule that any mismatch must be rejected, and its mutant statuses are not the runner's pass/fail/setup buckets. The `nlegs` guard is justified by the runner's own declared case count, not by an S087 policy.

The frozen fix's comment includes an S087 parenthetical (`witness/fix.diff:9-11`). This entry does not repeat that parenthetical as evidence for a required equality or SETUP refusal. The source supports the arithmetic it implements; it does not supply the runner's refusal policy.

## How the C1 ruler evolved

The initial contract freezes C1 and counter v1 at base revision `9ed6db840dc97a0a5f4758b6b5f60cee83a61645` (`contract.json:5-17`). All versions retain the 19-vector harness and the runtime check of nine one-operand-drop mutants. The selftest must pass pristine, kill the selected mutants, and accept the selected behavior-preserving rewrites. A required replacement site that is not found exactly once is a counter error, not a pass (`c1-measure.py:15-33`).

| Version | Frozen change | Evidence |
|---|---|---|
| v1 | 13 fixed family mutants (nine drops plus four arm mutants) and four fixed equivalent rewrites. | `contract.json:14-17`; `c1-measure.py:15-33` |
| v2 | Amendment 1 adds 12 commit-seeded held-out mutants and four held-out equivalent rewrites, with a sanity check that they differ from or match the pristine block under the 19-vector harness. This was added because exact public fixture strings could be recognized without testing the tally. | `contract-amendment-1.json:5-13`; `c1-measure-v2.py:7-11,21-43,289-310` |
| v3 | Amendment 2 adds eight inserted arithmetic-term mutants and four zero-effect equivalent rewrites, seeded from the revision plus one. This followed a control that met v2 without running the tally. | `contract-amendment-2.json:5-13`; `c1-measure-v3.py:7-19,29-55,186-225` |
| v4 | Amendment 3 adds six sealed mutants and six equivalent rewrites tied to the frozen fix's tally-block digest, written by the L1 after the fix was frozen (the attempt-1 seat meant to write them died with no output). It also runs each `--selftest` in a bubblewrap sandbox (S093) with a cleared environment and an isolated copy of `tools/` at the same path for every job, after control K9 met the draft by reading its job label from the working directory name. | `contract-amendment-3.json`; `c1-measure-v4.py` |
| exploratory | Amendment 4: control CtlS2SymEval met v4 with a selftest that models the block in Python and never runs bash. C1 is declared exploratory; no counter is amended. | `contract-amendment-4.json`; `v4/ctl2/CtlS2SymEval-v4.stdout` |

The v4 predicate carries conditions (a)-(i), requires the sealed-file and tally-block digests to match, then requires all six sealed mutants to be rejected and all six equivalent rewrites to pass (`contract-amendment-3.json:16-17`; `c1-measure-v4.py:432-440`). The exact counter command documented by the contract is `python3 .ufo/evidence/round-30/c1-measure-v4.py --repo CLONE --rev REV --sealed SEALED_JSON` (`contract-amendment-3.json:11`). No head measurement is included here.

## What the control receipts show

These are scores of named controls under successive frozen rulers, not a result for the lane head:

- The unchanged K1 control failed v2 (`CtlK1K3-K1.stdout:35-37`). The junk K2 control failed the pristine-selftest and equivalent-rewrite conditions (`CtlK2Junk.stdout:1-2,31-37`). The all-false K3 control returned a counter error, not a pass (`CtlK1K3-K3.stdout:1-3`).
- K4, guard only, refused all nine runtime drop mutants but killed none of the 13 selftest family mutants; it failed the predicate (`CtlK4GuardOnly.stdout:35-37`). K5, keyed on labels, killed 9/13 family mutants and 5/12 held-out mutants; it also failed (`CtlK5Labels.stdout:35-37`).
- K6's hash and verbatim shortcuts failed v2. The hash version accepted 0/4 equivalent rewrites; the verbatim version accepted 2/4 (`CtlK6Bytes-hash.stdout:35-37`; `CtlK6Bytes-verbatim.stdout:35-37`). Both versions also fail frozen v4 (`v4/K6hash.stdout:47-48`; `v4/K6verbatim.stdout:47-48`).
- K7 met v2 (`CtlK7Keyed.stdout:35-37`) but failed its v3 rescore because it killed 0/8 inserted-term mutants (`CtlK7Keyed-v3-rescore-by-L1.stdout:47-49`). K8's static allowlist met v3 in its recorded control run (`CtlK8NoRun.stdout:87-101`) but failed frozen v4 with no tally-block digest match (`v4/K8.stdout:47-48`). K8prime, which retained the fix's guard comments, matched the block but killed only 3/6 sealed mutants and accepted only 1/6 equivalent rewrites (`v4/K8prime.stdout:59-60`).
- K9 passed the v4 draft but failed the frozen v4 ruler; the frozen receipt records 0/13 family kills and 0/6 sealed kills (`contract-amendment-3.json:29`; `v4/K9.stdout:59-60`).
- The pre-data reachability witness is not a control or a lane-head measurement. The v4 receipt for sandbox revision `7165f904` records pristine selftest success, all 19 harness vectors, 9/9 refused drops, 13/13 family kills, 4/4 fixed rewrites, 12/12 held-out kills, 4/4 held-out rewrites, 8/8 inserted-term kills, 4/4 inserted-term rewrites, a matching tally-block digest, and 6/6 plus 6/6 sealed outcomes; it ends `PREDICATE: C1_R30_PASS=true`, `exit=0` (`v4/witness.stdout:59-61`). It establishes reachability in that sandbox only.

## What the static-model control teaches

Each ruler version was met by a cheaper program that knew the ruler's public shape: fixed strings (v1), finite generator spellings (v2, v3), a job label leaking through the working directory (v4 draft). A sealed set committed by hash before scoring (the held-out idea of S094: a test kept from the candidate) defeats allowlists of the public shapes: K8prime matched the block but scored 3/6 and 1/6 on the sealed items. It does not defeat a program that computes the block's meaning by another route. CtlS2SymEval parsed the block into its own model and reproduced every verdict, sealed items included (`v4/ctl2/CtlS2SymEval-v4.stdout`, PASS=true). A counter that scores verdicts cannot tell running the block from modelling it correctly; S094 also warns that a fixed holdout overfits once scores are returned and new candidates are submitted, which is what each round of controls did. "Behavioral" is therefore a property of the selftest's code (it executes the extracted block in bash), checked by reading it, not by the verdict counts.

## Limits

- C1 tests the tally surface under constructed status vectors; it does not replay the actual regression legs or establish that `regression_case_git` returns the right status.
- The guard, markers, operand check, vector lengths, and drop-mutation family assume nine legs. Extending the runner requires reviewing those fixed assumptions together; this entry does not claim general support for a different leg count.
- The counter tests the enumerated fixed, generated, and sealed families and rewrites. It does not establish detection of every possible faulty tally or acceptance of every possible equivalent rewrite.
- The witness and control receipts are sandbox/control artifacts. No lane-head C1 result or full `--regression` replay result is stated here.
- S093's `--unshare-all` is six flags, two of them try-else-skip; the v4 sandbox hides the job label, counter, argv and lane from the selftest (wave-A SentinelBwrap, ProbeSealedReach), but it is not a measured security boundary.
