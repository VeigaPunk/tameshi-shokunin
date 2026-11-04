#!/usr/bin/env python3
"""Design phase part 2: build the selfstate ARM11 candidate from the block
file, rebuild the five instrument mutants on the candidate bytes, and measure
the C2 manifest runs + instrument stdout token uniqueness + receipt-exists
leak. Scratch-only writes."""
import hashlib
import json
import os
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
BASE = "451ed5cb6d5f8c2bf4b3e10836e4634cfcb03ee0"
OUT = "/fast/scratch/hyaku/tameshi-r76/l1"
SCRATCH = "/fast/scratch/hyaku/tameshi-r76"


def git(*args):
    return subprocess.run(["git", "-C", LANE] + list(args),
                          check=True, stdout=subprocess.PIPE).stdout


def base_blob(path):
    return git("cat-file", "blob", "%s:%s" % (BASE, path))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sub(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit("edit %s: expected 1 occurrence, got %d" % (label, n))
    return text.replace(old, new, 1)


ss = base_blob("tools/selfstate-freshness.py").decode("utf-8")
block = open(os.path.join(OUT, "arm11-block.txt")).read()

DOC_REV1 = ("# toy scorecard\n\n## Capabilities\n\n"
            "| Capability | What it can now do | Evidence pointer | Round |\n"
            "|---|---|---|---|\n"
            "| toy capture | writes a figure | `TOY_FIGURE: 4/4 pass` | toy |\n")
DOC_WT = DOC_REV1.replace("4/4", "9/9")
CONSTS = ("DOC_REV1 = (\n"
          "    '# toy scorecard\\n\\n## Capabilities\\n\\n'\n"
          "    '| Capability | What it can now do | Evidence pointer | Round |\\n'\n"
          "    '|---|---|---|---|\\n'\n"
          "    '| toy capture | writes a figure | `TOY_FIGURE: 4/4 pass` | toy |\\n'\n"
          ")\n"
          "DOC_WT = DOC_REV1.replace('4/4', '9/9')\n")

cand = sub(ss, "SELFTEST_ARMS = 10", "SELFTEST_ARMS = 11", "ss-arms")
OLD_TAIL = ("    out.write('SELFSTATE_SELFTEST: %d/%d pass\\n' % (ok, total))\n"
            "    return 0 if (ok == total == SELFTEST_ARMS) else 1\n")
cand = sub(cand, "def selftest(out=sys.stdout):",
           CONSTS + "\ndef selftest(out=sys.stdout):", "ss-consts")
cand = sub(cand, OLD_TAIL, block, "ss-arm11")
open(os.path.join(OUT, "cand-ss-11.py"), "w", newline="\n").write(cand)
print("cand-ss-11 sha", sha(cand.encode()))

mutants = {}
m_a = sub(cand, "        stdout, exit_code, _stderr = runner(row)\n"
          "        measured_token = extract_token(row['figure'], stdout, rid)\n",
          "        stdout, exit_code, _stderr = ('', 0, '')\n"
          "        measured_token = doc_token\n", "echo")
mutants["echo-doc-token"] = m_a
m_b = sub(cand, "            'ok': measured == row['expect'],",
          "            'ok': True,", "expect")
mutants["expect-ignored"] = m_b
m_c = sub(cand, "                raise SetupError('capability-absent:%s:%s' % (rid, name))",
          "                raise SetupError('zero-rows-deflected')", "capabs")
mutants["capability-absent-deflected"] = m_c
m_d = sub(cand, "        raise SetupError('zero-rows')", "        pass", "zero")
mutants["zero-rows-success"] = m_d
m_e = sub(cand, "        if a.doc_rev:", "        if False:", "docrev")
mutants["doc-rev-ignored"] = m_e
for name, text in mutants.items():
    open(os.path.join(OUT, "mut-%s.py" % name), "w", newline="\n").write(text)
    print("mut", name, sha(text.encode()))

# receipt-exists leak red-before
leak = os.path.join(SCRATCH, "leak-probe")
subprocess.run(["rm", "-rf", leak], check=True)
os.makedirs(leak)
env = dict(os.environ, TMPDIR=leak)
before = sorted(os.listdir(leak))
r = subprocess.run(["python3", "-I", os.path.join(LANE, "tools/receipt-exists.py"),
                    "--selftest"], env=env, stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE, cwd=LANE)
after = sorted(os.listdir(leak))
print("receipt-exists rc", r.returncode, r.stdout.decode()[-80:].strip())
print("leak-before", len(before), before[:4])
print("leak-after", len(after), after[:8])
