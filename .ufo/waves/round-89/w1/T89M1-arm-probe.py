#!/usr/bin/env python3
"""T89M1 — run one selftest fixture arm of a (mutant) witness through its --audit CLI
and print the audit output, so a survivor's firing mechanism can be attributed to a
specific sub-check. Replicates exactly what ledger-witness.py selftest() does for one
arm (build_fixture(root, arm) then `python3 -I <witness> --audit ...`).

Usage: python3 -I T89M1-arm-probe.py <witness> <arm> <scratch-subdir>
"""
import importlib.util
import os
import subprocess
import sys


def main(argv):
    if len(argv) != 3:
        sys.stderr.write(__doc__)
        return 2
    witness, arm, outdir = argv
    spec = importlib.util.spec_from_file_location("witness_under_probe", witness)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    root = os.path.join(outdir, arm.replace(":", "_"))
    os.makedirs(root, exist_ok=True)
    av = mod.build_fixture(root, arm)
    p = subprocess.run([sys.executable, "-I", os.path.abspath(witness)] + av,
                       capture_output=True, text=True)
    sys.stdout.write(p.stdout)
    if p.stderr:
        sys.stderr.write(p.stderr)
    print("PROBE rc=%d arm=%s" % (p.returncode, arm))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
