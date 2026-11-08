#!/usr/bin/env python3
"""R95E4 — reproduce and classify the twelve round-94 rule-level survivors
against the round-95 C1 instrument.

READ-ONLY on the lane. Everything writable lives under $R95E4_SCRATCH
(default /fast/scratch/hyaku/tameshi-r95/R95E4/study).

For every survivor row in R95E4-defects.txt (the twelve rows copied verbatim
from R94M1-defects.txt):
  1. build a scratch instrument revision: clone the lane at HEAD into scratch,
     copy the frozen v95 counter/spec/pins/sources in, add the round-95 lesson
     and the S320-S323 SOURCES rows the counter's `source` conjunct reads, and
     commit inside the clone only (identity ctl <ctl@fixture.invalid>);
  2. materialize the battery state paired with the rule (rules from
     controls-v95.py states()); PLUS the supplementary isolation probes built
     here (P05/P09/P10/P13/P15/P16/P20/P26/P29/P30/P32) that try to make the
     rule's value move the verdict;
  3. run the PRISTINE v95 counter on that state and grade it with the battery's
     own pre-registered expectation (baseline);
  4. write the single-edit mutant (SELF_SHA256 recomputed, as the round-94
     driver did for all twelve), run it on the same state, grade it the same;
  5. restore the exact pristine bytes, verify the sha256, re-run, and compare
     byte-identical stdout with the baseline;
  6. record the exit codes, moved conjuncts and verdict.

The classification (killed-by / subsumed / invariant-pinned / ungraded) is
assigned after this driver's raw evidence exists; this script records the
mechanical facts and never fabricates one.

Usage: python3 -I R95E4-driver.py [--jobs N] [--only ID ...] [--keep]
Exit 0 when every row produced a verdict.
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
HEAD = "0d3fc99b36a8ea1f18356066425ecdb56fdad748"
C95 = LANE + "/.ufo/evidence/round-95/c1"
COUNTER_PATH = ".ufo/evidence/round-95/c1/measure-v95.py"
CONTROLS = C95 + "/controls-v95.py"
W1 = LANE + "/.ufo/waves/round-95/w1"
SPEC_FILE = W1 + "/R95E4-defects.txt"
SCRATCH = os.environ.get("R95E4_SCRATCH", "/fast/scratch/hyaku/tameshi-r95/R95E4/study")
INSTR = os.path.join(SCRATCH, "instrument")
SOURCE = INSTR          # repo the state clones and the revtree are read from
TREE_PATHS = ["corpus/knowledge/mutation-case-fleet-sources-census.md", "corpus/README.md",
              "corpus/SOURCES.md", "corpus/lessons/round-95.md",
              ".ufo/evidence/round-95/c1/census-mutants.json",
              ".ufo/evidence/round-95/c1/pins.json",
              ".ufo/evidence/round-95/c1/measure-v95.py",
              ".ufo/evidence/round-95/sources/s320.html",
              ".ufo/evidence/round-95/sources/s321.html",
              ".ufo/evidence/round-95/sources/s322.html",
              ".ufo/evidence/round-95/sources/s323.html"]
COPY_IN = [".ufo/evidence/round-95/c1/measure-v95.py",
           ".ufo/evidence/round-95/c1/census-mutants.json",
           ".ufo/evidence/round-95/c1/pins.json",
           ".ufo/evidence/round-95/sources/s320.html",
           ".ufo/evidence/round-95/sources/s321.html",
           ".ufo/evidence/round-95/sources/s322.html",
           ".ufo/evidence/round-95/sources/s323.html"]


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    with open(p, "rb") as f:
        return sha_bytes(f.read())


def sealed_env():
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null"}


def sh(*a, **kw):
    p = subprocess.run(list(a), capture_output=True, text=True, env=sealed_env(), **kw)
    if kw.get("check", True) and p.returncode != 0:
        raise SystemExit("cmd failed: %s\n%s" % (" ".join(a), p.stderr))
    return p.stdout


def assert_toplevel(repo):
    top = sh("git", "-C", repo, "rev-parse", "--show-toplevel").strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise SystemExit("toplevel mismatch: %s != %s" % (top, repo))


def load_controls():
    s = importlib.util.spec_from_file_location("ctl95", CONTROLS)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def read_spec():
    out = []
    with open(SPEC_FILE, encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            d = json.loads(line)
            if "old" in d:
                d.setdefault("edits", [{"old": d["old"], "new": d["new"]}])
            d["line"] = ln
            out.append(d)
    ids = [d["id"] for d in out]
    assert len(ids) == len(set(ids)), "duplicate defect id"
    assert len(out) == 12, "expected 12 survivor rows, got %d" % len(out)
    return out


# ---------------------------------------------------------------- instrument
def build_lesson(dest):
    """Round-95 lesson. Prefer the SC1 draft; else a labelled fixture lesson.

    Only the `## Gate` located quotes are read by the counter's `source`
    conjunct. The fixture is byte-recorded in the receipt header so no reader
    mistakes it for the integrated lesson.
    """
    draft = os.path.join(W1, "SC1-lesson.md")
    if os.path.exists(draft):
        b = open(draft, "rb").read()
        with open(dest, "wb") as f:
            f.write(b)
        return "SC1-lesson.md", sha_bytes(b)
    text = """# Round 95 — lesson (FIXTURE, synthesized by R95E4)

