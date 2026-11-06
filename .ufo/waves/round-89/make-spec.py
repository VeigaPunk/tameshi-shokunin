#!/usr/bin/env python3
"""Build the round-89 v1 wave spec (w1-spec.json). usage: make-spec.py <freeze-rev>"""
import json
import sys

FREEZE = sys.argv[1]
BASE = "61990f3d8cd99932bfb0575e1c292e03d310b436"
PRE = "a65e11c01a469336b74662d2e3c51ba6f174ac6f"
L = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = L + "/.ufo/waves/round-89/w1"
SC = "/fast/scratch/hyaku/tameshi-r89"
GOD = ("/skill:godspeed\nYou are a Godspeed-enabled subagent.\n\n1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n"
       "3. **Keep moves that improve any axis and harm none.**\n4. **Don't aim \u2014 let the frontier walk itself.**\n\n"
       "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. "
       "Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. "
       "Act directly via tool calls.\n\n")
WIT = "python3 -I %s/tools/ledger-witness.py" % L
RUN = ("%s --run --runner <runner file> --fleet %s --scratch <empty dir under your scratch>" % (WIT, F))

context = f"""# Goal and contract
Tameshi round 89 (lane tameshi, verification-fixture craft: mutation testing of fleet gates). L1 TameshiR89 is the sole planner and integration owner.
Lane repo (absolute): {L}. Fleet root: {F}.
ONE frozen claim, R89-C1 (operability, capability acquisition): a new tool {L}/tools/ledger-witness.py runs the mutation ledger {L}/tools/mutate-and-run.sh --regression under strace(1) and binds the declared ledger (parsed from the runner bytes) to what the KERNEL observed, not to what the runner prints. Its 15 checks W_PARSE..W_ENV are documented in its docstring (read it first: `sed -n 1,63p {L}/tools/ledger-witness.py`).
Read the frozen plan first: {L}/plans/round-89.plan.md (freeze commit {FREEZE}; pre-freeze instrument commit {PRE}; base {BASE}). It holds the predicate, the kill rule and the DECLARED LIMITS L1-L4 (out of model).
Frozen counter: {L}/.ufo/evidence/round-89/measure.sh — `bash {L}/.ufo/evidence/round-89/measure.sh {L} <REV> {F} <empty work dir>`; it takes ~15-25 minutes (13 traced regression runs, 7 in parallel; ~1.6 GB scratch per run). Prints `C1_R89 ... C1_R89_PASS=true|false`.
One witness run on one runner: `{RUN}` (~10-12 min for a runner that does the real work; seconds for a stub). It prints `WITNESS_FINDING <check> leg=<leg> <detail>` lines and ends with `LEDGER_WITNESS: legs=.. witnessed=.. findings=.. checks=.. PASS|FAIL`, exit 0 PASS / 1 FAIL / 2 setup. Offline re-audit of a kept run: `{WIT} --audit --runner R --fleet <scratch>/fleet --trace <scratch>/trace.txt --workdir <scratch>/wd --stdout <scratch>/runner.out --rc N`.
Existing forgery battery (12 runners, all refused pre-freeze): generator {L}/.ufo/evidence/round-89/controls/make-forgeries.py (`python3 -I ... <outdir> [<nonce>]`; also emits the two honest variants) plus {L}/.ufo/waves/round-88/w1/T88E2-make-variants.py (parked, stub, dupbase). Expectations: {L}/.ufo/evidence/round-89/controls/expected.tsv. Pre-freeze receipts: {L}/.ufo/evidence/round-89/pre-freeze/.
Frozen artifacts (never edit, rename or replace): plans/round-89.plan.md, tools/ledger-witness.py, .ufo/evidence/round-89/ (all of it).

Your item is READ-ONLY on the lane except for your own deliverable(s): write them at the absolute paths your item names, inside {W}/. If you build a runner variant, probe or script, COMMIT NOTHING but SAVE ITS SOURCE (or a generator that rebuilds it byte-exactly from `git -C {L} show {BASE}:tools/mutate-and-run.sh`) as a file next to your deliverable ({W}/<your-seat-name>-<name>.<ext>) together with the witness output, so the L1 can re-run it from committed bytes. Do not copy traces or 1 GB scratch trees into {W}; cite the command and paste the LEDGER_WITNESS line and the finding counts instead. Return a short final message naming your file and its VERDICT line.

# Hard rules for every seat
- Scratch: every clone, fixture, copy or work dir lives under {SC}/<your-seat-name>/ (mkdir -p). Pass it explicitly (--scratch, TMPDIR). Never write under /tmp except files under 50 MB. Remove your scratch dir before you yield: trap 'rm -rf -- "$S"' EXIT in shell. Check `{F}/scripts/hyaku/disk-guard.sh status` before a heavy pass.
- Git fixtures: create any fixture repo or clone under your scratch dir (D=$(mktemp -d -p {SC}/<seat> fx.XXXXXX) && git -C "$D" init -q); never pass an empty or unchecked variable to git -C; verify git -C "$D" rev-parse --show-toplevel equals $D before the first commit. Commit only inside such a fixture, with identity ctl <ctl@fixture.invalid>.
- Never run git add, commit, stash, checkout, switch, reset, pull, push, or any mutating jj command in {L}, in {F}, or in any sibling lane repo. Read-only git (show, log, ls-tree, cat-file, rev-parse, diff, status) is fine.
- Never modify any file under {L} except your own deliverable(s) under {W}/. Never edit frozen artifacts, tools/, corpus/, SCORECARD.md, LOG.md, MANIFEST.json, {F}/templates/, {F}/scripts/, or any sibling lane repo (sibling lanes are read-only). Never write into /home/vgpnk/Projects/shokuknow.
- Never mutate host settings (sysctl, services, user namespaces, ptrace scope). Name a need in your deliverable instead.
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. Use absolute paths everywhere.
- Never message agent://all; the L1 is TameshiR89.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool, version, channel and reason in your deliverable).
- pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide; install via uv tool, npx, or an official binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, never downgrade, never restart a host service.
- Never call the `ask` tool. The round is unattended.
- Your deliverable ends with a line `VERDICT: <one token>` and a line `TOOLS: none` or the installs with version, channel and reason.
- Run only what your item names; do not run unrelated repo sweeps.
"""

