#!/usr/bin/env python3
import os, subprocess, sys
real = '/usr/bin/git'
a = sys.argv[1:]
if 'commit' in a:
    if '-C' not in a: raise SystemExit('GUARD: commit without -C')
    root = a[a.index('-C')+1]
    top = subprocess.check_output([real, '-C', root, 'rev-parse', '--show-toplevel'], text=True).strip()
    if os.path.realpath(top) != os.path.realpath(root): raise SystemExit('GUARD: misroot')
    if not os.path.realpath(root).startswith('/fast/scratch/hyaku/tameshi-r78/T78W1M1' + os.sep): raise SystemExit('GUARD: outside scratch')
os.execv(real, [real, '-c', 'commit.gpgsign=false'] + a)
