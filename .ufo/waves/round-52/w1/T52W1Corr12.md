# T52W1Corr12 — correction record for round-51 cold-read re-key entry `### The six-leg regression — usage and this round's receipt` (T51W2Read12)

Seat T52W1Corr12, round 52 wave 1 (build + first falsifiers), lane `tameshi-shokunin`. Item: the ledger entry for the
six-leg regression section carries `wrong_expectations: 0` written from code (routed defect 3 of
`corpus/lessons/round-51-verifier-spotcheck.md`); read T51W2Read12's full read file and list every section statement it
recorded as not holding at the candidate. Deliverable: `.ufo/waves/round-52/w1/T52W1Corr12.json`.

## 1. Behavior

Produced one correction record for the ledger entry, `wrong_expectations: 14`, with 14 findings. The record is scoped to
what the reader recorded; it decides no claim and quotes no verdict of mine. Read-only on the lane except the two files
this item names (`.ufo/waves/round-52/w1/T52W1Corr12.json`, `.ufo/waves/round-52/w1/T52W1Corr12.md`).

The ledger entry as it stands (verified, §4 below) has `wrong_expectations: 0` while the reader's pointer table records
13 pointers failing at the candidate and one bullet understating — the overstatement the item names.

## 2. Sources read

- Contract `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-52/contract.json` (claim C2 m4; frozen
  floors `T51W2Read20`/`T51W2Read01` — this seat has no floor).
- Frozen counter `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-52/c2/measure.py:82-96`
  (`check_findings`), `:141-165` (m4 selection and field checks).
- Reader file `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-51/coldread/reads/T51W2Read12.md`
  (read in full; 176 lines). Present at REV:
  `git cat-file -e 02ec217c….ufo/evidence/round-51/coldread/reads/T51W2Read12.md` → exit 0; sha256
  `1be121139c8ae1d22386fa1b241c6d338a6b5f81d17ae0e1919ce81e1ca5449a` at REV and in the working tree (equal).
- Section text at read_rev, lines 1302–1364:
  `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md`
  (lines 1302–1364 dumped with numbers). Heading at `SKILL.md:1302`; next heading (`## Final pointers …`) at `:1365`.
- Section bytes at the reader's candidate are identical to the section at read_rev: section sha256
  `68cb8e72f29236e2e12306495093716d9262527deb41f7fc743133ea9a8dff0d` at both
  `02ec217c4d0afabe727fde2e261b7951d28fb4e9` and `6d8c11e378aa90b12650808e1b79270742935f15` (the reader already
  recorded this: reader `:18-19` "this section's bytes are identical at base and CAND (1302–1364)"). So the reader's
  CAND verdicts are the section's state at the ledger's read_rev, not a later drift.
