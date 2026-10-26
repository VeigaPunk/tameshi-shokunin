seat: T47MutC3Counter
item: mutation-audit of the round-47 C3 coverage counter's `--selftest` (24 cases, T01–T24): one minimal mutant per probe across all 22 named rules

Target: `.ufo/evidence/round-47/coverage/measure.py` (lane copy never edited; byte-identical to the scratch reference at audit end, `cmp` clean). Scratch copy `/tmp/tameshi-r47-T47MutC3Counter/measure.py` from lane bytes, sha256 `c8fb89e69196fc2401e2364142b848bd8d53e5c6e3d97f17c528951c9f894260`; `pristine.py` (same bytes) restored over it after every mutant, restore asserted by hash inside the harness. Detector only ever `python3 measure.py --selftest` in the scratch dir — no `--lane/--rev` run, no verdict, no lane writes, no lane git/jj commands, no tool installs (python3/git/coreutils only).

Baseline (pristine): `C3_R47_SELFTEST: cases=24 failed=0` / `VERDICT: PASS` / exit 0 (~3.4 s).

Result: 35 probes — 25 killed, 10 survived (6 survivor rules new vs round 46, 4 routed confirmations of `.ufo/waves/round-46/w1/MutC3Counter.md`).

## Table: rule -> mutation (line in scratch copy = lane bytes) -> result

| # | rule | mutation (line) | verdict |
|---|------|-----------------|---------|
| M01 | doc_key normalization | dropped `.lower()` (line 67) | **survived** |
| M02 | doc_key normalization | dropped `.rstrip('/')` (line 67) | killed |
| M03 | doc_key normalization | dropped `(www\.)?` from the strip regex (line 67) | **survived** |
| M04 | doc_key normalization | scheme strip narrowed `https?` -> `http` (line 67) | killed |
| M35 | doc_key normalization | `.lower()` -> `.upper()` (line 67) | **survived** (self-consistent, like M01) |
| M05 | three frozen documents | DOCS[0] `2302.09330` -> `2302.09331` (line 43) | **survived** |
| M06 | status mined | `!= 'mined'` -> `== 'mined'` (line 104) | killed |
| M07 | 0-3-space row indent | ROW_RE `{0,3}` -> `{0,4}` (line 47) | killed |
| M08 | 0-3-space row indent | ROW_RE `{0,3}` -> `{1,3}` (line 47) | killed |
| M09 | 13 cells | `len(cells) != 13` -> `!= 14` (line 104) | killed |
| M10 | snapshot prefix | SNAP_PREFIX literal `round-47` -> `round-46` (line 40) | killed (T12 only — see M34) |
| M34 | snapshot prefix | SNAP_PREFIX `coverage/sources/` -> `coverage/source/` (line 40) | **survived** |
| M11 | snapshot present | guard disabled: `if data is None: continue` -> `if False:` (lines 113–114) | **survived** |
| M12 | snapshot present | guard inverted `is None` -> `is not None` (line 113) | killed |
| M13 | sha prefix match | `if not any(digest.startswith(...)` -> `if any(` (line 116) | killed |
| M14 | provenance trio | dropped `not lines[0].startswith('source:')` (line 125) | killed |
| M15 | cited-row filter | dropped `if c in rows` (line 127) | killed (crash, see below) |
| M16 | cited-row filter | `if c in rows` -> `if c not in rows` (line 127) | killed |
| M17 | verified-at floor | MIN_VERIFIED `2026-10-25` -> `2026-10-24` (line 53) | killed |
| M18 | verified-at floor | `m.group(1) < MIN_VERIFIED` -> `<=` (line 131) | killed |
| M19 | recheck line | check dropped -> `if False:` (line 133) | killed |
| M20 | used-by membership | `if path in rows[c]['used']` -> `not in` (line 135) | killed |
| M21 | quote token bounds 6..25 | lower bound `6` -> `1` (line 142) | **survived** |
| M22 | quote token bounds 6..25 | upper bound `25` -> `40` (line 142) | **survived** |
| M23 | quote located in a cited snapshot | location search `for c in cited` -> `for c in rows` (line 142) | **survived** |
| M24 | fresh-quote-vs-package | freshness requirement dropped: `if not fresh:` -> `if False:` (line 148) | killed |
| M25 | fresh-quote-vs-package (missing package copy) | dropped `package_text is None or` (line 144) | killed (crash: `fold(None)` TypeError) |
| M26 | README index | short form `` `knowledge/x.md` `` disjunct dropped (line 169) | killed |
| M27 | README index | full form `` `corpus/knowledge/x.md` `` disjunct dropped (line 169) | killed |
| M28 | rows>=3 | MIN_ROWS `3` -> `2` (line 54) | **survived** |
| M29 | rows>=3 | `>= MIN_ROWS` -> `> MIN_ROWS` (line 175) | killed |
| M30 | entries>=3 | MIN_ENTRIES `3` -> `2` (line 55) | **survived** |
| M31 | indexed==entries | `==` -> `<=` (line 176) | killed |
| M32 | covered==rows | `==` -> `<=` (line 176) | killed |
| M33 | self_pin | digest comparison `==` -> `!=` (line 157) | killed |

