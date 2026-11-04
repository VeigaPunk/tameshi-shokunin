#!/usr/bin/env python3
"""tools/registry-figure-bind.py — a gate figure printed in the lane's registry
home must equal the figure its instrument prints now (round 80).

What it answers: *does the self-assessment surface (SKILL.md's latest gate /
probe registry table and `tools/registry.json`) still print the figure the
instrument prints today?* The round-79 non-author closure routed this class as
defect 5: the round-76 registry section still read
`WAVE_RECONCILE_SELFTEST: 19/19 pass` (tool: 23/23) and
`SELFSTATE_SELFTEST: 11/11 pass` over a 20-row population (tool: 14/14 over
22), and the round-79 capability `receipt-bytes binding sweep` had no registry
row at all. A stale registry figure is an overreach in the lane's own
self-description, so this instrument counts mismatches between the two
surfaces instead of trusting either.

The population is declared, never inferred: `tools/registry-figure-bind.json`
names every row. Two surfaces, one verdict rule:

  doc            a markdown table row in `doc` whose first cell is `row_name`;
                 the LAST such row in the file is the live one (a later
                 section supersedes an earlier one); the manifest `figure`
                 regex must match exactly once in that row line.
  registry-json  a `rows[]` entry of `registry` whose `name` is `row_name`;
                 the declared figure is the entry's `expect.stdout_contains`
                 text.

The live figure is the ONE `figure` match in the instrument's stdout, run
from the repo root with the manifest argv; a stdout carrying two matches is a
setup error, never the last one silently. A row measures:

  match    the live figure token is a byte substring of the declared surface
  stale    the surface names a figure and the live token is absent from it
  absent   the named row does not exist on the surface
  error    the instrument could not be measured (never a pass)

Verdict lines:

  REGISTRY_BIND_ROW <id> surface=<doc|registry-json> expect=<match|stale>
                    measured=<match|stale|absent|error> declared=<token|->
                    live=<token|->
  REGISTRY_BIND: rows=N match=M stale=S absent=A error=E unexpected=U

Exit: 0 every row measured its declared expectation (a stale row with
`expect=stale` is the standing red arm and passes); 1 an unexpected row;
2 at least one `error` row, or a manifest-level setup refusal (zero rows,
unreadable manifest, duplicate registry row name, unparsable registry, a
manifest path that is not repo-relative). A per-row error (instrument exit,
live figure absent or not unique, ambiguous doc row) is emitted as an `error`
row and the summary is still printed before exit 2 — never a silent pass.

Read-only over the lane: runs the manifest instruments as subprocesses, writes
nothing. Stdlib only.

Usage:

  python3 -I -X utf8 tools/registry-figure-bind.py --repo .
  python3 -I -X utf8 tools/registry-figure-bind.py --selftest
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SELFTEST_ARMS = 11
SURFACES = ('doc', 'registry-json')
EXPECTS = ('match', 'stale')
MAX_DOC_BYTES = 8 * 1024 * 1024


class SetupError(Exception):
    pass


def _child_env():
    env = dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return env


def read_text(path):
    try:
        with open(path, 'rb') as fh:
            raw = fh.read(MAX_DOC_BYTES + 1)
    except OSError as exc:
        raise SetupError('input-unreadable:%s:%s' % (path, exc))
    if len(raw) > MAX_DOC_BYTES:
        raise SetupError('input-too-large:%s' % path)
    return raw.decode('utf-8', 'replace')


def _manifest_path_ok(rel):
    """A repo-relative POSIX path: no absolute form, no parent segment, no
    backslash, no drive qualifier (round-80 sentinel F4: a manifest could
    select an external registry home and still measure green)."""
    if not isinstance(rel, str) or not rel:
        return False
    if rel.startswith('/') or '\\' in rel or re.match(r'^[A-Za-z]:', rel):
        return False
    return '..' not in rel.split('/')


def _resolve_inside(repo, rel, row_id):
    base = os.path.realpath(repo)
    target = os.path.realpath(os.path.join(repo, rel))
    if target != base and not target.startswith(base + os.sep):
        raise SetupError('path-outside-repo:%s' % row_id)
    return target


def parse_manifest(path):
    text = read_text(path)
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise SetupError('manifest-unparsable:%s:%s' % (path, exc))
    rows = data.get('rows')
    if not isinstance(rows, list) or not rows:
        raise SetupError('manifest-zero-rows:%s' % path)
    out = []
    for row in rows:
        if not isinstance(row, dict):
            raise SetupError('manifest-row-not-object:%s' % path)
        rid = row.get('id')
        surface = row.get('surface')
        name = row.get('row_name')
        figure = row.get('figure')
        expect = row.get('expect')
        instrument = row.get('instrument')
        if not isinstance(rid, str) or not rid:
            raise SetupError('manifest-row-id:%s' % path)
        if surface not in SURFACES:
            raise SetupError('manifest-row-surface:%s:%s' % (rid, surface))
        if not isinstance(name, str) or not name:
            raise SetupError('manifest-row-name:%s' % rid)
        if not isinstance(figure, str) or not figure:
            raise SetupError('manifest-row-figure:%s' % rid)
        try:
            re.compile(figure)
        except re.error as exc:
            raise SetupError('manifest-row-figure-regex:%s:%s' % (rid, exc))
        if expect not in EXPECTS:
            raise SetupError('manifest-row-expect:%s:%s' % (rid, expect))
        if not isinstance(instrument, dict):
            raise SetupError('manifest-row-instrument:%s' % rid)
        argv = instrument.get('argv')
        if not isinstance(argv, list) or not argv \
                or not all(isinstance(a, str) for a in argv):
            raise SetupError('manifest-row-argv:%s' % rid)
        timeout = instrument.get('timeout_s', 300)
        if not isinstance(timeout, int) or timeout <= 0:
            raise SetupError('manifest-row-timeout:%s' % rid)
        if surface == 'doc':
            if not _manifest_path_ok(row.get('doc')):
                raise SetupError('manifest-path-not-repo-relative:%s:doc'
                                 % rid)
        else:
            if not _manifest_path_ok(row.get('registry')):
                raise SetupError('manifest-path-not-repo-relative:%s:registry'
                                 % rid)
        out.append({'id': rid, 'surface': surface, 'row_name': name,
                    'figure': figure, 'expect': expect, 'argv': argv,
                    'timeout_s': timeout,
                    'doc': row.get('doc'), 'registry': row.get('registry')})
    ids = [r['id'] for r in out]
    if len(set(ids)) != len(ids):
        raise SetupError('manifest-duplicate-id:%s' % path)
    return out


def _declared_doc(repo, row):
    path = _resolve_inside(repo, row['doc'], row['id'])
    text = read_text(path)
    want = row['row_name']
    found = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith('|'):
            continue
        cells = [c.strip() for c in stripped.strip('|').split('|')]
        if cells and cells[0] == want:
            found = stripped
    if found is None:
        return None
    matches = re.findall(row['figure'], found)
    if not matches:
        return ''
    if len(matches) > 1:
        raise SetupError('figure-not-unique:%s' % row['id'])
    return matches[0]


def _declared_registry(repo, row):
    path = _resolve_inside(repo, row['registry'], row['id'])
    text = read_text(path)
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise SetupError('registry-unparsable:%s:%s' % (path, exc))
    rows = data.get('rows')
    if not isinstance(rows, list):
        raise SetupError('registry-rows-missing:%s' % path)
    hits = [r for r in rows
            if isinstance(r, dict) and r.get('name') == row['row_name']]
    if not hits:
        return None
    if len(hits) > 1:
        raise SetupError('registry-row-duplicate:%s' % row['id'])
    expect = hits[0].get('expect')
    if not isinstance(expect, dict):
        raise SetupError('registry-row-expect:%s' % row['id'])
    contains = expect.get('stdout_contains', [])
    if not isinstance(contains, list) or \
            not all(isinstance(c, str) for c in contains):
        raise SetupError('registry-row-contains:%s' % row['id'])
    text = '\n'.join(contains)
    # a row that declares no text at all names no figure: absent, never a
    # stale-shaped pass (round-80 executor E1: an empty surface passed an
    # `expect=stale` row without naming anything)
    return text if text.strip() else None


def _live(repo, row):
    try:
        proc = subprocess.run(row['argv'], cwd=repo, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=_child_env(),
                              timeout=row['timeout_s'])
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise SetupError('instrument-unavailable:%s:%s' % (row['id'], exc))
    if proc.returncode != 0:
        raise SetupError('instrument-exit:%s:%s' % (row['id'],
                                                     proc.returncode))
    text = proc.stdout.decode('utf-8', 'replace')
    matches = re.findall(row['figure'], text)
    if not matches:
        raise SetupError('figure-absent-in-live:%s' % row['id'])
    if len(matches) > 1:
        # a stale token printed before the current one must never be silently
        # out-voted: exactly one live figure, or the row is unmeasurable
        raise SetupError('figure-not-unique-live:%s' % row['id'])
    return matches[0]


def measure(repo, row):
    if row['surface'] == 'doc':
        declared = _declared_doc(repo, row)
    else:
        declared = _declared_registry(repo, row)
    live = _live(repo, row)
    if declared is None:
        return 'absent', None, live
    if row['surface'] == 'doc':
        ok = declared == live
    else:
        # exactly one figure-shaped token in the declaration, and it must BE
        # the live one: a row naming both a stale and the live token (or a
        # longer figure that merely contains the live one) measures stale
        tokens = re.findall(row['figure'], declared)
        ok = len(tokens) == 1 and tokens[0] == live
    if declared and ok:
        return 'match', declared, live
    return 'stale', declared, live


def sweep(repo, manifest, out=sys.stdout):
    if not os.path.isdir(repo):
        raise SetupError('repo-not-a-directory:%s' % repo)
    rows = parse_manifest(manifest)
    counts = {'match': 0, 'stale': 0, 'absent': 0, 'error': 0}
    unexpected = 0
    for row in rows:
        try:
            state, declared, live = measure(repo, row)
        except SetupError as exc:
            state, declared, live = 'error', None, None
            out.write('REGISTRY_BIND_ROW %s surface=%s expect=%s '
                      'measured=error detail=%s\n'
                      % (row['id'], row['surface'], row['expect'], exc))
        else:
            out.write('REGISTRY_BIND_ROW %s surface=%s expect=%s '
                      'measured=%s declared=%r live=%r\n'
                      % (row['id'], row['surface'], row['expect'], state,
                         declared, live))
        counts[state] += 1
        if state != row['expect']:
            unexpected += 1
    out.write('REGISTRY_BIND: rows=%d match=%d stale=%d absent=%d error=%d '
              'unexpected=%d\n'
              % (len(rows), counts['match'], counts['stale'], counts['absent'],
                 counts['error'], unexpected))
    if counts['error']:
        return 2
    return 0 if unexpected == 0 else 1


# --- selftest -------------------------------------------------------------

def _fixture(root):
    """A three-surface fixture: SKILL.md, tools/registry.json, tools/fig.py."""
    def put(rel, text):
        path = os.path.join(root, rel)
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, 'w', newline='\n') as fh:
            fh.write(text)

    put('tools/fig.py', "print('TOY: 1/1 pass')\n")
    put('SKILL.md',
        '# toy\n\n### Gate/probe registry — toy\n\n'
        '| Name | Kind | Self-test command |\n|---|---|---|\n'
        '| toy gate | gate | `python3 tools/fig.py` -> `TOY: 1/1 pass` |\n')
    put('tools/registry.json', json.dumps({'schema': 'toy', 'rows': [
        {'name': 'toy-selftest', 'kind': 'selftest',
         'argv': ['python3', 'tools/fig.py'],
         'expect': {'exit': 0, 'stdout_contains': ['TOY: 1/1 pass']}}]}))
    return root


def _manifest(rows):
    return {'schema': 'tameshi-registry-figure-bind-v1', 'rows': rows}


def _row(rid, surface, name, expect='match', figure='TOY: [0-9]+/[0-9]+ pass'):
    row = {'id': rid, 'surface': surface, 'row_name': name,
           'figure': figure, 'expect': expect,
           'instrument': {'argv': [sys.executable, 'tools/fig.py'],
                          'timeout_s': 60}}
    if surface == 'doc':
        row['doc'] = 'SKILL.md'
    else:
        row['registry'] = 'tools/registry.json'
    return row


def selftest(out=sys.stdout):
    ok = 0
    total = SELFTEST_ARMS

    def arm(name, passed, detail=''):
        nonlocal ok
        if passed:
            ok += 1
            out.write('SELFTEST_%s: PASS\n' % name)
        else:
            out.write('SELFTEST_%s: FAIL %s\n' % (name, detail))

    work = tempfile.mkdtemp(prefix='registry-bind-',
                            dir=os.environ.get('TMPDIR') or None)
    try:
        def cli(fx, manifest_path, extra=()):
            proc = subprocess.run(
                [sys.executable, '-I', '-X', 'utf8', os.path.abspath(__file__),
                 '--repo', fx, '--manifest', manifest_path] + list(extra),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180,
                env=_child_env())
            return (proc.returncode,
                    proc.stdout.decode('utf-8', 'replace'),
                    proc.stderr.decode('utf-8', 'replace'))

        def fixture(tag):
            fx = _fixture(os.path.join(work, tag))
            os.makedirs(fx, exist_ok=True)
            _fixture(fx)
            return fx

        def manifest_for(fx, rows, tag):
            mp = os.path.join(work, tag + '.json')
            with open(mp, 'w', newline='\n') as fh:
                json.dump(_manifest(rows), fh)
            return mp

        # arm 1: a registry-json row matching its live figure
        fx1 = fixture('a1')
        rc, txt, err = cli(fx1, manifest_for(
            fx1, [_row('toy-reg', 'registry-json', 'toy-selftest')], 'm1'))
        arm('ARM1_registry_json_match', rc == 0
            and 'REGISTRY_BIND_ROW toy-reg surface=registry-json expect=match '
                'measured=match' in txt
            and 'REGISTRY_BIND: rows=1 match=1 stale=0 absent=0 error=0 '
                'unexpected=0' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 2: a doc row matching its live figure
        rc, txt, err = cli(fx1, manifest_for(
            fx1, [_row('toy-doc', 'doc', 'toy gate')], 'm2'))
        arm('ARM2_doc_match', rc == 0
            and 'REGISTRY_BIND_ROW toy-doc surface=doc expect=match '
                'measured=match' in txt
            and 'REGISTRY_BIND: rows=1 match=1 stale=0 absent=0 error=0 '
                'unexpected=0' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 3: a stale doc figure is measured, and is unexpected by default.
        # Round 80 folds in the registry-shape cheats: a declaration naming
        # BOTH a stale and the live token, and a longer figure that merely
        # contains the live one (`11/1` vs `1/1`) must both measure stale.
        fx3 = fixture('a3')
        with open(os.path.join(fx3, 'SKILL.md'), 'w', newline='\n') as fh:
            fh.write('# toy\n\n| Name | Kind | Self-test command |\n'
                     '|---|---|---|\n'
                     '| toy gate | gate | `TOY: 2/2 pass` |\n')
        rc, txt, err = cli(fx3, manifest_for(
            fx3, [_row('toy-stale', 'doc', 'toy gate')], 'm3'))
        fx3b = fixture('a3b')
        with open(os.path.join(fx3b, 'tools/registry.json'), 'w',
                  newline='\n') as fh:
            json.dump({'schema': 'toy', 'rows': [
                {'name': 'toy-selftest',
                 'expect': {'exit': 0,
                            'stdout_contains': ['TOY: 2/2 pass',
                                                'TOY: 1/1 pass']}}]}, fh)
        rc3b, txt3b, err3b = cli(fx3b, manifest_for(
            fx3b, [_row('toy-both', 'registry-json', 'toy-selftest')], 'm3b'))
        fx3c = fixture('a3c')
        with open(os.path.join(fx3c, 'tools/registry.json'), 'w',
                  newline='\n') as fh:
            json.dump({'schema': 'toy', 'rows': [
                {'name': 'toy-selftest',
                 'expect': {'exit': 0,
                            'stdout_contains': ['TOY: 11/1 pass']}}]}, fh)
        rc3c, txt3c, err3c = cli(fx3c, manifest_for(
            fx3c, [_row('toy-longer', 'registry-json', 'toy-selftest')],
            'm3c'))
        # round 80 mutation-tester: an EMPTY declaration is stale, never a
        # vacuous match (the falsy guard alone was unguarded)
        fx3d = fixture('a3d')
        with open(os.path.join(fx3d, 'tools/registry.json'), 'w',
                  newline='\n') as fh:
            json.dump({'schema': 'toy', 'rows': [
                {'name': 'toy-selftest',
                 'expect': {'exit': 0, 'stdout_contains': []}}]}, fh)
        rc3d, txt3d, err3d = cli(fx3d, manifest_for(
            fx3d, [_row('toy-empty', 'registry-json', 'toy-selftest')],
            'm3d'))
        arm('ARM3_stale_measured', rc == 1
            and 'measured=stale' in txt
            and 'REGISTRY_BIND: rows=1 match=0 stale=1 absent=0 error=0 '
                'unexpected=1' in txt
            and rc3b == 1 and 'measured=stale' in txt3b
            and rc3c == 1 and 'measured=stale' in txt3c
            and rc3d == 1 and 'measured=absent' in txt3d,
            'rc=%r %r %r | both rc=%r | longer rc=%r | empty rc=%r'
            % (rc, txt, err, rc3b, rc3c, rc3d))

        # arm 4: a named row missing from the surface is absent, not stale
        rc, txt, err = cli(fx1, manifest_for(
            fx1, [_row('toy-missing', 'doc', 'not a row')], 'm4'))
        arm('ARM4_absent_row', rc == 1
            and 'measured=absent' in txt
            and 'REGISTRY_BIND: rows=1 match=0 stale=0 absent=1 error=0 '
                'unexpected=1' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 5: a duplicate registry row name is an ambiguous surface
        fx5 = fixture('a5')
        with open(os.path.join(fx5, 'tools/registry.json'), 'w',
                  newline='\n') as fh:
            json.dump({'schema': 'toy', 'rows': [
                {'name': 'toy-selftest', 'expect': {'stdout_contains': ['x']}},
                {'name': 'toy-selftest', 'expect': {'stdout_contains': ['y']}}]},
                fh)
        rc, txt, err = cli(fx5, manifest_for(
            fx5, [_row('toy-dup', 'registry-json', 'toy-selftest')], 'm5'))
        esc = _row('toy-esc', 'doc', 'toy gate')
        esc['doc'] = '../outside.md'
        rc5b, txt5b, err5b = cli(fx1, manifest_for(fx1, [esc], 'm5b'))
        absrow = _row('toy-abs', 'registry-json', 'toy-selftest')
        absrow['registry'] = '/etc/registry.json'
        rc5c, txt5c, err5c = cli(fx1, manifest_for(fx1, [absrow], 'm5c'))
        arm('ARM5_registry_duplicate_refused', rc == 2
            and 'measured=error detail=registry-row-duplicate:toy-dup' in txt
            and 'REGISTRY_BIND: rows=1 match=0 stale=0 absent=0 error=1 '
                'unexpected=1' in txt
            and rc5b == 2 and 'manifest-path-not-repo-relative' in err5b
            and rc5c == 2 and 'manifest-path-not-repo-relative' in err5c,
            'rc=%r %r %r | parent rc=%r %r | abs rc=%r %r'
            % (rc, txt, err, rc5b, err5b, rc5c, err5c))

        # arm 6: an unparsable registry is a setup refusal, never a pass
        fx6 = fixture('a6')
        with open(os.path.join(fx6, 'tools/registry.json'), 'w',
                  newline='\n') as fh:
            fh.write('{not json')
        rc, txt, err = cli(fx6, manifest_for(
            fx6, [_row('toy-bad', 'registry-json', 'toy-selftest')], 'm6'))
        arm('ARM6_registry_unparsable_refused', rc == 2
            and 'measured=error detail=registry-unparsable' in txt
            and 'error=1' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 7: an instrument that exits non-zero is unmeasurable (setup)
        fx7 = fixture('a7')
        with open(os.path.join(fx7, 'tools/fig.py'), 'w', newline='\n') as fh:
            fh.write("import sys\nprint('TOY: 1/1 pass')\nsys.exit(3)\n")
        rc, txt, err = cli(fx7, manifest_for(
            fx7, [_row('toy-exit', 'doc', 'toy gate')], 'm7'))
        arm('ARM7_instrument_exit_refused', rc == 2
            and 'measured=error detail=instrument-exit:toy-exit:3' in txt
            and 'error=1' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 8: an instrument whose stdout lacks the figure is unmeasurable;
        # round 80 folds in the duplicate-live-token case — a stale token
        # printed before the live one must never be silently out-voted.
        fx8 = fixture('a8')
        with open(os.path.join(fx8, 'tools/fig.py'), 'w', newline='\n') as fh:
            fh.write("print('nothing useful')\n")
        rc, txt, err = cli(fx8, manifest_for(
            fx8, [_row('toy-nofig', 'doc', 'toy gate')], 'm8'))
        fx8b = fixture('a8b')
        with open(os.path.join(fx8b, 'tools/fig.py'), 'w', newline='\n') as fh:
            fh.write("print('TOY: 2/2 pass')\nprint('TOY: 1/1 pass')\n")
        rc8b, txt8b, err8b = cli(fx8b, manifest_for(
            fx8b, [_row('toy-twice', 'doc', 'toy gate')], 'm8b'))
        arm('ARM8_live_figure_absent_refused', rc == 2
            and 'measured=error detail=figure-absent-in-live:toy-nofig' in txt
            and 'error=1' in txt
            and rc8b == 2
            and 'measured=error detail=figure-not-unique-live:toy-twice' in txt8b,
            'rc=%r %r %r | twice rc=%r %r'
            % (rc, txt, err, rc8b, txt8b))

        # arm 9: the LAST row of a repeated name is the live one (a later
        # section supersedes an earlier one)
        fx9 = fixture('a9')
        with open(os.path.join(fx9, 'SKILL.md'), 'w', newline='\n') as fh:
            fh.write('# toy\n\n| Name | Kind | Self-test command |\n'
                     '|---|---|---|\n'
                     '| toy gate | gate | `TOY: 2/2 pass` |\n\n'
                     '### Gate/probe registry — later\n\n'
                     '| Name | Kind | Self-test command |\n|---|---|---|\n'
                     '| toy gate | gate | `TOY: 1/1 pass` |\n')
        rc, txt, err = cli(fx9, manifest_for(
            fx9, [_row('toy-latest', 'doc', 'toy gate')], 'm9'))
        arm('ARM9_latest_row_wins', rc == 0
            and "live='TOY: 1/1 pass'" in txt
            and 'measured=match' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 10: a zero-row manifest is refused
        rc, txt, err = cli(fx1, manifest_for(fx1, [], 'm10'))
        arm('ARM10_zero_rows_refused', rc == 2
            and 'REGISTRY_BIND:' not in txt and 'manifest-zero-rows' in err,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 11: a standing red arm (expect=stale) passes only when stale
        rc, txt, err = cli(fx3, manifest_for(
            fx3, [_row('toy-red', 'doc', 'toy gate', expect='stale')], 'm11'))
        arm('ARM11_declared_stale_arm', rc == 0
            and 'REGISTRY_BIND_ROW toy-red surface=doc expect=stale '
                'measured=stale' in txt
            and 'unexpected=0' in txt,
            'rc=%r %r %r' % (rc, txt, err))

    finally:
        shutil.rmtree(work, ignore_errors=True)

    out.write('REGISTRY_BIND_SELFTEST: %d/%d pass\n' % (ok, total))
    return 0 if ok == total == SELFTEST_ARMS else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--repo', default='.')
    ap.add_argument('--manifest', default='tools/registry-figure-bind.json')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        return sweep(os.path.abspath(a.repo), a.manifest)
    except SetupError as exc:
        sys.stderr.write('REGISTRY_BIND error=setup %s\n' % exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
