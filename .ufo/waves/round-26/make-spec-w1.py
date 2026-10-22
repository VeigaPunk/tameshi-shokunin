#!/usr/bin/env python3
"""Generate the round-26 wave-1 spec (build + first falsifiers), policy v1 band 32-64."""
import json
from pathlib import Path

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
KUM = FLEET + '/kumitate-shokunin'
REV = 'a08e85c5d7f899e8a5992e20517edb1a380d79eb'
PRE = '622d31d90b1fbc55c56e91a2b012bc18d6f1421a'
BASE = 'd4140796f4e48e8ec81b793facba73fbd03b4443'
PIN_REV = '1205c6621a2eccbb8ffceae86d9e7b79a7990b3a'
PIN_SHA = '40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f'
E = LANE + '/.ufo/evidence/round-26'
W = '.ufo/waves/round-26/w1'
DIRECTIVE = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text()
CLONE = ('Make your own private clone first: `git clone -q --no-hardlinks %s /tmp/<your-name>-r26 && '
         'git -C /tmp/<your-name>-r26 checkout -q --detach %s` and run commands only inside it. ') % (LANE, REV)

CONTEXT = f"""# Goal
Tameshi round 26 (verification-fixture craft), wave 1 of 2 (build + first falsifiers). Frozen contract {E}/contract.json, committed at
lane revision {PRE} before any mutant ran; integration landed at {REV} (base {BASE}).
C1 (depth, learning claim): ninth recorded mutation-ledger leg `js-cite-check` = kumitate {KUM}/scripts/cite-check.mjs at kumitate rev {PIN_REV}
(blob sha256 {PIN_SHA}, 2537 lines). Pre-registered spec {E}/cite-check/cite-check.defects.spec and predictions {E}/cite-check/predictions.json
(5 kill-aimed, 5 hole-aimed). Sweep result 5/10 killed, every verdict prediction held ({E}/cite-check/sweep/). Suite: hermetic `env -i` `node "$MUTANT" --selftest`
(62 hermetic cases). Runner {LANE}/tools/mutate-and-run.sh now carries nine legs; {LANE}/tools/mte-interop.py now judges nine legs.
Counter: `python3 {E}/c1-measure.py --repo CLONE` (before `depth_score=8` exit 1 at base; target `recorded_cases=9 wired_legs=9 depth_score=9` exit 0).
C2 (calibration): mismatches between the lane's own record and repo bytes for the three routed items 1-3 of {LANE}/corpus/lessons/round-25-verifier-spotcheck.md:189-199.
Counter: `python3 {E}/c2-measure.py --repo CLONE` (before `mismatches=3/3` at base; target 0/3). Item 1 (registry row) is already fixed at {REV}; items 2-3 are prose fixes this wave drafts.
The L1 TameshiR26 holds the planner seat and is the sole integrator: seats draft or attack; only the L1 edits lane files.
# Bounds (binding)
- Do exactly what your item names; verdict first, then evidence (path:line, exact commands with observed output), then the smallest safe correction.
- Write NOTHING except your own report file. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>, never at the fleet root.
- Never edit production files. Never run git write commands (add/commit/checkout/reset/stash/push/fetch/pull) in {LANE}. Never run ANY `jj` command anywhere —
  not `jj log`, not `jj st`, not at the fleet root {FLEET}, not in {LANE}, not in a clone: any jj command snapshots a colocated working copy (round-25 seats did this; it is a routed defect).
  Never touch the fleet repo {FLEET}, sibling lanes, lane jj state or the lane Git index. Read-only git with GIT_OPTIONAL_LOCKS=0 is fine. Sibling repos (e.g. {KUM}) are read-only; read pinned bytes with `git -C {KUM} show {PIN_REV}:scripts/cite-check.mjs`.
- Items that run code do so only inside their own /tmp clone or /tmp scratch dir. Never run gates, selftests or sweeps in {LANE} itself.
- No seat spawns, except an executor may spawn one read-only labrat probe for a falsifiable hypothesis.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool, version, channel and reason in your report). Pacman guard: all pacman transactions are PAUSED host-wide; install via uv tool, npx or an official binary in ~/.local/bin; never -Sy/-Syu/-U/-R, never restart a host service.
- Write plain English, no run-together words. No producer-authentication, promotion or numeric-score claims. A source counts only if you opened it this session: give URL or path, access date and a located quote of at most 25 words.
- Sourcing rule (Main, 2026-10-22T10:24Z): open sources by ordinary means only. Never use a headless browser or any other tool to pass a bot challenge, captcha or access control. Record a source you cannot open that way as unopened; it cannot support an admitted entry."""

