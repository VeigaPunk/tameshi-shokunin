#!/usr/bin/env python3
"""Round-48 C1 control harness: build one committed tree per contract control and run the
round-48 C1 counter on each.

Frozen predicate exercised (contract C1, amendment 3):
  C1_R48_PASS=true iff self_pin=1 stmts_pin=1 statements=22 rounds=3 append_only=1
  unpinned=0 total=0, where total = mismatches + unparsed + unobservable + dep_mismatch
  + unpinned + unattested + oversize over the 22 frozen statements of
  .ufo/evidence/round-47/calibration/statements.json.

Controls, as pre-registered in the contract (C1 `do_nothing_control`, `cheapest_controls`):
  CTL_A  base unchanged -> must print C1_R48_PASS=false (no row carries `runs 3`);
  CTL_B  the 22 round-47 standing rows (SCORECARD.md `### Standing self-assessment — re-stated
         at round 47`: 19 capability + 3 axis rows) re-appended under a new heading with
         `, runs 3 stable` added to each evidence cell and nothing else changed -> false (the
         `six-leg regression ledger` row states the one-shot `FAIL passed=7`);
  CTL_C  superset cheat: each row declares its round-47 value plus two invented members under
         class `nondeterministic` (three members total) -> refused as unattested (unattested>0);
  CTL_D  deps-everything: each row restates its round-47 value with
         deps `bwrap,env,fleet-root,jj,node` -> dep_mismatch>0;
  CTL_E  positive control: rows taken from the counter's own `--emit` output of the run on
         CTL_A -> the counter can pass (total=0), so a false E means the counter cannot pass
         at all, not that the population is bad.

Mechanics per the seat item: each control tree is `git clone -q --shared LANE` at BASE, gets
the counter copied byte-exact to .ufo/evidence/round-48/calibration/measure.py (the counter's
self-pin path), and one SCORECARD.md append (nothing outside the appended block is edited, so
the counter's append_only check holds). Each tree is committed with a throwaway identity set
only for that commit (`-c user.name` / `-c user.email`; no repository or global config is
written), after `git rev-parse --show-toplevel` is checked to be the clone itself. The counter
is then run on the tree as `--lane TREE --rev HEAD --base BASE --work EMPTY_DIR`.

Seat bounds: this script clones and commits only under --work (the seat's scratch tree). It
never touches the lane checkout, the fleet repo, /tmp, the lane's jj state or its Git index.
TMPDIR for every child is set below --work. It prints, per control, `CTL_<X> <C1_R48 line>`;
control scoring remains the L1's, so the script reports the counter's line and the tree
metadata and exits 0 when all five lines were produced (nonzero only when a tree or a counter
run produced no line at all).

Usage:
  python3 T48ExecC1Controls.run-controls.py --counter COUNTER.py --work DIR
  python3 T48ExecC1Controls.run-controls.py --counter COUNTER.py --work DIR \
      [--only depth,calibration,freshness] [--rounds N] [--jobs N]
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '473336d9d789f6081195e7376d17836a24666bc3'
COUNTER_DEST = '.ufo/evidence/round-48/calibration/measure.py'
STATEMENTS_PATH = '.ufo/evidence/round-47/calibration/statements.json'
ROUND47_HEADING = '### Standing self-assessment \u2014 re-stated at round 47'
ARROW = '\u2192'
ALL_DEPS = 'bwrap,env,fleet-root,jj,node'
CAP_HEADER = ['Capability', 'What it can now do', 'Evidence pointer', 'First-working round']
AXIS_HEADER = ['Axis', 'Score (0\u201310)', 'Evidence / counting rule', 'Measured commit',
               'Last-change round']
CAP_RE = re.compile(r'`([^`]+)`\s*' + ARROW + r'\s*`([^`]+)`\s*,\s*exit (\d+)\s*,\s*'
                    r'tool sha256 `([0-9a-f]{12})`\s*,\s*deps `([a-z,-]+)`')
DEPS_RE = re.compile(r'deps `[a-z,-]+`')
VERDICT_RE = re.compile(r'^C1_R48(_PARTIAL)?:')


class HarnessError(Exception):
    pass


def child_env(extra=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    if extra:
        env.update(extra)
    return env


def sh(argv, cwd=None, env=None):
    return subprocess.run(argv, capture_output=True, text=True, cwd=cwd,
                          env=env if env is not None else child_env())


def git(tree, *args, check=True):
    p = sh(['git', '-C', tree] + list(args))
    if check and p.returncode != 0:
        raise HarnessError('git %s failed in %s: %s' % (' '.join(args), tree, p.stderr.strip()))
    return p


def git_show(tree, spec):
    p = sh(['git', '-C', tree, 'show', spec])
    if p.returncode != 0:
        raise HarnessError('git show %s failed in %s: %s' % (spec, tree, p.stderr.strip()))
    return p.stdout


def cells_of(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def row_line(cells):
    return '| ' + ' | '.join(cells) + ' |'


def round47_rows(scorecard_text):
    """Capability and axis rows of the round-47 standing restatement, in file order."""
    lines = scorecard_text.split('\n')
    start = None
    for i, line in enumerate(lines):
        if line.startswith(ROUND47_HEADING):
            start = i
            break
    if start is None:
        raise HarnessError('heading %r absent from the base SCORECARD.md' % ROUND47_HEADING)
    end = start + 1
    while end < len(lines) and not lines[end].startswith('### '):
        end += 1
    cap, axis = [], []
    i = start
    while i < end:
        if not lines[i].startswith('|'):
            i += 1
            continue
        j = i
        while j < end and lines[j].startswith('|'):
            j += 1
        block = lines[i:j]
        header = cells_of(block[0])
        body = [b for b in block[2:] if b.strip()]
        if header and header[0] == 'Capability':
            cap.extend(cells_of(b) for b in body)
        elif len(header) > 1 and header[1].startswith('Score'):
            axis.extend(cells_of(b) for b in body)
        i = j
    return cap, axis


def add_runs(cells, cls='stable'):
    out = list(cells)
    out[2] = out[2].rstrip() + ', runs 3 ' + cls
    return out


def superset_row(cells, kind):
    """The row's round-47 value plus two invented members, class nondeterministic (CTL_C)."""
    out = list(cells)
    if kind == 'cap':
        m = CAP_RE.search(out[2])
        if m is None:
            raise HarnessError('cap evidence does not state the amendment-3 claim: %r' % out[2])
        cmd, line, code, sha, deps = m.groups()
        claim = '`%s` %s `%s`, exit %s or `%s`, exit %s or `%s`, exit %s' % (
            cmd, ARROW, line, code, line + ' [ctl-c-2]', code, line + ' [ctl-c-3]', code)
        out[2] = '%s, tool sha256 `%s`, deps `%s`, runs 3 nondeterministic' % (claim, sha, deps)
    else:
        score = int(out[1])
        invented = [v for v in (10, 0, 9, 1, 8, 2, 7, 3, 6, 4, 5) if v != score][:2]
        out[1] = '%d or %d or %d' % (score, invented[0], invented[1])
        out[2] = out[2].rstrip() + ', runs 3 nondeterministic'
    return out


