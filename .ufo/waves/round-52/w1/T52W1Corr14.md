# T52W1Corr14 — correction record for round-51 cold-read re-key `T51W2Read14`

Seat: T52W1Corr14 (scribe, calibration lane). L1 TameshiR52, wave 1. Milestone: C2 m4 correction record.
Lanerepo `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`.
Deliverable: `.ufo/waves/round-52/w1/T52W1Corr14.json` (written). Entry: heading
`### Gate/probe registry`, read_rev `02ec217c4d0afabe727fde2e261b7951d28fb4e9`, reader `T51W2Read14`,
reader file `.ufo/evidence/round-51/coldread/reads/T51W2Read14.md`.

## Behavior

Read `.ufo/evidence/round-52/contract.json` first (read, never edited): C2 `m4` requires one correction
record per round-51 re-key entry, a verbatim-quote `findings` list and
`wrong_expectations == len(findings)`. Then read the ledger entry, the reader file in full, and the
section at read_rev.

**Result: `findings: []`, `wrong_expectations: 0`.** The reader recorded no failing statement. The zero is
derived here from the reader's own verdicts, not inherited from round 51's write-from-code
(`coldread/refresh.py:224-227`, routed defect 3 of `corpus/lessons/round-51-verifier-spotcheck.md`): that
defect is that the count was unconditional, not that every reader found something.

Reader file facts: `wc -l` → `78` (79 lines when split, last line unterminated); sha256 at read_rev
`9b17352c4c1c13107b15fdbcb00bdde9c4e70c7c2045aa642a5c5b7b0971a2f8`, byte-identical to the working-tree
copy (`.ufo/waves/round-51/w2/T51W2Read14.md` is byte-identical too — `diff` → empty).

## Reader-record census (how the zero is derived)

```
$ f=.ufo/evidence/round-51/coldread/reads/T51W2Read14.md
$ grep -c '"raw":' $f                     -> 19
$ grep -c '"verdict": "holds"' $f         -> 20
$ grep -n '"verdict"' $f | grep -v '"verdict": "holds"'   -> (no output)
```

- 19 pointer rows (`reader:23-41`), every one `"verdict": "holds"`; the 20th is the section-level
  `"verdict": "holds",` at `reader:21`.
- `## Adversarial findings` (`reader:65`) body: "None actionable. No stale or moved pointer; no statement
  in the section is made false by the tenth leg, the runner TMPDIR change, or the four panel-tool updates."
  (`reader:67`).
- `reader:69` opens "Minor observations, not defects:"; the three items at `reader:70`, `reader:71`,
  `reader:72` are marked exact / locatable / outside a cold-read row's reach and are excluded by the item's
  rule.
- `## Verification gaps` (`reader:74-76`) records what the reader did not exercise, not a section
  statement it found not holding.

Section statements are all covered by those verdicts: table row 1 (pointers `reader:23-28`), table row 2
(`reader:29-33`), "Registry scope is these round-12 instruments…" (`reader:34`), "integrity-frozen
(declaration, mapping, target, spec, summary; `manifest.json` itself is not pinned, seat ReRead08)"
(`reader:35`), "not blind: …" (`reader:36`), the stale runner pin / `check` 1 DRIFT / `run`·`rerun` 2 /
`count` runner-independent claim (`reader:37`), "deepens one recorded case, never a seventh independently
measured gate" (`reader:38`), `SHONEN.md` box 3 `[~]` (`reader:39`), the spotcheck non-credit
(`reader:40`), the Appendix A/B scope disclaimer (`reader:41`). No statement of the section at read_rev is
without a `holds` verdict, and no verdict is other than `holds`.

## Candidates examined and why they are not findings

