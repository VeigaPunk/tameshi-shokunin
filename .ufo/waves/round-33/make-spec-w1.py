#!/usr/bin/env python3
"""Round 33 (L1 TameshiR33) wave 1: pre-data controls, dev sweeps, reviews, frontier source. Policy v1."""
import json
from pathlib import Path

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
FREEZE = 'f6d8a891f1d966c5c3cdda385090da3a6e804675'
BASE = '66e1fb444615b3afe380e7df0244ef7fae1dd985'
E = LANE + '/.ufo/evidence/round-33'
W = '.ufo/waves/round-33/w1'
S = '/fast/scratch/hyaku/tameshi-r33-seats/<your-name>'
DIRECTIVE = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text()
CTR = f'python3 {E}/c1/c1-measure.py'
C2CTR = f'python3 {E}/c2/c2-measure.py'
TOOL = LANE + '/tools/tally-audit-v2.py'

CONTEXT = f"""# Goal
Tameshi round 33 (verification-fixture craft), wave 1 (pre-data controls + dev sweeps + reviews + frontier source, policy v1).
Two claims were frozen at lane commit {FREEZE} (contract {E}/contract.json) before any data seat:

C1 (operability, capability acquisition; routed from the round-32 closure): the new tool {LANE}/tools/tally-audit-v2.py
audits the mutation runner {LANE}/tools/mutate-and-run.sh (sha256 a7d3f2dd...2eb9, NEVER edited) without editing it.
Interface: `python3 tally-audit-v2.py --runner COPY` prints a final stdout line beginning `TALLY_AUDIT: PASS` (exit 0),
`TALLY_AUDIT: FAIL` (exit 1) or `TALLY_AUDIT: SETUP` (exit 2). Round 32's v1 tool was defeated by a sealed held-out set of
runner copies ({LANE}/.ufo/evidence/round-32/heldout/*.json, committed); the four missed classes and v2's answers:
(1) runtime vectors never produced 3-8 failing/setup legs -> v2 sweeps every (failing,setup) count pair 0..9;
(2) per-position statuses stopped at {{1 2 3 4 126 127 255}} -> v2 sweeps every status 0..255 at every position;
(3) stress rewrote the first leg-status-named loop instead of the tally loop, false-rejecting auxiliary-loop copies
(HeldOutLoop-3 wrapper, HeldOutRefactor-a4 pre-count) -> v2 identifies the tally loop by dataflow (innermost `for`
governing the counting `case $st in`); (4) the harness check required exactly one `tblock=$(awk ...)` extraction line
and refused a second equivalent one (HeldOutRefactor-a3) -> v2 accepts >=1 and injects after the last. Also routed:
stdout-only comparison, a timeout on --then-regression. Counter: {E}/c1/c1-measure.py (label C1_R33_PASS); it refuses to
run unless a committed controls receipt names its own sha256 - the receipt is produced AFTER this wave, before any
held-out authoring, via `--write-controls`. Frozen before-values: {E}/before/c1-at-base.stdout (PASS=false) - the
runner_sha_ok=1 line shows the counter runs. Measurement happens in wave 2 on a FRESH sealed set authored after the
freeze, so your dev sweeps are the last cheap chance to break the tool before data.

C2 (freshness): repair the S055 digest drift (re-opened round 31, carried twice) - a new corpus/SOURCES.md row whose
teaches opens `supersedes S055 -` naming the VERSIONED url https://docs.python.org/3.15/library/doctest.html, pinned by
the committed snapshot {E}/c2/doctest-snapshot.html (sha256 217edd57...4899, frozen in the c2 counter). Counter:
{E}/c2/c2-measure.py (label C2_R33_PASS); before-value {E}/before/c2-at-base.stdout (row=none, false).

The L1 TameshiR33 holds the planner seat and is the sole integrator. You did not write the content you attack.
# Bounds (binding)
- Do exactly what your item names; verdict first, then evidence (path:line, exact commands with observed output), then the smallest safe correction.
- Your working directory is ONLY {S}/ (replace <your-name> with your item name exactly). One working directory per seat; never open another seat's scratch dir.
- Write NOTHING except your own report file and files inside your own scratch dir. Every `Report:` trailer path is relative to {LANE} - write it at {LANE}/<that path>, never at the fleet root {FLEET}.
- Never edit production files. Never run git write commands (add/commit/checkout/reset/stash/push/fetch/pull) in {LANE} or {FLEET}. Never run ANY `jj` command anywhere - not at the fleet root, not in {LANE}, not in a clone: any jj command snapshots a colocated working copy. Sandbox git (commits included) only in your own clone under {S}/, with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset. Never touch the fleet repo {FLEET}, sibling lanes, lane jj state or the lane Git index. Sibling repos are read-only.
- Code runs only inside your own scratch dir. The frozen counters are run only as your item names: control items use `--write-controls` with a `--receipt` path inside your own scratch; NEVER run the counters' default mode on lane bytes (that is the L1's measurement step, and the round-32 closure forbids counter runs outside their item). Wrap long runs in `timeout`; kill any process tree you started before you return.
- Never kill a process you did not start: before any kill, check that /proc/<pid>/cwd is inside your own scratch dir. Other seats run the same tools at the same time.
- No seat spawns, except an executor may spawn one read-only labrat probe for a falsifiable hypothesis.
- Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task - read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool, version, channel and reason in your report). Pacman guard: all pacman transactions are PAUSED host-wide; install via uv tool, npx or an official binary in ~/.local/bin, or file an L0 question; never -Sy/-Syu/-U/-R, never restart a host service.
- Receipt discipline (round-32 closure item 3): every command whose output you cite must have its exit code captured as `cmd; echo $? > file` - never `cmd && echo ...` (a failure would silently skip the capture).
- Time box: 40 minutes; a partial honest report beats none. Never pass a model.
- Disk: bound every file you write (no unbounded loops or appends); check `df -h /fast` before large builds. Never run du/find over /fast/scratch.
- Sourcing rule: open sources by ordinary means only (curl or a reader). Never use a headless browser or any other tool to pass a bot challenge, captcha or access control.
- Write plain English, no run-together words. No producer-authentication, promotion or numeric-score claims."""

