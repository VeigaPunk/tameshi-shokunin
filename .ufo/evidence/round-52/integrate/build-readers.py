#!/usr/bin/env python3
"""Assemble refresh.py READERS_JSON mechanically from fresh wave-3 reader reports.

Usage: build-readers.py LANE CAND OUT.json. Every section is matched by exact heading against the precheck's LOST
list. Reader JSON quote must occur byte-exact in its Markdown report. The output points only at committed wave-3
reader files (the wave results are committed before refresh runs). Missing reader is reported, never fabricated.
"""
import glob, hashlib, json, os, subprocess, sys
lane, cand, outpath = sys.argv[1:]
W = os.path.join(lane, '.ufo/waves/round-52/w3')
pre = os.path.join(lane, '.ufo/evidence/round-52/integrate/precheck-cand1.stdout')
lost = [l.split(' | ')[0][5:] for l in open(pre) if l.startswith('LOST ')]
readers = {}; missing = []
for h in lost:
    files = glob.glob(os.path.join(W, 'T52W3Read*.json'))
    matches = []
    for f in files:
        d = json.load(open(f, encoding='utf-8'))
        if d.get('heading') == h and d.get('cand') == cand:
            matches.append((f, d))
    if len(matches) != 1:
        missing.append((h, len(matches))); continue
    f, d = matches[0]; report = f[:-5] + '.md'; text = open(report, encoding='utf-8').read()
    for x in d.get('findings', []):
        if x.get('quote') not in text:
            raise SystemExit('quote not verbatim in %s: %r' % (report, x.get('quote')))
    # Verify the reader reported the exact section bytes its hash names.
    sec = subprocess.run(['git', '-C', lane, 'show', cand + ':SKILL.md'], capture_output=True, text=True, check=True).stdout.split('\n')
    start = sec.index(h); end = start + 1
    while end < len(sec) and not (sec[end].startswith('#') and len(sec[end].split(' ', 1)[0]) <= 3): end += 1
    sh = hashlib.sha256('\n'.join(sec[start:end]).encode()).hexdigest()
    if d.get('section_sha256') != sh:
        raise SystemExit('section sha mismatch %s expected=%s got=%s' % (h, sh, d.get('section_sha256')))
    readers[h] = {'seats': [os.path.basename(f)[:-5]], 'reader_files': [os.path.relpath(report, lane)],
                  'findings': d.get('findings', [])}
for h, n in missing:
    print('MISSING_READER', h, 'matches=%d' % n)
json.dump(readers, open(outpath, 'w'), indent=1, ensure_ascii=False)
print('READERS: lost=%d covered=%d missing=%d findings=%d' % (len(lost), len(readers), len(missing), sum(len(x['findings']) for x in readers.values())))
if missing:
    sys.exit(1)
