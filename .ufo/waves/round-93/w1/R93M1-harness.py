#!/usr/bin/env python3
"""R93M1 mutation harness — 30 single-edit defects + the plan's D01-D05.

Read-only on the lane: it clones the lane at the instrument revision into
/fast/scratch/hyaku/tameshi-r93/R93M1, materialises a committed battery state the
way controls-v93.py does, commits it under the fixture identity
ctl <ctl@fixture.invalid>, and runs the mutated counter (extracted from --rev's
object store, never the working tree) on that clone with --rev HEAD.

The fixture states and the grading function are imported from the battery driver
of record (sha256 400d8e0f...da74) so the semantics are the committed battery's.

Usage:
  python3 R93M1-harness.py --dry     # static: assert anchors, print mutant digests
  python3 R93M1-harness.py --run     # execute the matrix, write receipts + table
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "855f0c1c59ee2af7f184d8de62d02cdd576eb94e"
CTRL = os.path.join(LANE, ".ufo/evidence/round-93/c1/controls-v93.py")
S = "/fast/scratch/hyaku/tameshi-r93/R93M1"
PRISTINE = os.path.join(S, "measure-v93.pristine.py")
OUTDIR = os.path.join(S, "receipts")
LOG = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-93/w1/R93M1-output.txt"
SELF_LINE = re.compile(rb'^SELF_SHA256 = "[0-9a-f]{64}"\n', re.M)
DRIVER_SHA = "400d8e0ffceadc3e9aa7d057ac16b5142f0f4b60626544133462b1067bc0da74"
STATE_INPUTS = ("corpus/knowledge/mutation-case-fleet-sources-census.md",
                "corpus/lessons/round-93.md", "corpus/SOURCES.md",
                "corpus/README.md", ".ufo/evidence/round-93/c1/census-mutants.json")


def sha_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def verify_inputs():
    """The harness must be re-runnable from committed bytes, not from a drifted tree."""
    d = sha_file(CTRL)
    if d != DRIVER_SHA:
        raise SystemExit("DRIVER_DRIFT " + d)
    for p in STATE_INPUTS:
        wt = sha_file(os.path.join(LANE, p))
        rv = hashlib.sha256(subprocess.run(
            ["git", "-C", LANE, "cat-file", "blob", REV + ":" + p],
            capture_output=True, check=True).stdout).hexdigest()
        if wt != rv:
            raise SystemExit("INPUT_DRIFT " + p + " wt=" + wt + " rev=" + rv)
    print("INPUTS driver_sha=" + d + " state_inputs=rev-identical")


def load_driver():
    spec = importlib.util.spec_from_file_location("controls_v93", CTRL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def recompute_pin(path):
    b = open(path, "rb").read()
    norm = SELF_LINE.sub(b"", b)
    h = hashlib.sha256(norm).hexdigest()
    open(path, "wb").write(SELF_LINE.sub(('SELF_SHA256 = "%s"\n' % h).encode(), b, count=1))
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


# id, old, new, detector state (None => exposure probe on pos-real), detector?
DEFECTS = [
 ("D01", '''    selfpin = self_pin_ok()
    if not selfpin:
        die("self-pin-mismatch")''', '''    selfpin = True''', "selfpin-edit*", True),
 ("D02", '''                       "gate_sha256": gate_sha, "fixtures": g.get("fixtures")}''',
  '''                       "fixtures": g.get("fixtures")}''', "pins-mutated", True),
 ("D03", '''    spec_ok = (len(spec.get("mutants", [])) == N_MIN and len(spec_ids) == N_MIN''',
  '''    spec_ok = (len(spec.get("mutants", [])) == N_MIN''', "spec-shape", True),
 ("D04", '''    pin = gate_sha == g.get("sha256")''', '''    pin = True''', "pin-mismatch", True),
 ("D05", '''    green = all(r[0] == 0 and b"selftest ok" in r[1] for r in green_runs)''',
  '''    green = True''', "timeout", True),
 ("D06", '''    canary = selftest(cgp, work, to)[0] == 97''', '''    canary = True''',
  "pos-real", False),
 ("D07", "valid0=invalid == 0", "valid0=True", "noop-mutant", True),
 ("D08", "trivial0=trivial == 0", "trivial0=True", "trivial-mutant", True),
 ("D09", "inconclusive0=inconclusive == 0", "inconclusive0=True", "timeout", True),
 ("D10", '''    runs = int(spec.get("runs_per_verdict", 2))''', '''    runs = 1''',
  "pos-real", False),
 ("D11", "note=note is not None", "note=True", "note-absent", True),
 ("D12", '''    vtables_ok = info["verdict_tables"] == 1''',
  '''    vtables_ok = info["verdict_tables"] >= 1''', "hidden-c001", True),
 ("D13", '''        toks = [c for c in split_cells(raw) if c in VERDICTS]
        if toks:
            bad.append("stray-verdict:%d:%s" % (oi + 1, raw.strip()[:24]))''',
  '''        pass  # residual: stray-verdict scan removed''', "renamed-result", True),
 ("D14", '''            if first not in spec_ids:
                bad.append("out-of-set:%d:%s" % (ln + 1, first[:24]))
                continue''', '''            pass  # residual: out-of-set rule removed''', "hidden-c001", True),
 ("D15", '''            if first in rows:
                bad.append("dup:%d:%s" % (ln + 1, first))
                continue''', '''            pass  # residual: duplicate rule removed''', "dup-row", True),
 ("D16", '''            if len(toks) != 1 or vcol >= len(cells) or cells[vcol] not in VERDICTS:
                bad.append("position:%d:%s" % (ln + 1, first))
                continue''', '''            pass  # residual: position rule removed''', "position", True),
 ("D17", '''            if len(cells) != len(header):
                bad.append("width:%d:cells=%d" % (ln + 1, len(cells)))
                continue''', '''            pass  # residual: width row rule removed''', "pos-real", False),
 ("D18", '''        if delim and len(delim) != len(header):
            bad.append("width:%d:header=%d,delimiter=%d" % (oi + 1, len(header), len(delim)))''',
  '''        pass  # residual: width delimiter rule removed''', "pos-real", False),
 ("D19", '''    ids_ok = (note is not None and not bad and set(note_rows) == spec_ids)''',
  '''    ids_ok = (note is not None and not bad)  # residual: id-set equality removed''',
  "hidden-c001", True),
 ("D20", '''        figure_ok = len(heads) == 1 and int(heads[0][0]) == killed and int(heads[0][1]) == n''',
  '''        figure_ok = True''', "figure", True),
 ("D21", "witnessed=witnessed == survived", "witnessed=True", "witness-same", True),
 ("D22", '''        quote_ok = any(norm_text(q) in text for q in quotes.get(sid, []))''',
  '''        quote_ok = bool(quotes.get(sid))  # residual: occurrence-in-snapshot removed''',
  "source-noquote", True),
 ("D23", "n_min=n >= N_MIN", "n_min=True", "short-spec", True),
 ("D24", '''        if line.lstrip().startswith("|") and "knowledge/mutation-case-fleet-sources-census.md" in line:
            last_row = line''',
  '''        if line.lstrip().startswith("|") and "knowledge/mutation-case-fleet-sources-census.md" in line and last_row is None:
            last_row = line''', "coverage-denial", True),
 ("D25", '''DENIAL_TOKENS = ("not admitted", "not-admitted", "uncertified", "withdrawn", "refused",
                 "rejected")''', '''DENIAL_TOKENS = ()  # residual: denial list emptied''',
  "coverage-denial", True),
 ("D26", '''        figure_ok = len(heads) == 1 and int(heads[0][0]) == killed and int(heads[0][1]) == n''',
  '''        figure_ok = len(heads) >= 1 and int(heads[0][0]) == killed and int(heads[0][1]) == n''',
  "figure", True),
 ("D27", '''            if len(c) >= 13 and c[1] == sid and c[8] == "mined" and LESSON_PATH in c[11]:''',
  '''            if len(c) >= 13 and c[1] == sid and c[8] in ("mined", "queued") and LESSON_PATH in c[11]:''',
  "source-status", True),
 ("D28", '''    spec_ok = (len(spec.get("mutants", [])) == N_MIN and len(spec_ids) == N_MIN''',
  '''    spec_ok = (len(spec_ids) == N_MIN''', "short-spec", True),
 ("D29", '''            if m:
                fence = (m.group(1)[0], len(m.group(1)))
                continue''', '''            if m:
                vis.append((idx, raw))''', "pos-real", False),
 ("D30", '''        if len(vcols) != 1:''',
  '''        if False:  # residual: two-verdict-column rule removed''', "pos-real", False),
]


def mutants(pristine_text):
    out = []
    for mid, old, new, state, det in DEFECTS:
        assert pristine_text.count(old) == 1, "anchor %s count=%d" % (mid, pristine_text.count(old))
        out.append(dict(id=mid, old=old, new=new, text=pristine_text.replace(old, new, 1),
                        state=state, detector=det))
    return out


def write_mutant(text, label):
    p = os.path.join(S, "mutants", "counter-%s.py" % label)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(text)
    sha = recompute_pin(p)
    norm = SELF_LINE.sub(b"", open(p, "rb").read())
    return p, sha, hashlib.sha256(norm).hexdigest()


def run_job(job):
    """job: dict(label, state, expect, detector, counter_path or special)."""
    label = job["label"]
    try:
        return _run_job(job)
    except BaseException as e:  # keep one flaky clone from losing the matrix
        with open(os.path.join(OUTDIR, label + ".error"), "w", encoding="utf-8") as f:
            f.write("%s: %s\n" % (type(e).__name__, e))
        return dict(label=label, state=job.get("state", "?"), exit=-1,
                    body="JOB-ERROR %s: %s" % (type(e).__name__, e),
                    run_body="JOB-ERROR", grade=False, stderr="", receipt="error")


def _run_job(job):
    label = job["label"]
    d = tempfile.mkdtemp(dir=os.path.join(S, "jobs"), prefix="fx-" + label + "-")
    try:
        if job.get("special") == "selfpin-edit":
            repo, rev = LANE, REV
            work = os.path.join(d, "work")
            cp = job["counter"]
        else:
            repo = D.clone_at(LANE, REV, os.path.join(d, "repo"))
            top = D.sh("git", "-C", repo, "rev-parse", "--show-toplevel").strip()
            assert os.path.realpath(top) == os.path.realpath(repo), "toplevel %s" % repo
            D.materialize_state(repo, STATES[job["state"]])
            D.sh("git", "-C", repo, "add", "-A")
            D.sh("git", "-C", repo, "-c", "user.name=ctl", "-c", "user.email=ctl@fixture.invalid",
                 "commit", "-q", "--allow-empty", "-m", "r93m1 " + label)
            top = D.sh("git", "-C", repo, "rev-parse", "--show-toplevel").strip()
            assert os.path.realpath(top) == os.path.realpath(repo), "toplevel-after-commit"
            rev = "HEAD"
            cp = job["counter"]
            work = os.path.join(d, "work")
        p = subprocess.run([sys.executable, "-I", cp, "--repo", repo, "--rev", rev,
                            "--work", work], cwd=d, capture_output=True, text=True, timeout=1800)
        body = "job=%s state=%s counter_sha=%s exit=%d\n" % (
            label, job["state"], hashlib.sha256(open(cp, "rb").read()).hexdigest(), p.returncode)
        body += p.stdout + p.stderr
        rp = D.receipt_path(OUTDIR, label)
        with open(rp, "w", encoding="utf-8") as f:
            f.write(body)
        grade = D.grade(label, p.returncode, body, job["expect"])
        return dict(label=label, state=job["state"], exit=p.returncode, body=body,
                    run_body=p.stdout + p.stderr, grade=grade, stderr=p.stderr[-400:],
                    receipt=os.path.basename(rp))
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--jobs", type=int, default=10)
    a = ap.parse_args()
    global D, STATES
    D = load_driver()
    os.makedirs(os.path.join(S, "jobs"), exist_ok=True)
    os.makedirs(OUTDIR, exist_ok=True)
    verify_inputs()
    pristine = open(PRISTINE, "rb").read()
    ptext = pristine.decode()
    M = mutants(ptext)
    plan = D.mutant_edits(ptext)
    plan_m = []
    for name in sorted(plan):
        text, state = plan[name]
        plan_m.append(dict(id="P" + name[1:], old="(driver)", new="(driver)", text=text,
                           state=state, detector=True))
    print("PRISTINE sha256", hashlib.sha256(pristine).hexdigest(),
          "normalised", hashlib.sha256(SELF_LINE.sub(b"", pristine)).hexdigest())
    print("DEFECTS", len(M), "PLAN", len(plan_m))
    if a.dry:
        for m in M + plan_m:
            p, sha, norm = write_mutant(m["text"], m["id"])
            print(m["id"], "state=%-14s detector=%d" % (m["state"], m["detector"]),
                  "sha256", sha, "norm", norm)
        return
    assert a.run, "use --dry or --run"
    # detector-state baseline expectations: take the committed battery's own expect rows
    STATES = D.states(LANE)
    jobs = []
    base_states = sorted({m["state"] for m in M + plan_m if m["state"] != "selfpin-edit*"})
    for st in base_states:
        jobs.append(dict(label="base-" + st, state=st, expect=STATES[st]["expect"],
                         detector=True, counter=PRISTINE))
    jobs.append(dict(label="base-selfpin-edit", state="selfpin-edit",
                     expect=(2, {"__setup": "self-pin-mismatch"}), detector=True,
                     counter=os.path.join(S, "selfpin-edit.py"), special="selfpin-edit"))
    for m in M + plan_m:
        p, sha, norm = write_mutant(m["text"], m["id"])
        if m["state"] == "selfpin-edit*":
            pe = os.path.join(S, "selfpin-edit-mut-%s.py" % m["id"])
            open(pe, "w").write(m["text"] + "\n# post-freeze edit (never committed)\n")
            # the pin line was computed before the appended comment: selfpin must fail
            jobs.append(dict(label="mut-" + m["id"], state="selfpin-edit",
                             expect=(2, {"__setup": "self-pin-mismatch"}), detector=True,
                             counter=pe, special="selfpin-edit"))
        else:
            want = (0, {"__pass": True}) if m["id"].startswith("P") else STATES[m["state"]]["expect"]
            jobs.append(dict(label="mut-" + m["id"], state=m["state"], expect=want,
                             detector=m["detector"], counter=p))
    open(os.path.join(S, "selfpin-edit.py"), "w").write(
        pristine.decode() + "\n# post-freeze edit (never committed)\n")
    # provenance: the frozen bytes never move
    pre = hashlib.sha256(pristine).hexdigest()
    with ThreadPoolExecutor(max_workers=min(a.jobs, len(jobs))) as ex:
        res = list(ex.map(run_job, jobs))
    post_blob = subprocess.run(["git", "-C", LANE, "cat-file", "blob",
                                REV + ":.ufo/evidence/round-93/c1/measure-v93.py"],
                               capture_output=True).stdout
    result = {r["label"]: r for r in res}
    lines = ["R93M1 mutation matrix — receipts index",
             "pristine_sha256 " + pre,
             "pristine_sha256_after %s (file) %s (git blob at rev)" % (
                 hashlib.sha256(open(PRISTINE, "rb").read()).hexdigest(),
                 hashlib.sha256(post_blob).hexdigest()),
             ""
             "label state exit grade pass_line"]
    for r in sorted(res, key=lambda x: x["label"]):
        lines.append("%-24s %-14s %d %-7s %-18s %s" % (
            r["label"], r["state"], r["exit"], "MATCH" if r["grade"] else "MISMATCH",
            r.get("receipt", "?"),
            "C1_R93_PASS=true" if "C1_R93_PASS=true" in r["body"] else "-"))
    lines.append("")
    lines.append("per-defect verdicts")
    k = 0
    runnable = 0
    for m in M:
        base = result["base-" + ("selfpin-edit" if m["state"] == "selfpin-edit*" else m["state"])]
        mut = result["mut-" + m["id"]]
        base_ok, mut_ok = base["grade"], mut["grade"]
        if base_ok and m["detector"]:
            runnable += 1
            v = "SURVIVED" if mut_ok else "KILLED"
            k += 1 if v == "KILLED" else 0
        else:
            v = "INCONCLUSIVE"
        delta = "identical" if base["run_body"] == mut["run_body"] else "differs"
        lines.append("%s state=%-14s base=%-7s mut=%-7s verdict=%-12s delta=%s mut_exit=%d" % (
            m["id"], m["state"], "MATCH" if base_ok else "FAIL",
            "MATCH" if mut_ok else "MISMATCH", v, delta, mut["exit"]))
    lines.append("")
    lines.append("plan removal mutants (expect PASS=true: the cheat returns)")
    for m in plan_m:
        base = result["base-" + m["state"]]
        mut = result["mut-" + m["id"]]
        lines.append("P%s state=%-14s frozen_exit=%d frozen_pass=%s mutant_exit=%d mutant_pass=%s load_bearing=%s" % (
            m["id"][1:], m["state"], base["exit"],
            "true" if "C1_R93_PASS=true" in base["body"] else "false",
            mut["exit"], "true" if "C1_R93_PASS=true" in mut["body"] else "false",
            "YES" if mut["grade"] else "NO"))
    lines.append("VERDICT killed:%d/%d inconclusive:%d" % (
        k, runnable, len(M) - runnable))
    out = "\n".join(lines) + "\n"
    open(LOG, "w", encoding="utf-8").write(out)
    print(out)


if __name__ == "__main__":
    main()
