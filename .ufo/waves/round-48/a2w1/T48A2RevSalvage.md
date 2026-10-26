# T48A2RevSalvage — salvaged attempt-1 drafts (15b1521) vs content tree c7586b9a

Seat: T48A2RevSalvage (a2w1, leaf member — no subagents). Item: check every factual statement in the
orchestrator salvage commit `15b1521ea2e95d0d708059458c090e9f334adf32`'s DRAFT LOG.md round-48 entry
(LOG.md:2348-2357) and QUALITY 94-96 (corpus/QUALITY.md:1379-1426) against the content tree
`c7586b9a10effc63b4bd327f976edc094c1bdc17`; then check that the attempt-2 L1's appended LOG correction
(LOG.md:2359-2368) corrects each stale line. Read-only on the lane except this file. No tools installed
(no pacman, no uv, no binaries — none needed). Scratch `/fast/scratch/hyaku/tameshi-r48/T48A2RevSalvage`
removed before finish.

## Findings

### F1 (moderate) — QUALITY 96's falsifier claims its two round-47 inputs differ "for the same statement and revision"; they are at different revisions

- Statement: `corpus/QUALITY.md:1426` — "the round-47 freeze receipt (`--work` under `/tmp`) and deciding
  receipt (`/var/tmp`) print different P1 tuples **for the same statement and revision**"; same claim in the
  script comment `.ufo/evidence/round-48/quality/falsifiers.sh:36` — "# ---- 96: one statement, one revision,
  one counter: only the --work placement differs".
