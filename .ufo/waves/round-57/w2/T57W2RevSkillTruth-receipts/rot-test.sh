#!/usr/bin/env bash
# Rot tests: history rewrite (orphan WITH the tree), live mode, and shelf-life probes.
set -u
S=/fast/scratch/hyaku/tameshi-r57/T57W2RevSkillTruth
D=$S/desc
C0=ca75c2674645ab6bdadeecb8584007c74342bfa9
BASE=5e3569969b532310d2b8a3d130901757a3df356b
RECV=c34e2b1486714ad6c1c6cbe706599ddfc9d60d55

top=$(git -C "$D" rev-parse --show-toplevel)
[ "$top" = "$(cd "$D" && pwd -P)" ] || { echo "TOPLEVEL_FAIL"; exit 2; }
echo "TOPLEVEL_OK $top"

echo
echo "=== E. history rewrite: orphan commit that KEEPS the C0 tree (pinned revs unreachable)"
git -C "$D" checkout -q --detach "$C0"
git -C "$D" checkout -q --orphan orphan-tree
git -C "$D" rm -rq --cached . >/dev/null 2>&1
# restore the working tree files (checkout removed them from the index only)
git -C "$D" checkout -q -- . 2>/dev/null || true
git -C "$D" add -A >/dev/null 2>&1
git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "orphan with the C0 tree, no pinned history"
ORPH=$(git -C "$D" rev-parse HEAD)
echo "orphan-with-tree=$ORPH"
echo "  base resolvable?   $(git -C "$D" rev-parse --verify --quiet "$BASE^{commit}" || echo NO)"
echo "  receipt rev resolvable? $(git -C "$D" rev-parse --verify --quiet "$RECV^{commit}" || echo NO)"
echo "  registry.json present? $(test -f "$D/tools/registry.json" && echo YES || echo NO)"
( cd "$D" && python3 tools/registry-check.py --rev "$ORPH" --tag new-r57 ); echo "   rc=$?"

echo
echo "=== F. live mode (no --rev) in a scratch clone at C0"
git -C "$D" checkout -q --detach "$C0"
( cd "$D" && python3 tools/registry-check.py --tag new-r57 ); echo "   rc=$?"

echo
echo "=== G. shelf-life: does the accept row still hold if the fixture receipt is edited?"
git -C "$D" checkout -q --detach "$C0"
printf 'VERDICT: rev=%s C2_FIXTURE_PASS=true\n' "$RECV" > "$D/tools/fixtures/receipt-gate/accept.receipt"
git -C "$D" add -A
git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "edit the accept fixture to name an older rev"
( cd "$D" && python3 tools/registry-check.py --rev HEAD --tag new-r57 ); echo "   rc=$?"

echo
echo "=== H. shelf-life: does the accept row still hold if the fixture is RENAMED?"
git -C "$D" checkout -q --detach "$C0"
git -C "$D" mv tools/fixtures/receipt-gate/accept.receipt tools/fixtures/receipt-gate/accept2.receipt
git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "rename the accept fixture"
( cd "$D" && python3 tools/registry-check.py --rev HEAD --tag new-r57 ); echo "   rc=$?"

echo
echo "=== I. shelf-life: drift row when the paths fixture names a path that differs in NO revision"
git -C "$D" checkout -q --detach "$C0"
printf 'corpus/QUALITY.md\n' > "$D/tools/fixtures/receipt-gate/drift.paths"
git -C "$D" add -A
git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "repoint the drift paths fixture at an unrelated file"
( cd "$D" && python3 tools/registry-check.py --rev HEAD --tag new-r57 --only receipt-gate-content-drift ); echo "   rc=$?"
echo "   (detail line:)"
( cd "$D" && python3 tools/receipt-revision-gate.py --lane . --certified "$BASE" --paths tools/fixtures/receipt-gate/drift.paths --receipt tools/fixtures/receipt-gate/drift.receipt:positive ) 2>&1 | head -3
