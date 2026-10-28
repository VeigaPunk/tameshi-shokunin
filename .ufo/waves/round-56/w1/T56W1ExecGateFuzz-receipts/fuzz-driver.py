#!/usr/bin/env python3
"""Round-56 W1 T56W1ExecGateFuzz: crafted-receipt fuzz of the frozen
tools/receipt-revision-gate.py (sha256 1d80f8a6...).  Read-only against the lane:
the gate is copied to scratch and the revisions live in a scratch git fixture.

usage: fuzz-driver.py GATE FIXTURE REVS_ENV COLLISION_FILE OUTDIR
Writes OUTDIR/fuzz.tsv and OUTDIR/fuzz.log.  Never mutates the lane.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

GATE, FIXTURE, REVS_ENV, COLLISION_FILE, OUTDIR = sys.argv[1:6]
OUTDIR = Path(OUTDIR)
RECEIPTS = OUTDIR / 'fuzz-receipts'
RECEIPTS.mkdir(parents=True, exist_ok=True)

revs = {}
for line in Path(REVS_ENV).read_text().splitlines():
    if '=' in line:
        k, v = line.split('=', 1)
        revs[k] = v
A, B, C, SD = revs['A'], revs['B'], revs['C'], revs['SD']
TAGHEX = revs['TAGHEX']
C7, C12, C6 = C[:7], C[:12], C[:6]
UP12 = C12.upper()
coll_line = Path(COLLISION_FILE).read_text().splitlines()[0].split()
COLL, BLOB = coll_line[0], coll_line[1]
C7TAG = C7  # tag of this name exists at B

# ---- the crafted receipts ------------------------------------------------------
# (id, role, body, certified, paths, sidecar, expected)
#   expected = "ACCEPT" or the refusal code the C2 claim implies; kind is the
#   correctness verdict, recorded separately below.
cases = [
    ('01-no-rev', 'positive',
     'VERDICT: control set passed, no revision recorded\n', 'C', None, None,
     'RECEIPT_REV_ABSENT', 'RIGHT'),
    ('02-two-revs-positive', 'positive',
     'A rev=%s\nB rev=%s\n' % (A, B), 'C', None, None,
     'RECEIPT_REV_AMBIGUOUS', 'RIGHT'),
    ('03-rev-in-path-mismatch', 'positive',
     'wrote logs/rev=%s/run.log; controls passed\n' % A, 'C', None, None,
     'RECEIPT_REV_ABSENT', 'MISLABEL'),
    ('04-rev-in-path-certified', 'positive',
     'wrote logs/rev=%s/run.log; controls passed\n' % C, 'C', None, None,
     'RECEIPT_REV_ABSENT', 'FALSE_ACCEPT'),
    ('05-json-rev', 'verdict',
     '{"rev": "%s", "claim": "C2", "pass": true}\n' % C, 'C', None, None,
     'ACCEPT', 'RIGHT'),
    ('06-json-rev-uppercase', 'verdict',
     '{"rev": "%s"}\n' % UP12, 'C', None, None,
     'ACCEPT', 'FALSE_REFUSE'),
    ('07-certified-other-claim', 'verdict',
     'CLAIM=C1 rev=%s C1_R56_PASS=true\n' % C, 'C', None, None,
     'ACCEPT', 'DECLARED_GAP'),
    ('08-sidecar-match', 'positive',
     'VERDICT: rev=%s C2_R56_PASS=true\n' % C, 'C', None, 'MATCH',
     'ACCEPT', 'RIGHT'),
    ('09-sidecar-mismatch', 'positive',
     'VERDICT: rev=%s C2_R56_PASS=true\n' % C, 'C', None, 'ZERO',
     'RECEIPT_DIGEST_MISMATCH', 'RIGHT'),
    ('10-sidecar-empty', 'positive',
     'VERDICT: rev=%s C2_R56_PASS=true\n' % C, 'C', None, 'EMPTY',
     'RECEIPT_DIGEST_MISMATCH', 'RIGHT'),
    ('11-sidecar-uppercase', 'positive',
     'VERDICT: rev=%s C2_R56_PASS=true\n' % C, 'C', None, 'UPPER',
     'ACCEPT', 'FALSE_REFUSE'),
    ('12-tag-lightweight', 'positive', 'rev=rel-b\n', 'C', None, None,
     'RECEIPT_REV_ABSENT', 'RIGHT'),
    ('13-tag-annotated', 'positive', 'rev=ann-a\n', 'C', None, None,
     'RECEIPT_REV_ABSENT', 'RIGHT'),
    ('14-tag-shadows-commit-prefix', 'positive', 'rev=%s\n' % TAGHEX, 'B', None, None,
     'RECEIPT_REV_MISMATCH', 'FALSE_ACCEPT'),
    ('15-tag-shadows-certified-prefix', 'positive', 'rev=%s\n' % C7TAG, 'C', None, None,
     'ACCEPT', 'FALSE_REFUSE'),
    ('16-rev-in-comment', 'positive',
     '# measured at rev=%s\nVERDICT: control set passed\n' % C, 'C', None, None,
     'RECEIPT_REV_ABSENT', 'FALSE_ACCEPT'),
    ('17-comment-plus-real', 'positive',
     '# historical rev=%s\nVERDICT: rev=%s C2_R56_PASS=true\n' % (A, C), 'C', None, None,
     'ACCEPT', 'FALSE_REFUSE'),
    ('18-rev-in-code-fence', 'positive',
     '```\nrev=%s\n```\n' % C, 'C', None, None,
     'RECEIPT_REV_ABSENT', 'FALSE_ACCEPT'),
    ('19-fence-plus-real', 'positive',
     '```\nrev=%s\n```\nVERDICT: rev=%s\n' % (A, C), 'C', None, None,
     'ACCEPT', 'FALSE_REFUSE'),
    # B's 7-hex prefix is not shadowed by a tag; C's is (see case 15).
    ('20-prefix-7', 'positive', 'VERDICT: rev=%s\n' % B[:7], 'B', None, None,
     'ACCEPT', 'RIGHT'),
    ('21-prefix-12', 'positive', 'VERDICT: rev=%s\n' % C12, 'C', None, None,
     'ACCEPT', 'RIGHT'),
    ('22-uppercase-hex', 'positive', 'VERDICT: rev=%s\n' % UP12, 'C', None, None,
     'ACCEPT', 'FALSE_REFUSE'),
    ('23-prefix-6', 'positive', 'VERDICT: rev=%s\n' % C6, 'C', None, None,
     'ACCEPT', 'FALSE_REFUSE'),
    ('24-prefix-41', 'positive', 'VERDICT: rev=%sa\n' % C, 'C', None, None,
     'RECEIPT_REV_ABSENT', 'RIGHT'),
    ('25-spaced-rev', 'positive', 'VERDICT: rev = %s\n' % C, 'C', None, None,
     'RECEIPT_REV_ABSENT', 'MISLABEL'),
    ('26-notrev', 'positive', 'notrev=%s\n' % C, 'C', None, None,
     'RECEIPT_REV_ABSENT', 'RIGHT'),
    ('27-directory-receipt', 'positive', '<DIR>', 'C', None, None,
     'RECEIPT_NOT_BLOB', 'CRASH'),
    ('28-missing', 'positive', '<MISSING>', 'C', None, None,
     'RECEIPT_MISSING', 'RIGHT'),
    ('29-empty', 'positive', '\n\n', 'C', None, None,
     'RECEIPT_EMPTY', 'RIGHT'),
    ('30-paths-launder', 'positive', 'VERDICT: rev=%s\n' % A, 'C', 'UNCHANGED', None,
     'RECEIPT_REV_CONTENT_DRIFT', 'EXPLOITABLE'),
    ('31-paths-drift', 'positive', 'VERDICT: rev=%s\n' % A, 'C', 'DRIFT', None,
     'RECEIPT_REV_CONTENT_DRIFT', 'RIGHT'),
    ('32-control-descendant', 'control', 'CTL A rev=%s\n' % SD, 'C', None, None,
     'RECEIPT_CONTROL_NOT_ANCESTOR', 'RIGHT'),
    ('33-control-equal', 'control', 'CTL A rev=%s\n' % C, 'C', None, None,
     'ACCEPT', 'RIGHT'),
    ('34-control-multi', 'control', 'CTL A rev=%s\nCTL B rev=%s\n' % (A, C), 'C', None, None,
     'ACCEPT', 'RIGHT'),
    ('35-control-unresolvable', 'control', 'CTL A rev=deadbeefdead\n', 'C', None, None,
     'RECEIPT_REV_UNRESOLVABLE', 'RIGHT'),
    ('36-ambiguous-object-prefix', 'positive', 'VERDICT: rev=%s\n' % COLL, 'C', None, None,
     'RECEIPT_REV_UNRESOLVABLE', 'MISLABEL'),
    ('37-json-plus-text', 'verdict',
     '{"rev": "%s"}\nlog rev=%s\n' % (C, A), 'C', None, None,
     'RECEIPT_REV_AMBIGUOUS', 'RIGHT'),
    ('38-json-upper-key', 'verdict', '{"REV": "%s"}\n' % C, 'C', None, None,
     'RECEIPT_REV_ABSENT', 'RIGHT'),
    ('39-blob-rev', 'positive', 'VERDICT: rev=%s\n' % BLOB, 'C', None, None,
     'RECEIPT_REV_UNRESOLVABLE', 'RIGHT'),
    ('40-required-line', 'verdict', 'VERDICT: rev=%s\n' % C, 'C', None, None,
     'RECEIPT_REQUIRED_LINE_MISSING', 'RIGHT'),
    ('41-duplicate-rev', 'positive', 'rev=%s\nagain rev=%s\n' % (C, C), 'C', None, None,
     'ACCEPT', 'RIGHT'),
    ('42-rev-in-url', 'positive',
     'GET https://example.invalid/run?rev=%s 200\n' % C, 'C', None, None,
     'RECEIPT_REV_ABSENT', 'FALSE_ACCEPT'),
    ('43-paths-empty-list', 'positive', 'VERDICT: rev=%s\n' % A, 'C', 'EMPTYFILE', None,
     'RECEIPT_REV_CONTENT_DRIFT', 'RIGHT'),
    ('44-paths-nonexistent', 'positive', 'VERDICT: rev=%s\n' % A, 'C', 'NOFILE', None,
     'RECEIPT_REV_CONTENT_DRIFT', 'FALSE_ACCEPT'),
    ('45-two-causes-one-detail', 'positive', 'VERDICT: rev=deadbeefdead\n', 'C', None, 'ZERO',
     'RECEIPT_DIGEST_MISMATCH,RECEIPT_REV_UNRESOLVABLE', 'RIGHT'),
]

paths_files = {
    'UNCHANGED': 'surface.txt\n',   # identical at A and C
    'DRIFT': 'moved.txt\n',         # gamma at A, alpha at C -> differs
    'EMPTYFILE': '# no paths listed\n',
    'NOFILE': 'no-such-path.txt\n', # git diff on an absent path is silent
}
for name, body in paths_files.items():
    (OUTDIR / ('paths-%s.txt' % name.lower())).write_text(body)

gate_hash = hashlib.sha256(Path(GATE).read_bytes()).hexdigest()
lines = ['case\trole\texpected\tobserved\tcode\texit\tverdict\tgate_sha256']
log = ['GATE_SHA256=%s' % gate_hash, 'FIXTURE=%s' % FIXTURE,
       'A=%s B=%s C=%s SD=%s TAGHEX=%s COLL=%s BLOB=%s' % (A, B, C, SD, TAGHEX, COLL, BLOB)]

for cid, role, body, cert_name, paths_name, sidecar, expected, kind in cases:
    cert = {'A': A, 'B': B, 'C': C}[cert_name]
    rpath = RECEIPTS / cid
    if body == '<DIR>':
        rpath.mkdir(exist_ok=True)
    elif body == '<MISSING>':
        pass  # leave absent
    else:
        rpath.write_text(body)
        if sidecar:
            digest = hashlib.sha256(body.encode()).hexdigest()
            val = {'MATCH': digest, 'ZERO': '0' * 64, 'EMPTY': '', 'UPPER': digest.upper()}[sidecar]
            Path(str(rpath) + '.sha256').write_text(val + ('\n' if val else ''))
    argv = [sys.executable, GATE, '--lane', FIXTURE, '--certified', cert]
    if paths_name:
        argv += ['--paths', str(OUTDIR / ('paths-%s.txt' % paths_name.lower()))]
    spec = str(rpath) + ':' + role
    if cid == '40-required-line':
        spec += ':C2_R56_PASS='
    argv += ['--receipt', spec]
    r = subprocess.run(argv, capture_output=True, timeout=120)
    out = r.stdout.decode('utf-8', 'replace')
    err = r.stderr.decode('utf-8', 'replace')
    m = re.search(r'codes=(\S+) verdict=(\w+)', out)
    codes = m.group(1) if m else 'none'
    verdict = m.group(2) if m else 'NO-VERDICT-LINE'
    if r.returncode == 0 and verdict == 'PASS':
        observed = 'ACCEPT'
    elif r.returncode == 3 and verdict == 'REFUSED':
        observed = 'REFUSE'
    else:
        observed = 'CRASH'
    lines.append('%s\t%s\t%s\t%s\t%s\t%d\t%s\t%s'
                 % (cid, role, expected, observed, codes, r.returncode, kind, gate_hash[:12]))
    log.append('')
    log.append('=== %s role=%s certified=%s paths=%s sidecar=%s expected=%s kind=%s'
               % (cid, role, cert[:12], paths_name or '-', sidecar or '-', expected, kind))
    log.append('$ ' + ' '.join(argv))
    log.append('exit=%d observed=%s codes=%s' % (r.returncode, observed, codes))
    log.append(out.rstrip())
    if err.strip():
        log.append('--- stderr ---')
        log.append(err.rstrip()[-2000:])

(OUTDIR / 'fuzz.tsv').write_text('\n'.join(lines) + '\n')
(OUTDIR / 'fuzz.log').write_text('\n'.join(log) + '\n')
print('\n'.join(lines))