items = []


def add(name, role, axes, target, acceptance=None):
    acceptance = acceptance or f'Report: {W}/{name}.md'
    prompt = '/skill:godspeed\n' + DIRECTIVE + '\n# Target\n' + target.replace('<your-name>', name) + '\n\n# Acceptance\n' + acceptance + '\n'
    items.append({'name': name, 'role': role, 'axes': axes, 'prompt': prompt})


CLONE = (f'mkdir -p {S} && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks {LANE} {S}/lane '
         f'&& env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C {S}/lane checkout -q --detach {FREEZE}')

# ---- pre-data controls (the committed receipt is assembled by the L1 from these four)
ctl_setup = (f'Pre-data control for claim C1. Setup: `{CLONE}`. Read {E}/contract.json (C1) and {E}/c1/c1-measure.py first. '
             f'Write ONE control tool (python3, self-contained) at {S}/ctl.py that mimics the interface of {TOOL} '
             '(final stdout line `TALLY_AUDIT: PASS|FAIL (...)`; exit 0/1) but shortcuts the audit. ')
ctl_run = (f'Then score it with the frozen counter, controls mode only: `timeout 2400 {CTR} --lane {S}/lane --rev {FREEZE} '
           f'--work {S}/w1 --write-controls {S}/ctl.py --receipt {S}/receipt.json` (a fresh empty --work per run; no --seed). '
           'Capture the exit as `cmd; echo $? > exitfile`. Paste the counter output verbatim and the full source of your control. '
           'Expected: your control\'s row shows predicate_pass=false and all_false=true (exit 0). '
           'A control with predicate_pass=true is a finding: say exactly which copies it got right and why the counter failed to catch the shortcut.')
add('CtlDoNothing', 'mutation-tester', ['operability'],
    ctl_setup + 'Your shortcut: exit 0 with `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` without reading the runner at all.' + ctl_run)
add('CtlAlwaysPass', 'mutation-tester', ['operability'],
    ctl_setup + 'Your shortcut: read the runner (so it looks busy) but always print PASS and exit 0.' + ctl_run)
add('CtlAlwaysFail', 'mutation-tester', ['operability'],
    ctl_setup + 'Your shortcut: always print `TALLY_AUDIT: FAIL (...)` and exit 1, even on the pristine runner.' + ctl_run)
