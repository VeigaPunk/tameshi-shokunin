# ExecMeasureBase — round-44 w1 base measurements

Seat: L1Tameshi44.ExecMeasureBase
Date: 2026-10-25
Milestone: base measurements (judged on: calibration)
Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin
Base rev measured: `506e99c7b73c85711f066895984d501fcf7539cd`
Contract read: `.ufo/evidence/round-44/contract.json` (read-only; not edited).
No files changed in the lane. No tool installs performed (no tooling needed; all four commands ran with stock python3/git).

Receipts are saved verbatim (stdout + exit code) under `/tmp/tameshi-r44-ExecMeasureBase-/`:
- `c1_round44_count_at_base.stdout`
- `c2_old_round43_at_base.stdout`
- `commandD_depth_at_base.stdout`
- `coldread_monitor_at_base.stdout`

## 1. C1 — round-44 calibration counter at base

Command:
```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-44/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 506e99c7b73c85711f066895984d501fcf7539cd --freeze ba01973c73ad7de60e5bd19ae08255a1b7ef917e
```
Output (verbatim), exit code 1:
```
C2_R44: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=1 m13=0 total=1 records=4 sources_rows=114 standing=114 receipts=17 revisions=4 m13_probe=standing=7_column0=113_valid=114 rev=506e99c7b73c85711f066895984d501fcf7539cd freeze=ba01973c73ad7de60e5bd19ae08255a1b7ef917e C2_R44_PASS=false first=m12:newest_block_is_round_43,_the_contract_round_is_44
EXIT_CODE=1
```
Notes: at base the newest SCORECARD block is round 43, so m12 flags (`newest_block_is_round_43,_the_contract_round_is_44`); all other classes are clean including m7=0 (the value-vs-citation grammar masks the `safe_floor=S256` assignment value — the round-43 false alarm is gone). `self_pin=1` (running counter sha matches the freeze's pinned `counter_sha256` c0c6199f…).

## 2. C2 control — old round-43 counter at the same rev

Command:
```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-43/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 506e99c7b73c85711f066895984d501fcf7539cd --freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685
```
Output (verbatim), exit code 1:
```
C2_R43: self_pin=1 classes=7 m6=0 m7=1 m8=0 m10=0 m11=0 m12=0 m13=0 total=1 records=4 sources_rows=114 standing=114 receipts=17 revisions=4 m13_probe=standing=7_column0=113_valid=114 rev=506e99c7b73c85711f066895984d501fcf7539cd freeze=6b83a11c61f0fad1074ec1f2a4c38a2fd7034685 C2_R43_PASS=false first=m7:SCORECARD.md#round-43_unknown_S256
EXIT_CODE=1
```
This reproduces the contract's `do_nothing_control` claim exactly: old counter at base prints `m7=1 total=1 first=m7:SCORECARD.md#round-43_unknown_S256 C2_R43_PASS=false`.

## 3. Command D — depth at base

Command:
```
git show 506e99c7b73c85711f066895984d501fcf7539cd:tools/mutate-and-run.sh | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
```
Output (verbatim), git exit code 0:
```
recorded_cases=9 depth_score=9
EXIT_CODE=0
```

## 4. Calibration monitor — round-21 coldread at base

Command:
```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 506e99c7b73c85711f066895984d501fcf7539cd
```
Output: JSON (verbatim, saved at `coldread_monitor_at_base.stdout`, 242 KB incl. `external_inputs` hashes). Key fields, exit code 0:
```json
{
  "calibration_restraint_score": 6,
  "coldread": { "sections_covered": 60, "sections_total": 64, "box3_full_page": false },
  "ledger_source": "rev",
  "overrides_used": false,
  "recorded_cases": 9,
  "rev_input": "506e99c7b73c85711f066895984d501fcf7539cd",
  "revision": "506e99c7b73c85711f066895984d501fcf7539cd",
  "trace_gate": "strict",
  "sources": { "status": { "mined": 86, "queued": 22, "rejected": 6 }, "tiers": { "A": 102, "B": 9, "C": 3 } }
}
EXIT_CODE=0
```

## Findings

- C1 at base: `self_pin=1 classes=7 total=1` → `C2_R44_PASS=false`, sole hit `m12` (newest block is round 43, contract round is 44). This is the expected pre-landing state: the round-44 block does not exist yet at base. m7 already clean at base (grammar fix live: `safe_floor=S256` masked as a value).
- Old counter control at base: `m7=1 total=1 first=m7:SCORECARD.md#round-43_unknown_S256 C2_R43_PASS=false` — matches contract `do_nothing_control`.
- Depth at base: `recorded_cases=9 depth_score=9` (exit 0).
- Coldread monitor at base: `calibration_restraint_score=6`, `sections_covered=60/64`, `overrides_used=false`, `trace_gate=strict`, exit 0.

## Risks / blockers

- None for the measurement milestone; the L1's single deciding run must be executed at the landing revision with the contract's counting commands. No counter was run against any other revision.
- Scratch dir `/tmp/tameshi-r44-ExecMeasureBase-/` holds the four receipts (item-mandated; not deleted).
