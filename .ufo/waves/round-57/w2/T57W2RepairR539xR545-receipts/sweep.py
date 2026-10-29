import json, re, subprocess, sys, os
L = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
def git(*a, check=False):
    return subprocess.run(['git', '-C', L] + list(a), capture_output=True)
def show(rev, path):
    p = git('show', '%s:%s' % (rev, path))
    return p.stdout.decode('utf-8', 'replace') if p.returncode == 0 else None
def norm(t): return ' '.join(t.split())
c = json.load(open(L + '/.ufo/evidence/round-57/c1/defects.json'))
it = {x['id']: x for x in c['defects']}
ID = sys.argv[1]; item = it[ID]
keys = item['keys']; txt = item['text'] + ' ' + item.get('extended_text', '')
routed = item['routed_at']
revs = git('rev-list', '--reverse', '%s..%s' % (routed, BASE)).stdout.decode().split()
print('candidate commits after routed_at:', len(revs))
kre = [re.compile(r'(?<![\w-])' + re.escape(k) + r'(?![\w-])', re.I) for k in keys]
hits = []
for cm in revs:
    files = git('diff-tree', '--no-commit-id', '--name-only', '-r', '--root', '-m', cm).stdout.decode().split()
    files = set(f for f in files if f)
    named = [f for f in files if f in txt or f.rsplit('/', 1)[-1] in txt]
    if not named:
        continue
    msg = git('log', '-1', '--format=%B', cm).stdout.decode('utf-8', 'replace')
    names = re.search(r'(?<![\w.])' + re.escape(ID) + r'(?!\d)', msg) is not None
    print('COMMIT', cm[:12], 'named files:', named, 'names_id:', names, 'subj:', msg.split('\n')[0][:80])
    for f in named:
        now = show(BASE, f)
        if now is None: continue
        then = show(routed, f)
        parents = git('rev-list', '--parents', '-n', '1', cm).stdout.decode().split()[1:]
        prev = show(parents[0], f) if parents else None
        lines = now.split('\n')
        for i, ln in enumerate(lines):
            if any(r.search(ln) for r in kre):
                print('   KEYLINE', f, i+1, repr(ln[:160]))
