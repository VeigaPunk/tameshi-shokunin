#!/usr/bin/env python3
"""T91M1 — mutation probe for the sealed round-91 C1 counter.

Reads the frozen counter .ufo/evidence/round-91/c1/measure-v91.py, applies ONE
single-edit defect at a time (the frozen list is repeated verbatim from
T91M1-defects.txt), and evaluates each mutated counter against the committed
round-91 C1 control battery reproduced by a scratch copy of controls-v91.py.

The scratch copy of the controls driver differs from the frozen file in exactly
two lines: the measure path and the receipt outdir are taken from
T91_MEASURE / T91_OUTDIR, so this probe never writes into the frozen
.ufo/evidence/round-91/pre-freeze/controls/ directory.

Kill rule (from T91M1-defects.txt): a defect is KILLED iff at least one control
whose frozen receipt is not PASS=true now prints C1_R91_PASS=true. CTL14-pos
must keep passing (recorded as pos_ok).

Modes:
  --prepare   write + compile the mutated counter copies, print their hashes
  --run       run every battery (or --only ID ...), logs under SCRATCH/battery
  --summarize print/write the per-defect control matrix
  --all       prepare + run + summarize

Everything lives under /fast/scratch/hyaku/tameshi-r91/T91M1/ unless --scratch
is given; nothing outside the scratch dir and the wave deliverable is written.
"""
import argparse, hashlib, json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
TARGET = os.path.join(LANE, ".ufo/evidence/round-91/c1/measure-v91.py")
CONTROLS = os.path.join(LANE, ".ufo/evidence/round-91/c1/controls-v91.py")
FROZEN_RECEIPTS = os.path.join(LANE, ".ufo/evidence/round-91/pre-freeze/controls")
EXPECTED_HEAD = "584bbe3ca78fdb9188214b0a3de22caf6ffeb2e4"
POSITIVE = "CTL14-pos"
DEFAULT_SCRATCH = "/fast/scratch/hyaku/tameshi-r91/T91M1"

# Two literal patches that make the frozen driver parameterisable. Each must
# occur exactly once in controls-v91.py; no other line is changed.
DRIVER_PATCHES = [
    ('measure = os.path.join(lane, ".ufo/evidence/round-91/c1/measure-v91.py")',
     'measure = os.environ.get("T91_MEASURE", os.path.join(lane, ".ufo/evidence/round-91/c1/measure-v91.py"))'),
    ('outdir = os.path.join(lane, ".ufo/evidence/round-91/pre-freeze/controls")',
     'outdir = os.environ.get("T91_OUTDIR", os.path.join(lane, ".ufo/evidence/round-91/pre-freeze/controls"))'),
]

