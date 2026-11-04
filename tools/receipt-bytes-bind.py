#!/usr/bin/env python3
"""tools/receipt-bytes-bind.py — a receipt's recorded tool sha must exist in
the committed bytes of a revision the receipt names (round 79).

What it answers: *does the tool sha a receipt records actually live in the
committed bytes of the revision that receipt names?* The round-78 non-author
closure routed this class as a record defect: eight receipts under
`.ufo/evidence/round-78/` carry `# measured_rev: 6f532752…` while the
`# tool_sha256:` they record first exists at `091d50e4…` — the runs graded the
wave-close worktree and the bytes landed one commit later, so every receipt
named a revision that does not carry the bytes it certifies. Criterion 128
names the sibling class (a record naming a pre-settlement revision as the tip);
this instrument generalizes it to every receipt that records a measured tool.

The population is declared, never inferred:

  * a regular file under `--root` (default `.ufo/evidence`) — a symlink is
    not a receipt: it enters the population as a declared `unbound` row
    (`not-regular-file`) and its target's bytes are never read (round 83);
    whose text carries
    exactly one `# measured_rev: <rev>`, one `# tool: <repo-relative path>`
    and one `# tool_sha256: <64 hex>` header line — the lane's receipt-header
    convention, first used in round 78;
  * an optional append-only correction `# measured_bytes_rev: <rev>` names the
    commit whose bytes carry the recorded sha when the measured revision does
    not (the receipt was produced from a worktree whose bytes landed later).
  * a DESIGN receipt carries `# design_base: <rev>`, `# design_tool: <path>`,
    `# design_tool_sha256: <64 hex>` and the marker
    `# measured_bytes: worktree (uncommitted at design_base)` — one declared
    block, never mixed with the measured triple. Its sha certifies bytes that
    were never committed, so it is a measured `design` state: refusing the
    block blind would lose the declaration, and binding it to a blob would be
    false. A design block without the marker, or with an unresolvable
    `design_base`, is refused or unbound (round-79 closure defect 4).

A receipt measures one of:

  bound      sha256(`git cat-file blob <measured_rev>:<tool>`) == tool_sha256
  corrected  the measured-rev bytes differ, and exactly one
             `measured_bytes_rev` resolves and its bytes carry the sha
  design     a declared design-phase candidate; `design_base` resolves
  unbound    neither, with the reason in `detail` (tool-absent,
             rev-unresolvable, bytes-rev-absent, bytes-rev-unresolvable,
             bytes-rev-mismatch, design-base-unresolvable, not-regular-file)

A `measured_bytes_rev` that does not carry the recorded sha makes the receipt
unbound even when `measured_rev` happens to match: a false correction line is
never a pass. A file carrying both blocks is refused (`receipt-header-mixed`).

Verdict lines:

  RECEIPT_BIND_ROW <path> measured_rev=<r12> tool=<path> recorded=<sha12>
                   carrying=<rev12|-> state=bound|corrected|design|unbound
                   detail=<s>
  RECEIPT_BIND: receipts=N bound=B corrected=C design=D unbound=U

Exit: 0 every receipt bound or corrected; 1 at least one unbound; 2 setup
refusal before any row effect (zero population, a duplicate or malformed
header block, an unresolvable repo, a tool path that is not repo-relative, an
unreadable file). Read-only: git objects only. Stdlib only.

Usage:

  python3 -I -X utf8 tools/receipt-bytes-bind.py --repo . --root .ufo/evidence
  python3 -I -X utf8 tools/receipt-bytes-bind.py --selftest
"""

import argparse
import hashlib
import os
import re
import stat
import shutil
import subprocess
import sys
import tempfile

SELFTEST_ARMS = 14
REV_RE = re.compile(r'^# measured_rev:[ \t]*([0-9a-f]{7,40})[ \t]*$', re.M)
BYTES_REV_RE = re.compile(r'^# measured_bytes_rev:[ \t]*([0-9a-f]{7,40})[ \t]*$',
                          re.M)
