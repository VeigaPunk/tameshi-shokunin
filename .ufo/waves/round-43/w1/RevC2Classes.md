# RevC2Classes — C2 class-to-code agreement (round 43)

Seat: reviewer, calibration axis. Item: read
`.ufo/evidence/round-43/calibration/measure.py` against `claims.C2` in
`.ufo/evidence/round-43/contract.json`, quote each class sentence beside its
implementing code, and report broader/narrower classes and vacuity.

**The counter changed four times inside this seat's window** (A6/A7, A8, A10, A13). Report is
against the newest pin, with the earlier pin recorded where a finding was already repaired.
Read-only on the lane; probes ran in `/tmp/tameshi-r43-RevC2Classes` and `/tmp/t43rc`
(both deleted).

## Pin history (verified statically: file sha vs `claims.C2.counter_sha256`)

| counter bytes | first pinned at | note |
|---|---|---|
| `092c76cd6e10…` | `f0f2636`/`17f6ef0`/`5cd2154` | seat start; original F1–F10 filed against it |
| `52961c3709a3…` | `114ffac` (A6/A7), still at `53cb32b` | repaired m8/m10/m11/m12/m13 semantics; class sentences for those five reworded |
| `97609511bb77…` | `3aee2c0` (A10) → `ab76cbd3c98f…` at `f551ca6` (A13), current HEAD `6b83a11` (A14) | A10 adds m12 block-round binding and "field names something"; A13 reworks m7 value-id masking, m8 glob skip and m10 supersede coverage. **C2 class text, statement and target are unchanged from `53cb32b` through HEAD** (all seven sentences byte-equal) |

Correcting my previous replies: `52961c` was superseded by `97609511…`, which A13 then
superseded by `ab76cbd3…` (current pin). The contract's `claims.C2.counter_sha256` at HEAD
equals the working-tree file.

**Freeze-argument guidance (verified statically, blob sha vs `claims.*.counter_sha256`):**
`frozen_before` still names `114ffacd` as "the freeze of record", but A8–A14 landed after it;
at `114ffac`/`53cb32b` the contract pins C2 `52961c37…`, so `--freeze 114ffacd` gives
`self_pin=0`. The C1 pin break at `bb36f80` (`b56a34d7` pin vs `3d1ff3dc` blob) was repaired
at `f551ca6` (A13). At current HEAD (`6b83a11`, A14) and at `f551ca6`/`e25cd2f`, all pins
agree with their blobs: C1 `601c1840…` (A13/A14 bytes `601c1840…`), C2 `ab76cbd3…`
(bytes `ab76cbd3…`), C3 `47a6afce…` (bytes `47a6afce…`); guard `03a796c5…` = `tool_sha256`
and `frozen_tools.tools/staged-id-guard.py`; census `784de4c0…` unchanged. Valid `--freeze`
values for the deciding run: `f551ca6`, `e25cd2f`, `6b83a11`, or later self-consistent revs;
`114ffacd` (C1/C2/C3 old pins) and `bb36f80` (C1 unpinned) are invalid. Not measured here
(only `487b8f0` and `17f6ef0` are measurement revs for this seat); this is a sha comparison.

## Per class — current pin `97609511…`

Contract sentences are byte-identical to the ones reviewed at `53cb32b`, so the verdicts
below carry over; m12 gains two code requirements that the sentence does not carry.

### m6 — SAME STATEMENT

> "the newest standing sources-registry row's stated row count equals the census-valid
> registry row count"

`standing_registry_rows` `measure.py:151-157` (last `| sources-registry |` line),
`row_count_claim` `measure.py:159-164` (`N rows at round M`), comparison
`measure.py:444-446` against the census-valid line count `^ {0,3}\|\s*S\d{3,}\s*\|`. Same
statement. Not vacuous: no standing row → `stated=None`, `None == int` is False → hit.
Edge (open, benign direction): a correct count phrased differently becomes a hit.

### m7 — SAME QUANTIFIER AND MASKING; BROADER RECORD SET; MISSING-RECORD SKIP DISCLOSED, STILL CLEAN

