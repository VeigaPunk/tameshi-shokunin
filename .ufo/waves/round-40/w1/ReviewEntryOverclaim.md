# ReviewEntryOverclaim — r40-write-form-misses.md sentence the counters do not measure

## Finding (unmeasured claim, with paraphrase drift)

`corpus/knowledge/r40-write-form-misses.md:14` — "S152's abstract says fragility and lack of context **in snapshot files** can lead to false positives."

Neither counter reads this file or S152:
- `python3 .ufo/evidence/round-40/census/measure.py --lane … --rev …` checks only the v2/v1 tool shas, `classify_text` on `fixtures.json`, the selftest, two mutants, and lines in `tools/registry-replay.py` / `tools/bash-witness-study.py` (measure.py:189-221).
- `python3 .ufo/evidence/round-40/s108/measure.py --lane … --rev …` checks only the S108 snapshot sha and stripped quote.
Line 14's truth value is invisible to both; `C1_R40_PASS=true` and `C2_R40_PASS=true` are attainable with the sentence deleted or materially false.

Drift against the pin: the committed excerpt `.ufo/evidence/round-40/sources/s152-excerpt.txt:5-7` reads "drawbacks such as fragility and lack of context can lead to false positives, making it challenging for developers to interpret test failures" — the drawback is on snapshot **tests**/failure interpretation, not "snapshot files". The live PDF (sha256 `65f9603f364d9e811312600b0a161943cdae09fe1dbd53dbe4f19e0699a89703`, re-fetched today, matches the pinned sha in `corpus/lessons/round-40.md:13`) contains the same sentence. The qualifier "in snapshot files" is the entry's own narrowing, not in the source. The sibling entry `corpus/knowledge/r6-snapshot-practice-corpus.md:10` quotes verbatim and avoids the drift. Minor severity: the substance (fragility → false positives) is supported; only the object wording is added.

## Verified-true sentences (in scope, no defect)

- `:10` "`expected.json` on `.write_bytes` is an expected-path token for v2, not v1": v2 `EXPECTED_RE` contains `expected\.json` (write-path-census-v2.py:24); v1 `V1_EXPECTED_RE` does not (measure.py:38-40, `\.expected\b` requires a literal dot). Measured via `planted_ok` + `v1_bytes==0`.
- `:10` "`os.replace(` is a write site for v2 and not for v1": v2 `WRITE_RE` has `os\.replace\s*\(` (:20); v1 `V1_WRITE_RE` does not (measure.py:33-37). Measured via `replace_unflagged` + `v1_replace_writes==0` + `mutant_replace_killed`.
- `:10` discriminating-set claim holds: fixtures.json has `/tmp` in `scratch_replace` (line 6) and `--update_goldens` in both flagged cases; counter requires all three `==0`.
- `:18` live hits are exactly the two named sites: `grep` finds one `.write_bytes('expected.json')` (registry-replay.py:123, inside `publish`) and one `os.replace(tmp, path)` (bash-witness-study.py:778, destination is variable `path` as :18 admits). `tools/evidence-disposition.py:1759` writes `evidence / "expected.json"` only via `_write_bytes` helper — missed by both patterns, consistent with the file's own incompleteness disclaimer and `corpus/lessons/round-40.md:56`.
- `ground:`/`verified-at:`/`opened 2026-10-24` header claims: r39 contract pins v1's sha `bc8c660…` as the round-39 census tool, and round-39 lessons:49 records the same misses — accurate, though likewise unmeasured by counters.

## Verdict

One unmeasured sentence found (line 14, first clause): provenance attribution carrying a small unquoted qualifier. No falsifiable predicate violation — the sentence is substantively true per the sha-pinned PDF and committed excerpt. Residual risk: this file's provenance block (`:1-4`) and `:14` are entirely outside both counters' coverage; any error there would survive a green run.
