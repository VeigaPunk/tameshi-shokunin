import hashlib, json, os, subprocess, tempfile
CLONE="/fast/scratch/hyaku/tameshi-r97/R97SN1/clone"
HEAD=subprocess.run(["/usr/bin/git","-C",CLONE,"rev-parse","HEAD"],capture_output=True).stdout.decode().strip()
DRIVER_SHA="88bcca8651f6a60568c0b74346796b5ce3407a9b2c8ac70ca7f229102d3c0ff5"
CHECKER_SHA="02a5482a573193c37bd9ebfa9303e84284561f50326043967834c9fdbf0d1c80"
MANIFEST_SHA="9de0b7e9649e0e267d05489a9d14b4075424e16ae80a8a6b27ae34870fe094da"
MANIFEST=".ufo/evidence/round-97/c2/guard-inertia.json"
ENV={"PATH":"/usr/local/bin:/usr/bin:/bin","HOME":"/fast/scratch/hyaku/tameshi-r97/R97SN1/work",
     "TMPDIR":"/fast/scratch/hyaku/tameshi-r97/R97SN1/work","HYAKU_SCRATCH":"/fast/scratch/hyaku/tameshi-r97/R97SN1",
     "GIT_NO_REPLACE_OBJECTS":"1","GIT_CONFIG_NOSYSTEM":"1","GIT_CONFIG_GLOBAL":"/dev/null"}
def git(*a,index=None):
    e=dict(ENV)
    if index: e["GIT_INDEX_FILE"]=index
    p=subprocess.run(["/usr/bin/git","-C",CLONE]+list(a),capture_output=True,env=e)
    if p.returncode!=0: raise SystemExit("git %s: %s"%(" ".join(a),p.stderr.decode()[:200]))
    return p.stdout
def commit_tree(mut,parent=HEAD):
    d=tempfile.mkdtemp(dir="/fast/scratch/hyaku/tameshi-r97/R97SN1/work",prefix="idx-"); idx=d+"/i"
    git("read-tree",parent,index=idx); mut(idx)
    tree=git("write-tree",index=idx).decode().strip()
    e=dict(ENV); e.update(GIT_AUTHOR_NAME="sn97",GIT_AUTHOR_EMAIL="sn97@invalid",GIT_COMMITTER_NAME="sn97",
        GIT_COMMITTER_EMAIL="sn97@invalid",GIT_AUTHOR_DATE="2026-11-08T00:00:00Z",GIT_COMMITTER_DATE="2026-11-08T00:00:00Z")
    p=subprocess.run(["/usr/bin/git","-C",CLONE,"commit-tree",tree,"-p",parent,"-m","attack"],capture_output=True,env=e)
    return p.stdout.decode().strip()
def blob(t): return subprocess.run(["/usr/bin/git","-C",CLONE,"hash-object","-w","--stdin"],input=t.encode(),capture_output=True,env=ENV).stdout.decode().strip()
def put(idx,path,text,mode="100644"): git("update-index","--add","--cacheinfo","%s,%s,%s"%(mode,blob(text),path),index=idx)
def run(tool,rev,extra,lane=CLONE,env=None):
    e=dict(ENV)
    if env: e.update(env)
    p=subprocess.run(["python3","-I",tool,"--lane",lane,"--rev",rev]+extra,capture_output=True,text=True,env=e)
    return p.returncode,p.stdout,p.stderr
C1="/fast/scratch/hyaku/tameshi-r97/R97SN1/head-battery-bind.py"
C2="/fast/scratch/hyaku/tameshi-r97/R97SN1/head-guard-inertia.py"
def raw(t,rc,o,e):
    print("### %s"%t); print("exit=%d"%rc)
    print("STDOUT: %r"%(o[:400]))
    if e: print("STDERR: %r"%(e.strip().split(chr(10))[-1][:200]))
    print()
man=json.loads(git("cat-file","blob","%s:%s"%(HEAD,MANIFEST)).decode())
# T3 empty rows
rev_e=commit_tree(lambda idx: put(idx,MANIFEST,json.dumps({"rows":[]})))
raw("T3 manifest rows=[] (--manifest-sha omitted)", *run(C2,rev_e,["--checker-sha",CHECKER_SHA]))
# T4 unknown state
m5=json.loads(json.dumps(man)); m5["rows"][0]["state"]="no-such-state"
rev_s=commit_tree(lambda idx: put(idx,MANIFEST,json.dumps(m5,indent=1)+"\n"))
raw("T4 manifest row state=no-such-state", *run(C2,rev_s,["--checker-sha",CHECKER_SHA]))
# T5 limit row without mechanism
m6=json.loads(json.dumps(man))
for r in m6["rows"]:
    if r["expect"]=="limit": r.pop("limit_mechanism",None); break
rev_l=commit_tree(lambda idx: put(idx,MANIFEST,json.dumps(m6,indent=1)+"\n"))
raw("T5 limit row without limit_mechanism", *run(C2,rev_l,["--checker-sha",CHECKER_SHA]))
# P7/P8 optional pins raw
raw("P7 C2 --manifest-sha OMITTED (pristine manifest)", *run(C2,HEAD,["--checker-sha",CHECKER_SHA]))
raw("P8 C2 --checker-sha OMITTED", *run(C2,HEAD,["--manifest-sha",MANIFEST_SHA]))
raw("P4 C1 --driver-sha OMITTED", *run(C1,HEAD,[]))
