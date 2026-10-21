#!/usr/bin/env python3
"""Measure only the five frozen round-18 routed corrections (round 19).

0 measured; --check: 0 all five corrected, 1 at least one open;
2 could-not-evaluate; 64 usage. --selftest uses isolated public-CLI fixtures.
Reads revision-pinned blobs, never executes receipt argv. This is not a
cold-read/command-coverage ruler or a general claim-admission authority.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

REV18 = '4b7c6823a462f5ea2eafcb262275300a545f3ed7'
TOOLS18 = '921ef8077440f90d092aab4b9fdc750a45de1224'
PREFIX = '.ufo/evidence/round-19/'
GUARD = 'corpus/knowledge/guard-kill-closure.md'
CASE = 'corpus/knowledge/mutation-case-kumitate-sources-check.md'
LESSON = 'corpus/lessons/round-18.md'
SOURCES = 'corpus/SOURCES.md'
OLD_CHECKS = '.ufo/evidence/round-18/final/checks.json'
PROBES = '.ufo/evidence/round-18/final/probes.stdout'
WITNESS = PREFIX + 'bash-witness-selftest-complete.json'
MEASURE = PREFIX + 'round18-final-measure.json'
PATHS = (GUARD, CASE, LESSON, SOURCES, OLD_CHECKS, PROBES,
         WITNESS, PREFIX + 'bash-witness-selftest-complete.stdout',
         PREFIX + 'bash-witness-selftest-complete.stderr', MEASURE,
         PREFIX + 'round18-final-measure.stdout',
         PREFIX + 'round18-final-measure.stderr', PREFIX + 'sources-diff.txt')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def strict_json(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate-key')
            result[key] = value
        return result
    def constant(value):
        raise ValueError('nonfinite-json')
    return json.loads(raw, object_pairs_hook=unique, parse_constant=constant)


def clean_env():
    result = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    result.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
                  PYTHONDONTWRITEBYTECODE='1')
    return result


def receipt(data, path, argv):
    row = strict_json(data[path])
    if not isinstance(row, dict):
        return None
    if (row.get('argv') != argv or row.get('revision') != REV18
            or type(row.get('exit')) is not int or row['exit'] != 0):
        return None
    for stream in ('stdout', 'stderr'):
        expected_path = path.removesuffix('.json') + '.' + stream
        if row.get(stream) != expected_path or data.get(expected_path) is None:
            return None
        if row.get(stream + '_sha256') != digest(data[expected_path]):
            return None
    if data[row['stderr']] != b'':
        return None
    return data[row['stdout']]


def evaluate(data):
    rows = []
    def check(identifier, predicate):
        try:
            ok = bool(predicate())
        except (KeyError, IndexError, AttributeError, TypeError, ValueError, UnicodeError):
            ok = False
        rows.append({'id': identifier, 'status': 'corrected' if ok else 'open'})
    def text(path):
        return data[path].decode('utf-8')
    def guard():
        note = text(GUARD).split('## Erratum R18-1', 1)[1]
        old = strict_json(data[OLD_CHECKS])['probes']
        return ('line 2' in note and 'Effective verified-at:' in note
                and TOOLS18 in note and '18 mutation survivors' in note
                and old['revision'] == TOOLS18 and type(old['exit']) is int
                and old['exit'] == 0 and old['stdout_sha256'] == digest(data[PROBES])
                and b'DEFECT_PROBES: open=0 closed=11 total=11' in data[PROBES])
    def source():
        note = text(CASE).split('## Erratum R18-2', 1)[1]
        source_rows = [line.split('|') for line in text(SOURCES).splitlines()
                       if re.match(r'^\|\s*S008\s*\|', line)]
        return (len(source_rows) == 1 and len(source_rows[0]) == 13
                and source_rows[0][8].strip() == 'mined'
                and CASE in [part.strip() for part in source_rows[0][11].split(',')]
                and 'line 1' in note and REV18 in note and 'mined' in note)
    def arithmetic():
        note = text(LESSON).split('## Erratum R18-3', 1)[1]
        return ('five deleted table lines' in note
                and all(identifier in note for identifier in
                        ('S001', 'S008', 'S052', 'S056', 'S057'))
                and re.search(r'^25\s+5\s+corpus/SOURCES\.md$',
                              text(PREFIX + 'sources-diff.txt'), re.M) is not None)
    def witness():
        raw = receipt(data, WITNESS,
                      ['python3', 'tools/bash-witness-study.py', 'selftest'])
        note = text(LESSON).split('## Errata R18-4 / R18-5', 1)[1]
        row = strict_json(data[WITNESS])
        return (raw is not None and b'WITNESS_SELFTEST: 43/43 pass' in raw
                and b'VERDICT: PASS' in raw and 'failed raw invocation' in note
                and row.get('historical_receipt_preserved') is True
                and OLD_CHECKS + '#bash-witness-selftest' in row.get('supersedes', []))
    def measurement():
        argv = ['python3', '.ufo/evidence/round-18/measure.py', '--repo',
                '/home/vgpnk/Projects/shokunin/tameshi-shokunin', '--rev', REV18,
                '--explain']
        raw = receipt(data, MEASURE, argv)
        value = strict_json(raw)
        cold = value['coldread']
        note = text(LESSON).split('## Errata R18-4 / R18-5', 1)[1]
        return (value['revision'] == REV18 and value['rev_input'] == REV18
                and value['overrides_used'] is False and value['ledger_committed'] is True
                and type(cold['sections_covered']) is int and cold['sections_covered'] == 60
                and type(cold['sections_total']) is int and cold['sections_total'] == 60
                and cold['box3_full_page'] is True
                and type(value['calibration_restraint_score']) is int
                and value['calibration_restraint_score'] == 8
                and 'does not claim the receipt existed in round 18' in note)
    for identifier, predicate in zip(('R18-1', 'R18-2', 'R18-3', 'R18-4', 'R18-5'),
                                     (guard, source, arithmetic, witness, measurement)):
        check(identifier, predicate)
    return rows


def selftest():
    # Start with actual committed-format receipts but synthetic content; fixtures
    # are independent of the production corpus and run through the public CLI.
    data = {p: '' for p in PATHS}
    data[GUARD] = '## Erratum R18-1\nline 2 Effective verified-at: ' + TOOLS18 + ' 18 mutation survivors'
    data[CASE] = '## Erratum R18-2\nline 1 mined ' + REV18
    cells = ['S008', 'source', 'paper', 'A', 'scope', 'anchor', 'teaches',
             'mined', '2026-10-21', 'on-release', CASE]
    data[SOURCES] = '| ' + ' | '.join(cells) + ' |\n'
    data[LESSON] = ('## Erratum R18-3\nfive deleted table lines S001 S008 S052 S056 S057\n'
                    '## Errata R18-4 / R18-5\nfailed raw invocation; '
                    'does not claim the receipt existed in round 18')
    data[PROBES] = 'DEFECT_PROBES: open=0 closed=11 total=11\n'
    data[OLD_CHECKS] = json.dumps({'probes': {'revision': TOOLS18, 'exit': 0,
                                'stdout_sha256': digest(data[PROBES].encode())}})
    data[PREFIX + 'sources-diff.txt'] = '25\t5\tcorpus/SOURCES.md\n'
    def make_receipt(path, argv, stdout):
        out, err = path[:-5] + '.stdout', path[:-5] + '.stderr'
        data[out], data[err] = stdout, ''
        data[path] = json.dumps({'argv': argv, 'revision': REV18, 'exit': 0,
            'stdout': out, 'stderr': err, 'stdout_sha256': digest(stdout.encode()),
            'stderr_sha256': digest(b''), 'historical_receipt_preserved': True,
            'supersedes': [OLD_CHECKS + '#bash-witness-selftest']})
    make_receipt(WITNESS, ['python3', 'tools/bash-witness-study.py', 'selftest'],
                 'WITNESS_SELFTEST: 43/43 pass\nVERDICT: PASS\n')
    value = {'revision': REV18, 'rev_input': REV18, 'overrides_used': False,
             'ledger_committed': True, 'calibration_restraint_score': 8,
             'coldread': {'sections_covered': 60, 'sections_total': 60,
                          'box3_full_page': True}}
    make_receipt(MEASURE, ['python3', '.ufo/evidence/round-18/measure.py', '--repo',
                 '/home/vgpnk/Projects/shokunin/tameshi-shokunin', '--rev', REV18,
                 '--explain'], json.dumps(value))
    cases = [('pristine', data, 0, [])]
    for index, path in enumerate((GUARD, CASE, PREFIX + 'sources-diff.txt', WITNESS, MEASURE), 1):
        mutant = dict(data); mutant[path] = ''
        cases.append(('missing-' + str(index), mutant, 1, ['R18-' + str(index)]))
    for name, field, replacement in [('wrong-argv','argv',['python3','bad']),
                                    ('wrong-rev','revision','a'*40),
                                    ('bool-exit','exit',False), ('usage-exit','exit',64),
                                    ('wrong-digest','stdout_sha256','0'*64),
                                    ('wrong-path','stdout','/etc/passwd'),
                                    ('unpreserved','historical_receipt_preserved',False),
                                    ('unsuperseded','supersedes',[])]:
        mutant = dict(data); row = json.loads(mutant[WITNESS]); row[field] = replacement
        mutant[WITNESS] = json.dumps(row)
        cases.append((name, mutant, 1, ['R18-4']))
    mutant = dict(data); mutant[PREFIX+'bash-witness-selftest-complete.stderr'] = 'error'
    cases.append(('stderr-tamper', mutant, 1, ['R18-4']))
    mutant = dict(data); mutant[WITNESS] = '{"exit":0,"exit":64}'
    cases.append(('duplicate-key', mutant, 1, ['R18-4']))
    mutant = dict(data); mutant[WITNESS] = '{"exit":NaN}'
    cases.append(('nonfinite', mutant, 1, ['R18-4']))
    failed = 0
    with tempfile.TemporaryDirectory(prefix='tameshi-r19-ruler-', dir='/tmp') as temp:
        fixture = Path(temp) / 'snapshot.json'
        for name, snapshot, expected_exit, expected_open in cases:
            fixture.write_text(json.dumps(snapshot), encoding='utf-8')
            run = subprocess.run([sys.executable, __file__, '--snapshot', str(fixture), '--check'],
                                 env=clean_env(), capture_output=True, timeout=30)
            result = json.loads(run.stdout)
            opened = [r['id'] for r in result['rows'] if r['status'] == 'open']
            ok = run.returncode == expected_exit and opened == expected_open
            failed += not ok
            print('CASE', name, 'PASS' if ok else 'FAIL', 'exit='+str(run.returncode), 'open='+','.join(opened))
    print(f'SELFTEST: {len(cases)-failed}/{len(cases)}')
    return 1 if failed else 0


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(64, message + '\n')


def main():
    parser = Parser(description=__doc__)
    parser.add_argument('--rev'); parser.add_argument('--repo', default=str(Path(__file__).resolve().parents[3]))
    parser.add_argument('--snapshot'); parser.add_argument('--check', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if bool(args.rev) == bool(args.snapshot):
        parser.error('choose --rev REV or --snapshot FILE')
    try:
        if args.snapshot:
            snapshot = strict_json(Path(args.snapshot).read_bytes())
            if not isinstance(snapshot, dict) or any(not isinstance(v, str) for v in snapshot.values()):
                raise ValueError('snapshot must map paths to text')
            data = {p: snapshot[p].encode() if p in snapshot else None for p in PATHS}
        else:
            if not re.fullmatch('[0-9a-f]{40}', args.rev):
                raise ValueError('revision must be full lowercase commit hash')
            valid = subprocess.run(['git', '-C', args.repo, 'cat-file', '-e', args.rev+'^{commit}'],
                                   env=clean_env(), capture_output=True, timeout=30)
            if valid.returncode:
                raise ValueError('revision missing')
            data = {}
            for path in PATHS:
                run = subprocess.run(['git', '-C', args.repo, 'show', args.rev+':'+path],
                                     env=clean_env(), capture_output=True, timeout=30)
                data[path] = run.stdout if run.returncode == 0 else None
        rows = evaluate(data)
        corrected = sum(row['status'] == 'corrected' for row in rows)
        print(json.dumps({'revision': args.rev, 'ruler_sha256': digest(Path(__file__).read_bytes()),
                          'corrected': corrected, 'open': 5-corrected, 'total': 5, 'rows': rows,
                          'inputs': {p: digest(raw) if raw is not None else None for p, raw in data.items()}},
                         indent=2, sort_keys=True))
        return int(args.check and corrected != 5)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
