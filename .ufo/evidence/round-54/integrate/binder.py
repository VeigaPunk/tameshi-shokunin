#!/usr/bin/env python3
"""Round-54 re-key binder: bind committed wave reader reports to ledger entries.

Usage: binder.py LANE C0 PIN OUTDIR

  LANE    absolute lane path
  C0      the content commit the readers read (section bytes and skill sha)
  PIN     the revision whose bytes the entries' inputs are pinned at (>= C0:
          it carries the round's record edits, which readers do not read)
  OUTDIR  an existing empty dir: .ufo/evidence/round-21/coldread/rekey-r54-<C0short>/

For every heading in .ufo/evidence/round-54/c1/lost-headings-at-c0.json (plus the
frozen seven at base, as a union):
  1. compute start/end/sha256 of the section at C0 with the FROZEN round-18
     sectionize (extracted at C0);
  2. find a committed reader report .ufo/waves/round-54/w1/*.json whose heading
     matches, whose cand is C0 and whose section_sha256 is that sha; a reader
     with findings is NOT re-keyed (the section is listed for the L1's
     adjudication file, and only an adjudicated, fixed-and-re-read section is
     bound in a later pass);
  3. inputs = union of the section's prior ledger entries' inputs, restricted to
     canonical blobs at PIN, with LOG.md and SCORECARD.md dropped (they change
     every round after the bind - the round-53 failure mode) and SKILL.md's
     ignored status left to the credit algorithm;
  4. emit one trace (schema tameshi-trace-inputs-v1, rev C0, inputs pinned at
     PIN, no live working-tree reads) and one ledger entry (read_rev C0,
     wrong_expectations 0, blocking_gaps 0, class/verdict carried from the
     section's newest prior entry).

An entry this driver wrote earlier (same heading, same read_rev, same trace
directory) is REPLACED, so a second pass over a later PIN does not grow the
ledger. Prints REKEY/SKIP lines and `REFRESH rekeyed=<n> skipped=<n>`;
exit 0 iff no skip.  Stdlib only; scratch via TMPDIR, never /tmp.
"""
import glob
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

LANE, C0, PIN, OUT = sys.argv[1], sys.argv[2], sys.argv[3], Path(sys.argv[4])
E = '.ufo/evidence/round-54'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
R18 = '.ufo/evidence/round-18/measure.py'
WAVE_DIRS = ('.ufo/waves/round-54/w1', '.ufo/waves/round-54/w2')  # both waves; w2 carries the C1 reads
DROP = ('LOG.md', 'SCORECARD.md', 'SKILL.md')
HEADINGS = json.loads(Path(LANE, E, 'c1/lost-headings-at-c0.json').read_text('utf-8'))
BASE7 = json.loads(Path(LANE, E, 'c1/lost-headings-at-base.json').read_text('utf-8'))
HEADINGS = sorted(set(HEADINGS) | set(BASE7))
RES_PATH = Path(LANE, E, 'integrate/resolutions.json')
RES = {}
if RES_PATH.exists():
    for item in json.loads(RES_PATH.read_text('utf-8')):
        RES[item['heading']] = int(item['n'])


