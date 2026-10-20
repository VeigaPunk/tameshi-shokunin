#!/usr/bin/env python3
"""Count committed round-13 observations, never execute a target or gate."""
import argparse
import collections
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[3]
p = argparse.ArgumentParser()
p.add_argument('--rev', required=True)
a = p.parse_args()
rev = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', '--verify', a.rev + '^{commit}'], text=True).strip()
def blob(path):
    r = subprocess.run(['git', '-C', str(ROOT), 'show', f'{rev}:{path}'], capture_output=True)
    return r.stdout if r.returncode == 0 else None
def obj(path):
    b = blob(path)
    if b is None:
        return None
    try:
        return json.loads(b)
    except (ValueError, UnicodeError) as exc:
        return {'measurement_error': type(exc).__name__, 'path': path}
rows = []
for line in blob('corpus/SOURCES.md').decode().splitlines():
    cells = [c.strip() for c in line.split('|')]
    if len(cells) > 1 and re.fullmatch(r'S\d{3,}', cells[1]):
        rows.append(cells)
base = '.ufo/evidence/round-13/'
dispositions = obj(base + 'pin-dispositions.json')
companion = obj(base + 'witness-metadata.json')
marks = re.findall(r'^- \[([x~ ])\] ', blob('SHONEN.md').decode(), re.M)
gate_paths = re.findall(r'^#   (?:js|bash)-\S+\s+(\S+)\s+\d+/\d+', blob('tools/mutate-and-run.sh').decode(), re.M)
print(json.dumps({'revision': rev, 'pin_dispositions': dispositions, 'metadata_companion': companion,
    'metadata_companion_present': blob(base + 'witness-metadata.json') is not None,
    'pin_probe_artifact': int(blob('tools/pin-disposition.py') is not None),
    'metadata_checker_artifact': int(blob('tools/witness-metadata.py') is not None),
    'recorded_cases': len(gate_paths), 'unique_recorded_gates': len(set(gate_paths)),
    'calibration_restraint_score': 2 * sum(len(marks) >= box and marks[box - 1] == '~' for box in (1, 2, 4)),
    'calibration_scored_boxes': [1, 2, 4], 'calibration_excluded_boxes': [3],
    'source_rows': len(rows), 'source_tiers': dict(collections.Counter(c[4] for c in rows)),
    'source_statuses': dict(collections.Counter(c[8] for c in rows)),
    'malformed_rows': sum(len(c) != 13 for c in rows),
    'frozen_summary_sha256': __import__('hashlib').sha256(blob('.ufo/evidence/round-12/BashWitness/summary.json')).hexdigest()}, indent=2, sort_keys=True))
