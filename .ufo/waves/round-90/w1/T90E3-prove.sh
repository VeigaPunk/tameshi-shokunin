#!/usr/bin/env bash
# T90E3-prove.sh — prove the round-90 survivor-killing selftest arms (seat T90E3).
#
# Read-only on the fleet and the lane: every gate copy is materialized from the fleet's
# object store at the pinned commit into /fast/scratch/hyaku/tameshi-r90/T90E3 and removed
# on exit. Nothing under /home/vgpnk/Projects/shokunin is written except this driver's
# receipt next to it (T90E3-prove.out) — the patch is never applied to the real gate.
#
# What it shows, against scripts/sources-census.sh @ f47ad6ba:
#   1. pristine + arms: selftest exit 0 and `selftest ok` (all seven arms `killed`);
#   2. each of the 7 pre-registered SURVIVED mutants + arms: selftest exit 3 and exactly
#      the arm drafted for that mutant prints SURVIVED (the others stay killed);
#   3. each of the 5 pre-registered KILLED mutants + arms: still exit 3, every arm killed.
#
# Usage: bash T90E3-prove.sh
# Requires: bash, git, gawk, patch, python3, tar, sha256sum, mktemp.

set -u
SEAT=T90E3
FLEET=/home/vgpnk/Projects/shokunin
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
REV=f47ad6ba8d306f8125597401cb2ce45c1297a593
SPEC="$LANE/.ufo/evidence/round-90/c1/census-mutants.json"
W1="$LANE/.ufo/waves/round-90/w1"
PATCH="$W1/T90E3-arms.patch"
OUT="$W1/T90E3-prove.out"
S=/fast/scratch/hyaku/tameshi-r90/$SEAT

SURVIVORS="C02 C03 C06 C08 C09 C10 C12"
KILLED="C01 C04 C05 C07 C11"

trap 'rm -rf -- "$S"' EXIT
mkdir -p "$S/tmp" "$S/work" || exit 3
: > "$OUT"

say() { printf '%s\n' "$*" | tee -a "$OUT"; }
die() { say "PROVE-FAIL: $*"; exit 3; }

[ -r "$SPEC" ] || die "spec unreadable: $SPEC"
[ -r "$PATCH" ] || die "patch unreadable: $PATCH"
command -v patch >/dev/null || die "patch missing"

say "SEAT $SEAT  rev $REV"
say "SPEC $(sha256sum "$SPEC" | cut -d' ' -f1)"
say "PATCH $(sha256sum "$PATCH" | cut -d' ' -f1)"

materialize() { # dest
  local dest=$1
  rm -rf -- "$dest"
  mkdir -p "$dest/scripts" || return 1
  git -C "$FLEET" archive --format=tar "$REV" scripts/fixtures/sources-census |
    tar -x -C "$dest" || return 1
  git -C "$FLEET" show "$REV:scripts/sources-census.sh" > "$dest/scripts/sources-census.sh" || return 1
  chmod 755 "$dest/scripts/sources-census.sh"
}

apply_arms() { # dest
  patch -s --batch --forward -p1 -d "$1" < "$PATCH" || die "patch did not apply to $1"
}

mutate_gate() { # id gate-path
  python3 - "$SPEC" "$1" "$2" <<'PY'
import json, sys, pathlib
spec = json.load(open(sys.argv[1]))
mid, path = sys.argv[2], sys.argv[3]
m = next((x for x in spec["mutants"] if x["id"] == mid), None)
assert m is not None, mid
p = pathlib.Path(path)
src = p.read_text()
assert m["new"] != m["old"], (mid, "new == old")
assert src.count(m["old"]) == 1, (mid, "old count", src.count(m["old"]))
p.write_text(src.replace(m["old"], m["new"], 1))
PY
  bash -n "$2" || die "$1 mutant fails bash -n"
}

arm_label() {
  case $1 in
    C02) printf '%s\n' r90-W02-thin-reject-seven-chars ;;
    C03) printf '%s\n' r90-E04-supersedes-exemption ;;
    C06) printf '%s\n' r90-C06-colon-separator-single-row ;;
    C08) printf '%s\n' r90-E11-usedby-directory ;;
    C09) printf '%s\n' r90-E04-fragment-normalization ;;
    C10) printf '%s\n' r90-symbolic-space-cadence ;;
    C12) printf '%s\n' r90-E11-usedby-comma-trim ;;
    *) printf '' ;;
  esac
}

