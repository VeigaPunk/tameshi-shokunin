seat: MutC1Counter

# C1 freshness counter — mutation audit of `--selftest` coverage

Target: `.ufo/evidence/round-45/freshness/measure.py` @ freeze `3310e7be` (437 lines).
Pristine sha256 `ba64041f49ffcf15bb0d881604a5fe3ccf9d24e56f72bef055035fbe3d27c6ed`
(= worktree file = `git show 3310e7b:…measure.py` blob; verified before and after).
The lane was never written; the detector is only ever `python3 measure.py --selftest`.
Mutants were applied to scratch copies only (`/tmp/tameshi-r45-MutC1Counter/measure.py`,
later my private `/tmp/tameshi-r45-MutC1Counter/c3/measure.py`), one minimal mutation at a
time, each restored/rebuilt from pristine bytes. No tools installed (none needed).

Baseline: `python3 measure.py --selftest` → rc=0, `C1_R45_SELFTEST: cases=19 failed=0`, `VERDICT: PASS`.

## Table — rule → mutation (measure.py:line) → selftest result → verdict

| Rule | Mutation (one minimal disable) | Selftest result | Verdict |
|---|---|---|---|
| URL exact match | L137 `entry.get('url') != row['url']` → `False` | `FAIL T2_url_mismatch got=verified` | killed |
| opened >= 2026-10-25 | L139 `< MIN_OPENED` → `False` | `FAIL T7_old_opened got=verified` | killed |
| snapshot present | L141 `if raw is None:` → `if False:` | `CRASH TypeError` (sha256(None)), no VERDICT | killed (crash) |
| snapshot-absent *reason* | L141-142 `return 'invalid','snapshot absent'` → `raw = b''` | rc=0 PASS (T9 still `invalid` via sha-mismatch) | **SURVIVED** (S9) |
| sha256 match | L143 `!= entry.get('raw_sha256')` → `False` | `FAIL T3_sha_mismatch got=verified` | killed |
| verdict whitelist `holds` | L147 `if verdict != 'holds':` → `if False:` | `FAIL T16_bad_verdict got=verified` | killed |
| quote length 6..25 (both bounds) | L151 `if n < 6 or n > 25:` → `if False:` | `FAIL T6_quote_too_short got=verified` | killed |
| quote length lower 6 | L151 `n < 6` → `n < 1` | `FAIL T6_quote_too_short` | killed |
| quote length upper 25 | L151 `n > 25` → `n > 26` | rc=0 PASS — T5's 26-token quote also fails presence, masking the bound | **SURVIVED** (S1) |
| quote present in snapshot | L157 `if quote not in text:` → `if False:` | rc=0 PASS — T4 (moon/stars) still fails overlap (shares only `score`) | **SURVIVED** (S2) |
| quote not copied from row | L160 `if quote.lower() in fold(cells).lower():` → `if False:` | `FAIL T19_quote_copied_from_row got=verified` | killed |
| content-word overlap >= 2 | L163 `if len(shared) < 2:` → `if False:` | `FAIL T8_boilerplate_no_overlap got=verified` | killed |
| unreachable needs evidence | L136 ternary → `return ('unreachable', 'ok')` | `FAIL T11_unreachable_needs_evidence` | killed |
| population combined | L97 predicate → `True` | `FAIL T15_population_bounds got=['S001','S002','S161']` | killed |
| population status `mined` | L97 `r['status'] == 'mined' and` → `True and` | `FAIL T15 got=['S001','S002']` | killed |
| population id <= S160 | L97 `int(rid[1:]) <= MAX_ID` → `True` | `FAIL T15 got=['S001','S161']` | killed |
| population URL present | L98 `MAX_ID and r['url']}` → `MAX_ID}` | rc=0 PASS — all T15 fixture rows have URLs | **SURVIVED** (S3) |
| row indent 0-3 spaces | L63 `r'^ {0,3}\|` → `r'^ {0,4}\|` | `FAIL T15 got=['S001','S003']` | killed |
| duplicate-entry refusal | L241 `if counts[rid] != 1:` → `if False:` | rc=0 PASS — no selftest case touches the counts loop | **SURVIVED** (S4) |
| review non-author | L204 drop `who == authors.get(rid)` | rc=0 PASS — S002 self-review is *also* skipped because `ExecA` is absent from the fixture report text | **SURVIVED** (S5, masked) |
| wave-seat membership | L204 drop `who not in seats` | `FAIL T17 fresh=['S001','S008']` | killed |
| seat non-empty output | L189 drop `.strip()` | rc=0 PASS — whitespace-only output untested | **SURVIVED** (S6) |
| report path prefix | L206 `if not report.startswith(...)` → `if False:` | rc=0 PASS — `read_text('/tmp/Rev.md')` is None, presence masks the prefix check | **SURVIVED** (S7) |
| report names id and reviewer | L209 whole check → `if not text:` | `FAIL T17 fresh=['S001','S006']` | killed (id half) |
| report names reviewer | L209 drop `or who not in text:` | rc=0 PASS — no case of seat reviewer absent from report | **SURVIVED** (S8) |
| dispute sinks agree (selftest arithmetic) | L390 `sorted(agreed - disputed)` → `sorted(agreed)` | `FAIL T17 fresh=['S001','S003']` | killed |
| dispute sinks agree (measure L254) | `fresh = len(agreed - disputed)` → `len(agreed)` | rc=0 PASS — `measure()` unreachable under `--selftest` | **SURVIVED** (S10) |
| self_pin | L256 `self_pin == 1` → `True` | rc=0 PASS — same structural gap | **SURVIVED** (S11) |
| fresh >= TARGET 50 | L256 `fresh >= TARGET` → `fresh >= 0` | rc=0 PASS — same structural gap | **SURVIVED** (S12) |

