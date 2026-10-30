import hashlib, json, pathlib, re, subprocess
p=pathlib.Path('/fast/scratch/hyaku/tameshi-r58/T58W2Read10/clone')
paths=['corpus/knowledge/incremental-pin-disposition.md','corpus/lessons/round-12-verifier-spotcheck.md','.ufo/evidence/round-13/pin-manifest.json','.ufo/evidence/round-13/witness-metadata.json','tools/pin-disposition.py','tools/witness-metadata.py']
for name in paths:
 assert (p/name).is_file(), name
 print('pointer exists:',name)
sources=(p/'corpus/SOURCES.md').read_text()
for ident in ['S003','S041','S047','S048']:
 print(next(line for line in sources.splitlines() if line.startswith('| '+ident+' |')))
for rel in ['.ufo/evidence/round-12/BashWitness/summary.json','.ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json']:
 value=json.loads((p/rel).read_text()); assert value['declaration']['kind'] is None
 print('historical null preserved:',rel)
d=json.loads((p/'.ufo/evidence/round-12/BashWitness/declaration.json').read_text()); print('explicit top-level kind:',d['kind']); assert d['kind']=='declared-witness mapping (not a blind preregistration)'
producer=(p/'tools/bash-witness-study.py').read_text().splitlines()
for start,end in [(809,818),(1693,1701)]:
 print('\n'.join(f'{i+1}: {producer[i]}' for i in range(start-1,end)))
probe=(p/'tools/pin-disposition.py').read_text().splitlines()
print('\n'.join(f'{i+1}: {probe[i]}' for i in range(558-1,579)))
print('Recipe does not invoke a sibling gate; probe target reads are read-only git plumbing and file hashing (static inspection).')
