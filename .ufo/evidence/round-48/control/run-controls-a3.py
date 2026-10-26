#!/usr/bin/env python3
"""Round-48 attempt-3 driver for the C1 controls CTL_B-CTL_E (the frozen harness's CTL_A run
finished at freeze bytes; its B-E runs never did: control/c1-controls.stdout).

It imports the frozen harness control/run-controls.py (sha256 f5732f18..., unchanged) and uses
its own tree builders, row transforms, commit and counter-run functions; it changes only the
schedule: CTL_E's rows are taken from the committed CTL_A --emit output
(control/c1-CTL_A.stdout, produced by the frozen harness at freeze bytes) instead of a second
CTL_A run, and the four counter runs execute concurrently instead of one after another.
Every tree is a --shared clone under --work; nothing is written in the lane.

Usage: run-controls-a3.py --counter COUNTER.py --work EMPTY_DIR [--jobs N]
"""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.join(HERE, 'run-controls.py')
HARNESS_SHA = 'f5732f18a1580196d9e7a0ddf4381ff6dd47ffc34474d84cb0c9ef5ead2b998d'
CTL_A_EMIT = os.path.join(HERE, 'c1-CTL_A.stdout')


def load_harness():
    with open(HARNESS, 'rb') as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    if digest != HARNESS_SHA:
        sys.exit('run-controls-a3: harness sha256 %s != frozen %s' % (digest, HARNESS_SHA))
    spec = importlib.util.spec_from_file_location('run_controls', HARNESS)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    h = load_harness()
    ap = argparse.ArgumentParser()
    ap.add_argument('--counter', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--lane', default=h.LANE)
    ap.add_argument('--base', default=h.BASE)
    ap.add_argument('--jobs')
    a = ap.parse_args()
    counter = os.path.abspath(a.counter)
    work = os.path.abspath(a.work)
    if os.path.exists(work) and os.listdir(work):
        sys.exit('run-controls-a3: --work must be empty or absent')
    os.makedirs(work, exist_ok=True)
    extra = ['--jobs', a.jobs] if a.jobs else []

    kinds = {s['id']: s['kind'] for s in json.loads(h.git_show(a.lane, a.base + ':' + h.STATEMENTS_PATH))['statements']}
    cap47, axis47 = h.round47_rows(h.git_show(a.lane, a.base + ':SCORECARD.md'))
    if len(cap47) != 19 or len(axis47) != 3:
        sys.exit('run-controls-a3: round-47 restatement has %d + %d rows' % (len(cap47), len(axis47)))
    with open(CTL_A_EMIT, encoding='utf-8') as fh:
        emit_cap, emit_axis = h.parse_emit(fh.read(), kinds)
    if len(emit_cap) + len(emit_axis) != len(kinds):
        sys.exit('run-controls-a3: CTL_A emit holds %d rows, expected %d' % (len(emit_cap) + len(emit_axis), len(kinds)))

    specs = (
        ('CTL_B', 'Standing self-assessment \u2014 control CTL_B (round-47 rows, relabelled runs 3 stable)',
         'Control CTL_B of round 48: the round-47 standing rows re-appended verbatim with `, runs 3 stable` added to each evidence cell and nothing else changed. No re-observation was taken.',
         [h.add_runs(r) for r in cap47], [h.add_runs(r) for r in axis47]),
        ('CTL_C', 'Standing self-assessment \u2014 control CTL_C (three invented members, nondeterministic)',
         'Control CTL_C of round 48 (superset cheat): each row declares its round-47 value plus two invented members, class `nondeterministic`.',
         [h.superset_row(r, 'cap') for r in cap47], [h.superset_row(r, 'axis') for r in axis47]),
        ('CTL_D', 'Standing self-assessment \u2014 control CTL_D (deps everything)',
         'Control CTL_D of round 48 (deps-everything): each row restates its round-47 value with deps `%s` and `, runs 3 stable`.' % h.ALL_DEPS,
         [h.deps_everything_row(r) for r in cap47], [h.deps_everything_row(r) for r in axis47]),
        ('CTL_E', 'Standing self-assessment \u2014 control CTL_E (rows from the counter --emit of CTL_A)',
         'Control CTL_E of round 48 (positive): the rows below are the counter\'s own `--emit` output from its observation run on CTL_A, pasted unchanged.',
         emit_cap, emit_axis),
    )
    trees = {}
    for name, title, intro, cap_rows, axis_rows in specs:
        d = h.clone_tree(work, name, a.lane, a.base)
        sha = h.install_counter(d, counter)
        h.append_scorecard(d, h.section_text(title, intro, cap_rows, axis_rows))
        trees[name] = {'dir': d, 'sha': sha, 'append_only': int(h.base_prefix_ok(d, a.base)),
                       'rows': h.count_runs3(d)}
        trees[name]['rev'] = h.commit_tree(d, 'round-48 C1 control %s' % name)

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(trees)) as ex:
        futs = {n: ex.submit(h.run_counter, t['dir'], work, n, a.base, extra) for n, t in trees.items()}
        lines = {n: f.result() for n, f in futs.items()}

    for name, t in trees.items():
        print('TREE %s rev=%s runs3_rows=%d append_only=%d counter_sha256=%s' % (
            name, t['rev'], t['rows'], t['append_only'], t['sha'][:12]))
    missing = 0
    for name in trees:
        line, rc = lines[name]
        if not line:
            missing += 1
            print('%s NO-C1_R48-LINE rc=%d' % (name, rc))
            continue
        print('%s %s' % (name, line))
    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main())
