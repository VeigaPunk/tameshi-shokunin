#!/usr/bin/env python3
"""Generate the round-29 wave 1 (three independent cold reads of every uncovered section, F6 build, routed-defect checks, first falsifiers).

Usage: make-spec-w1.py REV MONITOR_JSON
REV is the round's content revision (commit A, which carries every widely read
input edit of the round); MONITOR_JSON is the strict round-21 monitor (--explain)
at REV. Adapted from round-28 make-spec-w1.py: a third reader per section
(round 28 lost 12 of 38 seats to a provider limit), round-29 paths.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
KUM = FLEET + '/kumitate-shokunin'
REV, MON, FROZEN = sys.argv[1], sys.argv[2], sys.argv[3]
BASE = '367ec0f1d79cb9b67d724f2962e7554a0841b1fc'
PRE = REV
E = LANE + '/.ufo/evidence/round-29'
TR = E + '/coldread/traces'
W = '.ufo/waves/round-29/w1'
DIRECTIVE = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text()
skill = subprocess.run(['git', '-C', LANE, 'show', REV + ':SKILL.md'], capture_output=True, check=True).stdout
SKILL_SHA = hashlib.sha256(skill).hexdigest()
monitor = json.loads(Path(MON).read_text())
assert monitor['revision'] == REV and monitor['trace_gate'] == 'strict' and not monitor['overrides_used']
missing = monitor['coldread']['missing']
APPENDED = ['SCORECARD.md', 'LOG.md', '.ufo/evidence/round-21/coldread/ledger.json', 'corpus/lessons/round-29.md']

CLONE = ('Make a private clone first: `git clone -q --no-hardlinks %s /tmp/<your-name>-r29 && '
         'git -C /tmp/<your-name>-r29 checkout -q --detach %s` and run commands only inside it. ') % (LANE, REV)
FLEET_CLONE = (f'W=$(mktemp -d /tmp/<your-name>-XXXX); mkdir $W/fleet; for d in {FLEET}/*-shokunin; do b=$(basename $d); '
               f'[ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done; git clone -q --no-hardlinks {LANE} $W/fleet/tameshi-shokunin; '
               f'git -C $W/fleet/tameshi-shokunin checkout -q --detach {REV}; R=$W/fleet/tameshi-shokunin')

CONTEXT = f"""# Goal
Tameshi round 29 (verification-fixture craft), wave 1 (build + first falsifiers, policy v1). Two claims, frozen with their counters and
predicates in {LANE}/.ufo/evidence/round-29/contract.json at commit {REV} and re-frozen before any data, after a control wave, in
contract-amendment-1.json (C2) and contract-amendment-2.json (C1) at lane commit {FROZEN}:
C1 (calibration repair, routed item 1 of {LANE}/corpus/lessons/round-28-verifier-spotcheck.md): `python3 .ufo/evidence/round-29/c1-measure-v2.py --repo CLONE --rev REV`
prints `PREDICATE: C1_R29_V2_PASS=true|false`; at base {BASE} the strict monitor reads covered=63/64 restraint=6 box3_mismatch=1; at {REV} 52/64, because {REV}
carries every widely read input edit of the round (corpus/SOURCES.md S024 re-open, corpus/README.md Round-29 section, corpus/QUALITY.md 55-57) BEFORE the cold reads.
Each of the 12 uncovered sections gets three independent fresh cold reads in this wave, at {REV}. A failing read is a valid result and is recorded as it is.
C2 (coverage, frontier F6, sourced on S024): `python3 .ufo/evidence/round-29/c2-measure-v2.py --repo CLONE --rev REV` prints `PREDICATE: C2_F6_V2_PASS=true|false`:
an original fixture built on the pinned kagi surface-census declaration that kills survivor B5, reduced by the counter's own ddmin to a committed 1-minimal fixture, plus an entry citing S024.
The L1 TameshiR29 holds the planner seat and is the sole integrator. You did not write the content you attack or read.
# Bounds (binding)
- Do exactly what your item names; verdict first, then evidence (path:line, exact commands with observed output), then the smallest safe correction.
- Write NOTHING except your own report file, trace receipts under {TR}/ (cold-read items only), and files under {E}/f6/<your-name>/ (F6 build items only). Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>, never at the fleet root.
- Never edit production files. Never run git write commands (add/commit/checkout/reset/stash/push/fetch/pull) in {LANE}. Never run ANY `jj` command anywhere —
  not at the fleet root {FLEET} (never), not in {LANE}, not in a clone: any jj command snapshots a colocated working copy.
  Never touch the fleet repo {FLEET}, sibling lanes, lane jj state or the lane Git index. Read-only git with GIT_OPTIONAL_LOCKS=0 is fine. Sibling repos are read-only.
