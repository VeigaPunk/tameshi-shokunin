#!/usr/bin/env python3
"""Round-51 C3 (operability) counter: the registry home (SKILL.md) carries a conforming, runnable row per lane gate.

Frozen predicate (the same sentence in the contract, here and in the receipt label):
  C3_R51_PASS=true iff tools >= 30 and total=0, total = missing + deleted, where, at REV:
  * the tool set is the frozen 30 base tools (.ufo/evidence/round-51/c3/tools-base.json) plus every other file
    directly under tools/ at REV with suffix .py or .sh whose bytes contain `selftest`; a frozen tool absent at REV
    counts in `deleted`;
  * a tool T is covered iff SKILL.md at REV holds, inside a section whose heading line matches
    `^#{2,4} Gate/probe registry` (to the next line starting with `#`), at least one 8-cell table row
    (Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner) with:
    Kind exactly `gate` or `probe`; an Entry command cell naming `tools/T`; a Verdict map cell containing both
    `0` and `1` as tokens; a Self-test cell holding exactly one backticked command whose argv (shlex) is
    `python3 [-I] tools/T ARGS...` or `bash tools/T ARGS...` with an ARG containing `selftest`, no shell
    metacharacters; a non-empty Pinned values cell in which every backticked token that looks like a repo path
    (contains `/`, no spaces, no `*`, `<`, `>`, `$`, not absolute) exists at REV, or the cell is `none` / starts
    with `none`; a non-empty Write scope cell; Owner exactly `tameshi`;
  * and that row's self-test command, run from a fresh `git clone --shared` of the lane checked out at REV (in
    WORK/tameshi-shokunin, TMPDIR=WORK/tmp, stdin /dev/null, 900 s timeout), exits 0, and the first
    whitespace-delimited token of its last non-empty stdout line (the self-test's finding id, e.g. `SELFTEST:`)
    appears in the row's Self-test cell;
  * and the usage probe — the self-test argv's interpreter prefix and tool followed by the single argument
    `--r51-no-such-flag`, same clone and limits but 60 s — exits with a code that appears as a token in the row's
    Verdict map (PROTOCOL §Gate standard: every exit code a gate can return is declared in its registry entry).
  A tool whose rows all fail is `missing` (the first failing reason of its best row is printed under --explain).
Usage: measure.py --lane LANE --rev REV --work EMPTY_DIR [--explain] | --selftest
Exit: 0 PASS · 1 not PASS · 2 setup error · 64 usage.
"""
import concurrent.futures
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
BASE_LIST = '.ufo/evidence/round-51/c3/tools-base.json'
HEAD_RE = re.compile(r'^#{2,4} Gate/probe registry')
META = set(';&|<>`$(){}\n')
PATHISH = re.compile(r'^[A-Za-z0-9._-][^\s*<>$]*/[^\s*<>$]*$')


def env():
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return e


def git(lane, *args, check=True):
    r = subprocess.run(['git', '-C', lane, *args], capture_output=True, env=env())
    if check and r.returncode != 0:
        raise RuntimeError('git %s: %s' % (' '.join(args), r.stderr.decode(errors='replace').strip()))
    return r


def show(lane, rev, path):
    r = git(lane, 'show', '%s:%s' % (rev, path), check=False)
    return r.stdout if r.returncode == 0 else None


def exists(lane, rev, path):
    return git(lane, 'cat-file', '-e', '%s:%s' % (rev, path), check=False).returncode == 0


def cells(line):
    s = line.strip()
    if not s.startswith('|'):
        return None
    s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    out, cur, tick = [], '', False
    for ch in s:
        if ch == '`':
            tick = not tick
        if ch == '|' and not tick:
            out.append(cur.strip())
            cur = ''
        else:
            cur += ch
    out.append(cur.strip())
    return out


def registry_rows(skill):
    rows, inside = [], False
    for n, line in enumerate(skill.split('\n'), 1):
        if line.startswith('#'):
            inside = bool(HEAD_RE.match(line))
            continue
        if inside:
            c = cells(line)
            if c and len(c) == 8 and c[0].lower() != 'name' and not re.match(r'^[\s:-]*$', c[0]):
                rows.append((n, c))
    return rows


