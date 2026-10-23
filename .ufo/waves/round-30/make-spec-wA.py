#!/usr/bin/env python3
"""Round 30 attempt 2, wave A (policy v1): the pre-data control wave against the frozen C1
counter v4 (one seat per shortcut shape), plus data-independent work in the same window:
source re-opens, no-harm runs on the frozen fix (witness), attacks on the fix, re-verification
of attempt-1 commits, draft repairs. Cold reads wait for the content revision (wave B).
Usage: make-spec-wA.py   (writes spec-wA.json next to this file)
"""
import json
from pathlib import Path

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
FROZEN = 'f09d3425258403a51422c9959e25340807982947'
BASE = '9ed6db840dc97a0a5f4758b6b5f60cee83a61645'
A1 = '8a8d25401413b76fb32b691412c9e1b1c83f2fed'
E = LANE + '/.ufo/evidence/round-30'
W = '.ufo/waves/round-30/wA'
SEALDIR = '/fast/scratch/hyaku/tameshi-r30a2'
DIRECTIVE = Path('/home/vgpnk/.agents/skills/godspeed/directive.md').read_text()
BLOCK = 'e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d'

CLONE = (f'`S=/fast/scratch/hyaku/tameshi-r30a2-seats/<your-name>; mkdir -p $S; env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE '
         f'git clone -q --no-hardlinks {LANE} $S/clone && git -C $S/clone checkout -q --detach {FROZEN}`')
WITNESS = (f'{CLONE}, then `cd $S/clone && git apply {E}/witness/fix.diff` (this is the frozen fix: the runner the round will land; '
           f'its tally block sha256 is {BLOCK})')
V3 = f'timeout -k 5 1500 python3 {E}/c1-measure-v3.py --repo $S/clone --rev <your commit> --jobs 4'

CONTEXT = f"""# Goal
Tameshi round 30 (verification-fixture craft), attempt 2, wave A (policy v1): the pre-data control wave plus data-independent work.
One measured claim, C1 (axis operability; surface = the `--regression` case-tally block of {LANE}/tools/mutate-and-run.sh and its `--selftest` detector;
routed item 7 of {LANE}/corpus/lessons/round-29-verifier-spotcheck.md). Frozen counter v4: {E}/c1-measure-v4.py (contract {E}/contract.json and
amendments 1-3; amendment 3 is {E}/contract-amendment-3.json, landed at lane commit {FROZEN}). v4 adds a SEALED set of 6 mutants and 6 equivalent rewrites
of the fix's tally block; only its sha256 is committed. The frozen fix is {E}/witness/fix.diff (runtime completeness guard + a behavioral selftest that runs the
extracted tally block under 19 fixed status vectors). Control seats build the cheapest program that meets the counter WITHOUT doing the claimed work;
the L1 (TameshiR30A2, planner seat and sole integrator) scores every control under v4 with the sealed file and commits the receipts before any data.
A control that meets the counter is the most valuable result: build it honestly and as strong as you can. You did not write what you attack.
# Bounds (binding)
- Do exactly what your item names; verdict first, then evidence (path:line, exact commands with observed output), then the smallest safe correction.
- NEVER open, list, search for or read anything under {SEALDIR} (the sealed set lives there); never try to recover the sealed items. A control built from them is void.
- Write NOTHING except your own report file and the files your item names under {E}/wA/. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>, never at the fleet root {FLEET}.
- Never edit production files in {LANE}. Never run git write commands (add/commit/checkout/reset/stash/push/fetch/pull) in {LANE} or {FLEET}. Never run ANY `jj` command anywhere.
  Never touch the fleet repo {FLEET}, sibling lanes, lane jj state or the lane Git index. Read-only git with GIT_OPTIONAL_LOCKS=0 is fine. Sibling repos are read-only.
- Code runs only inside your own clone under /fast/scratch/hyaku/tameshi-r30a2-seats/<your-name>/ with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset; git commits are allowed ONLY in that clone.
  Never run gates, selftests or sweeps in {LANE} itself. Wrap every long run in `timeout` (cap jobs at 4); kill any process tree you started before you return.
- Never kill a process you did not start: before any kill, check that /proc/<pid>/cwd is inside your own scratch dir. Other seats run the same tools at the same time.
- No seat spawns, except an executor may spawn one read-only labrat probe for a falsifiable hypothesis.
- Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool, version, channel and reason in your report). Pacman guard: all pacman transactions are PAUSED host-wide; install via uv tool, npx or an official binary in ~/.local/bin, or file an L0 question; never -Sy/-Syu/-U/-R, never restart a host service.
- Time box: 35 minutes; a partial honest report beats none. Never pass a model.
- Sourcing rule: open sources by ordinary means only (curl, a plain fetch). Never use a headless browser or any tool to pass a bot challenge, captcha or access control.
- Write plain English, no run-together words. No producer-authentication, promotion or numeric-score claims."""

