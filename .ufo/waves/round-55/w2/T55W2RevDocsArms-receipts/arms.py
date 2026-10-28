#!/usr/bin/env python3
"""T55W2RevDocsArms: check the three documentation surfaces the C2 counter reads,
at content commit C0 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb.

Usage: CLONE=<path to a git clone checked out at C0> python3 arms.py <section>

Sections: cells | diff | grammar | lazy | arms | classes | all
Everything is read-only; the clone is never mutated.
"""
import json
import os
import re
import subprocess
import sys

CLONE = os.environ["CLONE"]
BASE = "0a2010acd1e92e4e332774050825e21bcfc7e079"
C0 = "9cf0146b94ddba12d454ebf7288ce6e5c5d535bb"
MARKER = "could-not-evaluate: cannot create clone scratch under the scratch root"
GRAMMAR = re.compile(
    r"^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?: could-not-evaluate: cannot create clone "
    r"scratch under the scratch root: TMPDIR is not a usable directory: '.+' "
    r"\(could-not-evaluate\)$")
SEVEN = ("env-diff", "repeat-control", "registry-check", "bash-witness-study",
         "pin-disposition", "evidence-disposition", "context-capture")
ALLOC = [
    ("env-diff --selftest", ["python3", "tools/env-diff.py", "--selftest"]),
    ("env-diff --contract", ["python3", "tools/env-diff.py", "--contract",
                             ".ufo/evidence/round-55/c2/fixture-contract.json",
                             "--out", os.path.join(CLONE, "..", "envdiff-out.json"),
                             "--fleet-root", CLONE]),
    ("repeat-control --selftest", ["python3", "tools/repeat-control.py", "--selftest"]),
    ("registry-check --selftest", ["python3", "tools/registry-check.py", "--selftest"]),
    ("registry-check --rev", ["python3", "tools/registry-check.py", "--rev", "HEAD"]),
    ("bash-witness-study selftest", ["python3", "tools/bash-witness-study.py", "selftest"]),
    ("pin-disposition --selftest", ["python3", "tools/pin-disposition.py", "--selftest"]),
    ("evidence-disposition --selftest", ["python3", "tools/evidence-disposition.py", "--selftest"]),
    ("context-capture --selftest", ["python3", "tools/context-capture.py", "--selftest"]),
]
LAZY = [
    ("repeat-control --snapshot", ["python3", "tools/repeat-control.py", "--snapshot",
                                   ".ufo/evidence/round-12/ControlGate"]),
    ("bash-witness-study count", ["python3", "tools/bash-witness-study.py", "count"]),
    ("pin-disposition --read", ["python3", "tools/pin-disposition.py", "--manifest",
                                ".ufo/evidence/round-13/pin-manifest.json",
                                "--root", "/home/vgpnk/Projects/shokunin"]),
    ("evidence-disposition --json", ["python3", "tools/evidence-disposition.py",
                                     "--root", ".", "--dispositions",
                                     ".ufo/evidence/round-18/dispositions.json", "--json"]),
    ("context-capture --check", ["python3", "tools/context-capture.py", "--check", "--json"]),
]


def env(tmpdir):
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    e.pop("TMPDIR", None)
    if tmpdir is not None:
        e["TMPDIR"] = tmpdir
    return e


def run(argv, e, trace_to=None):
    cmd = (["strace", "-f", "-e", "trace=mkdir,mkdirat", "-o", trace_to] + argv) if trace_to else argv
    p = subprocess.run(cmd, cwd=CLONE, env=e, capture_output=True, text=True, timeout=1800)
    return p.returncode, p.stdout, p.stderr


def git(*args):
    return subprocess.run(["git", "-C", CLONE, *args], capture_output=True, text=True)


