# SHONENReview — four-box assertions vs C1/C2 scope (tameshi-r12-w1)

- Seat: `SHONENReview` (reviewer, leaf, read-only). Author of this file is a lane-internal seat: every line below is advisory, NOT independent non-author promotion or admission authority (PROTOCOL.md:63–68).
- Scope: assess the unchanged four `[~]` assertions in `SHONEN.md` against the round-12 claims C1 (repeat-control calibration) and C2 (declared-witness split for the pinned bash surface-census). No mark edits, no edits to any file other than this report, no build/lint/test runs.
- Snapshot: observed 2026-10-19 during the wave. Sibling seats were writing `.ufo/evidence/round-12/*` and `corpus/` concurrently; findings reflect that moment only.
- Tooling: no tool installed or updated by this seat (none needed; read-only `sha256sum`, `grep`, `sed`, `git show` on sibling pinned blobs).

## 1. Axes named

| Axis | Current pinned state | What C1/C2 can change |
|---|---|---|
| calibration (restraint of `[~]`) | 6 pinned (`LOG.md` fleet round 1 post-review: "re-pinned 6 without box 3"); box 3 unscored | C1 adds control-determinism evidence for the cold-read's control step; it adds no mark and no points by itself |
| depth (recorded cases) | 6 (command D) | C2 is a reanalysis of an existing bash leg; it does not add a seventh gate and does not add a recorded case |

No move on either axis is proposed here that harms another axis.

## 2. Current assertions (verified bytes)

`SHONEN.md` (repo HEAD `18ad5d0`, file last changed `121696b`): four `[~]`, zero `[x]`.

- Seed check: header and the four box texts are byte-identical to the canonical seed in `kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:455–462` after normalizing the mark character and dropping the evidence lines. Checked with `/tmp` scratch, removed after use. SEED-MATCH.
- Box 1 pointer `reports/round-1-calibration.md#box-1`; box 2 `#box-2`; box 3 `reports/round-1-kaika-coldread.md`; box 4 `#box-4`. All anchors resolve.
- `SKILL.md` sha256 = `33e3009c919cd0fb0b2c67bbd7927655289450750f4f69d9ca86758d81000f81` (unchanged; the kaika cold-read binds to these bytes).
- Cold-read copies under `.ufo/evidence/kaika-round-1/coldread/` match `SHA256SUMS.txt` for A-control, B-control, spec-B, appendixB/B4.out, both results.tsv.
- Witness evidence: `declared.tsv` sha `32241b02…` and `js-kimi-census.spec` sha `51fa6466…` match the README.
- Pinned bash gate: `git -C ../kagi-shokunin show fecee874:corpus/surface-census.sh` sha256 = `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` (matches the pin in SKILL and kagi notes).
- `tools/mutate-and-run.sh` sha256 = `75ed934d…` (matches the recorded runner).

## 3. Per-box assessment against C1/C2

### Box 1 — SKILL decision tables, error patterns, checklists, cited sources — `[~]`
- C1: no effect.
- C2: no effect unless `SKILL.md` is edited. Any edit moves the bytes that box 1's line anchors (`SKILL.md:58–92`, `:466–495`, `:497–525`) and box 3's cold-read both bind to.
- Recommendation: keep `[~]`. No `SKILL.md` edit in this round. A C2 "witness case(s)" field proposal (kaika witness README, "recipe step 7") must land in `corpus/` only.

### Box 2 — end-to-end domain task executed and logged — `[~]`
- Evidence today: the kagi `surface-census.sh` mutation sweep (`corpus/knowledge/mutation-case-kagi-census.md`, `LOG.md` round-3 entry around lines 277–298).
- C1: its N≥3 control repeats are calibration evidence for the control step only. They are not a new end-to-end task and must not be cited as box-2 evidence.
- C2: re-analysis of the same bash leg already counted in the six recorded legs. Under the round-12 contract it is NOT a seventh gate and must not be cited as an additional independent run or task.
- Recommendation: keep `[~]`. Cite any C2 output as "reanalysis of the recorded bash leg" in its own entry only.

### Box 3 — instructions executable without oral context — `[~]` (scope-bounded: Appendix A + B only)
This is the box the round-12 claims touch most.

- C1 relevance: the cold-read's control step (SKILL:138–148) was run once per appendix (`A-control.txt`, `B-control.txt`). N=1 each. A C1 run would be the first repeat of those controls. Notes:
  - `B-control.txt` shows `substrate-absent` skip arms (`verbs-sandboxed`, `verbs-break-injection`) and the selftest reads PATH and `SQLITE3_BIN` (`corpus/knowledge/gates-survey-kagi.md` ~:55; pinned gate ~:692–842). Identical bytes on one host say nothing about cross-host or PATH-varied stability (kaika `U(a)`).
  - C1 identity is per-run; a pass cannot retroactively upgrade box 3's scope.