items = []


def add(name, role, axes, target, acceptance=None):
    acceptance = acceptance or f'Report: {W}/{name}.md'
    prompt = '/skill:godspeed\n' + DIRECTIVE + '\n# Target\n' + target + '\n\n# Acceptance\n' + acceptance + '\n'
    items.append({'name': name, 'role': role, 'axes': axes, 'prompt': prompt})


CTL_TAIL = (f' Keep the tally block byte-identical to the fix (`python3 -c "import hashlib,sys;t=open(sys.argv[1]).read();s=t.find(\'  local nlegs=9 npass=0 nfail=0 nsetup=0 st\\n\');e=t.find(\'\\n}}\\n\',s);print(hashlib.sha256(t[s:e+1].encode()).hexdigest())" tools/mutate-and-run.sh` must print {BLOCK}); '
            f'replace ONLY the fix\'s behavioral selftest hunk (the lines from `# r30: --regression case-tally behavior` through the last `done` before `bash "$SELF" --help`) with your detector. '
            f'Commit in your clone, score it yourself with the public v3 counter `{V3}` (paste the summary and exit), and write `cd $S/clone && git diff {FROZEN} HEAD -- tools/mutate-and-run.sh > {E}/wA/<your-name>.diff`. '
            f'Report the commit id, the clone path, the diff path and the runner sha256. The L1 scores it under v4. First line of the report: `CONTROL <your-name>: v3_meets=<true|false> built=<yes|no>`.')
add('CtlS1Normalize', 'mutation-tester', ['operability'],
    f'Control, shape "static normalizer": {WITNESS}. Build a selftest detector that NEVER runs, sources or evaluates the tally block. It canonicalizes the block text (whitespace, comments, '
    f'arithmetic spellings such as `x=$((x+1))`/`((x++))`/`((++x))`/`x=$((x - -1))`, test spellings `-gt 0`/`!= 0`/`(( x ))`/`-ge 1`, case patterns, operand order) and accepts iff the canonical form equals the fix\'s canonical form. Make it as general as you can so that unseen equivalent rewrites still pass.' + CTL_TAIL)
add('CtlS2SymEval', 'mutation-tester', ['operability'],
    f'Control, shape "static symbolic evaluator": {WITNESS}. Build a detector (python inside the selftest is fine) that parses the block into its own model (loop operands, case arms, counter updates, if-checks, exit codes, printed first lines) '
    f'and computes the expected verdict for the 19 status vectors WITHOUT executing the bash block (no bash, eval, source or subprocess on block text). Accept iff the model\'s results equal the fix\'s. This tests whether "behavioral" can be met by a static interpreter.' + CTL_TAIL)
add('CtlS3DenyList', 'critic', ['operability'],
    f'Control, shape "default accept, deny known mutant shapes": {WITNESS}. Build a detector that accepts any block except those matching the mutant shapes the public generators make (read heldout() and inserted() in {E}/c1-measure-v3.py: dropped operands, wrong counters, arm swaps, thresholds, inserted non-zero terms) and the 13 family mutants.' + CTL_TAIL)
