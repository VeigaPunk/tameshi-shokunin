#!/usr/bin/env python3
"""Sandboxed confirmation of the round-49 C2 panel (tameshi round 50, seat T50ExecSuccC2).

Closes the second half of routed item R49.2: the round-49 counter (`.ufo/evidence/round-49/c2/
measure.py`) runs the property generator with the pristine guard in the generator's own cwd
(`measure.py:219` + `:250-258`) and with the whole filesystem readable (`:214-219`), so a
generator that merely diffs the guard under test against `./staged-id-guard.py` passes every
leg (critique `.ufo/waves/round-49/w1/T49CritC2Contract.md` F1/F2). The counter therefore
cannot tell a property-based generator from a differential one.

This harness re-runs the *same frozen generator* (`tools/pbt-staged-id.py` at REV) and the
*same 12 public round-49 panel mutants* inside a bubblewrap namespace whose filesystem view
holds only

    /run/pbt-staged-id.py      the generator, bytes from REV
    /run/staged-id-guard.py    the one guard under test (pristine for the baseline leg, the
                               mutant for that mutant's leg)
    /run/scratch/              writable scratch (TMPDIR, HOME, case files, dump)
    /usr /lib /lib64 /proc /dev /etc/ld.so.cache   read-only system, nothing else

There is no /home in the namespace, so the lane, its pristine guard and the round-49 panel are
unreachable; a probe script run in the same namespace proves it: it must fail to open the lane's
guard path, must fail to open the lane's panel path, must see no /home, must see exactly one
file named staged-id-guard.py (the guard under test, sha pinned) and must fail to run git in the
lane.

Interface (frozen by the seat item):

    python3 -I sandboxed-confirm.py --lane LANE --rev REV --panel PANEL --work DIR [--out FILE]
    python3 -I sandboxed-confirm.py --selftest [--work DIR]

CASE/verdict semantics are the round-49 counter's, re-implemented here: the baseline leg must
exit 0 with cases==CASES and violations=0 and a dump of CASES cases; a mutant is *confirmed*
only when the generator exits 1 with a counterexample index that is in its dump **and** the
pristine guard and the mutant guard, each run in its own sandbox on that single case, produce
different comparable output (exit code + JSON minus the two sha fields).

This is a probe, not a verdict: it prints confirmed/unconfirmed per mutant and exits 0 only when
the harness itself is sound (baseline leg green, every probe green, every status decided).

stdlib only; `bwrap` from PATH is required and its version is recorded.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

REV_DEFAULT = 'e3729de862f73ae080d98fcf522a7081ce16e40a'
GUARD = 'tools/staged-id-guard.py'
GENERATOR = 'tools/pbt-staged-id.py'
GUARD_SHA = '03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8'
GENERATOR_SHA = '0cbee392a83e4cd6609efa97395a9ae8a64115015cf290e42e9a4ff98bc01f05'
PANEL = '.ufo/evidence/round-49/c2/panel.json'
PANEL_SHA = 'd6dd2cf38317118b14dfcdc1069b3222e3d4dc65ff05e005fc2b0592ce2eeda1'
SEED, CASES = 4949, 400          # the round-49 counter's frozen seed and case count
LAST_RE = re.compile(r'^PBT_STAGED_ID: cases=(\d+) violations=(\d+) counterexample=(\d+|none)\b')
SHA_KEYS = ('registry_sha256', 'staged_sha256')
SYSTEM_BINDS = ('/usr', '/lib', '/lib64', '/etc/ld.so.cache', '/etc/alternatives')
GUARD_NAME = 'staged-id-guard.py'
# the sandbox scratch holds the two harness helpers, written by this file
RUN_CASE = r'''import json, os, subprocess, sys
case_path, guard = sys.argv[1], sys.argv[2]
work = os.path.dirname(os.path.abspath(case_path))
with open(case_path, encoding='utf-8') as fh:
    case = json.load(fh)
reg = os.path.join(work, 'registry.md')
stg = os.path.join(work, 'staged.md')
mp = os.path.join(work, 'map.json')
with open(reg, 'w', encoding='utf-8', newline='') as fh:
    fh.write(case['registry'])
with open(stg, 'w', encoding='utf-8', newline='') as fh:
    fh.write(case['staged'])
argv = [sys.executable, '-I', guard, '--registry', reg, '--staged', stg]
if case.get('map') is None:
    if os.path.exists(mp):
        os.unlink(mp)
else:
    with open(mp, 'w', encoding='utf-8') as fh:
        json.dump(case['map'], fh)
    argv += ['--map', mp]
argv.append('--json')
proc = subprocess.run(argv, capture_output=True, timeout=120, cwd=work)
try:
    answer = json.loads(proc.stdout.decode('utf-8'))
except Exception:
    answer = None
print(json.dumps({'exit': proc.returncode, 'json': answer,
                  'raw': proc.stdout.decode('utf-8', 'replace')[:2000]}))
'''
PROBE = r'''import hashlib, json, os, subprocess, sys
lane_guard, expect_sha, lane_root = sys.argv[1], sys.argv[2], sys.argv[3]

def attempt(path):
    try:
        with open(path, 'rb') as fh:
            return {'opened': True, 'bytes': len(fh.read())}
    except OSError as exc:
        return {'opened': False, 'errno': type(exc).__name__, 'detail': str(exc)[:140]}

out = {'lane_guard_open': attempt(lane_guard),
       'lane_panel_open': attempt(os.path.join(lane_root, '.ufo/evidence/round-49/c2/panel.json')),
       'home_exists': os.path.isdir('/home')}
found = []
for root, dirs, files in os.walk('/', topdown=True):
    dirs[:] = [d for d in dirs if os.path.join(root, d) not in ('/proc', '/sys', '/dev')]
    if 'staged-id-guard.py' in files:
        path = os.path.join(root, 'staged-id-guard.py')
        try:
            with open(path, 'rb') as fh:
                digest = hashlib.sha256(fh.read()).hexdigest()
        except OSError:
            digest = 'unreadable'
        found.append({'path': path, 'sha256': digest})
out['guards_found'] = found
try:
    git = subprocess.run(['/usr/bin/git', '-C', lane_root, 'rev-parse', '--show-toplevel'],
                         capture_output=True)
    out['lane_git'] = {'exit': git.returncode,
                       'stderr': git.stderr.decode('utf-8', 'replace')[:160]}
    git_failed = git.returncode != 0
except OSError as exc:
    out['lane_git'] = {'exit': None, 'stderr': type(exc).__name__}
    git_failed = True
out['ok'] = (not out['lane_guard_open']['opened'] and not out['lane_panel_open']['opened']
             and not out['home_exists'] and len(found) == 1
             and found[0]['sha256'] == expect_sha and git_failed)
print(json.dumps(out, sort_keys=True))
sys.exit(0 if out['ok'] else 1)
'''
GROSS_GUARD = '''#!/usr/bin/env python3
"""Fixture guard: answers every question with an empty object (never a valid answer)."""
import argparse
import json
import sys


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--registry')
    parser.add_argument('--staged')
    parser.add_argument('--map')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    parser.parse_args(argv)
    print(json.dumps({}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
'''


class Setup(Exception):
    """The harness cannot be built; nothing is measured."""


def sha256(data):
    import hashlib
    return hashlib.sha256(data).hexdigest()


def lane_default():
    here = os.path.abspath(__file__)
    probe = os.path.dirname(here)
    while True:
        if os.path.isfile(os.path.join(probe, GUARD)) and os.path.isdir(os.path.join(probe, '.ufo')):
            return probe
        parent = os.path.dirname(probe)
        if parent == probe:
            return os.getcwd()
        probe = parent


def blob(lane, rev, path):
    proc = subprocess.run(['git', '-C', lane, 'cat-file', '-p', '%s:%s' % (rev, path)],
                          capture_output=True)
    if proc.returncode != 0:
        raise Setup('git cat-file failed for %s:%s: %s'
                    % (rev, path, proc.stderr.decode('utf-8', 'replace').strip()[:200]))
    return proc.stdout


def bwrap_binary():
    path = shutil.which('bwrap')
    if path is None:
        raise Setup('bwrap is not on PATH; the sandbox cannot be built (no unsandboxed fallback)')
    proc = subprocess.run([path, '--version'], capture_output=True)
    version = (proc.stdout or proc.stderr).decode('utf-8', 'replace').strip()
    return path, version


def binds():
    used = []
    for src in SYSTEM_BINDS:
        if os.path.exists(src):
            used.append(src)
    return used


def make_run_dir(base, tag, gen_bytes, guard_bytes):
    """A directory that becomes /run inside the sandbox: generator, one guard, scratch."""
    run = os.path.join(base, 'run-%s' % tag)
    os.makedirs(os.path.join(run, 'scratch', 'tmp'), exist_ok=True)
    os.makedirs(os.path.join(run, 'scratch', 'home'), exist_ok=True)
    with open(os.path.join(run, 'pbt-staged-id.py'), 'wb') as fh:
        fh.write(gen_bytes)
    with open(os.path.join(run, GUARD_NAME), 'wb') as fh:
        fh.write(guard_bytes)
    with open(os.path.join(run, 'scratch', 'run-case.py'), 'w', encoding='utf-8') as fh:
        fh.write(RUN_CASE)
    with open(os.path.join(run, 'scratch', 'probe.py'), 'w', encoding='utf-8') as fh:
        fh.write(PROBE)
    return run


def sandbox_argv(bwrap, run, argv, extra_binds=()):
    cmd = [bwrap, '--die-with-parent', '--unshare-all', '--new-session']
    for src in binds():
        cmd += ['--ro-bind', src, src]
    for src in extra_binds:
        cmd += ['--ro-bind', src, src]
    cmd += ['--proc', '/proc', '--dev', '/dev',
            '--bind', run, '/run', '--chdir', '/run',
            '--clearenv',
            '--setenv', 'PATH', '/usr/bin',
            '--setenv', 'HOME', '/run/scratch/home',
            '--setenv', 'TMPDIR', '/run/scratch/tmp',
            '--setenv', 'LC_ALL', 'C.UTF-8',
            '--setenv', 'PYTHONDONTWRITEBYTECODE', '1']
    return cmd + list(argv)


def run_sandbox(bwrap, run, argv, timeout, extra_binds=()):
    cmd = sandbox_argv(bwrap, run, argv, extra_binds)
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {'exit': 124, 'stdout': '', 'stderr': 'timeout', 'argv': cmd}
    return {'exit': proc.returncode,
            'stdout': proc.stdout.decode('utf-8', 'replace'),
            'stderr': proc.stderr.decode('utf-8', 'replace'),
            'argv': cmd}


def probe(bwrap, run, lane_root, expect_sha, extra_binds=()):
    res = run_sandbox(bwrap, run, ['/usr/bin/python3', '-I', '/run/scratch/probe.py',
                                   os.path.join(lane_root, GUARD), expect_sha, lane_root], 300,
                      extra_binds)
    report = None
    for line in reversed([ln for ln in res['stdout'].splitlines() if ln.strip()]):
        try:
            report = json.loads(line)
        except ValueError:
            continue
        break
    ok = res['exit'] == 0 and isinstance(report, dict) and report.get('ok') is True
    return {'ok': ok, 'exit': res['exit'], 'report': report,
            'stderr': res['stderr'][:400]}


def load_dump(path):
    cases = []
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            if line.strip():
                cases.append(json.loads(line))
    return cases


def parse_last(stdout):
    lines = [ln for ln in stdout.splitlines() if ln.strip()]
    if not lines:
        return None
    return LAST_RE.match(lines[-1])


def generator_run(bwrap, run, tag, seed, cases, timeout):
    dump = os.path.join(run, 'scratch', 'dump-%s.jsonl' % tag)
    if os.path.exists(dump):
        os.unlink(dump)
    res = run_sandbox(bwrap, run,
                      ['/usr/bin/python3', '-I', '/run/pbt-staged-id.py',
                       '--guard', '/run/' + GUARD_NAME,
                       '--seed', str(seed), '--cases', str(cases),
                       '--dump', '/run/scratch/dump-%s.jsonl' % tag], timeout)
    last = parse_last(res['stdout'])
    dumped = load_dump(dump) if os.path.exists(dump) else None
    violation_lines = [ln for ln in res['stdout'].splitlines() if ln.startswith('VIOLATION')]
    return {'exit': res['exit'], 'last': last, 'dump': dumped,
            'violations': [ln[:300] for ln in violation_lines[:2]],
            'stderr': res['stderr'][:400]}


def comparable(observed):
    """The round-49 counter's comparison: exit code plus JSON minus the two sha fields."""
    if observed is None:
        return None
    answer = observed.get('json')
    if isinstance(answer, dict):
        stripped = {k: v for k, v in answer.items() if k not in SHA_KEYS}
        return (observed.get('exit'), json.dumps(stripped, sort_keys=True))
    return (observed.get('exit'), observed.get('raw'))


