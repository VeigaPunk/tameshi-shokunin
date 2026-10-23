#!/usr/bin/env python3
"""Round 31 (L1 TameshiR31) wave 1: pre-data control wave + build items, policy v1.
Freeze commit FROZEN carries the C1 counter, contract and binding v4 before any data seat."""
import json
from pathlib import Path

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
FROZEN = 'c111dab58b0a8d55e991bbd2efe3aad56717b95a'
BASE = '36c1d3933f680125aeefc447f07db0f03004901a'
E = LANE + '/.ufo/evidence/round-31'
W = '.ufo/waves/round-31/w1'
S = '/fast/scratch/hyaku/tameshi-r31-seats/<your-name>'
DIRECTIVE = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text()
CTR = f'python3 {E}/c1-measure.py'
CLONE = (f'mkdir -p {S} && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks {LANE} {S}/lane '
         f'&& git -C {S}/lane checkout -q --detach {FROZEN}')
CTLRUN = (f'Make your control as ONE sandbox commit in {S}/lane on top of {FROZEN} (`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE '
          f'git -C {S}/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qam <shape>`), then score it with the FROZEN counter, unchanged: '
          f'`timeout 2700 {CTR} --lane {S}/lane --rev HEAD --work {S}/w-<shape>` (a fresh empty --work per run). '
          'Paste the counter\'s full stdout verbatim and its exit code in your report, plus `git -C <clone> diff HEAD~1 HEAD -- SCORECARD.md | head -80`. '
          'Expected for a control: C1_R31_PASS=false. A control that prints C1_R31_PASS=true is a finding: say exactly why.')

CONTEXT = f"""# Goal
Tameshi round 31 (verification-fixture craft), wave 1 (pre-data adversarial controls + build, policy v1). One measured claim, C1, axis calibration.
Surface: the standing self-assessment rows of {LANE}/SCORECARD.md — the `| Capability |` tables (10 capability rows) and the `| Axis | Score (0–10) |` tables
(depth, calibration). Frozen predicate (contract {E}/contract.json, counter {E}/c1-measure.py, both frozen at lane commit {FROZEN}):
"C1 passes at REV iff, for each of the 12 frozen statements, the last row of its frozen table type in the committed SCORECARD.md at REV states values equal to
the values its frozen command prints when run at REV, and the base SCORECARD.md is a byte prefix of REV's SCORECARD.md." Label: C1_R31_PASS.
Before (base {BASE}): `C1_R31: statements=12 mismatches=7 ... C1_R31_PASS=false`, exit 1 ({E}/before/c1-at-base.stdout). Target: mismatches=0, PASS true.
The counter, predicate and target are never changed after the freeze; a control that meets the counter is a finding, not a reason to amend.
Also frozen at {FROZEN}: cold-read binding v4 {E}/coldread/bind-select-v4.py (for this round's drift restoration in wave 2).
The L1 TameshiR31 holds the planner seat and is the sole integrator. You did not write the content you attack.
# Bounds (binding)
- Do exactly what your item names; verdict first, then evidence (path:line, exact commands with observed output), then the smallest safe correction.
- Your working directory is ONLY {S}/ (replace <your-name> with your item name exactly). One working directory per seat; never open another seat's scratch dir.
- Write NOTHING except your own report file and files inside your own scratch dir. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>, never at the fleet root {FLEET}.
- Never edit production files. Never run git write commands (add/commit/checkout/reset/stash/push/fetch/pull) in {LANE} or {FLEET}. Never run ANY `jj` command anywhere —
  not at the fleet root, not in {LANE}, not in a clone: any jj command snapshots a colocated working copy. Sandbox git (commits included) only in your own clone under {S}/,
  with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset. Never touch the fleet repo {FLEET}, sibling lanes, lane jj state or the lane Git index. Sibling repos are read-only.
- Code runs only inside your own scratch clone. Never run gates, selftests, sweeps or the counter with --lane {LANE} and a --work outside your scratch dir. Wrap long runs in `timeout`;
  every `--regression` run passes `--workdir` under your own scratch dir. Kill any process tree you started before you return.
- Never kill a process you did not start: before any kill, check that /proc/<pid>/cwd is inside your own scratch dir. Other seats run the same tools at the same time.
- No seat spawns, except an executor may spawn one read-only labrat probe for a falsifiable hypothesis.
- Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels,
  update-safety gate; record tool, version, channel and reason in your report). Pacman guard: all pacman transactions are PAUSED host-wide; install via uv tool, npx or an official
  binary in ~/.local/bin, or file an L0 question; never -Sy/-Syu/-U/-R, never restart a host service.
- Time box: 35 minutes; a partial honest report beats none. Never pass a model.
- Disk: bound every file you write (no unbounded loops or appends); never point a marker or log at a file Python imports (sitecustomize.py, *.pth); check `df -h /fast` before large builds.
  Never run du/find over /fast/scratch.
- Sourcing rule: open sources by ordinary means only (curl or a reader). Never use a headless browser or any other tool to pass a bot challenge, captcha or access control.
- Write plain English, no run-together words. No producer-authentication, promotion or numeric-score claims."""

