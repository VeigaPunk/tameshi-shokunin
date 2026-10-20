# R01 — Case-8 acceptance review

Axes reviewed: **depth** (scored), with calibration evidence and operability/fixture integrity monitored. This is a read-only review; the only lane write is this report.

## Acceptance conditions and observations

| Condition | Evidence | Status at review |
|---|---|---|
| Pinned, in-province target | Kumitate rev `0acb7752d19058b953ebbeba253b1e35f6548de5` exists; `scripts/sources-check.mjs` is its last-touching file commit, mode `100755`, blob SHA-256 `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`; kumitate status was clean. `PROVINCE.md:7-11` includes `kumitate-shokunin/scripts/*`; `:61-62` already names `sources-check.mjs` as a kumitate gate. | Pass |
| Pre-registration committed before sweep | `93d22aa` at `2026-10-20T16:40:21-03:00` commits the spec, predictions, suite and control. Sweep receipt records that commit and `MUTATE_DATE: 2026-10-20T19:41:29Z` (`sweep/sweep.txt:1-10`): 19:40:21Z to 19:41:29Z, 68 seconds. | Pass |
| Prediction record and exact mutation anchors | Spec SHA-256 `c8d24cb4b6b1a372543764fc27c9d16f65510a29fed1045bedb2863ce2408c91` matches the committed spec and the current embedded heredoc. Independent count against the pinned target found all ten `@old` strings occur exactly once. `sweep/sweep.txt:120-131` reports `PREDICTION_MATCH: 10/10`; its table matches the current `TABLE_SOURCESCHECK` at staged runner `:620`. | Pass |
| Sweep result and restore proof | `sweep/sweep.txt:110-116` reports `MUTATE_RESTORE: OK`, before/after/pristine all `6a293a72…`, runner exit 0, and `MUTATE: DONE … defects=10 killed=5 survived=5 inconclusive=0`. | Pass; detailed per-mutant retention gap below |
| Determinism and environment handling | `control/repeat-hashes.json:14-24`: eight control runs, all exit 0, one stdout hash, one stderr hash, 6,274 stdout bytes and zero stderr bytes; `repeat/finding.txt:1-2` says `controls_match`, exit 0. `strace-summary.md:9-11` records zero reads under `~/Projects` and no observed external-network syscalls. `hazard-summary.md:7-8` records unchanged GIT_DIR canary and clean TMPDIR-in-worktree clone. | Pass |
| Survivor non-equivalence | I ran off-suite pristine-vs-mutant probes in my `/tmp/tameshi-r18w1-R01CaseAcceptance-zdNCNn` scratch against the pinned bytes, using each exact spec edit. Results are listed below. The lane's case entry still says no survivor witness is supplied and all five are `PENDING` (`mutation-case-kumitate-sources-check.md:150-163`). | Behavior independently demonstrated; durable case record pending |
| Regression and leg header | Current staged runner SHA `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b`: header at `:93` is `js-sources-check … 5/10`; exact spec embedded; suite call at `:1349-1352` matches `suite.txt`/`predictions.json`; tuple at `:1879` is `…:10:5`. In a `/tmp` fleet-mirror, `--selftest` returned 0 (`MUTATE_SELFTEST: 96/96 pass`) and `--regression` returned 0 (`REGRESSION: PASS (cases=8 passed=8…)`, leg-8 table `match=10/10`, flips 0). Regression tool hash printed as the same `d22c4025…`. | Pass on current staged bytes; not landed |
| Admitted knowledge/provenance record | A draft exists, but it is untracked. Its source header cites mined S001/S052/S056/S057, but also cites S008 as queued. Its own `:215-219` says S008 is not mined/used-by, the cited mined rows need this entry added to used-by, and the coverage-map/LOG entry is still owed. No `sources-check.mjs` row was found in `corpus/SOURCES.md`; `corpus/README.md:226` still lists case 7 only. | Not admitted / incomplete |

## Findings (severity order)

### High — the depth increase is not present at the committed tip

At current committed `HEAD=93d22aa`, command D still counts **7**, not 8. I ran the SCORECARD regex over `git show 93d22aa:tools/mutate-and-run.sh` and got `recorded_cases=7 depth_score=7`; the current staged runner counts 8. The case-8 runner edit remains under `.ufo/waves/round-18/staged/tools/mutate-and-run.sh`, and `git status --porcelain` shows it only within the untracked round-18 wave tree. The case entry also states that `git grep js-sources-check -- tools` finds no installed leg at `183f87b` or `93d22aa` (`mutation-case-kumitate-sources-check.md:174-183`).

This is the decisive boundary: SCORECARD defines depth as documented cases in the pinned replay ledger, not merely a successful scratch replay (`SCORECARD.md:66,72-76`); round 17 likewise counted the header regex and regression at the measured revision (`round-17-verifier-spotcheck.md:379`). My successful regression proves the current staged candidate, not an 8-case committed ledger. Until the L1 installs/commits the runner and rechecks the landing revision, C1 must not be reported as a committed 7→8 depth move.

