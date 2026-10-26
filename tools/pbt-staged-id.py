#!/usr/bin/env python3
"""Property-based generator for tools/staged-id-guard.py (tameshi round 49, C2 / F10).

This is a generator, not a fixture replay: each case is drawn from a seeded random
source, small on purpose (0-8 rows per table, QuickCheck `sized`), and the guard is
asked the question through its frozen CLI only.  Nothing here imports, execs or
re-reads the guard's source: the expected answer comes from an oracle written from
the guard's *documented* contract:

  * a registry/staged row is a line matching ``^ {0,3}\\|\\s*(S\\d{3,})\\s*\\|``
    (CORPUS census rule; a row at 4+ spaces is not a row, which is the whole point of
    the 0-3-space extractor);
  * ``collisions`` are the ids present in both tables, sorted numerically;
  * ``held`` / ``unmapped`` / ``naive_map`` / ``cascade`` / ``next_free`` /
    ``registry_max`` / ``staged_max`` / ``safe_floor`` / ``column0_*`` follow the
    module docstring's bullets;
  * ``--map`` admissibility follows validate_map's docstring: injective, S-id
    targets, a registry target only as the document's own dedupe id, never another
    staged id, fresh targets at or above the safe floor, every collision covered,
    no colliding id left on itself, no undocumented row decided, no held document
    moved off its registry id;
  * exit semantics are the OBSERVED ones recorded in the round-49 contract
    (claims.C2.guard_exit_semantics_observed): 0 answered/admitted, 1 analysis
    refused (unmapped or cascade non-empty) or map inadmissible, 2 setup refusal.
    The module docstring names exit 1 only for an inadmissible map; the observed
    1-for-refused-analysis is what this generator checks (recorded as a doc
    mismatch, not silently ignored).

For every case the generated case is dumped (one JSONL line per run) and the
guard's answer is compared with the oracle.  The first disagreement is a
counterexample: the run stops, prints ``VIOLATION`` and exits 1.  The distribution
is observed, not assumed (QuickCheck classify/collect): every case is classified
into the twelve frozen classes and the counts are printed.

Interface (frozen for the round-49 C2 counter):

  python3 -I pbt-staged-id.py --guard GUARD --seed INT --cases N --dump FILE
  python3 -I pbt-staged-id.py --selftest

Exit 0 = no violation over the N cases, 1 = violation (counterexample=index),
2 = setup problem (bad arguments, unwritable dump, unreadable guard).  Last stdout
line: ``PBT_STAGED_ID: cases=<run> violations=<0|1> counterexample=<index|none>
classes=<k=v,...>``.  Deterministic for a seed: one ``random.Random(seed)``.
"""
import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROW_RE = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
ROW_ANY = re.compile(r'^( *)\|\s*(S\d{3,})\s*\|')
COLUMN0_RE = re.compile(r'^\|\s*(S\d{3,})\s*\|')
URL_RE = re.compile(r'https?://[^\s|,;]+')
SID_RE = re.compile(r'S\d{3,}')
PROSE_RE = re.compile(r'\s+[\u2014\u2013]\s+')

CLASSES = ('indent_1_3', 'indent_4_plus', 'id_4_plus_digits', 'collision', 'no_collision',
           'held', 'unmapped', 'cascade', 'refusal', 'url_form_variant', 'map',
           'map_inadmissible')
CLASS_MIN = 20                     # this seat's observed distribution floor (contract: 10)
GUARD_TIMEOUT = 60
SHA_KEYS = ('registry_sha256', 'staged_sha256')

HEAD = ('| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck '
        '| used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n')


class Refused(Exception):
    """The oracle's read of the documented contract says: setup refusal (exit 2)."""


# --------------------------------------------------------------------------------------------
# oracle: the documented contract, implemented independently of the guard's source
# --------------------------------------------------------------------------------------------
def document_key(cells):
    """The row's document: its URL/DOI, else a path-like source head (docstring bullet)."""
    blob = ' '.join(cells[1:6])
    found = URL_RE.search(blob)
    if found:
        return found.group(0).rstrip('.,;)]')
    source = cells[1] if len(cells) > 1 else ''
    head = PROSE_RE.split(source)[0].strip()
    openable = '/' in head or (' ' not in head and re.search(r'\.[A-Za-z0-9]{2,6}$', head))
    return head if len(head) > 8 and openable else ''


def normalise_document(raw):
    """Form-insensitive identity: scheme, www., trailing slash, case (docstring)."""
    text = raw.strip().lower()
    text = re.sub(r'^https?://', '', text)
    text = re.sub(r'^www\.', '', text)
    return text.rstrip('/')


def id_number(sid):
    if not SID_RE.fullmatch(sid):
        raise Refused('not an S-id')
    if len(sid) > 12:              # observed guard rule; not generated, kept for fidelity
        raise Refused('S-id too long')
    return int(sid[1:])


def parse_rows(text):
    """{id: {document, cells, lineno}} in file order; refusal on a short row or a repeat."""
    rows = {}
    for lineno, line in enumerate(text.splitlines(), 1):
        match = ROW_RE.match(line)
        if not match:
            continue
        sid = match.group(1)
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        if len(cells) < 5:
            raise Refused('malformed row %s (%d cells)' % (sid, len(cells)))
        if sid in rows:
            raise Refused('duplicate id %s' % sid)
        rows[sid] = {'document': document_key(cells), 'cells': len(cells), 'lineno': lineno}
    return rows


