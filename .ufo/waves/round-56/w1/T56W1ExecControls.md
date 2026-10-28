# Round 56 wave 1 — controls harness dry run

## Scope and synthetic fixture

Ran frozen `.ufo/evidence/round-56/controls.sh` from a scratch clone based at freeze `c3e2ca9f020776b3d66c7af854fb82c834674fcf`. Constructed a synthetic content chain in `/fast/scratch/hyaku/tameshi-r56/T56W1ExecControls/synth`:

- A `28d6e631cead2c509a09ac0008cf0f21cd3e3d8a`: C2 docs/rule surfaces plus only the `## Standing rules` edit.
- B `faab54bbf29be2932d9f08b731efafe0c9137def`: 18 fake re-key entries/traces and 18 reader JSONs; each reader hash came from frozen round-18 `sectionize` over the committed `SKILL.md`.
- C / frozen-instrument PIN `55ebd9277e226e3d57e7aaf28463399849bcfe5a`: standing calibration row naming B. At C, the frozen C1 counter passed: `credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true` (`c1-at-synthetic-pin.stdout`).

Scratch-only diagnostic clone `synth-fix` changed the frozen C2 counter's SOURCES status-column index from `cells[8]` to `cells[7]`; this was solely a falsification demonstration, not a proposed production edit. At patched-counter commit `490ad84085fe2c185a78550a3b879410d80baf42`, docs became 4/4; after committing gate-acceptable own receipts at `0417763a14e359108e3cda6a5fcf5464126bcfc9`, C2 passed 14/14, all refusal codes as expected, `own=PASS`, `docs=4/4`, `total=0`.

## Harness verdicts

Frozen instruments at PIN C, exact output in `controls-frozen-pin.stdout`:

- `CONTROLS_A: 7/7 as pre-registered`.
- All five mutation controls applied: SKIP_c1 gave `rekeyed=0/18`; FAB_c1 printed `fabricated T56W2Read01.json` and gave `readers=17/18`; RESTATE printed the mutated row and gave `restate=9`; SKIP_c2 gave `selftest=13/14`; FAB_c2 gave `red54=none` because the fabricated slice was accepted.
- Both no-op controls matched their expected false verdicts.
- Phase B correctly scored C1 at the PIN it certifies, not the freeze: `CTL_POS_c1 ... rev=55ebd9277e22 ... PASS=true`; this is distinct from freeze `c3e2ca9f0207`.
- `CTL_POS_c2` was `PASS=false`, so `CONTROLS_B: 1/2 as pre-registered` (not the expected 2/2). This is caused by frozen counter defects below, not by phase B scoring the wrong revision.

With the one-token scratch-only C2 counter correction but before own receipts, phase A remained 7/7 and phase B was 1/2 (`own=own-receipts-missing`, docs 4/4), in `controls-fixedcounter-noown.stdout`. After adding a gate-acceptable own-receipt pair and running again at PIN D, output in `controls-fixedcounter-own.stdout` shows `CTL_POS_c1` and `CTL_POS_c2` both at `rev=0417763a14e3` and `CONTROLS_B: 2/2 as pre-registered`. Thus the harness's phase-B revision binding works.

## Instrument findings (frozen files were not edited)

1. **C2 docs arm has an unreachable mined-row test.** `c2/measure.py` strips the outer pipes, yielding 11 cells, then tests `cells[8] == 'mined'`. In the SOURCES schema, status is cell 7; cell 8 is `opened`. The direct probe against the synthetic valid S281 row found 114 mined rows at index 7 and zero at index 8; the cited S281 intersected index 7 only (`docs-mined-column-probe.stdout`). Frozen C2 reported `docs=3/4` at PIN C; a scratch-only `cells[7]` correction reported `docs=4/4`. Consequently the frozen counter cannot certify C2 even with the required content and all other arms satisfied. Do not treat this as a production fix by this seat; L1 should decide how to handle the frozen-instrument defect.

2. **Raw phase-A control receipt conflicts with C2's control-role gate.** `controls.sh` prints each mutation counter's `rev=` from the mutated clone HEAD. Those commits disappear when the harness exits and are absent from the lane object database. Gating raw harness stdout as `control` returned exit 3 `RECEIPT_REV_UNRESOLVABLE`; the real round-55 `control/controls-a.stdout` also returned that code (its 13bb9e5d92df, 2fd7f27ca799, and 61aaf834c377 revs are unresolvable). Evidence: `gate-control-receipts-refused.stdout`. A filtered synthetic own receipt containing only lane-resolvable rev lines passed the gate, so this is a receipt-production mismatch requiring explicit filtering/representation or an instrument decision, not proof that the arm is mathematically unreachable. The synthetic fixed-counter demonstration documents its filter in the receipt header; it is not a raw harness receipt.

3. **Needle fragility / skipped-mutation observability.** Verbatim extracted heredocs all changed their intended target in independent PIN clones; all five mutations applied (`needle-probe.json`). Variant probes (`fragility-probe.json`) show:
   - RESTATE's `startswith('| calibration |')` silently falls back to an older matching row if the new standing row is formatted `|calibration| 8 |`; it mutates the wrong row rather than failing.
   - FAB_c1's non-recursive `w[23]/*Read*.json` glob misses if all report names use lowercase `read`; the heredoc exits `no reader report found` and changes nothing.
   - SKIP_c2's literal indentation/text needle misses after either a two-space reindent or equivalent `if not paths:` rewrite (`gate needle absent`; no diff).
   - SKIP_c1 is structurally coupled to re-key paths in `traces` containing `/rekey-r56-`; when the test variant moved the marker to `reports` and emptied traces, the heredoc exited 0 but changed nothing. This also falls outside C1's own trace-path binding shape.
   - The shell has no `set -e` and does not check heredoc exit status or assert a changed target. Therefore a missed needle can flow into a verdict; if the counter is already false for another arm, a no-op mutation may still misleadingly `CTL_MATCH`.

## Ordering and harness behavior

`controls.sh` creates the supplied OUT directory but does not write receipts there; the caller must capture/split stdout. C2 reads its own receipts from the certified revision, while those receipts are outputs of the harness. A viable sequence is therefore: content PIN, run/capture controls, commit receipts at a later revision, then rerun with that later revision as PIN. The positive receipt may name the previous content PIN because the declared frozen surface is identical. In the dry run, adding only receipt files after C preserved the listed surface; patched C2 accepted the own pair.

Phase B uses a fresh `pos` clone checked out at PIN, and `run_c1`/`run_c2` obtain HEAD for `--rev`; observed positive lines named exactly PIN. This closes the specific scored-at-freeze path in the control harness.

## Receipts

All command outputs/probes cited above are under `.ufo/waves/round-56/w1/T56W1ExecControls-receipts/`:

- `controls-frozen-pin.stdout`, `controls-fixedcounter-noown.stdout`, `controls-fixedcounter-own.stdout`
- `c1-at-synthetic-pin.stdout`, `c2-fixed-counter-own-pass.stdout`
- `needle-probe.json`, `fragility-probe.json`
- `gate-control-receipts-refused.stdout`, `docs-mined-column-probe.stdout`

No tools were installed. No lane production file or frozen round-56 instrument was changed; all fixture edits/commits were in the `/fast/scratch/hyaku/tameshi-r56/T56W1ExecControls/` scratch tree. No build, lint, test, formatter, or verification suite was run.