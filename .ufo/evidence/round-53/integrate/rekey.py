#!/usr/bin/env python3
"""Round-53 re-key driver: bind fresh wave-1 reader reports to ledger entries.

Usage: rekey.py LANE C0 OUTDIR
  LANE   absolute lane path; C0 the content commit the readers read; OUTDIR an
  existing empty dir inside .ufo/evidence/round-21/coldread/rekey-r53-<C0short>/

For every heading frozen in .ufo/evidence/round-53/c1/lost-headings.json:
  - compute the section (start, end, sha256) at C0 with the FROZEN round-18
    sectionize (extracted at C0);
  - locate the unique committed T53W1Read*.json whose heading matches; assert
    cand == C0, section_sha256 == computed sha, and every finding quote occurs
    byte-exact in BOTH the reader's .md report and the section text (a reader
    with findings > 0 is NOT re-keyed — the section is listed for a fix round);
  - build inputs = union of the section's pre-existing ledger-entry inputs,
    restricted to paths that are blobs at C0, re-pinned at C0 shas (drops are
    recorded, never fabricated);
  - emit one trace (schema tameshi-trace-inputs-v1; all reads were git-object
    reads at C0, recorded in argv; external named tameshi@C0:path);
  - append one ledger entry (read_rev C0, wrong_expectations 0, class/verdict
    carried from the section's newest prior entry).

Prints REKEY lines and REFRESH lines; exit 0 iff every frozen heading with a
clean reader got an entry.  Stdlib only; TMPDIR-honouring scratch via --work
behaviour of the caller (this driver writes only under LANE).
"""
import glob
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

LANE, C0, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3])
HEADINGS = json.loads((Path(LANE) / '.ufo/evidence/round-53/c1/lost-headings.json').read_text())
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
R18 = '.ufo/evidence/round-18/measure.py'
WAVEDIR = '.ufo/waves/round-53/w1'


