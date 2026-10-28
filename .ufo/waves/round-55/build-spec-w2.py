#!/usr/bin/env python3
"""Build round-55 wave-2 spec (v1 band 32-64): fresh readers of the re-keyed section + attacks on C0."""
import json
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
BASE = "0a2010acd1e92e4e332774050825e21bcfc7e079"
FREEZE = "e2979f277138da503af27b263b783f626f109be4"
C0 = "9cf0146b94ddba12d454ebf7288ce6e5c5d535bb"
W = ".ufo/waves/round-55/w2"

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
tameshi round 55 (hyaku run 11; L1 TameshiR55), wave 2 — the falsify wave. Lane repo {LANE} (absolute paths only: seat tools start at the fleet root /home/vgpnk/Projects/shokunin). Base `{BASE}`; counter freeze `{FREEZE}` (7 amendments, all pre-control, all in `.ufo/evidence/round-55/freeze.json`); **content commit C0 `{C0}`** — wave 1 landed, this wave attacks it.

# What wave 1 and the L1 landed at C0 (attack all of it)
- **C1 calibration** (contract `.ufo/evidence/round-55/contract.json`): the lane's record must agree with the tree on ten routed defects of the round-54 spot-check. `SCORECARD.md` now carries a `## Round 55 - round-54 record corrections` section (ER-R54-1..10: old -> new, derived value, receipt) and the stale assertions were fixed in place. Counter: `python3 {LANE}/.ufo/evidence/round-55/c1/measure.py --lane LANE --rev {C0} --work <empty dir> --explain`. Base receipt: `total=10 premise=9/10 stale=4` (`.ufo/evidence/round-55/before/c1.stdout`).
- **C2 operability**: one stderr line, one exit class, nine documented allocating modes. `tools/repeat-control.py`, `tools/context-capture.py` and `tools/registry-check.py` now raise `ScratchRootUnusable` and print `tool: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)`; the seven `tools/registry.json` `scratch_root` cells, `corpus/knowledge/scratch-root-contract.md` (its `## One line, every mode` section) and the SKILL.md `## Standing rules` scratch bullet state it. Counter: `python3 {LANE}/.ufo/evidence/round-55/c2/measure.py --lane LANE --rev {C0} --work <empty dir> --explain`. Base receipt: `grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 docs=0/7 note=0/9 skill=0/1 total=21`.
- **One SKILL.md section drifted** by that edit (`## Standing rules`); three seats of this wave read it at C0 so the round can re-key its ledger entry.

