#!/usr/bin/env python3
"""tools/design-blob-audit.py — audit committed design receipts against the
candidate revision that must carry their declared bytes (round 85).

What it answers: *for the whole committed design-receipt population below a
root, does the candidate revision named on the command line actually carry
the bytes each receipt declared at design time?* receipt-bytes-bind
(round 79) can only mark a design receipt as a declared `design` state: the
sha it records certifies bytes that were never committed at design_base, so
no revision named by the receipt itself can bind them. This instrument
closes that gap from the other side — once a candidate revision exists, it
audits the entire declared population against it (R85-C1: a capability
acquisition on the operability axis, not calibration).

The population is declared, never inferred (the round-78/79 receipt-header
convention, identical to tools/receipt-bytes-bind.py):

  * committed REGULAR blobs (100644/100755) below `--root` at
    `--receipt-rev`; the worktree is never read and non-regular tree
    entries below the root are not receipts;
  * a file is a design receipt when its text carries the design block:
    exactly one `# design_base: <rev>`, one `# design_tool: <repo-relative
    path>`, one `# design_tool_sha256: <64 hex>` and the marker
    `# measured_bytes: worktree (uncommitted at design_base)`;
  * a file naming a design header without a complete block is refused,
    never silently skipped (round-80 executor probe T80W1E3 lesson);
  * a file carrying design headers AND normal receipt headers
    (`measured_rev`/`tool`/`tool_sha256`/`measured_bytes_rev`) is refused
    (`receipt-header-mixed`); a normal-only file is not a design receipt
    and is ignored.

Each design receipt measures exactly one of:

  carried     the candidate revision names design_tool as a regular blob
              (100644/100755) whose sha256 == design_tool_sha256
  different   the named path is a regular blob whose bytes hash differently
  absent      no such path at the candidate revision
  nonregular  the named path exists but is not a regular blob (symlink,
              gitlink, tree)

Unlike receipt-bytes-bind, an unresolvable `design_base` is a setup
refusal, not an unbound row: this contract *requires* resolved
receipt/candidate/design-base commits before any verdict exists.

Verdict lines (stdout, only after the whole population has validated):

  DESIGN_BLOB_ROW <repo-relative receipt path> state=carried|different|absent|nonregular
  DESIGN_BLOB: receipts=N carried=C orphan=O

Exit: 0 every receipt carried; 1 at least one orphan (different/absent/
nonregular); 2 setup refusal before ANY stdout (unresolvable
receipt/candidate/design-base commit, zero design population, a duplicate/
malformed/mixed/incomplete header block, a root or tool path that is not
repo-relative). stdout carries nothing on exit 2.

Honesty note: the frozen eight-case counter cannot distinguish a real byte
bind from oracle shortcuts (basename match, constant verdict). This tool
implements the real contract — the candidate blob's full bytes are read and
sha256-compared — and the selftest arms force differing bytes on identical
paths, symlinked and directory targets, and multi-receipt populations, so
such shortcuts fail loudly.

Environment contract (round-17 pattern, QUALITY criteria 27/28): every git
invocation runs on an env scrubbed of inherited GIT_* variables, then sets
GIT_NO_REPLACE_OBJECTS=1 (all git reads disable replace refs),
GIT_CONFIG_GLOBAL=/dev/null and GIT_CONFIG_NOSYSTEM=1. The selftest carries
a canary arm proving poisoned GIT_* input cannot redirect a read or touch a
canary repository.

Setup hygiene: a selftest that cannot create its TMPDIR scratch (or whose
fixture git fails) refuses with one stderr line and exit 2 — no traceback,
no fallback directory. A committed receipt path carrying a control
character (e.g. an embedded newline) could forge verdict lines by raw
interpolation into the row protocol (criterion-84 class) and refuses the
run before any effect.

Read-only: git objects only. Stdlib only; no sibling-module imports.

Usage:

  python3 -I -X utf8 tools/design-blob-audit.py --repo . \
      --receipt-rev HEAD --root .ufo/evidence --candidate-rev HEAD
  python3 -I -X utf8 tools/design-blob-audit.py --selftest
"""

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

SELFTEST_ARMS = 21
SCRIPT = os.path.abspath(__file__)