def analyse_fields(registry, staged, staged_text):
    collisions = sorted(set(registry) & set(staged), key=id_number)
    column0 = sorted({m.group(1) for m in
                      (COLUMN0_RE.match(line) for line in staged_text.splitlines()) if m},
                     key=id_number)
    registry_docs = {}
    for sid, row in registry.items():
        if row['document']:
            registry_docs.setdefault(normalise_document(row['document']), sid)
    held, unmapped = {}, []
    for sid in collisions:
        key = staged[sid]['document']
        if not key:
            unmapped.append(sid)
        elif normalise_document(key) in registry_docs:
            held[sid] = registry_docs[normalise_document(key)]
    top = max((id_number(sid) for sid in registry), default=0)
    staged_top = max((id_number(sid) for sid in staged), default=0)
    naive = {}
    for index, sid in enumerate(collisions, 1):
        naive[sid] = 'S%03d' % (top + index)
    cascade = sorted((target for target in naive.values() if target in staged), key=id_number)
    return {
        'registry_rows': len(registry),
        'staged_rows': len(staged),
        'collisions': collisions,
        'collision_count': len(collisions),
        'unmapped': unmapped,
        'held': held,
        'naive_map': naive,
        'cascade': cascade,
        'cascade_count': len(cascade),
        'refused': bool(unmapped) or bool(cascade),
        'next_free': 'S%03d' % (top + 1),
        'registry_max': 'S%03d' % top,
        'staged_max': 'S%03d' % staged_top,
        'safe_floor': 'S%03d' % (max(top, staged_top) + 1),
        'extractor': '0-3space',
        'column0_collisions': [sid for sid in collisions if sid in column0],
        'column0_miss': [sid for sid in collisions if sid not in column0],
        'registry_docs': len(registry_docs),
    }


def map_fields(registry, staged, analysis, map_doc):
    """validate_map's documented rules, as (ok, fields); each refusal as (class, ids)."""
    if not isinstance(map_doc, dict) or not isinstance(map_doc.get('map'), dict):
        raise Refused('map file carries no "map" object')
    mapping = {}
    for key, target in map_doc['map'].items():
        bare = key[7:] if isinstance(key, str) and key.startswith('staged:') else key
        if not isinstance(bare, str) or not SID_RE.fullmatch(bare):
            raise Refused('map key is not an S-id')
        if not isinstance(target, str) or not SID_RE.fullmatch(target):
            raise Refused('map target is not an S-id')
        mapping[bare] = target
    floor = 'S%03d' % (max([id_number(sid) for sid in list(registry) + list(staged)] + [0]) + 1)
    targets = list(mapping.values())
    injective = len(targets) == len(set(targets))
    carry, clash, staged_clash, below_floor, dedupe = [], [], [], [], {}
    for staged_id, target in sorted(mapping.items(), key=lambda kv: id_number(kv[0])):
        if staged_id not in staged:
            carry.append(staged_id)
            continue
        if target in registry:
            same = (bool(registry[target]['document']) and
                    normalise_document(registry[target]['document']) ==
                    normalise_document(staged[staged_id]['document']))
            if same:
                dedupe[staged_id] = target
            else:
                clash.append(target)
            continue
        if target in staged:
            staged_clash.append(target)
            continue
        if id_number(target) < id_number(floor):
            below_floor.append(target)
    uncovered = [sid for sid in analysis['collisions'] if sid not in mapping]
    selfmap = [sid for sid in analysis['collisions'] if mapping.get(sid) == sid]
    undocumented = [sid for sid in analysis['unmapped'] if sid in mapping]
    held_moved = [sid for sid, registry_id in analysis['held'].items()
                  if sid in mapping and mapping[sid] != registry_id]
    # reason order follows the guard's own order: injectivity, then the per-entry
    # "does not carry" refusals, then the aggregate ones.
    reasons = []
    if not injective:
        reasons.append(('injective',))
    for sid in carry:
        reasons.append(('carry', sid))
    if clash:
        reasons.append(('registry', tuple(sorted(clash, key=id_number))))
    if staged_clash:
        reasons.append(('staged', tuple(sorted(staged_clash, key=id_number))))
    if below_floor:
        reasons.append(('floor', tuple(sorted(below_floor, key=id_number))))
    if uncovered:
        reasons.append(('cover', tuple(uncovered)))
    if selfmap:
        reasons.append(('self', tuple(selfmap)))
    if undocumented:
        reasons.append(('undocumented', tuple(undocumented)))
    if held_moved:
        reasons.append(('held', tuple(held_moved)))
    return {
        'map_entries': len(mapping),
        'map_targets': len(set(targets)),
        'map_clash': clash,
        'map_staged_clash': staged_clash,
        'map_below_floor': below_floor,
        'map_dedupe': dedupe,
        'map_uncovered': uncovered,
        'map_undocumented': undocumented,
        'map_held_moved': held_moved,
        'map_floor': floor,
        'map_ok': not reasons,
        'map_reasons': reasons,
    }


def oracle_case(case):
    """(expected exit, expected JSON fields) for one case; fields None on setup refusal."""
    try:
        registry = parse_rows(case['registry'])
        staged = parse_rows(case['staged'])
        analysis = analyse_fields(registry, staged, case['staged'])
        if case['map'] is None:
            expected = dict(analysis)
            expected['verdict'] = 'refused' if analysis['refused'] else 'answered'
            return (1 if analysis['refused'] else 0), expected
        fields = map_fields(registry, staged, analysis, case['map'])
        expected = dict(analysis)
        expected.update(fields)
        expected['analysis_refused'] = analysis['refused']
        expected['refused'] = not fields['map_ok']
        expected['verdict'] = 'admitted' if fields['map_ok'] else 'inadmissible'
        return (0 if fields['map_ok'] else 1), expected
    except Refused:
        return 2, None


def reason_classes(reasons):
    """Project the guard's prose reasons onto (class, ids) so the prose itself is not graded."""
    out = []
    for reason in reasons if isinstance(reasons, list) else ['<not-a-list>']:
        text = reason if isinstance(reason, str) else repr(reason)
        tail = text.rsplit(': ', 1)[-1]
        if 'injective' in text:
            out.append(('injective',))
        elif 'does not carry' in text:
            out.append(('carry', tail))
        elif 'collide with registry ids' in text:
            out.append(('registry', tuple(tail.split(','))))
        elif 'still staged ids' in text:
            out.append(('staged', tuple(tail.split(','))))
        elif 'below the safe floor' in text:
            out.append(('floor', tuple(tail.split(','))))
        elif 'does not cover' in text:
            out.append(('cover', tuple(tail.split(','))))
        elif 'on itself' in text:
            out.append(('self', tuple(tail.split(','))))
        elif 'undocumented row' in text:
            out.append(('undocumented', tuple(tail.split(','))))
        elif 'held document off' in text:
            out.append(('held', tuple(re.findall(r'S\d+', tail)[:1])))
        else:
            out.append(('unknown', text))
    return out


