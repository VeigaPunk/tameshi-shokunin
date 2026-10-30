import argparse
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r58/T58W2MutC2')
spec = importlib.util.spec_from_file_location('m', S / 'cnt' / 'measure.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

orig_run_row = m.run_row


def run_row_dbg(rc_path, root, name, rev, work, env):
    cmd = [sys.executable, str(rc_path), '--root', str(root)]
    if rev is not None:
        cmd += ['--rev', rev]
    cmd += ['--only', name]
    proc = subprocess.run(cmd, capture_output=True, cwd=str(work), env=env)
    print('RUNROW name=%s rc=%d' % (name, proc.returncode))
    print('  stdout:', proc.stdout.decode('utf-8', 'replace')[:1500].replace('\n', '\n    '))
    print('  stderr:', proc.stderr.decode('utf-8', 'replace')[:1500].replace('\n', '\n    '))
    return orig_run_row(rc_path, root, name, rev, work, env)


m.run_row = run_row_dbg

orig_bcf = m.build_cell_fixture


def bcf_dbg(work, gate_path):
    d = Path(tempfile.mkdtemp(prefix='c2-cell-', dir=str(work)))
    env = m.lane_env()
    ident = ['-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid']

    def g(*a):
        return subprocess.run(['git', '-C', str(d)] + ident + list(a), env=env, capture_output=True)

    g('init', '-q')
    (d / 'surface.txt').write_text('one\n')
    g('add', '-A')
    g('commit', '-q', '-m', 'A')
    ra = g('rev-parse', 'HEAD').stdout.decode().strip()
    (d / 'surface.txt').write_text('two\n')
    g('commit', '-q', '-a', '-m', 'B')
    rb = g('rev-parse', 'HEAD').stdout.decode().strip()
    paths = d.parent / (d.name + '.paths')
    paths.write_text('surface.txt\n')
    receipt = d.parent / (d.name + '.receipt')
    receipt.write_text('VERDICT: rev=%s C1_X_PASS=true\n' % ra)
    proc = subprocess.run([sys.executable, str(gate_path), '--lane', str(d), '--certified', rb,
                           '--paths', str(paths), '--receipt', '%s:verdict' % receipt],
                          capture_output=True, env=env, cwd=str(d.parent))
    print('CELL gate rc=%d' % proc.returncode)
    print('  stdout:', proc.stdout.decode('utf-8', 'replace')[:1500].replace('\n', '\n    '))
    print('  stderr:', proc.stderr.decode('utf-8', 'replace')[:1500].replace('\n', '\n    '))
    return orig_bcf(work, gate_path)


m.build_cell_fixture = bcf_dbg

ns = argparse.Namespace(lane=str(S / 'clone'), rev='8063d0a551fc5b3cb5a2d397da7353af53444534',
                        work=str(S / 'work-probe'), explain=False)
Path(ns.work).mkdir(exist_ok=True)
rc = m.main_measure(ns)
print('main_measure rc=%d' % rc)
