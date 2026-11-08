#!/usr/bin/env bash
# R93SN1 safety probe for the round-93 C1 drivers.
# Read-only w.r.t. every repo except fixtures created under $S (scratch).
# Emits "PROBE <name> <result>" lines and a summary; nothing outside $S is written.
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
cd "$S" || exit 1

sec() { printf '\n===== %s =====\n' "$1"; }
probe() { printf 'PROBE %-34s %s\n' "$1" "${2:-}"; }

# --------------------------------------------------------------- E1 git -C ""
sec "E1 git -C '' behaviour (fleet incident 2026-11-06)"
git init -q "$S/e1" 2>/dev/null
mkdir -p "$S/cwdrepo" && git -C "$S/cwdrepo" init -q
( cd "$S/cwdrepo" && git -c user.name=t -c user.email=t@t commit -q --allow-empty -m base )
out=$(cd "$S/cwdrepo" && git -C "" rev-parse --show-toplevel 2>&1); rc=$?
probe "E1.git-C-empty.toplevel" "rc=$rc out=$out"
out=$(cd "$S/cwdrepo" && git -C "" status --porcelain 2>&1); rc=$?
probe "E1.git-C-empty.status" "rc=$rc out=$out"
out=$(cd "$S/cwdrepo" && git -C "" commit --allow-empty -m x 2>&1); rc=$?
probe "E1.git-C-empty.commit" "rc=$rc out=$out"

# ------------------------------------------- E2 GIT_NO_REPLACE_OBJECTS + replace -l
sec "E2 does GIT_NO_REPLACE_OBJECTS=1 hide 'git replace -l'?"
git init -q "$S/e2" && cd "$S/e2" || exit 1
git -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
B=$(git rev-parse HEAD)
echo hello > f.txt && git add f.txt && git -c user.name=t -c user.email=t@t commit -q -m f
FA=$(git rev-parse HEAD:f.txt)
FA2=$(git hash-object -w --stdin <<< "faked")
git replace "$FA" "$FA2"
probe "E2.replace-l-plain" "$(git replace -l | tr '\n' ' ')"
probe "E2.replace-l-no-replace-env" "$(GIT_NO_REPLACE_OBJECTS=1 git replace -l | tr '\n' ' ')"
probe "E2.replace-l-scrubbed" "$(GIT_NO_REPLACE_OBJECTS=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git replace -l | tr '\n' ' ')"

# ------------------------------------------- E3 ambient GIT_* vs -C / toplevel guard
sec "E3 ambient GIT_DIR / GIT_INDEX_FILE / GIT_OBJECT_DIRECTORY vs 'git -C dir'"
git init -q "$S/e3clone" && cd "$S/e3clone" || exit 1
git -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
git clone -q --shared --no-checkout "$S/e3clone" "$S/e3dst" 2>/dev/null
git -C "$S/e3dst" checkout -q --detach HEAD 2>/dev/null
probe "E3.clean.toplevel" "$(git -C "$S/e3dst" rev-parse --show-toplevel 2>&1)"
probe "E3.GIT_DIR.toplevel" "$(GIT_DIR="$S/e3clone/.git" git -C "$S/e3dst" rev-parse --show-toplevel 2>&1)"
probe "E3.GIT_DIR.status" "$(GIT_DIR="$S/e3clone/.git" git -C "$S/e3dst" status --porcelain 2>&1 | head -3)"
probe "E3.GIT_INDEX_FILE.add-target" "$(GIT_INDEX_FILE="$S/amb.idx" git -C "$S/e3dst" add -A 2>&1; ls "$S" | tr '\n' ' ')"
probe "E3.GIT_OBJECT_DIRECTORY.clone" "$(GIT_OBJECT_DIRECTORY="$S/ambobj" git clone -q --shared --no-checkout "$S/e3clone" "$S/e3dst2" 2>&1 | head -2)"

# ------------------------------------------- E4 git path syntax constraints
sec "E4 git rev:path syntax: traversal / absolute path"
git init -q "$S/e4" && cd "$S/e4" || exit 1
mkdir -p scripts && echo "echo ok" > scripts/gate.sh && git add -A
git -c user.name=t -c user.email=t@t commit -q -m base
H=$(git rev-parse HEAD)
probe "E4.normal" "$(git cat-file blob $H:scripts/gate.sh 2>&1 | head -1)"
probe "E4.traversal-dotdot" "$(git cat-file blob "$H:scripts/../../x" 2>&1 | head -1)"
probe "E4.absolute-path" "$(git cat-file blob "$H:/etc/passwd" 2>&1 | head -1)"
probe "E4.leading-slash-scripts" "$(git cat-file blob "$H:/scripts/gate.sh" 2>&1 | head -1)"

# ------------------------------------------- E5 M4 receipt guard vs symlink
sec "E5 M4 receipt_path() vs a pre-existing symlink"
cat > "$S/rp.py" <<'PY'
import os, sys
def receipt_path(outdir, name):
    p = os.path.join(outdir, name + ".out")
    if not os.path.exists(p):
        return p
    n = 1
    while os.path.exists(os.path.join(outdir, "%s.rerun-%d.out" % (name, n))):
        n += 1
    return os.path.join(outdir, "%s.rerun-%d.out" % (name, n))
outdir = sys.argv[1]
target = sys.argv[2]
os.makedirs(outdir, exist_ok=True)
link = os.path.join(outdir, "pos-real.out")
if not os.path.exists(link):
    os.symlink(target, link)
p = receipt_path(outdir, "pos-real")
print("chosen=" + p)
print("chosen_is_symlink=" + str(os.path.islink(p)))
with open(p, "w", encoding="utf-8") as f:
    f.write("exit=0\n")
PY
python3 "$S/rp.py" "$S/outdir5" "$S/ESCAPED-PAYLOAD.txt"
probe "E5.payload-written-outside-outdir" "$( [ -f "$S/ESCAPED-PAYLOAD.txt" ] && echo YES || echo no )"
probe "E5.payload-content" "$(head -c 40 "$S/ESCAPED-PAYLOAD.txt" 2>/dev/null | tr '\n' ' ')"
probe "E5.exists-on-dangling-symlink" "$(python3 -c 'import os,sys;print(os.path.exists(sys.argv[1]))' "$S/outdir5/pos-real.out")"

# ------------------------------------------- E6 tarfile data filter vs hostile tar
sec "E6 tarfile extractall(filter='data') vs traversal / absolute members"
python3 - "$S" <<'PY'
import io, os, sys, tarfile
S = sys.argv[1]
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w") as t:
    for nm, data in (("../escape-rel.txt", b"rel"), ("/abs-escape.txt", b"abs")):
        ti = tarfile.TarInfo(nm); ti.size = len(data)
        t.addfile(ti, io.BytesIO(data))
buf.seek(0)
try:
    with tarfile.open(fileobj=buf) as t:
        t.extractall(os.path.join(S, "e6"), filter="data")
    print("PROBE E6.extractall-data           NO ERROR")
except Exception as e:
    print("PROBE E6.extractall-data           refused: %s: %s" % (type(e).__name__, e))
print("PROBE E6.rel-escape-exists          %s" % os.path.exists(os.path.join(S, "escape-rel.txt")))
print("PROBE E6.abs-escape-exists          %s" % os.path.exists("/abs-escape.txt"))
PY

printf '\n===== done =====\n'
