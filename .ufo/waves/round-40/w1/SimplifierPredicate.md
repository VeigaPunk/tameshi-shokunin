# W1 — C1 predicate sentence vs census/measure.py pass condition (SimplifierPredicate)

Scope: static comparison only. Default counter not run (frozen-run belongs to the L1). No live-lane edits.

## Verdict

**Match — no field divergence in either direction.** Every clause of the frozen C1 sentence
(`.ufo/evidence/round-40/contract.json`, `claims.C1.predicate`) is enforced by the counter's
`ok` conjunction, and every conjunct of that conjunction traces to a sentence clause. The code
is a strict superset: stricter only in ways that keep a conforming tool passing.

## Clause-by-clause map

All paths relative to lane root; `M` = `.ufo/evidence/round-40/census/measure.py`.

| # | Sentence clause | Code |
|---|---|---|
| 1 | v2 tool sha matches pin | M:128-138 — sha256 of `git show REV:tools/write-path-census-v2.py` vs `claims.C1.tool_sha256` read from contract at REV (`sha_ok`) |
| 2 | v1 sha still `bc8c660c…` | M:29 (`V1_SHA` constant identical), M:139-140 (`v1_sha_ok`) |
| 3 | planted `bytes_unflagged=1`, `replace_unflagged=1` | M:211-212 (`got[...][1]`) via v2 `classify_text` on fixtures.json |
| 4 | flagged cases and `scratch_replace` = 0 | M:213-215 (`bytes_flagged`, `replace_flagged`, `scratch_replace` all `== 0`) |
| 5 | embedded v1 patterns: `bytes_unflagged=0`, replace writes=0 | M:187-188, M:220 (`v1_misses`) using embedded `V1_WRITE_RE`/`V1_EXPECTED_RE` (M:33-40) |
| 6 | registry-replay.py ≥1 `expected.json` write_bytes line: v2 hits, v1 misses | M:189, M:195-199, M:221 (`live_json_v2 >= 1 and live_json_v1 == 0`) |
| 7 | bash-witness-study.py ≥1 `os.replace` line: v2 hits, v1 misses | M:190, M:203-209, M:221 (`live_replace_v2 >= 1 and live_replace_v1 == 0`) |
| 8 | removing `os\.replace\s*\(` or `expected\.json` kills selftest | M:30-31 (marks byte-identical to sentence's escaped forms), M:165-186 (single-occurrence mutants, nonzero-exit kill), M:228-229 (`killed_replace == 1 and killed_json == 1`) |

Sentence's "or" in clause 8 reads as "each removal individually fails the selftest" — code
requires both kills; equivalent.

## Reverse direction — code checks more than the sentence says

1. **Selftest echo + pristine exit** — M:216-218: pass additionally requires the tool's own
   `--selftest` stdout to report `bytes_unflagged='1'`/`replace_unflagged='1'` (parsed at
   M:96-104, tag `WRITE_CENSUS_V2_SELFTEST:`) and `rc.returncode == 0`. The sentence names only
   the classify results; `rc == 0` is the implied baseline of "makes the selftest fail", and the
   two echoed fields re-measure the same quantity through the tool's selftest path. Stricter,
   not divergent: a tool satisfying the sentence verbatim also satisfies these unless its
   selftest lies about its own classifier.
2. **v2 WRITE_RE on replay lines** — M:196 requires both `mod.EXPECTED_RE` and `mod.WRITE_RE`;
   the sentence names only the expected pattern. Harmless: candidate lines already must contain
   the `.write_bytes` literal (M:195), consistent with "write_bytes line".
3. **Mutant guards** — M:169/M:176 require the mark to vanish entirely after replacement; a v2
   tool with a second `os\.replace\s*\(` occurrence yields `killed_replace=0` → fail. Fails
   only in the false direction.

## Reading choices worth recording (match, with interpretation)

- Clause 5 "on those two planted cases" is enforced **per-case**: v1 `unflagged==0` only on the
  `bytes_unflagged` fixture (M:187) and v1 `writes==0` only on the `replace_unflagged` fixture
  (M:188). The stronger reading (both v1 metrics on both fixtures) is not enforced —
  e.g. v1 `write` count on the bytes fixture is unconstrained (M:220 checks only `[1]==0` on
  M:187's value). No conforming case is affected; noted as the sentence's natural reading.
- v1's replay miss (clause 6) is `V1_EXPECTED_RE` alone (M:198); the write side is fixed by the
  literal `.write_bytes` line filter (M:195). Note `V1_WRITE_RE` requires `.write_bytes\s*\(`,
  so a hypothetical `expected.json` line with `.write_bytes` but no paren would count as a v1
  hit and fail the pass — fails false only.
- Clause 1's "this pin" resolves **dynamically**: the counter reads `tool_sha256` from
  contract.json at REV (M:134-138), not a hardcoded digest. The contract is frozen and
  committed, so this equals the frozen pin `40228532…878b` unless contract.json itself differs
  at REV — in which case both sides of the equality move together. Equivalent in practice.
- Embedded-v1 patterns are the counter's own constants (M:33-40), matching the sentence's
  "embedded v1 patterns" and the contract's `do_nothing` clause.

## Commands used

- `read .ufo/evidence/round-40/contract.json` (frozen claims)
- `read .ufo/evidence/round-40/census/measure.py` (full 253 lines)
- `read tools/write-path-census-v2.py` (WRITE_RE/EXPECTED_RE/selftest wiring, lines 16-99)
- No counter executed in default mode; no lane writes.
