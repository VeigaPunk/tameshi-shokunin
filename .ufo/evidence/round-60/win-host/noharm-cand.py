#!/usr/bin/env python3
"""noharm-cand.py — round-60 attempt-2 no-harm check for the win32 host.

The frozen no-harm instrument (`.ufo/evidence/round-48/quality/coldread-precheck.sh`
-> `.ufo/evidence/round-21/coldread/measure.py` -> `.ufo/evidence/round-18/measure.py`)
does not complete in round time on this host: the round-21 ledger records
75,889 inputs, the monitor spawns two git processes per input per measured
rev, and a git spawn costs ~0.044 s here (measured; Linux ~1-2 ms), so one
rev costs ~112 min and the floor->cand pair ~3.7 h (first background run was
killed after 35 min still inside the floor measure; second left running).

This script is a LANE-AUTHORED SUBSTITUTE, not the frozen instrument: it
imports the frozen round-18 module and runs its own decision functions
unchanged, with ONE short-circuit — `input_failures` fails fast (without
spawning) on any recorded input path that the floor->cand diff changed. The
short-circuit cannot flip a verdict:

* a floor-credited entry's recorded hash for a path equals the path's floor
  bytes (that is what its floor credit verified);
* the cand bytes of a changed path differ from its floor bytes (it is in the
  diff), so the recorded hash cannot match at cand: the entry fails at cand
  either way;
* entries and inputs off the changed set take the frozen code path verbatim.

The frozen monitor remains the decider wherever it can run; this receipt
records what the frozen code computes at the candidate revision on THIS
host, and the full frozen precheck keeps running beside it.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

FLOOR = "9bc9b20b5d6723a19d1b69c8edd7246f82ea3d78"
CAND = "f0ec3a5b4514b64752ff8fb1f97760bbc88f2acf"
LEDGER = ".ufo/evidence/round-21/coldread/ledger.json"
ROOT = Path(__file__).resolve().parents[4]


def git_bytes(args):
    return subprocess.run(args, capture_output=True).stdout


def main():
    impl = ROOT / ".ufo/evidence/round-18/measure.py"
    spec = importlib.util.spec_from_file_location("tameshi_r18_measure", impl)
    module = importlib.util.module_from_spec(spec)
    sys.modules["tameshi_r18_measure"] = module
    spec.loader.exec_module(module)

    diff = subprocess.run(["git", "-C", str(ROOT), "diff", "--name-only",
                           FLOOR, CAND], capture_output=True, text=True)
    changed = {line.strip().replace("\\", "/")
               for line in diff.stdout.splitlines() if line.strip()}

    real_input_failures = module.input_failures

    def short_circuit_input_failures(repo, rev, view):
        fails = []
        for path in sorted(view, key=lambda item: (str(type(item)), str(item))):
            if path in changed:
                fails.append("input-drift:%s" % path)
                continue
        if fails:
            return fails
        return real_input_failures(repo, rev, view)

    module.input_failures = short_circuit_input_failures
    # entry_is_stale re-derives staleness from input_failures too; the
    # patched function is what both credit and veto paths see.
    module.entry_is_stale.__globals__["input_failures"] = \
        short_circuit_input_failures

    skill_raw = git_bytes(["git", "-C", str(ROOT), "show",
                           "%s:SKILL.md" % CAND])
    ledger_raw = git_bytes(["git", "-C", str(ROOT), "show",
                            "%s:%s" % (CAND, LEDGER)])
    out = module.coldread(str(ROOT), CAND, skill_raw, ledger_raw, strict=True)
    credited = [s["heading"] for s in out["sections"] if s["credited"]]
    receipt = {
        "schema": "tameshi-noharm-substitute-v1",
        "lane": str(ROOT),
        "floor": FLOOR,
        "cand": CAND,
        "changed_paths": sorted(changed),
        "method": "frozen round-18 module functions, unchanged, with a "
                  "fail-fast short-circuit on changed input paths (proof in "
                  "the module docstring); ledger read from the candidate rev",
        "frozen_instrument_status": "infeasible in round time on this host "
                                    "(0.044 s/spawn x ~151,778 spawns/rev); "
                                    "frozen precheck left running beside it",
        "sections_total": out["sections_total"],
        "sections_credited": len(credited),
        "floor_credited_per_attempt1_receipt": 50,
        "credited_headings": credited,
        "not_credited": [{"heading": s["heading"], "reason": s["reason"]}
                         for s in out["sections"] if not s["credited"]],
    }
    dest = Path(__file__).with_name("noharm-cand.json")
    dest.write_text(json.dumps(receipt, indent=1, ensure_ascii=True) + "\n",
                    encoding="utf-8")
    print("NOHARM_CAND cand_credited=%d floor_credited=50 sections=%d "
          "changed=%d -> %s"
          % (len(credited), out["sections_total"], len(changed), dest.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
