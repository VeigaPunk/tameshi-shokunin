#!/usr/bin/env python3
"""Seat T57W1ScribeItemsR54x1to4: build and verify ledger rows for R54.1-R54.4.

Reuses the round-50 C1 resolver by import (check_evidence, has_key, show, norm, touched,
is_ancestor, ACK_WORDS, HEX40). Writes rows.json; prints one verdict line per row.
"""
import importlib.util, json, os, re, subprocess, sys, hashlib

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
M50 = LANE + '/.ufo/evidence/round-50/c1/measure.py'
OUT = LANE + '/.ufo/waves/round-57/w1/T57W1ScribeItemsR54x1to4'
SEAT = 'T57W1ScribeItemsR54x1to4'
SCRATCH = os.environ['S']

spec = importlib.util.spec_from_file_location('m50', M50)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

SPOT_RE = re.compile(r'^corpus/lessons/round-(\d+)-verifier-spotcheck\.md$')
SPOTS = {}
for p in m.git(LANE, 'ls-tree', '-r', '--name-only', BASE, 'corpus/lessons').stdout.decode().split():
    if SPOT_RE.match(p):
        SPOTS[p] = None
ROUTED_AT = m.git(LANE, 'log', '--diff-filter=A', '--format=%H', BASE, '--',
                  'corpus/lessons/round-54-verifier-spotcheck.md').stdout.decode().split()[-1]
SPOT54 = 'corpus/lessons/round-54-verifier-spotcheck.md'
FIX = '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'


def locate(rev, path, excerpt, maxspan=30):
    """Smallest 1-based line window at rev whose whitespace-normalised text contains excerpt."""
    blob = m.show(LANE, rev, path)
    if blob is None:
        raise SystemExit('path absent at rev: %s' % path)
    text = blob.decode('utf-8', 'replace').split('\n')
    ex = m.norm(excerpt)
    for a in range(len(text)):
        if ex[:12] not in m.norm(text[a]):
            continue
        for b in range(a, min(a + maxspan, len(text))):
            if ex in m.norm(' '.join(text[a:b + 1])):
                # shrink to the tightest window: drop lines the excerpt does not need
                while a < b and ex in m.norm(' '.join(text[a + 1:b + 1])):
                    a += 1
                while b > a and ex in m.norm(' '.join(text[a:b])):
                    b -= 1
                return '%d-%d' % (a + 1, b + 1)
    raise SystemExit('excerpt not located: %s :: %s' % (path, excerpt))


def ev(path, excerpt):
    ex = m.norm(excerpt)
    return {'path': path, 'lines': locate(BASE, path, ex), 'excerpt': ex}


