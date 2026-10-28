#!/bin/bash
# T55W2SentStrayWrites — fleet-root misroot / stray-write sweep at C0.
# Read-only against the fleet root and the lane. All mutation happens in $S only.
set -u
FLEET=/home/vgpnk/Projects/shokunin
LANE=$FLEET/tameshi-shokunin
C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
OUT=$LANE/.ufo/waves/round-55/w2/T55W2SentStrayWrites-receipts
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r55/T55W2SentStrayWrites
mkdir -p "$S" || exit 2
trap 'rm -rf -- "$S"' EXIT
mkdir -p "$OUT"

echo "## R1 fleet-root porcelain (no pathspec)"
{
  echo '$ git -C '"$FLEET"' status --porcelain'
  git -C "$FLEET" status --porcelain
  echo "entries=$(git -C "$FLEET" status --porcelain | wc -l)"
} > "$OUT/01-fleet-root-porcelain.txt" 2>&1

echo "## R2 content markers of every untracked entry"
{
  for f in o.bin oldrep1.out oldrep2.out \
           .scratch/closure-mado-r50.json .scratch/source-routing-queue.md \
           .ufo/reports/round-49/tsukuroi.md; do
    echo "===== $f  ($(stat -c '%s bytes mtime=%y' "$FLEET/$f"))"
    printf '  matches tameshi        : %s\n' "$(grep -c -i 'tameshi' "$FLEET/$f" 2>/dev/null)"
    printf '  matches round-55|r55   : %s\n' "$(grep -c -E 'round-55|round 55|\br55\b' "$FLEET/$f" 2>/dev/null)"
    printf '  matches T55W[123]      : %s\n' "$(grep -c -E 'T55W[123]' "$FLEET/$f" 2>/dev/null)"
    printf '  matches C0 sha         : %s\n' "$(grep -c '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb' "$FLEET/$f" 2>/dev/null)"
    echo '  first line:'
    head -c 200 "$FLEET/$f" | tr -d '\000' | sed -n '1p' | cut -c1-180 | sed 's/^/    /'
  done
  echo
  echo "===== .scratch/closure-r54/ (recursive; 1 line per file, git dirs excluded)"
  find "$FLEET/.scratch/closure-r54" -type f -not -path '*/.git/*' | head -20
  echo "  files(excluding .git)=$(find "$FLEET/.scratch/closure-r54" -type f -not -path '*/.git/*' | wc -l)"
  echo "  tameshi|round-55 hits among them:"
  grep -rlE 'tameshi|round-55|T55W[123]' "$FLEET/.scratch/closure-r54" --include='*' 2>/dev/null \
    | grep -v '/.git/' | head -10
  echo "  (end hits)"
} > "$OUT/02-untracked-content-markers.txt" 2>&1

echo "## R3 misroot directory scan (git-invisible class)"
{
  echo '$ find FLEET /tmp -maxdepth 2 -type d \( -name D= -o -name S= -o -name E= -o -name W= -o -name T= \)'
  find "$FLEET" /tmp -maxdepth 2 -type d \( -name 'D=' -o -name 'S=' -o -name 'E=' -o -name 'W=' -o -name 'T=' \) 2>/dev/null
  echo
  echo '$ find FLEET -maxdepth 2 -type d -name "*=*"'
  find "$FLEET" -maxdepth 2 -type d -name '*=*' 2>/dev/null
  echo
  echo '--- full tree of the misroot ---'
  find "$FLEET/D=" 2>/dev/null
  echo "dirs=$(find "$FLEET/D=" -type d 2>/dev/null | wc -l) files=$(find "$FLEET/D=" -type f 2>/dev/null | wc -l)"
  stat -c 'top: %n mode=%A size=%s mtime=%y' "$FLEET/D=" 2>/dev/null
  echo
  echo '--- why porcelain cannot see it: git has no entry for empty directories ---'
  echo '$ git -C FLEET status --porcelain | grep -c "^.. D=" ; echo got:'
  git -C "$FLEET" status --porcelain | grep -c '^.. D=' 
  echo '$ git -C FLEET ls-files -o --exclude-standard | grep -c "D="'
  git -C "$FLEET" ls-files -o --exclude-standard | grep -c 'D='
  echo '$ git -C FLEET check-ignore -v D=  (no ignore rule; nothing to report)'
  git -C "$FLEET" check-ignore -v 'D=' ; echo "check-ignore exit=$?"
  echo
  echo '--- same class inside the tameshi lane (depth 2) ---'
  find "$LANE" -maxdepth 2 -type d -name 'D=' -o -maxdepth 2 -type d -name 'S=' 2>/dev/null | head
  echo "lane-misroot-dirs=$(find "$LANE" -maxdepth 2 -type d -name 'D=' 2>/dev/null | wc -l)"
} > "$OUT/03-misroot-dir-scan.txt" 2>&1