def tool_set(lane, rev):
    base = json.loads(show(lane, rev, BASE_LIST) or b'{}').get('tools')
    if not base or len(base) != 30:
        raise RuntimeError('frozen base tool list missing or not 30 entries at REV')
    names = git(lane, 'ls-tree', '--name-only', rev, 'tools/').stdout.decode().split('\n')
    cur = []
    for p in names:
        if p.endswith(('.py', '.sh')):
            b = show(lane, rev, p)
            if b is not None and b'selftest' in b:
                cur.append(p)
    deleted = [t for t in base if not exists(lane, rev, t)]
    return sorted(set(base) | set(cur)), deleted


def row_reason(lane, rev, tool, c):
    name, kind, entry, vmap, st, pinned, scope, owner = c
    if kind not in ('gate', 'probe'):
        return 'kind', None
    if tool not in entry:
        return 'entry-names-other-tool', None
    if not (re.search(r'(?<![0-9])0(?![0-9])', vmap) and re.search(r'(?<![0-9])1(?![0-9])', vmap)):
        return 'verdict-map-lacks-0-or-1', None
    cmds = re.findall(r'`([^`]*)`', st)
    if len(cmds) != 1:
        return 'selftest-cell-commands=%d' % len(cmds), None
    cmd = cmds[0]
    if any(ch in META for ch in cmd):
        return 'selftest-shell-metachar', None
    try:
        argv = shlex.split(cmd)
    except ValueError:
        return 'selftest-unparsable', None
    rest = None
    if len(argv) >= 2 and argv[0] == 'python3':
        rest = argv[2:] if argv[1] == tool else (argv[3:] if argv[1] == '-I' and len(argv) >= 3 and argv[2] == tool else None)
    elif len(argv) >= 2 and argv[0] == 'bash' and argv[1] == tool:
        rest = argv[2:]
    if rest is None:
        return 'selftest-argv-not-the-tool', None
    if not any('selftest' in a for a in rest):
        return 'selftest-arg-missing', None
    if not pinned:
        return 'pinned-empty', None
    if not pinned.lower().startswith('none'):
        for tok in re.findall(r'`([^`]*)`', pinned):
            for part in tok.split():
                part = part.rstrip(',;')
                if PATHISH.match(part) and not part.startswith('/') and not exists(lane, rev, part):
                    return 'pinned-path-missing:%s' % part, None
    if not scope:
        return 'write-scope-empty', None
    if owner != 'tameshi':
        return 'owner', None
    prefix = argv[:len(argv) - len(rest)]
    return None, (argv, prefix + ['--r51-no-such-flag'], st, vmap)


def run_cmd(clone, work, argv, limit):
    tmp = os.path.join(work, 'tmp', hashlib.sha256(repr(argv).encode()).hexdigest()[:12])
    os.makedirs(tmp, exist_ok=True)
    e = env()
    e['TMPDIR'] = tmp
    try:
        r = subprocess.run(argv, cwd=clone, stdin=subprocess.DEVNULL, capture_output=True, env=e, timeout=limit)
        lines = [l for l in r.stdout.decode(errors='replace').split('\n') if l.strip()]
        return r.returncode, (lines[-1].strip()[:160] if lines else '')
    except subprocess.TimeoutExpired:
        return 124, 'timeout'


def run_row(clone, work, spec):
    argv, usage, st, vmap = spec
    rc, last = run_cmd(clone, work, argv, 900)
    if rc != 0:
        return 'selftest-exit=%d last=%s' % (rc, last), last
    marker = last.split()[0] if last.split() else ''
    if not marker or marker not in st:
        return 'finding-id-not-in-row (%s)' % marker, last
    urc, ulast = run_cmd(clone, work, usage, 60)
    if not re.search(r'(?<![0-9])%d(?![0-9])' % urc, vmap):
        return 'usage-exit-%d-undeclared' % urc, last
    return None, last


