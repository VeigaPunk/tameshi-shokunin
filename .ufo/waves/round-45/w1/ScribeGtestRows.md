seat: ScribeGtestRows
(runtime id ScribeGtestRows-3; w1, round 45, lane tameshi-shokunin; date 2026-10-25)

## 1. Scope and bounds compliance

- Contract read first: `.ufo/evidence/round-45/contract.json` (frozen; never edited). SOURCES.md contract read: `/home/vgpnk/Projects/shokunin/CORPUS.md` §SOURCES.md (frozen v1, incl. census commands). Tooling rules read: `/home/vgpnk/.omp/agent/RULES.md`.
- Lane checkout read-only except this report. Scratch only under `/tmp/tameshi-r45-ScribeGtestRows/` (created; rows.txt). No git/jj mutation, no campaign-tool or counter runs, no edits to the read-only package `/home/vgpnk/Projects/shokuknow` (opened read-only only).
- No tool installed or upgraded (nothing beyond curl/git/python3/awk needed).

## 2. Sources opened and evidence (file:line)

- Snapshots (committed at freeze): `.ufo/evidence/round-45/coverage/sources/googletest-advanced.md` (2457 lines), `googletest-primer.md` (482 lines), `googletest-testing.md` (1550 lines).
- `sha256sum` of the three snapshots (from `.ufo/evidence/round-45/coverage/sources/`):
  - `googletest-advanced.md` → `05546ed6db9221444a77702a9519b0f7e289cf8b281a7dcedcce893a2840d1c2` → prefix `05546ed6` (matches the brief).
  - `googletest-primer.md` → `03d756ab11521933cb59ef9bc081e7524e79c2dfbea496f6583ec166f819c26e` → prefix `03d756ab` (matches).
  - `googletest-testing.md` → `44c56c6198c6736bf2dc27c47391e4d481be70b36839e3c0073f273894d52d2b` → prefix `44c56c61` (REFUSED record, §5).
- Relevant section headings located in the snapshots:
  - `grep -nE '^## Sharing Resources' googletest-advanced.md` → `870:## Sharing Resources Between Tests in the Same Test Suite`; `grep -nE '^### Shuffling the Tests' googletest-advanced.md` → `1973:### Shuffling the Tests`.
  - `grep -nE '^## Test Fixtures' googletest-primer.md` → `205:## Test Fixtures: Using the Same Data Configuration for Multiple Tests {#same-data-multiple-tests}`.
- Package staged rows (read-only): `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md` lines 56 (S202 advanced.md), 57 (S203 primer.md), 58 (S204 Parameter generators). Line 56-57 full text read raw (carrier notes, bold markup, prose recheck cells all present).
- Guard receipt: `.ufo/evidence/round-45/assimilation/guard-map.json` → `"verdict": "admitted"`, `"map_ok": true`, `"safe_floor": "S256"`, `"map_floor": "S256"`, `"map_entries": 10`, `"registry_max": "S160"`, `"registry_rows": 115`, `"staged_max": "S255"` (identity S202/S203 and next-free maps refused — `analysis_refused`/`naive_map`).
- Lane registry: `corpus/SOURCES.md` last table row is S160 (grep of row lines ends at `| S160 |`); no S256/S257 rows exist yet.

## 3. Drafted rows S256 / S257 (11-column schema)

Draft (each line one row; no literal or escaped `|` inside any cell — checked, see below):

