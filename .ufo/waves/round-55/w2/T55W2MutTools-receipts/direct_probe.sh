#!/bin/bash
# Direct single-mode probe: run the exact mode on each mutant branch under a
# set-but-unusable TMPDIR; record rc, stdout, stderr byte-for-byte.
set -u
S="$(cd "$(dirname "$0")" && pwd)"
M="$S/mut"
BAD="$S/no-such-tmpdir"
OUT="$S/direct"
mkdir -p "$OUT"
probe() {
  local branch="$1" file="$2"; shift 2
  git -C "$M" checkout -q "$branch" || { echo "checkout $branch failed"; return 1; }
  local top; top=$(git -C "$M" rev-parse --show-toplevel)
  [ "$top" = "$M" ] || { echo "TOPLEVEL MISMATCH $top"; return 1; }
  ( cd "$M" && TMPDIR="$BAD" python3 "$file" "$@" >"$OUT/$branch.out" 2>"$OUT/$branch.err" )
  echo "== $branch  ($file $*)  rc=$?"
  echo "-- stdout:"; sed -n '1,4p' "$OUT/$branch.out"
  echo "-- stderr:"; sed -n '1,4p' "$OUT/$branch.err"
}
probe m-rc-revert          tools/repeat-control.py --selftest
probe m-rc-drop-value      tools/repeat-control.py --selftest
probe m-rc-drop-class      tools/repeat-control.py --selftest
probe m-rc-drop-label      tools/repeat-control.py --selftest
probe m-rc-stdout          tools/repeat-control.py --selftest
probe m-rc-wrong-prefix    tools/repeat-control.py --selftest
probe m-cc-revert          tools/context-capture.py --selftest
probe m-cc-stdout          tools/context-capture.py --selftest
probe m-reg-stdout         tools/registry-check.py --selftest
probe m-base               tools/repeat-control.py --selftest
