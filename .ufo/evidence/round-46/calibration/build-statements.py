#!/usr/bin/env python3
"""Write statements.json: the 22 frozen standing statements of the round-46 C1 (calibration) counter.

Each statement names a row id of a SCORECARD table type (`cap` = `| Capability |` tables, `axis` =
`| Axis | Score |` tables), the command whose output the row's evidence cell restates, the regex that
picks the printed line, and (optionally) the tool whose sha256 prefix the row pins.
"""
import json
import os

D = os.path.dirname(os.path.abspath(__file__))
CMD_D = ('git show "$REV:tools/mutate-and-run.sh" | python3 -c \'import re,sys; '
         'n=len(re.findall(r"^#   (?:js|bash)-\\S+\\s+\\S+\\s+\\d+/\\d+",sys.stdin.read(),re.M)); '
         'print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))\'')


def cap(sid, argv, obs, cmd_text, sha=None, cwd='clone', timeout=900, what=None, first=None):
    return dict(id=sid, kind='cap', argv=argv, obs=obs, cmd_text=cmd_text, sha_file=sha, cwd=cwd,
                timeout=timeout, what=what, first=first)


S = [
    cap('sources-registry', ['bash', '.ufo/evidence/kaika-round-1/sources-census-v2.sh'], 'census',
        'bash .ufo/evidence/kaika-round-1/sources-census-v2.sh', timeout=300),
    cap('mutation sweep runner', ['bash', 'tools/mutate-and-run.sh', '--selftest'],
        r'^(MUTATE_SELFTEST: \d+/\d+ pass)', 'bash tools/mutate-and-run.sh --selftest', sha='tools/mutate-and-run.sh', timeout=1800),
    cap('six-leg regression ledger', ['bash', 'tools/mutate-and-run.sh', '--regression', '--workdir', '{work}/regression-wd'],
        r'^(REGRESSION: \w+ \(cases=\d+ passed=\d+)', 'bash tools/mutate-and-run.sh --regression', cwd='mirror', timeout=2700),
    cap('repeated pristine-control gate', ['python3', 'tools/repeat-control.py', '--selftest'],
        r'^(SELFTEST: PASS \(\d+ cases\))', 'python3 tools/repeat-control.py --selftest', sha='tools/repeat-control.py'),
    cap('six-leg content-disposition probe', ['python3', 'tools/pin-disposition.py', '--selftest'],
        r'^(SELFTEST: PASS \(\d+/\d+\))', 'python3 tools/pin-disposition.py --selftest', sha='tools/pin-disposition.py'),
    cap('exposed witness provenance correction', ['python3', 'tools/witness-metadata.py', '--selftest'],
        r'^(SELFTEST: PASS \d+/\d+)', 'python3 tools/witness-metadata.py --selftest', sha='tools/witness-metadata.py'),
    cap('effective expectation reconciliation', ['python3', 'tools/evidence-disposition.py', '--selftest'],
        r'^(SELFTEST: PASS \(\d+/\d+\))', 'python3 tools/evidence-disposition.py --selftest', sha='tools/evidence-disposition.py'),
    cap('retained invocation-context gate', ['python3', '.ufo/evidence/round-15/verify.py', '--rev', '7650fe4db89f3a706aed63d048ac47e02289cc72'],
        r'^selftest-new-full-count: PASS summary (SELFTEST: PASS \(\d+/\d+\))',
        'python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72', sha='.ufo/evidence/round-15/verify.py'),
    cap('hermetic env-differential probe', ['python3', 'tools/env-diff.py', '--selftest'],
        r'^(ENVDIFF_SELFTEST: \d+/\d+ pass)', 'python3 tools/env-diff.py --selftest', sha='tools/env-diff.py'),
    cap('callback-authoritative wave accounting', ['python3', 'tools/wave-accounting.py', '--selftest'],
        r'^(ACCOUNTING_SELFTEST: \d+/\d+ pass)', 'python3 tools/wave-accounting.py --selftest', sha='tools/wave-accounting.py'),
    cap('required-command-receipt-binding', ['python3', 'tools/command-binding.py', '--selftest'],
        r'^(COMMAND_BINDING_SELFTEST: \d+/\d+ pass)', 'python3 tools/command-binding.py --selftest', sha='tools/command-binding.py'),
    cap('refusing-registry-replay', ['python3', 'tools/registry-replay.py', '--selftest'],
        r'^(REGISTRY_REPLAY_SELFTEST: \d+/\d+ pass)', 'python3 tools/registry-replay.py --selftest', sha='tools/registry-replay.py'),
    cap('mutation report interop', ['python3', 'tools/mte-interop.py', '--selftest'],
        r'^(MTE_SELFTEST: \d+/\d+ pass)', 'python3 tools/mte-interop.py --selftest', sha='tools/mte-interop.py'),
    cap('tally-audit-v2 runner audit', ['python3', 'tools/tally-audit-v2.py', '--selftest'],
        r'^(TALLY_AUDIT_V2_SELFTEST: \d+/\d+ pass)', 'python3 tools/tally-audit-v2.py --selftest', sha='tools/tally-audit-v2.py'),
    cap('tally-audit-v3 runner audit', ['python3', 'tools/tally-audit-v3.py', '--selftest'],
        r'^(TALLY_AUDIT_V3_SELFTEST: \d+/\d+ pass)', 'python3 tools/tally-audit-v3.py --selftest', sha='tools/tally-audit-v3.py', timeout=1800),
    cap('bounded ANSI-C code_view', ['python3', 'tools/tally-audit-v3.py', '--selftest'],
        r'^(TALLY_AUDIT_V3_SELFTEST: \d+/\d+ pass)', 'python3 tools/tally-audit-v3.py --selftest', sha='tools/tally-audit-v3.py', timeout=1800),
    cap('write-path-census-v2', ['python3', 'tools/write-path-census-v2.py', '--selftest'],
        r'^(WRITE_CENSUS_V2_SELFTEST: .*)$', 'python3 tools/write-path-census-v2.py --selftest', sha='tools/write-path-census-v2.py'),
    cap('write-path census destination resolution', ['python3', 'tools/write-path-census-v3.py', '--selftest'],
        r'^(WRITE_CENSUS_V3_SELFTEST: .*)$', 'python3 tools/write-path-census-v3.py --selftest', sha='tools/write-path-census-v3.py'),
    cap('staged-id adoption guard', ['python3', 'tools/staged-id-guard.py', '--selftest'],
        r'^(STAGED_ID_GUARD_SELFTEST: cases=\d+ failed=\d+)', 'python3 tools/staged-id-guard.py --selftest', sha='tools/staged-id-guard.py'),
    dict(id='depth', kind='axis', argv=['bash', '-c', CMD_D], obs=r'depth_score=(\d+)', cmd_text='command D', sha_file=None, cwd='clone', timeout=300,
         what=None, first=None),
    dict(id='calibration', kind='axis', argv=['python3', '.ufo/evidence/round-21/coldread/measure.py', '--repo', '{clone}', '--rev', '{rev}'],
         obs='monitor', cmd_text='python3 .ufo/evidence/round-21/coldread/measure.py --repo R --rev REV', sha_file=None, cwd='clone',
         timeout=900, what=None, first=None),
    dict(id='freshness', kind='axis', argv=['python3', '.ufo/evidence/round-45/freshness/measure.py', '--lane', '{clone}', '--rev', '{rev}'],
         obs=r'\bscore=(\d+)\b', cmd_text='python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev REV', sha_file=None,
         cwd='clone', timeout=300, what=None, first=None),
]
assert len(S) == 22 and len({s['id'] + s['kind'] for s in S}) == 22
with open(os.path.join(D, 'statements.json'), 'w', encoding='utf-8') as fh:
    json.dump(dict(statements=S), fh, indent=1, ensure_ascii=False)
    fh.write('\n')
print('wrote statements.json with %d statements' % len(S))
