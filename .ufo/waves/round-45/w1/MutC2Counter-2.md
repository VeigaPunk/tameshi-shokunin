seat: MutC2Counter

# C2 counter mutation audit — coverage milestone (instance MutC2Counter-2)

Instance note: agent id is `MutC2Counter-2`; the assigned report path
`.ufo/waves/round-45/w1/MutC2Counter.md` was already written at 16:54 by the concurrent
instance `MutC2Counter` (verified: first line `seat: MutC2Counter`). Per the
never-clobber-a-sibling rule this report lands beside it as `MutC2Counter-2.md`.
Scratch likewise isolated: `/tmp/tameshi-r45-MutC2Counter-2/` (sibling occupies
`/tmp/tameshi-r45-MutC2Counter/`; its `measure.py` was byte-identical pristine when checked).

## Object under test
`/.ufo/evidence/round-45/coverage/measure.py` at freeze `3310e7be803516ca5934b4e949d91bcec824b179`,
224 lines, sha256 `2f321b2c499ff4329483ef640ac96e629ad67a8e0e16f8e0a6920d7031fbf894`
(byte-identical to the lane file before, during and after the sweep).

## Method
- Detector: `python3 /tmp/tameshi-r45-MutC2Counter-2/measure.py --selftest` ONLY. The selftest
  builds its own scratch repos in a `TemporaryDirectory` (`git init -q -b m` + assert on
  `rev-parse --show-toplevel`); the counter was never run with `--lane/--rev` against anything,
  and the lane checkout was never written.
- Per enumerated rule: ONE minimal exact-string mutation on the isolated copy, one selftest run,
  then restore pristine bytes (sha-verified after every mutant). Two rules whose behavior spans
  two independent code points (README-index forms at line 129, self_pin at lines 119/135) got
  one probe per point, marked a/b.
- Baseline (pristine): `PASS` on all 10 cases, `C2_R45_SELFTEST: cases=10 failed=0`,
  `VERDICT: PASS`, rc=0 → detector conclusive, so every mutant verdict below is judgeable.

## Results — rule → mutation → verdict

| rule (measure.py:line) | mutation (old → new) | verdict | killed by |
|---|---|---|---|
| googletest URL filter (:35) | `GT_RE` host alternation → `r'^https?://'` | KILLED | T9_non_googletest_url |
| status mined (:74) | drop `or cells[8] != 'mined'` | KILLED | T8_queued_rows |
| snapshot path prefix (:36) | `SNAP_RE` prefix-anchored → bare `[A-Za-z0-9._/-]+` | SURVIVED | — |
| snapshot present (:83) | delete `if data is None: continue` | SURVIVED | — |
| sha prefix match (:86) | digest comparison → mere `HEX_RE.findall` presence | KILLED | T6_bad_sha_prefix |
| provenance trio order (:100) | `re.match(..., lines[1])` → `re.search(..., text)` | SURVIVED | — |
| verified-at >= 2026-10-25 (:40) | `MIN_VERIFIED` 2026-10-25 → 2026-10-24 | KILLED | T3_old_verified_at |
| recheck line (:103) | `if not lines[2].startswith('recheck:')` → `if False:` | SURVIVED | — |
| citation of qualifying row (:95) | drop `if c in rows` filter | KILLED (crash) | T6_bad_sha_prefix |
| used-by membership (:105) | drop the membership filter line | KILLED | T5_not_used_by |
| quote 6..25 tokens located (:110) | drop `6 <= len(quote.split()) <= 25` (location kept) | SURVIVED | — |
| README index, full `corpus/knowledge/…` form (:129) | drop first disjunct (short form kept) | SURVIVED | — |
| README index, short `knowledge/…` form (:129) | drop second disjunct (full form kept) | KILLED | T1, T7 |
| rows/entries>=2, indexed==entries (:135) | `len(entries) >= 2` → `>= 1` | SURVIVED | — |
| self_pin comparison (:119) | digest `==` → `!=` | KILLED | T1 |
| self_pin conjunct (:135) | drop `self_pin == 1 and` | SURVIVED | — |

