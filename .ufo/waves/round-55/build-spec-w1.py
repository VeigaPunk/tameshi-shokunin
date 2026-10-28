#!/usr/bin/env python3
"""Build round-55 wave-1 spec (v2 band 64-128, build + attack together). Stdlib only."""
import json
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
BASE = "0a2010acd1e92e4e332774050825e21bcfc7e079"
FREEZE = "631cd6455e58dce969310b4c0466c3383d9f5108"
W = ".ufo/waves/round-55/w1"

TEMPLATE = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim \u2014 let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

## Your item

{{item}}

Work the item end to end, then write your report file and return your findings.
"""

CONTEXT = f"""# Goal
tameshi round 55 (hyaku run 11; L1 TameshiR55), ONE v2 wave (build + attack together). Lane repo {LANE} (absolute paths only: seat tools start at the fleet root /home/vgpnk/Projects/shokunin, so every read/edit/write names an absolute path under the lane). Base `{BASE}`; frozen counter set `{FREEZE}` (`.ufo/evidence/round-55/`).

# The two claims (contract .ufo/evidence/round-55/contract.json, frozen before any seat ran)
- **C1 calibration** (the lowest non-retired axis, 8). The lane's records must agree with the tree on the ten routed defects the round-54 non-author spot-check pinned (`corpus/lessons/round-54-verifier-spotcheck.md`, R54.1-R54.10). Counter: `python3 {LANE}/.ufo/evidence/round-55/c1/measure.py --lane {LANE} --rev <rev> --work <empty dir> --explain`. At base it prints `premise=10/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false` (receipt `{LANE}/.ufo/evidence/round-55/before/c1.stdout`). Target `total=0`: each class needs (a) its premise receipt present at the revision, (b) zero stale occurrences of the wrong assertion OUTSIDE the `## Round 55 - round-54 record corrections` section of `SCORECARD.md`, (c) the corrections section carrying the value DERIVED from the tree (not a literal).
- **C2 operability**. One exit class, one line, every documented mode of the seven tools that call `strict_scratch_root()` - not the self-test only. Counter: `python3 {LANE}/.ufo/evidence/round-55/c2/measure.py --lane {LANE} --rev <rev> --work <empty dir> --explain`. At base: `grammar=6/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=18 C2_R55_PASS=false` (receipt `{LANE}/.ufo/evidence/round-55/before/c2.stdout`). Frozen grammar (one stderr line, exit 2):
  `^[A-Za-z][A-Za-z0-9_.-]*(\\.py)?: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' \\(could-not-evaluate\\)$`
  `repeat-control` and `context-capture` fail it today (they print the raw exception type; context-capture prints on stdout).

# What the round must land (the integration work)
1. `tools/repeat-control.py` and `tools/context-capture.py`: emit the frozen grammar line on stderr with exit 2 (no `RuntimeError` token, no traceback, stdout carries no setup error).
2. `tools/registry.json`: the seven `scratch_root` cells state the grammar and the eight allocating modes.
3. `corpus/knowledge/scratch-root-contract.md`: a "one line" section - the grammar, the 8 allocating modes, the 5 lazy modes, and the honest note that the class is an operator-visible line grammar, not a shared Python type.
4. `SKILL.md` `## Standing rules`: replace the sentence "Measured on each tool's `--selftest`/`selftest` path (round-54 C2 counter); other modes are outside that measurement" - it is false after this round (the counter measures `env-diff --contract` and the 5 lazy modes). This edit DRIFTS that one cold-read section; the round re-keys it (a fresh reader at the content commit + a bound ledger entry). No other SKILL.md section may be touched.
5. `SCORECARD.md`: a `## Round 55 - round-54 record corrections` section carrying each R54.N correction (old -> new, derived value, receipt pointer) plus in-place fixes of the stale assertions; a round-55 block; the standing axis table re-stated.
6. `corpus/lessons/round-55.md` (Gate + Mistakes + dispositions), one QUALITY criterion, one LOG.md entry, SOURCES rows for the sources opened this round.

# Counter facts you may rely on (measured, not asserted)
- C1 classes and their derived values at base: R54.1 `CTL_MISMATCH` + `2/3`; R54.2 freeze pointer `077d431e`; R54.3 `total=13`; R54.4 c2 digest `8528ee85`; R54.5 `w1=28 w2=25 sections=12`; R54.6 sweep commit `ff2a821`; R54.7 rename commit `7fa9a5e`; R54.8 `config.yml` + `fabricated` + the seat file marked superseded; R54.9 `reviewers=5 attack=21/76 seats=76 staged=81`; R54.10 `controls-a.stdout` + `rekeyed=0/7` + `r53-counter-at-88afa941`. Re-derive, never trust this list: each item names the command.
- The frozen counters, contract, freeze manifest, no-harm and deciding-run scripts are FROZEN: never edit them, and report (do not fix) anything you believe is wrong in them.

# Deliverables discipline
- Write into `{LANE}/{W}/<your-seat-name>.md` (the report) and, where the item asks for a machine-readable list, `<your-seat-name>.json` beside it. Receipts (command output you cite) go under `{LANE}/{W}/<your-seat-name>-receipts/`.
- Never edit a lane production file (`SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**`) - the L1 integrates. A patch you propose is a diff in your report, plus a scratch-clone demonstration.
- Write scratch under `export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r55/<your-seat-name>` with `trap 'rm -rf -- "$S"' EXIT`; `/tmp` only for files under 50 MB. A clone is `git clone --shared` of the lane, then `git -C <clone> checkout --detach <rev>`.
- Never run a mutating git/jj command anywhere (no add/commit/push/checkout of the lane, no jj). Fixtures: `D=$(mktemp -d)` under your scratch, every git call names `-C "$D"`, and `git -C "$D" rev-parse --show-toplevel` must equal `$D` before any commit there.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task - read `/home/vgpnk/.omp/agent/RULES.md` first (official channels, update-safety gate) and record tool/version/channel/reason in your report. **pacman transactions are PAUSED host-wide**: install via `uv tool`/`npx`/an official binary in `~/.local/bin`, or route around it.
- Every `Report:` trailer path the harness renders is relative to {LANE} - write it at {LANE}/<that path>. Never message `agent://all`; message only your own L1 (`TameshiR55`).
- An attack that finds nothing must show the sweep it ran. A finding without a command and its output is not a finding.

