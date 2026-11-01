#!/usr/bin/env python3
"""differential.py — synthetic-repo differential: frozen selector (spawns) vs
the portable batched execution form, byte-for-byte on the coldread section JSON."""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRATCH = Path(__file__).resolve().parent
LANE = Path(r"C:/Users/jpvei/.zcode/workspace/95b1ba4d-5089-47a4-9fd8-54adebbce2ae/fleet/tameshi-shokunin")
PORTABLE = SCRATCH / 'coldread-precheck-portable.py'

# frozen sectionizer, imported once for fixture construction
_spec = importlib.util.spec_from_file_location('r18fix', LANE / '.ufo/evidence/round-18/measure.py')
_modfix = importlib.util.module_from_spec(_spec)
sys.modules['r18fix'] = _modfix
_spec.loader.exec_module(_modfix)
mod_sectionize = _modfix.sectionize


def run(cmd, cwd, env=None, input_bytes=None):
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    if env:
        e.update(env)
    return subprocess.run(cmd, cwd=cwd, capture_output=True, env=e,
                          input=input_bytes)


def build_repo(root):
    repo = root / 'lane'
    repo.mkdir()
    def g(*args, input_bytes=None):
        r = run(['git', '-c', 'core.fileMode=true', *args], str(repo),
                input_bytes=input_bytes)
        assert r.returncode == 0, (args, r.stderr[:300])
        return r.stdout
    g('init', '--quiet', '-b', 'master')
    def put(rel, data, mode=None):
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, str):
            data = data.encode('utf-8')
        p.write_bytes(data)
        g('add', '--all', '--', rel)
        if mode == '120000':
            blob = g('hash-object', '-w', '--stdin', input_bytes=data).decode().strip()
            run(['git', 'update-index', '--add', '--cacheinfo',
                 '120000,%s,%s' % (blob, rel)], str(repo))
        if mode == '100755':
            run(['git', 'update-index', '--chmod=+x', '--', rel], str(repo))
    skill = "\n".join([
        "# lane",
        "",
        "## Section A",
        "alpha body",
        "",
        "## Section B",
        "beta body",
        "",
        "## Section C",
        "gamma body",
        "",
        "## Section D",
        "delta body",
        "",
        "```",
        "## not a heading",
        "```",
        "",
        "## Section E",
        "epsilon body",
        "",
    ]) + "\n"
    put('SKILL.md', skill)
    # real section shas from the frozen sectionizer
    import hashlib
    secs = mod_sectionize(skill.encode('utf-8'))
    sha_by_heading = {s['heading']: s['sha256'] for s in secs}
    put('tools/mutate-and-run.sh', "#   js-a x 1/1\n", mode='100755')
    put('SHONEN.md', "- [~] box one\n- [~] box two\n- [~] box three\n- [~] box four\n")
    put('corpus/SOURCES.md', "| id | tier | status |\n|---|---|---|\n| S001 | A | mined |\n")
    put('inputs/one.txt', 'content-one\n')
    put('inputs/two.txt', 'content-two\n')
    put('inputs/link-target.txt', 'link-target\n')
    put('inputs/exec.sh', '#!/bin/sh\n', mode='100755')
    # symlink entry recorded as a real 120000 tree entry
    put('inputs/sym.txt', 'inputs/link-target.txt\n', mode='120000')
    def sha(path_bytes):
        import hashlib
        return hashlib.sha256(path_bytes).hexdigest()
    one = sha(b'content-one\n')
    two = sha(b'content-two\n')
    lt = sha(b'inputs/link-target.txt\n')
    ex = sha(b'#!/bin/sh\n')
    sym = sha(b'inputs/link-target.txt\n')
    def mk_trace(name, inputs_map):
        return {
            'schema': 'tameshi-trace-inputs-v1',
            'argv': ['rekey-differential', name], 'cwd': str(repo), 'root': str(repo),
            'rev': None, 'rev_reason': 'differential fixture', 'exit': 0,
            'tracked_filter': True, 'env_overrides': {'git_vars_removed': [], 'set': {}},
            'inputs': inputs_map, 'untracked': [], 'external': {},
            'live_lane_reads': {}, 'dropped_home_count': 0,
        }
    traces = {
        't1': {'inputs/one.txt': one},
        't2': {'inputs/exec.sh': ex},
        't3': {'inputs/sym.txt': sym},
        't4': {'inputs/absent.txt': '00'},
        't5': {'inputs/two.txt': two},
    }
    for name, m in traces.items():
        put('.ufo/evidence/round-61/traces/%s.json' % name,
            json.dumps(mk_trace(name, m), indent=1))
    trace_ref = {name: '.ufo/evidence/round-61/traces/%s.json' % name
                 for name in traces}
    entries = [
        # A: verifies at rev1, drifts at rev2 (one.txt edited)
        {'skill_sha256': 'X', 'start': 3, 'heading': '## Section A',
         'sha256': sha_by_heading['## Section A'], 'class': 'record', 'verdict': 'verified-record',
         'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 0,
         'commands_executed_count': 1,
         'inputs': {'inputs/one.txt': one},
         'traces': [trace_ref['t1']]},
        # B: exec-bit input (mode 100755 passes BLOB_MODES)
        {'skill_sha256': 'X', 'start': 6, 'heading': '## Section B',
         'sha256': sha_by_heading['## Section B'], 'class': 'record', 'verdict': 'gap-minor',
         'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 1,
         'commands_executed_count': 1,
         'inputs': {'inputs/exec.sh': ex},
         'traces': [trace_ref['t2']]},
        # C: symlink input (mode 120000 -> input-not-blob)
        {'skill_sha256': 'X', 'start': 9, 'heading': '## Section C',
         'sha256': sha_by_heading['## Section C'], 'class': 'record', 'verdict': 'gap-minor',
         'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 0,
         'commands_executed_count': 1,
         'inputs': {'inputs/sym.txt': sym},
         'traces': [trace_ref['t3']]},
        # D: missing input
        {'skill_sha256': 'X', 'start': 12, 'heading': '## Section D',
         'sha256': sha_by_heading['## Section D'], 'class': 'record', 'verdict': 'gap-minor',
         'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 0,
         'commands_executed_count': 1,
         'inputs': {'inputs/absent.txt': '00'},
         'traces': [trace_ref['t4']]},
        # E: good entry whose inputs verify at both revs
        {'skill_sha256': 'X', 'start': 19, 'heading': '## Section E',
         'sha256': sha_by_heading['## Section E'], 'class': 'record', 'verdict': 'verified-record',
         'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 0,
         'commands_executed_count': 1,
         'inputs': {'inputs/two.txt': two},
         'traces': [trace_ref['t5']]},
    ]
    ledger = {'schema': 'tameshi-coldread-ledger-v2', 'entries': entries}
    put('.ufo/evidence/round-21/coldread/ledger.json', json.dumps(ledger, indent=1))
    # round-18 measure.py + the selector, so the selector main can run in the fixture
    put('.ufo/evidence/round-18/measure.py',
        (LANE / '.ufo/evidence/round-18/measure.py').read_bytes())
    put('.ufo/evidence/round-21/coldread/measure.py',
        (LANE / '.ufo/evidence/round-21/coldread/measure.py').read_bytes())
    put('tools/mutate-and-run.sh', "#   js-a x 1/1\n", mode='100755')
    g('-c', 'user.name=f', '-c', 'user.email=f@x', 'commit', '--quiet', '-m', 'rev1')
    rev1 = g('rev-parse', 'HEAD').decode().strip()
    # rev2: edit one.txt (drifts section A only)
    put('inputs/one.txt', 'content-one-EDITED\n')
    g('-c', 'user.name=f', '-c', 'user.email=f@x', 'commit', '--quiet', '-m', 'rev2')
    rev2 = g('rev-parse', 'HEAD').decode().strip()
    return repo, rev1, rev2, skill