# Reader discipline (only the three reader seats)
Read `## Standing rules` AT {C0} (the section's bytes at that revision, not the working tree). Write `{LANE}/{W}/<your-seat-name>.json` = `{{"heading": "## Standing rules", "cand": "{C0}", "section_sha256": "<sha of the section at that rev>", "findings": [...]}}`. Compute the sha with the frozen sectionizer `.ufo/evidence/round-18/measure.py` (`--repo`, `--rev`, its `sectionize`) - do not invent a hashing scheme. `findings` is a list of `{{"quote", "why"}}`; an empty list is a legitimate, valuable verdict for a clean section. Write the same facts in `<your-seat-name>.md` with the commands you ran and name every artifact you opened.

# Attack discipline (every non-reader seat)
Name what you attack, and put a runnable receipt in `{LANE}/{W}/<your-seat-name>.md` (command + output + verdict); fixtures belong under `{LANE}/{W}/<your-seat-name>-receipts/`. Never edit a lane production file, a frozen file (`.ufo/evidence/round-55/*`, `contract.json`, `freeze.json`) or the wave spec: work on `git clone --shared` copies at C0 in scratch. A finding without a command and its output is not a finding; an attack that finds nothing must show the sweep it ran.

# Bounds
- Read-only: the fleet root outside the lane, sibling lanes, `/home/vgpnk/Projects/shokuknow`, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`, `~/.omp/`. Write scope: ONLY `{LANE}/{W}/`.
- Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r55/<your-seat-name>` with `trap 'rm -rf -- "$S"' EXIT`; NEVER `rm -rf` the shared parent (a wave-1 seat did and destroyed peers' clones). `/tmp` only for files under 50 MB.
- Never run a mutating git/jj command in the lane. Fixtures: `D=$(mktemp -d)`, every git call names `-C "$D"`, `git -C "$D" rev-parse --show-toplevel` must equal `$D` before any commit there.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task - read `/home/vgpnk/.omp/agent/RULES.md` first (official channels, update-safety gate) and record tool/version/channel/reason in your report. **pacman transactions are PAUSED host-wide**: install via `uv tool`/`npx`/an official binary in `~/.local/bin`, or route around it.
- Every `Report:` trailer path is relative to {LANE} - write it at {LANE}/<that path>. Never message `agent://all`; message only your L1 (`TameshiR55`).
- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` must exit 0 (140 rows)."""

ITEMS = []


def add(name, role, axis, milestone, item):
    ITEMS.append({"name": name, "role": role, "axes": [axis], "milestone": milestone, "item": item})


READERS = {
 "01": ("anchors and counts",
        "Check every path, line anchor, count and cited note in the section against the tree at {c0}: does each `file:line` resolve, does each count match, does each cited corpus note exist and still say what the section says it says? The section's scratch bullet was rewritten by this round, so check it hardest."),
 "02": ("grammar vs code",
        "Check the section's scratch bullet against the three tools' code and the counter: the grammar it quotes must be the counter's frozen regex byte for byte, the nine modes must be the ones that allocate, and the five lazy modes must not allocate. Read `tools/repeat-control.py`, `tools/context-capture.py`, `tools/registry-check.py` call sites and `corpus/knowledge/scratch-root-contract.md`."),
 "03": ("executor sufficiency",
        "Judge the section as an executor with no lane context: can you carry out each rule from this text alone? Name the rule whose wording is ambiguous, unverifiable or stale, and the one a next round's editor could break without noticing. This is a sufficiency read, not a style review."),
}
for i, (angle, body) in READERS.items():
    add("T55W2Read" + i, "scribe", "calibration", "cold-read reader at C0 - " + angle,
        f"Read `## Standing rules` of `{LANE}/SKILL.md` AT {C0} (use `git -C {LANE} show {C0}:SKILL.md` and cut the section; never the working tree). Your angle: **{angle}**. "
        + body.format(c0=C0)
        + f" Write the reader JSON + MD per the wave context's Reader discipline (heading, cand {C0}, section_sha256 from the frozen round-18 sectionizer, findings list). A clean read with the sweep shown is a valuable verdict; an invented finding is not. Name every artifact you opened.")

add("T55W2RevCorrections", "reviewer", "calibration", "attack the corrections section",
    f"Take `SCORECARD.md` `## Round 55 - round-54 record corrections` at {C0} and check all ten entries byte-by-byte against the receipts they name (`git -C {LANE} show {C0}:.ufo/evidence/round-54/...`). For each: is the quoted old text what the file actually said at base `{BASE}`? is the corrected value what the receipt prints? is the receipt pointer right? Report a 10-row table with agree/disagree and the command. Any entry whose old text does not match base, or whose value the receipt contradicts, is a blocking finding for C1.")

add("T55W2RevToolDiffs", "reviewer", "operability", "attack the three tool diffs",
    f"Diff each of `tools/repeat-control.py`, `tools/context-capture.py`, `tools/registry-check.py` between `{BASE}` and {C0} (`git -C {LANE} diff {BASE} {C0} -- <path>`). For each hunk: does the new handler cover every path that can raise the scratch refusal (selftest, `--snapshot`, `--check`, `--rev`, the run path)? Does any change alter an exit code other than the scratch refusal? Is the exception ever swallowed by a broader handler that prints the raw type? Run `TMPDIR=/nonexistent/x` and `TMPDIR=<good>` against each tool's documented modes and report the pairs. A mode that still prints on stdout, or leaks `RuntimeError`, is the finding.")

add("T55W2RevDocsArms", "reviewer", "operability", "attack the docs arms",
    f"At {C0}, check the three documentation surfaces the C2 counter reads: (1) the seven `scratch_root` cells in `tools/registry.json` - does each describe ITS tool (selftest vs selftest,--rev) and the frozen grammar, and is the wording true of the code? (2) `corpus/knowledge/scratch-root-contract.md` `## One line, every mode` - does it name all nine allocating modes, is the grammar quote byte-identical to the counter's regex, and are the five lazy modes really lazy? (3) the SKILL.md bullet. Report each claim hold/overreach/wrong with the code line or receipt. Also check the registry diff for collateral changes (parsed rows other than the seven cells).")

add("T55W2CritNinthMode", "critic", "operability", "falsify the ninth-mode arm",
    f"`registry-check --rev` was added as the ninth allocating mode after wave 1 found it. Verify the claim is now true and the arm is real: at {BASE} show that mode prints `REGISTRY_CHECK: could-not-evaluate (...)` on stdout with empty stderr under an unusable TMPDIR; at {C0} show the grammar line on stderr, exit 2; then show the tool still works under a good TMPDIR (`--rev {C0}` succeeds, however long it takes - cap it and report the time). Then attack the arm's design: it is grammar-only (no empty/usable run) - is that disclosed in the note, and can a regression in its usable path pass unseen? Report with receipts.")

add("T55W2CritFreeze2", "critic", "calibration", "attack freeze F2",
    f"Re-derive every sha256 in `.ufo/evidence/round-55/freeze.json` at {FREEZE}, check the manifest covers every `contract.json` `frozen_paths` entry (and not itself), and confirm `deciding-run.sh`'s FROZEN list equals the contract's. Then check the seven amendments are each (a) before any control receipt, (b) plumbing-only or disclosed as a surface change (amendment 6 changes denominators), and (c) reproduced by a receipt. Report: is {FREEZE} a sound freeze pointer, and would `FROZEN_UNCHANGED=1` hold for a REV that descends from it?")

add("T55W2MutC1", "mutation-tester", "calibration", "mutate C1 at C0",
    f"Mutation-test the frozen C1 counter at {C0} in scratch copies: at least 6 single-edit mutants - drop one class's stale scan; replace a derived value with a literal; treat `premise=false` as ok; read the corrections section without trimming at the next heading; count reader files from the working tree; make the span scan case-insensitive on the wrong token. Score every mutant at {C0} (it must still be KILLED where the mutant would let a defect through) and report KILLED/SURVIVED with verdict lines. A survivor is a finding.")

add("T55W2MutC2", "mutation-tester", "operability", "mutate C2 at C0",
    f"Mutation-test the frozen C2 counter at {C0}: at least 6 mutants - accept rc 1 on the grammar arm; drop the `RuntimeError` check; match the grammar on stdout+stderr; make the note arm count labels without the note; make the docs arm accept any cell; shrink the allocating list to eight. Score each at {C0} and on a tree where the defect exists (revert one tool line in a scratch clone). Report KILLED/SURVIVED; say which arm each mutant should kill and whether it did.")

add("T55W2MutTools", "mutation-tester", "operability", "mutate the three tools",
    f"In a scratch clone at {C0}, revert each tool's grammar line one at a time (repeat-control, context-capture, registry-check --rev) and score the C2 counter: each must lose exactly one grammar mode and nothing else. Then mutate the message (drop the value, drop the class token, change 'stderr' to stdout) and show which arm catches each. Report the verdict lines side by side.")

add("T55W2RevLessonAccuracy", "reviewer", "calibration", "attack the lesson",
    f"Read `corpus/lessons/round-55.md` at {C0}: every number, path and claim. Check (a) the Gate's word counts and locators against the snapshots, (b) the Mistakes entries - is each a real mistake with a fix that can fail, and does the second one (a wrapped marker) describe what the counter actually did, (c) the R54 dispositions against the corrections section, (d) the `cannot_see` list against the code. Report each item with a command; a wrong number is a finding even when the round still passes.")

add("T55W2RevSources2", "reviewer", "coverage", "attack the source rows",
    f"At {C0}: re-open `https://www.gnu.org/prep/standards/html_node/Errors.html` yourself and check S280's quote, locator, word count and the `teaches` cell (the row was rewritten after a wave-1 finding that an earlier clause was unsourced). Check the sysexits refusal in the lesson Gate: is refusing it (duplicate of S090) the right call under CORPUS.md rule 2, and is the flip condition honest? Then run the census and report rows/warnings. Report per item: hold / overreach / wrong.")

add("T55W2SentScope2", "sentinel", "calibration", "scope audit of C0",
    f"Audit the C0 diff `{BASE}..{C0}`: list every changed path, check none is a frozen file, a sibling repo, `.ufo/state/`, or a path outside the lane; check `tools/registry.json`'s semantic diff is only the seven cells (not a re-serialization that changes a row); check the three tools' diffs touch only the scratch-refusal and the `--rev` handler; and check `git -C {LANE} status --porcelain` for stray writes. Report the audit with commands. Also verify no file under `.ufo/waves/round-55/` was edited after the wave-1 dispatch marker.")

add("T55W2SentConfig2", "sentinel", "calibration", "the config.yml incident, re-verified",
    f"Verify the R54.8 record now at {C0}: (1) confirm the operator turn exists (`~/.omp/agent/history.db`, session of round 54 - read-only) and that it reached the seat's transcript after it yielded; (2) confirm `~/.omp/agent/config.yml` reads `scout: \"@m_grok\"` and that no round-55 process wrote to `~/.omp/`; (3) read the SUPERSEDED block in `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` and the ER-R54-8 entry - do both state the incident honestly (instruction real, write still wrong)? Report with receipts. A false accusation in the permanent record is the finding.")

add("T55W2CritClaimShape2", "critic", "calibration", "claim shape at C0",
    f"Judge at {C0}: are C1 and C2 causally separable (each verifiable with the other unlanded - test by reverting one side in a scratch clone)? Does either harm an axis - does the C1 record edit damage freshness, does the C2 SKILL.md edit cost cold-read credit the round must repay? Is at least one claim on calibration (8, the lowest non-retired axis) and is the axis named by the surface, not the number? Is each target one a do-nothing control cannot reach (score a do-nothing clone)? Report a verdict per question with evidence.")

add("T55W2RevGateResidual", "reviewer", "calibration", "the deciding gate's residuals",
    f"Reproduce the residual wave-1 found and check for others, at {FREEZE}: `deciding-run.sh` verifies a control receipt's existence, blob-ness, size and commit order but never compares the `rev=` a `CTL` line names with the revision under test; can a stale receipt open the gate? Also test: `CONTROLS_A: 0/0` satisfies its regex; `controls-*.exit` content is never read; a second invocation with a different OUTDIR passes; the verdict grep reads the working tree. For each: fixture, command, output, and whether it is blocking for this round's decision. Do not edit the script.")

add("T55W2ScoutColdread", "scout", "calibration", "cold-read drift at C0",
    f"Measure the cold-read floor at base `{BASE}` and at {C0} with `.ufo/evidence/round-21/coldread/measure.py` and the round-48 precheck (`bash .ufo/evidence/round-48/quality/coldread-precheck.sh {LANE} {BASE} {C0}`). Report: credited counts at both, the exact headings that lost credit, and for the drifted section(s) the inputs the credit rule names. Then state precisely what the three wave-2 readers must bind for the floor to return to 64/64. This is the re-key plan's evidence.")

add("T55W2RevBaseReceipts", "reviewer", "calibration", "are the base receipts reproducible",
    f"Reproduce both base receipts from the frozen bytes at {FREEZE} in fresh empty work dirs: `python3` the counters extracted from `{FREEZE}` (not the working tree) against `--rev {BASE}`, and `cmp` the verdict lines with `.ufo/evidence/round-55/before/c1.stdout` / `c2.stdout`. Report every differing byte region (paths and timings in c2 are expected; a count is not). Then state whether the round's `before` values are reproducible with the frozen bytes - the round-54 closure's own complaint about round 53 was exactly this.")

add("T55W2RevER548", "critic", "calibration", "attack the R54.8 rewrite",
    f"Scrutinise the ER-R54-8 rewrite at {C0} (SCORECARD, lesson, seat file): it withdraws the word 'fabricated' while keeping the incident. Is the distinction it draws (the turn was real; the write was still against the operator-owned rule and arrived after the seat yielded) supported by the evidence, or does it now understate the incident? Check the turn's timestamp against the seat's yield time, the round-54 prompt's ownership rule, and the current alias value. Report a verdict: honest / overstates / understates, with receipts.")

add("T55W2RevScorecardNums", "reviewer", "calibration", "numbers in the round-55 block",
    f"At {C0}, take every number in the `## Round 55 - ...` SCORECARD block and the LOG entry and re-derive it: the base verdict lines, the wave-1 seat count and attack share (from `.ufo/waves/round-55/w1-registry.json`), the row count, the freeze/amendment count, the `before` values. Report a table value -> derived -> agree/disagree with the command. This is the calibration claim's own standard applied to its own record.")

add("T55W2MutReceipts", "mutation-tester", "calibration", "mutate the receipts",
    f"In a scratch clone at {C0}, flip one derived value in the corrections section (e.g. `total=13` -> `total=12`), remove one ER entry, and move one old->new pair above the `##` heading. Score the frozen C1 counter after each: every mutation must be caught, and the third must show why position matters. Report the three verdict lines and name any mutation the counter misses (that is a finding about the counter, not about you).")

add("T55W2RevNoteNine", "reviewer", "operability", "nine modes vs the code",
    f"Verify the note's claim that exactly nine modes allocate scratch: for each of the nine, cite the code line that allocates on that path (`strict_scratch_root()` call site and the mode that reaches it), and for each of the five lazy modes cite why its path cannot reach an allocation. Then look for a tenth documented mode (usage text, docstrings, registry rows) - the round already found one the mode table missed, so sweep hard. Report the table and any tenth mode with its line.")

add("T55W2Connector3", "connector", "operability", "is the grammar a fleet pattern",
    f"Sibling scan (read-only): do kumitate's, kagi's, tsukuroi's or mado's gates already emit a `could-not-evaluate` class line or a uniform error grammar? Report `path:line` evidence and state whether tameshi's grammar is (a) a lane invention, (b) a pattern one other lane holds, or (c) general by PROVINCE's two-lane rule. If (b)/(c), name the sibling's line and the differences; the round must not claim generality it has not earned.")

add("T55W2SimplDiff", "simplifier", "operability", "is the C0 diff minimal",
    f"Measure the C0 diff and find waste: `git -C {LANE} diff --stat {BASE} {C0}`. The registry file shows ~1275/1026 lines for seven changed cells (a whole-file re-serialization with the same parsed rows) - decide whether that must be reduced to seven lines before landing, and if so produce the minimal patch on a scratch clone and prove the parsed rows are identical and C2's docs arm still reads 7/7. Then look for any other avoidable churn (comment rewrites, whitespace) and name it.")

add("T55W2CritCalibrationMove", "critic", "calibration", "is C1 a real calibration move",
    f"Argue both ways, then decide: C1 fixes ten record defects a closure already found. Is that a calibration move (the lane's self-assessment reconciled to the tree, with a counter that would catch the same class again), or bookkeeping that a do-nothing control could have produced? Test the second arm: does the counter's stale/derived structure generalise to a NEW defect of the same class (plant one in a scratch clone at {C0} - a wrong number with a plausible receipt - and see whether the counter catches it)? Report the verdict with the receipt.")

add("T55W2RevWaveArtifacts", "reviewer", "calibration", "wave-1 artifact integrity",
    f"Audit the wave-1 deliverables under `.ufo/waves/round-55/w1/` at {C0}: how many seat reports exist vs the 75 dispatched; which seats wrote nothing; the T55W1Er10 collision (its JSON was overwritten twice by peer seats and restored from a session log - is the surviving artifact the R54.10 draft, and does it parse?); whether any seat report claims work whose files do not exist. Report the counts, the dead seats and the collision's current state. Do not fix anything.")

add("T55W2RevMistakes", "reviewer", "calibration", "are the mined mistakes real",
    f"Check the two `## Mistakes` entries in `corpus/lessons/round-55.md` at {C0}: for each, is the evidence pointer real and does it support the class claimed? For the first (a control scored before the work it certifies) verify the receipt's own line; for the second (a wrapped marker) verify that the counter as frozen at {FREEZE} really did score 0/1 on a correct edit before amendment 2, by running the pre-amendment bytes (`git show {FREEZE}^:.ufo/evidence/round-55/c2/measure.py` if it exists, else the freeze-commit parent). Report whether each fix can fail (a falsifier), or that the entry is prose.")

add("T55W2RevNoHarm", "reviewer", "freshness", "no-harm at C0",
    f"Run `bash {LANE}/.ufo/evidence/round-55/no-harm.sh {LANE} {C0}` and report every line. Confirm 15 `ok`, zero `RED`, and explain each monitor's meaning in one clause. If a monitor is RED, decide whether it is a real harm, a stale monitor or a defect in the monitor (a monitor that cannot fail is dead weight) and report which - do not fix it. Then run the seven tools' own self-tests at {C0} in a scratch clone and report the exit codes.")

add("T55W2CritC2Scope", "critic", "operability", "C2's denominator honesty",
    f"Attack the C2 claim's wording against what it measures: the claim says every documented allocating mode carries the class; the counter runs nine on the unusable arm but only eight of them (plus five lazy) on the empty/usable arms, and `registry-check --rev`'s usable path is covered only by the tool's own self-test. Is that disclosed where a reader meets it (contract, note, SKILL, report plan)? Build the cheapest tree where `registry-check --rev` works under a good TMPDIR but fails under an empty one (empty is 'unset', so a correct tool must work) and show whether any arm catches it. Report the gap precisely.")

add("T55W2ExecFloorRekeyProbe", "executor", "calibration", "probe the re-key before the L1 binds it",
    f"Take the three wave-2 reader JSONs (`{LANE}/{W}/T55W2Read0*.json`) if they exist when you start (else wait/read them; they are written in this same wave) and validate each against the round-21 credit code: heading equals `## Standing rules`, `cand` equals {C0}, `section_sha256` equals the section computed by the frozen round-18 `sectionize` at {C0}, `findings` a list. Then dry-run a bind into a scratch copy of `.ufo/evidence/round-21/coldread/ledger.json` (adapt the round-54 binder in scratch) and report whether the section credits and the round-48 precheck returns to 64/64. Report the exact commands the L1 should run, and any reader whose deliverable cannot be bound.")

add("T55W2RevRound54Wording", "reviewer", "calibration", "round-54 lesson after the edits",
    f"Read `corpus/lessons/round-54.md` at {C0} in full against its own receipts: the file was edited this round at three places (the R53.1 fix paragraph, the R53.9 area, the staged count). For each edit: does the new sentence agree with the receipts, and did dropping the tokens `rekeyed=7/7` / `positive control` from that paragraph lose any information a reader needs? Report per edit. Then check the file for any remaining falsehood the round did not touch.")

add("T55W2SentStrayWrites", "sentinel", "calibration", "stray writes and misroot",
    f"Sweep the fleet root for round-55 misroots: `git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec) - every untracked file whose content names tameshi round 55 but sits outside `{LANE}` is a candidate; also check `/tmp` for `tameshi-r55` scratch. Report each candidate with its first line, and say whether it must be moved into the lane (byte-exact `cmp`) or left alone (other lanes' files, `.scratch/`, `.ufo/state/`). Do not move anything; the L1 does.")

add("T55W2CritDoNothing", "critic", "calibration", "the do-nothing controls",
    f"Score the do-nothing tree for both claims at {BASE} with the frozen bytes and check each control receipt in `.ufo/evidence/round-55/control/` (phase A is running while you work; if `controls-a.stdout` exists read it, else run the two counters yourself at {BASE}). Verify: CTL_0 is false for both; CTL_SKIP_c1 (a corrections block with values but no fixes) is false; CTL_FAB_c1 (invented values) is false; CTL_SKIP_c2 (docs only) is false. If any control prints true, the counter or target is wrong - report which and why. Then state whether each claim's target is beyond a do-nothing control.")

add("T55W2RevHitlChecklist", "reviewer", "calibration", "the report's claim table preview",
    f"Pre-check what the round will have to claim. Read the contract's two claims and the counters' current verdicts at {C0} and at {BASE}; for each claim write the exact before->after line a reader could re-derive, the counting command, and the one value that would falsify it. Then check the round has the receipts it needs (base receipts, controls, deciding run - the last two may not exist yet: say so). Report the table and any claim that cannot be stated in one concrete value.")

add("T55W2RevengerTenth", "revenger", "operability", "why the ninth mode was missed",
    f"Reverse-engineer how `registry-check --rev` escaped the round-55 mode table and round 54's check: read the counter's original table, `tools/registry.json`, `SKILL.md`'s mention of `--rev`, and `tools/registry-check.py`'s usage/docstring. State the mechanism (which surface would have shown it: registry rows, usage text, a call-site sweep) and the minimal rule that would have caught it - a grep a next round can run in one line. Then test that rule against the seven tools and report what else it would catch.")

ITEMS = ITEMS[:34]
roles = {}
for it in ITEMS:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
attack = sum(roles.get(r, 0) for r in ("reviewer", "critic", "mutation-tester", "labrat"))
print("seats=%d attack=%d share=%.1f%%" % (len(ITEMS), attack, 100.0 * attack / len(ITEMS)))
print(json.dumps(roles))
Path(LANE, ".ufo/waves/round-55/spec-w2.json").write_text(json.dumps(
    {"wave": "round-55-w2", "reportDir": W, "template": TEMPLATE, "context": CONTEXT, "items": ITEMS},
    indent=1) + "\n")