items = []

def add(name, role, axes, target, acceptance=None):
    acceptance = acceptance or f'Report: {W}/{name}.md'
    prompt = '/skill:godspeed\n' + DIRECTIVE + '\n# Target\n' + target + '\n\n# Acceptance\n' + acceptance + '\n'
    items.append({'name': name, 'role': role, 'axes': axes, 'prompt': prompt})


ENTRY = LANE + '/corpus/knowledge/mutation-case-kumitate-sources-check.md'
# --- build: prose drafts (scribes) ------------------------------------------------
add('DraftEntry', 'scribe', ['depth'],
    f'C1. Draft the new knowledge entry `corpus/knowledge/mutation-case-kumitate-cite-check.md` in the shape of {ENTRY} '
    f'(frontmatter keys source/verified-at/recheck/ground first, then sections). Ground every number in {E}/cite-check/ (spec, predictions, sweep.txt, results.tsv, '
    'evidence/*.out). Include: the per-defect table (id, mutation, prediction, verdict, witness case from evidence/*.out), the kill rate, the prediction-witness '
    'mismatches (a verdict held but the killing case differs from the predicted case, e.g. K_FENCE_TILDE), survivor classes, and what the suite does not pin. '
    'Frontmatter `source:` must name S088 (the pinned kumitate file) and S089 (Stryker supported-mutators page) as placeholders the L1 will confirm. '
    'Give the full draft text in your report inside one fenced block.')
add('DraftSourcesRows', 'scribe', ['depth'],
    f'C1 frontier step. Read the SOURCES contract in {FLEET}/CORPUS.md section "SOURCES.md — where a shokunin learns" and rows S086/S087 in {LANE}/corpus/SOURCES.md. '
    f'Open both sources yourself this session: (a) S088 = kumitate scripts/cite-check.mjs at rev {PIN_REV} (`git -C {KUM} show {PIN_REV}:scripts/cite-check.mjs`, check sha256 {PIN_SHA}); '
    '(b) S089 = https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/ . Draft both rows in the exact column shape of the table '
    '(status mined, tier, recheck, used-by `knowledge/mutation-case-kumitate-cite-check.md`), plus a located quote (at most 25 words, with line or section) for each. '
    f'Then run `{FLEET}/scripts/sources-census.sh validate --root <a /tmp copy of the fleet layout or read-only> tameshi` only if it can run read-only; otherwise list the census rules your rows must satisfy (W04 duplicate url etc.).')
add('DraftScorecard', 'scribe', ['calibration', 'depth'],
    f'Draft two append-only blocks for {LANE}/SCORECARD.md (read its round-24 and round-25 sections first, lines 1127-1256). '
    f'(1) "## Round 26 — ninth recorded case and round-25 record repair (2026-10-22)": both claims from {E}/contract.json with counters, before values '
    f'({E}/c1-before.stdout, c2-before.stdout), targets, plus a capabilities-table note (none new; mte-interop row now registered). Leave the after values as `<AFTER>` placeholders. '
    '(2) "### Round 25 — correction (appended in round 26)": state that amendment 3 (in commit 77302fa, `contract-amendment-3.json`) also precedes the recorded after-measurement, '
    f'what it added (read {LANE}/.ufo/evidence/round-25/contract-amendment-3.json), and that the `before_any_after_measurement` flag is true for the L1 receipts but seats had already run the C2 counter at PASS 8/8 '
    f'at c9ff09f and 09dc114 (cite {LANE}/.ufo/waves/round-25/w1/C2LiveCheck.md and {LANE}/corpus/lessons/round-25-verifier-spotcheck.md:82-95). The words "amendment 3", "77302fa" and '
    '"before_any_after_measurement" must appear. Give both blocks in fenced text.')
add('DraftLesson25Correction', 'scribe', ['calibration'],
    f'Draft an append-only "## Correction (round 26)" block for the end of {LANE}/corpus/lessons/round-25.md: its `## Claims` names amendments 1-2 only; amendment 3 '
    f'(77302fa, {LANE}/.ufo/evidence/round-25/contract-amendment-3.json) also preceded the after-measurement. Say what amendment 3 added, quoting the JSON. '
    'The words "amendment 3" and "77302fa" must appear. Do not rewrite earlier text. Give the block fenced.')
