#!/usr/bin/env python3
"""Generate the round-28 wave 1 (cold reads of every uncovered section, two independent readers each, plus falsifiers).

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
BASE = '06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c'
PRE = REV
E = LANE + '/.ufo/evidence/round-28'
TR = E + '/coldread/traces'
W = '.ufo/waves/round-28/w1'
DIRECTIVE = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text()
skill = subprocess.run(['git', '-C', LANE, 'show', REV + ':SKILL.md'], capture_output=True, check=True).stdout
SKILL_SHA = hashlib.sha256(skill).hexdigest()
monitor = json.loads(Path(MON).read_text())
assert monitor['revision'] == REV and monitor['trace_gate'] == 'strict' and not monitor['overrides_used']
missing = monitor['coldread']['missing']
APPENDED = ['SCORECARD.md', 'LOG.md', '.ufo/evidence/round-21/coldread/ledger.json', 'corpus/lessons/round-28.md']

CLONE = ('Make a private clone first: `git clone -q --no-hardlinks %s /tmp/<your-name>-r28 && '
         'git -C /tmp/<your-name>-r28 checkout -q --detach %s` and run commands only inside it. ') % (LANE, REV)
FLEET_CLONE = (f'W=$(mktemp -d /tmp/<your-name>-XXXX); mkdir $W/fleet; for d in {FLEET}/*-shokunin; do b=$(basename $d); '
               f'[ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done; git clone -q --no-hardlinks {LANE} $W/fleet/tameshi-shokunin; '
               f'git -C $W/fleet/tameshi-shokunin checkout -q --detach {REV}; R=$W/fleet/tameshi-shokunin')

CONTEXT = f"""# Goal
Tameshi round 28 (verification-fixture craft), wave 1 (build + falsify, policy v1). One claim:
C1 (calibration, harm repair, routed item 1 of {LANE}/corpus/lessons/round-27-verifier-spotcheck.md):
`python3 .ufo/evidence/round-27/c1-measure.py --repo CLONE --rev REV` runs the strict cold-read monitor; at base {BASE} it reads
`covered=60/64 restraint=6 box3_mismatch=1`; target at the landed head `covered=64/64 restraint=8 box3_mismatch=0` (exit 0).
Content revision {REV}: adds a Round-28 correction to SKILL.md section "### Round-21 gate/probe registry", re-opens source S059 (corpus/SOURCES.md),
and drafts {LANE}/corpus/lessons/round-28.md. The SOURCES edit drifted 10 credited sections (input-drift:corpus/SOURCES.md), so 14 sections are uncovered at {REV};
each gets two independent fresh cold reads in this wave. A failing read is a valid result and is recorded as it is.
The L1 TameshiR28 holds the planner seat and is the sole integrator. You did not write the content you attack or read.
# Bounds (binding)
- Do exactly what your item names; verdict first, then evidence (path:line, exact commands with observed output), then the smallest safe correction.
- Write NOTHING except your own report file and, for cold-read items only, your trace receipts under {TR}/. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>, never at the fleet root.
- Never edit production files. Never run git write commands (add/commit/checkout/reset/stash/push/fetch/pull) in {LANE}. Never run ANY `jj` command anywhere —
  not at the fleet root {FLEET} (never), not in {LANE}, not in a clone: any jj command snapshots a colocated working copy.
  Never touch the fleet repo {FLEET}, sibling lanes, lane jj state or the lane Git index. Read-only git with GIT_OPTIONAL_LOCKS=0 is fine. Sibling repos are read-only.
- Code runs only inside your own /tmp clone or /tmp scratch dir. Never run gates, selftests or sweeps in {LANE} itself.
- No seat spawns, except an executor may spawn one read-only labrat probe for a falsifiable hypothesis.
- Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool, version, channel and reason in your report). Pacman guard: all pacman transactions are PAUSED host-wide; install via uv tool, npx or an official binary in ~/.local/bin, or file an L0 question; never -Sy/-Syu/-U/-R, never restart a host service.
- Time box: finish and write your report within 15 minutes; a partial honest report beats none.
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



