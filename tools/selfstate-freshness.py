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

Selftest (`--selftest`): seventeen arms. Arms 1-10 are hermetic — a fixture
doc string and a canned instrument stdout per row; arms 11 and 13-17 drive
the real CLI as a subprocess against a real git fixture (arm 11: the
`--doc-rev` binding; arm 13: a `bash` row executed from extracted bytes through
the frozen tuple table, then a python-defaulted row on the same path/rev/argv
refused because the row cache is keyed by the interpreter; arm 14: the python
tuple's `-I` measured through an instrument that prints `sys.flags.isolated`,
the round-78 wave's `s3-python-isolation-dropped` survivor; arm 15: the BOM and
non-UTF-8 doc refusals, the round-79 `ss-bom-strip` survivor; arm 16: two rows
on one path/rev with different argv, the `ss-cache-key-drops-argv` survivor;
arm 17: the tuple's `-X utf8` measured through `sys.flags.utf8_mode`, the
`python-utf8-dropped` survivor). Arm 12 refuses an unknown interpreter. The rest, in order: match, stale measured, frozen-span stale,
absent capability refused, absent figure refused, zero rows refused, unknown
expect refused, unknown mode refused, an instrument whose stdout lacks the
figure refused (a setup refusal, never a match), and a figure regex matching
more than once refused. `SELFTEST_ARMS` and the arm calls are asserted equal by
the suite's own exit binding — the round-78 docstring had said "Nine arms"
against a suite of eleven; this list is the count's source of truth.

Usage:

  python3 -I -X utf8 tools/selfstate-freshness.py --selftest
  python3 -I -X utf8 tools/selfstate-freshness.py --repo . \\
      --manifest tools/selfstate-freshness.json --doc-rev 21ef81e9
