import importlib.util, json, os, shutil, subprocess, sys, tempfile
S=os.getcwd(); LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'; REV='21ef81e9'
DEP='.ufo/evidence/round-18/measure.py'
def blob(rev,path):
    return subprocess.run(['git','-C',LANE,'cat-file','blob','%s:%s'%(rev,path)],capture_output=True,check=True).stdout
def mirror_runner(rev,path,argv):
    work=tempfile.mkdtemp(prefix='ssf-mirror-',dir=os.environ.get('TMPDIR') or None)
    try:
        target=os.path.join(work,path); os.makedirs(os.path.dirname(target),exist_ok=True)
        open(target,'wb').write(blob(rev,path))
        try: dep=blob(rev,DEP)
        except subprocess.CalledProcessError: dep=None
        if dep is not None:
            dpath=os.path.join(work,DEP); os.makedirs(os.path.dirname(dpath),exist_ok=True); open(dpath,'wb').write(dep)
        r=subprocess.run([sys.executable,'-I','-X','utf8',target]+list(argv),cwd=LANE,capture_output=True)
        return (r.stdout+r.stderr).decode('utf-8','replace')
    finally: shutil.rmtree(work,ignore_errors=True)
base=json.load(open('manifest17.json'))
rename=json.loads(json.dumps(base))
for row in rename['rows']:
    if row['id']=='r-receipt-exists':
        row['capability']='receipt-existence sweepX'
for label,manifest in [('renamed-capability',rename),('zero-rows',{'rows':[]})]:
    for mod in ['selfstate-freshness.py','m_c_capability_absent_match.py','m_d_zero_rows_success.py']:
        spec=importlib.util.spec_from_file_location('x',os.path.join(S,mod))
        mm=importlib.util.module_from_spec(spec); spec.loader.exec_module(mm)
        doc=mm.load_doc(LANE,REV,'SCORECARD.md',mm.GitReader(LANE))
        try:
            rows,match,stale,unexpected=mm.sweep(manifest,doc,mm.GitReader(LANE),mirror_runner)
            print('%-18s %-32s rows=%d match=%d stale=%d unexpected=%d' % (label,mod,len(rows),match,stale,unexpected))
        except Exception as exc:
            print('%-18s %-32s SETUP %s' % (label,mod,exc))
