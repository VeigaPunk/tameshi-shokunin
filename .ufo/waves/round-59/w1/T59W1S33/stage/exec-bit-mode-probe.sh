#!/usr/bin/env bash
# Proposed CLI probe for the round-59 executor-source-pin gate (T59W1S33).
# Surface: same blob, executable-bit change (both directions).
# NOT a production patch; nothing under tools/ is modified by this probe.
# It builds scratch fixtures with git primitives and runs the gate CLI once
# per case. Expected behavior is a decision for L1 (see T59W1S33.md):
#   mode-strict reading : exit 1 with EXECUTOR_SOURCE_DRIFT on both flips
#   blobs-only reading  : exit 0 with EXECUTOR_SOURCE_BOUND, and the claim
#                         must then state that file mode is not pinned.
set -euo pipefail

TOOL=${1:?usage: exec-bit-mode-probe.sh /path/to/executor-source-pin.py}
WORK=$(mktemp -d "${TMPDIR:-/tmp}/execbit.XXXXXX")
trap 'rm -rf "$WORK"' EXIT

mkbase() { # $1 repo $2 chmod-op (+x|-x as initial state: x=755, -x=644)
  local repo="$1" init="$2"
  git init -q "$repo"
  mkdir -p "$repo/tools"
  printf 'print("real executor")\n' > "$repo/tools/runner.py"
  if [ "$init" = x ]; then chmod +x "$repo/tools/runner.py"; fi
  git -C "$repo" add -- tools/runner.py
  git -C "$repo" -c user.name=probe -c user.email=probe@example.invalid commit -qm base
}

flip() { # $1 repo $2 +x|-x ; commits a mode-only change, prints new HEAD
  git -C "$1" update-index "--chmod=$2" -- tools/runner.py
  git -C "$1" commit -qm "mode flip $2"
  git -C "$1" rev-parse HEAD
}

run_case() { # $1 repo $2 trusted $3 candidate $4 label
  echo "== $4 =="
  echo "trusted entry: $(git -C "$1" ls-tree "$2" -- tools/runner.py)"
  echo "candidate entry: $(git -C "$1" ls-tree "$3" -- tools/runner.py)"
  set +e
  python3 -I "$TOOL" --repo "$1" --trusted "$2" --candidate "$3" --path tools/runner.py
  local rc=$?
  set -e
  echo "exit=$rc"
}

# Direction 1: trusted 100644 -> candidate 100755 (add exec bit, same blob)
R1="$WORK/f-644"; mkbase "$R1" -x
T1=$(git -C "$R1" rev-parse HEAD)
C1=$(flip "$R1" +x)
run_case "$R1" "$T1" "$C1" "644 -> 755 (add exec bit, same blob)"

# Direction 2: trusted 100755 -> candidate 100644 (strip exec bit, same blob)
R2="$WORK/f-755"; mkbase "$R2" x
T2=$(git -C "$R2" rev-parse HEAD)
C2=$(flip "$R2" -x)
run_case "$R2" "$T2" "$C2" "755 -> 644 (strip exec bit, same blob)"

# Negative control: identical tree entry must stay exit 0 / EXECUTOR_SOURCE_BOUND
R3="$WORK/f-ctl"; mkbase "$R3" -x
T3=$(git -C "$R3" rev-parse HEAD)
git -C "$R3" commit -qm noop --allow-empty
C3=$(git -C "$R3" rev-parse HEAD)
run_case "$R3" "$T3" "$C3" "control: identical entry (expect exit 0, BOUND)"
