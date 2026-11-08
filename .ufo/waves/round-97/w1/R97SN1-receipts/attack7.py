import hashlib, json, os, subprocess, tempfile
CLONE="/fast/scratch/hyaku/tameshi-r97/R97SN1/clone"
HEAD=subprocess.run(["/usr/bin/git","-C",CLONE,"rev-parse","HEAD"],capture_output=True).stdout.decode().strip()
DRIVER_SHA="88bcca8651f6a60568c0b74346796b5ce3407a9b2c8ac70ca7f229102d3c0ff5"
CHECKER_SHA="02a5482a573193c37bd9ebfa9303e84284561f50326043967834c9fdbf0d1c80"
MANIFEST_SHA="9de0b7e9649e0e267d05489a9d14b4075424e16ae80a8a6b27ae34870fe094da"
NOTE="corpus/knowledge/mutation-case-fleet-sources-census.md"
ENV={"PATH":"/usr/local/bin:/usr/bin:/bin","HOME":"/fast/scratch/hyaku/tameshi-r97/R97SN1/work",
     "TMPDIR":"/fast/scratch/hyaku/tameshi-r97/R97SN1/work","HYAKU_SCRATCH":"/fast/scratch/hyaku/tameshi-r97/R97SN1",
     "GIT_NO_REPLACE_OBJECTS":"1","GIT_CONFIG_NOSYSTEM":"1","GIT_CONFIG_GLOBAL":"/dev/null"}
def git(*a,index=None):
    e=dict(ENV)
    if index: e["GIT_INDEX_FILE"]=index
    p=subprocess.run(["/usr/bin/git","-C",CLONE]+list(a),capture_output=True,env=e)
    if p.returncode!=0: raise SystemExit("git %s: %s"%(" ".join(a),p.stderr.decode()[:300]))
    return p.stdout
def commit_tree(mut,parent=HEAD):
    idx=tempfile.mkdtemp(dir="/fast/scratch/hyaku/tameshi-r97/R97SN1/work",prefix="idx-")+"/i"
    git("read-tree",parent,index=idx); mut(idx)
    tree=git("write-tree",index=idx).decode().strip()
    e=dict(ENV); e.update(GIT_AUTHOR_NAME="sn97",GIT_AUTHOR_EMAIL="sn97@invalid",GIT_COMMITTER_NAME="sn97",
        GIT_COMMITTER_EMAIL="sn97@invalid",GIT_AUTHOR_DATE="2026-11-08T00:00:00Z",GIT_COMMITTER_DATE="2026-11-08T00:00:00Z")
    p=subprocess.run(["/usr/bin/git","-C",CLONE,"commit-tree",tree,"-p",parent,"-m","attack"],capture_output=True,env=e)
    if p.returncode!=0: raise SystemExit("commit-tree: "+p.stderr.decode()[:300])
    return p.stdout.decode().strip()
def blob(t): return subprocess.run(["/usr/bin/git","-C",CLONE,"hash-object","-w","--stdin"],input=t.encode(),capture_output=True,env=ENV).stdout.decode().strip()
def put(idx,path,text,mode="100644"): git("update-index","--add","--cacheinfo","%s,%s,%s"%(mode,blob(text),path),index=idx)
def run(tool,rev,extra,lane=CLONE,env=None):
    e=dict(ENV)
    if env: e.update(env)
    p=subprocess.run(["python3","-I",tool,"--lane",lane,"--rev",rev]+extra,capture_output=True,text=True,env=e)
    return p.returncode,p.stdout.strip(),p.stderr.strip()
C1="/fast/scratch/hyaku/tameshi-r97/R97SN1/head-battery-bind.py"
C2="/fast/scratch/hyaku/tameshi-r97/R97SN1/head-guard-inertia.py"
def brief(t,rc,o,e):
    print("---- %s ----"%t); print("exit=%d  stdout_len=%d"%(rc,len(o)))
    for ln in o.split("\n"):
        if ln.startswith("BATTERY ") or ln.startswith("BATTERY_SETUP") or ln.startswith("GUARD_INERTIA") or ln.startswith("GUARD_SETUP"): print(ln)
    if e: print("STDERR(last 3):", " | ".join(e.strip().split("\n")[-3:])[:400])
    print()

# P-a: C2 with --lane pointing at a SUBDIR of the repo (toplevel differs)
brief("P-a C2 --lane = <repo>/.ufo (toplevel differs)", *run(C2,HEAD,["--checker-sha",CHECKER_SHA,"--manifest-sha",MANIFEST_SHA],lane=CLONE+"/.ufo"))
brief("P-b C1 --lane = <repo>/.ufo (toplevel differs)", *run(C1,HEAD,["--driver-sha",DRIVER_SHA],lane=CLONE+"/.ufo"))

# P-c: hostile NOTE that breaks the driver's 12-row premise
note=git("cat-file","blob","%s:%s"%(HEAD,NOTE)).decode()
rev_n=commit_tree(lambda idx: put(idx,NOTE,"garbage\n"))
brief("P-c C1 hostile NOTE (breaks fixture-premise)", *run(C1,rev_n,["--driver-sha",DRIVER_SHA]))

# P-d: hostile tree with absolute symlink -> unhandled exception?
rev_l=commit_tree(lambda idx: put(idx,"evil","/etc/passwd","120000"))
brief("P-d C1 hostile tree with absolute symlink", *run(C1,rev_l,["--driver-sha",DRIVER_SHA]))

# P-e: does C2's checker use the SHARED /fast/scratch/hyaku/tameshi-r96 (not HYAKU_SCRATCH)?
shared="/fast/scratch/hyaku/tameshi-r96"
before=set(os.listdir(shared)) if os.path.isdir(shared) else set()
priv="/fast/scratch/hyaku/tameshi-r97/R97SN1/priv2"
os.makedirs(priv,exist_ok=True)
rc,out,err=run(C2,HEAD,["--checker-sha",CHECKER_SHA,"--manifest-sha",MANIFEST_SHA],env={"HYAKU_SCRATCH":priv})
after=set(os.listdir(shared)) if os.path.isdir(shared) else set()
print("---- P-e C2 with HYAKU_SCRATCH=%s ----"%priv)
print("exit=%d"%rc)
print([l for l in out.split("\n") if l.startswith("GUARD_INERTIA")])
print("private HYAKU_SCRATCH tree:", sorted(os.listdir(priv)))
print("shared tameshi-r96 new entries:", sorted(after-before)[:8], "(n=%d)"%len(after-before))
print()