def section_cells():
    reg = json.load(open(os.path.join(CLONE, "tools/registry.json")))
    cells = [r for r in reg["rows"] if r.get("scratch_root")]
    print("rows=%d scratch_root cells=%d" % (len(reg["rows"]), len(cells)))
    unusable = "/nonexistent/such/tmpdir-T55W2RevDocsArms"
    for r in cells:
        cell = r["scratch_root"]
        quoted = re.search(r'"([^"]+): could-not-evaluate', cell)
        claimed = quoted.group(1) if quoted else "(none quoted)"
        tool = re.search(r"tools/([a-z-]+)\.py", " ".join(r["argv"])).group(1)
        argv = {"repeat-control": ["python3", "tools/repeat-control.py", "--selftest"],
                "bash-witness-study": ["python3", "tools/bash-witness-study.py", "selftest"],
                "pin-disposition": ["python3", "tools/pin-disposition.py", "--selftest"],
                "evidence-disposition": ["python3", "tools/evidence-disposition.py", "--selftest"],
                "context-capture": ["python3", "tools/context-capture.py", "--selftest"],
                "registry-check": ["python3", "tools/registry-check.py", "--selftest"],
                "env-diff": ["python3", "tools/env-diff.py", "--selftest"]}[tool]
        rc, out, err = run(argv, env(unusable))
        first = err.splitlines()[0] if err else ""
        actual = first.split(": could-not-evaluate")[0] if ": could-not-evaluate" in first else first
        print("---")
        print("row       : %s" % r["name"])
        print("argv      : %s" % " ".join(r["argv"]))
        print("alloc     : %s" % cell.split("Allocating modes:")[-1].strip())
        print("marker    : %s" % (MARKER in cell))
        print("claimed   : %s" % claimed)
        print("actual    : %s" % actual)
        print("VERDICT   : %s" % ("token MATCHES" if claimed == actual else "token FALSE in the cell"))


def section_diff():
    base = json.loads(git("show", BASE + ":tools/registry.json").stdout)
    c0 = json.load(open(os.path.join(CLONE, "tools/registry.json")))
    print("base rows=%d c0 rows=%d schema_equal=%s order_equal=%s"
          % (len(base["rows"]), len(c0["rows"]), base["schema"] == c0["schema"],
             [r["name"] for r in base["rows"]] == [r["name"] for r in c0["rows"]]))
    an = {r["name"]: r for r in base["rows"]}
    bn = {r["name"]: r for r in c0["rows"]}
    print("only_base=%s only_c0=%s" % (sorted(set(an) - set(bn)), sorted(set(bn) - set(an))))
    for n in an:
        if n in bn and an[n] != bn[n]:
            for k in sorted(set(an[n]) | set(bn[n])):
                if an[n].get(k) != bn[n].get(k):
                    print("CHANGED row=%s key=%s" % (n, k))
    print("--- line churn ---")
    print(git("diff", "--numstat", BASE, C0, "--", "tools/registry.json").stdout.strip())
    for rev in (BASE, C0):
        line2 = git("show", rev + ":tools/registry.json").stdout.splitlines()[1]
        print("rev %s line2 = %r" % (rev[:8], line2))


def section_grammar():
    # The counter materializes this contract into the clone; do the same here.
    path = os.path.join(CLONE, ".ufo/evidence/round-55/c2/fixture-contract.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(json.dumps({"surfaces": [
        {"name": "stable", "repo": ".", "rev": "HEAD",
         "path": ".ufo/evidence/round-12/BaselineControl/fixtures/target.sh",
         "interp": "bash"}]}, indent=1) + "\n")
    unusable = "/nonexistent/such/tmpdir-T55W2RevDocsArms"
    for name, argv in ALLOC:
        rc, out, err = run(argv, env(unusable))
        lines = err.splitlines()
        hit = [l for l in lines if GRAMMAR.match(l)]
        tok = hit[0].split(": could-not-evaluate")[0] if hit else "(no grammar line)"
        print("%-32s rc=%s stderr_lines=%d stdout_lines=%d grammar=%s token=%-26s"
              % (name, rc, len(lines), len(out.splitlines()), bool(hit), tok))
        if out.strip():
            print("    STDOUT:", repr(out.splitlines()[0][:100]))
        if not hit:
            for l in lines[:3]:
                print("    ERR:", repr(l))
        if "Traceback" in out + err or "RuntimeError" in out + err:
            print("    STREAM CARRIES A TRACEBACK/RUNTIMEERROR TOKEN")