add('CtlShaOnly', 'mutation-tester', ['operability'],
    ctl_setup + 'Your shortcut: sha256 the runner copy and compare it to the pristine runner\'s memorized digest; print FAIL if different, PASS if equal; run no tally logic.' + ctl_run)

# ---- dev sweeps against the frozen tool
sw_setup = (f'Dev sweep against the FROZEN tool v2 before any data seat. Setup: `{CLONE}`. The tool bytes at the freeze: '
            f'`git -C {S}/lane show {FREEZE}:tools/tally-audit-v2.py > {S}/tool.py`. The pinned runner: '
            f'`git -C {S}/lane show {FREEZE}:tools/mutate-and-run.sh > {S}/pristine.sh` (sha256 must be a7d3f2dd...2eb9 - verify). '
            f'Runner anatomy: run_regression() assigns 9 leg statuses `  st_x=$?` (the head), then a tally block starting '
            '`  local nlegs=9 npass=0 nfail=0 nsetup=0 st` with one `for st in ...; do case $st in` counting loop, guarded '
            'sums, and printf REGRESSION lines; a selftest harness (`local tblock`..`tblock=$tblock_full`) sits elsewhere in the file. '
            'Generate single-edit (or, where your item says, two-edit) mutants of the runner BY EXACT STRING replacement '
            '(assert your old-string occurs exactly once before applying; discard no-ops), run `timeout 300 python3 {S}/tool.py '
            '--runner {S}/m.sh` per mutant, and collect verdicts. For every mutant the tool PASSES (exit 0), decide whether it is '
            'behaviorally equivalent to pristine: run the pristine tally block and the mutant tally block on the status vector '
            'yourself in bash (recipe: a function `tally() { local st_js=${1} ... st_citecheck=${9}; local root=r auto=0 KEEP=1; '
            '<block>; }` then `out=$(tally <9 statuses>); echo $?:${out%%$\'\\n\'*}`) and search vectors (single statuses 0..255 at '
            'each position; a few (fail,setup) mixes). If you find a differing vector, you have a SURVIVOR: report its exact edit, '
            'the witness vector, and the two differing outputs. If none, say so and attach your sweep log (mutant ids, edits, verdicts). ')
add('DevArm', 'mutation-tester', ['operability', 'depth'],
    sw_setup + 'Your family: the `case $st in` arms - altered patterns (00, +1, quoted), extra arms, reordered arms, fall-through '
    '(;&/;;&), arithmetic inside arms, arms keyed on other vars. >= 24 mutants. Find a survivor the all-statuses sweep still misses, if one exists.')
add('DevGuard', 'mutation-tester', ['operability', 'depth'],
    sw_setup + 'Your family: the guard block `if (( npass + nfail + nsetup != nlegs ))` and the FAIL/SETUP precedence ifs - '
    'boundary comparisons (<, <=, >, ==), added conjuncts/disjuncts, swapped precedence, early exit changes. >= 24 mutants. '
    'Pay special attention to guards a (failing,setup) count sweep plus dup/drop stress might both miss.')
add('DevPrintf', 'mutation-tester', ['operability', 'depth'],
    sw_setup + 'Your family: the printf REGRESSION lines - swapped count fields, %-s vs %d, dropped fields, extra fields, wrong '
    'wording that still prints the counts (e.g. `failed=` relabeled), REGRESSION_WORKDIR lines changed. >= 24 mutants. '
    'Remember the oracle compares the exact stdout first line AND the exit code.')
add('DevLoopOps', 'mutation-tester', ['operability', 'depth'],
    sw_setup + 'Your family: the tally loop itself - operand permutation, duplication, omission, `for st in` -> `for st in '
    '${arr[@]}`, indirect expansion, a nested inner loop, a `continue`/`break`. Also: an auxiliary loop added BEFORE the tally '
    'loop (a pre-count) or WRAPPING it (single-iteration wrapper) that must NOT be flagged. >= 24 mutants, at least 6 benign.')
add('DevHead', 'mutation-tester', ['operability', 'depth'],
    sw_setup + 'Your family: the leg-status assignments OUTSIDE the tally block - masked captures (`st_x=$(($? & 127))`), '
    'overwrites (`st_x=0` after the assignment), swapped legs, captures from a different variable, double assignment, and '
    'assignments hidden in conditionals between the legs. >= 24 mutants. The tool\'s head check and the runtime sweep must '
    'catch these; a survivor here is the most dangerous class because --regression itself would print a wrong verdict.')
