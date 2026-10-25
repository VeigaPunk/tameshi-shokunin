#!/usr/bin/env python3
"""Pre-adoption id guard for a staged SOURCES registry package.

CORPUS.md makes the registry append-only and keyed by an id that is never
reused, and it accepts registry rows with 0-3 leading spaces. A staged
package built elsewhere keeps its own ids, so a package whose id range
overlaps the lane's registry cannot be appended as-is: the adopted row needs a
different id, and the citation must be re-pointed **by document** — the URL or
DOI is the evidence and the id follows it, never arithmetic.

This tool answers that question before anything is appended:

  * `collisions`   — ids present in both the registry and the staged package,
                     extracted with the census-valid 0-3-space pattern (the
                     column-zero pattern misses an indented row, which is how a
                     collision false-greens);
  * `unmapped`     — colliding staged rows whose row carries no document key
                     (no URL/DOI and an empty source cell): refused, because a
                     renumber decision that is not tied to a document is
                     arithmetic;
  * `held`         — colliding staged rows whose document the registry already
                     carries: dedupe to the registry id, do not append;
  * `naive_map`    — the obvious fix, every colliding id moved to
                     `max(registry)+1, +2, …`, and why it is refused: those
                     target ids are themselves staged ids, so the map is not
                     injective against the staged set (the cascade);
  * `--map FILE`   — validate a candidate map (JSON
                     `{"map": {"staged:S001": "S161", …}, "staged": path,
                     "registry": path}`): injective, disjoint from the
                     registry, and covering every collision.

Exit 0 = the question was answered and, with `--map`, the map is admissible;
exit 1 = the map is not admissible (or a collision has no document);
exit 2 = setup refusal (missing file, malformed row, bad map file);
exit 0 for `--selftest` only when every case passes.

Interface is frozen for the round-43 counter:

  python3 -I tools/staged-id-guard.py --registry F --staged G --json
  python3 -I tools/staged-id-guard.py --registry F --staged G --map M --json
  python3 -I tools/staged-id-guard.py --selftest

`--json` prints one object: collisions (list), collision_count, unmapped,
held, naive_map, cascade, cascade_count, refused, next_free, registry_rows,
staged_rows, extractor ("0-3space"), column0_extract (for the indented-row
proof), verdict ("refused"|"answered"|"admitted"|"inadmissible").
"""
import argparse
import json
import os
import re
import sys

ROW_RE = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
COLUMN0_RE = re.compile(r'^\|\s*(S\d{3,})\s*\|')
URL_RE = re.compile(r'https?://[^\s|,;]+')
HEXISH = re.compile(r'[0-9a-f]{7,40}')


class Refusal(Exception):
    """Setup refusal: the question cannot be answered from these bytes."""


def parse_rows(text, label):
    """Return {id: {"document": str, "cells": int, "lineno": int}}."""
    rows = {}
    for lineno, line in enumerate(text.splitlines(), 1):
        match = ROW_RE.match(line)
        if not match:
            continue
        sid = match.group(1)
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        if len(cells) < 5:
            raise Refusal('%s:%d malformed row %s (%d cells)'
                          % (label, lineno, sid, len(cells)))
        if sid in rows:
            raise Refusal('%s:%d duplicate id %s' % (label, lineno, sid))
        rows[sid] = {
            'document': document_key(cells),
            'cells': len(cells),
            'lineno': lineno,
        }
    return rows


def document_key(cells):
    """The row's document: its URL/DOI, else a path-like source head."""
    blob = ' '.join(cells[1:6])
    found = URL_RE.search(blob)
    if found:
        return found.group(0).rstrip('.,;)]')
    source = cells[1] if len(cells) > 1 else ''
    head = re.split(r'\s+[—–]\s+', source)[0].strip()
    head = HEXISH.sub('', head).strip()
    # A document key names something openable (a path, a host, a file). Prose
    # without a slash or dot is not a document, and a renumber decision tied to
    # prose would be arithmetic.
    return head if len(head) > 8 and re.search(r'[/.]', head) else ''


def id_number(sid):
    return int(sid[1:])


