#!/usr/bin/env python3
"""tools/selfstate-freshness.py — R75-C2 candidate stub (T75W1M1 battery).

Faithful to the frozen plan contract:
  * a manifest declares rows of mode `capability` (located by exact first-cell
    name inside the doc's `## Capabilities` section at `--doc-rev`) or `span`
    (the figure regex is searched in the whole doc text at `--doc-rev`);
  * every row carries the figure regex and the instrument (path, pinned rev,
    argv); the instrument is extracted from git objects at its rev and run
    `python -I -X utf8` with TMPDIR honoured, and its stdout is searched with
    the same regex;
  * a row measures `match` when the doc's figure equals the instrument's own
    token, `stale` otherwise; `expect: match|stale` makes a divergence
    `unexpected`;
  * an absent capability row, an absent doc figure, an absent instrument figure
    or a zero-row manifest is setup exit 2, never a pass;
  * the doc bytes come from the revision-bound reader, never the worktree.

Output: `SELFSTATE_ROW <id> expect=<e> measured=<state> ok|UNEXPECTED`
        `SELFSTATE_TOKEN <id> doc=<token> instrument=<token>`
        `SELFSTATE: rows=N match=M stale=S unexpected=U` (exit 0 iff 0)
        `SELFSTATE_FRESHNESS_SELFTEST: N/N pass` under `--selftest`.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SELFTEST_ARMS = 8


class SetupError(Exception):
    pass


def capabilities_rows(doc_text):
    """Return {exact first cell: row line} from the `## Capabilities` section."""
    rows = {}
    inside = False
    for line in doc_text.splitlines():
        if line.startswith('## Capabilities'):
            inside = True
            continue
        if inside and line.startswith('## '):
            break
        if inside and line.startswith('|') and not line.startswith('|---'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if len(cells) >= 2 and cells[0] and cells[0] != 'Capability':
                rows[cells[0]] = line
    return rows


class GitReader(object):
    """Doc bytes from git objects at a named revision (never the worktree)."""

    def __init__(self, repo):
        self.repo = repo

    def text(self, rev, path):
        if not re.fullmatch(r'[0-9a-f]{6,40}', rev or ''):
            raise SetupError('rev-unresolvable:%s' % (rev,))
        proc = subprocess.run(['git', '-C', self.repo, 'cat-file', 'blob',
                               '%s:%s' % (rev, path)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            raise SetupError('git-failed:%s:%s' % (
                path, proc.stderr.decode('utf-8', 'replace').strip()[:200]))
        return proc.stdout.decode('utf-8')


class FixtureReader(object):
    def __init__(self, docs):
        self.docs = docs

    def text(self, rev, path):
        key = (rev, path)
        if key not in self.docs:
            raise SetupError('rev-unresolvable-or-path-absent:%s:%s' % key)
        return self.docs[key].decode('utf-8')


def load_doc(repo, rev, path, reader):
    """The doc is read at `rev` through the revision-bound reader."""
    return reader.text(rev, path)


def git_blob(repo, rev, path):
    if not re.fullmatch(r'[0-9a-f]{6,40}', rev or ''):
        raise SetupError('rev-unresolvable:%s' % (rev,))
    proc = subprocess.run(['git', '-C', repo, 'cat-file', 'blob',
                           '%s:%s' % (rev, path)],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise SetupError('git-failed:%s:%s' % (
            path, proc.stderr.decode('utf-8', 'replace').strip()[:200]))
    return proc.stdout


class RealRunner(object):
    """Extract the instrument at its pinned rev and run `python -I -X utf8`."""

    def __init__(self, repo):
        self.repo = repo

    def __call__(self, rev, path, argv):
        data = git_blob(self.repo, rev, path)
        work = tempfile.mkdtemp(prefix='selfstate-instr-',
                                dir=os.environ.get('TMPDIR') or None)
        try:
            target = os.path.join(work, os.path.basename(path))
            with open(target, 'wb') as fh:
                fh.write(data)
            proc = subprocess.run(
                [sys.executable, '-I', '-X', 'utf8', target] + list(argv),
                cwd=self.repo, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            return proc.stdout.decode('utf-8', 'replace')
        finally:
            shutil.rmtree(work, ignore_errors=True)


def measure_row(row, doc_text, runner):
    """Return (state, doc_token, instrument_token)."""
    mode = row.get('mode')
    if mode == 'capability':
        caps = capabilities_rows(doc_text)
        line = caps.get(row['capability'])
        if line is None:
            raise SetupError('capability-absent:%s' % row['id'])
        found = re.search(row['figure'], line)
        if found is None:
            raise SetupError('doc-figure-absent:%s' % row['id'])
        doc_token = found.group(0)
    elif mode == 'span':
        region = doc_text
        if row.get('span'):
            start = doc_text.find(row['span'])
            if start < 0:
                raise SetupError('doc-span-absent:%s' % row['id'])
            region = doc_text[start:start + len(row['span'])]
        found = re.search(row['figure'], region)
        if found is None:
            raise SetupError('doc-figure-absent:%s' % row['id'])
        doc_token = found.group(0)
    else:
        raise SetupError('mode-unknown:%s' % row['id'])

    inst = row.get('instrument') or {}
    for key in ('path', 'rev', 'argv'):
        if key not in inst:
            raise SetupError('instrument-missing-%s:%s' % (key, row['id']))
    stdout = runner(inst['rev'], inst['path'], inst['argv'])
    found = re.search(row['figure'], stdout)
    if found is None:
        raise SetupError('instrument-figure-absent:%s' % row['id'])
    measured_token = found.group(0)
    state = 'match' if doc_token == measured_token else 'stale'
    return state, doc_token, measured_token


def sweep(manifest, doc_text, reader, runner):
    """Return (rows_out, match, stale, unexpected). Raises before any effect."""
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
        if row.get('expect') not in ('match', 'stale'):
            raise SetupError('row-expect-invalid:%s' % row['id'])
        if row.get('mode') not in ('capability', 'span'):
            raise SetupError('row-mode-invalid:%s' % row['id'])
        if not isinstance(row.get('figure'), str) or not row['figure']:
            raise SetupError('row-figure-absent:%s' % row['id'])
    out = []
    match = stale = unexpected = 0
    for row in rows:
        state, doc_token, measured_token = measure_row(row, doc_text, runner)
        if state == 'match':
            match += 1
        else:
            stale += 1
        ok = state == row['expect']
        if not ok:
            unexpected += 1
        out.append({'id': row['id'], 'expect': row['expect'],
                    'state': state, 'ok': ok, 'doc_token': doc_token,
                    'instrument_token': measured_token})
    return out, match, stale, unexpected


def load_manifest(path):
    try:
        with open(path, 'rb') as fh:
            raw = fh.read()
    except OSError as exc:
        raise SetupError('manifest-unreadable:%s:%s' % (path, exc))
    try:
        return json.loads(raw.decode('utf-8'))
    except (UnicodeDecodeError, ValueError) as exc:
        raise SetupError('manifest-unparsable:%s:%s' % (path, exc))


def run_manifest(repo, manifest_path, doc_path, doc_rev):
    manifest = load_manifest(manifest_path)
    reader = GitReader(repo)
    doc_text = load_doc(repo, doc_rev, doc_path, reader)
    rows, match, stale, unexpected = sweep(manifest, doc_text, reader,
                                          RealRunner(repo))
    for row in rows:
        print('SELFSTATE_ROW %s expect=%s measured=%s %s'
              % (row['id'], row['expect'], row['state'],
                 'ok' if row['ok'] else 'UNEXPECTED'))
        print('SELFSTATE_TOKEN %s doc=%s instrument=%s'
              % (row['id'], row['doc_token'], row['instrument_token']))
    print('SELFSTATE: rows=%d match=%d stale=%d unexpected=%d'
          % (len(rows), match, stale, unexpected))
    return 0 if unexpected == 0 else 1


# --- selftest -------------------------------------------------------------
REV = 'b' * 40
DOC = (
    '# SCORECARD\n\n'
    '## Capabilities\n\n'
    '| Capability | What it can now do | Evidence | Round |\n'
    '|---|---|---|---|\n'
    '| alpha probe | demo | `ALPHA: 5/5 pass` | 1 |\n'
    '| beta probe | demo | `BETA: rows=3 met=3 unexpected=0` | 2 |\n'
    '| gamma probe | demo | `GAMMA: 4/4 pass` | 3 |\n\n'
    '## Round-74\n\n'
    '- frozen: `ADDRANGE: rows=6 met=6 unexpected=0`\n'
)
STDOUT = {
    'tools/alpha.py': 'ALPHA: 5/5 pass\n',
    'tools/beta.py': 'BETA: rows=9 met=9 unexpected=0\n',
    'tools/gamma.py': 'GAMMA: 7/7 pass\n',
    'tools/addr.py': 'ADDRANGE: rows=11 met=11 unexpected=0\n',
}


def fixture_runner(rev, path, argv):
    return STDOUT[path]


def selftest():
    results = []

    def arm(name, cond, got, want):
        results.append((name, bool(cond), got, want))

    def arm_raises(name, prefix, fn):
        try:
            fn()
        except SetupError as exc:
            got = str(exc)
            results.append((name, got.startswith(prefix),
                            'setup:' + got.split(':')[0], 'setup:' + prefix))
            return
        results.append((name, False, 'no-refusal', 'setup:' + prefix))

    reader = FixtureReader({(REV, 'SCORECARD.md'): DOC.encode('utf-8')})

    alpha = {'id': 'r-alpha', 'mode': 'capability',
             'capability': 'alpha probe', 'figure': r'ALPHA: \d+/\d+ pass',
             'expect': 'match',
             'instrument': {'path': 'tools/alpha.py', 'rev': REV,
                            'argv': ['--selftest']}}
    beta = {'id': 'r-beta', 'mode': 'capability',
            'capability': 'beta probe',
            'figure': r'BETA: rows=\d+ met=\d+ unexpected=\d+',
            'expect': 'stale',
            'instrument': {'path': 'tools/beta.py', 'rev': REV,
                           'argv': ['--repo', '.']}}
    gamma = {'id': 'r-gamma', 'mode': 'capability',
             'capability': 'gamma probe', 'figure': r'GAMMA: \d+/\d+ pass',
             'expect': 'stale',
             'instrument': {'path': 'tools/gamma.py', 'rev': REV,
                            'argv': ['--selftest']}}
    frozen = {'id': 'r-frozen', 'mode': 'span',
              'span': 'ADDRANGE: rows=6 met=6 unexpected=0',
              'figure': r'ADDRANGE: rows=\d+ met=\d+ unexpected=0',
              'expect': 'stale',
              'instrument': {'path': 'tools/addr.py', 'rev': REV,
                             'argv': ['--repo', '.']}}

    def run(rows):
        return sweep({'rows': rows}, DOC, reader, fixture_runner)

    # arm1: the measured token is the instrument's, never a copy of the doc.
    state, doc_tok, meas_tok = measure_row(gamma, DOC, fixture_runner)
    arm('arm1-measured-is-instrument-not-doc',
        state == 'stale' and doc_tok == 'GAMMA: 4/4 pass'
        and meas_tok == 'GAMMA: 7/7 pass',
        'state=%s meas=%s' % (state, meas_tok), 'stale/GAMMA: 7/7 pass')
    # arm2: a row whose expect disagrees with its state is unexpected.
    rows, match, stale, unexpected = run([dict(gamma, expect='match')])
    arm('arm2-expect-divergence-is-unexpected', unexpected == 1,
        'unexpected=%d' % unexpected, 'unexpected=1')
    # arm3: an absent capability row is a setup refusal, never a match.
    try:
        arm_raises('arm3-absent-capability-refused', 'capability-absent',
                   lambda: run([dict(alpha, id='r-absent',
                                     capability='absent probe')]))
    except Exception:
        raise
    # arm4: a zero-row manifest is refused.
    arm_raises('arm4-zero-rows-refused', 'zero-rows',
               lambda: sweep({'rows': []}, DOC, reader, fixture_runner))
    # arm5: the doc comes from --doc-rev, never from the worktree.
    work = tempfile.mkdtemp(prefix='selfstate-docrev-',
                            dir=os.environ.get('TMPDIR') or None)
    try:
        decoy = os.path.join(work, 'SCORECARD.md')
        with open(decoy, 'wb') as fh:
            fh.write(b'## Capabilities\n| alpha probe | ALPHA: 9/9 pass |\n')
        text = load_doc(work, REV, 'SCORECARD.md', reader)
        arm('arm5-doc-rev-bound-not-worktree', text == DOC,
            'from=%s' % ('reader' if text == DOC else 'worktree'), 'reader')
    finally:
        shutil.rmtree(work, ignore_errors=True)
    # arm6: a live row whose doc figure equals its instrument reads match.
    rows, match, stale, unexpected = run([alpha])
    arm('arm6-live-row-match', rows[0]['state'] == 'match' and rows[0]['ok'],
        'state=%s' % rows[0]['state'], 'match')
    # arm7: the frozen red row MEASURES stale on every sweep.
    rows, match, stale, unexpected = run([frozen])
    arm('arm7-frozen-row-measures-stale',
        rows[0]['state'] == 'stale' and rows[0]['ok'], 
        'state=%s' % rows[0]['state'], 'stale')
    # arm8: the per-row token line carries the instrument's own stdout token.
    rows, match, stale, unexpected = run([beta])
    arm('arm8-token-line-carries-instrument-token',
        rows[0]['instrument_token'] == 'BETA: rows=9 met=9 unexpected=0'
        and rows[0]['doc_token'] == 'BETA: rows=3 met=3 unexpected=0',
        'instrument=%s' % rows[0]['instrument_token'],
        'BETA: rows=9 met=9 unexpected=0')

    passed = 0
    for name, ok, got, want in results:
        print('SELFTEST %-40s %s (got=%s want=%s)'
              % (name, 'ok' if ok else 'FAIL', got, want))
        if ok:
            passed += 1
    print('SELFSTATE_FRESHNESS_SELFTEST: %d/%d pass' % (passed, len(results)))
    return 0 if passed == len(results) == SELFTEST_ARMS else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--repo', default='.')
    ap.add_argument('--manifest', default='tools/selfstate-freshness.json')
    ap.add_argument('--doc', default='SCORECARD.md')
    ap.add_argument('--doc-rev')
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.doc_rev:
        print('SETUP_ERROR doc-rev-required', file=sys.stderr)
        return 2
    try:
        return run_manifest(args.repo, args.manifest, args.doc, args.doc_rev)
    except SetupError as exc:
        print('SETUP_ERROR %s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
