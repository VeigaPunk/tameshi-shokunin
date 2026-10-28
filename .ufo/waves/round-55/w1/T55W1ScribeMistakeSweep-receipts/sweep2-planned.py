#!/usr/bin/env python3
"""Sweep 2: the round-54 `Planned (round 55)` row vs the tree at REV.

Rule fixed before the run: a planned item is ALREADY-DONE iff the artifact the item
proposes to create/modify exists at REV with the property the item proposes; OPEN iff
it does not. Each item gets one command and one observable.
Usage: sweep2-planned.py LANE REV OUT.json
"""
import json, subprocess, sys
LANE, REV, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

def git(*a):
    return subprocess.run(["git", "-C", LANE, *a], capture_output=True, text=True)

def show(p):
    r = git("show", f"{REV}:{p}")
    return r.stdout if r.returncode == 0 else None

res = []

p = "corpus/knowledge/delta-debugging-minimization-contract.md"
present = git("cat-file", "-e", f"{REV}:{p}").returncode == 0
add = git("log", "--diff-filter=A", "--format=%h %ad", "--date=short", "--", p).stdout.strip().splitlines()
sources = show("corpus/SOURCES.md") or ""
cited = [l.split("|")[1].strip() for l in sources.splitlines()
         if "delta-debugging-minimization-contract.md" in l and l.startswith("|")]
res.append({"n": 1, "item": "adopt the staged merge/tameshi delta-debugging-minimization-contract.md entry",
            "command": f"git cat-file -e {REV}:{p}; git log --diff-filter=A -- {p}",
            "observable": {"present_at_rev": present, "introduced": add[:1], "sources_rows_citing_it": cited},
            "verdict": "ALREADY-DONE" if present and cited else "OPEN"})

reg = json.loads(show("tools/registry.json") or '{"rows":[]}')
envrow = [r for r in reg["rows"] if r["name"].startswith("env-diff")]
cell = envrow[0].get("scratch_root", "") if envrow else ""
c2before = show(".ufo/evidence/round-54/before/c2.stdout") or ""
envline = [l for l in c2before.splitlines() if "env-diff" in l]
res.append({"n": 2, "item": "env-diff --contract residue: unusable scratch root must be could-not-evaluate, not unavailable rc 1",
            "command": f"git show {REV}:tools/registry.json -> env-diff-selftest.scratch_root; git show {REV}:.ufo/evidence/round-54/before/c2.stdout | grep env-diff",
            "observable": {"registry_cell_names_contract_mode": "--contract" in cell,
                           "base_receipt_line": envline[0][:160] if envline else None},
            "verdict": "OPEN" if (envline and "rc=1" in envline[0]) else "ALREADY-DONE"})

mode_names = [r["name"].replace("-selftest", "") for r in reg["rows"] if "scratch_root" in r]
cells_wo_modes = [r["name"] for r in reg["rows"] if "scratch_root" in r
                  and not any(k in r["scratch_root"] for k in ("Allocating modes", "modes:"))]
res.append({"n": 3, "item": "C2 follow-on: every documented mode of the seven tools reports the class, not the self-test only",
            "command": f"git show {REV}:tools/registry.json -> the 7 scratch_root cells; grep them for a mode list",
            "observable": {"tools": len(mode_names), "cells_naming_no_mode_list": len(cells_wo_modes),
                           "cell_sample": ([r for r in reg["rows"] if "scratch_root" in r][0]["scratch_root"])[:120]},
            "verdict": "OPEN" if cells_wo_modes else "ALREADY-DONE"})

sl = show("corpus/knowledge/service-limits.md") or ""
u1 = [l for l in sl.splitlines() if "U1" in l]
skill = show("SKILL.md") or ""
carried = [l.strip() for l in skill.splitlines() if "U1–U6" in l or "U1-U6" in l]
res.append({"n": 4, "item": "service-limits §5 U1 heading re-read (carried from round 53)",
            "command": f"git show {REV}:corpus/knowledge/service-limits.md | grep U1; git show {REV}:SKILL.md | grep 'U1'",
            "observable": {"service_limits_u1_lines": [u[:140] for u in u1[:3]], "skill_carried_line": carried[:1]},
            "verdict": "OPEN" if carried else "ALREADY-DONE"})

print(f"REV={REV}")
print(f"{'#':2s} {'verdict':13s} item")
print("-" * 100)
for r in res:
    print(f"{r['n']:<2d} {r['verdict']:13s} {r['item'][:80]}")
    print(f"    cmd: {r['command']}")
    print(f"    obs: {json.dumps(r['observable'])[:400]}")
print()
print("ALREADY_DONE=%d OPEN=%d" % (sum(r["verdict"] == "ALREADY-DONE" for r in res),
                                   sum(r["verdict"] == "OPEN" for r in res)))
json.dump({"rev": REV, "items": res}, open(OUT, "w"), indent=1)
