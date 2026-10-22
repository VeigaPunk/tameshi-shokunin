# T8-1 mutation spec — kagi-shokunin/corpus/checklist-run.sh
# target pin sha256 7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf
# (506 L / 24697 B, mode 755, mtime 2026-10-13 16:51:07 -0300; = kagi HEAD fecee87 blob)
# clause map (gate's declared contract, checklist-run.sh:2-61):
#   A item extraction (:96-116)      B row-declaration policy (:120-172)
#   C lead bijection (:205-237)      D ratio floor (:174, :239-246)
#   E row execution (:256-279)       F verdict lines / exit map (:281-297)
#   G CLI modes (:79-91, :501-506)
# predictions pre-registered BEFORE the sweep; K = expect KILLED, S = expect SURVIVED.
#
@defect A1 | section never closes — the '## ' stop becomes an exact two-char header  # predict S (hole)
@old     [[ "$line" == '## '* ]] && break
@new     [[ "$line" == '## ' ]] && break
#
@defect A2 | section never opens — the header gate sets in=0  # predict K
@old       [[ "$line" == '## Credential-hygiene checklist' ]] && in=1
@new       [[ "$line" == '## Credential-hygiene checklist' ]] && in=0
#
@defect B1 | id charset loosened to ^[A-Z]+[0-9]+$ (multi-letter ids accepted)  # predict S (hole)
@old     if [[ ! "$id" =~ ^[A-Z][0-9]+$ ]]; then
@new     if [[ ! "$id" =~ ^[A-Z]+[0-9]+$ ]]; then
#
@defect B2 | by-hand non-space floor 20 -> 0 (padded reasons accepted)  # predict K
@old     ((ns >= 20)) || {
@new     ((ns >= 0)) || {
#
@defect B3 | deny list drops `the-janitor stop` (a denied surface re-opens)  # predict S (hole)
@old the-janitor start|the-janitor stop|the-janitor run
@new the-janitor start|the-janitor run
#
@defect B4 | expect_exit accepts a single integer only (multi-exit rows become POLICY)  # predict K
@old     [[ "$exexit" =~ ^[0-9]+(\\|[0-9]+)*$ ]]
@new     [[ "$exexit" =~ ^[0-9]+$ ]]
#
@defect C1 | UNMATCHED-ITEM never reported (condition 0 -> -1)  # predict S (hole)
@old ((hits == 0)) && defect "UNMATCHED-ITEM
@new ((hits == -1)) && defect "UNMATCHED-ITEM
#
@defect C2 | DUPLICATE-ITEM threshold raised 1 -> 2 (two declarers invisible)  # predict K
@old ((hits > 1)) && defect "DUPLICATE-ITEM
@new ((hits > 2)) && defect "DUPLICATE-ITEM
#
@defect D1 | floor_of truncates instead of ceiling (odd item counts)  # predict S (hole)
@old floor_of() { printf '%s' "$(((($1 + FLOOR_DEN - 1)) / FLOOR_DEN))"; }
@new floor_of() { printf '%s' "$((($1) / FLOOR_DEN))"; }
#
@defect D2 | ratio denominator 2 -> 1 (floor = every item)  # predict K
@old FLOOR_DEN=2   # floor = ceil(items / FLOOR_DEN)
@new FLOOR_DEN=1   # floor = ceil(items / FLOOR_DEN)
#
@defect E1 | exit-set membership becomes exact equality (A|B arms never accepted)  # predict K
@old       [[ "|$want|" == *"|$rc|"* ]] || {
@new       [[ "$want" == "$rc" ]] || {
#
@defect E2 | row output captured without stderr (2>&1 dropped)  # predict S (hole)
@old     out=$(cd "$ROOT" && timeout "$ROW_TIMEOUT" bash -c "${R_CHECK[$i]}" 2>&1) || rc=$?
@new     out=$(cd "$ROOT" && timeout "$ROW_TIMEOUT" bash -c "${R_CHECK[$i]}") || rc=$?
#
@defect F1 | defect path returns 0 — BROKEN still exits 0  # predict K
@old     return 1\n  fi\n  if [[ -n "$ONLY" ]]; then\n    printf 'CHECKLIST_ROW: CLEAN
@new     return 0\n  fi\n  if [[ -n "$ONLY" ]]; then\n    printf 'CHECKLIST_ROW: CLEAN
#
@defect F2 | --only BROKEN line prints failed=0  # predict S (hole)
@old printf 'CHECKLIST_ROW: BROKEN (id=%s failed=%s — this is a single row, not the checklist)\\n' "$ONLY" "$failed"
@new printf 'CHECKLIST_ROW: BROKEN (id=%s failed=0 — this is a single row, not the checklist)\\n' "$ONLY" "$failed"
#
@defect G1 | unknown argument fail-open — exit 2 -> 0  # predict S (hole)
@old     *) printf 'checklist-run: unknown argument: %s\\n' "$1" >&2; exit 2 ;;
@new     *) printf 'checklist-run: unknown argument: %s\\n' "$1" >&2; exit 0 ;;
