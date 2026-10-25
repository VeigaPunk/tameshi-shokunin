# RevC2Classes — C2 class-to-code agreement (round 43)

Seat: reviewer, calibration axis. Scope: `.ufo/evidence/round-43/calibration/measure.py`
(sha256 `092c76cd6e10f9280af21237ec90dc14e63f0bdb9ae74fffb9da841730a8f286`, matches
`claims.C2.counter_sha256`) against the seven class sentences in
`.ufo/evidence/round-43/contract.json` (`claims.C2.classes`). Read-only on the lane; all
probes under `/tmp/tameshi-r43-RevC2Classes` (deleted).

## Measured state (commands run)

| command | result |
|---|---|
| `measure.py --selftest` | `C2_R43_SELFTEST: cases=10 failed=0`, `VERDICT: PASS`, exit 0 |
| `--rev 487b8f0… --freeze 17f6ef0…` (base) | `self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=1 m13=1 total=2 records=3 sources_rows=113 standing=113 receipts=17 revisions=3 m13_probe=standing=6_column0=112_valid=113` → `C2_R43_PASS=false`, exit 1 |
| `--rev 17f6ef0… --freeze 17f6ef0…` (freeze) | identical line; `C2_R43_PASS=false`, exit 1 |

`before_state` is accurate at both permitted revs: `m12=1` (last `**Planned (…)**` line is
`SCORECARD.md:1893` = round 41; the newest block is `## Round 42` at `SCORECARD.md:1995`)
and `m13=1` (newest standing row `SCORECARD.md:2020` cites the column-zero
`grep -cE '^\| S[0-9]{3} \|'`). Neither permitted rev reaches `total=0`; that is the
pre-repair state, not a code/claim contradiction in itself.

## Class-by-class verdict

### m6 — SAME STATEMENT (one strictness edge, no vacuity)

Contract: "*the newest standing sources-registry row's stated row count equals the
census-valid registry row count*".

Code: `standing_registry_rows` `measure.py:125-131` takes the last `| sources-registry |`
line (newest by position); `row_count_claim` `measure.py:133-138` parses `N rows at round M`;
`measure.py:371-378` compares `stated == valid_count`, where `valid_count` is the census-valid
line count `^ {0,3}\|\s*S\d{3,}\s*\|` (`measure.py:372-373`).

Same statement. Evidence: freeze run `standing=113 sources_rows=113 → m6=0`.
Edge: a standing row that states the count in any other phrasing yields `(None, None)`
(`probe5` case 6) and becomes an m6 hit although the count is right — false-positive
direction only, never a false clean. Not vacuous: with no standing row `stated=None` and
`None == int` is False, so m6 always hits.

### m7 — SAME QUANTIFIER + MASKING; BROADER RECORD SET; VACUOUS ON MISSING RECORDS

Contract: "*every S-id cited by the round-42/43 records as a source is a mined row:
staged:S### package tokens and 'Next unused id: S###' declarations are masked first*".

Code: `ID_RE` `measure.py:64` (negative lookbehind `(?<!staged:)`), `MASK_IDS`
`measure.py:65-67`, masking and the mined test `measure.py:380-391`, `mined_ids`
`measure.py:100-107`. Masking and the "is a mined row" predicate match the sentence exactly
(at freeze the only S-ids are mined, `m7=0`).

Broader: the scanned set is `record_texts`, which is the two lesson files **plus** the
newest SCORECARD block and a `LOG.md` slice (`measure.py:357-369`), not just "the round-42/43
records". Over-inclusion only.

Narrower/vacuity: headerless record files are skipped silently (`measure.py:358-361`), so a
missing record contributes no citations instead of a hit. At the freeze rev
`corpus/lessons/round-43.md` does not exist (`git ls-tree` shows only `round-42.md`) yet the
run reports `records=3` with no signal; m7 is clean over a record set that omits one of the
two records the sentence names.

### m8 — NARROWER (drops declared cites); brace "normalization" is deletion

Contract: "*every backtick cite under corpus/, tools/, .ufo/, plans/, reports/ or the
declared root files resolves at REV (after :NN and brace normalization); a bare seat-report
filename is not a repo path*".

