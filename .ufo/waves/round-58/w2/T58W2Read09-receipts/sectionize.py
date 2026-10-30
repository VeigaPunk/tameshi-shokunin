import importlib.util
import subprocess
lane = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
spec = importlib.util.spec_from_file_location('frozen', lane + '/.ufo/evidence/round-18/measure.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
raw = subprocess.check_output(['git', '-C', lane, 'show', '8063d0a551fc5b3cb5a2d397da7353af53444534:SKILL.md'])
for sec in m.sectionize(raw):
    if sec['heading'] == '### Round-26 gate/probe registry — report interop':
        print(sec['start'], sec['end'], sec['sha256'])