Score: 16 probes → 8 killed, 8 survived, 0 inconclusive. (Corrected: the citation-filter
mutant was first mis-scored SURVIVED by a driver flaw — see "Driver flaw correction".)

## Survivors — each with the case that would kill it

1. **Snapshot path prefix (:36).** No fixture anchors a snapshot outside
   `…/coverage/sources/`. Kill case: valid row (mined, googletest URL, sha-valid) anchored at
   `.ufo/evidence/round-44/calibration/other.md` with that file committed in the scratch tree,
   expecting `rows=0`; the mutant counts it (`rows=1`).
2. **Snapshot present (:83).** Every fixture row's snapshot exists. Kill case: mined row
   anchored at `sources/absent.md` with a plausible sha, expecting `rows=0`; the mutant raises
   `TypeError` in `hashlib.sha256(None)` on the next line instead of excluding the row.
3. **Provenance trio order (:100).** All fixture trios are well-ordered. Kill case: entry with
   line 1 `source: S256 S257`, line 2 `see verified-at: 2026-10-25 note`, line 3
   `recheck: 365d` — pristine refuses (line 2 must start `verified-at:`), the mutant accepts.
4. **Recheck line (:103).** No case varies line 3. Kill case: entry line 3 `checked: 365d`,
   everything else valid, expecting refusal.
5. **Quote 6..25 token bound (:110).** The fixture quote is 11 tokens. Kill case: entry quoting
   a verbatim 30-token span of the snapshot (still located) expecting refusal.
6. **README full-path index form (:129).** The fixture README only ever uses short
   `` `knowledge/a.md` `` forms, so the `` `corpus/knowledge/a.md` `` disjunct is untested.
   Kill case: README indexing entries solely via backticked full paths, expecting
   `indexed=2 … C2_R45_PASS=true`; the mutant yields `indexed=0`, PASS=false.
7. **Count thresholds (:135).** T3 already produces exactly `entries=1` but its assertion is
   the substring `'entries=1'`, which the summary line prints regardless of the verdict — so
   `>= 2 → >= 1` flips `C2_R45_PASS` true and nothing notices. Kill case: same single-entry
   fixture with `want='C2_R45_PASS=false'` (verdict assertion, not count substring).
8. **self_pin conjunct (:135).** Structurally unkillable by the current selftest: `build()`
   always writes the running file's own bytes to `SELF_PATH` in the scratch tree, so
   `self_pin` is 1 in every case that can ever run. Kill case: a `build()` variant committing
   stale/different bytes at `SELF_PATH` while the live copy runs, expecting
   `self_pin=0 … C2_R45_PASS=false`.

