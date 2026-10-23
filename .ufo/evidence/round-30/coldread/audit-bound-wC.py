#!/usr/bin/env python3
"""Round 30 attempt 3: post-data AUDIT of the wave-C bound entries (supporting evidence only; it is not the
binding and changes no credit). Written after seat CtlBindV3 showed five hand-forged transcript shapes that
binding v3 keeps (.ufo/waves/round-30/wC/CtlBindV3.md). For every binding in bind-receipt-wC.json and every
trace it matched, it checks in the seat's real host transcript the stricter conditions v3 lacks:
  - the matching tool call is a `bash` call whose `command` names trace-inputs.py and `--out` followed by a
    path ending in the trace basename;
  - its tool result comes AFTER the call, has the same id, and is not marked isError;
  - the trace file exists in the lane and its `rev` equals the entry's read_rev.
Usage: audit-bound-wC.py BIND_RECEIPT ASSEMBLED_BOUND  -> prints one line per seat trace and a summary.
"""
import json
import os
import re
import sys

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'


def calls_and_results(path):
    order, calls, results = 0, {}, {}
    for line in open(path, encoding='utf-8'):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        m = d.get('message') if d.get('type') == 'message' else None
        if not m:
            continue
        order += 1
        if m.get('role') == 'toolResult' and m.get('toolCallId'):
            results.setdefault(m['toolCallId'], (order, bool(m.get('isError'))))
        elif m.get('role') == 'assistant':
            for c in m.get('content') or []:
                if c.get('type') == 'toolCall' and c.get('id'):
                    calls.setdefault(c['id'], (order, c.get('name'), (c.get('arguments') or {}).get('command', '')))
    return calls, results


def main():
    receipt = json.load(open(sys.argv[1]))
    bound = json.load(open(sys.argv[2]))['entries']
    ok = bad = 0
    for e, k in zip(bound, receipt['kept_entries']):
        assert (e['start'], e['heading']) == (k['start'], k['heading'])
        for b in k['bindings']:
            calls, results = calls_and_results(b['transcript'])
            for tb in b['traces_matched_to_tool_calls']:
                good = False
                for cid, (o, name, cmd) in calls.items():
                    if name != 'bash' or 'trace-inputs.py' not in str(cmd):
                        continue
                    if not re.search(r'--out[ =]\S*' + re.escape(tb) + r'(\s|$)', str(cmd)):
                        continue
                    r = results.get(cid)
                    if r and r[0] > o and not r[1]:
                        good = True
                        break
                tpath = [t for t in e['traces'] if os.path.basename(t) == tb]
                full = tpath[0] if tpath and os.path.isabs(tpath[0]) else os.path.join(LANE, tpath[0]) if tpath else ''
                rev_ok = False
                if full and os.path.exists(full):
                    try:
                        rev_ok = json.load(open(full)).get('rev') == e['read_rev']
                    except ValueError:
                        rev_ok = False
                verdict = 'ok' if good and rev_ok else 'FAIL'
                ok += verdict == 'ok'
                bad += verdict != 'ok'
                print(f"{verdict}\t{b['seat']}\t{e['start']}\t{tb}\tbash_call_ok_result={good}\ttrace_rev_ok={rev_ok}")
    print(f'AUDIT: traces_ok={ok} traces_fail={bad}')
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