- Code runs only inside your own /tmp (or /fast/scratch/hyaku) clone or scratch dir, with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset. Never run gates, selftests or sweeps in {LANE} itself. Wrap long runs in `timeout`; kill any process tree you started before you return.
- No seat spawns, except an executor may spawn one read-only labrat probe for a falsifiable hypothesis.
- Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool, version, channel and reason in your report). Pacman guard: all pacman transactions are PAUSED host-wide; install via uv tool, npx or an official binary in ~/.local/bin, or file an L0 question; never -Sy/-Syu/-U/-R, never restart a host service.
- Time box: finish and write your report within 20 minutes; a partial honest report beats none. Never pass a model.
- Sourcing rule: open sources by ordinary means only. Never use a headless browser or any other tool to pass a bot challenge, captcha or access control. Record a source you cannot open that way as unopened.
- Write plain English, no run-together words. No producer-authentication, promotion or numeric-score claims."""

items = []


def add(name, role, axes, target, acceptance=None):
    acceptance = acceptance or f'Report: {W}/{name}.md'
    prompt = '/skill:godspeed\n' + DIRECTIVE + '\n# Target\n' + target + '\n\n# Acceptance\n' + acceptance + '\n'
    items.append({'name': name, 'role': role, 'axes': axes, 'prompt': prompt})


RECIPE = f"""Independent cold read of ONE SKILL.md section at lane revision {REV} (SKILL.md sha256 {SKILL_SHA}). Claim served: C1 (calibration repair).
Section: start line {{start}}, heading exactly {{heading!r}}. It runs to the line before the next #/##/### heading outside ``` fences.
Steps:
1. Fleet-mirror clone: `{FLEET_CLONE}`.
2. Read the section in $R/SKILL.md. Decide its class: `instruction` (it tells a reader to run something) or `record` (it states facts with pointers).
3. Open what the section cites, under the trace collector, from inside $R:
   `cd $R && python3 tools/trace-inputs.py --root $R --out {TR}/<your-name>-<n>.json -- <argv>` — for a record, a reader such as
   `python3 -c "import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]" <cited lane paths>`; for an instruction, run at least one command it names
   (skip any that needs more than 6 minutes and say so). Check each claim you can against what you opened. Never read the live lane {LANE} during traces.
   EXCEPTION — four lane files are appended by the L1 after your read: {', '.join(APPENDED)}. Never open them under the trace collector or by path.
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
    for who in ('A', 'B', 'C'):
        name = 'Read%02d%s' % (k, who)
        body = RECIPE.format(start=m['start'], heading=m['heading'], heading_json=json.dumps(m['heading'])) + f"\nMonitor reason for this section at {REV}: {m['reason']}."
        if who != 'A':
            body = ('You are an additional, independent reader of this section; other seats read it too and you never see their reports. '
                    'Attack it: a wrong or unverifiable statement is a failing verdict.\n') + body
        add(name, 'reviewer', ['calibration'], body,
            f'Report: {W}/{name}.md, with exactly one ```json block as above. Last line exactly `COLDREAD {name}: <verdict>`.')