## Survivors (coverage findings about the selftest, not contract changes)

Every survivor ran `C3_R47_SELFTEST: cases=24 failed=0` / `VERDICT: PASS` / exit 0 under the mutated bytes (logs `logs/M<NN>.log`, mutated bytes `logs/M<NN>.mutated.py` in the scratch dir).

1. **M01/M35 doc_key case folding (line 67).** All fixtures derive from the lowercase `DOCS` tuple and the one hand-written URL (T09's `2504.16778`) is lowercase too, and `doc_key` normalizes both sides of the comparison — so any consistent case-handling mutation is invisible. The contract's "compared without … case" is unpinned. Killing shape: one fixture row whose source cell writes `https://ARXIV.org/abs/2302.09330` (accepted only if folding happens) next to the lowercase rows.
2. **M03 doc_key `www.` stripping (line 67).** Same structure: no `www.` fixture anywhere, and normalization applies to both sides. Killing shape: a row written as `https://www.arxiv.org/abs/2302.09330` that must still be admitted. (Scheme and trailing-slash halves of the same normalization ARE pinned — M02/M04 killed via `urls[1]`'s trailing slash and the scheme-bearing row URLs.)
3. **M05 three frozen documents (line 43).** The selftest builds `urls` from `DOCS` itself, so drifting a frozen id is self-consistently admitted; nothing pins the literal `arxiv.org/abs/2302.09330` / `2607.09345` / the `%2c`-encoded Semantic Scholar record. The only accidental catch is drifting an id INTO T09's hardcoded `2504.16778` (which is exactly how the round-46 copy killed its M02 — coincidence, not coverage). Killing shape: write one row's source cell with the hand-literal frozen id (not derived from `DOCS`) and require its admission, or pin `hashlib.sha256('\n'.join(DOCS))` in a case.
4. **M34 snapshot prefix `sources/` -> `source/` (line 40) — routed from round-46 M06.** T12 only proves a `round-45`-token prefix is wrong (and M10 shows the `round-47` token is pinned only because T12 mutates that token textually); any other wrong path component survives, since `row()`/`SNAP_RE`/`build()` all share the constant. Killing shape: a fixture row with the hand-literal `.ufo/evidence/round-47/coverage/sources/` anchor that must be admitted, beside a `coverage/source/` row that must not.
5. **M11 snapshot present (lines 113–114) — routed from round-46 M07.** `build()` never deletes snapshot files (T13 passes `snapshots={}`, which writes nothing; files persist from earlier cases), so `tree.read` never returns None and the `data is None` guard is dead code under the selftest; T13's `rows=0` comes from the `e3b0c442` digest mismatch. Killing shape: have `build()` actually remove the snapshot files for T13 (then the guard, not the digest, decides).
6. **M21/M22 quote token bounds 6..25 (line 142).** Every fixture quote sits comfortably inside the window (6–25 tokens), so widening it admits nothing new. Killing shape: an entry whose only located quote is 3 tokens (and a twin with 30 tokens), each refused — pinning both edges.
7. **M23 quote located in a *cited* snapshot (line 142).** Searching the quote over all row snapshots instead of the cited rows passes all 24 cases: no entry ever carries a quote that is located only in a non-cited row's snapshot. Killing shape: an entry citing S258 whose quotes are located only in S259's snapshot — must be refused (`no located quote`), with a twin citing S258 and quoting S258's text admitted.
8. **M28 rows>=3 (line 54) — routed from round-46 M18.** Lower side of the threshold unpinned: T18's two-row case still fails via `entries=2 < MIN_ENTRIES`, so `MIN_ROWS=2` is invisible. Killing shape: rows=2 + entries=3 + indexed=3 + covered=2 case that must print `C3_R47_PASS=false`.
9. **M30 entries>=3 (line 55) — routed from round-46 M19.** Same shape: every entries=2 case (T17) simultaneously fails via `covered != rows`. Killing shape: rows=3 + entries=2 + indexed=2 + covered=3 case that must print `C3_R47_PASS=false`.

## Killing cases (first decisive selftest line per killed mutant)

```
M02 FAIL T01_three_pass want='C3_R47_PASS=true' got=C3_R47: self_pin=1 rows=2 entries=2 indexed=2 covered=2 row_ids=S258,S260 …  (S259 dropped: urls[1] keeps its trailing slash)
M04 FAIL T01_three_pass want='C3_R47_PASS=true' got=C3_R47: self_pin=1 rows=0 entries=0 indexed=0 covered=0 row_ids=- …           (https:// no longer stripped from row URLs)
M06 FAIL T01_three_pass want='C3_R47_PASS=true' got=C3_R47: self_pin=1 rows=0 entries=0 indexed=0 covered=0 row_ids=- …           (T08 also flips: queued rows=3)
M07 FAIL T11_four_space_row_ignored want='rows=2' got=C3_R47: self_pin=1 rows=3 entries=3 indexed=3 covered=3 …
M08 FAIL T01_three_pass want='C3_R47_PASS=true' got=C3_R47: self_pin=1 rows=0 … row_ids=- …                                      (0-space row c no longer matches)
M09 FAIL T01_three_pass want='C3_R47_PASS=true' got=C3_R47: self_pin=1 rows=0 … row_ids=- …                                      (15 case failures)
M10 FAIL T12_wrong_round_prefix want='rows=0' got=C3_R47: self_pin=1 rows=3 entries=3 indexed=3 covered=3 …                      (T12's .replace('round-47','round-45') becomes a no-op, rows match the drifted constant)
M12 FAIL T01_three_pass want='C3_R47_PASS=true' got=C3_R47: self_pin=1 rows=0 … row_ids=- …
M13 FAIL T01_three_pass want='C3_R47_PASS=true' got=C3_R47: self_pin=1 rows=0 … row_ids=- …                                      (T13 also flips: rows=3 kept despite dead-beef/e3b0c442 prefixes)
M14 FAIL T14_no_source_prefix want='entries=2' got=C3_R47: self_pin=1 rows=3 entries=3 indexed=3 covered=3 …
M15 FAIL T06_bad_sha_prefix want='rows=2' got=NO-OUTPUT   File "…/measure.py", line 135, in entry_ok / KeyError                     (crash-kill: entries citing ids excluded from rows hit rows[c]['used']; 7 NO-OUTPUT cases: T06,T08,T09,T11,T12,T13,T18)
M16 FAIL T01_three_pass want='C3_R47_PASS=true' got=C3_R47: self_pin=1 rows=3 entries=0 indexed=0 covered=0 …
M17 FAIL T03_old_verified_at want='entries=2' got=C3_R47: self_pin=1 rows=3 entries=3 indexed=3 covered=3 …
M18 FAIL T01_three_pass want='C3_R47_PASS=true' got=C3_R47: self_pin=1 rows=3 entries=0 …                                        (good fixtures sit exactly on the floor 2026-10-25, so <= rejects them; T03 pins the rejecting side)
M19 FAIL T15_no_recheck want='entries=2' got=C3_R47: self_pin=1 rows=3 entries=3 indexed=3 covered=3 …
M20 FAIL T01_three_pass want='C3_R47_PASS=true' got=C3_R47: self_pin=1 rows=3 entries=0 …
M24 FAIL T21_relabelled_package_entry want='entries=2' got=C3_R47: self_pin=1 rows=3 entries=3 indexed=3 covered=3 …             (relabelled package copy re-admitted)
M25 FAIL T01_three_pass want='C3_R47_PASS=true' got=NO-OUTPUT  TypeError at fold(package_text) with package_text=None              (crash-kill: missing package copy must count as fresh; 18 case failures)
M26 FAIL T16_fullpath_index_form want='indexed=3' got=C3_R47: self_pin=1 rows=3 entries=3 indexed=0 covered=3 …
M27 FAIL T01_three_pass want='C3_R47_PASS=true' got=C3_R47: self_pin=1 rows=3 entries=3 indexed=0 covered=3 …                     (T07/T22 also flip)
M29 FAIL T01_three_pass want='C3_R47_PASS=true' got=C3_R47: self_pin=1 rows=3 entries=3 indexed=3 covered=3 … C3_R47_PASS=false   (T22 also flips: rows=3 must achieve the threshold)
M31 FAIL T19_unindexed_is_false want='C3_R47_PASS=false' got=C3_R47: self_pin=1 rows=3 entries=3 indexed=2 covered=3 … C3_R47_PASS=true
M32 FAIL T24_two_entries_one_row_is_false want='C3_R47_PASS=false' got=C3_R47: self_pin=1 rows=3 entries=3 indexed=3 covered=1 … C3_R47_PASS=true
M33 FAIL T01_three_pass want='C3_R47_PASS=true' got=C3_R47: self_pin=0 rows=3 entries=3 indexed=3 covered=3 … C3_R47_PASS=false   (T20 independently pins the positive detection)
```

## Restoration evidence

- `restore()` re-copies `pristine.py` over `measure.py` and asserts sha256 == `c8fb89e69196fc2401e2364142b848bd8d53e5c6e3d97f17c528951c9f894260` after every one of the 35 cycles (35/35 asserts passed; mutated-bytes digests per probe in the shell transcript and `logs/M<NN>.mutated.py`).
- Final restored run: `python3 measure.py --selftest` -> rc=0, `VERDICT: PASS`.
- Lane integrity: `cmp` of `.ufo/evidence/round-47/coverage/measure.py` vs `pristine.py` -> identical; lane sha256 `c8fb89e6…` before and after the audit. Only file written in the lane: this report.

## Bounds / unrun checks

- Counter run only as `--selftest`, inside `/tmp/tameshi-r47-T47MutC3Counter/`. No `--lane/--rev` run, no deciding run (the L1's), no verdict.
- Round-46-routed survivors (M11, M28, M30, M34-shape) were re-probed here against the round-47 bytes and confirmed still present; per the routing note they remain recorded in `.ufo/waves/round-46/w1/MutC3Counter.md` and are not contract changes.
- No tool installs or upgrades (nothing added to the tooling ledger).
