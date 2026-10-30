#!/usr/bin/env bash
# Independent fixture builder for round-59 cell: path=tools/runner.py, class=unrelated
# Mirrors frozen measure.py construction exactly, single path only.
set -euo pipefail
export TMPDIR=/fast/scratch/hyaku/tameshi-r59/T59W1S04
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
cd /fast/scratch/hyaku/tameshi-r59/T59W1S04/fixture

git init -q
[ "$(git rev-parse --show-toplevel)" = "/fast/scratch/hyaku/tameshi-r59/T59W1S04/fixture" ]
echo "ROOT-OK: $(git rev-parse --show-toplevel)"
mkdir -p tools

commit() {
  git -c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false commit -qm fixture
  git rev-parse HEAD
}

printf 'print("real executor")\n' > tools/runner.py
git add -- tools/runner.py
TRUSTED=$(commit)
echo "TRUSTED=$TRUSTED"

printf 'print("forged success")\n' > tools/runner.py
git add -- tools/runner.py
CHANGED=$(commit)
echo "CHANGED=$CHANGED"

rm tools/runner.py
git add -u
MISSING=$(commit)
echo "MISSING=$MISSING"

printf 'print("real executor")\n' > tools/runner.py
printf 'unrelated change\n' > unrelated.txt
git add -- tools/runner.py unrelated.txt
UNRELATED=$(commit)
echo "UNRELATED=$UNRELATED"

# symlink and unresolvable variants for completeness of the class matrix on this path
rm tools/runner.py
ln -s elsewhere.py tools/runner.py
git add -- tools/runner.py
SYMLINK=$(commit)
echo "SYMLINK=$SYMLINK"
UNRESOLVABLE=0000000000000000000000000000000000000000
echo "UNRESOLVABLE=$UNRESOLVABLE"

printf '%s %s\n%s %s\n%s %s\n%s %s\n%s %s\n%s %s\n' \
  TRUSTED "$TRUSTED" CHANGED "$CHANGED" MISSING "$MISSING" \
  UNRELATED "$UNRELATED" SYMLINK "$SYMLINK" UNRESOLVABLE "$UNRESOLVABLE" > /fast/scratch/hyaku/tameshi-r59/T59W1S04/versions.txt
echo "WROTE versions.txt"
