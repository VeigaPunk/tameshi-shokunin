#!/usr/bin/env python3
"""T92E3 stable-line diff: compare battery receipts vs committed on stable lines only."""
import sys, os
STABLE = ("C1_ROW", "C1_CONJUNCTS", "C1_R92_PASS", "C1_SETUP")
IGN = ("control=", "clone_rev=", "parent=", "mutant=", "counter_sha=", "exit=", "edit=", "rev=")
def stable(path):
    out = []
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if any(line.startswith(k) and not line.startswith(IGN) for k in STABLE):
            out.append(line)
        # also: full-line header ignores; only above prefixes kept
    return out
def main(mine_dir, committed_dir):
    diffs = {}
    names = sorted(f for f in os.listdir(committed_dir) if f.endswith(".out"))
    for n in names:
        c = os.path.join(committed_dir, n)
        m = os.path.join(mine_dir, n)
        if not os.path.exists(m):
            diffs[n] = "MISSING in mine"
            continue
        cs, ms = stable(c), stable(m)
        if cs != ms:
            diffs[n] = []
            import difflib
            for d in difflib.unified_diff(cs, ms, fromfile=f"committed/{n}", tofile=f"mine/{n}", lineterm=""):
                diffs[n].append(d)
    if not diffs:
        print("STABLE-DIFF: NONE — all receipts identical on stable lines")
    else:
        for n, v in diffs.items():
            print(f"=== {n}: {v if isinstance(v,str) else ''}")
            if isinstance(v, list):
                for line in v:
                    print(line)
    return 0
if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
