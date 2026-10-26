#!/usr/bin/env python3
"""Round-50 C1: enumerate the routed items of the ten closure spot-checks (rounds 40-49) at a revision.

Usage: extract-defects.py --lane LANE --rev REV [--manual MANUAL_JSON] > defects.json

An item is a list line (`N. ` or `- `) under the spot-check's routed heading (the first `## ` heading whose text
contains "Rout"), up to the next `## ` heading; continuation lines join the item. Keys are the item's backticked
spans, S-ids and path-like tokens, minus the generic record names in GENERIC; MANUAL_JSON adds keys by id.
"""
import argparse
import hashlib
import json
import re
import subprocess

ROUNDS = range(40, 50)
GENERIC = {'SKILL.md', 'SCORECARD.md', 'LOG.md', 'SHONEN.md', 'README.md', 'QUALITY.md', 'SOURCES.md',
           'corpus/SOURCES.md', 'corpus/QUALITY.md', 'corpus/README.md', '[~]', '--selftest', 'measure.py'}
ITEM_RE = re.compile(r'^(?:(\d+)\.|-)\s+(.*)$')
PATH_RE = re.compile(r'(?<![\w/.-])((?:[\w.-]+/)*[\w.-]+\.(?:md|py|sh|json|mjs|stdout|spec|jsonl))\b')
SID_RE = re.compile(r'\bS\d{3}\b')


def git(lane, *args):
    return subprocess.run(['git', '-C', lane] + list(args), check=True, capture_output=True).stdout


def items_of(text):
    lines = text.split('\n')
    out, inside, cur = [], False, None
    for no, line in enumerate(lines, 1):
        if line.startswith('## '):
            if inside:
                break
            inside = 'Rout' in line or 'rout' in line
            continue
        if not inside:
            continue
        m = ITEM_RE.match(line)
        if m:
            cur = {'line': no, 'text': m.group(2).strip()}
            out.append(cur)
        elif cur is not None and line.strip() and line.startswith((' ', '\t')):
            cur['text'] += ' ' + line.strip()
            cur['end'] = no
        elif not line.strip():
            cur = None
    return out


def keys_of(text):
    keys = []
    for span in re.findall(r'`([^`\n]+)`', text):
        span = span.strip()
        if span and span not in GENERIC and len(span) >= 4:
            keys.append(span)
    keys += [p for p in PATH_RE.findall(text) if p not in GENERIC]
    keys += SID_RE.findall(text)
    seen, uniq = set(), []
    for k in keys:
        if k not in seen:
            seen.add(k)
            uniq.append(k)
    return uniq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--manual')
    a = ap.parse_args()
    manual = json.load(open(a.manual)) if a.manual else {}
    defects = []
    for r in ROUNDS:
        path = 'corpus/lessons/round-%d-verifier-spotcheck.md' % r
        blob = git(a.lane, 'show', '%s:%s' % (a.rev, path))
        routed_at = git(a.lane, 'log', '--diff-filter=A', '--format=%H', a.rev, '--', path).decode().split()[-1]
        for i, it in enumerate(items_of(blob.decode('utf-8')), 1):
            did = 'R%d.%d' % (r, i)
            keys = manual[did] if did in manual else keys_of(it['text'])
            defects.append({'id': did, 'round': r, 'file': path, 'line': it['line'],
                            'end': it.get('end', it['line']), 'routed_at': routed_at,
                            'file_sha256': hashlib.sha256(blob).hexdigest(),
                            'text': it['text'][:600], 'keys': keys})
    print(json.dumps({'schema': 'tameshi-r50-defects-v1', 'rev': a.rev, 'count': len(defects),
                      'defects': defects}, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