items = [
    ("T89E1", "executor",
     f"TARGET (independent re-measurement of R89-C1): in fresh empty work dirs under {SC}/T89E1/, run the frozen counter at the freeze revision {FREEZE} and at the base {BASE}. Paste both complete stdouts and exit statuses. At the freeze the only conjunct expected false is capability_row=0 (the SCORECARD row lands after the freeze); name every other conjunct's value and whether it matches the plan's target. Then run `{WIT} --selftest` from `git -C {L} show {FREEZE}:tools/ledger-witness.py` extracted to your scratch and paste the summary. Deliverable: {W}/T89E1.md with the outputs verbatim, exit codes and wall times, and `VERDICT: conjuncts-met` (all but capability_row) or `VERDICT: conjunct-missed:<name>`."),
    ("T89E2", "executor",
     f"TARGET (attack: in-model counterfeits): build at least three NEW counterfeit runners, each NOT in the existing battery, each printing the runner's own success figure (per-leg `REGRESSION_CASE <leg>: PASS` and `REGRESSION: PASS (cases=11 passed=11 ...)`, exit 0) while skipping or faking real work in a way the plan's declared limits L1-L4 do NOT cover. Ideas to try (pick the cheapest that might pass): exec the interpreter on the spec-exact mutant but with stdin/argv/env identical and kill it with a signal you then mask; run each mutant's suite once and reuse that exit for another defect; exec a different same-named interpreter binary via an absolute path; write the mutant through a hard link or rename created before the exec; exec via execveat or a `/proc/self/fd` path; fork-bomb timing so strace reorders events. Run `{RUN}` on each (the runner file is your generated variant). Deliverable: {W}/T89E2.md with one row per counterfeit (name, generator file, what it skips, LEDGER_WITNESS line, exit, which checks fired, whether it falls under a declared limit) and `VERDICT: refused-all` or `VERDICT: accepted:<names>`."),
    ("T89E3", "executor",
     f"TARGET (attack: honest variants — kill rule (c)): build at least two NEW honest runner variants that do ALL the real ledger work and keep the `regression_case_git` call shape, but differ from the base runner in ways the witness must tolerate (examples: a different --timeout default, an extra log line, variables renamed, the order of two non-adjacent legs swapped, specs written to another directory name, an added comment block, a different TMPDIR handling). Run `{RUN}` on each. A refusal of an honest variant for a reason other than a declared limit kills the claim: report the exact finding lines. Deliverable: {W}/T89E3.md (one row per variant: generator file, change, LEDGER_WITNESS line, exit) and `VERDICT: accepted-all` or `VERDICT: refused:<names>`."),
    ("T89E4", "executor",
     f"TARGET (bounded probe on the declared boundary, the labrat seat): hypothesis H1 — 'the witness accepts a runner that runs survivors honestly but sabotages recorded-KILLED defects through process state the trace does not carry (L3), e.g. closing stdout or changing the working directory only for those defects'. Build the cheapest such runner (generator from the base runner bytes), run `{RUN}`, and report whether it is accepted and through which mechanism. Hypothesis H2 — 'the W_ENV environment comparison can be evaded by a per-defect variable whose value differs only by the defect id as a path token'. Construct one concrete case and say whether it is L3 or a hole. Deliverable: {W}/T89E4.md with both hypotheses, the generator files, witness outputs, and `VERDICT: H1=<accepted|refused> H2=<hole|L3|refused>`."),
    ("T89M1", "mutation-tester",
     f"TARGET (mutation-test the witness itself with the lane's own runner): copy `git -C {L} show {FREEZE}:tools/ledger-witness.py` to your scratch. Write a spec (format: see `sed -n 330,425p {L}/tools/mutate-and-run.sh`) with at least 15 single-edit defects, one per check W_PARSE..W_ENV (weaken or invert each check's condition, plus a few in the trace parser: exec tokenizer, exit parsing, write-event anchoring). Save the spec as {W}/T89M1-witness.defects.spec BEFORE you run anything. Then run `bash {L}/tools/mutate-and-run.sh --target <your copy> --defects <spec> --suite 'python3 -I \"$MUTANT\" --selftest' --workdir {SC}/T89M1/sweep` and paste the full DEFECT table. For each survivor say whether a control in the committed battery would kill it (reason from the dev receipts in {L}/.ufo/evidence/round-89/controls/dev-receipts/) or whether it is a real test gap. Deliverable: {W}/T89M1.md with the table, kill rate, survivor analysis, `VERDICT: <killed>/<total>-killed`."),
    ("T89R1", "reviewer",
     f"TARGET (code review for false-accept paths): review {L}/tools/ledger-witness.py at {FREEZE} line by line for any path by which a runner that skips or fakes ledger work could still get `LEDGER_WITNESS ... PASS` (outside the plan's declared limits), and any path by which an honest runner would be refused. Cover: parse_trace (unfinished/resumed joining, the ` = ` result split, failed execs, signal lines), exec_strings/_str_array tokenizing, interp_match (shutil.which in the witness's PATH vs the runner's), first_exec selection, exit_after (pid reuse), W_ORDER anchoring (REL: fallback, normpath, -y annotations), norm_env, the rlimit rule, W_EXTRA, the witnessed counter. Cite file:line for every finding with severity (kill / defect / note). Deliverable: {W}/T89R1.md, `VERDICT: <n>-kill <m>-defect`."),
    ("T89R2", "reviewer",
     f"TARGET (conformance of the freeze): check with read-only git that (1) every pre-freeze control receipt in {L}/.ufo/evidence/round-89/pre-freeze/ and controls/ was committed in a strict ancestor of the freeze commit {FREEZE} and that the plan was not changed after it; (2) the predicate is the same sentence in plans/round-89.plan.md, the header and the code of .ufo/evidence/round-89/measure.sh, and the receipt label; (3) the do-nothing control fails and the positive controls are real; (4) the round-88 closure's routed items 1-6 (see {L}/corpus/lessons/round-88-verifier-spotcheck.md §6) are each either addressed by named bytes or stated as carried; (5) QUALITY criteria 134 and 135 ({L}/corpus/QUALITY.md, search '^134.' and '^135.') are met or not applicable, with reasons. Deliverable: {W}/T89R2.md, `VERDICT: conformant` or `VERDICT: nonconformant:<items>`."),
    ("T89C1", "critic",
     f"TARGET (attack the claim as framed): argue against admitting R89-C1 using the fleet's claim-sizing rules (prompt §9: do-nothing control, no universal clauses unless enumerated, axis named by surface, no narrowing after data, frozen predicate identity) and the last three closures' rejection reasons ({L}/corpus/lessons/round-86-verifier-spotcheck.md, round-87-..., round-88-...). In particular: is a capability-acquisition claim whose before-state is 'tool absent' a do-nothing-control pass? Are the declared limits L1-L4 so broad that the claim is vacuous? Could a counterfeit WITNESS (a different tool) pass the frozen counter, e.g. by recognizing variants rather than auditing traces, given the nonce and the honest variants? Deliverable: {W}/T89C1.md with numbered objections, each graded fatal / serious / minor with evidence, and `VERDICT: admit|reject|admit-with-notes`."),
    ("T89C2", "critic",
     f"TARGET (attack the trace parser with crafted inputs): using the public `--audit` CLI only, craft small fixture traces (copy the fixture shape from the witness's build_fixture in {L}/tools/ledger-witness.py) that exercise parser edge cases: an execve split across `<unfinished ...>`/`resumed>`, argv strings containing `]`, `, ` or `\\\"`, -s truncation (`\"...\"...`), a path containing `>` inside a -y annotation, execveat, a pid reused after exit, an exit line before the exec line of another pid. For each, state the expected verdict, the observed verdict, and whether a misparse could turn a forgery into PASS or an honest run into FAIL. Save fixtures and a driver script under {W}/T89C2-*. Deliverable: {W}/T89C2.md and `VERDICT: <n>-misparse` (0 if none)."),
    ("T89S1", "scout",
     f"TARGET (source reconnaissance): (a) re-open https://man7.org/linux/man-pages/man2/execve.2.html and https://man7.org/linux/man-pages/man1/strace.1.html, locate these quotes, give their line in a tag-stripped text, and count their words: 'many attributes of the calling process remain unchanged (in particular, its PID)'; 'By default, file descriptors remain open across an execve().'; 'Prints paths associated with file descriptor arguments and with the AT_FDCWD constant.'; 'Prints unabbreviated versions of environment, stat, termios, etc. calls.' Compare the live sha256 to {L}/.ufo/evidence/round-89/sources/*.html. (b) Search for ONE primary source on syscall-trace-based verification of what a build or test actually executed (e.g. a build system's strace/ptrace dependency tracer, or a paper on test-execution provenance) that could ground a successor to this tool; open it, give URL, access date, a <=25-word located quote, and recommend admit or reject with reason. Deliverable: {W}/T89S1.md, `VERDICT: quotes-located=<n>/4 candidate=<admit|reject>`."),
    ("T89SC1", "scribe",
     f"TARGET (knowledge-entry draft): draft a corpus knowledge entry 'kernel-witnessed ledger audit' for the lane at {W}/T89SC1-kernel-witnessed-ledger.md (the L1 integrates it; do not write into corpus/). Match the shape of an existing entry ({L}/corpus/knowledge/mutation-case-kake-ledger-guard.md). Content: the problem (print-reading counters passed by counterfeits, rounds 85-88), the witness design (15 checks, what each binds, why strace -f -y -v), the evidence (dev receipts and pre-freeze receipts in {L}/.ufo/evidence/round-89/), the declared limits L1-L4 from the plan, and a `source:` line citing S313 (execve(2), man7) and S314 (strace(1) -y/-v, man7) with the quotes from {L}/.ufo/evidence/round-89/sources/. Every number you write must be copied from a committed receipt you name. Deliverable: the draft plus {W}/T89SC1.md listing each figure and its receipt, `VERDICT: drafted`."),
    ("T89CN1", "connector",
     f"TARGET (sibling-overlap and adjacency scan, read-only): in the fleet root {F}, find (a) other lanes' counters or gates whose predicate reads a figure printed by the subject they certify (the class this round closes for tameshi's ledger), and (b) any other lane tool that already uses strace/ptrace or kernel observation. Use grep over the lane repos' tools/ and scripts/ dirs (e.g. `strace`, `ptrace`, `PASS (cases=`, `passed=`), read-only. For each hit give path:line and whether the witness pattern would apply. Deliverable: {W}/T89CN1.md (a table) and `VERDICT: <n>-adjacent`."),
]

spec = {
    "wave": "r89-w1",
    "maxLanes": 16,
    "reportDir": ".ufo/waves/round-89/w1",
    "hoist": False,
    "context": context,
    "items": [
        {"name": n, "role": r, "axes": ["verification-fixture-craft"], "item": GOD + t}
        for n, r, t in items
    ],
}
json.dump(spec, open(L + "/.ufo/waves/round-89/w1-spec.json", "w"), indent=1)
print("items=%d" % len(items))
