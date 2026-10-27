# Seat T51LabWitHARDLINK — C2 survivor witness for S_HARDLINK

Verdict: **HOLE** — the surviving mutant S_HARDLINK is NOT equivalent to the
pristine gate. An off-suite witness exists on which pristine and mutant differ
in exit code and verdict line.

## Hypothesis falsified

S_HARDLINK = single edit in kagi `corpus/drift-pins.sh` at rev
`e64e81b8eb96f3682b00c1e7a291e84420b280fa` (blob sha256
`c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb`):

```
line 135 (pristine):  if [[ "$nlink" -gt 1 ]]; then
line 135 (mutant):    if [[ "$nlink" -gt 2 ]]; then
```

The `@old` string occurs exactly once in the pinned bytes (grep -c = 1, line 135).
Mutant construction: `sed '135s/…/> 2 …/'` on the pristine bytes → mutant sha256
`faef927e2db2f984b183e6425433811a85364334d18ea94f36db510218801abc`, which
exactly matches the sweep-recorded mutant sha for S_HARDLINK
(`.ufo/evidence/round-51/c2/sweep/results.tsv`).

The guard is at `corpus/drift-pins.sh:133-137`:

```sh
nlink=$(stat -c '%h' -- "$p" 2>/dev/null || echo 1)
if [[ "$nlink" -gt 1 ]]; then
  printf 'LINK    %s (hardlink count %s — the path is not uniquely the file)\n' "$p" "$nlink"
  f_bad=$((f_bad + 1)); continue
fi
```

## Smallest witness

- Baseline row pins `$HOME/wh/a.txt` — a regular file created as a hardlink to
  `$HOME/wh/b.txt` (verified `stat -c '%h'` = 2 for both), so link count = 2.
- Baseline row carries the true mode/lines/sha of the file (644, 1,
  `5891b5b5…`), so the hardlink guard is the *only* differing check.
- One symbols row (`$HOME/wh/sym.txt`, expected line 1, ere `^hello$`) passes on
  both gates.
- Alternate-baseline harness (`--baseline F --symbols F`); the membership/DUP
  block is skipped for an alternate baseline by design
  (`drift-pins.sh:166-171`), so FILES and the real `$HOME` are never touched.
- Runs are hermetic: `env -i HOME="$S/w/home" TMPDIR="$S/w" PATH="/usr/bin:/bin"`
  (the gate's pinned FILES/NOHASH paths under `$HOME` are never read; the
  witness files live entirely under the scratch HOME).

Evidence commands:

```
stat -c '%h' <a.txt> <b.txt>      # 2  2
/…/witness-run.sh                  # 3x3 harness (receipts dir)
sha256sum gates.before.sha256 gates.after.sha256   # identical
```

## Observed runs (3 each, same witness)

| run | pristine exit | pristine last line(s) | mutant exit | mutant last line |
|-----|---------------|------------------------|-------------|------------------|
| 1   | 1             | LINK … hardlink count 2; DRIFT (files_ok=0 files_bad=1 symbols_ok=1 symbols_bad=0) | 0 | CLEAN (files=1 symbols=1) |
| 2   | 1             | same | 0 | same |
| 3   | 1             | same | 0 | same |

- Differing line: the `LINK    … (hardlink count 2 …)` line is printed by the
  pristine gate only (`diff out.pristine.1.txt out.mutant.1.txt` → `1,2c1`).
- Verdict lines differ: `DRIFT_PINS: DRIFT (…)` vs `DRIFT_PINS: CLEAN (…)`.
- Exit codes differ: 1 vs 0.

## Why the suite missed it

The suite's selftest creates no hardlink (its link case is a symlink, caught by
`-L` at `drift-pins.sh:128` before the nlink guard), so the `nlink>1` guard is
never exercised there. With an off-suite witness (a real hardlink with link
count 2) the mutant accepts the hardlinked baseline path and reports CLEAN/exit
0, while pristine reports LINK/exit 1.

## Evidence

Receipts: `.ufo/waves/round-51/w1/T51LabWitHARDLINK/` — `witness-run.sh`,
`out.pristine.{1,2,3}.txt`, `out.mutant.{1,2,3}.txt`,
`gates.before.sha256`, `gates.after.sha256`, `wh-baseline.tsv`,
`wh-symbols.tsv`. Gate bytes unchanged by the probe (before/after hashes
identical). No lane/repo file was modified.

## Summary

- S_HARDLINK is a hole: hardlink-count-2 baseline witness → pristine exit 1 +
  LINK, mutant exit 0 + CLEAN (3/3 runs each, identical).
- Mutant bytes reproduced exactly (sha `faef927e…` = sweep's mutant sha).
- Differing line: the `LINK … hardlink count 2` line; exit 1 vs 0.
- Root cause of survival: selftest never creates a hardlink (only a symlink,
  caught earlier by `-L`).
- Witness is minimal: one baseline row, one symbols row, alternate-baseline
  harness, scratch HOME.
- Probe left all lane bytes untouched (gate hashes identical before/after).
