#!/usr/bin/env python3
"""Round-52 C2 counter (calibration): lane records the round-51 closure found false, still standing at REV.

Usage: measure.py --lane LANE --rev REV [--explain]      measure.py --selftest

Reads git objects only (`git show REV:<path>`); never the working tree. Prints one line per check
`C2_CHECK <id> <ok|MISMATCH> <detail>` with --explain, then the summary line
`C2_R52: rev=<sha> m1=.. m2=.. m3=.. m4=.. m5=.. m6=.. total=N C2_R52_PASS=<true|false>`; exit 0 iff total == 0.
  m1  SKILL.md section `### Round-26 gate/probe registry — report interop` (2 checks): a) every "<count> ledger legs"
      phrase names the leg count of LEG_TABLE in tools/mte-interop.py at REV, and at least one such phrase exists;
      b) the registry-row mention "`mte-interop-check` (K/K)" exists exactly once and K equals that leg count.
  m2  SKILL.md `#### Gate/probe registry — round 51`, row `| fleet mutation runner |`: present; no "/tmp" without
      "TMPDIR" in the row (1 check).
  m3  three runner statements located by their claim text, never by line number (3 checks):
      a  the line holding "the maintained driver also prints the failing count" cites tools/mutate-and-run.sh:N[-M]
         and that REV range of the runner contains "old-string-count=";
      b  the line holding "marks the run DEGRADED" cites tools/mutate-and-run.sh:N[-M] and the range contains
         "MUTATE: DEGRADED";
      c  the bullet opening "- **One command replays every leg.**" exists and does not name
         "/tmp/tameshi-r4-2-regression" unless it also names TMPDIR.
  m4  .ufo/evidence/round-21/coldread/ledger.json: for each of the 20 round-51 re-key entries (read_rev 02ec217c…),
      one record in the top-level "corrections" list with heading, read_rev, reader (the T51W2ReadNN seat),
      reader_file (that seat's read file, present at REV), findings (list of {"quote": ...}, every quote a verbatim
      substring of the reader file after whitespace collapse, at least 20 characters) and wrong_expectations equal
      to len(findings). Frozen floors: T51W2Read20 quotes must cover the labels HIGH-1, HIGH-2, MED-1, MED-2;
      T51W2Read01 quotes must cover ":425" and ":569-574". One count per entry failing (20 checks).
  m5  corpus/knowledge/fleet-kill-rate-ledger.md: the drift-pins queue row stays byte-identical and a later line
      supersedes it: names drift-pins, "unmeasured by sweep", "supersed" and "case 10" (1 check).
  m6  every ledger entry whose seats name a "T52" seat carries "findings" (verbatim quotes, as m4, from a file in its
      "reader_files" list, present at REV) with wrong_expectations == len(findings) (one count per bad entry; 0 when
      there are none — the guard against repeating defect 3 in this round's re-key).
"""
import argparse, ast, json, re, subprocess, sys

R51_REKEY_REV = '02ec217c'
FLOORS = {'T51W2Read20': ['HIGH-1', 'HIGH-2', 'MED-1', 'MED-2'], 'T51W2Read01': [':425', ':569-574']}
WORDS = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine',
         10: 'ten', 11: 'eleven', 12: 'twelve'}
NUM = {v: k for k, v in WORDS.items()}
DRIFT_ROW = '| drift-pins | 13 | `c138d34c7f0dfe95` | unmeasured by sweep; hermetic |'
POINTER = re.compile(r'tools/mutate-and-run\.sh:(\d+)(?:-(\d+))?')


def show(lane, rev, path):
    r = subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (rev, path)], capture_output=True)
    return r.stdout.decode('utf-8', 'replace') if r.returncode == 0 else None


def squash(s):
    return re.sub(r'\s+', ' ', s).strip()


def section(text, heading, levels):
    """Lines from the exact heading line to the next heading of a level in `levels` (or EOF)."""
    lines = text.split('\n')
    try:
        i = lines.index(heading)
    except ValueError:
        return None
    out = [lines[i]]
    for ln in lines[i + 1:]:
        m = re.match(r'^(#{1,6}) ', ln)
        if m and len(m.group(1)) in levels:
            break
        out.append(ln)
    return '\n'.join(out)


def leg_count(src):
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', None) == 'LEG_TABLE' for t in node.targets):
            return len(node.value.keys)
    return None


def range_has(runner_lines, m, needle):
    a = int(m.group(1)); b = int(m.group(2) or a)
    return any(needle in runner_lines[k - 1] for k in range(a, b + 1) if 0 < k <= len(runner_lines))


