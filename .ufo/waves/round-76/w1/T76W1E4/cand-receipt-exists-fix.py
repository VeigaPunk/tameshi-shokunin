#!/usr/bin/env python3
"""receipt-exists.py — cited-receipt existence sweep on committed bytes.

The cited-receipt-exists half of `considerthese/2026-10-28.md` proposal 1
(landed round 64): for each named document, read at a pinned revision via
`git show REV:path` (never the working tree), extract candidate evidence
paths, and resolve each against the same revision with
`git cat-file -e REV:path` — exit 0 means the object (blob or tree) exists
at REV, the `-e` semantics of held registry row S289.

Extraction rule (v1, disclosed): a candidate is a backtick span (a backtick
span never crosses a newline — the round-41 m8 lesson) whose first
whitespace-cut head matches `^([.]ufo|tools)/[A-Za-z0-9_@./+-]+` (a cite of
a lane evidence or tools path). A trailing `:` line reference, `#anchor` or
`*` glob in the head marks the span `skipped` and it is listed, not checked
(a v1 sweep does not guess referents). A trailing `/` is stripped before the
check so directory cites resolve through the tree object — the round-53.2
class (a cited `after/` directory that did not resolve). Corpus-relative
cites (`corpus/...`, `SCORECARD.md`, ...) are not candidates in v1: registry
rows and record files are addressed by their own criteria (97, 108), not by
this sweep.

Verdict lines:
  RECEIPT_EXISTS doc=<doc> checked=<n> skipped=<k> missing=<m>
  RECEIPT_EXISTS_MISSING doc=<doc> path=<path>     (one per missing path)
  RECEIPT_EXISTS_SKIPPED doc=<doc> span=<span>
  RECEIPT_EXISTS_EXTRA doc=<doc> path=<path> root=<root>  (filesystem hit)
  RECEIPT_EXISTS: docs=<d> paths=<total-checked> missing=<total-missing>
Exit 0 when every checked path resolves; 1 when at least one is missing;
2 on usage or setup (unresolvable rev, doc absent at rev, bad selftest).

--extra-root DIR (repeatable): a path missing in the lane repo is then
checked as a plain FILESYSTEM path under each extra root (the lane's
records cite some fleet-root surfaces — `.ufo/l0-questions.md`, the round
reports — by lane-relative spelling). A filesystem hit is a resolution
with a named location (`RECEIPT_EXISTS_EXTRA`), disclosed as a worktree
check, not a git-object check. Exit 0 iff nothing is missing after the
extra-root pass.

--selftest is hermetic: it builds a throwaway git repository under the
scratch root (TMPDIR), runs the tool against it out-of-process, and never
touches the lane. Every mkdtemp'd directory (the repo root and the
extra-root fixture) is removed in a `finally` via
`shutil.rmtree(..., ignore_errors=True)` — the S299 caller-deletion duty;
the selftest leaves zero scratch entries behind. Arms: green (cited blob and cited directory resolve,
exit 0), red (a cited path absent -> exit 1), usage (doc absent at the
rev -> exit 2), extra-root (a path absent in the repo resolving under an
extra root -> exit 0 with an EXTRA line). Prints
`RECEIPT_EXISTS_SELFTEST: <passed>/<total> pass`.
"""

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CAND = re.compile(r'^([.]ufo|tools)/[A-Za-z0-9_@./+-]+')
SPAN = re.compile(r'`([^`\n]+)`')


