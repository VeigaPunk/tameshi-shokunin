#!/usr/bin/env python3
"""R94SC1 probe: what IS the `counter_sha` in the round-93 D01 witness?

Read-only on the lane. It reads the two counter revisions with `git cat-file`
and reproduces, byte for byte, the construction the round-93 driver used for a
removal mutant:

    mutated  = counter_text.replace(anchor, "        pass  # D01: ...\n", 1)
    b        = mutated.encode()
    norm     = SELF_LINE.sub(b"", b)                 # strip the self-pin line
    h        = sha256(norm)
    b2       = SELF_LINE.sub('SELF_SHA256 = "<h>"\n', b, count=1)   # re-pin
    sha256(b2)                                        # what the driver wrote to the receipt

It shows that the D01 witness's `counter_sha=162aff76…` is the MUTATED rev-C
counter (the pre-A3 revision, which carried the stray-verdict rule twice), and
not a byte string any committed battery receipt was produced from.

Usage: R94SC1-d01-counter-sha.py [lane]
"""
import hashlib
import re
import subprocess
import sys

LANE = sys.argv[1] if len(sys.argv) > 1 else "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
SELF_LINE = re.compile(rb'^SELF_SHA256 = "[0-9a-f]{64}"\n', re.M)
ANCHOR = """        toks = [c for c in split_cells(raw) if c in VERDICTS]
        if toks:
            bad.append("stray-verdict:%d:%s" % (oi + 1, raw.strip()[:24]))
"""
REPLACEMENT = "        pass  # D01: stray-verdict scan removed\n"

REVS = [
    ("b34c929e", "rev-C (pre-A3, two copies of the rule)",
     "162aff7612bbfb82e375837c840ababe11f3ae90e780883b8d0462376f67df28"),
    ("855f0c1c", "rev-A3 (one copy of the rule)",
     "4bd4b77ce8b5ae4268b4bfb631cc71650306d4ed8e80126bf5d97509bb0c2d35"),
]


def blob(rev, path):
    p = subprocess.run(["git", "-C", LANE, "cat-file", "blob", "%s:%s" % (rev, path)],
                       capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else ""


def main():
    print("LANE %s" % LANE)
    for rev, label, want in REVS:
        ctr = blob(rev, ".ufo/evidence/round-93/c1/measure-v93.py")
        if not ctr:
            print("%s %s: COUNTER ABSENT" % (rev, label))
            continue
        sites = ctr.count('bad.append("stray-verdict:%d:%s"')
        print("%s  %s" % (rev, label))
        print("   stray-verdict append sites in the counter: %d" % sites)
        print("   D01 anchor occurrences: %d" % ctr.count(ANCHOR))
        mut = ctr.replace(ANCHOR, REPLACEMENT, 1)
        b = mut.encode()
        norm = SELF_LINE.sub(b"", b)
        h = hashlib.sha256(norm).hexdigest()
        b2 = SELF_LINE.sub(('SELF_SHA256 = "%s"\n' % h).encode(), b, count=1)
        got = hashlib.sha256(b2).hexdigest()
        print("   mutated+re-pinned sha256: %s  %s" % (got, "MATCHES" if got == want else "differs from %s" % want))
    print()
    print("The D01 witness (.ufo/waves/round-93/w1/R93SC1-revc-d01-repro.out) carries")
    print("counter_sha=162aff76… -> the MUTATED rev-C counter, so the receipt is a")
    print("mutation study over a scratch copy, not a frozen-driver battery receipt.")


if __name__ == "__main__":
    main()
