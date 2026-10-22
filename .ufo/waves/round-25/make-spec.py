#!/usr/bin/env python3
"""Generate the round-25 single v2 wave spec (build + attack items together)."""
import json
from pathlib import Path

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
REV = 'c9ff09fb41fb8aac5fc335faf10858ff606bd5df'
BASE = '1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5'
E = LANE + '/.ufo/evidence/round-25'
W = '.ufo/waves/round-25/w1'
DIRECTIVE = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text()
CLONE = ('Make your own private clone first: `git clone -q --no-hardlinks %s /tmp/<your-name>-r25 && '
         'git -C /tmp/<your-name>-r25 checkout -q --detach %s` and run commands only inside it. ') % (LANE, REV)

CONTEXT = f"""# Goal
Tameshi round 25 (verification-fixture craft). Frozen contract {E}/contract.json at lane revision {REV} (base {BASE}).
C1 (calibration, repair-first): the three round-23 closure-routed items round 24 left unrecorded — R23-ROUTED-1 multi-token stdout
fixture in the ruler ({E}/multitoken-cases.json, multitoken-mutants.spec), R23-ROUTED-2 receipted guard-sweep rerun (guard-mutants.spec),
R23-ROUTED-3 dead-falsifier coverage disposition (the 34 round-23 wave-2 seats that died; several items of THIS wave re-attack them).
Counter: `python3 {E}/c1-measure.py --repo CLONE` (before 0/3 at base; target 3/3). Suite {E}/c1-suite.py; runner {LANE}/tools/mutate-and-run.sh.
C2 (coverage, capability; frontier F1 report interop): {LANE}/tools/mte-interop.py emits each recorded mutation-ledger leg as a
mutation-testing-elements report, validates it with the official schema 3.9.0 and scores it with the official mutation-testing-metrics 3.9.0
library (both vendored, sha512-pinned in {LANE}/tools/vendor/). Counter: `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root {FLEET}`
(before: tool absent; target MTE_INTEROP: PASS legs_conforming=8/8). The L1 TameshiR25 holds the planner seat and is the sole integrator.
# Bounds (binding)
- Attack or build exactly what your item names; verdict first, then evidence (path:line, exact commands with observed output), then the smallest safe correction.
- Write NOTHING except your own report file. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>, never at the fleet root.
- Never edit production files; never run git/jj write commands (add/commit/checkout/reset/stash/push/fetch, any mutating jj) in {LANE}; never touch the fleet repo {FLEET}, sibling lanes, lane jj state or the lane Git index. Read-only git with GIT_OPTIONAL_LOCKS=0 is fine. Sibling repos are read-only.
- Items that say "Run" may execute commands, only inside their own /tmp clone (or /tmp scratch). Never run gates, selftests or sweeps in {LANE} itself.
- No seat spawns, except an executor may spawn one read-only labrat probe for a falsifiable hypothesis.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool, version, channel and reason in your report). Pacman guard: all pacman transactions are PAUSED host-wide; install via uv tool, npx or an official binary in ~/.local/bin; never -Sy/-Syu/-U/-R, never restart a host service.
- Write plain English. No producer-authentication, promotion or numeric-score claims."""

items = []


def add(name, role, axes, target, acceptance=None):
    acceptance = acceptance or f'Report: {W}/{name}.md'
    prompt = '/skill:godspeed\n' + DIRECTIVE + '\n# Target\n' + target + '\n\n# Acceptance\n' + acceptance + '\n'
    items.append({'name': name, 'role': role, 'axes': axes, 'prompt': prompt})


# --- R3: re-attack every round-23 wave-2 item whose seat died (34) -----------------
r23 = json.loads(Path(LANE + '/.ufo/waves/round-23/spec2.json').read_text())
dead = {r['name'] for r in json.loads(Path(LANE + '/.ufo/waves/round-23/original-outcomes2.json').read_text())['rows']
        if r['status'] != 'completed'}
for it in r23['items']:
    if it['name'] not in dead:
        continue
    original = it['prompt'][it['prompt'].index('# Target') + len('# Target\n'):].split('\n\n# Acceptance')[0].strip()
    role = 'scout' if it['role'] == 'scout' else 'critic' if it['role'] in ('connector', 'revenger') else 'reviewer'
    add('Re' + it['name'], role, ['calibration'],
        f'Re-attack of round-23 wave-2 item {it["name"]} (original role {it["role"]}); its seat died when the round-23 author died and '
        f'never reported, so this falsifier never ran. Original item text, verbatim:\n> {original}\n'
        f'Do it now against the round-23 artifacts (frozen) AND say whether the finding still applies at lane revision {REV} '
        f'(the row may be superseded in {LANE}/tools/registry.json; command-binding.py may have changed since round 23). '
        'You may read and run the original read-only checks; if the original says "do not write any file", that is superseded: write only your report.',
        f'Report: {W}/Re{it["name"]}.md. Its LAST line must be exactly `R23-REATTACK {it["name"]}: AGREE` (the attacked binding or claim holds; '
        f'say what you checked) or `R23-REATTACK {it["name"]}: FINDING` (a concrete counterexample is in the report).')

