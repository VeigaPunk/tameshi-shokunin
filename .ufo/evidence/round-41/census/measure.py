#!/usr/bin/env python3
"""Round-41 C2 counter — write-path census v3 destination resolution.

Frozen before any seat scored and before the deciding run. Predicate, one
sentence: C2_R41_PASS is true iff the committed v3 tool matches its contract
pin, the round-40 v2 pin is unchanged, v3's selftest exits 0 with all four
planted fixtures at their declared values, v2's own patterns resolve none of
the two new planted classes, both live variable-destination sites in
tools/repeat-control.py resolve to an expected-value path under v3 while v2
records no expected-value destination on the same lines, and both
recognizer-removal mutants make the v3 selftest fail.

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

TOOL = 'tools/write-path-census-v3.py'
V2 = 'tools/write-path-census-v2.py'
FIXTURES = '.ufo/evidence/round-41/census/fixtures.json'
CONTRACT = '.ufo/evidence/round-41/contract.json'
LIVE = 'tools/repeat-control.py'
V2_SHA = '4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b'

RESOLVE_MARK = '        bound = env.get(node.id)'
RESOLVE_MUTANT = '        bound = None'
SYMLINK_MARK = "    if dotted == 'os.symlink':"
SYMLINK_MUTANT = "    if dotted == 'os.symlink_DISABLED':"

V2_WRITE_RE = re.compile(
    r"""open\s*\([^)]*['"](?:w|a|w\+|a\+|wb|ab)['"]"""
    r"""|\.write_text\s*\("""
    r"""|\.write_bytes\s*\("""
    r"""|os\.replace\s*\("""
    r"""|os\.rename\s*\("""
)
V2_EXPECTED_RE = re.compile(
    r"""['"][^'"]*(?:\.expected\b|expected\.txt|expected\.json|golden|snapshot)[^'"]*['"]"""
)

TARGET = {
    'var_unflagged': 1,
    'var_expected': 1,
    'symlink_unflagged': 1,
    'symlink_expected': 1,
    'literal_unflagged': 1,
    'scratch_var_unflagged': 0,
}


def git_show(lane, rev, path):
    proc = subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (rev, path)], capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def emit(tag, fields, ok):
    body = ' '.join('%s=%s' % (k, v) for k, v in fields)
    print('%s: %s %s_PASS=%s' % (tag, body, tag, 'true' if ok else 'false'))
    return 0 if ok else 1


def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fixture_fields(mod, fixtures):
    fields = {}
    for name in ('var_unflagged', 'symlink_unflagged', 'literal_unflagged', 'scratch_var'):
        summary = mod.summarize(mod.classify_source(fixtures[name]))
        if name == 'scratch_var':
            fields['scratch_var_unflagged'] = summary['unflagged']
        else:
            fields['%s_unflagged' % name.split('_')[0]] = summary['unflagged']
            fields['%s_expected' % name.split('_')[0]] = summary['expected_sites']
    return fields


def v2_fixture_misses(fixtures):
    """v2 patterns on the two new planted classes: a resolution miss, not a site miss."""
    var_expected = 0
    for line in fixtures['var_unflagged'].splitlines():
        if V2_WRITE_RE.search(line) and V2_EXPECTED_RE.search(line):
            var_expected += 1
    symlink_sites = 0
    for line in fixtures['symlink_unflagged'].splitlines():
        if V2_WRITE_RE.search(line):
            symlink_sites += 1
    return var_expected, symlink_sites


def control(lane, fixtures_path):
    with open(fixtures_path, encoding='utf-8') as handle:
        fixtures = json.load(handle)
    var_expected, symlink_sites = v2_fixture_misses(fixtures)
    meets = var_expected == TARGET['var_expected'] and symlink_sites == 0
    return emit(
        'C2_R41_CONTROL',
        [('v2_var_expected', var_expected), ('v2_symlink_sites', symlink_sites)],
        meets,
    )


