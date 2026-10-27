#!/usr/bin/env python3
"""Build round-52 wave 2 (fix-reads of the 18 sections the round's edits drop + falsifiers of wave 1), v1 band."""
import json, os, re, subprocess
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
E = LANE + '/.ufo/evidence/round-52'
W1 = LANE + '/.ufo/waves/round-52/w1'
W = LANE + '/.ufo/waves/round-52/w2'
SCR = '/fast/scratch/hyaku/tameshi-r52'
P = 'T52W2'
BASE = 'ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4'
CAND = 'bcba8924894216268afc4171f06eb8c28e912b46'
spec1 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec-w1.json')))
TEMPLATE = spec1['template']

lost = [l.split(' | ')[0][5:] for l in open(E + '/integrate/precheck-cand0.stdout') if l.startswith('LOST ')]
assert len(lost) == 18, lost
skill = subprocess.run(['git', '-C', LANE, 'show', CAND + ':SKILL.md'], capture_output=True, text=True, check=True).stdout.split('\n')
led = json.load(open(LANE + '/.ufo/evidence/round-21/coldread/ledger.json'))
corr = {c['heading']: c for c in led.get('corrections', [])}

CONTEXT = f'''# Goal
tameshi round 52 (hyaku run 9; L1 TameshiR52), wave 2 of 3 (fix-reads + falsifiers of wave 1). Lane repo {LANE}. Base `{BASE}`; content candidate CAND0 `{CAND}` (lane branch tip). Counters frozen at `acc27abe9b155e165d282d4bb7f821317ba1e7a1`, amendment 1 `8827f3191393e14e7d3066368ce5558e92a12f47` (controls harness only); controls 11/11 as pre-registered ({E}/control/controls.stdout). Read {E}/contract.json first; never edit it. Wave 1 returned its deliverables under {W1}.

Claims: C1 operability (every registered row held at REV, mte-interop-check expecting the tool's own leg count, round-51 C3 counter total=0, round21-measure case literals kept; counter {E}/c1/measure.py). C2 calibration (frozen statement set of records the round-51 closure found false; counter {E}/c2/measure.py). At CAND0 the C2 probe prints total=0; C1 is unmeasured at CAND0.

Why this wave: the round's edits (registry row, round21-measure, SKILL corrections, kill-rate-ledger supersession line) drop 18 SKILL.md sections from the round-21 cold-read monitor's credit ({E}/integrate/precheck-cand0.stdout: 64 -> 46). The frozen no-harm floor needs 64. Those sections are re-keyed in wave 3 by fresh readers, and the monitor credits a section only when its reader records zero wrong expectations — and this round records the readers' real counts (C2 m6; routed defect 3 of round 51 was a constant 0). Wave-1 correction records show many of these sections carry stale pointers and counts ({W1}/T52W1Corr*.json). So wave 2 finds and drafts the in-line fixes; the L1 applies them; wave 3 reads the fixed bytes.

You are a seat: you produce findings and the deliverable files your item names. You never decide a claim. Run counters only as `--selftest` or against scratch clones into scratch work dirs; a probe is never a verdict.

Bounds for every seat: READ-ONLY on the lane checkout except your own report file and deliverables (always inside {W}). Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Never edit /home/vgpnk/Projects/shokunin (the fleet repo), a sibling lane (read-only: `git -C <repo> show <rev>:<path>`), anything under /home/vgpnk/Projects/shokuknow, the lane's jj state or Git index. Never run git add/commit/stash/checkout/switch/reset/pull/push or any mutating jj command in the lane or the fleet repo. Fixture repos: `git clone --shared {LANE} "$S/clone"` (or `D=$(mktemp -d -p "$S") && git -C "$D" init -q`), every later git call names `-C` that path, and `rev-parse --show-toplevel` must equal it before the first fixture commit. Never message agent://all.

Scratch (operator directive 2026-10-25): your scratch root is {SCR}/<your seat name>/ — `S={SCR}/<your seat name>; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT` (Python: shutil.rmtree in finally), pass it explicitly (TMPDIR="$S", --work "$S/w"), never write under /tmp beyond small files, one live clone at most, copy receipts you cite into {W} before you finish, delete your scratch dir before you yield. A /tmp or scratch path is never citable evidence.

Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first, official channels only, and record tool/version/channel/reason in your report. pacman guard: ALL pacman transactions are PAUSED host-wide (no -S, -Sy, -Syu, -U, -R, no downgrade, no service restart); install via uv tool / npx / an official binary in ~/.local/bin instead.

Report: every finding names file:line and the command that shows it. End your report with a `## Summary` of at most 8 lines.
'''

