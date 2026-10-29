#!/usr/bin/env python3
"""Focused probe for mutant M10 (panel verdict lookup defaults to 'fixed').

Builds a fixture git repo where ONE new row has status_at_base='fixed' and the panel file
OMITS that id's verdict. Pristine: a missing panel verdict is a disagreement (panel_over=1,
PASS=false). Mutant: the missing verdict defaults to 'fixed', the row's own claim is echoed,
the disagreement vanishes and the counter PASSes.

Usage: probe_m10.py <counter.py>            # prints the verdict line of that counter
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO = None
NOTES = []


def g(*args):
    return subprocess.run(['git', '-C', REPO] + list(args), check=True, capture_output=True,
                          env=dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t',
                                   GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t'))


def write(path, text):
    full = os.path.join(REPO, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as fh:
        fh.write(text)


def commit(msg):
    g('add', '-A')
    g('commit', '-q', '--allow-empty', '-m', msg)
    return g('rev-parse', 'HEAD').stdout.decode().strip()


def load(path):
    spec = importlib.util.spec_from_file_location('c1mut', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    global REPO
    counter_path = sys.argv[1]
    mod = load(counter_path)
    work = tempfile.mkdtemp(prefix='probe-m10-')
    REPO = tempfile.mkdtemp(prefix='probe-repo-', dir=work)
    try:
        g('init', '-q')
        assert os.path.realpath(g('rev-parse', '--show-toplevel').stdout.decode().strip()) == os.path.realpath(REPO)
        spot_path = 'corpus/lessons/round-50-verifier-spotcheck.md'
        spot = '# Round 50 verifier spot-check\n\n1. **Extractor pairing.** BACKTICK_RE spans newlines.\n'
        old_rows = [{'id': 'R49.1', 'status': 'declined', 'reason': 'x' * 45, 'seat': 's',
                     'evidence': [{'path': 'SHONEN.md', 'lines': '1-1', 'excerpt': '- [~] box one sentinel'}],
                     'note': 'n1'}]
        write('SHONEN.md', '- [~] box one\n')
        write('tools/f.py', 'old line\n')
        write(mod.LEDGER, json.dumps({'schema': 'x', 'defects': old_rows}))
        commit('base ledger')
        write(spot_path, spot)
        routed = commit('spot-check')           # routed_at
        write('tools/f.py', 'BACKTICK_RE = fixed_here\n')
        fix = commit('fix R50.1: BACKTICK_RE')   # the claimed fix, names the id
        base = commit('base marker')            # BASE, after the fix
        new_rows = list(old_rows) + [
            {'id': 'R50.1', 'status': 'fixed', 'status_at_base': 'fixed', 'commit': fix,
             'evidence': [{'path': 'tools/f.py', 'lines': '1-1', 'excerpt': 'BACKTICK_RE = fixed_here'}]}]
        write(mod.LEDGER, json.dumps({'schema': 'x', 'defects': new_rows}))
        # the blind panel OMITS a verdict for R50.1
        panel_blob = json.dumps({'verdicts': {'R50.9': 'open'}})
        write(mod.PANEL_PATH, panel_blob)
        rev = commit('ledger with the new row')
        defects = [{'id': 'R50.1', 'file': spot_path, 'file_sha256': hashlib.sha256(spot.encode()).hexdigest(),
                    'routed_at': routed, 'keys': ['BACKTICK_RE'],
                    'text': 'the BACKTICK_RE extractor spans newlines; use the tools/f.py line-scoped rule'}]
        ppin = hashlib.sha256(panel_blob.encode()).hexdigest()
        res = mod.measure(REPO, rev, defects, True, fixed_floor=0, declined_cap=999, this_round_floor=0,
                          base=base, old_expect=1, expected_spots=(spot_path,),
                          explain=lambda *a: NOTES.append(a), panel_pin=ppin, panel_allowed=0)
        print('counter  : %s' % counter_path)
        print('panel    : %s (no verdict for R50.1)' % panel_blob)
        print('verdict  : %s' % mod.verdict(res))
        print('notes    : %s' % NOTES)
        print('RESULT   : %s' % ('PASS (defect masked)' if res['total'] == 0 else 'REFUSED (defect caught)'))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    main()
