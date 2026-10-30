import ast
import collections
import hashlib
import json
import subprocess

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = '8063d0a551fc5b3cb5a2d397da7353af53444534'
BASE = '2a32aa8228d5f86a85c81a923a3148bf792a9538'
reads = []
duplicates = []
def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            duplicates.append(key)
        result[key] = value
    return result

def blob(path):
    command = ['git', '-C', LANE, 'show', REV + ':' + path]
    result = subprocess.run(command, capture_output=True, check=True)
    reads.append({'command': command, 'returncode': result.returncode,
                  'bytes': len(result.stdout), 'sha256': hashlib.sha256(result.stdout).hexdigest()})
    return result.stdout

def obj(path):
    return json.loads(blob(path), object_pairs_hook=pairs)

panel_path = '.ufo/evidence/round-58/c1/panel.json'
panel_raw = blob(panel_path)
panel = json.loads(panel_raw, object_pairs_hook=pairs)
module = ast.parse(blob('.ufo/evidence/round-58/c1/measure.py'))
constants = {}
for node in module.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in ('PANEL_SHA256', 'PANEL_ALLOWED', 'BASE'):
                constants[target.id] = ast.literal_eval(node.value)
defects = obj('.ufo/evidence/round-58/c1/defects.json')['defects']
ledger = obj('corpus/routed-defects.json')['defects']
results = obj('.ufo/waves/round-58/w1-results.json')['results']
ids = [d['id'] for d in defects]
seats = sorted(set(d['seat'] for d in panel['detail'].values()))
listed = collections.Counter(r['name'] for r in results)
seat_data = {}
seat_checks = []
for seat in seats:
    raw = blob('.ufo/waves/round-58/w1/' + seat + '.json')
    data = json.loads(raw, object_pairs_hook=pairs)
    seat_data[seat] = data
    seat_checks.append({'seat': seat, 'sha256': hashlib.sha256(raw).hexdigest(),
                        'expected_sha256': panel['files'].get(seat),
                        'hash_match': hashlib.sha256(raw).hexdigest() == panel['files'].get(seat),
                        'results_occurrences': listed[seat], 'self_identity_match': data.get('seat') == seat})
row_counts = collections.Counter(r['id'] for r in ledger)
seat_id_counts = collections.Counter(rid for data in seat_data.values() for rid in data['verdicts'])
rows = {r['id']: r for r in ledger}
item_checks = []
for rid in ids:
    seat = panel['detail'][rid]['seat']
    verdict = seat_data[seat]['verdicts'].get(rid, {}).get('verdict')
    item_checks.append({'id': rid, 'seat': seat, 'panel_verdict': panel['verdicts'][rid],
                        'seat_verdict': verdict, 'verdict_match': verdict == panel['verdicts'][rid],
                        'seat_occurrences': seat_id_counts[rid], 'ledger_occurrences': row_counts[rid],
                        'status_at_base': rows[rid].get('status_at_base'),
                        'disagree': rows[rid].get('status_at_base') != panel['verdicts'][rid]})
disagreements = [r for r in item_checks if r['disagree']]
checks = {
    'panel_pin_matches': hashlib.sha256(panel_raw).hexdigest() == constants['PANEL_SHA256'],
    'base_matches': panel['base'] == BASE == constants['BASE'],
    'frozen_ids_unique_51': len(ids) == len(set(ids)) == 51,
    'verdict_ids_exact': set(panel['verdicts']) == set(ids),
    'detail_ids_exact': set(panel['detail']) == set(ids),
    'files_seats_exact': set(panel['files']) == set(seats),
    'no_duplicate_json_keys': not duplicates,
    'all_hashes_match': all(r['hash_match'] for r in seat_checks),
    'all_seats_named_once': all(r['results_occurrences'] == 1 for r in seat_checks),
    'all_seat_identities_match': all(r['self_identity_match'] for r in seat_checks),
    'all_verdicts_match': all(r['verdict_match'] for r in item_checks),
    'seat_ids_exact_once': set(seat_id_counts) == set(ids) and all(n == 1 for n in seat_id_counts.values()),
    'ledger_ids_once': all(row_counts[rid] == 1 for rid in ids),
    'disagreements_within_allowance': len(disagreements) <= constants['PANEL_ALLOWED'],
}
print(json.dumps({'revision': REV, 'axes': ['digest integrity', 'unique item coverage', 'seat provenance', 'calibrated disagreement accounting'],
                  'checks': checks, 'panel_sha256': hashlib.sha256(panel_raw).hexdigest(),
                  'constants': constants, 'ids': len(ids), 'seats': len(seats),
                  'disagreement_count': len(disagreements), 'panel_over': max(0, len(disagreements)-constants['PANEL_ALLOWED']),
                  'disagreements': disagreements, 'seat_checks': seat_checks,
                  'item_checks': item_checks, 'duplicate_json_keys': duplicates, 'reads': reads}, indent=2))
