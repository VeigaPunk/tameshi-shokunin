#!/usr/bin/env python3
"""Independent behavioural consequence probe for the 8 C0 gate mutants.

For each mutant the probe builds ONE fixture repo, writes the receipt that the
mutant's target behaviour governs, and runs the pristine gate and the mutated
gate on the SAME inputs.  The claim a mutant makes is: the pristine gate refuses
(named code, exit 3) and the mutant accepts (exit 0) — i.e. the mutant really
removes a protection, it is not a cosmetic edit.

Read-only against the lane; all fixtures live in the scratch tree.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r56/T56W2MutGateOnC0')
LANE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
C0 = 'c0137451f5b7f22d65f748fc69f1b181f55e1378'
GATE_REL = 'tools/receipt-revision-gate.py'

MUT = json.loads((S / 'mutants.json').read_text())['mutants']

PRISTINE = S / 'pristine-gate.py'
PRISTINE.write_bytes((LANE / GATE_REL).read_bytes())


def gitx(repo, *args):
    env = dict(os.environ)
    env.update(HOME=str(repo), GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-C', str(repo)] + list(args),
                          capture_output=True, text=True, check=True, env=env)


def build_fixture(tmp):
    repo = Path(tmp) / 'repo'
    repo.mkdir()
    gitx(repo, 'init', '--quiet', '-b', 'master')
    (repo / 'surface.txt').write_text('alpha\n')
    (repo / 'moved.txt').write_text('alpha\n')
    gitx(repo, 'add', '--all')
    gitx(repo, '-c', 'user.name=f', '-c', 'user.email=f@example.invalid',
         'commit', '--quiet', '-m', 'c0')
    c0 = gitx(repo, 'rev-parse', 'HEAD').stdout.strip()
    (repo / 'moved.txt').write_text('gamma\n')
    gitx(repo, 'add', '--all')
    gitx(repo, '-c', 'user.name=f', '-c', 'user.email=f@example.invalid',
         'commit', '--quiet', '-m', 'c1')
    c1 = gitx(repo, 'rev-parse', 'HEAD').stdout.strip()
    # a side branch commit that is NOT an ancestor of c1
    gitx(repo, 'checkout', '--quiet', c0)
    (repo / 'side.txt').write_text('side\n')
    gitx(repo, 'add', '--all')
    gitx(repo, '-c', 'user.name=f', '-c', 'user.email=f@example.invalid',
         'commit', '--quiet', '-m', 'side')
    side = gitx(repo, 'rev-parse', 'HEAD').stdout.strip()
    gitx(repo, 'checkout', '--quiet', 'master')
    paths_all = Path(tmp) / 'paths-all.txt'
    paths_all.write_text('surface.txt\nmoved.txt\n')
    paths_one = Path(tmp) / 'paths-one.txt'
    paths_one.write_text('surface.txt\n')
    return repo, c0, c1, side, paths_all, paths_one


def gate_run(gate, repo, certified, receipts, paths=None):
    argv = [sys.executable, str(gate), '--lane', str(repo), '--certified', certified]
    if paths:
        argv += ['--paths', str(paths)]
    for r in receipts:
        argv += ['--receipt', r]
    env = dict(os.environ)
    env.update(HOME=str(repo), GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    r = subprocess.run(argv, capture_output=True, text=True, env=env, timeout=120)
    return r


def main():
    out = []
    with tempfile.TemporaryDirectory(prefix='tameshi-r56-mutprobe-') as tmp:
        repo, c0, c1, side, paths_all, paths_one = build_fixture(tmp)

        def receipt(name, text):
            p = Path(tmp) / name
            p.write_text(text)
            return str(p)

        # one probe per mutant: (mutant_id, expected code, receipt builder, role, certified, paths)
        def p_absent():
            return receipt('absent.txt', 'VERDICT: no revision named\n')
        def p_drift():
            return receipt('drift.txt', 'VERDICT: rev=%s C1_X_PASS=true\n' % c0)
        def p_notancestor():
            return receipt('ctl.txt', 'CTL A rev=%s\n' % side)
        def p_digest():
            p = receipt('dg.txt', 'VERDICT: rev=%s C1_X_PASS=true\n' % c1)
            Path(p + '.sha256').write_text('0' * 64 + '\n')
            return p
        def p_ambiguous():
            return receipt('amb.txt', 'A rev=%s\nB rev=%s\n' % (c0, c1))
        def p_required():
            return receipt('nl.txt', 'VERDICT: rev=%s\n' % c1)
        def p_empty():
            return receipt('em.txt', '\n')

        # a commit that is NOT c1 but whose bytes are identical to c1 on the
        # declared surface — used to isolate the ambiguity guard (M5): with the
        # guard removed the gate picks one rev and, finding no drift, accepts.
        (repo / 'unrelated.txt').write_text('unrelated\n')
        gitx(repo, 'add', '--all')
        gitx(repo, '-c', 'user.name=f', '-c', 'user.email=f@example.invalid',
             'commit', '--quiet', '-m', 'c1-twin (surface identical)')
        twin = gitx(repo, 'rev-parse', 'HEAD').stdout.strip()

        def p_ambiguous_isolated():
            # two distinct rev tokens, BOTH content-identical to certified on the
            # declared surface: pristine refuses (ambiguous), the mutant accepts.
            return receipt('amb2.txt', 'A rev=%s\nB rev=%s\n' % (c1, twin))

        probes = {
            'M1': ('RECEIPT_REV_ABSENT', p_absent, 'positive', c1, None, None),
            'M2': ('RECEIPT_REV_CONTENT_DRIFT', p_drift, 'positive', c1, paths_all, None),
            'M3': ('RECEIPT_CONTROL_NOT_ANCESTOR', p_notancestor, 'control', c1, None, None),
            'M4': ('RECEIPT_DIGEST_MISMATCH', p_digest, 'verdict', c1, None, None),
            'M5': ('RECEIPT_REV_AMBIGUOUS', p_ambiguous_isolated, 'positive', c1, paths_one, None),
            'M6': ('RECEIPT_REQUIRED_LINE_MISSING', p_required, 'verdict', c1, None, 'C1_X_PASS='),
            'M7': ('RECEIPT_EMPTY', p_empty, 'positive', c1, None, None),
            'M8': ('RECEIPT_CONTROL_NOT_ANCESTOR', p_notancestor, 'control', c1, None, None),
        }

        for m in MUT:
            mid = m['id']
            code, builder, role, certified, paths, regex = probes[mid]
            # mutate a fresh copy of the pristine gate
            mg = S / ('probe-%s-gate.py' % mid)
            src = PRISTINE.read_bytes()
            mg.write_bytes(src.replace(m['old'].encode(), m['new'].encode(), 1))
            path = builder()
            spec = '%s:%s' % (path, role)
            if regex:
                spec += ':' + regex
            rp = gate_run(PRISTINE, repo, certified, [spec], paths)
            rm = gate_run(mg, repo, certified, [spec], paths)
            row = {
                'id': mid, 'name': m['name'], 'expected_code': code,
                'pristine_exit': rp.returncode, 'pristine_stdout': rp.stdout.strip(),
                'pristine_stderr_tail': rp.stderr.strip().splitlines()[-1:] or [],
                'mutant_exit': rm.returncode, 'mutant_stdout': rm.stdout.strip(),
                'mutant_stderr_tail': rm.stderr.strip().splitlines()[-1:] or [],
                'pristine_refused': rp.returncode == 3 and code in rp.stdout,
                'mutant_accepted': rm.returncode == 0,
                'mutant_named_refusal_gone': not (rm.returncode == 3 and code in rm.stdout),
            }
            # "protection removed" = the pristine gate's NAMED refusal is no
            # longer produced.  Two severities:
            #   silent-acceptance  the mutant exits 0 (worst)
            #   degraded-refusal   the mutant still refuses but with another
            #                       code, or crashes (exit != 0, != 3)
            row['protection_removed'] = row['pristine_refused'] and row['mutant_named_refusal_gone']
            if row['mutant_accepted']:
                row['severity'] = 'silent-acceptance'
            elif rm.returncode == 3:
                row['severity'] = 'degraded-refusal-other-code'
            else:
                row['severity'] = 'crash-or-other-exit'
            out.append(row)
            print('%-3s %-42s pristine exit=%d refused=%s | mutant exit=%d accepted=%s'
                  % (mid, name_short(m), rp.returncode, row['pristine_refused'],
                     rm.returncode, row['mutant_accepted']))
            mg.unlink()

    (S / 'consequence-probe.json').write_text(json.dumps(out, indent=1))
    n = sum(1 for r in out if r['protection_removed'])
    print('protection removed by %d/%d mutants' % (n, len(out)))
    return 0 if n == len(out) else 1


def name_short(m):
    return m['name'][:40]


if __name__ == '__main__':
    sys.exit(main())
