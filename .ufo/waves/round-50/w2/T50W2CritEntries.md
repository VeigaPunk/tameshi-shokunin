# T50W2CritEntries — F6 knowledge entries review (wave 2)

Seat: `T50W2CritEntries-2` (critic). Item: attack `corpus/knowledge/fixture-shrinking-pilot.md`
and `corpus/knowledge/delta-debugging-minimization-contract.md` at the candidate content revision
`80ea77e99e239982ab0b93e416645ef2359725d3` against `corpus/QUALITY.md` (criteria 1–101, esp. 2, 3,
4, 9, 10, 34, 51, 79, 91, 97) and `PROVINCE.md`. Read-only on the lane; the only file written is
this report. No tool installed (pacman paused; nothing needed). No `/home/vgpnk/.local/state/` read;
no mutant names or edits quoted from `.ufo/evidence/round-50/control/c2-*.stdout` (summary lines
only).

## Method

- Read both entries, `corpus/QUALITY.md`, `PROVINCE.md`, `tools/shrink-case.py`, `.ufo/evidence/round-50/c2/measure.py`,
  `corpus/knowledge/pbt-generator-pilot.md`, `corpus/knowledge/survivor-fixture-minimization.md`,
  `corpus/README.md`, `corpus/SOURCES.md`, wave-1 receipts `T50ExecShrinker.md`, `T50ScribeSrcHeld.md`,
  `T50ScribePkgDD.md`, `contract.json` `claims.C2`, and control receipts (summary lines only).
- Every lane path cited by the two entries checked for existence at REV (`git cat-file -e REV:path`).
- Source quotes verified against the committed snapshots (PDF extracted with `pdftotext`; S024 HTML;
  S022 abstract via `T50ScribeSrcHeld.md`), and DOI identity via Crossref.
- Tool behavior probed in scratch (clone at REV): selftest in both layouts; sha256 of the committed
  shrinker vs the wave-1 deliverable receipt.

## Verification ledger (all true; commands that show each)

**Pointers resolve at REV** — every backticked lane path in both entries exists at `80ea77e9`
(`git cat-file -e` OK): knowledge files, README, SOURCES, `tools/shrink-case.py`,
`tools/staged-id-guard.py`, `tools/pbt-staged-id.py`, `measure.py`, `control/c2-CTL_REF.stdout`,
`control/c2-selftest.stdout`, `deciding-run.sh`, `round-49/c2/panel.json`,
`round-29/sources/S024-fuzzingbook-Reducer.html`, `w1/T50ScribeRows.src/zeller-hildebrandt-tse2002.pdf`,
`w1/T50ScribeSrcHeld.md`, `w1/T50ScribePkgDD.md` (incl. its `## Required edits` section, exactly 14
numbered edits, `sed -n '144,195p'`).

**Shrinker copy is byte-exact** — `git show REV:tools/shrink-case.py | sha256sum` =
`1ac31ae58d807df76d632d5eb18b06c2e62eae0428fc1fb3b2dc3f01ebb3526f`, identical to the wave-1
deliverable receipt (`T50ExecShrinker.md:6`).

**Pins match** — guard sha256 `03a796c572…` = `GUARD_SHA256`; panel sha256 `d6dd2cf383…` =
`PUBLIC_SHA256`; panel M02 `old`/`new` exactly equal the embedded `M02_EDIT` strings in the tool;
frozen generator blob at `7d3d977f` sha256 `0cbee392a8…` = `GEN_SHA256` (counter loads GEN_REV;
`measure.py:187-210`).