30 mutants, 18 killed, 12 survived. Survivor = mutation disables the rule and `--selftest`
still prints `VERDICT: PASS` → the rule is untested (a coverage finding, not a contract change).

## Killer cases — demonstrated on scratch (mutant+F fixture → FAIL; fixture alone → PASS)

Each was run twice on my private pristine copy: enriched-fixture-only (must stay PASS, proving
no false kill) and fixture+mutant (must FAIL, proving the case kills).

- **S1** (upper bound): T5' = 26-token quote *present* in the snapshot with >=2 overlap
  (`LONG26` sentence appended to `page`; `raw_sha256` recomputed). fixture-only PASS
  (`0a814f…`), mutant FAIL `T5_quote_too_long got=verified` (`ef4f6a…`).
- **S2** (presence): T4' quote `the score equals detected by the moon and stars` — absent but
  shares {score, equals, detected}. fixture-only PASS, mutant FAIL
  `T4_quote_absent got=verified`.
- **S3** (URL present): T15 row `| S004 | book only no url | … | mined | …` with no http(s) in
  the source cell. fixture-only PASS, mutant FAIL `T15 got=['S001','S004']`.
- **S5** (non-author, masked): the existing S002 self-review is double-masked —
  `reports[rep]='RevX RevY RevZ S001 …'` does not contain `ExecA`, so L209's reviewer-name
  check skips it even after the author check is removed. Adding `ExecA` to the report text:
  fixture-only PASS, mutant FAIL `T17 fresh=['S001','S002']`.
- **S6** (non-empty output): seat `RevZ` output `'   '` instead of `''`; pristine strips it,
  mutant admits it → FAIL `T17 fresh=['S001','S008']`.
- **S7** (report prefix): add `'/tmp/Rev.md': 'RevX S007 S008'` to the `reports` fixture so the
  path is readable; prefix check still skips it pristine, mutant counts S007 → FAIL.
- **S8** (reviewer named): review `{'id':'S008','reviewer':'RevX','report':rep2}` with
  `reports[rep2]='S008 rechecked today'` (id present, reviewer absent); mutant counts → FAIL.
- **S9** (snapshot-absent reason): T9 asserts state only; proposed kill: also assert
  `why == 'snapshot absent'` (selftest asserts `why` only in T19 today).

Structural survivors (measure-level, `main()` returns before `measure()` under `--selftest`):

- **S4** duplicate-refusal, **S10** measure-level dispute subtraction, **S11** self_pin,
  **S12** TARGET: sibling **MutC1Counter-2** owns the proposed `measure()`-level killer cases
  (their words, received 2026-10-25): `T23_measure_duplicate_refusal` (55 rows + duplicated
  S001 → fresh=54 invalid=2), `T24_measure_self_pin` (one-byte-different committed counter →
  self_pin=0 PASS=false), `T25_measure_dispute_and_target` (S002 with agree+dispute → fresh=1
  disputed=1 PASS=false; also pins TARGET). Cite those as theirs; my independent proposals
  (extract a pure `passed(self_pin, fresh)` / `fresh = agreed - disputed` helper and unit-test
  it) would cover the same gap without a fixture repo.

## Restoration evidence

- Lane file before and after: sha256 `ba64041f…3d27c6ed`, equal to the freeze blob
  (`git -C <lane> show 3310e7be:…measure.py | sha256sum`) and `git status --porcelain` clean
  for that path at both checks.
- Scratch copies restored to pristine and re-run: rc=0 `VERDICT: PASS`, sha match, both
  `/tmp/tameshi-r45-MutC1Counter/measure.py` and `…/c3/measure.py` end at `ba64041f…3d27c6ed`.
- Scratch-note: the shared root scratch is owned by sibling MutC1Counter-2 (their drivers
  rewrite/restore it per-mutant; their transient extended selftest briefly coexisted with my
  round-1 run). My round-1 battery ran against pristine bytes (baseline PASS verified first);
  all later probes ran in `c3/`. Coordinated via direct message; no lane bytes affected.

Commands: `python3 measure.py --selftest` on pristine/mutant/restored copies; mutant text
diffs are single-line replacements listed in the table above (driver: scratch `run.py`/`probes.py`).
No counter mode other than `--selftest` was executed; no pacman/install transactions.
