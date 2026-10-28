#!/usr/bin/env python3
"""Writes to T55W1Er10.{json,md} recorded as tool calls in the wave-1 session logs.
UTC timestamps; local = UTC-3 (C0 was committed 2026-10-28T17:16:25Z)."""
import glob,json,os
D='/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-28T14-01-34-216Z_01a182d0-f308-7371-97bc-ca8b0ed0633f'
hits=[]
for p in glob.glob(os.path.join(D,'*.jsonl')):
    for line in open(p,encoding='utf-8',errors='replace'):
        if 'T55W1Er10.md' not in line and 'T55W1Er10.json' not in line: continue
        try: d=json.loads(line)
        except Exception: continue
        if d.get('customType')!='tool_execution_start': continue
        a=d.get('data',{}); path=str((a.get('args') or {}).get('path') or '')
        if 'T55W1Er10.' in path:
            hits.append((d.get('timestamp'), os.path.basename(p)[:-6], a.get('toolName'), path.split('/')[-1]))
for t,seat,tool,f in sorted(hits):
    print(f'{t}  {seat:26} {tool:6} {f}')
print(f'\n{len(hits)} modifying/reading tool calls on the two paths; '
      f'{sum(1 for _,_,tool,_ in hits if tool in ("write","edit"))} are writes/edits')