add('DraftLesson26', 'scribe', ['calibration', 'depth'],
    f'Draft `corpus/lessons/round-26.md` in the shape of {LANE}/corpus/lessons/round-25.md: ## Claims (C1, C2 from {E}/contract.json), ## Gate (admit candidates: the new entry, '
    'the ninth leg, the two counters; rejects with reasons; S088/S089 with URL, access date 2026-10-22 and quote placeholders), ## Mistakes (mine one mistake: the round-25 '
    'verified-at line recorded the pre-amendment-3 tool run, tool sha 8c24255c and selftest 16/16, while the measured tool was 8269b82f with 17/17; class, evidence pointer, '
    'captured-by (which QUALITY criterion should have caught it, or none), fix = the C2 counter item R25-SPOT-3, shown able to fail: it reports MISMATCH at base, '
    f'see {E}/c2-before.stdout), ## Routed items 4-5 disposition (leave placeholders), ## After measurement (placeholders). Fenced draft.')
add('DraftQuality', 'scribe', ['calibration'],
    f'Read {LANE}/corpus/QUALITY.md (its last 60 lines for numbering and shape) and {LANE}/corpus/lessons/round-25-verifier-spotcheck.md:187-205. Draft two new lesson-backed criteria: '
    '(a) a knowledge entry\'s verified-at line names the sha256 of the measured tool bytes and a committed receipt of the run, never an earlier run; '
    '(b) every wave context names jj next to git: no seat runs any jj command, because any jj command snapshots a colocated working copy. '
    'For each give the check that can fail and how it was shown able to fail. Fenced draft with the next free numbers.')
add('DraftProvinceReadme', 'scribe', ['depth'],
    f'Draft (1) an append-only "## Core — round 26 append (2026-10-22)" block for {LANE}/PROVINCE.md in the shape of its round-18 append: the recorded legs are now nine; the ninth is '
    f'kumitate scripts/cite-check.mjs (rev {PIN_REV}, blob sha256 {PIN_SHA}), probed read-only as a kumitate scripts/* primary surface, no opt-in needed; '
    f'(2) a "## Round 26 — ninth recorded case, round-25 record repair" block for {LANE}/corpus/README.md (read its ## Frontier and the round-25 section first): coverage map row for the ninth leg, '
    'which frontier rows move or stay. Fenced drafts.')
add('DraftSkillSurvivors', 'scribe', ['depth'],
    f'Draft a "Survivor class in this case" table for the new SKILL.md section "## Ninth recorded case — round 26" ({LANE}/SKILL.md end of file), in the shape of the round-18 '
    f'table in "## Eighth recorded case — round 18". One row per survivor in {E}/cite-check/sweep/results.tsv: survivor class, what the suite does not pin, fix belongs to (kumitate). '
    f'Read the pinned bytes and the selftest code (`git -C {KUM} show {PIN_REV}:scripts/cite-check.mjs`) to justify each row with a line number. Flag any survivor that may be '
    'an equivalent mutant (no input can tell it apart), with your reasoning. Fenced draft.')
# --- sources (scouts) -------------------------------------------------------------
add('OpenStrykerMutators', 'scout', ['depth'],
    'C1 sourced claim. Open https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/ this session. Map each of the ten defects in '
    f'{E}/cite-check/cite-check.defects.spec to the closest Stryker mutator class (or "no Stryker mutator"), with a located quote of at most 25 words per class used, '
    'section names, access date. Say which survivors Stryker\'s default mutators would also generate.')
add('OpenEquivalentSource', 'scout', ['depth'],
    'Find and open a primary source that defines an equivalent mutant and says how mutation scores treat it (e.g. PIT FAQ or docs at pitest.org, the Stryker docs, '
    'or the survey "Overcoming the Equivalent Mutant Problem" by Madeyski et al., IEEE TSE 2014). Give URL, access date and a located quote of at most 25 words. '
    f'Check {LANE}/corpus/SOURCES.md for an existing row first and say if one already covers it (id and url).')
