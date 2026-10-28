#!/usr/bin/env python3
"""Round-2 of the harness: sharpened laundering arms + per-arm H1/H2 ledger capture."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, '/fast/scratch/hyaku/tameshi-r55/T55W3MutReader')
import run as R

REC = R.REC
H1, H2 = R.H1, R.H2


def keep_md_findings():
    """The .md next to the emptied JSON keeps the two findings it always named."""
    for f in R.W.glob('T55W3FIX*.json'):
        d = json.loads(f.read_text('utf-8'))
        if d.get('heading') != H2 or d.get('findings'):
            continue
        md = Path(str(f)[:-5] + '.md')
        md.write_text('# fixture reader (laundered)\n\nheading: `%s`\ncand: %s\n'
                      'section_sha256: %s\n\n## findings\n- finding A: the section names a cell '
                      'that does not exist -- why A\n- finding B: a value quoted without its '
                      'receipt -- why B\n' % (H2, R.C0, d['section_sha256']), 'utf-8')


def capture(arm, target_headings, env_extra=None):
    R.git('checkout', '--', R.LEDGER)
    shutil.rmtree(R.OUT, ignore_errors=True)
    work = R.S / 'work'
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    before = hashlib.sha256((R.CLONE / R.LEDGER).read_bytes()).hexdigest()
    env = dict(os.environ)
    env['TMPDIR'] = str(work)
    env.pop('GIT_DIR', None)
    p = subprocess.run([sys.executable, str(R.CLONE / '.ufo/evidence/round-55/integrate/binder.py'),
                        str(R.CLONE), R.C0, R.PIN, str(R.OUT)], env=env, cwd=str(R.CLONE),
                       capture_output=True)
    out, err = p.stdout.decode(), p.stderr.decode()
    after_bytes = (R.CLONE / R.LEDGER).read_bytes()
    led = json.loads(after_bytes.decode('utf-8', 'surrogateescape'))
    fresh = {}
    for e in led['entries']:
        if isinstance(e, dict) and e.get('heading') in target_headings \
                and str(e.get('read_rev')) == R.C0:
            fresh.setdefault(e['heading'], []).append(
                {'verdict': e.get('verdict'), 'minor_gaps': e.get('minor_gaps'),
                 'seats': e.get('seats'), 'sha256': e.get('sha256'),
                 'traces': e.get('traces')})
    rec = {'arm': arm, 'exit': p.returncode, 'stdout': out, 'stderr': err,
           'ledger_sha_before': before,
           'ledger_sha_after': hashlib.sha256(after_bytes).hexdigest(),
           'entry_count': len(led['entries']),
           'fresh_entries': fresh}
    (REC / ('%s.json' % arm)).write_text(json.dumps(rec, indent=1, ensure_ascii=False) + '\n', 'utf-8')
    (REC / ('%s.stdout' % arm)).write_text(out, 'utf-8')
    if err:
        (REC / ('%s.stderr' % arm)).write_text(err, 'utf-8')
    tail = out.strip().splitlines()[-1] if out.strip() else '(no stdout)'
    print('[%s] exit=%d %s' % (arm, p.returncode, tail))
    for h, es in fresh.items():
        for e in es:
            print('   BOUND %-58r verdict=%s minor_gaps=%s' % (h[:56], e['verdict'], e['minor_gaps']))
    if err:
        print('   STDERR tail: %s' % err.strip().splitlines()[-1])
    return rec


def main():
    R.setup()
    secs, skill_sha = R.section_shas()
    print('sections=%d skill_sha=%s' % (len(secs), skill_sha))

    # A1b: genuine baseline, both headings captured
    R.write_res([{'heading': H2, 'n': 2}])
    R.build_fixtures(secs, {})
    capture('A1b-baseline-2findings', (H1, H2))

    # A6b: the finding-bearing reader's JSON list emptied, its .md still names both findings
    R.write_res([{'heading': H2, 'n': 2}])
    R.build_fixtures(secs, {H2: 'empty'})
    keep_md_findings()
    capture('A6b-emptied-md-keeps', (H1, H2))

    # A7: emptied list and NO resolutions entry for the heading (nothing left to contradict it)
    R.write_res([])
    R.build_fixtures(secs, {H2: 'empty'})
    keep_md_findings()
    capture('A7-emptied-no-resolution', (H1, H2))

    # A8: control - the same reader with its two findings, no resolutions entry -> refused
    R.write_res([])
    R.build_fixtures(secs, {})
    capture('A8-findings-unadjudicated', (H1, H2))

    R.git('checkout', '--', R.LEDGER)
    R.build_fixtures(secs, {})


if __name__ == '__main__':
    main()
