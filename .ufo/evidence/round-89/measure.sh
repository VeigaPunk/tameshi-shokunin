#!/bin/bash
# R89-C1 frozen counter. usage: measure.sh <lane-repo> <REV> <fleet-root> <empty-work-dir>
# Reads every instrument from git objects at REV (never the worktree):
#   tools/ledger-witness.py, tools/mutate-and-run.sh,
#   .ufo/evidence/round-89/controls/make-forgeries.py, .ufo/waves/round-88/w1/T88E2-make-variants.py
# and prints one line
#   C1_R89 rev=<REV> witness=<present|absent> selftest=<p>/<n> real=<PASS|FAIL|SETUP>(legs=11)
#          honest_accepted=<a>/<h> forgeries_refused=<r>/<n> capability_row=<0|1> C1_R89_PASS=<true|false>
# exit 0 iff C1_R89_PASS=true. Predicate (frozen, plans/round-89.plan.md): witness present,
# selftest all arms pass; the REV runner and both honest variants each print
# `LEDGER_WITNESS: legs=11 witnessed=11 findings=0 checks=- PASS` with exit 0; every one of
# the 12 forgery runners exits 1 with a line ending ` FAIL`; and the SCORECARD
# capabilities table carries a row whose first cell is `ledger witness`. Every generated
# runner carries a fresh random nonce line, so no variant's bytes are known in advance.
set -u
R=$1; REV=$2; FLEET=$3; W=$4
[[ -d "$W" && -z "$(ls -A "$W")" ]] || { echo "C1_R89 SETUP (work dir must exist and be empty)"; exit 2; }
W=$(realpath "$W")
mkdir -p "$W/src" "$W/forg" "$W/tmp"
export TMPDIR="$W/tmp"
show() { git -C "$R" show "$REV:$1" > "$2" 2>/dev/null; }
witness=present
show tools/ledger-witness.py "$W/src/ledger-witness.py" || witness=absent
cap=0
git -C "$R" show "$REV:SCORECARD.md" 2>/dev/null | grep -qE '^\| ledger witness \|' && cap=1
if [[ $witness == absent ]]; then
  echo "C1_R89 rev=$REV witness=absent selftest=0/0 real=SETUP forgeries_refused=0/0 capability_row=$cap C1_R89_PASS=false"
  exit 1
fi
echo "C1_R89_TOOL sha256=$(sha256sum "$W/src/ledger-witness.py" | cut -c1-64)"
show tools/mutate-and-run.sh "$W/src/mutate-and-run.sh" || { echo "C1_R89 SETUP (runner absent at REV)"; exit 2; }
show .ufo/evidence/round-89/controls/make-forgeries.py "$W/src/make-forgeries.py" || { echo "C1_R89 SETUP (generator absent)"; exit 2; }
show .ufo/waves/round-88/w1/T88E2-make-variants.py "$W/src/T88E2-make-variants.py" || { echo "C1_R89 SETUP (T88E2 generator absent)"; exit 2; }

st=$(python3 -I "$W/src/ledger-witness.py" --selftest 2>&1 | tee "$W/selftest.out" | grep -oE '^LEDGER_WITNESS_SELFTEST: [0-9]+/[0-9]+' | grep -oE '[0-9]+/[0-9]+')
NONCE=$(od -An -N8 -tx1 /dev/urandom | tr -d ' \n')
echo "C1_R89_NONCE $NONCE"
python3 -I "$W/src/make-forgeries.py" "$W/forg" "$NONCE" > "$W/forg.gen" 2>&1 || { echo "C1_R89 SETUP (forgery generation failed)"; exit 2; }
mkdir -p "$W/t88"
python3 -I "$W/src/T88E2-make-variants.py" "$W/t88" >> "$W/forg.gen" 2>&1 || { echo "C1_R89 SETUP (T88E2 generation failed)"; exit 2; }
for f in "$W/t88"/*.sh; do
  { head -n1 "$f"; echo "# nonce: $NONCE"; tail -n +2 "$f"; } > "$W/forg/$(basename "$f")"
done
cat "$W/forg.gen"
nf=$(ls "$W/forg"/*.sh | grep -vc '/honest-')
nh=$(ls "$W/forg"/honest-*.sh | wc -l)
( echo "real $W/src/mutate-and-run.sh"; for f in "$W/forg"/*.sh; do echo "$(basename "$f" .sh) $f"; done ) |
  xargs -P 7 -n 2 bash -c 'python3 -I "'"$W"'/src/ledger-witness.py" --run --runner "$1" --fleet "'"$FLEET"'" --scratch "'"$W"'/run-$0" > "'"$W"'/run-$0.out" 2>&1; echo "$0 $?" >> "'"$W"'/rcs.txt"'
GOOD="LEDGER_WITNESS: legs=11 witnessed=11 findings=0 checks=- PASS"
refused=0; accepted=0; real=FAIL
for n in real $(ls "$W/forg"/*.sh | xargs -n1 basename | sed 's/\.sh$//'); do
  rc=$(awk -v n="$n" '$1==n{print $2}' "$W/rcs.txt")
  line=$(grep -E '^LEDGER_WITNESS: ' "$W/run-$n.out" | tail -1)
  case $n in
    real) echo "C1_R89_REAL rc=${rc:-none} ${line:-no-verdict-line}"
          [[ "$rc" == 0 && "$line" == "$GOOD" ]] && real=PASS ;;
    honest-*) echo "C1_R89_HONEST $n rc=${rc:-none} ${line:-no-verdict-line}"
          [[ "$rc" == 0 && "$line" == "$GOOD" ]] && accepted=$((accepted + 1)) ;;
    *) echo "C1_R89_FORGERY $n rc=${rc:-none} ${line:-no-verdict-line}"
       [[ "$rc" == 1 && "$line" == *" FAIL" ]] && refused=$((refused + 1)) ;;
  esac
done
pass=false
if [[ -n "$st" && "${st%/*}" == "${st#*/}" && $real == PASS && $nh -eq 2 && $accepted -eq 2 && $nf -eq 12 && $refused -eq 12 && $cap -eq 1 ]]; then pass=true; fi
echo "C1_R89 rev=$REV witness=present selftest=${st:-none} real=$real(legs=11) honest_accepted=$accepted/$nh forgeries_refused=$refused/$nf capability_row=$cap C1_R89_PASS=$pass"
[[ $pass == true ]] && exit 0 || exit 1
