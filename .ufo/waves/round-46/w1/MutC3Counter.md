seat: MutC3Counter
item: mutation-audit of the round-46 C3 coverage counter's `--selftest` (24 cases): one minimal mutant per rule across 22 rules

Target: `.ufo/evidence/round-46/coverage/measure.py` (lane copy never edited). Scratch copy `/tmp/tameshi-r46-MutC3Counter/measure.py` (from lane bytes, sha256 `f8bfefdf6c08ce880c3f329018d946168dd022c50391d24551853326dbcfb5f5`), mutated in place one rule at a time, restored from `pristine.py` (same lane bytes) after every run. The detector was only ever run as `python3 measure.py --selftest` inside `/tmp/tameshi-r46-MutC3Counter/` — no deciding runs, no verdicts, no lane writes, no lane git/jj commands, no tool installs (python3/git/coreutils only).

Baseline (pristine): `python3 measure.py --selftest` → `C3_R46_SELFTEST: cases=24 failed=0` / `VERDICT: PASS` / exit 0.

Result: 18 killed, 4 survived.

| # | rule | mutation (line in scratch copy) | verdict |
|---|------|--------------------------------|---------|
| M01 | doc_key normalization | dropped `.rstrip('/')` (line 68) | killed |
| M02 | three frozen documents | DOCS[0] `2504.16777`→`2504.16778` (line 44) | killed |
| M03 | status mined | `!= 'mined'`→`!= 'queued'` (line 105) | killed |
| M04 | 0-3-space row indent | ROW_RE `{0,3}`→`{0,4}` (line 48) | killed |
| M05 | 13 cells | `!= 13`→`!= 12` (line 105) | killed |
| M06 | snapshot prefix | SNAP_PREFIX `sources/`→`source/` (line 41) | **survived** |
| M07 | snapshot present | `if data is None: continue`→`data = b''` (lines 114-115) | **survived** |
| M08 | sha prefix match | `digest.startswith(h)`→`endswith` (line 117) | killed |
| M09 | provenance trio | dropped `not lines[0].startswith('source:')` (line 126) | killed |
| M10 | verified-at floor | MIN_VERIFIED `2026-10-25`→`2026-10-24` (line 54) | killed |
| M11 | recheck line | `'recheck:'`→`'checked:'` (line 134) | killed |
| M12 | cited-row filter | dropped `if c in rows` (line 128) | killed (crash) |
| M13 | used-by membership | filter→`cited = list(cited)` (line 136) | killed |
| M14 | quote token bounds 6..25 | lower bound `6`→`7` (line 143) | killed |
| M15 | quote located in cited snapshot | location test→`bool(cited)` (line 143) | killed |
| M16 | fresh-quote-vs-package (incl. missing copy) | `package_text is None or …`→`is not None and …` (line 145) | killed |
| M17 | README index (both forms) | dropped short-form disjunct (line 170) | killed |
| M18 | rows>=3 | MIN_ROWS `3`→`2` (line 55) | **survived** |
| M19 | entries>=3 | MIN_ENTRIES `3`→`2` (line 56) | **survived** |
| M20 | indexed==entries | dropped conjunct (lines 176-177) | killed |
| M21 | covered==rows | dropped conjunct (lines 176-177) | killed |
| M22 | self_pin | digest comparison dropped, `int(blob is not None)` (line 158) | killed |

All runs: `python3 measure.py --selftest > logs/M<NN>.log 2>&1` in the scratch dir; verdict = presence/absence of `VERDICT: PASS`.

## Survivors (coverage findings — selftest gaps, not contract changes)

