#!/usr/bin/env python3
"""Round-46 no-harm gate — the executable behind QUALITY draft criterion 88.

Criterion (draft 88): a frozen contract's `no_harm` monitors are each run at the base
before the freeze and printed green in a committed receipt; a monitor red at base is
refused, and a round-bound counter (one that grades any newest block that is not its
own round) is not a monitor.

The gate reads the contract's `no_harm` text, resolves a monitors list, runs every
monitor command at REV inside LANE (read-only: nothing in the lane is written, no git
index or jj state is touched — children get PYTHONDONTWRITEBYTECODE=1 and
GIT_OPTIONAL_LOCKS=0), and exits 0 only if every monitor printed ok. Every monitor
prints one line, in the format .ufo/evidence/round-46/no-harm.sh already uses:

  NOHARM <name> <observed> <ok|RED>

and every failure adds a named refusal plus its reason:

  RED <name>
  WHY <name> <reason>

Usage:

  python3 no-harm-gate.py --contract CONTRACT.json --lane LANE --rev REV [--monitors-file F]
  python3 no-harm-gate.py --list
  python3 no-harm-gate.py --selftest

Monitors source, in order:
  * --monitors-file F, JSON: {"monitors": [{"name": ..., "command": ..., ...}]}
  * --monitors-file F, not JSON: a shell script, run as `bash F LANE REV`, whose
    NOHARM lines are parsed and enforced (this is how .ufo/evidence/round-46/no-harm.sh
    is consumed as "the real list")
  * no file: DEFAULT_MONITORS, the hard-coded mapping of the six monitor names of
    .ufo/evidence/round-46/no-harm.sh to their commands, their expectations and the
    contract phrase each one discharges.

A monitor entry:
  name              required, unique
  command           required; run with `bash -c` in LANE, with LANE and REV in the env
  expect            exact match against stdout, trailing newlines stripped — the
                    comparison no-harm.sh itself makes (`[ "$D" = "..." ]`)
  expect_contains   every listed substring must appear in stdout
  expect_min        the last integer token of stdout must be >= this value
  contract_phrase   must appear (case-insensitively) in the contract's `no_harm` text;
                    absent means the monitor is not declared by the contract
  timeout           per-monitor seconds (default --timeout)
With no expect/expect_contains/expect_min the monitor is ok iff its last non-empty
line ends in the token `ok`. A non-zero exit, a timeout or a missing token is RED:
a gate that accepts an exit code or a substring on its own is not a gate.

Exit: 0 iff every monitor printed ok; 1 otherwise (one RED line per failing monitor,
the last line NO_HARM_GATE_PASS=false); 2 only for argparse misuse.

Falsifier — the round-44 record-agreement counter is red at the round-46 base by
construction and is NOT a monitor (contract `no_harm`, round-45 spot-check defect 1),
so the gate must refuse it:

  cat > /tmp/falsifier-monitors.json <<'JSON'
  {"monitors": [{"name": "r44-record-agreement",
                 "command": "python3 .ufo/evidence/round-44/calibration/measure.py --lane \"$LANE\" --rev \"$REV\" --freeze ba01973c73ad7de60e5bd19ae08255a1b7ef917e",
                 "expect_contains": ["C2_R44_PASS=true"]}]}
  JSON
  python3 .ufo/evidence/round-46/quality/no-harm-gate.py \
    --contract .ufo/evidence/round-46/contract.json \
    --lane . --rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d \
    --monitors-file /tmp/falsifier-monitors.json
  # -> NOHARM r44-record-agreement ... C2_R44_PASS=false RED ; RED r44-record-agreement ; exit 1
"""
import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE_ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))

