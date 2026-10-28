import json, subprocess, sys
LANE=sys.argv[1]; C0=sys.argv[2]; PIN=sys.argv[3]
E='.ufo/evidence/round-55'
DROP={'LOG.md','SCORECARD.md','SKILL.md','.ufo/evidence/round-21/coldread/ledger.json'}
H=sorted(set(json.load(open(f'{LANE}/{E}/c1/lost-headings-at-c0.json'))))
led=json.load(open(f'{LANE}/.ufo/evidence/round-21/coldread/ledger.json'))['entries']
def git(*a):
    return subprocess.run(['git','-C',LANE]+list(a),capture_output=True)
def blob(rev,p):
    r=git('rev-parse','--verify',f'{rev}:{p}')
    return r.stdout.decode().strip() if r.returncode==0 else None
print('heading\tunion\tdropped_missing_at_pin\tchanged_c0_to_pin')
for h in H:
    u={p for e in led if e.get('heading')==h for p in (e.get('inputs') or {}) if p not in DROP}
    missing=[p for p in u if blob(PIN,p) is None]
    changed=[p for p in u if blob(C0,p) and blob(PIN,p) and blob(C0,p)!=blob(PIN,p)]
    print('%s\t%d\t%d\t%d' % (h,len(u),len(missing),len(changed)))
    for p in changed[:4]:
        print('   CHANGED %s  %s -> %s' % (p, blob(C0,p)[:12], blob(PIN,p)[:12]))
