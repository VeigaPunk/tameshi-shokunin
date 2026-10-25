seat: ExecLiveDriftR43

# considerthese proposal 1 grounding: measured-to-landing drift check (round 43 vs round 44)

Item: considerthese/2026-10-25.md lines 66-68 ('Measured-to-landing drift check'). Re-ran the
round-43 and round-44 calibration counters at both their measured and landing revisions with the
frozen freezes, listed the measured-to-landing diff, and compared the claims.

## Round-43 counter runs (freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685)

Command (both): `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-43/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV --freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685`

Measured `3c4003f6e97e5c787e7538b2eb35d62f49783aaf` (exit 0):

```
C2_R43: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 records=4 sources_rows=114 standing=114 receipts=17 revisions=3 m13_probe=standing=7_column0=113_valid=114 rev=3c4003f6e97e5c787e7538b2eb35d62f49783aaf freeze=6b83a11c61f0fad1074ec1f2a4c38a2fd7034685 C2_R43_PASS=true
```

Landing `718a1e987febd32eb78ebc65adfe939f23b3de63` (exit 1):

```
C2_R43: self_pin=1 classes=7 m6=0 m7=1 m8=0 m10=0 m11=0 m12=0 m13=0 total=1 records=4 sources_rows=114 standing=114 receipts=17 revisions=4 m13_probe=standing=7_column0=113_valid=114 rev=718a1e987febd32eb78ebc65adfe939f23b3de63 freeze=6b83a11c61f0fad1074ec1f2a4c38a2fd7034685 C2_R43_PASS=false first=m7:SCORECARD.md#round-43_unknown_S256
```

`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --stat 3c4003f6e97e5c787e7538b2eb35d62f49783aaf 718a1e987febd32eb78ebc65adfe939f23b3de63`:

```
 .ufo/evidence/round-43/after/c1-at-3c4003f6.exit   |  1 +
 .ufo/evidence/round-43/after/c1-at-3c4003f6.stdout |  1 +
 .ufo/evidence/round-43/after/c2-at-3c4003f6.exit   |  1 +
 .ufo/evidence/round-43/after/c2-at-3c4003f6.stdout |  1 +
 .ufo/evidence/round-43/after/c3-at-3c4003f6.exit   |  1 +
 .ufo/evidence/round-43/after/c3-at-3c4003f6.stdout |  1 +
 LOG.md                                             |  3 ++
 SCORECARD.md                                       | 37 ++++++++++++++++++++++
 8 files changed, 46 insertions(+)
```

The measured→landing span is exactly one commit: `718a1e9 round-43: deciding-run receipts and verdict records`
(`git log --oneline 3c4003f..718a1e9`). Of the 8 changed files, the record-touching ones are LOG.md
(+3) and SCORECARD.md (+37); the other six are round-43 evidence `after/` counter receipts.

Verdict: proposal claim CONFIRMED. Measured rev is green (m7=0, PASS=true, exit 0); landing rev is red
(m7=1, PASS=false, exit 1) with the first failing class `m7:SCORECARD.md#round-43_unknown_S256`. Drift
mechanism: commit 718a1e9 appends a "### Round 43 — after the deciding run" block to SCORECARD.md that
quotes the C3_R43 record line including `safe_floor=S256`; S256 is not a mined registry row at
718a1e9 (the row landed in a later round), so the frozen C2 m7 class fires "unknown S256". The LOG.md
addition (3-line deciding-run summary) is inert for m7.

## Round-44 counter runs (freeze ba01973c73ad7de60e5bd19ae08255a1b7ef917e)

Command (both): `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-44/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV --freeze ba01973c73ad7de60e5bd19ae08255a1b7ef917e`

Measured `ef990aaea3f6546db20feccbff89ac9ab78c5405` (exit 0):

```
C2_R44: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 records=4 sources_rows=115 standing=115 receipts=17 revisions=2 m13_probe=standing=8_column0=114_valid=115 rev=ef990aaea3f6546db20feccbff89ac9ab78c5405 freeze=ba01973c73ad7de60e5bd19ae08255a1b7ef917e C2_R44_PASS=true
```

Landing `df000ab79a4c526bcb5cbf03a356c1a44fb32e27` (exit 0):

```
C2_R44: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 records=4 sources_rows=115 standing=115 receipts=17 revisions=4 m13_probe=standing=8_column0=114_valid=115 rev=df000ab79a4c526bcb5cbf03a356c1a44fb32e27 freeze=ba01973c73ad7de60e5bd19ae08255a1b7ef917e C2_R44_PASS=true
```

Span: two commits — `2240848 round-44: record final counter and no-harm measurements`, `df000ab round-44: record wave-1 settlement`; `git diff --stat ef990aae df000ab7` = 18 files +3750 -3, record-touching: SCORECARD.md (+20/-3), LOG.md (+2), `.ufo/waves/round-44/w1/summary.md` (+8) plus before/after evidence receipts.

Verdict: round 44 did NOT have the same drift — both measured and landing are green (m7=0, total=0,
PASS=true, exit 0). The post-measurement SCORECARD additions did not cite any unknown/unmined S-id,
so the round-43 drift did not recur in round 44.

## Notes
- No tools installed/updated (nothing needed; read /home/vgpnk/.omp/agent/RULES.md first).
- No scratch files needed; report-only write in the lane.
- Counter runs used the allowed `--rev`/`--freeze` forms; no deciding-run interference (measurement bounds
  apply to round-45 counters).
