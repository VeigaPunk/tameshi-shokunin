#!/usr/bin/env python3
"""Write w1r-dispatch.json: residual re-run (attempt 2) of the four w1 seats that left no evidence.

Attempt 1's orchestrator was SIGTERM-killed mid-wave; w1 was finalized with output=null for every
seat. Seats R100C1 (critic), R100CN1 (connector), R100R1 (reviewer) and R100E1 (executor) left no
report and no receipt in w1/. They are re-run unchanged from their frozen specs under new names
(suffix `b`) so their files never collide with any late write of the dead originals. Every other
w1 seat left a report or receipts and is not re-run.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
w1 = json.load(open(os.path.join(HERE, "w1-dispatch.json"), encoding="utf-8"))
RERUN = ["R100C1", "R100CN1", "R100R1", "R100E1"]
NOTE = (
    "\n\n## Re-run note (attempt 2, L1 `TameshiR100a2`)\n"
    "You are `{new}`, a re-run of w1 seat `{old}` whose first run died with the orchestrator before "
    "writing anything. Execute the spec `{old}.md` unchanged against FREEZE `56f247da25a0252fcdb8e04a61675e0d73aae9ab` "
    "(the claims are frozen; do not read later lane commits as the claim). Wherever the spec says "
    "`{old}`, use `{new}` for your file names: report at "
    "`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-100/w1/{new}.md`, receipts "
    "`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-100/w1/{new}-*`, scratch "
    "`/fast/scratch/hyaku/tameshi-r100/{new}/`. Sibling seat reports already in w1/ (R100E2, R100E3, "
    "R100M1, R100RV1, R100R2-receipt-*, R100SN1-*, R100S1-*) are readable evidence; do not edit them.\n"
)
tasks = []
for t in w1["taskCall"]["tasks"]:
    if t["name"] not in RERUN:
        continue
    new = t["name"] + "b"
    body = t["task"].replace(
        "Report: write your scoped findings to .ufo/waves/round-100/w1/%s.md" % t["name"],
        "Report: write your scoped findings to .ufo/waves/round-100/w1/%s.md" % new,
    )
    body += NOTE.format(new=new, old=t["name"])
    tasks.append({"name": new, "agent": t["agent"], "task": body})
assert len(tasks) == 4, tasks
ctx = w1["taskCall"]["context"].replace("L1 `TameshiR100`", "L1 `TameshiR100a2`")
dispatch = {
    "schema": "ufo-swarm-wave-dispatch-v1",
    "wave": "w1r",
    "taskCall": {"context": ctx, "tasks": tasks},
    "resumeSends": [],
    "note": "residual call (<=4 seats) re-running the four evidence-less w1 seats; lane tameshi round 100 attempt 2",
}
with open(os.path.join(HERE, "w1r-dispatch.json"), "w", encoding="utf-8") as f:
    json.dump(dispatch, f, indent=1)
    f.write("\n")
print("w1r tasks=%d %s" % (len(tasks), [(t["name"], t["agent"]) for t in tasks]))
