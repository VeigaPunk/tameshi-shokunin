#!/usr/bin/env python3
"""Round 32 C1 counter v2 (operability: runner tally audit), frozen before any data run.

Why v2: before any data, control seat CriticC1 met frozen counter v1 (`.ufo/evidence/round-32/c1-measure.py`,
left unchanged) with an allowlist that read v1's must-accept builders at run time and failed everything
else (`.ufo/waves/round-32/w1/CriticC1.md`). Every v1 copy family is public, so a tool written by
someone who has read the counter can memorize the accept shapes. v2 keeps every v1 copy and adds:
  1. a sandbox: the tool runs under bwrap with only /usr, /etc, the tool file and the copy visible
     (no lane, no counter, no sibling copies), so nothing can be read at run time;
  2. a tool freeze: REV's tools/tally-audit.py must have sha256 TOOL_SHA256, the bytes committed with
     this counter; the tool cannot change after the held-out set is written;
  3. a sealed held-out set: copies written AFTER the freeze by seats who did not write the tool,
     committed as `.ufo/evidence/round-32/heldout/*.json`. Each file adding commit must descend from
     the commit that added this counter. The counter checks every held-out copy mechanically before
     the tool sees it (validity rules below); invalid copies are excluded and listed.

Predicate (label C1_R32V2_PASS), the same sentence as contract-amendment-1.json `predicate`:
  C1 passes at REV iff REV's tools/tally-audit.py has sha256 TOOL_SHA256 and, run in the sandbox as
  `python3 tally-audit.py --runner COPY`, exits 1 with a stdout line beginning `TALLY_AUDIT: FAIL` on
  every must-kill copy and exits 0 with a stdout line beginning `TALLY_AUDIT: PASS` on every
  must-accept copy, over the 18 + 8 v1 copies and every valid held-out copy, with at least 6 valid
  held-out must-kill and 6 valid held-out must-accept copies, every held-out file added after this
  counter, and REV's tools/mutate-and-run.sh at sha256 PINNED_RUNNER_SHA.

Held-out file schema (one copy per file): {"id": str, "author": seat, "set": "kill"|"accept",
  "edits": [{"old": str, "new": str}, ...] applied in order to the pinned runner, each `old` occurring
  exactly once at its turn, "rationale": str, "witness": W}.
Validity (counter-checked):
  - every edit applies; the copy differs from the pinned runner; `bash -n` accepts it;
  - kill: W is {"vector": [9 ints 0..255], "loop": [optional leg names]} and the copy's tally block and
    the pinned block print a different (exit, first line) on it (with `loop`, both blocks' tally loop
    lines are replaced by that operand list first); or W is {"block": str} and the pinned harness
    rejects that injected tally block while the copy's harness accepts it;
  - accept: the copy's leg names and loop operands equal the pinned ones as multisets; its tally block
    prints the pinned (exit, first line) for every status 0..255 at the first leg, 1 2 3 4 126 127 255
    at every leg, and every one-operand duplicate/drop stress; and its harness gives the pinned verdict
    on the reference block, on each of the counter's 18 fault blocks and on every held-out block witness.
  Parsing uses fixed anchors (the pinned lines `  local nlegs=9 npass=0 nfail=0 nsetup=0 st`,
  `  for st in ...; do`, `  local tblock `, `  tblock=$(awk ... "$SELF")`, `  tblock=$tblock_full`);
  a copy the counter cannot parse is invalid.

Usage: c1-measure-v2.py --lane LANE --rev REV --work EMPTY_DIR [--seed HEX] [--jobs N]
Prints COPY and HELDOUT lines, then
  `C1_R32V2: v1_kill=K/18 v1_accept=A/8 ho_kill=k/n ho_accept=a/m ho_invalid=i tool_sha_ok=0|1
   runner_sha_ok=0|1 heldout_after_freeze=0|1 seed=S rev=REV C1_R32V2_PASS=true|false`.
Exit 0 iff PASS; 1 iff evaluated and not PASS; 2 on counter error.
"""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import os
import random
import re
import secrets
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('c1v1', os.path.join(HERE, '..', 'c1-measure.py'))
v1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v1)

