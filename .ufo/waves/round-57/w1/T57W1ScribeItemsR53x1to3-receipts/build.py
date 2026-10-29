import importlib.util, json, subprocess, sys, os
LANE = os.environ['LANE']; REV = os.environ['REV']
spec = importlib.util.spec_from_file_location('m50', '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-50/c1/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ls = subprocess.run(['git', '-C', LANE, 'ls-tree', '-r', '--name-only', REV, 'corpus/lessons'], capture_output=True, text=True).stdout.split('\n')
spotchecks = {p: 'x' for p in ls if p.endswith('-verifier-spotcheck.md')}
SEAT = 'T57W1ScribeItemsR53x1to3'
R53_1 = {
 'id': 'R53.1', 'status': 'open', 'seat': SEAT,
 'keys': ['rekey-dir-count', 'ls-tree', 'rekeyed=0', 'total=6', 'coldread'],
 'evidence': [
  {'path': '.ufo/evidence/round-53/c1/measure.py', 'lines': '94-95', 'excerpt': "r = git(['-C', lane, 'ls-tree', '--name-only', rev, '.ufo/evidence/round-21/coldread'])"},
  {'path': '.ufo/evidence/round-53/c1/measure.py', 'lines': '96-97', 'excerpt': "if re.fullmatch(r'rekey-r53-[0-9a-f]{12}', n)]"},
  {'path': '.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout', 'lines': '1-1', 'excerpt': 'C1_R53: rev=88afa9415454 credited=58 lost=6 rekeyed=0/30 readers=25/30 total=37 C1_R53_PASS=false'},
  {'path': 'SCORECARD.md', 'lines': '2550-2551', 'excerpt': '`C1_R53_PASS=false`, `total=6`.'},
 ],
 'note': 'frozen round-53 counter: pathspec lacks trailing slash and the basename is compared as full path; rekeyed=0/30 at every rev; SCORECARD quotes total=6 where the counter prints total=37 at 88afa941 (round-54 successor counter fixes the class; this frozen file is unchanged)',
 'verdict_basis': 'Still true at base: round-53 c1/measure.py lines 94-97 are unchanged (git log shows no commit after 2ef0a5a touching .ufo/evidence/round-53); the counter run at 88afa941 prints rekeyed=0/30 and total=37 while SCORECARD quotes total=6.',
}
R53_2 = {
 'id': 'R53.2', 'status': 'open', 'seat': SEAT,
 'keys': ['round-53/after', 'deciding run', 'deciding receipts', 'after/'],
 'evidence': [
  {'path': 'LOG.md', 'lines': '2489-2490', 'excerpt': 'break-one controls all printed false as pre-registered. Deciding receipts: `.ufo/evidence/round-53/after/`.'},
  {'path': 'SCORECARD.md', 'lines': '2543-2543', 'excerpt': 'Deciding run at `88afa941` (`.ufo/evidence/round-53/after/`): **C1 honest stop** —'},
  {'path': 'SCORECARD.md', 'lines': '2526-2526', 'excerpt': 'Deciding run (`.ufo/evidence/round-53/after/`): FROZEN_UNCHANGED=1 (freeze'},
 ],
 'note': 'past-tense pointers to round-53/after/ receipts that were never produced; corrected by the staged SCORECARD/LOG diff',
 'verdict_basis': 'Still true at base: LOG.md:2489-2490 and SCORECARD.md:2526,2543 cite .ufo/evidence/round-53/after/ in past tense and no path under that directory exists in the tree at base (git ls-tree -r finds none); no later commit touches the round-53 evidence tree.',
}
R53_3 = {
 'id': 'R53.3', 'status': 'open', 'seat': SEAT,
 'keys': ['CONTROLS_B', 'break-fixtures', 'phase B', 'control/'],
 'evidence': [
  {'path': '.ufo/evidence/round-53/control/break-fixtures.py', 'lines': '169-169', 'excerpt': "print('CONTROLS_B: total=%d pass=%d' % (len(results), sum(results)))"},
  {'path': '.ufo/evidence/round-53/control/break-fixtures.py', 'lines': '98-99', 'excerpt': "r = git(['ls-tree', '--name-only', CAND, '.ufo/evidence/round-21/coldread'])  rekey = [n for n in r.stdout.split('\\n') if re.fullmatch(r'rekey-r53-[0-9a-f]{12}', n)][0]"},
  {'path': 'SCORECARD.md', 'lines': '2518-2519', 'excerpt': 'unmodified candidate printed true (receipts `.ufo/evidence/round-53/control/`).'},
 ],
 'note': 'no CONTROLS_B receipt is committed under .ufo/; the phase-B script dies with IndexError at its rekey discovery (same pathspec class as R53.1) and its C1 leg is false for the dead-arm reason at 88afa941',
 'verdict_basis': 'Still true at base: no path under .ufo/ at base contains a round-53 CONTROLS_B tally (git grep CONTROLS_B finds only the script print and round-54/55/56 receipts); break-fixtures.py lines 98-99 use the same non-matching pathspec.',
}
rows = [R53_1, R53_2, R53_3]
out = []
for r in rows:
    ok = True; reasons = []
    for ev in r['evidence']:
        why = m.check_evidence(LANE, REV, ev, r['keys'], spotchecks, {})
        if why: ok = False; reasons.append((ev['path'], why))
    keyed = [ev for ev in r['evidence'] if m.has_key(ev, r['keys'])]
    print(r['id'], 'resolves' if ok else 'FAIL', reasons, 'keyed', len(keyed))
    out.append(r)
json.dump(out, open(os.environ['OUT'], 'w'), indent=1, ensure_ascii=False)
