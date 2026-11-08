#!/usr/bin/env python3
"""R95C1 C2 instrument probe: exercise the v95 disposition checker against a
scratch clone carrying the v95 draft instruments and a SYNTHETIC receipt set
(round-94 receipts + the v95 counter_sha) — the real battery receipts do not
exist yet. Then run the three forged artifacts. Read-only on the lane."""
import hashlib, os, shutil, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
HEAD = subprocess.run(["git", "-C", LANE, "rev-parse", "HEAD"], capture_output=True,
                      text=True).stdout.strip()
S = "/fast/scratch/hyaku/tameshi-r95/R95C1"
RUNS = os.path.join(S, "runs")
CHK = ".ufo/evidence/round-95/conjunct-disposition-v95.py"
COUNTER = ".ufo/evidence/round-95/c1/measure-v95.py"
MANIFEST = ".ufo/evidence/round-95/conjunct-disposition.json"
RECEIPTS = ".ufo/evidence/round-95/pre-freeze/controls"
V94_RECEIPTS = os.path.join(LANE, ".ufo/evidence/round-94/pre-freeze/controls")
SEALED = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
          "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}


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
    sh("git", "-C", dest, "checkout", "-q", "--detach", HEAD)
    for rel in [COUNTER, ".ufo/evidence/round-95/c1/census-mutants.json",
                ".ufo/evidence/round-95/c1/pins.json", MANIFEST, CHK]:
        d = os.path.join(dest, os.path.dirname(rel))
        os.makedirs(d, exist_ok=True)
        shutil.copy2(os.path.join(LANE, rel), os.path.join(dest, rel))
    shutil.copytree(os.path.join(LANE, ".ufo/evidence/round-95/sources"),
                    os.path.join(dest, ".ufo/evidence/round-95/sources"), dirs_exist_ok=True)
    return dest


def commit(repo, msg):
    sh("git", "-C", repo, "add", "-A")
    sh("git", "-C", repo, "-c", "user.name=r95-critic", "-c", "user.email=r95-critic@invalid",
       "commit", "-q", "-m", msg)
    return sh("git", "-C", repo, "rev-parse", "HEAD").strip()


def put_receipts(repo, counter_sha, skip=()):
    dst = os.path.join(repo, RECEIPTS)
    os.makedirs(dst, exist_ok=True)
    for name in sorted(os.listdir(V94_RECEIPTS)):
        if not name.endswith(".out"):
            continue
        state = name[:-4]
        if state in skip:
            continue
        body = open(os.path.join(V94_RECEIPTS, name), encoding="utf-8").read()
        with open(os.path.join(dst, name), "w", encoding="utf-8") as f:
            f.write("counter_sha=%s\n" % counter_sha + body)


def run(repo, rev, tag, extra=()):
    p = subprocess.run([sys.executable, "-I", os.path.join(repo, CHK), "--lane", repo,
                        "--rev", rev, "--min-falsifiable", "17", *extra],
                       capture_output=True, text=True)
    body = "probe=%s rev=%s\nexit=%d\n" % (tag, rev, p.returncode) + p.stdout + p.stderr
    with open(os.path.join(RUNS, tag + ".out"), "w", encoding="utf-8") as f:
        f.write(body)
    summary = [l for l in p.stdout.split("\n") if l.startswith("DISPOSITION rows=")]
    finds = [l for l in p.stdout.split("\n") if l.startswith("DISPOSITION_FINDING")]
    setup = [l for l in p.stdout.split("\n") if l.startswith("DISPOSITION_SETUP")]
    return p.returncode, summary, finds, setup


def main():
    os.makedirs(RUNS, exist_ok=True)
    repo = clone(os.path.join(S, "c2v95-store"))
    r_instr = commit(repo, "r95 critic: v95 instruments only")
    counter_sha = hashlib.sha256(open(os.path.join(repo, COUNTER), "rb").read()).hexdigest()

    code, summary, finds, setup = run(repo, r_instr, "c2-v95-instrument-only-rev")
    print("instrument-only rev exit=%d %s findings=%d %s" % (
        code, summary, len(finds), finds[:2]))

    put_receipts(repo, counter_sha)
    r_rcpt = commit(repo, "r95 critic: synthetic receipt set (round-94 receipts + v95 counter_sha)")
    code, summary, finds, setup = run(repo, r_rcpt, "c2-v95-synthetic-positive")
    print("synthetic positive exit=%d %s findings=%d %s" % (
        code, summary, len(finds), finds[:3]))

    # forge 1: a manifest-state receipt present only in the working tree (16 committed)
    repo2 = clone(os.path.join(S, "c2v95-forge1"))
    put_receipts(repo2, counter_sha, skip=("hidden-c001",))
    commit(repo2, "r95 critic: 16 of 17 receipts committed")
    with open(os.path.join(repo2, RECEIPTS, "hidden-c001.out"), "w") as f:
        f.write("counter_sha=%s\nhand-written, never committed\nC1_CONJUNCTS verdict_tables=false\n"
                % counter_sha)
    print("  worktree-only file status:",
          [l for l in sh("git", "-C", repo2, "status", "--porcelain").split("\n") if l][:2])
    code, summary, finds, setup = run(repo2, "HEAD", "c2-v95-forge-handwritten")
    print("forge-handwritten exit=%d %s findings=%s" % (code, summary, finds))

    # forge 2: a committed receipt whose counter_sha is 0*64
    repo3 = clone(os.path.join(S, "c2v95-forge2"))
    put_receipts(repo3, counter_sha)
    p = os.path.join(repo3, RECEIPTS, "figure.out")
    body = open(p).read().replace("counter_sha=" + counter_sha, "counter_sha=" + "0" * 64, 1)
    open(p, "w").write(body)
    commit(repo3, "r95 critic: forged counter_sha in a committed receipt")
    code, summary, finds, setup = run(repo3, "HEAD", "c2-v95-forge-counter-sha")
    print("forge-counter-sha exit=%d %s findings=%s" % (code, summary, finds))

    # forge 3: refs/replace inside the clone (counter blob, then an unrelated blob)
    repo4 = clone(os.path.join(S, "c2v95-forge3"))
    put_receipts(repo4, counter_sha)
    r_clean = commit(repo4, "r95 critic: clean receipt set for replace probe")
    counter_oid = sh("git", "-C", repo4, "rev-parse", r_clean + ":" + COUNTER).strip()
    manifest_oid = sh("git", "-C", repo4, "rev-parse", r_clean + ":" + MANIFEST).strip()
    sh("git", "-C", repo4, "replace", counter_oid, manifest_oid)
    print("  replace list len under GIT_NO_REPLACE_OBJECTS=1:",
          len([l for l in sh("git", "-C", repo4, "replace", "-l").split("\n") if l]))
    code, summary, finds, setup = run(repo4, r_clean, "c2-v95-forge-replace-ref")
    print("forge-replace-ref exit=%d %s setup=%s" % (code, summary, setup))
    sh("git", "-C", repo4, "replace", "-d", counter_oid)
    # unrelated blob: replace the note blob with the README blob
    note_oid = sh("git", "-C", repo4, "rev-parse", r_clean + ":corpus/README.md").strip()
    readme_oid = sh("git", "-C", repo4, "rev-parse", r_clean + ":corpus/SOURCES.md").strip()
    sh("git", "-C", repo4, "replace", note_oid, readme_oid)
    code, summary, finds, setup = run(repo4, r_clean, "c2-v95-forge-replace-unrelated")
    print("forge-replace-unrelated exit=%d %s setup=%s" % (code, summary, setup))


if __name__ == "__main__":
    sys.exit(main())
