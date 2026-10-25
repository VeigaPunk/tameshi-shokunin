#!/usr/bin/env python3
"""Build mutants.json: the declared mutant set for the round-46 C2 (operability) claim.

Each declared mutant is a single old->new text replacement on a round-45 counter. The
survivors come from the round-45 wave-1/wave-2 mutation audits (`.ufo/waves/round-45/w1/MutC1Counter.md`,
`MutC2Counter.md`, `w2/MutC1Reviews.md`); `neutral` mutants are behaviour-preserving edits
that a sound selftest must NOT kill (they catch a selftest that pins its own bytes).
Every `old` must occur exactly once in the round-45 source; the builder refuses otherwise.
"""
import json
import os
import sys

LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
FRESH = '.ufo/evidence/round-45/freshness/measure.py'
COVER = '.ufo/evidence/round-45/coverage/measure.py'

FRESH_MUT = [
    ('F01', 'snapshot-absent reason', "        return 'invalid', 'snapshot absent'\n", "        raw = b''\n", 'MutC1Counter S9'),
    ('F02', 'quote upper bound 25', "if n < 6 or n > 25:", "if n < 6 or n > 26:", 'MutC1Counter S1'),
    ('F03', 'quote present in snapshot', "if quote not in text:", "if False:", 'MutC1Counter S2'),
    ('F04', 'population needs a URL', "int(rid[1:]) <= MAX_ID and r['url']}", "int(rid[1:]) <= MAX_ID}", 'MutC1Counter S3'),
    ('F05', 'duplicate-entry refusal', "if counts[rid] != 1:", "if False:", 'MutC1Counter S4'),
    ('F06', 'review non-author', "or not who or who == authors.get(rid) or who not in seats:", "or not who or who not in seats:", 'MutC1Counter S5 / MutC1Reviews 1'),
    ('F07', 'seat output non-empty', "and str(x.get('output') or '').strip()}", "and str(x.get('output') or '')}", 'MutC1Counter S6'),
    ('F08', 'report path prefix', "if not report.startswith('.ufo/waves/round-45/'):", "if False:", 'MutC1Counter S7 / MutC1Reviews 3'),
    ('F09', 'report names reviewer', "re.escape(rid), text) or who not in text:", "re.escape(rid), text):", 'MutC1Counter S8 / MutC1Reviews 5'),
    ('F10', 'dispute sinks agree in measure', "fresh = len(agreed - disputed)", "fresh = len(agreed)", 'MutC1Counter S10 / MutC1Reviews 7'),
    ('F11', 'self_pin required in predicate', "passed = self_pin == 1 and fresh >= TARGET", "passed = fresh >= TARGET", 'MutC1Counter S11'),
    ('F12', 'target 50 in predicate', "passed = self_pin == 1 and fresh >= TARGET", "passed = self_pin == 1 and fresh >= 0", 'MutC1Counter S12'),
    ('F13', 'only agree counts as agree', "if r.get('verdict') == 'agree':", "if r.get('verdict') != 'dispute':", 'MutC1Reviews 6'),
    ('F14', 'population status mined', "r['status'] == 'mined'", "r['status'] != 'queued'", 'MutC1Reviews 9'),
    ('F15', 'population id bound inclusive', "int(rid[1:]) <= MAX_ID", "int(rid[1:]) < MAX_ID", 'MutC1Reviews 10'),
]
FRESH_NEUTRAL = [
    ('FN1', 'comment appended to the file', None, '\n# neutral comment\n', 'neutral'),
    ('FN2', 'cell count spelled in hex', "if len(cells) != 13:", "if len(cells) != 0xD:", 'neutral'),
    ('FN3', 'trailing comment on an assignment', "MAX_ID = 160", "MAX_ID = 160  # neutral", 'neutral'),
]
COVER_MUT = [
    ('C01', 'URL filter pinned to googletest', "/google/googletest/')\nSNAP_RE", "/')\nSNAP_RE", 'MutC2Counter M01'),
    ('C02', 'snapshot prefix pinned to round 45', "SNAP_RE = re.compile(re.escape(SNAP_PREFIX) + r'[A-Za-z0-9._/-]+')",
     "SNAP_RE = re.compile(r'\\.ufo/evidence/round-4[45]/coverage/sources/' + r'[A-Za-z0-9._/-]+')", 'MutC2Counter M03'),
    ('C03', 'missing snapshot skips the row', "        if data is None:\n            continue\n", "        if data is None:\n            data = b''\n", 'MutC2Counter M04'),
    ('C04', 'source: prefix on line 1', "if len(lines) < 3 or not lines[0].startswith('source:'):", "if len(lines) < 3:", 'MutC2Counter M06'),
    ('C05', 'recheck: prefix on line 3', "if not lines[2].startswith('recheck:'):", "if False:", 'MutC2Counter M08'),
    ('C06', 'README index full-path form', "if '`%s`' % path in readme or '`%s`' % path[len('corpus/'):] in readme:",
     "if '`%s`' % path[len('corpus/'):] in readme:", 'MutC2Counter M12'),
    ('C07', 'rows >= 2 threshold', "len(rows) >= 2", "len(rows) >= 1", 'MutC2Counter M13'),
    ('C08', 'entries >= 2 threshold', "len(entries) >= 2", "len(entries) >= 1", 'MutC2Counter M13'),
    ('C09', 'indexed == entries', "len(indexed) == len(entries)", "len(indexed) >= 1", 'MutC2Counter M13'),
    ('C10', 'self_pin required in predicate', "passed = self_pin == 1 and len(entries)", "passed = self_pin >= 0 and len(entries)", 'MutC2Counter M14'),
]
COVER_NEUTRAL = [
    ('CN1', 'comment appended to the file', None, '\n# neutral comment\n', 'neutral'),
    ('CN2', 'cell count spelled in hex', "len(cells) != 13 or cells[8]", "len(cells) != 0xD or cells[8]", 'neutral'),
    ('CN3', 'trailing comment on an assignment', "MIN_VERIFIED = '2026-10-25'", "MIN_VERIFIED = '2026-10-25'  # neutral", 'neutral'),
]


def entries(group_path, muts, neutrals):
    src = open(os.path.join(LANE, group_path), encoding='utf-8').read()
    out = []
    for kind, rows in (('mutant', muts), ('neutral', neutrals)):
        for mid, what, old, new, source in rows:
            if old is not None and src.count(old) != 1:
                sys.exit('refused: %s old text occurs %d times' % (mid, src.count(old)))
            out.append(dict(id=mid, kind=kind, what=what, old=old, new=new, source=source))
    return src, out


def main():
    groups = {}
    for name, path, muts, neutrals in (('freshness', FRESH, FRESH_MUT, FRESH_NEUTRAL),
                                       ('coverage', COVER, COVER_MUT, COVER_NEUTRAL)):
        _src, ms = entries(path, muts, neutrals)
        groups[name] = dict(orig=path, mutants=ms)
    out = os.path.join(LANE, '.ufo/evidence/round-46/hardening/mutants.json')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(dict(declared_from='round-45 wave audits MutC1Counter/MutC2Counter/MutC1Reviews',
                       groups=groups), fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    print('wrote %s: %s' % (out, {k: sum(1 for m in v['mutants'] if m['kind'] == 'mutant') for k, v in groups.items()}))


if __name__ == '__main__':
    main()
