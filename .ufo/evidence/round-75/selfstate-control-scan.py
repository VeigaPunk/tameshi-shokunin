#!/usr/bin/env python3
"""Pre-freeze control for R75-C2 (L1 prototype, NOT the instrument).

Scans the SCORECARD `## Capabilities` rows at one revision and compares every
declared figure regex against the lane instrument that prints it. Exit 1 with
`stale>0`; this is the cheap control that a do-nothing round cannot move to 0.
"""
import os, re, subprocess, sys
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
SPECS = [
 ('receipt-existence sweep', r'RECEIPT_EXISTS_SELFTEST: \d+/\d+ pass', ['tools/receipt-exists.py','--selftest']),
 ('commit-message receipt binding sweep', r'RECEIPT_COMMIT_BIND_SELFTEST: \d+/\d+ pass', ['tools/receipt-commit-bind.py','--selftest']),
 ('quoted-line receipt backability', r'QUOTED_LINE_EXISTS_SELFTEST: \d+/\d+ pass', ['tools/quoted-line-exists.py','--selftest']),
 ('counter-arm liveness check', r'ARM_LIVENESS_SELFTEST: \d+/\d+ pass', ['tools/arm-liveness.py','--selftest']),
 ('counter-arm liveness check', r'rows=\d+ live=\d+ dead=\d+', ['tools/arm-liveness.py','--repo','.','--manifest','tools/arm-liveness.json']),
 ('figure-attribution check', r'FIGURE_ATTRIBUTION_SELFTEST: \d+/\d+ pass', ['tools/figure-attribution.py','--selftest']),
 ('figure-attribution check', r'FIGURE_ATTRIBUTION: rows=\d+ met=\d+ unexpected=\d+', ['tools/figure-attribution.py','--repo','.','--manifest','tools/figure-attribution.json']),
 ('anchor-drift sweep', r'ANCHOR_DRIFT_SELFTEST: \d+/\d+ pass', ['tools/anchor-drift-sweep.py','--selftest']),
 ('anchor-drift sweep', r'ANCHOR_DRIFT: rows=\d+ met=\d+ unexpected=\d+', ['tools/anchor-drift-sweep.py','--repo','.','--manifest','tools/anchor-drift-sweep.json']),
 ('printed-count recheck', r'COUNT_RECHECK_SELFTEST: \d+/\d+ pass', ['tools/count-recheck.py','--selftest']),
 ('printed-count recheck', r'COUNT_RECHECK: rows=\d+ met=\d+ unexpected=\d+', ['tools/count-recheck.py','--repo','.','--manifest','tools/count-recheck.json']),
 ('line-pointer recheck', r'POINTER_RECHECK_SELFTEST: \d+/\d+ pass', ['tools/pointer-recheck.py','--selftest']),
 ('line-pointer recheck', r'POINTER_RECHECK: rows=\d+ met=\d+ unexpected=\d+', ['tools/pointer-recheck.py','--repo','.','--manifest','tools/pointer-recheck.json']),
 ('rekey-cost forecast', r'REKEY_COST_SELFTEST: \d+/\d+ pass', ['tools/rekey-cost.py','--selftest']),
 ('round-range additivity sweep', r'ADDRANGE: rows=\d+ met=\d+ unexpected=\d+', ['tools/additivity-range.py','--repo','.','--manifest','tools/additivity-range.json']),
 ('round-range additivity sweep', r'ADDITIVITY_RANGE_SELFTEST: \d+/\d+ pass', ['tools/additivity-range.py','--selftest']),
]
def main():
    argv = sys.argv[1:]
    doc = sys.stdin.read()
    rows = {}
    inside = False
    for line in doc.splitlines():
        if line.startswith('## Capabilities'):
            inside = True; continue
        if inside and line.startswith('## '): break
        if inside and line.startswith('|') and not line.startswith('|---'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if len(cells) >= 3 and cells[0] != 'Capability':
                rows[cells[0]] = line
    cache, match, stale = {}, 0, 0
    for cap, pat, tool in SPECS:
        key = tuple(tool)
        if key not in cache:
            p = subprocess.run([sys.executable, '-I', '-X', 'utf8'] + tool,
                               cwd=LANE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
            cache[key] = p.stdout.decode('utf-8', 'replace')
        line = rows.get(cap, '')
        m1 = re.search(pat, line)
        m2 = re.search(pat, cache[key])
        q = m1.group(0) if m1 else None
        g = m2.group(0) if m2 else None
        state = 'match' if q is not None and q == g else 'stale'
        if state == 'match': match += 1
        else: stale += 1
        print('SELFSTATE_ROW %-34s quoted=%-48s measured=%-48s %s'
              % (cap[:34], q, g, state))
    print('SELFSTATE_CONTROL: rows=%d match=%d stale=%d' % (len(SPECS), match, stale))
    return 0 if stale == 0 else 1
if __name__ == '__main__':
    sys.exit(main())