ROWS = [
    {
        'id': 'R54.1', 'status': 'fixed', 'commit': FIX, 'seat': SEAT,
        'keys': ['CTL_POS_c1', 'CTL_MISMATCH', 'ER-R54-1', 'rekeyed=7/7'],
        'evidence': [
            ev('corpus/QUALITY.md',
               '`CTL_POS_c1` line prints `C1_R54_PASS=false` at `rev=077d431e6996` (the freeze) with '
               '`CTL_MISMATCH CTL_POS_c1 expected=true actual=false`, while four round-54 records claimed the control passed.'),
            ev('corpus/lessons/round-54.md',
               '`CTL_MISMATCH` (3 of 7), so it never fired [ER-R54-1, round-55 correction].'),
            ev('SCORECARD.md',
               'Corrected: `CTL_MISMATCH` - `CTL_POS_c1 expected=true actual=false`, `CONTROLS_B: 2/3` at the revision the control cloned.'),
        ],
        'note': ('Fixed by 9cf0146 (round-55 C0 record corrections): SCORECARD ER-R54-1 and the claim row, '
                 'QUALITY 105 erratum falsifier, lesson round-54 lines 77 and 105 now record CTL_MISMATCH and "never fired". '
                 'Residual outside the lane tree: fleet report .ufo/reports/round-54/tameshi.md:162 still reads '
                 '"proven live by the phase-B positive control" (fleet fcb8d8db, unchanged to fleet HEAD).'),
        'verdict_basis': ('The lane-tree sites the item names were corrected at 9cf0146, which touches all three of the '
                          'cited paths; the three excerpts are absent at routed_at 650987a and present at base. '
                          'The fleet report copy is not a lane file and is recorded as a residual.'),
    },
    {
        'id': 'R54.2', 'status': 'fixed', 'commit': FIX, 'seat': SEAT,
        'keys': ['one freeze pointer', 'ER-R54-2', '077d431e', '097985c1'],
        'evidence': [
            ev('SCORECARD.md',
               'The round has **one freeze pointer, `077d431e`** (5 amendments), which the deciding run uses [ER-R54-2].'),
            ev('SCORECARD.md',
               'Corrected: one pointer, `077d431e` (5 amendments), which is what the deciding receipt prints.'),
        ],
        'note': ('Fixed by 9cf0146: SCORECARD round-54 standing text and ER-R54-2 name one freeze pointer, 077d431e. '
                 'Residual outside the lane tree: fleet report .ufo/reports/round-54/tameshi.md:157 still names '
                 'freeze pointer 097985c1 (fleet fcb8d8db, unchanged to fleet HEAD).'),
        'verdict_basis': ('Both lane-side pointer sites (the round standing text and the measured-close entry) were '
                          'rewritten at 9cf0146; both excerpts are absent at 650987a and present at base. '
                          'The fleet report residual is outside the lane tree.'),
    },
    {
        'id': 'R54.3', 'status': 'fixed', 'commit': FIX, 'seat': SEAT,
        'keys': ['total=14', 'total=13', 'ER-R54-3'],
        'evidence': [
            ev('SCORECARD.md',
               '`unusable_exit2=3 docs=0 note=0 sources=0 total=13` false'),
            ev('SCORECARD.md',
               'Old: `total=14` in the C2 claim row. Corrected: `total=13`.'),
        ],
        'note': ('Fixed by 9cf0146: the round-54 C2 claim row prints total=13 (the before receipt value); '
                 'ER-R54-3 records the old and corrected values. The lane tree has no remaining total=14 claim for this row.'),
        'verdict_basis': ('The claim row at 650987a read total=14 (grep at 650987a shows "sources=0 total=14"); '
                          'at base it reads total=13 and ER-R54-3 is present, both excerpts absent at routed_at.'),
    },
    {
        'id': 'R54.4', 'status': 'declined', 'seat': SEAT,
        'keys': ['49280fe5', '8528ee85', 'c2/measure.py'],
        'reason': ('The only surface still carrying the stale c2 digest 49280fe5 is the fleet report '
                   '.ufo/reports/round-54/tameshi.md line 122 (fleet fcb8d8db, unchanged to fleet HEAD). That file is '
                   'outside the lane tree, a lane seat cannot edit it, and the lane record already corrects the value '
                   '(SCORECARD ER-R54-4 names 8528ee85, the pinned c2/measure.py bytes in freeze.json).'),
        'evidence': [
            ev('.ufo/evidence/round-54/freeze.json',
               '"c2/measure.py": "8528ee8555da068519af4159f5f9e0efac8b29de88a53534a7043d7ec007e790"'),
            ev('SCORECARD.md',
               'Old: `49280fe5` for `c2/measure.py`. Corrected: `8528ee85` - the amendment-4 bytes that decided.'),
        ],
        'note': ('Not a lane surface: the defect is the fleet report copy at its line 122 (digest), 157 (pointer) and 162 '
                 '(phrase). Lane-side correction already present at 9cf0146 (ER-R54-4). A fleet-root correction would be '
                 'operator-owned; no lane seat may write it.'),
        'verdict_basis': ('The item names only the fleet report; the lane tree holds the pinned value (freeze.json) and '
                          'the correction (ER-R54-4), both resolvable at base, so the disposition is a fleet-ownership '
                          'declination rather than a lane fix.'),
    },
]

ITEM_TEXT = {}
for r in ROWS:
    ITEM_TEXT[r['id']] = r


