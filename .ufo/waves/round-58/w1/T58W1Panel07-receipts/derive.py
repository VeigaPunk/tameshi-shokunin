import hashlib
import json
import re
import subprocess

REPO = '/fast/scratch/hyaku/tameshi-r58/T58W1Panel07/clone'
BASE = '2a32aa8228d5f86a85c81a923a3148bf792a9538'
FIX = '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
DURABLE = 'ff2a821a1e83acd92bb4d62bad15f380973a55ea'

def git(*args, echo=True):
    cmd = ['git', '-C', REPO, *args]
    result = subprocess.run(cmd, capture_output=True, check=True)
    if echo:
        print('$ ' + ' '.join(cmd))
        print(result.stdout.decode())
    return result.stdout

def excerpt(path, first, last):
    data = git('show', BASE + ':' + path, echo=False).decode().splitlines()
    print('$ git -C ' + REPO + ' show ' + BASE + ':' + path + ' [lines ' + str(first) + '-' + str(last) + ']')
    for n in range(first, last + 1):
        print(str(n) + ':' + data[n - 1])

git('rev-parse', 'HEAD')
for commit in [FIX, DURABLE]:
    git('merge-base', '--is-ancestor', commit, BASE)
    print('ancestor exit=0: ' + commit)
excerpt('SCORECARD.md', 2654, 2690)
excerpt('.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md', 332, 343)
excerpt('corpus/lessons/round-55.md', 56, 64)
git('show', '--format=fuller', '--unified=0', FIX, '--', 'SCORECARD.md', '.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md', 'corpus/lessons/round-55.md')
for wave in [1, 2]:
    prefix = '.ufo/waves/round-54/w' + str(wave)
    paths = git('ls-tree', '-r', '--name-only', BASE, '--', prefix, echo=False).decode().splitlines()
    paths = [p for p in paths if re.fullmatch(prefix + r'/T54W' + str(wave) + r'Read\d+\.json', p)]
    counts = [(p, len(json.loads(git('show', BASE + ':' + p, echo=False))['findings'])) for p in paths]
    print('DERIVE committed ' + prefix + ' direct Read JSON findings:')
    print(json.dumps(counts))
    print(json.dumps({'wave': wave, 'readers': len(counts), 'findings': sum(n for _, n in counts), 'sections_with_findings': sum(n > 0 for _, n in counts)}))
resolutions = json.loads(git('show', BASE + ':.ufo/evidence/round-54/integrate/resolutions.json', echo=False))
print('RESOLUTIONS ' + json.dumps({'sections': len(resolutions), 'findings': sum(len(x['findings']) for x in resolutions)}))
blob = git('show', BASE + ':.ufo/evidence/round-54/c2/measure.py', echo=False)
print('R54.4 counter SHA256 ' + hashlib.sha256(blob).hexdigest())
print(git('show', BASE + ':.ufo/evidence/round-54/freeze.json', echo=False).decode())
paths = ['.ufo/waves/round-54/w2/T54W2Sent03.md', '.ufo/waves/round-54/w2/T54W2Sent03-receipts/c1committed-positive.stdout', '.ufo/waves/round-54/w2/T54W2Sent03-receipts/rejection-attribution.txt']
git('show', '--format=fuller', '--stat', DURABLE, '--', *paths)
for path in paths:
    git('ls-tree', BASE, '--', path)
    print('DURABILITY bytes equal at introduction/base: ' + str(git('show', DURABLE + ':' + path, echo=False) == git('show', BASE + ':' + path, echo=False)) + ' ' + path)
git('show', '--format=%H %s', '--name-status', '7fa9a5e', '--', '.ufo/waves/round-54/w2/T54W2Sent01-forged-reader.json', '.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json')
git('ls-tree', BASE, '--', '.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json')
