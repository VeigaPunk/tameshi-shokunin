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

Binding rules (twenty-three arms: seats-meet/mismatch, seat_reports-drift,
roles-spec/text-drift, attack-below-floor/at-floor, five setup refusals, - from
round 74 - arm13 delimited-token, arm14 record-span-substring and arm15
seat_reports-top-level-only, the three rules round 73 carried as arm gaps and
measured as survivors: `delimited := True` 12/12, the span-rule removal 12/12,
`seat_reports` any-depth 12/12 plus the standing sweep, and - from round 75 -
arm16 printed-span-not-record, arm17 record-claim-live-on-roles and arm18
record-claim-live-on-attack-share, the two round-74 survivors: a `printed` token
delimited in the record but outside the bound span, and the selective
`_record_claim` bypass on the `roles` and `attack_share` branches. Each new arm
names its mutant in `tools/wave-reconcile-mutants.spec`; from round 76
arm19 seat_reports-printed-required and arm20 nested-listing-recursion - the
first REAL git fixture, S305 - and from round 78 arm20's leftover
post-condition plus arm21 pinned-rev-listing-at-head-drift, the two survivors
the round-77 wave named; from round 79 arm22 leftover-detector-positive and
arm23 head-equals-rev-refused, the two survivors the round-78 wave named -
the leak detector had no positive-branch exercise and the pinned fixture's own
HEAD != rev guard had none):

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

SELFTEST_ARMS = 23
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
        _record_claim(row, readers)
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


GIT_FIXTURE_PREFIX = 'wave-reconcile-git-'


def _leftover(path):
    """1 when a fixture path survived its cleanup, else None.

    Round 79: the round-78 wave's `w1-leak-scan-empty` mutant (a detector that
    always reports clean) survived 21/21 because no arm positively exercised
    the leak branch — a healthy cleanup produces no leak, so arms 20/21 only
    ever measured the clean branch. arm22 calls this function on a live path
    and on a removed path, so the detector's two branches are both measured.
    """
    return 1 if os.path.exists(path) else None


