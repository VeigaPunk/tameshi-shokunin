#!/usr/bin/env python3
"""R98R1 adversarial fixture generator + runner.

Creates a scratch git repo, commits one driver per attack, runs
tools/control-assertion-audit.py on each committed blob, executes the
runnable fixtures to prove what they record at runtime, and leaves one
<fixture>.audit.txt / <fixture>.run.txt per fixture.

Every git mutation in the fixture repo is preceded by a toplevel assertion.
"""
import os
import subprocess
import sys

ROOT = "/fast/scratch/hyaku/tameshi-r98/R98R1"
REPO = os.path.join(ROOT, "fixtures")
RECEIPTS = os.path.join(ROOT, "receipts")
TOOL = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/control-assertion-audit.py"
LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"

FIXTURES = {}

FIXTURES["f01_module_const.py"] = '''\
RC = 0


def add(name, code, body, want_code):
    pass


def main():
    add("module-const", RC, "body", 0)
'''

FIXTURES["f02_ifelse_runner_last.py"] = '''\
import subprocess

RECORDED = []


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main(c):
    if c:
        rc = 7
    else:
        p = subprocess.run(["true"])
        rc = p.returncode
    add("ifelse", rc, "body", 0)


if __name__ == "__main__":
    import sys
    main(len(sys.argv) > 1)
    print(RECORDED)
'''

FIXTURES["f02b_ifelse_literal_last.py"] = '''\
import subprocess

RECORDED = []


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main(c):
    if c:
        p = subprocess.run(["true"])
        rc = p.returncode
    else:
        rc = 7
    add("ifelse-swapped", rc, "body", 0)


if __name__ == "__main__":
    main(True)
    print(RECORDED)
'''

FIXTURES["f03_try_except_fallback.py"] = '''\
import subprocess

RECORDED = []


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main():
    try:
        p = subprocess.run(["true"])
        rc = p.returncode
    except Exception:
        rc = 7
    add("try-fallback", rc, "body", 0)


if __name__ == "__main__":
    main()
    print(RECORDED)
'''

FIXTURES["f04_getattr.py"] = '''\
import subprocess


def add(name, code, body, want_code):
    pass


def main():
    p = subprocess.run(["true"])
    add("getattr", getattr(p, "returncode"), "body", 0)
'''

FIXTURES["f05_attrgetter.py"] = '''\
import operator
import subprocess


def add(name, code, body, want_code):
    pass


def main():
    p = subprocess.run(["true"])
    rc = operator.attrgetter("returncode")(p)
    add("attrgetter", rc, "body", 0)
'''

FIXTURES["f06_subclass_result.py"] = '''\
import subprocess


class Result(subprocess.CompletedProcess):
    pass


def add(name, code, body, want_code):
    pass


def main():
    p = Result(["true"], 0)
    add("subclass", p.returncode, "body", 0)
'''

FIXTURES["f07_lambda_call.py"] = '''\
def add(name, code, body, want_code):
    pass


def main():
    add("lambda-call", (lambda: 0)(), "body", 0)
'''

FIXTURES["f08_shadowed_add.py"] = '''\
import subprocess

RECORDED = []


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def add(name, code, body, want_code):
    RECORDED.append((name, 0, body, want_code))


def main():
    p = subprocess.run(["true"])
    add("shadowed", p.returncode, "body", 0)


if __name__ == "__main__":
    main()
    print(RECORDED)
'''

FIXTURES["f09_other_recorder.py"] = '''\
RECORDED = []


def record(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main():
    record("x", 0, "body", 0)
    record("y", 7, "body", 0)


if __name__ == "__main__":
    main()
    print(RECORDED)
'''

FIXTURES["f10_loop_two_sites.py"] = '''\
import subprocess


def add(name, code, body, want_code):
    pass


def main():
    for n in ("a", "b"):
        p = subprocess.run(["true"])
        add(n, p.returncode, "body", 0)
        add(n + "-2", p.returncode, "body", 0)
'''

FIXTURES["f11_local_run_literal.py"] = '''\
RECORDED = []


def run(cmd):
    return 0, ""


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main():
    code, out = run(["git", "grep", "-c", "GUARD_INERTIA"])
    add("literal-via-local-run", code, "body", 1)


if __name__ == "__main__":
    main()
    print(RECORDED)
'''

FIXTURES["f12_attr_mutation.py"] = '''\
import subprocess

RECORDED = []


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main():
    p = subprocess.run(["true"])
    p.returncode = 0
    add("mutated-attr", p.returncode, "body", 1)


if __name__ == "__main__":
    main()
    print(RECORDED)
'''

FIXTURES["f13_dead_branch.py"] = '''\
import subprocess

RECORDED = []


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main():
    rc = 7
    if False:
        p = subprocess.run(["true"])
        rc = p.returncode
    add("dead-branch", rc, "body", 1)


if __name__ == "__main__":
    main()
    print(RECORDED)
'''

FIXTURES["f14_worktree_blob.py"] = '''\
import subprocess


def add(name, code, body, want_code):
    pass


def main():
    p = subprocess.run(["true"])
    add("worktree-blob", p.returncode, "body", 0)
'''

FIXTURES["f15_method_add.py"] = '''\
class Collector:
    def add(self, name, code, body, want_code):
        pass


def main():
    c = Collector()
    c.add("method-add", 7, "body", 0)
'''

FIXTURES["f16_keyword_code.py"] = '''\
def add(name, code, body, want_code):
    pass


def main():
    add("keyword-code", code=7, body="b", want_code=0)
'''