TOOL_RE = re.compile(r'^# tool:[ \t]*(\S+)[ \t]*$', re.M)
SHA_RE = re.compile(r'^# tool_sha256:[ \t]*([0-9a-f]{64})[ \t]*$', re.M)
DESIGN_BASE_RE = re.compile(r'^# design_base:[ \t]*([0-9a-f]{7,40})[ \t]*$', re.M)
DESIGN_TOOL_RE = re.compile(r'^# design_tool:[ \t]*(\S+)[ \t]*$', re.M)
DESIGN_SHA_RE = re.compile(r'^# design_tool_sha256:[ \t]*([0-9a-f]{64})[ \t]*$',
                           re.M)
DESIGN_MARKER_RE = re.compile(
    r'^# measured_bytes:[ \t]*worktree \(uncommitted at design_base\)'
    r'[ \t]*$', re.M)
# Any column-0 header prefix, valid value or not: a file that names a receipt
# header but carries no complete block is refused, never silently skipped
# (round-80 executor probe T80W1E3: an all-malformed design block vanished).
PREFIX_RE = re.compile(
    r'^# (?:measured_rev|measured_bytes_rev|measured_bytes|tool|tool_sha256|'
    r'design_base|design_tool|design_tool_sha256):', re.M)
MAX_RECEIPT_BYTES = 8 * 1024 * 1024
HEAD_BYTES = 64 * 1024


class SetupError(Exception):
    pass


def lane_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
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


def blob_at(repo, rev, path):
    proc = git(repo, ['cat-file', 'blob', '%s:%s' % (rev, path)])
    if proc.returncode != 0:
        return None
    return proc.stdout


def _one(pattern, text):
    return pattern.findall(text)


def _repo_relative(tool):
    """A repo-relative POSIX path: no absolute form, no parent segment, no
    backslash, no drive qualifier (round-80 sentinel F5: Windows-style and
    drive-qualified design paths were accepted as design provenance)."""
    if not isinstance(tool, str) or not tool:
        return False
    if tool.startswith('/') or '\\' in tool or re.match(r'^[A-Za-z]:', tool):
        return False
    return '..' not in tool.split('/')


def _refuse_malformed(path, text, parsed):
    """Every column-0 header prefix must have parsed; `raw` counts include the
    malformed forms the regexes reject."""
    for name, values in parsed.items():
        raw = len(re.findall(r'^# %s:' % name, text, re.M))
        if raw != len(values):
            raise SetupError('receipt-header-malformed:%s:%s'
                             % (path, name))


