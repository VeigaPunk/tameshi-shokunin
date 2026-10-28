#!/usr/bin/env python3
"""A9: two readers for one heading - a gapped one (sorts first) plus a clean one."""
import json, sys
sys.path.insert(0, '/fast/scratch/hyaku/tameshi-r55/T55W3MutReader')
import run as R, run2 as R2
H1 = R.H1
def main():
    R.setup()
    secs, _ = R.section_shas()
    R.write_res([])
    R.build_fixtures(secs, {})
    # gapped twin that sorts before T55W3FIX00.json
    d = {'heading': H1, 'cand': R.C0, 'section_sha256': secs[H1]['sha256'],
         'findings': [{'quote': H1, 'why': 'fixture: one unadjudicated finding'}]}
    (R.W / 'T55W3AAA00.json').write_text(json.dumps(d, indent=1, ensure_ascii=False) + '\n', 'utf-8')
    (R.W / 'T55W3AAA00.md').write_text('# gapped twin\n', 'utf-8')
    R2.capture('A9-gapped-twin-blocks', (H1,))
    R.git('checkout', '--', R.LEDGER)
    R.build_fixtures(secs, {})
main()
