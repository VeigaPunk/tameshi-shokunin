# Round-25 C1 item R2 — receipted re-run of the guard sweep on tools/command-binding.py.
# Suite: c1-suite.py selftest "$MUTANT" (the gate's own public selftest, staged privately).
# One guard disabled per defect. G1-G8: frozen before the wave. Contract amendment 2 (before any after
# measurement) adds G9-G14 so every one of round 23's ten guard anchors (.ufo/evidence/round-23/mutate.py:13-22)
# is re-run verbatim: G1-G4 already were (argv, cwd, revision, exit); G12-G14 are round 23's stdout,
# membership and duplicate-command anchors, G9-G11 its bool-exit, snapshot-pin and empty-requirements.
# G5-G7 stay as additional finding-drop variants; G8 (duplicate-requirement) is lane-added.
@defect G1 | argv guard disabled
@old if receipt['argv'] != required['argv']:
@new if False:

@defect G2 | cwd guard disabled
@old if receipt['cwd'] != bundle['cwd']:
@new if False:

@defect G3 | revision guard disabled
@old if receipt['revision'] != bundle['revision']:
@new if False:

@defect G4 | exit guard disabled
@old if receipt['exit'] != required['expect']['exit']:
@new if False:

@defect G5 | stdout finding dropped
@old findings.add('STDOUT_MISMATCH')
@new pass

@defect G6 | membership finding dropped
@old findings.add('MEMBERSHIP_MISMATCH')
@new pass

@defect G7 | duplicate-command refusal dropped
@old return 1, ['DUPLICATE_COMMAND']
@new pass

@defect G8 | duplicate-requirement refusal dropped
@old return 2, ['DUPLICATE_REQUIREMENT']
@new pass

@defect G9 | round-23 anchor bool-exit: receipt exit type check dropped
@old or not revision(row.get('revision')) or type(row.get('exit')) is not int
@new or not revision(row.get('revision')) or False

@defect G10 | round-23 anchor snapshot-pin: bundle digest comparison disabled
@old if digest != expected['bundle_sha256']:
@new if False:

@defect G11 | round-23 anchor empty-requirements: empty requirement list accepted
@old or not isinstance(bundle.get('requirements'), list) or not bundle['requirements']
@new or not isinstance(bundle.get('requirements'), list)

@defect G12 | round-23 anchor stdout: token condition disabled
@old if any(token not in receipt['stdout'] for token in required['expect'].get('stdout_contains', [])):
@new if False:

@defect G13 | round-23 anchor membership: set comparison disabled
@old if set(receipts) != set(requirements):
@new if False:

@defect G14 | round-23 anchor duplicate-command: duplicate receipt name check disabled
@old if row['name'] in receipts:
@new if False:
