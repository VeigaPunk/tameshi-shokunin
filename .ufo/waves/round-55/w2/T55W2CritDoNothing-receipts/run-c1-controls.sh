#!/bin/bash
# T55W2CritDoNothing: independent reproduction of round-55 phase-A controls.
set -u
S=/fast/scratch/hyaku/tameshi-r55/T55W2CritDoNothing
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
BASE=0a2010acd1e92e4e332774050825e21bcfc7e079
C1="$S/code/c1/measure.py"
clone_at () { # clone_at NAME -> path
  local d="$S/clones/$1"
  rm -rf "$d"; mkdir -p "$S/clones"
  git clone --shared --quiet "$L" "$d" || return 1
  git -C "$d" -c advice.detachedHead=false checkout --quiet "$BASE" || return 1
  printf '%s' "$d"
}
commit_all () { # commit_all DIR MSG
  local env=(-c user.name=ctl -c user.email=ctl@invalid)
  git -C "$1" add -A >/dev/null
  GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 git -C "$1" "${env[@]}" commit --quiet -m "$2"
}
assert_toplevel () { # assert_toplevel DIR
  local got; got=$(git -C "$1" rev-parse --show-toplevel) || return 1
  [ "$got" = "$(cd "$1" && pwd -P)" ] || { echo "TOPLEVEL MISMATCH: $got"; return 1; }
}
score_c1 () { # score_c1 DIR TAG
  local w="$S/work-$2"; rm -rf "$w"; mkdir -p "$w"
  python3 "$C1" --lane "$1" --rev "$(git -C "$1" rev-parse HEAD)" --work "$w" --explain \
    > "$S/$2.explain" 2>&1
  echo "rc=$? tag=$2"
  grep -E '^C1_R55:' "$S/$2.explain" | tail -1
}

echo '### A. CTL_SKIP_c1 -- values-only corrections block, no stale assertion fixed'
d=$(clone_at skip1); assert_toplevel "$d" || exit 2
ADD=$(git -C "$L" log --format=%H --diff-filter=A "$BASE" -- .ufo/waves/round-54/w2/T54W2Sent03.md | head -1 | cut -c1-7)
REN=$(git -C "$L" log --format=%H --diff-filter=R "$BASE" -- .ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json | head -1 | cut -c1-7)
echo "ADD=$ADD REN=$REN"
cat >> "$d/SCORECARD.md" <<EOF

## Round 55 - round-54 record corrections

values-only control: CTL_MISMATCH expected=true actual=false 2/3 077d431e total=13
8528ee85 c2/measure.py w1=28 w2=25 sections=12 $ADD renamed $REN config.yml
fabricated superseded reviewers=5 attack=21/76 seats=76 staged=81
controls-a.stdout rekeyed=0/7 r53-counter-at-88afa941
EOF
commit_all "$d" "skip control: values without the fix" || exit 2
score_c1 "$d" skip1

echo
echo '### B. CTL_FAB_c1 -- fabricated values in the corrections block'
d=$(clone_at fab1); assert_toplevel "$d" || exit 2
cat >> "$d/SCORECARD.md" <<'EOF'

## Round 55 - round-54 record corrections

fabricated control: CTL_MISMATCH 9/9 deadbeef00 deadbeef total=9999
deadbeef c2/measure.py w1=99 w2=99 sections=99 0000000 renamed 0000000 config.yml
fabricated superseded reviewers=99 attack=99/99 seats=99 staged=999
controls-a.stdout rekeyed=0/99 r53-counter-at-999999
EOF
commit_all "$d" "fabricated control" || exit 2
score_c1 "$d" fab1

echo
echo '### B2. STRONGER (my variant): the CORRECT derived values pasted from --explain, still no stale fix'
d=$(clone_at correct1); assert_toplevel "$d" || exit 2
cat >> "$d/SCORECARD.md" <<'EOF'

## Round 55 - round-54 record corrections

CTL_MISMATCH 2/3 077d431e total=13 8528ee85 c2/measure.py
w1=28 w2=25 sections=12 ff2a821 7fa9a5e config.yml
fabricated superseded reviewers=5 attack=21/76 seats=76 staged=0
controls-a.stdout rekeyed=0/7 r53-counter-at-88afa941
EOF
commit_all "$d" "strong control: derived values, no stale fix" || exit 2
score_c1 "$d" correct1

echo
echo '### C. do-nothing at BASE (control CTL_0 reference on my own clone)'
d=$(clone_at base2); assert_toplevel "$d" || exit 2
score_c1 "$d" base2
