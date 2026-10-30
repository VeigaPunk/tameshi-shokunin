#!/usr/bin/env bash
# executor-source-pin.py — adversarial absolute-path CLI test (unscored hardening probe).
# Proposed by T59W1S29. NOT part of the frozen 24-fixture counter; L1 decides when to run.
#
# Usage: executor-source-pin-abspath-test.sh TOOL WORK
#   TOOL  path to tools/executor-source-pin.py under test
#   WORK  empty scratch dir (must not exist yet); removed on exit
#
# Sound behavior pinned here (see .ufo/waves/round-59/w1/T59W1S29.md):
#   * --repo may be absolute (the frozen counter always passes absolute --repo; exit 0 required).
#   * every absolute / traversal / trailing-slash --path fails closed:
#       exit 2 + EXECUTOR_SOURCE_UNAVAILABLE, no filesystem resolution of --path.
#   * relative spellings unchanged: equal -> 0 + EXECUTOR_SOURCE_BOUND, changed -> 1 + EXECUTOR_SOURCE_DRIFT.
set -u
TOOL=${1:?usage: $0 TOOL WORK}; WORK=${2:?usage: $0 TOOL WORK}
case "$WORK" in /*) ;; *) echo "WORK must be absolute" >&2; exit 64;; esac
[ -e "$WORK" ] && { echo "WORK must not exist" >&2; exit 64; }
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 TMPDIR="${TMPDIR:-/tmp}"
fail=0
expect() { # desc want_rc want_token rc out
  local desc=$1 want_rc=$2 want_token=$3 rc=$4 out=$5
  if [ "$rc" = "$want_rc" ] && printf '%s' "$out" | grep -q "$want_token"; then
    echo "ok   $desc (rc=$rc, $want_token)"
  else
    echo "FAIL $desc (want rc=$want_rc+$want_token, got rc=$rc: $out)"; fail=1
  fi
}
mkdir -p "$WORK/fixture/tools" && cd "$WORK/fixture" || exit 64
git init -q
[ "$(git rev-parse --show-toplevel)" = "$WORK/fixture" ] || { echo "fixture root mismatch" >&2; exit 64; }
printf 'print("real executor")\n' > tools/runner.py
git add -- tools/runner.py
git -c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false commit -qm fixture
TRUSTED=$(git rev-parse HEAD)
printf 'print("forged success")\n' > tools/runner.py
git add -u
git -c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false commit -qm forged
CAND=$(git rev-parse HEAD)
printf 'print("real executor")\n' > "$WORK/evil.py"   # external file byte-equal to trusted blob, OUTSIDE the repo

run() { out=$(python3 -I "$TOOL" --repo "$WORK/fixture" --trusted "$TRUSTED" --candidate "$CAND" --path "$1" 2>&1); rc=$?; }

out=$(python3 -I "$TOOL" --repo "$WORK/fixture" --trusted "$TRUSTED" --candidate "$TRUSTED" --path tools/runner.py 2>&1)
expect "relative equal"        0 EXECUTOR_SOURCE_BOUND $? "$out"
out=$(python3 -I "$TOOL" --repo "$WORK/fixture" --trusted "$TRUSTED" --candidate "$CAND" --path tools/runner.py 2>&1)
expect "relative changed"      1 EXECUTOR_SOURCE_DRIFT $? "$out"

run /tools/runner.py;       expect "absolute anchored"      2 EXECUTOR_SOURCE_UNAVAILABLE $rc "$out"
run "$WORK/evil.py";        expect "absolute external"      2 EXECUTOR_SOURCE_UNAVAILABLE $rc "$out"
run /etc/passwd;            expect "absolute system"        2 EXECUTOR_SOURCE_UNAVAILABLE $rc "$out"
run ../../etc/passwd;       expect "traversal escape"       2 EXECUTOR_SOURCE_UNAVAILABLE $rc "$out"
run tools/../tools/runner.py; expect "in-tree traversal"    2 EXECUTOR_SOURCE_UNAVAILABLE $rc "$out"
run tools/runner.py/;       expect "trailing slash"         2 EXECUTOR_SOURCE_UNAVAILABLE $rc "$out"

cd / && rm -rf "$WORK"
echo "abspath-test $([ $fail = 0 ] && echo PASS || echo FAIL)"
exit $fail