> "every S-id cited by the round-42/43 records as a source is a mined row: staged:S###
> package tokens and 'Next unused id: S###' declarations are masked first"

`ID_RE` `measure.py:71`, `MASK_IDS` `measure.py:73-77` plus `VALUE_ID_AFTER`/`VALUE_ID_BEFORE`
(`measure.py:81-82`), masking and mined test `measure.py:449-463`; record set
`measure.py:424-437` (lessons **plus** the newest SCORECARD block and a LOG slice — broader than
"the records"). An absent lesson is skipped (`measure.py:425-427`) and the docstring now discloses it (`measure.py:41-47`), but
`records=` is not in the predicate, so m7 stays clean over an incomplete record set
(vacuity, disclosed).

### m8 — SAME STATEMENT

> "every backtick cite under corpus/, tools/, .ufo/, plans/, reports/ or the declared root
> files resolves at REV after :NN normalization and brace expansion; directory cites
> resolve by prefix"

`path_cites` `measure.py:217-229` (`:NN` strip, `expand_brace` `measure.py:198-207`, prefix/root
filter), `m8_paths` `measure.py:232-242` (directory by prefix). Same statement. Verified:
`…/c1-at-242c1b4a.{stdout,exit}` expands to both real paths; `.ufo/waves/` is admitted and
prefix-resolves. Residual: `measure.py:223` truncates a backtick token at the first
whitespace or `(`; `measure.py:221` skips any token containing `*`, so a glob cite such as
`tools/*.py` is dropped rather than resolved — a narrowing vs "every backtick cite".

### m10 — SAME STATEMENT

> "no presence receipt under .ufo/waves asserts present/absent contrary to the tree; only a
> receipt named in another receipt's supersedes is skipped, and the superseding receipt is
> graded"

`m10_receipts` `measure.py:245-314`: scope filter `:257` (`.ufo/waves/` + `.json`), superseder
collection `:266-272`, **coverage-based skip** `:298-310` — a stale claim is excluded only
when a *different* receipt re-asserts the same target with the tree-correct value; a
self-supersede, a chain that does not cover, or a wrong value leaves the claim counted
(fixtures v3–v6, `probe5` cases A–E). This is stricter than the sentence's unconditional
"named … is skipped": a stale claim whose superseder does not re-assert it is now a hit
(verified: case C `(['.ufo/waves/r1/old.json present=true reports/missing.md'], 2)`), so m10
can be non-zero where the sentence text would skip. Coverage also requires the exact
string match of `report` values; differing spellings (e.g. `./…` vs `…`) fail to cover.
Real-tree check: the sole contradiction at HEAD — `.ufo/waves/round-41/residual/receipt.json`
`present=false` for `ResidualReceipts.md` — is covered by
`.ufo/waves/round-42/supersede/round-41-residual-receipt.json` re-asserting `present=true`,
so `m10=0` still holds and is a *real* agreement.

### m11 — SAME STATEMENT

> "every 40-hex object cited by those records resolves in the lane (object existence, not
> commit-only)"

`m11_revisions` `measure.py:317-327`, `git cat-file -e <token>` at `:325`. Same statement.
Residual narrowing: `HEX40` `measure.py:75` skips a 40-hex preceded by `:` (`rev:<hash>`
never examined).

### m12 — CODE NOW STRICTER THAN THE SENTENCE (A10) + A REACHABLE CRASH

> "the newest '## Round N' SCORECARD block carries the field '**Planned (round N+1):**' (a
> prose mention is not the field)"

`newest_round_block` `measure.py:124-130`; `m12_planned` `measure.py:132-148`;
block/contract-round binding `measure.py:428-431` and `measure.py:475-478`.

The sentence-level requirement is implemented exactly (`wanted = '**Planned (round %d):**'`
`measure.py:139`, prose rejected). A10 adds two requirements the sentence does not carry, and
the class text was **not** updated (verified byte-equal at `53cb32b` and HEAD):

1. **The field must be followed by non-empty same-line text** (`measure.py:143-147`,
   "names nothing"). Repro: `m12_planned('## Round 9\n\n**Planned (round 10):**\n', 9)` →
   `['**Planned (round 10):** names nothing']`. A record that puts the planned claims on the
   following lines is a false hit.
