# T57W3RevControlsDry — controls and deciding-run dry review

Axes: operability, control-arm fidelity, revision identity, lane isolation.

## Findings (severity order)

1. **P1 acceptance blocker, not a newly introduced harness defect:** current master `2c51affd37e15cd7cd258d76ba0f5f73ff235924` plus the dry-c1 working-tree overlay has only the 49 original ledger rows. `CTL_POS_c1` prints `rows=0/51`, `missing=51`, `this_round_short=6`, `panel_over=46`, `panel_prov=0`, total 103, false. C2 positive is true. Master identifies itself in checkout output as the round-57 honest-stop commit; this run does not overturn that stop or claim calibration success.
2. **P2 operability:** `controls.sh` returns **0** despite `CTL_MISMATCH CTL_POS_c1` and `CONTROLS_B: 1/2`. Lines 177–179 end with an unconditional summary echo. Proposed change: after both summaries, return nonzero unless both phase numerators equal their denominators. `deciding-run.sh:146–153` separately parses receipt contents, so this is not evidence that deciding-run accepts the failed control set. No source or staged implementation edits made (review-only seat).

## Executed commands and every CTL result

Reproducer: `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RevControlsDry-receipts/run.py`.
Exact subprocess argv, stdout, stderr, and exit codes: `T57W3RevControlsDry-receipts/run4/commands.json`.
The controls invocation was:

```text
bash /fast/scratch/hyaku/tameshi-r57/T57W3RevControlsDry/clone/.ufo/evidence/round-57/controls.sh /fast/scratch/hyaku/tameshi-r57/T57W3RevControlsDry/clone 5e3569969b532310d2b8a3d130901757a3df356b 332becb09a962561377e922ce13d835766087c30 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RevControlsDry-receipts/run4/controls
```

Working instruments, SCORECARD, and ledger were copied into a scratch clone detached at current master, then committed under the fixture identity. The scratch child revision, **not master itself**, is what controls grade, as required to make the uncommitted overlay visible to clone-based counters. Real panel.json now exists: its 51 verdicts and detail commits were retained (22 fixed, 27 open, 2 declined). Only provenance was replaced by an explicitly synthetic report and results file, committed in scratch and digest-pinned; PANEL_SHA256 was pinned to the scratch panel. No ledger statuses were invented or repaired. This certifies harness execution, not the real panel or lane content.

