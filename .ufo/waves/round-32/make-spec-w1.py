#!/usr/bin/env python3
"""Round 32 (L1 TameshiR32) wave 1: pre-data control wave + build/frontier items, policy v1.
Freeze commit FROZEN carries the C1 counter and contract before any data seat."""
import json
from pathlib import Path

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
FROZEN = 'c31814978969a41a8e9b0f7d99fa308c5993c1b7'
BASE = 'e24688b2ff6cca1c9ad20e112f02c629b8597ff8'
R31BASE = '36c1d3933f680125aeefc447f07db0f03004901a'
R31HEAD = '08125328f87df92d3f25d0034ee792253ecbcbd9'
E = LANE + '/.ufo/evidence/round-32'
W = '.ufo/waves/round-32/w1'
S = '/fast/scratch/hyaku/tameshi-r32-seats/<your-name>'
DIRECTIVE = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text()
CTR = f'python3 {E}/c1-measure.py'
CLONE = (f'mkdir -p {S} && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks {LANE} {S}/lane '
         f'&& git -C {S}/lane checkout -q --detach {FROZEN}')
CTLRUN = (f'Write your control tool at {S}/lane/tools/tally-audit.py, make it ONE sandbox commit in {S}/lane on top of {FROZEN} (`env -u GIT_DIR -u GIT_WORK_TREE '
          f'-u GIT_INDEX_FILE git -C {S}/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C {S}/lane -c user.name=ctl '
          '-c user.email=ctl@sandbox commit -qm <shape>`), then score it with the FROZEN counter, unchanged: '
          f'`timeout 2400 {CTR} --lane {S}/lane --rev HEAD --work {S}/w-<shape>` (a fresh empty --work per run; no --seed). '
          'Paste the counter\'s full stdout verbatim (every COPY line and the C1_R32 line) and its exit code, and the full source of your control tool. '
          'Expected for a control: C1_R32_PASS=false. A control that prints C1_R32_PASS=true is a finding: say exactly why and which copies it got right.')

