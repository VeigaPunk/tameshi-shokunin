#!/usr/bin/env bash
# R93SN1 probe 6: does the counter EXECUTE gate bytes whose pin does not hold,
# and does ambient GIT_DIR defeat the driver's toplevel guard (fleet-incident shape)?
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe6.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
CTRL="$LANE/.ufo/evidence/round-93/c1/controls-v93.py"
MEAS="$LANE/.ufo/evidence/round-93/c1/measure-v93.py"
REV=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
BASE=4a7e259b407d582d2010197f32d7524d6bed5370
FLEET=/home/vgpnk/Projects/shokunin
probe() { printf 'PROBE %-46s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "H1 spec pins a DIFFERENT fleet commit: does the counter still EXECUTE that gate?"
# a scratch fleet clone whose gate carries a marker line, so execution is observable
git clone -q --shared --no-checkout "$FLEET" "$S/fleet2" 2>/dev/null
git -C "$S/fleet2" checkout -q --detach f47ad6ba8d306f8125597401cb2ce45c1297a593 2>/dev/null
mkdir -p "$S/fleet2/scripts"
printf '#!/usr/bin/env bash\n# PROBE_MARKER_H1 executed-gate-bytes\necho "selftest ok"\n' > "$S/fleet2/scripts/sources-census.sh"
chmod +x "$S/fleet2/scripts/sources-census.sh"
git -C "$S/fleet2" add scripts/sources-census.sh
git -C "$S/fleet2" -c user.name=t -c user.email=t@t commit -q -m "probe marker gate"
HC=$(git -C "$S/fleet2" rev-parse HEAD)
probe "H1.probe-fleet-commit" "$HC"
# the fixture lane: the committed spec, but gate.commit/sha256 pointed at the probe fleet
git clone -q --shared --no-checkout "$LANE" "$S/laneH" 2>/dev/null
git -C "$S/laneH" checkout -q --detach "$REV" 2>/dev/null
GSHA=$(git -C "$S/fleet2" rev-parse "HEAD:scripts/sources-census.sh" | xargs -I{} git -C "$S/fleet2" cat-file blob {} | sha256sum | cut -d' ' -f1)
python3 - "$S/laneH/.ufo/evidence/round-93/c1/census-mutants.json" "$S/fleet2" "$HC" "$GSHA" <<'PY'
import json, sys
p, repo, commit, sha = sys.argv[1:5]
s = json.load(open(p))
s["gate"]["repo"] = repo
s["gate"]["commit"] = commit
s["gate"]["sha256"] = sha
json.dump(s, open(p, "w"), indent=1)
PY
git -C "$S/laneH" add -A && git -C "$S/laneH" -c user.name=t -c user.email=t@t commit -q -m "spec repointed at probe fleet"
RH=$(git -C "$S/laneH" rev-parse HEAD)
mkdir -p "$S/wH"
python3 -I "$MEAS" --repo "$S/laneH" --rev "$RH" --work "$S/wH" >"$S/h1.log" 2>&1
probe "H1.rc" "$?"
probe "H1.conjuncts-pin-pins-green" "$(grep '^C1_CONJUNCTS' "$S/h1.log" | tr ' ' '\n' | grep -E '^(pin|pins|green)=' | tr '\n' ' ')"
probe "H1.PASS-line" "$(grep '^C1_R93_PASS' "$S/h1.log")"
probe "H1.executed-gate-bytes" "$(grep -l PROBE_MARKER_H1 "$S/wH/pristine/scripts/sources-census.sh" 2>/dev/null && echo 'MARKER PRESENT - the unpinned gate WAS executed' || echo 'marker absent')"
probe "H1.pins-conjunct-note" "$(grep -c 'PROBE_MARKER_H1' "$S/h1.log" 2>/dev/null) marker mentions in stdout"

sec "H2 ambient GIT_DIR (a clone of the lane) vs the driver's toplevel guard"
git clone -q --shared --no-checkout "$LANE" "$S/hij2" 2>/dev/null
git -C "$S/hij2" checkout -q --detach "$REV" 2>/dev/null
mkdir -p "$S/wH2"
( cd "$S" && GIT_DIR="$S/hij2/.git" python3 -I "$CTRL" --lane "$LANE" --rev "$REV" \
   --base "$BASE" --work "$S/wH2" --outdir "$S/oH2" --only pos-real --jobs 1 ) >"$S/h2.log" 2>&1
probe "H2.driver-rc" "$?"
probe "H2.log-tail" "$(tail -3 "$S/h2.log" | tr '\n' '|')"
probe "H2.hij2-commits-beyond-lane-tip" "$(git -C "$S/hij2" log --oneline 2>/dev/null | grep -c 'r93 control')"
probe "H2.hij2-has-r93-control-commit" "$(git -C "$S/hij2" log --oneline --all 2>/dev/null | grep -c 'r93 control pos-real')"
probe "H2.receipts" "$(ls -A "$S/oH2" 2>/dev/null | tr '\n' ' ')"
probe "H2.LANE-refs-replace" "$(git -C "$LANE" replace -l | tr '\n' ' ')"

sec "H3 ambient GIT_INDEX_FILE redirect (re-test, clean)"
git init -q "$S/idx3" && git -C "$S/idx3" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
git clone -q --shared "$S/idx3" "$S/idx3c" 2>/dev/null
echo hello > "$S/idx3c/f.txt"
GIT_INDEX_FILE="$S/redirected.index" git -C "$S/idx3c" add -A 2>"$S/h3.err"
probe "H3.add-rc" "$?"
probe "H3.redirected-index-created" "$( [ -f "$S/redirected.index" ] && echo YES || echo no )"
probe "H3.clone-real-index-touched" "$( [ -f "$S/idx3c/.git/index" ] && echo yes || echo no )"
probe "H3.stderr" "$(head -1 "$S/h3.err")"

sec "H4 driver --work '' in an empty cwd"
mkdir -p "$S/cwdH4"
( cd "$S/cwdH4" && python3 -I "$CTRL" --lane "$LANE" --rev "$REV" --base "$BASE" \
    --work "" --outdir "$S/oH4" --only nowork-base --jobs 1 ) >"$S/h4.log" 2>&1
probe "H4.rc" "$?"
probe "H4.cwdH4-tree" "$(find "$S/cwdH4" -maxdepth 2 2>/dev/null | head -10 | tr '\n' ' ')"

sec "H5 receipts: instrument-digest provenance across all 35"
n_no_digest=0
for f in "$LANE/.ufo/evidence/round-93/pre-freeze/controls"/*.out; do
  grep -qi 'sha256' "$f" || n_no_digest=$((n_no_digest+1))
done
probe "H5.receipts-without-any-digest" "$n_no_digest of $(ls "$LANE/.ufo/evidence/round-93/pre-freeze/controls"/*.out | wc -l)"
probe "H5.summary-references-digest" "$(grep -ci 'sha256' "$LANE/.ufo/evidence/round-93/pre-freeze/controls/C1-summary.txt" || true)"

printf '\n===== done =====\n'
