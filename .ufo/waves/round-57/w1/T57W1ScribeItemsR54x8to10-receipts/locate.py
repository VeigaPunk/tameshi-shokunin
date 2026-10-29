import sys, subprocess
sys.dont_write_bytecode = True
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
RA = '650987a0d6fc285b37f0f9e63a3aae864af9cd5a'
def show(rev, path):
    return subprocess.run(['git', '-C', LANE, 'show', '%s:%s' % (rev, path)], capture_output=True).stdout.decode('utf-8', 'replace').split('\n')
want = {
 'corpus/lessons/round-54.md': ['## Round-53 routed defects', 'The other 80 staged', 'REFUSED for the same capacity', '## Mistakes'],
 '.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md': ['SUPERSEDED (round 55', 'recorded in `corpus/lessons/round-55.md`', 'It was edited on the operator', 'scout: "@m_glm53"'],
 'SCORECARD.md': ['**ER-R54-9', 'Corrected: `reviewers=5', 'merge/tameshi/knowledge', '**ER-R54-10', "Corrected: `controls-a.stdout`", "`rekeyed=0/30` reading belongs"],
 '.ufo/evidence/round-54/control/controls-a.stdout': ['CTL CTL_R53'],
}
for p, needles in want.items():
    lines = show(BASE, p)
    print('==', p, 'nlines', len(lines))
    for n in needles:
        hits = [i+1 for i, l in enumerate(lines) if n in l]
        print('  ', repr(n), hits)