def parse_receipt(path):
    """Return the receipt's header block, or None when the file is not a
    receipt (carries no complete header triple). Raises SetupError on a
    duplicate or mixed header: an ambiguous block cannot be measured.

    Two declared blocks exist. The measured block (`measured_rev` + `tool` +
    `tool_sha256`) names committed bytes. The design block (`design_base` +
    `design_tool` + `design_tool_sha256` + the `measured_bytes: worktree
    (uncommitted at design_base)` marker) names a design-phase candidate whose
    bytes were never committed; its sha cannot be bound to a blob and is
    therefore a declared `design` state, never a silent pass (round-79 closure
    defect 4: seven such receipts were outside the recognised population)."""
    try:
        with open(path, 'rb') as fh:
            head = fh.read(HEAD_BYTES)
            head_text = head.decode('utf-8', 'replace')
            if not PREFIX_RE.search(head_text):
                return None
            rest = fh.read(MAX_RECEIPT_BYTES + 1 - len(head))
    except OSError as exc:
        raise SetupError('receipt-unreadable:%s:%s' % (path, exc))
    if len(head) + len(rest) > MAX_RECEIPT_BYTES:
        raise SetupError('receipt-too-large:%s' % path)
    # CRLF: a Windows-authored receipt is the same declaration, not an
    # invisible file (round-80 sentinel F1: a CRLF file vanished from an
    # otherwise green population). Normalise before any matching.
    text = (head_text + rest.decode('utf-8', 'replace')).replace('\r\n', '\n')
    revs, tools, shas, brevs = (_one(REV_RE, text), _one(TOOL_RE, text),
                                _one(SHA_RE, text), _one(BYTES_REV_RE, text))
    drevs, dtools, dshas, dmarks = (_one(DESIGN_BASE_RE, text),
                                    _one(DESIGN_TOOL_RE, text),
                                    _one(DESIGN_SHA_RE, text),
                                    _one(DESIGN_MARKER_RE, text))
    normal = bool(revs or tools or shas or brevs)
    design = bool(drevs or dtools or dshas or dmarks)
    if not normal and not design:
        raise SetupError('receipt-header-incomplete:%s' % path)
    if normal and design:
        raise SetupError('receipt-header-mixed:%s' % path)
    if design:
        if not (drevs and dtools and dshas):
            raise SetupError('design-header-incomplete:%s' % path)
        raw_markers = len(re.findall(r'^# measured_bytes:', text, re.M))
        if raw_markers == 0:
            raise SetupError('design-marker-absent:%s' % path)
        if raw_markers > 1:
            raise SetupError('receipt-header-duplicate:%s:measured_bytes'
                             % path)
        for name, values in (('design_base', drevs),
                             ('design_tool', dtools),
                             ('design_tool_sha256', dshas)):
            if len(values) > 1:
                raise SetupError('receipt-header-duplicate:%s:%s'
                                 % (path, name))
        _refuse_malformed(path, text, {'measured_rev': [], 'tool': [],
                                       'tool_sha256': [],
                                       'measured_bytes_rev': [],
                                       'design_base': drevs,
                                       'design_tool': dtools,
                                       'design_tool_sha256': dshas,
                                       'measured_bytes': dmarks})
        tool = dtools[0]
        if not _repo_relative(tool):
            raise SetupError('tool-path-not-repo-relative:%s:%s'
                             % (path, tool))
        return {'path': path, 'kind': 'design',
                'measured_rev': drevs[0], 'tool': tool,
                'tool_sha256': dshas[0], 'design': True}
    if not (revs and tools and shas):
        raise SetupError('receipt-header-incomplete:%s' % path)
    for name, values in (('measured_rev', revs), ('tool', tools),
                         ('tool_sha256', shas), ('measured_bytes_rev', brevs)):
        if len(values) > 1:
            raise SetupError('receipt-header-duplicate:%s:%s' % (path, name))
    # A recognised header prefix whose value does not parse (a space in the
    # tool path, a short sha, a stray design line) must be refused, never
    # silently ignored: a receipt with one valid and one malformed `# tool:`
    # line would otherwise bind against the valid one while a reader sees two
    # declarations (round-79 sentinel probe; widened to every prefix round 80).
    _refuse_malformed(path, text, {'measured_rev': revs, 'tool': tools,
                                   'tool_sha256': shas,
                                   'measured_bytes_rev': brevs,
                                   'design_base': [], 'design_tool': [],
                                   'design_tool_sha256': [],
                                   'measured_bytes': []})
    tool = tools[0]
    if not _repo_relative(tool):
        raise SetupError('tool-path-not-repo-relative:%s:%s' % (path, tool))
    return {'path': path, 'kind': 'measured', 'measured_rev': revs[0],
            'tool': tool, 'tool_sha256': shas[0],
            'measured_bytes_rev': brevs[0] if brevs else None,
            'design': False}


