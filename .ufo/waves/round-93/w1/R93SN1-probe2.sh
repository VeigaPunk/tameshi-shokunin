#!/usr/bin/env bash
# R93SN1 safety probe 2: write-containment, empty/unchecked variables, ambient GIT_*
# leakage, shared-clone object leakage, and the disposition checker's mechanism test.
# Read-only w.r.t. the lane and the fleet repo; all writes land under $S.
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe2.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
CTRL="$LANE/.ufo/evidence/round-93/c1/controls-v93.py"
BASE=4a7e259b407d582d2010197f32d7524d6bed5370
REV=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
sec() { printf '\n===== %s =====\n' "$1"; }
probe() { printf 'PROBE %-38s %s\n' "$1" "${2:-}"; }

sec "E7 empty --outdir writes into the process cwd"
mkdir -p "$S/cwd7" && cd "$S/cwd7" || exit 1
mkdir -p "$S/work7"
python3 -I "$CTRL" --lane "$LANE" --rev "$REV" --base "$BASE" \
  --work "$S/work7" --outdir "" --only nowork-base --jobs 1 >"$S/e7.log" 2>&1
probe "E7.rc" "$?"
probe "E7.cwd-listing" "$(ls "$S/cwd7" | tr '\n' ' ')"
probe "E7.receipt-in-cwd" "$( [ -f "$S/cwd7/nowork-base.out" ] && echo YES || echo no )"
probe "E7.summary-in-cwd" "$( [ -f "$S/cwd7/C1-summary.txt" ] && echo YES || echo no )"
probe "E7.tail" "$(tail -3 "$S/e7.log" | tr '\n' '|')"

sec "E8 empty --work in an EMPTY cwd (counter materialization target)"
mkdir -p "$S/cwd8" "$S/work8"
( cd "$S/cwd8" && python3 -I "$LANE/.ufo/evidence/round-93/c1/measure-v93.py" \
    --repo "$LANE" --rev "$BASE" --work "" >"$S/e8.log" 2>&1 )
probe "E8.rc-and-out" "$(head -2 "$S/e8.log" | tr '\n' '|')"
probe "E8.cwd8-listing" "$(ls -A "$S/cwd8" | tr '\n' ' ')"

sec "E9 shared clone: does hash-object -w / git replace leak into the lane?"
git -C "$LANE" replace -l >"$S/e9.lane-replace-before" 2>&1
probe "E9.lane-replace-refs-before" "$(tr '\n' ' ' < "$S/e9.lane-replace-before")"
git clone -q --shared --no-checkout "$LANE" "$S/e9clone" 2>/dev/null
git -C "$S/e9clone" checkout -q --detach "$REV" 2>/dev/null
NEW=$(printf 'r93 probe object\n' | git -C "$S/e9clone" hash-object -w --stdin)
probe "E9.new-oid" "$NEW"
git -C "$S/e9clone" cat-file -e "$NEW" 2>/dev/null && probe "E9.clone-has-object" "yes" || probe "E9.clone-has-object" "no"
git -C "$LANE" cat-file -e "$NEW" 2>/dev/null && probe "E9.LANE-HAS-OBJECT" "LEAK" || probe "E9.LANE-HAS-OBJECT" "no-leak"
FA=$(git -C "$S/e9clone" rev-parse "$REV:corpus/README.md")
git -C "$S/e9clone" replace "$FA" "$NEW" >/dev/null 2>&1
probe "E9.clone-replace-l" "$(git -C "$S/e9clone" replace -l | tr '\n' ' ')"
probe "E9.LANE-replace-l-after" "$(git -C "$LANE" replace -l | tr '\n' ' ')"
probe "E9.lane-status-after" "$(git -C "$LANE" status --porcelain | wc -l) untracked/modified lines"
probe "E9.lane-refs-replace-dir" "$( [ -d "$LANE/.git/refs/replace" ] && ls "$LANE/.git/refs/replace" | tr '\n' ' ' || echo none )"

sec "E3b ambient GIT_DIR hijack of 'git -C <dir>' (precise)"
git init -q "$S/amb" && git -C "$S/amb" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
git clone -q --shared "$S/amb" "$S/tgt" 2>/dev/null
probe "E3b.plain.toplevel" "$(git -C "$S/tgt" rev-parse --show-toplevel 2>&1)"
probe "E3b.GIT_DIR.toplevel" "$(GIT_DIR="$S/amb/.git" git -C "$S/tgt" rev-parse --show-toplevel 2>&1)"
probe "E3b.GIT_DIR.commit-lands-in" "$(GIT_DIR="$S/amb/.git" git -C "$S/tgt" commit -q --allow-empty -m hijack 2>&1; git -C "$S/amb" log --oneline -1 2>&1)"
probe "E3b.GIT_INDEX_FILE.add" "$(GIT_INDEX_FILE="$S/amb.idx" git -C "$S/tgt" add -A 2>&1; ls "$S" | grep -c 'amb.idx')"
probe "E3b.GIT_WORK_TREE.toplevel" "$(GIT_WORK_TREE="$S/amb" git -C "$S/tgt" rev-parse --show-toplevel 2>&1)"

sec "E11 disposition checker: mechanism-word match on a contentless reason"
python3 - "$LANE" <<'PY'
import importlib.util, json, os, sys, tempfile
lane = sys.argv[1]
spec = importlib.util.spec_from_file_location("cd", os.path.join(lane, "tools/conjunct-disposition.py"))
cd = importlib.util.module_from_spec(spec); spec.loader.exec_module(cd)
with tempfile.TemporaryDirectory() as d:
    open(os.path.join(d, "st.out"), "w").write("exit=1\nC1_CONJUNCTS alpha=false\n")
    keys = ["alpha"]
    bad = {"alpha": {"unfalsifiable": "the shipping manifest pins nothing at all in this shipping lane"}}
    print("PROBE E11.contentless-40char-reason findings=%d detail=%s"
          % (len(cd.check(keys, bad, d)), cd.check(keys, bad, d)))
    bad2 = {"alpha": {"unfalsifiable": "x" * 39 + " pin"}}
    print("PROBE E11.short-reason findings=%d" % len(cd.check(keys, bad2, d)))
PY

sec "E12 hardcoded /tmp or credential reads in the four drivers"
for f in "$LANE/.ufo/evidence/round-93/c1/controls-v93.py" \
         "$LANE/.ufo/evidence/round-93/c1/measure-v93.py" \
         "$LANE/tools/conjunct-disposition.py" \
         "$LANE/.ufo/evidence/round-93/c1/make-pins.py"; do
  n=$(grep -c -E '/tmp/|/etc/passwd|\.ssh|GITHUB_TOKEN|os\.environ\[.HOME|getpass' "$f" 2>/dev/null || echo 0)
  probe "E12.hardcoded-paths.$(basename "$f")" "matches=$n"
done

printf '\n===== done =====\n'