ITEMS = []
def add(name, role, axes, milestone, text):
    ITEMS.append({'name': P + name, 'role': role, 'axes': axes, 'milestone': milestone, 'item': text})

for i, h in enumerate(lost, 1):
    start = skill.index(h) + 1
    c = corr.get(h)
    known = (f' Known candidates: the round-52 correction record for this heading in the ledger\'s "corrections" list ({c["source"]}: {len(c["findings"])} findings recorded by round-51 reader {c["reader"]}, {LANE}/{c["reader_file"]}); some may already be fixed at CAND0.'
             if c else ' No earlier reader record exists for this section; read it fresh.')
    add('Fix%02d' % i, 'scribe', ['calibration'], 'section fix-read',
        f'''Fix-read the SKILL.md section headed exactly `{h}` at CAND0 `{CAND}` (heading at line {start}; the section runs to the next heading of level 1-3: `git -C {LANE} show {CAND}:SKILL.md | sed -n '{start},$p'`). Read every statement and every pointer it makes into lane files (tools, corpus/knowledge, .ufo/evidence, SKILL.md lines) against CAND0 bytes, and list each statement that does not hold at CAND0: false, stale or moved pointer (even if the claim holds elsewhere), stale count, unsupported premise.{known} Also see {W1}/T52W1ReviewSkillLines.md (extra stale runner pointers). For EACH failing statement draft one minimal in-line replacement: `old` = an exact substring of ONE line of this section at CAND0 that occurs exactly once in the section, `new` = its replacement on the same line (never add or remove a newline: other files cite SKILL.md line numbers), `evidence` = CAND0 file:line plus the command that shows it, `class`. Dated history stays history: qualify it in place ("nine since round 26, ten since round 51"), never rewrite what an earlier round recorded; when no correct in-line wording exists, append an in-line bracketed note on the same line (" [round 52: … — see <file:line>]"). Do not touch statements that hold. Deliverable {W}/{P}Fix{i:02d}.json = {{"heading": "{h}", "cand": "{CAND}", "replacements": [{{"old": ..., "new": ..., "class": ..., "evidence": ...}}], "holds_checked": <number of statements you checked that hold>, "not_fixable_inline": [...]}} plus the report. Self-check: apply your replacements to a scratch copy of SKILL.md at CAND0 and show `diff` touches only lines inside this section and that the line count is unchanged; paste that diff into the report.''')

groups = [('01', '04'), ('05', '08'), ('09', '12'), ('13', '16'), ('17', '20')]
for a, b in groups:
    add('RevCorr%s%s' % (a, b), 'reviewer', ['calibration'], 'C2 m4 record falsifier',
        f'''Attack the wave-1 correction records T52W1Corr{a}..T52W1Corr{b} ({W1}/T52W1CorrNN.json, now in the ledger's top-level "corrections" list at CAND0 `{CAND}`, {LANE}/.ufo/evidence/round-21/coldread/ledger.json). For each record read its reader file ({LANE}/.ufo/evidence/round-51/coldread/reads/T51W2ReadNN.md) in full and the section at read_rev 02ec217c. Judge each finding: is it a statement the reader recorded as NOT holding (not a "holds", not a disclosed/historical-and-accurate note)? Then search the reader file for failing statements the record missed. Per record report: over-counted findings (with the reader line), missed findings (with the reader line), verdict exact / over / under. The frozen C2 counter cannot see this (contract C2 cannot_see). Deliverable {W}/{P}RevCorr{a}{b}.md.''')

