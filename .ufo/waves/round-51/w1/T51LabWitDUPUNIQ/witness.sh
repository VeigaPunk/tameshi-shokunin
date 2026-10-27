#!/usr/bin/env bash
# T51LabWitDUPUNIQ — C2 survivor witness for S_DUP_UNIQ.
# Gate: kagi corpus/drift-pins.sh @ e64e81b8eb96f3682b00c1e7a291e84420b280fa
#   (blob sha256 c138d34c…). Mutant S_DUP_UNIQ: one line,
#   `uniq -d` -> `uniq -u` in the default-baseline DUP membership block.
# Builds a scratch HOME + gate dir whose DEFAULT_BASELINE sits next to the
# script copy (membership block active), materializes the 15 hardcoded FILES
# paths, lets the gate's own --pin write a truthful baseline, then runs
# pristine and mutant on identical witness inputs, 3 reps each.
# Everything is confined to the scratch root given as $1; real $HOME is never
# touched (env -i, HOME/TMPDIR pointed into the scratch root).
set -euo pipefail

S=${1:?usage: witness.sh <scratch-root>}
W=$S/wit
O=$S/out
GATE=$W/gate
rm -rf "$W" "$O"
mkdir -p "$W/home" "$GATE" "$O" "$S/tmp"

PRISTINE=$S/pristine.sh
MUTANT=$S/mutant.sh
[[ -f $PRISTINE && -f $MUTANT ]] || { echo "need $PRISTINE and $MUTANT" >&2; exit 2; }
cp "$PRISTINE" "$GATE/drift-pins-pristine.sh"
cp "$MUTANT"   "$GATE/drift-pins-mutant.sh"

E=(env -i "HOME=$W/home" "TMPDIR=$S/tmp" PATH=/usr/bin:/bin)

# --- 1. materialize the 15 hardcoded FILES paths under the scratch HOME ----
mk() { # mk <path-under-HOME> <printf-%b-content> <mode>
  mkdir -p "$W/home/$(dirname "$1")"
  printf '%b' "$2" > "$W/home/$1"
  chmod "$3" "$W/home/$1"
}
mk .local/bin/the-janitor                '#!/usr/bin/env bash\necho the-janitor\n' 755
mk .config/the-janitor/client.py         '# client\nserve()\n'                     644
mk .config/the-janitor/opencode.json     '{"a":1}\n'                               644
mk .config/the-janitor/config.json       '{"b":2}\n'                               600
mk .config/the-janitor/op.env            'A=1\nB=2\n'                              600
mk .config/opencode/opencode.json        '{"c":3}\n'                               644
mk .config/opencode/agents/janitor.md    '# janitor\n'                             644
mk .config/opencode/tools/janitor_auth.ts 'export const k = 1\n'                   644
mk .config/opencode/plugin/fnm-nudge.js  'export function n() {}\n'                644
mk .local/bin/tac-check                  '#!/usr/bin/env bash\necho tac\n'         755
mk .local/state/tac/daybreak-blue-access.json '{}\n'                              600
mk .local/state/the-janitor/tac-daybreak-blue.json '{}\n'                          600
mk .local/state/tac/handoff-status.json  'status=idle\n'                           600
mk .agents/AGENTS.md                     '# agents\n'                              644
mk .local/share/the-musketeer/chrome-profile/NativeMessagingHosts/com.1password.1password.json '{}\n' 644

# --- 2. seed one symbol row; the gate's own --pin writes the baseline ------
printf '%s\t%s\t%s\n' '$HOME/.local/bin/the-janitor' 1 '^#!' > "$GATE/drift-symbols.tsv"
"${E[@]}" bash "$GATE/drift-pins-pristine.sh" --pin > "$O/pin.out" 2>&1
cp "$GATE/drift-baseline.tsv" "$O/baseline.pinned.tsv"

run3() { # run3 <gate-script> <tag> — 3 reps, capture out/err/exit
  local g=$1 tag=$2 i rc
  for i in 1 2 3; do
    if "${E[@]}" bash "$g" > "$O/${tag}.$i.out" 2> "$O/${tag}.$i.err"; then rc=0; else rc=$?; fi
    printf '%s\n' "$rc" > "$O/${tag}.$i.exit"
  done
}

# --- C: control — pinned baseline, no duplicate row ------------------------
cp "$O/baseline.pinned.tsv" "$GATE/drift-baseline.tsv"
run3 "$GATE/drift-pins-pristine.sh" C-pristine
run3 "$GATE/drift-pins-mutant.sh"   C-mutant

# --- A: item witness — one duplicated baseline row -------------------------
cp "$O/baseline.pinned.tsv" "$GATE/drift-baseline.tsv"
grep -F '$HOME/.agents/AGENTS.md' "$O/baseline.pinned.tsv" >> "$GATE/drift-baseline.tsv"
cp "$GATE/drift-baseline.tsv" "$O/baseline.A-dup.tsv"
run3 "$GATE/drift-pins-pristine.sh" A-pristine
run3 "$GATE/drift-pins-mutant.sh"   A-mutant
diff -u "$O/A-pristine.1.out" "$O/A-mutant.1.out" > "$O/A.diff" || true

# --- B: exit-flip witness — every row duplicated ----------------------------
awk '{print; print}' "$O/baseline.pinned.tsv" > "$GATE/drift-baseline.tsv"
cp "$GATE/drift-baseline.tsv" "$O/baseline.B-alldup.tsv"
run3 "$GATE/drift-pins-pristine.sh" B-pristine
run3 "$GATE/drift-pins-mutant.sh"   B-mutant
diff -u "$O/B-pristine.1.out" "$O/B-mutant.1.out" > "$O/B.diff" || true

# --- integrity: gate scripts do not self-modify across runs ----------------
{
  sha256sum "$GATE/drift-pins-pristine.sh" "$GATE/drift-pins-mutant.sh"
} > "$O/sha256.after.txt"
cp "$S/pristine.sh" "$S/mutant.sh" "$GATE/" 2>/dev/null || true
sha256sum "$GATE/pristine.sh" "$GATE/mutant.sh" | sed 's#.*/##' > "$O/sha256.before-copy.txt"

# --- ledger -----------------------------------------------------------------
{
  echo "== exits (3 reps each) =="
  for t in C-pristine C-mutant A-pristine A-mutant B-pristine B-mutant; do
    printf '%-14s %s\n' "$t" "$(paste -sd, "$O/$t".[123].exit)"
  done
  echo "== last lines (rep 1) =="
  for t in C-pristine C-mutant A-pristine A-mutant B-pristine B-mutant; do
    printf '%-14s | %s\n' "$t" "$(tail -n 1 "$O/$t.1.out")"
  done
} > "$O/ledger.txt"
cat "$O/ledger.txt"
