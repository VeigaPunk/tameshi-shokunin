# T50RevControls — round-50 control receipts vs contract

Seat: T50RevControls (reviewer, leaf). Scope: the committed control receipts at
`.ufo/evidence/round-50/control/` against `contract.json` `claims.C1.controls`, `claims.C2.controls`,
and the freeze binding. Read-only on the lane except this file and the probe receipt named below.
No tool installs (none needed). No scratch remains; the one probe clone was deleted after its
receipt was copied into w1.

## Method (commands that reproduce the checks)

- Freeze digests: `git -C <lane> show cdbf24c07f9be3a991997c25b1f1d4bb375014ae:.ufo/evidence/round-50/c1/measure.py | sha256sum` (and the c2 twin); all 14 `freeze.json` entries re-hashed against the freeze commit's bytes.
- Receipt integrity: `sha256sum` of each of the 20 control files vs `git show f87910f:<file>`; `git status --porcelain -- .ufo/evidence/round-50/`.
- Ordering: `git -C <lane> log --format='%h %ci %s' -- .ufo/evidence/round-50/control/`; `git -C <lane> log --diff-filter=A -- .ufo/waves/round-50/w1/`; start/end receipts; oldest w1 mtime.
- Term semantics: read of the frozen counters `.ufo/evidence/round-50/c1/measure.py` (460 ln) and `c2/measure.py` (558 ln) and both harnesses `control/c1-controls.py`, `control/c2-controls.py`.
- Route measurement: exact replication of the harness `fabricate()` (c1-controls.py:67-88) against freeze and against HEAD; one probe run of the frozen counter (`--explain`, scratch clone of the lane at 4afb060c1d6e994d1bbb9095493b1f6b2b8344f2, ledger committed in the clone, TMPDIR in scratch) — receipt copied to `.ufo/waves/round-50/w1/T50RevControls.probe-fab-rev.stdout`. A probe, not a verdict.

## Verified clean

1. **Freeze-bytes binding.** Every control line's `self=` equals the freeze.json sha256 prefix of its counter: c1 `ceee320c9ad8` (freeze.json:8), c2 `c3da7e59abf2` (freeze.json:12). All 14 freeze.json digests verify against the freeze commit's bytes (contract.json:7, counters:8,12, harnesses:13,14, no-harm:15, deciding:16, round-21/18/48 monitors:17-19, guard:20).
2. **Receipts are the committed bytes.** All 20 control files byte-identical to commit f87910f; the frozen code byte-identical to cdbf24c0; only untracked `integrate/` dirties the round-50 evidence tree.
3. **Ordering.** freeze cdbf24c0 18:53:35−03:00 → controls ran (c1 21:53:47Z–21:54:04Z, c2 21:53:47Z–21:54:52Z per start/end receipts) → receipts + selftests committed f87910f 18:55:58−03:00 → wave-1 dispatch 65a2215 18:59:07−03:00 → SCORECARD pre-registration 4afb060c 19:00:08−03:00. No wave-1 file has ever been committed (`--diff-filter=A` log empty) and the oldest w1 mtime (21:58:57Z) postdates the receipt commit (21:55:58Z). "Before any seat" holds.
4. **Expected-false controls false for the stated reasons** (term decode against the frozen counter):
   - CTL_0 (c1-controls.stdout:1): missing=49 + fixed_short=20 + this_round_short=5 = 74 (do-nothing).
   - CTL_OPEN (:3): open_unplanned=47 — 49 open rows minus the 2 empty-evidence rows that short-circuit to evidence_bad (c1/measure.py:206-209) before the open check (:256-258) — + evidence_bad=2 + floors = 74.
   - CTL_PLANOPEN (:4): fixed_short=20 + this_round_short=5 + evidence_bad=2 = 27 (fixed floor).
   - CTL_DECLINE (:5): declined_over=37 (49 > cap 12) + fixed_short=20 + this_round_short=5 + evidence_bad=2 = 64; generic reason is 48 chars so declined_bad=0.
   - CTL_ABSENT (c2-controls.stdout:1): shrinker_absent=1 + ok_short=19 + no_reduction=1 + records_bad=2 = 23 (no shrinker, F6 open).
   - CTL_IDENTITY (:2): minimality only — all 20 mutants (M01-M12, H01-H08) show exit0=1 valid=1 subset=1 kills=1 cost=1 reduced=1 **minimal=0** → ok=0 → ok_short=19 + no_reduction=1 = 20; runs=0 == logged=0 (cost honest).
   - CTL_REF (:3): positive control true — ok=20, units 164→43, runs==logged on every mutant, minimal=1 on all 20, total=0, exit=0.
   - Harness verdicts: c1-controls.stdout:8 `expected_false_all=true`, exit 0; c2-controls.stdout:4 `expected_false_all=true CTL_REF_exit=0`, exit 0.
