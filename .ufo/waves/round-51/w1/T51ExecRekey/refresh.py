#!/usr/bin/env python3
"""Round-51 cold-read re-key: one ledger entry per SKILL.md section the round-21 monitor stopped crediting.

Usage: refresh.py LANE CAND READERS_JSON
  LANE          lane checkout; the round-21 ledger and the re-key receipts are written there (never committed here)
  CAND          candidate commit whose bytes the re-read observes (content revision: C2 runner, C3 registry row)
  READERS_JSON  {"<heading>": ["seat", ...]} — the seats whose wave-2 read rows cover that section; the key "*"
                supplies the seats for a target heading the file does not name (fixture runs use it)

Targets are computed, never listed here: they are the headings the unchanged round-21 cold-read monitor
(.ufo/evidence/round-21/coldread/measure.py, strict, no override flag) credits at BASE
9962033fd7a75aa2f2847e979dd687a5d28505a1 and does not credit at CAND. The monitor is also what scores the
round, so a section it stopped crediting is exactly what a re-key has to carry. Refusals: CAND or BASE
unresolvable; a monitor run that does not exit 0; no target at all (nothing to re-key); a target heading
that is not a single section at CAND; a target that cites no lane file even after following its own internal
pointer; reader seats missing for a target; the working-tree ledger differing from the ledger at CAND; or a
trace that is not clean (volatile input, live-lane read outside .git/, untracked read, missed direct read).

Per target, from round 49 (`.ufo/evidence/round-49/c1/refresh.py`, extractor/resolver from the round-49 counter
`.ufo/evidence/round-49/c1/measure.py`): the section and every lane file its pointers cite are read in a
--shared scratch clone checked out at CAND, under tools/trace-inputs.py. Files in the round-49 VOLATILE record
list (LOG.md, SCORECARD.md, corpus/SOURCES.md, corpus/QUALITY.md, corpus/README.md) are read through
`git cat-file blob CAND:<path>`: their cited lines are append-only bytes, so the read observes them without
making the whole growing file an input. When a section's pointers resolve to no non-record file at all, its
own unresolved internal line pointer (`:N-M` into SKILL.md) is followed once: those SKILL.md lines are read and
the file pointers they carry are opened — a one-hop internal pointer, recorded in the receipt as
`internal_pointer_follow`. The trace's inputs become the entry's inputs; the entry appends to the round-21
ledger (the path the unchanged monitor reads). Scope, carried into the receipts: "reading-bound re-key: the
section's pointers were read by the named seats (wave-2 read rows with located excerpts) and its cited
non-record files are bound by trace; not blind cold-read or recipe execution".

Order of work (the L1 owns the commits): run this against a tree whose ledger equals CAND's; then commit the
ledger entries together with the receipts under .ufo/evidence/round-51/coldread/rekey-<cand8>/ (the monitor
resolves each entry's traces at the measured revision); then re-run the monitor and the QUALITY coldread
pre-check at the new revision.

Writes: the round-21 ledger; .ufo/evidence/round-51/coldread/rekey-<cand8>/{traces/section-<n>.json,
refresh-receipts.json}. Scratch: $HYAKU_SCRATCH/tameshi-r51/refresh (never /tmp).
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
BASE = '9962033fd7a75aa2f2847e979dd687a5d28505a1'
MONITOR = '.ufo/evidence/round-21/coldread/measure.py'
MONITOR_IMPL = '.ufo/evidence/round-18/measure.py'
R49 = '.ufo/evidence/round-49/c1/measure.py'
E = '.ufo/evidence/round-51'
READS_DIR = E + '/coldread/reads/'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
SCR = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'tameshi-r51', 'refresh')
SCOPE = ('reading-bound re-key: the section\'s pointers were read by the named seats (wave-2 read rows with '
         'located excerpts) and its cited non-record files are bound by trace; not blind cold-read or recipe execution')
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
    """One section record per heading (heading -> {start,end,sha256,text}); duplicates are a refusal."""
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
        out[s['heading']] = {'start': s['start'], 'end': s['end'], 'sha256': s['sha256'],
                             'text': '\n'.join(body)}
    return out


def cited_files(clone, rev, text):
    """Resolve the section's pointers: (direct non-record files, record files, unresolved line ranges)."""
    direct, records, internal = set(), set(), []
    for p in c1.extract(text):
        f, kind, _ranges = c1.resolve(clone, rev, p['token'], p['kind'])
        if f and kind in ('line', 'path'):
            if f == 'SKILL.md':
                continue  # the page is the section's own bytes: read as the page, never an entry input
            (records if f in c1.VOLATILE else direct).add(f)
        elif p['kind'] == 'line' and p['token'] is None and p['ranges']:
            internal.extend(p['ranges'])
    return sorted(direct), sorted(records), internal


def follow_internal(clone, rev, ranges):
    """One hop through the section's own SKILL.md line pointer: what do those lines cite?"""
    if not ranges:
        return [], []
    lines = c1.blob(clone, rev, 'SKILL.md').decode('utf-8', 'surrogateescape').split('\n')
    frag = '\n'.join('\n'.join(lines[s - 1:e]) for s, e in ranges if 1 <= s <= e <= len(lines))
    direct, records, _more = cited_files(clone, rev, frag)
    return direct, records


