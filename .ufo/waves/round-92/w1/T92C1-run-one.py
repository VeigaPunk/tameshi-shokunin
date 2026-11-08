#!/usr/bin/env python3
"""T92C1 one-off runner: executes a single named attempt from
T92C1-attack-driver.py's ATTEMPTS list (used for A12/A13 after the main
batch).  Usage: python3 T92C1-run-one.py <scratch> <w1-dir> <attempt-prefix>
"""
import importlib.util, os, sys

scratch, out, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
p = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-92/w1/T92C1-attack-driver.py"
spec = importlib.util.spec_from_file_location("drv", p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
counter = os.path.join(scratch, "measure-v92.py")
name, desc, fn = [a for a in m.ATTEMPTS if a[0].startswith(prefix)][0]
print(m.run_one(scratch, out, name, desc, fn, counter), flush=True)
