#!/usr/bin/env bash
# T91S2 — replace-ref fixture: demonstrate, on this host's git, the mechanics
# git-replace(1) documents and the C1 counter's setup gate depends on.
#
# READ-ONLY with respect to the lane, the fleet root and every sibling lane
# repo. Every git repository it creates lives under the seat scratch dir and
# is deleted on exit (trap). The lane's own repos are only *read* (cloned with
# --shared into the scratch dir).
#
# Usage:  bash T91S2-replace-fixture.sh
# Env:    SCRATCH (default /fast/scratch/hyaku/tameshi-r91/T91S2)
#
# What it shows:
#   1. `git replace <obj> <repl>` creates a ref under refs/replace/ named for
#      the replaced object (git-replace(1) DESCRIPTION).
#   2. `git replace -l` lists that ref — this is exactly what the sealed C1
#      counter runs and refuses on (measure-v91.py: `git replace -l`).
#   3. GIT_NO_REPLACE_OBJECTS=1 makes `git cat-file` read the ORIGINAL object,
#      but does NOT hide the ref from `git replace -l` — so the counter's
#      "refuse a non-empty `git replace -l`" gate is not redundant with the
#      environment variable.
#   4. Running the sealed C1 counter against a clone that carries such a ref
#      refuses at setup with `replace-refs-present:lane` (exit 2), matching the
#      frozen pre-freeze control `.ufo/evidence/round-91/pre-freeze/controls/
#      V4-replace.out`.
set -u

SCRATCH="${SCRATCH:-/fast/scratch/hyaku/tameshi-r91/T91S2}"
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
COUNTER="$LANE/.ufo/evidence/round-91/c1/measure-v91.py"

mkdir -p "$SCRATCH"
ROOT="$(mktemp -d -p "$SCRATCH" fx.XXXXXX)"
trap 'rm -rf -- "$ROOT"' EXIT

export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
export GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@fixture.invalid
export GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@fixture.invalid

echo "=== 1. scratch fixture repo ==="
D="$ROOT/fx"
git -C "$ROOT" init -q "$D" 2>/dev/null || git init -q "$D"
top="$(git -C "$D" rev-parse --show-toplevel)"
if [ "$top" != "$D" ]; then echo "FAIL toplevel=$top != $D"; exit 1; fi
echo "toplevel=$top"

printf 'original\n' > "$D/a.txt"
git -C "$D" add a.txt
git -C "$D" commit -qm base
blob_a="$(git -C "$D" rev-parse HEAD:a.txt)"
printf 'replaced\n' > "$D/b.txt"
blob_b="$(git -C "$D" hash-object -w b.txt)"
echo "blob_a(replaced)   =$blob_a"
echo "blob_b(replacement)=$blob_b"

git -C "$D" replace "$blob_a" "$blob_b"

echo "=== 2. git replace -l (what the counter reads) ==="
git -C "$D" replace -l; echo "exit=$?"
echo "=== 2b. the ref itself ==="
git -C "$D" for-each-ref refs/replace --format='%(refname) %(objectname)'

echo "=== 3a. cat-file WITHOUT GIT_NO_REPLACE_OBJECTS ==="
git -C "$D" cat-file -p "$blob_a"
echo "=== 3b. cat-file WITH GIT_NO_REPLACE_OBJECTS=1 ==="
GIT_NO_REPLACE_OBJECTS=1 git -C "$D" cat-file -p "$blob_a"
echo "=== 3c. git replace -l WITH GIT_NO_REPLACE_OBJECTS=1 (still lists) ==="
GIT_NO_REPLACE_OBJECTS=1 git -C "$D" replace -l; echo "exit=$?"

echo "=== 4. sealed C1 counter against a clone carrying the replace ref ==="
CLONE="$ROOT/clone"
git clone --shared -q "$LANE" "$CLONE"
ctop="$(git -C "$CLONE" rev-parse --show-toplevel)"
if [ "$ctop" != "$CLONE" ]; then echo "FAIL clone toplevel=$ctop != $CLONE"; exit 1; fi
cb="$(printf 'orig\n' | git -C "$CLONE" hash-object -w --stdin)"
cr="$(printf 'repl\n' | git -C "$CLONE" hash-object -w --stdin)"
git -C "$CLONE" replace "$cb" "$cr"
echo "clone replace -l:"; git -C "$CLONE" replace -l
W="$ROOT/work"
mkdir -p "$W"
python3 -I "$COUNTER" --repo "$CLONE" --rev HEAD --work "$W" 2>&1 | tail -4
echo "counter_exit=${PIPESTATUS[0]}"
