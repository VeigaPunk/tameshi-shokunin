import importlib.util, sys
p=sys.argv[1]
s=importlib.util.spec_from_file_location('wr',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
r=m.REV
row={'id':'sr-no-printed','kind':'seat_reports','record':{'path':'report.md','rev':r,'span':'11 reports'},'wave':{'dir':'wave','rev':r}}
reader=m.FixtureReader({(r,'report.md'):m.REPORT},{(r,'wave'):['wave/a.md','wave/b.md']})
try: print(m.measure(row,{'lane':reader}))
except Exception as e: print(type(e).__name__+': '+str(e))
