#!/usr/bin/env python3
"""Generate the round-30 wave 1: two independent cold reads of every section the
content revision drifts (three sections per reader seat, two disjoint groupings),
plus C1 falsifiers, no-harm executors and the frontier checks.

Usage: make-spec-w1.py REV MONITOR_JSON FROZEN
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
W = '.ufo/waves/round-30/w1'
DIRECTIVE = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text()
skill = subprocess.run(['git', '-C', LANE, 'show', REV + ':SKILL.md'], capture_output=True, check=True).stdout
SKILL_SHA = hashlib.sha256(skill).hexdigest()
monitor = json.loads(Path(MON).read_text())
assert monitor['revision'] == REV and monitor['trace_gate'] == 'strict' and not monitor['overrides_used']
missing = monitor['coldread']['missing']
APPENDED = ['SCORECARD.md', 'LOG.md', '.ufo/evidence/round-21/coldread/ledger.json', 'corpus/lessons/round-30.md']
C1CTR = 'python3 .ufo/evidence/round-30/c1-measure-v3.py --repo <clone> --rev ' + REV

FLEET_CLONE = (f'W=$(mktemp -d /tmp/<your-name>-XXXX); mkdir $W/fleet; for d in {FLEET}/*-shokunin; do b=$(basename $d); '
               f'[ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done; env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks {LANE} $W/fleet/tameshi-shokunin; '
               f'git -C $W/fleet/tameshi-shokunin checkout -q --detach {REV}; R=$W/fleet/tameshi-shokunin')

CONTEXT = f"""# Goal
Tameshi round 30 (verification-fixture craft), wave 1 (build + first falsifiers, policy v1). One measured claim, frozen before data:
C1 (operability; surface = the `--regression` case tally of {LANE}/tools/mutate-and-run.sh and its `--selftest` detector; routed item 7 of
{LANE}/corpus/lessons/round-29-verifier-spotcheck.md; sourced on S087). Counter `{C1CTR}` prints `PREDICATE: C1_R30_PASS=true|false`;
contract {E}/contract.json, amendments 1 and 2 (v3 counter, re-designed after control CtlK7Keyed met v2); every control receipt is committed at lane commit {FROZEN}.
The content revision {REV} carries every widely read input edit of the round (the runner fix, corpus/SOURCES.md S092 row and S087 used-by,
corpus/QUALITY.md 58-63, corpus/README.md Round-30 section, corpus/knowledge/regression-tally-completeness.md). Those edits drift the lane's
cold-read credit (strict monitor at {REV}: {monitor['coldread']['sections_covered']}/{monitor['coldread']['sections_total']}). No-harm duty: each drifted section gets two independent fresh cold reads in this wave,
at {REV}, by two disjoint reader sets (A and B group the sections differently). A failing read is a valid result and is recorded as it is.
The L1 TameshiR30 holds the planner seat and is the sole integrator. You did not write the content you attack or read.
# Bounds (binding)
- Do exactly what your item names; verdict first, then evidence (path:line, exact commands with observed output), then the smallest safe correction.
- Your `seat` value in any JSON is exactly your item name (e.g. `Read03A`), never an agent id or a prefixed label.
- Write NOTHING except your own report file and, for cold-read items only, trace receipts under {TR}/. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>, never at the fleet root {FLEET}.
- Never edit production files. Never run git write commands (add/commit/checkout/reset/stash/push/fetch/pull) in {LANE} or {FLEET}. Never run ANY `jj` command anywhere —
  not at the fleet root, not in {LANE}, not in a clone: any jj command snapshots a colocated working copy.
  Never touch the fleet repo {FLEET}, sibling lanes, lane jj state or the lane Git index. Read-only git with GIT_OPTIONAL_LOCKS=0 is fine. Sibling repos are read-only.
