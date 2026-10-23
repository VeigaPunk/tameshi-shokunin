#!/usr/bin/env python3
"""Round 32 (L1 TameshiR32) wave 2: fresh cold reads of every section the content revision drifts
(two sections per reader seat, three disjoint groupings A/B/C, bound by round-31 binding v5), sealed
held-out copy authors for C1 counter v2, and falsifiers of what wave 1 and the L1 produced.
Adapted from round-31 make-spec-w2.py.

Usage: make-spec-w2.py REV MONITOR_JSON FROZEN
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
REV, MON, FROZEN = sys.argv[1], sys.argv[2], sys.argv[3]
BASE = 'e24688b2ff6cca1c9ad20e112f02c629b8597ff8'
E = LANE + '/.ufo/evidence/round-32'
BIND = LANE + '/.ufo/evidence/round-31/coldread/bind-select-v5.py'
TR = E + '/coldread/traces'
W = '.ufo/waves/round-32/w2'
S = '/fast/scratch/hyaku/tameshi-r32-seats/<your-name>'
DIRECTIVE = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text()
skill = subprocess.run(['git', '-C', LANE, 'show', REV + ':SKILL.md'], capture_output=True, check=True).stdout
SKILL_SHA = hashlib.sha256(skill).hexdigest()
monitor = json.loads(Path(MON).read_text())
assert monitor['revision'] == REV and monitor['trace_gate'] == 'strict' and not monitor['overrides_used']
missing = monitor['coldread']['missing']
APPENDED = ['SCORECARD.md', 'LOG.md', '.ufo/evidence/round-21/coldread/ledger.json', 'corpus/lessons/round-32.md']
V2 = E + '/v2/c1-measure-v2.py'
FLEET_CLONE = (f'mkdir -p {S}/fleet; for d in {FLEET}/*-shokunin; do b=$(basename $d); '
               f'[ $b = tameshi-shokunin ] || ln -s $d {S}/fleet/$b; done; env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks {LANE} {S}/fleet/tameshi-shokunin; '
               f'git -C {S}/fleet/tameshi-shokunin checkout -q --detach {REV}; R={S}/fleet/tameshi-shokunin')
CL = f'{S}/c'
CLONE = (f'In your own clone at {REV} (`mkdir -p {S} && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks {LANE} {CL} && '
         f'git -C {CL} checkout -q --detach {REV}`)')

CONTEXT = f"""# Goal
Tameshi round 32 (verification-fixture craft), wave 2 (fresh cold reads + sealed held-out authors + falsifiers, policy v1). One measured claim, C1, operability, capability
acquisition: the new versioned tool {LANE}/tools/tally-audit.py audits the mutation runner {LANE}/tools/mutate-and-run.sh without editing it (static per-leg presence of the
--regression tally loop; the tally block against an oracle over every status 0-255 with overcount/undercount stress; the runner's own tally selftest harness against a panel of
27 faulty tally blocks). The runner stays byte-identical (sha256 a7d3f2dd…2eb9). Counter v1 ({E}/c1-measure.py) was met before data by a control (seat CriticC1's
allowlist) and re-designed before data as counter v2 ({V2}; {E}/v2/contract-amendment-1.json and -2.json; tool frozen at sha256 9639c458…99ef, lane commit {FROZEN}).
v2 predicate (label C1_R32V2_PASS): "C1 passes at REV iff REV's tools/tally-audit.py has sha256 TOOL_SHA256 and, run in the sandbox as `python3 tally-audit.py --runner COPY`,
exits 1 with a stdout line beginning `TALLY_AUDIT: FAIL` on every must-kill copy and exits 0 with a stdout line beginning `TALLY_AUDIT: PASS` on every must-accept copy, over
the 18 + 8 v1 copies and every valid held-out copy, with at least 6 valid held-out must-kill and 6 valid held-out must-accept copies, every held-out file added after this
counter, and REV's tools/mutate-and-run.sh at sha256 PINNED_RUNNER_SHA." The held-out set is written in THIS wave by the HeldOut* seats; the L1 commits every file they return,
unedited, and never drops one because the tool fails on it. Content revision {REV} carries the round's widely read input edits (corpus/SOURCES.md S097/S099 and the S094
used-by, corpus/README.md row, corpus/knowledge/runner-tally-audit.md, SCORECARD/LOG round-32 blocks). Those edits drift the lane's cold-read credit (strict monitor at {REV}:
{monitor['coldread']['sections_covered']}/{monitor['coldread']['sections_total']}). No-harm duty: each drifted section gets three independent fresh cold reads in this wave, at {REV}, by
three disjoint reader sets (A, B, C), bound by the frozen binding v5 ({BIND}). A failing read is a valid result.
The L1 TameshiR32 holds the planner seat and is the sole integrator. You did not write the content you attack or read.
# Bounds (binding)
- Do exactly what your item names; verdict first, then evidence (path:line, exact commands with observed output), then the smallest safe correction.
- Your `seat` value in any JSON is exactly your item name (e.g. `ColdA03`), never an agent id or a prefixed label.
- Your working directory is ONLY {S}/ (replace <your-name> with your item name exactly). One working directory per seat; never open another seat's scratch dir.
- Write NOTHING except your own report file, files in your own scratch dir and, for cold-read items only, trace receipts under {TR}/. Every `Report:` trailer path is relative
  to {LANE} — write it at {LANE}/<that path>, never at the fleet root {FLEET}.