Code: `path_cites` `measure.py:174-193`, `m8_paths` `measure.py:196-206`.

Narrower in two ways:

1. `measure.py:183-186` gates every cite on `token.endswith(SKIP_SUFFIXES)`
   (`measure.py:63-65`). Directory cites and suffix-less cites are dropped, not resolved.
   At freeze, 8 declared-prefix cites are silently dropped, including
   `.ufo/waves/`, `.ufo/evidence/round-42/sources/`, `corpus/knowledge/`,
   `.ufo/waves/round-42/assimilation/guard/`.
2. `measure.py:182` "brace normalization" deletes the brace group instead of expanding it:
   `LOG.md` cites `` `.ufo/evidence/round-42/after/c1-at-242c1b4a.{stdout,exit}` `` and
   `c2-at-…`; after deletion the token is `.ufo/…/c1-at-242c1b4a.` (trailing dot), which does
   not resolve at REV (`exact=False prefix=False`), and is then dropped by the suffix gate.
   The two real files exist as `.stdout`/`.exit`. A dangling brace cite and a valid one are
   indistinguishable to this code, and neither is checked.

`measure.py:191-192` (`elif token.startswith('.ufo/')`) is unreachable — `.ufo/` is already in
`CITE_PREFIXES` (`measure.py:60`) and caught at `:189`; `measure.py:183` is subsumed by
`:185`.

### m10 — BROADER SCOPE + OVER-BROAD EXCLUSION (false-negative, demonstrated)

Contract: "*no presence receipt under .ufo/waves asserts present/absent contrary to the tree;
a receipt named in another receipt's supersedes is history and its claims are not counted*".

Code: `m10_receipts` `measure.py:209-257`; superse­des collection `:211-228`; exclusion set
`:241-244`; per-claim test `:246-256`.