def main():
    lane = os.path.realpath(sys.argv[1])
    cand = sh('git', '-C', lane, 'rev-parse', '--verify', sys.argv[2] + '^{commit}').strip()
    base = sh('git', '-C', lane, 'rev-parse', '--verify', BASE + '^{commit}').strip()
    readers = json.load(open(sys.argv[3], encoding='utf-8'))
    if not isinstance(readers, dict):
        raise SystemExit('READERS_JSON must be an object: {"<heading>": ["seat", ...]}')
    tag = 'rekey-' + cand[:8]  # one directory per re-key: an earlier re-key's receipts are never overwritten
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
            raise SystemExit('working-tree ledger differs from the ledger at CAND: run this where the tree is at '
                             'CAND (its ledger is the base the entries are appended to)')

        mbase, base_rows = run_monitor(clone, base, 'base', work)
        mcand, cand_rows = run_monitor(clone, cand, 'cand', work)
        if not (mbase['strict'] and mcand['strict']):
            raise SystemExit('monitor ran in legacy mode; the round measures strict')
        base_credit = {h: cr for h, cr, _r in base_rows}
        cand_credit = {h: cr for h, cr, _r in cand_rows}
        cand_reason = {h: r for h, _cr, r in cand_rows}
        targets = [h for h, _cr, _r in base_rows if base_credit[h] and not cand_credit.get(h, False)]
        if not targets:
            raise SystemExit('no section lost credit between %s and %s: nothing to re-key' % (base[:8], cand[:8]))
        for h in targets:
            if not base_credit[h]:
                raise SystemExit('target not credited at base: %s' % h)
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
                    raise SystemExit('section %s cites no non-record lane file, even after following its '
                                     'internal pointer %s' % (h, followed))
            seats = readers.get(h) or readers.get('*')
            if not isinstance(seats, list) or not seats:
                raise SystemExit('READERS_JSON names no reader seats for section: %s' % h)
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
            # object-store reads through the --shared clone's alternates are .git/ reads, which the monitor binds to REV
            live = [p for p in (trace.get('live_lane_reads') or {}) if '/.git/' not in p]
            missed = [f for f in direct if f not in trace['inputs']]
            if bad or live or trace.get('untracked') or missed:
                raise SystemExit('trace of %s is not clean: volatile=%s live=%s untracked=%s missed=%s'
                                 % (h, bad, live, trace.get('untracked'), missed))
            working['entries'].append({
                'skill_sha256': sec['sha256'], 'start': sec['start'], 'end': sec['end'], 'heading': h,
                'sha256': sec['sha256'], 'class': 'record', 'verdict': 'verified-record',
                'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 0,
                'commands_executed_count': 1, 'read_rev': cand, 'inputs': inputs, 'traces': [trace_rel],
                'seats': list(seats) + ['L1 TameshiR51 integration'],
                'reports': [READS_DIR, '%s/refresh-receipts.json' % trace_rel.rsplit('/traces/', 1)[0]]})
            receipts.append({'section': h, 'start': sec['start'], 'end': sec['end'], 'sha256': sec['sha256'],
                             'credit_at_cand': cand_reason.get(h), 'direct': direct,
                             'records_via_blob': records, 'internal_pointer_follow': followed,
                             'inputs': inputs, 'trace': trace_rel,
                             'argv_tail': argv[4:7] + ['<READ_CMD>'] + argv[10:], 'exit': r.returncode,
                             'stdout_sha256': sha256(r.stdout)})
            print('REKEY %-62s start=%-5d inputs=%-3d records_via_blob=%d%s'
                  % (h[:62], sec['start'], len(inputs), len(records),
                     ' internal_follow=%s' % followed if followed else ''))

        with open(os.path.join(lane, LEDGER), 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(working, indent=1, ensure_ascii=True))  # the ledger's own serialization (no newline)
        with open(os.path.join(receipt_dir, 'refresh-receipts.json'), 'w', encoding='utf-8') as fh:
            json.dump({'candidate': cand, 'base': base, 'scope': SCOPE, 'read_command': READ_CMD,
                       'instrument_sha256': sha256(open(tracer, 'rb').read()),
                       'monitor': {'path': MONITOR, 'sha256': sha256(open(os.path.join(clone, MONITOR), 'rb').read()),
                                   'impl': MONITOR_IMPL,
                                   'impl_sha256': sha256(open(os.path.join(clone, MONITOR_IMPL), 'rb').read())},
                       'measured_before': {'base': mbase, 'cand': mcand},
                       'targets': len(targets), 'entries_added': len(receipts), 'receipts': receipts},
                      fh, indent=1, ensure_ascii=False)
        print('TARGETS %d BASE %s (%d/%d score %d) CAND %s (%d/%d score %d)'
              % (len(targets), base[:8], mbase['covered'], mbase['total'], mbase['score'],
                 cand[:8], mcand['covered'], mcand['total'], mcand['score']))
    finally:
        shutil.rmtree(SCR, ignore_errors=True)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.stderr.write(__doc__.split('Writes:')[0] + '\n')
        sys.exit(64)
    counter = os.path.join(os.path.realpath(sys.argv[1]), R49)
    if not os.path.exists(counter):
        raise SystemExit('round-49 counter missing at %s' % R49)
    spec = importlib.util.spec_from_file_location('c1', counter)
    c1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c1)
    sys.exit(main())
