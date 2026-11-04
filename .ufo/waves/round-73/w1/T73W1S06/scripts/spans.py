#!/usr/bin/env python3
"""Byte-slice verification of every claim span quoted in the recon table (read-only)."""
import subprocess

FLEET = '/home/vgpnk/Projects/shokunin'
SPANS = {
    60: ('9f39c5fcb9400667ffb2846dd2183ef9cd5dfe82', [
        (6919, 6927, '32 seats'), (6929, 6941, 'settled 2/32'),
        (16803, 16811, '32 seats'), (16813, 16822, '2 settled'),
        (16824, 16840, '30 cap-cancelled')]),
    72: ('3664a6d30051410c3d2bb8c32926d13e284a5118', [
        (416, 424, '12 seats'), (3618, 3626, '12 seats'),
        (3628, 3638, '11 reports'), (5786, 5794, '12 seats'),
        (5874, 5889, '12 seat records'), (6029, 6037, '12 seats')]),
}


def blob(rev, path):
    p = subprocess.run(['git', '-C', FLEET, 'cat-file', 'blob', '%s:%s' % (rev, path)],
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return p.stdout if p.returncode == 0 else None


for r, (rev, spans) in SPANS.items():
    raw = blob(rev, '.ufo/reports/round-%d/tameshi.md' % r)
    print('round-%d rev=%s bytes=%d' % (r, rev, len(raw)))
    for a, b, want in spans:
        sl = raw[a:b].decode('utf-8')
        print('  bytes[%d:%d]=%r  expected=%r  %s'
              % (a, b, sl, want, 'MATCH' if sl == want else 'MISMATCH'))
    print()

raw = blob(SPANS[72][0], '.ufo/reports/round-72/tameshi.md')
needle = b'12 seats, 11 reports'
print('span-substring test "12 seats, 11 reports" in blob:', needle in raw)
print('span bytes for that string:', raw.index(needle), 'to',
      raw.index(needle) + len(needle))
raw60 = blob(SPANS[60][0], '.ufo/reports/round-60/tameshi.md')
print('r60 "(32 seats, settled 2/32" in blob:', b'(32 seats, settled 2/32' in raw60)
print('r60 second claim string "(32 seats, 2 settled, 30 cap-cancelled" in blob:',
      b'(32 seats, 2 settled, 30 cap-cancelled' in raw60)
