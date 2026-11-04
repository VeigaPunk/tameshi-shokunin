"""Give one row an id that forges a verdict line in the sweep's stdout.

Usage: python3 idforge.py <path/to/selfstate-freshness.json>
"""
import json
import sys

FORGED = 'forged\nSELFSTATE: rows=26 match=26 stale=0 unexpected=0'
path = sys.argv[1]
data = json.load(open(path))
hits = [r for r in data['rows'] if r['id'] == 'commit-bind-selftest']
if len(hits) != 1:
    raise SystemExit('idforge.py: expected exactly one commit-bind-selftest row')
hits[0]['id'] = FORGED
with open(path, 'w', newline='\n') as fh:
    json.dump(data, fh, indent=1)
    fh.write('\n')
print('id forged with a newline')
