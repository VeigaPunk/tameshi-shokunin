#!/usr/bin/env python3
"""Round 32 C1 counter (operability: runner tally audit), frozen before any data seat.

Usage: c1-measure.py --lane LANE --rev REV --work EMPTY_DIR [--seed HEX] [--jobs N]

Predicate (label C1_R32_PASS), the same sentence as contract.json `predicate`:
  C1 passes at REV iff the committed `tools/tally-audit.py` at REV, run as
  `python3 tally-audit.py --runner COPY`, exits 1 with a stdout line beginning
  `TALLY_AUDIT: FAIL` on every one of the 18 must-kill runner copies, exits 0 with a
  stdout line beginning `TALLY_AUDIT: PASS` on every one of the 8 must-accept runner
  copies, and REV's `tools/mutate-and-run.sh` has sha256 PINNED_RUNNER_SHA.

Copies are built from the pinned runner bytes (base blob, sha256 PINNED_RUNNER_SHA):
  - 9 frozen must-kill copies: the 8 real survivors of round-30 seat MutateHead
    (T08 N05 H03 H04 H05 N01 N02 N03, exact edits from .ufo/waves/round-30/wC/MutateHead.md)
    plus D01 (one tally operand duplicated, another dropped: the per-leg defect).
  - 9 generated must-kill copies, one per family above, drawn from a seeded RNG at run
    time (the seed is printed; --seed replays it). They are not knowable when the tool is
    written, so a tool keyed on the frozen copies' bytes or hashes cannot meet them.
  - 6 frozen must-accept copies: pristine, T07 (equivalent guard), operands reversed,
    decoy comments carrying every frozen mutant's new text, cosmetic tally edit,
    harness variable renamed; plus 2 generated: random operand permutation, nonce comments.
Each copy is written under an opaque random file name in WORK; the tool receives only the
path. The tool never sees a label, a set name or the seed.

Outcome per copy: KILL iff exit 1 and a stdout line starts `TALLY_AUDIT: FAIL`;
ACCEPT iff exit 0 and a stdout line starts `TALLY_AUDIT: PASS`; anything else is OTHER.
A must-kill copy counts only as KILL; a must-accept copy counts only as ACCEPT.

Prints one `COPY` line per copy, then
  `C1_R32: kill=K/18 accept=A/8 other=O runner_sha_ok=0|1 tool_present=0|1 seed=S rev=REV C1_R32_PASS=true|false`.
Exit 0 iff PASS; 1 iff evaluated and not PASS; 2 on counter error (bad rev, anchor missing).
"""
import argparse
import concurrent.futures
import hashlib
import os
import random
import secrets
import subprocess
import sys

PINNED_RUNNER_SHA = 'a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9'
PIN_REV = 'e24688b2ff6cca1c9ad20e112f02c629b8597ff8'  # round-32 base; its runner blob has PINNED_RUNNER_SHA
RUNNER = 'tools/mutate-and-run.sh'
TOOL = 'tools/tally-audit.py'
N_KILL, N_ACCEPT = 18, 8

NAMES = ['st_js', 'st_kagi', 'st_tsu', 'st_mado', 'st_checklist', 'st_claims', 'st_roundgate',
         'st_sourcescheck', 'st_citecheck']
LOOP = '  for st in ' + ' '.join('"$%s"' % n for n in NAMES) + '; do\n'
ARM0 = '      0) npass=$((npass + 1)) ;;\n'
ARM1 = '      1) nfail=$((nfail + 1)) ;;\n'
GUARD = '  if (( npass + nfail + nsetup != nlegs )); then\n'
CMP = '    [[ $rc -eq $want_rc && "${out%%$\'\\n\'*}" == "$want_line" ]]\n'
POS = '    for ti in 0 1 2 3 4 5 6 7 8; do\n'
V11 = "  for tvec in '1 1 0 0 0 0 0 0 0:1:REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)' \\\n"
V22 = "    '2 2 0 0 0 0 0 0 0:2:REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)' \\\n"
V12 = "    '1 2 0 0 0 0 0 0 0:1:REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)' \\\n"
V30 = "    '3 0 0 0 0 0 0 0 0:2:REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)'; do\n"
STRESS_IF = '  [[ "$tblock" != "$tblock_full" ]] &&\n'
STRESS_CALL = "    tally_line 2 'REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)' 0 0 0 0 0 0 0 0 0\n"
GUARD_NOTE = '  # of a mutation report are sums of its per-state counts).\n'
TBFULL = '  local tblock_full=$tblock\n'
MAIN = '# -------------------------------------------------------------------- main\n'


class CounterError(Exception):
    pass


def rep(text, old, new):
    if text.count(old) != 1:
        raise CounterError('anchor count %d != 1: %r' % (text.count(old), old[:80]))
    return text.replace(old, new, 1)


def loop_with(ops):
    return '  for st in ' + ' '.join('"$%s"' % n for n in ops) + '; do\n'


