#!/usr/bin/env python3
"""Replay the identical summary regression with a location-correct tool fixture."""
import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--source', required=True)
p.add_argument('--runner', required=True)
a = p.parse_args()
with tempfile.TemporaryDirectory(prefix='tameshi-r13-producer-oracle-') as d:
    tools = pathlib.Path(d) / 'tools'
    tools.mkdir()
    shutil.copyfile(a.source, tools / 'bash-witness-study.py')
    shutil.copyfile(a.runner, tools / 'mutate-and-run.sh')
    result = subprocess.run([sys.executable, str(tools / 'bash-witness-study.py'), 'selftest'])
    sys.exit(result.returncode)
