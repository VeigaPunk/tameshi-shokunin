#!/usr/bin/env bash
# Round-99 pre-freeze controls. Every receipt records its own command line, revision and tool
# digest in `# ` header lines (round-98 spot-check D3), then the tool's stdout+stderr, then `rc=N`.
# Usage: pre-freeze-run.sh <lane abs path> <instrument rev 40-hex> <base rev 40-hex> <outdir abs>
set -u
L="$1"; I="$2"; B="$3"; O="$4"
case "$I$B" in *[!0-9a-f]*) echo "bad rev"; exit 2;; esac
[ ${#I} -eq 40 ] && [ ${#B} -eq 40 ] || { echo "bad rev length"; exit 2; }
[ "$(/usr/bin/git -C "$L" rev-parse --show-toplevel)" = "$L" ] || { echo "lane not toplevel"; exit 2; }
mkdir -p "$O"
export GIT_NO_REPLACE_OBJECTS=1
cd "$L" || exit 2

rec() {  # rec <name> <tool path or -> <cmd...>
  local name="$1" tool="$2"; shift 2
  local f="$O/$name.out" sha="-"
  [ "$tool" != "-" ] && sha=$(/usr/bin/git -C "$L" show "$I:$tool" | sha256sum | cut -d' ' -f1)
  {
    printf '# cmd: %s\n' "$*"
    printf '# cwd: %s\n' "$L"
    printf '# instrument_rev: %s\n' "$I"
    printf '# tool: %s\n' "$tool"
    printf '# tool_sha256_at_rev: %s\n' "$sha"
    "$@" 2>&1
    printf 'rc=%d\n' "$?"
  } > "$f"
}

POP=""
for n in 93 94 95 96 97 98; do POP="$POP --record corpus/lessons/round-$n.md --record plans/round-$n.plan.md"; done
T1=tools/tally-reconcile.py
A1=tools/control-assertion-audit.py
A2=tools/control-assertion-audit-v2.py
FX=.ufo/evidence/round-99/c2/alias-driver.py
D98=.ufo/evidence/round-98/controls98.py
D97=.ufo/evidence/round-97/controls97.py

# C1
# shellcheck disable=SC2086
rec c1-population "$T1" python3 -I "$T1" --repo "$L" --rev "$I" $POP
rec c1-selftest "$T1" python3 -I "$T1" --selftest
rec c1-before-token - /usr/bin/git -C "$L" grep -c TALLY_RECONCILE "$B" -- .
rec c1-r94-only "$T1" python3 -I "$T1" --repo "$L" --rev "$I" --record corpus/lessons/round-94.md
# C2
rec c2-v1-fixture "$A1" python3 -I "$A1" --repo "$L" --rev "$I" --driver "$FX"
rec c2-v2-fixture "$A2" python3 -I "$A2" --repo "$L" --rev "$I" --driver "$FX"
rec c2-v1-controls98 "$A1" python3 -I "$A1" --repo "$L" --rev "$I" --driver "$D98"
rec c2-v2-controls98 "$A2" python3 -I "$A2" --repo "$L" --rev "$I" --driver "$D98"
rec c2-v1-controls97 "$A1" python3 -I "$A1" --repo "$L" --rev "$I" --driver "$D97"
rec c2-v2-controls97 "$A2" python3 -I "$A2" --repo "$L" --rev "$I" --driver "$D97"
rec c2-v2-selftest "$A2" python3 -I "$A2" --selftest
rec c2-v1-selftest "$A1" python3 -I "$A1" --selftest
rec c2-before-token - /usr/bin/git -C "$L" grep -c CONTROL_ASSERT_RECORDERS "$B" -- .
# C2 no-regression: the site lines of v1 and v2 agree byte-for-byte on both committed drivers
for d in 98 97; do
  {
    printf '# cmd: diff <(grep ^CONTROL_ASSERT_SITE c2-v1-controls%s.out) <(grep ^CONTROL_ASSERT_SITE c2-v2-controls%s.out)\n' "$d" "$d"
    printf '# instrument_rev: %s\n' "$I"
    diff <(grep '^CONTROL_ASSERT_SITE' "$O/c2-v1-controls$d.out") <(grep '^CONTROL_ASSERT_SITE' "$O/c2-v2-controls$d.out")
    printf 'rc=%d\n' "$?"
    printf 'site_lines=%d\n' "$(grep -c '^CONTROL_ASSERT_SITE' "$O/c2-v2-controls$d.out")"
  } > "$O/c2-site-diff-controls$d.out"
done
grep -H -E '^(TALLY_RECONCILE|CONTROL_ASSERT |CONTROL_ASSERT_RECORDERS|[A-Z_]+_SELFTEST:|rc=|site_lines=|[0-9])' "$O"/*.out | grep -v '^.*SELFTEST [A-Z]'