```text
# controls: one generation; recomputed from lane git objects, no committed receipt read
# LANE=/fast/scratch/hyaku/tameshi-r57/T57W3RevControlsDry/clone BASE=5e3569969b532310d2b8a3d130901757a3df356b REV=332becb09a962561377e922ce13d835766087c30
# phase A: do-nothing and mutation controls (expected false)
CTL CTL_0_c1 C1_R57: self=8e64704229ff clone_rev=c0949e6873e1 rows=0/51 agree=0/51 old49=ok fixed=0 declined=0 thisround=0 panel=51/5 spot=ok total=154 C1_R57_PASS=false
CTL_MATCH CTL_0_c1 expected=false actual=false counter_exit=1
CTL_ARM CTL_0_c1 missing=51
CTL CTL_0_c2 C2_R57: self=a5138acb2248 clone_rev=c0949e6873e1 gate_rows=0 exits=none held=0/0 mutants=0/3 skill_row=0 codes_known=4/4 standing_cell=WRONG:RECEIPT_REV_MISMATCH total=11 C2_R57_PASS=false
CTL_MATCH CTL_0_c2 expected=false actual=false counter_exit=1
CTL_GEN CTL_SKIP_c1 {"kept_rows": 49, "mode": "skip", "new_rows": 51, "panel_agree": 2, "panel_present": true, "reason_len": 45, "unkeyed": 0}
CTL CTL_SKIP_c1 C1_R57: self=8e64704229ff clone_rev=fcd326804a2d rows=51/51 agree=51/51 old49=ok fixed=0 declined=51 thisround=0 panel=49/5 spot=ok total=50 C1_R57_PASS=false
CTL_MATCH CTL_SKIP_c1 expected=false actual=false counter_exit=1
CTL_ARM CTL_SKIP_c1 panel_over=44
CTL_GEN CTL_FAB_c1 {"kept_rows": 49, "mode": "fab", "new_rows": 51, "panel_agree": 29, "panel_present": true, "unkeyed": 0}
CTL CTL_FAB_c1 C1_R57: self=8e64704229ff clone_rev=aadc7730a943 rows=51/51 agree=0/51 old49=ok fixed=51 declined=0 thisround=0 panel=22/5 spot=ok total=74 C1_R57_PASS=false
CTL_MATCH CTL_FAB_c1 expected=false actual=false counter_exit=1
CTL_ARM CTL_FAB_c1 evidence_bad=51
CTL_GEN CTL_OPEN_c1 {"kept_rows": 49, "mode": "open", "new_rows": 51, "panel_agree": 29, "panel_present": true, "planned_ids_blanked": 0, "unkeyed": 0}
CTL CTL_OPEN_c1 C1_R57: self=8e64704229ff clone_rev=f1524a00bca9 rows=51/51 agree=0/51 old49=ok fixed=0 declined=0 thisround=0 panel=22/5 spot=ok total=74 C1_R57_PASS=false
CTL_MATCH CTL_OPEN_c1 expected=false actual=false counter_exit=1
CTL_ARM CTL_OPEN_c1 open_unplanned=51
CTL_GEN CTL_BULKOPEN_c1 {"kept_rows": 49, "mode": "bulkopen", "new_rows": 51, "panel_agree": 27, "panel_present": true, "planned_ids_named": 51, "unkeyed": 0}
CTL CTL_BULKOPEN_c1 C1_R57: self=8e64704229ff clone_rev=e86b99e4e6bd rows=51/51 agree=51/51 old49=ok fixed=0 declined=0 thisround=0 panel=24/5 spot=ok total=25 C1_R57_PASS=false
CTL_MATCH CTL_BULKOPEN_c1 expected=false actual=false counter_exit=1
CTL_ARM CTL_BULKOPEN_c1 panel_over=19
CTL_GEN CTL_QUOTE_c1 {"file": "corpus/ctl-quote-housekeeping.md", "lines": 51, "mode": "quote-file", "unkeyed": 0}
CTL_GEN CTL_QUOTE_c1 {"commit": "b349ff7f000c7bdfc6730dc8d9f75cdc1165996a", "kept_rows": 49, "mode": "quote", "new_rows": 51, "panel_agree": 29, "panel_present": true, "unkeyed": 0}
CTL CTL_QUOTE_c1 C1_R57: self=8e64704229ff clone_rev=3772624aeb81 rows=51/51 agree=0/51 old49=ok fixed=51 declined=0 thisround=0 panel=22/5 spot=ok total=74 C1_R57_PASS=false
CTL_MATCH CTL_QUOTE_c1 expected=false actual=false counter_exit=1
CTL_ARM CTL_QUOTE_c1 fixed_bad=51
CTL_GEN CTL_SKIP_c2 {"drift_path": "LOG.md", "gate_rows_removed": 3, "mode": "skip", "rows_added": 3}
CTL CTL_SKIP_c2 C2_R57: self=a5138acb2248 clone_rev=47b9c4d2cbca gate_rows=3 exits=0,2,3 held=0/3 mutants=0/3 skill_row=1 codes_known=4/4 standing_cell=ok total=7 C2_R57_PASS=false
CTL_MATCH CTL_SKIP_c2 expected=false actual=false counter_exit=1
CTL_GEN CTL_FAB_c2 {"drift_path": "LOG.md", "gate_rows_removed": 3, "mode": "fab", "rows_added": 3}
CTL CTL_FAB_c2 C2_R57: self=a5138acb2248 clone_rev=7b2fe23aa415 gate_rows=3 exits=0,2,3 held=1/3 mutants=1/3 skill_row=1 codes_known=4/4 standing_cell=ok total=4 C2_R57_PASS=false
CTL_MATCH CTL_FAB_c2 expected=false actual=false counter_exit=1
CTL_GEN CTL_MUT_c2 {"drift_path": "LOG.md", "gate_rows_removed": 3, "mode": "mut", "rows_added": 3}
CTL CTL_MUT_c2 C2_R57: self=a5138acb2248 clone_rev=a271af245f35 gate_rows=3 exits=0,2,3 held=3/3 mutants=1/3 skill_row=1 codes_known=4/4 standing_cell=ok total=2 C2_R57_PASS=false
CTL_MATCH CTL_MUT_c2 expected=false actual=false counter_exit=1
CONTROLS_A: 10/10 as pre-registered
# phase B: the positive controls scored at the revision they certify (REV=332becb09a962561377e922ce13d835766087c30)
CTL CTL_POS_c1 C1_R57: self=8e64704229ff rev=332becb09a96 rows=0/51 agree=0/51 old49=ok fixed=0 declined=0 thisround=0 panel=51/5 spot=ok total=103 C1_R57_PASS=false
CTL_MISMATCH CTL_POS_c1 expected=true actual=false counter_exit=1
CTL CTL_POS_c2 C2_R57: self=a5138acb2248 rev=332becb09a96 gate_rows=3 exits=0,2,3 held=3/3 mutants=3/3 skill_row=1 codes_known=4/4 standing_cell=ok total=0 C2_R57_PASS=true
CTL_MATCH CTL_POS_c2 expected=true actual=true counter_exit=0
CONTROLS_B: 1/2 as pre-registered
controls.sh process exit=0
```

