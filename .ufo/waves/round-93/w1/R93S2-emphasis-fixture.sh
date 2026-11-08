#!/usr/bin/env bash
# R93S2 - end-to-end check of the EMPHASIS ASYMMETRY in the round-93 reader.
#
# Read-only on the lane and on the fleet.  Every clone, fixture and work dir
# lives under the scratch dir named by $1 (default: a fresh one under
# /fast/scratch/hyaku/tameshi-r93/R93S2).  Nothing is committed in the lane.
#
# Two fixtures, each a `git clone --shared` of the lane at the instrument
# revision 855f0c1c59ee2af7f184d8de62d02cdd576eb94e, one edit committed under
# the fixture identity ctl <ctl@fixture.invalid>, read by the FROZEN counter
# (bytes taken from the lane at that revision, never the worktree).
#
#   FX-A  the twelve verdict cells of the REAL verdict table written as
#         **KILLED** / **SURVIVED** (same rendered words, markdown emphasis).
#         Expected on the honest side: the reader does not recognise the
#         emphasised token, so every row reads "no-verdict" and the note is
#         REFUSED (ids=false, mismatched0=false, exit 1).
#
#   FX-B  the honest note plus a second table whose header is `result` (not
#         `verdict`) and whose two tokens are emphasised.  Expected on the
#         hostile side: the stray-verdict scan does not match the emphasised
#         token either, so the hostile table is NOT refused (exit 0).
#
# Together the two show the SAME asymmetry from both directions: the reader
# matches the token bytes exactly, while the header cell is matched through
# norm_cell (which strips `*` and backticks and lowercases).  The header side
# is emphasis-tolerant; the token side is not.
#
# Usage: bash R93S2-emphasis-fixture.sh [SCRATCH_DIR]
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
REV=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
COUNTER=.ufo/evidence/round-93/c1/measure-v93.py
NOTE=corpus/knowledge/mutation-case-fleet-sources-census.md
BASE=${1:-}
if [ -z "$BASE" ]; then
  BASE=$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93S2 fx.XXXXXX)
fi
mkdir -p "$BASE"
echo "SCRATCH=$BASE"

run_fixture () {          # $1 = name, $2 = python edit script (stdin = note path)
  local name="$1"; shift
  local D="$BASE/$name"
  rm -rf "$D"; mkdir -p "$D"
  git clone --shared -q "$LANE" "$D/lane" || return 1
  git -C "$D/lane" checkout -q --detach "$REV" || return 1
  git -C "$D/lane" config user.name ctl
  git -C "$D/lane" config user.email ctl@fixture.invalid
  local top; top=$(git -C "$D/lane" rev-parse --show-toplevel)
  if [ "$top" != "$D/lane" ]; then echo "FIXTURE TOPLEVEL MISMATCH: $top"; return 1; fi
  if [ -n "$(git -C "$D/lane" replace -l)" ]; then echo "FIXTURE HAS REPLACE REFS"; return 1; fi
  python3 - "$D/lane/$NOTE" <<PYEOF
import sys, re
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
$1
open(p, "w", encoding="utf-8").write(t)
PYEOF
  git -C "$D/lane" add "$NOTE"
  git -C "$D/lane" commit -q -m "fixture: $name"
  local fxrev; fxrev=$(git -C "$D/lane" rev-parse HEAD)
  mkdir -p "$D/work"
  echo "--- fixture $name at $fxrev ---"
  ( cd "$LANE" && TMPDIR="$D/tmp" timeout 900 python3 -I "$COUNTER" \
      --repo "$D/lane" --rev "$fxrev" --work "$D/work" > "$D/out" 2> "$D/err" )
  echo "counter exit=$?"
  grep -E 'C1_SUMMARY|C1_BADROWS|C1_CONJUNCTS|C1_R93_PASS' "$D/out" || true
  echo
}

run_fixture FX-A-emphasised-verdict-cells '
n = 0
def repl(m):
    global n; n += 1
    return m.group(1) + "**" + m.group(2) + "**" + m.group(3)
t = re.sub(r"(\| C\d\d \| [^\n]*?\| )(KILLED|SURVIVED)( \|)", repl, t)
assert n == 12, n
print("FX-A: emphasised", n, "verdict cells")
'

run_fixture FX-B-renamed-header-emphasised-tokens '
t = t + ("\n| id | arm | result | witness |\n|---|---|---|---|\n"
         "| C01 | fixture arm | **SURVIVED** | differs |\n"
         "| C02 | fixture arm | **KILLED** | differs |\n")
print("FX-B: appended renamed-header table with EMPHASISED tokens")
'

# FX-B2 is the MINIMAL PAIR of FX-B: byte-identical table, plain tokens.  It is
# the control `renamed-result` shape and it IS refused (ids=false, exit 1).  The
# ONLY difference between FX-B and FX-B2 is the two `**` pairs, and that alone
# flips the verdict from PASS to REFUSE.
run_fixture FX-B2-renamed-header-plain-tokens '
t = t + ("\n| id | arm | result | witness |\n|---|---|---|---|\n"
         "| C01 | fixture arm | SURVIVED | differs |\n"
         "| C02 | fixture arm | KILLED | differs |\n")
print("FX-B2: appended renamed-header table with PLAIN tokens (minimal pair)")
'
