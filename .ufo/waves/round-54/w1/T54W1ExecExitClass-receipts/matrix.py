#!/usr/bin/env python3
"""Differential exit-class matrix: base d33053f vs C0 59c3810, four tools.

Every invocation runs in the same clone, same cwd, same argv, and differs only in
the TMPDIR state. Prints one TSV row per (tool, arm, tmpdir, rev) plus a
COMPARE line stating whether base and C0 agree.
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r54/T54W1ExecExitClass')
REVS = {'base': S / 'base', 'c0': S / 'c0'}
USE = S / 'tmp-use'
MISSING = S / 'tmp-missing'          # never created
CONTRACT = S / 'contract.json'
TIMEOUT = 1800

# evidence copy for the witness FAIL arm, made once from the base clone
WITNESS_EVIDENCE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-12/BashWitness')


def env_for(tmpdir):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['TMPDIR'] = tmpdir
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return env


def run(clone, argv, tmpdir, out_tag=None):
    proc = subprocess.run([sys.executable] + argv, cwd=str(clone), env=env_for(tmpdir),
                          capture_output=True, text=True, timeout=TIMEOUT)
    text = proc.stdout + proc.stderr
    lines = [l for l in text.strip().splitlines() if l.strip()]
    tb = 'Traceback (most recent call last)' in text
    return proc.returncode, (lines[-1][:160] if lines else ''), tb, proc.stdout, proc.stderr


def arms(clone):
    """(arm name, argv, tmpdir string, extra setup)"""
    od = str(S / ('out-%s.json' % clone.name))
    tam = S / ('tamper-witness-%s' % clone.name)
    return [
        ('selftest-usable',        ['tools/env-diff.py', '--selftest'], str(USE)),
        ('selftest-empty',         ['tools/env-diff.py', '--selftest'], ''),
        ('selftest-unusable',      ['tools/env-diff.py', '--selftest'], str(MISSING)),
        ('usage-missing-out',      ['tools/env-diff.py', '--contract', str(CONTRACT)], str(USE)),
        ('usage-unknown-flag',     ['tools/env-diff.py', '--bogus'], str(USE)),
        ('help',                   ['tools/env-diff.py', '--help'], str(USE)),
        ('setup-missing-contract', ['tools/env-diff.py', '--contract', '/nonexistent/c.json', '--out', od], str(USE)),
        ('fail-unavailable-surface', ['tools/env-diff.py', '--contract', str(CONTRACT), '--out', od,
                                      '--fleet-root', str(clone)], str(USE)),
        ('runpath-unusable',       ['tools/env-diff.py', '--contract', str(CONTRACT), '--out', od,
                                     '--fleet-root', str(clone)], str(MISSING)),
        ('--SEP--', [], ''),
        ('selftest-usable',        ['tools/bash-witness-study.py', 'selftest'], str(USE)),
        ('selftest-empty',         ['tools/bash-witness-study.py', 'selftest'], ''),
        ('selftest-unusable',      ['tools/bash-witness-study.py', 'selftest'], str(MISSING)),
        ('usage-no-args',          ['tools/bash-witness-study.py'], str(USE)),
        ('usage-unknown-mode',     ['tools/bash-witness-study.py', 'bogusmode'], str(USE)),
        ('help',                   ['tools/bash-witness-study.py', '--help'], str(USE)),
        ('check-default-evidence', ['tools/bash-witness-study.py', 'check'], str(USE)),
        ('setup-missing-evidence', ['tools/bash-witness-study.py', 'count', '--evidence', '/nonexistent/BW'], str(USE)),
        ('fail-tampered-evidence', ['tools/bash-witness-study.py', 'check', '--evidence', str(tam)], str(USE)),
        ('--SEP--', [], ''),
        ('selftest-usable',        ['tools/evidence-disposition.py', '--selftest'], str(USE)),
        ('selftest-empty',         ['tools/evidence-disposition.py', '--selftest'], ''),
        ('selftest-unusable',      ['tools/evidence-disposition.py', '--selftest'], str(MISSING)),
        ('usage-no-args',          ['tools/evidence-disposition.py'], str(USE)),
        ('usage-unknown-flag',     ['tools/evidence-disposition.py', '--bogus'], str(USE)),
        ('usage-selftest-extra',   ['tools/evidence-disposition.py', '--selftest', '--json'], str(USE)),
        ('help',                   ['tools/evidence-disposition.py', '--help'], str(USE)),
        ('setup-missing-inputs',   ['tools/evidence-disposition.py', '--root', '/nonexistent',
                                     '--dispositions', '/nonexistent/d.json'], str(USE)),
        ('--SEP--', [], ''),
        ('selftest-usable',        ['tools/pin-disposition.py', '--selftest'], str(USE)),
        ('selftest-empty',         ['tools/pin-disposition.py', '--selftest'], ''),
        ('selftest-unusable',      ['tools/pin-disposition.py', '--selftest'], str(MISSING)),
        ('usage-no-args',          ['tools/pin-disposition.py'], str(USE)),
        ('usage-unknown-flag',     ['tools/pin-disposition.py', '--bogus'], str(USE)),
        ('usage-selftest-extra',   ['tools/pin-disposition.py', '--selftest', '--manifest', 'x'], str(USE)),
        ('help',                   ['tools/pin-disposition.py', '--help'], str(USE)),
        ('setup-missing-manifest', ['tools/pin-disposition.py', '--manifest', '/nonexistent/m.json',
                                     '--root', '/nonexistent'], str(USE)),
    ]


def make_tamper_copy():
    for name in ('tamper-witness-base', 'tamper-witness-c0'):
        if (S / name).exists():
            shutil.rmtree(S / name)
    if not WITNESS_EVIDENCE.is_dir():
        return False
    for name in ('tamper-witness-base', 'tamper-witness-c0'):
        dst = S / name
        shutil.copytree(WITNESS_EVIDENCE, dst)
        # flip one byte of the declared mapping: a committed file's digest no longer matches
        p = dst / 'declared.tsv'
        data = p.read_bytes()
        p.write_bytes(data.replace(b'B1', b'B0', 1) if b'B1' in data else data + b'#tampered\n')
    return True


def main():
    tampered = make_tamper_copy()
    rows = []
    streams = {}
    snap = S / 'streams'
    snap.mkdir(exist_ok=True)
    for rev, clone in REVS.items():
        for arm, argv, td in arms(clone):
            if arm == '--SEP--':
                rows.append((rev, clone.name, '---', '---', '---', ''))
                continue
            if arm == 'fail-tampered-evidence' and not tampered:
                rows.append((rev, clone.name, arm, 'SKIP', 'no-fixture', ''))
                continue
            out = run(clone, argv, td)
            tool = argv[0]
            streams[(tool, arm, clone.name)] = (out[3], out[4])
            tag = '%s--%s--%s' % (clone.name, Path(tool).stem, arm)
            (snap / (tag + '.stdout')).write_text(out[3])
            (snap / (tag + '.stderr')).write_text(out[4])
            rows.append((rev, tool, arm, out[0], 'tb' if out[2] else '-', out[1]))
    print('REV\tTOOL\tARM\tRC\tTRACEBACK\tLAST_LINE')
    for r in rows:
        print('\t'.join(str(x) for x in r))
    # comparison
    print()
    by = {}
    for rev, tool, arm, rc, tb, last in rows:
        by.setdefault((tool, arm), {})[rev] = (rc, tb, last)
    bad = 0
    for (tool, arm), d in by.items():
        if arm == '---':
            continue
        b, c = d.get('base'), d.get('c0')
        if b is None or c is None:
            continue
        if arm == 'selftest-unusable':
            ok = b[0] == 1 and b[1] == 'tb' and c[0] == 2 and c[1] == '-' and 'could-not-evaluate' in c[2]
            print('INTENDED\t%s\t%s\tbase=%s(%s)\tc0=%s(%s)\t%s'
                  % (tool, arm, b[0], b[1], c[0], c[1], 'OK' if ok else 'MISMATCH'))
            if not ok:
                bad += 1
            continue
        ok = b[0] == c[0]
        print('COMPARE\t%s\t%s\tbase=%s(%s)\tc0=%s(%s)\t%s'
              % (tool, arm, b[0], b[1], c[0], c[1], 'SAME' if ok else 'DIFF'))
        if not ok:
            bad += 1
    # every arm except the intended one must emit the same streams once the
    # clone path, my own out-file name, the tool's self-digest and the source
    # line numbers (which the added wrapper lines legitimately shift) are folded
    def norm(rev, text):
        text = text.replace(str(S / rev), 'CLONE')
        text = text.replace('T54W1ExecExitClass/' + rev, 'SCRATCH')
        text = text.replace('out-%s.json' % rev, 'OUT')
        text = text.replace('tamper-witness-%s' % rev, 'TAMPER')
        text = re.sub(r'[0-9a-f]{64}', 'SHA256', text)
        text = re.sub(r'line \d+, in', 'line N, in', text)
        return text

    print()
    for (tool, arm, rev) in sorted(streams):
        if rev != 'base':
            continue
        if arm == 'selftest-unusable':
            continue
        c = streams.get((tool, arm, 'c0'))
        if c is None:
            continue
        raw = streams[(tool, arm, 'base')]
        same_raw = raw == c
        same_norm = (norm('base', raw[0]), norm('base', raw[1])) == (norm('c0', c[0]), norm('c0', c[1]))
        print('STREAMS\t%s\t%s\traw=%s\tnormalized=%s'
              % (tool, arm, 'IDENTICAL' if same_raw else 'DIFF',
                 'IDENTICAL' if same_norm else 'DIFF'))
        if not same_norm:
            bad += 1
    print('MATRIX: %d rows, %d disagreements' % (len(rows), bad))
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