All 10 negative controls trip their named arms; 11/12 expected booleans match. The sole mismatch is positive C1 because of the missing rows. No CTL_ARM_MISMATCH. Per-control full outputs are under `T57W3RevControlsDry-receipts/run4/controls/`.

## Deciding-run refusal matrix

Each invocation uses the same overlay clone with a fresh empty in-clone OUTDIR. Exact argv is in commands.json. All three exit **3**, and each OUTDIR remains `[]` (receipts `*.outdir.json`).

### missing-freeze

```text
DECIDING_REFUSED counter-missing .ufo/evidence/round-57/freeze.json
```

### rev-not-head

```text
DECIDING_REFUSED rev-is-not-head-of-fresh-clone rev=2c51affd37e15cd7cd258d76ba0f5f73ff235924 head=332becb09a962561377e922ce13d835766087c30
```

### missing-panel-pin

```text
FREEZE_INTEGRITY: OK files=19 amendments=0 freeze=5fce29523aa2
DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-57/control/controls-a.stdout
```

There is **no dedicated missing-panel-pin preflight refusal** in deciding-run. After supplying a synthetic integrity-valid freeze (19 digests, first manifest commit, amendments=[] mirrored into contract), restoring the original pending pin reaches the missing-controls-receipt refusal shown above. A separate counter invocation in `missing-panel-pin-counter.stdout` confirms `EXPLAIN panel-pin ...`, `panel_pin=1`, `C1_R57_PASS=false` (exit 1). Do not describe that as an exercised `DECIDING_REFUSED panel-pin` path: no such string was emitted. Freeze and head refusals are canonical deciding-run lines 55 and 60–64; pin rejection is canonical C1 measure.py lines 421–447. No controls receipt was fabricated to bypass these gates.

## Residual risk and verification gaps

- Deciding-run did not reach counters/no-harm/census/final gate; no successful certification is asserted. The real missing freeze/receipts remain prerequisites.
- Real-panel provenance and the 64/64 cold-read obligation remain unverified by this dry run. Synthetic provenance is expressly not independent evidence.
- Three preliminary attempts remain preserved: initial empty-panel run; run2 missing synthetic results provenance; run3 fixture staging failure. Only run4 supports the final tallies. The runner's terminal JSON key `controls_exit` accidentally reports the last counter exit (1); authoritative controls process exit is **0**, captured in commands.json and controls.exit.
- LSP device unavailable (`xd://lsp`: No such tool), so definition/caller inspection used text, not semantic LSP proof. The reviewed diff adds both harness files relative to BASE.
- Scratch was removed after the completed run. No lane/fleet git mutations, runtime dispatch, installations, judgment/admission, or edits outside assigned report/receipts paths.

Self-evaluation: accuracy 4 (all claims have raw receipts, synthetic provenance limits inference); completeness 4 (all requested refusals attempted; no pin-specific path exists); clarity 4 (authoritative run distinguished from preliminary fixtures); actionability 4 (exit-status fix and content blocker identified, no implementation mutation); conciseness 4 (full CTL transcript retained because explicitly required). Overall 4.0. Improvement: re-execute certification only after the real freeze, pin, ledger and control receipts exist; no current pass is claimed.
