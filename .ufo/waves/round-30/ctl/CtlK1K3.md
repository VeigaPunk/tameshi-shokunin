CONTROL CtlK1K3-K1: meets=false C1_R30_PASS=false
CONTROL CtlK1K3-K3: meets=false C1_R30_PASS=false

## Frozen-counter results

K1, unchanged lane tip `e59728df5ebb053c9810049c05fd4e9d59d82dee`:

```text
C1_R30: rev=e59728df5ebb053c9810049c05fd4e9d59d82dee pristine_selftest=1 harness=19/19 refused_drops=0/9 killed=0/13 equiv_pass=4/4 heldout_killed=0/12 heldout_equiv=4/4
PREDICATE: C1_R30_PASS=false
exit=1
```

K3, sandbox control commit `d103739302942d5f166b613cd69ae9657cf15a63`:

```text
C1_R30: counter error: held-out mutant H01-drop is harness-equivalent to pristine
PREDICATE: C1_R30_PASS=false
exit=2
```

The K3 error is the counter's generator-sanity refusal, not a timeout, missing replacement site, successful mutation kill, or passing measurement. The frozen command emits no numeric metric summary for K3 because it stops before the selftest jobs. Both captured stderr streams were empty. Elapsed times: K1 57.493 s; K3 0.138 s.

## Axes, controls, and diffs

Claim axis: **operability**. Probe axes: unchanged-work rejection, refusal-versus-correctness discrimination, behavioral detector sensitivity, and exact-byte restoration. These are control probes, not additional round claims or an admission judgment.

- **K1 / do-nothing:** no source change and no synthetic empty commit; the measured revision is exactly the dispatched lane tip. Its diff artifact is empty.
- **K3 / all-false:** only two lines inserted immediately after `run_regression`'s tally declaration in `tools/mutate-and-run.sh`:

  ```bash
  printf 'REGRESSION: SETUP (all-false control)\n'
  exit 2
  ```

  This bypasses the complete tally decision, including FAIL and PASS. Every fixed-status vector returns SETUP/2. All frozen replacement anchors remain untouched. Diff summary: one file, two insertions, zero deletions; no selftest change.

## Clauses (a)–(g)

K1 fails **(c), (d), (f)**. K3 fails **(b), (d), (f)** in the supplemental clause observations below; its official frozen-counter result remains the exit-2 error above.

| Clause | Required | K1, frozen result | K3, supplemental observation |
|---|---|---|---|
| (a) pristine selftest | exit 0 and `VERDICT: PASS` | satisfied | satisfied |
| (b) correct tally outcomes | 19/19 | satisfied: 19/19 | **fails: 9/19** |
| (c) refuse dropped operands | 9/9 | **fails: 0/9** | satisfied: 9/9 |
| (d) family mutant detection | 13/13 | **fails: 0/13** | **fails: 0/13** |
| (e) frozen equivalent acceptance | 4/4 | satisfied: 4/4 | satisfied: 4/4 |
| (f) held-out mutant detection | 12/12 | **fails: 0/12** | **fails: 0/12** |
| (g) held-out equivalent acceptance | 4/4 | satisfied: 4/4 | satisfied: 4/4 |

Because K3's official run aborts before clause results are printed, these additional observations were obtained separately, without modifying the frozen counter: import its unchanged module; obtain the committed K3 runner and tools through sandbox `git show`/`git archive`; use the counter's `harness`, `replace_once`, `equivalents`, `apply`, `heldout(seed=int(REV,16))`, and `selftest` helpers on the same vectors and generated jobs. This supplemental probe does **not** replace the official command or waive its generator-sanity error.

Actual supplemental output:

```text
SUPPLEMENTAL_C1_R30: rev=d103739302942d5f166b613cd69ae9657cf15a63 pristine_selftest=1 harness=9/19 refused_drops=9/9 killed=0/13 equiv_pass=4/4 heldout_killed=0/12 heldout_equiv=4/4
SUPPLEMENTAL_HARNESS: vectors=19 observed=[(2, 'REGRESSION: SETUP (all-false control)\n')]
```

All 34 supplemental selftest rows (pristine + 13 family mutants + 4 frozen equivalents + 12 held-out mutants + 4 held-out equivalents) returned `selftest_exit=0 verdict_pass=1`. The nine status-2 vectors account for K3's 9/19 harness matches; all-zero and all nine single-status-1 vectors have the wrong result.

## Expected detector and interpretation

