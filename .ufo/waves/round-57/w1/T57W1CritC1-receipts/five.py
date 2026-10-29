import sys, json, subprocess
sys.path.insert(0,'/fast/scratch/hyaku/tameshi-r57/T57W1CritC1')
from harness import *
T = json.load(open(S + '/triage.json'))
PROBE_LINE = 'Declined: the item is an observation about the record, not a repairable defect in the lane tree.'
def single(rid):
    v = T[rid]
    rows = []
    for d in D:
        if d['id'] == rid:
            rows.append({'id': rid, 'status': 'fixed', 'commit': v['commit'], 'evidence': [{'path': v['path'], 'lines': '%d-%d' % (v['line'], v['line']), 'excerpt': v['excerpt']}]})
        else:
            rows.append({'id': d['id'], 'status': 'declined', 'reason': PROBE_LINE, 'evidence': [{'path': 'LOG.md', 'lines': '1-1', 'excerpt': None}]})
    # use a real excerpt for declined rows so only the target row is under test
    reset()
    lg = open(CLONE + '/LOG.md').read().split('\n')
    for r in rows:
        if r['status'] == 'declined':
            ln = next(i for i, l in enumerate(lg, 1) if len(' '.join(l.split())) >= 15)
            r['evidence'] = [{'path': 'LOG.md', 'lines': '%d-%d' % (ln, ln), 'excerpt': ' '.join(lg[ln-1].split())}]
    open(CLONE + '/corpus/routed-defects.json', 'w').write(json.dumps({'schema': 'tameshi-routed-defects-v1', 'round': 57, 'note': 'single-row test ' + rid, 'defects': rows}))
    rev = commit_all('single ' + rid)
    rv, counts, stat, total, n = MR.measure(CLONE, rev, D, True, 0, 99, None, 0, B)
    bad = {k: v for k, v in counts.items() if v}
    print('%-7s commit=%s path=%s excerpt=%r -> fixed_bad=%s evidence_bad=%s stat=%s' % (rid, v['commit'][:9], v['path'], v['excerpt'][:60], counts['fixed_bad'], counts['evidence_bad'], stat))
for rid in ['R50.1', 'R50.3', 'R52.5', 'R53.9', 'R54.1']:
    single(rid)
