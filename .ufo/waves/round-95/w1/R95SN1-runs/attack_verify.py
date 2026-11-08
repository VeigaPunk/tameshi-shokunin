#!/usr/bin/env python3
"""R95SN1 final airtight verification of the two HIGH findings, using the
instruments extracted from the FROZEN object store (not a working-tree copy).

K1: the C2 checker resolves `git` from the inherited PATH; a hostile git can
    forge the counter, the manifest and every receipt -> a fully green C2
    verdict with ZERO committed receipts.
K2: the C1 counter with --rev '' grades the git INDEX (staged, uncommitted
    bytes) instead of a commit.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/tameshi-r95/R95SN1"
LANE_SRC = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
FREEZE = "3ca1981a2265880ae3ce9b88d316e71741b02426"
INSTR = "20fabad4dc64b2feff16853a4cce01d9b324f821"
COUNTER_REL = ".ufo/evidence/round-95/c1/measure-v95.py"
MANIFEST_REL = ".ufo/evidence/round-95/conjunct-disposition.json"
RECEIPTS_REL = ".ufo/evidence/round-95/pre-freeze/controls"
KEYS = ["selfpin", "pins", "spec", "pin", "green", "canary", "valid0", "trivial0",
        "inconclusive0", "unstable0", "note", "verdict_tables", "ids", "mismatched0",
        "figure", "witnessed", "source", "coverage", "n_min"]


def sh(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)


def blob_at(rev, path):
    return sh(["git", "-C", LANE_SRC, "cat-file", "blob", rev + ":" + path]).stdout


def main():
    out = {}
    work = os.path.join(S, "verify")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)

    # ---- extract the instruments from the frozen object store
    checker_p = os.path.join(work, "conjunct-disposition-v95.py")
    counter_p = os.path.join(work, "measure-v95.py")
    open(checker_p, "w").write(blob_at(INSTR, ".ufo/evidence/round-95/conjunct-disposition-v95.py"))
    open(counter_p, "w").write(blob_at(INSTR, COUNTER_REL))
    out["checker_sha256"] = hashlib.sha256(open(checker_p, "rb").read()).hexdigest()
    out["counter_sha256"] = hashlib.sha256(open(counter_p, "rb").read()).hexdigest()
    out["counter_sha256_matches_freeze_revtxt"] = (
        out["counter_sha256"] == "5f0d177034173971439be06eb5fbf32dfa8fec4b35a856fc617999e4554ccc2e")

    # ---- K1: hostile git forges everything
    lane = os.path.join(work, "lane")
    sh(["git", "clone", "-q", "--shared", LANE_SRC, lane])
    rev = sh(["git", "-C", lane, "rev-parse", FREEZE]).stdout.strip()
    out["lane_rev"] = rev

    forge = os.path.join(work, "forge")
    os.makedirs(os.path.join(forge, "receipts"))
    counter_src = '#!/usr/bin/env python3\nprint("C1_CONJUNCT_KEYS %s")\n' % " ".join(KEYS)
    open(os.path.join(forge, "counter.py"), "w").write(counter_src)
    sha = hashlib.sha256(counter_src.encode()).hexdigest()
    man = json.loads(blob_at(INSTR, MANIFEST_REL))
    for k, row in man["rows"].items():
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

    bindir = os.path.join(work, "bin")
    os.makedirs(bindir)
    with open(os.path.join(bindir, "git"), "w") as f:
        f.write(
            "#!/bin/sh\n"
            "REALGIT=/usr/bin/git\n"
            "FORGE=%s\n"
            "case \"$3\" in\n"
            "  replace) exit 0 ;;\n"
            "  cat-file)\n"
            "    spec=\"$5\"; base=$(basename \"$spec\" 2>/dev/null)\n"
            "    case \"$spec\" in\n"
            "      *measure-v95.py) exec cat \"$FORGE/counter.py\" ;;\n"
            "      *conjunct-disposition.json) exec cat \"$FORGE/manifest.json\" ;;\n"
            "      *pre-freeze/controls/*) exec cat \"$FORGE/receipts/$base\" ;;\n"
            "    esac ;;\n"
            "  ls-tree)\n"
            "    spec=\"$6\"\n"
            "    case \"$spec\" in\n"
            "      *pre-freeze/controls) exec ls -1 \"$FORGE/receipts\" ;;\n"
            "    esac ;;\n"
            "esac\n"
            "exec $REALGIT \"$@\"\n" % forge)
    os.chmod(os.path.join(bindir, "git"), 0o755)

    env = dict(os.environ)
    env["PATH"] = bindir + ":" + env["PATH"]
    p = subprocess.run([sys.executable, "-I", checker_p, "--lane", lane, "--rev", rev,
                        "--min-falsifiable", "17"], capture_output=True, text=True, env=env)
    k1_out = p.stdout + p.stderr
    committed = sh(["git", "-C", lane, "ls-tree", "-r", "--name-only",
                    rev + ":" + RECEIPTS_REL]).stdout.strip()
    out["K1"] = dict(exit=p.returncode,
                     verdict=[l for l in k1_out.splitlines() if l.startswith("DISPOSITION rows=")],
                     committed_receipts_at_rev=committed or "(NONE)",
                     forged_green=any("findings=0" in l for l in k1_out.splitlines()
                                      if l.startswith("DISPOSITION rows=")))

    # control: the same checker WITHOUT the hostile git
    env2 = dict(os.environ)
    p2 = subprocess.run([sys.executable, "-I", checker_p, "--lane", lane, "--rev", rev,
                         "--min-falsifiable", "17"], capture_output=True, text=True, env=env2)
    out["K1_control"] = dict(exit=p2.returncode,
                             verdict=[l for l in (p2.stdout + p2.stderr).splitlines()
                                      if l.startswith("DISPOSITION rows=")],
                             findings=[l for l in (p2.stdout + p2.stderr).splitlines()
                                       if "FINDING" in l][:3])

    # ---- K2: --rev '' on the C1 counter reads the INDEX
    lane2 = os.path.join(work, "lane2")
    sh(["git", "clone", "-q", "--shared", LANE_SRC, lane2])
    note = "corpus/knowledge/mutation-case-fleet-sources-census.md"
    np_ = os.path.join(lane2, note)
    body = open(np_).read()
    marker = "| C99 | x | KILLED | differs |"
    open(np_, "w").write(body + "\n" + marker + "\n")
    sh(["git", "-C", lane2, "add", "-A"])
    st = sh(["git", "-C", lane2, "status", "--porcelain"]).stdout.strip()
    w = os.path.join(work, "wk2")
    os.makedirs(w)
    p3 = subprocess.run([sys.executable, "-I", counter_p, "--repo", lane2, "--rev", "",
                         "--work", w], capture_output=True, text=True, timeout=500)
    k2_out = p3.stdout + p3.stderr
    out["K2"] = dict(exit=p3.returncode,
                     git_status=st,
                     staged_marker_visible=(marker in k2_out),
                     summary=[l for l in k2_out.splitlines() if l.startswith("C1_SUMMARY")],
                     badrows=[l for l in k2_out.splitlines() if l.startswith("C1_BADROWS")])

    # control: the same repo at HEAD (committed) must NOT see the staged row
    lane3 = os.path.join(work, "lane3")
    sh(["git", "clone", "-q", "--shared", LANE_SRC, lane3])
    np3 = os.path.join(lane3, note)
    open(np3, "w").write(open(np_).read())
    sh(["git", "-C", lane3, "add", "-A"])
    w3 = os.path.join(work, "wk3")
    os.makedirs(w3)
    p4 = subprocess.run([sys.executable, "-I", counter_p, "--repo", lane3, "--rev", "HEAD",
                         "--work", w3], capture_output=True, text=True, timeout=500)
    k2c_out = p4.stdout + p4.stderr
    out["K2_control"] = dict(exit=p4.returncode,
                             staged_marker_visible=(marker in k2c_out),
                             summary=[l for l in k2c_out.splitlines() if l.startswith("C1_SUMMARY")])

    rj = os.path.join(S, "runs", "R95SN1-verify.json")
    json.dump(out, open(rj, "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
