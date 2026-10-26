import importlib.util, json, os, subprocess, sys
S = '/fast/scratch/hyaku/tameshi-r50/T50SentinelShrink'
REAL = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
spec = importlib.util.spec_from_file_location('r50c2', S + '/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
LANE = S + '/lane'
REV = sys.argv[1]

print('== F: instrument() anchors on the first column-0 "import " even inside a docstring ==')
synth = '#!/usr/bin/env python3\n"""Doc.\n\nimport os\n"""\nimport sys\nprint("body ran")\n'
inst = m.instrument(synth, 'p')
print('instrumented source:', json.dumps(inst))
d = os.path.join(S, 'probe', 'anchor'); os.makedirs(d, exist_ok=True)
p = os.path.join(d, 'g.py'); open(p, 'w').write(inst)
if os.path.exists(os.path.join(d, '.runs')):
    os.unlink(os.path.join(d, '.runs'))
r = subprocess.run([sys.executable, '-I', p], capture_output=True)
print('run rc:', r.returncode, ' stdout:', r.stdout, ' .runs exists:',
      os.path.exists(os.path.join(d, '.runs')))

print('== C: a panel that is a JSON array crashes measure() with AttributeError ==')
arr = os.path.join(S, 'harness', 'panel-array.json')
raw = b'[{"id": "M01", "old": "x", "new": "y"}]'
open(arr, 'wb').write(raw)
w = os.path.join(S, 'w-array')
os.makedirs(w, exist_ok=True)
try:
    m.measure(LANE, REV, w, arr, S + '/harness/hidden.json', m.sha(raw),
              m.sha(open(S + '/harness/hidden.json', 'rb').read()),
              'e3729de862f73ae080d98fcf522a7081ce16e40a', log=print, gen_lane=REAL)
    print('NO CRASH')
except Exception as exc:
    print('RAISED %s: %s' % (type(exc).__name__, exc))

print('== E: capture_output=True has no size cap (parent buffers the child output) ==')
r = subprocess.run([sys.executable, '-c',
                    'import sys\nsys.stdout.buffer.write(b"x" * (300 * 1024 * 1024))\n'],
                   capture_output=True)
hwm = [l for l in open('/proc/self/status') if l.startswith('VmHWM')][0].strip()
print('captured bytes:', len(r.stdout), ' parent', hwm)
