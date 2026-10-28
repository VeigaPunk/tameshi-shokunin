#!/usr/bin/env python3
"""T55W3R04 findings: the two residual issues this read reports, each with the
command output that establishes it, plus the round-27 corrections this read
confirms present at C0.

Reads blobs at C0 only (git -C LANE show REV:path); writes nothing.
"""
import importlib.util
import subprocess

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
HEADING = '## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence'
KM = 'corpus/knowledge/mutation-case-kimi-census.md'
KG = 'corpus/knowledge/mutation-case-kagi-census.md'


def lines(path):
    raw = subprocess.run(['git', '-C', LANE, 'show', '%s:%s' % (REV, path)],
                         capture_output=True, check=True).stdout
    return raw.decode('utf-8', 'surrogateescape').split('\n')


def section_text():
    spec = importlib.util.spec_from_file_location(
        'r18', LANE + '/.ufo/evidence/round-18/measure.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    raw = subprocess.run(['git', '-C', LANE, 'show', REV + ':SKILL.md'],
                         capture_output=True, check=True).stdout
    sec = [s for s in mod.sectionize(raw) if s['heading'] == HEADING][0]
    ls = raw.decode('utf-8', 'surrogateescape').split('\n')
    body = list(ls[sec['start'] - 1:sec['end']])
    while body and body[-1].strip() == '':
        body.pop()
    return '\n'.join(body), sec, ls


def grep(lines_, pred):
    return [(i + 1, l) for i, l in enumerate(lines_) if pred(l)]


def main():
    text, sec, skill = section_text()
    print('section sha256 (frozen round-18 sectionizer): %s' % sec['sha256'])
    print()

    print('=' * 72)
    print('FINDING 1 - step 10 model pointer omits the kimi section that holds')
    print('            the survivor probes it asks the record to carry')
    print('=' * 72)
    print('section quote:')
    for i, l in enumerate(skill):
        if 'the two mutation-case notes are the model' in l:
            print('  SKILL.md:%d: %s' % (i + 1, l))
            print('  SKILL.md:%d: %s' % (i + 2, skill[i + 1]))
    print()
    print('kimi headings (kimi note at C0):')
    for n, l in grep(lines(KM), lambda l: l.startswith('#')):
        print('  %4d: %s' % (n, l))
    print()
    print('non-equivalence PROBES live in kimi section 2:')
    for n, l in grep(lines(KM), lambda l: 'non-equivalence' in l or '+22 more' in l
                     or 'frozen=24' in l):
        print('  %4d: %s' % (n, l.strip()))
    print()
    print('kimi section 3 carries only the inventory (no probe command/output):')
    k3 = lines(KM)
    for n in range(135, 143):
        print('  %4d: %s' % (n, k3[n - 1]))
    print()
    print('kagi pointer includes its section 2 (which does hold the probes):')
    for n, l in grep(lines(KG), lambda l: 'non-equivalence' in l):
        print('  %4d: %s' % (n, l.strip()))
    print('mitigation: step 8 of the same section cites kimi :82-99, inside section 2')
    for i, l in enumerate(skill):
        if 'JS D2 on an empty root' in l:
            print('  SKILL.md:%d: %s' % (i + 1, l.strip()))
    print()

    print('=' * 72)
    print('FINDING 2 - the reproduce step does not carry the recorded caveat that')
    print('            the model notes\' reproduce specs cannot rebuild the driver')
    print('=' * 72)
    hits = [l for l in text.split('\n')
            if 'regression' in l or 'unversioned' in l or 'scratch loss' in l]
    print('section lines mentioning regression/unversioned/scratch loss: %d' % len(hits))
    for l in hits:
        print('  ' + l.strip())
    print()
    print('kagi Erratum R21 (mutation-case-kagi-census.md:271-275):')
    k = lines(KG)
    for n in range(271, 276):
        print('  %4d: %s' % (n, k[n - 1]))
    print()
    print('SKILL.md Restore discipline item 6 (411-415):')
    for n in range(411, 416):
        print('  %4d: %s' % (n, skill[n - 1]))
    print()
    print('the maintained replay route exists in the tree at C0:')
    drv = subprocess.run(['git', '-C', LANE, 'show', REV + ':tools/mutate-and-run.sh'],
                         capture_output=True, check=True).stdout.decode(
                             'utf-8', 'surrogateescape').split('\n')
    for n, l in grep(drv, lambda l: '--regression' in l)[:6]:
        print('  tools/mutate-and-run.sh:%d: %s' % (n, l.strip()))
    print('section mentions of tools/mutate-and-run.sh (implementation details only):')
    for i, l in enumerate(text.split('\n')):
        if 'mutate-and-run.sh' in l:
            print('  SKILL.md:%d: %s' % (sec['start'] + i, l.strip()))
    print()

    print('=' * 72)
    print('CONFIRMED PRESENT: the round-27 Read03 corrections (calibration)')
    print('=' * 72)
    checks = [
        ('step 9 endpoint-identity wording',
         'endpoint identity, not the absence of a transient write'),
        ('step 9 repo-revision parenthetical',
         'repo revision included; neither model note records an after-revision'),
        ('step 7 names the maintained driver', 'tools/mutate-and-run.sh:579-583'),
        ('step 5 names the maintained driver', 'tools/mutate-and-run.sh:434'),
        ('step 1 kumitate wording corrected',
         'cite-check and surface-probe print `n/m cases passed`'),
        ('step 4 pair acknowledgment', 'the :47-48 pair'),
        ('step 4 bash pair acknowledgment', "the bash exemplar's :70-71 pair"),
        ('step 5 no-op guard disclaimed',
         'The cited historical notes do\n   not establish that the round-2 driver carried the `new != old` no-op guard.'),
    ]
    for name, needle in checks:
        print('  %-42s %s' % (name, 'PRESENT' if needle in text else 'ABSENT'))
    r27 = subprocess.run(
        ['git', '-C', LANE, 'cat-file', '-e', REV + ':.ufo/waves/round-27/w1/Read03.md'])
    print('  %-42s %s' % ('.ufo/waves/round-27/w1/Read03.md',
                          'present at C0' if r27.returncode == 0 else 'MISSING'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
