#!/usr/bin/env python3
"""Run C1 counter variants over fixtures, bounded parallelism, receipts per run."""
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r56/T56W1MutCounterArms')
LANE = S / 'lane'
RUNS = S / 'runs'
RUNS.mkdir(exist_ok=True)
ENV = {'PATH': '/usr/local/bin:/usr/bin:/bin', 'HOME': '/home/vgpnk',
       'HYAKU_SCRATCH': '/fast/scratch/hyaku', 'LANG': 'C.UTF-8'}


def one(job):
    label, counter, rev = job['label'], job['counter'], job['rev']
    work = S / 'work' / label
    if work.exists():
        subprocess.run(['rm', '-rf', str(work)], check=True)
    work.mkdir(parents=True)
    t0 = time.time()
    r = subprocess.run([sys.executable, counter, '--lane', str(LANE), '--rev', rev,
                        '--work', str(work), '--explain'],
                       capture_output=True, env=ENV, text=True, timeout=1800)
    dt = time.time() - t0
    (RUNS / (label + '.out')).write_text(r.stdout)
    (RUNS / (label + '.err')).write_text(r.stderr)
    (RUNS / (label + '.exit')).write_text('%d\n' % r.returncode)
    (RUNS / (label + '.meta')).write_text(json.dumps(
        {'label': label, 'counter': counter, 'rev': rev, 'exit': r.returncode,
         'seconds': round(dt, 1),
         'counter_sha256': __import__('hashlib').sha256(
             Path(counter).read_bytes()).hexdigest()}, indent=2) + '\n')
    verdict = [l for l in r.stdout.splitlines() if l.startswith('C1_R56:')]
    return {'label': label, 'exit': r.returncode, 'seconds': round(dt, 1),
            'verdict': verdict[-1] if verdict else '(no verdict line)',
            'stderr_tail': r.stderr.strip().splitlines()[-1:] }


def main():
    jobs = json.loads(Path(sys.argv[1]).read_text())
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for res in pool.map(one, jobs):
            print(json.dumps(res))
    return 0


if __name__ == '__main__':
    sys.exit(main())
