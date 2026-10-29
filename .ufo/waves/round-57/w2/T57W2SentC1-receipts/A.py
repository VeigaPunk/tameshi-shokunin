import sys
sys.path.insert(0,'/fast/scratch/hyaku/tameshi-r57/T57W2SentC1/h')
from scen import *
ids=[d['id'] for d in D]
forged=lambda r: r['status_at_base']
honest=lambda r: truth(r['id'])
which=sys.argv[1]
if which=='A1':   # all 51 fixed via one probe commit naming every id; forged panel
    r=run('A1_all51_probe_forgedpanel', ids, forged, probe_msg='round-57 notes for '+' '.join(ids))
elif which=='A1t':
    r=run('A1t_all51_probe_TRUTHpanel', ids, honest, probe_msg='round-57 notes for '+' '.join(ids))
elif which=='A2':  # 6 probe fixes (floor) + 45 open with lane-keyed evidence; forged panel
    r=run('A2_6probe_45open_forgedpanel', ids[:6], forged, probe_msg='round-57 notes for '+' '.join(ids[:6]))
elif which=='A2t':
    r=run('A2t_6probe_45open_TRUTHpanel', ids[:6], honest, probe_msg='round-57 notes for '+' '.join(ids[:6]))
print('TOTAL', which, r['total'])
