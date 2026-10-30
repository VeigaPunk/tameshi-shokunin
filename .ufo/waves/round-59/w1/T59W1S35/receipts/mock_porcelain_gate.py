#!/usr/bin/env python3
"""MOCK vulnerable family (receipt aid, NOT a candidate implementation):
porcelain diff gate. Passes the frozen 24-fixture counter shape; must FAIL
T59W1S35's adversarial_config_test on textconv / diff.external fixtures."""
import argparse
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--repo', required=True)
p.add_argument('--trusted', required=True)
p.add_argument('--candidate', required=True)
p.add_argument('--path', action='append', required=True)
a = p.parse_args()
rc = 0
for path in a.path:
    r = subprocess.run(['git', '-C', a.repo, 'diff', '--quiet', a.trusted, a.candidate, '--', path])
    if r.returncode == 1:
        rc = 1
    elif r.returncode != 0:
        print('EXECUTOR_SOURCE_UNAVAILABLE', file=sys.stderr)
        sys.exit(2)
print('EXECUTOR_SOURCE_BOUND' if rc == 0 else 'EXECUTOR_SOURCE_DRIFT')
sys.exit(rc)