def analyse(registry_text, staged_text):
    registry = parse_rows(registry_text, 'registry')
    staged = parse_rows(staged_text, 'staged')
    collisions = sorted(set(registry) & set(staged), key=id_number)
    column0 = sorted({m.group(1) for m in
                      (COLUMN0_RE.match(line) for line in staged_text.splitlines()) if m},
                     key=id_number)
    held, unmapped = {}, []
    registry_docs = {}
    for sid, row in registry.items():
        if row['document']:
            registry_docs.setdefault(row['document'], sid)
    for sid in collisions:
        key = staged[sid]['document']
        if not key:
            unmapped.append(sid)
        elif key in registry_docs:
            held[sid] = registry_docs[key]
    top = max((id_number(sid) for sid in registry), default=0)
    staged_top = max((id_number(sid) for sid in staged), default=0)
    naive = {}
    for index, sid in enumerate(collisions, 1):
        naive[sid] = 'S%03d' % (top + index)
    cascade = sorted((target for target in naive.values() if target in staged),
                     key=id_number)
    refused = bool(unmapped) or bool(cascade)
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
        'refused': refused,
        'next_free': 'S%03d' % (top + 1),
        'registry_max': 'S%03d' % top,
        'staged_max': 'S%03d' % staged_top,
        'safe_floor': 'S%03d' % (max(top, staged_top) + 1),
        'extractor': '0-3space',
        'column0_collisions': [sid for sid in collisions if sid in column0],
        'column0_miss': [sid for sid in collisions if sid not in column0],
        'registry_docs': len(registry_docs),
    }


def validate_map(registry_text, staged_text, map_doc):
    """Return (ok, reasons, fields) for a candidate adoption map.

    Each entry is judged by document:
      * a target that is a registry id is admissible only when the staged row's
        document is the document of that registry row (dedupe: adopt nothing);
      * any other target must be a fresh id — above the safe floor for a partial
        map, and never an id another staged row still holds.
    """
    base = analyse(registry_text, staged_text)
    registry = parse_rows(registry_text, 'registry')
    staged = parse_rows(staged_text, 'staged')
    mapping = map_doc.get('map') if isinstance(map_doc, dict) else None
    reasons = []
    if not isinstance(mapping, dict):
        raise Refusal('map file carries no "map" object')
    targets = list(mapping.values())
    if len(targets) != len(set(targets)):
        reasons.append('map is not injective (two staged rows share a target)')
    # Per-target, not over the concatenation: a multi-entry map's targets run
    # together when joined, so a whole-string fullmatch refused every map with
    # two or more entries (wave-1 mutation-tester MutC3Selftest, round 43).
    if not all(re.fullmatch(r'S\d{3,}', target) for target in targets):
        reasons.append('map has a target that is not an S-id')
    whole_set = len(mapping) == len(staged)
    floor = 'S%03d' % (max([id_number(sid) for sid in list(registry) + list(staged)] + [0]) + 1)
    clash, staged_clash, below_floor, dedupe = [], [], [], {}
    for staged_id, target in sorted(mapping.items(), key=lambda kv: id_number(kv[0])):
        if staged_id not in staged:
            reasons.append('map names a row the package does not carry: %s' % staged_id)
            continue
        if target in registry:
            if registry[target]['document'] and \
                    registry[target]['document'] == staged[staged_id]['document']:
                dedupe[staged_id] = target
            else:
                clash.append(target)
            continue
        if target in staged and not whole_set:
            staged_clash.append(target)
            continue
        if not whole_set and id_number(target) < id_number(floor):
            below_floor.append(target)
    if clash:
        reasons.append('map targets collide with registry ids: %s'
                       % ','.join(sorted(clash, key=id_number)))
    if staged_clash:
        reasons.append('map targets are still staged ids: %s'
                       % ','.join(sorted(staged_clash, key=id_number)))
    if below_floor:
        reasons.append('partial map targets are below the safe floor %s: %s'
                       % (floor, ','.join(sorted(below_floor, key=id_number))))
    uncovered = [sid for sid in base['collisions'] if sid not in mapping]
    if uncovered:
        reasons.append('map does not cover every collision: %s' % ','.join(uncovered))
    selfmap = [sid for sid in base['collisions'] if mapping.get(sid) == sid]
    if selfmap:
        reasons.append('map leaves a colliding id on itself: %s' % ','.join(selfmap))
    fields = {
        'map_entries': len(mapping),
        'map_targets': len(set(targets)),
        'map_clash': clash,
        'map_staged_clash': staged_clash,
        'map_below_floor': below_floor,
        'map_dedupe': dedupe,
        'map_uncovered': uncovered,
        'map_floor': floor,
        'map_ok': not reasons,
        'map_reasons': reasons,
    }
    return (not reasons), reasons, fields