2. **The newest block's N must equal `contract['round']`** (`measure.py:429-430` append
   `BLOCK_ROUND_MISMATCH`; `:476-478` an extra m12 hit). The sentence only says "the newest
   **## Round N** block"; it does not bind N to the contract. A pre-created round-44 stub
   heading, or a contract carried forward, becomes a hit even with the correct field.

**Crash (high):** when the block ends exactly at the field with no trailing newline,
`measure.py:145` slices to `''`, `''.splitlines()` is `[]`, and `[0]` raises. Verified:
`m12_planned('## Round 9\n\n**Planned (round 10):**', 9)` →
`RAISED IndexError list index out of range`. A SCORECARD whose last line is the Planned field
crashes the counter with a traceback (no `C2_R43:` line), which is neither a hit nor the
declared `exit 2` setup refusal. Reachable from record state alone; not exercised by the
current records (`SCORECARD.md:2076` carries inline text, newest block is round 43 = contract
round).

### m13 — CLOSE, TWO RESIDUAL MISMATCHES (unchanged by A10)

> "the newest standing sources-registry row's backticked counting command names the
> census-valid 0-3-space pattern, and an indented-row mirror proves the difference
> (column0 = N-1, census-valid = N)"

`m13_standing_command` `measure.py:184-203`; `commands` = backticked spans containing `grep`
(`:194`); clause (a) `:195-198`; clause (b) `:199-202` (`valid == column0 + 1` — same
statement).

- **R1 (narrower, false hit):** only spans containing `grep` count (`:194`). Verified:
  `` `awk '/^ {0,3}\| S[0-9]{3} \|/' corpus/SOURCES.md` `` →
  `['standing row carries no backticked counting command']`, though it names the pattern.
- **R2 (broader, false clean):** any grep span containing `0,3` passes, so a column-zero
  counting command plus a second `` `grep 0,3` `` cell is clean. Verified: `[]`.
- Positive: prose `0,3` beside a column-zero command is caught; the honest
  `grep -cE '^ {0,3}\| S[0-9]{3} \|'` cell is clean; the mirror is load-bearing
  (`column0=112 valid=113` at freeze; `113/114` on the 114-row working registry).

## Repairs and A10/A13 additions are not test-pinned (calibration gap)

`--selftest` = `cases=12 failed=0`; the twelve cases are unchanged since the `52961c` pin.
A10's two m12 requirements (tail, block-round binding) and A13's rework (m7 value-id masks,
m8 `*` skip, m10 coverage-based supersede skip) have **no fixture**; value m10's coverage
rule is documented in the docstring with wave-2 fixture names (v3–v6) but none are in the
selftest. Reverting each behaviour in a `/tmp` copy still passes:

```
a10a.py (m12 tail/“names nothing” removed)      cases=12 failed=0  VERDICT: PASS
a10b.py (block-round binding removed)           cases=12 failed=0  VERDICT: PASS
f1.py   (superseders excluded again)            cases=12 failed=0  VERDICT: PASS
f4.py   (brace deletion + suffix gate restored) cases=12 failed=0  VERDICT: PASS
f7.py   (cat-file '^{commit}' restored)         cases=12 failed=0  VERDICT: PASS
a13m.py (m10 coverage-based skip reverted to the unconditional key-skip)
        cases=12 failed=0  VERDICT: PASS
```

No receipt fixture (F6/F1/A13-m10 behaviour), no brace/directory fixture (F4), no object-type
fixture (F7), no missing-record fixture (F5), no tail/binding fixture (A10), no value-id
fixture (A13-m7), no glob fixture (A13-m8). The class text and code agree today except m12's
two additions and m10/A13's stricter coverage rule; the agreement can regress silently,
exactly as it did between the earlier pins.

## Vacuity under the current pin

