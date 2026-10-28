#!/usr/bin/env python3
"""Positive control fixture for the C2 `tmp_mkdirs` arm.

A tool that regains the round-53 `dir="/tmp"` fallback allocates its scratch
through `os.mkdir`/`os.makedirs`, which is the plain `mkdir(2)` syscall on
Linux. This fixture does exactly that one thing and nothing else, so a strace
log of it MUST register under any census that really counts "/tmp" allocations.

usage: probe-mkdir-tmp.py [/tmp/<unique-name>]
"""
import os
import sys

target = sys.argv[1] if len(sys.argv) > 1 else '/tmp/T54W2Exec02-probe'
os.makedirs(target)
print('created', target)
