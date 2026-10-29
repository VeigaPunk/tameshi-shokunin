import subprocess, re, sys, json
LANE='.'
B='5e3569969b532310d2b8a3d130901757a3df356b'; R='650987a0d6fc285b37f0f9e63a3aae864af9cd5a'
def g(*a): return subprocess.run(['git','-C',LANE]+list(a),capture_output=True).stdout.decode('utf-8','replace')
keys={'R54.6':['T54W2Sent03','c1committed-positive.stdout','rejection-attribution.txt','clean-tree-after.txt'],
      'R54.7':['forged-reader.json','T54W2Sent01','7fa9a5e','R100','section_sha256']}
commits=g('rev-list','--reverse',f'{R}..{B}').split()
print('commits after routed_at up to base:',len(commits))
for rid,ks in keys.items():
    print('==',rid)
    for c in commits:
        msg=g('log','-1','--format=%B',c)
        names=re.search(r'(?<![\w.])'+re.escape(rid)+r'(?!\d)',msg) is not None
        diff=g('show','--format=','-U0',c)
        path=None
        for line in diff.split('\n'):
            if line.startswith('+++ '):
                path=line[6:] if line.startswith('+++ b/') else None
            elif line.startswith('+') and path:
                for k in ks:
                    if re.search(r'(?<![\w-])'+re.escape(k)+r'(?![\w-])',line[1:],re.I) or path.endswith('/'+k) or path==k:
                        print(f'  {c[:7]} names_id={names} path={path} key={k} :: {line[1:][:200]}')
                        break
