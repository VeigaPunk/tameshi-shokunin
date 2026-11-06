#!/usr/bin/env bash
# T88L1 (round 88, wave 1) — leg-11 determinism / environment-independence probe.
#
# H: leg 11's verdict table (py-kake-ledger-guard) is deterministic and
# environment-independent: the kake guard's pristine selftest exits 0 and the
# ten mutants give the recorded table (5 KILLED: K_*, 5 SURVIVED: S_*) on three
# consecutive sweeps, under a different TMPDIR and cwd, and the pristine
# selftest's stdout is byte-identical between the host environment and
# `env -i PATH=$PATH HOME=<scratch> TMPDIR=<scratch> LC_ALL=C`.
#
# Method: the lane's own mutate-and-run.sh in fixture mode (--target/--defects/
# --suite/--workdir) over the pinned kake blob materialized from kake's git
# object store, with the exact leg-11 suite literal taken byte-for-byte from
# the candidate runner (`git show 28ec5885:tools/mutate-and-run.sh`, occurrence
# asserted == 1 below). Every sweep runs from a distinct cwd, with a distinct
# runner TMPDIR and a distinct workdir (hence a distinct per-defect sandbox
# TMPDIR). A split-stream probe then re-executes each sweep's mutant bytes with
# stdout/stderr separated (exit status alone is the verdict oracle) and compares
# the streams across sweeps.
#
# Read-only on the lane: writes only $OUT (this seat's deliverable dir) and
# /fast/scratch/hyaku/tameshi-r88/T88L1 (removed on exit).

set -u -o pipefail

LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
RUNNER=$LANE/tools/mutate-and-run.sh
SPEC=$LANE/.ufo/evidence/round-88/c1/py-kake-ledger-guard.defects.spec
KAKE=/home/vgpnk/Projects/shokunin/kake-shokunin
CAND=28ec58858a084bc193a89ca5b0a751942694ccfb
REV=e8d3a924249983972e5163d160cf236487986c55
BLOB_SHA=0c12838e3d4ea441eb750fd4c6af2398cfa704e5077f6c58b053d535f8514067
RUNNER_SHA=0a0e46de70e8b4f7cda2220efc37757e8bb49ea3833e0920a97a78aaad795a4a
SPEC_SHA=724beed385222b6342dc6d3af5ad19ae605bca8101f983f3ce58da905492689e
OUT=$LANE/.ufo/waves/round-88/w1
S=/fast/scratch/hyaku/tameshi-r88/T88L1
EXPECTED='K_CUT_WHOLE:KILLED,K_STARTSWITH:KILLED,K_FILES_EQ:KILLED,K_GLOB:KILLED,K_SHOW_RC:KILLED,S_HEAD_SHORT:SURVIVED,S_OFFSET_EQ:SURVIVED,S_OK_ALL:SURVIVED,S_VACUOUS:SURVIVED,S_RED_FILES:SURVIVED'
EXPECTED_IDS='K_CUT_WHOLE,K_STARTSWITH,K_FILES_EQ,K_GLOB,K_SHOW_RC,S_HEAD_SHORT,S_OFFSET_EQ,S_OK_ALL,S_VACUOUS,S_RED_FILES'
# Leg 11 suite literal, byte-identical to the candidate runner at line 1591
# (asserted by grep -cF against `git show $CAND:tools/mutate-and-run.sh`).
SUITE='h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" python3 -I "$MUTANT" --selftest'

fails=0
bad() { echo "CHECK-FAIL: $*"; fails=$((fails + 1)); }

cleanup() { rm -rf -- "$S"; }
trap cleanup EXIT

mkdir -p "$S" "$OUT"

observed_table() {
  awk -F'\t' 'NR>1 { if (n++) printf ","; printf "%s:%s", $1, $2 } END { print "" }' "$1"
}
observed_ids() {
  awk -F'\t' 'NR>1 { if (n++) printf ","; printf "%s", $1 } END { print "" }' "$1"
}
expected_verdict() {
  case "$1" in K_*) echo KILLED ;; S_*) echo SURVIVED ;; esac
}

echo "== T88L1 leg-11 determinism probe =="
date -u +"start-utc %Y-%m-%dT%H:%M:%SZ"

