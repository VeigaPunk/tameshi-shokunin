#!/usr/bin/env python3
"""tools/capability-census-v2.py — bind every `## Capabilities` row to repo
state, with the round-86 routed refusals.

Successor of `tools/capability-census.py` (round 86, frozen, verdict
unchanged): that census could not discriminate a receipt pin that resolved to
a TREE (its check was `git cat-file -e`, which accepts any object), accepted a
bare ancestor directory or a `path:line` token as the receipt path, and took
its manifest and self-state manifests from arbitrary caller paths (a
`--manifest` outside the repo printed the frozen after-state tuple while
binding nothing — round-86 probes P4/P5; lesson `## Mistakes` M4). This
instrument closes exactly those gaps and nothing else:

* every `git` invocation runs a git binary resolved ONCE at startup with
  `shutil.which("git")`; the resolved absolute path is used for every child
  call, so the data channel is not PATH-inherited after resolution (r86
  attempt-3 probes P1/P2), and a missing git fails closed (exit 2);
* manifest and self-state are read FROM GIT OBJECTS at `--rev` through
  repo-relative paths — a caller-supplied file outside the repo is refused;
* a historical pin must be repo-relative (no leading `/`, no `..`, no
  backslash, no drive qualifier, no trailing `/`, and no `:` anywhere, which
  refuses `path:line` tokens) AND must resolve as a REGULAR BLOB:
  `git cat-file -t <rev>:<path>` must print exactly `blob` — a tree,
  commit or tag pin is refused (`pin-not-blob`), an unresolvable pin is
  (`pin-unresolvable`);
* citation matching is exact-token: the pin path must appear as its own
  backticked token in the row, or as a whole word inside a cited command, or
  under a cited directory token (ending in `/`). A `path:line` token never
  prefix-satisfies a pin (it does not end in `/` and never equals the pin);
* the table parser refuses, instead of skipping, a second header-like row
  (`Capability` as a data row), duplicate capability rows, a missing header
  or separator row, and empty capability cells;
* duplicate manifest entries and manifest names that are not table rows stay
  mismatches.

Verdict lines (stdout, only after document and both manifests parse):

  CAP2_ROW <name> disposition=live|historical bound=yes|no reason=<token>
  CAP_CENSUS_V2: rows=N bound=B unbound=U mismatches=M

Exit: 0 every row bound and no manifest defect; 1 at least one unbound row or
manifest defect; 2 setup refusal before any stdout (unreadable document at
the revision, absent/malformed table, manifest or self-state not readable AT
the revision through their repo-relative paths, unparsable manifest, unknown
disposition, git binary unresolvable, cwd not a git repository).

Read-only: git objects only. Stdlib only; no sibling-module imports.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys

TABLE_HEAD = '## Capabilities'
ROW_RE = re.compile(r'^\|(.+)\|\s*$')
TOKEN_RE = re.compile(r'`([^`]+)`')


class SetupError(Exception):
    pass


TRUSTED_DIRS = ('/usr/bin', '/bin')


def resolve_git():
    """Resolve git ONCE from the trusted system directories, never from the
    caller's PATH (r86 attempt-3 probes P1/P2: a PATH shim received every
    git call). The returned absolute path is the only git this process runs.
    """
    path = shutil.which('git', path=os.pathsep.join(TRUSTED_DIRS))
    if not path or not os.path.isabs(path):
        raise SetupError('git-unresolved')
    return path


GIT = None


def lane_env(extra=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_NO_REPLACE_OBJECTS='1', GIT_CONFIG_GLOBAL='/dev/null',
               GIT_CONFIG_NOSYSTEM='1')
    if extra:
        env.update(extra)
    return env


def git(repo, *args):
    return subprocess.run([GIT, '-C', repo] + list(args),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=lane_env())


def read_blob(repo, rev, path):
    proc = git(repo, 'cat-file', 'blob', '%s:%s' % (rev, path))
    if proc.returncode:
        raise SetupError('blob-unreadable:%s:%s' % (rev[:12], path))
    return proc.stdout.decode('utf-8')


def repo_relative(path):
    """A repo-relative POSIX path usable as a pin or manifest location:
    no absolute form, no parent segment, no backslash, no drive qualifier,
    no `:` (path:line tokens are not paths), no trailing `/` (a bare
    ancestor directory is not a receipt), not `.` (round-80 sentinel F5 plus
    the r86 M4 classes)."""
    if not isinstance(path, str) or not path:
        return False
    if path.startswith('/') or '\\' in path or re.match(r'^[A-Za-z]:', path):
        return False
    if ':' in path or path.endswith('/') or path == '.' or path == '..':
        return False
    return '..' not in path.split('/') and os.path.basename(path) != ''


def parse_rows(text):
    """Return [(name, full_row_text)] from the `## Capabilities` table.

    Strict header discipline: the first `|` line after the heading must be
    the header row, the next must be the separator; a later header-like or
    duplicate row is a refusal, never a skipped row."""
    lines = text.splitlines()
    try:
        start = lines.index(TABLE_HEAD)
    except ValueError:
        raise SetupError('capabilities-table-absent')
    rows = []
    cur = None
    saw_header = False
    saw_separator = False
    names = set()
    for line in lines[start + 1:]:
        if line.startswith('## '):
            break
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if not saw_header:
                if not cells or cells[0] != 'Capability':
                    raise SetupError('table-header-absent')
                saw_header = True
                continue
            if not saw_separator:
                if len(cells) < 2 or not set(cells[0]) <= set('-: '):
                    raise SetupError('table-separator-absent')
                saw_separator = True
                continue
            if len(cells) < 3:
                raise SetupError('malformed-table-row:%s' % line[:80])
            if set(cells[0]) <= set('-: '):
                raise SetupError('table-separator-repeated')
            if cells[0] == 'Capability':
                raise SetupError('table-header-row-repeated')
            if not cells[0]:
                raise SetupError('empty-table-cell')
            if cells[0] in names:
                raise SetupError('duplicate-table-row:%s' % cells[0])
            names.add(cells[0])
            cur = {'name': cells[0], 'text': line}
            rows.append(cur)
        elif cur is not None and line.strip():
            cur['text'] += '\n' + line.strip()
    if not saw_header:
        raise SetupError('capabilities-table-absent')
    if not saw_separator:
        raise SetupError('table-separator-absent')
    if not rows:
        raise SetupError('zero-table-rows')
    return rows


def cited(row_text):
    return TOKEN_RE.findall(row_text)


def is_cited(row_text, path):
    """The pin path is cited when the row names it exactly: as its own
    backticked token, as a whole word inside a cited command, or under a
    cited directory token (ending in `/`). A `path:line` token never
    prefix-satisfies (r86 M4: it must not stand for the receipt path)."""
    for token in cited(row_text):
        if token == path:
            return True
        for part in token.split():
            if part == path:
                return True
            if part.endswith('/') and path.startswith(part):
                return True
    return False


REGULAR_MODES = ('100644', '100755')


def tree_at(repo, rev):
    """Exact recursive listing {path: (mode, type, oid)} at REV. Matching is
    done in Python, so no pathspec magic redirects a named path."""
    proc = git(repo, 'ls-tree', '-r', '-z', rev)
    if proc.returncode:
        raise SetupError('tree-unreadable:%s' % rev[:12])
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


def pin_state(tree, path):
    """'blob' only for a regular blob entry (100644/100755). A symlink (120000)
    is a blob whose bytes are its target, so `cat-file -t` alone would bind
    it; a tree (directory prefix) and a gitlink are refused by name."""
    hit = tree.get(path)
    if hit is not None:
        mode, otype, _ = hit
        if mode in REGULAR_MODES and otype == 'blob':
            return 'blob'
        return 'not-regular:%s' % mode
    if any(name.startswith(path + '/') for name in tree):
        return 'not-blob:tree'
    return None


def census(repo, doc_rev, doc_path, manifest_path, selfstate_path,
           out=sys.stdout):
    global GIT
    if GIT is None:
        GIT = resolve_git()
    probe = git(repo, 'rev-parse', '--git-dir')
    if probe.returncode != 0:
        raise SetupError('repo-unusable:%s' % repo)
    for rel in (doc_path, manifest_path, selfstate_path):
        if not repo_relative(rel):
            raise SetupError('path-not-repo-relative:%s' % rel)
    text = read_blob(repo, doc_rev, doc_path)
    rows = parse_rows(text)
    tree = tree_at(repo, doc_rev)
    manifest = json_load_git(repo, doc_rev, manifest_path, 'manifest')
    selfstate = json_load_git(repo, doc_rev, selfstate_path, 'self-state')
    if manifest.get('schema') != 'tameshi-capability-census-v2':
        raise SetupError('manifest-schema:%r' % manifest.get('schema'))
    entries = manifest.get('rows')
    if not isinstance(entries, list):
        raise SetupError('manifest-rows-not-a-list')
    live_rows = {}
    for row in selfstate.get('rows') or []:
        if row.get('mode') == 'capability' and row.get('capability'):
            live_rows.setdefault(row['capability'], set()).add(row.get('id'))
    by_name = {}
    mismatches = 0
    for entry in entries:
        name = entry.get('capability')
        if name in by_name:
            mismatches += 1
        by_name[name] = entry
    names = [r['name'] for r in rows]
    unexpected = sorted(set(by_name) - set(names))
    mismatches += len(unexpected)
    bound = 0
    for row in rows:
        name, body = row['name'], row['text']
        entry = by_name.get(name)
        if entry is None:
            out.write('CAP2_ROW %s disposition=none bound=no reason=no-disposition\n'
                      % name)
            continue
        disp = entry.get('disposition')
        if disp == 'live':
            wanted = entry.get('selfstate_row')
            if name not in live_rows:
                out.write('CAP2_ROW %s disposition=live bound=no reason=no-live-row\n'
                          % name)
                continue
            if wanted not in live_rows[name]:
                out.write('CAP2_ROW %s disposition=live bound=no reason=selfstate-id-mismatch\n'
                          % name)
                continue
            bound += 1
            out.write('CAP2_ROW %s disposition=live bound=yes reason=selfstate:%s\n'
                      % (name, wanted))
        elif disp == 'historical':
            pin = entry.get('receipt') or {}
            path, rev = pin.get('path'), pin.get('rev')
            if not path or not rev:
                out.write('CAP2_ROW %s disposition=historical bound=no reason=pin-incomplete\n'
                          % name)
                continue
            if not repo_relative(path):
                out.write('CAP2_ROW %s disposition=historical bound=no reason=pin-path-shape\n'
                          % name)
                continue
            if not is_cited(body, path):
                out.write('CAP2_ROW %s disposition=historical bound=no reason=pin-not-cited\n'
                          % name)
                continue
            try:
                state = pin_state(tree_at(repo, rev), path)
            except SetupError:
                state = None
            if state is None:
                out.write('CAP2_ROW %s disposition=historical bound=no reason=pin-unresolvable\n'
                          % name)
                continue
            if state != 'blob':
                out.write('CAP2_ROW %s disposition=historical bound=no reason=pin-%s\n'
                          % (name, state))
                continue
            bound += 1
            out.write('CAP2_ROW %s disposition=historical bound=yes reason=pin:%s@%s\n'
                      % (name, path, rev[:12]))
        else:
            raise SetupError('unknown-disposition:%r:%s' % (disp, name))
    for name in unexpected:
        out.write('CAP2_ROW %s disposition=extra bound=no reason=not-in-table\n'
                  % name)
    out.write('CAP_CENSUS_V2: rows=%d bound=%d unbound=%d mismatches=%d\n'
              % (len(rows), bound, len(rows) - bound, mismatches))
    return 0 if bound == len(rows) and mismatches == 0 else 1


def json_load_git(repo, rev, path, what):
    import json
    proc = git(repo, 'cat-file', 'blob', '%s:%s' % (rev, path))
    if proc.returncode:
        raise SetupError('%s-unbound:%s:%s' % (what, rev[:12], path))
    try:
        return json.loads(proc.stdout.decode('utf-8'))
    except (UnicodeDecodeError, ValueError) as exc:
        raise SetupError('%s-unparsable:%s' % (what, exc))


def selftest(out=sys.stdout):
    import json
    import tempfile
    ok = 0
    total = 15

    def arm(name, passed, detail=''):
        nonlocal ok
        if passed:
            ok += 1
            out.write('SELFTEST_%s: PASS\n' % name)
        else:
            out.write('SELFTEST_%s: FAIL %s\n' % (name, detail))

    doc = ('# doc\n\n## Capabilities\n\n'
           '| Capability | What | Evidence | Round |\n'
           '|---|---|---|---|\n'
           '| alpha | does a | `r/a.txt` | r1 |\n'
           '| beta | does b | `bash tools/run.sh --x r/b.txt`, dir `r/` '
           '| r2 |\n')
    doc_dup = doc.replace('| beta | does b', '| alpha | does a2')
    doc_headerrow = doc.replace('| beta | does b', '| Capability | c |')
    selfstate = {'rows': [{'id': 'alpha-live', 'mode': 'capability',
                           'capability': 'alpha'}]}
    global GIT
    try:
        GIT = resolve_git()
        work = tempfile.mkdtemp(prefix='cap-census-v2-selftest-',
                                dir=os.environ.get('TMPDIR') or None)
    except SetupError as exc:
        sys.stderr.write('capability-census-v2: selftest setup refused:%s\n'
                         % exc)
        return 2
    except OSError as exc:
        sys.stderr.write('capability-census-v2: selftest setup refused:%s\n'
                         % exc)
        return 2
    try:
        repo = os.path.join(work, 'repo')
        os.makedirs(os.path.join(repo, 'r'))
        os.makedirs(os.path.join(repo, 'r', 'subdir'))
        for rel, body in (('r/a.txt', 'a\n'), ('r/b.txt', 'b\n'),
                           ('r/subdir/x.txt', 'x\n')):
            with open(os.path.join(repo, rel), 'w') as fh:
                fh.write(body)
        os.symlink('a.txt', os.path.join(repo, 'r', 'link'))
        with open(os.path.join(repo, 'DOC.md'), 'w') as fh:
            fh.write(doc)
        env = lane_env({'GIT_CONFIG_GLOBAL': '/dev/null',
                        'GIT_CONFIG_NOSYSTEM': '1'})
        ident = ['-c', 'user.name=f', '-c', 'user.email=f@invalid',
                 '-c', 'commit.gpgsign=false']
        subprocess.run([GIT, '-C', repo, 'init', '-q'], check=True, env=env)
        subprocess.run([GIT, '-C', repo] + ident + ['add', '-A'], check=True,
                       env=env)
        subprocess.run([GIT, '-C', repo] + ident + ['commit', '-qm',
                                                    'fixture'], check=True,
                       env=env)
        rev = subprocess.run([GIT, '-C', repo, 'rev-parse', 'HEAD'],
                             capture_output=True, text=True,
                             env=env).stdout.strip()

        def run(doc_text=doc, manifest=None, doc_name='DOC.md',
                manifest_name='m.json'):
            def commit():
                subprocess.run([GIT, '-C', repo] + ident +
                               ['commit', '-qm', 'fixture', '--allow-empty'],
                               check=True, env=env,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
                return subprocess.run([GIT, '-C', repo, 'rev-parse', 'HEAD'],
                                      capture_output=True, text=True,
                                      env=env).stdout.strip()
            with open(os.path.join(repo, 'DOC.md'), 'w') as fh:
                fh.write(doc_text)
            subprocess.run([GIT, '-C', repo, 'add', '-A'], check=True,
                           env=env, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            commit()
            with open(os.path.join(repo, 'm.json'), 'w') as fh:
                json.dump(manifest, fh) if manifest is not None \
                    else fh.write(manifest)
            subprocess.run([GIT, '-C', repo, 'add', '-A'], check=True,
                           env=env, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            r2 = commit()
            ss = os.path.join(repo, 'ss.json')
            with open(ss, 'w') as fh:
                json.dump(selfstate, fh)
            subprocess.run([GIT, '-C', repo, 'add', '-A'], check=True,
                           env=env, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            r3 = commit()
            import io
            buf = io.StringIO()
            try:
                code = census(repo, r3, doc_name, manifest_name, 'ss.json',
                              out=buf)
            except SetupError as exc:
                return 2, str(exc), buf.getvalue()
            return code, buf.getvalue(), ''

        def m(rows):
            return {'schema': 'tameshi-capability-census-v2', 'rows': rows}

        code, txt, _ = run(manifest=m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/b.txt', 'rev': rev}}]))
        arm('all-bound-exit0',
            code == 0 and 'bound=2 unbound=0 mismatches=0' in txt, txt[:200])

        code, txt, _ = run(manifest=m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'}]))
        arm('missing-disposition-refused',
            code == 1 and 'CAP2_ROW beta disposition=none' in txt, txt[:200])

        code, txt, _ = run(manifest=m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'q/zzz.txt', 'rev': rev}}]))
        arm('uncited-pin-refused',
            code == 1 and 'reason=pin-not-cited' in txt, txt[:200])

        code, txt, _ = run(manifest=m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/b.txt', 'rev': '0' * 40}}]))
        arm('unresolvable-pin-refused',
            code == 1 and 'reason=pin-unresolvable' in txt, txt[:200])

        code, txt, _ = run(manifest=m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/subdir', 'rev': rev}}]))
        arm('tree-pin-refused',
            code == 1 and 'reason=pin-not-blob:tree' in txt, txt[:200])

        code, txt, _ = run(manifest=m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/', 'rev': rev}}]))
        arm('ancestor-dir-pin-refused',
            code == 1 and 'reason=pin-path-shape' in txt, txt[:200])

        code, txt, _ = run(manifest=m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/b.txt:12', 'rev': rev}}]))
        arm('pathline-pin-refused',
            code == 1 and 'reason=pin-path-shape' in txt, txt[:200])

        code, txt, _ = run(manifest=m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/b.txt', 'rev': rev}}]),
            manifest_name='absent.json')
        arm('manifest-unbound-refused',
            code == 2 and 'manifest-unbound' in txt, txt[:200])

        code, txt, err = run(doc_text=doc_dup, manifest=m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'}]))
        arm('duplicate-table-row-refused',
            code == 2 and 'duplicate-table-row' in txt, txt[:200])

        code, txt, err = run(doc_text=doc_headerrow, manifest=m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'}]))
        arm('capability-data-row-refused',
            code == 2 and 'table-header-row-repeated' in txt, txt[:200])

        code, txt, _ = run(manifest=m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'wrong-id'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/b.txt', 'rev': rev}}]))
        arm('wrong-live-id-refused',
            code == 1 and 'reason=selfstate-id-mismatch' in txt, txt[:200])

        code, txt, _ = run(manifest=m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/b.txt', 'rev': rev}}]))
        arm('duplicate-manifest-entry-counted',
            code == 1 and 'mismatches=1' in txt, txt[:200])

        code, txt, _ = run(manifest=m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/b.txt', 'rev': rev}},
            {'capability': 'ghost', 'disposition': 'live',
             'selfstate_row': 'alpha-live'}]))
        arm('extra-manifest-name-counted',
            code == 1 and 'reason=not-in-table' in txt and 'mismatches=1' in
            txt, txt[:200])

        code, txt, _ = run(manifest=m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/link', 'rev': rev}}]))
        arm('symlink-pin-refused',
            code == 1 and 'reason=pin-not-regular:120000' in txt, txt[:200])

        shim = os.path.join(work, 'shim')
        os.makedirs(shim)
        with open(os.path.join(shim, 'git'), 'w') as fh:
            fh.write('#!/bin/sh\nexit 99\n')
        os.chmod(os.path.join(shim, 'git'), 0o755)
        envpath = lane_env({'PATH': shim})
        proc = subprocess.run([sys.executable, '-I', os.path.abspath(__file__),
                               '--repo', repo, '--rev', rev,
                               '--doc', 'DOC.md', '--manifest', 'm.json',
                               '--selfstate', 'ss.json'],
                              capture_output=True, text=True, env=envpath,
                              cwd=repo)
        arm('path-shim-ignored',
            proc.returncode == 2 and 'manifest-unbound' in proc.stderr
            or proc.returncode in (0, 1) and 'CAP_CENSUS_V2' in proc.stdout,
            proc.stderr[:200] + proc.stdout[:200])
    finally:
        import shutil as _sh
        _sh.rmtree(work, ignore_errors=True)
    out.write('CAPABILITY_CENSUS_V2_SELFTEST: %d/%d pass\n' % (ok, total))
    return 0 if ok == total else 1


def main():
    global GIT
    p = argparse.ArgumentParser(
        description='Bind every `## Capabilities` row to repo state (v2).')
    p.add_argument('--repo')
    p.add_argument('--rev')
    p.add_argument('--doc', default='SCORECARD.md')
    p.add_argument('--manifest', default='tools/capability-census-v2.json')
    p.add_argument('--selfstate', default='tools/selfstate-freshness.json')
    p.add_argument('--selftest', action='store_true')
    a = p.parse_args()
    if a.selftest:
        return selftest()
    if not a.repo or not a.rev:
        p.error('--repo and --rev are required without --selftest')
    try:
        GIT = resolve_git()
        return census(a.repo, a.rev, a.doc, a.manifest, a.selfstate)
    except SetupError as exc:
        sys.stderr.write('capability-census-v2: setup refusal %s\n' % exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
