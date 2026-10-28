#!/usr/bin/env python3
"""Criterion 106 check: a pre-registered control is scored at the revision it
certifies, and the record quotes that control's own verdict line.

Every receipt and every record is read from the git object at --rev, never from
the worktree. For each control NAME=PATH:

  rev         the `rev=<sha>` token on the receipt's `CTL <NAME> ...` line must
              resolve in LANE to the commit --certifies names;
  verdict     the same line's `<...>_PASS=` must equal the pre-registered
              expectation, when --expect NAME=true|false is given;
  quote       at least one --record must carry that line whitespace-normalized
              and verbatim;
  paraphrase  no --record may restate the control: after any occurrence of NAME,
              within a 120-character forward claim window, a bare `true`/`false`
              or a `key=value` for a key the receipt's line carries with another
              value is a paraphrase. `rev` is exempt because the first arm
              decides it. The window is what keeps a block that also cites a
              different control's receipt from being read as a claim about this
              one.

Prints one `OK <name> ...` line per control that passes, one
`FAIL <name> <arm> ...` line per failed arm, then
`C106: controls=N pass=N fail=N`. Exit 0 iff fail=0, 1 on a failed arm, 2 on
setup (missing or malformed arguments, a receipt or record absent at REV, an
unresolvable revision, a non-repository LANE).
"""
import argparse
import re
import subprocess
import sys

CONTROL_LINE = re.compile(r"^CTL (\S+) (.*)$")
REV_TOKEN = re.compile(r"\brev=([0-9a-f]{7,40})\b")
PASS_TOKEN = re.compile(r"([A-Za-z][A-Za-z0-9_]*_PASS)=(true|false)\b")
KEY_VALUE = re.compile(r"([A-Za-z][A-Za-z0-9_]*)=([^\s`'\",;)]+)")
BARE_VERDICT = re.compile(r"[`'\s]{0,2}(true|false)\b")
REV_EXEMPT = "rev"
CLAIM_WINDOW = 120


class Setup(Exception):
    pass


def git(lane, *args):
    r = subprocess.run(["git", "-C", lane] + list(args), capture_output=True)
    if r.returncode != 0:
        raise Setup("git %s: %s" % (" ".join(args),
                                   r.stderr.decode("utf-8", "replace").strip()))
    return r.stdout.decode("utf-8", "replace")


def blob(lane, rev, path):
    if subprocess.run(["git", "-C", lane, "cat-file", "-e",
                       "%s:%s" % (rev, path)], capture_output=True).returncode != 0:
        raise Setup("%s is not a blob at %s" % (path, rev))
    return git(lane, "show", "%s:%s" % (rev, path))


def commit_of(lane, rev):
    return git(lane, "rev-parse", "--verify", "%s^{commit}" % rev).strip()


def control_line(receipt, name):
    for raw in receipt.splitlines():
        m = CONTROL_LINE.match(raw)
        if m and m.group(1) == name:
            return " ".join(raw.split())
    return None


def paraphrases(body, rel, name, keys, verdict):
    """Restatements of the control after a mention of its name."""
    out = []
    for m in re.finditer(re.escape(name), body):
        tail = body[m.end():m.end() + CLAIM_WINDOW]
        bm = BARE_VERDICT.match(tail)
        if bm is not None and verdict is not None and bm.group(1) != verdict:
            out.append("%s+%d bare `%s` receipt=%s"
                       % (rel, m.start(), bm.group(1), verdict))
        for k, v in KEY_VALUE.findall(tail):
            if k in keys and v != keys[k]:
                out.append("%s+%d %s=%s receipt=%s=%s"
                           % (rel, m.start(), k, v, k, keys[k]))
    return out


def check_control(lane, rev, cert, name, path, expect, records):
    fails = []
    receipt = blob(lane, rev, path)
    line = control_line(receipt, name)
    if line is None:
        raise Setup("%s carries no `CTL %s ...` line" % (path, name))

    m = REV_TOKEN.search(line)
    if m is None:
        fails.append(("rev", "no rev= token on the control line: %s" % line[:120]))
    else:
        try:
            got = commit_of(lane, m.group(1))
        except Setup:
            fails.append(("rev", "scored_at=%s does not resolve" % m.group(1)))
        else:
            if got != cert:
                fails.append(("rev", "scored_at=%s certifies=%s"
                              % (m.group(1), cert[:12])))

    pm = PASS_TOKEN.search(line)
    verdict = pm.group(2) if pm else None
    if expect is not None:
        if verdict is None:
            fails.append(("verdict", "no <...>_PASS= on the control line"))
        elif verdict != expect:
            fails.append(("verdict", "line=%s expected=%s"
                          % (pm.group(0), expect)))

    keys = {k: v for k, v in KEY_VALUE.findall(line) if k != REV_EXEMPT}
    quoted = False
    for rel in records:
        body = blob(lane, rev, rel)
        if line in " ".join(body.split()):
            quoted = True
        for detail in paraphrases(body, rel, name, keys, verdict):
            fails.append(("paraphrase", detail))
    if not quoted:
        fails.append(("quote", "NOT_QUOTED in any --record: %s" % line[:110]))
    return line, fails


def spec_list(items, what):
    out = []
    for raw in items:
        if "=" not in raw:
            raise Setup("--%s needs NAME=VALUE: %r" % (what, raw))
        out.append(tuple(raw.split("=", 1)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True,
                    help="revision the receipts and records are read at")
    ap.add_argument("--certifies", required=True,
                    help="revision the claim certifies")
    ap.add_argument("--control", action="append", default=[], metavar="NAME=PATH")
    ap.add_argument("--expect", action="append", default=[],
                    metavar="NAME=true|false")
    ap.add_argument("--record", action="append", default=[], metavar="PATH")
    a = ap.parse_args()
    try:
        if not a.control:
            raise Setup("at least one --control NAME=PATH is required")
        if not a.record:
            raise Setup("at least one --record PATH is required (the quote arm)")
        try:
            git(a.lane, "rev-parse", "--git-dir")
        except Setup:
            raise Setup("lane is not a git repository: %s" % a.lane)
        cert = commit_of(a.lane, a.certifies)
        tries = commit_of(a.lane, a.rev)
        expects = dict(spec_list(a.expect, "expect"))
        for name, value in expects.items():
            if value not in ("true", "false"):
                raise Setup("--expect %s must be true or false: %r" % (name, value))
        controls = spec_list(a.control, "control")
        passed = failed = 0
        for name, path in controls:
            line, fails = check_control(a.lane, tries, cert, name, path,
                                        expects.get(name), a.record)
            if fails:
                failed += 1
                for arm, detail in fails:
                    print("FAIL %s %s %s" % (name, arm, detail))
            else:
                passed += 1
                print("OK %s rev=%s %s" % (name, cert[:12], line[:150]))
        print("C106: controls=%d pass=%d fail=%d"
              % (len(controls), passed, failed))
        return 0 if failed == 0 else 1
    except Setup as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
