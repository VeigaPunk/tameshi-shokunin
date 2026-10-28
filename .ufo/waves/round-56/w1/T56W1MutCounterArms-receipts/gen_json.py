#!/usr/bin/env python3
"""Assemble the machine-readable deliverable from the measured run receipts."""
import json
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r56/T56W1MutCounterArms')
LANE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
OUT = LANE / '.ufo/waves/round-56/w1/T56W1MutCounterArms.json'
RUNS = S / 'runs'
mut = json.loads((S / 'mutants.json').read_text())
fx = json.loads((S / 'fixtures.json').read_text())


def run(label):
    out = (RUNS / (label + '.out')).read_text().splitlines()
    verdict = [l for l in out if l.startswith('C1_R56:')][-1]
    explain = {l.split()[1].split('-')[0]: l[len('EXPLAIN '):]
               for l in out if l.startswith('EXPLAIN ')}
    return {'label': label, 'exit': int((RUNS / (label + '.exit')).read_text().strip()),
            'verdict': verdict, 'explain': explain,
            'meta': json.loads((RUNS / (label + '.meta')).read_text())}


MUTANTS = [
    ('M1_precheck_ok', 'arm 1: the `lost=0 ok` clause',
     'base_pristine', 'base_M1_precheck_ok', 'C', 'C_pristine', 'C_M1_precheck_ok',
     'The clause is reachable and load-bearing: a 65-section page with 64 credited sections and '
     'one floor heading lost makes the frozen precheck exit 0 with `lost=1 ok`, so the pristine '
     'counter fires arm 1 while the mutant does not (total 4 -> 3). This is the only probe that '
     'does not flip PASS: any exit-0-with-lost>0 state forces sections_total > 64, which kills '
     'box3_full_page and therefore also fires arm 2. Arm 1 is detection-redundant with arm 2 '
     '(finding F3).'),
    ('M2_covered64', 'arm 2: the `covered == 64` conjunct',
     'base_pristine', 'base_M2_covered64', 'P', 'P_pristine', 'P_M2_covered64',
     'The literal 64 is the only pin on the page cardinality: on a 65-section page that is fully '
     'credited (65/65, score 8, box3 true) the frozen counter refuses (total=1) and the mutant '
     'passes (total=0). Nothing else in the counter notices a page that grew a section.'),
    ('M3_score8', 'arm 2: the `score == 8` conjunct',
     'base_pristine', 'base_M3_score8', 'S2', 'S2_pristine', 'S2_M3_score8',
     'The score conjunct is the only pin on box 3 being marked and ledger-linked: on a 64/64 page '
     'whose box 3 is unmarked (score 6, box3_full_page true) the frozen counter refuses (total=1) '
     'and the mutant passes (total=0). Not an equivalent mutant.'),
    ('M4_rekeyed', 'arm 3: the `rekeyed != len(frozen)` guard',
     'base_pristine', 'base_M4_rekeyed', 'W', 'W_pristine', 'W_M4_rekeyed',
     'Arm 3 is independently load-bearing on its binding, not on coverage: at W the page is 64/64 '
     'with 18/18 re-keyed entries bound to a read_rev that is not c0, so the frozen counter refuses '
     '(rekeyed=0/18, total=1) and the mutant passes (total=0). At the base revision the same edit '
     'already drops total 5 -> 4 (no re-key directory at all).'),
    ('M5_reader_sha', 'arm 4: the per-report `section_sha256` comparison',
     'base_pristine', 'base_M5_reader_sha', 'R', 'R_pristine', 'R_M5_reader_sha',
     'The per-report sha is the only binding between a reader report and the section bytes at REV: '
     'with one report carrying a wrong sha the frozen counter refuses (readers=17/18, total=1) and '
     'the mutant credits it (readers=18/18, total=0).'),
    ('M6_unstable', 'arm 5: `UNSTABLE_INPUTS`',
     'base_pristine', 'base_M6_unstable', 'U', 'U_pristine', 'U_M6_unstable',
     'Arm 5 is the only check on the round-53/55 loss mechanism: with one entry bound under the '
     're-key pinning LOG.md the frozen counter refuses (unstable=1, total=1) and the mutant passes '
     '(unstable=0, total=0).'),
    ('M7_rowscore', 'arm 6: the `row_score == score` conjunct',
     'base_pristine', 'base_M7_rowscore', 'T', 'T_pristine', 'T_M7_rowscore',
     'This is the R55.3 class. At T the standing row asserts 6 at a commit where the monitor really '
     'reads 6 while REV reads 8; the frozen counter refuses (restate=6, monitor=8/64, total=1) and '
     'the mutant passes. The `same_at_row == row_score` conjunct alone cannot catch it: it is '
     'satisfied by the stale row by construction.'),
    ('M8_ancestor', 'arm 6: the ancestry conjunct',
     'base_pristine', 'base_M8_ancestor', 'A', 'A_pristine', 'A_M8_ancestor',
     'The ancestry conjunct is the only check that the row names a commit in REV\'s history: at A '
     'the row names a side-branch commit that reads 8 but is not an ancestor (score_at_row=None), '
     'the frozen counter refuses (total=1) and the mutant passes (total=0). This is the R55.5 '
     'class (a gate that cannot compare the revision it certifies).'),
]