- Never edit production files. Never run git write commands (add/commit/checkout/reset/stash/push/fetch/pull) in {LANE} or {FLEET}. Never run ANY `jj` command anywhere —
  not at the fleet root, not in {LANE}, not in a clone: any jj command snapshots a colocated working copy. Sandbox git only in your own clone under {S}/, with GIT_DIR,
  GIT_WORK_TREE and GIT_INDEX_FILE unset. Never touch the fleet repo {FLEET}, sibling lanes, lane jj state or the lane Git index. Sibling repos are read-only.
- Code runs only inside your own scratch clone or scratch dir. Never run gates, selftests or sweeps in {LANE} itself. Never run the full v2 counter (`c1-measure-v2.py` main) on the
  lane or on any clone holding the real tool: the L1's first full v2 run at the measurement revision is the measurement. Importing the counter module to call its validation
  functions, and running tools/tally-audit.py on your own copies, are allowed where your item says so. Wrap long runs in `timeout`. Every `--regression` run passes
  `--workdir {S}/rg-<k>`. Kill any process tree you started before you return.
- Never kill a process you did not start: before any kill, check that /proc/<pid>/cwd is inside your own scratch dir {S}/. Other seats run the same tools at the same time.
- No seat spawns, except an executor may spawn one read-only labrat probe for a falsifiable hypothesis.
- Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels,
  update-safety gate; record tool, version, channel and reason in your report). Pacman guard: all pacman transactions are PAUSED host-wide; install via uv tool, npx or an official
  binary in ~/.local/bin, or file an L0 question; never -Sy/-Syu/-U/-R, never restart a host service.
- Time box: 35 minutes; a partial honest report beats none. Never pass a model.
- Disk: bound every file you write (no unbounded loops or appends); never point a marker or log at a file Python imports (sitecustomize.py, *.pth); check `df -h /fast` before large builds.
  Never run du/find over /fast/scratch.