TOOL_SHA256 = '158202f8bc85a82e92bbc7bb3c42f636f468a4484a9725937cefcc41997a356a'
SELF_PATH = '.ufo/evidence/round-32/v2/c1-measure-v2.py'
HELDOUT_DIR = '.ufo/evidence/round-32/heldout'
MIN_HO = 6
START = '  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n'
LOOP_LINE = re.compile(r'^  for st in (.*); do$', re.M)
H_START = '  local tblock '
H_END = '  tblock=$tblock_full\n'
EXTRACT = re.compile(r'^  tblock=\$\(awk .*"\$SELF"\)\n', re.M)


class Invalid(Exception):
    pass


def git(lane, *args):
    return v1.git(lane, *args)


# ------------------------------------------------------------ counter-owned instruments

def cblock(text):
    a = text.find('\nrun_regression() {\n')
    s = text.find(START, a)
    if a < 0 or s < 0:
        raise Invalid('tally start anchor missing')
    e = text.find('\n}\n', s)
    names = re.findall(r'^  (st_[a-z]+)=\$\?$', text[a:s], re.M)
    if e < 0 or not names:
        raise Invalid('tally block or leg names missing')
    return text[s:e + 1], names


def coperands(block):
    m = LOOP_LINE.search(block)
    if not m:
        raise Invalid('tally loop line missing')
    ops = re.findall(r'"\$(st_[a-z]+)"', m.group(1))
    if len(ops) != len(m.group(1).split()):
        raise Invalid('tally loop operand form')
    return ops


def set_loop(block, ops):
    m = LOOP_LINE.search(block)
    if not m:
        raise Invalid('tally loop line missing')
    return block[:m.start(1)] + ' '.join('"$%s"' % o for o in ops) + block[m.end(1):]


