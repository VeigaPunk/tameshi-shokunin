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
def brief(t,rc,o,e):
    print("---- %s ----"%t); print("exit=%d"%rc)
    for ln in o.split("\n"):
        if ln.startswith("BATTERY ") or ln.startswith("BATTERY_SETUP"): print(ln)
    bad=[l for l in o.split("\n") if l.startswith("BATTERY_ROW")]
    if bad: print("  first rows:", bad[0], "| n_rows=%d"%len(bad))
    if e: print("STDERR:",e[:400])
    print()

names=git("ls-tree","--name-only","%s:%s"%(HEAD,RCPT)).decode().split()
counter_sha=hashlib.sha256(git("cat-file","blob","%s:%s"%(HEAD,COUNTER)).decode().encode()).hexdigest()

# F1: DRIVER SUBSTITUTION with pin OMITTED + receipts carrying correct counter_sha
fake=("EXPECT_EXTRA = {}\n"
 "def states(lane):\n"
 "    return {%s}\n"
 "def grade(name, code, out, want):\n"
 "    return True\n")%", ".join("'%s': {'expect': (0, {'__pass': True})}"%n[:-4] for n in names)
def m_drv(idx):
    put(idx,DRIVER,fake)
    for n in names: put(idx,"%s/%s"%(RCPT,n),"counter_sha=%s\nexit=0\nC1_R96_PASS=true\n"%counter_sha)
rev_drv=commit_tree(m_drv)
brief("F1 C1 FORGERY (substituted driver, grade() always True + forged receipts), --driver-sha OMITTED",
      *run(C1,rev_drv,[]))
brief("F1b same forgery WITH correct --driver-sha pin", *run(C1,rev_drv,["--driver-sha",DRIVER_SHA]))

# F2: symlink escaping the archive destination
def m_esc(idx):
    put(idx,"evil-link","/etc/passwd","120000")
rev_esc=commit_tree(m_esc)
brief("F2 C1 tree contains symlink -> /etc/passwd (archive extraction)", *run(C1,rev_esc,["--driver-sha",DRIVER_SHA]))

# F3: .gitattributes export-ignore on the NOTE the driver reads
def m_ign(idx):
    put(idx,".gitattributes","corpus/knowledge/mutation-case-fleet-sources-census.md export-ignore\n")
rev_ign=commit_tree(m_ign)
brief("F3 C1 .gitattributes export-ignore on the NOTE", *run(C1,rev_ign,["--driver-sha",DRIVER_SHA]))

# F4: .gitattributes export-subst on the NOTE with a $Format: marker
def m_sub(idx):
    put(idx,".gitattributes","corpus/knowledge/mutation-case-fleet-sources-census.md export-subst\n")
    note=git("cat-file","blob","%s:corpus/knowledge/mutation-case-fleet-sources-census.md"%HEAD).decode()
    put(idx,"corpus/knowledge/mutation-case-fleet-sources-census.md", note+"\n$Format:%%H$\n")
rev_sub=commit_tree(m_sub)
brief("F4 C1 .gitattributes export-subst on the NOTE", *run(C1,rev_sub,["--driver-sha",DRIVER_SHA]))

# F5: receipts path traversal / absolute
for arg in ["../../../etc", "/etc", RCPT+"/../../../../etc"]:
    brief("F5 C1 --receipts %r"%arg, *run(C1,HEAD,["--driver-sha",DRIVER_SHA,"--receipts",arg]))