add('CtlS4Sniff', 'mutation-tester', ['operability'],
    f'Control, shape "environment sniffing" (keys on the run, not the block): {WITNESS}. v4 runs each selftest in a bubblewrap sandbox (read BWRAP and selftest() in {E}/c1-measure-v4.py). Build a detector that tries to tell the pristine job from mutant jobs by anything other than running the block: '
    f'file mtimes or sizes in /w/tools, /proc contents, hostname, environment, timing, open file descriptors, inode numbers, the order of jobs. Run the v4 sandbox command yourself on your clone to see what is visible (copy BWRAP from the counter; bind your own tools copy at /w). Report each channel you tried and what it showed.' + CTL_TAIL)
add('CtlS6PartialRun', 'mutation-tester', ['operability'],
    f'Control, shape "reduced work": {WITNESS}. Replace the behavioral selftest with the cheapest partial run: run the extracted block under ONE status vector only (all zero), or under the all-zero vector plus a static check of the rest. Pick the cheapest variant you believe meets the counter.' + CTL_TAIL)
add('CtlS7Metadata', 'mutation-tester', ['operability'],
    f'Control, shape "content-free metadata": {WITNESS}. Build a detector keyed on cheap metadata of the block only: line count, byte length, count of `+ 1`/`exit` tokens, the multiset of tokens, or a fuzzy hash, with a tolerance band you choose so that rewrites of similar size pass and mutants fail.' + CTL_TAIL)
add('CtlS8TokenBag', 'critic', ['operability'],
    f'Control, shape "bag of required tokens": {WITNESS}. Build a detector that greps the block for a set of required substrings (each operand name, each counter name, each exit code 0/1/2, each first-line text) and a set of forbidden substrings (for example `npass + 0`, `-gt 1`), never running it.' + CTL_TAIL)
add('CriticV4Design', 'critic', ['operability'],
    f'Adversarial review of the frozen counter v4 before data. Read {E}/c1-measure-v4.py, {E}/contract-amendment-3.json, {E}/contract.json, amendments 1-2 and the receipts in {E}/v4/. Do NOT open {SEALDIR}. '
    f'(1) Name every shape of runner that could meet v4 without its selftest running the tally block, and say why it would or would not pass (j) and (k). (2) Is the predicate the same sentence in amendment 3, the same condition in the code (`ok = ...`) and the same label in the receipts? Quote each. '
    f'(3) Does `git -C {LANE} diff {A1} {FROZEN} -- .ufo/evidence/round-30/` show v4 frozen before any data (no runner change in the lane)? (4) Is an L1-authored sealed set acceptable under the contract\'s hold rule, given the attempt-1 seat SealHeldout died? Verdict first per question.')
add('SentinelBwrap', 'sentinel', ['operability'],
    f'Security attack on v4\'s selftest sandbox (BWRAP list and selftest() in {E}/c1-measure-v4.py). In your own scratch dir, reproduce the exact bwrap invocation around a probe script bound at /w and report what a selftest can see or reach: /proc (pid 1, parent cmdline), /sys, /dev, network, the host filesystem outside /usr and /etc, '
    f'environment, other jobs\' directories, writable paths that persist between jobs. Never read {SEALDIR}; to test whether it is reachable, only test existence of the directory path from inside the sandbox. Verdict: can a selftest inside the sandbox learn which job it is, or read the counter, its argv or the lane?')
add('ProbeSealedReach', 'mutation-tester', ['operability'],
    f'One falsifiable hypothesis: "inside v4\'s bwrap sandbox, no path that contains the string `tameshi` or `c1-sealed` is reachable". Build a probe runner in your own clone ({CLONE}) whose --selftest runs `find / -xdev -path /proc -prune -o \\( -name \'*tameshi*\' -o -name \'*c1-sealed*\' \\) -print 2>/dev/null | head -20` and prints the count; '
    f'run it under the exact BWRAP list from {E}/c1-measure-v4.py with your tools copy at /w. Report the command and its output. Do not open anything you find; print paths only.')
