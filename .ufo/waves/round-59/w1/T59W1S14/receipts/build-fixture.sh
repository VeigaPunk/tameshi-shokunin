#!/usr/bin/env bash
# Independent fixture builder for round-59 cell: path='tools/日本語.py', class='changed'.
# Mirrors frozen .ufo/evidence/round-59/measure.py construction for ONE path.
set -euo pipefail
export TMPDIR=/fast/scratch/hyaku/tameshi-r59/T59W1S14
R=/fast/scratch/hyaku/tameshi-r59/T59W1S14/receipts
mkdir -p "$R"
PATH_JP='tools/日本語.py'
REAL='print("real executor")'
FORGED='print("forged success")'

# Counter-faithful env: strip GIT_*, neutralize global/system config (as measure.py env).
env_clean() { env -i HOME="$HOME" PATH="$PATH" LANG=C.UTF-8 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR="$TMPDIR" "$@"; }

gitq() { env_clean git -C "$1" "${@:2}"; }

build_common() { # $1 = repo dir
  local repo="$1"
  rm -rf "$repo"
  mkdir -p "$repo"
  env_clean git -C "$repo" init -q
  [ "$(env_clean git -C "$repo" rev-parse --show-toplevel)" = "$repo" ] || { echo "fixture root mismatch"; exit 1; }
  mkdir -p "$repo/tools"
}

commit_fixture() { # $1=repo  $2=path  ; commits index, prints HEAD
  gitq "$1" -c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false commit -qm fixture
  gitq "$1" rev-parse HEAD
}

facts() { # $1=repo $2=rev $3=label  -> append object facts to facts.txt
  {
    echo "== $3 =="
    echo "rev: $2"
    echo "ls-tree: $(gitq "$1" ls-tree "$2" -- "$PATH_JP")"
    local obj; obj=$(gitq "$1" rev-parse "$2:$PATH_JP")
    echo "object: $obj"
    echo "cat-file -t: $(gitq "$1" cat-file -t "$obj")"
    echo "cat-file -s: $(gitq "$1" cat-file -s "$obj")"
    echo "cat-file -p: $(gitq "$1" cat-file -p "$obj")"
  } >> "$R/facts.txt"
}

# ---------- Fixture A: minimal two-commit (trusted -> changed), worktree left at changed ----------
A="$TMPDIR/fixture-jp-changed"
build_common "$A"
printf '%s\n' "$REAL"  > "$A/$PATH_JP"
gitq "$A" add -- "$PATH_JP"
TRUSTED_A=$(commit_fixture "$A")
printf '%s\n' "$FORGED" > "$A/$PATH_JP"
gitq "$A" add -- "$PATH_JP"
CHANGED_A=$(commit_fixture "$A")
{
  echo "TRUSTED_A=$TRUSTED_A"
  echo "CHANGED_A=$CHANGED_A"
  echo "worktree-state: $(stat -c '%F %a' "$A/$PATH_JP")"
} | tee "$R/fixtureA.revs"
facts "$A" "$TRUSTED_A" "A:trusted(original content)"
facts "$A" "$CHANGED_A" "A:changed(forged content)"

# ---------- Fixture B: full measure.py chain for one path; worktree ends as dangling symlink ----------
B="$TMPDIR/fixture-jp-chain"
build_common "$B"
printf '%s\n' "$REAL" > "$B/$PATH_JP"
gitq "$B" add -- "$PATH_JP"
TRUSTED_B=$(commit_fixture "$B")
printf '%s\n' "$FORGED" > "$B/$PATH_JP"
gitq "$B" add -- "$PATH_JP"
CHANGED_B=$(commit_fixture "$B")
rm "$B/$PATH_JP"; gitq "$B" add -u
MISSING_B=$(commit_fixture "$B")
printf '%s\n' "$REAL" > "$B/$PATH_JP"
printf 'unrelated change\n' > "$B/unrelated.txt"
gitq "$B" add -- "$PATH_JP" unrelated.txt
UNRELATED_B=$(commit_fixture "$B")
UNRESOLVABLE_B=0000000000000000000000000000000000000000
rm "$B/$PATH_JP"
ln -s elsewhere.py "$B/$PATH_JP"
gitq "$B" add -- "$PATH_JP"
SYMLINK_B=$(commit_fixture "$B")
{
  echo "TRUSTED_B=$TRUSTED_B"
  echo "CHANGED_B=$CHANGED_B"
  echo "MISSING_B=$MISSING_B"
  echo "UNRELATED_B=$UNRELATED_B"
  echo "UNRESOLVABLE_B=$UNRESOLVABLE_B"
  echo "SYMLINK_B=$SYMLINK_B"
  echo "worktree-state at run time: $(stat -c '%F %a' "$B/$PATH_JP" 2>&1 || true)"
  echo "readlink: $(readlink "$B/$PATH_JP")"
  echo "worktree read attempt: $(cat "$B/$PATH_JP" 2>&1 || true)"
} | tee "$R/fixtureB.revs"
facts "$B" "$TRUSTED_B" "B:trusted(original content)"
facts "$B" "$CHANGED_B" "B:changed(forged content)"

# Sanity: blob identity comparison
echo "trusted-vs-changed blob equal? $([ "$(gitq "$A" rev-parse "$TRUSTED_A:$PATH_JP")" = "$(gitq "$A" rev-parse "$CHANGED_A:$PATH_JP")" ] && echo yes || echo no)" | tee "$R/blob-equality.txt"
echo "fixture build OK"
