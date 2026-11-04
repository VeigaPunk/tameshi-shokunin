#!/usr/bin/env python3
"""gen-receipts-r79.py — regenerate the round-79 receipts at the landing rev.

Every receipt this round carries the lane's receipt-header convention
(`# receipt:`, `# measured_rev:`, `# tool:`, `# tool_sha256:`, `# at_utc:`), so
`tools/receipt-bytes-bind.py` measures it: the named revision must carry the
recorded tool sha (criterion 130). The design-phase receipts used
`# design_base:`/`# design_tool:` headers instead, because their bytes were
uncommitted at the time; this generator is the post-landing pass.

Usage:
  python3 -I -X utf8 .ufo/evidence/round-79/gen-receipts-r79.py <lane> <rev>
"""
import hashlib
import os
import subprocess
import sys

LANE = os.path.abspath(sys.argv[1])
REV = sys.argv[2]
EV = os.path.join(LANE, '.ufo', 'evidence', 'round-79')
WORK = os.environ.get('TMPDIR') or '/fast/scratch/hyaku/tameshi-r79'
SCRATCH = os.path.join(WORK, 'l1')


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    with open(path, 'rb') as fh:
        return sha_bytes(fh.read())


def blob(rev, path):
    proc = subprocess.run(['git', '-C', LANE, 'cat-file', 'blob',
                           '%s:%s' % (rev, path)],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise SystemExit('blob-absent: %s:%s' % (rev, path))
    return proc.stdout


def run(cmd):
    proc = subprocess.run(cmd, shell=True, cwd=LANE, capture_output=True,
                          text=True, env={**os.environ})
    return proc.stdout + proc.stderr, proc.returncode


def receipt(name, tool, body, rc, extra=''):
    header = ('# receipt: %s\n# measured_rev: %s\n# tool: %s\n'
              '# tool_sha256: %s\n# at_utc: %s\n# rc: %d\n'
              % (name, REV, tool, sha_bytes(blob(REV, tool)),
                 subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'],
                                capture_output=True, text=True).stdout.strip(),
                 rc))
    with open(os.path.join(EV, name + '.txt'), 'w') as fh:
        fh.write(header + extra + body)
    print('wrote %s rc=%d' % (name, rc))


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    # C1
    out, rc = run('python3 -I -X utf8 tools/receipt-bytes-bind.py --selftest')
    receipt('c1-selftest', 'tools/receipt-bytes-bind.py', out, rc)
    out, rc = run('python3 -I -X utf8 tools/receipt-bytes-bind.py --repo . '
                  '--root .ufo/evidence/round-78')
    receipt('c1-landed-sweep', 'tools/receipt-bytes-bind.py', out, rc)
    out, rc = run('python3 -I -X utf8 tools/receipt-bytes-bind.py --repo . '
                  '--root .ufo/evidence')
    receipt('c1-standing-sweep', 'tools/receipt-bytes-bind.py', out, rc)
    # C2
    out, rc = run('python3 -I -X utf8 tools/wave-reconcile.py --selftest')
    receipt('c2-landed-selftest', 'tools/wave-reconcile.py', out, rc)
    battery = ('bash tools/mutate-and-run.sh --target tools/wave-reconcile.py '
               '--defects tools/wave-reconcile-mutants.spec '
               '--suite \'python3 -I -X utf8 "$MUTANT" --selftest\' '
               '--workdir %s/battery-final --label wave-reconcile-arms-r79'
               % SCRATCH)
    out, rc = run(battery)
    receipt('c2-landed-battery', 'tools/wave-reconcile.py', out, rc,
            extra='# command: %s\n' % battery)
    # C3
    out, rc = run('python3 -I -X utf8 tools/selfstate-freshness.py --selftest')
    receipt('c3-landed-selftest', 'tools/selfstate-freshness.py', out, rc)
    battery = ('bash tools/mutate-and-run.sh --target tools/selfstate-freshness.py '
               '--defects tools/selfstate-freshness-mutants.spec '
               '--suite \'python3 -I -X utf8 "$MUTANT" --selftest\' '
               '--workdir %s/battery-ss-final --label selfstate-arms-r79'
               % SCRATCH)
    out, rc = run(battery)
    receipt('c3-landed-battery', 'tools/selfstate-freshness.py', out, rc,
            extra='# command: %s\n' % battery)
    # standing sweeps
    out, rc = run('python3 -I -X utf8 tools/wave-reconcile.py --repo . '
                  '--extra-root fleet=/home/vgpnk/Projects/shokunin '
                  '--manifest tools/wave-reconcile.json')
    receipt('standing-sweep-wr-r79', 'tools/wave-reconcile.py', out, rc)
    out, rc = run('python3 -I -X utf8 tools/selfstate-freshness.py --repo . '
                  '--doc-rev %s' % REV)
    receipt('standing-sweep-ss-r79', 'tools/selfstate-freshness.py', out, rc)
    # coldread at the landing rev
    out, rc = run('python3 -I tools/coldread-precheck-portable.py --repo . '
                  '--rev %s --work %s/coldread-landing' % (REV, SCRATCH))
    receipt('coldread-landing', 'tools/coldread-precheck-portable.py', out, rc)
    print('done')


if __name__ == '__main__':
    main()