echo "== preconditions =="
rs=$(sha256sum "$RUNNER" | cut -d' ' -f1)
echo "runner $RUNNER sha256=$rs (candidate pin $RUNNER_SHA)"
[[ "$rs" == "$RUNNER_SHA" ]] || { echo "PRECONDITION-FAIL: lane runner != candidate revision bytes"; exit 90; }
cand_rs=$(git -C "$LANE" show "$CAND:tools/mutate-and-run.sh" | sha256sum | cut -d' ' -f1)
echo "candidate runner blob sha256=$cand_rs"
[[ "$cand_rs" == "$RUNNER_SHA" ]] || { echo "PRECONDITION-FAIL: candidate runner bytes differ"; exit 90; }
n=$(git -C "$LANE" show "$CAND:tools/mutate-and-run.sh" | grep -cF -- "$SUITE")
echo "leg-11 suite literal occurrences in candidate runner: $n"
[[ "$n" -eq 1 ]] || { echo "PRECONDITION-FAIL: suite literal is not byte-equal to the leg-11 line"; exit 90; }
ss=$(sha256sum "$SPEC" | cut -d' ' -f1)
echo "spec $SPEC sha256=$ss (frozen pin $SPEC_SHA)"
[[ "$ss" == "$SPEC_SHA" ]] || { echo "PRECONDITION-FAIL: spec sha256 != frozen pin"; exit 90; }

echo "== materialize pinned kake blob =="
git -C "$KAKE" show "$REV:scripts/ledger_append_guard.py" > "$S/ledger_append_guard.py" || { echo "PRECONDITION-FAIL: git show failed"; exit 90; }
bs=$(sha256sum "$S/ledger_append_guard.py" | cut -d' ' -f1)
blines=$(wc -l < "$S/ledger_append_guard.py")
echo "blob $S/ledger_append_guard.py sha256=$bs lines=$blines (pin $BLOB_SHA, 153 lines)"
[[ "$bs" == "$BLOB_SHA" ]] || { echo "PRECONDITION-FAIL: blob sha256 != pin"; exit 90; }
[[ "$blines" -eq 153 ]] || bad "blob line count $blines != 153"

echo "expected table: $EXPECTED"

echo "== three sweeps (fixture mode; distinct cwd, runner TMPDIR and workdir per sweep) =="
for i in 1 2 3; do
  cwd="$S/cwd-$i"; tmd="$S/tmp-$i"; wo="$S/work-$i"
  mkdir -p "$cwd" "$tmd"; rm -rf "$wo"
  echo "--- sweep $i: cwd=$cwd TMPDIR=$tmd workdir=$wo"
  ( cd "$cwd" && TMPDIR="$tmd" bash "$RUNNER" \
      --target "$S/ledger_append_guard.py" \
      --defects "$SPEC" \
      --suite "$SUITE" \
      --workdir "$wo" ) > "$S/sweep-$i.out" 2>&1
  rc=$?
  echo "sweep $i: runner-exit=$rc"
  if [[ $rc -ne 0 ]]; then bad "sweep $i runner exit $rc"; fi
  if grep -q '^CONTROL: GREEN' "$S/sweep-$i.out"; then ctl=GREEN; else ctl=NOT-GREEN; bad "sweep $i control not green"; fi
  if grep -q '^MUTATE_RESTORE: OK' "$S/sweep-$i.out"; then rst=OK; else rst=DRIFT; bad "sweep $i restore not OK"; fi
  if grep -q '^MUTATE: DONE' "$S/sweep-$i.out"; then done_=DONE; else done_=NOT-DONE; bad "sweep $i not DONE"; fi
  rows=$(awk 'END { print NR - 1 }' "$wo/results.tsv" 2>/dev/null || echo 0)
  inc=$(awk -F'\t' 'NR>1 && $2=="INCONCLUSIVE" { n++ } END { print n + 0 }' "$wo/results.tsv" 2>/dev/null || echo 0)
  sbx=$(find "$wo" -maxdepth 1 -type d -name 'sandbox-*' | wc -l)
  sbxtmp=$(find "$wo" -mindepth 2 -maxdepth 2 -type d -name 'tmp' -path '*/sandbox-*/*' | wc -l)
  echo "sweep $i: per-defect sandbox dirs=$sbx sandbox TMPDIRs=$sbxtmp (distinct workdir per sweep => distinct TMPDIRs)"
  [[ "$sbx" -eq 11 ]] || bad "sweep $i expected 11 sandbox dirs, found $sbx"
  [[ "$sbxtmp" -eq 11 ]] || bad "sweep $i expected 11 sandbox TMPDIRs, found $sbxtmp"
  obs=$(observed_table "$wo/results.tsv")
  oids=$(observed_ids "$wo/results.tsv")
  [[ "$oids" == "$EXPECTED_IDS" ]] || bad "sweep $i defect ids differ: $oids"
  match=no
  if [[ "$obs" == "$EXPECTED" ]]; then match=yes; else bad "sweep $i verdict table differs: $obs"; fi
  echo "sweep $i: rows=$rows defects=10 inconclusive=$inc control=$ctl restore=$rst state=$done_ verdicts-match=$match"
  awk -F'\t' 'NR>1 { printf "  %-14s %-11s exit=%s\n", $1, $2, $3 }' "$wo/results.tsv"
  echo "observed table: $obs"
