#!/bin/sh
# Round-98 records run: every counter at the records revision R.
# Usage: sh .ufo/evidence/round-98/records-run.sh <R> <scratch-dir>
set -u
R="$1"
S="$2"
P=".ufo/evidence/round-98/records"
mkdir -p "$P"
rm -rf "$S/records" && mkdir -p "$S/records"

{
  python3 -I tools/control-assertion-audit.py --repo . --rev "$R" --driver .ufo/evidence/round-98/controls98.py
  echo "rc=$?"
} > "$P/c1-audit-controls98.out" 2>&1

{
  python3 -I tools/control-assertion-audit.py --repo . --rev "$R" --driver .ufo/evidence/round-97/controls97.py
  echo "rc=$?"
} > "$P/c1-audit-r97-driver.out" 2>&1

{
  python3 -I tools/control-assertion-audit.py --selftest
  echo "rc=$?"
} > "$P/c1-audit-selftest.out" 2>&1

{
  python3 -I .ufo/evidence/round-98/refusals/guard-refusals.py --lane . --rev "$R" \
    --tool .ufo/evidence/round-97/c2/guard-inertia.py \
    --tool-sha 634997d09d2dba5cd87df12e2844962b3517ede798ab0ce04303807b6db042c8 \
    --work "$S/records/refuse-pos"
  echo "rc=$?"
} > "$P/c2-refusals-positive.out" 2>&1

{
  python3 -I .ufo/evidence/round-98/refusals/guard-refusals.py --lane . --rev "$R" \
    --tool .ufo/evidence/round-97/c2/guard-inertia.py \
    --tool-sha 634997d09d2dba5cd87df12e2844962b3517ede798ab0ce04303807b6db042c8 \
    --work "$S/records/refuse-red" --red state-unbuildable
  echo "rc=$?"
} > "$P/c2-refusals-red.out" 2>&1

{
  python3 -I .ufo/evidence/round-98/refusals/guard-refusals.py --selftest
  echo "rc=$?"
} > "$P/c2-refusals-selftest.out" 2>&1

{
  python3 -I .ufo/evidence/round-98/controls98.py --lane . \
    --base 07e50d6d0142b21e8443b5417b8edc4d1dd76455 --rev "$R" \
    --work "$S/records/controls-work" --outdir "$P/controls"
  echo "rc=$?"
} > "$P/controls98-run.out" 2>&1

{
  python3 -I tools/registry-cell-immutability.py --repo . \
    --from 29734beb095984038d66bb5dd4d149d81378de31 --to "$R"
  echo "rc=$?"
} > "$P/registry-green-r97-records.out" 2>&1

{
  python3 -I tools/registry-cell-immutability.py --selftest
  echo "rc=$?"
} > "$P/registry-selftest.out" 2>&1

{
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --root /home/vgpnk/Projects/shokunin tameshi
  echo "rc=$?"
} > .ufo/waves/round-98/census-after.txt 2>&1

echo "records-run done at $R"
