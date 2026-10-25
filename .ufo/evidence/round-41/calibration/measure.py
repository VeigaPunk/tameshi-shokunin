#!/usr/bin/env python3
"""Round-41 C1 counter — self-assessment records vs observed repo state.

Frozen before any seat scored and before the deciding run. Four mismatch
classes, each counted over the committed bytes at REV (or the working tree
under `--mode work`, which exists only for pre-run checks):

  m6  the SCORECARD standing `sources-registry` capability row's stated row
      count differs from the `SOURCES.md` S-row count (carried from the frozen
      round-35 counter, unchanged rule)
  m7  a round-41 record cites an S-id the registry does not hold as `mined`
  m8  a round-41 record cites a repo-relative path that does not resolve at
      REV
  m9  the round-40 lesson's quarantine summary contradicts its own verdict
      table and no appended round-41 correction states the table's counts
      (the round-40 closure's routed defect 1, mechanically re-checked)

"Round-41 record" means `corpus/lessons/round-41.md`, the SCORECARD section
that starts at `## Round 41`, and the LOG.md section that starts at
`## 2026-10-25 — round 41`. A class whose audit surface does not exist yet
counts 0: it has nothing to disagree with.

Predicate: `C1_R41_PASS` true iff every class counts 0. Counting command:

  python3 .ufo/evidence/round-41/calibration/measure.py --lane LANE --rev REV

Exit 0 iff the predicate is true.
"""
import argparse
import os
import re
import subprocess
import sys

LESSON = 'corpus/lessons/round-41.md'
LESSON_40 = 'corpus/lessons/round-40.md'
SCORECARD = 'SCORECARD.md'
LOG = 'LOG.md'
SOURCES = 'corpus/SOURCES.md'
SCORECARD_HEAD = '## Round 41'
LOG_HEAD = '## 2026-10-25 — round 41'

S_ROW_RE = re.compile(r'^ {0,3}\|[ \t]*S(\d{3,})')
S_CITE_RE = re.compile(r'\bS(\d{3,})\b')
BACKTICK_RE = re.compile(r'`([^`]+)`')
PATH_PREFIXES = (
    'corpus/',
    'tools/',
    '.ufo/evidence/round-41/',
    '.ufo/waves/round-41/',
)
PATH_EXACT = {
    'SCORECARD.md',
    'LOG.md',
    'SHONEN.md',
    'PROVINCE.md',
    'SKILL.md',
    'README.md',
    'MINT.md',
}
WORDS = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
}


def number(token):
    token = token.strip().lower()
    if token in WORDS:
        return WORDS[token]
    if token.isdigit():
        return int(token)
    return None


