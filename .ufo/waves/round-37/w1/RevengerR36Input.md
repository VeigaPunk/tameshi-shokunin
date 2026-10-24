# RevengerR36Input — r36 emptied-panel control: object history and reachability (r37 w1, 2026-10-24)

**Verdict: the scratch commit `91373d55557fe26c431e9e3dd9e8fa4a00d7b57f` was never an object of the lane repo — it was created only inside the ephemeral scratch clone `/tmp/tameshi-r36-ctl-2/lane`, which still solely holds it at a detached HEAD. A committed alternative fully resolves the control input: manifest `.ufo/evidence/round-37/control/empty-panel/manifest.json` + adapter `replay-empty-panel.py` + receipts `replay-at-final-control.stdout`/`replay-at-final-fixed.stdout` (all ancestors of lane HEAD `e6185d5f`) reproduce v1 PASS / v2 FAIL on a lane-resolvable zero-specimen panel. No lane writes; all commands read-only (`--no-optional-locks`).**

## Axes

(A) provenance of the emptied-panel control, (B) exact object-database reachability, (C) committed alternatives and their resolution, (D) report fidelity. No tooling installed or updated (system `git` only; pacman untouched per bounds). Leaf seat: no subagents.

## 1. Object history (axis A)

1. Source panel: `.ufo/evidence/round-35/c1/panel`, tree `4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e`, 9 JSON specimens. Verified: `git rev-parse d9c496b19371b779ce0eec6dfee1b049b27a3a2d:.ufo/evidence/round-35/c1/panel` → `4f3d8af5…`; identical at `b455001e2589b3…`; `git ls-tree -r` lists exactly the 9 specimens later named in the r37 manifest.
2. Creation of the mutant: commit `91373d55557fe26c431e9e3dd9e8fa4a00d7b57f`, subject `MUTANT (scratch control): empty public panel`, parent `b455001e2589b3f4f471d94a3de7e5e549b9f54c`, authored `2026-10-24 03:18:18 -0300`, deleting exactly the 9 panel JSONs (9 files, 135 deletions, no other path). Observed in the surviving clone:
   `git -C /tmp/tameshi-r36-ctl-2/lane --no-optional-locks show --stat --format=… 91373d55` (full output captured; `cat-file -t` there → `commit`; `rev-parse HEAD` there → `91373d55…`).
3. The clone is a scratch checkout of the lane: `branch -a` shows `HEAD detached from b455001`, `master`, `remotes/origin/{master,hyaku/s3-tameshi-r25-author,hyaku/s3-ready66-tameshi}` — the mutant sits on **no branch anywhere**, not even in the clone; it is held only by that clone's detached HEAD + reflog. The r36 receipts were produced against it: `control/v1-at-emptypanel.stdout:8` and `control/v2-at-emptypanel.stdout:8` both embed `rev=91373d55557fe26c431e9e3dd9e8fa4a00d7b57f` (v1 `C1_R35_PASS=true`, v2 `C1_R36V2_PASS=false`); r36 reviewer traced the invocation at `history://L1-tameshi-r36` transcript line 400 (`--lane /tmp/tameshi-r36-ctl-2/lane --rev 91373d5…`) — `.ufo/waves/round-36/w1/ReviewC2Claim.md:113,141-142,188-190`.
4. The commit was never pushed, fetched, or bundled into the lane. Timeline: mutant 03:18:18 → committed receipts at r36 tip `d9c496b` (receipts cite the scratch rev as-is) → r37 repair chain `c2b08d7` 03:55:32 → `7500239` 04:18:55 → `32826f3` (all ancestors of HEAD `e6185d5f0b63a6963205110cb098f2f1eca27622`).

## 2. Why it is unreachable (axis B) — absent, not merely dangling

Precision on the frozen wording "unreachable": the object is **entirely absent from the lane object database**; it never entered it, so no ref/reflog/pack/loose trace exists. Evidence (all in lane, exit codes observed):

- `git --no-optional-locks cat-file -t 91373d55557fe26c431e9e3dd9e8fa4a00d7b57f` → `fatal: git cat-file: could not get object info`, exit 128.
- `git log --all --oneline -1 91373d55…` → `fatal: bad object 91373d55557fe26c431e9e3dd9e8fa4a00d7b57f`.
- `git reflog --all | grep -c 91373d5` → `0`; `git show-ref | grep -c 91373d5` → `0` (covers `refs/jj/keep/*` too — jj keeps no trace); `git fsck --unreachable --no-progress | grep -c 91373d5` → `0` (not even a dangling copy).

Cause chain: the commit was made inside the scratch clone at a detached HEAD (step A2/A3) and never transferred; the receipts were then committed to the lane citing a rev the lane cannot resolve — the exact r36 defect class (dead pointer) recorded at `.ufo/waves/round-36/w1/SimplifierReceiptDupes.md:39-41` (C6) and `.ufo/waves/round-36/w1/ReviewC2Claim.md` LOW-3.

Sole surviving holder: `/tmp/tameshi-r36-ctl-2/lane` (verified present and resolving today). This is ephemeral: r36 w2 already found it absent under `/fast/scratch/hyaku` (`.ufo/waves/round-36/w2/W2CriticReport.md:17`), and w1 flagged the `/tmp` cleanup risk (`ReviewC2Claim.md` residual risks). The lane record therefore cannot depend on it — and no longer does.

## 3. Committed alternative — resolves the input without the scratch commit (axis C)

Append-only supersession chain, all ancestors of lane HEAD:

