#!/usr/bin/env python3
"""Round23 final source re-anchor: actual traced L1-author source byte reads.

For each uncredited SKILL.md section named by a strict monitor --explain run
at REV, clone the lane at REV privately, read the section bytes plus the input
paths of that section's latest ledger entry under tools/trace-inputs.py, and
write one trace per section to the lane plus a receipt file. Writes only
under --out-dir and the receipt/entries paths; never edits the ledger, the
lane Git index or jj state. Appending entries to the ledger is a separate step.
Not recipe execution, independent/blind cold-read or command coverage.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

sys.dont_write_bytecode = True
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
IGNORED = {'SKILL.md', '.ufo/evidence/round-17/coldread/ledger.json',
           '.ufo/evidence/round-18/coldread/ledger.json', LEDGER}
READER = ("import sys,json,hashlib\nfrom pathlib import Path\nr=Path(sys.argv[1]);start=int(sys.argv[2]);"
          "end=int(sys.argv[3]);paths=json.loads(sys.argv[4]);page=(r/'SKILL.md').read_bytes();"
          "sys.stdout.buffer.write(b''.join(page.splitlines(keepends=True)[start-1:end]));"
          "print('\\nSOURCE-READS: actual L1-author source byte reads; not recipe execution or independent/blind cold-read')\n"
          "for rel in paths:\n data=(r/rel).read_bytes();print('SOURCE',rel,'bytes='+str(len(data)),'sha256='+hashlib.sha256(data).hexdigest())\n")
PROVENANCE = ('actual L1-author byte-consuming source reads; not recipe execution, '
              'independent/blind cold-read or required-command coverage')


def now():
    return datetime.now(timezone.utc).isoformat()


def env():
    return {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--monitor', type=Path, required=True, help='strict --explain monitor JSON at REV')
    ap.add_argument('--out-dir', type=Path, required=True, help='trace directory inside the lane')
    ap.add_argument('--receipts', type=Path, required=True)
    ap.add_argument('--entries', type=Path, required=True)
    ap.add_argument('--seat', required=True)
    a = ap.parse_args()
    repo = a.repo.resolve()
    spec = importlib.util.spec_from_file_location('m18', repo / '.ufo/evidence/round-18/measure.py')
    m18 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m18)
    monitor = json.loads(a.monitor.read_text())
    if monitor.get('revision') != a.rev or monitor.get('trace_gate') != 'strict' or monitor.get('overrides_used'):
        raise SystemExit('monitor receipt must be strict, no overrides, at --rev')
    missing = [s for s in monitor['coldread']['sections'] if not s['credited']]
    show = lambda p: subprocess.run(['git', '-C', str(repo), 'show', a.rev + ':' + p], check=True,
                                    capture_output=True, env=env()).stdout
    skill = show('SKILL.md')
    sections = {s['start']: s for s in m18.sectionize(skill)}
    ledger = json.loads(show(LEDGER))['entries']
    a.out_dir.mkdir(parents=True, exist_ok=True)
    observations, entries = [], []
    with tempfile.TemporaryDirectory(prefix='tameshi-r23-reanchor-final-') as tmp:
        clone = Path(tmp) / 'lane'
        subprocess.run(['git', 'clone', '-q', '--no-hardlinks', str(repo), str(clone)], check=True, env=env())
        subprocess.run(['git', '-C', str(clone), 'checkout', '-q', '--detach', a.rev], check=True, env=env())
        tool = clone / 'tools/trace-inputs.py'
        tool_sha = hashlib.sha256(tool.read_bytes()).hexdigest()
        for miss in missing:
            sec = sections[miss['start']]
            if sec['heading'] != miss['heading']:
                raise SystemExit('section identity changed: %r' % miss)
            prior = [e for e in ledger if e.get('start') == sec['start'] and e.get('heading') == sec['heading']]
            if not prior:
                raise SystemExit('no prior entry for section %r' % sec['heading'])
            base = prior[-1]
            paths = sorted(p for p in base['inputs'] if p not in IGNORED)
            trace = (a.out_dir / ('source-%d.json' % sec['start'])).resolve()
            if trace.exists():
                raise SystemExit('refusing to overwrite %s' % trace)
            argv = ['python3', str(tool), '--root', str(clone), '--out', str(trace), '--',
                    'python3', '-c', READER, str(clone), str(sec['start']), str(sec['end']), json.dumps(paths)]
            start = now()
            p = subprocess.run(argv, cwd=str(clone), capture_output=True, text=True, env=env(), timeout=300)
            end = now()
            observations.append({'argv': argv, 'cwd': str(clone), 'exit': p.returncode,
                                 'instrument_sha256': tool_sha, 'measurement_interval': {'start': start, 'end': end},
                                 'revision': a.rev, 'stderr': p.stderr, 'stdout': p.stdout})
            if p.returncode != 0:
                raise SystemExit('trace failed for %s: %s' % (sec['heading'], p.stderr[-500:]))
            t = json.loads(trace.read_text())
            if t.get('live_lane_reads') or t.get('external') or t.get('rev') != a.rev:
                raise SystemExit('trace not bound to clone at rev: %s' % trace)
            inputs = {k: v for k, v in t['inputs'].items() if k not in IGNORED}
            if sorted(inputs) != paths:
                raise SystemExit('trace inputs differ from planned paths for %s' % sec['heading'])
            entry = dict(base)
            entry.update({'end': sec['end'], 'heading': sec['heading'], 'sha256': sec['sha256'],
                          'skill_sha256': hashlib.sha256(skill).hexdigest(), 'start': sec['start'],
                          'inputs': inputs, 'read_rev': a.rev, 'external_inputs': {},
                          'traces': [os.path.relpath(trace, repo)], 'reports': [os.path.relpath(a.receipts.resolve(), repo)],
                          'seats': [a.seat], 'provenance': PROVENANCE})
            entries.append(entry)
    a.receipts.write_text(json.dumps({'count': len(observations), 'observations': observations,
                                      'read_revision': a.rev}, indent=1, ensure_ascii=False) + '\n')
    a.entries.write_text(json.dumps({'entries': entries}, indent=1, ensure_ascii=False) + '\n')
    print('REANCHOR: %d sections traced at %s' % (len(entries), a.rev))


if __name__ == '__main__':
    main()
