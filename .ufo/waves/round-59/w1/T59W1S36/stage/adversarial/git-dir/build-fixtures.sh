#!/usr/bin/env bash
# Build victim and attacker fixture repos for GIT_DIR poisoning demos.
# Fixture git writes use explicit -C into scratch dirs only.
set -euo pipefail
ROOT="${1:?usage: build-fixtures.sh SCRATCH_ROOT}"
V="$ROOT/fixtures/victim"
A="$ROOT/fixtures/attacker"
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid
export GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid

rm -rf "$V" "$A"
mkdir -p "$V/tools" "$A/tools"

# --- victim: trusted commit T (clean), candidate commit C (forged HEAD) ---
echo 'print("real executor")' > "$V/tools/runner.py"
git -C "$V" init -q
git -C "$V" add -- tools/runner.py
git -C "$V" -c commit.gpgsign=false commit -qm trusted
T=$(git -C "$V" rev-parse HEAD)

echo 'print("forged success")' > "$V/tools/runner.py"
git -C "$V" add -- tools/runner.py
git -C "$V" -c commit.gpgsign=false commit -qm forged
C=$(git -C "$V" rev-parse HEAD)

# --- attacker: HEAD blob equal to trusted content; contains T,C objects? no ---
# Attacker repo is independent: its own HEAD content matches the trusted blob,
# so any gate that reads blobs HERE reports "equal to trusted".
echo 'print("real executor")' > "$A/tools/runner.py"
git -C "$A" init -q
git -C "$A" add -- tools/runner.py
git -C "$A" -c commit.gpgsign=false commit -qm clean-head
AH=$(git -C "$A" rev-parse HEAD)

cat > "$ROOT/fixtures/ids.env" <<EOF
TRUSTED=$T
CANDIDATE=$C
ATTACKER_HEAD=$AH
VICTIM=$V
ATTACKER=$A
EOF
echo "trusted=$T"
echo "candidate=$C"
echo "attacker_head=$AH"
