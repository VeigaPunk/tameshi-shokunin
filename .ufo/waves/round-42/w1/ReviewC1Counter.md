# ReviewC1Counter — round 42 wave 1

Reviewer: L1Tameshi42.ReviewC1Counter (UFO-FSD). Scope: C1 counter
`.ufo/evidence/round-42/calibration/measure.py` vs contract claims (predicate,
classes, kill_rule, before_expected). No files edited; no counter run at the
lane tip (the deciding run belongs to L1).

## Mandated checks — all pass

1. **sha256 == counter_sha256.** `sha256sum .ufo/evidence/round-42/calibration/measure.py` →
   `9782a5a0e6404d2f305a51db085c7606914a2c381b35da7f7927c804df914c0e` =
   contract.json line 18 `counter_sha256`. The freeze copy is identical:
   `git show 322b5cd32b4319a05340d249ae752d12a9e6b19f:.ufo/evidence/round-42/calibration/measure.py | sha256sum` → same hash.
   Self-pin gate (measure.py:379-382) therefore passes on the canonical run.

2. **Predicate sentence == code condition == printed label.** Contract predicate
   (contract.json:16): "C1_R42_PASS is true iff self_pin=1, records=6, and m6,
   m7, m8, m10 and m11 all count 0". Code docstring (measure.py:44-45) restates
   it. Code condition (measure.py:392-393): `total = sum(count(...) for c in
   ('m6','m7','m8','m10','m11'))`; `passed = total == 0 and n_records ==
   EXPECTED_RECORDS` (EXPECTED_RECORDS=6, measure.py:75). self_pin != 1 exits 2
   before this point (measure.py:383-385), so `passed` cannot be true unless
   self_pin=1. Printed label (measure.py:394-398) derives `C1_R42_PASS` from
   `passed`. All three agree.

3. **Base receipt matches before_expected.** Contract before_expected
   (contract.json:20): "m10=1 … records=3 … C1_R42_PASS=false at the base";
   `before/c1-at-base.stdout` shows exactly `m10=1`, `records 3 of 6`, `C1_R42_PASS=false`,
   exit 1 (`c1-at-base.exit`), stderr empty. Independent rerun of the allowed base run
   `python3 .ufo/evidence/round-42/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev c77c2b7e64d2e356381441ecf94abac03e984606 --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f`
   produced byte-identical stdout and exit 1 (labelled pre-run check, not a measurement).
   `--selftest` rerun also byte-identical to `before/c1-selftest.stdout`, exit 0.

## do_nothing_control (second clause) reproduced

Contract (contract.json:23): "a scratch clone that adds the three round-42
records but no superseding receipt keeps m10=1". Reproduced in scratch clone
`/tmp/tameshi-r42-ReviewC1Counter-ctrl` (cloned `--shared`; added
`corpus/lessons/round-42.md` plus `## Round 42` section in SCORECARD.md and
`## 2026-10-25 — round 42` section in LOG.md, committed; clone deleted):
```
MISMATCH m10 .ufo/waves/round-41/residual/receipt.json asserts present=false for .ufo/waves/round-41/residual/ResidualReceipts.md; tree says true
C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=1 m11=0 total=1 records=6 sources_rows=109 rev=e0899d35… freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f C1_R42_PASS=false
exit=1
```
Also confirms the records gate fires (records=6) without masking m10.

## Findings by severity

No correctness defect found against the contract's predicate, classes, or
kill_rule. Observations below are robustness notes, not live defects.

- **Note (low): measure.py:394** prints a literal `self_pin=1` instead of the
  computed value. Only reachable when self_pin=1 (else exit 2 at :383-385), so
  the label is always accurate; cosmetic only.
- **Note (low): measure.py:166** `path_tokens` discards any backtick token
  containing `< > * { } | ( ) … , $`; a record citing such a path in backticks
  would be a silent m8 false-negative. No current record triggers it; limit of
  the line-scoped backtick extraction scheme contract C1 m8 prescribes.
- **Note (low): measure.py:230-231** m6 uses `re.search(r'(\d+) rows', …)`; a
  standing row phrased otherwise (e.g. "rows: 109") would silently pass.
  Current standing row at base (SCORECARD.md:1993) reads "109 rows" and matches
  SOURCES.md (109 rows), so no live gap.
- **Note (low): measure.py:193-196** unparseable JSON under `.ufo/waves` is
  skipped silently by m10; no such file exists at base/freeze.
- **Note (low): measure.py:207-213** supersede coverage is computed per direct
  `supersedes` edge with `theirs <= mine`; >1-hop chains work through
  `covered` set propagation (read-verified; selftest T2 covers one-hop
  junk/partial cases only). No defect found.

## Verification gaps

- Did not run the counter at the lane's current tip (forbidden other the L1's
  deciding run); tip-state claims in the round goal are outside this review.
- Did not re-run the supersede chain edge (>1 hop) empirically; judged by code
  read and the T2 selftest cases.
- m11 fleet fallback exercised only through the canonical base run (no m11
  mismatches); the fleet repo path `/home/vgpnk/Projects/shokunin` existed and
  was used during the rerun.

## Tooling

No tools installed or upgraded this session (nothing to record).
