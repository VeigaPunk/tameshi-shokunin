# SHONEN evidence — round-12 w2 (TameshiR12.SHONENEvidence)

Read-only leaf report. Advisory lane-local observation; no independent promotion or discernment authority is claimed. No `[x]` is asserted. No tools installed or updated. No edits made outside this file.

## Four report lines

Live `SHONEN.md` (blob matches HEAD `18ad5d0`, no working-tree diff) carries `[~]` on all four boxes. Pointers below are lane-local.

- Box 1 (SKILL decision tables, error patterns, checklists, cited sources): [~] — `SHONEN.md:5-6`; audit `reports/round-1-calibration.md:71-103` (`## box-1`).
- Box 2 (end-to-end domain task logged in LOG.md): [~] — `SHONEN.md:7-8`; audit `reports/round-1-calibration.md:105-130` (`## box-2`); `corpus/knowledge/mutation-case-kagi-census.md` present; `LOG.md:277-298` cited by the audit (sampled, not re-read line by line here).
- Box 3 (executable without oral context): [~] as the live mark, scope-bounded and unscored — `SHONEN.md:9-10`; `reports/round-1-kaika-coldread.md` (`COLDREAD: SUFFICIENT`, line 273). Conflicting in-repo marks recorded in Finding 1.
- Box 4 (no cross-domain bleed / PROVINCE accurate): [~] — `SHONEN.md:11-12`; audit `reports/round-1-calibration.md:167-200` (`## box-4`); `PROVINCE.md:22-47` (Core/Frontier/Adjacent append).

## Findings (path:line)

1. **Box 3 mark conflict (unresolved in repo).** Live `SHONEN.md:9` = `[~]`. Latest adjudication `SCORECARD.md:209-217` says box 3 "stays `[~]` as a scope-noted lane assertion" and is unscored. Contradicting records:
   - `reports/round-1-calibration.md:159-165` and the disposition table `:208` = `[ ]` (assertion rejected).
   - `SCORECARD.md:98-99` candidate row = `[~], [~], [ ], [~]`.
   - `.ufo/evidence/fleet-round-1/calibration-acceptance.json` candidate marks `["~","~"," ","~"]`.
   - `LOG.md:575` records "SHONEN box 3 `[ ]` → `[~]`", while `corpus/lessons/round-1-verifier-spotcheck.md:17` records the box-3 increment as not credited.
   - `measure.py` (round-12) excludes box 3 from scoring (`scored_boxes = (1, 2, 4)`).
   Integrator must reconcile; this lane does not pick one.

2. **Canonical geometry holds.** Title `SHONEN.md:1`, preamble `:3`, four rows in canonical order `:5,7,9,11` with canonical wording, one indented evidence line per box (`:6,8,10,12`). Canonical seed = `kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:455-462`, marks spec `:464-465`.

3. **Stale sibling line pins.** `reports/round-1-calibration.md:14-22` and `SHONEN`-adjacent audit cites `PROTOCOL.md:413, 419-431` and `:63-68`. In the current sibling file the seed is at `:453-462` and the marks spec at `:464-465`; "Promotion gates" starts at `:59`. The pins are stale by about 34 lines (sibling-repo read-only; not fixed here).

4. **Box 3 evidence line is long but in-scope.** `SHONEN.md:10` discloses scope (Appendix A+B sweep only, probes reconstructed, lane-dispatched seat, no independent verifier). Its scope exclusions match `corpus/knowledge/executor-test-sufficiency.md:160-184` (full sweep, survivor probes, Appendix B and a second executor remain unproven). `corpus/lessons/round-1-verifier-spotcheck.md:17` debt: "box 3 needs a fresh reader".

5. **Historical four-`[x]` record preserved.** Baseline `git show 284ab0f:SHONEN.md:5-34` is all `[x]`; superseded by `reports/round-1-calibration.md:45-69`. Not editable here.

6. **Round-12 posture consistent.** `corpus/lessons/round-12.md:24` and `:38` state no `[x]` is earned and outside admit/reject spot-check remains pending. `.ufo/waves/round-12/w2/swarm-registry.json` lists this seat with no conflicting claim.

## Limits

- Pointers resolved by path and anchor (`reports/round-1-calibration.md` `## box-1..4` exist at `:71,105,132,167`; `reports/round-1-kaika-coldread.md` exists). Cited sub-ranges (e.g., `LOG.md:277-298`, `corpus/knowledge/mutation-case-kagi-census.md:1-17`) were not verified line-by-line.
- Working tree: `LOG.md`, `corpus/SOURCES.md`, `corpus/knowledge/witness-scoped-kill-verdict.md` modified; `SHONEN.md` unmodified.
- No builds, tests, or CLI runs performed (not assigned).
- Owned path written: `.ufo/waves/round-12/w2/SHONENEvidence.md` only.
