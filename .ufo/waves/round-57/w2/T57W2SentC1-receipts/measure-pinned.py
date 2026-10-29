#!/usr/bin/env python3
"""Round-57 C1 counter (calibration): routed-defect dispositions agree with the tree (rounds 50-56 closures).

Usage:
  python3 measure.py --lane LANE --rev REV [--work DIR] [--explain]
  python3 measure.py --selftest [--work DIR]

Successor of the round-50 counter (`.ufo/evidence/round-50/c1/measure.py`), which it inherits verbatim for the
fixed/open/declined agreement rules. The frozen statement set is the routed items of the seven closure
spot-checks of rounds 50-56 (`.ufo/evidence/round-57/c1/defects.json`, sha256 pinned below). The lane's
self-assessment is the ledger `corpus/routed-defects.json` at REV: one row per item, {id, status, evidence[],
commit?, reason?}. Only git objects at REV (and BASE) are read; the working tree is never read.

Arms (all must be clean for PASS):
  rows/agree  every item of the set has exactly one row (rows=<have>/<N>) and every such row agrees (agree=<n>/<N>);
              a row whose id is neither in the set nor one of the original rows is `extra`, a second row for an
              id is `duplicate`;
  old49       the original rows (every row of the ledger at BASE, rounds 40-49) are present at REV exactly once
              and equal as canonical JSON objects to their bytes at BASE (old49=ok|CHANGED);
  spot        every spot-check file is byte-equal (sha256) to the frozen set at REV, and every expected
              round-50..56 spot-check is in the set (spot=ok|DRIFT);
  floors      fixed >= FIXED_FLOOR, declined <= DECLINED_CAP, and at least THIS_ROUND_FLOOR fixes carried by
              commits after BASE (a ledger that calls everything open or declined, or only cites history,
              does not pass).

A row agrees with the tree when:
  * every evidence item {path, lines "a-b", excerpt} resolves at REV: the path is a lane file that is not
    a spot-check of the set, not the ledger and not this round's C1 instrument or control, contract or freeze
    record (HARD) (`.ufo/waves/` and `.ufo/reports/` paths only when the path ends with one of the item's
    keys), 1 <= a <= b <= len, b - a <= 30, and the whitespace-normalised excerpt (15-400 chars) occurs in
    lines a..b;
  * at least one evidence item carries one of the item's keys (case-insensitive, in the excerpt or as the
    path's suffix);
  * fixed: `commit` is a full hash, an ancestor of REV (or REV) and not an ancestor of the commit that
    added the item's spot-check (`routed_at`); at least one keyed evidence item is in a path that commit
    touches, its excerpt is absent from that path at `routed_at`, and its lines carry none of ACK_WORDS
    (a planned/carried line acknowledges a defect, it does not fix it);
  * open: the item id is named in the newest `**Planned (round` paragraph of SCORECARD.md at REV;
  * declined: a reason of at least 40 characters.

What it cannot see: that a keyed, new excerpt really resolves the defect (semantic support). That is
attacked per row by wave-2 seats and sampled by the closure; and whether the set is the complete set of
routed items (extractor recall).

Last stdout line: `C1_R57: self=<sha12> rev=<rev12> rows=<have>/<N> agree=<n>/<N> old49=<ok|CHANGED> fixed=<n>
declined=<n> thisround=<n> spot=<ok|DRIFT> total=<n> C1_R57_PASS=<true|false>`; exit 0 iff PASS, 1 otherwise, 2 on
setup error. With --explain the per-term tally (`C1_R57_TERMS: ...`) and one EXPLAIN line per refusal precede it.
`--selftest` prints `C1_R57_SELFTEST: n/n pass` (exit 0 iff every case passes).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

DEFECTS_PATH = '.ufo/evidence/round-57/c1/defects.json'
DEFECTS_SHA256 = 'bef2293ba3db863b03247e9867b11aa2501aa54af0b098ce0f974817f485dee9'
LEDGER = 'corpus/routed-defects.json'
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
OLD_COUNT = 49
EXPECTED_SPOTS = tuple('corpus/lessons/round-%d-verifier-spotcheck.md' % r for r in range(50, 57))
STATUSES = ('fixed', 'open', 'declined')
# Amendment 1 (L1, before any scoring; contract amendments[0]): the round-50 floors (fixed >= 20, declined <= 14)
# are replaced by the blind-panel arm below - a floor on a status rewards claiming, not agreeing (wave-1 critic
# T57W1CritClaimShape B2, T57W1CritC1). They stay as arms with non-binding values so the verdict line is stable.
FIXED_FLOOR = 0
THIS_ROUND_FLOOR = 6
DECLINED_CAP = 999
PANEL_PATH = '.ufo/evidence/round-57/c1/panel.json'
PANEL_SHA256 = '0000000000000000000000000000000000000000000000000000000000000000'
PANEL_ALLOWED = 5
MAX_SPAN = 30
ACK_WORDS = ('planned', 'carried', 'still open', 'not worked', 'stay open', 'stays open', 'remain open',
             'remains open', 'routed to round', 'not fixed', 'unfixed', 'not landed')
HEX40 = re.compile(r'^[0-9a-f]{40}$')
LINES = re.compile(r'^(\d+)-(\d+)$')
PLANNED_ID = re.compile(r'\bR5[0-6]\.\d+\b')
SOFT = ('.ufo/waves/', '.ufo/reports/')
HARD = ('.ufo/evidence/round-57/c1/', '.ufo/evidence/round-57/control/', '.ufo/evidence/round-57/contract.json',
        '.ufo/evidence/round-57/freeze.json')
TERMS = ('missing', 'extra', 'duplicate', 'old49', 'spotcheck_changed', 'defects_pin', 'bad_status',
         'evidence_bad', 'key_miss', 'fixed_bad', 'open_unplanned', 'declined_bad', 'fixed_short',
         'declined_over', 'this_round_short', 'panel_pin', 'panel_over', 'base_status_bad')


class Setup(Exception):
    pass


def git(lane, *args, check=True):
    proc = subprocess.run(['git', '-C', lane] + list(args), capture_output=True)
    if check and proc.returncode != 0:
        raise Setup('git %s: %s' % (' '.join(args), proc.stderr.decode('utf-8', 'replace').strip()))
    return proc


def show(lane, rev, path):
    proc = git(lane, 'show', '%s:%s' % (rev, path), check=False)
    return proc.stdout if proc.returncode == 0 else None


def norm(text):
    return ' '.join(text.split())


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def is_ancestor(lane, a, b):
    return git(lane, 'merge-base', '--is-ancestor', a, b, check=False).returncode == 0


def touched(lane, commit):
    out = git(lane, 'diff-tree', '--no-commit-id', '--name-only', '-r', '--root', '-m', commit).stdout
    return set(out.decode('utf-8', 'replace').split('\n')) - {''}


def ledger_rows(blob):
    """Rows of a ledger blob: [] when absent, unparsable or not shaped {defects: [...]}."""
    if blob is None:
        return []
    try:
        doc = json.loads(blob.decode('utf-8'))
    except ValueError:
        return []
    rows = doc.get('defects', []) if isinstance(doc, dict) else []
    return rows if isinstance(rows, list) else []


def planned_ids(lane, rev):
    blob = show(lane, rev, 'SCORECARD.md')
    if blob is None:
        return set()
    lines = blob.decode('utf-8', 'replace').split('\n')
    start, best = None, -1
    for i, line in enumerate(lines):
        m = re.match(r'\*\*Planned \(round (\d+)\)', line)
        if m and int(m.group(1)) >= best:
            start, best = i, int(m.group(1))
    if start is None:
        return set()
    para = []
    for line in lines[start:]:
        if not line.strip():
            break
        para.append(line)
    return set(PLANNED_ID.findall(' '.join(para)))


def has_key(item, keys):
    # Amendment 1: a key matches as a whole token (not a substring of a longer word) or as a whole path suffix.
    low = norm(item.get('excerpt', ''))
    path = item.get('path', '')
    for k in keys:
        if path == k or path.endswith('/' + k):
            return True
        if re.search(r'(?<![\w-])' + re.escape(k) + r'(?![\w-])', low, re.IGNORECASE):
            return True
    return False


def check_evidence(lane, rev, item, keys, spotchecks, cache):
    """Return None when the evidence item resolves at REV, else a reason."""
    if not isinstance(item, dict):
        return 'not-an-object'
    path, lines, excerpt = item.get('path'), item.get('lines'), item.get('excerpt')
    if not all(isinstance(v, str) for v in (path, lines, excerpt)):
        return 'fields'
    if (path in spotchecks or path == LEDGER or path.startswith('/') or '..' in path.split('/')
            or path.startswith(HARD)):
        return 'excluded-path'
    if path.startswith(SOFT) and not any(path.endswith(k) for k in keys):
        return 'soft-excluded-path'
    m = LINES.match(lines)
    if not m:
        return 'lines-form'
    a, b = int(m.group(1)), int(m.group(2))
    ex = norm(excerpt)
    if not (15 <= len(ex) <= 400):
        return 'excerpt-length'
    key = (rev, path)
    if key not in cache:
        blob = show(lane, rev, path)
        cache[key] = None if blob is None else blob.decode('utf-8', 'replace').split('\n')
    text = cache[key]
    if text is None:
        return 'path-absent'
    if not (1 <= a <= b <= len(text)) or b - a > MAX_SPAN:
        return 'lines-range'
    if ex not in norm('\n'.join(text[a - 1:b])):
        return 'excerpt-not-in-lines'
    return None


def judge(lane, rev, d, row, planned, cache, spotchecks, base, stat, note):
    """Judge one new row. Returns the fault term (a TERMS key) or None when the row agrees."""
    status = row.get('status')
    if status not in STATUSES:
        note('bad-status', d['id'], status)
        return 'bad_status'
    sab = row.get('status_at_base')
    if sab not in STATUSES or (sab == 'fixed' and status != 'fixed'):
        note('base-status', d['id'], sab, status)
        return 'base_status_bad'
    stat[status] += 1
    evidence = row.get('evidence')
    if not isinstance(evidence, list) or not evidence:
        note('evidence-empty', d['id'])
        return 'evidence_bad'
    good, bad = [], False
    for item in evidence:
        why = check_evidence(lane, rev, item, d['keys'], spotchecks, cache)
        if why is not None:
            bad = True
            note('evidence-bad', d['id'], why, item.get('path') if isinstance(item, dict) else item)
        else:
            good.append(item)
    if bad:
        return 'evidence_bad'
    keyed = [item for item in good if has_key(item, d['keys'])]
    if not keyed:
        note('key-miss', d['id'])
        return 'key_miss'
    if status == 'fixed':
        commit = row.get('commit')
        ok = isinstance(commit, str) and HEX40.match(commit) is not None
        ok = ok and git(lane, 'cat-file', '-e', (commit or '') + '^{commit}', check=False).returncode == 0
        ok = ok and is_ancestor(lane, commit, rev) and not is_ancestor(lane, commit, d['routed_at'])
        if not ok:
            note('fixed-commit', d['id'], commit)
            return 'fixed_bad'
        if (sab == 'fixed') != is_ancestor(lane, commit, base):
            note('fixed-base-incoherent', d['id'], sab, commit)
            return 'fixed_bad'
        files = touched(lane, commit)
        fresh = False
        # Amendment 1 (wave-1 critics F1): the excerpt must be introduced BY the commit (absent at its first
        # parent), and the commit must be tied to the item: the evidence path is named by the item's own text,
        # or the commit message names the item id. A commit that only quotes an excerpt into a new file under
        # an unrelated message no longer passes.
        parents = git(lane, 'rev-list', '--parents', '-n', '1', commit).stdout.decode().split()[1:]
        msg = git(lane, 'log', '-1', '--format=%B', commit).stdout.decode('utf-8', 'replace')
        names_id = re.search(r'(?<![\w.])' + re.escape(d['id']) + r'(?!\d)', msg) is not None
        item_text = d.get('text', '') + ' ' + d.get('extended_text', '')
        for item in keyed:
            if item['path'] not in files:
                continue
            if not (names_id or item['path'] in item_text or os.path.basename(item['path']) in item_text):
                continue
            then = show(lane, d['routed_at'], item['path'])
            if then is not None and norm(item['excerpt']) in norm(then.decode('utf-8', 'replace')):
                continue
            prev = show(lane, parents[0], item['path']) if parents else None
            if prev is not None and norm(item['excerpt']) in norm(prev.decode('utf-8', 'replace')):
                continue
            a, b = (int(x) for x in item['lines'].split('-'))
            span = ' '.join(cache[(rev, item['path'])][a - 1:b]).lower()
            if any(w in span for w in ACK_WORDS):
                continue
            fresh = True
            break
        if not fresh:
            note('fixed-not-new', d['id'])
            return 'fixed_bad'
        if not is_ancestor(lane, commit, base):
            stat['fixed_this_round'] += 1
    elif status == 'open':
        if d['id'] not in planned:
            note('open-unplanned', d['id'])
            return 'open_unplanned'
    else:
        reason = row.get('reason')
        if not isinstance(reason, str) or len(norm(reason)) < 40:
            note('declined-reason', d['id'])
            return 'declined_bad'
    return None


def measure(lane, rev, defects, defects_pin_ok, fixed_floor=FIXED_FLOOR, declined_cap=DECLINED_CAP,
            this_round_floor=THIS_ROUND_FLOOR, base=BASE, old_expect=OLD_COUNT, expected_spots=EXPECTED_SPOTS,
            explain=None, panel_pin=None, panel_allowed=PANEL_ALLOWED):
    rev = git(lane, 'rev-parse', '--verify', rev + '^{commit}').stdout.decode().strip()
    base = git(lane, 'rev-parse', '--verify', base + '^{commit}').stdout.decode().strip()
    if not is_ancestor(lane, base, rev):
        raise Setup('BASE %s is not an ancestor of REV %s' % (base[:12], rev[:12]))
    counts = {t: 0 for t in TERMS}
    counts['defects_pin'] = 0 if defects_pin_ok else 1
    stat = {'fixed': 0, 'open': 0, 'declined': 0, 'fixed_this_round': 0}
    note = explain if explain is not None else (lambda *a: None)
    ids = [d['id'] for d in defects]
    if len(set(ids)) != len(ids):
        raise Setup('duplicate ids in the frozen set')
    spotchecks = {}
    for d in defects:
        spotchecks.setdefault(d['file'], d['file_sha256'])
    spot_bad = 0
    for path in expected_spots:
        if path not in spotchecks:
            spot_bad += 1
            note('spotcheck-not-in-set', path)
    for path, sha in sorted(spotchecks.items()):
        blob = show(lane, rev, path)
        if blob is None or hashlib.sha256(blob).hexdigest() != sha:
            spot_bad += 1
            note('spotcheck-changed', path)
    counts['spotcheck_changed'] = spot_bad
    # arm old49: every row of the ledger at BASE, exactly once, canonically equal at REV
    old = {}
    old_rows = ledger_rows(show(lane, base, LEDGER))
    for row in old_rows:
        old.setdefault(row.get('id') if isinstance(row, dict) else None, canon(row))
    if len(old_rows) != old_expect or len(old) != old_expect or None in old:
        raise Setup('ledger at BASE holds %d rows (%d ids), expected %d' % (len(old_rows), len(old), old_expect))
    if set(old) & set(ids):
        raise Setup('the frozen set names an id already in the BASE ledger')
    rows = ledger_rows(show(lane, rev, LEDGER))
    by_id, old_seen, known = {}, {}, set(ids)
    for row in rows:
        rid = row.get('id') if isinstance(row, dict) else None
        if rid in old:
            old_seen.setdefault(rid, []).append(canon(row))
            continue
        if rid not in known:
            counts['extra'] += 1
            note('extra', rid)
            continue
        if rid in by_id:
            counts['duplicate'] += 1
            note('duplicate', rid)
            continue
        by_id[rid] = row
    for rid, was in sorted(old.items()):
        seen = old_seen.get(rid, [])
        if len(seen) != 1 or seen[0] != was:
            counts['old49'] += 1
            note('old-row-changed', rid, len(seen))
    planned = planned_ids(lane, rev)
    cache = {}
    agree = 0
    for d in defects:
        row = by_id.get(d['id'])
        if row is None:
            counts['missing'] += 1
            note('missing', d['id'])
            continue
        fault = judge(lane, rev, d, row, planned, cache, spotchecks, base, stat, note)
        if fault is None:
            agree += 1
        else:
            counts[fault] += 1
    counts['fixed_short'] = max(0, fixed_floor - stat['fixed'])
    counts['declined_over'] = max(0, stat['declined'] - declined_cap)
    counts['this_round_short'] = max(0, this_round_floor - stat['fixed_this_round'])
    # Amendment 1: blind-panel arm. The panel file holds an independent verdict per id (fixed|open|declined AT BASE),
    # produced by seats that never saw the ledger rows; each new row's `status_at_base` must equal it, at most
    # `panel_allowed` disagreements (the adjudicated residue). panel_pin None disables the arm (selftest only).
    if panel_pin is not None:
        pblob = show(lane, rev, PANEL_PATH)
        if pblob is None or hashlib.sha256(pblob).hexdigest() != panel_pin:
            counts['panel_pin'] = 1
            note('panel-pin', PANEL_PATH)
        else:
            verdicts = json.loads(pblob.decode('utf-8')).get('verdicts', {})
            dis = [d['id'] for d in defects if (by_id.get(d['id']) or {}).get('status_at_base') != verdicts.get(d['id'])]
            counts['panel_over'] = max(0, len(dis) - panel_allowed)
            stat['panel_disagree'] = len(dis)
            for rid in dis:
                note('panel-disagree', rid)
    total = sum(counts.values())
    return {'rev': rev, 'counts': counts, 'stat': stat, 'total': total, 'have': len(by_id), 'n': len(defects),
            'agree': agree}


def self_sha():
    with open(os.path.abspath(__file__), 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def terms_line(res):
    parts = ['%s=%d' % (k, res['stat'][k]) for k in ('fixed', 'open', 'declined', 'fixed_this_round')]
    parts += ['%s=%d' % (t, res['counts'][t]) for t in TERMS]
    return 'C1_R57_TERMS: ' + ' '.join(parts)


def verdict(res):
    c = res['counts']
    return ('C1_R57: self=%s rev=%s rows=%d/%d agree=%d/%d old49=%s fixed=%d declined=%d thisround=%d panel=%s spot=%s '
            'total=%d C1_R57_PASS=%s') % (
        self_sha()[:12], res['rev'][:12], res['have'], res['n'], res['agree'], res['n'],
        'ok' if c['old49'] == 0 else 'CHANGED', res['stat']['fixed'], res['stat']['declined'],
        res['stat']['fixed_this_round'],
        ('pin' if c['panel_pin'] else '%d/%d' % (res['stat'].get('panel_disagree', 0), PANEL_ALLOWED)),
        'ok' if c['spotcheck_changed'] == 0 else 'DRIFT', res['total'],
        'true' if res['total'] == 0 else 'false')


def cli(lane, rev, explain, pin=DEFECTS_SHA256, **kw):
    """Run the counter on a lane; returns (exit code, output lines). Raises Setup on a setup error."""
    blob = show(lane, rev, DEFECTS_PATH)
    if blob is None:
        raise Setup('frozen defect set absent at REV: ' + DEFECTS_PATH)
    pin_ok = hashlib.sha256(blob).hexdigest() == pin
    defects = json.loads(blob.decode('utf-8'))['defects']
    out = []
    note = (lambda *x: out.append('EXPLAIN ' + ' '.join(str(v) for v in x))) if explain else None
    kw.setdefault('panel_pin', PANEL_SHA256)
    res = measure(lane, rev, defects, pin_ok, explain=note, **kw)
    if explain:
        out.append(terms_line(res))
    out.append(verdict(res))
    return (0 if res['total'] == 0 else 1), out


# ------------------------------------------------------------------------------------------------
# selftest: builds a fixture repo and runs measure()/cli() end to end. Every arm has a fixture that
# moves its tally away from zero (round-53 lesson: a counter arm that can never fire), asserted on the
# printed verdict line, not only on the internal counters.
# ------------------------------------------------------------------------------------------------
SPOT = """# Round 50 verifier spot-check

