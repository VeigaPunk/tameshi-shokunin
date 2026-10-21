#!/usr/bin/env python3
"""Generate the round24 falsification wave spec (64 distinct items)."""
import json
from pathlib import Path

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = 'c8c5b88c8e961a929cdc351b95a7074c76958909'
BASE = '6a1821a8897eea6e7d9669292160ec9593669409'
E = LANE + '/.ufo/evidence/round-24'
DIRECTIVE = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text()
CLONE = ('Create your own private clone: `git clone -q --no-hardlinks %s /tmp/<your-name>-r24 && '
         'git -C /tmp/<your-name>-r24 checkout -q --detach <REV>` and run commands only there. ') % LANE

CONTEXT = f"""# Goal
Tameshi round24 C1 calibration: harden required-command binding against eleven frozen predicates
(contract {E}/contract.json, ruler {E}/measure.py, before {E}/before.json: 1/11 at base {BASE}).
Delivered implementation revision for this wave: {REV}. L1 CloseTameshi22 is the sole production integrator and planner.
New/changed surfaces: {LANE}/tools/registry-replay.py (new), {LANE}/tools/command-binding.py (selftest loads a second fixture file),
{E}/extra-cases.json, {LANE}/tools/registry.json (three round23 rows superseded by pinned/updated successors plus registry-replay-selftest),
{LANE}/corpus/knowledge/replay-projection-hardening.md, {LANE}/corpus/lessons/round-24.md, QUALITY48, SKILL.md round24 addition, SOURCES S084/S085,
actual replay {E}/replay/ (+ replay-command.json, replay-gate.json), fifteen source re-anchors {E}/source-refresh-*.json.
# Bounds (binding)
- Fresh falsification: attack what your item names; report defects with a concrete counterexample, or say none found and what you checked.
- Write NOTHING except your own report file. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>, and nowhere else (never the fleet root).
- Never edit production files, never run git/jj write commands (add/commit/checkout/reset/stash/push/fetch, any mutating jj) in {LANE}; never touch the fleet repo /home/vgpnk/Projects/shokunin outside your report, sibling lanes, lane jj state or Git index. Read-only git (show/log/diff/cat-file/rev-parse) with GIT_OPTIONAL_LOCKS=0 is fine.
- Only items that explicitly say "Run" may execute commands beyond read-only inspection, and only inside their own /tmp clone. Never run the registry battery, gates or selftests in {LANE} itself.
- No seat spawns; executors may spawn at most one read-only labrat probe for a falsifiable hypothesis.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate, record tool/version/channel/reason in your report). Pacman guard: all pacman transactions are PAUSED host-wide; install via uv tool/npx/an official binary in ~/.local/bin, never -Sy/-Syu/-U/-R, never restart a host service.
- Do not claim producer authentication, promotion, historical R17-CMD-BIND closure or numeric score uplift.
- Final answer: verdict first, then evidence (paths:lines, commands with observed output), then smallest safe correction."""

items = []


def add(name, role, target, acceptance):
    prompt = ('/skill:godspeed\n' + DIRECTIVE + '\n# Target\n' + target + '\n\n# Acceptance\n' + acceptance + '\n')
    items.append({'name': name, 'role': role, 'axes': ['calibration'], 'prompt': prompt})


PRED = {
    'K1': 'argv name-insensitive mutant killed by `tools/command-binding.py --selftest` (fixture argv-swapped-between-names)',
    'K2': 'argv case-fold mutant killed (fixture argv-case-only)',
    'K3': 'negative-exit-ignored mutant killed (fixture negative-exit-mismatch)',
    'K4': 'stdout any-token mutant killed (round23 all-of-tokens control, already killed at base)',
    'K5': 'frozen-clean registry row fails when the replay bundle is substituted by another valid bundle with regenerated expected',
    'K6': 'source-read-red registry row fails when its red bundle is substituted by another self-consistent red bundle',
    'K7': 'registry-replay --project refuses RUNNER_NOT_HELD and writes no bundle',
    'K8': 'registry-replay --project refuses RUNNER_CLEANUP_FAILED',
    'K9': 'registry-replay --project refuses STREAM_LIMIT under --max-stream-bytes',
    'K10': 'registry-replay lists external/non_hermetic rows in live_dependent while still publishing',
    'K11': 'registry-replay --plan realpath-normalises repo, fleet root and siblings',
}
for key, text in PRED.items():
    add('Pred' + key, 'reviewer' if key in ('K1', 'K2', 'K3', 'K5', 'K6', 'K7') else 'critic',
        f'Attack frozen predicate {key}: {text}. Read {E}/measure.py (its {key} code path), {E}/contract.json, '
        f'{E}/before.json and the implementation it exercises at {REV}. Can {key} pass vacuously, pass for the wrong '
        f'reason, or fail to discriminate a plausible weaker implementation? Is the base result in before.json honest?',
        f'Report: .ufo/waves/round-24/w1/Pred{key}.md with verdict, counterexample or explicit none-found.')

