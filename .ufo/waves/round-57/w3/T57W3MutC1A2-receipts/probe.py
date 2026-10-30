#!/usr/bin/env python3
"""Independent behavioural probe of the round-57 C1 counter's amendment-2 arms (A7/A8/A9).

Why: the shipped selftest of the amendment-2 counter is RED on the pristine bytes
(92/99), so it cannot carry a mutation verdict by itself. This probe builds its own
fixture lane, calls measure() of the module under test, and prints the observable value
of each amendment-2 arm. On pristine bytes every scenario reproduces its expected
observation, so a difference observed on a mutant is attributable to the mutation.

Usage: probe.py <path-to-measure.py> <scenario> <work-dir>
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

EX = 'BACKTICK_RE = re.compile(r"`([^`\\n]+)`")'
SPOT = ("1. **Extractor pairing.** the extractor pairs lines\n"
        "2. **Planned item.** the wave-slots pointer does not resolve\n"
        "3. **Observation.** nothing to fix; SHONEN boxes stay [~]\n")
SPOT_PATH = 'corpus/lessons/round-50-verifier-spotcheck.md'
LEDGER = 'corpus/routed-defects.json'
PANEL_PATH = '.ufo/evidence/round-57/c1/panel.json'
OLD_ROWS = [
    {'id': 'R49.1', 'status': 'fixed', 'commit': 'a' * 40, 'seat': 's',
     'evidence': [{'path': 'tools/x.py', 'lines': '1-1', 'excerpt': 'old = 1 sentinel text'}], 'note': 'n1'},
    {'id': 'R49.2', 'status': 'declined', 'reason': 'x' * 45, 'seat': 's',
     'evidence': [{'path': 'SHONEN.md', 'lines': '1-1', 'excerpt': '- [~] box one sentinel'}], 'note': 'n2'}]
SEAT_A, SEAT_B = 'T57W3SeatA', 'T57W3SeatB'


def load(path):
    spec = importlib.util.spec_from_file_location('measure_under_test', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def g(repo, *args):
    return subprocess.run(['git', '-C', repo] + list(args), check=True, capture_output=True,
                          env=dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t',
                                   GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t'))


class Fixture(object):
    def __init__(self, work):
        self.repo = tempfile.mkdtemp(prefix='probe-', dir=work)
        g(self.repo, 'init', '-q')
        real = os.path.realpath(g(self.repo, 'rev-parse', '--show-toplevel').stdout.decode().strip())
        assert real == os.path.realpath(self.repo), 'fixture toplevel mismatch: %s vs %s' % (real, self.repo)

    def write(self, path, text):
        full = os.path.join(self.repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as fh:
            fh.write(text)

    def commit(self, msg):
        g(self.repo, 'add', '-A')
        g(self.repo, 'commit', '-q', '--allow-empty', '-m', msg)
        return g(self.repo, 'rev-parse', 'HEAD').stdout.decode().strip()

    def destroy(self):
        shutil.rmtree(self.repo, ignore_errors=True)


def wave_blob(verdicts):
    return json.dumps({'seat': 'x', 'verdicts': verdicts})


def fixed_row(commit_id, status_at_base):
    return {'id': 'R50.1', 'status': 'fixed', 'status_at_base': status_at_base, 'commit': commit_id,
            'evidence': [{'path': 'tools/x.py', 'lines': '2-2', 'excerpt': EX}]}


def open_row():
    return {'id': 'R50.1', 'status': 'open', 'status_at_base': 'open',
            'evidence': [{'path': 'docs/note.md', 'lines': '1-1',
                          'excerpt': 'the wave-slots pointer is still open'}]}


def declined_row():
    return {'id': 'R50.2', 'status': 'declined', 'status_at_base': 'declined',
            'reason': 'an observation, not a defect: promotion is operator-owned and not actionable',
            'evidence': [{'path': 'docs/note2.md', 'lines': '1-1',
                          'excerpt': 'an observation only, nothing to repair'}]}


def scenario_spec(name, fix):
    """Returns dict describing rows/defects/panel/wave files/results/scorecard/base for a scenario."""
    spec = {}
    if name == 'npath_spotcheck':
        spec.update(
            rows=[{'id': 'R50.3', 'status': 'open', 'status_at_base': 'open',
                   'evidence': [{'path': './' + SPOT_PATH, 'lines': '1-1',
                                 'excerpt': '1. **Extractor pairing.**'}]}],
            defects=[{'id': 'R50.3', 'keys': ['Extractor']}],
            verdicts={'R50.3': 'open'},
            detail={'R50.3': {'seat': SEAT_A, 'commit': fix}},
            wave_files={SEAT_A: wave_blob({'R50.3': {'verdict': 'open'}})},
            results={'w2': [], 'w3': [SEAT_A]},
            scorecard='**Planned (round 58):** R50.3 the extractor pairing.\n',
            base='routed')
    elif name in ('tie_always_true', 'tie_len7_dropped'):
        short = 'deadbeef' if name == 'tie_always_true' else fix[:3]
        spec.update(
            rows=[fixed_row(fix, 'fixed')],
            defects=[{'id': 'R50.1', 'keys': ['BACKTICK_RE']}],
            verdicts={'R50.1': 'fixed'},
            detail={'R50.1': {'seat': SEAT_A, 'commit': short}},
            wave_files={SEAT_A: wave_blob({'R50.1': {'verdict': 'fixed'}})},
            results={'w2': [], 'w3': [SEAT_A]},
            scorecard='',
            base='base2')
    elif name == 'pcommits_filter':
        spec.update(
            rows=[fixed_row(fix, 'open')],
            defects=[{'id': 'R50.1', 'keys': ['BACKTICK_RE']}],
            verdicts={'R50.1': 'open'},
            detail={'R50.1': {'seat': SEAT_A, 'commit': fix[:8]}},
            wave_files={SEAT_A: wave_blob({'R50.1': {'verdict': 'open'}})},
            results={'w2': [], 'w3': [SEAT_A]},
            scorecard='',
            base='routed')
    elif name.startswith('prov_'):
        wave = {SEAT_A: wave_blob({'R50.1': {'verdict': 'open'}}),
                SEAT_B: wave_blob({'R50.2': {'verdict': 'declined'}})}
        results = {'w2': [], 'w3': [SEAT_A, SEAT_B]}
        corrupt = []
        wave_dir = 'w3'
        if name == 'prov_sha':
            corrupt = [SEAT_A]
        elif name == 'prov_verdict':
            wave[SEAT_A] = wave_blob({'R50.1': {'verdict': 'declined'}})
        elif name == 'prov_listed':
            results = {'w2': [], 'w3': [SEAT_B]}
        elif name == 'prov_loop_skip':
            corrupt = [SEAT_B]
        elif name == 'prov_w2_route':
            # the seat file lives in w2/ although the seat is named like a w3 seat
            wave_dir = 'w2'
            results = {'w2': [SEAT_A, SEAT_B], 'w3': []}
        spec.update(
            rows=[open_row(), declined_row()],
            defects=[{'id': 'R50.1', 'keys': ['wave-slots']}, {'id': 'R50.2', 'keys': ['observation']}],
            verdicts={'R50.1': 'open', 'R50.2': 'declined'},
            detail={'R50.1': {'seat': SEAT_A, 'commit': fix}, 'R50.2': {'seat': SEAT_B, 'commit': fix}},
            wave_files=wave,
            results=results,
            scorecard='**Planned (round 58):** R50.1 the wave-slots pointer.\n',
            base='routed',
            corrupt_files=corrupt,
            wave_dir=wave_dir)
    else:
        raise SystemExit('unknown scenario ' + name)
    spec.setdefault('corrupt_files', [])
    spec.setdefault('wave_dir', 'w3')
    return spec


def run_scenario(mod, name, work):
    fx = Fixture(work)
    try:
        fx.write('tools/x.py', 'old = 1\n')
        fx.write('SHONEN.md', '- [~] box one\n- [~] box two\n')
        fx.write('docs/old.md', 'BACKTICK_RE = legacy_definition_here\n')
        fx.write(LEDGER, json.dumps({'schema': 'x', 'defects': OLD_ROWS}))
        fx.commit('base0')
        fx.write(SPOT_PATH, SPOT)
        routed = fx.commit('spot-check routed')
        fx.write('tools/x.py', 'old = 1\n' + EX + '  # line-scoped extraction\n')
        fix = fx.commit('fix the extractor')
        base2 = fx.commit('base2')
        spec = scenario_spec(name, fix)
        rows = list(OLD_ROWS) + spec['rows']
        fx.write(LEDGER, json.dumps({'schema': 'x', 'defects': rows}))
        fx.write('docs/note.md', 'the wave-slots pointer is still open here\n')
        fx.write('docs/note2.md', 'an observation only, nothing to repair\n')
        fx.write('SCORECARD.md', spec['scorecard'])
        panel = {'verdicts': spec['verdicts'], 'detail': spec['detail']}
        files = {}
        for seat, blob in spec['wave_files'].items():
            fx.write('.ufo/waves/round-57/%s/%s.json' % (spec['wave_dir'], seat), blob)
            files[seat] = hashlib.sha256(blob.encode('utf-8')).hexdigest()
        for seat in spec['corrupt_files']:
            files[seat] = 'f' * 64
        panel['files'] = files
        fx.write(PANEL_PATH, json.dumps(panel))
        for wv, names in spec['results'].items():
            fx.write('.ufo/waves/round-57/%s-results.json' % wv,
                     json.dumps({'results': [{'name': n} for n in names]}))
        rev = fx.commit('ledger + panel + wave files')
        sha = hashlib.sha256(SPOT.encode('utf-8')).hexdigest()
        defects = [{'id': d['id'], 'file': SPOT_PATH, 'file_sha256': sha, 'routed_at': routed,
                    'keys': d['keys'], 'text': ''} for d in spec['defects']]
        base = base2 if spec['base'] == 'base2' else routed
        ppin = hashlib.sha256(open(os.path.join(fx.repo, PANEL_PATH), 'rb').read()).hexdigest()
        res = mod.measure(fx.repo, rev, defects, True, 0, 999, 0, base, 2, (SPOT_PATH,),
                          panel_pin=ppin, panel_allowed=5)
        terms = mod.terms_line(res)
        observed = {
            'total': res['total'],
            'agree': res['agree'],
            'fixed_bad': res['counts']['fixed_bad'],
            'evidence_bad': res['counts']['evidence_bad'],
            'panel_prov': res['counts'].get('panel_prov'),
            'panel_over': res['counts']['panel_over'],
            'terms_has_panel_prov': 'panel_prov=' in terms,
            'terms_line': terms,
        }
        return observed
    finally:
        fx.destroy()


SCENARIOS = ['npath_spotcheck', 'tie_always_true', 'tie_len7_dropped', 'pcommits_filter',
             'prov_sha', 'prov_verdict', 'prov_listed', 'prov_w3_route', 'prov_w2_route',
             'prov_count', 'prov_loop_skip']


def main():
    path = sys.argv[1]
    work = sys.argv[2] if len(sys.argv) > 2 else '/tmp'
    os.makedirs(work, exist_ok=True)
    mod = load(path)
    out = {}
    for sc in SCENARIOS:
        try:
            out[sc] = run_scenario(mod, sc, work)
        except Exception as exc:  # noqa: BLE001 - the probe reports the failure as data
            out[sc] = {'error': '%s: %s' % (type(exc).__name__, exc)}
    print(json.dumps(out, sort_keys=True, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