def deps_everything_row(cells):
    out = add_runs(cells)
    out[2] = DEPS_RE.sub('deps `%s`' % ALL_DEPS, out[2], count=1)
    return out


def section_text(title, intro, cap_rows, axis_rows):
    lines = ['### ' + title, '', intro, '', row_line(CAP_HEADER), '|---|---|---|---|']
    lines.extend(row_line(r) for r in cap_rows)
    lines.extend(['', row_line(AXIS_HEADER), '|---|---|---|---|---|'])
    lines.extend(row_line(r) for r in axis_rows)
    return '\n'.join(lines) + '\n'


def clone_tree(work, name, lane, base):
    dest = os.path.join(work, name)
    if os.path.exists(dest):
        raise HarnessError('--work already holds %s; use an empty --work' % dest)
    p = sh(['git', 'clone', '-q', '--shared', lane, dest])
    if p.returncode != 0:
        raise HarnessError('git clone --shared %s %s failed: %s' % (lane, dest, p.stderr.strip()))
    top = git(dest, 'rev-parse', '--show-toplevel').stdout.strip()
    if os.path.realpath(top) != os.path.realpath(dest):
        raise HarnessError('toplevel %r is not the clone %r; refusing to commit' % (top, dest))
    git(dest, 'checkout', '-q', '--detach', base)
    git(dest, 'rev-parse', '--verify', base + '^{commit}')
    return dest


