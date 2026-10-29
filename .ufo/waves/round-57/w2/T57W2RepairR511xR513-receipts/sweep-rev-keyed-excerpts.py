import subprocess, re, sys
C = sys.argv[1]
def show(rev, path):
    return subprocess.run(['git', '-C', C, 'show', '%s:%s' % (rev, path)], capture_output=True).stdout.decode('utf-8', 'replace')
norm = lambda t: ' '.join(t.split())
rev_lines = show('master', 'tools/registry.json').split('\n')
bcba = norm(show('bcba8924894216268afc4171f06eb8c28e912b46', 'tools/registry.json'))
par = norm(show('1f72d7d8189042b434a2f3753c2c346aefd5ec0f', 'tools/registry.json'))
KEYS = ['mte-interop-check', 'ten-leg', 'registry-check --only mte-interop-check']
hits = []
for i, line in enumerate(rev_lines, 1):
    if not any(re.search(r'(?<![\w-])' + re.escape(k) + r'(?![\w-])', line, re.I) for k in KEYS[:2]):
        continue
    for a in range(max(1, i - 30), i + 1):
        for b in range(i, min(len(rev_lines), a + 30) + 1):
            W = norm('\n'.join(rev_lines[a - 1:b]))
            # candidate substrings of W (15..400 chars) that contain 'mte-interop-check' or 'ten-leg'
            for s in range(len(W)):
                for e in range(s + 15, min(len(W), s + 400) + 1):
                    S = W[s:e]
                    if not re.search(r'(?<![\w-])(mte-interop-check|ten-leg)(?![\w-])', S, re.I):
                        continue
                    if S in bcba and S not in par:
                        hits.append((a, b, S[:120]))
                        break
                else:
                    continue
                break
    if hits:
        break
print('REV key lines scanned; candidate (in bcba892, absent at parent, keyed) hits:', len(hits))
for h in hits[:5]:
    print(h)
