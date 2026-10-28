#!/usr/bin/env python3
"""Round-54 W1 item (T54W1ExecEmptyStrace): strace the seven self-tests under TMPDIR="".

Runs each tool listed in the frozen counter's TOOLS (imported from the clone's
.ufo/evidence/round-54/c2/measure.py, so the mapping is provably the counter's)
as:

    TMPDIR="" strace -f -e trace=mkdir,mkdirat -o LOG python3 <tool> <arg>

with cwd = the clone (the deciding revision 59c38109bf11).  For each tool it
reports exit, the mkdir/mkdirat paths used, and whether any of them landed in
or under the working directory (relative path with AT_FDCWD, or the clone
itself) rather than the platform default root.

Writes: <out>/logs/<name>.log (raw strace), <out>/logs/<name>.out (child
stdout+stderr), <out>/summary.json, <out>/tree-before.txt, <out>/tree-after.txt.
"""
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

LINE = re.compile(r'^\s*(\d+)\s+(mkdir|mkdirat)\((.*)\)\s+=\s+(-?\d+)')
STR = re.compile(r'"((?:[^"\\]|\\.)*)"')

def load_tools(clone):
    p = Path(clone) / '.ufo' / 'evidence' / 'round-54' / 'c2' / 'measure.py'
    spec = importlib.util.spec_from_file_location('c2measure', str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.TOOLS

def tree(root):
    root = Path(root)
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != '.git']
        rel = os.path.relpath(dirpath, root)
        out.append('D ' + (rel if rel != '.' else '.'))
        for f in filenames:
            out.append('F ' + os.path.relpath(os.path.join(dirpath, f), root))
    return sorted(out)

def parse_log(text):
    rows = []
    for line in text.splitlines():
        m = LINE.match(line)
        if not m:
            continue
        pid, call, rest, ret = m.group(1), m.group(2), m.group(3), m.group(4)
        dirs = STR.findall(rest)
        if call == 'mkdir':
            path = dirs[0] if dirs else ''
            base = 'cwd'
        else:
            # mkdirat(dirfd, path, mode); dirs[0] may be AT_FDCWD (no quotes),
            # so the quoted path is dirs[0] when the dirfd is numeric.
            path = dirs[-1] if dirs else ''
            base = 'AT_FDCWD' if 'AT_FDCWD' in rest else 'DIRFD'
        rows.append({'pid': pid, 'call': call, 'path': path, 'dirfd': base,
                     'ret': ret, 'line': line.strip()})
    return rows

def classify(path, clone):
    if path.startswith('/'):
        if path == clone or path.startswith(clone + '/'):
            return 'under-workdir'
        if path.startswith('/tmp/') or path == '/tmp':
            return 'platform-default-tmp'
        return 'absolute-other'
    return 'relative-cwd'

def main():
    clone = os.path.realpath(sys.argv[1])
    out = Path(sys.argv[2])
    (out / 'logs').mkdir(parents=True, exist_ok=True)
    tools = load_tools(clone)
    before = tree(clone)
    (out / 'tree-before.txt').write_text('\n'.join(before) + '\n')
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['TMPDIR'] = ''
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    summary = []
    for name, path, arg, row in tools:
        log = out / 'logs' / ('%s.log' % name)
        obs = out / 'logs' / ('%s.out' % name)
        cmd = ['strace', '-f', '-e', 'trace=mkdir,mkdirat', '-o', str(log),
               sys.executable, path, arg]
        proc = subprocess.run(cmd, cwd=clone, env=env, capture_output=True, timeout=900)
        text = (proc.stdout + proc.stderr).decode('utf-8', 'replace')
        obs.write_text(text)
        rows = parse_log(log.read_text(errors='replace')) if log.exists() else []
        paths = [r['path'] for r in rows]
        classes = {}
        for r in rows:
            c = classify(r['path'], clone)
            classes[c] = classes.get(c, 0) + 1
        summary.append({
            'tool': name,
            'row': row,
            'argv': [path, arg],
            'exit': proc.returncode,
            'mkdir_calls': len(rows),
            'first_mkdir_path': paths[0] if paths else None,
            'unique_roots': sorted({('/' + p.split('/')[1]) if p.startswith('/') and len(p) > 1 else p for p in paths}),
            'classes': classes,
            'under_workdir': [r['path'] for r in rows if classify(r['path'], clone) == 'under-workdir'],
            'relative': [r['path'] for r in rows if classify(r['path'], clone) == 'relative-cwd'],
            'all_paths': paths,
            'last_line': text.strip().splitlines()[-1] if text.strip() else '',
        })
    after = tree(clone)
    (out / 'tree-after.txt').write_text('\n'.join(after) + '\n')
    (out / 'summary.json').write_text(json.dumps(summary, indent=1) + '\n')
    for s in summary:
        print('%s exit=%s mkdirs=%d first=%s classes=%s cwd_allocs=%d'
              % (s['tool'], s['exit'], s['mkdir_calls'], s['first_mkdir_path'],
                 s['classes'], len(s['under_workdir']) + len(s['relative'])))
    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    print('TREE_ADDED=%d TREE_REMOVED=%d' % (len(added), len(removed)))
    for a in added:
        print('ADDED ' + a)
    for r in removed:
        print('REMOVED ' + r)
    return 0

if __name__ == '__main__':
    sys.exit(main())
