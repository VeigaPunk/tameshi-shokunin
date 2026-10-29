#!/usr/bin/env python3
"""Round-57 C1: enumerate the routed items of the seven closure spot-checks (rounds 50-56) at a revision.

Usage:
  extract-defects.py --lane LANE --rev REV [--manual KEYS_JSON] > defects.json
  extract-defects.py --selftest [--work DIR]

Successor of round-50/c1/extract-defects.py (rounds 40-49, `R<round>.<position>` ids, list items only).

Scope of a spot-check: every `## ` section whose heading contains "rout" (case-insensitive); several such
sections are all read (round 54 has two), other sections are skipped. Round 56's items sit under
`## 6. Verdict and routing`.

An item starts at a list line (`N. ` or `- `) or at a bold-led paragraph (a non-indented line that begins with
`**`) inside such a section; it continues over every following non-blank line that does not itself start an
item and ends at the next blank line. Paragraphs that are not list lines or bold-led (preambles, "Operator
note", "For the operator", closing remarks) are not items.

Ids are `R<round>.<n>`:
  * an item whose text begins (after an optional list marker) with `**R<round>.<n>` is labelled; n is that label;
  * otherwise n is the item's 1-based position in the section order of the spot-check's items, labelled ones
    included (a position among only the unlabelled ones would collide with a label whenever a spot-check
    labels some items and not others: round 51 labels item 1 only; with every item unlabelled, the two
    readings coincide: round 50);
  * an item that repeats an earlier label (round 54 `**R54.5 extended.**`) is folded into the earlier item:
    its text is kept in `extended_text`, its span in `extended` ([[line, end], ...]), its keys join the keys;
  * a duplicate id that is not a fold, a label of another round, or an unlabelled position that collides with a
    label, is an error (exit 2).
`routed_at` is the commit that ADDED the spot-check file (`git log --diff-filter=A`, oldest). Keys are the
item's backticked spans, S-ids and path-like tokens, minus GENERIC; MANUAL_JSON ({id: [keys]}) replaces them
by id (a manual key list that names an id outside the set is an error).

Output schema `tameshi-r57-defects-v1`: {schema, rev, count, per_round, defects[]}; each defect carries
id, round, file, line, end, routed_at, file_sha256, text (first 600 chars), text_chars, keys, and for a folded
item extended, extended_text.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROUNDS = range(50, 57)
SCHEMA = 'tameshi-r57-defects-v1'
GENERIC = {'SKILL.md', 'SCORECARD.md', 'LOG.md', 'SHONEN.md', 'README.md', 'QUALITY.md', 'SOURCES.md',
           'corpus/SOURCES.md', 'corpus/QUALITY.md', 'corpus/README.md', '[~]', '--selftest', 'measure.py'}
LIST_RE = re.compile(r'^(?:\d+\.|-)\s+(.*)$')
LABEL_RE = re.compile(r'^\*\*R(\d+)\.(\d+)\b')
PATH_RE = re.compile(r'(?<![\w/.-])((?:[\w.-]+/)*[\w.-]+\.(?:md|py|sh|json|mjs|stdout|spec|jsonl))\b')
SID_RE = re.compile(r'\bS\d{3}\b')


def spotcheck_path(r):
    return 'corpus/lessons/round-%d-verifier-spotcheck.md' % r


def git(lane, *args):
    return subprocess.run(['git', '-C', lane] + list(args), check=True, capture_output=True).stdout


def items_of(text, rnd):
    """Return [{id, label, line, end, text}] in file order for a spot-check's text; raises ValueError."""
    out, inside, cur = [], False, None
    for no, line in enumerate(text.split('\n'), 1):
        if line.startswith('## '):
            inside = 'rout' in line.lower()
            cur = None
            continue
        if not inside:
            continue
        m = LIST_RE.match(line)
        start = m.group(1).strip() if m else (line.strip() if line.startswith('**') else None)
        if start is not None:
            lab = LABEL_RE.match(start)
            if lab and int(lab.group(1)) != rnd:
                raise ValueError('round %d line %d: label of another round: %s' % (rnd, no, lab.group(0)))
            cur = {'line': no, 'end': no, 'text': start, 'label': int(lab.group(2)) if lab else None}
            out.append(cur)
        elif not line.strip():
            cur = None
        elif cur is not None:
            cur['text'] += ' ' + line.strip()
            cur['end'] = no
    items, seen = [], {}
    for pos, it in enumerate(out, 1):
        n = it['label'] if it['label'] is not None else pos
        did = 'R%d.%d' % (rnd, n)
        if it['label'] is not None and did in seen:
            host = seen[did]
            host.setdefault('extended', []).append([it['line'], it['end']])
            host['extended_text'] = (host.get('extended_text', '') + ' ' + it['text']).strip()
            continue
        if did in seen:
            raise ValueError('round %d line %d: id %s collides with line %d' % (rnd, it['line'], did, seen[did]['line']))
        rec = {'id': did, 'line': it['line'], 'end': it['end'], 'text': it['text']}
        seen[did] = rec
        items.append(rec)
    return items


