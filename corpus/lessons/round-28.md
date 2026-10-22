# Round 28 — lesson (tameshi)

Base `06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c` (round-27 spot-check head).
Claims: C1 calibration repair (routed item 1 of
`corpus/lessons/round-27-verifier-spotcheck.md`): the frozen round-27 counter
`python3 .ufo/evidence/round-27/c1-measure.py --repo LANE --rev REV` reads
`covered=60/64 restraint=6 box3_mismatch=1` at base; target at the landed
head `covered=64/64 restraint=8 box3_mismatch=0` (exit 0).

## Gate

- S059 re-opened: https://bazel.build/remote/caching, fetched 2026-10-22
  with `curl -sL` (HTML sha256 `9e3a2ebba08234a1b5896faaea54be7c4aea2adb3e1051037f477d8f24d42348`).
  Located quote (§Remote Caching intro, "The remote cache stores two types
  of data"): "The action cache, which is a map of action hashes to action
  result metadata." (13 words). §Known issues still reads "Bazel currently
  does not track tools outside a workspace" — the row's recorded scope holds.
- Change log: S059 `used-by` `corpus/knowledge/input-keyed-coldread-credit.md`
  → `corpus/knowledge/input-keyed-coldread-credit.md, corpus/lessons/round-28.md`.
  Status `mined` and recheck `90d` unchanged. No new row; a first draft
  added S092 for the same URL, the census flagged W04 duplicate URL, and the
  draft row was removed before any commit.
- `Next unused id: S092.` appended (routed item 3; the stale S090 line kept).

## Mistakes

1. **class:** self-inflicted credit loss — the lane's own round bookkeeping
   de-credits cold-read sections. **evidence:** probe at base `06b59b93`,
   scratch clones under `/tmp/tameshi-r28-p-*`: appending one blank line to
   one file and committing, then running the frozen C1 counter, gives
   `corpus/SOURCES.md` 60→50, `corpus/README.md` 60→55,
   `corpus/QUALITY.md` 60→57, `SHONEN.md` 60→59, `LOG.md` 60→60,
   `SCORECARD.md` 60→60; all six together 60→47 (receipt
   `.ufo/evidence/round-28/append-probe.txt`). The monitor's input gate keys
   each credited entry to the sha256 of every recorded input
   (`.ufo/evidence/round-18/measure.py:47-55`, `input-drift:<p>`), and 99
   ledger entries record `corpus/SOURCES.md`. The frontier step requires a
   SOURCES edit every round, so the round's own conformance work removes
   credit after the cold reads that earned it — the same digest-keyed miss
   S059 describes. **captured-by:** none; the round-27 wave context excepted
   only SCORECARD.md, LOG.md and the ledger from reader inputs.
   **fix:** order the round so every edit to a widely read lane file
   (SOURCES, README, QUALITY, SHONEN) lands BEFORE the content revision the
   cold reads are run against, and run the monitor at the final landed head;
   the probe above is the failing case that shows the order matters.