5. **Selftests.** c1-selftest.stdout: 25/25 ok, exit 0; c2-selftest.stdout: 9/9 ok, exit 0. Both run `measure()` end to end on fixture repos (c1/measure.py:324ff; c2/measure.py:430ff, four fixture shrinkers) — the round-49 mistake named in `frontier_step.mistake` is addressed in the receipts.
6. **Hidden-panel hygiene.** c2 receipts print mutant ids only (M01-M12, H01-H08); no mutant names or edits appear in any c2-*.stdout; `unfound=0` in all three — the frozen generator found all 20 mutants at freeze bytes, consistent with the custody note.

## Findings

### H1 — The after-base floor (fixed_after_base_min=5) is already spuriously meetable at HEAD (observed)
Probe (frozen counter `self=ceee320c9ad8`, scratch clone at 4afb060c, receipt
`.ufo/waves/round-50/w1/T50RevControls.probe-fab-rev.stdout`): a hand-written ledger whose only
fixed rows cite post-base commits scores `fixed=8 fixed_this_round=8 fixed_bad=0
this_round_short=0` — the floor of 5 met with **zero real fixes**. The 8 rows:
R49.1, R49.2 → commit cdbf24c0 citing `.ufo/evidence/round-50/c2/measure.py:10,65`;
R49.4, R49.6 → commit 4afb060c citing `SCORECARD.md:2423`;
R42.3, R45.2, R45.3, R48.1 → commit 4afb060c citing `.ufo/evidence/round-50/before/no-harm-at-base.stdout:2,3,10`.
Mechanism: the C1 counter's HARD list (c1/measure.py:59-60) excludes only `c1/`, `control/`,
contract.json, freeze.json — the **c2 instrument and the `before/` receipts are allowed evidence
paths**; a path absent at `routed_at` counts as fresh (c1/measure.py:241-243) and any fixed commit
not an ancestor of base counts as this-round (:254-255). Consequence: at REV the floor cannot
distinguish fabricated from genuine this-round fixes; the pre-registered mitigation (wave-2
semantic attack per row, closure sampling) is the only defense, and the closure must not cite the
floor as evidence that fixes are genuine.

### H2 — At HEAD, R40.2 and R41.7 are unsatisfiable: C1_R50_PASS is unreachable at HEAD regardless of every other row
`git -C <lane> grep -l -F -i -e <key> HEAD` shows their keys occur only in excluded places:
'wave-slots'/'settlement-receipt.json'/'grant pointer' (R40.2) and 'SOURCES.md:436'/'436-437'/
'bullet list' (R41.7) appear only in the spot-check files (excluded), the round-50 c1 instruments
(HARD), and `.ufo/waves/…` files whose paths end with none of the keys (soft-excluded,
c1/measure.py:130-131). Any ledger row for them therefore fails: empty evidence → evidence_bad
(c1/measure.py:206-209); non-empty → excluded/soft-excluded/path-absent (:128-131,145). Observed
in all four c1 controls as `evidence_bad=2` with `EXPLAIN evidence-empty R40.2/R41.7`
(c1-CTL_FAB.stdout:1-2). So the claim can pass at final REV **only if** new allowed prose carries
one of those keys (e.g. corpus/lessons/round-50.md mentioning 'wave-slots' or 'bullet list', or a
wave-report path ending in a key) — which is simultaneously what makes them fabricatable (H1).
The counter's last barrier and its satisfiability requirement are the same lever; the L1 and the
integration seat need to know this before writing round-50 prose.

### M1 — Contract prose deviates from the CTL_FAB receipt
contract.json `cannot_see`: "reaches fixed=38 with every other term green except the after-base
floor"; `controls.CTL_FAB`: "expected false at freeze only through the after-base floor".
Observed (c1-controls.stdout:7): fixed=**40**, evidence_bad=**2**, this_round_short=3, total=5 —
false through **two** terms. Root causes are H1 (the freeze commit's own c2/measure.py is citable,
+2 fixed) and H2 (2 items with no keyed line anywhere). The blind-spot demonstration itself
stands: `fixed_bad=0` over 40 fabricated rows — the counter found no defect in any of them.

