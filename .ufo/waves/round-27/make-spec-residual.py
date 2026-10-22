#!/usr/bin/env python3
"""Generate the round-27 residual call (<=8 reviewer seats, two corrected sections each).

Usage: make-spec-w1.py REV MONITOR_JSON
REV is the round's content revision; MONITOR_JSON is the strict round-21 monitor
(--explain) at REV. Every uncovered SKILL.md heading becomes one cold-read item for
a fresh seat that did not write the section. Adapted from round-26 make-spec-w2.py.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
KUM = FLEET + '/kumitate-shokunin'
REV, MON = sys.argv[1], sys.argv[2]
BASE = '91edf9cd82ccc72e10f62f81d37181f549d593b8'
PRE = '70df8d6a485418d9e57fed9d21e84fba71d4be66'
E = LANE + '/.ufo/evidence/round-27'
TR = E + '/coldread/traces'
W = '.ufo/waves/round-27/residual'
DIRECTIVE = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text()
skill = subprocess.run(['git', '-C', LANE, 'show', REV + ':SKILL.md'], capture_output=True, check=True).stdout
SKILL_SHA = hashlib.sha256(skill).hexdigest()
monitor = json.loads(Path(MON).read_text())
assert monitor['revision'] == REV and monitor['trace_gate'] == 'strict' and not monitor['overrides_used']
missing = monitor['coldread']['missing']
APPENDED = ['SCORECARD.md', 'LOG.md', '.ufo/evidence/round-21/coldread/ledger.json']

CLONE = ('Make a private clone first: `git clone -q --no-hardlinks %s /tmp/<your-name>-r27 && '
         'git -C /tmp/<your-name>-r27 checkout -q --detach %s` and run commands only inside it. ') % (LANE, REV)
FLEET_CLONE = (f'W=$(mktemp -d /tmp/<your-name>-XXXX); mkdir $W/fleet; for d in {FLEET}/*-shokunin; do b=$(basename $d); '
               f'[ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done; git clone -q --no-hardlinks {LANE} $W/fleet/tameshi-shokunin; '
               f'git -C $W/fleet/tameshi-shokunin checkout -q --detach {REV}; R=$W/fleet/tameshi-shokunin')

CONTEXT = f"""# Goal
Tameshi round 27 (verification-fixture craft), residual call: fresh seats cold-read the sections corrected after wave-1 cold reads failed them; the SKILL.md sections whose cold-read credit drifted or never existed,
and fresh falsifiers attack the round's two claims. Content revision {REV} (pre-registration {PRE}, base {BASE}).
C1 (calibration, harm repair): `python3 .ufo/evidence/round-27/c1-measure.py --repo CLONE --rev REV` runs the strict cold-read monitor;
before `covered=25/64 restraint=6 box3_mismatch=1` at base; target `covered=T/T restraint=8 box3_mismatch=0` at the landed head.
C2 (frontier F8, oracle anchoring): `python3 .ufo/evidence/round-27/c2-measure.py --repo CLONE --rev REV`; before `classified=0`; target `classified=4`.
Contract {E}/contract.json and contract-amendment-1.json. New entry {LANE}/corpus/knowledge/oracle-anchored-survivors.md; evidence {E}/f8/.
The L1 TameshiR27 holds the planner seat and is the sole integrator. You did not write the content you attack or read.
# Bounds (binding)
- Do exactly what your item names; verdict first, then evidence (path:line, exact commands with observed output), then the smallest safe correction.
- Write NOTHING except your own report file and, for cold-read items only, your trace receipts under {TR}/. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>, never at the fleet root.
- Never edit production files. Never run git write commands (add/commit/checkout/reset/stash/push/fetch/pull) in {LANE}. Never run ANY `jj` command anywhere —
  not at the fleet root {FLEET} (never), not in {LANE}, not in a clone: any jj command snapshots a colocated working copy. (The L1 alone may run read-only jj in the lane, and only with --ignore-working-copy.)
  Never touch the fleet repo {FLEET}, sibling lanes, lane jj state or the lane Git index. Read-only git with GIT_OPTIONAL_LOCKS=0 is fine. Sibling repos are read-only.