add('OpenCiteCheckPin', 'scout', ['depth'],
    f'Re-open the pinned target: `git -C {KUM} cat-file -t {PIN_REV}`, `git -C {KUM} ls-tree {PIN_REV} scripts/cite-check.mjs`, sha256 of `git show {PIN_REV}:scripts/cite-check.mjs`, '
    f'whether {PIN_REV} is an ancestor of kumitate origin/master and whether the blob is unchanged at the master tip. Quote (at most 25 words, with line numbers) the header text that defines '
    'the exit map and the hermetic suite group. Report the kumitate working-tree state only as context (it is not the pin).')
# --- code (executors) -------------------------------------------------------------
for sid, hint in [('S_OOR_EDGE', 'a citation of exactly line n+1 of an n-line file'),
                  ('S_STRICT', 'a --strict run over a tree with exactly one warning'),
                  ('S_EMPTY_GUARD', 'whether any input reaches filesScanned==0 with resolved>0 (prove equivalence or find the input)'),
                  ('S_USAGE', 'an unknown flag on the CLI'),
                  ('S_PIN_INCLUDES', 'a sha256 pin whose hex sits inside, not at the start of, the cited file digest')]:
    add('Probe' + sid.replace('_', ''), 'executor', ['depth'],
        f'C1 survivor probe for {sid}. In /tmp scratch, materialize the pristine pin (`git -C {KUM} show {PIN_REV}:scripts/cite-check.mjs`), build the mutant by applying '
        f'exactly the {sid} @old/@new edit from {E}/cite-check/cite-check.defects.spec, and write a small hermetic off-suite probe (temp tree, CLI run of pristine and mutant) '
        f'that tells them apart — hint: {hint}. Paste the probe and both observed outputs. If no input can tell them apart, give the argument.',
        f'Report: {W}/Probe{sid.replace("_", "")}.md. Its LAST line must be exactly `PROBE {sid}: DISTINGUISHED`, `PROBE {sid}: EQUIVALENT` or `PROBE {sid}: UNDECIDED`.')
add('ReplicateSweep', 'executor', ['depth'], CLONE +
    f'Run: replicate the ninth-leg sweep independently. Materialize the pin from kumitate, then run `bash tools/mutate-and-run.sh --target <pin copy> --defects '
    '.ufo/evidence/round-26/cite-check/cite-check.defects.spec --suite "<the suite string in contract.json claims.C1.leg.suite>" --workdir /tmp/<you>-sweep` in your clone. '
    'Compare every verdict with the committed results.tsv. Then run `bash tools/mutate-and-run.sh --regression` in the clone and report the REGRESSION line.')
add('RegistryCheck', 'executor', ['operability'],
    f'Run: `git clone -q --no-hardlinks {LANE} /tmp/<you>-reg` (a full clone, so master holds {REV}), then from inside it `python3 tools/registry-check.py --rev {REV}`. '
    'Report the REGISTRY_CHECK line, every row that is not `held`, the two new rows mte-interop-selftest and mte-interop-check, and the wall time.')
add('InteropCheck', 'executor', ['coverage'], CLONE +
    f'Run: `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root {FLEET} --emit /tmp/<you>-mte` and the `--selftest`. '
    'Report every MTE_LEG line and the verdict. For the js-cite-check report, check every mutant location (line, column) against the unique @old string in the pinned file.')
add('ColdreadPilot', 'executor', ['calibration'],
    f'Prepare wave 2. Read the cold-read recipe in {LANE}/SKILL.md ("Recipe for one bucket, cold", near lines 1878-1893), {LANE}/.ufo/evidence/round-18/coldread/assemble.py and '
    f'{LANE}/.ufo/evidence/round-21/coldread/measure.py. Do ONE real cold read end to end in /tmp: the SKILL.md section "## Ninth recorded case — round 26" at {REV} '
    '(fleet-mirror clone layout per the recipe, commands under tools/trace-inputs.py, a tameshi-coldread-report-v2 verdict block, assemble with --carry the current ledger into a '
    'scratch ledger, then run the round-21 measure against a scratch commit in your clone). Write in your report an exact, copy-paste recipe a fresh seat can follow for one '
    'section, the report-v2 JSON shape with every required key, and the pitfalls you hit.')
add('ProbeIntegrations', 'executor', ['depth'],
    f'Run in /tmp: does cite-check\'s non-hermetic `--integrations` group (needs --src/--self; read-only over {KUM} and ~/Projects/ufo-fsd-alpha) kill any of the five survivors '
    f'in {E}/cite-check/sweep/results.tsv? Apply each survivor edit to a copy of the pinned file, run `node <copy> --integrations` for pristine and mutant, compare. '
    'The ledger leg uses the hermetic group only; this is an observation, not a re-measure.')
