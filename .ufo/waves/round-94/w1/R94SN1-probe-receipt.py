#!/usr/bin/env python3
"""R94SN1 probe: receipt writer/grader index asymmetry and symlink handling.

Imports the COMMITTED driver (.ufo/evidence/round-94/c1/controls-v94.py) as a
module -- no copy of its code -- and drives receipt_path() / write_receipt() and
the driver's own grading loop against a scratch outdir.

Nothing here writes outside the given scratch directory.

Usage: python3 -I R94SN1-probe-receipt.py <scratch-outdir>
"""
import importlib.util
import os
import shutil
import sys

DRIVER = ("/home/vgpnk/Projects/shokunin/tameshi-shokunin"
          "/.ufo/evidence/round-94/c1/controls-v94.py")


def load_driver():
    spec = importlib.util.spec_from_file_location("drv", DRIVER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def driver_grader(outdir, name):
    """VERBATIM the grading loop from controls-v94.py main()."""
    found = None
    for cand in [name + ".out"] + ["%s.rerun-%d.out" % (name, i) for i in range(1, 50)]:
        p = os.path.join(outdir, cand)
        if os.path.lexists(p):
            found = p          # no break: the LAST (highest-index) match wins
    return found


def main():
    outdir = sys.argv[1]
    shutil.rmtree(outdir, ignore_errors=True)
    os.makedirs(outdir)
    m = load_driver()
    print("driver:", DRIVER)
    print("driver sha256 check: self-pin present =",
          "SELF_SHA256" in open(DRIVER, encoding="utf-8").read())
    print()

    print("== F4: writer picks the LOWEST unused index; grader picks the HIGHEST ==")
    w1 = m.receipt_path(outdir, "ctlX")
    m.write_receipt(w1, "FRESH-RUN-1\n")
    print("  writer run1 ->", os.path.basename(w1))
    # plant a higher-index stale receipt
    m.write_receipt(os.path.join(outdir, "ctlX.rerun-9.out"), "STALE-PLANTED\n")
    w2 = m.receipt_path(outdir, "ctlX")
    m.write_receipt(w2, "FRESH-RUN-2\n")
    print("  writer run2 ->", os.path.basename(w2))
    g = driver_grader(outdir, "ctlX")
    print("  GRADER reads->", os.path.basename(g))
    print("  GRADER content:", open(g).read().strip())
    print("  -> CLAIM FALSIFIED" if open(g).read().strip() == "STALE-PLANTED"
          else "  -> claim holds")
    print()

    print("== F5a: symlink at name.out -> grader dereferences it ==")
    d2 = outdir + ".sym1"
    shutil.rmtree(d2, ignore_errors=True)
    os.makedirs(d2)
    outside = os.path.abspath(outdir + ".outside")
    open(outside, "w").write("EXTERNAL-PLANTED\n")
    os.symlink(outside, os.path.join(d2, "ctlZ.out"))
    print("  writer chooses:", os.path.basename(m.receipt_path(d2, "ctlZ")))
    sel = driver_grader(d2, "ctlZ")
    print("  grader picks  :", os.path.basename(sel))
    print("  content graded:", open(sel).read().strip())
    print("  -> content came from OUTSIDE the outdir:", outside)
    os.remove(outside)
    print()

    print("== F5b: symlink at the highest-index candidate ==")
    d3 = outdir + ".sym2"
    shutil.rmtree(d3, ignore_errors=True)
    os.makedirs(d3)
    outside2 = os.path.abspath(outdir + ".outside2")
    open(outside2, "w").write("exit=0\nC1_R94_PASS=true\n")
    os.symlink(outside2, os.path.join(d3, "ctlA.rerun-9.out"))
    sel2 = driver_grader(d3, "ctlA")
    print("  grader picks  :", os.path.basename(sel2))
    print("  content graded:", open(sel2).read().strip().replace("\n", " | "))
    print("  -> content came from OUTSIDE the outdir:", outside2)
    os.remove(outside2)
    print()

    print("== F5c: write_receipt refuses to overwrite a symlink (O_EXCL) ==")
    d4 = outdir + ".sym3"
    shutil.rmtree(d4, ignore_errors=True)
    os.makedirs(d4)
    tgt = os.path.abspath(outdir + ".outside3")
    open(tgt, "w").write("ORIGINAL\n")
    os.symlink(tgt, os.path.join(d4, "ctlW.out"))
    chosen = m.receipt_path(d4, "ctlW")
    print("  writer chooses:", os.path.basename(chosen),
          "(lexists skips the symlinked .out)")
    try:
        m.write_receipt(chosen, "x")
        print("  write_receipt -> OK")
    except OSError as e:
        print("  write_receipt -> refused:", e.__class__.__name__, e.errno)
    print("  external file unchanged:", open(tgt).read().strip())
    os.remove(tgt)
    print()

    print("== F5d: unwritable outdir is refused by O_CREAT ==")
    d5 = outdir + ".ro"
    shutil.rmtree(d5, ignore_errors=True)
    os.makedirs(d5)
    os.chmod(d5, 0o555)
    try:
        m.write_receipt(m.receipt_path(d5, "someCtl"), "body\n")
        print("  write_receipt -> OK (UNEXPECTED)")
    except OSError as e:
        print("  write_receipt -> refused:", e.__class__.__name__, e.errno,
              os.strerror(e.errno))
    os.chmod(d5, 0o755)


if __name__ == "__main__":
    main()
