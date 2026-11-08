#!/usr/bin/env python3
"""Build the round-93 v1 wave spec (w1-spec.json).

Round-92 M5 fix (R92-DEF-1): every constant is DERIVED from git objects at the
named revisions, never hand-copied. If a derived value disagrees with the value
the frozen plan states, this generator refuses with `SPEC_CONST_DRIFT` and
writes nothing. Usage: python3 make-spec.py
"""
import hashlib
import json
import re
import subprocess
import sys

L = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = L + "/.ufo/waves/round-93/w1"
E = L + "/.ufo/evidence/round-93"
SC = "/fast/scratch/hyaku/tameshi-r93"
PLAN = L + "/plans/round-93.plan.md"
BASE = "4a7e259b407d582d2010197f32d7524d6bed5370"
INSTR_REV = "855f0c1c59ee2af7f184d8de62d02cdd576eb94e"
DRIVER_REV = "69d377a03093792016a46868c38974d050261fc1"
PIN = "f47ad6ba8d306f8125597401cb2ce45c1297a593"
COUNTER = ".ufo/evidence/round-93/c1/measure-v93.py"
DRIVER = ".ufo/evidence/round-93/c1/controls-v93.py"
SPEC = ".ufo/evidence/round-93/c1/census-mutants.json"
LOCAL = "/home/vgpnk/Projects/shokunin/.ufo/waves/round-93"


def git(*a):
    p = subprocess.run(["git", "-C", L, *a], capture_output=True,
                       env={"PATH": "/usr/local/bin:/usr/bin:/bin", "LC_ALL": "C.UTF-8",
                            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
                            "GIT_CONFIG_GLOBAL": "/dev/null"})
    if p.returncode != 0:
        raise SystemExit("SPEC_CONST_DRIFT git-failed " + " ".join(a))
    return p.stdout


def derive(rev, path):
    return hashlib.sha256(git("cat-file", "blob", rev + ":" + path)).hexdigest()


plan = open(PLAN, encoding="utf-8").read()
derived = {"counter": derive(INSTR_REV, COUNTER), "driver": derive(DRIVER_REV, DRIVER),
           "spec": derive(INSTR_REV, SPEC)}
declared = {"counter": "18903602aa040b7e258fd6c81491cfee4ea7bb0575784fe27e351587fe094c2d",
            "driver": "400d8e0ffceadc3e9aa7d057ac16b5142f0f4b60626544133462b1067bc0da74",
            "spec": "ce8983d577b1fa71afd1760b80304cba87c56ca339384df06eb2705a5bfde290"}
drift = [k for k in derived if derived[k] != declared[k] or declared[k] not in plan]
print("SPEC_DERIVED " + " ".join("%s=%s" % (k, derived[k]) for k in sorted(derived)))
if drift:
    print("SPEC_CONST_DRIFT " + ",".join(drift)
          + " (derived value disagrees with the plan or the plan does not state it)")
    sys.exit(1)
print("SPEC_CONST_OK derived=3 plan-declared=3")
COUNTER_SHA = derived["counter"]
DRIVER_SHA = derived["driver"]

GOD = ("/skill:godspeed\nYou are a Godspeed-enabled subagent.\n\n1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n"
       "3. **Keep moves that improve any axis and harm none.**\n4. **Don't aim \u2014 let the frontier walk itself.**\n\n"
       "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. "
       "Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. "
       "Act directly via tool calls.\n\n")
C1 = (f"python3 -I {E}/c1/measure-v93.py --repo {L} --rev <REV> --work <empty dir under your scratch>")
CTL = (f"python3 -I {E}/c1/controls-v93.py --lane {L} --rev {INSTR_REV} --base {BASE} "
       f"--work <empty dir under your scratch> --outdir <your scratch>/receipts --jobs 4")
MAT = (f"materialize a pristine copy: D=<your scratch>/g; mkdir -p \"$D/scripts\"; "
       f"git -C {F} archive --format=tar {PIN} scripts/fixtures/sources-census | tar -x -C \"$D\"; "
       f"git -C {F} show {PIN}:scripts/sources-census.sh > \"$D/scripts/sources-census.sh\"; "
       f"chmod 755 \"$D/scripts/sources-census.sh\"; then `bash \"$D/scripts/sources-census.sh\" selftest` "
       f"(exit 0 and `selftest ok` when pristine)")

