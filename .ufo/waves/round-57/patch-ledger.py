#!/usr/bin/env python3
"""patch-ledger.py LEDGER_IN ROWS_JSON LEDGER_OUT : replace/insert rows by id (rows.json is a list of row objects)."""
import json, sys
d = json.load(open(sys.argv[1])); new = {r['id']: r for r in json.load(open(sys.argv[2]))}
seen = set()
for i, r in enumerate(d['defects']):
    if r['id'] in new:
        d['defects'][i] = new[r['id']]; seen.add(r['id'])
assert seen == set(new), ('ids not in ledger', set(new) - seen)
open(sys.argv[3], 'w', encoding='utf-8').write(json.dumps(d, indent=1, ensure_ascii=False) + '\n')
print('patched', len(new))