def measure(lane, rev, work):
    explain = []
    rev = git(lane, 'rev-parse', '--verify', rev + '^{commit}').stdout.decode().strip()
    skill = show(lane, rev, 'SKILL.md')
    if skill is None:
        raise RuntimeError('SKILL.md missing at REV')
    tools, deleted = tool_set(lane, rev)
    rows = registry_rows(skill.decode('utf-8', 'surrogateescape'))
    clone = os.path.join(work, 'tameshi-shokunin')
    if os.path.exists(clone):
        raise RuntimeError('work dir not empty')
    subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', lane, clone], check=True, env=env(), capture_output=True)
    subprocess.run(['git', '-C', clone, 'checkout', '-q', '--detach', rev], check=True, env=env(), capture_output=True)
    cand = {}
    reasons = {}
    for t in tools:
        for n, c in rows:
            if t not in c[2]:
                continue
            why, argv = row_reason(lane, rev, t, c)
            if why:
                reasons.setdefault(t, []).append('line %d %s' % (n, why))
            else:
                cand.setdefault(t, []).append((n, argv))
    jobs = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for t, lst in cand.items():
            for n, spec in lst:
                jobs[(t, n)] = ex.submit(run_row, clone, work, spec)
    covered, selftest_fail = [], 0
    for t in tools:
        ok = False
        for n, spec in cand.get(t, []):
            why, last = jobs[(t, n)].result()
            if why is None:
                ok = True
                explain.append('C3_TOOL %s: covered line %d selftest exit=0 last=%s' % (t, n, last))
                break
            selftest_fail += 1
            reasons.setdefault(t, []).append('line %d %s' % (n, why))
        if ok:
            covered.append(t)
        else:
            explain.append('C3_TOOL %s: MISSING (%s)' % (t, '; '.join(reasons.get(t, ['no-row']))))
    missing = len(tools) - len(covered)
    total = missing + len(deleted)
    for d in deleted:
        explain.append('C3_TOOL %s: DELETED at REV' % d)
    line = ('C3_R51: rev=%s tools=%d rows=%d covered=%d missing=%d deleted=%d selftest_fail_rows=%d total=%d C3_R51_PASS=%s'
            % (rev, len(tools), len(rows), len(covered), missing, len(deleted), selftest_fail, total,
               'true' if total == 0 and len(tools) >= 30 else 'false'))
    return (0 if total == 0 and len(tools) >= 30 else 1), line, explain


