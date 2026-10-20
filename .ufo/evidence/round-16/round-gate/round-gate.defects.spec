# tameshi round-16 C1 — PRE-REGISTERED mutation spec for kumitate scripts/round-gate.mjs
# rev 364f1d5954158ef8844bca4a5fef57b05d2f2ca5 · blob sha256 f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9 · 1511 lines
# Suite (guarded, RGSentinel): see suite.txt beside this file. Verdict oracle = exit status only
# (KILLED = exit not in {0,124,126,127}); stdout is not byte-deterministic (mkdtemp names, RGControl).
# Predictions are fixed here BEFORE any mutant run; composition 5 kill-aimed / 5 hole-aimed.
# Sources: corpus/knowledge/arm-class-matrix.md §13 (projection, round 4) + wave-1 seat fragments
# (.ufo/waves/round-16/w1/RGSpec{A,B,C,E}.spec). Operator classes: S052 (Stryker supported mutators).

# PREDICT KILLED — parseVerdict full-line anchored regex :862-868; all 10 call sites assert v!==null (matrix §13.2; RGSpecA)
@defect A1 | verdict path: audit/close verdict fields lane/checks reordered (:677) (predict KILLED)
@old (round=${round} lane=${opts.lane} checks=${items.length}
@new (round=${round} checks=${items.length} lane=${opts.lane}

# PREDICT KILLED — rt1 :1411 and rt2 :1426 full-line regexes fail; rt8 prefix regex :1481 stays green (matrix §13.2; RGSpecA)
@defect A3 | verdict path: tracked verdict tail errors/warnings reordered (:575-576) (predict KILLED)
@old lines.push(`ROUND_GATE: ${verdict} (mode=tracked checked=${checked}`\n      + ` errors=${errors} warnings=${warnings})`);
@new lines.push(`ROUND_GATE: ${verdict} (mode=tracked checked=${checked}`\n      + ` warnings=${warnings} errors=${errors})`);

# PREDICT KILLED — fcA :1188 pins (REPORTS_DIR_MISSING); jFc :1283 pins findings[0].kind (matrix §13.3; RGSpecB)
@defect B1 | fail-closed token: main-path REPORTS_DIR_MISSING site emits MAIN_REPO_NOT_GIT (:647) (predict KILLED)
@old return failClosed(opts, mode, 'REPORTS_DIR_MISSING',
@new return failClosed(opts, mode, 'MAIN_REPO_NOT_GIT',

# PREDICT KILLED — rt3 :1432-1438 files exactly one report and pins exit 2 + token (matrix §13.3/§13.8; RGSpecE, RGMatrix D3)
@defect E3 | predicate boundary: NO_FILED_REPORTS threshold filed.length < 2 -> < 1 (:535) (predict KILLED)
@old if (filed.length < 2) {
@new if (filed.length < 1) {

# PREDICT KILLED — r8 report is 1059 B (matrix §13.4/§13.10 #3; RGMatrix, RGSpecC); 1060 makes it thin -> r8 kind list changes
@defect C1060 | count floor: REPORT_MIN_BYTES 1024 -> 1060, one past the projected interval [26,1059] (:167) (predict KILLED)
@old const REPORT_MIN_BYTES = 1024;
@new const REPORT_MIN_BYTES = 1060;

# PREDICT SURVIVED — matrix §13.4: a single edit to any integer in [26,1059] changes no fixture verdict (projected, PU1)
@defect C1059 | count floor: REPORT_MIN_BYTES 1024 -> 1059, the upper edge of the projected interval [26,1059] (:167) (predict SURVIVED)
@old const REPORT_MIN_BYTES = 1024;
@new const REPORT_MIN_BYTES = 1059;

# PREDICT SURVIVED — every fail-closed assert pins the (TOKEN) or a needle the prefix preserves (matrix §13.2/§13.5 #1; RGSpecA)
@defect A2 | reported-unread: FAIL-CLOSED detail tail decorated with "detail: " (:617) (predict SURVIVED)
@old ROUND_GATE: FAIL-CLOSED (${token}) ${detail}
@new ROUND_GATE: FAIL-CLOSED (${token}) detail: ${detail}

# PREDICT SURVIVED — no --tracked fixture with a missing reports dir (matrix §13.3, §13.6 #2; RGSpecB)
@defect B2 | unreached species: tracked-mode REPORTS_DIR_MISSING site emits MAIN_REPO_NOT_GIT (:527) (predict SURVIVED)
@old return failClosed(opts, 'tracked', 'REPORTS_DIR_MISSING',
@new return failClosed(opts, 'tracked', 'MAIN_REPO_NOT_GIT',

# PREDICT SURVIVED — meta-check reads enum minus observed only; shrinking the enum cannot fail it (matrix §13.4 one-sided count; RGSpecC)
@defect CKIND | meta-check blindness: TREE_DIRTY dropped from FINDING_KINDS (:175) (predict SURVIVED)
@old   'TREE_DIRTY', 'UNPUSHED', 'REPORT_UNTRACKED',
@new   'UNPUSHED', 'REPORT_UNTRACKED',

# PREDICT SURVIVED — cleanEnv deletes UFO_SRC; fixtures set only UFO_SRC:"" (matrix §13.6 #5; RGSpecE)
@defect E1 | unreached arm: UFO_SRC set-value branch resolves the canonical candidate instead (:163) (predict SURVIVED)
@old   if (typeof envSrc === 'string' && envSrc.trim() !== '') return resolve(envSrc);
@new   if (typeof envSrc === 'string' && envSrc.trim() !== '') return resolve(SRC_CANDIDATES[0]);
