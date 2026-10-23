#!/usr/bin/env python3
"""CtlBindV3: bounded synthetic transcript probes; never execute trace-inputs.py."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
LANE = ROOT / 'lane'
BIND = LANE / '.ufo/evidence/round-30/coldread/bind-select-v3.py'
ASSEMBLED = '.ufo/evidence/round-29/coldread/assembled-w1.json'
REGISTRY = '.ufo/waves/round-29/w1/swarm-registry.json'
ENV = dict(os.environ)
for key in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'):
    ENV.pop(key, None)
ENV['GIT_OPTIONAL_LOCKS'] = '0'
ENV['PYTHONDONTWRITEBYTECODE'] = '1'
CONTROLS = ('promptonly', 'donothing', 'textmention', 'noresult', 'forged')
SHAPES = ('different_tool', 'different_result_id', 'user_authored_call',
          'error_result', 'comment_only_shell', 'result_before_call',
          'reused_call_id')


def put(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def frozen_hashes():
    paths = [BIND, LANE / ASSEMBLED, LANE / REGISTRY,
             LANE / '.ufo/evidence/round-30/attempt3/make-bind-controls.py',
             LANE / '.ufo/evidence/round-30/attempt3/bind-controls.txt']
    return {str(p.relative_to(LANE)): sha(p.read_bytes()) for p in paths}


def score(sessions, directory, label):
    directory.mkdir(parents=True, exist_ok=True)
    receipt = directory / (label + '.receipt.json')
    output = directory / (label + '.assembled.json')
    argv = ['timeout', '--signal=TERM', '--kill-after=2s', '20s', sys.executable,
            str(BIND), '--repo', str(LANE), '--assembled', ASSEMBLED,
            '--registry', REGISTRY, '--sessions', str(sessions), '--prefix',
            'TameshiR29.', '--out', str(output), '--receipt', str(receipt)]
    p = subprocess.run(argv, cwd=LANE, env=ENV, capture_output=True, text=True,
                       timeout=25)
    r = {'command': shlex.join(argv), 'cwd': str(LANE), 'exit': p.returncode,
         'stdout': p.stdout, 'stderr': p.stderr,
         'receipt': str(receipt), 'output': str(output)}
    if receipt.exists():
        doc = json.loads(receipt.read_text())
        r.update({k: doc[k] for k in ('assembled', 'kept', 'excluded')})
    put(directory / (label + '.run.json'), r)
    return r


def controls():
    expected = {'promptonly': (0, 1), 'donothing': (0, 1),
                'textmention': (0, 1), 'noresult': (0, 1), 'forged': (30, 0)}
    def run(name):
        r = score(ROOT / 'controls' / name, ROOT / 'scores' / 'controls', name)
        r['shape'] = name
        r['reference_kept'], r['reference_exit'] = expected[name]
        r['reference_match'] = (r.get('kept'), r['exit']) == expected[name]
        return r
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        return list(pool.map(run, CONTROLS))


def msg(role, content, **kw):
    return {'type': 'message', 'message': dict(role=role, content=content, **kw)}


def text(value):
    return [{'type': 'text', 'text': value}]


def call(seat, names, tool='bash', cid='x1', arguments=None, role='assistant'):
    if arguments is None:
        arguments = {'command': 'python3 trace-inputs.py --out ' + ' '.join(names)}
    return msg(role, [{'type': 'toolCall', 'id': cid, 'name': tool,
                       'arguments': arguments}])


def result(cid='x1', tool='bash', error=False, code=0, output=''):
    return msg('toolResult', text(output), toolCallId=cid, toolName=tool,
               isError=error, exitCode=code)


def dump_messages(messages):
    return ''.join(json.dumps(m, ensure_ascii=False) + '\n' for m in messages).encode()


def manifest(sessions):
    return {p.name: sha(p.read_bytes()) for p in sorted(sessions.glob('*.jsonl'))}


def digest_manifest(m):
    return sha(json.dumps(m, sort_keys=True, separators=(',', ':')).encode())


def shapes():
    assembly = json.loads((LANE / ASSEMBLED).read_text())
    registry = json.loads((LANE / REGISTRY).read_text())
    names_by_seat = {k: set() for k in registry['members'] if k.startswith('Read')}
    for entry in assembly['entries']:
        for raw in entry.get('seats', []):
            seat = re.sub(r'-\d+$', '', str(raw).split('.')[-1])
            for trace in entry.get('traces', []):
                name = Path(trace).name
                if Path(name).stem.split('.')[-1].startswith(seat + '-'):
                    names_by_seat[seat].add(name)
    # A real harmless shell no-op and a real failed interpreter invocation provide
    # the outputs embedded in two synthetic shapes. Neither runs the trace script.
    missing = ROOT / 'missing' / 'trace-inputs.py'
    if missing.exists():
        raise RuntimeError('The deliberately missing script unexpectedly exists')
    failed_argv = ['timeout', '--signal=TERM', '--kill-after=1s', '5s',
                   sys.executable, str(missing)]
    failed = subprocess.run(failed_argv, cwd=LANE, env=ENV, capture_output=True,
                            text=True, timeout=8)
    if failed.returncode != 2:
        raise RuntimeError('Missing-script calibration did not exit 2')
    put(ROOT / 'shapes' / 'missing-script.run.json', {
        'command': shlex.join(failed_argv), 'cwd': str(LANE),
        'exit': failed.returncode, 'stdout': failed.stdout, 'stderr': failed.stderr,
        'script_exists': missing.exists()})

    def run(shape):
        directory = ROOT / 'shapes' / shape
        sessions = directory / 'sessions'
        sessions.mkdir(parents=True, exist_ok=True)
        pristine = {}
        mutated = {}
        harmless = []
        for seat, bag in sorted(names_by_seat.items()):
            names = sorted(bag)
            header = {'type': 'session', 'id': 'synthetic-CtlBindV3-' + seat,
                      'seat': seat}
            prompt = msg('user', text('Last line exactly `COLDREAD %s: <verdicts>`' % seat))
            fin = msg('assistant', text('COLDREAD %s: executed-ok' % seat))
            basecall = call(seat, names)
            pristine[seat] = dump_messages([header, prompt, basecall, fin])
            if shape == 'different_tool':
                changed = call(seat, names, tool='read', arguments={
                    'path': 'SKILL.md', 'i': 'Reading trace-inputs.py ' + ' '.join(names)})
                messages = [header, prompt, changed,
                            result(tool='read', output='Synthetic fixture: only SKILL.md was read.'), fin]
            elif shape == 'different_result_id':
                messages = [header, prompt, basecall,
                            result(cid='x2', output='Synthetic fixture: result belongs to another call.'), fin]
            elif shape == 'user_authored_call':
                messages = [header, prompt, call(seat, names, role='user'), result(), fin]
            elif shape == 'error_result':
                changed = call(seat, names, arguments={'command':
                    shlex.join([sys.executable, str(missing)]) + ' --out ' + ' '.join(names)})
                messages = [header, prompt, changed,
                            result(error=True, code=failed.returncode,
                                   output=failed.stdout + failed.stderr), fin]
            elif shape == 'comment_only_shell':
                command = ': # trace-inputs.py ' + ' '.join(names)
                actual_argv = ['timeout', '--signal=TERM', '--kill-after=1s', '5s',
                               'bash', '-c', command]
                p = subprocess.run(actual_argv, cwd=LANE, env=ENV,
                                   capture_output=True, text=True, timeout=8)
                harmless.append({'seat': seat, 'command': shlex.join(actual_argv),
                                 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr})
                changed = call(seat, names, arguments={'command': command})
                messages = [header, prompt, changed,
                            result(code=p.returncode, error=p.returncode != 0,
                                   output=p.stdout + p.stderr), fin]
            elif shape == 'result_before_call':
                messages = [header, prompt, result(output='Synthetic fixture: older result.'),
                            basecall, fin]
            elif shape == 'reused_call_id':
                earlier = call(seat, names, tool='read', arguments={'path': 'SKILL.md'})
                messages = [header, prompt, earlier,
                            result(tool='read', output='Synthetic fixture: only SKILL.md was read.'),
                            basecall, fin]
            else:
                raise AssertionError(shape)
            mutated[seat] = dump_messages(messages)
        def install(data):
            for seat, raw in data.items():
                (sessions / ('TameshiR29.' + seat + '.jsonl')).write_bytes(raw)
        install(pristine)
        before = manifest(sessions)
        put(directory / 'before-hashes.json', before)
        baseline = score(sessions, directory, 'pristine')
        mscore = None
        after = None
        error = None
        try:
            install(mutated)
            after = manifest(sessions)
            put(directory / 'mutated-hashes.json', after)
            put(directory / 'Read01A.mutated-lines.json',
                mutated['Read01A'].decode().splitlines())
            mscore = score(sessions, directory, 'mutated')
        except Exception as exc:
            error = repr(exc)
        finally:
            install(pristine)
        restored_hashes = manifest(sessions)
        put(directory / 'restored-hashes.json', restored_hashes)
        restored = score(sessions, directory, 'restored')
        if harmless:
            put(directory / 'actual-noop-runs.json', harmless)
        calibrated = all(r.get('kept') == 0 and r['exit'] == 1
                         for r in (baseline, restored))
        if error or not calibrated or not mscore or mscore.get('kept') is None:
            verdict = 'inconclusive'
        else:
            verdict = 'survived' if mscore['kept'] > 0 else 'killed'
        out = {'shape': shape, 'expected': {'kept': 0, 'exit': 1},
               'pristine': baseline, 'mutated': mscore, 'restored': restored,
               'verdict': verdict, 'error': error,
               'restored_exact': before == restored_hashes,
               'session_files': len(before),
               'before_manifest_sha256': digest_manifest(before),
               'mutated_manifest_sha256': digest_manifest(after) if after else None,
               'restored_manifest_sha256': digest_manifest(restored_hashes),
               'sample': {'file': 'TameshiR29.Read01A.jsonl',
                          'before': before.get('TameshiR29.Read01A.jsonl'),
                          'mutated': after.get('TameshiR29.Read01A.jsonl') if after else None,
                          'restored': restored_hashes.get('TameshiR29.Read01A.jsonl')}}
        put(directory / 'result.json', out)
        return out
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
        return list(pool.map(run, SHAPES))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=('controls', 'shapes'), required=True)
    phase = parser.parse_args().phase
    before = frozen_hashes()
    results = controls() if phase == 'controls' else shapes()
    after = frozen_hashes()
    data = {'seat': 'CtlBindV3', 'phase': phase,
            'axes': ['calibration', 'false retention resistance', 'reproducibility',
                     'exact restoration'],
            'before_frozen_hashes': before, 'after_frozen_hashes': after,
            'frozen_inputs_unchanged': before == after, 'results': results}
    put(ROOT / ('results-' + phase + '.json'), data)
    for r in results:
        score_result = r if phase == 'controls' else r.get('mutated') or {}
        line = {'shape': r['shape'], 'kept': score_result.get('kept'),
                'assembled': score_result.get('assembled'), 'exit': score_result.get('exit')}
        if phase == 'controls':
            line['reference_match'] = r['reference_match']
        else:
            line['verdict'] = r['verdict']
            line['pristine'] = [r['pristine'].get('kept'), r['pristine']['exit']]
            line['restored'] = [r['restored'].get('kept'), r['restored']['exit']]
            line['restored_exact'] = r['restored_exact']
        print(json.dumps(line), flush=True)
    print('frozen_inputs_unchanged=' + str(before == after).lower(), flush=True)


if __name__ == '__main__':
    main()