def keys_of(text):
    keys = []
    for span in re.findall(r'`([^`\n]+)`', text):
        span = span.strip()
        if span and span not in GENERIC and len(span) >= 4:
            keys.append(span)
    keys += [p for p in PATH_RE.findall(text) if p not in GENERIC]
    keys += SID_RE.findall(text)
    seen, uniq = set(), []
    for k in keys:
        if k not in seen:
            seen.add(k)
            uniq.append(k)
    return uniq


def build(lane, rev, manual, rounds=ROUNDS, path_of=spotcheck_path):
    defects, per_round = [], {}
    for r in rounds:
        path = path_of(r)
        blob = git(lane, 'show', '%s:%s' % (rev, path))
        routed_at = git(lane, 'log', '--diff-filter=A', '--format=%H', rev, '--', path).decode().split()[-1]
        digest = hashlib.sha256(blob).hexdigest()
        items = items_of(blob.decode('utf-8'), r)
        per_round[str(r)] = len(items)
        for it in items:
            extra = it.get('extended_text', '')
            keys = manual[it['id']] if it['id'] in manual else keys_of(it['text'] + ' ' + extra)
            d = {'id': it['id'], 'round': r, 'file': path, 'line': it['line'], 'end': it['end'],
                 'routed_at': routed_at, 'file_sha256': digest, 'text': it['text'][:600],
                 'text_chars': len(it['text']), 'keys': keys}
            if extra:
                d['extended'] = it['extended']
                d['extended_text'] = extra[:600]
            defects.append(d)
    unknown = sorted(set(manual) - {d['id'] for d in defects})
    if unknown:
        raise ValueError('manual keys name ids outside the set: %s' % ', '.join(unknown))
    return {'schema': SCHEMA, 'rev': rev, 'count': len(defects), 'per_round': per_round, 'defects': defects}


