#!/usr/bin/env bash
# Round-90 C2 counter (calibration): the round-89 closure's routed record defects 1-4,
# measured over committed bytes at REV, plus a live run of the new registry row.
#
#   measure-c2.sh LANE REV WORK [MANIFEST_SRC]
#
# WORK must be an empty directory. The manifest is read from MANIFEST_SRC (default REV)
# at tools/defect-bind-r90.json and must hash to MANIFEST_SHA (frozen below), so rows
# cannot be dropped or relaxed. REV is checked out in a --shared clone under WORK; the
# lane itself is never written. Conjuncts:
#   manifest  sha256 of the manifest bytes == MANIFEST_SHA
#   rows      tools/defect-bind.py (REV's copy) prints rows=5 closed=5 open=0 unexpected=0, exit 0
#   registry  tools/registry-check.py --root <clone> --only ledger-witness-selftest exits 0
#             and prints REGISTRY_CHECK: held=1/1 (the row runs the real tool's selftest)
# C2_R90_PASS=true iff all three. Exit 0 PASS, 1 not PASS, 2 setup.
set -u
MANIFEST_SHA="c52870037ea55307b0e61e62b97ac20d10b1915d8b79906e174de2c7ae849d95"
LANE=${1:?lane}; REV=${2:?rev}; WORK=${3:?work}; MSRC=${4:-$2}
[ -d "$WORK" ] && [ -z "$(ls -A "$WORK")" ] || { echo "C2_SETUP work-not-empty-dir"; echo "C2_R90_PASS=false"; exit 2; }
WORK=$(realpath -- "$WORK")
R="$WORK/repo"
git clone -q --shared --no-checkout "$LANE" "$R" || { echo "C2_SETUP clone-failed"; echo "C2_R90_PASS=false"; exit 2; }
[ "$(git -C "$R" rev-parse --show-toplevel)" = "$R" ] || { echo "C2_SETUP toplevel"; echo "C2_R90_PASS=false"; exit 2; }
git -C "$R" checkout -q --detach "$REV" || { echo "C2_SETUP rev"; echo "C2_R90_PASS=false"; exit 2; }
FULL=$(git -C "$R" rev-parse HEAD)
git -C "$LANE" show "$MSRC:tools/defect-bind-r90.json" > "$WORK/manifest.json" 2>/dev/null \
  || { echo "C2_SETUP manifest-unreadable"; echo "C2_R90_PASS=false"; exit 2; }
got=$(sha256sum "$WORK/manifest.json" | cut -d' ' -f1)
man=unpinned; [ "$got" = "$MANIFEST_SHA" ] && man=pinned
mkdir -p "$WORK/tmp"
export TMPDIR="$WORK/tmp"
db=$(cd "$R" && python3 -I -X utf8 tools/defect-bind.py --repo . --manifest "$WORK/manifest.json" 2>&1); dbrc=$?
printf '%s\n' "$db" | grep -E '^DEFECT_BIND(_ROW)? '
dbsum=$(printf '%s\n' "$db" | grep -E '^DEFECT_BIND: ' | tail -1)
rows=fail
[ "$dbrc" = 0 ] && printf '%s' "$dbsum" | grep -q 'rows=5 closed=5 open=0 unexpected=0' && rows=ok
rc_out=$(cd "$R" && python3 -I tools/registry-check.py --root . --only ledger-witness-selftest 2>/dev/null); rcrc=$?
printf '%s\n' "$rc_out" | grep -E '^(ROW|REGISTRY_CHECK)'
reg=fail
[ "$rcrc" = 0 ] && printf '%s\n' "$rc_out" | grep -qx 'REGISTRY_CHECK: held=1/1 superseded=0' && reg=held
echo "C2_SUMMARY rev=$FULL manifest=$man manifest_src=$MSRC rows=$rows registry=$reg defect_bind_exit=$dbrc registry_exit=$rcrc"
if [ "$man" = pinned ] && [ "$rows" = ok ] && [ "$reg" = held ]; then
  echo "C2_R90_PASS=true"; exit 0
fi
echo "C2_R90_PASS=false"; exit 1
