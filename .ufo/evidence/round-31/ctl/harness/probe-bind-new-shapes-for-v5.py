#!/usr/bin/env python3
"""Bounded, isolated input-mutation controls for the frozen round-31 binding v4.

These are deliberately forged transcript fixtures, never historical sessions.
The generated command strings are data only: this harness never executes them.
"""
import concurrent.futures
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT / 'repo'
PRISTINE = ROOT / 'sessions-pristine'
BINDER = REPO / '.ufo/evidence/round-31/coldread/bind-select-v5.py'
ASSEMBLED = REPO / '.ufo/evidence/round-30/coldread/assembled-wC.json'
REGISTRY = REPO / '.ufo/waves/round-30/wC/swarm-registry.json'
SOURCE_ROOT = '/home/vgpnk/Projects/shokunin/tameshi-shokunin/'
PREFIX = 'TameshiR30A3.'
SHAPES = (
    'echo_full_call',
    'python_c_string',
    'literal_heredoc',
    'split_simple_commands',
    'python_c_script_argument',
    'false_and_branch',
    'uncalled_function',
    'quoted_separator_argument',
    'changed_traced_argv',
)
EXPECTED_BINDER_SHA = '8760ddc9014af73a20dc95627528b845af75c9539c780fa509fba2c9b2e61338'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def hashes(directory):
    return {str(p.relative_to(directory)): sha(p.read_bytes())
            for p in sorted(directory.rglob('*')) if p.is_file()}


def manifest_sha(manifest):
    return sha(json.dumps(manifest, sort_keys=True, separators=(',', ':')).encode())


def command_for(shape, out, argv):
    base = shlex.join(['python3', 'tools/trace-inputs.py', '--out', out, '--', *argv])
    if shape == 'echo_full_call':
        return 'echo ' + base
    if shape == 'python_c_string':
        return shlex.join(['python3', '-c', 'print(' + repr(base) + ')'])
    if shape == 'literal_heredoc':
        return "cat <<'R31_LITERAL_DATA'\n" + base + '\nR31_LITERAL_DATA'
    if shape == 'split_simple_commands':
        return shlex.join(['python3', '-c', 'pass', '--out', out]) + '; ' + shlex.join(
            ['python3', 'tools/trace-inputs.py', '--', *argv])
    if shape == 'python_c_script_argument':
        # -c consumes the following token as Python code, not as a script path.
        return shlex.join(['python3', '-c', 'tools/trace-inputs.py', '--out', out, '--', *argv]) + '; :'
    if shape == 'false_and_branch':
        return 'false && ' + base + '; :'
    if shape == 'uncalled_function':
        return 'r31_never_called() {\n' + base + '\n}\n:'
    if shape == 'quoted_separator_argument':
        # The quoted semicolon is a printf argument, never a shell separator.
        return "printf '%s\\n' literal ';' " + base
    if shape == 'changed_traced_argv':
        return shlex.join(['python3', 'tools/trace-inputs.py', '--out', out, '--',
                           'python3', '-c', 'pass', 'R31_DIFFERENT_ARGV'])
    raise ValueError(shape)


