#!/usr/bin/env python3
"""BuildF6A — generator + reducer for the round-29 F6 (frontier F6) B5 fixture.

Everything is derived from the pinned kagi objects (read-only) and from the
FROZEN counter's own machinery (Oracle, ddmin, materialize, b5_mutant) imported
from .ufo/evidence/round-29/c2-measure-v2.py.  Nothing is reimplemented.

Two variants are produced:

  anchored  ORIGINAL census.tsv is byte-identical to the pinned kagi
            corpus/surface-census.tsv at REV_BASH (counter clause 1, first half).
            Its host manifest makes the pristine gate report drift for exactly
            one exec row whose live file lacks the execute bit.

  probe     the pinned declaration plus ONE appended probe row
            (kind=exec, declared mode 644) that carries the B5 differential:
            pristine prints "(declared exec, no execute bit)" (exit 1) while the
            B5 mutant prints "SURFACE OK (exec 644)" (exit 0).

Reduction uses the counter's own frozen ddmin() with its own Oracle.kills().

Usage:  python3 gen.py [--out DIR] [--kagi DIR] [--ctr PATH]
"""
import argparse
import hashlib
import importlib.util
import os
import re
import shutil
import sys
import time

DEFAULT_CTR = '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/c2-measure-v2.py'
DEFAULT_KAGI = '/home/vgpnk/Projects/shokunin/kagi-shokunin'
DEFAULT_LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FILES = ('census.tsv', 'shapes.tsv', 'baseline.tsv', 'host.tsv')

# The exec row whose live file loses the execute bit (variant "anchored").
BROKEN_EXEC = '$HOME/.config/the-janitor/client.py'
# Probe row for variant "probe": declared mode == live mode, so the mutant's
# mode check stays silent while the pristine's x-bit arm fires.
PROBE_ROW = ('$HOME/.local/bin/b5-probe\tasset\texec\t644\t'
             'F6 probe row: declared mode 644, live file lacks the execute bit')
PROBE_REL = '.local/bin/b5-probe'

# Shapes rows kept: verbatim lines of the pinned state-shape.tsv whose target is
# absent at run time (SHAPE ABSENT is informational) or whose single mode
# assertion matches the live file.  No sqlite/keys assertion is kept, so the
# fixture needs neither sqlite3 nor a JSON body.
SHAPE_KEEP = (
    '$STATE/client.lock\tlock\tmode\t600\t',
    '$STATE/session-id\tmarker\tmode\t600\t',
    '$STATE/xdg-data/opencode/opencode.db\tsqlite\tmode\t600\t',
    '$STATE/xdg-cache/opencode/models.json\tjson\tmode\t600\t',
    '$STATE/xdg-data/opencode/log/opencode.log\tlog\tmode\t600\t',
    '$HOME/.local/state/tac/handoff-status.json\tjson\tmode\t600\t',
)


