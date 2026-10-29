import sys, json, re
sys.path.insert(0, '/fast/scratch/hyaku/tameshi-r57/T57W1CritC1')
from harness import *
T = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
base_ledger = json.loads(subprocess.run(['git','-C',T,'show',B+':corpus/routed-defects.json'],capture_output=True,check=True).stdout)
ids = [d['id'] for d in D]
def probe_commit():
    reset()
    lines = []
    for d in D:
        key = d['keys'][0] if d['keys'] else d['id']
        lines.append('%s: covered by the round-57 probe note for %s, see the routed entry.' % (key, d['id']))
    os.makedirs(CLONE + '/corpus', exist_ok=True)
    open(CLONE + '/corpus/r57-probe.txt', 'w').write('\n'.join(lines) + '\n')
    c = commit_all('probe')
    return c, lines
def ledger_rows(fixed_commit, lines, statuses):
    rows = []
    for i, d in enumerate(D, 1):
        st = statuses[d['id']]
        keys = d['keys'] or [d['id']]
        if st == 'fixed':
            rows.append({'id': d['id'], 'status': 'fixed', 'commit': fixed_commit,
                         'evidence': [{'path': 'corpus/r57-probe.txt', 'lines': '%d-%d' % (i, i), 'excerpt': lines[i-1]}]})
        elif st == 'declined':
            rows.append({'id': d['id'], 'status': 'declined', 'reason': 'Declined: the item is an observation about the record, not a repairable defect in the lane tree.',
                         'evidence': [{'path': 'corpus/r57-probe.txt', 'lines': '%d-%d' % (i, i), 'excerpt': lines[i-1]}]})
        else:
            rows.append({'id': d['id'], 'status': 'open', 'evidence': [{'path': 'corpus/r57-probe.txt', 'lines': '%d-%d' % (i, i), 'excerpt': lines[i-1]}]})
    return rows
def write_ledger(rows, keep_base=False):
    doc = {'schema': 'tameshi-routed-defects-v1', 'round': 57, 'note': 'attack ledger', 'defects': (base_ledger['defects'] if keep_base else []) + rows}
    open(CLONE + '/corpus/routed-defects.json', 'w').write(json.dumps(doc, indent=1))
def planned_para(open_ids, round_no=58):
    txt = '\n**Planned (round %d):** ' % round_no + ' '.join(open_ids) + '\n'
    return txt
def run_case(name, statuses, keep_base=False, plan_open=True, measure_mod=M, base=None, floor=20, cap=14, trf=6):
    c, lines = probe_commit()
    rows = ledger_rows(c, lines, statuses)
    write_ledger(rows, keep_base)
    if plan_open:
        opens = [i for i in ids if statuses[i] == 'open']
        if opens:
            sc = open(CLONE + '/SCORECARD.md').read()
            open(CLONE + '/SCORECARD.md', 'w').write(sc + planned_para(opens))
    rev = commit_all('ledger ' + name)
    rv, counts, stat, total, nrows = measure_mod.measure(CLONE, rev, D, True, floor, cap, None, trf, base)
    nz = {k: v for k, v in counts.items() if v}
    print('%-42s total=%d PASS=%s stat=%s counts_nonzero=%s' % (name, total, total == 0, stat, nz))
    return total
allfix = {i: 'fixed' for i in ids}
run_case('S1 51 fixed -> probe, base=B', allfix, base=B)
run_case('S1b 51 fixed -> probe, inherited BASE', allfix, base=None)
mix = {}
for n, i in enumerate(ids):
    mix[i] = 'fixed' if n < 20 else ('declined' if n < 34 else 'open')
run_case('S2 20 fixed+14 decl+17 open, inherit regex', mix, measure_mod=M, base=B)
run_case('S2b same, R\\d\\d regex', mix, measure_mod=MR, base=B)
run_case('S2c same, R\\d\\d, 49 base rows kept', mix, keep_base=True, measure_mod=MR, base=B)
allopen = {i: 'open' for i in ids}
mx = {i: ('fixed' if n < 20 else 'open') for n, i in enumerate(ids)}
run_case('S3 20 fixed + 31 open, R\\d\\d regex', mx, measure_mod=MR, base=B)
run_case('S3b 51 open named in Planned, R\\d\\d', allopen, measure_mod=MR, base=B)
run_case('S3c 51 open named, inherited regex', allopen, measure_mod=M, base=B)
run_case('S4 51 declined (bulk decline)', {i:'declined' for i in ids}, measure_mod=MR, base=B)
run_case('S5 this-round, 20 fixed, base=default', mix, measure_mod=MR, base=None)
print('--- rerun with lane-curated keys for empty-key items')
T_ = json.load(open(S + '/triage.json'))
run_case('S1 51 fixed -> probe, base=B', allfix, base=B)
run_case('S1b 51 fixed -> probe, inherited BASE', allfix, base=None)
run_case('S2 20f+14d+17o, inherited regex', mix, measure_mod=M, base=B)
run_case('S2b 20f+14d+17o, R\\d\\d regex', mix, measure_mod=MR, base=B)
run_case('S2c as S2b, 49 base rows kept', mix, keep_base=True, measure_mod=MR, base=B)
run_case('S3 20f + 31 open named, R\\d\\d', mx, measure_mod=MR, base=B)
run_case('S3b 51 open named in Planned, R\\d\\d', allopen, measure_mod=MR, base=B)
run_case('S4 51 declined (bulk decline)', {i:'declined' for i in ids}, measure_mod=MR, base=B, cap=14)
# S6: BASE definition: rows fixed only by pre-base real commits
pre = {k: v for k, v in T_.items() if v}
st = {i: 'declined' for i in ids}
c, lines = probe_commit()
rows = []
for d in D:
    if d['id'] in pre:
        v = pre[d['id']]
        rows.append({'id': d['id'], 'status': 'fixed', 'commit': v['commit'], 'evidence': [{'path': v['path'], 'lines': '%d-%d' % (v['line'], v['line']), 'excerpt': v['excerpt']}]})
    else:
        rows.append({'id': d['id'], 'status': 'declined', 'reason': 'Declined: the item is an observation about the record, not a repairable defect in the lane tree.', 'evidence': [{'path': 'corpus/r57-probe.txt', 'lines': '%d-%d' % (ids.index(d['id'])+1, ids.index(d['id'])+1), 'excerpt': lines[ids.index(d['id'])]}]})
write_ledger(rows)
rev = commit_all('S6 pre-base only')
for lbl, bb in (('base=B', B), ('inherited BASE', None)):
    rv, counts, stat, total, nrows = MR.measure(CLONE, rev, D, True, 0, 99, None, 0, bb)
    print('S6 pre-base-only fixed rows, %-16s stat=%s total=%d' % (lbl, stat, total), {k:v for k,v in counts.items() if v})
