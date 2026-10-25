# MutOldBug — round-43 false-m7-alarm reproduction (round-44 w1)

**Seat:** L1Tameshi44.MutOldBug — **Milestone:** old-bug reproduction — **Axes:** calibration (C1, m7 value-vs-citation grammar)

## Mutation probe

- Target: round-44 counter `.ufo/evidence/round-44/calibration/measure.py` (line 89 `ASSIGN_ID`, line 109 its use in `m7_citations`), sha256 `c0c6199fd6172df69326834eaad4884a27427fdd84cf79404dd5b1f44bd9c0d6` = contract pin (`contract.json` C1 `counter_sha256`).
- Copy: `/tmp/tameshi-r44-MutOldBug-repro/measure_mutated.py`, identical sha256 before mutation.
- Mutation: replaced the ASSIGN_ID mask surface with the round-43 VALUE_ID_AFTER-only state — removed the `ASSIGN_ID` definition and the `masked = ASSIGN_ID.sub(...)` line, exactly the round-43 counter's value-masking surface (round-43 `measure.py` has no ASSIGN_ID; lines 71-84 vs round-44 lines 75-89).
- Nothing else changed; the round-44 `MASK_IDS` 'safe-floor' entry is label-skipped in `m7_citations` in both counters (line 104), so the only value-surface difference round-43 → round-44 is ASSIGN_ID.

## Regexes (quoted)

- `VALUE_ID_AFTER = re.compile(r'(?:staged:|next unused id|safe floor|register:)[^\n]{0,30}?\bS\d{3,}\b', re.I)` — prose-only: the literal alternative is `safe floor` (space). It cannot match the underscore assignment form `safe_floor=S256`.
- `ASSIGN_ID = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*"?S\d{3,}"?')` — round-44 addition, masks any `key=S###` assignment, including `safe_floor=S256` and `safe_floor = S256`. Removed in the mutant.
- `ID_RE = re.compile(r'(?<!staged:)\bS\d{3,}\b')` — the residual citation scan.

## VALUE_ID_AFTER-only probe (mutant module, live)

```
VALUE_ID_AFTER.search('safe_floor=S256')   -> None            # MISSED (underscore form)
ID_RE.findall('safe_floor=S256')            -> ['S256']        # residue -> m7 "unknown"
ASSIGN_ID.search('safe_floor=S256')         -> <re.Match ... match='safe_floor=S256'>   (round-44, removed)
VALUE_ID_AFTER.search('safe floor S256')    -> <re.Match ... match='safe floor S256'>   # prose masked
VALUE_ID_AFTER.search('safe_floor = S256')  -> None            # MISSED (underscore + spaces)
ASSIGN_ID.search('safe_floor = S256')       -> <re.Match ... match='safe_floor = S256'> (round-44, removed)
```

So `VALUE_ID_AFTER` alone (round-43 state) misses `safe_floor=S256` in both spacing forms; the residual `S256` survives to `ID_RE` and is reported as `r unknown S256` — the precise round-43 false m7 alarm.

## Selftest runs (scratch)

Baseline (pristine round-44 counter `measure.py`), exit 0:
```
C2_R44_SELFTEST: cases=16 failed=0
VERDICT: PASS
```

Mutant (`measure_mutated.py`, ASSIGN_ID removed), exit 1:
```
C2_R44_SELFTEST: cases=16 failed=2
FAIL T6_safe_floor_value_not_citation ['r unknown S256']
FAIL T6_assign_with_spaces_masked ['r unknown S256']
VERDICT: FAIL
```

T6 cases (lines 412-431) fail exactly as the contract's do-nothing control predicts (`.ufo/evidence/round-44/contract.json` line 36: "with the ASSIGN_ID mask line removed fails its own T6 selftest cases with ['r unknown S256']"). `T6_genuine_unknown_still_flagged` (S777) and `T6_unmined_flagged` (queued S001) still pass — the mutant only regresses the value-masking, not genuine-flagging.

## Verdict

- **Killed mutant** (the two T6 cases fail against the mutated detector; exit 1). The round-43 bug is reproduced precisely: with only the prose VALUE_ID_AFTER surface, `safe_floor=S256` reads as an unknown citation → `m7` fires → the round-43 C2 line `m7=1 total=1 first=m7:SCORECARD.md#round-43_unknown_S256` (receipt `.ufo/evidence/round-44/before/c2-old-at-base.stdout`).
- Coverage finding: the ASSIGN_ID surface is the exact fix that resolves the round-43 false alarm; removing it re-arms the bug, and T6 pins it.

## Restoration evidence

- Only the scratch copy `/tmp/tameshi-r44-MutOldBug-repro/measure_mutated.py` was edited (sha256 before `c0c6199f...`, after c `F39D` tag read); the lane checkout was never modified, no git/jj commands run.
- Scratch receipts preserved in report: baseline `baseline.selftest.stdout`, mutant `mutant.selftest.stdout`; scratch dir deleted after capture.
- No tools installed (no installs needed).
