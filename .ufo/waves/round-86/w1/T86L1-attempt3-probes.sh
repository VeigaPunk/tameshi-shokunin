#!/bin/sh
# attempt-3 (TameshiR86a3) probe battery: the two frozen instruments' PATH
# channel and their fail-closed behaviour under a poisoned `git`.
# Read-only against the lane; every write lands in $S (scratch).
set -u
S=${S:-/fast/scratch/hyaku/tameshi-r86/l1/a3}
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
REV=$(git -C "$L" rev-parse refs/heads/master)
mkdir -p "$S/shim" "$S/work"
printf 'REV=%s\n' "$REV"

# --- shim 1: logging pass-through (records every git argv the instrument issues)
cat > "$S/shim/git" <<'EOS'
#!/bin/sh
printf '%s\n' "$*" >> "$SHIM_LOG"
exec /usr/bin/git "$@"
EOS
chmod +x "$S/shim/git"

echo "=== P1: measure.py under a logging PATH shim ==="
SHIM_LOG="$S/p1-calls.log" PATH="$S/shim:$PATH" \
  python3 -I "$L/.ufo/evidence/round-86/measure.py" --repo "$L" --rev "$REV" \
  --work "$S/work/p1" > "$S/p1.out" 2>&1
echo "P1_EXIT=$?"
tail -2 "$S/p1.out"
echo "P1 git argv issued (first 6):"
sed -n '1,6p' "$S/p1-calls.log"
echo "P1 argv count: $(wc -l < "$S/p1-calls.log")"

echo "=== P2: capability-census.py under the same logging shim ==="
rm -f "$S/p2-calls.log"
SHIM_LOG="$S/p2-calls.log" PATH="$S/shim:$PATH" \
  python3 -I -X utf8 "$L/tools/capability-census.py" --repo "$L" --rev "$REV" \
  > "$S/p2.out" 2>&1
echo "P2_EXIT=$?"
tail -2 "$S/p2.out"
echo "P2 git argv issued (first 4):"
sed -n '1,4p' "$S/p2-calls.log"
echo "P2 argv count: $(wc -l < "$S/p2-calls.log")"

# --- shim 2: hostile `git` that always fails
mkdir -p "$S/shimfail"
printf '#!/bin/sh\nexit 127\n' > "$S/shimfail/git"
chmod +x "$S/shimfail/git"

echo "=== P3: measure.py with a failing git (must not print a pass) ==="
PATH="$S/shimfail:$PATH" python3 -I "$L/.ufo/evidence/round-86/measure.py" \
  --repo "$L" --rev "$REV" --work "$S/work/p3" > "$S/p3.out" 2>&1
echo "P3_EXIT=$?"
grep -c 'C1_R86_PASS=true' "$S/p3.out" | sed 's/^/P3_PASS_LINES=/'
tail -2 "$S/p3.out"

echo "=== P4: capability-census.py with a failing git ==="
PATH="$S/shimfail:$PATH" python3 -I -X utf8 "$L/tools/capability-census.py" \
  --repo "$L" --rev "$REV" > "$S/p4.out" 2>&1
echo "P4_EXIT=$?"
tail -2 "$S/p4.out"

echo "=== P5: census manifest accepted from outside the repo (absolute path) ==="
cp "$L/tools/capability-census.json" "$S/outside-manifest.json"
python3 -I -X utf8 "$L/tools/capability-census.py" --repo "$L" --rev "$REV" \
  --manifest "$S/outside-manifest.json" > "$S/p5.out" 2>&1
echo "P5_EXIT=$?"
tail -1 "$S/p5.out"

echo "=== P6: census against a non-repository path ==="
python3 -I -X utf8 "$L/tools/capability-census.py" --repo /etc --rev "$REV" \
  > "$S/p6.out" 2>&1
echo "P6_EXIT=$?"
tail -2 "$S/p6.out"