def measure_receipt(repo, rec):
    """Return (state, carrying_rev, detail) for one parsed receipt."""
    if rec.get('kind') == 'non-regular':
        return 'unbound', None, 'not-regular-file'
    if rec.get('design'):
        if resolve_commit(repo, rec['measured_rev']) is None:
            return 'unbound', None, 'design-base-unresolvable'
        return 'design', None, 'uncommitted-design-candidate'
    measured = resolve_commit(repo, rec['measured_rev'])
    if measured is None:
        return 'unbound', None, 'rev-unresolvable'
    blob = blob_at(repo, measured, rec['tool'])
    if blob is None:
        if rec['measured_bytes_rev'] is None:
            return 'unbound', None, 'tool-absent'
    elif hashlib.sha256(blob).hexdigest() == rec['tool_sha256']:
        if rec['measured_bytes_rev'] is None:
            return 'bound', measured, 'measured-rev-carries'
        brevt = resolve_commit(repo, rec['measured_bytes_rev'])
        if brevt is None:
            return 'unbound', None, 'bytes-rev-unresolvable'
        bblob = blob_at(repo, brevt, rec['tool'])
        if bblob is None:
            return 'unbound', None, 'bytes-rev-tool-absent'
        if hashlib.sha256(bblob).hexdigest() != rec['tool_sha256']:
            return 'unbound', None, 'bytes-rev-mismatch'
        return 'bound', measured, 'measured-rev-carries'
    brevt = rec['measured_bytes_rev']
    if brevt is None:
        return 'unbound', None, 'bytes-rev-absent'
    brevt = resolve_commit(repo, brevt)
    if brevt is None:
        return 'unbound', None, 'bytes-rev-unresolvable'
    bblob = blob_at(repo, brevt, rec['tool'])
    if bblob is None:
        return 'unbound', None, 'bytes-rev-tool-absent'
    if hashlib.sha256(bblob).hexdigest() != rec['tool_sha256']:
        return 'unbound', None, 'bytes-rev-mismatch'
    return 'corrected', brevt, 'bytes-rev-carries'


def collect(root):
    if not os.path.isdir(root):
        raise SetupError('root-not-a-directory:%s' % root)
    receipts = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            # R83-C3: the population is the tree's REGULAR files. `isfile`
            # follows a symlink, so a link's target's bytes certified a
            # receipt that is not in the tree (the round-83 control
            # c3-before-symlink-bound.txt reads bound=2 over two entries, one
            # of them a link). lstat states the type; a non-regular entry is a
            # declared row that measures `unbound`, never a silent skip.
            try:
                mode = os.lstat(path).st_mode
            except OSError as exc:
                raise SetupError('receipt-unreadable:%s:%s' % (path, exc))
            if not stat.S_ISREG(mode):
                receipts.append({'path': path, 'kind': 'non-regular',
                                 'measured_rev': '', 'tool': '',
                                 'tool_sha256': '', 'design': False})
                continue
            rec = parse_receipt(path)
            if rec is not None:
                receipts.append(rec)
    return receipts


def sweep(repo, root, out=sys.stdout):
    probe = git(repo, ['rev-parse', '--git-dir'])
    if probe.returncode != 0:
        raise SetupError('repo-unusable:%s' % repo)
    receipts = collect(root)
    if not receipts:
        raise SetupError('zero-receipts:%s' % root)
    counts = {'bound': 0, 'corrected': 0, 'design': 0,
              'unbound': 0}
    for rec in receipts:
        state, carrying, detail = measure_receipt(repo, rec)
        counts[state] += 1
        out.write(
            'RECEIPT_BIND_ROW %s measured_rev=%s tool=%s recorded=%s '
            'carrying=%s state=%s detail=%s\n'
            % (rec['path'], (rec.get('measured_rev') or '-')[:12],
               rec.get('tool') or '-',
               (rec.get('tool_sha256') or '-')[:12],
               (carrying or '-')[:12], state, detail))
    out.write('RECEIPT_BIND: receipts=%d bound=%d corrected=%d design=%d '
              'unbound=%d\n'
              % (len(receipts), counts['bound'], counts['corrected'],
                 counts['design'], counts['unbound']))
    return 0 if counts['unbound'] == 0 else 1