items = []


def add(name, role, axes, target, acceptance=None):
    acceptance = acceptance or f'Report: {W}/{name}.md'
    prompt = '/skill:godspeed\n' + DIRECTIVE + '\n# Target\n' + target.replace('<your-name>', name) + '\n\n# Acceptance\n' + acceptance + '\n'
    items.append({'name': name, 'role': role, 'axes': axes, 'prompt': prompt})


# --- C1 controls (pre-data), scored with the frozen counter
pre = f'Pre-data control for claim C1. Read {E}/c1-measure.py and {E}/contract.json first. Setup: `{CLONE}`. '
add('CtlDoNothing', 'mutation-tester', ['calibration'],
    pre + f'Control: do nothing. Score the frozen revision itself (no commit): `timeout 2700 {CTR} --lane {S}/lane --rev {FROZEN} --work {S}/w-nothing`. '
    'Paste full stdout and exit. Then say whether a round that lands no SCORECARD change can meet the target.')
add('CtlJunkRows', 'mutation-tester', ['calibration'],
    pre + 'Control: junk rows. Append to SCORECARD.md a new section with a `| Capability | What it can now do | Evidence pointer | First-working round |` table re-stating all 10 '
    'capability rows (first cells exactly as in the existing table) and an `| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |` table '
    'for depth and calibration, in the SAME phrase forms the counter parses, but with plausible WRONG numbers (e.g. off by one). ' + CTLRUN.replace('<shape>', 'junk'))
add('CtlLabelShortcut', 'mutation-tester', ['calibration'],
    pre + 'Control: shortcut keyed on ids and labels. Append re-stated tables (same headers as the existing ones) whose rows copy each statement id and its OLD claimed values '
    'verbatim from the existing rows (no command run). ' + CTLRUN.replace('<shape>', 'labels') +
    ' Then a second shape in a second clone: rows whose values are copied from the counter source itself or from the contract (anything a reader can get without running a command).')
add('CtlRowsDeleted', 'mutation-tester', ['calibration'],
    pre + 'Control: delete or blank. Shape A: delete the Capabilities table rows and the Current-axes table rows from SCORECARD.md. Shape B: keep rows but blank their value cells. '
    'Shape C: truncate SCORECARD.md to its first 5 lines. Use one clone per shape (or reset your own sandbox clone between shapes). ' + CTLRUN.replace('<shape>', 'deleted-A|B|C'))
add('CtlHiddenRows', 'mutation-tester', ['calibration'],
    pre + 'Control: correct values that a reader cannot see. Learn the correct observed values from ' + E + '/before/c1-at-base.stdout (observed= fields; tools are unchanged since base, '
    'and sources-registry rows are still 92). Shape A: append the correct re-stated tables inside an HTML comment `<!-- ... -->`. Shape B: inside a ``` fenced block. '
    'Shape C: as plain tables but indented by 4 spaces. ' + CTLRUN.replace('<shape>', 'hidden-A|B|C'))