context = f"""# Goal and contract
Tameshi round 93 (lane tameshi, verification-fixture craft: honest verification instruments). L1 TameshiR93 is the sole planner and integration owner.
Lane repo (absolute): {L}. Fleet root: {F}.
Read the frozen plan first: {L}/plans/round-93.plan.md (instrument {INSTR_REV}; driver {DRIVER_REV}; base {BASE}). TWO frozen claims:
- R93-C1 (coverage, fourth attempt at certifying the round-90 fleet-gate mutation case): the case note corpus/knowledge/mutation-case-fleet-sources-census.md is certified by the verdict-content reader {E}/c1/measure-v93.py (sha256 {COUNTER_SHA}), which keys a table only when its HEADER ROW carries a `verdict` cell (QUALITY 154, grounded in S321 GFM tables), reads the `verdict` header only from the header row (QUALITY 155), skips fenced blocks (S322), grades the LAST corpus/README.md row naming the note for coverage and requires a located quote occurring in a committed snapshot for source (QUALITY 157). The case measures the fleet's own registry gate {F}/scripts/sources-census.sh pinned at fleet commit {PIN} under its own `selftest`; spec {E}/c1/census-mutants.json (12 single-edit mutants C01-C12, each with a witness registry); pins {E}/c1/pins.json (derived from git objects, never hand-copied - round-92 M5).
- R93-C2 (calibration): tools/conjunct-disposition.py + tools/conjunct-disposition.json prove every one of the counter's 19 conjuncts is falsifiable by a named committed battery receipt, or declared unfalsifiable with a reason naming the seal that forbids the falsifier (QUALITY 158).
Frozen counter: `{C1}` (~60 s; prints C1_ROW lines, C1_SUMMARY, C1_SOURCE, C1_CONJUNCTS, C1_R93_PASS=true|false). At the base the counter refuses at setup (`C1_SETUP spec-absent-at-rev`, exit 2): the do-nothing receipt.
Control battery: {E}/c1/controls-v93.py + receipts {E}/pre-freeze/controls/ (summary C1-summary.txt, derived from the receipts on disk; 35 pre-registered controls: 4 positive, 23 hostile, 3 setup, 5 removal mutants). `{CTL}` (~20-30 min at --jobs 4; prints per-control MATCH/MISMATCH/MISSING and `C1_CONTROLS states=.. matched=..`).
Disposition checker: `python3 -I {L}/tools/conjunct-disposition.py --lane {L} --rev {INSTR_REV}` -> `DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0`; `--selftest` -> `DISPOSITION_SELFTEST: 6/6 pass`.
Spec id set: C01-C12. The note's single verdict table has header `| id | arm targeted | edit | verdict | witness |`. Its §2b impact table and its survivor-lanes table key ids in their first cells and assert NO verdict: under QUALITY 154 they are not verdict tables and must not refuse the note.
Frozen artifacts (never edit, rename or replace): plans/round-93.plan.md, .ufo/waves/round-93/claims.json, and everything under .ufo/evidence/round-93/.

Your item is READ-ONLY on the lane except for your own deliverable(s): write them at the absolute paths your item names, inside {W}/. If you build a probe, fixture or script, COMMIT NOTHING but SAVE ITS SOURCE next to your deliverable ({W}/<your-seat-name>-<name>.<ext>) with its output, so the L1 can re-run it from committed bytes. Return a short final message naming your file and its VERDICT line.

# Hard rules for every seat
- Scratch: every clone, copy, fixture or work dir lives under {SC}/<your-seat-name>/ (mkdir -p). Pass it explicitly (TMPDIR, --work, --outdir). Never write under /tmp except files under 50 MB. Remove your scratch dir before you yield: trap 'rm -rf -- "$S"' EXIT in shell. Check `{F}/scripts/hyaku/disk-guard.sh status` before a heavy pass.
- Git fixtures: create any fixture repo or clone under your scratch dir (D=$(mktemp -d -p {SC}/<seat> fx.XXXXXX) && git -C "$D" init -q, or git clone --shared); never pass an empty or unchecked variable to git -C; verify git -C "$D" rev-parse --show-toplevel equals $D before the first commit. Commit only inside such a fixture, with identity ctl <ctl@fixture.invalid>.
- Never run git add, commit, stash, checkout, switch, reset, pull, push, or any mutating jj command in {L}, in {F}, or in any sibling lane repo. Read-only git (show, log, ls-tree, cat-file, rev-parse, diff, status, archive) is fine.
- Never modify any file under {L} except your own deliverable(s) under {W}/. Never edit {F}/scripts/ (the census gate is read-only: mutate only scratch copies), {F}/templates/, MANIFEST.json, tools/, corpus/, SCORECARD.md, LOG.md, or any sibling lane repo. Never write into /home/vgpnk/Projects/shokuknow.
- Never mutate host settings (sysctl, services, user namespaces, ptrace scope). Name a need in your deliverable instead.
- Every `Report:` trailer path is relative to {L} - write it at {L}/<that path>. Use absolute paths everywhere.
- Never message agent://all; the L1 is TameshiR93. Message the L1 with `write agent://TameshiR93` only if you must, once, with a short note.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool, version, channel and reason in your deliverable).
- pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide; install via uv tool, npx, or an official binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, never downgrade, never restart a host service.
- Never call the `ask` tool. The round is unattended.
- Your deliverable ends with a line `VERDICT: <one token>` and a line `TOOLS: none` or the installs with version, channel and reason.
- Run only what your item names; do not run unrelated repo sweeps.
"""