def selftest():
    """End-to-end through measure() on a throwaway repo with 30 frozen tools."""
    cases = failed = 0
    root = tempfile.mkdtemp(prefix='tameshi-r51-c3-selftest-', dir=os.environ.get('TMPDIR') or None)
    try:
        d = os.path.join(root, 'lane')
        os.makedirs(os.path.join(d, 'tools'))
        os.makedirs(os.path.join(d, '.ufo/evidence/round-51/c3'))
        g = lambda *a: subprocess.run(['git', '-C', d, *a], check=True, capture_output=True, env=env())
        g('init', '-q')
        if g('rev-parse', '--show-toplevel').stdout.decode().strip() != os.path.realpath(d):
            raise RuntimeError('fixture toplevel mismatch')
        tools = ['tools/t%02d.py' % i for i in range(30)]
        for t in tools:
            open(os.path.join(d, t), 'w').write('import sys\n# selftest\nif sys.argv[1:] == ["--selftest"]:\n    print("T_SELFTEST: 1/1 pass")\n    sys.exit(0)\nsys.exit(2)\n')
        open(os.path.join(d, 'tools/fail.py'), 'w').write('import sys\n# selftest\nsys.exit(1)\n')
        open(os.path.join(d, 'pin.json'), 'w').write('{}')
        json.dump({'tools': tools}, open(os.path.join(d, BASE_LIST), 'w'))
        hdr = '### Gate/probe registry\n\n| Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner |\n|---|---|---|---|---|---|---|---|\n'
        good = ''.join('| %s | gate | `python3 %s` | 0 clean; 1 failed; 2 usage | `python3 %s --selftest` → T_SELFTEST: | `pin.json` | none | tameshi |\n' % (t, t, t) for t in tools)
        good += '| f | gate | `python3 tools/fail.py` | 0 clean; 1 failed; 2 usage | `python3 tools/fail.py --selftest` → T_SELFTEST: | none | none | tameshi |\n'

        def commit(skill, msg):
            open(os.path.join(d, 'SKILL.md'), 'w').write(skill)
            g('add', '-A')
            g('-c', 'user.name=selftest', '-c', 'user.email=selftest@invalid', 'commit', '-qm', msg)
            return g('rev-parse', 'HEAD').stdout.decode().strip()
        plan = [
            ('no-rows', hdr, 1, 'missing=31'),
            ('all-good-but-failing-tool', hdr + good, 1, 'covered=30 missing=1'),
            ('help-not-selftest', hdr + good.replace(' --selftest`', ' --help`'), 1, 'covered=0'),
            ('missing-pin-path', hdr + good.replace('`pin.json`', '`nope/pin.json`'), 1, 'covered=0 missing=31'),
            ('row-outside-registry', '### Other\n\n' + good, 1, 'rows=0'),
            ('metachar', hdr + good.replace('--selftest`', '--selftest; true`'), 1, 'covered=0'),
            ('usage-code-undeclared', hdr + good.replace('; 2 usage', ''), 1, 'covered=0'),
            ('finding-id-absent', hdr + good.replace(' → T_SELFTEST:', ''), 1, 'covered=0'),
        ]
        for i, (name, skill, want_rc, want) in enumerate(plan):
            cases += 1
            rev = commit(skill, name)
            w = os.path.join(root, 'w%d' % i)
            os.makedirs(w)
            rc, line, _ = measure(d, rev, w)
            if rc != want_rc or want not in line:
                failed += 1
                print('C3_R51_SELFTEST FAIL %s: rc=%d %s' % (name, rc, line))
        cases += 1
        open(os.path.join(d, 'tools/fail.py'), 'w').write('import sys\n# selftest\nprint("T_SELFTEST: ok")\nsys.exit(0 if sys.argv[1:] == ["--selftest"] else 2)\n')
        rev = commit(hdr + good, 'fixed')
        w = os.path.join(root, 'wpass')
        os.makedirs(w)
        rc, line, _ = measure(d, rev, w)
        if rc != 0 or 'total=0 C3_R51_PASS=true' not in line:
            failed += 1
            print('C3_R51_SELFTEST FAIL pass-case: rc=%d %s' % (rc, line))
        cases += 1
        os.remove(os.path.join(d, 'tools/t00.py'))
        rev = commit(hdr + good, 'deleted')
        w = os.path.join(root, 'wdel')
        os.makedirs(w)
        rc, line, _ = measure(d, rev, w)
        if rc != 1 or 'deleted=1' not in line:
            failed += 1
            print('C3_R51_SELFTEST FAIL deleted-tool: rc=%d %s' % (rc, line))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print('C3_R51_SELFTEST: cases=%d failed=%d' % (cases, failed))
    return 0 if failed == 0 else 1


def main(argv):
    if argv == ['--selftest']:
        return selftest()
    ok = len(argv) in (6, 7) and argv[0] == '--lane' and argv[2] == '--rev' and argv[4] == '--work' \
        and (len(argv) == 6 or argv[6] == '--explain')
    if not ok:
        print('usage: measure.py --lane LANE --rev REV --work EMPTY_DIR [--explain] | --selftest', file=sys.stderr)
        return 64
    work = os.path.realpath(argv[5])
    if not os.path.isdir(work) or os.listdir(work):
        print('C3_R51: SETUP (--work must be an existing empty directory)')
        return 2
    try:
        rc, line, explain = measure(os.path.realpath(argv[1]), argv[3], work)
    except (RuntimeError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print('C3_R51: SETUP (%s)' % exc)
        return 2
    if len(argv) == 7:
        for e in explain:
            print(e)
    print(line)
    return rc


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