def git_run(repo, *args, inp=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['GIT_TERMINAL_PROMPT'] = '0'
    return subprocess.run(['git', '-C', str(repo), *args], capture_output=True,
                          input=inp, env=env)


def resolve_rev(repo, rev):
    r = git_run(repo, 'rev-parse', '--verify', '--quiet', rev + '^{commit}')
    if r.returncode != 0:
        return None
    return r.stdout.decode().strip()


def read_doc(repo, rev, doc):
    r = git_run(repo, 'show', '%s:%s' % (rev, doc))
    if r.returncode != 0:
        return None
    return r.stdout


def path_exists(repo, rev, path):
    # `-e` already suppresses output (git-cat-file §OPTIONS); there is no
    # --quiet option (probed: exit 129) — the missing-object error goes to
    # stderr and is captured, not printed.
    r = git_run(repo, 'cat-file', '-e', '%s:%s' % (rev, path))
    return r.returncode == 0


def extract(doc_bytes):
    text = doc_bytes.decode('utf-8', 'surrogateescape')
    checked, skipped = [], []
    for m in SPAN.finditer(text):
        head = m.group(1).strip().split(' ')[0] if m.group(1).strip() else ''
        head = head.rstrip('.,;:)')
        if not CAND.match(head):
            continue
        if head.endswith((':', '#')) or '*' in head or re.search(r':\d', head):
            skipped.append(m.group(1))
            continue
        path = head.rstrip('/')
        if path not in checked:
            checked.append(path)
    return checked, skipped


def sweep(repo, rev, docs, extra_roots=()):
    total_checked = total_missing = total_extra = 0
    for doc in docs:
        body = read_doc(repo, rev, doc)
        if body is None:
            print('RECEIPT_EXISTS error=doc-absent-at-rev doc=%s' % doc,
                  file=sys.stderr)
            return 2
        checked, skipped = extract(body)
        missing = []
        for path in checked:
            if path_exists(repo, rev, path):
                continue
            hit = None
            for root in extra_roots:
                if (Path(root) / path).is_file():
                    hit = str(root)
                    break
            if hit is None:
                missing.append(path)
            else:
                total_extra += 1
                print('RECEIPT_EXISTS_EXTRA doc=%s path=%s root=%s'
                      % (doc, path, hit))
        total_checked += len(checked)
        total_missing += len(missing)
        for s in skipped:
            print('RECEIPT_EXISTS_SKIPPED doc=%s span=%s' % (doc, s))
        for path in missing:
            print('RECEIPT_EXISTS_MISSING doc=%s path=%s' % (doc, path))
        print('RECEIPT_EXISTS doc=%s checked=%d skipped=%d missing=%d'
              % (doc, len(checked), len(skipped), len(missing)))
    print('RECEIPT_EXISTS: docs=%d paths=%d missing=%d extra=%d'
          % (len(docs), total_checked, total_missing, total_extra))
    return 1 if total_missing else 0


def selftest():
    tmp = tempfile.mkdtemp(prefix='receipt-exists-selftest-')
    extra = Path(tmp + '-extra')
    try:
        passed = failed = 0

        def arm(name, ok):
            nonlocal passed, failed
            if ok:
                passed += 1
            else:
                failed += 1
                print('FAIL %s' % name)

        def run_tool(argv):
            tool = Path(__file__).resolve()
            env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
            return subprocess.run([sys.executable, '-I', str(tool)] + argv,
                                  capture_output=True, env=env, cwd=tmp)

        g = lambda *a: git_run(tmp, *a)
        g('init', '-q')
        g('config', 'user.email', 'selftest@invalid')
        g('config', 'user.name', 'selftest')
        d = Path(tmp)
        (d / '.ufo/evidence/r64').mkdir(parents=True)
        (d / '.ufo/evidence/r64/ok.txt').write_bytes(b'receipt bytes\n')
        (d / '.ufo/evidence/r64/sub').mkdir(parents=True)
        (d / '.ufo/evidence/r64/sub/inner.txt').write_bytes(b'inner\n')
        (d / 'docs').mkdir()
        (d / 'docs/lesson.md').write_bytes(
            b'cite `.ufo/evidence/r64/ok.txt` and dir `.ufo/evidence/r64/sub/` '
            b'with suffix `.ufo/evidence/r64/ok.txt:12` skipped\n')
        (d / 'docs/bad.md').write_bytes(b'cite `.ufo/evidence/r64/gone.txt`\n')
        (d / 'docs/cross.md').write_bytes(b'cite `.ufo/other-root-file.txt`\n')
        g('add', '.')
        g('commit', '-qm', 'fixtures')
        rev = resolve_rev(tmp, 'HEAD')

        r = run_tool(['--repo', tmp, '--rev', rev, '--doc', 'docs/lesson.md'])
        out = r.stdout.decode('utf-8', 'replace')
        arm('green-exit0', r.returncode == 0 and 'missing=0' in out
            and 'checked=2' in out and 'skipped=1' in out)
        r = run_tool(['--repo', tmp, '--rev', rev, '--doc', 'docs/bad.md'])
        out = r.stdout.decode('utf-8', 'replace')
        arm('red-exit1', r.returncode == 1 and 'missing=1' in out
            and 'gone.txt' in out)
        r = run_tool(['--repo', tmp, '--rev', rev, '--doc', 'docs/absent.md'])
        arm('usage-exit2', r.returncode == 2)
        extra.mkdir()
        (extra / '.ufo').mkdir()
        (extra / '.ufo/other-root-file.txt').write_bytes(b'fleet-root surface\n')
        r = run_tool(['--repo', tmp, '--rev', rev, '--doc', 'docs/cross.md',
                      '--extra-root', str(extra)])
        out = r.stdout.decode('utf-8', 'replace')
        arm('extra-root-exit0', r.returncode == 0 and 'missing=0' in out
            and 'extra=1' in out and 'RECEIPT_EXISTS_EXTRA' in out)
        print('RECEIPT_EXISTS_SELFTEST: %d/%d pass' % (passed, passed + failed))
        return 1 if failed else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.rmtree(extra, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default='.')
    ap.add_argument('--rev')
    ap.add_argument('--doc', action='append')
    ap.add_argument('--extra-root', action='append', default=[])
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.rev or not a.doc:
        ap.print_usage()
        return 2
    repo = Path(a.repo).resolve()
    rev = resolve_rev(repo, a.rev)
    if rev is None:
        print('RECEIPT_EXISTS error=rev-unresolvable rev=%s' % a.rev,
              file=sys.stderr)
        return 2
    return sweep(repo, rev, a.doc, a.extra_root)


if __name__ == '__main__':
    sys.exit(main())
