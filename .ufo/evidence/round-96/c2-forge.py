#!/usr/bin/env python3
"""Round-96 C2 forge battery.

Builds the three pre-registered forged receipt sets of plans/round-96.plan.md
§Controls — C2 in scratch clones and runs both the sealed round-96 checker
(.ufo/evidence/round-96/conjunct-disposition-v96.py) and the round-94 checker
at `6a2a1fdd` against each:

  forge-handwritten   a receipt named for a manifest state, hand-written in the
                      working tree only (absent from the audited revision);
  forge-counter-sha   a committed receipt whose `counter_sha=` line is 0x64;
  forge-replace-ref   `git replace` of the counter blob inside the clone.

Every checker run writes one receipt per (artifact x checker) with the exit
code and the DISPOSITION_FINDING / DISPOSITION_SETUP lines. The round-94
checker is the before-witness: it reads receipts from the filesystem and never
reads `counter_sha=`, so it accepts both receipt forgeries and follows the
replacement ref.

The instrument commit in the scratch clone contains the v96 checker, the v96
manifest and the v95 receipts directory. When the real v95 battery receipts do
not exist yet (the usual state during the wave), the receipts are the committed
round-94 battery bodies with a `counter_sha=<sha256 of the counter blob at the
instrument commit>` line prepended; the matrix records that provenance. Nothing
is read from a temporary receipt root and no receipt is read from the lane working tree by the
checker.

Usage:
  python3 -I .ufo/evidence/round-96/c2-forge.py --lane LANE --work SCRATCH \
      --outdir RECEIPTS

Exit: 0 every expectation met; 1 one or more expectations missed; 2 setup error.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

V96_CHECKER = ".ufo/evidence/round-96/conjunct-disposition-v96.py"
V96_MANIFEST = ".ufo/evidence/round-96/conjunct-disposition.json"
V96_COUNTER = ".ufo/evidence/round-96/c1/measure-v96.py"
V96_RECEIPTS = ".ufo/evidence/round-96/pre-freeze/controls"
V94_REV = "6a2a1fdd"
V94_CHECKER = ".ufo/evidence/round-94/conjunct-disposition-v94.py"
V94_COUNTER = ".ufo/evidence/round-94/c1/measure-v94.py"
V94_MANIFEST = ".ufo/evidence/round-94/conjunct-disposition.json"
V94_RECEIPTS = ".ufo/evidence/round-94/pre-freeze/controls"
CLEAN_LINE = "DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0"


def child_env():
    """No inherited GIT_*; no system/global git config. Replace refs stay live
    for the round-94 before-witness (it has no seal); the v96 checker installs
    its own GIT_NO_REPLACE_OBJECTS=1 seal internally."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    return env


def git_env():
    env = child_env()
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    return env