add('ReopenS059', 'scout', ['freshness'],
    f'Frontier step, routed debt (spot-check routed item 7, first bullet: the S059 supersedes row). Re-open `curl -sSL https://bazel.build/remote/caching.md` twice about 30 s apart; sha256 each; compare with {E}/sources/S059-bazel-remote-caching.md and with row S059 in `git -C {LANE} show {FROZEN}:corpus/SOURCES.md`. '
    f'Locate "Bazel does not track tools outside a workspace" (line numbers) and give a <=25-word quote. Read {FLEET}/CORPUS.md section "SOURCES.md — where a shokunin learns": what exact shape must a supersedes row have (column order, `supersedes S0NN —` opening)? Draft that row for id S092 in your report.')
add('ReopenS087', 'scout', ['coverage'],
    f'Frontier step: re-open S087 by ordinary means: `curl -sSL -o <your scratch>/m.tgz https://registry.npmjs.org/mutation-testing-metrics/-/mutation-testing-metrics-3.9.0.tgz`; compute sha512 (base64) and sha256; compare with row S087 (`git -C {LANE} show {FROZEN}:corpus/SOURCES.md`) and {E}/sources/S087-mutation-testing-metrics-3.9.0.tgz. '
    f'Extract and quote (<=25 words each, with path:line) the lines where the library computes totals as sums of per-state counts (package/src/model/metrics.ts, package/src/calculateMetrics.ts). Does the source support "a total must equal the sum of per-state counts" as the C1 fix\'s rationale (fix comment in {E}/witness/fix.diff)? Agree or disagree.')
add('ScoutBwrapSource', 'scout', ['freshness'],
    f'Frontier step: v4 rests on bubblewrap isolation. Open by ordinary means the bubblewrap manual (`man bwrap` locally, bwrap 0.13.1, and the upstream https://github.com/containers/bubblewrap README or bwrap.xml). Give the exact documented meaning of --unshare-all, --clearenv, --proc, --tmpfs, --die-with-parent, --new-session with <=25-word quotes and locators, and any documented caveat (for example --unshare-all and user namespaces, what remains shared). '
    f'Draft a SOURCES row (contract: {FLEET}/CORPUS.md section "SOURCES.md — where a shokunin learns") for id S093 in your report, with URL, tier, scope, anchor and the lesson it teaches for counter design.')
add('ScoutHoldoutSource', 'scout', ['coverage'],
    f'Frontier step: find and open ONE primary source on keeping a held-out evaluation set secret so a candidate cannot overfit the test (for example Dwork et al. 2015, "The reusable holdout", Science 349(6248); or a mutation-testing paper on held-out or hidden mutants). Open it by ordinary means (publisher page, arXiv, author PDF); no paywall bypass. '
    f'Give URL, access date, a <=25-word located quote and what it teaches about a sealed set committed by hash before data. Draft a SOURCES row for id S094 (contract: {FLEET}/CORPUS.md section "SOURCES.md — where a shokunin learns").')
add('PilotBind', 'executor', ['calibration'],
    f'Routed item 2/3 pilot (QUALITY draft criterion 60: a binding check runs on real assembled entries before it is frozen). Read {E}/coldread/bind-select.py (attempt-1 draft, untrusted). Run it on round-29 data: `--assembled {LANE}/.ufo/evidence/round-29/coldread/assembled-w1.json --registry {LANE}/.ufo/waves/round-29/w1/swarm-registry.json '
    f'--sessions ~/.omp/agent/sessions/-Projects-shokunin/2026-10-23T00-54-50-959Z_01a16640-e34f-76e4-8a3b-4d245a8bb241/TameshiR29 --prefix TameshiR29. --out {E}/wA/pilot-bound.json --receipt {E}/wA/pilot-receipt.json` (adjust --sessions if the transcripts sit elsewhere; find them with ls). '
    f'Report kept/excluded with reasons, check 3 kept bindings by hand (transcript exists, sha256 matches, contains `COLDREAD <seat>:`), and name any defect in the script (for example a report path resolved relative to the cwd).')
