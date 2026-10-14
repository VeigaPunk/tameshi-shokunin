# WWKD plan — tameshi round 4 (ufo-round-plan-v1)
Axis move: calibration (suite-vs-arm completeness across the two worked cases).
Claim: a cross-case analysis of the JS (r2) and bash (r3) kill tables yields
the protected/not-protected matrix BY ARM CLASS (what hermetic suites
generically protect: verdict paths, fail-closed arms, counts; what they
miss: reported-but-unasserted surfaces, unreached arms, coordinated edits)
— the calibration axis moves from two data points to a general matrix with
stated confidence.
Also: mutate-and-run.sh gains a --regression mode (re-run both cases as a
kill-rate regression gate for the tool itself).
Anti-claim: if the two cases disagree on any arm class, the disagreement
is the finding (no averaging).
Measure: arm-class matrix rows with per-case kill evidence; the regression
gate's own selftest.