def _fixture(root):
    """A two-commit git fixture: rev1 carries tool bytes A, rev2 bytes B."""
    def g(*args):
        proc = subprocess.run(['git', '-C', root] + list(args),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=lane_env())
        if proc.returncode != 0:
            raise SetupError('git-fixture-failed:%s'
                             % proc.stderr.decode('utf-8', 'replace')[:120])
        return proc.stdout.decode('utf-8', 'replace').strip()

    def put(rel, text):
        path = os.path.join(root, rel)
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, 'w', newline='\n') as fh:
            fh.write(text)

    g('init', '-q')
    top = g('rev-parse', '--show-toplevel')
    if os.path.realpath(top) != os.path.realpath(root):
        raise SetupError('git-fixture-misroot:%s' % top)
    put('tools/toy.py', "print('TOY: 1/1 pass')\n")
    g('-c', 'user.name=tameshi-fixture', '-c', 'user.email=tameshi@shokunin.local',
      '-c', 'commit.gpgsign=false', 'add', 'tools/toy.py')
    g('-c', 'user.name=tameshi-fixture', '-c', 'user.email=tameshi@shokunin.local',
      '-c', 'commit.gpgsign=false', 'commit', '-q', '-m', 'rev1')
    rev1 = g('rev-parse', 'HEAD')
    put('tools/toy.py', "print('TOY: 2/2 pass')\n")
    g('-c', 'user.name=tameshi-fixture', '-c', 'user.email=tameshi@shokunin.local',
      '-c', 'commit.gpgsign=false', 'add', 'tools/toy.py')
    g('-c', 'user.name=tameshi-fixture', '-c', 'user.email=tameshi@shokunin.local',
      '-c', 'commit.gpgsign=false', 'commit', '-q', '-m', 'rev2')
    rev2 = g('rev-parse', 'HEAD')
    sha1 = hashlib.sha256(blob_at(root, rev1, 'tools/toy.py')).hexdigest()
    sha2 = hashlib.sha256(blob_at(root, rev2, 'tools/toy.py')).hexdigest()
    return rev1, rev2, sha1, sha2


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

    work = tempfile.mkdtemp(prefix='receipt-bytes-bind-',
                            dir=os.environ.get('TMPDIR') or None)
    try:
        repo = os.path.join(work, 'repo')
        os.makedirs(repo)
        rev1, rev2, sha1, sha2 = _fixture(repo)

        def receipt(name, rev, sha, bytes_rev=None, tool='tools/toy.py',
                    extra=''):
            path = os.path.join(work, name)
            lines = ['# receipt: %s' % name,
                     '# measured_rev: %s' % rev,
                     '# tool: %s' % tool,
                     '# tool_sha256: %s' % sha]
            if bytes_rev is not None:
                lines.append('# measured_bytes_rev: %s' % bytes_rev)
            with open(path, 'w', newline='\n') as fh:
                fh.write('\n'.join(lines) + '\n' + extra)
            return path

        def design_receipt(name, base, sha, tool='tools/toy.py',
                           marker=True):
            path = os.path.join(work, name)
            lines = ['# receipt: %s' % name,
                     '# design_base: %s' % base,
                     '# design_tool: %s' % tool,
                     '# design_tool_sha256: %s' % sha]
            if marker:
                lines.append('# measured_bytes: worktree '
                             '(uncommitted at design_base)')
            with open(path, 'w', newline='\n') as fh:
                fh.write('\n'.join(lines) + '\n')
            return path

        def run(root):
            import io
            buf = io.StringIO()
            try:
                rc = sweep(repo, root, out=buf)
                err = ''
            except SetupError as exc:
                return 2, buf.getvalue(), str(exc)
            return rc, buf.getvalue(), err

        # arm 1: a receipt naming the revision that carries its sha -> bound.
        # Round 80 folds in the CRLF form (sentinel F1: a CRLF receipt was
        # invisible, so a newline conversion could hide an unbound one).
        root = os.path.join(work, 'pop1')
        os.makedirs(root)
        receipt(os.path.join(root, 'bound.txt'), rev1, sha1)
        rc, txt, err = run(root)
        root1b = os.path.join(work, 'pop1b')
        os.makedirs(root1b)
        crlf = os.path.join(root1b, 'crlf.txt')
        with open(crlf, 'w', newline='') as fh:
            fh.write('# receipt: crlf\r\n'
                     '# measured_rev: %s\r\n'
                     '# tool: tools/toy.py\r\n'
                     '# tool_sha256: %s\r\n' % (rev1, sha1))
        rc1b, txt1b, err1b = run(root1b)
        arm('ARM1_bound', rc == 0 and 'state=bound' in txt
            and 'RECEIPT_BIND: receipts=1 bound=1 corrected=0 design=0 '
                'unbound=0' in txt
            and rc1b == 0 and 'state=bound' in txt1b
            and 'receipts=1 bound=1' in txt1b,
            'rc=%r %r %r | crlf rc=%r %r %r'
            % (rc, txt, err, rc1b, txt1b, err1b))

        # arm 2: the measured rev's bytes differ, no correction -> unbound
        root = os.path.join(work, 'pop2')
        os.makedirs(root)
        receipt(os.path.join(root, 'drift.txt'), rev2, sha1)
        rc, txt, err = run(root)
        arm('ARM2_unbound_named', rc == 1 and 'state=unbound' in txt
            and 'detail=bytes-rev-absent' in txt
            and 'unbound=1' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 3: the same receipt plus the append-only correction -> corrected
        root = os.path.join(work, 'pop3')
        os.makedirs(root)
        receipt(os.path.join(root, 'drift.txt'), rev2, sha1, bytes_rev=rev1)
        rc, txt, err = run(root)
        arm('ARM3_corrected', rc == 0 and 'state=corrected' in txt
            and 'detail=bytes-rev-carries' in txt
            and 'corrected=1 design=0 unbound=0' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 4: a correction that names the wrong revision -> unbound
        root = os.path.join(work, 'pop4')
        os.makedirs(root)
        receipt(os.path.join(root, 'drift.txt'), rev2, sha1, bytes_rev=rev2)
        rc, txt, err = run(root)
        arm('ARM4_false_correction_refused', rc == 1
            and 'detail=bytes-rev-mismatch' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 5: a correction naming a revision the repo does not have
        root = os.path.join(work, 'pop5')
        os.makedirs(root)
        receipt(os.path.join(root, 'drift.txt'), rev2, sha1,
                bytes_rev='0' * 40)
        rc, txt, err = run(root)
        arm('ARM5_unresolvable_correction_refused', rc == 1
            and 'detail=bytes-rev-unresolvable' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 6: a duplicate header block, and a recognised prefix whose value
        # does not parse (a space in the tool path), are both refused before
        # any row effect — one valid plus one malformed `# tool:` line must
        # never bind against the valid one.
        root = os.path.join(work, 'pop6')
        os.makedirs(root)
        receipt(os.path.join(root, 'dup.txt'), rev1, sha1,
                extra='# measured_rev: %s\n' % rev2)
        rc, txt, err = run(root)
        root6b = os.path.join(work, 'pop6b')
        os.makedirs(root6b)
        receipt(os.path.join(root6b, 'malformed.txt'), rev1, sha1,
                extra='# tool: tools/path with spaces.py\n')
        rc6b, txt6b, err6b = run(root6b)
        # round 80 (executor probe T80W1E3): a file naming a design header
        # that does not parse carries no complete block and used to be skipped
        # silently; a raw prefix now makes it an incomplete receipt.
        root6c = os.path.join(work, 'pop6c')
        os.makedirs(root6c)
        with open(os.path.join(root6c, 'broken.txt'), 'w', newline='\n') as fh:
            fh.write('# receipt: broken\n# design_base: NOT-A-REV\n')
        rc6c, txt6c, err6c = run(root6c)
        arm('ARM6_duplicate_header_refused', rc == 2
            and 'RECEIPT_BIND:' not in txt
            and 'receipt-header-duplicate' in err
            and rc6b == 2
            and 'RECEIPT_BIND:' not in txt6b
            and 'receipt-header-malformed' in err6b
            and rc6c == 2
            and 'RECEIPT_BIND:' not in txt6c
            and 'receipt-header-incomplete' in err6c,
            'rc=%r %r %r | malformed rc=%r %r %r | incomplete rc=%r %r %r'
            % (rc, txt, err, rc6b, txt6b, err6b, rc6c, txt6c, err6c))

        # arm 7: an empty population is a setup refusal, never a vacuous pass
        root = os.path.join(work, 'pop7')
        os.makedirs(root)
        rc, txt, err = run(root)
        arm('ARM7_zero_population_refused', rc == 2
            and 'RECEIPT_BIND:' not in txt and 'zero-receipts' in err,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 8: the named tool does not exist at the measured rev
        root = os.path.join(work, 'pop8')
        os.makedirs(root)
        receipt(os.path.join(root, 'absent.txt'), rev1, sha1,
                tool='tools/missing.py')
        rc, txt, err = run(root)
        arm('ARM8_tool_absent_unbound', rc == 1
            and 'detail=tool-absent' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 9: a root that is not a git repository is a setup refusal
        import io
        buf = io.StringIO()
        plain = os.path.join(work, 'plain')
        os.makedirs(plain)
        try:
            sweep(plain, os.path.join(work, 'pop1'), out=buf)
            rc9, err9 = 0, ''
        except SetupError as exc:
            rc9, err9 = 2, str(exc)
        arm('ARM9_non_repo_refused', rc9 == 2 and 'repo-unusable' in err9,
            'rc=%r err=%r' % (rc9, err9))

        # arm 10: a tool path outside the repo is a setup refusal — both the
        # parent-traversal and the absolute-path forms (round-79 wave seat
        # T79W1M1 measured `absolute-tool-path-accepted` surviving a
        # traversal-only arm).
        root = os.path.join(work, 'pop10')
        os.makedirs(root)
        receipt(os.path.join(root, 'escape.txt'), rev1, sha1,
                tool='../outside.py')
        rc, txt, err = run(root)
        root10b = os.path.join(work, 'pop10b')
        os.makedirs(root10b)
        receipt(os.path.join(root10b, 'absolute.txt'), rev1, sha1,
                tool='/etc/passwd')
        rc10b, txt10b, err10b = run(root10b)
        root10c = os.path.join(work, 'pop10c')
        os.makedirs(root10c)
        design_receipt(os.path.join(root10c, 'win.txt'), rev1, sha1,
                       tool='..\\outside.py')
        rc10c, txt10c, err10c = run(root10c)
        root10d = os.path.join(work, 'pop10d')
        os.makedirs(root10d)
        design_receipt(os.path.join(root10d, 'drive.txt'), rev1, sha1,
                       tool='C:\\outside.py')
        rc10d, txt10d, err10d = run(root10d)
        arm('ARM10_tool_path_escape_refused', rc == 2
            and 'RECEIPT_BIND:' not in txt
            and 'tool-path-not-repo-relative' in err
            and rc10b == 2
            and 'RECEIPT_BIND:' not in txt10b
            and 'tool-path-not-repo-relative' in err10b
            and rc10c == 2
            and 'tool-path-not-repo-relative' in err10c
            and rc10d == 2
            and 'tool-path-not-repo-relative' in err10d,
            'rc=%r %r %r | abs rc=%r | win rc=%r | drive rc=%r'
            % (rc, txt, err, rc10b, rc10c, rc10d))

        # arm 11 (round 80): a declared design receipt is MEASURED as
        # `design`, not invisible. Round-79's control receipts carried the
        # design block while the instrument recognised only the measured one,
        # so the class it targets (a sha that exists in no blob) swept clean
        # by being outside the population (closure defect 4).
        root = os.path.join(work, 'pop11')
        os.makedirs(root)
        design_receipt(os.path.join(root, 'design.txt'), rev1, sha1)
        rc, txt, err = run(root)
        arm('ARM11_design_receipt_measured', rc == 0
            and 'state=design' in txt
            and 'detail=uncommitted-design-candidate' in txt
            and 'RECEIPT_BIND: receipts=1 bound=0 corrected=0 design=1 '
                'unbound=0' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 12 (round 80): a design block without the uncommitted marker is
        # an unbound declaration, never a design pass; a valid marker plus a
        # second, bogus `# measured_bytes:` line is ambiguous (executor probe
        # T80W1E3 measured both forms accepted before the fold).
        root = os.path.join(work, 'pop12')
        os.makedirs(root)
        design_receipt(os.path.join(root, 'naked.txt'), rev1, sha1,
                       marker=False)
        rc, txt, err = run(root)
        root12b = os.path.join(work, 'pop12b')
        os.makedirs(root12b)
        with open(os.path.join(root12b, 'twomarkers.txt'), 'w',
                  newline='\n') as fh:
            fh.write('# receipt: twomarkers\n'
                     '# design_base: %s\n'
                     '# design_tool: tools/toy.py\n'
                     '# design_tool_sha256: %s\n'
                     '# measured_bytes: worktree (uncommitted at design_base)\n'
                     '# measured_bytes: bogus\n' % (rev1, sha1))
        rc12b, txt12b, err12b = run(root12b)
        arm('ARM12_design_marker_absent_refused', rc == 2
            and 'RECEIPT_BIND:' not in txt
            and 'design-marker-absent' in err
            and rc12b == 2
            and 'RECEIPT_BIND:' not in txt12b
            and 'receipt-header-duplicate' in err12b
            and 'measured_bytes' in err12b,
            'rc=%r %r %r | duplicate rc=%r %r %r'
            % (rc, txt, err, rc12b, txt12b, err12b))

        # arm 13 (round 80): a design base the repo does not carry is unbound
        # by name, never design
        root = os.path.join(work, 'pop13')
        os.makedirs(root)
        design_receipt(os.path.join(root, 'ghostbase.txt'), '0' * 40, sha1)
        rc, txt, err = run(root)
        arm('ARM13_design_base_unresolvable', rc == 1
            and 'state=unbound' in txt
            and 'detail=design-base-unresolvable' in txt,
            'rc=%r %r %r' % (rc, txt, err))

        # arm 14 (round 83): a symlink is not a receipt. The link's target
        # carries a valid header and binds, which is exactly the cheat: the
        # base instrument read through the link and certified bytes that are
        # not in the tree. The regular sibling in the same population must
        # still bind (no over-kill).
        root = os.path.join(work, 'pop14')
        os.makedirs(root)
        target = receipt(os.path.join(work, 'pop14-target.txt'), rev1, sha1)
        os.symlink(target, os.path.join(root, 'link.txt'))
        receipt(os.path.join(root, 'regular.txt'), rev1, sha1)
        rc, txt, err = run(root)
        arm('ARM14_symlink_not_a_receipt', rc == 1
            and 'RECEIPT_BIND_ROW %s' % os.path.join(root, 'link.txt') in txt
            and 'state=unbound detail=not-regular-file' in txt
            and 'RECEIPT_BIND_ROW %s' % os.path.join(root, 'regular.txt') in txt
            and 'state=bound' in txt
            and 'RECEIPT_BIND: receipts=2 bound=1 corrected=0 design=0 '
                'unbound=1' in txt,
            'rc=%r %r %r' % (rc, txt, err))

    finally:
        shutil.rmtree(work, ignore_errors=True)

    out.write('RECEIPT_BIND_SELFTEST: %d/%d pass\n' % (ok, total))
    # round 83: the declared arm count is asserted, not just printed — a suite
    # that loses an arm call must not report a smaller perfect total
    return 0 if (ok == total == SELFTEST_ARMS) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--repo', default='.')
    ap.add_argument('--root', default='.ufo/evidence',
                    help='receipt population root (default .ufo/evidence)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        return sweep(a.repo, a.root)
    except SetupError as exc:
        print('RECEIPT_BIND error=setup:%s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
