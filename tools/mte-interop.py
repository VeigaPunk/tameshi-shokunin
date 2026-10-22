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
  4. judges four checks per leg:
     schema      the official schema accepts the report;
     ledger      official killed = recorded killed = measured killed, official
                 survived = measured survived, official invalid = measured
                 inconclusive, official total = defect count, runner flips 0
                 (the leg's REGRESSION_TABLE line, not the emitted report);
     per_mutant  every emitted status equals the mapped verdict of the same
                 defect id in the runner's committed TABLE_* recorded table
                 (catches balanced flips that keep the counts equal);
     score       official mutationScore = killed/(killed+survived)*100. This
                 one is a sanity check only: with the 1:1 mapping it holds by
                 construction (round-25 wave seat C2Tautology).
A leg conforms only when all four hold. Each leg line also prints the runner's
integer kill-rate next to the official score rounded half up (information only:
the ledger's integer percentages are rounded, e.g. 7/15 = 46.67 printed as 47).

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
                   r'survived=(\d+) inconclusive=(\d+) flips=(\d+)', re.M)
# Recorded per-defect verdict tables embedded in the runner (committed bytes, not this run).
LEG_TABLE = {'js-kimi-census': 'TABLE_JS', 'bash-surface-census': 'TABLE_BASH',
             'bash-tsukuroi-census': 'TABLE_TSUKUROI', 'bash-mado-verify': 'TABLE_MADO',
             'bash-checklist-run': 'TABLE_CHECKLIST', 'js-claims-check': 'TABLE_CLAIMS',
             'js-round-gate': 'TABLE_ROUNDGATE', 'js-sources-check': 'TABLE_SOURCESCHECK'}
KILL_RATE = re.compile(r'^MUTATE: DONE \(.* kill-rate=(\d+)%\)', re.M)
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
                    rel = member.name[len('package/'):] if member.name.startswith('package/') else ''
                    if member.isdir() and member.name.rstrip('/') == 'package':
                        continue
                    if (not rel or Path(rel).is_absolute() or '..' in Path(rel).parts
                            or not (member.isfile() or member.isdir())):
                        raise Setup('unexpected tar member %s' % member.name)
                    if member.isfile():
                        target = dest / member.name[len('package/'):]
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(tar.extractfile(member).read())
        (tmp / 'run.mjs').write_text(NODE_RUNNER)
        (tmp / 'reports.json').write_text(json.dumps(reports))
        try:
            run = subprocess.run([node, str(tmp / 'run.mjs'), str(tmp / 'reports.json')],
                                 cwd=tmp, capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            raise Setup('official metrics timed out after 120 s')
        if run.returncode != 0:
            raise Setup('official metrics failed: %s' % run.stderr.strip()[-200:])
        return json.loads(run.stdout)


def recorded_verdicts(runner_text):
    """{leg: {defect id: KILLED|SURVIVED}} from the runner's embedded TABLE_* lines."""
    tables = dict(re.findall(r"^(TABLE_\w+)='([^']*)'", runner_text, re.M))
    out = {}
    for leg, var in LEG_TABLE.items():
        if var in tables:
            out[leg] = dict(pair.split(':', 1) for pair in tables[var].split(','))
    return out


def judge(leg, report, errors, official, recorded, verdicts):
    """recorded: the leg's REGRESSION_TABLE counts (defects, recorded_killed, measured_killed,
    survived, inconclusive, flips) or None; verdicts: the recorded per-defect table or None.
    Returns (ok, detail, failed check names)."""
    killed, survived, inconclusive = tameshi_counts(report)
    tameshi_score = 100.0 * killed / (killed + survived) if killed + survived else None
    statuses = {m['id']: m['status'] for f in report['files'].values() for m in f['mutants']}
    checks = {
        'schema': not errors,
        # sanity only: with a 1:1 Killed/Survived mapping this equality holds by construction
        'score': (tameshi_score is not None and official['mutationScore'] is not None
                  and abs(official['mutationScore'] - tameshi_score) < 1e-9),
        # independent of the emitter: the runner's own measured table line for this leg
        'ledger': (recorded is not None and recorded['flips'] == 0
                   and official['killed'] == recorded['recorded_killed'] == recorded['measured_killed']
                   and official['survived'] == recorded['survived']
                   and official['totalInvalid'] == recorded['inconclusive']
                   and official['totalMutants'] == recorded['defects']),
        # independent of this run: the committed per-defect recorded verdict table
        'per_mutant': (verdicts is not None and statuses == {i: STATUS.get(v) for i, v in verdicts.items()}),
    }
    failed = sorted(k for k, v in checks.items() if not v)
    detail = ('schema=%s official_score=%s official_killed=%s official_survived=%s official_invalid=%s '
              'recorded=%s per_mutant=%s failed=%s' % (
                  'ok' if not errors else 'invalid:' + '|'.join(errors[:2]),
                  official['mutationScore'], official['killed'], official['survived'],
                  official['totalInvalid'], recorded and '%(recorded_killed)s/%(defects)s' % recorded,
                  'ok' if checks['per_mutant'] else 'mismatch', ','.join(failed) or 'none'))
    return not failed, detail, failed


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
        if not shutil.which('node'):
            raise Setup('node not found')
        if args.workdir:
            workdir = Path(args.workdir)
            stdout = (workdir / 'regression.stdout').read_text() if (workdir / 'regression.stdout').is_file() \
                else args.regression_stdout.read_text() if args.regression_stdout else ''
        else:
            workdir = Path(tempfile.mkdtemp(prefix='tameshi-mte-regression-'))
            print('MTE_WORKDIR: %s (removed on PASS)' % workdir)
            stdout = run_regression(workdir, args.fleet_root or ROOT.parent)
        tables = {m.group(1): dict(zip(('defects', 'recorded_killed', 'measured_killed', 'survived',
                                        'inconclusive', 'flips'), map(int, m.groups()[1:])))
                  for m in TABLE.finditer(stdout)}
        verdicts = recorded_verdicts((ROOT / 'tools/mutate-and-run.sh').read_text())
        legs = sorted(p.parent.name for p in workdir.glob('*/results.tsv'))
        if set(legs) != set(LEG_TABLE) or set(tables) != set(LEG_TABLE):
            raise Setup('leg set %s / table set %s differs from the eight ledger legs %s'
                        % (legs, sorted(tables), sorted(LEG_TABLE)))
        reports = {leg: leg_report(workdir / leg) for leg in legs}
        official = official_metrics(reports)
    except (Setup, OSError, ValueError, KeyError) as exc:
        print('MTE_INTEROP: SETUP (%s)' % exc)
        return 2
    conforming = 0
    for leg in legs:
        ok, detail, _ = judge(leg, reports[leg], schema_errors(validator, reports[leg]),
                              official[leg], tables.get(leg), verdicts.get(leg))
        conforming += ok
        sweep_log = workdir / leg / 'sweep.log'
        rate = KILL_RATE.search(sweep_log.read_text()) if sweep_log.is_file() else None
        k, s = official[leg]['killed'], official[leg]['survived']
        rounding = ('runner_pct=%s official_rounded_half_up=%d' % (rate.group(1), (200 * k + k + s) // (2 * (k + s)))
                    if rate and k + s else 'runner_pct=unavailable')
        print('MTE_LEG %s: %s (%s %s)' % (leg, 'CONFORMS' if ok else 'FAILS', detail, rounding))
    if args.emit:
        out = Path(args.emit)
        out.mkdir(parents=True, exist_ok=True)
        for leg in legs:
            (out / ('%s.mte.json' % leg)).write_text(json.dumps(reports[leg], indent=1, sort_keys=True) + '\n')
            shutil.copyfile(workdir / leg / 'spec.copy', out / ('%s.spec' % leg))
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
    def rec(defects, killed, survived, inconclusive=0, flips=0):
        return {'defects': defects, 'recorded_killed': killed, 'measured_killed': killed,
                'survived': survived, 'inconclusive': inconclusive, 'flips': flips}
    V3 = {'D1': 'KILLED', 'D2': 'KILLED', 'D3': 'SURVIVED'}
    good = report([mutant('D1', 'Killed'), mutant('D2', 'Killed'), mutant('D3', 'Survived')])
    flipped = json.loads(json.dumps(good))
    flipped['files']['t.py']['mutants'][0]['status'] = 'Survived'          # tameshi says KILLED
    balanced = report([mutant('D1', 'Killed'), mutant('D2', 'Survived', verdict='SURVIVED'),
                       mutant('D3', 'Killed', verdict='KILLED')])             # counts equal, ids swapped
    nocoverage = report([mutant('D1', 'Killed'), mutant('D2', 'Killed'),
                         mutant('D3', 'NoCoverage', verdict='SURVIVED')])
    inconclusive = report([mutant('D1', 'Killed'), mutant('D2', 'RuntimeError', verdict='INCONCLUSIVE'),
                           mutant('D3', 'Survived')])
    timeout_as_kill = report([mutant('D1', 'Killed'), mutant('D2', 'Timeout', verdict='SURVIVED'),
                              mutant('D3', 'Survived')])
    no_thresholds = json.loads(json.dumps(good))
    del no_thresholds['thresholds']
    # Emitter-level cases: a synthetic leg directory goes through the real leg_report().
    emit_tmp = Path(tempfile.mkdtemp(prefix='tameshi-mte-selftest-'))
    try:
        (emit_tmp / 'pristine.target.t.py').write_text(source)
        (emit_tmp / 'spec.copy').write_text('@defect D1 | a\n@old a = 1\n@new a = 2\n\n'
                                            '@defect D2 | b\n@old if a == 1:\\n    ok()\n@new pass\n\n'
                                            '@defect D3 | c\n@old ok()\n@new no()\n')
        (emit_tmp / 'results.tsv').write_text('id\tverdict\texit\tduration-ms\tmutant-sha256\tdesc\n'
                                              'D1\tKILLED\t1\t1\tx\ta\nD2\tINCONCLUSIVE\t124\t1\tx\tb\n'
                                              'D3\tSURVIVED\t0\t1\tx\tc\n')
        emitted = leg_report(emit_tmp)
    except (Setup, OSError, ValueError, KeyError) as exc:
        print('MTE_SELFTEST: SETUP (emitter: %s)' % exc)
        return 2
    finally:
        shutil.rmtree(emit_tmp, ignore_errors=True)
    locations = {m['id']: (m['location']['start']['line'], m['location']['start']['column'],
                           m['location']['end']['line'], m['location']['end']['column'])
                 for m in emitted['files']['t.py']['mutants']}
    V_EMIT = {'D1': 'KILLED', 'D2': 'INCONCLUSIVE', 'D3': 'SURVIVED'}
    cases = [
        ('conforming', good, rec(3, 2, 1), V3, True, None),
        ('tameshi-vocabulary-status', report([mutant('D1', 'KILLED'), mutant('D2', 'Killed'), mutant('D3', 'Survived')]), rec(3, 2, 1), V3, False, 'schema'),
        ('line-zero-location', report([mutant('D1', 'Killed', line=0), mutant('D2', 'Killed'), mutant('D3', 'Survived')]), rec(3, 2, 1), V3, False, 'schema'),
        ('missing-thresholds', no_thresholds, rec(3, 2, 1), V3, False, 'schema'),
        ('bad-schema-version', report([mutant('D1', 'Killed'), mutant('D2', 'Killed'), mutant('D3', 'Survived')], schemaVersion='3'), rec(3, 2, 1), V3, False, 'schema'),
        ('status-flipped-vs-verdict', flipped, rec(3, 2, 1), V3, False, 'per_mutant'),
        ('balanced-flip-same-counts', balanced, rec(3, 2, 1), V3, False, 'per_mutant'),
        ('survived-as-nocoverage', nocoverage, rec(3, 2, 1), V3, False, 'ledger'),
        ('inconclusive-is-not-recorded-survived', inconclusive, rec(3, 1, 1, inconclusive=1), V3, False, 'per_mutant'),
        ('timeout-is-not-a-tameshi-kill', timeout_as_kill, rec(3, 1, 2), {'D1': 'KILLED', 'D2': 'SURVIVED', 'D3': 'SURVIVED'}, False, 'score'),
        ('ledger-count-mismatch', good, rec(3, 3, 0), V3, False, 'ledger'),
        ('runner-flips-nonzero', good, rec(3, 2, 1, flips=1), V3, False, 'ledger'),
        ('no-ledger-row', good, None, V3, False, 'ledger'),
        ('no-recorded-table', good, rec(3, 2, 1), None, False, 'per_mutant'),
        ('emitter-inconclusive-to-runtimeerror', emitted, rec(3, 1, 1, inconclusive=1), V_EMIT, True, None),
        # seat C2Mutants: a 0.5-point gap that only the score check can see (tolerance mutants)
        ('narrow-score-delta', report([mutant('N%d' % i, 'Killed', verdict='SURVIVED' if i == 0 else None)
                                       for i in range(200)]),
         rec(200, 200, 0), {'N%d' % i: 'KILLED' for i in range(200)}, False, 'score'),
    ]
    try:
        official = official_metrics({c[0]: c[1] for c in cases})
    except Setup as exc:
        print('MTE_SELFTEST: SETUP (%s)' % exc)
        return 2
    passed = 0
    for name, rep, recorded, verdicts, want, reason in cases:
        ok, detail, failed = judge(name, rep, schema_errors(validator, rep), official[name], recorded, verdicts)
        good_case = ok == want and (want or reason in failed)
        passed += good_case
        print('CASE %s %s (%s)' % (name, 'PASS' if good_case else 'FAIL', detail))
    # 1-based, end-exclusive positions computed from the unique @old strings (schema Location)
    want_loc = {'D1': (1, 1, 1, 6), 'D2': (2, 1, 3, 9), 'D3': (3, 5, 3, 9)}
    loc_ok = locations == want_loc
    passed += loc_ok
    print('CASE emitter-locations %s (%s)' % ('PASS' if loc_ok else 'FAIL', locations))
    total = len(cases) + 1
    print('MTE_SELFTEST: %d/%d pass' % (passed, total))
    return 0 if passed == total else 1


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
