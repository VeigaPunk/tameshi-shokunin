import re
line = [l for l in open('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/before/c2.stdout')
        if l.startswith('C2_R54:')][-1].strip()
f = dict(re.findall(r'(\w+)=(\d+)', line))
t = int(f['tools'])
e2 = t - int(f['unusable_exit2']); n = t - int(f['naming']); eo = t - int(f['empty_ok'])
uo = t - int(f['usable_ok']); d = t - int(f['docs'])
pen = (0 if int(f['note']) else 1) + (0 if int(f['sources']) else 1)
total = e2 + n + eo + uo + d + pen
print('line:', line)
print('terms: exit2=%d naming=%d empty=%d usable=%d docs=%d note_sources_penalty=%d' % (e2, n, eo, uo, d, pen))
print('RECOMPUTED_TOTAL=%d PRINTED_TOTAL=%s MATCH=%s' % (total, f['total'], total == int(f['total'])))
