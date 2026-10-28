import json, sys
sys.path.insert(0, '/fast/scratch/hyaku/tameshi-r54/T54W1Sent03')
import attack as A

legacy = A.load_r18()
C0 = A.C0
skill = A.show(C0, 'SKILL.md')
sec = {s['heading']: s for s in legacy.sectionize(skill)}[A.HEADING]
inputs = {p: A.sha_at(C0, p) for p in ('tools/mutate-and-run.sh', 'SHONEN.md',
                                      'corpus/SOURCES.md', 'tools/registry.json')}
tp = A.REKEYDIR + '/traces/' + A.DIRNAME
trace = {
 'schema': 'tameshi-trace-inputs-v1', 'argv': ['git', 'show', C0 + ':SKILL.md'],
 'cwd': A.LIVE, 'root': A.LIVE, 'rev': C0, 'rev_reason': 'dotgit carve-out probe',
 'exit': 0, 'tracked_filter': 'git-object reads only',
 'env_overrides': {'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_NOSYSTEM': '1'},
 'inputs': dict(inputs), 'untracked': [], 'external': {},
 'live_lane_reads': {A.LIVE + '/.git/config': 'c' * 64,
                     A.LIVE + '/.git/objects/pack': 'd' * 64},
 'dropped_home_count': 0}
entry = {
 'skill_sha256': __import__('hashlib').sha256(skill).hexdigest(),
 'start': sec['start'], 'end': sec['end'], 'heading': A.HEADING,
 'sha256': sec['sha256'], 'class': 'instruction', 'verdict': 'executed-ok',
 'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 0,
 'commands_executed_count': 3, 'read_rev': C0, 'inputs': inputs,
 'external_inputs': {}, 'traces': [tp], 'seats': ['T54W1Sent03'],
 'reports': ['.ufo/waves/round-54/w1/T54W1Sent03.md'],
 'carried_from': {'synthetic': 'trace-fabrication attack'}}
raw = A.show(C0, A.LEDGER)
rev = A.make_commit({tp: json.dumps(trace, indent=1, sort_keys=True).encode(),
                     A.LEDGER: A.splice(raw, entry)},
                    'attack: live_lane_reads under the lane .git at bogus digests')
print('commit', rev)
print('entry_reason', legacy.entry_reason(str(A.CLONE), rev, entry, True))
print('live_read_bound(.git/config, c*64)',
      legacy.live_read_bound(str(A.CLONE), rev, A.LIVE + '/.git/config', 'c' * 64))
open(str(A.RECEIPTS / 'dotgit-probe.json'), 'w').write(json.dumps(
    {'commit': rev, 'trace': trace, 'reason': legacy.entry_reason(str(A.CLONE), rev, entry, True)}, indent=1, sort_keys=True))