def _fixture_git(fix):
    def g(*args):
        proc = subprocess.run(['git', '-C', fix] + list(args),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            raise SetupError('git-fixture-failed:%s'
                             % proc.stderr.decode('utf-8', 'replace')[:120])
        return proc.stdout
    return g


def _build_listing_fixture(fix, mode, second_commit=True):
    """Build a wave-reconcile git fixture in `fix`; return the pinned rev.

    mode='nested': one commit; `wave/one.md` plus `wave/nested/two.md` and the
                   record `report.md`.
    mode='pinned': rev1 carries the record and `wave/one.md`; rev2 (HEAD) adds
                   `wave/two.md`, so a pinned listing differs from a HEAD
                   listing. `second_commit=False` leaves HEAD == rev ON
                   PURPOSE: the builder then refuses the degenerate fixture
                   (`git-fixture-head-equals-rev`), and arm23 measures that
                   refusal (round-78 wave seat M1's `w2-head-guard-removed`
                   mutant survived because nothing exercised the guard).
    """
    g = _fixture_git(fix)
    g('init', '-q')
    top = g('rev-parse', '--show-toplevel').decode().strip()
    if os.path.realpath(top) != os.path.realpath(fix):
        raise SetupError('git-fixture-misroot:%s' % top)
    os.makedirs(os.path.join(fix, 'wave'))
    with open(os.path.join(fix, 'wave', 'one.md'), 'w',
              encoding='utf-8') as fh:
        fh.write('one\n')
    if mode == 'nested':
        os.makedirs(os.path.join(fix, 'wave', 'nested'))
        with open(os.path.join(fix, 'wave', 'nested', 'two.md'), 'w',
                  encoding='utf-8') as fh:
            fh.write('two\n')
    elif mode != 'pinned':
        raise SetupError('git-fixture-mode-unknown:%s' % mode)
    with open(os.path.join(fix, 'report.md'), 'w', encoding='utf-8') as fh:
        fh.write('1 seat report\n')
    g('add', '-A')
    g('-c', 'user.name=tameshi-fixture',
      '-c', 'user.email=tameshi@shokunin.local',
      '-c', 'commit.gpgsign=false', 'commit', '-q', '-m', 'rev1')
    rev = g('rev-parse', 'HEAD').decode().strip()
    if mode == 'nested':
        return rev
    if second_commit:
        with open(os.path.join(fix, 'wave', 'two.md'), 'w',
                  encoding='utf-8') as fh:
            fh.write('two\n')
        g('add', '-A')
        g('-c', 'user.name=tameshi-fixture',
          '-c', 'user.email=tameshi@shokunin.local',
          '-c', 'commit.gpgsign=false', 'commit', '-q', '-m', 'rev2')
        head = g('rev-parse', 'HEAD').decode().strip()
    else:
        head = rev
    if head == rev:
        raise SetupError('git-fixture-head-equals-rev')
    return rev


def _listing_measure(fix, rev):
    return measure({'id': 'pinned-rev-listing',
                    'kind': 'seat_reports',
                    'record': {'path': 'report.md', 'rev': rev,
                               'span': '1 seat report', 'printed': 1},
                    'wave': {'dir': 'wave', 'results': 'report.md',
                             'rev': rev}},
                   {'lane': GitReader(fix)})[0]


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
        # round 76: the printed-less seat_reports bypass (round-75 carry,
        # T75W1R1). A seat_reports row whose record carries NO `printed` value
        # must refuse; the bypass mutant drops require_printed in this branch
        # only, so printed=None reaches the comparison and the detail
        # formatting raises TypeError — the wrapper catches that crash and the
        # arm fails on its named refusal instead of crashing the suite.
        def _seatreports_printed_required():
            try:
                return measure_row(
                    kind='seat_reports',
                    record={'path': 'report.md', 'rev': REV,
                            'span': '12 seats, 11 reports'})
            except SetupError as exc:
                return 'setup:' + str(exc).split(':')[0]
            except TypeError:
                return 'printed-none-reached-comparison'
        arm('arm19-seatreports-printed-required',
            'setup:record-printed-absent', _seatreports_printed_required)
        # round 77: the production git reader's recursion is unprotected by the
        # dictionary-backed fixture readers (round-76 wave seat M1 measured a
        # `git-listing-recursion-removed` mutant surviving every arm). This arm
        # builds a REAL git fixture (mkdtemp + `git -C init`, toplevel verified
        # equal to the fixture root per the lane's git-fixture rule, removed in
        # finally) whose `wave/` dir holds one top-level report and one nested
        # report: a recursive listing yields the top-level file and excludes the
        # nested one, while `ls-tree` without -r yields the tree entry itself
        # and counts zero. S305: `-r` recurses into sub-trees.
        # Round 78 closes the two survivors the round-77 wave named: arm20 now
        # carries a leftover post-condition (a cleanup-deleted mutant stayed
        # green 20/20 and leaked one fixture per run) and arm21 builds a
        # TWO-commit fixture so the pinned rev differs from HEAD (a
        # `git-listing-uses-head` mutant stayed green 20/20 because the
        # single-commit fixture made HEAD == rev).
        def _nested_listing_arm():
            fix = tempfile.mkdtemp(prefix=GIT_FIXTURE_PREFIX,
                                   dir=os.environ.get('TMPDIR') or None)
            try:
                rev = _build_listing_fixture(fix, 'nested')
                got = _listing_measure(fix, rev)
            finally:
                # arm20 cleanup (anchored: the mutant spec deletes THIS line)
                shutil.rmtree(fix, ignore_errors=True)
            # The post-condition asks whether THIS fixture survived its
            # cleanup, never whether the shared temp dir gained an entry: a
            # directory scan is not concurrency-safe (round-78 simplifier
            # measured a spurious leak:1 in 12/12 concurrent trials).
            if _leftover(fix) is not None:
                return 'leak:1'
            return got
        arm('arm20-nested-listing-recursion', 'meet', _nested_listing_arm)

        # arm21: the fixture is TWO commits deep. The record and the wave dir
        # live in rev1; rev2 (HEAD) adds `wave/two.md`. A reader that resolves
        # the row's rev sees one top-level report and meets the printed 1; a
        # reader that resolves HEAD sees two and drifts. gitrevisions: "HEAD
        # names the commit on which you based the changes in the working tree"
        # — a revision argument, never the argument's substitute.
        def _pinned_rev_listing_arm():
            fix = tempfile.mkdtemp(prefix=GIT_FIXTURE_PREFIX,
                                   dir=os.environ.get('TMPDIR') or None)
            try:
                rev = _build_listing_fixture(fix, 'pinned')
                got = _listing_measure(fix, rev)
            finally:
                shutil.rmtree(fix, ignore_errors=True)
            if _leftover(fix) is not None:
                return 'leak:1'
            return got
        arm('arm21-pinned-rev-listing-at-head-drift', 'meet',
            _pinned_rev_listing_arm)

        # arm22 (round 79): the leftover detector is measured on BOTH branches.
        # A healthy cleanup never leaks, so arms 20/21 cannot positively
        # exercise the detector: the round-78 wave's `w1-leak-scan-empty`
        # mutant (always clean) survived 21/21. This arm calls the detector on
        # a live fixture path (must report 1) and on the same path after its
        # removal (must report None).
        def _leftover_positive_arm():
            fix = tempfile.mkdtemp(prefix=GIT_FIXTURE_PREFIX,
                                   dir=os.environ.get('TMPDIR') or None)
            try:
                if _leftover(fix) != 1:
                    return 'detector-blind:live'
            finally:
                shutil.rmtree(fix, ignore_errors=True)
            if _leftover(fix) is not None:
                return 'detector-blind:clean'
            return 'meet'
        arm('arm22-leftover-detector-positive', 'meet',
            _leftover_positive_arm)

        # arm23 (round 79): the pinned fixture's own HEAD != rev precondition
        # is measured. `second_commit=False` builds the degenerate fixture on
        # purpose; the builder must refuse it (round-78 wave seat M1's
        # `w2-head-guard-removed` mutant survived because no arm reached the
        # guard, so a deleted guard left the fixture silently vacuous).
        def _head_guard_arm():
            fix = tempfile.mkdtemp(prefix=GIT_FIXTURE_PREFIX,
                                   dir=os.environ.get('TMPDIR') or None)
            try:
                try:
                    _build_listing_fixture(fix, 'pinned', second_commit=False)
                except SetupError as exc:
                    if str(exc).startswith('git-fixture-head-equals-rev'):
                        return 'meet'
                    raise
                return 'guard-absent'
            finally:
                shutil.rmtree(fix, ignore_errors=True)
        arm('arm23-head-equals-rev-refused', 'meet', _head_guard_arm)
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
