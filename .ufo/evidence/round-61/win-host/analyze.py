#!/usr/bin/env python3
"""analyze.py — per-section passing-entry map at a rev, via the batched cache.

For each SKILL.md section: the ledger entries that PASS entry_reason at the
rev (credited) and the union of input paths across those passing entries.
Projected effect of editing a file set F: a section fails iff every passing
entry records >=1 path in F. Emits JSON for the rekey planner.
"""
import importlib.util
import json
import sys
from pathlib import Path

SCRATCH = Path(__file__).resolve().parent
import importlib.util as _ilu  # noqa: E402
_pspec = _ilu.spec_from_file_location('portable', SCRATCH / 'coldread-precheck-portable.py')
P = _ilu.module_from_spec(_pspec)
sys.modules['portable'] = P
_pspec.loader.exec_module(P)

EDITED = {'SCORECARD.md', 'LOG.md', 'corpus/SOURCES.md'}


def main():
    repo = Path(sys.argv[1]).resolve()
    rev = sys.argv[2]
    out_file = sys.argv[3]
    work = SCRATCH / 'work-analyze'
    module = P.load_frozen(repo)
    res = module.resolve_commit(str(repo), rev)
    assert res is not None
    rev = res
    paths, ledger_raw = P.needed_paths(module, repo, rev)
    skill_raw = module.blob(str(repo), rev, 'SKILL.md')
    byte_cache, stats = P.prefetch(repo, rev, paths, work, 2000)
    mode_map = P.build_mode_map(repo, rev)
    probe_log = {'blob_hits': 0, 'blob_tracked_misses': 0, 'mode_hits': 0,
                 'mode_from_bytes': 0}
    orig_blob, orig_mode = P.install_cache(module, repo, rev, byte_cache,
                                           mode_map, probe_log)
    try:
        ledger = json.loads(ledger_raw.decode('utf-8', 'surrogateescape'))
        sections = module.sectionize(skill_raw)
        by_sha = {}
        for i, entry in enumerate(ledger['entries']):
            if isinstance(entry, dict) and isinstance(entry.get('sha256'), str):
                by_sha.setdefault(entry['sha256'], []).append(i)
        plan = []
        repo_s = str(repo)
        for sec in sections:
            idxs = by_sha.get(sec['sha256'], [])
            passing = []
            for i in idxs:
                entry = ledger['entries'][i]
                if module.entry_reason(repo_s, rev, entry, True) is None:
                    passing.append(i)
            view_union = {}
            for i in passing:
                v = module.inputs_view(ledger['entries'][i]) or {}
                for k in v:
                    view_union[k] = v[k]
            hits_edited = sorted(view_union.keys() & EDITED)
            survives = bool(passing) and not hits_edited
            plan.append({
                'heading': sec['heading'], 'start': sec['start'],
                'entries_total': len(idxs), 'entries_passing': passing,
                'credited_now': bool(passing),
                'survives_edits': survives,
                'passing_input_union': sorted(view_union.keys()),
                'edited_hits': hits_edited,
            })
        need = [p for p in plan if (not p['credited_now']) or (not p['survives_edits'])]
        result = {
            'rev': rev,
            'sections_total': len(sections),
            'credited_now': sum(1 for p in plan if p['credited_now']),
            'projected_credited_after_edits': sum(1 for p in plan if p['credited_now'] and p['survives_edits']),
            'need_rekey_count': len(need),
            'need_rekey': need,
            'all': plan,
        }
        Path(out_file).write_text(json.dumps(result, indent=1, ensure_ascii=True),
                                  encoding='utf-8')
        print('sections=%d credited_now=%d projected_after=%d need_rekey=%d'
              % (result['sections_total'], result['credited_now'],
                 result['projected_credited_after_edits'],
                 result['need_rekey_count']))
        for p in need:
            print('NEED %-70s credited_now=%s passing=%d edited_hits=%s'
                  % (p['heading'][:70], p['credited_now'],
                     len(p['entries_passing']), ','.join(p['edited_hits']) or '-'))
    finally:
        module.cat_file_blob = orig_blob
        module.ls_tree_mode = orig_mode


if __name__ == '__main__':
    main()
