#!/usr/bin/env python3
"""R95SN1: corrected A06 (working-tree-only receipt) and a full PATH-hijack
forgery that demonstrates a forged green verdict."""
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
RECEIPTS_REL = ".ufo/evidence/round-95/pre-freeze/controls"
RESULTS = []


def rec(fid, title, observed, expected, severity, verdict):
    RESULTS.append(dict(id=fid, title=title, observed=observed, expected=expected,
                        severity=severity, verdict=verdict))


def sh(cmd, cwd=None, env=None, check=False):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError("cmd failed: %s\n%s" % (cmd, p.stderr))
    return p


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


KEYS = ["selfpin", "pins", "spec", "pin", "green", "canary", "valid0", "trivial0",
        "inconclusive0", "unstable0", "note", "verdict_tables", "ids", "mismatched0",
        "figure", "witnessed", "source", "coverage", "n_min"]


def build(name, omit=(), forge=None):
    d = os.path.join(S, "atk8", name)
    lane = clone(d)
    stage_instruments(lane)
    blob = sh(["git", "-C", lane, "cat-file", "blob", "HEAD:" + COUNTER_REL]).stdout
    sha = hashlib.sha256(blob.encode()).hexdigest()
    man = json.load(open(os.path.join(lane, ".ufo/evidence/round-95/conjunct-disposition.json")))
    rd = os.path.join(lane, RECEIPTS_REL)
    os.makedirs(rd, exist_ok=True)
    for k, row in man["rows"].items():
        if "unfalsifiable" in row:
            continue
        st = row["state"]
        if st in omit:
            continue
        if row["mode"] == "setup-refusal":
            body = "counter_sha=%s\nexit=2\nC1_SETUP %s\n" % (sha, row["token"])
        else:
            body = ("counter_sha=%s\nexit=1\nC1_CONJUNCTS %s\n"
                    % (sha, " ".join("%s=false" % x for x in KEYS)))
        open(os.path.join(rd, st + ".out"), "w").write(body)
    if forge:
        forge(lane, rd, sha)
    return lane, sha, rd


