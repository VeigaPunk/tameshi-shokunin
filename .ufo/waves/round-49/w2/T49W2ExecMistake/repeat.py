import json, os, signal, subprocess, time
S="/fast/scratch/hyaku/tameshi-r49/T49W2ExecMistake"; CLONE=os.path.join(S,"clone")
SCRIPT=".ufo/evidence/round-49/deciding-run.sh"
FREEZE="14d03ea4270c6904064022b62b6faf467e5c0968"; REV="f181a961ae44061af486f600e5ea257d2baf78f8"
def run(tag, outdir, hc):
    env=dict(os.environ, HYAKU_SCRATCH=hc, TMPDIR=S)
    p=subprocess.Popen(["bash",SCRIPT,CLONE,REV,FREEZE,outdir],cwd=CLONE,stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,text=True,bufsize=1,start_new_session=True,env=env)
    pg=os.getpgid(p.pid); lines=[]; killed=None
    for line in p.stdout:
        lines.append(line.rstrip("\n"))
        if line.startswith("FROZEN_UNCHANGED"):
            os.killpg(pg, signal.SIGTERM); killed=line.rstrip("\n"); break
    rc=p.wait(timeout=60); rest=p.stdout.read()
    scr=os.path.join(hc,"tameshi-r49","deciding")
    r={"tag":tag,"rc":rc,"lines":lines,"killed":killed,"after":rest,
       "out":sorted(os.listdir(outdir)),"scr_exists":os.path.isdir(scr),
       "scr":sorted(os.listdir(scr)) if os.path.isdir(scr) else "ABSENT",
       "counter_artifacts":[f for f in os.listdir(outdir) if f.split(".")[0] in ("c1","c2")]}
    print(json.dumps(r, indent=1), flush=True); return r
r2=os.path.join(S,"out-c")          # same OUT left by case c: frozen.stdout only, no start receipt
r3=os.path.join(S,"out-c3"); os.makedirs(r3, exist_ok=True)
res=[run("c-repeat2-same-outdir", r2, os.path.join(S,"hc2")), run("c-repeat3-fresh-outdir", r3, os.path.join(S,"hc3"))]
json.dump(res, open(os.path.join(S,"repeat.json"),"w"), indent=1)
