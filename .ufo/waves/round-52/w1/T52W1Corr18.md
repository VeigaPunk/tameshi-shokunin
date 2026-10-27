# T52W1Corr18 — correction record for round-51 re-key entry `### Round-17 gate/probe registry — re-pin and monitor`

Seat: T52W1Corr18 (scribe). Item: C2 m4 correction record for reader T51W2Read18.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Section read at `02ec217c4d0afabe727fde2e261b7951d28fb4e9`, SKILL.md `:1846-1854`.
I decide no claim; every number below is a probe output or a byte read, reported as observed.

## Deliverable

`.ufo/waves/round-52/w1/T52W1Corr18.json` — exactly the six keys the item names (`heading`, `read_rev`, `reader`, `reader_file`, `wrong_expectations`, `findings`), one finding, `wrong_expectations: 1`.
`.ufo/waves/round-52/w1/T52W1Corr18.check.txt` — the verification transcript quoted below.

```json
{"heading": "### Round-17 gate/probe registry — re-pin and monitor",
 "read_rev": "02ec217c4d0afabe727fde2e261b7951d28fb4e9", "reader": "T51W2Read18",
 "reader_file": ".ufo/evidence/round-51/coldread/reads/T51W2Read18.md", "wrong_expectations": 1,
 "findings": [{"quote": "The cited section's shorthand 'as the round-16 row' does not state this changed scratch behavior or ten-leg contract.",
               "class": "stale-pointer",
               "skill_statement": "as the round-16 row; a borrowed repo identity is SETUP 2"}]}
```

## Behavior

1. Read `.ufo/evidence/round-52/contract.json` first (never edited): C2's m4 requires, per round-51 re-key entry, one top-level `corrections` record with `heading`, `read_rev`, `reader`, `reader_file`, `findings` (verbatim quotes ≥ 20 chars) and `wrong_expectations == len(findings)`.
2. Read the reader file in full. It is 5 lines: heading, blank, ```` ```json ````, one JSON line of 4,689 bytes, ```` ``` ````. Decoded the fenced JSON and enumerated its verdicts:

```
$ python3 - <<'EOF'  # decode fenced JSON, list verdicts
...
EOF
POINTERS=6
0 tools/evidence-disposition.py -> holds
1 tools/registry-check.py -> holds
2 tools/mutate-and-run.sh -> absent
3 tools/pin-disposition.py -> holds
4 .ufo/evidence/round-13/pin-manifest.json -> holds
5 .ufo/evidence/round-18/dispositions.json -> holds
NONHOLDING=['tools/mutate-and-run.sh']
```

3. Read the section bytes at the candidate:
   `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md | sed -n '1846,1854p'` → heading at `:1846`, table `:1848-1853`, blank `:1854`; the reader's `heading` string equals line 1846 byte for byte (`HEADING_AT_1846_OK=True`).

## The finding

- **Reader record:** `.ufo/evidence/round-51/coldread/reads/T51W2Read18.md:4`, pointer index 2, `"file":"tools/mutate-and-run.sh"`, `"verdict":"absent"`. Its `located_excerpt` says the shorthand "does not state this changed scratch behavior or ten-leg contract"; its `falsifier_checked` says "the pointer remains valid for guard/scrub and borrowed-identity SETUP 2, but 'as the round-16 row' is stale/incomplete: round-16 described seven legs and pre-TMPDIR behavior".
- **Section text it concerns:** `SKILL.md:1852` at the candidate — the row's Exits cell `as the round-16 row; a borrowed repo identity is SETUP 2` (command: `git show 02ec217c…:SKILL.md | sed -n '1852p'`).
- **Class `stale-pointer`:** the cell delegates the current runner contract to another registry row, and the reader recorded that delegation as no longer describing the tool. The substance is observable in the candidate runner (`git show 02ec217c…:tools/mutate-and-run.sh`): `:84` `… r16 seven; r18 eight; r26 nine; r51 ten …`, `:1510` `local nlegs=10`, and `:149-150` / `:160` / `:1432` the TMPDIR-honouring default scratch `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX`. The round-16 row the cell points at carries exits only (`SKILL.md:1810`), so the delegated text cannot carry either change — which is the reader's recorded point.
- **Observed nuance (reported, not upgraded):** the reader attributes "seven legs" to round-16. At the candidate the seven-leg fact lives in the runner's own ledger comment (`tools/mutate-and-run.sh:84`), while the round-16 SKILL row (`:1810`) states exits and no leg count. This does not weaken the recorded defect (the shorthand carries neither the ten-leg contract nor the TMPDIR scratch); it only locates the reader's evidence.

## Why one finding, and why not zero

- The reader marked 5 of 6 pointers `holds`; those are excluded by the item's rule.
- The reader's note on the four panel-tool updates is an explicit non-finding: "no claim here is falsified by their existence". Excluded.
- `strongest_falsifier_checked` restates the same defect ("This disproves reading 'as the round-16 row' as a current complete description") — a restatement, not a second expectation.
- The single `absent` pointer states one section-side shortfall with two facets (missing ten-leg contract; missing TMPDIR scratch). I recorded it as **one** wrong expectation, matching the reader's own unit of record (one pointer verdict), because the two facets are properties of the same delegated row, not two distinct section statements. A critic preferring per-facet granularity can extend without re-reading: the second byte-exact sentence is on the same line, `'as the round-16 row' is stale/incomplete: round-16 described seven legs and pre-TMPDIR behavior` (96 chars, class `stale-count`). I did not include it, to avoid inflating a count the way round 51 inflated it toward zero.
- Observed, not a verdict: at the candidate revision itself the ledger has **no** `corrections` key and **0** entries whose `read_rev` starts `02ec217c`; at the round-52 base `ef19d8e1` there are exactly 20 such entries (seats `T51W2Read01`…`T51W2Read20`). So the `corrections` list is the wave-2 append, as the counter's m4 expects.

