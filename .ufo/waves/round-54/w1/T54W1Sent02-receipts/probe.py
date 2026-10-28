#!/usr/bin/env python3
"""Ask the FROZEN round-18 credit algorithm (bytes at C0) why the bound entry
credits or does not, at each revision. Usage: probe.py LANE REV [LEDGER_AT_REV]"""
import importlib.util
import json
import os
import subprocess
import sys

lane, rev = sys.argv[1], sys.argv[2]
r18_path = '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py'
raw = subprocess.run(['git', '-C', lane, 'show', '59c38109bf119d0e9d4f878644a82babc937bc1e:.ufo/evidence/round-18/measure.py'],
                     capture_output=True, check=True).stdout
tmp = '/fast/scratch/hyaku/tameshi-r54/T54W1Sent02/r18_frozen.py'
with open(tmp, 'wb') as f:
    f.write(raw)
spec = importlib.util.spec_from_file_location('r18_frozen', tmp)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

ledger_raw = subprocess.run(['git', '-C', lane, 'show', '%s:.ufo/evidence/round-21/coldread/ledger.json' % rev],
                            capture_output=True, check=True).stdout
ledger = json.loads(ledger_raw.decode('utf-8', 'surrogateescape'))
mine = [e for e in ledger['entries'] if isinstance(e, dict)
        and e.get('heading') == '## Standing rules'
        and e.get('read_rev') == '59c38109bf119d0e9d4f878644a82babc937bc1e'
        and any('rekey-r54-' in str(t) for t in (e.get('traces') or []))]
out = {'rev': rev, 'entries': []}
for e in mine:
    out['entries'].append({
        'inputs': e.get('inputs'),
        'trace_inputs': json.loads(subprocess.run(
            ['git', '-C', lane, 'show', '%s:%s' % (rev, e['traces'][0])],
            capture_output=True, check=True).stdout.decode())['inputs'],
        'entry_reason': mod.entry_reason(lane, rev, e, True),
        'input_reason': mod.input_reason(lane, rev, e),
        'trace_reason': mod.trace_reason(lane, rev, e, True),
    })
print(json.dumps(out, indent=1))
