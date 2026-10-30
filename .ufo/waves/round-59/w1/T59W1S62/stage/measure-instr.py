#!/usr/bin/env python3
"""Frozen round59 counter: 24 CLI fixtures, no implementation-reported credit."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PATHS = ['tools/runner.py', 'tools/space name.py', 'tools/日本語.py', 'tools/-runner.py']
CLASSES = ['equal', 'changed', 'missing', 'unrelated', 'unresolvable', 'symlink']

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--lane', required=True)
    p.add_argument('--rev', required=True)
    p.add_argument('--work', required=True)
    p.add_argument('--tool', help='control executable override; never used for certification')
    a = p.parse_args()
    work = Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    if any(work.iterdir()):
        p.error('--work must be empty')
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(work))
    def run(argv, **kw):
        return subprocess.run(argv, capture_output=True, text=True, env=env, timeout=30, **kw)
    def git(repo, *args):
        r = run(['git', '-C', str(repo), *args])
        if r.returncode:
            raise RuntimeError(r.stderr)
        return r.stdout.strip()
    rev = git(a.lane, 'rev-parse', '--verify', a.rev+'^{commit}')
    r = run(['git', '-C', a.lane, 'show', rev+':tools/executor-source-pin.py'])
    if r.returncode and not a.tool:
        print(f'C1_R59 rev={rev} passed=0/24 C1_R59_PASS=false reason=tool-absent')
        return 1
    results = []
    try:
        tool = Path(a.tool).resolve() if a.tool else work/'tool.py'
        if not a.tool:
            tool.write_text(r.stdout)
        for ix, path in enumerate(PATHS):
            repo = work/f'fixture-{ix}'
            repo.mkdir()
            git(repo, 'init', '-q')
            if Path(git(repo, 'rev-parse', '--show-toplevel')).resolve() != repo:
                raise RuntimeError('fixture root mismatch')
            f = repo/path
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text('print("real executor")\n')
            git(repo, 'add', '--', path)
            def commit():
                git(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
                return git(repo, 'rev-parse', 'HEAD')
            trusted = commit()
            versions = {'equal': trusted}; print('TRUSTED', path, trusted)
            f.write_text('print("forged success")\n')
            git(repo, 'add', '--', path)
            versions['changed'] = commit()
            f.unlink()
            git(repo, 'add', '-u')
            versions['missing'] = commit()
            f.write_text('print("real executor")\n')
            (repo/'unrelated.txt').write_text('unrelated change\n')
            git(repo, 'add', '--', path, 'unrelated.txt')
            versions['unrelated'] = commit()
            versions['unresolvable'] = '0'*40
            f.unlink()
            f.symlink_to('elsewhere.py')
            git(repo, 'add', '--', path)
            versions['symlink'] = commit()
            for cls in CLASSES:
                expected = 0 if cls in ('equal', 'unrelated') else 2 if cls == 'unresolvable' else 1
                out = run([sys.executable, '-I', str(tool), '--repo', str(repo), '--trusted', trusted, '--candidate', versions[cls], '--path', path])
                token = 'EXECUTOR_SOURCE_BOUND' if expected == 0 else 'EXECUTOR_SOURCE_UNAVAILABLE' if expected == 2 else 'EXECUTOR_SOURCE_DRIFT'
                ok = out.returncode == expected and token in (out.stdout+out.stderr)
                results.append({'path':path,'class':cls,'expected':expected,'exit':out.returncode,'stdout':out.stdout,'stderr':out.stderr,'ok':ok})
        passed = sum(x['ok'] for x in results)
        print(json.dumps(results, ensure_ascii=False, indent=1))
        print(f'C1_R59 rev={rev} passed={passed}/24 C1_R59_PASS={str(passed == 24).lower()}')
        return 0 if passed == 24 else 1
    finally:
        for f in list(work.iterdir()):
            if f.is_dir():
                shutil.rmtree(f)
            else:
                f.unlink()

if __name__ == '__main__':
    sys.exit(main())
