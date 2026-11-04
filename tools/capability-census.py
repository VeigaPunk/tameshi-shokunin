#!/usr/bin/env python3
"""tools/capability-census.py — bind every `## Capabilities` row to repo state.

The lane's capability repertoire (`SCORECARD.md` `## Capabilities`) is its own
self-assessment of what it can do. Before this tool, 18 of the 30 rows were
bound to a live figure by `tools/selfstate-freshness.json` and the other 12
were bound by nothing at all: no sweep re-read them, so a stale or invented
capability row could stand indefinitely. This instrument measures that gap
per row and refuses an unbound row.

A row is bound when its census disposition verifies against committed bytes:

  live        the manifest names a `tools/selfstate-freshness.json` row whose
              `capability` cell equals the table row's name — the row's live
              figure is re-executed by the standing freshness sweep;
  historical  the manifest names a receipt path and revision, AND that path is
              one the row itself cites (exact backticked token, or inside a
              cited directory), AND the path resolves at that revision through
              git objects. A disposition naming a receipt the row never cited
              is refused: relabelling a row is not binding it.

Verdict lines (stdout, only after the document and both manifests parse):

  CAP_ROW <name> disposition=live|historical bound=yes|no reason=<token>
  CAP_CENSUS: rows=N bound=B unbound=U mismatches=M

Exit: 0 every row bound and no manifest defect; 1 at least one unbound row or
manifest defect (duplicate entry, live row naming a missing selfstate row,
historical pin not cited by its row or unresolvable at its revision); 2 setup
refusal before any stdout (unreadable document, absent `## Capabilities`
table, zero table rows, unparsable manifest, unknown disposition).

Read-only: git objects only; the document is read from the revision named on
the command line. Stdlib only; no sibling-module imports.
"""

import argparse
import json
import os
import re
import subprocess
import sys

TABLE_HEAD = '## Capabilities'
ROW_RE = re.compile(r'^\|(.+)\|\s*$')
TOKEN_RE = re.compile(r'`([^`]+)`')


class SetupError(Exception):
    pass


def lane_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_NO_REPLACE_OBJECTS='1', GIT_CONFIG_GLOBAL='/dev/null',
               GIT_CONFIG_NOSYSTEM='1')
    return env


def git(repo, *args):
    return subprocess.run(['git', '-C', repo] + list(args),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=lane_env())


def read_doc(repo, rev, path):
    proc = git(repo, 'cat-file', 'blob', '%s:%s' % (rev, path))
    if proc.returncode:
        raise SetupError('document-unreadable:%s:%s' % (rev, path))
    return proc.stdout.decode('utf-8')


def parse_rows(text):
    """Return [(name, full_row_text)] from the `## Capabilities` table.

    A row continues on following lines until the next table row; the
    continuation text is kept because a row's cited receipts may sit there.
    """
    lines = text.splitlines()
    try:
        start = lines.index(TABLE_HEAD)
    except ValueError:
        raise SetupError('capabilities-table-absent')
    rows = []
    cur = None
    for line in lines[start + 1:]:
        if line.startswith('## '):
            break
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) < 3:
                raise SetupError('malformed-table-row:%s' % line[:80])
            if set(cells[0]) <= set('-: ') or cells[0] == 'Capability':
                continue
            cur = {'name': cells[0], 'text': line}
            rows.append(cur)
        elif cur is not None and line.strip():
            cur['text'] += '\n' + line.strip()
    if not rows:
        raise SetupError('zero-table-rows')
    return rows


def cited(row_text):
    return TOKEN_RE.findall(row_text)


def is_cited(row_text, path):
    """A row cites a receipt by naming it, either as its own backticked token
    or as a word inside a cited command (`bash tools/mutate-and-run.sh
    --regression`), or by naming a directory that contains it."""
    for token in cited(row_text):
        for part in [token] + token.split():
            if path == part or part.startswith(path) or path.startswith(part):
                return True
    return False


