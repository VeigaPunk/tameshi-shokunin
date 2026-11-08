#!/usr/bin/env bash
# Round 100 pre-freeze controls (tameshi). Every receipt carries its command line, the measured
# revision and the sha256 of the tool blob that ran. Tools execute from `git show REV:<tool>`
# bytes, never the worktree (round-99 M5). Scratch only under $S; removed on exit.
# Usage: bash .ufo/evidence/round-100/pre-freeze-run.sh <lane> <INSTR rev> <BASE rev> <scratch>
set -u
L=$1; I=$2; B=$3; S=$4
[ -n "$L" ] && [ -n "$I" ] && [ -n "$B" ] && [ -n "$S" ] || { echo "usage"; exit 64; }
[[ "$I" =~ ^[0-9a-f]{40}$ && "$B" =~ ^[0-9a-f]{40}$ ]] || { echo "revs must be 40 hex"; exit 64; }
mkdir -p "$S" && W=$(mktemp -d "$S/prefreeze.XXXXXX") || exit 2
trap 'rm -rf -- "$W"' EXIT
export TMPDIR="$W"
O="$L/.ufo/evidence/round-100/pre-freeze"; mkdir -p "$O"
G=/usr/bin/git
blob() { "$G" -C "$L" show "$1:$2" > "$W/$(basename "$2")" && echo "$W/$(basename "$2")"; }
hdr() { # out rev tool cmd
  { echo "# measured_rev: $2"; echo "# tool: $3";
    echo "# tool_sha256: $("$G" -C "$L" show "$2:$3" | sha256sum | cut -d' ' -f1)";
    echo "# cmd: $4"; } > "$1"; }
REC="--record corpus/lessons/round-95.md --record corpus/lessons/round-96.md --record corpus/lessons/round-97.md --record corpus/lessons/round-98.md --record corpus/lessons/round-99.md"

# ---- C1 ---------------------------------------------------------------------------------
T=$(blob "$I" tools/registry-check.py)
hdr "$O/c1-before-tag-miss.out" "$B" tools/registry-check.py "python3 -I <git show $I:tools/registry-check.py> --root $L --rev $B --tag r100-c1"
( cd "$L" && python3 -I "$T" --root "$L" --rev "$B" --tag r100-c1 ) >> "$O/c1-before-tag-miss.out" 2>&1; echo "rc=$?" >> "$O/c1-before-tag-miss.out"
hdr "$O/c1-at-instruments.out" "$I" tools/registry-check.py "python3 -I <git show $I:tools/registry-check.py> --root $L --rev $I --tag r100-c1"
( cd "$L" && python3 -I "$T" --root "$L" --rev "$I" --tag r100-c1 ) >> "$O/c1-at-instruments.out" 2>&1; echo "rc=$?" >> "$O/c1-at-instruments.out"
# unregistered count of the four C1 tools, at base and at INSTR (rows naming the tool in argv)
for R in "$B" "$I"; do
  "$G" -C "$L" show "$R:tools/registry.json" | python3 -I -c '
import json,sys
rows=json.load(sys.stdin)["rows"]
four=["tools/tally-reconcile.py","tools/control-assertion-audit-v2.py","tools/control-assertion-audit.py","tools/registry-cell-immutability.py"]
c={t:sum(1 for r in rows if t in r["argv"] and r.get("status")=="active") for t in four}
print("C1_ROWS rev=%s rows=%d %s tools_with_rows=%d/4" % (sys.argv[1][:12], len(rows), " ".join("%s=%d"%(t.split("/")[1],n) for t,n in c.items()), sum(1 for n in c.values() if n)))' "$R"
done > "$O/c1-rows-base-vs-instr.out" 2>&1
# forgery controls: each of the four tools replaced by a stub that prints the GREEN row's needle
# and exits 0 in a scratch checkout of INSTR; the r100-c1 rows must differ (registry-check rc 1)
for tool in tally-reconcile control-assertion-audit-v2 control-assertion-audit registry-cell-immutability; do
  C="$W/stub-$tool"; "$G" clone -q --shared "$L" "$C" && "$G" -C "$C" checkout -q --detach "$I"
  [ "$("$G" -C "$C" rev-parse --show-toplevel)" = "$C" ] || { echo "stub toplevel mismatch"; exit 2; }
  case $tool in
    tally-reconcile) needle='TALLY_RECONCILE_SELFTEST: 25/25 pass\nTALLY_RECONCILE records=1 tallies=1 pairs=1 matched=1 mismatched=0 unbound=0 uncited=0';;
    control-assertion-audit-v2) needle='CONTROL_ASSERT_V2_SELFTEST: 38/38 pass\nCONTROL_ASSERT sites=15 measured=15 literal=0 unmeasured=0';;
    control-assertion-audit) needle='CONTROL_ASSERT_SELFTEST: 18/18 pass\nCONTROL_ASSERT sites=15 measured=15 literal=0 unmeasured=0';;
    registry-cell-immutability) needle='REGISTRY_IMMUTABLE_SELFTEST: 10/10 pass\nREGISTRY_IMMUTABLE from=29734beb0959 to=3b7ae1272d16 shared=183 changed=0 removed=0 added=0';;
  esac
  printf 'import sys\nprint("%s")\nsys.exit(0)\n' "$needle" > "$C/tools/$tool.py"
  out="$O/c1-forgery-stub-$tool.out"
  { echo "# measured_rev: $I (worktree copy, tools/$tool.py replaced by an always-green stub)";
    echo "# cmd: python3 -I <git show $I:tools/registry-check.py> --root <scratch checkout> --tag r100-c1"; } > "$out"
  ( cd "$C" && python3 -I "$T" --root "$C" --tag r100-c1 ) >> "$out" 2>&1; echo "rc=$?" >> "$out"
  rm -rf -- "$C"
