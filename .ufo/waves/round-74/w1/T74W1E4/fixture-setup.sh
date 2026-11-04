#!/usr/bin/env bash
# fixture-setup.sh — synthetic validation of scan.py (seat T74W1E4, round 74).
# Builds a throwaway git repo under $HYAKU_SCRATCH/tameshi-r74/T74W1E4 with a
# known append / CRLF-rewrite / content-alter / delete / CRLF-revert series,
# then runs scan.py and prints one ROW per commit. Expected numbers are named
# in the transcript lines below; they are checked by the author against the
# output (the scan itself does not assert).
set -e
S="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r74/T74W1E4"
mkdir -p "$S"
D=$(mktemp -d "$S/fixture.XXXXXX")
git -C "$D" init -q
T=$(git -C "$D" rev-parse --show-toplevel)
test "$T" = "$D" || { echo "TOPLEVEL MISMATCH $T != $D" >&2; exit 1; }
git -C "$D" config user.email "fixture@example.invalid"
git -C "$D" config user.name "fixture"

# c1: a b c d (LF)
printf 'a\nb\nc\nd\n' > "$D/F.md"; git -C "$D" add F.md; git -C "$D" commit -qm c1
# c2: append e                      -> raw_old=0 new=1 norm=0 prefix=true
printf 'e\n' >> "$D/F.md"; git -C "$D" add F.md; git -C "$D" commit -qm c2
# c3: rewrite all to CRLF + append f -> raw_old=5 new=6 norm=0 prefix=true disclosed
python3 - "$D/F.md" <<'PY'
import sys
p = sys.argv[1]; b = open(p, 'rb').read().replace(b'\n', b'\r\n')
open(p, 'wb').write(b + b'f\r\n')
PY
git -C "$D" add F.md; git -C "$D" commit -qm c3
# c4: alter c -> C                  -> raw_old=1 new=1 norm=1 prefix=false
python3 - "$D/F.md" <<'PY'
import sys
p = sys.argv[1]; b = open(p, 'rb').read()
open(p, 'wb').write(b.replace(b'c\r\n', b'C\r\n'))
PY
git -C "$D" add F.md; git -C "$D" commit -qm c4
# c5: delete d                      -> raw_old=1 new=0 norm=1 prefix=false
python3 - "$D/F.md" <<'PY'
import sys
p = sys.argv[1]; b = open(p, 'rb').read()
open(p, 'wb').write(b.replace(b'd\r\n', b''))
PY
git -C "$D" add F.md; git -C "$D" commit -qm c5
# c6: CRLF -> LF (no content change) -> raw_old=5 new=5 norm=0 prefix=true disclosed
python3 - "$D/F.md" <<'PY'
import sys
p = sys.argv[1]; b = open(p, 'rb').read()
open(p, 'wb').write(b.replace(b'\r\n', b'\n'))
PY
git -C "$D" add F.md; git -C "$D" commit -qm c6

echo "FIXTURE D=$D"
git -C "$D" rev-list --reverse HEAD | cat -n
echo "=== FIXTURE SCAN ==="
python3 "$(dirname "$0")/scan.py" --repo "$D" --base "$(git -C "$D" rev-list --max-parents=0 HEAD)" \
  --tip HEAD --path F.md
