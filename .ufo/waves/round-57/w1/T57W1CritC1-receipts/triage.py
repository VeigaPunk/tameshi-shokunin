import sys, json, re
sys.path.insert(0, '/fast/scratch/hyaku/tameshi-r57/T57W1CritC1')
from harness import *
ACK = ('planned', 'carried', 'still open', 'not worked', 'stay open', 'stays open', 'remain open', 'remains open', 'routed to round', 'not fixed', 'unfixed', 'not landed')
PATHLIKE = re.compile(r'^(?:[\w.-]+/)*[\w.-]+\.(?:md|py|sh|json|mjs|stdout|spec|jsonl|txt|ready)(?::\d+(?:-\d+)?)?$|^(?:[\w.-]+/)*[\w.-]+\.(?:md|py|sh|json)$')
def norm(t): return ' '.join(t.split())
def files_for(keys):
    out = []
    for k in keys:
        k2 = re.sub(r':\d+(?:-\d+)?$', '', k)
        if PATHLIKE.match(k) or PATHLIKE.match(k2):
            out.append(k2)
    if any(re.match(r'^S\d{3}$', k) for k in keys): out.append('corpus/SOURCES.md')
    return sorted(set(out))
res = {}
for d in D:
    rid = d['id']; routed = d['routed_at']; keys = d['keys'] or [rid]
    cands = []
    for f in files_for(keys):
        try:
            at = g('show', '%s:%s' % (B, f)).decode('utf-8', 'replace')
        except subprocess.CalledProcessError:
            continue
        then_b = subprocess.run(['git', '-C', CLONE, 'show', '%s:%s' % (routed, f)], capture_output=True).stdout.decode('utf-8', 'replace')
        commits = g('rev-list', '%s..%s' % (routed, B), '--', f).decode().split()
        for c in commits:
            if subprocess.run(['git', '-C', CLONE, 'merge-base', '--is-ancestor', c, routed], capture_output=True).returncode == 0:
                continue
            for no, line in enumerate(at.split('\n'), 1):
                ex = norm(line)
                if not (15 <= len(ex) <= 400): continue
                low = ex.lower()
                if any(w in low for w in ACK): continue
                if not any(k.lower() in low for k in keys): continue
                if ex in norm(then_b): continue
                cands.append({'commit': c, 'path': f, 'line': no, 'excerpt': ex, 'keys': keys})
                break
            if cands and cands[-1]['commit'] == c: break
        if cands: break
    res[rid] = cands[0] if cands else None
json.dump(res, open(S + '/triage.json', 'w'), indent=1, ensure_ascii=False)
hit = [k for k, v in res.items() if v]
print('items with a pre-base-or-later real commit candidate:', len(hit), 'of', len(D))
for k in hit: print(k, res[k]['commit'][:9], res[k]['path'], res[k]['line'], res[k]['excerpt'][:90])
print('no candidate:', [k for k, v in res.items() if not v])