echo "## R4 /tmp sweep"
{
  echo '$ find /tmp -maxdepth 4 \( -name "*tameshi*" -o -name "*r55*" -o -name "*round-55*" -o -name "*T55W*" \)'
  find /tmp -maxdepth 4 \( -name '*tameshi*' -o -name '*r55*' -o -name '*round-55*' -o -name '*T55W*' \) 2>/dev/null | sort
  echo
  echo '--- of those, mtime today only ---'
  find /tmp -maxdepth 4 -newermt '2026-10-28 00:00' \( -name '*tameshi*' -o -name '*r55*' -o -name '*round-55*' -o -name '*T55W*' \) 2>/dev/null | sort
  echo
  echo '--- literal /tmp/tameshi-r55* (the seat-scratch name this item names) ---'
  ls -d /tmp/tameshi-r55* 2>&1
  echo
  echo '--- named candidates: size/mtime/md5 ---'
  for f in t55stat.txt c0.json fl.json sentscope_frozen.txt skill_c0_923625.md \
           census-r55.txt census-r55-rev01.txt census-r55-mut.txt census-val.out census-now.txt; do
    [ -e "/tmp/$f" ] && stat -c '  %n %s bytes mtime=%y' "/tmp/$f"
  done
  echo
  echo '--- top-level /tmp files today containing a round-55 marker (tameshi|round-55|T55W*|C0 sha) ---'
  find /tmp -maxdepth 1 -newermt '2026-10-28 00:00' -type f -print0 2>/dev/null \
    | xargs -0 grep -lE 'tameshi|round-55|T55W[123]|9cf0146b94ddba12d454ebf7288ce6e5c5d535bb' 2>/dev/null | sort
} > "$OUT/04-tmp-sweep.txt" 2>&1

echo "## R5 byte-equality verdict per /tmp candidate"
{
  echo '--- census receipt strays vs the lane copies (must-move test: cmp) ---'
  for f in census-r55.txt census-r55-rev01.txt census-r55-mut.txt census-val.out census-now.txt; do
    for lane in \
      .ufo/waves/round-55/w1/T55W1ExecCensus-receipts/base-validate.tsv \
      .ufo/waves/round-55/w1/T55W1ExecCensus-receipts/current-validate.tsv \
      .ufo/waves/round-55/w1/T55W1Er09-receipts/24-census-final.stdout; do
      if cmp -s "/tmp/$f" "$LANE/$lane"; then
        echo "cmp IDENTICAL  /tmp/$f  == $lane  (md5 $(md5sum "/tmp/$f" | cut -d' ' -f1))"
        break
      fi
    done
  done
  echo
  echo '--- coldread JSONs ---'
  for f in fl.json c0.json; do
    echo "/tmp/$f md5=$(md5sum "/tmp/$f" | cut -d' ' -f1) size=$(stat -c %s "/tmp/$f")"
    echo "  rev_input=$(python3 -c "import json,sys;print(json.load(open('/tmp/$f')).get('rev_input'))")"
    echo '  lane files of identical size:'
    find "$LANE" -type f -size "$(stat -c %s "/tmp/$f")c" -not -path '*/.git/*' -exec sh -c \
      'for g; do if cmp -s /tmp/'"$f"' "$g"; then echo "    cmp IDENTICAL $g"; fi; done' _ {} +
  done
  echo
  echo '--- skill snapshot /tmp/skill_c0_923625.md ---'
  echo "sha256=$(sha256sum /tmp/skill_c0_923625.md | cut -d' ' -f1) size=$(stat -c %s /tmp/skill_c0_923625.md)"
  echo "SKILL.md @C0  sha256=$(git -C "$LANE" show $C0:SKILL.md | sha256sum | cut -d' ' -f1)"
  echo "SKILL.md @base sha256=$(git -C "$LANE" show 0a2010acd1e92e4e332774050825e21bcfc7e079:SKILL.md | sha256sum | cut -d' ' -f1)"
  echo -n 'blob whose sha256 equals the /tmp copy: '
  git -C "$LANE" cat-file --batch-all-objects --batch-check 2>/dev/null \
    | awk '$2=="blob" && $3==198186 {print $1}' \
    | while read -r b; do
        if [ "$(git -C "$LANE" cat-file blob "$b" | sha256sum | cut -d' ' -f1)" = \
             "e0e0b4d0134f4555951183dec11872ff6665f7c1f94d3958fa2888df3ef47ff9" ]; then
          echo "$b  (SKILL.md at $(git -C "$LANE" log --all --format='%h %ad' --date=iso -1 "$(git -C "$LANE" log --all --format=%H -- SKILL.md | while read -r c; do [ "$(git -C "$LANE" rev-parse "$c:SKILL.md" 2>/dev/null)" = "$b" ] && { echo "$c"; break; }; done)"))"
        fi
      done
  echo
  echo '--- t55stat.txt / specdump.txt / l54.md / sentscope_frozen.txt / sc60.md: any lane twin? ---'
  for f in t55stat.txt specdump.txt l54.md sentscope_frozen.txt sc60.md; do
    m=$(md5sum "/tmp/$f" | cut -d' ' -f1); sz=$(stat -c %s "/tmp/$f")
    hits=$(find "$LANE" -type f -size "${sz}c" -not -path '*/.git/*' -exec md5sum {} + 2>/dev/null | grep -c "^$m")
    echo "  /tmp/$f size=$sz md5=$m lane-identical-copies=$hits"
  done
} > "$OUT/05-byte-equality-verdict.txt" 2>&1

