#!/usr/bin/env python3
"""Generate the round-26 wave-2 spec (falsify + independent cold reads), policy v1 band 32-64.

Usage: make-spec-w2.py REV MONITOR_JSON
MONITOR_JSON is the strict round-21 monitor (--explain) at REV; every uncovered SKILL.md
heading becomes one cold-read item for a fresh seat that did not write the section.
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
PRE = '622d31d90b1fbc55c56e91a2b012bc18d6f1421a'
BASE = 'd4140796f4e48e8ec81b793facba73fbd03b4443'
E = LANE + '/.ufo/evidence/round-26'
TR = E + '/coldread/traces'
W = '.ufo/waves/round-26/w2'
DIRECTIVE = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text()
skill = subprocess.run(['git', '-C', LANE, 'show', REV + ':SKILL.md'], capture_output=True, check=True).stdout
SKILL_SHA = hashlib.sha256(skill).hexdigest()
monitor = json.loads(Path(MON).read_text())
assert monitor['revision'] == REV and monitor['trace_gate'] == 'strict' and not monitor['overrides_used']
missing = monitor['coldread']['missing']

CLONE = ('Make a private clone first: `git clone -q --no-hardlinks %s /tmp/<your-name>-r26 && '
         'git -C /tmp/<your-name>-r26 checkout -q --detach %s` and run commands only inside it. ') % (LANE, REV)
FLEET_CLONE = (f'W=$(mktemp -d /tmp/<your-name>-XXXX); mkdir $W/fleet; for d in {FLEET}/*-shokunin; do b=$(basename $d); '
               f'[ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done; git clone -q --no-hardlinks {LANE} $W/fleet/tameshi-shokunin; '
               f'git -C $W/fleet/tameshi-shokunin checkout -q --detach {REV}; R=$W/fleet/tameshi-shokunin')

CONTEXT = f"""# Goal
Tameshi round 26 (verification-fixture craft), wave 2 of 2: fresh falsifiers attack what wave 1 and the L1 produced, and fresh seats
cold-read the SKILL.md sections whose cold-read credit drifted. Final content revision {REV} (pre-registration {PRE}, base {BASE}).
C1 (depth): ninth recorded ledger leg js-cite-check (kumitate scripts/cite-check.mjs, 5/10). Counter `python3 .ufo/evidence/round-26/c1-measure.py --repo CLONE`
(before depth_score=8 at base; target recorded_cases=9 wired_legs=9 depth_score=9). C2 (calibration): `python3 .ufo/evidence/round-26/c2-measure.py --repo CLONE`
(before mismatches=3/3; target 0/3). Contract {E}/contract.json. Wave-1 reports: {LANE}/.ufo/waves/round-26/w1/.
The L1 TameshiR26 holds the planner seat and is the sole integrator. You did not write the content you attack or read.
# Bounds (binding)
- Do exactly what your item names; verdict first, then evidence (path:line, exact commands with observed output), then the smallest safe correction.
- Write NOTHING except your own report file and, for cold-read items only, your trace receipts under {TR}/. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>, never at the fleet root.
- Never edit production files. Never run git write commands (add/commit/checkout/reset/stash/push/fetch/pull) in {LANE}. Never run ANY `jj` command anywhere —
  not `jj log`, not `jj st`, not at the fleet root {FLEET}, not in {LANE}, not in a clone: any jj command snapshots a colocated working copy.
  Never touch the fleet repo {FLEET}, sibling lanes, lane jj state or the lane Git index. Read-only git with GIT_OPTIONAL_LOCKS=0 is fine. Sibling repos are read-only.
- Code runs only inside your own /tmp clone or /tmp scratch dir. Never run gates, selftests or sweeps in {LANE} itself.
- No seat spawns, except an executor may spawn one read-only labrat probe for a falsifiable hypothesis.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool, version, channel and reason in your report). Pacman guard: all pacman transactions are PAUSED host-wide; install via uv tool, npx or an official binary in ~/.local/bin; never -Sy/-Syu/-U/-R, never restart a host service.
- Sourcing rule (Main, 2026-10-22T10:24Z): open sources by ordinary means only. Never use a headless browser or any other tool to pass a bot challenge, captcha or access control. Record a source you cannot open that way as unopened.
- Write plain English, no run-together words. No producer-authentication, promotion or numeric-score claims."""

items = []


def add(name, role, axes, target, acceptance=None):
    acceptance = acceptance or f'Report: {W}/{name}.md'
    prompt = '/skill:godspeed\n' + DIRECTIVE + '\n# Target\n' + target + '\n\n# Acceptance\n' + acceptance + '\n'
    items.append({'name': name, 'role': role, 'axes': axes, 'prompt': prompt})


RECIPE = f"""Independent cold read of ONE SKILL.md section at lane revision {REV} (SKILL.md sha256 {SKILL_SHA}).
Section: start line {{start}}, heading exactly {{heading!r}}. It runs to the line before the next #/##/### heading outside ``` fences.
Steps:
1. Fleet-mirror clone: `{FLEET_CLONE}`.
2. Read the section in $R/SKILL.md. Decide its class: `instruction` (it tells a reader to run something) or `record` (it states facts with pointers).
3. Open what the section cites, under the trace collector, from inside $R:
   `cd $R && python3 tools/trace-inputs.py --root $R --out {TR}/<your-name>-<n>.json -- <argv>` — for a record, a reader such as
   `python3 -c "import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]" <cited lane paths>`; for an instruction, run at least one command it names
   (skip any that needs more than 6 minutes and say so). Check each claim you can against what you opened. Never read the live lane {LANE} during traces.