- `c2b08d70427921998677c780930c448a4ecefcf1` "round-37: freeze claims and empty-panel input" added:
  - `.ufo/evidence/round-37/control/empty-panel/manifest.json` (schema `tameshi-empty-panel-v1`): `source_revision=d9c496b…`, `source_panel_tree=4f3d8af5…`, the 9 named specimens, `mutation` = "Remove all nine JSON specimen files … retain only this manifest", `expected_specimen_count=0`, and `prior_unreachable_mutant_revision=91373d55…` (manifest.json:20). Tree identity re-verified: `git rev-parse d9c496b:.ufo/evidence/round-35/c1/panel` = `4f3d8af5…` — the spec pins the exact pre-mutation content and states the deterministic mutation, so the emptied panel is reconstructible from lane objects alone.
  - `.ufo/evidence/round-37/control/replay-empty-panel.py`: redirects only the public-panel path to the committed empty panel; counter/runner/sealed/tool read from committed objects at `--rev`; `--tool` pins `6188db16…` so receipts print `mode=control`; aborts on manifest/tree mismatch (`replay-empty-panel.py:14-16,47-73`).
- `7397981` "label mutant counter runs as controls" (adapter/counter edits, `mode=control` labeling — closes r36 LOW-1); `65b799d` separated counter rev from panel rev; `21b96a2` aligned the counter's receipt checks.
- `7500239ebadfe7a7e627167fa4a81789f8614207` "supersede unreachable r36 control input" committed `control/replay-at-final-fixed.{stdout,exit,stderr}` + the SCORECARD erratum; `32826f3` committed the explicit `mode=control` receipt set `control/replay-at-final-control.*`.
- Committed receipt `control/replay-at-final-control.stdout` (exit 0, `replay-at-final-control.exit` = `0`): `source_tree=4f3d8af5… source_specimens=9 empty_specimens=0 counter_rev=d9c496b… panel_rev=c2b08d7… v1_pass=1 v2_reject=1 EMPTY_PANEL_REPLAY_PASS=true`, with `C1_R35_CONTROL: mode=control … pub_slots=0 … C1_R35_CONTROL_PASS=true` and `C1_R36V2_CONTROL: mode=control … C1_R36V2_CONTROL_PASS=false` — both counter revs lane-resolvable (`d9c496b`), panel rev an ancestor of HEAD. The earlier `replay-at-final-fixed.stdout` shows the same verdicts with `mode=deciding` labels (pre-`7397981` adapter); the r37 counter checks `mode=control`, satisfied by the `-control` receipt.
- Counter encoding the resolution: `.ufo/evidence/round-37/calibration/measure.py:8-11` (`OLD_MUTANT`, `ERRATUM_MARKER`, `MANIFEST`, `REPLAY_RECEIPT=replay-at-final-control.stdout`), `:66-73` — mismatch=0 iff `cat-file -e 91373d55^{commit}` fails AND the SCORECARD erratum marker is present AND manifest checks pass AND both control receipts verify (label, `pub_kill=0/0`/`pub_slots=0`, `mode=control`, `EMPTY_PANEL_REPLAY_PASS=true`, `counter_rev==manifest source_rev`, `panel_rev` ancestor of `rev`).
- Record side: `LOG.md:1962-1968` (before PASS=false at `d9c496b` → after PASS=true at `32826f37`, naming manifest + receipt) and `SCORECARD.md:1780` (erratum clause: r36 stdout files remain historical, `rev=91373d55…` "is not an object in this lane", superseded by the committed tree/spec and replay).

**Answer: yes — the committed empty-panel specification plus both replay receipts resolve the r36 control input entirely from lane objects; the scratch commit itself is unrecoverable from the lane by design of the original run and is deliberately not needed.**

## 4. Residual observations (no repair taken; report-only)

- The only copy of `91373d55` lives in `/tmp/tameshi-r36-ctl-2/lane` at a detached HEAD. Its eventual loss changes nothing for C1 (the supersession is committed), but any future audit wanting the *original* mutant bytes must do it soon; the committed manifest+adapter path is the durable equivalent.
- `control/v1-at-emptypanel.stdout` / `v2-at-emptypanel.stdout` retain `rev=91373d55…` and `mode=deciding` verbatim — correct append-only behavior; the SCORECARD erratum at `SCORECARD.md:1780` is the clause that re-keys them to the committed input. No committed assertion still treats `91373d55…` as a lane object (grep over LOG/SCORECARD/contract/manifest: all mentions are either historical-quote, `prior_unreachable_mutant_revision`, or the counter's own absence check).

## Commands (all read-only; lane untouched except this report)

```
git --no-optional-locks cat-file -t 91373d55557fe26c431e9e3dd9e8fa4a00d7b57f   # exit 128
git --no-optional-locks log --all --oneline -1 91373d55557fe26c431e9e3dd9e8fa4a00d7b57f  # fatal: bad object
git --no-optional-locks reflog --all | grep -c 91373d5                          # 0
git --no-optional-locks show-ref | grep -c 91373d5                              # 0
git --no-optional-locks fsck --unreachable --no-progress | grep -c 91373d5      # 0
git --no-optional-locks rev-parse '4f3d8af5…^{tree}' d9c496b:.ufo/evidence/round-35/c1/panel b455001e:.ufo/evidence/round-35/c1/panel  # 4f3d8af5… ×3
git --no-optional-locks show --stat 7500239 / c2b08d7 / 32826f3 / 7397981
git --no-optional-locks ls-tree --name-only HEAD:.ufo/evidence/round-37/control/
git -C /tmp/tameshi-r36-ctl-2/lane --no-optional-locks cat-file -t 91373d55…    # commit
git -C /tmp/tameshi-r36-ctl-2/lane --no-optional-locks show --stat 91373d55     # 9 files, 135 deletions, parent b455001e
git -C /tmp/tameshi-r36-ctl-2/lane --no-optional-locks branch -a; rev-parse HEAD  # detached, no branch holds it
```
