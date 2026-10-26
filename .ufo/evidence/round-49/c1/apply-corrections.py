#!/usr/bin/env python3
"""Apply .ufo/evidence/round-49/c1/corrections.json to SKILL.md in the lane working tree.

Each correction must (a) target one of the seven C1 sections, (b) have its `old` text occur exactly once inside that
section's current text, and (c) keep the newline count (a correction never moves a line, so every SKILL.md line
pointer outside the edited line keeps its target). Anything else aborts before a byte is written.
Usage: apply-corrections.py LANE
"""
import importlib.util
import json
import os
import sys

LANE = os.path.realpath(sys.argv[1])
E = os.path.join(LANE, '.ufo/evidence/round-49')
spec = importlib.util.spec_from_file_location('c1m', os.path.join(E, 'c1/measure.py'))
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)
mod = c1.load_monitor_module(LANE)
path = os.path.join(LANE, 'SKILL.md')
raw = open(path, 'rb').read()
text = raw.decode('utf-8')
nlines = text.count('\n')
for i, c in enumerate(json.load(open(os.path.join(E, 'c1/corrections.json'), encoding='utf-8'))['corrections']):
    if c['section'] not in c1.TARGETS:
        sys.exit('correction %d: not a target section' % i)
    if c['old'].count('\n') != c['new'].count('\n'):
        sys.exit('correction %d: changes the line count' % i)
    secs = [s for s in mod.sectionize(text.encode('utf-8')) if s['heading'] == c['section']]
    if len(secs) != 1:
        sys.exit('correction %d: heading not unique' % i)
    lines = text.split('\n')
    s, e = secs[0]['start'], secs[0]['end']
    body = '\n'.join(lines[s - 1:e])
    if body.count(c['old']) != 1:
        sys.exit('correction %d (%s): old text occurs %d times in the section' % (i, c['source_seat'], body.count(c['old'])))
    body = body.replace(c['old'], c['new'], 1)
    text = '\n'.join(lines[:s - 1] + body.split('\n') + lines[e:])
    print('APPLIED %2d %-24s %s' % (i, c['source_seat'], c['why'][:70]))
if text.count('\n') != nlines:
    sys.exit('line count changed')
with open(path, 'w', encoding='utf-8') as fh:
    fh.write(text)
print('SKILL.md lines unchanged: %d' % nlines)
