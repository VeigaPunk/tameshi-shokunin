#!/usr/bin/env bash
# tameshi round-18 w2 KilledAttribution runner (scratch; every write stays under $W).
# Builds the five KILLED-predicted mutants of the pinned kumitate sources-check.mjs
# blob with the mutate-and-run.sh apply helper extracted verbatim from the tool at
# the read rev, then runs the registered suite string (suite.txt) once per mutant
# under bwrap (fleet read-only, no network), capturing full stdout / stderr / exit.
# Extra runs: pristine control (host PATH), and pristine + K_ROWS with every
# *awk* name removed from PATH (symlink farm of all other PATH executables).
set -uo pipefail
W=/tmp/tameshi-r18w2-KilledAttribution-3xtmud
C=$W/fleet/tameshi-shokunin
EV=$C/.ufo/evidence/round-18/sources-check
SPEC=$EV/sources-check.defects.spec
PIN=$W/pin/sources-check.mjs
SUITE=$(cat "$EV/suite.txt")
WORK=$W/work
WORK_NOAWK=$W/work-noawk
OUT=$W/out
FARM=$W/noawk-bin
HOSTPATH=$PATH
IDS=(K_KIND K_EXIT K_STRICT K_CLOSED K_ROWS)

mkdir -p "$WORK" "$WORK_NOAWK" "$OUT/runs" "$OUT/diffs" "$W/home" "$W/tmp" "$FARM"

# 1. apply helper: the tool's embedded Python, extracted verbatim (marker-delimited)
python3 - "$C/tools/mutate-and-run.sh" "$W/helper.py" <<'EOF'
import sys
src = open(sys.argv[1], encoding='utf-8').read().split('\n')
start = src.index("  python3 - \"$@\" <<'PYEOF'") + 1
end = src.index('PYEOF', start)
open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(src[start:end]) + '\n')
print('HELPER_LINES: %d-%d of tools/mutate-and-run.sh' % (start + 1, end))
EOF

# 2. pristine copy + mutants (same naming as run_sweep: mutant-<id>.<basename>)
PRISTINE=$WORK/pristine.sources-check.mjs
cp -p "$PIN" "$PRISTINE"
printf 'PIN_SHA256: %s\n' "$(sha256sum "$PIN" | cut -d' ' -f1)"
printf 'PRISTINE_SHA256: %s\n' "$(sha256sum "$PRISTINE" | cut -d' ' -f1)"
for id in "${IDS[@]}"; do
  m=$WORK/mutant-$id.sources-check.mjs
  cp -p "$PRISTINE" "$m"
  python3 "$W/helper.py" apply "$SPEC" "$PRISTINE" "$m" "$id"
  printf 'MUTANT %s sha256=%s\n' "$id" "$(sha256sum "$m" | cut -d' ' -f1)"
  diff -u --label "pristine/sources-check.mjs" --label "mutant-$id/sources-check.mjs" "$PRISTINE" "$m" > "$OUT/diffs/$id.diff"
  printf 'DIFF %s exit=%s\n' "$id" "$?"
done

# 3. awk-hidden PATH: symlink every PATH executable (first match wins) except *awk* names
excluded=()
IFS=: read -ra dirs <<<"$HOSTPATH"
for d in "${dirs[@]}"; do
  [[ -d "$d" ]] || continue
  for f in "$d"/*; do
    n=${f##*/}
    if [[ "$n" == *awk* ]]; then excluded+=("$f"); continue; fi
    if [[ -e "$FARM/$n" || -L "$FARM/$n" ]]; then continue; fi
    [[ -f "$f" && -x "$f" ]] || continue
    ln -s "$f" "$FARM/$n"
  done
done
printf 'NOAWK_FARM_ENTRIES: %s\n' "$(find "$FARM" -mindepth 1 -maxdepth 1 | wc -l)"
printf 'NOAWK_EXCLUDED: %s\n' "${excluded[*]}"
printf 'NOAWK_PROBE: %s\n' "$(env -i PATH="$FARM" sh -c 'command -v awk || echo awk-absent; command -v gawk || echo gawk-absent; for t in node sh grep sort uniq wc tr mkdir env bash timeout; do command -v "$t" >/dev/null || echo "MISSING-$t"; done')"
printf 'HOST_PROBE: %s\n' "$(env -i PATH="$HOSTPATH" sh -c 'command -v awk')"

# 4. suite runs under bwrap (fleet read-only; only $W writable; no network)
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

run_suite CONTROL CONTROL "$PRISTINE" "$HOSTPATH" "$WORK"
for id in "${IDS[@]}"; do
  run_suite "$id" "$id" "$WORK/mutant-$id.sources-check.mjs" "$HOSTPATH" "$WORK"
done
run_suite CONTROL.noawk CONTROL "$PRISTINE" "$FARM" "$WORK_NOAWK"
run_suite K_ROWS.noawk K_ROWS "$WORK/mutant-K_ROWS.sources-check.mjs" "$FARM" "$WORK_NOAWK"

# 5. independent cross-check: the tool's own sweep of the full spec (full tails)
s=$(date +%s%N)
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind "$W" "$W" \
  --unshare-net --die-with-parent --chdir "$W" \
  env -i PATH="$HOSTPATH" HOME="$W/home" TMPDIR="$W/tmp" GIT_CONFIG_GLOBAL=/dev/null \
    GIT_CONFIG_NOSYSTEM=1 LC_ALL=C \
    bash "$C/tools/mutate-and-run.sh" --target "$PIN" --defects "$SPEC" --suite "$SUITE" \
      --workdir "$W/toolsweep" --tail 200 </dev/null >"$OUT/toolsweep.txt" 2>"$OUT/toolsweep.stderr"
rc=$?
e=$(date +%s%N)
printf '%s\n' "$rc" >"$OUT/toolsweep.exit"
printf 'TOOLSWEEP exit=%s duration-ms=%s summary=%s\n' "$rc" "$(( (e - s) / 1000000 ))" "$(grep -E '^MUTATE: ' "$OUT/toolsweep.txt")"
