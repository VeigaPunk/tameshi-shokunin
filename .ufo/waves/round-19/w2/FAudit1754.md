# FAudit1754 — falsification of build item Audit1754 (round 19 w2)

Seat `TameshiR19-2.FAudit1754`, 2026-10-21; target `w1/Audit1754.md`; frozen rev `55e1d312c4e8ac67aefad80099bd27581ff805c9`; also read `.ufo/evidence/round-19/measure.py`.
Axes: digest fidelity · argv/revision attribution · M1 assertion strength · L1 resolution. Read-only; receipt argv not executed; no suites/builds/installs.


## Strongest assertion — M1: AGREE

M1 says stdout's final `VERIFIED ... ancestor runs have the same instrument blobs ...` line is unconditional and uncomputed. Trace JSON line 33 confirms: local reads/prints/assertions only; no git/rev/ancestor logic; VERIFIED prints after nine asserts.
The ancestry claim rests on the seat note at `.ufo/waves/round-18/w3/L1Residual.md:524-526`, not the receipt. Agree with M1 and its appended-erratum/no-rewrite routing.
The digest objection below is withdrawn by Erratum 1.

## Arithmetic reproduced (observation, plain read-only ops)

stdout sha256 `e4764d51…` (6382 B, 81 LF), stderr empty `e3b0c442…`; line 1 `SECTION 1754 1804`, line 81 VERIFIED. At 55e1d312 the trio's Git blob IDs are stdout `2c27151a…`, stderr `e69de29b…`, trace `238ff14f…`.
M2 arithmetic: jq finds 17 ledger entries listing `final/checks.json`, starts {131,921,965,1021,1069,1164,1212,1436,1479,1676,1707,1754,1814,1846,1855,1905,1925}; exactly reported. Its 55e1d312 blob remains `fed3c8e6…`; §5 item 4 confirms the failed exit-64 row. The 6/15 digest-only split follows from the argv script (nine asserts; six opened/printed only).
All 15 inputs of the round-18 start=1754/read_rev=`a9c94c5…` entry match 55e1d312 blobs. Ledger is identical at worktree, 55e1d312, and master `e7039fd`; section hash `b43ed7be…` reproduces from SKILL.md 1754–1804 (1805 blank; 1806 next heading).
The report's SKILL.md `4d0190fd…` is dated to 21e7932; at 55e1d312 it is `0e3d7453…` (stale-but-dated, not a new defect).

## Audit1754's open L1 unknown — resolved by the delivered surface

The committed `current-ledger-monitor-55e1d31.json` (sha `52d6a390…`, committed at `e7039fd`) records 60/60 credited, missing 0, strict gate, no overrides, `rev_input=55e1d312`, calibration restraint 8; section 1754 credited without input drift.
At that revision per-entry `skill_sha256` remains `1334c512…`, while SKILL.md is `0e3d7453…`. Thus the delivered monitor resolves L1 empirically: whole-file skill hash does not gate coverage; calibration-8 boundary is unthreatened. Monitor is committed after the measured rev, consistent with later retention. (Behavior observed; counter source not read.)
## Concrete falsifier

M1 fails if trace JSON line 33 contains ancestor/blob computation or if the quoted seat-note passage at `L1Residual.md:524-526` does not match; both are bounded, directly checkable criteria.

## Residual unknowns

The nine asserted receipts were not independently re-opened beyond Audit1754's transcription; mtime corroboration remains weak. No resume path is in scope.

Verdict: AGREE with M1 and the no-harm conclusions; L1's delivered-tip uncertainty is resolved by the retained strict monitor.
## Erratum 1 — 2026-10-21 (my fd1a63a3 objection withdrawn)

I misread `fd1a63a3…` as a sha256; it is the Git blob OID of `tools/mutate-and-run.sh` at 921ef807, 5923d89, a9c94c5, and 55e1d312. Verified with `git rev-parse <rev>:tools/mutate-and-run.sh`; staged path shares the same OID/content. The bytes' sha256 is `d22c4025…`. Audit1754 consistently uses Git blob OIDs (e.g. stderr `e69de29b…`, Git's empty-blob OID), so its corroboration is correct. My misattribution finding and its proposed falsifier are withdrawn; M1 verdict remains AGREE.
