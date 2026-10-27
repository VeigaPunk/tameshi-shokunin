# T52W1Corr15 — correction record for round-51 re-key entry `## Seventh recorded case and full-page cold-read — round 16`

Seat: `T52W1Corr15` (leaf). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, read-only (base
`ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`). Round-52 contract read first at
`.ufo/evidence/round-52/contract.json` (C2 m4: "one correction record per round-51 cold-read re-key entry (20)
… with verbatim reader quotes and wrong_expectations == len(findings)"); not edited.
Routed defect 3 of `corpus/lessons/round-51-verifier-spotcheck.md` is the reason the entry's
`wrong_expectations: 0` cannot stand.

Inputs read in full: reader file `.ufo/evidence/round-51/coldread/reads/T51W2Read15.md` (117 lines) and the
section at the re-key revision
`git -C <lane> show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md` lines 1754–1805 (the ledger entry's own
`start`/`end`; line 1806 is the nested `### Round-16 gate/probe registry`).

## Behavior

The reader recorded **one** statement of the section as not holding at its candidate: the leg-count
progression, which stops at `cases=9` while the runner at `02ec217c` carries ten measured legs. Everything else
in its 29-row pointer table is `holds`, and its "Record-level observations (not section defects)" block
(reader `:63-66`) explicitly exempts the dated case-note receipts and the ledger `input-drift` credit as records
that "need no edit". Per the seat spec those are not findings, so `findings` has one entry and
`wrong_expectations: 1` (the frozen entry's `0` becomes `1`).

Deliverable: `.ufo/waves/round-52/w1/T52W1Corr15.json` — exactly the six keys the item names
(`heading`, `read_rev`, `reader`, `reader_file`, `wrong_expectations`, `findings`).

## Findings (1)

### F1 — `stale-count`: the section's leg-count progression stops at nine; the runner has ten legs

- Reader evidence (reader `:11`, verdict summary; same verdict in the table at reader `:29` as
  `**stale at CAND**`):
  `- **One stale statement (the re-key edit this section needs):** the leg-count progression "(`tools/mutate-and-run.sh --regression` → `cases=7` at round 16; `cases=8` since round 18; `cases=9` since round 26)" stops at nine. …`
- Section statement concerned, `SKILL.md:1762` at `02ec217c` (section span 1754–1805):
  `` `tools/mutate-and-run.sh --regression` → `cases=7` at round 16; `cases=8` since round 18; `cases=9` since round 26``
  — shown by `git -C <lane> show 02ec217c…:SKILL.md | sed -n '1762p'`.
- Quote recorded in the JSON (159 chars, byte-exact substring of reader line 11, one line):
  `the leg-count progression "(`tools/mutate-and-run.sh --regression` → `cases=7` at round 16; `cases=8` since round 18; `cases=9` since round 26)" stops at nine.`
- `class`: `stale-count`. The two dated clauses were true when written; the open-ended progression is stale at
  `02ec217c` because a tenth leg landed in round 51.

Independent static check of the claim at the same revision (no execution needed, no repo write):

| Command | Observed |
|---|---|
| `git show 02ec217c…:tools/mutate-and-run.sh \| sed -n '84p'` | `# --regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten) — the fleet's` |
| `git show 02ec217c…:tools/mutate-and-run.sh \| sed -n '1459,1507p' \| grep -cE '^\s+regression_case_'` | `10` |
| `git show 02ec217c…:tools/mutate-and-run.sh \| grep -n 'bash-drift-pins'` | tenth ledger case at `:1504` (`regression_case_git bash-drift-pins`), leg declared for `kagi-shokunin/corpus/drift-pins.sh` |

So `--regression` reports `cases=10` at `02ec217c` (the reader cites the wave-1 receipt
`.ufo/waves/round-51/w1/T51ExecEmbed/regression.stdout`: `REGRESSION: PASS (cases=10 passed=10; …)`; I did not
re-run the runner, and the static count independently establishes the number). The section's progression must
gain "`cases=10` since round 51" (the reader's proposed re-key wording, reader `:70`).

### Why no other finding

- Reader table rows 1–9 and 11–29 are verdict `holds` (reader `:20-48`); they are not findings by the spec
  ("Do not count a reader's 'holds' verdicts").
- The reader's executed falsifier of the section's reproduce block returned `rc=0` with the exact expected
  lines and closed "Falsification of the reproduce claim **failed**" (reader `:61`), and its `falsifier` field
  states "The one candidate-made staleness found is pointer #10" (reader `:113`) — corroborating a one-finding
  set.
- Reader `:63-66` ("Record-level observations (not section defects)") marks the dated case-note receipts and the
  ledger `input-drift` credit as disclosed/historical and needing no edit; the spec excludes those.

## Gates run (instrument checks only; no claim decided)

| Check | Command | Observed |
|---|---|---|
| Frozen C2 counter selftest | `TMPDIR=<scratch> python3 -B .ufo/evidence/round-52/c2/measure.py --selftest` | 8/8 `ok`; `C2_SELFTEST: cases=8 failed=0`; exit 0 |
| Counter identity | `sha256sum .ufo/evidence/round-52/c2/measure.py` | `2c771d768e692811f7a39135800d27fbdb6403f4d12d46289bff404ee6ba9fbd` |
| Spec self-check: verbatim rule of the frozen counter (`check_findings`) | imported a byte-identical scratch copy of `c2/measure.py` (`sha256` equal), called `m.check_findings(record['findings'], git show REV:reader_file, ())` | `None` (passes) at base `ef19d8e1…`, at `02ec217c…` and at `HEAD` |
| Spec self-check: count | `wrong_expectations` vs `len(findings)` | `1` vs `1` |
| m4 wrapper preconditions for this entry | ledger at `HEAD`: `r51_entries=20`, heading matches `1`, `seat=T51W2Read15`, reader match, reader_file match, read_rev prefix match, heading byte-equal | all true |

`check_findings` output pasted verbatim (from `.ufo/waves/round-52/w1/T52W1Corr15.receipts.txt`):

```
KEYS ['heading', 'read_rev', 'reader', 'reader_file', 'wrong_expectations', 'findings']
COUNT wrong_expectations=1 len(findings)=1
CHECK_FINDINGS rev=ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4 -> None
  quote_len=159 in_reader=True in_one_line=True class=stale-count skill_statement_in_section(1754-1805)=True
CHECK_FINDINGS rev=02ec217c4d0afabe727fde2e261b7951d28fb4e9 -> None
  quote_len=159 in_reader=True in_one_line=True class=stale-count skill_statement_in_section(1754-1805)=True
CHECK_FINDINGS rev=HEAD -> None
  quote_len=159 in_reader=True in_one_line=True class=stale-count skill_statement_in_section(1754-1805)=True
M4_WRAPPER r51_entries=20 heading_matches=1 seat=T51W2Read15 reader_match=True reader_file_match=True read_rev_prefix=True heading_eq=True entry_wrong_expectations_now=0
QUOTE_REPR 'the leg-count progression "(`tools/mutate-and-run.sh --regression` → `cases=7` at round 16; `cases=8` since round 18; `cases=9` since round 26)" stops at nine.'
```

Not run (and why): `c2/measure.py --lane/--rev` (a claim counter; the L1 owns the deciding run), the C1 counter,
`no-harm.sh`, `controls.py`, `deciding-run.sh`, and the runner's `--regression`. The one claim I assert above
(the ten-leg count at `02ec217c`) is established statically from committed bytes.

## Touched surfaces

Written (all under `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-52/w1/`):

- `T52W1Corr15.json` — the correction record (deliverable).
- `T52W1Corr15.md` — this report.
- `T52W1Corr15.receipts.txt` — command outputs cited here (instrument sha + selftest, reader-file shas at three
  revisions, reader verdict lines, section lines 1754/1762/1805-1806, runner lines 84 and 1459–1507, the
  `check_findings` block).

Not touched: `SKILL.md`, `tools/registry.json`, `tools/round21-measure.py`,
`.ufo/evidence/round-21/coldread/ledger.json`, `.ufo/evidence/round-52/contract.json`, the reader file, any Git
index or jj state, the fleet repo, sibling lanes. No fixture repo was created; no counter was run against a
clone. Scratch `/fast/scratch/hyaku/tameshi-r52/T52W1Corr15` (holding only the counter copy used for the import
check) was deleted before yielding.

Pre-existing, not mine: `.ufo/evidence/round-52/c2/__pycache__/measure.cpython-314.pyc` (mtime
`2026-10-27T01:52:29-03`, gitignored by `.gitignore:4`) was already present when this seat's first command ran
(~02:10); left in place. My counter import ran against a byte-identical **scratch** copy with `python3 -B`, so
no bytecode was written by this seat.

## Out of scope (owned elsewhere)

- Appending this record to the round-21 ledger's top-level `corrections` list and re-scoring m4 is the L1's
  integration step; `ledger.json` still shows the entry with `wrong_expectations: 0`, `verdict:
  verified-record` at `HEAD`. m4 keys records by `heading` + `read_rev` prefix `02ec217c` + `reader`, all of
  which this record matches.
- The SKILL.md re-key edit itself (append "`cases=10` since round 51") and the wave-2 re-read of the touched
  sections.
- The other 19 re-key entries' correction records (other seats).

## Known limits

- The finding set is only as complete as the reader's own verdict column: the reader marked one row
  `stale at CAND` and everything else `holds`, and I adopted its verdicts rather than re-reading all 29 targets.
  I independently confirmed the one stale count (runner doc and ten regression cases at `02ec217c`), so a
  reader omission would be undetected here, not contradicted.
- `cases=10` is inferred from the ten ledger `regression_case_*` calls plus the runner's own doc line; I did not
  execute `--regression` (out of my run bounds and unnecessary for the count).
- Class taxonomy is the item's four values; a stale count rather than a false statement is the accurate label
  (the dated clauses `cases=7/8/9` remain true of their rounds).

## Conflicts

None observed. The reader's verdict summary (`:11`), its table row 10 (`:29`), its `reads.json` row (`:94`) and
its `falsifier` field (`:113`) agree with each other and with the committed runner bytes at `02ec217c`. For the
canonical Rust judge, the only discrepancy worth naming verbatim is between the ledger's recorded
`wrong_expectations: 0` and the reader's `- **One stale statement (the re-key edit this section needs):** the leg-count progression … stops at nine.` — the record above replaces `0` with `1`.

Tooling: no installs or upgrades (nothing needed; `python3`, `git`, `sha256sum` sufficed).

## Summary

- Reader `T51W2Read15` recorded exactly one non-holding statement in section `## Seventh recorded case and full-page cold-read — round 16` (SKILL.md:1762 at `02ec217c`, span 1754–1805).
- `stale-count`: the leg-count progression ends at "`cases=9` since round 26"; at `02ec217c` the runner's doc line `tools/mutate-and-run.sh:84` reads "r26 nine; r51 ten" and its ledger block carries ten `regression_case_*` calls (`:1459-1507`, `bash-drift-pins` at `:1504`).
- Record `T52W1Corr15.json` carries that one finding, `stale-count`, with a 159-char single-line quote from reader `:11` and the section statement it concerns; `wrong_expectations: 1`.
- Self-check under the frozen counter's own rule: `check_findings → None` at base, at `02ec217c` and at `HEAD`; `C2_SELFTEST: cases=8 failed=0`; m4 wrapper preconditions (heading, reader, reader_file, read_rev prefix) all match, `r51_entries=20`.
- No ledger, SKILL.md, registry or counter edit; scratch deleted; no tool installs.

Report: .ufo/waves/round-52/w1/T52W1Corr15.md
