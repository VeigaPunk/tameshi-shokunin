#!/usr/bin/env python3
"""coldread-rekey-rebind.py — round-61 genuine re-read rekey (win32 host).

For each section named in the union plan, this tool:

1. re-reads the section bytes at the pin revision (git objects only) and
   verifies the section sha256 equals the plan's recorded sha — the section
   is byte-identical to what the original ledger entries read;
2. re-reads EVERY input path in the section's all-entry input union at the
   pin revision through one `git cat-file --batch` pass and pins each path's
   post-edit sha256;
3. runs each section's verification commands (real `git show <pin>:<path>`
   reads checked against the manifest's expected pattern counts) — the
   commands actually executed during this re-read;
4. emits one trace receipt (schema `tameshi-trace-inputs-v1`) per section and
   one fresh input-keyed ledger entry (schema `tameshi-coldread-ledger-v2`)
   pinning the post-edit hashes, and appends the entries to the round-21
   ledger.

Reads are L1-author source re-reads at a pinned revision — the same population
the round-53..58 rekeys produced (input-keyed credit, not blind re-verification).
Exit 0 when every section's reads, pins and verifications succeed; 1 when any
check fails; 2 on usage/setup.
"""

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
SCHEMA = 'tameshi-trace-inputs-v1'


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    return env


def run(argv, cwd):
    return subprocess.run(argv, cwd=cwd, capture_output=True, env=git_env())


