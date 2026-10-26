# T48W2MutC2CounterB — mutation audit of the frozen C2 freshness counter

Seat: T48W2MutC2CounterB (a2w1, tameshi round 48 attempt 2). Target of attack:
`.ufo/evidence/round-48/freshness/measure.py`, frozen at sha256
`faefe9b442741bcd7238ffe028841a0da7453c14c70f9f33afbd0f77be2df63f`
(freeze-2.json: `freshness/measure.py.sha256`, byte-identical to the w1 file).
Detector: the counter's own `--selftest` (43 built-in cases), run as
`TMPDIR=$S python3 $S/measure.py --selftest` on a scratch copy only. A probe is
never a verdict; every survivor below is a coverage finding against the selftest,
not a change to the C2 contract.

## Baseline and method

- Frozen bytes copied to `/fast/scratch/hyaku/tameshi-r48/T48W2MutC2CounterB/measure.py`;
  arrival sha256 equals the frozen sha (`sha256sum` both — identical).
- Pristine detector run (python 3.14.8): exit 0, `C2_R48_SELFTEST: cases=43 failed=0`,
  5.0 s wall, empty stderr. Baseline passes, so no mutant is inconclusive-by-baseline.
- 44 mutants specified, 43 applied (first F2 old-string was non-unique — wrong
  indentation — and was re-specified; all applied mutants matched exactly one site,
  `raw.count(old)==1` asserted, 43/43 distinct mutant hashes).
- After every mutant run the pristine bytes were restored in the same step and
  `sha256 == faefe9b4…` asserted; final tree sha equals the frozen sha. The lane
  file itself was never written.
- Mutant sha256 prefixes (before-restore values) are recorded in the table; before
  every mutant the bytes were the pristine frozen sha above.

## Result totals

killed 30 · survived 13 (one of them an equivalent/dead-branch mutant) · 1
re-specified. All file:line refer to the frozen counter.

