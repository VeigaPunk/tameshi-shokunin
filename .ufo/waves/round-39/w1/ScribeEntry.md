# ScribeEntry — Entry check: `corpus/knowledge/r8-golden-update-flag.md` (godspeed, round-39 w1)

## Axes
- Axis under judgment: **depth** (milestone: Entry check).
- No other axis touched; no command-run, calibration, or ledger claim asserted here.

## Verdict
The entry claims **only the flag rule**, not the lane census result.

## Citation (exact)
- File: `corpus/knowledge/r8-golden-update-flag.md`
- Boundary section header: `corpus/knowledge/r8-golden-update-flag.md:16` — `## Boundary`
- Boundary bullet: `corpus/knowledge/r8-golden-update-flag.md:18` — "The note describes a documented flag. It is **not a run of TensorFlow Federated's test runner**, and it **does not say the lane's gates are free of unflagged writes**."
- Scoping sentence in the "What this lane uses it for" section: `corpus/knowledge/r8-golden-update-flag.md:14` — "This entry **does not claim that measurement**; the counter receipt does."
- Rule stated: `corpus/knowledge/r8-golden-update-flag.md:14` — "a write of an expected file is a flagged path, and a comparison that rewrites the expected file with no flag is not the discipline."

## Consistency with the frozen contract
- `.ufo/evidence/round-39/contract.json` C2 (`depth`) pins the census measurement to the counting command `python3 .ufo/evidence/round-39/census/measure.py --lane LANE --rev REV` and the tool pin `tools/write-path-census.py` (sha256 `bc8c660c…`). The knowledge entry defers exactly to that receipt ("the counter receipt does"), so the entry and the contract partition cleanly: rule in the entry, measurement in the census tool.
- C2 sources line matches the entry header sources (S107/S108, opened 2026-10-24).

## Gates / commands run
| Command / path | Outcome |
|---|---|
| `read corpus/knowledge/r8-golden-update-flag.md` | Full 20-line entry read; no unobserved content cited. |
| `grep "Boundary\|does not claim that measurement\|does not say the lane's gates\|counter receipt" corpus/knowledge/r8-golden-update-flag.md` | Hits at lines 14, 16, 18 (plus 19–20 boundary bullets). |
| `read .ufo/evidence/round-39/contract.json` | Frozen contract read; not edited; base rev `50aadd1bbd94e43cd3fcfb81459414394db2dc35` untouched. |

## Touched surfaces
- Written only this report: `.ufo/waves/round-39/w1/ScribeEntry.md`.
- Live lane checkout, `.ufo/state`, Git index/jj state, fleet repo, `considerthese/`, `shokuknow`: untouched. No edits to the knowledge file, the census tool, or any gate.

## Out of scope / limits
- Did not run C1/C2 measure.py (those runs are the designated executors' seats; kill rule forbids pre-deciding runs).
- No conflicts with peer claims observed from this seat; nothing to report verbatim to the judge beyond the citations above.
- No tool installs performed (pacman paused per lane bounds; none needed).
