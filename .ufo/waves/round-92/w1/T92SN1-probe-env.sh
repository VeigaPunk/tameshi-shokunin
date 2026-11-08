#!/usr/bin/env bash
# T92SN1 probe (read-only wrt lane/fleet; all writes under scratch).
# Q1: does an ambient GIT_DIR make a mutating `git -C <scratch clone>` write
#     OUTSIDE the scratch clone (the 2026-11-06 `git -C ""` fleet-root class)?
# Q2: does ambient git config (core.hooksPath) cause code execution at
#     `git commit` time inside the control driver's fixture clones?
# Q3: does `git clone --shared` fail or write elsewhere under GIT_DIR?
set -u
S=/fast/scratch/hyaku/tameshi-r92/T92SN1
mkdir -p "$S"
cd "$S" || exit 1
rm -rf envprobe && mkdir envprobe && cd envprobe || exit 1

export HOME="$S/envprobe/home"; mkdir -p "$HOME"
export GIT_CONFIG_GLOBAL="$HOME/.gitconfig"
mkdir -p "$S/envprobe/hooks"
printf '#!/bin/sh\necho HOOK-EXECUTED > %s/envprobe/hook.marker\n' "$S" > "$S/envprobe/hooks/pre-commit"
chmod +x "$S/envprobe/hooks/pre-commit"
printf '[core]\n\thooksPath = %s/envprobe/hooks\n' "$S" > "$HOME/.gitconfig"

git init -q victim
git -C victim config user.name ctl
git -C victim config user.email ctl@fixture.invalid
echo base > victim/f
git -C victim add -A
git -C victim commit -qm base
VICTIM_HEAD_BEFORE=$(git -C victim rev-parse HEAD)

git clone -q --shared --no-checkout victim clone
git -C clone checkout -q --detach HEAD
echo "clone toplevel: $(git -C clone rev-parse --show-toplevel)"

echo "=== Q1a: ambient GIT_DIR + 'git -C clone add -A' ==="
GIT_DIR="$S/envprobe/victim/.git" git -C "$S/envprobe/clone" add -A 2>&1 | head -3
echo "rc=${PIPESTATUS[0]}"
echo "=== Q1b: ambient GIT_DIR + 'git -C clone commit' ==="
echo new > clone/g
GIT_DIR="$S/envprobe/victim/.git" git -C "$S/envprobe/clone" -c user.name=ctl -c user.email=ctl@fixture.invalid commit -qm leak 2>&1 | head -5
echo "victim HEAD before: $VICTIM_HEAD_BEFORE"
echo "victim HEAD after : $(git -C victim rev-parse HEAD)"
echo "victim log:"; git -C victim log --oneline | head -5
echo "victim status:"; git -C victim status --porcelain | head -5
echo "clone HEAD: $(git -C clone rev-parse HEAD 2>&1)"
echo "clone log:"; git -C clone log --oneline | head -5

echo "=== Q1c: ambient GIT_DIR + 'git -C clone replace' (replace-ref creation) ==="
OID=$(git -C clone rev-parse HEAD:f)
GIT_DIR="$S/envprobe/victim/.git" git -C "$S/envprobe/clone" replace "$OID" "$OID" 2>&1 | head -3
echo "victim replace -l: [$(git -C victim replace -l 2>&1 | tr '\n' ' ')]"
echo "clone replace -l : [$(git -C clone replace -l 2>&1 | tr '\n' ' ')]"

echo "=== Q1d: ambient GIT_INDEX_FILE + 'git -C clone add -A' ==="
rm -f "$S/envprobe/idx"
GIT_INDEX_FILE="$S/envprobe/idx" git -C "$S/envprobe/clone" add -A 2>&1 | head -3
echo "index landed outside clone: $([ -f "$S/envprobe/idx" ] && echo YES || echo NO)"

echo "=== Q3: 'git clone --shared' under ambient GIT_DIR ==="
GIT_DIR="$S/envprobe/victim/.git" git clone -q --shared --no-checkout victim clone2 2>&1 | head -3
echo "clone2 exists: $([ -d "$S/envprobe/clone2/.git" ] && echo YES || echo NO)"

echo "=== Q2: hook execution at commit time in the fixture clone ==="
rm -f "$S/envprobe/hook.marker"
git -C clone add -A
git -C clone -c user.name=ctl -c user.email=ctl@fixture.invalid commit -qm hooktest 2>&1 | head -3
echo "hook.marker: $([ -f "$S/envprobe/hook.marker" ] && cat "$S/envprobe/hook.marker" || echo NOT-EXECUTED)"