C2CTR = f'`python3 .ufo/evidence/round-29/c2-measure-v2.py --repo <clone> --rev HEAD`'
F6 = f'{E}/f6/<your-name>'
B5DOC = f'{LANE}/corpus/knowledge/mutation-case-kagi-census.md (sections 2 and the B5 paragraph near lines 105-120, recipe near lines 225-260), kaika receipts {LANE}/.ufo/evidence/kaika-round-1/coldread/B-probe-B5-pristine.txt and B-probe-B5-mutant.txt'
KREV = 'fecee8743e52eb8fb5fbb40782934cb619a1a96e'
for who in ('A', 'B'):
    add(f'BuildF6{who}', 'executor', ['coverage'],
        f'Claim C2 (frontier F6), independent builder {who} (another seat builds the same thing; you never see its work). Work in your own clone at {FROZEN} (`git clone -q --no-hardlinks {LANE} /tmp/<your-name>-r29 && git -C /tmp/<your-name>-r29 checkout -q --detach {FROZEN}`). '
        f'(1) Read the frozen counter `.ufo/evidence/round-29/c2-measure-v2.py` (docstring, `materialize()`, `Oracle.kills()`, `ddmin()`) and the amended predicate in `.ufo/evidence/round-29/contract-amendment-1.json`. Fixture layout: census.tsv, shapes.tsv, baseline.tsv and the manifest host.tsv (`<relative path>\\t<dir|file>\\t<octal mode>\\t<content>`; the gate maps `$HOME` to the root and `$STATE` to `<root>/.local/state/the-janitor`). '
        f'(2) Build the ORIGINAL fixture: census.tsv byte-identical to `git -C {FLEET}/kagi-shokunin show {KREV}:corpus/surface-census.tsv` (read-only; every line, comments and `# scan` lines included); shapes.tsv and baseline.tsv any subset of the lines of the pinned `corpus/state-shape.tsv` / `corpus/drift-baseline.tsv` (empty is allowed); host.tsv a manifest that makes the pinned gate `git -C {FLEET}/kagi-shokunin show {KREV}:corpus/surface-census.sh` report drift ONLY for one `exec` row whose file lacks the execute bit, so the B5 mutant (exec x-bit arm deleted, see {B5DOC}) exits 0. Iterate by running both gates in /tmp until `Oracle.kills()` on your original is true. A generator script is the cheap way. Save original/ (four files) and your generator under {F6}/. '
        f'(3) Reduce: run the counter\'s own `ddmin()` with `Oracle.kills()` (import them from the counter file; do not reimplement) on the original\'s units and write the result as {F6}/minimized/ (four files, lines in the order ddmin returns them per file). Record the number of oracle tests. '
        f'(4) Verify: in your clone copy original/ and minimized/ to `.ufo/evidence/round-29/f6/`, commit in the clone (`git -c user.name=b -c user.email=b@x commit`), run {C2CTR} under `timeout 1800`; paste stdout and exit. entry_sourced and quote_located will read 0 (the L1 lands those); report every fixture field. '
        f'Report units before and after, tests run, wall time, and the four files of minimized/ verbatim.')
add('ScribeEntryF6', 'scribe', ['coverage'],
    f'Claim C2. Draft, in your report only, the knowledge entry `corpus/knowledge/survivor-fixture-minimization.md` (the L1 writes the final file): first line `# Survivor fixture minimization — B5 probe, delta debugging`, then a line `source: S024 (https://www.fuzzingbook.org/html/Reducer.html, re-opened 2026-10-23)`. '
    f'Content: what F6 asks ({LANE}/corpus/README.md `## Frontier` row F6 and the Round-29 section at {REV}), what S024 teaches (open the snapshot {LANE}/.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html; quote at most 25 words verbatim, e.g. on 1-minimal), how the B5 survivor arises ({B5DOC}), the method as the frozen counter `{LANE}/.ufo/evidence/round-29/c2-measure-v2.py` defines it (original anchored on the pinned declaration, `Oracle.kills()`, `ddmin()`, the host manifest), the unit granularity bound (lines, not bytes), and the validity risk (a reduction that keeps the outcome for a different reason; how the oracle guards it). Mark every number the builders have not produced yet as `<from BuildF6A/B>`; never invent results. Plain English, under 90 lines.')
