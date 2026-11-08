#!/usr/bin/env python3
"""Conjunct-disposition checker, round-95 C2 (sealed object-store audit).

A counter's conjunct list is a claim about what the instrument measures. This
checker makes that claim auditable: every conjunct key the frozen counter
prints must have a manifest row that is either

  * a committed battery state whose receipt shows that conjunct FALSE
    (`{"state": "<name>", "mode": "conjunct-false"}`), or
  * a committed setup refusal whose receipt shows the named `C1_SETUP` token
    (`{"state": "<name>", "mode": "setup-refusal", "token": "<token>"}`), or
  * `{"unfalsifiable": "<reason>"}` with a reason of at least 40 characters
    that names the mechanism that forbids the falsifier and a declared battery
    state or a hex digest.

Round-95 changes (plan §C2 / A7), nothing else:

  * receipts are read from the object store at `--rev`
    (`git cat-file blob <rev>:<receipts>/<state>.out`), never from the
    filesystem, so a receipt that exists only in the working tree is absent;
  * every receipt named by a state row must carry `counter_sha=<64 hex>` equal
    to the sha256 of the counter blob at `--rev`; the first `counter_sha=` line
    is authoritative;
  * every git call runs under a scrubbed environment (`GIT_NO_REPLACE_OBJECTS=1`,
    `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, no inherited
    `GIT_*`), and `git -C <lane> replace -l` must be empty before any read;
  * the reason test consults the states present in the object store.

A manifest key the counter does not print is a finding (a stale row is a
self-assessment that no longer describes the instrument). A missing row, a
receipt absent at the revision, a receipt whose `counter_sha=` is absent or
different, a row whose receipt does not move the conjunct, and a contentless
`unfalsifiable` reason are each findings.

Usage:
  python3 -I .ufo/evidence/round-95/conjunct-disposition-v95.py --lane LANE \
      --rev REV [--counter PATH] [--manifest PATH] [--receipts DIR] \
      [--min-falsifiable N]
  python3 -I .ufo/evidence/round-95/conjunct-disposition-v95.py --selftest

Exit: 0 no findings; 1 findings (each printed as `DISPOSITION_FINDING <id> <detail>`);
      2 setup refusal (replace refs present, unreadable counter or manifest); 64 usage.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

COUNTER = ".ufo/evidence/round-95/c1/measure-v95.py"
MANIFEST = ".ufo/evidence/round-95/conjunct-disposition.json"
RECEIPTS = ".ufo/evidence/round-95/pre-freeze/controls"
MIN_REASON = 40
MECHANISM = ("pin", "sealed", "seal", "gate bytes", "GIT_", "pinned", "replace")
# The reason is sound only when it names a concrete battery state or a pin
# digest, not just a mechanism word. DIGEST_RE keeps round-94's acceptance
# (64 hex or a short-prefix digest of at least 12 hex).
DIGEST_RE = re.compile(r"[0-9a-f]{64}|[0-9a-f]{12,}")
SHA_RE = re.compile(r"[0-9a-f]{64}")


def sealed_env():
    """Explicit environment: path pinned, HOME/TMPDIR under scratch, no GIT_*."""
    import tempfile as _tf
    _scratch = os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku")
    _home = os.path.join(_scratch, "tameshi-r96-checker-home")
    _tmp = os.path.join(_home, "tmp")
    os.makedirs(_tmp, exist_ok=True)
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "HOME": _home, "TMPDIR": _tmp,
            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null"}


GIT = "/usr/bin/git"


def git(lane, args, env, text=False):
    return subprocess.run([GIT, "-C", lane] + args, capture_output=True,
                          text=text, env=env)


def die(msg):
    print("DISPOSITION_SETUP " + msg)
    return 2


def parse_conjuncts(text):
    for line in text.split("\n"):
        if line.startswith("C1_CONJUNCT_KEYS "):
            return line.split()[1:]
    return None


def parse_counter_sha(body):
    """First `counter_sha=` line only, exactly as the battery writes it."""
    for line in body.split("\n"):
        s = line.strip()
        if s.startswith("counter_sha="):
            return s.split("=", 1)[1].strip()
    return None


def receipt_conjuncts(body):
    conj = {}
    for line in body.split("\n"):
        if line.startswith("C1_CONJUNCTS "):
            for kv in line.split()[1:]:
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    conj[k] = (v.strip() == "true")
    return conj


def names_a_state_or_digest(reason, present_states):
    """A reason names a hex digest or a state present in the object store."""
    if DIGEST_RE.search(reason):
        return True
    for m in re.finditer(r"state[s]?\s+([A-Za-z0-9_.-]+)", reason):
        if m.group(1).strip(".,;:`") in present_states:
            return True
    return False


class GitStore:
    """Read-only view of one lane revision: blobs and the receipts tree."""

    def __init__(self, lane, rev, receipts, env):
        self.lane = os.path.realpath(lane)
        self.rev = rev
        self.receipts = receipts.rstrip("/") if receipts != "/" else receipts
        self.env = env

    def receipt_path(self, state):
        return "%s:%s/%s.out" % (self.rev, self.receipts, state)

    def read_blob(self, path):
        r = git(self.lane, ["cat-file", "blob", "%s:%s" % (self.rev, path)],
                self.env)
        if r.returncode != 0:
            return None
        return r.stdout

    def read_receipt(self, state):
        blob = self.read_blob("%s/%s.out" % (self.receipts, state))
        if blob is None:
            return None
        return blob.decode("utf-8", "replace")

    def states(self):
        r = git(self.lane, ["ls-tree", "-r", "--name-only",
                            "%s:%s" % (self.rev, self.receipts)], self.env)
        if r.returncode != 0:
            return set()
        names = set()
        for name in r.stdout.decode("utf-8", "replace").splitlines():
            base = name.rsplit("/", 1)[-1]
            if base.endswith(".out"):
                names.add(base[:-4])
        return names


def check(keys, rows, store, counter_sha, present_states):
    """keys: counter's conjunct key list. Returns findings."""
    findings = []
    for k in keys:
        row = rows.get(k)
        if row is None:
            findings.append(("missing-row", k, "the counter prints this conjunct and the manifest has no row"))
            continue
        if "unfalsifiable" in row:
            reason = str(row["unfalsifiable"]).strip()
            if len(reason) < MIN_REASON:
                findings.append(("reason-too-short", k, "%d chars, minimum %d" % (len(reason), MIN_REASON)))
            elif not any(tok.lower() in reason.lower() for tok in MECHANISM):
                findings.append(("reason-names-no-mechanism", k,
                                 "the reason names no seal/pin mechanism: " + reason[:80]))
            elif not names_a_state_or_digest(reason, present_states):
                findings.append(("reason-names-no-state-or-digest", k,
                                 "the reason must name a committed battery state (state <name>) or a hex digest, not only a mechanism word: " + reason[:80]))
            continue
        mode = row.get("mode")
        state = row.get("state")
        if mode not in ("conjunct-false", "setup-refusal"):
            findings.append(("bad-mode", k, "mode=%r" % (mode,)))
            continue
        if not state:
            findings.append(("no-state", k, "row names no state"))
            continue
        body = store.read_receipt(state)
        if body is None:
            findings.append(("receipt-absent-at-rev", k,
                             "receipt absent from the object store at %s (looked for %s)"
                             % (store.rev, store.receipt_path(state))))
            continue
        got_sha = parse_counter_sha(body)
        if got_sha is None or not SHA_RE.fullmatch(got_sha) or got_sha != counter_sha:
            findings.append(("receipt-counter-sha-mismatch", k,
                             "receipt %s carries counter_sha=%r, counter blob sha256=%s"
                             % (state, got_sha, counter_sha)))
            continue
        if mode == "setup-refusal":
            token = str(row.get("token", ""))
            if not token or ("C1_SETUP " + token) not in body:
                findings.append(("token-absent", k, "receipt does not print C1_SETUP " + token))
            continue
        conj = receipt_conjuncts(body)
        if k not in conj:
            findings.append(("conjunct-absent", k, "receipt prints no C1_CONJUNCTS line for it"))
        elif conj[k] is not False:
            findings.append(("no-flip", k, "receipt shows %s=%s on state %s" % (k, conj[k], state)))
    for k in rows:
        if k not in keys:
            findings.append(("unknown-key", k, "the manifest names a conjunct the counter does not print"))
    return findings


