seat: MutC2Counter

# C2 counter mutation audit — coverage milestone

Target: `.ufo/evidence/round-45/coverage/measure.py` (frozen, sha256 `2f321b2c499ff4329483ef640ac96e629ad67a8e0e16f8e0a6920d7031fbf894`; byte-identical to the scratch copy). Lane checkout untouched except this report; all work under `/tmp/tameshi-r45-MutC2Counter/`.

Method: one minimal behavior-bearing mutation per rule, each in its own copy (`mutants/M*.py`, never the lane file). Detector = the counter's own `--selftest` (builds its own scratch fixture repos; runs `git init -q -b m` in a tempfile dir and asserts `rev-parse --show-toplevel` equals it before committing). Killed = any case FAIL / crash / nonzero exit; survived = `VERDICT: PASS`, exit 0.

Baseline: `python3 /tmp/tameshi-r45-MutC2Counter/measure.py --selftest` → `C2_R45_SELFTEST: cases=10 failed=0`, `VERDICT: PASS`, exit 0. Detector usable.

Command: `python3 /tmp/tameshi-r45-MutC2Counter/mutate.py` (driver applies each old→new, asserts the old string is unique, runs `--selftest` per mutant).

## Rule → mutation → result

| rule | site (counter line) | mutation (old → new) | verdict | evidence |
|---|---|---|---|---|
| googletest URL filter | L35 | GT_RE drops `/google/googletest/` host-path pin (any github.com/raw URL passes) | **SURVIVED** | cases=10 failed=0 |
| status mined | L74 | `cells[8] != 'mined'` → `!= 'queued'` | killed | T8 fails: `want='rows=0' got=... rows=2 entries=1 indexed=1 ... C2_R45_PASS=false` (8 cases fail) |
| snapshot path prefix | L36 | compiled prefix `re.escape(SNAP_PREFIX)` → `\.ufo/evidence/round-4[45]/coverage/sources/` (admits round-44 snapshots) | **SURVIVED** | cases=10 failed=0 |
| snapshot present | L83 | `if data is None: continue` → `data = b''` | **SURVIVED** | cases=10 failed=0 |
| sha prefix match | L86 | `if not any(digest.startswith(h) ...)` → `if False:` | killed | T6 fails: `want='rows=1' got=... rows=2 entries=2 indexed=2 ... C2_R45_PASS=true` |
| provenance trio order | L98 | drop `not lines[0].startswith('source:')` | **SURVIVED** | cases=10 failed=0 |
| verified-at >= 2026-10-25 | L40 | `MIN_VERIFIED = '2026-10-25'` → `'2026-10-24'` | killed | T3 fails: `want='entries=1' got=... entries=2 ... C2_R45_PASS=true` |
| recheck line | L103 | `if not lines[2].startswith('recheck:')` → `if False:` | **SURVIVED** | cases=10 failed=0 |
| citation of a qualifying row | L95 | drop `if c in rows` from the cited-ids filter | killed | mutant counter raises `KeyError 'S256'` when an entry cites a non-qualifying id; selftest exits 1 with IndexError/traceback, no VERDICT. Inner defect demonstrated: `entry_ok('corpus/knowledge/a.md', entry, {})` → `KeyError 'S256'` (pristine returns `(False, 'cites no googletest row')`) |
| used-by membership | L105 | `if path in rows[c]['used']` → `if True` | killed | T5 fails: `want='entries=1' got=... entries=2 ... C2_R45_PASS=true` |
| quote 6..25 tokens located in a cited snapshot | L110 | `and any(quote in rows[c]['text'] for c in cited)` → `or ...` (location no longer required) | killed | T4 fails: `want='entries=1' got=... entries=2 ... C2_R45_PASS=true` |
| README index (both forms) | L129 | drop the full-path disjunct (keep only `` `knowledge/…` `` short form) | **SURVIVED** | cases=10 failed=0 |
| rows>=2/entries>=2/indexed==entries | L135 | `len(rows) >= 2` → `>= 1` | **SURVIVED** | cases=10 failed=0 |
| self_pin | L135 | `self_pin == 1` → `self_pin >= 0` (pin ignored) | **SURVIVED** | cases=10 failed=0 |

6 killed / 8 survived. Line numbers verified against the frozen counter via `grep -n`.

## Survivors — coverage gaps and the case that would kill each

All kill cases are additions to the selftest `cases` list (same `build()` harness); each kills only the named mutant and passes on pristine.