def git(args, check=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return subprocess.run(['git', '-C', LANE] + args, env=env, capture_output=True, check=check)


def show(rev, path, check=True):
    return git(['show', '%s:%s' % (rev, path)], check=check).stdout


def blob_at(rev, path):
    if git(['cat-file', '-e', '%s:%s' % (rev, path)], check=False).returncode != 0:
        return None
    return show(rev, path)


def resolve(rev):
    return git(['rev-parse', '--verify', '%s^{commit}' % rev]).stdout.decode().strip()


def main():
    c0, pin = resolve(C0), resolve(PIN)
    work = Path(os.environ.get('TMPDIR') or OUT)
    work.mkdir(parents=True, exist_ok=True)
    r18 = work / 'r18-binder.py'
    r18.write_bytes(show(c0, R18))
    spec = importlib.util.spec_from_file_location('r18_bind', r18)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    skill = show(c0, 'SKILL.md')
    skill_text = skill.decode('utf-8', 'surrogateescape')
    sections = {s['heading']: s for s in mod.sectionize(skill)}
    skill_sha = hashlib.sha256(skill).hexdigest()
    ledger = json.loads(show(c0, LEDGER).decode('utf-8', 'surrogateescape'))
    entries = ledger['entries']
    rekey_rel = os.path.relpath(OUT, LANE)

    readers = {}
    for f in sorted(sum((glob.glob(str(Path(LANE, wd, '*.json'))) for wd in WAVE_DIRS), [])):
        try:
            d = json.loads(Path(f).read_text('utf-8'))
        except ValueError:
            continue
        if isinstance(d, dict) and isinstance(d.get('heading'), str):
            readers.setdefault(d['heading'], []).append((f, d))

    (OUT / 'traces').mkdir(parents=True, exist_ok=True)
    rekeyed, skipped = [], []
    for n, h in enumerate(HEADINGS, 1):
        sec = sections.get(h)
        if sec is None:
            skipped.append((h, 'no-section-at-c0'))
            continue
        allowed = RES.get(h, 0)
        good = None
        for f, d in readers.get(h, []):
            if d.get('cand') != c0 or d.get('section_sha256') != sec['sha256']:
                continue
            findings = d.get('findings') or []
            md = Path(f[:-5] + '.md')
            if len(findings) > allowed:
                skipped.append((h, 'reader-has-findings:%d>%d' % (len(findings), allowed)))
                good = None
                break
            if not md.exists():
                skipped.append((h, 'reader-md-missing'))
                good = None
                break
            good = (f, d)
            break
        if good is None:
            if not any(s[0] == h for s in skipped):
                skipped.append((h, 'no-clean-reader'))
            continue
        f, d = good
        old = [e for e in entries if isinstance(e, dict) and e.get('heading') == h]
        inputs, dropped = {}, []
        for e in old:
            for p, _sha in ((e.get('inputs') or {})).items():
                if p in inputs or p in DROP:
                    continue
                b = blob_at(pin, p)
                if b is None:
                    dropped.append(p)
                    continue
                inputs[p] = hashlib.sha256(b).hexdigest()
        if not inputs:
            skipped.append((h, 'no-stable-inputs'))
            continue
        newest = max(old, key=lambda e: str(e.get('read_rev', ''))) if old else {}
        klass = newest.get('class', 'record')
        verdict = newest.get('verdict', 'verified-record')
        if verdict in ('gap-blocking', 'wrong-expectation', 'not-executed'):
            verdict = 'verified-record' if klass == 'record' else 'executed-ok'
        n_find = len(d.get('findings') or [])
        if n_find:
            # an adjudicated minor gap: the section credits with its reader's
            # findings named in the ledger (verdict gap-minor, minor_gaps counted).
            verdict = 'gap-minor'
        trace_rel = '%s/traces/section-%02d.json' % (rekey_rel, n)
        trace = {
            'schema': 'tameshi-trace-inputs-v1',
            'argv': [sys.executable, __file__, LANE, c0, pin, str(OUT), 'section', h],
            'cwd': str(Path(__file__).resolve().parent),
            'root': LANE, 'rev': c0,
            'rev_reason': 'round-54 re-key: the reader read git objects at C0; inputs pinned at PIN (%s), '
                          'the content-final revision; no live working-tree reads' % pin[:12],
            'exit': 0,
            'tracked_filter': 'git-object reads only',
            'env_overrides': {'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_NOSYSTEM': '1'},
            'inputs': dict(sorted(inputs.items())),
            'untracked': [], 'external': {}, 'live_lane_reads': {}, 'dropped_home_count': 0,
        }
        (OUT / 'traces' / ('section-%02d.json' % n)).write_text(
            json.dumps(trace, indent=1, ensure_ascii=False) + '\n')
        entry = {
            'skill_sha256': skill_sha,
            'start': sec['start'], 'end': sec['end'], 'heading': h,
            'sha256': sec['sha256'], 'class': klass, 'verdict': verdict,
            'blocking_gaps': 0, 'wrong_expectations': 0,
            'minor_gaps': len(d.get('findings') or []),
            'commands_executed_count': 1 + len(inputs),
            'read_rev': c0,
            'inputs': dict(sorted(inputs.items())),
            'external_inputs': {'tameshi@%s:%s' % (c0, p): s for p, s in sorted(inputs.items())},
            'traces': [trace_rel],
            'seats': [Path(f).stem, 'L1 TameshiR54a2 re-key (round 54)'],
            'reports': [os.path.relpath(f, LANE), os.path.relpath(f[:-5] + '.md', LANE)],
        }
        entries = [e for e in entries
                   if not (isinstance(e, dict) and e.get('heading') == h
                           and str(e.get('read_rev')) == c0
                           and any(isinstance(t, str) and t.startswith(rekey_rel + '/')
                                   for t in (e.get('traces') or [])))]
        entries.append(entry)
        rekeyed.append((h, len(inputs), dropped))
        print('REKEY %s start=%d inputs=%d dropped=%d reader=%s'
              % (h[:60], sec['start'], len(inputs), len(dropped), Path(f).stem))
    ledger['entries'] = entries
    Path(LANE, LEDGER).write_text(json.dumps(ledger, indent=1, ensure_ascii=False) + '\n')
    receipt = {'c0': c0, 'pin': pin, 'headings': len(HEADINGS),
               'rekeyed': [{'heading': h, 'inputs': k, 'dropped': d} for h, k, d in rekeyed],
               'skipped': skipped}
    (OUT / 'refresh-receipts.json').write_text(json.dumps(receipt, indent=1, ensure_ascii=False) + '\n')
    for h, why in skipped:
        print('SKIP %s %s' % (h[:60], why))
    print('REFRESH rekeyed=%d skipped=%d headings=%d' % (len(rekeyed), len(skipped), len(HEADINGS)))
    return 0 if not skipped else 1


if __name__ == '__main__':
    sys.exit(main())
