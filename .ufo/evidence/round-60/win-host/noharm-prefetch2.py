#!/usr/bin/env python3
"""noharm-prefetch2.py — the frozen round-18/21 monitor, host-feasible (v2).

Same goal as noharm-prefetch.py (the frozen precheck needs ~151,778 git
spawns per pair on this host; infeasible). v2 fetches bytes ONCE per
distinct path at the CANDIDATE revision and serves BOTH sides:

* cand side: cached bytes/modes are exactly what plumbing returns;
* floor side: for any path NOT in the floor->cand diff the bytes are
  identical, so the cand cache is the floor answer; for the changed paths,
  floor bytes come from five one-off `git show FLOOR:path` reads.

Every verdict is computed by the frozen module's own functions
(entry_failure, entry_credit_reason, input_reason, trace_reason, coldread);
only the git accessors are backed by the cache. Receipt records per-section
credit at floor and cand plus the lost/gained sets.
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


def git_out(args):
    r = subprocess.run(args, capture_output=True)
    return r.returncode, r.stdout


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    rc, diff_b = git_out(["git", "-C", str(ROOT), "diff", "--name-only",
                          FLOOR, CAND])
    diff = diff_b.decode("utf-8", "replace")
    changed = {x.strip() for x in diff.splitlines() if x.strip()}

    lraw_f = git_out(["git", "-C", str(ROOT), "show",
                      "%s:%s" % (FLOOR, LEDGER)])[1]
    lraw_c = git_out(["git", "-C", str(ROOT), "show",
                      "%s:%s" % (CAND, LEDGER)])[1]
    entries_f = json.loads(lraw_f.decode("utf-8", "surrogateescape"))["entries"]
    entries_c = json.loads(lraw_c.decode("utf-8", "surrogateescape"))["entries"]

    paths = {"SKILL.md"}
    for entries in (entries_f, entries_c):
        for e in entries:
            if isinstance(e, dict):
                paths |= set(e.get("inputs") or {})
                paths |= set(e.get("traces") or [])
    print("distinct paths: %d (changed: %d)" % (len(paths), len(changed)),
          flush=True)

    blob_cache = {}   # path -> bytes at CAND (None when absent)
    mode_cache = {}   # path -> mode at CAND (None when absent)
    t0 = time.time()
    floor_hashes = {}
    for i, path in enumerate(sorted(paths)):
        rc, out = git_out(["git", "-C", str(ROOT), "cat-file", "blob",
                           "%s:%s" % (CAND, path)])
        blob_cache[path] = out if rc == 0 else None
        rc2, out2 = git_out(["git", "-C", str(ROOT), "ls-tree", "-z", CAND,
                             "--", path])
        chunks = [c for c in out2.split(b"\x00") if c]
        if rc2 == 0 and len(chunks) == 1:
            mode_cache[path] = chunks[0].split(b"\t", 1)[0].split()[0].decode(
                "ascii", "replace")
        else:
            mode_cache[path] = None
        if path in changed:
            rcf, outf = git_out(["git", "-C", str(ROOT), "cat-file", "blob",
                                 "%s:%s" % (FLOOR, path)])
            floor_hashes[path] = outf if rcf == 0 else None
        if (i + 1) % 500 == 0:
            print("prefetch %d/%d (%.0fs)"
                  % (i + 1, len(paths), time.time() - t0), flush=True)
    print("prefetch done (%.0fs)" % (time.time() - t0), flush=True)

    impl = ROOT / ".ufo/evidence/round-18/measure.py"
    spec = importlib.util.spec_from_file_location("tameshi_r18_measure", impl)
    module = importlib.util.module_from_spec(spec)
    sys.modules["tameshi_r18_measure"] = module
    spec.loader.exec_module(module)

    real_blob = module.cat_file_blob
    real_ls = module.ls_tree_mode
    real_blobfn = module.blob

    def cached_blob(repo, rev, path):
        if rev == CAND:
            return blob_cache.get(path, real_blob(repo, rev, path))
        if path in changed:
            return floor_hashes.get(path, real_blob(repo, rev, path))
        return blob_cache.get(path, real_blob(repo, rev, path))

    def cached_ls(repo, rev, path):
        if path in changed and rev == FLOOR:
            # the five changed files are regular blobs at both revs; verify
            # once so the cached answer is grounded
            if path not in mode_cache or mode_cache[path] is None:
                return real_ls(repo, rev, path)
            return mode_cache[path]
        return mode_cache.get(path, real_ls(repo, rev, path))

    def cached_blobfn(repo, rev, path):
        return cached_blob(repo, rev, path)

    module.cat_file_blob = cached_blob
    module.ls_tree_mode = cached_ls
    module.blob = cached_blobfn

    skill_c = blob_cache["SKILL.md"]
    results = {}
    for rev, entries, skill, lraw in (
            (FLOOR, entries_f, None, lraw_f),
            (CAND, entries_c, skill_c, lraw_c)):
        if rev == FLOOR:
            skill = git_out(["git", "-C", str(ROOT), "show",
                             "%s:SKILL.md" % FLOOR])[1]
        t0 = time.time()
        out = module.coldread(str(ROOT), rev, skill, lraw, strict=True)
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
        "schema": "tameshi-noharm-prefetch-v2",
        "lane": str(ROOT),
        "floor": FLOOR,
        "cand": CAND,
        "method": "frozen module functions with a prefetch cache; cand bytes "
                  "fetched once per distinct path and served to both revs "
                  "(identical bytes off the diff; changed paths carry their "
                  "own floor bytes)",
        "changed_paths": sorted(changed),
        "floor_credited": results[FLOOR]["sections_credited"],
        "cand_credited": results[CAND]["sections_credited"],
        "lost": sorted(fl - cd),
        "gained": sorted(cd - fl),
        "sections_floor": results[FLOOR]["sections"],
        "sections_cand": results[CAND]["sections"],
    }
    dest = Path(__file__).with_name("noharm-prefetch2.json")
    dest.write_text(json.dumps(receipt, indent=1, ensure_ascii=True) + "\n",
                    encoding="utf-8")
    print("NOHARM_PREFETCH2 floor=%d cand=%d lost=%d gained=%d -> %s"
          % (results[FLOOR]["sections_credited"],
             results[CAND]["sections_credited"],
             len(receipt["lost"]), len(receipt["gained"]), dest.name),
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
