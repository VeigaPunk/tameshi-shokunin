#!/usr/bin/env python3
"""T76W1E2 independent re-derivation of the R76-C1 selfstate ARM11 candidate.

Builds from the BASE BYTES of tools/selfstate-freshness.py @451ed5cb
(extracted via git cat-file; sha256 verified against the plan) — does NOT
read the L1's candidate file. Applies, per plans/round-76.plan.md R76-C1:

  * SELFTEST_ARMS 10 -> 11
  * one new selftest arm ARM11_doc_rev_cli_binding: the real CLI runs as a
    subprocess against a two-state git fixture (rev1 doc `4/4` vs worktree
    doc `9/9`, toy instrument committed at rev1); reading --doc-rev must
    measure rows=1 match=1 stale=0 unexpected=0 exit 0; a tool that ignores
    --doc-rev reads the worktree and fails the arm.

Then rebuilds the five frozen instrument mutants on the candidate bytes and
one base doc-rev mutant on the base bytes, asserting count(old)==1 per edit.
Scratch-only writes.
"""
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "base-selfstate.py")
CAND = os.path.join(HERE, "cand-ss-11-mine.py")


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def sub(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit("edit %s: expected 1 occurrence, got %d" % (label, n))
    return text.replace(old, new, 1)


assert sha(BASE) == "3b09676340fc63007d3a1e5de3e54471feddb22024a2f40bd4b3b469f560eba6", \
    "base bytes mismatch vs plan"
ss = open(BASE, encoding="utf-8").read()

cand = sub(ss, "SELFTEST_ARMS = 10", "SELFTEST_ARMS = 11", "arms")

# Fixture doc constants: committed rev1 quotes 4/4, the worktree doc 9/9.
CONSTS = (
    "DOC_REV1 = (\n"
    "    '# toy scorecard\\n\\n## Capabilities\\n\\n'\n"
    "    '| Capability | What it can now do | Evidence pointer | Round |\\n'\n"
    "    '|---|---|---|---|\\n'\n"
    "    '| toy capture | writes a figure | `TOY_FIGURE: 4/4 pass` | toy |\\n'\n"
    ")\n"
    "DOC_WT = DOC_REV1.replace('4/4', '9/9')\n"
)

# The new arm, in my own hand: a fixture temp dir under TMPDIR, a throwaway
# identity used ONLY inside the fixture repo (-c user.name/user.email on each
# git call), the manifest rewritten with the real rev1 after the commit, and
# the real CLI driven as a subprocess with --doc-rev.
BLOCK = '''\
    # arm 11: the CLI subprocess binds --doc-rev (round-76 carry: the
    # --doc-rev-ignored instrument mutant survived the round-75 battery
    # 10/10). The arm materializes a two-state git fixture under TMPDIR: rev1
    # commits a doc quoting 4/4 plus a toy instrument printing 4/4; the
    # worktree doc is then rewritten to 9/9. The real CLI run with
    # --doc-rev rev1 must measure rows=1 match=1 stale=0 unexpected=0 exit 0;
    # a tool that ignores --doc-rev reads the worktree doc and measures
    # stale, so this arm fails.
    fx = tempfile.mkdtemp(prefix='selfstate-arm11-',
                          dir=os.environ.get('TMPDIR') or None)
    try:
        def fx_git(*args):
            subprocess.run(['git', '-C', fx] + list(args), check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        def fx_put(rel, text):
            dest = os.path.join(fx, rel)
            parent = os.path.dirname(dest)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(dest, 'w', newline='\\n') as fh:
                fh.write(text)

        fx_put('SCORECARD.md', DOC_REV1)
        fx_put('tools/toy.py', "print('TOY_FIGURE: 4/4 pass')\\n")
        mpath = os.path.join(fx, 'manifest.json')
        with open(mpath, 'w', newline='\\n') as fh:
            json.dump({'schema': 'tameshi-selfstate-freshness-v1',
                       'rows': [{'id': 'toy-cli', 'mode': 'capability',
                                 'capability': 'toy capture',
                                 'expect': 'match', 'figure': fig,
                                 'instrument': {'path': 'tools/toy.py',
                                                'rev': None, 'argv': []}}]},
                      fh)
        fx_git('init', '-q')
        fx_git('-c', 'user.name=arm11-t', '-c', 'user.email=arm11-t@fixture',
               'add', 'SCORECARD.md', 'tools/toy.py')
        fx_git('-c', 'user.name=arm11-t', '-c', 'user.email=arm11-t@fixture',
               'commit', '-qm', 'rev1')
        rev1 = subprocess.run(['git', '-C', fx, 'rev-parse', 'HEAD'],
                              check=True,
                              stdout=subprocess.PIPE).stdout.decode().strip()
        with open(mpath, encoding='utf-8') as fh:
            manifest_rows = json.load(fh)
        manifest_rows['rows'][0]['instrument']['rev'] = rev1
        with open(mpath, 'w', newline='\\n') as fh:
            json.dump(manifest_rows, fh)
        fx_put('SCORECARD.md', DOC_WT)
        cli = subprocess.run(
            [sys.executable, '-I', '-X', 'utf8',
             os.path.abspath(__file__),
             '--repo', fx, '--doc-rev', rev1, '--manifest', mpath],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        cli_out = cli.stdout.decode('utf-8', 'replace')
        arm('ARM11_doc_rev_cli_binding',
            cli.returncode == 0
            and 'SELFSTATE: rows=1 match=1 stale=0 unexpected=0' in cli_out,
            'rc=%r tail=%r err=%r' % (
                cli.returncode, cli_out[-160:],
                cli.stderr.decode('utf-8', 'replace')[-160:]))
    finally:
        shutil.rmtree(fx, ignore_errors=True)

'''

OLD_TAIL = ("    out.write('SELFSTATE_SELFTEST: %d/%d pass\\n' % (ok, total))\n"
            "    return 0 if (ok == total == SELFTEST_ARMS) else 1\n")

cand = sub(cand, "def selftest(out=sys.stdout):",
           CONSTS + "\ndef selftest(out=sys.stdout):", "consts")
cand = sub(cand, OLD_TAIL, BLOCK + OLD_TAIL, "arm11")

with open(CAND, "w", newline="\n") as fh:
    fh.write(cand)
print("candidate sha256", sha(CAND))
print("candidate bytes", len(cand.encode("utf-8")))

# --- five frozen instrument mutants on MY candidate bytes -----------------
mutants = {}
m_a = sub(cand,
          "        stdout, exit_code, _stderr = runner(row)\n"
          "        measured_token = extract_token(row['figure'], stdout, rid)\n",
          "        stdout, exit_code, _stderr = ('', 0, '')\n"
          "        measured_token = doc_token\n", "echo")
mutants["mut-echo-doc-token.py"] = m_a
m_b = sub(cand, "            'ok': measured == row['expect'],",
          "            'ok': True,", "expect")
mutants["mut-expect-ignored.py"] = m_b
m_c = sub(cand,
          "                raise SetupError('capability-absent:%s:%s' % (rid, name))",
          "                raise SetupError('zero-rows-deflected')", "capabs")
mutants["mut-capability-absent-deflected.py"] = m_c
m_d = sub(cand, "        raise SetupError('zero-rows')", "        pass", "zero")
mutants["mut-zero-rows-success.py"] = m_d
m_e = sub(cand, "        if a.doc_rev:", "        if False:", "docrev")
mutants["mut-doc-rev-ignored.py"] = m_e

for name, text in mutants.items():
    path = os.path.join(HERE, name)
    with open(path, "w", newline="\n") as fh:
        fh.write(text)
    print(name, sha(path))

# --- base-bytes doc-rev mutant (the survivor that passed 10/10 at r75) ----
m_base = sub(ss, "        if a.doc_rev:", "        if False:", "base-docrev")
path = os.path.join(HERE, "mut-base-docrev.py")
with open(path, "w", newline="\n") as fh:
    fh.write(m_base)
print("mut-base-docrev.py", sha(path))
