#!/usr/bin/env python3
"""Round-52 cold-read re-key instrument.

Usage: refresh.py LANE CAND READERS_JSON
READERS_JSON maps each target heading (or '*' fallback) to {"seats": [...],
"reader_files": [lane-relative paths], "findings": [{"quote": ..., "class": ...,
"skill_statement": ...}]}. Finding quotes must occur verbatim in reader files.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
BASE = 'ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4'
MONITOR = '.ufo/evidence/round-21/coldread/measure.py'
MONITOR_IMPL = '.ufo/evidence/round-18/measure.py'
R49 = '.ufo/evidence/round-49/c1/measure.py'
E = '.ufo/evidence/round-52'
READS_DIR = E + '/coldread/reads/'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
SCR = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'tameshi-r52', 'refresh')
SCOPE = ('reading-bound re-key: section pointers and reader findings were read by named wave-2 seats '
         'and their cited non-record files are bound by trace; not blind cold-read or recipe execution')
READ_CMD = r'''
import hashlib, subprocess, sys
root, rev, start, end = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
direct, records, internal = sys.argv[5].split(','), sys.argv[6].split(','), [r for r in sys.argv[7].split(',') if r]
page = open(root + '/SKILL.md', 'rb').read().split(b'\n')
sys.stdout.buffer.write(b'\n'.join(page[start - 1:end]) + b'\n')
print('READS: direct opens of cited non-record files; record files through git blobs at the read revision')
for span in internal:
    s, _, e = span.partition('-')
    sys.stdout.buffer.write(b'INTERNAL-POINTER ' + span.encode() + b'\n')
    sys.stdout.buffer.write(b'\n'.join(page[int(s) - 1:int(e)]) + b'\n')
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


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def run_monitor(clone, rev, tag, work):
    r = subprocess.run([sys.executable, '-B', os.path.join(clone, MONITOR), '--repo', clone, '--rev', rev],
                       capture_output=True, env=dict(c1.GIT_ENV, TMPDIR=work), cwd=work)
    with open(os.path.join(work, 'monitor-%s.json' % tag), 'wb') as fh:
        fh.write(r.stdout)
    if r.returncode != 0:
        raise SystemExit('monitor exit %d at %s: %s' % (r.returncode, tag, r.stderr.decode(errors='replace')[-400:]))
    d = json.loads(r.stdout)
    c = d['coldread']
    return ({'total': c['sections_total'], 'covered': c['sections_covered'],
             'score': d['calibration_restraint_score'], 'strict': d.get('trace_gate') == 'strict'},
            [(s['heading'], s['credited'], s['reason']) for s in c['sections']])


def sections_at(clone, rev):
    impl = c1.load_monitor_module(clone)
    raw = c1.blob(clone, rev, 'SKILL.md')
    if raw is None:
        raise SystemExit('SKILL.md missing at %s' % rev)
    lines = raw.decode('utf-8', 'surrogateescape').split('\n')
    out = {}
    for s in impl.sectionize(raw):
        body = list(lines[s['start'] - 1:s['end']])
        while body and body[-1].strip() == '':
            body.pop()
        if s['heading'] in out:
            raise SystemExit('heading is not a single section at %s: %s' % (rev, s['heading']))
        out[s['heading']] = {'start': s['start'], 'end': s['end'], 'sha256': s['sha256'], 'text': '\n'.join(body)}
    return out


def cited_files(clone, rev, text):
    direct, records, internal = set(), set(), []
    for p in c1.extract(text):
        f, kind, _ranges = c1.resolve(clone, rev, p['token'], p['kind'])
        if f and kind in ('line', 'path'):
            if f == 'SKILL.md':
                continue
            (records if f in c1.VOLATILE else direct).add(f)
        elif p['kind'] == 'line' and p['token'] is None and p['ranges']:
            internal.extend(p['ranges'])
    return sorted(direct), sorted(records), internal


def follow_internal(clone, rev, ranges):
    if not ranges:
        return [], []
    lines = c1.blob(clone, rev, 'SKILL.md').decode('utf-8', 'surrogateescape').split('\n')
    frag = '\n'.join('\n'.join(lines[s - 1:e]) for s, e in ranges if 1 <= s <= e <= len(lines))
    direct, records, _more = cited_files(clone, rev, frag)
    return direct, records


def validate_readers(data, lane, heading):
    if not isinstance(data, dict):
        raise SystemExit('READERS_JSON entry must be an object for section: %s' % heading)
    seats, files, findings = data.get('seats'), data.get('reader_files'), data.get('findings')
    if not isinstance(seats, list) or not seats or not all(isinstance(s, str) and s for s in seats):
        raise SystemExit('READERS_JSON names no reader seats for section: %s' % heading)
    if not isinstance(files, list) or not files or not all(isinstance(f, str) and f for f in files):
        raise SystemExit('READERS_JSON names no reader_files for section: %s' % heading)
    if not isinstance(findings, list):
        raise SystemExit('READERS_JSON findings must be a list for section: %s' % heading)
    texts = []
    root = os.path.realpath(lane)
    for rel in files:
        if os.path.isabs(rel) or '..' in rel.split('/') or not rel.endswith('.md'):
            raise SystemExit('invalid lane-relative reader file: %s' % rel)
        path = os.path.realpath(os.path.join(root, rel))
        if os.path.commonpath((root, path)) != root or not os.path.isfile(path):
            raise SystemExit('reader file missing or outside lane: %s' % rel)
        with open(path, encoding='utf-8') as fh:
            texts.append(fh.read())
    for finding in findings:
        if not isinstance(finding, dict):
            raise SystemExit('finding must be an object for section: %s' % heading)
        quote = finding.get('quote')
        if not isinstance(quote, str) or not quote or not any(quote in text for text in texts):
            raise SystemExit('finding quote is not a verbatim substring of its reader files for %s: %r'
                             % (heading, quote))
        if not isinstance(finding.get('class'), str) or not finding['class']:
            raise SystemExit('finding needs class for section: %s' % heading)
    return {'seats': seats, 'reader_files': files, 'findings': findings}


def main():
    lane = os.path.realpath(sys.argv[1])
    cand = sh('git', '-C', lane, 'rev-parse', '--verify', sys.argv[2] + '^{commit}').strip()
    base = sh('git', '-C', lane, 'rev-parse', '--verify', BASE + '^{commit}').strip()
    readers = json.load(open(sys.argv[3], encoding='utf-8'))
    if not isinstance(readers, dict):
        raise SystemExit('READERS_JSON must be an object keyed by heading')
    tag = 'rekey-' + cand[:8]
    shutil.rmtree(SCR, ignore_errors=True)
    os.makedirs(SCR)
    try:
        clone = os.path.join(SCR, 'lane')
        sh('git', 'clone', '-q', '--shared', lane, clone)
        sh('git', '-C', clone, 'checkout', '-q', '--detach', cand)
        if os.path.realpath(sh('git', '-C', clone, 'rev-parse', '--show-toplevel').strip()) != os.path.realpath(clone):
            raise SystemExit('clone toplevel mismatch')
        work = os.path.join(SCR, 'w')
        os.makedirs(work)
        working = json.load(open(os.path.join(lane, LEDGER), encoding='utf-8'))
        at_cand = c1.blob(clone, cand, LEDGER)
        if at_cand is None or json.loads(at_cand.decode('utf-8', 'surrogateescape')) != working:
            raise SystemExit('working-tree ledger differs from the ledger at CAND')
        mbase, base_rows = run_monitor(clone, base, 'base', work)
        mcand, cand_rows = run_monitor(clone, cand, 'cand', work)
        if not (mbase['strict'] and mcand['strict']):
            raise SystemExit('monitor ran in legacy mode; the round measures strict')
        base_credit = {h: cr for h, cr, _r in base_rows}
        cand_credit = {h: cr for h, cr, _r in cand_rows}
        cand_reason = {h: r for h, _cr, r in cand_rows}
        targets = [h for h, _cr, _r in base_rows if base_credit[h] and not cand_credit.get(h, False)]
        if not targets:
            raise SystemExit('no section lost credit: nothing to re-key')
        for h in targets:
            if h not in cand_credit:
                raise SystemExit('target heading absent at CAND: %s' % h)
        secs = sections_at(clone, cand)
        tracer = os.path.join(clone, 'tools/trace-inputs.py')
        receipt_dir = os.path.join(lane, E, 'coldread', tag)
        os.makedirs(os.path.join(receipt_dir, 'traces'), exist_ok=True)
        receipts = []
        for n, h in enumerate(targets, 1):
            sec = secs[h]
            direct, records, internal = cited_files(clone, cand, sec['text'])
            followed = []
            if not direct:
                direct, more_records = follow_internal(clone, cand, internal)
                records = sorted(set(records) | set(more_records))
                followed = ['%d-%d' % (s, e) for s, e in internal]
                if not direct:
                    raise SystemExit('section %s cites no non-record lane file' % h)
            reader = readers.get(h) or readers.get('*')
            if reader is None:
                raise SystemExit('READERS_JSON names no reader data for section: %s' % h)
            reader = validate_readers(reader, lane, h)
            trace_rel = '%s/coldread/%s/traces/section-%d.json' % (E, tag, n)
            trace_out = os.path.join(lane, trace_rel)
            argv = [sys.executable, tracer, '--root', clone, '--out', trace_out, '--',
                    sys.executable, '-B', '-c', READ_CMD, clone, cand, str(sec['start']), str(sec['end']),
                    ','.join(direct), ','.join(records), ','.join(followed)]
            r = subprocess.run(argv, capture_output=True, env=dict(c1.GIT_ENV, TMPDIR=SCR), cwd=clone)
            if r.returncode != 0:
                raise SystemExit('trace failed for %s: %s' % (h, r.stderr.decode(errors='replace')[-800:]))
            trace = json.load(open(trace_out, encoding='utf-8'))
            inputs = {p: v for p, v in trace['inputs'].items() if p != 'SKILL.md'}
            bad = [p for p in inputs if p in c1.VOLATILE]
            live = [p for p in (trace.get('live_lane_reads') or {}) if '/.git/' not in p]
            missed = [f for f in direct if f not in trace['inputs']]
            if bad or live or trace.get('untracked') or missed:
                raise SystemExit('trace of %s is not clean: volatile=%s live=%s untracked=%s missed=%s'
                                 % (h, bad, live, trace.get('untracked'), missed))
            entry = {'skill_sha256': sec['sha256'], 'start': sec['start'], 'end': sec['end'], 'heading': h,
                     'sha256': sec['sha256'], 'class': 'record', 'verdict': 'verified-record',
                     'blocking_gaps': 0, 'wrong_expectations': len(reader['findings']), 'minor_gaps': 0,
                     'commands_executed_count': 1, 'read_rev': cand, 'inputs': inputs, 'traces': [trace_rel],
                     'seats': list(reader['seats']), 'reader_files': list(reader['reader_files']),
                     'findings': list(reader['findings']),
                     'reports': [READS_DIR, '%s/refresh-receipts.json' % trace_rel.rsplit('/traces/', 1)[0]]}
            working['entries'].append(entry)
            receipts.append({'section': h, 'start': sec['start'], 'end': sec['end'], 'sha256': sec['sha256'],
                             'credit_at_cand': cand_reason.get(h), 'direct': direct, 'records_via_blob': records,
                             'internal_pointer_follow': followed, 'inputs': inputs, 'trace': trace_rel,
                             'reader_files': reader['reader_files'], 'findings': reader['findings'], 'exit': r.returncode,
                             'stdout_sha256': sha256(r.stdout)})
        with open(os.path.join(lane, LEDGER), 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(working, indent=1, ensure_ascii=True))
        with open(os.path.join(receipt_dir, 'refresh-receipts.json'), 'w', encoding='utf-8') as fh:
            json.dump({'candidate': cand, 'base': base, 'scope': SCOPE, 'read_command': READ_CMD,
                       'instrument_sha256': sha256(open(tracer, 'rb').read()),
                       'monitor': {'path': MONITOR, 'sha256': sha256(open(os.path.join(clone, MONITOR), 'rb').read()),
                                   'impl': MONITOR_IMPL,
                                   'impl_sha256': sha256(open(os.path.join(clone, MONITOR_IMPL), 'rb').read())},
                       'measured_before': {'base': mbase, 'cand': mcand},
                       'targets': len(targets), 'entries_added': len(receipts), 'receipts': receipts}, fh, indent=1)
        print('TARGETS %d BASE %s (%d/%d score %d) CAND %s (%d/%d score %d)' %
              (len(targets), base[:8], mbase['covered'], mbase['total'], mbase['score'],
               cand[:8], mcand['covered'], mcand['total'], mcand['score']))
    finally:
        shutil.rmtree(SCR, ignore_errors=True)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.stderr.write(__doc__ + '\n')
        sys.exit(64)
    counter = os.path.join(os.path.realpath(sys.argv[1]), R49)
    if not os.path.exists(counter):
        raise SystemExit('round-49 counter missing at %s' % R49)
    spec = importlib.util.spec_from_file_location('c1', counter)
    c1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c1)
    sys.exit(main())
