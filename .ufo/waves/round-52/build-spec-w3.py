#!/usr/bin/env python3
"""Build round-52 wave 3 (fresh cold-read readers of the 19 dropped sections at CAND1 + final falsifiers)."""
import json, os, subprocess
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
E = LANE + '/.ufo/evidence/round-52'
W2 = LANE + '/.ufo/waves/round-52/w2'
W = LANE + '/.ufo/waves/round-52/w3'
SCR = '/fast/scratch/hyaku/tameshi-r52'
P = 'T52W3'
BASE = 'ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4'
CAND = '7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135'
HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = json.load(open(HERE + '/spec-w1.json'))['template']
lost = [l.split(' | ')[0][5:] for l in open(E + '/integrate/precheck-cand1.stdout') if l.startswith('LOST ')]
assert len(lost) == 19, lost
skill = subprocess.run(['git', '-C', LANE, 'show', CAND + ':SKILL.md'], capture_output=True, text=True, check=True).stdout.split('\n')

CONTEXT = f'''# Goal
tameshi round 52 (hyaku run 9; L1 TameshiR52), wave 3 of 3 (fresh cold-read readers + final falsifiers). Lane repo {LANE}. Base `{BASE}`; content candidate CAND1 `{CAND}` (lane branch tip). Counters frozen at `acc27abe9b155e165d282d4bb7f821317ba1e7a1`, amendment 1 `8827f3191393e14e7d3066368ce5558e92a12f47` (controls harness only); controls 11/11 as pre-registered. Read {E}/contract.json and {LANE}/corpus/lessons/round-52.md first; never edit them.

Claims: C1 operability (registry homes; counter {E}/c1/measure.py), C2 calibration (closure-found false records; counter {E}/c2/measure.py). The round's edits dropped 19 SKILL.md sections from the round-21 cold-read monitor's credit ({E}/integrate/precheck-cand1.stdout). Wave 2 drafted in-line fixes for stale statements in them; the L1 applied 59 ({E}/integrate/apply-fixes.stdout, apply-fixes-pass2.stdout). This wave's readers re-read the fixed bytes; a section is re-keyed with EXACTLY the findings its reader records (no selection by the L1), and the monitor credits it only if the reader records none. Readers must be honest: a stale statement you find is a finding even if it costs credit.

You are a seat: you produce findings and the deliverable files your item names. You never decide a claim. Run counters only as `--selftest` or against scratch clones into scratch work dirs; a probe is never a verdict.

Bounds for every seat: READ-ONLY on the lane checkout except your own report file and deliverables (always inside {W}). Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Never edit /home/vgpnk/Projects/shokunin (the fleet repo), a sibling lane (read-only: `git -C <repo> show <rev>:<path>`), anything under /home/vgpnk/Projects/shokuknow, the lane's jj state or Git index. Never run git add/commit/stash/checkout/switch/reset/pull/push or any mutating jj command in the lane or the fleet repo. Fixture repos: `git clone --shared {LANE} "$S/clone"`, every later git call names `-C` that path, `rev-parse --show-toplevel` must equal it before the first fixture commit. Never message agent://all.

Scratch (operator directive 2026-10-25): your scratch root is {SCR}/<your seat name>/ — `S={SCR}/<your seat name>; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT`, pass it explicitly (TMPDIR="$S", --work "$S/w"), never write under /tmp beyond small files, one live clone at most, copy receipts you cite into {W} before you finish, delete your scratch dir before you yield. A /tmp or scratch path is never citable evidence.

Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first, official channels only, and record tool/version/channel/reason in your report. pacman guard: ALL pacman transactions are PAUSED host-wide (no -S, -Sy, -Syu, -U, -R, no downgrade, no service restart); install via uv tool / npx / an official binary in ~/.local/bin instead.

Report: every finding names file:line and the command that shows it. End your report with a `## Summary` of at most 8 lines.
'''

ITEMS = []
def add(name, role, axes, milestone, text):
    ITEMS.append({'name': P + name, 'role': role, 'axes': axes, 'milestone': milestone, 'item': text})