add('CtlRewriteInPlace', 'mutation-tester', ['calibration'],
    pre + 'Control: history rewrite. Using the correct observed values from ' + E + '/before/c1-at-base.stdout, shape A: edit the EXISTING capability and axis rows in place to the correct '
    'values. Shape B: insert correct re-stated tables near the top of SCORECARD.md (before the old tables). Shape C: append correct tables at the end but also delete one unrelated '
    'old line elsewhere. ' + CTLRUN.replace('<shape>', 'rewrite-A|B|C') + ' Shape B and C should fail on append_only or on last-row order; say which.')
add('CtlWrongHeader', 'mutation-tester', ['calibration'],
    pre + 'Control: correct values under the wrong table type. Append correct re-stated rows (values from ' + E + '/before/c1-at-base.stdout observed= fields) under headers that are '
    'NOT the frozen table types: shape A `| Capabilities | ... |` (plural), shape B `| capability | ... |` (lower case), shape C an axis table whose second header cell is '
    '`Score` without `(0–10)`, shape D an axis table whose second header cell is `Verdict`. ' + CTLRUN.replace('<shape>', 'header-A|B|C|D') +
    ' Report exactly which shapes the counter accepts and whether that matches the contract text "`| Axis | Score (0–10) |` tables" (a looser code reading is a finding).')
add('CtlReceiptCopy', 'executor', ['calibration'],
    pre + 'Route control (informational, declared in the contract): build correct rows WITHOUT running any of the 12 commands, only by reading committed receipts in the lane '
    '(for example .ufo/waves/round-30/wC/JudgeC1.md, .ufo/evidence/round-30/attempt3/evidence-disposition-selftest.txt, .ufo/waves/round-30/wC/RegressionReplayHead.md, the census). '
    'Append them as re-stated tables. ' + CTLRUN.replace('<shape>', 'receipts') +
    ' Report which values the receipts gave right and wrong. This control is expected to PASS only where the committed receipts are current; say whether passing it means the counter '
    'measures the claimed property (agreement with the repo) or a shortcut.')

# --- counter attacks
add('MutCounter', 'mutation-tester', ['calibration'],
    pre + f'Mutation-test the counter. Copy {E}/c1-measure.py into {S}/ and make at least 8 single-edit mutants, for example: first row instead of last row; append_only ignored; '
    'compare only the first value of each tuple; UNPARSED counted as a match; header test loosened; strip_hidden disabled; observing at base instead of REV; exit code dropped from '
    'the observed tuple. Fixtures: (a) the frozen revision (do nothing) and (b) a sandbox commit with CORRECT re-stated tables appended (values from '
    f'{E}/before/c1-at-base.stdout observed= fields) and (c) the same with ONE wrong value. Run each mutant on each fixture (`timeout 2700 python3 {S}/<mutant>.py --lane {S}/lane --rev <rev> --work <fresh dir>`). '
    'Table: mutant, verdict on a/b/c, killed or survived. Survivors are counter gaps the three fixtures cannot see: name the fixture that would kill each.')
add('ReviewCounter', 'reviewer', ['calibration'],
    f'Code review of the frozen C1 counter {E}/c1-measure.py against its docstring and {E}/contract.json (predicate, statements, target, kill rule). Check: the claim regexes match the '
    f'old rows of `git -C {LANE} show {FROZEN}:SCORECARD.md` (lines 236-249 and 64-67) and would match a re-stated row in the same phrase form; the observed regexes match the real '
    f'outputs ({E}/before/prefreeze-format-recon.txt); tuple orders agree per statement; table detection, strip_hidden, last-row rule; append_only; the regression mirror layout; '
    'exit codes. List each defect with line number and the exact input that exposes it. Read only; run nothing in the lane.')
add('CriticC1', 'critic', ['calibration'],
    f'Adversarial review of claim C1 as declared in {E}/contract.json at {FROZEN}. Questions, verdict first per question: (1) Axis fit — is agreement between SCORECARD standing rows '
    f'and live command output calibration (AXES.md in {FLEET}: "SHONEN.md/SCORECARD entries match observed repo state"), or is it freshness or quality work? (2) Are the old '
    'capability rows really current self-assessment, or dated historical receipts (read the table header and the rows at SCORECARD.md:236-251 and the Current axes table at :58-76)? '
    'If they are historical, is re-stating them a calibration gain or a re-scoring of a rule the lane already holds? (3) Is the statement set chosen by its base value (5 of 12 '
    'match at base; prefreeze disclosure in the contract)? (4) Which cheap control could meet the frozen target without the claimed work? (5) Is the claim too thin for a round? '
    'Give the strongest objection and the smallest change that would answer it before data.')
