#!/usr/bin/env bash
# prereg-order.sh <repo> <spec-path> <receipt-path> — round-88 M1 check.
# A pre-registered mutation spec is provably earlier than the first run of its
# mutants only if the commit that first adds the spec is a STRICT ancestor of the
# commit that first adds the first receipt carrying a mutant verdict.
# Prints PREREG_ORDER: ok|same-commit|later|missing and exits 0 only on ok.
set -u
repo=$1 spec=$2 receipt=$3
first_add() { git -C "$repo" log --diff-filter=A --format=%H -- "$1" | tail -n 1; }
s=$(first_add "$spec"); r=$(first_add "$receipt")
if [[ -z "$s" || -z "$r" ]]; then
  printf 'PREREG_ORDER: missing spec=%s receipt=%s\n' "${s:-none}" "${r:-none}"; exit 2
fi
if [[ "$s" == "$r" ]]; then
  printf 'PREREG_ORDER: same-commit spec=%s receipt=%s\n' "${s:0:12}" "${r:0:12}"; exit 1
fi
if git -C "$repo" merge-base --is-ancestor "$s" "$r"; then
  printf 'PREREG_ORDER: ok spec=%s receipt=%s\n' "${s:0:12}" "${r:0:12}"; exit 0
fi
printf 'PREREG_ORDER: later spec=%s receipt=%s\n' "${s:0:12}" "${r:0:12}"; exit 1
