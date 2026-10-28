#!/bin/bash
# T54W1Read01 receipts: the three-arm probe of the seven strict_scratch_root()
# callers at C0, plus the two non-selftest paths.
#
# usage: probe-arms.sh CLONE_AT_C0 WORKDIR
#   CLONE_AT_C0  a `git clone --shared` of the lane checked out at
#                59c38109bf119d0e9d4f878644a82babc937bc1e
#   WORKDIR      scratch dir for the captured streams and the env-diff contract
#
# Read-only against the lane; writes only under WORKDIR.
set -u
CLONE=$(cd "$1" && pwd) || exit 2
W=$2
mkdir -p "$W" || exit 2
C0=59c38109bf119d0e9d4f878644a82babc937bc1e
test "$(git -C "$CLONE" rev-parse HEAD)" = "$C0" || { echo "clone not at C0"; exit 2; }
cd "$CLONE" || exit 2
export PYTHONDONTWRITEBYTECODE=1

run () {  # run TAG TMPDIR_VALUE TOOL ARG
  local tag=$1 tv=$2 tool=$3 arg=$4
  env TMPDIR="$tv" timeout 300 python3 "tools/$tool.py" "$arg" \
      > "$W/$tag.out" 2> "$W/$tag.err"
  local rc=$?
  local tb=$(grep -c 'Traceback' "$W/$tag.err" || true)
  local named=$(cat "$W/$tag.out" "$W/$tag.err" | grep -c 'could-not-evaluate' || true)
  echo "$tag rc=$rc traceback_lines=$tb could_not_evaluate_lines=$named"
}

echo "## arm 1: TMPDIR set but unusable (a path that is not a directory)"
for spec in "registry-check:--selftest" "env-diff:--selftest" \
            "bash-witness-study:selftest" "evidence-disposition:--selftest" \
            "pin-disposition:--selftest" "context-capture:--selftest" \
            "repeat-control:--selftest"; do
  tool=${spec%%:*}; arg=${spec##*:}
  run "unusable-$tool" /nonexistent-t54-xyz "$tool" "$arg"
done

echo "## arm 2: TMPDIR empty (declared unset)"
for spec in "registry-check:--selftest" "env-diff:--selftest" \
            "bash-witness-study:selftest" "evidence-disposition:--selftest" \
            "pin-disposition:--selftest" "context-capture:--selftest" \
            "repeat-control:--selftest"; do
  tool=${spec%%:*}; arg=${spec##*:}
  run "empty-$tool" "" "$tool" "$arg"
done

echo "## non-selftest path 1: registry-check --rev at C0 (conforms: rc 2)"
env TMPDIR=/nonexistent-t54-xyz timeout 300 python3 tools/registry-check.py \
    --root "$CLONE" --rev "$C0" > "$W/nonself-registry-check.out" 2> "$W/nonself-registry-check.err"
echo "registry-check --rev rc=$? first_stdout=$(head -1 "$W/nonself-registry-check.out")"

echo "## non-selftest path 2: env-diff --contract (documented usage) at C0"
SHA=$(git -C "$CLONE" show "$C0:tools/env-diff.py" | sha256sum | cut -d' ' -f1)
REPO=$(basename "$CLONE")
python3 - "$W" "$REPO" "$C0" "$SHA" <<'PY'
import json, sys
w, repo, rev, sha = sys.argv[1:5]
contract = {"surfaces": [{"name": "lane-envdiff", "repo": repo, "rev": rev,
                          "path": "tools/env-diff.py", "interp": "bash",
                          "blob_sha256": sha}]}
open(w + "/envdiff-contract.json", "w").write(json.dumps(contract))
PY
env TMPDIR=/nonexistent-t54-xyz timeout 300 python3 tools/env-diff.py \
    --contract "$W/envdiff-contract.json" --out "$W/envdiff-out.json" \
    --fleet-root "$(dirname "$CLONE")" \
    > "$W/nonself-envdiff.out" 2> "$W/nonself-envdiff.err"
echo "env-diff --contract rc=$? traceback_lines=$(grep -c Traceback "$W/nonself-envdiff.err" || true) stdout_bytes=$(wc -c < "$W/nonself-envdiff.out")"
tail -2 "$W/nonself-envdiff.err"
