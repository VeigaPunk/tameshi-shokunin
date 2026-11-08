#!/usr/bin/env python3
"""T92M1 — mutation probe of the round-92 C1 counter (measure-v92.py, A3 bytes).

Pre-registered defect spec: T92M1-defects.txt (written before any run). This
driver applies each defect as ONE edit to the frozen counter bytes, recomputes
the SELF_SHA256 line for the edited bytes (the self-pin is a seal against drift,
not a defence against a deliberate mutation study), builds the battery state
that must expose the defect, and runs the FROZEN counter and the MUTANT counter
on the SAME state clone and rev with separate --work dirs.

Score: KILLED iff the two receipts differ (exit code or stdout); SURVIVED iff
byte-identical; INCONCLUSIVE iff the frozen baseline on that state does not show
the pre-registered refusal (a baseline failure is never a killed mutant).

Nothing in the lane, the fleet repo or .ufo/evidence is written: every state is
a `git clone --shared` under --scratch, committed under ctl <ctl@fixture.invalid>.

Usage: python3 T92M1-mutants.py --defects T92M1-defects.txt --scratch DIR --out DIR
                               [--jobs N] [--only M01 ...]
Exit: 0 the probe ran (see the matrix for verdicts); 2 harness precondition failed.
"""
import argparse
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "84904d41a31fb5ddde49e8bf1ad6fc2b489671a0"          # A3 instrument
BASE = "63172b9889475103aeca976d37389d204010dd11"          # spec absent here
COUNTER_PATH = ".ufo/evidence/round-92/c1/measure-v92.py"
SPEC_PATH = ".ufo/evidence/round-92/c1/census-mutants.json"
NOTE = "corpus/knowledge/mutation-case-fleet-sources-census.md"
README = "corpus/README.md"
SOURCES = "corpus/SOURCES.md"
RAW_SHA = "be5a9221b36983d6c45e983c398ee9c9c088b374d36fb17e2ae67f50ad749ea9"
NORM_SHA = "723562ed5b20e1a914d9addbce9007b8edf1c962c8237592dbac3b39e5509c2c"
PIN_RE = re.compile(rb'^SELF_SHA256 = "[0-9a-f]{64}"\n', re.M)
GATE_SHA = "3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30"
GATE_COMMIT = "f47ad6ba8d306f8125597401cb2ce45c1297a593"
TRIVIAL_NEW = ('function symbolic(s) { return s ~ /^[A-Za-z][A-Za-z0-9 _-]*$/ ')
CONJ_KEYS = ("selfpin", "pin", "spec", "green", "canary", "invalid0", "trivial0",
             "inconclusive0", "unstable0", "note", "ids", "mismatched0", "figure",
             "witnessed", "source", "coverage", "n_min")


def sh(a, cwd=None, check=True, stdin=None):
    p = subprocess.run(a, cwd=cwd, capture_output=True, text=True, input=stdin)
    if check and p.returncode != 0:
        raise SystemExit("cmd failed: %s\n%s" % (" ".join(a), p.stderr))
    return p


