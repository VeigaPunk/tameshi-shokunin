#!/usr/bin/env python3
"""Seat T49W2ExecC2Probe: mutant probe of tools/pbt-staged-id.py against the pinned guard.

Mutants are built in scratch from the candidate clone's guard bytes (sha asserted against the
pinned digest) with one exact-string replacement each.  Each mutant is fed to the generator
(seed 4949, 400 cases, the claim's parameters).  A survivor (generator exit 0) gets a hand-made
witness case run through pristine and mutant to prove the difference is real (oracle blind spot)
rather than an equivalent mutation.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

S = '/fast/scratch/hyaku/tameshi-r49/T49W2ExecC2Probe'
CAND = os.path.join(S, 'cand')
GUARD = os.path.join(CAND, 'tools/staged-id-guard.py')
GEN = os.path.join(CAND, 'tools/pbt-staged-id.py')
PINNED = '03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8'
SHA_KEYS = ('registry_sha256', 'staged_sha256')

text = open(GUARD, encoding='utf-8').read()
assert hashlib.sha256(text.encode()).hexdigest() == PINNED, 'guard digest changed'

MUTANTS = [
    ('X1', 'sha256-value', "    result['registry_sha256'] = hashlib.sha256(read_bytes(args.registry)).hexdigest()",
     "    result['registry_sha256'] = hashlib.sha256(read_bytes(args.staged)).hexdigest()"),
    ('X2', 'size-cap', 'MAX_TEXT = 32 * 1024 * 1024', 'MAX_TEXT = 1024 * 1024'),
    ('X3', 'registry_docs-count', "        'registry_docs': len(registry_docs),",
     "        'registry_docs': len(registry),"),
    ('X4', 'registry-doc-first-wins',
     "        if row['document']:\n            registry_docs.setdefault(normalise_document(row['document']), sid)\n    held, unmapped = {}, []",
     "        if row['document']:\n            registry_docs[normalise_document(row['document'])] = sid\n    held, unmapped = {}, []"),
    ('X5', 'en-dash-head', "    head = re.split(r'\\s+[\u2014\u2013]\\s+', source)[0].strip()",
     "    head = re.split(r'\\s+\u2014\\s+', source)[0].strip()"),
    ('X6', 'non-regular-refusal', '    if not stat.S_ISREG(info.st_mode):',
     '    if False and not stat.S_ISREG(info.st_mode):'),
    ('X7', 'cells-floor-KILLCONTROL', '        if len(cells) < 5:', '        if len(cells) < 4:'),
    ('X8', 'map-duplicate-key-refusal', '        if bare in seen:', '        if False and bare in seen:'),
]

mutdir = os.path.join(S, 'mut')
shutil.rmtree(mutdir, ignore_errors=True)
os.makedirs(mutdir)


def env_for():
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    env['TMPDIR'] = os.path.join(S, 'w')
    os.makedirs(env['TMPDIR'], exist_ok=True)
    return env


paths = {}
for mid, name, old, new in MUTANTS:
    n = text.count(old)
    assert n == 1, (mid, n)
    p = os.path.join(mutdir, mid + '.py')
    open(p, 'w', encoding='utf-8').write(text.replace(old, new, 1))
    paths[mid] = p

print('=== generator against each mutant: seed 4949 cases 400 ===')
results = {}
for mid, name, old, new in MUTANTS:
    dump = os.path.join(S, 'w', 'dump-%s.jsonl' % mid)
    t0 = time.monotonic()
    r = subprocess.run([sys.executable, '-I', GEN, '--guard', paths[mid], '--seed', '4949',
                        '--cases', '400', '--dump', dump], capture_output=True, env=env_for(),
                       cwd=CAND, timeout=1800)
    dt = time.monotonic() - t0
    lines = [ln for ln in r.stdout.decode().splitlines() if ln.strip()]
    last = lines[-1] if lines else '<no stdout>'
    viol = [ln for ln in lines if ln.startswith('VIOLATION')]
    results[mid] = (r.returncode, last, viol)
    print('%s %-28s exit=%d wall=%.1fs' % (mid, name, r.returncode, dt))
    print('   last: ' + last)
    for v in viol[:2]:
        print('   ' + v)
    # guard's own selftest on the mutant, for the record
    st = subprocess.run([sys.executable, '-I', paths[mid], '--selftest'], capture_output=True,
                        env=env_for(), timeout=300)
    print('   guard-selftest exit=%d' % st.returncode)


# ------------------------------------------------------------------ witnesses for survivors
def rows(*spec):
    head = ('| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck '
            '| used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n')
    out = head
    for sid, source in spec:
        out += '| %s | %s | docs | A | x | y | z | queued | 2026-10-24 | 180d | - |\n' % (sid, source)
    return out


def run(guard, registry, staged, map_doc=None, path_override=None):
    d = tempfile.mkdtemp(prefix='wit-', dir=env_for()['TMPDIR'])
    try:
        rp = os.path.join(d, 'registry.md')
        sp = os.path.join(d, 'staged.md')
        if path_override is None:
            open(rp, 'w', encoding='utf-8').write(registry)
        else:
            rp = path_override
        open(sp, 'w', encoding='utf-8').write(staged)
        argv = [sys.executable, '-I', guard, '--registry', rp, '--staged', sp]
        if map_doc is not None:
            mp = os.path.join(d, 'map.json')
            open(mp, 'w', encoding='utf-8').write(map_doc if isinstance(map_doc, str)
                                                  else json.dumps(map_doc))
            argv += ['--map', mp]
        argv.append('--json')
        r = subprocess.run(argv, capture_output=True, cwd=d, timeout=60)
        try:
            js = json.loads(r.stdout)
        except ValueError:
            js = None
        return r.returncode, js
    finally:
        shutil.rmtree(d, ignore_errors=True)


def diff(a, b):
    if a[0] != b[0]:
        return 'exit %s vs %s' % (a[0], b[0])
    if a[1] is None or b[1] is None:
        return 'stdout not JSON: %r vs %r' % (a[1], b[1])
    keys = sorted(set(a[1]) | set(b[1]))
    out = []
    for k in keys:
        if a[1].get(k) != b[1].get(k):
            out.append('%s: pristine=%r mutant=%r' % (k, a[1].get(k), b[1].get(k)))
    return '; '.join(out)


BIG_PAD = '# pad\n' + ('x' * 1023 + '\n') * 1200          # ~1.2 MiB, no parseable rows

WITNESSES = {
    'X1': dict(registry=rows(('S001', 'notes/a.md'), ('S002', 'notes/b.md')),
               staged=rows(('S001', 'notes/c.md'))),
    'X2': dict(registry=BIG_PAD + rows(('S001', 'notes/a.md')),
               staged=rows(('S001', 'notes/b.md'))),
    'X3': dict(registry=rows(('S001', 'nothing here')), staged=rows(('S004', 'notes/d.md'))),
    'X4': dict(registry=rows(('S001', 'https://doc.test/paper \u2014 a'),
                             ('S002', 'https://www.doc.test/paper/ \u2014 b')),
               staged=rows(('S002', 'https://doc.test/paper'))),
    'X5': dict(registry=rows(('S001', 'notes/paper-3.md \u2013 note')),
               staged=rows(('S001', 'notes/paper-3.md \u2014 note'))),
    'X6': dict(registry='', staged=rows(('S001', 'notes/a.md')), path_override='/dev/null'),
    'X8': dict(registry=rows(('S002', 'notes/a.md')), staged=rows(('S002', 'notes/b.md')),
               map_doc='{"map": {"S002": "S010", "staged:S002": "S011"}}'),
}

print('\n=== witnesses: pristine vs survivor (differential, sha fields shown) ===')
for mid, w in WITNESSES.items():
    a = run(GUARD, w['registry'], w['staged'], w.get('map_doc'), w.get('path_override'))
    b = run(paths[mid], w['registry'], w['staged'], w.get('map_doc'), w.get('path_override'))
    print('%s pristine_exit=%s mutant_exit=%s' % (mid, a[0], b[0]))
    print('   diff: ' + diff(a, b))
    if a[1] and b[1]:
        print('   pristine sha pair: reg=%s stg=%s' % (a[1].get('registry_sha256', '')[:12],
                                                       a[1].get('staged_sha256', '')[:12]))
        print('   mutant   sha pair: reg=%s stg=%s' % (b[1].get('registry_sha256', '')[:12],
                                                       b[1].get('staged_sha256', '')[:12]))
    print('   pristine json: %s' % json.dumps({k: v for k, v in (a[1] or {}).items()
                                               if k not in SHA_KEYS}, sort_keys=True)[:300])
    print('   mutant   json: %s' % json.dumps({k: v for k, v in (b[1] or {}).items()
                                               if k not in SHA_KEYS}, sort_keys=True)[:300])
