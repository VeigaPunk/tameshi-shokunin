import hashlib, json, os, subprocess, tempfile

CLONE = "/fast/scratch/hyaku/tameshi-r97/R97SN1/clone"
HEAD = subprocess.run(["/usr/bin/git","-C",CLONE,"rev-parse","HEAD"],capture_output=True).stdout.decode().strip()
DRIVER_SHA = "88bcca8651f6a60568c0b74346796b5ce3407a9b2c8ac70ca7f229102d3c0ff5"
CHECKER_SHA = "02a5482a573193c37bd9ebfa9303e84284561f50326043967834c9fdbf0d1c80"
MANIFEST_SHA = "9de0b7e9649e0e267d05489a9d14b4075424e16ae80a8a6b27ae34870fe094da"
RCPT_DIR = ".ufo/evidence/round-96/pre-freeze/controls"
MANIFEST = ".ufo/evidence/round-97/c2/guard-inertia.json"
ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "/fast/scratch/hyaku/tameshi-r97/R97SN1/work",
       "TMPDIR": "/fast/scratch/hyaku/tameshi-r97/R97SN1/work", "HYAKU_SCRATCH": "/fast/scratch/hyaku/tameshi-r97/R97SN1",
       "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}

def git(*args, index=None):
    env = dict(ENV)
    if index: env["GIT_INDEX_FILE"] = index
    p = subprocess.run(["/usr/bin/git","-C",CLONE]+list(args), capture_output=True, env=env)
    if p.returncode != 0: raise SystemExit("git %s: %s" % (" ".join(args), p.stderr.decode()[:300]))
    return p.stdout

def commit_tree(mutate, parent=HEAD):
    idx = tempfile.mktemp(dir="/fast/scratch/hyaku/tameshi-r97/R97SN1/work", prefix="idx-")
    git("read-tree", parent, index=idx); mutate(idx)
    tree = git("write-tree", index=idx).decode().strip(); os.unlink(idx)
    env = dict(ENV); env.update(GIT_AUTHOR_NAME="sn97", GIT_AUTHOR_EMAIL="sn97@invalid",
        GIT_COMMITTER_NAME="sn97", GIT_COMMITTER_EMAIL="sn97@invalid",
        GIT_AUTHOR_DATE="2026-11-08T00:00:00Z", GIT_COMMITTER_DATE="2026-11-08T00:00:00Z")
    p = subprocess.run(["/usr/bin/git","-C",CLONE,"commit-tree",tree,"-p",parent,"-m","attack"],
                       capture_output=True, env=env)
    if p.returncode != 0: raise SystemExit("commit-tree: "+p.stderr.decode()[:300])
    return p.stdout.decode().strip()

def blob(text):
    return subprocess.run(["/usr/bin/git","-C",CLONE,"hash-object","-w","--stdin"],input=text.encode(),
                          capture_output=True,env=ENV).stdout.decode().strip()
def add_blob(idx, path, text, mode="100644"):
    git("update-index","--add","--cacheinfo","%s,%s,%s"%(mode,blob(text),path), index=idx)