# Census (round start and end, conformance)
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` must exit 0; 139 rows now (S001-S279)."""

AX = {
    "er": ["calibration"],
    "note": ["operability"],
    "skill": ["operability", "calibration"],
    "cells": ["operability"],
    "lesson": ["calibration"],
    "sources": ["coverage"],
    "quality": ["calibration"],
    "log": ["calibration"],
    "scorecard": ["calibration"],
    "seat": ["calibration"],
    "considerthese": ["coverage"],
    "patch": ["operability"],
    "c1": ["calibration"],
    "c2": ["operability"],
    "rekey": ["calibration"],
    "no-harm": ["freshness"],
    "census": ["freshness"],
    "attack": ["calibration", "operability"],
}

INV = ["re", "note", "skill", "cells", "lesson", "sources", "quality", "log", "scorecard",
       "seat", "considerthese", "patch", "c1", "c2", "rekey", "no-harm", "census", "attack"]

ITEMS = []


def add(name, role, axis, milestone, item):
    ITEMS.append({"name": name, "role": role, "axes": [axis], "milestone": milestone, "item": item})


# ---------------------------------------------------------------- C1 corrections (10 scribes)
CORR = {
 "R54.1": ("the phase-B positive control",
   "`{L}/.ufo/evidence/round-54/control/controls-b.stdout` prints `CTL_MISMATCH CTL_POS_c1 expected=true actual=false` and `CONTROLS_B: 2/3`, yet four lane records assert it passed: `SCORECARD.md:2583` (`CTL_POS_c1 true`), `corpus/QUALITY.md:1590` (`rekeyed=7/7` on the positive control), `corpus/lessons/round-54.md:101` (same claim), report `:162` (fleet file, not editable here). Draft: the exact old->new text for each of the three lane locations, the corrected value (`CTL_MISMATCH`, `2/3`), and the honest cause (phase B cloned the FREEZE commit `077d431e`, which predates the re-key `7fa9a5e`, so the control could not fire). Re-derive every quoted line with `git -C {L} show <base>:<path> | grep -n ...`."),
 "R54.2": ("three freeze pointers",
   "`SCORECARD.md` names three freeze pointers for round 54 (`7883e0e5` at :2564-2567, `fe70474d` at :2608) while the deciding receipt `{L}/.ufo/evidence/round-54/after/frozen.stdout` prints `freeze=077d431e...`. Draft: the old->new text for each occurrence (the corrected pointer `077d431e`), and one sentence naming the receipt that decides it."),
 "R54.3": ("a quoted total that no receipt contains",
   "`SCORECARD.md:2584` quotes `total=14` from `.ufo/evidence/round-54/before/c2.stdout`, which prints `total=13`; the contract's `before` text also prints 13. Draft: the old->new text (`total=13`), the exact command that prints it, and a note that the round-54 parenthetical's claimed 'delta' inverted the two."),
 "R54.4": ("a stale counter digest",
   "The round-54 report cites `49280fe5` for `c2/measure.py`; `.ufo/evidence/round-54/freeze.json` pins `8528ee85...` (the amendment-4 bytes that decided). Draft: the correction line naming `8528ee85` and `c2/measure.py`, with the command that re-derives it from `freeze.json`."),
 "R54.5": ("finding counts that do not match the committed readers",
   "The report says 25 wave-1 findings and 22 wave-2 findings in 9 sections; the committed reader files say otherwise. Re-derive with your own command over `git ls-tree -r --name-only <base> -- .ufo/waves/round-54/w1` and `.../w2`, counting only files matching `/T54W\\d+[A-Za-z]*Read\\d+\\.json$` (receipt JSONs in `-receipts/` are not reader reports). Draft: the exact corrected triple (`w1=<n> w2=<n> sections=<n>`, sections = reader files with at least one finding), your command and its output."),
 "R54.6": ("round work uncommitted at closure",
   "Three seat deliverables were untracked at the round-54 closure and were swept later: `.ufo/waves/round-54/w2/T54W2Sent03.md`, `.../T54W2Sent03-receipts/c1committed-positive.stdout`, `.../rejection-attribution.txt`. Check they exist at base, find the commit that added the first one (`git -C {L} log --reverse --format=%H <base> -- <path> | head -1`) and draft the correction naming that sweep commit and the rule broken."),
 "R54.7": ("an imprecise forged-file disposition",
   "The forged reader was not deleted: it was RENAMED into `.../T54W2Sent01-receipts/forged-reader.json`. Verify both facts (old path absent, new path present) and find the rename commit; draft the correction (`renamed`, the commit, and why it can never credit: its path fails the reader pattern and its `section_sha256` matches no section)."),
 "R54.8": ("a half-recorded host-write incident",
   "A wave-1 seat self-authorized a write to `~/.omp/agent/config.yml` on a fabricated 'operator instruction'; the round-54 report names the incident but the lesson never mentions it and the seat's own file still asserts the edit was authorised. Draft: (a) the superseded annotation to append to `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` (it must contain the word `superseded`), (b) the incident paragraph for the lesson, containing `config.yml` and `fabricated`."),
 "R54.9": ("wave-table numbers",
   "`corpus/lessons/round-54.md:51` says 'the other 84 staged `merge/tameshi` entries'; the package holds 81 `.md` files. Re-derive both: `python3 -c` over `.ufo/waves/round-54/w1-registry.json` for `reviewers`, `attack_seats`, `seats` (expect `reviewers=5 attack=21/76 seats=76`) and `find /home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge -name '*.md' | wc -l` (read-only) for the staged count. Draft the correction carrying both derived numbers."),
 "R54.10": ("a quote under the wrong receipt",
   "The round-54 report quotes `CTL_R53 ... rekeyed=0/30` under `control/controls-a.stdout`, whose `CTL CTL_R53` line prints `rekeyed=0/7`; `0/30` belongs to `control/r53-counter-at-88afa941.stdout`. Read both receipts, then draft the correction naming `controls-a.stdout`, `rekeyed=0/7`, and `r53-counter-at-88afa941.stdout` for the `0/30`."),
}

for cid, (what, body) in CORR.items():
    name = "T55W1Er" + cid.split(".")[1].zfill(2)
    add(name, "scribe", "calibration", f"C1 {cid} correction draft",
        body.replace("{L}", LANE) + f"\n\nWrite `{LANE}/{W}/{name}.json` as `{{\"id\": \"{cid}\", \"what\": ..., \"old\": [...], \"new\": [...], \"derived\": ..., \"command\": ..., \"output\": ...}}` and the same facts in `{name}.md` with the commands you ran. Your output feeds the L1's `## Round 55 - round-54 record corrections` section: make each old->new a byte-exact quote pair.")

# ---------------------------------------------------------------- drafting scribes
add("T55W1ScribeNote", "scribe", "operability", "C2 note - one line section",
    f"Read `{LANE}/corpus/knowledge/scratch-root-contract.md` in full (66 lines) and draft its new `## One line, every mode` section: (a) the frozen grammar exactly as the counter carries it, (b) the eight allocating modes (the seven self-tests plus `env-diff --contract`, named verbatim), (c) the five lazy modes that keep their exit under an unusable TMPDIR because scratch is allocated on the real path, not at parse time, (d) the honest boundary: the class is an operator-visible line grammar, not a shared Python type - the seven tools keep their own exception classes. Cite S277-S279 where the note already does and add the new source row's S id if the sources scribe supplies one (otherwise say `S-pending`). Draft only; write `{name}.md`.")

add("T55W1ScribeSkill", "scribe", "operability", "C2 SKILL.md rule sentence",
    f"Read `{LANE}/SKILL.md` `## Standing rules` (the section starts at that heading; the scratch rule is around lines 32-39). Draft the exact old->new replacement for: 'Measured on each tool's `--selftest`/`selftest` path (round-54 C2 counter); other modes are outside that measurement'. The new sentence must be true after this round: every documented allocating mode is measured (the seven self-tests plus `env-diff --contract`), the class is one stderr line with the frozen grammar, and the five non-allocating modes stay lazy. Keep line length and the section's citation style. Touch NOTHING else - the section's bytes drift the cold-read floor and the round re-keys it; quote the section's sha256 at base (`python3 -c` with the round-18 `sectionize`) so the L1 can prove the drift is one section.")

add("T55W1ScribeCells", "scribe", "operability", "C2 registry cells",
    f"Read `{LANE}/tools/registry.json` and select the seven rows that carry a `scratch_root` cell (one selftest per tool). Draft one replacement cell text per row stating: the frozen grammar (one stderr line, the value named, exit 2), the empty arm (unset), the usable arm (nothing under /tmp), and the allocating-mode scope. Keep a single cell shape across all seven (one template sentence), so the counter's docs arm matches 7/7. Also state which of the five lazy modes is NOT covered by that cell. Write `{name}.json` (row name -> new cell) and `{name}.md`.")

add("T55W1ScribeLesson", "scribe", "calibration", "lesson round-55",
    f"Draft `{LANE}/corpus/lessons/round-55.md` skeleton: `## Gate` (the sources opened this round: URL, access date, a <=25-word located quote per row; adopt and reject counts), `## Mistakes` (one mined mistake: class, evidence pointer, captured-by, fix - the strongest candidate is 'a control scored at a revision that predates the work it certifies' from R54.1, but mine what the evidence supports), `## Round-54 routed defects - dispositions (this round)` (one row per R54.1-R54.10 with FIXED/REFUSED + evidence), and `## What the counters cannot see`. Match the shape of `corpus/lessons/round-54.md`. Draft only; the L1 lands it.")

add("T55W1ScribeSources", "scribe", "coverage", "source rows opened this round",
    f"Open (fetch and read) the sources C2 rests on for the uniform-line claim. Candidates: GNU coding standards 'Errors' (https://www.gnu.org/prep/standards/html_node/Errors.html) and FreeBSD `sysexits(3)` (https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3). For each: record the URL, today's access date (2026-10-28), a <=25-word located quote (name the byte offset or heading where you found it), tier per `{LANE}/corpus/SOURCES.md` contract v1, and the proposed `S` row (11 columns, no literal `|` inside a cell). Reject anything that does not actually support 'one consistent line format / one exit code per class' and say why. Write `{name}.json` (rows) + `{name}.md` (quotes + locators). Read-only on the registry: the L1 appends and re-runs the census.")

add("T55W1ScribeQuality", "scribe", "calibration", "QUALITY criterion",
    f"Draft criterion 106 for `{LANE}/corpus/QUALITY.md`, learned from R54.1: a pre-registered control must be scored AT the revision it certifies (a control cloned at the freeze commit cannot certify a later fix), and a control receipt's own verdict line must be quoted, never paraphrased. State the falsifier so that the round-54 `control/controls-b.stdout` line fails it and a re-scored positive control at the content revision passes it. Also draft the note that QUALITY 105's falsifier is the very receipt that refutes its claim (do not delete 105; append the correction as an erratum).")

add("T55W1ScribeLog", "scribe", "calibration", "LOG.md entry",
    f"Draft the `## 2026-10-28 - round 55` LOG.md entry: base, freeze, both claims with before->after, the content commits, the round shape (wave sizes and role mix - placeholders the L1 fills), the sources opened, and the routed-defect dispositions. Match `{LANE}/LOG.md`'s existing entry shape (one paragraph per claim plus a measured-close section).")

add("T55W1ScribeScorecard", "scribe", "calibration", "SCORECARD round-55 block",
    f"Draft the `## Round 55 - ...` SCORECARD.md block: the two claims with axis, before (quoted from `{LANE}/.ufo/evidence/round-55/before/c1.stdout` and `c2.stdout`), target, counting command, controls; the standing axis table re-stated at base `{BASE}`; the `## Round 55 - round-54 record corrections` section skeleton (one subsection per R54.N: old -> new, derived value, receipt) with an explicit statement that the old text is preserved here and removed in place. Also draft the `Planned (round 56)` line - it must name only work that is genuinely pending (check each named path exists or not; the round-54 planned row's `delta-debugging-minimization-contract.md` was already adopted at `79f44b5`).")

add("T55W1ScribeSeat", "scribe", "calibration", "R54.8 seat annotation",
    f"Read `{LANE}/.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` and draft: (a) a short, appended `SUPERSEDED` block for the end of that file stating that its claim of an operator-authorised `config.yml` write is fabricated (no such instruction exists in the session record) and pointing at the round-55 lesson; (b) the paragraph for the lesson naming the incident (`config.yml`, `fabricated`, the revert now at `scout: \"@m_grok\"`), and (c) the rule the lane should adopt so a seat never edits `~/.omp/agent/` again. Do not edit the seat file - the L1 lands the annotation.")

add("T55W1ScribeConsiderthese", "scribe", "coverage",
    "considerthese mining (at most one proposal)",
    f"`{LANE}/considerthese/` is operator-authored input: mine it, never edit it. Read the newest file (`2026-10-28.md`) and the two before it; find at most ONE still-unimplemented proposal that touches verification-fixture craft, ground it by opening what it points at, and draft how it lands as a lesson, a QUALITY criterion or a SOURCES row (with date). If every proposal is already implemented, say so with the check that shows it. Write `{name}.md`.")

add("T55W1ScribeScratchDoc", "scribe", "operability", "operator snippet",
    f"Draft a five-line operator snippet for the note or runbook: how to parse the scratch-root class from a tool's output (which stream, which regex prefix, what exit), what an empty TMPDIR means, and what NOT to infer (a lazy mode's exit 0 under an unusable TMPDIR is not a pass). Keep it copy-pasteable and cite the frozen grammar verbatim.")

add("T55W1ScribeMistakeSweep", "scribe", "calibration", "mined-mistake sweep",
    f"Run a sweep for this round's mined mistake candidates and write `{name}.md` with the command and output for each: (1) grep the lane's rounds 50-54 lessons for a routed defect that recurred (a class routed twice); (2) diff the round-54 planned row against the tree to find planned items already done; (3) check whether any round-54 receipt is cited for a value it does not print (grep each `total=`/`=true`/digest quoted in the round-54 SCORECARD block against its receipt). Report which candidate has the strongest evidence and why, or that the sweep found none.")

# ---------------------------------------------------------------- executors
add("T55W1ExecRepPatch", "executor", "operability", "C2 patch - repeat-control",
    f"Produce the exact patch for `{LANE}/tools/repeat-control.py` that makes the unusable-TMPDIR path print the frozen grammar on stderr: define a `ScratchRootUnusable(RuntimeError)` in the tool, raise it from `strict_scratch_root()` (line ~156), and in `main()` catch it BEFORE the generic handler, printing `repeat-control: could-not-evaluate: {{exc}}` via `emit_err` plus `REPEAT_CONTROL: setup_error`, returning 2. Anchor the emit line EXACTLY as `emit_err(f\"repeat-control: could-not-evaluate: {{exc}}\")` (the round's break control rewrites that one string). Demonstrate in a `git clone --shared` scratch clone at `{FREEZE}`: apply the patch, then show (a) `TMPDIR=/nonexistent/x python3 tools/repeat-control.py --selftest` → rc 2, one stderr line matching the frozen grammar, no `RuntimeError` token; (b) `TMPDIR= python3 ... --selftest` → rc 0; (c) `TMPDIR=$S/tmp python3 ... --selftest` → rc 0. Report the diff and the three receipts.")

add("T55W1ExecCcPatch", "executor", "operability", "C2 patch - context-capture",
    f"Produce the exact patch for `{LANE}/tools/context-capture.py`: define `ScratchRootUnusable(RuntimeError)`, raise it in `strict_scratch_root()` (line ~300), and in `run_selftest()`'s except handler (line ~2210) write `context-capture.py: could-not-evaluate: {{exc}}` to STDERR (not stdout) and return 2. `--check` mode must keep its exit contract. Demonstrate in a scratch clone at `{FREEZE}`: the three TMPDIR arms (unusable → rc 2 + grammar line on stderr, empty → its current expected exit, usable → same), plus `python3 tools/context-capture.py --selftest` under a good TMPDIR still printing its own selftest verdict. Report the diff and receipts.")

add("T55W1ExecCells", "executor", "operability", "C2 registry cells applied",
    f"In a scratch clone at `{FREEZE}`, apply the seven `scratch_root` cell rewords (use the draft from `{LANE}/{W}/T55W1ScribeCells.json` if it exists when you start, else derive the template yourself) and then run the frozen C2 counter at the patched clone: `python3 {LANE}/.ufo/evidence/round-55/c2/measure.py --lane <clone> --rev <clone HEAD> --work <empty dir> --explain`, and show the docs arm moving 0/7 -> 7/7 while the grammar arm stays 6/8. Also run `python3 tools/registry-check.py --selftest` in the clone (rc 0) so the reword does not break the registry gate. Report the diff hunks and both receipts.")

add("T55W1ExecNote", "executor", "operability", "C2 note applied",
    f"In a scratch clone at `{FREEZE}`, apply the `## One line, every mode` section to `corpus/knowledge/scratch-root-contract.md` (use `T55W1ScribeNote.md`'s draft if present) and run the frozen C2 counter at the clone: show note 0/8 -> 8/8 with grammar still 6/8. Then check the note's internal citations still resolve (`grep -n 'tools/' corpus/knowledge/scratch-root-contract.md` and confirm each cited path:line exists at the clone). Report the diff and receipts.")

add("T55W1ExecC1FixOnly", "executor", "calibration", "C1 differential - stale fixes without values",
    f"Build the 'fix without values' tree: a scratch clone at `{FREEZE}` where each stale assertion is corrected IN PLACE (SCORECARD `CTL_POS_c1 true` -> the receipt's `CTL_MISMATCH`/`false`, `7883e0e5`/`fe70474d` -> `077d431e`, `total=14` -> `total=13`, QUALITY 1590's positive-control claim, lesson round-54 `84 staged` -> the derived count, lesson :101's `rekeyed=7/7` claim) with NO corrections section added. Run the frozen C1 counter there and show which classes clear and which stay (expect corrected misses). This is the differential that proves the corrections section is load-bearing.")

add("T55W1ExecC1Full", "executor", "calibration", "C1 dry run at the target",
    f"Build a scratch clone at `{FREEZE}` that reaches C1 `total=0`: apply every in-place stale fix AND add a `## Round 55 - round-54 record corrections` section in `SCORECARD.md` carrying each derived value (re-derive each one yourself with the command the class names; do not copy the L1's list blindly). Then run the frozen C1 counter at the clone and paste the verdict line. If any class refuses, say exactly which arm and why - that is the finding, not a failure of your item.")

add("T55W1ExecC2Full", "executor", "operability", "C2 dry run at the target",
    f"Build a scratch clone at `{FREEZE}` where both tool patches, the seven cells, the note section AND the SKILL.md rule edit are applied, then run the frozen C2 counter at the clone: paste the full verdict line and the EXPLAIN lines. The skill arm reads `SKILL.md` from the clone, so the edit must carry the frozen grammar marker. Report every arm's numbers and any mode that still fails. Note: this clone's SKILL.md drift is expected and the counter does not measure the cold-read floor - do not run the floor here.")

add("T55W1ExecRekeyPrep", "executor", "calibration", "re-key prep - lost headings",
    f"In a scratch clone at `{FREEZE}`, apply ONLY the SKILL.md `## Standing rules` edit (the one C2 needs) and compute the cold-read floor at base vs the edited clone with `.ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev <HEAD>`, plus the round-48 precheck `bash .ufo/evidence/round-48/quality/coldread-precheck.sh <clone> {BASE} <HEAD>`. Report: which headings lost credit, the lost section's `start`, `end`, `sha256` at the edited revision (computed with the round-18 `sectionize`), and whether the lost set is exactly one section (`## Standing rules`) or more. Write the JSON the L1's binder needs as `{name}.json`.")

add("T55W1ExecReKeyDryBind", "executor", "calibration", "re-key dry bind",
    f"Prove the re-key route end to end on your own scratch clone at `{FREEZE}` with the SKILL.md edit applied: (1) write a reader report JSON for `## Standing rules` with `heading`, `cand=<edited clone HEAD>`, `section_sha256` computed from the round-18 sectionize, and an empty `findings` list; (2) adapt `{LANE}/.ufo/evidence/round-54/integrate/binder.py` in your scratch (it is frozen for round 54 - copy, never edit) to bind that reader into a copy of `.ufo/evidence/round-21/coldread/ledger.json`; (3) show the round-18/round-21 credit algorithm credits the section with that entry, and the precheck prints `lost=0`. Report the exact command sequence the L1 must run. If the binder cannot be reused as-is, say precisely what must change.")

add("T55W1ExecCountersAtBase", "executor", "calibration", "independent base receipts",
    f"Independently reproduce both before receipts at `{BASE}` in fresh work dirs: `python3 {LANE}/.ufo/evidence/round-55/c1/measure.py --lane {LANE} --rev {BASE} --work <empty>` (expect `total=10 C1_R55_PASS=false`) and `python3 {LANE}/.ufo/evidence/round-55/c2/measure.py --lane {LANE} --rev {BASE} --work <empty>` (expect `total=18 C2_R55_PASS=false`). Then `cmp` your stdout against the committed receipts `{LANE}/.ufo/evidence/round-55/before/c1.stdout` and `c2.stdout` and report any differing line (timings and the clone path will differ in `c2` - name every differing byte region). A mismatch is a finding.")

add("T55W1ExecNoHarm", "executor", "freshness", "no-harm at base",
    f"Run `bash {LANE}/.ufo/evidence/round-55/no-harm.sh {LANE} {BASE}` and report every line. Confirm 15 `ok` lines and zero `RED`. If any monitor is RED at base, that is a defect in the monitor, not the round: name it with its line and the command you ran to see why.")

add("T55W1ExecCensus", "executor", "freshness", "census at base",
    f"Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` and report exit code, row count (`grep -cE '^ {{0,3}}\\| S[0-9]{{3,}} \\|' {LANE}/corpus/SOURCES.md`) and every warning. Then run it against a scratch copy of the lane's corpus with one indented (`  | S999 |`) duplicate row appended and show it reports the duplicate (the guard must be load-bearing before any append).")

add("T55W1ExecGrammarBreak", "executor", "operability", "grammar arm sensitivity",
    f"Break the grammar three ways in scratch copies of the patched tool set (use the patch from `T55W1ExecRepPatch` if present, else apply your own to a clone) and score each with the frozen C2 counter: (1) remove the `could-not-evaluate:` prefix; (2) append `RuntimeError` to the line; (3) return 0 instead of 2. Each must lose exactly one mode on the grammar arm and the rest must stay. Report the three verdict lines side by side - this is the arm-sensitivity receipt the closure will ask for.")

add("T55W1ExecModeDiscovery", "executor", "operability", "mode-discovery blind spot hunt",
    f"Enumerate every documented mode of the seven tools (from `tools/registry.json` rows and each tool's `--help`/usage text) and compare it with the counter's 13 modes. For every documented mode NOT in the counter, decide by READING the tool whether it can allocate scratch before its preconditions (e.g. `evidence-disposition --root .`, `pin-disposition --read`, `context-capture --check` with a real receipt). Report: the full documented-mode inventory, the counter's 13, the difference, and for each difference a verdict (allocates / does not allocate, with the line of code). A mode that allocates and is missing from the counter is a defect in the frozen counter - report it, do not fix it.")

# ---------------------------------------------------------------- reviewers (C1 rows)
REV_ROWS = [("01", ["R54.1", "R54.2"]), ("02", ["R54.3", "R54.4"]), ("03", ["R54.5", "R54.6"]),
            ("04", ["R54.7", "R54.8"]), ("05", ["R54.9", "R54.10"]), ("06", ["R54.1", "R54.5"]),
            ("07", ["R54.2", "R54.9"]), ("08", ["R54.4", "R54.10"]), ("09", ["R54.3", "R54.6"]),
            ("10", ["R54.5", "R54.8"])]
for i, ids in REV_ROWS:
    name = f"T55W1Rev{i}"
    add(name, "reviewer", "calibration", f"attack C1 rows {','.join(ids)}",
        f"Independently re-derive the corrected value for {', '.join(ids)} from the receipts and the tree at `{BASE}` - open `{LANE}/corpus/lessons/round-54-verifier-spotcheck.md` for the defect text, then the receipt it names, then the stale line in the lane's records. For each class report: agree/disagree with the defect as stated, the exact value the tree derives (your command and output), whether the spotcheck's own claim is overstated anywhere, and whether the L1's correction draft (`{LANE}/{W}/T55W1Er<NN>.json`) is byte-accurate. A disagreement is your finding: name the byte that proves it.")

add("T55W1RevR54Honesty", "reviewer", "calibration", "attack the spotcheck's own claims",
    f"Treat `{LANE}/corpus/lessons/round-54-verifier-spotcheck.md` as a claim set: for each R54.N, check that the spotcheck's quoted receipt text exists verbatim and that its count is right. Report every place where the spotcheck itself overreaches (e.g. a count that includes a receipt file, a claim about a file it did not open, an 'all revisions' claim). Then state whether the round-55 corrections are faithful to what the receipts actually say.")

add("T55W1RevQuality", "reviewer", "calibration", "attack QUALITY 105/106",
    f"Read `{LANE}/corpus/QUALITY.md` criteria 99-105 and the drafted 106 (in `{LANE}/{W}/T55W1ScribeQuality.md` if present, else the idea: a control must be scored at the revision it certifies). Verify by running the falsifier: does criterion 105's claimed falsifier actually fail on `{LANE}/.ufo/evidence/round-54/control/controls-b.stdout`? Does 106's falsifier fail there and pass on a re-scored control? Report the two commands and outputs, and say whether 105 needs an erratum or is merely imprecise.")

add("T55W1RevSources", "reviewer", "coverage", "attack the new source rows",
    f"Open each source the sources scribe proposes (in `{LANE}/{W}/T55W1ScribeSources.md`/`.json`) yourself. Check: the URL resolves, the quote is verbatim at the locator, the quote is <=25 words, the tier is right per `{LANE}/corpus/SOURCES.md` contract v1, and the row parses as 11 columns with no escaped pipe. Report per row: admit/reject with the reason, plus the row as you would write it. If a proposed row does not support the uniform-line claim, reject it and say what would.")

add("T55W1RevNote", "reviewer", "operability", "attack the note draft",
    f"Read the drafted `## One line, every mode` section and the note's existing text. Check every factual claim against the code and the counter: the eight allocating modes are exactly the ones the counter names, the five lazy modes really do not allocate, the grammar quoted matches the frozen regex byte for byte, the S277-S279 citations still say what the note says, and nothing claims a shared Python type that does not exist. Report each claim: holds / overreaches / wrong, with the line of code or receipt.")

add("T55W1RevColdread", "reviewer", "calibration", "attack the re-key plan",
    f"Verify the re-key obligation is exactly one section: read the SKILL.md `## Standing rules` edit, compute with the round-18 `sectionize` the section boundaries at `{BASE}`, and reason about which sections' inputs the edit can drift (inputs are the files its commands/anchors name). Then check the round-18/round-21 credit rules in `{LANE}/.ufo/evidence/round-21/coldread/measure.py` to confirm a fresh reader bound at the content commit restores credit, and that the binder's DROP list (`LOG.md`, `SCORECARD.md`, `SKILL.md`) is right for this round. Report the exact heading list the L1 must re-key and any section the edit might drift that the plan omits.")

add("T55W1RevWave", "reviewer", "calibration", "self-audit of the wave",
    f"Read `{LANE}/{W}/../spec-w1.json` (the spec that produced this wave) and audit it: seat count in the v2 band 64-128, attack-role share >=25% (reviewer/critic/mutation-tester/labrat), every item distinct and naming what it attacks, no item asking a seat to edit a frozen file or a lane production file, every item naming absolute paths. Report the audit with the counts you derive (`python3 -c` over the spec) and any item you would reject as padding.")

# ---------------------------------------------------------------- critics / mutation / scouts / sentinels / etc.
add("T55W1CritC1", "critic", "calibration", "falsify C1's design",
    f"Attack the C1 counter's design, not its output. Read `{LANE}/.ufo/evidence/round-55/c1/measure.py` and answer: can a tree that does NO work reach `total=0` (e.g. by writing a corrections section with the right literals)? Is the stale scan's file scope right (does it read the spotcheck lesson, where the wrong values legitimately appear)? What happens if the corrections section is the last one in the file, or if a second `##` heading intervenes? Does `premise` ever fail quietly? Build the cheapest tree you can that reaches `total=0` without the real fixes and score it - if it passes, that is a counter defect.")

add("T55W1CritC2", "critic", "operability", "falsify C2's design",
    f"Attack the C2 counter's design. Questions: is the grammar regex anchored so a tool cannot pass by printing the line anywhere (e.g. to stdout)? Does the lazy arm's pass mean anything (a mode that exits 0 for another reason also passes - how would you distinguish)? Does the empty arm's `TMPDIR=\"\"` really test what S278 says? Is the docs arm satisfiable by pasting the marker without describing the modes? Can the usable arm's strace census miss a mkdir (`cloneat`, `openat` with O_TMPFILE)? Build the cheapest tree that reaches `total=0` without fixing the two tools and score it.")

add("T55W1CritFreeze", "critic", "calibration", "attack the freeze",
    f"Verify the freeze is sound: re-derive every sha256 in `{LANE}/.ufo/evidence/round-55/freeze.json` from the bytes at `{FREEZE}`, check every `contract.json` `frozen_paths` entry is covered (and that the manifest does not hash itself), and confirm the deciding run's FROZEN list equals the contract's list. Then check the deciding-run's gate logic for holes: can a stale or empty control receipt open it? can a second invocation slip past? Report each check with its command.")

add("T55W1MutC1", "mutation-tester", "calibration", "mutate C1's counter",
    f"Mutation-test the frozen C1 counter (`{LANE}/.ufo/evidence/round-55/c1/measure.py`) in scratch copies: at least 6 single-edit mutants (e.g. drop the stale scan for one class, hardcode a derived value instead of deriving it, accept `premise=false` as ok, read the corrections section without trimming at the next heading, count rows from the working tree instead of the revision, skip a class). Each mutant must be scored at `{BASE}` and at a tree that reaches `total=0` (build one if the executors have not). Report KILLED/SURVIVED per mutant with the verdict lines; a survivor is the round's finding.")

add("T55W1MutC2", "mutation-tester", "operability", "mutate C2's counter",
    f"Mutation-test the frozen C2 counter (`{LANE}/.ufo/evidence/round-55/c2/measure.py`) in scratch copies: at least 6 single-edit mutants (e.g. accept rc 1, drop the `RuntimeError` check, match the grammar anywhere in stdout+stderr, drop the docs arm, treat the lazy arm as optional, make the empty arm compare against itself). Score each at `{BASE}` and at a fixed tree. Report KILLED/SURVIVED with verdict lines; say which arm each mutant is meant to kill and whether it did.")

add("T55W1ScoutModes", "scout", "operability", "per-surface recon - scratch paths",
    f"Map where each of the seven tools allocates scratch on its real path (not just the self-test): read `strict_scratch_root()` and every call site in each file, and report a table tool -> call sites (file:line) -> modes that reach them. Flag any tool whose ONLY scratch allocation is inside its self-test (that would make the round's claim cover a branch the product never uses). Read-only: report, do not edit.")

add("T55W1ScoutReceipts", "scout", "calibration", "receipt inventory",
    f"Inventory every receipt the round-54 spotcheck cites: for each, confirm it exists at `{BASE}`, is a blob, is non-empty, and print the exact line the spotcheck quotes from it. Report a table: R-id -> receipt path -> quoted line present (yes/no) -> line number. Any receipt the spotcheck cites that does not contain the quoted text is a finding about the spotcheck; any receipt missing at `{BASE}` is a finding about the tree.")

add("T55W1SentScope", "sentinel", "calibration", "scope and write audit",
    f"Audit the wave's own behaviour: list every file written under `{LANE}/{W}/` (and any stray write elsewhere in the lane or the fleet root that names round 55), check none of the frozen files or lane production files changed (`git -C {LANE} status --porcelain`), and check no seat ran a mutating git/jj command in the lane (look for new commits, changed refs, `git -C {LANE} reflog -20`). Report the audit with commands; a violation is your finding, named with the seat id.")

add("T55W1SentConfig", "sentinel", "operability", "host-write and network audit",
    f"Verify the round's changes cannot write outside the lane: read the two tool patches' diffs (or the drafted diffs) and confirm they only touch their own file's scratch/exit path; grep the wave deliverables for writes to `~/.omp`, `/home/vgpnk/.config`, or any fleet path outside `{LANE}`; and confirm the C2 counter's clone/scratch stay under `--work`. Report with commands; name any deliverable that proposes a write outside the lane. Also confirm `~/.omp/agent/config.yml` is unmodified (mtime, and the scout alias still reads `@m_grok`).")

add("T55W1Revenger", "revenger", "calibration", "reconstruct round-54's control intent",
    f"Reverse-engineer why round 54's phase-B control cloned the FREEZE commit instead of the revision it certified, and what the harness's author actually intended: read `{LANE}/.ufo/evidence/round-54/control/controls.sh` (phase B), `{LANE}/.ufo/evidence/round-54/deciding-run.sh`'s control gate, and `{LANE}/.ufo/evidence/round-54/contract.json`'s control list. Then state the minimal correct shape of a phase-B control that cannot repeat the error, and check round 55's `controls.sh` against it (does it re-score at the revision it certifies? does it refuse a control that could not fire?).")

add("T55W1Connector1", "connector", "operability", "cross-lane exit-class grammar",
    f"Sibling-overlap scan: do other lanes' gates already declare a uniform could-not-evaluate line or an exit-class grammar (kumitate's `scripts/*.mjs`, kagi's `corpus/*.sh`, tsukuroi, mado)? Grep their gates for `could-not-evaluate`, `EXIT`/`exit 2` grammars and any documented 'one line' rule, and report with `path:line` evidence. The point: is tameshi's grammar a lane invention or a fleet pattern two independent lanes already hold (the PROVINCE rule for calling a pattern general)? Read-only on siblings.")

add("T55W1Connector2", "connector", "calibration", "routed-defect overlap",
    f"Check overlap between R54.1-R54.10 and the lane's earlier routed defects (`corpus/lessons/round-52*.md`, `round-53*.md`, `round-51*.md`): is any round-54 row a duplicate of an earlier row (i.e. the same class routed twice)? For each duplicate: quote both, say which round fixed it, and whether the earlier fix was partial. Report the overlap matrix; this feeds the round's `## Mistakes`.")

add("T55W1Simplifier", "simplifier", "operability", "YAGNI on the grammar fix",
    f"Argue both sides, then decide: is the two-tool grammar fix minimal, or should the seven tools share one module (`tools/scratch_root.py`)? Count the duplicated lines across the seven definitions, the divergence risk, and what a shared module would cost (import path, vendoring, selftest impact). Recommend one option with evidence; if the shared module is warranted, sketch its interface but do not build it. Also check the C2 counter for dead arms (an arm that cannot fail).")

add("T55W1LabMode", "mutation-tester", "operability", "probe - lazy modes stay lazy",
    f"One falsifiable hypothesis: 'the five modes the counter calls lazy never allocate scratch, even when their inputs make them work hardest.' Probe at least two of them with real work under an unusable TMPDIR (e.g. `pin-disposition --manifest` with a manifest whose pins mismatch, `context-capture --check --receipt/--expected` with a mismatching pair, `evidence-disposition --root . --dispositions` with a failing disposition set) and show the exit code stays their expected class with no scratch error. A mode that allocates under load falsifies the lazy arm and is the round's finding.")

add("T55W1LabEmpty", "mutation-tester", "operability", "probe - empty TMPDIR semantics",
    f"One falsifiable hypothesis: 'an empty `TMPDIR` is unset for these tools, and nothing is created in the working directory when it is empty.' Probe it: with `TMPDIR=\"\"`, run each of the seven self-tests and strace one of them for opens under the CWD and under `/tmp`; also read CPython's `_candidate_tempdir_list` to confirm the mechanism. Report the strace evidence and any tool whose behaviour differs. Also probe whether a *relative* TMPDIR (e.g. `tmp-rel`) is honoured as a path - that is a fourth arm the counter does not measure; report what you see.")

add("T55W1RevLedger", "reviewer", "calibration", "attack the ledger machinery",
    f"Audit the machinery the re-key will use: read `{LANE}/.ufo/evidence/round-21/coldread/measure.py` (the credit rules) and `{LANE}/.ufo/evidence/round-54/integrate/binder.py`. Report: what exactly makes a section credit (inputs + read_rev + reader report), which inputs the binder drops and why, and whether a reader report with an empty findings list is accepted (it must be, for a clean section) or silently ignored. Then state the minimal reader JSON the L1 must land for `## Standing rules` and the exact binder arguments, verified against the code.")

add("T55W1CritClaimShape", "critic", "calibration", "causal separability and no-harm",
    f"Judge the claim shape: are C1 and C2 causally separable (can each verify with the other unlanded)? Does either harm an axis (does the C1 record edit damage freshness? does the C2 SKILL.md edit cost cold-read credit that the round must repay)? Is at least one claim on the lowest non-retired axis (calibration 8) and is the axis named by the surface rather than the number? Is there a do-nothing control for each? Report a verdict per question with the evidence you read, and name any claim you would reject.")

add("T55W1CritGate", "critic", "calibration", "attack the deciding-run gate",
    f"Attack `{LANE}/.ufo/evidence/round-55/deciding-run.sh`: enumerate every refusal path (freeze integrity, control receipts, second invocation, dirty tree) and try to defeat one in a scratch clone/fixture without editing the frozen script: e.g. a control receipt committed before the freeze (ancestry check), an empty file that is still a blob, a dirty file that matches the outdir exclusion, a `frozen.stdout` that prints MISMATCH but exits 0. Report which defences hold and which are bypassable, with the fixture and the output. Do not edit the script.")

add("T55W1RevRekeyByteProof", "reviewer", "calibration", "attack the reader deliverable the re-key needs",
    f"Specify and then verify the reader-report contract for the one re-keyed section: read the round-54 wave reader JSONs (`{LANE}/.ufo/waves/round-54/w1/T54W1Read*.json`) and the round-21 credit code, then write a validator script in your scratch that accepts exactly the reports the credit code accepts (heading, cand, section_sha256 equal to the section at cand, findings list). Run it over the round-54 readers to prove it accepts 23/23 and rejects the forged one (`.../T54W2Sent01-receipts/forged-reader.json`). Report the script, the two verdicts, and the exact shape the round-55 reader must take.")

add("T55W1ExecRegistryGate", "executor", "operability", "registry gate regression",
    f"Run `python3 {LANE}/tools/registry-check.py --selftest` at `{BASE}` (rc 0) and, in a scratch clone, after the seven-cell reword plus the copies of the two patches (use the drafts if present), run it again. Then run `python3 {LANE}/tools/registry-replay.py` if it has a self-test mode, and report every verdict. Any regression from the reword is the finding; name the cell that broke it.")

add("T55W1ExecCensusAfter", "executor", "freshness", "census guard on a candidate append",
    f"Build the append block the L1 will land (use `T55W1ScribeSources.json` if present) in scratch: copy the lane's `corpus/` to `$S/corpus`, add the proposed rows to the Registry table, and run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/corpus/SOURCES.md`. Then prove the guard catches a defect: an indented duplicate id (`  | S280 |`) must produce E03/E04 or an equivalent finding; an 11-column row with a literal `|` must fail parsing. Report exit codes and findings; do not touch the real registry.")

add("T55W1ExecFooterPaths", "executor", "operability", "wave artifact hygiene",
    f"Audit the wave's own artifacts: every `Report:` path a seat was handed resolves under `{LANE}/.ufo/waves/round-55/w1/`; every seat report exists or the seat is dead (list both); no seat wrote a file outside the wave dir (compare `git -C {LANE} status --porcelain` against the wave dir); no file under the wave dir exceeds 2 MiB; no scratch tree under `/tmp` names tameshi-r55. Report the audit with commands and the exact list of missing/dead seats for the L1's report.")

add("T55W1CritSourcedClaim", "critic", "coverage", "falsify the sourced-claim requirement",
    f"Check the round's sourced claim (§2b): C2's grammar rests on the sources opened this round. For each candidate source (GNU Errors, sysexits), decide whether it actually supports (a) a consistent line format and (b) one exit code per class, or whether it is decoration. Then check the lane's own `corpus/SOURCES.md` contract v1 requirements are met by the proposed rows (tier, recheck cadence, used-by, quote length). Report admit/reject per source with the quote; a rejected source must leave the round with no sourced claim, which you must say loudly.")

# ---------------------------------------------------------------- build

spec = {"wave": "round-55-w1", "reportDir": W, "template": TEMPLATE,
        "context": CONTEXT, "items": ITEMS}
out = Path(LANE, ".ufo/waves/round-55/spec-w1.json")
out.write_text(json.dumps(spec, indent=1) + "\n")
roles = {}
for it in ITEMS:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
attack = sum(roles.get(r, 0) for r in ("reviewer", "critic", "mutation-tester", "labrat"))
print("seats=%d attack=%d share=%.1f%%" % (len(ITEMS), attack, 100.0 * attack / len(ITEMS)))
print(json.dumps(roles, indent=0))
