#!/usr/bin/env python3
"""Round-39 C2 counter — F4 write-path census with a real write fixture.

Contract: C2_R39_PASS=true iff the committed census tool's sha256 equals the
contract pin, its selftest reports planted_unflagged=1 planted_flagged=0
planted_scratch=0 fixture_wrote=1, the same selftest fails after the FLAG_GATE
early-return is removed, and all 21 frozen gates are classified from REV bytes.
A missing tool is the do-nothing control and cannot pass.

Exit codes: 0 pass · 1 fail · 2 usage or unreadable revision.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

TOOL = 'tools/write-path-census.py'
MARKER = 'return False  # FLAG_GATE'
GATES = 21


def git_show(lane, rev, path):
    proc = subprocess.run(
        ['git', '-C', lane, 'show', '%s:%s' % (rev, path)],
        capture_output=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


def emit(fields, ok):
    body = ' '.join('%s=%s' % (k, v) for k, v in fields)
    print('C2_R39: %s C2_R39_PASS=%s' % (body, 'true' if ok else 'false'))
    return 0 if ok else 1


def run_tool(path, args):
    proc = subprocess.run([sys.executable, path, *args], capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def parse_selftest(stdout):
    for line in stdout.splitlines():
        if line.startswith('WRITE_CENSUS_SELFTEST:'):
            fields = {}
            for part in line.split()[1:]:
                if '=' in part:
                    k, v = part.split('=', 1)
                    fields[k] = v
            return fields
    return {}


def main():
    ap = argparse.ArgumentParser(description='round-39 C2 census counter')
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    args = ap.parse_args()
    blob = git_show(args.lane, args.rev, TOOL)
    contract_blob = git_show(args.lane, args.rev, '.ufo/evidence/round-39/contract.json')
    if blob is None:
        return emit([
            ('tool_absent', 1),
            ('gates', '0/%d' % GATES),
            ('planted_unflagged', 0),
            ('planted_flagged', 0),
            ('planted_scratch', 0),
            ('fixture_wrote', 0),
            ('mutant_killed', 0),
            ('rev', args.rev),
        ], False)
    pin = None
    if contract_blob is not None:
        try:
            pin = json.loads(contract_blob.decode('utf-8'))['claims']['C2']['tool_sha256']
        except (json.JSONDecodeError, KeyError, TypeError):
            pin = None
    digest = hashlib.sha256(blob).hexdigest()
    sha_ok = int(pin == digest)
    text = blob.decode('utf-8')
    with tempfile.TemporaryDirectory(prefix='c2-r39-') as tmp:
        tool = os.path.join(tmp, 'write-path-census.py')
        with open(tool, 'w', encoding='utf-8') as fh:
            fh.write(text)
        os.chmod(tool, 0o755)
        spec = importlib.util.spec_from_file_location('write_path_census_rev', tool)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        names = list(mod.GATES)
        root = os.path.join(tmp, 'lane')
        os.makedirs(os.path.join(root, 'tools'))
        missing = 0
        for name in names:
            gate = git_show(args.lane, args.rev, 'tools/%s' % name)
            if gate is None:
                missing += 1
                continue
            with open(os.path.join(root, 'tools', name), 'wb') as fh:
                fh.write(gate)
        rc, out, err = run_tool(tool, ['--selftest'])
        fields = parse_selftest(out)
        rc_c, out_c, _err_c = run_tool(tool, ['--census', root])
        classified = 0
        live_write_sites = 0
        live_unflagged = 0
        for line in out_c.splitlines():
            if line.startswith('WRITE_CENSUS:'):
                parts = dict(
                    item.split('=', 1) for item in line.split()[1:] if '=' in item
                )
                classified = int(parts.get('gates', '0/0').split('/')[0])
                live_write_sites = int(parts.get('live_write_sites', '0'))
                live_unflagged = int(parts.get('live_unflagged', '0'))
        mutant = text.replace(MARKER, 'update = True  # FLAG_GATE', 1)
        mutant_path = os.path.join(tmp, 'mutant.py')
        with open(mutant_path, 'w', encoding='utf-8') as fh:
            fh.write(mutant)
        rc_m, out_m, _err_m = run_tool(mutant_path, ['--selftest'])
        mutant_killed = int(rc_m != 0 and MARKER not in mutant)
    planted_ok = (
        fields.get('planted_unflagged') == '1'
        and fields.get('planted_flagged') == '0'
        and fields.get('planted_scratch') == '0'
        and fields.get('fixture_wrote') == '1'
        and rc == 0
    )
    gates_ok = classified == GATES and missing == 0 and len(names) == GATES
    ok = planted_ok and mutant_killed == 1 and sha_ok == 1 and gates_ok
    return emit([
        ('tool_absent', 0),
        ('tool_sha_ok', sha_ok),
        ('gates', '%d/%d' % (classified, GATES)),
        ('live_write_sites', live_write_sites),
        ('live_unflagged', live_unflagged),
        ('planted_unflagged', fields.get('planted_unflagged', '0')),
        ('planted_flagged', fields.get('planted_flagged', '0')),
        ('planted_scratch', fields.get('planted_scratch', '0')),
        ('fixture_wrote', fields.get('fixture_wrote', '0')),
        ('mutant_killed', mutant_killed),
        ('rev', args.rev),
    ], ok)


if __name__ == '__main__':
    sys.exit(main())