class Forge:
    def __init__(self, lane, work, outdir, instrument_rev=None):
        self.lane = os.path.realpath(lane)
        self.work = os.path.realpath(work)
        self.outdir = os.path.realpath(outdir)
        self.instrument_rev = instrument_rev
        self.git_env = git_env()
        self.child_env = child_env()
        self.checks = []

    # ---- git helpers -------------------------------------------------
    def git(self, repo, args, env=None, check=True):
        r = subprocess.run(["git", "-C", repo] + args, capture_output=True,
                           text=True, env=env or self.git_env)
        if check and r.returncode != 0:
            raise RuntimeError("git %s in %s failed: %s" % (
                " ".join(args), repo, r.stderr.strip()))
        return r

    def toplevel(self, repo):
        top = self.git(repo, ["rev-parse", "--show-toplevel"]).stdout.strip()
        if not top or os.path.realpath(top) != os.path.realpath(repo):
            raise RuntimeError("fixture toplevel %r is not %r" % (top, repo))

    def clone(self, src, dst):
        r = subprocess.run(["git", "clone", "-q", "--shared", src, dst],
                           capture_output=True, text=True, env=self.git_env)
        if r.returncode != 0:
            raise RuntimeError("clone %s -> %s failed: %s" % (src, dst, r.stderr.strip()))
        self.toplevel(dst)
        return dst

    def commit(self, repo, msg):
        self.toplevel(repo)
        self.git(repo, ["add", "-A"])
        self.git(repo, ["-c", "user.name=round95-forge",
                        "-c", "user.email=round95-forge@invalid",
                        "-c", "commit.gpgsign=false", "commit", "-qm", msg])
        return self.git(repo, ["rev-parse", "HEAD"]).stdout.strip()

    def blob(self, repo, rev, path):
        r = subprocess.run(["git", "-C", repo, "cat-file", "blob",
                            "%s:%s" % (rev, path)], capture_output=True,
                           env=self.git_env)
        if r.returncode != 0:
            raise RuntimeError("blob absent: %s:%s" % (rev, path))
        return r.stdout

    def sha256(self, data):
        return hashlib.sha256(data).hexdigest()

    # ---- instrument commit ------------------------------------------
    def read_lane_file(self, path):
        if self.instrument_rev:
            return self.blob(self.lane, self.instrument_rev, path)
        full = os.path.join(self.lane, path)
        if not os.path.isfile(full):
            raise RuntimeError("instrument file absent in lane: " + full)
        with open(full, "rb") as f:
            return f.read()

    def prepare(self):
        os.makedirs(self.work, exist_ok=True)
        os.makedirs(self.outdir, exist_ok=True)
        if os.listdir(self.work):
            raise RuntimeError("work dir is not empty: " + self.work)
        prep = os.path.join(self.work, "prep")
        self.lane_head = self.git(self.lane, ["rev-parse", "HEAD"]).stdout.strip()
        self.clone(self.lane, prep)

        checker = self.read_lane_file(V96_CHECKER)
        manifest_bytes = self.read_lane_file(V96_MANIFEST)
        try:
            rows = json.loads(manifest_bytes)["rows"]
        except Exception as e:
            raise RuntimeError("v96 manifest unparsable: %s" % e)
        states = sorted({v["state"] for v in rows.values()
                         if isinstance(v, dict) and "state" in v})
        if not states:
            raise RuntimeError("v96 manifest has no state rows")

        # Counter: E1's bytes when they already answer --conjuncts, otherwise
        # the round-94 counter bytes as an explicitly labelled stand-in.
        counter_source = V96_COUNTER
        try:
            counter_bytes = self.read_lane_file(V96_COUNTER)
        except RuntimeError:
            counter_bytes = self.blob(self.lane, V94_REV, V94_COUNTER)
            counter_source = V94_COUNTER + "@" + V94_REV + " (v96 counter absent: stand-in)"
        probe = os.path.join(self.work, "counter-probe.py")
        with open(probe, "wb") as f:
            f.write(counter_bytes)
        pr = subprocess.run([sys.executable, "-I", probe, "--conjuncts"],
                            capture_output=True, text=True, env=self.child_env)
        if pr.returncode != 0 or "C1_CONJUNCT_KEYS " not in pr.stdout:
            counter_bytes = self.blob(self.lane, V94_REV, V94_COUNTER)
            counter_source = (V94_COUNTER + "@" + V94_REV +
                              " (v96 counter fails --conjuncts: stand-in; %s)"
                              % pr.stdout.strip()[:80])

        ev = os.path.join(prep, ".ufo/evidence/round-96")
        os.makedirs(os.path.join(ev, "c1"), exist_ok=True)
        self.write(os.path.join(ev, os.path.basename(V96_CHECKER)), checker)
        self.write(os.path.join(ev, os.path.basename(V96_MANIFEST)), manifest_bytes)
        self.write(os.path.join(ev, "c1", os.path.basename(V96_COUNTER)), counter_bytes)
        counter_sha = self.sha256(counter_bytes)

        receipts_dir = os.path.join(prep, V96_RECEIPTS)
        os.makedirs(receipts_dir, exist_ok=True)
        for st in states:
            body = self.blob(prep, "HEAD", "%s/%s.out" % (V94_RECEIPTS, st))
            self.write(os.path.join(receipts_dir, st + ".out"),
                       ("counter_sha=%s\n" % counter_sha).encode() + body)

        rev = self.commit(prep, "round-96 forge fixture: v96 instrument + receipts")
        blob_sha = self.sha256(self.blob(prep, rev, V96_COUNTER))
        if blob_sha != counter_sha:
            raise RuntimeError("receipt counter_sha %s != committed counter blob %s"
                               % (counter_sha, blob_sha))
        self.prep = prep
        self.instrument_rev = rev
        self.counter_sha = counter_sha
        self.counter_source = counter_source
        self.checker_sha = self.sha256(checker)
        self.manifest_sha = self.sha256(manifest_bytes)
        self.states = states
        self.receipts_note = ("v95 battery receipts absent at preparation time; "
                              "bodies are the committed round-94 receipts with "
                              "counter_sha=%s prepended" % counter_sha)
        return prep

    @staticmethod
    def write(path, data):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)

    # ---- checker runs ------------------------------------------------
    def run(self, name, script, args, env, header):
        cmd = [sys.executable, "-I", script] + args
        r = subprocess.run(cmd, capture_output=True, text=True, env=env)
        receipt = os.path.join(self.outdir, name + ".out")
        with open(receipt, "w", encoding="utf-8") as f:
            f.write(header + "\n")
            f.write("command=" + " ".join(cmd) + "\n")
            f.write("exit=%d\n" % r.returncode)
            f.write(r.stdout)
            if r.stderr:
                f.write("--- stderr ---\n" + r.stderr)
        return r, receipt

    def record(self, artifact, checker, r, expectation, ok, extra=""):
        got = "exit=%d" % r.returncode
        flagged = [l for l in r.stdout.splitlines()
                   if l.startswith("DISPOSITION_FINDING ") or l.startswith("DISPOSITION_SETUP ")]
        if flagged:
            got += " " + flagged[0]
        self.checks.append((artifact, checker, expectation, got, ok, extra))
        return ok

    # ---- artifacts ---------------------------------------------------
    def v95_args(self, clone, rev):
        return ["--lane", clone, "--rev", rev, "--min-falsifiable", "17"]

    def v94_args(self, clone, receipts):
        return ["--lane", clone, "--rev", V94_REV,
                "--counter", V94_COUNTER, "--manifest", V94_MANIFEST,
                "--receipts", receipts]

    def v94_script(self):
        path = os.path.join(self.work, "v94-checker-" + V94_REV + ".py")
        data = self.blob(self.lane, V94_REV, V94_CHECKER)
        self.write(path, data)
        self.v94_sha = self.sha256(data)
        return path

    def baseline(self):
        prep, rev = self.prep, self.instrument_rev
        script = os.path.join(prep, V96_CHECKER)
        header = ("artifact=baseline checker=v95 rev=%s counter_sha=%s "
                  "counter_source=%s receipts=%s" % (
                      rev, self.counter_sha, self.counter_source, self.receipts_note))
        r, _ = self.run("forge-baseline.v95", script, self.v95_args(prep, rev),
                        self.child_env, header)
        ok = r.returncode == 0 and any(
            l.strip() == CLEAN_LINE for l in r.stdout.splitlines())
        self.record("baseline", "v96", r, "exit 0 + " + CLEAN_LINE, ok)

        v94 = self.v94_script()
        header = ("artifact=baseline checker=v94@%s checker_sha256=%s rev=%s "
                  "receipts=%s" % (V94_REV, self.v94_sha, V94_REV, V96_RECEIPTS))
        r, _ = self.run("forge-baseline.v94", v94,
                        self.v94_args(prep, V96_RECEIPTS), self.child_env, header)
        ok = r.returncode == 0 and any(
            l.strip() == CLEAN_LINE for l in r.stdout.splitlines())
        self.record("baseline", "v94", r, "exit 0 + " + CLEAN_LINE, ok)

    def handwritten(self):
        clone = self.clone(self.prep, os.path.join(self.work, "handwritten"))
        self.toplevel(clone)
        self.git(clone, ["rm", "-q", "%s/figure.out" % V96_RECEIPTS])
        rev = self.commit(clone, "forge-handwritten: drop figure receipt from the store")
        original = self.blob(self.prep, self.instrument_rev,
                             "%s/figure.out" % V96_RECEIPTS).decode("utf-8")
        conj = [l for l in original.splitlines() if l.startswith("C1_CONJUNCTS ")][0]
        forged = ("counter_sha=%s\nforged=handwritten-worktree-only\nexit=1\n%s\n"
                  % (self.counter_sha, conj))
        self.write(os.path.join(clone, V96_RECEIPTS, "figure.out"), forged.encode())

        script = os.path.join(clone, V96_CHECKER)
        header = ("artifact=forge-handwritten checker=v95 rev=%s receipt=%s "
                  "written_only_in_worktree=1 counter_sha=%s" % (
                      rev, "%s/figure.out" % V96_RECEIPTS, self.counter_sha))
        r, _ = self.run("forge-handwritten.v95", script,
                        self.v95_args(clone, rev), self.child_env, header)
        ok = r.returncode == 1 and any(
            l.startswith("DISPOSITION_FINDING receipt-absent-at-rev figure:") for l in r.stdout.splitlines())
        self.record("forge-handwritten", "v96", r, "exit 1 receipt-absent-at-rev figure", ok)

        v94 = os.path.join(self.work, "v94-checker-" + V94_REV + ".py")
        header = ("artifact=forge-handwritten checker=v94@%s rev=%s receipts=%s "
                  "reads=filesystem" % (V94_REV, V94_REV, V96_RECEIPTS))
        r, _ = self.run("forge-handwritten.v94", v94,
                        self.v94_args(clone, V96_RECEIPTS), self.child_env, header)
        ok = r.returncode == 0 and any(
            l.strip() == CLEAN_LINE for l in r.stdout.splitlines())
        self.record("forge-handwritten", "v94", r, "exit 0 " + CLEAN_LINE, ok)

    def forge_counter_sha(self):
        clone = self.clone(self.prep, os.path.join(self.work, "counter-sha"))
        self.toplevel(clone)
        path = os.path.join(clone, V96_RECEIPTS, "inverted.out")
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines(True)
        for i, line in enumerate(lines):
            if line.startswith("counter_sha="):
                lines[i] = "counter_sha=" + "0" * 64 + "\n"
                break
        else:
            raise RuntimeError("inverted.out carries no counter_sha= line")
        with open(path, "w", encoding="utf-8") as f:
            f.write("".join(lines))
        rev = self.commit(clone, "forge-counter-sha: zero the inverted receipt binding")

        script = os.path.join(clone, V96_CHECKER)
        header = ("artifact=forge-counter-sha checker=v95 rev=%s receipt=%s "
                  "counter_sha=%s" % (rev, "%s/inverted.out" % V96_RECEIPTS, "0" * 64))
        r, _ = self.run("forge-counter-sha.v95", script,
                        self.v95_args(clone, rev), self.child_env, header)
        ok = r.returncode == 1 and any(
            l.startswith("DISPOSITION_FINDING receipt-counter-sha-mismatch mismatched0:")
            for l in r.stdout.splitlines())
        self.record("forge-counter-sha", "v96", r,
                    "exit 1 receipt-counter-sha-mismatch mismatched0", ok)

        v94 = os.path.join(self.work, "v94-checker-" + V94_REV + ".py")
        header = ("artifact=forge-counter-sha checker=v94@%s rev=%s receipts=%s "
                  "reads=filesystem" % (V94_REV, V94_REV, V96_RECEIPTS))
        r, _ = self.run("forge-counter-sha.v94", v94,
                        self.v94_args(clone, V96_RECEIPTS), self.child_env, header)
        ok = r.returncode == 0 and any(
            l.strip() == CLEAN_LINE for l in r.stdout.splitlines())
        self.record("forge-counter-sha", "v94", r, "exit 0 " + CLEAN_LINE, ok)

    def replace_ref(self):
        clone = self.clone(self.prep, os.path.join(self.work, "replace-ref"))
        self.toplevel(clone)
        old = self.git(clone, ["rev-parse", "%s:%s" % (V94_REV, V94_COUNTER)]).stdout.strip()
        new = self.git(clone, ["rev-parse", "%s:%s" % (self.instrument_rev, V96_COUNTER)]).stdout.strip()
        self.git(clone, ["replace", old, new])
        listed = self.git(clone, ["replace", "-l"]).stdout.strip()
        if listed != old:
            raise RuntimeError("replace ref not written as expected: %r" % listed)
        new_bytes = self.blob(clone, self.instrument_rev, V96_COUNTER)
        new_sha = self.sha256(new_bytes)

        script = os.path.join(clone, V96_CHECKER)
        header = ("artifact=forge-replace-ref checker=v95 rev=%s replace=%s->%s" % (
            self.instrument_rev, old, new_sha))
        r, _ = self.run("forge-replace-ref.v95", script,
                        self.v95_args(clone, self.instrument_rev), self.child_env, header)
        ok = r.returncode == 2 and any(
            l.strip() == "DISPOSITION_SETUP replace-refs-present" for l in r.stdout.splitlines())
        self.record("forge-replace-ref", "v96", r,
                    "exit 2 DISPOSITION_SETUP replace-refs-present", ok)

        v94 = os.path.join(self.work, "v94-checker-" + V94_REV + ".py")
        header = ("artifact=forge-replace-ref checker=v94@%s rev=%s receipts=%s "
                  "expects_read_of_substituted_blob=%s" % (
                      V94_REV, V94_REV, V96_RECEIPTS, new_sha))
        r, _ = self.run("forge-replace-ref.v94", v94,
                        self.v94_args(clone, V96_RECEIPTS), self.child_env, header)
        instrument = [l for l in r.stdout.splitlines()
                      if l.startswith("DISPOSITION_INSTRUMENT sha256=")]
        read_sha = instrument[0].split("sha256=", 1)[1].split()[0] if instrument else ""
        ok = (r.returncode == 0
              and any(l.strip() == CLEAN_LINE for l in r.stdout.splitlines())
              and read_sha == new_sha)
        self.record("forge-replace-ref", "v94", r,
                    "exit 0 + read substituted blob " + new_sha, ok,
                    extra="instrument_sha256=" + (read_sha or "absent"))

    # ---- main --------------------------------------------------------
    def run_all(self):
        self.prepare()
        self.baseline()
        self.handwritten()
        self.forge_counter_sha()
        self.replace_ref()
        lines = [
            "# round-96 C2 forge matrix",
            "lane=%s" % self.lane,
            "lane_head=%s" % self.lane_head,
            "prep=%s" % self.prep,
            "instrument_rev=%s" % self.instrument_rev,
            "checker_sha256=%s" % self.checker_sha,
            "manifest_sha256=%s" % self.manifest_sha,
            "counter_source=%s" % self.counter_source,
            "counter_sha=%s" % self.counter_sha,
            "v94_checker_rev=%s corpus_sha256=%s" % (V94_REV, getattr(self, "v94_sha", "")),
            "receipts=%s" % self.receipts_note,
            "",
            "%-18s %-4s %-58s %s %s" % ("artifact", "chk", "expected", "MATCH", "got"),
        ]
        failed = 0
        for artifact, checker, expected, got, ok, extra in self.checks:
            lines.append("%-18s %-4s %-58s %-5s %s%s" % (
                artifact, checker, expected, "yes" if ok else "NO", got,
                (" " + extra) if extra else ""))
            failed += 0 if ok else 1
        lines.append("")
        lines.append("summary: %d checks, %d failed" % (len(self.checks), failed))
        text = "\n".join(lines) + "\n"
        with open(os.path.join(self.outdir, "forge-matrix.txt"), "w", encoding="utf-8") as f:
            f.write(text)
        sys.stdout.write(text)
        return 0 if failed == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True, help="empty scratch dir for the clones")
    ap.add_argument("--outdir", required=True, help="receipt dir")
    ap.add_argument("--instrument-rev", default=None,
                    help="read the v96 instrument from this lane revision instead of the work tree")
    a = ap.parse_args()
    try:
        f = Forge(a.lane, a.work, a.outdir, a.instrument_rev)
        return f.run_all()
    except RuntimeError as e:
        print("FORGE_SETUP " + str(e))
        return 2


if __name__ == "__main__":
    sys.exit(main())
