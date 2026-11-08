#!/usr/bin/env bash
# T91SN1 — safety / trust-boundary probe for the round-91 committed drivers.
#
# READ-ONLY on the lane and on the fleet: this script never writes inside
# /home/vgpnk/Projects/shokunin or .../tameshi-shokunin. Every clone, fixture,
# work dir and scratch file lives under $S (absolute).
#
# Usage: bash T91SN1-probe.sh <lane> <scratch-abs-dir>
# The transcript is the evidence; the exit code only says "the probe ran".
set -u
LANE=$(realpath -- "${1:?lane}"); S=$(realpath -m -- "${2:?scratch}")
C1="$LANE/.ufo/evidence/round-91/c1"
C2="$LANE/.ufo/evidence/round-91/c2"
mkdir -p "$S"
export GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@fixture.invalid
export GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@fixture.invalid
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES 2>/dev/null || true

hdr() { printf '\n===== %s =====\n' "$*"; }

hdr "P1  C2 'toolpin' is a self-comparison: sha(file) vs sha(same file). Never fails."
: > "$S/p1.empty"
e=$(sha256sum "$S/p1.empty" | cut -d' ' -f1); p=$(sha256sum "$S/p1.empty" | cut -d' ' -f1)
echo "expect=$e"
echo "pinned=$p"
if [ -n "$e" ] && [ "$e" = "$p" ]; then echo "RESULT: toolpin would be OK even for a MISSING/EMPTY blob"; fi

hdr "P2  the 'pinned' blob is an ABBREVIATED rev (ff7a4b06) resolved against the clone's refs"
rm -rf "$S/p2"; git clone -q --shared --no-checkout "$LANE" "$S/p2"
git -C "$S/p2" checkout -q --detach 048c3f3000a79ee35b53678af19411d3f9fa1816
mkdir -p "$S/p2/tools"
printf 'import sys\nprint("LEDGER_WITNESS_SELFTEST: 21/21 pass")\nsys.exit(0)\n' > "$S/p2/tools/ledger-witness.py"
git -C "$S/p2" add -A; git -C "$S/p2" commit -q -m "attacker blob"
git -C "$S/p2" tag ff7a4b06 HEAD
echo "true pinned blob sha (lane @ff7a4b06): $(git -C "$LANE" show ff7a4b06:tools/ledger-witness.py | sha256sum | cut -d' ' -f1)"
echo "shadowing tag resolves to        : $(git -C "$S/p2" show 'ff7a4b06:tools/ledger-witness.py' 2>&1 | head -1)"

hdr "P2b END-TO-END: a candidate tag named ff7a4b06 substitutes the 'pinned' witness blob"
rm -rf "$S/p2b"; git clone -q --shared --no-checkout "$LANE" "$S/p2b"
git -C "$S/p2b" checkout -q --detach 048c3f3000a79ee35b53678af19411d3f9fa1816
mkdir -p "$S/p2b/tools"
printf 'import sys\nprint("LEDGER_WITNESS_SELFTEST: 21/21 pass")\nsys.exit(0)\n' > "$S/p2b/tools/ledger-witness.py"
git -C "$S/p2b" add -A; git -C "$S/p2b" commit -q -m "attacker witness blob"
git -C "$S/p2b" tag ff7a4b06 HEAD
P2BREV=$(git -C "$S/p2b" rev-parse HEAD); rm -rf "$S/p2bwork"; mkdir -p "$S/p2bwork"
bash "$C2/measure-c2-v91.sh" "$S/p2b" "$P2BREV" "$S/p2bwork" 048c3f3000a79ee35b53678af19411d3f9fa1816 > "$S/p2b.out" 2>&1
echo "counter exit=$?"
grep -E 'toolpin=|C2_SUMMARY|C2_R91_PASS' "$S/p2b.out"
echo "TRUE pinned blob sha (lane @ff7a4b06): $(git -C "$LANE" show ff7a4b06:tools/ledger-witness.py | sha256sum | cut -d' ' -f1)"

