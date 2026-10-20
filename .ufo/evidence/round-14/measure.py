#!/usr/bin/env python3
"""Static revision counts only; gate execution is recorded separately."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--rev', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]

def blob(path):
    result = subprocess.run(['git', '-C', str(root), 'show', f'{args.rev}:{path}'], capture_output=True)
    return result.stdout if result.returncode == 0 else None

def obj(path):
    value = blob(path)
    return json.loads(value) if value is not None else None

spec = obj('.ufo/evidence/round-14/dispositions.json')
rows = spec['rows'] if spec else []
expected = obj('.ufo/evidence/round-13/expected.json')['expected_checks']
verification = obj('.ufo/evidence/round-13/verification.json')
raw = next(x for x in verification['checks'] if x['name'] == 'producer_before')
runner = blob('tools/mutate-and-run.sh')
marks = re.findall(rb'^- \[([x~ ])\] ', blob('SHONEN.md'), re.M)
sources = [line.split('|') for line in blob('corpus/SOURCES.md').decode().splitlines() if re.match(r'^\|\s*S\d{3,}\s*\|', line)]
from collections import Counter
print(json.dumps({
    'revision': args.rev,
    'gate_artifact': int(blob('tools/evidence-disposition.py') is not None),
    'historical_expected_rows': len(expected),
    'effective_disposition_rows': sum(x['state'] == 'effective' for x in rows),
    'superseded_disposition_rows': sum(x['state'] == 'superseded' for x in rows),
    'disposition_name_coverage': len({x['name'] for x in rows} & expected.keys()),
    'historical_setup_exit': raw['exit'],
    'historical_mechanism_assertion_present': expected['producer_before']['contains'] in raw['stdout'],
    'recorded_cases': len(re.findall(rb'^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+', runner, re.M)),
    'calibration_restraint_score': 2 * sum(marks[i - 1] == b'~' for i in (1, 2, 4)),
    'runner_sha256': hashlib.sha256(runner).hexdigest(),
    'frozen_summary_sha256': hashlib.sha256(blob('.ufo/evidence/round-12/BashWitness/summary.json')).hexdigest(),
    'source_rows': len(sources),
    'source_tiers': dict(Counter(x[4].strip() for x in sources)),
    'source_statuses': dict(Counter(x[8].strip() for x in sources)),
}, indent=2, sort_keys=True))
