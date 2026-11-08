#!/usr/bin/env python3
"""Build the round-92 v1 wave spec (w1-spec.json). usage: make-spec.py"""
import json

L = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = L + "/.ufo/waves/round-92/w1"
E = L + "/.ufo/evidence/round-92"
SC = "/fast/scratch/hyaku/tameshi-r92"
BASE = "63172b9889475103aeca976d37389d204010dd11"
INSTR_REV = "884a4dc11a61434f8733683fdc691d997d5625ac"   # A: counter + battery + S320 + lesson gate
DRIVER_REV = "3119c0ea42062538fa13bc5637132c1f6d7fd831"   # A2: control driver syntax repair
FREEZE = "25f976625501663f2ea3336cc3e40499580ea59c"                             # B: plan + claims.json + control receipts
COUNTER_SHA = "a6adf4a6c89feb35f8633a2942c0bfcd729aa3ccbdc57e10fef98ce9b8cc2fe3"
PIN = "f47ad6ba8d306f8125597401cb2ce45c1297a593"
GOD = ("/skill:godspeed\nYou are a Godspeed-enabled subagent.\n\n1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n"
       "3. **Keep moves that improve any axis and harm none.**\n4. **Don't aim \u2014 let the frontier walk itself.**\n\n"
       "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. "
       "Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. "
       "Act directly via tool calls.\n\n")
C1 = f"python3 -I {E}/c1/measure-v92.py --repo {L} --rev <REV> --work <empty dir under your scratch>"
CTL = (f"python3 -I {E}/c1/controls-v92.py --lane {L} --rev {INSTR_REV} --base {BASE} "
       f"--work <empty dir under your scratch> --outdir <your scratch>/receipts --jobs 3")
MAT = (f"materialize a pristine copy: D=<your scratch>/g; mkdir -p \"$D/scripts\"; "
       f"git -C {F} archive --format=tar {PIN} scripts/fixtures/sources-census | tar -x -C \"$D\"; "
       f"git -C {F} show {PIN}:scripts/sources-census.sh > \"$D/scripts/sources-census.sh\"; chmod 755 \"$D/scripts/sources-census.sh\"; "
       f"then `bash \"$D/scripts/sources-census.sh\" selftest` (exit 0 and `selftest ok` when pristine)")

context = f"""# Goal and contract
Tameshi round 92 (lane tameshi, verification-fixture craft: mutation testing of gates). L1 TameshiR92 is the sole planner and integration owner.
Lane repo (absolute): {L}. Fleet root: {F}.
Read the frozen plan first: {L}/plans/round-92.plan.md (freeze {FREEZE}; base {BASE}; instrument commit {INSTR_REV}; control-driver repair {DRIVER_REV}). ONE frozen claim:
- R92-C1 (coverage, third attempt at certifying the round-90 fleet-gate mutation case): the case note corpus/knowledge/mutation-case-fleet-sources-census.md is certified by the sealed successor counter {E}/c1/measure-v92.py, whose own sha256 is pinned in the plan and asserted at run time (QUALITY 144), and which refuses (`ids=false`) any note table row that carries a verdict token or an id outside the spec's twelve ids C01-C12 (QUALITY 143). The case measures the fleet's own registry gate {F}/scripts/sources-census.sh pinned at fleet commit {PIN} under its own `selftest`; spec {E}/c1/census-mutants.json (12 single-edit mutants C01-C12, each with a witness registry).
Frozen counter (sha256 {COUNTER_SHA}): `{C1}` (~2 m 45 s; prints C1_ROW lines, C1_SUMMARY, C1_CONJUNCTS, C1_R92_PASS=true|false). At the base the counter refuses at setup (`C1_SETUP spec-absent-at-rev`, exit 2): the do-nothing receipt.
Control battery: {E}/c1/controls-v92.py + receipts {E}/pre-freeze/controls/ (summary C1-summary.txt, derived from the receipts by the driver). `{CTL}` (~12 min with --jobs 3; prints per-state MATCH/MISMATCH and `C1_CONTROLS states=.. matched=..`).
Spec id set: C01-C12. The note's single verdict table has header `| id | arm targeted | edit | verdict | witness |`.
Frozen artifacts (never edit, rename or replace): plans/round-92.plan.md, .ufo/waves/round-92/claims.json, and everything under .ufo/evidence/round-92/.

Your item is READ-ONLY on the lane except for your own deliverable(s): write them at the absolute paths your item names, inside {W}/. If you build a probe, fixture or script, COMMIT NOTHING but SAVE ITS SOURCE next to your deliverable ({W}/<your-seat-name>-<name>.<ext>) with its output, so the L1 can re-run it from committed bytes. Return a short final message naming your file and its VERDICT line.

# Hard rules for every seat
- Scratch: every clone, copy, fixture or work dir lives under {SC}/<your-seat-name>/ (mkdir -p). Pass it explicitly (TMPDIR, --work, --outdir). Never write under /tmp except files under 50 MB. Remove your scratch dir before you yield: trap 'rm -rf -- "$S"' EXIT in shell. Check `{F}/scripts/hyaku/disk-guard.sh status` before a heavy pass.
- Git fixtures: create any fixture repo or clone under your scratch dir (D=$(mktemp -d -p {SC}/<seat> fx.XXXXXX) && git -C "$D" init -q, or git clone --shared); never pass an empty or unchecked variable to git -C; verify git -C "$D" rev-parse --show-toplevel equals $D before the first commit. Commit only inside such a fixture, with identity ctl <ctl@fixture.invalid>.
- Never run git add, commit, stash, checkout, switch, reset, pull, push, or any mutating jj command in {L}, in {F}, or in any sibling lane repo. Read-only git (show, log, ls-tree, cat-file, rev-parse, diff, status, archive) is fine.
- Never modify any file under {L} except your own deliverable(s) under {W}/. Never edit {F}/scripts/ (the census gate is read-only: mutate only scratch copies), {F}/templates/, MANIFEST.json, tools/, corpus/, SCORECARD.md, LOG.md, or any sibling lane repo. Never write into /home/vgpnk/Projects/shokuknow.
- Never mutate host settings (sysctl, services, user namespaces, ptrace scope). Name a need in your deliverable instead.
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. Use absolute paths everywhere.
- Never message agent://all; the L1 is TameshiR92.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool, version, channel and reason in your deliverable).
- pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide; install via uv tool, npx, or an official binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, never downgrade, never restart a host service.
- Never call the `ask` tool. The round is unattended.
- Your deliverable ends with a line `VERDICT: <one token>` and a line `TOOLS: none` or the installs with version, channel and reason.
- Run only what your item names; do not run unrelated repo sweeps.
"""

