#!/usr/bin/env python3
"""Independent reproduction of the 12 fleet-gate mutants, OUTSIDE measure-v92.py.

Materializes a pristine copy of scripts/sources-census.sh (+ fixtures) from the
fleet repo at f47ad6ba8d306f8125597401cb2ce45c1297a593, asserts `selftest ok`
with rc 0, then for each mutant in census-mutants.json asserts the `old` string
occurs exactly once, applies old->new, runs selftest twice in the ordinary shell
environment (no env -i), records (rc1, rc2) and the differing selftest arm lines,
derives verdict rc==0 ? SURVIVED : KILLED, and compares against the C1_ROW lines
in pos-real.out.

Usage:
  python3 T92E1-repro.py --scratch /fast/scratch/hyaku/tameshi-r92/T92E1
"""
import argparse
import json
import pathlib
import shutil
import subprocess
import sys

FLEET = "/home/vgpnk/Projects/shokunin"
GATE_COMMIT = "f47ad6ba8d306f8125597401cb2ce45c1297a593"
SPEC = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-92/c1/census-mutants.json"
POS_REAL = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-92/pre-freeze/controls/pos-real.out"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    args = ap.parse_args()
    S = pathlib.Path(args.scratch)
    G = S / "g"
    if G.exists():
        shutil.rmtree(G)
    (G / "scripts").mkdir(parents=True)
    subprocess.run(
        ["git", "-C", FLEET, "archive", "--format=tar", GATE_COMMIT, "scripts/fixtures/sources-census"],
        stdout=subprocess.PIPE, check=True,
    )
    with subprocess.Popen(
        ["git", "-C", FLEET, "archive", "--format=tar", GATE_COMMIT, "scripts/fixtures/sources-census"],
        stdout=subprocess.PIPE,
    ) as git, subprocess.Popen(["tar", "-x", "-C", str(G)], stdin=git.stdout) as tar:
        git.stdout.close()
        tar.wait()
        assert git.wait() == 0
    with open(G / "scripts/sources-census.sh", "wb") as f:
        subprocess.run(
            ["git", "-C", FLEET, "show", f"{GATE_COMMIT}:scripts/sources-census.sh"],
            stdout=f, check=True,
        )
    (G / "scripts/sources-census.sh").chmod(0o755)

    def selftest(path):
        p = subprocess.run(["bash", str(path), "selftest"], capture_output=True, text=True)
        return p.returncode, p.stdout.splitlines()

    rc, pristine_lines = selftest(G / "scripts/sources-census.sh")
    assert rc == 0 and "selftest ok" in pristine_lines, (rc, pristine_lines[-3:])
    print(f"PRISTINE rc=0 selftest ok ({len(pristine_lines)} lines)")

    spec = json.load(open(SPEC))
    counter = {}
    for line in open(POS_REAL):
        if line.startswith("C1_ROW "):
            cid = line.split()[1]
            counter[cid] = line.strip()
    print(f"Loaded {len(counter)} counter C1_ROW lines from pos-real.out")

    for m in spec["mutants"]:
        derived, rcs, diff = [], [], None
        for run in (1, 2):
            D = S / f"m-{m['id']}-{run}"
            if D.exists():
                shutil.rmtree(D)
            shutil.copytree(G, D)
            f = D / "scripts/sources-census.sh"
            text = f.read_text()
            n = text.count(m["old"])
            assert n == 1, (m["id"], n)
            f.write_text(text.replace(m["old"], m["new"], 1))
            rc, lines = selftest(f)
            rcs.append(rc)
            derived.append("SURVIVED" if rc == 0 else "KILLED")
            if run == 1:
                missing = [l for l in pristine_lines if l not in set(lines)]
                newlines = [l for l in lines if l not in set(pristine_lines)]
                diff = (missing, newlines)
            shutil.rmtree(D)
        verdict = derived[0]
        agree = "agree" if derived[0] == derived[1] else "UNSTABLE"
        crow = counter.get(m["id"], "")
        agrees_counter = derived[0] in crow and f"note={derived[0]}" in crow
        print(f"{m['id']} derived={verdict} rc={rcs[0]},{rcs[1]} runs={derived[0]},{derived[1]} counter_agree={agrees_counter}")
        print(f"  arm={m['arm']}")
        print(f"  missing={diff[0]}")
        print(f"  new={diff[1]}")
        assert derived[0] == derived[1], (m["id"], derived)
        assert agrees_counter, (m["id"], crow)
    print("ALL 12 MATCH pos-real.out")


if __name__ == "__main__":
    sys.exit(main())
