# Tameshi R16 wave 1: seat count, role mix, completion

Lane: tameshi-shokunin. Lane HEAD at check time: `c699c8c`. Scope: wave-1 artifacts under `.ufo/waves/round-16/` (spec1, dispatch1, spawn1, record1, w1/swarm-registry.json). Seat reports read for presence, size, tail and JSON fence only; report content was not adjudicated.

**Verdict:** holds. Wave 1 is 68 seats in every artifact (spec, dispatch, spawn, registry, record). All 68 report files exist, are non-empty, and end cleanly. All 30 cold-read seats carry a parseable JSON block. No seat is recorded as dead or errored. Two caveats: the registry has no per-seat status field, so completion is inferred from report files; and one wave-1 report (Overlap1) differs from its commit.

## 1. Counts (evidence)

| Artifact | Count | Command and key output |
|---|---|---|
| spec1.json `.items` | 68 | `jq '.items \| length' spec1.json` → `68` (exit 0) |
| dispatch1.json `.counts` | spawn 68, resume 0, total 68 | `jq -c '.counts' dispatch1.json` → `{"spawn":68,"resume":0,"total":68}` (exit 0) |
| dispatch1.json `.taskCall.tasks` | 68 | `jq '.taskCall.tasks \| length'` → `68` (exit 0) |
| spawn1.json text | "Spawned 68 background agents" | `grep -o -E 'Spawned [0-9]+ background agents'` → `Spawned 68 background agents` (exit 0) |
| w1/swarm-registry.json `.members` | 68, all `kind=spawn` | `jq '.members\|length'` → `68`; kind counts `spawn=68` |
| record1.json `.members` | 68 | identical to registry `.members` (`cmp` of `jq -S '.members'` exit 0, `RECORD1_EQ_REGISTRY_MEMBERS`) |
| w1/*.md seat reports | 68 | `ls w1/ \| grep '\.md$' \| wc -l` = 68; `comm` against spec names: no extra files |

Name-set and role cross-checks (all exit 0):
- spec names = registry keys = dispatch task names (`diff` silent, `SAME_NAMES`, `DISPATCH_NAMES_EQ_SPEC`).
- spec `role` = registry `role` for all 68 (`diff`, `SAME_ROLES`).
- Dispatch `registry.members` shows `agentId: null` (pre-spawn plan). The post-spawn registry shows `agentId: "TameshiR16.<key>"`. This is the expected pre/post difference, not a mismatch.
- Compaction: `applied: false`, all saved bytes 0 (dispatch1.json).

## 2. Role mix (registry `.members`, 68 seats)

| Role | Count | Seats |
|---|---|---|
| executor | 25 | CR04a, CR04b, CR07, CR09, CR11a, CR11b, CR12a, CR12b, CR13, CR16, CR18, CR22, CR24, CR25, CR26, CR27, RGSpecA, RGSpecB, RGSpecC, RGSpecD, RGSpecE, RGLeg, CRMeasure, CRLedger, AttrFix |
| scout | 14 | CR03, CR06, CR08, CR15, CR19, CR20, CR23, RGRecon, RGControl, RGMatrix, RGSource1, CRSource, AttrRecon, FrontierMap |
| reviewer | 10 | CR01, CR02, CR05, CR10, CR14, CR17, CR21, ProvinceBox4, QualityAudit, RoutedDisposition |
| scribe | 5 | RGSource2, CRSource2, MistakeScribe, PITSource, SurveySource |
| connector | 4 | RGConnector, Overlap1, Overlap2, PlannerWalk |
| critic | 4 | RGCritic, CRCritic1, CRCritic2, AttrCritic |
| revenger | 4 | RGPriorCase, CRRevenger, Misroot, SurvivorPrep |
| sentinel | 2 | RGSentinel, CRSentinel |
| **Total** | **68** | sum 25+14+10+5+4+4+4+2 = 68 |

Command: `jq -r '.members \| to_entries \| group_by(.value.role) \| map(...)' w1/swarm-registry.json` (exit 0). Role lists were checked by hand against the same output.

## 3. Completion and death

- **Report presence:** 68/68 present and non-empty (`[ -s "$p" ]` loop over paths extracted from each spec prompt's "Write your report at …" sentence; `NOPATH` count 0; all `OK`).
- **Tails:** every report's last non-blank line is a sentence, bullet or closing fence. None ends mid-token. Shortest is AttrFix (46 lines); longest is CRRevenger (570 lines). See table below.
- **Cold-read JSON (30 seats CR01–CR27, incl. a/b splits):** each has one ```json fence; every block parses with `jq -e '.seat'`. Non-cold-read `CR*` files: CRCritic1, CRCritic2, CRLedger, CRMeasure, CRRevenger, CRSentinel, CRSource, CRSource2 (no JSON required).
- **Dead or errored:** spawn1.json has 0 spawn failures (`grep -o -i -E 'failed to spawn|spawn fail|could not spawn'` → 0 hits). The `KILLED`/`ERROR` strings in spawn1 are prompt text (mutation-prediction wording, `INTERNAL_ERROR`, `usage_error` fixtures), not seat states. No seat is marked dead, killed or errored in any artifact.
- **Inference:** the registry has no status field, so "completed" = report file present, non-empty, ends cleanly, and (for cold-read seats) carries a parseable JSON block. This is a file-level check; the content was not verified.

## 4. Caveats

1. **Drift:** `Overlap1.md` is modified in the working tree and not committed. `git diff --stat` shows `2 insertions(+)`, and the file is 27183 bytes against 26765 at HEAD. The appended erratum is dated 2026-10-20. The wave-1 Overlap1 content at HEAD is therefore not the content on disk. I did not verify the erratum's correctness.
2. **Seat-id naming in cold-read JSON:** the `seat` field is not uniform. Ten seats use `TameshiR16.CRxx` (CR01, CR03, CR06, CR08, CR10, CR14, CR19, CR20, CR22, CR23) and twenty use bare `CRxx`. The spec's interface does not fix the form. Relevant to the ledger assembler that keys on `seat`.
3. **Timestamps:** registry `createdAt` 2026-10-20T13:23:43Z (10:23 −03), `updatedAt` 13:25:33Z (10:25 −03). Report and registry mtimes are all 10:39:59 −03, consistent with a bulk materialization after the registry was written. Inference, not verified.
4. **`w2/swarm-registry.json`** belongs to the wave-2 dispatch and was not read or modified by this check.

## 5. Seat table (68 rows)

Report path = `.ufo/waves/round-16/w1/<seat>.md` (lane-relative). Lines = `wc -l`. JSON = cold-read JSON block parses (cold-read seats only).

| # | Seat | Role | Registry agentId | Report (lane-relative) | Lines | JSON |
|---|---|---|---|---|---|---|
| 1 | CR01 | reviewer | TameshiR16.CR01 | .ufo/waves/round-16/w1/CR01.md | 301 | yes |
| 2 | CR02 | reviewer | TameshiR16.CR02 | .ufo/waves/round-16/w1/CR02.md | 182 | yes |
| 3 | CR03 | scout | TameshiR16.CR03 | .ufo/waves/round-16/w1/CR03.md | 188 | yes |
| 4 | CR04a | executor | TameshiR16.CR04a | .ufo/waves/round-16/w1/CR04a.md | 134 | yes |
| 5 | CR04b | executor | TameshiR16.CR04b | .ufo/waves/round-16/w1/CR04b.md | 165 | yes |
| 6 | CR05 | reviewer | TameshiR16.CR05 | .ufo/waves/round-16/w1/CR05.md | 269 | yes |
| 7 | CR06 | scout | TameshiR16.CR06 | .ufo/waves/round-16/w1/CR06.md | 144 | yes |
| 8 | CR07 | executor | TameshiR16.CR07 | .ufo/waves/round-16/w1/CR07.md | 92 | yes |
| 9 | CR08 | scout | TameshiR16.CR08 | .ufo/waves/round-16/w1/CR08.md | 101 | yes |
| 10 | CR09 | executor | TameshiR16.CR09 | .ufo/waves/round-16/w1/CR09.md | 73 | yes |
| 11 | CR10 | reviewer | TameshiR16.CR10 | .ufo/waves/round-16/w1/CR10.md | 158 | yes |
| 12 | CR11a | executor | TameshiR16.CR11a | .ufo/waves/round-16/w1/CR11a.md | 81 | yes |
| 13 | CR11b | executor | TameshiR16.CR11b | .ufo/waves/round-16/w1/CR11b.md | 113 | yes |
| 14 | CR12a | executor | TameshiR16.CR12a | .ufo/waves/round-16/w1/CR12a.md | 68 | yes |
| 15 | CR12b | executor | TameshiR16.CR12b | .ufo/waves/round-16/w1/CR12b.md | 162 | yes |
| 16 | CR13 | executor | TameshiR16.CR13 | .ufo/waves/round-16/w1/CR13.md | 79 | yes |
| 17 | CR14 | reviewer | TameshiR16.CR14 | .ufo/waves/round-16/w1/CR14.md | 347 | yes |
| 18 | CR15 | scout | TameshiR16.CR15 | .ufo/waves/round-16/w1/CR15.md | 145 | yes |
| 19 | CR16 | executor | TameshiR16.CR16 | .ufo/waves/round-16/w1/CR16.md | 91 | yes |
| 20 | CR17 | reviewer | TameshiR16.CR17 | .ufo/waves/round-16/w1/CR17.md | 211 | yes |
| 21 | CR18 | executor | TameshiR16.CR18 | .ufo/waves/round-16/w1/CR18.md | 107 | yes |
| 22 | CR19 | scout | TameshiR16.CR19 | .ufo/waves/round-16/w1/CR19.md | 145 | yes |
| 23 | CR20 | scout | TameshiR16.CR20 | .ufo/waves/round-16/w1/CR20.md | 212 | yes |
| 24 | CR21 | reviewer | TameshiR16.CR21 | .ufo/waves/round-16/w1/CR21.md | 143 | yes |
| 25 | CR22 | executor | TameshiR16.CR22 | .ufo/waves/round-16/w1/CR22.md | 63 | yes |
| 26 | CR23 | scout | TameshiR16.CR23 | .ufo/waves/round-16/w1/CR23.md | 158 | yes |
| 27 | CR24 | executor | TameshiR16.CR24 | .ufo/waves/round-16/w1/CR24.md | 95 | yes |
| 28 | CR25 | executor | TameshiR16.CR25 | .ufo/waves/round-16/w1/CR25.md | 113 | yes |
| 29 | CR26 | executor | TameshiR16.CR26 | .ufo/waves/round-16/w1/CR26.md | 93 | yes |
| 30 | CR27 | executor | TameshiR16.CR27 | .ufo/waves/round-16/w1/CR27.md | 103 | yes |
| 31 | RGSpecA | executor | TameshiR16.RGSpecA | .ufo/waves/round-16/w1/RGSpecA.md | 90 | — |
| 32 | RGSpecB | executor | TameshiR16.RGSpecB | .ufo/waves/round-16/w1/RGSpecB.md | 109 | — |
| 33 | RGSpecC | executor | TameshiR16.RGSpecC | .ufo/waves/round-16/w1/RGSpecC.md | 122 | — |
| 34 | RGSpecD | executor | TameshiR16.RGSpecD | .ufo/waves/round-16/w1/RGSpecD.md | 92 | — |
| 35 | RGSpecE | executor | TameshiR16.RGSpecE | .ufo/waves/round-16/w1/RGSpecE.md | 95 | — |
| 36 | RGRecon | scout | TameshiR16.RGRecon | .ufo/waves/round-16/w1/RGRecon.md | 292 | — |
| 37 | RGControl | scout | TameshiR16.RGControl | .ufo/waves/round-16/w1/RGControl.md | 159 | — |
| 38 | RGMatrix | scout | TameshiR16.RGMatrix | .ufo/waves/round-16/w1/RGMatrix.md | 241 | — |
| 39 | RGPriorCase | revenger | TameshiR16.RGPriorCase | .ufo/waves/round-16/w1/RGPriorCase.md | 297 | — |
| 40 | RGLeg | executor | TameshiR16.RGLeg | .ufo/waves/round-16/w1/RGLeg.md | 113 | — |
| 41 | RGSource1 | scout | TameshiR16.RGSource1 | .ufo/waves/round-16/w1/RGSource1.md | 220 | — |
| 42 | RGSource2 | scribe | TameshiR16.RGSource2 | .ufo/waves/round-16/w1/RGSource2.md | 54 | — |
| 43 | RGCritic | critic | TameshiR16.RGCritic | .ufo/waves/round-16/w1/RGCritic.md | 91 | — |
| 44 | RGSentinel | sentinel | TameshiR16.RGSentinel | .ufo/waves/round-16/w1/RGSentinel.md | 150 | — |
| 45 | RGConnector | connector | TameshiR16.RGConnector | .ufo/waves/round-16/w1/RGConnector.md | 261 | — |
| 46 | CRSource | scout | TameshiR16.CRSource | .ufo/waves/round-16/w1/CRSource.md | 167 | — |
| 47 | CRSource2 | scribe | TameshiR16.CRSource2 | .ufo/waves/round-16/w1/CRSource2.md | 94 | — |
| 48 | CRMeasure | executor | TameshiR16.CRMeasure | .ufo/waves/round-16/w1/CRMeasure.md | 99 | — |
| 49 | CRLedger | executor | TameshiR16.CRLedger | .ufo/waves/round-16/w1/CRLedger.md | 103 | — |
| 50 | CRCritic1 | critic | TameshiR16.CRCritic1 | .ufo/waves/round-16/w1/CRCritic1.md | 212 | — |
| 51 | CRCritic2 | critic | TameshiR16.CRCritic2 | .ufo/waves/round-16/w1/CRCritic2.md | 240 | — |
| 52 | CRRevenger | revenger | TameshiR16.CRRevenger | .ufo/waves/round-16/w1/CRRevenger.md | 570 | — |
| 53 | CRSentinel | sentinel | TameshiR16.CRSentinel | .ufo/waves/round-16/w1/CRSentinel.md | 279 | — |
| 54 | AttrRecon | scout | TameshiR16.AttrRecon | .ufo/waves/round-16/w1/AttrRecon.md | 250 | — |
| 55 | AttrFix | executor | TameshiR16.AttrFix | .ufo/waves/round-16/w1/AttrFix.md | 46 | — |
| 56 | AttrCritic | critic | TameshiR16.AttrCritic | .ufo/waves/round-16/w1/AttrCritic.md | 164 | — |
| 57 | Overlap1 | connector | TameshiR16.Overlap1 | .ufo/waves/round-16/w1/Overlap1.md | 219 | — |
| 58 | Overlap2 | connector | TameshiR16.Overlap2 | .ufo/waves/round-16/w1/Overlap2.md | 230 | — |
| 59 | PlannerWalk | connector | TameshiR16.PlannerWalk | .ufo/waves/round-16/w1/PlannerWalk.md | 290 | — |
| 60 | Misroot | revenger | TameshiR16.Misroot | .ufo/waves/round-16/w1/Misroot.md | 309 | — |
| 61 | FrontierMap | scout | TameshiR16.FrontierMap | .ufo/waves/round-16/w1/FrontierMap.md | 189 | — |
| 62 | ProvinceBox4 | reviewer | TameshiR16.ProvinceBox4 | .ufo/waves/round-16/w1/ProvinceBox4.md | 245 | — |
| 63 | QualityAudit | reviewer | TameshiR16.QualityAudit | .ufo/waves/round-16/w1/QualityAudit.md | 280 | — |
| 64 | RoutedDisposition | reviewer | TameshiR16.RoutedDisposition | .ufo/waves/round-16/w1/RoutedDisposition.md | 79 | — |
| 65 | SurvivorPrep | revenger | TameshiR16.SurvivorPrep | .ufo/waves/round-16/w1/SurvivorPrep.md | 310 | — |
| 66 | MistakeScribe | scribe | TameshiR16.MistakeScribe | .ufo/waves/round-16/w1/MistakeScribe.md | 95 | — |
| 67 | PITSource | scribe | TameshiR16.PITSource | .ufo/waves/round-16/w1/PITSource.md | 129 | — |
| 68 | SurveySource | scribe | TameshiR16.SurveySource | .ufo/waves/round-16/w1/SurveySource.md | 85 | — |

Registry agentId check: `jq -r '.members | to_entries[] | select(.value.agentId != ("TameshiR16." + .key))' w1/swarm-registry.json | wc -l` → `0`. All 68 registry agentIds equal `TameshiR16.<key>`; rows 1–68 show those values.

## 6. Commands run

All exits 0 unless stated. Scratch: `/tmp/tameshi-r16w2-WaveCounts-yhPyQh/`.
- `git --no-optional-locks -C <lane> rev-parse --short HEAD` → `c699c8c`
- `git --no-optional-locks -C <lane> status --porcelain -- .ufo/waves/round-16` → `M w1/Overlap1.md`; `??` for assignments2, dispatch2, record2, spawn2, spec2, w2/
- `jq` (already installed at `/home/vgpnk/.local/bin/jq`; no install or upgrade performed)
- `jq -r '.items[] | …' spec1.json`; `jq -r '.members | to_entries[] | …' w1/swarm-registry.json`; `cmp <(jq -S '.members' record1.json) <(jq -S '.members' w1/swarm-registry.json)`
- Report presence loop over `spec_reports.tsv` (`[ -s "$p" ]`), tail loop (`grep -v '^[[:space:]]*$' | tail -n 1`), cold-read JSON extraction (`awk` fence extract + `jq -e '.seat'`)
- `git show HEAD:.ufo/waves/round-16/w1/Overlap1.md | wc -c` → 26765; `wc -c` working → 27183; `git diff --stat` → `2 insertions(+)`

## 7. Installs or updates

None. `jq` already present; no pacman transaction; no sibling repo written; no file written except this report.
