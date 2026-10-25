# ExecC2Base — C2 census counter at the base revision

Seat: `L1Tameshi41.ExecC2Base` (read-only). Lane checkout not modified; only this report written.

## Exact command

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev a3d6c690bcbf8914551d4f4e8e1612784c1c2046
```

## stdout (verbatim, single line)

```
C2_R41: tool_absent=1 var_expected=0 symlink_expected=0 rev=a3d6c690bcbf8914551d4f4e8e1612784c1c2046 C2_R41_PASS=false
```

## exit code (verbatim)

```
1
```

(measured as `EXIT=1` appended by the harness after `; echo "EXIT=$?"`)

## What the numbers mean

- `tool_absent=1` — `tools/write-path-census-v3.py` does not exist at
  `a3d6c690bcbf8914551d4f4e8e1612784c1c2046`, so `.ufo/evidence/round-41/census/measure.py:161-172`
  returns the early-return `emit(...)` branch before any fixture, selftest, live-site or mutant
  measurement runs. This matches the contract's declared `before`:
  `tool_absent=1 var_expected=0 symlink_expected=0 C2_R41_PASS=false`.
- `var_expected=0` and `symlink_expected=0` are the hard-coded sentinels of that early-return branch
  (lines 167-168), not measurements of fixtures or live sites.
- `C2_R41_PASS=false` is therefore the do-nothing-control outcome the contract predicts: the base
  revision cannot pass, and none of the seven target fields beyond `tool_absent` is reachable.

## Retained evidence (re-checked, not asserted)

| Check | Command | Result |
|---|---|---|
| counter pin matches contract `claims.C2.counter_sha256` | `sha256sum .ufo/evidence/round-41/census/measure.py` | `5d57c7097fb33a66d11cb19b834dd7f92ade268c56562c8a34d7a94bf64ef696` — identical to the frozen pin |
| base revision resolves | `git cat-file -e a3d6c690bcbf8914551d4f4e8e1612784c1c2046^{commit}` | exit 0 (`REV_OK`) |
| v3 tool absent at base | `git cat-file -e a3d6c690...:tools/write-path-census-v3.py` | absent (`TOOL_ABSENT`) |
| v2 tool present at base | `git cat-file -e a3d6c690...:tools/write-path-census-v2.py` | present (`V2_PRESENT`) |
| lane tree untouched by this seat | `git status --porcelain` | only `?? .ufo/evidence/round-41/sources/` and `?? .ufo/waves/round-41/` (pre-existing wave/scribe artefacts from sibling seats, not mine) |

Contract file read-only per instruction and never edited: `.ufo/evidence/round-41/contract.json`
(working-tree sha256 `058f43932f5376d6ef47b025e2e5b6898942e8a7f7628cc8a3ba4acf718442f2`).

## Scope discipline

- This is a control/as-baseline run at the allowed `--rev a3d6c690...`; it is **not** the deciding
  run. No `--rev work` run and no tip run was performed by this seat.
- `--control` and `--selftest` modes were not executed here; they belong to other seats
  (`L1Tameshi41.ExecC2Control`, `L1Tameshi41.ExecV3Selftest`).

## Tooling

No install or update performed (nothing needed; `python3` and `git` already present). pacman
transactions untouched per the host-wide pause.

## Risks / blockers

None. The counter behaves exactly as frozen: base → `C2_R41_PASS=false` via the tool-absent branch.

Report: .ufo/waves/round-41/w1/ExecC2Base.md
