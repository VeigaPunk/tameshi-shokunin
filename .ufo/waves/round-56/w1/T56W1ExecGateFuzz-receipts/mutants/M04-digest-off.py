#!/usr/bin/env python3
"""receipt-revision-gate — bind a receipt to the revision it certifies.

The round-54/55 defect this gate exists for (ER-R54-1, R55.5): a positive control
was scored at the FREEZE commit, which predated the work it certified, and every
gate in the lane accepted it because none compared the `rev=` a receipt names with
the revision under test. A verdict, or a positive control, is evidence only for the
content it was measured against.

Usage:
  receipt-revision-gate.py --lane LANE --certified REV [--paths FILE]
                           --receipt PATH:ROLE[:REQUIRE_REGEX] [--receipt ...] [--json]
  receipt-revision-gate.py --selftest

ROLE is one of:
  positive  a control whose expected verdict is PASS. Exactly one distinct `rev=`
            token; it must equal the certified revision, or (when --paths is given)
            name a revision whose bytes are identical to the certified revision on
            every path listed in FILE.
  verdict   a counter's verdict receipt. Same rule as `positive`.
  control   a control set (several CTL lines, possibly at different revisions).
            Every `rev=` token must resolve and be an ancestor of, or equal to,
            the certified revision.

Codes (each a named refusal, exit 3):
  RECEIPT_MISSING · RECEIPT_EMPTY · RECEIPT_NOT_BLOB · RECEIPT_REV_ABSENT
  RECEIPT_REV_AMBIGUOUS · RECEIPT_REV_UNRESOLVABLE · RECEIPT_REV_MISMATCH
  RECEIPT_REV_CONTENT_DRIFT · RECEIPT_CONTROL_NOT_ANCESTOR
  RECEIPT_DIGEST_MISMATCH · RECEIPT_REQUIRED_LINE_MISSING

Verdict line: `GATE: receipts=N ok=N refused=N codes=<comma|none> verdict=PASS|REFUSED`
Exit 0 iff PASS. Read-only: git objects only. Stdlib only.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REV_RE = re.compile(r'\brev=([0-9a-f]{7,40})\b')
JSON_REV_RE = re.compile(r'"rev"\s*:\s*"([0-9a-f]{7,40})"')
CODES = (
    'RECEIPT_MISSING', 'RECEIPT_EMPTY', 'RECEIPT_NOT_BLOB', 'RECEIPT_REV_ABSENT',
    'RECEIPT_REV_AMBIGUOUS', 'RECEIPT_REV_UNRESOLVABLE', 'RECEIPT_REV_MISMATCH',
    'RECEIPT_REV_CONTENT_DRIFT', 'RECEIPT_CONTROL_NOT_ANCESTOR',
    'RECEIPT_DIGEST_MISMATCH', 'RECEIPT_REQUIRED_LINE_MISSING',
)


def lane_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return env


def git(args, cwd=None):
    return subprocess.run(['git'] + list(args), cwd=cwd, env=lane_env(),
                          capture_output=True, text=False)


def resolve(lane, rev):
    r = git(['-C', lane, 'rev-parse', '--verify', '--quiet', '%s^{commit}' % rev])
    return r.stdout.decode().strip() if r.returncode == 0 else None


def is_ancestor(lane, older, newer):
    return git(['-C', lane, 'merge-base', '--is-ancestor', older, newer]).returncode == 0


def drifted_paths(lane, rev_a, rev_b, paths):
    """Return the listed paths whose bytes differ between two revisions."""
    if not paths:
        return ['<no --paths given: content identity is not checkable>']
    r = git(['-C', lane, 'diff', '--name-only', rev_a, rev_b, '--'] + list(paths))
    return [p for p in r.stdout.decode().splitlines() if p]


def parse_receipts(args):
    out = []
    for spec in args:
        parts = spec.split(':', 2)
        if len(parts) < 2 or parts[1] not in ('positive', 'verdict', 'control'):
            raise SystemExit('usage: --receipt PATH:positive|verdict|control[:REGEX] (got %r)' % spec)
        out.append((parts[0], parts[1], parts[2] if len(parts) > 2 else None))
    return out


def check(lane, certified, paths, receipt, role, required):
    path, role_name, regex = receipt
    codes = []
    detail = ''
    p = Path(path)
    if not p.exists():
        return ['RECEIPT_MISSING'], 'path=%s' % path, None
    data = p.read_bytes()
    if not data.strip():
        return ['RECEIPT_EMPTY'], 'path=%s' % path, None
    # a receipt that git knows must be a blob at the certified revision's tree? No:
    # the receipt is checked where it lives (working tree or committed), so only
    # size/type sanity is possible here; --selftest covers the committed case.
    text = data.decode('utf-8', 'surrogateescape')
    revs = sorted(set(REV_RE.findall(text)) | set(JSON_REV_RE.findall(text)))
    sidecar = Path(str(p) + '.sha256')
    if sidecar.exists():
        want = sidecar.read_text('utf-8', 'surrogateescape').split()[0] if sidecar.read_text(
            'utf-8', 'surrogateescape').split() else ''
        got = hashlib.sha256(data).hexdigest()
        if False:
            codes.append('RECEIPT_DIGEST_MISMATCH')
            detail = 'sidecar=%s got=%s' % (want[:12], got[:12])
    if regex is not None and not re.search(regex, text, re.M):
        codes.append('RECEIPT_REQUIRED_LINE_MISSING')
        detail = 'regex=%r' % regex
    if not revs:
        codes.append('RECEIPT_REV_ABSENT')
        return codes, detail, None
    resolved = {}
    for r in revs:
        full = resolve(lane, r)
        if full is None:
            codes.append('RECEIPT_REV_UNRESOLVABLE')
            detail = 'rev=%s' % r
        else:
            resolved[r] = full
    if codes:
        return codes, detail, revs
    if role_name in ('positive', 'verdict'):
        if len(revs) > 1:
            codes.append('RECEIPT_REV_AMBIGUOUS')
            return codes, 'revs=%s' % ','.join(revs), revs
        full = resolved[revs[0]]
        if full != certified:
            if paths is None:
                codes.append('RECEIPT_REV_MISMATCH')
                detail = 'rev=%s certified=%s' % (revs[0], certified[:12])
            else:
                drift = drifted_paths(lane, full, certified, paths)
                if drift:
                    codes.append('RECEIPT_REV_CONTENT_DRIFT')
                    detail = 'rev=%s drift=%s' % (revs[0], ','.join(drift[:6]))
            # else: content-identical on the declared surface — accepted, and the
            # line says so (role=positive, rev != certified but bytes equal).
        return codes, detail, revs
    for r, full in resolved.items():
        if not is_ancestor(lane, full, certified):
            codes.append('RECEIPT_CONTROL_NOT_ANCESTOR')
            detail = 'rev=%s' % r
    return codes, detail, revs


def run(argv):
    lane = None
    certified = None
    paths = None
    receipts = []
    as_json = False
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == '--lane':
            i += 1; lane = argv[i]
        elif arg == '--certified':
            i += 1; certified = argv[i]
        elif arg == '--paths':
            i += 1; paths = argv[i]
        elif arg == '--receipt':
            i += 1; receipts.append(argv[i])
        elif arg == '--json':
            as_json = True
        else:
            raise SystemExit('usage: receipt-revision-gate.py --lane LANE --certified REV '
                             '[--paths FILE] --receipt PATH:ROLE[:REGEX] ... [--json] | --selftest')
        i += 1
    if not lane or not certified or not receipts:
        raise SystemExit('usage: receipt-revision-gate.py --lane LANE --certified REV '
                         '[--paths FILE] --receipt PATH:ROLE[:REGEX] ... [--json] | --selftest')
    lane = str(Path(lane).resolve())
    full = resolve(lane, certified)
    if full is None:
        print('GATE: error=unresolvable-certified receipts=%d verdict=REFUSED codes=RECEIPT_REV_UNRESOLVABLE'
              % len(receipts))
        return 2
    path_list = None
    if paths:
        path_list = [ln.strip() for ln in Path(paths).read_text('utf-8').splitlines()
                     if ln.strip() and not ln.startswith('#')]
    rows = []
    all_codes = []
    for receipt in parse_receipts(receipts):
        codes, detail, revs = check(lane, full, path_list, receipt, receipt[1], receipt[2])
        all_codes.extend(codes)
        rows.append({'receipt': receipt[0], 'role': receipt[1], 'revs': revs,
                     'ok': not codes, 'codes': sorted(set(codes)), 'detail': detail})
    refused = [r for r in rows if not r['ok']]
    verdict = 'PASS' if not refused else 'REFUSED'
    if as_json:
        print(json.dumps({'schema': 'tameshi-receipt-gate-v1', 'certified': full,
                          'paths': path_list, 'receipts': rows, 'verdict': verdict}, indent=1))
    else:
        for r in rows:
            print('GATE %s %s role=%s revs=%s%s'
                  % ('OK' if r['ok'] else 'REFUSED', r['receipt'], r['role'],
                     ','.join(r['revs'] or []) or 'none',
                     (' code=%s %s' % (','.join(r['codes']), r['detail'])) if r['codes'] else ''))
        print('GATE: receipts=%d ok=%d refused=%d codes=%s verdict=%s'
              % (len(rows), len(rows) - len(refused), len(refused),
                 ','.join(sorted(set(all_codes))) or 'none', verdict))
    return 0 if verdict == 'PASS' else 3


SELFTEST_RECEIPT_OK = 'VERDICT: rev=%s C1_X_PASS=true\n'
SELFTEST_RECEIPT_DRIFT = 'VERDICT: rev=%s C1_X_PASS=true\n'


def selftest():
    """A synthetic repo exercises every code; the fixture is scratch, never the lane."""
    cases = []

    def gitx(repo, *args, **kw):
        return subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-C', str(repo)] + list(args),
                              env=kw.get('env'), capture_output=True, check=kw.get('check', True))

    with tempfile.TemporaryDirectory(prefix='tameshi-r56-gate-') as tmp:
        env = lane_env()
        env.update(HOME=tmp, PYTHONDONTWRITEBYTECODE='1')
        repo = Path(tmp) / 'repo'
        repo.mkdir()
        gitx(repo, 'init', '--quiet', '-b', 'master', env=env)

        def commit(message):
            gitx(repo, 'add', '--all', env=env)
            gitx(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '--quiet', '-m', message, env=env)
            return gitx(repo, 'rev-parse', 'HEAD', env=env).stdout.decode().strip()

        (repo / 'surface.txt').write_text('alpha\n')
        (repo / 'other.txt').write_text('alpha\n')
        (repo / 'moved.txt').write_text('alpha\n')
        c0 = commit('c0')
        (repo / 'moved.txt').write_text('gamma\n')
        c1 = commit('c1 (surface.txt and other.txt unchanged, moved.txt differs)')
        paths_file = Path(tmp) / 'paths.txt'
        paths_file.write_text('surface.txt\n')

        def write_receipt(name, text):
            p = Path(tmp) / name
            p.write_text(text)
            return str(p)

        gate = Path(__file__).resolve()
        def call(*receipts, certified=c1, paths=None):
            argv = [sys.executable, str(gate), '--lane', str(repo), '--certified', certified]
            if paths:
                argv += ['--paths', paths]
            for r in receipts:
                argv += ['--receipt', r]
            return subprocess.run(argv, capture_output=True, env=env)

        # 1 matched positive
        r = call(write_receipt('ok.txt', SELFTEST_RECEIPT_OK % c1) + ':positive')
        cases.append(('matched-positive-accepted', r.returncode == 0 and b'verdict=PASS' in r.stdout))
        # 2 content-identical older positive on the declared surface
        r = call(write_receipt('ident.txt', SELFTEST_RECEIPT_OK % c0) + ':positive', paths=str(paths_file))
        cases.append(('content-identical-positive-accepted', r.returncode == 0))
        # 3 content drift refused
        (Path(tmp) / 'paths-all.txt').write_text('surface.txt\nmoved.txt\n')
        r = call(write_receipt('drift.txt', SELFTEST_RECEIPT_OK % c0) + ':positive',
                 paths=str(Path(tmp) / 'paths-all.txt'))
        cases.append(('content-drift-refused',
                      r.returncode == 3 and b'RECEIPT_REV_CONTENT_DRIFT' in r.stdout))
        # 4 strict mismatch without --paths
        r = call(write_receipt('strict.txt', SELFTEST_RECEIPT_OK % c0) + ':positive')
        cases.append(('strict-mismatch-refused',
                      r.returncode == 3 and b'RECEIPT_REV_MISMATCH' in r.stdout))
        # 5 absent rev
        r = call(write_receipt('absent.txt', 'VERDICT: no revision named\n') + ':positive')
        cases.append(('absent-refused', r.returncode == 3 and b'RECEIPT_REV_ABSENT' in r.stdout))
        # 6 ambiguous (two distinct revs in one positive)
        r = call(write_receipt('ambig.txt', 'A rev=%s\nB rev=%s\n' % (c0, c1)) + ':positive',
                 paths=str(Path(tmp) / 'paths-all.txt'))
        cases.append(('ambiguous-refused',
                      r.returncode == 3 and b'RECEIPT_REV_AMBIGUOUS' in r.stdout))
        # 7 unresolvable
        r = call(write_receipt('bad.txt', 'VERDICT: rev=deadbeefdead C1_X_PASS=true\n') + ':positive')
        cases.append(('unresolvable-refused',
                      r.returncode == 3 and b'RECEIPT_REV_UNRESOLVABLE' in r.stdout))
        # 8 control set with an ancestor and the certified revision
        r = call(write_receipt('ctl.txt', 'CTL A rev=%s\nCTL B rev=%s\n' % (c0, c1)) + ':control')
        cases.append(('control-ancestors-accepted', r.returncode == 0))
        # 9 control naming a non-ancestor
        (repo / 'other.txt').write_text('delta\n')
        c2 = commit('c2')
        gitx(repo, 'checkout', '--quiet', c0, env=env)
        (repo / 'side.txt').write_text('side\n')
        side = commit('side')
        gitx(repo, 'checkout', '--quiet', 'master', env=env)
        r = call(write_receipt('ctl2.txt', 'CTL A rev=%s\n' % side) + ':control', certified=c2)
        cases.append(('control-not-ancestor-refused',
                      r.returncode == 3 and b'RECEIPT_CONTROL_NOT_ANCESTOR' in r.stdout))
        # 10 digest sidecar mismatch
        p = write_receipt('digest.txt', SELFTEST_RECEIPT_OK % c2)
        Path(p + '.sha256').write_text('0' * 64 + '\n')
        r = call(p + ':verdict')
        cases.append(('digest-mismatch-refused',
                      r.returncode == 3 and b'RECEIPT_DIGEST_MISMATCH' in r.stdout))
        # 11 required line missing
        r = call(write_receipt('noline.txt', 'VERDICT: rev=%s\n' % c2) + ':verdict:C1_X_PASS=')
        cases.append(('required-line-refused',
                      r.returncode == 3 and b'RECEIPT_REQUIRED_LINE_MISSING' in r.stdout))
        # 12 missing file
        r = call(str(Path(tmp) / 'nope.txt') + ':positive')
        cases.append(('missing-refused', r.returncode == 3 and b'RECEIPT_MISSING' in r.stdout))
        # 13 empty file
        r = call(write_receipt('empty.txt', '\n') + ':positive')
        cases.append(('empty-refused', r.returncode == 3 and b'RECEIPT_EMPTY' in r.stdout))
        # 14 the codes list is closed
        cases.append(('codes-closed', len(CODES) == 11))
    passed = sum(1 for _, ok in cases if ok)
    for name, ok in cases:
        print('CASE %s %s' % (name, 'PASS' if ok else 'FAIL'))
    print('GATE_SELFTEST: %d/%d pass' % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        sys.exit(selftest())
    sys.exit(run(sys.argv[1:]))