## Routed defects (status-neutral)

1. **Extractor pairing.** `BACKTICK_RE` spans newlines; use line-scoped extraction.
2. **Planned item.** The `wave-slots` pointer does not resolve.
3. **Observation.** Nothing to fix; `SHONEN` boxes stay `[~]`.

## Next
"""
SPOT_PATH = 'corpus/lessons/round-50-verifier-spotcheck.md'
OLD_ROWS = [
    {'id': 'R49.1', 'status': 'fixed', 'commit': 'a' * 40, 'seat': 's',
     'evidence': [{'path': 'tools/x.py', 'lines': '1-1', 'excerpt': 'old = 1 sentinel text'}], 'note': 'n1'},
    {'id': 'R49.2', 'status': 'declined', 'reason': 'x' * 45, 'seat': 's',
     'evidence': [{'path': 'SHONEN.md', 'lines': '1-1', 'excerpt': '- [~] box one sentinel'}], 'note': 'n2'}]


def parse_line(text):
    kv = dict(re.findall(r'(\w+)=(\S+)', text))
    return kv


def selftest(work):
    results = []

    def case(name, ok):
        results.append((name, bool(ok)))
        print('SELFTEST %-46s %s' % (name, 'ok' if ok else 'FAIL'))

    repo = tempfile.mkdtemp(prefix='c1r57-', dir=work)
    try:
        def g(*args):
            return subprocess.run(['git', '-C', repo] + list(args), check=True, capture_output=True,
                                  env=dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t',
                                           GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t'))
        g('init', '-q')
        if os.path.realpath(g('rev-parse', '--show-toplevel').stdout.decode().strip()) != os.path.realpath(repo):
            raise Setup('fixture toplevel mismatch')

        def write(path, text):
            full = os.path.join(repo, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, 'w', encoding='utf-8') as fh:
                fh.write(text)

        def commit(msg):
            g('add', '-A')
            g('commit', '-q', '--allow-empty', '-m', msg)
            return g('rev-parse', 'HEAD').stdout.decode().strip()

        write('tools/x.py', 'old = 1\nBACKTICK_RE = old pairing across lines\n')
        write('SHONEN.md', '- [~] box one\n- [~] box two\n')
        write(LEDGER, json.dumps({'schema': 'x', 'defects': OLD_ROWS}))
        c0 = commit('base')
        write(SPOT_PATH, SPOT)
        routed = commit('spot-check')
        write('tools/x.py', 'old = 1\nBACKTICK_RE = re.compile(r"`([^`\\n]+)`")  # line-scoped extraction\n')
        fix = commit('fix')
        write('SCORECARD.md', 'x\n\n**Planned (round 58):** R50.2 the wave-slots pointer.\n')
        write('LOG.md', 'carried: the wave-slots pointer is still open (R50.2)\n')
        c3 = commit('plan')
        sha = hashlib.sha256(SPOT.encode()).hexdigest()
        defects = [{'id': 'R50.%d' % i, 'file': SPOT_PATH, 'file_sha256': sha, 'routed_at': routed, 'keys': k}
                   for i, k in ((1, ['BACKTICK_RE', 'line-scoped']), (2, ['wave-slots']), (3, ['SHONEN', '[~]']))]
        dblob = json.dumps({'defects': defects})
        write(DEFECTS_PATH, dblob)
        commit('defects set')
        dsha = hashlib.sha256(dblob.encode()).hexdigest()
        good = {'defects': [
            {'id': 'R50.1', 'status': 'fixed', 'commit': fix,
             'evidence': [{'path': 'tools/x.py', 'lines': '2-2', 'excerpt': 'BACKTICK_RE = re.compile(r"`([^`\\n]+)`")'}]},
            {'id': 'R50.2', 'status': 'open',
             'evidence': [{'path': 'LOG.md', 'lines': '1-1', 'excerpt': 'the wave-slots pointer is still open'}]},
            {'id': 'R50.3', 'status': 'declined', 'reason': 'an observation, not a defect: promotion is operator-owned',
             'evidence': [{'path': 'SHONEN.md', 'lines': '1-2', 'excerpt': '- [~] box one - [~] box two'}]}]}

        def run(new, old=None, pin=True, floor=1, cap=1, mutate=None, trf=1, base=None, spots=(SPOT_PATH,)):
            rows = json.loads(json.dumps(OLD_ROWS)) if old is None else old
            write(LEDGER, json.dumps({'schema': 'x', 'defects': rows + new['defects']}))
            if mutate:
                mutate()
            rev = commit('ledger')
            res = measure(repo, rev, defects, pin, floor, cap, trf, base or routed, 2, spots)
            return res['counts'], res['stat'], res['total'], parse_line(verdict(res)), res

        def variant(fn):
            doc = json.loads(json.dumps(good))
            fn(doc['defects'])
            return doc

        counts, stat, total, kv, res = run(good)
        case('good ledger passes', total == 0 and stat['fixed'] == 1 and stat['open'] == 1)
        case('good verdict line fields', kv['rows'] == '3/3' and kv['agree'] == '3/3' and kv['old49'] == 'ok'
             and kv['fixed'] == '1' and kv['declined'] == '1' and kv['thisround'] == '1' and kv['spot'] == 'ok'
             and kv['total'] == '0' and kv['C1_R57_PASS'] == 'true')
        counts, _, total, kv, _ = run(good, pin=False)
        case('defects pin mismatch counted', counts['defects_pin'] == 1 and total == 1 and kv['C1_R57_PASS'] == 'false')
        # arm rows / agree
        counts, _, total, kv, _ = run(variant(lambda r: r.pop()))
        case('missing row counted (rows arm)', counts['missing'] == 1 and total == 1 and kv['rows'] == '2/3'
             and kv['agree'] == '2/3')
        counts, _, total, kv, _ = run(variant(lambda r: r.append(dict(r[0]))))
        case('duplicate row counted', counts['duplicate'] == 1 and total == 1)
        counts, _, total, kv, _ = run(variant(lambda r: r.append({'id': 'R99.1', 'status': 'open'})))
        case('extra row counted', counts['extra'] == 1 and total == 1)
        counts, _, total, kv, _ = run(variant(lambda r: r.append({'id': 'R49.3', 'status': 'open'})))
        case('new row in the old id range is extra', counts['extra'] == 1 and kv['old49'] == 'ok')
        counts, _, total, kv, _ = run(variant(lambda r: r[0].update(status='done')))
        case('bad status counted (agree arm)', counts['bad_status'] == 1 and kv['agree'] == '2/3' and kv['rows'] == '3/3')
        counts, _, total, kv, _ = run(variant(lambda r: r[0].update(commit=c0)))
        case('fix commit before routing refused', counts['fixed_bad'] == 1 and kv['agree'] == '2/3')
        counts, _, total, _, _ = run(variant(lambda r: r[0].update(commit='0' * 40)))
        case('unknown commit refused', counts['fixed_bad'] == 1)
        counts, _, total, _, _ = run(variant(lambda r: r[0].update(commit=c3)))
        case('commit not touching evidence refused', counts['fixed_bad'] == 1)
        counts, _, total, _, _ = run(variant(lambda r: r[0]['evidence'][0].update(lines='1-2', excerpt='old = 1 BACKTICK_RE')))
        case('excerpt present at routing refused', counts['fixed_bad'] == 1 or counts['evidence_bad'] == 1)
        counts, _, total, _, _ = run(variant(lambda r: r[1].update(status='fixed', commit=c3)))
        case('ack line is not a fix', counts['fixed_bad'] == 1)
        counts, _, total, _, _ = run(variant(lambda r: r[0]['evidence'][0].update(excerpt='not in the file at all, really')))
        case('excerpt not in lines refused', counts['evidence_bad'] == 1)
        counts, _, total, _, _ = run(variant(lambda r: r[0]['evidence'][0].update(lines='2-40')))
        case('range past end refused', counts['evidence_bad'] == 1)
        counts, _, total, _, _ = run(variant(lambda r: r[2]['evidence'][0].update(path=SPOT_PATH, lines='5-5',
                                                                                  excerpt='1. **Extractor pairing.**')))
        case('spot-check evidence refused', counts['evidence_bad'] == 1)
        counts, _, total, _, _ = run(variant(lambda r: r[2]['evidence'][0].update(path='LOG.md', lines='1-1',
                                                                                  excerpt='the wave-slots pointer is still open')))
        case('unkeyed evidence refused', counts['key_miss'] == 1)
        counts, _, total, _, _ = run(variant(lambda r: r[0].update(status='open')))
        case('open not in Planned refused', counts['open_unplanned'] == 1)
        counts, _, total, _, _ = run(variant(lambda r: r[2].update(reason='short')))
        case('short decline reason refused', counts['declined_bad'] == 1)
        # floors
        counts, _, total, kv, _ = run(good, floor=2)
        case('fixed floor counted', counts['fixed_short'] == 1 and total == 1 and kv['fixed'] == '1')
        counts, _, total, kv, _ = run(good, cap=0)
        case('declined cap counted', counts['declined_over'] == 1 and total == 1 and kv['declined'] == '1')
        counts, stat, total, kv, _ = run(good, base=fix)
        case('fix older than base is not this round', counts['this_round_short'] == 1 and total == 1
             and kv['thisround'] == '0')
        counts, _, total, kv, _ = run(good, trf=2)
        case('this-round floor counted', counts['this_round_short'] == 1 and total == 1)
        # HARD paths
        hards = ('.ufo/evidence/round-57/c1/keys.json', '.ufo/evidence/round-57/control/ctl.json',
                 '.ufo/evidence/round-57/contract.json', '.ufo/evidence/round-57/freeze.json')
        for hard in hards:  # the files exist and are keyed: only the HARD rule can refuse them
            write(hard, 'a keyed line: the wave-slots pointer is resolved here\n')
        for hard in hards:
            counts, _, total, _, _ = run(variant(lambda r, h=hard: r[1]['evidence'][0].update(
                path=h, lines='1-1', excerpt='the wave-slots pointer is resolved here')))
            case('hard path refused: %s' % hard.split('round-57/')[1], counts['evidence_bad'] == 1)
        write('.ufo/evidence/round-52/ok.md', 'a keyed line: the wave-slots pointer is resolved here\n')
        counts, _, total, _, _ = run(variant(lambda r: r[1]['evidence'][0].update(
            path='.ufo/evidence/round-52/ok.md', lines='1-1', excerpt='the wave-slots pointer is resolved here')))
        case('older round evidence path is allowed', counts['evidence_bad'] == 0 and total == 0)
        counts, _, total, _, _ = run(variant(lambda r: r[1]['evidence'][0].update(path='.ufo/waves/r/notes.md')))
        case('soft-excluded wave path refused', counts['evidence_bad'] == 1)
        counts, _, total, _, _ = run(variant(lambda r: r[0]['evidence'][0].update(path='../x.py')))
        case('path escape refused', counts['evidence_bad'] == 1)
        # arm spot
        counts, _, total, kv, _ = run(good, mutate=lambda: write(SPOT_PATH, SPOT + 'edited\n'))
        case('edited spot-check counted (spot arm)', counts['spotcheck_changed'] == 1 and kv['spot'] == 'DRIFT'
             and total == 1)
        write(SPOT_PATH, SPOT)
        counts, _, total, kv, _ = run(good, spots=(SPOT_PATH, 'corpus/lessons/round-51-verifier-spotcheck.md'))
        case('spot-check absent from the set counted', counts['spotcheck_changed'] == 1 and kv['spot'] == 'DRIFT')
        counts, _, total, kv, _ = run(good, mutate=lambda: os.remove(os.path.join(repo, SPOT_PATH)))
        case('deleted spot-check counted', counts['spotcheck_changed'] == 1 and kv['spot'] == 'DRIFT')
        write(SPOT_PATH, SPOT)
        # arm old49
        changed = json.loads(json.dumps(OLD_ROWS))
        changed[0]['note'] = 'rewritten'
        counts, _, total, kv, _ = run(good, old=changed)
        case('rewritten old row counted (old49 arm)', counts['old49'] == 1 and kv['old49'] == 'CHANGED' and total == 1)
        counts, _, total, kv, _ = run(good, old=OLD_ROWS[:1])
        case('deleted old row counted', counts['old49'] == 1 and kv['old49'] == 'CHANGED')
        counts, _, total, kv, _ = run(good, old=OLD_ROWS + [OLD_ROWS[0]])
        case('duplicated old row counted', counts['old49'] == 1 and kv['old49'] == 'CHANGED')
        reordered = json.loads(json.dumps(OLD_ROWS))
        reordered[0] = {k: reordered[0][k] for k in sorted(reordered[0], reverse=True)}
        counts, _, total, kv, _ = run(good, old=list(reversed(reordered)))
        case('key/row order is not a change (canonical)', counts['old49'] == 0 and total == 0)
        # setup errors
        write(LEDGER, json.dumps({'defects': good['defects']}))
        rev = commit('ledger without old rows')
        try:
            measure(repo, rev, defects, True, 1, 1, 1, routed, 3, (SPOT_PATH,))
            raised = False
        except Setup:
            raised = True
        case('BASE ledger row count mismatch is setup', raised)
        branch = g('symbolic-ref', '--short', 'HEAD').stdout.decode().strip()
        head = g('rev-parse', 'HEAD').stdout.decode().strip()
        g('checkout', '-q', '--orphan', 'other')
        write(LEDGER, json.dumps({'defects': OLD_ROWS}))
        other = commit('unrelated base with a valid old ledger')
        g('checkout', '-q', '-f', branch)
        try:
            measure(repo, head, defects, True, 1, 1, 1, other, 2, (SPOT_PATH,))
            raised = False
        except Setup as exc:
            raised = 'not an ancestor' in str(exc)
        case('BASE not an ancestor of REV is setup', raised)
        clash = [dict(defects[0], id='R49.1')] + defects[1:]
        try:
            measure(repo, head, clash, True, 1, 1, 1, routed, 2, (SPOT_PATH,))
            raised = False
        except Setup as exc:
            raised = 'already in the BASE ledger' in str(exc)
        case('set id clashing with a BASE row is setup', raised)
        # cli: exit codes, last line, explain
        run(good)
        rev = g('rev-parse', 'HEAD').stdout.decode().strip()
        rc, out = cli(repo, rev, False, dsha, base=routed, old_expect=2, expected_spots=(SPOT_PATH,),
                      fixed_floor=1, declined_cap=1, this_round_floor=1)
        case('cli good exits 0, verdict is last line', rc == 0 and out[-1].startswith('C1_R57: self=')
             and out[-1].endswith('C1_R57_PASS=true'))
        rc, out = cli(repo, rev, True, dsha, base=routed, old_expect=2, expected_spots=(SPOT_PATH,),
                      fixed_floor=2, declined_cap=1, this_round_floor=1)
        case('cli miss exits 1 with terms line', rc == 1 and out[-1].endswith('C1_R57_PASS=false')
             and out[-2].startswith('C1_R57_TERMS:') and 'fixed_short=1' in out[-2])
        rc, out = cli(repo, rev, True, 'f' * 64, base=routed, old_expect=2, expected_spots=(SPOT_PATH,),
                      fixed_floor=1, declined_cap=1, this_round_floor=1)
        case('cli wrong pin exits 1', rc == 1 and 'defects_pin=1' in out[-2])
        try:
            cli(repo, c0, False, dsha, base=c0, old_expect=2)
            raised = False
        except Setup:
            raised = True
        case('cli absent defect set is setup (exit 2)', raised)
        case('shipped pin is a sha256 or an explicit pending marker',
             re.match(r'^[0-9a-f]{64}$', DEFECTS_SHA256) is not None or DEFECTS_SHA256.startswith('PIN_PENDING'))
    finally:
        shutil.rmtree(repo, ignore_errors=True)
    passed = sum(1 for _, ok in results if ok)
    print('C1_R57_SELFTEST: %d/%d pass' % (passed, len(results)))
    return 0 if passed == len(results) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--work')
    ap.add_argument('--explain', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    try:
        work = a.work or os.environ.get('TMPDIR') or None
        if work:
            os.makedirs(work, exist_ok=True)
            os.environ['TMPDIR'] = work
            tempfile.tempdir = None
        if a.selftest:
            return selftest(work)
        if not a.lane or not a.rev:
            raise Setup('--lane and --rev are required')
        rc, out = cli(a.lane, a.rev, a.explain)
        print('\n'.join(out))
        return rc
    except (Setup, KeyError, ValueError, TypeError, AttributeError) as exc:
        print('C1_R57: setup error: %s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
