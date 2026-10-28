"""Does binder.py's `max(key=str(read_rev))` pick the newest prior entry?

Usage: recency.py LANE LEDGER_REV
Reads LEDGER_REV:.ufo/evidence/round-21/coldread/ledger.json, and for every
heading in the lost-headings list prints the binder's pick next to the entry
whose read_rev is newest by committer date.
"""
import json, subprocess, sys
LANE, REV = sys.argv[1], sys.argv[2]
def git(*a):
    return subprocess.run(['git', '-C', LANE, *a], capture_output=True).stdout
led = json.loads(git('show', '%s:.ufo/evidence/round-21/coldread/ledger.json' % REV))['entries']
lost = json.loads(git('show', '%s:.ufo/evidence/round-55/c1/lost-headings-at-c0.json' % REV))
bad = 0
for h in sorted(lost):
    old = [e for e in led if e.get('heading') == h]
    pick = max(old, key=lambda e: str(e.get('read_rev', '')))
    def ctime(e):
        out = git('show', '-s', '--format=%ct', str(e.get('read_rev')))
        return out.decode().strip()
    newest = max(old, key=ctime)
    same = newest.get('read_rev') == pick.get('read_rev')
    bad += not same
    print('%-62s pick=%s(%-18s) newest_by_date=%s %s' % (
        h[:62], pick.get('read_rev')[:8], pick.get('verdict'),
        newest.get('read_rev')[:8], 'ok' if same else 'MISMATCH'))
print('RECENCY mismatches=%d of %d' % (bad, len(lost)))
