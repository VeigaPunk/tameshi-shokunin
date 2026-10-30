# T58W1RevFixOld — fixed-at-base review

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`.
Axes: calibration, evidence fidelity, scope preservation. Recommendations only; no admission or integration.

## Finding — medium: R55.2 remains open

`corpus/lessons/round-57.md:19-26` rebuts a different report from the routed item. It says the verifier quoted the **scribe report** incorrectly, pointing to `T55W1ScribeSkill.md`. The routed defect concerns the **round report's quotation of that seat run**, not a false statement by the seat itself.

The actual receipt at `.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/c2-integrated.out:44` reads:

```text
C2_R55: rev=08d64e946006 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
```

The seat correctly quotes that result at lines 146-148. This does not refute the routed defect. Supplementary direct read of the current fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-55/tameshi.md:88` finds `grammar=9/9 … note=9/9 skill=1/1 total=0` attributed to the `T55W1ScribeSkill` run. That current external file is not asserted to be an artifact of the lane base.

`ca75c2674645ab6bdadeecb8584007c74342bfa9` originally added an explicit, correctly targeted superseding receipt correction. But `adf87899c70d616140a81185a8f9acbbdfb30392` removed it and replaced it with the wrong-report rebuttal now present at base. Do not cite the removed correction as an enduring fixed-at-base resolution. The current text does retain the right numeric result; the defect is its incorrect referent and denial of the original report's mistake. Restore a superseder explicitly correcting the fleet round report, not the honest seat report.

Commands and full output: `T58W1RevFixOld-receipts/r55-regression.txt`, including `git -C /fast/scratch/hyaku/tameshi-r58/T58W1RevFixOld/clone show adf87899c70d616140a81185a8f9acbbdfb30392 -- corpus/lessons/round-57.md` (exit 0), plus the direct fleet-report read. `underlying.txt` preserves base-tree blame output for the actual receipt and honest seat quotation.

## Fixed-at-base recommendations

### R54.7 — fixed

Resolving commit: `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

`SCORECARD.md:2674-2678` explicitly corrects the deletion claim:

> Corrected: the file was **renamed** into `.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json` at `7fa9a5e` (`R100`); it still sits in the tree as the incident receipt.

The same paragraph says its reader path and `section_sha256` cannot credit. `git ... blame -l -L 2673,2678 BASE -- SCORECARD.md` attributes every line to the resolving commit. `git ... diff-tree --no-commit-id --name-status -r -M 7fa9a5e -- OLD_PATH NEW_PATH` independently inspects the rename. Exact commands/output are in `history.txt`; `route-comparison.txt` records that the corrective excerpt was absent at routed revision `650987a0d6fc285b37f0f9e63a3aae864af9cd5a`.

### R54.9 — fixed

Resolving commit: `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

`SCORECARD.md:2694-2696`:

> Corrected: `reviewers=5 attack=21/76 seats=76` (27.6 %) from `.ufo/waves/round-54/w1-registry.json`, and `staged=81` staged `.md` files under `merge/tameshi/knowledge`.

`git ... blame -l -L 2692,2696 BASE -- SCORECARD.md` assigns the excerpt to the resolving commit. Independent `git ... show BASE:.ufo/waves/round-54/w1-registry.json` projection returns `seats=76`, `attack_seats=21`, reviewer 5, and role mix {connector:2, critic:4, executor:13, mutation-tester:12, revenger:3, reviewer:5, scout:4, scribe:27, sentinel:4, simplifier:2}. Arithmetic yields 27.6%. `corpus/lessons/round-54.md:51` also now says **other 80**, consistent with an 81-entry package after the separately named candidate. The package total is supported by the committed correction, not a fresh external-package census. Commands/output: `history.txt`, `underlying.txt`, `route-comparison.txt`.

### R56.2 — fixed, both clauses

Complete resolving commit: `870d9b987f14a046964018429662a238f2fe9e20` (counter); prerequisite documentation fix: `ca75c2674645ab6bdadeecb8584007c74342bfa9`.

`SKILL.md:53` now carries `RECEIPT_REV_CONTENT_DRIFT` in the final code cell, explicitly reserving `RECEIPT_REV_MISMATCH` for no `--paths`.

The canonical replacement docs arm is `.ufo/evidence/round-57/c2/measure.py`: `standing_cell` (206-223) extracts the final cell of the verdict-receipt row; `build_cell_fixture` (298-331) creates two revisions with a changed declared surface and runs the gate with `--paths` and receipt role `verdict`; lines 438-458 require exit 3, exactly one emitted code, and `set(carried) == emitted`. A merely present but wrong code fails. This is code-to-role truth, not the old whole-section code-presence test. The original round-56 frozen counter was intentionally not rewritten.

`git ... log --format='%H %s' -- .ufo/evidence/round-57/c2/measure.py` identifies `870d9b98` as the introducing commit; base blame preserves the exact implementation. Commands/output: `history.txt` and `underlying.txt`. No live counter pass is claimed.

## Evidence and limits

All review work used a shared scratch clone checked out detached at base; `rev-parse HEAD` returned the exact base. `git merge-base --is-ancestor COMMIT BASE` exited 0 for both fixed-at-base resolving commits, the documentation prerequisite, and the R55.2 replacement commit. Full commands, outputs and exit codes are in receipts. Route comparison shows each proposed keyed excerpt absent from its path at the item's routed revision. JSON has only the four assigned verdicts.

LSP unavailable: reading `xd://lsp` returned **No such tool**. Searches were literal fallback, not semantic reference evidence. No build, counter, selftest, runtime admission or saturation check was run or claimed. No lane content was changed; no staged change is proposed by this reviewer. No prior-round evidence was modified. No tools installed or updated.

Scratch cleanup executed: `rm -rf -- /fast/scratch/hyaku/tameshi-r58/T58W1RevFixOld && test ! -e /fast/scratch/hyaku/tameshi-r58/T58W1RevFixOld`, exit 0; output `SCRATCH_REMOVED=/fast/scratch/hyaku/tameshi-r58/T58W1RevFixOld`.

Self-evaluation: accuracy 4 (R56.2 source review, not live execution); completeness 4 (external package census not repeated); clarity 4 (R55.2 requires distinguishing two reports); actionability 5 (exact correction and commits named); conciseness 4 (receipt pointers carry detail). Overall 4.2. Highest-impact improvement for integration: explicitly correct the fleet-report referent for R55.2; retain source-review/live-execution distinction for R56.2. The user should agree with these scoped limitations.
