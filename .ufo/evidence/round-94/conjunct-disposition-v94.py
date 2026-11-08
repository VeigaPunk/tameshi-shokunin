#!/usr/bin/env python3
"""Conjunct-disposition checker (round-94 C2, QUALITY 158 + round-94 A4 upgrade).

A counter's conjunct list is a claim about what the instrument measures. This
checker makes that claim auditable: every conjunct key the frozen counter
prints must have a manifest row that is either

  * a committed battery state whose receipt shows that conjunct FALSE
    (`{"state": "<name>", "mode": "conjunct-false"}`), or
  * a committed setup refusal whose receipt shows the named `C1_SETUP` token
    (`{"state": "<name>", "mode": "setup-refusal", "token": "<token>"}`), or
  * `{"unfalsifiable": "<reason>"}` with a reason of at least 40 characters
    that names the mechanism that forbids the falsifier.

A manifest key the counter does not print is a finding (a stale row is a
self-assessment that no longer describes the instrument). A missing row, a
missing receipt, a row whose receipt does not move the conjunct, and a
contentless `unfalsifiable` reason are each findings.

Usage:
  python3 -I tools/conjunct-disposition.py --lane LANE --rev REV \
      [--counter PATH] [--manifest PATH] [--receipts DIR]
  python3 -I tools/conjunct-disposition.py --selftest

Exit: 0 no findings; 1 findings (each printed as `DISPOSITION_FINDING <id> <detail>`);
      2 setup refusal (unreadable counter or manifest); 64 usage.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

COUNTER = ".ufo/evidence/round-94/c1/measure-v94.py"
MANIFEST = ".ufo/evidence/round-94/conjunct-disposition.json"
RECEIPTS = ".ufo/evidence/round-94/pre-freeze/controls"
MIN_REASON = 40
MECHANISM = ("pin", "sealed", "seal", "gate bytes", "GIT_", "pinned", "replace")
# Round-94 A4: an unfalsifiable reason is sound only when it names a concrete
# battery state or a pin digest, not just a mechanism word. The old substring
# test accepts "the pin forbids it"; the new test requires a state name or a
# 64-hex digest (or a short-prefix digest >=12 hex) or a backtick-quoted
# artifact. See check() and --selftest case 7 (the A4 cheat) which must fail.
DIGEST_RE = re.compile(r"[0-9a-f]{64}|[0-9a-f]{12,}")


def names_a_state_or_digest(reason, receipt_dir):
    """Round-94 A4 (rev 2): the reason must name a DECLARED battery state (the word
    `state` followed by a receipt name that exists in the receipt dir) or a hex digest.
    The word `state` in prose is not a state: the first rev matched `state exists` and
    let a 96-character mechanism-only reason through (control receipt
    pre-freeze/c2-cheat-mechanism-word.out, rev 1)."""
    if DIGEST_RE.search(reason):
        return True
    try:
        names = {f[:-4] for f in os.listdir(receipt_dir) if f.endswith(".out")}
    except OSError:
        names = set()
    for m in re.finditer(r"state[s]?\s+([A-Za-z0-9_.-]+)", reason):
        if m.group(1).strip(".,;:`") in names:
            return True
    return False


def die(msg):
    print("DISPOSITION_SETUP " + msg)
    return 2


def parse_conjuncts(text):
    for line in text.split("\n"):
        if line.startswith("C1_CONJUNCT_KEYS "):
            return line.split()[1:]
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


def check(keys, rows, receipt_dir):
    """keys: counter's conjunct key list. rows: manifest 'rows'. Returns findings."""
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
            elif not names_a_state_or_digest(reason, receipt_dir):
                findings.append(("reason-names-no-state-or-digest", k,
                                 "the reason must name a declared battery state (state <name>) or a hex digest, not only a mechanism word: " + reason[:80]))
            continue
        mode = row.get("mode")
        state = row.get("state")
        if mode not in ("conjunct-false", "setup-refusal"):
            findings.append(("bad-mode", k, "mode=%r" % (mode,)))
            continue
        if not state:
            findings.append(("no-state", k, "row names no state"))
            continue
        path = os.path.join(receipt_dir, state + ".out")
        if not os.path.exists(path):
            findings.append(("no-receipt", k, "receipt absent: " + path))
            continue
        body = open(path, encoding="utf-8", errors="replace").read()
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


