import importlib.util, json, os, sys
exec(open(os.environ['HYAKU_SCRATCH']+'/tameshi-r57/T57W2CritPanel/drive.py').read().split("truth=dict(derived)")[0])
rows_h,pl_h=ledger(set())
rev,pin=make_rev('probe_honest', rows_h, pl_h, dict(derived))
notes=[]
res=m.measure(C, rev, defects, True, 0, 999, 0, B, 49, m.EXPECTED_SPOTS, explain=lambda *a: notes.append(a), panel_pin=pin, panel_allowed=5)
for n in notes: print(n)