### M2 — The CTL_FAB route grows at REV (measured)
Exact `fabricate()` replication (c1-controls.py:67-88): at freeze 40/49 fabricatable, 2 post-base;
at HEAD (4afb060c) **42/49, 4 post-base** — R49.4 and R49.6 newly fabricatable via 4afb060c's
`SCORECARD.md:2423` (the round-50 standing calibration row; verified absent at freeze). Still
unfabricatable at HEAD: R40.2, R41.7, R44.2, R47.5, R48.4, R49.3, R49.5 — and one new keyed line
converts several at once ('brace_depth_at' → R47.5+R48.4+R49.5; 'wave shape' → R44.2;
'wave-slots'/'bullet list' → R40.2/R41.7). Every later post-base commit adding keyed non-ack lines
in allowed paths (tools/shrink-case.py will contain 'pbt-staged-id.py'; lessons; knowledge
entries) grows the route further.

### L1 — C2 term semantics: `no_reduction` is a 0/1 flag, not a per-mutant count
c2/measure.py:312-317: `ok_short = max(0, N-1-ok)` (N when the shrinker is absent);
`no_reduction = 0 iff ok and after_sum < before_sum` (1 when absent). The receipts'
`no_reduction=1` on CTL_ABSENT/CTL_IDENTITY is that flag. Also note CTL_REF is the counter's own
`REF_SHRINKER` (c2/measure.py:375) with MODE→pass/LIE→0 (c2-controls.py:57) — circular by design
and pre-registered as such ("it shows the counter can pass").

### L2 — Contract C1 "before" wording
contract.json says "at base: no ledger, missing=49 … (CTL_0 receipt)" but CTL_0 measured the
freeze tree (rev=cdbf24c0, c1-controls.stdout:1), not base. Substance holds (no ledger at either
revision); wording nit for the closure note.

### L3 — Selftest receipts carry no embedded digest
c1-selftest.stdout / c2-selftest.stdout end `cases=25 failed=0` / `cases=9 failed=0` with no
`self=` line binding them to the freeze bytes; the binding holds only via commit f87910f, whose
tree I verified byte-equal to all 14 freeze.json digests. Fine in context; the closure should cite
the commit, not the file alone, when referencing the selftests.

## Residual risk and verification gaps

- The deciding run at REV: after the round prose needed for H2 lands, a fully fabricated ledger can
  reach total=0 (all floors met spuriously; floor met probe-observed). Defense is wave-2 semantic
  attack per row + closure sampling; fixed rows citing cdbf24c0/`.ufo/evidence/round-50/c2/measure.py`,
  4afb060c/`SCORECARD.md:2423`, or 4afb060c/`.ufo/evidence/round-50/before/no-harm-at-base.stdout`
  should be treated as presumptively spurious.
- I did not re-run the c1/c2 harnesses (their scratch receipts are the committed observations;
  re-running would require the hidden panel, which I must not read). The fabricate() replication
  and the probe used public data only.
- The probe is a probe, not a verdict: it shows what the frozen counter does with a hand-written
  ledger at HEAD; the deciding run's ledger is a different artifact.

## Summary

- All controls ran at freeze bytes: `self=` digests match freeze.json prefixes; all 14 freeze digests verify; receipts byte-identical to commit f87910f; ordering (freeze → controls → receipts → dispatch) holds; no wave-1 file committed.
- Expected-false controls false for their stated reasons (term-level decoded); CTL_REF positive control true (ok=20, 164→43 units, cost honest); selftests 25/25 and 9/9, exit 0, both reaching measure() end to end.
- CTL_FAB's fixed_this_round=2 cites the freeze commit itself via `.ufo/evidence/round-50/c2/measure.py:10,65` (R49.1/R49.2) — the C1 HARD list does not exclude the c2 instrument.
- Route grows at REV: 4 post-base fabricatable citations at HEAD (added R49.4/R49.6 via SCORECARD.md:2423); probe shows 8 hand-written post-base rows credit as this-round fixes (fixed_bad=0), meeting the floor of 5 spuriously.
- R40.2/R41.7 have no keyed line in any allowed path at HEAD — C1 is unsatisfiable at HEAD; it passes at REV only if new prose names their keys, which also makes them fabricatable.
- Contract prose (fixed=38, "only through the after-base floor") deviates from the receipt (fixed=40, also evidence_bad=2); blind-spot demonstration (fixed_bad=0 over 40 fabricated rows) stands.
- Residual: after H2's prose lands, a fully fabricated ledger can reach total=0; wave-2 semantic attack is the only defense. No tool installs; scratch deleted.