def selftest():
    """Six cases; three must produce a finding, three must not."""
    cases = []
    keys = ["alpha", "beta", "gamma"]
    with tempfile.TemporaryDirectory() as d:
        def receipt(name, conj):
            body = "exit=1\nC1_CONJUNCTS " + " ".join("%s=%s" % (k, str(v).lower())
                                                      for k, v in conj.items()) + "\n"
            open(os.path.join(d, name + ".out"), "w").write(body)

        receipt("st-alpha", dict(alpha=False, beta=True, gamma=True))
        receipt("st-token", dict(alpha=True, beta=True, gamma=True))
        open(os.path.join(d, "st-token.out"), "w").write("exit=2\nC1_SETUP spec-absent-at-rev\n")
        clean = {"alpha": {"state": "st-alpha", "mode": "conjunct-false"},
                 "beta": {"state": "st-token", "mode": "setup-refusal", "token": "spec-absent-at-rev"},
                 "gamma": {"unfalsifiable": "needs a nondeterministic gate, which the sealed pin at state st-alpha forbids"}}
        cases.append(("clean", clean, 0))
        m = dict(clean)
        del m["beta"]
        cases.append(("missing-row", m, 1))
        m = dict(clean)
        m["beta"] = {"state": "st-alpha", "mode": "conjunct-false"}
        cases.append(("no-flip", m, 1))
        m = dict(clean)
        m["gamma"] = {"unfalsifiable": "unknown"}
        cases.append(("reason-too-short", m, 1))
        m = dict(clean)
        m["delta"] = {"state": "st-alpha", "mode": "conjunct-false"}
        cases.append(("unknown-key", m, 1))
        m = dict(clean)
        m["beta"] = {"state": "absent-receipt", "mode": "conjunct-false"}
        cases.append(("no-receipt", m, 1))
        # Round-94 A4: a mechanism-word reason with no state/digest must now be a finding.
        m = dict(clean)
        m["gamma"] = {"unfalsifiable": "the sealed pin forbids it"}
        cases.append(("a4-mechanism-word-cheat", m, 1))
        m = dict(clean)
        m["gamma"] = {"unfalsifiable": "the sealed pin and the pinned gate bytes forbid any committed "
                                       "falsifier, so no such state exists and none can be built"}
        cases.append(("a4-prose-state-word-cheat", m, 1))
        m = dict(clean)
        m["gamma"] = {"unfalsifiable": "the sealed pin at state timeout with digest 3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30 forbids it"}
        cases.append(("a4-digest-named", m, 0))
        passed = 0
        for name, rows, want in cases:
            got = check(keys, rows, d)
            ok = (len(got) == 0) == (want == 0)
            print("SELFTEST %s %s findings=%d want_clean=%d %s" % (
                name, "PASS" if ok else "FAIL", len(got), want == 0,
                ",".join(f[0] for f in got)))
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
    lane = os.path.realpath(a.lane)
    blob = subprocess.run(["git", "-C", lane, "cat-file", "blob",
                           a.rev + ":" + a.counter], capture_output=True)
    if blob.returncode != 0:
        sys.exit(die("counter-absent-at-rev"))
    with tempfile.TemporaryDirectory() as d:
        cp = os.path.join(d, "counter.py")
        open(cp, "wb").write(blob.stdout)
        p = subprocess.run([sys.executable, "-I", cp, "--conjuncts"],
                           capture_output=True, text=True)
    keys = parse_conjuncts(p.stdout)
    if not keys:
        sys.exit(die("counter-prints-no-conjunct-keys:" + p.stdout.strip()[:120]))
    mb = subprocess.run(["git", "-C", lane, "cat-file", "blob", a.rev + ":" + a.manifest],
                        capture_output=True)
    if mb.returncode != 0:
        sys.exit(die("manifest-absent-at-rev"))
    try:
        rows = json.loads(mb.stdout)["rows"]
    except Exception:
        sys.exit(die("manifest-unparsable"))
    rdir = os.path.join(lane, a.receipts)
    print("DISPOSITION_INSTRUMENT sha256=" + __import__("hashlib").sha256(blob.stdout).hexdigest()
          + " conjuncts=%d" % len(keys))
    sys.exit(report(check(keys, rows, rdir), len(keys), rows, a.min_falsifiable))


if __name__ == "__main__":
    main()
