# tameshi round-16 · RGSpecE fragment — class E/G (unreached usage/refusal arms +
# behaviour predicates/boundaries) against kumitate scripts/round-gate.mjs
# pinned blob sha256 f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9
# (git rev 364f1d5954158ef8844bca4a5fef57b05d2f2ca5). PREDICTIONS PRE-REGISTERED
# BEFORE ANY MUTANT RUN — pristine control observed 60/60 PASS (exit 0) only.
#
# RGE-1  SURVIVED — UFO_SRC set-value arm (:163) is dead under the suite:
#        every runGate call goes through cleanEnv() (:712-716) which deletes
#        UFO_SRC (:711); the only non-empty set-values are UFO_SRC:'' on the
#        derived-origin runs (:1347/:1354/:1369 — fails envSrc.trim()!=='')
#        and UFO_SRC:'/nonexistent/origin' on the nested --selftest spawn
#        (:1390), where opts.selftest short-circuits resolveSrcDefault (:296)
#        before main() calls selfTest() (:635).
# RGE-2  SURVIVED — dirValue flag-like guard (:246) is dead under the suite:
#        no runGate call passes a '--'-prefixed value to --repo/--reports-dir/
#        --main-repo/--origin (:1186-1247, :1447-1484); u5's '' value exits via
#        the :245 throw and the nested --selftest uses non-flag paths (:1392-1394).
# RGE-3  KILLED   — NO_FILED_REPORTS refusal threshold (:535) moved off its
#        boundary: rt3's fixture has filed.length==1 (:1432-1438), so the mutant
#        skips fail-closed, summarizes an empty items list (:544 slice(0,-1)),
#        prints CLEAN exit 0 vs the pinned exit 2 + '(NO_FILED_REPORTS)'.

@defect RGE-1 | UFO_SRC set-value arm: resolve env value -> resolve canonical candidate (unreached arm)
@old   if (typeof envSrc === 'string' && envSrc.trim() !== '') return resolve(envSrc);
@new   if (typeof envSrc === 'string' && envSrc.trim() !== '') return resolve(SRC_CANDIDATES[0]);

@defect RGE-2 | dirValue flag-like guard: '--' predicate weakened to '---' (unreached usage arm)
@old     if (v.startsWith('--')) throw new Error(`${flag} requires a directory (got ${JSON.stringify(v)})`);
@new     if (v.startsWith('---')) throw new Error(`${flag} requires a directory (got ${JSON.stringify(v)})`);

@defect RGE-3 | NO_FILED_REPORTS refusal threshold: <2 -> <1 (boundary shift on a reached arm)
@old   if (filed.length < 2) {
@new   if (filed.length < 1) {