def run(tool, rev, extra, lane=CLONE):
    env = dict(ENV)
    p = subprocess.run(["python3","-I",tool,"--lane",lane,"--rev",rev]+extra, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout.strip(), p.stderr.strip()

C1 = "/fast/scratch/hyaku/tameshi-r97/R97SN1/head-battery-bind.py"
C2 = "/fast/scratch/hyaku/tameshi-r97/R97SN1/head-guard-inertia.py"

def show(tag, rc, out, err):
    print("---- %s ----" % tag); print("exit=%d" % rc)
    for ln in out.split("\n"):
        if ln.startswith("GUARD_INERTIA") or ln.startswith("BATTERY "): print(ln)
    if err: print("STDERR:", err[:400])
    print()

print("HEAD rev:", HEAD)
show("B0 C1 baseline @HEAD", *run(C1, HEAD, ["--driver-sha", DRIVER_SHA]))
show("B0b C2 baseline @HEAD", *run(C2, HEAD, ["--checker-sha", CHECKER_SHA, "--manifest-sha", MANIFEST_SHA]))

# empty pins
show("P1 C1 --driver-sha ''", *run(C1, HEAD, ["--driver-sha", ""]))
show("P2 C1 --driver-sha 'zz'", *run(C1, HEAD, ["--driver-sha", "zz"]))
show("P3 C1 --driver-sha wrong64", *run(C1, HEAD, ["--driver-sha", "0"*64]))
show("P4 C1 --driver-sha OMITTED", *run(C1, HEAD, []))
show("P5 C2 --manifest-sha ''", *run(C2, HEAD, ["--checker-sha", CHECKER_SHA, "--manifest-sha", ""]))
show("P6 C2 --manifest-sha wrong", *run(C2, HEAD, ["--checker-sha", CHECKER_SHA, "--manifest-sha", "0"*64]))
show("P7 C2 --manifest-sha OMITTED", *run(C2, HEAD, ["--checker-sha", CHECKER_SHA]))
show("P8 C2 --checker-sha OMITTED", *run(C2, HEAD, ["--manifest-sha", MANIFEST_SHA]))

# manifest tamper at new rev, WITH the correct original manifest-sha pin
man = json.loads(git("cat-file","blob","%s:%s"%(HEAD,MANIFEST)).decode())
m2 = json.loads(json.dumps(man))
for r in m2["rows"]:
    if r["expect"]=="killed": r["expect"]="limit"; break
rev_t = commit_tree(lambda idx: add_blob(idx, MANIFEST, json.dumps(m2, indent=1)+"\n"))
show("T1 C2 tampered manifest @newrev, ORIGINAL manifest-sha pin",
     *run(C2, rev_t, ["--checker-sha", CHECKER_SHA, "--manifest-sha", MANIFEST_SHA]))
show("T1b C2 tampered manifest @newrev, manifest-sha = digest of TAMPERED manifest",
     *run(C2, rev_t, ["--checker-sha", CHECKER_SHA, "--manifest-sha", hashlib.sha256((json.dumps(m2,indent=1)+"\n").encode()).hexdigest()]))
show("T1c C2 tampered manifest @newrev, manifest-sha OMITTED",
     *run(C2, rev_t, ["--checker-sha", CHECKER_SHA]))

# coherent substitute manifest: same rows semantics but different bytes (reordered)
m3 = json.loads(json.dumps(man)); m3["rows"] = list(reversed(m3["rows"]))
m3b = json.dumps(m3, indent=1)+"\n"
rev_c = commit_tree(lambda idx: add_blob(idx, MANIFEST, m3b))
show("T2 C2 coherent substitute manifest (rows reordered) @newrev, manifest-sha = ITS digest",
     *run(C2, rev_c, ["--checker-sha", CHECKER_SHA, "--manifest-sha", hashlib.sha256(m3b.encode()).hexdigest()]))

# manifest with no rows
m4 = {"rows": []}
rev_e = commit_tree(lambda idx: add_blob(idx, MANIFEST, json.dumps(m4)))
show("T3 C2 manifest with empty rows @newrev", *run(C2, rev_e, ["--checker-sha", CHECKER_SHA]))

# unknown state
m5 = json.loads(json.dumps(man)); m5["rows"][0]["state"]="no-such-state"
rev_s = commit_tree(lambda idx: add_blob(idx, MANIFEST, json.dumps(m5,indent=1)+"\n"))
show("T4 C2 manifest row state=no-such-state @newrev", *run(C2, rev_s, ["--checker-sha", CHECKER_SHA]))

# limit row missing mechanism
m6 = json.loads(json.dumps(man))
for r in m6["rows"]:
    if r["expect"]=="limit": r.pop("limit_mechanism",None); break
rev_l = commit_tree(lambda idx: add_blob(idx, MANIFEST, json.dumps(m6,indent=1)+"\n"))
show("T5 C2 limit row without limit_mechanism @newrev", *run(C2, rev_l, ["--checker-sha", CHECKER_SHA]))
