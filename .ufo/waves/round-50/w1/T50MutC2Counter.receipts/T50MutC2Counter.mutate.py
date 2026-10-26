#!/usr/bin/env python3
"""T50MutC2Counter: generate single-edit mutants of the frozen C2 counter and run its selftest on each.

Scratch-only: reads the lane counter once (pristine copy), writes mutants under S/mut,
runs `--selftest --lane LANE --work S/w/<id>` per mutant, logs outputs under S/out.
Never writes to the lane."""
import concurrent.futures as cf
import hashlib
import json
import os
import subprocess
import sys
import time

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
S = '/fast/scratch/hyaku/tameshi-r50/T50MutC2Counter'
PRISTINE = os.path.join(S, 'pristine.py')
OUT = os.path.join(S, 'out')
MUT = os.path.join(S, 'mut')

src = open(PRISTINE, encoding='utf-8').read()

# (id, category, expectation, old, new) -- each old must occur exactly once in the pristine source
MUTANTS = [
    ('m01', 'instrument insertion', 'survive',
     r"""        return '\n'.join(lines[:i]) + '\n' + (INSTRUMENT % tag) + '\n'.join(lines[i:])""",
     r"""        return '\n'.join(lines[:i + 1]) + '\n' + (INSTRUMENT % tag) + '\n'.join(lines[i + 1:])"""),
    ('m02', 'instrument .runs path', 'kill',
     r"""__file__)), '.runs'), 'a') """,
     r"""__file__)), '.runz'), 'a') """),
    ('m03', 'instrument write no-newline', 'kill',
     r"""_r50_fh.write('%s\\n')""",
     r"""_r50_fh.write('%s')"""),
    ('m04', 'units() drops map entries', 'unknown',
     "    return n + (len(entries) if entries is not None else 0)",
     "    return n"),
    ('m05', 'units() off-by-one when map None', 'unknown',
     "(len(entries) if entries is not None else 0)",
     "(len(entries) if entries is not None else 1)"),
    ('m06', 'removals() no-op slice', 'kill',
     r"""yield dict(case, **{field: ''.join(lines[:i] + lines[i + 1:])})""",
     r"""yield dict(case, **{field: ''.join(lines[:i] + lines[i:])})"""),
    ('m07', 'removals() drops map branch', 'survive',
     "    if entries is not None:\n        for key in list(entries):",
     "    if False:\n        for key in list(entries):"),
    ('m08', 'subsequence() arg order swap', 'kill',
     "    it = iter(big)\n    return all(any(x == y for y in it) for x in small)",
     "    it = iter(small)\n    return all(any(x == y for y in it) for x in big)"),
    ('m09', 'is_subcase() skips field check', 'kill',
     "        if not subsequence(s[field].splitlines(), c[field].splitlines()):",
     "        if False:"),
    ('m10', 'Judge.kills order swap', 'kill',
     "        if self.gen.check(case, self.gen.run_guard(self.mutant, self.casedir, case)) is None:\n"
     "            return False\n"
     "        return self.gen.check(case, self.gen.run_guard(self.pristine, self.casedir, case)) is None",
     "        if self.gen.check(case, self.gen.run_guard(self.pristine, self.casedir, case)) is None:\n"
     "            return False\n"
     "        return self.gen.check(case, self.gen.run_guard(self.mutant, self.casedir, case)) is None"),
    ('m11', 'minimality any() -> all()', 'kill',
     "not any(judge.kills(r) for r in removals(s))",
     "not all(judge.kills(r) for r in removals(s))"),
    ('m12', 'minimality drops kills conjunct', 'survive',
     "flags['minimal'] = flags['kills'] and not any(",
     "flags['minimal'] = not any("),
    ('m13', 'cost drops units_before equality', 'survive',
     "and out.get('units_before') == ub and out.get('units_after') == ua)",
     "and out.get('units_after') == ua)"),
    ('m14', 'cost runs == logged+1', 'kill',
     "out.get('runs') == logged and isinstance(",
     "out.get('runs') == logged + 1 and isinstance("),
    ('m15', 'ok threshold N-1 -> N', 'kill',
     "counts['ok_short'] = max(0, (total_mutants - 1) - ok)",
     "counts['ok_short'] = max(0, total_mutants - ok)"),
    ('m16', 'no_reduction < -> <=', 'survive',
     "0 if (ok and after_sum < before_sum) else 1",
     "0 if (ok and after_sum <= before_sum) else 1"),
    ('m17', 'no_reduction drops ok conjunct', 'survive',
     "0 if (ok and after_sum < before_sum) else 1",
     "0 if (after_sum < before_sum) else 1"),
    ('m18', 'records F6 drops word boundary', 'survive',
     r"""re.search(r'\bF6\b', l) and 'held (round 50)' in l""",
     r"""re.search(r'F6', l) and 'held (round 50)' in l"""),
    ('m19', 'records held pin weakened to prefix', 'survive',
     "'held (round 50)' in l",
     "'held (round 5' in l"),
    ('m20', 'records mined check inverted', 'kill',
     "cells[7] == 'mined'",
     "cells[7] != 'mined'"),
    ('m21', 'records opened date changed', 'kill',
     "cells[8] == OPENED",
     "cells[8] == '2026-10-27'"),
    ('m22', 'panel sha check dropped', 'kill',
     "if sha(raw) != pin or not isinstance(doc.get('mutants'), list):",
     "if not isinstance(doc.get('mutants'), list):"),
    ('m23', 'PUBLIC_SHA256 constant changed', 'survive',
     "PUBLIC_SHA256 = 'd6dd2cf38317118b14dfcdc1069b3222e3d4dc65ff05e005fc2b0592ce2eeda1'",
     "PUBLIC_SHA256 = 'd6dd2cf38317118b14dfcdc1069b3222e3d4dc65ff05e005fc2b0592ce2eeda0'"),
    ('m24', 'GUARD_SHA256 constant changed', 'survive',
     "GUARD_SHA256 = '03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8'",
     "GUARD_SHA256 = '03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca9'"),
    ('m25', 'GEN_SHA256 constant changed', 'kill',
     "GEN_SHA256 = '0cbee392a83e4cd6609efa97395a9ae8a64115015cf290e42e9a4ff98bc01f05'",
     "GEN_SHA256 = '0cbee392a83e4cd6609efa97395a9ae8a64115015cf290e42e9a4ff98bc01f06'"),
    ('m26', 'SEED changed 4949 -> 4948', 'unknown',
     "SEED, CASES = '4949', '400'",
     "SEED, CASES = '4948', '400'"),
    ('m27', 'find_case index match inverted', 'kill',
     "            if row.get('index') == index:",
     "            if row.get('index') != index:"),
    ('m28', 'unfound misattributed to panel_invalid', 'survive',
     "            counts['unfound'] += 1",
     "            counts['panel_invalid'] += 1"),
]

