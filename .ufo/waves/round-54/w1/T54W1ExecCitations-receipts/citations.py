#!/usr/bin/env python3
"""T54W1ExecCitations — every in-section citation vs the C0 tree.

For each of the 23 headings the C1 counter lost at C0, extract (a) the
lane-relative paths the section names and (b) its file:line references, then
check each against the git objects of the C0 commit only:

  (a) path  -> `git cat-file -t REV:<path>` must succeed (blob or tree);
  (b) file:line -> the highest cited line must be <= the blob's line count.

Bare `:N[-N]` clusters inherit the file their sentence names; where a section
declares page-relative anchors ("Anchors `:...` are this page", or an
unqualified `:N` beside "this page"), they resolve to SKILL.md at REV.

Exit 0 when every citation resolves, 1 when any does not.

Usage: python3 citations.py LANE REV
"""
import json
import os
import re
import subprocess
import sys

HEADINGS = [
    "## Standing rules",
    "## Mutation-sweep recipe — numbered steps; bounded cold-read evidence",
    "### The boundaries — what a service run is not",
    "## The leg ledger — replay, receipt, and how it is read (round 7, measured)",
    "### Using the ledger",
    "### The tick and the pin read",
    "### Triggers T1–T3 and the re-pin rule",
    "### The service's limits — what tameshi refuses to mutation-test",
    "## The operator's runbook and the six-leg regression (round 10, measured)",
    "### The operator's runbook — `corpus/knowledge/operator-runbook.md`",
    "## Repeated controls and gate registry — round 12",
    "### Gate/probe registry",
    "## Pin disposition and provenance correction — round 13",
    "### Round-13 gate/probe registry",
    "## Effective expectation reconciliation — round 14",
    "### Round-14 historical registry — superseded by round 15",
    "## Context gate classification and explicit exit classes — round 15",
    "### Round-15 gate/probe registry",
    "## Live-tree re-pin and entry-command monitor — round 17",
    "### Round-17 gate/probe registry — re-pin and monitor",
    "### Round-18 gate/probe registry — routed-defect closure",
    "### Round-21 gate/probe registry — finite environment differential",
    "### Round-26 gate/probe registry — report interop",
]

# basename -> lane path, where the lane holds the file at more than one path
# (the round-53 assimilation snapshot copies are never the citation's target).
RESOLVE = {
    "SKILL.md": "SKILL.md",
    "PROVINCE.md": "PROVINCE.md",
    "SOURCES.md": "corpus/SOURCES.md",
    "RerunSweep.md": ".ufo/waves/round-16/w2/RerunSweep.md",
    "Read25.md": ".ufo/waves/round-27/w1/Read25.md",
    "SentinelKillCode.md": ".ufo/waves/round-18/w2/SentinelKillCode.md",
    "round-8.plan.md": "plans/round-8.plan.md",
    "round-1-verifier-spotcheck.md": "corpus/lessons/round-1-verifier-spotcheck.md",
    "round-12-verifier-spotcheck.md": "corpus/lessons/round-12-verifier-spotcheck.md",
    "round-13-verifier-spotcheck.md": "corpus/lessons/round-13-verifier-spotcheck.md",
    "round-14-verifier-spotcheck.md": "corpus/lessons/round-14-verifier-spotcheck.md",
    "round-16-verifier-spotcheck.md": "corpus/lessons/round-16-verifier-spotcheck.md",
    "round-15.md": "corpus/lessons/round-15.md",
    "round-21.md": "corpus/lessons/round-21.md",
    "round-24.md": "corpus/lessons/round-24.md",
    "capture-context.py": ".ufo/evidence/round-14/capture-context.py",
    "defect-probes.py": ".ufo/evidence/round-18/defect-probes.py",
    "c1-survivors.py": ".ufo/evidence/round-21/c1-survivors.py",
    "c2-count.py": ".ufo/evidence/round-21/c2-count.py",
    "pin-manifest.json": ".ufo/evidence/round-13/pin-manifest.json",
    "witness-metadata.json": ".ufo/evidence/round-13/witness-metadata.json",
    "context-receipt.json": ".ufo/evidence/round-14/context-receipt.json",
    "context-missing-env.json": ".ufo/evidence/round-14/context-missing-env.json",
    "verification-3.json": ".ufo/evidence/round-15/verification-3.json",
    "replay.py": ".ufo/evidence/round-23/replay.py",
    "requirements.json": ".ufo/evidence/round-23/requirements.json",
    "registry-baseline.json": ".ufo/evidence/round-23/registry-baseline.json",
    "producer-oracle-repair.json": ".ufo/evidence/round-13/producer-oracle-repair.json",
    "historical-receipts.json": ".ufo/evidence/round-20/final/historical-receipts.json",
    "receipt-window-selftest.json": ".ufo/evidence/round-20/final/receipt-window-selftest.json",
    "public-cli-cases.json": ".ufo/evidence/round-20/public-cli-cases.json",
    "declaration.json": ".ufo/evidence/round-12/BashWitness/declaration.json",
    "routemix-spec1.json": ".ufo/waves/round-21/routemix-spec1.json",
    "wrong-count-bundle.json": ".ufo/evidence/round-22/wrong-count-bundle.json",
    "wrong-count-expected.json": ".ufo/evidence/round-22/wrong-count-expected.json",
    "accounting-extra-cases.json": ".ufo/evidence/round-22/accounting-extra-cases.json",
}

