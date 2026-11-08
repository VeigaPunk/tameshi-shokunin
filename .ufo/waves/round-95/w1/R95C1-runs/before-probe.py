#!/usr/bin/env python3
"""R95C1 before-witness probe: run the round-94 counter (extracted at 6a2a1fdd)
on the five round-95 C1 fixtures exactly as plans/round-95.plan.md §Controls
describes them. Read-only on the lane; all fixtures are scratch clones."""
import hashlib, importlib.util, json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "6a2a1fdd"
SCRATCH = "/fast/scratch/hyaku/tameshi-r95/R95C1"
COUNTER_PATH = ".ufo/evidence/round-94/c1/measure-v94.py"
NOTE = "corpus/knowledge/mutation-case-fleet-sources-census.md"
SEALED = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
          "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
          "GIT_CONFIG_GLOBAL": "/dev/null"}


def sh(*a, cwd=None):
    p = subprocess.run(list(a), cwd=cwd, capture_output=True, text=True, env=SEALED)
    if p.returncode != 0:
        raise SystemExit("cmd failed: %s\n%s" % (" ".join(a), p.stderr))
    return p.stdout


def load_driver():
    spec = importlib.util.spec_from_file_location(
        "drv94", os.path.join(LANE, ".ufo/evidence/round-94/c1/controls-v94.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def clone_at(rev, dest):
    sh("git", "clone", "-q", "--shared", "--no-checkout", LANE, dest)
    top = sh("git", "-C", dest, "rev-parse", "--show-toplevel").strip()
    assert os.path.realpath(top) == os.path.realpath(dest), (top, dest)
    sh("git", "-C", dest, "checkout", "-q", "--detach", rev)
    return dest


def commit(repo, name):
    sh("git", "-C", repo, "add", "-A")
    sh("git", "-C", repo, "-c", "user.name=r95-critic", "-c", "user.email=r95-critic@invalid",
       "commit", "-q", "--allow-empty", "-m", "r95 before fixture " + name)
    return sh("git", "-C", repo, "rev-parse", "HEAD").strip()


def run_counter(counter, repo, rev, work):
    os.makedirs(work, exist_ok=True)
    p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev,
                        "--work", work], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def slots(m, drv):
    """fixture name -> (note text, counter transform or None)"""
    base = drv.note_text()
    inv = {k: ("SURVIVED" if v == "KILLED" else "KILLED") for k, v in drv.DERIVED.items()}
    ind_table = "\n".join(["    | id | arm | verdict | witness |",
                           "    |---|---|---|---|"] +
                          ["    | %s | fixture arm | %s | differs |" % (k, inv[k])
                           for k in drv.DERIVED])
    s1 = base + "\n" + ind_table + "\n\n    measured: 99/12 killed\n"
    s2 = base + "\n    | C01 | KILLED |\n"
    # s3a: the round-94 fixture shape, witness cell last: raw `C:\\` + the row's
    # trailing boundary pipe.
    s3a = base.replace("| C01 | fixture arm | KILLED | differs |",
                       "| C01 | fixture arm | KILLED | differs C:\\\\|", 1)
    # s3b: witness cell NOT last: header id|arm|witness|verdict, so the boundary
    # after `C:\\` is the interior witness/verdict delimiter (the only shape in
    # which the v94 escape rule merges two cells and moves the verdict).
    rows = ["source: S316/S321 fixture note (positive control only)", "",
            "# fixture note", "", "measured: 5/12 killed", "",
            "| id | arm | witness | verdict |", "|---|---|---|---|"]
    for k, v in drv.DERIVED.items():
        w = "differs C:\\\\" if k == "C01" else "differs"
        rows.append("| %s | fixture arm | %s| %s |" % (k, w, v))
    s3b = "\n".join(rows) + "\n"
    s4 = base.replace("|---|---|---|---|", "|--|--|--|--|", 1)
    return {
        "pos-fixture": (base, None),
        "indent-code-row": (s1, None),
        "indent-token": (s2, None),
        "escaped-backslash-pipe-trailing": (s3a, None),
        "escaped-backslash-pipe-interior": (s3b, None),
        "two-hyphen-delimiter": (s4, None),
        "double-pin": (None, "double-pin"),
    }


def double_pin_bytes(counter_bytes):
    anchor = b'if __name__ == "__main__":'
    assert counter_bytes.count(anchor) == 1
    pin = b'SELF_SHA256 = "' + hashlib.sha256(
        b"x").hexdigest().encode() + b'"\n'
    # reuse the file's own pinned digest so the inserted line is stripped by the
    # counter's own SELF_PIN_RE and cannot be the reason the pin fails
    import re
    m = re.search(rb'^SELF_SHA256 = "([0-9a-f]{64})"\n', counter_bytes, re.M)
    line = b'SELF_SHA256 = "' + m.group(1) + b'"\n'
    return counter_bytes.replace(anchor, line + anchor, 1)


def one(name, note, special, drv, outdir):
    d = os.path.join(SCRATCH, "ctl-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    repo = clone_at(REV, os.path.join(d, "repo"))
    if note is not None:
        with open(os.path.join(repo, NOTE), "w", encoding="utf-8") as f:
            f.write(note)
    if special == "double-pin":
        cb = open(os.path.join(SCRATCH, "counter-v94.py"), "rb").read()
        with open(os.path.join(repo, COUNTER_PATH), "wb") as f:
            f.write(double_pin_bytes(cb))
    crev = commit(repo, name)
    if special == "double-pin":
        counter = os.path.join(d, "counter-double-pin.py")
        with open(counter, "wb") as f:
            f.write(subprocess.run(["git", "-C", repo, "cat-file", "blob",
                                    crev + ":" + COUNTER_PATH],
                                   capture_output=True, env=SEALED).stdout)
    else:
        counter = os.path.join(SCRATCH, "counter-v94.py")
    code, out, err = run_counter(counter, repo, crev, os.path.join(d, "work"))
    body = ("control=%s clone_rev=%s parent=%s counter_sha=%s\nexit=%d\n"
            % (name, crev, REV, hashlib.sha256(open(counter, "rb").read()).hexdigest(), code)
            + out + err)
    with open(os.path.join(outdir, name + ".out"), "w", encoding="utf-8") as f:
        f.write(body)
    return name, code, out


def conj(out):
    c = {}
    for line in out.split("\n"):
        if line.startswith("C1_CONJUNCTS "):
            for kv in line.split()[1:]:
                k, v = kv.split("=", 1)
                c[k] = v
    return c


def main():
    drv = load_driver()
    outdir = os.path.join(SCRATCH, "runs")
    os.makedirs(outdir, exist_ok=True)
    slots_ = slots(None, drv)
    names = list(slots_)
    with ThreadPoolExecutor(max_workers=len(names)) as ex:
        futs = [ex.submit(one, n, *slots_[n], drv, outdir) for n in names]
        results = [f.result() for f in futs]
    with open(os.path.join(outdir, "before-summary.txt"), "w", encoding="utf-8") as f:
        f.write("rev=%s counter_sha=%s\n\n" % (
            REV, hashlib.sha256(open(os.path.join(SCRATCH, "counter-v94.py"), "rb").read()).hexdigest()))
        for name, code, out in sorted(results):
            c = conj(out)
            keys = ("verdict_tables", "ids", "mismatched0", "figure", "note")
            f.write("%-34s exit=%d %s\n" % (name, code,
                    " ".join("%s=%s" % (k, c.get(k, "-")) for k in keys)))
    for name, code, out in sorted(results):
        print("%-34s exit=%d %s" % (name, code, conj(out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