# --- attacks ----------------------------------------------------------------------
add('MutateC1Counter', 'mutation-tester', ['depth'], CLONE +
    'Run: show .ufo/evidence/round-26/c1-measure.py can fail. In the clone make scratch variants of tools/mutate-and-run.sh: drop the js-cite-check ledger line; drop its '
    'regression_case_git call; drop its spec heredoc; change its lent tuple killed count; change one TABLE_CITECHECK verdict; duplicate a ledger line. Run the counter on each and report '
    'line and exit. Also name any weakening the counter cannot see.')
add('MutateC2Counter', 'mutation-tester', ['calibration'], CLONE +
    'Run: show .ufo/evidence/round-26/c2-measure.py can fail and find where it can be gamed. For each label build a scratch variant that should resolve and one that should not '
    '(e.g. "amendment 3 was never applied" text; a verified-at receipt path to an unrelated file that happens to contain the string; a superseded registry row). Report each result.')
add('MutateRunnerSelftest', 'mutation-tester', ['depth'], CLONE +
    'Run: mutate the round-26 lines of tools/mutate-and-run.sh in scratch copies (nlegs 9 to 8; drop the js-cite-check lent tuple; TABLE_CITECHECK killed count off by one; '
    'drop the js-cite-check spec file check; drop "$st_citecheck" from the loop) and run `bash <copy> --selftest` and, where cheap, `--regression`. Which mutants does the tool catch?')
add('MutateInteropLegSet', 'mutation-tester', ['coverage'], CLONE +
    'Run: mutate tools/mte-interop.py in scratch (drop js-cite-check from LEG_TABLE; map it to the wrong TABLE_ var; keep eight legs but add a ninth workdir) and run --check '
    'against a kept nine-leg regression workdir (`bash tools/mutate-and-run.sh --regression --keep`, then `--workdir`). Report which mutants are refused and how.')
add('MtGuardGapsRecheck', 'mutation-tester', ['calibration'], CLONE +
    f'Routed item 4, first part. {LANE}/.ufo/waves/round-25/w1/MtGuardGaps.md lists 17 single-edit weakenings of tools/command-binding.py evaluate() that its selftest did not kill. '
    'Re-run each at this revision (`python3 .ufo/evidence/round-25/c1-suite.py selftest <mutant>` or the selftest directly) and report which still survive. No fixes.')
add('ReviewRunnerDiff', 'reviewer', ['depth'],
    f'Review `git -C {LANE} diff {PRE} {REV} -- tools/mutate-and-run.sh tools/mte-interop.py`: every leg-count site updated (search the whole runner and SKILL.md for "eight" and 8 that '
    'refer to legs), comments accurate, and the embedded js-cite-check spec heredoc byte-identical to the committed spec file (extract and cmp). List misses with line numbers.')
add('ReviewPredictions', 'reviewer', ['depth'],
    f'For each defect, compare the predicted verdict and named selftest case in {E}/cite-check/predictions.json with the observed verdict and the FAIL lines in {E}/cite-check/sweep/evidence/<id>.out. '
    'Count verdict mismatches and witness mismatches separately and explain each witness mismatch from the pinned code.')
add('ReviewPreregTiming', 'reviewer', ['depth'],
    f'Check that pre-registration preceded every mutant run: commit time of {PRE} (`git -C {LANE} show -s --format=%cI {PRE}`), MUTATE_DATE in {E}/cite-check/sweep/sweep.txt, the spec and '
    f'predictions bytes at {PRE} versus {REV} (unchanged?), and {FLEET}/.ufo/watchdog.log is not needed. Report times and sha256 values.')
add('ReviewSkillRows', 'reviewer', ['operability'],
    f'Review the new SKILL.md section at the end of {LANE}/SKILL.md ("## Ninth recorded case — round 26" and its registry table) and the two new rows at the end of {LANE}/tools/registry.json: '
    'exit map and wording versus the tool docstring (tools/mte-interop.py:1-45), expected stdout strings, timeouts, the uv dependency, and any claim the section makes that the evidence does not show.')
