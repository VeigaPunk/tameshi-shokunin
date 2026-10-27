# Round 51 — L1 integration notes (TameshiR51)

## N1 — the C3 surface sentence overstates the gap (found by the L1 after the freeze, before wave-1 results)

`contract.json` `claims.C3.axis` says the registry home "names 2 of the 30 lane tools that expose a self-test".
That reads only the `### Gate/probe registry` section (SKILL.md:1499-1516). SKILL.md at base carries twelve
registry sections (`grep -niE '^#{2,4} .*registry' SKILL.md`: round 12 at :1479/:1499, then rounds 13, 14, 15, 16,
17 (two), 18, 20, 21, 26). Counting a tool as named when its file name appears in a table row of any of them,
18 of the 30 frozen tools are named and 12 are not: golden-verdict.py, pbt-staged-id.py, shrink-case.py,
staged-id-guard.py, tally-audit.py, tally-audit-v2.py, tally-audit-v3.py, wave-parent-settle.py and the four
write-path-census versions (command in this file's commit: the python block run on 2026-10-26 ~21:10 -03).
The frozen predicate and counter are unchanged by this (they require a conforming row inside a section whose
heading starts `Gate/probe registry`, with the PROTOCOL fields the older rows mostly lack: the usage exit code and
the self-test finding id); the before value the counter prints (`covered=0 missing=30`) is a statement about that
canonical table, not about "no row anywhere". The report and SCORECARD state the corrected before: 12 of 30 tools
had no registry row anywhere, 18 had rows in per-round sections, none in the PROTOCOL field set the counter checks.
Class: a surface statement built from one section without a sweep for siblings. Mined in the lesson.

## N2 — placement of the new rows

Inserting rows at SKILL.md:1504 would shift every later SKILL.md line by 30 and stale every `SKILL.md:N` pointer
past it. The rows are appended at the end of SKILL.md under `#### Gate/probe registry — round 51` (four hashes: not a
cold-read section boundary, `HEADING_RE ^#{1,3}`), so no earlier line moves; the change touches the last cold-read
section (`### Round-26 gate/probe registry — report interop`), which the re-key covers.
