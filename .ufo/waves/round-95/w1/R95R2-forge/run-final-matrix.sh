#!/bin/bash
# R95R2 final matrix — every command, exit code, and receipt.
S=/fast/scratch/hyaku/tameshi-r95/R95R2
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C="$S/clone95"
CK="$L/.ufo/evidence/round-95/conjunct-disposition-v95.py"
V94="$S/v94-checker-at-6a2a1fdd.py"
OUT="$S/final"
LOG="$OUT/commands.log"
R95C=".ufo/evidence/round-95/c1/measure-v95.py"
R95M=".ufo/evidence/round-95/conjunct-disposition.json"
R95R=".ufo/evidence/round-95/pre-freeze/controls"
mkdir -p "$OUT"
: > "$LOG"
say() { echo "$@" | tee -a "$LOG"; }
repo() { git -C "$C" rev-parse --show-toplevel; }
checkout() { local rev="$1"; rm -f "$C/.ufo/evidence/round-95/pre-freeze/controls/pins-mutated.out"; git -C "$C" checkout -q --detach "$rev"; test "$(repo)" = "$C"; }
run95() {
  local name="$1"; local rev="$2"; shift 2
  say "### $name"
  say "\$ python3 -I $CK --lane $C --rev $rev --min-falsifiable 17 $*"
  python3 -I "$CK" --lane "$C" --rev "$rev" --min-falsifiable 17 "$@" > "$OUT/$name.out" 2>&1
  local rc=$?
  say "exit=$rc"
  grep -E 'DISPOSITION_INSTRUMENT|DISPOSITION_SETUP|DISPOSITION_FINDING|DISPOSITION rows=' "$OUT/$name.out" | tee -a "$LOG"
  say ""
  return 0
}
run94() {
  local name="$1"; local rev="$2"; shift 2
  say "### $name (v94 checker at 6a2a1fdd)"
  say "\$ python3 -I $V94 --lane $C --rev $rev --counter $R95C --manifest $R95M --receipts $R95R --min-falsifiable 17 $*"
  python3 -I "$V94" --lane "$C" --rev "$rev" --counter "$R95C" --manifest "$R95M" --receipts "$R95R" --min-falsifiable 17 "$@" > "$OUT/$name.out" 2>&1
  local rc=$?
  say "exit=$rc"
  grep -E 'DISPOSITION_INSTRUMENT|DISPOSITION_SETUP|DISPOSITION_FINDING|DISPOSITION rows=' "$OUT/$name.out" | tee -a "$LOG"
  say ""
  return 0
}
say "==== R95R2 final matrix start $(date -Is) ===="
say "checker=$CK sha256=$(sha256sum "$CK" | cut -d' ' -f1)"
say "v94-checker sha256=$(sha256sum "$V94" | cut -d' ' -f1)"
say "v94-counter sha256=$(sha256sum "$S/v94-counter-at-6a2a1fdd.py" | cut -d' ' -f1)"
say "v95-counter-lane sha256=$(sha256sum "$L/$R95C" | cut -d' ' -f1)"
say "toplevel=$(repo)"
say ""

# 1 clean baseline
checkout 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc
say "replace-list=[$(git -C "$C" replace -l | tr '\n' ' ')]"
run95 synth-clean 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc
run94 synth-clean-v94 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc

# 2 forge-handwritten
checkout 8679b03dec969a6a49b705bc602b1f1edb8808a6
cat > "$C/.ufo/evidence/round-95/pre-freeze/controls/pins-mutated.out" <<'EOF'
control=pins-mutated forged=handwritten
counter_sha=5f0d177034173971439be06eb5fbf32dfa8fec4b35a856fc617999e4554ccc2e
exit=1
C1_CONJUNCTS selfpin=true pins=false spec=true pin=true green=true canary=true valid0=true trivial0=true inconclusive0=true unstable0=true note=true verdict_tables=true ids=true mismatched0=true figure=true witnessed=true source=true coverage=true n_min=true
C1_R95_PASS=false
EOF
say "untracked-forged-receipt: $(git -C "$C" status --porcelain=v1 | grep pins-mutated || echo none)"
say "receipt-blob-at-rev: $(git -C "$C" cat-file blob 8679b03dec969a6a49b705bc602b1f1edb8808a6:.ufo/evidence/round-95/pre-freeze/controls/pins-mutated.out 2>&1 | head -1)"
run94 forge-handwritten-v94 8679b03dec969a6a49b705bc602b1f1edb8808a6
run95 forge-handwritten-v95 8679b03dec969a6a49b705bc602b1f1edb8808a6

