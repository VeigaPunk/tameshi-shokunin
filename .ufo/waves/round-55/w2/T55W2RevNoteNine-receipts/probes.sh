#!/usr/bin/env bash
# T55W2RevNoteNine receipts: the nine allocating modes against the code, the five
# lazy modes, the tenth documented allocating mode, and four edge probes.
#   probes.sh CLONE WORKDIR
# CLONE = a `git clone --shared` of the lane checked out at C0
#         (9cf0146b94ddba12d454ebf7288ce6e5c5d535bb); WORKDIR = scratch.
# Every grammar verdict below is made with the FROZEN counter's own GRAMMAR
# object, imported from .ufo/evidence/round-55/c2/measure.py at that revision --
# not with a hand-written pattern.
set -u
CLONE=${1:?clone}; WORK=${2:?workdir}
OUT=$(cd "$(dirname "$0")" && pwd)
BAD="$WORK/no-such-tmpdir"
PY=/usr/bin/python3
STRACE=/usr/bin/strace
mkdir -p "$WORK"
cd "$CLONE" || exit 99
git rev-parse HEAD > "$OUT/00-rev.txt"
git status --porcelain >> "$OUT/00-rev.txt"
cat > "$WORK/fixture-contract.json" <<'JSON'
{"surfaces": [{"name": "stable", "repo": ".", "rev": "HEAD",
  "path": ".ufo/evidence/round-12/BaselineControl/fixtures/target.sh",
  "interp": "bash"}]}
JSON

# grammar verdict with the frozen counter's GRAMMAR
grammar() { "$PY" - "$CLONE/.ufo/evidence/round-55/c2/measure.py" "$WORK/line.txt" <<'PY'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("c2measure", sys.argv[1])
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
line = open(sys.argv[2]).read().rstrip("\n")
print("    -> frozen GRAMMAR.match: %s" % bool(mod.GRAMMAR.match(line)))
PY
}