items = [
    ("T92E1", "executor",
     f"TARGET (independent reproduction OUTSIDE the counter): for each of the 12 mutants in {E}/c1/census-mutants.json, {MAT}; apply the mutant's exact `old`->`new` edit to the copy with your own code (not measure-v92.py; assert the old string occurs exactly once), run the selftest in your ordinary shell environment (do NOT use env -i), twice, and record rc and the SURVIVED/killed arm lines. Compare each verdict (rc 0 = SURVIVED, else KILLED) with the C1_ROW lines in {E}/pre-freeze/controls/pos-real.out. Then run the frozen counter once at the freeze: `{C1.replace('<REV>', FREEZE)}` and paste its full stdout. Save your driver as {W}/T92E1-repro.sh (or .py). Deliverable: {W}/T92E1.md — a 12-row table (id, rc run1/run2, which selftest arm differs, derived verdict, counter verdict, agree/disagree), the counter stdout, and `VERDICT: reproduced-12/12` or `VERDICT: differs:<ids>`."),
    ("T92E2", "executor",
     f"TARGET (no-harm baseline and landing): at the base {BASE} AND at the freeze {FREEZE}, each in its own `git clone --shared` under your scratch, run the lane's standing sweeps from the clone root and paste their summary lines and exit codes: `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json` (summary SELFSTATE:), the same with `--pin-audit` (read the tool's docstring for the exact flag usage), `python3 -I -X utf8 tools/registry-figure-bind.py` with its manifest (read its docstring; use --manifest tools/registry-figure-bind.json if required), `python3 -I -X utf8 tools/pointer-recheck.py` with tools/pointer-recheck.json (read its docstring), and `python3 -I tools/registry-check.py --root .` (all rows; it can take minutes). Deliverable: {W}/T92E2.md — one table base vs freeze per sweep with the exact command, summary line and exit, plus `VERDICT: no-regression` or the named regression. Do not change any file in the clone except your scratch receipts."),
    ("T92E3", "executor",
     f"TARGET (reproduce the control battery from committed bytes): run `{CTL}` exactly (jobs 3, receipts under your scratch), then (a) paste the driver's `CONTROL_INSTRUMENT sha256=` line and its final `C1_CONTROLS states=.. matched=..` line with the exit code; (b) for each receipt you produced, compare against the committed receipt of the same name in {E}/pre-freeze/controls/ on the STABLE lines only — every `C1_ROW`, `C1_CONJUNCTS`, `C1_R92_PASS` and `C1_SETUP` line — ignoring the drive-level header (`control=`, `clone_rev=`, `parent=`, `mutant=`, `counter_sha=`) and `exit=`; list every receipt whose stable lines differ; (c) explain each difference at file level; (d) verify your instrument sha line equals {COUNTER_SHA} and run the frozen counter at the freeze `{C1.replace('<REV>', FREEZE)}`, pasting `C1_CONJUNCTS` + `C1_R92_PASS`. Deliverable: {W}/T92E3.md with `VERDICT: reproduced` only if every stable line matches; otherwise `VERDICT: differs:<files>`."),
    ("T92SC1", "scribe",
     f"TARGET (case-note status addendum draft): draft the append block for {L}/corpus/knowledge/mutation-case-fleet-sources-census.md at {W}/T92SC1-addendum.md (the L1 integrates it; do not write into corpus/). It must (1) state the round-92 certification status under the sealed counter {E}/c1/measure-v92.py with its sha256 {COUNTER_SHA}, the freeze {FREEZE}, the honest receipt path, and the control battery summary; (2) cite S320 (sha256sum(1), https://man.archlinux.org/man/sha256sum.1.en, opened 2026-11-08) for the self-pin digest semantics, in the note's own `source:` style; (3) name the limit classes the counter does not cover (fenced tables, HTML tables, prose verdicts, a note that copies predictions instead of receipts) — read {L}/corpus/lessons/round-90.md § Limits and {L}/corpus/lessons/round-91.md for the exact wording the note already uses; (4) never claim admission (admission is the closure's). Deliverable: {W}/T92SC1-addendum.md and `VERDICT: draft`."),
    ("T92S1", "scout",
     f"TARGET (independent source verification, S320): re-fetch https://man.archlinux.org/man/sha256sum.1.en yourself into your scratch with `curl -sS -D headers -o body`, record the HTTP date header, byte size and sha256, and compare with the committed snapshot {E}/sources/s320.html (sha256 b968bc09839877f9b0bf892b8a37fce0f72f4fa0ff0f17208824161b8547277b, 12127 B) and its headers file. Tag-strip the body, verify the two quotes the lesson's Gate records — \"Print or check SHA256 (256-bit) checksums.\" and \"The sums are computed as described in FIPS-180-2.\" — give their line numbers in your stripped text and their `wc -w` word counts (≤25 each), and verify the registry row {L}/corpus/SOURCES.md S320 parses as 11 columns with status mined, opened 2026-11-08, and used-by naming corpus/lessons/round-92.md. Deliverable: {W}/T92S1.md with `VERDICT: agree` or `VERDICT: disagree:<what>`, plus the fetched files saved beside it."),
    ("T92S2", "scout",
     f"TARGET (audit the parser's premise on the real note): write a read-only probe that (a) enumerates every Markdown table row in {L}/corpus/knowledge/mutation-case-fleet-sources-census.md (0-3 leading spaces, `## Registry` irrelevant here) and in {L}/corpus/README.md, listing for each row its first cell and whether it is id-shaped per `^[A-Za-z]{{1,4}}[_-]?[0-9]{{1,4}}$` or carries a KILLED/SURVIVED token; (b) proves the honest note raises no refusal of the frozen parser (run the parser's logic in isolation or call the committed counter at the freeze); (c) names every table FORM in the note the parser would not key (fenced code, HTML table, cell with an escaped pipe, table without a `verdict` header, a row whose id cell has leading text) and gives one concrete example of each found; (d) checks the README row that satisfies the coverage conjunct and quotes it. Deliverable: {W}/T92S2.md with the row census table and `VERDICT: premise-holds` or `VERDICT: over-broad:<rows>` / `VERDICT: blind:<forms>`."),
    ("T92R1", "reviewer",
     f"TARGET (code review of the C1 counter for false-green and false-red paths): review {E}/c1/measure-v92.py at the freeze line by line. Find any way a committed lane state could print C1_R92_PASS=true while some note verdict is not the true selftest verdict of its mutant, and any way an honest note would be refused. Cover at least: the self-pin normalisation (can an edited file keep the same normalised digest? what if the SELF_SHA256 line is duplicated or moved?), parse_note's fence handling and header counting, escaped pipes and cell trimming, duplicate and out-of-set rows, the `measured:` regex, the source/coverage checks, materialize/tar extraction, env_for, the canary, the validity/trivial checks, the two-run stability rule, and the seal. Cite file:line for every finding and give severity (blocker / should-fix / note). Deliverable: {W}/T92R1.md with `VERDICT: clean` or `VERDICT: findings:<n>`."),
    ("T92R2", "reviewer",
     f"TARGET (freeze conformance): with read-only git, check (1) every receipt under {E}/pre-freeze/controls/ and the counter/driver blobs were committed in a strict ancestor of the freeze {FREEZE}, and that the counter blob sha256 at the freeze equals {COUNTER_SHA}; (2) {L}/.ufo/waves/round-92/claims.json's `freeze` field equals the freeze rev named in the plan (QUALITY 144 / r91 routed defect 2); (3) the predicate in {L}/plans/round-92.plan.md is the same condition as the counter's `ok = all(conj.values())` and the receipt label C1_R92_PASS; (4) the plan's declared sha256 of the counter equals the committed blob's sha256 and the sha256 the driver printed; (5) the two r91 routed record repairs are actually present in this round's tree (the stale 'QUALITY 143-148' counts corrected append-only; the claims.json freeze pin). Deliverable: {W}/T92R2.md — one row per check with the command and observed value, `VERDICT: conformant` or `VERDICT: defects:<n>`."),
    ("T92C1", "critic",
     f"TARGET (attack R92-C1 as framed): read the plan's claim, predicate and kill rule, then TRY TO KILL the claim under its own kill rule (a): build in a scratch clone (`git clone --shared {L}`, checkout {FREEZE}, commit with the fixture identity) the cheapest note/SOURCES/README state you can that reaches C1_R92_PASS=true WITHOUT holding the true verdicts (12/12 from {E}/pre-freeze/controls/pos-real.out), or argue the claim is unreachable/unfalsifiable. Try at least: a second table inside a fenced block, an HTML table, a row with an escaped pipe, a verdict word inside prose vs a table, a duplicated header, a note that drops a spec id, a `measured:` line inside a fence, and a source/coverage decoy. Save every attempt as {W}/T92C1-<name>.* with the counter's full output and exit. Deliverable: {W}/T92C1.md with the attempt table and `VERDICT: survives` or `VERDICT: killed:<attempt>`."),
    ("T92M1", "mutation-tester",
     f"TARGET (mutation-test the counter against its own battery): copy {E}/c1/measure-v92.py to your scratch. Write a spec of at least 14 single-edit defects, each weakening ONE conjunct or check (self-pin assert, id-shape rule, unkeyed rule, position rule, dup rule, header count, figure, source, coverage, witness rule, canary, two-run rule, seal, pin). Save the spec as {W}/T92M1-defects.txt BEFORE running anything. For each defect, recompute the SELF_SHA256 line for the mutated bytes (the pin is a seal, not a defence against a deliberate mutation study — say so), then run the mutated counter against the battery state that must expose it (use `{E}/c1/controls-v92.py --only <state> --states-only` with a scratch copy whose counter path points at your mutant, or build the state yourself) and score KILLED (the mutant's receipt differs from the frozen one) vs SURVIVED. Deliverable: {W}/T92M1.md — the defect matrix, the survivors named, and `VERDICT: killed:<k>/<n>` plus the survivor list. D01/D02/D03 of the plan are not re-declared: you may use them as examples of the expected form."),
    ("T92SN1", "sentinel",
     f"TARGET (safety audit of the round's committed drivers): read {E}/c1/controls-v92.py and {E}/c1/measure-v92.py. Check: every git call that mutates (clone, checkout, add, commit, replace) targets a directory asserted to be its own toplevel and never an empty or unchecked variable (the 2026-11-06 fleet incident: `git -C \"\"` fell back to the fleet root); no write can land outside the scratch dir or the lane's .ufo/evidence/round-92/; scratch is removed on exit (temp dirs, the `_states` dirs, receipts keep); no hardcoded /tmp; the `--work`/`--outdir` arguments are validated; `git replace` creation cannot touch the lane or fleet repo; nothing reads credentials or host settings. Run nothing that writes outside your scratch. Deliverable: {W}/T92SN1.md — finding table with file:line, severity and a suggested fix — and `VERDICT: clean` or `VERDICT: findings:<n>`."),
]

spec = {
    "wave": "r92-w1",
    "maxLanes": 16,
    "reportDir": ".ufo/waves/round-92/w1",
    "hoist": False,
    "context": context,
    "items": [
        {"name": n, "role": r, "axes": ["verification-fixture-craft"], "item": GOD + t}
        for n, r, t in items
    ],
}
json.dump(spec, open(L + "/.ufo/waves/round-92/w1-spec.json", "w"), indent=1)
print("items=%d" % len(items))