# 3 forge-counter-sha zero
checkout b8a64e414141c8bc49adfeb7e2f80ee123aaaa2b
run94 forge-counter-sha-zero-v94 b8a64e414141c8bc49adfeb7e2f80ee123aaaa2b
run95 forge-counter-sha-zero-v95 b8a64e414141c8bc49adfeb7e2f80ee123aaaa2b

# 4 forge-counter-sha absent
checkout 0ca27d018d131c5a5728ca9ffe7c3581d8a1836e
run94 forge-counter-sha-absent-v94 0ca27d018d131c5a5728ca9ffe7c3581d8a1836e
run95 forge-counter-sha-absent-v95 0ca27d018d131c5a5728ca9ffe7c3581d8a1836e

# 5 forge-replace-ref (counter blob -> v94 counter blob)
checkout 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc
V95B=$(git -C "$C" rev-parse 4138ff0c:.ufo/evidence/round-95/c1/measure-v95.py)
V94B=$(git -C "$C" hash-object -w "$S/v94-counter-at-6a2a1fdd.py")
git -C "$C" replace -f "$V95B" "$V94B"; test "$(repo)" = "$C"
say "### forge-replace-ref setup"
say "\$ git -C $C replace -f $V95B $V94B"
say "replace-list=[$(git -C "$C" replace -l | tr '\n' ' ')]"
run94 forge-replace-ref-v94 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc
run95 forge-replace-ref-v95 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc
git -C "$C" replace -d "$V95B"; test "$(repo)" = "$C"
say "replace-list-after=[$(git -C "$C" replace -l | tr '\n' ' ')]"
run95 forge-replace-ref-restored-v95 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc

# 6 committed symlink receipt
checkout 9c162399f56d21b948494d893b36ad2d06d61920
run94 symlink-v94 9c162399f56d21b948494d893b36ad2d06d61920
run95 symlink-v95 9c162399f56d21b948494d893b36ad2d06d61920

# 7 receipts path traversal
checkout 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc
run95 receipts-dotdot 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc --receipts ../..
run95 receipts-absolute 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc --receipts "$C/.ufo/evidence/round-95/pre-freeze/controls"
run95 receipts-dot 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc --receipts .
run95 receipts-inner-dotdot 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc --receipts .ufo/evidence/round-95/pre-freeze/controls/..
run95 receipts-default 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc
run94 receipts-absolute-v94 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc --receipts "$C/.ufo/evidence/round-95/pre-freeze/controls"

# 8 ambient GIT_DIR
say "### ambient GIT_DIR=$S/evil95/.git"
GIT_DIR="$S/evil95/.git" python3 -I "$CK" --lane "$C" --rev 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc --min-falsifiable 17 > "$OUT/gitdir-v95.out" 2>&1
say "exit=$?"; grep -E 'DISPOSITION_INSTRUMENT|DISPOSITION_SETUP|DISPOSITION_FINDING|DISPOSITION rows=' "$OUT/gitdir-v95.out" | tee -a "$LOG"; say ""
GIT_DIR="$S/evil95/.git" python3 -I "$V94" --lane "$C" --rev 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc --counter "$R95C" --manifest "$R95M" --receipts "$R95R" --min-falsifiable 17 > "$OUT/gitdir-v94.out" 2>&1
say "exit=$?"; grep -E 'DISPOSITION_INSTRUMENT|DISPOSITION_SETUP|DISPOSITION_FINDING|DISPOSITION rows=' "$OUT/gitdir-v94.out" | tee -a "$LOG"; say ""

