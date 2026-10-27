import importlib.util, json, os, sys
S = sys.argv[1]; L = sys.argv[2]
CAND = '7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135'
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
c1 = load(os.path.join(L, '.ufo/evidence/round-49/c1/measure.py'), 'c1mod')
refresh = load(os.path.join(L, '.ufo/evidence/round-52/coldread/refresh.py'), 'refreshmod')
refresh.c1 = c1
clone = os.path.join(S, 'clone')
targets = [l.split('|',1)[0].replace('LOST ','').strip() for l in open(os.path.join(L,'.ufo/evidence/round-52/integrate/precheck-cand1.stdout')) if l.startswith('LOST ')]
print('VOLATILE', sorted(c1.VOLATILE))
secs = refresh.sections_at(clone, CAND)
print('sections_at=%d targets=%d' % (len(secs), len(targets)))
bad = 0
for h in targets:
    if h not in secs:
        print('ABSENT', h); bad += 1; continue
    sec = secs[h]
    direct, records, internal = refresh.cited_files(clone, CAND, sec['text'])
    followed = []
    if not direct:
        direct, more = refresh.follow_internal(clone, CAND, internal)
        records = sorted(set(records) | set(more)); followed = ['%d-%d' % (a,b) for a,b in internal]
    ok = bool(direct)
    if not ok: bad += 1
    print('%s %s | start=%d end=%d direct=%s records=%s internal=%s' % ('OK  ' if ok else 'ABORT', h[:58], sec['start'], sec['end'], direct, records, followed))
print('WOULD_ABORT=%d of %d' % (bad, len(targets)))
