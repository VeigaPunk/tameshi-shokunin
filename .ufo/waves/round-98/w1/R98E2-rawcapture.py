#!/usr/bin/env python3
"""R98E2 raw capture: re-run the frozen tool CLI at the fixture commits the hand
drive created, writing exact stdout/stderr/exit per class to a receipt file."""
import hashlib
import os
import shutil
import subprocess
import sys

BASE = "/fast/scratch/hyaku/tameshi-r98/R98E2/hand"
OUT = "/fast/scratch/hyaku/tameshi-r98/R98E2"
CLONE = os.path.join(BASE, "clone")
TOOL = os.path.join(BASE, "tool.py")
MAN_REL = ".ufo/evidence/round-97/c2/guard-inertia.json"
REV = "764aca97e513d650949999362cd4b0f5f0e566a5"

CASES = [
    ("edit-no-op", "9e9cd3914e47a973d13ce5e44d423a2ec755169b",
     "6cba53e0b1e3a8d2e13c722e21e3bc8e43279b7002c65787964182aa20300942"),
    ("edit-ambiguous", "dc98d1e1f01117256d257b00daf5f997118c2e5f",
     "5b61030fc7ceecc635e1b6effebea1d70499aa0e59a251fc5032b981dd918964"),
    ("state-unbuildable", "e766f7a62cea11beaef1cb32793975e230d800c3",
     "cd0e0d3cf146733fdf39cbd1b7b72bff2c60ad4e5f5332ec3d568988bf6339e5"),
    ("limit-mechanism-missing", "5220232e4dd59678428b14d5b28a1476c7fc0175",
     "5de816b4eeab9df253d1c21e90b3d329d6c5547fa996120e2fb1c4ece1f6c389"),
    ("manifest-sha-mismatch", "febbc5cd6283b265afdbbcc23321d7e3767dcac2",
     "65852017f81726a68ca7cb2dee9862b4b1cf638b339f1ef04c3222b8476e3010"),
    ("manifest-empty", "4b7ee8c81040b8110075e3aad627024dbf70d5a5",
     "507110f675a8cba5fabff93049a3fbffdb74339b20050b2f02c10172fd993149"),
    ("positive", REV,
     "9de0b7e9649e0e267d05489a9d14b4075424e16ae80a8a6b27ae34870fe094da"),
    ("attack-unused-field", "2d201717d25c126a28722f545e63748a9fadab0f",
     "76a1bd8a3657bc1aa78c7c2f67f351c48316d9faf37d2572135db340101edf9e"),
    ("attack-echoed-field", "03a40ad35164822a1e613e8ab511ebcee42a7cd2",
     "d7e807de9c03b4caf5ccc44be0169562daf80aa5f8c5c530d2a7e21ab9887698"),
]

env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
       "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
       "GIT_CONFIG_GLOBAL": "/dev/null"}

for name, rev, sha in CASES:
    scratch = os.path.join(BASE, "raw-scratch-" + name)
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch)
    e = dict(env)
    e.update({"HOME": scratch, "TMPDIR": scratch, "HYAKU_SCRATCH": scratch})
    p = subprocess.run([sys.executable, "-I", TOOL, "--lane", CLONE, "--rev", rev,
                        "--manifest", MAN_REL, "--manifest-sha", sha],
                       capture_output=True, text=True, env=e)
    path = os.path.join(OUT, "R98E2-hand-" + name + ".out")
    with open(path, "w") as f:
        f.write(p.stdout)
        if p.stderr:
            f.write("[stderr] " + p.stderr)
    print("%s rev=%s rc=%d sha_stdout=%s lines=%d" % (
        name, rev, p.returncode,
        hashlib.sha256(p.stdout.encode()).hexdigest()[:16],
        len(p.stdout.splitlines())))