for k, m in enumerate(missing, 1):
    for who in ('A', 'B'):
        name = 'Read%02d%s' % (k, who)
        body = RECIPE.format(start=m['start'], heading=m['heading'], heading_json=json.dumps(m['heading'])) + f"\nMonitor reason for this section at {REV}: {m['reason']}."
        if who == 'B':
            body = ('You are the second, independent reader of this section; another seat reads it too and you never see its report. '
                    'Attack it: a wrong or unverifiable statement is a failing verdict.\n') + body
        add(name, 'reviewer', ['calibration'], body,
            f'Report: {W}/{name}.md, with exactly one ```json block as above. Last line exactly `COLDREAD {name}: <verdict>`.')

C27 = LANE + '/.ufo/evidence/round-27'
add('RerunC1', 'executor', ['calibration'], CLONE + f'Claim C1. Run `python3 .ufo/evidence/round-27/c1-measure.py --repo /tmp/<your-name>-r28 --rev {REV}` and at base {BASE}. Paste outputs and exits. Confirm the counter file is byte-identical at {BASE} and {REV} (`git diff {BASE} {REV} -- .ufo/evidence/round-27/c1-measure.py .ufo/evidence/round-21/coldread/measure.py .ufo/evidence/round-18/measure.py` empty). List the uncovered headings at {REV} with their monitor reasons (`--explain`).')
add('RerunCensus', 'executor', ['coverage'], f'Frontier step. In a fleet mirror (`{FLEET_CLONE}`; also `cp {FLEET}/shokunin.conf {FLEET}/CORPUS.md $W/fleet/../` is NOT enough: run instead `W2=$(mktemp -d); cp {FLEET}/shokunin.conf $W2/; ln -s {FLEET}/scripts $W2/scripts; git clone -q --no-hardlinks {LANE} $W2/tameshi-shokunin; git -C $W2/tameshi-shokunin checkout -q --detach {REV}; {FLEET}/scripts/sources-census.sh validate --root $W2 tameshi`), paste output and exit; repeat at {BASE}. Then check row S059 at {REV} against {BASE} (`git -C {LANE} diff {BASE} {REV} -- corpus/SOURCES.md`): only the used-by cell may change in place (contract: {FLEET}/CORPUS.md section "SOURCES.md — where a shokunin learns"); the appended lookup note and `Next unused id: S092` line must be appends. Verdict per check.')
add('RegistryCheckAtR', 'executor', ['operability'], f'Routed item 2 of {LANE}/corpus/lessons/round-27-verifier-spotcheck.md (registry no-harm at the head). In a fleet mirror: `{FLEET_CLONE}`, then `cd $R && python3 tools/registry-check.py --rev {REV}` (if it needs other flags, read its --help). Paste the summary line and every row that is not held, with its exit. Do the same at {BASE}. Compare row by row; name any row whose result differs and why. Write the full stdout into your report.')
add('ReopenS059', 'reviewer', ['coverage'], f'Frontier step. Re-open S059 https://bazel.build/remote/caching by ordinary means (curl). Check row S059 in `git -C {LANE} show {REV}:corpus/SOURCES.md` and the `## Gate` of `git -C {LANE} show {REV}:corpus/lessons/round-28.md`: is the quote "The action cache, which is a map of action hashes to action result metadata." verbatim and located as stated; does "Bazel currently does not track tools outside a workspace" still appear under Known issues; is the tier-A call and the use in the lesson within what the page says? Agree or disagree with reason.')
add('MutateAppendProbe', 'mutation-tester', ['calibration'], f'Lesson round-28 Mistake 1 claims an append of one blank line to a widely read lane file de-credits cold-read sections. Reproduce independently in /tmp clones at {REV}: for each of corpus/SOURCES.md, corpus/README.md, corpus/QUALITY.md, SHONEN.md, LOG.md, SCORECARD.md, corpus/lessons/round-28.md and .ufo/evidence/round-21/coldread/ledger.json (append a JSON-neutral change only for the ledger: skip it if it cannot be made neutral), append, commit in the clone, run `python3 .ufo/evidence/round-27/c1-measure.py --repo <clone> --rev HEAD`. Table: file → covered count. Critical for the L1: confirm whether SCORECARD.md, LOG.md and the lesson file can be appended after the cold reads without any drop. Compare with `git -C {LANE} show {REV}:.ufo/evidence/round-28/append-probe.txt`.')
add('CriticC1', 'critic', ['calibration'], f'Attack claim C1. (1) Is "repair" honest when the round itself drifted 10 sections by editing SOURCES.md and then re-reads them (see lesson {LANE}/corpus/lessons/round-28.md at {REV})? (2) Does 64/64 from fresh reads at {REV} still hold at the landed head if the L1 later appends SCORECARD.md, LOG.md, the ledger and the lesson? (3) Does restraint 8 / box3_mismatch 0 overstate SHONEN box 3 (read `git -C {LANE} show {REV}:SHONEN.md`)? (4) What would make C1 false? Name evidence, not opinion.')
add('ReviewSkillCorrection', 'reviewer', ['calibration'], f'Review the "Round 28 correction" paragraph added to SKILL.md (`git -C {LANE} diff {BASE} {REV} -- SKILL.md`). Check each statement against bytes: `.ufo/evidence/round-21/c2-count.py` lines 19 and 52 at {REV}; whether tools/round21-measure.py --claim c2 and --selftest really reach the live lane through FLEET; `.ufo/waves/round-21/routemix-spec1.json` ok value; the ReRead03 finding in {LANE}/.ufo/waves/round-27/residual/ReRead03.md. List each mismatch with path:line.')
add('ConnectorOverlap', 'connector', ['adjacency'], f'Sibling-overlap scan for the round-28 mistake (input-digest-keyed credit lost by the round\'s own bookkeeping edits). Search sibling lanes under {FLEET}/*-shokunin (read-only; never tameshi) for monitors or ledgers that key credit or verdict reuse to input digests (sha256 of inputs, "input-drift", "stale", cache key) and for lessons about edit ordering versus verification. Report overlaps with path:line and whether tameshi absorbs nothing (report-only).')
add('ScoutNextFrontier', 'scout', ['coverage'], f'Planning data walk (the L1 holds the planner seat; this rides a scout). For routed items 2-8 of {LANE}/corpus/lessons/round-27-verifier-spotcheck.md, state whether each is still open at {REV}, and for each fix name the lane files it must edit and how many cold-read ledger entries record those files as inputs (count keys in `git -C {LANE} show {REV}:.ufo/evidence/round-21/coldread/ledger.json` entries[].inputs). Output a table; rank fixes by credit drift cost.')
add('ScribeMistakes', 'scribe', ['calibration'], f'Draft (in your report only) candidate `## Mistakes` rows for {LANE}/corpus/lessons/round-28.md, format: class · evidence pointer · captured-by (criterion or rule, or `none`) · fix. Mine {LANE}/corpus/lessons/round-27-verifier-spotcheck.md, {LANE}/corpus/lessons/round-26-verifier-spotcheck.md and the round-28 lesson at {REV} (one extra: the L1 first drafted a new source row S092 for a URL already registered as S059; the census W04 warning caught it). For each, name the QUALITY.md criterion (`git -C {LANE} show {REV}:corpus/QUALITY.md`) that captures it or `none`. Plain English.')

spec = {'wave': 'round-28-w1', 'reportDir': W, 'context': CONTEXT, 'items': items}
out = Path(LANE + '/.ufo/waves/round-28/spec-w1.json')
out.write_text(json.dumps(spec, indent=1) + '\n')
print(len(items), 'items for', len(missing), 'sections ->', out)
