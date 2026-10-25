# ScribeLesson — round 42, wave 1

Seat: L1Tameshi42.ScribeLesson. Scope: draft `## Mistakes` rows for `corpus/lessons/round-42.md`.
Read-only seat; the only lane write is this report.

## Findings

**F1 — stale-receipt class (m10) is live at base and uncaptured.**
Evidence pointer: `.ufo/waves/round-41/residual/receipt.json:14-17` asserts
`ResidualReceipts` → `"present": false` (line 16), while
`.ufo/waves/round-41/residual/ResidualReceipts.md` exists (23.8 KB, listed in the
same dir). The receipt was written before the report it describes.
Base measurement confirms the live mismatch — `.ufo/evidence/round-42/before/c1-at-base.stdout:1-3`:
`MISMATCH m10 .ufo/waves/round-41/residual/receipt.json asserts present=false for .ufo/waves/round-41/residual/ResidualReceipts.md; tree says true`, then
`C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=1 m11=0 total=1 records=3 ... C1_R42_PASS=false` (exit failure).
No instrument captured it before: it survived round 41 into the round-42 base
(routed as spotcheck defect 2 but unfixed), so captured-by = none.
Fix landed in the round-42 counter: m10 audit + superseding-receipt rule
(`.ufo/evidence/round-42/calibration/measure.py:38-42,199-202`), shown able to
fail by selftest `T2_stale_counts`, `T2_superseded_clears`,
`T2_junk_supersede_still_counts`, `T2_partial_supersede_still_counts`
(`measure.py:304-315`; all OK in `.ufo/evidence/round-42/before/c1-selftest.stdout:3-6`).

**F2 — newline-spanning backtick regex (m8 extractor defect) in the round-41 C1 counter.**
`BACKTICK_RE = \`([^\`]+)\`` spanned newlines, so a cited path inside a mispaired
span was silently skipped (`corpus/SOURCES.md` was skipped round 41) —
`corpus/lessons/round-41-verifier-spotcheck.md:69` (routed defect 1, closure finding,
corroborated). Fix in the round-42 counter is line-scoped:
`BACKTICK_RE = re.compile(r'`([^`\n]+)`')` (`measure.py:79`); shown able to fail by
selftest `T1_old_extractor_misses` / `T1_new_extractor_sees` (`measure.py:294-296`;
both OK in `c1-selftest.stdout:1-2`).

## Draft `## Mistakes` rows (for corpus/lessons/round-42.md)

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| calibration m10 — a wave receipt asserts `present:false` for a report that exists (receipt written before the report it describes), with no covering superseding receipt | `.ufo/waves/round-41/residual/receipt.json:14-17` vs file `.ufo/waves/round-41/residual/ResidualReceipts.md` present; base receipt `.ufo/evidence/round-42/before/c1-at-base.stdout:1` (`MISMATCH m10 …`) | none (routed round-41 spotcheck defect 2; unfixed at base) | C1 m10 counter class + superseding-receipt rule (`measure.py:38-42,199-202`); shown able to fail by selftest `T2_stale_counts`/`T2_superseded_clears`/`T2_junk_supersede_still_counts`/`T2_partial_supersede_still_counts` (`c1-selftest.stdout:3-6`; `measure.py:304-315`) and base receipt `c1-at-base.stdout` |
| calibration m8 — newline-spanning backtick regex in the round-41 C1 counter skips cited paths inside mispaired spans (`corpus/SOURCES.md` skipped round 41) | `corpus/lessons/round-41-verifier-spotcheck.md:69`; selftest `T1_old_extractor_misses` (`c1-selftest.stdout:1`) | round-41 verifier spot-check closure finding (hyaku @m_flash), corroborated | line-scoped extractor `BACKTICK_RE = r'`([^`\n]+)`'` (`measure.py:79`); shown able to fail by selftest `T1_old_extractor_misses`/`T1_new_extractor_sees` (`c1-selftest.stdout:1-2`; `measure.py:294-296`) |

## Limits

- I did not execute the counter or touch repo state (read-only seat); all quoted
  outputs are committed receipts read as files (`before/c1-at-base.stdout`,
  `before/c1-selftest.stdout`), not reruns.
- Not checked: whether the round-42 counter itself passes at the measurement
  revision (deciding run belongs to the L1; base only documented).
- Tooling: no tools installed or updated this seat.
