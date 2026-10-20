# WitnessSourceReview — S006 pinned README vs witness knowledge claim

Lane-internal advisory (round 12, w1). Not independent non-author promotion or admission. No outcome hints were sent to the experiment seat.

## Scope and axes

Named axes:
1. Quote fidelity: knowledge quotes vs the pinned S006 README.
2. Semantic fidelity: the S006 verdict grammar as paraphrased vs source semantics.
3. Mapping fidelity: S006's witness rule vs the tameshi declared-label rule used in the witness experiment.
4. Record integrity: digests, fetch timestamps, recheck commands.

Target knowledge file: `corpus/knowledge/witness-scoped-kill-verdict.md`, section `## S006 verdict grammar (O)` and its correspondence paragraph. Evidence: `.ufo/evidence/kaika-round-1/witness/README.md`, `declared.tsv`, `case-labels.tsv`, `D1.out`–`D10.out`, `control.out`.

## Evidence (observed)

- **Pinned README fetched independently** from `https://raw.githubusercontent.com/BWBama85/shmutant/7eefc73010ad6342b80e3ed43915503e02c90618/README.md` into `/tmp/s006-readme-pinned.md` (scratch). 231 lines, 12117 bytes.
  - SHA-256 `dc0051c79ab792d0f4e1b19404ed661b4c94a8e54016595aeae853d5410178a3`. This matches the digest in the knowledge header, the witness receipt, and `.ufo/evidence/kaika-round-1/score-semantics/S006.md`.
- **Recheck re-run:** `grep -c 'not on its witness'` returns `1` on the pinned commit and `1` on `main`. Both match the recorded recheck. This only confirms that one sentence exists; it does not confirm the semantics.
- **Source lines confirmed:**
  - README:29 `killed` = "The suite went red **on its witness**. The test detects the defect."
  - README:31 `accidental` = "The suite went red, but not on its witness. Caught by accident, not by the assertion that claims to cover it."
  - README:38 `unapplied` = "The old literal matched nothing. The row injected no defect and tests **nothing**."
  - README:39 `baseline` = "The selected tests were not green before any defect was injected (red, or aborted: the red status with no red line), or, with `SHMUTANT_COUNTS=1`, did not count for each of their units the assertions the whole suite counts for it. A red result would prove nothing."
  - README:41–45 names `aborted`, `timeout`, `unsettled`, `lost` as runs with no answer.
  - README:90–93 non-unique old literal refused. README:94–97 "Every distinct selector is run once, uninjected, and must come back green" (step 2).
  - README:101–102 "Red is exit 1 with a line starting `FAIL: ` that carries the witness as a whole token (`parse-empty` is not found in `parse-empty-list`)."
- **Witness experiment labels, exact-line probe** (python, read-only). For each `declared.tsv` alternative (split on ` | `), I checked for an exact `FAIL <label>` line in that defect's own `D*.out`:
  - D1 2/2 exact; D3 3/3; D4 3/3; D5 1/1; D7 2/2; D8 3/3; D9 2/2.
  - D6 1/2. The non-matching alternative is "secrecy: fixtures are shape-clean with a 0600 leaf token (mode floor passes)", which describes a passing expectation and never appears as a FAIL line.
  - D2 and D10 are `NONE`, with 0 FAIL lines each.
  - Every killed defect has at least one exact declared hit, so the 8 killed-on-witness / 0 accidental / 2 survived split is reproduced by the probe. I did not re-run the experiment.
- **Control:** `control.out` tail reads `KIMI_CENSUS_SELFTEST: 43/43 pass`, `VERDICT: PASS`. Recorded only; not my gate.
- **Sensitivity (from the probe above):** D1 keeps its exact hit on "UNLISTED: a 19th lane file under agents/secondary/" if the generic "green fixture" alternative is dropped. D3 keeps exact hits on its `--json` alternatives. So the 8 kills do not depend on the generic clean-fixture alternative. This is an observation from the probe, not a re-run classification.

## Findings (by severity)

