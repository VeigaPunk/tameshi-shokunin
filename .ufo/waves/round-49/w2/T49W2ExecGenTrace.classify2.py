"""Classify strace openat/open/execve events for the T49W2ExecGenTrace deliverable.

Buckets: python-install, tmpdir (the run's TMPDIR), and outside.  Every event that
cannot be bucketed from an absolute path is reported as dirfd-relative instead of
being dropped, so nothing is silently skipped.
"""
import collections
import re
import sys

S, trace, tmp = sys.argv[1], sys.argv[2], sys.argv[3]
PY = ('/usr/lib/python3', '/usr/lib64/python3', '/usr/local/lib/python3')
call_re = re.compile(r'^(?P<pid>\d+)\s+(?P<call>openat|open|execve)\((?P<rest>.*)$')

events = []          # (kind, path_or_name, dirfd)
unparsed = []
for line in open(trace, encoding='utf-8', errors='replace'):
    m = call_re.match(line)
    if not m:
        continue
    rest = m.group('rest')
    if m.group('call') == 'execve':
        p = re.match(r'"([^"]*)"', rest)
        events.append(('execve', p.group(1) if p else '<unparsed>', False))
        continue
    d = re.match(r'AT_FDCWD, "([^"]*)"', rest)
    if d:
        events.append(('open', d.group(1), False))
        continue
    d = re.match(r'(?P<fd>\d+|AT_FDCWD), "(?P<name>[^"]*)"', rest)
    if d:
        events.append(('open', d.group('name'), True))
        continue
    unparsed.append(line.rstrip())


def bucket(path, dirfd):
    if dirfd:
        return 'dirfd-relative'
    if path.startswith(tmp + '/'):
        return 'tmpdir'
    if path.startswith(PY):
        return 'python-install'
    return 'outside'


counts = collections.Counter()
first = {}
for i, (kind, path, dirfd) in enumerate(events):
    key = (bucket(path, dirfd), kind, path)
    counts[key] += 1
    first.setdefault(key, i)

print('TRACE %s' % trace)
print('TOTAL_PARSED_EVENTS %d  UNPARSED_LINES %d' % (len(events), len(unparsed)))
for b in ('outside', 'dirfd-relative', 'tmpdir', 'python-install'):
    keys = sorted([k for k in counts if k[0] == b], key=lambda k: first[k])
    print('BUCKET %s distinct=%d events=%d' % (b, len(keys), sum(counts[k] for k in keys)))
    if b in ('outside', 'dirfd-relative'):
        for k in keys:
            print('  %-7s n=%-5d %s' % (k[1], counts[k], k[2]))
