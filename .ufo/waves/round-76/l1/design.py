#!/usr/bin/env python3
"""Round-76 L1 design phase: build the C1 candidates (arm19 + ARM11), the
seven-defect spec, the five instrument mutants, the C2 extended manifest, and
measure every before-state. Runs OUTSIDE the lane tree writes (scratch only);
the lane is read from git objects at the base revision.

Base: 451ed5cb6d5f8c2bf4b3e10836e4634cfcb03ee0 (= origin/master, clean tree).
"""
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
BASE = "451ed5cb6d5f8c2bf4b3e10836e4634cfcb03ee0"
OUT = "/fast/scratch/hyaku/tameshi-r76/l1"

os.makedirs(OUT, exist_ok=True)


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


report = {}

# ---------- pristine pins ----------
wr = base_blob("tools/wave-reconcile.py").decode("utf-8")
ss = base_blob("tools/selfstate-freshness.py").decode("utf-8")
spec6 = base_blob("tools/wave-reconcile-mutants.spec").decode("utf-8")
man17 = json.loads(base_blob("tools/selfstate-freshness.json"))
report["pins"] = {
    "wave-reconcile.py": sha(wr.encode()),
    "selfstate-freshness.py": sha(ss.encode()),
    "wave-reconcile-mutants.spec": sha(spec6.encode()),
}

# ---------- C1a: wave-reconcile arm19 candidate ----------
ARM19 = """        # round 76: the printed-less seat_reports bypass (round-75 carry,
        # T75W1R1). A seat_reports row whose record carries NO `printed` value
        # must refuse; the bypass mutant drops require_printed in this branch
        # only, so printed=None reaches the comparison and the detail
        # formatting raises TypeError — the wrapper catches that crash and the
        # arm fails on its named refusal instead of crashing the suite.
        def _seatreports_printed_required():
            try:
                return measure_row(
                    kind='seat_reports',
                    record={'path': 'report.md', 'rev': REV,
                            'span': '12 seats, 11 reports'})
            except SetupError as exc:
                return 'setup:' + str(exc).split(':')[0]
            except TypeError:
                return 'printed-none-reached-comparison'
        arm('arm19-seatreports-printed-required',
            'setup:record-printed-absent', _seatreports_printed_required)
    finally:"""
cand_wr = sub(wr, "SELFTEST_ARMS = 18", "SELFTEST_ARMS = 19", "wr-arms")
cand_wr = sub(cand_wr, "                       floor_pct=25))\n    finally:",
              "                       floor_pct=25))\n" + ARM19, "wr-arm19")
open(os.path.join(OUT, "cand-wr-19.py"), "w", newline="\n").write(cand_wr)
report["cand_wr_sha"] = sha(cand_wr.encode())

DEFECT7 = """
@defect adv-seatreports-require-printed-bypass | require_printed is dropped in the seat_reports branch only (r75 carry T75W1R1); arm19-seatreports-printed-required must kill it
@old     if kind == 'seat_reports':\\n        printed = _record_claim(row, readers, require_printed=True)
@new     if kind == 'seat_reports':\\n        printed = _record_claim(row, readers)
"""
spec7 = spec6 + DEFECT7
open(os.path.join(OUT, "wave-reconcile-mutants-r76.spec"), "w",
     newline="\n").write(spec7)
report["spec7_sha"] = sha(spec7.encode())

# ---------- C1b: selfstate ARM11 candidate ----------
ARM11 = '''
    # arm 11: the CLI binds --doc-rev (round-76 carry: the --doc-rev-ignored
    # mutant survived the round-75 battery 10/10, T75W1M1 settlement errata).
    # The arm runs the real CLI as a subprocess against a two-commit fixture
    # repo whose worktree doc disagrees with rev1: reading rev1 must measure
    # match; a tool that ignores --doc-rev reads the worktree and fails.
    fx = tempfile.mkdtemp(prefix="selfstate-arm11-",
                          dir=os.environ.get("TMPDIR") or None)
    try:
        def _git(*args):
            subprocess.run(["git", "-C", fx] + list(args), check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        def _put(rel, text):
            path = os.path.join(fx, rel)
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(path, "w", newline="\\n") as fh:
                fh.write(text)

        _put("SCORECARD.md", DOC_REV1)
        _put("tools/toy.py", "print('TOY_FIGURE: 4/4 pass')\\n")
        mpath = os.path.join(fx, "manifest.json")
        with open(mpath, "w", newline="\\n") as fh:
            json.dump({"schema": "tameshi-selfstate-freshness-v1",
                       "rows": [{"id": "toy-cli", "mode": "capability",
                                 "capability": "toy capture",
                                 "expect": "match", "figure": fig,
                                 "instrument": {"path": "tools/toy.py",
                                                "rev": None, "argv": []}}]},
                      fh)
        _git("init", "-q")
        _git("-c", "user.name=t", "-c", "user.email=t@t", "add",
             "SCORECARD.md", "tools/toy.py")
        _git("-c", "user.name=t", "-c", "user.email=t@t", "commit",
             "-qm", "rev1")
        rev1 = subprocess.run(["git", "-C", fx, "rev-parse", "HEAD"],
                              check=True, stdout=subprocess.PIPE)
        rev1 = rev1.stdout.decode().strip()
        rows = json.load(open(mpath))
        rows["rows"][0]["instrument"]["rev"] = rev1
        with open(mpath, "w", newline="\\n") as fh:
            json.dump(rows, fh)
        _put("SCORECARD.md", DOC_WT)
        proc = subprocess.run(
            [sys.executable, "-I", "-X", "utf8",
             os.path.abspath(__file__),
             "--repo", fx, "--doc-rev", rev1, "--manifest", mpath],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        out_text = proc.stdout.decode("utf-8", "replace")
        arm("ARM11_doc_rev_cli_binding",
            proc.returncode == 0
            and "SELFSTATE: rows=1 match=1 stale=0 unexpected=0" in out_text,
            "rc=%r tail=%r err=%r" % (
                proc.returncode, out_text[-160:],
                proc.stderr.decode("utf-8", "replace")[-160:]))
    finally:
        shutil.rmtree(fx, ignore_errors=True)

    out.write('SELFSTATE_SELFTEST: %d/%d pass\\n' % (ok, total))
    return 0 if (ok == total == SELFTEST_ARMS) else 1
'''
DOC_REV1 = ("# toy scorecard\\n\\n## Capabilities\\n\\n"
            "| Capability | What it can now do | Evidence pointer | Round |\\n"
            "|---|---|---|---|\\n"
            "| toy capture | writes a figure | `TOY_FIGURE: 4/4 pass` | toy |\\n")