add('ReviewMonitorHarm', 'reviewer', ['calibration'], CLONE +
    f'Run: `python3 .ufo/evidence/round-21/coldread/measure.py --repo /tmp/<your-name>-r26 --rev {REV} --explain` (use a clone whose master contains {REV}; clone without --detach if needed). '
    'Report calibration_restraint_score, depth_score, sections covered/total and, for every uncovered heading, the reason (which input drifted or that it is new). This is the harmed intermediate reading.')
add('ReviewMteLeg9', 'reviewer', ['coverage'],
    'Review how tools/mte-interop.py builds the js-cite-check report: language for .mjs, location from the unique @old string, status mapping, and whether the leg\'s pinned '
    'revision appears anywhere in the emitted report (routed item 4: emitted reports name targets without a lane or revision pin). Read the code; cite lines.')
add('CriticC1', 'critic', ['depth'],
    'Attack C1: is a ninth leg a real depth move or a count bump? Consider: the PROVINCE two-lane rule, the round-12 ruling that reanalysis of a measured target is depth within a case, '
    'the fact that predictions were written by the L1 after reading the suite, the suite being only the hermetic group, and whether the counter (c1-measure.py) can pass while '
    'the leg is wrong. Name each objection with evidence and say which ones hold.')
add('CriticC2', 'critic', ['calibration'],
    f'Attack C2 against {FLEET}/.ufo/prompts/tameshi-round-26.md section 6.9 (claim sizing; a calibration claim must count mismatches between the lane\'s self-assessment and repo state) '
    'and the drift sentinel "same routed defect class in a lane 3 rounds running". Is C2 a calibration claim or a record chore? Is the population honest (three fixed labels)? Holes in c2-measure.py?')
add('CriticEquivalence', 'critic', ['depth'],
    'Attack the 5/10 headline of the ninth leg. If S_EMPTY_GUARD (or another survivor) is an equivalent mutant, what is the honest way to record it in the ledger and the entry? '
    'How do PIT and Stryker treat equivalent mutants in the score (cite opened sources)? Should the recorded table change, or only the entry text? Give a recommendation that does not move a frozen target.')
add('ConnectorOverlap', 'connector', ['adjacency'],
    f'Sibling-overlap scan. Does kumitate ({KUM}) own or record mutation work on scripts/cite-check.mjs (QUALITY, lessons, its own --integrations "symbol-machinery mutation copy")? '
    f'Does any other lane measure it? Is the ninth leg in tameshi\'s PROVINCE ({LANE}/PROVINCE.md lines 7-11, 27-40)? Also check kotoba-shokunin/corpus/knowledge/frontmatter-rule-authorities-round48.md only if a draft touches SKILL.md frontmatter (it should not). Report contested scope, if any.')
add('ScoutRoutedOpen', 'scout', ['calibration'],
    f'Routed item 4, second part: at {REV}, give the current state (open or closed, path:line) of (a) the 14 re-attack FINDING rows in {LANE}/.ufo/evidence/round-25/dead-falsifier-disposition.json, '
    f'(b) round-24 spot-check items 2-4 ({LANE}/corpus/lessons/round-24-verifier-spotcheck.md), (c) "emitted reports name targets without a lane or revision pin" ({LANE}/.ufo/waves/round-25/w1/SiblingOverlap.md). One line each.')
add('ScoutJjBounds', 'scout', ['calibration'],
    f'Routed item 5. Without running jj: list whether {FLEET}/.jj exists (ls only), read {LANE}/corpus/lessons/round-25.md:83 and the round-25 wave context ({LANE}/.ufo/waves/round-25/spec.json, key context), '
    'and say whether this wave\'s context (you have it above) closes the gap. Run `git -C ' + FLEET + ' status --porcelain` and list any untracked file that names tameshi round 25 or 26.')
add('ScoutFrontier', 'scout', ['depth'],
    f'Read {LANE}/corpus/README.md "## Frontier" (F1-F10) and all later frontier status notes, and {LANE}/PROVINCE.md. Which frontier row, if any, does a ninth recorded leg on a kumitate gate advance? '
    'Is it Core ground already (recorded legs)? Report exact lines so the L1 can write the README block without overclaiming.')

spec = {'wave': 'round-26-w1', 'reportDir': W, 'context': CONTEXT, 'items': items}
out = Path(LANE + '/.ufo/waves/round-26/spec-w1.json')
out.write_text(json.dumps(spec, indent=1) + '\n')
print(len(items), 'items ->', out)