def check(case, observed):
    """None when the run matches the oracle; otherwise a one-line reason."""
    expected_exit, expected = oracle_case(case)
    if observed['exit'] != expected_exit:
        return 'exit %r, oracle expects %r' % (observed['exit'], expected_exit)
    answer = observed['json']
    if not isinstance(answer, dict):
        return 'stdout is not one JSON object: %r' % (observed['stdout'][:200],)
    if expected_exit == 2:
        if answer.get('verdict') != 'setup_refusal':
            return 'setup refusal without verdict=setup_refusal: %r' % (answer.get('verdict'),)
        if not isinstance(answer.get('reason'), str) or not answer['reason']:
            return 'setup refusal without a reason string'
        return None
    if answer.get('verdict') != expected['verdict']:
        return 'verdict %r, oracle %r' % (answer.get('verdict'), expected['verdict'])
    want = set(expected) | set(SHA_KEYS)
    got = set(answer)
    if got != want:
        return 'field set mismatch: extra=%s missing=%s' % (sorted(got - want),
                                                            sorted(want - got))
    for key in sorted(expected):
        mine, theirs = expected[key], answer.get(key)
        if key == 'map_reasons':
            theirs = reason_classes(theirs)
        if mine != theirs:
            return 'field %s: guard %r, oracle %r' % (key, theirs, mine)
    return None


# --------------------------------------------------------------------------------------------
# classification (QuickCheck classify/collect): the twelve frozen classes, same predicates
# --------------------------------------------------------------------------------------------
def case_classes(case, exit_code, answer):
    found = set()
    for line in case['registry'].splitlines() + case['staged'].splitlines():
        match = ROW_ANY.match(line)
        if match:
            indent = len(match.group(1))
            if 1 <= indent <= 3:
                found.add('indent_1_3')
            elif indent >= 4:
                found.add('indent_4_plus')
            if indent <= 3 and len(match.group(2)) >= 5:
                found.add('id_4_plus_digits')
    if case['map'] is None:
        if exit_code in (0, 1) and isinstance(answer, dict):
            found.add('collision' if answer.get('collision_count', 0) > 0 else 'no_collision')
            if answer.get('held'):
                found.add('held')
            if answer.get('unmapped'):
                found.add('unmapped')
            if answer.get('cascade'):
                found.add('cascade')
        if exit_code == 2:
            found.add('refusal')
    else:
        found.add('map')
        if exit_code == 1:
            found.add('map_inadmissible')
        if exit_code == 2:
            found.add('refusal')
    registry_urls = {}
    for url in URL_RE.findall(case['registry']):
        url = url.rstrip('.,;)]')
        registry_urls.setdefault(normalise_document(url), set()).add(url)
    for url in URL_RE.findall(case['staged']):
        url = url.rstrip('.,;)]')
        key = normalise_document(url)
        if key in registry_urls and any(other != url for other in registry_urls[key]):
            found.add('url_form_variant')
    return found


# --------------------------------------------------------------------------------------------
# case builders: twelve shapes, each one deterministic about the class it exists to cover
# --------------------------------------------------------------------------------------------
def prose_row(sid, indent=0):
    """A source cell that carries no document at all (a short prose note)."""
    return row(sid, 'nothing here', indent)


def ids(rnd, lo, hi, count, exclude=()):
    blocked = set(exclude)
    pool = [value for value in range(lo, hi + 1) if value not in blocked]
    return sorted(rnd.sample(pool, min(count, len(pool))))


class Cycle:
    """Deterministic round-robin over a recipe's shapes, so every shape is exercised.

    A plain random.choice lets one shape drift out of a 30-case block; the distribution
    of *shapes* is part of what the generator promises, so it is scheduled, not sampled.
    """

    def __init__(self, values):
        self.values = tuple(values)
        self.index = 0

    def __call__(self, rnd):
        value = self.values[self.index % len(self.values)]
        self.index += 1
        rnd.random()                    # keep the stream seed-dependent at this point
        return value


def row(sid, source, indent=0, cells=None):
    body = cells if cells is not None else [sid, source, 'docs', 'A', 'scope', 'anchor',
                                            'teaches', 'queued', '2026-10-24', '180d', '-']
    return ' ' * indent + '| ' + ' | '.join(body) + ' |\n'


def doc_row(sid, document, indent=0):
    return row(sid, 'Src %s %s %s' % (sid, '\u2014', document), indent)


def doc_forms(rnd, seed):
    base = 'doc%d.test/paper' % seed
    forms = ['https://' + base, 'https://' + base + '/', 'https://www.' + base,
             'http://' + base + '/', 'https://' + base.upper()]
    return rnd.sample(forms, 2)


def rec_no_collision(rnd):
    registry_ids = ids(rnd, 1, 40, rnd.randint(1, 4))
    staged_ids = ids(rnd, 41, 90, rnd.randint(1, 4))
    registry = HEAD + ''.join(doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n,
                                      rnd.randint(0, 3)) for n in registry_ids)
    staged = HEAD + ''.join(doc_row('S%03d' % n, 'https://stg%d.test/doc/' % n,
                                    rnd.randint(0, 3)) for n in staged_ids)
    return {'registry': registry, 'staged': staged, 'map': None}


def rec_collision(rnd):
    registry_ids = ids(rnd, 1, 40, rnd.randint(1, 4))
    top = registry_ids[-1]
    collide = rnd.choice(registry_ids)
    extra = ids(rnd, 1, top, rnd.randint(0, 3), exclude=registry_ids)
    registry = HEAD + ''.join(doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n,
                                     rnd.randint(0, 3)) for n in registry_ids)
    rows = [doc_row('S%03d' % collide, 'https://staged%d.test/doc/' % collide,
                    rnd.randint(0, 3))]
    rows += [doc_row('S%03d' % n, 'https://staged%d.test/doc/' % n, rnd.randint(0, 3))
             for n in extra]
    return {'registry': registry, 'staged': HEAD + ''.join(rows), 'map': None}


