#!/usr/bin/env bash
# Independent fixture construction for round-59 cell: path 'tools/日本語.py' (measure.py ix=2).
# Replicates frozen measure.py construction exactly; logs every command + output.
set -euo pipefail
SCRATCH=/fast/scratch/hyaku/tameshi-r59/T59W1S13
FIX="$SCRATCH/fixture"
PATHCELL='tools/日本語.py'
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 TMPDIR="$SCRATCH"
unset $(env | sed -n 's/^\(GIT_[A-Z_]*\)=.*/\1/p') 2>/dev/null || true

log() { echo "== $*"; }
run() { echo "+ $*"; "$@"; echo "  rc=$?"; }

rm -rf "$FIX"
run git init -q "$FIX"
TOP="$(git -C "$FIX" rev-parse --show-toplevel)"
log "fixture toplevel: $TOP"
[ "$(readlink -f "$TOP")" = "$(readlink -f "$FIX")" ] && log "toplevel assert: OK" || { log "toplevel assert: MISMATCH"; exit 1; }

mkdir -p "$FIX/tools"
printf 'print("real executor")\n' > "$FIX/$PATHCELL"
log "byte count of initial content: $(wc -c < "$FIX/$PATHCELL")"
run git -C "$FIX" add -- "$PATHCELL"
run git -C "$FIX" -c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false commit -qm fixture
TRUSTED="$(git -C "$FIX" rev-parse HEAD)"
log "TRUSTED=$TRUSTED"

printf 'print("forged success")\n' > "$FIX/$PATHCELL"
run git -C "$FIX" add -- "$PATHCELL"
run git -C "$FIX" -c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false commit -qm fixture
CHANGED="$(git -C "$FIX" rev-parse HEAD)"
log "CHANGED=$CHANGED"

log "--- source-object verification at TRUSTED ---"
run git -C "$FIX" ls-tree "$TRUSTED" -- "$PATHCELL"
TBLOB="$(git -C "$FIX" rev-parse "$TRUSTED:$PATHCELL")"
log "TRUSTED blob oid: $TBLOB"
run git -C "$FIX" cat-file -t "$TBLOB"
run git -C "$FIX" cat-file -s "$TBLOB"
run git -C "$FIX" show "$TRUSTED:$PATHCELL"
log "sha256 of trusted blob content:"
git -C "$FIX" show "$TRUSTED:$PATHCELL" | sha256sum

log "--- source-object verification at CHANGED ---"
run git -C "$FIX" ls-tree "$CHANGED" -- "$PATHCELL"
CBLOB="$(git -C "$FIX" rev-parse "$CHANGED:$PATHCELL")"
log "CHANGED blob oid: $CBLOB"
run git -C "$FIX" cat-file -t "$CBLOB"
run git -C "$FIX" cat-file -s "$CBLOB"
run git -C "$FIX" show "$CHANGED:$PATHCELL"

log "--- object identity facts ---"
log "trusted==changed commit? $([ "$TRUSTED" = "$CHANGED" ] && echo yes || echo no)"
log "trusted blob==changed blob? $([ "$TBLOB" = "$CBLOB" ] && echo yes || echo no)"
log "full ls-tree trusted:"; git -C "$FIX" ls-tree -r "$TRUSTED"
log "full ls-tree changed:"; git -C "$FIX" ls-tree -r "$CHANGED"
log "on-disk name bytes (od):"; printf '%s' "$PATHCELL" | od -An -tx1
log "git index name at trusted (ls-files --stage):"; git -C "$FIX" ls-files --stage

cat > "$SCRATCH/cell.env" <<EOF
FIXTURE=$FIX
TRUSTED=$TRUSTED
CHANGED=$CHANGED
TRUSTED_BLOB=$TBLOB
CHANGED_BLOB=$CBLOB
PATHCELL=$PATHCELL
EOF
log "cell.env written"
