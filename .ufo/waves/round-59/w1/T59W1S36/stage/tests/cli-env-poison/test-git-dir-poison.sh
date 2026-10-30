#!/usr/bin/env bash
# Exact CLI test: executor-source-pin must be immune to GIT_DIR poisoning.
# Usage: test-git-dir-poison.sh /path/to/executor-source-pin.py
# Builds scratch victim + mirror fixtures, asserts:
#   1. clean run on forged candidate           -> exit 1 EXECUTOR_SOURCE_DRIFT
#   2. GIT_DIR-poisoned run, ref candidate      -> exit 1 DRIFT (NOT 0 BOUND, NOT 2)
#   3. GIT_DIR-poisoned run, full-hash candidate-> exit 1 DRIFT (no verdict flip to 2)
#   4. GIT_DIR-poisoned run on equal repo       -> exit 0 BOUND (poison breaks nothing legit)
set -euo pipefail
TOOL="${1:?usage: test-git-dir-poison.sh TOOL}"
TROOT="${TMPDIR:-/tmp}/executor-source-pin-env-poison.$$"
mkdir -p "$TROOT"
trap 'rm -rf "$TROOT"' EXIT
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid
export GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid

V="$TROOT/victim"; M="$TROOT/mirror"
mkdir -p "$V/tools"
printf 'print("real executor")\n' > "$V/tools/runner.py"
git -C "$V" init -q && git -C "$V" add -- tools/runner.py && git -C "$V" -c commit.gpgsign=false commit -qm trusted
TRUSTED=$(git -C "$V" rev-parse HEAD)
printf 'print("forged success")\n' > "$V/tools/runner.py"
git -C "$V" add -- tools/runner.py && git -C "$V" -c commit.gpgsign=false commit -qm forged
CANDIDATE=$(git -C "$V" rev-parse HEAD)
git clone -q "$V" "$M" && git -C "$M" checkout -q "$TRUSTED"
git -C "$M" -c commit.gpgsign=false commit -q --allow-empty -m clean-mirror-head

fails=0
check() { # name expected_exit expected_token
  local name="$1" want_exit="$2" want_token="$3"
  local log="$TROOT/$name.log"
  if [ ! -f "$log" ]; then echo "FAIL $name: no run log"; fails=$((fails+1)); return; fi
  local got_exit token
  got_exit=$(tail -n1 "$log" | sed 's/exit=//')
  if [ "$got_exit" != "$want_exit" ]; then
    echo "FAIL $name: exit=$got_exit want=$want_exit"; fails=$((fails+1)); return
  fi
  if ! grep -q "$want_token" "$log"; then
    echo "FAIL $name: token $want_token absent"; fails=$((fails+1)); return
  fi
  echo "PASS $name (exit=$got_exit, $want_token)"
}
rune() { # name env... -- args...
  local name="$1"; shift
  local envs=()
  while [ "$1" != "--" ]; do envs+=("$1"); shift; done
  shift
  { printf '$'; printf ' %q' "${envs[@]}" "$@"; echo
    env "${envs[@]}" "$@"; echo "exit=$?"
  } > "$TROOT/$name.log" 2>&1 || true
}

rune clean -- python3 -I "$TOOL" --repo "$V" --trusted "$TRUSTED" --candidate "$CANDIDATE" --path tools/runner.py
rune poisoned-ref "GIT_DIR=$M/.git" -- python3 -I "$TOOL" --repo "$V" --trusted "$TRUSTED" --candidate HEAD --path tools/runner.py
rune poisoned-full "GIT_DIR=$M/.git" -- python3 -I "$TOOL" --repo "$V" --trusted "$TRUSTED" --candidate "$CANDIDATE" --path tools/runner.py
rune poisoned-equal "GIT_DIR=$M/.git" -- python3 -I "$TOOL" --repo "$V" --trusted "$TRUSTED" --candidate "$TRUSTED" --path tools/runner.py

check clean 1 EXECUTOR_SOURCE_DRIFT
check poisoned-ref 1 EXECUTOR_SOURCE_DRIFT
check poisoned-full 1 EXECUTOR_SOURCE_DRIFT
check poisoned-equal 0 EXECUTOR_SOURCE_BOUND
if [ "$fails" -gt 0 ]; then echo "GIT_DIR-poison test: $fails failure(s)"; exit 1; fi
echo "GIT_DIR-poison test: all 4 assertions passed"
