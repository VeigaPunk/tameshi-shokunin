#!/bin/sh
# Rebuild the F1 fixtures and rerun the C0 pin-disposition probe.
# Usage: ./reproduce.sh   (needs a writable scratch root; writes only under $S)
set -eu
LANE=${LANE:-/home/vgpnk/Projects/shokunin/tameshi-shokunin}
REV=${REV:-59c38109bf119d0e9d4f878644a82babc937bc1e}
HYAKU_SCRATCH=${HYAKU_SCRATCH:-/fast/scratch/hyaku}
S=$(mktemp -d "$HYAKU_SCRATCH/t54w1read13-repro.XXXXXX")
trap 'rm -rf -- "$S"' EXIT
export TMPDIR="$S/tmp"; mkdir -p "$TMPDIR"

git clone --shared -q "$LANE" "$S/lane"
git -C "$S/lane" checkout -q "$REV"
test "$(git -C "$S/lane" rev-parse HEAD)" = "$REV"

R="$S/root"; mkdir -p "$R"
mkrepo() {
  d=$R/$1; mkdir -p "$d/$(dirname "$2")"
  printf '%s' "$3" > "$d/$2"
  git -C "$d" init -q
  git -C "$d" add -- "$2"
  git -C "$d" -c user.name=f -c user.email=f@example.invalid commit -q -m fixture
}
mkrepo kumitate-shokunin scripts/kimi-census.mjs 'KIMI-BYTES-X'
mkrepo kumitate-shokunin scripts/claims-check.mjs 'CLAIMS-BYTES-X'
mkrepo kagi-shokunin corpus/surface-census.sh 'SURFACE-BYTES-X'
mkrepo kagi-shokunin corpus/checklist-run.sh 'CHECKLIST-BYTES-X'
mkrepo tsukuroi-shokunin tools/tsukuroi-census.sh 'TSUKUROI-BYTES-X'
mkrepo mado-shokunin tools/mado-verify.sh 'MADO-BYTES-X'

python3 - "$R" "$S" <<'PY'
import hashlib, json, os, subprocess, sys
root, out = sys.argv[1], sys.argv[2]
legs = [("js-kimi-census", "kumitate-shokunin", "scripts/kimi-census.mjs"),
        ("bash-surface-census", "kagi-shokunin", "corpus/surface-census.sh"),
        ("bash-tsukuroi-census", "tsukuroi-shokunin", "tools/tsukuroi-census.sh"),
        ("bash-mado-verify", "mado-shokunin", "tools/mado-verify.sh"),
        ("bash-checklist-run", "kagi-shokunin", "corpus/checklist-run.sh"),
        ("js-claims-check", "kumitate-shokunin", "scripts/claims-check.mjs")]
rows = []
for leg, repo, path in legs:
    d = os.path.join(root, repo)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    sha = hashlib.sha256(open(os.path.join(d, path), "rb").read()).hexdigest()
    if leg == "js-kimi-census":
        sha = hashlib.sha256(b"KIMI-WRONG-DIGEST-Y").hexdigest()
    rows.append({"leg": leg, "repo": repo, "path": path, "pinned_commit": rev,
                 "expected_sha256": sha, "pinned_source": "fixture"})
json.dump({"schema": "pin-manifest-v1",
           "source": "fixture A: manifest digest disagrees with the pinned blob; worktree bytes equal it",
           "legs": rows}, open(os.path.join(out, "manifest-a.json"), "w"), indent=1)
for e in rows:
    if e["leg"] == "js-kimi-census":
        e["expected_sha256"] = hashlib.sha256(b"KIMI-WRONG-DIGEST-Y").hexdigest()
json.dump({"schema": "pin-manifest-v1",
           "source": "fixture B: manifest digest equals the worktree; pinned blob differs",
           "legs": rows}, open(os.path.join(out, "manifest-b.json"), "w"), indent=1)
PY
# Fixture B needs the worktree bytes at the manifest digest, not the committed blob.
printf '%s' 'KIMI-WRONG-DIGEST-Y' > "$R/kumitate-shokunin/scripts/kimi-census.mjs"

# Rebuild fixture A state for its run (worktree back to the committed blob).
git -C "$R/kumitate-shokunin" checkout -q -- scripts/kimi-census.mjs
cd "$S/lane"
echo "A:"
python3 tools/pin-disposition.py --manifest "$S/manifest-a.json" --root "$R" \
  | python3 -c 'import json,sys; p=json.load(sys.stdin); r=[x for x in p["legs"] if x["leg"]=="js-kimi-census"][0]; print("counts", p["counts"]); print("pinned", r["pinned"]["blob_sha256"], r["pinned"]["status"]); print("worktree", r["worktree"]["sha256"], r["worktree"]["status"], r["worktree"]["reason"]); print("content_status", r["content_status"])'
printf '%s' 'KIMI-WRONG-DIGEST-Y' > "$R/kumitate-shokunin/scripts/kimi-census.mjs"
echo "B:"
python3 tools/pin-disposition.py --manifest "$S/manifest-b.json" --root "$R" \
  | python3 -c 'import json,sys; p=json.load(sys.stdin); r=[x for x in p["legs"] if x["leg"]=="js-kimi-census"][0]; print("counts", p["counts"]); print("pinned", r["pinned"]["blob_sha256"], r["pinned"]["status"]); print("worktree", r["worktree"]["sha256"], r["worktree"]["status"], r["worktree"]["reason"]); print("content_status", r["content_status"])'