def verify_rows(rows, rev):
    """Per-row resolver checks: reuse m.check_evidence, m.has_key, m.is_ancestor, m.touched, m.show, m.norm."""
    cache, out, ok_all = {}, [], True
    for r in rows:
        notes = []
        keys = r['keys']
        assert 2 <= len(keys) <= 5, r['id']
        good = []
        for item in r['evidence']:
            why = m.check_evidence(LANE, rev, item, keys, SPOTS, cache)
            if why is not None:
                notes.append(('evidence-bad', why, item['path']))
            else:
                good.append(item)
        keyed = [it for it in good if m.has_key(it, keys)]
        if len(good) != len(r['evidence']):
            ok_all = False
        if not keyed:
            notes.append(('key-miss',))
            ok_all = False
        if r['status'] == 'fixed':
            commit = r.get('commit')
            c_ok = isinstance(commit, str) and m.HEX40.match(commit) is not None
            c_ok = c_ok and m.is_ancestor(LANE, commit, rev) and not m.is_ancestor(LANE, commit, ROUTED_AT)
            if not c_ok:
                notes.append(('fixed-commit',))
            fresh = False
            files = m.touched(LANE, commit) if c_ok else set()
            for item in keyed:
                if item['path'] not in files:
                    continue
                then = m.show(LANE, ROUTED_AT, item['path'])
                if then is not None and m.norm(item['excerpt']) in m.norm(then.decode('utf-8', 'replace')):
                    notes.append(('present-at-routed-at', item['path']))
                    continue
                a, b = (int(x) for x in item['lines'].split('-'))
                span = ' '.join(cache[(rev, item['path'])][a - 1:b]).lower()
                if any(w in span for w in m.ACK_WORDS):
                    notes.append(('ack-word', item['path']))
                    continue
                fresh = True
                break
            if not fresh:
                notes.append(('fixed-not-new',))
            if not c_ok or not fresh:
                ok_all = False
            r['_this_round'] = not m.is_ancestor(LANE, commit, BASE) if c_ok else None
        elif r['status'] == 'declined':
            if len(m.norm(r['reason'])) < 40:
                notes.append(('declined-reason',))
                ok_all = False
        else:
            ok_all = False
            notes.append(('status-not-handled', r['status']))
        out.append({'id': r['id'], 'status': r['status'], 'keyed_items': len(keyed),
                    'notes': notes, 'ok': not notes})
    return out, ok_all


KEYS = {r['id']: r['keys'] for r in ROWS}


def e2e(rows, defects_rows):
    """Run the round-50 measure() on a scratch clone whose ledger holds exactly these rows."""
    clone = os.path.join(SCRATCH, 'clone')
    if os.path.exists(clone):
        subprocess.run(['rm', '-rf', '--', clone], check=True)
    subprocess.run(['git', 'clone', '-q', '--shared', LANE, clone], check=True)
    top = subprocess.run(['git', '-C', clone, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
    assert top == clone, top
    subprocess.run(['git', '-C', clone, 'checkout', '-q', '--detach', BASE], check=True)
    ledger = {'schema': 'tameshi-routed-defects-v1', 'round': 57,
              'note': 'scratch fixture: R54.1-R54.4 rows only (seat %s)' % SEAT,
              'defects': defects_rows}
    with open(os.path.join(clone, 'corpus/routed-defects.json'), 'w', encoding='utf-8') as fh:
        json.dump(ledger, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    subprocess.run(['git', '-C', clone, 'add', 'corpus/routed-defects.json'], check=True)
    subprocess.run(['git', '-C', clone, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
                    'commit', '-q', '-m', 'scratch ledger for seat verification'], check=True)
    new = subprocess.run(['git', '-C', clone, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    spot_blob = m.show(clone, new, SPOT54)
    sha = hashlib.sha256(spot_blob).hexdigest()
    defects = [{'id': r['id'], 'round': 54, 'file': SPOT54, 'line': 0, 'end': 0, 'routed_at': ROUTED_AT,
                'file_sha256': sha, 'text': r['id'], 'keys': KEYS[r['id']]} for r in rows]
    notes = []
    rev, counts, stat, total, nrows = m.measure(clone, new, defects, True, fixed_floor=0, declined_cap=99,
                                                explain=lambda *a: notes.append(a), this_round_floor=0,
                                                base=BASE)
    return {'clone_rev': rev, 'counts': counts, 'stat': stat, 'total': total, 'rows': nrows, 'notes': notes}


def main():
    clean = []
    for r in ROWS:
        row = {k: v for k, v in r.items() if k not in ('keys', 'verdict_basis', '_this_round')}
        clean.append(row)
    rows_out, ok = verify_rows(ROWS, BASE)
    full = []
    for r in ROWS:
        d = {k: v for k, v in r.items() if k != '_this_round'}
        full.append(d)
    e = e2e(clean, clean)
    report = {'seat': SEAT, 'base': BASE, 'routed_at_round54_spotcheck': ROUTED_AT,
              'per_row_resolver_checks': rows_out, 'all_rows_resolver_ok': ok,
              'end_to_end_round50_measure_on_fixture_ledger': e}
    print(json.dumps(report, indent=1, ensure_ascii=False, default=str))
    with open(os.path.join(OUT, 'rows.json'), 'w', encoding='utf-8') as fh:
        json.dump(full, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    return 0 if ok and e['total'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