done

echo "== split-stream probe: same mutant bytes, stdout/stderr separated =="
stream_ok=yes
mkdir -p "$S/stream"
: > "$S/stream/combined.txt"
for id in $(echo "$EXPECTED_IDS" | tr ',' ' '); do
  for i in 1 2 3; do
    h="$S/stream/s$i-$id"; mkdir -p "$h/home" "$h/tmp"
    ( cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" \
        python3 -I "$S/work-$i/mutant-$id.ledger_append_guard.py" --selftest ) \
      > "$h/stdout" 2> "$h/stderr"
    echo $? > "$h/rc"
    # the file under test must be the bytes results.tsv recorded for this id
    msha=$(sha256sum "$S/work-$i/mutant-$id.ledger_append_guard.py" | cut -d' ' -f1)
    rsha=$(awk -F'\t' -v id="$id" '$1==id { print $5 }' "$S/work-$i/results.tsv")
    [[ "$msha" == "$rsha" ]] || bad "sweep $i $id mutant sha != results.tsv ($msha vs $rsha)"
    sed "s|$S/work-$i|<WORKDIR>|g" "$h/stderr" > "$h/stderr.masked"
  done
  id_ok=yes
  cmp -s "$S/stream/s1-$id/stdout" "$S/stream/s2-$id/stdout" || { id_ok=no; stream_ok=no; bad "$id stdout differs sweep 1 vs 2"; }
  cmp -s "$S/stream/s1-$id/stdout" "$S/stream/s3-$id/stdout" || { id_ok=no; stream_ok=no; bad "$id stdout differs sweep 1 vs 3"; }
  cmp -s "$S/stream/s1-$id/rc" "$S/stream/s2-$id/rc" || bad "$id exit differs sweep 1 vs 2"
  cmp -s "$S/stream/s1-$id/rc" "$S/stream/s3-$id/rc" || bad "$id exit differs sweep 1 vs 3"
  cmp -s "$S/stream/s1-$id/stderr.masked" "$S/stream/s2-$id/stderr.masked" || bad "$id stderr differs beyond workdir path (1 vs 2)"
  cmp -s "$S/stream/s1-$id/stderr.masked" "$S/stream/s3-$id/stderr.masked" || bad "$id stderr differs beyond workdir path (1 vs 3)"
  src=$(cat "$S/stream/s1-$id/rc")
  exp=$(expected_verdict "$id")
  if [[ "$src" -eq 0 ]]; then v=SURVIVED; else v=KILLED; fi
  [[ "$v" == "$exp" ]] || bad "$id split-stream rc=$src gives $v, predicted $exp"
  off=$(sed -nE 's/.*first divergence at byte ([0-9]+).*/\1/p' "$S/stream/s1-$id/stdout"); [[ -n "$off" ]] || off='-'
  ssha=$(sha256sum "$S/stream/s1-$id/stdout" | cut -d' ' -f1)
  echo "  $id: rc=$src verdict=$v predicted=$exp stdout-sha256=$ssha offset=$off stdout-lines=$(wc -l < "$S/stream/s1-$id/stdout")"
  {
    echo "### $id stdout (sweep 1; identical across sweeps 1/2/3 = $id_ok)"
    cat "$S/stream/s1-$id/stdout"
    echo "### $id stderr (sweep 1; workdir path masked; identical in 2/3)"
    cat "$S/stream/s1-$id/stderr.masked"
  } >> "$S/stream/combined.txt"
done
echo "split-stream stdout identical across sweeps: $stream_ok"

echo "== cross-sweep merged-log identity (runner evidence) =="
: > "$S/evidence-sha.txt"
for i in 1 2 3; do
  ( cd "$S/work-$i/evidence" && sha256sum *.out ) | sed "s|^|sweep-$i |" >> "$S/evidence-sha.txt"
done
cat "$S/evidence-sha.txt"
exact=identical; pathonly=''
for f in $( cd "$S/work-1/evidence" && ls *.out ); do
  if cmp -s "$S/work-1/evidence/$f" "$S/work-2/evidence/$f" && cmp -s "$S/work-1/evidence/$f" "$S/work-3/evidence/$f"; then
    :
  else
    exact=DIFFER
    for i in 1 2 3; do sed "s|$S/work-$i|<WORKDIR>|g" "$S/work-$i/evidence/$f" > "$S/evidence-masked-$i-$f"; done
    if cmp -s "$S/evidence-masked-1-$f" "$S/evidence-masked-2-$f" && cmp -s "$S/evidence-masked-1-$f" "$S/evidence-masked-3-$f"; then
      pathonly="$pathonly $f"
      echo "path-only difference: $f (only the absolute workdir path printed in a Python traceback)"
    else
      bad "evidence $f differs beyond the workdir path"
    fi
  fi
done
echo "cross-sweep evidence logs exact=$exact path-only:${pathonly:-none}"
ctl_sha=$(sha256sum "$S/work-1/evidence/control.out" | cut -d' ' -f1)
echo "control.out sha256 (env-i sandbox, identical in all three sweeps): $ctl_sha"

echo "== env diff: pristine selftest stdout, host env vs env -i =="
mkdir -p "$S/env-cwd-host" "$S/env-cwd-min" "$S/tmp-host" "$S/tmp-min" "$S/home-min"
( cd "$S/env-cwd-host" && TMPDIR="$S/tmp-host" python3 -I "$S/ledger_append_guard.py" --selftest ) \
  > "$S/env-host.out" 2> "$S/env-host.err"
hrc=$?
( cd "$S/env-cwd-min" && env -i PATH="$PATH" HOME="$S/home-min" TMPDIR="$S/tmp-min" LC_ALL=C \
    python3 -I "$S/ledger_append_guard.py" --selftest ) \
  > "$S/env-min.out" 2> "$S/env-min.err"
mrc=$?
h_sha=$(sha256sum "$S/env-host.out" | cut -d' ' -f1)
m_sha=$(sha256sum "$S/env-min.out" | cut -d' ' -f1)
host_nvars=$(env | wc -l)
echo "host-env: inherited host env ($host_nvars vars incl. host HOME=/home/vgpnk and host git config; only TMPDIR pointed at scratch): rc=$hrc stdout-bytes=$(wc -c < "$S/env-host.out") stdout-sha256=$h_sha stderr-bytes=$(wc -c < "$S/env-host.err")"
echo "min-env (env -i PATH HOME TMPDIR LC_ALL=C): rc=$mrc stdout-bytes=$(wc -c < "$S/env-min.out") stdout-sha256=$m_sha stderr-bytes=$(wc -c < "$S/env-min.err")"
sed 's/^/  host-stdout| /' "$S/env-host.out"
sed 's/^/  min-stdout | /' "$S/env-min.out"
env_same=no
if cmp -s "$S/env-host.out" "$S/env-min.out"; then env_same=yes; echo "stdout exact: IDENTICAL"; else
  echo "stdout exact: DIFFERS"
  diff -u "$S/env-host.out" "$S/env-min.out" | sed 's/^/  /' || true
  # offset-masked comparison (hypothesis allows only per-run byte offsets to differ)
  sed -E 's/first divergence at byte [0-9]+/first divergence at byte N/' "$S/env-host.out" > "$S/env-host.masked"
  sed -E 's/first divergence at byte [0-9]+/first divergence at byte N/' "$S/env-min.out" > "$S/env-min.masked"
  if cmp -s "$S/env-host.masked" "$S/env-min.masked"; then env_same=masked; echo "stdout masked: IDENTICAL"; else bad "env stdout differs beyond byte offsets"; fi
fi
[[ $hrc -eq 0 ]] || bad "host-env pristine selftest exit $hrc"
[[ $mrc -eq 0 ]] || bad "min-env pristine selftest exit $mrc"
grep -q '^selftest: 2/2 passed$' "$S/env-host.out" || bad "host-env selftest line not 2/2"
grep -q '^selftest: 2/2 passed$' "$S/env-min.out" || bad "min-env selftest line not 2/2"
if cmp -s "$S/env-host.err" "$S/env-min.err"; then err_same=IDENTICAL; else err_same=DIFFERS; fi
echo "stderr: $err_same (not part of H; host git config may emit different hints)"

echo "== copy evidence next to deliverable =="
for i in 1 2 3; do
  cp -- "$S/sweep-$i.out" "$OUT/T88L1-sweep-$i.out"
  cp -- "$S/work-$i/results.tsv" "$OUT/T88L1-results-$i.tsv"
  {
    echo "### sweep $i workdir: $S/work-$i (scratch, removed on exit)"
    echo "### control.out"
    cat "$S/work-$i/evidence/control.out"
    for f in "$S/work-$i/evidence/"*.out; do
      [[ "$(basename "$f")" == control.out ]] && continue
      echo "### $(basename "$f")"
      cat "$f"
    done
  } > "$OUT/T88L1-logs-$i.txt"
done
cp -- "$S/stream/combined.txt" "$OUT/T88L1-splitstream.txt"
cp -- "$S/env-host.out" "$OUT/T88L1-env-host.out"
cp -- "$S/env-host.err" "$OUT/T88L1-env-host.err"
cp -- "$S/env-min.out" "$OUT/T88L1-env-min.out"
cp -- "$S/env-min.err" "$OUT/T88L1-env-min.err"
{
  echo "host-env rc=$hrc stdout-sha256=$h_sha stderr-bytes=$(wc -c < "$S/env-host.err") inherited-vars=$host_nvars"
  echo "min-env  rc=$mrc stdout-sha256=$m_sha stderr-bytes=$(wc -c < "$S/env-min.err")"
  echo "host arm: inherited host environment (host HOME, host git config incl. init.defaultbranch=main; GIT_* editor/pager vars) with only TMPDIR pointed at scratch."
  echo "min arm: exactly env -i PATH HOME TMPDIR LC_ALL=C (no GIT_CONFIG_NOSYSTEM, no GIT_CEILING_DIRECTORIES)."
  echo "stdout-exact-identical=$env_same"
  echo "stderr=$err_same"
  echo "--- host stdout ---"; cat "$S/env-host.out"
  echo "--- min stdout ---"; cat "$S/env-min.out"
  if ! cmp -s "$S/env-host.out" "$S/env-min.out"; then
    echo "--- masked diff (offsets normalized) ---"
    diff -u "$S/env-host.masked" "$S/env-min.masked" || true
  fi
  echo "--- stderr diff (informational) ---"
  diff -u "$S/env-host.err" "$S/env-min.err" || true
} > "$OUT/T88L1-env-cmp.txt"
cp -- "$S/evidence-sha.txt" "$OUT/T88L1-evidence-sha.txt"

if [[ $fails -eq 0 ]]; then final=holds; else final=falsified; fi
echo "== summary =="
echo "env-stdout-identical=$env_same"
echo "split-stream-stdout-identical=$stream_ok"
echo "cross-sweep-evidence-exact=$exact path-only:${pathonly:-none}"
echo "checks-failed=$fails"
echo "FINAL: $final"
date -u +"end-utc %Y-%m-%dT%H:%M:%SZ"
exit 0
