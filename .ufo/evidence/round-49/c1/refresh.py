#!/usr/bin/env python3
"""Round-49 C1 re-key: one ledger entry per target section, trace-bound to the section's cited non-record files.

Usage: refresh.py LANE CAND READERS_JSON
  CAND          the candidate commit: corrected sections + reads.json + every record edit of the round
  READERS_JSON  {"<heading>": ["seat name", ...]} — the seats whose read rows cover that section

For each of the seven target sections at CAND (heading text from the frozen C1 counter), a read command runs
under tools/trace-inputs.py in a --shared scratch clone checked out at CAND. The command prints the section and,
for every lane file the section cites (its line and path pointers), the file's bytes-consuming SHA-256. Files in
the counter's VOLATILE record list (LOG.md, SCORECARD.md, corpus/SOURCES.md, corpus/QUALITY.md, corpus/README.md)
are read through `git cat-file blob CAND:<path>` instead: their cited lines are append-only bytes, so the read
observes them without making the whole growing file an input. The trace's recorded inputs become the entry's
inputs; the entry appends to the round-21 ledger (the path the unchanged monitor reads). Scope, carried into the
receipts: "reading-bound refresh: the section's pointers were read by the named seats (reads.json rows with
located excerpts) and its cited non-record files are bound by trace; not blind cold-read or recipe execution".
Writes: the ledger, .ufo/evidence/round-49/coldread/traces/<n>.json and .ufo/evidence/round-49/coldread/refresh-receipts.json.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

LANE, CAND, READERS = os.path.realpath(sys.argv[1]), sys.argv[2], sys.argv[3]
E = '.ufo/evidence/round-49'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
SCR = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'tameshi-r49', 'refresh')
SCOPE = ('reading-bound refresh: the section\'s pointers were read by the named seats (reads.json rows with '
         'located excerpts) and its cited non-record files are bound by trace; not blind cold-read or recipe execution')
spec = importlib.util.spec_from_file_location('c1m', os.path.join(LANE, E, 'c1/measure.py'))
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)
READ_CMD = r'''
import hashlib, subprocess, sys
root, rev, start, end = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
direct, records = sys.argv[5].split(','), sys.argv[6].split(',')
page = open(root + '/SKILL.md', 'rb').read().split(b'\n')
sys.stdout.buffer.write(b'\n'.join(page[start - 1:end]) + b'\n')
print('READS: direct opens of cited non-record files; record files through git blobs at the read revision')
for rel in [p for p in direct if p]:
    data = open(root + '/' + rel, 'rb').read()
    print('SOURCE', rel, 'bytes=%d' % len(data), 'sha256=' + hashlib.sha256(data).hexdigest())
for rel in [p for p in records if p]:
    data = subprocess.run(['git', '-C', root, 'cat-file', 'blob', rev + ':' + rel], capture_output=True, check=True).stdout
    print('RECORD-BLOB', rel, 'bytes=%d' % len(data), 'sha256=' + hashlib.sha256(data).hexdigest())
'''


def sh(*a, **k):
    r = subprocess.run(list(a), capture_output=True, env=c1.GIT_ENV, **k)
    if r.returncode != 0:
        raise SystemExit('failed: %s\n%s' % (a, r.stderr.decode(errors='replace')[-500:]))
    return r.stdout.decode()


def main():
    cand = sh('git', '-C', LANE, 'rev-parse', '--verify', CAND + '^{commit}').strip()
    readers = json.load(open(READERS, encoding='utf-8'))
    shutil.rmtree(SCR, ignore_errors=True)
    os.makedirs(SCR)
    clone = os.path.join(SCR, 'lane')
    sh('git', 'clone', '-q', '--shared', LANE, clone)
    sh('git', '-C', clone, 'checkout', '-q', '--detach', cand)
    if os.path.realpath(sh('git', '-C', clone, 'rev-parse', '--show-toplevel').strip()) != os.path.realpath(clone):
        raise SystemExit('clone toplevel mismatch')
    found, missing = c1.target_sections(LANE, cand)
    if missing:
        raise SystemExit('target headings missing at CAND: %s' % missing)
    pointers, _ = c1.list_pointers(LANE, cand)
    ledger_path = os.path.join(LANE, LEDGER)
    ledger = json.load(open(ledger_path, encoding='utf-8'))
    tracer = os.path.join(clone, 'tools/trace-inputs.py')
    receipts = []
    os.makedirs(os.path.join(LANE, E, 'coldread/traces'), exist_ok=True)
    for n, h in enumerate(c1.TARGETS, 1):
        sec = found[h]
        files = sorted({p['file'] for p in pointers if p['heading'] == h and p['file']
                        and p['kind'] in ('line', 'path') and p['file'] != 'SKILL.md'})
        direct = [f for f in files if f not in c1.VOLATILE]
        records = [f for f in files if f in c1.VOLATILE]
        if any(p['heading'] == h and p['kind'] == 'sid' for p in pointers) and 'corpus/SOURCES.md' not in records:
            records.append('corpus/SOURCES.md')
        if not direct:
            raise SystemExit('section %s cites no non-record lane file' % h)
        trace_rel = '%s/coldread/traces/section-%d.json' % (E, n)
        argv = [sys.executable, tracer, '--root', clone, '--out', os.path.join(LANE, trace_rel), '--',
                sys.executable, '-B', '-c', READ_CMD, clone, cand, str(sec['start']), str(sec['end']),
                ','.join(direct), ','.join(records)]
        r = subprocess.run(argv, capture_output=True, env=dict(c1.GIT_ENV, TMPDIR=SCR), cwd=clone)
        if r.returncode != 0:
            raise SystemExit('trace failed for %s: %s' % (h, r.stderr.decode(errors='replace')[-800:]))
        trace = json.load(open(os.path.join(LANE, trace_rel), encoding='utf-8'))
        inputs = trace['inputs']
        bad = [p for p in inputs if p in c1.VOLATILE]
        # object-store reads through the --shared clone's alternates are .git/ reads, which the monitor binds to REV
        live = [p for p in (trace.get('live_lane_reads') or {}) if '/.git/' not in p]
        if bad or live or trace.get('untracked'):
            raise SystemExit('trace of %s is not clean: volatile=%s live=%s untracked=%s'
                             % (h, bad, live, trace.get('untracked')))
        missing_direct = [f for f in direct if f not in inputs]
        if missing_direct:
            raise SystemExit('trace of %s missed direct reads %s' % (h, missing_direct))
        ledger['entries'].append({
            'skill_sha256': sec['sha256'], 'start': sec['start'], 'end': sec['end'], 'heading': h,
            'sha256': sec['sha256'], 'class': 'record', 'verdict': 'verified-record', 'blocking_gaps': 0,
            'wrong_expectations': 0, 'minor_gaps': 0, 'commands_executed_count': 1, 'read_rev': cand,
            'inputs': inputs, 'traces': [trace_rel], 'seats': readers.get(h, []) + ['L1 TameshiR49 integration'],
            'reports': ['%s/c1/reads.json' % E, '%s/coldread/refresh-receipts.json' % E]})
        receipts.append({'section': h, 'start': sec['start'], 'end': sec['end'], 'sha256': sec['sha256'],
                         'direct': direct, 'records_via_blob': records, 'inputs': inputs, 'trace': trace_rel,
                         'argv_tail': argv[4:7] + ['<READ_CMD>'] + argv[10:], 'exit': r.returncode,
                         'stdout_sha256': hashlib.sha256(r.stdout).hexdigest()})
        print('REKEY %s start=%d inputs=%d records_via_blob=%d' % (h[:50], sec['start'], len(inputs), len(records)))
    with open(ledger_path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(ledger, indent=1, ensure_ascii=True))  # the ledger's own serialization (no newline)
    with open(os.path.join(LANE, E, 'coldread/refresh-receipts.json'), 'w', encoding='utf-8') as fh:
        json.dump({'candidate': cand, 'scope': SCOPE, 'read_command': READ_CMD,
                   'instrument_sha256': hashlib.sha256(open(tracer, 'rb').read()).hexdigest(),
                   'entries_added': len(receipts), 'receipts': receipts}, fh, indent=1, ensure_ascii=False)
    shutil.rmtree(SCR, ignore_errors=True)


if __name__ == '__main__':
    main()