add('ReviewQualityDraft', 'reviewer', ['quality'],
    f'Review the attempt-1 uncommitted draft criteria 58-63 (`git -C {LANE} diff -- corpus/QUALITY.md`, read-only) against bytes: each Falsifier pointer ({E}/r29-mistake1-ordering.txt, {E}/drift-sim-union4.txt, {LANE}/.ufo/evidence/round-29/coldread/select-receipt-w1.json, {LANE}/.ufo/waves/round-29/spec-w1.json, round-29 contract.json) and the routed items 1-7 of {LANE}/corpus/lessons/round-29-verifier-spotcheck.md. '
    f'Is each criterion true, checkable and able to fail? Which routed item has no criterion? Propose one criterion for the round-30 lesson "a counter must not leak job labels to the program it judges" (control K9, {E}/v4/K9-on-draft.stdout). List exact wording fixes.')
add('ScribeEntry', 'scribe', ['quality'],
    f'Redraft the knowledge entry {LANE}/corpus/knowledge/regression-tally-completeness.md (attempt-1 draft, untrusted; read it) so every statement matches committed bytes: the fix {E}/witness/fix.diff, counters v1-v4 and contract amendments 1-3 under {E}/, the control receipts {E}/ctl/ and {E}/v4/, MutateLegSum {LANE}/.ufo/waves/round-29/w1/MutateLegSum.md, source S087. '
    f'The entry must not state the head result (not measured yet) and must not quote the sealed items. Keep the header shape of sibling entries in {LANE}/corpus/knowledge/. Write the full redraft to {E}/wA/ScribeEntry-draft.md and list every change from the attempt-1 draft with its evidence.')
add('ScribeMistakes', 'scribe', ['calibration'],
    f'Draft `## Mistakes` rows for corpus/lessons/round-30.md (format: class · evidence pointer · captured-by · fix; a fix counts only once shown able to fail). Mine: the v1→v2→v3→v4 counter history (each a control or self-attack meeting the counter before data: {E}/contract-amendment-1.json, -2, -3); the v4 draft label leak (K9, {E}/v4/K9-on-draft.stdout); '
    f'the attempt-1 orchestrator death leaving uncommitted scratch (`git -C {LANE} status --porcelain`); round-29 routed items ({LANE}/corpus/lessons/round-29-verifier-spotcheck.md). For each give the command whose output shows the check failing on the old state. Write rows in your report only.')
add('RegressionReplay', 'executor', ['operability'],
    f'No-harm, operability: the full ledger replay must still pass with the frozen fix. Build a fleet mirror: `W=/fast/scratch/hyaku/tameshi-r30a2-seats/<your-name>; mkdir -p $W/fleet; for d in {FLEET}/*-shokunin; do b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done; env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks {LANE} $W/fleet/tameshi-shokunin; R=$W/fleet/tameshi-shokunin; git -C $R checkout -q --detach {FROZEN}; cd $R && git apply {E}/witness/fix.diff`. '
    f'Run `timeout 2400 bash tools/mutate-and-run.sh --regression --workdir $W/rg` and paste the REGRESSION_* lines and exit. If not PASS (cases=9 passed=9), repeat at base {BASE} in a second mirror and report both.')
add('SelftestsNoHarm', 'executor', ['operability'],
    f'No-harm: in your clone with the frozen fix applied ({WITNESS}) and in a second clone at base {BASE}, run `timeout 600 bash tools/mutate-and-run.sh --selftest` and `timeout 600 python3 tools/<x>.py --selftest` for each tools/*.py that accepts --selftest. Table: tool, exit at base, exit with fix, summary line. Name every difference and its cause.')