items = [
    ("R93E1", "executor",
     f"TARGET (independent reproduction OUTSIDE the counter): for each of the 12 mutants in {E}/c1/census-mutants.json, {MAT}; apply the mutant's exact `old`->`new` edit to the copy with your own code (not measure-v93.py; assert the old string occurs exactly once), run the selftest in your ordinary shell environment (do NOT use env -i), twice, and record rc and the SURVIVED/killed arm lines. Compare each verdict (rc 0 = SURVIVED, else KILLED) with the C1_ROW lines in {E}/pre-freeze/controls/pos-real.out. Then run the frozen counter once at {INSTR_REV}: `{C1.replace('<REV>', INSTR_REV)}` and paste its stdout. Save your driver as {W}/R93E1-repro.sh (or .py). Deliverable: {W}/R93E1.md - a 12-row table (id, rc run1/run2, which selftest arm differs, derived verdict, note verdict, agree), the counter's C1_SUMMARY and C1_R93_PASS lines, and your VERDICT (`reproduced-12/12` or the count)."),
    ("R93E2", "executor",
     f"TARGET (no-harm baseline and landing): at the base {BASE} AND at the instrument revision {INSTR_REV}, each in its own `git clone --shared` under your scratch, run the lane's standing sweeps from the clone root and paste their summary lines and exit codes: `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json`, `python3 -I -X utf8 tools/receipt-bytes-bind.py --repo . --root .ufo/evidence/round-78` (read its docstring for flags), `python3 -I -X utf8 tools/pointer-recheck.py --repo . --manifest tools/pointer-recheck.json`, `python3 -I -X utf8 tools/wave-reconcile.py --repo . --extra-root fleet={F} --manifest tools/wave-reconcile.json`, and `python3 -I tools/registry-check.py --root .` (if a tool's flags differ, read its docstring and say what you ran). Also `python3 -I tools/hardening-lint.py --selftest` and `python3 -I tools/hardening-lint.py --counter {E}/c1/measure-v93.py` (record the defences=N/8 line; the new counter must not regress the lint). Deliverable: {W}/R93E2.md - one row per sweep (command, base exit+summary, landing exit+summary, verdict same/drift), plus an explicit statement of any drift and your `VERDICT: no-regression` or the drift named."),
    ("R93E3", "executor",
     f"TARGET (replay the battery from committed bytes, twice, into ONE outdir): run `{CTL}` exactly (jobs 4, receipts under your scratch), then (a) paste the driver's `CONTROL_INSTRUMENT sha256=` line and its final `C1_CONTROLS states=.. matched=..` line with the exit code; (b) for each receipt you produced, compare against the committed receipt of the same name in {E}/pre-freeze/controls/ on the STABLE lines only - every `C1_ROW`, `C1_CONJUNCTS`, `C1_SUMMARY`, `C1_SOURCE`, `C1_R93_PASS` and `C1_SETUP` line - ignoring the driver header (`control=`, `clone_rev=`, `parent=`, `mutant=`, `counter_sha=`) and `exit=`; list every receipt whose stable lines differ; (c) run the battery a SECOND time into the SAME outdir and prove the M4 guard: the second run must create `<name>.rerun-1.out` files and must not modify any existing `<name>.out` (compare sha256 before and after) - paste the file list and the two C1_CONTROLS lines; (d) verify your instrument sha line equals {COUNTER_SHA}. Deliverable: {W}/R93E3.md - the two summaries, the differing-receipt list (or `none`), the receipt-guard evidence, and `VERDICT: reproduced` or the drift named."),
    ("R93SC1", "scribe",
     f"TARGET (records draft): draft three append blocks at {W}/R93SC1-*.md for the L1 to integrate (do NOT write into corpus/): (1) the case note's round-93 status block for {L}/corpus/knowledge/mutation-case-fleet-sources-census.md - it must state what the verdict-content reader certifies (the twelve cells), what it does NOT (how they were obtained; fenced presentations; a table with no `verdict` header), cite S320, S321 and S322 with their located quotes, and end without an admission claim (admission is the non-author closure's); (2) a QUALITY.md criterion draft for QUALITY 158's operational half - a conjunct-disposition manifest is a claim about the instrument and must be audited by a checker that can fail, citing `.ufo/evidence/round-93/c1/controls-v93.py` and `tools/conjunct-disposition.py`; (3) a `## Mistakes` row draft for the round-93 lesson whose class is `a duplicated rule hides which removal is load-bearing` (the first controls-v93 D01 removed one of two copies of the stray-verdict rule and the mutant still scored MATCH=false; the counter now has one rule in one place), with the evidence pointer `.ufo/evidence/round-93/c1/measure-v93.py` rev `855f0c1c` vs the D01 run. Read the note, the plan and QUALITY 150-158 first. Deliverable: the three blocks plus `VERDICT: drafted`."),
    ("R93S1", "scout",
     f"TARGET (independent source verification, S321 and S322): re-fetch https://github.github.com/gfm/ and https://spec.commonmark.org/0.31.2/ yourself into your scratch with `curl -sS -L -D headers -o body`, record the HTTP date header, byte size and sha256, and compare with the committed snapshots {E}/sources/s321.html (sha256 b153d814fdfc8624bb6da7449162c1cd707a637f7d1c1b636eb44b9cf63fa220, 508310 B) and {E}/sources/s322.html (sha256 c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d, 514698 B). Tag-strip both bodies and verify the quotes the lesson Gate records - GFM: \"The table is broken at the first empty line, or beginning of another block-level structure\" (15 words) and \"a single header row, a delimiter row separating the header from the data\" (13 words); CommonMark: \"A fenced code block begins with a code fence, preceded by up to three spaces of indentation.\" (17 words) - give their line numbers in your stripped text, and verify the registry rows S321/S322 in {L}/corpus/SOURCES.md parse as 11 columns with status mined and used-by naming corpus/lessons/round-93.md. Also verify the GFM spec's own statement that the header row must match the delimiter row in cell count (the reader's width rule). Deliverable: {W}/R93S1.md - snapshot hashes, the quote table with line numbers and word counts, the registry-row parse, and `VERDICT: agree` or `disagree: <what>`."),
    ("R93S2", "scout",
     f"TARGET (audit the reader's premise on the real note): write a read-only probe that (a) enumerates EVERY GFM table in {L}/corpus/knowledge/mutation-case-fleet-sources-census.md and {L}/corpus/README.md using the same definition the reader uses (a header row followed by a delimiter row, broken at the first blank or non-pipe line; 0-3 leading spaces) and prints for each: start line, header cells, data-row count, and whether the header carries a `verdict` cell; (b) prints every block line outside the single verdict table that carries a KILLED/SURVIVED token and at least two pipes (must be empty on the honest note); (c) names every presentation form in either file that the reader does NOT key and says why that is the declared limit (fenced block, table with no verdict header, prose token, escaped pipe); (d) proves the reader's classification on six hand-built variants you construct in your scratch (second verdict table, renamed header with tokens, bare pipe line with a token, id-keyed non-verdict table, `verdict` data cell, fenced inverted table) and reports the counter's `verdict_tables` and `badrows` for each. Use the counter's own functions by importing {E}/c1/measure-v93.py (importlib) - do not reimplement the parser. Deliverable: {W}/R93S2.md + your probe source, with `VERDICT: premise-holds` or the disagreement named."),
    ("R93R1", "reviewer",
     f"TARGET (code review of the reader for false-green and false-red paths): review {E}/c1/measure-v93.py at {INSTR_REV} line by line. Find any way a committed lane state could print C1_R93_PASS=true while the note's twelve verdict cells are not the true selftest verdicts of their mutants, and any way an honest note would be refused. Cover at least: the self-pin normalisation (can an edited file keep the same normalised digest? duplicated or moved SELF_SHA256 line?), `block_lines` fence tracking (tilde fences, indented fences, an unclosed fence swallowing the verdict table), `tables()` (delimiter detection, blank-line break, pipe-in-prose), `split_cells` (escaped pipes, leading/trailing pipes, an escaped backslash), the header/verdict-column rule, the width rule, the stray-verdict scan and its `consumed` set, the idset equality, the `measured:` regex and the declared fenced limit, the `source` conjunct's quote matching (could an unrelated quote satisfy it?), the `coverage` last-row rule (could a row be appended that does not name the path but still counts? could the census's own appended rows break it?), and the seal. Cite file:line for every finding. Save any probe you write next to the deliverable. Deliverable: {W}/R93R1.md - numbered findings with severity and a `VERDICT: findings:N` line (0 is a valid, earned answer only if you state what you tried)."),
    ("R93R2", "reviewer",
     f"TARGET (freeze conformance + the C2 manifest audited row by row): with read-only git, check (1) the counter blob at {INSTR_REV} has sha256 {COUNTER_SHA} and the driver blob at {DRIVER_REV} has sha256 {DRIVER_SHA}; (2) every receipt under {E}/pre-freeze/controls/ was produced by those bytes (the `CONTROL_INSTRUMENT sha256=` line) and its `clone_rev` is a child of the instrument revision; (3) `.ufo/waves/round-93/claims.json` names the same instrument revision the plan does; (4) the plan's predicate is the same condition as the counter's `ok = all(conj.values())` and its `C1_R93_PASS` label - check the conjunct list in the code against the list in the plan, name by name; (5) EVERY row of {L}/tools/conjunct-disposition.json: open the named receipt in {E}/pre-freeze/controls/, confirm the `C1_CONJUNCTS` line shows that conjunct FALSE (or the named `C1_SETUP` token for the two setup rows), and for each `unfalsifiable` row judge whether the stated mechanism really forbids a committed falsifier. Report any row whose receipt does not move it, any conjunct the manifest omits, and any manifest key the counter does not print. Deliverable: {W}/R93R2.md - a row-by-row table (conjunct, manifest row, receipt, moves y/n, judgement) plus `VERDICT: conforms` or the defects numbered."),
    ("R93C1", "critic",
     f"TARGET (attack C1 as framed): read the plan's claim, predicate, kill rule and declared limits, then try to KILL the claim. Two lines of attack, both required: (A) honest-note refusal (rule a) - build, in a `git clone --shared` of {L} checked out at {INSTR_REV}, the cheapest committed state that a reader of the plan would call an HONEST note and that the counter refuses: at minimum an id-keyed table appended with no verdict token, a `verdict`-word data cell in a non-verdict table, a bolded id in a non-verdict table, an escaped pipe inside a cell, a table whose header has `verdict` plus one extra column, a note whose §2b-style table has an empty first cell, and a table indented three spaces. (B) false green (rule b) - build a state that presents verdicts the reader does not key and that a reader of the claim would still count: a table with a `verdict` cell spelled with different case, `verdict ` with a trailing space, `**verdict**`, a fenced `measured:` line, an HTML table with verdict tokens, a second table whose header says `verdicts`. For each attempt record the counter's exit, C1_SUMMARY, C1_CONJUNCTS and whether it is a kill under the plan's own wording (rule a, rule b, or a declared limit). Save every attempt as {W}/R93C1-<name>.{{md,out}} with the command. Deliverable: {W}/R93C1.md - the attempt table and `VERDICT: killed:<rule>` or `survives`."),
    ("R93M1", "mutation-tester",
     f"TARGET (mutation-test the reader against its own battery): copy {E}/c1/measure-v93.py to your scratch. Write a spec of at least 16 single-edit defects, each weakening ONE rule of the reader (self-pin assert, pins equality, spec shape, pin, green, canary, valid0, trivial0, inconclusive0, unstable0/run count, note presence, table-count rule, stray-verdict scan, out-of-set rule, duplicate rule, position rule, width rule, idset equality, figure regex, witness rule, source quote, coverage last-row, n_min). Save the spec as {W}/R93M1-defects.txt BEFORE running anything. For each defect, recompute the SELF_SHA256 line for the mutated bytes (the pin is a seal, not a defence against a deliberate mutation study - say so), then run the mutated counter against the battery state that must expose it (clone the lane at {INSTR_REV}, apply the state's edit the way {E}/c1/controls-v93.py does, or use that driver's `--only <state>` with a scratch copy whose counter path points at your mutant - read its code). Report KILLED / SURVIVED / INCONCLUSIVE per defect, then answer: are D01-D05 (the plan's removal mutants) the load-bearing rules for their states, and is any rule of the reader survivable and unstated (a QUALITY 158 violation C2 would miss)? Deliverable: {W}/R93M1.md - the defect table, the `SURVIVORS:` line, and `VERDICT: killed:<n>/<m>`."),
    ("R93SN1", "sentinel",
     f"TARGET (safety audit of the round's committed drivers): read {E}/c1/controls-v93.py, {E}/c1/measure-v93.py, {L}/tools/conjunct-disposition.py and {E}/c1/make-pins.py. Check: every mutating git call targets a directory asserted to be its own toplevel and never an empty or unchecked variable (fleet incident 2026-11-06: `git -C \"\"` fell back to the fleet root and committed there); no write can land outside the scratch dir, the lane's .ufo/evidence/round-93/ or the wave dir; scratch is removed on exit; no hardcoded /tmp; `--work`/`--outdir`/`--rev` are validated; `git replace` creation cannot touch the lane or the fleet repo; `make-pins.py` writes only under the lane; the disposition checker's `--selftest` uses a TemporaryDirectory and deletes it; nothing reads credentials, host settings or sibling lane bytes for writing. Also verify the M4 receipt guard cannot be defeated by a pre-existing symlink or an unwritable outdir. Run nothing that writes outside your scratch. Deliverable: {W}/R93SN1.md - findings with severity and `VERDICT: findings:N`."),
    ("R93CN1", "connector",
     f"TARGET (sibling-overlap scan, report-only): does any other lane in the fleet already implement (a) a Markdown-table reader keyed on a verdict header, (b) a conjunct-falsifiability disposition checker, or (c) a battery-summary-derived-from-receipts helper? Search read-only over {F} for evidence: `grep`/`rg` for `verdict`, `delimiter row`, `header row`, `CONJUNCT`, `unfalsifiable`, `receipt` in the sibling lane repos' `tools/`, `.ufo/evidence/` and `corpus/knowledge/`, plus {F}/scripts/. Record for each hit: lane, path, what it does, and whether tameshi's reader duplicates it, could reuse it, or covers a surface it does not. Judge against PROVINCE.md: tameshi owns the reusable craft, so a sibling's *product* use of the same pattern is adjacency, not overlap, and must be reported, not absorbed. Also check whether the fleet's own `scripts/sources-census.sh` has a table parser whose verdict semantics differ from the reader's (read-only; mutate nothing). Deliverable: {W}/R93CN1.md - a hit table with the overlap verdict per hit and `VERDICT: no-overlap` or `overlap:N`."),
]

spec = {
    "wave": "r93-w1",
    "maxLanes": 16,
    "reportDir": ".ufo/waves/round-93/w1",
    "hoist": False,
    "context": context,
    "items": [
        {"name": n, "role": r, "axes": ["verification-fixture-craft"], "item": GOD + t}
        for n, r, t in items
    ],
}
roles = {}
for _, r, _ in items:
    roles[r] = roles.get(r, 0) + 1
attack = sum(roles.get(r, 0) for r in ("reviewer", "critic", "mutation-tester", "labrat"))
print("SPEC_ITEMS items=%d roles=%s attack=%d/%d" % (
    len(items), ",".join("%s:%d" % (k, roles[k]) for k in sorted(roles)), attack, len(items)))
json.dump(spec, open(W + "-spec.json", "w"), indent=1)
print("SPEC_WRITTEN " + W + "-spec.json")