def rec_indent_1_3(rnd):
    registry_ids = ids(rnd, 1, 40, rnd.randint(1, 3))
    collide = rnd.choice(registry_ids)
    rows = []
    for n in registry_ids:
        indent = rnd.randint(1, 3) if n == collide else rnd.randint(0, 3)
        rows.append(doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n, indent))
    staged = HEAD + doc_row('S%03d' % collide, 'https://moved%d.test/doc/' % collide,
                            rnd.randint(0, 3))
    return {'registry': HEAD + ''.join(rows), 'staged': staged, 'map': None}


def rec_indent_4_plus(rnd):
    registry_ids = ids(rnd, 1, 30, rnd.randint(1, 3))
    deep = ids(rnd, 1, 30, 1, exclude=registry_ids)
    registry = HEAD + ''.join(doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n,
                                      rnd.randint(0, 3)) for n in registry_ids)
    if deep and rnd.random() < 0.5:
        registry += doc_row('S%03d' % deep[0], 'https://deep%d.test/doc/' % deep[0],
                            rnd.randint(4, 6))
    staged = HEAD
    if deep:
        staged += doc_row('S%03d' % deep[0], 'https://pack%d.test/doc/' % deep[0],
                          rnd.randint(4, 6))
    for n in ids(rnd, 1, 30, rnd.randint(0, 2), exclude=registry_ids + deep):
        staged += doc_row('S%03d' % n, 'https://pack%d.test/doc/' % n, rnd.randint(0, 3))
    return {'registry': registry, 'staged': staged, 'map': None}


def rec_id_4_plus_digits(rnd):
    digits = rnd.randint(4, 6)
    number = rnd.randrange(10 ** (digits - 1), 10 ** digits)
    sid = 'S%d' % number
    others = ids(rnd, 1, 20, rnd.randint(0, 2))
    registry = HEAD + doc_row(sid, 'https://wide%d.test/doc/' % number, rnd.randint(0, 3))
    registry += ''.join(doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n) for n in others)
    staged = HEAD + doc_row(sid, 'https://wide-moved%d.test/doc/' % number, rnd.randint(0, 3))
    return {'registry': registry, 'staged': staged, 'map': None}


def rec_refusal(rnd):
    """Setup refusal: a row that is an id but not a row, or the same id twice."""
    kind = REFUSAL_KINDS(rnd)
    registry_ids = ids(rnd, 1, 10, rnd.randint(1, 2))
    sid = 'S%03d' % ids(rnd, 1, 20, 1)[0]
    registry = HEAD + ''.join(doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n)
                              for n in registry_ids)
    staged = HEAD + ''.join(doc_row('S%03d' % n, 'https://pack%d.test/doc/' % n)
                            for n in ids(rnd, 1, 10, 1, exclude=registry_ids))
    if kind == 'staged_short4':
        staged += '  | %s | x | y | z |\n' % sid
    elif kind == 'staged_short2':
        staged += '| %s | x |\n' % sid
    elif kind == 'registry_short4':
        registry += ' | %s | x | y | z |\n' % sid
    elif kind == 'dup_staged':
        staged += doc_row(sid, 'https://dup%d.test/a' % ids(rnd, 1, 99, 1)[0])
        staged += doc_row(sid, 'https://dup%d.test/b' % ids(rnd, 1, 99, 1)[0])
    else:
        registry += doc_row(sid, 'https://dup%d.test/a' % ids(rnd, 1, 99, 1)[0])
        registry += doc_row(sid, 'https://dup%d.test/b' % ids(rnd, 1, 99, 1)[0])
    return {'registry': registry, 'staged': staged, 'map': None}


NON_DOCUMENTS = {
    # documented in document_key: no URL/DOI, and the head is not openable
    'prose': 'nothing here',              # a space, no slash: prose is not a document
    'short_head': 'a/b.md',               # openable but 6 characters: len(head) > 8 fails
    'no_slash_no_dot': 'plainword',       # no slash and no dot-suffix
    'long_extension': 'example.testlongextension',   # suffix longer than 6 characters
    'short_word': 'ref',                  # prose, too short to be anything
}


def rec_unmapped(rnd):
    registry_ids = ids(rnd, 1, 30, rnd.randint(1, 3))
    top = registry_ids[-1]
    collide = rnd.choice(registry_ids)
    source = NON_DOCUMENTS[UNMAPPED_KINDS(rnd)]
    registry = HEAD + ''.join(doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n)
                              for n in registry_ids)
    rows = [row('S%03d' % collide, source, rnd.randint(0, 3))]
    rows += [row('S%03d' % n, 'nothing here', rnd.randint(0, 3))
             for n in ids(rnd, 1, top, rnd.randint(0, 2), exclude=registry_ids)]
    return {'registry': registry, 'staged': HEAD + ''.join(rows), 'map': None}


def rec_held(rnd):
    registry_ids = ids(rnd, 1, 30, rnd.randint(1, 3))
    top = registry_ids[-1]
    collide = rnd.choice(registry_ids)
    kind = HELD_KINDS(rnd)
    stem = 'doc%d.test/paper' % collide
    if kind == 'url_pair':
        # scheme / www. / trailing slash / case: two URL forms of one document
        first, second = doc_forms(rnd, collide)
        own = doc_row('S%03d' % collide, first, rnd.randint(0, 3))
        staged_row = doc_row('S%03d' % collide, second, rnd.randint(0, 3))
    elif kind == 'scheme_less_staged':
        # the registry row carries the URL, the staged row only the bare host/path:
        # this is the scheme-stripping rule and nothing else
        own = doc_row('S%03d' % collide, 'https://' + stem, rnd.randint(0, 3))
        staged_row = row('S%03d' % collide, stem + ' \u2014 note', rnd.randint(0, 3))
    else:
        # the reverse: a bare head in the registry, a URL in the staged package
        own = row('S%03d' % collide, stem + ' \u2014 note', rnd.randint(0, 3))
        staged_row = doc_row('S%03d' % collide, 'https://' + stem + '/', rnd.randint(0, 3))
    registry = HEAD + ''.join(
        own if n == collide else doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n,
                                         rnd.randint(0, 3)) for n in registry_ids)
    staged = HEAD + staged_row
    if rnd.random() < 0.34:                     # the naive renumber then lands on a staged id
        staged += doc_row('S%03d' % (top + 1), 'https://bump%d.test/doc/' % (top + 1))
    return {'registry': registry, 'staged': staged, 'map': None}


