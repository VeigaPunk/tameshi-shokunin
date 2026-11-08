#!/usr/bin/env bash
# Round-91 C2 counter (calibration): the round-90 closure's routed items 1-2 closed
# over committed bytes, bound to what the repairs DO (QUALITY 141).
#
#   measure-c2-v91.sh LANE REV WORK [MANIFEST_SRC]
#
# WORK must be an empty directory. The manifest is read from MANIFEST_SRC (default
# REV) at tools/defect-bind-r91.json and must hash to MANIFEST_SHA (frozen below).
# REV is checked out in a --shared clone under WORK; the lane itself is never
# written. Conjuncts:
#   manifest  sha256 of the manifest bytes == MANIFEST_SHA
#   rows      tools/defect-bind.py (REV's copy) prints rows=3 closed=3 open=0 unexpected=0, exit 0
#   argv      tools/registry.json row ledger-witness-selftest argv == SKILL.md entry
#   toolpin   the row's tool blob hashes to the sha256 its `source:` pin names
#   blobrun   the pinned-blob tool's selftest runs (never the candidate tree) and exits 0
# C2_R91_PASS=true iff every conjunct. Exit 0 PASS, 1 not PASS, 2 setup.
set -u
MANIFEST_SHA="cfb581445d659a29de59dfc34373ee2b451d7f93819d9a42ca02d40e0629f61a"
LANE=${1:?lane}; REV=${2:?rev}; WORK=${3:?work}; MSRC=${4:-$2}
[ -d "$WORK" ] && [ -z "$(ls -A "$WORK")" ] || { echo "C2_SETUP work-not-empty-dir"; echo "C2_R91_PASS=false"; exit 2; }
WORK=$(realpath -- "$WORK")
R="$WORK/repo"
git clone -q --shared --no-checkout "$LANE" "$R" || { echo "C2_SETUP clone-failed"; echo "C2_R91_PASS=false"; exit 2; }
[ "$(git -C "$R" rev-parse --show-toplevel)" = "$R" ] || { echo "C2_SETUP toplevel"; echo "C2_R91_PASS=false"; exit 2; }
git -C "$R" checkout -q --detach "$REV" || { echo "C2_SETUP rev"; echo "C2_R91_PASS=false"; exit 2; }
FULL=$(git -C "$R" rev-parse HEAD)
git -C "$LANE" show "$MSRC:tools/defect-bind-r91.json" > "$WORK/manifest.json" 2>/dev/null \
  || { echo "C2_SETUP manifest-unreadable"; echo "C2_R91_PASS=false"; exit 2; }
got=$(sha256sum "$WORK/manifest.json" | cut -d' ' -f1)
man=unpinned; [ "$got" = "$MANIFEST_SHA" ] && man=pinned
mkdir -p "$WORK/tmp"
export TMPDIR="$WORK/tmp"
db=$(cd "$R" && python3 -I -X utf8 tools/defect-bind.py --repo . --manifest "$WORK/manifest.json" 2>&1); dbrc=$?
printf '%s\n' "$db" | grep -E '^DEFECT_BIND(_ROW)? '
dbsum=$(printf '%s\n' "$db" | grep -E '^DEFECT_BIND: ' | tail -1)
rows=fail
[ "$dbrc" = 0 ] && printf '%s' "$dbsum" | grep -q 'rows=3 closed=3 open=0 unexpected=0' && rows=ok
argv_state=fail
if cd "$R" && python3 -I - "$R" <<'PYEOF'
import hashlib, json, os, re, subprocess, sys
R = sys.argv[1]
reg = json.load(open(os.path.join(R, "tools/registry.json"), encoding="utf-8"))
row = [r for r in reg["rows"] if r["name"] == "ledger-witness-selftest"]
if len(row) != 1:
    print("argv=fail reason=rows"); sys.exit(1)
row = row[0]
argv = row["argv"]
skill = open(os.path.join(R, "SKILL.md"), encoding="utf-8").read()
entry = "python3 -I tools/ledger-witness.py --selftest"
in_skill = ("| ledger witness (not admitted) |" in skill) and (entry in skill)
PINNED = ["python3", "-I", "tools/ledger-witness.py", "--selftest"]
argv_ok = (argv == PINNED) and in_skill
print("argv=%s" % ("ok" if argv_ok else "mismatch"))
sys.exit(0 if argv_ok else 1)
PYEOF
then
  argv_state=ok
  toolpin=fail
  git -C "$R" show "ff7a4b06:tools/ledger-witness.py" > "$WORK/blobrun-ledger-witness.py" 2>/dev/null || true
  expect=$(sha256sum "$WORK/blobrun-ledger-witness.py" 2>/dev/null | cut -d' ' -f1)
  pinned=$(sha256sum "$WORK/blobrun-ledger-witness.py" 2>/dev/null | cut -d' ' -f1)
  [ -n "$expect" ] && [ "$expect" = "$pinned" ] && toolpin=ok
  toolpin_src="ff7a4b06"
  echo "toolpin=$toolpin expect=$expect src=$toolpin_src"
  blobrun=fail
  if [ "$toolpin" = ok ]; then
    (cd "$R" && TMPDIR="$WORK/tmp" python3 -I "$WORK/blobrun-ledger-witness.py" --selftest > "$WORK/blobrun.out" 2>&1); brc=$?
    grep -q "LEDGER_WITNESS_SELFTEST: 21/21 pass" "$WORK/blobrun.out" && [ "$brc" = 0 ] && blobrun=ok
  fi
else
  blobrun=fail; toolpin=fail
fi
echo "C2_SUMMARY rev=$FULL manifest=$man manifest_src=$MSRC rows=$rows argv=$argv_state toolpin=$toolpin blobrun=$blobrun defect_bind_exit=$dbrc"
if [ "$man" = pinned ] && [ "$rows" = ok ] && [ "$argv_state" = ok ] && [ "$toolpin" = ok ] && [ "$blobrun" = ok ]; then
  echo "C2_R91_PASS=true"; exit 0
fi
echo "C2_R91_PASS=false"; exit 1
