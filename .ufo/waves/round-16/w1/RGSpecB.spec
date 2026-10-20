# RGSpecB — class B candidates (fail-closed arms/tokens) for js-round-gate leg
# Target: kumitate-shokunin/scripts/round-gate.mjs @ 364f1d59 (blob sha256
# f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9, 1511 lines).
# Predictions pre-registered from corpus/knowledge/arm-class-matrix.md §13.3/§13.6
# BEFORE any mutant run. Pristine selftest baseline: 60/60 pass, exit 0
# (node v24.21.0, /tmp copy of the pinned blob, 2026-10-20).
# Each @old string verified count==1 against the pinned blob via literal counter.
#
# RGD-B1 — main-path REPORTS_DIR_MISSING call site (:647) rewrites the token to
# the wrong declared token; the covered species must die.
# PRE-REGISTERED: KILLED — fcA (:1187-1189, selftest check [32]) pins the
# parenthesized token; jFc (:1278-1285, check [45]) pins findings[0].kind ===
# 'REPORTS_DIR_MISSING' on the same arm.
@defect RGD-B1 | main-path REPORTS_DIR_MISSING site emits MAIN_REPO_NOT_GIT token (predicted KILLED: fcA, jFc)
@old return failClosed(opts, mode, 'REPORTS_DIR_MISSING',
@new return failClosed(opts, mode, 'MAIN_REPO_NOT_GIT',
#
# RGD-B2 — same one-token defect cut at the tracked-mode REPORTS_DIR_MISSING
# site (:527); the identical species probe on the uncovered call-site species.
# PRE-REGISTERED: SURVIVED — no fixture runs --tracked with a missing
# --reports-dir (§13.3/§13.6 #2). rt1-rt8 all pass existing reports dirs; rt5's
# fixture reports dir exists so the :526 arm is skipped and :530's own
# MAIN_REPO_NOT_GIT token still satisfies its regex.
@defect RGD-B2 | tracked-mode REPORTS_DIR_MISSING site emits MAIN_REPO_NOT_GIT token (predicted SURVIVED: species uncovered)
@old return failClosed(opts, 'tracked', 'REPORTS_DIR_MISSING',
@new return failClosed(opts, 'tracked', 'MAIN_REPO_NOT_GIT',
#
# RGD-B3 — catch-all token renamed (:683); the INTERNAL_ERROR net is asserted
# by nothing (§13.3: "none", §13.6 #1, PU3).
# PRE-REGISTERED: SURVIVED — no fixture throws inside main's try (:641-684);
# fail-closed text lines cannot be parsed by parseFindings (:857-860) and the
# kind meta-check (:1487-1493) iterates FINDING_KINDS, which excludes all 7
# fail-closed tokens.
@defect RGD-B3 | INTERNAL_ERROR catch-all token renamed to UPSTREAM_MISSING (predicted SURVIVED: zero fixture coverage)
@old return failClosed(opts, mode, 'INTERNAL_ERROR', e && e.message ? e.message : String(e), [], started);
@new return failClosed(opts, mode, 'UPSTREAM_MISSING', e && e.message ? e.message : String(e), [], started);
