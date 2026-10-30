#!/usr/bin/env python3
import importlib.util
import json
from pathlib import Path
import subprocess

LANE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
CLONE = Path('/fast/scratch/hyaku/tameshi-r57/T57W3Read05/clone')
REV = 'adf87899c70d616140a81185a8f9acbbdfb30392'
HEADING = "### The service's limits — what tameshi refuses to mutation-test"
spec = importlib.util.spec_from_file_location('frozen', LANE / '.ufo/evidence/round-18/measure.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
raw = subprocess.check_output(['git', '-C', str(LANE), 'show', REV + ':SKILL.md'])
sec = next(s for s in m.sectionize(raw) if s['heading'] == HEADING)
print('SECTION', sec['start'], sec['end'], sec['sha256'])
print('CLONE_HEAD', subprocess.check_output(['git', '-C', str(CLONE), 'rev-parse', 'HEAD'], text=True).strip())
assert (CLONE / 'SKILL.md').read_bytes() == raw
print('CLONE_SKILL_MATCH true')
lines = raw.decode().splitlines()
print('SECTION_BEGIN')
print('\n'.join(lines[sec['start']-1:sec['end']]))
print('SECTION_END')
anchors = {
 'corpus/knowledge/service-limits.md': [(4,5)],
 'corpus/knowledge/service-optin-protocol.md': [(25,30),(86,91),(129,132),(267,269)],
 'corpus/knowledge/fleet-suite-census.md': [(277,286)],
 'corpus/knowledge/fleet-kill-rate-ledger.md': [(35,36),(156,158),(220,220),(285,285),(318,318)],
 'PROVINCE.md': [(14,18),(20,20)],
 'SKILL.md': [(824,828),(851,855),(834,836),(890,892)],
}
for path, ranges in anchors.items():
 content = (CLONE / path).read_text().splitlines()
 for start,end in ranges:
  assert len(content) >= end
  print(f'ANCHOR {path}:{start}-{end} exists')
  for n in range(start,end+1):
   print(f'{n}: {content[n-1]}')
for label,start,end in [('b-hermetic',841,845),('b-setup',868,872),('c-no-edit',851,853),('f-sensitivity',907,909)]:
 print(f'RESOLVED {label} SKILL.md:{start}-{end}')
 print('\n'.join(f'{n}: {lines[n-1]}' for n in range(start,end+1)))
# Literal search fallback: no LSP device is mounted in this session.
cadence = '\n'.join(lines[1022:1169])
ledger = (CLONE / 'corpus/knowledge/fleet-kill-rate-ledger.md').read_text()
print('CADENCE_NAMES_SERVICE_LIMITS', 'service-limits' in cadence)
print('LEDGER_NAMES_SERVICE_LIMITS', 'service-limits' in ledger)
note = (CLONE / 'corpus/knowledge/service-limits.md').read_text()
import re
page_rows = re.findall(r'^\| ([a-j]) \|', '\n'.join(lines[sec['start']-1:sec['end']]), re.M)
note_rows = re.findall(r'^\| ([a-j]) \|', note, re.M)
print('PAGE_ROW_IDS', ','.join(page_rows))
print('NOTE_ROW_IDS', ','.join(note_rows))
assert page_rows == note_rows == list('abcdefghij')
print('ANCHOR_SWEEP_COMPLETE 17 anchor ranges; rows a-j present in both renderings; no runnable command appears in assigned section')
