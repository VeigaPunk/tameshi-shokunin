# One-defect spec used only to show tools/mutate-and-run.sh cannot attribute
# kills on the round-56 C1 counter: its suite contract needs a GREEN control run
# on the pristine artifact, but the pristine counter is red on every defective
# fixture by construction (that is what the arm does).
@defect M6 | UNSTABLE_INPUTS emptied: arm 5 can no longer fire
@old UNSTABLE_INPUTS = ('LOG.md', 'SCORECARD.md')
@new UNSTABLE_INPUTS = ()
