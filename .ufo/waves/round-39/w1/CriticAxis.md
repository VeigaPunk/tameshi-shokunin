# CriticAxis — Axis name (round 39, wave 1)

## Axis named
**Depth.** C2 changes a **fixture surface**, not a ledger leg. This is a census of the 21 lane-owned gate tools plus a behavioral FLAG_GATE fixture — not a coverage claim and not a new recorded case.

## Finding: no counterexample — the predicate's axis placement holds

### C2 touches a fixture surface, not the ledger
The freeze commit `233077f` adds `tools/write-path-census.py` (160 lines, sha256 `bc8c660c…dc62`, matching the contract pin `contract.json:30`). The ledger file `tools/mutate-and-run.sh` is byte-identical across the claim:

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 50aadd1bbd94e43cd3fcfb81459414394db2dc35 233077f -- tools/mutate-and-run.sh | wc -l
→ 0
```

Command D stays at 9 on both revs (canonical one-liner from `contract.json:36`):

```
git show 50aadd1…:tools/mutate-and-run.sh | python3 -c '…regex…'  → recorded_cases=9 depth_score=9
git show 233077f :tools/mutate-and-run.sh | python3 -c '…regex…'  → recorded_cases=9 depth_score=9
```

The 9 counted legs are the pre-existing recorded-case headers at `tools/mutate-and-run.sh:87-95`; none was added or removed.

### Where the new depth lives
- Fixture surface: `tools/write-path-census.py:77-83` — `update_expected()` writes an expected file only behind `update=True`; the `return False  # FLAG_GATE` early-return at line 80 is the mutation target (`.ufo/evidence/round-39/census/measure.py:119-124` replaces it with `update = True` and requires the selftest to then fail → `mutant_killed`).
- Planted classifier controls: `tools/write-path-census.py:57-61` (`PLANTED` unflagged/flagged/scratch strings scored in `selftest()` lines 86-114).
- `mutate-and-run.sh` appears only as one of 21 read-only census subjects: `tools/write-path-census.py:30` (`GATES` tuple), classified from `git show REV` bytes at `.ufo/evidence/round-39/census/measure.py:99-104` — it is observed, never extended.

### Do-nothing control holds
```
python3 .ufo/evidence/round-39/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 50aadd1bbd94e43cd3fcfb81459414394db2dc35
→ C2_R39: tool_absent=1 gates=0/21 planted_unflagged=0 planted_flagged=0 planted_scratch=0 fixture_wrote=0 mutant_killed=0 rev=50aadd1… C2_R39_PASS=false
```
Matches `contract.json:25` (`tool_absent=1 gates=0/21 … C2_R39_PASS=false`). Base also stays `C1_R39_PASS=false` per the recorded before-run at `.ufo/evidence/round-39/before/c1-at-base.stdout`.

## Impacted axes
Depth only. No calibration interaction (C1's guard is a separate `guard/measure.py` regex). Command D's `recorded_cases=9` is preserved — verified, not assumed.

## Smallest safe correction
None required. Note for the judge: `GATES` at `tools/write-path-census.py:30` names `mutate-and-run.sh` as a census *subject*; that is classification from REV bytes, not a ledger leg — a misread there is the only plausible false-positive attack, and the zero-line diff above falsifies it.