add('DevHarness', 'mutation-tester', ['operability'],
    sw_setup + 'Your family: the selftest harness region (`local tblock` .. `tblock=$tblock_full`) - weakened comparisons, '
    'skipped positions or vectors, swallowed statuses, exit-only checks, a second equivalent `tblock=$(awk ...)` extraction '
    'line (benign), extraction pattern loosened. >= 20 mutants, at least 4 benign. A benign variant the tool false-rejects '
    '(exit != 0) is also a finding: report it as a FALSE REJECT with the edit.')
add('DevStderr', 'mutation-tester', ['operability'],
    sw_setup + 'Your family: output-channel tricks - junk printed to stderr by the tally block, stderr-only verdict lines, '
    'stdout closed early, printf to fd 3, a block that prints the right first line but wrong exit via a trap. >= 16 mutants. '
    'The tool must compare stdout only; a stderr-channel survivor means the stdout-only rule is not actually enforced.')
add('DevMulti', 'mutation-tester', ['operability'],
    sw_setup + 'Your family: TWO-edit mutants (one in the tally block, one in the head or harness) chosen so each edit alone '
    'is caught but the pair might slip (interactions between masking and guard stress, arm edits and printf swaps). >= 24 mutants. '
    'Any pair where the tool passes and the behavior differs from pristine on some vector is a survivor.')
add('DevStatusEdge', 'mutation-tester', ['operability'],
    sw_setup + 'Your family: status semantics at the edges - vectors with statuses 255 at the last position, repeated '
    'non-zero statuses, all-setup and all-fail extremes with nlegs operands stressed, and bash-specific values (negative '
    'exit arguments are impossible via $?, but try statuses expressed as arithmetic like $((256+1)) inside mutant blocks). '
    '>= 20 mutants. Try to make the tool\'s own driver (run_vectors) mis-count results rather than the runner itself.')
add('DevNlegs', 'mutation-tester', ['operability'],
    sw_setup + 'Your family: the nlegs declaration and its uses - `local nlegs=9` -> 8/10, `$nlegs` replaced by a literal in '
    'one printf but not another, nlegs recomputed after the loop. >= 16 mutants. The static check and the oracle both key on '
    'nlegs; find a split they disagree on, if one exists.')
add('DevAccept', 'mutation-tester', ['operability'],
    sw_setup + 'Your family is BENIGN edits that must NOT be flagged: comment additions, whitespace-only changes, renamed '
    'local variables outside the tally path, reordered independent functions, an unused variable, a second extraction line '
    '(as round-32 HeldOutRefactor-a3), a wrapper loop (HeldOutLoop-3), a pre-count loop (HeldOutRefactor-a4). >= 20 variants. '
    'Every false reject (tool exit != 0) is a finding: report the edit and the failing check line. All-clear only if every '
    'benign variant passes.')

# ---- reviews and audits
add('ReviewCounterA', 'reviewer', ['calibration'],
    f'Adversarial review of the frozen C1 counter {E}/c1/c1-measure.py against its contract {E}/contract.json (C1). Verify the '
    'round-32 routed defects are actually fixed: witness loop/vector names validated before bash use; a non-string witness is '
    'ho_invalid (no crash); held-out discovery is recursive. Then attack: (a) the controls gate - can a committed receipt name '
    'the counter sha256 while recording all_false=true without controls having failed (forge paths: receipt written by hand, '
    'counter self-sha read from the wrong revision, git show ambiguity); (b) copy-order or seed side channels in score_tool; '
    '(c) witness verification gaps - a kill copy whose edits change the block but keep witness-vector behavior identical, or '
    'whose witness vector has length != 9; (d) freeze check bypasses (adding_commit on a path that also existed at the freeze). '
    'For each finding give a concrete exploit sketch or run it in your scratch if possible. Verdict: sound / defects listed.')
add('ReviewCounterB', 'reviewer', ['calibration'],
    f'Review the C2 counter {E}/c2/c2-measure.py against contract C2 and the SOURCES contract v1 ({FLEET}/CORPUS.md). Check: row '
    'parsing (cell positions in the 13-field table), the versioned-URL regex, the snapshot/lesson digest comparison (could a '
    'lesson mention a DIFFERENT sha256 that also appears, e.g. the fetch receipt\'s, and pass gate_sha_ok without the Gate '
    'recording the snapshot digest?), the quote check, and the row-absent before-state. Confirm the counter reads everything '
    'from REV (no worktree dependence). Run it at --rev ' + FREEZE + ' (expect row=none, false, exit 1) and at the base '
    + BASE + ' (same) with exits captured. Report defects or confirm soundness with the receipts.')
