import hashlib, json, subprocess, sys
lane, E = sys.argv[1], ".ufo/evidence/round-55"
env = {k: v for k, v in __import__("os").environ.items() if not k.startswith("GIT_")}
def blob(rev, path):
    r = subprocess.run(["git","-C",lane,"show","%s:%s"%(rev,path)],capture_output=True,env=env)
    return r.stdout if r.returncode==0 else None
for freeze in sys.argv[2:]:
    raw = blob(freeze, E+"/freeze.json")
    fr = json.loads(raw)
    bad=[]
    for rel,want in sorted(fr["files"].items()):
        path = rel if rel.startswith(".ufo/") else "%s/%s"%(E,rel)
        b = blob(freeze,path)
        if b is None: bad.append(rel+" unreadable"); continue
        got=hashlib.sha256(b).hexdigest()
        if got!=want: bad.append("%s %s != %s"%(rel,got[:12],want[:12]))
    print("GATE0 freeze=%s files=%d amendments=%d %s"%(freeze[:12],len(fr["files"]),len(fr.get("amendments") or []),"OK" if not bad else "MISMATCH "+"; ".join(bad)))