add('RegistryNoHarm', 'executor', ['operability'],
    f'No-harm of the gate/probe registry with the frozen fix. In a fleet mirror built as in the lane SKILL.md recipe (sibling lanes symlinked, tameshi cloned; never in {LANE}), at {FROZEN} with `git apply {E}/witness/fix.diff`, run `timeout 1200 python3 tools/registry-check.py` (read --help for flags) and the same at base {BASE}. Compare row by row; name any row whose result differs and why.')
add('DepthNoHarm', 'executor', ['depth'],
    f'No-harm, depth: run command D from {LANE}/SCORECARD.md (the `# D:` line near line 73) at base {BASE} and on the runner with the frozen fix (in your clone: {WITNESS}; feed `cat tools/mutate-and-run.sh` instead of `git show`). Paste both outputs. Then check that the fix adds no `#   js-`/`#   bash-` ledger line and removes none.')
add('MutateTallyExtra', 'mutation-tester', ['operability'],
    f'Attack the frozen fix beyond every counter family. {WITNESS}. Make at least 8 hand-made mutants of the tally block and the new guard that no counter generator makes (for example: delete the guard; guard `!=` → `>`; `nlegs=9` → `nlegs=8` with a dropped operand; FAIL and SETUP checks swapped; `[[ $st -eq 1 ]] && st=0` inside the loop; a mutant that misbehaves only when two legs fail). '
    f'For each run `timeout 300 bash tools/mutate-and-run.sh --selftest` and record exit and the MUTATE_SELFTEST line; restore exact bytes after each (sha256 before/after). Table: mutant, killed or survived; for each survivor, equivalent or a real detector gap (two-leg vectors are outside the 19).')
add('MutateSelftestHarness', 'mutation-tester', ['operability'],
    f'Attack the fix\'s own selftest harness code (not the tally block). {WITNESS}. Mutate the harness: the awk start/end markers that extract the block, the `st_*=$?` name extraction, the `[[ ${{#tnames[@]}} -eq 9 ]]` check, tally_line\'s first-line comparison, the vector loop bounds. For each, run `timeout 300 bash tools/mutate-and-run.sh --selftest` and then re-run a drop mutant of the tally loop on top of it: '
    f'does the weakened harness still pass the pristine runner while letting the drop mutant through (a silent detector loss)? Table with exits. Restore exact bytes each time.')
add('ConnectorOverlap', 'connector', ['adjacency'],
    f'Sibling-overlap scan for the C1 surface: a PASS summary whose counts are not checked to add up to the case total, and selftests that run their own summary logic. Search sibling lanes under {FLEET}/*-shokunin (read-only; never tameshi) with path:line. Report overlaps and whether tameshi should report them to the owner (report-only; never absorb).')
add('ConnectorSandbox', 'connector', ['adjacency'],
    f'Cross-lane pattern scan: how do sibling lanes\' counters run the candidate program they judge (subprocess, sandbox, fixed directory names, job labels in paths or argv)? Leg lesson: label-keyed programs met kumitate r44. Search {FLEET}/*-shokunin/.ufo/evidence and scripts (read-only) for counters that run candidate code with the job name visible (paths, argv, env). Report path:line findings and whether v4\'s bwrap isolation ({E}/c1-measure-v4.py BWRAP) is a pattern worth reporting to them (report-only).')
add('CriticC1Axis', 'critic', ['operability'],
    f'Adversarial review of C1\'s naming and sizing against {FLEET}/AXES.md and the round prompt {FLEET}/.ufo/prompts/tameshi-round-30.md §9: read {E}/contract.json and amendments 1-3. (1) Is "operability" named by the surface the round changes (a runnable gate verdict) or is this quality work misnamed? (2) Can a do-nothing, junk, all-false, no-reader or label-keyed program meet the frozen predicate (cite receipts under {E}/ctl/ and {E}/v4/)? '
    f'(3) Is the target one value re-derivable by one command over committed bytes? (4) What would show the surface unmoved? Verdict first per question.')