DEFECTS = [
    dict(id="D01", check="replace-list gate (lane) refuses non-empty git replace -l",
         old='        if p.stdout.strip():\n            die("replace-refs-present:" + label)\n',
         new='        if p.stdout.strip():\n            pass\n',
         predict="SURVIVED (V4-replace still refused by sealed reads / source=false)"),
    dict(id="D02", check="sealed git env carries GIT_NO_REPLACE_OBJECTS=1",
         old='"GIT_NO_REPLACE_OBJECTS": "1"', new='"GIT_NO_REPLACE_OBJECTS": "0"',
         predict="SURVIVED (replace-list gate still refuses V4-replace)"),
    dict(id="D03", check="pristine gate is green on two runs",
         old='green_runs = [selftest(gp, work, to) for _ in range(2)]',
         new='green_runs = [selftest(gp, work, to) for _ in range(1)]',
         predict="SURVIVED (no control state exercises green)"),
    dict(id="D04", check="exit-97 canary gate",
         old='canary = selftest(cgp, work, to)[0] == 97', new='canary = True',
         predict="SURVIVED (canary is constant across control states)"),
    dict(id="D05", check="figure: compare both K and N of measured: K/N killed",
         old='figure_ok = len(heads) == 1 and int(heads[0][0]) == killed and int(heads[0][1]) == n',
         new='figure_ok = len(heads) == 1 and int(heads[0][1]) == n',
         predict="KILLED by CTL3-figure"),
    dict(id="D06", check="figure: compare K only",
         old='figure_ok = len(heads) == 1 and int(heads[0][0]) == killed and int(heads[0][1]) == n',
         new='figure_ok = len(heads) == 1 and int(heads[0][0]) == killed',
         predict="SURVIVED (CTL3-figure also changes K)"),
    dict(id="D07", check="note verdicts must match derived verdicts",
         old='mism = sum(1 for r in rows if note_rows.get(r["id"]) != r["derived"])',
         new='mism = 0',
         predict="KILLED by CTL2-flip"),
    dict(id="D08", check="duplicate id row refuses the note",
         old='        if cid in rows:\n            ambiguous.append(cid)\n            continue\n',
         new='        if cid in rows:\n            continue\n',
         predict="KILLED by VOV1-dup-row, VOV3-draft-column"),
    dict(id="D09", check="out-of-vocabulary verdict cell refuses the note",
         old='        if v not in ("KILLED", "SURVIVED"):\n            ambiguous.append(cid)\n            continue\n',
         new='        if v not in ("KILLED", "SURVIVED"):\n            continue\n',
         predict="KILLED by VOV3-draft-column"),
    dict(id="D10", check="note id set must equal the spec id set",
         old='ids_ok = (len(ambiguous) == 0) and sorted(note_rows) == sorted(ids)',
         new='ids_ok = len(ambiguous) == 0',
         predict="SURVIVED (CTL4-ids also flips mismatched0)"),
    dict(id="D11", check="mutant spec bytes pinned to SPEC_SHA",
         old='spec_pinned = hashlib.sha256(spec_bytes).hexdigest() == SPEC_SHA',
         new='spec_pinned = True',
         predict="KILLED by CTL5-spec"),
    dict(id="D12", check="gate blob pinned to the spec sha256",
         old='pin = hashlib.sha256(gate_bytes).hexdigest() == g["sha256"]',
         new='pin = True',
         predict="SURVIVED (CTL12-pin also flips spec=false)"),
    dict(id="D13", check="mutant edit must be unique and non-noop (invalid0)",
         old='invalid0=invalid == 0,', new='invalid0=True,',
         predict="SURVIVED (invalid-flipping controls also edit the spec)"),
    dict(id="D14", check="mutant validate run must not fail trivially (trivial0)",
         old='trivial0=trivial == 0,', new='trivial0=True,',
         predict="SURVIVED (trivial-flipping controls also edit the spec)"),
    dict(id="D15", check="no-op mutant counts as invalid",
         old='        if m["new"] == m["old"]:\n            inv.append("noop")\n',
         new='        if False:\n            inv.append("noop")\n',
         predict="SURVIVED (CTL6-noop also edits the spec)"),
    dict(id="D16", check="witness must actually differ",
         old='            witness = "differs" if (p1[0], p1[1]) != (p2[0], p2[1]) else "same"',
         new='            witness = "differs"',
         predict="SURVIVED (CTL9-equiv also edits the spec)"),
    dict(id="D17", check="timeout derives INCONCLUSIVE, not SURVIVED",
         old='            verdicts.append("INCONCLUSIVE" if rc is None else ("SURVIVED" if rc == 0 else "KILLED"))',
         new='            verdicts.append("SURVIVED" if rc is None or rc == 0 else "KILLED")',
         predict="SURVIVED (no control produces a timeout)"),
    dict(id="D18", check="fenced code blocks are skipped by the note parser",
         old='        if line.startswith("```"):\n            in_fence = not in_fence\n            continue\n',
         new='        if line.startswith("```"):\n            continue\n',
         predict="SURVIVED (no control note carries fenced rows)"),
    dict(id="D19", check="at least 12 mutants (n_min)",
         old='n_min=n >= N_MIN)', new='n_min=True)',
         predict="SURVIVED (no control shrinks the mutant list without editing the spec)"),
    dict(id="D20", check="note cites a mined S318 registry row naming the note",
         old='    ids_ok = figure_ok = source_ok = False\n    mism = 0\n',
         new='    ids_ok = figure_ok = False\n    source_ok = True\n    mism = 0\n',
         predict="KILLED by CTL10-source, CTL16-oldsource"),
    dict(id="D21", check="README carries a row naming the note",
         old='    coverage_ok = any(l.lstrip().startswith("|") and "knowledge/mutation-case-fleet-sources-census.md" in l\n                      for l in readme.split("\\n"))',
         new='    coverage_ok = True',
         predict="KILLED by CTL15-coverage"),
]
BY_ID = {d["id"]: d for d in DEFECTS}


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sh(argv, cwd=None, env=None, timeout=None):
    p = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0:
        raise SystemExit("command failed (%d): %s\n%s" % (p.returncode, " ".join(argv), p.stderr[-4000:]))
    return p.stdout


def frozen_controls():
    names = sorted(f[:-4] for f in os.listdir(FROZEN_RECEIPTS)
                   if f.endswith(".out") and f.startswith(("CTL", "VOV", "V4")))
    return names


