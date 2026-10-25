# ReplayC1: round 42, wave 2 (FALSIFY)

Seat: L1Tameshi42.ReplayC1. Judged on: calibration. Accessed 2026-10-25.
Attacked thing: the C1 receipts written in wave 1, and the claim that the integration tip clears m10.
Counter: `.ufo/evidence/round-42/calibration/measure.py`, sha256 `9782a5a0e6404d2f305a51db085c7606914a2c381b35da7f7927c804df914c0e`.
Scratch output: `/tmp/tameshi-r42w2-ReplayC1-out/` (deleted before return). No lane writes except this file. Tools installed: none.

Common prefix: `L=/home/vgpnk/Projects/shokunin/tameshi-shokunin; F=322b5cd32b4319a05340d249ae752d12a9e6b19f`.

## Findings

1. **The base receipt replays exactly.**
   `python3 $L/.ufo/evidence/round-42/calibration/measure.py --lane $L --rev c77c2b7e64d2e356381441ecf94abac03e984606 --freeze $F` exits with rc=1, which matches `before/c1-at-base.exit` (`1`).
   `diff before/c1-at-base.stdout <replay>` and `diff before/c1-at-base.stderr <replay>` both produce empty output, so stdout and stderr are identical. The replayed stdout:
   - `MISMATCH m10 .ufo/waves/round-41/residual/receipt.json asserts present=false for .ufo/waves/round-41/residual/ResidualReceipts.md; tree says true`
   - `MISMATCH records 3 of 6 round-41/42 records present`
   - `C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=1 m11=0 total=1 records=3 sources_rows=109 rev=c77c2b7e… C1_R42_PASS=false`

2. **The selftest receipt replays exactly.**
   `python3 $L/.ufo/evidence/round-42/calibration/measure.py --selftest` exits with rc=0, which matches `before/c1-selftest.exit` (`0`).
   `diff before/c1-selftest.stdout <replay>` produces empty output. The summary line is `C1_R42_SELFTEST: cases=9 failed=0`. The nine cases include `T2_superseded_clears`, `T2_junk_supersede_still_counts` and `T2_partial_supersede_still_counts` (measure.py:305-315).

3. **The 5f739acf pre-run receipt replays exactly.**
   `python3 $L/.ufo/evidence/round-42/calibration/measure.py --lane $L --rev 5f739acf21e878e22bd3f66249ae8bec2aaf1fc1 --freeze $F` exits with rc=1, which matches `prerun/c1-at-5f739acf.exit` (`1`).
   `diff prerun/c1-at-5f739acf.stdout <replay>` produces empty output. At this revision m10 was already 0, but m7 was 1: `MISMATCH m7 S159 cited but absent from the registry`.
   The source of the m7 hit is a bare `S159` at `5f739acf:corpus/lessons/round-42.md:71-72`. In the tip, the same passage reads `staged:S159` (`a21845f:corpus/lessons/round-42.md:72`, commit `a21845f round-42: lesson guard-proof wording (pre-run m7 finding)`).

4. **Pre-run at the integration tip a21845f: m10 is 0 and no mismatch is left.**
   `python3 $L/.ufo/evidence/round-42/calibration/measure.py --lane $L --rev a21845f523b75adbd3e3f7a62af91294db224ad9 --freeze $F` exits with rc=0 and empty stderr. Its entire stdout is one line, with no `MISMATCH` lines:
   `C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=0 m11=0 total=0 records=6 sources_rows=113 rev=a21845f523b75adbd3e3f7a62af91294db224ad9 freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f C1_R42_PASS=true`
   The supersede repair `.ufo/waves/round-42/supersede/round-41-residual-receipt.json` is in the tree at a21845f (`git ls-tree`). That is consistent with m10 falling from 1 at base to 0 here. The counter only clears m10 when the supersede document covers every seat and is not junk (measure.py:39, 199; selftest T2_*).

## Residual risk and verification gaps

- This is a pre-run, not the deciding run. The L1's default-mode run is still the one that counts.
- `calibration/__pycache__/measure.cpython-314.pyc` (06:28:27 -0300) predates this seat's runs and was not created by it.
- I did not check the supersede JSON's own contents against the tree; that belongs to the ReviewSupersede seat.

Verdict: SURVIVES