# --- C1 attacks ---------------------------------------------------------------------
add('MtWeakerGate', 'mutation-tester', ['calibration'], CLONE +
    f'Run: find a weaker implementation of the stdout-token check in tools/command-binding.py:111 that still passes all seven ruler-owned fixtures in '
    f'{E}/multitoken-cases.json (via `python3 .ufo/evidence/round-25/c1-suite.py multitoken <your mutant copy>`). Try at least six weakenings '
    '(token-set equality, prefix match, case-folded match, whitespace-split membership, first-and-last only, per-line match). Report each with its suite result.')
add('MtGuardGaps', 'mutation-tester', ['calibration'], CLONE +
    'Run: find single-edit guard weakenings of tools/command-binding.py evaluate() (lines 65-113) that the gate selftest does NOT kill '
    '(`python3 .ufo/evidence/round-25/c1-suite.py selftest <mutant>`), beyond the eight in guard-mutants.spec: e.g. cwd compared after normpath, '
    'revision prefix compare, exit compared with abs(), membership via subset instead of equality. Report kills/survivors with outputs.')
add('MeasureVacuity', 'critic', ['calibration'],
    f'Attack {E}/c1-measure.py: can any of the three items count while its check is vacuous? Look at: the SCORECARD label regex, sweep() witness regex, '
    'empty defect lists, runner exit handling, the R3 negative controls (drop-one-row, flip-one-status) when all rows are died rows, '
    'and staging (which files are copied). Name each concrete hole with a constructed input.')
add('MeasureMutants', 'mutation-tester', ['calibration'], CLONE +
    'Run: mutate .ufo/evidence/round-25/c1-measure.py itself (drop the witness check; accept runner exit 1; skip set equality in R3; skip the '
    'negative controls) and run each mutant with --repo against your clone. Which mutants change the result at this revision? A mutant that changes '
    'nothing marks a check this revision cannot exercise; list them.')
add('C1BeforeRerun', 'executor', ['calibration'], CLONE +
    f'Run: in a second clone checked out at base {BASE}, run `python3 <your REV clone>/.ufo/evidence/round-25/c1-measure.py --repo <base clone>` and '
    f'the same against your REV clone. Compare the base output with the recorded {E}/c1-before.json (exit, final line). Report exact outputs.')
add('C1Framing', 'critic', ['calibration'],
    f'Attack the framing of C1 in {E}/contract.json: is it a calibration claim that counts mismatches between the lane self-assessment and repo state '
    f'(round-24 verifier spot-check {LANE}/corpus/lessons/round-24-verifier-spotcheck.md:34,37,63), or a renamed fixture count? Is the 0/3 baseline a '
    'capability-absence baseline only? Does the claim narrow the routed items (compare MANIFEST rounds[421].notes, read-only via python json parse of '
    f'{FLEET}/MANIFEST.json)? Give the strongest honest wording.')
add('FixtureOracle', 'reviewer', ['calibration'],
    f'Review {E}/multitoken-cases.json and {E}/c1-suite.py: are the expected exits and finding_ids independently derivable from the gate contract '
    '(not copied from a run)? Does each mutant in multitoken-mutants.spec map to a fixture that kills it for the stated reason (name the fixture)? '
    'Is any fixture order-dependent or able to pass for the wrong reason?')

# --- C2 build and attacks ----------------------------------------------------------
add('C2LiveCheck', 'executor', ['coverage'], CLONE +
    f'Run: `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --selftest` and '
    f'`uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root {FLEET} --emit /tmp/<your-name>-mte`. '
    'Report both exits and every MTE_LEG / CASE line verbatim, and the wall time.')
add('C2Mutants', 'mutation-tester', ['coverage'], CLONE +
    'Run: mutate tools/mte-interop.py (INCONCLUSIVE mapped to Timeout; KILLED mapped to Timeout; location column off by one; end position = start; '
    'score tolerance widened to 1.0; ledger check dropped; schema validation skipped) and run --selftest and --check --workdir on a kept regression workdir '
    'for each. Which mutants survive both? Each survivor is a missing check: say which.')
add('C2Locations', 'reviewer', ['coverage'], CLONE +
    'Run the tool with --emit, then independently recompute start/end line and column for every mutant of two legs (one js, one bash) from the pinned '
    'target and the spec @old string (1-based, end exclusive per the schema Location description). Report any mismatch.')
