import json, os, shutil, subprocess, sys
LANE="/home/vgpnk/Projects/shokunin/tameshi-shokunin"
S="/fast/scratch/hyaku/tameshi-r55/T55W1Rev08"
BASE="0a2010acd1e92e4e332774050825e21bcfc7e079"
HEADING="## Round 55 - round-54 record corrections"
def sh(*a): return subprocess.run(a,capture_output=True,text=True)
body=open(os.path.join(LANE,"SCORECARD.md"),encoding="utf-8").read().splitlines()
out={};cur=None;buf=[]
for line in body:
    if line.startswith("**ER-R54-"):
        if cur: out[cur]="\n".join(buf).rstrip()+"\n"
        cur=line[2:line.index(" ")];buf=[line]
    elif cur: buf.append(line)
out[cur]="\n".join(buf).rstrip()+"\n"
POS=HEADING+"\n\n"+out["ER-R54-4"]+"\n"+out["ER-R54-10"]
STALE4=("\nThe round-54 c2 counter, as decided, is `49280fe5` for `c2/measure.py`.\n")
STALE10=("\nPhase-A `control/controls-a.stdout` prints `CTL_R53 ... 58/64, rekeyed=0/30`.\n")
def run(name, extra):
    d=os.path.join(S,name); shutil.rmtree(d,ignore_errors=True)
    assert sh("git","clone","--shared",LANE,d).returncode==0
    assert sh("git","-C",d,"checkout","--detach",BASE).returncode==0
    top=sh("git","-C",d,"rev-parse","--show-toplevel").stdout.strip()
    assert os.path.realpath(top)==os.path.realpath(d),(top,d)
    sc=os.path.join(d,"SCORECARD.md"); lines=open(sc,encoding="utf-8").read().splitlines()
    # insert the stale assertion BEFORE the corrections heading (outside the section)
    final="\n".join(lines)+extra+"\n"+POS
    open(sc,"w",encoding="utf-8").write(final)
    assert sh("git","-C",d,"add","SCORECARD.md").returncode==0
    assert sh("git","-C",d,"-c","user.name=fixture","-c","user.email=fixture@local","commit","-q","-m",name).returncode==0
    rev=sh("git","-C",d,"rev-parse","HEAD").stdout.strip()
    w=os.path.join(d,"_work");os.makedirs(w,exist_ok=True)
    cmd=[sys.executable,os.path.join(LANE,".ufo/evidence/round-55/c1/measure.py"),"--lane",d,"--rev",rev,"--work",w,"--explain"]
    r=sh(*cmd);txt=r.stdout+r.stderr
    open(os.path.join(S,"receipts",name+".stdout"),"w").write("$ "+" ".join(cmd)+"\n"+txt+"rc=%d\n"%r.returncode)
    print("###",name,"rev="+rev[:12])
    for ln in txt.splitlines():
        if ln.startswith(("EXPLAIN R54.4 ","EXPLAIN R54.10 ","C1_R55:")): print("   "+ln)
run("fix-stale4",STALE4)
run("fix-stale10",STALE10)
