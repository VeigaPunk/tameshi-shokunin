# Seat T51LabWitPOLICY — C2 S_POLICY survivor witness (round-51 w1)

## Verdict: HOLE — the S_POLICY mutant is NOT equivalent to the pristine gate.
An off-suite witness input exists on which pristine and mutant differ in the
verdict line (the item's falsification criterion). Exit codes coincide at 1;
the emitted verdict line differs (POLICY refusal vs sha-DRIFT complaint).

## Witness (smallest found)
One no-hash baseline row whose sha field is not `-`, plus one symbol row (the
gate refuses an empty symbols file, so the second row is required).
- baseline row: `secret.txt` (0600, 1 line) registered no-hash via
  `DRIFT_EXTRA_NOHASH`; sha field `deadbeefdeadbeef…` (not `-`).
- symbol row: `pinned.txt` (644, 2 lines), line-pin `1` ERE `alpha`.
Files: `w1/T51LabWitPOLICY/{base.tsv,sym.tsv,secret.txt,pinned.txt}`.
This is exactly the off-suite blind spot named in the spec at
`.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec:44` — "the selftest's
no-hash row carries sha `-`, so the POLICY refusal is never reached".

## Mutant bytes
- Pristine: `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh` — sha256 `c138d34c…` matches the spec pin; 451 lines.
- Mutant: single-line edit (pristine line 145): `if [[ "$sha" != "-" ]]; then` → `if [[ "$sha" == "-x" ]]; then`. Resulting sha256 `daa39220…` == the sweep-recorded S_POLICY mutant hash (`.ufo/evidence/round-51/c2/sweep/results.tsv:9`), i.e. byte-exact reproduction of the sweep's mutant.

## Runs (3x each, deterministic)
Command:
`env -i HOME=$S/home TMPDIR=$S/w DRIFT_EXTRA_NOHASH=$S/w/wit/secret.txt bash <gate> --baseline $S/w/wit/base.tsv --symbols $S/w/wit/sym.tsv`

| gate | exit | output line 1 | output line 2 |
|---|---|---|---|
| pristine (x3) | 1 | `POLICY  …/secret.txt baseline sha must be `-` (secret-bearing path is never hashed)` | `DRIFT_PINS: DRIFT (files_ok=0 files_bad=1 symbols_ok=1 symbols_bad=0)` |
| mutant (x3) | 1 | `DRIFT   …/secret.txt sha deadbeefdead->-` | `DRIFT_PINS: DRIFT (files_ok=0 files_bad=1 symbols_ok=1 symbols_bad=0)` |

- Evidence: `w1/T51LabWitPOLICY/runs.tsv`, `runs.pristine.{1,2,3}.out`, `runs.mutant.{1,2,3}.out`; `cmp` proves x3 identity within each gate.
- Differing line: line 1 (`diff runs.pristine.1.out runs.mutant.1.out`).

## Why the mutant survives the suite but is not equivalent
- `drift-pins.sh:144-146`: the POLICY branch prints `POLICY` and `continue`s
  *before* any mode/lines/sha comparison. The mutant's flipped guard
  (`sha == "-x"` never true) skips that refusal, falls into the no-hash
  fingerprint (`fp … nohash` → `cs="-"`), and the unconditional sha compare at
  `drift-pins.sh:154` then emits `DRIFT … sha deadbeefdead->-`.
- On the suite's actual inputs the blind spot never triggers: the selftest's
  no-hash row pins sha `-` (spec:44), so both gates emit the same exit
  status (0); the mutant "survives". On the off-suite witness the observable
  verdict line changes — the secret-refusal semantics (never hash, refuse a
  baseline that asks for a hash) is replaced by a content-drift complaint.
- The exit code alone does not separate the gates on this witness (1/1); the
  separation is the verdict line, which is within the item's stated criterion.

## Tooling
No tools installed (git/bash/coreutils only). Scratch used per directive:
`S=/fast/scratch/hyaku/tameshi-r51/T51LabWitPOLICY`, HOME/TMPDIR pointed at
scratch, deleted after receipt copy.

## Summary
- HOLE: S_POLICY mutant is non-equivalent (verdict line differs on witness input).
- Witness: no-hash baseline row with sha `deadbeef…` ≠ `-` + one symbol row.
- Pristine: POLICY refusal, exit 1; mutant: no POLICY, `DRIFT … sha deadbeefdead->-`, exit 1.
- Mutant bytes match sweep hash `daa39220…`; 3+3 runs, deterministic.
- Blind spot: suite's no-hash row pins `-` (spec:44), never reaching the guard at drift-pins.sh:145.
- Receipts: `w1/T51LabWitPOLICY/` (witness.sh, inputs, outputs, runs.tsv, manifest.sha256).
