import hashlib, importlib.util, json, pathlib, re, subprocess
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
CLONE = '/fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone'
REV = 'adf87899c70d616140a81185a8f9acbbdfb30392'
spec = importlib.util.spec_from_file_location('frozen', LANE + '/.ufo/evidence/round-18/measure.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
raw = subprocess.check_output(['git', '-C', LANE, 'show', REV + ':SKILL.md'])
sec = next(s for s in m.sectionize(raw) if s['heading'] == '## Standing rules')
print('SECTION', sec['start'], sec['end'], sec['sha256'])
print('CLONE_REV', subprocess.check_output(['git', '-C', CLONE, 'rev-parse', 'HEAD'], text=True).strip())
root = pathlib.Path(CLONE)
for p in ('PROVINCE.md', 'tools/receipt-revision-gate.py', 'tools/registry.json', 'corpus/knowledge/scratch-root-contract.md', 'corpus/knowledge/mutation-case-kimi-census.md', 'corpus/knowledge/mutation-case-kagi-census.md', '.ufo/evidence/round-55/c2/measure.py', '.ufo/evidence/round-56/c2/measure.py'):
    data = (root / p).read_bytes()
    print('POINTER', p, 'exists', hashlib.sha256(data).hexdigest())
text = raw.decode()
print('ERRATA_HEADING', '## Errata — round 16 full-page cold-read' in text)
print('ERRATA_DISCLOSURE', "The page edits are in-place repairs, and so are this table's own cells" in text)
source = (root / 'corpus/SOURCES.md').read_text()
print('S278', next(l for l in source.splitlines() if l.startswith('| S278 |')))
print('S279', next(l for l in source.splitlines() if l.startswith('| S279 |')))
rows = json.loads((root / 'tools/registry.json').read_text())['rows']
seven = ('repeat-control-selftest', 'bash-witness-selftest', 'pin-disposition-selftest', 'evidence-disposition-selftest', 'context-capture-selftest', 'registry-check-selftest', 'env-diff-selftest')
print('SEVEN_CELLS', sum(bool(r.get('scratch_root')) for r in rows if r['name'] in seven), '/7')
files = subprocess.check_output(['git', '-C', CLONE, 'ls-tree', '-r', '--name-only', REV, '--', '.ufo/waves'], text=True).splitlines()
dash = slash = 0
sampled = 0
for p in files:
    if not re.match(r'^\.ufo/waves/round-(48|49|50|51|52)/w[12]/', p):
        continue
    data = (root / p).read_text(errors='replace')
    sampled += 1
    dash += len(re.findall(r'/tameshi-r(?:48|49|50|51|52)-[A-Za-z0-9]', data))
    slash += len(re.findall(r'/tameshi-r(?:48|49|50|51|52)/[A-Za-z0-9]', data))
print('SCRATCH_OCCURRENCES', 'files=', sampled, 'dash=', dash, 'slash=', slash)
