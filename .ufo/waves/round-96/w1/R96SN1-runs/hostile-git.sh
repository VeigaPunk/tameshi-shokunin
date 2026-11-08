#!/bin/sh
# Hostile git: forges `cat-file blob` output and `rev-parse --show-toplevel`.
LOG=/fast/scratch/hyaku/tameshi-r96/R96SN1/hostile-git.log
echo "HOSTILE $*" >> "$LOG"

# find the -C repo argument and the subcommand
repo=""
sub=""
prev=""
for a in "$@"; do
  if [ "$prev" = "-C" ]; then repo="$a"; fi
  prev="$a"
done
# strip -C <repo>
newargs=""
skip=0
for a in "$@"; do
  if [ $skip -eq 1 ]; then skip=0; continue; fi
  if [ "$a" = "-C" ]; then skip=1; continue; fi
  newargs="$newargs $a"
done
set -- $newargs
sub="$1"

case "$sub" in
  rev-parse)
    if [ "$2" = "--show-toplevel" ]; then
      # forge a toplevel that matches whatever lane we are in
      echo "$repo"
      exit 0
    fi
    exec /usr/bin/git "$@"
    ;;
  cat-file)
    # cat-file blob <rev>:<path>  -> forge a chosen blob
    spec="$3"
    case "$spec" in
      *census-mutants.json)
        printf '{"gate":{"repo":"/home/vgpnk/Projects/shokunin","commit":"f47ad6ba8d306f8125597401cb2ce45c1297a593","path":"scripts/sources-census.sh","sha256":"FORGED_BY_HOSTILE_GIT_0000000000000000000000000000000000000","fixtures":"scripts/fixtures/sources-census"}}'
        exit 0
        ;;
      *sources-census.sh)
        echo "FORGED-GATE-BYTES"
        exit 0
        ;;
    esac
    exec /usr/bin/git "$@"
    ;;
  *)
    exec /usr/bin/git "$@"
    ;;
esac
