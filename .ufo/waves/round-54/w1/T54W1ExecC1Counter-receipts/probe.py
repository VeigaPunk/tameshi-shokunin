#!/usr/bin/env python3
"""C1 reachability probe (scratch clone only; never touches the lane).

Question: can the frozen round-54 C1 counter reach C1_R54_PASS at a LATER
revision whose only change is ledger ENTRIES (+ their trace receipts under a
single rekey-r54-<c0> dir), with SKILL.md byte-identical to C0?

Method: clone the lane (--shared) into scratch, build such a revision with
entries synthesised from the frozen round-18 gate itself (inputs re-pinned to
their C0 blob shas, one trace receipt per entry), commit it in the clone, then
run the frozen counter with --lane <clone> --rev <synthetic revision>.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
C0 = '59c38109bf119d0e9d4f878644a82babc937bc1e'
REKEY = '.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
GITC = ['-c', 'user.name=c1-probe', '-c', 'user.email=c1-probe@example.invalid',
        '-c', 'commit.gpgsign=false']


def git(repo, *args, check=True):
    r = subprocess.run(['git', '-C', repo] + list(args), capture_output=True,
                       env=ENV, check=False)
    if check and r.returncode != 0:
        raise SystemExit('git %s failed: %s' % (' '.join(args), r.stderr.decode()))
    return r


def show(repo, rev, path):
    r = git(repo, 'show', '%s:%s' % (rev, path), check=False)
    return r.stdout if r.returncode == 0 else None


def main():
    clone = sys.argv[1]
    top = git(clone, 'rev-parse', '--show-toplevel').stdout.decode().strip()
    assert Path(top).resolve() == Path(clone).resolve(), (top, clone)
    mod_spec = importlib.util.spec_from_file_location(
        'r18probe', os.path.join(clone, '.ufo/evidence/round-18/measure.py'))
    r18 = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(r18)

    skill = show(clone, C0, 'SKILL.md')
    ledger_raw = show(clone, C0, LEDGER)
    sections = r18.sectionize(skill)
    cr = r18.coldread(clone, C0, skill, ledger_raw, strict=True, explain=True)
    lost = [s for s in cr['sections'] if not s['credited']]
    credited_starts = {s['start'] for s in cr['sections'] if s['credited']}
    print('C0 sections=%d credited=%d lost=%d score_not_checked_here'
          % (len(sections), cr['sections_covered'], len(lost)))

    ledger = json.loads(ledger_raw.decode('utf-8', 'surrogateescape'))
    entries = ledger['entries']
    by_sha, by_head = {}, {}
    for e in entries:
        if not isinstance(e, dict):
            continue
        if isinstance(e.get('sha256'), str):
            by_sha.setdefault(e['sha256'], []).append(e)
        if isinstance(e.get('heading'), str):
            by_head.setdefault(e['heading'], []).append(e)

    skill_sha = hashlib.sha256(skill).hexdigest()
    new_entries = []
    new_files = {}
    for sec in sections:
        if sec['start'] in credited_starts:
            continue
        heads = by_sha.get(sec['sha256']) or by_head.get(sec['heading'], [])
        paths = set()
        for e in heads:
            for p in (e.get('inputs') or {}):
                if p in r18.IGNORED_INPUTS:
                    continue
                paths.add(p)
        if not paths:
            paths = {'corpus/SOURCES.md'}
        pins = {}
        for p in sorted(paths):
            data = r18.blob(clone, C0, p)
            if data is None:
                continue
            pins[p] = hashlib.sha256(data).hexdigest()
        slug = sec['heading'].strip('# ').strip() or 'preamble'
        slug = ''.join(c if c.isalnum() else '-' for c in slug)[:48].strip('-')
        trace = '%s/traces/%s/1.json' % (REKEY, slug)
        receipt = {
            'schema': r18.TRACE_SCHEMA,
            'argv': ['git', 'show', '%s:%s' % (C0, sorted(pins)[0])],
            'cwd': '.',
            'root': clone,
            'rev': C0,
            'exit': 0,
            'inputs': pins,
            'external': {},
            'live_lane_reads': {},
        }
        new_files[trace] = (json.dumps(receipt, indent=2) + '\n').encode()
        new_entries.append({
            'skill_sha256': skill_sha,
            'start': sec['start'],
            'end': sec['end'],
            'heading': sec['heading'],
            'sha256': sec['sha256'],
            'class': 'record',
            'verdict': 'verified-record',
            'blocking_gaps': 0,
            'wrong_expectations': 0,
            'minor_gaps': 0,
            'commands_executed_count': 1,
            'read_rev': C0,
            'inputs': pins,
            'external_inputs': {},
            'traces': [trace],
            'seats': ['T54W1ExecC1Counter'],
            'reports': [],
            'probe': 'c1-reachability-fixture: synthetic entry, not a reader claim',
        })
    print('probe entries=%d traces=%d' % (len(new_entries), len(new_files)))

    ledger['entries'] = entries + new_entries
    Path(clone, LEDGER).write_text(json.dumps(ledger, indent=2) + '\n', 'utf-8')
    for rel, data in new_files.items():
        target = Path(clone, rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    git(clone, 'add', '-A')
    git(clone, *GITC, 'commit', '-q', '-m',
        'c1-probe: later revision — ledger entries + rekey traces only (SKILL.md byte-identical to C0)')
    rev = git(clone, 'rev-parse', 'HEAD').stdout.decode().strip()
    print('PROBE_REV %s' % rev)
    print('SKILL_SHA_AT_PROBE %s' % hashlib.sha256(show(clone, rev, 'SKILL.md')).hexdigest())
    print('SKILL_SHA_AT_C0    %s' % skill_sha)

    # entries-only measurement: the frozen selector at the probe revision
    r = subprocess.run([sys.executable,
                        os.path.join(clone, '.ufo/evidence/round-21/coldread/measure.py'),
                        '--repo', clone, '--rev', rev],
                       capture_output=True, env=ENV)
    out = json.loads(r.stdout.decode())
    print('selector covered=%s score=%s'
          % (out['coldread']['sections_covered'], out['calibration_restraint_score']))
    bad = [s for s in out['coldread']['sections'] if not s['credited']]
    print('selector still-lost=%d' % len(bad))
    for s in bad[:5]:
        print('  STILL_LOST %s | %s' % (s['heading'][:50], s['reason'][:120]))
    return rev


if __name__ == '__main__':
    main()
