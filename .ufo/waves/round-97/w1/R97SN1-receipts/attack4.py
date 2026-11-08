import hashlib, json, os, subprocess, tempfile
CLONE="/fast/scratch/hyaku/tameshi-r97/R97SN1/clone"
HEAD=subprocess.run(["/usr/bin/git","-C",CLONE,"rev-parse","HEAD"],capture_output=True).stdout.decode().strip()
DRIVER_SHA="88bcca8651f6a60568c0b74346796b5ce3407a9b2c8ac70ca7f229102d3c0ff5"
RCPT=".ufo/evidence/round-96/pre-freeze/controls"; DRIVER=".ufo/evidence/round-96/c1/controls-v96.py"
COUNTER=".ufo/evidence/round-96/c1/measure-v96.py"
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
    idx=tempfile.mktemp(dir="/fast/scratch/hyaku/tameshi-r97/R97SN1/work",prefix="idx-")
    git("read-tree",parent,index=idx); mut(idx)
    tree=git("write-tree",index=idx).decode().strip(); os.unlink(idx)
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
def show(t,rc,o,e):
    print("---- %s ----"%t); print("exit=%d"%rc)
    for ln in o.split("\n"):
        if ln.startswith("BATTERY") or ln.startswith("GUARD_INERTIA"): print(ln)
    if e: print("STDERR:",e[:500])
    print()

names=git("ls-tree","--name-only","%s:%s"%(HEAD,RCPT)).decode().split()
counter_sha=hashlib.sha256(git("cat-file","blob","%s:%s"%(HEAD,COUNTER)).decode().encode()).hexdigest()

# S2: receipt as a TREE (directory) at rev
def m_tree(idx):
    git("update-index","--force-remove","%s/pos-real.out"%RCPT,index=idx)
    tb=subprocess.run(["/usr/bin/git","-C",CLONE,"mktree"],input=b"100644 blob %s\tinner.txt\n"%blob("x").encode(),capture_output=True,env=ENV).stdout.decode().strip()
    git("update-index","--add","--cacheinfo","040000,%s,%s"%(tb,"%s/pos-real.out"%RCPT),index=idx)
rev_tree=commit_tree(m_tree)
show("S2 C1 receipt pos-real.out replaced by TREE object", *run(C1,rev_tree,["--driver-sha",DRIVER_SHA]))

# S3: DRIVER SUBSTITUTION forgery with pin OMITTED
fake_driver=("EXPECT_EXTRA = {}\n"
 "def states(lane):\n"
 "    return {%s}\n"
 "def grade(name, code, out, want):\n"
 "    return True\n")%", ".join("'%s': {'expect': (0, {'__pass': True})}"%n[:-4] for n in names)
def m_drv(idx):
    put(idx,DRIVER,fake_driver)
    for n in names: put(idx,"%s/%s"%(RCPT,n),"exit=0\nC1_R96_PASS=true\n")
rev_drv=commit_tree(m_drv)
show("S3 C1 FORGERY: substituted driver (grade() always True) + forged receipts, --driver-sha OMITTED",
     *run(C1,rev_drv,[]))
show("S3b same forgery WITH correct --driver-sha pin", *run(C1,rev_drv,["--driver-sha",DRIVER_SHA]))

# S4: scratch failures at HEAD
open("/fast/scratch/hyaku/tameshi-r97/R97SN1/notadir2","w").close()
show("S4a C1 HYAKU_SCRATCH=file",*run(C1,HEAD,["--driver-sha",DRIVER_SHA],
     env={"HYAKU_SCRATCH":"/fast/scratch/hyaku/tameshi-r97/R97SN1/notadir2"}))
os.makedirs("/fast/scratch/hyaku/tameshi-r97/R97SN1/ro2",exist_ok=True); os.chmod("/fast/scratch/hyaku/tameshi-r97/R97SN1/ro2",0o555)
show("S4b C1 HYAKU_SCRATCH=read-only dir",*run(C1,HEAD,["--driver-sha",DRIVER_SHA],
     env={"HYAKU_SCRATCH":"/fast/scratch/hyaku/tameshi-r97/R97SN1/ro2"}))
show("S4c C2 HYAKU_SCRATCH=file",*run(C2,HEAD,["--checker-sha","02a5482a573193c37bd9ebfa9303e84284561f50326043967834c9fdbf0d1c80"],
     env={"HYAKU_SCRATCH":"/fast/scratch/hyaku/tameshi-r97/R97SN1/notadir2"}))
os.chmod("/fast/scratch/hyaku/tameshi-r97/R97SN1/ro2",0o755)