- Code runs only inside your own /tmp clone or /tmp scratch dir. Never run gates, selftests or sweeps in {LANE} itself.
- No seat spawns, except an executor may spawn one read-only labrat probe for a falsifiable hypothesis.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool, version, channel and reason in your report). Pacman guard: all pacman transactions are PAUSED host-wide; install via uv tool, npx or an official binary in ~/.local/bin; never -Sy/-Syu/-U/-R, never restart a host service.
- Sourcing rule: open sources by ordinary means only. Never use a headless browser or any other tool to pass a bot challenge, captcha or access control. Record a source you cannot open that way as unopened.
- Write plain English, no run-together words. No producer-authentication, promotion or numeric-score claims."""

items = []


def add(name, role, axes, target, acceptance=None):
    acceptance = acceptance or f'Report: {W}/{name}.md'
    prompt = '/skill:godspeed\n' + DIRECTIVE + '\n# Target\n' + target + '\n\n# Acceptance\n' + acceptance + '\n'
    items.append({'name': name, 'role': role, 'axes': axes, 'prompt': prompt})


RECIPE = f"""Independent cold read of ONE SKILL.md section at lane revision {REV} (SKILL.md sha256 {SKILL_SHA}). Claim served: C1 (calibration harm repair).
Section: start line {{start}}, heading exactly {{heading!r}}. It runs to the line before the next #/##/### heading outside ``` fences.
Steps:
1. Fleet-mirror clone: `{FLEET_CLONE}`.
2. Read the section in $R/SKILL.md. Decide its class: `instruction` (it tells a reader to run something) or `record` (it states facts with pointers).
3. Open what the section cites, under the trace collector, from inside $R:
   `cd $R && python3 tools/trace-inputs.py --root $R --out {TR}/<your-name>-<n>.json -- <argv>` — for a record, a reader such as
   `python3 -c "import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]" <cited lane paths>`; for an instruction, run at least one command it names
   (skip any that needs more than 6 minutes and say so). Check each claim you can against what you opened. Never read the live lane {LANE} during traces.
   EXCEPTION — three lane files are appended by the L1 after your read: {', '.join(APPENDED)}. Never open them under the trace collector or by path.
   If the section cites one, read it with `git -C $R show {REV}:<path>` outside the collector and record it in `external_inputs` as
   `tameshi-shokunin@{REV}:<path>` with the sha256 of those bytes (`git -C $R show {REV}:<path> | sha256sum`).
4. Verdict: `executed-ok` (instruction ran as written), `verified-record` (record checks out), `gap-minor` (true but with minor gaps; list them),
   `gap-blocking` or `wrong-expectation` (list them). Be honest: a failing verdict keeps the section uncovered, and that is a valid result.
5. Put EXACTLY ONE fenced ```json block in your report, schema tameshi-coldread-report-v2:
   {{{{"schema": "tameshi-coldread-report-v2", "seat": "<your-name>", "skill_sha256": "{SKILL_SHA}", "read_rev": "{REV}",
     "sections": [{{{{"start": {{start}}, "heading": {{heading_json}}, "class": "...", "verdict": "...", "blocking_gaps": [], "wrong_expectations": [],
     "minor_gaps": [], "commands_executed": ["<argv as one string>", ...], "opened": ["<lane-relative path>", ...],
     "inputs": {{{{"<lane-relative path>": "<sha256 at {REV}>"}}}}, "external_inputs": {{{{}}}}, "traces": ["{TR}/<your-name>-<n>.json", ...]}}}}]}}}}
   `inputs` = every lane file you opened (the trace receipts' `inputs` plus any file read by hand), lane-relative, sha256 of the bytes at {REV}; never SKILL.md
   itself. `external_inputs` keys are absolute paths or repo@rev:path outside the lane, plus the `tameshi-shokunin@{REV}:<path>` form above. Every command you ran is in commands_executed and has a receipt in traces.
Credit rules the assembler and monitor enforce (tested end to end in round 26, {LANE}/.ufo/waves/round-26/w1/ColdreadPilot.md, sections "Class/verdict pairing" and "Pitfalls"):
class `instruction` needs verdict `executed-ok` or `gap-minor`; class `record` needs `verified-record` or `gap-minor`; EVERY section needs at least one command run under the
trace collector with its receipt listed in `traces` (a record read counts). Receipt `rev` must equal `read_rev` (keep the clone detached at {REV}). `skill_sha256` is the whole page's sha256 (given above).
Sibling reads made with `git show` do not appear in receipts: record them in `external_inputs` as `<repo>@<40-hex rev>:<path>` with the sha256 of the bytes. Line numbers belong to {REV} only.
Then, below the JSON, a short plain-English note of what you checked."""


SEATS = 8
groups = [missing[i::SEATS] for i in range(SEATS)]
groups = [g for g in groups if g]
for i, g in enumerate(groups, 1):
    name = 'ReRead%02d' % i
    parts = []
    for k, m in enumerate(g, 1):
        parts.append(('PART %d of %d. ' % (k, len(g))) + RECIPE.format(start=m['start'], heading=m['heading'], heading_json=json.dumps(m['heading'])) +
                     f"\nMonitor reason for this section at {REV}: {m['reason']}.")
    note = ('You read %d sections, one after the other, each with its own fresh clone step if you like (one clone is fine). '
            'Put ONE ```json block in your report whose `sections` list has one object per section (same schema). '
            'Trace receipt names <your-name>-<n>.json must not collide across parts.\n\n' % len(g)) if len(g) > 1 else ''
    add(name, 'reviewer', ['calibration'], note + '\n\n'.join(parts),
        f'Report: {W}/{name}.md, with exactly one ```json block as above. Last line exactly `COLDREAD {name}: <verdicts in section order, comma-separated>`.')

spec = {'wave': 'round-27-residual', 'reportDir': W, 'context': CONTEXT, 'items': items}
out = Path(LANE + '/.ufo/waves/round-27/spec-residual.json')
out.write_text(json.dumps(spec, indent=1) + '\n')
print(len(items), 'seats for', len(missing), 'sections ->', out)
