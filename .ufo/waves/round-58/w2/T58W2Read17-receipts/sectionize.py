import importlib.util, subprocess
p='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
s=importlib.util.spec_from_file_location('frozen', p+'/.ufo/evidence/round-18/measure.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
raw=subprocess.check_output(['git','-C',p,'show','8063d0a551fc5b3cb5a2d397da7353af53444534:SKILL.md'])
for sec in m.sectionize(raw):
 if sec['heading']=='### Round-21 gate/probe registry — finite environment differential':
  print(sec['start'],sec['end'],sec['sha256'])
