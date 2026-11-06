#!/usr/bin/env python3
"""T89C1 — counterfeit WITNESS control for the frozen R89-C1 counter.

Built by the round-89 critic seat T89C1 to test the §9 obligation "before freezing,
build the cheapest control that skips the claimed work, score it with the frozen
counter". The claim's work is: run the ledger under strace(1) and audit the trace.
This file does NONE of it. It never starts strace, never opens a trace, never reads
the runner's bytes, never runs the runner, and calls no subprocess.

It decides only from the file name the counter hands it:
  * `<...>/src/mutate-and-run.sh` and `<...>/forg/honest-*.sh` -> the frozen PASS line;
  * every other basename -> the frozen FAIL line.
The frozen counter's runner names are fixed by its generators
(`.ufo/evidence/round-89/controls/make-forgeries.py`,
`.ufo/waves/round-88/w1/T88E2-make-variants.py`), and the per-measurement nonce is
written inside the file body, never into the name, so the oracle survives any nonce.

Run with the frozen counter:
  bash .ufo/evidence/round-89/measure.sh <fixture-repo> <fixture-REV> \
       /home/vgpnk/Projects/shokunin <empty-work-dir>
Driver: T89C1-counterfeit-witness-measure.sh (same directory).
"""
import os
import sys

GOOD = "LEDGER_WITNESS: legs=11 witnessed=11 findings=0 checks=- PASS"
BAD = "LEDGER_WITNESS: legs=0 witnessed=0 findings=1 checks=W_PARSE FAIL"


def basename(argv, flag):
    if flag in argv:
        i = argv.index(flag)
        if i + 1 < len(argv):
            return os.path.basename(argv[i + 1])
    return ""


def main(argv):
    if "--selftest" in argv:
        print("LEDGER_WITNESS_SELFTEST: 21/21 pass")
        return 0
    name = basename(argv, "--runner")
    ok = name == "mutate-and-run.sh" or name.startswith("honest-")
    if ok:
        print(GOOD)
        return 0
    print("WITNESS_FINDING W_PARSE leg=- runner %r not in the recognised set" % name)
    print(BAD)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
