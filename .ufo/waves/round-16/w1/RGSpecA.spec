# tameshi round-16 C1 wave-1 spec fragment — seat RGSpecA (class A: verdict-line paths & pin styles)
# Target: kumitate-shokunin scripts/round-gate.mjs @ 364f1d5954158ef8844bca4a5fef57b05d2f2ca5
# Blob sha256 f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9 (verified 2026-10-20)
# Suite: node "$MUTANT" --selftest   (pristine control observed: 60/60 pass, VERDICT: PASS, exit 0)
# Predictions pre-registered BEFORE any mutant run, from corpus/knowledge/arm-class-matrix.md §13 + pinned-byte reads.
#
# A1 prediction: KILLED — parseVerdict anchored regex (:863) requires `lane=` before `checks=`;
#    v===null in all 10 parseVerdict asserts (:882 :892 :901 :981 :1012 :1053 :1060 :1134 :1299 :1313).
@defect A1 | round-gate.mjs:677 audit/close verdict field reorder lane/checks (full-line pin probe)
@old (round=${round} lane=${opts.lane} checks=${items.length}
@new (round=${round} checks=${items.length} lane=${opts.lane}
#
# A2 prediction: SURVIVED — every FAIL-CLOSED assert matches the (TOKEN) literal or a bare token
#    (:1188 :1193 :1198 :1206 :1218 :1435 :1450) plus detail-substring probes (:1212 :1436);
#    a `detail: ` prefix preserves every asserted substring. Exit 2 (:618) and stderr (:615) unchanged;
#    jFc reads --json only (:1279-1285). Probes the §13.2/§13.5 unasserted detail tail.
@defect A2 | round-gate.mjs:617 FAIL-CLOSED verdict detail tail decorated (unasserted-remainder probe)
@old ROUND_GATE: FAIL-CLOSED (${token}) ${detail}
@new ROUND_GATE: FAIL-CLOSED (${token}) detail: ${detail}
#
# A3 prediction: KILLED (differential) — full-line tracked regexes fail: rt1 (:1411, CLEAN) and rt2
#    (:1426, DRIFT). rt8's prefix regex /^ROUND_GATE: CLEAN \(mode=tracked checked=2 /u (:1481)
#    still matches → rt8 (:1480-1481) stays green. Kills exactly 2 checks; probes the
#    §13.2 full-line vs prefix pin-width gradient inside one verdict family.
@defect A3 | round-gate.mjs:575-576 tracked verdict tail reorder errors/warnings (pin-width probe)
@old lines.push(`ROUND_GATE: ${verdict} (mode=tracked checked=${checked}`\n      + ` errors=${errors} warnings=${warnings})`);
@new lines.push(`ROUND_GATE: ${verdict} (mode=tracked checked=${checked}`\n      + ` warnings=${warnings} errors=${errors})`);
