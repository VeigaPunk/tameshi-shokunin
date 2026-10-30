#!/usr/bin/env python3
"""PROPOSED round+1 counter addendum (T59W1S32): multi-path aggregation surface.

The frozen round-59 counter (evidence/round-59/measure.py) invokes the gate with
exactly ONE --path per run. A gate that evaluates only the first declared path, or
that accepts when any one path matches, passes 24/24 while violating the frozen
exit_map: exit 0 requires ALL declared regular executable-source blobs to equal
trusted blobs. This addendum measures the multi-path surface with the same
contract CLI, same env discipline, and the same pass criterion (exit code +
token in stdout+stderr).

Not for certification of round 59: measure.py there is frozen
(frozen_before_scoring=true). L1 seats the canonical measurement.

Usage: python3 executor-source-pin-multipath-probe.py --tool TOOL [--work EMPTY_DIR]
Prints one JSON line per case and a final C1_R59_MULTIPATH summary line.
"""
import argparse, itertools, json, os, shutil, subprocess, sys, tempfile

PATHS = ['tools/runner.py', 'tools/space name.py', 'tools/日本語.py', 'tools/-runner.py']
TOK = {0: 'EXECUTOR_SOURCE_BOUND', 1: 'EXECUTOR_SOURCE_DRIFT', 2: 'EXECUTOR_SOURCE_UNAVAILABLE'}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tool', required=True)
    ap.add_argument('--work', default=None)
    a = ap.parse_args()
    from pathlib import Path
    work = Path(a.work).resolve() if a.work else Path(tempfile.mkdtemp(prefix='mp-probe-'))
    work.mkdir(parents=True, exist_ok=True)
    if any(work.iterdir()):
        ap.error('--work must be empty')
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(work))
    def run(argv):
        return subprocess.run(argv, capture_output=True, text=True, env=env, timeout=30)
    def git(repo, *args):
        r = run(['git', '-C', str(repo), *args])
        if r.returncode:
            raise RuntimeError(r.stderr)
        return r.stdout.strip()

    repo = work / 'fixture'
    repo.mkdir()
    git(repo, 'init', '-q')
    assert Path(git(repo, 'rev-parse', '--show-toplevel')).resolve() == repo
    for p in PATHS:
        f = repo / p
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text('print("real executor")\n')
    git(repo, 'add', '--', *PATHS)
    def commit(msg):
        git(repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
            '-c', 'commit.gpgsign=false', 'commit', '-qm', msg)
        return git(repo, 'rev-parse', 'HEAD')
    trusted = commit('trusted')

    # candidate variants: one path per class of violation, all four paths declared
    def rewrite(path, text):
        (repo / path).write_text(text)
        git(repo, 'add', '--', path)
    cands = {}
    for p in PATHS:
        rewrite(p, 'print("forged")\n')
        cands[('changed', p)] = commit(f'changed {p}')
        git(repo, 'checkout', '-q', trusted)
    for p in PATHS:
        (repo / p).unlink()
        git(repo, 'add', '-u')
        cands[('missing', p)] = commit(f'missing {p}')
        git(repo, 'checkout', '-q', trusted)
    (repo / PATHS[3]).unlink()
    (repo / PATHS[3]).symlink_to('elsewhere.py')
    git(repo, 'add', '--', PATHS[3])
    cands[('symlink', PATHS[3])] = commit('symlink')
    git(repo, 'checkout', '-q', trusted)
    git(repo, 'rm', '-q', '--cached', PATHS[0])
    (repo / PATHS[0]).unlink()
    git(repo, 'update-index', '--add', '--cacheinfo', '160000',
        git(repo, 'rev-parse', f'{trusted}:tools'), PATHS[0])
    cands[('gitlink', PATHS[0])] = commit('gitlink')
    git(repo, 'checkout', '-q', trusted)
    cands[('unrelated', None)] = trusted  # equal baseline; unrelated file tested below
    (repo / 'unrelated.txt').write_text('unrelated\n')
    git(repo, 'add', '--', 'unrelated.txt')
    cands[('unrelated', None)] = commit('unrelated')

    def invoke(cand, paths):
        argv = [sys.executable, '-I', a.tool, '--repo', str(repo),
                '--trusted', trusted, '--candidate', cand]
        for p in paths:
            argv += ['--path', p]
        return subprocess.run(argv, capture_output=True, text=True, env=env, timeout=30)

    results = []
    def check(label, cand, paths, expected):
        out = invoke(cand, paths)
        ok = out.returncode == expected and TOK[expected] in (out.stdout + out.stderr)
        results.append({'case': label, 'expected': expected, 'exit': out.returncode,
                        'stdout': out.stdout.strip(), 'stderr': out.stderr.strip(), 'ok': ok})

    check('all-equal, all four declared', cands[('unrelated', None)], PATHS, 0)
    for (cls, p), c in sorted(cands.items()):
        if cls == 'unrelated':
            continue
        exp = 2 if cls == 'unresolved' else 1
        check(f'{cls}: {p} (all four declared)', c, PATHS, exp)
    check('candidate unresolvable (all four declared)', '0' * 40, PATHS, 2)
    check('vacuous declaration (absent at both revs)', cands[('unrelated', None)],
          ['tools/ghost.py'], 2)
    check('duplicate --path idempotent', cands[('unrelated', None)],
          [PATHS[0]] * 3, 0)
    # order invariance: same evidence, every permutation must give identical exit
    drift_c = cands[('changed', PATHS[1])]
    exits = set()
    for perm in itertools.permutations(PATHS):
        out = invoke(drift_c, list(perm))
        exits.add(out.returncode)
    results.append({'case': 'order invariance: 24 permutations of changed evidence',
                    'expected': 1, 'exit': sorted(exits), 'ok': exits == {1}})

    passed = sum(1 for r in results if r['ok'])
    for r in results:
        print(json.dumps(r, ensure_ascii=False))
    print(f'C1_R59_MULTIPATH passed={passed}/{len(results)} '
          f'C1_R59_MULTIPATH_PASS={str(passed == len(results)).lower()}')
    shutil.rmtree(work, ignore_errors=True)
    return 0 if passed == len(results) else 1

if __name__ == '__main__':
    sys.exit(main())
