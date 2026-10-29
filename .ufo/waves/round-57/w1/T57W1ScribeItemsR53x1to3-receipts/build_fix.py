import importlib.util, json, subprocess, os
LANE = os.environ['LANE']; FIX = os.environ['FIX']; ROUTED = os.environ['ROUTED']; OUT = os.environ['OUT']
spec = importlib.util.spec_from_file_location('m50', '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-50/c1/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ls = subprocess.run(['git', '-C', LANE, 'ls-tree', '-r', '--name-only', ROUTED, 'corpus/lessons'], capture_output=True, text=True).stdout.split('\n')
spotchecks = {p: 'x' for p in ls if p.endswith('-verifier-spotcheck.md')}
SEAT = 'T57W1ScribeItemsR53x1to3'
rows = [
 {'id': 'R53.1', 'status': 'fixed', 'commit': FIX, 'seat': SEAT,
  'keys': ['rekey-dir-count', 'ls-tree', 'rekeyed=0', 'rekeyed=28', 'total=6', 'total=37', 'coldread', 'rekey-r53'],
  'evidence': [
   {'path': '.ufo/evidence/round-53/c1/measure.py', 'lines': '96-97', 'excerpt': "if re.fullmatch(r'rekey-r53-[0-9a-f]{12}', n.rsplit('/', 1)[-1])]"},
   {'path': '.ufo/evidence/round-53/direct-runs/c1-patched-counter-at-88afa941.stdout', 'lines': '1-1', 'excerpt': 'C1_R53: rev=88afa9415454 credited=58 lost=6 rekeyed=28/30 readers=25/30 total=8 C1_R53_PASS=false'},
  ]},
 {'id': 'R53.2', 'status': 'fixed', 'commit': FIX, 'seat': SEAT,
  'keys': ['round-53/after', 'direct-runs', 'after/', 'deciding run'],
  'evidence': [
   {'path': 'LOG.md', 'lines': '2489-2490', 'excerpt': 'Deciding receipts: none committed (round-57 R53.2; `.ufo/evidence/round-53/after/` does not exist).'},
   {'path': '.ufo/evidence/round-53/direct-runs/c1-at-88afa941.stdout', 'lines': '1-1', 'excerpt': 'C1_R53: rev=88afa9415454 credited=58 lost=6 rekeyed=0/30 readers=25/30 total=37 C1_R53_PASS=false'},
  ]},
 {'id': 'R53.3', 'status': 'fixed', 'commit': FIX, 'seat': SEAT,
  'keys': ['CONTROLS_B', 'break-fixtures', 'phase B', 'rekey-r53'],
  'evidence': [
   {'path': '.ufo/evidence/round-53/control/controls-b.stdout', 'lines': '8-8', 'excerpt': 'CONTROLS_B: total=7 pass=6'},
   {'path': '.ufo/evidence/round-53/control/break-fixtures.py', 'lines': '98-99', 'excerpt': "rekey = [n.rsplit('/', 1)[-1] for n in r.stdout.split('\\n') if re.fullmatch(r'rekey-r53-[0-9a-f]{12}', n.rsplit('/', 1)[-1])][0]"},
  ]},
]
ACK = m.ACK_WORDS
for r in rows:
    problems = []
    if not m.is_ancestor(LANE, FIX, FIX) or m.is_ancestor(LANE, FIX, ROUTED): problems.append('commit-order')
    files = m.touched(LANE, FIX)
    fresh = False
    keyed = [ev for ev in r['evidence'] if m.has_key(ev, r['keys'])]
    for ev in r['evidence']:
        why = m.check_evidence(LANE, FIX, ev, r['keys'], spotchecks, {})
        if why: problems.append(('resolve', ev['path'], why))
    for ev in keyed:
        if ev['path'] not in files: continue
        then = m.show(LANE, ROUTED, ev['path'])
        if then is not None and m.norm(ev['excerpt']) in m.norm(then.decode('utf-8', 'replace')): continue
        a, b = (int(x) for x in ev['lines'].split('-'))
        text = m.show(LANE, FIX, ev['path']).decode('utf-8', 'replace').split('\n')
        span = ' '.join(text[a-1:b]).lower()
        if any(w in span for w in ACK): continue
        fresh = True; break
    if not fresh: problems.append('fixed-not-new')
    if not keyed: problems.append('key-miss')
    r['verdict_check_at_fix'] = 'pass' if not problems else problems
    print(r['id'], r['verdict_check_at_fix'], 'files_touched', len(files))
json.dump(rows, open(OUT, 'w'), indent=1, ensure_ascii=False)
