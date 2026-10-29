import importlib.util, json, os, subprocess, sys, hashlib
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
REFERENT = '877eedee3ddb7fe25d7a6a09922b04ba13e5a99b'
spec = importlib.util.spec_from_file_location('m50', LANE + '/.ufo/evidence/round-50/c1/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def git(*a):
    return subprocess.run(['git', '-C', LANE] + list(a), capture_output=True).stdout

spotchecks = {}
for line in git('ls-tree', '-r', '--name-only', BASE, '--', 'corpus/lessons').decode().split('\n'):
    if line.endswith('verifier-spotcheck.md'):
        spotchecks[line] = None
ledger21 = git('show', BASE + ':.ufo/evidence/round-21/coldread/ledger.json').decode()
ledger21_lines = ledger21.split('\n')
sk = git('show', BASE + ':SKILL.md').decode().split('\n')
ent = json.loads(ledger21)['entries']

def sha_at(rev, path):
    b = git('show', rev + ':' + path)
    return hashlib.sha256(b).hexdigest()

lab_sources = ('"tameshi@c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/SOURCES.md": "%s"' % ent[591]['external_inputs']['tameshi@c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/SOURCES.md'])
lab_quality = ('"tameshi@c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/QUALITY.md": "%s"' % ent[593]['external_inputs']['tameshi@c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/QUALITY.md'])
ln_sources = [i + 1 for i, l in enumerate(ledger21_lines) if lab_sources in l][0]
ln_quality = [i + 1 for i, l in enumerate(ledger21_lines) if lab_quality in l][0]
gate = git('show', BASE + ':tools/receipt-revision-gate.py').decode().split('\n')
kn = git('show', BASE + ':corpus/knowledge/receipt-revision-binding.md').decode().split('\n')
reg = git('show', BASE + ':tools/registry.json').decode().split('\n')
rd = git('show', BASE + ':corpus/README.md').decode().split('\n')
qu = git('show', BASE + ':corpus/QUALITY.md').decode().split('\n')

def find(lines, needle):
    hits = [i + 1 for i, l in enumerate(lines) if needle in l]
    assert hits, needle
    return hits[0]

# Each evidence: (path, a, b, excerpt). Excerpt is the exact substring located by needle search.
E = {}
E['R56.1'] = dict(keys=['SKILL.md:', 'bare line anchor', 'page-local'], evidence=[
    ('SKILL.md', 491, 491, 'Band interiors were unprobed at round 3 (both at 80 %, SKILL.md:335-339)'),
    ('SKILL.md', 335, 339, 'Shared survivor classes across the two cases, named'),
    ('corpus/README.md', 100, 100, '`SKILL.md:14-15` and `:133-135` still call full-sweep/bash'),
    ('corpus/QUALITY.md', 253, 253, 'A bare line anchor into such a file expires with the next'),
])
E['R56.2'] = dict(keys=['RECEIPT_REV_MISMATCH', 'RECEIPT_REV_CONTENT_DRIFT', '--paths'], evidence=[
    ('SKILL.md', 53, 53, 'a verdict receipt names another revision | refused unless its bytes equal the certified revision on the declared `--paths` surface | `RECEIPT_REV_MISMATCH`'),
    ('tools/receipt-revision-gate.py', 145, 146, "if paths is None: codes.append('RECEIPT_REV_MISMATCH')"),
    ('tools/receipt-revision-gate.py', 148, 151, "else: drift = drifted_paths(lane, full, certified, paths) if drift: codes.append('RECEIPT_REV_CONTENT_DRIFT')"),
])
E['R56.3'] = dict(keys=['14/14', 'recheck:', '19/19'], evidence=[
    ('corpus/knowledge/receipt-revision-binding.md', 3, 3, '`python3 tools/receipt-revision-gate.py --selftest` must print `GATE_SELFTEST: 14/14 pass`'),
    ('corpus/knowledge/receipt-revision-binding.md', 224, 225, "The frontmatter `recheck:` and §Falsifier item 3 still name the original freeze's"),
    ('tools/registry.json', find(reg, 'GATE_SELFTEST: 19/19 pass'), find(reg, 'GATE_SELFTEST: 19/19 pass'), 'GATE_SELFTEST: 19/19 pass'),
])
E['R56.4'] = dict(keys=['tameshi@c0137451', 'corpus/SOURCES.md', 'corpus/QUALITY.md', 'external_inputs'], evidence=[
    ('.ufo/evidence/round-21/coldread/ledger.json', ln_sources, ln_sources, lab_sources),
    ('.ufo/evidence/round-21/coldread/ledger.json', ln_quality, ln_quality, lab_quality),
])

fileset = {}
def lines_of(path):
    if path not in fileset:
        fileset[path] = git('show', BASE + ':' + path).decode('utf-8', 'replace').split('\n')
    return fileset[path]

cache = {}
results = {}
ok_all = True
for rid, spec_ in E.items():
    items = []
    for path, a, b, exc in spec_['evidence']:
        item = {'path': path, 'lines': '%d-%d' % (a, b), 'excerpt': exc}
        why = m.check_evidence(LANE, BASE, item, spec_['keys'], spotchecks, cache)
        keyed = m.has_key(item, spec_['keys'])
        # confirm the excerpt occurs at the cited lines of the base blob (independent of resolver)
        seg = m.norm('\n'.join(lines_of(path)[a - 1:b]))
        direct = m.norm(exc) in seg
        ok = why is None and direct
        ok_all = ok_all and ok
        items.append({'path': path, 'lines': item['lines'], 'excerpt': exc, 'resolver': why or 'ok', 'direct': direct, 'keyed': keyed})
    results[rid] = items
    print(rid, [(i['path'], i['lines'], i['resolver'], i['direct'], i['keyed']) for i in items])
print('ALL_EXCERPTS_OK', ok_all)
json.dump({'base': BASE, 'referent': REFERENT, 'ledger_lines': {'sources': ln_sources, 'quality': ln_quality},
           'evidence': results, 'keys': {k: v['keys'] for k, v in E.items()}}, open(os.path.join(os.environ['S'], 'verify.json'), 'w'), indent=1, ensure_ascii=False)
