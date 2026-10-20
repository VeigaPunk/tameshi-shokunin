#!/usr/bin/env python3
r"""C1+C2 counting command for tameshi round 16 (hyaku phase 2).

Reads blobs via `git show REV:path` only (no worktree access) and prints one
JSON object:

  recorded_cases   count of `^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+` lines
                   (multiline) in tools/mutate-and-run.sh — the ledger comment
  depth_score      min(10, recorded_cases)
  ledger_legs      leg names captured from those lines
  shonen           mark census from `^- \[([x~ ])\] ` in SHONEN.md (boxes 1-4
                   in file order)
  coldread         SKILL.md parsed into sections (preamble + every #/##/###
                   heading outside ``` fences; section text = heading line
                   through the line before the next heading with trailing
                   blank (whitespace-only) lines stripped, joined by \n, no
                   trailing newline) matched by sha256 against
                   .ufo/evidence/round-16/coldread/ledger.json at REV.
                   box3_full_page = every section's sha256 is covered by a
                   ledger entry credited per the L1 rule: verdict
                   executed-ok or gap-minor on class instruction requires
                   commands_executed_count>0; verdict verified-record or
                   gap-minor on class record is credited; any
                   blocking_gaps>0, wrong_expectations>0, or verdict in
                   (gap-blocking, wrong-expectation, not-executed) fails.
                   Reports covered/total and every uncovered heading.
  calibration_restraint_score
                   2 * count of boxes 1,2,4 marked `~` + 2 * (box3 is `~`,
                   box3_full_page, and the SHONEN box-3 line at REV contains
                   `.ufo/evidence/round-16/coldread/ledger.json`)
  sources          corpus/SOURCES.md census: rows matching
                   `^\|\s*S[0-9]{3,}\s*\|`, awk -F'|' NF!=13 malformed count,
                   tier ($5) and status ($9) histograms over NF==13 rows

Exits: 0 ok · 2 rev/blob missing or unparseable required input · 64 usage.

`--selftest` builds synthetic git repos in mkdtemp and proves: no ledger ->
box3 false, score 6; complete ledger -> 8; one section missing -> 6; one
gap-blocking -> 6; one section byte changed -> 6; instruction entry with
commands_executed_count 0 or with a verified-record verdict -> no credit;
record-class verified-record credited; missing SHONEN box-3 ledger link -> 6;
plus literal expected exits (0/2/64). Stdlib only.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

DEFAULT_REPO = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
LEDGER_PATH = '.ufo/evidence/round-16/coldread/ledger.json'
REQUIRED_BLOBS = (
    'tools/mutate-and-run.sh',
    'SHONEN.md',
    'SKILL.md',
    'corpus/SOURCES.md',
)
LEG_RE = re.compile(r'^#   ((?:js|bash)-\S+)\s+\S+\s+\d+/\d+', re.M)
BOX_RE = re.compile(r'^- \[([x~ ])\] (.*)$', re.M)
SOURCE_ROW_RE = re.compile(r'^\|\s*S[0-9]{3,}\s*\|')
HEADING_RE = re.compile(r'^#{1,3}(?:\s|$)')
FAIL_VERDICTS = frozenset(('gap-blocking', 'wrong-expectation', 'not-executed'))
EXEC_VERDICTS = frozenset(('executed-ok', 'gap-minor'))
REC_VERDICTS = frozenset(('verified-record', 'gap-minor'))
BOX3_LINK = '.ufo/evidence/round-16/coldread/ledger.json'


class UsageParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        sys.stderr.write('%s: error: %s\n' % (self.prog, message))
        raise SystemExit(64)


def git(repo, *args):
    return subprocess.run(['git', '-C', repo] + list(args),
                          capture_output=True)


def blob(repo, rev, path):
    """Return raw bytes of REV:path, or None when the blob does not resolve."""
    result = git(repo, 'show', '%s:%s' % (rev, path))
    if result.returncode != 0:
        return None
    return result.stdout


def sectionize(raw):
    r"""Split SKILL.md bytes into sections: preamble + heading blocks.

    A heading is a line matching ^#{1,3}(\s|$) outside ``` fences. Section
    text is the heading line through the line before the next heading, with
    trailing blank (whitespace-only) lines stripped, joined with \n and no
    trailing newline; lines before the first heading form a preamble section
    whose heading is ''. Byte fidelity is kept with surrogateescape so the
    sha256 is over the original blob bytes.
    """
    text = raw.decode('utf-8', 'surrogateescape')
    lines = text.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    heads = []
    in_fence = False
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_fence = not in_fence
            continue
        if not in_fence and HEADING_RE.match(line):
            heads.append(i)
    pairs = []
    if heads:
        if heads[0] > 0:
            pairs.append((0, heads[0]))          # preamble
        for s, e in zip(heads, heads[1:] + [len(lines)]):
            pairs.append((s, e))
    else:
        pairs.append((0, len(lines)))            # whole file = preamble
    head_set = set(heads)
    sections = []
    for s, e in pairs:
        body_lines = list(lines[s:e])
        while body_lines and body_lines[-1].strip() == '':
            body_lines.pop()
        body = '\n'.join(body_lines)
        sections.append({
            'start': s + 1,
            'heading': lines[s] if s in head_set else '',
            'sha256': hashlib.sha256(
                body.encode('utf-8', 'surrogateescape')).hexdigest(),
        })
    return sections


def shonen_boxes(raw):
    """Return [(mark, block)] per `- [m] ` checklist box, in order.

    A box's block is its own line plus the indented continuation lines right
    under it (SHONEN.md carries each box's evidence link on the continuation
    line). Round-16 L1 repair: the first version returned the box line only,
    so a link on the continuation line was never seen.
    """
    out, open_box = [], False
    for line in raw.decode('utf-8', 'surrogateescape').split('\n'):
        match = BOX_RE.match(line)
        if match:
            out.append([match.group(1), line])
            open_box = True
        elif open_box and line[:1] in (' ', '\t') and line.strip():
            out[-1][1] += '\n' + line
        else:
            open_box = False
    return [tuple(b) for b in out]


def sources_census(raw):
    text = raw.decode('utf-8', 'surrogateescape')
    rows, malformed, tiers, status = 0, 0, {}, {}
    for line in text.split('\n'):
        if not SOURCE_ROW_RE.match(line):
            continue
        rows += 1
        fields = line.split('|')
        if len(fields) != 13:
            malformed += 1
            continue
        tier = re.sub(r'\s', '', fields[4])
        stat = re.sub(r'\s', '', fields[8])
        tiers[tier] = tiers.get(tier, 0) + 1
        status[stat] = status.get(stat, 0) + 1
    return {'rows': rows, 'malformed': malformed,
            'tiers': dict(sorted(tiers.items())),
            'status': dict(sorted(status.items()))}


def entry_credit_reason(entry):
    """L1 credit rule; return None when the entry credits its section.

    Hard fail: any blocking_gaps>0, wrong_expectations>0, or a verdict in
    FAIL_VERDICTS (unknown/missing verdicts included). Then
    class-conditional: class 'instruction' credits on executed-ok|gap-minor
    with commands_executed_count>0; class 'record' credits on
    verified-record|gap-minor.
    """
    verdict = entry.get('verdict')
    try:
        bg = int(entry.get('blocking_gaps', 0))
        we = int(entry.get('wrong_expectations', 0))
    except (TypeError, ValueError):
        return 'malformed-entry'
    if verdict in FAIL_VERDICTS or not isinstance(verdict, str):
        return 'verdict:%s' % verdict
    if bg != 0:
        return 'blocking-gaps:%d' % bg
    if we != 0:
        return 'wrong-expectations:%d' % we
    cls = entry.get('class')
    if cls == 'instruction':
        if verdict not in EXEC_VERDICTS:
            return 'verdict-class:%s/instruction' % verdict
        try:
            cmd_count = int(entry.get('commands_executed_count', 0))
        except (TypeError, ValueError):
            return 'malformed-entry'
        if cmd_count <= 0:
            return 'commands-executed-count:%s' % (
                entry.get('commands_executed_count'))
        return None
    if cls == 'record':
        if verdict in REC_VERDICTS:
            return None
        return 'verdict-class:%s/record' % verdict
    return 'class:%s' % cls


def coldread(skill_raw, ledger_raw):
    sections = sectionize(skill_raw)
    out = {'sections_total': len(sections), 'sections_covered': 0,
           'box3_full_page': False, 'missing': [], 'uncovered_headings': []}
    if ledger_raw is None:
        out['ledger_present'] = False
        for sec in sections:
            out['missing'].append({'start': sec['start'],
                                   'heading': sec['heading'],
                                   'reason': 'no-ledger'})
            out['uncovered_headings'].append(sec['heading'])
        return out
    out['ledger_present'] = True
    try:
        ledger = json.loads(ledger_raw.decode('utf-8', 'surrogateescape'))
        entries = ledger['entries']
        assert isinstance(entries, list)
    except Exception as exc:
        out['ledger_error'] = '%s: %s' % (type(exc).__name__, exc)
        for sec in sections:
            out['missing'].append({'start': sec['start'],
                                   'heading': sec['heading'],
                                   'reason': 'invalid-ledger'})
            out['uncovered_headings'].append(sec['heading'])
        return out
    by_sha = {}
    for entry in entries:
        if isinstance(entry, dict) and isinstance(entry.get('sha256'), str):
            by_sha.setdefault(entry['sha256'], []).append(entry)
    for sec in sections:
        matches = by_sha.get(sec['sha256'], [])
        reasons = []
        covered = False
        for entry in matches:
            reason = entry_credit_reason(entry)
            if reason is None:
                covered = True
                break
            reasons.append(reason)
        if covered:
            out['sections_covered'] += 1
        else:
            reason = ';'.join(sorted(set(reasons))) if reasons else 'no-ledger-entry'
            out['missing'].append({'start': sec['start'],
                                   'heading': sec['heading'],
                                   'reason': reason})
            out['uncovered_headings'].append(sec['heading'])
    out['box3_full_page'] = out['sections_covered'] == out['sections_total']
    return out


def measure(repo, rev):
    runner = blob(repo, rev, 'tools/mutate-and-run.sh')
    boxes = shonen_boxes(blob(repo, rev, 'SHONEN.md'))
    marks = [mark for mark, _line in boxes]
    skill = blob(repo, rev, 'SKILL.md')
    sources = sources_census(blob(repo, rev, 'corpus/SOURCES.md'))
    legs = LEG_RE.findall(runner.decode('utf-8', 'surrogateescape'))
    rtext = runner.decode('utf-8', 'surrogateescape')
    # Guardrail (round-16 w2 DepthCritic): command D counts header comment
    # lines only; report whether the header, the regression call sites and
    # the selftest leg tuples agree, and how many distinct gate paths the
    # header names. These fields do not change depth_score.
    leg_calls = len(re.findall(r'^  regression_case_git (?:js|bash)-', rtext, re.M))
    leg_tuples = len(re.findall(r"^    '(?:js|bash)-[^:]+:[^:]+\.spec:TABLE_", rtext, re.M))
    gate_paths = re.findall(r'^#   (?:js|bash)-\S+\s+(\S+)\s+\d+/\d+', rtext, re.M)
    cr = coldread(skill, blob(repo, rev, LEDGER_PATH))
    box3_marked = len(marks) >= 3 and marks[2] == '~'
    box3_link = len(boxes) >= 3 and BOX3_LINK in boxes[2][1]
    box3_points = box3_marked and box3_link and cr['box3_full_page']
    restraint = 2 * sum(len(marks) >= b and marks[b - 1] == '~'
                        for b in (1, 2, 4)) + 2 * box3_points
    return {
        'revision': rev,
        'recorded_cases': len(legs),
        'depth_score': min(10, len(legs)),
        'ledger_legs': legs,
        'ledger_guardrail': {
            'header_legs': len(legs), 'regression_calls': leg_calls,
            'selftest_tuples': leg_tuples,
            'lists_agree': len(legs) == leg_calls == leg_tuples,
            'unique_recorded_gates': len(set(gate_paths)),
        },
        'shonen': {
            'boxes': len(marks),
            'marks': marks,
            'checked': marks.count('x'),
            'asserted': marks.count('~'),
            'untouched': marks.count(' '),
            'box3_marked': box3_marked,
            'box3_ledger_link': box3_link,
            'box3_points': box3_points,
        },
        'coldread': cr,
        'calibration_restraint_score': restraint,
        'sources': sources,
    }


SKILL_LINES = [
    '---',
    'name: syn-skill',
    '---',
    '',
    'Intro line before first heading.',
    '',
    '# Alpha',
    '',
    'alpha body',
    '',
    '## Beta',
    '',
    '```',
    '# hidden-heading-inside-fence',
    '```',
    '',
    'beta body',
    '',
    '### Gamma',
    '',
    'gamma body',
]
SHONEN_BOX3 = '- [~] box three — evidence .ufo/evidence/round-16/coldread/ledger.json'
SHONEN_TEXT = '\n'.join([
    '# syn promotion checklist',
    '',
    '- [~] box one',
    '- [~] box two',
    SHONEN_BOX3,
    '- [~] box four',
]) + '\n'
SHONEN_NOLINK_TEXT = SHONEN_TEXT.replace(SHONEN_BOX3, '- [~] box three')
SHONEN_CONT_TEXT = SHONEN_TEXT.replace(
    SHONEN_BOX3, '- [~] box three\n  [lane assertion](.ufo/evidence/round-16/coldread/ledger.json)')
SHONEN_WRONGBOX_TEXT = SHONEN_NOLINK_TEXT.replace(
    '- [~] box four', '- [~] box four\n  [link](.ufo/evidence/round-16/coldread/ledger.json)')
RUNNER_TEXT = '\n'.join([
    '#!/bin/sh',
    '# ledger legs:',
    '#   js-syn-aaa   repo/a.mjs   8/10 (80 %)',
    '#   bash-syn-bbb repo/b.sh   4/10 (40 %)',
]) + '\n'
SOURCES_TEXT = '\n'.join([
    '# syn sources',
    '',
    '| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |',
    '|---|---|---|---|---|---|---|---|---|---|---|',
    '| S001 | x | docs | A | s | a | t | mined | 2026-10-20 | 90d | — |',
    '| S002 | y | paper | B | s | a | t | queued | 2026-10-20 | 90d | — |',
]) + '\n'
# Section texts for the ledger, sliced literally from SKILL_LINES with
# trailing blank lines stripped, so the selftest does not reuse sectionize()
# to produce its own expectation.
def _strip_tail(slice_lines):
    while slice_lines and slice_lines[-1].strip() == '':
        slice_lines.pop()
    return '\n'.join(slice_lines)


SYNTH_SECTIONS = [
    (1, '', _strip_tail(SKILL_LINES[0:6])),
    (7, '# Alpha', _strip_tail(SKILL_LINES[6:10])),
    (11, '## Beta', _strip_tail(SKILL_LINES[10:18])),
    (19, '### Gamma', _strip_tail(SKILL_LINES[18:21])),
]


def ledger_json(drop=None, blocking=None, changed=None):
    entries = []
    for i, (start, heading, text) in enumerate(SYNTH_SECTIONS):
        if i == drop:
            continue
        body = text + ' CHANGED' if i == changed else text
        entries.append({
            'skill_sha256': 'deadbeef',
            'start': start,
            'end': start + len(text.split('\n')) - 1,
            'heading': heading,
            'sha256': hashlib.sha256(body.encode()).hexdigest(),
            'class': 'instruction',
            'verdict': 'executed-ok',
            'blocking_gaps': 1 if i == blocking else 0,
            'wrong_expectations': 0,
            'commands_executed_count': 1,
            'seats': ['syn'],
            'reports': ['syn.md'],
        })
    return json.dumps({'schema': 'tameshi-coldread-ledger-v1',
                       'entries': entries}, indent=2) + '\n'


def selftest():
    script = os.path.abspath(__file__)
    tmp = tempfile.mkdtemp(prefix='tameshi-r16-CRMeasure-')
    env = dict(os.environ,
               GIT_CONFIG_NOSYSTEM='1',
               GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t',
               GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t',
               HOME=tmp)

    def run(*args, cwd=None):
        return subprocess.run(args, capture_output=True, text=True,
                              cwd=cwd, env=env)

    def git_in(repo, *args):
        return run('git', '-C', repo, *args)

    def write_file(repo, rel, content):
        path = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)

    def commit(repo, label):
        git_in(repo, 'add', '-A')
        res = git_in(repo, 'commit', '-qm', label)
        assert res.returncode == 0, res.stderr
        return git_in(repo, 'rev-parse', 'HEAD').stdout.strip()

    def call_measure(repo, rev):
        return run(sys.executable or 'python3', script,
                   '--rev', rev, '--repo', repo)

    repo = os.path.join(tmp, 'synrepo')
    os.makedirs(repo)
    init = git_in(repo, 'init', '-q')
    assert init.returncode == 0, init.stderr

    checks = []

    def check(name, cond, detail=''):
        checks.append((name, bool(cond), detail))
        print('%s %s %s' % ('PASS' if cond else 'FAIL', name, detail))

    write_file(repo, 'tools/mutate-and-run.sh', RUNNER_TEXT)
    write_file(repo, 'SHONEN.md', SHONEN_TEXT)
    write_file(repo, 'SKILL.md', '\n'.join(SKILL_LINES) + '\n')
    write_file(repo, 'corpus/SOURCES.md', SOURCES_TEXT)
    rev_base = commit(repo, 'base, no ledger')

    # --- case: no ledger -> box3 false, restraint 6 ------------------------------
    res = call_measure(repo, rev_base)
    check('exit0-no-ledger', res.returncode == 0, res.stderr.strip()[:200])
    out = json.loads(res.stdout) if res.returncode == 0 else {}
    check('no-ledger-depth', out.get('recorded_cases') == 2
          and out.get('depth_score') == 2
          and out.get('ledger_legs') == ['js-syn-aaa', 'bash-syn-bbb'])
    check('no-ledger-marks', out.get('shonen', {}).get('marks') == ['~'] * 4)
    check('no-ledger-sections', out.get('coldread', {}).get('sections_total') == 4,
          'fence-hidden heading excluded, preamble counted')
    check('no-ledger-box3-false',
          out.get('coldread', {}).get('box3_full_page') is False
          and out.get('coldread', {}).get('ledger_present') is False)
    check('no-ledger-score-6', out.get('calibration_restraint_score') == 6)
    check('no-ledger-sources', out.get('sources') == {
        'rows': 2, 'malformed': 0,
        'tiers': {'A': 1, 'B': 1},
        'status': {'mined': 1, 'queued': 1}})

    # --- case: complete ledger -> 8 --------------------------------------------
    write_file(repo, LEDGER_PATH, ledger_json())
    rev_full = commit(repo, 'complete ledger')
    out = json.loads(call_measure(repo, rev_full).stdout)
    check('full-ledger-covered', out['coldread']['sections_covered'] == 4
          and out['coldread']['sections_total'] == 4
          and out['coldread']['missing'] == [])
    check('full-ledger-box3', out['coldread']['box3_full_page'] is True)
    check('full-ledger-score-8', out['calibration_restraint_score'] == 8)

    # --- case: one section missing -> 6 ----------------------------------------
    write_file(repo, LEDGER_PATH, ledger_json(drop=3))
    rev_miss = commit(repo, 'gamma entry absent')
    out = json.loads(call_measure(repo, rev_miss).stdout)
    check('missing-section-covered3', out['coldread']['sections_covered'] == 3)
    check('missing-section-box3', out['coldread']['box3_full_page'] is False)
    check('missing-section-heading',
          out['coldread']['missing'] == [
              {'start': 19, 'heading': '### Gamma', 'reason': 'no-ledger-entry'}])
    check('missing-section-score-6', out['calibration_restraint_score'] == 6)

    # --- case: one gap-blocking -> 6 -------------------------------------------
    write_file(repo, LEDGER_PATH, ledger_json(blocking=3))
    rev_block = commit(repo, 'gamma blocking')
    out = json.loads(call_measure(repo, rev_block).stdout)
    check('blocking-covered3', out['coldread']['sections_covered'] == 3)
    check('blocking-reason',
          out['coldread']['missing'] == [
              {'start': 19, 'heading': '### Gamma', 'reason': 'blocking-gaps:1'}])
    check('blocking-score-6', out['calibration_restraint_score'] == 6)

    # --- case: one section byte changed -> 6 -----------------------------------
    write_file(repo, LEDGER_PATH, ledger_json(changed=3))
    rev_byte = commit(repo, 'gamma sha over changed bytes')
    out = json.loads(call_measure(repo, rev_byte).stdout)
    check('bytechange-covered3', out['coldread']['sections_covered'] == 3)
    check('bytechange-reason',
          out['coldread']['missing'] == [
              {'start': 19, 'heading': '### Gamma', 'reason': 'no-ledger-entry'}])
    check('bytechange-score-6', out['calibration_restraint_score'] == 6)

    # --- case: uncredited verdict also fails coverage ---------------------------
    bad = json.loads(ledger_json())
    bad['entries'][3]['verdict'] = 'gap-blocking'
    write_file(repo, LEDGER_PATH, json.dumps(bad) + '\n')
    rev_verdict = commit(repo, 'gamma gap-blocking verdict')
    out = json.loads(call_measure(repo, rev_verdict).stdout)
    check('badverdict-score-6', out['calibration_restraint_score'] == 6
          and out['coldread']['missing'][0]['reason'] == 'verdict:gap-blocking')

    # --- case: instruction entry with zero commands -> no credit ----------------
    bad = json.loads(ledger_json())
    bad['entries'][3]['commands_executed_count'] = 0
    write_file(repo, LEDGER_PATH, json.dumps(bad) + '\n')
    rev_nocmd = commit(repo, 'gamma zero commands')
    out = json.loads(call_measure(repo, rev_nocmd).stdout)
    check('nocmd-score-6', out['calibration_restraint_score'] == 6)
    check('nocmd-reason',
          out['coldread']['missing'] == [
              {'start': 19, 'heading': '### Gamma',
               'reason': 'commands-executed-count:0'}])

    # --- case: instruction class + verified-record verdict -> no credit ---------
    bad = json.loads(ledger_json())
    bad['entries'][3]['verdict'] = 'verified-record'
    write_file(repo, LEDGER_PATH, json.dumps(bad) + '\n')
    rev_misverd = commit(repo, 'gamma instruction verified-record')
    out = json.loads(call_measure(repo, rev_misverd).stdout)
    check('instr-verified-nocredit',
          out['calibration_restraint_score'] == 6
          and out['coldread']['missing'][0]['reason']
          == 'verdict-class:verified-record/instruction')

    # --- case: record class + verified-record verdict -> credited ---------------
    rec = json.loads(ledger_json())
    for e in rec['entries']:
        e['class'] = 'record'
        e['verdict'] = 'verified-record'
        e.pop('commands_executed_count', None)
    write_file(repo, LEDGER_PATH, json.dumps(rec) + '\n')
    rev_rec = commit(repo, 'all record verified-record')
    out = json.loads(call_measure(repo, rev_rec).stdout)
    check('record-credited', out['coldread']['sections_covered'] == 4
          and out['coldread']['box3_full_page'] is True
          and out['calibration_restraint_score'] == 8)

    # --- round-16 w2 MutateMeasure survivors -----------------------------------
    # (a) an unknown class is never credited
    unk = json.loads(ledger_json())
    unk['entries'][3]['class'] = 'frobnicate'
    write_file(repo, LEDGER_PATH, json.dumps(unk) + '\n')
    out = json.loads(call_measure(repo, commit(repo, 'unknown class')).stdout)
    check('unknown-class-nocredit', out['calibration_restraint_score'] == 6
          and out['coldread']['missing'][0]['reason'] == 'class:frobnicate')
    # (b) a record cannot pass as executed-ok
    rx = json.loads(ledger_json())
    rx['entries'][3]['class'] = 'record'
    write_file(repo, LEDGER_PATH, json.dumps(rx) + '\n')
    out = json.loads(call_measure(repo, commit(repo, 'record executed-ok')).stdout)
    check('record-executed-ok-nocredit', out['calibration_restraint_score'] == 6
          and out['coldread']['missing'][0]['reason']
          == 'verdict-class:executed-ok/record')
    # (c) whitespace-only trailing lines are stripped before hashing
    a = sectionize(b'# A\nbody\n   \n\t\n')[0]['sha256']
    check('trailing-whitespace-stripped',
          a == hashlib.sha256(b'# A\nbody').hexdigest())

    # --- case: SHONEN box-3 line lacks the ledger link -> 6 ---------------------
    write_file(repo, LEDGER_PATH, ledger_json())
    write_file(repo, 'SHONEN.md', SHONEN_NOLINK_TEXT)
    rev_nolink = commit(repo, 'box3 without ledger link')
    out = json.loads(call_measure(repo, rev_nolink).stdout)
    check('nolink-fullpage', out['coldread']['box3_full_page'] is True)
    check('nolink-flag', out['shonen']['box3_ledger_link'] is False
          and out['shonen']['box3_points'] is False)
    check('nolink-score-6', out['calibration_restraint_score'] == 6)

    # --- case: link on box 3's indented continuation line -> 8 -----------------
    write_file(repo, 'SHONEN.md', SHONEN_CONT_TEXT)
    rev_cont = commit(repo, 'box3 link on continuation line')
    out = json.loads(call_measure(repo, rev_cont).stdout)
    check('contlink-score-8', out['shonen']['box3_ledger_link'] is True
          and out['calibration_restraint_score'] == 8)

    # --- case: link only under box 4 -> box 3 not credited (6) -----------------
    write_file(repo, 'SHONEN.md', SHONEN_WRONGBOX_TEXT)
    rev_wrong = commit(repo, 'link under box 4 only')
    out = json.loads(call_measure(repo, rev_wrong).stdout)
    check('wrongbox-score-6', out['shonen']['box3_ledger_link'] is False
          and out['calibration_restraint_score'] == 6)

    # --- literal expected exits -------------------------------------------------
    os.remove(os.path.join(repo, 'SHONEN.md'))
    rev_noshonen = commit(repo, 'drop SHONEN.md')
    res = call_measure(repo, rev_noshonen)
    check('exit2-blob-missing', res.returncode == 2,
          'stderr=%r' % res.stderr.strip()[:120])
    res = call_measure(repo, '0' * 40)
    check('exit2-bad-rev', res.returncode == 2)
    res = run(sys.executable or 'python3', script, '--repo', repo)
    check('exit64-no-rev', res.returncode == 64)
    res = run(sys.executable or 'python3', script, '--rev', rev_base,
              '--bogus')
    check('exit64-unknown-arg', res.returncode == 64)
    res = call_measure(os.path.join(tmp, 'no-such-repo'), rev_base)
    check('exit2-no-repo', res.returncode == 2)

    passed = sum(1 for _, ok, _ in checks if ok)
    print('MEASURE_SELFTEST: %d/%d pass (scratch %s)' % (passed, len(checks), tmp))
    return 0 if passed == len(checks) else 1


def main(argv=None):
    parser = UsageParser(
        description='C1+C2 counting command: depth legs, SHONEN marks, '
                    'cold-read ledger coverage, SOURCES census.')
    parser.add_argument('--rev', help='git revision to measure')
    parser.add_argument('--repo', default=DEFAULT_REPO,
                        help='repository path (default: %(default)s)')
    parser.add_argument('--selftest', action='store_true',
                        help='build synthetic repos and self-check')
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.rev:
        parser.error('--rev is required')
    if not os.path.isdir(args.repo):
        print(json.dumps({'error': 'repo-not-found', 'repo': args.repo},
                         indent=2, sort_keys=True))
        return 2
    rev = git(args.repo, 'rev-parse', '--verify', '--quiet',
              '%s^{commit}' % args.rev)
    if rev.returncode != 0:
        print(json.dumps({'error': 'rev-missing', 'rev': args.rev,
                          'repo': args.repo},
                         indent=2, sort_keys=True))
        return 2
    missing = [p for p in REQUIRED_BLOBS if blob(args.repo, args.rev, p) is None]
    if missing:
        print(json.dumps({'error': 'blob-missing', 'rev': args.rev,
                          'missing': missing},
                         indent=2, sort_keys=True))
        return 2
    print(json.dumps(measure(args.repo, args.rev), indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