runs = [
    ('RunRulerAfter', f'Run `python3 {E}/measure.py --repo /tmp/<clone>` with the clone at REV={REV}. Report discriminated/total, exit and each row.'),
    ('RunRulerBase', f'Run the same ruler with a second clone at REV={BASE}. Confirm before.json (1/11, exit1, only K4) or report the difference.'),
    ('RunSelftests', f'At REV={REV} run `python3 tools/command-binding.py --selftest` and `python3 tools/registry-replay.py --selftest` inside the clone. Report summary lines and exits.'),
    ('RunReplayGate', f'At REV={REV} run `python3 tools/command-binding.py --bundle .ufo/evidence/round-24/replay/bundle.json --expected .ufo/evidence/round-24/replay/expected.json --json` and the two round23 pinned-row argv pairs from tools/registry.json. Report exits and digests.'),
    ('RunRegistry', f'Run `python3 {LANE}/tools/registry-check.py --root /tmp/<clone> --rev {REV} --json` against your clone (its --rev mode makes a throwaway fleet mirror). Report held/total/superseded, exit, and any row not held.'),
    ('RunMonitor', f'Run `python3 {LANE}/.ufo/evidence/round-21/coldread/measure.py --repo {LANE} --rev {REV}` (read-only, revision-addressed). Report sections_covered/total, calibration_restraint_score, depth_score, overrides_used, trace_gate.'),
    ('RunR23Ruler', f'No-harm: at REV={REV} run `python3 .ufo/evidence/round-23/measure.py --repo /tmp/<clone>` (round23 ten-case ruler). Report discriminated/total and exit; it must still be 10/10.'),
    ('RunSourcesCount', f'Run `git -C {LANE} show {REV}:corpus/SOURCES.md` and count S-rows, tiers, statuses and malformed rows (11 cells); compare with base {BASE}. Report exact counts and added ids.'),
]
for name, text in runs:
    add(name, 'executor', CLONE + 'Run: ' + text, f'Report: .ufo/waves/round-24/w1/{name}.md with exact argv, cwd, exit and decisive output lines.')

mutants = [
    ('MutProject', 'Mutation-test the guards of `project()` in tools/registry-replay.py one at a time (held check, cleanup check, stream bound, live_dependent, invalid-input checks) against `--selftest` and the round24 ruler K7-K10, in your own /tmp copy only. Report killed/survived per mutant with outputs.'),
    ('MutPlan', 'Mutation-test `plan()` in tools/registry-replay.py (drop realpath on repo, drop realpath on siblings, include self in siblings) against `--selftest` and ruler K11 in a /tmp copy. Report killed/survived.'),
    ('MutFixtures', 'In a /tmp copy, try further argv/exit comparison weakenings of tools/command-binding.py beyond K1-K3 (strip tokens, dedupe flags, prefix match, abs(exit), exit truthiness) against the 44-case selftest. Report survivors with exact mutant text.'),
    ('MutPins', 'In a /tmp copy, weaken the pinned registry rows (drop the bundle_sha256 token, change one hex digit, revert to the superseded row) and run ruler K5/K6 plus `tools/registry-check.py --only` on those rows. Report whether each weakening is detected.'),
]
for name, text in mutants:
    add(name, 'mutation-tester', CLONE.replace('<REV>', REV) + text, f'Report: .ufo/waves/round-24/w1/{name}.md.')