FIXTURES["f17_cross_scope.py"] = '''\
import subprocess


def add(name, code, body, want_code):
    pass


def helper():
    p = subprocess.run(["true"])


def main():
    add("cross-scope", p.returncode, "body", 0)
'''

FIXTURES["f18_augassign.py"] = '''\
import subprocess

RECORDED = []


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main():
    p = subprocess.run(["true"])
    rc = p.returncode
    rc += 7
    add("augassign", rc, "body", 0)


if __name__ == "__main__":
    main()
    print(RECORDED)
'''
FIXTURES["f19_fifteen_fake_run.py"] = '''\\
RECORDED = []


def run(cmd):
    return 0, ""


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main():
    code, out = run(["git", "grep", "-c", "TOKEN-1"])
    add("fake-01", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-2"])
    add("fake-02", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-3"])
    add("fake-03", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-4"])
    add("fake-04", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-5"])
    add("fake-05", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-6"])
    add("fake-06", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-7"])
    add("fake-07", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-8"])
    add("fake-08", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-9"])
    add("fake-09", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-10"])
    add("fake-10", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-11"])
    add("fake-11", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-12"])
    add("fake-12", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-13"])
    add("fake-13", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-14"])
    add("fake-14", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-15"])
    add("fake-15", code, "body", 1)


if __name__ == "__main__":
    main()
    print(len(RECORDED), set(r[1] for r in RECORDED))
'''

EXECUTE = {
    "f02_ifelse_runner_last.py": ["x"],
    "f02b_ifelse_literal_last.py": [],
    "f03_try_except_fallback.py": [],
    "f08_shadowed_add.py": [],
    "f09_other_recorder.py": [],
    "f11_local_run_literal.py": [],
    "f12_attr_mutation.py": [],
    "f13_dead_branch.py": [],
    "f18_augassign.py": [],
    "f19_fifteen_fake_run.py": [],
}


def run(argv, cwd=None):
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def assert_toplevel(repo):
    rc, out = run(["git", "rev-parse", "--show-toplevel"], cwd=repo)
    top = os.path.realpath(out.strip().splitlines()[-1]) if out.strip() else "<none>"
    if rc != 0 or top != os.path.realpath(repo):
        raise SystemExit("TOPLEVEL-ASSERT-FAIL rc=%d got=%r want=%r" % (rc, top, repo))


def main():
    os.makedirs(REPO, exist_ok=True)
    os.makedirs(RECEIPTS, exist_ok=True)
    if not os.path.isdir(os.path.join(REPO, ".git")):
        rc, out = run(["git", "init", "-q", "-b", "main"], cwd=REPO)
        if rc != 0:
            raise SystemExit("git init failed: " + out)
        run(["git", "config", "user.name", "r98r1-fixture"], cwd=REPO)
        run(["git", "config", "user.email", "r98r1@invalid"], cwd=REPO)
    assert_toplevel(REPO)
    for name, text in FIXTURES.items():
        with open(os.path.join(REPO, name), "w", encoding="utf-8") as f:
            f.write(text)
    rc, out = run(["git", "add", "-A"], cwd=REPO)
    assert_toplevel(REPO)
    rc, out = run(["git", "commit", "-qm", "R98R1 adversarial fixtures"], cwd=REPO)
    assert_toplevel(REPO)
    rc, out = run(["git", "rev-parse", "HEAD"], cwd=REPO)
    rev = out.strip()
    print("FIXTURE_REPO %s rev=%s" % (REPO, rev))

    summary = []
    for name in sorted(FIXTURES):
        cmd = ["python3", "-I", TOOL, "--repo", REPO, "--rev", rev,
               "--driver", name]
        rc, out = run(cmd)
        with open(os.path.join(RECEIPTS, name.replace(".py", ".audit.txt")), "w",
                  encoding="utf-8") as f:
            f.write("$ %s\n%s\nrc=%d\n" % (" ".join(cmd), out, rc))
        last = [ln for ln in out.splitlines() if ln.startswith("CONTROL_ASSERT sites=")]
        summary.append((name, rc, last[-1] if last else out.strip()))

    # kill rule (e): a worktree-only edit must not change the audit line.
    wt = os.path.join(REPO, "f14_worktree_blob.py")
    committed = open(wt, encoding="utf-8").read()
    with open(wt, "w", encoding="utf-8") as f:
        f.write(committed.replace("p.returncode", "7"))
    cmd = ["python3", "-I", TOOL, "--repo", REPO, "--rev", rev,
           "--driver", "f14_worktree_blob.py"]
    rc, out = run(cmd)
    with open(os.path.join(RECEIPTS, "f14_worktree_blob.worktree-edit.audit.txt"), "w",
              encoding="utf-8") as f:
        f.write("$ %s\n%s\nrc=%d\n" % (" ".join(cmd), out, rc))
    summary.append(("f14_worktree_blob.py(wt-edit)", rc,
                    [ln for ln in out.splitlines() if ln.startswith("CONTROL_ASSERT sites=")][-1]))
    with open(wt, "w", encoding="utf-8") as f:
        f.write(committed)

    for name, extra in EXECUTE.items():
        cmd = ["python3", name] + extra
        rc, out = run(cmd, cwd=REPO)
        with open(os.path.join(RECEIPTS, name.replace(".py", ".run.txt")), "w",
                  encoding="utf-8") as f:
            f.write("$ %s\n%s\nrc=%d\n" % (" ".join(cmd), out, rc))

    print("\n=== SUMMARY ===")
    for name, rc, last in summary:
        print("%-32s rc=%d %s" % (name, rc, last))
    return 0


if __name__ == "__main__":
    sys.exit(main())
