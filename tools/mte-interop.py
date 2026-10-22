#!/usr/bin/env python3
"""Frontier F1 report interop: tameshi ledger legs as mutation-testing-elements reports.

  mte-interop.py --check [--fleet-root DIR | --workdir DIR [--regression-stdout F]] [--emit DIR]
  mte-interop.py --selftest

--check runs `tools/mutate-and-run.sh --regression --keep` (or reads an existing
kept regression workdir given by --workdir), then for every leg it finds:
  1. emits one report in the mutation-testing-elements format (schema
     mutation-testing-report-schema 3.9.0, vendored and sha512-pinned in
     tools/vendor/): the pristine pinned target as `source`, one mutant per
     recorded defect, location computed from the defect's unique @old string,
     status mapped KILLED->Killed, SURVIVED->Survived, INCONCLUSIVE->RuntimeError;
  2. validates the report against the official JSON Schema (draft-07,
     python `jsonschema` package);
  3. computes the official metrics with the vendored mutation-testing-metrics
     3.9.0 library (node, `calculateMetrics`), not with tameshi's own code;
  4. compares the official mutationScore with tameshi's measured kill rate
     killed/(killed+survived)*100 and the official killed count and valid
     count with the leg's recorded ledger table (REGRESSION_TABLE line).
A leg conforms only when all three comparisons hold and the schema accepts it.

Lines: MTE_LEG <leg>: CONFORMS|FAILS (...) per leg, then
MTE_INTEROP: PASS|FAIL legs_conforming=N/M, or MTE_INTEROP: SETUP (<reason>).
Exit: 0 PASS (every leg found conforms, M >= 1) · 1 FAIL · 2 SETUP · 64 usage.
Needs python `jsonschema` (e.g. `uv run --no-project --with jsonschema==4.25.1
python3 tools/mte-interop.py --check`), node >= 18, bash, git.

Bounds: interop of the report format and score semantics only. It does not
make the hand-seeded tameshi defects Stryker mutators, does not run Stryker,
and does not validate the HTML report elements.
"""
import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / 'tools/vendor'
PACKAGES = {
    # npm registry dist.integrity for the exact versions, re-checked before every use
    'mutation-testing-report-schema': ('mutation-testing-report-schema-3.9.0.tgz',
        'sha512-28CobrcLdQm35zySemaLMKrUpVccLMA1DekUGtfezOSmnI0Xq8oJisixYnO0BQYIwKCkKL7+AE71/uWq/vFSJQ=='),
    'mutation-testing-metrics': ('mutation-testing-metrics-3.9.0.tgz',
        'sha512-E2i+8bXoEST8KIyJymc+OjO3eW+Q2gBAwI+hh0tvEZxif9nZQnawAh/+2hLWg+aZRWsG5s3I5xDAGZfELxC7hw=='),
}
SCHEMA_MEMBER = 'package/src/mutation-testing-report-schema.json'
STATUS = {'KILLED': 'Killed', 'SURVIVED': 'Survived', 'INCONCLUSIVE': 'RuntimeError'}
LANGUAGE = {'.mjs': 'javascript', '.js': 'javascript', '.sh': 'shell', '.py': 'python'}
TABLE = re.compile(r'^REGRESSION_TABLE (\S+): match=\d+/(\d+) recorded-killed=(\d+) measured-killed=(\d+) '
                   r'survived=(\d+) inconclusive=(\d+)', re.M)
NODE_RUNNER = r"""
import { readFileSync } from 'node:fs';
import { calculateMetrics } from 'mutation-testing-metrics';
const reports = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const out = {};
for (const [leg, report] of Object.entries(reports)) {
  const m = calculateMetrics(report.files).metrics;
  out[leg] = { mutationScore: m.mutationScore, killed: m.killed, survived: m.survived,
               totalValid: m.totalValid, totalInvalid: m.totalInvalid, totalMutants: m.totalMutants };
}
process.stdout.write(JSON.stringify(out));
"""


class Setup(Exception):
    pass


def unescape(text):
    out, i = [], 0
    while i < len(text):
        if text[i] == '\\' and i + 1 < len(text):
            nxt = text[i + 1]
            if nxt not in 'ntr\\':
                raise Setup('unsupported escape \\%s in spec' % nxt)
            out.append({'n': '\n', 't': '\t', 'r': '\r', '\\': '\\'}[nxt])
            i += 2
        else:
            out.append(text[i])
            i += 1
    return ''.join(out)


