Round-73 rehearsal receipts (built and scored BEFORE the plan's freeze).

reh-c1-controls.txt
  The three cheapest controls that skip C1's claimed work, scored with the
  frozen counter. Driver: c1-control-stub.py (this dir). Modes: always-meet,
  echo-printed, green-only. Target line: WAVE_RECONCILE: rows=6 met=6
  unexpected=0. Measured: rows=6 met=4 unexpected=2 exit 1 (always-meet and
  echo-printed); rows=4 met=4 unexpected=0 exit 0 (green-only, refuted by the
  frozen row count).

reh-c2-m3-six-arms.txt
  C2's before-state: the IGNORED-filter mutant M3 (the three-line
  `IGNORED = frozenset((SKILL, '.ufo/evidence/round-17/coldread/ledger.json',
  LEDGER))` block replaced by `IGNORED = frozenset()`, old-string count
  asserted == 1) run against the six recorded live arms. Every arm reads the
  same at_risk under pristine and mutant: KILLING_ARMS=0/6.

reh-c2-m3-battery.txt
  C2's after-state: the same 7-arm battery under the same M3 pair. Pristine
  reads REKEY_ARMS: arms=7 meet=7 unexpected=0 exit 0; the mutant reads
  ARM_UNEXPECTED ignored-skill expected=0 measured=9 and
  REKEY_ARMS: arms=7 meet=6 unexpected=1 exit 1.

Mutant bytes: pristine sha256 85ca2b69d723871d41dfc17307131d81262c1a8404e140f6ab4b461543bd88f4,
M3 sha256 7e0fdf623f6693b0414983c48c0fea62086618e63460e1c88f54ef63781db844.