DOC_WT = DOC_REV1.replace("4/4", "9/9")
cand_ss = sub(ss, "SELFTEST_ARMS = 10", "SELFTEST_ARMS = 11", "ss-arms")
OLD_TAIL = ("    out.write('SELFSTATE_SELFTEST: %d/%d pass\\n' % (ok, total))\n"
            "    return 0 if (ok == total == SELFTEST_ARMS) else 1\n")
assert OLD_TAIL in cand_ss, "selfstate tail anchor missing"
NEW_TAIL = ARM11.replace("\\\\n", "\\\\n")
NEW_TAIL = (ARM11.replace("\\\\n", "\\\\n")
            if False else ARM11)
cand_ss = sub(cand_ss, OLD_TAIL,
              NEW_TAIL.replace("\\\\n", "\005").replace("\\n", "\n")
              .replace("\005", "\\n").replace('\\"', '"')
              .replace("\\\\", "\\"), "ss-arm11")
open(os.path.join(OUT, "cand-ss-11.py"), "w", newline="\n").write(cand_ss)
report["cand_ss_sha"] = sha(cand_ss.encode())

# ---------- five instrument mutants on the candidate bytes ----------
mutants = {}
m_a = sub(cand_ss, """        stdout, exit_code, _stderr = runner(row)
        measured_token = extract_token(row['figure'], stdout, rid)
""", """        measured_token = doc_token
""", "echo")
mutants["echo-doc-token"] = m_a
m_b = sub(cand_ss, "            'ok': measured == row['expect'],",
          "            'ok': True,", "expect")
mutants["expect-ignored"] = m_b
m_c = sub(cand_ss, "                raise SetupError('capability-absent:%s:%s' % (rid, name))",
          "                raise SetupError('zero-rows-deflected')", "capabs")
mutants["capability-absent-deflected"] = m_c
m_d = sub(cand_ss, "        raise SetupError('zero-rows')", "        pass", "zero")
mutants["zero-rows-success"] = m_d
m_e = sub(cand_ss, "        if a.doc_rev:", "        if False:", "docrev")
mutants["doc-rev-ignored"] = m_e
for name, text in mutants.items():
    open(os.path.join(OUT, "mut-%s.py" % name), "w", newline="\n").write(text)
    report["mut_" + name] = sha(text.encode())

# ---------- C2 extended manifest (17 -> 20 rows) ----------
man = json.loads(base_blob("tools/selfstate-freshness.json"))
rows = man["rows"] if isinstance(man, dict) else man
INST_REV = BASE
new_rows = [
    {"id": "r76-pin-disposition-selftest", "mode": "capability",
     "capability": "six-leg content-disposition probe",
     "figure": r"\d+/\d+",
     "instrument": {"path": "tools/pin-disposition.py", "rev": INST_REV,
                    "argv": ["--selftest"]}, "expect": "match"},
    {"id": "r76-evidence-disposition-selftest", "mode": "capability",
     "capability": "effective expectation reconciliation",
     "figure": r"\d+/\d+",
     "instrument": {"path": "tools/evidence-disposition.py", "rev": INST_REV,
                    "argv": ["--selftest"]}, "expect": "match"},
    {"id": "r76-r17-evidence-disposition", "mode": "span",
     "span": "56/56",
     "figure": r"\d+/\d+",
     "instrument": {"path": "tools/evidence-disposition.py", "rev": INST_REV,
                    "argv": ["--selftest"]}, "expect": "stale"},
]
ext = (man if isinstance(man, dict) else {"rows": rows})
ext_rows = (ext["rows"] if isinstance(ext, dict) else ext) + new_rows
if isinstance(ext, dict):
    ext["rows"] = ext_rows
    man20 = ext
else:
    man20 = ext_rows
open(os.path.join(OUT, "selfstate-freshness-r76.json"), "w",
     newline="\n").write(json.dumps(man20, indent=1) + "\n")
report["man20_rows"] = len(ext_rows)

# ---------- receipts ----------
with open(os.path.join(OUT, "design-report.json"), "w") as fh:
    json.dump(report, fh, indent=1, sort_keys=True)
print(json.dumps(report, indent=1, sort_keys=True))