| class | zero without its subject existing | evidence |
|---|---|---|
| m6 | no | `stated=None` always differs from an int count |
| m7 | yes, on a missing record file | `measure.py:425-427` skips; `records=` visible but not in the predicate |
| m8 | yes, on a missing record file | same record set |
| m10 | yes, on no receipts / untracked receipts | `([], 0)`; tree is `ls-tree`-only, so uncommitted round-43 receipts are invisible |
| m11 | yes, on a missing record file | same record set |
| m12 | no for the field; **yes** for the crash path (no measurement at all) | `IndexError` repro above |
| m13 | yes, via R2 | a second grep cell carrying `0,3` clears a column-zero counting command |

## Earlier-pin findings and disposition

| # | class | finding against `092c76` | status at `97609511` |
|---|---|---|---|
| F1 | m10 | superseding receipts were excluded (`superseded.add(value)`) | fixed at `52961c`, untested |
| F2 | m12 | field reduced to substring | fixed at `52961c`, tested |
| F3 | m13 | clause (a) scanned the whole row | fixed to command cells; R1/R2 remain |
| F4 | m8 | suffix gate dropped directory/brace cites | fixed at `52961c`, untested |
| F5 | m7/m8/m11 | absent record files skipped silently | docstring discloses; predicate unchanged |
| F6 | m10 | scope was every `.json` | fixed to `.ufo/waves/`, untested |
| F7 | m11 | commit-only `^{commit}` | fixed at `52961c`, untested |
| F8 | counter | documented `--records N` did not exist | fixed (fixed record set) |
| F9 | counter | `classes=7` is the constant `declared = 7` (`:484,500`) | disclosed in docstring; code unchanged |
| F10 | m6 | count accepted only as `N rows at round M` | open, benign direction |

New at the current pin: **N1** m12 crash (`measure.py:145`), **N2** m12 code stricter than
the class text (tail requirement, block-round binding) while A10 is marked
`rule_changed: false`, **N3** the `frozen_before` freeze-of-record narration (`114ffacd`)
now lags A8–A14, and the invalid-freeze set (`114ffacd`, `bb36f80`) is documented above.

## Residual risk and verification gaps

- N2 is a rule addition recorded in `amendments[].what` but not in `classes.m12` and not
  flagged `rule_changed`. The `amendments` array at HEAD carries A1–A14 (complete); it is the
  `amendments_note` prose that stops at A8, and its "class sentences restated verbatim" is
  false versus `17f6ef0`. Verified locus of the rewording: `classes` are byte-identical at
  `17f6ef0` and `5cd2154`, and m8/m10/m11/m12/m13 differ from `114ffacd` onward — so the
  `53cb32b`-vs-HEAD equality and the `17f6ef0` delta are consistent.
- N3 decides the run's `self_pin`: `--freeze 114ffacd` gives C2 0, `bb36f80` gives C1 0;
  at `f551ca6`/`e25cd2f`/`6b83a11` all three counters are pinned (C1 `601c1840…`, C2
  `ab76cbd3…`, C3 `47a6afce…`), so C2 can be graded there; the decision still rests on the
  L1 picking a self-consistent freeze rev.
- The repaired records are now committed (`c5335c7`, `e20cf89`): HEAD carries
  `SCORECARD.md:2048` `## Round 43`, `:2076` `**Planned (round 44):** …` (inline text), `:2081`
  standing row "114 rows at round 43" with a census-valid backticked grep cell, a 114-row
  `corpus/SOURCES.md`, and `corpus/lessons/round-43.md`. Under the current code these give
  m6=0 (114==114), m12=0 (block round 43 == contract round, field with tail content) and
  m13=0 (grep cell carries `0,3`; mirror 113/114). Round-43 wave receipts carry no `present`
  claims (3 JSONs at HEAD), so m10's subject is still the older 17 claims; m10's zero is only
  as good as the supersede-key exclusion.
- Had the 114-row registry landed without the restated standing row, m6 would read 1 — the
  L1's repair avoided that, and a deciding run at `f551ca6`/`e25cd2f`/`6b83a11` satisfies
  C2's self_pin=1 statically.
- Not audited here (other seats): C1/C3 counters, round-21 coldread monitor, the
  `m13_probe standing=N` denominator.

## Tooling

No tool installed or upgraded. Probes used in-tree `python3` only.
