#!/usr/bin/env python3
"""T55W3R04 sweep: resolve every citation in SKILL.md '## Mutation-sweep recipe'
at C0 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb against the tree at the same rev.

Usage: python3 sweep.py
Prints: (1) the section as cut by the frozen round-18 sectionizer, with sha256;
(2) every path:line / bare :line citation token found by regex;
(3) a claim table: each claim -> cited range -> the cited lines, verbatim;
(4) token checks: literal strings asserted by the section, searched inside the
    cited range only (so a token that lives elsewhere in the file does not pass).
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
HEADING = '## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence'
KM = 'corpus/knowledge/mutation-case-kimi-census.md'
KG = 'corpus/knowledge/mutation-case-kagi-census.md'
SK = 'corpus/knowledge/gates-survey-kumitate.md'
SG = 'corpus/knowledge/gates-survey-kagi.md'
DRV = 'tools/mutate-and-run.sh'


def blob(path):
    return subprocess.run(['git', '-C', LANE, 'show', '%s:%s' % (REV, path)],
                          capture_output=True, check=True).stdout


def lines_of(path):
    raw = blob(path).decode('utf-8', 'surrogateescape')
    return raw.split('\n')


def show(path, rng):
    ls = lines_of(path)
    a, b = rng
    out = []
    for n in range(a, b + 1):
        if n <= len(ls):
            out.append('%4d: %s' % (n, ls[n - 1]))
        else:
            out.append('%4d: <OUT OF RANGE: file has %d lines>' % (n, len(ls)))
    return out


def section():
    spec = importlib.util.spec_from_file_location(
        'r18', LANE + '/.ufo/evidence/round-18/measure.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    raw = blob('SKILL.md')
    secs = mod.sectionize(raw)
    hit = [s for s in secs if s['heading'] == HEADING]
    assert len(hit) == 1, hit
    return hit[0], secs


# (claim, path, range, needles that must occur inside the range)
CLAIMS = [
    ('step1 hermetic control: no live-path/host effects', KM, (4, 7),
     ['--selftest', 'mkdtemp', '--root']),
    ('step1 host-gated branches excluded/controlled', KG, (24, 38),
     ['mktemp -d', 'substrate-gated', 'skip-case']),
    ('step1 kumitate count+verdict shape', SK, (19, 31),
     ['cases passed', 'VERDICT: PASS']),
    ('step1 kimi control green 43/43 exit 0', KM, (20, 21),
     ['KIMI_CENSUS_SELFTEST: 43/43 pass', 'VERDICT: PASS', 'exit 0']),
    ('step1 bash 16 cases, 14 executed +2 skipped', KG, (27, 35),
     ['16 cases', 'skip-case 15', '14']),
    ('step1 bash control exit 0', KG, (42, 43), ['SELFTEST: PASS (16 cases)', 'exit 0']),
    ('step2 pin: path/sha/size/mtime/rev/clean', KM, (13, 16),
     ['sha256', '43273 B', 'mtime', 'repo', 'git status --porcelain']),
    ('step2 kagi pin + 887th line no newline', KG, (13, 17),
     ['44212 B', '887th line carries no trailing newline', 'git status --porcelain']),
    ('step2 G-R2-1 dirty-pin lesson row', 'corpus/README.md', (11, 11),
     ['G-R2-1', 'intermediate dirty-tree state']),
    ('step2 gates-survey-kagi errata block', SG, (545, 558),
     ['### Errata (round 2)', 'G-R2-1', 'intermediate dirty-tree state']),
    ('step3 scratch copy + cmp', KG, (44, 45), ['cp -p', 'cmp`-verified']),
    ('step4 manifest shape (JS ten)', KM, (41, 53),
     ['D1', 'D10']),
    ('step4 driver spec (JS ten)', KM, (155, 166),
     ['D1  kimi-census.mjs:105', 'D10 kimi-census.mjs:145']),
    ('step4 JS pair sharing a class at :47-48', KM, (47, 48),
     ['dropped arm', 'dropped arm (presence gate)']),
    ('step4 bash pair sharing a class at :70-71', KG, (70, 71),
     ['dropped branch', 'dropped branch']),
    ('step4 E1 pre-registration kept (JS)', KM, (183, 191),
     ['E1', 'wrong on D7', 'calibration miss']),
    ('step4 E1 miscalled counts kept (bash)', KG, (184, 191),
     ['E1', 'failing-case *counts* on only 6/10']),
    ('step5 uniqueness gate: count==1 + all unique', KM, (22, 25),
     ['asserts the old string occurs exactly once', 'all unique', 'first-line match']),
    ('step5 bash records assert + all unique', KG, (44, 47),
     ['asserts the old string occurs exactly once', 'all unique']),
    ('step5 maintained driver prints failing count', DRV, (434, 434),
     ['old-string-count=%d expected=1']),
    ('step6 kimi per-defect evidence', KM, (26, 28),
     ['selftest.txt', 'meta.json', 'results.json']),
    ('step6 kagi records duration/summary', KG, (48, 49),
     ['wall time', 'case summary']),
    ('step6 timeouts 300 s / 280 s', KM, (29, 31), ['300 s timeout']),
    ('step6 timeouts 300 s / 280 s (bash)', KG, (50, 53), ['280 s per-run bound']),
    ('step7 denominators held 43', KM, (30, 33), ['43']),
    ('step7 denominators held 16', KG, (27, 35), ['16']),
    ('step7 denominators held 16 (kill-rate row)', KG, (50, 53), ['16 cases']),
    ('step7 failing labels required', KM, (59, 76), ['Failing-case labels', 'D4 (3)']),
    ('step7 bash grammar line 1/16 FAIL', KG, (67, 67), ['1/16', 'FAIL']),
    ('step7 bash failing labels', KG, (82, 103),
     ['bad-case 05 undeclared-file want exit=1 token=SURFACE UNLISTED got exit=0']),
    ('step7 token-only kill B4', KG, (88, 91),
     ['bad-case 07 symlink-swap', 'exit code']),
    ('step7 round-2 numbers 8/10 11 runs 7.0 s', KM, (29, 31),
     ['8/10 (80 %)', '11 runs', '7.0 s']),
    ('step7 round-3 numbers', KG, (50, 53), ['8/10 (80 %)', '11.0 s']),
    ('step8 D2 probe +22/+23', KM, (82, 99), ['+22 more', '+23 more']),
    ('step8 D10 probe frozen=24/25', KM, (82, 99), ['frozen=25', 'frozen=24']),
    ('step8 B5 probe exec 644 vs no execute bit', KG, (111, 114),
     ['SURFACE DIVERGED', 'no execute bit', 'SURFACE OK', 'exec 644']),
    ('step8 B10 probe ok=0/ok=1', KG, (118, 122), ['ok=1', 'ok=0']),
    ('step8 B5/B10 sensitivity expectations', KG, (252, 254),
     ['SURFACE OK \u2026 (exec 644)', 'ok=0']),
    ('step9 endpoint identity (no after-revision)', KM, (34, 35),
     ['sha256 before', 'mtime unchanged', 'working tree clean']),
    ('step9 endpoint identity (bash)', KG, (54, 56),
     ['sha256 before', 'mtime', 'git status --porcelain']),
    ('step10 model note JS sections', KM, (80, 107),
     ['## 2. Surviving-defect class analysis']),
    ('cost profile node version', KM, (20, 21), ['node v24.21.0']),
    ('cross-host unknown Kimi U5', KM, (204, 205), ['U5', 'kill-rate stability']),
    ('cross-host unknown Kagi U5', KG, (203, 204), ['U5', 'kill-rate stability']),
]


def main():
    sec, secs = section()
    print('SECTION CUT BY FROZEN .ufo/evidence/round-18/measure.py sectionize()')
    print('  rev      %s' % REV)
    print('  heading  %s' % sec['heading'])
    print('  lines    %d-%d (1-based, trailing blank lines stripped)' % (sec['start'], sec['end']))
    print('  sha256   %s' % sec['sha256'])
    print('  sections in file: %d' % len(secs))
    print()

    # Rebuild the section body with the sectionizer's own rule so the digest can
    # be re-derived independently of the dict, then compare.
    ls = lines_of('SKILL.md')
    body_lines = list(ls[sec['start'] - 1:sec['end']])
    while body_lines and body_lines[-1].strip() == '':
        body_lines.pop()
    text = '\n'.join(body_lines)
    mine = hashlib.sha256(text.encode('utf-8', 'surrogateescape')).hexdigest()
    print('  sha256 re-derived from lines %d-%d: %s (%s)'
          % (sec['start'], sec['end'], mine, 'MATCH' if mine == sec['sha256'] else 'MISMATCH'))
    print()
    print('--- citation tokens found by regex in the section ---')
    toks = re.findall(r'(?:[A-Za-z0-9_./-]+\.(?:md|sh|py|json|mjs))?:\d+(?:-\d+)?', text)
    print('  %d tokens:' % len(toks))
    for t in toks:
        print('    %s' % t)
    print()

    print('--- heading/path anchors, resolved at %s ---' % REV[:7])
    anchors = ['corpus/knowledge/mutation-case-kimi-census.md',
               'corpus/knowledge/mutation-case-kagi-census.md',
               'corpus/knowledge/gates-survey-kumitate.md',
               'corpus/knowledge/gates-survey-kagi.md',
               'corpus/README.md', 'corpus/QUALITY.md', DRV, 'corpus/SOURCES.md']
    for p in anchors:
        r = subprocess.run(['git', '-C', LANE, 'cat-file', '-e', '%s:%s' % (REV, p)])
        print('  %-52s %s' % (p, 'blob OK' if r.returncode == 0 else 'MISSING'))
    ls = lines_of('SKILL.md')
    print('  %-52s %s' % ('SKILL.md headings referenced by name', ''))
    for want in ['## The mutation bar', '## Restore discipline', '## Errata \u2014 round 16',
                 '## Defect-taxonomy templates', '## Standing rules']:
        hits = [i + 1 for i, l in enumerate(ls) if l.startswith(want)]
        print('    %-40s -> line %s' % (want, hits))
    print()

    print('--- claim table (each claim -> cited range -> verbatim lines, needle check) ---')
    bad = 0
    for claim, path, rng, needles in CLAIMS:
        print('CLAIM: %s' % claim)
        print('  cite %s:%d-%d' % (path, rng[0], rng[1]))
        body = show(path, rng)
        for l in body:
            print('   ', l)
        joined = '\n'.join(body)
        for n in needles:
            ok = n in joined
            if not ok:
                bad += 1
                print('    NEEDLE %r -> MISSING' % n)
            else:
                print('    needle %r -> present' % n)
        print()
    print('--- summary ---')
    print('  claims checked: %d' % len(CLAIMS))
    print('  missing needles: %d' % bad)
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
