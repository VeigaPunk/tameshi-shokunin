#!/usr/bin/env bash
# Scratch-only driver: runs receipt-revision-gate.py (read-only on the lane) against fixture repos.
set -u
S=/fast/scratch/hyaku/tameshi-r57/T57W1RevGateSurface
G=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/receipt-revision-gate.py
OUT=$S/out; RC=$S/rcpt
rm -rf "$OUT" "$RC"; mkdir -p "$OUT" "$RC"
D=$(mktemp -d -p "$S" fixture.XXXX)
git -C "$D" init -q -b master
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "FIXTURE NOT TOPLEVEL"; exit 9; }
ID=(-c user.name=fixture -c user.email=fixture@example.invalid)
printf 'alpha\n' > "$D/surface.txt"; printf 'alpha\n' > "$D/other.txt"; printf 'alpha\n' > "$D/moved.txt"
git -C "$D" add -A && git -C "$D" "${ID[@]}" commit -q -m c0 && C0=$(git -C "$D" rev-parse HEAD)
printf 'gamma\n' > "$D/moved.txt"
git -C "$D" add -A && git -C "$D" "${ID[@]}" commit -q -m c1 && C1=$(git -C "$D" rev-parse HEAD)
printf 'delta\n' > "$D/other.txt"
git -C "$D" add -A && git -C "$D" "${ID[@]}" commit -q -m c2 && C2=$(git -C "$D" rev-parse HEAD)
git -C "$D" checkout -q -b side "$C0"; printf 'side\n' > "$D/side.txt"
git -C "$D" add -A && git -C "$D" "${ID[@]}" commit -q -m side && SIDE=$(git -C "$D" rev-parse HEAD)
git -C "$D" checkout -q master
echo "FIXTURE D=$D C0=$C0 C1=$C1 C2=$C2 SIDE=$SIDE"
echo "$D" > "$S/fixture-path.txt"

printf 'surface.txt\n' > "$RC/paths-surface.txt"
printf 'surface.txt\nmoved.txt\n' > "$RC/paths-all.txt"
printf '# only comments\n\n' > "$RC/paths-empty.txt"
printf 'VERDICT: rev=%s C1_X_PASS=true\n' "$C1" > "$RC/pos_c1.txt"
printf 'VERDICT: rev=%s C1_X_PASS=true\n' "$C0" > "$RC/pos_c0.txt"
printf 'VERDICT: rev=%s and rev=%s C1_X_PASS=true\n' "${C1:0:12}" "$C1" > "$RC/same_commit_twice.txt"
printf 'VERDICT: no revision named\n' > "$RC/absent.txt"
printf 'VERDICT: rev=abc123 C1_X_PASS=true\n' > "$RC/short6.txt"
printf 'A rev=%s\nB rev=%s\n' "$C0" "$C1" > "$RC/ambig.txt"
printf 'VERDICT: rev=deadbeefdead C1_X_PASS=true\n' > "$RC/unres.txt"
printf 'CTL A rev=%s\nCTL B rev=%s\n' "$C0" "$C1" > "$RC/ctl_ok.txt"
printf 'CTL A rev=%s\n' "$SIDE" > "$RC/ctl_bad.txt"
printf 'CTL A rev=%s\nCTL B rev=deadbeefdead\n' "$C1" > "$RC/ctl_unres.txt"
printf '{"rev": "%s"}\n' "$C1" > "$RC/json_c1.txt"
printf 'VERDICT: rev=%s\n' "$C1" > "$RC/noline.txt"
printf '\n' > "$RC/empty.txt"
cp "$RC/pos_c1.txt" "$RC/digest.txt"; printf '%064d\n' 0 > "$RC/digest.txt.sha256"
cp "$RC/pos_c1.txt" "$RC/a:b.txt"

