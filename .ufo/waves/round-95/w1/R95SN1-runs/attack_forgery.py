#!/usr/bin/env python3
"""R95SN1: the strongest PATH attack — a hostile `git` that forges the counter,
the manifest AND the receipts consistently, producing a fully synthetic green
C2 verdict with no committed evidence at all."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/tameshi-r95/R95SN1"
LANE_SRC = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
CHECKER = S + "/snap/conjunct-disposition-v95.py"
COUNTER_REL = ".ufo/evidence/round-95/c1/measure-v95.py"
MANIFEST_REL = ".ufo/evidence/round-95/conjunct-disposition.json"
RECEIPTS_REL = ".ufo/evidence/round-95/pre-freeze/controls"
RESULTS = []

KEYS = ["selfpin", "pins", "spec", "pin", "green", "canary", "valid0", "trivial0",
        "inconclusive0", "unstable0", "note", "verdict_tables", "ids", "mismatched0",
        "figure", "witnessed", "source", "coverage", "n_min"]


def rec(fid, title, observed, expected, severity, verdict):
    RESULTS.append(dict(id=fid, title=title, observed=observed, expected=expected,
                        severity=severity, verdict=verdict))


def sh(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)


def clone(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    sh(["git", "clone", "-q", "--shared", LANE_SRC, dest])
    top = sh(["git", "-C", dest, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(dest), "toplevel mismatch " + dest
    return dest


def commit_all(lane, msg):
    sh(["git", "-C", lane, "add", "-A"])
    sh(["git", "-C", lane, "-c", "user.name=atk", "-c", "user.email=atk@invalid",
        "commit", "-qm", msg])
    return sh(["git", "-C", lane, "rev-parse", "HEAD"]).stdout.strip()


def stage_instruments(lane):
    shutil.copytree(os.path.join(LANE_SRC, ".ufo/evidence/round-95"),
                    os.path.join(lane, ".ufo/evidence/round-95"), dirs_exist_ok=True)
    shutil.rmtree(os.path.join(lane, ".ufo/evidence/round-95/c1/__pycache__"),
                  ignore_errors=True)


def write_fake_git(bindir, forge_dir):
    """A `git` that answers the checker's reads from a forged directory."""
    os.makedirs(bindir, exist_ok=True)
    g = os.path.join(bindir, "git")
    with open(g, "w") as f:
        f.write(
            "#!/bin/sh\n"
            "REALGIT=/usr/bin/git\n"
            "FORGE=%s\n"
            "case \"$3\" in\n"
            "  replace) exit 0 ;;\n"                     # pretend no replace refs
            "  cat-file)\n"
            "    spec=\"$5\"\n"
            "    base=$(basename \"$spec\" 2>/dev/null)\n"
            "    case \"$spec\" in\n"
            "      *measure-v95.py) exec cat \"$FORGE/counter.py\" ;;\n"
            "      *conjunct-disposition.json) exec cat \"$FORGE/manifest.json\" ;;\n"
            "      *pre-freeze/controls/*) exec cat \"$FORGE/receipts/$base\" ;;\n"
            "    esac\n"
            "    ;;\n"
            "  ls-tree)\n"
            "    spec=\"$6\"\n"
            "    case \"$spec\" in\n"
            "      *pre-freeze/controls) exec ls -1 \"$FORGE/receipts\" ;;\n"
            "    esac\n"
            "    ;;\n"
            "esac\n"
            "exec $REALGIT \"$@\"\n" % forge_dir)
    os.chmod(g, 0o755)
    return g


