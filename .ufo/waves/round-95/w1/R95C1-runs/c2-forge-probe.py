#!/usr/bin/env python3
"""R95C1 C2 before-witness probe: demonstrate that the round-94 checker at
6a2a1fdd (a) accepts a receipt that exists only in a working tree, (b) accepts a
committed receipt with a wrong/absent counter_sha=, (c) reads a counter blob
substituted by refs/replace. All clones are scratch."""
import hashlib, os, re, shutil, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "6a2a1fdd"
S = "/fast/scratch/hyaku/tameshi-r95/R95C1"
RUNS = os.path.join(S, "runs")
CHK = os.path.join(LANE, ".ufo/evidence/round-94/conjunct-disposition-v94.py")
COUNTER = ".ufo/evidence/round-94/c1/measure-v94.py"
RCPT = ".ufo/evidence/round-94/pre-freeze/controls"
SEALED = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
          "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
          "GIT_CONFIG_GLOBAL": "/dev/null"}


def sh(*a, check=True, env=SEALED):
    p = subprocess.run(list(a), capture_output=True, text=True, env=env)
    if check and p.returncode != 0:
        raise SystemExit("cmd failed: %s\n%s" % (" ".join(a), p.stderr))
    return p.stdout


def clone(dest):
    shutil.rmtree(dest, ignore_errors=True)
    sh("git", "clone", "-q", "--shared", "--no-checkout", LANE, dest)
    top = sh("git", "-C", dest, "rev-parse", "--show-toplevel").strip()
    assert os.path.realpath(top) == os.path.realpath(dest), (top, dest)
    sh("git", "-C", dest, "checkout", "-q", "--detach", REV)
    return dest


def commit(repo, msg):
    sh("git", "-C", repo, "add", "-A")
    sh("git", "-C", repo, "-c", "user.name=r95-critic", "-c", "user.email=r95-critic@invalid",
       "commit", "-q", "-m", msg)
    return sh("git", "-C", repo, "rev-parse", "HEAD").strip()


def run_checker(lane, tag):
    p = subprocess.run([sys.executable, "-I", CHK, "--lane", lane, "--rev", "HEAD",
                        "--min-falsifiable", "17"], capture_output=True, text=True)
    body = "forge=%s lane=%s\nexit=%d\n" % (tag, lane, p.returncode) + p.stdout + p.stderr
    open(os.path.join(RUNS, tag + ".out"), "w").write(body)
    return p.returncode, p.stdout


def main():
    os.makedirs(RUNS, exist_ok=True)
    # (a) receipt present only in the working tree, never committed
    a = clone(os.path.join(S, "c2-a"))
    forged = os.path.join(a, RCPT, "hidden-c001.out")
    open(forged, "w").write("hand-written receipt, never committed\n"
                            "C1_CONJUNCTS verdict_tables=false\n")
    code, out = run_checker(a, "forge-handwritten-v94")
    print("forge-handwritten-v94 exit=%d %s" % (
        code, [l for l in out.split("\n") if l.startswith("DISPOSITION rows=")]))
    print("  git status:", [l for l in sh("git", "-C", a, "status", "--porcelain").split("\n") if l][:2])

    # (b) committed receipt with counter_sha=0*64 (v94 never reads the line)
    b = clone(os.path.join(S, "c2-b"))
    p = os.path.join(b, RCPT, "figure.out")
    body = open(p).read()
    open(p, "w").write("counter_sha=" + "0" * 64 + "\n" + body)
    commit(b, "r95 forge: wrong counter_sha in a committed receipt")
    code, out = run_checker(b, "forge-counter-sha-v94")
    print("forge-counter-sha-v94 exit=%d %s" % (
        code, [l for l in out.split("\n") if l.startswith("DISPOSITION rows=")]))
    print("  receipt line:", [l for l in open(p).read().split("\n") if l.startswith("counter_sha=")][0][:40])

    # (c) refs/replace substitutes the counter blob; v94 reads the replacement
    c = clone(os.path.join(S, "c2-c"))
    orig = sh("git", "-C", c, "rev-parse", "HEAD:" + COUNTER).strip()
    cb = subprocess.run(["git", "-C", c, "cat-file", "blob", orig], capture_output=True,
                        env=SEALED).stdout
    m = re.search(rb'^SELF_SHA256 = "([0-9a-f]{64})"\n', cb, re.M)
    anchor = b'if __name__ == "__main__":'
    fake = (b'SELF_SHA256 = "' + b"0" * 64 + b'"\n')
    repl = cb.replace(anchor, fake + anchor, 1)
    new = sh_stdin(c, ["git", "-C", c, "hash-object", "-w", "--stdin"], repl).strip()
    sh("git", "-C", c, "replace", orig, new)
    print("  orig=%s new=%s" % (orig, new))
    print("  cat-file after replace sha256=%s" % hashlib.sha256(
        subprocess.run(["git", "-C", c, "cat-file", "blob", "HEAD:" + COUNTER],
                       capture_output=True, env=SEALED).stdout).hexdigest())
    code, out = run_checker(c, "forge-replace-ref-v94")
    inst = [l for l in out.split("\n") if l.startswith("DISPOSITION_INSTRUMENT")]
    row = [l for l in out.split("\n") if l.startswith("DISPOSITION rows=")]
    print("forge-replace-ref-v94 exit=%d %s %s" % (code, inst, row))
    sh("git", "-C", c, "replace", "-d", orig)


def sh_stdin(cwd_args, cmd, data):
    p = subprocess.run(cmd, input=data, capture_output=True, env=SEALED)
    if p.returncode != 0:
        raise SystemExit(p.stderr)
    return p.stdout.decode()


if __name__ == "__main__":
    sys.exit(main())
