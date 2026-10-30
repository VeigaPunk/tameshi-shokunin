#!/usr/bin/env python3
"""Strawman NONconforming gate: inspects the WORKTREE file, never the candidate commit.
Used only to demonstrate the frozen counter's false-pass hazard on the 'changed' cell."""
import argparse
import os
import sys

ap = argparse.ArgumentParser()
ap.add_argument('--repo', required=True)
ap.add_argument('--trusted', required=True)
ap.add_argument('--candidate', required=True)
ap.add_argument('--path', required=True)
a = ap.parse_args()

try:
    with open(os.path.join(a.repo, a.path), 'rb') as fh:
        fh.read()
except OSError:
    print('EXECUTOR_SOURCE_DRIFT')
    sys.exit(1)
print('EXECUTOR_SOURCE_BOUND')
sys.exit(0)