# 01: the nine allocating modes, unusable TMPDIR -> rc, first stderr line, grammar
: > "$OUT/01-nine-modes.out"
run() { local label="$1"; shift; local err rc
  err=$(TMPDIR="$BAD" "$@" 2>&1 >/dev/null); rc=$?
  printf '%s\n' "$err" | head -1 > "$WORK/line.txt"
  { printf '=== %-36s rc=%s\n' "$label" "$rc"
    printf '%s\n' "$err" | sed -n '1,2p' | sed 's/^/    | /'
  } >> "$OUT/01-nine-modes.out"
  grammar >> "$OUT/01-nine-modes.out"
  case "$err" in *Traceback*|*RuntimeError*) printf '    -> FORBIDDEN TOKEN\n' >> "$OUT/01-nine-modes.out";; esac
}
run "env-diff --selftest"             python3 tools/env-diff.py --selftest
run "env-diff --contract"             python3 tools/env-diff.py --contract "$WORK/fixture-contract.json" --out "$WORK/envdiff-out.json" --fleet-root "$CLONE"
run "repeat-control --selftest"       python3 tools/repeat-control.py --selftest
run "registry-check --selftest"       python3 tools/registry-check.py --selftest
run "registry-check --rev"            python3 tools/registry-check.py --rev HEAD
run "bash-witness-study selftest"     python3 tools/bash-witness-study.py selftest
run "pin-disposition --selftest"      python3 tools/pin-disposition.py --selftest
run "evidence-disposition --selftest" python3 tools/evidence-disposition.py --selftest
run "context-capture --selftest"      python3 tools/context-capture.py --selftest
printf '\n--- five lazy modes (no allocation claimed; expected exit kept) ---\n' >> "$OUT/01-nine-modes.out"
for m in "repeat-control --snapshot|--snapshot .ufo/evidence/round-12/ControlGate" \
         "bash-witness-study count|count" \
         "pin-disposition read path|--manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin" \
         "evidence-disposition read|--root . --dispositions .ufo/evidence/round-18/dispositions.json --json" \
         "context-capture --check|--check --json"; do
  label=${m%%|*}; args=${m#*|}
  # shellcheck disable=SC2086
  TMPDIR="$BAD" python3 "tools/${label%% *}.py" $args >/dev/null 2>&1
  printf '=== %-36s rc=%s (expected 0, no grammar line)\n' "$label" "$?" >> "$OUT/01-nine-modes.out"
done
printf '\n--- the note'"'"'s fifth lazy label, literally ---\n' >> "$OUT/01-nine-modes.out"
TMPDIR="$BAD" python3 tools/pin-disposition.py --read >/dev/null 2>&1
printf '=== pin-disposition --read (literal)   rc=%s\n' "$?" >> "$OUT/01-nine-modes.out"

# 02: stdout of the nine at the refusal (verdict-token sweep)
: > "$OUT/02-nine-stdout.out"
for m in "env-diff --selftest|python3 tools/env-diff.py --selftest" \
         "env-diff --contract|python3 tools/env-diff.py --contract $WORK/fixture-contract.json --out $WORK/o.json --fleet-root $CLONE" \
         "repeat-control --selftest|python3 tools/repeat-control.py --selftest" \
         "registry-check --selftest|python3 tools/registry-check.py --selftest" \
         "registry-check --rev|python3 tools/registry-check.py --rev HEAD" \
         "bash-witness-study selftest|python3 tools/bash-witness-study.py selftest" \
         "pin-disposition --selftest|python3 tools/pin-disposition.py --selftest" \
         "evidence-disposition --selftest|python3 tools/evidence-disposition.py --selftest" \
         "context-capture --selftest|python3 tools/context-capture.py --selftest"; do
  label=${m%%|*}; cmd=${m#*|}
  out=$(TMPDIR="$BAD" sh -c "$cmd" 2>/dev/null); rc=$?
  printf '%-36s rc=%s stdout=%s\n' "$label" "$rc" "$(printf '%s' "$out" | tr '\n' ' ')" >> "$OUT/02-nine-stdout.out"
done

# 03: the five lazy modes under a fresh usable TMPDIR: zero mkdir anywhere in it
: > "$OUT/03-lazy-strace.out"
LZ="$WORK/tmp-usable-lazy"
probe() { local label="$1"; shift; rm -rf "$LZ"; mkdir -p "$LZ"
  TMPDIR="$LZ" "$STRACE" -f -e trace=mkdir,mkdirat -o "$WORK/lazy.strace" "$@" >/dev/null 2>&1
  local rc=$?; local n; n=$(grep -cF "$LZ" "$WORK/lazy.strace" 2>/dev/null || true)
  printf '%-34s rc=%s mkdirs-under-TMPDIR=%s\n' "$label" "$rc" "${n:-0}" >> "$OUT/03-lazy-strace.out"; }
probe "repeat-control --snapshot"    python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate
probe "bash-witness-study count"     python3 tools/bash-witness-study.py count
probe "pin-disposition read"         python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin
probe "evidence-disposition read"    python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json
probe "context-capture --check"      python3 tools/context-capture.py --check --json

# 04: the tenth documented mode -- registry-check --root (live run) -- unusable TMPDIR
{ echo "\$ TMPDIR=<unusable> python3 tools/registry-check.py --root \$CLONE --only repeat-control-selftest"
  TMPDIR="$BAD" python3 tools/registry-check.py --root "$CLONE" --only repeat-control-selftest 2>&1; echo "rc=$?"
  echo "\$ TMPDIR=<usable> python3 tools/registry-check.py --root \$CLONE --only repeat-control-selftest"
  UT="$WORK/tmp-usable-live"; rm -rf "$UT"; mkdir -p "$UT"
  TMPDIR="$UT" python3 tools/registry-check.py --root "$CLONE" --only repeat-control-selftest 2>&1; echo "rc=$?"
} > "$OUT/04-live-mode.out"

# 05: the live mode allocates scratch *in its rows* -- strace under a usable TMPDIR
UT="$WORK/tmp-usable-live"; rm -rf "$UT"; mkdir -p "$UT"
TMPDIR="$UT" "$STRACE" -f -e trace=mkdir,mkdirat -o "$WORK/live-row.strace" \
  python3 tools/registry-check.py --root "$CLONE" --only repeat-control-selftest >/dev/null 2>&1
{ echo "# row scratch mkdirs under the live mode's TMPDIR:"
  grep -cF "$UT/tameshi-r12-repeat-control-selftest" "$WORK/live-row.strace"
  echo "# first two:"
  grep -F "$UT/tameshi-r12-repeat-control-selftest" "$WORK/live-row.strace" | head -2
} > "$OUT/05-live-alloc.out"

# 06: a TMPDIR value containing a single quote against the frozen grammar
{ BADQ="/tmp/it's-not-a-dir-$$"
  echo "\$ TMPDIR=\"$BADQ\" python3 tools/repeat-control.py --selftest"
  TMPDIR="$BADQ" python3 tools/repeat-control.py --selftest 2> "$WORK/q.err" >/dev/null; rc=$?
  echo "rc=$rc"
  echo "# stderr line:"; head -1 "$WORK/q.err"
  head -1 "$WORK/q.err" > "$WORK/line.txt"
  grammar
} > "$OUT/06-quoted-grammar.out"

# 07: the literal fifth lazy label
{ echo '$ TMPDIR=<unusable> python3 tools/pin-disposition.py --read'
  TMPDIR="$BAD" python3 tools/pin-disposition.py --read > "$WORK/pin-read.json" 2>&1; echo "rc=$?"
  head -12 "$WORK/pin-read.json"
} > "$OUT/07-pin-read-literal.out"

# 08: env-diff --selftest on a host whose PATH has no bwrap (guard ordering)
SHIM="$WORK/shim-nobwrap"; rm -rf "$SHIM"; mkdir -p "$SHIM"
for b in bash git sleep sh env cat timeout; do p=$(command -v "$b") && ln -sf "$p" "$SHIM/$b"; done
{ echo "# PATH=$SHIM (no bwrap); TMPDIR=$BAD"
  PATH="$SHIM" TMPDIR="$BAD" "$STRACE" -f -e trace=mkdir,mkdirat -o "$WORK/nobwrap.strace" \
    "$PY" tools/env-diff.py --selftest > "$WORK/nobwrap.out" 2> "$WORK/nobwrap.err"
  echo "rc=$?"
  echo "# stderr:"; cat "$WORK/nobwrap.err"
  echo "# stdout tail:"; tail -2 "$WORK/nobwrap.out"
  echo "# mkdirs under /tmp in the mode:"; grep -c '"/tmp' "$WORK/nobwrap.strace" || true
} > "$OUT/08-bwrap-absent.out"

# 09: the branch-scoped reachability table
"$PY" "$OUT/reach2.py" "$CLONE" > "$OUT/09-reach.out" 2>&1

# 10: the remaining documented modes that allocate nothing
{ echo '$ TMPDIR=<unusable> python3 tools/repeat-control.py --runs 3 --out OUT -- /bin/true'
  TMPDIR="$BAD" python3 tools/repeat-control.py --runs 3 --out "$WORK/rc-out" -- /bin/true 2>&1 | tail -2; echo "rc=${PIPESTATUS[0]}"
  echo '$ TMPDIR=<unusable> python3 tools/bash-witness-study.py declare'
  TMPDIR="$BAD" python3 tools/bash-witness-study.py declare 2>&1 | tail -1; echo "rc=${PIPESTATUS[0]}"
  echo '$ TMPDIR=<unusable> python3 tools/bash-witness-study.py check'
  TMPDIR="$BAD" python3 tools/bash-witness-study.py check 2>&1 | tail -2; echo "rc=${PIPESTATUS[0]}"
} > "$OUT/10-unmeasured-modes.out"
echo "receipts written to $OUT"
