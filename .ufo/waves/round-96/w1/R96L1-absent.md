# R96L1 — CORRECTION: the seat settled late; the earlier absence record is withdrawn

**Correction (2026-11-08 ~10:45 -03, after the orchestrator's `WAVE-DONE tameshi r96 w1`).**
The seat **did** land: `.ufo/waves/round-96/w1/R96L1.md` exists (and `R96L1-runs/`), and the
orchestrator's `w1-results.json` lists all 13 seats. The absence claim below was written at
10:39 -03 from the then-present files; it is kept only as the record of what the L1 observed
and of the defect it caused (a premature dead-seat call, `corpus/lessons/round-96.md` M5).
**The rounded report and the falsification ledger point at `R96L1.md`, not at this file.**
The seat's verdict (`partly refuted`) is integrated in the round report and confirms A1/A2/A6
independently.

---

## Superseded record (written 10:39 -03)

Seat `R96L1` (revenger, wave `w1`, round 96) was dispatched in
`.ufo/waves/round-96/w1-dispatch.json` (`counts.total=13`) and spawned by the orchestrator at
`2026-11-08T09:21:38` (`spawned tameshi 96 w1 13`, `.ufo/state/inline-dispatcher.log`).
It produced **no** report and no receipt under `.ufo/waves/round-96/w1/`.

## Evidence of absence, measured

- `ls .ufo/waves/round-96/w1/R96L1*` → no match (checked 2026-11-08 10:39 -03, after every
  other seat's report was on disk).
- Its scratch root `/fast/scratch/hyaku/tameshi-r96/R96L1/` exists with staging dirs
  (`clone-staged`, `lane-guard`, `variants`, `runs`, `work`) whose newest file is
  `runs/v96-abbrev.out`, mtime `2026-11-08 09:33:18 -03`; no write after that instant.
- The dispatcher wrote no `w1-results.json` for this wave either; the accounting file in
  this directory is L1-constructed and marks R96L1 `stalled-no-report`
  (`"_source": "l1-constructed"`).

## Consequence for the round

The hypothesis R96L1 held — *the v96 seal guards are inert: the honest note's twelve cells,
the 50/50 battery and the 19/17/2/0 disposition are unchanged under the guards* — is
**unmeasured** this round and is reported as unmeasured, not as holding. The claim set does
not depend on it: both claims rest on their own counters and batteries
(`.ufo/evidence/round-96/landing/`, `pre-freeze/controls/`), and R96E1/E2/E3/R96M1
independently exercise the guards.

Per the protocol a dead or stalled seat stays dead in the evidence; it was not replaced and
its slot is reported in the round report's wave accounting.