- Refutation (the receipts' own label lines):
  `grep -m1 -oE 'rev=[0-9a-f]{40}' .ufo/evidence/round-47/before/c1-at-freeze.stdout` → `rev=9acfbe21435e1976636a276448dee1d5e7155915` (line 45);
  same command on `.ufo/evidence/round-47/after/c1.stdout` → `rev=8b0e15d25ea598c0bf908d183fb410a085bf3a18` (line 45).
  Freeze commit = 9acfbe2 (round-47 freeze), deciding revision = 8b0e15d (round-47 content revision). Two variables
  differ (revision and `--work` placement), so the named pair is not the controlled pair criterion 96 itself
  requires ("same revision, same counter, same profile, with exactly the named variable changed").
- What is true: the P1 tuples do differ — `c1-at-freeze.stdout:18` `P1=ENVDIFF_SELFTEST: 2/9 pass|1` vs
  `c1.stdout:18` `P1=ENVDIFF_SELFTEST: 9/9 pass|0`; the round-48 counter refuses a `/tmp` work dir
  (`calibration/measure.py:101` `def under_tmp`, refused at `:395`, selftest case `T63_work_under_tmp_refused`
  at `:836`). Probe (as observed, never a verdict): `HYAKU_SCRATCH=$S bash .ufo/evidence/round-48/quality/falsifiers.sh`
  prints `CRITERION-96-FALSIFIER-OK` — the block fires, but on inputs that do not satisfy the described control.
- The honest same-revision pair exists and is a wave report, not a receipt: `.ufo/waves/round-47/w1/T47ExecObsC.md`
  runs 1-2 (`--work /tmp/...`) vs runs 3-4 (`--work /var/tmp/...`), all at `--rev 9acfbe2…` (commands :30-44,
  rev line :56, PROFILES :54 vs :85); `w1/T48RevenEnvDiff.md:39-47` cites exactly that split and never claims the
  freeze/deciding receipts are same-revision. The salvaged criterion text overstates what its named inputs show.
- Not corrected: the attempt-2 LOG correction (LOG.md:2359-2368) and the lesson's attribution row
  (`corpus/lessons/round-48.md:350-354`, which cites the same two receipts without a same-rev claim) do not flag
  the clause; the salvaged text is unrewritten by design. Fix shape: an appended erratum dropping "and revision"
  or re-pointing the falsifier's pair to the T47ExecObsC same-rev runs (and the same for `falsifiers.sh:36`).

### F2 (minor) — LOG.md:2354 cites "routed defects 2, 4" for the selftest receipts; routed defect 4 is the reject citation

- Statement: "round-47 selftest receipts committed (routed defects 2, 4: `.ufo/waves/round-48/w1/selftest/`)".
- `corpus/lessons/round-47-verifier-spotcheck.md:101-107`: routed defect 2 = "Commit selftest receipts for the
  three round-47 counters, `addition-lint.py` and the criterion-93 falsifier block (conformance defects 3 and 4)";
  routed defect 4 = "Reject citation: ... cite the unopened-row reason (QUALITY 10) rather than
  `PROVINCE.md:14-18`" — not a selftest receipt, and it is answered by the lesson's re-stated Reject
  (`corpus/lessons/round-48.md:98-102`), not by `w1/selftest/`. The directory (committed at `755298415f8c`:
  c1-measure, c2-pool, c3-coverage, addition-lint, falsifiers*.stdout carrying `CRITERION-91/92/93-FALSIFIER-OK`,
  lesson-quote-check) answers routed defect 2 = conformance defects 3 and 4. Correct cite: "routed defect 2
  (conformance defects 3 and 4)". Not corrected by the attempt-2 append.

### F3 (minor) — LOG.md:2350 "three rows without per-snapshot fetch receipts or anchor digests (S026, S093, S108)" is false for S093's digest half

- S093's anchor cell already carries a digest at the round-45 tip and at the round-48 base:
  `git show 0b5b7cd2:corpus/SOURCES.md | grep -E '^\| S093 ' | grep -oE 'sha256 [0-9a-f]{12}'` → `sha256 2cb77df2f4be`
  (same at `473336d`: "xml sha256 2cb77df2f4be… (33289 bytes), re-fetched by the L1 with the same digest").
  S026 and S108 anchors carry no digest at either revision. All three (and S048) lack per-snapshot fetch
  receipts: `ls .ufo/evidence/round-45/freshness/sources/` holds only `.raw.gz` snapshots, no `.receipt.json`.
- The pre-registered phrasing (contract C2 `type`; round-47 routed defect 5) is "per-snapshot fetch receipts and
  anchor refresh for S026, S093, S108" — the draft's "or anchor digests" is a paraphrase that overstates S093's
  gap. Substance unaffected: receipts for all three and the re-anchoring are delivered (S265-S268 + 4 receipts +
  4 re-pointed entries). Not corrected by the attempt-2 append.

### F4 (observation, disclosed — not a stale-uncorrected finding) — the two receipts the salvaged criteria name still do not exist

- At `c7586b9a` and at the current tip `17cc5ce141868454d05bf75ef5cd230e35f0cdf4`:
  `.ufo/evidence/round-48/control/c1-controls.stdout` (QUALITY.md:1418) and
  `.ufo/evidence/round-48/quality/c94-96-falsifiers.stdout` (QUALITY.md:1398) are absent; no `after/` dir yet.
  Probe (as observed): `python3 .ufo/evidence/round-48/quality/pointer-check.py --lane LANE --rev 17cc5ce
  --file corpus/QUALITY.md --start "## Criteria appended — round 48"` → two `MISSING` lines, `checked=11
  missing=2`, exit 1.
- This is mined and corrected by the erratum chain: the lesson's prospective-record Mistakes row
  (`corpus/lessons/round-48.md:356-360`) names both receipts as absent at `15b1521e`; QUALITY 97
  (QUALITY.md:1428-1435) makes pointer resolution at the landing tip a checked criterion; the red receipt
  `quality/pointer-check-red-15b1521.stdout` shows exactly those two `MISSING` lines at `15b1521` (exit 1,
  LOG pointers checked=8 missing=0); the LOG correction (LOG.md:2362) states the c1-controls receipt "lands
  with" the C1 controls. Residual: the LOG append itself does not name `c94-96-falsifiers.stdout`; its landing
  is enforced only via QUALITY 97's landing-tip pointer-check — if the landing tip ships without it, the L1's
  own falsifier fires.

### F5 (observation) — the correction's "the 24 reports under `.ufo/waves/round-48/w1/`"

- `git ls-tree -r --name-only c7586b9a -- .ufo/waves/round-48/w1/ | grep -c 'T48.*\.md$'` → 26: 22 final seat
  reports + 2 `.draft.md` drafts (T48ScribeLessonCorrection.draft.md, T48ScribeMistakes.draft.md) + 2 `.rows.md`
  artifacts (T48ScribeRowsA.rows.md, T48ScribeRowsB.rows.md). "24" is exact only as "non-draft .md files"
  (22 reports + 2 rows artifacts); as "seat reports" it would be 22 (23 counting T48ScribeRowsB.rows.md as
  ScribeRowsB's only deliverable). Footnote-level imprecision in the correction, not in the salvaged draft.

## Verified true (salvaged drafts vs c7586b9a) — compact inventory

- Motivating (LOG.md:2350): routed defect 1 is the one-shot `six-leg regression ledger` restatement —
  `corpus/lessons/round-47-verifier-spotcheck.md:102-103` (N ≥ 3 per profile or a declared nondeterministic
  class); the claimed value `REGRESSION: FAIL (cases=9 passed=7` is `.ufo/evidence/round-47/after/c1.stdout:5`
  (`claimed=...FAIL (cases=9 passed=7|1`); "calibration, monitor 6, the lowest non-retired axis" = contract
  `axes.lowest_non_retired_axis`. Round-45 disputes: `.ufo/evidence/round-45/freshness/reviews.json` — S048
  CritJudge02 `dispute` (quote truncated mid-`<li>`, drops the consequent), S093 CritJudge03 `dispute`
  (markup-only fragment, never names `--unshare-all`); "carried unworked since round 45" = round-47 routed
  defect 5 "still open". Shas: `e73389c0b474…`, `f1cfaad3601…`, `755298415f8c4eef3bed0c0d7625e2aacb03d6c2`
  all resolve (`git rev-parse`); contract has amendments 1-10 (10 = declined F2); `freeze-2.json` exists.
- C1 bullet (LOG.md:2352): at `c7586b9a` the SCORECARD round-48 standing section holds exactly 22 data rows
  (19 capability + 3 axis), every evidence cell `runs 3 stable` — `emit-15b1521.stdout` has 22 `runs 3 stable`
  lines, 0 `nondeterministic`, exit 1 (`emit-15b1521.exit`) as an unparsed tree must; `six-leg regression ledger`
  r1/r2/r3 all `REGRESSION: PASS (cases=9 passed=9|0`; DEPS lines print `required=/unstable=/never=`.
  Root causes: `w1/T48RevenEnvDiff.md` §1-§5 (2/9 under P1 is `--work`-under-`/tmp` masking — tmpfs over the
  profile PATH shim, `tools/env-diff.py:68-71`; SCORECARD.md:2314 "not stable across runs under host load" is
  the misattribution) and `w1/T48RevenRegression.md` §1-§5 (SIGPIPE under `set -uo pipefail` at
  `tsukuroi-census.sh:638`, pinned blob `084951be…` @ `165307fe`; leg selftest failed 4 of 40 runs at 6-way
  concurrency; one-sided PASS→FAIL). Both files exist and support the draft's wording.
- C2 bullet (LOG.md:2353): rows S265-S268 exist at `c7586b9a` with `supersedes S0xx's anchor and quote only`
  scope cells; 4 snapshots + 4 receipts under `.ufo/evidence/round-48/freshness/sources/` (each receipt: url in
  R's source cell, `fetched_at` 2026-10-26T08:4xZ, `http_status` 200, sha256; S093's receipt sha256 equals the
  base anchor digest `2cb77df2f4be…`); Gate lines `corpus/lessons/round-48.md:21-24` carry all four required
  phrases (`84%`; `should therefore be prioritised`; `--unshare-all` + `--unshare-cgroup-try`, exactly 25
  whitespace tokens; `--update_goldens`) and restore exactly the content the two round-45 disputes said was
  dropped; the four base used-by entries (S026→repeated-control-precondition, S048→incremental-pin-disposition,
  S093→regression-tally-completeness, S108→r8-golden-update-flag) each cite their new row with
  `verified-at: 2026-10-26`.
- Frontier bullet (LOG.md:2354): SOURCES registry rows 124 → 128 (`grep -cE '^\| S[0-9]{3} '` at `473336d` vs
  `c7586b9a`); `census-start.exit` = 0; `## Mistakes` exists with the attribution mined-mistake row
  (round-48.md:350); `quality/falsifiers.sh` exists; `w1/selftest/` committed (see F2 for the defect numbers);
  `considerthese/2026-10-25.md:78-79` idea 5 "Proposal uptake ledger" mined at round-48.md:364; "assimilation
  none" consistent with the contract (no assimilation claim; the staged package refused, round-48.md:91-96).
- Waves bullet (LOG.md:2355): stale as written (w2 never ran) — corrected, see below.
- QUALITY 94 (QUALITY.md:1379-1398): `PROVINCE.md:14-18` refuses product domains and sibling gates (read);
  the decisive reason QUALITY 10 clause 2 (entry cites staged S205/arXiv 1810.05286, never opened) matches the
  spotcheck's "agree, reason partly" row (round-47-verifier-spotcheck.md:89-90) and the lesson's re-stated
  Reject (round-48.md:98-102); block 94 exists and behaves as described — probe printed `WEAK-CITE` + exit 1 on
  the bad fixture and `rejects=2 weak=0` on the real lesson (`CRITERION-94-FALSIFIER-OK`).
- QUALITY 95 (QUALITY.md:1400-1418): cross-references resolve — criterion 92 at QUALITY.md:1363, criterion 71
  at QUALITY.md:833 (round-31 numbered-list form, "when the quoted tool changes, the lane appends a new row");
  "9/9 and 2/9 under the same profile P1" = the two round-47 receipts' P1 cells; the SCORECARD disclosed limit
  is `473336d:SCORECARD.md:2314`. CTL_B/CTL_E expectations match `falsifiers.sh:24-33`'s greps.
- QUALITY 96 (QUALITY.md:1420-1426): lesson row matches (SCORECARD.md:2314 host-load wording;
  T48RevenEnvDiff.md masking finding); `under_tmp` refusal true (measure.py:101,112,395,836); VACUOUS logic
  as described — except the "same revision" clause, F1.
- Attempt-2 correction (LOG.md:2359-2368) verified: w1 dispatched 32 (`w1-dispatch.json` counts spawn=32),
  no results file, `w1/swarm-registry.json` 32 members 0 terminals; no `w2` directory (only `w2-items.py`);
  a2w1 = 64 seats (`spec-a2w1.json` items=64: 32 `T48W2*` + 32 `T48A2*`; `a2w1-dispatch.json` counts 64);
  c2-controls.stdout `CONTROLS: F=0 G=0 H=2 expected=F0,G0,H<=2 ok=true`; C1 rows restated from the emit at
  `15b1521e` (22 `runs 3 stable`); six-leg PASS passed=9 in all three emit rounds, disclosed known-
  nondeterministic in the SCORECARD round-48 block; QUALITY 97 + pointer-check.py + red receipt exist; the
  lesson's seat-draft scaffolding (```markdown blocks, "Correction block to append", "Not changed") replaced
  by integrated text (diff 15b1521..c7586b9).

## Correction adequacy (each stale line → where corrected)

| Stale/false line in the salvage | Corrected by |
|---|---|
| LOG.md:2355 "w1 build (32 seats) and w2 falsify (32 seats)" | LOG.md:2361 (w1 dispatched 32, crash before results, 24 reports; "No `w2` ran"; a2w1 64 seats) — adequate |
| QUALITY.md:1398/1418 receipts absent at the revision | LOG.md:2362 (c1-controls receipt "lands with" the C1 controls) + LOG.md:2364 → lesson prospective-record row (round-48.md:356-360, names both receipts) + QUALITY 97 + red receipt — adequate via the named chain |
| Draft C1 provenance ("three observation rounds") | LOG.md:2363 (restated from the emit at `15b1521e`, all 22 `runs 3 stable`; six-leg PASS passed=9 ×3, disclosed) — adequate |
| LOG.md:2354 "routed defects 2, 4" | not corrected — F2 |
| LOG.md:2350 "or anchor digests" (S093) | not corrected — F3 |
| QUALITY.md:1426 "same statement and revision" | not corrected — F1 |

## Probes run (as observed; a probe is never a verdict)

1. `HYAKU_SCRATCH=$S bash .ufo/evidence/round-48/quality/falsifiers.sh` at the working tree (17cc5ce):
   block 94 `CRITERION-94-FALSIFIER-OK` (bad fixture `WEAK-CITE` + exit 1; lesson `rejects=2 weak=0`);
   block 95 `CRITERION-95-FALSIFIER-VACUOUS` (grep: c1-controls.stdout: No such file or directory — the
   disclosed pending state); block 96 `CRITERION-96-FALSIFIER-OK` (`tmp-work P1=...2/9 pass|1` vs
   `var-tmp-work P1=...9/9 pass|0`); script exit 0 (it signals via printed OK/VACUOUS lines, not its exit code).
2. `python3 .ufo/evidence/round-48/quality/pointer-check.py --lane LANE --rev 17cc5ce --file corpus/QUALITY.md
   --start "## Criteria appended — round 48"` → 2 MISSING, checked=11 missing=2, exit 1.

## Residual risk and verification gaps

- The deciding run has not landed (no `.ufo/evidence/round-48/after/`, no c1-controls.stdout, no
  c94-96-falsifiers.stdout as of this check); QUALITY 97's landing-tip pointer-check and the correction's
  Controls bullet govern their landing. I did not wait for it.
- I did not run either claim counter (other seats' assignments); every check here is against committed bytes
  plus the two read-only probes above.
- The correction's "patched where amendments 4-10 changed their premise" (w2-items → a2w1 spec) was not
  diff-checked item-by-item; the derived counts (32+32=64) are verified from `spec-a2w1.json`/dispatch.
- F5's "24 reports" reading (non-draft .md) is interpretive; final seat reports number 22.

## Tooling record

No tools installed or upgraded ( pacman guard respected — zero pacman calls; no uv/npx/binary installs).
