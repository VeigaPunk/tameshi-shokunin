#!/usr/bin/env bash
# Round-99 records run (amendment A11). Each tool is extracted from the records revision R with
# `git show R:<tool>` into scratch and THOSE bytes run, so the digest a receipt names is the
# digest of the bytes that executed. Tool receipts carry the lane's round-78 header triple
# (`# measured_rev:` / `# tool:` / `# tool_sha256:`) plus `# tree:` and `# cmd:`, and live in
# records/ (bindable by tools/receipt-bytes-bind.py); tool-less receipts live in records-aux/.
# Usage: records-run.sh <lane abs> <R 40-hex> <frozen rev 40-hex> <scratch abs>
set -u
L="$1"; R="$2"; F="$3"; S="$4"
case "$R$F" in *[!0-9a-f]*) echo "bad rev"; exit 2;; esac
[ ${#R} -eq 40 ] && [ ${#F} -eq 40 ] || { echo "bad rev length"; exit 2; }
[ "$(/usr/bin/git -C "$L" rev-parse --show-toplevel)" = "$L" ] || { echo "lane not toplevel"; exit 2; }
[ -n "$S" ] && mkdir -p "$S/tools" || exit 2
O="$L/.ufo/evidence/round-99/records"; X="$L/.ufo/evidence/round-99/records-aux"
mkdir -p "$O" "$X"
export GIT_NO_REPLACE_OBJECTS=1 TMPDIR="$S"
TREE=$(/usr/bin/git -C "$L" rev-parse "$R^{tree}")
cd "$L" || exit 2

pin() {  # extract tool bytes at R into scratch; print the scratch path
  local t="$1" out="$S/tools/$(basename "$1")"
  /usr/bin/git -C "$L" show "$R:$t" > "$out" || exit 2
  printf '%s' "$out"
}
rec() {  # rec <name> <tool path> <args...>   (tool executed from its bytes at R)
  local name="$1" tool="$2"; shift 2
  local bin; bin=$(pin "$tool")
  local sha; sha=$(sha256sum "$bin" | cut -d' ' -f1)
  {
    printf '# measured_rev: %s\n' "$R"
    printf '# tool: %s\n' "$tool"
    printf '# tool_sha256: %s\n' "$sha"
    printf '# tree: %s\n' "$TREE"
    printf '# cmd: python3 -I <git show %s:%s> %s\n' "$R" "$tool" "$*"
    python3 -I "$bin" "$@" 2>&1
    printf 'rc=%d\n' "$?"
  } > "$O/$name.out"
}
aux() {  # aux <name> <cmd...>
  local name="$1"; shift
  { printf '# measured_rev: %s\n# tree: %s\n# cmd: %s\n' "$R" "$TREE" "$*"; "$@" 2>&1; printf 'rc=%d\n' "$?"; } > "$X/$name.out"
}

POP=()
for n in 93 94 95 96 97 98; do POP+=(--record "corpus/lessons/round-$n.md" --record "plans/round-$n.plan.md"); done
T1=tools/tally-reconcile.py; A1=tools/control-assertion-audit.py; A2=tools/control-assertion-audit-v2.py
C2D=.ufo/evidence/round-99/c2

# C1
rec c1-population "$T1" --repo "$L" --rev "$R" "${POP[@]}"
rec c1-r94-only "$T1" --repo "$L" --rev "$R" --record corpus/lessons/round-94.md
rec c1-r93-only "$T1" --repo "$L" --rev "$R" --record corpus/lessons/round-93.md
rec c1-selftest "$T1" --selftest
# C2
for fx in alias-driver alias-driver-renamed alias-driver-chain; do
  rec "c2-v2-$fx" "$A2" --repo "$L" --rev "$R" --driver "$C2D/$fx.py"
  rec "c2-v1-$fx" "$A1" --repo "$L" --rev "$R" --driver "$C2D/$fx.py"
done
for d in 98 97; do
  drv=".ufo/evidence/round-$d/controls$d.py"
  rec "c2-v1-controls$d" "$A1" --repo "$L" --rev "$R" --driver "$drv"
  rec "c2-v2-controls$d" "$A2" --repo "$L" --rev "$R" --driver "$drv"
  aux "c2-site-diff-controls$d" diff <(grep -E '^CONTROL_ASSERT(_SITE| )' "$O/c2-v1-controls$d.out") <(grep -E '^CONTROL_ASSERT(_SITE| )' "$O/c2-v2-controls$d.out")
done
rec c2-v2-selftest "$A2" --selftest
rec c2-v1-selftest "$A1" --selftest
# before tokens at the base, and the isolation refusal (A10)
B=$(cat "$L/.ufo/waves/round-99/base-rev.txt")
aux c1-before-token /usr/bin/git -C "$L" grep -c TALLY_RECONCILE "$B" -- .
aux c2-before-token /usr/bin/git -C "$L" grep -c CONTROL_ASSERT_RECORDERS "$B" -- .
aux a10-no-isolation-c1 python3 "$(pin $T1)" --selftest
aux a10-no-isolation-c2 python3 "$(pin $A2)" --selftest
# amendment discrimination: the new selftest arms against the FROZEN tool bytes at F
/usr/bin/git -C "$L" show "$F:$T1" > "$S/tools/frozen-tally.py"
/usr/bin/git -C "$L" show "$F:$A2" > "$S/tools/frozen-v2.py"
aux a1-a9-discrimination python3 -I "$L/.ufo/evidence/round-99/discriminate.py" "$S/tools/frozen-tally.py" "$(pin $T1)" "$S/tools/frozen-v2.py" "$(pin $A2)"
# receipt binding over records/ (the lane's own binder, A11)
aux receipt-bytes-bind python3 -I -X utf8 "$(pin tools/receipt-bytes-bind.py)" --repo "$L" --root .ufo/evidence/round-99/records
grep -H -E '^(TALLY_RECONCILE|CONTROL_ASSERT |CONTROL_ASSERT_RECORDERS|[A-Z_0-9]+_SELFTEST:|RECEIPT_BIND:|DISCRIM|rc=)' "$O"/*.out "$X"/*.out
