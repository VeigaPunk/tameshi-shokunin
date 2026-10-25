#!/usr/bin/env python3
"""Round-46 do-nothing / cheapest-cheat controls, scored by the FROZEN counters on scratch repos.

Run from the lane repo root (working tree files are copied into throwaway git repos created with
`git init` in a mktemp dir; every git call names -C; nothing is committed in the lane).

  CTL_A  C3 package entries copied byte-exact (rows with lane snapshots added)      -> entries=0
  CTL_B  C3 relabel: package entries with only the header rewritten (ids, verified-at) -> entries=0
  CTL_C  C3 rows only, no entries                                                     -> entries=0
  CTL_D  C3 rows with a wrong snapshot digest and entries rewritten                   -> rows=0
  CTL_E  C2 selftest that pins its own bytes (kills every mutant, neutral ones too)   -> neutral_killed>0, PASS false
  CTL_F  C2 selftest that always fails                                                -> pristine=0, PASS false
  CTL_G  C2 unchanged round-45 counters (the do-nothing baseline)                     -> killed=0, PASS false
Each control prints the counter's final line.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1')
C3 = '.ufo/evidence/round-46/coverage/measure.py'
C2 = '.ufo/evidence/round-46/hardening/mutate.py'
SNAP = '.ufo/evidence/round-46/coverage/sources/'
PKG = '.ufo/evidence/round-46/assimilation/package/'
DOCS = [
    ('S258', 'arxiv-2504.16777-abs.html', 'https://arxiv.org/abs/2504.16777', 'r6-flaky-failures-cluster.md'),
    ('S259', 'tum-portal-flaky-failures.html',
     'https://portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures/',
     'r5-undetected-flaky-failures.md'),
    ('S260', 'google-flaky-feed-6277555988217606236.json',
     'https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json', 'r9-false-red-rate.md'),
]


def git(d, *a):
    return subprocess.run(['git', '-C', d, *a], env=ENV, capture_output=True, check=True)


def scratch():
    d = tempfile.mkdtemp(prefix='tameshi-r46-ctl-')
    git(d, 'init', '-q', '-b', 'm')
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], env=ENV, capture_output=True).stdout.decode().strip()
    assert top == os.path.realpath(d), (top, d)
    return d


def copy(d, rel, data=None):
    dst = os.path.join(d, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if data is None:
        shutil.copyfile(os.path.join(LANE, rel), dst)
    else:
        with open(dst, 'wb') as fh:
            fh.write(data if isinstance(data, bytes) else data.encode())


def commit(d):
    git(d, 'add', '-A')
    git(d, '-c', 'user.name=ctl', '-c', 'user.email=ctl@ctl', 'commit', '-qm', 'ctl')


def last(cmd):
    out = subprocess.run(cmd, env=ENV, capture_output=True, text=True)
    lines = [l for l in out.stdout.strip().splitlines() if l]
    return (lines[-1] if lines else 'NO-OUTPUT ' + out.stderr[-200:]), out.returncode


def c3_repo(entries, wrong_digest=False, rows=True):
    d = scratch()
    copy(d, C3)
    reg = ''
    for sid, snap, url, pkg in DOCS:
        copy(d, SNAP + snap)
        copy(d, PKG + pkg)
        digest = hashlib.sha256(open(os.path.join(LANE, SNAP + snap), 'rb').read()).hexdigest()[:8]
        if wrong_digest:
            digest = 'deadbeef'
        used = 'corpus/knowledge/%s' % pkg
        reg += ('| %s | t — %s | paper | A | s | %s%s %s | t | mined | 2026-10-25 | 365d | %s |\n'
                % (sid, url, SNAP, snap, digest, used))
    copy(d, 'corpus/SOURCES.md', reg if rows else '')
    readme = ''
    for sid, snap, url, pkg in DOCS:
        text = entries(sid, pkg)
        if text is not None:
            copy(d, 'corpus/knowledge/%s' % pkg, text)
            readme += '`corpus/knowledge/%s`\n' % pkg
    copy(d, 'corpus/README.md', readme)
    commit(d)
    return d


def package_text(pkg):
    return open(os.path.join(LANE, PKG + pkg), encoding='utf-8').read()


def relabel(sid, pkg):
    body = package_text(pkg).lstrip('\n').split('\n')
    head = ['source: %s — relabelled package entry' % sid, 'verified-at: 2026-10-25', 'recheck: 365d']
    return '\n'.join(head + body[3:]) + '\n'


def run_c3(name, d):
    line, rc = last([sys.executable, os.path.join(d, C3), '--lane', d, '--rev', 'HEAD'])
    print('%s rc=%d %s' % (name, rc, line))


def run_c2(name, d, targets='hardened'):
    line, rc = last([sys.executable, os.path.join(d, C2), '--lane', d, '--rev', 'HEAD', '--targets', targets])
    print('%s rc=%d %s' % (name, rc, line))


def c2_repo(fresh_src, cover_src):
    d = scratch()
    copy(d, C2)
    copy(d, '.ufo/evidence/round-46/hardening/mutants.json')
    copy(d, '.ufo/evidence/round-45/freshness/measure.py')
    copy(d, '.ufo/evidence/round-45/coverage/measure.py')
    copy(d, '.ufo/evidence/round-46/hardening/freshness-counter.py', fresh_src)
    copy(d, '.ufo/evidence/round-46/hardening/coverage-counter.py', cover_src)
    commit(d)
    return d


def main():
    run_c3('CTL_A_package_byte_exact', c3_repo(lambda sid, pkg: package_text(pkg)))
    run_c3('CTL_B_relabel_header_only', c3_repo(relabel))
    run_c3('CTL_C_rows_only', c3_repo(lambda sid, pkg: None))
    run_c3('CTL_D_wrong_digest', c3_repo(relabel, wrong_digest=True))
    fresh = open(os.path.join(LANE, '.ufo/evidence/round-45/freshness/measure.py'), 'rb').read().decode()
    cover = open(os.path.join(LANE, '.ufo/evidence/round-45/coverage/measure.py'), 'rb').read().decode()

    def pin_cheat(src):
        # the selftest pins the byte length of its own file (fixed-width placeholder, so no circularity)
        cheat = ("    if len(open(__file__, 'rb').read()) != int('{LEN}'):\n"
                 "        print('VERDICT: FAIL')\n        return 1\n")
        final = src.replace('def selftest():\n', 'def selftest():\n' + cheat, 1).replace('{LEN}', '00000000')
        return final.replace('00000000', '%08d' % len(final.encode()))

    def always_fail(src):
        return src.replace('def selftest():\n', "def selftest():\n    print('VERDICT: FAIL')\n    return 1\n", 1)

    run_c2('CTL_E_selftest_pins_own_bytes', c2_repo(pin_cheat(fresh), pin_cheat(cover)))
    run_c2('CTL_F_selftest_always_fails', c2_repo(always_fail(fresh), always_fail(cover)))
    run_c2('CTL_G_round45_counters_unchanged', c2_repo(fresh, cover), targets='orig')


if __name__ == '__main__':
    main()