SELFTEST_REGISTRY = '''| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S001 | Alpha docs — https://example.test/alpha | docs | A | x | y | z | mined | 2026-01-01 | 180d | — |
| S002 | Beta docs — https://example.test/beta | docs | A | x | y | z | mined | 2026-01-01 | 180d | — |
| S003 | Kappa docs — https://example.test/kappa | docs | A | x | y | z | mined | 2026-01-01 | 180d | — |
'''

# T1: the collision sits on an indented row (2 spaces) — census-valid, column-zero blind.
SELFTEST_STAGED_INDENTED = '''| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
  | S002 | Gamma docs — https://example.test/gamma | docs | A | x | y | z | queued | 2026-10-24 | 180d | — |
| S004 | Delta docs — https://example.test/delta | docs | A | x | y | z | queued | 2026-10-24 | 180d | — |
'''

# T5: a staged row whose document the registry already holds (dedupe, no append).
SELFTEST_STAGED_HELD = '''| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S002 | Alpha again — https://example.test/alpha | docs | A | x | y | z | queued | 2026-10-24 | 180d | — |
'''

# T2: a colliding row with no document at all.
SELFTEST_STAGED_UNDOCUMENTED = '''| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S002 | nothing here | docs | A | x | y | z | queued | 2026-10-24 | 180d | — |
'''

# T6: a row that carries an id but not a row's cells.
SELFTEST_STAGED_MALFORMED = '''| id | source |
|---|---|
| S002 | x |
'''