add('C2Tautology', 'critic', ['coverage'],
    f'Attack C2 in {E}/contract.json and {LANE}/tools/mte-interop.py: given a 1:1 status mapping, is "official score equals tameshi kill rate" a '
    'tautology? Which parts of the check carry real information (schema acceptance, Timeout/RuntimeError semantics, ledger counts, rounding of the '
    'ledger percentages)? Propose the honest claim wording and any additional falsifier.')
add('C2Integrity', 'reviewer', ['coverage'],
    f'Run: verify {LANE}/tools/vendor/*.tgz against the npm registry: `npm view mutation-testing-report-schema@3.9.0 dist.integrity` and the '
    'metrics package, compare to the PACKAGES table in tools/mte-interop.py and to sha512 of the files. Check that the schema member the tool reads '
    'equals the GitHub master file https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/master/packages/report-schema/src/mutation-testing-report-schema.json (or say what differs).')
add('C2TarSafety', 'reviewer', ['coverage'],
    f'Review {LANE}/tools/mte-interop.py official_metrics() and run_regression(): tar extraction path safety, symlink staging of sibling repos '
    '(can anything write into a sibling repo?), temp cleanup, and whether a missing node/jsonschema yields SETUP (exit 2) rather than PASS.')
add('C2Semantics', 'scout', ['coverage'],
    'Open https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/ now. Quote (<=25 words each) the definitions of '
    'Killed, Survived, Timeout, RuntimeError and the mutation score. Does mapping tameshi INCONCLUSIVE to RuntimeError (excluded from valid) match '
    'the definitions better than Timeout? Record the access date.')
add('C2SchemaSource', 'scout', ['coverage'],
    'Open the npm page or registry metadata of mutation-testing-report-schema 3.9.0 and mutation-testing-metrics 3.9.0 '
    '(https://www.npmjs.com/package/mutation-testing-report-schema, https://registry.npmjs.org/mutation-testing-metrics/3.9.0), and the GitHub '
    'repo stryker-mutator/mutation-testing-elements. Record publish date, license, repository URL and one <=25-word located quote each for the '
    'Position definition and the mutationScore formula (packages/metrics/src/calculateMetrics.ts or dist).')
add('C2OtherEmitters', 'scout', ['coverage'],
    'Find which other mutation tools emit the mutation-testing-elements JSON format (e.g. cargo-mutants, mutmut, Stryker.NET, Stryker4s, Infection, '
    'mull). Open each primary doc page you cite and quote it (<=25 words). This informs which sibling-lane gates could be compared later.')
add('C2Rounding', 'reviewer', ['coverage'],
    f'Compare the ledger percentages in {LANE}/tools/mutate-and-run.sh:84-96 (integer percent) with the official float scores the tool reports '
    '(e.g. 7/15 = 46.67). Are any ledger lines or SKILL.md/knowledge statements wrong under exact arithmetic? List them with path:line.')

# --- prose drafts (scribes) and recon ------------------------------------------------
add('DraftKnowledge', 'scribe', ['coverage'],
    f'Draft a knowledge entry for {LANE}/corpus/knowledge/mte-report-interop.md (write the DRAFT only into your report). Follow the shape of '
    f'{LANE}/corpus/knowledge/hermetic-env-differential.md (source: header, verified-at, recheck, scope, bounds). Content: the tameshi->mutation-testing-elements '
    'mapping (status, location from unique @old, language, thresholds), what the official schema and metrics library check, the INCONCLUSIVE and '
    'Timeout semantics, the integer-percent rounding of the ledger, and explicit non-claims (no Stryker run, hand-seeded defects are not Stryker mutators). '
    f'Cite S001, S002 and the new rows S086 (schema package 3.9.0) and S087 (metrics package 3.9.0). Use {LANE}/tools/mte-interop.py as the evidence surface.')
add('DraftSources', 'scribe', ['coverage'],
    f'Draft two new rows for {LANE}/corpus/SOURCES.md in its exact column shape (read the header and rows S084/S085): S086 npm '
    'mutation-testing-report-schema 3.9.0 and S087 npm mutation-testing-metrics 3.9.0 (tier A, status mined, recheck 180d, used-by '
    'knowledge/mte-report-interop.md), plus the round-25 search-log paragraph in the same shape as the round-24 one. Write drafts into your report only.')
