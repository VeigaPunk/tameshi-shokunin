#!/usr/bin/env python3
"""Round 30 attempt 3 (L1 TameshiR30A3): adapted from attempt 2's make-spec-wB.py. Wave B was registered but
never spawned (no seat transcript; .ufo/evidence/round-30/attempt3/inherited-removed.txt), so wave C is a new
dispatch with new seat names, binding v3 (.ufo/evidence/round-30/coldread/bind-select-v3.py, trace names bound to
executed tool calls) and four added items (connector, scribe, binding attack, routed-defect review).
Generate wave C: two independent cold reads of every section the content revision drifts (three sections per
reader seat, two disjoint groupings), plus C1 falsifiers, no-harm executors and the frontier checks.

Usage: make-spec-wC.py REV MONITOR_JSON FROZEN
REV is the round's content revision (it carries every widely read input edit of
the round); MONITOR_JSON is the strict round-21 monitor output at REV; FROZEN is
the lane commit that holds the final C1 counter and every control receipt.
Adapted from round-29 make-spec-w1.py (one section per seat, three readers).
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
REV, MON, FROZEN = sys.argv[1], sys.argv[2], sys.argv[3]
BASE = '9ed6db840dc97a0a5f4758b6b5f60cee83a61645'
E = LANE + '/.ufo/evidence/round-30'
TR = E + '/coldread/traces'
W = '.ufo/waves/round-30/wC'
DIRECTIVE = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text()
skill = subprocess.run(['git', '-C', LANE, 'show', REV + ':SKILL.md'], capture_output=True, check=True).stdout
SKILL_SHA = hashlib.sha256(skill).hexdigest()
monitor = json.loads(Path(MON).read_text())
assert monitor['revision'] == REV and monitor['trace_gate'] == 'strict' and not monitor['overrides_used']
missing = monitor['coldread']['missing']
APPENDED = ['SCORECARD.md', 'LOG.md', '.ufo/evidence/round-21/coldread/ledger.json', 'corpus/lessons/round-30.md']
C1CTR = 'python3 .ufo/evidence/round-30/c1-measure-v4.py --repo <clone> --rev ' + REV + ' --sealed ' + E + '/v4/c1-sealed.json'

FLEET_CLONE = (f'W=$(mktemp -d /tmp/<your-name>-XXXX); mkdir $W/fleet; for d in {FLEET}/*-shokunin; do b=$(basename $d); '
               f'[ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done; env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks {LANE} $W/fleet/tameshi-shokunin; '
               f'git -C $W/fleet/tameshi-shokunin checkout -q --detach {REV}; R=$W/fleet/tameshi-shokunin')

CONTEXT = f"""# Goal
Tameshi round 30 (verification-fixture craft), attempt 3, wave C (cold reads + falsifiers, policy v1). One claim, C1, EXPLORATORY
(operability; surface = the `--regression` case tally of {LANE}/tools/mutate-and-run.sh and its `--selftest` detector; routed item 7 of
{LANE}/corpus/lessons/round-29-verifier-spotcheck.md; sourced on S087, S093, S094). It was declared exploratory before data after control CtlS2SymEval
met the frozen counter v4 ({E}/contract-amendment-4.json); the v4 counter `{C1CTR}` is supporting evidence only. Every control receipt is committed at lane commit {FROZEN} or earlier.
The content revision {REV} carries every widely read input edit of the round (the runner fix, corpus/SOURCES.md S092-S094 rows and S087 used-by,
corpus/QUALITY.md 58-65, corpus/README.md Round-30 section, corpus/knowledge/regression-tally-completeness.md). Those edits drift the lane's
cold-read credit (strict monitor at {REV}: {monitor['coldread']['sections_covered']}/{monitor['coldread']['sections_total']}). No-harm duty: each drifted section gets two independent fresh cold reads in this wave,
at {REV}, by two disjoint reader sets (A and B group the sections differently). A failing read is a valid result and is recorded as it is.
The L1 TameshiR30A3 holds the planner seat and is the sole integrator. You did not write the content you attack or read.
# Bounds (binding)
- Do exactly what your item names; verdict first, then evidence (path:line, exact commands with observed output), then the smallest safe correction.
- Your `seat` value in any JSON is exactly your item name (e.g. `ColdA03`), never an agent id or a prefixed label.
- Write NOTHING except your own report file and, for cold-read items only, trace receipts under {TR}/. Never open anything under /fast/scratch/hyaku/tameshi-r30a3/ or /fast/scratch/hyaku/tameshi-r30a2/. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>, never at the fleet root {FLEET}.
- Never edit production files. Never run git write commands (add/commit/checkout/reset/stash/push/fetch/pull) in {LANE} or {FLEET}. Never run ANY `jj` command anywhere —
  not at the fleet root, not in {LANE}, not in a clone: any jj command snapshots a colocated working copy.
  Never touch the fleet repo {FLEET}, sibling lanes, lane jj state or the lane Git index. Read-only git with GIT_OPTIONAL_LOCKS=0 is fine. Sibling repos are read-only.
