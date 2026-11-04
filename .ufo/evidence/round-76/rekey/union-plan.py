#!/usr/bin/env python3
"""union-plan.py — per-section ALL-entry input union for the 18 rekey sections."""
import importlib.util as ilu
import json
import sys
from pathlib import Path

SCRATCH = Path(__file__).resolve().parent
LANE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
REV = sys.argv[3] if len(sys.argv) > 3 else 'HEAD'

spec = ilu.spec_from_file_location('portable', SCRATCH / 'coldread-precheck-portable.py')
P = ilu.module_from_spec(spec)
sys.modules['portable'] = P
spec.loader.exec_module(P)

module = P.load_frozen(str(LANE))
res = module.resolve_commit(str(LANE), REV)
paths, ledger_raw = P.needed_paths(module, LANE, res)
byte_cache, stats = P.prefetch(LANE, res, paths, SCRATCH / 'work-analyze', 2000)
mode_map = P.build_mode_map(LANE, res)
probe_log = {'blob_hits': 0, 'blob_tracked_misses': 0, 'mode_hits': 0,
             'mode_from_bytes': 0}
orig_blob, orig_mode = P.install_cache(module, str(LANE), res, byte_cache,
                                       mode_map, probe_log)
try:
    ledger = json.loads(ledger_raw.decode('utf-8', 'surrogateescape'))
    skill_raw = module.blob(str(LANE), res, 'SKILL.md')
    sections = module.sectionize(skill_raw)
    by_sha = {}
    for i, entry in enumerate(ledger['entries']):
        if isinstance(entry, dict) and isinstance(entry.get('sha256'), str):
            by_sha.setdefault(entry['sha256'], []).append(i)
    plan = json.loads(Path(SCRATCH / 'rekey-plan.json').read_text(encoding='utf-8'))
    need_headings = {p['heading'] for p in plan['need_rekey']}
    out = []
    for sec in sections:
        if sec['heading'] not in need_headings:
            continue
        idxs = by_sha.get(sec['sha256'], [])
        union = {}
        src_entries = []
        for i in idxs:
            e = ledger['entries'][i]
            v = module.inputs_view(e) or {}
            for k in v:
                union[k] = v[k]  # old recorded hash; re-pinned at pin rev later
            src_entries.append(i)
        missing_at_rev = [k for k in sorted(union) if k not in mode_map]
        out.append({
            'heading': sec['heading'], 'start': sec['start'],
            'sha256': sec['sha256'], 'end': sec['end'],
            'src_entries': src_entries,
            'union_paths': sorted(union.keys()),
            'union_size': len(union),
            'not_in_tree_at_rev': missing_at_rev,
            'record_files': sorted(set(union) & {'SCORECARD.md', 'LOG.md',
                                                 'corpus/SOURCES.md',
                                                 'corpus/QUALITY.md',
                                                 'PROVINCE.md', 'README.md'}),
        })
        print('%-72s entries=%3d union=%5d not_in_tree=%d record_files=%s'
              % (sec['heading'][:72], len(idxs), len(union), len(missing_at_rev),
                 out[-1]['record_files'] or '-'))
    OUT.write_text(json.dumps({'rev': res, 'sections': out}, indent=1,
                              ensure_ascii=True), encoding='utf-8')
finally:
    module.cat_file_blob = orig_blob
    module.ls_tree_mode = orig_mode