**Source quotes verified against snapshots** (reading-order extract of the 247,738 B PDF, sha256
`7ed0c812…`, 17 pages A4, no journal folios, running head "IEEE TRANSACTIONS ON SOFTWARE
ENGINEERING, VOL. 28, NO. 2, FEBRUARY 2002" present):
- `removing any single input entity would cause the failure to disappear` — count 1 (both recheck
  commands reproduce their expected `1`; pilot recheck and delta recheck).
- `After 57 tests, the original 896-line HTML input is reduced to the minimal failing test case` — 1.
- `After 82 test runs (or 21 minutes), only 3 out of 95 user actions are left` — 1, in the Fig. 11
  body (`Minimizing Mozilla user actions`); the `896 lines to a 1-line input` sentence sits in the
  Fig. 12 body (`Minimizing Mozilla HTML input`).
- `The case study required 139 automated test runs, or 35 minutes on a 500 MHz PC` — 1 (Abstract).
- `is fed with a failing test case, which it simplifies by successive testing` — 1.
- `is 1-minimal in the sense of definition 10` — 1 (Proposition 11); `Definition 10` present (×2).
- `After 26 steps, the line is reduced to the single <SELECT> tag` — present (§V-A).
- Mirror page anchors p. 1 / p. 4 / p. 6 (S271 row) resolve: `pdftotext -f N -l N` finds the §I
  sentence, Definition 10, Proposition 11 respectively; `-layout` extraction hyphen-folds
  `sim-\nplifies` (the recheck parenthetical is accurate).
- S024 `Its result is 1-minimal, meaning that every character contained is required to produce the
  error` verified in the committed round-29 snapshot (also `T50ScribeSrcHeld.md`).
- S022 abstract fragments verified via `T50ScribeSrcHeld.md` (tag-strip substring checks all True).

**DOI identity** — `10.1109/32.988498` resolves via Crossref to "Simplifying and isolating
failure-inducing input", IEEE TSE 28(2):183-200, Feb 2002, Zeller & Hildebrandt.

**Counter/records claims match `measure.py` and control receipts** — `units()` identical to the
tool's unit count; `removals()` enumerates every single-unit removal; sub-case/kill/minimal/cost
flags as described; ok threshold `total−1` with net reduction required; `records()` needs a README
line with `F6` + `held (round 50)` (present at `README.md:608`) and a new knowledge file whose
`source:` line cites a `mined` row opened `2026-10-26` (S271 satisfies); `c2-CTL_REF.stdout` last
line: `mutants=20 ok=20 units_before=164 units_after=43 … total=0 C2_R50_PASS=true`;
`c2-selftest.stdout` ends `C2_R50_SELFTEST: cases=9 failed=0` with the nine labels (reference,
cost-liar, identity, non-subset, absent shrinker, failing tool selftest, missing records, panel
digest mismatch, instrumentation).

**Tool selftest measured on a scratch clone** — layout 1 (generator only, the counter's copy):
`cases=14 failed=0`, exit 0; layout 2 (+guard+panel): `cases=21 failed=0`, exit 0. Confirms the
pilot's "(14 cases there, 21 when the guard sits beside it)".

**No F6 overclaim** — both entries explicitly state B5 stays masked (round-29 record at
`survivor-fixture-minimization.md:53,57`), the method is on killing cases, not survivors of a
battery, and status lives in `corpus/README.md` `## Round 50`, not in the entries; the README line
holds F6 pending the deciding receipt.

## Findings

**Finding 1 — severity 4 (low).** `fixture-shrinking-pilot.md:12` presents the gate pair as
"the round-49 generator's oracle `tools/pbt-staged-id.py` (frozen at `7d3d977f`, sha256
`0cbee392…`)". That is accurate for the frozen revision (the counter loads the generator via
`GEN_REV`; `measure.py` verifies the digest), but at the revision under test the working-tree file
differs: `git show 7d3d977f:tools/pbt-staged-id.py | sha256sum` = `0cbee392…`, while
`git show 80ea77e9:tools/pbt-staged-id.py | sha256sum` = `a6e1253a…` (the routed R49.1 error-path
fix, commit `43bfa7a`; `git diff 7d3d977f..80ea77e9 -- tools/`). A reader at 80ea77e9 sees
different bytes at the cited path, and the counter places the REV copy beside the shrinker for the
tool's selftest leg while judging with the frozen oracle. Fix (one clause): state that the
working-tree copy carries the R49.1 error-path fix and that the measured oracle is the blob at
`7d3d977f` (`GEN_REV`), so "frozen" is unambiguous.

**Finding 2 — severity 4 (low).** `fixture-shrinking-pilot.md:30-31`: "A reduction reported without
its run count cannot be compared with another reduction; runs are also the unit the lane counts
everywhere else." This is an inference presented as fact (QUALITY 3); the sibling entry marks the
parallel claim explicitly ("Inference:" at `delta-debugging-minimization-contract.md:31`). The
second clause also overstates the lane's cost units (round 29 counted the tests; round 49 counted
generated cases; C2 counts guard runs). Fix: prefix "Inference:" and narrow, e.g. "runs are the
unit the F6 attempts count".

No false or unlocatable statements, unsupported shrinker claims, or F6 overclaims found at severity
3 or above.

## Summary

- All pointers cited by the two F6 entries resolve at `80ea77e9`; all quoted source text verifies
  verbatim against committed snapshots (Zeller/Hildebrandt TSE 2002 PDF, Fuzzing Book S024, ECOOP
  S022 via the Held receipt); the DOI resolves to the article.
- The committed shrinker is byte-exact to the wave-1 deliverable; its interface, units, kill rule,
  cost accounting, exit behavior and both selftest shapes (14/21 checks, exit 0) match the entries
  and the frozen counter's own audit.
- Control receipts support the positive-control and selftest descriptions (20/20, 164→43 units;
  cases=9 failed=0); SOURCES/README/F6-status handling is consistent and does not overclaim F6.
- Two low-severity findings: (1) the working-tree generator at the candidate differs from the frozen
  blob (R49.1 error-path fix) — add one clarifying clause; (2) one unmarked inference with an
  over-broad "everywhere else" cost-unit claim — label and narrow it.
- Verdict: entries are accurate; only precision/clarity edits recommended.