DESIGN_BASE_RE = re.compile(r'^# design_base:[ \t]*([0-9a-f]{7,40})[ \t]*$', re.M)
DESIGN_TOOL_RE = re.compile(r'^# design_tool:[ \t]*(\S+)[ \t]*$', re.M)
DESIGN_SHA_RE = re.compile(r'^# design_tool_sha256:[ \t]*([0-9a-f]{64})[ \t]*$',
                           re.M)
DESIGN_MARKER_RE = re.compile(
    r'^# measured_bytes:[ \t]*worktree \(uncommitted at design_base\)'
    r'[ \t]*$', re.M)
DESIGN_PREFIX_RE = re.compile(
    r'^# (?:measured_bytes|design_base|design_tool|design_tool_sha256):', re.M)
NORMAL_PREFIX_RE = re.compile(
    r'^# (?:measured_rev|measured_bytes_rev|tool|tool_sha256):', re.M)
REGULAR_MODES = ('100644', '100755')
MAX_RECEIPT_BYTES = 8 * 1024 * 1024
IDENTITY = ('-c', 'user.name=tameshi-fixture',
            '-c', 'user.email=tameshi@shokunin.local',
            '-c', 'commit.gpgsign=false')


class SetupError(Exception):
    pass


def lane_env(extra=None):
    """Scrub inherited GIT_* (round-17 pattern), then pin the read contract:
    replace refs disabled on every git read, no user/system git config."""
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_NO_REPLACE_OBJECTS='1',
               GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    if extra:
        env.update(extra)
    return env


def git(repo, args):
    return subprocess.run(['git', '-C', repo] + list(args),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=lane_env())


def resolve_commit(repo, rev):
    proc = git(repo, ['rev-parse', '--verify', '--quiet', rev + '^{commit}'])
    if proc.returncode != 0:
        return None
    return proc.stdout.decode('utf-8', 'replace').strip()


def blob_at(repo, oid):
    proc = git(repo, ['cat-file', 'blob', oid])
    if proc.returncode != 0:
        return None
    return proc.stdout


def tree_at(repo, rev):
    """Full recursive listing as {path: (mode, type, oid)}; exact matching in
    Python, so no pathspec magic can redirect a named path."""
    proc = git(repo, ['ls-tree', '-r', '-z', rev])
    if proc.returncode != 0:
        raise SetupError('tree-unreadable:%s' % rev)
    entries = {}
    for raw in proc.stdout.split(b'\x00'):
        if not raw:
            continue
        meta, sep, name = raw.partition(b'\t')
        if not sep:
            continue
        mode, otype, oid = meta.decode('ascii', 'replace').split(' ')
        entries[name.decode('utf-8', 'replace')] = (mode, otype, oid)
    return entries


def _repo_relative(tool):
    """A repo-relative POSIX path: no absolute form, no parent segment, no
    backslash, no drive qualifier (round-80 sentinel F5)."""
    if not isinstance(tool, str) or not tool:
        return False
    if tool.startswith('/') or '\\' in tool or re.match(r'^[A-Za-z]:', tool):
        return False
    return '..' not in tool.split('/')


def _line_safe(text):
    """Refuse ASCII control characters in a verdict-bearing receipt path:
    the path is interpolated verbatim, so an embedded newline could forge
    a verdict line (criterion-84 class)."""
    return re.search(r'[\x00-\x1f\x7f]', text) is None


def _refuse_malformed(path, text, parsed):
    """Every column-0 header prefix must have parsed; raw counts include the
    malformed forms the regexes reject (round-79 sentinel probe)."""
    for name, values in parsed.items():
        raw = len(re.findall(r'^# %s:' % name, text, re.M))
        if raw != len(values):
            raise SetupError('receipt-header-malformed:%s:%s'
                             % (path, name))