fixtures = []
for name, rev in sorted(fx['fixtures'].items()):
    entry = {'name': name, 'rev': rev}
    if name == 'S1_superseded':
        entry['superseded'] = True
        entry['note'] = ('first score probe: it edited SHONEN.md while the re-key entries pinned '
                         'SHONEN.md, so the entries drifted (rekeyed=0/18, credited=45, total=3) '
                         'and M3 was undiscriminated; replaced by S_score')
    fixtures.append(entry)

probes = {
    'G': ('G_pristine',), 'C': ('C_pristine', 'C_M1_precheck_ok'),
    'P': ('P_pristine', 'P_M2_covered64'), 'S2': ('S2_pristine', 'S2_M3_score8'),
    'W': ('W_pristine', 'W_M4_rekeyed'), 'R': ('R_pristine', 'R_M5_reader_sha'),
    'U': ('U_pristine', 'U_M6_unstable'), 'T': ('T_pristine', 'T_M7_rowscore'),
    'A': ('A_pristine', 'A_M8_ancestor'), 'S1': ('S_pristine', 'S_M3_score8'),
}

mutants = []
for mid, target, bl, bm, probe, pl, pm, finding in MUTANTS:
    b = (run(bl), run(bm))
    p = (run(pl), run(pm))
    mutants.append({
        'id': mid, 'target': target,
        'old': mut[mid]['old'], 'new': mut[mid]['new'],
        'old_count_in_frozen_bytes': mut[mid]['old_count'],
        'frozen_sha256': mut[mid]['sha256_pristine'],
        'mutant_sha256': mut[mid]['sha256_mutant'],
        'base': {'pristine': b[0], 'mutant': b[1],
                 'discriminated': b[0]['verdict'] != b[1]['verdict']},
        'probe': {'fixture': probe, 'pristine': p[0], 'mutant': p[1],
                  'discriminated': p[0]['verdict'] != p[1]['verdict'],
                  'pristine_exit': p[0]['exit'], 'mutant_exit': p[1]['exit']},
        'verdict': 'KILLED' if (p[0]['verdict'] != p[1]['verdict']
                               or b[0]['verdict'] != b[1]['verdict']) else 'SURVIVED',
        'verdict_basis': 'battery-observable: the run distinguishes the mutated bytes from the '
                         'frozen bytes on the named input (the fleet\'s mutate-and-run convention: '
                         'the refusal assertion fails on the mutant)',
        'self_detected': False,
        'finding': finding,
    })