CONTEXT = f"""# Goal
Tameshi round 32 (verification-fixture craft), wave 1 (pre-data adversarial controls + build/frontier items, policy v1). One measured claim, C1, a capability
acquisition on axis operability: a new versioned tool {LANE}/tools/tally-audit.py (not yet written; the L1 writes it after this wave's controls return) that audits
the mutation runner {LANE}/tools/mutate-and-run.sh WITHOUT editing it. Interface: `python3 tally-audit.py --runner PATH` prints a final line beginning
`TALLY_AUDIT: PASS` (exit 0) or `TALLY_AUDIT: FAIL` (exit 1), exit 2 when it cannot audit. Planned checks: (a) per-leg presence — each `st_*=$?` leg status of
run_regression named exactly once in the --regression tally loop; (b) the tally block run against an independent oracle for every exit status 0-255 plus
overcount/undercount stress; (c) the runner's own tally selftest harness (lines 1989-2040) run against a panel of known-faulty tally blocks it must reject.
Motivation: round-30 seat MutateHead ({LANE}/.ufo/waves/round-30/wC/MutateHead.md) left 8 real survivors of the runner's --selftest (T08 N05 H03 H04 H05 N01 N02
N03), and a sum-preserving miscount (duplicate one tally operand, drop another) passes the runner's run-time guard. Both were deferred twice because the runner is
an input of 270 of 480 cold-read ledger entries; the runner therefore stays byte-identical (sha256 a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9).
Frozen predicate (contract {E}/contract.json, counter {E}/c1-measure.py, both frozen at lane commit {FROZEN}):
"C1 passes at REV iff the committed tools/tally-audit.py at REV, run as `python3 tally-audit.py --runner COPY`, exits 1 with a stdout line beginning
`TALLY_AUDIT: FAIL` on every one of the 18 must-kill runner copies, exits 0 with a stdout line beginning `TALLY_AUDIT: PASS` on every one of the 8 must-accept
runner copies, and REV's tools/mutate-and-run.sh has sha256 a7d3f2dd…2eb9." Label: C1_R32_PASS. 9 must-kill copies are frozen (the 8 MutateHead survivors,
byte-identical to MutateHead's mutated SHA-256 column, plus D01), 9 are generated per run from a seeded RNG (one per family); 6 must-accept copies are frozen, 2 generated.
Before (base {BASE}, no tool): `C1_R32: kill=0/18 accept=0/8 other=26 runner_sha_ok=1 tool_present=0 … C1_R32_PASS=false`, exit 1 ({E}/before/c1-at-base.stdout).
Target: kill=18/18 accept=8/8, PASS true. The counter, predicate and target are never changed after the freeze; a control that meets the counter is a finding.
The L1 TameshiR32 holds the planner seat and is the sole integrator. You did not write the content you attack.
# Bounds (binding)
- Do exactly what your item names; verdict first, then evidence (path:line, exact commands with observed output), then the smallest safe correction.
- Your working directory is ONLY {S}/ (replace <your-name> with your item name exactly). One working directory per seat; never open another seat's scratch dir.
- Write NOTHING except your own report file and files inside your own scratch dir. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>,
  never at the fleet root {FLEET}.
- Never edit production files. Never run git write commands (add/commit/checkout/reset/stash/push/fetch/pull) in {LANE} or {FLEET}. Never run ANY `jj` command anywhere —
  not at the fleet root, not in {LANE}, not in a clone: any jj command snapshots a colocated working copy. Sandbox git (commits included) only in your own clone under {S}/,
  with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset. Never touch the fleet repo {FLEET}, sibling lanes, lane jj state or the lane Git index. Sibling repos are read-only.
- Code runs only inside your own scratch clone or scratch dir. Running the frozen counter is read-only on the repo you pass as --lane: pass your own clone, and a --work
  under your own scratch dir. Wrap long runs in `timeout`; every `--regression` run passes `--workdir` under your own scratch dir. Kill any process tree you started before you return.
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


pre = f'Pre-data control for claim C1. Read {E}/c1-measure.py and {E}/contract.json first. Setup: `{CLONE}`. '
ctl = [
    ('CtlDoNothing', 'mutation-tester', f'Control: do nothing. Score the frozen revision itself (no tool, no commit): `timeout 2400 {CTR} --lane {S}/lane --rev {FROZEN} --work {S}/w-nothing`. '
     'Paste full stdout and exit. Then say whether a round that lands no tool can meet the target.', False),
    ('CtlAlwaysPass', 'mutation-tester', 'Control: a tool that ignores its input, prints `TALLY_AUDIT: PASS` and exits 0.', True),
    ('CtlAlwaysFail', 'mutation-tester', 'Control: a tool that ignores its input, prints `TALLY_AUDIT: FAIL` and exits 1.', True),
    ('CtlJunk', 'mutation-tester', 'Control: junk. A tool that prints both labels in random order plus random noise and exits with a random code from {0,1,2} (seed from os.urandom).', True),
    ('CtlShaPin', 'mutation-tester', 'Control: sha pin. A tool that prints PASS/exit 0 iff sha256 of the --runner file equals the pinned runner sha256 '
     '(a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9), else FAIL/exit 1.', True),
    ('CtlRegionDiff', 'mutation-tester', 'Control: region diff. Embed the pinned runner bytes (from `git show ' + BASE + ':tools/mutate-and-run.sh`) in the tool; '
     'FAIL iff the --runner file differs from them anywhere inside run_regression\'s tally block (from `  local nlegs=9` to the function\'s closing `}`) or inside the '
     'selftest tally harness (lines 1989-2040 of the pinned file, located by content); PASS otherwise. Then a second shape: the same but ignoring comment-only lines and whitespace.', True),
    ('CtlLineCount', 'mutation-tester', 'Control: line count. A tool that passes iff the --runner file has the pinned line count (2080), fails otherwise. Second shape: passes iff '
     'the byte size equals the pinned size.', True),
    ('CtlShaTable', 'mutation-tester', 'Control: fixture-keyed sha table. Import the frozen counter as a module (importlib from ' + E + '/c1-measure.py) at control-build time, compute the '
     'sha256 of all 9 frozen must-kill copies (`frozen_kill`) and of the 6 frozen must-accept copies, and embed them in the tool: FAIL iff the --runner sha is in the must-kill table, '
     'PASS otherwise. Second shape: also FAIL iff the file after deleting comment lines matches any frozen must-kill copy after the same normalization.', True),
    ('CtlTextKeyed', 'mutation-tester', 'Control: text-keyed. A tool that FAILs iff any non-comment line of the --runner file equals the new text of any frozen mutant edit in '
     f'{E}/c1-measure.py (`frozen_kill`: e.g. `      4) npass=$((npass + 1)) ;;`, `    rc=$?` right after the comparison line, `    for ti in 0 1 2 3 4 5 6 7 7; do`, the `||` forms, the '
     'N01 vector missing, the D01 loop), PASS otherwise. Make it as good a pure text matcher as you can in 20 minutes; report which generated copies it misses.', True),
    ('CtlSiblingConsensus', 'mutation-tester', 'Control: sibling consensus. The counter writes all 26 copies into one directory. A tool that reads every sibling file in the --runner '
     'file\'s directory, builds the per-line majority text, and FAILs iff the --runner file differs from the majority in any non-comment line; PASS otherwise. '
     'Report whether reading siblings lets a tool meet the counter.', True),
    ('CtlStaticOnly', 'mutation-tester', 'Partial-work control: static per-leg presence only. A tool that extracts the `st_*=$?` assignment names inside run_regression and the operands '
     'of the tally loop `for st in ...; do`, FAILs iff they differ as multisets or nlegs differs from the count, PASS otherwise. No runtime or harness checks.', True),
    ('CtlRuntimeOnly', 'mutation-tester', 'Partial-work control: runtime tally only. A tool that extracts the tally block (from `  local nlegs=9 npass=0 nfail=0 nsetup=0 st` to the '
     'closing `}` of run_regression), runs it in bash (inside a function with the nine st_* names declared local, `local root=x auto=0 KEEP=1`) for every status 0..255 at the first '
     'leg and statuses 1,2,3,4,126,127,255 at every leg, plus the loop with its last operand duplicated and with it removed, and compares first line and exit with an oracle '
     '(any 1 -> `REGRESSION: FAIL (cases=9 passed=P failed=F setup=S)` exit 1; else any non-zero -> `REGRESSION: SETUP (cases=9 passed=P cannot-verify=S)` exit 2; else count != 9 -> '
     '`REGRESSION: SETUP (case-tally mismatch: cases=9 counted=N)` exit 2; else PASS line exit 0). No harness check.', True),
    ('CtlHarnessOnly', 'mutation-tester', 'Partial-work control: harness panel only. A tool that runs the selftest tally harness section of the --runner file (from `  local tblock ` to '
     '`  tblock=$tblock_full`) inside a bash function with its own `st` accounting, once with the pristine tally block injected and once per known-faulty block (see MutateHead.md '
     '"Exact supplemental construction": faults H03 H04 H05 N01 N02 N03), and FAILs iff the harness accepts any fault or rejects the pristine block. No runtime or static check.', True),
    ('CtlOldSelftest', 'executor', 'Control: the existing gate. A tool that runs `timeout 900 bash <runner> --selftest` in a fresh temporary directory copy and passes its verdict '
     'through (exit 0 -> PASS, else FAIL). Run the counter with `--jobs 4`. This shows which copies the runner\'s own selftest already kills; expected: it kills D01/gD01 (and any '
     'generated copy its vectors cover) but none of the 8 frozen MutateHead survivors.', True),
    ('CtlComboShortcut', 'mutation-tester', 'Control: best cheap shortcut. Combine CtlStaticOnly, a text matcher for the frozen mutant texts that ignores comment lines, and a '
     'sha table of the frozen must-kill copies (see the contract). No runtime or harness execution. Report which copies it misses.', True),
]
for name, role, body, commit in ctl:
    add(name, role, ['operability'], pre + body + (' ' + CTLRUN.replace('<shape>', name) if commit else ''))

add('MutCounter', 'mutation-tester', ['operability'],
    pre + f'Mutation-test the counter. Copy {E}/c1-measure.py into {S}/ and make at least 8 single-edit mutants, for example: kill condition checks exit only; kill condition '
    'checks label only; OTHER counted as KILL; accept set ignored; runner_sha_ok dropped from the pass condition; generated copies skipped; the copy label leaked into the copy file '
    'name; the tool read from the working tree instead of REV; N_KILL compared with >= instead of ==. Fixtures: (a) the frozen revision (no tool), (b) an always-FAIL tool commit, '
    '(c) an always-PASS tool commit, (d) a tool that exits 1 printing nothing, (e) a runner edit at REV (any one-byte change to tools/mutate-and-run.sh plus an always-FAIL tool). '
    f'Run each mutant on each fixture (`timeout 1200 python3 {S}/<mutant>.py --lane {S}/lane --rev <rev> --work <fresh dir> --seed 1`). Table: mutant, verdict on a-e, killed or '
    'survived. Survivors are counter gaps the fixtures cannot see: name the fixture that would kill each.')
add('ReviewCounter', 'reviewer', ['operability'],
    f'Code review of the frozen C1 counter {E}/c1-measure.py against its docstring and {E}/contract.json. Check predicate identity: the contract `predicate` sentence, the '
    'docstring sentence, the code conditions (`code_conditions` quoted in the contract vs the actual Python) and the receipt label C1_R32_PASS must say the same thing; list every '
    'difference. Check: each anchor edit in frozen_kill/generated_kill/frozen_accept/generated_accept does what its label says; the tool is read from REV, not the worktree; copy '
    'names leak nothing; exit codes; --work emptiness; seed replay. List each defect with line number and the exact input that exposes it. Read only; run nothing in the lane.')
add('CriticC1', 'critic', ['operability'],
    f'Adversarial review of claim C1 as declared in {E}/contract.json at {FROZEN}. Verdict first per question: (1) Axis fit under addendum §9 ("name the axis by the surface the '
    'round changes"): is a new audit tool for the runner operability or capability acquisition, and is it a real new surface or re-scoring a rule the lane already holds? '
    '(2) Does building the fix in a new tool while leaving tools/mutate-and-run.sh untouched actually resolve the twice-deferred items (runner per-leg tally check; 8 MutateHead '
    'survivors), or does it only move them? (3) Which cheap control could meet the frozen target without the claimed work (consider tools that read the counter, the contract, '
    'sibling copies, or the pinned runner)? (4) Is the target sized to one round and re-derivable with one command over committed bytes? (5) Strongest objection and the smallest '
    'change that would answer it BEFORE data. Read-only; you may read any lane file.')
add('EquivFamilies', 'mutation-tester', ['operability'],
    pre + f'Equivalence attack on the must-kill set. For each frozen and generated must-kill family in {E}/c1-measure.py, decide whether ANY parameter value yields a copy that is '
    'behaviorally equivalent to the pristine runner for both the --regression tally and the tally selftest harness (an equivalent must-kill copy would make the target unreachable '
    'for a correct tool, or reward a tool that rejects correct code). For each family, give a concrete witness that the pristine runner and the mutant differ: a status vector '
    '(tally families) or a faulty tally block the pristine harness rejects and the mutant harness accepts (harness families), and RUN it in bash in your scratch dir on copies built '
    'by importing the counter module. Cover every parameter value of gT08 (K=2..255), gN05 (3 forms), gH03 (3), gH04 (3), gH05 (all P,Q pairs), gN01 (4), gN02 (2), gN03 (2), gD01 '
    '(all i,j). Also check every must-accept copy is equivalent. Table: family, parameter values checked, equivalent values found (should be none), witness.')
add('ReplaySurvivors', 'executor', ['operability'],
    pre + f'Hypothesis: the 9 frozen must-kill copies still survive the runner\'s own selftest at the pinned runner (8 MutateHead survivors print `MUTATE_SELFTEST: 106/106 pass` '
    'except N01 which prints 105/105), and D01 is killed by it. Build the copies by importing the counter module (frozen_kill on `git show ' + BASE + ':tools/mutate-and-run.sh`), '
    f'write each into its own dir {S}/c-<id>/tools/mutate-and-run.sh, and run `timeout 900 bash tools/mutate-and-run.sh --selftest` there (at most 3 at a time). Table: id, exit, '
    'MUTATE_SELFTEST line, VERDICT line. Falsified if any MutateHead survivor is killed or D01 survives.')
add('DeterminismProbe', 'executor', ['operability'],
    pre + f'Hypothesis: the counter is deterministic for a fixed seed — two runs with `--seed 2a` on the same tool print identical COPY lines (outcome, exit, sha256). Use an '
    'always-FAIL control tool committed in your clone (see CtlAlwaysFail), run twice with fresh --work, diff. Then run once with no seed twice and show the seeds and generated '
    'labels differ. Falsified if fixed-seed runs differ.')
add('SeedSpace', 'executor', ['operability'],
    pre + f'Import {E}/c1-measure.py as a module in your scratch dir. For 500 seeds, build all copies from the pinned runner text and check: every must-kill copy differs from '
    'pristine; no must-kill copy equals any must-accept copy; every must-accept generated copy differs from pristine; the generated labels cover every parameter value of each family '
    'over the 500 seeds (report the observed distribution); `bash -n` passes on every copy built for 20 seeds. Paste the script and its output.')

# --- repairs routed by the round-31 closure
add('RunCounterV2', 'executor', ['calibration'],
    f'Repair check (routed items 1-2 of {LANE}/corpus/lessons/round-31-verifier-spotcheck.md). {E}/repair/c1-r31-measure-v2.py is the round-31 counter with two conditions '
    f'changed (axis header equals `Score (0–10)`; append-only is a byte prefix). Diff it against {LANE}/.ufo/evidence/round-31/c1-measure.py and confirm only those two changes plus '
    f'the docstring. Setup a fleet mirror as the round-31 counter expects (read its docstring and --lane/--base options); clone the lane into {S}/lane. Run v2 and the frozen v1 at '
    f'{R31HEAD} and at {R31BASE} (fresh --work each, timeout 2700). Table: rev, v1 C1_R31 line, v2 C1_R31 line, equal? Expected: equal at both revisions (v2 changes no verdict on real data).')
add('CtlHeaderV2', 'mutation-tester', ['calibration'],
    f'Control for the v2 repair counter {E}/repair/c1-r31-measure-v2.py versus the frozen v1 {LANE}/.ufo/evidence/round-31/c1-measure.py. Clone the lane into {S}/lane at {R31HEAD}. '
    'Shape A: append correct re-stated axis rows under a header whose second cell is `Score` (no range). Shape B: `Score (0-10)` with a hyphen-minus instead of the en dash. '
    'Shape C: SCORECARD.md rewritten with CRLF line endings for its first 10 lines (content otherwise unchanged) plus the correct appended rows. Shape D: one invisible byte '
    '(U+200B) inserted in an old line. One sandbox commit per shape; run v1 and v2 on each (fresh --work, timeout 2700). Table: shape, v1 verdict, v2 verdict. Expected: v1 accepts '
    'at least A (and possibly C), v2 rejects A, B, C and D.')
add('ReviewRepairReceipts', 'reviewer', ['calibration'],
    f'Verify the repair receipts the L1 committed at {FROZEN}: {E}/repair/c1monitor-at-r31-base-36c1d393.*, {E}/repair/commandD-at-r31-67c0e013.*, '
    f'{E}/repair/commandD-at-r31-final-08125328.*, {E}/before/*. In your own clone under {S}/ re-run the monitor (`python3 .ufo/evidence/round-27/c1-measure.py --repo <clone> --rev REV`) '
    'and command D (SCORECARD.md `# D:` line) at the same revisions and compare byte for byte. Check the contract does not claim to reconstruct the missing round-31 exit. Verdict per receipt.')
add('ExecReceiptCheck', 'executor', ['calibration'],
    f'Build a small receipt-completeness checker in {S}/receipt-check.py (the L1 may commit it): `python3 receipt-check.py DIR` lists every `*.stdout` file under DIR with no sibling '
    '`.exit` file of the same stem, prints `RECEIPT_CHECK: missing_exit=N files=M`, exits 1 iff N>0. Include `--selftest` with at least 4 fixture cases in a temp dir. Show it able '
    f'to fail: run it on {LANE}/.ufo/evidence/round-31 (expect after/commandD-at-final.stdout listed) and on {E} (expect 0). Paste the full script and outputs.')

# --- frontier: sources (prose)
src_rules = (f'Read the SOURCES contract in {FLEET}/CORPUS.md section "SOURCES.md — where a shokunin learns" and the header and rows S094-S096 of '
             f'`git -C {LANE} show {FROZEN}:corpus/SOURCES.md` (11 columns). First check that the URL is not already a row (grep the file). Open the source with curl into {S}/, '
             'record URL, access date (UTC), byte size and sha256, and locate a verbatim quote of at most 25 words with its line or section anchor. Draft ONE SOURCES row in exactly '
             'the existing column format (id given below, tier, kind, status `mined`, used-by `tools/tally-audit.py; corpus/knowledge/runner-tally-audit.md`), and a Gate line '
             '(URL, access date, quote). Report the row as a fenced block; the L1 commits it.')
add('SrcBashExit', 'scribe', ['operability'],
    'Source S097: GNU Bash Reference Manual, "Exit Status", https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html (exit status range 0-255; 126 not executable; '
    '127 not found; 128+N fatal signal). This grounds the audit oracle\'s full 0..255 status sweep. ' + src_rules)
add('SrcBashCase', 'scribe', ['operability'],
    'Source S098: GNU Bash Reference Manual, "Conditional Constructs", https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html (the `case` command: patterns '
    'tried in order, the first match wins, `*` as a final catch-all; `[[ ]]` with && and ||). This grounds why an inserted arm before `*)` reclassifies a status. ' + src_rules)
add('SrcMutationAdequacy', 'scribe', ['operability'],
    'Source S099: one primary source, not already a row, on judging a test suite by the seeded faults it detects (mutation adequacy / mutation score, or "testing the tests"), '
    'e.g. the PIT mutation testing home page https://pitest.org/ (only if not a duplicate of S047/S048), or Petrović and Ivanković, "State of Mutation Testing at Google" '
    '(ICSE-SEIP 2018) on an openly accessible page. Choose the best openly reachable one and say why. ' + src_rules)
add('ReopenS094', 'scribe', ['operability'],
    f'Re-open existing row S094 (Dwork et al., arXiv:1411.2664, holdout reuse) in `git -C {LANE} show {FROZEN}:corpus/SOURCES.md`. Fetch the PDF into {S}/ with curl, compare sha256 '
    'with the pin in the row, re-locate its quoted sentence (page and words), and decide whether it supports the counter\'s design of generating must-kill copies from a fresh seed '
    'per run (a holdout the tool author cannot see). Draft the old->new `used-by` change (add `.ufo/evidence/round-32/c1-measure.py`) and a Gate line, or argue it does not apply.')

# --- mistakes, recon, adjacency
add('ScribeMistakes', 'scribe', ['calibration'],
    f'Mine mistakes for {LANE}/corpus/lessons/round-32.md `## Mistakes` (class · evidence pointer · captured-by · fix · shown able to fail). Candidates to check against the '
    f'record: (1) the runner per-leg tally check and the 8 MutateHead survivors deferred twice because the runner is a cold-read input ({LANE}/corpus/lessons/round-30.md '
    '"Routed to round 31", round-31.md "Routed defects" item 4 and "Routed to round 32"), with no alternative route recorded; (2) round-31 command D receipt with no `.exit` '
    f'file ({LANE}/.ufo/evidence/round-31/after/); (3) the round-31 report stating a base monitor reading with no committed receipt; (4) any other closure disagreement in '
    f'{LANE}/corpus/lessons/round-31-verifier-spotcheck.md. For each give exact path:line evidence and a fix that can be shown to fail. Draft text only; the L1 commits.')
add('DriftSim', 'executor', ['calibration'],
    pre + 'Drift simulation for the calibration no-harm monitor. In your clone, make one sandbox commit per planned content edit, each on top of the frozen revision separately: '
    '(1) append one row line to corpus/SOURCES.md registry table; (2) append a line to corpus/README.md; (3) append a block to SCORECARD.md; (4) append a block to LOG.md; '
    '(5) add a new file corpus/knowledge/runner-tally-audit.md; (6) add a new file tools/tally-audit.py; (7) append a line to corpus/QUALITY.md; (8) all of 1-6 together. For each run '
    f'`timeout 900 python3 .ufo/evidence/round-27/c1-measure.py --repo {S}/lane --rev HEAD` and report the C1_MONITOR line and every `uncovered:` heading. This tells the L1 which '
    'sections a content edit drifts and so how many cold reads wave 2 needs.')
add('ConnectorOverlap', 'connector', ['adjacency'],
    f'Sibling-overlap scan, read-only: do any sibling lanes under {FLEET}/*-shokunin hold a tool or knowledge entry that audits a test harness against seeded faulty implementations '
    '("test the tests", harness meta-tests), a static per-operand tally presence check, or a held-out generated mutant set? grep their corpus/, tools/, scripts/ and SKILL.md. Table: '
    'lane, path:line, what it holds, overlap with C1 (none/adjacent/same). Name contested scope; do not absorb it.')
add('ScoutFrontier', 'scout', ['coverage'],
    f'Read-only. In {LANE}/corpus/README.md `## Frontier` and {LANE}/PROVINCE.md, find whether a runner tally audit (per-leg presence, oracle sweep, harness meta-test) moves any '
    'frontier F-row toward core, or is lane ground already held. Quote the rows (path:line). Also find where SKILL.md and README describe the runner\'s --regression tally and its '
    'selftest harness (path:line), so the L1 can document the new tool without editing any file that is an input of a credited cold-read section (read '
    f'{LANE}/.ufo/evidence/round-21/coldread/ledger.json `inputs` fields to know which files those are).')
add('ScoutDeferrals', 'scout', ['operability'],
    f'Read-only data walk for the L1 planner seat. In {LANE}/corpus/lessons/round-29.md, round-30.md, round-31.md and their verifier spot-checks, and SCORECARD.md round-29 to -31 '
    'blocks, list every item routed about tools/mutate-and-run.sh (tally, guard, harness, per-leg, survivors), with its first round, its current status, and whether C1\'s planned '
    'checks (a) static per-leg presence, (b) runtime oracle sweep 0..255 with stress, (c) harness panel would close it. Table with path:line. Flag any routed runner item C1 leaves open.')

spec = {'wave': 'round-32-w1', 'reportDir': W, 'context': CONTEXT, 'items': items}
out = Path(LANE + '/.ufo/waves/round-32/spec-w1.json')
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + '\n')
print(len(items), 'items ->', out)
