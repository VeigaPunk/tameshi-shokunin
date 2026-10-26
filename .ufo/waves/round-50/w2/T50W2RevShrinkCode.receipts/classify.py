"""Classify the strace log: every write-ish syscall target and every read target,
whitelisted by path prefix. Prints anything outside the whitelist."""
import re

S = '/fast/scratch/hyaku/tameshi-r50/T50W2RevShrinkCode'
B = S + '/fix/b'

WRITE_OK_PREFIXES = (
    B + '/tmp-strace',          # the handed TMPDIR (incl. its mkdtemp children)
    B + '/out-strace.json',     # the handed --out
    B + '/.runs',               # written by the counter-style instrumented guards (not shrinker code)
    B + '/count.log',           # written by my exec-counting wrappers
    B + '/cwdrun2',             # not expected, but flag separately if hit
)
READ_OK_PREFIXES = (
    S + '/fix',                 # tool, generator, guards, case, fixture tree
    '/usr/lib/python3',
    '/usr/lib/locale',
    '/usr/local/lib',
    '/etc/ld.so',
    '/etc/localtime',
    '/proc/',
    '/sys/',
    '/dev/urandom',
)

open_re = re.compile(r'open(at)?\((.*?)"((?:[^"\\]|\\.)*)"(.*)\)\s*=')
plain_re = re.compile(r'^\d+\s+(creat|unlink|unlinkat|rename|renameat|mkdir|mkdirat|rmdir|execve)\((.*?)\)\s*=')
flag_re = re.compile(r'(O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_EXCL|O_APPEND)')

writes, reads, others = {}, {}, {}


def add(bucket, path, line):
    bucket.setdefault(path, []).append(line.strip()[:180])


for raw in open(S + '/trace.log', encoding='utf-8', errors='replace'):
    line = raw.rstrip('\n')
    if '<unfinished' in line or 'resumed' in line:
        continue
    m = open_re.search(line)
    if m:
        path = m.group(3).replace('\\"', '"')
        flags = m.group(4)
        w = bool(flag_re.search(flags)) or 'O_WRONLY' in flags
        if w:
            add(writes, path, line)
        else:
            add(reads, path, line)
        continue
    m = plain_re.match(line)
    if m:
        call, args = m.group(1), m.group(2)
        pm = re.search(r'"((?:[^"\\]|\\.)*)"', args)
        path = pm.group(1).replace('\\"', '"') if pm else args[:60]
        if call == 'execve' or call == 'write':
            continue
        add(others, '%s %s' % (call, path), line)

print('== WRITE-ish targets outside whitelist ==')
for path in sorted(writes):
    if not path.startswith(WRITE_OK_PREFIXES):
        print('  %s' % path)
        for l in writes[path][:2]:
            print('      %s' % l)
print('== WRITE-ish targets inside whitelist (summary) ==')
for path in sorted(writes):
    if path.startswith(WRITE_OK_PREFIXES):
        print('  %s  (%d call(s))' % (path, len(writes[path])))
print('== mutating calls (creat/unlink/rename/mkdir/rmdir) outside TMPDIR+out ==')
for key in sorted(others):
    tgt = key.split(' ', 1)[1]
    if not (tgt.startswith(B + '/tmp-strace') or tgt == B + '/out-strace.json'
            or tgt.startswith(B + '/.runs') or tgt.startswith(B + '/count.log')):
        print('  %s' % others[key][0])
print('== READ targets outside whitelist ==')
for path in sorted(reads):
    if not path.startswith(READ_OK_PREFIXES):
        for l in reads[path][:2]:
            print('  %s' % l)
print('== read-target families inside whitelist (top) ==')
fams = {}
for path in reads:
    fam = path.split('/python3.14/')[0] + '/python3.14/...' if '/python3.14/' in path else path
    fams[fam] = fams.get(fam, 0) + 1
for fam, n in sorted(fams.items(), key=lambda kv: -kv[1])[:14]:
    print('  %4d  %s' % (n, fam))