hdr "P3  C2 counter runs the CANDIDATE's tools/defect-bind.py; a stub tool => PASS with docs UNREPAIRED"
rm -rf "$S/p3"; git clone -q --shared --no-checkout "$LANE" "$S/p3"
git -C "$S/p3" checkout -q --detach 048c3f3000a79ee35b53678af19411d3f9fa1816
cat > "$S/p3/tools/defect-bind.py" <<'EOF'
import sys
print("DEFECT_BIND_ROW R90-1-not-admitted-marker kind=doc-contains expect=closed state=closed detail=section-carries")
print("DEFECT_BIND_ROW R90-2-entry-cites-coverage-row kind=doc-contains expect=closed state=closed detail=section-carries")
print("DEFECT_BIND_ROW R90-2-lesson-receipt-addendum kind=doc-contains expect=closed state=closed detail=section-carries")
print("DEFECT_BIND: rows=3 closed=3 open=0 unexpected=0 manifest=bound")
sys.exit(0)
EOF
git -C "$S/p3" commit -q -am "doctored measuring tool"
P3REV=$(git -C "$S/p3" rev-parse HEAD); rm -rf "$S/p3work"; mkdir -p "$S/p3work"
echo "committed note   'not admitted' count: $(git -C "$S/p3" show HEAD:corpus/knowledge/mutation-case-fleet-sources-census.md | grep -c 'not admitted')"
echo "committed lesson 'receipt addendum'  : $(git -C "$S/p3" show HEAD:corpus/lessons/round-90.md | grep -c 'Round-91 receipt addendum')"
# NOTE: the counter requires an EMPTY work dir, so the transcript must NOT be
# written inside it (a redirect into $S/p3work would make it non-empty).
bash "$C2/measure-c2-v91.sh" "$S/p3" "$P3REV" "$S/p3work" 048c3f3000a79ee35b53678af19411d3f9fa1816 > "$S/p3.out" 2>&1
echo "counter exit=$?"
grep -E 'C2_SUMMARY|C2_R91_PASS|toolpin=' "$S/p3.out"

hdr "P4  C1 counter --repo '' -> os.path.realpath('') == cwd (the fleet root under the seat host guard)"
python3 -c "import os;print('realpath(\'\') =', os.path.realpath(''))"
echo "git -C '' rev-parse --show-toplevel: $(git -C '' rev-parse --show-toplevel 2>&1 | head -1)"

hdr "P5  ambient GIT_DIR defeats the C2 toplevel guard: git acts on the injected repo, guard still passes"
rm -rf "$S/p5"; git init -q "$S/p5"; git -C "$S/p5" commit -q --allow-empty -m p5
mkdir -p "$S/p5/clone"
echo "plain   : git -C p5/clone rev-parse --show-toplevel -> $(git -C "$S/p5/clone" rev-parse --show-toplevel 2>&1)"
echo "GIT_DIR : git -C p5/clone rev-parse --show-toplevel -> $(GIT_DIR="$S/p5/.git" git -C "$S/p5/clone" rev-parse --show-toplevel 2>&1)"
GIT_DIR="$S/p5/.git" git -C "$S/p5/clone" checkout -q --detach HEAD >/dev/null 2>&1
echo "GIT_DIR : 'git -C p5/clone checkout' rc=$? (operates on the injected GIT_DIR, not the clone)"

hdr "P6  ambient GIT_INDEX_FILE redirects 'git add -A' writes OUTSIDE the scratch clone"
rm -rf "$S/p6"; git clone -q --shared --no-checkout "$LANE" "$S/p6"; git -C "$S/p6" checkout -q --detach HEAD
printf 'x\n' > "$S/p6/new.txt"
GIT_INDEX_FILE="$S/p6.ambient.idx" git -C "$S/p6" add -A
echo "ambient index written outside the clone: $(ls -l "$S/p6.ambient.idx" 2>&1 | head -1)"