## Gates run (probes only, never a claim verdict)

1. Item self-check — quote is a whitespace-collapsed substring of the reader file, 20–200 chars:
```
$ python3 …   # squash = re.sub(r'\s+',' ',s).strip(), same rule as check_findings
QUOTE_CHECK chars=117 in_reader=True ok=True
COUNT_CHECK wrong_expectations=1 len(findings)=1 ok=True
```
2. Frozen counter's own validator, imported from `.ufo/evidence/round-52/c2/measure.py` (no edit, no byte change):
```
$ python3 …  # import measure.py; m.check_findings(rec['findings'], reader_text)
check_findings -> None
```
3. Frozen counter selftest (allowed form):
```
$ python3 .ufo/evidence/round-52/c2/measure.py --selftest
SELFTEST leg-count ok / section-stops ok / quote-verbatim ok / quote-forged ok / quote-short ok / floor ok / range ok / range-miss ok
C2_SELFTEST: cases=8 failed=0        selftest exit=0
```
4. In-situ m4 probe on a scratch clone (`git clone --shared` of the lane at base `ef19d8e1`, toplevel asserted, my record plus 19 zero-finding stubs committed as a fixture rev; scratch deleted):
```
$ python3 .ufo/evidence/round-52/c2/measure.py --lane <scratch clone> --rev <probe rev> --explain
C2_CHECK m4 MISMATCH r51_entries=20 corrections=20 bad=['T51W2Read01:floor-uncovered::425', 'T51W2Read20:floor-uncovered:HIGH-1']
C2_R52: rev=<probe rev> m1=2 m2=1 m3=3 m4=2 m5=1 m6=0 total=9 C2_R52_PASS=false
```
`T51W2Read18` appears nowhere in that m4 bad list: the record satisfies the frozen per-entry path (heading/read_rev/reader/reader_file match, quote verbatim, count equals length). The two bads are the stubbed frozen-floor seats (`T51W2Read01`, `T51W2Read20`), which are other seats' records. This is a probe of one entry, not a score.

## Touched surfaces

- Written: `.ufo/waves/round-52/w1/T52W1Corr18.json`, `.ufo/waves/round-52/w1/T52W1Corr18.check.txt`, this report.
- Read-only: `.ufo/evidence/round-52/contract.json`, `.ufo/evidence/round-52/c2/measure.py`, `.ufo/evidence/round-52/control/controls.py`, `.ufo/evidence/round-51/coldread/reads/T51W2Read18.md`, `.ufo/evidence/round-51/coldread/reads/T51W2Read05.md` (granularity precedent), `.ufo/evidence/round-21/coldread/ledger.json`, `corpus/lessons/round-51-verifier-spotcheck.md`, `.ufo/waves/round-52/w1/T52W1Corr0{1,4,5,6}.json` (format precedent), and `git show` bytes at `02ec217c`, `ef19d8e1`.
- Tooling: none installed or upgraded (no need; python3/git only).

## Out of scope / not done

- Did not edit the round-21 ledger, SKILL.md, `tools/*`, ID the claim, or run the deciding/c1/c3 counters. No git or jj mutation in the lane or the fleet repo; the only commits were inside the scratch fixture clone, deleted after use.
- No `/tmp` writes beyond nothing; scratch root `/fast/scratch/hyaku/tameshi-r52/T52W1Corr18` removed before yielding.
- m6 (round-52 re-key entries) is not this seat's surface.

## Limits

- Whether one finding or a per-facet two is the "right" count is not frozen for this seat (contract C2 `cannot_see`: completeness of findings for the 18 seats without floors). I chose the reader's own unit of record and disclosed the alternative.
- The reader's verdicts are source-byte reads, not executions (its own `strongest_falsifier_checked` says so); my record reproduces its finding, not new runtime evidence.

## Summary

- Read the contract, the reader file in full, and the section bytes at `02ec217c` (SKILL.md `:1846-1854`).
- Reader T51W2Read18 records 6 pointer verdicts: 5 `holds`, 1 `absent` (`tools/mutate-and-run.sh`).
- Recorded exactly one finding: the row's `as the round-16 row` delegation is a stale pointer (candidate runner `:84`/`:1510` ten legs, `:149-150` TMPDIR scratch; round-16 row `:1810` exits only).
- Quote is 117 chars, byte-exact from reader line 4; `check_findings -> None`; frozen selftest `cases=8 failed=0`.
- In-situ m4 probe: my seat absent from the bad list; only the stubbed floor seats fail.
- One finding, not two: the reader's two facets belong to one pointer verdict; the alternative `stale-count` quote is disclosed.
- No claim scored; ledger, SKILL.md, tools and lane git/jj untouched; scratch removed.