add('RevSource', 'reviewer', ['operability'], 'sourced claim falsifier',
    f'''Re-open the source behind C1's sourced claim yourself: https://bazel.build/basics/hermeticity (wave-1 draft {W1}/T52W1ScribeSource.md and snapshot {W1}/T52W1ScribeSource-snapshot.txt). Fetch it now, record HTTP status, byte count, sha256, and locate each quote the draft proposes (≤25 words, verbatim after whitespace normalisation). Check the drafted S274 row against {LANE}/corpus/SOURCES.md's header and /home/vgpnk/Projects/shokunin/CORPUS.md section "SOURCES.md — where a shokunin learns" (11 columns, tier/kind fit, no pipe in a cell, recheck form, used-by). Then judge the lesson text's use of the source: does Bazel's definition support calling tools/round21-measure.py's self-test (at CAND0 `{CAND}`, :77-84) "fleet-bound, not hermetic"? Deliverable {W}/{P}RevSource.md with agree/disagree per quote and per claim sentence.''')

add('ExecC1Probe', 'executor', ['operability'], 'C1 probe at CAND0',
    f'''Run the frozen C1 counter once at CAND0 as a probe (non-deciding): `S={SCR}/{P}ExecC1Probe; mkdir -p "$S/w"; HYAKU_SCRATCH="$S" TMPDIR="$S" python3 {E}/c1/measure.py --lane {LANE} --rev {CAND} --work "$S/w" --explain` (expect ~15 min; registry-check writes its clone under /tmp by its own code, note the size). Copy stdout to {W}/{P}ExecC1Probe.stdout and the counter's registry-check.stdout and c3.stdout from the work dir into {W}/{P}ExecC1Probe/. Report every row not held and every C3 MISSING line with its cause. Also run `python3 {LANE}/tools/registry-check.py --root {LANE} --rev {CAND} --only mte-interop-check` and record exit + last lines.''')

add('RevR21', 'reviewer', ['operability'], 'round21-measure fix review',
    f'''Review the landed round21-measure change: `git -C {LANE} diff {BASE} {CAND} -- tools/round21-measure.py` versus the wave-1 patch {W1}/T52W1ExecR21Fix.patch. Check: the FLEET root comes from the subject counter's own literal (no second hard-coded root); all 11 case literals and 13 checks survive; exit codes 0/1/64 unchanged; docstring statement true. Run the selftest at CAND0 from a `git clone --shared` placed outside the fleet root (TMPDIR=$S) and from the lane path; then point a scratch copy of c2-count.py's FLEET at an empty dir and show red. Also check SKILL.md at CAND0 rows that describe this self-test (grep -n round21-measure SKILL.md) for statements now false (e.g. "requires sibling fleet repos at the expected parent"). Deliverable {W}/{P}RevR21.md.''')

add('MutC1Survivors', 'mutation-tester', ['operability'], 'C1 counter survivors',
    f'''Follow up {W1}/T52W1MutC1.md: survivors M05/M06/M19 (base-active drop clause), M14 (C3 digest gate), M20/M21 (label/exit) and the pristine holes it lists (parse_c3 ignores the PASS token; needle list may carry a stale 9/9 beside K/K; LEG_TABLE absent gives a None/None needle). For each, build the cheapest concrete tree (scratch clone of CAND0, fixture commits there only) the PRISTINE frozen counter would wrongly pass, and run only the clauses that matter by importing {E}/c1/measure.py functions (no full registry-check). Classify each: real forgery reachable by a lane edit / unreachable / requires editing frozen evidence (which the deciding script's FROZEN diff would show). Deliverable {W}/{P}MutC1Survivors.md.''')

add('MutC2Followup', 'mutation-tester', ['calibration'], 'C2 counter survivors',
    f'''Follow up {W1}/T52W1MutC2.md and {W1}/T52W1CritC2.md: resolve its inconclusive probes (M07, M13, M15) to KILLED/SURVIVED with a concrete tree, and reproduce the critic's false pass (an unrelated stale nine-leg statement coexisting with C2_R52_PASS=true) on a scratch clone of CAND0. For every survivor say whether the round-52 SKILL.md at CAND0 actually contains such a statement (grep for "nine ledger legs", "9/9", "legs_conforming=9", "/tmp/tameshi-r4-2-regression" across SKILL.md and corpus/knowledge). Deliverable {W}/{P}MutC2Followup.md + mutants under {W}/{P}MutC2Followup/.''')

