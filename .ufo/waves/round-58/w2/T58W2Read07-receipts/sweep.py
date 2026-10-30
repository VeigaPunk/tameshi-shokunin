import importlib.util, json, pathlib, re, subprocess, sys
lane = pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
root = pathlib.Path(sys.argv[1])
cand = '8063d0a551fc5b3cb5a2d397da7353af53444534'
heading = '### The map — where a reader enters, artifact by artifact'
spec = importlib.util.spec_from_file_location('frozen', lane / '.ufo/evidence/round-18/measure.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
raw = subprocess.check_output(['git', '-C', str(lane), 'show', cand + ':SKILL.md'])
sec = next(s for s in m.sectionize(raw) if s['heading'] == heading)
print('SECTION', sec['start'], sec['end'], sec['sha256'])
text = '\n'.join(raw.decode().splitlines()[sec['start']-1:sec['end']])
print(text)
print('AXES: factual accuracy; pointer resolution; executable command coverage; calibration')
for path in ['corpus/knowledge/operator-runbook.md', 'corpus/knowledge/fleet-kill-rate-ledger.md', 'corpus/knowledge/service-limits.md', 'corpus/knowledge/service-optin-protocol.md', 'corpus/knowledge/fleet-suite-census.md', 'corpus/knowledge/service-standing-state.md', 'tools/mutate-and-run.sh', 'corpus/README.md', 'plans/round-11.plan.md', 'plans/completion-evidence.md', 'corpus/knowledge/closeout-r11.md', 'LOG.md', 'SCORECARD.md']:
    print('PATH', path, 'exists=' + str((root / path).is_file()))
for path, pattern in [('corpus/knowledge/operator-runbook.md', r'^## (?:0|2|3|4|5|6|7|10)\.'), ('corpus/knowledge/service-optin-protocol.md', r'^## [1-4]\.'), ('corpus/knowledge/service-standing-state.md', r'^## |SC[123]'), ('corpus/knowledge/fleet-suite-census.md', r'^## .*offer|^## .*queue'), ('corpus/knowledge/fleet-kill-rate-ledger.md', r'^\| [1-6] |^\|.*(?:round-gate|sources-check).*\|')]:
    for i, line in enumerate((root / path).read_text().splitlines(), 1):
        if re.search(pattern, line): print(path + ':' + str(i), line)
for path, ranges in [('tools/mutate-and-run.sh', [(88,97),(149,150)]), ('corpus/README.md', [(125,125),(326,326),(614,614)]), ('corpus/knowledge/operator-runbook.md', [(349,351)]), ('corpus/knowledge/fleet-kill-rate-ledger.md', [(439,441)]), ('LOG.md', [(316,317)])]:
    lines = (root/path).read_text().splitlines()
    for a,b in ranges:
        for i in range(a,b+1): print(path + ':' + str(i),lines[i-1])
print('MUTATION_CASE_NOTES', len(list((root/'corpus/knowledge').glob('mutation-case-*.md'))))
print('PLANS', sorted(p.name for p in (root/'plans').iterdir()))
print('ROUND11_RECORD_FILES', sorted(p.name for p in (root/'plans').glob('round-11*record*')))
print('LIMITS_HEADING', "### The service's limits — what tameshi refuses to mutation-test" in raw.decode())
print('POINTER_NOT_SECOND_HOME', 'Pointer, not a second home.' in raw.decode())
print('BASE_TO_C0_SKILL_DIFF_BYTES', len(subprocess.check_output(['git','-C',str(lane),'diff','2a32aa8228d5f86a85c81a923a3148bf792a9538',cand,'--','SKILL.md'])))
