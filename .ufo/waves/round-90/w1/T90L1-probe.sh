#!/usr/bin/env bash
# T90L1 probe — are the 12 round-90 C1 mutant verdicts invariant under the host
# environment knobs the C1 counter effectively pins (TZ, LANG/LC_ALL, PATH order,
# TMPDIR location)?
#
# Method (read-only on fleet and lane; every mutant is a scratch copy):
#   1. materialize scripts/sources-census.sh + scripts/fixtures/sources-census at
#      fleet commit f47ad6ba... from git objects; verify the pinned sha256;
#   2. apply each of the 12 spec single edits verbatim (old occurs exactly once,
#      new != old) to its own copy; verify `bash -n`;
#   3. run the gate's own `selftest` twice per (mutant, environment) under a
#      6-environment matrix that varies TZ, LC_ALL/LANG, PATH order and TMPDIR;
#   4. verdict = SURVIVED iff every run exits 0 (the counter's mapping), KILLED
#      iff every run exits non-zero, UNSTABLE/INCONCLUSIVE otherwise.
#
# Scratch: /fast/scratch/hyaku/tameshi-r90/T90L1 (removed on exit).
# Usage:  bash T90L1-probe.sh     (prints PIN/VALID/ENV/PRISTINE/CASE/SUMMARY/VERDICT)
set -u

SEAT=T90L1
S=/fast/scratch/hyaku/tameshi-r90/$SEAT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
FLEET=/home/vgpnk/Projects/shokunin
REV=f47ad6ba8d306f8125597401cb2ce45c1297a593
SPEC=$LANE/.ufo/evidence/round-90/c1/census-mutants.json
EXPECTED=$LANE/.ufo/evidence/round-90/pre-freeze/expected.tsv
RECEIPT=$LANE/.ufo/evidence/round-90/pre-freeze/controls/CTL1b-nowork-A.out
GATE_SHA=3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30
SPEC_SHA=ce8983d577b1fa71afd1760b80304cba87c56ca339384df06eb2705a5bfde290

trap 'rm -rf -- "$S"' EXIT
rm -rf -- "$S"
mkdir -p "$S/logs" || exit 2

# ---------------------------------------------------------------- 1. pristine --
D=$S/g
mkdir -p "$D/scripts" || exit 2
git -C "$FLEET" archive --format=tar "$REV" scripts/fixtures/sources-census | tar -x -C "$D"
rc=$?
[ "$rc" = 0 ] || { echo "SETUP archive-failed rc=$rc"; exit 2; }
git -C "$FLEET" show "$REV:scripts/sources-census.sh" > "$D/scripts/sources-census.sh"
rc=$?
[ "$rc" = 0 ] || { echo "SETUP show-failed rc=$rc"; exit 2; }
chmod 755 "$D/scripts/sources-census.sh"
got=$(sha256sum "$D/scripts/sources-census.sh" | awk '{print $1}')
[ "$got" = "$GATE_SHA" ] || { echo "SETUP gate-sha-mismatch $got"; exit 2; }
got=$(sha256sum "$SPEC" | awk '{print $1}')
[ "$got" = "$SPEC_SHA" ] || { echo "SETUP spec-sha-mismatch $got"; exit 2; }
echo "PIN gate=sha256:$GATE_SHA spec=sha256:$SPEC_SHA rev=$REV"

# ------------------------------------------------------- 2. mutant scratch copies --
M=$S/mut
python3 - "$SPEC" "$D/scripts/sources-census.sh" "$D/scripts/fixtures" "$M" <<'PY'
import json, os, shutil, sys
spec, base_path, fix_root, root = sys.argv[1:5]
base = open(base_path, encoding="utf-8").read()
doc = json.load(open(spec, encoding="utf-8"))
for m in doc["mutants"]:
    mid, old, new = m["id"], m["old"], m["new"]
    n = base.count(old)
    assert n == 1, "%s: old occurs %dx" % (mid, n)
    assert new != old, "%s: noop" % mid
    d = os.path.join(root, mid, "scripts")
    os.makedirs(d)
    # copies scripts/fixtures/sources-census/... verbatim under <mutant>/scripts/fixtures
    shutil.copytree(fix_root, os.path.join(d, "fixtures"))
    p = os.path.join(d, "sources-census.sh")
    with open(p, "w", encoding="utf-8") as f:
        f.write(base.replace(old, new, 1))
    os.chmod(p, 0o755)
    print("MUTANT %s applied=1 occurrences=%d" % (mid, n))
PY
[ $? -eq 0 ] || { echo "SETUP mutation-apply-failed"; exit 2; }

ids=$(python3 -c 'import json,sys;print(" ".join(m["id"] for m in json.load(open(sys.argv[1]))["mutants"]))' "$SPEC") || { echo "SETUP ids-failed"; exit 2; }
for mid in $ids; do
  if bash -n "$M/$mid/scripts/sources-census.sh" 2>/dev/null; then
    echo "VALID $mid syntax=ok"
  else
    echo "VALID $mid syntax=FAIL"; exit 2
  fi
