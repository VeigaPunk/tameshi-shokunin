#!/usr/bin/env python3
"""T57W1SentLedger forgery probe. Scratch only: writes commits to the scratch clone, never the lane.

Loads the round-50 counter's measure() from the base (unchanged bytes) and scores forged ledger rows
per item id via the explain() notes. Also measures candidate extra checks on the real fixed rows.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

S = os.environ['S']
CL = os.path.join(S, 'clone')
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
ROUND_BASE = 'e3729de862f73ae080d98fcf522a7081ce16e40a'
ENV = dict(os.environ, GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
           GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')


def G(*a):
    p = subprocess.run(['git', '-C', CL] + list(a), capture_output=True, env=ENV)
    if p.returncode != 0:
        raise SystemExit('git %s: %s' % (' '.join(a), p.stderr.decode('utf-8', 'replace')))
    return p.stdout.decode('utf-8', 'replace')


assert os.path.realpath(G('rev-parse', '--show-toplevel').strip()) == os.path.realpath(CL), 'toplevel'
MOD = os.path.join(S, 'measure50.py')
with open(MOD, 'wb') as fh:
    fh.write(subprocess.run(['git', '-C', CL, 'show', BASE + ':.ufo/evidence/round-50/c1/measure.py'],
                            capture_output=True, check=True).stdout)
spec = importlib.util.spec_from_file_location('measure50', MOD)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

DEF_LIST = json.loads(m.show(CL, BASE, '.ufo/evidence/round-50/c1/defects.json').decode())['defects']
DEF = {d['id']: d for d in DEF_LIST}
ALL = [d['id'] for d in DEF_LIST]
SPOT = {d['file']: d['file_sha256'] for d in DEF_LIST}
REAL = json.loads(m.show(CL, BASE, 'corpus/routed-defects.json').decode())
REAL_ROWS = {r['id']: r for r in REAL['defects']}
STOP = set('that this with from have been were will into only when than also they them their there which '
           'about would could should does doing each being after before under over across other where while '
           'since until both very more most such some'.split())


def toks(s):
    return {t for t in re.findall(r'[a-z][a-z0-9_]{3,}', s.lower()) if t not in STOP}


def append_commit(path, text, msg):
    full = os.path.join(CL, path)
    n = open(full, encoding='utf-8').read().count('\n')
    with open(full, 'a', encoding='utf-8') as fh:
        fh.write(text)
    G('add', '--', path)
    G('commit', '-q', '-m', msg)
    return G('rev-parse', 'HEAD').strip(), n + 1


# ---- forged content chain on top of BASE (appends only; no lane file is touched) ----
G('checkout', '-q', '--detach', BASE)
EXC_T1 = 'Index note: the line-scoped digest was regenerated for the week; no criterion changed.'
EXC_T2 = 'SHADOW_NOTE = "anchor digest rebuilt nightly"'
EXC_T3 = '# pbt-staged-id.py: header comment reflowed; behaviour unchanged'
EXC_T4 = '- [~] box five: unchanged this round, operator-owned'
K1, L1 = append_commit('corpus/QUALITY.md', EXC_T1 + '\n', 'chore: regenerate QUALITY index note')
K2, L2 = append_commit('tools/staged-id-guard.py', EXC_T2 + '\n', 'chore: staged-id guard header')
K3, L3 = append_commit('tools/pbt-staged-id.py', EXC_T3 + '\n', 'tidy: pbt-staged-id header')
K4, L4 = append_commit('SHONEN.md', EXC_T4 + '\n', 'docs: SHONEN box note')
REV_F = K4
planned = '\n**Planned (round 51):** ' + ' '.join(ALL) + '\n'
K5, _ = append_commit('SCORECARD.md', planned, 'docs: scorecard planned list')
REV_O = K5


# ---- probe: write a ledger at a commit on top of rev, run inherited measure(), return per-id notes ----
def probe(rev, overrides, label):
    rows = [overrides.get(i, REAL_ROWS[i]) for i in ALL]
    doc = dict(REAL)
    doc['defects'] = rows
    G('checkout', '-q', '--detach', rev)
    with open(os.path.join(CL, 'corpus/routed-defects.json'), 'w', encoding='utf-8') as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
    G('add', '--', 'corpus/routed-defects.json')
    G('commit', '-q', '--allow-empty', '-m', 'ledger probe: ' + label)
    head = G('rev-parse', 'HEAD').strip()
    notes = []
    _, counts, stat, total, _ = m.measure(CL, head, DEF_LIST, True,
                                         explain=lambda *a: notes.append(a))
    return counts, stat, total, notes


def row_verdict(rid, rev, row, label):
    counts, stat, total, notes = probe(rev, {rid: row}, label)
    fails = [a for a in notes if len(a) > 1 and a[1] == rid]
    return {'id': rid, 'pass': not fails, 'notes': [list(map(str, a)) for a in fails],
            'total_all_rows': total, 'counts_nonzero': {k: v for k, v in counts.items() if v}}


# ---- fresh-evidence logic (mirror of round-50 fixed branch), evidence read at ev_rev ----
def fresh_items(rid, row, ev_rev):
    d = DEF[rid]
    files = m.touched(CL, row['commit'])
    out = []
    for item in row['evidence']:
        if not isinstance(item, dict) or not m.has_key(item, d['keys']):
            continue
        if item.get('path') not in files:
            continue
        then = m.show(CL, d['routed_at'], item['path'])
        if then is not None and m.norm(item['excerpt']) in m.norm(then.decode('utf-8', 'replace')):
            continue
        a, b = (int(x) for x in item['lines'].split('-'))
        text = m.show(CL, ev_rev, item['path']).decode('utf-8', 'replace').split('\n')
        span = ' '.join(text[a - 1:b]).lower()
        if any(w in span for w in m.ACK_WORDS):
            continue
        out.append(item)
    return out


CODE_EXT = ('.py', '.sh', '.js', '.ts', '.rb', '.yaml', '.toml')


def X1_overlap(rid, fresh):
    """keyed fresh excerpt shares >= 3 content words with the item text"""
    return any(len(toks(i['excerpt']) & toks(DEF[rid]['text'])) >= 3 for i in fresh)


def X2_message(rid, row):
    """fixed commit message names the item id or one of its keys"""
    msg = G('log', '-1', '--format=%B', row['commit']).lower()
    return rid.lower() in msg or any(k.lower() in msg for k in DEF[rid]['keys'])


def X2d_diff_added(rid, row, fresh):
    """diff of the commit (added lines) mentions a key (vacuous if the excerpt itself is an added keyed line)"""
    for p in {i['path'] for i in fresh}:
        diff = G('show', '--format=', '-U0', row['commit'], '--', p)
        for ln in diff.split('\n'):
            if ln.startswith('+') and not ln.startswith('+++') and any(k.lower() in ln.lower() for k in DEF[rid]['keys']):
                return True
    return False


def X3_removal(rid, row, fresh):
    """fixed commit removes at least one line (in an evidence path) that carries a key"""
    for p in {i['path'] for i in fresh}:
        diff = G('show', '--format=', '-U0', row['commit'], '--', p)
        for ln in diff.split('\n'):
            if ln.startswith('-') and not ln.startswith('---') and any(k.lower() in ln.lower() for k in DEF[rid]['keys']):
                return True
    return False


def X4_not_comment(rid, fresh):
    """some fresh excerpt is not a comment-only line in a code file"""
    for i in fresh:
        ex = m.norm(i['excerpt'])
        if i['path'].endswith(CODE_EXT) and ex.startswith(('#', '//', '--', ';', '<!--')):
            continue
        return True
    return False


def X5_open_defect_unchanged(rid, row, ev_rev):
    """open row: some evidence excerpt is already present at routed_at (defect text unchanged since routing)"""
    d = DEF[rid]
    for item in row['evidence']:
        then = m.show(CL, d['routed_at'], item['path'])
        if then is not None and m.norm(item['excerpt']) in m.norm(then.decode('utf-8', 'replace')):
            return True
    return False


def evidence_resolves(rid, row, rev):
    cache = {}
    return all(m.check_evidence(CL, rev, it, DEF[rid]['keys'], SPOT, cache) is None for it in row['evidence'])


def find_substitute(rid, rev):
    cache = {}
    for key in DEF[rid]['keys']:
        out = subprocess.run(['git', '-C', CL, 'grep', '-n', '-i', '-F', '-e', key, rev], capture_output=True,
                             env=ENV).stdout.decode('utf-8', 'replace')
        for line in out.split('\n'):
            parts = line.split(':', 3)
            if len(parts) < 4:
                continue
            _, path, num, text = parts
            if not num.isdigit():
                continue
            item = {'path': path, 'lines': '%s-%s' % (num, num), 'excerpt': text.strip()}
            if m.has_key(item, DEF[rid]['keys']) and m.check_evidence(CL, rev, item, DEF[rid]['keys'], SPOT, cache) is None:
                return [item]
    return None


out = {'rev_forge': REV_F, 'rev_open': REV_O, 'commits': {'K1': K1, 'K2': K2, 'K3': K3, 'K4': K4, 'K5': K5},
       'lines': {'K1': L1, 'K2': L2, 'K3': L3, 'K4': L4}}

# ---- forgery rows: fixed with off-topic / comment / restating excerpts ----
forg = {
    'F1_R41.1_offtopic_prose_line': ('R41.1', {'id': 'R41.1', 'status': 'fixed', 'commit': K1,
                                              'evidence': [{'path': 'corpus/QUALITY.md', 'lines': '%d-%d' % (L1, L1), 'excerpt': EXC_T1}]}),
    'F2_R43.3_offtopic_code_line': ('R43.3', {'id': 'R43.3', 'status': 'fixed', 'commit': K2,
                                             'evidence': [{'path': 'tools/staged-id-guard.py', 'lines': '%d-%d' % (L2, L2), 'excerpt': EXC_T2}]}),
    'F3_R49.1_comment_line': ('R49.1', {'id': 'R49.1', 'status': 'fixed', 'commit': K3,
                                       'evidence': [{'path': 'tools/pbt-staged-id.py', 'lines': '%d-%d' % (L3, L3), 'excerpt': EXC_T3}]}),
}
for rid in ('R46.5', 'R47.7', 'R48.6', 'R49.6'):
    forg['F4_%s_SHONEN_restates_defect' % rid] = (rid, {'id': rid, 'status': 'fixed', 'commit': K4,
                                                         'evidence': [{'path': 'SHONEN.md', 'lines': '%d-%d' % (L4, L4), 'excerpt': EXC_T4}]})
# controls: must FAIL under the rules (harness sanity)
ctl = {
    'C-a_existing_line_not_new (R46.5)': ('R46.5', {'id': 'R46.5', 'status': 'fixed', 'commit': K4,
                                                    'evidence': [{'path': 'SHONEN.md', 'lines': '5-5', 'excerpt': '- [~] No cross-domain bleed (PROVINCE.md still accurate)'}]}, REV_F),
    'C-b_excerpt_absent (R41.1)': ('R41.1', {'id': 'R41.1', 'status': 'fixed', 'commit': K1,
                                             'evidence': [{'path': 'corpus/QUALITY.md', 'lines': '%d-%d' % (L1, L1), 'excerpt': 'this text is not in the file at all'}]}, REV_F),
    'C-c_commit_not_touching_path (R41.1)': ('R41.1', {'id': 'R41.1', 'status': 'fixed', 'commit': K2,
                                                       'evidence': [{'path': 'corpus/QUALITY.md', 'lines': '%d-%d' % (L1, L1), 'excerpt': EXC_T1}]}, REV_F),
    'C-d_open_without_planned (R41.1)': ('R41.1', {'id': 'R41.1', 'status': 'open', 'evidence': REAL_ROWS['R41.1']['evidence']}, REV_F),
}
out['forgery'] = {}
for name, (rid, row) in forg.items():
    out['forgery'][name] = row_verdict(rid, REV_F, row, name)
    out['forgery'][name]['row'] = row
out['control'] = {}
for name, (rid, row, rev) in ctl.items():
    out['control'][name] = row_verdict(rid, rev, row, name)

# ---- open-flip acceptance per item: every item flipped to open, real evidence, at planned rev ----
out['open_flip_planned'] = {}
for rid in ALL:
    row = {'id': rid, 'status': 'open', 'evidence': REAL_ROWS[rid]['evidence']}
    out['open_flip_planned'][rid] = row_verdict(rid, REV_O, row, 'open ' + rid)

# ---- declined flip acceptance per item (reason >= 40 chars, cap checked separately) ----
REASON = 'declined: superseded by a later rewrite; no change needed here'
out['declined_flip'] = {}
for rid in ALL:
    row = {'id': rid, 'status': 'declined', 'reason': REASON, 'evidence': REAL_ROWS[rid]['evidence']}
    out['declined_flip'][rid] = row_verdict(rid, REV_F, row, 'declined ' + rid)

# ---- full forged ledger: 20 fixed kept (all this-round fixes + first others with resolving evidence) ----
REAL_FIXED = [i for i in ALL if REAL_ROWS[i]['status'] == 'fixed']
this_round = [i for i in REAL_FIXED if not m.is_ancestor(CL, REAL_ROWS[i]['commit'], ROUND_BASE)]
ok_fixed = [i for i in REAL_FIXED if i not in this_round and evidence_resolves(i, REAL_ROWS[i], REV_O)]
keep = this_round + ok_fixed[:20 - len(this_round)]
full = {}
subs = []
for rid in ALL:
    if rid in keep:
        continue
    row = {'id': rid, 'status': 'open', 'evidence': REAL_ROWS[rid]['evidence']}
    if not evidence_resolves(rid, row, REV_O):
        sub = find_substitute(rid, REV_O)
        if sub is None:
            raise SystemExit('no substitute for %s' % rid)
        row['evidence'] = sub
        subs.append(rid)
    full[rid] = row
counts, stat, total, notes = probe(REV_O, full, 'full forged 20 fixed / rest open')
out['full_forgery'] = {'keep_fixed': keep, 'this_round_kept': this_round, 'substituted_evidence': subs,
                       'stat': stat, 'total': total,
                       'counts_nonzero': {k: v for k, v in counts.items() if v},
                       'notes': [list(map(str, a)) for a in notes]}

# ---- candidate-check measurement on the real 31 fixed rows (evidence read at BASE) ----
X = {}
for rid in REAL_FIXED:
    row = REAL_ROWS[rid]
    fresh = fresh_items(rid, row, BASE)
    X[rid] = {'fresh_n': len(fresh), 'X1_overlap3': X1_overlap(rid, fresh), 'X2_message': X2_message(rid, row),
              'X2d_diff_added': X2d_diff_added(rid, row, fresh), 'X3_removal': X3_removal(rid, row, fresh),
              'X4_not_comment': X4_not_comment(rid, fresh), 'this_round': rid in this_round,
              'evidence_resolves_base': evidence_resolves(rid, row, BASE)}
out['real_fixed_checks'] = X

# ---- candidate checks on forged fixed rows (same logic, evidence read at REV_F) ----
FX = {}
for name, (rid, row) in forg.items():
    fresh = fresh_items(rid, row, REV_F)
    FX[name] = {'fresh_n': len(fresh), 'X1_overlap3': X1_overlap(rid, fresh), 'X2_message': X2_message(rid, row),
                'X2d_diff_added': X2d_diff_added(rid, row, fresh), 'X3_removal': X3_removal(rid, row, fresh),
                'X4_not_comment': X4_not_comment(rid, fresh)}
out['forged_fixed_checks'] = FX

# ---- open-row check on the 7 real open rows and on the 29 forged open flips ----
OPEN_REAL = [i for i in ALL if REAL_ROWS[i]['status'] == 'open']
out['open_checks_real'] = {i: X5_open_defect_unchanged(i, REAL_ROWS[i], BASE) for i in OPEN_REAL}
out['open_checks_forged'] = {i: X5_open_defect_unchanged(i, full[i], REV_O) for i in full}
out['open_checks_flipped_from_fixed'] = {i: X5_open_defect_unchanged(i, full[i], REV_O) for i in full if REAL_ROWS[i]['status'] == 'fixed'}

path = os.path.join(S, 'out.json')
with open(path, 'w', encoding='utf-8') as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)
print('WROTE', path)