"""

import argparse
import hashlib
import inspect
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SELFTEST_ARMS = 24
# R81-C3: the selftest's own assertion text is pinned. The round-80 battery's
# `ss-bom-only` mutant deleted arm15's non-UTF-8 conjuncts and survived 17/17:
# a weakened test text is invisible to the suite it weakens. The digest below
# covers this function's source (inspect.getsource), so any edit to an arm's
# assertion text fails an arm until the pin is recomputed deliberately. A
# two-edit mutant that also recomputes the constant is out of the declared
# single-edit class; the battery's control measures the pin's own do-nothing
# state.
SELFTEST_TEXT_SHA256 = ('891d3acc844977a1b7e7365a743f49ee7e585550522e42608eac8012514fafd3')
MODES = ('capability', 'span')
EXPECTS = ('match', 'stale')
# R83-C1: a row id is printed into a `SELFSTATE_ROW` line, so it is an output
# token, not free text; a newline in it forges a verdict line (the round-83
# control `c1-before-id-forge.txt` prints a green `SELFSTATE:` summary the
# measurement never produced). The alphabet is closed to what a line-safe
# identity needs.
ROW_ID_RE = re.compile(r'^[A-Za-z0-9._-]{1,64}$')
# R83-C1: a manifest path is a *tree entry*, and only its mode says whether the
# entry is a regular file; `cat-file blob` returns a symlink's target string
# without complaint (S291).
REGULAR_MODES = ('100644', '100755')
BOM = b'\xef\xbb\xbf'
CAPS_HEADING = '## Capabilities'
INSTRUMENT_TIMEOUT = 600
# Frozen runner tuple table (criterion 127: a widened runner needs its own
# before/after and a frozen tuple table). A row names its interpreter here; an
# unnamed interpreter is python (the round-75 default, unchanged). `bash` is
# the round-78 addition: the lane's mutation runner is a bash instrument and no
# live freshness row could exist for it (round-77 carry).
INTERPRETERS = {
    'python': ('python3', '-I', '-X', 'utf8'),
    'bash': ('bash',),
}
DEFAULT_INTERPRETER = 'python'
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
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=_fixture_env())
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

    def tree_mode(self, rev, path):
        """The mode of the tree entry `rev:path`, or None when it is absent.

        A symlink is a blob too: `cat-file blob` returns the link target's
        text and nothing in the read tells it apart from a regular file's
        bytes. The mode is where git states the difference (S291: the 9-bit
        permission field, with symlinks a distinct type), so a binding that
        reads "the object at this path" must read the mode as well."""
        if not _rev_ok(rev):
            return None
        proc = self._git('ls-tree', '-z', '--full-tree', rev, '--', path)
        if proc.returncode != 0:
            return None
        for record in proc.stdout.split(b'\x00'):
            if not record:
                continue
            meta, _, name = record.partition(b'\t')
            fields = meta.split()
            if len(fields) != 3:
                continue
            if name.decode('utf-8', 'surrogateescape') != path:
                continue
            return fields[0].decode('ascii', 'replace')
        return None


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
    matches = rx.findall(text)
    if not matches:
        raise SetupError('figure-absent:%s' % label)
    if len(matches) > 1:
        # a second match is a setup refusal: silently binding the first one is
        # the wrong-occurrence hazard (round-75 seat T75W1R2 §5c).
        raise SetupError('figure-not-unique:%s:%d' % (label, len(matches)))
    return matches[0]


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
        if not ROW_ID_RE.match(rid):
            # the repr keeps a newline escaped: the refusal itself must be one
            # line, or the refusal forges the same output line it refuses
            raise SetupError('row-id-alphabet:%r' % rid)
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
        interp = inst.get('interpreter', DEFAULT_INTERPRETER)
        if not isinstance(interp, str) or interp not in INTERPRETERS:
            raise SetupError('interpreter-unknown:%s:%s' % (rid, interp))
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
        interp = inst.get('interpreter', DEFAULT_INTERPRETER)
        key = (rev, path, argv, interp)
        if key in self.cache:
            return self.cache[key]
        dest = self._extract(rev, path)
        self._support(rev)
        try:
            prefix = INTERPRETERS[interp]
            proc = subprocess.run(
                list(prefix) + [dest] + list(argv),
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
        measured_token = extract_token(row['figure'], stdout, rid)
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


DOC_REV1 = (
    '# toy scorecard\n\n## Capabilities\n\n'
    '| Capability | What it can now do | Evidence pointer | Round |\n'
    '|---|---|---|---|\n'
    '| toy capture | writes a figure | `TOY_FIGURE: 4/4 pass` | toy |\n'
)
DOC_WT = DOC_REV1.replace('4/4', '9/9')

def _fixture_env():
    """Isolated environment for fixture git calls (round-79 sentinel): an
    inherited GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE would redirect `git init`
    before any post-init assertion could run."""
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               # R83-C1: a replacement ref substitutes the bytes every reader
               # sees, so an object-bound check that honours `git replace`
               # reads the substitute's identity, not the declared revision's
               # (round-82 repair 4, carried to this instrument).
               GIT_NO_REPLACE_OBJECTS='1')
    return env


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

    # arm 10: the figure regex matches TWICE in the located row -> setup
    # refusal (first-match-silently is the wrong-occurrence hazard)
    rc, txt, err = run(
        [_toy_row('toy-dup', 'capability', 'match', 'toy',
                  capability='toy capture')],
        {'toy-dup': 'toy\n'})
    arm('ARM10_figure_not_unique_refused', rc == 2
        and 'SELFSTATE:' not in txt and 'figure-not-unique' in err,
        'rc=%r %r %r' % (rc, txt, err))

    # arm 11: the CLI binds --doc-rev (round-76 carry: the --doc-rev-ignored
    # mutant survived the round-75 battery 10/10, T75W1M1 settlement errata).
    # The arm runs the real CLI as a subprocess against a two-state fixture
    # whose worktree doc disagrees with the committed rev: reading the rev
    # must measure match; a tool that ignores --doc-rev reads the worktree
    # doc and measures stale instead.
    fx = tempfile.mkdtemp(prefix="selfstate-arm11-",
                          dir=os.environ.get("TMPDIR") or None)
    try:
        def _git(*args):
            subprocess.run(["git", "-C", fx] + list(args), check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=_fixture_env())

        def _put(rel, text):
            path = os.path.join(fx, rel)
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(path, "w", newline="\n") as fh:
                fh.write(text)

        _put("SCORECARD.md", DOC_REV1)
        _put("tools/toy.py", "print('TOY_FIGURE: 4/4 pass')\n")
        mpath = os.path.join(fx, "manifest.json")
        with open(mpath, "w", newline="\n") as fh:
            json.dump({"schema": "tameshi-selfstate-freshness-v1",
                       "rows": [{"id": "toy-cli", "mode": "capability",
                                 "capability": "toy capture",
                                 "expect": "match", "figure": fig,
                                 "instrument": {"path": "tools/toy.py",
                                                "rev": None, "argv": []}}]},
                      fh)
        _git("init", "-q")
        _top = subprocess.run(["git", "-C", fx, "rev-parse",
                                "--show-toplevel"], check=True,
                               stdout=subprocess.PIPE,
                               env=_fixture_env()).stdout.decode().strip()
        if os.path.realpath(_top) != os.path.realpath(fx):
            raise SetupError("git-fixture-misroot:%s" % _top)
        _git("-c", "user.name=t", "-c", "user.email=t@t", "add",
             "SCORECARD.md", "tools/toy.py")
        _git("-c", "user.name=t", "-c", "user.email=t@t", "commit",
             "-qm", "rev1")
        rev1 = subprocess.run(["git", "-C", fx, "rev-parse", "HEAD"],
                              check=True,
                              stdout=subprocess.PIPE,
                              env=_fixture_env()).stdout.decode().strip()
        rows_manifest = json.load(open(mpath))
        rows_manifest["rows"][0]["instrument"]["rev"] = rev1
        with open(mpath, "w", newline="\n") as fh:
            json.dump(rows_manifest, fh)
        _put("SCORECARD.md", DOC_WT)
        proc = subprocess.run(
            [sys.executable, "-I", "-X", "utf8",
             os.path.abspath(__file__),
             "--repo", fx, "--doc-rev", rev1, "--manifest", mpath],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        out_text = proc.stdout.decode("utf-8", "replace")
        arm("ARM11_doc_rev_cli_binding",
            proc.returncode == 0
            and "SELFSTATE: rows=1 match=1 stale=0 unexpected=0" in out_text,
            "rc=%r tail=%r err=%r" % (
                proc.returncode, out_text[-160:],
                proc.stderr.decode("utf-8", "replace")[-160:]))
    finally:
        shutil.rmtree(fx, ignore_errors=True)

    # arm 12: an interpreter outside the frozen tuple table -> setup refusal
    row12 = _toy_row('toy-interp', 'capability', 'match', fig,
                     capability='toy capture')
    row12['instrument']['interpreter'] = 'zsh'
    rc, txt, err = run([row12], {'toy-interp': 'TOY_FIGURE: 4/4 pass\n'})
    arm('ARM12_unknown_interpreter_refused', rc == 2
        and 'SELFSTATE:' not in txt and 'interpreter-unknown:toy-interp:zsh' in err,
        'rc=%r %r %r' % (rc, txt, err))

    # arm 13: a `bash` row runs from extracted bytes through the tuple table.
    # The real CLI is a subprocess against a git fixture whose instrument is a
    # bash script: a runner that keeps the hardcoded `python3 -I` prefix cannot
    # execute it, and the row never measures match.
    fx2 = tempfile.mkdtemp(prefix="selfstate-arm13-",
                           dir=os.environ.get("TMPDIR") or None)
    try:
        def _git2(*args):
            subprocess.run(["git", "-C", fx2] + list(args), check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=_fixture_env())

        def _put2(rel, text):
            path = os.path.join(fx2, rel)
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(path, "w", newline="\n") as fh:
                fh.write(text)

        _put2("SCORECARD.md", DOC_REV1)
        _put2("tools/toy.sh", "#!/bin/bash\nprintf 'TOY_FIGURE: 4/4 pass\\n'\n")
        mpath2 = os.path.join(fx2, "manifest.json")
        with open(mpath2, "w", newline="\n") as fh:
            json.dump({"schema": "tameshi-selfstate-freshness-v1",
                       "rows": [{"id": "toy-bash", "mode": "capability",
                                 "capability": "toy capture",
                                 "expect": "match", "figure": fig,
                                 "instrument": {"path": "tools/toy.sh",
                                                "rev": None, "argv": [],
                                                "interpreter": "bash"}}]},
                      fh)
        _git2("init", "-q")
        _top = subprocess.run(["git", "-C", fx2, "rev-parse",
                                "--show-toplevel"], check=True,
                               stdout=subprocess.PIPE,
                               env=_fixture_env()).stdout.decode().strip()
        if os.path.realpath(_top) != os.path.realpath(fx2):
            raise SetupError("git-fixture-misroot:%s" % _top)
        _git2("-c", "user.name=t", "-c", "user.email=t@t", "add",
              "SCORECARD.md", "tools/toy.sh")
        _git2("-c", "user.name=t", "-c", "user.email=t@t", "commit",
              "-qm", "rev1")
        rev2 = subprocess.run(["git", "-C", fx2, "rev-parse", "HEAD"],
                              check=True,
                              stdout=subprocess.PIPE,
                              env=_fixture_env()).stdout.decode().strip()
        rows_manifest2 = json.load(open(mpath2))
        rows_manifest2["rows"][0]["instrument"]["rev"] = rev2
        with open(mpath2, "w", newline="\n") as fh:
            json.dump(rows_manifest2, fh)
        proc2 = subprocess.run(
            [sys.executable, "-I", "-X", "utf8",
             os.path.abspath(__file__),
             "--repo", fx2, "--doc-rev", rev2, "--manifest", mpath2],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        out_text2 = proc2.stdout.decode("utf-8", "replace")
        # second invocation, same fixture bytes: the row cache must be keyed by
        # the interpreter too. A python-defaulted row on the SAME path/rev/argv
        # must not be served the bash row's stdout; the run refuses
        # figure-absent before any match (round-78 reviewer R1 measured the
        # cache-key bypass on the declared design bytes).
        rows_manifest2["rows"].append({"id": "toy-python", "mode": "capability",
                                       "capability": "toy capture",
                                       "expect": "match", "figure": fig,
                                       "instrument": {"path": "tools/toy.sh",
                                                      "rev": rev2,
                                                      "argv": []}})
        with open(mpath2, "w", newline="\n") as fh:
            json.dump(rows_manifest2, fh)
        proc2b = subprocess.run(
            [sys.executable, "-I", "-X", "utf8",
             os.path.abspath(__file__),
             "--repo", fx2, "--doc-rev", rev2, "--manifest", mpath2],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        err2b = proc2b.stderr.decode("utf-8", "replace")
        arm("ARM13_bash_interpreter_row_and_cache",
            proc2.returncode == 0
            and "SELFSTATE: rows=1 match=1 stale=0 unexpected=0" in out_text2
            and proc2b.returncode == 2
            and "figure-absent:toy-python" in err2b
            and "measured=match" not in proc2b.stdout.decode("utf-8", "replace"),
            "rc=%r tail=%r err=%r | cache rc=%r err=%r" % (
                proc2.returncode, out_text2[-160:],
                proc2.stderr.decode("utf-8", "replace")[-160:],
                proc2b.returncode, err2b[-160:]))
    finally:
        shutil.rmtree(fx2, ignore_errors=True)

    # arm 14 (round 79): the python tuple's `-I` is load-bearing. The round-78
    # wave's `s3-python-isolation-dropped` mutant (a python tuple without `-I`)
    # survived 13/13 because no fixture distinguished isolated mode. The real
    # CLI runs an instrument whose printed figure depends on
    # `sys.flags.isolated`: under the frozen tuple it prints 1/1 (match); a
    # runner without `-I` prints 0/1 and the row measures stale, so the arm
    # fails. The python docs (S307) state `-I` "Run Python in isolated mode.
    # This also implies -E, -P and -s options."
    DOC_ISO = DOC_REV1.replace('TOY_FIGURE: 4/4 pass', 'TOY_ISO: 1/1 pass')
    fig_iso = r'TOY_ISO: \d+/\d+ pass'
    fx3 = tempfile.mkdtemp(prefix="selfstate-arm14-",
                           dir=os.environ.get("TMPDIR") or None)
    try:
        def _git3(*args):
            subprocess.run(["git", "-C", fx3] + list(args), check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=_fixture_env())

        def _put3(rel, text):
            path = os.path.join(fx3, rel)
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(path, "w", newline="\n") as fh:
                fh.write(text)

        _put3("SCORECARD.md", DOC_ISO)
        _put3("tools/toy_iso.py",
              "import sys\n"
              "print('TOY_ISO: 1/1 pass' if sys.flags.isolated"
              " else 'TOY_ISO: 0/1 pass')\n")
        mpath3 = os.path.join(fx3, "manifest.json")
        with open(mpath3, "w", newline="\n") as fh:
            json.dump({"schema": "tameshi-selfstate-freshness-v1",
                       "rows": [{"id": "toy-iso", "mode": "capability",
                                 "capability": "toy capture",
                                 "expect": "match", "figure": fig_iso,
                                 "instrument": {"path": "tools/toy_iso.py",
                                                "rev": None, "argv": []}}]},
                      fh)
        _git3("init", "-q")
        _top = subprocess.run(["git", "-C", fx3, "rev-parse",
                                "--show-toplevel"], check=True,
                               stdout=subprocess.PIPE,
                               env=_fixture_env()).stdout.decode().strip()
        if os.path.realpath(_top) != os.path.realpath(fx3):
            raise SetupError("git-fixture-misroot:%s" % _top)
        _git3("-c", "user.name=t", "-c", "user.email=t@t", "add",
              "SCORECARD.md", "tools/toy_iso.py")
        _git3("-c", "user.name=t", "-c", "user.email=t@t", "commit",
              "-qm", "rev1")
        rev3 = subprocess.run(["git", "-C", fx3, "rev-parse", "HEAD"],
                              check=True,
                              stdout=subprocess.PIPE,
                              env=_fixture_env()).stdout.decode().strip()
        rows_manifest3 = json.load(open(mpath3))
        rows_manifest3["rows"][0]["instrument"]["rev"] = rev3
        with open(mpath3, "w", newline="\n") as fh:
            json.dump(rows_manifest3, fh)
        proc3 = subprocess.run(
            [sys.executable, "-I", "-X", "utf8",
             os.path.abspath(__file__),
             "--repo", fx3, "--doc-rev", rev3, "--manifest", mpath3],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        out_text3 = proc3.stdout.decode("utf-8", "replace")
        arm("ARM14_python_isolation_tuple",
            proc3.returncode == 0
            and "SELFSTATE_ROW toy-iso capability=toy capture expect=match "
                "measured=match ok" in out_text3
            and "SELFSTATE: rows=1 match=1 stale=0 unexpected=0" in out_text3,
            "rc=%r tail=%r err=%r" % (
                proc3.returncode, out_text3[-200:],
                proc3.stderr.decode("utf-8", "replace")[-200:]))
    finally:
        shutil.rmtree(fx3, ignore_errors=True)

    # arm 15 (round 80): the decode refusals are measured end to end. The
    # round-79 scout's `ss-bom-strip` mutant (the BOM guard deleted) survived
    # 14/14 because no fixture fed the CLI a BOM or a non-UTF-8 doc. Both
    # paths are setup exits carrying their named diagnostic, never a match.
    fx4 = tempfile.mkdtemp(prefix="selfstate-arm15-",
                           dir=os.environ.get("TMPDIR") or None)
    try:
        def _git4(*args):
            subprocess.run(["git", "-C", fx4] + list(args), check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=_fixture_env())

        def _put4(rel, data):
            path = os.path.join(fx4, rel)
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            if isinstance(data, bytes):
                with open(path, "wb") as fh:
                    fh.write(data)
            else:
                with open(path, "w", newline="\n") as fh:
                    fh.write(data)

        _put4("SCORECARD.md", BOM + DOC_REV1.encode("utf-8"))
        _put4("tools/toy.py", "print('TOY_FIGURE: 4/4 pass')\n")
        mpath4 = os.path.join(fx4, "manifest.json")
        with open(mpath4, "w", newline="\n") as fh:
            json.dump({"schema": "tameshi-selfstate-freshness-v1",
                       "rows": [{"id": "toy-bom", "mode": "capability",
                                 "capability": "toy capture",
                                 "expect": "match", "figure": fig,
                                 "instrument": {"path": "tools/toy.py",
                                                "rev": None, "argv": []}}]},
                      fh)
        _git4("init", "-q")
        _top = subprocess.run(["git", "-C", fx4, "rev-parse",
                               "--show-toplevel"], check=True,
                              stdout=subprocess.PIPE,
                              env=_fixture_env()).stdout.decode().strip()
        if os.path.realpath(_top) != os.path.realpath(fx4):
            raise SetupError("git-fixture-misroot:%s" % _top)
        _git4("-c", "user.name=t", "-c", "user.email=t@t", "add",
              "SCORECARD.md", "tools/toy.py")
        _git4("-c", "user.name=t", "-c", "user.email=t@t", "commit",
              "-qm", "rev1")
        rev4 = subprocess.run(["git", "-C", fx4, "rev-parse", "HEAD"],
                              check=True, stdout=subprocess.PIPE,
                              env=_fixture_env()).stdout.decode().strip()
        rows4 = json.load(open(mpath4))
        rows4["rows"][0]["instrument"]["rev"] = rev4
        with open(mpath4, "w", newline="\n") as fh:
            json.dump(rows4, fh)

        def _cli4(doc_rev, env=None):
            proc = subprocess.run(
                [sys.executable, "-I", "-X", "utf8",
                 os.path.abspath(__file__), "--repo", fx4,
                 "--doc-rev", doc_rev, "--manifest", mpath4],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=120, env=env)
            return (proc.returncode,
                    proc.stdout.decode("utf-8", "replace"),
                    proc.stderr.decode("utf-8", "replace"))

        bom_rc, bom_txt, bom_err = _cli4(rev4)
        _put4("SCORECARD.md", b"\xff\xfe\x00 not utf-8\n")
        _git4("-c", "user.name=t", "-c", "user.email=t@t", "add",
              "SCORECARD.md")
        _git4("-c", "user.name=t", "-c", "user.email=t@t", "commit",
              "-qm", "rev2")
        rev4b = subprocess.run(["git", "-C", fx4, "rev-parse", "HEAD"],
                               check=True, stdout=subprocess.PIPE,
                               env=_fixture_env()).stdout.decode().strip()
        bad_rc, bad_txt, bad_err = _cli4(rev4b)
        arm('ARM15_decode_refusals',
            bom_rc == 2 and 'bom-present:SCORECARD.md' in bom_err
            and 'SELFSTATE:' not in bom_txt
            and bad_rc == 2 and 'not-utf8:SCORECARD.md' in bad_err
            and 'SELFSTATE:' not in bad_txt,
            'bom rc=%r err=%r | bad rc=%r err=%r'
            % (bom_rc, bom_err[-120:], bad_rc, bad_err[-120:]))
    finally:
        shutil.rmtree(fx4, ignore_errors=True)

    # arm 16 (round 80): the row cache is keyed by argv too. The round-79
    # scout's `ss-cache-key-drops-argv` mutant survived 14/14: no fixture ran
    # two rows on one path/rev with different argv. Both rows must measure
    # match; a cache that drops argv serves the first row's stdout to the
    # second and refuses figure-absent.
    DOC_ARGV = (
        '# toy scorecard\n\n'
        '## Capabilities\n\n'
        '| Capability | What it can now do | Evidence pointer | Round |\n'
        '|---|---|---|---|\n'
        '| toy argv a | writes a figure | `TOY_ARGV: A: 1/1 pass` | toy |\n'
        '| toy argv b | writes a figure | `TOY_ARGV: B: 1/1 pass` | toy |\n'
    )
    fig_argv = r'TOY_ARGV: [A-Z]: 1/1 pass'
    fx5 = tempfile.mkdtemp(prefix="selfstate-arm16-",
                           dir=os.environ.get("TMPDIR") or None)
    try:
        def _git5(*args):
            subprocess.run(["git", "-C", fx5] + list(args), check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=_fixture_env())

        def _put5(rel, text):
            path = os.path.join(fx5, rel)
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(path, "w", newline="\n") as fh:
                fh.write(text)

        _put5("SCORECARD.md", DOC_ARGV)
        _put5("tools/toy_argv.py",
              "import sys\n"
              "print('TOY_ARGV: %s: 1/1 pass'\n"
              "      % (sys.argv[1] if len(sys.argv) > 1 else 'none'))\n")
        mpath5 = os.path.join(fx5, "manifest.json")
        with open(mpath5, "w", newline="\n") as fh:
            json.dump({"schema": "tameshi-selfstate-freshness-v1",
                       "rows": [
                           {"id": "toy-argv-a", "mode": "capability",
                            "capability": "toy argv a", "expect": "match",
                            "figure": fig_argv,
                            "instrument": {"path": "tools/toy_argv.py",
                                           "rev": None, "argv": ["A"]}},
                           {"id": "toy-argv-b", "mode": "capability",
                            "capability": "toy argv b", "expect": "match",
                            "figure": fig_argv,
                            "instrument": {"path": "tools/toy_argv.py",
                                           "rev": None, "argv": ["B"]}}]},
                      fh)
        _git5("init", "-q")
        _top5 = subprocess.run(["git", "-C", fx5, "rev-parse",
                                "--show-toplevel"], check=True,
                               stdout=subprocess.PIPE,
                               env=_fixture_env()).stdout.decode().strip()
        if os.path.realpath(_top5) != os.path.realpath(fx5):
            raise SetupError("git-fixture-misroot:%s" % _top5)
        _git5("-c", "user.name=t", "-c", "user.email=t@t", "add",
              "SCORECARD.md", "tools/toy_argv.py")
        _git5("-c", "user.name=t", "-c", "user.email=t@t", "commit",
              "-qm", "rev1")
        rev5 = subprocess.run(["git", "-C", fx5, "rev-parse", "HEAD"],
                              check=True, stdout=subprocess.PIPE,
                              env=_fixture_env()).stdout.decode().strip()
        rows5 = json.load(open(mpath5))
        for row5 in rows5["rows"]:
            row5["instrument"]["rev"] = rev5
        with open(mpath5, "w", newline="\n") as fh:
            json.dump(rows5, fh)
        proc5 = subprocess.run(
            [sys.executable, "-I", "-X", "utf8", os.path.abspath(__file__),
             "--repo", fx5, "--doc-rev", rev5, "--manifest", mpath5],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        out_text5 = proc5.stdout.decode("utf-8", "replace")
        arm('ARM16_cache_key_keeps_argv',
            proc5.returncode == 0
            and 'SELFSTATE: rows=2 match=2 stale=0 unexpected=0' in out_text5,
            'rc=%r tail=%r err=%r' % (
                proc5.returncode, out_text5[-200:],
                proc5.stderr.decode("utf-8", "replace")[-200:]))
    finally:
        shutil.rmtree(fx5, ignore_errors=True)

    # arm 17 (round 80): the python tuple's `-X utf8` is load-bearing. The
    # round-79 mutation-tester's `python-utf8-dropped` mutant (the tuple loses
    # `-X utf8`) survived: no fixture distinguished UTF-8 mode. The instrument
    # prints `sys.flags.utf8_mode` and the CLI is spawned under an explicit
    # UTF-8 locale, so `-I` alone measures 0/1 and a dropped flag measures
    # stale (S308: "disabled by default and enabled by the POSIX locale").
    DOC_UTF8 = DOC_REV1.replace('TOY_FIGURE: 4/4 pass', 'TOY_UTF8: 1/1 pass')
    fig_utf8 = r'TOY_UTF8: \d+/\d+ pass'
    fx6 = tempfile.mkdtemp(prefix="selfstate-arm17-",
                           dir=os.environ.get("TMPDIR") or None)
    try:
        def _git6(*args):
            subprocess.run(["git", "-C", fx6] + list(args), check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=_fixture_env())

        def _put6(rel, text):
            path = os.path.join(fx6, rel)
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(path, "w", newline="\n") as fh:
                fh.write(text)

        _put6("SCORECARD.md", DOC_UTF8)
        _put6("tools/toy_utf8.py",
              "import sys\n"
              "print('TOY_UTF8: 1/1 pass' if sys.flags.utf8_mode"
              " else 'TOY_UTF8: 0/1 pass')\n")
        mpath6 = os.path.join(fx6, "manifest.json")
        with open(mpath6, "w", newline="\n") as fh:
            json.dump({"schema": "tameshi-selfstate-freshness-v1",
                       "rows": [{"id": "toy-utf8", "mode": "capability",
                                 "capability": "toy capture",
                                 "expect": "match", "figure": fig_utf8,
                                 "instrument": {"path": "tools/toy_utf8.py",
                                                "rev": None, "argv": []}}]},
                      fh)
        _git6("init", "-q")
        _top6 = subprocess.run(["git", "-C", fx6, "rev-parse",
                                "--show-toplevel"], check=True,
                               stdout=subprocess.PIPE,
                               env=_fixture_env()).stdout.decode().strip()
        if os.path.realpath(_top6) != os.path.realpath(fx6):
            raise SetupError("git-fixture-misroot:%s" % _top6)
        _git6("-c", "user.name=t", "-c", "user.email=t@t", "add",
              "SCORECARD.md", "tools/toy_utf8.py")
        _git6("-c", "user.name=t", "-c", "user.email=t@t", "commit",
              "-qm", "rev1")
        rev6 = subprocess.run(["git", "-C", fx6, "rev-parse", "HEAD"],
                              check=True, stdout=subprocess.PIPE,
                              env=_fixture_env()).stdout.decode().strip()
        rows6 = json.load(open(mpath6))
        rows6["rows"][0]["instrument"]["rev"] = rev6
        with open(mpath6, "w", newline="\n") as fh:
            json.dump(rows6, fh)
        env6 = {k: v for k, v in os.environ.items()
                if not k.startswith("PYTHON")}
        env6["LC_ALL"] = "en_US.UTF-8"
        env6["LANG"] = "en_US.UTF-8"
        proc6 = subprocess.run(
            [sys.executable, "-I", "-X", "utf8", os.path.abspath(__file__),
             "--repo", fx6, "--doc-rev", rev6, "--manifest", mpath6],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120,
            env=env6)
        out_text6 = proc6.stdout.decode("utf-8", "replace")
        arm('ARM17_python_utf8_mode_tuple',
            proc6.returncode == 0
            and 'SELFSTATE: rows=1 match=1 stale=0 unexpected=0' in out_text6,
            'rc=%r tail=%r err=%r' % (
                proc6.returncode, out_text6[-200:],
                proc6.stderr.decode("utf-8", "replace")[-200:]))
    finally:
        shutil.rmtree(fx6, ignore_errors=True)

    # arm 18 (round 81): the pin audit MEASURES a row pinned at pre-settlement
    # bytes. The round-80 closure defect D3: two rows pinned the declaration
    # commit while their instruments changed at the landing commit.
    fx7 = tempfile.mkdtemp(prefix='selfstate-arm18-',
                           dir=os.environ.get('TMPDIR') or None)
    try:
        def _git7(*args):
            subprocess.run(['git', '-C', fx7] + list(args), check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=_fixture_env())

        def _put7(rel, text):
            path = os.path.join(fx7, rel)
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(path, 'w', newline='\n') as fh:
                fh.write(text)

        _git7('init', '-q')
        _top7 = subprocess.run(['git', '-C', fx7, 'rev-parse',
                                '--show-toplevel'], check=True,
                               stdout=subprocess.PIPE,
                               env=_fixture_env()).stdout.decode().strip()
        if os.path.realpath(_top7) != os.path.realpath(fx7):
            raise SetupError('git-fixture-misroot:%s' % _top7)
        _put7('tools/toy.py', "print('rev1')\n")
        _git7('-c', 'user.name=t', '-c', 'user.email=t@t', 'add', '-A')
        _git7('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm',
              'rev1')
        pin1 = subprocess.run(['git', '-C', fx7, 'rev-parse', 'HEAD'],
                              check=True, stdout=subprocess.PIPE,
                              env=_fixture_env()).stdout.decode().strip()
        _put7('tools/toy.py', "print('rev2')\n")
        _git7('-c', 'user.name=t', '-c', 'user.email=t@t', 'add', '-A')
        _git7('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm',
              'rev2')
        pin2 = subprocess.run(['git', '-C', fx7, 'rev-parse', 'HEAD'],
                              check=True, stdout=subprocess.PIPE,
                              env=_fixture_env()).stdout.decode().strip()

        def _pin_row(rid, rev, path='tools/toy.py'):
            return {'id': rid, 'mode': 'capability', 'capability': 'toy',
                    'expect': 'match', 'figure': r'TOY: \d+/\d+',
                    'instrument': {'path': path, 'rev': rev, 'argv': []}}

        rows_stale = [_pin_row('stale-row', pin1), _pin_row('settled-row',
                                                            pin2)]
        buf = io.StringIO()
        rc_stale = pin_audit(fx7, rows_stale, pin2, out=buf)
        txt_stale = buf.getvalue()
        buf = io.StringIO()
        rc_settled = pin_audit(fx7, [_pin_row('a', pin2), _pin_row('b', pin2)],
                               pin2, out=buf)
        txt_settled = buf.getvalue()
        arm('ARM18_pin_audit_measures_stale',
            rc_stale == 1
            and 'SELFSTATE_PINS_ROW stale-row path=tools/toy.py' in txt_stale
            and 'state=stale' in txt_stale
            and 'state=settled' in txt_stale
            and 'SELFSTATE_PINS: rows=2 settled=1 stale=1' in txt_stale
            and rc_settled == 0
            and 'SELFSTATE_PINS: rows=2 settled=2 stale=0' in txt_settled,
            'rc=%r %r | rc2=%r %r' % (rc_stale, txt_stale[-160:], rc_settled,
                                      txt_settled[-120:]))

        # arm 19 (round 81): the audit's refusals are setup exit 2 before any
        # row effect — an unresolvable pin rev, a path absent at the pin, and
        # the manifest-level zero-row / unpinned-row refusals.
        def _refused(prefix, fn):
            try:
                fn()
            except SetupError as exc:
                return str(exc).startswith(prefix)
            return False

        arm('ARM19_pin_audit_refusals',
            _refused('pin-rev-unresolvable',
                     lambda: pin_audit(fx7, [_pin_row('x', pin2)], 'nope-rev',
                                       out=io.StringIO()))
            and _refused('pin-path-absent',
                         lambda: pin_audit(fx7, [_pin_row('x', pin2,
                                                          'tools/ghost.py')],
                                           pin2, out=io.StringIO()))
            and _refused('zero-rows',
                         lambda: validate_manifest({'rows': []}))
            and _refused('instrument-rev-unresolvable',
                         lambda: validate_manifest({'rows': [
                             _pin_row('x', None)]}))
            and _refused('instrument-path-invalid',
                         lambda: validate_manifest({'rows': [
                             _pin_row('x', pin2, '../escape')]})),
            '')

        # arm 20 (round 81): the pin audit's summary counts every validated
        # row and exits 0 only when the whole population is settled — an
        # audit over one row is not evidence for the manifest's others.
        buf = io.StringIO()
        rc_one = pin_audit(fx7, [_pin_row('only', pin1)], pin2, out=buf)
        buf_all = io.StringIO()
        pin_audit(fx7, rows_stale, pin2, out=buf_all)
        arm('ARM20_pin_audit_single_row_not_vacuous',
            rc_one == 1
            and 'SELFSTATE_PINS: rows=1 settled=0 stale=1' in buf.getvalue()
            and 'SELFSTATE_PINS: rows=2 settled=1 stale=1'
            in buf_all.getvalue(),
            'rc=%r' % rc_one)
    finally:
        shutil.rmtree(fx7, ignore_errors=True)

    # arm 21 (round 81): the selftest's own assertion text is pinned. The
    # round-80 battery's `ss-bom-only` mutant deleted arm15's non-UTF-8
    # conjuncts, kept the arm name and both fixture executions, and survived
    # 17/17: a weakened test text is invisible to the suite it weakens. The
    # digest covers this function's source (inspect.getsource), so any edit to
    # an arm's assertion text fails this arm until the constant is recomputed
    # deliberately (a second edit — outside the single-edit mutant class).
    try:
        self_text = inspect.getsource(selftest)
        measured_digest = hashlib.sha256(self_text.encode('utf-8')).hexdigest()
        arm('ARM21_selftest_text_pin', measured_digest == SELFTEST_TEXT_SHA256,
            'measured=%s pinned=%s' % (measured_digest[:12],
                                       SELFTEST_TEXT_SHA256[:12]))
    except OSError as exc:
        arm('ARM21_selftest_text_pin', False, 'source-unreadable:%s' % exc)

    # arm 22 (round 83): the manifest is bound to its declared revision. A
    # worktree manifest that differs from `REV:<manifest>` is refused before any
    # row effect; the same narrowed bytes still certify when the binding is not
    # asked for, which is what makes the binding the fix and not the narrowing.
    fx8 = tempfile.mkdtemp(prefix="selfstate-arm22-",
                           dir=os.environ.get("TMPDIR") or None)
    try:
        def _git8(*args):
            subprocess.run(["git", "-C", fx8] + list(args), check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=_fixture_env())

        def _put8(rel, text):
            path = os.path.join(fx8, rel)
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(path, "w", newline="\n") as fh:
                fh.write(text)

        def _rows8():
            return {"schema": "tameshi-selfstate-freshness-v1",
                    "rows": [
                        {"id": "toy-a", "mode": "capability",
                         "capability": "toy capture", "expect": "match",
                         "figure": fig,
                         "instrument": {"path": "tools/toy.py",
                                        "rev": None, "argv": []}},
                        {"id": "toy-b", "mode": "capability",
                         "capability": "toy capture", "expect": "match",
                         "figure": fig,
                         "instrument": {"path": "tools/toy.py",
                                        "rev": None, "argv": []}}]}

        def _commit8(message):
            _git8("-c", "user.name=t", "-c", "user.email=t@t", "add",
                  "SCORECARD.md", "tools/toy.py", "manifest.json")
            _git8("-c", "user.name=t", "-c", "user.email=t@t", "commit",
                  "-qm", message)
            return subprocess.run(["git", "-C", fx8, "rev-parse", "HEAD"],
                                  check=True, stdout=subprocess.PIPE,
                                  env=_fixture_env()).stdout.decode().strip()

        def _write_manifest8(rows):
            with open(os.path.join(fx8, "manifest.json"), "w",
                      newline="\n") as fh:
                json.dump({"schema": "tameshi-selfstate-freshness-v1",
                           "rows": rows}, fh)

        def _cli8(*extra):
            return subprocess.run(
                [sys.executable, "-I", "-X", "utf8",
                 os.path.abspath(__file__), "--repo", fx8,
                 "--manifest", "manifest.json"] + list(extra),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180,
                cwd=fx8)

        _put8("SCORECARD.md", DOC_REV1)
        _put8("tools/toy.py", "print('TOY_FIGURE: 4/4 pass')\n")
        _write_manifest8(_rows8()["rows"])
        _git8("init", "-q")
        _top8 = subprocess.run(["git", "-C", fx8, "rev-parse",
                                "--show-toplevel"], check=True,
                               stdout=subprocess.PIPE,
                               env=_fixture_env()).stdout.decode().strip()
        if os.path.realpath(_top8) != os.path.realpath(fx8):
            raise SetupError("git-fixture-misroot:%s" % _top8)
        rev8a = _commit8("rev1 (pins unset)")
        rows8 = _rows8()["rows"]
        for row in rows8:
            row["instrument"]["rev"] = rev8a
        _write_manifest8(rows8)
        rev8 = _commit8("rev2 (pins set)")

        bound = _cli8("--manifest-rev", rev8)
        bound_ok = (bound.returncode == 0
                    and b"SELFSTATE: rows=2 match=2 stale=0 unexpected=0"
                    in bound.stdout)
        narrowed = [dict(row) for row in rows8 if row["id"] != "toy-b"]
        _write_manifest8(narrowed)
        refused = _cli8("--manifest-rev", rev8)
        free = _cli8()
        refused_ok = (refused.returncode == 2
                      and b"manifest-rev-mismatch:" in refused.stderr
                      and b"SELFSTATE:" not in refused.stdout)
        free_ok = (free.returncode == 0
                   and b"SELFSTATE: rows=1 match=1 stale=0 unexpected=0"
                   in free.stdout)

        # a symlink manifest at the declared revision: the mode is the refusal
        os.remove(os.path.join(fx8, "manifest.json"))
        _put8("real.json", json.dumps({"schema": "x", "rows": rows8}))
        os.symlink("real.json", os.path.join(fx8, "manifest.json"))
        rev8link = _commit8("rev3 (manifest is a symlink)")
        link = _cli8("--manifest-rev", rev8link)
        link_ok = (link.returncode == 2
                   and b"manifest-rev-unreadable:mode:120000" in link.stderr
                   and b"SELFSTATE:" not in link.stdout)
        absent = _cli8("--manifest", "tools/ghost.json",
                       "--manifest-rev", rev8)
        absent_ok = (absent.returncode == 2
                     and b"manifest-rev-unreadable:absent" in absent.stderr
                     and b"SELFSTATE:" not in absent.stdout)
        arm('ARM22_manifest_rev_binding',
            bound_ok and refused_ok and free_ok,
            'bound=%r refused=%r free=%r' % (
                (bound.returncode, bound.stdout[-80:], bound.stderr[-80:]),
                (refused.returncode, refused.stdout[-80:],
                 refused.stderr[-80:]),
                (free.returncode, free.stdout[-80:], free.stderr[-80:])))
        arm('ARM23_manifest_rev_regular_file',
            link_ok and absent_ok,
            'link=%r absent=%r' % (
                (link.returncode, link.stderr[-90:]),
                (absent.returncode, absent.stderr[-90:])))
    finally:
        shutil.rmtree(fx8, ignore_errors=True)

    # arm 24 (round 83): a row id outside the line-safe alphabet is refused
    # before any instrument runs; the refusal itself is one line, so it cannot
    # forge the verdict line it refuses. The control (c1-before-id-forge.txt)
    # prints a green summary the measurement never produced.
    fx9 = tempfile.mkdtemp(prefix="selfstate-arm24-",
                           dir=os.environ.get("TMPDIR") or None)
    try:
        def _put9(rel, text):
            path = os.path.join(fx9, rel)
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(path, "w", newline="\n") as fh:
                fh.write(text)

        def _git9(*args):
            subprocess.run(["git", "-C", fx9] + list(args), check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=_fixture_env())

        _put9("SCORECARD.md", DOC_REV1)
        _put9("tools/toy.py", "print('TOY_FIGURE: 4/4 pass')\n")
        _git9("init", "-q")
        _git9("-c", "user.name=t", "-c", "user.email=t@t", "add",
              "SCORECARD.md", "tools/toy.py")
        _git9("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm",
              "rev1")
        rev9 = subprocess.run(["git", "-C", fx9, "rev-parse", "HEAD"],
                              check=True, stdout=subprocess.PIPE,
                              env=_fixture_env()).stdout.decode().strip()
        forged = ("forged\nSELFSTATE: rows=99 match=99 stale=0 "
                  "unexpected=0")
        _put9("manifest.json", json.dumps(
            {"schema": "tameshi-selfstate-freshness-v1", "rows": [
                {"id": forged, "mode": "capability",
                 "capability": "toy capture", "expect": "match",
                 "figure": fig,
                 "instrument": {"path": "tools/toy.py", "rev": rev9,
                                "argv": []}}]}))
        proc9 = subprocess.run(
            [sys.executable, "-I", "-X", "utf8", os.path.abspath(__file__),
             "--repo", fx9, "--manifest", "manifest.json"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180,
            cwd=fx9)
        arm('ARM24_row_id_alphabet',
            proc9.returncode == 2
            and b"row-id-alphabet:" in proc9.stderr
            and b"SELFSTATE:" not in proc9.stdout
            and proc9.stderr.count(b"\n") == 1,
            'rc=%r err=%r' % (proc9.returncode, proc9.stderr[-160:]))
    finally:
        shutil.rmtree(fx9, ignore_errors=True)

    out.write('SELFSTATE_SELFTEST: %d/%d pass\n' % (ok, total))
    return 0 if (ok == total == SELFTEST_ARMS) else 1


def _resolve_commit(repo, rev):
    proc = subprocess.run(['git', '-C', repo, 'rev-parse', '--verify',
                           '%s^{commit}' % rev],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=_fixture_env())
    if proc.returncode != 0:
        raise SetupError('pin-rev-unresolvable:%s' % rev)
    return proc.stdout.decode('ascii').strip()


def pin_audit(repo, rows, pin_rev, out=sys.stdout):
    """Measure whether every row's PINNED instrument bytes are the bytes the
    named tip carries. R81-C2: the round-80 closure defect D3 — two rows pinned
    the declaration commit while their instruments changed at the landing
    commit, so the standing sweep measured pre-settlement bytes (the figures
    happened to agree; the pin did not).

    State per row: `settled` when the instrument's blob at the row's pinned
    revision is byte-identical to its blob at `pin_rev`; `stale` otherwise.
    An unresolvable pin revision or a path absent at the pin is setup exit 2
    before any row effect; a zero-row manifest is refused by the same
    validate_manifest the sweep uses."""
    reader = GitReader(repo)
    tip = _resolve_commit(repo, pin_rev)
    counts = {'settled': 0, 'stale': 0}
    for row in rows:
        inst = row['instrument']
        path = inst['path']
        rev = inst['rev']
        if not reader.exists(tip, path):
            raise SetupError('pin-path-absent:%s:%s' % (tip, path))
        pinned = reader.blob(rev, path)
        settled = pinned == reader.blob(tip, path)
        state = 'settled' if settled else 'stale'
        counts[state] += 1
        out.write('SELFSTATE_PINS_ROW %s path=%s pin=%s tip=%s state=%s\n'
                  % (row['id'], path, rev[:12], tip[:12], state))
    out.write('SELFSTATE_PINS: rows=%d settled=%d stale=%d\n'
              % (len(rows), counts['settled'], counts['stale']))
    return 0 if counts['stale'] == 0 else 1


def _resolve_manifest_rev(repo, rev):
    """Resolve `--manifest-rev` with its own refusal token: a caller who asked
    for a manifest binding must not read a pin-audit refusal for it."""
    proc = subprocess.run(['git', '-C', repo, 'rev-parse', '--verify',
                           '%s^{commit}' % rev],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=_fixture_env())
    if proc.returncode != 0:
        raise SetupError('manifest-rev-unresolvable:%s' % rev)
    return proc.stdout.decode('ascii', 'replace').strip()


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('--repo')
    ap.add_argument('--doc', default='SCORECARD.md')
    ap.add_argument('--doc-rev')
    ap.add_argument('--manifest', default='tools/selfstate-freshness.json')
    ap.add_argument('--manifest-rev')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--pin-audit', action='store_true')
    ap.add_argument('--pin-rev', default='HEAD')
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
        if a.manifest_rev:
            # R83-C1: the manifest the sweep measures must be the object at the
            # declared revision. The object's checks run FIRST (mode, then
            # bytes), because the worktree copy is what may be lying: a
            # symlink is a blob too, and an absent worktree path must not mask
            # what the revision actually carries. Nothing is measured and no
            # instrument runs before the bytes agree.
            reader = GitReader(repo)
            rev = _resolve_manifest_rev(repo, a.manifest_rev)
            mode = reader.tree_mode(rev, a.manifest)
            if mode is None:
                raise SetupError('manifest-rev-unreadable:absent:%s'
                                 % a.manifest)
            if mode not in REGULAR_MODES:
                raise SetupError('manifest-rev-unreadable:mode:%s:%s'
                                 % (mode, a.manifest))
            bound = reader.blob(rev, a.manifest)
        try:
            with open(a.manifest, 'rb') as fh:
                raw = fh.read()
        except OSError as exc:
            raise SetupError('manifest-unreadable:%s:%s' % (a.manifest, exc))
        if a.manifest_rev:
            if raw != bound:
                raise SetupError('manifest-rev-mismatch:%s:%s'
                                 % (rev[:12], a.manifest))
            # one read serves both the binding and the parse: the bytes that
            # were compared are the bytes that are measured
            raw = bound
        text = decode_text(raw, a.manifest)
        try:
            manifest = json.loads(text)
        except ValueError as exc:
            raise SetupError('manifest-unparsable:%s:%s' % (a.manifest, exc))
        rows = validate_manifest(manifest)

        if a.pin_audit:
            return pin_audit(repo, rows, a.pin_rev)

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