**F1 (medium, quote and paraphrase fidelity — baseline).** The knowledge quote "The selected tests were not green before any defect was injected." truncates README:39 and adds a closing period that is not in the source. The source definition also covers red-or-aborted baselines and the `SHMUTANT_COUNTS=1` per-unit assertion-count rule. The knowledge paraphrase is narrower than the source. The witness receipt repeats the same truncation. Fix: quote the full clause, or mark the truncation with an ellipsis and state the omitted qualifiers.

**F2 (low, paraphrase precision).** The knowledge says `How a row is run` "runs the selected witness before the mutation." README step 2 says every distinct *selector* is run once uninjected and must come back green. The unit is the selected tests, not a single witness. Also the unapplied quote drops the README's bold markup; the words are unchanged.

**F3 (medium, mapping omitted from the knowledge file).** S006 requires a `FAIL: ` line that carries the witness as a *whole token* (README:101–102). The knowledge file does not state this rule. The tameshi classification in the witness experiment is instead exact equality of a declared alternative with a `FAIL ` line (probe above). Exact equality is stricter than substring matching and is not S006's rule. The knowledge should state the matching rule actually used, and say it is not S006's whole-token rule.

**F4 (medium, experiment declaration — D6, not S006).** Declared alternative 2 for D6 ("secrecy: fixtures are shape-clean with a 0600 leaf token (mode floor passes)") is a passing expectation, not a failing witness. It never appears as a FAIL line. Under the current any-of rule the D6 classification still holds, via the SHAPE_DRIFT alternative. But the declaration is not a valid failing witness and would fail a stricter reading. D6's failing "secrecy: server.token is a FIFO" label is outside D6's declared set; `case-labels.tsv` records it as extra. Recommendation: note this in the witness README as a declaration defect; do not rewrite the pre-registration.

**F5 (low-medium, witness breadth — experiment).** S006 has one witness per row. The tameshi declaration is any-of up to three alternatives. The generic "green fixture → CLEAN exit 0 …" alternative appears in D1 and D3 and fails on several defects. The probe shows the 8/8 kill classification does not depend on it (see Sensitivity). Still, the knowledge should not describe these as single-witness kills.

**F6 (low, record integrity — timestamps).** The witness receipt and knowledge header record fetch time `2026-10-19T22:03:41Z`. `.ufo/evidence/kaika-round-1/score-semantics/opened.tsv` and `corpus/SOURCES.md` context record `2026-10-19T19:03:06-03:00`, which is `22:03:06Z`. Same digest, 35 seconds apart. Reconcile or annotate as separate fetches.

**F7 (info, not verified).** The SOURCES row's "0 stars, 239 commits at open" was not re-verified in this lane. The classification of the witness experiment as "manual" is inferred from the absence of a retained classifier script in `witness/`; the witness README describes the rule in prose.

## Recommendation (lane-internal; not an independent admission)

**ADMIT the `## S006 verdict grammar (O)` paragraph, conditioned on errata for F1 and F3.** The four verdict definitions (killed, accidental, unapplied, baseline) and the aborted/timeout/unsettled/lost list match the pinned README by exact sentence and digest.

Do **not** cite the 8/0/2 split as S006-verified semantics. It remains a tameshi declared-witness result (`partly contaminated`, errata E1), and the mapping differs from S006 as stated in F3 and F5. F4 is a declaration defect in the experiment and should be recorded as an erratum there, not used to change the split.

## Owned paths

- Written: `.ufo/waves/round-12/w1/WitnessSourceReview.md` (this file).
- Scratch only: `/tmp/s006-readme-pinned.md`.
- Not written: no knowledge, evidence, SOURCES, LOG, or experiment files were modified.

## Tools

- Used: `curl`, `sha256sum`, `grep`, `sed`, `python3` (read-only probe). No installs or upgrades were performed.

## Verification gaps

- The experiment was not re-run. The probe checks only that declared alternatives appear as exact FAIL lines in retained outputs.
- The recheck confirms one sentence, not semantics.
- The classifier is not retained as a script; manual steps cannot be reproduced mechanically from the repo.
- Star and commit counts for the S006 repository were not re-verified.