- Code runs only inside your own /tmp (or /fast/scratch/hyaku) clone or scratch dir, with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset. Never run gates, selftests or sweeps in {LANE} itself. Wrap long runs in `timeout`; kill any process tree you started before you return.
- Never kill a process you did not start: before any kill, check that /proc/<pid>/cwd is inside your own scratch dir. Other seats run the same tools at the same time.
- No seat spawns, except an executor may spawn one read-only labrat probe for a falsifiable hypothesis.
- Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool, version, channel and reason in your report). Pacman guard: all pacman transactions are PAUSED host-wide; install via uv tool, npx or an official binary in ~/.local/bin, or file an L0 question; never -Sy/-Syu/-U/-R, never restart a host service.
- Time box: cold-read items 45 minutes, others 30 minutes; a partial honest report beats none. Never pass a model.
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
   `cd $R && python3 tools/trace-inputs.py --root $R --out {TR}/<your-name>-<n>.json -- <argv>` — for a record, a reader such as
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
     "inputs": {{{{"<lane-relative path>": "<sha256 at {REV}>"}}}}, "external_inputs": {{{{}}}}, "traces": ["{TR}/<your-name>-<n>.json", ...]}}}}, ...]}}}}
   `inputs` = every lane file you opened for THAT section (the trace receipts' `inputs` plus any file read by hand), lane-relative, sha256 of the bytes at {REV}; never SKILL.md
   itself. `external_inputs` keys are absolute paths or repo@rev:path outside the lane, plus the `tameshi-shokunin@{REV}:<path>` form above. Every command you ran is in commands_executed and has a receipt in traces.
   Use a distinct trace file name per command (<your-name>-<section number>-<k>.json); a section's `traces` lists only its own receipts.
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
        name = 'Read%s%02d' % (who, g)
        body = RECIPE.format(n=len(idxs), listing=listing)
        if who == 'B':
            body = ('You are an independent reader; other seats read these sections too and you never see their reports. '
                    'Attack each section: a wrong or unverifiable statement is a failing verdict.\n') + body
        add(name, 'reviewer', ['calibration'], body,
            f'Report: {W}/{name}.md, with exactly one ```json block as above. Last line exactly `COLDREAD {name}: <verdict of each section, comma separated>`.')

MUT = f'In your own clone at {REV} (`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks {LANE} /tmp/<your-name>-r30 && git -C /tmp/<your-name>-r30 checkout -q --detach {REV}`)'
add('RerunC1R1', 'executor', ['operability'],
    f'Claim C1, first re-run. {MUT}, run `timeout 1200 {C1CTR.replace("<clone>", "/tmp/<your-name>-r30")}` and paste the complete stdout and the exit code. '
    f'Check the counter file equals the frozen digest (`sha256sum .ufo/evidence/round-30/c1-measure-v3.py` vs counter_sha256 in .ufo/evidence/round-30/contract-amendment-2.json). Then run it once more at base {BASE} and compare. Verdict: does `C1_R30_PASS=true` reproduce at {REV}?')
add('MutateTallyExtra', 'mutation-tester', ['operability'],
    f'Claim C1, attack the landed fix beyond the frozen mutant family. {MUT}, make at least 8 hand-made mutants of the tally block and of the new guard and selftest code in tools/mutate-and-run.sh that the counter does NOT generate '
    f'(for example: delete the guard; guard `!=` → `>`; `nlegs=9` → `nlegs=8` with a dropped operand; FAIL and SETUP checks swapped; a status remapped inside the loop body such as `[[ $st -eq 1 ]] && st=0`; the selftest awk marker made to extract nothing; the selftest names list sourced from the loop instead of the assignments). '
    f'For each run `timeout 300 bash tools/mutate-and-run.sh --selftest` and record exit and `MUTATE_SELFTEST` line; restore the exact bytes after each (sha256 before/after). Report a table: mutant, killed or survived, and for each survivor whether it is equivalent or a real detector gap.')
add('CriticC1Claim', 'critic', ['operability'],
    f'Claim C1, adversarial review. Read {E}/contract.json, contract-amendment-1.json, contract-amendment-2.json, every control report under {LANE}/.ufo/waves/round-30/ctl/ and receipt under {E}/ctl/, and the fix (`git -C {LANE} diff {BASE} {REV} -- tools/mutate-and-run.sh`). '
    f'(1) Was the counter frozen before data (commit order: `git -C {LANE} log --format="%h %cI %s" {BASE}..{REV}`) and was every required control class scored before {REV}, including a shortcut keyed on labels? (2) Is the axis named by the surface it changes (operability: a runnable gate verdict), and is the claim quality work misnamed? (3) Can a do-nothing or shortcut change meet the frozen predicate? Name any untested shape. (4) Is the claim sized to one value re-derivable by one command? Verdict first per question.')
add('RegressionReplay', 'executor', ['operability'],
    f'No-harm, operability: the full ledger replay must still pass after the tally fix. In a fleet mirror (`{FLEET_CLONE}`), run `cd $R && timeout 2400 bash tools/mutate-and-run.sh --regression --workdir $W/rg` and paste the REGRESSION_* summary lines and exit. If it is not PASS (cases=9 passed=9), repeat the same at base {BASE} in a second mirror to show whether the result differs from base. Report both.')
add('RegistryNoHarm', 'executor', ['operability'],
    f'No-harm check of the gate/probe registry at {REV}. In a fleet mirror: `{FLEET_CLONE}`, then `cd $R && timeout 1200 python3 tools/registry-check.py --rev {REV}` (read its --help if flags differ). Paste the summary line and every row that is not held, with its exit. Do the same at base {BASE}. Compare row by row and name any row whose result differs and why.')
add('SelftestsNoHarm', 'executor', ['operability'],
    f'No-harm: run every lane tool selftest at {REV} and at base {BASE}, each in its own clone: `bash tools/mutate-and-run.sh --selftest` and `python3 tools/<x>.py --selftest` for each tools/*.py that accepts --selftest (check --help or the source), each under `timeout 600`. Table: tool, exit at base, exit at {REV}, summary line. Name every difference and its cause.')
add('RerunCensusR1', 'executor', ['coverage'],
    f'Frontier step. Run the SOURCES census at {REV} in a mirror: `W2=$(mktemp -d); cp {FLEET}/shokunin.conf $W2/; ln -s {FLEET}/scripts $W2/scripts; env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks {LANE} $W2/tameshi-shokunin; git -C $W2/tameshi-shokunin checkout -q --detach {REV}; {FLEET}/scripts/sources-census.sh validate --root $W2 tameshi`; paste output and exit; repeat at {BASE}. '
    f'Then `git -C {LANE} diff {BASE} {REV} -- corpus/SOURCES.md`: confirm only the S087 used-by cell changed in place, row S092 and the notes were appended, and every used-by path named exists at {REV}.')
add('ReopenS087', 'scout', ['coverage'],
    f'Frontier step. Re-open S087 by ordinary means: `curl -sSL -o /tmp/<your-name>.tgz https://registry.npmjs.org/mutation-testing-metrics/-/mutation-testing-metrics-3.9.0.tgz`; compute sha512 (base64) and compare with the row\'s anchor in `git -C {LANE} show {REV}:corpus/SOURCES.md` (row S087) and with the L1 snapshot {E}/sources/S087-mutation-testing-metrics-3.9.0.tgz. '
    f'Extract and check that `package/src/calculateMetrics.ts:254` reads `totalMutants: totalValid + totalInvalid + ignored + pending,` and `package/src/model/metrics.ts:60-61` the doc comment `The total number of mutants.` / `totalInvalid + totalValid`. Then read {LANE}/corpus/knowledge/regression-tally-completeness.md section "What S087 teaches here": is the reading faithful to the source, or overreaching? Agree or disagree with reasons.')
add('ReopenS092', 'scout', ['freshness'],
    f'Frontier step. Re-open the S092 source: `curl -sSL https://bazel.build/remote/caching.md` twice about 30 s apart; sha256 each; compare with the row S092 anchor (`git -C {LANE} show {REV}:corpus/SOURCES.md`) and the snapshot {E}/sources/S059-bazel-remote-caching.md. Is "Bazel does not track tools outside a workspace" present, and where? '
    f'Does row S092 follow the SOURCES contract ({FLEET}/CORPUS.md section "SOURCES.md — where a shokunin learns": append-only, a correction is a new row whose teaches opens `supersedes S0NN —`) and does it resolve routed item 7 (first bullet) of {LANE}/corpus/lessons/round-29-verifier-spotcheck.md? Agree or disagree with reasons.')
add('ReviewEntry', 'reviewer', ['quality'],
    f'Review {LANE}/corpus/knowledge/regression-tally-completeness.md at {REV} against bytes: every claim about the runner (`git -C {LANE} show {REV}:tools/mutate-and-run.sh`, guard and selftest lines), the counter ({E}/c1-measure-v3.py), the controls ({E}/ctl/), the witness ({E}/witness/) and MutateLegSum ({LANE}/.ufo/waves/round-29/w1/MutateLegSum.md). '
    f'List each statement that is wrong or imprecise with path:line, and say whether the entry overclaims (it must not state the measured head result).')
add('ReviewQualityR30', 'reviewer', ['quality'],
    f'Review the widely read edits of {REV} other than the entry: `git -C {LANE} diff {BASE} {REV} -- corpus/QUALITY.md corpus/README.md`. For QUALITY 58-63, check each Falsifier against bytes ({E}/r29-mistake1-ordering.txt, {E}/drift-sim-union4.txt, {LANE}/.ufo/evidence/round-29/coldread/select-receipt-w1.json, {LANE}/.ufo/waves/round-29/spec-w1.json key context, round-29 contract.json) and that each criterion routes the spot-check item it names ({LANE}/corpus/lessons/round-29-verifier-spotcheck.md routed items 1-7). '
    f'Name any routed item 1-7 that no criterion or fix routes. List mismatches with path:line.')
add('ConnectorOverlap', 'connector', ['adjacency'],
    f'Sibling-overlap scan for the C1 surface: tally/total completeness checks in runners and gates (a verdict summary whose counts must add up to the case total; selftests that run their own summary logic). Search sibling lanes under {FLEET}/*-shokunin (read-only; never tameshi) for the same defect class (a PASS that does not check every case was counted) with path:line. Report overlaps and whether tameshi should report them to the owner (report-only; never absorb).')
add('ScribeMistakes', 'scribe', ['calibration'],
    f'Draft, in your report only, candidate `## Mistakes` rows for corpus/lessons/round-30.md, format: class · evidence pointer · captured-by (criterion or rule, or `none`) · fix, where a fix counts only once shown able to fail. Mine this round so far: the v1 → v2 → v3 counter history (contract.json, amendment-1 and -2 under {E}/, control CtlK7Keyed {LANE}/.ufo/waves/round-30/ctl/CtlK7Keyed.md) and round-29\'s routed items ({LANE}/corpus/lessons/round-29-verifier-spotcheck.md). '
    f'For each, name the QUALITY criterion at {REV} (`git -C {LANE} show {REV}:corpus/QUALITY.md`, criteria 58-63) that captures it or `none`, and one command whose output shows the check failing on the old state.')

spec = {'wave': 'round-30-w1', 'reportDir': W, 'context': CONTEXT, 'items': items}
out = Path(LANE + '/.ufo/waves/round-30/spec-w1.json')
out.write_text(json.dumps(spec, indent=1) + '\n')
print(len(items), 'items for', n, 'sections ->', out)