run() {
  local name=$1; shift
  python3 "$G" "$@" > "$OUT/$name.out" 2> "$OUT/$name.err"; local rc=$?
  echo "== $name rc=$rc"; cat "$OUT/$name.out"
  [ -s "$OUT/$name.err" ] && { echo "-- stderr (last 3 lines):"; tail -n 3 "$OUT/$name.err"; }
  echo "$name $rc" >> "$OUT/rc-table.txt"
}
L="--lane $D"
run 01-positive-matched          --lane "$D" --certified "$C1" --receipt "$RC/pos_c1.txt:positive"
run 02-positive-identical-paths  --lane "$D" --certified "$C1" --paths "$RC/paths-surface.txt" --receipt "$RC/pos_c0.txt:positive"
run 03-positive-drift-paths      --lane "$D" --certified "$C1" --paths "$RC/paths-all.txt" --receipt "$RC/pos_c0.txt:positive"
run 04-positive-mismatch-strict  --lane "$D" --certified "$C1" --receipt "$RC/pos_c0.txt:positive"
run 05-absent                    --lane "$D" --certified "$C1" --receipt "$RC/absent.txt:positive"
run 06-ambiguous-two-commits     --lane "$D" --certified "$C1" --receipt "$RC/ambig.txt:positive"
run 07-same-commit-named-twice   --lane "$D" --certified "$C1" --receipt "$RC/same_commit_twice.txt:positive"
run 08-unresolvable-receipt-rev  --lane "$D" --certified "$C1" --receipt "$RC/unres.txt:positive"
run 09-control-ancestors-ok      --lane "$D" --certified "$C2" --receipt "$RC/ctl_ok.txt:control"
run 10-control-not-ancestor      --lane "$D" --certified "$C2" --receipt "$RC/ctl_bad.txt:control"
run 11-control-unresolvable      --lane "$D" --certified "$C2" --receipt "$RC/ctl_unres.txt:control"
run 12-digest-mismatch           --lane "$D" --certified "$C1" --receipt "$RC/digest.txt:verdict"
run 13-required-line-missing     --lane "$D" --certified "$C1" --receipt "$RC/noline.txt:verdict:C1_X_PASS="
run 14-missing-file              --lane "$D" --certified "$C1" --receipt "$RC/nope.txt:positive"
run 15-empty-file                --lane "$D" --certified "$C1" --receipt "$RC/empty.txt:positive"
run 16-not-blob-directory        --lane "$D" --certified "$C1" --receipt "$RC:positive"
run 17-json-rev-verdict-ok       --lane "$D" --certified "$C1" --receipt "$RC/json_c1.txt:verdict"
run 18-certified-unresolvable    --lane "$D" --certified deadbeefdeaddead --receipt "$RC/pos_c1.txt:positive"
run 19-certified-unres-json      --lane "$D" --certified deadbeefdeaddead --receipt "$RC/pos_c1.txt:positive" --json
run 20-lane-not-a-repo           --lane "$S/no-such-lane" --certified "$C1" --receipt "$RC/pos_c1.txt:positive"
run 21-empty-paths-file-drift    --lane "$D" --certified "$C1" --paths "$RC/paths-empty.txt" --receipt "$RC/pos_c0.txt:positive"
run 22-paths-file-missing        --lane "$D" --certified "$C1" --paths "$RC/nope-paths.txt" --receipt "$RC/pos_c1.txt:positive"
run 23-paths-empty-string        --lane "$D" --certified "$C1" --paths "" --receipt "$RC/pos_c0.txt:positive"
run 24-usage-no-receipt          --lane "$D" --certified "$C1"
run 25-usage-bogus-role          --lane "$D" --certified "$C1" --receipt "$RC/pos_c1.txt:bogus"
run 26-usage-unknown-flag        --lane "$D" --certified "$C1" --frobnicate --receipt "$RC/pos_c1.txt:positive"
run 27-usage-flag-missing-value  --lane "$D" --certified "$C1" --receipt
run 28-usage-colon-in-path       --lane "$D" --certified "$C1" --receipt "$RC/a:b.txt:positive"
run 29-empty-receipt-path        --lane "$D" --certified "$C1" --receipt ":positive"
run 30-short-rev-token-6hex      --lane "$D" --certified "$C1" --receipt "$RC/short6.txt:positive"
run 31-json-output-positive      --lane "$D" --certified "$C1" --receipt "$RC/pos_c1.txt:positive" --json
run 32-order-unres-cert-bad-role --lane "$D" --certified deadbeefdeaddead --receipt "$RC/pos_c1.txt:bogus"
run 33-selftest                  --selftest
run 34-selftest-with-extra-arg   --selftest --json
run 35-zero-args                 
run 36-json-control-ok           --lane "$D" --certified "$C2" --receipt "$RC/ctl_ok.txt:control" --json
echo "RC_TABLE:"; cat "$OUT/rc-table.txt"
