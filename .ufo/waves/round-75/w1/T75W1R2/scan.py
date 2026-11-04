#!/usr/bin/env python3
"""T75W1R2 independent C2 scanner (seat-owned; NOT the lane candidate).

Re-derives the 16 declared SCORECARD `## Capabilities` figures at a pinned
doc rev using the pinned instruments. Doc and instruments come from git
objects (a verified detached clone at the pinned rev); measured tokens come
ONLY from child-process stdout. Prints per-figure old-vs-measured pairs.
"""
import re, subprocess, sys

CLONE = sys.argv[1]
REV = sys.argv[2]
DOC_OVERRIDE = sys.argv[3] if len(sys.argv) > 3 else None
DOC = 'SCORECARD.md'

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

def git(*args):
    p = subprocess.run(['git', '-C', CLONE] + list(args),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if p.returncode != 0:
        sys.exit('git failed: %s' % p.stdout.decode())
    return p.stdout.decode('utf-8', 'replace')

def main():
    head = git('rev-parse', 'HEAD').strip()
    assert head == REV, 'clone HEAD %s != pinned %s' % (head, REV)
    dirty = git('status', '--porcelain').strip()
    assert not dirty, 'clone dirty: %r' % dirty
    doc = open(DOC_OVERRIDE).read() if DOC_OVERRIDE else git('show', REV + ':' + DOC)

    # capability rows inside ## Capabilities
    rows, inside = {}, False
    for line in doc.splitlines():
        if line.startswith('## Capabilities'):
            inside = True; continue
        if inside and line.startswith('## '): break
        if inside and line.startswith('|') and not line.startswith('|---'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if len(cells) >= 3 and cells[0] != 'Capability':
                rows.setdefault(cells[0], []).append(line)

    uniq_cmds = sorted({tuple(s[2]) for s in SPECS})
    uniq_paths = sorted({s[2][0] for s in SPECS})
    print('# unique instrument commands: %d ; unique tool paths: %d'
          % (len(uniq_cmds), len(uniq_paths)))

    cache, match, stale, refused = {}, 0, 0, 0
    for name, pat, tool in SPECS:
        key = tuple(tool)
        if key not in cache:
            p = subprocess.run([sys.executable, '-I', '-X', 'utf8'] + tool,
                               cwd=CLONE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
            cache[key] = (p.stdout.decode('utf-8', 'replace'), p.returncode)
        out, rc = cache[key]
        candidates = rows.get(name, [])
        if len(candidates) != 1:
            print('SELFSTATE_ROW %-38s NAME-LOOKUP-REFUSED rows_with_name=%d'
                  % (name[:38], len(candidates)))
            refused += 1; continue
        m1 = re.search(pat, candidates[0])
        m2 = re.search(pat, out)
        q = m1.group(0) if m1 else None
        g = m2.group(0) if m2 else None
        if q is None or g is None:
            print('SELFSTATE_ROW %-38s FIGURE-REFUSED doc=%s stdout=%s rc=%d'
                  % (name[:38], q, g, rc))
            refused += 1; continue
        state = 'match' if q == g else 'stale'
        if state == 'match': match += 1
        else: stale += 1
        print('SELFSTATE_ROW %-38s quoted=%-46s measured=%-46s %s'
              % (name[:38], q, g, state))
    print('SELFSTATE_MINE: rows=%d match=%d stale=%d refused=%d'
          % (len(SPECS), match, stale, refused))
    return 0

if __name__ == '__main__':
    sys.exit(main())
