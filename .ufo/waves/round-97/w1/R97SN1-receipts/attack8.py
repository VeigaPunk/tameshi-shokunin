import hashlib, json, os, subprocess, tempfile
CLONE="/fast/scratch/hyaku/tameshi-r97/R97SN1/clone"
HEAD=subprocess.run(["/usr/bin/git","-C",CLONE,"rev-parse","HEAD"],capture_output=True).stdout.decode().strip()
DRIVER_SHA="88bcca8651f6a60568c0b74346796b5ce3407a9b2c8ac70ca7f229102d3c0ff5"
CHECKER_SHA="02a5482a573193c37bd9ebfa9303e84284561f50326043967834c9fdbf0d1c80"
MANIFEST_SHA="9de0b7e9649e0e267d05489a9d14b4075424e16ae80a8a6b27ae34870fe094da"
RCPT=".ufo/evidence/round-96/pre-freeze/controls"; COUNTER=".ufo/evidence/round-96/c1/measure-v96.py"
CHECKER=".ufo/evidence/round-96/conjunct-disposition-v96.py"; MANIFEST=".ufo/evidence/round-97/c2/guard-inertia.json"
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
    d=tempfile.mkdtemp(dir="/fast/scratch/hyaku/tameshi-r97/R97SN1/work",prefix="idx-"); idx=d+"/i"
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
    return p.returncode,p.stdout,p.stderr
C1="/fast/scratch/hyaku/tameshi-r97/R97SN1/head-battery-bind.py"
C2="/fast/scratch/hyaku/tameshi-r97/R97SN1/head-guard-inertia.py"
def raw(t,rc,o,e):
    print("### %s"%t); print("exit=%d"%rc)
    print("STDOUT: %r"%(o[:300]))
    if e: print("STDERR: %r"%e.strip().split(chr(10))[-1][:200])
    print()

# G1: COUNTER SUBSTITUTION at a new rev (driver stays pinned)
newc="#!/usr/bin/env python3\n# hostile counter\n"
newsha=hashlib.sha256(newc.encode()).hexdigest()
names=git("ls-tree","--name-only","%s:%s"%(HEAD,RCPT)).decode().split()
def m_cnt(idx):
    put(idx,COUNTER,newc)
    for n in names:
        b=git("cat-file","blob","%s:%s/%s"%(HEAD,RCPT,n)).decode()
        b="\n".join(("counter_sha="+newsha) if l.startswith("counter_sha=") else l for l in b.split("\n"))
        put(idx,"%s/%s"%(RCPT,n),b)
rev_c=commit_tree(m_cnt)
raw("G1 C1 COUNTER substituted at rev + all receipts' counter_sha rewritten (driver pin kept)",
    *run(C1,rev_c,["--driver-sha",DRIVER_SHA]))
# G1b: counter substituted, receipts untouched
def m_cnt2(idx): put(idx,COUNTER,newc)
rev_c2=commit_tree(m_cnt2)
raw("G1b C1 COUNTER substituted, receipts untouched", *run(C1,rev_c2,["--driver-sha",DRIVER_SHA]))

# G2: receipts DIR as a symlink at rev
def m_rdir(idx):
    git("update-index","--force-remove",RCPT,index=idx)
    git("update-index","--force-remove","%s/D01.out"%RCPT,index=idx)
    # add symlink entry for the dir path is not possible; instead point a receipt path at a symlink
    put(idx,"%s/pos-real.out"%RCPT,"elsewhere/x","120000")
rev_r=commit_tree(m_rdir)
raw("G2 C1 receipt pos-real.out is a SYMLINK (target string as body)", *run(C1,rev_r,["--driver-sha",DRIVER_SHA]))

# G3: C2 --checker / --manifest pointed at a symlink entry
def m_sym2(idx):
    put(idx,CHECKER,"/etc/passwd","120000")
rev_sy=commit_tree(m_sym2)
raw("G3 C2 --checker path is a SYMLINK entry (--checker-sha OMITTED)", *run(C2,rev_sy,[]))
raw("G3b C2 --checker path is a SYMLINK entry (--checker-sha PINNED)", *run(C2,rev_sy,["--checker-sha",CHECKER_SHA]))

# G4: replace-ref in the lane clone mapping the driver blob to a forged one
print("### G4 refs/replace present in the lane clone")
