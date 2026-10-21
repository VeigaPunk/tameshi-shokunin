# FRoute05 — scoped falsification (2026-10-21)

- Axis: C1 CALIBRATION only; no score or promotion claim.
- Strongest assertion: R18-5 was missing same-revision evidence at round-18 close; later replay repairs evidence, not timeliness. **Agree** with this factual attribution. The correction is present and properly scoped in the delivered lesson.
- Finding — **MEDIUM, ruler coverage**: the delivered C1 ruler does not implement all of Route05's proposed failure-capable predicate: it never checks the historical fleet-report blob that predicate item 1 requires.

## Evidence

- Route05 `w1/Route05.md:23-32` requires both the historical report blob and delivered lesson blob from committed trees. Primary spot-check `corpus/lessons/round-18-verifier-spotcheck.md:201-204` names the final-tip claim at `4b7c682…` and receipt at `a85f710…`.
- Re-opened fleet report at its cited commit `a85e4d87…`, `.ufo/reports/round-18/tameshi.md:53,77`: it states 60/60, restraint 8 at the final `4b7c682…` tip. Lane receipt `.ufo/evidence/round-18/final/measure-final-60.json` at `4b7c682…` instead has `revision == rev_input == a85f710…` (the exact blob SHA-256 matches the delivered tree).
- Later replay receipt `.ufo/evidence/round-19/round18-final-measure.json` binds argv `python3 .ufo/evidence/round-18/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 4b7c6823a462f5ea2eafcb262275300a545f3ed7 --explain`, revision `4b7c682…`, exit 0, and stdout/stderr SHA-256 `55c530…0ae8` / `e3b0…b855`; those hashes match the delivered output blobs. Parsed stdout: `revision == rev_input == 4b7c682…`, `sections_covered == sections_total == 60` (60/60), `calibration_restraint_score == 8`, overrides false. The instrument record pins the receipt and original round-18 measure SHA (`7ca87a…dd37`), matching that tool blob at `4b7c682…`.
- Delivered `corpus/lessons/round-18.md:148-155` contains R18-5 and says “This repairs missing evidence, not its original timeliness” (2026-10-21); it also disclaims 60/60 for later round-19 revisions. No stale/missing prose correction found.
- `measure.py` at requested revision `55e1d312…` is byte-identical to the reviewed file (SHA-256 `bb651e…5053`). Its `PATHS` (`:46-51`) omit the fleet report and its CLI accepts one lane `--repo/--rev` (`:367-403`); `measurement()` checks the lane lesson, replay receipt and instrument (`:200-222`) only. It therefore cannot assert predicate item 1's historical-report half.

## Concrete falsifier and residuals

- Falsifier to the delivered ruler's completeness: keep every `measure.py` `PATHS` input unchanged but remove or alter the external fleet report. By the inspected input list and `measurement()` predicate, R18-5 still counts corrected. This is a source-derived counterexample, not an executed mutation.
- Residual: L1 may separately verify the fleet-tree predicate; that verification is outside this review. Receipt hashes/argv establish recorded attribution, not arbitrary historical execution authenticity. No lane selftest or measurement was run. `xd://lsp` is unavailable here (no LSP status/references/diagnostics device), so this is direct source inspection, not semantic-server proof.