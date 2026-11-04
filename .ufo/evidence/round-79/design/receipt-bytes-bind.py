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

  * a regular file under `--root` (default `.ufo/evidence`) whose text carries
    exactly one `# measured_rev: <rev>`, one `# tool: <repo-relative path>`
    and one `# tool_sha256: <64 hex>` header line — the lane's receipt-header
    convention, first used in round 78;
  * an optional append-only correction `# measured_bytes_rev: <rev>` names the
    commit whose bytes carry the recorded sha when the measured revision does
    not (the receipt was produced from a worktree whose bytes landed later).

A receipt measures one of:

  bound      sha256(`git cat-file blob <measured_rev>:<tool>`) == tool_sha256
  corrected  the measured-rev bytes differ, and exactly one
             `measured_bytes_rev` resolves and its bytes carry the sha
  unbound    neither, with the reason in `detail` (tool-absent,
             rev-unresolvable, bytes-rev-absent, bytes-rev-unresolvable,
             bytes-rev-mismatch)

A `measured_bytes_rev` that does not carry the recorded sha makes the receipt
unbound even when `measured_rev` happens to match: a false correction line is
never a pass.

Verdict lines:

  RECEIPT_BIND_ROW <path> measured_rev=<r12> tool=<path> recorded=<sha12>
                   carrying=<rev12|-> state=bound|corrected|unbound detail=<s>
  RECEIPT_BIND: receipts=N bound=B corrected=C unbound=U

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
import shutil
import subprocess
import sys
import tempfile

SELFTEST_ARMS = 10
REV_RE = re.compile(r'^# measured_rev:[ \t]*([0-9a-f]{7,40})[ \t]*$', re.M)
BYTES_REV_RE = re.compile(r'^# measured_bytes_rev:[ \t]*([0-9a-f]{7,40})[ \t]*$',
                          re.M)
TOOL_RE = re.compile(r'^# tool:[ \t]*(\S+)[ \t]*$', re.M)
SHA_RE = re.compile(r'^# tool_sha256:[ \t]*([0-9a-f]{64})[ \t]*$', re.M)
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


def parse_receipt(path):
    """Return the receipt's header block, or None when the file is not a
    receipt (carries no complete header triple). Raises SetupError on a
    duplicate header: an ambiguous block cannot be measured."""
    try:
        with open(path, 'rb') as fh:
            head = fh.read(HEAD_BYTES)
            head_text = head.decode('utf-8', 'replace')
            if not (REV_RE.search(head_text) or TOOL_RE.search(head_text)
                    or SHA_RE.search(head_text)
                    or BYTES_REV_RE.search(head_text)):
                return None
            rest = fh.read(MAX_RECEIPT_BYTES + 1 - len(head))
    except OSError as exc:
        raise SetupError('receipt-unreadable:%s:%s' % (path, exc))
    if len(head) + len(rest) > MAX_RECEIPT_BYTES:
        raise SetupError('receipt-too-large:%s' % path)
    text = head_text + rest.decode('utf-8', 'replace')
    revs, tools, shas, brevs = (_one(REV_RE, text), _one(TOOL_RE, text),
                                _one(SHA_RE, text), _one(BYTES_REV_RE, text))
    if not revs and not tools and not shas:
        return None
    if not (revs and tools and shas):
        raise SetupError('receipt-header-incomplete:%s' % path)
    for name, values in (('measured_rev', revs), ('tool', tools),
                         ('tool_sha256', shas), ('measured_bytes_rev', brevs)):
        if len(values) > 1:
            raise SetupError('receipt-header-duplicate:%s:%s' % (path, name))
    tool = tools[0]
    if tool.startswith('/') or '..' in tool.split('/'):
        raise SetupError('tool-path-not-repo-relative:%s:%s' % (path, tool))
    return {'path': path, 'measured_rev': revs[0], 'tool': tool,
            'tool_sha256': shas[0],
            'measured_bytes_rev': brevs[0] if brevs else None}


def measure_receipt(repo, rec):
    """Return (state, carrying_rev, detail) for one parsed receipt."""
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
            if not os.path.isfile(path):
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
    counts = {'bound': 0, 'corrected': 0, 'unbound': 0}
    for rec in receipts:
        state, carrying, detail = measure_receipt(repo, rec)
        counts[state] += 1
        out.write(
            'RECEIPT_BIND_ROW %s measured_rev=%s tool=%s recorded=%s '
            'carrying=%s state=%s detail=%s\n'
            % (rec['path'], rec['measured_rev'][:12], rec['tool'],
               rec['tool_sha256'][:12],
               (carrying or '-')[:12], state, detail))
    out.write('RECEIPT_BIND: receipts=%d bound=%d corrected=%d unbound=%d\n'
              % (len(receipts), counts['bound'], counts['corrected'],
                 counts['unbound']))
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

        def run(root):
            import io
            buf = io.StringIO()
            try:
                rc = sweep(repo, root, out=buf)
                err = ''
            except SetupError as exc:
                return 2, buf.getvalue(), str(exc)
            return rc, buf.getvalue(), err

        # arm 1: a receipt naming the revision that carries its sha -> bound
        root = os.path.join(work, 'pop1')
        os.makedirs(root)
        receipt(os.path.join(root, 'bound.txt'), rev1, sha1)
        rc, txt, err = run(root)
        arm('ARM1_bound', rc == 0 and 'state=bound' in txt
            and 'RECEIPT_BIND: receipts=1 bound=1 corrected=0 unbound=0' in txt,
            'rc=%r %r %r' % (rc, txt, err))

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
            and 'corrected=1 unbound=0' in txt,
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

        # arm 6: a duplicate header block is refused before any row effect
        root = os.path.join(work, 'pop6')
        os.makedirs(root)
        receipt(os.path.join(root, 'dup.txt'), rev1, sha1,
                extra='# measured_rev: %s\n' % rev2)
        rc, txt, err = run(root)
        arm('ARM6_duplicate_header_refused', rc == 2
            and 'RECEIPT_BIND:' not in txt
            and 'receipt-header-duplicate' in err,
            'rc=%r %r %r' % (rc, txt, err))

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

        # arm 10: a tool path outside the repo is a setup refusal
        root = os.path.join(work, 'pop10')
        os.makedirs(root)
        receipt(os.path.join(root, 'escape.txt'), rev1, sha1,
                tool='../outside.py')
        rc, txt, err = run(root)
        arm('ARM10_tool_path_escape_refused', rc == 2
            and 'RECEIPT_BIND:' not in txt
            and 'tool-path-not-repo-relative' in err,
            'rc=%r %r %r' % (rc, txt, err))
    finally:
        shutil.rmtree(work, ignore_errors=True)

    out.write('RECEIPT_BIND_SELFTEST: %d/%d pass\n' % (ok, total))
    return 0 if ok == total else 1


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
