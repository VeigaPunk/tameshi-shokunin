import hashlib, importlib.util, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
AUD = os.path.join(ROOT, "instr/control-assertion-audit.py")
MUT = lambda m: os.path.join(ROOT, "mut", m, "control-assertion-audit.py")
LANE = os.path.join(ROOT, "lane")
WT = os.path.join(ROOT, "wtclone")
REV = "764aca97e513d650949999362cd4b0f5f0e566a5"
out = []

def say(s):
    out.append(s)
    print(s)

def sh(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr

def make_repo(name, text):
    d = os.path.join(ROOT, "probe", name)
    os.makedirs(d, exist_ok=True)
    subprocess.run(["git", "init", "-q", d], check=True)
    subprocess.run(["git", "-C", d, "config", "user.name", "r98-probe"], check=True)
    subprocess.run(["git", "-C", d, "config", "user.email", "r98-probe@invalid"], check=True)
    open(os.path.join(d, "drv.py"), "w").write(text)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-qm", "probe"], check=True)
    rc, so, se = sh(["git", "-C", d, "rev-parse", "HEAD"])
    return d, so.strip()

def audit(tool, repo, rev):
    rc, so, se = sh([PY, "-I", tool, "--repo", repo, "--rev", rev, "--driver", "drv.py"])
    lines = [l for l in so.splitlines() if l.startswith("CONTROL_ASSERT")]
    return rc, lines, se.strip()

# ---------- survivor diagnostics (audit) ----------
say("=== D1 a5-code-arg-off-by-one: two positional args (add(name, code)) ===")
d1 = ("def run(a):\n    return 1, \"o\"\n\ndef main():\n    code, out = run([\"x\"])\n"
      "    add(\"two-arg\", code)\n")
repo1, rev1 = make_repo("two-arg", d1)
for label, tool in (("pristine", AUD), ("mutant-a5", MUT("a5-code-arg-off-by-one"))):
    rc, lines, err = audit(tool, repo1, rev1)
    say("%-10s rc=%d %s" % (label, rc, " | ".join(lines) or err))

say("=== D2 a9-tuple-index-ignored: second tuple element (add(name, out)) ===")
d2 = ("def run(a):\n    return 1, \"o\"\n\ndef main():\n    code, out = run([\"x\"])\n"
      "    add(\"second-element\", out)\n")
repo2, rev2 = make_repo("second-element", d2)
for label, tool in (("pristine", AUD), ("mutant-a9", MUT("a9-tuple-index-ignored"))):
    rc, lines, err = audit(tool, repo2, rev2)
    say("%-10s rc=%d %s" % (label, rc, " | ".join(lines) or err))

say("=== D3 a10-depth-guard-widened: 10-link name chain ===")
chain = ["def main():", "    a0 = 0"]
for i in range(1, 11):
    chain.append("    a%d = a%d" % (i, i - 1))
chain.append('    add("deep-chain", a10)')
d3 = "\n".join(chain) + "\n"
repo3, rev3 = make_repo("deep-chain", d3)
for label, tool in (("pristine", AUD), ("mutant-a10", MUT("a10-depth-guard-widened"))):
    rc, lines, err = audit(tool, repo3, rev3)
    say("%-10s rc=%d %s" % (label, rc, " | ".join(lines) or err))

# ---------- survivor diagnostics (battery helpers) ----------
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

say("=== D4 b1-rc-accepts-one: class_token_ok with exit 1 ===")
pris = load(os.path.join(ROOT, "instr/guard-refusals.py"), "battery_pristine")
b1 = load(os.path.join(ROOT, "mut/b1-rc-accepts-one/guard-refusals.py"), "battery_b1")
for rc_ in (2, 1, 0):
    say("class_token_ok(token, rc=%d): pristine=%s mutant=%s" % (rc_,
        pris.class_token_ok("edit-no-op", "GUARD_SETUP edit-no-op:row-1\n", rc_),
        b1.class_token_ok("edit-no-op", "GUARD_SETUP edit-no-op:row-1\n", rc_)))

say("=== D5 b6-positive-substring: predicate embedded in a longer line ===")
b6 = load(os.path.join(ROOT, "mut/b6-positive-substring/guard-refusals.py"), "battery_b6")
for text in (pris.PREDICATE + "\n", "note " + pris.PREDICATE + "\n", "GUARD_INERTIA rows=1\n"):
    say("positive_ok(%r, 0): pristine=%s mutant=%s" % (text.strip(),
        pris.positive_ok(text, 0), b6.positive_ok(text, 0)))

say("=== D6 b5-token-from-stderr: frozen tool token stream ===")
gi = open(os.path.join(ROOT, "instr/guard-inertia.py")).read()
say("guard-inertia.py contains 'sys.stderr': %s" % ("sys.stderr" in gi))
say("guard-inertia.py die() prints via stdout: %s" % ('print("GUARD_SETUP " + msg)' in gi))
b5src = open(os.path.join(ROOT, "mut/b5-token-from-stderr/guard-refusals.py")).read()
say("mutant b5 merges stderr into graded text: %s" % ("class_token_ok(name, out + err, rc)" in b5src))

# ---------- post-registration probes (NOT part of the k/n mutant set) ----------
say("=== P1 (post-registration) audit silently drops unlabeled sites ===")
src = open(AUD).read()
old = ('        cls, det = classify(code_expr, node.lineno, assigns)\n'
       '        sites.append((node.lineno, label, cls, det))')
assert src.count(old) == 1
p1 = src.replace(old, '        cls, det = classify(code_expr, node.lineno, assigns)\n'
                        '        if label == "?":\n'
                        '            continue\n'
                        '        sites.append((node.lineno, label, cls, det))', 1)
p1path = os.path.join(ROOT, "probe/p1-skip-unlabeled.py")
open(p1path, "w").write(p1)
for driver in (".ufo/evidence/round-97/controls97.py", ".ufo/evidence/round-98/controls98.py"):
    rc, so, se = sh([PY, "-I", p1path, "--repo", LANE, "--rev", REV, "--driver", driver])
    say("P1 %s rc=%d last=%r" % (driver, rc, so.splitlines()[-1] if so.splitlines() else se.strip()))

say("=== P2 (post-registration) battery reads the worktree tool (wtlane) ===")
src = open(os.path.join(ROOT, "instr/guard-refusals.py")).read()
old = ('    tb = git(lane, ["cat-file", "blob", "%s:%s" % (rev, a.tool)], env)\n'
       '    if tb[0] != 0:\n'
       '        sys.exit(die("tool-absent-at-rev"))\n'
       '    tool_blob = tb[1].encode()')
assert src.count(old) == 1
p2 = src.replace(old, '    try:\n'
                       '        tool_blob = open(os.path.join(lane, a.tool), "rb").read()\n'
                       '    except OSError:\n'
                       '        sys.exit(die("tool-absent-at-rev"))', 1)
p2path = os.path.join(ROOT, "probe/p2-worktree-read.py")
open(p2path, "w").write(p2)
wtlane = os.path.join(ROOT, "wtlane")
if not os.path.isdir(wtlane):
    subprocess.run(["git", "clone", "-q", "--shared", "/home/vgpnk/Projects/shokunin/tameshi-shokunin", wtlane], check=True)
    subprocess.run(["git", "-C", wtlane, "checkout", "-q", "--detach", REV], check=True)
    gt = os.path.join(wtlane, ".ufo/evidence/round-97/c2/guard-inertia.py")
    s = open(gt).read()
    marker = 'print("GUARD_INERTIA rows=%d killed=%d limits=%d survived=%d unmet=%d" % ('
    assert s.count(marker) == 1
    open(gt, "w").write(s.replace(marker, 'print("GUARD_INERTIA rows=%d killed=%d limits=%d survived=%d unmet=%d WORKTREE-EDIT" % (', 1))
say("wtlane worktree tool sha256=%s blob sha256=%s" % (
    hashlib.sha256(open(os.path.join(wtlane, ".ufo/evidence/round-97/c2/guard-inertia.py"), "rb").read()).hexdigest(),
    hashlib.sha256(subprocess.run(["/usr/bin/git", "-C", wtlane, "cat-file", "blob", REV + ":.ufo/evidence/round-97/c2/guard-inertia.py"], capture_output=True).stdout).hexdigest()))
TOOL = ".ufo/evidence/round-97/c2/guard-inertia.py"
SHA = "634997d09d2dba5cd87df12e2844962b3517ede798ab0ce04303807b6db042c8"
import shutil
for label, tool in (("pristine", os.path.join(ROOT, "instr/guard-refusals.py")), ("mutant-p2", p2path)):
    w = os.path.join(ROOT, "probe/work-p2-" + label)
    shutil.rmtree(w, ignore_errors=True)
    rc, so, se = sh([PY, "-I", tool, "--lane", wtlane, "--rev", REV, "--tool", TOOL,
                     "--tool-sha", SHA, "--work", w])
    say("P2 %-10s rc=%d last=%r" % (label, rc, so.splitlines()[-1] if so.splitlines() else se.strip()[:120]))

open(os.path.join(ROOT, "R98M1-survivor-probes.out"), "w").write("\n".join(out) + "\n")
print("WROTE R98M1-survivor-probes.out")