1. **Stale runner pin (the only runner-coupled statement).** Section: "The declaration's runner pin
   `75ed934d…` is stale at round 27 (`check` exits 1 DRIFT; `run`/`rerun` refuse, exit 2; `count` never
   reads the runner…)". Reader `reader:37` records **holds**, re-measured at CAND. Re-verified at read_rev
   independently:
   ```
   $ git -C … show 02ec217c:tools/mutate-and-run.sh | sha256sum
   977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda  -     # = reader's CAND sha 977de470…
   $ git -C … show 02ec217c:.ufo/evidence/round-12/BashWitness/declaration.json   (inputs.runner.sha256)
   75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5           # = pin the section calls stale
   ```
   The pin is still unequal at the re-key rev, so the "stale" claim and its exit contract hold. This is the
   class the item warns about ("even when the claim holds elsewhere") — the reader did not record it as
   moved, and the pointer is not stale for what it asserts.
2. **"integrity-frozen (… summary …)"** — reader `reader:35` records holds, listing pins
   `declared/sha256, target/pin, spec/sha256, runner/sha256`. Summary is pinned indirectly:
   `summary.json` sha `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9` appears in
   `.ufo/evidence/round-12/BashWitness/manifest.json` (`git grep -l` over `.ufo/evidence/round-12` at
   read_rev → that file), and `manifest.json` is the one the section itself says is not self-pinned. The
   statement is corroborated; the reader's holds stands; not counted.
3. **Verdict-map wording "2 and 64 could-not-evaluate"** (`reader:70`) — reader records it as the tool's own
   classification verbatim, "exact, not a compression"; excluded by the item's rule.
4. **"seat ReRead08" cited without a path** (`reader:71`) — the reader records the report as locatable;
   `git -C … cat-file -e 02ec217c:.ufo/waves/round-27/residual/ReRead08.md` → exists (rc 0). Not a finding.
5. **Historical round-12 byte state** (`reader:72`) — the reader discloses it is outside a cold-read row's
   reach and asserts nothing; a limit of the read, not a recorded failure.
