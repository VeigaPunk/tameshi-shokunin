#!/usr/bin/env python3
"""Round-50 C1 counter (calibration): routed-defect dispositions agree with the tree.

Usage:
  python3 measure.py --lane LANE --rev REV [--explain]
  python3 measure.py --selftest [--work DIR]

The frozen statement set is the 49 routed items of the ten closure spot-checks of rounds 40-49
(`.ufo/evidence/round-50/c1/defects.json`, sha256 pinned below; built by extract-defects.py at base
e3729de8 with the curated keys of keys.json). The lane's self-assessment is the ledger
`corpus/routed-defects.json` at REV: one row per item, {id, status, evidence[], commit?, reason?}.

A row agrees with the tree when:
  * every evidence item {path, lines "a-b", excerpt} resolves at REV: the path is a lane file that is not
    a spot-check, not the ledger and not this round's C1 instrument (HARD) (`.ufo/waves/` and `.ufo/reports/`
    paths only when the path ends with one of the item's keys), 1 <= a <= b <= len, b - a <= 30, and the whitespace-normalised excerpt
    (15-400 chars) occurs in lines a..b;
  * at least one evidence item carries one of the item's keys (case-insensitive, in the excerpt or as the
    path's suffix);
  * fixed: `commit` is a full hash, an ancestor of REV (or REV) and not an ancestor of the commit that
    added the item's spot-check (`routed_at`); at least one keyed evidence item is in a path that commit
    touches, its excerpt is absent from that path at `routed_at`, and its lines carry none of ACK_WORDS
    (a planned/carried line acknowledges a defect, it does not fix it);
  * open: the item id is named in the newest `**Planned (round` paragraph of SCORECARD.md at REV;
  * declined: a reason of at least 40 characters.
Floors: fixed >= FIXED_FLOOR, declined <= DECLINED_CAP, and at least THIS_ROUND_FLOOR fixes landed by commits
after BASE (a ledger that calls everything open or declined, or only cites history,
does not pass). The spot-check files must be byte-equal to the frozen set.

What it cannot see: that a keyed, new excerpt really resolves the defect (semantic support). That is
attacked per row by wave-2 seats and sampled by the closure.

Last stdout line: `C1_R50: self=<sha12> rev=<rev> ... total=<n> C1_R50_PASS=<true|false>`; exit 0 iff PASS,
1 otherwise, 2 on setup error.
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

DEFECTS_PATH = '.ufo/evidence/round-50/c1/defects.json'
DEFECTS_SHA256 = '6a953e6ea8d3b186444a99a890c3b46ab891ab01c0428d5d2debec204e83cd3f'
LEDGER = 'corpus/routed-defects.json'
STATUSES = ('fixed', 'open', 'declined')
FIXED_FLOOR = 20
THIS_ROUND_FLOOR = 5
DECLINED_CAP = 12
MAX_SPAN = 30
ACK_WORDS = ('planned', 'carried', 'still open', 'not worked', 'stay open', 'stays open', 'remain open',
             'remains open', 'routed to round', 'not fixed', 'unfixed', 'not landed')
HEX40 = re.compile(r'^[0-9a-f]{40}$')
LINES = re.compile(r'^(\d+)-(\d+)$')
SOFT = ('.ufo/waves/', '.ufo/reports/')
HARD = ('.ufo/evidence/round-50/c1/', '.ufo/evidence/round-50/control/', '.ufo/evidence/round-50/contract.json',
        '.ufo/evidence/round-50/freeze.json')
TERMS = ('missing', 'extra', 'duplicate', 'spotcheck_changed', 'defects_pin', 'bad_status', 'evidence_bad',
         'key_miss', 'fixed_bad', 'open_unplanned', 'declined_bad', 'fixed_short', 'declined_over',
         'this_round_short')


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


def is_ancestor(lane, a, b):
    return git(lane, 'merge-base', '--is-ancestor', a, b, check=False).returncode == 0


def touched(lane, commit):
    out = git(lane, 'diff-tree', '--no-commit-id', '--name-only', '-r', '--root', '-m', commit).stdout
    return set(out.decode('utf-8', 'replace').split('\n')) - {''}


def planned_ids(lane, rev):
    blob = show(lane, rev, 'SCORECARD.md')
    if blob is None:
        return set()
    lines = blob.decode('utf-8', 'replace').split('\n')
    start = None
    for i, line in enumerate(lines):
        if line.startswith('**Planned (round'):
            start = i
    if start is None:
        return set()
    para = []
    for line in lines[start:]:
        if not line.strip():
            break
        para.append(line)
    return set(re.findall(r'\bR4\d\.\d+\b', ' '.join(para)))


def has_key(item, keys):
    low = norm(item.get('excerpt', '')).lower()
    path = item.get('path', '')
    return any(k.lower() in low or path.endswith(k) for k in keys)


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


def measure(lane, rev, defects, defects_pin_ok, fixed_floor=FIXED_FLOOR, declined_cap=DECLINED_CAP,
            explain=None, this_round_floor=THIS_ROUND_FLOOR, base=None):
    rev = git(lane, 'rev-parse', '--verify', rev + '^{commit}').stdout.decode().strip()
    counts = {t: 0 for t in TERMS}
    counts['defects_pin'] = 0 if defects_pin_ok else 1
    stat = {'fixed': 0, 'open': 0, 'declined': 0, 'fixed_this_round': 0}
    note = explain if explain is not None else (lambda *a: None)
    spotchecks = {}
    for d in defects:
        spotchecks.setdefault(d['file'], d['file_sha256'])
    for path, sha in sorted(spotchecks.items()):
        blob = show(lane, rev, path)
        if blob is None or hashlib.sha256(blob).hexdigest() != sha:
            counts['spotcheck_changed'] += 1
            note('spotcheck-changed', path)
    raw = show(lane, rev, LEDGER)
    rows = []
    if raw is not None:
        try:
            doc = json.loads(raw.decode('utf-8'))
            rows = doc.get('defects', []) if isinstance(doc, dict) else []
        except ValueError:
            rows = []
    if not isinstance(rows, list):
        rows = []
    by_id = {}
    known = {d['id'] for d in defects}
    for row in rows:
        rid = row.get('id') if isinstance(row, dict) else None
        if rid not in known:
            counts['extra'] += 1
            note('extra', rid)
            continue
        if rid in by_id:
            counts['duplicate'] += 1
            note('duplicate', rid)
            continue
        by_id[rid] = row
    planned = planned_ids(lane, rev)
    cache = {}
    for d in defects:
        row = by_id.get(d['id'])
        if row is None:
            counts['missing'] += 1
            note('missing', d['id'])
            continue
        status = row.get('status')
        if status not in STATUSES:
            counts['bad_status'] += 1
            note('bad-status', d['id'], status)
            continue
        stat[status] += 1
        evidence = row.get('evidence')
        if not isinstance(evidence, list) or not evidence:
            counts['evidence_bad'] += 1
            note('evidence-empty', d['id'])
            continue
        good = []
        bad = False
        for item in evidence:
            why = check_evidence(lane, rev, item, d['keys'], spotchecks, cache)
            if why is not None:
                bad = True
                note('evidence-bad', d['id'], why, item.get('path') if isinstance(item, dict) else item)
            else:
                good.append(item)
        if bad:
            counts['evidence_bad'] += 1
            continue
        keyed = [item for item in good if has_key(item, d['keys'])]
        if not keyed:
            counts['key_miss'] += 1
            note('key-miss', d['id'])
            continue
        if status == 'fixed':
            commit = row.get('commit')
            ok = isinstance(commit, str) and HEX40.match(commit) is not None
            ok = ok and git(lane, 'cat-file', '-e', (commit or '') + '^{commit}', check=False).returncode == 0
            ok = ok and is_ancestor(lane, commit, rev) and not is_ancestor(lane, commit, d['routed_at'])
            if not ok:
                counts['fixed_bad'] += 1
                note('fixed-commit', d['id'], commit)
                continue
            files = touched(lane, commit)
            fresh = False
            for item in keyed:
                if item['path'] not in files:
                    continue
                then = show(lane, d['routed_at'], item['path'])
                if then is not None and norm(item['excerpt']) in norm(then.decode('utf-8', 'replace')):
                    continue
                a, b = (int(x) for x in item['lines'].split('-'))
                span = ' '.join(cache[(rev, item['path'])][a - 1:b]).lower()
                if any(w in span for w in ACK_WORDS):
                    continue
                fresh = True
                break
            if not fresh:
                counts['fixed_bad'] += 1
                note('fixed-not-new', d['id'])
                continue
            if not is_ancestor(lane, commit, base or BASE):
                stat['fixed_this_round'] += 1
        elif status == 'open':
            if d['id'] not in planned:
                counts['open_unplanned'] += 1
                note('open-unplanned', d['id'])
        else:
            reason = row.get('reason')
            if not isinstance(reason, str) or len(norm(reason)) < 40:
                counts['declined_bad'] += 1
                note('declined-reason', d['id'])
    counts['fixed_short'] = max(0, fixed_floor - stat['fixed'])
    counts['declined_over'] = max(0, stat['declined'] - declined_cap)
    counts['this_round_short'] = max(0, this_round_floor - stat['fixed_this_round'])
    total = sum(counts.values())
    return rev, counts, stat, total, len(rows)


BASE = 'e3729de862f73ae080d98fcf522a7081ce16e40a'


def self_sha():
    with open(os.path.abspath(__file__), 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def line(rev, counts, stat, total, nrows, ndefects):
    parts = ['C1_R50: self=%s rev=%s defects=%d rows=%d' % (self_sha()[:12], rev, ndefects, nrows)]
    parts += ['%s=%d' % (k, stat[k]) for k in ('fixed', 'open', 'declined', 'fixed_this_round')]
    parts += ['%s=%d' % (t, counts[t]) for t in TERMS]
    parts.append('total=%d C1_R50_PASS=%s' % (total, 'true' if total == 0 else 'false'))
    return ' '.join(parts)


# ------------------------------------------------------------------------------------------------
# selftest: builds a fixture repo and runs measure() end to end (round-49 mutation finding: the
# round-49 selftests never reached measure()).
# ------------------------------------------------------------------------------------------------
SPOT = """# Round 40 verifier spot-check

