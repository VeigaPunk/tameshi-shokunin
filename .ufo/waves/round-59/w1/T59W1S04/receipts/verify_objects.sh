#!/usr/bin/env bash
# Object-level verification of the fixture for cell tools/runner.py/unrelated
set -euo pipefail
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
cd /fast/scratch/hyaku/tameshi-r59/T59W1S04/fixture
. /fast/scratch/hyaku/tameshi-r59/T59W1S04/versions.env

echo "== ls-tree tools/runner.py at each version =="
for v in TRUSTED CHANGED MISSING UNRELATED SYMLINK; do
  eval "c=\$$v"
  printf '%-12s %s : ' "$v" "$c"
  git ls-tree "$c" -- tools/runner.py || true
done

echo
echo "== blob hashes for tools/runner.py =="
for v in TRUSTED CHANGED UNRELATED; do
  eval "c=\$$v"
  printf '%-12s ' "$v"
  git rev-parse "$c:tools/runner.py"
done

echo
echo "== content at UNRELATED:tools/runner.py =="
git cat-file -p UNRELATED_PLACEHOLDER 2>/dev/null || git cat-file -p "$UNRELATED:tools/runner.py"

echo
echo "== diff TRUSTED..UNRELATED (name-status) =="
git diff --name-status "$TRUSTED" "$UNRELATED"

echo
echo "== diff TRUSTED..CHANGED (name-status + blob) =="
git diff --name-status "$TRUSTED" "$CHANGED"

echo
echo "== full-tree diff TRUSTED..UNRELATED must be empty for declared path =="
git diff "$TRUSTED" "$UNRELATED" -- tools/runner.py | wc -l

echo
echo "== commit chain =="
git log --oneline --all --graph

echo
echo "== unresolvable rev-parse check =="
git rev-parse --verify "$UNRESOLVABLE^{commit}" && echo "UNEXPECTED-RESOLVABLE" || echo "UNRESOLVABLE-FAILS-AS-EXPECTED rc=$?"
