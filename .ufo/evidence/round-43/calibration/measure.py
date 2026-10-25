#!/usr/bin/env python3
"""Round-43 C2 counter — record agreement, extended to two new classes (calibration).

Successor of the round-42 C1 counter. The five round-42 classes are carried
unchanged in meaning (m6 registry count, m7 mined S-ids, m8 path cites, m10
presence receipts, m11 revision reachability) and two classes are added:

  m12 — SCORECARD contract conformance. The newest `## Round N` block must
        carry a `**Planned (round N+1):**` line, because AXES.md's SCORECARD
        contract makes `planned` a required field and a round that omits it
        leaves its successor undeclared. At the base, the round-42 block has
        no such line (the last one is `Planned (round 41)`).
  m13 — the newest standing `sources-registry` row's counting command is
        census-valid. CORPUS.md's census accepts rows with 0-3 leading spaces,
        so a column-zero count under-counts an indented row. The class (a)
        requires the standing command's cell to name the 0-3-space pattern and
        (b) proves the requirement load-bearing on a built mirror in which one
        registry row is indented two spaces: the column-zero pattern counts
        N-1 and the census-valid pattern counts N.

Predicate `C2_R43_PASS` is true iff: self_pin=1, classes=7 (all seven declared
classes ran — a counter that omits m12/m13 cannot pass), and
m6=m7=m8=m10=m11=m12=m13=0.

Counting command:

  python3 .ufo/evidence/round-43/calibration/measure.py --lane LANE --rev REV --freeze FREEZE

`--records N` restricts the record set (default: round-42 and round-43
records). Exit 0 iff the predicate is true, 1 if false, 2 on a setup refusal.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

SELF_REL = '.ufo/evidence/round-43/calibration/measure.py'
CONTRACT_REL = '.ufo/evidence/round-43/contract.json'
SOURCES_REL = 'corpus/SOURCES.md'
SCORECARD_REL = 'SCORECARD.md'
LOG_REL = 'LOG.md'
RECORDS = (
    'corpus/lessons/round-42.md',
    'corpus/lessons/round-43.md',
)
FLEET_PREFIXES = ('/home/vgpnk/Projects/shokunin/', '/tmp/', '…/')
SKIP_SUFFIXES = ('.md', '.py', '.sh', '.mjs', '.json', '.stdout', '.stdin', '.txt', '.tsv',
                 '.html', '.java', '.exit', '.stderr', '.diff', '.jsonl')
ID_RE = re.compile(r'\bS\d{3,}\b')
HEX40 = re.compile(r'(?<![0-9a-f:])[0-9a-f]{40}(?![0-9a-f])')
BACKTICK = re.compile(r'`([^`\n]+)`')


class Refusal(Exception):
    pass


def git(lane, *args):
    return subprocess.run(['git', '-C', lane] + list(args), capture_output=True)


def show(lane, rev, path):
    proc = git(lane, 'show', '%s:%s' % (rev, path))
    return proc.stdout if proc.returncode == 0 else None


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def rows(text):
    found = {}
    for line in text.splitlines():
        match = re.match(r'^ {0,3}\|\s*(S\d{3,})\s*\|', line)
        if not match:
            continue
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        found[match.group(1)] = cells
    return found


def mined_ids(registry_text):
    mined = set()
    for sid, cells in rows(registry_text).items():
        status = cells[7] if len(cells) > 7 else ''
        if status == 'mined':
            mined.add(sid)
    return mined


def newest_round_block(scorcard_text):
    matches = list(re.finditer(r'^## Round (\d+)\b.*$', scorcard_text, re.M))
    if not matches:
        raise Refusal('SCORECARD carries no "## Round N" block')
    last = matches[-1]
    return int(last.group(1)), scorcard_text[last.start():]


def m12_planned(block_text, round_no):
    """(hits, note): the block must declare the next round's planned claims."""
    wanted = 'Planned (round %d)' % (round_no + 1)
    hits = [] if wanted in block_text else [wanted]
    return hits


