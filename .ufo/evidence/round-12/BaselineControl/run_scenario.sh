#!/usr/bin/env bash
# run_scenario.sh — minimal baseline scenario demonstrating single-control limitation
# in tools/mutate-and-run.sh
set -eu -o pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$DIR/../../../.." && pwd)"
RUNNER="$REPO_ROOT/tools/mutate-and-run.sh"

echo "=== Setting up minimal fixtures in $DIR/fixtures ==="
FIXTURES="$DIR/fixtures"
rm -rf "$FIXTURES"
mkdir -p "$FIXTURES"

# 1. Target artifact
cat << 'EOF' > "$FIXTURES/target.sh"
#!/usr/bin/env bash
echo "hello world"
EOF
chmod +x "$FIXTURES/target.sh"

# 2. Defect spec (harmless comment addition / no-op semantic change)
cat << 'EOF' > "$FIXTURES/spec.txt"
@defect D1 | harmless change that should survive
@old hello world
@new hello world # noop
EOF

# ------------------------------------------------------------------------------
# Scenario A: Flaky suite (passes 1st time, fails 2nd time)
# State counter stored in file.
# ------------------------------------------------------------------------------
echo "=== Running Scenario A: Flaky suite (run 1 PASS -> control green; run 2 FAIL -> false positive kill) ==="
STATE_A="$FIXTURES/state_a.txt"
echo 0 > "$STATE_A"

SUITE_A='
c=$(cat "'"$STATE_A"'")
c=$((c + 1))
echo "$c" > "'"$STATE_A"'"
echo "Suite run #$c for DEFECT_ID=$DEFECT_ID"
if [[ "$c" -eq 1 ]]; then
  echo "Run 1 passes"
  exit 0
else
  echo "Run 2 fails due to flakiness"
  exit 1
fi
'

WORKDIR_A="$DIR/workdir-scenario-a"
rm -rf "$WORKDIR_A"
set +e
bash "$RUNNER" \
  --target "$FIXTURES/target.sh" \
  --defects "$FIXTURES/spec.txt" \
  --suite "$SUITE_A" \
  --workdir "$WORKDIR_A" > "$DIR/scenario-a.stdout" 2> "$DIR/scenario-a.stderr"
EXIT_A=$?
set -e
echo "$EXIT_A" > "$DIR/scenario-a.exit"

# ------------------------------------------------------------------------------
# Scenario B: Flaky suite starting on failure (run 1 FAIL -> control red)
# ------------------------------------------------------------------------------
echo "=== Running Scenario B: Flaky suite failing on control (run 1 FAIL -> abort) ==="
STATE_B="$FIXTURES/state_b.txt"
echo 0 > "$STATE_B"

SUITE_B='
c=$(cat "'"$STATE_B"'")
c=$((c + 1))
echo "$c" > "'"$STATE_B"'"
echo "Suite run #$c for DEFECT_ID=$DEFECT_ID"
if [[ "$c" -eq 1 ]]; then
  echo "Run 1 flaked"
  exit 1
else
  echo "Run 2 passes"
  exit 0
fi
'

WORKDIR_B="$DIR/workdir-scenario-b"
rm -rf "$WORKDIR_B"
set +e
bash "$RUNNER" \
  --target "$FIXTURES/target.sh" \
  --defects "$FIXTURES/spec.txt" \
  --suite "$SUITE_B" \
  --workdir "$WORKDIR_B" > "$DIR/scenario-b.stdout" 2> "$DIR/scenario-b.stderr"
EXIT_B=$?
set -e
echo "$EXIT_B" > "$DIR/scenario-b.exit"

# ------------------------------------------------------------------------------
# Scenario C: Nondeterministic output on pristine (exit 0 every time, but differing stdout)
# ------------------------------------------------------------------------------
echo "=== Running Scenario C: Unstable output (exit 0, varying stdout) ==="
SUITE_C='
echo "Timestamp: $(date +%s%N)"
echo "PID: $$"
echo "Random: $RANDOM"
exit 0
'

WORKDIR_C="$DIR/workdir-scenario-c"
rm -rf "$WORKDIR_C"
set +e
bash "$RUNNER" \
  --target "$FIXTURES/target.sh" \
  --defects "$FIXTURES/spec.txt" \
  --suite "$SUITE_C" \
  --workdir "$WORKDIR_C" > "$DIR/scenario-c.stdout" 2> "$DIR/scenario-c.stderr"
EXIT_C=$?
set -e
echo "$EXIT_C" > "$DIR/scenario-c.exit"

# ------------------------------------------------------------------------------
# Scenario D: Persistent nonzero baseline (always exit 1)
# ------------------------------------------------------------------------------
echo "=== Running Scenario D: Nonzero baseline (always exit 1) ==="
SUITE_D='
echo "Baseline broken: cannot evaluate"
exit 1
'

WORKDIR_D="$DIR/workdir-scenario-d"
rm -rf "$WORKDIR_D"
set +e
bash "$RUNNER" \
  --target "$FIXTURES/target.sh" \
  --defects "$FIXTURES/spec.txt" \
  --suite "$SUITE_D" \
  --workdir "$WORKDIR_D" > "$DIR/scenario-d.stdout" 2> "$DIR/scenario-d.stderr"
EXIT_D=$?
set -e
echo "$EXIT_D" > "$DIR/scenario-d.exit"

echo "=== All scenarios completed ==="