def h01_forge_everything():
    lane = os.path.join(S, "atk9", "h01")
    shutil.rmtree(lane, ignore_errors=True)
    lane = clone(lane)
    stage_instruments(lane)
    rev = commit_all(lane, "h01 base")
    # the lane has NO receipts committed at all
    forge = os.path.join(S, "atk9", "h01_forge")
    shutil.rmtree(forge, ignore_errors=True)
    os.makedirs(os.path.join(forge, "receipts"))
    counter_src = """#!/usr/bin/env python3
print("C1_CONJUNCT_KEYS %s")
""" % " ".join(KEYS)
    open(os.path.join(forge, "counter.py"), "w").write(counter_src)
    sha = hashlib.sha256(counter_src.encode()).hexdigest()
    man = json.load(open(os.path.join(lane, MANIFEST_REL)))
    rows = man["rows"]
    for k, row in rows.items():
        if "unfalsifiable" in row:
            continue
        st = row["state"]
        if row["mode"] == "setup-refusal":
            body = "counter_sha=%s\nexit=2\nC1_SETUP %s\n" % (sha, row["token"])
        else:
            body = ("counter_sha=%s\nexit=1\nC1_CONJUNCTS %s\n"
                    % (sha, " ".join("%s=false" % x for x in KEYS)))
        open(os.path.join(forge, "receipts", st + ".out"), "w").write(body)
    json.dump(man, open(os.path.join(forge, "manifest.json"), "w"))
    bindir = os.path.join(S, "atk9", "h01_bin")
    write_fake_git(bindir, forge)
    env = dict(os.environ)
    env["PATH"] = bindir + ":" + env["PATH"]
    p = subprocess.run([sys.executable, "-I", CHECKER, "--lane", lane, "--rev", rev,
                        "--min-falsifiable", "17"], capture_output=True, text=True, env=env)
    out = p.stdout + p.stderr
    rows_line = [l for l in out.splitlines() if l.startswith("DISPOSITION rows=")]
    # how many receipts were actually committed at the audited rev?
    committed = sh(["git", "-C", lane, "ls-tree", "-r", "--name-only",
                    rev + ":" + RECEIPTS_REL]).stdout.strip()
    green = bool(rows_line) and "findings=0" in rows_line[0]
    rec("H01", "a hostile `git` earlier in PATH forges the counter, the manifest AND the "
               "receipts: the C2 verdict is computed from bytes that were never committed",
        "exit=%d verdict=%r committed_receipts_at_rev=%r forged_verdict_green=%s" % (
            p.returncode, rows_line[:1], committed[:60] or "(NONE)", green),
        "the C2 verdict must be bound to the bytes committed at --rev; the checker resolves "
        "`git` from the inherited PATH, so a hostile git supplies the counter, the manifest "
        "and every receipt",
        "HIGH" if green else "MEDIUM",
        "VULNERABLE" if green else "observed")


def h02_same_attack_without_path_hijack():
    """control: the same forged evidence committed at --rev (the declared limit)."""
    lane = os.path.join(S, "atk9", "h02")
    shutil.rmtree(lane, ignore_errors=True)
    lane = clone(lane)
    stage_instruments(lane)
    rev = commit_all(lane, "h02 base")
    forge = os.path.join(S, "atk9", "h02_forge")
    shutil.rmtree(forge, ignore_errors=True)
    os.makedirs(os.path.join(forge, "receipts"))
    counter_src = """#!/usr/bin/env python3
print("C1_CONJUNCT_KEYS %s")
""" % " ".join(KEYS)
    open(os.path.join(forge, "counter.py"), "w").write(counter_src)
    sha = hashlib.sha256(counter_src.encode()).hexdigest()
    man = json.load(open(os.path.join(lane, MANIFEST_REL)))
    rd = os.path.join(lane, RECEIPTS_REL)
    os.makedirs(rd, exist_ok=True)
    for k, row in man["rows"].items():
        if "unfalsifiable" in row:
            continue
        st = row["state"]
        if row["mode"] == "setup-refusal":
            body = "counter_sha=%s\nexit=2\nC1_SETUP %s\n" % (sha, row["token"])
        else:
            body = ("counter_sha=%s\nexit=1\nC1_CONJUNCTS %s\n"
                    % (sha, " ".join("%s=false" % x for x in KEYS)))
        open(os.path.join(rd, st + ".out"), "w").write(body)
    open(os.path.join(lane, COUNTER_REL), "w").write(counter_src)
    json.dump(man, open(os.path.join(lane, MANIFEST_REL), "w"))
    rev = commit_all(lane, "forged evidence committed")
    p = subprocess.run([sys.executable, "-I", CHECKER, "--lane", lane, "--rev", rev,
                        "--min-falsifiable", "17"], capture_output=True, text=True)
    out = p.stdout + p.stderr
    rows_line = [l for l in out.splitlines() if l.startswith("DISPOSITION rows=")]
    rec("H02", "control: the same forged evidence COMMITTED at --rev (the plan's declared "
               "limit: a hand-written receipt with the correct counter_sha is not certified)",
        "exit=%d verdict=%r" % (p.returncode, rows_line[:1]),
        "the checker accepts a committed hand-written receipt carrying the correct "
        "counter_sha (plan §C2 declared limits) — this is the baseline the PATH attack "
        "H01 reproduces WITHOUT requiring commit access",
        "MEDIUM (declared limit)", "accepted-by-design")


def main():
    os.makedirs(os.path.join(S, "atk9"), exist_ok=True)
    only = sys.argv[1:]
    for fn in [h01_forge_everything, h02_same_attack_without_path_hijack]:
        if only and not any(o in fn.__name__ for o in only):
            continue
        try:
            fn()
        except Exception as e:
            import traceback
            rec(fn.__name__, "ATTACK ERROR", repr(e), "no exception", "INFO", "error")
            traceback.print_exc()
        print("%-46s %s" % (fn.__name__, RESULTS[-1]["verdict"]))
    out = os.path.join(S, "runs", "R95SN1-forgery-results.json")
    json.dump(RESULTS, open(out, "w"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