### High — survivor evidence is still marked pending in the case record

The five predicted survivors are not equivalent on the observable CLI behavior I probed. Exact scratch probes (each compares the pinned pristine script with the one-edit mutant; both exit codes shown):

- `S_KIND`: `node <script> --help`, exit 0/0; the mutant's `findings:` usage line omits `RECHECK_OVERDUE` (`sources-check.mjs:108-115,117-130`).
- `S_VERDICT`: `node <script> --self <drift-fixture> --today 2026-10-19`, exit 1/1; final line changes from `SOURCES_CHECK: DRIFT (KIND_ENUM)` to `SOURCES_CHECK: DRIFT [KIND_ENUM]` (`:483-484`).
- `S_DUP_LINE`: same CLI with a duplicate-ID fixture, exit 1/1; `ID_DUPLICATE` location changes from `corpus/SOURCES.md:8` to `:9` (`:250`).
- `S_ENTRY_COUNT`: `node <script> --self <one-entry-fixture> --today 2026-10-19 --json`, exit 0/0; `counts.entriesWithSource` changes from 1 to 2 (`:365-368`).
- `S_FILE_READ`: one `.md` knowledge file chmod 000 (probe EUID 1000), same CLI, exit 2/2; pristine reports `FAIL-CLOSED (READ_FAILED)` / `EACCES`, mutant reports `FAIL-CLOSED (SOURCES_MISSING)` / `EACCES` (`:352-356`).

Thus the witnesses exist in this reviewer report, but not in lane evidence: the draft explicitly labels every survivor `PENDING` and says none is supplied (`mutation-case-kumitate-sources-check.md:150-163`). Carry these outputs into the durable case evidence/entry before treating the survivor condition as closed. Round 16 used either an off-suite witness or an explicit equivalence argument for each survivor (`mutation-case-kumitate-round-gate.md:98-115`).

### Medium — draft entry and registry/index obligations prevent admission

The untracked case entry has the required `source:` header and cites several mined rows, but the entry itself records outstanding source-registry work: S008 is queued with `used-by —`, and S001/S052/S056/S057 need this knowledge path added to `used-by`; it also says the coverage-map row and LOG entry remain owed (`mutation-case-kumitate-sources-check.md:1-3,215-219`). The source header's inline target pin is not a mined `SOURCES.md` row for the target artifact; a literal search of `corpus/SOURCES.md` for `sources-check.mjs`/`0acb7752` returned no match. README still has only the case-7 row (`corpus/README.md:226`). This is not yet an admitted, source-headed knowledge entry under the frontier rule (`PROVINCE.md:40-42`), even though the draft contains mined source IDs.

### Medium — the lane sweep retains only summarized tails, not the per-mutant receipts

The lane evidence directory contains `sweep/sweep.txt`, while the sweep itself reports `MUTATE_EVIDENCE` at a temporary `/tmp` path (`sweep/sweep.txt:111`; case entry `:107-115`). The entry notes that per-check attribution is absent for K_KIND, K_STRICT and K_CLOSED, so the predicted selftest case for those kills is not established by the retained sweep output (`:107-118`). I independently ran each killed mutant's `--selftest` in scratch: K_KIND failed the named TIER_ENUM fixture (plus two related checks), K_EXIT failed both exit-64 checks, K_STRICT failed the strict-warning check, K_CLOSED failed the SOURCES_MISSING arm and fail-closed coverage check, and K_ROWS failed the row-count/parity checks. This supports the intended predictions, but those per-check runs are not durable lane receipts. Retain sufficient output at the lane path before relying on the case as a fully auditable record.

## Residual risks and verification gaps

- `PROVINCE.md:51-57` still records seven legs; it needs an append-only update when case 8 lands. Its existing note at `:61-62` that sources-check is a kumitate gate establishes target scope, not an eighth admitted leg.
- The current runner header and the SCORECARD count are syntax-based. During integration I observed an earlier staged snapshot with `0/10 (PLACEHOLDER)`; command D still counted that header as case 8. Current staged bytes now have the real `5/10` table, exact pre-registered spec, exact suite and no placeholder tokens. This is why the pre-registration/result/table comparisons—not the count alone—are necessary.
- The L1 check receipt itself does not name the runner SHA, as the case draft notes at `:178-183`; my independent current-stage run binds the pass to SHA `d22c4025…`, but the installed runner still needs its own hash-bound receipt.
- No `lsp` device was exposed in the mounted tool inventory. Literal text searches were used only for literal absence checks; code behavior above is supported by direct source reads and the described executions, not by grep as semantic proof.

**Verdict: partial — pre-registration, sweep, determinism, exact staged embedding and current staged regression pass; the committed depth ledger and admitted knowledge record are still pending.**