## Killed mutants (for the record)
- `GT_RE` relaxation → T9 (`rows=0` expected, got `rows=2`).
- status-mined drop → T8 (queued rows counted).
- sha-prefix comparison drop → T6 (`deadbeef` anchor accepted, `rows=1` expected).
- `MIN_VERIFIED` lowered → T3 (2026-10-24 entry accepted).
- used-by drop → T5 (entry not listed in the row's used-by accepted).
- citation-filter drop (`if c in rows` removed, :95) → T6 (crash): T6's entries cite
  `S256 S257` while S256 is excluded from qualifying rows by its `deadbeef` sha, so the
  unfiltered id reaches the used-by lookup `rows['S256']` → `KeyError`; the selftest then
  aborts in `build()` with `IndexError: list index out of range` after T5, rc=1. Verified raw
  (re-applied mutant, separate run): rc=1, cases T1–T5 PASS, no VERDICT line, stderr
  `IndexError: list index out of range`. Mutant bytes sha256
  `4fc68cb9437110607c53ce80da65a99f70342101adcab53a211222bc9cd1f8cc`, deleted after the check.
- README short-form drop → T1 and T7 (fixture only uses short forms).
- self_pin `==` flip → T1 (`self_pin=0`, PASS=false).

## Driver flaw correction (affects the initially reported score)
- The first sweep scored the citation-filter mutant SURVIVED because `run_mutants.py`
  classified any selftest run lacking a `VERDICT:` line as SURVIVED — a selftest that dies
  mid-case (mutant crashes the counter, selftest aborts) is a KILL, not an escape. Raw
  re-verification (above) establishes T6 kills it. Corrected score: **8 killed / 8 survived**.
- No other survivor is affected: each of the 8 printed a genuine `VERDICT: PASS` with all 10
  cases run (crash-class survivors would have been M4-shaped, but every fixture snapshot
  exists, so the None guard is never exercised — survivor 2 stands).

## Cross-check with instance `MutC2Counter` (their report: MutC2Counter.md)
- Convergent survivors, same sites: snap-path-prefix :36, snap-present :83, provenance-trio
  order :100, recheck :103, README full-path form :129, thresholds and self_pin conjunct :135.
- Convergent split at :110 — location half pinned (their `and`→`or` killed by T4), token-bound
  half unpinned (my bound-drop survivor) — matches their named residual slack.
- Divergence at :95 resolved: same mutation direction (filter drop), their run saw the T6
  crash-kill; mine initially mis-scored it SURVIVED via the driver flaw corrected above. Both
  now agree: KILLED by T6.
- Additional unpinned aspect from their sweep, adopted here: `GT_RE` weakened to accept any
  github.com/raw.githubusercontent repo (not just `google/googletest`) SURVIVES — T9's
  example.org URL cannot catch repo-scoped slack. The URL-filter rule is only pinned against
  fully off-platform hosts.
- No contract changes implied; all survivors are selftest negative-space.

## Detector observations (no code changed; findings only)
- T2–T7 assert count substrings (`entries=0/1`, `indexed=1`, `rows=0/1`) that appear in the
  `C2_R45:` summary line whether or not the PASS verdict flipped. Any mutant whose only effect
  is behind such a count survives — the root cause of survivors 3, 4, 5, 7. Adding
  `C2_R45_PASS=false` expectations to the negative cases would raise the kill rate materially.
- Selftest line numbers referenced: cases list at measure.py:170-182, driver assertions
  `ok = want in line` at :186.

## Restoration evidence
- before (pristine): `2f321b2c499ff4329483ef640ac96e629ad67a8e0e16f8e0a6920d7031fbf894`
- after every mutant and final restore: driver assert `restore() → True`;
  `sha256sum measure.py` → `2f321b2c499ff4329483ef640ac96e629ad67a8e0e16f8e0a6920d7031fbf894`
- lane file re-hashed after the sweep: unchanged,
  `2f321b2c499ff4329483ef640ac96e629ad67a8e0e16f8e0a6920d7031fbf894`
- scratch retained for inspection: `/tmp/tameshi-r45-MutC2Counter-2/` (pristine `measure.py`,
  `run_mutants.py` driver). Driver cosmetic note: its baseline summary line prints the
  case/failed counters swapped (`cases=0 failed=10`); the authoritative baseline is the direct
  selftest output quoted above (10/10 PASS). Per-mutant parsing is unaffected.
- after the correction re-check: `mut9.py` (mutant,
  `4fc68cb9437110607c53ce80da65a99f70342101adcab53a211222bc9cd1f8cc`) created, run once
  (`--selftest`), deleted; `measure.py` re-hashed pristine
  `2f321b2c499ff4329483ef640ac96e629ad67a8e0e16f8e0a6920d7031fbf894` before and after.

## Bounds & tooling
- Counter invoked only as `--selftest`, always on the /tmp copy; no `--lane/--rev` invocation,
  no deciding run performed or approached; contract.json read, never edited; no git/jj command
  run in the lane; the only lane write is this report file.
- No tools installed or upgraded (none needed); pacman untouched.