add('CritRekey', 'critic', ['calibration'], 're-key honesty',
    f'''Attack the round's re-key plan before it runs. Read {W1}/T52W1ExecRefresh.md and its refresh.py ({W1}/T52W1ExecRefresh/refresh.py), the round-21 monitor ({LANE}/.ufo/evidence/round-21/coldread/measure.py: how it treats wrong_expectations, minor_gaps, blocking_gaps and inputs), and the C2 m6 rule. Questions: (1) Can a re-key entry with honest findings ever be credited? (2) What stops the L1 from choosing readers' findings selectively (e.g. dropping a reader's finding to get credit)? Propose the binding the L1 should use (e.g. findings copied mechanically from the reader's JSON block, reader files committed before refresh runs). (3) Does refresh.py bind the read to the exact section sha the readers read? (4) Diff refresh.py against round 51's and flag any weakened refusal. Deliverable {W}/{P}CritRekey.md.''')

add('CritPrereg', 'critic', ['operability', 'calibration'], 'pre-registration integrity',
    f'''Audit pre-registration integrity: freeze `acc27abe`, amendment 1 `8827f319` (controls harness only), controls receipts at `1f72d7d8`, CAND0 `{CAND}`. Check with git that no frozen file in {E}/freeze.json changed after amendment 1 (`git -C {LANE} diff 8827f319 {CAND} -- <each frozen path>`), that the amendment changed no counter byte and was made before any seat ran (compare commit times with {LANE}/.ufo/waves/round-52/w1.ready.dispatched and the first w1 file mtimes), and that the SCORECARD round-52 block states the contract's C1 `before` erratum (prose said total=2; CTL_0 printed 4). Judge whether amendment 1 changed what any control measures in a way that favours the claim. Deliverable {W}/{P}CritPrereg.md.''')

add('RevRouting', 'reviewer', ['adjacency', 'calibration'], 'kill-rate note + kagi routing',
    f'''Review two small landed/drafted texts. (1) The kill-rate ledger supersession block at CAND0 (`git -C {LANE} show {CAND}:corpus/knowledge/fleet-kill-rate-ledger.md | tail -5`) against {LANE}/.ufo/evidence/round-51/c2/sweep/sweep.txt, after/c2.stdout and corpus/lessons/round-51.md: every number and pointer exact? compare with the wave-1 draft {W1}/T52W1ScribeKillNote.md. (2) The kagi cross-domain routing draft {W1}/T52W1ScribeKagiRoute.md against kagi `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh` lines 150-165 and 395-410 and kagi's current HEAD copy. Deliverable {W}/{P}RevRouting.md with exact corrections.''')

add('ConnGate', 'connector', ['operability', 'calibration'], 'recurrence -> gate',
    f'''Turn {W1}/T52W1ScoutRecurrence.md into one QUALITY.md criterion draft for {LANE}/corpus/QUALITY.md (read its last three criteria for format and numbering): the recurring class "a tool's behaviour changed while its registered gate row or SKILL statement did not" (R47.1, R51.1). The criterion must name the check (replay every active tools/registry.json row at the candidate revision with tools/registry-check.py --rev, and diff SKILL.md leg/count statements against the tools), its pass rule, and the lesson pointer `corpus/lessons/round-52.md`. Show it able to fail: cite the base receipt (registry-check at base `{BASE}`: `REGISTRY_CHECK: held=48/49`, {E}/control/C1_CTL_0.stdout) and able to pass ({E}/control/C1_CTL_POSITIVE.stdout). Also connect: which other lanes' closures routed the same class ({W1}/T52W1ConnSibling.md if present). Deliverable {W}/{P}ConnGate.md with the criterion text.''')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec-w2.json'), 'w') as f:
    json.dump({'wave': 'round-52-w2', 'reportDir': '.ufo/waves/round-52/w2', 'template': TEMPLATE,
               'context': CONTEXT, 'items': ITEMS}, f, indent=1, ensure_ascii=False)
print('items', len(ITEMS))