def report(findings, n, rows, min_falsifiable=0):
    unf = sum(1 for v in rows.values() if isinstance(v, dict) and "unfalsifiable" in v)
    fals = sum(1 for v in rows.values() if isinstance(v, dict) and "unfalsifiable" not in v)
    if min_falsifiable and fals < min_falsifiable:
        findings.append(("falsifiable-below-minimum", "-",
                         "falsifiable=%d < --min-falsifiable=%d" % (fals, min_falsifiable)))
    for fid, key, detail in findings:
        print("DISPOSITION_FINDING %s %s: %s" % (fid, key, detail))
    for k, v in sorted(rows.items()):
        if isinstance(v, dict) and "unfalsifiable" in v:
            print("DISPOSITION_ROW %s unfalsifiable" % k)
        elif isinstance(v, dict):
            print("DISPOSITION_ROW %s state=%s mode=%s" % (k, v.get("state"), v.get("mode")))
    print("DISPOSITION rows=%d falsifiable=%d unfalsifiable=%d findings=%d" % (
        n, fals, unf, len(findings)))
    return 0 if not findings else 1


def _git_mutate(repo, args, env):
    r = subprocess.run([GIT, "-C", repo] + args, capture_output=True,
                       text=True, env=env)
    if r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), r.stderr.strip()))
    return r


