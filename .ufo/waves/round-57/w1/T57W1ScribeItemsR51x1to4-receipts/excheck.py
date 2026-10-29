import json, subprocess, sys
C, B, R, S = sys.argv[1:5]
rows = json.load(open(S + '/rows_only.json'))['defects']
def show(rev, p):
    r = subprocess.run(['git', '-C', C, 'show', rev + ':' + p], capture_output=True)
    return r.stdout.decode('utf-8', 'replace') if r.returncode == 0 else None
for row in rows:
    for e in row['evidence']:
        a, b = map(int, e['lines'].split('-'))
        win = ' '.join(' '.join(show(B, e['path']).split('\n')[a - 1:b]).split())
        rtxt = show(R, e['path'])
        absent = rtxt is not None and e['excerpt'] not in ' '.join(rtxt.split())
        print(row['id'], e['path'], e['lines'], 'present_at_base=%s' % (e['excerpt'] in win), 'absent_at_ef19d8e=%s' % absent, '|', e['excerpt'][:80])
