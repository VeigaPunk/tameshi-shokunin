import json, re, subprocess, sys
lane, rev, wave = sys.argv[1], sys.argv[2], sys.argv[3]
out = subprocess.run(["git","-C",lane,"ls-tree","-r","--name-only",rev,"--",".ufo/waves/round-54/"+wave],capture_output=True,text=True,check=True).stdout.split()
names = [n for n in out if re.search(r"/T54W\d+[A-Za-z]*Read\d+\.json$", n)]
total = 0; sec = 0
for n in sorted(names):
    d = json.loads(subprocess.run(["git","-C",lane,"show",rev+":"+n],capture_output=True,text=True,check=True).stdout)
    k = len(d.get("findings") or [])
    total += k; sec += 1 if k else 0
    print("%s findings=%d" % (n.rsplit("/",1)[-1], k))
print("%s: reader_files=%d findings=%d sections_with_findings=%d" % (wave, len(names), total, sec))
