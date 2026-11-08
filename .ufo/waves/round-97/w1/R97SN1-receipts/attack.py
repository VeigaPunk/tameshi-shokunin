import hashlib, json, os, subprocess, sys, tarfile, tempfile, shutil

CLONE = "/fast/scratch/hyaku/tameshi-r97/R97SN1/clone"
FREEZE = "e72a0c8bde44920554dc81c88c0dbb8dde491977"
DRIVER_SHA = "88bcca8651f6a60568c0b74346796b5ce3407a9b2c8ac70ca7f229102d3c0ff5"
CHECKER_SHA = "02a5482a573193c37bd9ebfa9303e84284561f50326043967834c9fdbf0d1c80"
RCPT_DIR = ".ufo/evidence/round-96/pre-freeze/controls"
MANIFEST = ".ufo/evidence/round-97/c2/guard-inertia.json"
ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "/fast/scratch/hyaku/tameshi-r97/R97SN1/work",
       "TMPDIR": "/fast/scratch/hyaku/tameshi-r97/R97SN1/work",
       "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}

def git(*args, index=None):
    env = dict(ENV)
    if index:
        env["GIT_INDEX_FILE"] = index
    p = subprocess.run(["/usr/bin/git", "-C", CLONE] + list(args), capture_output=True, env=env)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args), p.stderr.decode()[:300]))
    return p.stdout

def commit_tree(mutate):
    """Build a new commit on top of FREEZE with a mutated tree. Returns new rev."""
    idx = tempfile.mktemp(dir="/fast/scratch/hyaku/tameshi-r97/R97SN1/work", prefix="idx-")
    git("read-tree", FREEZE, index=idx)
    mutate(idx)
    tree = git("write-tree", index=idx).decode().strip()
    os.unlink(idx)
    env = dict(ENV); env.update(GIT_AUTHOR_NAME="sn97", GIT_AUTHOR_EMAIL="sn97@invalid",
        GIT_COMMITTER_NAME="sn97", GIT_COMMITTER_EMAIL="sn97@invalid",
        GIT_AUTHOR_DATE="2026-11-08T00:00:00Z", GIT_COMMITTER_DATE="2026-11-08T00:00:00Z")
    p = subprocess.run(["/usr/bin/git", "-C", CLONE, "commit-tree", tree, "-p", FREEZE, "-m", "attack"],
                       capture_output=True, env=env)
    if p.returncode != 0:
        raise SystemExit("commit-tree failed: " + p.stderr.decode()[:300])
    return p.stdout.decode().strip()

def blob(text):
    p = subprocess.run(["/usr/bin/git", "-C", CLONE, "hash-object", "-w", "--stdin"], input=text.encode(),
                       capture_output=True, env=ENV)
    return p.stdout.decode().strip()

def remove_path(idx, path):
    git("update-index", "--force-remove", path, index=idx)

def add_blob(idx, path, text, mode="100644"):
    sha = blob(text)
    git("update-index", "--add", "--cacheinfo", "%s,%s,%s" % (mode, sha, path), index=idx)

def run(tool, rev, extra):
    env = dict(ENV); env["HYAKU_SCRATCH"] = "/fast/scratch/hyaku/tameshi-r97/R97SN1"
    cmd = ["python3", "-I", tool, "--lane", CLONE, "--rev", rev] + extra
    p = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout.strip(), p.stderr.strip()

TOOL_C1 = "/fast/scratch/hyaku/tameshi-r97/R97SN1/battery-bind.py"
TOOL_C2 = "/fast/scratch/hyaku/tameshi-r97/R97SN1/guard-inertia.py"

def show(tag, rc, out, err):
    print("---- %s ----" % tag)
    print("exit=%d" % rc)
    print(out)
    if err:
        print("STDERR:", err[:600])
    print()

# ---- A1: 49 receipts (one removed from the tree at R) ----
victim = None
names = git("ls-tree", "--name-only", "%s:%s" % (FREEZE, RCPT_DIR)).decode().split()
victim = names[0]
print("removing receipt:", victim)
rev49 = commit_tree(lambda idx: remove_path(idx, "%s/%s" % (RCPT_DIR, victim)))
show("A1 C1 with 49 receipts (removed %s, file still on disk) at rev %s" % (victim, rev49[:12]),
     *run(TOOL_C1, rev49, ["--driver-sha", DRIVER_SHA]))

# ---- A2: 51 receipts (extra .out naming no state) ----
rev51 = commit_tree(lambda idx: add_blob(idx, "%s/zz-extra-not-a-state.out" % RCPT_DIR, "exit=0\n"))
show("A2 C1 with 51 receipts (extra zz-extra-not-a-state.out) at rev %s" % rev51[:12],
     *run(TOOL_C1, rev51, ["--driver-sha", DRIVER_SHA]))

# ---- C1: manifest tamper (expect flipped) ----
man = json.loads(git("cat-file", "blob", "%s:%s" % (FREEZE, MANIFEST)).decode())
man2 = json.loads(json.dumps(man))
for r in man2["rows"]:
    if r["expect"] == "killed":
        r["expect"] = "limit"; break
revman = commit_tree(lambda idx: add_blob(idx, MANIFEST, json.dumps(man2, indent=1) + "\n"))
show("C1 C2 with tampered manifest (one killed->limit) at rev %s" % revman[:12],
     *run(TOOL_C2, revman, ["--checker-sha", CHECKER_SHA]))

# ---- C2: claims.json tampered (digests changed) ----
claims = json.loads(git("cat-file", "blob", "%s:.ufo/waves/round-97/claims.json" % FREEZE).decode())
claims["claims"]["C1"]["driver_sha256"] = "0"*64
claims["claims"]["C2"]["manifest_sha256"] = "1"*64
claims["claims"]["C2"]["checker_sha256"] = "2"*64
revclaims = commit_tree(lambda idx: add_blob(idx, ".ufo/waves/round-97/claims.json", json.dumps(claims, indent=1)+"\n"))
show("C2a C1 at rev with tampered claims.json, ORIGINAL driver-sha pin",
     *run(TOOL_C1, revclaims, ["--driver-sha", DRIVER_SHA]))
show("C2b C2 at rev with tampered claims.json, ORIGINAL checker-sha pin",
     *run(TOOL_C2, revclaims, ["--checker-sha", CHECKER_SHA]))

# ---- C3: manifest with unknown state ----
man3 = json.loads(json.dumps(man))
man3["rows"][0]["state"] = "no-such-state"
revstate = commit_tree(lambda idx: add_blob(idx, MANIFEST, json.dumps(man3, indent=1)+"\n"))
show("C3 C2 with manifest row state=no-such-state at rev %s" % revstate[:12],
     *run(TOOL_C2, revstate, ["--checker-sha", CHECKER_SHA]))

# ---- C4: manifest limit row with no limit_mechanism ----
man4 = json.loads(json.dumps(man))
for r in man4["rows"]:
    if r["expect"] == "limit":
        r.pop("limit_mechanism", None); break
revlim = commit_tree(lambda idx: add_blob(idx, MANIFEST, json.dumps(man4, indent=1)+"\n"))
show("C4 C2 with limit row lacking limit_mechanism at rev %s" % revlim[:12],
     *run(TOOL_C2, revlim, ["--checker-sha", CHECKER_SHA]))
