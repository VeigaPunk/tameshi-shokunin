# T51LabWitUSAGEEXIT — C2 survivor witness: S_USAGE_EXIT

Round 51 · hyaku run 9 · L1 tameshi R51 · seat: mutation-tester (leaf; no subagents).

## Item

Falsify equivalence of surviving mutant **S_USAGE_EXIT** (kagi `corpus/drift-pins.sh`,
rev `e64e81b8eb96f3682b00c1e7a291e84420b280fa`, blob sha256 `c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb`, mode 100755)
with an off-suite witness input where pristine and mutant differ in exit code or verdict line.

## Mutant construction

- Spec row: `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec:55-57`
  (`@defect S_USAGE_EXIT | an unknown argument exits 0 instead of 2`;
  `@old ... exit 2 ;;` → `@new ... exit 0 ;;`).
- Applied to pristine bytes (extracted via
  `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show e64e81b8...:corpus/drift-pins.sh`)
  exactly once, at the gate's `*)` catch-all arm, `corpus/drift-pins.sh:88`
  (`*) printf 'drift-pins: unknown argument: %s\n' "$1" >&2; exit 2 ;;`).
- Diff receipt `mutant.diff`: exactly one changed line (catch-all `exit 2` → `exit 0`);
  everything else byte-identical. Pristine sha256 `c138d34c...` matches the pin;
  mutant sha256 `c4e57c95c9bdcac2cf6a4bc2a08cdc9d6924b70c56a9ff0b684752ac6d236718`
  (`sha256sums.txt`).

## Witness input

One unknown argument; no other argv; empty scratch HOME/TMPDIR; cwd = scratch workdir:

```
bash <gate> --witness-unknown-arg
```

The gate exits inside its argument loop at line 88 before touching any file,
so no baseline/symbols fixture is needed and no pinned real-HOME file is read.
Hermetic env: `HOME=$S/home`, `TMPDIR=$S` (scratch root), run from `$S/w`.

## Probe results (3 runs each; witness.sh + run.log in receipts)

| variant | run | exit | stdout bytes | stderr last line |
|---|---|---|---|---|
| pristine | 1 | 2 | 0 | `drift-pins: unknown argument: --witness-unknown-arg` |
| pristine | 2 | 2 | 0 | same |
| pristine | 3 | 2 | 0 | same |
| mutant | 1 | 0 | 0 | `drift-pins: unknown argument: --witness-unknown-arg` |
| mutant | 2 | 0 | 0 | same |
| mutant | 3 | 0 | 0 | same |

- All six runs deterministic; stdout empty in every run.
- Cross-variant compare (run 1): stdout and stderr **byte-identical** (`diff` clean).
- The only differing observable between pristine and mutant on this input is the
  **exit code: 2 vs 0**.

## Verdict: HOLE (witness differs)

Pristine reports the usage error and exits 2; the mutant prints the same diagnostic but
exits 0 — silent success on an invalid invocation. Non-equivalent.

Coverage explanation: the gate's selftest oracle is exit-status-only (spec header:
"verdict oracle = exit status only") and every case re-invokes the gate with known flags
only (`--baseline`/`--symbols` at `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec:2-3,383-400` area, i.e. the `case` arms at `corpus/drift-pins.sh:85-86`); no case passes an unknown argument, so the catch-all arm is never exercised by the suite. Any caller that checks exit status after a usage error would silently proceed under the mutant.

## Receipts (.ufo/waves/round-51/w1/T51LabWitUSAGEEXIT/)

- `witness.sh` — probe script (source of the table above).
- `run.log` — full probe transcript incl. per-variant sha256.
- `pristine.run{1,2,3}.out/.err`, `mutant.run{1,2,3}.out/.err` — captured streams.
- `mutant.diff` — pristine→mutant unified diff (one line).
- `sha256sums.txt` — hashes of pristine/mutant/witness scripts.

No tools installed (no installs needed). No counters run. Lane checkout untouched except
the deliverable report and receipts dirs named by this item.

## Summary

- S_USAGE_EXIT (spec:55-57) is a single-line edit: usage catch-all `exit 2` → `exit 0` (`corpus/drift-pins.sh:88`).
- Witness: `bash <gate> --witness-unknown-arg`; solitary argv; scratch HOME/TMPDIR; no fixture needed.
- Pristine: exit 2, stderr `drift-pins: unknown argument: --witness-unknown-arg` (3/3 runs).
- Mutant: exit 0, same stderr line (3/3 runs); stdout/stderr byte-identical across variants.
- Only differing observable is the exit code (2 vs 0) → witness exists → **hole**.
- Suite misses it because its oracle is exit-status-only and no selftest case passes an unknown argument.
- Deterministic (6/6 runs consistent); receipts archived in w1 deliverable dir.