def append_scorecard(tree, text):
    path = os.path.join(tree, 'SCORECARD.md')
    with open(path, 'a', encoding='utf-8') as fh:
        fh.write('\n' + text)


def base_prefix_ok(tree, base):
    base_sc = git_show(tree, base + ':SCORECARD.md')
    with open(os.path.join(tree, 'SCORECARD.md'), encoding='utf-8') as fh:
        return fh.read().startswith(base_sc)


def install_counter(tree, counter):
    dest = os.path.join(tree, COUNTER_DEST)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(counter, dest)
    with open(dest, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def commit_tree(tree, message):
    git(tree, 'add', '-A')
    p = sh(['git', '-C', tree, '-c', 'user.name=tameshi-ctl',
            '-c', 'user.email=ctl@tameshi.invalid', '-c', 'commit.gpgsign=false',
            '-c', 'tag.gpgsign=false', 'commit', '-qm', message])
    if p.returncode != 0:
        raise HarnessError('commit failed in %s: %s' % (tree, p.stderr.strip()))
    return git(tree, 'rev-parse', 'HEAD').stdout.strip()


def count_runs3(tree):
    with open(os.path.join(tree, 'SCORECARD.md'), encoding='utf-8') as fh:
        text = fh.read()
    rows = 0
    runs3 = 0
    for line in text.split('\n'):
        if not line.startswith('|'):
            continue
        cells = cells_of(line)
        if cells and re.fullmatch(r'[^|]+', cells[0]):
            rows += 1
        if len(cells) > 2 and 'runs 3' in cells[2]:
            runs3 += 1
    return runs3


def run_counter(tree, work, tag, base, extra):
    rundir = os.path.join(work, 'run-' + tag)
    if os.path.exists(rundir):
        shutil.rmtree(rundir)
    tmp = os.path.join(work, 'tmp', tag)
    os.makedirs(tmp, exist_ok=True)
    cmd = [sys.executable, os.path.join(tree, COUNTER_DEST), '--lane', tree, '--rev', 'HEAD',
           '--base', base, '--work', rundir] + list(extra)
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=work,
                       env=child_env({'TMPDIR': tmp}))
    for suffix, data in (('.stdout', p.stdout), ('.stderr', p.stderr)):
        with open(os.path.join(work, tag + suffix), 'w', encoding='utf-8') as fh:
            fh.write(data)
    line = ''
    for out_line in p.stdout.splitlines():
        if VERDICT_RE.match(out_line):
            line = out_line
    return line, p.returncode


