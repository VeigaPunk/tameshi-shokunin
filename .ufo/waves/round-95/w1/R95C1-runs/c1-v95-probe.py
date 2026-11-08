#!/usr/bin/env python3
"""R95C1 probe 3: (a) the five C1 state fixtures through the v95 reader and the
v95 counter module; (b) a full v95 counter run on the honest committed note in a
scratch clone carrying the v95 drafts (no round-95 lesson -> the source conjunct
is the only expected failure); (c) the v95 driver's expectation count with a stub
round-95 lesson; (d) the exact v94 working-tree receipt forge; (e) a receipt with
the counter_sha line absent."""
import hashlib, importlib.util, json, os, shutil, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
HEAD = subprocess.run(["git", "-C", LANE, "rev-parse", "HEAD"], capture_output=True,
                      text=True).stdout.strip()
S = "/fast/scratch/hyaku/tameshi-r95/R95C1"
RUNS = os.path.join(S, "runs")
SEALED = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
          "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
V95 = [".ufo/evidence/round-95/c1/measure-v95.py",
       ".ufo/evidence/round-95/c1/controls-v95.py",
       ".ufo/evidence/round-95/c1/census-mutants.json",
       ".ufo/evidence/round-95/c1/pins.json",
       ".ufo/evidence/round-95/c1/make-pins95.py",
       ".ufo/evidence/round-95/conjunct-disposition-v95.py",
       ".ufo/evidence/round-95/conjunct-disposition.json"]


def sh(*a, check=True, env=SEALED):
    p = subprocess.run(list(a), capture_output=True, text=True, env=env)
    if check and p.returncode != 0:
        raise SystemExit("cmd failed: %s\n%s" % (" ".join(a), p.stderr))
    return p.stdout


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def clone(dest, stub_lesson=False):
    shutil.rmtree(dest, ignore_errors=True)
    sh("git", "clone", "-q", "--shared", "--no-checkout", LANE, dest)
    assert os.path.realpath(sh("git", "-C", dest, "rev-parse", "--show-toplevel").strip()) \
        == os.path.realpath(dest)
    sh("git", "-C", dest, "checkout", "-q", "--detach", HEAD)
    for rel in V95:
        os.makedirs(os.path.join(dest, os.path.dirname(rel)), exist_ok=True)
        shutil.copy2(os.path.join(LANE, rel), os.path.join(dest, rel))
    shutil.copytree(os.path.join(LANE, ".ufo/evidence/round-95/sources"),
                    os.path.join(dest, ".ufo/evidence/round-95/sources"), dirs_exist_ok=True)
    if stub_lesson:
        p = os.path.join(dest, "corpus/lessons/round-95.md")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write("# round-95 lesson stub (critic probe only)\n")
    return dest


def commit(repo, msg):
    sh("git", "-C", repo, "add", "-A")
    sh("git", "-C", repo, "-c", "user.name=r95-critic", "-c", "user.email=r95-critic@invalid",
       "commit", "-q", "-m", msg)
    return sh("git", "-C", repo, "rev-parse", "HEAD").strip()