- **M06 snapshot prefix (line 41).** `SNAP_PREFIX = '…/coverage/source/'` (singular): `C3_R46_SELFTEST: cases=24 failed=0` / `VERDICT: PASS` / exit 0. The constant is self-consistent everywhere: `row()` writes it into fixture rows, SNAP_RE is built from it, `build()` writes snapshots at it, and T12 probes a prefix that is wrong relative to *any* constant (`SNAP_PREFIX.replace('round-46','round-45')` → still mismatched → `rows=0`, want `rows=0`). No case pins the literal round-46 path against the counter, so the mutated predicate (rows must cite `…/coverage/source/…`) is invisible to the selftest. Killing shape: a case asserting a row with a hand-written round-46 `coverage/sources/` anchor is admitted while a `coverage/source/` anchor row is not.
- **M07 snapshot present (lines 114-115).** Missing-snapshot skip replaced by `data = b''`: `cases=24 failed=0` / `VERDICT: PASS`. T13 (`T13_missing_snapshot_empty_digest`) passed identically under mutant and pristine (`PASS T13_missing_snapshot_empty_digest want='rows=0' got=… rows=0 …` in both logs/M07.log and baseline) — because `build()` never deletes snapshots, the files written by earlier cases (T01+) persist in the fixture repo and are committed again, so `tree.read()` succeeds and `rows=0` comes from the digest mismatch, never from `data is None`. The `data is None` guard is never exercised. Killing shape: T13 with snapshots actually absent — then `sha256(b'').hexdigest()` = `e3b0c442…`, which is exactly the `h='e3b0c442'` the case pins, so rows would be 3 and T13 would fail [INFERENCE from committed constants; the flip itself was not run because it needs a second selftest edit, outside the one-mutation-per-rule probe].
- **M18 rows>=3 (line 55).** `MIN_ROWS = 2`: `cases=24 failed=0` / `VERDICT: PASS`. Every case that reduces rows also fails on another axis: T18 (`rows=2`) is still false via `entries=2 < MIN_ENTRIES`, and the true-cases all have rows=3 ≥ 2. The lower side of the threshold is unpinned; only `MIN_ROWS ≥ 4` would trip T01/T10/T16/T22.
- **M19 entries>=3 (line 56).** `MIN_ENTRIES = 2`: `cases=24 failed=0` / `VERDICT: PASS`. Every entries=2 case (T03/T04/T14/T15/T21) is simultaneously false via `covered=2 != rows=3`, so the entries threshold's lower side is never the deciding conjunct.

## Killing cases (first decisive selftest line per killed mutant)