- **M01 googletest URL filter (L35).** The only negative-URL case is `T9_non_googletest_url` with `https://example.org/…`, which even the loosened `^https?://(github\.com|raw\.githubusercontent\.com)/` regex rejects. A github-but-not-googletest URL is unpinned. Kill case: `('T11_github_non_googletest', row('S256','advanced', ea+', '+eb, url='https://github.com/google/flatbuffers/%s.md') + row('S257','primer', ea+', '+eb, url='https://github.com/google/flatbuffers/%s.md'), {ea: entry, eb: entry}, idx, 'rows=0')` — pristine rows=0, mutant rows=2.
- **M03 snapshot path prefix (L36).** Fixtures only use round-45 paths; the loosened regex still matches them. Related structural gap: `row()` and `put()` build fixtures from `SNAP_PREFIX` itself, so any drift of that constant is self-consistent and invisible. Kill case: commit snap bytes at `.ufo/evidence/round-44/coverage/sources/{advanced,primer}.md`, anchor both rows there (hardcoded literal path + sha of those bytes), expect `'rows=0'` — pristine rejects (prefix is round-45), mutant accepts `round-4[45]`.
- **M04 snapshot present (L83).** Missing snapshot → `data = b''` → digest = sha256(b"") = `e3b0c442…`; the row still dies at the sha check unless the anchor carries that hex, and empty text can never host a located quote — doubly masked, so no current fixture can see it. Kill case: two rows anchored to nonexistent snapshot paths with anchor hex `e3b0c442`, expect `'rows=0'` — pristine rows=0 (missing), mutant rows=2 (sha256(b"") matches). (Only the rows count exposes it; entries cannot, since empty text rejects every quote either way.)
- **M06 provenance trio order (L98).** No fixture entry lacks the `source:` prefix; T2's `'x\n'` dies earlier at "cites no googletest row". Kill case: `('T13_no_source_prefix', good_reg, {ea: 'S256 S257 — upstream\nverified-at: 2026-10-25\nrecheck: 365d\n\nUpstream says "the test order is undefined, so your code cannot depend on it".\n', eb: entry}, idx, 'entries=1')` — pristine REFUSES ea (`no provenance trio`), entries=1; mutant accepts (ids found on line 1 regardless of prefix), entries=2.
- **M08 recheck line (L103).** No fixture entry omits `recheck:` on line 3. Kill case: `('T14_no_recheck', good_reg, {ea: entry with line 3 'checked: 365d', eb: entry}, idx, 'entries=1')` — pristine REFUSES ea (`recheck`), entries=1; mutant entries=2.
- **M12 README index forms (L129).** Every fixture README indexes only the short `` `knowledge/…` `` form; the full `` `corpus/knowledge/…` `` disjunct is unpinned. Kill case: `('T15_fullpath_index', good_reg, {ea: entry, eb: entry}, '`corpus/knowledge/a.md` `corpus/knowledge/b.md`', 'indexed=2')` — pristine indexed=2 via the first disjunct; mutant indexed=0.
- **M13 pass thresholds (L135).** T6 (rows=1) pins the printed count, not the threshold's effect on the PASS flag — its `want='rows=1'` is satisfied either way. Sibling slack at the same site: `len(entries) >= 2 → >= 1` survives via T3, `len(indexed) == len(entries) → >= 1` survives via T7, for the same reason (wants assert counts, not PASS=false at boundary values). Kill case: T6's exact fixture with `want='C2_R45_PASS=false'` — pristine rows=1 → false; mutant rows=1, entries=2, indexed=2 → true. (Residual quote-rule slack, noted not probed: the 6 and 25 token bounds and "located in a *cited* row's snapshot" vs "any qualifying row" are also unpinned — all fixture quotes are 12 tokens inside both cited rows' identical snapshot text.)
- **M14 self_pin (L135).** Structural survivor: `build()` always writes the running script's own bytes to SELF_PATH, so `self_pin=1` in every selftest case by construction; `--selftest` cannot detect pin-logic tampering. Kill case: a build variant that after the script copy does `put(SELF_PATH, b'#!/usr/bin/env python3\n# not the counter\n')` and expects `'C2_R45_PASS=false'` — pristine self_pin=0 → false; mutant `self_pin >= 0` → true. The pin's real protection remains the deciding run comparing the lane blob at REV against the frozen counter bytes.

## Hashes and restoration

- Pristine scratch copy `/tmp/tameshi-r45-MutC2Counter/measure.py`: `2f321b2c499ff4329483ef640ac96e629ad67a8e0e16f8e0a6920d7031fbf894` before and after all runs (`RESTORE scratch copy after=2f321b2c… match=True`).
- Lane counter `.ufo/evidence/round-45/coverage/measure.py`: `2f321b2c499ff4329483ef640ac96e629ad67a8e0e16f8e0a6920d7031fbf894` (read-only, never written; identical to scratch).
- Mutants (mutants/ dir, each a separate copy): M01 `10c1478292c67db1…4270ad8`, M02 `b5c3a15032d3ec4c…a8bb9fa3`, M03 `b992bca99fbfe892…a787029`, M04 `91f047b4668ce45b…b9194` (full: `91f047b4668ce45b9022f4a98d448ccd1600bc07d9ad681c495edd908a6b9194`), M05 `d96cc8bafed9fbed…b885c`, M06 `6b4e91753b568908…bf26d`, M07 `82c475032c3446b7…59ea9`, M08 `d1a34f3d3a457e3b…30639`, M09 `d796df829c181d8d…cc50b`, M10 `5a1f48d44871f08b…8557`, M11 `c2d2c846c2f9118b…b3b90`, M12 `279134777ba53c3a…7807e`, M13 `2e1d141ec6ef93f5…b95c`, M14 `78cd65bb4f496431…9637f`.

## Tooling

No installs or upgrades (pacman guard respected): python 3.14.8 and git 2.56.0 already present; driver + mutants are scratch files under `/tmp/tameshi-r45-MutC2Counter/`.

## Verdict

The selftest pins 6 of 14 rule families (status mined, sha prefix match, verified-at floor, citation qualifying, used-by membership, quote location). 8 survived — negative-space coverage gaps, not counter defects: the frozen counter itself shows no defect under these probes. The highest-value selftest hardening, in order: boundary `want='C2_R45_PASS=false'` cases for rows=1/entries=1/indexed<entries (M13), a non-`source:` and a non-`recheck:` entry (M06/M08), a github-non-googletest URL (M01), a foreign SELF_PATH blob (M14), a full-path README index (M12), a snapshot outside the prefix (M03), and a missing-snapshot row with `e3b0c442` anchor hex (M04).
