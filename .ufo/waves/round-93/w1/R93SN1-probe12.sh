#!/usr/bin/env bash
# R93SN1 probe 12: the empty-gate.repo fallback - what exactly does the counter read
# and execute when the SPEC says gate.repo == ""?
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe12.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
MEAS="$LANE/.ufo/evidence/round-93/c1/measure-v93.py"
probe() { printf 'PROBE %-52s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "N1 cwd repo holds a gate on the INDEX (staged, uncommitted) - is it executed?"
# The cwd repo: gate script is STAGED (index only), never committed.
git init -q "$S/cwd"
mkdir -p "$S/cwd/scripts/fixtures/sources-census"
printf 'fixture\n' > "$S/cwd/scripts/fixtures/sources-census/root.txt"
printf '#!/usr/bin/env bash\n# PROBE_MARKER_N1 index-gate-executed\ncase "$1" in selftest) echo "selftest ok";; esac\n' \
  > "$S/cwd/scripts/sources-census.sh"
chmod +x "$S/cwd/scripts/sources-census.sh"
git -C "$S/cwd" add -A
git -C "$S/cwd" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
# NOTE: scripts/sources-census.sh is STAGED ONLY - not committed.
probe "N1.committed-has-gate" "$(git -C "$S/cwd" cat-file -e HEAD:scripts/sources-census.sh 2>/dev/null && echo yes || echo 'no (index only)')"
probe "N1.index-has-gate" "$(git -C "$S/cwd" cat-file -e :scripts/sources-census.sh 2>/dev/null && echo yes || echo no)"
git -C "$S/cwd" rev-parse HEAD > "$S/cwd/../emptyrev" 2>/dev/null
# a lane whose spec names gate.repo="" and gate.commit=""
git init -q "$S/lane"
mkdir -p "$S/lane/.ufo/evidence/round-93/c1"
python3 - "$S/lane/.ufo/evidence/round-93/c1/census-mutants.json" <<'PY'
import json, sys
json.dump({"schema": 1, "gate": {"repo": "", "commit": "", "path": "scripts/sources-census.sh",
                                 "sha256": "0"*64, "fixtures": "scripts/fixtures/sources-census"},
           "timeout_s": 2, "runs_per_verdict": 1, "mutants": []}, open(sys.argv[1], "w"))
PY
git -C "$S/lane" add -A && git -C "$S/lane" -c user.name=t -c user.email=t@t commit -q -m spec
RL=$(git -C "$S/lane" rev-parse HEAD)
mkdir -p "$S/w"
( cd "$S/cwd" && python3 -I "$MEAS" --repo "$S/lane" --rev "$RL" --work "$S/w" ) >"$S/n1.log" 2>&1
probe "N1.counter-output" "$(head -2 "$S/n1.log" | tr '\n' '|')"
probe "N1.blob-read-from-cwd-index" "$(grep -m1 'C1_SETUP' "$S/n1.log")"
probe "N1.did-it-execute-the-cwd-index-gate" "$(grep -q PROBE_MARKER_N1 "$S/w/pristine/scripts/sources-census.sh" 2>/dev/null && echo 'YES - the CWD repo index gate was EXECUTED' || echo 'no')"
probe "N1.written-gate-digest" "$(sha256sum "$S/w/pristine/scripts/sources-census.sh" 2>/dev/null | cut -c1-16)"
probe "N1.cwd-index-gate-digest" "$(git -C "$S/cwd" cat-file blob :scripts/sources-census.sh | sha256sum | cut -c1-16)"

sec "N2 same, but the CWD is a repo whose INDEX carries a hostile gate (no commit needed)"
git init -q "$S/cwd2"
mkdir -p "$S/cwd2/scripts/fixtures/sources-census"
printf 'fixture\n' > "$S/cwd2/scripts/fixtures/sources-census/root.txt"
printf '#!/usr/bin/env bash\n# PROBE_MARKER_N2 index-gate-executed\necho "selftest ok"\n' > "$S/cwd2/scripts/sources-census.sh"
chmod +x "$S/cwd2/scripts/sources-census.sh"
git -C "$S/cwd2" add -A
git -C "$S/cwd2" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
mkdir -p "$S/w2"
( cd "$S/cwd2" && python3 -I "$MEAS" --repo "$S/lane" --rev "$RL" --work "$S/w2" ) >"$S/n2.log" 2>&1
probe "N2.counter-output" "$(head -2 "$S/n2.log" | tr '\n' '|')"
probe "N2.executed-cwd-index-gate" "$(grep -q PROBE_MARKER_N2 "$S/w2/pristine/scripts/sources-census.sh" 2>/dev/null && echo YES || echo no)"

printf '\n===== done =====\n'
