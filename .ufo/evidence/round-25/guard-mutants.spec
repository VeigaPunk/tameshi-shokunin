# Round-25 C1 item R2 — receipted re-run of the guard sweep on tools/command-binding.py.
# Suite: c1-suite.py selftest "$MUTANT" (the gate's own public selftest, staged privately).
# One guard disabled per defect; G2, G3, G6 and G7 are the four guards round 24 did not re-mutate.
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