def frozen_kill(t):
    return [
        ('T08', rep(t, ARM1, ARM1 + '      4) npass=$((npass + 1)) ;;\n')),
        ('N05', rep(t, GUARD, GUARD.replace('!= nlegs', '< nlegs'))),
        ('H03', rep(t, CMP, '    [[ $rc -eq $want_rc ]]\n')),
        ('H04', rep(t, CMP, CMP + '    rc=$?\n')),
        ('H05', rep(t, POS, '    for ti in 0 1 2 3 4 5 6 7 7; do\n')),
        ('N01', rep(t, V12, '')),
        ('N02', rep(t, STRESS_IF, STRESS_IF.replace('&&', '||'))),
        ('N03', rep(t, CMP, CMP.replace(' && ', ' || '))),
        ('D01', rep(t, LOOP, loop_with(NAMES[:8] + ['st_js']))),
    ]


def generated_kill(t, rng):
    out = []
    k = rng.randint(2, 255)
    out.append(('gT08(arm=%d)' % k, rep(t, ARM1, ARM1 + '      %d) npass=$((npass + 1)) ;;\n' % k)))
    form = rng.choice(['< nlegs', '< nlegs + 0', '<= nlegs - 1'])
    out.append(('gN05(%s)' % form, rep(t, GUARD, GUARD.replace('!= nlegs', form))))
    cmp_forms = ['    [[ $rc -eq $want_rc ]]\n',
                 '    [[ $rc -eq $want_rc && -n "$out" ]]\n',
                 '    [[ $rc -eq $want_rc && "${out:0:11}" == "${want_line:0:11}" ]]\n']
    i = rng.randrange(len(cmp_forms))
    out.append(('gH03(form=%d)' % i, rep(t, CMP, cmp_forms[i])))
    tail = rng.choice(['    rc=$?\n', '    true\n', '    :\n'])
    out.append(('gH04(%s)' % tail.strip(), rep(t, CMP, CMP + tail)))
    p = rng.randrange(9)
    q = rng.choice([x for x in range(9) if x != p])
    pos = [str(x) for x in range(9)]
    pos[p] = str(q)
    out.append(('gH05(drop=%d,dup=%d)' % (p, q), rep(t, POS, '    for ti in ' + ' '.join(pos) + '; do\n')))
    v = rng.randrange(4)
    if v == 0:
        body = rep(t, V11, '  for tvec in \\\n')
    elif v == 1:
        body = rep(t, V22, '')
    elif v == 2:
        body = rep(t, V12, '')
    else:
        body = rep(t, V12 + V30, V12.replace("' \\\n", "'; do\n"))
    out.append(('gN01(vector=%d)' % v, body))
    if rng.randrange(2):
        out.append(('gN02(or)', rep(t, STRESS_IF, STRESS_IF.replace('&&', '||'))))
    else:
        out.append(('gN02(true)', rep(t, STRESS_IF + STRESS_CALL, STRESS_IF + '    true\n')))
    if rng.randrange(2):
        out.append(('gN03(or)', rep(t, CMP, CMP.replace(' && ', ' || '))))
    else:
        out.append(('gN03(split)', rep(t, CMP, '    [[ $rc -eq $want_rc ]] || [[ "${out%%$\'\\n\'*}" == "$want_line" ]]\n')))
    a = rng.randrange(9)
    b = rng.choice([x for x in range(9) if x != a])
    ops = list(NAMES)
    ops[a] = NAMES[b]
    out.append(('gD01(drop=%s,dup=%s)' % (NAMES[a], NAMES[b]), rep(t, LOOP, loop_with(ops))))
    return out


def frozen_accept(t):
    decoy = ''.join('# decoy: ' + line + '\n' for line in (
        '      4) npass=$((npass + 1)) ;;', '  if (( npass + nfail + nsetup < nlegs )); then',
        '    [[ $rc -eq $want_rc ]]', '    rc=$?', '    for ti in 0 1 2 3 4 5 6 7 7; do',
        '  [[ "$tblock" != "$tblock_full" ]] ||',
        '    [[ $rc -eq $want_rc || "${out%%$\'\\n\'*}" == "$want_line" ]]',
        '  for st in ' + ' '.join('"$%s"' % n for n in NAMES[:8] + ['st_js']) + '; do'))
    renamed = t
    if renamed.count('tgot') != 6:
        raise CounterError('tgot count %d != 6' % renamed.count('tgot'))
    renamed = renamed.replace('tgot', 'tcount')
    return [
        ('B0-pristine', t),
        ('B1-T07', rep(t, GUARD, '  if (( npass != nlegs )); then\n')),
        ('B2-reversed', rep(t, LOOP, loop_with(list(reversed(NAMES))))),
        ('B3-decoys', rep(t, MAIN, decoy + MAIN)),
        ('B4-cosmetic', rep(t, ARM0, '      0) npass=$(( npass + 1 )) ;; # pass\n')),
        ('B5-renamed', renamed),
    ]