def census(repo, doc_rev, doc_path, manifest_path, selfstate_path, out=sys.stdout):
    text = read_doc(repo, doc_rev, doc_path)
    rows = parse_rows(text)
    try:
        with open(manifest_path, encoding='utf-8') as fh:
            manifest = json.load(fh)
        with open(selfstate_path, encoding='utf-8') as fh:
            selfstate = json.load(fh)
    except (OSError, ValueError) as exc:
        raise SetupError('manifest-unreadable:%s' % exc)
    if manifest.get('schema') != 'tameshi-capability-census-v1':
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
            out.write('CAP_ROW %s disposition=none bound=no reason=no-disposition\n' % name)
            continue
        disp = entry.get('disposition')
        if disp == 'live':
            wanted = entry.get('selfstate_row')
            if name not in live_rows:
                out.write('CAP_ROW %s disposition=live bound=no reason=no-live-row\n' % name)
                continue
            if wanted not in live_rows[name]:
                out.write('CAP_ROW %s disposition=live bound=no reason=selfstate-id-mismatch\n' % name)
                continue
            bound += 1
            out.write('CAP_ROW %s disposition=live bound=yes reason=selfstate:%s\n'
                      % (name, wanted))
        elif disp == 'historical':
            pin = entry.get('receipt') or {}
            path, rev = pin.get('path'), pin.get('rev')
            if not path or not rev:
                out.write('CAP_ROW %s disposition=historical bound=no reason=pin-incomplete\n' % name)
                continue
            if not is_cited(body, path):
                out.write('CAP_ROW %s disposition=historical bound=no reason=pin-not-cited\n' % name)
                continue
            if git(repo, 'cat-file', '-e', '%s:%s' % (rev, path)).returncode:
                out.write('CAP_ROW %s disposition=historical bound=no reason=pin-unresolvable\n' % name)
                continue
            bound += 1
            out.write('CAP_ROW %s disposition=historical bound=yes reason=pin:%s@%s\n'
                      % (name, path, rev[:12]))
        else:
            raise SetupError('unknown-disposition:%r:%s' % (disp, name))
    for name in unexpected:
        out.write('CAP_ROW %s disposition=extra bound=no reason=not-in-table\n' % name)
    out.write('CAP_CENSUS: rows=%d bound=%d unbound=%d mismatches=%d\n'
              % (len(rows), bound, len(rows) - bound, mismatches))
    return 0 if bound == len(rows) and mismatches == 0 else 1


