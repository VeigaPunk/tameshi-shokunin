# MutatePanelManifest — single-field mutants of the committed empty-panel spec (C1 calibration)

Assignee: mutation-tester (leaf). Round 37, wave 1. Probe only: one defect class per run,
pristine/mutant/restored bytes, same bounded detector throughout. No contract change proposed.

## Detector under test

C1 counting command, run verbatim from the committed tree:

```
python3 .ufo/evidence/round-37/calibration/measure.py --lane LANE --rev REV
```

Fields the detector actually reads (`.ufo/evidence/round-37/calibration/measure.py`):

| line | read | predicate |
|---|---|---|
| 55 | `source_revision` | `git rev-parse <rev>:<path>` must equal the declared tree |
| 56 | `source_panel_path` | same resolution |
| 57 | `source_panel_tree` | exact string equality with the resolved tree |
| 63 | `source_specimen_count` | `== 9` |
| 64 | `expected_specimen_count` | `== 0` |
| 65 | (file inventory) | `ls-tree -r` at the measured rev must be exactly `[<empty-panel>/manifest.json]` |
| 26-45 | committed receipts | each receipt's `counter_rev` must equal `source_revision` verbatim; `panel_rev` must exist and be an ancestor of the measured rev |

Not read by the detector: `schema`, `source_specimens`, `mutation`,
`prior_unreachable_mutant_revision`, any unknown key. The constant
`OLD_MUTANT = 91373d5…` is hard-coded in the counter, independent of the manifest field.

## Method and isolation

```
git clone --no-local /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/r37-mut-panel-1792846812
```

Disposable clone at `/tmp/r37-mut-panel-1792846812` (264-commit object db, HEAD `e6185d5`, identical
panel tree at `d9c496b`, `b455001` and HEAD: `4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e`). Each
mutant: `git reset --hard e6185d5` → one-field edit → `git commit` → run the clone's own committed
counter (`--lane /tmp/r37-mut-panel-1792846812 --rev <mutant>`). Mutants are descendants of HEAD, so
both committed receipts stay ancestor-valid and only the mutated field varies. `git show --name-only`
confirms exactly one path changed per mutant. Mutant commits remain reachable through the clone
reflog (`git -C /tmp/r37-mut-panel-1792846812 log -g`). The live lane was only ever read
(`git -C LANE show/rev-parse/cat-file/merge-base`, plus one `git clone`); no lane index, jj, `.git`
or `.ufo/state` write was issued. No tool install or update was needed.

Pristine bytes, reference hash of `manifest.json` at `e6185d5`:
`e0c06148c71e6c4f02fde85d04a0e9d6ca87f5862227f4cb11578497a945bd13`.

## Baselines (same detector, before any mutant)

```
$ python3 /tmp/r37-mut-panel-1792846812/.ufo/evidence/round-37/calibration/measure.py --lane /tmp/r37-mut-panel-1792846812 --rev e6185d5
C1_R37: unresolved_control_inputs=0 old_mutant_resolves=0 correction=1 manifest_ok=1 receipts_ok=1 rev=e6185d5f0b63a6963205110cb098f2f1eca27622 C1_R37_PASS=true      (exit 0)

$ python3 .ufo/evidence/round-37/calibration/measure.py --lane . --rev d9c496b
C1_R37: unresolved_control_inputs=1 old_mutant_resolves=0 correction=0 manifest_ok=0 receipts_ok=0 rev=d9c496b19371b779ce0eec6dfee1b049b27a3a2d C1_R37_PASS=false     (exit 1)
```

Both match the frozen before/after expectation, so a mutation verdict below is a kill, not a
baseline artefact.

## DETECTED — single-field edits the counter reports as a mismatch

