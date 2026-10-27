# T52W2RevCorr1720 — correction-record falsifier

Compared CAND0 correction records 17–20 in `ledger.json` with the complete reader files and the referenced sections at `02ec217c4d0afabe727fde2e261b7951d28fb4e9`. Commands: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show bcba8924894216268afc4171f06eb8c28e912b46:.ufo/evidence/round-21/coldread/ledger.json`; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md`. Reader line references below are within the named reader files.

## Corr17 — T51W2Read17, SKILL.md:1814–1845

- Over-counted: none. Record has no findings; reader 17’s pointer-by-pointer row entries call the claims “holds” (reader lines 1–300, 301–414); its disclosed nuances are explicitly immaterial, not failures.
- Missed: none found. The reader reports its section claims and recipe as holding (reader lines 1–300, 301–414); its live stale registry-row observation is described as caught by the section’s monitor, not a false section statement (reader lines 1–300).
- Verdict: **exact** (0 findings).

## Corr18 — T51W2Read18, SKILL.md:1846–1853

- Over-counted: none. Its sole record finding matches the reader’s `verdict:"absent"` and “stale/incomplete” text for `tools/mutate-and-run.sh` (reader line 4).
- Missed: none found. Other pointers are explicitly marked `holds`; the reader characterizes the omitted ten-leg/TMPDIR contract as the one stale-by-omission point (reader line 4).
- Verdict: **exact** (1 finding).

## Corr19 — T51W2Read19, SKILL.md:1905–1924

- Over-counted: none. The record’s `cases=10` / obsolete “from round 26 on” quote matches F1 and the explicit stale verdict (reader lines 21, 27–33; JSON row lines 56–60).
- Missed: none found. Reader marks the remaining section pointers P1–P6 and P8–P9 holds; its findings section identifies only F1 (reader lines 15–26, 27–39; JSON row lines 50–58).
- Verdict: **exact** (1 finding).

## Corr20 — T51W2Read20, SKILL.md:2132–2171

- Over-counted: none. Each of the seven recorded items is explicitly identified in the reader’s findings: HIGH-1/2, MED-1/2, LOW-1/2/3 (reader lines 62–81; summary at 87–95). The disclosed NOTE-A/B are expressly not row falsehoods (reader lines 83–85).
- Missed: none in the section. The reader notes `tally-audit-v2.py:266` has stale wording (reader line 72), but this is a tool comment, not a false statement in the section’s row; the section says the simulated literal `/tmp/tally-audit-work` is present (reader line 41), which the reader marks holding. All other row claims are marked holds or covered by the seven findings (reader lines 17–53).
- Verdict: **exact** (7 findings).

## Summary

All four records are exact against the reader’s explicit failures: Corr17 0/0, Corr18 1/1, Corr19 1/1, Corr20 7/7.
No over-count or missed section failure found. C2’s frozen counter cannot see completeness of these findings lists, as the round-52 contract states.