add('ReopenS024', 'reviewer', ['coverage'],
    f'Frontier step. Re-open S024 https://www.fuzzingbook.org/html/Reducer.html by ordinary means (curl). Compare with the L1 snapshot {LANE}/.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html (sha256 3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99): same bytes or not; if not, is the text the same after stripping tags? '
    f'Is the quote "Its result is 1-minimal, meaning that every character contained is required to produce the error" verbatim (after tag stripping and whitespace normalization), and under which section? Check row S024 at {REV} (`git -C {LANE} show {REV}:corpus/SOURCES.md`, compare with {BASE}): only status and used-by may change in place (contract: {FLEET}/CORPUS.md section "SOURCES.md — where a shokunin learns"). Is tier B and kind `book` right for this page? Agree or disagree with reasons.')
add('ReopenS059', 'reviewer', ['freshness'],
    f'Routed item 2 of {LANE}/corpus/lessons/round-28-verifier-spotcheck.md: S059 pinned digests no longer reproduce. Fetch https://bazel.build/remote/caching three times with `curl -sL` about 30 s apart and the markdown alternate (find its URL in row S059 of `git -C {LANE} show {REV}:corpus/SOURCES.md` or the page head); sha256 each. '
    f'Do the HTML bytes differ between fetches seconds apart (non-deterministic) or are they stable but different from the recorded values (`9e3a2ebb…` HTML, `0d362d11…` markdown)? If they differ, show what differs (diff of the varying region, a few lines). Verdict: non-deterministic HTML / content drift / stable. Is a supersedes row needed or is a recorded note enough under the SOURCES contract?')
add('RegistryNoHarm', 'executor', ['operability'],
    f'No-harm check of the gate/probe registry at {REV}. In a fleet mirror: `{FLEET_CLONE}`, then `cd $R && timeout 900 python3 tools/registry-check.py --rev {REV}` (read its --help if flags differ). Paste the summary line and every row that is not held, with its exit. Do the same at base {BASE}. Compare row by row and name any row whose result differs and why.')
add('RerunCensusA', 'executor', ['coverage'],
    f'Frontier step. Run the SOURCES census at {REV} in a mirror: `W2=$(mktemp -d); cp {FLEET}/shokunin.conf $W2/; ln -s {FLEET}/scripts $W2/scripts; git clone -q --no-hardlinks {LANE} $W2/tameshi-shokunin; git -C $W2/tameshi-shokunin checkout -q --detach {REV}; {FLEET}/scripts/sources-census.sh validate --root $W2 tameshi`; paste output and exit; repeat at {BASE}. '
    f'Then `git -C {LANE} diff {BASE} {REV} -- corpus/SOURCES.md`: confirm only the S024 status and used-by cells changed. Note whether the census checks that a used-by path exists (the entry lands after {REV}).')
add('MutateLegSum', 'mutation-tester', ['operability'],
    f'Routed item 6 of {LANE}/corpus/lessons/round-27-verifier-spotcheck.md (round-26 item 5): `tools/mutate-and-run.sh --regression` does not check npass + nfail + nsetup == nlegs (lines near 1430-1452 at {REV}). In your own clone at {REV}, make the mutant that drops one `"$st_x"` from the tally loop; WITHOUT running the full regression (too long), show by a minimal harness (extract the tally block into a small bash script fed fixed statuses) that the mutant prints `REGRESSION: PASS (cases=9 passed=8 …)` with exit 0. '
    f'Then check whether `--selftest` (`timeout 900 bash tools/mutate-and-run.sh --selftest` in the clone) kills that mutant (it has a leg-count agreement check near line 1938). Report: does the defect exist, does any existing check catch it, and the smallest fix as a unified diff in your report only (never applied).')
