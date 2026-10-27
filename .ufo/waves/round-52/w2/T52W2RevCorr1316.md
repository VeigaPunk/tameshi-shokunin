# T52W2RevCorr1316 — falsifier of Corr13–Corr16

Reviewed each complete reader file and its section at `read_rev` `02ec217c4d0afabe727fde2e261b7951d28fb4e9`. Findings below assess whether every correction-record item quotes an actual not-holding statement (excluding holds and explicitly disclosed/historical-accurate notes), and whether the reader recorded other failures. Commands show the source bytes/text: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:<path>`; reader line citations refer to `.ufo/evidence/round-51/coldread/reads/`.

## Corr13 — T51W2Read13 — verdict: over

Reader file: `.ufo/evidence/round-51/coldread/reads/T51W2Read13.md`; section `### The map — where a reader enters, artifact by artifact`, SKILL.md:1380-1395.

- Over-counted: Corr13 finding 1 quotes reader line 16's runner-count failure but its `skill_statement` is the runbook-count phrase “§3 the six-case ledger (six rows; the lane has held nine cases since round 26)”. The reader explicitly calls the runbook's six-case presentation historical, not a current ten-leg roster (line 16); this is not a live failure. The actual failed nine-count statement is separately represented in findings 4 and 5 (reader lines 24 and 25). The record's runbook §7 TMPDIR item (finding 2) is also not a failure of the section statement: line 16 says the *runner* explicitly honors TMPDIR, but the section points to the runbook as detail-of-record and does not assert that runbook scratch defaults match runner defaults. Thus finding 2 is over-counted as a section-statement failure.
- Missed findings: none beyond the over-counted items. Reader lines 18, 24-26 record the measured-gate/ledger-row, two stale nine-count cells, and unsupported README-shape gloss, all present in the record.
- Evidence: reader lines 16-18 and 24-26 in full-file read; correction JSON `w1/T52W1Corr13.json` lines 8-36.

## Corr14 — T51W2Read14 — verdict: exact

Reader file `.ufo/evidence/round-51/coldread/reads/T51W2Read14.md`; section `### Gate/probe registry`, SKILL.md:1499-1547. Corr14 has `findings: []`. All pointer verdicts in the full reader row (lines 22-41) are `holds`; its adversarial findings section says “None actionable” (line 67). Lines 69-72 label the remaining observations as minor/locatable/historical and accurate; lines 74-76 are verification gaps, not false section statements. No missed failing statement.

Evidence: `T52W1Corr14.json` lines 2-8; reader lines 21-76. The reader's own shell expression reported in the Corr14 report (`grep -n '"verdict"' | grep -v '"verdict": "holds"'`) is consistent with its explicit full-file contents, but is not treated as independent semantic proof.

## Corr15 — T51W2Read15 — verdict: exact

Reader file `.ufo/evidence/round-51/coldread/reads/T51W2Read15.md`; section `## Seventh recorded case and full-page cold-read — round 16`, SKILL.md:1754-1813.

- Its sole correction finding is valid: reader line 11 directly says the progression stops at nine while the candidate runner has the tenth leg, and recommends adding the round-51 count. Corr15's quote and section statement match this failure.
- Missed findings: none. Reader lines 12-14 say the rest holds, including the reproduced block and no-impact checks; pointer rows 20-28, 30-48 are holds. The record-level dated receipts at reader line 65 are explicitly described as dated records needing no edit.

Evidence: `T52W1Corr15.json` lines 8-12; reader lines 9-14, 20-48, 61-70.

## Corr16 — T51W2Read16 — verdict: exact

Reader file `.ufo/evidence/round-51/coldread/reads/T51W2Read16.md`; section `### Round-16 gate/probe registry`, SKILL.md:1806-1813.

- All four Corr16 findings correspond to actual section statements the reader identifies as unsupported/incomplete: omitted measure selftest failure exit (reader line 92), undisclosed live-lane DEFAULT_REPO premise (line 94), omitted argparse exit (line 128), and inaccurate “round 17” provenance (line 115). The reader explicitly distinguishes these from the four pointer verdicts, all holds.
- Missed findings: none. Reader lines 99-101 concern a side observation outside the section; line 117 says the behavior claim is accurate, while the provenance tag is the failure; lines 133-148 conclude there is no other stale/moved pointer or round-51-introduced failure.

Evidence: `T52W1Corr16.json` lines 8-27; reader lines 82-148.

## Summary
- Corr13 over-counts two items: historical runbook six-case statement (finding 1) and TMPDIR comparison not asserted by the section (finding 2); no misses found.
- Corr14 exact; no missed findings.
- Corr15 exact; no missed findings.
- Corr16 exact; no missed findings.
- LSP status/references/definition/diagnostics were not available as a mounted device; conclusions cite the complete reader-file and correction-record text reads.