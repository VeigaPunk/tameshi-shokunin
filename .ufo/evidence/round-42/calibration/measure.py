#!/usr/bin/env python3
"""Round-42 C1 counter — self-assessment records vs observed repo state.

Successor of the round-41 counter. Frozen before any seat scored and before
the deciding run. It closes the round-41 closure's routed defects:

  * self-pin: the counter's bytes at the FREEZE revision and the bytes of the
    running file must equal `claims.C1.counter_sha256` in the contract read at
    FREEZE (not at REV), and the copy at REV must be absent (the base) or
    identical, so a revision cannot agree with itself by carrying a re-pinned
    contract;
  * `records` gate: every round-42 record must exist, otherwise the run fails
    (m7/m8/m11 can no longer pass vacuously);
  * line-scoped path extraction: a backtick span never crosses a newline, so
    a mispaired span no longer hides the paths after it (round-41 routed
    defect 1).

Mismatch classes, counted over the committed bytes at REV:

  m6   the SCORECARD standing `sources-registry` row's stated row count
       differs from the `SOURCES.md` S-row count (rule carried unchanged)
  m7   a record cites an S-id the registry does not hold as `mined`
       (`staged:S###` names a package id, not a registry citation)
  m8   a record cites a repo-relative path that does not resolve at REV
  m10  a committed wave receipt asserts `present` for a report path and the
       assertion disagrees with the tree at REV, and no superseding receipt
       covers it (see SUPERSEDE below)
  m11  a record cites a 40-hex revision that is neither a lane commit
       reachable from REV nor a commit in the fleet repo
       (`blob:<hex>` / `tree:<hex>` name non-commit objects and are skipped)

Records: round-41 records (lesson, `## Round 41` SCORECARD section, the
`## 2026-10-25 — round 41` LOG section) for m8/m11 re-audit with the fixed
extractor, and round-42 records (lesson, `## Round 42` SCORECARD section,
`## 2026-10-25 — round 42` LOG section) for m7/m8/m11. A section runs from its
heading to the next heading of the same level or to EOF.

SUPERSEDE: a tracked JSON file under `.ufo/waves/` whose top-level
`supersedes` names a receipt path R covers R only if (a) its own `present`
assertions all agree with the tree at REV and (b) every report path R asserts
on is asserted on again in the superseding file. The superseding file is
itself a receipt and is audited by m10 like any other.

Predicate: `C1_R42_PASS` is true iff self_pin=1, records=6, and m6, m7, m8,
m10 and m11 all count 0.

Counting command:

  python3 .ufo/evidence/round-42/calibration/measure.py --lane LANE --rev REV --freeze FREEZE

Exit 0 iff the predicate is true; 1 if false; 2 on a setup refusal.
`--selftest` runs the built-in fixtures (no lane needed) and exits 0 iff every
fixture case behaves as declared.
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

SELF_REL = '.ufo/evidence/round-42/calibration/measure.py'
CONTRACT_REL = '.ufo/evidence/round-42/contract.json'
FLEET_DEFAULT = '/home/vgpnk/Projects/shokunin'
SOURCES = 'corpus/SOURCES.md'
SCORECARD = 'SCORECARD.md'
LOG = 'LOG.md'
RECORDS = {
    41: ('corpus/lessons/round-41.md', '## Round 41', '## 2026-10-25 — round 41'),
    42: ('corpus/lessons/round-42.md', '## Round 42', '## 2026-10-25 — round 42'),
}
EXPECTED_RECORDS = 6

S_ROW_RE = re.compile(r'^ {0,3}\|[ \t]*S(\d{3,})')
S_CITE_RE = re.compile(r'(?<!staged:)\bS(\d{3,})\b')
BACKTICK_RE = re.compile(r'`([^`\n]+)`')
HEX40_RE = re.compile(r'(?<![0-9a-f:])(?<!blob:)(?<!tree:)([0-9a-f]{40})(?![0-9a-f])')
PATH_PREFIXES = ('corpus/', 'tools/', '.ufo/', 'considerthese/', 'plans/', 'reports/')
PATH_EXACT = {
    'SCORECARD.md', 'LOG.md', 'SHONEN.md', 'PROVINCE.md', 'SKILL.md',
    'README.md', 'MINT.md', 'AGENTS.md',
}
FLEET_ONLY_PREFIXES = ('.ufo/reports/', '.ufo/prompts/', '.ufo/state/')


class Repo:
    """Reads one revision of a git repo."""

    def __init__(self, lane, rev):
        self.lane = lane
        self.rev = rev

    def git(self, *args):
        return subprocess.run(['git', '-C', self.lane] + list(args), capture_output=True)

    def read(self, path):
        proc = self.git('show', '%s:%s' % (self.rev, path))
        if proc.returncode != 0:
            return None
        return proc.stdout

    def text(self, path):
        raw = self.read(path)
        return None if raw is None else raw.decode('utf-8', 'replace')

    def resolves(self, path):
        return self.git('cat-file', '-e', '%s:%s' % (self.rev, path)).returncode == 0

    def tracked(self, prefix):
        proc = self.git('ls-tree', '-r', '--name-only', self.rev, '--', prefix)
        return proc.stdout.decode().split('\n') if proc.returncode == 0 else []

    def ancestor_commit(self, sha):
        if self.git('cat-file', '-e', '%s^{commit}' % sha).returncode != 0:
            return False
        return self.git('merge-base', '--is-ancestor', sha, self.rev).returncode == 0


def section(text, head):
    if text is None:
        return None
    lines = text.split('\n')
    level = len(head) - len(head.lstrip('#'))
    start = None
    for idx, line in enumerate(lines):
        if start is None:
            if line.startswith(head):
                start = idx
            continue
        stripped = line.lstrip('#')
        hashes = len(line) - len(stripped)
        if 0 < hashes <= level and stripped.startswith(' '):
            return '\n'.join(lines[start:idx])
    if start is None:
        return None
    return '\n'.join(lines[start:])


def registry(text):
    rows = {}
    for line in (text or '').splitlines():
        match = S_ROW_RE.match(line)
        if not match:
            continue
        cells = line.split('|')
        rows['S%s' % match.group(1).zfill(3)] = cells[8].strip() if len(cells) > 8 else ''
    return rows


def records_for(repo, rnd):
    lesson, sc_head, log_head = RECORDS[rnd]
    found = []
    found.append(('%s' % lesson, repo.text(lesson)))
    found.append(('%s %s' % (SCORECARD, sc_head), section(repo.text(SCORECARD), sc_head)))
    found.append(('%s %s' % (LOG, log_head), section(repo.text(LOG), log_head)))
    return [(name, body) for name, body in found if body]


def path_tokens(text):
    out = []
    for token in BACKTICK_RE.findall(text or ''):
        raw = re.sub(r':\d+(?:-\d+)?$', '', token.strip()).rstrip('/')
        if any(ch in raw for ch in '<>*{}|()…, $'):
            continue
        if raw.startswith(FLEET_ONLY_PREFIXES):
            continue
        if raw.startswith(PATH_PREFIXES) or raw in PATH_EXACT:
            out.append(raw)
    return out


def walk_present(obj, out):
    if isinstance(obj, dict):
        rep = obj.get('report') if isinstance(obj.get('report'), str) else obj.get('path')
        if isinstance(obj.get('present'), bool) and isinstance(rep, str):
            out.append((rep, obj['present']))
        for value in obj.values():
            walk_present(value, out)
    elif isinstance(obj, list):
        for value in obj:
            walk_present(value, out)


def receipt_audit(repo):
    """Return the m10 mismatch strings for REV."""
    receipts = {}
    for path in repo.tracked('.ufo/waves'):
        if not path.endswith('.json'):
            continue
        try:
            doc = json.loads(repo.read(path).decode('utf-8'))
        except Exception:
            continue
        found = []
        walk_present(doc, found)
        sup = doc.get('supersedes') if isinstance(doc, dict) else None
        if found or sup:
            receipts[path] = (found, sup if isinstance(sup, str) else None)
    stale = {}
    for path, (found, _sup) in receipts.items():
        bad = [(rep, said) for rep, said in found if said != repo.resolves(rep)]
        stale[path] = bad
    covered = set()
    for path, (found, sup) in receipts.items():
        if not sup or sup not in receipts or stale[path]:
            continue
        mine = {rep for rep, _ in found}
        theirs = {rep for rep, _ in receipts[sup][0]}
        if theirs <= mine:
            covered.add(sup)
    out = []
    for path in sorted(stale):
        if path in covered:
            continue
        for rep, said in stale[path]:
            out.append('m10 %s asserts present=%s for %s; tree says %s'
                       % (path, str(said).lower(), rep, str(not said).lower()))
    return out


def audit(repo, fleet):
    mismatches = []
    rows = registry(repo.text(SOURCES))
    score = repo.text(SCORECARD) or ''
    standing = [ln for ln in score.splitlines() if ln.startswith('| sources-registry |')]
    if standing:
        match = re.search(r'(\d+) rows', standing[-1])
        if match and int(match.group(1)) != len(rows):
            mismatches.append('m6 SCORECARD standing row says %s rows, SOURCES.md has %d'
                              % (match.group(1), len(rows)))
    rec41 = records_for(repo, 41)
    rec42 = records_for(repo, 42)
    for _name, text in rec42:
        for raw in sorted(set(S_CITE_RE.findall(text))):
            sid = 'S%s' % raw.zfill(3)
            status = rows.get(sid)
            if status is None:
                mismatches.append('m7 %s cited but absent from the registry' % sid)
            elif status != 'mined':
                mismatches.append('m7 %s cited but status=%s' % (sid, status))
    for name, text in rec41 + rec42:
        for path in sorted(set(path_tokens(text))):
            if not repo.resolves(path):
                mismatches.append('m8 %s cited in %s does not resolve' % (path, name))
    mismatches.extend(receipt_audit(repo))
    for name, text in rec41 + rec42:
        for sha in sorted(set(HEX40_RE.findall(text))):
            if repo.ancestor_commit(sha):
                continue
            if fleet and subprocess.run(['git', '-C', fleet, 'cat-file', '-e', '%s^{commit}' % sha],
                                        capture_output=True).returncode == 0:
                continue
            mismatches.append('m11 %s cited in %s is not a reachable lane commit or a fleet commit'
                              % (sha, name))
    return mismatches, len(rec41) + len(rec42), len(rows)


def count(mismatches, cls):
    return sum(1 for item in mismatches if item.startswith(cls + ' '))


def selftest():
    """Fixture cases; each must behave as declared. Builds throwaway git repos."""
    results = []
    scratch = tempfile.mkdtemp(prefix='tameshi-r42-c1-selftest-')

    def make_repo(files):
        root = tempfile.mkdtemp(dir=scratch)
        subprocess.run(['git', 'init', '-q', root], check=True)
        for rel, body in files.items():
            full = os.path.join(root, rel)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, 'w', encoding='utf-8') as handle:
                handle.write(body)
        subprocess.run(['git', '-C', root, 'add', '-A'], check=True)
        subprocess.run(['git', '-C', root, '-c', 'user.name=t', '-c', 'user.email=t@t',
                        'commit', '-q', '-m', 'fixture'], check=True)
        return root

    base = {
        'corpus/SOURCES.md': '| S001 | a | docs | A | p | l | c | mined | 2026-10-25 | 30d | x |\n',
        'SCORECARD.md': '| sources-registry | x | 1 rows | y |\n## Round 42\nok\n',
        'LOG.md': '## 2026-10-25 — round 42\nok\n',
        'corpus/lessons/round-42.md': 'lesson\n',
    }

    # T1: a mispaired backtick span before a dead path. The round-41 extractor
    # (spans may cross newlines) skips it; the round-42 extractor reports it.
    text = 'opens `here\nand `tools/missing.py` is cited\n'
    old = [t for t in re.findall(r'`([^`]+)`', text) if t.startswith('tools/')]
    new = path_tokens(text)
    results.append(('T1_old_extractor_misses', old == []))
    results.append(('T1_new_extractor_sees', new == ['tools/missing.py']))

    # T2: a stale receipt counts; a valid superseding receipt clears it; a
    # superseding receipt that repeats the stale assertion, or omits the path,
    # does not.
    stale = json.dumps({'seats': {'A': {'report': 'w/A.md', 'present': False}}})
    files = dict(base, **{'.ufo/waves/r/receipt.json': stale, 'w/A.md': 'x\n'})
    repo = Repo(make_repo(files), 'HEAD')
    results.append(('T2_stale_counts', count(receipt_audit(repo), 'm10') == 1))
    good = json.dumps({'supersedes': '.ufo/waves/r/receipt.json',
                       'seats': {'A': {'report': 'w/A.md', 'present': True}}})
    repo = Repo(make_repo(dict(files, **{'.ufo/waves/s/receipt.json': good})), 'HEAD')
    results.append(('T2_superseded_clears', count(receipt_audit(repo), 'm10') == 0))
    junk = json.dumps({'supersedes': '.ufo/waves/r/receipt.json',
                       'seats': {'A': {'report': 'w/A.md', 'present': False}}})
    repo = Repo(make_repo(dict(files, **{'.ufo/waves/s/receipt.json': junk})), 'HEAD')
    results.append(('T2_junk_supersede_still_counts', count(receipt_audit(repo), 'm10') == 2))
    empty = json.dumps({'supersedes': '.ufo/waves/r/receipt.json', 'seats': {}})
    repo = Repo(make_repo(dict(files, **{'.ufo/waves/s/receipt.json': empty})), 'HEAD')
    results.append(('T2_partial_supersede_still_counts', count(receipt_audit(repo), 'm10') == 1))

    # T3: an unreachable 40-hex revision in a record counts; a reachable one does not.
    root = make_repo(base)
    head = subprocess.run(['git', '-C', root, 'rev-parse', 'HEAD'], capture_output=True,
                          text=True).stdout.strip()
    files = dict(base, **{'corpus/lessons/round-42.md':
                          'cites %s and %s and blob:%s\n' % (head, 'f' * 40, 'e' * 40)})
    root2 = make_repo(files)
    subprocess.run(['git', '-C', root2, 'fetch', '-q', root, 'HEAD'], check=True)
    mism, _, _ = audit(Repo(root2, 'HEAD'), '')
    results.append(('T3_unreachable_counts', count(mism, 'm11') == 2))

    # T4: staged:S### is not a registry citation; a bare unknown S-id is.
    files = dict(base, **{'corpus/lessons/round-42.md': 'staged:S159 maps to S001; S777\n'})
    mism, _, _ = audit(Repo(make_repo(files), 'HEAD'), '')
    results.append(('T4_staged_skipped_bare_counted', count(mism, 'm7') == 1))

    # T5: a section ends at the next same-level heading.
    body = section('## Round 42\na `tools/x.py`\n## Round 43\n`tools/y.py`\n', '## Round 42')
    results.append(('T5_section_bounded', 'tools/y.py' not in body))

    shutil.rmtree(scratch, ignore_errors=True)
    for name, ok in results:
        print('SELFTEST %s %s' % (name, 'OK' if ok else 'FAIL'))
    failed = [name for name, ok in results if not ok]
    print('C1_R42_SELFTEST: cases=%d failed=%d' % (len(results), len(failed)))
    return 0 if not failed else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lane')
    parser.add_argument('--rev')
    parser.add_argument('--freeze')
    parser.add_argument('--fleet', default=FLEET_DEFAULT)
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if not (args.lane and args.rev and args.freeze):
        print('C1_R42: SETUP usage --lane --rev --freeze required')
        return 2
    lane = os.path.abspath(args.lane)
    revs = []
    for given in (args.rev, args.freeze):
        proc = subprocess.run(['git', '-C', lane, 'rev-parse', '--verify', given + '^{commit}'],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            print('C1_R42: SETUP rev_unresolved=%s' % given)
            return 2
        revs.append(proc.stdout.strip())
    rev, freeze = revs
    repo = Repo(lane, rev)
    contract_raw = Repo(lane, freeze).read(CONTRACT_REL)
    try:
        pin = json.loads(contract_raw.decode('utf-8'))['claims']['C1']['counter_sha256']
    except Exception:
        print('C1_R42: SETUP contract_unreadable_at_freeze=%s' % freeze)
        return 2
    at_freeze = Repo(lane, freeze).read(SELF_REL)
    at_rev = repo.read(SELF_REL)
    with open(os.path.abspath(__file__), 'rb') as handle:
        running = handle.read()
    self_pin = int(at_freeze is not None
                   and hashlib.sha256(at_freeze).hexdigest() == pin
                   and hashlib.sha256(running).hexdigest() == pin
                   and (at_rev is None or hashlib.sha256(at_rev).hexdigest() == pin))
    if not self_pin:
        print('C1_R42: SETUP self_pin=0 pin=%s rev=%s freeze=%s' % (pin, rev, freeze))
        return 2
    fleet = args.fleet if args.fleet and os.path.isdir(args.fleet) else ''
    mismatches, n_records, n_rows = audit(repo, fleet)
    if n_records != EXPECTED_RECORDS:
        mismatches.append('records %d of %d round-41/42 records present' % (n_records, EXPECTED_RECORDS))
    for item in mismatches:
        print('MISMATCH %s' % item)
    total = sum(count(mismatches, c) for c in ('m6', 'm7', 'm8', 'm10', 'm11'))
    passed = total == 0 and n_records == EXPECTED_RECORDS
    print('C1_R42: self_pin=1 m6=%d m7=%d m8=%d m10=%d m11=%d total=%d records=%d sources_rows=%d '
          'rev=%s freeze=%s C1_R42_PASS=%s'
          % (count(mismatches, 'm6'), count(mismatches, 'm7'), count(mismatches, 'm8'),
             count(mismatches, 'm10'), count(mismatches, 'm11'), total, n_records, n_rows,
             rev, freeze, 'true' if passed else 'false'))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