def single_case(bwrap, run, case, tag, timeout):
    """Run the sandbox's one guard on one dumped case; returns the comparable answer."""
    case_path = os.path.join(run, 'scratch', 'case-%s.json' % tag)
    with open(case_path, 'w', encoding='utf-8') as fh:
        json.dump(case, fh)
    res = run_sandbox(bwrap, run, ['/usr/bin/python3', '-I', '/run/scratch/run-case.py',
                                   '/run/scratch/case-%s.json' % tag, '/run/' + GUARD_NAME],
                      timeout)
    if res['exit'] != 0:
        return None, res
    for line in reversed([ln for ln in res['stdout'].splitlines() if ln.strip()]):
        try:
            return json.loads(line), res
        except ValueError:
            continue
    return None, res


def mutant_text(guard_text, mutant):
    old, new = mutant['old'], mutant['new']
    count = guard_text.count(old)
    if count != 1:
        raise Setup('mutant %s: old text occurs %d times, expected exactly 1' % (mutant['id'], count))
    return guard_text.replace(old, new, 1)


def load_panel(path, guard_bytes, panel_sha):
    with open(path, 'rb') as fh:
        raw = fh.read()
    if panel_sha and sha256(raw) != panel_sha:
        raise Setup('panel sha256 %s != expected %s' % (sha256(raw), panel_sha))
    panel = json.loads(raw.decode('utf-8'))
    if panel.get('target_sha256') != sha256(guard_bytes):
        raise Setup('panel target_sha256 %r != guard sha at REV %s'
                    % (panel.get('target_sha256'), sha256(guard_bytes)))
    text = guard_bytes.decode('utf-8')
    for mutant in panel['mutants']:
        if text.count(mutant['old']) != 1:
            raise Setup('mutant %s: old text not unique in the guard at REV' % mutant['id'])
    return panel['mutants'], sha256(raw)


