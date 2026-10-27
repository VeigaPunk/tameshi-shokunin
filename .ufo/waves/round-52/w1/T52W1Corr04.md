# T52W1Corr04 — correction record for round-51 cold-read re-key `T51W2Read04`

Seat: T52W1Corr04 (scribe, calibration lane). L1 TameshiR52, wave 1. Milestone: C2 m4 correction record.
Deliverable: `.ufo/waves/round-52/w1/T52W1Corr04.json` (written). Section:
`### The boundaries — what a service run is not`, read_rev
`02ec217c4d0afabe727fde2e261b7951d28fb4e9`, reader `T51W2Read04`, reader file
`.ufo/evidence/round-51/coldread/reads/T51W2Read04.md`.

## Behavior

Read the contract first (`.ufo/evidence/round-52/contract.json`, read, not edited): C2 `m4` demands one
correction record per round-51 re-key entry, verbatim quotes, `wrong_expectations == len(findings)`.
Then read, in full, the ledger entry, the reader file (85 lines,
`awk 'END{print NR}'` → `85`), and the section at read_rev.

**Result: `findings: []`, `wrong_expectations: 0`.** The reader recorded no failing statement: 15 of the
section's pointers are recorded `**holds**` (`grep -c '| \*\*holds\*\*'` → `15`), the section-level verdict
is `**Verdict: every pointer in the section holds at CAND; no absent pointer, no stale range, no
unsupported load-bearing premise.**` (reader:31), and all five "strongest falsifiers" record
`all failed to falsify` (reader:33-40). The 0 is therefore derived from the reader record here, not
inherited from round 51's `refresh.py` write-from-code — which is the distinction routed defect 3 draws:
that defect is that the count was 0 *by construction*, not that every reader found something.

Section identity re-established independently at read_rev, not taken from the reader:

```
$ git -C …/tameshi-shokunin show 02ec217c…:SKILL.md | awk 'NR>=858&&NR<=882'
858: ### The boundaries — what a service run is not
…883: ### The report shape — what the opting-in lane receives
$ python3 -c "…sha256 of SKILL.md lines 858-882 at 02ec217c and at 6d8c11e3…"
section858-882 identical: True
sha at 02ec217c: fcfff5c18025e1dc585aca5e5725477099fcf178c29b57706ab2fbfd50a09e84
sha at 6d8c11e3: fcfff5c18025e1dc585aca5e5725477099fcf178c29b57706ab2fbfd50a09e84
```

Both equal the sha the reader printed (reader:8), so the reader read the same bytes that the ledger's
`read_rev` names (`ledger.json` entry: `heading` = the heading above, `read_rev` = `02ec217c…`,
`seats` = `["T51W2Read04", "L1 TameshiR51a3 integration (attempt 3)"]`, `wrong_expectations: 0`,
`verdict: verified-record`).

## Candidates examined and why they are not findings