payload = {
    'seat': 'T56W1MutCounterArms',
    'round': 56, 'wave': 1, 'lane': str(LANE),
    'base': fx['base'],
    'freeze': 'c3e2ca9f020776b3d66c7af854fb82c834674fcf',
    'instrument': {
        'path': '.ufo/evidence/round-56/c1/measure.py',
        'sha256_frozen_blob': '048122cf1c7c65d283366837f155925a03a58ecc2eab70e7085b1796bfccb772',
        'edited': False,
        'sibling_input': {'path': '.ufo/evidence/round-56/c1/lost-headings-at-base.json',
                          'sha256': 'dcfc9f800b8bc7b25851d80ec384b8e8781ead6a5f8adf9f0a5340479282fd4a'},
    },
    'criterion': {
        'fixture_battery': 'a scratch clone of the lane at the base revision plus synthetic commits '
                           'that make the frozen counter green (G) and then break exactly one arm '
                           'per probe',
        'KILLED': 'at least one input distinguishes the mutated bytes from the frozen bytes '
                  '(the refusal assertion the frozen bytes satisfy fails on the mutant)',
        'SURVIVED': 'no input in the battery distinguishes the mutant (equivalent mutant)',
        'INCONCLUSIVE': 'no discriminating input could be built or the run did not complete',
        'self_detected': 'whether the counter itself (its verdict on the lane) notices the edit; '
                         'false for all eight, because the counter has no selftest and judges the '
                         'lane, not itself',
    },
    'green_control': {
        'label': 'G_pristine', 'rev': fx['fixtures']['G_green'], 'run': run('G_pristine'),
        'meaning': 'all six arms are simultaneously satisfiable at one revision; the counter is '
                   'not structurally stuck red, and every arm is reachable',
    },
    'fixtures': fixtures,
    'c0': fx['c0'], 'rekey_dir': fx['rekey_dir'], 'side_commit': fx['side_commit'],
    'probe_runs': {k: [run(x) for x in v] for k, v in probes.items()},
    'mutants': mutants,
    'kill_rate': '8/8 killed by the fixture battery; 0/8 killed by the counter itself',
    'findings': [
        {'id': 'F1', 'claim': 'Every arm is live and the six are jointly satisfiable.',
         'evidence': 'G_pristine total=0 C1_R56_PASS=true at 469127008ea3'},
        {'id': 'F2', 'claim': 'No single-edit weakening of any arm is detectable from inside the '
                              'lane: the counter has no selftest and no arm-isolating mode.',
         'evidence': '8/8 mutants leave the frozen instrument bytes untouched and are visible only '
                     'to the external battery; base-revision runs are byte-identical for 7 of 8 '
                     '(only M4 moves total 5 -> 4)'},
        {'id': 'F3', 'claim': 'Arm 1 is detection-redundant with arm 2.',
         'evidence': 'arm2 green => covered==64 and score==8 => box3_full_page => covered==total '
                     '=> sections_total==64 => lost==0 => arm1 green. Conversely arm1 red with '
                     'exit!=0 means covered<64, so arm2 fires; and arm1 red through `lost=0 ok` '
                     'requires cc>=64 with a differing set, which forces sections_total>64, so '
                     'box3_full_page is false, score is 6 and arm2 fires. Fixtures base, C and G '
                     'show the two arms firing and passing together.'},
        {'id': 'F4', 'claim': 'Each of the other five arms uniquely pins a named property, with a '
                              'fixture that isolates it.',
         'evidence': 'arm2 covered==64 -> page cardinality (P); arm2 score==8 -> box-3 mark and '
                     'ledger link (S2); arm3 read_rev==c0 -> re-key binding (W); arm4 per-report '
                     'sha -> report/bytes binding (R); arm5 -> unstable-input exclusion (U); arm6 '
                     'row_score==score -> R55.3 (T); arm6 ancestry -> R55.5 (A)'},
        {'id': 'F5', 'claim': 'The verdict line is the only aggregate; a weakened arm can vanish '
                              'from `total` without any field showing it.',
         'evidence': 'M1 at base and at C: the arm1 EXPLAIN line is byte-identical between pristine '
                     'and mutant; only total (4 vs 3) moves'},
        {'id': 'F6', 'claim': 'The C1 claim\'s precheck clause (`lost=0`) is not independently '
                              'enforced by the frozen counter.',
         'evidence': 'F3: arm 1 never fires without arm 2. Recommendation only: instruments are '
                     'frozen, so the round\'s record should state the coupling rather than imply '
                     'six independent checks.'},
    ],
    'limits': [
        'Fixture level only: G and every probe are synthetic commits in a scratch clone (ledger '
        'entries, trace receipts, reader reports, SCORECARD rows). Nothing here says the lane at '
        'C0 reads 64/64 score 8; that is wave 2.',
        'The probes isolate one arm each; they are not a property test over the input space. Not '
        'exercised: missing blobs, unresolvable revs, invalid ledger JSON, `ls-tree` failures, a '
        'lane whose page has fewer than 64 sections, and multi-arm simultaneous defects beyond the '
        'base revision.',
        'The 46 base-credited entries are the lane\'s real entries; the 18 re-keyed entries, the '
        '18 reader reports, the fixture calibration rows and (in S2 only) the 34 re-credited '
        'SHONEN-pinning entries are synthetic.',
        'The S2 fixture pins fixture entries to corpus/QUALITY.md; a real C0 re-key that pins '
        'SHONEN.md would drift on any later SHONEN edit (this is what the first S build hit).',
    ],
    'mistakes': [
        {'id': 'S1', 'what': 'First score probe (45d39e3a) edited SHONEN.md while the 18 re-key '
                             'entries pinned SHONEN.md as an input: the entries drifted, '
                             'rekeyed=0/18, credited=45, total=3, and M3 was undiscriminated '
                             '(identical total 3).',
         'fix': 'Rebuilt as S2 (b390a637) with every fixture entry pinned to corpus/QUALITY.md and '
                'the 34 base entries that pinned SHONEN.md re-credited; S2 reads credited=64 '
                'rekeyed=18/18 total=1 and M3 flips PASS.',
         'receipts': ['S_pristine', 'S_M3_score8', 'S2_pristine', 'S2_M3_score8']},
        {'id': 'P1', 'what': 'Predicted before measuring that M1 was an equivalent mutant (the '
                             '`lost=0 ok` clause redundant with exit==0 on the lane\'s 64-section '
                             'page). Fixture C falsified it: exit 0 with lost=1 is reachable on a '
                             '65-section page.', 'fix': 'Kept as a recorded prediction miss.'},
    ],
    'tool_installs': [],
    'receipts': {
        'dir': '.ufo/waves/round-56/w1/T56W1MutCounterArms-receipts/',
        'runs': 'runs/<label>.out|.exit|.meta for every invocation',
        'mutants': 'mutants.json (exact old/new strings, uniqueness counts, sha256)',
        'diffs': 'diff-<mutant>.txt (unified diff against the frozen bytes)',
        'fixtures': 'fixture-provenance.txt, fixtures.json',
        'instrument': 'instrument-provenance.txt',
        'mutate_and_run_misfit': 'misfit.out (CONTROL: RED -> MUTATE: SETUP)',
        'census': 'census.txt (exit 0)',
    },
}
OUT.write_text(json.dumps(payload, indent=2) + '\n')
print('wrote', OUT, len(json.dumps(payload)), 'bytes')
print(json.dumps({m['id']: (m['verdict'], m['probe']['pristine']['exit'],
                            m['probe']['mutant']['exit']) for m in mutants}, indent=1))