def materialize(lane, rev, work):
    if not re.fullmatch(r'[0-9a-f]{40}', rev or ''):
        raise Setup('--rev must be a full 40-hex commit id')
    top = subprocess.run(['git', '-C', lane, 'rev-parse', '--show-toplevel'], capture_output=True)
    if top.returncode != 0 or top.stdout.decode().strip() != os.path.realpath(lane):
        raise Setup('lane is not a git work tree: %s' % lane)
    guard = blob(lane, rev, GUARD)
    gen = blob(lane, rev, GENERATOR)
    if sha256(guard) != GUARD_SHA:
        raise Setup('guard sha at REV %s != pinned %s' % (sha256(guard), GUARD_SHA))
    if sha256(gen) != GENERATOR_SHA:
        raise Setup('generator sha at REV %s != pinned %s' % (sha256(gen), GENERATOR_SHA))
    os.makedirs(work, exist_ok=True)
    return guard, gen


def classify(bwrap, base, guard_bytes, pristine_bytes, case, tag, timeout):
    """Comparables for one case under the pristine guard and under the guard under test."""
    pristine_run = make_run_dir(base, 'confirm-pristine-%s' % tag, GENERATOR_BYTES,
                                pristine_bytes)
    mutant_run = make_run_dir(base, 'confirm-guard-%s' % tag, GENERATOR_BYTES, guard_bytes)
    a, ra = single_case(bwrap, pristine_run, case, 'p', timeout)
    b, rb = single_case(bwrap, mutant_run, case, 'm', timeout)
    return comparable(a), comparable(b), {'pristine_exit': ra['exit'], 'guard_exit': rb['exit']}