The behavioral detector is the runner's own `bash tools/mutate-and-run.sh --selftest`, invoked by the frozen `selftest` helper with its 300-second bound. A tally-sensitive detector should reject the all-false change while accepting the original bytes.

Observed pristine / K3 / restored selftest results were **exit 0 + PASS / exit 0 + PASS / exit 0 + PASS**. Thus K3 **survived the runner's own detector**, a coverage finding. Neither control meets C1. The frozen counter rejects do-nothing through clauses (c)/(d)/(f), and rejects all-false through generator sanity; independently, clause (b) distinguishes blanket refusal from correct tally behavior. Clause (c) alone is satisfied trivially by blanket refusal and must not be mistaken for the complete predicate.

The aggregate frozen-counter baseline was already false. Its sequence was false/exit 1 → false/exit 2 → false/exit 1, so **no killed-mutant claim is made from that failing baseline**; aggregate kill attribution is inconclusive. No counter or contract change is proposed or applied.

## Commands and artifacts

Each official score used the frozen executable unchanged, default jobs=6, clean Git environment, an isolated sandbox TMPDIR, and this bounded command shape:

```bash
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  TMPDIR="$TMP" timeout --kill-after=10 900 python3 \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v2.py \
  --repo "$CLONE" --rev "$REV"
```

| Run | CLONE | REV |
|---|---|---|
| K1 pristine | `/fast/scratch/hyaku/tameshi-r30/ctl/CtlK1K3/K1-clone` | `e59728df5ebb053c9810049c05fd4e9d59d82dee` |
| K3 mutated | `/fast/scratch/hyaku/tameshi-r30/ctl/CtlK1K3/K3-clone` | `d103739302942d5f166b613cd69ae9657cf15a63` |
| K3 restored | `/fast/scratch/hyaku/tameshi-r30/ctl/CtlK1K3/K3-clone` | `e59728df5ebb053c9810049c05fd4e9d59d82dee` |

Lane-relative evidence, containing the complete official stdout and final `exit=<n>` line:

- `.ufo/evidence/round-30/ctl/CtlK1K3-K1.stdout`
- `.ufo/evidence/round-30/ctl/CtlK1K3-K3.stdout`
- `.ufo/evidence/round-30/ctl/CtlK1K3-K1.diff` — empty
- `.ufo/evidence/round-30/ctl/CtlK1K3-K3.diff` — sandbox `git diff HEAD~1 HEAD -- tools/mutate-and-run.sh`

Additional complete observations remain in the assigned sandbox:

- `/fast/scratch/hyaku/tameshi-r30/ctl/CtlK1K3/K3-supplemental.stdout`
- `/fast/scratch/hyaku/tameshi-r30/ctl/CtlK1K3/restored-counter.stdout`

## Restoration and containment evidence

`timeout 20 sha256sum` recorded these runner hashes:

| Bytes | SHA-256 |
|---|---|
| K1 before and after, unchanged | `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |
| K3 before mutation | `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |
| K3 committed mutation | `85a1ff7721aa593d2b991f8c1510ebb33fec344e3e093766f7210ae8d4968aab` |
| K3 restored worktree | `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |

K3 restoration deleted exactly the two inserted lines. The mutant commit is retained for reproduction; its worktree is intentionally restored to the original runner bytes. The same frozen counter was then run at the original revision in the K3 clone, with this actual result (61.416 s):

```text
C1_R30: rev=e59728df5ebb053c9810049c05fd4e9d59d82dee pristine_selftest=1 harness=19/19 refused_drops=0/9 killed=0/13 equiv_pass=4/4 heldout_killed=0/12 heldout_equiv=4/4
PREDICATE: C1_R30_PASS=false
exit=1
```

The frozen counter's SHA-256 before and after scoring remained `5ed4e663ff16556d0bfef68a9fc1e3cf820ab8bc2b620169e800da914f0c8719`, matching the amendment. No production file, contract, lane Git index, sibling clone, or runtime routing was modified. All Git writes occurred only in the assigned sandbox with the three Git override variables removed.

Final owned-process sweep checked `/proc/<pid>/cwd` against the assigned sandbox prefix and returned:

```text
PROCESS_CLEANUP: own_sandbox_cwd_matches=[] terminated=[]
TEMP_DIRECTORY_CLEANUP: exit=0
```

All launched commands finished; no background job was used. Counter/audit temporary trees were removed, and the empty per-control TMPDIRs were removed. No tools were installed or updated.
