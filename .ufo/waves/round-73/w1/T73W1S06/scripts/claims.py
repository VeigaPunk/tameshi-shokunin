#!/usr/bin/env python3
"""Enumerate seat/report-count claim spans in the swept round reports (read-only)."""
import re
import subprocess

FLEET = '/home/vgpnk/Projects/shokunin'
REVS = {
    60: '9f39c5fcb9400667ffb2846dd2183ef9cd5dfe82',
    61: 'ab9521f69ccafd9ab54db53d897aaf1a919a9361',
    62: '224e67321220c8c0c6fcbffc986e4e7da2721a85',
    63: '674b6b7d1f4435148313548b30d03d652160776c',
    64: 'fded7c9b7d0ab4e513dfdfc05e3d92b535a78395',
    65: '8896e743f6bd5ea6b38486666e82c7056688d5a4',
    66: '88b1c187b5d600e2d7ed5f89524e4bd45fa5a45a',
    67: '2b04913e067e7bbd1edec187136ed759254d4c04',
    68: '635c407d9b840380df4166ee0eda79f209804bc5',
    69: '7d93c406be30a361d2cc531bc0f1ef35029bc93a',
    70: '17f2c24131e0e79930ce92f5a121ebeb32de6863',
    71: '449987085bdbb32027cf26812fe60183b8837274',
    72: '3664a6d30051410c3d2bb8c32926d13e284a5118',
}
PATS = [
    (r'(?<![0-9])\d+\s+seat reports?\b', 'N seat reports'),
    (r'(?<![0-9])\d+\s*/\s*\d+\s+seats?\b', 'N/M seats'),
    (r'(?<![0-9])\d+\s+seats?\b', 'N seats'),
    (r'(?<![0-9])\d+\s+reports?\b', 'N reports'),
    (r'settled\s+\d+\s*/\s*\d+', 'settled N/M'),
    (r'\b\d+\s+settled\b', 'N settled'),
    (r'\b\d+\s+cap-cancelled\b', 'N cap-cancelled'),
    (r'\b\d+\s+seat records?\b', 'N seat records'),
]
WORDS = r'\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|thirty-two)\b[ -]+(seat|report)'


def blob(rev, path):
    p = subprocess.run(['git', '-C', FLEET, 'cat-file', 'blob', '%s:%s' % (rev, path)],
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return p.stdout if p.returncode == 0 else None


total, seat_hits = 0, 0
for r, rev in REVS.items():
    raw = blob(rev, '.ufo/reports/round-%d/tameshi.md' % r)
    t = raw.decode('utf-8')
    n_hits, n_words = 0, len(re.findall(WORDS, t, re.I))
    if 'seat' in t.lower():
        seat_hits += 1
    print('--- round-%d rev=%s bytes=%d lines=%d crlf=%s seat_lines=%d word_number_hits=%d'
          % (r, rev[:12], len(raw), t.count('\n'), b'\r\n' in raw,
             sum(1 for l in t.splitlines() if 'seat' in l.lower()), n_words))
    seen = set()
    for pat, label in PATS:
        for m in re.finditer(pat, t):
            s, e = m.start(), m.end()
            tok = m.group(0)
            if (s, tok) in seen:
                continue
            seen.add((s, tok))
            b0 = len(t[:s].encode('utf-8'))
            b1 = len(t[:e].encode('utf-8'))
            sl = raw[b0:b1].decode('utf-8')
            ctx = t[max(0, s - 55):e + 45].replace('\r', '').replace('\n', '\\n')
            print('  line=%-4d bytes[%d:%d] slice=%-20r %-16s ctx=%r'
                  % (t.count('\n', 0, s) + 1, b0, b1, sl, label, ctx))
            total += 1
        # dedupe across patterns by exact byte span is not possible pre-encode;
        # report is inspected by hand from these lines
print()
print('claim_spans_enumerated=%d reports_with_any_seat_line=%d' % (total, seat_hits))