1. **Runner-citation drift (the only non-`holds` note in the file).** Reader:18 records that the runner
   header gained one line, "the quoted claim is still fully inside the cited range, but the sentence's
   tail (…) now ends at :39, one line past the range. Pointer holds for the quoted text; noted for
   calibration." Falsifier 5 repeats it and labels it "(falsifier candidate found, **downgrade not
   falsification**)" (reader:39); the reader's own JSON row writes `"verdict": "holds"` with the note
   "quote itself inside" (reader:58) and "holds, downgraded note" (reader:76).

   Re-verified independently at read_rev:
   ```
   $ git -C …/tameshi-shokunin show 02ec217c…:tools/mutate-and-run.sh | awk 'NR>=33&&NR<=41'
   37: # INCONCLUSIVE (timeout 124, or 126/127 = suite not runnable). The target is
   38: # never written: every mutant is a fresh byte copy of the pinned pristine copy,
   39: # and the target's sha256 before/after is the restore proof.
   ```
   The section (`SKILL.md:865`) quotes only the words `"The target is never written"` against
   `tools/mutate-and-run.sh:36-38`. Those words are a contiguous, whitespace-collapsed substring of
   lines 37-38, i.e. **inside** the cited range. The clause the reader noticed moving out is the source
   comment's tail, which the section never cites. So this is not a stale or moved pointer to the text
   the section attributes, and the item's exclusion ("Do not count a reader's `holds` verdicts") applies.
   Recorded here so the L1 sees it; if the canonical reading is stricter ("a range must cover the whole
   source sentence"), this row would become one `stale-pointer` finding with quote
   `the quoted claim is still fully inside the cited range, but the sentence's tail` (reader:18) and
   `skill_statement` = the `SKILL.md:865` clause — the seat does not make that call.
2. **"(matrix row F)"** — an uncited inline premise (reader:28). Verdict `**holds** (premise corroborated
   in the file the bullet already cites)` with `fleet-suite-census.md:187,341` located. Not counted.
3. **Round-27 provenance aside** ("corrected in round 27 after the cold read of seat Read09") — reader:29
   verdict `**holds** (corroborated, not load-bearing)`; the residual risk at reader:83 says the aside
   "was corroborated … does not affect the verdict". A method gap the reader states about itself, not a
   recorded failure of the section. Not counted.
4. **Tenth leg vs "single-edit mutants only"** — falsifier 3 (reader:37) records "No recorded leg
   contradicts the boundary bullets". Not counted.
5. **Reader's method limits** (did not execute the runner; did not diff the round-27 correction) —
   reader:81-85. Limits of the read, not statements recorded as not holding.

No stale count exists in this section (no numeric count is asserted; the only number-adjacent claims are
the sha pair and the 4/4 / 0/6 composition figures, both recorded as holding).

## Gates / checks run (observed, never a verdict)

```
$ python3 -B - <<'EOF'   # frozen check_findings from .ufo/evidence/round-52/c2/measure.py, FLOORS.get('T51W2Read04', ())
keys: ['findings', 'heading', 'read_rev', 'reader', 'reader_file', 'wrong_expectations']
heading-exact: True
read_rev: 02ec217c4d0afabe727fde2e261b7951d28fb4e9
read_rev-prefix: True
reader_file: True
reader-exists: True
count==len: True findings= 0
check_findings(floors=Read04 none): None
no-quotes-to-check: True
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
exit=0
```

`check_findings(...) → None` is the frozen rule's pass value (`.ufo/evidence/round-52/c2/measure.py:82-95`
for `check_findings`, `:141-165` for the m4 path). Because `findings` is empty, the item's per-quote
rule ("each quote is a substring after whitespace collapse, 20-200 chars") is vacuously satisfied; there
is no quote to paste a per-quote line for. `wrong_expectations == len(findings) == 0`. No deciding-run
verdict was taken; m4's verdict belongs to the L1.

## Touched surfaces

- Written: `.ufo/waves/round-52/w1/T52W1Corr04.json` (deliverable), `.ufo/waves/round-52/w1/T52W1Corr04.md` (this report).
- Not written: the lane checkout (including `.ufo/evidence/round-21/coldread/ledger.json`, whose
  top-level `corrections` list is still empty — `len(corrections)` → `0` at base; the L1 inserts this
  record there), the contract, the fleet repo, sibling lanes, `~/.local/bin` or any PATH dir.
- No git/jj mutation, no index change, no commit; every read was `git show` or a direct file read. No
  fixture repo and no clone, so no `rev-parse --show-toplevel` assertion was needed.
- Scratch `/fast/scratch/hyaku/tameshi-r52/T52W1Corr04` was never created (nothing was written outside
  the two deliverable paths), so there is nothing to delete. No tool installed or upgraded (none needed).

## Out of scope (not done, by bounds)

- No claim decision; no counter run against a lane rev; no ledger edit, no SKILL.md edit, no registry
  edit; no wave-2 re-key; no mutation of the lane's jj state or Git index.

## Findings

Zero findings for `T51W2Read04`; see "Candidates examined" for the four recorded non-failing notes and
the one excluded-pointer judgement (runner-citation line drift, reader:18/39).

## Summary
- Deliverable `.ufo/waves/round-52/w1/T52W1Corr04.json`: heading/read_rev/reader/reader_file exact, `wrong_expectations = 0`, `findings = []`.
- Reader `T51W2Read04` recorded 15 `**holds**` pointer verdicts, a section verdict of "every pointer … holds" (reader:31), and five falsifiers that "all failed to falsify" — no failing statement.
- Count is derived from the reader record, not from round 51's write-from-code `wrong_expectations: 0`.
- Section at `02ec217c` = lines 858-882, sha `fcfff5c1…a09e84`, identical at reader's CAND `6d8c11e3` (`git show` + sha256).
- Only non-`holds` note is the runner-citation line drift (reader:18/39), excluded: the quoted words sit inside `:36-38` at read_rev (runner:37-38); the moved clause is not cited by the section. Recorded for L1 override.
- Frozen `check_findings` → `None`; `c2/measure.py --selftest` → `cases=8 failed=0`, exit 0.
- Lane checkout untouched; no clone/fixture/scratch, no git mutation, no tool install.
