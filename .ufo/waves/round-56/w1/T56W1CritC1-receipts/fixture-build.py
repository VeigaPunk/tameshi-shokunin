#!/usr/bin/env python3
"""Build round-56 C1 falsification fixture states in a scratch clone.

Every state is a commit (or working-tree edit) in $S/lane, a --shared clone of
the lane detached at the round-56 base. No lane object is written: commits land
in the clone's own object store. Git calls all name -C $L and the toplevel is
asserted to be $L before any commit.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/tameshi-r56/T56W1CritC1'
L = S + '/lane'
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1'
C0 = BASE
LEDGER_REL = '.ufo/evidence/round-21/coldread/ledger.json'
PIN = 'tools/mutate-and-run.sh'
FROZEN = json.load(open(LANE + '/.ufo/evidence/round-56/c1/lost-headings-at-base.json'))
FAIL_VERDICTS = {'gap-blocking', 'wrong-expectation', 'not-executed'}
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')


def git(*a, check=True):
    r = subprocess.run(['git', '-C', L] + list(a), capture_output=True, text=True, env=ENV)
    if check and r.returncode != 0:
        raise SystemExit('git %s failed: %s' % (a, r.stderr))
    return r.stdout.strip()


def assert_toplevel():
    top = git('rev-parse', '--show-toplevel')
    assert top == L, 'toplevel %r != %r' % (top, L)


def reset(name):
    assert_toplevel()
    git('checkout', '-f', '-B', name, BASE)


def commit(msg, amend=False):
    assert_toplevel()
    git('add', '-A')
    args = ['-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
            'commit', '--quiet', '--allow-empty']
    if amend:
        args.append('--amend')
    git(*(args + ['-m', msg]))
    return git('rev-parse', 'HEAD')


def blob(rev, path):
    r = subprocess.run(['git', '-C', L, 'show', '%s:%s' % (rev, path)],
                       capture_output=True, env=ENV)
    assert r.returncode == 0, 'missing %s at %s' % (path, rev)
    return r.stdout


def r18():
    spec = importlib.util.spec_from_file_location('r18x', L + '/.ufo/evidence/round-18/measure.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sections(rev):
    return {s['heading']: s for s in r18().sectionize(blob(rev, 'SKILL.md'))}


def read_text(path):
    with open(path, 'r', encoding='utf-8', errors='surrogateescape') as f:
        return f.read()


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', errors='surrogateescape') as f:
        f.write(text)


def load_ledger():
    return json.loads(read_text(L + '/' + LEDGER_REL))


def save_ledger(d):
    write_text(L + '/' + LEDGER_REL, json.dumps(d, indent=1, ensure_ascii=False) + '\n')


def rekey_dir():
    return '.ufo/evidence/round-21/coldread/rekey-r56-' + C0[:12]


def trace_path():
    return rekey_dir() + '/traces/1.json'


def pin_sha(rev):
    return hashlib.sha256(blob(rev, PIN)).hexdigest()


def write_trace(rev):
    write_text(L + '/' + trace_path(),
               json.dumps({'schema': 'tameshi-trace-inputs-v1',
                           'inputs': {PIN: pin_sha(rev)},
                           'note': 'fixture: no command was run for this receipt'},
                          indent=1) + '\n')


def entry_for(head, sec, rev, bogus_external=False):
    e = {
        'skill_sha256': hashlib.sha256(blob(rev, 'SKILL.md')).hexdigest(),
        'start': sec['start'], 'end': sec['end'], 'heading': head,
        'sha256': sec['sha256'], 'class': 'record', 'verdict': 'verified-record',
        'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 0,
        'commands_executed_count': 1, 'read_rev': C0,
        'inputs': {PIN: pin_sha(rev)},
        'traces': [trace_path()],
        'seats': ['T56W1CritC1'],
        'reports': [],
        'provenance': 'fixture-fabricated entry: no section was read',
    }
    if bogus_external:
        e['external_inputs'] = {'tameshi@%s:SHONEN.md' % C0: '0' * 64}
    return e


def write_readers(rev):
    secs = sections(rev)
    for i, head in enumerate(sorted(FROZEN), 1):
        path = L + '/.ufo/waves/round-56/w2/T56W2ReadCrit%02d.json' % i
        write_text(path, json.dumps({
            'heading': head, 'cand': C0, 'section_sha256': secs[head]['sha256'],
            'reader': 'T56W2ReadCrit%02d' % i,
            'note': 'fixture: sha256 copied from the tree; the section was never read',
        }, indent=1) + '\n')


ROW6 = ('| calibration | 6 | Restraint score of the strict cold-read monitor '
        '`python3 .ufo/evidence/round-21/coldread/measure.py --repo R --rev REV` '
        '(`calibration_restraint_score`; 64 of 64 sections credited at the named commit) | '
        '%s | 56 (restated 8 -> 6) |' % C0[:12])
ROW6_WRONG = ROW6.replace('%s | 56' % C0[:12], '0a2010acd1e9 | 56')
# After a full re-key the monitor reads 8 at REV, so the standing row must state 8
# and name a commit where the monitor also reads 8 (the round-55 floor).
ROW8 = ('| calibration | 8 | Restraint score of the strict cold-read monitor '
        '`python3 .ufo/evidence/round-21/coldread/measure.py --repo R --rev REV` '
        '(`calibration_restraint_score`; 64 of 64 sections credited at the named commit) | '
        '0a2010acd1e9 | 56 (restated at the commit it names) |')


def append_row(text, row=None):
    return text.rstrip('\n') + '\n\n' + (row or ROW6) + '\n'


DOCTOR = '''#!/usr/bin/env python3
"""Fixture stub: a doctored copy of the round-21 selector (working tree only)."""
import json
import sys
if '--selftest' in sys.argv:
    print('SELECTOR_SELFTEST: 0/0 pass')
    sys.exit(0)
print(json.dumps({'coldread': {'sections_total': 64, 'sections_covered': 64,
                               'box3_full_page': True,
                               'sections': [{'heading': 'stub-%d' % i, 'credited': True}
                                            for i in range(64)]},
                  'calibration_restraint_score': 8}))
sys.exit(0)
'''


def monitor(rev):
    out = subprocess.run(['python3', LANE + '/.ufo/evidence/round-21/coldread/measure.py',
                          '--repo', L, '--rev', rev], capture_output=True, env=ENV)
    return json.loads(out.stdout.decode())


def fill_uncredited(rev):
    """Add one clean fabricated entry per section the monitor does not credit at REV."""
    secs = sections(rev)
    mon = monitor(rev)
    missing = [s['heading'] for s in mon['coldread']['sections'] if not s['credited']]
    if not missing:
        return []
    led = load_ledger()
    for head in missing:
        led['entries'].append(entry_for(head, secs[head], rev, bogus_external=(head == FROZEN[0])))
    save_ledger(led)
    return missing


def build(name):
    if name == 'del18':
        reset('exp-del18')
        led = load_ledger()
        led['entries'] = [e for e in led['entries'] if e.get('heading') not in FROZEN]
        save_ledger(led)
        return commit('fixture: delete every ledger entry for the 18 frozen headings')
    if name == 'delfail':
        reset('exp-delfail')
        led = load_ledger()
        led['entries'] = [e for e in led['entries'] if e.get('verdict') not in FAIL_VERDICTS]
        save_ledger(led)
        return commit('fixture: delete every failing-verdict ledger entry')
    if name == 'row6':
        reset('exp-row6')
        write_text(L + '/SCORECARD.md', append_row(read_text(L + '/SCORECARD.md')))
        return commit('fixture: append a restated calibration row, no binding')
    if name == 'row6wrong':
        reset('exp-row6wrong')
        text = read_text(L + '/SCORECARD.md').rstrip('\n') + '\n\n' + ROW6_WRONG + '\n'
        write_text(L + '/SCORECARD.md', text)
        return commit('fixture: restated row naming 0a2010ac where the monitor reads 8')
    if name in ('repin', 'fabricate', 'unstable'):
        reset('exp-' + name)
        write_trace(BASE)
        secs = sections(BASE)
        led = load_ledger()
        for head in FROZEN:
            led['entries'].append(entry_for(head, secs[head], BASE))
        save_ledger(led)
        write_text(L + '/SCORECARD.md', append_row(read_text(L + '/SCORECARD.md'), ROW8))
        if name in ('fabricate', 'unstable'):
            write_readers(BASE)
        rev = commit('fixture: %s re-key of the 18 frozen headings' % name)
        for _ in range(4):
            added = fill_uncredited(rev)
            if not added:
                break
            rev = commit('fixture: clean fabricated entries for %d uncredited sections' % len(added),
                         amend=True)
        if name == 'unstable':
            led = load_ledger()
            log_sha = hashlib.sha256(blob(rev, 'LOG.md')).hexdigest()
            for e in led['entries']:
                if e.get('heading') == FROZEN[0] and e.get('read_rev') == C0:
                    e['inputs']['LOG.md'] = log_sha
            save_ledger(led)
            rev = commit('fixture: one bound entry pins LOG.md', amend=True)
        return rev
    if name == 'wttamper':
        reset('exp-wttamper')
        write_text(L + '/.ufo/evidence/round-21/coldread/measure.py', DOCTOR)
        return BASE  # uncommitted: the working tree differs from REV
    if name == 'tamper':
        reset('exp-tamper')
        write_text(L + '/.ufo/evidence/round-21/coldread/measure.py', DOCTOR)
        write_text(L + '/SCORECARD.md', append_row(read_text(L + '/SCORECARD.md'), ROW8))
        return commit('fixture: doctored round-21 selector committed at REV')
    raise SystemExit('unknown state ' + name)


if __name__ == '__main__':
    print(build(sys.argv[1]))
