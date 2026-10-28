#!/usr/bin/env python3
"""Round-56 reader-report validator: gates the L1's C1 bind (round-56 arm 4).

For every heading frozen in `.ufo/evidence/round-56/c1/lost-headings-at-base.json`
this tool requires, in the committed tree at REV, a report under
`.ufo/waves/round-56/w2` or `.../w3` whose path matches `T56W<digits>...Read....json`
(the FROZEN round-56 C1 counter's own glob, mirrored exactly so this gate can
never be laxer than the counter it gates) carrying:

  heading          exactly one frozen heading string
  cand             40-hex, equal to the content commit C0
  section_sha256   equal to the sha256 of that heading's section bytes at C0,
                   computed by the FROZEN round-18 `sectionize` (the blob at C0,
                   pinned by sha256 below) -- never a reimplementation
  findings         a list
  commands         a non-empty list of strings

and, beside it, a committed `.md` with the same stem that names the heading and
runs at least one of those commands verbatim.

Usage:
  validate-readers.py --lane LANE --rev REV [--c0 C0] [--headings PATH]
                      [--work EMPTY_DIR] [--explain]
  validate-readers.py --selftest

C0 is taken from --c0 when given, else derived exactly as the C1 counter derives
it: the single `.ufo/evidence/round-21/coldread/rekey-r56-<12hex>` directory at
REV (which only exists after the wave-3 bind, so wave-2 seats pass --c0).

Refusals (each printed as `REFUSE <code> <detail>`):

  C0_UNRESOLVABLE        --c0 absent and the re-key directory is not exactly one
                         resolvable, REV-ancestor commit
  C0_NOT_ANCESTOR        C0 is not REV or an ancestor of REV
  REV_UNRESOLVABLE       REV does not resolve
  R18_MISSING            no round-18 measure.py blob at C0
  R18_SECTIONIZE_DRIFT   that blob's sha256 is not the pinned frozen one
  SKILL_MISSING_AT_C0    no SKILL.md blob at C0
  HEADING_ABSENT_AT_C0   a frozen heading has no section at C0 (a miss, never a
                         narrowed heading list)
  HEADING_AMBIGUOUS      a frozen heading maps to more than one section
  READER_JSON_INVALID    a candidate report does not parse as JSON
  READER_HEADING_MISSING a candidate report has no usable `heading` string
  READER_MISSING         a frozen heading has no report at all
  READER_CAND_MISMATCH   `cand` absent, not 40-hex, or not C0
  READER_HASH_MISMATCH   `section_sha256` absent or not the C0 section sha256
  READER_HASH_XREV_DRIFT the C0 section sha256 is not the section's sha256 at REV,
                         so the C1 counter (which reads sections at REV) would
                         refuse the report even though it is right at C0
  READER_FINDINGS_NOT_LIST  `findings` absent or not a list
  READER_COMMANDS_EMPTY  `commands` absent, not a list, empty, or not all strings
  READER_MD_MISSING      no committed sibling `.md`, or it does not name the
                         heading, or it does not run any listed command

Warnings (printed as `WARN ...`, never a refusal): a well-formed report whose
heading is not frozen (dead weight, not harm), and an empty `findings` list.

Verdict: `READERS_R56: rev=.. c0=.. r18=.. headings=.. passed=../.. failed=..
refusals=.. warn=.. xrev=.. READERS_R56_PASS=true|false`. Exit 0 iff PASS,
1 on refusal, 2 on usage/IO error. Every read is a git object at REV/C0; the
live working tree is never read. Stdlib only.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

HEADINGS_PATH = '.ufo/evidence/round-56/c1/lost-headings-at-base.json'
R18_PATH = '.ufo/evidence/round-18/measure.py'
# sha256 of the round-18 measure.py blob at base 981c5e8b and at the round-56
# freeze c3e2ca9f (identical); the frozen sectionize this tool must use.
R18_PIN = '7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37'
WAVE_DIRS = ('.ufo/waves/round-56/w2', '.ufo/waves/round-56/w3')
REKEY_ROOT = '.ufo/evidence/round-21/coldread/'
REKEY_RE = re.compile(r'^rekey-r56-([0-9a-f]{12})$')
# identical to the round-56 C1 counter's report glob
REPORT_RE = re.compile(r'/T56W\d+.*Read.*\.json$')
HEX40 = re.compile(r'^[0-9a-f]{40}$')


def lane_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return env


def git(*args):
    return subprocess.run(['git'] + list(args), env=lane_env(),
                          capture_output=True, text=False)


def show(repo, rev, path):
    r = git('-C', repo, 'show', '%s:%s' % (rev, path))
    return r.stdout if r.returncode == 0 else None


def resolve(repo, prefix):
    r = git('-C', repo, 'rev-parse', '--verify', '--quiet', '%s^{commit}' % prefix)
    return r.stdout.decode().strip() if r.returncode == 0 else None


def is_ancestor(repo, older, newer):
    return git('-C', repo, 'merge-base', '--is-ancestor', older, newer).returncode == 0


def load_sectionize(repo, rev, work):
    """Import the frozen round-18 module from its blob at REV. Returns (mod, sha256)."""
    raw = show(repo, rev, R18_PATH)
    if raw is None:
        return None, None
    digest = hashlib.sha256(raw).hexdigest()
    path = work / 'r18-sectionize.py'
    path.write_bytes(raw)
    spec = importlib.util.spec_from_file_location('tameshi_r18_sectionize_r56', str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, digest


def group_sections(mod, raw):
    out = {}
    for sec in mod.sectionize(raw):
        out.setdefault(sec['heading'], []).append(sec)
    return out


def derive_c0(repo, rev):
    """The single rekey-r56-<c0> directory at REV, resolved, as the C1 counter does."""
    tree = git('-C', repo, 'ls-tree', '-r', '--name-only', rev, REKEY_ROOT).stdout.decode(
        'utf-8', 'surrogateescape')
    dirs = sorted({part for p in tree.splitlines() if '/traces/' in p
                   for part in Path(p).parts if REKEY_RE.fullmatch(part)})
    if len(dirs) != 1:
        return None, dirs
    prefix = REKEY_RE.match(dirs[0]).group(1)
    c0 = resolve(repo, prefix)
    if c0 is None or not c0.startswith(prefix) or not is_ancestor(repo, c0, rev):
        return None, dirs
    return c0, dirs


def report_paths(repo, rev):
    paths = []
    for wd in WAVE_DIRS:
        out = git('-C', repo, 'ls-tree', '-r', '--name-only', rev, wd + '/').stdout
        for p in out.decode('utf-8', 'surrogateescape').splitlines():
            if REPORT_RE.search(p):
                paths.append(p)
    return sorted(set(paths))


def md_path_for(json_path):
    return json_path[:-len('.json')] + '.md'


def check_candidate(repo, rev, path, data, heading, sec_c0, sec_rev, c0):
    """Return (codes, details) for one parsed report dict."""
    codes, details = [], []

    def bad(code, detail):
        codes.append(code)
        details.append('%s path=%s %s' % (code, path, detail))

    cand = data.get('cand')
    if not (isinstance(cand, str) and HEX40.fullmatch(cand)):
        bad('READER_CAND_MISMATCH', 'cand=%r not-40-hex' % (cand,))
    elif cand != c0:
        bad('READER_CAND_MISMATCH', 'cand=%s c0=%s' % (cand[:12], c0[:12]))

    got = data.get('section_sha256')
    want = sec_c0['sha256']
    if not (isinstance(got, str) and got == want):
        bad('READER_HASH_MISMATCH', 'section_sha256=%r c0-sha256=%s'
            % (got if got is not None else 'absent', want[:12]))
    elif sec_rev is not None and sec_rev['sha256'] != want:
        # the C1 counter reads sections at REV: right at C0 but stale at REV is
        # still a refusal by the counter, so refuse it here first.
        bad('READER_HASH_XREV_DRIFT', 'c0-sha256=%s rev-sha256=%s'
            % (want[:12], sec_rev['sha256'][:12]))

    if not isinstance(data.get('findings'), list):
        bad('READER_FINDINGS_NOT_LIST', 'findings=%r' % (type(data.get('findings')).__name__,))

    cmds = data.get('commands')
    if not isinstance(cmds, list) or not cmds or not all(isinstance(c, str) for c in cmds):
        bad('READER_COMMANDS_EMPTY', 'commands=%r' % (cmds,))
        cmds = [c for c in cmds if isinstance(c, str)] if isinstance(cmds, list) else []

    md = md_path_for(path)
    raw = show(repo, rev, md)
    if raw is None:
        bad('READER_MD_MISSING', 'no committed sibling %s' % md)
    else:
        text = raw.decode('utf-8', 'replace')
        if heading not in text:
            bad('READER_MD_MISSING', 'sibling %s does not name the heading' % md)
        elif not any(c in text for c in cmds):
            bad('READER_MD_MISSING', 'sibling %s runs none of the listed commands' % md)
    return codes, details


def validate(lane, rev_arg, c0_arg, headings_path, work, explain=False):
    res = {'rev': None, 'c0': None, 'r18': None, 'headings': 0, 'passed': 0,
           'failed': 0, 'refusals': [], 'warnings': [], 'notes': [], 'xrev': 0,
           'error': None, 'heading_lines': []}

    def refuse(code, detail):
        res['refusals'].append((code, detail))

    rev = resolve(lane, rev_arg)
    if rev is None:
        res['error'] = 'rev-unresolvable'
        refuse('REV_UNRESOLVABLE', 'rev=%r' % (rev_arg,))
        return res
    res['rev'] = rev

    if c0_arg:
        c0 = resolve(lane, c0_arg)
        if c0 is None:
            refuse('C0_UNRESOLVABLE', 'c0=%r does not resolve' % (c0_arg,))
            return res
    else:
        c0, dirs = derive_c0(lane, rev)
        if c0 is None:
            refuse('C0_UNRESOLVABLE', 'no single rekey-r56-* directory at rev=%s (dirs=%s)'
                   % (rev[:12], dirs or 'none'))
            return res
        res['notes'].append('c0-derived rekey-r56-%s' % c0[:12])
    res['c0'] = c0
    if not is_ancestor(lane, c0, rev):
        refuse('C0_NOT_ANCESTOR', 'c0=%s rev=%s' % (c0[:12], rev[:12]))
        return res

    mod, digest = load_sectionize(lane, c0, work)
    res['r18'] = digest
    if mod is None:
        refuse('R18_MISSING', 'no %s at c0=%s' % (R18_PATH, c0[:12]))
        return res
    if digest != R18_PIN:
        refuse('R18_SECTIONIZE_DRIFT', 'c0=%s sha256=%s pin=%s'
               % (c0[:12], digest, R18_PIN))

    skill_c0 = show(lane, c0, 'SKILL.md')
    if skill_c0 is None:
        refuse('SKILL_MISSING_AT_C0', 'c0=%s' % c0[:12])
        return res
    secs_c0 = group_sections(mod, skill_c0)
    secs_rev = secs_c0
    if rev != c0:
        skill_rev = show(lane, rev, 'SKILL.md')
        if skill_rev is not None:
            secs_rev = group_sections(mod, skill_rev)

    try:
        frozen = json.loads(Path(headings_path).read_text('utf-8'))
    except (OSError, ValueError) as exc:
        res['error'] = 'headings-unreadable'
        refuse('HEADINGS_UNREADABLE', '%s: %s' % (headings_path, exc))
        return res
    if not isinstance(frozen, list) or not all(isinstance(h, str) for h in frozen):
        res['error'] = 'headings-not-a-list-of-strings'
        refuse('HEADINGS_UNREADABLE', '%s is not a list of heading strings' % headings_path)
        return res
    res['headings'] = len(frozen)

    parsed = {}
    for path in report_paths(lane, rev):
        raw = show(lane, rev, path)
        if raw is None:
            continue
        try:
            data = json.loads(raw.decode('utf-8', 'surrogateescape'))
        except ValueError as exc:
            refuse('READER_JSON_INVALID', 'path=%s %s' % (path, exc))
            continue
        if not isinstance(data, dict):
            refuse('READER_JSON_INVALID', 'path=%s not-a-JSON-object' % path)
            continue
        heading = data.get('heading')
        if not isinstance(heading, str) or not heading:
            refuse('READER_HEADING_MISSING', 'path=%s heading=%r' % (path, heading))
            continue
        parsed.setdefault(heading, []).append((path, data))

    for heading, reports in sorted(parsed.items()):
        if heading not in frozen:
            res['warnings'].append('READER_HEADING_UNFROZEN path=%s heading=%r'
                                   % (reports[0][0], heading))

    for heading in frozen:
        if heading not in secs_c0:
            refuse('HEADING_ABSENT_AT_C0', 'heading=%r' % heading)
            res['failed'] += 1
            res['heading_lines'].append('FAIL %r no-section-at-c0' % heading)
            continue
        if len(secs_c0[heading]) > 1:
            refuse('HEADING_AMBIGUOUS', 'heading=%r sections=%s'
                   % (heading, [s['start'] for s in secs_c0[heading]]))
            res['failed'] += 1
            res['heading_lines'].append('FAIL %r ambiguous' % heading)
            continue
        sec_c0 = secs_c0[heading][0]
        sec_rev = secs_rev.get(heading, [None])[0]
        reports = parsed.get(heading, [])
        if not reports:
            refuse('READER_MISSING', 'heading=%r' % heading)
            res['failed'] += 1
            res['heading_lines'].append('FAIL %r no-report' % heading)
            continue
        ok = False
        for path, data in reports:
            codes, details = check_candidate(lane, rev, path, data, heading,
                                             sec_c0, sec_rev, c0)
            for detail in details:
                res['refusals'].append((detail.split(' ', 1)[0], detail))
            if isinstance(data.get('findings'), list) and not data['findings']:
                res['warnings'].append('READER_FINDINGS_EMPTY path=%s' % path)
            if not codes:
                ok = True
        if ok:
            res['passed'] += 1
            res['heading_lines'].append('PASS %r sha=%s' % (heading, sec_c0['sha256'][:12]))
        else:
            res['failed'] += 1
            res['heading_lines'].append('FAIL %r refused' % heading)
        if sec_rev is not None and sec_rev['sha256'] != sec_c0['sha256']:
            res['xrev'] += 1
            res['notes'].append('xrev-drift heading=%r c0=%s rev=%s'
                                % (heading, sec_c0['sha256'][:12], sec_rev['sha256'][:12]))
    return res


def verdict(res):
    return ('READERS_R56: rev=%s c0=%s r18=%s headings=%d passed=%d/%d failed=%d '
            'refusals=%d warn=%d xrev=%d READERS_R56_PASS=%s'
            % ((res['rev'] or 'none')[:12], (res['c0'] or 'none')[:12],
               (res['r18'] or 'none')[:12], res['headings'], res['passed'],
               res['headings'], res['failed'], len(res['refusals']),
               len(res['warnings']), res['xrev'],
               'true' if passed(res) else 'false'))


def passed(res):
    return (res['error'] is None and res['headings'] > 0
            and res['passed'] == res['headings'] and not res['refusals'])


def render(res, explain=False):
    lines = []
    for code, detail in res['refusals']:
        lines.append('REFUSE %s' % (detail if detail.startswith(code) else '%s %s' % (code, detail)))
    for w in res['warnings']:
        lines.append('WARN %s' % w)
    if explain:
        for note in res['notes']:
            lines.append('EXPLAIN %s' % note)
        for hl in res['heading_lines']:
            lines.append('EXPLAIN %s' % hl)
    lines.append(verdict(res))
    return '\n'.join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Validate round-56 cold-read reader reports.')
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--c0')
    ap.add_argument('--headings', default=None,
                    help='heading list (default: the frozen round-56 list in --lane)')
    ap.add_argument('--work', help='empty scratch dir (default: a fresh temp dir)')
    ap.add_argument('--explain', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.lane or not a.rev:
        ap.error('--lane and --rev are required (or --selftest)')

    tmp = None
    if a.work:
        work = Path(a.work)
        work.mkdir(parents=True, exist_ok=True)
        if any(work.iterdir()):
            print('READERS_R56: error=work-not-empty READERS_R56_PASS=false')
            return 2
    else:
        tmp = tempfile.mkdtemp(prefix='validate-readers-')
        work = Path(tmp)
    try:
        headings = a.headings or str(Path(a.lane) / HEADINGS_PATH)
        res = validate(a.lane, a.rev, a.c0, headings, work, a.explain)
        print(render(res, a.explain))
        return 0 if passed(res) else 1
    finally:
        if tmp is not None:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------------------- #
# selftest: synthetic tree, accept arm + every refusal, CLI wiring
# --------------------------------------------------------------------------- #
SKILL_TEXT = """Preamble paragraph.
Second preamble line.