def selftest():
    cases = []

    def case(name, ok, note=''):
        cases.append((name, bool(ok), note))

    base = analyse(SELFTEST_REGISTRY, SELFTEST_STAGED_INDENTED)
    case('T1_indented_collision_seen', base['collisions'] == ['S002'],
         'collisions=%s' % base['collisions'])
    case('T1_column0_blind', base['column0_miss'] == ['S002'],
         'column0_miss=%s' % base['column0_miss'])
    case('T1_extractor_label', base['extractor'] == '0-3space', base['extractor'])
    case('T3_cascade_refused', base['refused'] and base['naive_map'] == {'S002': 'S004'}
         and base['cascade'] == ['S004'],
         'naive=%s cascade=%s' % (base['naive_map'], base['cascade']))

    held = analyse(SELFTEST_REGISTRY, SELFTEST_STAGED_HELD)
    case('T5_dedupe_to_registry_id', held['held'] == {'S002': 'S001'},
         'held=%s' % held['held'])

    undocumented = analyse(SELFTEST_REGISTRY, SELFTEST_STAGED_UNDOCUMENTED)
    case('T2_unmapped_refused', undocumented['unmapped'] == ['S002'] and undocumented['refused'],
         'unmapped=%s' % undocumented['unmapped'])

    try:
        analyse(SELFTEST_REGISTRY, SELFTEST_STAGED_MALFORMED)
        case('T6_malformed_refused', False, 'no refusal')
    except Refusal as exc:
        case('T6_malformed_refused', True, str(exc))

    good = {'map': {'S002': 'S010'}}
    ok, reasons, fields = validate_map(SELFTEST_REGISTRY, SELFTEST_STAGED_INDENTED, good)
    case('T4_valid_map_admitted', ok, 'reasons=%s' % reasons)
    bad = {'map': {'S002': 'S001'}}
    ok2, reasons2, _ = validate_map(SELFTEST_REGISTRY, SELFTEST_STAGED_INDENTED, bad)
    case('T3_map_onto_registry_refused', not ok2 and any('registry' in r for r in reasons2),
         'reasons=%s' % reasons2)
    cascade_map = {'map': {'S002': 'S004'}}
    ok5, reasons5, _ = validate_map(SELFTEST_REGISTRY, SELFTEST_STAGED_INDENTED, cascade_map)
    case('T3_map_onto_staged_refused',
         not ok5 and any('still staged' in r for r in reasons5), 'reasons=%s' % reasons5)
    partial = {'map': {}}
    ok3, reasons3, _ = validate_map(SELFTEST_REGISTRY, SELFTEST_STAGED_INDENTED, partial)
    case('T4_partial_map_refused', not ok3 and any('cover' in r for r in reasons3),
         'reasons=%s' % reasons3)
    multi_map = {'map': {'S002': 'S010', 'S004': 'S011'}}
    ok7, reasons7, _ = validate_map(SELFTEST_REGISTRY, SELFTEST_STAGED_INDENTED, multi_map)
    case('T4_multi_entry_map_admitted', ok7, 'reasons=%s' % reasons7)
    dedupe_map = {'map': {'S002': 'S001'}}
    ok6, reasons6, fields6 = validate_map(SELFTEST_REGISTRY, SELFTEST_STAGED_HELD, dedupe_map)
    case('T5_dedupe_map_admitted', ok6 and fields6['map_dedupe'] == {'S002': 'S001'},
         'reasons=%s dedupe=%s' % (reasons6, fields6['map_dedupe']))
    dup = {'map': {'S002': 'S010', 'S999': 'S010'}}
    ok4, reasons4, _ = validate_map(SELFTEST_REGISTRY, SELFTEST_STAGED_INDENTED, dup)
    case('T4_non_injective_refused', not ok4 and any('injective' in r for r in reasons4),
         'reasons=%s' % reasons4)

    failed = [row for row in cases if not row[1]]
    print('STAGED_ID_GUARD_SELFTEST: cases=%d failed=%d' % (len(cases), len(failed)))
    for name, ok, note in cases:
        if not ok:
            print('FAIL %s %s' % (name, note))
    print('VERDICT: %s' % ('PASS' if not failed else 'FAIL'))
    return 0 if not failed else 1


def read(path):
    try:
        with open(path, encoding='utf-8') as handle:
            return handle.read()
    except OSError as exc:
        raise Refusal('cannot read %s: %s' % (path, exc))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--registry')
    parser.add_argument('--staged')
    parser.add_argument('--map')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.registry or not args.staged:
        print('staged-id-guard: --registry and --staged are required', file=sys.stderr)
        return 2
    try:
        registry_text = read(args.registry)
        staged_text = read(args.staged)
        result = analyse(registry_text, staged_text)
        if args.map:
            try:
                map_doc = json.loads(read(args.map))
            except json.JSONDecodeError as exc:
                raise Refusal('map file is not JSON: %s' % exc)
            ok, reasons, fields = validate_map(registry_text, staged_text, map_doc)
            result.update(fields)
            result['verdict'] = 'admitted' if ok else 'inadmissible'
        else:
            result['verdict'] = 'refused' if result['refused'] else 'answered'
    except Refusal as exc:
        print('staged-id-guard: REFUSED: %s' % exc, file=sys.stderr)
        if args.json:
            print(json.dumps({'verdict': 'setup_refusal', 'reason': str(exc)}))
        return 2
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print('STAGED_ID_GUARD: collisions=%d unmapped=%d held=%d cascade=%d next_free=%s '
              'verdict=%s' % (result['collision_count'], len(result['unmapped']),
                              len(result['held']), result['cascade_count'],
                              result['next_free'], result['verdict']))
        for sid in result['collisions']:
            print('  collision %s naive->%s' % (sid, result['naive_map'].get(sid)))
    if result['verdict'] in ('admitted', 'answered'):
        return 0
    return 1


if __name__ == '__main__':
    sys.exit(main())