Finding 1 (LATENT FALSE NEGATIVE, high): `measure.py:242-244` adds **both** the superseded
targets (`key`) **and the superseding receipts** (`value`) to `superseded`, and
`measure.py:252` then skips every failing claim whose file is in that set. The sentence (and
the counter's own docstring at `measure.py:16-17`, "the superseding receipt carries the
claims") excludes only the *named* receipt. A live superseding receipt's own false
`present` claim is therefore never counted. Proof (`/tmp/…/synth/repo2`, `probe3b.py`):

```
A: superseder silent, old receipt lies:            ([], 1)
B: the ACTIVE superseding receipt itself lies:     ([], 2)   # claim present=true, path absent
C: same lie with no supersedes key (control):      (['.ufo/waves/r1/new-receipt.json present=true reports/missing.md', ...], 2)
```

Case B is the defect: identical claim, only difference is the file also supersedes
something, and m10 goes clean. At freeze this is latent, not exercised: the single
contradiction in the tree (`.ufo/waves/round-41/residual/receipt.json` present=false for
`.ufo/waves/round-41/residual/ResidualReceipts.md`) is a **key** of the round-42 max
supersede receipt (`is key: True, is value: False`), i.e. a legitimate history exclusion —
m10's zero at freeze rests entirely on that one exclusion.

Finding 2 (BROADER, low/medium): `measure.py:213-215` scans **every** `.json` in the tree,
not only `.ufo/waves`; any JSON carrying nested `present: bool` + `report|path` is treated
as a presence receipt. Demonstrated: a receipt at `.ufo/evidence/x/receipt.json` asserting
`present=true` for `reports/nowhere.md` is counted
(`['.ufo/evidence/x/receipt.json present=true reports/nowhere.md'], 1`). No live bite at
freeze — all 17 claims come from `.ufo/waves/`.

Vacuity: `m10_receipts(lane, rev, [])` returns `([], 0)`. Structurally the subject is the
committed tree only (`git ls-tree`, `measure.py:350-355`): the round-43 wave receipts are
untracked (`?? .ufo/waves/round-43/`, 3 JSONs, 0 with `present`) and cannot be seen at
REV=freeze, so the zero says nothing about this round's receipts.

### m11 — SAME SET/QUANTIFIER; RESOLUTION IS COMMIT-ONLY

Contract: "*every 40-hex revision cited by those records resolves in the lane*".

Code: `m11_revisions` `measure.py:260-270`; resolution test
`git cat-file -e <token>^{commit}` at `measure.py:268`; dedupe `:264-266`.

Same cited set (same `record_texts`) and same universal quantifier. Evidence: the 3 cited
hashes (`242c1b4a…`, `322b5cd3…`, `c77c2b7e…`) are all commit objects at freeze, `revisions=3`.
Narrower in one respect: "resolves" is implemented as "is a commit". A cited **tree** hash
resolves (`git cat-file -e` → 0) but is reported as unresolved
(`(["r:1cbfb27d024e…"], 1)`), a false hit. `HEX40` at `measure.py:69` also skips any 40-hex
immediately preceded by `:` (`rev:<hash>` form is invisible). Vacuity: empty record set →
`([], 0)`, and the same missing-record silence as m7 applies (no round-43 lesson at freeze).

### m12 — NARROWER THAN THE SENTENCE (bold+colon field reduced to a substring)

Contract: "*the newest '## Round N' SCORECARD block carries '**Planned (round N+1):**'*".

Code: `newest_round_block` `measure.py:110-116`; `m12_planned` `measure.py:118-122`;
`wanted = 'Planned (round %d)' % (round_no + 1)` at `measure.py:120`, membership test
`wanted in block_text` at `measure.py:121`.

Heading selection and N→N+1 are the same statement. But the requirement is weaker than the
sentence: the bold markers and the trailing colon are not required, and the substring may
occur anywhere in the block. Proof:

```
prose-only m12 hits = []          # '## Round 9 … We Planned (round 10) stuff in prose, no field.'
proper field m12 hits = []
```

So m12 can be zero while the declared `**Planned (round N+1):**` field is absent — a class
that is clean without its subject existing. (`newest_round_block` also extends the "block" to
EOF, so text in a trailing non-round section would count; SCORECARD.md currently ends at the
round-42 block, `SCORECARD.md:1995-2046`, so no live bite.)

### m13 — CLAUSE (a) CHECK IS NOT THE COUNTING COMMAND (false-negative, demonstrated)

Contract: "*the newest standing sources-registry row's counting command names the
census-valid 0-3-space pattern, and an indented-row mirror proves the difference
(column0 = N-1, census-valid = N)*".

Code: `m13_standing_command` `measure.py:158-171`; clause (a) at `measure.py:165`
(`'0,3' not in newest and '0-3space' not in newest`) tests the **whole row line**, not the
command cell; the mirror probe `measure.py:166-170` uses `indent_mirror`
(`measure.py:148-156`) and `count_patterns` (`measure.py:140-146`) with the counter's own two
regexes, independent of the standing command.

Clause (b) is the same statement: `valid == column0 + 1` is exactly "column0 = N-1,
census-valid = N" (freeze: `column0=112 valid=113`, pass). Clause (a) is not: it is a
substring test over prose. Proof (`probe.py`):

```
row_bad_cmd_good_prose = | sources-registry | we discuss 0,3-space census conventions here |
                         `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` -> 113 rows at round 42 |
m13 hits = ([], 'standing=1 column0=112 valid=113')
m13 honest hits = ([], ...)          # identical verdict for the column-zero command
```

So m13 can be zero while the newest standing counting command is still column-zero — clean
without the subject (a census-valid counting command) existing. At freeze the real hit is
legitimate: `SCORECARD.md:2020` cites `^\| S[0-9]{3} \|`, hence `m13=1`.

Also: only lines beginning exactly `| sources-registry |` at column zero are standing rows
(`measure.py:127-128`), so an indented standing row would read as "no standing row"
(a hit, not a false clean).

## Findings by severity

| # | sev | class | finding | code |
|---|---|---|---|---|
| F1 | high | m10 | supersed**ing** receipts are added to the exclusion set, so their own contradicting claims are never counted (sentence excludes only the supersed**ed** target). Demonstrated: identical lie counted without a `supersedes` key, clean with one. | `measure.py:242-244,252` |
| F2 | high | m12 | requirement is the substring `Planned (round N+1)`, not the `**Planned (round N+1):**` field; prose passes. | `measure.py:118-122` |
| F3 | high | m13 | clause (a) tests the whole row for `0,3`/`0-3space`, not the counting command; a column-zero command plus prose `0,3` passes. | `measure.py:158-166` |
| F4 | medium | m8 | `endswith(SKIP_SUFFIXES)` gate drops directory/suffix-less cites (8 at freeze); brace "normalization" deletes the group, so `.ufo/…/c1-at-242c1b4a.{stdout,exit}` becomes a dropped `…242c1b4a.`. | `measure.py:182-186` |
| F5 | medium | m7,m8,m11 | declared record files absent at REV are skipped silently; at freeze `round-43.md` is missing, `records=3`, no hit/refusal, so these classes do not cover "the round-42/43 records". | `measure.py:357-361` |
| F6 | medium | m10 | scope is every `.json` in the tree, not `.ufo/waves`; demonstrated a `.ufo/evidence/` receipt counted. | `measure.py:213-215` |
| F7 | low | m11 | "resolves" is commit-only (`^{commit}`): a cited tree/blob hash resolves but is flagged; `HEX40` hides `rev:<hash>`. | `measure.py:268`, `:69` |
| F8 | low | counter | docstring documents `--records N` (`measure.py:40`); argparse has no such option (`--records 2` → `error: unrecognized arguments`, exit 2). | `measure.py:40`, `:326-329` |
| F9 | low | counter | `classes=7` is the constant `declared = 7`, and the predicate `declared == 7` is tautological; it is not a count of classes that ran (only the field loop at `:412-413` would KeyError on a missing class). | `measure.py:409,411,425` |
| F10 | low | m6 | the stated count is recognized only as `N rows at round M`; a correct count phrased otherwise becomes a hit (never a false clean). | `measure.py:133-138,377-378` |

## Vacuity (class can be zero without its subject existing)

| class | vacuity | evidence |
|---|---|---|
| m6 | **no** | no standing row → `stated=None` → `None == valid_count` is False → hit |
| m7 | yes, on missing records | `round-43.md` absent at freeze, silently skipped; empty record set → `[]` |
| m8 | yes, on missing records | empty record set → `[]` (probe5 case 3) |
| m10 | yes, on no receipts, and on untracked receipts | `m10_receipts(..., [])` → `([], 0)`; round-43 wave receipts untracked → invisible at REV |
| m11 | yes, on missing records | `m11_revisions(lane, {})` → `([], 0)` |
| m12 | yes, on the field | prose `Planned (round 10)` passes (`m12=0`) |
| m13 | yes, on the command | prose `0,3` in the row passes with a column-zero command (`m13=0`) |

## Residual risk and verification gaps

- F1 and F6 are latent at freeze; both are demonstrated only in throwaway repos, because the
  lane is read-only for this seat. The live m10 zero depends on exactly one exclusion, and
  that exclusion is a legitimate `key` (history), so the current zero is not manufactured by
  F1 — but a future superseding receipt that lies would be invisible.
- F5 is a property of the permitted revs: the counter reads `git show`/`ls-tree` only, so the
  untracked round-43 records and wave receipts are structurally outside m7/m8/m10/m11 at
  REV=freeze. A deciding run at a rev that commits those records is required before the
  `records=4`/`receipts` coverage can be called complete.
- Not audited here (other seats): the C1/C3 counters, the round-21 coldread monitor, and
  whether `m13_probe`'s `standing=6` includes every standing row the SCORECARD contract
  defines.
- The selftest (10 cases) does not cover the m12 prose case, the m13 prose-`0,3` case, the
  m10 superseder case, the m8 suffix-gate drop, or the m11 non-commit object; the three
  demonstrated false cleans are therefore unpinned by any test.

## Tooling

No tool installed or upgraded. All probes used in-tree `python3` (probe scripts written under
`/tmp/tameshi-r43-RevC2Classes`, deleted before returning).
