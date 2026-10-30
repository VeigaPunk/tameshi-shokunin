#!/usr/bin/env python3
"""Read-only excerpt audit; emits evidence, never executes lane code."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
WAVE = ROOT / '.ufo/waves/round-58/w1'
BASE = '2a32aa8228d5f86a85c81a923a3148bf792a9538'

def load(path):
    return json.loads(path.read_text())

def norm(text):
    return ' '.join(text.split())

def show(rev, path):
    cmd = ['git', '-C', str(ROOT), 'show', rev + ':' + path]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return {'command': cmd, 'returncode': p.returncode,
            'stdout': p.stdout, 'stderr': p.stderr}

keys = load(ROOT / '.ufo/evidence/round-58/c1/keys.json')
defects = {r['id']: r for r in load(ROOT / '.ufo/evidence/round-58/c1/defects.json')['defects']}
tree = ast.parse((ROOT / '.ufo/evidence/round-58/c1/measure.py').read_text())
ack = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ACK_WORDS' for t in n.targets))
files = []
fixed = []
missing = []
for i in range(1, 14):
    path = WAVE / ('T58W1Verify%02d.json' % i)
    if not path.exists():
        missing.append(path.name)
        continue
    blob = path.read_bytes()
    data = json.loads(blob)
    files.append({'path': str(path), 'sha256': hashlib.sha256(blob).hexdigest()})
    for row in data.get('rows', []):
        if row.get('status_now_proposed') == 'fixed':
            fixed.append((path.name, row))
# Spread across available source seats, then fill to twelve in source order.
selected = []
seen = set()
for source, row in fixed:
    if source not in seen:
        selected.append((source, row)); seen.add(source)
for source, row in fixed:
    if len(selected) >= 12:
        break
    if not any(r['id'] == row['id'] for _, r in selected):
        selected.append((source, row))
rows = []
for source, row in selected:
    results = []
    for e in row.get('evidence', []):
        path, excerpt, lines = e.get('path', ''), e.get('excerpt', ''), str(e.get('lines', ''))
        ex = norm(excerpt)
        base = show(BASE, path)
        routed = show(defects[row['id']]['routed_at'], path)
        commit = show(row.get('commit', ''), path)
        m = re.fullmatch(r'(\d+)(?:-(\d+))?', lines)
        a, b = (int(m[1]), int(m[2] or m[1])) if m else (0, 0)
        text = base['stdout'].split('\n')
        selected_text = '\n'.join(text[a-1:b]) if 1 <= a <= b <= len(text) else ''
        hits = [k for k in keys[row['id']] if re.search(r'(?<![\w-])' + re.escape(k) + r'(?![\w-])', ex, re.I)]
        words = [word for word in ack if word in ex.lower()]
        checks = {
            'normalized_length_15_400': 15 <= len(ex) <= 400,
            'present_in_named_base_lines': base['returncode'] == 0 and bool(selected_text) and ex in norm(selected_text),
            'whole_key_token_in_excerpt': bool(hits),
            'absent_from_routed_path': routed['returncode'] != 0 or ex not in norm(routed['stdout']),
            'no_ack_words': not words,
            'counter_lines_syntax': bool(re.fullmatch(r'\d+-\d+', lines)),
            'counter_max_span': bool(m) and 1 <= a <= b and b-a <= 30,
        }
        results.append({'evidence': e, 'checks': checks, 'pass': all(checks.values()),
                        'length_raw': len(excerpt), 'length_normalized': len(ex),
                        'key_hits': hits, 'ack_hits': words,
                        'base_command': base['command'], 'base_returncode': base['returncode'],
                        'base_selected_output': selected_text,
                        'routed_command': routed['command'], 'routed_returncode': routed['returncode'],
                        'routed_excerpt_present': ex in norm(routed['stdout']) if routed['returncode'] == 0 else False,
                        'routed_output_sha256': hashlib.sha256(routed['stdout'].encode()).hexdigest(),
                        'routed_stderr': routed['stderr'],
                        'commit_command': commit['command'], 'commit_returncode': commit['returncode'],
                        'commit_excerpt_present_anywhere': commit['returncode'] == 0 and ex in norm(commit['stdout']),
                        'commit_stderr': commit['stderr']})
    rows.append({'id': row['id'], 'source': source, 'status_at_base': row.get('status_at_base'),
                 'commit': row.get('commit'), 'pass': bool(results) and all(e['pass'] for e in results),
                 'any_usable_evidence': any(e['pass'] for e in results), 'evidence': results})
print(json.dumps({'seat': 'T58W1RevExcerpts', 'base': BASE,
                  'axes': ['excerpt fidelity', 'whole-token relevance', 'historical novelty', 'counter compatibility'],
                  'lsp': 'Unavailable: xd://lsp returned No such tool; no semantic references claimed.',
                  'selection': 'First fixed row per available source seat, then earliest unselected fixed rows, capped at 12.',
                  'inputs': files, 'missing_inputs': missing, 'ack_words': ack,
                  'sample_size': len(rows), 'all_evidence_pass_rows': sum(r['pass'] for r in rows),
                  'any_usable_evidence_rows': sum(r['any_usable_evidence'] for r in rows), 'rows': rows}, indent=2))
