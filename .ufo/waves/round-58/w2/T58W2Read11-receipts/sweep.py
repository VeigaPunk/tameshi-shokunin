import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, pathlib, subprocess
lane = pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
clone = pathlib.Path('/fast/scratch/hyaku/tameshi-r58/T58W2Read11/clone')
rev = '8063d0a551fc5b3cb5a2d397da7353af53444534'
spec = importlib.util.spec_from_file_location('frozen', lane / '.ufo/evidence/round-18/measure.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
raw = subprocess.check_output(['git', '-C', str(lane), 'show', rev + ':SKILL.md'])
sec = next(s for s in m.sectionize(raw) if s['heading'] == '### Round-13 gate/probe registry')
print(sec['start'], sec['end'], sec['sha256'])
assert (clone / 'SKILL.md').read_bytes() == raw
for p in ['tools/pin-disposition.py', 'tools/witness-metadata.py', '.ufo/evidence/round-13/pin-manifest.json', '.ufo/evidence/round-13/witness-metadata.json', '.ufo/evidence/round-12/BashWitness/summary.json', '.ufo/evidence/round-12/BashWitness/declaration.json', '.ufo/evidence/round-12/BashWitness/declared.tsv', '.ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json']:
    data = (clone / p).read_bytes()
    print('RESOLVED', p, hashlib.sha256(data).hexdigest())
text = raw.decode()
assert '## Seventh recorded case and full-page cold-read — round 16' in text
print('RESOLVED seventh-case heading')
source = (clone / 'corpus/SOURCES.md').read_text()
for ident in ['S047', 'S048', 'S266']:
    print(next(line for line in source.splitlines() if line.startswith('| ' + ident + ' |')))
summary = json.loads((clone / '.ufo/evidence/round-12/BashWitness/summary.json').read_text())
producer = hashlib.sha256((clone / 'tools/bash-witness-study.py').read_bytes()).hexdigest()
print('HISTORICAL_PRODUCER', json.dumps(summary['tool'], sort_keys=True))
print('CURRENT_PRODUCER_SHA256', producer)
print('EXPECTED_JSON_REFERENCES_IN_GATE', (clone / 'tools/witness-metadata.py').read_text().count('expected.json'))
diff = subprocess.check_output(['git', '-C', str(clone), 'diff', '2a32aa8228d5f86a85c81a923a3148bf792a9538', rev, '--', 'SKILL.md', 'tools/pin-disposition.py', 'tools/witness-metadata.py'])
print('SCOPED_DIFF_BYTES', len(diff))
print('SCOPE_SWEEP_COMPLETE')
