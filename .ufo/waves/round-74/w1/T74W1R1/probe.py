import contextlib, copy, io, pathlib, subprocess
ROOT = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
base = subprocess.check_output(['git', '-C', ROOT, 'show', '3d6ea1ee:tools/wave-reconcile.py']).decode()
# Independently build the frozen fixture inputs, reproducing the current proposed listing.
arms = '''        arm('arm13-printed-undelimited-refused', 'setup',
            lambda: measure_row(kind='seats', record={'path': 'report.md', 'rev': REV,
                'span': '11 reports', 'printed': 1}))
        arm('arm14-span-not-in-record-refused', 'setup',
            lambda: measure_row(kind='seats', record={'path': 'report.md', 'rev': REV,
                'span': '13 seats', 'printed': 13}))
        arm('arm15-seatreports-top-level-only', 'meet',
            lambda: measure_row(kind='seat_reports', record={'path': 'report.md', 'rev': REV,
                'span': '12 seats, 11 reports', 'printed': 12}))
'''
proposed = base.replace('SELFTEST_ARMS = 12', 'SELFTEST_ARMS = 15')
proposed = proposed.replace("SEAT_FILES = ['%s/T1W1S%02d.md' % ('x', i) for i in range(12)] + ['x/swarm-registry.json']", "SEAT_FILES = ['wave/T1W1S%02d.md' % i for i in range(12)] + ['wave/swarm-registry.json', 'wave/nested/deep.md']")
proposed = proposed.replace('    finally:\n        shutil.rmtree(work', arms + '    finally:\n        shutil.rmtree(work')
span_guard = "    if rec['span'].encode('utf-8') not in raw:\n        raise SetupError('span-not-in-record:%s:%s' % (row['id'], rec['path']))\n"
delim = "    return re.search(r'(?<![0-9])%d(?![0-9])' % value, span) is not None"
depth = "if p.startswith(prefix) and '/' not in p[len(prefix):]"
mutations = {'m2': (delim, '    return True'), 'span': (span_guard, ''), 'W2': (depth, 'if p.startswith(prefix)')}
def load(src):
    ns = {'__name__': 'probe'}
    exec(compile(src, 'wave-reconcile-copy.py', 'exec'), ns)
    return ns
def run(label, src):
    ns = load(src)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = ns['selftest']()
    print('=== %s exit=%s ===' % (label, code))
    print(out.getvalue(), end='')
    return out.getvalue()
run('pristine', base)
for name, (old, new) in mutations.items():
    assert base.count(old) == 1
    run('pristine+' + name, base.replace(old, new))
run('proposed', proposed)
for name, (old, new) in mutations.items():
    assert proposed.count(old) == 1
    run('proposed+' + name, proposed.replace(old, new))
# Every supported kind must bind the span, even without printed on non-count rows.
ns = load(proposed)
blobs, listings = ns['fixture_rows']()
REV = ns['REV']
reader = {'lane': ns['FixtureReader'](blobs, listings)}
def mk(kind, span='13 seats', printed=None):
    rec = {'path': 'report.md', 'rev': REV, 'span': span}
    if printed is not None: rec['printed'] = printed
    return {'id': 'probe-' + kind, 'kind': kind, 'record': rec,
            'wave': {'rev': REV, 'dir': 'wave', 'results': 'results.json'},
            'declaration': {'form': 'spec-items', 'path': 'spec.json', 'rev': REV},
            'named': ['reviewer', 'critic', 'mutation-tester'], 'floor_pct': 25}
for kind in ('seats', 'seat_reports', 'roles', 'attack_share'):
    row = mk(kind, printed=13 if kind in ('seats', 'seat_reports') else None)
    try: print('ABSENT-SPAN %s %r' % (kind, ns['measure'](row, reader)))
    except ns['SetupError'] as exc: print('ABSENT-SPAN %s SetupError:%s' % (kind, exc))
for span in ('11 reports', '12 seats, 11 reports'):
    row = mk('seats', span, 1)
    for label, module in [('guarded', ns), ('m2', load(proposed.replace(delim, '    return True')))]:
        try: print('UNDELIMITED %s %s %r' % (label, span, module['measure'](row, reader)))
        except module['SetupError'] as exc: print('UNDELIMITED %s %s SetupError:%s' % (label, span, exc))
# Demonstrate masked alternative SetupErrors: no evidence that named error is asserted.
run('proposed+wrong-delimited-error', proposed.replace("raise SetupError('printed-not-in-span:%s' % row['id'])", "raise SetupError('unrelated-refusal')"))
run('proposed+wrong-span-error', proposed.replace("raise SetupError('span-not-in-record:%s:%s' % (row['id'], rec['path']))", "raise SetupError('unrelated-refusal')"))
# Show exact detail and the old arm3's unobserved population change.
for label, src in [('pristine', base), ('proposed', proposed), ('W2', proposed.replace(depth, 'if p.startswith(prefix)'))]:
    m = load(src); b, ls = m['fixture_rows'](); rd = {'lane': m['FixtureReader'](b, ls)}
    for printed in (11, 12):
        row = mk('seat_reports', '12 seats, 11 reports', printed)
        print('POPULATION %s printed=%s %r' % (label, printed, m['measure'](row, rd)))
# Selective bypass only on unexercised row kinds survives all 15.
selective = proposed.replace('        _record_claim(row, readers)\n', '        pass  # selective record-binding bypass\n')
run('proposed+noncount-binding-bypass', selective)
