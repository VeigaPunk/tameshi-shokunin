#!/usr/bin/env bash
# ControlThreats round-12 refusal probes for tools/repeat-control.py (C1).
# Advisory critic evidence, NOT a suite and NOT an admission. Each row names
# argv, expected finding ID and exit as read from the round-12 contract
# (.ufo/waves/round-12/spec.json context "New gate interface"). Rows marked
# AMBIG depend on an unresolved precedence reading; the expectation shown is
# the critic's recommended reading (disagreement before nonzero-baseline).
# Assumption: the gate prints its finding ID somewhere on stdout or stderr.
# Usage: bash gate-probes.sh [REPO_ROOT]   (default: cwd). Scratch: mktemp /tmp.
set -u
ROOT=${1:-$PWD}
GATE="$ROOT/tools/repeat-control.py"
[[ -f "$GATE" ]] || { printf 'GATE_PROBES: SETUP (gate missing: %s)\n' "$GATE"; exit 2; }
T=$(mktemp -d /tmp/tameshi-r12-ct-gate.XXXXXX) || exit 2
pass=0 fail=0

row() { # row <name> <want-id> <want-exit> <stdin-file> -- argv...
  local name=$1 want_id=$2 want_rc=$3 in=$4; shift 5
  local out="$T/$name"
  python3 "$GATE" --runs 3 --out "$out.d" -- "$@" <"$in" >"$out.o" 2>"$out.e"
  local rc=$?
  if [[ $rc -eq $want_rc ]] && grep -qw -- "$want_id" "$out.o" "$out.e"; then
    pass=$((pass + 1)); printf 'ROW %s: OK (exit=%s id=%s)\n' "$name" "$rc" "$want_id"
  else
    fail=$((fail + 1)); printf 'ROW %s: MISS (exit=%s want=%s id-want=%s)\n' "$name" "$rc" "$want_rc" "$want_id"
  fi
}
usage_row() { # usage_row <name> args...
  local name=$1; shift
  python3 "$GATE" "$@" </dev/null >"$T/$name.o" 2>"$T/$name.e"
  local rc=$?
  if [[ $rc -eq 64 ]]; then pass=$((pass + 1)); printf 'ROW %s: OK (exit=64)\n' "$name"
  else fail=$((fail + 1)); printf 'ROW %s: MISS (exit=%s want=64)\n' "$name" "$rc"; fi
}

: >"$T/empty"; printf 'payload\n' >"$T/payload"
# counter fixtures: per-run value selected by a counter file under $T only
run_seq() { # run_seq <name> <id> <rc> <stream> <letters...>
  local name=$1 id=$2 rc=$3 s=$4; shift 4
  local c="$T/$name.cnt"; rm -f "$c"
  row "$name" "$id" "$rc" "$T/empty" -- bash -c \
    'c=$1; s=$2; shift 2; n=$(cat "$c" 2>/dev/null || echo 0); n=$((n+1)); echo $n >"$c"; v=${!n}; if [ "$s" = err ]; then printf "%b" "$v" >&2; else printf "%b" "$v"; fi' \
    _ "$c" "$s" "$@"
}
exit_seq() { # exit_seq <name> <id> <rc> <codes...>
  local name=$1 id=$2 rc=$3; shift 3
  local c="$T/$name.cnt"; rm -f "$c"
  row "$name" "$id" "$rc" "$T/empty" -- bash -c \
    'c=$1; shift; n=$(cat "$c" 2>/dev/null || echo 0); n=$((n+1)); echo $n >"$c"; echo same; exit ${!n}' \
    _ "$c" "$@"
}

# R1/R2 positional mismatch: only run 3 differs / run 2 differs and run 3 returns
run_seq R1-stdout-AAB controls_mismatch 1 out 'A\n' 'A\n' 'B\n'
run_seq R2-stdout-ABA controls_mismatch 1 out 'A\n' 'B\n' 'A\n'
run_seq R3-stderr-AAB controls_mismatch 1 err 'e\n' 'e\n' 'f\n'
# R4 CRLF vs LF: kills text-mode capture (universal newlines; probes.out P3)
run_seq R4-crlf-lf controls_mismatch 1 out 'a\r\n' 'a\n' 'a\r\n'
# R5 exit disagreement with identical bytes. AMBIG under nonzero-first precedence
exit_seq R5-exit-001 controls_mismatch 1 0 0 1
exit_seq R5b-exit-100-cold-first controls_mismatch 1 1 0 0
exit_seq R5c-exit-121 controls_mismatch 1 1 2 1
# R6 stable nonzero baseline
exit_seq R6-exit-111 baseline_nonzero 2 1 1 1
row R6b-sigkill baseline_nonzero 2 "$T/empty" -- bash -c 'kill -9 $$'
# R7 stdin must be DEVNULL even when the gate's own stdin carries data
row R7-cat-devnull controls_match 0 "$T/payload" -- cat
# R8 argv literal, no shell
row R8-argv-literal controls_match 0 "$T/empty" -- printf '%s\n' '$HOME;$(id)'
# R9 spawn failures -> command_unavailable (exit 2, never a traceback exit 1)
printf '#!/bin/sh\nexit 0\n' >"$T/noexec.sh"; chmod 644 "$T/noexec.sh"
printf 'exit 0\n' >"$T/noshebang"; chmod 755 "$T/noshebang"
row R9a-missing command_unavailable 2 "$T/empty" -- "$T/does-not-exist"
row R9b-not-executable command_unavailable 2 "$T/empty" -- "$T/noexec.sh"
row R9c-exec-format command_unavailable 2 "$T/empty" -- "$T/noshebang"
row R9d-directory command_unavailable 2 "$T/empty" -- "$T"
# R10 claim bounds: time-dependent output admitted when runs share a second
row R10-epoch-seconds controls_match 0 "$T/empty" -- date +%s
row R10b-nanoseconds controls_mismatch 1 "$T/empty" -- date +%N
# R11 usage: N>=3 boundary
usage_row R11a-runs-2 --runs 2 --out "$T/u2" -- true
usage_row R11b-runs-1 --runs 1 --out "$T/u1" -- true
usage_row R11c-runs-0 --runs 0 --out "$T/u0" -- true
usage_row R11d-runs-abc --runs abc --out "$T/ua" -- true
usage_row R11e-no-command --runs 3 --out "$T/un" --

# R12 byte fidelity of saved evidence: R4 run1 stdout must be exactly 'a\r\n'
if find "$T/R4-crlf-lf.d" -type f -size 3c 2>/dev/null | grep -q .; then
  pass=$((pass + 1)); printf 'ROW R12-saved-crlf-bytes: OK (a 3-byte file exists)\n'
else
  fail=$((fail + 1)); printf 'ROW R12-saved-crlf-bytes: MISS (no 3-byte saved stream in R4 out dir)\n'
fi
# R13 provenance: does the out dir record argv? (contract does not require it)
if grep -rqF -- 'date' "$T/R10-epoch-seconds.d" 2>/dev/null; then
  printf 'NOTE R13-argv-recorded: yes\n'
else
  printf 'NOTE R13-argv-recorded: no (out dir cannot name its command)\n'
fi

printf 'GATE_PROBES: %s/%s rows as expected (scratch %s)\n' "$pass" "$((pass + fail))" "$T"
[[ $fail -eq 0 ]]