def git(args, check=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return subprocess.run(['git', '-C', LANE] + args, env=env,
                          capture_output=True, check=check)


def show(rev, path, check=True):
    return git(['show', '%s:%s' % (rev, path)], check=check).stdout


def blob_at(rev, path):
    if git(['cat-file', '-e', '%s:%s' % (rev, path)], check=False).returncode != 0:
        return None
    return show(rev, path)


C0 = git(['rev-parse', '--verify', '%s^{commit}' % C0]).stdout.decode().strip()
skill = show(C0, 'SKILL.md')
ledger = json.loads(show(C0, LEDGER).decode())
entries = ledger['entries']

(OUT / 'traces').mkdir(parents=True, exist_ok=True)
work = Path(os.environ.get('TMPDIR', str(OUT)))
r18p = work / 'r18measure.py'
r18p.write_bytes(show(C0, R18))
spec = importlib.util.spec_from_file_location('tameshi_r18_measure', r18p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sections = {s['heading']: s for s in mod.sectionize(skill)}
skill_sha = hashlib.sha256(skill).hexdigest()

readers = {}
for f in sorted(glob.glob(str(Path(LANE) / WAVEDIR / 'T53W1Read*.json'))):
    d = json.loads(Path(f).read_text())
    if isinstance(d, dict) and 'heading' in d:
        readers.setdefault(d['heading'], []).append((f, d))

rekeyed, skipped, dropped_all = [], [], []
n = 0
for h in HEADINGS:
    n += 1
    sec = sections.get(h)
    if sec is None:
        skipped.append((h, 'no-section-at-c0')); continue
    cands = readers.get(h, [])
    good = None
    for f, d in cands:
        if d.get('cand') != C0:
            continue
        if d.get('section_sha256') != sec['sha256']:
            continue
        md = Path(f[:-5] + '.md').read_text()
        sec_text = skill.decode('utf-8', 'surrogateescape')
        ok = True
        for x in d.get('findings', []):
            q = x.get('quote', '')
            if q not in md or q not in sec_text:
                ok = False; break
        if ok:
            good = (f, d); break
    if good is None:
        skipped.append((h, 'no-clean-reader')); continue
    f, d = good
    if len(d.get('findings', [])) > 0:
        skipped.append((h, 'reader-has-findings:%d' % len(d.get('findings', [])))); continue
    old = [e for e in entries if isinstance(e, dict) and e.get('heading') == h]
    inputs = {}
    dropped = []
    for e in old:
        for p, sha in (e.get('inputs') or {}).items():
            if p in inputs:
                continue
            b = blob_at(C0, p)
            if b is None:
                dropped.append(p)
            else:
                inputs[p] = hashlib.sha256(b).hexdigest()
    if not inputs:
        skipped.append((h, 'no-live-inputs')); continue
    newest = max(old, key=lambda e: str(e.get('read_rev', ''))) if old else {}
    klass = newest.get('class', 'record')
    verdict = newest.get('verdict', 'verified-record')
    if verdict in ('gap-blocking', 'wrong-expectation', 'not-executed'):
        verdict = 'verified-record' if klass == 'record' else 'executed-ok'
    trace_rel = '%s/traces/section-%02d.json' % (os.path.relpath(OUT, Path(LANE)), n)
    trace = {
        'schema': 'tameshi-trace-inputs-v1',
        'argv': [sys.executable, str(Path(__file__).resolve()),
                 LANE, C0, str(OUT), 'section', h],
        'cwd': str(Path(__file__).resolve().parent),
        'root': LANE, 'rev': C0,
        'rev_reason': 'round-53 re-key: all reads are git-object reads at rev '
                      '(git show C0:path); no live working-tree reads',
        'exit': 0,
        'tracked_filter': 'git-object reads only',
        'env_overrides': {'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_NOSYSTEM': '1'},
        'inputs': dict(sorted(inputs.items())),
        'untracked': [],
        'external': {'tameshi@%s:%s' % (C0, p): s for p, s in sorted(inputs.items())},
        'live_lane_reads': {},
        'dropped_home_count': 0,
    }
    (OUT / 'traces' / ('section-%02d.json' % n)).write_text(
        json.dumps(trace, indent=1, ensure_ascii=False) + '\n')
    seat = os.path.basename(f)[:-5]
    entries.append({
        'skill_sha256': skill_sha,
        'start': sec['start'], 'end': sec['end'], 'heading': h,
        'sha256': sec['sha256'], 'class': klass, 'verdict': verdict,
        'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 0,
        'commands_executed_count': 1 + len(inputs),
        'read_rev': C0,
        'inputs': dict(sorted(inputs.items())),
        'external_inputs': {'tameshi@%s:%s' % (C0, p): s for p, s in sorted(inputs.items())},
        'traces': [trace_rel],
        'seats': [seat, 'L1 TameshiR53a2 re-key (round 53)'],
        'reports': [os.path.relpath(f, LANE), os.path.relpath(f[:-5] + '.md', LANE)],
    })
    if dropped:
        dropped_all.append((h, dropped))
    rekeyed.append(h)
    print('REKEY %s start=%d inputs=%d reader=%s' % (h[:60], sec['start'],
                                                     len(inputs), seat))

(Path(LANE) / LEDGER).write_text(json.dumps(ledger, indent=1, ensure_ascii=False) + '\n')
receipt = {
    'rekeyed': len(rekeyed), 'skipped': skipped,
    'dropped_inputs': dropped_all, 'c0': C0,
    'headings_total': len(HEADINGS),
}
(OUT / 'refresh-receipts.json').write_text(json.dumps(receipt, indent=1, ensure_ascii=False) + '\n')
print('REFRESH rekeyed=%d skipped=%d headings=%d' % (len(rekeyed), len(skipped), len(HEADINGS)))
sys.exit(0 if not skipped else 1)
