#!/usr/bin/env bash
# T59W1S03 fixture driver: replicates frozen measure.py construction for
# PATHS[0] = 'tools/runner.py', all six classes, in an isolated scratch repo.
# Mirrors measure.py env: GIT_* stripped, GIT_CONFIG_GLOBAL=/dev/null,
# GIT_CONFIG_NOSYSTEM=1, user via -c flags, gpgsign off.
set -euo pipefail

SEAT=T59W1S03
SCRATCH=/fast/scratch/hyaku/tameshi-r59/$SEAT
REPO="$SCRATCH/fixture"
REL='tools/runner.py'

export GIT_CONFIG_GLOBAL=/dev/null
export GIT_CONFIG_NOSYSTEM=1
unset "${!GIT_@}" 2>/dev/null || true
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_CONFIG_NOSYSTEM=1

cd "$SCRATCH"
git -C "$REPO" init -q
root="$(git -C "$REPO" rev-parse --show-toplevel)"
[ "$(readlink -f "$root")" = "$(readlink -f "$REPO")" ] || { echo 'fixture root mismatch' >&2; exit 99; }

f="$REPO/$REL"
mkdir -p "$(dirname "$f")"

commit() {
  git -C "$REPO" -c user.name=fixture -c user.email=fixture@example.invalid \
      -c commit.gpgsign=false commit -qm fixture
  git -C "$REPO" rev-parse HEAD
}

printf 'print("real executor")\n' > "$f"
git -C "$REPO" add -- "$REL"
TRUSTED="$(commit)"

printf 'print("forged success")\n' > "$f"
git -C "$REPO" add -- "$REL"
CHANGED="$(commit)"

rm "$f"
git -C "$REPO" add -u
MISSING="$(commit)"

printf 'print("real executor")\n' > "$f"
printf 'unrelated change\n' > "$REPO/unrelated.txt"
git -C "$REPO" add -- "$REL" unrelated.txt
UNRELATED="$(commit)"

UNRESOLVABLE=0000000000000000000000000000000000000000

rm "$f"
ln -s elsewhere.py "$f"
git -C "$REPO" add -- "$REL"
SYMLINK="$(commit)"

cat > "$SCRATCH/versions.env" <<EOF
TRUSTED=$TRUSTED
CHANGED=$CHANGED
MISSING=$MISSING
UNRELATED=$UNRELATED
UNRESOLVABLE=$UNRESOLVABLE
SYMLINK=$SYMLINK
EOF
cat "$SCRATCH/versions.env"
echo "DRIVER_OK"