def run_panel(lane, rev, panel_path, panel_sha, work, seed, cases, timeout, bwrap, version):
    guard_bytes, gen_bytes = materialize(lane, rev, work)
    global GENERATOR_BYTES
    GENERATOR_BYTES = gen_bytes
    mutants, panel_digest = load_panel(panel_path, guard_bytes, panel_sha)
    receipt = {'schema': 'tameshi-r50-sandboxed-confirm-v1', 'seat': 'T50ExecSuccC2',
               'rev': rev, 'lane': os.path.realpath(lane), 'panel': panel_path,
               'panel_sha256': panel_digest,
               'guard_sha256': sha256(guard_bytes), 'generator_sha256': sha256(gen_bytes),
               'seed': seed, 'cases': cases,
               'bwrap': {'path': bwrap, 'version': version},
               'binds': binds(), 'pristine': None, 'negative_control': {}, 'mutants': []}
    pristine_run = make_run_dir(work, 'pristine', gen_bytes, guard_bytes)
    pristine = generator_run(bwrap, pristine_run, 'pristine', seed, cases, timeout)
    pr_probe = probe(bwrap, pristine_run, lane, sha256(guard_bytes))
    indices = [c.get('index') for c in pristine['dump'] or []]
    pristine_ok = (pristine['exit'] == 0 and pristine['last'] is not None
                   and int(pristine['last'].group(1)) == cases
                   and int(pristine['last'].group(2)) == 0
                   and pristine['last'].group(3) == 'none'
                   and indices == list(range(cases)))
    receipt['pristine'] = {'exit': pristine['exit'],
                           'cases': int(pristine['last'].group(1)) if pristine['last'] else None,
                           'violations': int(pristine['last'].group(2)) if pristine['last'] else None,
                           'dump_cases': len(pristine['dump'] or []),
                           'ok': pristine_ok, 'probe': pr_probe,
                           'violations_lines': pristine['violations'],
                           'stderr': pristine['stderr']}
    if not pristine_ok:
        raise Setup('baseline leg is not green: %r' % receipt['pristine'])
    if not pr_probe['ok']:
        raise Setup('baseline probe failed: %r' % pr_probe)

    confirmed = 0
    for mutant in mutants:
        text = mutant_text(guard_bytes.decode('utf-8'), mutant)
        mbytes = text.encode('utf-8')
        if sha256(mbytes) == sha256(guard_bytes):
            raise Setup('mutant %s does not change the guard' % mutant['id'])
        run = make_run_dir(work, mutant['id'], gen_bytes, mbytes)
        pr = probe(bwrap, run, lane, sha256(mbytes))
        gen = generator_run(bwrap, run, mutant['id'], seed, cases, timeout)
        entry = {'id': mutant['id'], 'name': mutant['name'],
                 'guard_sha256': sha256(mbytes),
                 'generator_exit': gen['exit'],
                 'generator_cases': int(gen['last'].group(1)) if gen['last'] else None,
                 'generator_violations': int(gen['last'].group(2)) if gen['last'] else None,
                 'counterexample': None, 'status': 'unconfirmed', 'detail': '',
                 'probe': pr, 'violations_lines': gen['violations'],
                 'generator_stderr': gen['stderr']}
        if not pr['ok']:
            entry['detail'] = 'sandbox probe failed: %r' % pr
        elif gen['exit'] not in (0, 1):
            entry['detail'] = 'generator error (exit %s): %s' % (gen['exit'], gen['stderr'][:160])
        elif gen['exit'] == 0:
            entry['detail'] = 'no violation inside the sandbox (generator exit 0)'
        else:
            index = int(gen['last'].group(3)) if gen['last'] and gen['last'].group(3) != 'none' else None
            entry['counterexample'] = index
            dumped = [c for c in (gen['dump'] or []) if c.get('index') == index]
            if index is None or len(dumped) != 1:
                entry['detail'] = 'counterexample %r is not exactly one dumped case' % (index,)
            else:
                a, b, exits = classify(bwrap, work, mbytes, guard_bytes, dumped[0],
                                       mutant['id'], timeout)
                entry['confirmation'] = dict(exits, pristine=a, guard=b, differ=a != b)
                if a != b:
                    entry['status'] = 'confirmed'
                    entry['detail'] = 'guards differ on the counterexample'
                    confirmed += 1
                else:
                    entry['detail'] = 'guards agree on the counterexample (differential blind spot)'
        receipt['mutants'].append(entry)
        print('MUTANT %s %-24s status=%-11s generator_exit=%s cases=%s counterexample=%s probe_ok=%s'
              % (entry['id'], entry['name'], entry['status'], entry['generator_exit'],
                 entry['generator_cases'], entry['counterexample'], str(entry['probe']['ok']).lower()))

    receipt['summary'] = {'mutants': len(receipt['mutants']), 'confirmed': confirmed,
                          'unconfirmed': len(receipt['mutants']) - confirmed,
                          'probes_ok': all(m['probe']['ok'] for m in receipt['mutants'])}
    receipt['negative_control'] = {
        'probe': 'run/scratch/probe.py, executed inside the same namespace as each generator run',
        'checks': ['the lane guard path cannot be opened',
                   'the lane panel path cannot be opened',
                   'there is no /home',
                   'exactly one file named staged-id-guard.py is visible, sha pinned to the guard '
                   'under test (so a pristine guard would show up as a second file or a wrong sha)',
                   'git in the lane fails (the lane is not a path in the namespace)'],
        'baseline': pr_probe,
        'per_mutant': {m['id']: m['probe']['ok'] for m in receipt['mutants']},
        'all_ok': bool(pr_probe['ok'] and all(m['probe']['ok'] for m in receipt['mutants']))}
    receipt['ok'] = (receipt['negative_control']['all_ok'] and pristine_ok
                     and len(receipt['mutants']) == len(mutants))
    print('SANDBOXED_CONFIRM: bwrap=%s rev=%s guard_sha=%s generator_sha=%s seed=%d cases=%d '
          'baseline_exit=%s confirmed=%d/%d unconfirmed=%d probes_ok=%s ok=%s'
          % (version, rev, sha256(guard_bytes), sha256(gen_bytes), seed, cases,
             pristine['exit'], confirmed, len(receipt['mutants']),
             len(receipt['mutants']) - confirmed,
             str(receipt['summary']['probes_ok']).lower(), str(receipt['ok']).lower()))
    return receipt