done

# ------------------------------------------------------------ 3. env matrix ----
# name|PATH|TZ|LANG|LC_ALL|tmp-subdir   (empty field = variable unset)
ENVS='E0-counter-exact|/usr/local/bin:/usr/bin:/bin||C.UTF-8|C.UTF-8|e0
E1-tz-saopaulo|/usr/local/bin:/usr/bin:/bin|America/Sao_Paulo|C.UTF-8|C.UTF-8|e1
E2-tz-kiritimati|/usr/local/bin:/usr/bin:/bin|Pacific/Kiritimati|C.UTF-8|C.UTF-8|e2
E3-lc-c|/usr/local/bin:/usr/bin:/bin||C|C|e3
E4-lc-enus|/usr/local/bin:/usr/bin:/bin||en_US.UTF-8|en_US.UTF-8|e4
E5-path-rev-lang|/bin:/usr/bin:/usr/local/bin|Pacific/Kiritimati|en_US.UTF-8||e5'

csv=$S/cases.tsv
: > "$csv"

env_args() { # <name> <path> <tz> <lang> <lcall>  -> prints NUL-safe? no: fills global EA
  EA=(env -i "PATH=$2" "HOME=$S/home/$1" "TMPDIR=$S/tmp/$1" "LANG=$4")
  [ -n "$5" ] && EA+=("LC_ALL=$5")
  [ -n "$3" ] && EA+=("TZ=$3")
}

run_pair() { # <gate> <name> <path> <tz> <lang> <lcall> <log>  -> echoes "rc1,rc2"
  local gate=$1 log=$7 rcs="" i r
  env_args "$2" "$3" "$4" "$5" "$6"
  mkdir -p "$S/tmp/$2" "$S/home/$2" || return 90
  for i in 1 2; do
    ( cd "$(dirname "$gate")" && "${EA[@]}" timeout 180 bash "$gate" selftest ) \
      >"$log.r$i" 2>&1 < /dev/null
    r=$?
    rcs=${rcs:+$rcs,}$r
  done
  printf '%s' "$rcs"
}

verdict_of() { # <rcs csv>
  local rcs=$1 r any0=0 anybad=0 anyto=0
  local IFS=,
  for r in $rcs; do
    case "$r" in
      0) any0=1 ;;
      124) anyto=1 ;;
      *) anybad=1 ;;
    esac
  done
  if [ "$anyto" = 1 ]; then echo INCONCLUSIVE
  elif [ "$any0" = 1 ] && [ "$anybad" = 1 ]; then echo UNSTABLE
  elif [ "$any0" = 1 ]; then echo SURVIVED
  else echo KILLED; fi
}

arm_count() { # <log> <run-index>  (a run that reached the end prints ~96 arms)
  local n
  n=$(grep -c -E '^(killed|SURVIVED)' "$1.r$2" 2>/dev/null || true)
  printf '%s' "${n:-0}"
}
final_marker() { # <log> <run-index>
  local f
  f=$(grep -E '^selftest (ok|FAILED)$' "$1.r$2" 2>/dev/null | tail -n1)
  printf '%s' "${f:-none}"
}

broken=0

while IFS='|' read -r ename epath etz elang elcall _esub; do
  [ -n "$ename" ] || continue
  mkdir -p "$S/tmp/$ename" "$S/home/$ename" || exit 2
  env_args "$ename" "$epath" "$etz" "$elang" "$elcall"
  ev=$(cd "$S" && "${EA[@]}" bash -c 'printf "local=%s utc=%s charmap=%s TZ=%s LC_ALL=%s LANG=%s TMPDIR=%s" "$(date +%FT%T%z)" "$(date -u +%FT%TZ)" "$(locale charmap 2>/dev/null || echo NA)" "${TZ:-unset}" "${LC_ALL:-unset}" "${LANG:-unset}" "$TMPDIR"')
  echo "ENV $ename $ev"

  # pristine green control, twice, in this environment
  rcs=$(run_pair "$D/scripts/sources-census.sh" "$ename" "$epath" "$etz" "$elang" "$elcall" "$S/logs/pristine-$ename")
  pa=$(arm_count "$S/logs/pristine-$ename" 1); pb=$(arm_count "$S/logs/pristine-$ename" 2)
  last=$(final_marker "$S/logs/pristine-$ename" 1)
  if [ "$rcs" = "0,0" ] && [ "$last" = "selftest ok" ] && [ "$pa" -ge 90 ] && [ "$pb" -ge 90 ]; then
    echo "PRISTINE $ename rcs=$rcs arms=$pa,$pb state=green last=$last"
  else
    echo "PRISTINE $ename rcs=$rcs arms=$pa,$pb state=BROKEN last=$last"
    broken=$((broken+1))
  fi

  for mid in $ids; do
    log=$S/logs/$mid-$ename
    rcs=$(run_pair "$M/$mid/scripts/sources-census.sh" "$ename" "$epath" "$etz" "$elang" "$elcall" "$log")
    a1=$(arm_count "$log" 1); a2=$(arm_count "$log" 2)
    f1=$(final_marker "$log" 1); f2=$(final_marker "$log" 2)
    if [ "$a1" -lt 90 ] || [ "$a2" -lt 90 ] || [ "$f1" = none ] || [ "$f2" = none ]; then
      echo "CASE_ERROR $mid $ename rcs=$rcs arms=$a1,$a2 finals=$f1/$f2"
      printf '%s\t%s\t%s\tBROKEN\tarms=%s,%s\n' "$mid" "$ename" "$rcs" "$a1" "$a2" >> "$csv"
      broken=$((broken+1))
      continue
    fi
    v=$(verdict_of "$rcs")
    labels=$(grep -h '^SURVIVED' "$log".r1 "$log".r2 2>/dev/null \
             | sed 's/^SURVIVED[[:space:]]*//' | sort -u | paste -sd, -)
    [ -n "$labels" ] || labels=-
    printf 'CASE %s %s rcs=%s arms=%s,%s final=%s verdict=%s labels=%s\n' "$mid" "$ename" "$rcs" "$a1" "$a2" "$f1" "$v" "$labels"
    printf '%s\t%s\t%s\t%s\t%s\n' "$mid" "$ename" "$rcs" "$v" "$labels" >> "$csv"
  done