- Sourcing rule: open sources by ordinary means only. Never use a headless browser or any other tool to pass a bot challenge, captcha or access control.
- Write plain English, no run-together words. No producer-authentication, promotion or numeric-score claims."""

items = []


def add(name, role, axes, target, acceptance=None):
    acceptance = acceptance or f'Report: {W}/{name}.md'
    prompt = '/skill:godspeed\n' + DIRECTIVE + '\n# Target\n' + target.replace('<your-name>', name) + '\n\n# Acceptance\n' + acceptance + '\n'
    items.append({'name': name, 'role': role, 'axes': axes, 'prompt': prompt})


RECIPE = f"""Independent cold reads of {{n}} SKILL.md sections at lane revision {REV} (SKILL.md sha256 {SKILL_SHA}). Duty served: calibration no-harm (cold-read credit).
Sections (each runs to the line before the next #/##/### heading outside ``` fences):
{{listing}}
Steps, for EACH section:
1. Fleet-mirror clone (once): `{FLEET_CLONE}`.
2. Read the section in $R/SKILL.md. Decide its class: `instruction` (it tells a reader to run something) or `record` (it states facts with pointers).
3. Open what the section cites, under the trace collector, from inside $R, ONE command per trace, the trace file name written literally (no loop variable, no glob in the name):
   `cd $R && python3 tools/trace-inputs.py --root $R --out {TR}/<your-name>-<section number>-<k>.json -- <argv>` — for a record, a reader such as
   `python3 -c "import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]" <cited lane paths>`; for an instruction, run at least one command it names
   (skip any that needs more than 6 minutes and say so; any `--regression` gets `--workdir {S}/rg-<k>`). Check each claim you can against what you opened. Never read the live lane {LANE} during traces.
   EXCEPTION — four lane files are appended by the L1 after your read: {', '.join(APPENDED)}. Never open them under the trace collector or by path.
   If a section cites one, read it with `git -C $R show {REV}:<path>` outside the collector and record it in `external_inputs` as
   `tameshi-shokunin@{REV}:<path>` with the sha256 of those bytes (`git -C $R show {REV}:<path> | sha256sum`).
4. Verdict per section: `executed-ok` (instruction ran as written), `verified-record` (record checks out), `gap-minor` (true but with minor gaps; list them),
   `gap-blocking` or `wrong-expectation` (list them). Be honest: a failing verdict keeps the section uncovered, and that is a valid result.
5. Put EXACTLY ONE fenced ```json block in your report, schema tameshi-coldread-report-v2, with one element of `sections` per section you read:
   {{{{"schema": "tameshi-coldread-report-v2", "seat": "<your item name>", "skill_sha256": "{SKILL_SHA}", "read_rev": "{REV}",
     "sections": [{{{{"start": <start>, "heading": "<heading exactly as given>", "class": "...", "verdict": "...", "blocking_gaps": [], "wrong_expectations": [],
     "minor_gaps": [], "commands_executed": ["<argv as one string>", ...], "opened": ["<lane-relative path>", ...],
     "inputs": {{{{"<lane-relative path>": "<sha256 at {REV}>"}}}}, "external_inputs": {{{{}}}}, "traces": ["{TR}/<your-name>-<section number>-<k>.json", ...]}}}}, ...]}}}}
   `inputs` = every lane file you opened for THAT section (the trace receipts' `inputs` plus any file read by hand), lane-relative, sha256 of the bytes at {REV}; never SKILL.md
   itself. `external_inputs` keys are absolute paths or repo@rev:path outside the lane, plus the `tameshi-shokunin@{REV}:<path>` form above. Every command you ran is in commands_executed and has a receipt in traces.
   BINDING (frozen, {BIND}): a trace is credited only when your transcript holds a `bash` tool call that EXECUTES tools/trace-inputs.py
   (as `python3 tools/trace-inputs.py ...` or `cd $R && python3 tools/trace-inputs.py ...`) with `--out` naming that trace file literally, that call gets a non-error result,
   and the receipt's argv equals the argv after `--`. Do not wrap the call in echo, a loop, a heredoc, a script file or python -c.
Credit rules the assembler and monitor enforce: class `instruction` needs verdict `executed-ok` or `gap-minor`; class `record` needs `verified-record` or `gap-minor`; EVERY section
needs at least one command run under the trace collector with its receipt listed in `traces`. Receipt `rev` must equal `read_rev` (keep the clone detached at {REV}).
`skill_sha256` is the whole page's sha256 (given above). Input digests are full 64-hex sha256 values. Sibling reads made with `git show` do not appear in receipts: record them in
`external_inputs` as `<repo>@<40-hex rev>:<path>` with the sha256 of the bytes; never put a URL there. Line numbers belong to {REV} only.
If time runs short, report the sections you finished; an unread section is simply absent from your JSON.
Then, below the JSON, a short plain-English note of what you checked."""

n = len(missing)
def grp(off):
    out = []
    for k in range(0, n, 2):
        out.append(sorted({(k + off + d) % n for d in range(2) if k + d < n}))
    return out
groups = {'A': grp(0), 'B': grp(1), 'C': grp(2)}
for who, gs in groups.items():
    for g, idxs in enumerate(gs, 1):
        listing = '\n'.join(f'- section {i + 1}: start line {missing[i]["start"]}, heading exactly {json.dumps(missing[i]["heading"], ensure_ascii=False)}'
                            f' (monitor reason at {REV}: {missing[i]["reason"]})' for i in idxs)
        name = 'Cold%s%02d' % (who, g)
        body = RECIPE.format(n=len(idxs), listing=listing)
        if who != 'A':
            body = ('You are an independent reader; other seats read these sections too and you never see their reports. '
                    'Attack each section: a wrong or unverifiable statement is a failing verdict.\n') + body
        add(name, 'reviewer', ['calibration'], body,
            f'Report: {W}/{name}.md, with exactly one ```json block as above. Last line exactly `COLDREAD {name}: <verdict of each section, comma separated>`.')

for spec in json.loads(Path(E + '/w2-items.json').read_text()):
    add(spec['name'], spec['role'], spec['axes'], spec['target'].format(LANE=LANE, FLEET=FLEET, REV=REV, FROZEN=FROZEN, BASE=BASE, E=E, S=S,
                                                                         V2=V2, CL=CL, CLONE=CLONE, FLEET_CLONE=FLEET_CLONE))

spec = {'wave': 'round-32-w2', 'reportDir': W, 'context': CONTEXT, 'items': items}
out = Path(LANE + '/.ufo/waves/round-32/spec-w2.json')
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + '\n')
print(len(items), 'items for', n, 'sections ->', out)