4. Verdict: `executed-ok` (instruction ran as written), `verified-record` (record checks out), `gap-minor` (true but with minor gaps; list them),
   `gap-blocking` or `wrong-expectation` (list them). Be honest: a failing verdict keeps the section uncovered, and that is a valid result.
5. Put EXACTLY ONE fenced ```json block in your report, schema tameshi-coldread-report-v2:
   {{{{"schema": "tameshi-coldread-report-v2", "seat": "<your-name>", "skill_sha256": "{SKILL_SHA}", "read_rev": "{REV}",
     "sections": [{{{{"start": {{start}}, "heading": {{heading_json}}, "class": "...", "verdict": "...", "blocking_gaps": [], "wrong_expectations": [],
     "minor_gaps": [], "commands_executed": ["<argv as one string>", ...], "opened": ["<lane-relative path>", ...],
     "inputs": {{{{"<lane-relative path>": "<sha256 at {REV}>"}}}}, "external_inputs": {{{{}}}}, "traces": ["{TR}/<your-name>-<n>.json", ...]}}}}]}}}}
   `inputs` = every lane file you opened (the trace receipts' `inputs` plus any file read by hand), lane-relative, sha256 of the bytes at {REV}; never SKILL.md
   itself. `external_inputs` keys are absolute paths or repo@rev:path outside the lane. Every command you ran is in commands_executed and has a receipt in traces.
Credit rules the assembler and monitor enforce (tested end to end by wave-1 seat ColdreadPilot, {LANE}/.ufo/waves/round-26/w1/ColdreadPilot.md, sections "Class/verdict pairing" and "Pitfalls"):
class `instruction` needs verdict `executed-ok` or `gap-minor`; class `record` needs `verified-record` or `gap-minor`; EVERY section needs at least one command run under the
trace collector with its receipt listed in `traces` (a record read counts). Receipt `rev` must equal `read_rev` (keep the clone detached at {REV}). `skill_sha256` is the whole page's sha256 (given above).
Sibling reads made with `git show` do not appear in receipts: record them in `external_inputs` as `<repo>@<40-hex rev>:<path>` with the sha256 of the bytes. Line numbers belong to {REV} only.
Then, below the JSON, a short plain-English note of what you checked."""

for i, m in enumerate(missing, 1):
    name = 'Read%02d' % i
    add(name, 'reviewer', ['calibration'],
        RECIPE.format(start=m['start'], heading=m['heading'], heading_json=json.dumps(m['heading'])) +
        f"\nMonitor reason for this section at {REV}: {m['reason']}.",
        f'Report: {W}/{name}.md, with exactly one ```json block as above. Last line exactly `COLDREAD {name}: <verdict>`.')

