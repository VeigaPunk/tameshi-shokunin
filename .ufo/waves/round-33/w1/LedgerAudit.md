# LedgerAudit — round 33 w1 cold-read ledger audit

Seat: `tameshi-r33-w1-LedgerAudit-4` (reviewer, calibration axis).
Item: run the round-21 cold-read monitor at the freeze commit f6d8a891f1d966c5c3cdda385090da3a6e804675; file the receipt; size wave-2 cold-read seats against the files this round touches.

## Verdict

**PASS — the strict monitor runs clean at the frozen rev, and no cold-read ledger section currently cites a file that this round will alter in a way that breaks coverage today.** The monitor (round-21 selector delegating to the unchanged round-18 credit algorithm) measured 64/64 SKILL.md sections at f6d8a89 with `overrides_used=false`, `trace_gate=strict`, `calibration_restraint_score=8`, exit 0. Wave-2 seat sizing follows: 48 of the 64 covered sections cite `tools/*`; 19 cite `corpus/SOURCES.md`; exactly 3 cite `LOG.md`; exactly 3 cite `SCORECARD.md`; the 3 sections citing all four families are the ones that will drift when wave reports/scorecards/SOURCES land (details below).

## Re-runability and scope notes

- The round-21 selector (`measure.py`) reads blobs only via `git cat-file`/`git show` at an explicit `--rev` (no worktree access, no writes). It has no `--work` flag — `--work` belongs to the round-33 C1 counter, which this seat did NOT run (default-mode C1 counter is the L1's measurement step). "Fresh" was honored by running against a fresh clone of the lane in this seat's scratch, checked out at f6d8a89.
- The coldread package and round-18 `measure.py` are byte-identical at HEAD and at f6d8a89 (`git diff f6d8a89 -- .ufo/evidence/round-21/coldread/ .ufo/evidence/round-18/measure.py` empty), so the receipt is valid for the frozen rev and current HEAD alike.

## Receipt

Command (run from seat scratch `/fast/scratch/hyaku/tameshi-r33-seats/LedgerAudit/`; monitor copy relocated depth-preserving into `monitor/.ufo/evidence/round-21/coldread/`):

```
python3 monitor/.ufo/evidence/round-21/coldread/measure.py \
  --repo /fast/scratch/hyaku/tameshi-r33-seats/LedgerAudit/lane-clone \
  --rev f6d8a891f1d966c5c3cdda385090da3a6e804675 \
  > monitor-out.json 2> monitor-err.txt; echo $? > monitor-rc
```

Observed output (exit captured per round-32 closure item 3):

- `monitor-rc` = `0`
- `monitor-err.txt` = empty
- `monitor-out.json` (243252 bytes) key fields:
  - `revision` = `f6d8a891f1d966c5c3cdda385090da3a6e804675`
  - `overrides_used` = `false`
  - `trace_gate` = `strict`
  - `calibration_restraint_score` = `8`
  - `coldread.sections_covered` = `64`, `coldread.reasons` = `{"credited": 64}` — every emitted section credited, zero vetoed, zero uncovered.
- Lane clone provenance: `git clone` of the lane into scratch (rc 0), `git checkout f6d8a891…` (rc 0), `git rev-parse HEAD` = `f6d8a891f1d966c5c3cdda385090da3a6e804675`. No git write/jj commands anywhere; no lane or fleet state touched.

The `--work` freeze note from the item text maps to the C1 counter's own flag; for this monitor it is not part of the CLI, and no default-mode counter ran here.

## Ledger section census — files this round touches

Ledger: `.ufo/evidence/round-21/coldread/ledger.json` (schema `tameshi-coldread-ledger-v2`, 493 entries, 384 distinct section keys after dedup by start/end/heading/skill, family union across entries sharing a key).

Distinct sections citing each family:

| Family | Distinct sections | Notes |
|---|---|---|
| `tools/*` | 302 | 22 distinct tool input paths (incl. `tools/vendor/*.tgz` x2 and pinned `tools/mutate-and-run.sh@75ed…`); `tools/mutate-and-run.sh` most-cited (288 entries), `tools/trace-inputs.py` (156) |
| `corpus/SOURCES.md` | 110 | spread over rounds 1–26 entries |
| `LOG.md` | 3 | sections 17–29 (Standing rules), 131–245 (mutation-sweep recipe), 1155–1163 (cadence's first scheduled tick) |
| `SCORECARD.md` | 3 | the same three sections |
| All four families | 3 | sections 17–29, 131–245, 1155–1163 |

### Covered sections at f6d8a89 that cite the touched families

Of the 64 sections the monitor credits at the frozen rev (SKILL.md section starts):

- `tools/*`: 48 sections (starts 1, 17, 131, 314, 375, 405, 668, 827, 858, 883, 921, 933, 965, 1021, 1069, 1092, 1155, 1164, 1212, 1230, 1246, 1272, 1281, 1302, 1380, 1396, 1436, 1449, 1479, 1499, 1517, 1548, 1563, 1597, 1609, 1676, 1707, 1754, 1806, 1814, 1846, 1855, 1905, 1925, 1938, 1964, 2104, 2132).
- `corpus/SOURCES.md`: 19 sections (starts 6, 17, 131, 921, 1069, 1155, 1436, 1479, 1517, 1548, 1563, 1609, 1814, 1846, 1855, 1925, 1938, 1964, 2104).
- `LOG.md` and `SCORECARD.md`: 3 sections each — starts 17 (Standing rules), 131 (mutation-sweep recipe), 1155 (cadence's first scheduled tick). These are the only covered sections that will drift when wave-1/wave-2 reports and the scorecard are committed, because they pin `LOG.md` and `SCORECARD.md` digests.
- Sections with no citations of the four families (unaffected by this round's touches when re-measured): starts 30, 58, 94, 246, and the remaining unlisted starts (e.g., Source notes, Gate-shape decision table, mutation bar).

## Wave-2 sizing guidance for the L1

- New tool `tools/tally-audit-v2.py` (C1) appears in NO current ledger entry (it post-dates the ledger). Its addition to the lane does not drift any existing entry; cold-read seats only need a NEW section if the tool is written into SKILL.md. `tools/mutate-and-run.sh` is never edited (sha a7d3f2dd…2eb9 pinned), so the 288 entries pinning it stay stable.
- `corpus/SOURCES.md` (C2 supersedes-S055 row) WILL change its digest; the 19 covered sections that cite it will fail the input gate (`input-drift:corpus/SOURCES.md`) at wave-2 measurement unless re-read and re-pinned (or their records updated). These are the primary seats to size: 19 sections, concentrated in rounds 12–26 entry bands.
- `LOG.md` / `SCORECARD.md` will change with wave reports; exactly 3 covered sections (17–29, 131–245, 1155–1163) cite them and will drift. These three are also the only sections citing all four families — expect them to be the first cold-read seats in wave 2.
- Sizing floor: ~22 covered sections are pin-affected by this round's C1/C2 changes (19 SOURCES-citing + 3 LOG/SCORECARD-citing, with the 3 all-four counted once). If wave reports are re-committed mid-wave, the 3 LOG/SCORECARD sections may need re-reads per increment.

## Residual risk / verification gaps

- The monitor's per-section `sections` list contains start lines only; I matched ledger ranges by start containment. Where multiple ledger entries share a range (6 skill generations), a section's family membership is the union across entries at that start; the monitor itself matches by section sha256 against entry `sha256`, so the union is the correct sizing basis.
- I did not run the round-33 counters (C1 default mode, controls, or C2) — out of scope for this seat; nothing here predicts their verdicts.
- Ledger duplicate entries (52 duplicate skill/start groups) are a pre-existing ledger property, not introduced by this round; worth an L1 note but not a defect of this item.
