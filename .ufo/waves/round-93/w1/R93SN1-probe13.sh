#!/usr/bin/env bash
# R93SN1 probe 13: gate.repo == "" with a VALID commit -> does the counter read the
# gate bytes out of the PROCESS CWD repo (the 2026-11-06 fleet-incident shape) and
# EXECUTE them?
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe13.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
MEAS="$LANE/.ufo/evidence/round-93/c1/measure-v93.py"
probe() { printf 'PROBE %-54s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "O1 gate.repo='' + valid commit in the CWD repo -> CWD gate read + executed?"
git init -q "$S/cwd"
mkdir -p "$S/cwd/scripts/fixtures/sources-census"
printf 'fixture\n' > "$S/cwd/scripts/fixtures/sources-census/root.txt"
printf '#!/usr/bin/env bash\n# PROBE_MARKER_O1 cwd-repo-gate-executed\ncase "$1" in selftest) echo "selftest ok";; esac\n' \
  > "$S/cwd/scripts/sources-census.sh"
chmod +x "$S/cwd/scripts/sources-census.sh"
git -C "$S/cwd" add -A && git -C "$S/cwd" -c user.name=t -c user.email=t@t commit -q -m gate
CC=$(git -C "$S/cwd" rev-parse HEAD)
CSHA=$(git -C "$S/cwd" cat-file blob HEAD:scripts/sources-census.sh | sha256sum | cut -d' ' -f1)
probe "O1.cwd-commit" "$CC"
probe "O1.cwd-gate-sha" "$CSHA"

git init -q "$S/lane"
mkdir -p "$S/lane/.ufo/evidence/round-93/c1"
python3 - "$S/lane/.ufo/evidence/round-93/c1/census-mutants.json" "$CC" "$CSHA" <<'PY'
import json, sys
p, commit, sha = sys.argv[1:4]
json.dump({"schema": 1, "gate": {"repo": "", "commit": commit, "path": "scripts/sources-census.sh",
                                 "sha256": sha, "fixtures": "scripts/fixtures/sources-census"},
           "timeout_s": 2, "runs_per_verdict": 1, "mutants": []}, open(p, "w"))
PY
git -C "$S/lane" add -A && git -C "$S/lane" -c user.name=t -c user.email=t@t commit -q -m spec
RL=$(git -C "$S/lane" rev-parse HEAD)
mkdir -p "$S/w"
( cd "$S/cwd" && python3 -I "$MEAS" --repo "$S/lane" --rev "$RL" --work "$S/w" ) >"$S/o1.log" 2>&1
probe "O1.counter-output" "$(head -2 "$S/o1.log" | tr '\n' '|')"
probe "O1.conjuncts" "$(grep '^C1_CONJUNCTS' "$S/o1.log" | tr ' ' '\n' | grep -E '^(pin|pins|green|canary)=' | tr '\n' ' ')"
probe "O1.CWD-gate-executed" "$(grep -q PROBE_MARKER_O1 "$S/w/pristine/scripts/sources-census.sh" 2>/dev/null && echo 'YES - gate bytes came from the CWD repo and were EXECUTED' || echo no)"
probe "O1.executed-gate-digest" "$(sha256sum "$S/w/pristine/scripts/sources-census.sh" 2>/dev/null | cut -c1-16) vs cwd $CSHA" 
probe "O1.PASS" "$(grep '^C1_R93_PASS' "$S/o1.log")"

sec "O2 the same run from a NON-repo cwd (fleet root is a repo; a plain dir is not)"
mkdir -p "$S/plain"
( cd "$S/plain" && python3 -I "$MEAS" --repo "$S/lane" --rev "$RL" --work "$S/w2" ) >"$S/o2.log" 2>&1
probe "O2.counter-output" "$(head -2 "$S/o2.log" | tr '\n' '|')"

sec "O3 does the driver's clone_at guard survive a repo whose toplevel differs?"
git init -q "$S/a"; git -C "$S/a" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
mkdir -p "$S/b"; git init -q "$S/b"; git -C "$S/b" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
probe "O3.nested-repo-toplevel" "$(git -C "$S/b" rev-parse --show-toplevel | sed "s|$S|\$S|g")"

printf '\n===== done =====\n'
