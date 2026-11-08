#!/usr/bin/env python3
"""Write w1-dispatch.json (the driver's read shape) from the validator plan."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(HERE, "w1-plan-full.json"), encoding="utf-8"))
spec = json.load(open(os.path.join(HERE, "w1-spec.json"), encoding="utf-8"))
tasks = [{"name": t["name"], "agent": t["agent"], "task": t["task"]} for t in plan["taskCall"]["tasks"]]
dispatch = {
    "schema": "ufo-swarm-wave-dispatch-v1",
    "wave": "w1",
    "policy": plan["policy"],
    "counts": plan["counts"],
    "registry": plan["registry"],
    "compaction": plan.get("compaction"),
    "taskCall": {"context": plan["taskCall"]["context"], "tasks": tasks},
    "resumeSends": [],
    "note": "one batched task call; %d seats; lane tameshi round 99" % len(tasks),
}
with open(os.path.join(HERE, "w1-dispatch.json"), "w", encoding="utf-8") as f:
    json.dump(dispatch, f, indent=1)
    f.write("\n")
print("dispatch tasks=%d context=%d bytes" % (len(tasks), len(dispatch["taskCall"]["context"])))