def bash_run(script, tmp, env_extra=None):
    fd, path = tempfile.mkstemp(suffix='.sh', dir=tmp)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(script)
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': tmp, 'TMPDIR': tmp}
    env.update(env_extra or {})
    try:
        p = subprocess.run(['bash', path], cwd=tmp, env=env, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        raise Invalid('bash timed out')
    return p.returncode, p.stdout.decode('utf-8', 'replace')


def tally_outputs(block, names, vectors, tmp):
    decl = ' '.join('%s=${%d}' % (n, i + 1) for i, n in enumerate(names))
    lines = ['set -u -o pipefail', 'tally() {', '  local ' + decl, '  local root=c1v2 auto=0 KEEP=1', block.rstrip('\n'), '}']
    for v in vectors:
        lines.append('out=$(tally %s 2>&1); rc=$?; printf "R\\t%%s\\t%%s\\n" "$rc" "${out%%%%$\'\\n\'*}"' % ' '.join(map(str, v)))
    rc, out = bash_run('\n'.join(lines) + '\n', tmp)
    got = [tuple(x.split('\t', 2)[1:]) for x in out.splitlines() if x.startswith('R\t')]
    if rc != 0 or len(got) != len(vectors):
        raise Invalid('tally driver failed')
    return got


def harness_failed(text, runner_path, injected, tmp):
    a = text.find(H_START)
    e = text.find(H_END, a)
    if a < 0 or e < 0:
        raise Invalid('harness anchors missing')
    sec = text[a:e + len(H_END)]
    if len(EXTRACT.findall(sec)) != 1:
        raise Invalid('harness extraction line missing')
    sec = EXTRACT.sub(lambda m: m.group(0) + '  tblock=$C1V2_INJECT\n', sec, count=1)
    script = ('set -u -o pipefail\nSELF=%s\nh() {\n  local root cases=0 failed=0\n  root=$(mktemp -d "$TMPDIR/h.XXXXXX")\n'
              '  st() { cases=$((cases + 1)); if [[ $2 -ne 0 ]]; then failed=$((failed + 1)); fi; }\n' % v1_quote(runner_path)
              + sec + '  printf "H %s %s\\n" "$cases" "$failed"\n}\nh\n')
    rc, out = bash_run(script, tmp, {'C1V2_INJECT': injected.rstrip('\n')})
    m = re.search(r'^H (\d+) (\d+)$', out, re.M)
    if not m:
        return True  # harness aborted on this block: it rejected it
    return int(m.group(1)) == 0 or int(m.group(2)) > 0


def v1_quote(s):
    return "'" + s.replace("'", "'\\''") + "'"


def fault_blocks(ref):
    b = ref
    start = START
    out = [b.replace('passed=%s', 'passing=%s'), b.replace('    exit 1\n', '    exit 0\n', 1),
           b.replace(' "$st_citecheck"; do\n', '; do\n', 1)]
    out += [b.replace(start, start + '  %s=0\n' % n, 1) for n in v1.NAMES]
    g0 = b.index('  if (( npass + nfail + nsetup != nlegs )); then\n')
    g1 = b.index('  fi\n', g0) + len('  fi\n')
    out.append(b[:g0] + b[g1:])
    out.append(b.replace('!= nlegs', '> nlegs'))
    fi = b[b.index('  if [[ $nfail -gt 0 ]]'):b.index('  if [[ $nsetup -gt 0 ]]')]
    se = b[b.index('  if [[ $nsetup -gt 0 ]]'):b.index('  # r30: tally completeness')]
    out.append(b.replace(fi + se, se + fi))
    out.append(b.replace('$nfail -gt 0', '$nfail -eq 1'))
    out.append(b.replace('$nsetup -gt 0', '$nsetup -eq 1'))
    out.append(b.replace('      *) nsetup', '      3) npass=$((npass + 1)) ;;\n      *) nsetup', 1))
    if len(out) != 18 or len(set(out)) != 18 or ref in out:
        raise RuntimeError('fault panel malformed')
    return out


def sweep_vectors(n):
    vs = [[0] * n] + [[s] + [0] * (n - 1) for s in range(1, 256)]
    for pos in range(n):
        for s in (1, 2, 3, 4, 126, 127, 255):
            v = [0] * n
            v[pos] = s
            vs.append(v)
    return vs


# ------------------------------------------------------------ held-out validation

def apply_edits(text, edits):
    for ed in edits:
        old, new = ed['old'], ed['new']
        if not isinstance(old, str) or not isinstance(new, str) or not old or text.count(old) != 1:
            raise Invalid('edit anchor not found exactly once: %r' % (old[:60] if isinstance(old, str) else old))
        text = text.replace(old, new, 1)
    return text


def validate(ho, pristine, ppath, tmp, block_witnesses):
    body = apply_edits(pristine, ho['edits'])
    if body == pristine:
        raise Invalid('copy equals pristine')
    fd, cpath = tempfile.mkstemp(suffix='.sh', dir=tmp)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(body)
    if subprocess.run(['bash', '-n', cpath], capture_output=True).returncode:
        raise Invalid('bash -n rejects copy')
    pblock, pnames = cblock(pristine)
    w = ho.get('witness') or {}
    if ho['set'] == 'kill':
        if 'vector' in w:
            v = w['vector']
            if not (isinstance(v, list) and len(v) == 9 and all(isinstance(x, int) and 0 <= x <= 255 for x in v)):
                raise Invalid('vector witness malformed')
            cb, cn = cblock(body)
            if cn != pnames:
                raise Invalid('vector witness needs pinned leg names')
            if 'loop' in w:
                cb, pb = set_loop(cb, w['loop']), set_loop(pblock, w['loop'])
            else:
                pb = pblock
            if tally_outputs(cb, cn, [v], tmp) == tally_outputs(pb, pnames, [v], tmp):
                raise Invalid('vector witness shows no difference')
        elif 'block' in w:
            if not (harness_failed(pristine, ppath, w['block'], tmp) and not harness_failed(body, cpath, w['block'], tmp)):
                raise Invalid('block witness: pinned harness must reject and copy harness accept')
        else:
            raise Invalid('kill copy without witness')
        return body
    if ho['set'] != 'accept':
        raise Invalid('set must be kill or accept')
    cb, cn = cblock(body)
    if sorted(cn) != sorted(pnames) or sorted(coperands(cb)) != sorted(pnames):
        raise Invalid('accept copy changes legs or loop operands')
    vs = sweep_vectors(9)
    if tally_outputs(cb, cn, [[dict(zip(pnames, v))[x] for x in cn] for v in vs], tmp) != tally_outputs(pblock, pnames, vs, tmp):
        raise Invalid('accept copy tally differs from pinned on the sweep')
    for i in range(9):
        for ops in (pnames[:i + 1] + pnames[i:], pnames[:i] + pnames[i + 1:]):
            if tally_outputs(set_loop(cb, ops), cn, [[0] * 9], tmp) != tally_outputs(set_loop(pblock, ops), pnames, [[0] * 9], tmp):
                raise Invalid('accept copy tally differs from pinned under stress')
    for blk in [pblock] + fault_blocks(pblock) + block_witnesses:
        if harness_failed(body, cpath, blk, tmp) != harness_failed(pristine, ppath, blk, tmp):
            raise Invalid('accept copy harness verdict differs from pinned')
    return body


# ------------------------------------------------------------ sandboxed tool run

def run_sandboxed(tool, copy):
    cmd = ['timeout', '600', 'bwrap', '--unshare-all', '--die-with-parent', '--new-session', '--clearenv',
           '--ro-bind', '/usr', '/usr', '--symlink', 'usr/bin', '/bin', '--symlink', 'usr/lib', '/lib',
           '--symlink', 'usr/lib', '/lib64', '--symlink', 'usr/bin', '/sbin', '--ro-bind', '/etc', '/etc',
           '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp', '--ro-bind', tool, '/t/tally-audit.py',
           '--ro-bind', copy, '/in/runner.sh', '--setenv', 'PATH', '/usr/bin', '--setenv', 'HOME', '/tmp',
           '--setenv', 'TMPDIR', '/tmp', '--setenv', 'LANG', 'C.UTF-8', '--chdir', '/tmp',
           'python3', '-I', '/t/tally-audit.py', '--runner', '/in/runner.sh']
    p = subprocess.run(cmd, capture_output=True, env={'PATH': '/usr/bin:/bin'})
    lines = p.stdout.decode('utf-8', 'replace').splitlines()
    rc = p.returncode
    if rc == 1 and any(x.startswith('TALLY_AUDIT: FAIL') for x in lines):
        outcome = 'KILL'
    elif rc == 0 and any(x.startswith('TALLY_AUDIT: PASS') for x in lines):
        outcome = 'ACCEPT'
    else:
        outcome = 'OTHER'
    last = next((x for x in reversed(lines) if x.startswith('TALLY_AUDIT:')), '')
    return outcome, rc, last


def adding_commit(lane, rev, path):
    r = git(lane, 'log', '--diff-filter=A', '--format=%H', rev, '--', path)
    hs = r.stdout.decode().split()
    return hs[-1] if hs else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--seed')
    ap.add_argument('--jobs', type=int, default=4)
    a = ap.parse_args()
    lane, work = os.path.abspath(a.lane), os.path.abspath(a.work)
    if os.path.exists(work) and os.listdir(work):
        print('C1_R32V2: --work must be empty or absent', file=sys.stderr)
        return 2
    os.makedirs(work, exist_ok=True)
    r = git(lane, 'rev-parse', '--verify', a.rev + '^{commit}')
    if r.returncode:
        print('C1_R32V2: cannot resolve rev', file=sys.stderr)
        return 2
    rev = r.stdout.decode().strip()
    seed = a.seed or secrets.token_hex(8)
    rng = random.Random(int(seed, 16))
    pinned = git(lane, 'show', v1.PIN_REV + ':' + v1.RUNNER)
    if pinned.returncode or hashlib.sha256(pinned.stdout).hexdigest() != v1.PINNED_RUNNER_SHA:
        print('C1_R32V2: pinned runner unavailable', file=sys.stderr)
        return 2
    at_rev = git(lane, 'show', rev + ':' + v1.RUNNER)
    runner_sha_ok = int(at_rev.returncode == 0 and hashlib.sha256(at_rev.stdout).hexdigest() == v1.PINNED_RUNNER_SHA)
    text = pinned.stdout.decode('utf-8')
    try:
        kill = [('v1', l, b) for l, b in v1.frozen_kill(text) + v1.generated_kill(text, rng)]
        accept = [('v1', l, b) for l, b in v1.frozen_accept(text) + v1.generated_accept(text, rng)]
    except v1.CounterError as e:
        print('C1_R32V2: ' + str(e), file=sys.stderr)
        return 2
    tmp = os.path.join(work, 'validate')
    os.makedirs(tmp)
    ppath = os.path.join(tmp, 'pinned.sh')
    with open(ppath, 'w', encoding='utf-8') as f:
        f.write(text)
    # held-out set at REV
    freeze = adding_commit(lane, rev, SELF_PATH)
    ls = git(lane, 'ls-tree', '--name-only', rev, HELDOUT_DIR + '/')
    files = sorted(x for x in ls.stdout.decode().split('\n') if x.endswith('.json'))
    after = int(freeze is not None)
    hos = []
    for path in files:
        add = adding_commit(lane, rev, path)
        if freeze is None or add is None or add == freeze or \
                git(lane, 'merge-base', '--is-ancestor', freeze, add).returncode:
            after = 0
        try:
            hos.append((path, json.loads(git(lane, 'show', rev + ':' + path).stdout)))
        except ValueError:
            hos.append((path, None))
    witnesses = [h['witness']['block'] for _, h in hos
                 if isinstance(h, dict) and h.get('set') == 'kill' and isinstance(h.get('witness'), dict)
                 and isinstance(h['witness'].get('block'), str)]
    invalid = 0
    ho_n = {'kill': 0, 'accept': 0}
    for path, h in hos:
        try:
            if not isinstance(h, dict) or not isinstance(h.get('edits'), list) or h.get('set') not in ('kill', 'accept'):
                raise Invalid('schema')
            body = validate(h, text, ppath, tmp, witnesses)
        except (Invalid, KeyError, TypeError, ValueError) as e:
            invalid += 1
            print('HELDOUT file=%s valid=0 reason=%r' % (path, str(e)[:160]))
            continue
        ho_n[h['set']] += 1
        print('HELDOUT file=%s valid=1 set=%s id=%s author=%s' % (path, h['set'], h.get('id'), h.get('author')))
        (kill if h['set'] == 'kill' else accept).append(('ho', os.path.basename(path), body))
    tool_blob = git(lane, 'show', rev + ':tools/tally-audit.py')
    tool_sha_ok = int(tool_blob.returncode == 0 and hashlib.sha256(tool_blob.stdout).hexdigest() == TOOL_SHA256)
    tool = os.path.join(work, 'tool-' + secrets.token_hex(4) + '.py')
    with open(tool, 'wb') as f:
        f.write(tool_blob.stdout if tool_blob.returncode == 0 else b'')
    cdir = os.path.join(work, 'c-' + secrets.token_hex(4))
    os.makedirs(cdir)
    copies = []
    for set_name, group in (('kill', kill), ('accept', accept)):
        for src, label, body in group:
            d = os.path.join(cdir, secrets.token_hex(8))
            os.makedirs(d)
            p = os.path.join(d, 'r.sh')
            with open(p, 'w', encoding='utf-8') as f:
                f.write(body)
            copies.append((set_name, src, label, p, hashlib.sha256(body.encode()).hexdigest()))
    results = {}
    if tool_blob.returncode == 0:
        order = list(copies)
        random.Random(secrets.randbits(64)).shuffle(order)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            futs = {ex.submit(run_sandboxed, tool, c[3]): c for c in order}
            for fu in concurrent.futures.as_completed(futs):
                results[futs[fu][3]] = fu.result()
    cnt = {('v1', 'kill'): 0, ('v1', 'accept'): 0, ('ho', 'kill'): 0, ('ho', 'accept'): 0}
    for set_name, src, label, p, sha in copies:
        outcome, rc, last = results.get(p, ('OTHER', 'no-tool', ''))
        if (set_name == 'kill' and outcome == 'KILL') or (set_name == 'accept' and outcome == 'ACCEPT'):
            cnt[(src, set_name)] += 1
        print('COPY src=%s set=%s id=%s outcome=%s exit=%s sha256=%s last=%r' % (src, set_name, label, outcome, rc, sha[:16], last[:160]))
    ok = (cnt[('v1', 'kill')] == 18 and cnt[('v1', 'accept')] == 8 and cnt[('ho', 'kill')] == ho_n['kill']
          and cnt[('ho', 'accept')] == ho_n['accept'] and ho_n['kill'] >= MIN_HO and ho_n['accept'] >= MIN_HO
          and tool_sha_ok and runner_sha_ok and after)
    print('C1_R32V2: v1_kill=%d/18 v1_accept=%d/8 ho_kill=%d/%d ho_accept=%d/%d ho_invalid=%d tool_sha_ok=%d runner_sha_ok=%d '
          'heldout_after_freeze=%d seed=%s rev=%s C1_R32V2_PASS=%s'
          % (cnt[('v1', 'kill')], cnt[('v1', 'accept')], cnt[('ho', 'kill')], ho_n['kill'], cnt[('ho', 'accept')], ho_n['accept'],
             invalid, tool_sha_ok, runner_sha_ok, after, seed, rev, 'true' if ok else 'false'))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
