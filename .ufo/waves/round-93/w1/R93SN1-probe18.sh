#!/usr/bin/env bash
# R93SN1 probe 18 (CANONICAL reproduction of F1): the pin/pins conjuncts are
# self-referential.  A lane commit that (a) repoints census-mutants.json's gate
# block at a FOREIGN repo/commit and (b) regenerates pins.json with the lane's own
# committed make-pins.py yields pin=true, pins=true, green=true -- while the
# counter EXECUTES the foreign gate's bytes.
#
# Nothing here writes to the lane or to the fleet repo: every fixture lives under
# $S and is removed on exit.
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe18.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
MEAS="$LANE/.ufo/evidence/round-93/c1/measure-v93.py"
MPINS="$LANE/.ufo/evidence/round-93/c1/make-pins.py"
REV=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
probe() { printf 'PROBE %-52s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "F1 step 1: a FOREIGN 'fleet' repo whose gate is a marker script"
git init -q "$S/foreign"
mkdir -p "$S/foreign/scripts/fixtures/sources-census"
printf 'fixture\n' > "$S/foreign/scripts/fixtures/sources-census/root.txt"
printf '#!/usr/bin/env bash\n# PROBE_MARKER_F1 FOREIGN-GATE-EXECUTED\ncase "$1" in selftest) echo "selftest ok";; esac\n' \
  > "$S/foreign/scripts/sources-census.sh"
chmod +x "$S/foreign/scripts/sources-census.sh"
git -C "$S/foreign" add -A && git -C "$S/foreign" -c user.name=t -c user.email=t@t commit -q -m gate
FC=$(git -C "$S/foreign" rev-parse HEAD)
FSHA=$(git -C "$S/foreign" cat-file blob HEAD:scripts/sources-census.sh | sha256sum | cut -d' ' -f1)
probe "F1.foreign-commit" "$FC"
probe "F1.foreign-gate-sha256" "$FSHA"

sec "F1 step 2: a lane clone whose spec names the foreign repo, pins regenerated"
git clone -q --shared --no-checkout "$LANE" "$S/lane" 2>/dev/null
git -C "$S/lane" checkout -q --detach "$REV" 2>/dev/null
python3 - "$S/lane/.ufo/evidence/round-93/c1/census-mutants.json" "$S/foreign" "$FC" "$FSHA" <<'PY'
import json, sys
p, repo, commit, sha = sys.argv[1:5]
s = json.load(open(p))
s["gate"].update(repo=repo, commit=commit, path="scripts/sources-census.sh", sha256=sha)
json.dump(s, open(p, "w"), indent=1)
PY
git -C "$S/lane" add -A && git -C "$S/lane" -c user.name=t -c user.email=t@t commit -q -m "spec repointed"
R1=$(git -C "$S/lane" rev-parse HEAD)
python3 -I "$MPINS" --lane "$S/lane" --rev "$R1" >"$S/mp.log" 2>&1
probe "F1.make-pins.rc" "$?"
probe "F1.make-pins-output" "$(tail -1 "$S/mp.log" | cut -c1-120)"
git -C "$S/lane" add -A && git -C "$S/lane" -c user.name=t -c user.email=t@t commit -q -m "pins regenerated"
R2=$(git -C "$S/lane" rev-parse HEAD)
probe "F1.lane-commit-under-test" "$R2"
probe "F1.pins-now-name-the-foreign-gate" "$(git -C "$S/lane" show "$R2:.ufo/evidence/round-93/c1/pins.json" | grep -E 'gate_commit|gate_sha256' | tr '\n' ' ')"

sec "F1 step 3: run the frozen counter at that commit"
mkdir -p "$S/w"
python3 -I "$MEAS" --repo "$S/lane" --rev "$R2" --work "$S/w" >"$S/f1.log" 2>&1
probe "F1.counter-rc" "$?"
probe "F1.PASS-line" "$(grep '^C1_R93_PASS' "$S/f1.log")"
probe "F1.pin-pins-green-canary" "$(grep '^C1_CONJUNCTS' "$S/f1.log" | tr ' ' '\n' | grep -E '^(pin|pins|green|canary)=' | tr '\n' ' ')"
probe "F1.FOREIGN-gate-EXECUTED" "$(grep -q PROBE_MARKER_F1 "$S/w/pristine/scripts/sources-census.sh" 2>/dev/null && echo 'YES - the FOREIGN gate bytes were executed' || echo no)"
probe "F1.executed-bytes-digest" "$(sha256sum "$S/w/pristine/scripts/sources-census.sh" 2>/dev/null | cut -c1-16) vs foreign $FSHA"
probe "F1.conclusion" "pin=true AND pins=true AND green=true while the measured gate is NOT the fleet gate at f47ad6b"

sec "F1 control: the SAME counter on the untouched lane at the frozen rev"
mkdir -p "$S/w2"
python3 -I "$MEAS" --repo "$LANE" --rev "$REV" --work "$S/w2" >"$S/ctrl.log" 2>&1
probe "F1.control-rc" "$?"
probe "F1.control-conjuncts" "$(grep '^C1_CONJUNCTS' "$S/ctrl.log" | tr ' ' '\n' | grep -E '^(pin|pins|green)=' | tr '\n' ' ')"
probe "F1.control-executed-gate-has-marker" "$(grep -q PROBE_MARKER_F1 "$S/w2/pristine/scripts/sources-census.sh" 2>/dev/null && echo 'marker present (unexpected)' || echo 'no marker - the real fleet gate ran')"

printf '\n===== done =====\n'