def main():
    os.makedirs(RUNS, exist_ok=True)
    # (c) driver expectation count with a stub lesson (its states() reads the lesson)
    stub = clone(os.path.join(S, "c1-stub"), stub_lesson=True)
    drv = load("drv95", os.path.join(stub, ".ufo/evidence/round-95/c1/controls-v95.py"))
    C = drv.states(stub)
    total = len(set(C) | set(drv.EXPECT_EXTRA))
    print("driver states()=%d EXPECT_EXTRA=%d total=%d" % (len(C), len(drv.EXPECT_EXTRA), total))
    print("added:", [n for n in C if n in ("indent-code-row", "indent-token",
                                           "escaped-backslash-pipe", "two-hyphen-delimiter")],
          "extra:", sorted(drv.EXPECT_EXTRA))
    with open(os.path.join(RUNS, "c1-driver-count.txt"), "w") as f:
        f.write("states()=%d EXPECT_EXTRA=%d total=%d\n" % (len(C), len(drv.EXPECT_EXTRA), total))
        f.write("total names: " + ",".join(sorted(set(C) | set(drv.EXPECT_EXTRA))) + "\n")

    # (a) the five fixtures through the v95 reader
    v95 = load("c95", os.path.join(LANE, ".ufo/evidence/round-95/c1/measure-v95.py"))
    note_path = "corpus/knowledge/mutation-case-fleet-sources-census.md"
    ids = set(drv.DERIVED)
    out = []
    for name in ("indent-code-row", "indent-token", "escaped-backslash-pipe", "two-hyphen-delimiter"):
        spec = C[name]
        note = list(spec["files"].values())[0]
        r, b, i = v95.parse_note(note, ids)
        block = "\n".join(t for _, t in v95.block_lines(note))
        import re as _re
        heads = _re.findall(r"^measured: (\d+)/(\d+) killed\s*$", block, _re.M)
        out.append("%-24s v95 verdict_tables=%d badrows=%d ids_rows=%d bad=%s figures=%s" % (
            name, i["verdict_tables"], len(b), len(r), b[:2], heads))
        print(out[-1])
    with open(os.path.join(RUNS, "c1-five-states-v95-reader.txt"), "w") as f:
        f.write("\n".join(out) + "\n")

    # (b) full v95 counter run on the honest committed note, no round-95 lesson
    run_repo = clone(os.path.join(S, "c1-full"), stub_lesson=False)
    rev = commit(run_repo, "r95 critic: v95 drafts on HEAD, no round-95 lesson")
    work = os.path.join(S, "c1-full-work")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    p = subprocess.run([sys.executable, "-I", os.path.join(run_repo, V95[0]),
                        "--repo", run_repo, "--rev", rev, "--work", work],
                       capture_output=True, text=True)
    body = "probe=c1-full-note-no-lesson rev=%s\nexit=%d\n" % (rev, p.returncode) + p.stdout + p.stderr
    open(os.path.join(RUNS, "c1-full-note-no-lesson.out"), "w").write(body)
    keep = [l for l in p.stdout.split("\n")
            if l.startswith("C1_SUMMARY") or l.startswith("C1_CONJUNCTS") or l.startswith("C1_SOURCE")
            or l.startswith("C1_SETUP") or l.startswith("C1_R95_PASS")]
    print("full counter exit=%d" % p.returncode)
    for l in keep:
        print("  " + l[:240])

    # (d) exact v94 working-tree forge: a receipt name absent from the store, file untracked
    rdir = os.path.join(S, "v94-receipts-forge")
    shutil.rmtree(rdir, ignore_errors=True)
    shutil.copytree(os.path.join(LANE, ".ufo/evidence/round-94/pre-freeze/controls"), rdir)
    os.unlink(os.path.join(rdir, "hidden-c001.out"))
    open(os.path.join(rdir, "hidden-c001.out"), "w").write(
        "hand-written receipt, present only in this directory\nC1_CONJUNCTS verdict_tables=false\n")
    chk94 = os.path.join(LANE, ".ufo/evidence/round-94/conjunct-disposition-v94.py")
    p = subprocess.run([sys.executable, "-I", chk94, "--lane", LANE, "--rev", "6a2a1fdd",
                        "--receipts", rdir, "--min-falsifiable", "17"],
                       capture_output=True, text=True)
    open(os.path.join(RUNS, "forge-handwritten-v94-untracked.out"), "w").write(
        "probe=forge-handwritten-v94-untracked receipts=%s\nexit=%d\n" % (rdir, p.returncode)
        + p.stdout + p.stderr)
    print("v94 untracked-receipt forge exit=%d %s" % (
        p.returncode, [l for l in p.stdout.split("\n") if l.startswith("DISPOSITION rows=")]))

    # (e) v95: a committed receipt with the counter_sha line absent
    store = clone(os.path.join(S, "c2v95-nosha"))
    counter_sha = hashlib.sha256(open(os.path.join(store, V95[0]), "rb").read()).hexdigest()
    dst = os.path.join(store, ".ufo/evidence/round-95/pre-freeze/controls")
    os.makedirs(dst, exist_ok=True)
    for name in sorted(os.listdir(os.path.join(LANE, ".ufo/evidence/round-94/pre-freeze/controls"))):
        if not name.endswith(".out"):
            continue
        body = open(os.path.join(LANE, ".ufo/evidence/round-94/pre-freeze/controls", name)).read()
        open(os.path.join(dst, name), "w").write("counter_sha=%s\n" % counter_sha + body)
    pth = os.path.join(dst, "figure.out")
    open(pth, "w").write(open(pth).read().replace("counter_sha=" + counter_sha + "\n", "", 1))
    rev = commit(store, "r95 critic: counter_sha line absent from figure.out")
    chk95 = os.path.join(store, ".ufo/evidence/round-95/conjunct-disposition-v95.py")
    p = subprocess.run([sys.executable, "-I", chk95, "--lane", store, "--rev", rev,
                        "--min-falsifiable", "17"], capture_output=True, text=True)
    open(os.path.join(RUNS, "c2-v95-forge-counter-sha-absent.out"), "w").write(
        "probe=counter_sha-absent rev=%s\nexit=%d\n" % (rev, p.returncode) + p.stdout + p.stderr)
    print("v95 absent counter_sha exit=%d %s" % (
        p.returncode, [l for l in p.stdout.split("\n")
                       if l.startswith("DISPOSITION rows=") or l.startswith("DISPOSITION_FINDING")]))


if __name__ == "__main__":
    sys.exit(main())
