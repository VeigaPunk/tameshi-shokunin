#!/bin/bash
# head-vs-branch.sh — jj-colocation hazard fixture for tools/pin-disposition.py
# (tameshi-shokunin, round 17; wave-1 build, follow-up-2 GIT_* scrub).
#
# Reproduces JjAuditTameshi.md §2.3: under jj colocation, git HEAD can be a
# detached jj working-copy snapshot commit (jj's `@-`) one commit ahead of the
# `master` bookmark, carrying unbookmarked bytes. pin-disposition.py's
# head_observation at rev 98bea7d resolved `HEAD^{commit}` verbatim, so on a
# jj-worked lane it reports snapshot bytes as the repo's "current" head; the
# landed (eb7838b) tool resolves the branch tip instead.
#
# Fixture (all under mktemp in /tmp, removed on exit):
#   $SCRATCH/fleet/                     fleet root (a plain dir; leg repos are
#                                       validated by the tool's own
#                                       repo_identity toplevel guard)
#   $SCRATCH/fleet/kagi-shokunin/       git repo, branch `master`
#     commit V1C (master tip): corpus/surface-census.sh = v1 bytes
#     detached HEAD commit HEADC (child of V1C, not on any branch):
#       corpus/surface-census.sh = v2 bytes   <- emulates jj `@-` snapshot:
#       master..HEAD = 1, HEAD detached, HEAD:path carries unbookmarked bytes
#
# A minimal pin-manifest-v1 is written pinning V1C + v1 sha256 for the kagi
# surface-census leg. The other five recorded legs are present (the tool
# rejects manifests that omit a leg) but pin unavailable placeholders; their
# rows are irrelevant to the verdict.
#
# Harness hygiene (round-17 lesson S063 / 12:29:33 incident): every inherited
# GIT_* variable is unset before the first fixture git call — an exported
# GIT_DIR otherwise redirects `git -C` so fixture commits land in the victim
# repo. Only the deliberately re-pinned variables below are then exported.
# After init the fixture asserts `git rev-parse --absolute-git-dir` resolves
# under $SCRATCH.
#
# Usage: head-vs-branch.sh <path to pin-disposition.py>
# Exit:  0  tool's head observation used master's tip (commit V1C, v1 bytes)
#        1  tool's head observation used the detached HEAD commit or its v2
#           bytes — red: unpushed snapshot state is reported as the repo head
#        2  setup or evaluation failure (fixture could not be built, the tool
#           did not emit a usable observation document, or head.* matched
#           neither fixture commit/blob pair)

set -u

TOOL="${1:-}"
if [ -z "$TOOL" ]; then
    echo "usage: $0 <path to pin-disposition.py>" >&2
    exit 2
fi
if [ ! -f "$TOOL" ]; then
    echo "SETUP-FAIL: tool not found: $TOOL" >&2
    exit 2
fi
for dep in git python3 sha256sum realpath; do
    if ! command -v "$dep" >/dev/null 2>&1; then
        echo "SETUP-FAIL: dependency missing: $dep" >&2
        exit 2
    fi
done

SCRATCH=$(mktemp -d /tmp/tameshi-r17-jj-head-XXXXXX) || {
    echo "SETUP-FAIL: mktemp failed" >&2
    exit 2
}
SCRATCH_REAL=$(realpath -- "$SCRATCH")
cleanup() { rm -rf "$SCRATCH"; }
trap cleanup EXIT

# --- GIT_* scrub -----------------------------------------------------------
# Unset every inherited GIT_* variable (list derived from `env`, per the
# S063 lesson: GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE/GIT_OBJECT_DIRECTORY/
# GIT_COMMON_DIR redirect or corrupt fixture git calls). This runs before any
# fixture git invocation; the pins re-exported next are the only GIT_* this
# script intends.
while IFS='=' read -r _git_name _git_rest; do
    case "$_git_name" in
        GIT_*) unset "$_git_name" ;;
    esac
done < <(env)
unset _git_name _git_rest

# Deliberate pins: no host hooks, templates, or global/system config, fixed
# committer identity, no prompts.
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_TERMINAL_PROMPT=0 \
    GIT_AUTHOR_NAME=head-vs-branch GIT_AUTHOR_EMAIL=fixture@example.invalid \
    GIT_COMMITTER_NAME=head-vs-branch GIT_COMMITTER_EMAIL=fixture@example.invalid
GIT=(git -c init.templateDir="$SCRATCH/git-templates" -c core.hooksPath="$SCRATCH/git-hooks" -c commit.gpgsign=false)