def selftest(work):
    work = work or tempfile.mkdtemp(prefix='r57-extract-selftest-')
    own = not os.path.isdir(work) or not os.listdir(work)
    os.makedirs(work, exist_ok=True)
    if os.listdir(work):
        print('selftest: --work must be empty', file=sys.stderr)
        return 2
    fails = []

    def check(name, cond, detail=''):
        print('SELFTEST %s %s%s' % ('ok' if cond else 'FAIL', name, (' ' + detail) if detail and not cond else ''))
        if not cond:
            fails.append(name)

    try:
        # pure parser cases
        lab = ('## Step-1 conformance\n\n1. **R9.7 not in scope** `skip.py`.\n\n## Routed defects\n\n'
               '1. **R9.1 first.** `a/b.py` S101 wraps\n   onto two lines.\n2. **R9.2 second.** `x`\n'
               '3. **R9.3 third.**\n\nTail paragraph is not an item.\n\n## Closure\n\n1. out of scope\n')
        it = items_of(lab, 9)
        check('labelled ids', [i['id'] for i in it] == ['R9.1', 'R9.2', 'R9.3'], str([i['id'] for i in it]))
        check('labelled continuation', it[0]['line'] == 7 and it[0]['end'] == 8 and 'onto two lines' in it[0]['text'])
        check('tail paragraph excluded', 'Tail' not in ' '.join(i['text'] for i in it))
        unl = '## Routed defects for next round\n\n1. **No label one.** x\n2. **No label two.** y\n3. plain\n- dash\n\nOperator note: z\n'
        it = items_of(unl, 8)
        check('unlabelled positions', [i['id'] for i in it] == ['R8.1', 'R8.2', 'R8.3', 'R8.4'], str([i['id'] for i in it]))
        mix = '## Routed\n\n1. **R7.1, labelled.** a\n2. **Unlabelled second.** b\n3. **R7.3 labelled.** c\n4. d\n'
        it = items_of(mix, 7)
        check('mixed positions', [i['id'] for i in it] == ['R7.1', 'R7.2', 'R7.3', 'R7.4'], str([i['id'] for i in it]))
        two = ('## Routed defects (a)\n\n**R6.1 para one.** first line\n`second line` of it\n\n**R6.2 para two.** y\n\n'
               '---\n\n## Closure\n\nprose\n\n## Routed defects - one new\n\n**R6.3 new.** z\n\n**R6.1 extended.** more\n\n'
               'R6.1-R6.2 as filed are unaffected.\n')
        it = items_of(two, 6)
        check('two headings', [i['id'] for i in it] == ['R6.1', 'R6.2', 'R6.3'], str([i['id'] for i in it]))
        check('bold paragraph continuation', it[0]['end'] == it[0]['line'] + 1 and '`second line`' in it[0]['text'])
        check('fold extended', it[0].get('extended') == [[it[2]['line'] + 2, it[2]['line'] + 2]] and
              'more' in it[0].get('extended_text', ''), str(it[0].get('extended')))
        check('closing remark excluded', all('unaffected' not in i['text'] for i in it))
        try:
            items_of('## Routed\n\n1. **R5.2 a.**\n2. **R4.1 wrong round.**\n', 5)
            check('foreign label rejected', False)
        except ValueError:
            check('foreign label rejected', True)
        try:
            items_of('## Routed\n\n1. **R5.2 a.**\n2. **b.**\n', 5)
            check('collision rejected', False)
        except ValueError:
            check('collision rejected', True)
        check('keys_of', keys_of('see `tools/x.py` and S012, `SKILL.md`, results/out.json') ==
              ['tools/x.py', 'results/out.json', 'S012'])
        # fixture repo end to end
        repo = os.path.join(work, 'repo')
        os.makedirs(os.path.join(repo, 'corpus', 'lessons'))
        subprocess.run(['git', '-C', repo, 'init', '-q'], check=True)
        top = subprocess.run(['git', '-C', repo, 'rev-parse', '--show-toplevel'], check=True,
                             capture_output=True, text=True).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(repo):
            print('selftest: fixture toplevel mismatch', file=sys.stderr)
            return 2
        ident = ['-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid']

        def commit(msg):
            subprocess.run(['git', '-C', repo, 'add', '-A'], check=True)
            subprocess.run(['git', '-C', repo] + ident + ['commit', '-q', '-m', msg], check=True)
            return git(repo, 'rev-parse', 'HEAD').decode().strip()

        bodies = {50: unl, 51: mix.replace('R7.', 'R51.'), 52: lab.replace('R9.', 'R52.'),
                  53: two.replace('R6.', 'R53.')}
        for r in (50, 51, 52, 53):
            with open(os.path.join(repo, spotcheck_path(r)), 'w') as fh:
                fh.write(bodies[r])
        first = commit('add spot-checks')
        with open(os.path.join(repo, spotcheck_path(50)), 'a') as fh:
            fh.write('\nlater edit\n')
        tip = commit('edit one')
        out = build(repo, tip, {'R53.2': ['k1', 'k2']}, rounds=range(50, 54))
        ids = [d['id'] for d in out['defects']]
        check('fixture count', out['count'] == 4 + 4 + 3 + 3 and ids[:4] == ['R50.1', 'R50.2', 'R50.3', 'R50.4'], str(out['per_round']))
        check('fixture per_round', out['per_round'] == {'50': 4, '51': 4, '52': 3, '53': 3}, str(out['per_round']))
        check('routed_at is the adding commit', {d['routed_at'] for d in out['defects']} == {first})
        check('file_sha256 of rev blob', out['defects'][0]['file_sha256'] ==
              hashlib.sha256(git(repo, 'show', '%s:%s' % (tip, spotcheck_path(50)))).hexdigest())
        check('manual keys replace', [d for d in out['defects'] if d['id'] == 'R53.2'][0]['keys'] == ['k1', 'k2'])
        check('folded keys include extension', 'R53.1' in ids and 'extended_text' in
              [d for d in out['defects'] if d['id'] == 'R53.1'][0])
        try:
            build(repo, tip, {'R99.1': ['x']}, rounds=range(50, 54))
            check('manual unknown id rejected', False)
        except ValueError:
            check('manual unknown id rejected', True)
    finally:
        if own:
            shutil.rmtree(work, ignore_errors=True)
    print('SELFTEST %s' % ('PASS' if not fails else 'FAIL ' + ','.join(fails)))
    return 0 if not fails else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--manual')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--work')
    a = ap.parse_args()
    if a.selftest:
        return selftest(a.work)
    if not a.lane or not a.rev:
        ap.error('--lane and --rev are required')
    manual = json.load(open(a.manual)) if a.manual else {}
    try:
        out = build(a.lane, a.rev, manual)
    except ValueError as e:
        print('extract-defects: %s' % e, file=sys.stderr)
        return 2
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