def parse_spec(text):
    defects, current = [], None
    for line in text.splitlines():
        if line.startswith('@defect '):
            ident, _, desc = line[len('@defect '):].partition(' | ')
            current = {'id': ident.strip(), 'desc': desc.strip(), 'old': None, 'new': None}
            defects.append(current)
        elif line.startswith('@old ') and current is not None:
            current['old'] = unescape(line[len('@old '):])
        elif line.startswith('@new') and current is not None:
            current['new'] = unescape(line[len('@new '):]) if line.startswith('@new ') else ''
    return defects


def position(source, offset):
    line = source.count('\n', 0, offset) + 1
    column = offset - (source.rfind('\n', 0, offset) + 1) + 1
    return {'line': line, 'column': column}


def leg_report(leg_dir):
    leg_dir = Path(leg_dir)
    pristine = sorted(leg_dir.glob('pristine.target.*'))
    if len(pristine) != 1:
        raise Setup('%s: expected one pristine target' % leg_dir.name)
    source = pristine[0].read_text()
    name = pristine[0].name[len('pristine.target.'):]
    defects = parse_spec((leg_dir / 'spec.copy').read_text())
    verdicts = {}
    rows = (leg_dir / 'results.tsv').read_text().splitlines()
    for row in rows[1:]:
        cols = row.split('\t')
        verdicts[cols[0]] = cols[1]
    if [d['id'] for d in defects] != list(verdicts):
        raise Setup('%s: spec defects and results rows differ' % leg_dir.name)
    mutants = []
    for d in defects:
        if d['old'] is None or source.count(d['old']) != 1:
            raise Setup('%s %s: @old is not unique in the pristine target' % (leg_dir.name, d['id']))
        start = source.index(d['old'])
        mutants.append({'id': d['id'], 'mutatorName': 'tameshi-hand-seeded',
                        'description': d['desc'], 'replacement': d['new'],
                        'location': {'start': position(source, start),
                                     'end': position(source, start + len(d['old']))},
                        'status': STATUS[verdicts[d['id']]],
                        'statusReason': 'tameshi verdict %s' % verdicts[d['id']]})
    language = LANGUAGE.get(Path(name).suffix, 'plaintext')
    return {'schemaVersion': '1', 'thresholds': {'high': 80, 'low': 60},
            'framework': {'name': 'tameshi mutate-and-run.sh'},
            'files': {name: {'language': language, 'source': source, 'mutants': mutants}}}


def tameshi_counts(report):
    killed = survived = inconclusive = 0
    for f in report['files'].values():
        for m in f['mutants']:
            reason = m.get('statusReason', '')
            killed += reason.endswith('KILLED')
            survived += reason.endswith('SURVIVED')
            inconclusive += reason.endswith('INCONCLUSIVE')
    return killed, survived, inconclusive


def verified_tarball(package):
    filename, integrity = PACKAGES[package]
    raw = (VENDOR / filename).read_bytes()
    digest = 'sha512-' + base64.b64encode(hashlib.sha512(raw).digest()).decode()
    if digest != integrity:
        raise Setup('%s integrity mismatch' % filename)
    return raw


def load_schema():
    raw = verified_tarball('mutation-testing-report-schema')
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        return json.loads(tar.extractfile(SCHEMA_MEMBER).read())


def schema_errors(validator, report):
    return sorted(e.message[:120] for e in validator.iter_errors(report))


def official_metrics(reports):
    node = shutil.which('node')
    if not node:
        raise Setup('node not found')
    with tempfile.TemporaryDirectory(prefix='tameshi-mte-') as tmp:
        tmp = Path(tmp)
        for package in PACKAGES:
            dest = tmp / 'node_modules' / package
            dest.mkdir(parents=True)
            with tarfile.open(fileobj=io.BytesIO(verified_tarball(package))) as tar:
                for member in tar.getmembers():
                    if not member.name.startswith('package/') or '..' in Path(member.name).parts:
                        raise Setup('unexpected tar member %s' % member.name)
                    if member.isfile():
                        target = dest / member.name[len('package/'):]
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(tar.extractfile(member).read())
        (tmp / 'run.mjs').write_text(NODE_RUNNER)
        (tmp / 'reports.json').write_text(json.dumps(reports))
        run = subprocess.run([node, str(tmp / 'run.mjs'), str(tmp / 'reports.json')],
                             cwd=tmp, capture_output=True, text=True, timeout=120)
        if run.returncode != 0:
            raise Setup('official metrics failed: %s' % run.stderr.strip()[-200:])
        return json.loads(run.stdout)