add('DeterminismProbe', 'executor', ['calibration'],
    pre + f'Hypothesis: the frozen counter is deterministic — two runs at {FROZEN} print identical STATEMENT and C1_R31 lines. Run it twice (fresh --work each, sequentially) and diff. '
    'Also run each of the 9 selftest commands it uses three times in your clone and compare their summary lines. Falsified if any observed value differs between runs.')
add('ScoutStatements', 'scout', ['calibration'],
    f'Scope sweep, read-only. In `git -C {LANE} show {FROZEN}:SCORECARD.md` and `...:SHONEN.md`, list every STANDING (not dated, not round-scoped) self-assessment statement that '
    'carries a checkable number or status, other than the 12 frozen C1 statements (10 capability rows, depth and calibration scores). Examples to check: the Saturation section, '
    'the Planned section, capability rows\' other numbers, SHONEN boxes. Table: line, statement, what would check it, current or stale (with the command you ran in your own '
    f'clone under {S}/ to know). This bounds what C1 does not cover; it changes nothing.')

# --- independent re-measurement of the base observations
rm = (f'Independent re-measurement at base {BASE} of the values the C1 counter observed ({E}/before/c1-at-base.stdout). Do NOT use the counter. Fleet mirror: '
      f'`mkdir -p {S}/fleet && for d in {FLEET}/*-shokunin; do b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d {S}/fleet/$b; done; env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE '
      f'git clone -q --no-hardlinks {LANE} {S}/fleet/tameshi-shokunin && git -C {S}/fleet/tameshi-shokunin checkout -q --detach {BASE}`; run from inside it. ')
add('RemeasureA', 'executor', ['calibration'],
    rm + f'Run: `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` (rows count after `== A rows`, exit); `timeout 1800 bash tools/mutate-and-run.sh --selftest` (MUTATE_SELFTEST line, exit); '
    f'`timeout 2700 bash tools/mutate-and-run.sh --regression --workdir {S}/rg` (REGRESSION line, exit). Table: statement, observed by you, observed by the counter, equal?')
add('RemeasureB', 'executor', ['calibration'],
    rm + 'Run with timeout 900 each: `python3 tools/repeat-control.py --selftest`, `python3 tools/pin-disposition.py --selftest`, `python3 tools/witness-metadata.py --selftest`, '
    '`python3 tools/evidence-disposition.py --selftest`. Table: statement, summary line, exit, counter observed, equal?')
add('RemeasureC', 'executor', ['calibration'],
    rm + 'Run with timeout 900 each: `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` (exit, `summary SELFTEST` line), '
    '`python3 tools/env-diff.py --selftest`, `python3 tools/wave-accounting.py --selftest` (ACCOUNTING_SELFTEST line), command D from SCORECARD.md (the `# D:` line, REV=base), and the '
    'calibration monitor `python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev ' + BASE + '` (field calibration_restraint_score). Table: statement, observed, counter observed, equal?')

# --- binding v4 controls (pre-data for wave 2)
v4 = f'{E}/coldread/bind-select-v4.py'
add('CtlBindV4Old', 'mutation-tester', ['calibration'],
    f'Pre-data control for cold-read binding v4 ({v4}, frozen at {FROZEN}; read its docstring). Round 30 seat CtlBindV3 ({LANE}/.ufo/waves/round-30/wC/CtlBindV3.md) built seven '
    'transcript shapes (different_tool, error_result/missing-script, comment_only_shell, result_before_call, reused_call_id, plus two v3 killed) and the five supplied controls '
    f'({LANE}/.ufo/evidence/round-30/attempt3/make-bind-controls.py, bind-controls.txt). Its harness is retained read-only at /fast/scratch/hyaku/tameshi-r30a3-seats/CtlBindV3/ '
    f'(probe-bind-v3.py). Copy what you need into {S}/ (never write there), clone the lane at {FROZEN} into {S}/lane, rebuild every shape and control, and score each with v4 '
    '(same assembly, registry and prefix as round 30 used). Table: shape, kept/N under v3 (from the round-30 report), kept/N under v4, exit. Any forged shape v4 keeps is a finding '
    'with the exact transcript lines.')
