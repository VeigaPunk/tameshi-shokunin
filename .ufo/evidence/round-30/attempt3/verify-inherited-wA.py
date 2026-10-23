#!/usr/bin/env python3
"""Round 30 attempt 3: re-derive authorship of the uncommitted wave-A seat reports left by attempt 2.
For each .ufo/waves/round-30/wA/<Seat>.md, open the seat's host transcript
TameshiR30A2.<Seat>-<N>.jsonl and report: assistant tool calls that name the report path (write,
edit, eval, bash), and whether the last `write` content equals the file bytes now in the lane."""
import glob, json, os, sys
L = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
SS = '/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-23T00-54-50-959Z_01a16640-e34f-76e4-8a3b-4d245a8bb241/TameshiR30A2'
for f in sorted(glob.glob(L + '/.ufo/waves/round-30/wA/*.md')):
    n = os.path.basename(f)[:-3]
    cur = open(f).read()
    ts = sorted(glob.glob(f'{SS}/TameshiR30A2.{n}-*.jsonl'))
    if not ts:
        print(f'{n}\ttranscript=none'); continue
    kinds, last = [], None
    for line in open(ts[0]):
        try: o = json.loads(line)
        except ValueError: continue
        m = o.get('message') or {}
        if m.get('role') != 'assistant': continue
        for c in m.get('content') or []:
            if c.get('type') != 'toolCall': continue
            a = c.get('arguments') or {}
            if f'wA/{n}.md' in json.dumps(a):
                kinds.append(c.get('name'))
                if c.get('name') == 'write' and str(a.get('path', '')).endswith(f'wA/{n}.md'):
                    last = a.get('content')
    print(f'{n}\ttranscript={os.path.basename(ts[0])}\tcalls={",".join(kinds)}\tlast_write_equals_file={None if last is None else last == cur}')
