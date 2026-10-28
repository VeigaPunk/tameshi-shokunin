import hashlib, importlib.util, json, os, shutil, subprocess, sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
C0 = '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
S = Path(os.environ['S'])
spec = importlib.util.spec_from_file_location('r18', LANE / '.ufo/evidence/round-18/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1')

def git(repo, *a):
    return subprocess.run(['git', '-C', str(repo), *a], env=ENV, capture_output=True, check=True)

def new_repo(name, skill_text):
    repo = S / name
    if repo.exists(): shutil.rmtree(repo)
    repo.mkdir(parents=True)
    git(repo, 'init', '-q', '-b', 'master')
    assert git(repo, 'rev-parse', '--show-toplevel').stdout.decode().strip() == str(repo), repo
    git(repo, 'config', 'user.name', 't'); git(repo, 'config', 'user.email', 't@t.invalid')
    put(repo, 'tools/mutate-and-run.sh', m.RUNNER_TEXT)
    put(repo, 'SHONEN.md', m.SHONEN_TEXT.replace(m.DEFAULT_LEDGER_PATH, m.DEFAULT_LEDGER_PATH))
    put(repo, 'SKILL.md', skill_text)
    put(repo, 'corpus/SOURCES.md', m.SOURCES_TEXT)
    put(repo, m.INPUT_FILE, m.INPUT_V1)
    put(repo, m.TRACE_PATH, m.trace_receipt({m.INPUT_FILE: m.INPUT_V1_SHA}))
    git(repo, 'add', '-A'); git(repo, 'commit', '-qm', 'fixture'); 
    return repo

def put(repo, rel, text):
    p = repo / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding='utf-8')

def entry_for(text, start=1, end=None, heading='', **over):
    input_sha = m.INPUT_V1_SHA
    e = {'skill_sha256': 'deadbeef', 'start': start,
         'end': end if end is not None else start + text.count('\n'),
         'heading': heading, 'sha256': hashlib.sha256(text.encode()).hexdigest(),
         'class': 'instruction', 'verdict': 'executed-ok', 'blocking_gaps': 0,
         'wrong_expectations': 0, 'commands_executed_count': 1, 'read_rev': 'f' * 40,
         'inputs': {m.INPUT_FILE: input_sha}, 'traces': [m.TRACE_PATH]}
    e.update(over); return e

def run_measure(repo, rev):
    r = subprocess.run([sys.executable, str(LANE / '.ufo/evidence/round-18/measure.py'),
                        '--rev', rev, '--repo', str(repo)], env=ENV, capture_output=True, text=True)
    if r.returncode != 0:
        return {'_rc': r.returncode, '_stderr': r.stderr[-2000:]}
    out = json.loads(r.stdout)
    return {'covered': out['coldread']['sections_covered'], 'total': out['coldread']['sections_total'],
            'sections': [(s['start'], s['heading'], s['credited']) for s in out['coldread']['sections']],
            'reasons': out['coldread']['reasons']}

results = {}
skill = '\n'.join(m.SKILL_LINES) + '\n'
secs = {s['heading']: s for s in m.sectionize(skill.encode())}
texts = {h: m._strip_tail(list(m.SKILL_LINES[s['start']-1:s['end']]))
         for h, s in secs.items() if s['heading']}

# A: baseline 4 entries / 4 sections
repo = new_repo('A', skill)
ent = [entry_for(texts[h], secs[h]['start'], secs[h]['end'], h) for h in texts]
put(repo, m.DEFAULT_LEDGER_PATH, json.dumps({'schema': 'tameshi-coldread-ledger-v2', 'entries': ent}))
git(repo, 'add', '-A'); git(repo, 'commit', '-qm', 'ledger'); rev = git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()
results['A_4_entries_4_sections'] = run_measure(repo, rev)

# B: same but Beta entry carries a bogus start/end
ent_b = [dict(e) for e in ent]
for e in ent_b:
    if e['heading'] == '## Beta':
        e['start'], e['end'] = 500, 501
put(repo, m.DEFAULT_LEDGER_PATH, json.dumps({'schema': 'tameshi-coldread-ledger-v2', 'entries': ent_b}))
git(repo, 'add', '-A'); git(repo, 'commit', '-qm', 'bogus start'); rev_b = git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()
results['B_bogus_start_still_credits'] = run_measure(repo, rev_b)

# C: only the Beta entry remains
put(repo, m.DEFAULT_LEDGER_PATH, json.dumps({'schema': 'tameshi-coldread-ledger-v2',
    'entries': [e for e in ent if e['heading'] == '## Beta']}))
git(repo, 'add', '-A'); git(repo, 'commit', '-qm', 'one entry'); rev_c = git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()
results['C_one_entry_one_section'] = run_measure(repo, rev_c)

# D: entry sha256 is a list of two digests
put(repo, m.DEFAULT_LEDGER_PATH, json.dumps({'schema': 'tameshi-coldread-ledger-v2',
    'entries': [dict(ent[1], sha256=[ent[1]['sha256'], ent[2]['sha256']])]}))
git(repo, 'add', '-A'); git(repo, 'commit', '-qm', 'list sha'); rev_d = git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()
results['D_list_sha'] = run_measure(repo, rev_d)

# E: two byte-identical sections, one entry
twin = '## Twin\n\nbody'
skill2 = twin + '\n\n' + twin + '\n'
repo2 = new_repo('E', skill2)
secs2 = m.sectionize(skill2.encode())
results['E_section_shas'] = [(s['start'], s['heading'], s['sha256'][:12]) for s in secs2]
put(repo2, m.DEFAULT_LEDGER_PATH, json.dumps({'schema': 'tameshi-coldread-ledger-v2',
    'entries': [entry_for(twin, 3, 5, '## Twin')]}))
git(repo2, 'add', '-A'); git(repo2, 'commit', '-qm', 'twin ledger'); rev_e = git(repo2, 'rev-parse', 'HEAD').stdout.decode().strip()
results['E_one_entry_two_identical_sections'] = run_measure(repo2, rev_e)

print(json.dumps(results, indent=1))
