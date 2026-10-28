#!/bin/bash
# T54W1Simplify01 — reproduction for the round-54 "four copies of ScratchRootUnusable" item.
# Read-only against the lane: every mutation happens in a --shared clone under HYAKU_SCRATCH.
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C0=59c38109bf119d0e9d4f878644a82babc937bc1e
BASE=d33053f7552d
export HYAKU_SCRATCH=${HYAKU_SCRATCH:-/fast/scratch/hyaku}
S=$HYAKU_SCRATCH/tameshi-r54/T54W1Simplify01/repro
rm -rf -- "$S"; mkdir -p "$S"
trap 'echo "[scratch kept at $S]"' EXIT

clone_at() {  # $1 = dest, $2 = rev
    git clone --shared -q "$LANE" "$1" || exit 1
    git -C "$1" rev-parse --show-toplevel
    git -C "$1" checkout -q "$2" || exit 1
}

ARMS=(
  "env-diff.py --selftest"
  "evidence-disposition.py --selftest"
  "pin-disposition.py --selftest"
  "bash-witness-study.py selftest"
  "context-capture.py --selftest"
  "registry-check.py --selftest"
  "repeat-control.py --selftest"
)

sweep() {  # $1 = tree label, $2 = tree path, $3 = TMPDIR value
    local label=$1 tree=$2 tmpdir=$3 a tool arg out rc
    echo "### $label  TMPDIR=$tmpdir"
    for a in "${ARMS[@]}"; do
        tool=${a%% *}; arg=${a#* }
        out=$(cd "$tree" && TMPDIR="$tmpdir" PYTHONDONTWRITEBYTECODE=1 python3 "tools/$tool" "$arg" 2>&1)
        rc=$?
        printf '%-30s rc=%d lines=%d traceback=%d could-not-evaluate=%d\n' \
            "$tool" "$rc" "$(printf '%s\n' "$out" | wc -l)" \
            "$(printf '%s' "$out" | grep -c 'Traceback (most recent call last)')" \
            "$(printf '%s' "$out" | grep -c 'could-not-evaluate')"
        printf '%s\n' "$out" | tail -1 | cut -c1-160 | sed 's/^/    | /'
    done
    echo
}

echo "===== 1. base d33053f vs C0 59c3810, one set-but-unusable TMPDIR ====="
clone_at "$S/base" "$BASE" >/dev/null
clone_at "$S/c0" "$C0" >/dev/null
sweep "base d33053f (no class)" "$S/base" "/nonexistent/nope-r54"
sweep "C0 59c3810 (class + arm)" "$S/c0" "/nonexistent/nope-r54"

echo "===== 2. duplication measurement (7 copies of strict_scratch_root) ====="
(cd "$LANE" && python3 - "$C0" <<'PY'
import ast, hashlib, difflib
files = ["context-capture", "registry-check", "repeat-control",
         "env-diff", "evidence-disposition", "pin-disposition", "bash-witness-study"]
bodies, raisers, arms = {}, {}, {}
for n in files:
    src = open("tools/%s.py" % n).read()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "strict_scratch_root":
            seg = ast.get_source_segment(src, node)
            bodies[n] = seg
            r = [x for x in ast.walk(node) if isinstance(x, ast.Raise)]
            raisers[n] = r[0].exc.func.id if r and isinstance(r[0].exc, ast.Call) else "?"
    tops = [x for x in tree.body if isinstance(x, ast.ClassDef) and x.name == "ScratchRootUnusable"]
    arms[n] = "class" if tops else "-"
for n in files:
    b = bodies[n]
    print("%-22s helper_lines=%2d sha=%s raises=%-18s class=%s" %
          (n, b.count("\n") + 1, hashlib.sha256(b.encode()).hexdigest()[:16], raisers[n], arms[n]))
groups = {}
for n, b in bodies.items():
    groups.setdefault(b, []).append(n)
print("\ndistinct strict_scratch_root bodies: %d" % len(groups))
for b, ns in groups.items():
    print("   %s" % ns)
ks = list(groups)
if len(ks) == 2:
    print("\ndiff between the two variants:")
    for line in difflib.unified_diff(ks[0].splitlines(), ks[1].splitlines(),
                                     "A:%s" % groups[ks[0]], "B:%s" % groups[ks[1]],
                                     lineterm="", n=0):
        print("   " + line)
print("\nhelper lines duplicated: %d copies = %d lines; class = 2 lines x 4 ; arm = 3 lines x 4" %
      (len(files), sum(b.count("\n") + 1 for b in bodies.values())))
PY
)

echo
echo "===== 3. import-graph: does any tool import a sibling module? ====="
(cd "$LANE" && python3 - <<'PY'
import ast, glob, os
names = {os.path.basename(p)[:-3] for p in glob.glob("tools/*.py")}
hits = []
for p in glob.glob("tools/*.py"):
    t = ast.parse(open(p).read())
    for node in ast.walk(t):
        if isinstance(node, ast.Import):
            hits += [(p, a.name) for a in node.names if a.name.split(".")[0] in names or a.name.startswith("tools")]
        elif isinstance(node, ast.ImportFrom) and (node.level or (node.module and node.module.split(".")[0] in names)):
            hits.append((p, node.module, node.level))
print("tool files:", len(glob.glob("tools/*.py")), "local/relative imports:", hits)
PY
)
echo "staged subset copies of tools/ (historical practice):"
(cd "$LANE" && for d in .ufo/waves/round-17/staged/tools .ufo/waves/round-18/staged/tools; do
    printf '   %-34s %s files (live tools/ has %s entries)\n' "$d" "$(ls $d | wc -l)" "$(ls tools | wc -l)"
 done)

echo
echo "===== 4. what a tools/scratch_root.py module would cost ====="
mkdir -p "$S/fix1/tools"
printf 'class ScratchRootUnusable(RuntimeError):\n    pass\n' > "$S/fix1/tools/scratch_root.py"
printf 'import sys\nfrom scratch_root import ScratchRootUnusable\nprint("imported ok")\n' > "$S/fix1/tools/consumer.py"
mkdir -p "$S/fix1/subset" "$S/fix2/reva" "$S/fix2/revb"
cp "$S/fix1/tools/consumer.py" "$S/fix1/subset/consumer.py"
echo "4a. subset copy (one tool file staged alone, as round-17 staged 3 of 33):"
(cd "$S/fix1/subset" && PYTHONDONTWRITEBYTECODE=1 python3 consumer.py; echo "    rc=$?") 2>&1 | tail -3
echo "4b. by-path load (registry-replay's spec_from_file_location on tools/registry-check.py):"
PYTHONDONTWRITEBYTECODE=1 python3 -c "
import importlib.util, sys
spec = importlib.util.spec_from_file_location('m', '$S/fix1/subset/consumer.py')
m = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(m); print('    loaded ok')
except Exception as exc:
    print('    %s: %s' % (type(exc).__name__, exc)); sys.exit(3)
"; echo "    rc=$?"
printf 'VERSION="revA-helper"\n' > "$S/fix2/reva/helper.py"
printf 'VERSION="revB-helper"\n' > "$S/fix2/revb/helper.py"
printf 'from helper import VERSION\nprint("    runner saw helper:", VERSION)\n' > "$S/fix2/reva/runner.py"
echo "4c. cross-revision: exec_module on revision A's runner with sys.path[0] at revision B's tools dir:"
PYTHONDONTWRITEBYTECODE=1 python3 -c "
import importlib.util, sys
sys.path[0] = '$S/fix2/revb'
spec = importlib.util.spec_from_file_location('runner', '$S/fix2/reva/runner.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
"
echo "4d. instrument hashes cover __file__ only (a sibling module would not be hashed):"
(cd "$LANE" && grep -n "instrument_sha256\|tool_sha256()\|Path(__file__).read_bytes()\|\"sha256\": sha256_file" \
    tools/env-diff.py tools/evidence-disposition.py tools/pin-disposition.py tools/bash-witness-study.py | sed 's/^/   /')

echo
echo "===== 5. laundering test: typed arm vs bare-RuntimeError arm ====="
echo "5a. C0 code + a RuntimeError raised inside evidence-disposition's selftest (injected in the clone):"
cp -a "$S/c0/tools/evidence-disposition.py" "$S/evd.py"
python3 - "$S/evd.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = '    """Isolated /tmp fixtures; invokes this CLI via subprocess only."""\n'
new = old + '    raise RuntimeError("injected interior bug: jj status failed")\n'
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
PY
mkdir -p "$S/tmpok"
cp -a "$S/c0/tools" "$S/c0evd" 2>/dev/null
mkdir -p "$S/evdA/tools" && cp -a "$S/c0/tools/." "$S/evdA/tools/" && cp "$S/evd.py" "$S/evdA/tools/evidence-disposition.py"
(cd "$S/evdA" && out=$(TMPDIR="$S/tmpok" PYTHONDONTWRITEBYTECODE=1 python3 tools/evidence-disposition.py --selftest 2>&1); echo "    rc=$? traceback=$(printf '%s' "$out" | grep -c 'Traceback (most recent call last)')"; printf '%s\n' "$out" | tail -1 | sed 's/^/    | /')
echo "5b. same file with the arm widened to 'except RuntimeError':"
mkdir -p "$S/evdB/tools" && cp -a "$S/c0/tools/." "$S/evdB/tools/" && cp "$S/evd.py" "$S/evdB/tools/evidence-disposition.py"
python3 - "$S/evdB/tools/evidence-disposition.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = "        except ScratchRootUnusable as exc:\n"
new = "        except RuntimeError as exc:\n"
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
PY
(cd "$S/evdB" && out=$(TMPDIR="$S/tmpok" PYTHONDONTWRITEBYTECODE=1 python3 tools/evidence-disposition.py --selftest 2>&1); echo "    rc=$? traceback=$(printf '%s' "$out" | grep -c 'Traceback (most recent call last)')"; printf '%s\n' "$out" | tail -1 | sed 's/^/    | /')
echo "5c. one of the three tools without the class, context-capture, same injection:"
mkdir -p "$S/cc/tools" && cp -a "$S/c0/tools/." "$S/cc/tools/"
python3 - "$S/cc/tools/context-capture.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = "        harness = SelftestHarness()\n"
new = '        raise RuntimeError("injected interior bug: fixture case crashed")\n' + old
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
PY
(cd "$S/cc" && out=$(TMPDIR="$S/tmpok" PYTHONDONTWRITEBYTECODE=1 python3 tools/context-capture.py --selftest 2>&1); echo "    rc=$? traceback=$(printf '%s' "$out" | grep -c 'Traceback (most recent call last)')"; printf '%s\n' "$out" | tail -1 | sed 's/^/    | /')

echo
echo "===== 6. conformance checks unchanged ====="
(cd "$LANE" && python3 -c "
import json
rows = json.load(open('tools/registry.json'))['rows']
cells = [(r['name'], r['scratch_root']) for r in rows if 'scratch_root' in r]
print('  rows with scratch_root cell:', len(cells))
print('  cell text:', cells[0][1][:120] + '...')
")
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi >/tmp/census-r54-simpl.txt 2>&1
echo "  census validate rc=$? (last line: $(tail -1 /tmp/census-r54-simpl.txt))"

echo
echo "===== 7. does the arm cover every path that allocates scratch? ====="
(cd "$LANE" && python3 - <<'PY'
import ast
files = ["env-diff", "evidence-disposition", "pin-disposition", "bash-witness-study",
         "context-capture", "registry-check", "repeat-control"]
for n in files:
    src = open("tools/%s.py" % n).read()
    def walk(node, top):
        for ch in ast.iter_child_nodes(node):
            nxt = ch.name if isinstance(ch, ast.FunctionDef) else top
            if isinstance(ch, ast.Call) and getattr(ch.func, "id", "") == "strict_scratch_root":
                print("   %-22s line %5d inside %s" % (n, ch.lineno, top))
            walk(ch, nxt)
    walk(ast.parse(src), "<module>")
PY
)
echo "  -> env-diff also allocates on its run path (execute), not only in selftest."
D="$S/fixrepo"; mkdir -p "$D"
(cd "$D" && git init -q . && printf '#!/bin/bash\nprintf "stable\\n"\n' > target.sh && chmod +x target.sh \
 && git -c user.name=f -c user.email=f@invalid add target.sh \
 && git -c user.name=f -c user.email=f@invalid commit -qm fixture >/dev/null)
echo "  fixture toplevel: $(git -C "$D" rev-parse --show-toplevel)"
REV=$(git -C "$D" rev-parse HEAD); SHA=$(sha256sum "$D/target.sh" | cut -d" " -f1)
printf '{"surfaces": [{"name": "one", "repo": "%s", "rev": "%s", "path": "target.sh", "interp": "bash", "blob_sha256": "%s"}]}\n' "$D" "$REV" "$SHA" > "$S/contract.json"
mkdir -p "$S/tmpok"
echo "  7a. env-diff RUN path, usable TMPDIR (control):"
(cd "$S/c0" && out=$(TMPDIR="$S/tmpok" PYTHONDONTWRITEBYTECODE=1 python3 tools/env-diff.py --contract "$S/contract.json" --out "$S/r-ok.json" 2>&1); echo "    rc=$? last=$(printf '%s' "$out" | tail -1)")
echo "  7b. env-diff RUN path, unusable TMPDIR:"
(cd "$S/c0" && out=$(TMPDIR=/nonexistent/nope-r54 PYTHONDONTWRITEBYTECODE=1 python3 tools/env-diff.py --contract "$S/contract.json" --out "$S/r-bad.json" 2>&1); echo "    rc=$? traceback=$(printf '%s' "$out" | grep -c 'Traceback (most recent call last)')"; printf '%s\n' "$out" | tail -1 | cut -c1-150 | sed 's/^/    | /')

echo
echo "===== 8. what the lane's own registry runner does with the class ====="
echo "  8a. registry-check --only env-diff-selftest under an unusable TMPDIR:"
(cd "$S/c0" && out=$(TMPDIR=/nonexistent/nope-r54 PYTHONDONTWRITEBYTECODE=1 python3 tools/registry-check.py --root . --only env-diff-selftest 2>&1); echo "    rc=$?"; printf '%s\n' "$out" | grep -E "ROW |REGISTRY_CHECK" | sed 's/^/    | /')
echo "  8b. the contract note's rule this is measured against:"
(cd "$LANE" && grep -n "never 1 (a verdict" corpus/knowledge/scratch-root-contract.md | sed 's/^/    /')

echo
echo "===== 9. the current tip (the lane moved while this seat ran) ====="
TIP=$(git -C "$LANE" rev-parse HEAD)
echo "  tip=$TIP  ($(git -C "$LANE" log -1 --format=%s | cut -c1-100))"
clone_at "$S/tip" "$TIP" >/dev/null
(cd "$S/tip" && python3 - <<'PY'
import ast
sites = {}
for n in ["env-diff", "evidence-disposition", "pin-disposition", "bash-witness-study"]:
    src = open("tools/%s.py" % n).read()
    t = ast.parse(src)
    cls = [x for x in t.body if isinstance(x, ast.ClassDef) and x.name == "ScratchRootUnusable"]
    arms = [x.lineno for x in ast.walk(t) if isinstance(x, ast.ExceptHandler)
            and x.type is not None and getattr(x.type, "id", "") == "ScratchRootUnusable"]
    sites[n] = (len(cls), arms)
    print("   %-22s class_blocks=%d arm_sites=%s" % (n, len(cls), arms))
print("   totals: class_blocks=%d arm_sites=%d" %
      (sum(v[0] for v in sites.values()), sum(len(v[1]) for v in sites.values())))
PY
)
echo "  9a. env-diff RUN path at the tip, unusable TMPDIR:"
(cd "$S/tip" && out=$(TMPDIR=/nonexistent/nope-r54 PYTHONDONTWRITEBYTECODE=1 python3 tools/env-diff.py --contract "$S/contract.json" --out "$S/r-tip.json" 2>&1); echo "    rc=$? traceback=$(printf '%s' "$out" | grep -c 'Traceback (most recent call last)') lines=$(printf '%s\n' "$out" | wc -l)"; printf '%s\n' "$out" | tail -1 | cut -c1-140 | sed 's/^/    | /')
echo "  9b. the commit that closed it:"
(git -C "$LANE" log --oneline 59c38109bf11.."$TIP" -- tools/env-diff.py | sed 's/^/    /')

echo
echo "===== 10. the one intra-file deletion candidate: merge env-diff's two identical arms ====="
rm -rf "$S/v2"; mkdir -p "$S/v2"; cp -a "$S/c0/tools" "$S/v2/tools"
python3 - "$S/v2/tools/env-diff.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = "def selftest():\n    checks = []\n"
new = 'def selftest():\n    raise ValueError("injected selftest ValueError")\n    checks = []\n'
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
PY
echo "  10a. C0 shape + a genuine selftest ValueError (the selftest branch is outside the outer try):"
(cd "$S/v2" && before=$(wc -l < tools/env-diff.py); out=$(TMPDIR="$S/tmpok" PYTHONDONTWRITEBYTECODE=1 python3 tools/env-diff.py --selftest 2>&1); echo "    rc=$? traceback=$(printf '%s' "$out" | grep -c 'Traceback (most recent call last)') file_lines=$before")
python3 - "$S/v2/tools/env-diff.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = """    if a.selftest:
        try:
            return selftest()
        except ScratchRootUnusable as exc:
            print("ENVDIFF_SETUP: could-not-evaluate: %s" % exc, file=sys.stderr)
            return 2
    if not a.contract or not a.out or not 1 <= a.jobs <= 3:
        p.error("--contract and --out are required; --jobs must be 1..3")
    try:
        raw = a.contract.read_bytes()
"""
new = """    try:
        if a.selftest:
            return selftest()
        if not a.contract or not a.out or not 1 <= a.jobs <= 3:
            p.error("--contract and --out are required; --jobs must be 1..3")
        raw = a.contract.read_bytes()
"""
assert s.count(old) == 1, s.count(old)
open(p, "w").write(s.replace(old, new))
PY
echo "  10b. the merged arm (inner arm deleted, selftest inside the outer try), same ValueError:"
(cd "$S/v2" && after=$(wc -l < tools/env-diff.py); out=$(TMPDIR="$S/tmpok" PYTHONDONTWRITEBYTECODE=1 python3 tools/env-diff.py --selftest 2>&1); echo "    rc=$? traceback=$(printf '%s' "$out" | grep -c 'Traceback (most recent call last)') file_lines=$after"; printf '%s\n' "$out" | tail -1 | sed 's/^/    | /')
