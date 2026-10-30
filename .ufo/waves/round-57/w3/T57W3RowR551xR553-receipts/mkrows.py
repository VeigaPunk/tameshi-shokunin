#!/usr/bin/env python3
"""Build the two adjudicated ledger rows (R55.1, R55.3) from the tree at the dry-run revision."""
import json
import subprocess

CLONE = '/fast/scratch/hyaku/tameshi-r57/T57W3RowR551xR553/clone'
REV = '2c51affd37e15cd7cd258d76ba0f5f73ff235924'   # lane master == dry-run HEAD
OUT = '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR551xR553/rows.json'


def show(path, rev=REV):
    out = subprocess.run(['git', '-C', CLONE, 'show', '%s:%s' % (rev, path)],
                         capture_output=True)
    if out.returncode != 0:
        raise SystemExit('missing %s at %s' % (path, rev))
    return out.stdout.decode('utf-8')


def norm(text):
    return ' '.join(text.split())


def span(path, a, b):
    lines = show(path).split('\n')
    return norm('\n'.join(lines[a - 1:b]))


# --- R55.1: the lane's own round-56 C2 counter states the defect class is still refused -------------
R551_PATH = '.ufo/evidence/round-56/c2/measure.py'
R551_LINES = '25-28'
R551_EXCERPT = span(R551_PATH, 25, 28)

# --- R55.3: the round-56 re-key trace binds the lost heading "### Triggers T1-T3 ..." --------------
R553_PATH = '.ufo/evidence/round-21/coldread/rekey-r56-c0137451f5b7/traces/section-18.json'
R553_LINES = '17-19'
R553_EXCERPT = span(R553_PATH, 17, 19)

rows = [
    {
        'id': 'R55.1',
        'status': 'open',
        'evidence': [
            {'path': R551_PATH, 'lines': R551_LINES, 'excerpt': R551_EXCERPT},
        ],
        'seat': 'T57W3RowR551xR553',
        'note': (
            'Adjudicated to the blind panel (T57W2PanelR5410R551, verdict open, commit null; '
            'panel.json detail.R55.1.seat=T57W2PanelR5410R551). Status and status_at_base both open: '
            'nothing is fixed for this id in round 57. The defect still shows at the round base '
            '5e3569969b532310d2b8a3d130901757a3df356b and at C0b adf87899c70d616140a81185a8f9acbbdfb30392: '
            'the committed round-55 C2 receipt .ufo/evidence/round-55/after/c2.stdout is still truncated '
            'mid-run (28 lines, no C2_R55 verdict line) and no committed receipt names C2_R55 at the '
            'round-55 measured revision 4c04c1d3. Evidence is the lane\'s own round-56 C2 counter, whose '
            'red55 arm names exactly this: the round-55 receipt gated against 4c04c1d3 is refused '
            'RECEIPT_REV_ABSENT - the R55.1 class. The prior row said fixed with commit '
            '18bbdab73b26422e33186076be6be433b3358bc1 (round-56\'s green C2_R56 verdict at rev '
            '1b44bace0974); that receipt is a round-56 verdict at round-56\'s own measured revision and '
            'does not repair round 55\'s missing verdict at 4c04c1d3, so the panel is not disproved and '
            'the triage status is not kept. L1 requirement: R55.1 must be named in SCORECARD\'s Planned '
            'paragraph (round 58) - the master SCORECARD does not name it (grep R55\\. = no hit).'
        ),
        'status_at_base': 'open',
    },
    {
        'id': 'R55.3',
        'status': 'fixed',
        'evidence': [
            {'path': R553_PATH, 'lines': R553_LINES, 'excerpt': R553_EXCERPT},
        ],
        'commit': 'c1dd23b3f83f5dff676c4a4482498e87345375ef',
        'seat': 'T57W3RowR551xR553',
        'note': (
            'Adjudicated to the blind panel (T57W2PanelR552R553, verdict fixed, commit '
            'c1dd23b3f83f5dff676c4a4482498e87345375ef; panel.json detail.R55.3.commit = that commit). '
            'Status and status_at_base both fixed. The commit is the round-56 re-key of the 18 lost '
            'cold-read headings ("round-56: bind cold-read headings at C0"); it is a full 40-hex ancestor '
            'of the lane base 5e3569969b532310d2b8a3d130901757a3df356b, is not an ancestor of the routing '
            'commit fa48c06c3669355fd80e8722eb733c1d6dfdd2f8, introduces the excerpted line (the trace '
            'file is new in that commit - absent at its first parent and at fa48c06c) and ties to the item '
            'by the panel commit arm (amendment 2 of the C1 counter). The excerpt names the re-key and '
            'the heading it bound; the key "re-key" is a whole token in it. The prior row\'s commit '
            '8c20d5c351b39d51c8842bccf3ea8dc45171ccfb (the SCORECARD predicate fix) introduces no keyed '
            'excerpt of the re-key and is not what the panel named, so it is replaced. Measured at the '
            'base by the frozen round-21 monitor: calibration_restraint_score 8, 64/64, box3=true - '
            'see the receipts. Caveat recorded for the L1: at C0b the same monitor reads 6 (46/64, '
            'box3=false) because C0/C0b changed the pinned inputs; that regression is wave 3\'s re-bind, '
            'not a defect of this row.'
        ),
        'status_at_base': 'fixed',
    },
]

with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(rows, fh, indent=1, ensure_ascii=False)
    fh.write('\n')
print('wrote', OUT)
print('R55.1 excerpt:', R551_EXCERPT)
print('R55.3 excerpt:', R553_EXCERPT)
