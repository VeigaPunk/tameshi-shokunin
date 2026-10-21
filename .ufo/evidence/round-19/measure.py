#!/usr/bin/env python3
"""Measure only the five frozen round-18 routed corrections (round 19).

0 measured; --check: 0 all five corrected, 1 at least one open;
2 could-not-evaluate; 64 usage. --selftest uses isolated public-CLI fixtures.
Reads revision-pinned blobs, never executes receipt argv. This is not a
cold-read/command-coverage ruler or a general claim-admission authority.
"""
import argparse
import datetime
from collections import Counter
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
TOOL_SHA18 = '8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12'
RUNNER_SHA18 = 'd22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b'
FREEZE_TIME = datetime.datetime.fromisoformat('2026-10-21T02:28:10-03:00')
DIFF_COMMAND = ('git diff --numstat 183f87b899e6cae46be98d251cbc87fb5118f6ca '
                + REV18 + ' -- corpus/SOURCES.md')
PREFIX = '.ufo/evidence/round-19/'
GUARD = 'corpus/knowledge/guard-kill-closure.md'
CASE = 'corpus/knowledge/mutation-case-kumitate-sources-check.md'
LESSON = 'corpus/lessons/round-18.md'
SOURCES = 'corpus/SOURCES.md'
OLD_CHECKS = '.ufo/evidence/round-18/final/checks.json'
PROBES = '.ufo/evidence/round-18/final/probes.stdout'
WITNESS = PREFIX + 'bash-witness-selftest-complete.json'
MEASURE = PREFIX + 'round18-final-measure.json'
INSTRUMENT = PREFIX + 'round18-final-measure-instrument.json'
MEASURE_SHA18 = '7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37'
SOURCE_BEFORE = PREFIX + 'source-baseline.txt'
SOURCE_AFTER = PREFIX + 'source-round18-final.txt'
SOURCE_PINS = {
    SOURCE_BEFORE: 'ac82b2df0ffd44f4e3e74e90cdae2a2eac6bc72ed557dd428c45397f97c828d5',
    SOURCE_AFTER: '018ee9a86500efc6d07ea141d20c7de6b2ec76e5e808ffbf12508ada46a84e0e',
}
OLD_TALLY = '.ufo/evidence/round-18/final/bash-witness.stdout'
PATHS = (GUARD, CASE, LESSON, SOURCES, OLD_CHECKS, PROBES, INSTRUMENT,
         SOURCE_BEFORE, SOURCE_AFTER, OLD_TALLY,
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
    recorded = datetime.datetime.fromisoformat(row.get('recorded_at', ''))
    if recorded.tzinfo is None or recorded < FREEZE_TIME:
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


def compare_sources(before, after):
    """Compare row identity/cells and net retained non-row lines, not subjects."""
    fields = ('id', 'source', 'kind', 'tier', 'scope', 'anchor', 'teaches',
              'status', 'opened', 'recheck', 'used-by')
    def parse(raw):
        rows, other = {}, []
        for line in raw.decode('utf-8').splitlines():
            if re.match(r'^\|\s*S[0-9]{3,}\s*\|', line):
                cells = [part.strip() for part in line.split('|')[1:-1]]
                if len(cells) != 11 or cells[0] in rows:
                    raise ValueError('source-row-malformed-or-duplicate')
                rows[cells[0]] = dict(zip(fields, cells))
            else:
                other.append(line)
        return rows, Counter(other)
    old, old_other = parse(before)
    new, new_other = parse(after)
    changes = {identifier: [f for f in fields if old[identifier][f] != new[identifier][f]]
               for identifier in sorted(old.keys() & new.keys()) if old[identifier] != new[identifier]}
    return {
        'before_rows': len(old), 'after_rows': len(new),
        'changed': changes, 'changed_cells': sum(map(len, changes.values())),
        'removed': sorted(old.keys() - new.keys()),
        'added': sorted(new.keys() - old.keys()),
        'immutable_changes': [(i, f) for i, fs in changes.items() for f in fs
                              if f not in ('status', 'recheck', 'used-by')],
        'nonrow_deleted': list((old_other - new_other).elements()),
    }


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
                and PROBES in note and TOOLS18 in note and '18 mutation survivors' in note
                and 'Landed-tip results: PENDING (filled by L1 after landing).'
                in text(GUARD).split('## Erratum R18-1', 1)[0]
                and old['revision'] == TOOLS18 and type(old['exit']) is int
                and old['exit'] == 0 and old['stdout_sha256'] == digest(data[PROBES])
                and b'DEFECT_PROBES: open=0 closed=11 total=11' in data[PROBES])
    def source():
        note = text(CASE).split('## Erratum R18-2', 1)[1]
        source_rows = [line.split('|') for line in text(SOURCES).splitlines()
                       if re.match(r'^\|\s*S008\s*\|', line)]
        pinned_rows = [line.split('|') for line in text(SOURCE_AFTER).splitlines()
                       if re.match(r'^\|\s*S008\s*\|', line)]
        return (len(source_rows) == 1 and len(source_rows[0]) == 13
                and len(pinned_rows) == 1 and len(pinned_rows[0]) == 13
                and digest(data[SOURCE_AFTER]) == SOURCE_PINS[SOURCE_AFTER]
                and all(source_rows[0][i].strip() == pinned_rows[0][i].strip()
                        for i in (1, 2, 3, 4, 5, 6, 7, 9))
                and source_rows[0][8].strip() == 'mined'
                and source_rows[0][9].strip() == '2026-10-19'
                and CASE in [part.strip() for part in source_rows[0][11].split(',')]
                and 'line 1' in note and REV18 in note and 'mined' in note
                and '**queued**' in text(CASE).split('## Erratum R18-2', 1)[0])
    def arithmetic():
        note = text(LESSON).split('## Erratum R18-3', 1)[1].split('\n## ', 1)[0]
        comparison = compare_sources(data[SOURCE_BEFORE], data[SOURCE_AFTER])
        expected = {i: ['used-by'] for i in ('S001', 'S052', 'S056', 'S057')}
        expected['S008'] = ['status', 'used-by']
        return ('five deleted table lines' in note and DIFF_COMMAND in note
                and all(digest(data[path]) == pin for path, pin in SOURCE_PINS.items())
                and comparison['changed'] == expected and comparison['changed_cells'] == 6
                and not comparison['removed'] and not comparison['immutable_changes']
                and not comparison['nonrow_deleted']
                and comparison['before_rows'] == 62 and comparison['after_rows'] == 76
                and set(re.findall(r'\bS[0-9]{3,}\b', note)) == set(expected)
                and 'deletions = the four allowed used-by cells only'
                in text(LESSON).split('## Erratum R18-3', 1)[0]
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
                and raw == data[OLD_TALLY]
                and b'VERDICT: PASS' in raw and 'failed raw invocation' in note
                and row.get('historical_receipt_preserved') is True
                and row.get('tool_sha256') == TOOL_SHA18
                and row.get('runner_sha256') == RUNNER_SHA18
                and strict_json(data[OLD_CHECKS])['bash-witness-selftest']['exit'] == 64
                and strict_json(data[OLD_CHECKS])['bash-witness-selftest']['stdout_sha256'] == digest(b'')
                and type(row.get('supersedes')) is list
                and sorted(row['supersedes']) == sorted([
                    OLD_CHECKS + '#bash-witness-selftest',
                    PREFIX + 'bash-witness-selftest.json']))
    def measurement():
        argv = ['python3', '.ufo/evidence/round-18/measure.py', '--repo',
                '/home/vgpnk/Projects/shokunin/tameshi-shokunin', '--rev', REV18,
                '--explain']
        raw = receipt(data, MEASURE, argv)
        value = strict_json(raw)
        instrument = strict_json(data[INSTRUMENT])
        cold = value['coldread']
        note = text(LESSON).split('## Errata R18-4 / R18-5', 1)[1]
        return (value['revision'] == REV18 and value['rev_input'] == REV18
                and value['overrides_used'] is False and value['ledger_committed'] is True
                and value['ledger_source'] == 'rev' and value['trace_gate'] == 'strict'
                and instrument['receipt'] == MEASURE
                and instrument['receipt_sha256'] == digest(data[MEASURE])
                and instrument['revision'] == REV18
                and instrument['instrument'] == '.ufo/evidence/round-18/measure.py'
                and instrument['instrument_sha256'] == MEASURE_SHA18
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
    data[GUARD] = ('Landed-tip results: PENDING (filled by L1 after landing).\n'
                   '## Erratum R18-1\nline 2 Effective verified-at: '
                   + TOOLS18 + ' 18 mutation survivors ' + PROBES)
    data[CASE] = '**queued**\n## Erratum R18-2\nline 1 mined ' + REV18
    for path in SOURCE_PINS:
        data[path] = (Path(__file__).parent / Path(path).name).read_text(encoding='utf-8')
    data[SOURCES] = data[SOURCE_AFTER]
    data[LESSON] = ('deletions = the four allowed used-by cells only\n'
                    '## Erratum R18-3\nfive deleted table lines S001 S008 S052 S056 S057\n'
                    + DIFF_COMMAND + '\n## Errata R18-4 / R18-5\nfailed raw invocation; '
                    'does not claim the receipt existed in round 18')
    data[PROBES] = 'DEFECT_PROBES: open=0 closed=11 total=11\n'
    data[OLD_CHECKS] = json.dumps({'probes': {'revision': TOOLS18, 'exit': 0,
                                'stdout_sha256': digest(data[PROBES].encode())},
                                'bash-witness-selftest': {
                                    'exit': 64, 'stdout_sha256': digest(b'')}})
    data[PREFIX + 'sources-diff.txt'] = '25\t5\tcorpus/SOURCES.md\n'
    def make_receipt(path, argv, stdout):
        out, err = path[:-5] + '.stdout', path[:-5] + '.stderr'
        data[out], data[err] = stdout, ''
        data[path] = json.dumps({'argv': argv, 'revision': REV18, 'exit': 0,
            'stdout': out, 'stderr': err, 'stdout_sha256': digest(stdout.encode()),
            'stderr_sha256': digest(b''), 'historical_receipt_preserved': True,
            'tool_sha256': TOOL_SHA18, 'runner_sha256': RUNNER_SHA18,
            'recorded_at': '2026-10-21T06:00:00+00:00',
            'supersedes': [OLD_CHECKS + '#bash-witness-selftest',
                           PREFIX + 'bash-witness-selftest.json']})
    make_receipt(WITNESS, ['python3', 'tools/bash-witness-study.py', 'selftest'],
                 'WITNESS_SELFTEST: 43/43 pass\nVERDICT: PASS\n')
    data[OLD_TALLY] = data[WITNESS[:-5] + '.stdout']
    value = {'revision': REV18, 'rev_input': REV18, 'overrides_used': False,
             'ledger_committed': True, 'calibration_restraint_score': 8,
             'ledger_source': 'rev', 'trace_gate': 'strict',
             'coldread': {'sections_covered': 60, 'sections_total': 60,
                          'box3_full_page': True}}
    make_receipt(MEASURE, ['python3', '.ufo/evidence/round-18/measure.py', '--repo',
                 '/home/vgpnk/Projects/shokunin/tameshi-shokunin', '--rev', REV18,
                 '--explain'], json.dumps(value))
    data[INSTRUMENT] = json.dumps({
        'receipt': MEASURE, 'receipt_sha256': digest(data[MEASURE].encode()),
        'revision': REV18, 'instrument': '.ufo/evidence/round-18/measure.py',
        'instrument_sha256': MEASURE_SHA18})
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
                                    ('wrong-tool','tool_sha256','0'*64),
                                    ('wrong-runner','runner_sha256','0'*64),
                                    ('backdated','recorded_at','2026-10-21T02:00:00+00:00'),
                                    ('naive-time','recorded_at','2026-10-21T06:00:00'),
                                    ('unsuperseded','supersedes',[])]:
        mutant = dict(data); row = json.loads(mutant[WITNESS]); row[field] = replacement
        mutant[WITNESS] = json.dumps(row)
        cases.append((name, mutant, 1, ['R18-4']))
    mutant = dict(data); mutant[PREFIX+'bash-witness-selftest-complete.stderr'] = 'error'
    cases.append(('stderr-tamper', mutant, 1, ['R18-4']))
    mutant = dict(data); mutant[WITNESS] = '{"exit":64,' + data[WITNESS][1:]
    cases.append(('duplicate-key', mutant, 1, ['R18-4']))
    mutant = dict(data); mutant[WITNESS] = data[WITNESS][:-1] + ',"unused":NaN}'
    cases.append(('nonfinite', mutant, 1, ['R18-4']))
    mutant = dict(data)
    outpath = WITNESS[:-5] + '.stdout'
    mutant[outpath] += 'tampered\n'
    row = json.loads(mutant[WITNESS]); row['stdout_sha256'] = digest(mutant[outpath].encode())
    mutant[WITNESS] = json.dumps(row)
    cases.append(('rehashed-tally-tamper', mutant, 1, ['R18-4']))
    mutant = dict(data); mutant[OLD_TALLY] = ''
    cases.append(('missing-historical-tally', mutant, 1, ['R18-4']))
    mutant = dict(data); row = json.loads(mutant[WITNESS])
    row['supersedes'] = OLD_CHECKS + '#bash-witness-selftest'
    mutant[WITNESS] = json.dumps(row)
    cases.append(('string-supersedes', mutant, 1, ['R18-4']))
    mutant = dict(data); mutant[SOURCE_AFTER] = mutant[SOURCE_BEFORE]
    cases.append(('wrong-source-history', mutant, 1, ['R18-2', 'R18-3']))
    mutant = dict(data); mutant[SOURCE_AFTER] += '\n'
    cases.append(('source-snapshot-pin-tamper', mutant, 1, ['R18-2', 'R18-3']))
    mutant = dict(data); mutant[LESSON] = mutant[LESSON].replace(
        'five deleted table lines', 'S999 five deleted table lines')
    cases.append(('extra-changed-source-id', mutant, 1, ['R18-3']))
    for field, replacement in [('ledger_source', 'file'), ('trace_gate', 'legacy'),
                               ('overrides_used', True), ('revision', 'a'*40)]:
        mutant = dict(data); changed = dict(value); changed[field] = replacement
        outpath = MEASURE[:-5] + '.stdout'
        mutant[outpath] = json.dumps(changed)
        row = json.loads(mutant[MEASURE]); row['stdout_sha256'] = digest(mutant[outpath].encode())
        mutant[MEASURE] = json.dumps(row)
        instrument = json.loads(mutant[INSTRUMENT])
        instrument['receipt_sha256'] = digest(mutant[MEASURE].encode())
        mutant[INSTRUMENT] = json.dumps(instrument)
        cases.append(('measurement-' + field, mutant, 1, ['R18-5']))
    mutant = dict(data)
    source_lines = []
    for line in mutant[SOURCES].splitlines():
        if re.match(r'^\|\s*S008\s*\|', line):
            cells = line.split('|'); cells[3] = ' own-work '; line = '|'.join(cells)
        source_lines.append(line)
    mutant[SOURCES] = '\n'.join(source_lines) + '\n'
    cases.append(('foreign-source-identity', mutant, 1, ['R18-2']))
    for name, path, old, new, identifier in [
            ('wrong-effective-receipt', GUARD, PROBES,
             '.ufo/evidence/round-18/c2-probes-v2-183f87b.txt', 'R18-1'),
            ('removed-original-metadata', GUARD, 'Landed-tip results: PENDING', '', 'R18-1'),
            ('immutable-opened', SOURCES, '2026-10-19', '2026-10-21', 'R18-2'),
            ('moving-diff-bound', LESSON, DIFF_COMMAND,
             DIFF_COMMAND.replace(REV18, 'HEAD'), 'R18-3')]:
        mutant = dict(data); mutant[path] = mutant[path].replace(old, new)
        cases.append((name, mutant, 1, [identifier]))
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
                          'source_history': (compare_sources(data[SOURCE_BEFORE], data[SOURCE_AFTER])
                                             if data[SOURCE_BEFORE] is not None and data[SOURCE_AFTER] is not None else None),
                          'inputs': {p: digest(raw) if raw is not None else None for p, raw in data.items()}},
                         indent=2, sort_keys=True))
        return int(args.check and corrected != 5)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