def blob_bytes(rev, path):
    p = subprocess.run(["git", "-C", LANE, "cat-file", "blob", rev + ":" + path],
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None


def blob(rev, path):
    b = blob_bytes(rev, path)
    return None if b is None else b.decode()


# ---------------------------------------------------------------- defect spec

def parse_defects(path):
    txt = open(path, encoding="utf-8").read()
    blocks = re.split(r"(?m)^### ", txt)[1:]
    out = {}
    for b in blocks:
        head, rest = b.split("\n", 1)
        parts = [x.strip() for x in head.split("|")]
        mid, check = parts[0], parts[1]
        state = re.search(r"state=(\S+)", head).group(1)
        expect = re.search(r"expect=(\S+)", head).group(1)
        old = re.search(r"(?ms)^--- OLD\n(.*?)^--- NEW\n", rest).group(1)
        new = re.search(r"(?ms)^--- NEW\n(.*?)^--- END\n", rest).group(1)
        out[mid] = dict(id=mid, check=check, state=state, expect=expect,
                        old=old.rstrip("\n"), new=new.rstrip("\n"))
    return out


def build_mutants(base_bytes, defects):
    mutants = {}
    for mid, d in defects.items():
        txt = base_bytes.decode()
        n = txt.count(d["old"])
        if n != 1:
            raise SystemExit("precondition: %s anchor occurs %d times" % (mid, n))
        mut = txt.replace(d["old"], d["new"], 1)
        raw = mut.encode()
        norm = PIN_RE.sub(b"", raw)
        pin = hashlib.sha256(norm).hexdigest()
        b = PIN_RE.sub(('SELF_SHA256 = "%s"\n' % pin).encode(), raw, count=1)
        if hashlib.sha256(PIN_RE.sub(b"", b)).hexdigest() != pin:
            raise SystemExit("precondition: %s recomputed pin does not verify" % mid)
        if b == base_bytes:
            raise SystemExit("precondition: %s is a no-op" % mid)
        mutants[mid] = dict(bytes=b, pin=pin,
                            sha=hashlib.sha256(b).hexdigest(),
                            diff="".join(difflib.unified_diff(
                                txt.splitlines(True), mut.splitlines(True),
                                "frozen", mid, n=1)))
    return mutants


# ---------------------------------------------------------------- states

def flip_verdict_cells(note):
    out, n = [], 0
    for line in note.split("\n"):
        if re.match(r"^\| C\d\d \|", line):
            if "| KILLED |" in line:
                line = line.replace("| KILLED |", "| SURVIVED |", 1)
                n += 1
            elif "| SURVIVED |" in line:
                line = line.replace("| SURVIVED |", "| KILLED |", 1)
                n += 1
        out.append(line)
    if n != 12:
        raise SystemExit("precondition: flipped %d note rows, wanted 12" % n)
    return "\n".join(out)


def replace_row(note, cid, newrow):
    out, n = [], 0
    for line in note.split("\n"):
        if line.startswith("| %s |" % cid):
            line = newrow
            n += 1
        out.append(line)
    if n != 1:
        raise SystemExit("precondition: row %s matched %d times" % (cid, n))
    return "\n".join(out)


def sub_once(text, old, new, label):
    if text.count(old) != 1:
        raise SystemExit("precondition: %s anchor occurs %d times" % (label, text.count(old)))
    return text.replace(old, new, 1)


def spec_json(text, fn):
    s = json.loads(text)
    fn(s)
    return json.dumps(s, indent=1, ensure_ascii=False) + "\n"


def build_states():
    note = blob(REV, NOTE)
    spec = blob(REV, SPEC_PATH)
    readme = blob(REV, README)
    sources = blob(REV, SOURCES)
    inverted = flip_verdict_cells(note)
    src_queued = []
    hit = 0
    for line in sources.split("\n"):
        c = [x.strip() for x in re.sub(r"^ {0,3}", "", line).split("|")]
        if len(c) >= 13 and c[1] == "S320":
            line = sub_once(line, "| mined |", "| queued |", "S320 status")
            hit += 1
        src_queued.append(line)
    if hit != 1:
        raise SystemExit("precondition: S320 row matched %d times" % hit)

    S = {}

    def add(name, expect, files=None, drop=(), replace_note=None, raw=False,
            rev=REV, counter_append="", work_prefilled=False):
        S[name] = dict(name=name, files=files or {}, drop=list(drop), expect=expect,
                       replace_note=replace_note, raw=raw, rev=rev,
                       counter_append=counter_append, work_prefilled=work_prefilled)

    add("honest", expect={"__pass": True})
    add("figure-denominator",
        files={NOTE: sub_once(note, "measured: 5/12 killed", "measured: 5/13 killed", "figure")},
        expect={"cond": {"figure": False}})
    add("source-queued", files={SOURCES: "\n".join(src_queued)},
        expect={"cond": {"source": False}})
    add("coverage-row-gone",
        files={README: "\n".join(l for l in readme.split("\n")
                                 if "knowledge/mutation-case-fleet-sources-census.md" not in l)},
        expect={"cond": {"coverage": False}})
    add("witness-same",
        files={SPEC_PATH: sub_once(spec, "| 1234567 |", "| no |", "C02 witness")},
        expect={"cond": {"witnessed": False}})
    add("pin-mismatch", files={SPEC_PATH: sub_once(spec, GATE_SHA, "0" * 64, "gate sha")},
        expect={"cond": {"pin": False}})
    add("spec-edit", files={SPEC_PATH: sub_once(spec, '"timeout_s": 180',
                                                '"timeout_s": 181', "timeout_s")},
        expect={"cond": {"spec": False}})
    add("gate-commit-bogus", files={SPEC_PATH: sub_once(spec, GATE_COMMIT, "0" * 40, "gate commit")},
        expect={"__setup": "gate-blob-unreadable"})
    add("note-inverted", files={NOTE: inverted}, expect={"cond": {"mismatched0": False}})
    add("noop-mutant", files={SPEC_PATH: sub_once(spec, "length(teaches)<7",
                                                  "length(teaches)<8", "C02 new")},
        expect={"cond": {"invalid0": False}})
    add("trivial-mutant",
        files={SPEC_PATH: spec_json(spec, lambda s: [m for m in s["mutants"]
                                                     if m["id"] == "C10"][0].update(new=TRIVIAL_NEW))},
        expect={"cond": {"trivial0": False}})
    add("note-absent", drop=[NOTE], expect={"cond": {"note": False, "ids": False}})
    add("spec-11", files={SPEC_PATH: spec_json(spec, lambda s: s["mutants"].pop())},
        expect={"cond": {"n_min": False}})
    add("header-2", files={NOTE: note + "\n| id | arm | edit | verdict | witness |\n"
                                          "|---|---|---|---|---|\n"},
        expect={"cond": {"ids": False}})
    add("c13-row", files={NOTE: note + "\n| C13 | fixture arm | fixture edit | differs |\n"},
        expect={"cond": {"ids": False}})
    add("unkeyed-row", files={NOTE: note + "\n| appended | fixture arm | fixture edit | KILLED | differs |\n"},
        expect={"cond": {"ids": False}})
    add("two-token",
        files={NOTE: replace_row(note, "C12",
                                 "| C12 | fixture arm | fixture edit | SURVIVED | KILLED |")},
        expect={"cond": {"ids": False}})
    add("dup-row", files={NOTE: note + "\n| C02 | fixture arm | fixture edit | SURVIVED | differs |\n"},
        expect={"cond": {"ids": False}})
    add("replace-honest", expect={"__setup": "replace-refs-present"}, replace_note=inverted)
    add("selfpin-edit", raw=True, rev=BASE, counter_append="\n# post-freeze edit (never committed)\n",
        expect={"__setup": "self-pin-mismatch"})
    add("work-not-empty", raw=True, rev=BASE, work_prefilled=True,
        expect={"__setup": "work-not-empty-dir"})
    add("spec-absent", raw=True, rev=BASE, expect={"__setup": "spec-absent-at-rev"})
    add("fleet-replace", files={SPEC_PATH: spec},
        expect={"__setup": "replace-refs-present:fleet"})
    # batch-3 state: the battery has no timeout control; a 1 ms oracle timeout is the
    # one state that can falsify inconclusive0 without touching the pinned gate bytes.
    add("timeout", files={SPEC_PATH: sub_once(spec, '"timeout_s": 180',
                                              '"timeout_s": 0.001', "timeout_s")},
        expect={"cond": {"inconclusive0": False}})
    return S


MUTANT_STATE = {
    "M01": "selfpin-edit", "M02": "spec-edit", "M03": "pin-mismatch",
    "M04": "replace-honest", "M05": "gate-commit-bogus", "M06": "work-not-empty",
    "M07": "header-2", "M08": "c13-row", "M09": "unkeyed-row", "M10": "two-token",
    "M11": "dup-row", "M12": "figure-denominator", "M13": "source-queued",
    "M14": "coverage-row-gone", "M15": "witness-same", "M16": "note-inverted",
    "M17": "noop-mutant", "M18": "trivial-mutant", "M19": "honest",
    "M20": "honest", "M21": "note-absent", "M22": "spec-11",
    "M23": "honest", "M24": "honest", "M25": "honest", "M26": "figure-denominator",
    "M27": "figure-denominator", "M28": "honest",
    "M29": "spec-absent", "M30": "fleet-replace",
}
# a second, hostile state for the canary mutant: the canary input is state-independent
EXTRA_STATES = {"M25": "pin-mismatch", "M19": "timeout"}


# ---------------------------------------------------------------- execution

def prepare_fleet_clone(scratch):
    d = tempfile.mkdtemp(dir=scratch, prefix="fleet-")
    dest = os.path.join(d, "fleet")
    sh(["git", "clone", "-q", "--shared", "--no-checkout",
        "/home/vgpnk/Projects/shokunin", dest])
    top = sh(["git", "-C", dest, "rev-parse", "--show-toplevel"]).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(dest):
        raise SystemExit("precondition: fleet clone toplevel mismatch " + dest)
    if sh(["git", "-C", dest, "replace", "-l"]).stdout.strip():
        raise SystemExit("precondition: fleet clone already carries replace refs")
    parent = sh(["git", "-C", dest, "rev-parse", GATE_COMMIT + "~1"]).stdout.strip()
    sh(["git", "-C", dest, "replace", GATE_COMMIT, parent])
    if not sh(["git", "-C", dest, "replace", "-l"]).stdout.strip():
        raise SystemExit("precondition: fleet clone replace ref did not land")
    return dest


def make_state_repo(state, scratch):
    if state["raw"]:
        return LANE, state["rev"]
    d = tempfile.mkdtemp(dir=scratch, prefix="st-" + state["name"] + "-")
    dest = os.path.join(d, "repo")
    sh(["git", "clone", "-q", "--shared", "--no-checkout", LANE, dest])
    top = sh(["git", "-C", dest, "rev-parse", "--show-toplevel"]).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(dest):
        raise SystemExit("precondition: clone toplevel mismatch " + dest)
    sh(["git", "-C", dest, "sparse-checkout", "set", "--no-cone", "corpus/",
        ".ufo/evidence/round-92/c1/"])
    sh(["git", "-C", dest, "checkout", "-q", "--detach", REV])
    dirty = sh(["git", "-C", dest, "status", "--porcelain"]).stdout.strip()
    if dirty:
        raise SystemExit("precondition: sparse checkout left a dirty tree: " + dirty[:200])
    for path, text in state["files"].items():
        fp = os.path.join(dest, path)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write(text)
    for path in state["drop"]:
        fp = os.path.join(dest, path)
        if os.path.exists(fp):
            os.unlink(fp)
    sh(["git", "-C", dest, "add", "-A"])
    changed = sh(["git", "-C", dest, "diff", "--cached", "--name-only"]).stdout.split()
    allowed = set(state["files"]) | set(state["drop"])
    if set(changed) != allowed:
        raise SystemExit("precondition: state %s staged unexpected paths: %s"
                         % (state["name"], sorted(set(changed) ^ allowed))[:300])
    sh(["git", "-C", dest, "-c", "user.name=ctl", "-c", "user.email=ctl@fixture.invalid",
        "commit", "-q", "--allow-empty", "-m", "t92m1 state " + state["name"]])
    rev = sh(["git", "-C", dest, "rev-parse", "HEAD"]).stdout.strip()
    if state["replace_note"] is not None:
        false_oid = sh(["git", "-C", dest, "hash-object", "-w", "--stdin"],
                       stdin=state["replace_note"]).stdout.strip()
        true_oid = sh(["git", "-C", dest, "rev-parse", "HEAD:" + NOTE]).stdout.strip()
        sh(["git", "-C", dest, "replace", true_oid, false_oid])
    return dest, rev


def run_counter(counter_path, repo, rev, work, scratch, work_prefilled=False):
    if work_prefilled:
        open(os.path.join(work, "occupied.txt"), "w").write("t92m1: the work dir is not empty\n")
    env = dict(os.environ)
    env.update(HOME=scratch, TMPDIR=os.path.join(scratch, "tmp"))
    t0 = time.time()
    p = subprocess.run([sys.executable, "-I", counter_path, "--repo", repo, "--rev", rev,
                        "--work", work], capture_output=True, text=True, env=env, timeout=2400)
    return dict(exit=p.returncode, out=p.stdout, err=p.stderr, secs=round(time.time() - t0, 1))


def receipt_sha(r):
    return hashlib.sha256(("%d\n" % r["exit"]).encode() + r["out"].encode()).hexdigest()


def conjuncts(out):
    for line in out.split("\n"):
        if line.startswith("C1_CONJUNCTS "):
            d = {}
            for kv in line.split()[1:]:
                k, v = kv.split("=")
                d[k] = (v == "true")
            return d
    return {}


def check_baseline(state, r):
    e = state["expect"]
    if "__pass" in e:
        return r["exit"] == 0 and "C1_R92_PASS=true" in r["out"], "pass"
    if "__setup" in e:
        return ("C1_SETUP " + e["__setup"]) in r["out"] and r["exit"] == 2, e["__setup"]
    c = conjuncts(r["out"])
    ok = r["exit"] != 0 and "C1_R92_PASS=false" in r["out"]
    for k, v in e["cond"].items():
        ok = ok and c.get(k) is v
    return ok, ",".join("%s=%s" % (k, v) for k, v in e["cond"].items())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--defects", required=True, nargs="+")
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    scratch = os.path.realpath(a.scratch)
    outdir = os.path.realpath(a.out)
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(os.path.join(scratch, "tmp"), exist_ok=True)

    base = blob_bytes(REV, COUNTER_PATH)
    if base is None:
        raise SystemExit("precondition: counter absent at " + REV)
    base_bytes = base
    if hashlib.sha256(base_bytes).hexdigest() != RAW_SHA:
        raise SystemExit("precondition: frozen counter raw sha256 differs")
    if hashlib.sha256(PIN_RE.sub(b"", base_bytes)).hexdigest() != NORM_SHA:
        raise SystemExit("precondition: frozen counter pin-normalized sha256 differs")

    defects, origin = {}, {}
    for fn in a.defects:
        for mid, dd in parse_defects(fn).items():
            dd["spec"] = os.path.basename(fn)
            defects[mid] = dd
            origin[mid] = os.path.basename(fn)
    mutants = build_mutants(base_bytes, defects)
    frozen = os.path.join(scratch, "frozen-counter.py")
    open(frozen, "wb").write(base_bytes)
    mdir = os.path.join(scratch, "mutants")
    os.makedirs(mdir, exist_ok=True)
    for mid, m in mutants.items():
        open(os.path.join(mdir, mid + ".py"), "wb").write(m["bytes"])

    states = build_states()
    used = sorted({MUTANT_STATE[m] for m in defects})
    if a.only:
        sel = [m for m in sorted(defects) if m in a.only]
        used = sorted({MUTANT_STATE[m] for m in sel} | {EXTRA_STATES[m] for m in sel if m in EXTRA_STATES})
    else:
        sel = sorted(defects)

    t0 = time.time()
    print("T92M1_MUTANT_BASE sha256=%s pin=%s mutants=%d states=%d jobs=%d"
          % (RAW_SHA, NORM_SHA, len(defects), len(used), a.jobs), flush=True)

    if "fleet-replace" in used:
        fclone = prepare_fleet_clone(scratch)
        st = states["fleet-replace"]
        st["files"][SPEC_PATH] = spec_json(st["files"][SPEC_PATH],
                                           lambda sp: sp["gate"].update(repo=fclone))
        print("T92M1_FLEET_REPLACE_CLONE " + fclone, flush=True)
    repos = {n: make_state_repo(states[n], scratch) for n in used}
    print("T92M1_STATES_READY " + " ".join("%s=%s" % (n, repos[n][1][:12]) for n in used), flush=True)

    jobs = []

    def submit(counter_path, state_name, work_prefilled, tag):
        repo, rev = repos[state_name]
        work = tempfile.mkdtemp(dir=os.path.join(scratch, "tmp"), prefix="w-" + tag + "-")
        state = states[state_name]
        cp = counter_path
        if state["counter_append"]:
            cp = os.path.join(scratch, "tmp", "cnt-" + tag + ".py")
            open(cp, "wb").write(open(counter_path, "rb").read() + state["counter_append"].encode())
        return dict(tag=tag, state=state_name, counter=cp, repo=repo, rev=rev, work=work,
                    work_prefilled=work_prefilled)

    for n in used:
        jobs.append(submit(frozen, n, states[n]["work_prefilled"], "base:" + n))
    for mid in sel:
        for st in ([MUTANT_STATE[mid]] + ([EXTRA_STATES[mid]] if mid in EXTRA_STATES else [])):
            jobs.append(submit(os.path.join(mdir, mid + ".py"), st,
                               states[st]["work_prefilled"], "mut:%s:%s" % (mid, st)))

    results = {}

    def worker(j):
        r = run_counter(j["counter"], j["repo"], j["rev"], j["work"], scratch, j["work_prefilled"])
        r.update(tag=j["tag"], state=j["state"], rev=j["rev"], sha=receipt_sha(r))
        return r

    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for r in ex.map(worker, jobs):
            results[r["tag"]] = r
            print("T92M1_RUN %-28s state=%-20s exit=%d secs=%s sha=%s"
                  % (r["tag"], r["state"], r["exit"], r["secs"], r["sha"][:16]), flush=True)

    # ---- scoring
    lines, matrix, inconclusive = [], [], []
    rows = []
    for mid in sel:
        st = MUTANT_STATE[mid]
        b = results["base:" + st]
        m = results["mut:%s:%s" % (mid, st)]
        bok, why = check_baseline(states[st], b)
        if not bok:
            verdict, detail = "INCONCLUSIVE", "baseline on %s did not show %s" % (st, why)
        elif m["exit"] != b["exit"] or m["out"] != b["out"]:
            verdict = "KILLED"
            d = [l for l in difflib.unified_diff(b["out"].split("\n"), m["out"].split("\n"),
                                                 "frozen", mid, n=0, lineterm="") if l[:1] in "+-" and l[:3] not in ("---", "+++")]
            detail = "exit %d->%d; %s" % (b["exit"], m["exit"], " | ".join(d[:3])
                                           or "stdout identical, exit code differs")
            if m["err"] and not b["err"]:
                detail += " | stderr-only: " + m["err"].strip().split("\n")[-1][:120]
        else:
            verdict, detail = "SURVIVED", "receipt byte-identical"
        rows.append((mid, defects[mid]["state"], defects[mid]["expect"], verdict, detail, b, m, st))

    # second exposure for the canary mutant
    extra = {}
    for mid, st in EXTRA_STATES.items():
        if mid not in sel:
            continue
        b, m = results["base:" + st], results["mut:%s:%s" % (mid, st)]
        extra[mid] = ("SURVIVED" if (b["exit"] == m["exit"] and b["out"] == m["out"]) else "KILLED", st)

    killed = sum(1 for r in rows if r[3] == "KILLED")
    survived = [r[0] for r in rows if r[3] == "SURVIVED"]
    inc = [r[0] for r in rows if r[3] == "INCONCLUSIVE"]

    rep = []
    rep.append("T92M1 mutation matrix — frozen counter sha256 %s (pin-normalized %s)" % (RAW_SHA, NORM_SHA))
    rep.append("states built from lane rev %s; base rev %s for the setup probes" % (REV, BASE))
    rep.append("defect specs: " + ", ".join(os.path.basename(f) for f in a.defects))
    rep.append("score = frozen receipt vs mutant receipt on the SAME state clone and rev")
    rep.append("")
    rep.append("%-5s %-20s %-9s %-12s %s" % ("id", "state", "expect", "verdict", "evidence"))
    for mid, st, exp, verdict, detail, b, m, stn in rows:
        rep.append("%-5s %-20s %-9s %-12s %s" % (mid, st, exp, verdict, detail))
    rep.append("")
    rep.append("T92M1_MUTANT_VERDICT killed=%d/%d survived=%d inconclusive=%d"
               % (killed, len(rows), len(survived), len(inc)))
    if survived:
        rep.append("T92M1_SURVIVORS " + ",".join(survived))
    if inc:
        rep.append("T92M1_INCONCLUSIVE " + ",".join(inc))
    for mid, (v, st) in sorted(extra.items()):
        rep.append("T92M1_EXTRA %s state=%s verdict=%s" % (mid, st, v))

    # baselines: the frozen receipt every mutant was compared against
    rep.append("")
    rep.append("## frozen baselines (the receipt a mutant must differ from)")
    for n in used:
        b = results["base:" + n]
        ok, why = check_baseline(states[n], b)
        rep.append("")
        rep.append("### baseline state=%s rev=%s expect=%s ok=%s sha=%s"
                   % (n, b["rev"][:12], states[n]["expect"], ok, b["sha"]))
        rep.append(b["out"].rstrip("\n"))
        if b["err"].strip():
            rep.append("[stderr] " + b["err"].strip().split("\n")[-1][:200])

    # mutant receipts: only the changed lines (the rest is the baseline above)
    rep.append("")
    rep.append("## mutant receipts (diff vs the frozen baseline of the same state)")
    for mid, st, exp, verdict, detail, b, m, stn in rows:
        rep.append("")
        rep.append("### %s state=%s verdict=%s receipt_sha=%s mutant_sha=%s pin=%s"
                   % (mid, st, verdict, m["sha"], mutants[mid]["sha"], mutants[mid]["pin"]))
        rep.append(mutants[mid]["diff"].rstrip("\n"))
        d = list(difflib.unified_diff(b["out"].split("\n"), m["out"].split("\n"),
                                      "frozen/" + st, mid, n=1, lineterm=""))
        if d:
            rep.extend(d)
        else:
            rep.append("(receipt byte-identical)")
        if m["err"].strip() and not b["err"].strip():
            rep.append("[mutant stderr tail] " + m["err"].strip().split("\n")[-1][:300])

    # restore evidence
    restored = os.path.join(scratch, "restored-counter.py")
    open(restored, "wb").write(base_bytes)
    rsha = hashlib.sha256(open(restored, "rb").read()).hexdigest()
    rw = tempfile.mkdtemp(dir=os.path.join(scratch, "tmp"), prefix="w-restored-")
    if "honest" not in repos:
        repos["honest"] = make_state_repo(states["honest"], scratch)
    repo, rev = repos["honest"]
    rr = run_counter(restored, repo, rev, rw, scratch)
    rr["sha"] = receipt_sha(rr)
    if "base:honest" in results:
        bh = results["base:honest"]
    else:
        bw = tempfile.mkdtemp(dir=os.path.join(scratch, "tmp"), prefix="w-honestbase-")
        bh = run_counter(frozen, repo, rev, bw, scratch)
        bh["sha"] = receipt_sha(bh)
    rep.append("")
    rep.append("## restoration")
    rep.append("restored bytes sha256=%s (frozen=%s) equal=%s" % (rsha, RAW_SHA, rsha == RAW_SHA))
    rep.append("restored run on state=honest exit=%d receipt_sha=%s baseline_receipt_sha=%s equal=%s"
               % (rr["exit"], rr["sha"], bh["sha"], rr["sha"] == bh["sha"]))
    rep.append("")
    rep.append("wall_secs=%d" % (time.time() - t0))

    body = "\n".join(rep)
    open(os.path.join(outdir, "T92M1-mutants.out"), "w", encoding="utf-8").write(body + "\n")
    open(os.path.join(outdir, "T92M1-matrix.tsv"), "w", encoding="utf-8").write(
        "\n".join("\t".join(x) for x in
                  [("id", "state", "expect", "verdict", "evidence", "frozen_sha", "mutant_sha")] +
                  [(mid, st, exp, v, d, b["sha"], m["sha"]) for mid, st, exp, v, d, b, m, _ in rows]
                  ) + "\n")
    print(body)
    sys.exit(0)


if __name__ == "__main__":
    main()
