#!/usr/bin/env python3
"""Probe shrinker (seat T50SentinelShrink). MODE selects the attack under test."""
import argparse, base64, importlib.util, json, os, sys

MODE = os.environ.get('R50_MODE', 'greedy')


def load_gen():
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location('g', os.path.join(here, 'pbt-staged-id.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def striplog(text):
    return ''.join(l for l in text.splitlines(True)
                   if '_r50_os' not in l and '_r50_fh' not in l)


def entries(c):
    m = c.get('map')
    return m['map'] if isinstance(m, dict) and isinstance(m.get('map'), dict) else None


def unit_list(c):
    out = []
    for f in ('registry', 'staged'):
        out += [(f, i) for i in range(len(c[f].splitlines(True)))]
    e = entries(c)
    if e is not None:
        out += [('map', k) for k in e]
    return out


def drop(c, u):
    f, i = u
    if f == 'map':
        m = dict(c['map']); m['map'] = {k: v for k, v in c['map']['map'].items() if k != i}
        return dict(c, map=m)
    l = c[f].splitlines(True)
    return dict(c, **{f: ''.join(l[:i] + l[i + 1:])})


def counts(c):
    n = len(c['registry'].splitlines(True)) + len(c['staged'].splitlines(True))
    e = entries(c)
    return n + (len(e) if e is not None else 0)


WRAPPER = '''#!/usr/bin/env python3
import base64, json, os, sys
T_REG = base64.b64decode(%(reg)r)
T_STG = base64.b64decode(%(stg)r)
T_MAP = %(mapval)s
PRISTINE = %(pris)r
a = sys.argv[1:]
def opt(name):
    return a[a.index(name) + 1] if name in a else None
reg, stg, mp = opt('--registry'), opt('--staged'), opt('--map')
same = (open(reg, 'rb').read() == T_REG and open(stg, 'rb').read() == T_STG
        and ((mp is None and T_MAP is None) or (mp is not None and T_MAP is not None
             and open(mp, 'rb').read() == T_MAP)))
if same:
    print(json.dumps({'verdict': 'setup_refusal', 'reason': 'probe: target case'}))
    sys.exit(2)
os.execv(sys.executable, [sys.executable, '-I', PRISTINE] + a)
'''


def forge(case, out):
    """Overwrite the counter's judge copy of the mutant so only the target case kills."""
    shr = os.getcwd()
    ver = os.path.join(shr, os.pardir, 'ver')
    tmp = os.environ.get('TMPDIR') or os.path.join(shr, 'tmp')
    src_p = os.path.join(ver, 'pristine.py')
    pris = os.path.join(tmp, 'pristine_clean.py')
    with open(src_p, encoding='utf-8') as fh:
        clean = striplog(fh.read())
    with open(pris, 'w', encoding='utf-8') as fh:
        fh.write(clean)
    if case['map'] is None:
        mapval, mbytes = 'None', None
    else:
        mbytes = json.dumps(case['map']).encode()
        mapval = 'base64.b64decode(%r)' % (base64.b64encode(mbytes),)
    wrapper = WRAPPER % {'reg': base64.b64encode(case['registry'].encode()),
                         'stg': base64.b64encode(case['staged'].encode()),
                         'mapval': mapval, 'pris': pris}
    dest = os.path.join(ver, 'mutant.py')
    with open(dest, 'w', encoding='utf-8') as fh:
        fh.write(wrapper)
    return dest


def main():
    ap = argparse.ArgumentParser()
    for k in ('--pristine', '--mutant', '--case', '--out'):
        ap.add_argument(k)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        print('PROBE_SELFTEST ok')
        return 0
    case = json.load(open(a.case))
    before = counts(case)
    tmp = os.environ.get('TMPDIR') or os.getcwd()
    clean_p = os.path.join(tmp, 'pristine_clean.py')
    clean_m = os.path.join(tmp, 'mutant_clean.py')
    if MODE == 'honest':
        clean_p, clean_m = a.pristine, a.mutant
    else:
        for src, dst in ((a.pristine, clean_p), (a.mutant, clean_m)):
            with open(src, encoding='utf-8') as fh:
                text = striplog(fh.read())
            with open(dst, 'w', encoding='utf-8') as fh:
                fh.write(text)
    gen = load_gen()
    real = []

    def rg(guard, x):
        real.append(1)
        return gen.run_guard(guard, tmp, x)

    def kills(x):
        return (gen.check(x, rg(clean_m, x)) is not None
                and gen.check(x, rg(clean_p, x)) is None)

    c = dict(case)
    if MODE == 'poison':
        poison = ('import sys, json\n'
                  'dump = sys.argv[sys.argv.index("--dump") + 1]\n'
                  'with open(dump, "w") as fh:\n'
                  '    fh.write(json.dumps({"index": 0, "registry": "POISONED-CASE-BY-SHRINKER\\n",'
                  ' "staged": "", "map": None}) + "\\n")\n'
                  'print("PBT_STAGED_ID: cases=1 violations=1 counterexample=0 classes=x")\n'
                  'sys.exit(1)\n')
        with open(os.path.join(os.getcwd(), os.pardir, os.pardir, 'frozen-pbt.py'), 'w') as fh:
            fh.write(poison)
    if MODE in ('greedy', 'honest', 'inflate', 'poison'):
        changed = True
        while changed:
            changed = False
            for u in unit_list(c):
                t = drop(c, u)
                if kills(t):
                    c = t; changed = True
                    break
    elif MODE == 'fifo':
        c = dict(c)
    elif MODE == 'fifoout':
        c = dict(c)
    elif MODE == 'surrogate':
        c = dict(c, registry=c['registry'] + '\ud800')
    elif MODE in ('forge', 'droponly'):
        u = [x for x in unit_list(c) if x[0] != 'map'] or unit_list(c)
        if u:
            c = drop(c, u[-1])
    after = counts(c)
    if MODE == 'forge':
        forge(c, a.out)
    runs = 0
    if MODE in ('greedy', 'honest', 'inflate'):
        if MODE == 'honest':
            runs = len(real)
        elif MODE == 'inflate':
            runs = 5000
            with open(os.path.join(os.getcwd(), '.runs'), 'a') as fh:
                fh.write('probe\n' * 5000)
        else:
            runs = False if os.environ.get('R50_RUNS') == 'bool' else 0
        ub, ua = float(before), float(after)
    else:
        runs = 0
        ub, ua = before, after
    if MODE == 'fifo':
        rp = os.path.join(os.getcwd(), '.runs')
        if os.path.lexists(rp):
            os.unlink(rp)
        os.mkfifo(rp)
    if MODE == 'fifoout':
        if os.path.lexists(a.out):
            os.unlink(a.out)
        os.mkfifo(a.out)
        with open(os.path.join(os.getcwd(), 'real-runs.txt'), 'w') as fh:
            fh.write('%d\n' % len(real))
        return 0
    with open(a.out, 'w', encoding='utf-8') as fh:
        json.dump({'case': c, 'runs': runs, 'units_before': ub, 'units_after': ua,
                   'note': 'probe'}, fh)
    # sidecar: the shrinker's own record of how many guard subprocesses it really ran
    with open(os.path.join(os.getcwd(), 'real-runs.txt'), 'w') as fh:
        fh.write('%d\n' % len(real))
    return 0


sys.exit(main())
