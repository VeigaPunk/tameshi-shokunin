#!/usr/bin/env python3
"""Round-99 amendment discrimination (A1-A9): run every selftest case the records tools ADD
over the frozen tools through the FROZEN tool bytes, and report whether the frozen tool grades
it the way the new arm requires. `discriminates` = the frozen tool fails the arm (the repair is
load-bearing); `armour` = the frozen tool already passes it (the arm pins a boundary or a live
code path a mutant could remove).

Usage: python3 -I discriminate.py <frozen tally> <records tally> <frozen v2> <records v2>
"""
import importlib.util
import shutil
import sys
import tempfile


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ft, nt, fv, nv = (load(p, "m%d" % i) for i, p in enumerate(sys.argv[1:5]))
    old_names = {c[0] for c in ft.SELFTEST_CASES}
    base = tempfile.mkdtemp(prefix="discrim-")
    nd = na = 0
    try:
        for name, files, records, roots, want, wrc in nt.SELFTEST_CASES:
            if name in old_names:
                continue
            d, rev = nt.build_fixture(base, files)
            lines, rc = ft.reconcile(ft.Tree(d, rev), records, roots)
            got = nt.summary_fields(lines[-1])
            ok = rc == wrc and all(got.get(k) == v for k, v in want.items())
            nd += not ok
            na += ok
            print("DISCRIM tally %s %s frozen_rc=%d frozen=%s" % (name, "armour" if ok else "discriminates", rc, lines[-1]))
        try:
            d3, rev3 = nt.build_fixture(base, {"p/round-3.md": "`X_SELFTEST: 9/9 pass` (`dig.out`)\n",
                                               ".ufo/evidence/round-3/dig.out":
                                               b"X_SELFTEST: 9/9 pass\nX_SELFTEST: 8\xff/8 pass\n"})
            lines, rc = ft.reconcile(ft.Tree(d3, rev3), ["p/round-3.md"], [])
            print("DISCRIM tally setup-receipt-not-utf8 discriminates frozen_rc=%d frozen=%s" % (rc, lines[-1]))
            nd += 1
        except ft.Setup as exc:
            print("DISCRIM tally setup-receipt-not-utf8 armour frozen_setup=%s" % exc)
            na += 1
    finally:
        shutil.rmtree(base, ignore_errors=True)
    print("DISCRIM_TALLY discriminates=%d armour=%d" % (nd, na))
    old_names = {c[0] for c in fv.SELFTEST_CASES}
    vd = va = 0
    for name, text, want in nv.SELFTEST_CASES:
        if name in old_names:
            continue
        sites, _, _ = fv.audit_text(text)
        got = sites[0][2] if sites and len(sites) == 1 else "site-count(%d)" % len(sites or [])
        ok = got == want
        vd += not ok
        va += ok
        print("DISCRIM v2 %s %s frozen=%s want=%s" % (name, "armour" if ok else "discriminates", got, want))
    print("DISCRIM_V2 discriminates=%d armour=%d" % (vd, va))
    return 0


if __name__ == "__main__":
    sys.exit(main())
