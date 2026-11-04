#!/usr/bin/env python3
r"""tools/selfstate-freshness.py — a record's live capability figures must
still be the figures the lane's own instruments print (round 75; closes the
round-74 closure defect 3: two live `## Capabilities` rows quoted figures the
tip tools no longer printed, and nothing in the lane noticed).

What it answers: *is every figure the SCORECARD declares for a capability
still what the named instrument prints at the revision the row pins?* The
pre-freeze control (`.ufo/evidence/round-75/selfstate-control-scan.py`) read
the table at the round-74 base and measured seven stale live figures; this
instrument GENERALIZES that control into a standing sweep with a declared
population, a pinned instrument revision per row, and setup refusals instead
of silent passes.

Two row modes:

  capability  locate the table row in the `## Capabilities` section whose
              FIRST CELL is exactly the row's `capability` string (the scan
              stops at the next `## ` heading); the figure is extracted from
              that row line with the row's `figure` regex.
  span        bind a LITERAL byte span of the doc (the span must be a byte
              substring of the doc bytes); the figure is extracted from the
              span with the same `figure` regex. A span row is how a frozen
              historical statement stays measurable after the live cell it
              cites has been superseded.

Measurement: the row's instrument is extracted with
`git cat-file blob <rev>:<path>` into a fresh temp directory (never the
worktree bytes), written at its repo-relative path — repo-shaped because two
lane instruments re-invoke themselves by `__file__` neighbour
(`quoted-line-exists.py:442`) or copy a frozen support blob from
`Path(__file__).parent.parent` (`rekey-cost.py:240`); the support blob is
materialized from the SAME pinned revision into the same temp root. The
extracted file is run as `python3 -I -X utf8 <extracted> <argv...>` with
`cwd=repo`, the caller's environment (so `TMPDIR` is honoured exactly as the
lane contract requires), and a bounded timeout. The SAME `figure` regex then
extracts the measured token from the instrument's stdout. A row measures

  match   the doc token equals the instrument token
  stale   it does not

`expect` is the row's declared state (`match` | `stale`), so a frozen red row
MEASURES its divergence on every sweep instead of assuming it away. A row
whose measured state differs from `expect` is counted in `unexpected`.

Verdict lines (the instrument-exit field is evidence only; the lane's
instruments legitimately exit 1 while still printing a standing red arm):

  SELFSTATE_ROW <id> capability=<name> expect=<e> measured=<m> ok doc_figure=<q> measured_figure=<g> instrument_exit=<n>
  SELFSTATE_ROW <id> expect=<e> measured=<m> ok span_figure=<q> measured_figure=<g> instrument_exit=<n>
  SELFSTATE: rows=N match=M stale=S unexpected=U

`match`/`stale` in the summary count the MEASURED states; `unexpected`
counts rows whose measured state differs from `expect`.

Exit map: 0 = every row measured its declared expectation; 1 = at least one
did not; 2 = usage/setup. Setup refusals happen BEFORE any row effect (no
partial row output, no summary): zero rows; a malformed row; an unknown mode;
an unknown `expect`; a duplicate id; an invalid or absent figure regex; a
capability absent from (or ambiguous in) the `## Capabilities` table; a span
absent from the doc; an unresolvable instrument revision or blob; an
instrument whose stdout carries no token for the row's figure regex; an
instrument timeout. Nothing is certified from an unreadable input.

Selftest (`--selftest`): hermetic — a fixture doc string and a canned
instrument stdout per row, no git, no lane subprocess. Nine arms: match,
stale measured, frozen-span stale, absent capability refused, absent figure
refused, zero rows refused, unknown expect refused, unknown mode refused, and
an instrument whose stdout lacks the figure refused (a setup refusal, never
a match).

Usage:

  python3 -I -X utf8 tools/selfstate-freshness.py --selftest
  python3 -I -X utf8 tools/selfstate-freshness.py --repo . \\
      --manifest tools/selfstate-freshness.json --doc-rev 21ef81e9
"""

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SELFTEST_ARMS = 9
MODES = ('capability', 'span')
EXPECTS = ('match', 'stale')
BOM = b'\xef\xbb\xbf'
CAPS_HEADING = '## Capabilities'
INSTRUMENT_TIMEOUT = 600
# Location-dependent lane instruments read support bytes relative to their own
# path: rekey-cost.py:240 copies `Path(__file__).resolve().parent.parent /
# '.ufo/evidence/round-18/measure.py'` into its fixture. The extraction root is
# therefore repo-shaped and this blob is materialized from the SAME pinned
# revision (best effort: absent at a rev means the instrument fails on its own
# and its row refuses as instrument-figure-absent, never a silent pass).
SUPPORT_BLOBS = ('.ufo/evidence/round-18/measure.py',)


