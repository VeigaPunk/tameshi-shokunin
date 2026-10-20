#!/usr/bin/env python3
"""GateSecurity r12 evidence probes (lane-internal, advisory).

Stdlib behaviours a naive tools/repeat-control.py would inherit. Does NOT
import or run tools/repeat-control.py; every probe is a hermetic fixture
under a fresh mktemp dir. Each probe prints one line: PROBE <id> <observed>.
"""
import argparse
import filecmp
import json
import os
import subprocess
import sys
import tempfile
import time

PY = sys.executable
T = tempfile.mkdtemp(prefix="tameshi-r12-gatesec.")


def out(pid, msg):
    print(f"PROBE {pid} {msg}", flush=True)


def rc(argv, **kw):
    return subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True, **kw)


# P1 argparse default exits collide with the gate exit map (2 = could-not-evaluate, 0 = clean)
p = rc([PY, "-c", "import argparse;a=argparse.ArgumentParser();a.add_argument('--runs',type=int);a.parse_args(['--runs','x'])"])
out("P1a", f"argparse-type-error exit={p.returncode} (contract usage=64)")
p = rc([PY, "-c", "import argparse;a=argparse.ArgumentParser();a.parse_args(['--help'])"])
out("P1b", f"argparse --help exit={p.returncode} (same as controls_match=0)")
p = rc([PY, "-c", "import argparse;a=argparse.ArgumentParser();a.add_argument('--runs');a.parse_args(['--ru','3']);print('abbrev-accepted')"])
out("P1c", f"argparse prefix '--ru' -> {p.stdout.decode().strip() or p.returncode}")

# P2 '--' / REMAINDER handling on this interpreter
a = argparse.ArgumentParser()
a.add_argument("--runs")
a.add_argument("--out")
a.add_argument("cmd", nargs=argparse.REMAINDER)
for v in (["--runs", "3", "--out", "d", "--", "echo", "--out", "x"],
          ["--runs", "3", "--out", "d", "echo", "--runs", "9"],
          ["--runs", "3", "--out", "d", "--", "--", "x"]):
    try:
        ns = a.parse_args(v)
        out("P2", f"argv={v!r} -> runs={ns.runs} out={ns.out} cmd={ns.cmd!r}")
    except SystemExit as e:
        out("P2", f"argv={v!r} -> SystemExit {e.code}")

# P3 int() leniency for --runs
for s in ("3", " 3 ", "+3", "3_0", "\u0663", "03"):
    out("P3", f"int({s!r})={int(s)}")

# P4 uncaught exception / KeyboardInterrupt exit statuses
p = rc([PY, "-c", "raise FileNotFoundError('x')"])
out("P4a", f"uncaught exception exit={p.returncode} (same as controls_mismatch=1)")
p = rc([PY, "-c", "import json;json.loads('{')"])
out("P4b", f"uncaught json error exit={p.returncode}")
p = rc([PY, "-c", "raise KeyboardInterrupt"])
out("P4c", f"uncaught KeyboardInterrupt returncode={p.returncode} (shell sees 128+2)")

# P5 exec failure taxonomy with shell=False
noexec = os.path.join(T, "noexec.sh")
with open(noexec, "w") as f:
    f.write("echo hi\n")
os.chmod(noexec, 0o644)
noshebang = os.path.join(T, "noshebang")
with open(noshebang, "w") as f:
    f.write("echo hi\n")
os.chmod(noshebang, 0o755)
for label, argv in (("missing", ["tameshi-no-such-cmd-r12"]),
                    ("not-exec", [noexec]),
                    ("no-shebang", [noshebang]),
                    ("directory", [T]),
                    ("empty-argv0", [""])):
    try:
        p = rc(argv)
        out("P5", f"{label}: ran exit={p.returncode}")
    except OSError as e:
        out("P5", f"{label}: {type(e).__name__} errno={e.errno}")
p = rc(["env", "tameshi-no-such-cmd-r12"])
out("P5w", f"wrapped missing (env X) exit={p.returncode} -> nonzero baseline, not exec error")

# P5m command disappears mid-series (self-deleting script)
selfdel = os.path.join(T, "selfdel.sh")
with open(selfdel, "w") as f:
    f.write("#!/bin/sh\necho ok\nrm -f \"$0\"\n")
os.chmod(selfdel, 0o755)
seq = []
for i in range(3):
    try:
        seq.append(rc([selfdel]).returncode)
    except OSError as e:
        seq.append(type(e).__name__)
out("P5m", f"self-deleting command runs={seq}")

# P6 signal death
p = rc(["sh", "-c", "kill -9 $$"])
out("P6", f"SIGKILL child returncode={p.returncode} (negative; shell form would be 137)")

# P7 grandchild holding the pipe defeats capture_output and timeout
t0 = time.monotonic()
p = rc(["sh", "-c", "sleep 4 & echo hi"])
out("P7a", f"child exits at once, run() returned after {time.monotonic()-t0:.1f}s stdout={p.stdout!r}")
t0 = time.monotonic()
try:
    rc(["sh", "-c", "sleep 4 & sleep 60"], timeout=1)
