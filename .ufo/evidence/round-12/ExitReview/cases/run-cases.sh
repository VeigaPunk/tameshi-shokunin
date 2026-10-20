#!/usr/bin/env bash
# ExitReview round-12 evidence: run the four CLI cases against tools/repeat-control.py.
# Each case: fresh --out (must be absent), fresh child state file, stdin from /dev/null.
# Writes per-case observed gate stdout/stderr/exit and a summary (expected vs observed).
set -u
REPO=/home/vgpnk/Projects/shokunin/tameshi-shokunin
EV=$REPO/.ufo/evidence/round-12/ExitReview
CASES=$EV/cases
GATE=$REPO/tools/repeat-control.py
SEQ=$CASES/seq.py
OUT=$EV/run
mkdir -p "$OUT"
SUMMARY=$OUT/summary.tsv
printf 'case\texpected_id\texpected_exit\tobserved_exit\tgate_stdout_last\n' > "$SUMMARY"

run_case() {  # name expected_id expected_exit mode-args...
  local name=$1 eid=$2 eexit=$3; shift 3
  local dir=$OUT/$name
  rm -rf "$dir"; mkdir -p "$dir"
  local state=$dir/child-state.cnt
  python3 "$GATE" --runs 3 --out "$dir/gate-out" -- "$@" </dev/null >"$dir/gate.stdout" 2>"$dir/gate.stderr"
  local rc=$?
  printf '%s\n' "$rc" > "$dir/gate.exit"
  local last
  last=$(grep -v '^[[:space:]]*$' "$dir/gate.stdout" | tail -n 1)
  printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$eid" "$eexit" "$rc" "$last" >> "$SUMMARY"
}

# Case A: exits [0,1,0], stdout/stderr identical -> controls_mismatch, exit 1
run_case A_seq_0_1_0 controls_mismatch 1 python3 "$SEQ" "$OUT/A_seq_0_1_0/child-state.cnt" 0,1,0 same
# Case B: exits [1,1,1], identical -> baseline_nonzero, exit 2
run_case B_seq_1_1_1 baseline_nonzero 2 python3 "$SEQ" "$OUT/B_seq_1_1_1/child-state.cnt" 1,1,1 same
# Case C: exits [0,0,0], stderr differs per run -> controls_mismatch, exit 1
run_case C_seq_0_0_0_stderr controls_mismatch 1 python3 "$SEQ" "$OUT/C_seq_0_0_0_stderr/child-state.cnt" 0,0,0 stderr-diff
# Case D: command unavailable (exec OSError) -> command_unavailable, exit 2
run_case D_command_unavailable command_unavailable 2 /nonexistent/repeat-control-fixture-bin

cat "$SUMMARY"
