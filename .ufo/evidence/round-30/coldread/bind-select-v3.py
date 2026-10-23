#!/usr/bin/env python3
"""Round 30 attempt 3 (v3, frozen before any wave-C data): bind-select.py of attempt 2 plus one
condition. The L1 of attempt 3 scored a do-nothing control against v2 before data: transcripts that
hold only the prompt and ONE assistant text line `COLDREAD <seat>: executed-ok` (no tool call) kept
32/32 round-29 entries, so v2 proves a seat existed and said the line, never that it read.
v3 adds: for EVERY seat, the entry lists at least one trace whose basename (without `.json`, part
after the last '.') starts with `<seat>-` (the round-29 pilot showed seats that prefix the label),
and each such trace basename appears in an assistant-authored tool call whose arguments also name
`trace-inputs.py`, and that tool call has a tool result in the same transcript (matching
toolCallId). Receipts: .ufo/evidence/round-30/attempt3/bind-controls.txt.
Earlier history: attempt-1 draft rewritten by the L1 of attempt 2 after the wave-A pilot
(.ufo/waves/round-30/wA/PilotBind.md, defects D1-D7).

Usage: bind-select.py --repo LANE --assembled IN.json --registry REG.json --sessions DIR
                      --prefix PREFIX --out OUT.json --receipt RECEIPT.json

An entry is bound when it names at least one report and one seat and, for EVERY seat it names
(label normalised: the part after the last '.', without a trailing '-<digits>' retry suffix, D3):
  - the normalised seat is a member of the wave registry;
  - one of the entry's own `reports` (D4) is `<...>/<seat>.md`, readable under --repo (D1), and holds
    a json block whose `seat` normalises to the same name, whose `read_rev` equals the entry's, and
    which has a section with the entry's `start` and `heading` (verdicts are not compared: the
    assembler normalises them, round-29 Mistake 5);
  - the host session store holds a transcript `<DIR>/<PREFIX><seat>.jsonl` or
    `<DIR>/<PREFIX><seat>-<N>.jsonl` (D7) in which an ASSISTANT-authored message (text or tool-call
    arguments) contains `COLDREAD <seat>:` (D2: the prompt also contains that string, so a
    whole-file substring test proves nothing).
The receipt records per kept entry and seat: raw label, registry key, transcript path, byte size,
sha256 and session id (D5: the registry carries no agent id). Exit 1 when nothing is kept or the
sessions directory is missing (D6).
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys


def norm(label):
    return re.sub(r'-\d+$', '', str(label).split('.')[-1])


def assistant_has(path, needle):
    """Return (hit, session_id, traced): hit when an assistant message holds `needle`; traced is the
    list of tool-call argument strings that name trace-inputs.py and have a tool result."""
    sid = None
    hit = False
    calls = {}
    results = set()
    with open(path, encoding='utf-8') as f:
        for line in f:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get('type') == 'session' and sid is None:
                sid = d.get('id')
            m = d.get('message') if d.get('type') == 'message' else None
            if not m:
                continue
            if m.get('role') == 'toolResult' and m.get('toolCallId'):
                results.add(m.get('toolCallId'))
                continue
            if m.get('role') != 'assistant':
                continue
            for c in m.get('content') or []:
                if c.get('type') == 'text' and needle in (c.get('text') or ''):
                    hit = True
                elif c.get('type') == 'toolCall':
                    args = json.dumps(c.get('arguments'), ensure_ascii=False)
                    if needle in args:
                        hit = True
                    if 'trace-inputs.py' in args and c.get('id'):
                        calls[c.get('id')] = args
    traced = [args for cid, args in calls.items() if cid in results]
    return hit, sid, traced


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--assembled', required=True)
    ap.add_argument('--registry', required=True)
    ap.add_argument('--sessions', required=True)
    ap.add_argument('--prefix', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--receipt', required=True)
    a = ap.parse_args()
    if not os.path.isdir(a.sessions):
        print('bind-select: --sessions is not a directory', file=sys.stderr)
        return 1
    reg = json.load(open(a.registry))
    members = reg.get('members', {})
    doc = json.load(open(a.assembled))
    keep, drop = [], []
    for e in doc['entries']:
        seats = list(e.get('seats') or [])
        reports = list(e.get('reports') or [])
        reasons, bindings = [], []
        if not reports:
            reasons.append('no-reports')
        if not seats:
            reasons.append('no-seats')
        for raw in seats:
            seat = norm(raw)
            if seat not in members:
                reasons.append('seat-not-registry-member:%s' % raw)
                continue
            named = [r for r in reports if os.path.basename(r) == seat + '.md']
            if not named:
                reasons.append('report-not-named-by-entry:%s' % seat)
                continue
            rp = named[0]
            full = rp if os.path.isabs(rp) else os.path.join(a.repo, rp)
            try:
                text = open(full, encoding='utf-8').read()
            except OSError:
                reasons.append('report-unreadable:%s' % rp)
                continue
            ok = False
            for blk in re.findall(r'```json\s*\n(.*?)\n```', text, re.S):
                try:
                    d = json.loads(blk)
                except ValueError:
                    continue
                if norm(d.get('seat')) == seat and d.get('read_rev') == e.get('read_rev') and any(
                        s.get('start') == e.get('start') and s.get('heading') == e.get('heading')
                        for s in d.get('sections', [])):
                    ok = True
            if not ok:
                reasons.append('report-block-unbound:%s' % seat)
                continue
            cands = sorted(glob.glob(os.path.join(a.sessions, '%s%s.jsonl' % (a.prefix, seat))) +
                           glob.glob(os.path.join(a.sessions, '%s%s-[0-9]*.jsonl' % (a.prefix, seat))))
            found = None
            for tp in cands:
                hit, sid, traced = assistant_has(tp, 'COLDREAD %s:' % seat)
                if hit:
                    found = (tp, sid, traced)
                    break
            if found is None:
                reasons.append('transcript-without-assistant-coldread:%s (%d candidates)' % (seat, len(cands)))
                continue
            tp, sid, traced = found
            own = [os.path.basename(t) for t in (e.get('traces') or [])
                   if os.path.splitext(os.path.basename(t))[0].split('.')[-1].startswith(seat + '-')]
            if not own:
                reasons.append('no-trace-of-seat:%s' % seat)
                continue
            untraced = [b for b in own if not any(b in args for args in traced)]
            if untraced:
                reasons.append('trace-without-traced-tool-call:%s:%s' % (seat, ','.join(untraced)))
                continue
            rawb = open(tp, 'rb').read()
            bindings.append({'seat_label': raw, 'seat': seat, 'session_id': sid, 'report': rp,
                             'transcript': tp, 'transcript_bytes': len(rawb),
                             'transcript_sha256': hashlib.sha256(rawb).hexdigest(),
                             'traces_matched_to_tool_calls': own})
        (drop if reasons else keep).append((e, reasons, bindings))
    out = dict(doc)
    out['entries'] = [e for e, _, _ in keep]
    json.dump(out, open(a.out, 'w'), indent=2)
    receipt = {
        'repo': os.path.abspath(a.repo), 'sessions': os.path.abspath(a.sessions), 'prefix': a.prefix,
        'assembled': len(doc['entries']), 'kept': len(keep), 'excluded': len(drop),
        'registry_members': len(members),
        'kept_entries': [{'start': e['start'], 'heading': e['heading'], 'verdict': e['verdict'],
                          'bindings': b} for e, _, b in keep],
        'excluded_entries': [{'start': e['start'], 'heading': e['heading'], 'verdict': e['verdict'],
                              'seats': e.get('seats'), 'reports': e.get('reports'), 'reasons': r}
                             for e, r, _ in drop],
    }
    json.dump(receipt, open(a.receipt, 'w'), indent=2)
    print(json.dumps({k: receipt[k] for k in ('assembled', 'kept', 'excluded')}))
    return 0 if keep else 1


if __name__ == '__main__':
    sys.exit(main())
