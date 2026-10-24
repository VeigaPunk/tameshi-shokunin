# ScribeQualityCriterion — one falsifiable QUALITY criterion (round 37, w1)

Seat: scribe · Axes (godspeed): falsifiability · grounding · depth · non-duplication · lane-safety.
Scope: draft only — no edit to the live lane checkout; `corpus/QUALITY.md` untouched.
Read-only probes run: `git cat-file -e`, `git ls-tree`, `diff`, `grep` — no writes, no installs (pacman paused; none needed).

## Drafted criterion — slot 76 (next free under "## Criteria appended — round 37", corpus/QUALITY.md:858–889 already holds 73–75)

**76. Round 37.** A superseding mutation-control input is falsifiable field-by-field:
its specimen enumeration equals `git ls-tree --name-only` of the pinned source tree
byte-for-byte, and the revision it names as superseded is verified unresolvable in the
lane object database (`git cat-file -e` fails on the *manifest field*, not only on a
counter-embedded constant). A field no committed checker consumes is narration; a
control input that cannot be falsified this way is not a resolvable input.
**Captured by:** `corpus/lessons/round-37.md:16` (Mistakes row 1, class
`reference-drift`): r36 control receipts cited scratch commit
`91373d55557fe26c431e9e9dd9e8fa4a00d7b57f` — unresolvable in-lane — with no in-lane
criterion at r36 write time.
**Falsifier:** the two commands below; both can fail, both were observed this round.

## Grounding

- Mistakes row: `corpus/lessons/round-37.md:16` — reference-drift row (evidence:
  unreachable `91373d55…`; fix: committed manifest + explicit-control replay).
- Claim row: `SCORECARD.md:1802` (C1 r36 empty-panel control-input resolvability).
- Contract: `.ufo/evidence/round-37/contract.json` `C1` + `frozen_control_input`.
- Criterion 73 (corpus/QUALITY.md:860–869) covers counter revision / input-tree
  identity / `mode=control` label. Criterion 76 adds what 73 does not state:
  enumerable derivation fidelity and superseded-field liveness as mechanical checks.

## Command/output evidence (observed, live lane, read-only)

| Command | Exit | Output |
|---|---|---|
| `git -C <lane> cat-file -e 91373d55557fe26c431e9e3dd9e8fa4a00d7b57f` | 1 | (silent) — old mutant still unresolvable; this command *can fail* and did |
| `git -C <lane> cat-file -e 4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e` | 0 | — pinned source panel tree resolves |
| `diff <(git ls-tree --name-only 4f3d8af5… | sort) <(python3 -c "…manifest['source_specimens']…")` | 0 | exact 9-name equality, drift → exit 1 |
| `python3 .ufo/evidence/round-37/calibration/measure.py --lane LANE --rev d9c496b` | 1 | `unresolved_control_inputs=1 … C1_R37_PASS=false` — `.ufo/evidence/round-37/calibration/before-final-control.stdout:1` |
| `python3 .ufo/evidence/round-37/calibration/measure.py --lane LANE --rev 32826f37` | 0 | per `SCORECARD.md:1802` after cell [INFERENCE — receipt path `after-control-final.stdout` exists; line not quoted here] |

## Finding — checker-coverage split the criterion closes

- `calibration/measure.py:54-65` (`manifest_ok`) reads `source_revision`,
  `source_panel_path`, `source_panel_tree`, `source_specimen_count` (== 9),
  `expected_specimen_count` (== 0), and emptiness of the control dir. It never reads
  `source_specimens` or `prior_unreachable_mutant_revision` (grep: no hit).
- `measure.py:89-90` checks unresolvability against the hardcoded `OLD_MUTANT`
  constant, not the manifest's `prior_unreachable_mutant_revision` field — a manifest
  naming a resolvable commit as superseded would still pass the counter.
- `control/replay-empty-panel.py:81-84` is the only committed check enforcing
  specimen-set equality (`SETUP source_specimen_set_mismatch`); it lives in the
  replay adapter, not the counting predicate.
- Manifest fields: `.ufo/evidence/round-37/control/empty-panel/manifest.json:7-17`
  (`source_specimens`, 9 names), `:20` (`prior_unreachable_mutant_revision`).

## Rejected alternative (non-duplication axis)

A per-quote-form "discriminating pair" criterion for bounded `code_view` (Mistakes
row 2, `corpus/lessons/round-37.md:17`) was drafted then dropped: criterion 74
(`corpus/QUALITY.md:871-879`) already states the escaped-quote blank, literal-`#`
preserve, and branch-removal falsifier; the addition would restate it.

## Out of scope / limits

- Appending criterion 76 to `corpus/QUALITY.md` is the L1's commit decision; this
  report supplies text + evidence only.
- Mistakes rows 3 (`:18` number-drift) and 4 (`:19` attribution) already map to
  existing criteria (72/73/75); no new criterion drafted from them.
- Read-only verification; no builds/tests run (not this seat's verification job).
