import json, collections
# id: (first_ack, rounds_carried, closed_round|None, recurred_after_fix, class, duplicate_of)
T = {
 "R40.1": ("r41 corpus/lessons/round-41.md:51", 1, 41, "class: record-drift (r47 spot-check:25; r48 spot-check:30)", "record-drift", []),
 "R40.2": ("none in r41-r50", 10, None, "class: pointer-unresolvable (r41 spot-check:70 = R41.2; r48 spot-check:30)", "pointer-unresolvable", ["R41.2"]),
 "R40.3": ("none in r41-r50", 10, None, "-", "prompt-item-unmet", []),
 "R40.4": ("r41 corpus/lessons/round-41.md:75", 10, None, "class: label-count (r44 spot-check:73), then Q87 held (0 after r45)", "label-count", ["R44.1"]),
 "R40.5": ("pre-routing r39 SCORECARD.md:1859", 0, 39, "-", "guard-vacuous", []),
 "R41.1": ("r42 corpus/lessons/round-42.md:160", 1, 42, "class: instrument-defect (r43 lesson:132)", "instrument-defect", []),
 "R41.2": ("r42 corpus/lessons/round-42.md:159", 1, 42, "class: pointer-unresolvable (r48 spot-check:29)", "pointer-unresolvable", ["R40.2"]),
 "R41.3": ("r42 SCORECARD.md:2028", 1, 42, "-", "instrument-defect", []),
 "R41.4": ("r42 corpus/lessons/round-42.md:252", 1, 42, "-", "instrument-defect", []),
 "R41.5": ("r42 corpus/lessons/round-42.md:247", 1, 42, "-", "doc-overclaim", []),
 "R41.6": ("r42 corpus/lessons/round-42.md:118", 1, 42, "class: id-collision (r42 spot-check:114 -> guard r43)", "id-collision", ["R42.3"]),
 "R41.7": ("r42 corpus/lessons/round-42.md:254", 1, 42, "-", "format-cosmetic", []),
 "R42.1": ("r43 SCORECARD.md:2089", 1, 43, "-", "instrument-defect", []),
 "R42.2": ("r43 corpus/lessons/round-43.md:171", 8, None, "class: instrument-defect (r43 lesson:132; r49 lesson:94)", "instrument-defect", []),
 "R42.3": ("r43 corpus/lessons/round-43.md:81", 1, 43, "-", "id-collision", ["R41.6"]),
 "R42.4": ("r43 corpus/lessons/round-43.md:181", 8, None, "chain restated verbatim (R46.5/R47.7/R48.6/R49.6)", "shonen-box-unpromotable", ["R46.5","R47.7","R48.6","R49.6"]),
 "R43.1": ("r44 corpus/lessons/round-44.md:83", 1, 44, "-", "record-citation-unknown", []),
 "R43.2": ("r44 corpus/lessons/round-44.md:85", 1, 44, "class: record-mutation (r47 spot-check:22)", "record-mutation", []),
 "R43.3": ("r44 corpus/lessons/round-44.md:45", 1, 44, "class: stale-anchor (r45 spot-check:88; r46 spot-check:99)", "stale-anchor", ["R45.4","R46.1"]),
 "R44.1": ("r45 corpus/lessons/round-45.md:158", 6, None, "class: label-count, no recurrence after Q87", "label-count", ["R40.4"]),
 "R44.2": ("r45 (observation, not a defect)", 0, 45, "class: wave-shape (r47 spot-check:21; r48 lesson:305)", "wave-shape", ["R47.6"]),
 "R45.1": ("r46 corpus/lessons/round-46.md:121", 1, 46, "class: monitor-false-red (r48 spot-check:29, after Q88)", "monitor-false-red", []),
 "R45.2": ("r46 closure corpus/lessons/round-46-verifier-spotcheck.md:36", 1, 46, "YES: r47 spot-check:23 and :24", "receipt-not-committed", ["R47.2"]),
 "R45.3": ("r45 SCORECARD.md:2159 (same round)", 0, 45, "-", "measure-definition-change", []),
 "R45.4": ("r46 SCORECARD.md:2253", 3, 48, "class: stale-anchor", "stale-anchor", ["R46.1","R47.5"]),
 "R46.1": ("r47 SCORECARD.md:2312", 2, 48, "-", "stale-anchor", ["R45.4","R47.5"]),
 "R46.2": ("r47 SCORECARD.md:2309", 1, 47, "-", "capability-not-operative", []),
 "R46.3": ("r47 SCORECARD.md:2264", 1, 47, "class: standing-row-unreproducible (r47 spot-check:103 -> Q95)", "standing-row-unreproducible", ["R47.1"]),
 "R46.4": ("r47 corpus/lessons/round-47.md:105", 1, 47, "class: quote-fold, no recurrence after Q91", "quote-fold", []),
 "R46.5": ("chain restated", 4, None, "-", "shonen-box-unpromotable", ["R42.4"]),
 "R47.1": ("r48 corpus/lessons/round-48.md:108", 1, 48, "class: standing-row-unreproducible, residual race re-routed r49", "standing-row-unreproducible", ["R46.3"]),
 "R47.2": ("r48 corpus/lessons/round-48.md:306", 3, None, "YES (class): r45 -> fixed r46 -> r47", "receipt-not-committed", ["R45.2"]),
 "R47.3": ("r48 corpus/lessons/round-48.md:108", 1, 48, "-", "record-drift", []),
 "R47.4": ("r48 corpus/lessons/round-48.md:270", 1, 48, "-", "weak-citation", []),
 "R47.5": ("r48 SCORECARD.md:2312", 3, None, "carried-list class persists (R48.4/R49.5)", "carried-open", ["R45.4","R46.1","R48.4","R49.5"]),
 "R47.6": ("r48 corpus/lessons/round-48.md:305", 2, 49, "class: wave-shape (r48 spot-check:28)", "wave-shape", ["R44.2"]),
 "R47.7": ("chain restated", 3, None, "-", "shonen-box-unpromotable", ["R42.4"]),
 "R48.1": ("r49 corpus/lessons/round-49.md:6", 1, 49, "-", "coldread-credit-loss", []),
 "R48.2": ("r49 corpus/lessons/round-49.md:90", 1, 49, "-", "order-of-scoring", []),
 "R48.3": ("r49 corpus/lessons/round-49.md:90", 1, 49, "-", "order-of-scoring", ["R48.2"]),
 "R48.4": ("r49 closure corpus/lessons/round-49-verifier-spotcheck.md:126", 2, None, "carried-list class", "carried-open", ["R47.5","R49.5"]),
 "R48.5": ("r49 corpus/lessons/round-49.md:92", 1, 49, "-", "record-drift", []),
 "R48.6": ("chain restated", 2, None, "-", "shonen-box-unpromotable", ["R42.4"]),
 "R49.1": ("none: absent from Planned (round 50)", 1, None, "-", "generator-error-path", []),
 "R49.2": ("r50 SCORECARD.md:2410", 1, None, "-", "instrument-defect", []),
 "R49.3": ("r50 SCORECARD.md:2410", 1, None, "-", "outside-section-stale", []),
 "R49.4": ("r50 SCORECARD.md:2416", 1, 50, "-", "standing-axis-table-stale", []),
 "R49.5": ("r50 SCORECARD.md:2410", 1, None, "carried-list class", "carried-open", ["R47.5","R48.4"]),
 "R49.6": ("chain restated", 1, None, "-", "shonen-box-unpromotable", ["R42.4"]),
}
rows=[]
DECLINED = {"R41.7", "R44.2", "R45.3"}
PRE = {"R40.5"}
for k,(ack,carried,closed,rec,cls,dup) in T.items():
    rows.append(dict(id=k, first_ack=ack, rounds_carried=carried, closed_round=closed,
                     declined=(k in DECLINED), pre_routing=(k in PRE),
                     recurred_after_fix=rec, defect_class=cls, duplicate_of=dup))
json.dump({"schema":"tameshi-r50-recurrence-walk-v1","count":len(rows),"rows":rows},
          open('recurrence-walk.json','w'), indent=1)
c=collections.Counter(r['defect_class'] for r in rows)
multi={k:v for k,v in c.items() if v>=2}
print("rows", len(rows), "classes", len(c), "multi", len(multi))
print("multi:", dict(sorted(multi.items(), key=lambda kv:-kv[1])))
print("open(no closed round):", sum(1 for r in rows if r['closed_round'] is None))
print("open by carried>=2:", [r['id'] for r in rows if r['closed_round'] is None and r['rounds_carried']>=2])