This file is a scratch-clone fixture, not the committed round-95 lesson: it
exists so the v95 counter's `source` conjunct has located quotes to check when
the survivor matrix runs before integration. It claims no measurement.

## Gate

- S320 sha256sum(1) — "Print or check SHA256 (256-bit) checksums."
  (`.ufo/evidence/round-95/sources/s320.html:88`).
- S321 GFM §4.10 Tables — "The table is broken at the first empty line, or beginning of another block-level structure"
  (`.ufo/evidence/round-95/sources/s321.html:4607-4608`).
- S322 CommonMark §4.5 Fenced code blocks — "A fenced code block begins with a code fence, preceded by up to three spaces of indentation."
  (`.ufo/evidence/round-95/sources/s322.html:2732-2733`).
- S323 CommonMark §4.4 Indented code blocks — "An indented code block is composed of one or more indented chunks separated by blank lines."
  (`.ufo/evidence/round-95/sources/s323.html:3019`).

## Mistakes

None measured by this fixture.
"""
    b = text.encode("utf-8")
    with open(dest, "wb") as f:
        f.write(b)
    return "fixture", sha_bytes(b)


def patch_sources(path):
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    out = []
    for l in lines:
        if re.match(r"^\| S32[012] \|", l):
            cells = l.split("|")
            if len(cells) > 12 and "corpus/lessons/round-95.md" not in cells[11]:
                cells[11] = cells[11].rstrip() + ", corpus/lessons/round-95.md "
                l = "|".join(cells)
        out.append(l)
    idx = next(i for i, l in enumerate(out) if l.startswith("| S322 |"))
    s323 = ("| S323 | CommonMark Spec 0.31.2 — Indented code blocks — "
            "https://spec.commonmark.org/0.31.2/ | docs | A | why the round-95 note "
            "reader treats a 4-space-indented line as literal text, not a table row or "
            "the note's figure | §4.4 Indented code blocks, tag-stripped snapshot "
            "`.ufo/evidence/round-95/sources/s323.html` | \"An indented code block is "
            "composed of one or more indented chunks separated by blank lines.\" | mined "
            "| 2026-11-08 | 365d | corpus/lessons/round-95.md |")
    out.insert(idx + 1, s323)
    open(path, "w", encoding="utf-8").write("\n".join(out))


def build_instrument(want_rev=None):
    """Either use a committed lane revision as the instrument, or build a scratch one.

    --rev <lane commit> reads the frozen counter, lesson, spec, pins and sources
    out of the lane's object store (the battery's own discipline). Without it,
    the driver assembles a scratch clone at HEAD with a fixture lesson, for use
    before integration.
    """
    global SOURCE
    if want_rev:
        SOURCE = LANE
        p = subprocess.run(["git", "-C", LANE, "cat-file", "blob",
                            want_rev + ":" + COUNTER_PATH], capture_output=True,
                           env=sealed_env())
        if p.returncode != 0:
            raise SystemExit("counter absent at rev " + want_rev)
        lp = subprocess.run(["git", "-C", LANE, "cat-file", "blob",
                             want_rev + ":corpus/lessons/round-95.md"],
                            capture_output=True, env=sealed_env())
        if lp.returncode != 0:
            raise SystemExit("lesson absent at rev " + want_rev)
        return want_rev, "committed", sha_bytes(lp.stdout)
    SOURCE = INSTR
    if os.path.isdir(INSTR):
        shutil.rmtree(INSTR)
    sh("git", "clone", "-q", "--shared", LANE, INSTR)
    assert_toplevel(INSTR)
    sh("git", "-C", INSTR, "checkout", "-q", "--detach", HEAD)
    for rel in COPY_IN:
        src = os.path.join(LANE, rel)
        dst = os.path.join(INSTR, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
    patch_sources(os.path.join(INSTR, "corpus/SOURCES.md"))
    lesson_kind, lesson_sha = build_lesson(os.path.join(INSTR, "corpus/lessons/round-95.md"))
    sh("git", "-C", INSTR, "add", "-A")
    sh("git", "-C", INSTR, "-c", "user.name=ctl", "-c", "user.email=ctl@fixture.invalid",
       "commit", "-q", "-m", "r95e4 instrument revision")
    assert_toplevel(INSTR)
    rev = sh("git", "-C", INSTR, "rev-parse", "HEAD").strip()
    return rev, lesson_kind, lesson_sha


def extract_revtree(rev, dest):
    os.makedirs(dest, exist_ok=True)
    p = subprocess.run(["git", "-C", SOURCE, "archive", "--format=tar", rev, "--",
                        *TREE_PATHS], capture_output=True, env=sealed_env())
    if p.returncode != 0:
        raise SystemExit("git archive failed: " + p.stderr.decode(errors="replace"))
    subprocess.run(["tar", "-x", "-C", dest], input=p.stdout, check=True)
    missing = [p for p in TREE_PATHS if not os.path.exists(os.path.join(dest, p))]
    assert not missing, missing
    return dest


# ---------------------------------------------------------------- state specs
def pins_text(spec_text, revtree, ctl):
    pins = json.load(open(os.path.join(revtree, ctl.PINS), encoding="utf-8"))
    pins["spec_sha256"] = sha_bytes(spec_text.encode())
    return json.dumps(pins, indent=1) + "\n"


def probe_specs(revtree, ctl):
    """Supplementary isolation states, one per rule the battery does not grade.

    Every fixture is built from the revtree's committed bytes with the battery's
    own helpers (note_text / spec_edit / mut / READY / DERIVED), so the fixture
    shape is the battery's shape plus one targeted change.
    """
    P = {}
    # P13 — an out-of-set id INSIDE the single verdict table (hidden-c001's
    # out-of-set rows sit in a SECOND table, so the table-count rule masks them).
    P["P13-out-of-set-in-table"] = dict(
        files={ctl.NOTE: ctl.note_text() + "| C99 | fixture arm | KILLED | differs |\n"},
        defect="E13", intent="out-of-set row in the single table")
    # P15 — every row's token in the witness column, no duplicate row at all.
    P["P15-position-nodup"] = dict(
        files={ctl.NOTE: ctl.note_text(header="| id | arm | witness | verdict |")},
        defect="E15", intent="verdict token out of the verdict column, no duplicate")
    # P16 — an over-wide, non-duplicate last row carrying TWO verdict tokens.
    P["P16-width-nodup"] = dict(
        files={ctl.NOTE: ctl.note_text(drop="C12")
               + "| C12 | fixture arm | KILLED | KILLED | differs | extra |\n"},
        defect="E16", intent="over-wide remainder row, two verdict tokens, no duplicate")
    # P20 — the figure embedded in a longer visible line.
    P["P20-figure-embed"] = dict(
        files={ctl.NOTE: ctl.note_text().replace(
            "measured: 5/12 killed",
            "The run recorded measured: 5/12 killed overall")},
        defect="E20", intent="measured: embedded in a longer line")
    # P26 — a LAST corpus/README.md row naming a longer path that contains the
    # note path, with a denial token.
    P["P26-coverage-longer-path"] = dict(
        files={ctl.READY: open(os.path.join(revtree, ctl.READY), encoding="utf-8").read()
               + "\n| `knowledge/mutation-case-fleet-sources-census.md.bak` | control: "
                 "not admitted | fixture |\n"},
        defect="E26", intent="last README row names a longer path + denial")
    # P29 — validate on the clean lane hangs; the selftest itself does not.
    old29 = 'TODAY_S=$(iso_epoch "$TODAY") || die "--today not an ISO date: $TODAY"'
    new29 = old29 + '\ncase "$*" in *"/root/c-shokunin") sleep 70;; esac'
    spec29 = ctl.spec_edit(revtree, lambda s: ctl.mut(s, "C01").update(old=old29, new=new29))
    P["P29-validate-timeout"] = dict(
        files={ctl.SPEC: spec29, ctl.PINS: pins_text(spec29, revtree, ctl)},
        defect="E29", intent="C01 validate hangs on the clean-lane path (lrc is None)")
    # P30 — two verdict columns with one token per row, delimiter matching the
    # five-cell header, so the delimiter rule does not mask the column rule.
    def note5():
        out = ["# fixture note", "", "measured: 5/12 killed", "",
               "| id | arm | verdict | verdict | witness |", "|---|---|---|---|---|"]
        for k, v in ctl.DERIVED.items():
            out.append("| %s | fixture arm | %s |  | differs |" % (k, v))
        return "\n".join(out) + "\n"
    P["P30-two-verdict-cols"] = dict(
        files={ctl.NOTE: note5()}, defect="E30",
        intent="two verdict columns, delimiter matches the header")
    # P09/P10 — a deterministic alternating mutant: selftest run 1 exits 0,
    # run 2 exits 1, so two runs derive UNSTABLE and one run derives SURVIVED.
    oldalt = '  froot="$FIX/root"; fail=0'
    newalt = ('  froot="$FIX/root"; fail=0\n'
              '  if [ -e "$HOME/r95-flag" ]; then rm -f "$HOME/r95-flag"; exit 1; '
              'else : > "$HOME/r95-flag"; exit 0; fi')
    spec_alt = ctl.spec_edit(revtree, lambda s: ctl.mut(s, "C02").update(old=oldalt, new=newalt))
    P["P09P10-alternating"] = dict(
        files={ctl.NOTE: ctl.note_text(), ctl.SPEC: spec_alt,
               ctl.PINS: pins_text(spec_alt, revtree, ctl)},
        defect="E09", intent="selftest run 1 exit 0 / run 2 exit 1 on C02 (SURVIVED cell)")
    return P


# ---------------------------------------------------------------- runs
def clone_state(source, rev, dest, files, ctl, drop_note=False):
    ctl.clone_at(source, rev, dest)
    ctl.materialize_state(dest, dict(files=files, drop_note=drop_note))
    ctl.sh("git", "-C", dest, "add", "-A")
    ctl.sh("git", "-C", dest, "-c", "user.name=ctl", "-c", "user.email=ctl@fixture.invalid",
           "commit", "-q", "--allow-empty", "-m", "r95e4 state")
    assert_toplevel(dest)
    return ctl.sh("git", "-C", dest, "rev-parse", "HEAD").strip()


def run_counter(counter, repo, rev):
    work = tempfile.mkdtemp(dir=os.path.join(SCRATCH, "work"), prefix="w-")
    try:
        p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev,
                            "--work", work], capture_output=True, text=True,
                           timeout=2400, stdin=subprocess.DEVNULL)
        return p.returncode, p.stdout + p.stderr
    finally:
        shutil.rmtree(work, ignore_errors=True)


def grade_with(ctl, name, code, out, want):
    try:
        return ctl.grade(name, code, out, want)
    except SystemExit:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=10)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--rev", default=None,
                    help="lane commit holding the frozen v95 instrument")
    a = ap.parse_args()
    for sub in ("states", "mutants", "work", "receipts", "revtree"):
        os.makedirs(os.path.join(SCRATCH, sub), exist_ok=True)
    ctl = load_controls()
    defects = read_spec()
    if a.only:
        defects = [d for d in defects if d["id"] in a.only]

    rev, lesson_kind, lesson_sha = build_instrument(a.rev)
    revtree = extract_revtree(rev, os.path.join(SCRATCH, "revtree"))
    pristine = sh("git", "-C", SOURCE, "cat-file", "blob", rev + ":" + COUNTER_PATH).encode()
    counter_sha = sha_bytes(pristine)
    pristine_text = pristine.decode()
    pristine_path = os.path.join(SCRATCH, "pristine-counter.py")
    with open(pristine_path, "wb") as f:
        f.write(pristine)
    for d in defects:
        for e in d["edits"]:
            n = pristine_text.count(e["old"])
            assert n == 1, "%s anchor occurs %d times: %r" % (d["id"], n, e["old"][:50])
    C = ctl.states(revtree)
    probes = probe_specs(revtree, ctl)

    # ---- states: battery members the rows are paired with, plus every probe
    paired = {d["id"]: d["state"] for d in defects}
    battery_states = {}
    for d in defects:
        battery_states[d["state"]] = C[d["state"]]
    battery_states["spec-shape"] = C["spec-shape"]       # E32 subsumption probe
    battery_states["gate-foreign"] = C["gate-foreign"]   # E05 pin probe
    state_files = {}
    for n, spec in battery_states.items():
        state_files["B:" + n] = dict(files=spec.get("files", {}),
                                     drop_note=spec.get("drop_note", False),
                                     expect=spec["expect"], kind="battery")
    for n, p in probes.items():
        state_files["P:" + n] = dict(files=p["files"], drop_note=False,
                                     expect=None, kind="probe")
    if a.only:
        ids = {d["id"] for d in defects}
        need = {"B:" + d["state"] for d in defects}
        if "E32" in ids:
            need.add("B:spec-shape")
        if "E05" in ids:
            need.add("B:gate-foreign")
        for did, pid in (("E09", "P09P10-alternating"), ("E10", "P09P10-alternating"),
                         ("E13", "P13-out-of-set-in-table"), ("E15", "P15-position-nodup"),
                         ("E16", "P16-width-nodup"), ("E20", "P20-figure-embed"),
                         ("E26", "P26-coverage-longer-path"), ("E29", "P29-validate-timeout"),
                         ("E30", "P30-two-verdict-cols")):
            if did in ids:
                need.add("P:" + pid)
        state_files = {k: v for k, v in state_files.items() if k in need}

    def build_one(key):
        v = state_files[key]
        dest = os.path.join(SCRATCH, "states", key.replace(":", "-"))
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        crev = clone_state(SOURCE, rev, dest, v["files"], ctl, drop_note=v["drop_note"])
        return key, dest, crev

    built = {}
    with ThreadPoolExecutor(max_workers=min(6, max(1, len(state_files)))) as ex:
        for key, dest, crev in ex.map(build_one, sorted(state_files)):
            built[key] = (dest, crev)
    print("INSTRUMENT rev=%s counter_sha=%s lesson=%s/%s" % (
        rev[:12], counter_sha, lesson_kind, lesson_sha[:12]))
    print("STATES " + " ".join("%s=%s" % (k, built[k][1][:10]) for k in sorted(built)))

    # ---- baselines (pristine counter, one per state)
    baselines = {}

    def baseline(key):
        repo, crev = built[key]
        rc, out = run_counter(pristine_path, repo, crev)
        v = state_files[key]
        ok = True if v["expect"] is None else grade_with(ctl, key, rc, out, v["expect"])
        return key, dict(exit=rc, out=out, sha_out=sha_bytes(out.encode()), ok=ok,
                         conj=ctl.conj_of(out), repo=repo, rev=crev)

    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for key, r in ex.map(baseline, sorted(built)):
            baselines[key] = r
    for key in sorted(baselines):
        r = baselines[key]
        print("BASELINE %-28s exit=%d grade=%s" % (
            key, r["exit"], "MATCH" if r["ok"] else "MISMATCH"))

    # ---- main rows + supplementary probes
    def mutant_path(did):
        return os.path.join(SCRATCH, "mutants", did + ".py")

    def make_mutant(d):
        text = pristine_text
        for e in d["edits"]:
            text = text.replace(e["old"], e["new"], 1)
        assert text != pristine_text, d["id"]
        mp = mutant_path(d["id"])
        with open(mp, "w") as f:
            f.write(text)
        ctl.recompute_pin(mp)
        return mp, sha_file(mp)

    def run_row(d, state_key, tag, receipt_name):
        repo, crev = built[state_key]
        mp, msha = make_mutant(d)
        rc, out = run_counter(mp, repo, crev)
        want = state_files[state_key]["expect"]
        ok = True if want is None else grade_with(ctl, d["id"], rc, out, want)
        # restore exact pristine bytes and re-run on the same state
        with open(mp, "wb") as f:
            f.write(pristine)
        rsha = sha_file(mp)
        rc2, out2 = run_counter(pristine_path, repo, crev)
        bl = baselines[state_key]
        restored_same = (sha_bytes(out2.encode()) == bl["sha_out"] and rc2 == bl["exit"])
        base_conj, mconj = bl["conj"], ctl.conj_of(out)
        moved = {k: [base_conj.get(k), mconj.get(k)] for k in sorted(set(base_conj) | set(mconj))
                 if base_conj.get(k) != mconj.get(k)}
        body = ("defect=%s rule=%s tag=%s state=%s state_rev=%s instrument_rev=%s\n"
                "instrument_sha=%s mutant_sha=%s restored_sha=%s pristine_sha=%s\n"
                "lesson=%s lesson_sha=%s\n"
                "edit=%r\n"
                "baseline_exit=%d baseline_grade=%s baseline_sha_out=%s\n"
                "mutant_exit=%d mutant_grade=%s\n"
                "restored_exit=%d restored_matches_baseline=%s\n"
                "expect=%r\nmoved_conjuncts=%r\nbaseline_conjuncts=%r\nmutant_conjuncts=%r\n"
                "--- baseline output ---\n%s\n--- mutant output ---\n%s\n"
                "--- restored output ---\n%s\n") % (
            d["id"], d["rule"], tag, state_key, crev, rev, counter_sha, msha, rsha,
            sha_bytes(pristine), lesson_kind, lesson_sha, d["edits"], bl["exit"],
            "MATCH" if bl["ok"] else ("no-expectation" if want is None else "MISMATCH"),
            bl["sha_out"], rc, "MATCH" if ok else ("no-expectation" if want is None else "MISMATCH"),
            rc2, restored_same, want, moved, base_conj, mconj, bl["out"], out, out2)
        rp = os.path.join(SCRATCH, "receipts", receipt_name + ".out")
        with open(rp, "w") as f:
            f.write(body)
        return dict(id=d["id"], tag=tag, state=state_key, mutant_sha=msha, restored_sha=rsha,
                    baseline_exit=bl["exit"], baseline_ok=bl["ok"], mutant_exit=rc,
                    mutant_ok=ok, moved=moved, base_conj=base_conj, mutant_conj=mconj,
                    restored_same=restored_same, receipt=receipt_name + ".out",
                    expect=want)

    jobs = []
    for d in defects:
        jobs.append((d["id"], "main", lambda d=d: run_row(
            d, "B:" + d["state"], "main", d["id"])))
    probe_map = {
        "E09": "P09P10-alternating", "E10": "P09P10-alternating",
        "E13": "P13-out-of-set-in-table", "E15": "P15-position-nodup",
        "E16": "P16-width-nodup", "E20": "P20-figure-embed",
        "E26": "P26-coverage-longer-path", "E29": "P29-validate-timeout",
        "E30": "P30-two-verdict-cols",
    }
    for d in defects:
        if d["id"] in probe_map:
            pid = probe_map[d["id"]]
            jobs.append((d["id"] + ":" + pid, "probe", lambda d=d, pid=pid: run_row(
                d, "P:" + pid, "probe:" + pid, d["id"] + "-" + pid.split("-")[0])))
        if d["id"] == "E05":
            jobs.append(("E05:gate-foreign", "probe", lambda d=d: run_row(
                d, "B:gate-foreign", "probe:gate-foreign", "E05-gate-foreign")))
        if d["id"] == "E32":
            jobs.append(("E32:spec-shape", "probe", lambda d=d: run_row(
                d, "B:spec-shape", "probe:spec-shape", "E32-spec-shape")))

    results = []
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(fn) for _, _, fn in jobs]
        for f in futs:
            results.append(f.result())
    results.sort(key=lambda r: (r["id"], r["tag"]))
    for r in results:
        print("PROBE %-6s %-22s exit=%d/%d grade=%s moved=%s" % (
            r["id"], r["tag"], r["baseline_exit"], r["mutant_exit"],
            "MATCH" if r["mutant_ok"] else "MISMATCH",
            ",".join("%s %s->%s" % (k, v[0], v[1]) for k, v in r["moved"].items()) or "-"))
    print("ROWS %d main=%d probe=%d" % (
        len(results), sum(r["tag"] == "main" for r in results),
        sum(r["tag"] != "main" for r in results)))

    raw = dict(instrument_rev=rev, instrument_sha=counter_sha,
               lane_head=sh("git", "-C", LANE, "rev-parse", "HEAD").strip(),
               instrument_source=("lane" if SOURCE == LANE else "scratch-clone"),
               lesson=dict(kind=lesson_kind, sha=lesson_sha),
               spec_file=SPEC_FILE, spec_sha=sha_file(SPEC_FILE),
               results=results)
    with open(os.path.join(W1, "R95E4-results.raw.json"), "w") as f:
        json.dump(raw, f, indent=1, sort_keys=True)
        f.write("\n")
    shutil.copytree(os.path.join(SCRATCH, "receipts"),
                    os.path.join(W1, "R95E4-receipts"), dirs_exist_ok=True)
    if not a.keep:
        for name in os.listdir(os.path.join(SCRATCH, "states")):
            shutil.rmtree(os.path.join(SCRATCH, "states", name), ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
