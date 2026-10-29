import sys, os, json, subprocess, importlib.util, hashlib
sys.dont_write_bytecode = True
exec(open(os.environ['S'] + '/build.py').read().split('# ---- base-anchored evidence')[0])  # reuse constants + loader only
clone = os.environ['S'] + '/clone'
spot_sha = hashlib.sha256(m.show(LANE, BASE, SPOT)).hexdigest()
def git(*a):
    return subprocess.run(['git', '-C', clone] + list(a), capture_output=True, check=True)
def commit_ledger(rows, msg):
    git('checkout', '-q', '--detach', BASE)
    open(clone + '/corpus/routed-defects.json', 'w').write(json.dumps({'schema': 'x', 'defects': rows}))
    git('add', 'corpus/routed-defects.json')
    subprocess.run(['git', '-C', clone, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-q', '-m', msg], check=True)
    return git('rev-parse', 'HEAD').stdout.decode().strip()
def d(i):
    return {'id': i, 'round': 54, 'file': SPOT, 'line': 0, 'end': 0, 'routed_at': RA, 'file_sha256': spot_sha,
            'keys': {'R54.9': ['merge/tameshi', 'w1-registry.json', 'staged=81', 'reviewers=5'],
                     'R54.10': ['controls-a.stdout', 'CTL_R53', 'r53-counter-at-88afa941']}[i]}
lesson_ok = {'path': 'corpus/lessons/round-54.md', 'lines': '51-52', 'excerpt': 'The other 80 staged `merge/tameshi` entries'}
lesson_ok_full = {'path': 'corpus/lessons/round-54.md', 'lines': '51-52', 'excerpt': '- **The other 80 staged `merge/tameshi` entries** — REFUSED for the same capacity reason; they stay reserved by document.'}
scor = {'path': 'SCORECARD.md', 'lines': '2694-2696', 'excerpt': 'Corrected: `reviewers=5 attack=21/76 seats=76` (27.6 %) from `.ufo/waves/round-54/w1-registry.json`, and `staged=81` staged `.md` files under `merge/tameshi/knowledge` (read-only count of the source package).'}
ctl = {'path': '.ufo/evidence/round-54/control/controls-a.stdout', 'lines': '3-3', 'excerpt': 'CTL CTL_R53 C1_R54: rev=88afa9415454 c0=none credited=58 lost=6 rekeyed=0/7 readers=0/7 monitor=6/58 unstable=0 total=4 C1_R54_PASS=false'}
scorctl = {'path': 'SCORECARD.md', 'lines': '2700-2702', 'excerpt': 'Corrected: `controls-a.stdout`\'s `CTL CTL_R53` line prints `rekeyed=0/7`; the `rekeyed=0/30` reading belongs to `control/r53-counter-at-88afa941.stdout`, the round-53 counter\'s own bytes run at the round-53 final revision.'}
variants = {
 'N1_excerpt_84_not_in_lines': ({'id': 'R54.9', 'status': 'fixed', 'commit': FIX, 'evidence': [{'path': 'corpus/lessons/round-54.md', 'lines': '51-52', 'excerpt': 'The other 84 staged `merge/tameshi` entries'}, scor]}, 'R54.9'),
 'N2_commit_is_routed_at': ({'id': 'R54.10', 'status': 'fixed', 'commit': RA, 'evidence': [scorctl, ctl]}, 'R54.10'),
 'N3_commit_base_not_fix': ({'id': 'R54.9', 'status': 'fixed', 'commit': BASE, 'evidence': [lesson_ok_full, scor]}, 'R54.9'),
 'N4_declined_short_reason': ({'id': 'R54.10', 'status': 'declined', 'reason': 'too short', 'evidence': [ctl]}, 'R54.10'),
 'P1_positive_fixed_R54.10': ({'id': 'R54.10', 'status': 'fixed', 'commit': FIX, 'evidence': [scorctl, ctl]}, 'R54.10'),
}
out = {}
for name, (row, i) in variants.items():
    rev = commit_ledger([row], name)
    notes = []
    _, counts, stat, total, _n = m.measure(clone, rev, [d(i)], True, fixed_floor=0, declined_cap=99,
                                            explain=lambda *a: notes.append(' '.join(str(x) for x in a)), this_round_floor=0, base=BASE)
    out[name] = {'total': total - counts['extra'], 'bad': {k: v for k, v in counts.items() if v and k != 'extra'}, 'notes': notes}
print(json.dumps(out, indent=1))
