import importlib.util, json, os, shutil, subprocess, sys, tempfile
S=os.getcwd(); LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'; REV='21ef81e9'
DEP='.ufo/evidence/round-18/measure.py'
spec=importlib.util.spec_from_file_location('ssf',os.path.join(S,'selfstate-freshness.py'))
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

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
        run=subprocess.run([sys.executable,'-I','-X','utf8',target]+list(argv),cwd=LANE,capture_output=True)
        return (run.stdout+run.stderr).decode('utf-8','replace')
    finally: shutil.rmtree(work,ignore_errors=True)

doc=m.load_doc(LANE,REV,'SCORECARD.md',m.GitReader(LANE))
start=doc.index('## Capabilities'); end=doc.index('\n## ',start+1)
section=doc[start:end]
REPAIRS=[
 ('RECEIPT_COMMIT_BIND_SELFTEST: 4/4 pass','RECEIPT_COMMIT_BIND_SELFTEST: 7/7 pass'),
 ('QUOTED_LINE_EXISTS_SELFTEST: 4/4 pass','QUOTED_LINE_EXISTS_SELFTEST: 5/5 pass'),
 ('ARM_LIVENESS_SELFTEST: 4/4 pass','ARM_LIVENESS_SELFTEST: 5/5 pass'),
 ('rows=3 live=3 dead=0','rows=9 live=9 dead=0'),
 ('ANCHOR_DRIFT: rows=4 met=4 unexpected=0','ANCHOR_DRIFT: rows=16 met=16 unexpected=0'),
 ('POINTER_RECHECK: rows=8 met=8 unexpected=0','POINTER_RECHECK: rows=12 met=12 unexpected=0'),
 ('ADDRANGE: rows=6 met=6 unexpected=0','ADDRANGE: rows=11 met=11 unexpected=0'),
]
for old,new in REPAIRS:
    n=section.count(old)
    print('capability-section occurrences %d: %s' % (n, old))
    assert n==1, n
    section=section.replace(old,new)
patched=doc[:start]+section+doc[end:]
rows,match,stale,unexpected=m.sweep({'rows':json.load(open('manifest17.json'))['rows']},patched,m.GitReader(LANE),mirror_runner)
for r in rows:
    if r['state']!='match' or not r['ok']:
        print('SELFSTATE_ROW %s expect=%s measured=%s %s' % (r['id'],r['expect'],r['state'],'ok' if r['ok'] else 'UNEXPECTED'))
print('SELFSTATE: rows=%d match=%d stale=%d unexpected=%d' % (len(rows),match,stale,unexpected))
sys.exit(0 if unexpected==0 else 1)