# A bare `:N` cluster and the file its sentence names.  Value = (path, why).
BARE = {
    1: [(":155-166", "corpus/knowledge/mutation-case-kimi-census.md"),
        (":118-122", "corpus/knowledge/mutation-case-kagi-census.md"),
        (":252-254", "corpus/knowledge/mutation-case-kagi-census.md")],
    2: [(":240-260", "corpus/knowledge/mutation-case-mado-verify.md")],
    3: [(":511-522", "tools/mutate-and-run.sh@9f1d3c3"),
        (":597-620", "tools/mutate-and-run.sh@4b7c682")],
    4: [(":1302-1306", "tools/mutate-and-run.sh"),
        (":1247-1317", "tools/mutate-and-run.sh"),
        (":1459-1517", "tools/mutate-and-run.sh"),
        (":603-629", "tools/mutate-and-run.sh"),
        (":671-849", "tools/mutate-and-run.sh"),
        (":83-108", "tools/mutate-and-run.sh"),
        (":1459-1508", "tools/mutate-and-run.sh")],
    5: [(":14", "scripts/shokunin-watchdog.sh@17c1fad")],
    6: [(":318", "corpus/knowledge/fleet-kill-rate-ledger.md")],
    7: [(":1010-1154", "SKILL.md"), (":813-817", "SKILL.md"),
        (":840-844", "SKILL.md"), (":823-825", "SKILL.md"),
        (":879-881", "SKILL.md")],
    9: [(":1250-1254", "SKILL.md")],
    16: [(":2-31", ".ufo/evidence/round-14/capture-context.py"),
         (":553-580", ".ufo/evidence/round-14/capture-context.py"),
         (":605-643", ".ufo/evidence/round-14/capture-context.py")],
    18: [(":2891-2896", "tools/evidence-disposition.py"),
         (":2256", "tools/evidence-disposition.py")],
}

LANE_PREFIX = ("corpus/", "tools/", "plans/", ".ufo/")
ROOT_FILES = ("SKILL.md", "PROVINCE.md", "SHONEN.md")
# directory names and write-scope names, not citations of a committed file
NOT_A_LANE_PATH = {"corpus/knowledge", "tools/vendor", "refs/heads", "dev/null",
                   "tools/__pycache__",
                   # sibling-lane path: the mado gate, named inside a mado edit
                   "tools/mado-verify.sh"}
