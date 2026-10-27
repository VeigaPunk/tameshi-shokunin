#!/usr/bin/env python3
"""Replicate the frozen C3 counter's row_reason() verdict for tools/mte-interop.py at REV,
without running the whole counter. Read-only on the lane."""
import importlib.util, json, sys

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = sys.argv[1] if len(sys.argv) > 1 else '6d8c11e378aa90b12650808e1b79270742935f15'
spec = importlib.util.spec_from_file_location('c3', LANE + '/.ufo/evidence/round-51/c3/measure.py')
c3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c3)

skill = c3.show(LANE, REV, 'SKILL.md').decode('utf-8', 'surrogateescape')
rows = c3.registry_rows(skill)
tool = 'tools/mte-interop.py'
print('registry rows total:', len(rows))
hits = [(n, c) for n, c in rows if tool in c[2]]
print('rows whose Entry cell names the tool:', [n for n, _ in hits])
for n, c in hits:
    why, argv = c3.row_reason(LANE, REV, tool, c)
    print('--- line %d  row_reason=%s' % (n, why))
    if argv:
        print('    selftest argv:', argv[0])
        print('    usage argv  :', argv[1])
        print('    selftest cell:', argv[2])
        print('    verdict map  :', argv[3])
    for i, cell in enumerate(c):
        print('    cell[%d]: %s' % (i, cell))
