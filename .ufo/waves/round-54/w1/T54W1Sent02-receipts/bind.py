#!/usr/bin/env python3
"""Hand-bind one cold-read ledger entry at C0 in a scratch clone (attack fixture).

Usage: bind.py LANE MODE
  MODE=loginput  entry inputs carry LOG.md with its sha256 at C0,
                 trace receipt records the same sha
  MODE=laundry   entry inputs carry PROVINCE.md only; the LOG.md dependency is
                 recorded in the entry-level external_inputs map
Stdlib only; touches nothing outside LANE.
"""
import hashlib
import json
import os
import subprocess
import sys

LANE = sys.argv[1]
MODE = sys.argv[2]
C0 = '59c38109bf119d0e9d4f878644a82babc937bc1e'
HEADING = '## Standing rules'
START, END = 17, 40
SECTION_SHA = '164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
REKEY = '.ufo/evidence/round-21/coldread/rekey-r54-%s' % C0[:12]


def blob_sha(rel):
    out = subprocess.run(['git', '-C', LANE, 'show', '%s:%s' % (C0, rel)],
                         capture_output=True, check=True).stdout
    return hashlib.sha256(out).hexdigest()


log_sha = blob_sha('LOG.md')
prov_sha = blob_sha('PROVINCE.md')

if MODE == 'loginput':
    seat, trace, inputs, external = 'SENT01', {'LOG.md': log_sha}, {'LOG.md': log_sha}, {}
elif MODE == 'laundry':
    seat, trace, inputs, external = 'SENT02', {'PROVINCE.md': prov_sha}, {'PROVINCE.md': prov_sha}, {'LOG.md': log_sha}
else:
    sys.exit('unknown mode %s' % MODE)

trace_rel = '%s/traces/%s/1.json' % (REKEY, seat)
trace_abs = os.path.join(LANE, trace_rel)
os.makedirs(os.path.dirname(trace_abs), exist_ok=True)
with open(trace_abs, 'w', encoding='utf-8') as f:
    json.dump({'schema': 'tameshi-trace-inputs-v1', 'inputs': trace}, f,
              indent=1, sort_keys=True)
    f.write('\n')

ledger_abs = os.path.join(LANE, LEDGER)
with open(ledger_abs, encoding='utf-8') as f:
    ledger = json.load(f)
entry = {
    'skill_sha256': hashlib.sha256(subprocess.run(
        ['git', '-C', LANE, 'show', '%s:SKILL.md' % C0],
        capture_output=True, check=True).stdout).hexdigest(),
    'start': START,
    'end': END,
    'heading': HEADING,
    'sha256': SECTION_SHA,
    'class': 'record',
    'verdict': 'verified-record',
    'blocking_gaps': 0,
    'wrong_expectations': 0,
    'minor_gaps': 0,
    'commands_executed_count': 1,
    'read_rev': C0,
    'inputs': inputs,
    'external_inputs': external,
    'traces': [trace_rel],
    'seats': [seat],
    'reports': ['%s/traces/%s/1.json' % (REKEY, seat)],
}
ledger['entries'].append(entry)
with open(ledger_abs, 'w', encoding='utf-8') as f:
    json.dump(ledger, f, indent=1, ensure_ascii=False)
    f.write('\n')
print(json.dumps({'mode': MODE, 'entry': entry}, sort_keys=True))