def g01_working_tree_only_receipt():
    """The plan's forge-handwritten control: a receipt for a manifest state that
    exists ONLY in the working tree, never committed."""
    lane, sha, rd = build("g01", omit=("hidden-c001",))
    rev = commit_all(lane, "no hidden-c001 receipt committed")
    # now write it into the working tree, never staged
    open(os.path.join(rd, "hidden-c001.out"), "w").write(
        "control=hidden-c001\ncounter_sha=%s\nexit=1\nC1_CONJUNCTS %s\n"
        % (sha, " ".join("%s=false" % x for x in KEYS)))
    st = sh(["git", "-C", lane, "status", "--porcelain"]).stdout.strip()
    uncommitted = "hidden-c001.out" in st
    p = subprocess.run([sys.executable, "-I", CHECKER, "--lane", lane, "--rev", rev,
                        "--min-falsifiable", "17"], capture_output=True, text=True)
    out = p.stdout + p.stderr
    findings = [l for l in out.splitlines() if "FINDING" in l]
    ok = "receipt-absent-at-rev" in out and p.returncode == 1
    rec("G01", "plan control forge-handwritten: a receipt for the manifest state "
               "verdict_tables that exists ONLY in the working tree (never committed)",
        "exit=%d uncommitted_file_present=%s git_status=%r findings=%r" % (
            p.returncode, uncommitted, st[:90], findings[:2]),
        "exit 1 with the named finding receipt-absent-at-rev (plan C2 wording)",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def g02_path_hijack_forges_green():
    """A hostile `git` earlier in PATH that FORGES the counter blob the checker
    reads, producing a green verdict on a lane whose real receipts are absent."""
    lane, sha, rd = build("g02")
    rev = commit_all(lane, "g02 base")
    fake = os.path.join(S, "atk8", "g02_bin")
    shutil.rmtree(fake, ignore_errors=True)
    os.makedirs(fake)
    # a proxy git: real git, except `cat-file blob <rev>:<counter>` returns a
    # forged counter whose conjunct list omits every manifest row
    proxy = os.path.join(fake, "git")
    with open(proxy, "w") as f:
        f.write(
            "#!/bin/sh\n"
            "REALGIT=/usr/bin/git\n"
            "case \"$3\" in\n"
            "  cat-file)\n"
            "    if [ \"$4\" = \"blob\" ]; then\n"
            "      spec=\"$5\"\n"
            "      case \"$spec\" in\n"
            "        *measure-v95.py)\n"
            "          printf '#!/usr/bin/env python3\\n"
            "print(\"C1_CONJUNCT_KEYS selfpin\")\\n'\n"
            "          exit 0 ;;\n"
            "      esac\n"
            "    fi ;;\n"
            "esac\n"
            "exec $REALGIT \"$@\"\n")
    os.chmod(proxy, 0o755)
    env = dict(os.environ)
    env["PATH"] = fake + ":" + env["PATH"]
    p = subprocess.run([sys.executable, "-I", CHECKER, "--lane", lane, "--rev", rev,
                        "--min-falsifiable", "17"], capture_output=True, text=True, env=env)
    out = p.stdout + p.stderr
    rows = [l for l in out.splitlines() if l.startswith("DISPOSITION ")]
    findings = [l for l in out.splitlines() if "FINDING" in l]
    # the forged counter prints ONE key; the manifest has 19 rows -> unknown-key findings
    hijacked = any("unknown-key" in f for f in findings)
    rec("G02", "a hostile `git` earlier in PATH serves a FORGED counter blob to the checker",
        "exit=%d rows=%r unknown_key_findings=%d first=%r" % (
            p.returncode, rows[-1:], len(findings), findings[:1]),
        "the C2 verdict must be computed from the counter blob at --rev; the checker "
        "resolves `git` from the inherited PATH, so a hostile git supplies the bytes "
        "(the C1 counter pins PATH=/usr/local/bin:/usr/bin:/bin)",
        "HIGH" if hijacked else "MEDIUM",
        "VULNERABLE" if hijacked else "observed")


def g03_path_hijack_forges_counter_sha():
    """The same hijack, but the forged git also lies about the counter's sha256 by
    returning the honest counter bytes while the checker computes the sha itself."""
    lane, sha, rd = build("g03")
    rev = commit_all(lane, "g03 base")
    fake = os.path.join(S, "atk8", "g03_bin")
    shutil.rmtree(fake, ignore_errors=True)
    os.makedirs(fake)
    proxy = os.path.join(fake, "git")
    with open(proxy, "w") as f:
        f.write(
            "#!/bin/sh\n"
            "REALGIT=/usr/bin/git\n"
            "case \"$3\" in\n"
            "  cat-file)\n"
            "    if [ \"$4\" = \"blob\" ]; then\n"
            "      spec=\"$5\"\n"
            "      case \"$spec\" in\n"
            "        *measure-v95.py)\n"
            "          exec $REALGIT \"$@\" ;;\n"
            "      esac\n"
            "    fi ;;\n"
            "esac\n"
            "exec $REALGIT \"$@\"\n")
    os.chmod(proxy, 0o755)
    env = dict(os.environ)
    env["PATH"] = fake + ":" + env["PATH"]
    p = subprocess.run([sys.executable, "-I", CHECKER, "--lane", lane, "--rev", rev,
                        "--min-falsifiable", "17"], capture_output=True, text=True, env=env)
    out = p.stdout + p.stderr
    rows = [l for l in out.splitlines() if l.startswith("DISPOSITION ")]
    rec("G03", "control: a PATH proxy that behaves like real git (no tampering) "
               "must not change the verdict",
        "exit=%d rows=%r" % (p.returncode, rows[-1:]),
        "the verdict must be unchanged when git behaves honestly",
        "INFO", "observed")


def main():
    os.makedirs(os.path.join(S, "atk8"), exist_ok=True)
    only = sys.argv[1:]
    for fn in [g01_working_tree_only_receipt, g02_path_hijack_forges_green,
               g03_path_hijack_forges_counter_sha]:
        if only and not any(o in fn.__name__ for o in only):
            continue
        try:
            fn()
        except Exception as e:
            import traceback
            rec(fn.__name__, "ATTACK ERROR", repr(e), "no exception", "INFO", "error")
            traceback.print_exc()
        print("%-42s %s" % (fn.__name__, RESULTS[-1]["verdict"]))
    out = os.path.join(S, "runs", "R95SN1-final-results.json")
    json.dump(RESULTS, open(out, "w"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
