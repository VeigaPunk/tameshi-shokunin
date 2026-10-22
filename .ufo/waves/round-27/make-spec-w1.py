#!/usr/bin/env python3
"""Generate the round-27 wave spec (independent cold reads + falsifiers), policy v1 band 32-64.

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
W = '.ufo/waves/round-27/w1'
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
Tameshi round 27 (verification-fixture craft), one wave: fresh seats cold-read the SKILL.md sections whose cold-read credit drifted or never existed,
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

for i, m in enumerate(missing, 1):
    name = 'Read%02d' % i
    add(name, 'reviewer', ['calibration'],
        RECIPE.format(start=m['start'], heading=m['heading'], heading_json=json.dumps(m['heading'])) +
        f"\nMonitor reason for this section at {REV}: {m['reason']}.",
        f'Report: {W}/{name}.md, with exactly one ```json block as above. Last line exactly `COLDREAD {name}: <verdict>`.')

# --- falsifiers and the section-3 floor ------------------------------------------------
add('RerunC1', 'executor', ['calibration'], CLONE + f'Claim C1. Run `python3 .ufo/evidence/round-27/c1-measure.py --repo /tmp/<your-name>-r27 --rev {REV}` and, in a second clone, at base {BASE}. Paste outputs and exits. Then read the counter source: does `box3_mismatch` really compare SHONEN.md box 3 (the `[~]` self-assessment) with the monitor, and can it read 0 while a section stays uncovered? Run the monitor itself (`python3 .ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev {REV}`) and check the counter reports its numbers unchanged.')
add('RerunC2', 'executor', ['coverage'], CLONE + f'Claim C2. Run `python3 .ufo/evidence/round-27/c2-measure.py --repo /tmp/<your-name>-r27 --rev {REV}` and at base {BASE} (second clone). Then re-run the probe yourself in /tmp: `python3 .ufo/evidence/round-27/f8/anchor-probe.py --kumitate {KUM} --anchors .ufo/evidence/round-27/f8/anchors.json --out /tmp/<your-name>-receipt.json` and compare every result field with the committed receipt (stdout digests may differ only if node output embeds paths; say which). Paste every ANCHOR line.')
add('RerunRegistryCensus', 'executor', ['operability', 'freshness'], f'Routed item 3 and no-harm. Run: `git clone -q --no-hardlinks {LANE} /tmp/<your-name>-reg && cd /tmp/<your-name>-reg && git checkout -q --detach {REV} && python3 tools/registry-check.py --rev {REV}`. Paste the REGISTRY_CHECK line and every row that is not held. Then run `{FLEET}/scripts/sources-census.sh validate --root {FLEET} tameshi` (read-only validator), paste output and exit, and check rows S012, S090, S091 in corpus/SOURCES.md at {REV} against the contract in {FLEET}/CORPUS.md section "SOURCES.md — where a shokunin learns" (append-only rule: only status, recheck and used-by may change in place; compare S012 with `git -C {LANE} show {BASE}:corpus/SOURCES.md`).')
add('MutateC2Counter', 'mutation-tester', ['coverage'], CLONE + f'Claim C2 counter and probe. In scratch copies only: (a) mutate .ufo/evidence/round-27/c2-measure.py — drop the probe/anchors digest binding; drop the contract-quote line check; drop the external-row status/opened check; accept any S012 status — and for each, build a /tmp repo state (commit in your clone only) where the honest counter reads lower than the mutant; a mutant with no such state is a check this population cannot exercise. (b) mutate .ufo/evidence/round-27/f8/anchor-probe.py `meets()` to compare the mutant with the pristine run instead of the anchor, and to ignore the finding kind: does any committed artifact or the counter notice? List killed and surviving mutants with the exact edit.')
add('ReviewEntry', 'reviewer', ['coverage'], f'Claim C2. Review {LANE}/corpus/knowledge/oracle-anchored-survivors.md at {REV} against {E}/f8/anchors.json, receipt.json, probe.stdout, the pinned gate (`git -C {KUM} show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs`, header lines 35, 38, 61, 69, 71) and the round-26 entry {LANE}/corpus/knowledge/mutation-case-kumitate-cite-check.md §4. Every number, line, quote and class must match; every bound must be stated. List each mismatch with path:line.')
add('ReopenSources', 'reviewer', ['coverage'], f'Frontier step. Re-open by ordinary means S012 (https://arxiv.org/abs/2608.17214), S090 (https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3) and S091 (https://git-scm.com/docs/gitrevisions). For each, check the row in {LANE}/corpus/SOURCES.md at {REV} (`git -C {LANE} show {REV}:corpus/SOURCES.md`): tier, anchor, teaches, and every quote the entry {LANE}/corpus/knowledge/oracle-anchored-survivors.md and {E}/f8/anchors.json attribute to it, word for word, with its location and the 25-word limit. Per row: agree or disagree with reason.')
add('CriticAnchors', 'critic', ['coverage'], f'Claim C2. Attack the anchoring itself. (1) Were the anchors fixed before the probe ran (`git -C {LANE} log --format="%H %cI %s" -- .ufo/evidence/round-27/f8/`)? (2) Is a header comment line of the same file really "fixed outside the code under mutation" in S012\'s sense (abstract at https://arxiv.org/abs/2608.17214)? (3) Is S_PIN_INCLUDES honestly anchored, given the header fixes only 7-40 hex? (4) Could any anchored expectation have been read off the pristine output? (5) Does "anchored_holes=4" overstate anything the entry or README says? Say what evidence would make the C2 claim false.')
add('CriticRecordNoHarm', 'critic', ['calibration'], f'Attack the round\'s records and no-harm. (1) The SCORECARD.md sections "### Round 26 — correction (appended in round 27)" and "## Round 27 — monitor repair and frontier F8" at {REV}: do their numbers match {E}/c1-before.stdout, c2-before.stdout, c2-before-amended.stdout, the round-26 receipts {LANE}/.ufo/evidence/round-26/after/monitor-harmed-*.json and the closure {LANE}/corpus/lessons/round-26-verifier-spotcheck.md? Is the append-only rule kept (`git -C {LANE} diff --numstat {BASE} {REV}`)? (2) List every lane file changed {BASE}..{REV} and name the axis it could harm (depth: runner unchanged? registry, census, monitor). (3) Is contract-amendment-1 a narrowing of the C2 target or only a contract-legal correction?')
add('ReviewQuality', 'reviewer', ['calibration'], f'Review QUALITY.md criteria 53 and 54 added at {REV} (`git -C {LANE} diff {BASE} {REV} -- corpus/QUALITY.md`): is each lesson-backed (follow the cited lines), checkable, and shown able to fail as claimed? Make each one fail on a constructed case in a /tmp clone (e.g. run c1-measure.py at e08444d3 and c2-measure.py with a changed probe byte).')
add('ConnectorOverlap', 'connector', ['adjacency'], f'Sibling-overlap scan for C2 (oracle anchoring). Search sibling lanes under {FLEET}/*-shokunin (read-only; never tameshi) for knowledge on test-oracle anchoring, specification-anchored vs state-anchored or differential expectations, sysexits/usage exit 64, or content-pin prefix rules — especially kumitate (owner of cite-check.mjs: does its own corpus or a newer cite-check revision already pin any of the four holes S_OOR_EDGE, S_STRICT, S_USAGE, S_PIN_INCLUDES, or state a prefix rule for pins?). Report overlaps with path:line and whether tameshi absorbs nothing (report-only).')
add('ScoutLegAnchors', 'scout', ['coverage'], f'Planning data walk for the next F8 move (the L1 holds the planner seat; this item rides a scout). For each of the other eight recorded legs (kimi-census, surface-census, tsukuroi-census, mado-verify, checklist-run, claims-check, round-gate, sources-check; entries under {LANE}/corpus/knowledge/mutation-case-*.md and pins in {LANE}/tools/mutate-and-run.sh:603-620), list the survivors the lane calls suite holes and, for each, whether the pinned gate\'s header or usage text states the expected behaviour (path@rev:line, quote) — i.e. whether a specification anchor exists. Read-only; use `git -C <repo> show <rev>:<path>`. Output a table and a count.')
add('ScribeMistakes', 'scribe', ['calibration'], f'Draft (in your report only) candidate `## Mistakes` rows for {LANE}/corpus/lessons/round-27.md, format: class · evidence pointer · captured-by (criterion or rule, or `none`) · fix. Mine the round-26 closure {LANE}/corpus/lessons/round-26-verifier-spotcheck.md and lesson {LANE}/corpus/lessons/round-26.md: the cancelled harm-repair wave, the "numeric 8 → 8" record, the unreceipted registry reading, the counter that accepted unrelated receipts. For each, say whether QUALITY 53 or 54 (at {REV}) captures it and how the fix was shown able to fail. Plain English.')

spec = {'wave': 'round-27-w1', 'reportDir': W, 'context': CONTEXT, 'items': items}
out = Path(LANE + '/.ufo/waves/round-27/spec-w1.json')
out.write_text(json.dumps(spec, indent=1) + '\n')
print(len(items), 'items (', len(missing), 'cold reads ) ->', out)