# 9 post-hoc manifest, working tree
checkout 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc
M="$C/$R95M"; cp "$M" "$S/final-manifest.orig.json"
python3 - "$M" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p))
r="the sealed pin at state timeout with digest 000000000000 forbids any committed falsifier forever"
for k in d["rows"]: d["rows"][k]={"unfalsifiable":r}
open(p,"w").write(json.dumps(d,indent=1,sort_keys=True)+"\n")
PY
say "worktree-manifest modified: $(git -C "$C" status --porcelain=v1 | grep conjunct-disposition || echo none)"
run95 posthoc-worktree-manifest-v95 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc
cp "$S/final-manifest.orig.json" "$M"

# 10 post-hoc manifest, commit replacement
git -C "$C" replace -f 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc 50d77ad5dcc9b74bbec1f56a79bee5fdbd3eb54c; test "$(repo)" = "$C"
say "### post-hoc commit replacement 4138ff0c -> 50d77ad5"
say "replace-list=[$(git -C "$C" replace -l | tr '\n' ' ')]"
run95 posthoc-commit-replace-v95 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc
say "\$ python3 -I $V94 --lane $C --rev 4138ff0c --counter $R95C --manifest $R95M --receipts $R95R  (no --min-falsifiable)"
python3 -I "$V94" --lane "$C" --rev 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc --counter "$R95C" --manifest "$R95M" --receipts "$R95R" > "$OUT/posthoc-commit-replace-v94-nomin.out" 2>&1
say "exit=$?"; tail -1 "$OUT/posthoc-commit-replace-v94-nomin.out" | tee -a "$LOG"; say ""
run94 posthoc-commit-replace-v94-min 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc
git -C "$C" replace -d 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc; test "$(repo)" = "$C"
say "replace-list-after=[$(git -C "$C" replace -l | tr '\n' ' ')]"

# 11 manifest blob replacement
ORIGM=$(git -C "$C" rev-parse 4138ff0c:.ufo/evidence/round-95/conjunct-disposition.json)
FB=$(git -C "$C" hash-object -w "$S/evil95/forged-manifest.json")
git -C "$C" replace -f "$ORIGM" "$FB"; test "$(repo)" = "$C"
say "### manifest blob replacement $ORIGM -> $FB"
say "replace-list=[$(git -C "$C" replace -l | tr '\n' ' ')]"
run95 replace-manifest-blob-v95 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc
say "\$ python3 -I $V94 ... (no --min-falsifiable)"
python3 -I "$V94" --lane "$C" --rev 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc --counter "$R95C" --manifest "$R95M" --receipts "$R95R" > "$OUT/replace-manifest-blob-v94-nomin.out" 2>&1
say "exit=$?"; tail -1 "$OUT/replace-manifest-blob-v94-nomin.out" | tee -a "$LOG"; say ""
git -C "$C" replace -d "$ORIGM"; test "$(repo)" = "$C"

# 12 forged manifest reasons (bogus digest, fake state, non-battery receipt)
checkout 01b58421175d678c97a72e64574354ffccf153be
run95 forged-manifest-reasons-v95 01b58421175d678c97a72e64574354ffccf153be

# 13 caller-supplied receipts directory
checkout 8d5f9f0e04d37016091da402d4a7b1f949354c44
run95 alt-receipts-v95 8d5f9f0e04d37016091da402d4a7b1f949354c44 --receipts .ufo/evidence/round-95/alt-controls

# 14 do-nothing control at base
checkout 4138ff0c79fa4c3985572c33d394c2d9c8f79fcc
say "### c2-nowork-base"
python3 -I "$CK" --lane "$C" --rev 02ff6290945dde18062a366799a774abb50fb365 --min-falsifiable 17 > "$OUT/nowork-base-v95.out" 2>&1
say "exit=$?"; cat "$OUT/nowork-base-v95.out" | tee -a "$LOG"; say ""

say "==== R95R2 final matrix end $(date -Is) ===="
