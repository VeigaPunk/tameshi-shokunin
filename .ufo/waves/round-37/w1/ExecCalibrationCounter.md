# ExecCalibrationCounter — r37 C1 mismatch counter at the r36 base and the candidate final revision

seat: executor (leaf) · round 37 w1 · lane: `tameshi-shokunin` · date: 2026-10-24
scope: run `.ufo/evidence/round-37/calibration/measure.py` at the frozen r36 base and the
candidate final revision, re-derive its result from the cited scorecard, manifest and
receipts, and do not alter the predicate.

Observed lane base: `e6185d5f0b63a6963205110cb098f2f1eca27622` (detached HEAD, master).
Frozen r36 base: `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` (ancestor of the final, 11 commits
between). Counter bytes under test: sha256 `9a1823fc6e5b4aaa8b8bfe88e7643e9565d48be9265074b1ca3b964800eaa765`,
equal to `git show 32826f3:.ufo/evidence/round-37/calibration/measure.py | sha256sum` and equal
to the working file (`git diff HEAD -- …/measure.py` empty), so the same counter is used on
both sides of the comparison.

## Result — MISMATCH COUNT 1 → 0

All runs below used the committed counter file unmodified. The lane checkout was read with
`--lane` only (git plumbing reads: `show`, `rev-parse`, `cat-file`, `merge-base`,
`ls-tree`); the deciding runs also executed from an isolated clone at
`/fast/scratch/r37-cal/lane` (`git clone --no-hardlinks`), so no git index, `.git` or
`.ufo/state` entry of the lane was written.

```
$ cd /fast/scratch/r37-cal/lane
$ python3 .ufo/evidence/round-37/calibration/measure.py --lane /fast/scratch/r37-cal/lane \
    --rev d9c496b19371b779ce0eec6dfee1b049b27a3a2d
C1_R37: unresolved_control_inputs=1 old_mutant_resolves=0 correction=0 manifest_ok=0 receipts_ok=0 rev=d9c496b19371b779ce0eec6dfee1b049b27a3a2d C1_R37_PASS=false
exit=1

$ python3 .ufo/evidence/round-37/calibration/measure.py --lane /fast/scratch/r37-cal/lane \
    --rev e6185d5f0b63a6963205110cb098f2f1eca27622
C1_R37: unresolved_control_inputs=0 old_mutant_resolves=0 correction=1 manifest_ok=1 receipts_ok=1 rev=e6185d5f0b63a6963205110cb098f2f1eca27622 C1_R37_PASS=true
exit=0
```

Repeated against the live lane object database (read-only, same counter bytes) — identical
numbers, so the clone's object pruning is not supplying the result:

```
$ python3 /fast/scratch/r37-cal/lane/.ufo/evidence/round-37/calibration/measure.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev d9c496b19371b779ce0eec6dfee1b049b27a3a2d
C1_R37: unresolved_control_inputs=1 ... C1_R37_PASS=false                 (exit 1)
$ ... --rev e6185d5f0b63a6963205110cb098f2f1eca27622
C1_R37: unresolved_control_inputs=0 ... C1_R37_PASS=true                  (exit 0)
```

Intermediate revisions bracket the flip:

```
c2b08d7  unresolved_control_inputs=1  correction=0 manifest_ok=1 receipts_ok=0   (manifest only)
32826f3  unresolved_control_inputs=0  correction=1 manifest_ok=1 receipts_ok=1   (scorecard-recorded)
e6185d5  unresolved_control_inputs=0  correction=1 manifest_ok=1 receipts_ok=1   (candidate final)
```

## Independent re-derivation (predicate unchanged)

A separate scratch script (`/fast/scratch/r37-cal/rederive.py`) recomputes each sub-condition
from the committed artifacts, without importing the counter. Per revision:

| rev | erratum marker | manifest / source tree | empty-panel paths | receipts (v1 PASS / v2 FAIL, mode, revs) | old mutant | unresolved |
|---|---|---|---|---|---|---|
| `d9c496b` | 0 | absent | `[]` | absent | unresolvable | 1 |
| `c2b08d7` | 0 | present, tree `4f3d8af…` ok, 9/0 | `[…/manifest.json]` | absent | unresolvable | 1 |
| `32826f3` | 1 | present, tree ok, 9/0 | `[…/manifest.json]` | v1 ok / v2 ok, `panel_rev=c2b08d7`, `counter_rev=d9c496b` | unresolvable | 0 |
| `e6185d5` | 1 | present, tree ok, 9/0 | `[…/manifest.json]` | v1 ok / v2 ok, `panel_rev=c2b08d7`, `counter_rev=d9c496b` | unresolvable | 0 |

Direct checks behind that table:

- Marker: `SCORECARD.md:1778` at `e6185d5` = `### Round 36 control-input erratum (round 37)`;
  `grep -c` at `d9c496b` = 0.