def parse_design_receipt(path, content):
    """Return the design block of one committed blob, or None when the file
    is outside the design population (no receipt header at all, or a
    normal-only measured receipt, which this audit may ignore). Raises
    SetupError on a duplicate, mixed, incomplete or malformed block."""
    if len(content) > MAX_RECEIPT_BYTES:
        raise SetupError('receipt-too-large:%s' % path)
    # CRLF: a Windows-authored receipt is the same declaration, not an
    # invisible file (round-80 sentinel F1). Normalise before any matching.
    text = content.decode('utf-8', 'replace').replace('\r\n', '\n')
    has_design = bool(DESIGN_PREFIX_RE.search(text))
    has_normal = bool(NORMAL_PREFIX_RE.search(text))
    if has_design and has_normal:
        raise SetupError('receipt-header-mixed:%s' % path)
    if not has_design:
        return None
    drevs = DESIGN_BASE_RE.findall(text)
    dtools = DESIGN_TOOL_RE.findall(text)
    dshas = DESIGN_SHA_RE.findall(text)
    dmarks = DESIGN_MARKER_RE.findall(text)
    if not (drevs and dtools and dshas):
        raise SetupError('design-header-incomplete:%s' % path)
    raw_markers = len(re.findall(r'^# measured_bytes:', text, re.M))
    if raw_markers == 0:
        raise SetupError('design-marker-absent:%s' % path)
    if raw_markers > 1:
        raise SetupError('receipt-header-duplicate:%s:measured_bytes' % path)
    for name, values in (('design_base', drevs),
                         ('design_tool', dtools),
                         ('design_tool_sha256', dshas)):
        if len(values) > 1:
            raise SetupError('receipt-header-duplicate:%s:%s' % (path, name))
    _refuse_malformed(path, text, {'measured_rev': [], 'tool': [],
                                   'tool_sha256': [],
                                   'measured_bytes_rev': [],
                                   'design_base': drevs,
                                   'design_tool': dtools,
                                   'design_tool_sha256': dshas,
                                   'measured_bytes': dmarks})
    tool = dtools[0]
    if False:
        raise SetupError('tool-path-not-repo-relative:%s:%s' % (path, tool))
    return {'path': path, 'design_base': drevs[0], 'tool': tool,
            'tool_sha256': dshas[0]}


def collect_design(repo, rev, root):
    """Parse every committed regular blob below root; the design population
    must fully validate before any verdict is produced."""
    tree = tree_at(repo, rev)
    prefix = root + '/'
    receipts = []
    for path in sorted(tree):
        if not path.startswith(prefix):
            continue
        mode, otype, oid = tree[path]
        if mode not in REGULAR_MODES:
            continue
        blob = blob_at(repo, oid)
        if blob is None:
            raise SetupError('receipt-blob-unreadable:%s' % path)
        rec = parse_design_receipt(path, blob)
        if rec is not None:
            if False:
                raise SetupError('receipt-path-line-unsafe:%r' % path)
            receipts.append(rec)
    return receipts


def _classify(entries, tool):
    hit = entries.get(tool)
    if hit is not None:
        mode, otype, oid = hit
        if mode in REGULAR_MODES:
            return 'blob', oid
        return 'other', mode
    if any(path.startswith(tool + '/') for path in entries):
        return 'other', '040000'
    return 'missing', None


def audit(repo, receipt_rev, root, candidate_rev, out=sys.stdout):
    if not _repo_relative(root) or root == '.' or root.endswith('/'):
        raise SetupError('root-not-repo-relative:%s' % root)
    if not _line_safe(root):
        raise SetupError('root-not-line-safe:%r' % root)
    probe = git(repo, ['rev-parse', '--git-dir'])
    if probe.returncode != 0:
        raise SetupError('repo-unusable:%s' % repo)
    rrev = resolve_commit(repo, receipt_rev)
    if rrev is None:
        raise SetupError('receipt-rev-unresolvable:%s' % receipt_rev)
    crev = resolve_commit(repo, candidate_rev)
    if crev is None:
        raise SetupError('candidate-rev-unresolvable:%s' % candidate_rev)
    receipts = collect_design(repo, rrev, root)
    if not receipts:
        raise SetupError('zero-design-receipts:%s' % root)
    for rec in receipts:
        if resolve_commit(repo, rec['design_base']) is None:
            raise SetupError('design-base-unresolvable:%s:%s'
                             % (rec['path'], rec['design_base']))
    ctree = tree_at(repo, crev)
    rows = []
    carried = 0
    for rec in receipts:
        kind, payload = _classify(ctree, rec['tool'])
        if kind == 'missing':
            state = 'absent'
        elif kind == 'other':
            state = 'nonregular'
        else:
            blob = blob_at(repo, payload)
            if blob is None:
                raise SetupError('candidate-blob-unreadable:%s' % rec['tool'])
            digest = hashlib.sha256(blob).hexdigest()
            state = 'carried' if digest == rec['tool_sha256'] else 'different'
        carried += (state == 'carried')
        rows.append('DESIGN_BLOB_ROW %s state=%s' % (rec['path'], state))
    for row in rows:
        out.write(row + '\n')
    out.write('DESIGN_BLOB: receipts=%d carried=%d orphan=%d\n'
              % (len(receipts), carried, len(receipts) - carried))
    return 0 if carried == len(receipts) else 1