def check_findings(rec_findings, reader_text, floors=()):
    if not isinstance(rec_findings, list) or reader_text is None:
        return 'findings-or-reader-missing'
    flat = squash(reader_text)
    quotes = []
    for f in rec_findings:
        q = f.get('quote') if isinstance(f, dict) else None
        if not isinstance(q, str) or len(squash(q)) < 20 or squash(q) not in flat:
            return 'quote-not-verbatim:%r' % (q[:60] if isinstance(q, str) else q)
        quotes.append(squash(q))
    for label in floors:
        if not any(label in q for q in quotes):
            return 'floor-uncovered:%s' % label
    return None


def measure(lane, rev):
    res = {}
    skill = show(lane, rev, 'SKILL.md') or ''
    mte = show(lane, rev, 'tools/mte-interop.py') or ''
    runner = (show(lane, rev, 'tools/mutate-and-run.sh') or '').split('\n')
    # m1
    n = None
    try:
        n = leg_count(mte)
    except SyntaxError:
        pass
    sec = section(skill, '### Round-26 gate/probe registry \u2014 report interop', (1, 2, 3)) or ''
    phrases = re.findall(r'\b(\w+) ledger legs\b', sec)
    bad = [p for p in phrases if NUM.get(p.lower(), int(p) if p.isdigit() else -1) != n]
    m1b = re.findall(r'`mte-interop-check` \((\d+)/(\d+)\)', sec)
    ok_b = len(m1b) == 1 and int(m1b[0][0]) == n and int(m1b[0][1]) == n
    res['m1'] = ((0 if n and phrases and not bad else 1) + (0 if ok_b else 1),
                 'legs=%s phrases=%s bad=%s mte_check_mentions=%s' % (n, phrases, bad, m1b))
    # m2
    sec51 = section(skill, '#### Gate/probe registry \u2014 round 51', (1, 2, 3, 4)) or ''
    row = next((ln for ln in sec51.split('\n') if ln.startswith('| fleet mutation runner |')), None)
    ok = row is not None and not ('/tmp' in row and 'TMPDIR' not in row)
    res['m2'] = (0 if ok else 1, 'row=%s tmp=%s tmpdir=%s' % (row is not None, row and '/tmp' in row, row and 'TMPDIR' in row))
    # m3
    lines = skill.split('\n')
    for key, phrase, needle in (('m3a', 'the maintained driver also prints the failing count', 'old-string-count='),
                                ('m3b', 'marks the run DEGRADED', 'MUTATE: DEGRADED')):
        hit = [ln for ln in lines if phrase in ln]
        m = POINTER.search(hit[0].split(phrase, 1)[1]) if len(hit) == 1 else None
        ok = bool(m) and range_has(runner, m, needle)
        res[key] = (0 if ok else 1, 'lines=%d pointer=%s' % (len(hit), m.group(0) if m else None))
    start = [i for i, ln in enumerate(lines) if ln.startswith('- **One command replays every leg.**')]
    if len(start) == 1:
        body = [lines[start[0]]]
        for ln in lines[start[0] + 1:]:
            if ln.startswith('- **') or not ln.strip() or ln.startswith('#'):
                break
            body.append(ln)
        b = ' '.join(body)
        ok = not ('/tmp/tameshi-r4-2-regression' in b and 'TMPDIR' not in b)
        res['m3c'] = (0 if ok else 1, 'bullet=1 tmp=%s tmpdir=%s' % ('/tmp/tameshi-r4-2-regression' in b, 'TMPDIR' in b))
    else:
        res['m3c'] = (1, 'bullet=%d' % len(start))
    # m4 / m6
    try:
        ledger = json.loads(show(lane, rev, '.ufo/evidence/round-21/coldread/ledger.json') or '{}')
    except ValueError:
        ledger = {}
    entries = ledger.get('entries') or []
    corr = ledger.get('corrections') or []
    r51 = [e for e in entries if str(e.get('read_rev', '')).startswith(R51_REKEY_REV)]
    m4_bad = [] if len(r51) == 20 else ['r51-entries=%d' % len(r51)]
    for e in r51:
        seat = next((s for s in e.get('seats', []) if s.startswith('T51W2Read')), None)
        recs = [c for c in corr if isinstance(c, dict) and c.get('heading') == e['heading']
                and str(c.get('read_rev', '')).startswith(R51_REKEY_REV) and c.get('reader') == seat]
        if len(recs) != 1:
            m4_bad.append('%s:records=%d' % (seat, len(recs))); continue
        c = recs[0]
        want = '.ufo/evidence/round-51/coldread/reads/%s.md' % seat
        if c.get('reader_file') is None:
            m4_bad.append('%s:reader_file' % seat); continue
        why = check_findings(c.get('findings'), show(lane, rev, want), FLOORS.get(seat, ()))
        if why is None and c.get('wrong_expectations') != len(c['findings']):
            why = 'count!=findings'
        if why:
            m4_bad.append('%s:%s' % (seat, why))
    res['m4'] = (len(m4_bad) if len(r51) == 20 else 20, 'r51_entries=%d corrections=%d bad=%s' % (len(r51), len(corr), m4_bad))
    m6_bad = []
    t52 = [e for e in entries if any(str(s).startswith('T52') for s in e.get('seats', []))]
    for e in t52:
        files = e.get('reader_files') or []
        texts = '\n'.join(show(lane, rev, f) or '' for f in files) if files else None
        why = check_findings(e.get('findings'), texts or None)
        if why is None and e.get('wrong_expectations') != len(e['findings']):
            why = 'count!=findings'
        if why:
            m6_bad.append('%s:%s' % (e.get('heading', '?')[:40], why))
    res['m6'] = (len(m6_bad), 't52_entries=%d bad=%s' % (len(t52), m6_bad))
    # m5
    led = (show(lane, rev, 'corpus/knowledge/fleet-kill-rate-ledger.md') or '').split('\n')
    idx = [i for i, ln in enumerate(led) if ln == DRIFT_ROW]
    sup = [ln for ln in led[idx[0] + 1:]] if len(idx) == 1 else []
    ok = any('drift-pins' in ln and 'unmeasured by sweep' in ln and 'supersed' in ln.lower() and 'case 10' in ln
             for ln in sup)
    res['m5'] = (0 if ok else 1, 'row=%d note=%s' % (len(idx), ok))
    return res