def rec_cascade(rnd):
    registry_ids = ids(rnd, 1, 25, rnd.randint(1, 3))
    top = registry_ids[-1]
    collide = rnd.choice(registry_ids)
    registry = HEAD + ''.join(doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n)
                              for n in registry_ids)
    staged = HEAD + doc_row('S%03d' % collide, 'https://moved%d.test/doc/' % collide)
    staged += doc_row('S%03d' % (top + 1), 'https://take%d.test/doc/' % (top + 1))
    return {'registry': registry, 'staged': staged, 'map': None}


def rec_map_admissible(rnd):
    kind = ADMISSIBLE_KINDS(rnd)
    if kind == 'held':
        registry_ids = ids(rnd, 1, 20, rnd.randint(2, 4))
        holder, collide = registry_ids[0], registry_ids[-1]
        first, second = doc_forms(rnd, holder)
        registry = HEAD + ''.join(
            doc_row('S%03d' % n, first if n == holder else 'https://reg%d.test/doc/' % n)
            for n in registry_ids)
        staged = HEAD + doc_row('S%03d' % collide, second)
        if rnd.random() < 0.34:       # analysis refused, map still admissible
            staged += doc_row('S%03d' % (registry_ids[-1] + 1),
                              'https://bump%d.test/doc/' % (registry_ids[-1] + 1))
        mapping = {('S%03d' % collide): 'S%03d' % holder}
        if rnd.random() < 0.5:
            mapping = {'staged:' + key: value for key, value in mapping.items()}
        return {'registry': registry, 'staged': staged, 'map': {'map': mapping}}
    registry_ids = ids(rnd, 1, 20, rnd.randint(1, 3))
    top = registry_ids[-1]
    collide = rnd.choice(registry_ids)
    registry = HEAD + ''.join(doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n)
                              for n in registry_ids)
    staged = HEAD + doc_row('S%03d' % collide, 'https://moved%d.test/doc/' % collide)
    target = top + 1 if kind == 'boundary' else top + 1 + rnd.randint(0, 5)
    key = 'S%03d' % collide
    if kind == 'prefixed':
        key = 'staged:' + key
    return {'registry': registry, 'staged': staged, 'map': {'map': {key: 'S%03d' % target}}}


def rec_map_inadmissible(rnd):
    kind = INADMISSIBLE_KINDS(rnd)
    if kind == 'registry_clash':
        registry_ids = ids(rnd, 1, 20, 3)
        collide, other = registry_ids[-1], registry_ids[0]
        registry = HEAD + ''.join(
            doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n) for n in registry_ids)
        staged = HEAD + doc_row('S%03d' % collide, 'https://moved%d.test/doc/' % collide)
        return {'registry': registry, 'staged': staged,
                'map': {'map': {'S%03d' % collide: 'S%03d' % other}}}
    if kind == 'below_floor':
        registry_ids = ids(rnd, 1, 5, 2)
        top = registry_ids[-1]
        collide = registry_ids[-1]
        registry = HEAD + ''.join(doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n)
                                  for n in registry_ids)
        staged = HEAD + doc_row('S%03d' % collide, 'https://moved%d.test/doc/' % collide)
        staged += doc_row('S%03d' % 9, 'https://high.test/doc/')
        return {'registry': registry, 'staged': staged,
                'map': {'map': {'S%03d' % collide: 'S%03d' % (top + 1)}}}
    if kind == 'staged_target':
        registry_ids = ids(rnd, 1, 10, 2)
        top = registry_ids[-1]
        collide = registry_ids[-1]
        registry = HEAD + ''.join(doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n)
                                  for n in registry_ids)
        staged = HEAD + doc_row('S%03d' % collide, 'https://moved%d.test/doc/' % collide)
        staged += doc_row('S%03d' % (top + 2), 'https://keep%d.test/doc/' % (top + 2))
        return {'registry': registry, 'staged': staged,
                'map': {'map': {'S%03d' % collide: 'S%03d' % (top + 2)}}}
    if kind == 'uncovered':
        registry_ids = ids(rnd, 1, 10, 2)
        top = registry_ids[-1]
        registry = HEAD + ''.join(doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n)
                                  for n in registry_ids)
        staged = HEAD + ''.join(doc_row('S%03d' % n, 'https://moved%d.test/doc/' % n)
                                for n in registry_ids)
        return {'registry': registry, 'staged': staged,
                'map': {'map': {'S%03d' % registry_ids[0]: 'S%03d' % (top + 2)}}}
    if kind == 'selfmap':
        registry_ids = ids(rnd, 1, 10, 2)
        holder, collide = registry_ids[0], registry_ids[-1]
        first, second = doc_forms(rnd, holder)
        registry = HEAD + ''.join(
            doc_row('S%03d' % n, first if n == holder else 'https://reg%d.test/doc/' % n)
            for n in registry_ids)
        staged = HEAD + doc_row('S%03d' % collide, second)
        return {'registry': registry, 'staged': staged,
                'map': {'map': {'S%03d' % collide: 'S%03d' % collide}}}
    if kind == 'undocumented':
        registry_ids = ids(rnd, 1, 10, 1)
        collide = registry_ids[0]
        registry = HEAD + doc_row('S%03d' % collide, 'https://reg%d.test/doc/' % collide)
        staged = HEAD + prose_row('S%03d' % collide)
        return {'registry': registry, 'staged': staged,
                'map': {'map': {'S%03d' % collide: 'S050'}}}
    if kind == 'held_moved':
        registry_ids = ids(rnd, 1, 20, 2)
        holder, collide = registry_ids[0], registry_ids[-1]
        first, second = doc_forms(rnd, holder)
        registry = HEAD + ''.join(
            doc_row('S%03d' % n, first if n == holder else 'https://reg%d.test/doc/' % n)
            for n in registry_ids)
        staged = HEAD + doc_row('S%03d' % collide, second)
        return {'registry': registry, 'staged': staged,
                'map': {'map': {'S%03d' % collide: 'S050'}}}
    if kind == 'non_injective':
        registry_ids = ids(rnd, 1, 10, 2)
        top = registry_ids[-1]
        registry = HEAD + ''.join(doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n)
                                  for n in registry_ids)
        staged = HEAD + ''.join(doc_row('S%03d' % n, 'https://moved%d.test/doc/' % n)
                                for n in registry_ids)
        target = 'S%03d' % (top + 1)
        return {'registry': registry, 'staged': staged,
                'map': {'map': {'S%03d' % registry_ids[0]: target,
                                'S%03d' % registry_ids[1]: target}}}
    registry_ids = ids(rnd, 1, 10, 1)
    top = registry_ids[-1]
    collide = registry_ids[0]
    registry = HEAD + doc_row('S%03d' % collide, 'https://reg%d.test/doc/' % collide)
    staged = HEAD + doc_row('S%03d' % collide, 'https://moved%d.test/doc/' % collide)
    return {'registry': registry, 'staged': staged,
            'map': {'map': {'S%03d' % collide: 'S%03d' % (top + 1), 'S999': 'S%03d' % (top + 2)}}}