- Runner state at read_rev (grounds the reader's drift at that rev, not only at CAND):
  `git show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:tools/mutate-and-run.sh` → 2159 lines; `:84`
  "# --regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten)"; `:88-97` ten leg
  lines (`js-round-gate`, `js-sources-check`, `js-cite-check`, `bash-drift-pins` appended); `:1432`
  `root=$(mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX")`; `:1446` `REGRESSION_EXPECT:`; `:1510`
  `local nlegs=10 npass=0 nfail=0 nsetup=0 st`. Same six lines at CAND `6d8c11e…` (runner 2159 lines there too).

## 3. Rule applied to decide what counts

One finding per reader pointer row whose verdict is not a hold: rows marked `drift`, `moved` (including `imprecise` /
`partial`), `half stale`, or `understates at CAND`. Rows marked `holds`, `holds-hist` (historical record, corroborated)
and `holds-as-disclosed` are excluded, per the item's rule; `holds-hist` rows explicitly qualified "at this write" or
"dated there since round 16" are the excluded class. Reader line references below are to
`.ufo/evidence/round-51/coldread/reads/T51W2Read12.md`.

## 4. Findings (14)

| # | reader line | reader verdict wording | class | quote (byte-exact, one line) | section lines | skill_statement |
|---|---|---|---|---|---|---|
| 1 | `:55` (P2) | `**drift**` | stale-count | `"`--regression` replays **six** embedded legs" \| **drift**` | 1305–1306 | `` `--regression` replays **six** `` / `` embedded legs `` |
| 2 | `:56` (P3) | `holds@sha (imprecise) + moved` | stale-pointer | `"list `tools/mutate-and-run.sh:85-89`" \| holds@sha (imprecise) + moved` | 1306 | `` (list `tools/mutate-and-run.sh:85-89` `` |
| 3 | `:57` (P4) | `holds@sha + moved` | stale-pointer | `"sources `:90-97`" \| holds@sha + moved` | 1306 | `` sources `:90-97` `` |
| 4 | `:58` (P5) | `holds@sha (partial) + moved` | stale-pointer | `"pins/tables `:550-559`" \| holds@sha (partial) + moved` | 1307 | `` pins/tables `:550-559` `` |
| 5 | `:59` (P6) | `holds@sha + moved` | stale-pointer | `"specs `:766`, `:841`" \| holds@sha + moved` | 1307 | `` specs `:766`, `:841` `` |
| 6 | `:60` (P7) | `holds@sha (partial) + moved` | stale-pointer | `"registry `:1132-1141`" \| holds@sha (partial) + moved` | 1307 | `` registry `:1132-1141` `` |
| 7 | `:63` (P10) | `**drift**` | false | `"default scratch `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`" \| **drift**` | 1320–1321 | `` default scratch `` / `` `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` `` |
| 8 | `:64` (P11) | `holds@sha + moved/extended` | stale-pointer | `"Exit map: 0 all legs PASS · 1 ≥1 leg FAIL · 2 cannot verify (SETUP) (`tools/mutate-and-run.sh:115-119`)" \| holds@sha + moved/extended` | 1322–1323 | `Exit` / `map: 0 all legs PASS · 1 ≥1 leg FAIL · 2 cannot verify (SETUP) (`tools/mutate-and-run.sh:115-119`)` |
| 9 | `:66` (P13) | `holds@sha + moved` | stale-pointer | `"r10-2 also mirrors the blob's mode … (`:104-106`, `:932-960`)" \| holds@sha + moved` | 1328 | `a `100755` blob is `chmod +x`'d after materialization (`:104-106`, `:932-960`)` |
| 10 | `:67` (P14) | `holds@sha + moved` | stale-pointer | `"the added selftest arms at `:1488-1527` cover the mirror" \| holds@sha + moved` | 1331 | `` the added selftest arms at `:1488-1527` cover the mirror `` |
| 11 | `:70` (P17) | `holds-hist, **stale at CAND**` | stale-count | `` "`--selftest` → `MUTATE_SELFTEST: 80/80 pass` / `VERDICT: PASS`, rc 0" \| holds-hist, **stale at CAND** `` | 1336 | `` `--selftest` → `MUTATE_SELFTEST: 80/80 pass` / `VERDICT: PASS`, rc 0 `` |
| 12 | `:71` (P18) | `holds-hist, stale at CAND` | stale-count | `` "`--regression` → six legs, all exact … closing `REGRESSION: PASS (cases=6 passed=6; …)`, rc 0" \| holds-hist, stale at CAND `` | 1339–1341 | the `--regression` receipt span, "six legs" through `` `REGRESSION: PASS (cases=6 passed=6; …` `` |
| 13 | `:72` (P19) | `holds@sha; half stale at CAND` | stale-count | `` "Each `REGRESSION_PIN` line now carries the blob's `mode=` … `REGRESSION_EXPECT` lists six recorded rates" \| holds@sha; half stale at CAND `` | 1343–1344 | `` `REGRESSION_EXPECT` lists six `` / `` recorded rates. `` |
| 14 | `:102` (§4 note) | the named-debt bullet "understates at CAND" (row `:82` P29: `holds, **understates at CAND**`) | stale-count | `The named-debt bullet understates at CAND: no ledger registry row exists and the registry is ten legs.` | 1361–1362 | `a ledger row recording the six-leg` / `registry is the ledger owner's follow-on` |

The `skill_statement` column above is abbreviated for the table; the JSON holds each one as the exact contiguous span of
the section text (newlines preserved), verified as a substring of the section at read_rev (no failures in the check, §6).

Notes on individual entries:

- #1, #11, #12, #13, #14 are stale counts recorded by the reader: six legs → ten (`reader :28`, `:88`); `80/80` →
  measured `107/107` (`reader :36`, `:90`, `:70`); `cases=6` → ten (`reader :136`, `:71`); "six recorded rates" → ten
  (`reader :95`, `:72`); "six-leg registry" → ten, named debt grew (`reader :102`, `:82`).
- #7 is recorded as false, not merely moved: at read_rev `tools/mutate-and-run.sh:1432` reads
  `"${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX"` (§2 command), and header `:149-150` says "(r51 honours TMPDIR)".
- #8 is recorded once although the reader names two defects (anchor moved `:115-119` → `:139-145`; rendering
  "extended"/incomplete with the r30 case-tally clause, `reader :94`). The reader row carries one verdict for one
  sentence, and a second finding would quote the same statement.
- #5's secondary note (only legs 5–6 specs are anchored; legs 1–4 specs sit at `:589/:630/:675/:720` sha)
  (`reader :59`, `:104`) is a coverage remark on the same pointer list, not a further section statement; the
  stale-pointer finding carries the row.
- #14: the row's verdict is `holds, **understates at CAND**` — the claim that no ledger cell is edited from here holds,
  but the debt description is stale ("six-leg"), so it is counted as a stale count; the quote is the reader's own §4
  note because the full row cell exceeds the 200-character cap.

Excluded rows and why (each a reader hold, not a drift):

- P1 `:54` `holds-hist` — the pinned revision's sha, 1 642 L and "uncommitted worktree file at this write" are
  historical and corroborated; the reader's cand_note that the file is 2159 L at CAND is a note under a holds verdict.
- P8 `:61`, P9 `:62`, P12 `:65`, P21–P25 `:74-78`, P27 `:80`, P28 `:81` — `holds`.
- P20 `:73` `holds-as-disclosed` — "Four legs at this revision" is the pre-dating phrasing, disclosed by the section
  itself ("dated there since round 16") and by errata `:1733`/`:1739`.
- P26 `:79` `holds` — the runbook's own stale anchors (`:350`, `:353`, `:361`) are disclosed and governed by the
  sentence the section states.
- F9 `:96-97` — "no additional statement made false".
- The §0 pinned-sha analysis (`:9-17`) and the reads.json rows (`:117-147`) restate the same findings; they are not
  separate section statements.

## 5. Ledger entry state (what the record corrects)

`python3` over the lane's working-tree ledger `.ufo/evidence/round-21/coldread/ledger.json` (the blob carrying the 20
round-51 re-key entries; the `02ec217c…` git blob predates them — `git show 02ec217c…:.ufo/evidence/round-21/coldread/ledger.json`
parsed through the frozen m4 filter yields `r51-entries 0`, the working-tree ledger yields 20, and its top-level keys are
`['carried_from','entries','provenance','round21_provenance','schema']` — no `corrections` list yet):

