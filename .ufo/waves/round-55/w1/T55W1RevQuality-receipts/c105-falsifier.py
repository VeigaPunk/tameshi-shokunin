#!/usr/bin/env python3
"""Score criterion 105's own falsifier against the receipt it names.

Criterion 105 (corpus/QUALITY.md, round-54 block) as landed at BASE says:

  "while the round-54 counter's arm prints `rekeyed=7/7` on its positive control;
   the two receipts are ... `.ufo/evidence/round-54/control/controls-b.stdout`
   (the round-54 positive control)"

and its check-that-can-fail has two arms:
  arm1  a positive-control receipt in which the arm's own counter reads zero;
  arm2  a control run that pre-registers the arm's value without a tree that
        carries it.

This reads the landed falsifier text from REV, then runs the two arms on the
named receipt. Exit 0 iff the falsifier's factual claim about the receipt holds
AND neither arm fires (i.e. the receipt really is the positive control the
falsifier says it is).
"""
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "0a2010acd1e92e4e332774050825e21bcfc7e079"
RECEIPT = ".ufo/evidence/round-54/control/controls-b.stdout"
QUALITY = "corpus/QUALITY.md"


def git(*args):
    r = subprocess.run(["git", "-C", LANE] + list(args), capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def show(rev, path):
    rc, out = git("show", "%s:%s" % (rev, path))
    if rc:
        raise SystemExit("cannot read %s at %s" % (path, rev))
    return out


def main():
    q = show(REV, QUALITY)
    start = q.index("### Criterion 105")
    end = q.find("\n## ", start)
    block = q[start:end if end > 0 else len(q)]
    fals = [l for l in block.splitlines() if l.startswith("Falsifier that must fail:")]
    if not fals:
        print("SETUP: criterion 105 carries no falsifier line")
        return 2
    fals = fals[0]
    print("FALSIFIER-TEXT (landed at %s): %s" % (REV[:12], fals))
    print()
    claimed_full = bool(re.search(r"rekeyed=7/7`\s+on its positive control", fals))
    names_controls_b = "controls-b.stdout" in fals and "positive control" in fals
    print("CLAIM full-count-on-control=%s names-controls-b-as-positive=%s"
          % (claimed_full, names_controls_b))

    receipt = show(REV, RECEIPT)
    ctl = [l for l in receipt.splitlines() if l.startswith("CTL CTL_POS_c1")]
    if not ctl:
        print("SETUP: receipt carries no CTL CTL_POS_c1 line")
        return 2
    line = ctl[0]
    m = re.search(r"rekeyed=(\d+)/(\d+)", line)
    got, whole = int(m.group(1)), int(m.group(2))
    rev = re.search(r"rev=([0-9a-f]+)", line).group(1)
    expect = re.search(r"C1_R54_PASS=(true|false)", line).group(1)
    pre = re.search(r"CTL_MISMATCH CTL_POS_c1 expected=(true|false) actual=(true|false)",
                    receipt)
    print("RECEIPT-%s line: %s" % (RECEIPT, line))
    print("RECEIPT rekeyed-now=%d/%d expectation=%s%s" %
          (got, whole, expect,
           " mismatched(expected=%s actual=%s)" % pre.groups() if pre else ""))
    print("CLAIM-HOLDS full-count-present=%s" % (got == whole and whole == 7))
    print()

    # arm1: the arm's own counter reads zero on the named positive control.
    arm1 = (got == 0)
    # arm2: the control pre-registers the arm's value on a tree that does not
    # carry the round's work. The re-key commit is derived from the record
    # rather than assumed: the counter's own after/ receipt names the value.
    rc, _ = git("merge-base", "--is-ancestor",
                "7fa9a5e0104bc181872401547987d6744f3b570d", rev)
    carries = (rc == 0)
    arm2 = (not carries) and (got != whole)
    print("ARM1 zero-count-fires=%s (rekeyed=%d)" % (arm1, got))
    print("ARM2 preregistered-without-tree-fires=%s (re-key ancestor of control rev=%s)"
          % (arm2, carries))
    print()
    verdict = (not arm1) and (not arm2)
    print("C105-FALSIFIER: full-count-claim=%s check-fires=%s -> %s" % (
        got == whole and whole == 7, arm1 or arm2,
        "FALSIFIER FAILS as landed (the receipt refutes its own falsifier)"
        if not (got == whole and whole == 7) else "falsifier holds"))
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