def judge(leg, report, errors, official, recorded):
    """recorded = (defects, recorded_killed) from the ledger table, or None."""
    killed, survived, inconclusive = tameshi_counts(report)
    tameshi_score = 100.0 * killed / (killed + survived) if killed + survived else None
    checks = {
        'schema': not errors,
        'score': (tameshi_score is not None and official['mutationScore'] is not None
                  and abs(official['mutationScore'] - tameshi_score) < 1e-9),
        'ledger': (recorded is not None and official['killed'] == recorded[1]
                   and official['totalValid'] == recorded[0]),
    }
    detail = ('schema=%s official_score=%s tameshi_score=%s official_killed=%s recorded_killed=%s '
              'official_valid=%s recorded_defects=%s' % (
                  'ok' if not errors else 'invalid:' + '|'.join(errors[:2]),
                  official['mutationScore'], tameshi_score, official['killed'],
                  recorded and recorded[1], official['totalValid'], recorded and recorded[0]))
    return all(checks.values()), detail


def run_regression(workdir, fleet_root):
    """The runner resolves sibling lanes from its own grandparent directory, so it
    runs from a private staged fleet: a copy of this checkout's runner plus
    read-only symlinks to the sibling repos under fleet_root."""
    fleet_root = Path(fleet_root).resolve()
    if not fleet_root.is_dir():
        raise Setup('fleet root %s is not a directory' % fleet_root)
    stage = Path(tempfile.mkdtemp(prefix='tameshi-mte-fleet-'))
    try:
        lane = stage / ROOT.name
        (lane / 'tools').mkdir(parents=True)
        shutil.copy2(ROOT / 'tools/mutate-and-run.sh', lane / 'tools/mutate-and-run.sh')
        for sibling in fleet_root.iterdir():
            if sibling.is_dir() and sibling.name != ROOT.name and (sibling / '.git').exists():
                (stage / sibling.name).symlink_to(sibling)
        run = subprocess.run(['bash', str(lane / 'tools/mutate-and-run.sh'), '--regression',
                              '--workdir', str(workdir), '--keep'], capture_output=True, text=True)
    finally:
        shutil.rmtree(stage, ignore_errors=True)
    (Path(workdir) / 'regression.stdout').write_text(run.stdout)
    if run.returncode != 0:
        raise Setup('regression exit %d' % run.returncode)
    return run.stdout


def check(args):
    try:
        import jsonschema
    except ImportError:
        print('MTE_INTEROP: SETUP (python jsonschema not importable)')
        return 2
    try:
        validator = jsonschema.Draft7Validator(load_schema())
        if args.workdir:
            workdir = Path(args.workdir)
            stdout = (workdir / 'regression.stdout').read_text() if (workdir / 'regression.stdout').is_file() \
                else args.regression_stdout.read_text() if args.regression_stdout else ''
        else:
            workdir = Path(tempfile.mkdtemp(prefix='tameshi-mte-regression-'))
            stdout = run_regression(workdir, args.fleet_root or ROOT.parent)
        tables = {m.group(1): (int(m.group(2)), int(m.group(3))) for m in TABLE.finditer(stdout)}
        legs = sorted(p.parent.name for p in workdir.glob('*/results.tsv'))
        if not legs:
            raise Setup('no leg results under %s' % workdir)
        reports = {leg: leg_report(workdir / leg) for leg in legs}
        official = official_metrics(reports)
    except (Setup, OSError, ValueError, KeyError) as exc:
        print('MTE_INTEROP: SETUP (%s)' % exc)
        return 2
    conforming = 0
    for leg in legs:
        ok, detail = judge(leg, reports[leg], schema_errors(validator, reports[leg]),
                           official[leg], tables.get(leg))
        conforming += ok
        print('MTE_LEG %s: %s (%s)' % (leg, 'CONFORMS' if ok else 'FAILS', detail))
    if args.emit:
        out = Path(args.emit)
        out.mkdir(parents=True, exist_ok=True)
        for leg in legs:
            (out / ('%s.mte.json' % leg)).write_text(json.dumps(reports[leg], indent=1, sort_keys=True) + '\n')
        (out / 'official-metrics.json').write_text(json.dumps(official, indent=1, sort_keys=True) + '\n')
    print('MTE_INTEROP: %s legs_conforming=%d/%d' % ('PASS' if conforming == len(legs) else 'FAIL',
                                                    conforming, len(legs)))
    if not args.workdir and conforming == len(legs):
        shutil.rmtree(workdir, ignore_errors=True)
    return 0 if conforming == len(legs) else 1


