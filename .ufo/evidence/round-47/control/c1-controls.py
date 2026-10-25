#!/usr/bin/env python3
"""Round-47 C1 controls on a scratch clone (several minutes: each --emit/deciding run observes 22 statements
under six profiles).

  CTL_I  the unchanged tree (no deps clause on any standing row)                                 -> unparsed>0, PASS false
  CTL_J  the cheapest pass attempt: every standing row restated with the right value, exit and
         sha but `deps none` everywhere                                                          -> dep_mismatch>0, PASS false
  CTL_K  positive control: the rows restated with the OBSERVED dependences                        -> total=0, PASS true

Usage: c1-controls.py [LANE] [--emit-from FILE]. `--emit-from` reuses a committed `--emit` output of the same counter instead of
re-running it (CTL_I then reads that file's final C1_R47 line: it was an unchanged-tree run). The scratch clone is `git clone` of LANE (default: the lane two levels up) into a
mktemp dir; every git call names -C; the toplevel is verified before the first commit; nothing is committed in LANE.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

ARGS = [a for a in sys.argv[1:]]
EMIT_FROM = ARGS[ARGS.index('--emit-from') + 1] if '--emit-from' in ARGS else None
POS = [a for i, a in enumerate(ARGS) if not a.startswith('--') and (i == 0 or ARGS[i - 1] != '--emit-from')]
LANE = os.path.abspath(POS[0]) if POS else os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1')
E = '.ufo/evidence/round-47'
C1 = E + '/calibration/measure.py'
FILES = [C1, E + '/calibration/statements.json']
CAP_HDR = '\n\n| Capability | What it can now do | Evidence pointer | First-working round |\n|---|---|---|---|\n'
AXIS_HDR = '\n\n| Axis | Score (0\u201310) | Evidence / counting rule | Measured commit | Last-change round |\n|---|---|---|---|---|\n'


def git(d, *a):
    return subprocess.run(['git', '-C', d, *a], env=ENV, capture_output=True, check=True)


def scratch():
    d = tempfile.mkdtemp(prefix='tameshi-r47-c1ctl-')
    subprocess.run(['git', 'clone', '-q', '--no-hardlinks', LANE, d], env=ENV, capture_output=True, check=True)
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], env=ENV, capture_output=True).stdout.decode().strip()
    assert top == os.path.realpath(d), (top, d)
    for rel in FILES:
        dst = os.path.join(d, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(os.path.join(LANE, rel), dst)
    return d


def commit(d, msg):
    git(d, 'add', '-A')
    git(d, '-c', 'user.name=ctl', '-c', 'user.email=ctl@ctl', 'commit', '-qm', msg)
    return subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], env=ENV, capture_output=True, text=True).stdout.strip()


def run(d, rev, base, work, emit=False):
    cmd = [sys.executable, os.path.join(d, C1), '--lane', d, '--rev', rev, '--base', base, '--work', work]
    if emit:
        cmd.append('--emit')
    out = subprocess.run(cmd, env=ENV, capture_output=True, text=True)
    return out.stdout, out.returncode


def final(out):
    lines = [l for l in out.splitlines() if l.startswith('C1_R47:')]
    return lines[-1] if lines else 'NO-C1-LINE'


def tables(emit_out, none_deps):
    caps, axes = [], []
    for line in emit_out.splitlines():
        if line.startswith('EMIT_CAP | '):
            row = line[len('EMIT_CAP '):]
        elif line.startswith('EMIT_AXIS | '):
            row = line[len('EMIT_AXIS '):]
        else:
            continue
        if none_deps:
            row = re.sub(r"deps `[a-z,-]+`", "deps `none`", row)
        (caps if line.startswith('EMIT_CAP') else axes).append(row)
    return CAP_HDR + '\n'.join(caps) + '\n' + AXIS_HDR + '\n'.join(axes) + '\n'


def main():
    if EMIT_FROM:
        emit_out = open(EMIT_FROM, encoding='utf-8').read()
        print('CTL_I_unchanged_tree (from %s) %s' % (os.path.basename(EMIT_FROM), final(emit_out)))
    else:
        d = scratch()
        base = commit(d, 'ctl base')
        emit_out, rc = run(d, base, base, os.path.join(d, '.work1'), emit=True)
        print('CTL_I_unchanged_tree rc=%d %s' % (rc, final(emit_out)))
    import concurrent.futures
    jobs = []
    def variant(none_deps, name):
        d2 = scratch()
        base2 = commit(d2, 'ctl base')
        text = open(os.path.join(d2, 'SCORECARD.md'), encoding='utf-8').read() + tables(emit_out, none_deps)
        with open(os.path.join(d2, 'SCORECARD.md'), 'w', encoding='utf-8') as fh:
            fh.write(text)
        rev = commit(d2, 'ctl rows')
        out2, rc2 = run(d2, rev, base2, os.path.join(d2, '.work'))
        lines = ['%s rc=%d %s' % (name, rc2, final(out2))]
        for l in out2.splitlines():
            if l.startswith('STATEMENT') and ('DEPS-MISMATCH' in l or 'UNPARSED' in l or ' MISMATCH ' in l):
                lines.append('  ' + l[:300])
        return lines

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futs = [pool.submit(variant, True, 'CTL_J_all_rows_deps_none'), pool.submit(variant, False, 'CTL_K_observed_deps_positive_control')]
        for f in futs:
            print('\n'.join(f.result()))


if __name__ == '__main__':
    main()