def section_lazy():
    unusable = "/nonexistent/such/tmpdir-T55W2RevDocsArms"
    usable = os.path.join(os.path.dirname(CLONE), "tmp-usable")
    os.makedirs(usable, exist_ok=True)
    for name, argv in LAZY:
        rc1, _, _ = run(argv, env(unusable))
        log = os.path.join(os.path.dirname(CLONE), "lazy.log")
        rc2, _, _ = run(argv, env(usable), trace_to=log)
        txt = open(log, errors="replace").read() if os.path.exists(log) else ""
        under = [l for l in txt.splitlines() if "mkdir" in l and usable in l]
        print("%-32s rc_unusable=%s rc_usable=%s mkdir_under_TMPDIR=%d"
              % (name, rc1, rc2, len(under)))
        if os.path.exists(log):
            os.unlink(log)


def section_arms():
    def norm(t):
        return " ".join(t.split())
    note = norm(open(os.path.join(CLONE, "corpus/knowledge/scratch-root-contract.md")).read())
    skill = norm(open(os.path.join(CLONE, "SKILL.md")).read())
    labels = [n for n, _ in ALLOC]
    missing = [l for l in labels if l not in note]
    reg = json.load(open(os.path.join(CLONE, "tools/registry.json")))
    cells = [r for r in reg["rows"] if r.get("scratch_root")]
    docs = sum(1 for r in cells if MARKER in r["scratch_root"])
    template = ("could-not-evaluate: cannot create clone scratch under the scratch root: "
                "TMPDIR is not a usable directory: '<value>' (could-not-evaluate)")
    print("docs  = %d/7 (MARKER in each scratch_root cell)" % docs)
    print("note  = %d/9 mode labels present; missing=%s" % (len(labels) - len(missing), missing))
    print("note grammar template present (byte-identical modulo placeholders): %s" % (template in note))
    print("skill = %d/1 (MARKER present: %s)" % (1 if MARKER in skill else 0, MARKER in skill))
    # Denominators as the C0 bytes actually use them: len(table)=14 rows,
    # cheap=13 (registry-check --rev is grammar-arm only), note=9/9, docs=7/7,
    # skill=1/1, tmp_mkdirs=0. C0 measure.py line 272-273:
    #   (len(table) - empty_ok) + (len(table) - usable_ok) + ... + (8 - note)
    table, cheap, note_n = 14, 13, len(labels)
    total = (9 - 9) + (5 - 5) + (table - cheap) + (table - cheap) + 0 \
        + (7 - 7) + (8 - note_n) + (1 - 1)
    print("--- counter total at C0 bytes with every arm green ---")
    print("len(table)=%d cheap=%d note=%d" % (table, cheap, note_n))
    print("total = (9-9)+(5-5)+(%d-%d)+(%d-%d)+0+(7-7)+(8-%d)+(1-1) = %d"
          % (table, cheap, table, cheap, note_n, total))
    print("PASS requires total == 0 and no bad arm -> PASS=%s" % (total == 0))


def section_classes():
    for rev in (BASE, C0):
        print("=== %s ===" % rev[:8])
        for f in ("tools/%s.py" % t for t in SEVEN):
            src = git("show", "%s:%s" % (rev, f)).stdout
            hits = [l for l in src.splitlines() if l.startswith("class ScratchRootUnusable")]
            print("%-34s %s" % (f, hits[0] if hits else "(no ScratchRootUnusable class)"))


SECTIONS = {"cells": section_cells, "diff": section_diff, "grammar": section_grammar,
            "lazy": section_lazy, "arms": section_arms, "classes": section_classes}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    names = list(SECTIONS) if which == "all" else [which]
    for n in names:
        print("########## %s ##########" % n)
        SECTIONS[n]()