verdict_of() { # label outfile -> killed|SURVIVED|absent
  local v
  v=$(grep -F -m1 -- "$1" "$2" 2>/dev/null | awk -F'\t' '{print $1}')
  [ -n "$v" ] && printf '%s\n' "$v" || printf 'absent\n'
}

run_suite() { # gate outfile -> rc on stdout
  local gate=$1 out=$2 rc
  TMPDIR="$S/tmp" bash "$gate" selftest > "$out" 2>&1
  rc=$?
  printf '%s\n' "$rc"
}

report_arm_set() { # outfile -> space-separated "label=verdict"
  local out=$1 label v listed=""
  for label in \
    r90-W02-thin-reject-seven-chars \
    r90-E04-supersedes-exemption \
    r90-C06-colon-separator-single-row \
    r90-E11-usedby-directory \
    r90-E04-fragment-normalization \
    r90-symbolic-space-cadence \
    r90-E11-usedby-comma-trim; do
    v=$(verdict_of "$label" "$out")
    listed=${listed:+$listed }"$label=$v"
  done
  printf '%s\n' "$listed"
}

# ---- 1. pristine + arms -----------------------------------------------------
P="$S/work/pristine"
materialize "$P" || die "materialize pristine"
PRISTINE_SHA=$(sha256sum "$P/scripts/sources-census.sh" | cut -d' ' -f1)
SPEC_SHA=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["gate"]["sha256"])' "$SPEC")
[ "$PRISTINE_SHA" = "$SPEC_SHA" ] || die "pristine sha256 $PRISTINE_SHA != spec $SPEC_SHA"
apply_arms "$P" || exit 3
rc=$(run_suite "$P/scripts/sources-census.sh" "$S/work/pristine-arms.out")
arms=$(report_arm_set "$S/work/pristine-arms.out")
grep -qxF 'selftest ok' "$S/work/pristine-arms.out" || die "pristine+arms did not print selftest ok"
[ "$rc" = 0 ] || die "pristine+arms exit $rc, want 0"
case "$arms" in
  *SURVIVED*|*absent*) die "pristine+arms arm set not all killed: $arms" ;;
esac
say "P pristine+arms rc=$rc selftest=ok arms=all-killed PASS"

# ---- 2/3. mutants + arms ----------------------------------------------------
surv_killed=0; killed_kept=0
for id in C01 C02 C03 C04 C05 C06 C07 C08 C09 C10 C11 C12; do
  M="$S/work/m-$id"
  materialize "$M" || die "materialize $id"
  mutate_gate "$id" "$M/scripts/sources-census.sh" || exit 3
  apply_arms "$M" || exit 3
  bash -n "$M/scripts/sources-census.sh" || die "$id+arms fails bash -n"
  rc=$(run_suite "$M/scripts/sources-census.sh" "$S/work/$id.out")
  arms=$(report_arm_set "$S/work/$id.out")
  label=$(arm_label "$id")
  case " $SURVIVORS " in
    *" $id "*)
      v=$(verdict_of "$label" "$S/work/$id.out")
      others_survived=0
      for l in $arms; do
        case "$l" in
          "$label="*) : ;;
          *=SURVIVED) others_survived=$((others_survived+1)) ;;
          *=absent) others_survived=$((others_survived+1)) ;;
        esac
      done
      if [ "$rc" = 3 ] && [ "$v" = SURVIVED ] && [ "$others_survived" = 0 ]; then
        surv_killed=$((surv_killed+1))
        say "M $id expect=SURVIVED rc=$rc target-arm=$v other-arm-survivors=$others_survived PASS"
      else
        say "M $id expect=SURVIVED rc=$rc target-arm=$v other-arm-survivors=$others_survived arms=[$arms] FAIL"
      fi
      ;;
    *)
      other_survived=0
      for l in $arms; do
        case "$l" in *=SURVIVED|*=absent) other_survived=$((other_survived+1)) ;; esac
      done
      if [ "$rc" = 3 ] && [ "$other_survived" = 0 ]; then
        killed_kept=$((killed_kept+1))
        say "M $id expect=KILLED rc=$rc arms=all-killed PASS"
      else
        say "M $id expect=KILLED rc=$rc arm-survivors=$other_survived arms=[$arms] FAIL"
      fi
      ;;
  esac
done

say "PROVE: survivor_arms=$surv_killed/7 killed_stay_killed=$killed_kept/5 pristine_green=yes"
if [ "$surv_killed" = 7 ] && [ "$killed_kept" = 5 ]; then
  say "VERDICT: arms-kill-7/7"
  exit 0
fi
say "VERDICT: arms-incomplete"
exit 1
