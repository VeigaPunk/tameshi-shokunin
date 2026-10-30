#!/usr/bin/env python3
"""Build the round-58 wave-2 (v1) spec: fresh attacks on the installed state + the cold-read re-readers.
Run AFTER the content commits land; pass C0 (content-final rev) as argv[1]."""
import json, sys

GODSPEED = """You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '2a32aa8228d5f86a85c81a923a3148bf792a9538'
W2 = LANE + '/.ufo/waves/round-58/w2'
C0 = sys.argv[1] if len(sys.argv) > 1 else 'HEAD'

CONTEXT = f"""# Goal
tameshi round 58 (hyaku run 11; L1 TameshiR58), wave 2 of two (v1: falsify what wave 1 produced and what the L1 installed). Lane repo {LANE}; lane base `{BASE}`; content-final revision C0 = `{C0}` (the newest lane commit at dispatch; verify with git -C {LANE} log --oneline -3). Every path you read, edit or write is ABSOLUTE: seat tools start at the fleet root /home/vgpnk/Projects/shokunin, so a relative `.ufo/...` lands in the FLEET repo. Every `Report:` trailer path the harness renders is relative to {LANE}: write it at {LANE}/<that path>.

# What wave 1 + the L1 installed (attack THIS)
- The routed-defect ledger {LANE}/corpus/routed-defects.json now carries rows for the 51 routed items R50.1–R56.7 (frozen set {LANE}/.ufo/evidence/round-58/c1/defects.json) plus the 49 baseline rows; fix commits land after base and name their item ids.
- tools/registry.json refusal rows now carry the BARE code elements; the strict counter {LANE}/.ufo/evidence/round-58/c2/measure.py must read total=0 at C0.
- corpus/knowledge/llm-mutant-equivalence-cost.md (F9) landed, citing new rows S286/S287; S288 supersedes S285; README F9 row updated.
- The blind round-58 panel {LANE}/.ufo/evidence/round-58/c1/panel.json is pinned (amendment 1); wave-1 seats' outputs are under {LANE}/.ufo/waves/round-58/w1/.