```
| S256 | Advanced GoogleTest Topics (googletest docs/advanced.md; Google) — https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/advanced.md | docs | A | the upstream normative statement of F3's determinism precondition — test order is undefined, shuffle and random-seed flags make an order-related failure reproducible | §Sharing Resources Between Tests in the Same Test Suite and §Shuffling the Tests @ commit cd8e73f067129f8489e35c7b51c7a68552b289d2, snapshot .ufo/evidence/round-45/coverage/sources/googletest-advanced.md sha256 05546ed6 | GoogleTest states test order is undefined, that --gtest_shuffle reveals bad dependencies between tests, and that the computed seed is printed so an order-related failure can be reproduced | mined | 2026-10-25 | 365d | corpus/knowledge/r8-gtest-order-and-seed.md |
| S257 | GoogleTest Primer (googletest docs/primer.md; Google) — https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/primer.md | docs | A | the upstream normative statement of F3's determinism precondition — a fresh fixture object per test keeps tests independent within a suite | §Test Fixtures: Using the Same Data Configuration for Multiple Tests @ commit cd8e73f067129f8489e35c7b51c7a68552b289d2, snapshot .ufo/evidence/round-45/coverage/sources/googletest-primer.md sha256 03d756ab | GoogleTest creates a fresh fixture per test and deletes it before creating the next one, so changes one test makes do not affect other tests | mined | 2026-10-25 | 365d | corpus/knowledge/r8-gtest-primer-independence.md |
```

Validation (commands and outputs):

- `awk -F'|' '{print NF}' /tmp/tameshi-r45-ScribeGtestRows/rows.md` → `13` `13` (11 columns; must print 13 — passes).
- `grep -c '\\|' /tmp/tameshi-r45-ScribeGtestRows/rows.md` → `0` (no escaped pipes).
- `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' /tmp/tameshi-r45-ScribeGtestRows/rows.md` → `2`.
- Column contract: kind `docs`, tier `A`, status `mined`, opened `2026-10-25`, recheck `365d`, used-by exactly `corpus/knowledge/r8-gtest-order-and-seed.md` / `corpus/knowledge/r8-gtest-primer-independence.md`; source = title — pinned raw URL at commit cd8e73f067129f8489e35c7b51c7a68552b289d2; anchor names section heading(s) + snapshot path + 8-hex sha256 prefix (05546ed6 / 03d756ab).

## 4. Gate block draft (for the round lesson, `## Gate`)

