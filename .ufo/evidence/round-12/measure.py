#!/usr/bin/env python3
"""Count round-12 artifact coverage at a revision, not inferred capability."""
import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--rev')
args = parser.parse_args()

def content(path):
    if args.rev:
        result = subprocess.run(['git', 'show', f'{args.rev}:{path}'], capture_output=True)
        return result.stdout.decode() if result.returncode == 0 else ''
    file = Path(path)
    return file.read_text() if file.is_file() else ''

rows = []
for line in content('corpus/SOURCES.md').splitlines():
    if re.match(r'^\|\s*S\d{3,}\s*\|', line):
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        rows.append(cells)
summary_text = content('.ufo/evidence/round-12/BashWitness/summary.json')
summary = json.loads(summary_text) if summary_text else {}
marks = re.findall(r'^- \[([x~ ])\] ', content('SHONEN.md'), re.M)
# Fixed adjudication: round-1 outside review excludes box 3 from score credit.
scored_boxes = (1, 2, 4)
calibration = 2 * sum(len(marks) >= box and marks[box - 1] == '~' for box in scored_boxes)
gate_paths = re.findall(r'^#   (?:js|bash)-\S+\s+(\S+)\s+\d+/\d+', content('tools/mutate-and-run.sh'), re.M)
print(json.dumps({
    'revision': args.rev or 'worktree',
    'repeat_control_artifact': int(bool(content('tools/repeat-control.py'))),
    'bash_witness_summary': summary,
    'source_rows': len(rows),
    'source_malformed': sum(len(row) != 11 for row in rows),
    'source_tiers': dict(sorted(Counter(row[3] for row in rows if len(row) == 11).items())),
    'source_status': dict(sorted(Counter(row[7] for row in rows if len(row) == 11).items())),
    'unique_recorded_gates': len(set(gate_paths)),
    'calibration_restraint_score': calibration,
    'calibration_scored_boxes': list(scored_boxes),
    'calibration_excluded_boxes': [3],
    'recorded_cases': len(re.findall(r'^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+', content('tools/mutate-and-run.sh'), re.M)),
}, indent=2, sort_keys=True))