add('ConnectorOverlap', 'connector', ['adjacency'],
    f'Sibling-overlap scan for frontier F6 (fixture minimization: delta debugging, test-case reduction, shrinking, 1-minimal fixtures) and for survivor-probe fixtures. Search sibling lanes under {FLEET}/*-shokunin (read-only; never tameshi) for reducers, shrinkers, minimal-fixture rules or lessons. Report overlaps with path:line and whether tameshi absorbs anything (report-only).')
add('ScoutF6Next', 'scout', ['coverage'],
    f'Planning data walk (the L1 holds the planner seat; this rides a scout). From the nine recorded legs (header of `git -C {LANE} show {REV}:tools/mutate-and-run.sh` lines 84-100 and corpus/knowledge/mutation-case-*.md), list every survivor whose kill needs a fixture the suite lacks (the fixture-absent class, like B5), with its leg, pin and the knowledge-note line. Rank them as next F6 moves by expected fixture size. Table only, with path:line.')
add('ScribeMistakes', 'scribe', ['calibration'],
    f'Draft, in your report only, candidate `## Mistakes` rows for corpus/lessons/round-29.md, format: class · evidence pointer · captured-by (criterion or rule, or `none`) · fix, where a fix counts only once shown able to fail. Mine {LANE}/corpus/lessons/round-28-verifier-spotcheck.md (routed items 1-4, the post-closure landing of 41da22a3 and 1dde85f3 and the report rewrite 2012146 → 38ae0ff) and round-27-verifier-spotcheck.md. '
    f'For each, name the QUALITY.md criterion at {REV} (`git -C {LANE} show {REV}:corpus/QUALITY.md`, new criteria 55-57) that captures it or `none`, and give one command whose output shows the check failing on the old state.')
add('ReviewR1Edits', 'reviewer', ['quality'],
    f'Review the widely read edits of commit {REV} (`git -C {LANE} diff {BASE} {REV} -- corpus/QUALITY.md corpus/README.md corpus/SOURCES.md`). Check each statement in QUALITY 55-57 and the README Round-29 section against bytes: the cited lessons and spot-checks (path:line), {LANE}/.ufo/waves/round-27/w1/ReviewQuality.md H1/M1/M2/L2, {LANE}/.ufo/evidence/round-28/append-probe.txt, the round-28 heads named in criterion 57, and the F8 bound in {LANE}/corpus/knowledge/oracle-anchored-survivors.md. List each mismatch with path:line. These files cannot be corrected this round without drifting cold-read credit, so state whether a mismatch is wrong or only imprecise.')
add('CriticRound', 'critic', ['calibration', 'coverage'],
    f'Attack the round shape. The session note says: repair first (route every defect in {LANE}/corpus/lessons/round-28-verifier-spotcheck.md before new claims); work a different frontier area or axis than the rejected calibration streak (rounds 26-28); a fourth rejection on the same cause re-blocks the lane. Round 29 claims C1 calibration repair (the routed item 1) and C2 coverage on frontier F6 (never worked before). '
    f'(1) Does C1 risk the same cause as rounds 27-28 (missed 64/64), and what in the plan (three readers per section, all input edits in {REV}, binding check) changes the odds? (2) Is C2 a different frontier area, sourced, and does its counter fail every cheap control? Read {LANE}/.ufo/evidence/round-29/contract.json and the control reports under {LANE}/.ufo/waves/round-29/ctl/ if present. (3) Which routed items 1-4 of the round-28 spot-check are not routed by the plan? Evidence, not opinion.')

spec = {'wave': 'round-29-w1', 'reportDir': W, 'context': CONTEXT, 'items': items}
out = Path(LANE + '/.ufo/waves/round-29/spec-w1.json')
out.write_text(json.dumps(spec, indent=1) + '\n')
print(len(items), 'items for', len(missing), 'sections ->', out)