done <<< "$ENVS"

if [ "$broken" -gt 0 ]; then
  echo "PROBE_ERROR broken_cells=$broken (a selftest run did not reach its 96-arm end; no verdict is claimed)"
  exit 2
fi

# ------------------------------------------------------------- 4. aggregation ---
python3 - "$csv" "$EXPECTED" "$RECEIPT" <<'PY'
import sys

cases_path, expected_path, receipt_path = sys.argv[1:4]
rows = []
for line in open(cases_path, encoding="utf-8"):
    line = line.rstrip("\n")
    if not line:
        continue
    mid, env, rcs, verdict, labels = line.split("\t", 4)
    rows.append((mid, env, rcs, verdict, labels))

envs, mids = [], []
for mid, env, _, _, _ in rows:
    if env not in envs:
        envs.append(env)
    if mid not in mids:
        mids.append(mid)

pred = {}
for line in open(expected_path, encoding="utf-8"):
    p = line.rstrip("\n").split("\t")
    if len(p) >= 3 and p[0] == "predict":
        pred[p[1]] = p[2]

receipt = {}
for line in open(receipt_path, encoding="utf-8"):
    if line.startswith("C1_ROW "):
        parts = line.split()
        receipt[parts[1]] = parts[2].split("=", 1)[1]

varies, abnormal = [], []
per_mid = {}
for mid in mids:
    cells = [(r[1], r[2], r[3], r[4]) for r in rows if r[0] == mid]
    vs = [c[2] for c in cells]
    per_mid[mid] = cells
    if len(set(vs)) > 1:
        varies.append(mid)
    if any(v not in ("KILLED", "SURVIVED") for v in vs):
        abnormal.append(mid)

for mid in mids:
    cells = per_mid[mid]
    matrix = " ".join("%s=%s" % (env, v) for env, _, v, _ in cells)
    ex = pred.get(mid, "?")
    rc = receipt.get(mid, "?")
    ok = set(v for _, _, v, _ in cells) == {ex} == {rc}
    print("MID %s %s expected=%s receipt=%s match=%s" % (mid, matrix, ex, rc, str(ok).lower()))
    sigs = sorted(set(l for _, _, _, l in cells))
    print("SIG %s labelsets=%d %s" % (mid, len(sigs), " || ".join(sigs)))

killed = sum(1 for m in mids if set(r[3] for r in rows if r[0] == m) == {"KILLED"})
survived = sum(1 for m in mids if set(r[3] for r in rows if r[0] == m) == {"SURVIVED"})
pred_match = all(set(r[3] for r in rows if r[0] == m) == {pred.get(m)} for m in mids)
receipt_match = all(set(r[3] for r in rows if r[0] == m) == {receipt.get(m)} for m in mids)
unstable_cells = sum(1 for r in rows if r[3] not in ("KILLED", "SURVIVED"))
verdict = "invariant" if not varies and not abnormal else "varies:" + ",".join(varies + [a for a in abnormal if a not in varies])
print("SUMMARY envs=%d mutants=%d killed=%d survived=%d abnormal_cells=%d varies=%s "
      "predictions_match=%s receipt_match=%s"
      % (len(envs), len(mids), killed, survived, unstable_cells,
         ",".join(varies) or "-", str(pred_match).lower(), str(receipt_match).lower()))
print("VERDICT: " + verdict)
PY