echo "## R6 mechanism reproduction of the D= misroot (inside \$S only)"
{
  echo '$ (cd $S && mkdir mech-proof && cd mech-proof && mktemp -d "D=/fast/scratch/hyaku/tameshi-r54/T54W2Sent02/pinned.XXXXXX")'
  ( cd "$S" && mkdir -p mech-proof && cd mech-proof && mktemp -d "D=/fast/scratch/hyaku/tameshi-r54/T54W2Sent02/pinned.XXXXXX" )
  echo '$ find $S/mech-proof'
  find "$S/mech-proof"
  echo '--- compare shape with the fleet-root leftover ---'
  echo "fleet-root : $(find "$FLEET/D=" -type d | sed "s|$FLEET/||" | tr '\n' ' ')"
  echo "reproduced : $(find "$S/mech-proof" -type d | sed "s|$S/mech-proof/||" | tr '\n' ' ')"
  echo '--- producer documented at .ufo/waves/round-54/w2/T54W2Sent02.md:41 ---'
  sed -n '41p' "$LANE/.ufo/waves/round-54/w2/T54W2Sent02.md"
} > "$OUT/06-mechanism-reproduction.txt" 2>&1

echo "## R7 sibling-lane + home sweep"
{
  n=0; s=0
  for d in "$FLEET"/*/; do
    n=$((n+1))
    [ -d "$d/.git" ] || continue
    s=$((s+1))
    [ "$d" = "$LANE/" ] && continue
    out=$(git -C "$d" status --porcelain 2>/dev/null | grep -iE 'tameshi|T55W|r55|round-55')
    if [ -n "$out" ]; then echo "### $d"; echo "$out" | head -5; fi
  done
  echo "top-level dirs=$n git-repos=$s lanes-with-tameshi-r55-strays=0 (any lane listed above breaks this line)"
  echo
  echo '$ find /home/vgpnk -maxdepth 2 -newermt today \( -name "*T55W*" -o -name "*r55*" -o -name "*tameshi*" \)'
  find /home/vgpnk -maxdepth 2 -newermt '2026-10-28 00:00' \( -name '*T55W*' -o -name '*r55*' -o -name '*tameshi*' \) 2>/dev/null
  echo '(end home sweep)'
} > "$OUT/07-sibling-lanes-and-home.txt" 2>&1

echo "## R8 census"
{
  echo '$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi'
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
  echo "exit=$?"
  echo "rows=$(/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi 2>/dev/null | wc -l)"
} > "$OUT/08-census.txt" 2>&1

echo "receipts written to $OUT"
ls -la "$OUT"