| mutant (one field) | clone rev | stdout core | verdict |
|---|---|---|---|
| `source_panel_tree` → `921019db…` (valid sibling tree of `.ufo/evidence/round-35/c1`) | `16d32f0531e9` | `unresolved=1 … manifest_ok=0 receipts_ok=1` | killed |
| `source_panel_tree` → `4f3d8af5…9f` (nonexistent) | `ea0584f7011f` | `unresolved=1 … manifest_ok=0 receipts_ok=1` | killed |
| `source_revision` → `e6185d5…` (same panel tree, `4f3d8af5`) | `3368c4fdf378` | `unresolved=1 … manifest_ok=1 receipts_ok=0` | killed via receipts only |
| `source_revision` → `<d9c496b>^0` (same commit, other spelling) | `1ee927caa083` | `unresolved=1 … manifest_ok=1 receipts_ok=0` | killed via receipts only |
| `source_panel_path` → `.ufo/evidence/round-35/c1` (parent dir) | `6e5cfb48ca27` | `unresolved=1 … manifest_ok=0` | killed |
| `source_specimen_count` → `8` | `3845b8fabfb2` | `unresolved=1 … manifest_ok=0` | killed |
| `source_specimen_count` → `"9"` (string) | `1892b117af5d` | `unresolved=1 … manifest_ok=0` | killed |
| `expected_specimen_count` → `1` | `303f8a4c4f1b` | `unresolved=1 … manifest_ok=0` | killed |
| `source_panel_tree` key deleted | `b62c6e75bd7a` | `unresolved=1 … manifest_ok=0` | killed (KeyError path) |
| `expected_specimen_count` key deleted | `4d4ae4cb77dc` | `unresolved=1 … manifest_ok=0` | killed (KeyError path) |
| inventory: add `empty-panel/cfg99-extra.json` | `ca61f5849a46` | `unresolved=1 … manifest_ok=0` | killed (`got_paths` length 2) |
| inventory: add `empty-panel/.gitkeep` | `76eef700d71a` | `unresolved=1 … manifest_ok=0` | killed |
| inventory: rename `manifest.json` → `panel.json` | `8cbc109e583b` | `unresolved=1 … manifest_ok=0 receipts_ok=0` | killed |

The tree-ID axis is fully covered: both a plausible valid-but-wrong tree and an arbitrary
non-resolving tree are rejected. The `source_revision` mutants are rejected *only* by the receipt
coupling (`counter_rev` verbatim match), not by tree identity — the two panel trees are byte-identical,
so `manifest_ok` stays 1.

## SURVIVED — single-field edits that pass silently (`C1_R37_PASS=true`, exit 0)

| mutant (one field) | clone rev | mutated blob sha256 | verdict |
|---|---|---|---|
| `source_specimens`: drop last entry | `890b872b0344` | `3f26459a0a20…` | **survived** |
| `source_specimens`: replace `cfg00-accept-swap.json` with `ghost-specimen.json` | `1075ebad05b6` | `fb477c9b089a…` | **survived** |
| `source_specimens`: duplicate one entry, drop another (len stays 9) | `ba826f010c45` | `67962ed71a38…` | **survived** |
| `source_specimens`: reverse order | `839c38fbce03` | `5b02757eb723…` | **survived** |
| `source_specimens` key deleted entirely | `3e5fc50b8ede` | `223f647f26a0…` | **survived** |
| `schema` → `tameshi-empty-panel-v2` | `c50cfe76cff8` | `190cf9b6350d…` | survived |
| `mutation` prose rewritten ("No specimens removed; prose only.") | `6da0d9c4c15d` | `52e5a185d807…` | survived |
| `prior_unreachable_mutant_revision` → resolvable `d9c496b…` | `62561bfb28a5` | `31d91a307fbe…` | survived |
| `prior_unreachable_mutant_revision` deleted | `4f08d2d12e55` | `1606fd9e2ba0…` | survived |
| unknown key `control_operator: "hand-written"` added | `9d797fd44139` | `e05ca381b91d…` | survived |
| `source_specimen_count` → `9.0` (float; JSON type defect) | `d49da2a81827` | `d57a8d2c5d94…` | survived (`9.0 == 9`) |
| `expected_specimen_count` → `false` (bool; JSON type defect) | `114a1afab10a` | `d74d5c7c7309…` | survived (`False == 0`) |
| `source_panel_path` → trailing slash | `d561c1b139cf` | — | survived |
| `source_panel_path` → `./`-prefixed | `7ee13b45c385` | — | survived |

