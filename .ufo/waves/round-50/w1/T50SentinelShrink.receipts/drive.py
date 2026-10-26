import importlib.util, json, os, sys
S = '/fast/scratch/hyaku/tameshi-r50/T50SentinelShrink'
LANE = S + '/lane'
REAL = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
spec = importlib.util.spec_from_file_location('r50c2', S + '/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rev, mode, work = sys.argv[1], sys.argv[2], sys.argv[3]
pub = S + '/harness/panel.json'; hid = S + '/harness/hidden.json'
psha = m.sha(open(pub, 'rb').read()); hsha = m.sha(open(hid, 'rb').read())
os.environ['R50_MODE'] = mode
os.environ['R50_RUNS'] = os.environ.get('R50_RUNS', 'bool')
os.makedirs(work, exist_ok=True)
counts, stat, total = m.measure(LANE, rev, work, pub, hid, psha, hsha,
                                'e3729de862f73ae080d98fcf522a7081ce16e40a', log=lambda *a: print(*a),
                                gen_lane=REAL)
print(m.line(rev, counts, stat, total))
print('COUNTS=%r' % (counts,))
print('STAT=%r' % (stat,))
