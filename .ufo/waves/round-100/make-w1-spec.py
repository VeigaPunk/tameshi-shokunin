#!/usr/bin/env python3
"""Build .ufo/waves/round-100/w1-spec.json from the committed spec files.

Reads the instruments and freeze revisions from the sibling txt files, expands
the @@BASE@@/@@INSTR@@/@@FREEZE@@ placeholders in w1/specs/*.md (in a scratch
copy), and emits the wave spec the validator consumes. The committed spec
files keep their placeholders; the expanded bytes live in this json only.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read().strip()


BASE = read("base-rev.txt")
INSTR = read("instruments-rev.txt")
FREEZE = read("freeze-rev.txt")

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

ROLES = {}
SUMMARIES = {}
for fn in sorted(os.listdir(os.path.join(HERE, "w1", "specs"))):
    if not fn.endswith(".md"):
        continue
    name = fn[:-3]
    text = open(os.path.join(HERE, "w1", "specs", fn), encoding="utf-8").read()
    role = re.search(r"^# %s — (\S+) —" % re.escape(name), text, re.M).group(1)
    ROLES[name] = role
    SUMMARIES[name] = text.split("\n\n", 1)[1].strip().splitlines()[0]

items = []
for name in sorted(ROLES):
    spec = ".ufo/waves/round-100/w1/specs/%s.md" % name
    task = (GODSPEED
            + "\n## Your full task specification\nRead `/home/vgpnk/Projects/shokunin/tameshi-shokunin/%s` first and execute it end to end. It is your complete assignment; this line is only its summary.\n\n## Summary\n\n%s\n" % (spec, SUMMARIES[name]))
    items.append({"name": name, "role": ROLES[name],
                  "axes": ["verification-fixture-craft"], "item": task})

context = """# Tameshi round 100 — wave w1 (12 seats)

Lane repo (absolute): /home/vgpnk/Projects/shokunin/tameshi-shokunin — jj-colocated; the only writer is L1 `TameshiR100`. Never run a mutating git/jj command (no add/commit/push/checkout/reset/stash); read-only git (log, show, cat-file, grep, status, rev-parse) is fine. Never edit MANIFEST.json, a sibling repo, /home/vgpnk/Projects/shokunin/templates/ or /home/vgpnk/Projects/shokunin/scripts/. Never run `agent://all`. Never mutate a host sysctl or restart a host service.
Fleet root (read-only for you): /home/vgpnk/Projects/shokunin.
Round base: `%s`. Instruments commit: `%s`. Freeze commit: `%s` (claims C1/C2 frozen there).
Read first: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/plans/round-100.plan.md` (the two frozen claims and their kill rules) and `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-100/claims.json` (wording, sha256 pins, kill rules).
Your write scope: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-100/w1/<your reports and receipts>`. Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/tameshi-shokunin — write it at /home/vgpnk/Projects/shokunin/tameshi-shokunin/<that path>.
Scratch: `/fast/scratch/hyaku/tameshi-r100/<your-seat-name>/` (create with mkdir -p; pass it explicitly as TMPDIR/--work; delete it before you yield; receipts first copied into /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-100/w1). Never write under /tmp; never rely on an inherited TMPDIR.
Tooling authorization (operator, 2026-10-19): you may install or upgrade a tool that helps the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman is PAUSED host-wide: no pacman transaction at all; use `uv tool`/`npx`/an official binary in ~/.local/bin, or name the need in your report.
Do not commit, push, or leave a scratch tree on disk. Do not fabricate: an unrun check has not passed. A finding must carry the command and the observed output and exit.
Frozen claims (read `plans/round-100.plan.md`): C1 operability — at R, `python3 -I tools/registry-check.py --rev R --tag r100-c1` must print `REGISTRY_CHECK: held=12/12 superseded=0` exit 0 (selftest + red + green rows for tools/tally-reconcile.py, tools/control-assertion-audit-v2.py, tools/control-assertion-audit.py, tools/registry-cell-immutability.py); exit 2 at base; an always-green stub of any one tool flips its red row (held=11/12); the full registry at R `held=87/91 superseded=7` with the same four differing rows as base. C2 calibration — at R, `python3 -I tools/gate-line-recheck.py --repo . --rev R` over corpus/lessons/round-95..99.md must print `GATE_LINE_RECHECK records=5 pointers=21 hit=12 miss=6 absent=0 unbound=3` exit 1 with the six misses exactly round-95.md:17-22 (round-95 spot-check D1), round-95-only miss=6 exit 1, round-97-only and round-99-only hit=2 exit 0, `GATE_LINE_SELFTEST: 24/24 pass`; the quote-presence do-nothing control flags none of the six. FREEZE in your spec = the freeze commit above.
Your role decides what you may write: executor/scribe/scout write reports and receipts under the wave dir; reviewer/critic/mutation-tester/sentinel/connector/revenger are read-only on the lane and write only their own report and receipts under the wave dir. Every seat writes its report at /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-100/w1/<SEAT>.md.
""" % (BASE, INSTR, FREEZE)

spec = {
    "wave": "w1",
    "maxLanes": 12,
    "reportDir": ".ufo/waves/round-100/w1",
    "hoist": False,
    "context": context,
    "items": items,
}
with open(os.path.join(HERE, "w1-spec.json"), "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=1)
    f.write("\n")
print("items=%d roles=%s" % (len(items), ",".join(sorted(ROLES.values()))))
