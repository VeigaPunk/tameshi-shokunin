#!/usr/bin/env python3
"""R1: is 75+34+32 an overrun? Score each wave against ITS OWN dispatched band and the
round total against the per-L1 swarm budget. Read-only over the lane and the hub.

Usage: python3 r1_band_accounting.py LANE
"""
import json
import subprocess
import sys

LANE = sys.argv[1]
W = LANE + '/.ufo/waves/round-55'
HUB = '/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-mission-result.mjs'

total = 0
print('wave  spawn  band      verdict')
for w in ('w1', 'w2', 'w3'):
    d = json.load(open('%s/%s-dispatch.json' % (W, w)))
    p, n = d['policy'], int(d['counts']['total'])
    total += n
    lo, hi, cap = int(p['waveMinLanes']), int(p['waveMaxLanes']), int(p['maxLanes'])
    ok = lo <= n <= hi and n <= cap
    print('%s    %5d  %d..%-6d %s (per-swarm maxLanes=%d, hardCeiling=%d)'
          % (w, n, lo, hi, 'in band' if ok else 'OUT OF BAND', cap, int(p['hardCeiling'])))
print('round total %d seats; per-L1 round budget maxLanes=%d -> %s'
      % (total, int(p["maxLanes"]) if False else 256,
         'within' if total <= 256 else 'exceeds'))

print('\nprimary source for the two-band reading (line: text):')
out = subprocess.run(['grep', '-n', 'Two bands, two jobs', HUB], capture_output=True, text=True).stdout
print(out.strip())
out = subprocess.run(['sed', '-n', '2656,2658p', HUB], capture_output=True, text=True).stdout
print(out.rstrip())

print('\nprimary source for the per-wave obligation (ufo-swarm-wave.mjs:16-18):')
out = subprocess.run(['sed', '-n', '16,18p',
                      '/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs'],
                     capture_output=True, text=True).stdout
print(out.rstrip())

band_ok = all(
    int(json.load(open('%s/%s-dispatch.json' % (W, w)))['policy']['waveMinLanes'])
    <= int(json.load(open('%s/%s-dispatch.json' % (W, w)))['counts']['total'])
    <= int(json.load(open('%s/%s-dispatch.json' % (W, w)))['policy']['waveMaxLanes'])
    for w in ('w1', 'w2', 'w3'))
print('\nBAND_COMPLIANT=%s ROUND_TOTAL=%d ROUND_BUDGET=256' % ('true' if band_ok else 'false', total))
sys.exit(0 if band_ok and total <= 256 else 1)
