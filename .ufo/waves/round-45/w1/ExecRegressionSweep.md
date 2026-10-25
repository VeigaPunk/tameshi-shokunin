seat: ExecRegressionSweep

## Assignment

Run every committed calibration counter against base `5891bdb77aba8489683533ae4cdd3b49b5e2626b`, read-only: round-41 (no freeze), round-42 `--freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f`, round-43 `--freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685`, round-44 `--freeze ba01973c73ad7de60e5bd19ae08255a1b7ef917e`. Paste final line + exit per counter; classify every non-zero class; output a table class × round → hits.

## Commands and receipts (all read-only, `--rev 5891bdb77aba8489683533ae4cdd3b49b5e2626b`)

**Round-41** — `python3 .ufo/evidence/round-41/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 5891bdb77aba8489683533ae4cdd3b49b5e2626b`
```
MISMATCH m7 S256 cited but absent from the registry
MISMATCH m7 S256 cited but absent from the registry
C1_R41: m6=0 m7=2 m8=0 m9=0 total=2 records=3 sources_rows=115 rev=5891bdb77aba8489683533ae4cdd3b49b5e2626b C1_R41_PASS=false
```
exit 1

**Round-42** — `python3 .ufo/evidence/round-42/calibration/measure.py --lane … --rev 5891bdb… --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f`
```
MISMATCH m7 S256 cited but absent from the registry
C1_R42: self_pin=1 m6=0 m7=1 m8=0 m10=0 m11=0 total=1 records=6 sources_rows=115 rev=5891bdb77aba8489683533ae4cdd3b49b5e2626b freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f C1_R42_PASS=false
```
exit 1

**Round-43** — `python3 .ufo/evidence/round-43/calibration/measure.py --lane … --rev 5891bdb… --freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685`
```
C2_R43: self_pin=1 classes=7 m6=0 m7=2 m8=0 m10=0 m11=0 m12=1 m13=0 total=3 records=4 sources_rows=115 standing=115 receipts=17 revisions=4 m13_probe=standing=8_column0=114_valid=115 rev=5891bdb77aba8489683533ae4cdd3b49b5e2626b freeze=6b83a11c61f0fad1074ec1f2a4c38a2fd7034685 C2_R43_PASS=false first=m7:SCORECARD.md#round-44_unknown_S256
```
exit 1

**Round-44** — `python3 .ufo/evidence/round-44/calibration/measure.py --lane … --rev 5891bdb… --freeze ba01973c73ad7de60e5bd19ae08255a1b7ef917e`
```
C2_R44: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 records=4 sources_rows=115 standing=115 receipts=17 revisions=4 m13_probe=standing=8_column0=114_valid=115 rev=5891bdb77aba8489683533ae4cdd3b49b5e2626b freeze=ba01973c73ad7de60e5bd19ae08255a1b7ef917e C2_R44_PASS=true
```
exit 0

## Table: class × round → hits

| class | r41 | r42 | r43 | r44 |
|---|---|---|---|---|
| m6  | 0 | 0 | 0 | 0 |
| m7  | **2** | **1** | **2** | 0 |
| m8  | 0 | 0 | 0 | 0 |
| m9  | 0 | n/a | n/a | n/a |
| m10 | n/a | 0 | 0 | 0 |
| m11 | n/a | 0 | 0 | 0 |
| m12 | n/a | n/a | **1** | 0 |
| m13 | n/a | n/a | 0 | 0 |
| total | 2 | 1 | 3 | 0 |
| PASS | false | false | false | true |

## Classification of non-zero classes

### m7 (r41=2, r42=1, r43=2) — known superseded false positive: the historical `safe_floor=S256` assignment value

All m7 hits are the same root cause: the round-43 C3 staged-id-guard deciding-run receipt field `safe_floor=S256` (`SCORECARD.md:2091`), quoted by later records. S256 does not exist in the registry at base (115 census-valid rows, max id S160 — verified `git show 5891bdb:corpus/SOURCES.md`), so any un-masked S256 token fires m7.

- r41 (2 hits): the round-41 counter's record grammar reads whole remainder-of-file sections. `SCORECARD.md` from `## Round 41` to EOF (contains 2091 and 2126) and `LOG.md` from `## 2026-10-25 — round 41` to EOF (contains LOG.md:2243 `safe floor \`S256\` admitted`, 2265/2268 `safe_floor=S256`) each cite S256 → 2.
- r42 (1 hit): section-scoped records. Only the `LOG.md` round-42 section (LOG.md:2168 → EOF; the round-43/44 log bullets live under it) contains S256 (2243/2265/2268). The round-41/42 lesson and scorecard sections (SCORECARD.md:1895-2048) contain no S256 → 1.
- r43 (2 hits): record set is lessons 42/43 + newest scorecard block + LOG slice. `SCORECARD.md#round-44` block (line 2126 `safe_floor=S256` — underscore form, missed by the round-43 prose-only `safe floor` mask) and the `LOG.md#round-44` slice (line 2268 `safe_floor=S256`) → 2. First hit reported as `m7:SCORECARD.md#round-44_unknown_S256`.

Round lesson that explains it: `corpus/lessons/round-44.md:83` (Mistakes row 1): “source is the historical `safe_floor=S256` assignment at `SCORECARD.md:2091` … the old record grammar masked the prose phrase `safe floor` but no criterion required assignment-form values to be masked → add `ASSIGN_ID` assignment-value masking in the round-44 successor and four T6 tests.” The round-44 C1 claim row (`SCORECARD.md:2126`) and lesson line 88-90 (“the S256 m7 false alarm is fixed and measured”) confirm. Empirical confirmation: the round-44 counter at the same base prints `m7=0 total=0 C2_R44_PASS=true`, exit 0.

None are genuine regressions of fixed records — no registry row changed at base; every hit is an assignment-value citation.

### m12 (r43=1) — superseded stale-expectation artifact (round-43 counter vs tree advanced to round 44)

The round-43 counter requires the newest `## Round N` scorecard block to match its own frozen contract round (43); at base the newest block is round 44, so the counter appends the mismatch hit (`round-43/calibration/measure.py:476-478`: “newest block is round 44, the contract round is 43”). The planned-field check itself passes: the round-44 block carries `**Planned (round 45):**` with a non-empty tail (`SCORECARD.md:2145`), so `m12_planned` returns no hits (measure.py:132-148). This is the age-stale counter expectation, not a record regression: round-43's own landing run at `3c4003f6` shows `m12=0` (`SCORECARD.md:2090`), and the round-44 successor (which superseded the round-43 counter) reads the same base revision clean — `m12=0`, total=0, PASS=true. Round lesson context: `corpus/lessons/round-44.md` and the round-43 scorecard row describing m12 (`SCORECARD.md:2060`).

## Notes

- No tools installed/updated (system python3/git sufficed; nothing needed the operator tooling channel).
- All four runs read only `git show` at the pinned rev/freeze; no lane file was written except this report.