```
## Gate

Theme: C2 (coverage, sourced, assimilation) — adopt two GoogleTest upstream docs
from the read-only package shokuknow merge/tameshi as new rows S256/S257, each
cited by a re-grounded knowledge entry.

### Admit — S256 (new row): Advanced GoogleTest Topics (googletest docs/advanced.md)

- URL https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/advanced.md;
  access date 2026-10-25; snapshot .ufo/evidence/round-45/coverage/sources/googletest-advanced.md,
  sha256 05546ed6db9221444a77702a9519b0f7e289cf8b281a7dcedcce893a2840d1c2.
- Located quotes (grep -nF against the snapshot; each found exactly once at the cited line):
  - line 896 (15 words): "Remember that the test order is undefined, so your code can't depend on a test"
  - line 1977 (8 words): "This helps to reveal bad dependencies between tests."
  - line 1980 (8 words): "Therefore you'll get a different order every time."
- By-document id map: staged S202 -> S256 (package row text at SOURCES.append.md:56).

### Admit — S257 (new row): GoogleTest Primer (googletest docs/primer.md)

- URL https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/primer.md;
  access date 2026-10-25; snapshot .ufo/evidence/round-45/coverage/sources/googletest-primer.md,
  sha256 03d756ab11521933cb59ef9bc081e7524e79c2dfbea496f6583ec166f819c26e.
- Located quotes (grep -nF against the snapshot; each found exactly once at the cited line):
  - line 251 (12 words): "GoogleTest always deletes a test fixture before it creates the next one."
  - line 253 (12 words): "changes one test makes to the fixture do not affect other tests."
- By-document id map: staged S203 -> S257 (package row text at SOURCES.append.md:57).

Guard verdict: admitted on the whole collision map (receipt
.ufo/evidence/round-45/assimilation/guard-map.json: verdict "admitted",
map_ok=true, safe_floor=S256, map_floor=S256; the identity maps S202->S202 /
S203->S203 and the next-free maps S202->S161 / S203->S162 are refused by the
guard). Row ids S256/S257 are above the lane's registry max S160 and the guard's
safe floor.

Stripped from the campaign rows when adapting:
- (a) prose recheck cells: staged S202/S203 carried recheck prose ("365d — `curl -fsSL '…' \| grep -c '…'` (expect a non-zero count; the string was present in the copy opened 2026-10-24)"); adapted rows carry the bare cadence `365d`.
- (b) bold markup: staged source/teaches cells use `**…**` emphasis; adapted cells are plain text.
- (c) carrier notes in the source cell: S202's master-alias byte-identity note and S203's gtest_for_dummies.md 404/rename-history note are stripped (title + pinned URL remain).
- (d) scope trimmed to F3 only: S202's F10 mention and S203's F2 mention dropped; teaches condensed to one grounded sentence each.

### Refused / not adopted — package row S204 (r8-gtest-generator-contract.md)

- Staged package row S204 "Parameter generators (googletest docs/reference/testing.md)" — SOURCES.append.md:58; snapshot .ufo/evidence/round-45/coverage/sources/googletest-testing.md, sha256 44c56c6198c6736bf2dc27c47391e4d481be70b36839e3c0073f273894d52d2b.
- Judgment: REFUSED — the value-parameterized generator table is NOT a property-based generator contract for F10.
- Reason: the table under §INSTANTIATE_TEST_SUITE_P (googletest-testing.md lines 100-113: generators Range, Values, ValuesIn, Bool, Combine, ConvertGenerator) documents deterministic enumeration of fixed parameter sets for value-parameterized TEST_P instantiation: Range yields a bounded arithmetic sequence, Values a fixed set, ValuesIn values from a container/iterator range, Bool {false,true}, Combine the Cartesian product of its argument generators, ConvertGenerator a static_cast/function conversion of the generated values. The surrounding text (lines 140-235) describes factory-object type conversion and a dangling-string_view caveat — not generation semantics. No generator introduces randomness or a distribution, none shrinks, none searches for a counterexample, and no property/invariant semantics is stated; there is no falsification loop. F10's generator-craft contract (held rows S157, S182, S183) requires arbitrary-case generation with the generator as a first-class artefact whose quality bounds the found laws; this table does not meet that contract — it enumerates a static parameter list for repeated runs of the same test body.
- Flip condition: the row would be admitted if upstream states that these or further generators perform randomized/property-semantic generation (e.g., sampling distributions, shrinking) for property checks — or if the row is re-scoped to "value-parameterized deterministic enumeration as a test-repetition fixture practice" under a new frontier rather than F10.
```

## 5. Findings and handoff notes

- Both drafted rows pass the 11-column checks: `awk -F'|' '{print NF}'` prints `13` for each (census malformed-row rule), no literal/escaped `|` in any cell, snapshot sha256 prefixes match the anchored 8-hex values, quote lines verified with `grep -nF` (advanced 896/1977/1980; primer 251/253), all quotes ≤25 words.
- The C2 counter at the deciding revision additionally requires the two knowledge entries `corpus/knowledge/r8-gtest-order-and-seed.md` (S256) and `corpus/knowledge/r8-gtest-primer-independence.md` (S257) to exist with the provenance trio (`source:` line 1 citing the row id, `verified-at: 2026-10-25` line 2, `recheck:` line 3), to be listed in the row's used-by, to carry a 6-25-token quote of the cited snapshot, and to be indexed in `corpus/README.md`. Those are sibling seats' work (ScribeGtestOrder / ScribeGtestPrimer drafts exist at w1); S256/S257 presuppose them. The Gate quotes above are chosen to double as counter-locatable quote candidates.
- No lane file was edited; the only write is this report. No tool installed. Scratch: `/tmp/tameshi-r45-ScribeGtestRows/rows.md`.
