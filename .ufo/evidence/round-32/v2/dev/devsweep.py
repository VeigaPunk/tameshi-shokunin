#!/usr/bin/env python3
"""Dev sweep (L1, before the amendment-2 tool freeze): run the working tool on the PUBLIC v1 fixture
families over many seeds, deduplicated by body. Disclosed in contract-amendment-2.json."""
import concurrent.futures, hashlib, importlib.util, os, random, subprocess, sys, tempfile
L = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
s = importlib.util.spec_from_file_location('v1', L + '/.ufo/evidence/round-32/c1-measure.py')
v1 = importlib.util.module_from_spec(s); s.loader.exec_module(v1)
t = subprocess.run(['git', '-C', L, 'show', v1.PIN_REV + ':' + v1.RUNNER], capture_output=True).stdout.decode()
bodies = {}
for seed in range(int(sys.argv[1]) if len(sys.argv) > 1 else 300):
    rng = random.Random(seed)
    for l, b in v1.frozen_kill(t) + v1.generated_kill(t, rng):
        bodies.setdefault(b, ('kill', l))
    for l, b in v1.frozen_accept(t) + v1.generated_accept(t, rng):
        bodies.setdefault(b, ('accept', l))
tmp = tempfile.mkdtemp(prefix='devsweep.', dir='/fast/scratch/hyaku/tameshi-r32')
def run(item):
    b, (want, l) = item
    p = os.path.join(tmp, hashlib.sha256(b.encode()).hexdigest()[:16] + '.sh')
    open(p, 'w').write(b)
    r = subprocess.run([sys.executable, L + '/tools/tally-audit.py', '--runner', p], capture_output=True, text=True, timeout=600)
    os.unlink(p)
    ok = (want == 'kill' and r.returncode == 1) or (want == 'accept' and r.returncode == 0)
    return ok, want, l, r.returncode, (r.stdout.strip().splitlines() or [''])[-1]
bad = 0
with concurrent.futures.ThreadPoolExecutor(8) as ex:
    for ok, want, l, rc, last in ex.map(run, bodies.items()):
        if not ok:
            bad += 1
            print('MISS', want, l, rc, last[:120])
print('DEVSWEEP bodies=%d kill=%d accept=%d misses=%d' % (len(bodies), sum(1 for w, _ in bodies.values() if w == 'kill'),
      sum(1 for w, _ in bodies.values() if w == 'accept'), bad))
