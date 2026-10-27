# T52W2MutC2Followup — C2 counter survivors

All fixture probes use disposable `git clone --shared` scratch clone(s) from CAND0 `bcba8924894216268afc4171f06eb8c28e912b46`; the frozen counter and mutants are copies. The C2 counter `--selftest` passed (8/8), and pristine CAND0 returned `total=0 C2_R52_PASS=true` (receipt `T52W2MutC2Followup/receipts/00-selftests-baseline.stdout`).

## Inconclusive probe resolutions

| Probe | Concrete one-file fixture at CAND0 | Pristine output | Mutant output | Verdict |
|---|---|---|---|---|
| M07 — continuation scan | `85af447826310de66e66192cdc564b281bac9500`; in SKILL.md's existing m3c bullet, replace continuation `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX` with bare `/tmp/tameshi-r4-2-regression.XXXXXX`. The violating path is on a continuation line; the first line remains clean. | `m3=1 total=1 C2_R52_PASS=false` | `m3=0 total=0 C2_R52_PASS=true` | **SURVIVED** — mutant scans only the opening bullet line. |
| M13 — byte-identical drift row | `20de4571629269b719c225dc1cfb43532f2eceaf`; add one trailing space to the frozen drift-pins queue row, leaving its superseding note untouched. | `m5=1 total=1 C2_R52_PASS=false` | `m5=0 total=0 C2_R52_PASS=true` | **SURVIVED** — substring match accepts a byte-different row. |
| M15 — minimum quote length | `3d329176d96d30a76788cca785c9c2a0e8b4c020`; append verbatim quote `# T51W2Read01 —` (15 squashed chars) to the existing T51W2Read01 correction, preserve its floor-covering findings, set `wrong_expectations=len(findings)`. | `m4=1 total=1 C2_R52_PASS=false` | `m4=0 total=0 C2_R52_PASS=true` | **SURVIVED** — 10–19-character quotes pass the weakened threshold. |

Each fixture commit changes only the specified path. All three mutants and pristine passed `--selftest` (8 cases). Exact stdout receipts and mutant copies/hashes are under `T52W2MutC2Followup/`.

## Critic false-pass reproduction

On a separate clean CAND0-derived fixture, commit `fc9a0b2ef47616ebae762c134c0e2a657f18a4d9` adds only an unrelated final SKILL.md section: `### Round-26 unrelated notes` / `The nine ledger legs remain unchanged in this sibling section.` `git grep -n 'nine ledger legs' fc9a0b2e -- SKILL.md` locates it at SKILL.md:2176. The pristine counter nevertheless prints `m1=0 ... total=0 C2_R52_PASS=true` (receipt `false-pass-fc9a0b2e-pristine.stdout`). This reproduces the critic’s false pass on CAND0 bytes.

## Survivor statement check at CAND0

Commands used: `git -C LANE grep -n -e 'nine ledger legs' -e '9/9' -e 'legs_conforming=9' -e 'tameshi-r4-2-regression' CAND0 -- SKILL.md corpus/`; targeted `git show CAND0:SKILL.md` / `corpus/knowledge/...` reads; and the pristine `measure.py --lane CLONE --rev CAND0 --explain`. Full grep and observations are in `receipts/10-cand0-survey.txt`.

| Survivor | Does CAND0 SKILL.md contain the corresponding stale form? |
|---|---|
| M01 section boundary | No stale nine-leg claim: the checked Round-26 section says `ten ledger legs` and has the single correct `(10/10)` mention. The out-of-section stale knowledge statement is `corpus/knowledge/mte-report-interop.md:2` (dated 2026-10-22, historical verification). |
| M03 mention cardinality | No duplicate/wrong `(K/K)` mention: one `mte-interop-check (10/10)` at SKILL.md:2136. |
| M04 `/tmp`/TMPDIR row | No unsafe form in the checked fleet-mutation-runner row: SKILL.md:2149 describes auto scratch under `${TMPDIR:-/tmp}`. |
| M05 claim-location uniqueness | No duplicate claim lines: “the maintained driver also prints the failing count” occurs once at :174; “marks the run DEGRADED” occurs once at :211. |
| M06 pointer range | No failing checked pointer at CAND0: pristine m3 is 0, so the two cited ranges contain their expected runner tokens. |
| M07 continuation scan (resolved) | No violating m3c form: the actual continuation at :937 uses `${TMPDIR:-/tmp}`. The bare `/tmp` fixture form is not present in that bullet. |
| M09 canonical reader path | No: all 20 round-51 correction records use their canonical reader-file paths. |
| M11 floor labels | No missing frozen floor: CAND0 m4=0, including both floor-bearing readers. |
| M13 byte identity (resolved) | No: the sole drift-pins row at `corpus/knowledge/fleet-kill-rate-ledger.md:119` is byte-identical to the frozen row. |
| M14 T52 seat selection | No live entry to test: CAND0 has zero T52 ledger entries; m6 passes vacuously. |
| M15 quote minimum (resolved) | No short existing correction quote: shortest quote in CAND0 correction records is 35 squashed characters. |
| M16 supersession note | No: the CAND0 supersession entry at `corpus/knowledge/fleet-kill-rate-ledger.md:441` contains `drift-pins`, `unmeasured by sweep`, `supersession`, and `case 10`. |

The four requested grep strings yield these relevant CAND0 facts: `nine ledger legs` and `legs_conforming=9` do not occur in SKILL.md; `9/9` does occur in unrelated SKILL.md records (for example :729, :767, :2145), not as the interop leg count. `corpus/knowledge/mte-report-interop.md:2` retains the dated nine-leg/9/9 verification. `/tmp/tameshi-r4-2-regression` occurs in SKILL.md:937 with TMPDIR, and in historical Round-10 narrative at :1321 without TMPDIR; that :1321 passage describes the 2026-10-14 r10-2 replay, not the current runner. The m3c bullet and m2 row themselves are correctly TMPDIR-qualified.

## Restoration and evidence

Between probes the disposable clone was reset to CAND0 before constructing the next independent one-file tree. The final pristine rerun at CAND0 again returned `total=0 C2_R52_PASS=true`; receipt: `T52W2MutC2Followup/receipts/restored-CAND0-pristine.stdout`. No lane checkout, index, or jj state was changed. No tools were installed or updated. No verdict beyond the counter’s observed output is inferred.

## Summary
- M07, M13, M15 all resolved **SURVIVED** on isolated one-file trees.
- Reproduced unrelated stale nine-leg SKILL statement with C2 pass true on a CAND0 clone.
- CAND0 SKILL m3c and m2 statements are TMPDIR-qualified; historical bare `/tmp` narrative remains outside those checks.
- Probe outputs, copied mutants, and SHA-256 values are in `T52W2MutC2Followup/`.