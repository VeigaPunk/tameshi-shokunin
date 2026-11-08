#!/usr/bin/env bash
# T91R1 seal probe: proves GIT_NO_REPLACE_OBJECTS=1 is what makes the counter's
# reads replace-proof, and that dropping HOME does not break the read path.
# Fixture repo lives under the seat scratch dir; the lane and fleet repos are
# only read.
set -u
S=${S:-/fast/scratch/hyaku/tameshi-r91/T91R1}
mkdir -p "$S"
trap 'rm -rf -- "$D"' EXIT
D=$(mktemp -d -p "$S" fx.XXXXXX) || exit 1
git -C "$D" init -q || exit 1
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "toplevel mismatch"; exit 1; }
printf 'BAD-VERDICT\n' > "$D/gate.sh"
git -C "$D" -c user.name=ctl -c user.email=ctl@fixture.invalid add gate.sh
git -C "$D" -c user.name=ctl -c user.email=ctl@fixture.invalid commit -qm base
BAD=$(git -C "$D" rev-parse HEAD:gate.sh)
GOOD=$(printf 'GOOD-VERDICT\n' | git -C "$D" hash-object -w --stdin)
git -C "$D" replace "$BAD" "$GOOD"
SEAL=(env -i PATH=/usr/bin:/bin GIT_NO_REPLACE_OBJECTS=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null)
echo "replace_l=$(git -C "$D" replace -l)"
echo "unsealed_cat_file=$(git -C "$D" cat-file blob HEAD:gate.sh)"
echo "sealed_cat_file=$("${SEAL[@]}" git -C "$D" cat-file blob HEAD:gate.sh)"
echo "sealed_archive=$("${SEAL[@]}" git -C "$D" archive --format=tar HEAD | tar -xO gate.sh)"
echo "sealed_archive_rc=$?"
"${SEAL[@]}" git -C "$D" cat-file blob HEAD:gate.sh >/dev/null; echo "sealed_no_HOME_rc=$?"