def detector(shape_dir, phase, assembled):
    cmd = ['timeout', '--signal=TERM', '--kill-after=2s', '30s', sys.executable,
           str(BINDER), '--repo', str(REPO), '--assembled', str(assembled),
           '--registry', str(REGISTRY), '--sessions', str(shape_dir / 'sessions'),
           '--prefix', PREFIX, '--out', str(shape_dir / (phase + '.kept.json')),
           '--receipt', str(shape_dir / (phase + '.receipt.json'))]
    env = dict(os.environ)
    for key in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'):
        env.pop(key, None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    run = subprocess.run(cmd, cwd=REPO, env=env, capture_output=True, text=True, timeout=36)
    result = {'command': shlex.join(cmd), 'cwd': str(REPO), 'exit': run.returncode,
              'stdout': run.stdout, 'stderr': run.stderr}
    receipt = shape_dir / (phase + '.receipt.json')
    if receipt.exists():
        data = json.loads(receipt.read_text())
        result.update({key: data[key] for key in ('assembled', 'kept', 'excluded')})
        result['kept_entries'] = [{'start': e['start'], 'heading': e['heading']}
                                  for e in data['kept_entries']]
        result['excluded_entries'] = data['excluded_entries']
    dump(shape_dir / (phase + '.run.json'), result)
    return result


def mutate_sessions(shape, sessions, mod, trace_map):
    changes = []
    changed_basenames = set()
    for path in sorted(sessions.glob('*.jsonl')):
        lines = path.read_bytes().splitlines(keepends=True)
        changed = False
        for line_index, raw in enumerate(lines):
            try:
                record = json.loads(raw)
            except ValueError:
                continue
            msg = record.get('message') if record.get('type') == 'message' else None
            if not msg or msg.get('role') != 'assistant':
                continue
            line_changed = False
            for call in msg.get('content') or []:
                if call.get('type') != 'toolCall' or call.get('name') != 'bash':
                    continue
                args = call.get('arguments') or {}
                original = args.get('command', '')
                traced = mod.traced_commands(original)
                if not traced:
                    continue
                replacements = []
                outs = []
                for basename, _ in traced:
                    if basename not in trace_map:
                        continue
                    out, receipt = trace_map[basename]
                    replacements.append(command_for(shape, out, receipt['argv']))
                    outs.append(basename)
                    changed_basenames.add(basename)
                replacement = '\n'.join(replacements) if replacements else ':'
                call['arguments'] = dict(args, command=replacement)
                changes.append({'transcript': path.name, 'line': line_index + 1,
                                'call_id': call.get('id'), 'trace_basenames': outs,
                                'original_command': original, 'mutated_command': replacement})
                line_changed = True
            if line_changed:
                lines[line_index] = (json.dumps(record, ensure_ascii=False) + '\n').encode()
                changed = True
        if changed:
            path.write_bytes(b''.join(lines))
    if set(trace_map) - changed_basenames:
        raise RuntimeError('Some named traces lack a mutated call: ' + repr(sorted(set(trace_map) - changed_basenames)))
    return changes


def one_shape(shape, mod, assembled, trace_map):
    work = ROOT / 'shapes' / shape
    sessions = work / 'sessions'
    sessions.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(PRISTINE, sessions)
    originals = {p: p.read_bytes() for p in sessions.rglob('*') if p.is_file()}
    before = hashes(sessions)
    dump(work / 'before-hashes.json', before)
    result = {'shape': shape, 'expected_mutated': {'assembled': 63, 'kept': 0, 'exit': 1},
              'generated_commands_executed': False}
    mutated = None
    try:
        result['pristine'] = detector(work, 'pristine', assembled)
        changes = mutate_sessions(shape, sessions, mod, trace_map)
        dump(work / 'mutations.json', changes)
        mutated = hashes(sessions)
        dump(work / 'mutated-hashes.json', mutated)
        result['mutated'] = detector(work, 'mutated', assembled)
        result['changed_calls'] = len(changes)
        result['changed_transcripts'] = sum(before[k] != mutated[k] for k in before)
        result['changed_trace_basenames'] = len(trace_map)
    except Exception as exc:
        result['probe_error'] = repr(exc)
    finally:
        for path, raw in originals.items():
            path.write_bytes(raw)
        restored = hashes(sessions)
        dump(work / 'restored-hashes.json', restored)
        result['restored_exact'] = before == restored
        result['manifest_hashes'] = {'before': manifest_sha(before),
                                     'mutated': manifest_sha(mutated) if mutated else None,
                                     'restored': manifest_sha(restored)}
        try:
            result['restored'] = detector(work, 'restored', assembled)
        except Exception as exc:
            result['restored_error'] = repr(exc)
    clean = all(result.get(phase, {}).get('kept') == 63 and result.get(phase, {}).get('exit') == 0
                for phase in ('pristine', 'restored'))
    if not clean or not result.get('restored_exact') or 'probe_error' in result:
        result['verdict'] = 'inconclusive'
    elif result.get('mutated', {}).get('kept', -1) > 0:
        result['verdict'] = 'survived'
    elif result.get('mutated', {}).get('kept') == 0 and result.get('mutated', {}).get('exit') == 1:
        result['verdict'] = 'killed'
    else:
        result['verdict'] = 'inconclusive'
    dump(work / 'result.json', result)
    print(json.dumps({'shape': shape, 'verdict': result['verdict'],
                      'pristine': result.get('pristine', {}).get('stdout', '').strip(),
                      'mutated': result.get('mutated', {}).get('stdout', '').strip(),
                      'restored': result.get('restored', {}).get('stdout', '').strip(),
                      'restored_exact': result['restored_exact']}), flush=True)
    return result


def main():
    if Path.cwd().resolve() != REPO:
        raise RuntimeError('Run only from the isolated clone')
    frozen = {str(p.relative_to(REPO)): sha(p.read_bytes()) for p in (BINDER, ASSEMBLED, REGISTRY)}
    if sha(BINDER.read_bytes()) != EXPECTED_BINDER_SHA:
        raise RuntimeError('Binding is not the frozen v4 bytes')
    spec = importlib.util.spec_from_file_location('frozen_binding_v4', BINDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    doc = json.loads(ASSEMBLED.read_bytes())
    if len(doc['entries']) != 63:
        raise RuntimeError('Unexpected entry count')
    relocated = copy.deepcopy(doc)
    trace_map = {}
    for entry in relocated['entries']:
        mapped = []
        for original in entry.get('traces') or []:
            if not original.startswith(SOURCE_ROOT):
                raise RuntimeError('Unexpected trace path ' + original)
            local = original[len(SOURCE_ROOT):]
            target = REPO / local
            receipt = json.loads(target.read_bytes())
            basename = target.name
            prior = trace_map.get(basename)
            if prior is not None and prior != (local, receipt):
                raise RuntimeError('Conflicting trace basename')
            trace_map[basename] = (local, receipt)
            mapped.append(local)
        entry['traces'] = mapped
    assembled = ROOT / 'assembled-relocated.json'
    dump(assembled, relocated)
    dump(ROOT / 'entry-index.json', [{'start': e['start'], 'heading': e['heading'],
                                    'seats': e['seats']} for e in doc['entries']])
    # Only trace path spelling changes; the original frozen assembly remains byte untouched.
    dump(ROOT / 'relocation.json', {'original_assembled_sha256': sha(ASSEMBLED.read_bytes()),
                                   'relocated_assembled_sha256': sha(assembled.read_bytes()),
                                   'path_replacements': len(trace_map),
                                   'source_prefix': SOURCE_ROOT, 'destination_repo': str(REPO)})
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda shape: one_shape(shape, mod, assembled, trace_map), SHAPES))
    after = {str(p.relative_to(REPO)): sha(p.read_bytes()) for p in (BINDER, ASSEMBLED, REGISTRY)}
    result = {'frozen_inputs_before': frozen, 'frozen_inputs_after': after,
              'frozen_inputs_unchanged': frozen == after,
              'source_copy_hashes': hashes(PRISTINE), 'trace_basenames': len(trace_map),
              'results': results}
    dump(ROOT / 'results.json', result)
    print('frozen_inputs_unchanged=' + str(frozen == after).lower(), flush=True)
    return 0 if frozen == after and all(r['restored_exact'] for r in results) else 2


if __name__ == '__main__':
    sys.exit(main())