```
M01 FAIL T01_three_pass want='C3_R46_PASS=true' got=C3_R46: self_pin=1 rows=2 entries=2 indexed=2 covered=2 row_ids=S258,S260 rev=m C3_R46_PASS=false   (S259 dropped: urls[1] keeps its trailing slash)
M02 FAIL T09_unlisted_url want='rows=2' got=C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 rev=m C3_R46_PASS=true        (mutated doc id makes the "unlisted" 2504.16778 listed)
M03 FAIL T01_three_pass want='C3_R46_PASS=true' got=C3_R46: self_pin=1 rows=0 entries=0 indexed=0 covered=0 row_ids=- rev=m C3_R46_PASS=false             (and T08 inverted: queued rows=3)
M04 FAIL T11_four_space_row_ignored want='rows=2' got=C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 rev=m C3_R46_PASS=true
M05 FAIL T01_three_pass want='C3_R46_PASS=true' got=C3_R46: self_pin=1 rows=0 entries=0 indexed=0 covered=0 row_ids=- rev=m C3_R46_PASS=false             (15 case failures)
M08 FAIL T01_three_pass want='C3_R46_PASS=true' got=C3_R46: self_pin=1 rows=0 entries=0 indexed=0 covered=0 row_ids=- rev=m C3_R46_PASS=false             (15 case failures)
M09 FAIL T14_no_source_prefix want='entries=2' got=C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 rev=m C3_R46_PASS=true
M10 FAIL T03_old_verified_at want='entries=2' got=C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 rev=m C3_R46_PASS=true
M11 FAIL T01_three_pass want='C3_R46_PASS=true' got=C3_R46: self_pin=1 rows=3 entries=0 indexed=0 covered=0 row_ids=S258,S259,S260 rev=m C3_R46_PASS=false (11 case failures; T15 also flipped)
M12 FAIL T06_bad_sha_prefix want='rows=2' got=NO-OUTPUT  File "…/measure.py", line 136, in entry_ok / KeyError: 'S258'                                    (crash kill: entries cite ids excluded from rows; 7 NO-OUTPUT cases: T06,T08,T09,T11,T12,T13,T18)
M13 FAIL T05_not_in_used_by want='entries=1' got=C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 rev=m C3_R46_PASS=true
M14 FAIL T22_fresh_quote_passes want='C3_R46_PASS=true' got=C3_R46: self_pin=1 rows=3 entries=2 indexed=2 covered=2 rev=m C3_R46_PASS=false               (6-token fresh quote 'environments change flake rates between pipelines' excluded; T21 also flipped)
M15 FAIL T04_quote_absent want='entries=2' got=C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 rev=m C3_R46_PASS=true
M16 FAIL T01_three_pass want='C3_R46_PASS=true' got=C3_R46: self_pin=1 rows=3 entries=0 indexed=0 covered=0 row_ids=S258,S259,S260 rev=m C3_R46_PASS=false (9 case failures: no package copies → nothing counts as fresh)
M17 FAIL T01_three_pass want='C3_R46_PASS=true' got=C3_R46: self_pin=1 rows=3 entries=3 indexed=0 covered=3 row_ids=S258,S259,S260 rev=m C3_R46_PASS=false (T07, T22 also flipped; T16 full-path form still passed)
M20 FAIL T19_unindexed_is_false want='C3_R46_PASS=false' got=C3_R46: self_pin=1 rows=3 entries=3 indexed=2 covered=3 row_ids=S258,S259,S260 rev=m C3_R46_PASS=true
M21 FAIL T24_two_entries_one_row_is_false want='C3_R46_PASS=false' got=C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=1 row_ids=S258,S259,S260 rev=m C3_R46_PASS=true
M22 FAIL T20_self_pin_broken want='C3_R46_PASS=false' got=C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 rev=m C3_R46_PASS=true
```

(Logs with full 24-case output kept at `/tmp/tameshi-r46-MutC3Counter/logs/M<NN>.log`; mutated bytes at `logs/M<NN>.mutated.py`.)

## Restoration evidence

- After every mutant: `cp pristine.py measure.py` — restored sha256 `f8bfefdf6c08ce880c3f329018d946168dd022c50391d24551853326dbcfb5f5` each time (22/22, printed per cycle).
- Mutated-bytes hashes per mutant: M01 `1a2440c3…`, M02 `51c9b237…`, M03 `e508934d…`, M04 `3fb43872…`, M05 `d0c077c4…`, M06 `47d6b20d…`, M07 `78d7ebe4…`, M08 `38be47b4…`, M09 `1a6245b3…`, M10 `bc420937…`, M11 `9fa21fee…`, M12 `f3c5178f…`, M13 `2c6d8442…`, M14 `6d23fa28…`, M15 `d25a1e59…`, M16 `0aad15c2…`, M17 `3d90a882…`, M18 `e038a6d3…`, M19 `e059e788…`, M20 `1d8b3ac9…`, M21 `77479171…`, M22 `bf2b4e66…` (full digests in the shell transcript above).
- Final restored run: `python3 measure.py --selftest` → `C3_R46_SELFTEST: cases=24 failed=0` / `VERDICT: PASS` / exit 0.
- Lane integrity: `cmp` of lane `.ufo/evidence/round-46/coverage/measure.py` vs `pristine.py` → identical; lane sha256 `f8bfefdf6c08ce880c3f329018d946168dd022c50391d24551853326dbcfb5f5` before and after the whole audit.

## Bounds / unrun checks

- Counter runs: `--selftest` only, inside the scratch dir. No `--lane/--rev` run was taken by this seat (bounds: deciding runs are the L1's) — unrun, intentionally.
- No tool installs or upgrades were needed or made (no pacman, no uv/npm).
- Per the role: the 4 surviving mutants are coverage findings about the selftest, not permission to change the counter or contract; nothing outside the scratch copy and this report was modified.