def main():
    impl = LANE / '.ufo/evidence/round-18/measure.py'
    spec = importlib.util.spec_from_file_location('r18', impl)
    mod = importlib.util.module_from_spec(spec)
    sys.modules['r18'] = mod
    spec.loader.exec_module(mod)
    failures = []
    with tempfile.TemporaryDirectory(prefix='tameshi-r61-diff-', dir=SCRATCH) as tmp:
        repo, rev1, rev2, skill_raw = build_repo(Path(tmp))
        ledger_raw = (repo / '.ufo/evidence/round-21/coldread/ledger.json').read_bytes()
        sel = repo / '.ufo/evidence/round-21/coldread/measure.py'
        for rev in (rev1, rev2):
            r = run([sys.executable, '-I', str(sel), '--repo', str(repo), '--rev', rev],
                    str(repo))
            assert r.returncode == 0, r.stderr[:400]
            frozen_raw = json.loads(r.stdout)['coldread']
            frozen = {k: frozen_raw[k] for k in ('sections_total',
                                                 'sections_covered',
                                                 'box3_full_page', 'sections',
                                                 'reasons')}
            work = Path(tmp) / ('work-' + rev[:8])
            work.mkdir()
            # portable form: import and measure via the tool's own functions
            pspec = importlib.util.spec_from_file_location(
                'portable', PORTABLE)
            pmod = importlib.util.module_from_spec(pspec)
            sys.modules['portable'] = pmod
            pspec.loader.exec_module(pmod)
            fmod = pmod.load_frozen(str(repo))
            m = pmod.measure_rev(fmod, repo, rev, work, 2, 10, 7)
            mine = {k: m[k] for k in ('sections_total', 'sections_covered',
                                      'box3_full_page', 'sections', 'reasons')}
            # explain=True adds end/reasons; the frozen run above used none
            mine['sections'] = [{k: s[k] for k in ('start', 'heading',
                                                   'credited', 'vetoed',
                                                   'reason')}
                                for s in mine['sections']]
            if mine != frozen:
                failures.append('rev %s MISMATCH' % rev[:8])
                for k in mine:
                    if mine[k] != frozen[k]:
                        failures.append('  key %s: frozen=%r mine=%r'
                                        % (k, frozen[k], mine[k]))
            else:
                print('DIFF rev=%s credited=%d/%d sections-match=OK '
                      'probe_mismatches=%d'
                      % (rev[:8], m['sections_covered'], m['sections_total'],
                         m['probe']['mismatches']))
            # summarize discriminators
            if rev == rev2:
                reasons = {s['heading']: s['reason'] for s in frozen['sections']}
                print('DISCRIMINATORS at rev2:')
                for h in sorted(reasons):
                    print('  %-16s %s' % (h, reasons[h][:60]))
    if failures:
        print('DIFFERENTIAL: FAIL')
        for f in failures:
            print(f)
        return 1
    print('DIFFERENTIAL: PASS (frozen selector == portable batched form)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