class SetupError(Exception):
    pass


def _rev_ok(rev):
    return isinstance(rev, str) and re.fullmatch(r'[0-9a-f]{6,40}', rev) is not None


def _safe_relpath(path):
    """A repo-relative path that cannot escape the extraction root."""
    if not isinstance(path, str) or not path or path.startswith('/') or '\\' in path:
        return False
    parts = path.split('/')
    return all(part not in ('', '.', '..') for part in parts)


def decode_text(raw, label):
    """Strict UTF-8, BOM refused (S066 §8.1: a BOM is not part of the text)."""
    if raw.startswith(BOM):
        raise SetupError('bom-present:%s' % label)
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise SetupError('not-utf8:%s:%s' % (label, exc))


class GitReader(object):
    """Read blobs from git objects at a named revision (never a worktree)."""

    def __init__(self, root):
        self.root = root

    def _git(self, *args):
        proc = subprocess.run(['git', '-C', self.root] + list(args),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return proc

    def blob(self, rev, path):
        if not _rev_ok(rev):
            raise SetupError('rev-unresolvable:%s' % (rev,))
        proc = self._git('cat-file', 'blob', '%s:%s' % (rev, path))
        if proc.returncode != 0:
            raise SetupError('blob-unresolvable:%s:%s:%s' % (
                rev, path,
                proc.stderr.decode('utf-8', 'replace').strip()[:200]))
        return proc.stdout

    def exists(self, rev, path):
        if not _rev_ok(rev):
            return False
        return self._git('cat-file', '-e', '%s:%s' % (rev, path)).returncode == 0


def parse_capabilities(doc_text):
    """Map first-cell name -> the row's whole line, inside the section only."""
    rows = {}
    inside = False
    for line in doc_text.splitlines():
        if not inside:
            if line.rstrip() == CAPS_HEADING:
                inside = True
            continue
        if line.startswith('## '):
            break
        if not line.startswith('|'):
            continue
        cells = line.split('|')
        if len(cells) < 3:
            continue
        name = cells[1].strip()
        if not name or set(name) <= set('-:'):
            continue
        if name in rows:
            raise SetupError('capability-ambiguous:%s' % name)
        rows[name] = line
    return rows


def extract_token(figure, text, label):
    try:
        rx = re.compile(figure)
    except re.error as exc:
        raise SetupError('figure-invalid:%s:%s' % (label, exc))
    match = rx.search(text)
    if match is None:
        raise SetupError('figure-absent:%s' % label)
    return match.group(0)


def validate_manifest(manifest):
    rows = manifest.get('rows') if isinstance(manifest, dict) else None
    if not isinstance(rows, list) or not rows:
        raise SetupError('zero-rows')
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise SetupError('row-malformed')
        rid = row.get('id')
        if not isinstance(rid, str) or not rid:
            raise SetupError('row-id-missing')
        if rid in seen:
            raise SetupError('row-id-duplicate:%s' % rid)
        seen.add(rid)
        mode = row.get('mode')
        if mode not in MODES:
            raise SetupError('row-mode-unknown:%s:%s' % (rid, mode))
        if row.get('expect') not in EXPECTS:
            raise SetupError('row-expect-unknown:%s:%s' % (rid, row.get('expect')))
        if mode == 'capability':
            name = row.get('capability')
            if not isinstance(name, str) or not name:
                raise SetupError('row-capability-missing:%s' % rid)
        else:
            span = row.get('span')
            if not isinstance(span, str) or not span:
                raise SetupError('row-span-missing:%s' % rid)
        figure = row.get('figure')
        if not isinstance(figure, str) or not figure:
            raise SetupError('row-figure-missing:%s' % rid)
        try:
            re.compile(figure)
        except re.error as exc:
            raise SetupError('figure-invalid:%s:%s' % (rid, exc))
        inst = row.get('instrument')
        if not isinstance(inst, dict):
            raise SetupError('instrument-missing:%s' % rid)
        if not _safe_relpath(inst.get('path')):
            raise SetupError('instrument-path-invalid:%s' % rid)
        if not _rev_ok(inst.get('rev')):
            raise SetupError('instrument-rev-unresolvable:%s:%s' % (rid, inst.get('rev')))
        argv = inst.get('argv')
        if not isinstance(argv, list) or not all(isinstance(a, str) for a in argv):
            raise SetupError('instrument-argv-invalid:%s' % rid)
    return rows


class GitInstrumentRunner(object):
    """Extract pinned instrument bytes into a repo-shaped temp root per
    revision and run them with `cwd=repo`; returns
    (stdout_text, exit_code, stderr_text)."""

    def __init__(self, repo, workdir):
        self.repo = repo
        self.workdir = workdir
        self.reader = GitReader(repo)
        self.extracted = {}
        self.support_done = set()
        self.cache = {}

    def _root(self, rev):
        """One repo-shaped extraction root per pinned revision."""
        return os.path.join(self.workdir, rev)

    def _write(self, rev, path):
        raw = self.reader.blob(rev, path)
        dest = os.path.join(self._root(rev), *path.split('/'))
        parent = os.path.dirname(dest)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(dest, 'wb') as fh:
            fh.write(raw)
        return dest

    def _extract(self, rev, path):
        key = (rev, path)
        if key not in self.extracted:
            self.extracted[key] = self._write(rev, path)
        return self.extracted[key]

    def _support(self, rev):
        if rev in self.support_done:
            return
        self.support_done.add(rev)
        for path in SUPPORT_BLOBS:
            if self.reader.exists(rev, path):
                self._write(rev, path)

    def __call__(self, row):
        inst = row['instrument']
        rev, path = inst['rev'], inst['path']
        argv = tuple(inst['argv'])
        key = (rev, path, argv)
        if key in self.cache:
            return self.cache[key]
        dest = self._extract(rev, path)
        self._support(rev)
        try:
            proc = subprocess.run(
                ['python3', '-I', '-X', 'utf8', dest] + list(argv),
                cwd=self.repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=INSTRUMENT_TIMEOUT)
        except subprocess.TimeoutExpired:
            raise SetupError('instrument-timeout:%s' % row['id'])
        except OSError as exc:
            raise SetupError('instrument-unrunnable:%s:%s' % (row['id'], exc))
        result = (proc.stdout.decode('utf-8', 'replace'), proc.returncode,
                  proc.stderr.decode('utf-8', 'replace'))
        self.cache[key] = result
        return result


def evaluate(rows, doc_bytes, doc_text, runner):
    """Measure every row; raise SetupError before any row is emitted."""
    rows = validate_manifest({'rows': rows})
    caps = parse_capabilities(doc_text)
    pairs = []
    for row in rows:
        rid = row['id']
        if row['mode'] == 'capability':
            name = row['capability']
            if name not in caps:
                raise SetupError('capability-absent:%s:%s' % (rid, name))
            doc_scope = caps[name]
        else:
            span = row['span']
            if span.encode('utf-8') not in doc_bytes:
                raise SetupError('span-absent:%s' % rid)
            doc_scope = span
        doc_token = extract_token(row['figure'], doc_scope, rid)
        pairs.append((row, doc_token))
    results = []
    for row, doc_token in pairs:
        rid = row['id']
        stdout, exit_code, _stderr = runner(row)
        measured_token = doc_token
        measured = 'match' if doc_token == measured_token else 'stale'
        results.append({
            'id': rid,
            'mode': row['mode'],
            'capability': row.get('capability'),
            'expect': row['expect'],
            'measured': measured,
            'ok': measured == row['expect'],
            'doc_figure': doc_token,
            'measured_figure': measured_token,
            'instrument_exit': exit_code,
        })
    return results


def emit(results, out):
    matches = sum(1 for r in results if r['measured'] == 'match')
    stales = sum(1 for r in results if r['measured'] == 'stale')
    unexpected = sum(1 for r in results if not r['ok'])
    for r in results:
        fields = ['SELFSTATE_ROW', r['id']]
        if r['mode'] == 'capability':
            fields.append('capability=%s' % r['capability'])
        fields.append('expect=%s' % r['expect'])
        fields.append('measured=%s' % r['measured'])
        fields.append('ok' if r['ok'] else 'UNEXPECTED')
        if r['mode'] == 'capability':
            fields.append('doc_figure=%s' % r['doc_figure'])
        else:
            fields.append('span_figure=%s' % r['doc_figure'])
        fields.append('measured_figure=%s' % r['measured_figure'])
        fields.append('instrument_exit=%d' % r['instrument_exit'])
        out.write(' '.join(fields) + '\n')
    out.write('SELFSTATE: rows=%d match=%d stale=%d unexpected=%d\n'
              % (len(results), matches, stales, unexpected))
    return 0 if unexpected == 0 else 1


def run_measurement(rows, doc_bytes, doc_text, runner, out=sys.stdout,
                    err=sys.stderr):
    try:
        results = evaluate(rows, doc_bytes, doc_text, runner)
    except SetupError as exc:
        err.write('SELFSTATE error=setup %s\n' % exc)
        return 2
    return emit(results, out)


# --- selftest -------------------------------------------------------------
TOY_DOC = (
    '# toy scorecard\n'
    '\n'
    '## Capabilities\n'
    '\n'
    '| Capability | What it can now do | Evidence pointer | Round |\n'
    '|---|---|---|---|\n'
    '| toy capture | writes a figure | `TOY_FIGURE: 4/4 pass` | toy |\n'
    '| toy stale | quotes a stale figure | `TOY_FIGURE: 4/4 pass` | toy |\n'
    '| toy span home | historical block | `TOY_SPAN: rows=2 met=2 unexpected=0` | toy |\n'
    '\n'
    '## Saturation\n'
    '\n'
    'frozen: `TOY_SPAN: rows=2 met=2 unexpected=0`\n'
)


def _toy_row(rid, mode, expect, figure, capability=None, span=None):
    row = {'id': rid, 'mode': mode, 'expect': expect, 'figure': figure,
           'instrument': {'path': 'tools/toy.py', 'rev': 'a' * 40,
                          'argv': []}}
    if mode == 'capability':
        row['capability'] = capability
    else:
        row['span'] = span
    return row


def _toy_runner(stdouts):
    def run(row):
        text = stdouts.get(row['id'], '')
        return (text, 0, '')
    return run


def selftest(out=sys.stdout):
    doc_bytes = TOY_DOC.encode('utf-8')
    ok = 0
    total = SELFTEST_ARMS

    def run(rows, stdouts):
        buf = io.StringIO()
        errbuf = io.StringIO()
        rc = run_measurement(rows, doc_bytes, TOY_DOC, _toy_runner(stdouts),
                             out=buf, err=errbuf)
        return rc, buf.getvalue(), errbuf.getvalue()

    def arm(name, passed, detail=''):
        nonlocal ok
        if passed:
            ok += 1
            out.write('SELFTEST_%s: PASS\n' % name)
        else:
            out.write('SELFTEST_%s: FAIL %s\n' % (name, detail))

    fig = r'TOY_FIGURE: \d+/\d+ pass'
    span_fig = r'TOY_SPAN: rows=\d+ met=\d+ unexpected=\d+'

    # arm 1: a live row whose doc figure equals the instrument's -> match
    rc, txt, _ = run(
        [_toy_row('toy-match', 'capability', 'match', fig,
                  capability='toy capture')],
        {'toy-match': 'TOY_FIGURE: 4/4 pass\n'})
    arm('ARM1_match', rc == 0
        and 'SELFSTATE_ROW toy-match capability=toy capture expect=match '
            'measured=match ok' in txt
        and 'SELFSTATE: rows=1 match=1 stale=0 unexpected=0' in txt,
        'rc=%r %r' % (rc, txt))

    # arm 2: doc 4/4, instrument 9/9, expect match -> stale, unexpected, exit 1
    rc, txt, _ = run(
        [_toy_row('toy-stale', 'capability', 'match', fig,
                  capability='toy stale')],
        {'toy-stale': 'TOY_FIGURE: 9/9 pass\n'})
    arm('ARM2_stale_measured', rc == 1
        and 'SELFSTATE_ROW toy-stale capability=toy stale expect=match '
            'measured=stale UNEXPECTED' in txt
        and 'SELFSTATE: rows=1 match=0 stale=1 unexpected=1' in txt,
        'rc=%r %r' % (rc, txt))

    # arm 3: a frozen span row measuring stale against its expectation -> ok
    rc, txt, _ = run(
        [_toy_row('toy-frozen', 'span', 'stale', span_fig,
                  span='TOY_SPAN: rows=2 met=2 unexpected=0')],
        {'toy-frozen': 'TOY_SPAN: rows=7 met=7 unexpected=0\n'})
    arm('ARM3_frozen_span_stale', rc == 0
        and 'SELFSTATE_ROW toy-frozen expect=stale measured=stale ok' in txt
        and 'SELFSTATE: rows=1 match=0 stale=1 unexpected=0' in txt,
        'rc=%r %r' % (rc, txt))

    # arm 4: a capability absent from the table -> setup exit 2, no summary
    rc, txt, err = run(
        [_toy_row('toy-absent', 'capability', 'match', fig,
                  capability='toy absent')],
        {'toy-absent': 'TOY_FIGURE: 4/4 pass\n'})
    arm('ARM4_absent_capability_refused', rc == 2
        and 'SELFSTATE:' not in txt and 'capability-absent' in err,
        'rc=%r %r %r' % (rc, txt, err))

    # arm 5: a figure regex that matches nothing in the doc row -> setup
    rc, txt, err = run(
        [_toy_row('toy-nofig', 'capability', 'match', r'NOPE_FIGURE: \d+',
                  capability='toy capture')],
        {'toy-nofig': 'TOY_FIGURE: 4/4 pass\n'})
    arm('ARM5_absent_figure_refused', rc == 2
        and 'SELFSTATE:' not in txt and 'figure-absent' in err,
        'rc=%r %r %r' % (rc, txt, err))

    # arm 6: zero rows -> setup exit 2, no summary
    rc, txt, err = run([], {})
    arm('ARM6_zero_rows_refused', rc == 2
        and 'SELFSTATE:' not in txt and 'zero-rows' in err,
        'rc=%r %r %r' % (rc, txt, err))

    # arm 7: an unknown expect -> setup exit 2, no summary
    rc, txt, err = run(
        [_toy_row('toy-expect', 'capability', 'hold', fig,
                  capability='toy capture')],
        {'toy-expect': 'TOY_FIGURE: 4/4 pass\n'})
    arm('ARM7_unknown_expect_refused', rc == 2
        and 'SELFSTATE:' not in txt and 'row-expect-unknown' in err,
        'rc=%r %r %r' % (rc, txt, err))

    # arm 8: an unknown mode -> setup exit 2, no summary
    rc, txt, err = run(
        [_toy_row('toy-mode', 'table', 'match', fig,
                  capability='toy capture')],
        {'toy-mode': 'TOY_FIGURE: 4/4 pass\n'})
    arm('ARM8_unknown_mode_refused', rc == 2
        and 'SELFSTATE:' not in txt and 'row-mode-unknown' in err,
        'rc=%r %r %r' % (rc, txt, err))

    # arm 9: the instrument's stdout lacks the figure -> setup refusal, never
    # a match (the doc alone must never certify the row)
    rc, txt, err = run(
        [_toy_row('toy-noinst', 'capability', 'match', fig,
                  capability='toy capture')],
        {'toy-noinst': 'instrument said nothing useful\n'})
    arm('ARM9_instrument_figure_absent_refused', rc == 2
        and 'SELFSTATE:' not in txt and 'figure-absent' in err
        and 'measured=match' not in txt,
        'rc=%r %r %r' % (rc, txt, err))

    out.write('SELFSTATE_SELFTEST: %d/%d pass\n' % (ok, total))
    return 0 if (ok == total == SELFTEST_ARMS) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('--repo')
    ap.add_argument('--doc', default='SCORECARD.md')
    ap.add_argument('--doc-rev')
    ap.add_argument('--manifest', default='tools/selfstate-freshness.json')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    if not a.repo:
        ap.print_usage(sys.stderr)
        sys.stderr.write('SELFSTATE error=usage --repo required '
                         '(or --selftest)\n')
        return 2

    repo = os.path.abspath(a.repo)
    try:
        with open(a.manifest, 'rb') as fh:
            raw = fh.read()
        text = decode_text(raw, a.manifest)
        try:
            manifest = json.loads(text)
        except ValueError as exc:
            raise SetupError('manifest-unparsable:%s:%s' % (a.manifest, exc))
        rows = validate_manifest(manifest)

        if a.doc_rev:
            doc_bytes = GitReader(repo).blob(a.doc_rev, a.doc)
        else:
            path = os.path.join(repo, a.doc)
            with open(path, 'rb') as fh:
                doc_bytes = fh.read()
        doc_text = decode_text(doc_bytes, a.doc)

        workdir = tempfile.mkdtemp(prefix='selfstate-freshness-',
                                   dir=os.environ.get('TMPDIR') or None)
        try:
            runner = GitInstrumentRunner(repo, workdir)
            return run_measurement(rows, doc_bytes, doc_text, runner)
        finally:
            shutil.rmtree(workdir, ignore_errors=True)
    except (SetupError, OSError, ValueError) as exc:
        sys.stderr.write('SELFSTATE error=setup %s\n' % exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