def generated_accept(t, rng):
    perm = list(NAMES)
    while perm == NAMES:
        rng.shuffle(perm)
    n1, n2 = '%016x' % rng.getrandbits(64), '%016x' % rng.getrandbits(64)
    nonce = rep(t, GUARD_NOTE, GUARD_NOTE + '  # nonce ' + n1 + '\n')
    nonce = rep(nonce, TBFULL, TBFULL + '  # nonce ' + n2 + '\n')
    return [('gB6-permuted', rep(t, LOOP, loop_with(perm))), ('gB7-nonce', nonce)]


def git(lane, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['GIT_OPTIONAL_LOCKS'] = '0'
    return subprocess.run(['git', '-C', lane, *args], capture_output=True, env=env)


def run_tool(tool, copy, work):
    d = os.path.join(work, 'run-' + secrets.token_hex(8))
    os.makedirs(os.path.join(d, 'tmp'))
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'HOME': d, 'TMPDIR': os.path.join(d, 'tmp'),
           'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8'}
    try:
        p = subprocess.run([sys.executable, '-I', tool, '--runner', copy], cwd=d, env=env,
                           capture_output=True, timeout=600)
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--seed')
    ap.add_argument('--jobs', type=int, default=4)
    a = ap.parse_args()
    lane = os.path.abspath(a.lane)
    work = os.path.abspath(a.work)
    if os.path.exists(work) and os.listdir(work):
        print('C1_R32: --work must be empty or absent', file=sys.stderr)
        return 2
    os.makedirs(work, exist_ok=True)
    r = git(lane, 'rev-parse', '--verify', a.rev + '^{commit}')
    if r.returncode:
        print('C1_R32: cannot resolve rev', file=sys.stderr)
        return 2
    rev = r.stdout.decode().strip()
    seed = a.seed or secrets.token_hex(8)
    rng = random.Random(int(seed, 16))
    pinned = git(lane, 'show', PIN_REV + ':' + RUNNER)
    if pinned.returncode or hashlib.sha256(pinned.stdout).hexdigest() != PINNED_RUNNER_SHA:
        print('C1_R32: pinned runner blob unavailable or wrong sha', file=sys.stderr)
        return 2
    at_rev = git(lane, 'show', rev + ':' + RUNNER)
    runner_sha_ok = int(at_rev.returncode == 0 and hashlib.sha256(at_rev.stdout).hexdigest() == PINNED_RUNNER_SHA)
    text = pinned.stdout.decode('utf-8')
    try:
        kill = frozen_kill(text) + generated_kill(text, rng)
        accept = frozen_accept(text) + generated_accept(text, rng)
    except CounterError as e:
        print('C1_R32: ' + str(e), file=sys.stderr)
        return 2
    if len(kill) != N_KILL or len(accept) != N_ACCEPT:
        print('C1_R32: copy set size wrong', file=sys.stderr)
        return 2
    for label, body in kill:
        if body == text:
            print('C1_R32: must-kill copy %s equals pristine' % label, file=sys.stderr)
            return 2
    tool_blob = git(lane, 'show', rev + ':' + TOOL)
    tool_present = int(tool_blob.returncode == 0)
    copies = []
    cdir = os.path.join(work, 'copies')
    os.makedirs(cdir)
    for set_name, group in (('kill', kill), ('accept', accept)):
        for label, body in group:
            path = os.path.join(cdir, secrets.token_hex(8) + '.sh')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(body)
            copies.append((set_name, label, path, hashlib.sha256(body.encode()).hexdigest()))
    results = {}
    if tool_present:
        tdir = os.path.join(work, 'tool')
        os.makedirs(tdir)
        tool = os.path.join(tdir, 'tally-audit.py')
        with open(tool, 'wb') as f:
            f.write(tool_blob.stdout)
        order = list(copies)
        random.Random(secrets.randbits(64)).shuffle(order)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            futs = {ex.submit(run_tool, tool, c[2], work): c for c in order}
            for fu in concurrent.futures.as_completed(futs):
                results[futs[fu][2]] = fu.result()
    k = acc = other = 0
    for set_name, label, path, sha in copies:
        outcome, rc, last = results.get(path, ('OTHER', 'no-tool', ''))
        if set_name == 'kill' and outcome == 'KILL':
            k += 1
        elif set_name == 'accept' and outcome == 'ACCEPT':
            acc += 1
        else:
            other += 1
        print('COPY set=%s id=%s outcome=%s exit=%s sha256=%s last=%r' % (set_name, label, outcome, rc, sha[:16], last[:160]))
    ok = k == N_KILL and acc == N_ACCEPT and runner_sha_ok == 1 and tool_present == 1
    print('C1_R32: kill=%d/%d accept=%d/%d other=%d runner_sha_ok=%d tool_present=%d seed=%s rev=%s C1_R32_PASS=%s'
          % (k, N_KILL, acc, N_ACCEPT, other, runner_sha_ok, tool_present, seed, rev, 'true' if ok else 'false'))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