done

# ---- C2 ---------------------------------------------------------------------------------
{ echo "# cmd: git -C $L grep -c GATE_LINE_RECHECK $B -- ."; "$G" -C "$L" grep -c GATE_LINE_RECHECK "$B" -- .; echo "rc=$?"; } > "$O/c2-before-token.out" 2>&1
GT=$(blob "$I" tools/gate-line-recheck.py)
run2() { # name extra-args...
  local n=$1; shift
  hdr "$O/$n.out" "$I" tools/gate-line-recheck.py "python3 -I <git show $I:tools/gate-line-recheck.py> $*"
  ( cd "$L" && python3 -I "$GT" "$@" ) >> "$O/$n.out" 2>&1; echo "rc=$?" >> "$O/$n.out"; }
run2 c2-population --repo "$L" --rev "$I" $REC
run2 c2-red-r95-only --repo "$L" --rev "$I" --record corpus/lessons/round-95.md
run2 c2-green-r99-only --repo "$L" --rev "$I" --record corpus/lessons/round-99.md
run2 c2-green-r97-only --repo "$L" --rev "$I" --record corpus/lessons/round-97.md
run2 c2-selftest --selftest --repo "$L" --rev "$I"
# do-nothing control: quote presence anywhere in the rendered snapshot (the lane's prior check
# class, `C1_SOURCE ... quote:1`) over the same pointers — flags none of the six D1 misses
hdr "$O/c2-control-quote-presence.out" "$I" .ufo/evidence/round-100/c2/quote-presence-control.py "python3 -I <git show $I:...quote-presence-control.py> <tool blob> $L $I + five records"
QC=$(blob "$I" .ufo/evidence/round-100/c2/quote-presence-control.py)
( cd "$L" && python3 -I "$QC" "$GT" "$L" "$I" corpus/lessons/round-95.md corpus/lessons/round-96.md corpus/lessons/round-97.md corpus/lessons/round-98.md corpus/lessons/round-99.md ) >> "$O/c2-control-quote-presence.out" 2>&1; echo "rc=$?" >> "$O/c2-control-quote-presence.out"
# forgery control: a scratch clone of INSTR with ONE round-96 pointer moved 4403 -> 4399 and
# committed under a fixture identity must flip that pointer to miss (exit 1)
F="$W/forge"; "$G" clone -q --shared "$L" "$F" && "$G" -C "$F" checkout -q --detach "$I"
[ "$("$G" -C "$F" rev-parse --show-toplevel)" = "$F" ] || { echo "forge toplevel mismatch"; exit 2; }
python3 -I -c 'import sys;p=sys.argv[1];t=open(p).read();assert t.count("line 4403:")==1;open(p,"w").write(t.replace("line 4403:","line 4399:"))' "$F/corpus/lessons/round-96.md"
"$G" -C "$F" -c user.name=fx -c user.email=fx@fixture.invalid commit -q -am "forge: r96 S321 pointer 4403->4399"
FR=$("$G" -C "$F" rev-parse HEAD)
hdr "$O/c2-forgery-r96-pointer.out" "$I" tools/gate-line-recheck.py "python3 -I <git show $I:tools/gate-line-recheck.py> --repo <scratch clone> --rev <forged child $FR of $I> --record corpus/lessons/round-96.md"
( cd "$F" && python3 -I "$GT" --repo "$F" --rev "$FR" --record corpus/lessons/round-96.md ) >> "$O/c2-forgery-r96-pointer.out" 2>&1; echo "rc=$?" >> "$O/c2-forgery-r96-pointer.out"
hdr "$O/c2-forgery-r96-unforged.out" "$I" tools/gate-line-recheck.py "python3 -I <git show $I:tools/gate-line-recheck.py> --repo $L --rev $I --record corpus/lessons/round-96.md"
( cd "$L" && python3 -I "$GT" --repo "$L" --rev "$I" --record corpus/lessons/round-96.md ) >> "$O/c2-forgery-r96-unforged.out" 2>&1; echo "rc=$?" >> "$O/c2-forgery-r96-unforged.out"
echo "PREFREEZE_DONE"