- Code runs only inside your own /tmp (or /fast/scratch/hyaku) clone or scratch dir, with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset. Never run gates, selftests or sweeps in {LANE} itself. Wrap long runs in `timeout`; kill any process tree you started before you return.
- Never kill a process you did not start: before any kill, check that /proc/<pid>/cwd is inside your own scratch dir. Other seats run the same tools at the same time.
- No seat spawns, except an executor may spawn one read-only labrat probe for a falsifiable hypothesis.
- Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool, version, channel and reason in your report). Pacman guard: all pacman transactions are PAUSED host-wide; install via uv tool, npx or an official binary in ~/.local/bin, or file an L0 question; never -Sy/-Syu/-U/-R, never restart a host service.
- Time box: cold-read items 45 minutes, others 30 minutes; a partial honest report beats none. Never pass a model.
- Disk: bound every file you write (no unbounded loops or appends); never point a marker or log at a file Python imports (sitecustomize.py, *.pth); check `df -h /fast` before large builds. Never run du/find over /fast/scratch.
- Sourcing rule: open sources by ordinary means only. Never use a headless browser or any other tool to pass a bot challenge, captcha or access control.
- Write plain English, no run-together words. No producer-authentication, promotion or numeric-score claims."""

items = []


def add(name, role, axes, target, acceptance=None):
    acceptance = acceptance or f'Report: {W}/{name}.md'
    prompt = '/skill:godspeed\n' + DIRECTIVE + '\n# Target\n' + target + '\n\n# Acceptance\n' + acceptance + '\n'
    items.append({'name': name, 'role': role, 'axes': axes, 'prompt': prompt})


RECIPE = f"""Independent cold reads of {{n}} SKILL.md sections at lane revision {REV} (SKILL.md sha256 {SKILL_SHA}). Duty served: calibration no-harm (cold-read credit).
Sections (each runs to the line before the next #/##/### heading outside ``` fences):
{{listing}}
Steps, for EACH section:
1. Fleet-mirror clone (once): `{FLEET_CLONE}`.
2. Read the section in $R/SKILL.md. Decide its class: `instruction` (it tells a reader to run something) or `record` (it states facts with pointers).
3. Open what the section cites, under the trace collector, from inside $R:
   `cd $R && python3 tools/trace-inputs.py --root $R --out {TR}/<your-name>-<section number>-<k>.json -- <argv>` — for a record, a reader such as
   `python3 -c "import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]" <cited lane paths>`; for an instruction, run at least one command it names
   (skip any that needs more than 6 minutes and say so). Check each claim you can against what you opened. Never read the live lane {LANE} during traces.
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
   Use a distinct trace file name per command (<your-name>-<section number>-<k>.json); a section's `traces` lists only its own receipts.
   BINDING (frozen, {LANE}/.ufo/evidence/round-30/coldread/bind-select-v3.py): `<your-name>` is your item name exactly (case as given, no prefix), and each trace file
   name must appear LITERALLY in the bash command that runs tools/trace-inputs.py (no loop variable or glob builds the name; one command per trace). A trace whose
   name is not in such an executed command is not credited.
Credit rules the assembler and monitor enforce (tested end to end in round 26, {LANE}/.ufo/waves/round-26/w1/ColdreadPilot.md, sections "Class/verdict pairing" and "Pitfalls"):
class `instruction` needs verdict `executed-ok` or `gap-minor`; class `record` needs `verified-record` or `gap-minor`; EVERY section needs at least one command run under the
trace collector with its receipt listed in `traces` (a record read counts). Receipt `rev` must equal `read_rev` (keep the clone detached at {REV}). `skill_sha256` is the whole page's sha256 (given above).
Input digests are full 64-hex sha256 values. Sibling reads made with `git show` do not appear in receipts: record them in `external_inputs` as `<repo>@<40-hex rev>:<path>` with the sha256 of the bytes; never put a URL there. Line numbers belong to {REV} only.
If time runs short, report the sections you finished; an unread section is simply absent from your JSON.
Then, below the JSON, a short plain-English note of what you checked."""

n = len(missing)
groups = {'A': [list(range(k, min(k + 3, n))) for k in range(0, n, 3)],
          'B': [[(k + d) % n for d in range(3) if d < n] for k in range(1, n + 1, 3)]}
for who, gs in groups.items():
    for g, idxs in enumerate(gs, 1):
        idxs = sorted(set(idxs))
        listing = '\n'.join(f'- section {i + 1}: start line {missing[i]["start"]}, heading exactly {json.dumps(missing[i]["heading"], ensure_ascii=False)}'
                            f' (monitor reason at {REV}: {missing[i]["reason"]})' for i in idxs)
        name = 'Cold%s%02d' % (who, g)
        body = RECIPE.format(n=len(idxs), listing=listing)
        if who == 'B':
            body = ('You are an independent reader; other seats read these sections too and you never see their reports. '
                    'Attack each section: a wrong or unverifiable statement is a failing verdict.\n') + body
        add(name, 'reviewer', ['calibration'], body,
            f'Report: {W}/{name}.md, with exactly one ```json block as above. Last line exactly `COLDREAD {name}: <verdict of each section, comma separated>`.')


MUT = f'In your own clone at {REV} (`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks {LANE} /fast/scratch/hyaku/tameshi-r30a3-seats/<your-name>/c && git -C /fast/scratch/hyaku/tameshi-r30a3-seats/<your-name>/c checkout -q --detach {REV}`)'
CL = '/fast/scratch/hyaku/tameshi-r30a3-seats/<your-name>/c'
add('RerunC1Head', 'executor', ['operability'],
    f'C1 supporting evidence, independent re-run. {MUT}, check `sha256sum {E}/v4/c1-sealed.json` equals sealed_sha256 in {E}/contract-amendment-3.json and `sha256sum {E}/c1-measure-v4.py` equals counter_sha256, then run `timeout 1500 {C1CTR.replace("<clone>", CL)} --jobs 4` and paste the summary, the PREDICATE line and the exit. Compare with {E}/v4/head.stdout. Do NOT print or quote the sealed items. Verdict: does the receipt reproduce?')
add('MutateHead', 'mutation-tester', ['operability'],
    f'Attack the landed selftest at {REV}. {MUT}. Make at least 8 hand-made mutants of the tally block, the guard, and the new selftest cases (vectors, guard stress, tally_line) that no counter family makes, including the wave-A survivors in {LANE}/.ufo/waves/round-30/wA/MutateTallyExtra.md and {LANE}/.ufo/waves/round-30/wA/MutateSelftestHarness.md. For each run `timeout 300 bash tools/mutate-and-run.sh --selftest`; restore exact bytes after each (sha256). Table: mutant, killed or survived; each survivor equivalent or a real gap.')
add('JudgeC1', 'reviewer', ['operability'],
    f'You are the named non-author judge of the exploratory claim C1 (contract {E}/contract-amendment-4.json `exploratory_claim`). Read the change `git -C {LANE} diff 9ed6db840dc97a0a5f4758b6b5f60cee83a61645 {REV} -- tools/mutate-and-run.sh`, the entry {LANE}/corpus/knowledge/regression-tally-completeness.md, the base defect {LANE}/.ufo/waves/round-29/w1/MutateLegSum.md, and run in your clone ({MUT}) `timeout 300 bash tools/mutate-and-run.sh --selftest` and one dropped-operand mutant of the tally loop. '
    f'Decide: is the runner at {REV} better than at base on the named surface (a tally that silently passes with a leg uncounted), with no harm to its other behavior? First line of your report exactly `JUDGE C1: unprovable-but-better` or `JUDGE C1: unprovable` or `JUDGE C1: harmed`, then your reasons with evidence.')
add('CriticC1Exploratory', 'critic', ['operability'],
    f'Adversarial review of the exploratory declaration. Read {E}/contract-amendment-4.json, -3.json and the control receipts {E}/v4/ctl2/. (1) Was C1 declared exploratory BEFORE the content revision {REV} (`git -C {LANE} log --format="%h %cI %s" 9ed6db840dc97a0a5f4758b6b5f60cee83a61645..{REV}`)? (2) Did the runner change after the declaration (5 selftest cases) change the judged object after judgment, or before any judgment? (3) Is CtlS2SymEval really a control that skips the work, or a different implementation of it? (4) Does the round report the v4 head receipt only as supporting evidence? Verdict first per question.')
add('ReviewEntry', 'reviewer', ['quality'],
    f'Review {LANE}/corpus/knowledge/regression-tally-completeness.md at {REV} against bytes: every claim about the runner (`git -C {LANE} show {REV}:tools/mutate-and-run.sh`), the counters and amendments under {E}/, the controls ({E}/ctl/, {E}/v4/), the wave-A reports under {LANE}/.ufo/waves/round-30/wA/, and sources S087, S093, S094 (rows in `git -C {LANE} show {REV}:corpus/SOURCES.md`). List each wrong or imprecise statement with path:line; say whether the entry overclaims.')
add('ReviewQualityR30', 'reviewer', ['quality'],
    f'Review criteria 58-65 at {REV} (`git -C {LANE} diff 9ed6db840dc97a0a5f4758b6b5f60cee83a61645 {REV} -- corpus/QUALITY.md corpus/README.md`). Check every Falsifier pointer resolves at {REV} (`git -C {LANE} cat-file -e {REV}:<path>`) and says what the criterion claims; check each criterion routes the item it names in {LANE}/corpus/lessons/round-29-verifier-spotcheck.md. List mismatches with path:line.')
add('RerunCensus', 'executor', ['coverage'],
    f'Frontier step. Run the SOURCES census at {REV} in a mirror: `W2=/fast/scratch/hyaku/tameshi-r30a2-seats/<your-name>/m; mkdir -p $W2; cp {FLEET}/shokunin.conf $W2/ 2>/dev/null; ln -s {FLEET}/scripts $W2/scripts; env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks {LANE} $W2/tameshi-shokunin; git -C $W2/tameshi-shokunin checkout -q --detach {REV}; {FLEET}/scripts/sources-census.sh validate --root $W2 tameshi`; paste output and exit; repeat at base 9ed6db840dc97a0a5f4758b6b5f60cee83a61645. '
    f'Then `git -C {LANE} diff 9ed6db840dc97a0a5f4758b6b5f60cee83a61645 {REV} -- corpus/SOURCES.md`: confirm only the S087 used-by cell changed in place, rows S092-S094 and notes were appended, and every used-by path of a mined row exists at {REV}.')
add('ReopenS092', 'scout', ['freshness'],
    f'Frontier step. Re-open `curl -sSL https://bazel.build/remote/caching.md`; sha256; compare with row S092 (`git -C {LANE} show {REV}:corpus/SOURCES.md`). Is the quoted known issue present at the cited lines? Does S092 follow the contract in {FLEET}/CORPUS.md section "SOURCES.md — where a shokunin learns" (append-only; a correction is a new row whose teaches opens `supersedes S0NN —`; status/used-by consistent)? Agree or disagree with reasons.')
add('ReopenS093S094', 'scout', ['coverage'],
    f'Frontier step. Re-open S093 (`curl -sSL https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml | sha256sum`, then quote line 159) and S094 (`curl -sSL -A Mozilla/5.0 https://arxiv.org/pdf/1411.2664v3`, sha256, locate "available only to the organizers") and compare with rows S093/S094 at {REV} and snapshots {E}/sources/. Does the knowledge entry {LANE}/corpus/knowledge/regression-tally-completeness.md use each source faithfully (no overreach)? Agree or disagree with reasons.')
add('RegressionReplayHead', 'executor', ['operability'],
    f'No-harm, operability: the full ledger replay must pass at {REV}. Fleet mirror: `{FLEET_CLONE}`, then `cd $R && timeout 2400 bash tools/mutate-and-run.sh --regression --workdir $W/rg` and paste the REGRESSION_* lines and exit. Expected `REGRESSION: PASS (cases=9 passed=9 ...)`, exit 0; report what you observe.')
add('SelftestsNoHarmHead', 'executor', ['operability'],
    f'No-harm: at {REV} and at base 9ed6db840dc97a0a5f4758b6b5f60cee83a61645, each in its own clone, run `timeout 600 bash tools/mutate-and-run.sh --selftest` and `timeout 600 python3 tools/<x>.py --selftest` for each tools/*.py that accepts --selftest. Table: tool, exit at base, exit at {REV}, summary line. Name every difference and its cause.')
add('CriticNoHarm', 'critic', ['calibration'],
    f'No-harm review across axes: `git -C {LANE} diff --stat 9ed6db840dc97a0a5f4758b6b5f60cee83a61645 {REV} -- . ":!.ufo"`. For each axis in {LANE}/SCORECARD.md (calibration, coverage, depth, operability, freshness, adjacency), name what this round touched and whether any committed number could drop: depth command D at {REV} (SCORECARD.md `# D:` line), the SHONEN boxes, the cold-read credit (strict monitor at {REV} is 33/64 before this wave\'s reads; {E}/head/c1monitor-at-bb681566.stdout; the L1 appends this wave\'s bound reads to the ledger afterwards). Verdict per axis.')

add('ConnectorOverlap', 'connector', ['adjacency'],
    f'Sibling-overlap scan (read-only). Sibling lanes are {FLEET}/*-shokunin (never write there). Find where sibling lanes hold (1) a case/leg tally or summary line that could pass with an uncounted leg (compare {LANE}/corpus/knowledge/regression-tally-completeness.md and `git -C {LANE} diff 9ed6db840dc97a0a5f4758b6b5f60cee83a61645 {REV} -- tools/mutate-and-run.sh`), and (2) a seat-work binding for credited reads or reviews (compare {LANE}/.ufo/evidence/round-30/coldread/bind-select-v3.py). Use `git -C <sibling> grep` on each sibling HEAD. Table: sibling, path:line, overlap, whether tameshi duplicates, conflicts with or could serve it. Verdict first.')
add('ScribeMistakes30', 'scribe', ['quality'],
    f'Draft the `## Mistakes` rows for round 30 (format per {FLEET}/CORPUS.md and {LANE}/corpus/lessons/round-29.md `## Mistakes`: class · evidence pointer · captured-by (the criterion or rule that should have caught it, or `none`) · fix, where a fix counts only once shown able to fail). Sources, all committed or in this lane: the four C1 counter amendments {E}/contract-amendment-1.json to -4.json (each re-design forced by a control: K7, K8, CtlS2SymEval), {E}/attempt3/bind-controls.txt (binding v2 met by a do-nothing transcript, 32/32), {E}/attempt3/inherited-removed.txt (attempt-2 wave B registered but never spawned). One row per distinct mistake class, each with a path:line pointer you opened. Write only your report; the L1 integrates.')
add('CtlBindV3', 'mutation-tester', ['calibration'],
    f'Attack the frozen cold-read binding {LANE}/.ufo/evidence/round-30/coldread/bind-select-v3.py (read its docstring). In your own scratch dir under /fast/scratch/hyaku/tameshi-r30a3-seats/<your-name>/ (clone the lane there at {FROZEN}), run {E}/attempt3/make-bind-controls.py to rebuild the five synthetic controls, re-score them (compare {E}/attempt3/bind-controls.txt), then build at least four NEW transcript shapes in which no trace-inputs.py command really ran (for example: the trace name in a tool call to a different tool, a tool result for a different call id, a call in a user message, a call whose result is an error, a transcript of another seat renamed) and score each with v3 on the round-29 pilot assembly (`--assembled .ufo/evidence/round-29/coldread/assembled-w1.json --registry .ufo/waves/round-29/w1/swarm-registry.json --prefix TameshiR29.`). Table: shape, kept/32, exit. Any shape other than a hand-forged call+result pair that keeps entries is a finding: give the exact transcript lines. Write only under your scratch dir and your report.')
add('ReviewRoutedR29', 'reviewer', ['quality'],
    f'For each routed defect 1-7 in {LANE}/corpus/lessons/round-29-verifier-spotcheck.md (section "Routed defects"), find its disposition in committed lane bytes at {FROZEN} (`git -C {LANE} show {FROZEN}:<path>`; candidates: corpus/QUALITY.md criteria 58-65, {E}/contract.json hold_rule, {E}/coldread/bind-select-v3.py, {E}/r29-mistake1-ordering.txt, corpus/SOURCES.md S092, tools/mutate-and-run.sh, the wave contexts in {LANE}/.ufo/waves/round-30/spec-*.json). Table: defect, disposition path:line, resolved / partial / open, reason. Verdict first.')

spec = {'wave': 'round-30-wC', 'reportDir': W, 'context': CONTEXT, 'items': items}
out = Path(LANE + '/.ufo/waves/round-30/spec-wC.json')
out.write_text(json.dumps(spec, indent=1) + '\n')
print(len(items), 'items for', n, 'sections ->', out)