# --- attacks on wave-1 output and the final content --------------------------------
add('RerunC1', 'executor', ['depth'], CLONE + f'Run `python3 .ufo/evidence/round-26/c1-measure.py --repo /tmp/<your-name>-r26` and the scorecard command D from {LANE}/SCORECARD.md:72-73 with REV={REV}. Also run it with --repo at a clone of base {BASE}. Paste outputs and exits.')
add('RerunC2', 'executor', ['calibration'], CLONE + f'Run `python3 .ufo/evidence/round-26/c2-measure.py --repo /tmp/<your-name>-r26` at {REV} and at base {BASE} (second clone). Paste outputs and exits, then read each resolved item\'s text yourself: does the repo state really match what the counter says?')
add('RerunRegression', 'executor', ['depth'], CLONE + 'Run `bash tools/mutate-and-run.sh --regression` and `--selftest` in the clone. Paste the REGRESSION and MUTATE_SELFTEST lines.')
add('RerunInterop', 'executor', ['coverage'], CLONE + f'Run `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root {FLEET}` and `--selftest`. Paste every MTE_ line. Check the tool sha256 equals the one named in corpus/knowledge/mte-report-interop.md verified-at.')
add('RerunRegistry', 'executor', ['operability'], f'Run: `git clone -q --no-hardlinks {LANE} /tmp/<your-name>-reg && cd /tmp/<your-name>-reg && python3 tools/registry-check.py --rev {REV}`. Paste the REGISTRY_CHECK line and every row that is not held.')
add('RerunCensus', 'executor', ['freshness'], f'Run `{FLEET}/scripts/sources-census.sh validate --root {FLEET} tameshi` (read-only validator) and paste output and exit. Then check the new SOURCES rows of round 26 in {LANE}/corpus/SOURCES.md at {REV} against the contract in {FLEET}/CORPUS.md.')
add('ReopenSources', 'reviewer', ['depth'], f'Re-open every SOURCES.md row added in round 26 (`git -C {LANE} diff {BASE} {REV} -- corpus/SOURCES.md`) by ordinary means and check each located quote word for word, its location and the 25-word limit. Report per row: agree or disagree with reason.')
add('ReviewEntry', 'reviewer', ['depth'], f'Review the new entry {LANE}/corpus/knowledge/mutation-case-kumitate-cite-check.md at {REV} against the committed sweep evidence {E}/cite-check/. Every number, id and witness case must match; every claim about the gate must hold in the pinned bytes (`git -C {KUM} show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs`). List each mismatch.')
add('ReviewSkillSection', 'reviewer', ['depth'], f'Review the SKILL.md section "## Ninth recorded case — round 26" and its survivor table and registry table at {REV}: every claim against the evidence and the wave-1 probe reports {LANE}/.ufo/waves/round-26/w1/Probe*.md.')
add('ReviewCorrections', 'reviewer', ['calibration'], f'Review the round-25 corrections appended in round 26 (SCORECARD.md after "### Round 25 — measured results (TameshiR25)" and corpus/lessons/round-25.md end) against {LANE}/.ufo/evidence/round-25/contract-amendment-3.json and `git -C {LANE} log --format="%h %cI %s" 2a97ec1..f4e8f7d`. Are they true, complete and append-only (`git diff {BASE} {REV} --numstat`)?')
add('ReviewQualityNew', 'reviewer', ['calibration'], f'Review the QUALITY.md criteria added in round 26 (`git -C {LANE} diff {BASE} {REV} -- corpus/QUALITY.md`): is each lesson-backed, checkable, and shown able to fail as claimed? Try to make each one fail on a constructed case.')
add('CriticScorecardRows', 'critic', ['calibration'], f'Attack the SCORECARD round-26 section at {REV}: do the before/after values, counters and measured commit match the committed receipts in {E}? Any universal clause the counter does not enumerate? Any number that is not re-derivable by one command?')
add('CriticNoHarm', 'critic', ['calibration'], f'Attack no-harm: list every lane file changed between {BASE} and {REV} (`git diff --numstat`), and for each say which axis it could harm and whether a committed receipt shows it did not (monitor, registry, census, regression, interop). Name any unmeasured harm.')
add('CriticTrends', 'critic', ['depth', 'calibration'], 'Attack the round\'s likely trend verdicts: expansion (new admitted ground?), quality (a superseding or stronger entry?), discernment (did the lane recognise quality better: predictions, equivalence handling, the round-25 spot-check routed items). Say what evidence would make each "improved" false.')
add('MutateQualityChecks', 'mutation-tester', ['calibration'], CLONE + f'Run: mutate .ufo/evidence/round-26/c2-measure.py in scratch copies (drop the case-insensitive match; drop the receipt check; accept any sha prefix length 1) and run each against the clone at {REV} and at base {BASE}. Which mutants change no result? Those are checks this population cannot exercise; list them.')
add('ConnectorLedger', 'connector', ['adjacency'], f'Cross-check the ninth leg across lane records at {REV}: runner ledger lines, SKILL.md, PROVINCE.md, corpus/README.md, the new entry, SCORECARD and mte-interop agree on leg name, rev, blob sha256, kill rate and survivors. Report any disagreement with path:line.')

spec = {'wave': 'round-26-w2', 'reportDir': W, 'context': CONTEXT, 'items': items}
out = Path(LANE + '/.ufo/waves/round-26/spec-w2.json')
out.write_text(json.dumps(spec, indent=1) + '\n')
print(len(items), 'items (', len(missing), 'cold reads ) ->', out)
