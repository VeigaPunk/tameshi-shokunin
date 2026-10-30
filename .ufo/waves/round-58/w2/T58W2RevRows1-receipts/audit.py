import importlib.util, json, pathlib, re, subprocess, sys
CLONE=sys.argv[1]
C0='8063d0a551fc5b3cb5a2d397da7353af53444534'
BASE='2a32aa8228d5f86a85c81a923a3148bf792a9538'
ROOT=pathlib.Path(__file__).parent
commands=[]
def git(*args):
    cmd=['git','-C',CLONE,*args]
    p=subprocess.run(cmd,capture_output=True,text=True)
    commands.append({'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    return p

def blob(rev,path):
    return git('show',rev+':'+path).stdout

spec=importlib.util.spec_from_file_location('frozen',str(pathlib.Path(CLONE)/'.ufo/evidence/round-58/c1/measure.py'))
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
items=json.loads(blob(C0,'.ufo/evidence/round-58/c1/defects.json'))['defects'][:12]
rows={r['id']:r for r in json.loads(blob(C0,'corpus/routed-defects.json'))['defects']}
panel=json.loads(blob(C0,m.PANEL_PATH))
pc={k:v.get('commit','') for k,v in panel['detail'].items()}
results=[]
for d in items:
    r=rows[d['id']]; notes=[]
    stat={'fixed':0,'open':0,'declined':0,'fixed_this_round':0}
    fault=m.judge(CLONE,C0,d,r,m.planned_ids(CLONE,C0),{}, {i['file']:i['file_sha256'] for i in items},BASE,stat,lambda *a:notes.append(a),pc)
    result={'id':d['id'],'statement':d['text'],'keys':d['keys'],'row':r,'structural_fault':fault,'diagnostics':notes,'panel_status_at_base':panel['verdicts'][d['id']],'planned_current':d['id'] in m.planned_ids(CLONE,C0),'evidence_checks':[]}
    if 'commit' in r:
        c=r['commit']; result['ancestor_c0']=git('merge-base','--is-ancestor',c,C0).returncode==0
        result['ancestor_base']=git('merge-base','--is-ancestor',c,BASE).returncode==0
        result['commit_message']=git('log','-1','--format=%B',c).stdout
        result['touched']=git('diff-tree','--no-commit-id','--name-only','-r','--root','-m',c).stdout.splitlines()
        parent=git('rev-list','--parents','-n','1',c).stdout.split()[1]
    for e in r['evidence']:
        lines=blob(C0,e['path']).splitlines(); a,b=map(int,e['lines'].split('-')); excerpt=m.norm(e['excerpt'])
        check={'path':e['path'],'lines':e['lines'],'length':len(excerpt),'in_lines':excerpt in m.norm(' '.join(lines[a-1:b])),'whole_token_or_path_key':m.has_key(e,d['keys']),'span_ACK_WORDS':[w for w in m.ACK_WORDS if w in ' '.join(lines[a-1:b]).lower()]}
        if 'commit' in r and check['whole_token_or_path_key']:
            check['absent_at_routed']=excerpt not in m.norm(blob(d['routed_at'],e['path']))
            check['absent_at_fix_parent']=excerpt not in m.norm(blob(parent,e['path']))
            check['touched_by_fix']=e['path'] in result['touched']
        result['evidence_checks'].append(check)
    results.append(result)

snippets=[]
def excerpt(label,rev,path,a,b):
    p=git('show',rev+':'+path); lines=p.stdout.splitlines()
    snippets.append({'label':label,'command':commands[-1]['command'],'exit':p.returncode,'output':'\n'.join(str(j+1)+': '+lines[j] for j in range(a-1,min(b,len(lines))))})
for rev in (BASE,C0):
    excerpt('S022',rev,'corpus/SOURCES.md',33,33)
    excerpt('R50 monitor',rev,'.ufo/evidence/round-51/no-harm.sh',3,12)
    excerpt('round51 correction',rev,'corpus/lessons/round-51.md',5,16)
    excerpt('frontier supersession',rev,'corpus/README.md',610,628)
    excerpt('registry ten-leg',rev,'tools/registry.json',1251,1274)
    excerpt('registry allowance',rev,'.ufo/evidence/round-52/no-harm.sh',1,45)
    excerpt('mte fix-revision committed receipt',rev,'.ufo/waves/round-52/w2/T52W2ExecC1Probe.stdout',1,4)
    excerpt('mte isolated committed receipt',rev,'.ufo/waves/round-52/w2/T52W2ExecC1Probe/registry-check-only-mte.stdout',1,4)
    excerpt('SKILL counts and registry',rev,'SKILL.md',2177,2203)
    excerpt('coldread correction',rev,'.ufo/evidence/round-21/coldread/ledger.json',135653,135702)
    excerpt('fleet-bound declaration',rev,'tools/round21-measure.py',1,13)
    excerpt('kill-rate supersession',rev,'corpus/knowledge/fleet-kill-rate-ledger.md',439,441)
    excerpt('last-touch discriminator',rev,'.ufo/evidence/round-56/deciding-run.sh',94,102)
excerpt('new Gate',C0,'corpus/lessons/round-58.md',28,60)
excerpt('handoff claim',C0,'corpus/lessons/round-58.md',86,92)
excerpt('current Planned',C0,'SCORECARD.md',2823,2841)
excerpt('staged handoff not canonical filing',C0,'.ufo/waves/round-58/w1/T58W1Fix08/stage/kagi-crossdomain-r51.5.md',1,15)
files=git('ls-tree','-r','--name-only',C0).stdout.splitlines()
snippets.append({'label':'tracked report paths','command':commands[-1]['command'],'exit':0,'output':'\n'.join(p for p in files if p.startswith('.ufo/reports/') or ('report' in p.lower() and 'round-58' in p))})
# Verify fresh reader follow-on really precedes BASE, rather than trusting the assessment.
p=git('merge-base','--is-ancestor','7fa9a5e0104bc181872401547987d6744f3b570d',BASE)
snippets.append({'label':'R51.2 later re-key ancestry','command':commands[-1]['command'],'exit':p.returncode,'output':'exit='+str(p.returncode)})
ledger=json.loads(blob(BASE,'.ufo/evidence/round-21/coldread/ledger.json'))
def walk(obj):
    if isinstance(obj,dict):
        if any('T54W2Read' in str(v) for k,v in obj.items() if k in ('seats','reader')) and obj.get('heading') in ('## Mutation-sweep recipe — numbered steps; bounded cold-read evidence','### Using the ledger','### Round-26 gate/probe registry — report interop'):
            snippets.append({'label':'base fresh reader rekey','command':['git','-C',CLONE,'show',BASE+':.ufo/evidence/round-21/coldread/ledger.json'],'exit':0,'output':json.dumps(obj,ensure_ascii=False)})
        for v in obj.values(): walk(v)
    elif isinstance(obj,list):
        for v in obj: walk(v)
walk(ledger)
ROOT.joinpath('audit-results.json').write_text(json.dumps({'rows':results,'snippets':snippets},indent=2))
ROOT.joinpath('commands.json').write_text(json.dumps(commands,indent=2))
for r in results:
    print(r['id'], 'structural='+str(r['structural_fault']), 'base='+r['row']['status_at_base'], 'now='+r['row']['status'], 'planned='+str(r['planned_current']))
for s in snippets:
    if s['label'] in ('round51 correction','handoff claim','new Gate','tracked report paths','R51.2 later re-key ancestry'):
        print('\n'+s['label']+' '+str(s['command'])+'\n'+s['output'])
