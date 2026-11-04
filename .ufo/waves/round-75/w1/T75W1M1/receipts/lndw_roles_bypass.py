#!/usr/bin/env python3
"""tools/wave-reconcile.py — round record vs wave artifact reconciliation (round 73).

What it answers, after a round closes: *do the round's own execution claims —
how many seats ran, how many seat reports the wave committed, which roles ran,
how many of them were attack seats — survive a re-derivation from the committed
wave artifacts?* The round-72 non-author closure routed exactly this class as
two status-neutral defects (the report's "12 seats, 11 reports" against 12
committed seat reports; the frozen plan's `1 labrat` against the executed
`revenger`), and nothing in the lane could re-derive either claim.

Four row kinds. Each binds a RECORD claim to an ARTIFACT re-derivation:

  seats          a record span prints the wave's seat count; measured against
                 `len(results[])` and `results.seats`.
  seat_reports   a record span prints the count of seat reports; measured
                 against the `*.md` files at the top of the wave dir at the
                 artifact revision.
  roles          a record declares a role multiset (spec items, or `N role`
                 tokens inside a record span); measured against the `agent`
                 multiset in `results[]`.
  attack_share   the share of seats whose agent is in the row's named attack
                 set, measured against the row's floor percentage.

Binding rules (eighteen arms: seats-meet/mismatch, seat_reports-drift,
roles-spec/text-drift, attack-below-floor/at-floor, five setup refusals, - from
round 74 - arm13 delimited-token, arm14 record-span-substring and arm15
seat_reports-top-level-only, the three rules round 73 carried as arm gaps and
measured as survivors: `delimited := True` 12/12, the span-rule removal 12/12,
`seat_reports` any-depth 12/12 plus the standing sweep, and - from round 75 -
arm16 printed-span-not-record, arm17 record-claim-live-on-roles and arm18
record-claim-live-on-attack-share, the two round-74 survivors: a `printed` token
delimited in the record but outside the bound span, and the selective
`_record_claim` bypass on the `roles` and `attack_share` branches. Each new arm
names its mutant in `tools/wave-reconcile-mutants.spec`):

  * the record span must be a byte substring of the record at the record rev;
  * the printed integer must occur in the span as a delimited token;
  * a `text-tokens` role declaration must carry every `N role` pair inside the
    span — an absent declaration is a setup error, never a silent pass (the
    always-match cheat is refused by construction);
  * artifacts are read from git objects at their named revision, never from a
    worktree; a row-level `root` of `fleet` resolves against the `--extra-root`
    named path (the fleet repo holds the round reports — the
    `receipt-exists.py` `--extra-root` precedent);
  * artifact bytes decode as UTF-8; a UTF-8 BOM is refused as setup exit 2
    naming the artifact (S066 §8.1: a BOM is not part of a JSON text, and this
    reader refuses it rather than silently stripping bytes the emitter said are
    not JSON);
  * `expect` is `meet` or `drift`, so a standing red arm MEASURES the drift on
    every sweep instead of assuming it;
  * a zero-row manifest, an unresolvable revision or an undecodable artifact is
    setup exit 2 before any row effect.

Exit: 0 every row measured its expected status; 1 at least one did not; 2 setup.

Usage:

  python3 -I -X utf8 tools/wave-reconcile.py --selftest
  python3 -I -X utf8 tools/wave-reconcile.py --repo . \\
      --extra-root fleet=/home/vgpnk/Projects/shokunin \\
      --manifest tools/wave-reconcile.json
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SELFTEST_ARMS = 18
BOM = b'\xef\xbb\xbf'
ATTACK_NOTE = ('named attack roles are the row\'s own declaration; the policy '
               'floor is the row\'s floor_pct')


class SetupError(Exception):
    pass


def decode_json(raw, label):
    """Strict: UTF-8 only, a BOM is refused and never stripped (S066 §8.1)."""
    if raw.startswith(BOM):
        raise SetupError('bom-present:%s' % label)
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise SetupError('not-utf8:%s:%s' % (label, exc))
    try:
        return json.loads(text)
    except ValueError as exc:
        raise SetupError('unparsable:%s:%s' % (label, exc))


def delimited(value, span):
    return re.search(r'(?<![0-9])%d(?![0-9])' % value, span) is not None


class GitReader(object):
    """Read blobs and tree listings from git objects at a named revision."""

    def __init__(self, root):
        self.root = root

    def _git(self, *args):
        proc = subprocess.run(['git', '-C', self.root] + list(args),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            raise SetupError('git-failed:%s:%s' % (
                self.root, proc.stderr.decode('utf-8', 'replace').strip()[:200]))
        return proc.stdout

    def blob(self, rev, path):
        if not re.fullmatch(r'[0-9a-f]{6,40}', rev or ''):
            raise SetupError('rev-unresolvable:%s' % (rev,))
        return self._git('cat-file', 'blob', '%s:%s' % (rev, path))

    def listing(self, rev, path):
        out = self._git('ls-tree', '-r', '--name-only', rev, '--', path)
        return [line for line in out.decode('utf-8', 'replace').splitlines()
                if line]


class FixtureReader(object):
    """Hermetic reader for the selftest: blobs and listings from dicts."""

    def __init__(self, blobs, listings):
        self.blobs = blobs
        self.listings = listings

    def blob(self, rev, path):
        key = (rev, path)
        if key not in self.blobs:
            raise SetupError('rev-unresolvable-or-path-absent:%s:%s' % key)
        return self.blobs[key]

    def listing(self, rev, path):
        key = (rev, path)
        if key not in self.listings:
            raise SetupError('listing-absent:%s:%s' % key)
        return self.listings[key]


def _artifact(row, key, readers):
    art = row.get('wave') or {}
    if key not in art:
        raise SetupError('row-missing-%s:%s' % (key, row.get('id')))
    root = art.get('root', 'lane')
    if root not in readers:
        raise SetupError('unknown-root:%s:%s' % (root, row.get('id')))
    return readers[root], art['rev'], art[key]


def _record_span(row, readers):
    rec = row.get('record') or {}
    for key in ('path', 'rev', 'span'):
        if key not in rec:
            raise SetupError('record-missing-%s:%s' % (key, row.get('id')))
    root = rec.get('root', 'lane')
    if root not in readers:
        raise SetupError('unknown-root:%s:%s' % (root, row.get('id')))
    reader = readers[root]
    raw = reader.blob(rec['rev'], rec['path'])
    if rec['span'].encode('utf-8') not in raw:
        raise SetupError('span-not-in-record:%s:%s' % (row['id'], rec['path']))
    return raw.decode('utf-8'), rec


def _record_claim(row, readers, require_printed=False):
    """Bind the record span for EVERY kind (round-73 seat T73W1S03: an inert
    record block made a forged span a silent pass on roles/attack_share rows).
    A `printed` value, when the row carries one, must be a delimited token in
    the bound span; `seats`/`seat_reports` rows must carry one."""
    _, rec = _record_span(row, readers)
    printed = rec.get('printed')
    if printed is None:
        if require_printed:
            raise SetupError('record-printed-absent:%s' % row['id'])
        return None
    if not isinstance(printed, int):
        raise SetupError('record-printed-not-int:%s' % row['id'])
    if not delimited(printed, rec['span']):
        raise SetupError('printed-not-in-span:%s' % row['id'])
    return printed


def _results(row, readers):
    reader, rev, path = _artifact(row, 'results', readers)
    doc = decode_json(reader.blob(rev, path), path)
    if not isinstance(doc, dict):
        raise SetupError('results-not-object:%s' % path)
    records = doc.get('results')
    if not isinstance(records, list):
        raise SetupError('results-list-absent:%s' % path)
    seats = doc.get('seats')
    if not isinstance(seats, int):
        raise SetupError('results-seats-absent:%s' % path)
    return seats, records


def _agents(records):
    counts = {}
    for rec in records:
        if not isinstance(rec, dict) or not isinstance(rec.get('agent'), str):
            raise SetupError('results-agent-absent')
        counts[rec['agent']] = counts.get(rec['agent'], 0) + 1
    return counts


def measure(row, readers):
    """Return (measured, detail). measured in {'meet', 'drift'}."""
    kind = row.get('kind')
    if kind == 'seats':
        printed = _record_claim(row, readers, require_printed=True)
        seats, records = _results(row, readers)
        ok = printed == seats == len(records)
        return ('meet' if ok else 'drift',
                'printed=%d seats=%d records=%d' % (printed, seats, len(records)))
    if kind == 'seat_reports':
        printed = _record_claim(row, readers, require_printed=True)
        reader, rev, path = _artifact(row, 'dir', readers)
        prefix = path.rstrip('/') + '/'
        files = [p for p in reader.listing(rev, path)
                 if p.startswith(prefix) and '/' not in p[len(prefix):]
                 and p.endswith('.md')]
        ok = printed == len(files)
        return ('meet' if ok else 'drift',
                'printed=%d files=%d' % (printed, len(files)))
    if kind == 'roles':
        _, records = _results(row, readers)
        measured = _agents(records)
        decl = row.get('declaration') or {}
        form = decl.get('form')
        reader = readers[decl.get('root', 'lane')]
        if form == 'spec-items':
            doc = decode_json(reader.blob(decl['rev'], decl['path']),
                              decl['path'])
            items = doc.get('items')
            if not isinstance(items, list):
                raise SetupError('spec-items-absent:%s' % row['id'])
            declared = {}
            for item in items:
                if not isinstance(item, dict) or not isinstance(item.get('role'), str):
                    raise SetupError('spec-role-absent:%s' % row['id'])
                declared[item['role']] = declared.get(item['role'], 0) + 1
        elif form == 'text-tokens':
            declared = decl.get('roles')
            if not isinstance(declared, dict) or not declared:
                raise SetupError('declared-roles-absent:%s' % row['id'])
            span = decl.get('span')
            if not isinstance(span, str) or not span:
                raise SetupError('declared-span-absent:%s' % row['id'])
            raw = reader.blob(decl['rev'], decl['path'])
            if span.encode('utf-8') not in raw:
                raise SetupError('span-not-in-record:%s:%s' % (row['id'], decl['path']))
            for role, count in declared.items():
                if not re.search(r'(?<![0-9])%d\s+%s\b' % (count, re.escape(role)),
                                 span):
                    raise SetupError('declaration-absent-in-record:%s:%s'
                                     % (row['id'], role))
        else:
            raise SetupError('declaration-form-unknown:%s' % row['id'])
        ok = declared == measured
        return ('meet' if ok else 'drift',
                'declared=%s measured=%s' % (
                    json.dumps(declared, sort_keys=True),
                    json.dumps(measured, sort_keys=True)))
    if kind == 'attack_share':
        _record_claim(row, readers)
        seats, records = _results(row, readers)
        named = row.get('named')
        floor = row.get('floor_pct')
        if not isinstance(named, list) or not named:
            raise SetupError('named-roles-absent:%s' % row['id'])
        if not isinstance(floor, (int, float)):
            raise SetupError('floor-absent:%s' % row['id'])
        counted = sum(c for a, c in _agents(records).items() if a in named)
        total = len(records)
        pct = (100.0 * counted / total) if total else 0.0
        return ('meet' if pct >= floor else 'drift',
                'attack=%d/%d=%.1f%% floor=%.1f%%' % (counted, total, pct, floor))
    raise SetupError('kind-unknown:%s' % row.get('id'))


def sweep(manifest, readers):
    """Return (rows_out, unexpected). Raises SetupError before any row effect."""
    rows = manifest.get('rows') if isinstance(manifest, dict) else None
    if not isinstance(rows, list) or not rows:
        raise SetupError('zero-rows')
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('id'), str):
            raise SetupError('row-malformed')
        if row['id'] in seen:
            raise SetupError('row-id-duplicate:%s' % row['id'])
        seen.add(row['id'])
        if row.get('expect') not in ('meet', 'drift'):
            raise SetupError('row-expect-invalid:%s' % row['id'])
    out = []
    unexpected = 0
    for row in rows:
        measured, detail = measure(row, readers)
        ok = measured == row['expect']
        if not ok:
            unexpected += 1
        out.append({'id': row['id'], 'kind': row.get('kind'),
                    'expect': row['expect'], 'measured': measured,
                    'ok': ok, 'detail': detail})
    return out, unexpected


def run_manifest(manifest_path, repo, extra_roots, as_json=False, out=None):
    try:
        with open(manifest_path, 'rb') as fh:
            manifest = decode_json(fh.read(), manifest_path)
    except OSError as exc:
        raise SetupError('manifest-unreadable:%s:%s' % (manifest_path, exc))
    readers = {'lane': GitReader(repo)}
    for item in extra_roots:
        if '=' not in item:
            raise SetupError('extra-root-malformed:%s' % item)
        name, path = item.split('=', 1)
        readers[name] = GitReader(path)
    rows, unexpected = sweep(manifest, readers)
    met = len(rows) - unexpected
    for row in rows:
        print('WAVE_ROW %s kind=%s expect=%s measured=%s %s | %s'
              % (row['id'], row['kind'], row['expect'], row['measured'],
                 'ok' if row['ok'] else 'MISMATCH', row['detail']))
        if not row['ok']:
            print('WAVE_MISMATCH %s expect=%s measured=%s'
                  % (row['id'], row['expect'], row['measured']))
    print('WAVE_RECONCILE: rows=%d met=%d unexpected=%d'
          % (len(rows), met, unexpected))
    if as_json or out:
        doc = {'schema': 'tameshi-wave-reconcile-receipt-v1', 'rows': rows,
               'met': met, 'unexpected': unexpected}
        if out:
            with open(out, 'w', encoding='utf-8') as fh:
                fh.write(json.dumps(doc, indent=1, ensure_ascii=True) + '\n')
        if as_json:
            print(json.dumps(doc, indent=1, ensure_ascii=True))
    return 0 if unexpected == 0 else 1


# --- selftest -------------------------------------------------------------
REV = 'a' * 40
RESULTS = {
    'seats': 12,
    'results': ([{'name': 'S%d' % i, 'agent': 'executor'} for i in range(3)]
                + [{'name': 'S3', 'agent': 'scribe'},
                   {'name': 'S4', 'agent': 'scribe'},
                   {'name': 'S5', 'agent': 'scout'},
                   {'name': 'S6', 'agent': 'reviewer'},
                   {'name': 'S7', 'agent': 'critic'},
                   {'name': 'S8', 'agent': 'mutation-tester'},
                   {'name': 'S9', 'agent': 'sentinel'},
                   {'name': 'S10', 'agent': 'revenger'},
                   {'name': 'S11', 'agent': 'connector'}]),
}
REPORT = (b'- **The wave**: 12 seats, 11 reports; three seats found defects.\n')
PLAN = (b'- Wave `w1`: 12 seats - 3 executor, 2 scribe, 1 scout, 1 connector,\n'
        b'  1 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 labrat.\n')
SEAT_FILES = (['%s/T1W1S%02d.md' % ('wave', i) for i in range(12)]
              + ['wave/swarm-registry.json',
                 # round 74 arm15: a nested .md is NOT a seat report; the
                 # any-depth mutant counts it (13) and the arm measures that.
                 'wave/nested/deep.md'])


def fixture_rows():
    results = json.dumps(RESULTS).encode('utf-8')
    spec = json.dumps({'items': [{'name': 'S%d' % i, 'role': r} for i, r in
                                 enumerate(['executor'] * 3 + ['scribe'] * 2
                                           + ['scout', 'reviewer', 'critic',
                                              'mutation-tester', 'sentinel',
                                              'revenger', 'connector'])]}
                      ).encode('utf-8')
    blobs = {(REV, 'report.md'): REPORT, (REV, 'plan.md'): PLAN,
             (REV, 'results.json'): results, (REV, 'spec.json'): spec}
    listings = {(REV, 'wave'): SEAT_FILES}
    return blobs, listings


def selftest():
    work = tempfile.mkdtemp(prefix='wave-reconcile-selftest-',
                            dir=os.environ.get('TMPDIR') or None)
    results = []
    try:
        blobs, listings = fixture_rows()

        def row(**kw):
            base = {'id': 'fixture-row',
                    'record': {'path': 'report.md', 'rev': REV,
                               'span': '12 seats', 'printed': 12},
                    'wave': {'dir': 'wave', 'results': 'results.json',
                             'rev': REV}}
            base.update(kw)
            return base

        def measure_row(extra_blobs=None, **kw):
            b = dict(blobs)
            if extra_blobs:
                b.update(extra_blobs)
            return measure(row(**kw), {'lane': FixtureReader(b, listings)})[0]

        def sweep_exit(rows, extra_blobs=None):
            b = dict(blobs)
            if extra_blobs:
                b.update(extra_blobs)
            _, unexpected = sweep({'rows': rows},
                                  {'lane': FixtureReader(b, listings)})
            return unexpected

        def arm_raises(name, prefix, fn):
            """Arm that must fail with the NAMED refusal, not any SetupError
            (round-74 seat T74W1R1: `arm()` collapsed the reason, so changing
            a diagnostic to an unrelated SetupError kept the suite green)."""
            try:
                fn()
            except SetupError as exc:
                got = str(exc)
                ok = got.startswith(prefix)
                results.append((name, ok, 'setup:' + got.split(':')[0],
                                'setup:' + prefix))
                return
            results.append((name, False, 'no-refusal', 'setup:' + prefix))

        def arm(name, want, fn):
            try:
                got = fn()
                ok = got == want
            except SetupError:
                got = 'setup'
                ok = (want == 'setup')
            results.append((name, ok, got, want))

        arm('arm1-seats-meet', 'meet',
            lambda: measure_row(kind='seats'))
        arm('arm2-seats-mismatch-caught', 1, lambda: sweep_exit([
            dict(row(kind='seats'), id='r', expect='meet',
                 record={'path': 'report.md', 'rev': REV,
                         'span': '11 reports', 'printed': 11})]))
        arm('arm3-seatreports-drift-measured', 'drift',
            lambda: measure_row(kind='seat_reports',
                                record={'path': 'report.md', 'rev': REV,
                                        'span': '12 seats, 11 reports',
                                        'printed': 11}))
        arm('arm4-roles-spec-meet', 'meet',
            lambda: measure_row(kind='roles', declaration={
                'form': 'spec-items', 'path': 'spec.json', 'rev': REV}))
        arm('arm5-roles-text-drift-measured', 'drift',
            lambda: measure_row(kind='roles', declaration={
                'form': 'text-tokens', 'path': 'plan.md', 'rev': REV,
                'span': '12 seats - 3 executor, 2 scribe, 1 scout, 1 connector,\n'
                        '  1 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 labrat.',
                'roles': {'executor': 3, 'scribe': 2, 'scout': 1, 'connector': 1,
                          'reviewer': 1, 'critic': 1, 'mutation-tester': 1,
                          'sentinel': 1, 'labrat': 1}}))
        arm('arm6-attack-below-floor-caught', 1, lambda: sweep_exit([
            dict(row(kind='attack_share'), id='a', expect='meet',
                 named=['reviewer', 'critic', 'mutation-tester', 'labrat'],
                 floor_pct=26)]))
        arm('arm7-attack-at-floor-meet', 'meet',
            lambda: measure_row(kind='attack_share',
                                named=['reviewer', 'critic', 'mutation-tester'],
                                floor_pct=25))
        arm('arm8-bom-refused', 'setup', lambda: decode_json(
            BOM + b'{}', 'bom.json'))
        arm('arm9-invalid-utf8-refused', 'setup', lambda: decode_json(
            b'\xff\xfe{}', 'bad.json'))
        arm('arm10-zero-rows-refused', 'setup', lambda: sweep(
            {'rows': []}, {'lane': FixtureReader(blobs, listings)}))
        arm('arm11-unresolvable-rev-refused', 'setup',
            lambda: measure(row(kind='seats',
                                wave={'dir': 'wave', 'results': 'results.json',
                                      'rev': 'f' * 40}),
                            {'lane': FixtureReader(blobs, listings)}))
        arm('arm12-declaration-absent-refused', 'setup',
            lambda: measure_row(kind='roles', declaration={
                'form': 'text-tokens', 'path': 'plan.md', 'rev': REV,
                'span': '12 seats - 3 executor, 2 scribe',
                'roles': {'executor': 3, 'scribe': 2, 'wizard': 7}}))
        # round 74: the three rules the round-73 wave measured as unguarded.
        # Each arm is moved by exactly one mutant in
        # tools/wave-reconcile-mutants.spec; the arm names that mutant.
        arm_raises('arm13-printed-undelimited-refused', 'printed-not-in-span',
                   lambda: measure_row(kind='seats',
                                       record={'path': 'report.md', 'rev': REV,
                                               'span': '11 reports', 'printed': 1}))
        arm_raises('arm14-span-not-in-record-refused', 'span-not-in-record',
                   lambda: measure_row(kind='seats',
                                       record={'path': 'report.md', 'rev': REV,
                                               'span': '13 seats', 'printed': 13}))
        arm('arm15-seatreports-top-level-only', 'meet',
            lambda: measure_row(kind='seat_reports',
                                record={'path': 'report.md', 'rev': REV,
                                        'span': '12 seats, 11 reports',
                                        'printed': 12}))
        # round 75: the two round-74 survivors. arm16: a `printed` token that
        # is delimited in the RECORD but not in the bound span must refuse (the
        # M-C mutant binds printed to the whole record). arm17/arm18: the
        # `roles` and `attack_share` branches must bind the record span before
        # measuring (the selective `_record_claim` bypass).
        arm_raises('arm16-printed-span-not-record', 'printed-not-in-span',
                   lambda: measure_row(
                       kind='seats',
                       extra_blobs={(REV, 'late.md'):
                                    b'- The wave: 11 reports; '
                                    b'1 seat filed late.\n'},
                       record={'path': 'late.md', 'rev': REV,
                               'span': '11 reports', 'printed': 1}))
        arm_raises('arm17-record-claim-live-on-roles', 'span-not-in-record',
                   lambda: measure_row(
                       kind='roles',
                       record={'path': 'report.md', 'rev': REV,
                               'span': '13 seats'},
                       declaration={'form': 'spec-items', 'path': 'spec.json',
                                    'rev': REV}))
        arm_raises('arm18-record-claim-live-on-attack-share',
                   'span-not-in-record',
                   lambda: measure_row(
                       kind='attack_share',
                       record={'path': 'report.md', 'rev': REV,
                               'span': '13 seats'},
                       named=['reviewer', 'critic', 'mutation-tester'],
                       floor_pct=25))
    finally:
        shutil.rmtree(work, ignore_errors=True)

    passed = 0
    for name, ok, got, want in results:
        print('SELFTEST %-36s %s (got=%s want=%s)'
              % (name, 'ok' if ok else 'FAIL', got, want))
        if ok:
            passed += 1
    print('WAVE_RECONCILE_SELFTEST: %d/%d pass' % (passed, len(results)))
    return 0 if passed == len(results) == SELFTEST_ARMS else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--repo', default='.',
                    help='lane repo the rows default to (git objects, read-only)')
    ap.add_argument('--extra-root', action='append', default=[],
                    help='NAME=PATH for a row-level root other than `lane`')
    ap.add_argument('--manifest', default='tools/wave-reconcile.json')
    ap.add_argument('--json-out', default=None)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        try:
            return selftest()
        except OSError as exc:
            print('WAVE_RECONCILE error=selftest-setup:%s' % exc, file=sys.stderr)
            return 2
    try:
        return run_manifest(a.manifest, a.repo, a.extra_root,
                            out=a.json_out)
    except SetupError as exc:
        print('WAVE_RECONCILE error=setup:%s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