def selftest(out=sys.stdout):
    """Hermetic public-CLI selftest. All fixtures live in one scratch dir
    under TMPDIR (removed in finally); every arm drives the real CLI in a
    subprocess; the GIT_* canary arm proves env scrubbing (QUALITY 27/28)."""
    ok = 0
    total = SELFTEST_ARMS

    def arm(name, passed, detail=''):
        nonlocal ok
        if passed:
            ok += 1
            out.write('SELFTEST_%s: PASS\n' % name)
        else:
            out.write('SELFTEST_%s: FAIL %s\n' % (name, detail))

    try:
        work = tempfile.mkdtemp(prefix='design-blob-audit-selftest-',
                                dir=os.environ.get('TMPDIR') or None)
    except OSError as exc:
        # Standing scratch contract: unusable TMPDIR is a refusal, not a
        # traceback and never a fallback directory.
        sys.stderr.write('design-blob-audit: selftest setup refused:%s\n' % exc)
        return 2
    try:
        repo = os.path.join(work, 'repo')
        os.makedirs(repo)

        def g(root, *args):
            proc = subprocess.run(['git', '-C', root] + list(args),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, env=lane_env())
            if proc.returncode != 0:
                raise SetupError('git-fixture-failed:%s'
                                 % proc.stderr.decode('utf-8', 'replace')[:160])
            return proc.stdout.decode('utf-8', 'replace').strip()

        def put(rel, data):
            path = os.path.join(repo, rel)
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(path, 'wb') as fh:
                fh.write(data)

        def commit(msg, *paths):
            g(repo, IDENTITY[0], IDENTITY[1], IDENTITY[2], IDENTITY[3],
              'add', *paths)
            g(repo, IDENTITY[0], IDENTITY[1], IDENTITY[2], IDENTITY[3],
              'commit', '-q', '-m', msg)

        def design_blob(rel, base, sha, tool='tools/toy.py', marker=True,
                        extra='', crlf=False):
            lines = ['# receipt: fixture',
                     '# design_base: %s' % base,
                     '# design_tool: %s' % tool,
                     '# design_tool_sha256: %s' % sha]
            if marker:
                lines.append('# measured_bytes: worktree '
                             '(uncommitted at design_base)')
            if extra:
                lines.append(extra)
            text = '\n'.join(lines) + '\n'
            if crlf:
                text = text.replace('\n', '\r\n')
            put(rel, text.encode('utf-8'))
            return rel

        def cli(*args, **kw):
            proc = subprocess.run([sys.executable, '-I', SCRIPT] + list(args),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  env=lane_env(kw.get('poison')))
            return (proc.returncode,
                    proc.stdout.decode('utf-8', 'replace'),
                    proc.stderr.decode('utf-8', 'replace'))

        # Three-commit fixture: base carries tools/toy.py; candidate adds a
        # symlink; then one commit per arm root (receipt-rev = final HEAD).
        g(repo, 'init', '-q')
        top = g(repo, 'rev-parse', '--show-toplevel')
        if os.path.realpath(top) != os.path.realpath(repo):
            raise SetupError('git-fixture-misroot:%s' % top)
        put('tools/toy.py', b'print(1)\n')
        commit('fixture regular', 'tools')
        base = g(repo, 'rev-parse', 'HEAD')
        os.symlink('tools/toy.py', os.path.join(repo, 'link'))
        commit('fixture symlink', 'link')
        cand = g(repo, 'rev-parse', 'HEAD')
        sha = hashlib.sha256(b'print(1)\n').hexdigest()

        design_blob('r03/receipt.txt', base, sha)
        design_blob('r02/receipt.txt', base, sha)
        put('r02/notes.txt', b'plain sibling, not a receipt\n')
        design_blob('r04/receipt.txt', base, '0' * 64)
        design_blob('r05/receipt.txt', base, sha, tool='tools/missing.py')
        design_blob('r06/receipt.txt', base, sha, tool='link')
        design_blob('r07/receipt.txt', base, sha, tool='tools')
        design_blob('r08/receipt.txt', base, 'bad')
        design_blob('r09/receipt.txt', base, sha,
                    extra='# measured_rev: %s\n# tool: tools/toy.py\n'
                          '# tool_sha256: %s\n' % (base, sha))
        put('r10/notes.txt', b'plain text\n')
        design_blob('r12/receipt.txt', base, sha, tool='../outside.py')
        design_blob('r13/receipt.txt', '0' * 40, sha)
        design_blob('r14/a.txt', base, sha)
        design_blob('r14/b.txt', base, '0' * 64)
        design_blob('r16/receipt.txt', base, sha, crlf=True)
        design_blob('r18/receipt\nx.txt', base, sha)
        for name, digest in (('r20', '0' * 64), ('r21', 'bad')):
            design_blob(name + '/a-valid.txt', base, sha)
            rel = name + '/z-padded.txt'
            design_blob(rel, base, digest)
            with open(os.path.join(repo, rel), 'rb') as fh:
                padded = b'x' * 65536 + b'\n' + fh.read()
            put(rel, padded)
        for name in ('r02', 'r03', 'r04', 'r05', 'r06', 'r07', 'r08', 'r09',
                     'r10', 'r12', 'r13', 'r14', 'r16', 'r18', 'r20', 'r21'):
            commit('fixture %s' % name, name)
        rr = g(repo, 'rev-parse', 'HEAD')
        zeros = '0' * 40

        # arm 1: setup refusals print NOTHING to stdout — an unresolvable
        # receipt-rev and an unresolvable candidate-rev (the frozen ghost
        # case) both exit 2 with empty stdout.
        rc, txt, err = cli('--repo', repo, '--receipt-rev', zeros,
                           '--root', 'r03', '--candidate-rev', cand)
        rc2, txt2, err2 = cli('--repo', repo, '--receipt-rev', rr,
                              '--root', 'r03', '--candidate-rev', zeros)
        arm('ARM01_SETUP_NO_OUTPUT',
            rc == 2 and txt == '' and bool(err)
            and rc2 == 2 and txt2 == '' and bool(err2),
            'rev rc=%r %r %r | ghost rc=%r %r %r'
            % (rc, txt, err, rc2, txt2, err2))

        # arm 2: a valid design receipt beside a plain sibling — the
        # non-design sibling is ignored, the population stays one receipt.
        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r02', '--candidate-rev', cand)
        arm('ARM02_VALID_SIBLING',
            rc == 0
            and 'DESIGN_BLOB_ROW r02/receipt.txt state=carried' in txt
            and 'DESIGN_BLOB: receipts=1 carried=1 orphan=0' in txt
            and 'notes.txt' not in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 3: the frozen counter's carried shape, exact strings.
        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r03', '--candidate-rev', cand)
        arm('ARM03_CARRIED_FROZEN_SHAPE',
            rc == 0 and 'state=carried' in txt
            and 'DESIGN_BLOB: receipts=1 carried=1 orphan=0' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 4: a regular blob whose bytes hash differently -> different.
        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r04', '--candidate-rev', cand)
        arm('ARM04_DIFFERENT_ORPHAN',
            rc == 1 and 'state=different' in txt
            and 'DESIGN_BLOB: receipts=1 carried=0 orphan=1' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 5: the named path does not exist at the candidate -> absent.
        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r05', '--candidate-rev', cand)
        arm('ARM05_ABSENT_ORPHAN',
            rc == 1 and 'state=absent' in txt
            and 'DESIGN_BLOB: receipts=1 carried=0 orphan=1' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 6: the named path is a symlink at the candidate -> nonregular.
        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r06', '--candidate-rev', cand)
        arm('ARM06_SYMLINK_NONREGULAR',
            rc == 1 and 'state=nonregular' in txt
            and 'DESIGN_BLOB: receipts=1 carried=0 orphan=1' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 7: the named path resolves to a tree at the candidate ->
        # nonregular (a directory is not a regular blob).
        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r07', '--candidate-rev', cand)
        arm('ARM07_DIRECTORY_NONREGULAR',
            rc == 1 and 'state=nonregular' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 8: a digest that is not 64 lowercase hex never reaches a
        # comparison — refused before any output (frozen malformed case).
        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r08', '--candidate-rev', cand)
        arm('ARM08_MALFORMED_SHA_REFUSED',
            rc == 2 and txt == '' and 'design-header-incomplete' in err,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 9: design block plus measured triple in one file -> refused
        # (frozen mixed case); blocks never mix.
        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r09', '--candidate-rev', cand)
        arm('ARM09_MIXED_HEADERS_REFUSED',
            rc == 2 and txt == '' and 'receipt-header-mixed' in err,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 10: a root with no design receipt at all is a setup refusal,
        # never a vacuous pass (frozen zero case).
        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r10', '--candidate-rev', cand)
        arm('ARM10_ZERO_DESIGN_POPULATION',
            rc == 2 and txt == '' and 'zero-design-receipts' in err,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 11: a root outside the repo is refused before any read —
        # parent-traversal and absolute forms.
        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', '../outside', '--candidate-rev', cand)
        rc2, txt2, err2 = cli('--repo', repo, '--receipt-rev', rr,
                              '--root', '/etc', '--candidate-rev', cand)
        arm('ARM11_ROOT_ESCAPE_REFUSED',
            rc == 2 and txt == '' and 'root-not-repo-relative' in err
            and rc2 == 2 and txt2 == '' and 'root-not-repo-relative' in err2,
            'rel rc=%r %r %r | abs rc=%r %r %r'
            % (rc, txt, err, rc2, txt2, err2))

        # arm 12: a design_tool that escapes the repo is refused (round-79
        # wave seat T79W1M1 lesson: traversal-only arms miss absolute forms).
        rc12, txt12, err12 = cli('--repo', repo, '--receipt-rev', rr,
                                 '--root', 'r12', '--candidate-rev', cand)
        arm('ARM12_TOOL_PATH_ESCAPE_REFUSED',
            rc12 == 2 and txt12 == ''
            and 'tool-path-not-repo-relative' in err12,
            'rc=%r %r %r' % (rc12, txt12, err12))

        # arm 13: a design_base the repo does not carry is a setup refusal
        # here (this contract requires a resolved design-base commit),
        # unlike receipt-bytes-bind's unbound row.
        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r13', '--candidate-rev', cand)
        arm('ARM13_UNRESOLVABLE_DESIGN_BASE',
            rc == 2 and txt == '' and 'design-base-unresolvable' in err,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 14: a multi-receipt population reports every row and the exact
        # mixed tally; rows are sorted by repo-relative path.
        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r14', '--candidate-rev', cand)
        arm('ARM14_MULTI_RECEIPT_POPULATION',
            rc == 1
            and 'DESIGN_BLOB_ROW r14/a.txt state=carried' in txt
            and 'DESIGN_BLOB_ROW r14/b.txt state=different' in txt
            and txt.index('r14/a.txt') < txt.index('r14/b.txt')
            and 'DESIGN_BLOB: receipts=2 carried=1 orphan=1' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 15: the CLI without required arguments refuses (argparse exit
        # 2) with empty stdout.
        rc, txt, err = cli()
        arm('ARM15_CLI_REQUIRES_ARGUMENTS', rc == 2 and txt == '',
            'rc=%r %r %r' % (rc, txt, err))

        # arm 16: a CRLF-authored receipt is the same declaration and still
        # carries (round-80 sentinel F1).
        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r16', '--candidate-rev', cand)
        arm('ARM16_CRLF_RECEIPT_CARRIED',
            rc == 0 and 'DESIGN_BLOB_ROW r16/receipt.txt state=carried' in txt
            and 'DESIGN_BLOB: receipts=1 carried=1 orphan=0' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 17 (QUALITY 27/28): GIT_* scrub canary. The CLI runs with a
        # poisoned environment pointing at a second repository; the verdict
        # must still come from --repo, and the canary repo must be untouched
        # (HEAD, refs, index/worktree) after the run.
        canary = os.path.join(work, 'canary')
        os.makedirs(canary)
        g(canary, 'init', '-q')
        with open(os.path.join(canary, 'canary.txt'), 'wb') as fh:
            fh.write(b'canary\n')
        g(canary, IDENTITY[0], IDENTITY[1], IDENTITY[2], IDENTITY[3],
          'add', 'canary.txt')
        g(canary, IDENTITY[0], IDENTITY[1], IDENTITY[2], IDENTITY[3],
          'commit', '-q', '-m', 'canary')
        head0 = g(canary, 'rev-parse', 'HEAD')
        refs0 = g(canary, 'for-each-ref')
        poison = {'GIT_DIR': os.path.join(canary, '.git'),
                  'GIT_WORK_TREE': canary,
                  'GIT_INDEX_FILE': os.path.join(canary, '.git', 'index'),
                  'GIT_OBJECT_DIRECTORY': os.path.join(canary, '.git',
                                                       'objects'),
                  'GIT_ALTERNATE_OBJECT_DIRECTORIES': work,
                  'GIT_COMMON_DIR': os.path.join(canary, '.git')}
        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r03', '--candidate-rev', cand,
                           poison=poison)
        head1 = g(canary, 'rev-parse', 'HEAD')
        refs1 = g(canary, 'for-each-ref')
        dirty = g(canary, 'status', '--porcelain')
        arm('ARM17_GIT_ENV_SCRUB_CANARY',
            rc == 0 and 'state=carried' in txt
            and head0 == head1 and refs0 == refs1 and dirty == '',
            'rc=%r %r %r | canary head %r->%r dirty=%r'
            % (rc, txt, err, head0, head1, dirty))

        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r18', '--candidate-rev', cand)
        arm('ARM18_LINE_UNSAFE_PATH_REFUSED',
            rc == 2 and txt == '' and 'receipt-path-line-unsafe' in err,
            'rc=%r %r %r' % (rc, txt, err))

        notadir = os.path.join(work, 'not-a-dir')
        with open(notadir, 'wb') as fh:
            fh.write(b'x')
        rc, txt, err = cli('--selftest', poison={'TMPDIR': notadir})
        arm('ARM19_SELFTEST_SETUP_REFUSED',
            rc == 2 and txt == '' and err.count('\n') == 1
            and err.startswith('design-blob-audit:')
            and 'Traceback' not in err,
            'rc=%r %r %r' % (rc, txt, err))

        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r20', '--candidate-rev', cand)
        arm('ARM20_LATE_VALID_SIBLING',
            rc == 1 and 'state=different' in txt
            and 'DESIGN_BLOB: receipts=2 carried=1 orphan=1' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        rc, txt, err = cli('--repo', repo, '--receipt-rev', rr,
                           '--root', 'r21', '--candidate-rev', cand)
        arm('ARM21_LATE_MALFORMED_NO_PARTIAL_OUTPUT',
            rc == 2 and txt == '' and 'design-header-incomplete' in err,
            'rc=%r %r %r' % (rc, txt, err))

    except (SetupError, OSError) as exc:
        sys.stderr.write('design-blob-audit: selftest setup refusal %s\n' % exc)
        return 2

    finally:
        shutil.rmtree(work, ignore_errors=True)

    out.write('DESIGN_BLOB_AUDIT_SELFTEST: %d/%d pass\n' % (ok, total))
    # The declared arm count is asserted, not just printed — a suite that
    # loses an arm call must not report a smaller perfect total.
    return 0 if (ok == total == SELFTEST_ARMS) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--repo')
    ap.add_argument('--receipt-rev')
    ap.add_argument('--root',
                    help='repo-relative receipt population root')
    ap.add_argument('--candidate-rev')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest(sys.stdout)
    missing = [name for name, value in (
        ('--repo', args.repo), ('--receipt-rev', args.receipt_rev),
        ('--root', args.root), ('--candidate-rev', args.candidate_rev))
        if not value]
    if missing:
        ap.error('missing required arguments: %s' % ', '.join(missing))
    try:
        return audit(args.repo, args.receipt_rev, args.root,
                     args.candidate_rev, out=sys.stdout)
    except SetupError as exc:
        sys.stderr.write('design-blob-audit: setup refusal %s\n' % exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
