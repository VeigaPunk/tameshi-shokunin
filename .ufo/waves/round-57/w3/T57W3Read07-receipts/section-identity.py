#!/usr/bin/env python3
import importlib.util
import subprocess
p = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
spec = importlib.util.spec_from_file_location('frozen_round18', p + '/.ufo/evidence/round-18/measure.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
raw = subprocess.check_output(['git', '-C', p, 'show', 'adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md'])
for sec in m.sectionize(raw):
    if sec['heading'] == '### The map — where a reader enters, artifact by artifact':
        print(sec['start'], sec['end'], sec['sha256'])
        print('\n'.join(raw.decode().splitlines()[sec['start']-1:sec['end']]))
