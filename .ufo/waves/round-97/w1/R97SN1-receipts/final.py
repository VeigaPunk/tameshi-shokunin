import hashlib, json, os, re, subprocess, tempfile
CLONE="/fast/scratch/hyaku/tameshi-r97/R97SN1/clone"
HEAD=subprocess.run(["/usr/bin/git","-C",CLONE,"rev-parse","HEAD"],capture_output=True).stdout.decode().strip()
DRIVER_SHA="88bcca8651f6a60568c0b74346796b5ce3407a9b2c8ac70ca7f229102d3c0ff5"
CHECKER_SHA="02a5482a573193c37bd9ebfa9303e84284561f50326043967834c9fdbf0d1c80"
MANIFEST_SHA="9de0b7e9649e0e267d05489a9d14b4075424e16ae80a8a6b27ae34870fe094da"
RCPT=".ufo/evidence/round-96/pre-freeze/controls"; COUNTER=".ufo/evidence/round-96/c1/measure-v96.py"
MANIFEST=".ufo/evidence/round-97/c2/guard-inertia.json"
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
    print("STDOUT: %r"%(o[:260]))
    if e: print("STDERR: %r"%e.strip().split(chr(10))[-1][:160])
    print()
names=git("ls-tree","--name-only","%s:%s"%(HEAD,RCPT)).decode().split()
posreal=git("cat-file","blob","%s:%s/pos-real.out"%(HEAD,RCPT)).decode()

# V1: WELL-FORMED counter_sha edit (replace the 64 hex with zeros, same line shape)
def m_ok(idx):
    b=re.sub(r"^counter_sha=[0-9a-f]{64}$", "counter_sha="+"0"*64, posreal, flags=re.M)
    put(idx,"%s/pos-real.out"%RCPT,b)
raw("V1 C1 WELL-FORMED counter_sha= edit (pos-real, no mutant line)", *run(C1,commit_tree(m_ok),["--driver-sha",DRIVER_SHA]))
# V2: MALFORMED counter_sha line (value not 64 hex)
def m_bad(idx):
    b=re.sub(r"^counter_sha=[0-9a-f]{64}$", "counter_sha=nothex", posreal, flags=re.M)
    put(idx,"%s/pos-real.out"%RCPT,b)
raw("V2 C1 MALFORMED counter_sha= line (value not 64 hex)", *run(C1,commit_tree(m_bad),["--driver-sha",DRIVER_SHA]))
# V3: counter_sha line DELETED entirely
def m_del(idx):
    b="\n".join(l for l in posreal.split("\n") if not l.startswith("counter_sha="))
    put(idx,"%s/pos-real.out"%RCPT,b)
raw("V3 C1 counter_sha= line DELETED", *run(C1,commit_tree(m_del),["--driver-sha",DRIVER_SHA]))

# V4: forged counter WITH parse_note + receipts rewritten to its digest (driver pin intact)
realc=git("cat-file","blob","%s:%s"%(HEAD,COUNTER)).decode()
forgedc=realc+"\n# forged tail\n"
fsha=hashlib.sha256(forgedc.encode()).hexdigest()
def m_fc(idx):
    put(idx,COUNTER,forgedc)
    for n in names:
        b=git("cat-file","blob","%s:%s/%s"%(HEAD,RCPT,n)).decode()
        b="\n".join(("counter_sha="+fsha) if l.startswith("counter_sha=") else l for l in b.split("\n"))
        put(idx,"%s/%s"%(RCPT,n),b)
raw("V4 C1 forged COUNTER (parse_note present) + receipts rewritten to its digest, DRIVER PIN INTACT",
    *run(C1,commit_tree(m_fc),["--driver-sha",DRIVER_SHA]))

# V5: manifest tamper messages
man=json.loads(git("cat-file","blob","%s:%s"%(HEAD,MANIFEST)).decode())
m2=json.loads(json.dumps(man))
for r in m2["rows"]:
    if r["expect"]=="killed": r["expect"]="limit"; r["limit_mechanism"]="x"*50; break
rev_t=commit_tree(lambda idx: put(idx,MANIFEST,json.dumps(m2,indent=1)+"\n"))
raw("V5a C2 tampered manifest, ORIGINAL manifest-sha pin", *run(C2,rev_t,["--checker-sha",CHECKER_SHA,"--manifest-sha",MANIFEST_SHA]))
raw("V5b C2 tampered manifest, manifest-sha OMITTED", *run(C2,rev_t,["--checker-sha",CHECKER_SHA]))