manifest = []
for mid, cat, exp, old, new in MUTANTS:
    n = src.count(old)
    if n != 1:
        print('SKIP %s: old string occurs %d times' % (mid, n))
        continue
    msrc = src.replace(old, new)
    p = os.path.join(MUT, mid + '.py')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(msrc)
    manifest.append({'id': mid, 'category': cat, 'expect': exp, 'old': old, 'new': new,
                     'sha256': hashlib.sha256(msrc.encode('utf-8')).hexdigest(),
                     'path': p})
print('generated %d mutants' % len(manifest))


def run_one(m):
    mid = m['id']
    t0 = time.time()
    wd = os.path.join(S, 'w', mid)
    os.makedirs(wd, exist_ok=True)
    try:
        p = subprocess.run([sys.executable, m['path'], '--selftest', '--lane', LANE, '--work', wd],
                           capture_output=True, timeout=1500, env=dict(os.environ, TMPDIR=wd))
        rc, out, err = p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')
    except subprocess.TimeoutExpired as e:
        rc = 124
        out = (e.stdout or b'').decode('utf-8', 'replace')
        err = 'TIMEOUT after 1500s'
    dt = time.time() - t0
    with open(os.path.join(OUT, mid + '.txt'), 'w') as fh:
        fh.write('exit=%d seconds=%.1f\n--- stdout ---\n%s\n--- stderr ---\n%s\n' % (rc, dt, out, err))
    fails = [l.strip() for l in out.split('\n') if 'FAIL' in l]
    return {'id': mid, 'rc': rc, 'seconds': round(dt, 1),
            'verdict': 'SURVIVED' if rc == 0 else 'KILLED', 'failed_cases': fails}


with cf.ThreadPoolExecutor(max_workers=9) as ex:
    results = list(ex.map(run_one, manifest))
with open(os.path.join(S, 'results.json'), 'w') as fh:
    json.dump({'manifest': manifest, 'results': results}, fh, indent=1)
for r in sorted(results, key=lambda r: r['id']):
    print('%s %-8s rc=%-3d %5.1fs %s' % (r['id'], r['verdict'], r['rc'], r['seconds'],
                                         '; '.join(r['failed_cases'])[:160]))