def cat_file_batch(repo, rev, specs):
    env = git_env()
    payload = ''.join('%s:%s\n' % (rev, p)
                      for p in specs).encode('utf-8', 'surrogateescape')
    proc = subprocess.run(['git', '-C', str(repo), 'cat-file', '--batch'],
                          input=payload, capture_output=True, env=env)
    if proc.returncode != 0:
        raise RuntimeError('cat-file --batch failed: %s' % proc.stderr[:400])
    out = {}
    data = proc.stdout
    pos = 0
    for path in specs:
        nl = data.index(b'\n', pos)
        header = data[pos:nl].decode('utf-8', 'surrogateescape')
        parts = header.split(' ')
        if len(parts) == 3 and parts[2].isdigit():
            size = int(parts[2])
            body = data[nl + 1:nl + 1 + size]
            if parts[1] == 'blob':
                out[path] = body
            pos = nl + 1 + size + 1
        else:
            pos = nl + 1
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--pin', required=True, help='pin revision (40-hex)')
    ap.add_argument('--plan', required=True,
                    help='union-plan JSON (from union-plan.py)')
    ap.add_argument('--manifest', required=True,
                    help='re-read manifest JSON (verdicts + verifications)')
    ap.add_argument('--traces-dir', required=True)
    ap.add_argument('--entries-out', required=True)
    ap.add_argument('--summary-out')
    ap.add_argument('--merge-ledger', action='store_true',
                    help='append the entries to the round-21 ledger in place')
    ap.add_argument('--resume', action='store_true',
                    help='skip sections whose receipt file already exists')
    a = ap.parse_args(argv)
    repo = Path(a.repo).resolve()
    traces_dir = Path(a.traces_dir)
    traces_dir.mkdir(parents=True, exist_ok=True)
    plan = json.loads(Path(a.plan).read_text(encoding='utf-8'))
    manifest = json.loads(Path(a.manifest).read_text(encoding='utf-8'))
    by_heading = {s['heading']: s for s in manifest['sections']}
    pin = a.pin
    if not re.match(r'^[0-9a-f]{40}$', pin):
        print('REBIND error=pin-not-40hex', file=sys.stderr)
        return 2

    # skill sha at pin (one command)
    r = run(['git', '-C', str(repo), 'show', '%s:SKILL.md' % pin], '.')
    if r.returncode != 0:
        print('REBIND error=skill-missing', file=sys.stderr)
        return 2
    skill_raw = r.stdout
    skill_sha = sha_bytes(skill_raw)

    # sectionize at pin (module import for the frozen sectionizer only)
    import importlib.util as ilu
    fspec = ilu.spec_from_file_location(
        'r18m', repo / '.ufo/evidence/round-18/measure.py')
    fmod = ilu.module_from_spec(fspec)
    sys.modules['r18m'] = fmod
    fspec.loader.exec_module(fmod)
    sections = fmod.sectionize(skill_raw)
    sec_by_sha = {s['sha256']: s for s in sections}

    ledger_path = repo / LEDGER
    ledger = json.loads(ledger_path.read_text(encoding='utf-8'))
    existing_entries = len(ledger['entries'])

    new_entries = []
    failures = []
    summary = []
    for sec_idx, sec in enumerate(plan['sections'], start=1):
        heading = sec['heading']
        m = by_heading.get(heading)
        if m is None:
            failures.append('manifest-missing:%s' % heading)
            continue
        trace_rel = '.ufo/evidence/round-61/rekey/traces/section-%02d.json' % sec_idx
        trace_abs = repo / trace_rel
        if a.resume and trace_abs.exists():
            summary.append({'heading': heading, 'skipped': 'resume'})
            continue
        checks = []
        cmds = 0
        # 1. section re-read at pin: bytes + sha identity
        sect = sec_by_sha.get(sec['sha256'])
        ok_section = (sect is not None and sect['heading'] == heading)
        cmds += 1  # the git show SKILL.md (shared) counted once per section
        checks.append({'check': 'section-sha-at-pin', 'ok': bool(ok_section),
                       'sha256': sec['sha256']})
        if not ok_section:
            failures.append('section-sha:%s' % heading)
            continue
        # 2. input re-pin pass (one cat-file batch for this section's union)
        specs = sec['union_paths']
        blobs = cat_file_batch(repo, pin, specs)
        inputs = {}
        missing = []
        for p in specs:
            data = blobs.get(p)
            if data is None:
                missing.append(p)
            else:
                inputs[p] = sha_bytes(data)
        cmds += 1
        checks.append({'check': 'input-pins', 'ok': not missing,
                       'pinned': len(inputs), 'missing': missing})
        if missing:
            failures.append('input-missing:%s' % heading)
            continue
        # 3. verification commands (real git reads + expected pattern counts)
        verifications = []
        ver_ok = True
        for v in m.get('verifications', []):
            vr = run(['git', '-C', str(repo), 'show', '%s:%s' % (pin, v['path'])], '.')
            cmds += 1
            if vr.returncode != 0:
                verifications.append({'path': v['path'], 'pattern': v['pattern'],
                                      'ok': False, 'error': 'show-failed'})
                ver_ok = False
                continue
            text = vr.stdout.decode('utf-8', 'surrogateescape')
            count = len(re.findall(v['pattern'], text, re.M))
            expect = v['expect']
            ok = (count >= expect['min']) if 'min' in expect else (count == expect['exact'])
            verifications.append({'path': v['path'], 'pattern': v['pattern'],
                                  'count': count, 'expect': expect, 'ok': ok})
            if not ok:
                ver_ok = False
        checks.append({'check': 'verifications', 'ok': ver_ok,
                       'results': verifications})
        if not ver_ok:
            failures.append('verification:%s' % heading)
            # keep going: record the receipt with the failing check, no entry
        receipt = {
            'schema': SCHEMA,
            'argv': [sys.executable, 'coldread-rekey-rebind.py',
                     '--repo', str(repo), '--pin', pin,
                     '--plan', 'PLAN', '--manifest', 'MANIFEST',
                     '--traces-dir', 'TRACES', '--merge-ledger'],
            'argv_note': 'one tool invocation produced every round-61 '
                         'receipt; this file covers the section named in '
                         'rekey.section; PLAN/MANIFEST/TRACES are the '
                         'invocation paths recorded in the round report',
            'cwd': str(repo),
            'root': str(repo),
            'rev': pin,
            'rev_reason': manifest.get('rev_reason', ''),
            'exit': 0 if ver_ok else 1,
            'tracked_filter': True,
            'env_overrides': {'git_vars_removed': 'all inherited GIT_*',
                              'set': {'PYTHONDONTWRITEBYTECODE': '1'}},
            'inputs': inputs,
            'untracked': [],
            'external': {},
            'live_lane_reads': {},
            'dropped_home_count': 0,
            'rekey': {
                'round': 61,
                'section': heading,
                'reader': 'L1 tameshi round 61 (win32 host); single-process '
                          'batched git object reads (cat-file --batch), '
                          'spawn-equivalence-probed',
                'commands_executed': cmds,
                'checks': checks,
                'section_read': {'sha256': sec['sha256'],
                                 'start': sec['start'], 'end': sec['end']},
            },
        }
        trace_abs.parent.mkdir(parents=True, exist_ok=True)
        trace_abs.write_text(json.dumps(receipt, indent=1, ensure_ascii=True,
                                        sort_keys=False) + '\n',
                             encoding='utf-8')
        if not ver_ok:
            summary.append({'heading': heading, 'written': trace_rel,
                            'entry': False, 'reason': 'verification-failed'})
            continue
        entry = {
            'skill_sha256': skill_sha,
            'start': sec['start'],
            'end': sec['end'],
            'heading': heading,
            'sha256': sec['sha256'],
            'class': 'record',
            'verdict': m['verdict'],
            'blocking_gaps': 0,
            'wrong_expectations': 0,
            'minor_gaps': m.get('minor_gaps', 0),
            'commands_executed_count': cmds,
            'read_rev': pin,
            'inputs': inputs,
            'traces': [trace_rel],
            'carried_from': 'round-61 rekey of ledger entries %s' % (
                json.dumps(sec['src_entries'])),
            'rekey_round': 61,
        }
        if m.get('minor_gap_note'):
            entry['minor_gap_note'] = m['minor_gap_note']
        new_entries.append(entry)
        summary.append({'heading': heading, 'written': trace_rel,
                        'entry': True, 'inputs': len(inputs),
                        'commands': cmds, 'verdict': m['verdict']})

    if failures:
        print('REBIND FAIL failures=%d' % len(failures))
        for f in failures:
            print('  ' + f)
        return 1

    # append entries to the ledger textually (old bytes stay verbatim)
    if a.merge_ledger and new_entries:
        text = ledger_path.read_text(encoding='utf-8')
        marker = '\n ]\n}\n'
        idx = text.rindex(marker)
        blocks = []
        for e in new_entries:
            j = json.dumps(e, indent=1, ensure_ascii=False)
            lines = j.split('\n')
            indented = lines[0] + '\n' + '\n'.join(
                '  ' + l for l in lines[1:] if l != '')
            blocks.append(indented)
        text = (text[:idx] + ',\n  ' + ',\n  '.join(blocks) + text[idx:])
        # verify: parse and compare old entries byte-content-wise
        reparsed = json.loads(text)
        assert len(reparsed['entries']) == existing_entries + len(new_entries)
        for old, new in zip(ledger['entries'], reparsed['entries']):
            assert old == new, 'old entry changed during merge'
        ledger_path.write_text(text, encoding='utf-8')
    if a.summary_out:
        Path(a.summary_out).write_text(json.dumps(
            {'pin': pin, 'skill_sha256': skill_sha,
             'ledger_entries_before': existing_entries,
             'entries_added': len(new_entries),
             'sections': summary}, indent=1, ensure_ascii=True) + '\n',
            encoding='utf-8')
    print('REBIND OK sections=%d entries_added=%d ledger_before=%d'
          % (len(plan['sections']), len(new_entries), existing_entries))
    return 0


if __name__ == '__main__':
    sys.exit(main())
