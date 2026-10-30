#!/usr/bin/env bash
set -uo pipefail
export TMPDIR=/fast/scratch/hyaku/tameshi-r59/T59W1S14
S=/fast/scratch/hyaku/tameshi-r59/T59W1S14
R=$S/receipts
A=$S/fixture-jp-changed
B=$S/fixture-jp-chain
JP='tools/日本語.py'
TRUSTED_A=66b72636a06a1015f3bce434eed1f147b5a5db50
CHANGED_A=a45722837c34446ac76358596dc08bd2c592b67a
TRUSTED_B=2416d2003a9cd8dd4c59820753ee90eb13b1ddd1
CHANGED_B=1a032cc4ec72356d9cabec7c439d4f797c4b5d1d
ZEROES=0000000000000000000000000000000000000000

# Counter-faithful runtime env for the tool invocations (as in frozen measure.py).
cenv() { env -i HOME="$HOME" PATH="$PATH" LANG=C.UTF-8 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR="$TMPDIR" "$@"; }

run_case() { # label repo trusted candidate tool
  local label="$1" repo="$2" trusted="$3" cand="$4" tool="$5"
  {
    echo "== $label =="
    cenv python3 -I "$tool" --repo "$repo" --trusted "$trusted" --candidate "$cand" --path "$JP"
    echo "exit=$?"
  } >> "$R/oracle-tests.txt" 2>&1
  tail -2 "$R/oracle-tests.txt" | grep -q "exit=" && true
  # re-run capturing streams separately for exact frozen-counter ok computation
  local out rc
  out=$(cenv python3 -I "$tool" --repo "$repo" --trusted "$trusted" --candidate "$cand" --path "$JP" 2>&1)
  rc=$?
  {
    echo "frozen-counter-check: exit=$rc expected=1 token=EXECUTOR_SOURCE_DRIFT in-output=$(case "$out" in *EXECUTOR_SOURCE_DRIFT*) echo yes;; *) echo no;; esac) ok=$( { [ $rc -eq 1 ] && case "$out" in *EXECUTOR_SOURCE_DRIFT*) true;; *) false;; esac; } && echo true || echo false)"
    echo
  } >> "$R/oracle-tests.txt"
}

echo "oracle battery: path=$JP class=changed" > "$R/oracle-tests.txt"
run_case "1. FixtureA minimal: candidate=CHANGED (the assigned cell)" "$A" "$TRUSTED_A" "$CHANGED_A" "$S/oracle-changed-jp.py"
run_case "2. FixtureA discrimination control: candidate=TRUSTED (equal)" "$A" "$TRUSTED_A" "$TRUSTED_A" "$S/oracle-changed-jp.py"
run_case "3. FixtureA guard: candidate=ZEROES (unresolvable)" "$A" "$TRUSTED_A" "$ZEROES" "$S/oracle-changed-jp.py"
run_case "4. FixtureB counter-realistic chain: candidate=CHANGED_B, worktree=dangling-symlink" "$B" "$TRUSTED_B" "$CHANGED_B" "$S/oracle-changed-jp.py"
run_case "5. STRAWMAN worktree-reader on FixtureB: candidate=CHANGED_B (never reads candidate commit)" "$B" "$TRUSTED_B" "$CHANGED_B" "$S/strawman-worktree-tool.py"

# Apply the frozen counter's exact ok-rule to the strawman result (cell changed, expected=1):
{
  echo "== misclassification review inputs =="
  echo "fixture B worktree at tool-run time: $(stat -c '%F' "$B/$JP") -> $(readlink "$B/$JP") (dangling: $([ -e "$B/$JP" ] && echo no || echo yes))"
  echo "strawman decision source: open(repo/path) only; candidate commit never inspected"
} >> "$R/oracle-tests.txt"

cat "$R/oracle-tests.txt"
