#!/usr/bin/env bash
# GIT_DIR poisoning probes against naive vs hardened reference oracles.
set -uo pipefail
ROOT="${1:?usage: run-attacks.sh SCRATCH_ROOT}"
SEAT_STAGE="${2:?usage: run-attacks.sh SCRATCH_ROOT SEAT_STAGE_DIR}"
OUT="$ROOT/transcripts"
mkdir -p "$OUT"
set -a; . "$ROOT/fixtures/ids.env"; set +a
NAIVE="$SEAT_STAGE/adversarial/git-dir/naive-tool.py"
HARD="$SEAT_STAGE/adversarial/git-dir/hardened-tool.py"
P=tools/runner.py
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
run() { # name env-assignments... -- cmd...
  local name="$1"; shift
  local envs=()
  while [ "$1" != "--" ]; do envs+=("$1"); shift; done
  shift
  {
    echo "=== $name"
    printf '$'; printf ' %q' "${envs[@]}" "$@"; echo
    env "${envs[@]}" "$@"
    echo "exit=$?"
  } > "$OUT/$name.log" 2>&1
  tail -n 4 "$OUT/$name.log"
  echo "---"
}

echo "## git version"; git --version

run P0-gitdir-overrides-dashC "GIT_DIR=$ATTACKER/.git" -- git -C "$VICTIM" rev-parse --show-toplevel

run T1-naive-clean-fullhash -- python3 -I "$NAIVE" --repo "$VICTIM" --trusted "$TRUSTED" --candidate "$CANDIDATE" --path "$P"

run T2-naive-poisoned-fullhash "GIT_DIR=$ATTACKER/.git" -- python3 -I "$NAIVE" --repo "$VICTIM" --trusted "$TRUSTED" --candidate "$CANDIDATE" --path "$P"

run T3-naive-poisoned-ref-HEAD "GIT_DIR=$ATTACKER/.git" -- python3 -I "$NAIVE" --repo "$VICTIM" --trusted "$TRUSTED" --candidate HEAD --path "$P"

run T4-hardened-poisoned-ref-HEAD "GIT_DIR=$ATTACKER/.git" -- python3 -I "$HARD" --repo "$VICTIM" --trusted "$TRUSTED" --candidate HEAD --path "$P"

run T5-hardened-poisoned-fullhash "GIT_DIR=$ATTACKER/.git" -- python3 -I "$HARD" --repo "$VICTIM" --trusted "$TRUSTED" --candidate "$CANDIDATE" --path "$P"

run T6-hardened-clean-fullhash -- python3 -I "$HARD" --repo "$VICTIM" --trusted "$TRUSTED" --candidate "$CANDIDATE" --path "$P"

run T7-naive-poisoned-nonexistent-gitdir "GIT_DIR=$ROOT/fixtures/no-such-gitdir" -- python3 -I "$NAIVE" --repo "$VICTIM" --trusted "$TRUSTED" --candidate "$CANDIDATE" --path "$P"

# relative GIT_DIR resolves against process cwd, not -C target; demonstrate from attacker dir:
{
  echo "=== T8-naive-relative-gitdir-from-attacker-cwd"
  echo "\$ (cd attacker && GIT_DIR=.git python3 -I naive --repo \$VICTIM ...)"
  (cd "$ATTACKER" && env "GIT_DIR=.git" python3 -I "$NAIVE" --repo "$VICTIM" --trusted "$TRUSTED" --candidate HEAD --path "$P")
  echo "exit=$?"
} > "$OUT/T8-naive-relative-gitdir-from-attacker-cwd.log" 2>&1
tail -n 4 "$OUT/T8-naive-relative-gitdir-from-attacker-cwd.log"; echo "---"

echo "transcripts in $OUT"