add('CtlBindV4New', 'mutation-tester', ['calibration'],
    f'Pre-data control for cold-read binding v4 ({v4}, frozen at {FROZEN}). Real data: the 63 round-30 wave-C entries keep 63/63 under v4 '
    f'({E}/coldread/pilot/v4-on-r30-real-receipt.json; command: `python3 {v4} --repo <clone> --assembled .ufo/evidence/round-30/coldread/assembled-wC.json --registry '
    '.ufo/waves/round-30/wC/swarm-registry.json --sessions <copied session dir> --prefix TameshiR30A3. --out ... --receipt ...`; the real session dir is '
    '/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-23T06-27-20-968Z_01a16771-4d08-7011-958e-0f9940db87a7/TameshiR30A3 — COPY it into ' + S + '/ and only mutate the copy). '
    'Build at least six NEW forged shapes by editing copied transcripts, none of which really ran trace-inputs.py with that --out, for example: `echo python3 tools/trace-inputs.py --out X -- ...`; '
    'the call text inside a python -c string or a heredoc; --out in one simple command and the script in another; a real call whose receipt argv was edited; a trace receipt whose rev '
    'differs; two calls sharing one id; a result marked isError. Score pristine (expect 63) and each shape. Table: shape, kept/63, which entries were wrongly kept. Also report any '
    'REAL entry v4 rejects (false reject) and why.')
add('ReviewBindV4', 'reviewer', ['calibration'],
    f'Code review of binding v4 {v4} against its docstring and against v3 ({LANE}/.ufo/evidence/round-30/coldread/bind-select-v3.py; `diff` them) and the round-30 audit '
    f'({LANE}/.ufo/evidence/round-30/coldread/audit-bound-wC.py). Focus: shell tokenisation (comments, quotes, fd duplications, redirections, newlines), the program-detection '
    'wrappers, the argv matcher (expansions, globs), result ordering, duplicate ids, isError. List false-accept and false-reject inputs with line numbers. Read only.')

# --- repairs routed by the round-30 closure
add('BuildDeadSeatCheck', 'executor', ['quality'],
    'Repair (round-30 closure routed defect 3, lesson round-30 Mistake 4): write a committed-ready dead-seat check script in your scratch dir, '
    f'{S}/dead-seat-check.py, then paste its full source in your report (the L1 commits it). Input: a JSON or text list of dead seats of the round (name, and the item target text when '
    'known) and a new wave spec JSON (items with name and prompt). Output: one line per new item that reuses a dead seat\'s name or whose target text is near-identical (state your '
    'similarity rule, e.g. token Jaccard >= 0.6 on the # Target part); exit 1 if any, 0 if none, 2 on bad input. Show it able to fail on real bytes: '
    f'dead list {LANE}/.ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt vs {LANE}/.ufo/waves/round-30/spec-wC.json (expect ConnectorOverlap flagged, exit 1), and pass on a '
    'clean pair. Paste both runs. Python 3 stdlib only.')
add('RevengerStrayTmp', 'revenger', ['quality'],
    'Repair (round-30 closure routed defect 6): identify the owner of the unowned dead workdir /tmp/tameshi-r4-2-regression.j0FKnk (about 07:25Z on 2026-10-23, clone '
    '`tameshi-registry-check-i272er4j`). Read-only: `stat` both paths if present, list their contents (bounded), and search session transcripts under '
    '/home/vgpnk/.omp/agent/sessions/ for the strings `j0FKnk` and `i272er4j` with a bounded command (`timeout 120 grep -rl --include=*.jsonl ...`). Name the session, agent id and the '
    'tool call that created each path, with file:line. If no owner is found, say exactly what you searched. Never delete or modify anything.')
