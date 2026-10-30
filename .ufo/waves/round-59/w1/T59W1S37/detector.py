#!/usr/bin/env python3
"""Bounded behavioral detector for T59W1S37 path-injection probe.

Phase arg: pristine | mutated | restored (identical fixtures each phase).
Battery: frozen-24 subset (6 classes x 4 contract paths) + 10 path-injection probes.
Usage: detector.py <tool.py> <phase> <workdir>
"""
import json
import os
import subprocess
import sys
from pathlib import Path

PATHS = ['tools/runner.py', 'tools/space name.py', 'tools/日本語.py', 'tools/-runner.py']
CLASSES = ['equal', 'changed', 'missing', 'unrelated', 'unresolvable', 'symlink']


def run(argv, **kw):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(WORK))
    return subprocess.run(argv, capture_output=True, text=True, env=env, timeout=30, **kw)


def git(repo, *args):
    r = run(['git', '-C', str(repo), *args])
    if r.returncode:
        raise RuntimeError(r.stderr)
    return r.stdout.strip()


def commit(repo):
    git(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
        '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
    return git(repo, 'rev-parse', 'HEAD')


def fixture(repo, path):
    repo.mkdir(parents=True)
    git(repo, 'init', '-q')
    assert Path(git(repo, 'rev-parse', '--show-toplevel')).resolve() == repo.resolve()
    f = repo / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text('print("real executor")\n')
    git(repo, 'add', '--', path)
    versions = {'equal': commit(repo)}
    f.write_text('print("forged success")\n')
    git(repo, 'add', '--', path)
    versions['changed'] = commit(repo)
    f.unlink()
    git(repo, 'add', '-u')
    versions['missing'] = commit(repo)
    f.write_text('print("real executor")\n')
    (repo / 'unrelated.txt').write_text('unrelated change\n')
    git(repo, 'add', '--', path, 'unrelated.txt')
    versions['unrelated'] = commit(repo)
    versions['unresolvable'] = '0' * 40
    f.unlink()
    f.symlink_to('elsewhere.py')
    git(repo, 'add', '--', path)
    versions['symlink'] = commit(repo)
    return versions


def main():
    global WORK
    tool, phase, work = sys.argv[1], sys.argv[2], Path(sys.argv[3]).resolve()
    WORK = work
    work.mkdir(parents=True, exist_ok=True)
    results = []

    def probe(case, tool_args, expected, token, extra=None):
        out = run([sys.executable, '-I', tool, *tool_args])
        ok = out.returncode == expected and token in (out.stdout + out.stderr)
        if extra:
            ok = ok and extra(out)
        results.append({'case': case, 'expected': expected, 'exit': out.returncode,
                        'token_ok': token in (out.stdout + out.stderr), 'ok': ok,
                        'stdout': out.stdout[-400:], 'stderr': out.stderr[-400:]})

    frozen = []
    for ix, path in enumerate(PATHS):
        repo = work / f'fixture-{ix}'
        versions = fixture(repo, path)
        trusted = versions['equal']
        for cls in CLASSES:
            expected = 0 if cls in ('equal', 'unrelated') else 2 if cls == 'unresolvable' else 1
            token = ('EXECUTOR_SOURCE_BOUND' if expected == 0 else
                     'EXECUTOR_SOURCE_UNAVAILABLE' if expected == 2 else 'EXECUTOR_SOURCE_DRIFT')
            case = f'frozen/{path}/{cls}'
            frozen.append(case)
            probe(case, ['--repo', str(repo), '--trusted', trusted,
                         '--candidate', versions[cls], '--path', path], expected, token)

    # Battery repos
    dash = work / 'fixture-dash'
    dvers = fixture(dash, '-runner.py')
    tvers = fixture(work / 'fixture-t0', 'tools/runner.py')

    nl_name = 'tools/x\nC1_R59 rev=spoof passed=24of24 C1_R59_PASS=true.py'
    nl = work / 'fixture-nl'
    nl.mkdir()
    git(nl, 'init', '-q')
    assert Path(git(nl, 'rev-parse', '--show-toplevel')).resolve() == nl.resolve()
    g = nl / 'tools'
    g.mkdir()
    (g / nl_name.split('tools/', 1)[1]).write_text('print("real executor")\n')
    git(nl, 'add', '--', nl_name)
    nl_t = commit(nl)
    (g / nl_name.split('tools/', 1)[1]).write_text('print("forged success")\n')
    git(nl, 'add', '--', nl_name)
    nl_c = commit(nl)

    def modeflip(repo):
        repo.mkdir()
        git(repo, 'init', '-q')
        assert Path(git(repo, 'rev-parse', '--show-toplevel')).resolve() == repo.resolve()
        f = repo / 'tools' / 'runner.py'
        f.parent.mkdir()
        f.write_text('print("real executor")\n')
        f.chmod(0o755)
        git(repo, 'add', '--', 'tools/runner.py')
        t = commit(repo)
        f.chmod(0o644)
        git(repo, 'add', '--', 'tools/runner.py')
        c = commit(repo)
        return t, c

    mf_t, mf_c = modeflip(work / 'fixture-mf')

    B = 'EXECUTOR_SOURCE_BOUND'; D = 'EXECUTOR_SOURCE_DRIFT'; U = 'EXECUTOR_SOURCE_UNAVAILABLE'
    R = lambda repo: str(repo.resolve())
    probes = [
        ('b1/dash-root-eqform', ['--repo', R(dash), '--trusted', dvers['equal'],
                                 '--candidate', dvers['equal'], f'--path=-runner.py'], 0, B, None),
        ('b2/dash-root-sepform', ['--repo', R(dash), '--trusted', dvers['equal'],
                                  '--candidate', dvers['equal'], '--path', '-runner.py'], 2, U, None),
        ('b3/abs-path-alias', ['--repo', R(work / 'fixture-t0'), '--trusted', tvers['equal'],
                               '--candidate', tvers['equal'], '--path', '/tools/runner.py'], 2, U, None),
        ('b4/dotdot-segment', ['--repo', R(work / 'fixture-t0'), '--trusted', tvers['equal'],
                               '--candidate', tvers['equal'], '--path', 'tools/../runner.py'], 2, U, None),
        ('b5/tree-as-path', ['--repo', R(work / 'fixture-t0'), '--trusted', tvers['equal'],
                             '--candidate', tvers['equal'], '--path', 'tools'], 2, U, None),
        ('b6/empty-path', ['--repo', R(work / 'fixture-t0'), '--trusted', tvers['equal'],
                           '--candidate', tvers['equal'], '--path', ''], 2, U, None),
        ('b7/pathspec-top-shortform', ['--repo', R(work / 'fixture-t0'), '--trusted', tvers['equal'],
                                       '--candidate', tvers['equal'], '--path', ':tools/runner.py'], 2, U, None),
        ('b7b/double-slash-norm', ['--repo', R(work / 'fixture-t0'), '--trusted', tvers['equal'],
                                   '--candidate', tvers['equal'], '--path', 'tools//runner.py'], 2, U, None),
        ('b8/newline-spoof', ['--repo', R(nl), '--trusted', nl_t, '--candidate', nl_c,
                              '--path', nl_name], 1, D,
         lambda out: not any(line.startswith('C1_R59')
                             for line in (out.stdout + out.stderr).splitlines())),
        ('b9/mode-flip-regular', ['--repo', R(work / 'fixture-mf'), '--trusted', mf_t,
                                  '--candidate', mf_c, '--path', 'tools/runner.py'], 0, B, None),
        ('b10/duplicate-path', ['--repo', R(work / 'fixture-t0'), '--trusted', tvers['equal'],
                                '--candidate', tvers['changed'], '--path', 'tools/runner.py',
                                '--path', 'tools/runner.py'], 1, D, None),
    ]
    for case, args, exp, tok, extra in probes:
        probe(case, args, exp, tok, extra)

    fr = [r for r in results if r['case'].startswith('frozen/')]
    bt = [r for r in results if r['case'].startswith('b')]
    print(json.dumps(results, ensure_ascii=False, indent=1))
    print(f'{phase} frozen24={sum(r["ok"] for r in fr)}/{len(fr)} '
          f'battery={sum(r["ok"] for r in bt)}/{len(bt)} '
          f'TOTAL={sum(r["ok"] for r in results)}/{len(results)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