- Old input: `git -C <lane> cat-file -e 91373d55557fe26c431e9e3dd9e8fa4a00d7b57f^{commit}` →
  `fatal: Not a valid object name`, exit 128 at the live lane (not merely in the clone).
- Manifest: `.ufo/evidence/round-37/control/empty-panel/manifest.json` names source revision
  `d9c496b…`, path `.ufo/evidence/round-35/c1/panel`, tree `4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e`
  (re-resolved: equal; the source panel holds 9 specimens), counts 9/0.
- Empty panel: `git ls-tree -r --name-only e6185d5 -- .ufo/evidence/round-37/control/empty-panel`
  returns exactly `…/empty-panel/manifest.json`; at `d9c496b` the whole
  `.ufo/evidence/round-37` subtree has 0 files.
- Receipt `.ufo/evidence/round-37/control/replay-at-final-control.stdout:9,18,19`: both counter
  lines carry `mode=control`, `rev=d9c496b…`, `pub_kill=0/0 pub_accept=0/0 pub_slots=0
  pub_distinct=0`, with `C1_R35_CONTROL_PASS=true` / `C1_R36V2_CONTROL_PASS=false`; the
  aggregate line carries `counter_rev=d9c496b…`, `panel_rev=c2b08d70427921998677c780930c448a4ecefcf1`
  (resolvable commit, ancestor of `e6185d5`) and `EMPTY_PANEL_REPLAY_PASS=true`.
- Independent replay: ran the committed wrapper
  `.ufo/evidence/round-37/control/replay-empty-panel.py --lane . --rev d9c496b… --panel-rev c2b08d7…
  --work-root /fast/scratch/r37-cal/replay-work` in the clone. Its stdout sha256 is
  `8468af55fd66afb83d0b191f7a56b6b06c21273fb4a5982c85ff1136068ca57b` — **byte-identical** to the
  committed receipt (`diff` clean, 19 lines), including `v1_pass=1 v2_reject=1` and
  `EMPTY_PANEL_REPLAY_PASS=true`.

## Sensitivity battery (counter, not predicate, exercised in a throwaway clone)

Each mutation was committed in `/fast/scratch/r37-cal/mut`; the counter bytes and predicate
were untouched. Expected `1` wherever a required component is removed or broken:

| mutation | counter output | exit |
|---|---|---|
| M1 erratum heading text changed | `unresolved=1 … correction=0 manifest_ok=1 receipts_ok=1` | 1 |
| M3 both receipt lines `mode=control`→`deciding` | `unresolved=1 … receipts_ok=0` | 1 |
| M4 receipt `panel_rev` → `1111…` | `unresolved=1 … receipts_ok=0` | 1 |
| M5 one specimen restored into empty panel | `unresolved=1 … manifest_ok=0` | 1 |
| M2 only the v2 line `mode=control`→`deciding` | `unresolved=0 … receipts_ok=1` | 0 |
| M6 only the v1 line inline `rev=` → `2222…` | `unresolved=0 … receipts_ok=1` | 0 |

M1/M3/M4/M5 show the zero is not vacuous: the erratum marker, the receipt mode label (at
least once), both aggregate revision pointers, and the zero-specimen path set are all
load-bearing.

## Adverse bounds (do not change the verdict; state them plainly)

1. `receipt_ok` tests `mode=control` against the whole receipt text, not per counter line.
   M2 (v2 line says `mode=deciding`, v1 line still `mode=control`) still scores
   `receipts_ok=1`. The committed receipt has `mode=control` on both lines
   (`replay-at-final-control.stdout:9,18`), verified directly, so the frozen after-state is
   intact — but the erratum prose ("requires `mode=control`") overstates the gate for a
   mixed receipt.
2. The per-line `rev=` field inside each counter output line is not validated; only the
   aggregate `counter_rev=` (against the manifest's `source_revision`) and `panel_rev=` are
   cat-file-checked and ancestor-checked. M6 confirms a bogus inline `rev=` still yields 0.
   In the committed receipt both inline revs equal `d9c496b…`, so the final reading is
   unaffected.
3. `old_mutant_resolves=0` in a fresh clone is weak by itself (clone prunes unreachable
   objects). The live-lane `cat-file -e` failure (exit 128) is the authoritative form and was
   checked directly.

## Files changed

- This report only: `.ufo/waves/round-37/w1/ExecCalibrationCounter.md`.
- No lane source, evidence, index, `.git`, or `.ufo/state` mutation; the working checkout was
  read-only. Scratch work: `/fast/scratch/r37-cal/{lane,mut,rederive.py,replay-work,replay-rerun.stdout}`.
- Tool installs/updates: none (system `git 2.56.0`, `python3 3.14.8` sufficed).

## Verdict and blockers

`C1_R37` mismatch count: **1** at `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`, **0** at the
candidate final `e6185d5f0b63a6963205110cb098f2f1eca27622` (and at the scorecard-recorded
`32826f37`). Both kill-rule halves hold with one counter byte-identical across the
comparison, and the committed receipt is reproducible bit-for-bit. No blockers.
