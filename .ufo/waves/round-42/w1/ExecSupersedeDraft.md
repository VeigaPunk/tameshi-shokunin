# ExecSupersedeDraft — round-42 wave-1 report (C1 supersede receipt dry-run)

Date: 2026-10-25. Seat: leaf executor (godspeed). Scope: draft the C1 repair in a
scratch clone only; no live-lane edits besides this report.

## Findings

1. **Baseline at freeze (before repair), scratch clone at 322b5cd32b4319a05340d249ae752d12a9e6b19f:**
   `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-42/calibration/measure.py --lane /tmp/tameshi-r42-ExecSupersedeDraft-clone --rev 322b5cd32b4319a05340d249ae752d12a9e6b19f --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f`
   → `C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=1 m11=0 total=1 records=3 sources_rows=109 ... C1_R42_PASS=false`
   Only mismatch: `m10 .ufo/waves/round-41/residual/receipt.json asserts present=false for .ufo/waves/round-41/residual/ResidualReceipts.md; tree says true`. Matches contract before_expected.

2. **Observed truth at 322b5cd** (git ls-tree -r --name-only 322b5cd -- .ufo/waves/round-41/residual/): all 8 seat report files exist, including `ResidualReceipts.md`. So the supersede receipt asserts `present: true` for all 8 seats.

3. **Repair drafted** (scratch clone only): `.ufo/waves/round-42/supersede/round-41-residual-receipt.json` written, committed as
   `8c7edf6021d6edfe673a80e7c78cbad01cbfa440` ("round-42: supersede receipt correcting round-41 residual present=false (ResidualReceipts.md exists)"), 1 file, +40 lines.
   Clone checkout is clean (`git status --short` empty).

4. **Post-repair measurement** (deciding run for this wave, against the clone's HEAD):
   `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-42/calibration/measure.py --lane /tmp/tameshi-r42-ExecSupersedeDraft-clone --rev HEAD --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f`
   → `C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=0 m11=0 total=0 records=3 sources_rows=109 rev=8c7edf6021d6edfe673a80e7c78cbad01cbfa440 freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f C1_R42_PASS=false`
   `m10=0` (was 1); `records=3` unchanged, as expected — round-42 records do not exist yet, so `C1_R42_PASS=false` solely on records and the exit code is 1 for that reason. The m10 repair is complete and verified; the full C1 pass awaits the round-42 records (later wave).

5. The counter's selftest cases T2_* encode exactly this scenario (stale receipt counts; a valid superseding receipt re-asserting every path clears it; repeating present=false or omitting a path does not). Our receipt matches the "good" T2 shape: `supersedes` string present, zero stale assertions of its own (all 8 true and all resolve), and re-asserts every path of the superseded receipt (theirs ⊆ mine).

## Full JSON (byte-exact for landing)

File: `.ufo/waves/round-42/supersede/round-41-residual-receipt.json`
sha256: `987f82b4ce749787068d5845208382f930422d84126c94a7b2431e8d08334979` (1382 bytes)

```json
{
  "schema": "ufo-round-supersede-receipt-v1",
  "supersedes": ".ufo/waves/round-41/residual/receipt.json",
  "reason": "The round-41 residual receipt asserted present=false for .ufo/waves/round-41/residual/ResidualReceipts.md, but that report exists at the round-42 freeze commit; this superseding receipt re-asserts all eight seats with the observed tree truth.",
  "superseded_at": "2026-10-25",
  "seats": {
    "ResidualReplayC1": {
      "report": ".ufo/waves/round-41/residual/ResidualReplayC1.md",
      "present": true
    },
    "ResidualReplayC2": {
      "report": ".ufo/waves/round-41/residual/ResidualReplayC2.md",
      "present": true
    },
    "ResidualReceipts": {
      "report": ".ufo/waves/round-41/residual/ResidualReceipts.md",
      "present": true
    },
    "ResidualScope": {
      "report": ".ufo/waves/round-41/residual/ResidualScope.md",
      "present": true
    },
    "ResidualIds": {
      "report": ".ufo/waves/round-41/residual/ResidualIds.md",
      "present": true
    },
    "ResidualCounts": {
      "report": ".ufo/waves/round-41/residual/ResidualCounts.md",
      "present": true
    },
    "ResidualAppendOnly": {
      "report": ".ufo/waves/round-41/residual/ResidualAppendOnly.md",
      "present": true
    },
    "ResidualClaims": {
      "report": ".ufo/waves/round-41/residual/ResidualClaims.md",
      "present": true
    }
  }
}
```

## Risks / notes

- The scratch clone `/tmp/tameshi-r42-ExecSupersedeDraft-clone` is retained (per task instruction it was to be created; the report path convention says delete unless told to keep — the task instructs drafting+committing there, so I leave it for the L1 to reuse; note the commit `8c7edf6` is only in the clone, not in the live lane).
- Not checked: nothing else was needed — the live lane was never edited beyond this report; no tools installed (no installs required).
- C1 full pass (`C1_R42_PASS=true`) is blocked only by `records=3` (round-42 records absent), which is out of this seat's scope.
