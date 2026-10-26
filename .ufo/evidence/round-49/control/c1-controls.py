#!/usr/bin/env python3
"""Round-49 C1 controls, scored with the frozen C1 counter at freeze bytes, before any deciding run.

  CTL_0  do-nothing: the base tree as it is.
  CTL_J  the round-36 refresh shape: a ledger entry per target section keyed to its current sha,
         inputs = the inputs of that heading's latest ledger entry (records included), a synthetic
         trace; no read rows, no section edits.
  CTL_K  pinned-read re-key: entries whose inputs exclude the five record files, plus mechanical
         read rows (excerpt = the first 60 collapsed characters of the pointed text, `absent` for
         every unresolvable path pointer, fleet HEAD for the external pointer); no section edits.
  CTL_K2 fabrication positive control: CTL_K plus a mechanical edit that prefixes `SKILL.md` to the
         two bare map pointers. It shows the counter can pass, and what it cannot see: a read row
         that was never read and a pointer re-targeted without checking what it points at.
Usage: c1-controls.py LANE BASE OUTDIR   (work under $HYAKU_SCRATCH/tameshi-r49/controls)
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

LANE, BASE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
E = os.path.join(LANE, '.ufo/evidence/round-49')
COUNTER = os.path.join(E, 'c1/measure.py')
SCR = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'tameshi-r49', 'controls')
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
spec = importlib.util.spec_from_file_location('c1m', COUNTER)
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)
ENV = dict(c1.GIT_ENV, GIT_AUTHOR_NAME='r49-control', GIT_AUTHOR_EMAIL='control@invalid',
           GIT_COMMITTER_NAME='r49-control', GIT_COMMITTER_EMAIL='control@invalid')


def sh(*a, cwd=None):
    r = subprocess.run(list(a), capture_output=True, env=ENV, cwd=cwd)
    if r.returncode != 0:
        raise SystemExit('command failed: %s\n%s' % (a, r.stderr.decode(errors='replace')))
    return r.stdout.decode()


def fsha(path):
    import hashlib
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def clone(name):
    d = os.path.join(SCR, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(SCR, exist_ok=True)
    sh('git', 'clone', '-q', '--shared', LANE, os.path.join(d, 'lane'))
    lane = os.path.join(d, 'lane')
    sh('git', '-C', lane, 'checkout', '-q', '--detach', BASE)
    if os.path.realpath(sh('git', '-C', lane, 'rev-parse', '--show-toplevel').strip()) != os.path.realpath(lane):
        raise SystemExit('toplevel mismatch')
    return d, lane


def commit(lane, msg):
    sh('git', '-C', lane, 'add', '-A')
    sh('git', '-C', lane, 'commit', '-q', '-m', msg)
    return sh('git', '-C', lane, 'rev-parse', 'HEAD').strip()


def sections(lane):
    mod = c1.load_monitor_module(lane)
    raw = open(os.path.join(lane, 'SKILL.md'), 'rb').read()
    return {s['heading']: s for s in mod.sectionize(raw) if s['heading'] in c1.TARGETS}


def add_entries(lane, name, inputs_for):
    led_path = os.path.join(lane, LEDGER)
    led = json.load(open(led_path))
    secs = sections(lane)
    for i, h in enumerate(c1.TARGETS):
        s = secs[h]
        inputs = inputs_for(h)
        tr = '.ufo/evidence/round-49/control/%s-trace-%d.json' % (name, i)
        os.makedirs(os.path.dirname(os.path.join(lane, tr)), exist_ok=True)
        json.dump({'schema': 'tameshi-trace-inputs-v1', 'argv': ['control', name], 'cwd': lane, 'root': lane,
                   'rev': BASE, 'rev_reason': None, 'exit': 0, 'tracked_filter': True,
                   'env_overrides': {'git_vars_removed': [], 'set': {}}, 'inputs': inputs, 'untracked': {},
                   'external': {}, 'live_lane_reads': {}, 'dropped_home_count': 0},
                  open(os.path.join(lane, tr), 'w'), indent=1)
        led['entries'].append({'skill_sha256': s['sha256'], 'start': s['start'], 'end': s['end'], 'heading': h,
                               'sha256': s['sha256'], 'class': 'record', 'verdict': 'verified-record',
                               'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 0,
                               'commands_executed_count': 1, 'read_rev': BASE, 'inputs': inputs,
                               'traces': [tr], 'seats': ['control ' + name], 'reports': []})
    json.dump(led, open(led_path, 'w'), indent=1)
    open(led_path, 'a').write('\n')


def latest_inputs(lane):
    led = json.load(open(os.path.join(lane, LEDGER)))
    last = {}
    for e in led['entries']:
        if e.get('heading') in c1.TARGETS:
            last[e['heading']] = e
    def f(h):
        return {p: fsha(os.path.join(lane, p)) for p in last[h]['inputs']
                if p != 'SKILL.md' and os.path.isfile(os.path.join(lane, p))}
    return f


def pinned_inputs(lane, rev):
    ptrs, _ = c1.list_pointers(lane, rev)
    def f(h):
        files = sorted({p['file'] for p in ptrs if p['heading'] == h and p['file'] and p['kind'] in ('line', 'path')
                        and p['file'] not in c1.VOLATILE and p['file'] != 'SKILL.md'})
        return {p: fsha(os.path.join(lane, p)) for p in files}
    return f


def mech_reads(lane, rev, fleet_head):
    ptrs, _ = c1.list_pointers(lane, rev)
    rows = []
    for p in ptrs:
        row = {'heading': p['heading'], 'ordinal': p['ordinal'], 'raw': p['raw'], 'file': p['file'],
               'ranges': p['ranges'], 'reader': 'control (mechanical, unread)'}
        if p['file'] is None:
            row.update(verdict='absent', excerpt='')
        else:
            if p['kind'] in ('external', 'external-path'):
                data = c1.blob(os.path.dirname(LANE), fleet_head, p['file'][3:]) or b''
                row['fleet_commit'] = fleet_head
            else:
                data = c1.blob(lane, rev, p['file']) or b''
            text = c1.pointed_text(data, p['ranges']) if p['ranges'] else c1.norm(data.decode('utf-8', 'replace'))
            row.update(verdict='holds', excerpt=text[:60])
        rows.append(row)
    path = os.path.join(lane, c1.READS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump({'schema': 'tameshi-r49-reads-v1', 'rows': rows}, open(path, 'w'), indent=1)


def score(name, lane, rev):
    w = os.path.join(SCR, name, 'w')
    shutil.rmtree(w, ignore_errors=True)
    r = subprocess.run([sys.executable, '-B', COUNTER, '--lane', lane, '--rev', rev, '--work', w,
                        '--fleet', os.path.dirname(LANE)],
                       capture_output=True, env=dict(c1.GIT_ENV, TMPDIR=os.path.join(SCR, name)))
    with open(os.path.join(OUT, 'c1-%s.stdout' % name), 'wb') as fh:
        fh.write(r.stdout + r.stderr)
    last = [ln for ln in r.stdout.decode().splitlines() if ln.startswith('C1_R49:')]
    print('%s exit=%d %s' % (name, r.returncode, last[-1] if last else r.stderr.decode()[-300:]), flush=True)


fleet_head = sh('git', '-C', os.path.dirname(LANE), 'rev-parse', 'HEAD').strip()
score('CTL_0', LANE, BASE)
d, lane = clone('CTL_J')
add_entries(lane, 'CTL_J', latest_inputs(lane))
score('CTL_J', lane, commit(lane, 'CTL_J'))
for name, edit in (('CTL_K', False), ('CTL_K2', True)):
    d, lane = clone(name)
    if edit:
        p = os.path.join(lane, 'SKILL.md')
        t = open(p, encoding='utf-8').read()
        for bare in ('(`:1294-1297`)', '(`:1246-1270`)'):
            assert t.count(bare) == 1, bare
            t = t.replace(bare, '(`SKILL.md' + bare[2:])
        open(p, 'w', encoding='utf-8').write(t)
        a = commit(lane, name + ' edit')
    else:
        a = BASE
    add_entries(lane, name, pinned_inputs(lane, a))
    a2 = commit(lane, name + ' entries')
    mech_reads(lane, a2, fleet_head)
    score(name, lane, commit(lane, name + ' reads'))
shutil.rmtree(SCR, ignore_errors=True)