# The lane's corpus always wins over the round-53 assimilation snapshot copies.
PREFER = ("corpus/knowledge/", "corpus/lessons/", "tools/", "plans/")
# Fleet-repo files the sections cite by bare name (never lane paths).
FLEET_FILE = {"shokunin-watchdog.sh": "scripts/shokunin-watchdog.sh",
              "jj-lane.sh": "scripts/hyaku/jj-lane.sh"}
FLEET_FILE_REV = {"shokunin-watchdog.sh": "17c1fad"}
# Paths the section places outside the lane; checked in the fleet repo instead.
FLEET_PATHS = {
    "scripts/shokunin-watchdog.sh@17c1fad": ("scripts/shokunin-watchdog.sh", "17c1fad"),
    "../scripts/hyaku/jj-lane.sh": ("scripts/hyaku/jj-lane.sh", "HEAD"),
    "../PROTOCOL.md": ("PROTOCOL.md", "HEAD"),
    "shokunin.conf": ("shokunin.conf", "HEAD"),
}


def git(lane, *args, binary=False):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1")
    p = subprocess.run(["git", "-C", lane, *args], capture_output=True, env=env)
    if p.returncode != 0:
        return None
    return p.stdout if binary else p.stdout.decode("utf-8", "replace")


def sectionize(lane, rev):
    """Same sectionizer the round-54 counter uses (round-18 measure.py at REV)."""
    src = git(lane, "show", rev + ":.ufo/evidence/round-18/measure.py")
    import importlib.util
    import tempfile
    work = tempfile.mkdtemp(prefix="r54-cite-", dir=os.environ.get("TMPDIR"))
    path = os.path.join(work, "measure.py")
    with open(path, "w") as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location("r54_cite_r18", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    skill = git(lane, "show", rev + ":SKILL.md")
    return {s["heading"]: (s["start"], s["end"]) for s in mod.sectionize(skill.encode())}, skill


def lineno_cache(lane, rev, path):
    key = (rev, path)
    if key not in lineno_cache.memo:
        out = git(lane, "show", "%s:%s" % (rev, path), binary=True)
        lineno_cache.memo[key] = None if out is None else len(out.decode("utf-8", "replace").split("\n")) - 1
    return lineno_cache.memo[key]


lineno_cache.memo = {}


def ref_target(target):
    """Split `path[:lines]`, `path@rev[:lines]` into (rev_or_None, path, lines)."""
    m = re.match(r"^(.*?)@([0-9a-f]+):(\d+(?:-\d+)?)$", target)
    if m:
        return m.group(2), m.group(1), m.group(3)
    m = re.match(r"^(.*?)@([0-9a-f]+)$", target)
    if m:
        return m.group(2), m.group(1), None
    m = re.match(r"^(.*?):(\d+(?:-\d+)?)$", target)
    if m:
        return None, m.group(1), m.group(2)
    return None, target, None


def main():
    lane, rev = sys.argv[1], sys.argv[2]
    spans, skill = sectionize(lane, rev)
    lines = skill.split("\n")
    total_checked = total_unresolved = 0
    out = []
    for idx, heading in enumerate(HEADINGS):
        start, end = spans[heading]
        body = "\n".join(lines[start - 1:end])
        paths, linespecs, unresolved = set(), [], []

        # (a) lane-relative paths
        fleet_seen = set()
        rev_paths = set()
        for tok in FLEET_PATHS:
            if tok in body:
                fleet_seen.add(tok)
        for m in re.finditer(r"[A-Za-z0-9_.][A-Za-z0-9_./-]*/[A-Za-z0-9_.@-]+", body):
            tok = m.group(0)
            if tok in fleet_seen or tok in FLEET_PATHS:
                continue
            if not tok.startswith(LANE_PREFIX) and tok not in ROOT_FILES:
                continue
            if tok in NOT_A_LANE_PATH:
                continue
            tok = tok.rstrip(".,;")
            if "@" in tok:
                rev_paths.add(tok)      # path@rev: existence at that revision
                continue
            paths.add(tok)
        for p in sorted(fleet_seen):
            fp, frev = FLEET_PATHS[p]
            root = os.path.dirname(lane)
            if git(root, "cat-file", "-e", "%s:%s" % (frev, fp)) is None:
                unresolved.append(("path", p, "no %s in the fleet repo at %s"
                                   % (fp, frev)))
        for tok in sorted(rev_paths):
            p, r = tok.rsplit("@", 1)
            if git(lane, "cat-file", "-e", "%s:%s" % (r, p)) is None:
                unresolved.append(("path", tok, "no %s at %s" % (p, r)))
            paths.add(tok)
        for p in sorted(paths):
            if "@" in p:
                continue
            if git(lane, "cat-file", "-e", "%s:%s" % (rev, p)) is None:
                unresolved.append(("path", p, "no blob/tree at C0"))

        # (b) explicit file:line
        for m in re.finditer(r"([A-Za-z0-9_.-]+\.(?:md|py|sh|json|js|txt|yml|yaml)):(\d+(?:[-,\s]*:?\d+(?:-\d+)?)*)", body):
            name, cluster = m.group(1), m.group(2)
            if name in FLEET_FILE:
                linespecs.append(("%s:%s" % (name, cluster), FLEET_FILE[name], cluster,
                                  FLEET_FILE_REV.get(name)))
                continue
            path = RESOLVE.get(name)
            if path is None:
                hits = [t for t in git(lane, "ls-tree", "-r", "--name-only", rev).split()
                        if t.rsplit("/", 1)[-1] == name]
                pref = []
                for prefix in PREFER:
                    pref = [h for h in hits if h.startswith(prefix)]
                    if len(pref) == 1:
                        break
                if len(pref) == 1:
                    path = pref[0]
                elif len(hits) == 1:
                    path = hits[0]
                else:
                    unresolved.append(("file", "%s:%s" % (name, cluster),
                                       "ambiguous basename %d hits" % len(hits)))
                    continue
            linespecs.append(("%s:%s" % (name, cluster), path, cluster, None))

        # (b2) bare clusters
        for spec, target in BARE.get(idx, []):
            r, path, ln = ref_target(target)
            if not ln:
                linespecs.append((spec, path, "0", r))
                continue
            linespecs.append((spec, path, ln, r))

        checked_here = 0
        for label, path, cluster, ref_rev in linespecs:
            checked_here += 1
            use_rev = ref_rev or rev
            repo = lane
            if path in {v[0] for v in FLEET_PATHS.values()}:
                repo = os.path.dirname(lane)
            if git(repo, "cat-file", "-e", "%s:%s" % (use_rev, path)) is None:
                unresolved.append(("file", label, "no %s at %s" % (path, use_rev)))
                continue
            n = lineno_cache(repo, use_rev, path)
            nums = [int(x) for x in re.findall(r"\d+", cluster)]
            if nums and n is not None and max(nums) > n:
                unresolved.append(("file", label, "line %d > %d lines of %s"
                                   % (max(nums), n, path)))

        total_checked += len(paths) + checked_here
        total_unresolved += len(unresolved)
        out.append({"heading": heading, "lines": [start, end],
                    "paths": len(paths), "linerefs": checked_here,
                    "unresolved": unresolved})

    for row in out:
        mark = "OK " if not row["unresolved"] else "XX "
        print("%s[%4d-%4d] paths=%-2d file:line=%-2d  %s"
              % (mark, row["lines"][0], row["lines"][1], row["paths"],
                 row["linerefs"], row["heading"]))
        for kind, what, why in row["unresolved"]:
            print("      unresolved %s %s — %s" % (kind, what, why))
    print("\nTOTAL citations checked=%d unresolved=%d across %d sections"
          % (total_checked, total_unresolved, len(out)))
    return 1 if total_unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
