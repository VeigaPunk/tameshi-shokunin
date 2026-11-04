#!/usr/bin/env python3
"""Build the R75-C1 18-arm candidate from pristine base bytes and single-edit mutants.

Every replacement asserts an exact occurrence count of 1 so the edit is the only delta.
"""
import hashlib
import os
import sys

S = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(S, 'pristine.py')
SRC = open(BASE, encoding='utf-8').read()


def sub(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit('edit %s: expected 1 occurrence, got %d' % (label, n))
    return text.replace(old, new, 1)


def write(name, text):
    path = os.path.join(S, name)
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    print('%-28s %s' % (name, hashlib.sha256(text.encode()).hexdigest()))


# ---------------- 18-arm candidate (plan's three frozen arms) ----------------
c = SRC
c = sub(c, 'SELFTEST_ARMS = 15', 'SELFTEST_ARMS = 18', 'arm count')
c = sub(
    c,
    "REPORT = (b'- **The wave**: 12 seats, 11 reports; three seats found defects.\\n')",
    "REPORT = (b'- **The wave**: 12 seats, 11 reports; three seats found defects.\\n')\n"
    "# round-75 arm16: the record carries a delimited 1 OUTSIDE the span.\n"
    "CLAIM = (b'- The wave: 11 reports; 1 seat filed late.\\n')",
    'claim blob')
c = sub(
    c,
    "    blobs = {(REV, 'report.md'): REPORT, (REV, 'plan.md'): PLAN,\n"
    "             (REV, 'results.json'): results, (REV, 'spec.json'): spec}",
    "    blobs = {(REV, 'report.md'): REPORT, (REV, 'plan.md'): PLAN,\n"
    "             (REV, 'results.json'): results, (REV, 'spec.json'): spec,\n"
    "             (REV, 'claim.md'): CLAIM}",
    'fixture blobs')
arms = """        arm('arm15-seatreports-top-level-only', 'meet',
            lambda: measure_row(kind='seat_reports',
                                record={'path': 'report.md', 'rev': REV,
                                        'span': '12 seats, 11 reports',
                                        'printed': 12}))
        # round 75: the three rules measured as survivors at base 21ef81e9.
        # arm16 kills M-C (printed bound to the whole record, not the span);
        # arm17/arm18 kill the selective _record_claim bypass on roles and
        # attack_share. Each mutant dies on its NAMED arm and no other.
        arm_raises('arm16-printed-span-not-record', 'printed-not-in-span',
                   lambda: measure_row(kind='seats',
                                       record={'path': 'claim.md', 'rev': REV,
                                               'span': '11 reports',
                                               'printed': 1}))
        arm_raises('arm17-record-claim-live-on-roles', 'span-not-in-record',
                   lambda: measure_row(kind='roles',
                                       declaration={'form': 'spec-items',
                                                    'path': 'spec.json',
                                                    'rev': REV},
                                       record={'path': 'report.md', 'rev': REV,
                                               'span': '13 seats'}))
        arm_raises('arm18-record-claim-live-on-attack-share',
                   'span-not-in-record',
                   lambda: measure_row(kind='attack_share',
                                       named=['reviewer', 'critic',
                                              'mutation-tester'],
                                       floor_pct=25,
                                       record={'path': 'report.md', 'rev': REV,
                                               'span': '13 seats'}))
"""
c = sub(
    c,
    """        arm('arm15-seatreports-top-level-only', 'meet',
            lambda: measure_row(kind='seat_reports',
                                record={'path': 'report.md', 'rev': REV,
                                        'span': '12 seats, 11 reports',
                                        'printed': 12}))
""",
    arms,
    'new arms')
write('cand18.py', c)

# ---------------- named round-74 mutants (must die on one named arm) --------
m = c
m = sub(m, '    _, rec = _record_span(row, readers)',
        '    raw, rec = _record_span(row, readers)', 'M-C bind')
m = sub(m, "    if not delimited(printed, rec['span']):",
        "    if not delimited(printed, raw):", 'M-C span')
write('m_mc_record_bound.py', m)

m = c
m = sub(m, "    if kind == 'roles':\n        _record_claim(row, readers)\n",
        "    if kind == 'roles':\n", 'roles bypass')
write('m_roles_bypass.py', m)

m = c
m = sub(m, "    if kind == 'attack_share':\n        _record_claim(row, readers)\n",
        "    if kind == 'attack_share':\n", 'attack bypass')
write('m_attack_bypass.py', m)

# ---------------- alternative mutants (one per new arm) --------------------
# A16: printed admitted from span OR whole record (wider than base, narrower
# than M-C). A sharpness-blind fixture = arm13 (record carries no delimited 1).
m = c
m = sub(m, '    _, rec = _record_span(row, readers)',
        '    raw, rec = _record_span(row, readers)', 'A16 bind')
m = sub(m, "    if not delimited(printed, rec['span']):",
        "    if (not delimited(printed, rec['span'])\n"
        "            and not delimited(printed, raw)):",
        'A16 union')
write('a16_span_or_record.py', m)

# A17: roles text-tokens binds the record span but never the declaration.
m = c
m = sub(
    m,
    """            for role, count in declared.items():
                if not re.search(r'(?<![0-9])%d\\s+%s\\b' % (count, re.escape(role)),
                                 span):
                    raise SetupError('declaration-absent-in-record:%s:%s'
                                     % (row['id'], role))
""",
    """            for role, count in declared.items():
                pass
""",
    'A17 declaration')
write('a17_roles_decl_unbound.py', m)

# A18: attack_share binds the span but not the row's printed claim.
m = c
m = sub(m, "    if kind == 'attack_share':\n        _record_claim(row, readers)\n",
        "    if kind == 'attack_share':\n        _record_span(row, readers)\n",
        'A18 span only')
write('a18_attack_span_only.py', m)