def load_counter(path):
    spec = importlib.util.spec_from_file_location('c2v2', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out'))
    ap.add_argument('--kagi', default=DEFAULT_KAGI)
    ap.add_argument('--ctr', default=DEFAULT_CTR)
    ap.add_argument('--lane', default=DEFAULT_LANE)
    ap.add_argument('--lane-rev', default='HEAD')
    a = ap.parse_args()

    c2 = load_counter(a.ctr)
    print('counter bytes sha256 =', hashlib.sha256(open(a.ctr, 'rb').read()).hexdigest())

    runner = (c2.show(a.lane, a.lane_rev, 'tools/mutate-and-run.sh') or b'').decode()
    pin = re.search(r'^PIN_BASH=([0-9a-f]{64})$', runner, re.M).group(1)
    rev_bash = re.search(r'^REV_BASH=([0-9a-f]{40})$', runner, re.M).group(1)
    print('PIN_BASH  =', pin)
    print('REV_BASH  =', rev_bash)

    census_bytes = c2.show(a.kagi, rev_bash, 'corpus/surface-census.tsv')
    shapes_bytes = c2.show(a.kagi, rev_bash, 'corpus/state-shape.tsv')
    baseline_bytes = c2.show(a.kagi, rev_bash, 'corpus/drift-baseline.tsv')
    gate = c2.show(a.kagi, rev_bash, 'corpus/surface-census.sh')
    assert hashlib.sha256(gate).hexdigest() == pin, 'pinned gate digest mismatch'
    mutant = c2.b5_mutant(runner, gate.decode())
    assert mutant is not None, 'B5 spec does not apply exactly once'
    print('mutant    sha256 =', hashlib.sha256(mutant.encode()).hexdigest())

    census_lines = c2.lines_of(census_bytes)
    shapes_lines = c2.lines_of(shapes_bytes)
    baseline_lines = c2.lines_of(baseline_bytes)
    scan_dirs = [l.split('\t')[1][len('$HOME/'):] for l in census_lines if l.startswith('# scan\t')]
    exec_rows = [l for l in census_lines if '\texec\t' in l and not l.startswith('#')]

    def pick_shapes():
        return [l for l in shapes_lines if any(l.startswith(p) for p in SHAPE_KEEP)]

    def host_manifest(variant):
        """host.tsv lines: <rel path>\\t<dir|file>\\t<octal mode>\\t<content>"""
        rows = []
        seen = set()

        def add(rel, kind, mode, content=''):
            if rel in seen:
                return
            seen.add(rel)
            rows.append('%s\t%s\t%s\t%s' % (rel, kind, mode, content))

        for l in census_lines:
            if not l or l.startswith('#'):
                continue
            f = l.split('\t')
            if len(f) < 4 or not f[0].startswith('$HOME/') or f[1] != 'asset':
                continue
            path, kind, mode = f[0], f[2], f[3]
            rel = path[len('$HOME/'):]
            if kind == 'dir':
                add(rel, 'dir', '755' if mode == '-' else mode)
            else:
                add(rel, 'file', '644' if mode == '-' else mode, 'F6 fixture placeholder')
        # every # scan dir must exist, even the ones whose census row is runtime
        for d in scan_dirs:
            add(d, 'dir', '700')
        # xdg-data is the parent of the scanned xdg-data/opencode dir
        add('.local/state/the-janitor/xdg-data', 'dir', '700')
        if variant == 'anchored':
            # the file that loses its execute bit (declared 755, live 644)
            add(BROKEN_EXEC[len('$HOME/'):], 'file', '644', 'F6 fixture placeholder')
        else:
            # every pinned exec row stays clean; the probe row carries the kill
            add(PROBE_REL, 'file', '644', 'F6 probe placeholder')
        return rows

    def fixture(variant):
        census = list(census_lines)
        if variant == 'probe':
            census = census + [PROBE_ROW]
        return {
            'census.tsv': census,
            'shapes.tsv': pick_shapes(),
            'baseline.tsv': list(baseline_lines),
            'host.tsv': host_manifest(variant),
        }

    def write_fixture(d, fx, exact_census_bytes=None):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        for name in FILES:
            with open(os.path.join(d, name), 'w', encoding='utf-8', errors='surrogateescape') as h:
                h.write(''.join(l + '\n' for l in fx[name]))
        if exact_census_bytes is not None:
            with open(os.path.join(d, 'census.tsv'), 'wb') as h:
                h.write(exact_census_bytes)

    work = os.path.join(a.out, 'work')
    shutil.rmtree(a.out, ignore_errors=True)
    os.makedirs(work)
    open(os.path.join(work, 'pristine.sh'), 'wb').write(gate)
    open(os.path.join(work, 'mutant-B5.sh'), 'w').write(mutant)
    orc = c2.Oracle(os.path.join(work, 'pristine.sh'), os.path.join(work, 'mutant-B5.sh'), work)

    summary = []
    for variant, sub in (('anchored', ''), ('probe', 'probe/')):
        fx = fixture(variant)
        d = os.path.join(a.out, sub + 'original')
        write_fixture(d, fx, exact_census_bytes=(census_bytes if variant == 'anchored' else None))
        units = c2.to_units(fx)
        n0 = orc.n
        t0 = time.time()
        kill = orc.kills(units)
        t_kill = time.time() - t0
        t0 = time.time()
        got = c2.ddmin(units, orc.kills)
        t_dd = time.time() - t0
        mini = c2.from_units(got)
        write_fixture(os.path.join(a.out, sub + 'minimized'), mini)
        one_min = 1
        for k in range(len(got)):
            if orc.kills(got[:k] + got[k + 1:]):
                one_min = 0
                print('   NOT 1-minimal: removable %r' % (got[k],))
                break
        print('== variant %-8s units_original=%d kills=%s ddmin_units=%d one_minimal=%d '
              'oracle_tests=%d wall_kill=%.1fs wall_ddmin=%.1fs'
              % (variant, len(units), kill, len(got), one_min, orc.n - n0, t_kill, t_dd))
        summary.append((variant, len(units), len(got), orc.n - n0, one_min, kill))
    print()
    for s in summary:
        print('SUMMARY variant=%s units_original=%d units_minimized=%d oracle_tests=%d one_minimal=%d kills=%s' % s)
    print('pinned census sha256 =', hashlib.sha256(census_bytes).hexdigest())
    print('pinned census bytes  =', len(census_bytes))
    print('pinned exec rows     =', len(exec_rows), 'declared modes',
          sorted({l.split('\t')[3] for l in exec_rows}))


if __name__ == '__main__':
    main()
