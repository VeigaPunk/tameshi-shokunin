# T58W1Panel09 — blind panel

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`.
Axes: status accuracy, concrete evidence, blind independence, zero lane mutation.

## Verdicts

| Item | Verdict | Resolving ancestor |
|---|---|---|
| R55.4 | open | — |
| R55.5 | fixed | `c0137451f5b7f22d65f748fc69f1b181f55e1378` |
| R55.6 | fixed | `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1` |
| R55.7 | open | — |
| R56.1 | open | — |

## Commands and evidence

All lane judgments used an isolated shared clone, detached at the base. Setup commands:

```sh
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r58/T58W1Panel09
mkdir -p "$S"
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/clone"
test "$(git -C "$S/clone" rev-parse --show-toplevel)" = "$S/clone"
git -C "$S/clone" checkout --detach 2a32aa8228d5f86a85c81a923a3148bf792a9538
```

Observed: clone succeeded; `HEAD is now at 2a32aa82 round-57 verifier spot-check (integrator, hyaku): non-author admit/reject`.

The accompanying `T58W1Panel09-receipts/` files retain exact executed `git -C <absolute-clone> show <base>:<path>` commands, numbered excerpts and exit codes, plus commit/ancestry commands. Excerpt selection is explicitly stated alongside every command. These are static inspection receipts, not newly executed runtime tests.

### R55.4 — open

`read /home/vgpnk/Projects/shokunin/.ufo/reports/round-55/tameshi.md:90-94` returned:

> completed part of the phase-A set, `CTL_SKIP_c2` was still running at filing
> (`.ufo/evidence/round-55/control/controls-a.stdout`). No phase-B set exists.

Base `git show` of `.ufo/evidence/round-55/control/controls-a.stdout` returns `CTL CTL_SKIP_c2 ... total=4 C2_R55_PASS=false` and `CONTROLS_A: 5/5 as pre-registered` (receipt `R55.4.txt`, exit 0). Base lesson `corpus/lessons/round-56.md:105` claims “FIXED by construction” for the next round but still describes the prior report as claiming it was running. A future construction rule does not correct the false historical sentence. The fleet report read is supplementary current evidence, not represented as a file contained in the lane base.

### R55.5 — fixed

`R55.5.txt` captures canonical deciding logic at `.ufo/evidence/round-56/deciding-run.sh:114-127`: controls are extracted from committed REV, passed through `receipt-revision-gate.py --certified "$REV"`, and nonzero gate exit causes `DECIDING_REFUSED receipt-binding`. `tools/receipt-revision-gate.py:125-160` checks absent/unresolvable revisions, positive/verdict content identity, and control ancestry. Control role deliberately permits ancestor revisions; it is not an exact-sha claim for synthetic negative controls.

The requested QUALITY routing is present at `corpus/QUALITY.md:1616-1657`: Criterion 107 names the gate and refusal codes and includes the R55.5 lesson pointer. `R55.5-history.txt` retains `git show --format=fuller --unified=2 c0137451f5b7f22d65f748fc69f1b181f55e1378 -- corpus/QUALITY.md`, showing those exact paragraphs introduced by that commit. The gate itself was introduced earlier at `c3e2ca9f020776b3d66c7af854fb82c834674fcf`. `git merge-base --is-ancestor c0137451f5b7f22d65f748fc69f1b181f55e1378 <base>` exits 0. Thus the named resolving commit completes the item’s requested criterion plus lesson routing, rather than merely adding a tool.

### R55.6 — fixed

`R55.6-history.txt` retains `git show --format=fuller --stat 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`: message explicitly names inherited round-55 monitor dumps and R55.6, and the stat includes all seven named files. `git ls-tree -r <base> -- <seven exact paths>` returns seven `100644 blob` entries:

- coldread-HEAD.json: `e35494fce18eb4f99276234f75a411f2fa229503`
- coldread-at-base.json: `fc6d017c8707d9e02b1460365fb8b11d8af642dc`
- base.json: `0e97f1949edef587bd7758c65912d727552c74e9`
- cand.json: `1a3abc2b6794536596437a7ea9a3fcae9b5559d1`
- floor.json: `fc6d017c8707d9e02b1460365fb8b11d8af642dc`
- rekey.json: `4c3f14c1ca5b015def4043b381ed5029c538b543`
- inputs.json: `41fbb439aeafa93da0d32cb34e2df0feaea3c86a`

Both commands exit 0; ancestry check for the resolving commit exits 0. `R55.6.txt` also records the base lesson’s exact inherited-file disposition. This closes the seven-file defect; it does not claim that every later round avoids dirty evidence.

### R55.7 — open

`R55.7.txt` captures `corpus/lessons/round-56.md:59-73,108` at base. Exact located text:

> Residual, not closed: the lane cannot fence a closure harness’s own seats;
> the receipt is the spotcheck’s list plus the base commits.

The restoration and scratch-clone policy partially dispose of lane effects, but do not close the stated harness contamination problem. The recorded disposition explicitly calls it residual, not a reasoned decline; therefore neither fixed nor declined is supported.

### R56.1 — open

`R56.1.txt` captures base `SKILL.md:888-897,818-820`. Line 892 still cites `SKILL.md:819-820` for a porcelain-clean precondition. Actual lines 819-820 instead read:

> three holes demonstrably open; whether they stay open is the live test of
> the "add a case" repair.

This is a direct counterexample to completed conversion to heading/function anchors; no inference from a grep count is required.

## Verification gaps and discipline

- LSP unavailable: `read xd://lsp` returned `No such tool: xd://lsp`. Used textual inspection and Git history, not semantic-reference claims.
- No runtime, test, lint, or build was executed; this assignment judges historical tree status. No universal runtime, resume, or saturation claim was made.
- A broad filename-only glob accidentally enumerated round-57 wave filenames; no round-57 wave file content or panel judgment was opened/read. Historical discovery once used `git log --all`; final evidence is explicitly pinned to base and forbidden wave paths were excluded from the content-search history command.
- No lane content was edited or staged; only this seat’s report, JSON and receipts were written. No tools installed or updated.
- Cleanup command `rm -rf -- /fast/scratch/hyaku/tameshi-r58/T58W1Panel09 && test ! -e /fast/scratch/hyaku/tameshi-r58/T58W1Panel09 && echo SCRATCH_REMOVED` returned `SCRATCH_REMOVED`, exit 0. Scratch deleted before yield.

Self-evaluation: accuracy 4/5 (static review, no runtime claims); completeness 5/5 (all five assigned items); clarity 4/5 (historical report is fleet-external, explicitly distinguished); actionability 5/5 (per-item receipts and resolving hashes); conciseness 4/5 (evidence detail retained for reproducibility). Overall 4.4/5. Highest-impact improvement would be an independently archived base-time fleet-report snapshot; the present report does not mislabel the current fleet file as lane-base content.
