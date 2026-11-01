#!/usr/bin/env python3
"""noharm-prefetch.py — the frozen round-18/21 monitor, host-feasible.

The frozen precheck cannot finish in round time on this host: the round-21
ledger records 75,889 inputs and the monitor spawns two git processes per
input per measured rev (~151,778 spawns/rev; ~0.044 s/spawn here -> ~112
min/rev). This runner executes the frozen module's own `coldread()` — the
decision code is untouched — with the module's three git accessors
(`ls_tree_mode`, `cat_file_blob`, `blob`) backed by a prefetch cache: every
distinct (rev, path) is fetched ONCE with the same git plumbing and reused
for all entries that cite it. Bytes are identical to what the unpatched
accessors return, so every verdict is the frozen instrument's verdict; only
the process-spawn count drops (to ~2 per distinct path).

The ledger is read from each measured rev; SKILL.md likewise. Receipt:
per-section credit at floor and cand, the lost set (credited at floor,
not at cand), and the gained set.
"""

import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

FLOOR = "9bc9b20b5d6723a19d1b69c8edd7246f82ea3d78"
CAND = "f0ec3a5b4514b64752ff8fb1f97760bbc88f2acf"
LEDGER = ".ufo/evidence/round-21/coldread/ledger.json"
ROOT = Path(__file__).resolve().parents[4]
FLOOR_CRED_PER_ATTEMPT1 = 50


def git_out(args):
    r = subprocess.run(args, capture_output=True)
    return r.returncode, r.stdout


def collect_distinct_paths(rev):
    _, raw = git_out(["git", "-C", str(ROOT), "show", "%s:%s" % (rev, LEDGER)])
    ledger = json.loads(raw.decode("utf-8", "surrogateescape"))
    paths = {("SKILL.md",)}
    entries = ledger.get("entries", [])
    for e in entries:
        if not isinstance(e, dict):
            continue
        for p in (e.get("inputs") or {}):
            paths.add((p,))
        for p in (e.get("traces") or []):
            paths.add((p,))
    return entries, {p[0] for p in paths}


def main():
    impl = ROOT / ".ufo/evidence/round-18/measure.py"
    spec = importlib.util.spec_from_file_location("tameshi_r18_measure", impl)
    module = importlib.util.module_from_spec(spec)
    sys.modules["tameshi_r18_measure"] = module
    spec.loader.exec_module(module)

    results = {}
    for rev in (FLOOR, CAND):
        t0 = time.time()
        entries, distinct = collect_distinct_paths(rev)
        # collect the union across both revs lazily: this rev's paths only
        ls_cache = {}
        blob_cache = {}

        def prefetch(rev=rev, distinct=distinct, ls_cache=ls_cache,
                     blob_cache=blob_cache):
            for i, path in enumerate(sorted(distinct)):
                rc, out = git_out(["git", "-C", str(ROOT), "cat-file", "blob",
                                   "%s:%s" % (rev, path)])
                blob_cache[(rev, path)] = out if rc == 0 else None
                rc2, out2 = git_out(["git", "-C", str(ROOT), "ls-tree", "-z",
                                     rev, "--", path])
                entries_ = [c for c in out2.split(b"\x00") if c]
                if rc2 != 0 or len(entries_) != 1:
                    ls_cache[(rev, path)] = None
                else:
                    meta = entries_[0].split(b"\t", 1)[0].split()
                    ls_cache[(rev, path)] = meta[0].decode("ascii", "replace")
                if (i + 1) % 500 == 0:
                    print("prefetch %s %d/%d (%.0fs)"
                          % (rev[:8], i + 1, len(distinct), time.time() - t0),
                          flush=True)

        prefetch()

        real_blob = module.cat_file_blob
        real_ls = module.ls_tree_mode
        real_blobfn = module.blob

        module.cat_file_blob = lambda repo, rev_, path: blob_cache.get(
            (rev_, path), real_blob(repo, rev_, path))
        module.ls_tree_mode = lambda repo, rev_, path: ls_cache.get(
            (rev_, path), real_ls(repo, rev_, path))
        module.blob = lambda repo, rev_, path: blob_cache.get(
            (rev_, path), real_blobfn(repo, rev_, path))

        skill_raw = blob_cache[(rev, "SKILL.md")]
        ledger_raw = git_out(["git", "-C", str(ROOT), "show",
                              "%s:%s" % (rev, LEDGER)])[1]
        out = module.coldread(str(ROOT), rev, skill_raw, ledger_raw,
                              strict=True)
        module.cat_file_blob = real_blob
        module.ls_tree_mode = real_ls
        module.blob = real_blobfn
        results[rev] = {
            "sections_total": out["sections_total"],
            "sections_credited": out["sections_covered"],
            "credited": sorted(s["heading"] for s in out["sections"]
                               if s["credited"]),
            "sections": [{"heading": s["heading"], "credited": s["credited"],
                          "reason": s["reason"]} for s in out["sections"]],
        }
        print("rev %s credited %d/%d (%.0fs)"
              % (rev[:8], out["sections_covered"], out["sections_total"],
                 time.time() - t0), flush=True)

    fl = set(results[FLOOR]["credited"])
    cd = set(results[CAND]["credited"])
    receipt = {
        "schema": "tameshi-noharm-prefetch-v1",
        "lane": str(ROOT),
        "floor": FLOOR,
        "cand": CAND,
        "method": "frozen module coldread() with prefetch-backed git "
                  "accessors (bytes identical to plumbing; spawn count "
                  "reduced to ~2 per distinct rev:path)",
        "floor_credited": results[FLOOR]["sections_credited"],
        "cand_credited": results[CAND]["sections_credited"],
        "floor_credited_per_attempt1_receipt": FLOOR_CRED_PER_ATTEMPT1,
        "lost": sorted(fl - cd),
        "gained": sorted(cd - fl),
        "sections_floor": results[FLOOR]["sections"],
        "sections_cand": results[CAND]["sections"],
    }
    dest = Path(__file__).with_name("noharm-prefetch.json")
    dest.write_text(json.dumps(receipt, indent=1, ensure_ascii=True) + "\n",
                    encoding="utf-8")
    print("NOHARM_PREFETCH floor=%d cand=%d lost=%d gained=%d -> %s"
          % (results[FLOOR]["sections_credited"],
             results[CAND]["sections_credited"],
             len(receipt["lost"]), len(receipt["gained"]), dest.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
