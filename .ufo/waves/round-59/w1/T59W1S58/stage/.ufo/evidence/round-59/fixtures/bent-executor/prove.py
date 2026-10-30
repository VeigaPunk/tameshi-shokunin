#!/usr/bin/env python3
"""Read-only byte/provenance proof; never executes either executor or a counter."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess

BASE = 'b83f1bfc7b302f22e89d9631ac7e6ac87ea78c2a'
TRUSTED_BLOB = '9f9d0b7c1882ae7bf6d2917036f88c75c74c5b09'
FORGED_BLOB = 'c92668ee8189e43fd5a09924061d1dc052662966'
ATTACK = '.ufo/waves/round-58/w1/T58W1RevengerC2-receipts/attack.py'


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, type=Path)
    args = parser.parse_args()
    tree = ast.parse((args.repo / ATTACK).read_bytes())
    assignments = [n for n in tree.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'BENT_RC'
                           for t in n.targets)]
    if len(assignments) != 1:
        raise SystemExit('expected exactly one BENT_RC assignment')
    extracted = ast.literal_eval(assignments[0].value)
    fixture = Path(__file__).with_name('registry-check.py').read_bytes()
    trusted = subprocess.run(
        ['git', '-C', str(args.repo), 'show', BASE + ':tools/registry-check.py'],
        check=True, capture_output=True).stdout
    if extracted != fixture or blob(fixture) != FORGED_BLOB:
        raise SystemExit('forged fixture provenance mismatch')
    if blob(trusted) != TRUSTED_BLOB or trusted == fixture:
        raise SystemExit('trusted source identity mismatch')
    print(json.dumps({'proof': 'DECLARED_EXECUTOR_SOURCE_DRIFT',
                      'trusted_revision': BASE,
                      'declared_path': 'tools/registry-check.py',
                      'trusted_blob': blob(trusted), 'forged_blob': blob(fixture),
                      'trusted_bytes': len(trusted), 'forged_bytes': len(fixture),
                      'source_equal': False, 'gate_executed': False}, sort_keys=True))


if __name__ == '__main__':
    main()