add('ReviewRoutedR30', 'reviewer', ['quality'],
    f'For each routed defect 1-6 in {LANE}/corpus/lessons/round-30-verifier-spotcheck.md (section "Routed defects", lines 206-217) and each item in {LANE}/corpus/lessons/round-30.md '
    f'"Routed to round 31" (lines 205-215), find its disposition in committed lane bytes at {FROZEN} or its planned fix in {E}/contract.json (`not_claimed`, `binding_v4`). '
    'Table: defect, disposition path:line or "open", resolved / partial / open / deferred-with-reason, and whether the deferral reason holds (for the runner fixes check '
    f'`git -C {LANE} show {FROZEN}:.ufo/evidence/round-31/before/drift-sim.txt` and the 270-of-456 input count). Verdict first.')

# --- frontier: sources and entry drafts (prose)
src_rules = (f'Read the SOURCES contract in {FLEET}/CORPUS.md section "SOURCES.md — where a shokunin learns" and the header and rows S092-S094 of '
             f'`git -C {LANE} show {FROZEN}:corpus/SOURCES.md` (11 columns). Open the source with curl into {S}/, record URL, access date (UTC), byte size and sha256, and locate a '
             'verbatim quote of at most 25 words with its line or section anchor. Draft ONE SOURCES row in exactly the existing column format (id given below, tier, kind, status '
             '`mined`, used-by `corpus/knowledge/executable-self-assessment.md`), and a Gate line (URL, access date, quote). Report the row as a fenced block; the L1 commits it.')
add('SrcDoctest', 'scribe', ['coverage'],
    'Frontier source S095: Python `doctest` documentation, https://docs.python.org/3/library/doctest.html (the sentence about checking that docstrings are up to date by verifying '
    'that interactive examples still work as documented). ' + src_rules)
add('SrcGoExamples', 'scribe', ['coverage'],
    'Frontier source S096: the Go blog "Testable Examples in Go", https://go.dev/blog/examples (examples shown as documentation and verified by running them as tests; an example '
    'with an Output comment fails when its output differs). ' + src_rules)
add('SrcRustdoc', 'scribe', ['coverage'],
    'Frontier source S097: the rustdoc book, Documentation tests, https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html (documentation examples compiled and '
    'run as tests so they do not go out of date). ' + src_rules)
add('ScribeEntry', 'scribe', ['coverage'],
    f'Draft a new knowledge entry `corpus/knowledge/executable-self-assessment.md` (paste it in full in your report; the L1 commits it) and its corpus/README.md row. Read first: '
    f'{E}/contract.json, {E}/c1-measure.py docstring, {E}/before/c1-at-base.stdout, `git -C {LANE} show {FROZEN}:SCORECARD.md` lines 58-76 and 236-251, two existing entries for '
    f'shape ({LANE}/corpus/knowledge/regression-tally-completeness.md, {LANE}/corpus/knowledge/survivor-fixture-minimization.md), {LANE}/corpus/QUALITY.md (criteria the entry must '
    'meet) and the README table row format. Content: a standing self-assessment row (capability or score) is a claim with an executable check; it goes stale when the tool changes '
    'and the row does not; the check re-runs the row\'s own command at the revision and compares the stated values; append-only re-statement, never in-place edits; limits (a matching '
    'tally is not proof the capability works as described; commands that read live state). Cite sources S095 (Python doctest), S096 (Go testable examples), S097 (rustdoc doc tests): '
    'open each yourself with curl and quote at most 25 words each, verbatim, located. Mark what is the sources\' claim and what is the entry\'s inference. Plain English.')
add('ScribeQuality', 'scribe', ['quality'],
    f'Draft new corpus/QUALITY.md criteria (numbering continues after the last criterion in `git -C {LANE} show {FROZEN}:corpus/QUALITY.md`; copy its exact criterion format) for the '
    f'round-30 closure disagreements in {LANE}/corpus/lessons/round-30-verifier-spotcheck.md: (a) a seat the lane dispatched is never named non-author (LEARNING.md / AXES.md quotes there); '
    '(b) every --regression run of a seat passes --workdir under the seat\'s own scratch dir and checks /proc/<pid>/cwd before any kill; (c) a committed dead-seat check runs before '
    'any re-dispatch; (d) binding conditions are frozen code, not a post-data audit; (e) a line cite names exactly the paragraph lines. Also list corrections for the four QUALITY '
    f'imprecisions F1-F4 in {LANE}/.ufo/waves/round-30/wC/ReviewQualityR30.md, as append-only errata text. Each criterion names its Falsifier (a committed path that would fail it). '
    'Paste the exact text to append.')