hdr "P7  controls-v91.py --lane '' creates .ufo/... under the CWD before validating the lane"
rm -rf "$S/p7"; mkdir -p "$S/p7"
cp "$C1/controls-v91.py" "$S/p7/controls.py"
python3 - "$S/p7/controls.py" "$S/p7/OUT" <<'PYEOF'
import sys
p, out = sys.argv[1], sys.argv[2]
s = open(p).read()
s = s.replace('outdir = os.path.join(lane, ".ufo/evidence/round-91/pre-freeze/controls")',
              'outdir = %r' % out)
open(p, "w").write(s)
PYEOF
( cd "$S/p7" && python3 -I "$S/p7/controls.py" --lane "" --scratch "$S/p7/sc" --only NOSUCH >/dev/null 2>&1 )
echo "tree created under the CWD (cwd == \$S/p7):"; find "$S/p7" -maxdepth 5 -type d | sed "s|^$S/p7|.|" | head

hdr "P8  fixes-v91.py --target on a sibling-shaped tree FORGES corpus files (open(...,'a') creates)"
rm -rf "$S/p8"; mkdir -p "$S/p8/corpus/knowledge" "$S/p8/corpus/lessons"
printf '# unrelated sibling note\n' > "$S/p8/corpus/knowledge/other-note.md"
python3 -I "$C2/fixes-v91.py" --target "$S/p8" --variant pos >/dev/null 2>&1
echo "files now present in the sibling-shaped tree:"; find "$S/p8" -type f | sed "s|^$S/p8|.|"
echo "--- head of the forged note:"; head -3 "$S/p8/corpus/knowledge/mutation-case-fleet-sources-census.md" 2>/dev/null
echo "--- against a fleet-root-shaped target (no corpus/):"
rm -rf "$S/p8b"; mkdir -p "$S/p8b"
python3 -I "$C2/fixes-v91.py" --target "$S/p8b" --variant pos >/dev/null 2>&1; echo "   exit=$?  files created: $(find "$S/p8b" -type f | wc -l)"

hdr "P9  C1 counter blob(): empty --rev turns 'rev:path' into ':path' = the INDEX, not a commit"
rm -rf "$S/p9"; git clone -q --shared --no-checkout "$LANE" "$S/p9"
git -C "$S/p9" checkout -q --detach 048c3f3000a79ee35b53678af19411d3f9fa1816
N=corpus/knowledge/mutation-case-fleet-sources-census.md
printf '\nSTAGED-ONLY-MARKER not admitted\n' >> "$S/p9/$N"; git -C "$S/p9" add "$N"
echo "HEAD blob  'not admitted' count: $(git -C "$S/p9" cat-file blob "HEAD:$N" | grep -c 'not admitted')"
echo "index blob ':path'       count: $(git -C "$S/p9" cat-file blob ":$N" | grep -c 'not admitted')"

hdr "P10 worktree bytes != committed blob under core.autocrlf=true (C2 reads the WORKTREE)"
rm -rf "$S/p10"; git init -q "$S/p10"
( cd "$S/p10" && printf 'line1\nline2\n' > f.txt && git add f.txt && git commit -q -m base \
  && rm -f f.txt && git -c core.autocrlf=true checkout -q HEAD -- f.txt \
  && echo "committed blob sha: $(git cat-file blob HEAD:f.txt | sha256sum | cut -d' ' -f1)" \
  && echo "worktree file sha : $(sha256sum f.txt | cut -d' ' -f1)" )

hdr "P11 C1 sealed env: are global credential/user/safe config entries visible to git?"
python3 - <<'PYEOF'
import subprocess
env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
       "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
p = subprocess.run(["git","config","--list","--show-origin"], env=env,
                   capture_output=True, text=True, cwd="/home/vgpnk/Projects/shokunin/tameshi-shokunin")
print("rc", p.returncode)
print("origins seen:", sorted({l.split("\t")[0] for l in p.stdout.splitlines() if "\t" in l}))
print("global credential helper visible:", "credential" in p.stdout)
PYEOF

hdr "PROBE COMPLETE — no file inside the lane or the fleet was written by this script"