add('CriticCounter', 'critic', ['calibration'],
    f'Falsify the counters\' shared assumptions: (1) the runner pin a7d3f2dd...2eb9 - verify it equals `git -C {LANE} show '
    f'{FREEZE}:tools/mutate-and-run.sh | sha256sum`; (2) the tool pin 9dbbce62...33a4 at the freeze; (3) bwrap exists and '
    'v1.run_tool\'s sandbox flags (--unshare-all --die-with-parent --new-session --clearenv --ro-bind/--bind) actually prevent '
    'a malicious copy from reading the lane (construct a copy that tries to `cat ' + LANE + '/corpus/SOURCES.md` from inside '
    'the audit path? no - the tool never runs copy code; instead check what the COUNTER runs under bwrap in block_run and '
    'whether a mutant tally block could escape /w or survive the timeout); (4) the public panel - recount the frozen/generated '
    'families in the round-32 v1 counter (18 kill + 8 accept) and confirm none is trivially equivalent to pristine. '
    'Every claim needs a command and its observed output.')
add('ReviewTool', 'reviewer', ['operability'],
    f'Review {TOOL} (bytes at {FREEZE}) for faithfulness and shortcuts. (1) Replay check: the selftest seeds must match the '
    f'round-32 held-out classes - compare the v2 selftest edits byte-wise against {LANE}/.ufo/evidence/round-32/heldout/*.json '
    '(mask 7-bit = HeldOutLoop-1, wrapper = HeldOutLoop-3, pre-count = HeldOutRefactor-a4, second extraction = -a3, printf '
    'swap = -Printf-1, majority guard = -Guard-1, double count = -TallyArms-01); list any class with NO selftest seed. '
    '(2) Shortcut hunt: does the tool string-match known fault patterns, read held-out paths, or embed memorized mutant '
    'digests instead of auditing? (3) Verify the stdout-only claim and the --then-regression timeout by reading the code and '
    'running one probe each in your scratch. Report with path:line evidence.')
add('CriticTool', 'critic', ['operability'],
    f'Make the strongest honest case that {TOOL} still misses a class the round-32 held-out authors would have caught. '
    'Candidates to evaluate concretely (build the mutant in your scratch and test, do not argue from the armchair): faults '
    'between run_regression\'s closing constructs the block extraction might mis-slice; case arms keyed on the loop VARIABLE '
    'name rather than `st`; an `until`/`while` tally loop instead of `for`; a tally block that reads a leg twice via '
    'indirection; nlegs correct but a printf using a stale variable. If you produce a survivor or a false reject, it is a '
    'round-blocking finding. If every candidate is caught, paste the mutants and verdicts as the sweep.')
add('ReviewContract', 'reviewer', ['calibration'],
    f'Adversarial read of {E}/contract.json: universal clauses beyond enumerated sets; predicates whose truth a do-nothing '
    'control could reach (name the control); kill-rule gaps (what counts as "the first full run"; are seat re-runs '
    'observations or scorers; when exactly is the measurement revision chosen); amendment procedures (is a tool re-pin before '
    'any data run still the claim\'s rule - compare the round-32 closure\'s amendment-2 ruling); C2\'s lesson-digest coupling '
    '(the Gate must record the snapshot digest - what if the scribe writes a different digest sentence the regex still '
    'matches?). Recommend the exact sentence fixes; the L1 freezes amendments before data.')
add('ReviewFreeze', 'reviewer', ['calibration'],
    f'Conformance audit of the freeze commit {FREEZE}: `git diff-tree --name-status -z --no-renames {BASE} {FREEZE}` against the '
    f'contract\'s claimed frozen_artifacts (paths + sha256s: tool 9dbbce62...33a4, snapshot 217edd57...4899, runner untouched '
    f'a7d3f2dd...2eb9, SCORECARD.md/LOG.md/corpus byte-identical to {BASE}); verify {E}/before receipts carry real exits captured '
    'as `cmd; echo $? >` (not &&) and predate the freeze; verify the dev selftest receipt 21/21 exit 0. Any unexpected path or '
    'missing receipt is a conformance defect: name it.')
