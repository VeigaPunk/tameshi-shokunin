#!/usr/bin/env python3
"""Extended parity probe for the r37 ANSI-C code_view mutation receipts.

Ground truth: GNU bash (bash -n lexical witnesses + execution witnesses) — the
same fixture family wave-1 seat MutateAnsiEscapePair used in /tmp scratch.
Runs code_view loaded from pristine tool bytes and from the parity-lookbehind
mutant; prints per-fixture divergences from the bash-truth expectation.
"""
import subprocess, sys, hashlib

TOOL = open('/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/tally-audit-v3.py').read()
MUT = open('/tmp/mutant_lookbehind.py').read()

def load(src):
    ns = {"__name__": "probe", "__file__": "tool.py"}
    exec(compile(src, "tool.py", "exec"), ns)
    return ns["code_view"]

# fixture: (name, line, expect_blank_comment) — line shape keeps bash validity.
F = [
 ("frozen_1",          r": $'it\'s' # inert st_tsu=0" + "\nst_tsu=9\n", True),
 ("frozen_1_2bs",      r": $'it\\' # inert st_tsu=0" + "\nst_tsu=9\n", True),
 ("F1_1bs_comment",    "printf '%s' $'it\\'s' # INERT\nprintf 'TAIL\\n'\n", True),
 ("F2_2bs_comment",    "printf '%s' $'a\\\\' # INERT\nprintf 'TAIL\\n'\n", True),
 ("F3_1bs_literal",    "printf '%s' $'it\\'s # KEEP'\nprintf 'TAIL\\n'\n", False),
 ("F4_2bs_literal",    "printf '%s' $'a\\\\ # KEEP'\nprintf 'TAIL\\n'\n", False),
 ("F5_3bs_comment",    "printf '%s' $'a\\\\\\'b' # INERT\nprintf 'TAIL\\n'\n", True),
 ("F6_4bs_comment",    "printf '%s' $'a\\\\\\\\' # INERT\nprintf 'TAIL\\n'\n", True),
 ("F7_2bs_nospace",    "printf '%s' $'a\\\\'#INERT\n", False),
 ("F8_1bs_nospace",    "printf '%s' $'a\\'#'\n", False),
 ("F9_1bs_multiline",  "printf '%s' $'it\\'\nb' # INERT\n", True),
 ("F10_2bs_nextline",  "printf '%s' $'a\\\\'\n# INERT\n", True),
 ("frozen_2",          ": $'literal # data'\nst_tsu=9\n", False),
 ("frozen_2_2bs",      ": $'literal # data\\\\'\nst_tsu=9\n", False),
]

def expected_view(line, blank):
    if not blank:
        return line
    i = line.index('#')
    j = line.find('\n', i)
    if j < 0: j = len(line)
    return line[:i] + ' ' * (j - i) + line[j:]

def run(cv):
    div = 0
    rows = []
    for name, line, blank in F:
        want = expected_view(line, blank)
        got = cv(line)
        d = "ok" if got == want else "DIVERGES"
        if got != want: div += 1
        rows.append((name, d, got if d == "DIVERGES" else ""))
    return div, rows

# bash ground-truth spot witness: frozen_1 string stays open (rc=2), frozen_1_2bs closes.
for wname, wline in (("x=$'it\\'", "odd-parity quote OPEN at EOF"),
                     ("x=$'it\\\\'", "even-parity quote CLOSED")):
    p = subprocess.run(["bash", "-n", "/dev/stdin"], input=(wname + "\n").encode(),
                       capture_output=True)
    print(f"bash -n {wname!r}: rc={p.returncode} ({wline})")

for label, src in (("pristine", TOOL), ("mutant_lookbehind", MUT)):
    cv = load(src)
    div, rows = run(cv)
    print(f"== {label} sha256={hashlib.sha256(src.encode()).hexdigest()}")
    for name, d, got in rows:
        print(f"  {name:20s} {d}" + (f"  got={got!r}" if got else ""))
    print(f"SUMMARY tool={label} divergences={div} fixtures={len(F)}")
PYEOF = None