def rec_path_document(rnd):
    """The document is a path-like source head, not a URL (document_key's other branch).

    document_key reads the part of the source cell *before* the first spaced dash as the
    head, so a path document must start the cell: 'notes/paper-3.md — note'.
    """
    registry_ids = ids(rnd, 1, 30, rnd.randint(2, 4))
    holder, collide = registry_ids[0], registry_ids[-1]
    kind = DOCUMENT_KINDS(rnd)
    if kind == 'path_dot':
        stem = 'notes/paper-%d.md' % rnd.randint(1, 999)
        variants = [stem.upper(), stem + '/', stem.replace('paper', 'Paper')]
    elif kind == 'path_no_dot':
        stem = 'notes/paper/%d' % rnd.randint(1, 999)   # openable by the slash alone
        variants = [stem.upper(), stem + '/']
    else:
        stem = 'paper%d.example.test' % rnd.randint(1, 99)   # openable by the dot alone
        variants = [stem.upper(), stem + '/']
    document = stem
    registry = HEAD + ''.join(
        row('S%03d' % n, document if n == holder else 'https://reg%d.test/doc/' % n,
            rnd.randint(0, 3)) for n in registry_ids)
    variant = rnd.choice(variants)
    if rnd.random() < 0.5:
        variant += ' \u2014 note'
    staged = HEAD + row('S%03d' % collide, variant, rnd.randint(0, 3))
    map_doc = None
    if rnd.random() < 0.5:
        map_doc = {'map': {'S%03d' % collide: 'S%03d' % holder}}
    return {'registry': registry, 'staged': staged, 'map': map_doc}


def rec_map_setup_refusal(rnd):
    registry_ids = ids(rnd, 1, 10, rnd.randint(1, 2))
    collide = registry_ids[-1]
    registry = HEAD + ''.join(doc_row('S%03d' % n, 'https://reg%d.test/doc/' % n)
                              for n in registry_ids)
    staged = HEAD + doc_row('S%03d' % collide, 'https://moved%d.test/doc/' % collide)
    key = 'S%03d' % collide
    bad = [[], {}, {'nope': {}}, {'map': {key: 7}}, {'map': {'gamma': 'S050'}},
           {'map': {key: ['S050']}}, {'map': {'staged:' + key: None}}]
    return {'registry': registry, 'staged': staged, 'map': bad[SETUP_MAP_KINDS(rnd)]}


REFUSAL_KINDS = Cycle(['staged_short4', 'staged_short2', 'registry_short4', 'dup_staged',
                       'dup_registry'])
ADMISSIBLE_KINDS = Cycle(['held', 'fresh', 'boundary', 'prefixed'])
INADMISSIBLE_KINDS = Cycle(['registry_clash', 'below_floor', 'staged_target', 'uncovered',
                            'selfmap', 'undocumented', 'held_moved', 'non_injective',
                            'stranger_row'])
DOCUMENT_KINDS = Cycle(['path_dot', 'path_no_dot', 'host'])
HELD_KINDS = Cycle(['url_pair', 'url_pair', 'scheme_less_staged', 'scheme_less_registry'])
UNMAPPED_KINDS = Cycle(['prose', 'short_head', 'no_slash_no_dot', 'long_extension',
                        'short_word'])
SETUP_MAP_KINDS = Cycle(range(7))

RECIPES = (rec_no_collision, rec_collision, rec_indent_1_3, rec_indent_4_plus,
           rec_id_4_plus_digits, rec_refusal, rec_unmapped, rec_held, rec_cascade,
           rec_map_admissible, rec_map_inadmissible, rec_path_document,
           rec_map_setup_refusal)


# --------------------------------------------------------------------------------------------
# the run: seed -> cases -> guard CLI -> oracle
# --------------------------------------------------------------------------------------------
def write_text(path, text):
    with open(path, 'w', encoding='utf-8', newline='') as handle:
        handle.write(text)


