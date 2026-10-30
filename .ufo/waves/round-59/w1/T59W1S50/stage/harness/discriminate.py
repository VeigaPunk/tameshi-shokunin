#!/usr/bin/env python3
"""Build 24-case discriminator tables from frozen-counter receipts."""
import json
import re
from pathlib import Path

ROOT = Path('/fast/scratch/hyaku/tameshi-r59/T59W1S50')
TOKENS = ('EXECUTOR_SOURCE_BOUND', 'EXECUTOR_SOURCE_DRIFT', 'EXECUTOR_SOURCE_UNAVAILABLE')

def load(name):
    text = (ROOT / name).read_text()
    m = re.search(r'^\[.*\]$', text, re.M | re.S)
    cases = json.loads(m.group(0))
    summary = [l for l in text.splitlines() if l.startswith('C1_R59')][-1]
    return cases, summary

def rows(cases):
    out = []
    for c in cases:
        blob = c['stdout'] + c['stderr']
        tok = next((t for t in TOKENS if t in blob), None)
        out.append({
            'path': c['path'], 'class': c['class'], 'expected': c['expected'],
            'exit': c['exit'], 'token': tok, 'ok': c['ok'],
            'stdout': c['stdout'].strip(), 'stderr': c['stderr'].strip(),
        })
    return out

def main():
    rep = {}
    for key, fname in (('always_accept', 'measure-accept.out'),
                       ('always_unavailable', 'measure-unavailable.out')):
        cases, summary = load(fname)
        r = rows(cases)
        rep[key] = {
            'summary': summary,
            'passed': sum(x['ok'] for x in r),
            'failed': sum(not x['ok'] for x in r),
            'cases': r,
        }
    (ROOT / 'discriminator.json').write_text(json.dumps(rep, ensure_ascii=False, indent=1))
    for key in rep:
        print(f"== {key}: {rep[key]['summary']}")
        print(f"{'path':<20} {'class':<12} {'exp':>3} {'got':>3} {'token':<28} ok")
        for c in rep[key]['cases']:
            print(f"{c['path']:<20} {c['class']:<12} {c['expected']:>3} {c['exit']:>3} {str(c['token']):<28} {c['ok']}")

main()