def parse_emit(stdout, kinds):
    """Rows the counter's --emit printed: `EMIT_CAP | id | what | evidence | first |` and
    `EMIT_AXIS | id | score | evidence |` (the round-47 emit shape); fallback: markdown rows
    that carry `runs 3` and start with a statement id."""
    cap, axis = [], []
    for line in stdout.splitlines():
        s = line.strip()
        if not s.startswith('EMIT_'):
            continue
        parts = [p.strip() for p in s.strip('|').split('|')]
        if parts[0] == 'EMIT_CAP' and len(parts) >= 5:
            cap.append(parts[1:5])
        elif parts[0] == 'EMIT_AXIS' and len(parts) >= 4:
            row = parts[1:4]
            axis.append(row + ['\u2014'] * (5 - len(row)))
    if not cap and not axis:
        for line in stdout.splitlines():
            s = line.strip()
            if not s.startswith('|') or 'runs 3' not in s:
                continue
            cells = cells_of(s)
            if not cells or cells[0] not in kinds:
                continue
            (cap if kinds[cells[0]] == 'cap' else axis).append(cells)
    return cap, axis


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--counter', required=True, help='the round-48 C1 counter to test')
    ap.add_argument('--work', required=True, help='scratch dir; one clone per control lives here')
    ap.add_argument('--lane', default=LANE, help='lane to clone (default %s)' % LANE)
    ap.add_argument('--base', default=BASE, help='BASE revision of the controls')
    ap.add_argument('--only', help='passthrough: --only ID,ID (seat probe)')
    ap.add_argument('--rounds', help='passthrough: --rounds N (seat probe)')
    ap.add_argument('--jobs', help='passthrough: --jobs N')
    a = ap.parse_args()

    counter = os.path.abspath(a.counter)
    if not os.path.isfile(counter):
        raise HarnessError('--counter %s: no such file' % counter)
    work = os.path.abspath(a.work)
    if not (work.startswith('/fast/scratch/') or os.environ.get('TMPDIR', '').startswith('/fast/scratch/')):
        print('run-controls: note: --work %s is outside /fast/scratch' % work, file=sys.stderr)
    if os.path.exists(work) and os.listdir(work):
        raise HarnessError('--work %s must be empty or absent' % work)
    os.makedirs(work, exist_ok=True)
    extra = []
    if a.only:
        extra += ['--only', a.only]
    if a.rounds:
        extra += ['--rounds', a.rounds]
    if a.jobs:
        extra += ['--jobs', a.jobs]

    raw = git_show(a.lane, a.base + ':' + STATEMENTS_PATH)
    kinds = {s['id']: s['kind'] for s in json.loads(raw)['statements']}
    cap47, axis47 = round47_rows(git_show(a.lane, a.base + ':SCORECARD.md'))
    if len(cap47) != 19 or len(axis47) != 3:
        raise HarnessError('round-47 restatement has %d capability + %d axis rows, expected 19 + 3'
                           % (len(cap47), len(axis47)))
    for row in cap47 + axis47:
        if kinds.get(row[0]) is None:
            raise HarnessError('round-47 row %r is not a frozen statement id' % row[0])
    if len(cap47) + len(axis47) != len(kinds):
        raise HarnessError('%d rows for %d statements' % (len(cap47) + len(axis47), len(kinds)))

    # CTL_A (base unchanged) is committed first: the CTL_E rows come from its --emit run.
    trees = {}
    for name in ('CTL_A', 'CTL_B', 'CTL_C', 'CTL_D', 'CTL_E'):
        trees[name] = {'dir': clone_tree(work, name, a.lane, a.base), 'rows': 0}
        trees[name]['sha'] = install_counter(trees[name]['dir'], counter)

    trees['CTL_A']['rev'] = commit_tree(trees['CTL_A']['dir'],
                                        'round-48 C1 control CTL_A: base tree, counter '
                                        + COUNTER_DEST)

    for name, title, intro, cap_rows, axis_rows in (
        ('CTL_B', 'Standing self-assessment \u2014 control CTL_B (round-47 rows, relabelled runs 3 stable)',
         'Control CTL_B of round 48: the round-47 standing rows re-appended verbatim with `, runs 3 stable` added to each evidence cell and nothing else changed. No re-observation was taken.',
         [add_runs(r) for r in cap47], [add_runs(r) for r in axis47]),
        ('CTL_C', 'Standing self-assessment \u2014 control CTL_C (three invented members, nondeterministic)',
         'Control CTL_C of round 48 (superset cheat): each row declares its round-47 value plus two invented members, class `nondeterministic`.',
         [superset_row(r, 'cap') for r in cap47], [superset_row(r, 'axis') for r in axis47]),
        ('CTL_D', 'Standing self-assessment \u2014 control CTL_D (deps everything)',
         'Control CTL_D of round 48 (deps-everything): each row restates its round-47 value with deps `%s` and `, runs 3 stable`.'
         % ALL_DEPS,
         [deps_everything_row(r) for r in cap47], [deps_everything_row(r) for r in axis47]),
    ):
        append_scorecard(trees[name]['dir'], section_text(title, intro, cap_rows, axis_rows))
        ok = base_prefix_ok(trees[name]['dir'], a.base)
        trees[name]['append_only'] = int(ok)
        trees[name]['rows'] = count_runs3(trees[name]['dir'])
        trees[name]['rev'] = commit_tree(trees[name]['dir'], 'round-48 C1 control %s' % name)

    trees['CTL_A']['rows'] = count_runs3(trees['CTL_A']['dir'])
    trees['CTL_A']['append_only'] = int(base_prefix_ok(trees['CTL_A']['dir'], a.base))

    # CTL_A's single observation run --emit yields both the CTL_A line and the CTL_E rows.
    a_line, a_rc = run_counter(trees['CTL_A']['dir'], work, 'CTL_A', a.base, extra + ['--emit'])
    a_exit = a_rc
    with open(os.path.join(work, 'CTL_A.stdout'), encoding='utf-8') as fh:
        emit_out = fh.read()
    if not a_line:
        # the counter may not print a verdict under --emit; take the plain run instead.
        a_line, a_exit = run_counter(trees['CTL_A']['dir'], work, 'CTL_A-plain', a.base, extra)
        with open(os.path.join(work, 'CTL_A-plain.stdout'), encoding='utf-8') as fh:
            a_line_out = fh.read()
        if not a_line:
            raise HarnessError('counter produced no C1_R48 line on CTL_A (see %s/CTL_A-plain.stdout)'
                               % work)
        emit_cap, emit_axis = parse_emit(a_line_out, kinds)
    else:
        emit_cap, emit_axis = parse_emit(emit_out, kinds)

    expected = len(kinds) if not a.only else len([i for i in a.only.split(',') if i in kinds])
    emit_rows = emit_cap + emit_axis
    for row in emit_rows:
        if 'runs 3' not in row[2]:
            print('run-controls: WARN: emitted row %r has no `runs 3` clause' % row[0],
                  file=sys.stderr)
    if not emit_rows:
        raise HarnessError('counter --emit printed no rows on CTL_A; CTL_E cannot be built')

    append_scorecard(trees['CTL_E']['dir'], section_text(
        'Standing self-assessment \u2014 control CTL_E (rows from the counter --emit of CTL_A)',
        'Control CTL_E of round 48 (positive): the rows below are the counter\'s own `--emit` output from its observation run on CTL_A, pasted unchanged.',
        emit_cap, emit_axis))
    trees['CTL_E']['append_only'] = int(base_prefix_ok(trees['CTL_E']['dir'], a.base))
    trees['CTL_E']['rows'] = count_runs3(trees['CTL_E']['dir'])
    trees['CTL_E']['rev'] = commit_tree(trees['CTL_E']['dir'], 'round-48 C1 control CTL_E')

    lines = {'CTL_A': (a_line, a_exit)}
    for name in ('CTL_B', 'CTL_C', 'CTL_D', 'CTL_E'):
        lines[name] = run_counter(trees[name]['dir'], work, name, a.base, extra)

    for name in ('CTL_A', 'CTL_B', 'CTL_C', 'CTL_D', 'CTL_E'):
        t = trees[name]
        print('TREE %s rev=%s runs3_rows=%d append_only=%d counter_sha256=%s work=%s' % (
            name, t.get('rev', '-'), t['rows'], t.get('append_only', 0), t['sha'][:12], t['dir']))
    print('TREE emit_rows=%d expected_rows=%d' % (len(emit_rows), expected))
    missing = 0
    for name in ('CTL_A', 'CTL_B', 'CTL_C', 'CTL_D', 'CTL_E'):
        line, rc = lines[name]
        if not line:
            missing += 1
            print('CTL_%s NO-C1_R48-LINE rc=%d' % (name.split('_')[1], rc))
            print('run-controls: counter run on %s printed no C1_R48 line; see %s/%s.stderr'
                  % (name, work, name), file=sys.stderr)
            continue
        print('CTL_%s %s' % (name.split('_')[1], line))
    return 1 if missing else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except HarnessError as exc:
        print('run-controls: %s' % exc, file=sys.stderr)
        sys.exit(2)