add('DraftLesson', 'scribe', ['calibration'],
    f'Draft {LANE}/corpus/lessons/round-25.md sections `## Mistakes` and `## Gate`, following the shape of {LANE}/corpus/lessons/round-24.md. Mine one '
    'mistake: round 24 declared a routed population that omitted three closure-routed items (class, evidence pointer, captured-by, fix). Say which '
    f'existing QUALITY.md criterion should have caught it ({LANE}/corpus/QUALITY.md, e.g. 12, 44, 48) and whether the round-25 c1-measure can fail on it. Draft only.')
add('DraftSkillTable', 'scribe', ['coverage'],
    f'Draft a short SKILL.md decision table for {LANE}/SKILL.md: "Exporting a tameshi sweep as a mutation-testing-elements report" — '
    'columns: tameshi verdict, MTE status, counts in valid?, counts as detected?, source row. Plus three error patterns (vocabulary status, '
    'line 0 location, timeout treated as kill) each tied to a selftest case name in tools/mte-interop.py. Draft only.')
add('SiblingOverlap', 'connector', ['coverage', 'adjacency'],
    f'Sibling-overlap scan, read-only: grep the sibling lanes under {FLEET}/*-shokunin (excluding tameshi) for mutation-testing-elements, stryker, '
    '"mutationScore", mutation report JSON, and for any lane that already emits machine-readable mutation results. Report contested scope, if any.')
add('RoutingCarry', 'connector', ['calibration'],
    f'Map every routing item in {LANE}/corpus/lessons/round-24-verifier-spotcheck.md:61-67 (items 1-5) to round-25 handling at {REV} '
    '(C1 item, C2, or not handled). For each not handled, state whether the report must say why. Do not propose new work beyond naming it.')
add('ProvinceMove', 'reviewer', ['coverage'],
    f'Review the planned frontier move: F1 (report interop) in {LANE}/corpus/README.md:78,111-114 and PROVINCE.md Core rules (lines 40-42: ground moves '
    'to Core only through an admitted source-headed knowledge entry whose source cites a mined SOURCES row). What exactly must land this round for F1 '
    'to be "held" rather than "partly held"? Which F1 parts (NoCoverage candidates) stay open?')
add('NoHarmMonitor', 'executor', ['calibration'], CLONE +
    f'Run the lane no-harm monitors at REV in your clone: `bash tools/mutate-and-run.sh --selftest` (last lines), '
    '`python3 tools/command-binding.py --selftest` (last line), `python3 tools/registry-check.py --help` then its documented check against your clone, '
    f'and the round-21 strict monitor (find its command in {LANE}/.ufo/evidence/round-24/landing-verification.json). Report exits and summary lines.')
add('CensusRun', 'executor', ['coverage'],
    f'Run read-only: `{FLEET}/scripts/sources-census.sh validate --root {FLEET} tameshi` and report exit code and every non-ok line. Do not modify anything.')
add('C2Determinism', 'executor', ['coverage'], CLONE +
    f'Run: `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root {FLEET} --emit /tmp/<your-name>-a` '
    'and again with `--emit /tmp/<your-name>-b`; compare every emitted file byte-for-byte (cmp) and report exits and any difference.')
add('C2HtmlRender', 'executor', ['coverage'], CLONE +
    'Run: emit the reports with --emit, then check that one report loads in the official mutation-testing-elements web component or its '
    'documented CLI/HTML path (npm package mutation-testing-elements; read its README first). If no headless check is possible, say so and why. '
    'Report what ran and what it showed.')
add('C1RestoreBlob', 'reviewer', ['calibration'], CLONE +
    'Run both C1 sweeps through c1-measure.py in your clone, then compare the pristine sha256 printed by MUTATE_TARGET/MUTATE_RESTORE with '
    '`git show REV:tools/command-binding.py | sha256sum`. Do they match the committed blob? Is the gate under test the committed one?')
add('QualityCriterion', 'critic', ['calibration'],
    f'Read {LANE}/corpus/QUALITY.md criteria 12, 44 and 48 and the round-24 spot-check lines 34-37. Draft one new criterion (text + falsifier) '
    'that would have refused round 24 dropping three routed items, and say whether the round-25 c1-measure population would fail it. Draft only.')
add('SpotRouting2', 'reviewer', ['calibration'],
    f'Routing items 2-4 of {LANE}/corpus/lessons/round-24-verifier-spotcheck.md:64-66 (ruler output contract registration, MutPins survivors, '
    'registry-replay docstring promises) are not claimed this round. At revision ' + REV + ' check each: still open, partly handled, or '
    'handled elsewhere? Give path:line evidence so the report can say why each is deferred.')

print(len(items))
spec = {'wave': 'round-25-w1', 'reportDir': W, 'context': CONTEXT, 'items': items}
Path(LANE + '/.ufo/waves/round-25/spec.json').write_text(json.dumps(spec, indent=1) + '\n')
