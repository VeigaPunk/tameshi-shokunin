#!/usr/bin/env bash
# False-BOUND variant: attacker repo MIRRORS the victim (contains trusted commit)
# plus attacker's own clean HEAD. Run after build-fixtures.sh.
set -euo pipefail
ROOT="${1:?usage: build-mirror.sh SCRATCH_ROOT}"
M="$ROOT/fixtures/attacker-mirror"
V="$ROOT/fixtures/victim"
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid
export GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
set -a; . "$ROOT/fixtures/ids.env"; set +a

rm -rf "$M"
git clone -q "$V" "$M"
git -C "$M" checkout -q "$TRUSTED"
echo 'print("real executor")' > "$M/tools/runner.py"
git -C "$M" add -- tools/runner.py
git -C "$M" -c commit.gpgsign=false commit -q --allow-empty -m clean-mirror-head
AMH=$(git -C "$M" rev-parse HEAD)
echo "ATTACKER_MIRROR=$M" >> "$ROOT/fixtures/ids.env"
echo "ATTACKER_MIRROR_HEAD=$AMH" >> "$ROOT/fixtures/ids.env"
echo "attacker_mirror_head=$AMH"