def main():
    parser = argparse.ArgumentParser(description='round-41 C2 census-v3 counter')
    parser.add_argument('--lane', required=True)
    parser.add_argument('--rev', default='')
    parser.add_argument('--control', action='store_true')
    parser.add_argument('--fixtures', default='')
    args = parser.parse_args()
    if args.control:
        path = args.fixtures or os.path.join(args.lane, FIXTURES)
        return control(args.lane, path)
    if not args.rev:
        print('rev required unless --control', file=sys.stderr)
        return 2

    blob = git_show(args.lane, args.rev, TOOL)
    if blob is None:
        return emit(
            'C2_R41',
            [
                ('tool_absent', 1),
                ('var_expected', 0),
                ('symlink_expected', 0),
                ('rev', args.rev),
            ],
            False,
        )
    digest = hashlib.sha256(blob).hexdigest()
    contract_blob = git_show(args.lane, args.rev, CONTRACT)
    pin = None
    if contract_blob is not None:
        try:
            pin = json.loads(contract_blob.decode('utf-8'))['claims']['C2']['tool_sha256']
        except (json.JSONDecodeError, KeyError, TypeError, UnicodeDecodeError):
            pin = None
    sha_ok = int(pin == digest)

    v2_blob = git_show(args.lane, args.rev, V2)
    v2_sha_ok = int(v2_blob is not None and hashlib.sha256(v2_blob).hexdigest() == V2_SHA)
    fix_blob = git_show(args.lane, args.rev, FIXTURES)
    live_blob = git_show(args.lane, args.rev, LIVE)
    if fix_blob is None or live_blob is None:
        return emit(
            'C2_R41',
            [
                ('tool_absent', 0),
                ('fixtures_or_live_absent', 1),
                ('tool_sha_ok', sha_ok),
                ('rev', args.rev),
            ],
            False,
        )
    fixtures = json.loads(fix_blob.decode('utf-8'))
    live_text = live_blob.decode('utf-8', 'replace')
    text = blob.decode('utf-8')

    with tempfile.TemporaryDirectory(prefix='c2-r41-') as tmp:
        tool_path = os.path.join(tmp, 'write-path-census-v3.py')
        with open(tool_path, 'w', encoding='utf-8') as handle:
            handle.write(text)
        fix_path = os.path.join(tmp, 'fixtures.json')
        with open(fix_path, 'wb') as handle:
            handle.write(fix_blob)
        mod = load_mod(tool_path, 'census_v3_rev')
        fields = fixture_fields(mod, fixtures)
        selftest = subprocess.run(
            [sys.executable, tool_path, '--selftest', '--fixtures', fix_path],
            capture_output=True,
            text=True,
        )
        mutant_paths = {}
        for name, old, new in (
            ('resolve', RESOLVE_MARK, RESOLVE_MUTANT),
            ('symlink', SYMLINK_MARK, SYMLINK_MUTANT),
        ):
            mutant = text.replace(old, new, 1)
            if mutant == text or old in mutant:
                mutant_paths[name] = None
                continue
            path = os.path.join(tmp, 'mutant-%s.py' % name)
            with open(path, 'w', encoding='utf-8') as handle:
                handle.write(mutant)
            mutant_paths[name] = path
        killed = {}
        for name, path in mutant_paths.items():
            if path is None:
                killed[name] = 0
                continue
            run = subprocess.run(
                [sys.executable, path, '--selftest', '--fixtures', fix_path],
                capture_output=True,
                text=True,
            )
            killed[name] = int(run.returncode != 0)

        live_records = mod.classify_source(live_text)

    live_lines = live_text.splitlines()

    def v2_line(lineno):
        line = live_lines[lineno - 1] if 0 < lineno <= len(live_lines) else ''
        return (
            int(bool(V2_WRITE_RE.search(line))),
            int(bool(V2_EXPECTED_RE.search(line))),
        )

    var_rec = None
    sym_rec = None
    for rec in live_records:
        if rec['expected'] and rec['kind'] == 'open' and 805 <= rec['lineno'] <= 815:
            var_rec = rec
        if rec['expected'] and rec['kind'] == 'os.symlink' and 815 <= rec['lineno'] <= 825:
            sym_rec = rec
    live_var_lineno = var_rec['lineno'] if var_rec else 0
    live_sym_lineno = sym_rec['lineno'] if sym_rec else 0
    live_var_resolved = int(bool(var_rec and var_rec['expected']))
    live_var_scratch = int(bool(var_rec and var_rec['scratch']))
    live_sym_resolved = int(bool(sym_rec and sym_rec['expected']))
    live_sym_scratch = int(bool(sym_rec and sym_rec['scratch']))
    live_var_sites_v2, live_var_expected_v2 = v2_line(live_var_lineno) if var_rec else (0, 0)
    live_sym_sites_v2, _ = v2_line(live_sym_lineno) if sym_rec else (0, 0)
    v2_var_expected, v2_symlink_sites = v2_fixture_misses(fixtures)

    fixtures_ok = all(fields.get(key) == value for key, value in TARGET.items())
    v2_misses = v2_var_expected == 0 and v2_symlink_sites == 0
    live_ok = (
        live_var_resolved == 1
        and live_var_scratch == 1
        and live_var_expected_v2 == 0
        and live_sym_resolved == 1
        and live_sym_scratch == 1
        and live_sym_sites_v2 == 0
    )
    ok = (
        fixtures_ok
        and v2_misses
        and live_ok
        and sha_ok == 1
        and v2_sha_ok == 1
        and selftest.returncode == 0
        and killed.get('resolve') == 1
        and killed.get('symlink') == 1
    )
    return emit(
        'C2_R41',
        [
            ('tool_absent', 0),
            ('tool_sha_ok', sha_ok),
            ('v2_sha_ok', v2_sha_ok),
            ('selftest_exit', selftest.returncode),
            ('var_unflagged', fields.get('var_unflagged', -1)),
            ('var_expected', fields.get('var_expected', -1)),
            ('symlink_unflagged', fields.get('symlink_unflagged', -1)),
            ('symlink_expected', fields.get('symlink_expected', -1)),
            ('literal_unflagged', fields.get('literal_unflagged', -1)),
            ('scratch_var_unflagged', fields.get('scratch_var_unflagged', -1)),
            ('v2_var_expected', v2_var_expected),
            ('v2_symlink_sites', v2_symlink_sites),
            ('live_var_lineno', live_var_lineno),
            ('live_var_resolved_v3', live_var_resolved),
            ('live_var_scratch_v3', live_var_scratch),
            ('live_var_sites_v2', live_var_sites_v2),
            ('live_var_expected_v2', live_var_expected_v2),
            ('live_symlink_lineno', live_sym_lineno),
            ('live_symlink_resolved_v3', live_sym_resolved),
            ('live_symlink_scratch_v3', live_sym_scratch),
            ('live_symlink_sites_v2', live_sym_sites_v2),
            ('mutant_resolve_killed', killed.get('resolve', 0)),
            ('mutant_symlink_killed', killed.get('symlink', 0)),
            ('rev', args.rev),
        ],
        ok,
    )


if __name__ == '__main__':
    sys.exit(main())