code_reviews = [
    ('CodeRunReplay', f'Review `run_replay()` in {LANE}/tools/registry-replay.py: clone HEAD check, sibling symlink set from plan(), runner digest from the clone copy, observations content. Compare against {E}/replay/observations.json and the round23 instrument {LANE}/.ufo/evidence/round-23/replay.py.'),
    ('CodeProjectInputs', 'Review `project()` input validation: malformed rows, non-string streams, missing requirement name, duplicate names, non-int got, bool held. Find an input that publishes a bundle it should refuse or crashes instead of exit 2.'),
    ('CodePublish', 'Review `publish()` and the CLI exit/usage map of tools/registry-replay.py against the SKILL.md round24 registry row. Look for writes outside --out, partial bundles on refusal, stale files from a previous run in the same --out.'),
    ('CodeSelftestOracle', 'Review the literal-oracle independence of tools/registry-replay.py `--selftest` and the new round24 fixtures in tools/command-binding.py selftest: do expected outcomes derive from the code under test?'),
    ('CodeFixtureLoader', 'Review the command-binding.py selftest change that loads round-23 and round-24 extra-cases.json: missing file behaviour, ordering, duplicate case names, and whether the round23 38-case evidence remains interpretable.'),
    ('CodeSupersession', f'Review tools/registry.json supersession: three round23 rows now superseded with superseded_by; four new rows. Check registry-check.py semantics (superseded rows still run, do not count to held) and whether the superseded 38/38 row now failing is honest and disclosed. Compare git show {BASE}:tools/registry.json.'),
    ('CodeAnchors', 'Validate the `source` anchors of the four new registry rows (fresh-adjudication.json@6a1821a:53-59, :66, :74-93): do those lines exist at that revision and support each row?'),
    ('CodeLiveList', f'Check that {E}/replay/live-dependent.json and the replay report list exactly the rows that are external in the source registry or carry runner non_hermetic_argv in {E}/replay/observations.json; find any row reading live fleet state not listed.'),
]
for name, text in code_reviews:
    add(name, 'reviewer', text, f'Report: .ufo/waves/round-24/w1/{name}.md.')

corpus = [
    ('CorpusEntry', f'Attack {LANE}/corpus/knowledge/replay-projection-hardening.md for overclaims (authentication, isolation, mutation adequacy), provenance trio correctness and S084/S085 citation.'),
    ('CorpusLesson', f'Attack {LANE}/corpus/lessons/round-24.md: Claims, Gate admit/reject decisions, Mistakes row (captured-by, fix shown able to fail, evidence pointers resolve).'),
    ('CorpusQuality48', f'Attack QUALITY48 in {LANE}/corpus/QUALITY.md: is it lesson-backed, grounded, falsifiable, and consistent with QUALITY46/47?'),
    ('CorpusSkill', f'Attack the SKILL.md round24 addition (end of {LANE}/SKILL.md): registry-row fields complete per PROTOCOL Gate standard registry schema, verdict map vs actual exits, write scope honesty.'),
    ('CorpusScorecard', f'Attack the SCORECARD.md round24 section and capability row: falsifiable before->after, frozen before dispatch (commit e338f1bd0749a1786d95d3d3cd9572bb10757667 precedes this wave), numeric score not inflated, capability demonstrated.'),
    ('CorpusReadme', f'Attack the corpus/README.md round24 index row and verify every claim in it exists at {REV}.'),
    ('CorpusContract', f'Attack {E}/contract.json bounds: is K4-as-control honest, are the eleven predicates distinct mechanisms, do bounds disclaim what the ruler cannot show?'),
    ('CorpusErrataCarry', 'Check that round23 Errata A-D and QUALITY47 limits (instrument-supplied argv/cwd/revision, 41+2 rows, bundle-declared requirements) are preserved and not contradicted by any round24 text.'),
]
for name, text in corpus:
    add(name, 'critic', text, f'Report: .ufo/waves/round-24/w1/{name}.md.')

add('SourceS084', 'scout', 'Reopen https://docs.python.org/3/library/os.path.html#os.path.realpath. Verify the S084 row quote and scope in corpus/SOURCES.md and the lesson Gate; confirm the non-strict caveat.', 'Report: .ufo/waves/round-24/w1/SourceS084.md: agree/disagree with reason.')
add('SourceS085', 'scout', f'Reopen `git -C {LANE} show {BASE}:.ufo/waves/round-23/fresh-adjudication.json` lines 53-104; verify the S085 quote (line 66) and scope.', 'Report: .ufo/waves/round-24/w1/SourceS085.md: agree/disagree with reason.')
add('SourceCensus', 'scout', f'Statically check that rows S084/S085 have 11 cells, allowed kind/tier/status values, existing used-by paths, and that no existing row changed between {BASE} and {REV} (git diff of corpus/SOURCES.md).', 'Report: .ufo/waves/round-24/w1/SourceCensus.md.')

