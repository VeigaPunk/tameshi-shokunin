#!/usr/bin/env python3
"""Round-53 controls, phase B — break-one fixtures against the POST-FIX candidate.

Usage: break-fixtures.py LANE CAND FREEZE WORKDIR
Runs the FROZEN counters (extracted at FREEZE) against scratch clones of the
candidate with exactly one break planted per fixture; every control must print
*_R53_PASS=false.  Phase B complements phase A (control/controls.py) and runs
after the re-key has landed, before wave 2.

Pre-registered:
  CTL_C1_NOTRACE   — candidate with one rekey-r53 trace blob removed -> false
  CTL_C1_BADREADER — candidate with one wave-1 reader JSON's section_sha256
                     corrupted -> false
  CTL_C1_WRONGREV  — candidate with one rekey entry's read_rev altered -> false
  CTL_C2_TMP       — candidate with one dir="/tmp" line re-planted under tools/
                     -> false
  CTL_C2_CR47      — candidate whose registry-check prints a REGISTRY_CHECK
                     verdict line even with TMPDIR missing -> false
Plus the positive probe (expected true, disclosed as non-deciding):
  PROBE_CANDIDATE  — the frozen counters unmodified at CAND -> both true
"""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

LANE = sys.argv[1]
CAND = sys.argv[2]
FREEZE = sys.argv[3]
WORK = Path(sys.argv[4])
WORK.mkdir(parents=True, exist_ok=True)
SCR = WORK / 'break'
if SCR.exists():
    shutil.rmtree(SCR)
SCR.mkdir(parents=True)
os.environ['TMPDIR'] = str(SCR / 'tmp')
(SCR / 'tmp').mkdir()


def git(args, cwd=LANE, check=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return subprocess.run(['git'] + args, cwd=cwd, env=env,
                          capture_output=True, text=True)


def show(rev, path, cwd=LANE):
    return git(['show', '%s:%s' % (rev, path)], cwd=cwd).stdout


results = []


def record(name, ok, observed, expect='false'):
    print('CONTROL %s %s expected=%s %s' % (name, observed[:110], expect,
                                            'pass' if ok else 'FAIL'))
    results.append(ok)


def run_counter(kind, lane_path, rev, workdir):
    src = show(FREEZE, '.ufo/evidence/round-53/%s/measure.py' % kind)
    p = SCR / ('%s-measure.py' % kind)
    p.write_text(src)
    extra = []
    if kind == 'c1':
        lh = SCR / 'lost-headings.json'
        lh.write_text(show(FREEZE, '.ufo/evidence/round-53/c1/lost-headings.json'))
        extra = ['--explain']
    r = subprocess.run([sys.executable, str(p), '--lane', lane_path,
                        '--rev', rev, '--work', str(workdir)] + extra,
                       capture_output=True, text=True, timeout=3600)
    m = re.search(r'%s_R53_PASS=(true|false)' % kind.upper(), r.stdout or '')
    return (m.group(1) if m else 'none'), (r.stdout or '').strip().split('\n')[-1]


def clone_with(name, mutate):
    root = SCR / name
    env = dict(os.environ, GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    subprocess.run(['git', 'clone', '--shared', '-q', LANE, str(root)], env=env,
                   check=True)
    subprocess.run(['git', 'checkout', '-q', CAND], cwd=root, env=env, check=True)
    mutate(root)
    subprocess.run(['git', 'add', '-A'], cwd=root, env=env, check=True)
    if subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=root,
                      env=env).returncode == 0:
        return CAND
    subprocess.run(['git', '-c', 'user.name=fixture', '-c',
                    'user.email=fixture@invalid', 'commit', '-qm', 'break ' + name],
                   cwd=root, env=env, check=True)
    return subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, env=env,
                          capture_output=True, text=True, check=True).stdout.strip()


# discover the rekey dir + one heading at CAND
r = git(['ls-tree', '--name-only', CAND, '.ufo/evidence/round-21/coldread'])
rekey = [n for n in r.stdout.split('\n') if re.fullmatch(r'rekey-r53-[0-9a-f]{12}', n)][0]
c0 = rekey[len('rekey-r53-'):]
headings = json.loads(show(CAND, '.ufo/evidence/round-53/c1/lost-headings.json'))
h0 = headings[0]


def break_notrace(root):
    tr = json.loads(show(CAND, '.ufo/evidence/round-21/coldread/ledger.json'))
    target = None
    for e in tr['entries']:
        if any(t.startswith('.ufo/evidence/round-21/coldread/%s/' % rekey)
               for t in e.get('traces', [])) and e.get('heading') == h0:
            target = e['traces'][0]
            break
    (root / target).unlink()


def break_badreader(root):
    r = git(['ls-tree', '-r', '--name-only', CAND, '.ufo/waves/round-53'])
    f = [n for n in r.stdout.split('\n') if n.endswith('.json') and 'Read' in n][0]
    d = json.loads((root / f).read_text())
    d['section_sha256'] = '0' * 64
    (root / f).write_text(json.dumps(d, indent=1, ensure_ascii=False))


def break_wrongrev(root):
    led = json.loads(show(CAND, '.ufo/evidence/round-21/coldread/ledger.json'))
    for e in led['entries']:
        if any(t.startswith('.ufo/evidence/round-21/coldread/%s/' % rekey)
               for t in e.get('traces', [])):
            e['read_rev'] = 'f' * 40
            break
    (root / '.ufo/evidence/round-21/coldread/ledger.json').write_text(
        json.dumps(led, indent=1, ensure_ascii=False) + '\n')


def break_tmp(root):
    p = root / 'tools' / 'env-diff.py'
    src = p.read_text()
    p.write_text(re.sub(r'(TemporaryDirectory\(prefix="tameshi-r21-envdiff\.",\s*dir=)[^)]+\)',
                        r'\1"/tmp")', src, count=1))


def break_cr47(root):
    p = root / 'tools' / 'registry-check.py'
    src = p.read_text()
    src = src.replace('def selftest():\n    scratch = tempfile.mkdtemp(',
                      'def selftest():\n    print("REGISTRY_CHECK: held=0/0 superseded=0")\n'
                      '    scratch = tempfile.mkdtemp(', 1)
    p.write_text(src)


for name, fn, kind in (
        ('notrace', break_notrace, 'c1'),
        ('badreader', break_badreader, 'c1'),
        ('wrongrev', break_wrongrev, 'c1'),
        ('tmp', break_tmp, 'c2'),
        ('cr47', break_cr47, 'c2')):
    rev = clone_with('fx-' + name, fn)
    verdict, last = run_counter(kind, str(SCR / ('fx-' + name)), rev,
                                SCR / ('w-' + name))
    record('CTL_%s_%s' % (kind.upper(), name.upper()), verdict == 'false',
           'verdict=%s %s' % (verdict, last[-70:]))

for kind in ('c1', 'c2'):
    verdict, last = run_counter(kind, LANE, CAND, SCR / ('probe-%s' % kind))
    record('PROBE_%s_CANDIDATE' % kind.upper(), verdict == 'true',
           'verdict=%s %s' % (verdict, last[-70:]), expect='true')

ok = all(results)
print('CONTROLS_B: total=%d pass=%d' % (len(results), sum(results)))
sys.exit(0 if ok else 1)
