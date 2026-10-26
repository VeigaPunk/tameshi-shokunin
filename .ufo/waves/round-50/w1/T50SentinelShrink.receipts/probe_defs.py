import importlib.util, json, os, subprocess, sys
S = '/fast/scratch/hyaku/tameshi-r50/T50SentinelShrink'
REAL = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
spec = importlib.util.spec_from_file_location('r50c2', S + '/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
GUARD = subprocess.run(['git', '-C', REAL, 'show',
                        'e3729de862f73ae080d98fcf522a7081ce16e40a:tools/staged-id-guard.py'],
                       capture_output=True).stdout.decode()

print('== D: is_subcase ignores line terminators ==')
c = {'registry': '| S001 | a | b | c | d |\n| S002 | e | f | g | h |\n', 'staged': '', 'map': None}
s = {'registry': '| S001 | a | b | c | d |\r\n| S002 | e | f | g | h |\r\n', 'staged': '', 'map': None}
print('byte-equal-line-ends:', c['registry'] == s['registry'],
      ' is_subcase(s,c):', m.is_subcase(s, c),
      ' units c/s:', m.units(c), m.units(s),
      ' splitlines(True) c:', c['registry'].splitlines(True)[:1])

print('== A: .runs symlink escapes the work dir ==')
vic = os.path.join(S, 'victim-repo')
os.makedirs(vic, exist_ok=True)
open(os.path.join(vic, 'notes.txt'), 'w').write('clean\n')
subprocess.run(['git', '-C', vic, 'init', '-q'], check=True)
subprocess.run(['git', '-C', vic, '-c', 'user.name=t', '-c', 'user.email=t@t', 'add', '-A'], check=True)
subprocess.run(['git', '-C', vic, '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'base'], check=True)
assert subprocess.run(['git', '-C', vic, 'rev-parse', '--show-toplevel'], capture_output=True).stdout.decode().strip() == vic
probe = os.path.join(S, 'probe', 'symlink')
os.makedirs(probe, exist_ok=True)
open(os.path.join(probe, 'guard_p.py'), 'w').write(m.instrument(GUARD, 'p'))
link = os.path.join(probe, '.runs')
if os.path.lexists(link):
    os.unlink(link)
os.symlink(os.path.join(vic, 'notes.txt'), link)
rc = subprocess.run([sys.executable, '-I', os.path.join(probe, 'guard_p.py')], capture_output=True).returncode
print('guard rc:', rc, ' .runs is symlink:', os.path.islink(link), '->', os.readlink(link))
print('victim notes.txt now:', repr(open(os.path.join(vic, 'notes.txt')).read()))
print('victim git status:', repr(subprocess.run(['git', '-C', vic, 'status', '--porcelain'],
                                               capture_output=True).stdout.decode()))

print('== A2: .runs -> /dev/zero makes the counter read hang ==')
z = os.path.join(S, 'probe', 'zero')
os.makedirs(z, exist_ok=True)
if os.path.lexists(os.path.join(z, '.runs')):
    os.unlink(os.path.join(z, '.runs'))
os.symlink('/dev/zero', os.path.join(z, '.runs'))
r = subprocess.run([sys.executable, '-c',
                    'import sys\n'
                    'with open(sys.argv[1]) as fh:\n'
                    '    print("lines", sum(1 for _ in fh))\n', os.path.join(z, '.runs')],
                   capture_output=True, timeout=5)
print('bounded read rc:', r.returncode, r.stdout[:80])

print('== F: instrument() anchors inside a docstring when it holds a column-0 import ==')
synth = '#!/usr/bin/env python3\n"""Doc.\n\nimport os\n"""\nimport sys\nprint("body ran")\n'
inst = m.instrument(synth, 'p')
print('instrumented source:', json.dumps(inst))
d = os.path.join(S, 'probe', 'anchor'); os.makedirs(d, exist_ok=True)
p = os.path.join(d, 'g.py'); open(p, 'w').write(inst)
print('run rc:', subprocess.run([sys.executable, '-I', p], capture_output=True).returncode,
      ' .runs exists:', os.path.exists(os.path.join(d, '.runs')),
      ' stdout:', subprocess.run([sys.executable, '-I', p], capture_output=True).stdout)