| id | site | mutation (old → new) | verdict | killing case(s) / survivor rationale | mutant sha |
|----|------|----------------------|---------|--------------------------------------|-----------|
| A1 | :105 | GATE_RE `^- C2-QUOTE` → `^- c2-quote` | killed | positive_all_four +39 (40 fail) | d65db2e0cd19c98d |
| A2 | :105 | `([^`]+)` → `([^`]*)` | **SURVIVED** | S1 below — empty backtick quote accepted by the regex; still fails later as `quote=empty`, so verdict-neutral, but the amendment-2 `+` is unpinned | f9551c73aa688823 |
| A3 | :105 | drop `:` before backtick | killed | positive_all_four +39 | fca629e122fc18fe |
| A4 | :105 | `^- C2-QUOTE` → `^ *- C2-QUOTE` | **SURVIVED** | S2 below — indented gate lines become acceptable; amendment 2 pins `^-`; no indented fixture line | fa99a3155ebc032c |
| B1 | :174 | `(script|style)` → `(scripts|style)` | killed | quote_script_only | e7bef756839deb3f |
| B2 | :175 | tag strip `<[^>]*>` → `<x[^>]*>` | **SURVIVED** | S3 below — stripping disabled; no fixture quote spans a tag boundary | 8b7ab93c1e2d5259 |
| B3 | :176 | `html.unescape(text)` → `text` | killed | quote_entity_unescape | dfd49fe55d41b89f |
| B4 | :167 | collapse `' '.join` → `''.join` | killed | quote_26_words (word count collapses to 1) | f33a35e521c58293 |
| B5 | :257 | `gzip.decompress(raw)` → `raw` | killed | snapshot_bad_gzip, snapshot_gz | 9efc5fb8cf0c1d2e |
| B6 | :173 | decode `'replace'` → `'strict'` | **SURVIVED** | S4 below — no invalid-UTF-8 fixture; crash path unpinned | 21dbb6c9811bdeaf |
| B7 | :174 | drop `\|Z` fallback in script/style closer | **SURVIVED** | S5 below — unterminated `<script>` contents kept; all fixture scripts closed | 2cb95243f043af77 |
| C1 | :100 | `MAX_WORDS = 25` → `24` | killed | quote_25_words | c727f5b98db12261 |
| C2 | :100 | `MAX_WORDS = 25` → `26` | killed | quote_26_words | aae40afb40822e7e |
| C3 | :303 | `words > MAX_WORDS` → `>=` | killed | quote_25_words | aa5c591691a2fb29 |
| D1 | :89 | drop S093's `--unshare-cgroup-try` | killed | phrases_s093_needs_both | a58e0ae391ec7f8a |
| D2 | :87 | S026 `84%` → `85%` | killed | positive_all_four +9 | 52663cba05dea0cf |
| D3 | :312 | `REQUIRED[t]` → `REQUIRED[t][:1]` | killed | phrases_s093_needs_both (all-phrases rule pinned) | 6640a8c4caf1ce62 |
| E1 | :325 | `lines[:10]` → `lines` | killed | entry_source_beyond_ten_lines | 84e4b6bd6a416245 |
| E2 | :329 | `OPENED not in verified` → `'2026-' not in verified` | killed | entry_verified_at_wrong | 3fdac19cb016f3e9 |
| E3 | :331 | usedby `!= set(want)` → `<=` | killed | entry_usedby_empty | bebbb68e781f927b |
| E4 | :106 | ID_RE `{3,}` → `{4,}` | killed | positive_all_four +39 | f8de55f646996832 |
| E5 | :325 | `lines[:10]` → `lines[:11]` | **SURVIVED** | S6 below — the 10-line boundary is not pinned at 10 | 33cfc074c6a1e22d |
| F1 | :391 | census `return proc.returncode` → `return 0` | killed | census_nonzero | a2eed53d9f3e7175 |
| F2 | :447 | verdict drop `and code == 0` | killed | census_nonzero | 89aae010e6d87a72 |
| F3 | :380-381 | census-absent `return 127` → `return 0` | **SURVIVED** | S7 below — sharpest survivor: the never-credit branch is unreachable in selftest | 208495dbfbc73949 |
| G1 | :448 | `if live:` → `if not live:` (label swap) | killed | positive_all_four +8 (expects `C2_R48_PASS=true`; PARTIAL swap surfaced) | 7e28450aca108202 |
| G2 | :338 | `return 'skipped'` → `return 'ok'` | **SURVIVED (equivalent)** | S8 below — dead branch; measure() calls check_live only when live is truthy | d04f00bcd30ca21b |
| G3 | :350 | live contains-check → `return 'ok'` | killed | live_absent | 5e986b1c5140fc06 |
| G4 | :340-341 | no-url/no-quote `return 'absent'` → `return 'ok'` | **SURVIVED** | S9 below — receipt_absent case never asserts the live field | bce2205b2e893fa8 |
| G5 | :348 | drop `or not raw` | **SURVIVED (field-only)** | S10 below — empty fetch body flips `unreachable`→`absent`; verdict-neutral | c1c53f321e78886e |
| G6 | :191 | live_fetch gzip encoding `'gzip'` → `'GZIP'` | **SURVIVED** | S11 below — live_fetch (incl. gzip) has zero selftest coverage (fetch injected) | ce24b54d82e42dfe |
| H1 | :437 | `refreshed += 1` → `+= 2` | killed | positive_all_four +39 | 534660b6621a2b25 |
| H2 | :435 | drop live conjunction from `ok` | killed | live_absent, live_unreachable | a56468cf0591f435 |
| H3 | :446 | `self_pin == 1` → `>= 0` | killed | self_pin_mismatch | 64645275c03dbc16 |
| H4 | :446 | `refreshed == len(TARGETS)` → `>= 3` | killed | row_none (expects `C2_R48_PASS=false` at refreshed=3) | 448409e3c7c89b44 |
| H5 | :418 | drop `and row_state == 'ok'` from grading gate | **SURVIVED** | S12 below — stop-at-first-failure `-` grading unpinned | d99b4254308167c2 |
| I1 | :216 | `> MIN_NEW_ID` → `>=` (S264) | **SURVIVED** | S13 below — "id above S264" boundary unpinned | b5da178d530daca8 |
| I2 | :214 | prefix drops U+2014 | killed | row_ascii_hyphen | c9601ba05f7e92a0 |
| I3 | :219 | `len(cands) > 1` → `> 2` (row dup) | killed | row_ambiguous | 623beb8b9fbdd9c2 |
| I4 | :252 | `digest[:12]` → `[:13]` | killed | positive_all_four +39 | 61df09183b2d5ce8 |
| I5 | :276 | fetched_at `startswith(OPENED)` → `== OPENED` | killed | positive_all_four +39 | 7a3d43a10455943f |
| I6 | :235 | receipt-exclusion `endswith(...)` → `False` | killed | positive_all_four +39 (snapshot ambiguous) | ac378e74f7d1ee51 |
| I7 | :282 | `'bytes' not in data` → `'zzz' not in data` | killed | receipt_bytes_missing | 09d88d6ef1fffe2a |

## Survivor findings (coverage, ordered by severity)

Each names file:line and the command that shows it. Commands run from the lane
root; `S=/fast/scratch/hyaku/tameshi-r48/T48W2MutC2CounterB`.

- **S7 (F3) census-absent exit never credited — unpinned.**
  `measure.py:380-381` `if not os.path.isfile(CENSUS): return 127`. Mutant
  `return 0` survives `--selftest` because `CENSUS` is a host-absolute path that
  always exists (`ls -l /home/vgpnk/Projects/shokunin/scripts/sources-census.sh`).
  One token turns the "never credited" anti-cheat exit into a pass; the contract
  clause "127 when the tool is absent — never credited" has no selftest case.
  Killing fixture would need a case run with the census tool made absent.
- **S13 (I1) S264 boundary unpinned.** `measure.py:216`
  `int(r['id'][1:]) > MIN_NEW_ID` with `MIN_NEW_ID = 264` (:97). `>=` survives: no
  fixture registry row carries id S264 (`grep -n 'S264' $S/measure.py` shows it
  only in gate-line fixtures, never as a registry row). A superseding row with id
  S264 — excluded by the contract's "id above S264" — would be graded.
- **S12 (H5) stop-at-first-failure grading unpinned.** `measure.py:418`
  `if row is not None and row_state == 'ok':`. Dropping `and row_state == 'ok'`
  survives: for `row_opened_wrong` the mutant still prints `row=opened` and stays
  `NOT`, so every needle in the selftest still matches. The docstring's promised
  shape "later fields print `-`" (:33-35) is asserted nowhere; a regression that
  over-reports later fields would pass all 43 cases.
- **S6 (E5) the "first 10 lines" bound is not pinned at 10.** `measure.py:325`
  `lines[:10]`. `lines[:11]` survives: `entry_source_beyond_ten_lines` places
  `source:` at line 15 (12 fillers), far past either cut. A fixture with
  `source:` on exactly line 11 (index 10) would kill it.
- **S2 (A4) indented gate lines accepted.** `measure.py:105` GATE_RE anchors
  `^- C2-QUOTE`; `^ *- C2-QUOTE` survives. Amendment 2 fixes the shape as "a line
  … matching `^- C2-QUOTE …`"; an indented Gate line (e.g. nested list) is
  currently excluded and would become gradable. No fixture line is indented.
- **S3 (B2) tag-strip drop survives.** `measure.py:175`. With tags kept, every
  fixture quote is still a substring (tags sit outside the quoted spans). A
  snapshot like `about <b>84%</b> of the transitions…` — which amendment-2
  extraction makes quotable — would be graded `quote=absent` (false negative).
  No fixture quote spans a tag boundary.
- **S4 (B6) decode error path unpinned.** `measure.py:173`
  `raw.decode('utf-8', 'replace')`. `'strict'` survives: no fixture body is
  invalid UTF-8. Under the mutant a non-UTF-8 snapshot aborts the whole counter
  (uncaught `UnicodeDecodeError`) instead of grading the field.
- **S5 (B7) unterminated script/style unpinned.** `measure.py:174` closer
  `(?:</\1\s*>|\Z)`; dropping `\Z` survives because both `quote_script_only` and
  `quote_style_only` close their elements. An unterminated `<script>` containing
  the quote would then be graded `quote=ok` — a false positive.
- **S9 (G4) live=absent on missing receipt URL unpinned.** `measure.py:340-341`.
  `return 'ok'` survives: `receipt_absent` asserts only `receipt=absent` and
  `refreshed=3`, never the live field. The TARGET line would report `live=ok`
  with no fetch at all (verdict stays false via receipt, but the reported field
  lies).
- **S11 (G6) live_fetch itself untested.** `measure.py:185-193` (incl. the
  `Content-Encoding: gzip` decompress at :191-192). `--selftest` injects `fetch`
  (:772-778), so the real fetcher — timeouts, HTTP status, gzip bodies — has zero
  coverage. A gzip-served receipt URL would surface only at the deciding run.
- **S1 (A2) empty-backtick quote regex unpinned.** `measure.py:105`
  `([^`]+)` → `([^`]*)` survives; verdict-neutral downstream (`quote=empty`),
  but the amendment-2 capture shape is unpinned.
- **S10 (G5) empty fetch body unpinned (field-only).** `measure.py:348`. Dropping
  `or not raw` flips an empty body from `live=unreachable` to `live=absent`; both
  are non-refreshing, so the verdict is unchanged — unpinned field semantics only.
- **S8 (G2) dead branch — equivalent mutant, not a gap.** `measure.py:337-338`
  `if not live_on: return 'skipped'` is unreachable: `measure()` calls
  `check_live` only when `live` is truthy (:429-430), and `--no-live` reporting
  comes from the fields default (:417). Harmless, but it invites the false belief
  that `check_live` implements `--no-live`.

## Killed-mutant notes worth recording

- The S093 "all required phrases" rule is doubly pinned: dropping the second
  phrase (D1) and truncating the loop to the first phrase (D3) are both killed by
  `phrases_s093_needs_both`.
- The word bound is pinned from both sides (24 and 26 both killed) and at the
  comparison operator (C3).
- The census exit enters the verdict through both the return value (F1) and the
  predicate conjunction (F2) — each alone is killed by `census_nonzero`.
- `--no-live` PARTIAL labelling is pinned (G1): swapping the label branch breaks
  nine cases, including `positive_all_four` (`C2_R48_PASS=true` expected) and
  `no_live_partial` forbids `C2_R48_PASS=`.

## Observations (not mutants)

- freeze-2.json cites the frozen counter's selftest receipt at
  `freshness/selftest/c2-r48-selftest.stdout`; that path is absent from the tree
  right now (`ls .ufo/evidence/round-48/freshness/selftest/` → no such file or
  directory; the directory holds only `measure.py`, `__pycache__/`, `sources/`).
  Presumably lands with the deciding run's receipts-only commit (amendment 8).
  My pristine baseline (`cases=43 failed=0`) reproduces the recorded summary.
- The detector's `census_nonzero` case depends on the real fleet census script
  (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, read-only invoked;
  its work tree is materialised under TMPDIR inside the scratch dir), so the
  selftest is not hermetic w.r.t. that host path — related to S7.

## Bound compliance

- Lane checkout untouched except this report file; no lane git/jj mutation; no
  writes under `corpus/`, `tools/`, `SCORECARD.md`, or the fleet repo. The lane
  counter's sha256 was `faefe9b4…` before the sweep and after it (read-only).
- All fixtures, clones and temp files lived under
  `/fast/scratch/hyaku/tameshi-r48/T48W2MutC2CounterB` (also set as TMPDIR for
  every run, so the selftest's `tempfile.mkdtemp` fixture repos landed there);
  the selftest's own throwaway git repos always verified `rev-parse
  --show-toplevel` equals the fixture root (that check is built into the
  counter's `Fixture` class).
- disk-guard checked before the pass: `/fast/scratch/hyaku` at 26 %, 599.5 G
  free; no ENOSPC.
- No tools installed or upgraded (none needed); no pacman transactions.
- Scratch dir deleted at the end of the run; see the cleanup line in the final
  report message.
