import sys, json, subprocess, importlib.util, os, copy
sys.dont_write_bytecode = True
S = '/fast/scratch/hyaku/tameshi-r57/T57W1CritC1'
CLONE = S + '/clone'
B = '5e3569969b532310d2b8a3d130901757a3df356b'
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
M = load('m50', S + '/m50.py'); MR = load('m50r5', S + '/m50r5.py')
D = json.load(open(S + '/defects57.json'))['defects']
for d in D:
    if not d['keys']: d['keys'] = [d['id']]   # lane-curated key stands in for the five empty-key items
def g(*a, inp=None):
    return subprocess.run(['git', '-C', CLONE] + list(a), capture_output=True, check=True, input=inp).stdout
def commit_all(msg):
    g('add', '-A'); g('-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-q', '--allow-empty', '-m', msg)
    return g('rev-parse', 'HEAD').decode().strip()
def reset():
    g('checkout', '-q', '--detach', B); g('clean', '-qfd')
