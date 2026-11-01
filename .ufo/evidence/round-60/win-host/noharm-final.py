#!/usr/bin/env python3
"""noharm-final.py — exact lost-set computation, bounded.

Runs the frozen module's own decision functions (entry_failure,
entry_credit_reason, input_reason, trace_reason via entry_reason, and the
coldread coverage rule) over a REDUCED ledger that keeps only the entries
matching the 18 sections that noharm-cand.json found uncredited at the
candidate revision. Per-section coverage is independent (a section's credit
depends only on its own matching entries), so reducing the ledger cannot
change those sections' verdicts; the other sections read 'no-ledger' and
are ignored here.

Accessors are backed by a prefetch cache built only from the reduced
entries' paths. Floor side: bytes off the diff equal cand bytes; the five
changed paths carry their own floor bytes.
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
CAND_UNCREDITED_HEADINGS = None  # loaded from noharm-cand.json


def git_out(args):
    r = subprocess.run(args, capture_output=True)
    return r.returncode, r.stdout


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    prev = json.loads((Path(__file__).with_name("noharm-cand.json")
                       ).read_text(encoding="utf-8"))
    targets = [s["heading"] for s in prev["not_credited"]]
    print("target sections:", len(targets), flush=True)

    impl = ROOT / ".ufo/evidence/round-18/measure.py"
    spec = importlib.util.spec_from_file_location("tameshi_r18_measure", impl)
    module = importlib.util.module_from_spec(spec)
    sys.modules["tameshi_r18_measure"] = module
    spec.loader.exec_module(module)

    _, skill_c = git_out(["git", "-C", str(ROOT), "show",
                          "%s:SKILL.md" % CAND])
    sections = module.sectionize(skill_c)
    sha_by_heading = {s["heading"]: s["sha256"] for s in sections}
    target_shas = {sha_by_heading[h] for h in targets}

    _, lraw = git_out(["git", "-C", str(ROOT), "show",
                       "%s:%s" % (FLOOR, LEDGER)])
    all_entries = json.loads(lraw.decode("utf-8", "surrogateescape"))["entries"]
    reduced = [e for e in all_entries
               if isinstance(e, dict) and e.get("sha256") in target_shas]
    print("reduced entries:", len(reduced), flush=True)

    paths = {"SKILL.md"}
    for e in reduced:
        paths |= set(e.get("inputs") or {})
        paths |= set(e.get("traces") or [])
    diff = git_out(["git", "-C", str(ROOT), "diff", "--name-only", FLOOR,
                    CAND])[1].decode("utf-8", "replace")
    changed = {x.strip() for x in diff.splitlines() if x.strip()}

    blob_cache, mode_cache, floor_hashes = {}, {}, {}
    t0 = time.time()
    for i, path in enumerate(sorted(paths)):
        rc, out = git_out(["git", "-C", str(ROOT), "cat-file", "blob",
                           "%s:%s" % (CAND, path)])
        blob_cache[path] = out if rc == 0 else None
        rc2, out2 = git_out(["git", "-C", str(ROOT), "ls-tree", "-z", CAND,
                             "--", path])
        chunks = [c for c in out2.split(b"\x00") if c]
        mode_cache[path] = (chunks[0].split(b"\t", 1)[0].split()[0].decode(
            "ascii", "replace") if rc2 == 0 and len(chunks) == 1 else None)
        if path in changed:
            rcf, outf = git_out(["git", "-C", str(ROOT), "cat-file", "blob",
                                 "%s:%s" % (FLOOR, path)])
            floor_hashes[path] = outf if rcf == 0 else None
        if (i + 1) % 200 == 0:
            print("prefetch %d/%d (%.0fs)"
                  % (i + 1, len(paths), time.time() - t0), flush=True)
    print("prefetch done (%.0fs)" % (time.time() - t0), flush=True)

    real_blob = module.cat_file_blob
    real_ls = module.ls_tree_mode

    def cached_blob(repo, rev, path):
        if path in changed:
            if rev == CAND:
                return blob_cache.get(path, real_blob(repo, rev, path))
            return floor_hashes.get(path, real_blob(repo, rev, path))
        return blob_cache.get(path, real_blob(repo, rev, path))

    def cached_ls(repo, rev, path):
        return mode_cache.get(path, real_ls(repo, rev, path))

    module.cat_file_blob = cached_blob
    module.ls_tree_mode = cached_ls

    out_by_rev = {}
    for rev in (FLOOR, CAND):
        _, skill = git_out(["git", "-C", str(ROOT), "show",
                            "%s:SKILL.md" % rev])
        _, lraw_rev = git_out(["git", "-C", str(ROOT), "show",
                               "%s:%s" % (rev, LEDGER)])
        ledger = {"entries": reduced}
        # run the frozen coverage rule over the full section list, reduced
        # ledger; read only the target rows
        sections_full = module.sectionize(skill)
        out = module.coldread(str(ROOT), rev, skill,
                              json.dumps(ledger).encode("utf-8"),
                              strict=True)
        rows = {s["heading"]: s for s in out["sections"]}
        out_by_rev[rev] = {h: rows[h]["credited"] for h in targets
                           if h in rows}
        print("rev %s done (%.0fs)"
              % (rev[:8], time.time() - t0), flush=True)

    lost = sorted(h for h in targets
                  if out_by_rev[FLOOR].get(h) and not out_by_rev[CAND].get(h))
    already = sorted(h for h in targets
                     if not out_by_rev[FLOOR].get(h))
    receipt = {
        "schema": "tameshi-noharm-final-v1",
        "lane": str(ROOT),
        "floor": FLOOR,
        "cand": CAND,
        "method": "frozen module decision functions over a reduced ledger "
                  "(entries matching the 18 cand-uncredited sections only); "
                  "accessors prefetch-cached; changed paths carry floor bytes",
        "changed_paths": sorted(changed),
        "floor_credited_among_targets": sum(
            1 for h in targets if out_by_rev[FLOOR].get(h)),
        "lost": lost,
        "already_uncredited_at_floor": already,
        "detail": out_by_rev,
    }
    dest = Path(__file__).with_name("noharm-final.json")
    dest.write_text(json.dumps(receipt, indent=1, ensure_ascii=True) + "\n",
                    encoding="utf-8")
    print("NOHARM_FINAL lost=%d already=%d -> %s"
          % (len(lost), len(already), dest.name), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