```
r51 count 20
seat T51W2Read12 read_rev-eq True reader True
reader_file True
entries with this heading anywhere: [('eb7838b1','CR37',0), ('01d586dd','CR30',0), ('4acdeac9','CR30',0),
                                     ('2227d833','Read22',0), ('bb681566','ColdA05',0), ('bb681566','ColdB05',0),
                                     ('02ec217c','T51W2Read12',0)]
```

i.e. the round-51 re-key entry (read_rev `02ec217c…`, seat `T51W2Read12`, `start: 1302`, `end: 1364`) records
`wrong_expectations: 0`; the reader records 14 failing statements. The deliverable supplies the correction record the
m4 clause selects (heading, read_rev, reader, reader_file, findings, `wrong_expectations == len(findings)`). Adding it
to the ledger's top-level `corrections` list is the executor's edit (out of this seat's bounds).

Dry run of the frozen m4 per-entry logic with this one record supplied (working-tree ledger + this JSON; the other 19
entries are left uncovered by design — this is a shape probe of my record, not a measure):

```
r51-entries(worktree ledger) 20
matched entry seat T51W2Read12 reader_file True check_findings None wel 14 len 14
M4_DRYRUN_SIM (1 record supplied; other 19 entries uncovered by design) bad= [None]
```

## 6. Self-check (frozen rule, `check_findings`)

Quote check — each quote after whitespace collapse is a substring of the reader file, on exactly one reader line,
20–200 characters (`python3 -c` over the deliverable, using the frozen counter's squash rule):

```
QUOTE_CHECK 01 PASS len=58 single_line=1 class=stale-count
QUOTE_CHECK 02 PASS len=70 single_line=1 class=stale-pointer
QUOTE_CHECK 03 PASS len=38 single_line=1 class=stale-pointer
QUOTE_CHECK 04 PASS len=54 single_line=1 class=stale-pointer
QUOTE_CHECK 05 PASS len=42 single_line=1 class=stale-pointer
QUOTE_CHECK 06 PASS len=53 single_line=1 class=stale-pointer
QUOTE_CHECK 07 PASS len=77 single_line=1 class=false
QUOTE_CHECK 08 PASS len=134 single_line=1 class=stale-pointer
QUOTE_CHECK 09 PASS len=83 single_line=1 class=stale-pointer
QUOTE_CHECK 10 PASS len=78 single_line=1 class=stale-pointer
QUOTE_CHECK 11 PASS len=102 single_line=1 class=stale-count
QUOTE_CHECK 12 PASS len=123 single_line=1 class=stale-count
QUOTE_CHECK 13 PASS len=138 single_line=1 class=stale-count
QUOTE_CHECK 14 PASS len=102 single_line=1 class=stale-count
QUOTE_CHECK_TOTAL findings=14 pass=14 wel=14
rc=0
```

Frozen checker on the record (`check_findings` imported from
`.ufo/evidence/round-52/c2/measure.py`, reader text from the file at read_rev; no floors for this seat):

```
check_findings: None
```

i.e. `None` = no mismatch; floors would only apply to `T51W2Read20`/`T51W2Read01` (`measure.py:31`).

Field match against the ledger entry (the fields the m4 selector compares; entry selected by
`read_rev` prefix + heading + `T51W2Read12` in `seats`, because the heading is shared by six earlier
entries — `('eb7838b1','CR37')`, `('01d586dd','CR30')`, `('4acdeac9','CR30')`, `('2227d833','Read22')`,
`('bb681566','ColdA05')`, `('bb681566','ColdB05')` — and a first probe that selected by heading alone returned the
`CR37` entry with `read_rev False` / `reader_file-match False`; m4 itself matches on heading *and* seat *and*
`read_rev`, so the collision does not affect it):

```
r51-entries 20
m4-fields heading True
m4-fields read_rev True 02ec217c4d0afabe727fde2e261b7951d28fb4e9
m4-fields reader True T51W2Read12
m4-fields reader_file True
m4-fields wel True 14 ledger-wel 0
keys ['heading', 'read_rev', 'reader', 'reader_file', 'wrong_expectations', 'findings']
```

Counter self-test (the only counter invocation; the counter was not run as a measure — no deciding run from this seat):

```
$ TMPDIR=/fast/scratch/hyaku/tameshi-r52/T52W1Corr12 python3 .ufo/evidence/round-52/c2/measure.py --selftest
SELFTEST leg-count ok
SELFTEST section-stops ok
SELFTEST quote-verbatim ok
SELFTEST quote-forged ok
SELFTEST quote-short ok
SELFTEST floor ok
SELFTEST range ok
SELFTEST range-miss ok
C2_SELFTEST: cases=8 failed=0
rc=0
```

## 7. Findings (seat notes, not verdicts)

- The ledger entry's `wrong_expectations: 0` is the routed defect reproduced exactly: the reader's own table records
  13 failing pointers and one understatement, and its §1 summary lists five drifts (`reader :26-40`).
- The reader's candidate and the ledger's read_rev carry identical section bytes (sha `68cb8e72…`, §2), so no wave-2
  edit is needed to make the drift true at `02ec217c…`; it is already true there. Runner at that rev: ten legs, TMPDIR
  honoured (§2 command output).
- The section hedges its anchors with "line anchors as read at `75ed934d…`, the sha governs" (`SKILL.md:1308`). The
  reader's legend still classes `holds@sha` as "moved/stale at CAND" (`reader :49`), and the item counts moved pointers
  "even when the claim holds elsewhere"; the 7 pointer findings follow that rule.
- `P17`/`P18` are historical receipts (`holds-hist`) that the reader nonetheless marks stale at CAND because the
  recorded totals are what its wave-2 statement checks need (`reader :70-71`); they are counted as stale counts, not as
  false history.
- The named-debt bullet understates: at read_rev the ledger has no registry row and the registry is ten legs
  (`reader :102`). Recorded as #14.

## 8. Touched surfaces / out-of-scope

Touched: `.ufo/waves/round-52/w1/T52W1Corr12.json` (new), `.ufo/waves/round-52/w1/T52W1Corr12.md` (this report).
Not touched: `SKILL.md`, `tools/`, the round-21 ledger, the contract, the counters, any git/jj state. Out of scope here:
appending the record to the ledger's top-level `corrections` list (executor), the C2 measure at the deciding REV (L1),
the `m6` re-key entries (wave 2), and the SKILL.md corrections themselves.

Scratch `/fast/scratch/hyaku/tameshi-r52/T52W1Corr12` held the draft JSON and the runner dump; deleted before yield. No
tool installed or upgraded (nothing needed); no pacman transaction.

## Summary

- Correction record for read_rev `02ec217c…`, reader `T51W2Read12`: `wrong_expectations: 14`, 14 findings with
  byte-exact one-line quotes, classes and section statements.
- Ledger entry currently records `wrong_expectations: 0` (round-51 routed defect 3); no other entry field differs.
- Section bytes are identical at read_rev and the reader's candidate (`SKILL.md:1302-1364`, sha `68cb8e72…`), and the
  runner at read_rev has ten legs / honours TMPDIR, so the reader's drift is true at the ledger's rev.
- Classes: 1 false (the `/tmp` default), 8 stale-pointer (runner anchors), 5 stale-count (six legs, 80/80, cases=6,
  six rates, six-leg registry/named debt).
- Excluded per the item's rule: P1 holds-hist, P20 holds-as-disclosed, P26/F9 and the remaining `holds` rows.
- Frozen `check_findings` → `None`; all 14 quotes PASS the substring/single-line/length check; `C2_SELFTEST cases=8
  failed=0`.
- No claim decided, no counter run as a measure, no tool installed, scratch deleted.