# The six monitors of .ufo/evidence/round-46/no-harm.sh, name -> command, verbatim
# except that the observed value is printed instead of compared with `[ ... ] && s=ok`
# inside the shell: the gate makes that comparison itself, so a red monitor is named.
_CMD_D = (
    r'''D=$(git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; '''
    r'''n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); '''
    r'''print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'); printf '%s\n' "$D"'''
)
_CMD_COLDREAD = (
    r'''python3 .ufo/evidence/round-21/coldread/measure.py --repo "$LANE" --rev "$REV" 2>/dev/null '''
    r'''| python3 -c 'import json,sys; d=json.load(sys.stdin); print("score=%s box3_full_page=%s" '''
    r'''% (d["calibration_restraint_score"], d["coldread"]["box3_full_page"]))' '''
)
_CMD_R45_FRESHNESS = (
    r'''python3 .ufo/evidence/round-45/freshness/measure.py --lane "$LANE" --rev "$REV" | tail -1 '''
    r'''| grep -oE 'population=[0-9]+|fresh=[0-9]+|C1_R45_PASS=[a-z]+' | tr '\n' ' ' '''
)
_CMD_R45_COVERAGE = (
    r'''python3 .ufo/evidence/round-45/coverage/measure.py --lane "$LANE" --rev "$REV" | tail -1 '''
    r'''| grep -oE 'rows=[0-9]+|entries=[0-9]+|C2_R45_PASS=[a-z]+' | tr '\n' ' ' '''
)
_CMD_S160 = r'''git show "$REV:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S160 ' '''
_CMD_REGISTRY = r'''git show "$REV:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S[0-9]{3,} \|' '''

DEFAULT_MONITORS = [
    {'name': 'commandD', 'command': _CMD_D,
     'expect': 'recorded_cases=9 depth_score=9', 'contract_phrase': 'command D 9'},
    {'name': 'coldread', 'command': _CMD_COLDREAD,
     'expect': 'score=6 box3_full_page=False', 'contract_phrase': 'coldread restraint 6'},
    {'name': 'r45-freshness', 'command': _CMD_R45_FRESHNESS,
     'expect': 'population=73 fresh=71 C1_R45_PASS=true ',
     'contract_phrase': 'fresh=71'},
    {'name': 'r45-coverage', 'command': _CMD_R45_COVERAGE,
     'expect': 'rows=2 entries=2 C2_R45_PASS=true ', 'contract_phrase': 'rows=2 entries=2'},
    {'name': 'S160-count', 'command': _CMD_S160,
     'expect': '1', 'contract_phrase': 'S160 count 1'},
    {'name': 'registry-rows-not-below-117', 'command': _CMD_REGISTRY,
     'expect_min': 117, 'contract_phrase': 'registry rows not below 117'},
]

NOHARM_LINE = re.compile(r'^NOHARM\s+(\S+)\s+(.*?)\s+(ok|RED)\s*$')
INT = re.compile(r'-?\d+')


