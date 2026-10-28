#!/usr/bin/env python3
"""Second pass: resolve every mkdir/mkdirat path against each pid's cwd.

Traces mkdir, mkdirat, chdir, fchdir (with -y so numeric dirfds print as
N</resolved/path>).  Every pid starts with the traced process's cwd (the
clone); `chdir` updates that pid's cwd, so a relative mkdir path is resolved
the way the kernel resolved it.  A pid that reached its cwd through
`fchdir(fd)` is marked unresolved instead of guessed.

Usage: driver2.py CLONE OUTDIR TOOL [TOOL...]   (TOOL is an index into the
counter's TOOLS list, or "all")
"""
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

LINE = re.compile(r'^\s*(\d+)\s+([a-z0-9_]+)\((.*)\)\s+=\s+(-?\d+)')
STR = re.compile(r'"((?:[^"\\]|\\.)*)"')
FD = re.compile(r'^(\d+)<([^>]*)>')

def load_tools(clone):
    p = Path(clone) / '.ufo' / 'evidence' / 'round-54' / 'c2' / 'measure.py'
    spec = importlib.util.spec_from_file_location('c2measure', str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.TOOLS

def parse_arg_list(rest):
    """split top-level args on commas outside quotes/brackets"""
    out, buf, depth, q = [], [], 0, False
    i = 0
    while i < len(rest):
        c = rest[i]
        if q:
            buf.append(c)
            if c == '\\' and i + 1 < len(rest):
                buf.append(rest[i + 1]); i += 2; continue
            if c == '"':
                q = False
            i += 1
            continue
        if c == '"':
            q = True; buf.append(c); i += 1; continue
        if c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
        if c == ',' and depth == 0:
            out.append(''.join(buf).strip()); buf = []; i += 1; continue
        buf.append(c); i += 1
    if buf:
        out.append(''.join(buf).strip())
    return out

def resolve(cwd, path):
    if path.startswith('/'):
        return path
    if cwd is None:
        return None
    return os.path.normpath(os.path.join(cwd, path))

def track(log_text, clone):
    cwd = {}
    rows = []
    unresolved = []
    for line in log_text.splitlines():
        m = LINE.match(line)
        if not m:
            continue
        pid, call, rest, ret = m.group(1), m.group(2), m.group(3), m.group(4)
        args = parse_arg_list(rest)
        if call == 'chdir':
            p = STR.search(args[0]).group(1) if STR.search(args[0]) else ''
            cwd[pid] = resolve(cwd.get(pid, clone), p)
            continue
        if call == 'fchdir':
            cwd[pid] = None
            unresolved.append((pid, line.strip()))
            continue
        if call not in ('mkdir', 'mkdirat'):
            continue
        if call == 'mkdir':
            p = STR.search(args[0]).group(1) if args and STR.search(args[0]) else None
            base = 'AT_FDCWD'
            resolved = resolve(cwd.get(pid, clone), p) if p is not None else None
        else:
            fdarg = args[0] if args else ''
            fm = FD.match(fdarg)
            if fdarg.startswith('AT_FDCWD'):
                base = 'AT_FDCWD'
                p = STR.search(args[1]).group(1) if len(args) > 1 and STR.search(args[1]) else None
                resolved = resolve(cwd.get(pid, clone), p) if p is not None else None
            elif fm:
                base = fm.group(2)
                p = STR.search(args[1]).group(1) if len(args) > 1 and STR.search(args[1]) else None
                resolved = resolve(fm.group(2), p) if p is not None else None
            else:
                base = fdarg
                p = STR.search(args[1]).group(1) if len(args) > 1 and STR.search(args[1]) else None
                resolved = None
        rows.append({'pid': pid, 'call': call, 'base': base, 'path': p,
                     'resolved': resolved, 'ret': ret, 'line': line.strip()})
    return rows, unresolved

def main():
    clone = os.path.realpath(sys.argv[1])
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    want = sys.argv[3:]
    tools = load_tools(clone)
    if want and want[0] != 'all':
        tools = [t for t in tools if t[0] in want]
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['TMPDIR'] = ''
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    results = []
    for name, path, arg, row in tools:
        log = out / ('%s.log' % name)
        obs = out / ('%s.out' % name)
        cmd = ['strace', '-f', '-y', '-e',
               'trace=mkdir,mkdirat,chdir,fchdir', '-o', str(log),
               sys.executable, path, arg]
        proc = subprocess.run(cmd, cwd=clone, env=env, capture_output=True, timeout=1800)
        text = (proc.stdout + proc.stderr).decode('utf-8', 'replace')
        obs.write_text(text)
        rows, unresolved = track(log.read_text(errors='replace'), clone)
        under = [r for r in rows if r['resolved'] and (r['resolved'] == clone or r['resolved'].startswith(clone + '/'))]
        unknown = [r for r in rows if r['resolved'] is None]
        tmp = [r for r in rows if r['resolved'] and (r['resolved'] == '/tmp' or r['resolved'].startswith('/tmp/'))]
        other = [r for r in rows if r['resolved'] and r not in under and r not in tmp]
        results.append({
            'tool': name, 'row': row, 'exit': proc.returncode,
            'mkdir_calls': len(rows),
            'first_resolved': next((r['resolved'] for r in rows if r['resolved']), None),
            'under_workdir': [r['resolved'] for r in under],
            'unresolved': [r['line'] for r in unknown],
            'platform_tmp': len(tmp), 'other_abs': sorted({os.path.dirname(r['resolved']) for r in other})[:10],
            'other_count': len(other),
            'last_line': text.strip().splitlines()[-1] if text.strip() else '',
        })
        print('%s exit=%s mkdirs=%d tmp=%d other=%d under_workdir=%d unresolved=%d first=%s'
              % (name, proc.returncode, len(rows), len(tmp), len(other), len(under), len(unknown),
                 results[-1]['first_resolved']))
        for r in under:
            print('  UNDER_WORKDIR ' + r['resolved'])
        for u in unknown[:5]:
            print('  UNRESOLVED ' + u)
        if results[-1]['other_abs']:
            print('  other dirs: ' + json.dumps(results[-1]['other_abs']))
    (out / 'summary2.json').write_text(json.dumps(results, indent=1) + '\n')
    return 0

if __name__ == '__main__':
    sys.exit(main())
