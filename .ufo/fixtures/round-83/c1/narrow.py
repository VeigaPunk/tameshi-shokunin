"""Delete the self-state manifest's own population monitor row.

The cheat R83-C1 closes: with the monitor row (`standing-pin-audit`) gone, no
remaining row re-runs the sweep, so a narrowed population measures green.
Usage: python3 narrow.py <path/to/selfstate-freshness.json>
"""
import json
import sys

path = sys.argv[1]
data = json.load(open(path))
before = len(data['rows'])
data['rows'] = [r for r in data['rows'] if r['id'] != 'standing-pin-audit']
if len(data['rows']) != before - 1:
    raise SystemExit('narrow.py: expected exactly one standing-pin-audit row')
with open(path, 'w', newline='\n') as fh:
    json.dump(data, fh, indent=1)
    fh.write('\n')
print('narrowed: rows %d -> %d' % (before, len(data['rows'])))