def selftest(out=sys.stdout):
    import tempfile
    ok = 0
    total = 10

    def arm(name, passed, detail=''):
        nonlocal ok
        if passed:
            ok += 1
            out.write('SELFTEST_%s: PASS\n' % name)
        else:
            out.write('SELFTEST_%s: FAIL %s\n' % (name, detail))

    doc = ('# doc\n\n## Capabilities\n\n| Capability | What | Evidence | Round |\n'
           '|---|---|---|---|\n'
           '| alpha | does a | `r/a.txt` | r1 |\n'
           '| beta | does b | `r/b.txt` | r2 |\n')
    selfstate = {'rows': [{'id': 'alpha-live', 'mode': 'capability',
                           'capability': 'alpha'}]}
    try:
        work = tempfile.mkdtemp(prefix='cap-census-selftest-',
                                dir=os.environ.get('TMPDIR') or None)
    except OSError as exc:
        sys.stderr.write('capability-census: selftest setup refused:%s\n' % exc)
        return 2
    try:
        repo = os.path.join(work, 'repo')
        os.makedirs(os.path.join(repo, 'r'))
        with open(os.path.join(repo, 'r', 'a.txt'), 'w') as fh:
            fh.write('a\n')
        with open(os.path.join(repo, 'r', 'b.txt'), 'w') as fh:
            fh.write('b\n')
        with open(os.path.join(repo, 'DOC.md'), 'w') as fh:
            fh.write(doc)
        subprocess.run(['git', '-C', repo, 'init', '-q'], check=True)
        subprocess.run(['git', '-C', repo, '-c', 'user.name=f', '-c',
                        'user.email=f@invalid', '-c', 'commit.gpgsign=false',
                        'add', '-A'], check=True)
        subprocess.run(['git', '-C', repo, '-c', 'user.name=f', '-c',
                        'user.email=f@invalid', '-c', 'commit.gpgsign=false',
                        'commit', '-qm', 'fixture'], check=True)
        rev = subprocess.run(['git', '-C', repo, 'rev-parse', 'HEAD'],
                             capture_output=True, text=True,
                             env=lane_env()).stdout.strip()
        ss = os.path.join(work, 'selfstate.json')
        with open(ss, 'w') as fh:
            json.dump(selfstate, fh)

        def run(manifest):
            path = os.path.join(work, 'manifest.json')
            with open(path, 'w') as fh:
                json.dump(manifest, fh) if not isinstance(manifest, str) else fh.write(manifest)
            import io
            buf = io.StringIO()
            try:
                code = census(repo, rev, 'DOC.md', path, ss, out=buf)
            except SetupError as exc:
                return 2, str(exc), buf.getvalue()
            return code, buf.getvalue(), ''

        def m(rows):
            return {'schema': 'tameshi-capability-census-v1', 'rows': rows}

        code, txt, _ = run(m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/b.txt', 'rev': rev}}]))
        arm('all-bound-exit0', code == 0 and 'bound=2 unbound=0 mismatches=0' in txt, txt)

        code, txt, _ = run(m([{'capability': 'alpha', 'disposition': 'live',
                               'selfstate_row': 'alpha-live'}]))
        arm('missing-disposition-refused',
            code == 1 and 'CAP_ROW beta disposition=none bound=no' in txt, txt)

        code, txt, _ = run(m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/zzz.txt', 'rev': rev}}]))
        arm('uncited-pin-refused',
            code == 1 and 'reason=pin-not-cited' in txt, txt)

        code, txt, _ = run(m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/b.txt', 'rev': '0' * 40}}]))
        arm('unresolvable-pin-refused',
            code == 1 and 'reason=pin-unresolvable' in txt, txt)

        code, txt, _ = run(m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'wrong-id'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/b.txt', 'rev': rev}}]))
        arm('wrong-live-id-refused',
            code == 1 and 'reason=selfstate-id-mismatch' in txt, txt)

        code, txt, _ = run(m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/b.txt', 'rev': rev}}]))
        arm('duplicate-entry-counted',
            code == 1 and 'mismatches=1' in txt, txt)

        code, txt, _ = run(m([
            {'capability': 'alpha', 'disposition': 'live',
             'selfstate_row': 'alpha-live'},
            {'capability': 'beta', 'disposition': 'historical',
             'receipt': {'path': 'r/b.txt', 'rev': rev}},
            {'capability': 'ghost', 'disposition': 'live',
             'selfstate_row': 'alpha-live'}]))
        arm('extra-entry-counted',
            code == 1 and 'reason=not-in-table' in txt, txt)

        code, txt, _ = run('{"schema":"tameshi-capability-census-v1","rows":[]}')
        arm('empty-manifest-all-unbound',
            code == 1 and 'rows=2 bound=0 unbound=2' in txt, txt)

        import io as _io
        buf = _io.StringIO()
        with open(os.path.join(repo, 'DOC2.md'), 'w') as fh:
            fh.write(doc.replace('`r/b.txt`', '`bash r/b.txt --flag`'))
        subprocess.run(['git', '-C', repo, '-c', 'user.name=f', '-c',
                        'user.email=f@invalid', '-c', 'commit.gpgsign=false',
                        'add', '-A'], check=True)
        subprocess.run(['git', '-C', repo, '-c', 'user.name=f', '-c',
                        'user.email=f@invalid', '-c', 'commit.gpgsign=false',
                        'commit', '-qm', 'fixture2'], check=True)
        rev2 = subprocess.run(['git', '-C', repo, 'rev-parse', 'HEAD'],
                              capture_output=True, text=True,
                              env=lane_env()).stdout.strip()
        path = os.path.join(work, 'manifest2.json')
        with open(path, 'w') as fh:
            json.dump(m([{'capability': 'alpha', 'disposition': 'live',
                          'selfstate_row': 'alpha-live'},
                         {'capability': 'beta', 'disposition': 'historical',
                          'receipt': {'path': 'r/b.txt', 'rev': rev2}}]), fh)
        try:
            code = census(repo, rev2, 'DOC2.md', path, ss, out=buf)
            txt = buf.getvalue()
        except SetupError as exc:
            code, txt = 2, str(exc)
        arm('command-token-cite-binds', code == 0 and 'bound=2' in txt, txt)

        code, txt, _ = run('not json')
        arm('unparsable-manifest-setup-refusal', code == 2, txt)
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)
    out.write('CAPABILITY_CENSUS_SELFTEST: %d/%d pass\n' % (ok, total))
    return 0 if ok == total else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--repo', default='.')
    ap.add_argument('--rev')
    ap.add_argument('--doc', default='SCORECARD.md')
    ap.add_argument('--manifest', default='tools/capability-census.json')
    ap.add_argument('--selfstate', default='tools/selfstate-freshness.json')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.rev:
        ap.error('--rev is required outside --selftest')
    try:
        return census(a.repo, a.rev, a.doc, a.manifest, a.selfstate)
    except SetupError as exc:
        sys.stderr.write('capability-census: setup refusal %s\n' % exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
