## Replay43 — `wave-accounting-wrong-count-entry`

Report: `.ufo/waves/round-23/w2/Replay43.md`

**Axes:** argv identity · exit/stdout binding · defect semantics · evidence vs inference · no producer auth

**Evidence:** Present in `replay/bundle.json` and `replay/observations.json` (full stdout, not tails only); `496d212` clone execution; bundle receipt stdout equals observations.

**Static binding:** Confirmed — frozen argv/expect matches `28cae179` baseline, `requirements.json`, and `registry-baseline.json`; replay `got=1`, `held=true`; whole replay bundle passes `command-binding.py` (exit 0).

**False acceptance:** Frozen `stdout_contains` pins `TOTAL_MISMATCH` plus aggregate `"total"` literals `"completed": 66` and `"dead": 80`, not wave2’s claimed 40/35 vs observed 38/37. Adversarial receipt copies still pass `command-binding.evaluate()` if finding `"wave": "wave2"` → `"wave1"` or detail claimed counts are tampered, as long as exit 1 and total block literals remain. Substring note: needle `TOTAL_MISMATCH` matches inside `TOTAL_MISMATCH_X`.

**Rejected:** Producer authentication, source-read as execution credit, historical metadata retrofill.

**Calibration:** Structural binding is exact; stdout token policy over-accepts relative to the wrong-count fixture intent. No tooling installs.
