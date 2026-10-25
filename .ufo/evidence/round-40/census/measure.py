#!/usr/bin/env python3
"""Round-40 C1 counter — write-form census v2.

C1_R40_PASS=true only when the committed v2 tool matches the contract pin,
the round-39 tool pin is unchanged, the planted fixtures discriminate, the
embedded v1 patterns miss both new classes, the two disclosed live sites
move from miss to hit, and both recognizer-removal mutants fail the selftest.

A missing v2 tool is the do-nothing control and cannot pass.
--control scores the same fixtures with the embedded v1 patterns and must
not meet the v2 target.

Exit codes: 0 pass · 1 fail · 2 usage or unreadable revision.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

TOOL = 'tools/write-path-census-v2.py'
V1 = 'tools/write-path-census.py'
FIXTURES = '.ufo/evidence/round-40/census/fixtures.json'
CONTRACT = '.ufo/evidence/round-40/contract.json'
V1_SHA = 'bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62'
REPLACE_MARK = r'os\.replace\s*\('
JSON_MARK = 'expected\\.json'

V1_WRITE_RE = re.compile(
    r"""open\s*\([^)]*['"](?:w|a|w\+|a\+|wb|ab)['"]"""
    r"""|\.write_text\s*\("""
    r"""|\.write_bytes\s*\("""
)
V1_EXPECTED_RE = re.compile(
    r"""['"][^'"]*(?:\.expected\b|expected\.txt|golden|snapshot)[^'"]*['"]"""
)
V1_SCRATCH_RE = re.compile(r'/tmp/|tempfile|TemporaryDirectory|NamedTemporaryFile|\bscratch\b')
V1_FLAG_RE = re.compile(r'--update_goldens|--update-goldens|--update\b|update_goldens')