add('LedgerAudit', 'reviewer', ['calibration'],
    f'Read {LANE}/.ufo/evidence/round-21/coldread/ledger.json (the cold-read ledger) and the strict monitor '
    f'{LANE}/.ufo/evidence/round-21/coldread/measure.py: run the monitor at {FREEZE} (fresh --work) and file the receipt in your '
    'report; list which sections cite files this round will touch (tools/*, corpus/SOURCES.md, LOG.md, SCORECARD.md) so the '
    'L1 can size wave 2\'s cold-read seats. Do NOT run the default-mode C1 counter; this item is the monitor only.')
add('PanelCheckA', 'reviewer', ['operability'],
    f'Calibrate the public panel. Setup: `{CLONE}`. Score the FROZEN V1 tool `git -C {S}/lane show {BASE}:tools/tally-audit.py` '
    f'against the public families with the round-32 v1 counter in your scratch: `python3 {LANE}/.ufo/evidence/round-32/c1-measure.py '
    f'--lane {S}/lane --rev {FREEZE} --work {S}/w1` and a second run with `--seed 0123456789abcdef`. Expected: v1_kill=18/18 '
    'v1_accept=8/8 PASS=true both runs (the panel is live and the v1 tool still meets it). Then score the FROZEN V2 tool the '
    'same way (same counter, v1 panel): expected v2 also 18/18 8/8. Any deviation is a finding. Exits captured per the receipt '
    'discipline. Paste all summary lines.')
add('PanelCheckB', 'reviewer', ['operability'],
    f'Independent repeat of PanelCheckA with different seeds (your choice, two runs): v1 tool and v2 tool against the public '
    f'panel via the round-32 v1 counter in your own scratch clone at {FREEZE}. Purpose: seed-independence of the panel verdict. '
    'Paste summary lines and exits.')
add('SentinelSandbox', 'sentinel', ['operability'],
    f'Security review of the C1 measurement path. bwrap is used in (a) v1.run_tool (tool + one copy) and (b) the c1 counter '
    'block_run (a seat-authored MUTANT bash block). List what a malicious mutant block could attempt at counter time (write '
    'outside /w, network, fork bombs, reading /proc for lane data) and test one bounded probe of each in your scratch against '
    'the actual bwrap invocation (read the flags first; note --dev /dev and --proc /proc are bound in block_run - judge '
    'whether that is a gap and recommend the minimal flag fix if so). Also review the held-out JSON contract (edits are '
    'exact-string; the mutated file is the only thing executed) and recommend the authoring bounds for wave 2. No production '
    'changes; report only.')
add('RevengerWitness', 'revenger', ['calibration'],
    f'Reverse-engineer the witness semantics of {E}/c1/c1-measure.py. Questions to settle by experiment in your scratch: '
    '(1) a kill copy whose tally block differs textually but is behaviorally identical on EVERY 0..255 vector at every '
    'position (e.g. an added comment inside the block) - the counter runs only the witness vector, not the full sweep: show '
    'whether such a copy would be scored by ho_witness_ok (pristine-block vs mutated-block differ? run the counter\'s own '
    'block_run logic on a comment-only mutant) and argue whether ho_invalid is the RIGHT verdict for it; (2) a kill copy with '
    'witness vector length 4 - validate_ho accepts it (ints 0..255); does block_run then mis-compare? (3) the kind=head '
    'witness: construct a head edit that changes the head text but cannot change any --regression outcome (rename an unused '
    'variable in the head) - should it be kill or invalid? Recommend the exact counter patch for each gap, or argue none is '
    'needed. Do not edit the counter; report.')
