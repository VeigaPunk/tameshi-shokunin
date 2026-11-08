import hashlib, json, os, subprocess, tempfile
CLONE="/fast/scratch/hyaku/tameshi-r97/R97SN1/clone"
HEAD=subprocess.run(["/usr/bin/git","-C",CLONE,"rev-parse","HEAD"],capture_output=True).stdout.decode().strip()
BASE="07e50d6d0142b21e8443b5417b8edc4d1dd76455"
DRIVER_SHA="88bcca8651f6a60568c0b74346796b5ce3407a9b2c8ac70ca7f229102d3c0ff5"
CHECKER_SHA="02a5482a573193c37bd9ebfa9303e84284561f50326043967834c9fdbf0d1c80"
MANIFEST_SHA="9de0b7e9649e0e267d05489a9d14b4075424e16ae80a8a6b27ae34870fe094da"
RCPT=".ufo/evidence/round-96/pre-freeze/controls"; DRIVER=".ufo/evidence/round-96/c1/controls-v96.py"
COUNTER=".ufo/evidence/round-96/c1/measure-v96.py"; MANIFEST=".ufo/evidence/round-97/c2/guard-inertia.json"
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
def brief(t,rc,o,e):
    print("---- %s ----"%t); print("exit=%d"%rc)
    for ln in o.split("\n"):
        if ln.startswith("BATTERY ") or ln.startswith("BATTERY_SETUP") or ln.startswith("GUARD_INERTIA") or ln.startswith("GUARD_SETUP"): print(ln)
    rows=[l for l in o.split("\n") if l.startswith("BATTERY_ROW")]
    if rows: print("  rows:", rows[0], "| n=%d"%len(rows))
    if e: print("STDERR:",e[:300])
    print()

def read_rcpt(name): return git("cat-file","blob","%s:%s/%s"%(HEAD,RCPT,name)).decode()

# R1: counter_sha= edit on a NON-mutant receipt
r=read_rcpt("pos-real.out")
def m_cs(idx): put(idx,"%s/pos-real.out"%RCPT, r.replace("counter_sha=","counter_sha=0"*1) if False else r.split("counter_sha=")[0]+"counter_sha="+"0"*64+r.split("counter_sha=",1)[1])
rev_cs=commit_tree(m_cs)
brief("R1 C1 counter_sha= edit on pos-real.out (no mutant line)", *run(C1,rev_cs,["--driver-sha",DRIVER_SHA]))

# R2: exit= edit
def m_ex(idx): put(idx,"%s/pos-real.out"%RCPT, r.replace("exit=","exit=",1) if False else "\n".join(("exit=7" if l.startswith("exit=") else l) for l in r.split("\n")))
rev_ex=commit_tree(m_ex)
brief("R2 C1 exit= edit on pos-real.out", *run(C1,rev_ex,["--driver-sha",DRIVER_SHA]))

# R3: C1_R96_PASS=true payload edit on a __pass receipt (pos-real is __pass)
def m_pl(idx): put(idx,"%s/pos-real.out"%RCPT, r.replace("C1_R96_PASS=true","C1_R96_PASS=false"))
rev_pl=commit_tree(m_pl)
brief("R3 C1 payload edit C1_R96_PASS=true->false on pos-real.out", *run(C1,rev_pl,["--driver-sha",DRIVER_SHA]))

# R4: gitlink (mode 160000) receipt
def m_gl(idx):
    git("update-index","--force-remove","%s/pos-real.out"%RCPT,index=idx)
    put(idx,"%s/pos-real.out"%RCPT,"0"*40,"160000")
rev_gl=commit_tree(m_gl)
brief("R4 C1 receipt as GITLINK (160000)", *run(C1,rev_gl,["--driver-sha",DRIVER_SHA]))

# R5/R6: C2 edit-no-op and edit-ambiguous
man=json.loads(git("cat-file","blob","%s:%s"%(HEAD,MANIFEST)).decode())
m_noop=json.loads(json.dumps(man)); m_noop["rows"][0]["edit"]["new"]=m_noop["rows"][0]["edit"]["old"]
rev_noop=commit_tree(lambda idx: put(idx,MANIFEST,json.dumps(m_noop,indent=1)+"\n"))
brief("R5 C2 manifest edit.no-op", *run(C2,rev_noop,["--checker-sha",CHECKER_SHA]))
m_amb=json.loads(json.dumps(man)); m_amb["rows"][0]["edit"]["old"]="import"
rev_amb=commit_tree(lambda idx: put(idx,MANIFEST,json.dumps(m_amb,indent=1)+"\n"))
brief("R6 C2 manifest ambiguous anchor", *run(C2,rev_amb,["--checker-sha",CHECKER_SHA]))

# R7: base rev absence claims
p=subprocess.run(["/usr/bin/git","-C",CLONE,"grep","-c","GUARD_INERTIA",BASE],capture_output=True,text=True)
print("R7 git grep -c 'GUARD_INERTIA' at base: rc=%d out=%r"%(p.returncode,p.stdout))
p=subprocess.run(["/usr/bin/git","-C",CLONE,"grep","-c","BATTERY states=",BASE],capture_output=True,text=True)
print("R7b git grep -c 'BATTERY states=' at base: rc=%d out=%r"%(p.returncode,p.stdout))
p=subprocess.run(["/usr/bin/git","-C",CLONE,"cat-file","-e",BASE+":.ufo/evidence/round-96/pre-freeze/controls/C1-summary.txt"],capture_output=True)
print("R7c cat-file -e C1-summary.txt at 8ed9c526: rc=%d"%p.returncode)