FLEET="$SCRATCH/fleet"
REPO="$FLEET/kagi-shokunin"
RELPATH="corpus/surface-census.sh"
LEG="bash-surface-census"
mkdir -p "$FLEET" "$SCRATCH/git-templates" "$SCRATCH/git-hooks" "$REPO/corpus" || {
    echo "SETUP-FAIL: cannot create fixture dirs" >&2
    exit 2
}

assert_gitdir_under_scratch() {
    local d
    d=$("${GIT[@]}" -C "$REPO" rev-parse --absolute-git-dir 2>/dev/null) || {
        echo "SETUP-FAIL: rev-parse --absolute-git-dir failed in fixture repo" >&2
        exit 2
    }
    d=$(realpath -- "$d")
    case "$d" in
        "$SCRATCH_REAL"/*) : ;;
        *) echo "SETUP-FAIL: fixture git dir escapes scratch: $d not under $SCRATCH_REAL" >&2
           exit 2 ;;
    esac
}

V1='#!/bin/sh
# surface-census fixture v1 (master tip bytes)
exit 0
'
V2='#!/bin/sh
# surface-census fixture v2 (jj working-copy snapshot bytes, not on master)
exit 0
'
printf '%s' "$V1" > "$REPO/$RELPATH"
V1_SHA=$(sha256sum "$REPO/$RELPATH" | cut -d' ' -f1)

if ! "${GIT[@]}" -C "$REPO" init -q -b master; then
    echo "SETUP-FAIL: git init failed" >&2
    exit 2
fi
assert_gitdir_under_scratch
if ! (cd "$REPO" && "${GIT[@]}" add -A && "${GIT[@]}" commit -q -m "v1: master tip"); then
    echo "SETUP-FAIL: v1 commit failed" >&2
    exit 2
fi
MASTER_TIP=$("${GIT[@]}" -C "$REPO" rev-parse HEAD) || {
    echo "SETUP-FAIL: cannot resolve master tip" >&2
    exit 2
}

# Emulate jj's `@-` state per JjAuditTameshi.md §2.3: a detached commit one
# ahead of master carrying snapshot bytes. (Real `jj` colocation leaves the
# same observable git state: detached HEAD, master..HEAD = 1, HEAD blob = v2.)
if ! "${GIT[@]}" -C "$REPO" checkout -q --detach master; then
    echo "SETUP-FAIL: detach failed" >&2
    exit 2
fi
printf '%s' "$V2" > "$REPO/$RELPATH"
V2_SHA=$(sha256sum "$REPO/$RELPATH" | cut -d' ' -f1)
if ! (cd "$REPO" && "${GIT[@]}" add -A && "${GIT[@]}" commit -q -m "jj working-copy snapshot (@- emulation)"); then
    echo "SETUP-FAIL: detached snapshot commit failed" >&2
    exit 2
fi
HEAD_DETACHED=$("${GIT[@]}" -C "$REPO" rev-parse HEAD) || {
    echo "SETUP-FAIL: cannot resolve detached HEAD" >&2
    exit 2
}
assert_gitdir_under_scratch
if "${GIT[@]}" -C "$REPO" symbolic-ref -q HEAD >/dev/null; then
    echo "SETUP-FAIL: HEAD is attached, fixture invalid" >&2
    exit 2
fi
if [ "$HEAD_DETACHED" = "$MASTER_TIP" ]; then
    echo "SETUP-FAIL: detached commit equals master tip" >&2
    exit 2
fi

MANIFEST="$SCRATCH/pin-manifest.json"
ZERO40=0000000000000000000000000000000000000000
cat > "$MANIFEST" <<EOF
{
  "schema": "pin-manifest-v1",
  "source": "head-vs-branch.sh fixture (round-17 jj hazard)",
  "note": "Only the bash-surface-census leg is exercised; the other five recorded legs are present because the tool rejects manifests that omit a leg.",
  "legs": [
    {"leg": "js-kimi-census", "repo": "kumitate-shokunin", "path": "scripts/kimi-census.mjs", "pinned_commit": "$ZERO40", "expected_sha256": "$V1_SHA"},
    {"leg": "bash-surface-census", "repo": "kagi-shokunin", "path": "corpus/surface-census.sh", "pinned_commit": "$MASTER_TIP", "expected_sha256": "$V1_SHA"},
    {"leg": "bash-tsukuroi-census", "repo": "tsukuroi-shokunin", "path": "tools/tsukuroi-census.sh", "pinned_commit": "$ZERO40", "expected_sha256": "$V1_SHA"},
    {"leg": "bash-mado-verify", "repo": "mado-shokunin", "path": "tools/mado-verify.sh", "pinned_commit": "$ZERO40", "expected_sha256": "$V1_SHA"},
    {"leg": "bash-checklist-run", "repo": "kagi-shokunin", "path": "corpus/checklist-run.sh", "pinned_commit": "$ZERO40", "expected_sha256": "$V1_SHA"},
    {"leg": "js-claims-check", "repo": "kumitate-shokunin", "path": "scripts/claims-check.mjs", "pinned_commit": "$ZERO40", "expected_sha256": "$V1_SHA"}
  ]
}
EOF

OUT="$SCRATCH/tool-output.json"
python3 "$TOOL" --manifest "$MANIFEST" --root "$FLEET" > "$OUT" 2> "$SCRATCH/tool-stderr.txt"
TOOL_EXIT=$?

echo "FIXTURE scratch=$SCRATCH (removed on exit)"
echo "FIXTURE repo=$REPO branch=master master_tip=$MASTER_TIP"
echo "FIXTURE head_detached=$HEAD_DETACHED (master..HEAD = 1, symbolic-ref HEAD = detached)"
echo "FIXTURE v1_sha256=$V1_SHA pinned at master tip"
echo "FIXTURE v2_sha256=$V2_SHA present only in detached HEAD commit + worktree"
echo "TOOL argv: python3 $TOOL --manifest $MANIFEST --root $FLEET"
echo "TOOL exit=$TOOL_EXIT"
if [ -s "$SCRATCH/tool-stderr.txt" ]; then
    echo "TOOL stderr:"; sed 's/^/  /' "$SCRATCH/tool-stderr.txt"
fi
if [ "$TOOL_EXIT" -ne 0 ]; then
    echo "SETUP-FAIL: tool exited $TOOL_EXIT (expected 0 observation document)" >&2
    exit 2
fi

# Extract the exercised leg's head/pinned/worktree fields (head.branch exists
# on landed tools, null on the 98bea7d tool).
read -r HEAD_COMMIT HEAD_BLOB HEAD_STATUS HEAD_BRANCH PINNED_COMMIT WORKTREE_SHA <<EOF
$(python3 - "$OUT" "$LEG" <<'PY'
import json, sys
try:
    payload = json.load(open(sys.argv[1], "rb"))
    row = next(r for r in payload.get("legs", []) if r.get("leg") == sys.argv[2])
    head = row.get("head") or {}
    pinned = row.get("pinned") or {}
    worktree = row.get("worktree") or {}
    print(head.get("commit") or "null",
          head.get("blob_sha256") or "null",
          head.get("status") or "null",
          head.get("branch") or "null",
          pinned.get("commit") or "null",
          worktree.get("sha256") or "null")
except Exception:
    print("null null null null null null")
PY
)
EOF

echo "OBSERVED leg=$LEG"
echo "OBSERVED head.commit=$HEAD_COMMIT head.branch=$HEAD_BRANCH head.status=$HEAD_STATUS head.blob_sha256=$HEAD_BLOB"
echo "OBSERVED pinned.commit=$PINNED_COMMIT worktree.sha256=$WORKTREE_SHA"

# "Used master's tip" = reported commit AND blob are the branch tip's pair.
# "Used HEAD" = reported commit is the detached snapshot commit or the
# reported blob carries v2-only bytes (covers a mixed tool that names the
# branch tip but hashes HEAD's blob).
if [ "$HEAD_COMMIT" = "$MASTER_TIP" ] && [ "$HEAD_BLOB" = "$V1_SHA" ]; then
    echo "VERDICT: head observation used master's tip ($MASTER_TIP, v1 bytes) — branch-safe"
    exit 0
fi
if [ "$HEAD_COMMIT" = "$HEAD_DETACHED" ] || [ "$HEAD_BLOB" = "$V2_SHA" ]; then
    echo "VERDICT: head observation used detached HEAD state (commit=$HEAD_COMMIT blob=$HEAD_BLOB, v2 bytes) — jj @- snapshot reported as repo head (JjAuditTameshi.md §2.3)"
    exit 1
fi
echo "SETUP-FAIL: head commit/blob pair ($HEAD_COMMIT / $HEAD_BLOB) matches neither fixture pair" >&2
exit 2