def selftest():
    """Negative controls: each doctored report must be rejected for the stated reason."""
    try:
        import jsonschema
        validator = jsonschema.Draft7Validator(load_schema())
    except (ImportError, Setup, OSError, ValueError) as exc:
        print('MTE_SELFTEST: SETUP (%s)' % exc)
        return 2
    source = 'a = 1\nif a == 1:\n    ok()\n'
    def mutant(ident, status, line=1, verdict=None):
        return {'id': ident, 'mutatorName': 'tameshi-hand-seeded', 'replacement': 'x',
                'location': {'start': {'line': line, 'column': 1}, 'end': {'line': line, 'column': 2}},
                'status': status, 'statusReason': 'tameshi verdict %s' % (verdict or status.upper())}
    def report(mutants, **extra):
        value = {'schemaVersion': '1', 'thresholds': {'high': 80, 'low': 60},
                 'files': {'t.py': {'language': 'python', 'source': source, 'mutants': mutants}}}
        value.update(extra)
        return value
    good = report([mutant('D1', 'Killed'), mutant('D2', 'Killed'), mutant('D3', 'Survived')])
    flipped = json.loads(json.dumps(good))
    flipped['files']['t.py']['mutants'][0]['status'] = 'Survived'          # tameshi says KILLED
    inconclusive = report([mutant('D1', 'Killed'), mutant('D2', 'RuntimeError', verdict='INCONCLUSIVE'),
                           mutant('D3', 'Survived')])
    timeout_as_kill = report([mutant('D1', 'Killed'), mutant('D2', 'Timeout', verdict='SURVIVED'),
                              mutant('D3', 'Survived')])
    no_thresholds = json.loads(json.dumps(good))
    del no_thresholds['thresholds']
    cases = [
        ('conforming', good, (3, 2), True, None),
        ('tameshi-vocabulary-status', report([mutant('D1', 'KILLED'), mutant('D2', 'Killed'), mutant('D3', 'Survived')]), (3, 2), False, 'schema'),
        ('line-zero-location', report([mutant('D1', 'Killed', line=0), mutant('D2', 'Killed'), mutant('D3', 'Survived')]), (3, 2), False, 'schema'),
        ('missing-thresholds', no_thresholds, (3, 2), False, 'schema'),
        ('bad-schema-version', report([mutant('D1', 'Killed'), mutant('D2', 'Killed'), mutant('D3', 'Survived')], schemaVersion='3'), (3, 2), False, 'schema'),
        ('status-flipped-vs-verdict', flipped, (3, 2), False, 'score'),
        ('inconclusive-leaves-denominator', inconclusive, (3, 1), False, 'ledger'),
        ('timeout-is-not-a-tameshi-kill', timeout_as_kill, (3, 1), False, 'score'),
        ('ledger-count-mismatch', good, (3, 3), False, 'ledger'),
        ('no-ledger-row', good, None, False, 'ledger'),
    ]
    try:
        official = official_metrics({name: rep for name, rep, _, _, _ in cases})
    except Setup as exc:
        print('MTE_SELFTEST: SETUP (%s)' % exc)
        return 2
    passed = 0
    for name, rep, recorded, want, reason in cases:
        errors = schema_errors(validator, rep)
        ok, detail = judge(name, rep, errors, official[name], recorded)
        killed, survived, _ = tameshi_counts(rep)
        t_score = 100.0 * killed / (killed + survived) if killed + survived else None
        reasons = {'schema': bool(errors),
                   'score': not (official[name]['mutationScore'] is not None and t_score is not None
                                 and abs(official[name]['mutationScore'] - t_score) < 1e-9),
                   'ledger': recorded is None or official[name]['killed'] != recorded[1]
                             or official[name]['totalValid'] != recorded[0]}
        good_case = ok == want and (want or reasons[reason])
        passed += good_case
        print('CASE %s %s (%s)' % (name, 'PASS' if good_case else 'FAIL', detail))
    print('MTE_SELFTEST: %d/%d pass' % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(64, '%s: error: %s\n' % (self.prog, message))


def main():
    parser = Parser(description=__doc__, allow_abbrev=False)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--selftest', action='store_true')
    parser.add_argument('--workdir', help='existing kept regression workdir (skips the live run)')
    parser.add_argument('--regression-stdout', type=Path, help='its stdout, if not inside the workdir')
    parser.add_argument('--fleet-root', help='directory holding the sibling lane repos (default: parent of this checkout)')
    parser.add_argument('--emit', help='write the per-leg reports and official metrics here')
    args = parser.parse_args()
    if args.selftest:
        if args.workdir or args.emit or args.regression_stdout or args.fleet_root:
            parser.error('--selftest takes no other arguments')
        return selftest()
    return check(args)


if __name__ == '__main__':
    raise SystemExit(main())
