#!/usr/bin/env python3
"""run one frozen/mutant counter and record wall, cpu, rc, receipts."""
import os, resource, shutil, subprocess, sys, time
S = "/fast/scratch/hyaku/tameshi-r55/T55W2MutC2"
name, counter, lane, rev = sys.argv[1:5]
w = os.path.join(S, "runs", name + ".work")
shutil.rmtree(w, ignore_errors=True); os.makedirs(w)
t0 = time.time()
with open(os.path.join(S, "runs", name + ".out"), "wb") as o, \
     open(os.path.join(S, "runs", name + ".err"), "wb") as e:
    p = subprocess.run([sys.executable, counter, "--lane", lane, "--rev", rev,
                        "--work", w, "--explain"], stdout=o, stderr=e)
wall = time.time() - t0
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
rec = os.path.join(w, "c2-receipts.json")
if os.path.exists(rec):
    shutil.copy(rec, os.path.join(S, "runs", name + ".receipts.json"))
line = "%s rc=%d wall=%.1fs cpu=%.1fs(maxrss_kb=%d)\n" % (
    name, p.returncode, wall, ru.ru_utime + ru.ru_stime, ru.ru_maxrss)
with open(os.path.join(S, "runs", "status.txt"), "a") as f:
    f.write(line)
print(line, end="")