def selftest(work, timeout):
    """End to end on a tiny fixture: 2 cases, a 12-line fixture guard, one probe per leg."""
    bwrap, version = bwrap_binary()
    checks = []

    def check(name, ok, detail=''):
        checks.append({'name': name, 'ok': bool(ok), 'detail': detail})
        print('SELFTEST check=%-28s ok=%s%s'
              % (name, str(bool(ok)).lower(), '' if not detail else ' ' + detail))

    print('SELFTEST bwrap=%s' % version)
    lane = os.path.realpath(args_lane)
    fixture = os.path.join(work, 'fixture')
    flane = os.path.join(fixture, 'lane')
    os.makedirs(os.path.join(flane, 'tools'), exist_ok=True)
    os.makedirs(os.path.join(flane, '.ufo/evidence/round-49/c2'), exist_ok=True)
    guard_bytes, gen_bytes = materialize(lane, args_rev, work)
    with open(os.path.join(flane, GUARD), 'wb') as fh:
        fh.write(guard_bytes)
    with open(os.path.join(flane, GENERATOR), 'wb') as fh:
        fh.write(gen_bytes)
    with open(os.path.join(flane, PANEL), 'w', encoding='utf-8') as fh:
        fh.write('{"fixture": "sentinel; must be invisible inside the sandbox"}\n')
    global GENERATOR_BYTES
    GENERATOR_BYTES = gen_bytes
    check('fixture-lane-guard-on-host', os.path.isfile(os.path.join(flane, GUARD)))

    # leg 1: the pristine guard answers two tiny cases cleanly
    run = make_run_dir(work, 'selftest-pristine', gen_bytes, guard_bytes)
    pr = probe(bwrap, run, flane, sha256(guard_bytes))
    rep = pr['report'] or {}
    check('probe-hides-fixture-lane', pr['ok'],
          'guard_open=%r panel_open=%r home=%r guards=%d'
          % (rep.get('lane_guard_open'), rep.get('lane_panel_open'), rep.get('home_exists'),
             len(rep.get('guards_found') or [])))
    check('probe-sees-one-guard',
          len(rep.get('guards_found') or []) == 1
          and (rep.get('guards_found') or [{}])[0].get('path') == '/run/staged-id-guard.py',
          json.dumps(rep.get('guards_found'))[:160])
    check('probe-lane-git-fails', (rep.get('lane_git') or {}).get('exit') not in (0, None),
          json.dumps(rep.get('lane_git'))[:160])
    leak = probe(bwrap, run, flane, sha256(guard_bytes), extra_binds=(flane,))
    lrep = leak['report'] or {}
    check('probe-detects-bound-lane',
          leak['ok'] is False and (lrep.get('lane_guard_open') or {}).get('opened') is True,
          'leaked_probe_ok=%r guard_open=%r' % (lrep.get('ok'),
                                               (lrep.get('lane_guard_open') or {}).get('opened')))
    gen = generator_run(bwrap, run, 'selftest-pristine', SEED, 2, timeout)
    check('tiny-baseline-exit0', gen['exit'] == 0, 'exit=%s' % gen['exit'])
    check('tiny-baseline-cases2',
          bool(gen['last']) and gen['last'].group(1) == '2' and gen['last'].group(3) == 'none',
          gen['last'].group(0) if gen['last'] else 'no summary line')
    check('tiny-baseline-dump2', len(gen['dump'] or []) == 2)

    # leg 2: a 12-line fixture guard (answers {}) must be caught, and confirmed by comparison
    gross = GROSS_GUARD.encode('utf-8')
    mrun = make_run_dir(work, 'selftest-mutant', gen_bytes, gross)
    mp = probe(bwrap, mrun, flane, sha256(gross))
    check('probe-hides-pristine-guard', mp['ok'],
          json.dumps(mp['report'] or {}, sort_keys=True)[:220])
    mg = generator_run(bwrap, mrun, 'selftest-mutant', SEED, 2, timeout)
    check('tiny-mutant-exit1', mg['exit'] == 1, 'exit=%s' % mg['exit'])
    index = int(mg['last'].group(3)) if mg['last'] and mg['last'].group(3) != 'none' else None
    dumped = [c for c in (mg['dump'] or []) if c.get('index') == index]
    check('tiny-mutant-counterexample-in-dump', index is not None and len(dumped) == 1,
          'index=%r dumped=%d' % (index, len(dumped)))
    if index is not None and len(dumped) == 1:
        a, b, exits = classify(bwrap, work, gross, guard_bytes, dumped[0], 'selftest', timeout)
        check('tiny-confirmation-differs', a is not None and b is not None and a != b,
              'pristine=%r guard=%r' % (a, b))

    # leg 3: the real panel applies cleanly to the real guard at REV
    mutants, digest = load_panel(os.path.join(lane, PANEL), guard_bytes, args_panel_sha)
    applied = 0
    for mutant in mutants:
        text = mutant_text(guard_bytes.decode('utf-8'), mutant)
        applied += int(sha256(text.encode('utf-8')) != sha256(guard_bytes))
    check('panel-applies-12', applied == len(mutants) == 12, 'applied=%d mutants=%d'
          % (applied, len(mutants)))
    check('panel-sha-pinned', digest == PANEL_SHA, digest)

    # leg 4: the classifier's own rules (pure function, no sandbox)
    check('classify-exit0-unconfirmed',
          classify_status(0, None, True) == 'unconfirmed')
    check('classify-equal-unconfirmed',
          classify_status(1, ((0, '{}'), (0, '{}')), True) == 'unconfirmed')
    check('classify-differ-confirmed',
          classify_status(1, ((1, '{"a": 1}'), (0, '{}')), True) == 'confirmed')
    check('classify-no-counterexample-unconfirmed',
          classify_status(1, ((1, '{"a": 1}'), (0, '{}')), False) == 'unconfirmed')

    ok = all(c['ok'] for c in checks)
    print('SELFTEST: checks=%d failed=%d bwrap=%s ok=%s'
          % (len(checks), sum(1 for c in checks if not c['ok']), version, str(ok).lower()))
    return 0 if ok else 1


