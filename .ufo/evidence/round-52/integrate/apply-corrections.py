#!/usr/bin/env python3
"""Round-52 L1 integration: append the 20 wave-1 correction records to the round-21 cold-read ledger.

Usage: apply-corrections.py LANE [--check]
Reads .ufo/waves/round-52/w1/T52W1CorrNN.json (one per round-51 re-key entry), validates each against the frozen C2
rule (counter .ufo/evidence/round-52/c2/measure.py check_findings, floors, count == len(findings), heading/read_rev/
reader/reader_file equal to the ledger entry), and writes them as the ledger's top-level "corrections" list (the
entries stay as written: append-only). Each record also carries "source": the seat file and "routed_by": the
closure defect. --check validates only. Exit 0 iff every record is valid.
"""
import importlib.util, json, os, sys

lane = sys.argv[1]
check_only = '--check' in sys.argv
spec = importlib.util.spec_from_file_location('c2', os.path.join(lane, '.ufo/evidence/round-52/c2/measure.py'))
c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
led_path = os.path.join(lane, '.ufo/evidence/round-21/coldread/ledger.json')
led = json.load(open(led_path))
if 'corrections' in led and not check_only:
    raise SystemExit('ledger already carries corrections; refusing to rewrite')
out, bad = [], []
for e in led['entries']:
    if not str(e.get('read_rev', '')).startswith('02ec217c'):
        continue
    seat = next(s for s in e['seats'] if s.startswith('T51W2Read'))
    src = '.ufo/waves/round-52/w1/T52W1Corr%s.json' % seat[-2:]
    try:
        r = json.load(open(os.path.join(lane, src)))
    except (OSError, ValueError) as exc:
        bad.append('%s: %s' % (src, exc)); continue
    rf = '.ufo/evidence/round-51/coldread/reads/%s.md' % seat
    why = None
    if (r.get('heading'), r.get('read_rev'), r.get('reader'), r.get('reader_file')) != (e['heading'], e['read_rev'], seat, rf):
        why = 'identity fields differ from the ledger entry'
    else:
        why = c2.check_findings(r.get('findings'), open(os.path.join(lane, rf), encoding='utf-8').read(), c2.FLOORS.get(seat, ()))
        if why is None and r.get('wrong_expectations') != len(r['findings']):
            why = 'count != len(findings)'
    if why:
        bad.append('%s: %s' % (src, why)); continue
    out.append({'heading': e['heading'], 'read_rev': e['read_rev'], 'reader': seat, 'reader_file': rf,
                'wrong_expectations': r['wrong_expectations'],
                'findings': [{k: f[k] for k in ('quote', 'class', 'skill_statement') if k in f} for f in r['findings']],
                'corrects': 'ledger entry %s @ %s: wrong_expectations 0 was written from code (round-51 refresh.py:227)'
                            % (e['heading'], e['read_rev'][:8]),
                'source': src, 'routed_by': 'corpus/lessons/round-51-verifier-spotcheck.md routed defect 3'})
for b in bad:
    print('CORRECTION_BAD', b)
print('CORRECTIONS: valid=%d bad=%d findings=%d' % (len(out), len(bad), sum(len(x['findings']) for x in out)))
if bad or len(out) != 20:
    sys.exit(1)
if not check_only:
    led['corrections'] = out
    with open(led_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(led, indent=1, ensure_ascii=True))  # the ledger's own serialization (no newline)
    print('CORRECTIONS: written to', led_path)