def selftest():
    """Eleven cases; the store is a real git repo, so reads exercise cat-file."""
    keys = ["alpha", "beta", "gamma"]
    env = sealed_env()
    with tempfile.TemporaryDirectory(prefix="disposition-selftest-") as base:
        repo = os.path.join(base, "store")
        os.makedirs(repo)
        _git_mutate(repo, ["init", "-q"], env)
        counter = os.path.join(repo, "counter.py")
        with open(counter, "w", encoding="utf-8") as f:
            f.write("#!/usr/bin/env python3\n# selftest counter bytes\n")
        receipts = os.path.join(repo, "receipts")
        os.makedirs(receipts)
        with open(counter, "rb") as f:
            counter_sha = hashlib.sha256(f.read()).hexdigest()

        def write_receipt(name, body):
            with open(os.path.join(receipts, name + ".out"), "w", encoding="utf-8") as f:
                f.write("counter_sha=%s\n" % counter_sha + body)

        write_receipt("st-alpha", "exit=1\nC1_CONJUNCTS alpha=false beta=true gamma=true\n")
        write_receipt("st-token", "exit=2\nC1_SETUP spec-absent-at-rev\n")
        _git_mutate(repo, ["add", "-A"], env)
        _git_mutate(repo, ["-c", "user.name=selftest", "-c", "user.email=selftest@invalid",
                           "commit", "-qm", "clean receipts"], env)
        with open(os.path.join(receipts, "sha-cheat.out"), "w", encoding="utf-8") as f:
            f.write("counter_sha=" + "0" * 64
                    + "\nexit=1\nC1_CONJUNCTS alpha=false beta=true gamma=true\n")
        _git_mutate(repo, ["add", "-A"], env)
        _git_mutate(repo, ["-c", "user.name=selftest", "-c", "user.email=selftest@invalid",
                           "commit", "-qm", "counter-sha cheat receipt"], env)
        rev = _git_mutate(repo, ["rev-parse", "HEAD"], env).stdout.strip()
        # Worktree-only cheat: written after the last commit, never added.
        write_receipt("wt-cheat", "exit=1\nC1_CONJUNCTS alpha=false beta=true gamma=true\n")

        store = GitStore(repo, rev, "receipts", env)
        blob_sha = hashlib.sha256(store.read_blob("counter.py")).hexdigest()
        if blob_sha != counter_sha:
            raise RuntimeError("selftest counter digest changed between file and blob")
        present = store.states()

        clean = {"alpha": {"state": "st-alpha", "mode": "conjunct-false"},
                 "beta": {"state": "st-token", "mode": "setup-refusal", "token": "spec-absent-at-rev"},
                 "gamma": {"unfalsifiable": "the sealed pin at state st-alpha forbids a committed falsifier for it"}}
        cases = []
        cases.append(("clean", clean, 0, None))
        m = dict(clean)
        del m["beta"]
        cases.append(("missing-row", m, 1, None))
        m = dict(clean)
        m["beta"] = {"state": "st-alpha", "mode": "conjunct-false"}
        cases.append(("no-flip", m, 1, None))
        m = dict(clean)
        m["gamma"] = {"unfalsifiable": "unknown"}
        cases.append(("reason-too-short", m, 1, None))
        m = dict(clean)
        m["delta"] = {"state": "st-alpha", "mode": "conjunct-false"}
        cases.append(("unknown-key", m, 1, None))
        m = dict(clean)
        m["beta"] = {"state": "absent-receipt", "mode": "conjunct-false"}
        cases.append(("no-receipt", m, 1, "receipt-absent-at-rev"))
        m = dict(clean)
        m["gamma"] = {"unfalsifiable": "the sealed pin forbids it"}
        cases.append(("a4-mechanism-word-cheat", m, 1, None))
        m = dict(clean)
        m["gamma"] = {"unfalsifiable": "the sealed pin and the pinned gate bytes forbid any committed "
                                       "falsifier, so no such state exists and none can be built"}
        cases.append(("a4-prose-state-word-cheat", m, 1, None))
        m = dict(clean)
        m["gamma"] = {"unfalsifiable": "the sealed pin at state timeout with digest 3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30 forbids it"}
        cases.append(("a4-digest-named", m, 0, None))
        m = dict(clean)
        m["alpha"] = {"state": "wt-cheat", "mode": "conjunct-false"}
        cases.append(("worktree-only-receipt-cheat", m, 1, "receipt-absent-at-rev"))
        m = dict(clean)
        m["alpha"] = {"state": "sha-cheat", "mode": "conjunct-false"}
        cases.append(("counter-sha-cheat", m, 1, "receipt-counter-sha-mismatch"))

        passed = 0
        for name, rows, want, want_id in cases:
            got = check(keys, rows, store, counter_sha, present)
            ids = [f[0] for f in got]
            if want == 0:
                ok = len(got) == 0
            else:
                ok = len(got) > 0 and (want_id is None or want_id in ids)
            print("SELFTEST %s %s findings=%d want=%s %s" % (
                name, "PASS" if ok else "FAIL", len(got),
                "clean" if want == 0 else (want_id or "finding"), ",".join(ids)))
            passed += 1 if ok else 0
    print("DISPOSITION_SELFTEST: %d/%d pass" % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane")
    ap.add_argument("--rev")
    ap.add_argument("--counter", default=COUNTER)
    ap.add_argument("--manifest", default=MANIFEST)
    ap.add_argument("--receipts", default=RECEIPTS)
    ap.add_argument("--min-falsifiable", type=int, default=0)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.lane or not a.rev:
        print(__doc__)
        sys.exit(64)
    if not re.fullmatch(r"[0-9a-f]{40}", a.rev):
        sys.exit(die("rev-not-a-commit-id"))
    _res = git(a.lane, ["rev-parse", a.rev], sealed_env())
    if _res.returncode != 0:
        sys.exit(die("rev-unresolvable"))
    a.rev = _res.stdout.decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40}", a.rev):
        sys.exit(die("rev-unresolvable"))
    lane = os.path.realpath(a.lane)
    env = sealed_env()
    if not os.path.isdir(lane):
        sys.exit(die("lane-absent:" + lane))
    replaces = git(lane, ["replace", "-l"], env)
    if replaces.returncode != 0:
        sys.exit(die("replace-list-failed:" + replaces.stderr.decode("utf-8", "replace").strip()[:160]))
    if replaces.stdout.strip():
        sys.exit(die("replace-refs-present"))
    store = GitStore(lane, a.rev, a.receipts, env)
    counter_blob = store.read_blob(a.counter)
    if counter_blob is None:
        sys.exit(die("counter-absent-at-rev"))
    counter_sha = hashlib.sha256(counter_blob).hexdigest()
    with tempfile.TemporaryDirectory(prefix="disposition-counter-") as d:
        cp = os.path.join(d, "counter.py")
        with open(cp, "wb") as f:
            f.write(counter_blob)
        p = subprocess.run([sys.executable, "-I", cp, "--conjuncts"],
                           capture_output=True, text=True, env=env)
    keys = parse_conjuncts(p.stdout)
    if not keys:
        sys.exit(die("counter-prints-no-conjunct-keys:" + p.stdout.strip()[:120]))
    manifest_blob = store.read_blob(a.manifest)
    if manifest_blob is None:
        sys.exit(die("manifest-absent-at-rev"))
    try:
        rows = json.loads(manifest_blob)["rows"]
    except Exception:
        sys.exit(die("manifest-unparsable"))
    present_states = store.states()
    print("DISPOSITION_INSTRUMENT sha256=" + counter_sha + " conjuncts=%d" % len(keys))
    sys.exit(report(check(keys, rows, store, counter_sha, present_states),
                    len(keys), rows, a.min_falsifiable))


if __name__ == "__main__":
    main()
