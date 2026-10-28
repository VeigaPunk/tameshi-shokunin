#!/usr/bin/env python3
"""Build the round-56 C1 counter mutation fixtures in a scratch clone of the lane.

Every fixture is a synthetic commit in the *clone* (never the lane). The green
fixture G makes all six arms of .ufo/evidence/round-56/c1/measure.py pass at one
revision; each probe fixture is G (or a child of it) carrying exactly one arm's
defect, so a mutated counter that suppresses that arm flips PASS false -> true.

Nothing here is lane content: the re-key entries, trace receipts, reader
reports and SCORECARD rows are fixture bytes in /fast/scratch only.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r56/T56W1MutCounterArms')
CLONE = S / 'lane'
BASE = '981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1'
LANE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
FROZEN_JSON = LANE / '.ufo/evidence/round-56/c1/lost-headings-at-base.json'
REKEY_PARENT = '.ufo/evidence/round-21/coldread'
LEDGER = REKEY_PARENT + '/ledger.json'
WAVE = '.ufo/waves/round-56/w2'
TRACE_SCHEMA = 'tameshi-trace-inputs-v1'
EXTRA_HEADING = ('## Fixture mutation probe section (round 56, scratch only)\n'
                 'Fixture body line for the mutation probe.')

GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
GIT_ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
               GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')


def git(*args, check=True):
    r = subprocess.run(['git', '-C', str(CLONE)] + list(args), env=GIT_ENV,
                       capture_output=True)
    if check and r.returncode != 0:
        raise SystemExit('git %s failed: %s' % (' '.join(args), r.stderr.decode()))
    return r.stdout


def show(rev, path):
    r = subprocess.run(['git', '-C', str(CLONE), 'show', '%s:%s' % (rev, path)],
                       env=GIT_ENV, capture_output=True)
    if r.returncode != 0:
        raise SystemExit('missing %s:%s' % (rev, path))
    return r.stdout


def sha(data):
    return hashlib.sha256(data).hexdigest()


def checkout(rev):
    git('checkout', '--detach', rev)
    top = git('rev-parse', '--show-toplevel').decode().strip()
    assert top == str(CLONE), 'fixture toplevel %r != %r' % (top, CLONE)


def write(rel, data):
    p = CLONE / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data if isinstance(data, bytes) else data.encode())


def commit(msg):
    git('add', '--all')
    git('commit', '--quiet', '-m', msg)
    return git('rev-parse', 'HEAD').decode().strip()


def load_r18():
    src = S / 'r18measure.py'
    src.write_bytes(show(BASE, '.ufo/evidence/round-18/measure.py'))
    spec = importlib.util.spec_from_file_location('r18_fixture', str(src))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def credit_entry(sec, skill_sha, read_rev, trace_path, input_path, input_sha):
    return {
        'skill_sha256': skill_sha, 'start': sec['start'], 'end': sec['end'],
        'heading': sec['heading'], 'sha256': sec['sha256'],
        'class': 'instruction', 'verdict': 'executed-ok',
        'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 0,
        'commands_executed_count': 1, 'read_rev': read_rev,
        'inputs': {input_path: input_sha}, 'traces': [trace_path],
        'seats': ['FIX56'], 'reports': [],
    }


def receipt(input_path, input_sha):
    return json.dumps({'schema': TRACE_SCHEMA,
                       'inputs': {input_path: input_sha}}) + '\n'


def main():
    r18 = load_r18()
    frozen = json.loads(FROZEN_JSON.read_text('utf-8'))
    out = {'base': BASE, 'frozen_headings': frozen, 'fixtures': {}}

    checkout(BASE)
    ledger_base = json.loads(show(BASE, LEDGER))
    skill_base = show(BASE, 'SKILL.md')
    shonen_base = show(BASE, 'SHONEN.md')
    log_base = show(BASE, 'LOG.md')
    sections_base = {s['heading']: s for s in r18.sectionize(skill_base)}
    missing = [h for h in frozen if h not in sections_base]
    assert not missing, 'frozen headings absent from base page: %r' % missing

    # ---- c0: the commit the re-key directory is named after ----------------------
    write('.ufo/evidence/round-56/c1/_fixture_c0.txt', 'c0 anchor for mutation probes\n')
    x = commit('fixture: c0 anchor (mutation probes)')
    rekey_dir = '%s/rekey-r56-%s' % (REKEY_PARENT, x[:12])
    out['c0'] = x
    out['rekey_dir'] = rekey_dir

    # ---- Y: 18 re-keyed entries + traces + 18 reader reports (page 64/64) --------
    shonen_sha = sha(shonen_base)
    skill_sha = sha(skill_base)
    entries = list(ledger_base['entries'])
    for i, h in enumerate(frozen, 1):
        sec = sections_base[h]
        trace_path = '%s/traces/F%02d.json' % (rekey_dir, i)
        write(trace_path, receipt('SHONEN.md', shonen_sha))
        entries.append(credit_entry(sec, skill_sha, x, trace_path,
                                    'SHONEN.md', shonen_sha))
        write('%s/T56W1ReadF%02d.json' % (WAVE, i),
              json.dumps({'heading': h, 'cand': x,
                          'section_sha256': sec['sha256']}) + '\n')
    ledger_y = dict(ledger_base)
    ledger_y['entries'] = entries
    write(LEDGER, json.dumps(ledger_y, indent=2) + '\n')
    y = commit('fixture: re-key 18 headings + 18 reader reports')
    out['fixtures']['Y_rekey_only'] = y

    # ---- Z: the standing calibration row (arm 6 green) --------------------------
    row = ('| calibration | 8 | fixture row: the round-21 cold-read monitor reads 8 '
           'at the named commit | `%s` | 56 (fixture) |\n' % y[:12])
    card = show(BASE, 'SCORECARD.md').decode('utf-8', 'surrogateescape')
    write('SCORECARD.md', card + row)
    z = commit('fixture: standing calibration row restated at the green commit')
    out['fixtures']['G_green'] = z
    out['G_row'] = row.strip()

    # ---- U: one bound entry pins LOG.md (arm 5 red, everything else green) ------
    checkout(z)
    led = json.loads(show(z, LEDGER))
    log_sha = sha(log_base)
    trace_u = '%s/traces/U01.json' % rekey_dir
    write(trace_u, receipt('LOG.md', log_sha))
    led['entries'].append({
        'skill_sha256': sha(show(z, 'SKILL.md')), 'start': 1, 'end': 1, 'heading': '',
        'sha256': sha(b'unstable-probe-round-56'), 'class': 'instruction',
        'verdict': 'executed-ok', 'blocking_gaps': 0, 'wrong_expectations': 0,
        'minor_gaps': 0, 'commands_executed_count': 1, 'read_rev': x,
        'inputs': {'LOG.md': log_sha}, 'traces': [trace_u],
        'seats': ['FIX56'], 'reports': []})
    write(LEDGER, json.dumps(led, indent=2) + '\n')
    out['fixtures']['U_unstable'] = commit('fixture: bound entry pins LOG.md')

    # ---- R: one reader report carries a wrong section sha (arm 4 red) ----------
    checkout(z)
    write('%s/T56W1ReadF01.json' % WAVE,
          json.dumps({'heading': frozen[0], 'cand': x,
                      'section_sha256': '0' * 64}) + '\n')
    out['fixtures']['R_reader_sha'] = commit('fixture: reader report section_sha256 corrupted')

    # ---- T: row asserts 6 at a commit that reads 6 while REV reads 8 (arm 6) ---
    checkout(z)
    row_t = ('| calibration | 6 | fixture row: the round-21 cold-read monitor reads 6 '
             'at the named commit | `%s` | 56 (fixture) |\n' % BASE[:12])
    write('SCORECARD.md', show(z, 'SCORECARD.md').decode('utf-8', 'surrogateescape') + row_t)
    out['fixtures']['T_restate'] = commit('fixture: stale calibration row (6 at a 6-reading commit)')
    out['T_row'] = row_t.strip()

    # ---- S: box 3 unmarked -> score 6 with the page still 64/64 (arm 2) --------
    checkout(z)
    shonen_s = show(z, 'SHONEN.md').decode('utf-8', 'surrogateescape')
    lines = shonen_s.split('\n')
    flipped = 0
    for i, line in enumerate(lines):
        if line.startswith('- [~] ') and flipped < 3:
            flipped += 1
            if flipped == 3:
                lines[i] = '- [x] ' + line[len('- [~] '):]
    assert flipped == 3, 'box 3 not found in SHONEN.md'
    write('SHONEN.md', '\n'.join(lines))
    write('SCORECARD.md', show(z, 'SCORECARD.md').decode('utf-8', 'surrogateescape') + row_t)
    out['fixtures']['S_score'] = commit('fixture: box 3 unmarked (score 6, page 64/64)')

    # ---- P: one extra credited section -> page 65/65, score 8 (arm 2) ----------
    checkout(z)
    skill_p = show(z, 'SKILL.md') + ('\n' + EXTRA_HEADING + '\n').encode()
    write('SKILL.md', skill_p)
    sec_p = {s['heading']: s for s in r18.sectionize(skill_p)}
    extra = sec_p['## Fixture mutation probe section (round 56, scratch only)']
    led = json.loads(show(z, LEDGER))
    trace_p = '%s/traces/P01.json' % rekey_dir
    write(trace_p, receipt('SHONEN.md', shonen_sha))
    led['entries'].append(credit_entry(extra, sha(skill_p), x, trace_p,
                                       'SHONEN.md', shonen_sha))
    write(LEDGER, json.dumps(led, indent=2) + '\n')
    out['fixtures']['P_pagecard'] = commit('fixture: extra credited section (page 65/65)')

    # ---- C: page 65, one floor heading uncredited -> precheck exit 0, lost=1 --
    checkout(z)
    skill_c = show(z, 'SKILL.md') + ('\n' + EXTRA_HEADING + '\n').encode()
    write('SKILL.md', skill_c)
    sec_c = {s['heading']: s for s in r18.sectionize(skill_c)}
    extra_c = sec_c['## Fixture mutation probe section (round 56, scratch only)']
    led = json.loads(show(z, LEDGER))
    kept = []
    dropped = 0
    for e in led['entries']:
        if (dropped == 0 and isinstance(e, dict) and e.get('heading') == frozen[0]
                and any(isinstance(t, str) and rekey_dir in t for t in (e.get('traces') or []))):
            dropped += 1
            continue
        kept.append(e)
    assert dropped == 1, 'did not drop exactly one re-keyed entry'
    trace_c = '%s/traces/C01.json' % rekey_dir
    write(trace_c, receipt('SHONEN.md', shonen_sha))
    kept.append(credit_entry(extra_c, sha(skill_c), x, trace_c, 'SHONEN.md', shonen_sha))
    led['entries'] = kept
    write(LEDGER, json.dumps(led, indent=2) + '\n')
    out['fixtures']['C_precheck'] = commit('fixture: page 65/65 with one floor heading uncredited')

    # ---- side commit S (not an ancestor) + Z2 naming it (arm 6) ---------------
    checkout(y)
    write('.ufo/evidence/round-56/c1/_fixture_side.txt', 'side branch commit\n')
    side = commit('fixture: side-branch commit (not an ancestor of the probe revision)')
    checkout(z)
    row_a = ('| calibration | 8 | fixture row: the round-21 cold-read monitor reads 8 '
             'at the named commit | `%s` | 56 (fixture) |\n' % side[:12])
    write('SCORECARD.md', show(z, 'SCORECARD.md').decode('utf-8', 'surrogateescape') + row_a)
    out['fixtures']['A_ancestor'] = commit('fixture: row names a non-ancestor commit')
    out['side_commit'] = side
    out['A_row'] = row_a.strip()

    (S / 'fixtures.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: (v[:12] if isinstance(v, str) else v)
                      for k, v in out['fixtures'].items()}, indent=1))
    print('c0', x[:12], 'side', side[:12], 'rekey', rekey_dir)
    return 0


if __name__ == '__main__':
    sys.exit(main())
