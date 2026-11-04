import runpy, pathlib, subprocess, json, copy
S=pathlib.Path('/fast/scratch/hyaku/tameshi-r78/T78W1SN1')
D=pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-78/design')
m=runpy.run_path(str(D/'selfstate-freshness.py'))
row=json.loads((D/'selfstate-freshness.json').read_text())['rows'][-1]
runner=m['GitInstrumentRunner'](str(S),str(S/'tmp/unset-sim'))
runner._extract=lambda rev,path:str(S/'tmp/unset-sim'/rev/path)
runner._support=lambda rev:None
calls=[]
def spy(args,**kwargs):
    calls.append(args)
    return subprocess.CompletedProcess(args,0,b'BASH_RESULT',b'')
subprocess.run=spy
first=runner(row)
second=copy.deepcopy(row);second['id']='python-same-path';second['instrument']['interpreter']='python'
m['validate_manifest']({'rows':[row,second]})
other=runner(second)
print('INTERPRETER_CACHE subprocess_calls=%d reused=%s requested=bash,python executed=%s'%(len(calls),str(first==other).lower(),json.dumps([x[0] for x in calls])))
