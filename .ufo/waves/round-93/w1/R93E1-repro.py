#!/usr/bin/env python3
"""R93E1 independent reproduction OUTSIDE the counter.

For each of the 12 mutants in census-mutants.json:
  - materialize pristine gate copy from fleet commit f47ad6ba8d306f8125597401cb2ce45c1297a593
    via `git archive` + `git show` (read-only on the fleet repo),
  - verify pristine selftest: exit 0 and "selftest ok",
  - apply the mutant's exact old->new edit with this script's own code
    (assert old occurs exactly once) — NOT measure-v93.py,
  - run `bash <gate> selftest` twice in the ordinary shell environment
    (no env -i), recording rc and SURVIVED arm lines,
  - derive verdict: rc==0 -> SURVIVED, else KILLED,
  - compare with the C1_ROW note verdicts in pos-real.out.

Exit 0 iff all 12 derived verdicts agree with pos-real.out note verdicts.
"""
import json, os, re, shutil, subprocess, sys, tarfile, io

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
GATE_COMMIT = "f47ad6ba8d306f8125597401cb2ce45c1297a593"
SPEC = f"{LANE}/.ufo/evidence/round-93/c1/census-mutants.json"
POSREAL = f"{LANE}/.ufo/evidence/round-93/pre-freeze/controls/pos-real.out"
BASE = "/fast/scratch/hyaku/tameshi-r93/R93E1"
G = f"{BASE}/g"
RUNS = 2

def sh(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)

def materialize(dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(f"{dst}/scripts", exist_ok=True)
    # fixtures via git archive
    arc = subprocess.run(
        ["git", "-C", FLEET, "archive", "--format=tar", GATE_COMMIT,
         "scripts/fixtures/sources-census"],
        capture_output=True, check=True)
    with tarfile.open(fileobj=io.BytesIO(arc.stdout)) as tf:
        tf.extractall(dst)
    # gate script via git show
    gate = subprocess.run(
        ["git", "-C", FLEET, "show", f"{GATE_COMMIT}:scripts/sources-census.sh"],
        capture_output=True, check=True, text=True)
    with open(f"{dst}/scripts/sources-census.sh", "w") as fh:
        fh.write(gate.stdout)
    os.chmod(f"{dst}/scripts/sources-census.sh", 0o755)
    return f"{dst}/scripts/sources-census.sh"

def run_selftest(gate):
    r = subprocess.run(["bash", gate, "selftest"], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

def survived_arms(output):
    arms = []
    for line in output.splitlines():
        if line.startswith("SURVIVED\t"):
            arms.append(line[len("SURVIVED\t"):].strip())
    return arms

def main():
    spec = json.load(open(SPEC))
    mutants = spec["mutants"]
    assert len(mutants) == 12, len(mutants)
    # expected note verdicts from pos-real.out (the committed receipt)
    note = {}
    for line in open(POSREAL):
        m = re.match(r"C1_ROW (C\d+) derived=\S+ runs=\S+ note=(\S+)", line)
        if m:
            note[m.group(1)] = m.group(2)
    assert len(note) == 12, note

    pristine = materialize(G)
    rc, out = run_selftest(pristine)
    print(f"PRISTINE rc={rc} ok={'selftest ok' in out}")
    assert rc == 0 and "selftest ok" in out, f"pristine gate failed rc={rc}\n{out[-2000:]}"

    agree = 0
    rows = []
    for m in mutants:
        mid, old, new = m["id"], m["old"], m["new"]
        gate = materialize(G)  # fresh pristine copy per mutant
        with open(gate) as fh:
            src = fh.read()
        n = src.count(old)
        assert n == 1, f"{mid}: old occurs {n} times (expected 1)"
        src = src.replace(old, new)
        with open(gate, "w") as fh:
            fh.write(src)
        os.chmod(gate, 0o755)
        rcs, arms_all, outs = [], [], []
        for _ in range(RUNS):
            rc, out = run_selftest(gate)
            rcs.append(rc)
            arms_all.append(survived_arms(out))
            outs.append(out)
        derived = "SURVIVED" if all(rc == 0 for rc in rcs) else "KILLED"
        assert len(set(rcs)) == 1, f"{mid}: unstable rc {rcs}"
        merged = sorted(set(a for arms in arms_all for a in arms))
        ok = (derived == note[mid])
        agree += ok
        rows.append((mid, rcs, merged, derived, note[mid], "YES" if ok else "NO"))
        print(f"{mid} rc={rcs} derived={derived} note={note[mid]} "
              f"agree={'YES' if ok else 'NO'} arms={merged}")
    print(f"AGREE {agree}/12")
    print("MATRIX")
    for mid, rcs, arms, derived, nv, ag in rows:
        print(f"| {mid} | {rcs[0]} | {rcs[1]} | {', '.join(arms) if arms else '(none)'} | {derived} | {nv} | {ag} |")
    sys.exit(0 if agree == 12 else 1)

if __name__ == "__main__":
    main()