def summary(lane, rev, explain):
    full = subprocess.run(['git', '-C', lane, 'rev-parse', '--verify', rev + '^{commit}'],
                          capture_output=True, text=True).stdout.strip() or rev
    res = measure(lane, full)
    if explain:
        for k in sorted(res):
            print('C2_CHECK %s %s %s' % (k, 'ok' if res[k][0] == 0 else 'MISMATCH', res[k][1]))
    m3 = res['m3a'][0] + res['m3b'][0] + res['m3c'][0]
    total = res['m1'][0] + res['m2'][0] + m3 + res['m4'][0] + res['m5'][0] + res['m6'][0]
    print('C2_R52: rev=%s m1=%d m2=%d m3=%d m4=%d m5=%d m6=%d total=%d C2_R52_PASS=%s'
          % (full, res['m1'][0], res['m2'][0], m3, res['m4'][0], res['m5'][0], res['m6'][0], total,
             'true' if total == 0 else 'false'))
    return 0 if total == 0 else 1


def selftest():
    fails = 0
    def t(name, cond):
        nonlocal fails
        print('SELFTEST %s %s' % (name, 'ok' if cond else 'FAIL')); fails += 0 if cond else 1
    t('leg-count', leg_count("LEG_TABLE = {'a': 1, 'b': 2}\n") == 2)
    t('section-stops', section('# A\nx\n### H\ny\n#### I\nz\n## B\nq', '### H', (1, 2, 3)) == '### H\ny\n#### I\nz')
    t('quote-verbatim', check_findings([{'quote': 'abc  def ghi jkl mno pqr'}], 'xx abc def\nghi jkl mno pqr yy') is None)
    t('quote-forged', check_findings([{'quote': 'abc def ghi jkl mno pqr zz'}], 'abc def ghi jkl mno pqr') is not None)
    t('quote-short', check_findings([{'quote': 'abc'}], 'abc') is not None)
    t('floor', check_findings([{'quote': 'HIGH-1 is false here ok'}], 'HIGH-1 is false here ok', ['MED-1']) == 'floor-uncovered:MED-1')
    t('range', range_has(['a', 'MUTATE: DEGRADED x'], POINTER.search('tools/mutate-and-run.sh:1-2'), 'MUTATE: DEGRADED'))
    t('range-miss', not range_has(['a', 'b'], POINTER.search('tools/mutate-and-run.sh:1-2'), 'MUTATE: DEGRADED'))
    print('C2_SELFTEST: cases=8 failed=%d' % fails)
    return 1 if fails else 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--lane'); p.add_argument('--rev'); p.add_argument('--explain', action='store_true')
    p.add_argument('--selftest', action='store_true')
    a = p.parse_args()
    if a.selftest:
        return selftest()
    if not a.lane or not a.rev:
        p.error('--lane and --rev are required')
    return summary(a.lane, a.rev, a.explain)


if __name__ == '__main__':
    sys.exit(main())
