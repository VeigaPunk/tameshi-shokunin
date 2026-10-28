#!/usr/bin/env python3
"""Round-54 w1 dry-run binder, second receipt: classify each of the 23 C0-lost
headings against the ledger at C0 and against the emitted input map.

Prints one line per heading:
  heading(56) start-end sha_hit=.. map=.. eff=.. uns=r/e lastfail=n -> verdict
plus a Counter of verdicts. Reads git objects only; writes nothing.
"""
import collections
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
C0 = '59c38109bf119d0e9d4f878644a82babc937bc1e'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
HEADINGS = '.ufo/evidence/round-54/c1/lost-headings-at-c0.json'
MAP = '.ufo/waves/round-54/w1/T54W1ExecDryBinder-input-map.json'
IGNORED = frozenset(('SKILL.md', '.ufo/evidence/round-17/coldread/ledger.json',
                     '.ufo/evidence/round-21/coldread/ledger.json'))


def git(*args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return subprocess.run(['git', '-C', LANE] + list(args), env=env,
                          capture_output=True, check=False)


def load_r18():
    src = git('show', C0 + ':.ufo/evidence/round-18/measure.py').stdout
    fd, path = tempfile.mkstemp(suffix='.py', dir=os.environ.get('TMPDIR'))
    with os.fdopen(fd, 'wb') as fh:
        fh.write(src)
    try:
        spec = importlib.util.spec_from_file_location('r54_r18_classify', path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    finally:
        os.unlink(path)


def main():
    r18 = load_r18()
    skill = git('show', C0 + ':SKILL.md').stdout
    sections = {s['heading']: s for s in r18.sectionize(skill)}
    entries = [e for e in json.loads(git('show', C0 + ':' + LEDGER).stdout
                                     .decode('utf-8', 'surrogateescape'))['entries']
               if isinstance(e, dict)]
    headings = json.load(open(os.path.join(LANE, HEADINGS)))
    emitted = {o['heading']: o for o in json.load(open(os.path.join(LANE, MAP)))}
    cache = {}

    def blob(p):
        if p not in cache:
            r = git('show', '%s:%s' % (C0, p))
            cache[p] = r.stdout if r.returncode == 0 else None
        return cache[p]

    def nfail(inp):
        n = 0
        for p, v in (inp or {}).items():
            if p in IGNORED:
                continue
            data = blob(p)
            if data is None or hashlib.sha256(data).hexdigest() != v:
                n += 1
        return n

    counts = collections.Counter()
    for h in headings:
        sec = sections[h]
        o = emitted[h]
        prior = [e for e in entries if e.get('heading') == h]
        matched = [e for e in prior if e.get('sha256') == sec['sha256']]
        last = prior[-1]
        eff = len([p for p in o['inputs'] if p not in IGNORED])
        effun = len([p for p in o['unstable'] if p not in IGNORED])
        sha_hit = bool(matched)
        if not sha_hit:
            verdict = 'section-sha-drift'
        elif any(nfail(e.get('inputs')) > 0 for e in matched):
            verdict = 'input-drift'
        else:
            verdict = 'credited-by-existing-entry'
        counts[verdict] += 1
        print('%-56s %5d-%-5d sha_hit=%-5s map=%5d eff=%5d uns=%2d/%2d '
              'lastfail=%2d -> %s'
              % (h[:56], sec['start'], sec['end'], sha_hit, len(o['inputs']),
                 eff, len(o['unstable']), effun, nfail(last.get('inputs')),
                 verdict))
    print(counts)
    return 0


if __name__ == '__main__':
    sys.exit(main())
