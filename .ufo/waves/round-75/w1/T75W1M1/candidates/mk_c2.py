#!/usr/bin/env python3
"""Build the five single-edit C2 mutants from the unmutated stub."""
import hashlib
import os

S = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(S, 'selfstate-freshness.py')
SRC = open(BASE, encoding='utf-8').read()


def sub(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit('edit %s: expected 1 occurrence, got %d' % (label, n))
    return text.replace(old, new, 1)


def write(name, text):
    with open(os.path.join(S, name), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    print('%-30s %s' % (name, hashlib.sha256(text.encode()).hexdigest()))


# (a) measured := doc token (the echo cheat): the instrument is never run.
a = sub(
    SRC,
    """    stdout = runner(inst['rev'], inst['path'], inst['argv'])
    found = re.search(row['figure'], stdout)
    if found is None:
        raise SetupError('instrument-figure-absent:%s' % row['id'])
    measured_token = found.group(0)
""",
    """    measured_token = doc_token
""",
    'echo')
write('m_a_echo_doc_token.py', a)

# (b) expect ignored: every row ok, nothing unexpected.
b = sub(SRC, "        ok = state == row['expect']", "        ok = True", 'expect')
write('m_b_expect_ignored.py', b)

# (c) missing capability treated as match instead of setup refusal.
c = sub(SRC, """        if line is None:
            raise SetupError('capability-absent:%s' % row['id'])
""", """        if line is None:
            return ('match', None, None)
""", 'absent capability')
write('m_c_capability_absent_match.py', c)

# (d) zero rows succeed instead of refusing.
d = sub(SRC, """    if not isinstance(rows, list) or not rows:
        raise SetupError('zero-rows')
""", """    if not isinstance(rows, list):
        raise SetupError('zero-rows')
""", 'zero rows')
write('m_d_zero_rows_success.py', d)

# (e) --doc-rev ignored: always read the worktree copy.
e = sub(SRC, """def load_doc(repo, rev, path, reader):
    \"\"\"The doc is read at `rev` through the revision-bound reader.\"\"\"
    return reader.text(rev, path)
""", """def load_doc(repo, rev, path, reader):
    \"\"\"The doc is read at `rev` through the revision-bound reader.\"\"\"
    with open(os.path.join(repo, path), 'rb') as fh:
        return fh.read().decode('utf-8')
""", 'doc rev')
write('m_e_doc_rev_ignored.py', e)