6. **Verification gaps** (`reader:75-76`: `run`/`rerun` exercised only at the pin precheck; entry mode
   `--runs 3 --out DIR -- COMMAND` exercised via the selftest's child calls) — gaps of the read.

## Reader-metadata anomalies (not findings; recorded for the L1)

These are errors in the reader's own bookkeeping, not section statements it recorded as not holding. The
frozen `m4` counter does not read them; they do not change `findings`.

- `reader:4` says "section = lines 1499-1547; next heading `### Round-13 gate/probe registry` at 1548;
  parent `## Repeated controls and gate registry — round 12` at 1496". At read_rev the section is
  **1499-1516** (18 lines); the next line, 1517, is `## Pin disposition and provenance correction — round
  13`; the parent heading is at 1479; line 1496 is prose ("of reliability. Command stdout/stderr…").
  ```
  $ git -C … show 02ec217c:SKILL.md | grep -n '^## Repeated controls and gate registry\|^### Gate/probe registry\|^## Pin disposition\|^### Round-13 gate/probe registry'
  1479:## Repeated controls and gate registry — round 12
  1499:### Gate/probe registry
  1517:## Pin disposition and provenance correction — round 13
  1548:### Round-13 gate/probe registry
  ```
  Section bytes 1499-1516: sha256 `a8952368dc213a95b1d381647f65b6547abf649d7d56d6d18eb26ca159623538`,
  identical at read_rev and at the reader's candidate `6d8c11e3` (18/18 lines equal), so the reader did
  read these bytes; only its boundary arithmetic is off.
- `reader:34` attributes "Registry scope …" to `1505-1506` (actual 1506-1507) and `reader:41` attributes
  "Appending this registry …" to `1540-1547` (actual 1514-1515; 1540 at read_rev is inside the round-13
  pin-disposition list). Range metadata offset; the statements themselves are recorded as holding and were
  covered by the reader's verdicts.

## Gates / checks run (observed, never a verdict)

```
$ python3 -B <<'EOF'   # imports the frozen check_findings from .ufo/evidence/round-52/c2/measure.py
ledger-entry-matches: 1
entry heading= '### Gate/probe registry'
entry start/end= 1499 1516 wrong_expectations= 0 verdict= verified-record
record keys= ['heading', 'read_rev', 'reader', 'reader_file', 'wrong_expectations', 'findings']
heading-equal: True
read_rev-exact: True prefix-ok: True
reader-equal: True
reader_file-equal: True
reader-file-at-rev: rc=0 sha256=9b17352c4c1c13107b15fdbcb00bdde9c4e70c7c2045aa642a5c5b7b0971a2f8
reader-file-working-tree-identical: True
FLOORS for reader: ()
check_findings(record): None
wrong_expectations==len(findings): True len= 0
probe-substring-in-file: True -> check_findings: None
probe-forged: quote-not-verbatim:'None actionable. No stale or moved pointer NOT-IN-FILE'
probe-short: quote-not-verbatim:'abc'
EOF

$ python3 -B .ufo/evidence/round-52/c2/measure.py --selftest
SELFTEST leg-count ok
SELFTEST section-stops ok
SELFTEST quote-verbatim ok
SELFTEST quote-forged ok
SELFTEST quote-short ok
SELFTEST floor ok
SELFTEST range ok
SELFTEST range-miss ok
C2_SELFTEST: cases=8 failed=0
selftest exit=0
```

Per-quote substring self-check: there is no quote to check (`findings: []`), so the item's rule is
vacuously satisfied; `check_findings(record) -> None` is the frozen rule's pass value, and the two control
probes above show the same function rejects a forged and a short quote against this reader file (the file
text loads correctly, so the pass is not vacuous-for-the-wrong-reason). `wrong_expectations ==
len(findings) == 0`. No deciding-run verdict was taken; `m4`'s verdict belongs to the L1.

## Touched surfaces

- Written: `.ufo/waves/round-52/w1/T52W1Corr14.json` (deliverable), `.ufo/waves/round-52/w1/T52W1Corr14.md`
  (this report).
- Not written: the lane checkout. `.ufo/evidence/round-21/coldread/ledger.json` still has
  `len(corrections) == 0` in the working tree (the L1 inserts this record); contract, SKILL.md,
  `tools/registry.json`, `tools/round21-measure.py`, the fleet repo, sibling lanes, the lane's jj state and
  Git index untouched. No `git add/commit/stash/checkout/switch/reset/pull/push`, no mutating jj command.
- No fixture repo and no clone were needed, so no `rev-parse --show-toplevel` assertion applied; scratch
  `/fast/scratch/hyaku/tameshi-r52/T52W1Corr14/` was never created, so nothing to delete. No tool installed
  or upgraded (`~/.local/bin` and PATH dirs untouched; no pacman).

## Out of scope (not done, by bounds)

- No claim decision; no counter invocation against a lane rev (only `--selftest`); no ledger/SKILL.md/
  registry edit; no wave-2 re-key; no judgment of whether the section should change.

## Findings

Zero findings for `T51W2Read14`: the reader recorded 19 pointer verdicts and one section verdict, all
`holds`, an "Adversarial findings" body of "None actionable", and only explicitly excluded notes/gaps. See
"Candidates examined" (six items) and "Reader-metadata anomalies" (two items, non-findings).

## Summary
- Deliverable `.ufo/waves/round-52/w1/T52W1Corr14.json`: heading/read_rev/reader/reader_file exact; `wrong_expectations = 0`; `findings = []`.
- Reader `T51W2Read14` recorded 19 pointer verdicts and one section verdict, all `holds`; no non-holds (`grep -n '"verdict"' | grep -v '"verdict": "holds"'` → empty).
- `reader:65-67` "Adversarial findings" = "None actionable"; the notes at `reader:69-72` and gaps at `reader:74-76` are excluded by type (exact / locatable / out of reach / not exercised).
- Zero is derived from the reader record, not from round 51's write-from-code (`refresh.py:224-227`).
- Section at `02ec217c` = lines 1499-1516, sha `a8952368…9623538`, identical at reader CAND `6d8c11e3`; reader's own 1499-1547 / `:1505-1506` / `:1540-1547` bookkeeping is off (non-finding).
- Independently re-confirmed runner sha `977de470…` vs declaration pin `75ed934d…` at read_rev, and summary pin via `manifest.json` sha `acc01268…`.
- Frozen `check_findings(record) → None`; forged/short control quotes rejected; `c2/measure.py --selftest` → `cases=8 failed=0`, exit 0.
- Lane checkout untouched; no clone/fixture/scratch; no git/jj mutation; no tool install.
