#!/usr/bin/env python3
"""Round 33 C1 counter (operability: runner tally audit v2), frozen before any data run.

Claim C1 (contract .ufo/evidence/round-33/contract.json): the committed tools/tally-audit-v2.py
at REV, run as `python3 tally-audit-v2.py --runner COPY` in a sandbox (bwrap: only the tool and
one runner copy visible, stdout only), exits 1 with a last stdout line beginning
`TALLY_AUDIT: FAIL` on every must-kill runner copy (18 public families + every valid sealed
held-out copy) and exits 0 with a last stdout line beginning `TALLY_AUDIT: PASS` on every
must-accept copy (8 public + every valid sealed held-out accept copy); REV's
tools/mutate-and-run.sh has sha256 a7d3f2dd...2eb9; the tool's bytes equal the frozen pin; at
least 8 valid sealed must-kill and 6 valid sealed must-accept copies exist, all written after
the tool and counter freezes; a committed controls receipt names this counter's sha256 and
records every control tool failing the predicate. Label: C1_R33_PASS.

Kill rule (frozen): the first full default-mode run at the measurement revision decides;
PASS=false is a miss, never re-scaled, re-seeded or amended. A rule changed after any seat has
scored is not the claim's rule.

Routed repairs carried into this counter (round-32 closure items 1 and 4):
  - the default mode REFUSES to run unless a committed controls receipt names this counter's
    sha256 (git show REV:.ufo/evidence/round-33/c1/controls-receipt.json); controls are written
    with --write-controls BEFORE any data run and committed; a counter edit therefore
    invalidates the receipt on its own;
  - witness.loop names are validated against ^[A-Za-z_][A-Za-z0-9_]*$ before any bash use;
  - a non-string block witness is a validation error (ho_invalid), never a crash;
  - held-out discovery is recursive (any depth under .ufo/evidence/round-33/heldout).
Routed repairs carried into this counter (round 34, amendment 6, pre-authoring and pre-data):
  - the sealed-copy witness gate is SET-AWARE (RevengerWitness Q1b/Q3/Q3b, routed by the
    round-33 closure): kill+head requires a leg-assignment-line diff with an identical block;
    accept+head requires an identical block; accept+vector requires behavioral equivalence
    (a == b) with the bytes changed; kill+vector keeps a != b over a len-9 vector. Adopted
    BEFORE any sealed held-out authoring; no default-mode deciding run had occurred at
    amendment time (round-33 head receipt is a not-run structural false; r34 dev/panel runs
    are authoring observations, not the deciding run).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import secrets
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V1_PATH = os.path.join(HERE, '..', '..', 'round-32', 'c1-measure.py')
_spec = importlib.util.spec_from_file_location('c1r32', V1_PATH)
v1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v1)

TOOL = 'tools/tally-audit-v2.py'
RUNNER = 'tools/mutate-and-run.sh'
SELF_PATH = '.ufo/evidence/round-33/c1/c1-measure.py'
CONTROLS_PATH = '.ufo/evidence/round-33/c1/controls-receipt.json'
HELDOUT_DIR = '.ufo/evidence/round-33/heldout'
TOOL_SHA256 = '7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10'  # pinned at freeze; see contract.json ("tool_sha")
PINNED_RUNNER_SHA = 'a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9'
NAME_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

START = '  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n'


class CounterError(Exception):
    pass


def git(lane, *args):
    return v1.git(lane, *args)


def show(lane, rev, path):
    r = git(lane, 'show', '%s:%s' % (rev, path))
    if r.returncode != 0:
        return None
    return r.stdout


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def adding_commit(lane, rev, path):
    r = git(lane, 'log', '--diff-filter=A', '--format=%H', rev, '--', path)
    hs = r.stdout.decode().split()
    return hs[-1] if hs else None


def is_ancestor(lane, a, b):
    return git(lane, 'merge-base', '--is-ancestor', a, b).returncode == 0


def list_tree(lane, rev, path):
    r = git(lane, 'ls-tree', '-r', '--name-only', rev, '--', path)
    if r.returncode != 0:
        return []
    return [ln for ln in r.stdout.decode().splitlines() if ln.endswith('.json')]


# ------------------------------------------------------------ held-out handling

def validate_ho(ho):
    if not isinstance(ho, dict):
        raise CounterError('not an object')
    if not isinstance(ho.get('id'), str) or not isinstance(ho.get('author'), str):
        raise CounterError('id/author must be strings')
    if ho.get('set') not in ('kill', 'accept'):
        raise CounterError('set must be kill|accept')
    edits = ho.get('edits')
    if not isinstance(edits, list) or not edits:
        raise CounterError('edits must be a nonempty list')
    for ed in edits:
        if not isinstance(ed, dict) or not isinstance(ed.get('old'), str) or not isinstance(ed.get('new'), str):
            raise CounterError('each edit needs string old/new')
    w = ho.get('witness')
    if w is not None:
        if not isinstance(w, dict):
            raise CounterError('witness must be an object')
        if 'vector' in w:
            vec = w['vector']
            if not isinstance(vec, list) or not all(isinstance(x, int) and 0 <= x <= 255 for x in vec):
                raise CounterError('witness.vector must be a list of ints 0..255')
            if len(vec) != 9:
                raise CounterError('witness.vector must name all 9 leg statuses (len %d)' % len(vec))
        elif w.get('kind') == 'head':
            pass
        else:
            raise CounterError('witness needs vector or kind=head')


def apply_edits(text, edits):
    for ed in edits:
        old, new = ed['old'], ed['new']
        if text.count(old) != 1:
            raise CounterError('edit old-string occurs %d times (need exactly 1)' % text.count(old))
        text = text.replace(old, new, 1)
    return text


def tally_block_of(text):
    i = text.find(START)
    if i < 0:
        raise CounterError('tally start not found')
    return text[i:text.index('\n}\n', i) + 1]


def head_of(text):
    i = text.find(START)
    if i < 0:
        raise CounterError('tally start not found')
    return text[:i]


def block_run(block, vector, work):
    """Run one tally block on one status vector under a real bwrap boundary; return (rc, stdout-first-line).

    Read-only runtime mounts make `bash` resolvable inside the sandbox; `timeout` runs OUTSIDE it
    (CriticCounter: the frozen form execvp'd timeout inside a sandbox with no runtime mounts, so every
    witness run failed closed). Writes are confined to the per-run workdir."""
    d = os.path.join(work, 'w-' + secrets.token_hex(6))
    os.makedirs(d)
    script = os.path.join(d, 'run.sh')
    names = ['st_js', 'st_kagi', 'st_tsu', 'st_mado', 'st_checklist', 'st_claims', 'st_roundgate',
             'st_sourcescheck', 'st_citecheck']
    decl = ' '.join('%s=${%d}' % (n, i + 1) for i, n in enumerate(names[:len(vector)]))
    with open(script, 'w') as f:
        f.write('set -u -o pipefail\ntally() {\n  local %s\n  local root=r auto=0 KEEP=1\n%s}\n'
                'out=$(tally %s 2>/dev/null); rc=$?; printf "RC\\t%%s\\t%%s\\n" "$rc" "${out%%%%$\'\\n\'*}"\n'
                % (decl, block, ' '.join(str(s) for s in vector)))
    inner = ['bash', '/w/run.sh']
    p = subprocess.run(['timeout', '90'] + bwrap_argv(inner, d),
                       env={'PATH': '/usr/bin:/bin', 'HOME': '/w', 'TMPDIR': '/tmp', 'LC_ALL': 'C'},
                       capture_output=True, timeout=120)
    first = ''
    rc = p.returncode
    for ln in p.stdout.decode('utf-8', 'replace').splitlines():
        if ln.startswith('RC\t'):
            parts = ln.split('\t', 2)
            rc = int(parts[1])
            first = parts[2] if len(parts) > 2 else ''
    return rc, first


def ho_witness_ok(ho, pristine, mutated, work):
    # Amendment 6 (r34, pre-authoring, pre-data; RevengerWitness Q1b/Q3/Q3b): the set-aware
    # witness rule. kill+head requires a leg-assignment-line diff with an identical block;
    # accept+head requires an identical block (a lethal ride-along behind a benign head edit
    # is refused); accept+vector flips to equivalence (a == b), so cosmetic/decoy clones are
    # satisfiable; kill+vector keeps a != b with len==9 (validated in validate_ho).
    w = ho.get('witness') or {}
    pb, mb = tally_block_of(pristine), tally_block_of(mutated)
    if w.get('kind') == 'head':
        if head_of(mutated) == head_of(pristine):
            return False, 'head'
        if mb != pb:
            return False, 'head-with-block-edit'
        if ho['set'] == 'kill':
            # v2's head check kills exactly: a leg var not assigned exactly once as bare
            # `st_x=$?` before the block, or an extra assignment to a leg var. Require the
            # diff to touch that surface (an inert rename/comment head edit then validates
            # as invalid, never as a must-kill the tool would blamelessly pass).
            A = re.compile(r'^[ \t]*(st_[A-Za-z0-9_]+)=\$\?[ \t]*$', re.M)
            X = re.compile(r'^[ \t]*(st_[A-Za-z0-9_]+)[ \t]*=', re.M)
            if (sorted(A.findall(head_of(pristine))) != sorted(A.findall(head_of(mutated)))
                    or sorted(X.findall(head_of(pristine))) != sorted(X.findall(head_of(mutated)))):
                return True, 'head-leg-assignment'
            return False, 'head-edit-cannot-kill'
        return True, 'head'
    vec = w.get('vector')
    if not vec:
        return False, 'no-witness'
    a = block_run(pb, vec, work)
    b = block_run(mb, vec, work)
    if ho['set'] == 'accept':
        return a == b and mutated != pristine, 'vector-equivalence'
    if pb == mb:
        return False, 'block-identical'
    return a != b, 'vector'


# ------------------------------------------------------------ sandboxed runs (repaired boundary)

BWRAP_RUNTIME = ('--ro-bind', '/usr', '/usr', '--ro-bind', '/bin', '/bin',
                 '--ro-bind', '/lib', '/lib', '--ro-bind', '/lib64', '/lib64',
                 '--ro-bind', '/etc', '/etc')


def bwrap_argv(inner, workdir):
    return ['bwrap', '--unshare-all', '--die-with-parent', '--new-session', '--clearenv',
            '--dev', '/dev', '--proc', '/proc', '--tmpfs', '/tmp',
            *BWRAP_RUNTIME, '--bind', workdir, '/w', '--chdir', '/w'] + inner


def run_tool_sandboxed(tool, copy, work):
    """Run `python3 -I tool --runner copy` under a real bwrap boundary: read-only runtime mounts
    (so python/coreutils resolve), writes confined to the per-run workdir, no network, new session.
    `timeout` runs OUTSIDE the sandbox (CriticCounter/SentinelSandbox: the frozen v1.run_tool had no
    bubblewrap boundary at all and the round-33 block_run could not exec `timeout` inside it)."""
    d = os.path.join(work, 'run-' + secrets.token_hex(8))
    os.makedirs(os.path.join(d, 'tmp'))
    t = os.path.join(d, 'tool.py')
    c = os.path.join(d, 'copy.sh')
    import shutil as _sh
    _sh.copyfile(tool, t)
    _sh.copyfile(copy, c)
    env = {'PATH': '/usr/bin:/bin', 'HOME': '/w', 'TMPDIR': '/w/tmp',
           'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8'}
    try:
        p = subprocess.run(['timeout', '600'] + bwrap_argv([sys.executable, '-I', '/w/tool.py', '--runner', '/w/copy.sh'], d),
                           env=env, capture_output=True, timeout=660)
        rc, out = p.returncode, p.stdout.decode('utf-8', 'replace')
    except subprocess.TimeoutExpired:
        rc, out = 'timeout', ''
    lines = out.splitlines()
    if rc == 1 and any(x.startswith('TALLY_AUDIT: FAIL') for x in lines):
        outcome = 'KILL'
    elif rc == 0 and any(x.startswith('TALLY_AUDIT: PASS') for x in lines):
        outcome = 'ACCEPT'
    else:
        outcome = 'OTHER'
    last = next((x for x in reversed(lines) if x.startswith('TALLY_AUDIT:')), '')
    return outcome, rc, last


def score_tool(tool_path, copies, work):
    """copies: list of (label, set, body_bytes). Returns (kill_hit, kill_total, accept_hit, accept_total)."""
    k_hit = k_tot = a_hit = a_tot = 0
    for label, set_, body in copies:
        d = os.path.join(work, 'c-' + secrets.token_hex(6))
        os.makedirs(d)
        cp = os.path.join(d, 'mutant.sh')
        with open(cp, 'wb') as f:
            f.write(body)
        outcome, rc, last = run_tool_sandboxed(tool_path, cp, d)
        verdict = (rc == 1 and last.startswith('TALLY_AUDIT: FAIL'))
        accept = (rc == 0 and last.startswith('TALLY_AUDIT: PASS'))
        if set_ == 'kill':
            k_tot += 1
            k_hit += bool(verdict)
        else:
            a_tot += 1
            a_hit += bool(accept)
    return k_hit, k_tot, a_hit, a_tot


def public_panel(pristine, seed):
    import random
    rng = random.Random(seed)
    t = pristine.decode()
    copies = []
    for name, body in v1.frozen_kill(t) + v1.generated_kill(t, rng):
        copies.append(('pub-' + name, 'kill', body.encode()))
    for name, body in v1.frozen_accept(t) + v1.generated_accept(t, rng):
        copies.append(('pub-' + name, 'accept', body.encode()))
    return copies


def write_controls(lane, rev, work, seed, receipt_path=None, tools=None):
    """Score control TOOLS against the public panel; write the controls receipt (pre-data)."""
    tools = tools or []
    if receipt_path is None:
        receipt_path = os.path.join(lane, CONTROLS_PATH)
    pristine = show(lane, rev, RUNNER)
    if pristine is None:
        raise CounterError('runner not found at %s' % rev)
    if sha256(pristine) != PINNED_RUNNER_SHA:
        raise CounterError('runner sha mismatch at %s' % rev)
    self_bytes = show(lane, rev, SELF_PATH)
    if self_bytes is None:
        self_bytes = open(os.path.abspath(__file__), 'rb').read()
    copies = public_panel(pristine, seed)
    rows = []
    all_false = True
    for tpath in tools:
        k_hit, k_tot, a_hit, a_tot = score_tool(tpath, copies, work)
        passed = (k_hit == k_tot and a_hit == a_tot)
        all_false = all_false and not passed
        rows.append({'tool': os.path.basename(tpath), 'kill': '%d/%d' % (k_hit, k_tot),
                     'accept': '%d/%d' % (a_hit, a_tot), 'predicate_pass': passed})
    receipt = {'counter': os.path.basename(SELF_PATH), 'counter_sha256': sha256(self_bytes),
               'seed': seed, 'runner_sha256': PINNED_RUNNER_SHA, 'controls': rows, 'all_false': all_false}
    os.makedirs(os.path.dirname(receipt_path), exist_ok=True)
    with open(receipt_path, 'w') as f:
        json.dump(receipt, f, indent=1, sort_keys=True)
        f.write('\n')
    print('C1_R33_CONTROLS: controls=%d all_false=%s receipt=%s' % (len(rows), all_false, receipt_path))
    for r in rows:
        print('  %s kill=%s accept=%s predicate_pass=%s' % (r['tool'], r['kill'], r['accept'], r['predicate_pass']))
    return 0 if all_false else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--seed', default=None)
    ap.add_argument('--receipt', default=None)
    ap.add_argument('--write-controls', nargs='+', default=None)
    a = ap.parse_args()
    seed = a.seed or secrets.token_hex(8)
    os.makedirs(a.work, exist_ok=True)
    if a.write_controls is not None:
        return write_controls(a.lane, a.rev, a.work, seed, a.receipt, a.write_controls)

    tool_b = show(a.lane, a.rev, TOOL)
    runner_b = show(a.lane, a.rev, RUNNER)
    tool_present = tool_b is not None
    tool_sha_ok = tool_present and TOOL_SHA256 is not None and sha256(tool_b) == TOOL_SHA256
    runner_sha_ok = runner_b is not None and sha256(runner_b) == PINNED_RUNNER_SHA

    controls_ok = False
    controls_detail = 'not-checked'
    if tool_present:
        self_b = show(a.lane, a.rev, SELF_PATH)
        receipt_b = show(a.lane, a.rev, CONTROLS_PATH)
        if self_b is None:
            controls_detail = 'counter-absent-at-rev'
        elif receipt_b is None:
            controls_detail = 'receipt-missing'
        else:
            try:
                receipt = json.loads(receipt_b)
                rows = receipt.get('controls')
                rows_ok = isinstance(rows, list) and len(rows) >= 1 and all(
                    isinstance(r, dict) and r.get('predicate_pass') is False for r in rows)
                controls_ok = (receipt.get('counter_sha256') == sha256(self_b)
                               and receipt.get('all_false') is True and rows_ok)
                controls_detail = 'ok' if controls_ok else 'sha-or-allfalse-or-rows-mismatch'
            except (ValueError, AttributeError):
                controls_detail = 'receipt-unparseable'

    v1k = v1kt = v1a = v1at = 0
    ho_k = ho_kt = ho_a = ho_at = ho_invalid = 0
    heldout_after_freeze = 0
    if tool_present and tool_sha_ok and runner_sha_ok and controls_ok:
        tdir = os.path.join(a.work, 't-' + secrets.token_hex(6))
        os.makedirs(tdir)
        tp = os.path.join(tdir, 'tool.py')
        with open(tp, 'wb') as f:
            f.write(tool_b)
        copies = public_panel(runner_b, seed)
        v1k, v1kt, v1a, v1at = score_tool(tp, copies, tdir)
        pristine = runner_b.decode()
        self_add = adding_commit(a.lane, a.rev, SELF_PATH)
        tool_add = adding_commit(a.lane, a.rev, TOOL)
        freeze_ok = True
        ho_copies = []
        for path in list_tree(a.lane, a.rev, HELDOUT_DIR):
            raw = show(a.lane, a.rev, path)
            try:
                ho = json.loads(raw)
                validate_ho(ho)
                mutated = apply_edits(pristine, ho['edits'])
                if mutated == pristine:
                    raise CounterError('edits do not change the runner')
                if not ho_witness_ok(ho, pristine, mutated, tdir)[0]:
                    raise CounterError('witness does not demonstrate the fault')
            except (CounterError, ValueError):
                ho_invalid += 1
                continue
            if ho['set'] == 'kill':
                ho_kt += 1
            else:
                ho_at += 1
            ho_copies.append((ho['id'], ho['set'], mutated.encode()))
            add = adding_commit(a.lane, a.rev, path)
            if add and self_add and tool_add:
                if not (is_ancestor(a.lane, self_add, add) and is_ancestor(a.lane, tool_add, add)):
                    freeze_ok = False
        heldout_after_freeze = int(freeze_ok and ho_kt + ho_at > 0)
        for label, set_, body in ho_copies:
            d = os.path.join(tdir, 'h-' + secrets.token_hex(6))
            os.makedirs(d)
            cp = os.path.join(d, 'm.sh')
            with open(cp, 'wb') as f:
                f.write(body)
            outcome, rc, last = run_tool_sandboxed(tp, cp, d)
            if set_ == 'kill':
                ho_k += bool(rc == 1 and last.startswith('TALLY_AUDIT: FAIL'))
            else:
                ho_a += bool(rc == 0 and last.startswith('TALLY_AUDIT: PASS'))

    ok = (tool_present and tool_sha_ok and runner_sha_ok and controls_ok
          and v1k == v1kt and v1a == v1at and v1kt == 18 and v1at == 8
          and ho_invalid == 0 and ho_kt >= 8 and ho_at >= 6
          and ho_k == ho_kt and ho_a == ho_at and heldout_after_freeze == 1)
    print('C1_R33: tool_present=%d tool_sha_ok=%d runner_sha_ok=%d controls_ok=%d(%s) '
          'v1_kill=%d/%d v1_accept=%d/%d ho_kill=%d/%d ho_accept=%d/%d ho_invalid=%d '
          'heldout_after_freeze=%d seed=%s rev=%s C1_R33_PASS=%s'
          % (int(tool_present), int(tool_sha_ok), int(runner_sha_ok), int(controls_ok), controls_detail,
             v1k, v1kt, v1a, v1at, ho_k, ho_kt, ho_a, ho_at, ho_invalid,
             heldout_after_freeze, seed, a.rev, 'true' if ok else 'false'))
    return 0 if ok else 1


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except CounterError as e:
        print('C1_R33: SETUP (%s)' % e)
        raise SystemExit(2)
