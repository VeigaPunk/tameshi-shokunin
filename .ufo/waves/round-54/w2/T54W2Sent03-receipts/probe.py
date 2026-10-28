#!/usr/bin/env python3
"""Two adversarial probes against the C1 counter's read_rev arm.

Both start from the POSITIVE fixture (counter PASS=true, 64/64, rekeyed 7/7)
and change nothing except what the read_rev arm is supposed to police.

  split   For "## Standing rules" two bound entries replace the honest one:
            A: the C1 section sha256, read_rev = 12-char prefix   (monitor credits it)
            B: a sha256 that belongs to NO section, read_rev = c0 (arm 3 accepts it)
          Neither entry carries BOTH the right bytes and the right read_rev.
          Tests whether the two instruments can be satisfied by disjoint witnesses.

  provenance
          The re-key directory is renamed to rekey-r54-<C0> (the wave-1 read
          commit, an ancestor), read_rev = C0, and every reader report claims
          cand = C0 - while section_sha256 stays the C1 sha. The recorded sha is
          therefore NOT the sha of those bytes at C0.
          Tests whether the counter verifies that a report's bytes exist at the
          revision it names.

Usage: probe.py split|provenance
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

S = '/fast/scratch/hyaku/tameshi-r54/T54W2Sent03'
C1 = '99c3bc88d704566197783f66b211ee0a830e0330'
C0 = '59c38109bf119d0e9d4f878644a82babc937bc1e'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
REKEY_C1 = '.ufo/evidence/round-21/coldread/rekey-r54-' + C1[:12]
REKEY_C0 = '.ufo/evidence/round-21/coldread/rekey-r54-' + C0[:12]
HEADING = '## Standing rules'
VARIANT = sys.argv[1]
D = '%s/fixtures/%s' % (S, VARIANT)

env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')


def git(args, check=True):
    return subprocess.run(['git', '-C', D] + args, env=env, capture_output=True, check=check)


def main():
    if os.path.exists(D):
        shutil.rmtree(D)
    subprocess.run(['git', 'clone', '--shared', '--quiet', S + '/fixtures/positive', D],
                   env=env, check=True)
    assert git(['rev-parse', '--show-toplevel']).stdout.decode().strip() == D
    head = git(['rev-parse', 'HEAD']).stdout.decode().strip()
    ledger = json.loads(git(['show', head + ':' + LEDGER]).stdout.decode('utf-8', 'surrogateescape'))
    entries = ledger['entries']

    spec = importlib.util.spec_from_file_location('r18p', S + '/code/r18-at-c1.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    skill = git(['show', head + ':SKILL.md']).stdout
    secs = {s['heading']: s for s in mod.sectionize(skill)}

    def bound(prefix, heading=HEADING):
        return [e for e in entries
                if e.get('heading') == heading
                and any(isinstance(t, str) and t.startswith(prefix + '/')
                        for t in (e.get('traces') or []))]

    if VARIANT == 'split':
        good = bound(REKEY_C1)
        assert len(good) == 1, good
        honest = good[0]
        assert honest['read_rev'] == C1
        entries.remove(honest)
        sec = secs[HEADING]
        # A: right bytes, wrong read_rev - the monitor credits this one
        a = json.loads(json.dumps(honest))
        a['read_rev'] = C1[:12]
        a['traces'] = [REKEY_C1 + '/traces/section-90.json']
        a['sha256'] = sec['sha256']
        # B: wrong bytes, right read_rev - arm 3 accepts this one
        b = json.loads(json.dumps(honest))
        b['read_rev'] = C1
        b['traces'] = [REKEY_C1 + '/traces/section-91.json']
        b['sha256'] = hashlib.sha256(b'no section at any revision has these bytes').hexdigest()
        for e, n in ((a, 90), (b, 91)):
            with open(os.path.join(D, REKEY_C1, 'traces', 'section-%02d.json' % n), 'w') as fh:
                json.dump({'schema': 'tameshi-trace-inputs-v1', 'argv': ['true'], 'cwd': S,
                           'root': D, 'rev': C1, 'exit': 0, 'inputs': dict(e['inputs']),
                           'external': {}, 'live_lane_reads': {}, 'untracked': []}, fh, indent=1)
                fh.write('\n')
        entries.extend([a, b])
        detail = {'A_sha_is_section_at_C1': a['sha256'] == sec['sha256'],
                  'A_read_rev': a['read_rev'],
                  'B_sha_matches_any_section': b['sha256'] in {s['sha256'] for s in secs.values()},
                  'B_read_rev': b['read_rev']}

    elif VARIANT == 'provenance':
        os.makedirs(os.path.join(D, REKEY_C0, 'traces'), exist_ok=True)
        namemap = {}
        for name in sorted(os.listdir(os.path.join(D, REKEY_C1, 'traces'))):
            src = os.path.join(D, REKEY_C1, 'traces', name)
            dst = os.path.join(D, REKEY_C0, 'traces', name)
            shutil.copyfile(src, dst)
            namemap[REKEY_C1 + '/traces/' + name] = REKEY_C0 + '/traces/' + name
        shutil.rmtree(os.path.join(D, REKEY_C1))
        for e in entries:
            tr = e.get('traces') or []
            if not any(isinstance(t, str) and t.startswith(REKEY_C1 + '/') for t in tr):
                continue
            e['traces'] = [namemap[t] for t in tr]
            e['read_rev'] = C0
        # every reader report now claims it read C0, but keeps the C1 section sha
        for name in os.listdir(os.path.join(D, '.ufo/waves/round-54/w1')):
            if not name.endswith('.json'):
                continue
            p = os.path.join(D, '.ufo/waves/round-54/w1', name)
            d = json.load(open(p))
            d['cand'] = C0
            with open(p, 'w') as fh:
                json.dump(d, fh, indent=1)
                fh.write('\n')
        c0_skill = subprocess.run(
            ['git', '-C', S + '/clone', 'show', C0 + ':SKILL.md'],
            capture_output=True, env=env, check=True).stdout
        c0_secs = {s['heading']: s for s in mod.sectionize(c0_skill)}
        detail = {'C0_section_sha': c0_secs[HEADING]['sha256'],
                  'C1_section_sha_recorded': secs[HEADING]['sha256'],
                  'sha_equal': c0_secs[HEADING]['sha256'] == secs[HEADING]['sha256'],
                  'read_rev': C0}
    else:
        print('variant must be split or provenance')
        return 2

    with open(os.path.join(D, LEDGER), 'w') as fh:
        json.dump(ledger, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    git(['add', '-A'])
    git(['-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
         'commit', '--quiet', '-m', 'probe: %s' % VARIANT])
    print('PROBE %s dir=%s head=%s %s'
          % (VARIANT, D, git(['rev-parse', 'HEAD']).stdout.decode().strip(),
             json.dumps(detail, sort_keys=True)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
