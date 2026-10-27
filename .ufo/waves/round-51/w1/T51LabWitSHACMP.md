# T51LabWitSHACMP — C2 survivor witness for S_SHA_CMP

Seat: T51LabWitSHACMP (UFO-FSD mutation tester / wave-1 witness probe).
Claim: C2 (depth 9→10). Item: off-suite witness for surviving mutant **S_SHA_CMP** of kagi `corpus/drift-pins.sh` @ e64e81b8eb96f3682b00c1e7a291e84420b280fa (blob sha256 `c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb`).

## Mutant (same bytes the sweep ran)

- Source: `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh` (451 lines, mode 100755).
- Spec row: `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec` S_SHA_CMP: `@old [[ "$cs" != "$sha" ]] && diffs+=("sha …")` → `@new [[ "$cs" != "$cs" ]] && diffs+=("sha …")` (lines 36-37 of the spec; the @old occurs exactly once in the pinned bytes).
- Applied at `drift-pins.sh:156` (`grep -n 'diffs+=('` → line 156 `[[ "$cs" != "$sha" ]] && diffs+=("sha ${sha:0:12}->${cs:0:12}")`). The compare `"$cs" != "$cs"` is never true → the sha diff is never appended → sha drift is unasserted.
- Rebuilt mutant sha: `a29e775fef22e8bcd4ec3bcf5686ce889b67fcbc8913101c905b31930fa62fab` — identical to `.ufo/evidence/round-51/c2/sweep/results.tsv` S_SHA_CMP `mutant-sha256`. I ran exactly the sweep's mutant.

## Witness (minimal)

Single hashed file `w/f.txt` pinned by one baseline row + one symbol row (both in the scratch fixture; `--baseline F --symbols F`; `env -i HOME=<scratch> TMPDIR=<scratch>` — no real `$HOME` files touched):

- baseline `base.tsv` row: `<w/f.txt> 644 2 <sha(pristine)>`; symbols `sym.tsv` row: `<w/f.txt> 1 ^alpha$`.
- Pristine `f.txt` = `alpha\nbeta\n` (11 bytes, 2 lines, mode 644, sha `e49c81e2d2f8…`); witness content change keeps line count (2), mode (644) and byte count (11): `alpha\nBETA\n` (sha `69726aa46966…`). Only the hash differs.
- Driver: `witness.sh` (receipts).

## Runs (identical command for both gates)

`env -i HOME=$S/home TMPDIR=$S PATH=$PATH bash <gate> --baseline $S/fix/w/base.tsv --symbols $S/fix/w/sym.tsv`

| run | gate | exit | last line |
|---|---|---|---|
| control A (pristine f.txt) | pristine | 0 | `DRIFT_PINS: CLEAN (files=1 symbols=1)` |
| control B (pristine f.txt) | mutant | 0 | `DRIFT_PINS: CLEAN (files=1 symbols=1)` |
| witness (mutated f.txt) ×3 | pristine | 1,1,1 | `DRIFT_PINS: DRIFT (files_ok=0 files_bad=1 symbols_ok=1 symbols_bad=0)` |
| witness (mutated f.txt) ×3 | mutant | 0,0,0 | `DRIFT_PINS: CLEAN (files=1 symbols=1)` |

Differing line (pristine only): `DRIFT   <w/f.txt> sha e49c81e2d2f8->69726aa46966` — see `diff -u` of `witness-pristine.1.out` vs `witness-mutant.1.out`. Exit codes differ (1 vs 0) and verdict lines differ (DRIFT vs CLEAN) on the same input.

Selftest parity (confirms the hole is off-suite): both gates print `DRIFT_SELFTEST: PASS (13 cases)` exit 0 (`bash <gate> --selftest` in the scratch env), matching the sweep's green control and `S_SHA_CMP SURVIVED`. The selftest has no content-only change case: every case touches lines/mode/symbols (`drift-pins.sh:408-438` — `run "content drift"` appends a line (`gamma`), count=2; no case rewrites bytes at equal line count).

## Verdict

**HOLE** — the surviving mutant S_SHA_CMP is not equivalent: the off-suite witness above differs from pristine in exit code (0 vs 1) and verdict line (CLEAN vs DRIFT) on all 3×3 runs. The mutant silently drops content-hash drift detection (`drift-pins.sh:156`), so a file whose bytes changed under identical mode/lines/membership passes as CLEAN. The on-suite der is purely a selftest coverage gap.

## Notes

- No tools installed (stdin coreutils; nothing to record under the 2026-10-19 directive).
- Lane untouched (read-only); sibling kagi read via `git show` only; no clones made; scratch `/fast/scratch/hyaku/tameshi-r51/T51LabWitSHACMP` deleted after copying receipts.
- Receipts: `.ufo/waves/round-51/w1/T51LabWitSHACMP/` — `witness.sh`, `base.tsv`, `sym.tsv`, `witness-f-mutated.txt`, `control-pristine.clean.out`, `control-mutant.clean.out`, `witness-pristine.{1,2,3}.out`, `witness-mutant.{1,2,3}.out`, `drift-pins.pristine.sh`, `drift-pins.mutant.sh`, `MANIFEST.txt` (rev, blob sha, mutant sha, witness shas/mode/lines/bytes).

## Summary

- S_SHA_CMP mutant rebuilt byte-identically to the sweep (sha `a29e775f…`, results.tsv match) by applying spec @old→@new at `drift-pins.sh:156`.
- Minimal witness: one file `alpha\nbeta\n`→`alpha\nBETA\n` (same 2 lines, mode 644, 11 bytes) pinned by one baseline row + one symbol row.
- Pristine gate: exit 1 ×3, `DRIFT … sha e49c81e2d2f8->69726aa46966`, final `DRIFT_PINS: DRIFT …`.
- Mutant gate: exit 0 ×3, single line `DRIFT_PINS: CLEAN (files=1 symbols=1)` — same input.
- Controls (pristine input) exit 0 CLEAN for both gates; both gates' selftest PASS 13/13.
- **Verdict: HOLE** — witness differs in exit code and verdict line; S_SHA_CMP is a real (non-equivalent) survivor, not an equivalent mutant.
- Root cause: `cs != cs` never true at line 156; on-suite survival is a selftest coverage gap (no equal-line-count content-change case, lines 408-438).