# Deliverables discipline
- Report {W2}/<your-seat-name>.md; machine-readable output beside it {W2}/<your-seat-name>.json; receipts under {W2}/<your-seat-name>-receipts/. NEVER edit a lane file in place; never edit anything under {LANE}/.ufo/evidence/round-5[0-7]/ (read-only prior-round evidence).
- Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r58/<your-seat-name>; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT`; `/tmp` only for files under 50 MB; delete your scratch before you yield and say so.
- Clones: `git clone --shared {LANE} "$S/clone"` then `git -C "$S/clone" checkout --detach <rev>`; every git call names `-C`. NEVER run a mutating git/jj command in the lane or the fleet repo. Fixture repos: `D=$(mktemp -d -p "$S")`, `git -C "$D" init -q`, verify toplevel; commit only with `-c user.name=fixture -c user.email=fixture@example.invalid`.
- Never message agent://all; message only your own L1 (`TameshiR58`) when blocked.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools; first read /home/vgpnk/.omp/agent/RULES.md; record tool/version/channel/reason. All pacman transactions are PAUSED host-wide: install via `uv tool` / `npx` / an official binary in `~/.local/bin`; never pacman transactions, never service restarts.
- An attack that finds nothing must show the sweep it ran (command + output). A finding without a command and its output is not a finding. An unrun check has not passed. Honesty: an unobserved statement is marked INFERENCE.

# Reader contract (seats named T58W2Read*)
You re-read ONE SKILL.md section whose cold-read credit the round's edits drifted. C0 = `{C0}`.
1. Compute your section's sha256 with the FROZEN round-18 sectionize - never reimplement it: a python3 snippet that loads `{LANE}/.ufo/evidence/round-18/measure.py` with importlib, reads `git -C {LANE} show {C0}:SKILL.md`, calls `m.sectionize(raw)` and prints `sec['start'], sec['end'], sec['sha256']` for your heading. Your JSON's `section_sha256` MUST be that value and `cand` MUST be `{C0}`.
2. Read the section end to end as a reader who must act on it: every command must exist and run; every pointer must resolve; every claim must be true of the tree at C0; no contradiction with another section. Work in a scratch clone detached at C0.
3. Write {W2}/<your-seat-name>.json with keys `seat`, `heading`, `cand` (40-hex), `section_sha256`, `section_start`, `section_end`, `findings` (list; only statements FALSE or commands FAILING at C0, each with the command and its output), `notes` (improvements, stale-but-true, style), `commands` (non-empty list), `verdict` (`verified-record` when findings is empty, else `gap-minor`), and the .md report beside it.
4. Do NOT edit SKILL.md: findings are adjudicated by the L1 (fixed in this round where cheap, else recorded and routed). A finding without a command and its output is not a finding.
"""

ITEMS = []


def add(name, role, item, axes=None, milestone=None):
    ITEMS.append({'name': name, 'role': role, 'axes': axes or ['calibration'],
                  'milestone': milestone or '', 'item': item})


# ---- 17 cold-read re-readers ----
HEADINGS = [
    '## Standing rules',
    '## Mutation-sweep recipe — numbered steps; bounded cold-read evidence',
    '## The leg ledger — replay, receipt, and how it is read (round 7, measured)',
    '### Triggers T1–T3 and the re-pin rule',
    "### The service's limits — what tameshi refuses to mutation-test",
    "## The operator's runbook and the six-leg regression (round 10, measured)",
    '### The map — where a reader enters, artifact by artifact',
    '## Repeated controls and gate registry — round 12',
    '### Gate/probe registry',
    '## Pin disposition and provenance correction — round 13',
    '### Round-13 gate/probe registry',
    '## Effective expectation reconciliation — round 14',
    '## Context gate classification and explicit exit classes — round 15',
    '## Live-tree re-pin and entry-command monitor — round 17',
    '### Round-17 gate/probe registry — re-pin and monitor',
    '### Round-18 gate/probe registry — routed-defect closure',
    '### Round-21 gate/probe registry — finite environment differential',
]
if len(HEADINGS) != 17:
    print('HEADING COUNT', len(HEADINGS))
for i, h in enumerate(HEADINGS):
    add(f'T58W2Read{i+1:02d}', 'reviewer',
        'Cold-read re-reader. Heading: `' + h + '`. Follow the Reader contract exactly: '
        'sectionize at C0, read end to end at C0, write {}/T58W2Read{:02d}.json + .md.'.format(W2, i + 1),
        axes=['calibration'], milestone=f're-read {i+1}/17')

# ---- fresh attacks (20) ----
add('T58W2RevRows1', 'reviewer',
    'Row re-verification A. In a scratch clone at C0, re-derive the true tree-supported status for ledger rows '
    'R50.1-R51.8 (ids and rules in {0}/.ufo/evidence/round-58/c1/defects.json + measure.py docstring): does each '
    'row in {0}/corpus/routed-defects.json agree? Check status_at_base coherence at base {1}, the fix commit chain '
    '(ancestor of C0, message names the id or the evidence path), and the keyed excerpt (15-400 chars, in-lines, '
    'whole-token key, absent at routed_at, no ACK_WORDS). Report per-row agree/disagree with commands. '
    'Output {2}/T58W2RevRows1.json.'.format(LANE, BASE, W2),
    axes=['calibration'], milestone='rows R50-R51')
add('T58W2RevRows2', 'reviewer',
    'Row re-verification B: same contract as T58W2RevRows1 for rows R52.1-R53.9. Output {0}/T58W2RevRows2.json.'.format(W2),
    axes=['calibration'], milestone='rows R52-R53')
add('T58W2RevRows3', 'reviewer',
    'Row re-verification C: same contract for rows R54.1-R54.10. Output {0}/T58W2RevRows3.json.'.format(W2),
    axes=['calibration'], milestone='rows R54')
add('T58W2RevRows4', 'reviewer',
    'Row re-verification D: same contract for rows R55.1-R55.7 and R56.1-R56.7. Output {0}/T58W2RevRows4.json.'.format(W2),
    axes=['calibration'], milestone='rows R55-R56')
add('T58W2RevThis', 'reviewer',
    'This-round-floor reviewer. Verify the >=6 post-base fixes the round claims: list every ledger row whose fix commit is NOT an ancestor of base {0} (run the counter term: python3 -I {{1}}/.ufo/evidence/round-58/c1/measure.py --lane {2} --rev <C0> --work <scratch> --explain and read thisround=<n> plus the per-row EXPLAIN lines); then for two of those fixes, re-run the receipt-producing command yourself (e.g. the round-53 counter at 88afa941 in a scratch clone) and confirm the committed receipt matches your output byte-for-byte or semantically. Output {{1}}/T58W2RevThis.json.'.format(BASE, LANE, LANE),
    axes=['calibration'], milestone='this-round fixes')
add('T58W2RevSrc1', 'reviewer',
    'Source re-opener A. Independently fetch https://arxiv.org/abs/2406.09843 (your own curl, record bytes + sha16), locate the Gate quote in the abstract, and compare with the L1 extract {0}/.ufo/waves/round-58/l1/sources/arxiv-2406.09843-abstract.txt and the committed row S286 + entry corpus/knowledge/llm-mutant-equivalence-cost.md: any contradicted number/date/sha is a finding. Output {1}/T58W2RevSrc1.json.'.format(LANE, W2),
    axes=['coverage'], milestone='re-open S286')
add('T58W2RevSrc2', 'reviewer',
    'Source re-opener B. Independently fetch https://pdf.dfcfw.com/pdf/H3_AP202503221646031757_1.pdf, run pdftotext, locate the quotes at your lines 230-241 and compare with the extract {0}/.ufo/waves/round-58/l1/sources/dfcfw-deck.txt, row S287 and the entry. Output {1}/T58W2RevSrc2.json.'.format(LANE, W2),
    axes=['coverage'], milestone='re-open S287')
add('T58W2RevSrc3', 'reviewer',
    'Source re-opener C. Independently fetch the Atlassian page (https://www.atlassian.com/incident-management/handbook/postmortems), locate the severity-2 sentence, and compare with the extract {0}/.ufo/waves/round-58/l1/sources/atlassian-postmortems.txt, the new row S288, and the untouched S285. Verify the supersession shape (CORPUS rule 2: new row, teaches opens supersedes, old row untouched, rejection + flip carried). Output {1}/T58W2RevSrc3.json.'.format(LANE, W2),
    axes=['coverage'], milestone='re-open S288')
add('T58W2CritLedger', 'critic',
    'Ledger install critic. Attack the installed ledger at C0: (a) run the frozen counter python3 -I {{1}}/.ufo/evidence/round-58/c1/measure.py --lane {2} --rev <C0> --work <scratch> --explain - it must print C1_R58_PASS=true total=0 at C0 (if the panel pin amendment landed); (b) name the weakest two rows (evidence that cites the round\'s own receipts circularly, or a fixed row whose excerpt does not resolve the defect semantically) and say what a closure spot-check would find; (c) verify the newest Planned paragraph names every row left open (A5). Output {{1}}/T58W2CritLedger.json.'.format(BASE, LANE, LANE),
    axes=['calibration'], milestone='installed ledger attack')
add('T58W2CritC2', 'critic',
    'C2 installed-state critic. Run the frozen C2 counter at C0 (expect total=0 PASS=true), then attack the registry rows semantically: does each of the three rows\' stdout_contains actually match what the gate prints on its fixture (run the rows via registry-check yourself)? Is any bare-code element trivially satisfiable (a code the gate can never emit on that path)? Output {0}/T58W2CritC2.json.'.format(W2),
    axes=['operability'], milestone='C2 installed attack')
add('T58W2CritC3', 'critic',
    'C3 installed-state critic. At C0: (a) the counting command `grep -rl 2406.09843 corpus/knowledge | wc -l` must print 1 and the S286-S288 row count must be 3; (b) CORPUS rule 4: every appended row is cited by the admitted entry (used-by) and no uncited row was appended; (c) the entry does not overclaim (its boundary section must say the transfer is not measured); (d) the F9 README row matches reality. Output {0}/T58W2CritC3.json.'.format(W2),
    axes=['coverage'], milestone='C3 installed attack')
add('T58W2MutC1', 'mutation-tester',
    'Counter mutation re-check C1. In a scratch clone at C0, apply 4 fresh single-edit mutants to a COPY of {{1}}/.ufo/evidence/round-58/c1/measure.py inside the clone (different sites than wave-1: the old49 comparison, the planned-paragraph regex, the A6 disagreement allowance, the A9 digest compare), score each against the installed ledger, report killed/survived with diffs. Output {{1}}/T58W2MutC1.json.'.format(BASE, LANE),
    axes=['calibration'], milestone='C1 counter mutations 2')
add('T58W2MutC2', 'mutation-tester',
    'Counter mutation re-check C2. Same contract for {{1}}/.ufo/evidence/round-58/c2/measure.py at C0: 4 fresh mutants (the executed arm tally, the cell fixture builder, the codes parser, the verdict-line total). Output {{1}}/T58W2MutC2.json.'.format(LANE),
    axes=['operability'], milestone='C2 counter mutations 2')
add('T58W2RevPanel', 'reviewer',
    'Panel provenance reviewer. Verify amendment 1: {{1}}/.ufo/evidence/round-58/c1/measure.py PANEL_SHA256 equals the sha256 of the committed {{1}}/.ufo/evidence/round-58/c1/panel.json; the panel covers all 51 ids; every detail.seat file exists at C0 under {{1}}/.ufo/waves/round-58/w1/<seat>.json, hashes to panel.files[seat], its verdict matches the panel, and the seat is listed in {{1}}/.ufo/waves/round-58/w1-results.json (A9). Report disagreements >5 if any. Output {{1}}/T58W2RevPanel.json.'.format(LANE),
    axes=['calibration'], milestone='panel provenance')
add('T58W2Sent01', 'sentinel',
    'Write-scope sentinel. Sweep `git -C /home/vgpnk/Projects/shokunin status --porcelain` and the lane repo for seat misroots at the fleet root; verify no seat edited corpus/, SKILL.md, tools/ or prior-round evidence outside the wave dirs; scan wave reports for mutating git/jj commands in the lane or fleet. Output {0}/T58W2Sent01.json.'.format(W2),
    axes=['calibration'], milestone='write scope sweep')
add('T58W2Sent02', 'sentinel',
    'Scratch + hygiene sentinel. df -h /fast; du -sh /fast/scratch/hyaku/tameshi-r58; grep the round-58 instruments and any seat-written tool for hardcoded /tmp; check the new extracts for credential material. Output {0}/T58W2Sent02.json.'.format(W2),
    axes=['operability'], milestone='scratch sweep')
add('T58W2ExecDry', 'executor',
    'Decide-preview executor. In a scratch clone of the lane at C0 (shared clone, detached): run both counters and the no-harm monitors exactly as the deciding run will: python3 -I .ufo/evidence/round-58/c1/measure.py --lane <clone> --rev <C0> --work <scratch> --explain; python3 -I .ufo/evidence/round-58/c2/measure.py --lane <clone> --rev <C0> --work <scratch> --explain; bash .ufo/evidence/round-58/no-harm.sh <clone> {0} <C0> - report all three outputs verbatim plus any RED line. (The bind runs after you; expect coldread-floor RED if your clone predates the bind - report what you see with the commit you measured.) Output {1}/T58W2ExecDry.json.'.format(BASE, W2),
    axes=['operability'], milestone='decide preview')
add('T58W2ConnSib', 'connector',
    'Sibling overlap scan 2. Same contract as wave 1 T58W1ConnSib but for the INSTALLED state: any sibling lane already holding an LLM-mutant/equivalence entry, a routed-defect ledger, or strict registry-code binding that round 58 must cite instead of absorb. Output {0}/T58W2ConnSib.json.'.format(W2),
    axes=['adjacency'], milestone='sibling overlap 2')
add('T58W2ScoutCT', 'scout',
    'considerthese confirmation. Read {0}/considerthese/ (read-only) and confirm the ONE still-unimplemented proposal this round mines (the L1 will name it in the report): verify it is unimplemented with a tree sweep and quote its text verbatim. Output {1}/T58W2ScoutCT.json.'.format(LANE, W2),
    axes=['coverage'], milestone='considerthese confirm')
add('T58W2RevLesson', 'reviewer',
    'Lesson reviewer. Read {0}/corpus/lessons/round-58.md (the round\'s own lesson): its Gate records carry YOUR-verifyable facts (fetch dates, byte counts, shas, located quotes) - re-check two of them against the committed extracts; its Mistakes rows name class/evidence/captured-by/fix; flag anything a closure would call fabricated or unverifiable. Output {1}/T58W2RevLesson.json.'.format(LANE, W2),
    axes=['calibration'], milestone='lesson re-check')

assert 32 <= len(ITEMS) <= 64, len(ITEMS)
from collections import Counter
roles = Counter(i['role'] for i in ITEMS)
attack = roles['reviewer'] + roles['critic'] + roles['mutation-tester'] + roles['labrat']
print('items:', len(ITEMS), 'roles:', dict(roles), 'attack:', attack, '=%.1f%%' % (100 * attack / len(ITEMS)))

spec = {
    'wave': 'round-58-w2',
    'reportDir': '.ufo/waves/round-58/w2',
    'template': '/skill:godspeed\n' + GODSPEED + '\n\n## Your item\n\n{{item}}\n\nWork the item end to end, then write your report file and return your findings.\n',
    'context': CONTEXT,
    'items': ITEMS,
}
json.dump(spec, open('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/spec-w2.json', 'w'), indent=1, ensure_ascii=False)
print('spec written')