- C2 relevance: the Appendix B step 8 cell is `ADDITIVE-IMPROVISATION` (B-probe fixtures reconstructed from a contamination-flagged note). A witness split would be the first witness-level evidence for Appendix B, but it cannot widen box 3 to full-sweep or Appendix-A-independent claims (MK-10 overreach; SKILL:14–16 says "current full-sweep/bash sufficiency remains unverified").
- Contamination risk for C2 declarations (blocking if ignored): the page's expected-results table `SKILL.md:652–663` and `corpus/knowledge/mutation-case-kagi-census.md` list the failing case per defect (B1→05, B4→07 token-only, B7→10 tripwire, etc.). Declarations copied from those are post-hoc and not a witness split. The JS witness itself was declared "partly contaminated" (`witness/README.md`, erratum E1), so that precedent applies.
- Recommendation: keep `[~]` with the existing scope note. Do not widen. No `[x]`.

### Box 4 — no cross-domain bleed, PROVINCE accurate — `[~]`
- C1/C2 risk: both run sibling-pinned gate code. The `repeat-control` command form executes an arbitrary argv. A run in a sibling working tree could write there (PROVINCE.md:16–17 forbids editing sibling gates).
- Observed: during the kaika cold-read the kumitate worktree was dirtied by a foreign in-flight edit at `2026-10-19T22:06:51Z` (`coldread` O4), which the lane did not cause. Box 4 wording must therefore say "this lane did not modify" and never "sibling tree clean".
- Frontier: PROVINCE.md:40–42 moves F3 (C1 topic) to Core only through a knowledge entry citing a mined `SOURCES.md` row. Current statuses: S004 mined, S026 mined, S006 mined; S011, S025, S027, S040 are **queued** (`corpus/SOURCES.md`). F3 must stay Frontier until its cited rows are mined.
- Recommendation: keep `[~]`. C1/C2 runs use materialized blobs in scratch (the witness experiment's pattern) or the `--snapshot` path, and record `git -C <sibling> status --porcelain` before and after.

## 4. Stale in-repo statements (not fixed here; need L1 decision)

These contradict each other or the bytes. None are marks. Fixing any `SKILL.md` line changes the cold-read-bound bytes, so the safe path is append-only errata in `LOG.md` or the calibration report, or a new cold read.

1. `SKILL.md:1464–1476` ("Promotion-evidence calibration — fleet round-1") says "Box 3 remains `[ ]`". `SHONEN.md:9` says `[~]` (scope-bounded). `LOG.md` post-review adjudication says box 3 "stays `[~]` with its scope note, unscored". The in-page section is stale.
2. `SKILL.md:12–16` preamble: "current full-sweep/bash sufficiency remains unverified". The kaika Appendix B cold-read records SUFFICIENT for Appendix B. Consistent only if read as "full sweep" alone; the sentence as written reads "bash sufficiency". Flag.
3. `LOG.md` (fleet round-1 phase-2 corrections entry) says "`SKILL.md:14-15`/`:133-135` marked stale". The bytes carry no stale marker: `grep -i stale SKILL.md` finds none in those ranges, and `sha256` is unchanged. The log claim is not reflected in the file.
4. `reports/round-1-calibration.md` box-3 row and prose still say `[ ]` and "Box 3's two points … remain unearned". The LOG adjudication supersedes this; the report was not updated.
5. Citation drift in `reports/round-1-calibration.md` (MK-1 class). Current protocol locations: seed `PROTOCOL.md:455–462` (cited 419–428); mark spec and `[~]` rule `:446`, `:464` (cited 413, 430–431); `/tmp`/`local://` evidence-standard rule `:370` (cited 327–344, which now carry unrelated text). Gate text at `:63–68` still matches.
6. `corpus/SOURCES.md` S006 `used-by` lists `corpus/lessons/round-12.md`, and S004/S006 `used-by` list `corpus/knowledge/repeated-control-precondition.md`. Neither file exists at the snapshot (in flight). When they land: QUALITY 10 requires `source:`/`verified-at:`/`recheck:` headers and QUALITY 7 a coverage-map row in the same round.
7. Scorecard command C (`SCORECARD.md` current axes) now yields `asserted_mark_upper_bound = min(8, 2×4) = 8`. That is a census upper bound, not the pinned score (6). Any reader running C must be told that the 8 is not awarded.

## 5. Risks ranked

1. Post-hoc C2 witness declarations sourced from the SKILL expected table (box 3). Mitigation: hash `declared.tsv` before opening `SKILL.md:652–663` or `mutation-case-kagi-census.md`; derive witnesses only from the pinned `surface-census.sh` selftest source at `fecee874`; permit `NONE`; log the contamination pattern in the README the way E1 did.
2. Any `SKILL.md` edit this round silently invalidates box 1 anchors and the box 3 cold-read. Mitigation: no `SKILL.md` edit; proposal to `corpus/` only.
3. C1 identical-output on one host read as determinism (box 3 and calibration). Mitigation: record host, PATH, env; state N and host; no "determinism proven" wording (round-12 contract).
4. C2 or C1 counted as a seventh gate or as box-2 independence. Mitigation: label as reanalysis of a recorded leg; keep leg count at six.
5. Sibling tree write by a C1 run (box 4). Mitigation: scratch materialization; pre/post porcelain check.
6. `/tmp` evidence (MK-6, PROTOCOL.md:370). The witness README retains copies in-repo, but its pinned target `pristine.mjs` is only a sha, not a copy (reproducible via `git show 175de6ba:scripts/kimi-census.mjs`). Round-12 outputs must land under `.ufo/evidence/round-12/{seat}/`, not `/tmp`.
7. Verified-but-unrecorded tool/state: no `round-12` entry in `LOG.md` yet; spec requires one for every change (L1 owns it).

## 6. Recommendations (read-only; L1 decides)

- Keep all four marks `[~]`. No `[x]` is supported under C1/C2 (no non-author verifier exists).
- Keep box scope notes unchanged. Box 3 stays Appendix A + B only.
- C1 (calibration): record repeated pristine-control results as a capability/measurement entry with the N, host, env, and the exact finding IDs (`controls_match`/`controls_mismatch`/`baseline_nonzero`/`command_unavailable`/usage). Do not map them to box marks or points.
- C2 (depth): record the bash split as a reanalysis of the recorded bash leg, with a pre-registered declaration hash, a contamination log, and an explicit `NONE` option per defect. Expected denominator: 10 defects; expected baseline: kagi `surface-census --selftest` 16/16 green (B-control).
- Errata (append-only, L1): items 4.1–4.5 and 4.7 above, plus the `LOG.md` "marked stale" correction (4.3).
- F3 remains Frontier until S011/S025/S027/S040 are mined.

## 7. Verification gaps (not run; not claimed)

- No C1 repeat-control run was executed by this seat (reviewer scope; the gate tool `tools/repeat-control.py` did not exist at snapshot).
- No C2 witness run was executed by this seat.
- Cross-host stability of the bash selftest (kaika U(a)) and PATH-varied behavior are unmeasured.
- The two in-flight knowledge files (`repeated-control-precondition.md`, `corpus/lessons/round-12.md`) were not reviewed (not present at snapshot).

## 8. Evidence pointers (this seat's reads)

- `SHONEN.md:5–11` (marks), `reports/round-1-calibration.md` (box-1..4, dispositions table), `reports/round-1-kaika-coldread.md` (Appendix A/B tables, step table, O/I/U), `.ufo/evidence/kaika-round-1/witness/README.md` + `declared.tsv` (hash checks), `corpus/knowledge/witness-scoped-kill-verdict.md`, `corpus/knowledge/mutation-case-kagi-census.md`, `corpus/README.md` `## Frontier` (F1–F10), `corpus/SOURCES.md` (registry rows S004/S006/S011/S025/S026/S027/S040), `corpus/QUALITY.md` (criteria 1–10), `corpus/lessons/round-1.md` `## Mistakes` (MK-1…MK-11), `PROVINCE.md:3–47`, `SKILL.md` (sha, 12–16, 58, 466–525, 594–668, 1464–1476), `LOG.md` lines 270–300 and tail, `SCORECARD.md:58–70, 154–256`, `kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md` (`:63–68`, `:370`, `:446`, `:455–464`), pinned `kagi-shokunin fecee874:corpus/surface-census.sh` (sha `275d8294…`).

## 9. Exact owned path

- Written: `.ufo/waves/round-12/w1/SHONENReview.md` (this file).
- Not written: any `SHONEN.md` mark, any `SKILL.md`, `LOG.md`, `PROVINCE.md`, `reports/*`, `corpus/*`, `tools/*`, `.ufo/evidence/*`, sibling trees.

## Finding IDs (for L1 index)

- SHN-1 (box 3 contamination risk for C2 declarations): blocking for any C2 box-3 claim.
- SHN-2 (SKILL bytes bound by box 1/3): hold `SKILL.md`.
- SHN-3 (stale `[ ]` in SKILL:1464–1476 and calibration report box-3 row vs `[~]`): errata.
- SHN-4 (LOG "marked stale" claim not in bytes): errata.
- SHN-5 (protocol citation drift in calibration report): errata.
- SHN-6 (C1 cross-host / PATH limits): record as limit, not determinism.
- SHN-7 (F3 sources queued): keep F3 Frontier.