def frozen_expected(control):
    """PASS value in the frozen receipt (true / false); None when unreadable."""
    path = os.path.join(FROZEN_RECEIPTS, control + ".out")
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("C1_R91_PASS="):
                return line.split("=", 1)[1].strip()
    return None


def make_driver(scratch):
    src = open(CONTROLS, encoding="utf-8").read()
    for old, new in DRIVER_PATCHES:
        if src.count(old) != 1:
            raise SystemExit("driver patch anchor is not unique: " + old)
        src = src.replace(old, new, 1)
    dst = os.path.join(scratch, "controls-probe.py")
    with open(dst, "w", encoding="utf-8") as f:
        f.write(src)
    os.chmod(dst, 0o755)
    return dst


def prepare(scratch):
    base = open(TARGET, encoding="utf-8").read()
    target_sha = sha(TARGET)
    root = os.path.join(scratch, "mut")
    shutil.rmtree(root, ignore_errors=True)
    rows = []
    for d in DEFECTS:
        n = base.count(d["old"])
        if n != 1:
            raise SystemExit("%s: old snippet occurs %d times" % (d["id"], n))
        mut = base.replace(d["old"], d["new"], 1)
        md = os.path.join(root, d["id"])
        os.makedirs(md)
        mp = os.path.join(md, "measure.py")
        with open(mp, "w", encoding="utf-8") as f:
            f.write(mut)
        os.chmod(mp, 0o755)
        subprocess.run([sys.executable, "-m", "py_compile", mp], check=True,
                       capture_output=True, text=True)
        msha = sha(mp)
        if msha == target_sha:
            raise SystemExit(d["id"] + ": mutation did not change bytes")
        rows.append(dict(id=d["id"], check=d["check"], predict=d["predict"],
                         mutated=mp, sha_target=target_sha, sha_mutant=msha,
                         old=d["old"], new=d["new"]))
        print("%s %s -> %s" % (d["id"], target_sha[:16], msha[:16]))
    driver = make_driver(scratch)
    snap = os.path.join(scratch, "lane")
    if not os.path.isdir(snap):
        sh(["git", "clone", "-q", "--shared", LANE, snap])
    top = sh(["git", "-C", snap, "rev-parse", "--show-toplevel"]).strip()
    if os.path.realpath(top) != os.path.realpath(snap):
        raise SystemExit("snapshot toplevel mismatch")
    head = sh(["git", "-C", snap, "rev-parse", "HEAD"]).strip()
    if head != EXPECTED_HEAD:
        # The lane may have advanced since the pre-freeze battery; the snapshot
        # is pinned to the state the frozen receipts reproduce.
        sh(["git", "-C", snap, "checkout", "-q", "--detach", EXPECTED_HEAD])
        head = sh(["git", "-C", snap, "rev-parse", "HEAD"]).strip()
    if head != EXPECTED_HEAD:
        raise SystemExit("lane snapshot HEAD %s != spec-frozen %s" % (head, EXPECTED_HEAD))
    dirty = sh(["git", "-C", snap, "status", "--porcelain"]).strip()
    if dirty:
        raise SystemExit("lane snapshot is dirty:\n" + dirty)
    manifest = dict(scratch=scratch, target=TARGET, sha_target=target_sha,
                    controls_driver=driver, sha_controls_driver=sha(driver),
                    sha_controls_frozen=sha(CONTROLS),
                    lane_snapshot=snap, lane_head=head,
                    corpus_sha=dict(S=sha(os.path.join(snap, "corpus/SOURCES.md")),
                                    R=sha(os.path.join(snap, "corpus/README.md")),
                                    N=sha(os.path.join(snap, "corpus/knowledge/mutation-case-fleet-sources-census.md"))),
                    frozen_controls={c: frozen_expected(c) for c in frozen_controls()},
                    defects=rows)
    with open(os.path.join(scratch, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
        f.write("\n")
    print("prepared %d mutants; driver %s; snapshot %s" % (len(rows), sha(driver)[:16], head))
    return manifest


def run_battery(scratch, did, kind="full", jobs=3, timeout=5400):
    d = BY_ID[did]
    mp = os.path.join(scratch, "mut", did, "measure.py")
    outdir = os.path.join(scratch, "out", did if kind == "full" else did + "-" + kind)
    ctl = os.path.join(scratch, "ctl", did if kind == "full" else did + "-" + kind)
    shutil.rmtree(outdir, ignore_errors=True)
    shutil.rmtree(ctl, ignore_errors=True)
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(ctl, exist_ok=True)
    env = dict(os.environ)
    env["T91_MEASURE"] = mp
    env["T91_OUTDIR"] = outdir
    argv = [sys.executable, "-I", os.path.join(scratch, "controls-probe.py"),
            "--lane", os.path.join(scratch, "lane"), "--scratch", ctl,
            "--jobs", str(jobs)]
    if kind != "full":
        argv += ["--only", kind]
    log = os.path.join(scratch, "battery", did + ".log")
    os.makedirs(os.path.dirname(log), exist_ok=True)
    with open(log, "w", encoding="utf-8") as f:
        f.write("cmd=" + " ".join(argv) + "\n")
        f.flush()
        try:
            p = subprocess.run(argv, env=env, stdout=f, stderr=subprocess.STDOUT,
                               timeout=timeout)
            rc = p.returncode
        except subprocess.TimeoutExpired:
            f.write("\nBATTERY TIMEOUT\n")
            rc = None
    return did, rc, log


def run_all(scratch, only, concurrency, jobs, timeout):
    ids = only or [d["id"] for d in DEFECTS]
    with ThreadPoolExecutor(concurrency) as ex:
        futs = [ex.submit(run_battery, scratch, i, "full", jobs, timeout) for i in ids]
        for f in futs:
            did, rc, log = f.result()
            print("%s battery_rc=%s log=%s" % (did, rc, log))


def read_receipt(scratch, did, control):
    path = os.path.join(scratch, "out", did, control + ".out")
    if not os.path.isfile(path):
        return dict(control=control, pass_=None, exit=None, conjuncts=None, raw="MISSING")
    txt = open(path, encoding="utf-8", errors="replace").read()
    pass_ = None
    exit_ = None
    conj = None
    for line in txt.split("\n"):
        if line.startswith("C1_R91_PASS="):
            pass_ = line.split("=", 1)[1].strip()
        elif line.startswith("exit="):
            try:
                exit_ = int(line.split("=", 1)[1])
            except ValueError:
                pass_
        elif line.startswith("C1_CONJUNCTS "):
            conj = line[len("C1_CONJUNCTS "):]
    return dict(control=control, pass_=pass_, exit=exit_, conjuncts=conj, raw=txt)


def summarize(scratch):
    controls = frozen_controls()
    expected = {c: frozen_expected(c) for c in controls}
    result = dict(sha_target=sha(TARGET), controls=expected, defects={})
    for d in DEFECTS:
        did = d["id"]
        rows = {c: read_receipt(scratch, did, c) for c in controls}
        killed_by = [c for c in controls if c != POSITIVE and rows[c]["pass_"] == "true"]
        pos = rows.get(POSITIVE, {}).get("pass_")
        result["defects"][did] = dict(check=d["check"], predict=d["predict"],
                                      killed_by=killed_by, pos_ok=(pos == "true"),
                                      pos_pass=pos,
                                      rows={c: dict(pass_=rows[c]["pass_"], exit=rows[c]["exit"],
                                                    conjuncts=rows[c]["conjuncts"])
                                            for c in controls})
        print("%s %-6s killed_by=%s pos_ok=%s" % (
            did, "KILLED" if killed_by else "SURVIVED",
            ",".join(killed_by) or "-", result["defects"][did]["pos_ok"]))
    with open(os.path.join(scratch, "results.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    # Evidence file: every C1_CONJUNCTS / C1_R91_PASS / C1_SETUP line, per control.
    with open(os.path.join(scratch, "receipts.txt"), "w", encoding="utf-8") as f:
        for did in [d["id"] for d in DEFECTS]:
            f.write("### %s\n" % did)
            for c in controls:
                r = read_receipt(scratch, did, c)
                f.write("## %s exit=%s\n" % (c, r["exit"]))
                for line in r["raw"].split("\n"):
                    if line.startswith(("C1_CONJUNCTS ", "C1_R91_PASS=", "C1_SETUP")):
                        f.write(line + "\n")
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", default=DEFAULT_SCRATCH)
    ap.add_argument("--mode", choices=["prepare", "run", "summarize", "all"], default="all")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--concurrency", type=int, default=6)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=5400)
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    if a.mode in ("prepare", "all"):
        prepare(a.scratch)
    if a.mode in ("run", "all"):
        run_battery_preflight(a.scratch)
        run_all(a.scratch, a.only, a.concurrency, a.jobs, a.timeout)
    if a.mode in ("summarize", "all"):
        summarize(a.scratch)


def run_battery_preflight(scratch):
    for p in (os.path.join(scratch, "controls-probe.py"), os.path.join(scratch, "lane"),
              os.path.join(scratch, "manifest.json")):
        if not os.path.exists(p):
            raise SystemExit("missing preparation output: " + p)


if __name__ == "__main__":
    main()
