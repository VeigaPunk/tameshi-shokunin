# defect spec v1 — T6-1 service sweep, target mado-shokunin/tools/mado-verify.sh
# pin: sha256 d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13
# clause map: A verdict token · B UNKNOWN-never-CLEAN · C exit map · D declared-plane census
#             E sha comparison · F reader fallback

@defect D1 | clause A: file-plane CLEAN verdict token renamed (CLEAN -> OK)
@old MADO_VERIFY: CLEAN (%s pass, %s notes; file plane only
@new MADO_VERIFY: OK (%s pass, %s notes; file plane only

@defect D2 | clause B: UNKNOWN guard dropped from the CLEAN test
@old if [ "$FAIL" = 0 ] && [ "$UNKNOWN" = 0 ]; then
@new if [ "$FAIL" = 0 ]; then

@defect D3 | clause B: skipped live layer row reports PASS instead of SKIP
@old     row hypr-live live.plane SKIP "live layer skipped ($live_skipped_reason) — file plane only"
@new     row hypr-live live.plane PASS "live layer skipped ($live_skipped_reason) — file plane only"

@defect D4 | clause C: DIVERGED path exits 0
@old "$reason"\nexit 1
@new "$reason"\nexit 0

@defect D5 | clause C: failing --selftest returns 1 not 2
@old   return 2
@new   return 1

@defect D6 | clause D: xdph dropped from the 12-conf local inventory
@old (hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs xdph)
@new (hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs)

@defect D7 | clause D: include-graph count test -ne -> -lt (extra source lines tolerated)
@old if [ "${#got[@]}" -ne "${#EXPECT[@]}" ]; then
@new if [ "${#got[@]}" -lt "${#EXPECT[@]}" ]; then

@defect D8 | clause E: hyprland.conf sha pin comparison always "matches"
@old if [ "$sha" = "4f52854a3c14" ]; then
@new if [ -n "$sha" ]; then

@defect D9 | clause E: read-only boundary comparison always reads byte-identical
@old if [ "$after" = "$before" ]; then
@new if [ -n "$after" ]; then

@defect R1 | clause F: tomllib-unavailable arm reads PASS not UNKNOWN
@old     row walker walker.config UNKNOWN "python3 tomllib unavailable — cannot parse TOML"
@new     row walker walker.config PASS "python3 tomllib unavailable — cannot parse TOML"