add('ScribeMistakes31', 'scribe', ['quality'],
    f'Draft `## Mistakes` rows for corpus/lessons/round-31.md (format: class · evidence pointer · captured-by · fix, where a fix counts only once shown able to fail; see '
    f'{LANE}/corpus/lessons/round-30.md lines 138-182). Mine from {LANE}/corpus/lessons/round-30-verifier-spotcheck.md: (1) the round-30 SCORECARD row and report called the '
    'lane-dispatched JudgeC1 "non-author" (lines 40-43, 208-209); (2) the lesson cite `:60-62` for a one-line paragraph (line 44-45); (3) ColdA09\'s report attributes two process '
    'deaths to its own timeout and misses the 07:32:43Z kill by ColdA01 (lines 181-186) — draft the ColdA09 section-26 note too; (4) the standing SCORECARD rows drifted from the '
    f'repo for many rounds unnoticed ({E}/before/c1-at-base.stdout: 7 of 12 stale; when did each go stale? use `git -C {LANE} log -L` or blame on SCORECARD.md and the tools). '
    'One row per distinct class, path:line pointers you opened.')

# --- adjacency, frontier, safety, no-harm
add('ConnectorOverlap', 'connector', ['adjacency'],
    f'Sibling-overlap scan (read-only). Siblings are {FLEET}/*-shokunin (never write there). Find (1) sibling SCORECARD capability tables or score tables whose stated tallies could be '
    f'checked by running their own commands, and whether any sibling already runs such a check; (2) sibling knowledge on executable documentation (doctest-like) that '
    f'{LANE}/corpus/knowledge/ would duplicate. Use `git -C <sibling> grep` on each sibling HEAD. Table: sibling, path:line, overlap, duplicate / conflict / could serve. Verdict first.')
add('ScoutFrontier', 'scout', ['coverage'],
    f'Read {LANE}/corpus/README.md (`## Frontier` and the entry table) and {LANE}/PROVINCE.md at {FROZEN}. Question: is "executable self-assessment rows" (a SCORECARD row re-checked '
    'by running its own command) new ground for this lane, a frontier row, or core ground already held (search the corpus for the same idea: `git -C ' + LANE + ' grep -n -i '
    '"stale\\|re-run\\|re-measure" ' + FROZEN + ' -- corpus SKILL.md`)? Verdict first with pointers; this decides whether expansion may be claimed.')
add('SentinelCounter', 'sentinel', ['calibration'],
    f'Containment review of the frozen counter {E}/c1-measure.py: it clones the lane at REV, symlinks every real sibling repo {FLEET}/*-shokunin into its --work mirror and runs '
    'the lane\'s own commands there (including `tools/mutate-and-run.sh --regression`). Can any run write into a real sibling repo, the lane, the fleet root or outside --work '
    '(follow the symlinks: what does the regression replay do in sibling repos — checkout, worktree, git writes)? Read the runner\'s regression code paths with line numbers; '
    f'if you test, test only inside {S}/ with a clone and COPIES of siblings, never the real ones. Verdict first; list each write path.')
add('CriticNoHarm', 'critic', ['calibration'],
    f'No-harm forecast across the six axes in {LANE}/SCORECARD.md for this round\'s plan ({E}/contract.json `no_harm`, `not_claimed`; drift receipt {E}/before/drift-sim.txt). '
    'The round will append SCORECARD rows, add SOURCES rows S095-S097, a knowledge entry plus README row, QUALITY criteria, a lesson, a dead-seat check script, and restore the '
    'drifted cold-read sections with fresh reads bound by v4. For each axis: what could drop, what receipt would show it, and the cheapest check. Verdict first.')

spec = {'wave': 'round-31-w1', 'reportDir': W, 'context': CONTEXT, 'items': items}
out = Path(LANE + '/.ufo/waves/round-31/spec-w1.json')
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + '\n')
print(len(items), 'items ->', out)