def classify_status(exit_code, comparable_pair, in_dump):
    """The verdict rule, isolated so the selftest can exercise it without a sandbox."""
    if exit_code != 1 or not in_dump:
        return 'unconfirmed'
    if comparable_pair is None or comparable_pair[0] == comparable_pair[1]:
        return 'unconfirmed'
    return 'confirmed'


GENERATOR_BYTES = b''
args_lane = None
args_rev = REV_DEFAULT
args_panel_sha = PANEL_SHA


def main(argv=None):
    global args_lane, args_rev, args_panel_sha
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--lane', default=lane_default())
    parser.add_argument('--rev', default=REV_DEFAULT)
    parser.add_argument('--panel', default=None)
    parser.add_argument('--panel-sha', default=PANEL_SHA,
                        help="expected panel sha256 ('-' to skip the check)")
    parser.add_argument('--work', default=None)
    parser.add_argument('--out', default=None)
    parser.add_argument('--seed', type=int, default=SEED)
    parser.add_argument('--cases', type=int, default=CASES)
    parser.add_argument('--timeout', type=int, default=1800)
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args(argv)
    args_lane = os.path.abspath(args.lane)
    args_rev = args.rev
    args_panel_sha = '' if args.panel_sha == '-' else args.panel_sha
    panel = args.panel or os.path.join(args_lane, PANEL)
    work = args.work or tempfile.mkdtemp(prefix='sandboxed-confirm-')
    os.makedirs(work, exist_ok=True)
    try:
        if args.selftest:
            return selftest(work, args.timeout)
        bwrap, version = bwrap_binary()
        if args.cases < 1:
            raise Setup('--cases must be at least 1')
        receipt = run_panel(args_lane, args_rev, panel, args_panel_sha, work,
                            args.seed, args.cases, args.timeout, bwrap, version)
        out = args.out or os.path.join(work, 'sandboxed-confirm.json')
        with open(out, 'w', encoding='utf-8') as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
            fh.write('\n')
        print('SANDBOXED_CONFIRM_OUT: %s' % out)
        return 0 if receipt['ok'] else 3
    except Setup as exc:
        print('SANDBOXED_CONFIRM: setup error: %s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