def child_env(lane, rev):
    """Read-only child environment: no bytecode writes, no git optional locks."""
    env = dict(os.environ)
    env.update(LANE=lane, REV=rev, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    return env


def run(cmd, cwd, env, timeout):
    """(rc, stdout, stderr) with rc None on timeout/exec failure. Never writes."""
    try:
        p = subprocess.run(['bash', '-c', cmd], cwd=cwd, env=env,
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ''
        if isinstance(out, bytes):
            out = out.decode('utf-8', 'replace')
        return None, out, 'timeout after %ss' % timeout
    except OSError as exc:
        return None, '', 'cannot run: %s' % exc
    return p.returncode, p.stdout, p.stderr


def observed(out):
    """One-line rendering of a monitor's stdout, for the NOHARM line."""
    text = ' | '.join(line.strip() for line in out.strip().splitlines() if line.strip())
    if len(text) > 300:
        text = text[:297] + '...'
    return text or '(no output)'


def judge(entry, rc, out):
    """Reasons this monitor is not ok; [] means ok."""
    if rc is None:
        return ['did not finish']
    reasons = []
    if rc != 0:
        reasons.append('exit %d' % rc)
    checks = 0
    if 'expect' in entry:
        checks += 1
        if out.rstrip('\n') != entry['expect']:
            reasons.append('expect %r' % entry['expect'])
    if entry.get('expect_contains'):
        checks += 1
        for token in entry['expect_contains']:
            if token not in out:
                reasons.append('missing token %r' % token)
    if entry.get('expect_min') is not None:
        checks += 1
        nums = INT.findall(out.strip())
        if not nums or int(nums[-1]) < int(entry['expect_min']):
            reasons.append('expect_min %d' % int(entry['expect_min']))
    if checks == 0:
        lines = [line for line in out.splitlines() if line.strip()]
        if not lines or not lines[-1].rstrip().endswith('ok'):
            reasons.append('last line does not end in ok')
    return reasons


def load_contract(path):
    """(no_harm_text, error)."""
    try:
        with open(path, 'r') as fh:
            doc = json.load(fh)
    except OSError as exc:
        return None, 'cannot read %s: %s' % (path, exc)
    except ValueError as exc:
        return None, '%s is not JSON: %s' % (path, exc)
    if not isinstance(doc, dict):
        return None, '%s is not a JSON object' % path
    text = doc.get('no_harm')
    if not isinstance(text, str) or not text.strip():
        return None, '%s has no non-empty string `no_harm`' % path
    return text, None


def resolve_monitors(path):
    """(mode, monitors, error). mode is 'json', 'shell' or 'default'."""
    if path is None:
        return 'default', [dict(entry) for entry in DEFAULT_MONITORS], None
    if not os.path.exists(path):
        return 'json', None, 'monitors file not found: %s' % path
    try:
        with open(path, 'r') as fh:
            raw = fh.read()
    except OSError as exc:
        return 'json', None, 'cannot read %s: %s' % (path, exc)
    try:
        doc = json.loads(raw)
    except ValueError:
        return 'shell', None, None
    if not isinstance(doc, dict) or not isinstance(doc.get('monitors'), list):
        return 'json', None, '%s is JSON without a `monitors` list' % path
    return 'json', doc['monitors'], None


def validate(monitors):
    """(valid_entries, [(name, reason)]) — a malformed entry is a refusal, not a skip."""
    good, bad = [], []
    seen = set()
    for i, entry in enumerate(monitors):
        if not isinstance(entry, dict):
            bad.append(('monitors[%d]' % i, 'not an object'))
            continue
        name = entry.get('name')
        if not isinstance(name, str) or not name.strip():
            bad.append(('monitors[%d]' % i, 'no name'))
            continue
        if name in seen:
            bad.append((name, 'duplicate monitor name'))
            continue
        seen.add(name)
        if not isinstance(entry.get('command'), str) or not entry['command'].strip():
            bad.append((name, 'no command'))
            continue
        good.append(entry)
    return good, bad


def emit_reds(lines, reds):
    """One `RED <name>` line per failing monitor, reasons joined on its WHY line."""
    order, reasons = [], {}
    for name, reason in reds:
        if name not in reasons:
            order.append(name)
            reasons[name] = []
        if reason not in reasons[name]:
            reasons[name].append(reason)
    for name in order:
        lines.append('RED %s' % name)
        lines.append('WHY %s %s' % (name, '; '.join(reasons[name])))
    return order


def gate(contract_path, lane, rev, monitors_file, timeout):
    """(exit_code, report_lines)."""
    lines = []
    reds = []          # (name, reason)
    noharm = []        # rendered NOHARM lines
    phrase_checks = [0, 0]  # checked, satisfied

    text, err = load_contract(contract_path)
    if err:
        lines.append('RED contract')
        lines.append('WHY contract %s' % err)
        lines.append('NO_HARM_GATE_PASS=false')
        return 1, lines
    if not os.path.isdir(lane):
        lines.append('RED lane')
        lines.append('WHY lane not a directory: %s' % lane)
        lines.append('NO_HARM_GATE_PASS=false')
        return 1, lines

    env = child_env(os.path.abspath(lane), rev)
    rc, _, _ = run('git rev-parse --verify --quiet %s^{commit}' % shlex.quote(rev),
                   lane, env, min(60.0, timeout))
    if rc != 0:
        lines.append('RED revision')
        lines.append('WHY revision %s does not resolve in %s' % (rev, lane))
        lines.append('NO_HARM_GATE_PASS=false')
        return 1, lines

    mode, monitors, err = resolve_monitors(monitors_file)
    if err:
        lines.append('RED monitors-file')
        lines.append('WHY monitors-file %s' % err)
        lines.append('NO_HARM_GATE_PASS=false')
        return 1, lines

    if mode == 'shell':
        src = os.path.abspath(monitors_file)
        rc, out, serr = run('bash %s %s %s' % (shlex.quote(src), shlex.quote(os.path.abspath(lane)),
                                               shlex.quote(rev)), lane, env, timeout)
        rows = []
        for line in out.splitlines():
            match = NOHARM_LINE.match(line)
            if match:
                rows.append(match.groups())
        if rc is None:
            reds.append(('monitors-file', 'did not finish: %s' % serr))
        elif not rows:
            reds.append(('no-monitors', 'the script printed no NOHARM line'))
        elif rc != 0:
            reds.append(('monitors-file', 'script exit %d' % rc))
        for name, value, verdict in rows:
            noharm.append('NOHARM %s %s %s' % (name, value, verdict))
            if verdict != 'ok':
                reds.append((name, 'monitor printed RED'))
        lines.extend(noharm)
        red_names = emit_reds(lines, reds)
        lines.append('monitors=%d ok=%d red=%d contract_no_harm_chars=%d'
                     % (len(rows),
                        len([r for r in rows if r[2] == 'ok' and r[0] not in red_names]),
                        len(red_names), len(text)))
        lines.append('NO_HARM_GATE_PASS=%s' % ('true' if not reds else 'false'))
        return (0 if not reds else 1), lines

    good, bad = validate(monitors)
    for name, reason in bad:
        reds.append((name, reason))
    if not good and not bad:
        reds.append(('no-monitors', 'the monitors list is empty: nothing to prove'))

    for entry in good:
        name = entry['name']
        phrase = entry.get('contract_phrase')
        if phrase:
            phrase_checks[0] += 1
            if phrase.lower() in text.lower():
                phrase_checks[1] += 1
            else:
                reds.append((name, 'contract no_harm does not declare %r' % phrase))
        limit = float(entry.get('timeout', timeout))
        rc, out, serr = run(entry['command'], lane, env, limit)
        reasons = judge(entry, rc, out)
        if rc is None and serr:
            reasons.append(serr)
        noharm.append('NOHARM %s %s %s' % (name, observed(out), 'ok' if not reasons else 'RED'))
        for reason in reasons:
            reds.append((name, reason))

    lines.extend(noharm)
    red_names = emit_reds(lines, reds)
    ok_count = len([line for line in noharm
                    if line.endswith(' ok') and line.split()[1] not in red_names])
    lines.append('monitors=%d ok=%d red=%d contract_no_harm_chars=%d contract_phrases=%d/%d'
                 % (len(noharm), ok_count, len(red_names),
                    len(text), phrase_checks[1], phrase_checks[0]))
    lines.append('NO_HARM_GATE_PASS=%s' % ('true' if not reds else 'false'))
    return (0 if not reds else 1), lines


# --------------------------------------------------------------------------- selftest

DEFAULT_CONTRACT = {
    'no_harm': ('every monitor prints ok (command D 9, coldread restraint 6, fresh=71, '
                'rows=2 entries=2, S160 count 1, registry rows not below 117)'),
}


def _write(path, text):
    with open(path, 'w') as fh:
        fh.write(text)


def _fixture_repo(root):
    """A throwaway git repo under root with one commit; toplevel is verified first."""
    repo = os.path.join(root, 'repo')
    os.makedirs(repo)
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               GIT_AUTHOR_NAME='tameshi-r46-selftest', GIT_AUTHOR_EMAIL='selftest@invalid',
               GIT_COMMITTER_NAME='tameshi-r46-selftest', GIT_COMMITTER_EMAIL='selftest@invalid')
    subprocess.run(['git', '-C', repo, 'init', '-q'], env=env, check=True)
    top = subprocess.run(['git', '-C', repo, 'rev-parse', '--show-toplevel'],
                         env=env, capture_output=True, text=True, check=True).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise SystemExit('selftest: fixture toplevel %s != %s' % (top, repo))
    _write(os.path.join(repo, 'README'), 'selftest fixture\n')
    subprocess.run(['git', '-C', repo, 'add', 'README'], env=env, check=True)
    subprocess.run(['git', '-C', repo, 'commit', '-q', '-m', 'selftest fixture'],
                   env=env, check=True)
    rev = subprocess.run(['git', '-C', repo, 'rev-parse', 'HEAD'],
                         env=env, capture_output=True, text=True, check=True).stdout.strip()
    return repo, rev


def selftest():
    root = tempfile.mkdtemp(prefix='tameshi-r46-no-harm-gate-')
    repo, rev = _fixture_repo(root)
    bare = os.path.join(root, 'not-a-repo')
    os.makedirs(bare)
    results = []

    def case(name, monitors, want_rc, contains=(), absent=(), contract=None,
             script=False, timeout=None, lane=None, rev_arg=None, mfile=None):
        d = os.path.join(root, 'case-' + name)
        os.makedirs(d)
        cp = os.path.join(d, 'contract.json')
        _write(cp, json.dumps(DEFAULT_CONTRACT if contract is None else contract))
        argv = ['--contract', cp, '--lane', lane or repo, '--rev', rev_arg or rev]
        if mfile is not None:
            argv += ['--monitors-file', mfile]
        elif monitors is not None:
            mp = os.path.join(d, 'monitors.sh' if script else 'monitors.json')
            _write(mp, monitors if script else json.dumps(monitors))
            argv += ['--monitors-file', mp]
        if timeout is not None:
            argv += ['--timeout', str(timeout)]
        proc = subprocess.run([sys.executable, os.path.abspath(__file__)] + argv,
                              capture_output=True, text=True, cwd=root)
        out = proc.stdout + proc.stderr
        ok = (proc.returncode == want_rc
              and all(token in out for token in contains)
              and not any(token in out for token in absent))
        results.append((name, ok))
        print('SELFTEST %-26s rc=%d want=%d %s' % (name, proc.returncode, want_rc,
                                                   'PASS' if ok else 'FAIL'))
        if not ok:
            for line in out.splitlines():
                print('    | %s' % line)
        return out

    # 1-2: the green path, and the same path through an exact expectation.
    case('json-all-ok', {'monitors': [
        {'name': 'm1', 'command': "printf 'A=1\\n'", 'expect': 'A=1'},
        {'name': 'm2', 'command': "printf 'B=2\\n'", 'expect': 'B=2'}]},
         0, contains=('NO_HARM_GATE_PASS=true', 'NOHARM m1 A=1 ok', 'NOHARM m2 B=2 ok'),
         absent=('RED ',))
    # 3: exact mismatch (the no-harm.sh comparison) must be refused.
    case('json-expect-mismatch', {'monitors': [
        {'name': 'bad', 'command': "printf 'X=false\\n'", 'expect': 'X=true'}]},
         1, contains=('RED bad', 'NO_HARM_GATE_PASS=false'))
    # 4: a missing token must be refused (the round-44 falsifier shape).
    case('json-token-missing', {'monitors': [
        {'name': 'bad', 'command': "printf 'C2_R44_PASS=false\\n'",
         'expect_contains': ['C2_R44_PASS=true']}]},
         1, contains=('RED bad', 'missing token', 'monitors=1 ok=0 red=1'))
    # 5-6: the threshold branch, below and at the bound.
    case('json-min-below', {'monitors': [
        {'name': 'cnt', 'command': "printf '116\\n'", 'expect_min': 117}]},
         1, contains=('RED cnt',))
    case('json-min-at-bound', {'monitors': [
        {'name': 'cnt', 'command': "printf '117\\n'", 'expect_min': 117}]},
         0, contains=('NOHARM cnt 117 ok',))
    # 7: a non-zero exit is a refusal even when the token matched.
    case('json-nonzero-exit', {'monitors': [
        {'name': 'crash', 'command': "printf 'K=true\\n'; exit 3", 'expect': 'K=true'}]},
         1, contains=('RED crash', 'exit 3'))
    # 8: one red among greens names only the red and keeps the green line.
    case('json-one-red-of-two', {'monitors': [
        {'name': 'good', 'command': "printf 'A=1\\n'", 'expect': 'A=1'},
        {'name': 'bad', 'command': "printf 'A=2\\n'", 'expect': 'A=1'}]},
         1, contains=('NOHARM good A=1 ok', 'RED bad'), absent=('RED good',))
    # 9: an empty list cannot prove anything.
    case('json-empty-list', {'monitors': []}, 1, contains=('RED no-monitors',))
    # 10: a malformed entry is a refusal, never a skip.
    case('json-malformed-entry', {'monitors': [{'name': 'nocmd'}]},
         1, contains=('RED nocmd', 'no command'))
    # 11: a named monitors file that does not exist.
    case('json-missing-file', None, 1, contains=('RED monitors-file', 'not found'),
         mfile=os.path.join(root, 'absent-monitors.json'))
    # 12-14: the shell-script list (.ufo/evidence/round-46/no-harm.sh shape).
    case('shell-all-ok', "#!/bin/bash\necho 'NOHARM a 1 ok'\necho 'NOHARM b 2 ok'\n",
         0, contains=('NOHARM a 1 ok', 'NOHARM b 2 ok', 'NO_HARM_GATE_PASS=true'), script=True)
    case('shell-one-red', "#!/bin/bash\necho 'NOHARM a 1 ok'\necho 'NOHARM b 2 RED'\n",
         1, contains=('RED b', 'NOHARM a 1 ok'), script=True)
    case('shell-nonzero-exit', "#!/bin/bash\necho 'NOHARM a 1 ok'\nexit 2\n",
         1, contains=('RED monitors-file', 'script exit 2'), script=True)
    case('shell-no-lines', "#!/bin/bash\necho 'nothing here'\n",
         1, contains=('RED no-monitors',), script=True)
    # 15-16: the contract is read, and a monitor it does not declare is refused.
    case('contract-no-noharm', {'monitors': [
        {'name': 'm1', 'command': "printf 'A=1\\n'", 'expect': 'A=1'}]},
         1, contains=('RED contract',), contract={})
    case('contract-phrase-drift', {'monitors': [
        {'name': 'phrased', 'command': "printf 'A=1\\n'", 'expect': 'A=1',
         'contract_phrase': 'a monitor the contract never declares'}]},
         1, contains=('RED phrased', 'does not declare',
                      'monitors=1 ok=0 red=1 contract_no_harm_chars=130 contract_phrases=0/1'))
    # 17: the timeout path.
    case('json-timeout', {'monitors': [
        {'name': 'slow', 'command': "sleep 5; printf 'A=1\\n'", 'expect': 'A=1'}]},
         1, contains=('RED slow', 'timeout'), timeout=0.4)
    # 18: a lane that is not a directory, and a revision that does not resolve.
    case('lane-missing', {'monitors': [
        {'name': 'm1', 'command': "printf 'A=1\\n'", 'expect': 'A=1'}]},
         1, contains=('RED lane',), lane=os.path.join(root, 'absent'))
    case('revision-unresolvable', {'monitors': [
        {'name': 'm1', 'command': "printf 'A=1\\n'", 'expect': 'A=1'}]},
         1, contains=('RED revision',), lane=bare, rev_arg='0' * 40)

    # 19: the hard-coded mapping and its own --list dump are the same gate.
    dumped = os.path.join(root, 'default-monitors.json')
    listing = subprocess.run([sys.executable, os.path.abspath(__file__), '--list'],
                             capture_output=True, text=True, cwd=root)
    _write(dumped, listing.stdout)
    cp = os.path.join(root, 'default-contract.json')
    _write(cp, json.dumps(DEFAULT_CONTRACT))
    base = ['--contract', cp, '--lane', repo, '--rev', rev]
    a = subprocess.run([sys.executable, os.path.abspath(__file__)] + base,
                       capture_output=True, text=True, cwd=root)
    b = subprocess.run([sys.executable, os.path.abspath(__file__)] + base
                       + ['--monitors-file', dumped], capture_output=True, text=True, cwd=root)
    ok = (listing.returncode == 0 and a.returncode == b.returncode == 1
          and a.stdout == b.stdout
          and [line.split()[1] for line in a.stdout.splitlines()
               if line.startswith('NOHARM ')] ==
          ['commandD', 'coldread', 'r45-freshness', 'r45-coverage', 'S160-count',
           'registry-rows-not-below-117'])
    results.append(('default-list-parity', ok))
    print('SELFTEST %-26s rc=%d want=%d %s' % ('default-list-parity', a.returncode, 1,
                                               'PASS' if ok else 'FAIL'))
    if not ok:
        for line in (a.stdout + '---\n' + b.stdout).splitlines():
            print('    | %s' % line)

    passed = len([1 for _, ok in results if ok])
    print('SELFTEST: %d/%d passed' % (passed, len(results)))
    print('VERDICT: %s' % ('PASS' if passed == len(results) else 'FAIL'))
    return 0 if passed == len(results) else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--contract')
    parser.add_argument('--lane')
    parser.add_argument('--rev')
    parser.add_argument('--monitors-file')
    parser.add_argument('--timeout', type=float, default=600.0,
                        help='seconds per monitor (default 600)')
    parser.add_argument('--list', action='store_true',
                        help='print the hard-coded monitor mapping as JSON and exit')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.list:
        print(json.dumps({'monitors': DEFAULT_MONITORS}, indent=1))
        return 0
    for flag in ('contract', 'lane', 'rev'):
        if not getattr(args, flag):
            parser.error('--%s is required (or --selftest)' % flag)
    code, lines = gate(args.contract, args.lane, args.rev, args.monitors_file, args.timeout)
    for line in lines:
        print(line)
    return code


if __name__ == '__main__':
    sys.exit(main())
