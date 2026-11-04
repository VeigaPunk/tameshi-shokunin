import concurrent.futures, hashlib, json, os, pathlib, shutil, subprocess
S = pathlib.Path(__file__).resolve().parent
D = pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-78/design')
R = pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-78/w1/T78W1M1')
R.mkdir(parents=True, exist_ok=True)
B = S / 'bin'; B.mkdir(exist_ok=True)
realgit = shutil.which('git')
wrapper = '''#!/usr/bin/env python3
import os, subprocess, sys
real = %r
a = sys.argv[1:]
if 'commit' in a:
    if '-C' not in a: raise SystemExit('GUARD: commit without -C')
    root = a[a.index('-C')+1]
    top = subprocess.check_output([real, '-C', root, 'rev-parse', '--show-toplevel'], text=True).strip()
    if os.path.realpath(top) != os.path.realpath(root): raise SystemExit('GUARD: misroot')
    if not os.path.realpath(root).startswith(%r + os.sep): raise SystemExit('GUARD: outside scratch')
os.execv(real, [real, '-c', 'commit.gpgsign=false'] + a)
''' % (realgit, str(S))
(B / 'git').write_text(wrapper); (B / 'git').chmod(0o755)
(R / 'git-guard.py').write_text(wrapper)
mutants = [
 ('s1-python-prefix', 'selfstate-freshness.py', "prefix = INTERPRETERS[inst.get('interpreter', DEFAULT_INTERPRETER)]", "prefix = INTERPRETERS['python']", 'ARM13_bash_interpreter_row', 'Real defect: explicit bash rows run as Python and refuse instead of measuring.'),
 ('s2-default-bash', 'selfstate-freshness.py', "DEFAULT_INTERPRETER = 'python'", "DEFAULT_INTERPRETER = 'bash'", 'ARM11_doc_rev_cli_binding', 'Real defect: rows without interpreter run as bash instead of the frozen Python default.'),
 ('s3-python-isolation-dropped', 'selfstate-freshness.py', "'python': ('python3', '-I', '-X', 'utf8'),", "'python': ('python3',),", 'No existing arm predicted; the Python tuple changes', 'Real coverage hole if survived: real Python instruments can import cwd/PYTHONPATH packages, and encoding flags differ; the fixed interpreter tuple is not enforced by a distinguishing fixture. This changes execution, not just fixture assurance.'),
 ('w1-leak-scan-empty', 'wave-reconcile.py', "return set(p for p in os.listdir(tempfile.gettempdir())\n                           if p.startswith(GIT_FIXTURE_PREFIX))", "return set()", 'No existing arm predicted without a cleanup fault', 'Real detector coverage hole if survived: a leftover fixture is never reported. Healthy cleanup produces no leak and therefore cannot positively exercise the leak post-condition; not equivalent under a cleanup failure.'),
 ('w2-head-guard-removed', 'wave-reconcile.py', "if head == rev:\n                    raise SetupError('git-fixture-head-equals-rev')", 'if False:\n                    pass', 'No existing arm predicted', 'Equivalent for healthy git fixture execution: rev2 successfully adds a tracked file and commits, so HEAD necessarily differs from rev1. This removes defensive fixture assurance, not production pinned-revision behavior.'),
 ('w3-arm21-cleanup-removed', 'wave-reconcile.py', '                shutil.rmtree(fix)\n', '                pass\n', 'arm21-pinned-rev-listing-at-head-drift', 'Real fixture defect: arm21 leaves its git fixture behind; the new leftover post-condition should kill it.'),
]
def digest(raw): return hashlib.sha256(raw).hexdigest()
def run_one(m):
    name, filename, old, new, expected, interpretation = m
    root = S / name; root.mkdir()
    tmp = root / 'tmp'; tmp.mkdir()
    target = root / filename
    raw = (D / filename).read_bytes()
    assert raw.count(old.encode()) == 1, (name, raw.count(old.encode()))
    mutated = raw.replace(old.encode(), new.encode(), 1)
    env = dict(os.environ, TMPDIR=str(tmp), PATH=str(B)+os.pathsep+os.environ['PATH'])
    phases = []
    try:
        for phase, data in [('pristine', raw), ('mutated', mutated), ('restored', raw)]:
            target.write_bytes(data)
            cmd = ['python3', '-I', '-X', 'utf8', str(target), '--selftest']
            try:
                p = subprocess.run(cmd, cwd=root, env=env, capture_output=True, timeout=180)
                stdout, stderr, rc = p.stdout.decode(errors='replace'), p.stderr.decode(errors='replace'), p.returncode
            except subprocess.TimeoutExpired as e:
                stdout, stderr, rc = (e.stdout or b'').decode(errors='replace'), (e.stderr or b'').decode(errors='replace'), 'TIMEOUT'
            (R / (name+'-'+phase+'.stdout')).write_text(stdout)
            (R / (name+'-'+phase+'.stderr')).write_text(stderr)
            phases.append({'phase':phase, 'command':cmd, 'cwd':str(root), 'TMPDIR':str(tmp), 'exit':rc, 'sha256':digest(target.read_bytes()), 'terminal':stdout.splitlines()[-1:] , 'failing_arms':[line for line in stdout.splitlines() if 'FAIL' in line]})
    finally:
        target.write_bytes(raw)
    verdict = 'INCONCLUSIVE' if phases[0]['exit'] != 0 or phases[2]['exit'] != 0 else ('SURVIVED' if phases[1]['exit'] == 0 else 'KILLED')
    return {'mutant':name, 'instrument':filename, 'old':old, 'new':new, 'expected_detector':expected, 'interpretation':interpretation, 'verdict':verdict, 'phases':phases, 'restoration_sha256':digest(target.read_bytes()), 'byte_identical_restore':target.read_bytes()==raw}
try:
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(run_one, mutants))
    (R / 'results.json').write_text(json.dumps(results, indent=2)+'\n')
    for result in results:
        print(result['mutant'], result['verdict'])
        for phase in result['phases']:
            print(phase['phase'], 'exit='+str(phase['exit']), *phase['terminal'])
            for failure in phase['failing_arms']: print(failure)
        print('RESTORE', result['restoration_sha256'], result['byte_identical_restore'])
finally:
    shutil.rmtree(S)
    (R / 'cleanup.txt').write_text('scratch_exists='+str(S.exists())+'\n')
