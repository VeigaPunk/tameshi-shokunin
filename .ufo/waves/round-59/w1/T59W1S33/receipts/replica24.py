#!/usr/bin/env python3
"""Scratch replica of the round-59 counter fixture matrix (24 cases) to test
reference implementations. Does NOT touch the production lane or the frozen
counter; fixtures live entirely under scratch."""
import json, os, shutil, subprocess, sys
from pathlib import Path

WORK = Path('/fast/scratch/hyaku/tameshi-r59/T59W1S33/replica')
PATHS = ['tools/runner.py', 'tools/space name.py', 'tools/日本語.py', 'tools/-runner.py']
CLASSES = ['equal', 'changed', 'missing', 'unrelated', 'unresolvable', 'symlink']

def main():
    tool = sys.argv[1]
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1', TMPDIR=str(WORK))
    def run(argv, **kw):
        return subprocess.run(argv, capture_output=True, text=True, env=env, timeout=30, **kw)
    def git(repo, *args):
        r = run(['git', '-C', str(repo), *args])
        if r.returncode:
            raise RuntimeError(r.stderr)
        return r.stdout.strip()
    results = []
    for ix, path in enumerate(PATHS):
        repo = WORK / f'fixture-{ix}'
        repo.mkdir()
        git(repo, 'init', '-q')
        assert Path(git(repo, 'rev-parse', '--show-toplevel')).resolve() == repo
        f = repo / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text('print("real executor")\n')
        git(repo, 'add', '--', path)
        def commit():
            git(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
                '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
            return git(repo, 'rev-parse', 'HEAD')
        trusted = commit()
        versions = {'equal': trusted}
        f.write_text('print("forged success")\n')
        git(repo, 'add', '--', path)
        versions['changed'] = commit()
        f.unlink()
        git(repo, 'add', '-u')
        versions['missing'] = commit()
        f.write_text('print("real executor")\n')
        (repo / 'unrelated.txt').write_text('unrelated change\n')
        git(repo, 'add', '--', path, 'unrelated.txt')
        versions['unrelated'] = commit()
        versions['unresolvable'] = '0' * 40
        f.unlink()
        f.symlink_to('elsewhere.py')
        git(repo, 'add', '--', path)
        versions['symlink'] = commit()
        for cls in CLASSES:
            expected = 0 if cls in ('equal', 'unrelated') else 2 if cls == 'unresolvable' else 1
            out = run([sys.executable, '-I', tool, '--repo', str(repo), '--trusted', trusted,
                       '--candidate', versions[cls], '--path', path])
            token = 'EXECUTOR_SOURCE_BOUND' if expected == 0 else 'EXECUTOR_SOURCE_UNAVAILABLE' if expected == 2 else 'EXECUTOR_SOURCE_DRIFT'
            ok = out.returncode == expected and token in (out.stdout + out.stderr)
            results.append({'path': path, 'class': cls, 'expected': expected,
                            'exit': out.returncode, 'ok': ok,
                            'out': (out.stdout + out.stderr).strip()[:80]})
    passed = sum(x['ok'] for x in results)
    print(json.dumps(results, ensure_ascii=False, indent=1))
    print(f'REPLICA tool={Path(tool).name} passed={passed}/24 PASS={passed == 24}')
    return 0 if passed == 24 else 1

if __name__ == '__main__':
    sys.exit(main())
