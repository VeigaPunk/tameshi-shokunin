#!/bin/bash
# T59W1S37: does a non-canonical --path spelling change a DRIFT verdict?
# Builds explicit scratch fixture; verifies toplevel before every git write.
set -u
S=/fast/scratch/hyaku/tameshi-r59/T59W1S37
RD=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-59/w1/T59W1S37
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 TMPDIR=$S/tmp
AR=$S/aliasrepo
rm -rf "$AR"; mkdir -p "$AR/tools"
git -C "$AR" init -q
[ "$(git -C "$AR" rev-parse --show-toplevel)" = "$AR" ] || { echo FATAL-ROOT; exit 9; }
gc() { git -C "$AR" -c user.name=f -c user.email=f@e.invalid -c commit.gpgsign=false commit -qm "$1"; git -C "$AR" rev-parse HEAD; }
printf 'print("real executor")\n' > "$AR/tools/runner.py"; git -C "$AR" add -- tools/runner.py
T=$(gc trusted)
printf 'print("forged success")\n' > "$AR/tools/runner.py"; git -C "$AR" add -- tools/runner.py
C=$(gc changed)
git -C "$AR" rm -q -- tools/runner.py; M=$(gc missing)
git -C "$AR" checkout -q "$T" -- tools/runner.py; printf 'x\n' > "$AR/unrelated.txt"; git -C "$AR" add -- unrelated.txt; U=$(gc unrelated)
git -C "$AR" update-ref refs/heads/-x "$T"
echo "trusted=$T changed=$C missing=$M unrelated=$U"
for tool in "$S/mock.py" "$RD/mock-mutant.py"; do
  echo "== $(basename "$tool") sha=$(sha256sum "$tool" | cut -c1-12)"
  for sp in 'tools/runner.py' ':tools/runner.py' 'tools//runner.py' './tools/runner.py' ':(top)tools/runner.py' 'tools/./runner.py'; do
    for cls in equal:"$T" changed:"$C" missing:"$M" unrelated:"$U"; do
      name=${cls%%:*}; cand=${cls#*:}
      o=$(python3 -I "$tool" --repo "$AR" --trusted "$T" --candidate "$cand" --path "$sp" 2>&1); rc=$?
      echo "  path=[$sp] cand=$name rc=$rc tok=$(echo "$o" | tail -1 | cut -c1-70)"
    done
  done
  echo "  -- option-like rev via lookup: trusted=refs-name -x"
  o=$(python3 -I "$tool" --repo "$AR" --trusted=-x --candidate "$T" --path tools/runner.py 2>&1); echo "  trusted=-x rc=$? tok=$(echo "$o" | tail -1 | cut -c1-90)"
  o=$(python3 -I "$tool" --repo "$AR" --trusted "refs/heads/-x" --candidate "$T" --path tools/runner.py 2>&1); echo "  trusted=refs/heads/-x rc=$? tok=$(echo "$o" | tail -1 | cut -c1-90)"
done
