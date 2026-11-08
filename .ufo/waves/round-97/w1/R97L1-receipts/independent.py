#!/usr/bin/env python3
"""R97L1 independent guard probe for the round-96 checker.

Builds a scratch fixture store in the conjunct-disposition-v96.py layout
(counter stub + manifest + round-96 claims digest + receipts in a real git
repo), applies ONE exact-string edit per row, and runs the pristine and the
mutant checker against the SAME store and arguments.

Classification (R97L1 vocabulary):
  killed      pristine reproduces its declared refusal/finding and the mutant
              loses that token or changes exit;
  identical   pristine reproduces its declared outcome and the mutant run is
              the same in exit and declared token;
  inconclusive the fixture does not reproduce the pristine baseline, the edit
              is not unique in the byte stream, or the mutant will not compile.

Writes: independent.log (full transcript) and R97L1-independent.tsv (processed).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "07e50d6d0142b21e8443b5417b8edc4d1dd76455"
WANT = "02a5482a573193c37bd9ebfa9303e84284561f50326043967834c9fdbf0d1c80"
HERE = os.environ.get("R97L1_SCRATCH")
if not HERE:
    sys.exit("R97L1_SCRATCH is not set; point it at a scratch directory")
os.makedirs(HERE, exist_ok=True)
CHECKER = os.path.join(HERE, "R97L1-checker.py")
GIT = "/usr/bin/git"

POS = "counter_sha={CSHA}\nexit=1\nC1_CONJUNCTS alpha=false beta=true gamma=true\n"
POS2 = "counter_sha={CSHA}\nexit=1\nC1_CONJUNCTS alpha=true beta=false gamma=true\n"
GAMMA = "the sealed pin at state pos forbids a committed falsifier for gamma"
COUNTER = ("#!/usr/bin/env python3\n"
           "import sys\n"
           "if '--conjuncts' in sys.argv:\n"
           "    print('C1_CONJUNCT_KEYS alpha beta gamma')\n"
           "    sys.exit(0)\n"
           "print('C1_R96_PASS=false')\n"
           "sys.exit(1)\n")


def env_base(extra=None):
    home = os.path.join(HERE, "home")
    tmp = os.path.join(home, "tmp")
    os.makedirs(tmp, exist_ok=True)
    e = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8",
         "LC_ALL": "C.UTF-8", "HOME": home, "TMPDIR": tmp,
         "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
         "GIT_CONFIG_GLOBAL": "/dev/null", "HYAKU_SCRATCH": HERE}
    if extra:
        e.update(extra)
    return e


def g(repo, args):
    return subprocess.run([GIT, "-C", repo] + args, capture_output=True,
                          text=True, env=env_base())


def build_fixture(base, rows, receipts, claims_sha=None, worktree=None):
    repo = os.path.join(base, "store")
    c1 = os.path.join(repo, ".ufo/evidence/round-96/c1")
    rc = os.path.join(repo, ".ufo/evidence/round-96/pre-freeze/controls")
    os.makedirs(c1, exist_ok=True)
    os.makedirs(rc, exist_ok=True)
    os.makedirs(os.path.join(repo, ".ufo/waves/round-96"), exist_ok=True)
    with open(os.path.join(c1, "measure-v96.py"), "w", encoding="utf-8") as f:
        f.write(COUNTER)
    csha = hashlib.sha256(COUNTER.encode()).hexdigest()
    mbytes = (json.dumps({"rows": rows}, indent=1) + "\n").encode()
    with open(os.path.join(repo, ".ufo/evidence/round-96/conjunct-disposition.json"), "wb") as f:
        f.write(mbytes)
    digest = claims_sha or hashlib.sha256(mbytes).hexdigest()
    with open(os.path.join(repo, ".ufo/waves/round-96/claims.json"), "w", encoding="utf-8") as f:
        json.dump({"claims": {"C1": {"manifest_sha256": digest}}}, f)
    for name, body in receipts.items():
        with open(os.path.join(rc, name + ".out"), "w", encoding="utf-8") as f:
            f.write(body.replace("{CSHA}", csha))
    r = g(repo, ["init", "-q"])
    if r.returncode != 0:
        raise RuntimeError("git init failed: " + r.stderr)
    top = g(repo, ["rev-parse", "--show-toplevel"]).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise RuntimeError("toplevel assert failed: %r != %r" % (top, repo))
    g(repo, ["add", "-A"])
    r = g(repo, ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
                 "commit", "-qm", "fixture"])
    if r.returncode != 0:
        raise RuntimeError("fixture commit failed: " + r.stderr)
    g(repo, ["branch", "-M", "master"])
    rev = g(repo, ["rev-parse", "HEAD"]).stdout.strip()
    # worktree-only receipts: written after the commit, never added
    for name, body in (worktree or {}).items():
        with open(os.path.join(rc, name + ".out"), "w", encoding="utf-8") as f:
            f.write(body.replace("{CSHA}", csha))
    return repo, rev


def run_checker(path, repo, rev, extra, env):
    r = subprocess.run([sys.executable, "-I", path, "--lane", repo,
                        "--rev", rev] + extra, capture_output=True, text=True,
                       env=env)
    return r.returncode, r.stdout + r.stderr


def tokens(text):
    out = []
    for line in text.splitlines():
        if line.startswith("DISPOSITION_SETUP ") or line.startswith("DISPOSITION_FINDING "):
            out.append(" ".join(line.split()[:2]))
    return sorted(set(out))


def clean_rows(gamma=GAMMA):
    return {
        "alpha": {"state": "pos", "mode": "conjunct-false"},
        "beta": {"state": "pos2", "mode": "conjunct-false"},
        "gamma": {"unfalsifiable": gamma},
    }


# ---------------------------------------------------------------- row states
def state_clean(base):
    return dict(rows=clean_rows(), receipts={"pos": POS, "pos2": POS2})


def state_wt_receipt(base):
    rows = clean_rows()
    rows["alpha"] = {"state": "wt-cheat", "mode": "conjunct-false"}
    return dict(rows=rows, receipts={"pos": POS, "pos2": POS2},
                worktree={"wt-cheat": POS})


def state_bad_claims(base):
    clean = clean_rows()
    clean_bytes = (json.dumps({"rows": clean}, indent=1) + "\n").encode()
    attack = {k: {"unfalsifiable": "the sealed pin at state pos forbids a committed "
                                    "falsifier for " + k} for k in clean}
    return dict(rows=attack, receipts={"pos": POS, "pos2": POS2},
                claims_sha=hashlib.sha256(clean_bytes).hexdigest())


def state_other_token(base):
    rows = clean_rows()
    rows["alpha"] = {"state": "tok", "mode": "setup-refusal",
                     "token": "spec-absent-at-rev"}
    return dict(rows=rows,
                receipts={"pos": POS, "pos2": POS2,
                          "tok": "counter_sha={CSHA}\nexit=2\nC1_SETUP other-refusal\n"})


def state_reason_no_state(base):
    return dict(rows=clean_rows(
                    "the sealed pin and the pinned gate bytes forbid every "
                    "conceivable committed falsifier here"),
                receipts={"pos": POS, "pos2": POS2})


def state_sha_cheat(base):
    rows = clean_rows()
    rows["alpha"] = {"state": "sha-cheat", "mode": "conjunct-false"}
    return dict(rows=rows,
                receipts={"pos": POS, "pos2": POS2,
                          "sha-cheat": "counter_sha=" + "0" * 64
                          + "\nexit=1\nC1_CONJUNCTS alpha=false beta=true gamma=true\n"})


def state_hostile(base):
    shim = os.path.join(base, "shim")
    os.makedirs(shim, exist_ok=True)
    p = os.path.join(shim, "git")
    with open(p, "w", encoding="utf-8") as f:
        f.write("#!/bin/sh\nexit 99\n")
    os.chmod(p, 0o755)
    return dict(rows=clean_rows(), receipts={"pos": POS, "pos2": POS2},
                env_override={"PATH": shim + ":/usr/local/bin:/usr/bin:/bin"})


ROWS = [
    dict(id="R97L1-1", guard="GitStore.read_receipt reads the object store at --rev, not the worktree",
         state="worktree-only receipt named by a conjunct-false row",
         build=state_wt_receipt, expect="killed",
         pristine_exit=1, token="receipt-absent-at-rev",
         old='        blob = self.read_blob("%s/%s.out" % (self.receipts, state))',
         new='        _p = os.path.join(self.lane, self.receipts, state + ".out")\n'
             '        blob = open(_p, "rb").read() if os.path.exists(_p) else None'),
    dict(id="R97L1-2", guard="the manifest must equal the sha256 the round-96 claims file names",
         state="manifest rewritten to all-unfalsifiable; claims still names the clean manifest digest",
         build=state_bad_claims, expect="killed",
         pristine_exit=2, token="manifest-sha-mismatch",
         old='        if _want and hashlib.sha256(manifest_blob).hexdigest() != _want:',
         new='        if False:'),
    dict(id="R97L1-3", guard="a setup-refusal row's declared token must appear in its receipt",
         state="row declares spec-absent-at-rev, receipt prints C1_SETUP other-refusal",
         build=state_other_token, expect="killed",
         pristine_exit=1, token="token-absent",
         old='            if not token or ("C1_SETUP " + token) not in body:',
         new='            if not token:'),
    dict(id="R97L1-4", guard="an unfalsifiable reason must name a committed state or a hex digest",
         state="reason names a mechanism but no state and no digest",
         build=state_reason_no_state, expect="killed",
         pristine_exit=1, token="reason-names-no-state-or-digest",
         old='            elif not names_a_state_or_digest(reason, present_states):',
         new='            elif False:'),
    dict(id="R97L1-5", guard="a receipt's counter_sha must equal the counter blob digest at --rev",
         state="receipt carries counter_sha=0*64",
         build=state_sha_cheat, expect="killed",
         pristine_exit=1, token="receipt-counter-sha-mismatch",
         old='        if got_sha is None or not SHA_RE.fullmatch(got_sha) or got_sha != counter_sha:',
         new='        if got_sha is None or not SHA_RE.fullmatch(got_sha):'),
    dict(id="R97L1-6", guard="git is resolved by absolute path",
         state="hostile git shim first on the checker process PATH",
         build=state_hostile, expect="identical",
         pristine_exit=0, token=None,
         old='GIT = "/usr/bin/git"', new='GIT = "git"'),
]


def ensure_checker():
    if os.path.exists(CHECKER):
        return
    blob = subprocess.run([GIT, "-C", LANE, "cat-file", "blob",
                           REV + ":.ufo/evidence/round-96/conjunct-disposition-v96.py"],
                          capture_output=True).stdout
    if hashlib.sha256(blob).hexdigest() != WANT:
        raise SystemExit("checker blob digest is not the frozen 02a5482a...")
    with open(CHECKER, "wb") as f:
        f.write(blob)


def main():
    log = []
    tsv = []
    ensure_checker()
    src = open(CHECKER, "rb").read()
    sha = hashlib.sha256(src).hexdigest()
    log.append("CHECKER %s sha256=%s" % (CHECKER, sha))

    for i, row in enumerate(ROWS):
        base = os.path.join(HERE, "work", row["id"])
        shutil.rmtree(base, ignore_errors=True)
        os.makedirs(base)
        print("\nROW %s :: %s" % (row["id"], row["guard"]))
        log.append("\nROW %s :: %s" % (row["id"], row["guard"]))
        old_b = row["old"].encode()
        count = src.count(old_b)
        print("  anchor_count=%d" % count)
        log.append("  anchor_count=%d" % count)
        if count != 1:
            print("  observed=inconclusive (anchor not unique)")
            tsv.append((row["id"], row["guard"], count, row["state"], "", "", "", "",
                        "", "inconclusive", row["expect"],
                        "anchor count %d != 1" % count))
            continue
        mut = src.replace(old_b, row["new"].encode(), 1)
        try:
            compile(mut, "<mutant-%s>" % row["id"], "exec")
        except SyntaxError as exc:
            print("  observed=inconclusive (mutant does not compile: %s)" % exc)
            tsv.append((row["id"], row["guard"], count, row["state"], "", "", "", "",
                        "", "inconclusive", row["expect"],
                        "mutant SyntaxError: %s" % exc))
            continue
        spec = row["build"](base)
        repo, rev = build_fixture(base, spec["rows"], spec["receipts"],
                                  spec.get("claims_sha"), spec.get("worktree"))
        cpath = os.path.join(base, "checker-pristine.py")
        with open(cpath, "wb") as f:
            f.write(src)
        mpath = os.path.join(base, "checker-%s.py" % row["id"])
        with open(mpath, "wb") as f:
            f.write(mut)
        env = env_base(spec.get("env_override"))
        extra = []
        pe, pt = run_checker(cpath, repo, rev, extra, env)
        me, mt = run_checker(mpath, repo, rev, extra, env)
        p_tok = row["token"] is not None and row["token"] in pt
        m_tok = row["token"] is not None and row["token"] in mt
        baseline = (pe == row["pristine_exit"]) and (row["token"] is None or p_tok)
        differs = (me != pe) or (row["token"] is not None and not m_tok)
        if not baseline:
            observed = "inconclusive"
        elif differs:
            observed = "killed"
        else:
            observed = "identical"
        identical_out = pt == mt
        print("  state=%s rev=%s" % (row["state"], rev))
        print("  pristine: exit=%d token_present=%s" % (pe, p_tok))
        print("  mutant:   exit=%d token_present=%s stdout_identical=%s" % (me, m_tok, identical_out))
        print("  observed=%s expected=%s" % (observed, row["expect"]))
        log.append("  state=%s rev=%s" % (row["state"], rev))
        log.append("  pristine: exit=%d token_present=%s tokens=%s" % (pe, p_tok, tokens(pt)))
        log.append("  mutant:   exit=%d token_present=%s tokens=%s stdout_identical=%s"
                   % (me, m_tok, tokens(mt), identical_out))
        log.append("  observed=%s expected=%s" % (observed, row["expect"]))
        log.append("  --- pristine stdout ---\n" + pt.strip())
        log.append("  --- mutant stdout ---\n" + mt.strip())
        tsv.append((row["id"], row["guard"], count, row["state"], pe, p_tok,
                    me, m_tok, identical_out, observed, row["expect"],
                    "baseline" if baseline else "pristine baseline unmet"))

    with open(os.path.join(HERE, "independent.log"), "w", encoding="utf-8") as f:
        f.write("\n".join(log) + "\n")
    with open(os.path.join(HERE, "R97L1-independent.tsv"), "w", encoding="utf-8") as f:
        f.write("# independent\n")
        f.write("id\tguard\tanchor_count\tstate\tpristine_exit\tpristine_token_present\t"
                "mutant_exit\tmutant_token_present\tstdout_identical\tobserved\texpected\tdiagnosis\n")
        for r in tsv:
            f.write("\t".join(str(x) for x in r) + "\n")
    print("\nWROTE %s" % os.path.join(HERE, "R97L1-independent.tsv"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