for i, h in enumerate(lost, 1):
    start = skill.index(h) + 1
    add('Read%02d' % i, 'reviewer', ['calibration'], 'cold-read re-key reader',
        f'''Cold-read the SKILL.md section headed exactly `{h}` at CAND1 `{CAND}` (heading at line {start}; the section runs to the next heading of level 1-3; `git -C {LANE} show {CAND}:SKILL.md | sed -n '{start},$p'`). Read every statement and open every pointer it makes into lane files (tools, corpus, .ufo/evidence, other SKILL.md lines) at CAND1 bytes (`git -C {LANE} show {CAND}:<path>`). Do not rely on earlier reader files or fix drafts. A finding is a statement of the section that does NOT hold at CAND1: false, stale/moved pointer, stale count, unsupported premise. Dated history that is accurately dated is not a finding. In your report {W}/{P}Read{i:02d}.md write a `## Findings` list with ONE line per finding, beginning `- F<n>:` and quoting the section text; then a `## Holds` list with the pointers you checked that hold (count them). Deliverable {W}/{P}Read{i:02d}.json = {{"heading": "{h}", "cand": "{CAND}", "section_sha256": <sha256 of the section text you read, lines joined by \\n>, "findings": [{{"quote": <the exact `- F<n>: …` line copied byte-for-byte from your .md>, "class": ..., "skill_statement": ...}}], "holds_checked": <int>}}. If you find nothing failing, "findings" is [] — say so explicitly in the report.''')

hunks = ['Fix01-Fix05', 'Fix06-Fix10', 'Fix11-Fix14', 'Fix15-Fix18 and pass 2']
for k, rng in enumerate(hunks, 1):
    add('RevApplied%d' % k, 'reviewer', ['calibration'], 'applied fix falsifier',
        f'''Attack the applied in-line SKILL.md fixes for {rng}: the APPLY lines in {E}/integrate/apply-fixes.stdout and apply-fixes-pass2.stdout name each fix (seat, line, old -> new); the drafts with evidence are {W2}/T52W2FixNN.json. For each applied replacement in your range, check at CAND1 `{CAND}` that the new text is true (open the cited file:line), that it changed only what was stale, and that dated history was qualified rather than rewritten. Report per replacement: true / false / overreach, with the command. Also list any REFUSE/LEAVE2 item in your range that left a stale statement standing. Deliverable {W}/{P}RevApplied{k}.md.''')

add('ExecC1Probe', 'executor', ['operability'], 'C1 probe at CAND1',
    f'''Run the frozen C1 counter once at CAND1 as a probe (non-deciding): `S={SCR}/{P}ExecC1Probe; mkdir -p "$S/w"; HYAKU_SCRATCH="$S" TMPDIR="$S" python3 {E}/c1/measure.py --lane {LANE} --rev {CAND} --work "$S/w" --explain`. Copy stdout to {W}/{P}ExecC1Probe.stdout and registry-check.stdout + c3.stdout from the work dir into {W}/{P}ExecC1Probe/. Report every row not held and every C3 MISSING line with its cause.''')
add('ExecNoHarm', 'executor', ['calibration', 'depth', 'freshness', 'operability'], 'no-harm + C2 probe at CAND1',
    f'''At CAND1 `{CAND}`: run `HYAKU_SCRATCH=$S bash {E}/no-harm.sh {LANE} {CAND}` and `python3 {E}/c2/measure.py --lane {LANE} --rev {CAND} --explain`, and the census `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch copy of CAND1 corpus/SOURCES.md>`. Copy outputs to {W}/{P}ExecNoHarm-*.out. The coldread-floor monitor is expected RED until the re-key lands (19 sections); report every other monitor and any RED with cause.''')
add('MutRefresh', 'mutation-tester', ['calibration'], 'refresh refusals',
    f'''Mutation-test the round-52 re-key instrument {W2}/../w1/T52W1ExecRefresh/refresh.py on scratch copies (it will be committed as {E}/coldread/refresh.py). Mutants: drop the verbatim-quote check; accept a reader file absent at CAND; write wrong_expectations 0; ignore findings for one heading; skip the trace-cleanliness refusal. For each, build a scratch-clone case (fixture commits in the clone only) where the pristine instrument refuses and the mutant writes a ledger entry. Report KILLED/SURVIVED and whether the frozen C2 m6 check would catch the mutant's output. Deliverable {W}/{P}MutRefresh.md.''')