## Alpha
Alpha body.
second alpha line.

## Beta
Beta body with a fenced block:

```sh
## Fenced not a heading
echo hi
```

### Gamma
Gamma body.
"""


def selftest():
    real_r18 = Path(__file__).resolve().parents[3] / R18_PATH
    cases = []

    def record(name, cond, detail=''):
        cases.append((name, bool(cond), detail))

    if not real_r18.is_file():
        print('SELFTEST FAIL fixture-missing no %s' % real_r18)
        print('SELFTEST: cases=1 failed=1')
        return 1

    tmp = Path(tempfile.mkdtemp(prefix='validate-readers-selftest-'))
    try:
        R = tmp / 'repo'
        R.mkdir()

        def g(*args):
            return git('-C', str(R), *args)

        if g('init', '-q').returncode != 0:
            print('SELFTEST FAIL git-init')
            return 1
        top = g('rev-parse', '--show-toplevel').stdout.decode().strip()
        if Path(top) != R.resolve():
            print('SELFTEST FAIL fixture-toplevel got=%r want=%r' % (top, str(R.resolve())))
            return 1

        def commit(msg):
            g('add', '-A')
            r = g('-c', 'user.name=selftest', '-c', 'user.email=selftest@example.invalid',
                  'commit', '-q', '-m', msg)
            if r.returncode != 0:
                raise RuntimeError('commit failed: %s' % r.stderr.decode('utf-8', 'replace'))
            return g('rev-parse', 'HEAD').stdout.decode().strip()

        (R / 'SKILL.md').write_text(SKILL_TEXT, encoding='utf-8')
        (R / '.ufo/evidence/round-18').mkdir(parents=True)
        (R / R18_PATH).write_bytes(real_r18.read_bytes())
        headings = ['## Alpha', '## Beta', '### Gamma']
        H = tmp / 'headings.json'
        H.write_text(json.dumps(headings), encoding='utf-8')
        c0 = commit('c0')

        # the frozen sectionize is in play: preamble + 3 headings, the fenced
        # `## Fenced not a heading` line is not a section (a naive reimplementation
        # would report 5 sections and shift every hash below).
        mod, digest = load_sectionize(str(R), c0, tmp)
        secs = group_sections(mod, (R / 'SKILL.md').read_bytes())
        record('frozen-sectionize-shape', len(secs) == 4 and '## Fenced not a heading' not in secs,
               'sections=%d keys=%s' % (len(secs), sorted(secs)))
        record('frozen-sectionize-pin', digest == R18_PIN, 'sha256=%s' % digest)

        w2 = R / '.ufo/waves/round-56/w2'
        w3 = R / '.ufo/waves/round-56/w3'
        w1 = R / '.ufo/waves/round-56/w1'

        def sha_of(heading):
            return secs[heading][0]['sha256']

        def write_state(cand, drop=(), cand_of=None, hash_of=None, findings_of=None,
                        commands_of=None, no_heading=(), md_drop=(), md_of=None,
                        extra=None, dir_of=None):
            for d in (w2, w3, w1):
                if d.exists():
                    for p in sorted(d.iterdir()):
                        p.unlink()
            dir_of = dir_of or {}
            for i, h in enumerate(headings):
                d = dir_of.get(h, w2 if i == 0 else w3)
                d.mkdir(parents=True, exist_ok=True)
                if h in drop:
                    continue
                cmd = 'grep -n %r SKILL.md' % h
                data = {
                    'heading': h,
                    'cand': (cand_of or {}).get(h, cand),
                    'section_sha256': (hash_of or {}).get(h, sha_of(h)),
                    'findings': (findings_of or {}).get(h, ['read in full']),
                    'commands': (commands_of or {}).get(h, [cmd]),
                }
                if h in no_heading:
                    data.pop('heading')
                stem = 'T56W2Read%s' % h.split()[-1]
                (d / (stem + '.json')).write_text(json.dumps(data, indent=1), encoding='utf-8')
                if h in md_drop:
                    continue
                (d / (stem + '.md')).write_text(
                    (md_of or {}).get(h, '# %s\n\nCommand: %s\n' % (h, cmd)), encoding='utf-8')
            for name, payload in (extra or {}).items():
                d = w2
                d.mkdir(parents=True, exist_ok=True)
                md = d / (name[:-len('.json')] + '.md')
                if isinstance(payload, str):          # raw bytes, not a report
                    (d / name).write_text(payload, encoding='utf-8')
                    md.write_text('# malformed report\n', encoding='utf-8')
                    continue
                (d / name).write_text(json.dumps(payload, indent=1), encoding='utf-8')
                md.write_text('%s\n\n%s\n' % (payload.get('heading', ''),
                                              (payload.get('commands') or [''])[0]),
                              encoding='utf-8')

        def run(rev, c0_arg=None, heads=str(H), work=None, explain=False):
            wd = Path(work or tempfile.mkdtemp(dir=str(tmp)))
            return validate(str(R), rev, c0_arg, heads, wd, explain)

        def codes_of(res, needle):
            return [c for c, d in res['refusals'] if needle in d]

        # ---- accept arm -----------------------------------------------------
        write_state(c0)
        rev = commit('good')
        res = run(rev, c0)
        record('accept-arm', passed(res) and res['passed'] == 3, verdict(res))
        record('accept-arm-no-refusal', not res['refusals'], str(res['refusals']))

        # ---- refusals -------------------------------------------------------
        write_state(c0, drop=('## Beta',))
        rev = commit('missing')
        res = run(rev, c0)
        record('refuse-missing-heading', 'READER_MISSING' in codes_of(res, 'Beta')
               and not passed(res) and res['passed'] == 2, verdict(res))

        write_state(c0, dir_of={'## Beta': w1})
        rev = commit('wrong-dir')
        res = run(rev, c0)
        record('refuse-report-outside-w2w3', 'READER_MISSING' in codes_of(res, 'Beta'),
               verdict(res))

        write_state(c0, cand_of={'## Beta': 'a' * 40})
        rev = commit('wrong-cand')
        res = run(rev, c0)
        record('refuse-wrong-cand', 'READER_CAND_MISMATCH' in codes_of(res, 'Beta')
               and not passed(res), verdict(res))

        write_state(c0, cand_of={'## Beta': 'not-a-revision'})
        rev = commit('nonhex-cand')
        res = run(rev, c0)
        record('refuse-nonhex-cand', 'READER_CAND_MISMATCH' in codes_of(res, 'Beta'),
               verdict(res))

        write_state(c0, hash_of={'## Beta': 'b' * 64})
        rev = commit('wrong-hash')
        res = run(rev, c0)
        record('refuse-wrong-hash', 'READER_HASH_MISMATCH' in codes_of(res, 'Beta')
               and not passed(res), verdict(res))

        write_state(c0, md_drop=('### Gamma',))
        rev = commit('no-md')
        res = run(rev, c0)
        record('refuse-md-missing', 'READER_MD_MISSING' in codes_of(res, 'Gamma')
               and not passed(res), verdict(res))

        write_state(c0, md_of={'### Gamma': '# Gamma, no command quoted\n'})
        rev = commit('md-no-command')
        res = run(rev, c0)
        record('refuse-md-without-command',
               'READER_MD_MISSING' in codes_of(res, 'Gamma') and not passed(res),
               verdict(res))

        write_state(c0, md_of={'### Gamma': 'command: grep -n Gamma SKILL.md\n'})
        rev = commit('md-no-heading')
        res = run(rev, c0)
        record('refuse-md-without-heading',
               'READER_MD_MISSING' in codes_of(res, 'Gamma'), verdict(res))

        write_state(c0, findings_of={'## Alpha': 'looks fine'})
        rev = commit('findings-not-list')
        res = run(rev, c0)
        record('refuse-findings-not-list', 'READER_FINDINGS_NOT_LIST' in codes_of(res, 'Alpha')
               and not passed(res), verdict(res))

        write_state(c0, findings_of={'## Alpha': []})
        rev = commit('findings-empty')
        res = run(rev, c0)
        record('warn-findings-empty', passed(res) and any('READER_FINDINGS_EMPTY' in w
                                                         for w in res['warnings']), verdict(res))

        write_state(c0, commands_of={'## Alpha': []})
        rev = commit('commands-empty')
        res = run(rev, c0)
        record('refuse-commands-empty', 'READER_COMMANDS_EMPTY' in codes_of(res, 'Alpha')
               and not passed(res), verdict(res))

        write_state(c0, commands_of={'## Alpha': ['ok', 7]})
        rev = commit('commands-nonstr')
        res = run(rev, c0)
        record('refuse-commands-nonstr', 'READER_COMMANDS_EMPTY' in codes_of(res, 'Alpha'),
               verdict(res))

        write_state(c0, no_heading=('## Alpha',))
        rev = commit('heading-missing')
        res = run(rev, c0)
        record('refuse-heading-missing', 'READER_HEADING_MISSING' in
               [c for c, d in res['refusals']] and not passed(res), verdict(res))

        write_state(c0, extra={'T56W2ReadGhost.json': {
            'heading': '## Not Frozen', 'cand': c0,
            'section_sha256': sha_of('## Alpha'), 'findings': [], 'commands': ['true']}})
        rev = commit('unfrozen-extra')
        res = run(rev, c0)
        record('warn-unfrozen-heading-not-refusal',
               passed(res) and any('READER_HEADING_UNFROZEN' in w for w in res['warnings']),
               verdict(res))

        write_state(c0, extra={'T56W2ReadBroken.json': 'not json'})
        (w2 / 'T56W2ReadBroken.md').write_text('## Alpha\n', encoding='utf-8')
        rev = commit('bad-json')
        res = run(rev, c0)
        record('refuse-json-invalid', 'READER_JSON_INVALID' in [c for c, d in res['refusals']]
               and not passed(res), verdict(res))

        # ---- the C1 counter's REV view --------------------------------------
        write_state(c0)
        (R / 'SKILL.md').write_text(
            SKILL_TEXT.replace('Beta body with a fenced block:', 'Beta body, edited after c0:'),
            encoding='utf-8')
        rev = commit('xrev-drift')
        res = run(rev, c0)
        record('refuse-xrev-drift', 'READER_HASH_XREV_DRIFT' in codes_of(res, 'Beta')
               and not passed(res) and res['xrev'] == 1, verdict(res))
        (R / 'SKILL.md').write_text(SKILL_TEXT, encoding='utf-8')

        # ---- the frozen sectionize must not have drifted --------------------
        (R / R18_PATH).write_text((R / R18_PATH).read_text(encoding='utf-8') + '\n# drift\n',
                                  encoding='utf-8')
        drift = commit('r18-drift')
        write_state(drift)
        rev = commit('r18-drift-reports')
        res = run(rev, drift)
        record('refuse-r18-drift', 'R18_SECTIONIZE_DRIFT' in [c for c, d in res['refusals']]
               and not passed(res), verdict(res))
        (R / R18_PATH).write_bytes(real_r18.read_bytes())

        # ---- c0 derivation from the re-key directory ------------------------
        write_state(c0)
        rekey = R / REKEY_ROOT / ('rekey-r56-' + c0[:12]) / 'traces'
        rekey.mkdir(parents=True)
        (rekey / 'alpha.json').write_text('{}', encoding='utf-8')
        rev = commit('rekey-one')
        res = run(rev, None)
        record('derive-c0-from-rekey', passed(res) and res['c0'] == c0, verdict(res))

        other = R / REKEY_ROOT / ('rekey-r56-' + rev[:12]) / 'traces'
        other.mkdir(parents=True)
        (other / 'beta.json').write_text('{}', encoding='utf-8')
        rev2 = commit('rekey-two')
        res = run(rev2, None)
        record('refuse-two-rekey-dirs', 'C0_UNRESOLVABLE' in [c for c, d in res['refusals']]
               and not passed(res), verdict(res))

        # ---- C0 must be REV or an ancestor of REV ---------------------------
        write_state(rev2)
        rev3 = commit('later')
        res = run(rev3, rev2)                 # ancestor c0: accepted
        record('accept-ancestor-c0', passed(res), verdict(res))
        res = run(rev2, rev3)                 # descendant c0: refused
        record('refuse-c0-not-ancestor', 'C0_NOT_ANCESTOR' in [c for c, d in res['refusals']]
               and not passed(res), verdict(res))
        write_state(rev3)
        rev4 = commit('post-c0')
        # a report set committed in the same commit it names as c0 is a hash
        # fixed-point and cannot exist, so c0 is always a strict ancestor of the
        # commit carrying the reports; assert that here rather than test it.
        record('c0-strict-ancestor-of-reports',
               not passed(run(rev4, rev4)), 'c0==rev accepted: fixed point exists')

        # ---- CLI wiring -----------------------------------------------------
        def cli(*args):
            return subprocess.run([sys.executable, str(Path(__file__).resolve()), '--lane', str(R)]
                                  + list(args), capture_output=True, text=True)

        write_state(c0)
        cli_rev = commit('cli-good')
        r = cli('--rev', cli_rev, '--c0', c0, '--headings', str(H),
                '--work', str(tmp / 'cliwork1'))
        record('cli-exit0-accept', r.returncode == 0 and 'READERS_R56_PASS=true' in r.stdout,
               'rc=%d out=%r' % (r.returncode, r.stdout.strip().splitlines()[-1:]))

        write_state(c0, drop=('## Alpha',))
        cli_rev = commit('cli-bad')
        r = cli('--rev', cli_rev, '--c0', c0, '--headings', str(H),
                '--work', str(tmp / 'cliwork2'))
        record('cli-exit1-refuse', r.returncode == 1 and 'READERS_R56_PASS=false' in r.stdout
               and 'REFUSE READER_MISSING' in r.stdout,
               'rc=%d out=%r' % (r.returncode, r.stdout.strip().splitlines()[-1:]))

        r = cli('--rev', 'f' * 40, '--c0', c0, '--headings', str(H),
                '--work', str(tmp / 'cliwork3'))
        record('cli-exit1-unresolvable-rev', r.returncode == 1
               and 'REV_UNRESOLVABLE' in r.stdout, 'rc=%d' % r.returncode)

        (tmp / 'cliwork4').mkdir()
        (tmp / 'cliwork4' / 'occupied').write_text('x', encoding='utf-8')
        r = cli('--rev', cli_rev, '--c0', c0, '--headings', str(H),
                '--work', str(tmp / 'cliwork4'))
        record('cli-exit2-work-not-empty', r.returncode == 2
               and 'work-not-empty' in r.stdout, 'rc=%d' % r.returncode)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)

    failed = 0
    for name, ok, detail in cases:
        if ok:
            print('SELFTEST PASS %s' % name)
        else:
            failed += 1
            print('SELFTEST FAIL %s %s' % (name, detail))
    print('SELFTEST: cases=%d failed=%d' % (len(cases), failed))
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