def git_show(lane, rev, path):
    proc = subprocess.run(
        ['git', '-C', lane, 'show', '%s:%s' % (rev, path)],
        capture_output=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


def emit(tag, fields, ok):
    body = ' '.join('%s=%s' % (k, v) for k, v in fields)
    print('%s: %s %s=%s' % (tag, body, tag + '_PASS', 'true' if ok else 'false'))
    return 0 if ok else 1


def v1_classify(text):
    flagged = V1_FLAG_RE.search(text) is not None
    writes = 0
    unflagged = 0
    for line in text.splitlines():
        if V1_WRITE_RE.search(line) is None:
            continue
        writes += 1
        if V1_EXPECTED_RE.search(line) and V1_SCRATCH_RE.search(line) is None and not flagged:
            unflagged += 1
    return writes, unflagged


def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_selftest(stdout):
    for line in stdout.splitlines():
        if line.startswith('WRITE_CENSUS_V2_SELFTEST:'):
            fields = {}
            for part in line.split()[1:]:
                if '=' in part:
                    k, v = part.split('=', 1)
                    fields[k] = v
            return fields
    return {}


def control(fixture_path):
    with open(fixture_path, encoding='utf-8') as fh:
        planted = json.load(fh)
    bytes_u = v1_classify(planted['bytes_unflagged'])[1]
    replace_w = v1_classify(planted['replace_unflagged'])[0]
    # The v2 target is both new classes at 1. v1 cannot reach it.
    meets = bytes_u == 1 and replace_w >= 1 and v1_classify(planted['replace_unflagged'])[1] == 1
    return emit('C1_R40_CONTROL', [
        ('v1_bytes_unflagged', bytes_u),
        ('v1_replace_writes', replace_w),
        ('v1_replace_unflagged', v1_classify(planted['replace_unflagged'])[1]),
    ], meets)


def main():
    ap = argparse.ArgumentParser(description='round-40 C1 census-v2 counter')
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', default='')
    ap.add_argument('--control', action='store_true')
    ap.add_argument('--fixtures', default='')
    args = ap.parse_args()
    if args.control:
        path = args.fixtures or os.path.join(args.lane, FIXTURES)
        return control(path)
    if not args.rev:
        print('rev required unless --control', file=sys.stderr)
        return 2
    blob = git_show(args.lane, args.rev, TOOL)
    if blob is None:
        return emit('C1_R40', [
            ('tool_absent', 1),
            ('bytes_unflagged', 0),
            ('replace_unflagged', 0),
            ('v1_bytes_unflagged', 0),
            ('v1_replace_writes', 0),
            ('rev', args.rev),
        ], False)
    digest = hashlib.sha256(blob).hexdigest()
    contract_blob = git_show(args.lane, args.rev, CONTRACT)
    pin = None
    if contract_blob is not None:
        try:
            pin = json.loads(contract_blob.decode('utf-8'))['claims']['C1']['tool_sha256']
        except (json.JSONDecodeError, KeyError, TypeError, UnicodeDecodeError):
            pin = None
    sha_ok = int(pin == digest)
    v1_blob = git_show(args.lane, args.rev, V1)
    v1_sha_ok = int(v1_blob is not None and hashlib.sha256(v1_blob).hexdigest() == V1_SHA)
    fix_blob = git_show(args.lane, args.rev, FIXTURES)
    if fix_blob is None:
        return emit('C1_R40', [
            ('tool_absent', 0),
            ('fixtures_absent', 1),
            ('tool_sha_ok', sha_ok),
            ('rev', args.rev),
        ], False)
    planted = json.loads(fix_blob.decode('utf-8'))
    text = blob.decode('utf-8')
    with tempfile.TemporaryDirectory(prefix='c1-r40-') as tmp:
        tool = os.path.join(tmp, 'write-path-census-v2.py')
        with open(tool, 'w', encoding='utf-8') as fh:
            fh.write(text)
        fix_path = os.path.join(tmp, 'fixtures.json')
        with open(fix_path, 'wb') as fh:
            fh.write(fix_blob)
        mod = load_mod(tool, 'census_v2_rev')
        got = {name: mod.classify_text(planted[name]) for name in planted}
        rc = subprocess.run(
            [sys.executable, tool, '--selftest', '--fixtures', fix_path],
            capture_output=True, text=True,
        )
        fields = parse_selftest(rc.stdout)
        mutant_replace = text.replace(REPLACE_MARK, 'os.replace_REMOVED(', 1)
        mutant_json = text.replace(JSON_MARK, 'expected_REMOVED', 1)
        killed_replace = 0
        killed_json = 0
        if mutant_replace != text and REPLACE_MARK not in mutant_replace:
            path_m = os.path.join(tmp, 'mutant-replace.py')
            with open(path_m, 'w', encoding='utf-8') as fh:
                fh.write(mutant_replace)
            rc_m = subprocess.run(
                [sys.executable, path_m, '--selftest', '--fixtures', fix_path],
                capture_output=True, text=True,
            )
            killed_replace = int(rc_m.returncode != 0)
        if mutant_json != text and JSON_MARK not in mutant_json:
            path_j = os.path.join(tmp, 'mutant-json.py')
            with open(path_j, 'w', encoding='utf-8') as fh:
                fh.write(mutant_json)
            rc_j = subprocess.run(
                [sys.executable, path_j, '--selftest', '--fixtures', fix_path],
                capture_output=True, text=True,
            )
            killed_json = int(rc_j.returncode != 0)
    v1_bytes = v1_classify(planted['bytes_unflagged'])[1]
    v1_replace_writes = v1_classify(planted['replace_unflagged'])[0]
    replay = git_show(args.lane, args.rev, 'tools/registry-replay.py')
    witness = git_show(args.lane, args.rev, 'tools/bash-witness-study.py')
    live_json_v2 = 0
    live_json_v1 = 0
    if replay is not None:
        for line in replay.decode('utf-8', 'replace').splitlines():
            if '.write_bytes' in line and 'expected.json' in line:
                if mod.EXPECTED_RE.search(line) and mod.WRITE_RE.search(line):
                    live_json_v2 += 1
                if V1_EXPECTED_RE.search(line):
                    live_json_v1 += 1
    live_replace_v2 = 0
    live_replace_v1 = 0
    if witness is not None:
        for line in witness.decode('utf-8', 'replace').splitlines():
            if 'os.replace' not in line:
                continue
            if mod.WRITE_RE.search(line):
                live_replace_v2 += 1
            if V1_WRITE_RE.search(line):
                live_replace_v1 += 1
    planted_ok = (
        got['bytes_unflagged'][1] == 1
        and got['replace_unflagged'][1] == 1
        and got['bytes_flagged'][1] == 0
        and got['replace_flagged'][1] == 0
        and got['scratch_replace'][1] == 0
        and fields.get('bytes_unflagged') == '1'
        and fields.get('replace_unflagged') == '1'
        and rc.returncode == 0
    )
    v1_misses = v1_bytes == 0 and v1_replace_writes == 0
    live_ok = live_json_v2 >= 1 and live_json_v1 == 0 and live_replace_v2 >= 1 and live_replace_v1 == 0
    ok = (
        planted_ok
        and v1_misses
        and live_ok
        and sha_ok == 1
        and v1_sha_ok == 1
        and killed_replace == 1
        and killed_json == 1
    )
    return emit('C1_R40', [
        ('tool_absent', 0),
        ('tool_sha_ok', sha_ok),
        ('v1_sha_ok', v1_sha_ok),
        ('bytes_unflagged', got['bytes_unflagged'][1]),
        ('replace_unflagged', got['replace_unflagged'][1]),
        ('bytes_flagged', got['bytes_flagged'][1]),
        ('replace_flagged', got['replace_flagged'][1]),
        ('scratch_replace', got['scratch_replace'][1]),
        ('v1_bytes_unflagged', v1_bytes),
        ('v1_replace_writes', v1_replace_writes),
        ('live_json_v2', live_json_v2),
        ('live_json_v1', live_json_v1),
        ('live_replace_v2', live_replace_v2),
        ('live_replace_v1', live_replace_v1),
        ('mutant_replace_killed', killed_replace),
        ('mutant_json_killed', killed_json),
        ('rev', args.rev),
    ], ok)


if __name__ == '__main__':
    sys.exit(main())