## Routed defects (status-neutral)

1. **Extractor pairing.** `BACKTICK_RE` spans newlines; use line-scoped extraction.
2. **Planned item.** The `wave-slots` pointer does not resolve.
3. **Observation.** Nothing to fix; `SHONEN` boxes stay `[~]`.

## Next
"""


def selftest(work):
    results = []

    def case(name, ok):
        results.append((name, bool(ok)))
        print('SELFTEST %-34s %s' % (name, 'ok' if ok else 'FAIL'))

    repo = tempfile.mkdtemp(prefix='c1r50-', dir=work)
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
        c0 = commit('base')
        spot = 'corpus/lessons/round-40-verifier-spotcheck.md'
        write(spot, SPOT)
        routed = commit('spot-check')
        write('tools/x.py', 'old = 1\nBACKTICK_RE = re.compile(r"`([^`\\n]+)`")  # line-scoped extraction\n')
        fix = commit('fix')
        write('SCORECARD.md', 'x\n\n**Planned (round 51):** R40.2 the wave-slots pointer.\n')
        write('LOG.md', 'carried: the wave-slots pointer is still open (R40.2)\n')
        c3 = commit('plan')
        sha = hashlib.sha256(SPOT.encode()).hexdigest()
        defects = [{'id': 'R40.%d' % i, 'file': spot, 'file_sha256': sha, 'routed_at': routed, 'keys': k}
                   for i, k in ((1, ['BACKTICK_RE', 'line-scoped']), (2, ['wave-slots']), (3, ['SHONEN', '[~]']))]
        good = {'defects': [
            {'id': 'R40.1', 'status': 'fixed', 'commit': fix,
             'evidence': [{'path': 'tools/x.py', 'lines': '2-2', 'excerpt': 'BACKTICK_RE = re.compile(r"`([^`\\n]+)`")'}]},
            {'id': 'R40.2', 'status': 'open',
             'evidence': [{'path': 'LOG.md', 'lines': '1-1', 'excerpt': 'the wave-slots pointer is still open'}]},
            {'id': 'R40.3', 'status': 'declined', 'reason': 'an observation, not a defect: promotion is operator-owned',
             'evidence': [{'path': 'SHONEN.md', 'lines': '1-2', 'excerpt': '- [~] box one - [~] box two'}]}]}

        def run(ledger, pin=True, floor=1, cap=1, mutate=None, trf=1, base=None):
            write(LEDGER, json.dumps(ledger))
            if mutate:
                mutate()
            rev = commit('ledger')
            _, counts, stat, total, _ = measure(repo, rev, defects, pin, floor, cap, None, trf, base or routed)
            return counts, stat, total

        def variant(fn):
            doc = json.loads(json.dumps(good))
            fn(doc['defects'])
            return doc

        counts, stat, total = run(good)
        case('good ledger passes', total == 0 and stat['fixed'] == 1 and stat['open'] == 1)
        counts, _, total = run(good, pin=False)
        case('defects pin mismatch counted', counts['defects_pin'] == 1 and total == 1)
        counts, _, total = run(variant(lambda r: r.pop()))
        case('missing row counted', counts['missing'] == 1 and total == 1)
        counts, _, total = run(variant(lambda r: r.append(dict(r[0]))))
        case('duplicate row counted', counts['duplicate'] == 1)
        counts, _, total = run(variant(lambda r: r.append({'id': 'R99.1', 'status': 'open'})))
        case('extra row counted', counts['extra'] == 1)
        counts, _, total = run(variant(lambda r: r[0].update(status='done')))
        case('bad status counted', counts['bad_status'] == 1)
        counts, _, total = run(variant(lambda r: r[0].update(commit=c0)))
        case('fix commit before routing refused', counts['fixed_bad'] == 1)
        counts, _, total = run(variant(lambda r: r[0].update(commit='0' * 40)))
        case('unknown commit refused', counts['fixed_bad'] == 1)
        counts, _, total = run(variant(lambda r: r[0].update(commit=c3)))
        case('commit not touching evidence refused', counts['fixed_bad'] == 1)
        counts, _, total = run(variant(lambda r: r[0]['evidence'][0].update(lines='1-2', excerpt='old = 1 BACKTICK_RE')))
        case('excerpt present at routing refused', counts['fixed_bad'] == 1 or counts['evidence_bad'] == 1)
        counts, _, total = run(variant(lambda r: r[1].update(status='fixed', commit=c3)))
        case('ack line is not a fix', counts['fixed_bad'] == 1)
        counts, _, total = run(variant(lambda r: r[0]['evidence'][0].update(excerpt='not in the file at all, really')))
        case('excerpt not in lines refused', counts['evidence_bad'] == 1)
        counts, _, total = run(variant(lambda r: r[0]['evidence'][0].update(lines='2-40')))
        case('range past end refused', counts['evidence_bad'] == 1)
        counts, _, total = run(variant(lambda r: r[2]['evidence'][0].update(path=spot, lines='5-5',
                                                                             excerpt='1. **Extractor pairing.**')))
        case('spot-check evidence refused', counts['evidence_bad'] == 1)
        counts, _, total = run(variant(lambda r: r[2]['evidence'][0].update(path='LOG.md', lines='1-1',
                                                                             excerpt='the wave-slots pointer is still open')))
        case('unkeyed evidence refused', counts['key_miss'] == 1)
        counts, _, total = run(variant(lambda r: r[1].update(id='R40.2') or r[0].update(status='open')))
        case('open not in Planned refused', counts['open_unplanned'] == 1)
        counts, _, total = run(variant(lambda r: r[2].update(reason='short')))
        case('short decline reason refused', counts['declined_bad'] == 1)
        counts, _, total = run(good, floor=2)
        case('fixed floor counted', counts['fixed_short'] == 1 and total == 1)
        counts, _, total = run(good, cap=0)
        case('declined cap counted', counts['declined_over'] == 1 and total == 1)
        counts, stat, total = run(good, base=fix)
        case('fix older than base is not this round', counts['this_round_short'] == 1 and total == 1)
        counts, _, total = run(variant(lambda r: r[1]['evidence'][0].update(path='.ufo/evidence/round-50/c1/keys.json')))
        case('round-50 instrument path refused', counts['evidence_bad'] == 1)
        counts, _, total = run(good, mutate=lambda: write(spot, SPOT + 'edited\n'))
        case('edited spot-check counted', counts['spotcheck_changed'] == 1)
        write(spot, SPOT)
        counts, _, total = run(variant(lambda r: r[0]['evidence'][0].update(path='../x.py')))
        case('path escape refused', counts['evidence_bad'] == 1)
        counts, _, total = run(variant(lambda r: r[1]['evidence'][0].update(path='.ufo/waves/r/notes.md')))
        case('soft-excluded wave path refused', counts['evidence_bad'] == 1)
        os.remove(os.path.join(repo, LEDGER))
        rev = commit('no ledger')
        _, counts, stat, total, _ = measure(repo, rev, defects, True, 1, 1, None, 1, routed)
        case('absent ledger counts every item missing', counts['missing'] == 3)
    finally:
        shutil.rmtree(repo, ignore_errors=True)
    failed = [n for n, ok in results if not ok]
    print('C1_R50_SELFTEST: cases=%d failed=%d' % (len(results), len(failed)))
    return 0 if not failed else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--work')
    ap.add_argument('--explain', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    try:
        if a.selftest:
            work = a.work or os.environ.get('TMPDIR') or None
            if work:
                os.makedirs(work, exist_ok=True)
            return selftest(work)
        if not a.lane or not a.rev:
            raise Setup('--lane and --rev are required')
        blob = show(a.lane, a.rev, DEFECTS_PATH)
        if blob is None:
            raise Setup('frozen defect set absent at REV: ' + DEFECTS_PATH)
        pin_ok = hashlib.sha256(blob).hexdigest() == DEFECTS_SHA256
        defects = json.loads(blob.decode('utf-8'))['defects']
        explain = (lambda *x: print('EXPLAIN', *x)) if a.explain else None
        rev, counts, stat, total, nrows = measure(a.lane, a.rev, defects, pin_ok, explain=explain)
        print(line(rev, counts, stat, total, nrows, len(defects)))
        return 0 if total == 0 else 1
    except (Setup, KeyError, ValueError) as exc:
        print('C1_R50: setup error: %s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
