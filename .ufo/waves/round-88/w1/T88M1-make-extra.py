#!/usr/bin/env python3
"""T88M1 — counterfeit control that no committed pre-freeze control covers.

usage: T88M1-make-extra.py <base-runner> <out-runner> (badpin|...) --spec FILE

badpin: the minted py-kake-ledger-guard leg carries the real suite, the real
pre-registered spec and the real predicted table, but its PIN_KAKEGUARD is a
64-hex digest that is NOT the sha256 of the blob at REV_KAKEGUARD. This is the
control that would expose a counter which drops its own pinned-blob check (M8) —
it is expected to die on the runner's own pin check instead, which is the point
of the probe: it measures whether the counter's check is load-bearing or shadowed.

The leg construction logic is imported from the frozen control generator
(controls/make-runner.py) so the leg shape cannot drift from the pre-freeze ones.
"""
import importlib.util
import sys
from pathlib import Path

FROZEN_GEN = Path("/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-88/controls/make-runner.py")
BOGUS_PIN = "0" * 64


def load_frozen():
    spec = importlib.util.spec_from_file_location("make_runner_frozen", FROZEN_GEN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    base, out, variant = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    spec = Path(sys.argv[5]).read_text() if len(sys.argv) > 5 and sys.argv[4] == "--spec" else None
    assert spec is not None, "--spec required"
    g = load_frozen()
    t = base.read_text()
    if variant == "lie-badpin":
        # correct prereg leg (real suite, real table) + a runner that prints the frozen
        # PASS line without running anything + a pin that names no blob. Under the frozen
        # counter the pin check is the only thing that refuses this leg; under M8 the
        # counting path has nothing left between it and C1_R88_PASS=true.
        t = g.add_leg(t, "py-kake-ledger-guard", "KAKEGUARD", g.KAKE_REL, g.KAKE_PIN,
                      g.KAKE_REV, g.PY_SUITE, g.table(g.PREDICTED), spec)
        anchor = "run_regression() {\n"
        assert t.count(anchor) == 1
        t = t.replace(anchor, anchor + "  printf 'REGRESSION: PASS (cases=11 passed=11; ledger "
                      "legs exact: killed-delta<=0 flips<=0)\\n'; exit 0\n", 1)
        pin = "PIN_KAKEGUARD=%s\n" % g.KAKE_PIN
        assert t.count(pin) == 1
        t = t.replace(pin, "PIN_KAKEGUARD=%s\n" % BOGUS_PIN, 1)
    elif variant == "forged-badpin":
        import subprocess
        tmp = Path(str(out) + ".forged.tmp")
        subprocess.run(["python3", str(FROZEN_GEN), str(base), str(tmp), "forged",
                        "--spec", str(Path(sys.argv[5]))], check=True)
        t = tmp.read_text()
        tmp.unlink()
        anchor = "PIN_KAKEGUARD=%s\n" % g.KAKE_PIN
        assert t.count(anchor) == 1, "PIN_KAKEGUARD anchor"
        t = t.replace(anchor, "PIN_KAKEGUARD=%s\n" % BOGUS_PIN, 1)
        assert "exit 0\n" in t and "REGRESSION: PASS (cases=11 passed=11" in t
    elif variant == "badpin":
        t = g.add_leg(t, "py-kake-ledger-guard", "KAKEGUARD", g.KAKE_REL, g.KAKE_PIN,
                      g.KAKE_REV, g.PY_SUITE, g.table(g.PREDICTED), spec)
        anchor = "PIN_KAKEGUARD=%s\n" % g.KAKE_PIN
        assert t.count(anchor) == 1, "PIN_KAKEGUARD anchor"
        t = t.replace(anchor, "PIN_KAKEGUARD=%s\n" % BOGUS_PIN, 1)
    else:
        sys.exit("unknown variant " + variant)
    out.write_text(t)
    print("wrote %s variant=%s bytes=%d" % (out, variant, len(t.encode())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