def read(lane, rev, path):
    """Read a repo path at REV, or from the working tree when rev is 'work'."""
    if rev == 'work':
        full = os.path.join(lane, path)
        if not os.path.isfile(full):
            return None
        with open(full, encoding='utf-8', errors='replace') as handle:
            return handle.read()
    proc = subprocess.run(
        ['git', '-C', lane, 'show', '%s:%s' % (rev, path)], capture_output=True
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.decode('utf-8', 'replace')


def resolves(lane, rev, path):
    if rev == 'work':
        return os.path.isfile(os.path.join(lane, path))
    proc = subprocess.run(
        ['git', '-C', lane, 'cat-file', '-e', '%s:%s' % (rev, path)], capture_output=True
    )
    return proc.returncode == 0


def section(text, head):
    if text is None:
        return None
    idx = text.find(head)
    if idx < 0:
        return None
    return text[idx:]


def registry(text):
    """Return {id: status} for the 11-column registry rows."""
    rows = {}
    for line in (text or '').splitlines():
        match = S_ROW_RE.match(line)
        if not match:
            continue
        cells = line.split('|')
        status = cells[9].strip() if len(cells) > 9 else ''
        rows['S%s' % match.group(1).zfill(3)] = status
    return rows


def round41_records(lane, rev):
    parts = [read(lane, rev, LESSON)]
    parts.append(section(read(lane, rev, SCORECARD), SCORECARD_HEAD))
    parts.append(section(read(lane, rev, LOG), LOG_HEAD))
    return [part for part in parts if part]


def quarantine_counts(lesson):
    """(adopted, refused, present) counted from the round-40 verdict table."""
    body = section(lesson, '### Quarantine')
    if body is None:
        return None
    body = body.split('\n### ', 1)[0]
    adopted = refused = present = 0
    for line in body.splitlines():
        if not re.match(r'^\| S\d{3} \|', line):
            continue
        if '**Adopted**' in line:
            adopted += 1
        elif re.search(r'refus', line, re.I):
            refused += 1
        elif 'present' in line or 'misbound' in line:
            present += 1
    return adopted, refused, present


def quarantine_summary(lesson):
    words = '|'.join(sorted(WORDS, key=len, reverse=True)) + r'|\d+'
    flat = re.sub(r'\s+', ' ', lesson or '')
    match = re.search(
        r'(%s) row adopted,?\s*(?:and\s+)?(%s) refused.*?(%s) present' % (words, words, words),
        flat,
        re.I,
    )
    if not match:
        return None
    return (number(match.group(1)), number(match.group(2)), number(match.group(3)))


def path_tokens(text):
    out = []
    for token in BACKTICK_RE.findall(text or ''):
        raw = token.strip()
        raw = re.sub(r':\d+(?:-\d+)?$', '', raw)
        if any(ch in raw for ch in '<>*{}|()…, '):
            continue
        if raw.startswith(PATH_PREFIXES) or raw in PATH_EXACT:
            out.append(raw)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lane', required=True)
    parser.add_argument('--rev', required=True)
    parser.add_argument('--fleet', default='')
    args = parser.parse_args()

    lane = os.path.abspath(args.lane)
    rev = args.rev
    if rev != 'work':
        proc = subprocess.run(['git', '-C', lane, 'rev-parse', rev], capture_output=True)
        rev = proc.stdout.decode().strip()
        if not rev:
            print('C1_R41: SETUP rev_unresolved=%s' % args.rev)
            return 2

    sources_text = read(lane, rev, SOURCES) or ''
    rows = registry(sources_text)
    observed_rows = len(rows)
    mismatches = []

    # m6 -- standing sources-registry row count vs the registry
    score_text = read(lane, rev, SCORECARD) or ''
    standing = [ln for ln in score_text.splitlines() if ln.startswith('| sources-registry |')]
    if standing:
        match = re.search(r'(\d+) rows', standing[-1])
        if match and int(match.group(1)) != observed_rows:
            mismatches.append(
                'm6 SCORECARD standing row says %s rows, SOURCES.md has %d'
                % (match.group(1), observed_rows)
            )

    records = round41_records(lane, rev)

    # m7 -- cited S-ids that are not mined
    for text in records:
        for raw in sorted(set(S_CITE_RE.findall(text))):
            sid = 'S%s' % raw.zfill(3)
            status = rows.get(sid)
            if status is None:
                mismatches.append('m7 %s cited but absent from the registry' % sid)
            elif status != 'mined':
                mismatches.append('m7 %s cited but status=%s' % (sid, status))

    # m8 -- cited repo paths that do not resolve
    for text in records:
        for path in sorted(set(path_tokens(text))):
            if not resolves(lane, rev, path):
                mismatches.append('m8 %s cited but does not resolve at %s' % (path, rev))

    # m9 -- round-40 quarantine summary vs its own table, unless corrected here
    lesson40 = read(lane, rev, LESSON_40)
    if lesson40 is not None:
        table = quarantine_counts(lesson40)
        summary = quarantine_summary(lesson40)
        if table is not None and summary is not None and table != summary:
            correction = read(lane, rev, LESSON) or ''
            fixed = (
                'round-40' in correction
                and 'six refused' in correction
                and 'ten present' in correction
            )
            if not fixed:
                mismatches.append(
                    'm9 round-40 quarantine summary says %s, its table counts %s '
                    '(no round-41 correction)' % (summary, table)
                )

    for item in mismatches:
        print('MISMATCH %s' % item)
    print(
        'C1_R41: m6=%d m7=%d m8=%d m9=%d total=%d records=%d sources_rows=%d rev=%s C1_R41_PASS=%s'
        % (
            sum(1 for x in mismatches if x.startswith('m6')),
            sum(1 for x in mismatches if x.startswith('m7')),
            sum(1 for x in mismatches if x.startswith('m8')),
            sum(1 for x in mismatches if x.startswith('m9')),
            len(mismatches),
            len(records),
            observed_rows,
            rev,
            'true' if not mismatches else 'false',
        )
    )
    return 0 if not mismatches else 1


if __name__ == '__main__':
    sys.exit(main())
