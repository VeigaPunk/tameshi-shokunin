#!/usr/bin/env python3
"""ControlThreats round-12 evidence probes (critic seat; NOT the C1 gate).

Models only the raw facts the C1 contract compares (exit, stdout bytes, stderr
bytes per run). It never classifies with the gate's finding IDs and is not an
implementation of tools/repeat-control.py. Output: one PROBE line per fact.
Usage: python3 probes.py [--legs FLEET_ROOT]
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile


def run(argv, env=None, cwd=None, timeout=300):
    p = subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True,
                       env=env, cwd=cwd, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def triple(argv, **kw):
    return [run(argv, **kw) for _ in range(3)]


def all_same(t):
    return t[0] == t[1] == t[2]


def say(k, v):
    print('PROBE %s: %s' % (k, v), flush=True)


def p1_flake_admission(trials=300, p=0.1):
    # A control that fails 10% of runs at random. The contract's clean outcome
    # needs three identical runs with exit 0; count how often that happens.
    cmd = [sys.executable, '-c',
           'import random,sys; sys.exit(1 if random.random() < %r else 0)' % p]
    clean = sum(1 for _ in range(trials)
                if [r[0] for r in triple(cmd)] == [0, 0, 0])
    say('P1-flake10-all-zero-triples', '%d/%d measured; model (1-p)^3=%.3f'
        % (clean, trials, (1 - p) ** 3))


def p2_time_dependent(trials=50):
    # Output is a function of wall-clock seconds; back-to-back runs usually
    # land in the same second, so bytes agree although output is time-dependent.
    same = sum(1 for _ in range(trials) if all_same(triple(['date', '+%s'])))
    say('P2-date-epoch-seconds-identical-triples', '%d/%d' % (same, trials))
    same = sum(1 for _ in range(trials) if all_same(triple(['date', '+%N'])))
    say('P2-date-nanoseconds-identical-triples', '%d/%d' % (same, trials))


def p3_text_mode_normalization():
    # Python text-mode capture applies universal newlines: CRLF and LF compare
    # equal after decode, different as bytes.
    a = subprocess.run(['printf', 'a\\r\\n'], capture_output=True, text=True).stdout
    b = subprocess.run(['printf', 'a\\n'], capture_output=True, text=True).stdout
    ab = subprocess.run(['printf', 'a\\r\\n'], capture_output=True).stdout
    bb = subprocess.run(['printf', 'a\\n'], capture_output=True).stdout
    say('P3-text-mode-crlf-equals-lf', a == b)
    say('P3-bytes-mode-crlf-equals-lf', ab == bb)
    say('P3-strip-hides-trailing-newline', b'a' == b'a\n'.strip())


def p4_spawn_failures(tmp):
    noexec = os.path.join(tmp, 'noexec.sh')
    with open(noexec, 'w') as fh:
        fh.write('#!/bin/sh\nexit 0\n')
    os.chmod(noexec, 0o644)
    noshebang = os.path.join(tmp, 'noshebang')
    with open(noshebang, 'w') as fh:
        fh.write('exit 0\n')
    os.chmod(noshebang, 0o755)
    for name, argv in [('missing', [os.path.join(tmp, 'nope')]),
                       ('not-executable', [noexec]),
                       ('no-shebang-exec-format', [noshebang]),
                       ('directory', [tmp])]:
        try:
            rc = run(argv)[0]
            say('P4-spawn-' + name, 'spawned exit=%d' % rc)
        except OSError as e:
            say('P4-spawn-' + name, '%s errno=%s' % (type(e).__name__, e.errno))
    for name, argv in [('bash-c-missing', ['bash', '-c', 'nope-cmd-r12']),
                       ('bash-c-noexec', ['bash', '-c', noexec])]:
        say('P4-wrapped-' + name, 'spawned exit=%d' % run(argv)[0])


def p5_signal_and_exit_truncation():
    say('P5-sigkill-returncode', run(['bash', '-c', 'kill -9 $$'])[0])
    say('P5-exit-256-returncode', run(['bash', '-c', 'exit 256'])[0])


def p6_cross_run_state(tmp):
    # Runs share filesystem state: the first run differs from later runs.
    marker = os.path.join(tmp, 'warm')
    cmd = ['bash', '-c', '[ -e "$1" ] && echo warm || { : > "$1"; echo cold; exit 1; }',
           '_', marker]
    t = triple(cmd)
    say('P6-cold-first-run-exits', [r[0] for r in t])
    say('P6-cold-first-run-stdout', [r[1] for r in t])
    t = triple(cmd)
    say('P6-second-invocation-warm-triple-identical', all_same(t)
        and t[0][0] == 0)


def p7_stdin_inheritance():
    # Gate must pass DEVNULL; inherited stdin changes `cat` output.
    inh = subprocess.run(['cat'], input=b'payload', capture_output=True).stdout
    dn = run(['cat'])[1]
    say('P7-cat-inherited-stdin-stdout', inh)
    say('P7-cat-devnull-stdout', dn)


def p8_merged_vs_split(tmp):
    # Runner control merges 2>&1 (mutate-and-run.sh:395); interleaving order of
    # a merged stream is a different observable than split streams.
    cmd = ['bash', '-c', 'echo out; echo err >&2; echo out2']
    split = run(cmd)
    merged = run(['bash', '-c', '{ echo out; echo err >&2; echo out2; } 2>&1'])
    say('P8-split-stdout', split[1])
    say('P8-split-stderr', split[2])
    say('P8-merged', merged[1])


def p9_legs(fleet):
    legs = [
        ('js-kimi-census', 'kumitate-shokunin', 'scripts/kimi-census.mjs',
         '175de6ba2e9e904010411b19cab27e0af9aad3d4',
         '83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426',
         'node "$MUTANT" --selftest'),
        ('bash-surface-census', 'kagi-shokunin', 'corpus/surface-census.sh',
         'fecee8743e52eb8fb5fbb40782934cb619a1a96e',
         '275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f',
         'bash "$MUTANT" --selftest'),
        ('bash-tsukuroi-census', 'tsukuroi-shokunin', 'tools/tsukuroi-census.sh',
         '165307fe4746a8807b02ec4a7d7ecac0368454a6',
         '084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5',
         'bash "$MUTANT" --selftest'),
        ('bash-mado-verify', 'mado-shokunin', 'tools/mado-verify.sh',
         'eead56b20ad2b28299ae4fa623d52a99b44c743c',
         'd7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13',
         'bash "$MUTANT" --selftest'),
        ('bash-checklist-run', 'kagi-shokunin', 'corpus/checklist-run.sh',
         'fecee8743e52eb8fb5fbb40782934cb619a1a96e',
         '7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf',
         'bash "$MUTANT" --selftest'),
        ('js-claims-check', 'kumitate-shokunin', 'scripts/claims-check.mjs',
         '175de6ba2e9e904010411b19cab27e0af9aad3d4',
         'e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b',
         'node "$MUTANT" --selftest'),
    ]
    for name, repo, path, rev, pin, suite in legs:
        blob = subprocess.run(['git', '-C', os.path.join(fleet, repo), 'show',
                               '%s:%s' % (rev, path)], capture_output=True)
        if blob.returncode != 0:
            say('P9-%s' % name, 'blob unavailable')
            continue
        sha = hashlib.sha256(blob.stdout).hexdigest()
        if sha != pin:
            say('P9-%s' % name, 'pin mismatch %s' % sha)
            continue
        wd = tempfile.mkdtemp(prefix='tameshi-r12-ct-%s.' % name)
        mut = os.path.join(wd, 'pristine.' + os.path.basename(path))
        with open(mut, 'wb') as fh:
            fh.write(blob.stdout)
        env = dict(os.environ, MUTANT=mut, PRISTINE=mut, WORKDIR=wd,
                   DEFECT_ID='CONTROL')
        t = triple(['bash', '-c', suite], env=env, cwd=os.getcwd())
        diffs = []
        for i in (1, 2):
            for k, lab in ((0, 'exit'), (1, 'stdout'), (2, 'stderr')):
                if t[i][k] != t[0][k]:
                    diffs.append('run%d.%s' % (i + 1, lab))
        say('P9-%s' % name, 'pin-ok exits=%s stdout-sha=%s stderr-bytes=%s diffs=%s'
            % ([r[0] for r in t],
               [hashlib.sha256(r[1]).hexdigest()[:12] for r in t],
               [len(r[2]) for r in t], diffs or 'none'))
        if diffs:
            # keep the first differing pair for inspection
            for i in (1, 2):
                for k, lab in ((1, 'stdout'), (2, 'stderr')):
                    if t[i][k] != t[0][k]:
                        a, b = t[0][k].splitlines(), t[i][k].splitlines()
                        for j, (x, y) in enumerate(zip(a, b)):
                            if x != y:
                                say('P9-%s-first-diff' % name, 'run1 vs run%d %s line %d: %r != %r'
                                    % (i + 1, lab, j + 1, x[:160], y[:160]))
                                break
                        else:
                            say('P9-%s-first-diff' % name, 'run1 vs run%d %s length %d != %d lines'
                                % (i + 1, lab, len(a), len(b)))
        shutil.rmtree(wd, ignore_errors=True)


def main():
    tmp = tempfile.mkdtemp(prefix='tameshi-r12-ct.')
    try:
        p3_text_mode_normalization()
        p4_spawn_failures(tmp)
        p5_signal_and_exit_truncation()
        p6_cross_run_state(tmp)
        p7_stdin_inheritance()
        p8_merged_vs_split(tmp)
        p2_time_dependent()
        p1_flake_admission()
        if len(sys.argv) == 3 and sys.argv[1] == '--legs':
            p9_legs(sys.argv[2])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
