#!/bin/sh
# Regenerate .ufo/evidence/round-86/pointer-recheck.out (attempt 3, TameshiR86a3).
#
# Why: attempt 2 hand-drafted the receipt header with `# tool_sha256: e3b0c442…`
# (the empty-string digest) and `# tool:` a wave-dir fixture no revision then
# carried, so tools/receipt-bytes-bind.py read it `state=unbound
# detail=tool-absent` (mistake M8). This script prints the header from
# `sha256sum` and records the commit that carries the fixture as
# `measured_bytes_rev` (criterion-128 two-commit pattern: the records commit
# 7c146da8 carries the fixture, this receipt lands after it).
set -u
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
cd "$L" || exit 1
REV=a01293c75193cc343f36daeaf2f611ec7982286f
BYTES_REV=7c146da87987e8e41a0c89f9d12c731a2d512a32
TOOL=.ufo/waves/round-86/w1/T86S1-pointer-check.py
SNAP=.ufo/evidence/round-86/sources/s305-ls-tree.html
S=${S:-/fast/scratch/hyaku/tameshi-r86/l1/a3}
mkdir -p "$S"

{
  printf '# measured_rev: %s\n' "$REV"
  printf '# measured_bytes_rev: %s\n' "$BYTES_REV"
  printf '# tool: %s\n' "$TOOL"
  printf '# tool_sha256: %s\n' "$(sha256sum "$TOOL" | cut -d' ' -f1)"
  printf '# command: python3 %s --snapshot %s --expect-mode 1808 --expect-type 1812\n' "$TOOL" "$SNAP"
  printf '# date: 2026-11-04, attempt 3 (TameshiR86a3) — regenerated from its own run\n'
  printf '\n'
  python3 -I "$TOOL" --snapshot "$SNAP" --expect-mode 1808 --expect-type 1812
  printf 'POINTER_FIXTURE_EXIT=%s\n' "$?"
  printf '\n--- round-86 artifacts citing 1808/1812 at %s\n' "$REV"
  for f in corpus/lessons/round-86.md corpus/SOURCES.md plans/round-86.plan.md .ufo/evidence/round-86/contract.json; do
    printf '%s %s\n' "$(git show "$REV:$f" | grep -c '1808\|1812')" "$f"
  done
  printf '\n--- frozen 1807/1811 pointers still present (the lesson hit is the M5 amendment record itself)\n'
  printf 'plans/round-86.plan.md %s\n' "$(git show "$REV:plans/round-86.plan.md" | grep -c '1807\|1811')"
  printf 'corpus/lessons/round-86.md %s\n' "$(git show "$REV:corpus/lessons/round-86.md" | grep -c '1807\|1811')"
  printf 'corpus/SOURCES.md %s\n' "$(git show "$REV:corpus/SOURCES.md" | grep -c '1807\|1811')"
} > .ufo/evidence/round-86/pointer-recheck.out
echo "WROTE .ufo/evidence/round-86/pointer-recheck.out"