add('CriticHoldRule', 'critic', ['discernment'],
    f'Adversarial review of attempt 2\'s process before data. Facts: attempt 1 (TameshiR30) died at 05:25Z; its seats SealHeldout and CriticC1v2Design died with empty reports (`ls -la ~/.omp/agent/sessions/-Projects-shokunin/2026-10-23T00-54-50-959Z_01a16640-e34f-76e4-8a3b-4d245a8bb241/TameshiR30/`); attempt 2 wrote the sealed set as L1 and re-scored attempt-1 controls itself ({E}/contract-amendment-3.json). '
    f'Rules: the contract hold_rule ({E}/contract.json), the round prompt §6 and §9. (1) Did attempt 2 resend a dead seat\'s task or hand it to a living seat? (2) Is every control receipt the claim depends on committed before data (`git -C {LANE} log --format="%h %cI %s" {BASE}..{FROZEN}`)? (3) Were any attempt-1 uncommitted files cited without re-derivation? Verdict first.')
add('ReviewAttempt1', 'reviewer', ['calibration'],
    f'Re-verify the attempt-1 landed commits the round builds on: dcdf2d08, e59728df, {A1}. In your clone ({CLONE}), check each counter file\'s sha256 equals its contract/amendment `counter_sha256`, then re-run `timeout 1500 python3 {E}/c1-measure-v3.py --repo $S/clone --rev {BASE} --jobs 4` and compare with {E}/c1v3-at-base.stdout line by line. '
    f'Check commit order (contract before amendment 1 before controls before amendment 2) with `git -C {LANE} log --format="%h %cI %s" {BASE}..{FROZEN}`. Report any receipt that does not reproduce.')
add('RerunV3Witness', 'executor', ['operability'],
    f'Independent re-measure of the public part of C1 on the frozen fix: {WITNESS}; commit it in your clone, then run `{V3}` and paste the full summary and exit. Compare with {E}/witness/c1v3-at-witness-1fed832d.stdout (attempt 1) and {E}/v4/witness.stdout (attempt 2, v4). Do the (a)-(i) counts agree? Name any row that differs.')
add('RevengerCounterDiff', 'revenger', ['operability'],
    f'Reverse-check the v3→v4 counter change: `diff {E}/c1-measure-v3.py {E}/c1-measure-v4.py` and `diff {E}/v4/c1-measure-v4-draft.py {E}/c1-measure-v4.py`. Is every change the one amendment 3 declares ({E}/contract-amendment-3.json), and does any change weaken conditions (a)-(i)? '
    f'Does sealed_items() refuse a sealed file whose hash differs, and does the block mismatch path give PASS=false? Does the bwrap selftest still run the pristine runner identically (compare pristine rows of {E}/v4/base.stdout with {E}/c1v3-at-base.stdout)? Verdict first.')
add('ScoutSkillSections', 'scout', ['calibration'],
    f'Recon for wave B (cold reads of drifted SKILL.md sections). In `git -C {LANE} show {FROZEN}:SKILL.md`, list every section (start line, heading) that cites tools/mutate-and-run.sh, corpus/SOURCES.md, corpus/QUALITY.md or corpus/README.md, and for each say whether a cold reader would need to RUN the runner (and which mode: --selftest, --regression, a sweep) and roughly how long that takes (time one `--selftest` in your clone). '
    f'Name sections that cannot be read in 45 minutes. Report a table only.')
spec = {'wave': 'round-30-wA', 'reportDir': W, 'context': CONTEXT, 'items': items}
out = Path(LANE + '/.ufo/waves/round-30/spec-wA.json')
out.write_text(json.dumps(spec, indent=1) + '\n')
print(len(items), 'items ->', out)