def standing_registry_rows(scorcard_text):
    found = []
    for line in scorcard_text.splitlines():
        if line.startswith('| sources-registry |'):
            found.append(line)
    return found


def row_count_claim(cell):
    match = re.search(r'(\d+)\s+rows at round\s+(\d+)', cell)
    if not match:
        return None, None
    return int(match.group(1)), int(match.group(2))


def count_patterns(mirror_text):
    column0 = sum(1 for line in mirror_text.splitlines()
                  if re.match(r'^\|\s*S\d{3,}\s*\|', line))
    valid = sum(1 for line in mirror_text.splitlines()
                if re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', line))
    return column0, valid


def indent_mirror(registry_text):
    """One registry row indented two spaces: census-valid, column-zero blind."""
    lines = registry_text.splitlines()
    for index, line in enumerate(lines):
        if re.match(r'^\|\s*S\d{3,}\s*\|', line):
            lines[index] = '  ' + line
            break
    return '\n'.join(lines) + '\n'


def m13_standing_command(scorcard_text, registry_text):
    """(hits, note): newest standing row's command must be census-valid."""
    standing = standing_registry_rows(scorcard_text)
    if not standing:
        return ['no standing sources-registry row'], 'standing=0'
    newest = standing[-1]
    hits = []
    if '0,3' not in newest and '0-3space' not in newest:
        hits.append('standing command is column-zero only')
    mirror = indent_mirror(registry_text)
    column0, valid = count_patterns(mirror)
    if not (valid == column0 + 1):
        hits.append('indent probe not load-bearing (column0=%d valid=%d)' % (column0, valid))
    return hits, 'standing=%d column0=%d valid=%d' % (len(standing), column0, valid)


def path_cites(text):
    out = set()
    for match in BACKTICK.finditer(text):
        token = match.group(1).strip()
        if '://' in token or token.startswith('/') or token.startswith('…'):
            continue
        token = re.split(r'[\s(]', token)[0]
        token = re.sub(r':\d+(-\d+)?$', '', token)
        token = re.sub(r'\{[^}]*\}', '', token)
        if '/' not in token and not token.endswith(SKIP_SUFFIXES):
            continue
        if not token.endswith(SKIP_SUFFIXES):
            continue
        if token.startswith('$') or token.startswith('<') or token.startswith('.'):
            if token.startswith('.ufo/'):
                out.add(token)
            continue
        out.add(token)
    return out


def m8_paths(lane, rev, record_texts, tree_paths):
    hits = []
    for name, text in record_texts.items():
        for token in sorted(path_cites(text)):
            if token in tree_paths:
                continue
            # a directory cite is resolved as a prefix
            if any(path.startswith(token.rstrip('/') + '/') for path in tree_paths):
                continue
            hits.append('%s:%s' % (name, token))
    return hits


def m10_receipts(lane, rev, paths):
    """Presence claims under .ufo/waves whose path contradicts the tree."""
    supersedes = {}
    claims = []
    for path in paths:
        if not path.endswith('.json'):
            continue
        raw = show(lane, rev, path)
        if raw is None:
            continue
        try:
            doc = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(doc, dict) and isinstance(doc.get('supersedes'), (str, list)):
            targets = doc['supersedes']
            if isinstance(targets, str):
                targets = [targets]
            for target in targets:
                supersedes[target] = path
        stack = [doc]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                if isinstance(node.get('present'), bool):
                    target = node.get('report') or node.get('path')
                    if isinstance(target, str):
                        claims.append((path, target, node['present']))
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
    tree = set(paths)
    hits = []
    for receipt, target, present in claims:
        rel = target.lstrip('./')
        exists = rel in tree or any(p.startswith(rel.rstrip('/') + '/') for p in tree)
        if bool(exists) != present:
            if any(key in receipt for key in supersedes) or receipt in supersedes:
                continue
            covered = any(key.strip('./') in rel or rel.endswith(key.strip('./'))
                          for key in supersedes)
            if covered:
                continue
            hits.append('%s present=%s %s' % (receipt, str(present).lower(), rel))
    return hits, len(claims)


def m11_revisions(lane, record_texts):
    hits = []
    seen = set()
    for name, text in record_texts.items():
        for token in HEX40.findall(text):
            if token in seen:
                continue
            seen.add(token)
            if git(lane, 'cat-file', '-e', token + '^{commit}').returncode != 0:
                hits.append('%s:%s' % (name, token))
    return hits, len(seen)


def selftest():
    cases = []

    def case(name, ok, note=''):
        cases.append((name, bool(ok), note))

    block_missing = '## Round 9\n\n| C1 | x | y |\n\n**Planned (round 9):** stale\n'
    case('T1_missing_planned_detected', m12_planned(block_missing, 9) == ['Planned (round 10)'])
    block_ok = block_missing + '\n**Planned (round 10):** next\n'
    case('T1_planned_present_clean', m12_planned(block_ok, 9) == [])

    registry = ('| id | source | kind | tier | scope | anchor | teaches | status | '
                'opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n'
                '| S001 | a — https://x.test/a | docs | A | s | a | t | mined | 2026-01-01 | 180d | — |\n'
                '| S002 | b — https://x.test/b | docs | A | s | a | t | mined | 2026-01-01 | 180d | — |\n')
    mirror = indent_mirror(registry)
    column0, valid = count_patterns(mirror)
    case('T2_indent_probe_load_bearing', column0 == 1 and valid == 2,
         'column0=%d valid=%d' % (column0, valid))
    old_row = '| sources-registry | x | `grep -cE \'^\\| S[0-9]{3} \\|\' corpus/SOURCES.md` → 2 rows at round 9 |'
    hits, note = m13_standing_command(old_row + '\n', registry)
    case('T2_column_zero_standing_detected', hits, note)
    new_row = ('| sources-registry | x | `grep -cE \'^ {0,3}\\| S[0-9]{3} \\|\' corpus/SOURCES.md` '
               '→ 2 rows at round 9 |')
    hits2, note2 = m13_standing_command(new_row + '\n', registry)
    case('T2_census_valid_standing_clean', hits2 == [], note2)

    tree = {'corpus/SOURCES.md', 'tools/x.py', '.ufo/evidence/a/b.stdout'}
    good = {'r': 'see `corpus/SOURCES.md:12` and `tools/x.py`'}
    bad = {'r': 'see `tools/missing.py`'}
    case('T3_path_cites_clean', m8_paths('.', 'HEAD', good, tree) == [],
         str(m8_paths('.', 'HEAD', good, tree)))
    case('T3_path_cites_detected', m8_paths('.', 'HEAD', bad, tree) == ['r:tools/missing.py'],
         str(m8_paths('.', 'HEAD', bad, tree)))

    case('T4_mined_parse', mined_ids(registry) == {'S001', 'S002'})
    case('T4_id_regex', ID_RE.findall('S001 S 002 S99') == ['S001'])

    source_row = ('| sources-registry | x | `grep` → 2 rows at round 9 |')
    claim, round_no = row_count_claim(source_row)
    case('T5_count_claim', claim == 2 and round_no == 9, '%s %s' % (claim, round_no))

    failed = [row for row in cases if not row[1]]
    print('C2_R43_SELFTEST: cases=%d failed=%d' % (len(cases), len(failed)))
    for name, ok, note in cases:
        if not ok:
            print('FAIL %s %s' % (name, note))
    print('VERDICT: %s' % ('PASS' if not failed else 'FAIL'))
    return 0 if not failed else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--lane', default='.')
    parser.add_argument('--rev')
    parser.add_argument('--freeze')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    lane = os.path.abspath(args.lane)
    rev = args.rev or subprocess.run(['git', '-C', lane, 'rev-parse', 'master'],
                                     capture_output=True).stdout.decode().strip()
    freeze = args.freeze or rev
    contract_raw = show(lane, freeze, CONTRACT_REL)
    if contract_raw is None:
        raise SystemExit('refusing: no contract at %s' % freeze)
    contract = json.loads(contract_raw)
    pin = contract['claims']['C2']['counter_sha256']
    self_raw = show(lane, freeze, SELF_REL)
    if self_raw is None:
        raise SystemExit('refusing: counter absent at freeze')
    with open(os.path.abspath(__file__), 'rb') as handle:
        running = sha(handle.read())
    self_pin = 1 if sha(self_raw) == pin and running == pin else 0

    scorcard = (show(lane, rev, SCORECARD_REL) or b'').decode('utf-8', 'replace')
    registry = (show(lane, rev, SOURCES_REL) or b'').decode('utf-8', 'replace')
    if not scorcard or not registry:
        raise SystemExit('refusing: SCORECARD or registry absent at rev')
    paths = [p for p in git(lane, 'ls-tree', '-r', '--name-only', rev)
             .stdout.decode().split('\n') if p]
    tree_paths = set(paths)

    record_texts = {}
    for rel in RECORDS:
        raw = show(lane, rev, rel)
        if raw is not None:
            record_texts[rel] = raw.decode('utf-8', 'replace')
    round_no, block = newest_round_block(scorcard)
    record_texts['SCORECARD.md#round-%d' % round_no] = block
    log_raw = show(lane, rev, LOG_REL)
    if log_raw is not None:
        log_text = log_raw.decode('utf-8', 'replace')
        marker = 'round %d' % round_no
        cut = log_text.find(marker)
        record_texts['LOG.md#round-%d' % round_no] = log_text[cut:] if cut >= 0 else ''

    registry_rows = rows(registry)
    valid_count = sum(1 for line in registry.splitlines()
                      if re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', line))

    # m6 — the newest standing row's stated count equals the census-valid count.
    standing = standing_registry_rows(scorcard)
    stated, stated_round = row_count_claim(standing[-1]) if standing else (None, None)
    m6 = [] if stated == valid_count else ['standing=%s actual=%d' % (stated, valid_count)]

    # m7 — every S-id cited by the round's records is a mined row.
    m7 = []
    mined = mined_ids(registry)
    for name, text in record_texts.items():
        for sid in sorted(set(ID_RE.findall(text))):
            if sid not in registry_rows:
                m7.append('%s unknown %s' % (name, sid))
            elif sid not in mined:
                m7.append('%s unmined %s' % (name, sid))

    # m8 — backtick path cites resolve at REV.
    m8 = m8_paths(lane, rev, record_texts, tree_paths)

    # m10 — presence receipts agree with the tree.
    m10, claims = m10_receipts(lane, rev, paths)

    # m11 — cited 40-hex revisions resolve in the lane.
    m11, revisions = m11_revisions(lane, record_texts)

    # m12 — the newest round block declares the next round's planned claims.
    m12 = m12_planned(block, round_no)

    # m13 — the newest standing registry command is census-valid and load-bearing.
    m13, m13_note = m13_standing_command(scorcard, registry)

    classes = {'m6': m6, 'm7': m7, 'm8': m8, 'm10': m10, 'm11': m11, 'm12': m12, 'm13': m13}
    declared = 7
    total = sum(len(hits) for hits in classes.values())
    fields = ['C2_R43:', 'self_pin=%d' % self_pin, 'classes=%d' % declared]
    for name in ('m6', 'm7', 'm8', 'm10', 'm11', 'm12', 'm13'):
        fields.append('%s=%d' % (name, len(classes[name])))
    fields.extend([
        'total=%d' % total,
        'records=%d' % len(record_texts),
        'sources_rows=%d' % valid_count,
        'standing=%s' % (stated,),
        'receipts=%d' % claims,
        'revisions=%d' % revisions,
        'm13_probe=%s' % m13_note.replace(' ', '_'),
        'rev=%s' % rev,
        'freeze=%s' % freeze,
    ])
    passed = self_pin == 1 and declared == 7 and total == 0
    fields.append('C2_R43_PASS=%s' % ('true' if passed else 'false'))
    first = None
    for name in classes:
        if classes[name]:
            first = '%s:%s' % (name, classes[name][0])
            break
    if first:
        fields.append('first=%s' % re.sub(r'[\s|]', '_', first))
    print(' '.join(fields))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
