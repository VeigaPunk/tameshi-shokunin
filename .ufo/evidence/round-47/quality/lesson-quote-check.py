#!/usr/bin/env python3
"""Round-47 lesson-quote byte-fidelity checker (QUALITY criterion 91).

Mistake it catches (round-46 routed defect 4, class reference-drift + vacuous): a lesson's located quote printed
with a folded dash (`9.8 %-16.3 %` for the source's `9.8 %–16.3 %`) passes every counter, because every counter
compares through its own `fold`. This checker compares UNFOLDED text.

  lesson-quote-check.py [--lane LANE] LESSON.md [LESSON.md ...]   exit 0 clean, 1 on any bad quote, 2 on usage
  lesson-quote-check.py --selftest

A block is a `### ` subsection of the lesson (when the lesson has any), else a bullet (a `- ` line and its
continuation lines). In every block that names at least one committed snapshot (a backticked
`.ufo/evidence/<round>/<...>/sources/<file>` path), every double-quoted span of at least 6 whitespace tokens
(straight "..." or curly “...”) must occur in the text of one of THAT block's snapshots after only tag-strip,
entity-unescape and whitespace collapse (a `.txt` snapshot only whitespace collapse; a `.json` snapshot is also tried as the concatenation of its string
values); no dash, quote, soft-hyphen or ligature folding. A quote that occurs only after the counter-style fold
fails unless its block says `printed folded` (the declared fold). A block with no snapshot path is `unbound`
(reported, not failed: legacy lessons bind by prose).
Output: `LQ <PASS|FAIL|FOLD-DECLARED> <snapshot> <first words>` per quote, then
`LESSON_QUOTE_CHECK: file=... blocks=N quotes=Q bad=B unbound=U`.
"""
import argparse
import html
import json
import os
import re
import sys
import tempfile
import unicodedata

SNAP_RE = re.compile(r'`(\.ufo/evidence/[^`\s]*/sources/[^`\s]+)`')
QUOTE_RE = re.compile(r'"([^"]{10,600})"|\u201c([^\u201d]{10,600})\u201d')
LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))


def collapse(text):
    return ' '.join(text.split())


def fold(text):
    text = unicodedata.normalize('NFKC', text)
    for a, b in (('\u2018', "'"), ('\u2019', "'"), ('\u201c', '"'), ('\u201d', '"'), ('\u2013', '-'), ('\u2014', '-'),
                 ('\u00ad', ''), ('\u00a0', ' '), ('\u200b', '')):
        text = text.replace(a, b)
    return collapse(text)


def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings(v)


def snapshot_text(lane, rel):
    path = os.path.join(lane, rel)
    if not os.path.isfile(path):
        return None
    raw = open(path, 'rb').read().decode('utf-8', 'replace')
    if rel.endswith('.json'):
        try:
            raw = ' '.join(strings(json.loads(raw))) + ' ' + raw
        except ValueError:
            pass
    if rel.endswith('.txt'):
        return collapse(raw)
    text = re.sub(r'(?is)<(script|style)\b.*?</\1\s*>', ' ', raw)
    text = re.sub(r'(?s)<[^>]*>', ' ', text)
    return collapse(html.unescape(text))


def blocks(text):
    parts = [p for p in re.split(r'(?m)^(?=### )', text) if p.startswith('### ')]
    if parts:
        return parts
    out, cur = [], []
    for line in text.split('\n'):
        if line.startswith('- ') and cur:
            out.append('\n'.join(cur))
            cur = []
        cur.append(line)
    out.append('\n'.join(cur))
    return out


def check(lane, name, text, emit=print):
    n_blocks = n_quotes = bad = unbound = 0
    cache = {}
    for blk in blocks(text):
        snaps = SNAP_RE.findall(blk)
        quotes = [collapse(m.group(1) or m.group(2)) for m in QUOTE_RE.finditer(blk)]
        quotes = [q for q in quotes if len(q.split()) >= 6]
        if not quotes:
            continue
        if not snaps:
            unbound += 1
            continue
        n_blocks += 1
        declared = 'printed folded' in blk.lower()
        for q in quotes:
            n_quotes += 1
            verdict, where = 'FAIL', snaps[0]
            for s in snaps:
                if s not in cache:
                    cache[s] = snapshot_text(lane, s)
                t = cache[s]
                if t is None:
                    continue
                if q in t:
                    verdict, where = 'PASS', s
                    break
                if fold(q) in fold(t):
                    verdict, where = ('FOLD-DECLARED' if declared else 'FAIL'), s
                    break
            bad += verdict == 'FAIL'
            emit('LQ %s %s %r' % (verdict, os.path.basename(where), q[:60]))
    emit('LESSON_QUOTE_CHECK: file=%s blocks=%d quotes=%d bad=%d unbound=%d' % (name, n_blocks, n_quotes, bad, unbound))
    return bad