Representative exact output (specimen swap, `1075ebad05b6`):

```
$ python3 /tmp/r37-mut-panel-1792846812/.ufo/evidence/round-37/calibration/measure.py \
    --lane /tmp/r37-mut-panel-1792846812 --rev 1075ebad05b6
C1_R37: unresolved_control_inputs=0 old_mutant_resolves=0 correction=1 manifest_ok=1 receipts_ok=1 \
  rev=1075ebad05b6... C1_R37_PASS=true                                                                       (exit 0)
```

## Coverage finding (reported, not repaired)

1. **The specimen inventory is unattested by the C1 counter.** `measure.py:63-65` checks only
   `source_specimen_count == 9`, `expected_specimen_count == 0` and the *empty-panel* file list. It
   never reads `source_specimens`, so a committed input specification can name a nonexistent
   specimen, drop a real one, or lose the list and still score `C1_R37_PASS=true`. The strong case
   is `1075ebad05b6`: the spec asserts nine named specimens while one name does not exist in
   `4f3d8af5…`.
2. The separate replay wrapper does guard this, so the hole is local to the counting command:
   `replay-empty-panel.py:81-82` compares `sorted(source_names)` against `sorted(source_specimens)`.
   Same mutant, same clone:
   ```
   $ python3 /tmp/r37-mut-panel-1792846812/.ufo/evidence/round-37/control/replay-empty-panel.py \
       --lane /tmp/r37-mut-panel-1792846812 --rev 1075ebad05b6 --work-root /tmp/r37-mut-wrap-work-1075ebad
   EMPTY_PANEL_REPLAY: SETUP source_specimen_set_mismatch                                      (exit 2)
   ```
3. Both tools share the JSON type-coercion weakness (`9.0 == 9`, `False == 0` at
   `measure.py:63-64` and `replay-empty-panel.py:73`), so a `9.0`/`false` count is accepted by both.
4. `prior_unreachable_mutant_revision` is decorative for the detector: the "unreachable prior
   mutant" predicate uses the hard-coded `OLD_MUTANT` constant, so corrupting or deleting that
   manifest field cannot change the count. That is a documentation/provenance field, not a scored one.

None of these widen or narrow the frozen predicate; the surviving mutants are coverage facts for C1.

## Restoration evidence

Scratch copy reset to the pristine revision after the last probe:

```
restore: HEAD = e6185d5f0b63a6963205110cb098f2f1eca27622
restore: git show HEAD:<manifest> sha256 = e0c06148c71e6c4f02fde85d04a0e9d6ca87f5862227f4cb11578497a945bd13
restore: worktree file sha256           = e0c06148c71e6c4f02fde85d04a0e9d6ca87f5862227f4cb11578497a945bd13
restore: git status --porcelain         = ""
restore: measure rc=0  C1_R37: unresolved_control_inputs=0 … C1_R37_PASS=true
```

Live lane integrity (read-only throughout):

```
lane: HEAD = e6185d5f0b63a6963205110cb098f2f1eca27622
lane: committed manifest sha256 = e0c06148c71e6c4f02fde85d04a0e9d6ca87f5862227f4cb11578497a945bd13
lane: worktree manifest sha256  = e0c06148c71e6c4f02fde85d04a0e9d6ca87f5862227f4cb11578497a945bd13
lane: rev-parse --abbrev-ref HEAD = HEAD   (detached, unchanged)
```

Scratch tree `/tmp/r37-mut-panel-1792846812` is a disposable clone; it is restored to `e6185d5` and
retained only because its reflog holds the mutant commits cited above.

## Verdict summary

- 13 single-field / inventory mutants killed; 14 survived.
- Above the fold for C1: the source-tree-ID axis and the plain counts are enforced; the specimen
  *list* is not, so a corrupt inventory passes the counting command while the replay wrapper rejects
  it. Reported as a coverage finding only.
