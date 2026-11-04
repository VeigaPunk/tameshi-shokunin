"""Degrade one registry figure the round-83 binding measures.

`defect-bind-selftest` is bound from round 83 on; at the base manifest no row
reads it, so the same edit is invisible there.
Usage: python3 degrade.py <path/to/tools/registry.json>
"""
import json
import sys

path = sys.argv[1]
data = json.load(open(path))
hits = [r for r in data['rows'] if r.get('name') == 'defect-bind-selftest']
if len(hits) != 1:
    raise SystemExit('degrade.py: expected exactly one defect-bind-selftest row')
hits[0]['expect']['stdout_contains'] = ['DEFECT_BIND_SELFTEST: 11/11 pass']
with open(path, 'w', newline='\n') as fh:
    json.dump(data, fh, indent=1)
    fh.write('\n')
print('degraded: defect-bind-selftest -> 11/11 pass')
