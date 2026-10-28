#!/usr/bin/env python3
"""Classify every mutating file syscall in an `strace -f -y` log of the C2 counter.

Usage: parse-c2-write-audit.py STRACE WORK LANE

Classes: work (under --work), tmp (tool scratch with TMPDIR unset, by design),
dev (/dev/null etc.), bwrap-ns (private mount namespace: /newroot, /proc/<pid>,
/dev/stdin symlinks), lane (lane tree), HOST-OUTSIDE (anything else on the host).
Zero lane / HOST-OUTSIDE events is the audit's pass condition.
"""
import collections
import os
import re
import sys

strace_path, W, LANE = sys.argv[1], sys.argv[2].rstrip("/"), sys.argv[3].rstrip("/")
line_re = re.compile(r"^(\d+)\s+(\w+)\((.*)\)\s+=\s+(-?\d+|\?)")
q_re = re.compile(r'"((?:[^"\\]|\\.)*)"')
WRITE = ("O_WRONLY", "O_RDWR", "O_CREAT", "O_APPEND", "O_TRUNC")


def resolve(arg, cwd):
    if arg.startswith("AT_FDCWD<"):
        return arg[len("AT_FDCWD<"):-1]
    m = re.match(r"^-?\d+<([^>]*)>$", arg)
    return m.group(1) if m else cwd


def classify(path):
    p = os.path.normpath(path)
    if p == W or p.startswith(W + "/"):
        return "work"
    if p == "/tmp" or p.startswith("/tmp/"):
        return "tmp"
    if p == LANE or p.startswith(LANE + "/"):
        return "lane"
    if p == "/dev" or p.startswith("/dev/"):
        return "dev"
    if p.startswith("/proc/") or p == "/proc":
        return "bwrap-ns"
    if p.startswith("/newroot") or p in ("/stdin", "/stdout", "/stderr", "/fd", "/core", "/ptmx"):
        return "bwrap-ns"
    return "HOST-OUTSIDE"


cwd = {}
counts = collections.Counter()
examples = collections.defaultdict(list)

with open(strace_path, errors="replace") as fh:
    for line in fh:
        m = line_re.match(line.rstrip("\n"))
        if not m:
            continue
        pid, call, args, ret = m.groups()
        base = cwd.get(pid, LANE)
        if call in ("openat", "openat2"):
            mc = re.match(r"AT_FDCWD<([^>]*)>", args)
            if mc:  # every openat carries the true cwd; learn it for this pid
                cwd[pid] = base = mc.group(1)
            comma = args.find(",")
            dirfd = args[:comma].strip()
            rest = args[comma + 1:]
            mm = re.search(r'"(?:[^"\\]|\\.)*"', rest)
            if not mm:
                continue
            raw = mm.group(0)[1:-1]
            after = rest[mm.end():]
            parts = [x.strip() for x in after.split(",")]
            flags = parts[1] if len(parts) > 1 and parts[0] == "" else parts[0]
            if not any(w in flags for w in WRITE) or ret == "-1":
                continue
            b = resolve(dirfd, base)
            path = raw if raw.startswith("/") else os.path.join(b, raw)
        elif call == "chdir":
            mm = re.search(r'"(?:[^"\\]|\\.)*"', args)
            if not mm:
                continue
            path = mm.group(0)[1:-1]
            path = path if path.startswith("/") else os.path.join(base, path)
            if ret == "0":
                cwd[pid] = os.path.normpath(path)
            continue
        elif call in ("creat", "mkdir", "unlink", "rmdir"):
            mm = re.search(r'"(?:[^"\\]|\\.)*"', args)
            if not mm:
                continue
            path = mm.group(0)[1:-1]
            path = path if path.startswith("/") else os.path.join(base, path)
            if ret == "-1" and call in ("mkdir", "unlink", "rmdir"):
                continue
        elif call in ("rename", "link", "symlink"):
            qs = q_re.findall(args)
            if len(qs) < 2:
                continue
            path = qs[1]
            path = path if path.startswith("/") else os.path.join(base, path)
        elif call in ("renameat", "renameat2"):
            qs = q_re.findall(args)
            if len(qs) < 2:
                continue
            parts = args.split(",")
            d2 = parts[2].strip() if len(parts) >= 3 else ""
            b2 = resolve(d2, base) if d2 else base
            path = qs[1]
            path = path if path.startswith("/") else os.path.join(b2, path)
        elif call in ("unlinkat", "mkdirat", "linkat", "symlinkat"):
            qs = q_re.findall(args)
            if not qs:
                continue
            d = args[:args.find(",")].strip()
            b = resolve(d, base)
            path = qs[-1]
            path = path if path.startswith("/") else os.path.join(b, path)
        else:
            continue
        c = classify(path)
        counts[(call, c)] += 1
        if len(examples[(call, c)]) < 10:
            examples[(call, c)].append(os.path.normpath(path))

for k in sorted(counts):
    print("%-10s %-14s %d" % (k[0], k[1], counts[k]))
for kind in ("lane", "HOST-OUTSIDE"):
    total = sum(v for k, v in counts.items() if k[1] == kind)
    print("\n%s total: %d" % (kind, total))
    for k in sorted(examples):
        if k[1] == kind:
            for e in examples[k]:
                print("   %s %s" % (k[0], e))