for name, text in [
    ('OverlapKagi', 'Sibling-overlap scan: does /home/vgpnk/Projects/shokunin/kagi-shokunin (read-only) own registry/replay hardening or digest-pinned rows that this round absorbs? Name contested scope, if any.'),
    ('OverlapKumitate', 'Sibling-overlap scan of /home/vgpnk/Projects/shokunin/kumitate-shokunin (read-only) for gate-registry/replay tooling overlapping tools/registry-replay.py.'),
    ('OverlapKama', 'Sibling-overlap scan of /home/vgpnk/Projects/shokunin/kama-shokunin and /home/vgpnk/Projects/shokunin/mori-shokunin (read-only) for command-receipt or wave-accounting overlap.'),
    ('ProvinceFit', f'Check {LANE}/PROVINCE.md core/frontier/adjacent against the round24 additions: does the new tool stay inside verification-fixture craft?'),
    ('PlanWalk', f'Planning data-walk: list every routed round23 defect in {LANE}/.ufo/waves/round-23/fresh-adjudication.json and map each to a round24 predicate, a non-predicate change, or still-open; flag anything silently dropped.'),
    ('ClosureCarry', 'Map every routed item in the round23 closure (MANIFEST.json rounds[421] notes, read-only via `python3 -c` JSON parse of /home/vgpnk/Projects/shokunin/MANIFEST.json) to round24 handling; flag any unaddressed item (e.g. multi-token stdout fixture in the ruler, guard sweep re-run).'),
]:
    add(name, 'connector', text, f'Report: .ufo/waves/round-24/w1/{name}.md.')

for name, text in [
    ('RevBundleDiff', f'Reverse-engineer differences between {LANE}/.ufo/evidence/round-23/replay/bundle.json and {E}/replay/bundle.json row by row (exit, stdout tokens, argv); explain each difference or flag it.'),
    ('RevLiveRows', f'Establish from source code (verify.py, pin-disposition probe) which replay rows actually read live fleet paths; compare with live_dependent in {E}/replay/live-dependent.json.'),
    ('RevRunnerHash', f'Verify {E}/replay/observations.json runner_sha256_clone_copy equals the blob of tools/registry-check.py at the replay revision and states which copy ran.'),
]:
    add(name, 'revenger', text, f'Report: .ufo/waves/round-24/w1/{name}.md.')

add('SentinelRun', 'sentinel', 'Security review of `tools/registry-replay.py --run`: writes outside --out, sibling symlink exposure, stream retention and secrets, environment scrubbing. Static only.', 'Report: .ufo/waves/round-24/w1/SentinelRun.md.')
add('ScribeLimits', 'scribe', 'From the round24 contract, knowledge entry and lesson, draft (in your report only) a plain-language list of what the eleven predicates do NOT show, for the L1 report. Cite each source line.', 'Report: .ufo/waves/round-24/w1/ScribeLimits.md.')
add('SimplifyReplay', 'simplifier', 'YAGNI review of tools/registry-replay.py: identify dead code, duplicate logic with the round23 instrument, or options without a test. Static only; propose deletions preserving verified behaviour.', 'Report: .ufo/waves/round-24/w1/SimplifyReplay.md.')
add('LabStreamBytes', 'executor', CLONE.replace('<REV>', REV) + 'Hypothesis: STREAM_LIMIT counts UTF-8 bytes, not characters. Run `--project` on a fixture whose stdout has 5 three-byte characters with --max-stream-bytes 12 and 15.', 'Report: .ufo/waves/round-24/w1/LabStreamBytes.md with observed exits.')
add('LabPlanLaneLink', 'executor', CLONE.replace('<REV>', REV) + 'Hypothesis: if the lane directory itself is reached through a symlink, `--plan` still excludes the lane from siblings. Build a /tmp fixture and run `--plan --json`.', 'Report: .ufo/waves/round-24/w1/LabPlanLaneLink.md with observed output.')

rows = [r['name'] for r in json.loads(Path(LANE + '/.ufo/evidence/round-24/replay/bundle.json').read_text())['receipts']]
groups = [rows[i::8] for i in range(8)]
for i, group in enumerate(groups, 1):
    add('RowAudit%02d' % i, 'scout',
        f'Row audit of the round24 replay for rows {", ".join(group)}: compare requirement vs {LANE}/.ufo/evidence/round-23/requirements.json, '
        f'receipt vs {E}/replay/observations.json runner_result (exit, full stdout, held), and stdout tokens present. Flag any false acceptance.',
        f'Report: .ufo/waves/round-24/w1/RowAudit{i:02d}.md.')

spec = {'wave': 'tameshi-r24-w1', 'reportDir': '.ufo/waves/round-24/w1', 'maxLanes': 100, 'context': CONTEXT, 'items': items}
Path(LANE + '/.ufo/waves/round-24/spec1.json').write_text(json.dumps(spec, indent=1, ensure_ascii=False) + '\n')
from collections import Counter
print(len(items), Counter(i['role'] for i in items), len({i['name'] for i in items}))
