#!/usr/bin/env bash
# Independent replication of frozen measure.py fixture construction for ONE cell:
#   path = 'tools/-runner.py'  (PATHS[3] in measure.py)
# Builds all six candidate revisions for that path, per measure.py lines.
set -euo pipefail
BASE=/fast/scratch/hyaku/tameshi-r59/T59W1S21
export TMPDIR="$BASE"
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_CONFIG_NOSYSTEM=1
REPO="$BASE/fixture"
REL='tools/-runner.py'
rm -rf "$REPO"
mkdir -p "$REPO/tools"
cd "$BASE"

git -C "$REPO" init -q
TOP="$(git -C "$REPO" rev-parse --show-toplevel)"
[ "$(realpath "$TOP")" = "$(realpath "$REPO")" ] || { echo "FATAL fixture root mismatch: $TOP"; exit 9; }
echo "fixture-root-ok: $(realpath "$TOP")"

commit() {
  git -C "$REPO" -c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false commit -qm fixture
  git -C "$REPO" rev-parse HEAD
}

# trusted: original source content
printf 'print("real executor")\n' > "$REPO/$REL"
git -C "$REPO" add -- "$REL"
TRUSTED="$(commit)"; echo "trusted=$TRUSTED"

# changed: forged content
printf 'print("forged success")\n' > "$REPO/$REL"
git -C "$REPO" add -- "$REL"
CHANGED="$(commit)"; echo "changed=$CHANGED"

# missing: source deleted (git add -u, exactly as measure.py)
rm "$REPO/$REL"
git -C "$REPO" add -u
MISSING="$(commit)"; echo "missing=$MISSING"

# unrelated: source restored byte-identical + unrelated.txt added
printf 'print("real executor")\n' > "$REPO/$REL"
printf 'unrelated change\n' > "$REPO/unrelated.txt"
git -C "$REPO" add -- "$REL" unrelated.txt
UNRELATED="$(commit)"; echo "unrelated=$UNRELATED"

# unresolvable: synthetic '0'*40 (no commit)
echo "unresolvable=0000000000000000000000000000000000000000"

# symlink: source replaced by dangling symlink to elsewhere.py
rm "$REPO/$REL"
ln -s elsewhere.py "$REPO/$REL"
git -C "$REPO" add -- "$REL"
SYMLINK="$(commit)"; echo "symlink=$SYMLINK"

printf '%s\n' "$TRUSTED" "$CHANGED" "$MISSING" "$UNRELATED" "$SYMLINK" > "$BASE/commits.txt"
