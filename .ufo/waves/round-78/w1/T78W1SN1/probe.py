import os, sys, pathlib, subprocess, runpy, hashlib, json, copy, tempfile
S=pathlib.Path('/fast/scratch/hyaku/tameshi-r78/T78W1SN1')
L=pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
D=L/'.ufo/evidence/round-78/design'
mode=sys.argv[1]
tmp=S/'tmp/unset-sim'; tmp.mkdir(parents=True,exist_ok=True)
os.environ['TMPDIR']=str(tmp); tempfile.tempdir=None
os.environ['GIT_CONFIG_COUNT']='1'; os.environ['GIT_CONFIG_KEY_0']='commit.gpgsign'; os.environ['GIT_CONFIG_VALUE_0']='false'
os.chdir(S)
original=subprocess.run
initcount=0
force=int(sys.argv[2]) if len(sys.argv)>2 else 0

def guarded(args,*a,**kw):
    global initcount
    if isinstance(args,list) and args[0]=='git':
        if 'init' in args:
            initcount+=1
            if force and initcount==force:
                raise FileNotFoundError('sentinel forced git missing at init %d'%force)
        if 'commit' in args:
            root=args[args.index('-C')+1]
            top=original(['git','-C',root,'rev-parse','--show-toplevel'],check=True,stdout=subprocess.PIPE).stdout.decode().strip()
            assert os.path.realpath(top)==os.path.realpath(root)
            assert pathlib.Path(root).is_relative_to(tmp)
            print('FIXTURE_COMMIT_ROOT_OK '+root,flush=True)
    return original(args,*a,**kw)
subprocess.run=guarded
if mode in ('selfstate','wave'):
    path=D/('selfstate-freshness.py' if mode=='selfstate' else 'wave-reconcile.py')
    print('CANDIDATE_SHA256 '+path.name+' '+hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
    sys.argv=[str(path),'--selftest']
    try:
        runpy.run_path(str(path),run_name='__main__')
    except BaseException as e:
        print('TERMINAL '+type(e).__name__+' '+str(e),flush=True)
    leftovers=sorted(str(p.relative_to(tmp)) for p in tmp.iterdir())
    print('LEFTOVER_COUNT='+str(len(leftovers))+' '+json.dumps(leftovers),flush=True)
elif mode=='boundary':
    m=runpy.run_path(str(D/'selfstate-freshness.py'))
    manifest=json.loads((D/'selfstate-freshness.json').read_text())
    row=manifest['rows'][-1]
    for p in ['/absolute/tool.sh','../escape.sh','tools/../escape.sh','tools/toy.sh']:
        r=copy.deepcopy(row);r['instrument']['path']=p
        try:
            m['validate_manifest']({'rows':[r]}); result='ACCEPT'
        except m['SetupError'] as e: result='REFUSE '+str(e)
        print('PATH '+json.dumps(p)+' '+result)
    for argv in [['-c','printf injected'],['--rcfile','/not/executed'],['other.sh']]:
        r=copy.deepcopy(row);r['instrument']['argv']=argv
        m['validate_manifest']({'rows':[r]})
        print('ARGV_VALIDATED '+json.dumps(argv))
    calls=[]
    def spy(args,**kw):
        calls.append({'args':args,'cwd':kw.get('cwd')})
        return subprocess.CompletedProcess(args,0,b'figure',b'')
    runner=m['GitInstrumentRunner'](str(L),str(tmp))
    runner._extract=lambda rev,path:str(tmp/rev/path)
    runner._support=lambda rev:None
    subprocess.run=spy
    r=copy.deepcopy(row);r['instrument']['argv']=['-c','printf injected']
    runner(r)
    print('CAPTURED_COMMAND '+json.dumps(calls))
    subprocess.run=guarded
    print('BASH_ROW '+json.dumps(row,sort_keys=True))
    raw=original(['git','-C',str(L),'cat-file','blob',row['instrument']['rev']+':'+row['instrument']['path']],check=True,stdout=subprocess.PIPE).stdout
    print('BASH_BLOB_SHA256 '+hashlib.sha256(raw).hexdigest())
elif mode=='unset':
    os.environ.pop('TMPDIR',None)
    os.environ.pop('TEMP',None)
    os.environ.pop('TMP',None)
    tempfile.tempdir=None
    def no_create(*args,**kw):
        print('UNSET_MKDTEMP '+json.dumps({'args':args,'kwargs':kw}),flush=True)
        raise RuntimeError('sentinel stopped before default-root creation')
    tempfile.mkdtemp=no_create
    for name in ['selfstate-freshness.py','wave-reconcile.py']:
        m=runpy.run_path(str(D/name))
        print('UNSET_CANDIDATE '+name)
        try:
            m['main'](['--selftest'])
        except RuntimeError as e:
            print('UNSET_STOP '+str(e))
    print('DEFAULT_TMP_CANDIDATES '+json.dumps(tempfile._candidate_tempdir_list()))