except subprocess.TimeoutExpired:
    pass
out("P7b", f"timeout=1 with grandchild on pipe -> raised after {time.monotonic()-t0:.1f}s")

# P8 grandchild writes into evidence file after run 'completed' (file redirect, no group kill)
ev = os.path.join(T, "run-1.stdout")
with open(ev, "wb") as f:
    subprocess.run(["sh", "-c", "echo hi; (sleep 1; echo late) &"], stdin=subprocess.DEVNULL, stdout=f)
b1 = open(ev, "rb").read()
time.sleep(1.5)
b2 = open(ev, "rb").read()
out("P8", f"bytes at run end={b1!r} bytes 1.5s later={b2!r}")

# P9 filecmp.cmp default shallow=True false-match
x, y = os.path.join(T, "a"), os.path.join(T, "b")
open(x, "wb").write(b"AAAA")
open(y, "wb").write(b"BBBB")
os.utime(x, (1, 1))
os.utime(y, (1, 1))
out("P9", f"filecmp.cmp(shallow default) on different bytes same size+mtime -> {filecmp.cmp(x, y)}; shallow=False -> {filecmp.cmp(x, y, shallow=False)}")

# P10 pre-existing --out with planted symlink
victim = os.path.join(T, "victim.txt")
open(victim, "w").write("precious\n")
od = os.path.join(T, "out")
os.mkdir(od)
os.symlink(victim, os.path.join(od, "run-1.stdout"))
with open(os.path.join(od, "run-1.stdout"), "wb") as f:
    f.write(b"gate bytes\n")
out("P10a", f"open('wb') via planted symlink -> victim now {open(victim).read()!r}")
open(victim, "w").write("precious\n")
try:
    open(os.path.join(od, "run-1.stdout"), "xb")
    out("P10b", "open('xb') followed symlink")
except FileExistsError:
    out("P10b", "open('xb') refused planted symlink (FileExistsError)")
try:
    os.mkdir(od)
except FileExistsError:
    out("P10c", "os.mkdir(existing --out) -> FileExistsError (refusal available without rmtree)")
stale = os.path.join(T, "stale")
os.mkdir(stale)
for n in ("run-4.stdout", "verdict.json"):
    open(os.path.join(stale, n), "w").write("old\n")
out("P10d", f"reused --out keeps stale entries {sorted(os.listdir(stale))} beside a new --runs 3 set")

# P11 --out inside the observed tree: self-induced mismatch on a pristine, deterministic command
w = os.path.join(T, "repo")
os.mkdir(w)
open(os.path.join(w, "f.txt"), "w").write("x\n")
od = os.path.join(w, "ev")
os.mkdir(od)
outs = []
for i in range(1, 4):
    with open(os.path.join(od, f"run-{i}.stdout"), "wb") as so:
        subprocess.run(["find", ".", "-type", "f"], cwd=w, stdin=subprocess.DEVNULL, stdout=so)
    outs.append(open(os.path.join(od, f"run-{i}.stdout"), "rb").read())
out("P11", f"find over cwd with --out inside cwd: distinct stdout across 3 runs = {len(set(outs))} (1 means match)")

# P12 argv vs shell string
argv = ["printf", "%s|", "a b", "$HOME", "*"]
p1 = rc(argv)
p2 = rc(" ".join(argv), shell=True)
out("P12", f"argv={p1.stdout!r} joined+shell={p2.stdout[:60]!r}")

# P13 snapshot manifest path handling
for name in ("/etc/hostname", "../outside", "run-1.stdout/../../x"):
    out("P13", f"os.path.join('SNAP',{name!r}) -> {os.path.normpath(os.path.join('SNAP', name))!r}")
snap = os.path.join(T, "snap")
os.mkdir(snap)
os.symlink("/etc/hostname", os.path.join(snap, "run-1.stdout"))
out("P13s", f"git-committable symlink in snapshot: islink={os.path.islink(os.path.join(snap,'run-1.stdout'))} open() follows -> reads outside DIR")

# P14 self-consistent manifest edit is undetectable without an external anchor
import hashlib
d = os.path.join(T, "snap2")
os.mkdir(d)
open(os.path.join(d, "run-1.stdout"), "wb").write(b"original\n")
man = {"files": {"run-1.stdout": hashlib.sha256(b"original\n").hexdigest()}, "expected": {"id": "controls_match", "exit": 0}}
open(os.path.join(d, "run-1.stdout"), "wb").write(b"edited\n")
man["files"]["run-1.stdout"] = hashlib.sha256(b"edited\n").hexdigest()
ok = all(hashlib.sha256(open(os.path.join(d, k), "rb").read()).hexdigest() == v for k, v in man["files"].items())
out("P14", f"file+manifest co-edited: in-dir digest check passes={ok}")

out("DONE", f"scratch={T}")
