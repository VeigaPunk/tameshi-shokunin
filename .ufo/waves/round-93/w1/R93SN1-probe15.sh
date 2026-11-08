#!/usr/bin/env bash
# R93SN1 probe 15: final confirmations.
#   Q1 under ambient GIT_DIR, does 'git -C <dir> replace' write the ref into the
#      GIT_DIR repo (i.e. can a replace ref be created outside the scratch clone)?
#   Q2 does the counter's os.path.join(dest, gate_path) escape when gate_path is
#      a traversal / absolute path (git is asked for the blob first)?
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe15.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
MEAS="$LANE/.ufo/evidence/round-93/c1/measure-v93.py"
probe() { printf 'PROBE %-54s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "Q1 ambient GIT_DIR: does 'git -C dir replace' create the ref in the GIT_DIR repo?"
git init -q "$S/target"; git -C "$S/target" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
git init -q "$S/other"
git -C "$S/other" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
FA=$(git -C "$S/target" rev-parse HEAD:README 2>/dev/null || git -C "$S/target" rev-parse HEAD)
FB=$(git -C "$S/target" hash-object -w --stdin <<< "x" 2>/dev/null || true)
GIT_DIR="$S/other/.git" git -C "$S/target" replace "$FA" "$FB" >/dev/null 2>&1
probe "Q1.other-repo-replace-refs" "$(git -C "$S/other" replace -l | tr '\n' ' ')"
probe "Q1.target-repo-replace-refs" "$(git -C "$S/target" replace -l | tr '\n' ' ')"
probe "Q1.verdict" "$( [ -n "$(git -C "$S/other" replace -l)" ] && echo 'replace ref landed OUTSIDE the -C dir (in the GIT_DIR repo)' || echo 'stayed in the -C dir')"

sec "Q2 gate_path traversal: git refuses the blob, so no write happens"
for gp in "../../../../tmp/evil.sh" "/tmp/evil.sh" "scripts/../scripts/sources-census.sh"; do
  out=$(git -C "$LANE" cat-file blob "855f0c1c59ee2af7f184d8de62d02cdd576eb94e:$gp" 2>&1 | head -1 | cut -c1-70)
  probe "Q2.cat-file($gp)" "$out"
done
probe "Q2.os.path.join-behaviour" "$(python3 -c "import os;print(os.path.join('/w/pristine','../../../../tmp/evil.sh'))")"
probe "Q2.join-is-normalised-by-open" "the counter writes gp = os.path.join(dest, gate_path); open(gp) resolves '..'"

sec "Q3 is the gate_path used for the WRITE the same string git validated?"
grep -n 'gate_path\|g.get("path"\|g\["path"\]' "$MEAS" | sed 's/^/    /'

sec "Q4 the counter's replace-ref seal covers the lane AND the fleet"
grep -n 'replace", "-l"\|replace-refs-present' "$MEAS" | sed 's/^/    /'

printf '\n===== done =====\n'
