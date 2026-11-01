#!/usr/bin/env python3
"""probe-arms.py — round-62 fail-closed arms for the portable precheck's
spawn-equivalence probe (routed defect RD1, r61 verifier spot-check).

One fixture (the r61 differential builder, `build_repo`), one harness, and
the ONLY delta between the "base" and "new" tool bytes is the probe guard.
Arm-liveness rule (considerthese 2026-10-28 proposal 2, adopted): every arm
carries a committed input that moves the outcome it is named for.

  ARM-VACUOUS   drive main() with the exact dict the REAL probe returns for
                an EMPTY candidate set (captured from the real function at
                runtime), floor == cand so the verdict arm is `ok`:
                base bytes must exit 0 — the vacuous pass IS the defect;
                new bytes must exit 2 — the guard fails the run.
  ARM-MISMATCH  end-to-end through the CLI: populate the resume cache, then
                tamper one chunk AND its manifest sha256, re-run: the probe
                must report mismatches >= 1 and the run must exit 2 on BOTH
                byte versions (the pre-existing mismatch gate, intact).
  ARM-CLEAN     untampered end-to-end CLI run on the new bytes: probe
                mismatches = 0 on both revisions (the fixture's own verdict
                RED at cand is its drift design, not a probe failure).

The empty-candidate scenario is unreachable through the CLI on a valid repo
(the ledger is always prefetched and tracked, so candidates are non-empty);
ARM-VACUOUS therefore exercises main()'s gate at the function level —
disclosed here and in the round lesson.

Usage:
  python -I probe-arms.py --lane LANE --tool-base BASE.py --tool-new NEW.py

Exit 0 when every arm lands on its expected outcome; 1 otherwise.
"""
import argparse
import base64
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

sys.dont_write_bytecode = True


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def run_cli(tool, repo, floor, cand, work):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    return subprocess.run(
        [sys.executable, '-I', str(tool), '--repo', str(repo),
         '--floor', floor, '--cand', cand, '--work', str(work)],
        capture_output=True, env=env)


def tamper(work, rev):
    """Corrupt one cached blob AND its manifest sha so the resume path
    loads the tampered chunk as valid."""
    rev_dir = work / ('rev-%s' % rev[:12])
    mpath = rev_dir / 'manifest.json'
    manifest = json.loads(mpath.read_text(encoding='utf-8'))
    chunk_path = rev_dir / 'chunk-0000.json'
    raw = chunk_path.read_bytes()
    data = json.loads(raw.decode('ascii'))
    key = 'SHONEN.md' if 'SHONEN.md' in data else sorted(data)[0]
    body = base64.b64decode(data[key])
    data[key] = base64.b64encode(b'PROBE-ARMS-TAMPERED\n' + body).decode('ascii')
    tampered = json.dumps(data, sort_keys=True).encode('ascii')
    chunk_path.write_bytes(tampered)
    entry = manifest.get('0000', {})
    manifest['0000'] = {'specs': entry.get('specs', 0),
                        'sha256': hashlib.sha256(tampered).hexdigest()}
    mpath.write_text(json.dumps(manifest, sort_keys=True), encoding='utf-8')
    return key


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--tool-base', required=True)
    ap.add_argument('--tool-new', required=True)
    a = ap.parse_args()
    lane = Path(a.lane)
    diff_src = lane / '.ufo/evidence/round-61/win-host/differential.py'
    diffs = load_module('tameshi_r61_differential', diff_src)
    results = []
    ok = True
    with tempfile.TemporaryDirectory(prefix='tameshi-r62-arms-') as tmp:
        root = Path(tmp)
        repo, rev1, rev2, skill_raw = diffs.build_repo(root)
        print('FIXTURE rev1=%s rev2=%s (builder: r61 differential.build_repo)'
              % (rev1[:12], rev2[:12]))
        for tag, tool in (('base', Path(a.tool_base)),
                          ('new', Path(a.tool_new))):
            mod = load_module('portable_%s' % tag, tool)
            print('TOOL %s sha256=%s'
                  % (tag, hashlib.sha256(tool.read_bytes()).hexdigest()))
            fmod = mod.load_frozen(str(repo))
            # the REAL probe's empty-candidate outcome, captured, not assumed
            probe0 = mod.equivalence_probe(fmod, str(repo), rev1,
                                           fmod.cat_file_blob,
                                           fmod.ls_tree_mode, {}, {}, 40, 61)
            if tag == 'base':
                print('REAL-PROBE-EMPTY-CANDIDATES %r' % (probe0,))
                if probe0.get('sampled') != 0 or probe0.get('mismatches') != 0:
                    print('ARM-VACUOUS-PREMISE FAIL: real probe on an empty '
                          'candidate set did not return sampled=0/mismatches=0')
                    ok = False
            mod.equivalence_probe = lambda *args, **kw: dict(probe0)
            out = io.StringIO()
            with redirect_stdout(out):
                code = mod.main(['--repo', str(repo), '--floor', rev1,
                                 '--cand', rev1,
                                 '--work', str(root / ('vwork-%s' % tag))])
            verdict = ('VACUOUS-PASS (empty sample did not fail the run)'
                       if code == 0 else 'GUARD-FIRED (fail-closed)')
            print('ARM-VACUOUS tool=%s exit=%d %s' % (tag, code, verdict))
            for line in out.getvalue().splitlines():
                print('  %s' % line)
            expect = 0 if tag == 'base' else 2
            results.append(('vacuous', tag, code == expect))
        for tag, tool in (('base', Path(a.tool_base)),
                          ('new', Path(a.tool_new))):
            work = root / ('mwork-%s' % tag)
            work.mkdir()
            r1 = run_cli(tool, repo, rev1, rev2, work)
            if r1.returncode not in (0, 1):
                print('ARM-MISMATCH tool=%s SETUP-FAIL exit=%d %s'
                      % (tag, r1.returncode,
                         r2_stderr(r1)[:200]))
                ok = False
                continue
            key = tamper(work, rev1)
            r2 = run_cli(tool, repo, rev1, rev2, work)
            stdout = r2.stdout.decode('utf-8', 'replace')
            print('ARM-MISMATCH tool=%s tampered-key=%s exit=%d'
                  % (tag, key, r2.returncode))
            for line in stdout.splitlines():
                print('  %s' % line)
            for line in r2.stderr.decode('utf-8', 'replace').splitlines():
                print('  [stderr] %s' % line)
            fired = (r2.returncode == 2 and 'mismatches=1' in stdout)
            results.append(('mismatch', tag, fired))
        work = root / 'cwork-new'
        work.mkdir()
        r3 = run_cli(Path(a.tool_new), repo, rev1, rev2, work)
        stdout = r3.stdout.decode('utf-8', 'replace')
        print('ARM-CLEAN tool=new exit=%d' % r3.returncode)
        for line in stdout.splitlines():
            print('  %s' % line)
        clean = (r3.returncode in (0, 1)
                 and 'floor_mismatches=0' in stdout
                 and 'cand_mismatches=0' in stdout)
        results.append(('clean', 'new', clean))
    for name, tag, passed in results:
        if not passed:
            ok = False
            print('ARM-FAIL %s/%s' % (name, tag))
    print('PROBE_ARMS: %s (%s)' % (
        'PASS' if ok else 'FAIL',
        ' '.join('%s/%s=%s' % (n, t, 'ok' if v else 'FAIL')
                 for n, t, v in results)))
    return 0 if ok else 1


def r2_stderr(proc):
    return proc.stderr.decode('utf-8', 'replace')


if __name__ == '__main__':
    sys.exit(main())