add('CritAdmission', 'critic', ['operability', 'calibration'], 'claim admission review',
    f'''Adversarial admission review at CAND1 `{CAND}`: read {E}/contract.json, both counters, {E}/control/controls.stdout, {LANE}/corpus/lessons/round-52.md, the SCORECARD round-52 block and wave-2 findings (especially {W2}/T52W2RevCorr*.md, T52W2MutC1Survivors.md, T52W2MutC2Followup.md, T52W2ExecC1Probe.md). Would either claim verify only through a forgery or a narrowed reading? Is C2 a calibration move by the prompt's sizing rules (counts mismatches between lane records and the tree)? Is "no axis harmed" plausible given the re-key (19 sections must be re-credited by honest readers)? Name each risk with a pointer. Deliverable {W}/{P}CritAdmission.md.''')
add('CritRound26', 'critic', ['calibration', 'operability'], 'round-26 registry section second read',
    f'''The wave-2 fix-read seat for `### Round-26 gate/probe registry — report interop` died with no deliverable, so that section (SKILL.md at CAND1, from the heading to EOF: 30+ registry rows) got only the L1's partial fixes. Independently of its wave-3 reader, check every row's statements (kind, verdict map, self-test command and finding id, pinned values, write scope) against the tools at CAND1, prioritising write-scope claims (hard-coded /tmp vs TMPDIR, __pycache__ writes, lane writes) and counts. Deliverable {W}/{P}CritRound26.md with one line per false statement and its evidence.''')
add('RevQuality', 'reviewer', ['calibration'], 'QUALITY 103 + mistakes',
    f'''Review {LANE}/corpus/QUALITY.md criterion 103 (round-52 block at the end) and {LANE}/corpus/lessons/round-52.md `## Mistakes`: each row has class, evidence pointer, captured-by and a fix shown able to fail. Open every cited receipt at CAND1 and confirm the red/green values quoted. Flag any fix that is a note rather than a check. Deliverable {W}/{P}RevQuality.md.''')
add('RevGate', 'reviewer', ['coverage'], 'S274 row + lesson Gate',
    f'''Review the S274 row in {LANE}/corpus/SOURCES.md at CAND1 and the lesson `## Gate` against /home/vgpnk/Projects/shokunin/CORPUS.md section "SOURCES.md — where a shokunin learns": 11 columns, tier/kind, opened date, recheck form, used-by resolvable, ≤25-word located quote recorded with URL and access date, at least one rejected candidate with reason and flip. Re-fetch https://bazel.build/basics/hermeticity.md and confirm sha256 and both quoted sentences. Run the census validator on a scratch copy. Deliverable {W}/{P}RevGate.md.''')
add('ScoutMisroot', 'scout', ['operability'], 'misroot sweep preview',
    f'''Read-only misroot sweep preview: run `git -C /home/vgpnk/Projects/shokunin status --porcelain` and list untracked files at the fleet root whose content names tameshi, round 52 or a T52 seat name (grep -l). For each, give path, size, the seat that wrote it and whether an identical copy exists in {LANE}/.ufo/waves/round-52/. Never move, delete or edit anything. Deliverable {W}/{P}ScoutMisroot.md.''')
add('ConnShonen', 'connector', ['calibration'], 'SHONEN evidence map',
    f'''Map each box of {LANE}/SHONEN.md to the round-52 evidence that bears on it (contract, controls, lesson, wave receipts) and to round-51's closure note on SHONEN (corpus/lessons/round-51-verifier-spotcheck.md, last paragraph). For each box say what a non-author could check from committed bytes alone, and propose the honest mark ([x] only with a named non-author verifier on record; [~] with a resolvable pointer; [ ] untouched). Deliverable {W}/{P}ConnShonen.md.''')

with open(os.path.join(HERE, 'spec-w3.json'), 'w') as f:
    json.dump({'wave': 'round-52-w3', 'reportDir': '.ufo/waves/round-52/w3', 'template': TEMPLATE,
               'context': CONTEXT, 'items': ITEMS}, f, indent=1, ensure_ascii=False)
print('items', len(ITEMS))