add('SrcDoctestReopen', 'scout', ['freshness'],
    f'Source opening for C2. Re-open https://docs.python.org/3.15/library/doctest.html by ordinary curl (no headless browser): '
    'record HTTP status, byte count, sha256 (must equal 217edd573ef328316ac2410e5d046c5ad3a2df522270e5868bc5e5e5eb744899 - the '
    f'frozen snapshot {E}/c2/doctest-snapshot.html; `cmp` your fetch against the snapshot). Locate the module-introduction '
    'bullet and extract its first sentence as a <=25-word quote with its location. Draft, as plain text in your report: (a) the '
    'SOURCES.md row for id S100 (11 columns per the contract in ' + FLEET + '/CORPUS.md; teaches cell opens '
    '`supersedes S055 - the /3/ alias drifts; this pins the 3.15 build`; tier A; scope executable documentation examples; '
    'anchor names the version; used-by names corpus/lessons/round-33.md and corpus/knowledge/executable-self-assessment.md) '
    'and (b) the lesson Gate bullet (URL, access date 2026-10-23, bytes, sha256, the quote). The L1 integrates both.')
add('ReviewSrcDoctest', 'reviewer', ['freshness'],
    f'Independent verification for C2. (1) `sha256sum {E}/c2/doctest-snapshot.html` equals the contract pin and the digest in '
    f'{E}/c2/fetch-receipt.txt; the receipt records two fetches and the versioned URL. (2) The frozen URL form is versioned '
    '(docs.python.org/3.15/) and the snapshot contains the quoted sentence. (3) Independently curl the URL once: status, bytes, '
    'sha256 - must equal the snapshot (live stability check). (4) Review the S100 row draft and Gate bullet draft produced by '
    'seat SrcDoctestReopen (read their report file when present, else do the draft review against the contract yourself and say '
    'so). List any contract violation cell by cell.')
add('SrcPitestReopen', 'scout', ['freshness'],
    f'Source recheck for S099 (https://pitest.org/, tier A for mutation-adequacy vocabulary; recheck 180d from round 32, due '
    'this round). Curl the page: record status, bytes, sha256; compare with the round-32 Gate digest b0c7e050...10cc. Extract '
    'one <=25-word quote about mutation testing adequacy DIFFERENT from the round-32 quote ("The quality of your tests can be '
    'gauged from the percentage of mutations killed."), with its location. Verdict: unchanged (digest equal) or drifted (digest '
    'differs - then quote the live bytes and recommend a supersedes row). This recheck feeds the round-33 lesson Gate.')
add('ConnectorOverlap', 'connector', ['adjacency'],
    f'Sibling-overlap scan (adjacency import only, never absorption). This session\'s sibling rounds: chousa r34 (deep-research '
    f'method), kotoba r60, mado r27, kama r29, kake r42, kumitate r48. Search their committed waves/reports for work that '
    f'overlaps tameshi r33: auditing {LANE}/tools/mutate-and-run.sh or any lane\'s --regression tally, mutation-testing tool '
    'craft, or sealed held-out designs. Look under ' + FLEET + '/.ufo/reports/round-3*/ and ' + FLEET +
    '/.ufo/waves/ plus each sibling lane repo\'s .ufo/waves/ (read-only). Return up to 3 rows as path@hash with a one-line '
    'note on what tameshi could import; if none, paste the sweep (commands + hits/empty) that found none.')
add('CensusStart', 'scribe', ['freshness'],
    f'Census receipt for the round start. Run `TZ=UTC bash {FLEET}/scripts/sources-census.sh validate --root {FLEET} tameshi` '
    f'and capture exit; run the seven frozen manual census commands from {FLEET}/CORPUS.md §SOURCES against {LANE}/corpus/SOURCES.md '
    f'(rows, malformed, tier histogram, status histogram, duplicate ids, enum violations, mined used-by existence). File all '
    'outputs under your report; the L1 re-runs the same at round end for the before->after record. Receipt discipline: `cmd; '
    'echo $? > file` for every command.')
add('ScribeLesson', 'scribe', ['quality'],
    f'Prepare the round-33 lesson skeleton at your scratch (the L1 commits it): mirror the shape of {LANE}/corpus/lessons/round-32.md '
    '- title + base + L1 line + round order, `## Gate` (empty subsections: opened/rejected/row changes, to be filled from seat '
    'reports), `## Mistakes` (empty), `## Holds` (empty), routed-items section. Do NOT invent content; the skeleton only. '
    'Also draft the `## Gate` bullets for S100 and the S099 recheck as fill-in templates with <...> slots.')

spec = {'wave': 'round-33-w1', 'reportDir': W, 'context': CONTEXT, 'items': items}
out = Path(__file__).with_name('spec-w1.json')
out.write_text(json.dumps(spec, indent=1))
print('wrote', out, 'items', len(items))
