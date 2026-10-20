#!/usr/bin/env bash
# Companion to run-attribution.sh: the four other KILLED mutants with awk hidden
# from PATH (same bwrap envelope, same symlink farm, same WORKDIR as K_ROWS.noawk).
set -uo pipefail
W=/tmp/tameshi-r18w2-KilledAttribution-3xtmud
C=$W/fleet/tameshi-shokunin
EV=$C/.ufo/evidence/round-18/sources-check
SUITE=$(cat "$EV/suite.txt")
WORK=$W/work
WORK_NOAWK=$W/work-noawk
OUT=$W/out
FARM=$W/noawk-bin

run_suite() { # $1 label  $2 DEFECT_ID  $3 MUTANT  $4 PATH  $5 WORKDIR
  local label=$1 did=$2 mut=$3 p=$4 wd=$5 s e rc
  s=$(date +%s%N)
  bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind "$W" "$W" \
    --unshare-net --die-with-parent --chdir "$W" \
    env -i PATH="$p" HOME="$W/home" TMPDIR="$W/tmp" GIT_CONFIG_GLOBAL=/dev/null \
      GIT_CONFIG_NOSYSTEM=1 LC_ALL=C MUTANT="$mut" WORKDIR="$wd" DEFECT_ID="$did" \
      timeout 300 bash -c "$SUITE" </dev/null >"$OUT/runs/$label.stdout" 2>"$OUT/runs/$label.stderr"
  rc=$?
  e=$(date +%s%N)
  printf '%s\n' "$rc" >"$OUT/runs/$label.exit"
  printf 'RUN %s DEFECT_ID=%s exit=%s duration-ms=%s mutant-sha256=%s stdout-sha256=%s stdout-lines=%s stderr-bytes=%s last=%s\n' \
    "$label" "$did" "$rc" "$(( (e - s) / 1000000 ))" "$(sha256sum "$mut" | cut -d' ' -f1)" \
    "$(sha256sum "$OUT/runs/$label.stdout" | cut -d' ' -f1)" "$(wc -l <"$OUT/runs/$label.stdout")" \
    "$(wc -c <"$OUT/runs/$label.stderr")" "$(grep -E '^SOURCES_SELFTEST:' "$OUT/runs/$label.stdout")"
}

printf 'NOAWK_PROBE: %s\n' "$(env -i PATH="$FARM" sh -c 'command -v awk || echo awk-absent')"
for id in K_KIND K_EXIT K_STRICT K_CLOSED; do
  run_suite "$id.noawk" "$id" "$WORK/mutant-$id.sources-check.mjs" "$FARM" "$WORK_NOAWK"
done
