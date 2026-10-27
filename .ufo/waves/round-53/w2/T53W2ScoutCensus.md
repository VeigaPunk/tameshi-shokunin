# T53W2ScoutCensus — wave-2 scout census report

Seat: T53W2ScoutCensus (wave 2 of 2, tameshi round 53 / hyaku run 10)
Scope: read-only census + C** spot-checks; no edits outside this report.
C** = 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e (all file checks via `git show C**:<path>` / `git cat-file`, never the working tree).

## Item 1 — sources-census.sh validate

Command (as assigned):

```
TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

Result: **exit 0** (census terminal line `ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`).

Row-count cross-check via the `census` subcommand: `tameshi rows 136` — matches the expected 136.

Validate output class tally:

- 15 × W04 (duplicate-url-across-scopes): S047, S048, S075, S076, S077, S078, S081, S092, S104, S160, S265, S266, S267, S268, S274 — all of the "duplicate url … across scopes" shape; none fail validation. **HOLDS** ("only known W04s").
- 1 × W01: `S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md` — emitted by the tool's own W01-tierC-mined rule (script self-test `check "W01-tierC-mined"` confirms this class is an expected, non-failing warning). Observed; not a failure, not a W04.
- 1 × ok (file receipt).

No unknown statuses, no exit failure. **HOLDS.**

## Item 2 — corpus/SOURCES.md at C** carries S275/S276

`git -C … show C**:corpus/SOURCES.md`:

- Line 150: `| S275 | Change-Aware Mutation Testing for Evolving Systems (Ojdanić et al.; ESEC/FSE 2022, camera-ready) — https://doi.org/10.1145/3540250.3558911 | paper | A | … | mined | 2026-10-27 | 365d | corpus/knowledge/change-aware-resweep-cadence.md |`
- Line 151: `| S276 | Keeping Mutation Test Suites Consistent and Relevant with Long-Standing Mutants (Ojdanić, Papadakis, Harman; arXiv 2212.11762) — https://arxiv.org/abs/2212.11762 | paper | A | … | mined | 2026-10-27 | 365d | corpus/knowledge/change-aware-resweep-cadence.md |`

- 11-column shape: both rows split to 11 fields, matching the registry header `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`. **HOLDS.**
- used-by cells: both name exactly `corpus/knowledge/change-aware-resweep-cadence.md`. **HOLDS.**
- Both rows tier A, status `mined`, opened 2026-10-27, recheck 365d.
- Footer is not stale: the round-52 historical line reads "Next unused id: S275"; the round-53 line then adds S275–S276 and corrects to "Next unused id: S277 (staged ids S161-S255 stay reserved by document for the package)." The earlier `S275` line is an explicitly historical per-round receipt (same pattern as the round-48 correction note). **HOLDS** per finding discipline (dated historical milestones are HOLDS).

## Item 3 — corpus/knowledge/change-aware-resweep-cadence.md at C**

`git cat-file -e C**:corpus/knowledge/change-aware-resweep-cadence.md` → EXISTS; content read at C**.

- Front-matter source citations: exactly two — `source: S275 — https://doi.org/10.1145/3540250.3558911 — §3.2 … §3.3 …` and `source: S276 — https://arxiv.org/abs/2212.11762 — §Abstract …`. **Cites exactly S275/S276. HOLDS.**
- Quotes carried in the body match the rows' `teaches` cells (≈93% reduction / 52% of 143,500 mutants degrade).
- Other S-mentions are context, not source citations: one cross-reference to S101 (the lane's existing pin-level cadence under F7) and the round-53 adoption note mentioning staged S161/S162/S255 as explicitly historical staged ids (staged ids "stay reserved by document"). Per finding discipline, dated historical/adoption notes are HOLDS, not findings.
- Recheck line `recheck: 365d` matches the rows; `verified-at: 2026-10-27`.

## Findings

None.

## Notes (observed, non-finding)

- Validate prints one W01 (S101) in addition to the W04 set; the tool's own self-test pins this class as expected and non-failing. Recorded so the wave ledger is not surprised by the extra line.
- Registry shape at C**: 136 rows = 121 tier.A + 12 tier.B + 3 tier.C; status 109 mined / 21 queued / 6 rejected; tier.invalid 0; FLEET.missing 0.

## Hygiene

- Read-only over the lane and fleet; only this report written (under `.ufo/waves/round-53/w2/`).
- No scratch tree created (no fixture/mutant work); the single temp extraction `/tmp/SOURCES_at_Cstarstar.md` (< 50 MB) was deleted after use. No leftovers.
- No installs this seat.