def selftest():
    cases = []
    with tempfile.TemporaryDirectory(prefix='tameshi-r47-lq-') as d:
        os.makedirs(os.path.join(d, '.ufo/evidence/r/x/sources'))

        def put(name, data):
            with open(os.path.join(d, '.ufo/evidence/r/x/sources', name), 'w', encoding='utf-8') as fh:
                fh.write(data)
        put('a.html', '<html><body><p>Undetected flaky failures are 9.8 %\u201316.3 % of failed pipeline runs in industry.</p></body></html>')
        put('b.html', '<html><body><p>A second page states that environment changes move flake rates between pipelines.</p></body></html>')
        put('c.json', json.dumps({'entry': {'abstract': 'An automatic rerun costs 0.02 cents each time it is triggered.'}}))
        s = lambda n: '`.ufo/evidence/r/x/sources/%s`' % n
        q_exact = 'Undetected flaky failures are 9.8 %\u201316.3 % of failed pipeline runs'
        q_fold = q_exact.replace('\u2013', '-')

        def run(text):
            lines = []
            bad = check(d, 'fx.md', text, emit=lines.append)
            return bad, lines
        cases.append(('Q01_exact_passes', run('### S1\n- %s\n- Located quote: "%s"\n' % (s('a.html'), q_exact))[0] == 0))
        cases.append(('Q02_folded_dash_fails', run('### S1\n- %s\n- Located quote: "%s"\n' % (s('a.html'), q_fold))[0] == 1))
        cases.append(('Q03_folded_dash_declared_passes', run('### S1\n- %s\n- Located quote (printed folded: U+2013 -> -): "%s"\n' % (s('a.html'), q_fold))[0] == 0))
        cases.append(('Q04_quote_absent_fails', run('### S1\n- %s\n- Located quote: "this sentence never occurs in that snapshot at all"\n' % s('a.html'))[0] == 1))
        cases.append(('Q05_bound_by_block_not_first_path', run('### S1\n- %s %s\n- Located quote: "A second page states that environment changes move flake rates"\n' % (s('a.html'), s('b.html')))[0] == 0))
        cases.append(('Q06_quote_in_other_blocks_snapshot_fails', run('### S1\n- %s\n- Located quote: "A second page states that environment changes move flake rates"\n### S2\n- %s\n' % (s('a.html'), s('b.html')))[0] == 1))
        cases.append(('Q07_json_string_value_passes', run('### S1\n- %s\n- Located quote: "An automatic rerun costs 0.02 cents each time it is triggered"\n' % s('c.json'))[0] == 0))
        cases.append(('Q08_curly_quotes_are_parsed', run('### S1\n- %s\n- Located quote: \u201c%s\u201d\n' % (s('a.html'), q_fold))[0] == 1))
        cases.append(('Q09_missing_snapshot_fails', run('### S1\n- %s\n- Located quote: "%s"\n' % (s('nope.html'), q_exact))[0] == 1))
        bad, lines = run('- no snapshot here "this quote has no snapshot path in its block at all"\n')
        cases.append(('Q10_unbound_block_reported_not_failed', bad == 0 and 'unbound=1' in lines[-1]))
        cases.append(('Q11_short_quotes_ignored', run('### S1\n- %s\n- "too short here"\n' % s('a.html'))[0] == 0))
    failed = 0
    for name, ok in cases:
        failed += not ok
        print('%s %s' % ('PASS' if ok else 'FAIL', name))
    print('LESSON_QUOTE_SELFTEST: cases=%d failed=%d' % (len(cases), failed))
    return 0 if failed == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', default=LANE)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('files', nargs='*')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.files:
        ap.error('at least one lesson file is required')
    bad = 0
    for f in a.files:
        bad += check(a.lane, f, open(f, encoding='utf-8').read())
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
