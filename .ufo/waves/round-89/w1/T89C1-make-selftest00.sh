#!/bin/bash
# T89C1: rebuild the zero-arm selftest variant (byte-exactly) from the committed
# counterfeit witness control, then score it with the FROZEN R89-C1 counter.
# The only difference is the printed selftest line: 21/21 -> 0/0 (no arms at all).
set -uo pipefail
S=/fast/scratch/hyaku/tameshi-r89/T89C1alt
trap 'rm -rf -- "$S"' EXIT
rm -rf -- "$S"; mkdir -p "$S"
sed 's|print("LEDGER_WITNESS_SELFTEST: 21/21 pass")|print("LEDGER_WITNESS_SELFTEST: 0/0 pass")|' \
  "$(dirname "$0")/T89C1-counterfeit-witness.py" > "$S/cw00.py"
WIT=$S/cw00.py bash "$(dirname "$0")/T89C1-counterfeit-witness-measure.sh"
