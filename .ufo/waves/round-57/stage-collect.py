#!/usr/bin/env python3
"""List every staged file under <wave>/<seat>/stage/ with size and sha256; flag duplicate target paths.
Usage: stage-collect.py WAVE_DIR [--install]   (--install copies non-conflicting files into the lane, never overwriting)"""
import hashlib, os, shutil, sys
wave = sys.argv[1]; install = '--install' in sys.argv
lane = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
seen = {}
for seat in sorted(os.listdir(wave)):
    st = os.path.join(wave, seat, 'stage')
    if not os.path.isdir(st): continue
    for dp, dn, fn in os.walk(st):
        for f in fn:
            p = os.path.join(dp, f); rel = os.path.relpath(p, st)
            h = hashlib.sha256(open(p, 'rb').read()).hexdigest()[:12]
            seen.setdefault(rel, []).append((seat, h, os.path.getsize(p)))
for rel, v in sorted(seen.items()):
    flag = 'DUP' if len(v) > 1 else ''
    print(flag, rel, v)
    if install and len(v) == 1:
        dst = os.path.join(lane, rel)
        if os.path.exists(dst):
            print('  EXISTS-skip', dst); continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(wave, v[0][0], 'stage', rel), dst); print('  installed')