def run_guard(guard, case_dir, case):
    registry_path = os.path.join(case_dir, 'registry.md')
    staged_path = os.path.join(case_dir, 'staged.md')
    map_path = os.path.join(case_dir, 'map.json')
    write_text(registry_path, case['registry'])
    write_text(staged_path, case['staged'])
    argv = [sys.executable, '-I', guard, '--registry', registry_path,
            '--staged', staged_path]
    if case['map'] is None:
        if os.path.exists(map_path):
            os.unlink(map_path)
    else:
        write_text(map_path, json.dumps(case['map']))
        argv += ['--map', map_path]
    argv.append('--json')
    try:
        proc = subprocess.run(argv, capture_output=True, timeout=GUARD_TIMEOUT, cwd=case_dir)
    except subprocess.TimeoutExpired:
        return {'exit': 124, 'json': None, 'stdout': b'', 'stderr': b'timeout'}
    try:
        answer = json.loads(proc.stdout.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        answer = None
    return {'exit': proc.returncode, 'json': answer, 'stdout': proc.stdout,
            'stderr': proc.stderr}


def run(guard, seed, cases, dump_path):
    started = time.monotonic()
    rnd = random.Random(seed)
    order = list(range(len(RECIPES)))
    rnd.shuffle(order)
    counts = {name: 0 for name in CLASSES}
    work = tempfile.mkdtemp(prefix='pbt-staged-id-')
    case_dir = os.path.join(work, 'case')
    os.makedirs(case_dir, exist_ok=True)
    run_count = 0
    violation = None
    try:
        dump = open(dump_path, 'w', encoding='utf-8')
    except OSError as exc:
        shutil.rmtree(work, ignore_errors=True)
        print('pbt-staged-id: cannot write dump %s: %s' % (dump_path, exc), file=sys.stderr)
        return 2
    try:
        for index in range(cases):
            case = RECIPES[order[index % len(order)]](rnd)
            dump.write(json.dumps({'index': index, 'registry': case['registry'],
                                   'staged': case['staged'], 'map': case['map']},
                                  sort_keys=True) + '\n')
            dump.flush()
            observed = run_guard(guard, case_dir, case)
            run_count += 1
            for name in case_classes(case, observed['exit'], observed['json']):
                counts[name] += 1
            why = check(case, observed)
            if why is not None:
                violation = (index, why, observed)
                break
    finally:
        dump.close()
        shutil.rmtree(work, ignore_errors=True)
    if violation is not None:
        index, why, observed = violation
        print('VIOLATION index=%d %s' % (index, why))
        print('VIOLATION observed_exit=%s stdout=%s stderr=%s'
              % (observed['exit'],
                 observed['stdout'][:400].decode('utf-8', 'replace').replace('\n', ' '),
                 observed['stderr'][:200].decode('utf-8', 'replace').replace('\n', ' ')))
    for name in CLASSES:
        print('CLASS %s=%d%s' % (name, counts[name],
                                 '' if counts[name] >= CLASS_MIN else ' SHORT'))
    print('PBT_STAGED_ID_TIME: seconds=%.2f' % (time.monotonic() - started))
    print('PBT_STAGED_ID: cases=%d violations=%d counterexample=%s classes=%s'
          % (run_count, 0 if violation is None else 1,
             'none' if violation is None else violation[0],
             ','.join('%s=%d' % (name, counts[name]) for name in CLASSES)))
    return 0 if violation is None else 1


def _setup_error(message):
    print('pbt-staged-id: %s' % message, file=sys.stderr)
    return 2


# --------------------------------------------------------------------------------------------
# selftest: the oracle and the classifier, without the guard (no subprocess)
# --------------------------------------------------------------------------------------------
def selftest():
    cases = []

    def case(name, ok):
        cases.append((name, bool(ok)))
        print('CASE %s %s' % (name, 'PASS' if ok else 'FAIL'))

    def shape(registry, staged, map_doc=None):
        return {'registry': HEAD + registry, 'staged': HEAD + staged, 'map': map_doc}

    def doc(sid, url, indent=0):
        return doc_row(sid, url, indent)

    case('collision-counted', oracle_case(shape(doc('S002', 'https://a.test/x'),
                                                doc('S002', 'https://b.test/x')))[0] == 0
         and oracle_case(shape(doc('S002', 'https://a.test/x'),
                               doc('S002', 'https://b.test/x')))[1]['collisions'] == ['S002'])
    case('indented-collision-counted',
         oracle_case(shape(doc('S002', 'https://a.test/x'),
                           doc('S002', 'https://b.test/x', 2)))[1]['collisions'] == ['S002'])
    case('four-space-row-is-not-a-row',
         oracle_case(shape(doc('S002', 'https://a.test/x'),
                           doc('S002', 'https://b.test/x', 4)))[1]['collisions'] == [])
    case('column0-miss-recorded',
         oracle_case(shape(doc('S002', 'https://a.test/x'),
                           doc('S002', 'https://b.test/x', 3)))[1]['column0_miss'] == ['S002'])
    case('short-row-refused',
         oracle_case(shape(doc('S001', 'https://a.test/x'), '| S002 | x | y | z |\n'))[0] == 2)
    case('duplicate-id-refused',
         oracle_case(shape(doc('S001', 'https://a.test/x') + doc('S001', 'https://b.test/y'),
                           doc('S003', 'https://c.test/z')))[0] == 2)
    case('numeric-sort',
         oracle_case(shape(doc('S999', 'https://a.test/x') + doc('S1000', 'https://b.test/y'),
                           doc('S1000', 'https://c.test/z') + doc('S999', 'https://d.test/w'))
                     )[1]['collisions'] == ['S999', 'S1000'])
    empty = oracle_case(shape('', ''))
    case('empty-table-floor',
         empty[0] == 0 and empty[1]['next_free'] == 'S001' and empty[1]['safe_floor'] == 'S001'
         and empty[1]['registry_max'] == 'S000' and empty[1]['collisions'] == [])
    held = oracle_case(shape(doc('S002', 'https://www.Doc.test/paper/'),
                             doc('S002', 'https://doc.test/paper')))
    case('held-form-insensitive',
         held[1]['held'] == {'S002': 'S002'}
         and 'url_form_variant' in case_classes(shape(doc('S002', 'https://www.Doc.test/paper/'),
                                                      doc('S002', 'https://doc.test/paper')),
                                                held[0], held[1]))
    unmapped = oracle_case(shape(doc('S002', 'https://a.test/x'), prose_row('S002')))
    case('unmapped-refused',
         unmapped[0] == 1 and unmapped[1]['unmapped'] == ['S002'] and unmapped[1]['refused'])
    cascade = oracle_case(shape(doc('S002', 'https://a.test/x') + doc('S004', 'https://b.test/y'),
                                doc('S002', 'https://c.test/z') + doc('S005', 'https://d.test/w')))
    case('naive-cascade-detected',
         cascade[1]['naive_map'] == {'S002': 'S005'} and cascade[1]['cascade'] == ['S005']
         and cascade[0] == 1)
    admissible = oracle_case(shape(doc('S002', 'https://a.test/x'), doc('S002', 'https://b.test/x'),
                                   {'map': {'S002': 'S010'}}))
    case('map-admissible', admissible[0] == 0 and admissible[1]['verdict'] == 'admitted'
         and admissible[1]['map_ok'])
    case('map-prefixed-key-admitted',
         oracle_case(shape(doc('S002', 'https://a.test/x'), doc('S002', 'https://b.test/x'),
                           {'map': {'staged:S002': 'S010'}}))[0] == 0)
    case('map-onto-registry-refused',
         oracle_case(shape(doc('S002', 'https://a.test/x') + doc('S003', 'https://b.test/y'),
                           doc('S002', 'https://c.test/z'), {'map': {'S002': 'S003'}}))[1]
         ['map_reasons'] == [('registry', ('S003',))])
    case('map-onto-staged-refused',
         oracle_case(shape(doc('S002', 'https://a.test/x'), doc('S002', 'https://b.test/x')
                           + doc('S004', 'https://c.test/y'), {'map': {'S002': 'S004'}}))[1]
         ['map_reasons'] == [('staged', ('S004',))])
    case('map-below-floor-refused',
         oracle_case(shape(doc('S005', 'https://a.test/x'), doc('S005', 'https://b.test/x')
                           + doc('S009', 'https://c.test/y'), {'map': {'S005': 'S006'}}))[1]
         ['map_reasons'] == [('floor', ('S006',))])
    case('map-uncovered-refused',
         oracle_case(shape(doc('S002', 'https://a.test/x') + doc('S003', 'https://b.test/y'),
                           doc('S002', 'https://c.test/z') + doc('S003', 'https://d.test/w'),
                           {'map': {'S002': 'S010'}}))[1]['map_reasons'] == [('cover', ('S003',))])
    case('map-selfmap-refused',
         oracle_case(shape(doc('S002', 'https://doc.test/paper'),
                           doc('S002', 'https://www.doc.test/paper/'),
                           {'map': {'S002': 'S002'}}))[1]['map_reasons'] == [('self', ('S002',))])
    case('map-undocumented-refused',
         oracle_case(shape(doc('S002', 'https://a.test/x'), prose_row('S002'),
                           {'map': {'S002': 'S010'}}))[1]['map_reasons'] == [('undocumented', ('S002',))])
    case('map-held-moved-refused',
         oracle_case(shape(doc('S002', 'https://doc.test/paper') + doc('S003', 'https://b.test/y'),
                           doc('S003', 'https://doc.test/paper/'),
                           {'map': {'S003': 'S010'}}))[1]['map_reasons'] == [('held', ('S003',))])
    case('map-non-injective-refused',
         oracle_case(shape(doc('S002', 'https://a.test/x') + doc('S003', 'https://b.test/y'),
                           doc('S002', 'https://c.test/z') + doc('S003', 'https://d.test/w'),
                           {'map': {'S002': 'S010', 'S003': 'S010'}}))[1]['map_reasons']
         == [('injective',)])
    case('map-stranger-row-refused',
         oracle_case(shape(doc('S002', 'https://a.test/x'), doc('S002', 'https://b.test/x'),
                           {'map': {'S002': 'S010', 'S999': 'S011'}}))[1]['map_reasons']
         == [('carry', 'S999')])
    for name, bad in (('no-map-object', {}), ('target-int', {'map': {'S002': 7}}),
                      ('bad-key', {'map': {'gamma': 'S010'}}),
                      ('target-list', {'map': {'S002': ['S010']}})):
        case('map-%s-refused' % name,
             oracle_case(shape(doc('S002', 'https://a.test/x'), doc('S002', 'https://b.test/x'),
                               bad))[0] == 2)
    case('class-indent-and-digits',
         case_classes(shape(doc('S1234', 'https://a.test/x', 1), ''), 0,
                      {'collision_count': 0})
         == {'indent_1_3', 'id_4_plus_digits', 'no_collision'})
    case('class-map-exit2',
         case_classes(shape('', '', {}), 2, None) == {'map', 'refusal'})
    case('class-map-inadmissible',
         case_classes(shape('', '', {'map': {}}), 1, None) == {'map', 'map_inadmissible'})
    case('check-detects-field-drift',
         check(shape(doc('S002', 'https://a.test/x'), doc('S002', 'https://b.test/x')),
               {'exit': 0, 'json': {'verdict': 'answered', 'collision_count': 0},
                'stdout': b'', 'stderr': b''}) is not None)
    case('check-detects-exit-drift',
         check(shape(doc('S002', 'https://a.test/x'), doc('S002', 'https://b.test/x')),
               {'exit': 1, 'json': {}, 'stdout': b'', 'stderr': b''}) is not None)
    failed = sum(1 for _, ok in cases if not ok)
    print('PBT_STAGED_ID_SELFTEST: cases=%d failed=%d' % (len(cases), failed))
    return 0 if failed == 0 else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--guard')
    parser.add_argument('--seed', type=int)
    parser.add_argument('--cases', type=int)
    parser.add_argument('--dump')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.guard and args.dump) or args.seed is None or args.cases is None:
        return _setup_error('--guard, --seed, --cases and --dump are required')
    if args.cases < 1:
        return _setup_error('--cases must be at least 1')
    guard = os.path.abspath(args.guard)
    if not os.path.isfile(guard):
        return _setup_error('guard is not a regular file: %s' % guard)
    return run(guard, args.seed, args.cases, os.path.abspath(args.dump))


if __name__ == '__main__':
    sys.exit(main())
