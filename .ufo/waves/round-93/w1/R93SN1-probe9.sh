#!/usr/bin/env bash
# R93SN1 probe 9: (a) spec+pins swap keeps pin/pins TRUE while a foreign gate is executed;
#                 (b) the driver's toplevel guard vs an ambient GIT_DIR, precisely.
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe9.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
REV=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
probe() { printf 'PROBE %-50s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "K1 spec AND pins.json swapped together: are pin/pins still TRUE?"
git clone -q --shared --no-checkout "$LANE" "$S/laneK" 2>/dev/null
git -C "$S/laneK" checkout -q --detach "$REV" 2>/dev/null
# a foreign 'fleet' repo whose gate is a marker script
git init -q "$S/fleetK"
mkdir -p "$S/fleetK/scripts/fixtures/sources-census"
printf '#!/usr/bin/env bash\n# PROBE_MARKER_K1 foreign-gate\ncase "$1" in selftest) echo "selftest ok";; esac\n' \
  > "$S/fleetK/scripts/sources-census.sh"
chmod +x "$S/fleetK/scripts/sources-census.sh"
git -C "$S/fleetK" add -A && git -C "$S/fleetK" -c user.name=t -c user.email=t@t commit -q -m gate
FC=$(git -C "$S/fleetK" rev-parse HEAD)
FSHA=$(git -C "$S/fleetK" rev-parse "HEAD:scripts/sources-census.sh" | xargs -I{} git -C "$S/fleetK" cat-file blob {} | sha256sum | cut -d' ' -f1)
python3 - "$S/laneK/.ufo/evidence/round-93/c1/census-mutants.json" "$S/fleetK" "$FC" "$FSHA" <<'PY'
import json, sys
p, repo, commit, sha = sys.argv[1:5]
s = json.load(open(p))
s["gate"].update(repo=repo, commit=commit, sha256=sha)
json.dump(s, open(p, "w"), indent=1)
PY
git -C "$S/laneK" add -A && git -C "$S/laneK" -c user.name=t -c user.email=t@t commit -q -m "spec swapped"
R1=$(git -C "$S/laneK" rev-parse HEAD)
# regenerate pins.json from the swapped spec using the lane's OWN generator
python3 -I "$LANE/.ufo/evidence/round-93/c1/make-pins.py" --lane "$S/laneK" --rev "$R1" >"$S/k1p.log" 2>&1
probe "K1.make-pins.rc" "$?"
git -C "$S/laneK" add -A && git -C "$S/laneK" -c user.name=t -c user.email=t@t commit -q -m "pins regenerated"
R2=$(git -C "$S/laneK" rev-parse HEAD)
mkdir -p "$S/wK"
python3 -I "$LANE/.ufo/evidence/round-93/c1/measure-v93.py" --repo "$S/laneK" --rev "$R2" --work "$S/wK" >"$S/k1.log" 2>&1
probe "K1.rc" "$?"
probe "K1.pin-pins-green" "$(grep '^C1_CONJUNCTS' "$S/k1.log" | tr ' ' '\n' | grep -E '^(pin|pins|green)=' | tr '\n' ' ')"
probe "K1.foreign-gate-executed" "$(grep -q PROBE_MARKER_K1 "$S/wK/pristine/scripts/sources-census.sh" 2>/dev/null && echo 'YES - the FOREIGN gate ran' || echo no)"
probe "K1.plan-spec-digest-vs-now" "$(echo 'plan says ce8983d5...; the lane now has:'; sha256sum "$S/laneK/.ufo/evidence/round-93/c1/census-mutants.json" | cut -c1-16)"

sec "K2 the driver's toplevel guard vs ambient GIT_DIR (one-liner)"
git init -q "$S/otherK"; git -C "$S/otherK" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
git clone -q --shared "$S/otherK" "$S/tgtK" 2>/dev/null
probe "K2.plain.toplevel" "$(git -C "$S/tgtK" rev-parse --show-toplevel 2>&1 | sed "s|$S|\$S|g")"
probe "K2.hijacked.toplevel" "$(GIT_DIR="$S/otherK/.git" git -C "$S/tgtK" rev-parse --show-toplevel 2>&1 | sed "s|$S|\$S|g")"
GIT_DIR="$S/otherK/.git" git -C "$S/tgtK" commit -q --allow-empty -m hijack 2>/dev/null
probe "K2.hijacked-commit-landed-in" "$(git -C "$S/otherK" log --oneline -1 2>&1 | sed "s|$S|\$S|g")"
probe "K2.guard-would-pass" "$([ "$(GIT_DIR=$S/otherK/.git git -C $S/tgtK rev-parse --show-toplevel)" = "$S/tgtK" ] && echo 'YES - show-toplevel reports the -C dir, so the guard PASSES while the commit lands elsewhere' || echo no)"

sec "K3 git -C '' in the COUNTER's own helper (fleet-incident shape)"
git init -q "$S/cwdK"; git -C "$S/cwdK" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
probe "K3.git-C-empty-toplevel" "$(cd "$S/cwdK" && git -C "" rev-parse --show-toplevel 2>&1 | sed "s|$S|\$S|g")"
probe "K3.git-C-empty-commits-here" "$(cd "$S/cwdK" && git -C "" commit -q --allow-empty -m x >/dev/null 2>&1; git -C "$S/cwdK" log --oneline -1 | sed "s|$S|\$S|g")"

printf '\n===== done =====\n'
