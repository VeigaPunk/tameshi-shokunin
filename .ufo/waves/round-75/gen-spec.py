#!/usr/bin/env python3
"""Generate the round-75 wave spec (12 seats). Lane-local evidence; the wave
validator is the authority on shape."""
import json

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
SCRATCH = "$HYAKU_SCRATCH/tameshi-r75"
DPREFIX = ("/skill:godspeed\n\n"
           "You are a Godspeed-enabled subagent.\n\n"
           "1. **Name the axes.**\n"
           "2. **Iterate cheap, in parallel.**\n"
           "3. **Keep moves that improve any axis and harm none.**\n"
           "4. **Don't aim — let the frontier walk itself.**\n\n"
           "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool "
           "calls concurrently in large batches. Do not serialize what can "
           "run in parallel. Do not output philosophical reasoning or verbose "
           "plans. Act directly via tool calls.\n\n")

COMMON = """
HARD BOUNDS (read first):
- You are a LEAF seat. Do not spawn subagents, do not start background services.
- READ-ONLY on the lane repo except your own report file (and your same-named
  subdirectory of candidates/receipts) under
  {lane}/.ufo/waves/round-75/w1/ . Never run git/jj mutating commands
  (add/commit/stash/checkout/reset/pull/push, jj commit/new/describe/squash/
  rebase/abandon/bookmark/undo) anywhere, never edit tracked files, never
  touch /home/vgpnk/Projects/shokunin (fleet repo), /home/vgpnk/Projects/shokuknow,
  or any sibling lane repo. Read them if your item says so.
- Scratch root: {scratch}/<your-seat-name>/ , created with mkdir -p and REMOVED
  before you finish (trap 'rm -rf -- "$S"' EXIT or a finally block). /tmp is for
  files under 50 MB only. Every clone is `git clone --shared` or a git
  archive/worktree copy; no full mirror of the lane.
- A fixture git repo is created only as D=$(mktemp -d) && git -C "$D" init -q
  and every later git call names -C "$D"; verify
  `git -C "$D" rev-parse --show-toplevel` equals $D before any commit. Never
  commit with a throwaway identity in a real repo.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade
  tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first
  (official channels only; record tool/version/channel/reason in your report).
  pacman guard (orchestrator ruling 2026-10-20): ALL pacman transactions are
  PAUSED host-wide; install via `uv tool` / `npx` / an official binary into
  ~/.local/bin, or file the need in your report. Never -Sy/-Syu/-U/-R.
- Honesty: an unrun check has not passed. Do not fabricate output; paste the
  exact command and its exact output. Mark inference as [INFERENCE].
- Every `Report:` trailer path the harness prints is relative to {lane} —
  write your report at {lane}/<that path>, i.e.
  {lane}/.ufo/waves/round-75/w1/<your-seat-name>.md .
- Your final message must be a compact findings summary: commands run, exact
  verdict lines, files written, and what you could NOT establish.
"""


def item(name, role, text):
    text = text.replace("{lane}", LANE).replace("{scratch}", SCRATCH)
    assert "{lane}" not in text and "{scratch}" not in text, name
    assert "{" + "lane" + "}" not in text
    return {"name": name, "role": role,
            "axes": ["verification-fixture-craft"],
            "item": DPREFIX + text.strip() + "\n"}


CTX = """# Goal and authority
Tameshi lane (verification-fixture craft), round 75, wave w1. The L1 (agent id
`TameshiR75`) is the ONLY coordinator, writer, claim judge and committer. Two
claims are frozen BEFORE any of this wave's data in
{lane}/plans/round-75.plan.md — read it first; it carries the predicates,
counting commands, kill rules and controls. Seat outputs are evidence for the
L1's verdict, never verdicts themselves. Base revision
21ef81e99966198cf8cdb2c6d8e56aa3c482da56 = origin/master (the admitted
round-74 non-author closure). Your item's candidates/receipts go under your own
report subdirectory; the L1 integrates them into the lane.

R75-C1 (operability, sourced on re-opened S006) — `{lane}/tools/wave-reconcile.py`:
add three frozen selftest arms so the three mutants measured as survivors at
base die on their named arms — `M-C` (printed integer bound to the whole record
instead of the row's span), and the selective `_record_claim` bypass on
roles and on attack_share. Target after-state: `WAVE_RECONCILE_SELFTEST: 18/18
pass` and a committed six-defect runner spec that kills all six (three round-74
defects plus three new) on their named arms.

R75-C2 (calibration) — `{lane}/tools/selfstate-freshness.py` +
`tools/selfstate-freshness.json`: 17 declared rows (16 live SCORECARD
`## Capabilities` figures + 1 frozen historical statement) whose quoted figure
must equal the instrument's own printed figure at the measured revision.
Target after-state at the landing tip: `SELFSTATE: rows=17 match=16 stale=1
unexpected=0` exit 0; base state is `unexpected=7` exit 1. The seven stale live
figures and their repairs are named in the plan.

# Fleet context
The fleet runs other lanes concurrently; their trees are read-only to you.
{common}
""".format(lane=LANE, scratch=SCRATCH,
           common=COMMON.format(lane=LANE, scratch=SCRATCH))

ITEMS = [
    item("T75W1E1", "executor", """
TARGET: the R75-C1 candidate — arms 16/17/18 and the six-defect mutant spec,
built and measured in your scratch/report dir. Do NOT edit the lane.
Repo {lane}; base 21ef81e9 (`git -C {lane} show 21ef81e9:tools/wave-reconcile.py`,
sha256 97bb9272afb6c243cf7fb2dfde7bd34b90b4bcd769974d112ca574fccafd21fa).
Read `plans/round-75.plan.md` R75-C1 first: it freezes the three arms and the
kill rule.
1. Add three arms to the 15-arm tool (`SELFTEST_ARMS` must become 18):
   - `arm16-printed-span-not-record`: a seats row whose record blob is
     `- The wave: 11 reports; 1 seat filed late.\\n` (the span `11 reports` is
     present; a delimited `1` exists OUTSIDE the span), span `11 reports`,
     printed 1. The arm must expect SetupError prefix `printed-not-in-span`
     (use the existing `arm_raises` helper). Under the M-C mutant — which binds
     the printed value to the whole record with the single edit
     `delimited(printed, rec['span'])` -> `delimited(printed, _)` (the `_` is
     the decoded record text `_record_span` returned) — the same input reaches
     the seat comparison and returns `drift`, so the arm must FAIL under M-C.
   - `arm17-record-claim-live-on-roles`: a roles row whose record span
     `13 seats` is ABSENT from the fixture record, declaration
     `spec-items` at `spec.json`. Expect SetupError `span-not-in-record`
     (`arm_raises`). Under a mutant that deletes
     `_record_claim(row, readers)` from the roles branch only, the row measures
     `meet` instead of refusing, so the arm must FAIL under that mutant.
   - `arm18-record-claim-live-on-attack-share`: the same for the attack_share
     branch: record span `13 seats` absent, `named` = reviewer/critic/
     mutation-tester, floor_pct 25. Expect SetupError `span-not-in-record`.
2. Build `tools/wave-reconcile.py` candidate in your dir; run
   `python3 -I -X utf8 <candidate> --selftest` -> paste the last line (expect
   18/18) and the exact per-arm lines for 16/17/18.
3. Extend the mutant spec: copy the three existing defects from
   `tools/wave-reconcile-mutants.spec` and append
   `mc-record-bound` (the single edit above),
   `roles-bypass` (delete `_record_claim(row, readers)` from the roles branch;
   use enough context in @old/@new for count==1),
   `attack-bypass` (same for the attack_share branch).
   Write `<your-dir>/wave-reconcile-mutants-r75.spec`.
4. Run the battery against a COPY of the lane's `tools/mutate-and-run.sh`
   (copy it into your scratch; never modify the lane):
   `bash <copy> --target <candidate> --defects <spec> --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --workdir <scratch> --label wave-reconcile-arms-r75`
   Paste `CONTROL:`, every `DEFECT ... KILLED`, the `| SELFTEST armNN ... FAIL`
   lines, `MUTATE_RESTORE:` and `MUTATE: DONE`. Verify each new defect dies on
   ITS named arm only and that arms 1-15 keep their `ok` lines (compare the
   full selftest transcripts pristine vs candidate).
5. Write `<your-dir>/wave-reconcile-r75.py`, the spec, and the receipts; the
   L1 copies them into the lane. Report the exact old/new strings of the three
   spec defects.
"""),

    item("T75W1E2", "executor", """
TARGET: the R75-C2 instrument candidate — `tools/selfstate-freshness.py` +
`tools/selfstate-freshness.json` — built and measured in your dir. Do NOT edit
the lane. Read `plans/round-75.plan.md` R75-C2 first.
Design (the L1's frozen predicate; implement it exactly):
- `--repo` (REQUIRED; never derive the repo root from `__file__` — that was
  the pre-freeze control prototype's defect), `--doc` (default
  `SCORECARD.md`), `--doc-rev` (optional: read the doc from git objects at
  that rev; omit to read the worktree), `--manifest` (default
  `tools/selfstate-freshness.json`), `--selftest`.
- Row schema: `{id, mode: "capability"|"span", capability|span, figure,
  instrument: {path, rev, argv}, expect: "match"|"stale"}`. `capability` rows
  locate the table row in the `## Capabilities` section whose FIRST CELL is
  exactly the name (stop at the next `## `); `span` rows bind a literal byte
  span in the doc. Both use `figure` (a regex) as the only figure extractor.
- Every instrument is extracted with `git cat-file blob <rev>:<path>` into a
  temp dir and run `python3 -I -X utf8 <extracted> <argv...>` with `cwd=repo`
  and `TMPDIR` honoured; the SAME `figure` regex extracts the measured token
  from its stdout. `match` iff doc token == instrument token.
- `expect` is the declared state; `unexpected` counts rows whose measured
  state differs. Per row print
  `SELFSTATE_ROW <id> capability=<name> expect=<e> measured=<m> ok|UNEXPECTED`
  (also print the measured figure token); summary
  `SELFSTATE: rows=N match=M stale=S unexpected=U`; exit 0 iff U==0, 1 on
  unexpected, 2 on setup failure. Setup refusals (exit 2, before any row
  effect, no partial summary): zero rows, unknown mode, duplicate id, an
  unresolvable instrument rev/blob, a declared capability absent from the
  table, or a figure regex that matches nothing in the doc row.
- `--selftest`: hermetic fixture reader (no git, no subprocess of lane tools);
  arms for match, stale measured, frozen-span stale, absent capability
  refused, absent figure refused, zero rows refused, unknown expect refused,
  unknown mode refused, and (if cheap) an instrument whose output lacks the
  figure (setup refusal, not a match). Print
  `SELFSTATE_SELFTEST: n/N pass`; exit 0 only if all pass and the arm count is
  the declared constant.
- Manifest: 16 live `capability` rows, one per figure in the plan's list
  (commit-bind selftest, quoted-line selftest, arm-liveness selftest,
  arm-liveness standing rows, anchor-drift selftest, anchor-drift rows,
  count-recheck selftest, count-recheck rows, pointer selftest, pointer rows,
  figure selftest, figure rows, receipt-exists selftest, rekey-cost selftest,
  additivity selftest, additivity rows; the exact names and regexes are in
  `.ufo/evidence/round-75/selfstate-control-scan.py`) with
  `expect: "match"`, plus ONE frozen `span` row:
  id `r74-frozen-addr-six`, `span` = the round-74 SCORECARD block's
  `ADDRANGE: rows=6 met=6 unexpected=0`, figure regex
  `ADDRANGE: rows=\\d+ met=\\d+ unexpected=\\d+`, instrument =
  `tools/additivity-range.py` with
  `argv ["--repo", ".", "--manifest", "tools/additivity-range.json"]`,
  `expect: "stale"`. Pin every `instrument.rev` to
  `21ef81e99966198cf8cdb2c6d8e56aa3c482da56`.
5. Measure: run the candidate at `--doc-rev 21ef81e9` (expect
   `SELFSTATE: rows=17 match=9 stale=8 unexpected=7` exit 1) and at the
   worktree; run `--selftest`. Paste all three last lines. Save the candidate
   tool + manifest + a couple of receipts in your dir.
"""),

    item("T75W1E3", "executor", """
TARGET: the seven stale SCORECARD capability figures — independently
re-derived, and the exact repair patch. READ-ONLY on the lane; write only in
your dir. Read `plans/round-75.plan.md` R75-C2.
1. Read `{lane}/SCORECARD.md` `## Capabilities`. For each of the seven stale
   figures the plan names (commit-bind selftest, quoted-line selftest,
   arm-liveness selftest, arm-liveness standing rows, anchor-drift rows,
   line-pointer rows, additivity rows), write the EXACT old substring and the
   EXACT new substring as they occur in that row (paste both; count
   occurrences with `grep -c -F` to prove each is unique in SCORECARD.md).
2. Run each instrument yourself (the commands are in the capability rows /
   `.ufo/evidence/round-75/selfstate-control-scan.py`) and paste its exact
   verdict line; the new substring must be the instrument's token.
3. Sweep the WHOLE capability table for any other stale figure the plan's
   seven-row list misses (`SELFTEST:` and `rows=` tokens in every row, each
   compared with its instrument), and report the extra set (or the sweep
   command and its empty diff). A missed row is a real finding: say so.
4. Write `<your-dir>/scard-repairs.json` with rows
   `{capability, old, new, old_count, instrument_argv, measured_line}` and
   `<your-dir>/apply-repairs.py` (a deterministic applier asserting count==1
   per replacement, `--check` mode printing what it would do). Do not run the
   applier against the lane. Report the JSON path and every measured line.
"""),

    item("T75W1E4", "executor", """
TARGET: the frontier source — a fresh open of the held shmutant README (S006)
and the shipping evidence the lesson's Gate needs.
1. Fetch the document fresh this round:
   `curl -sS -D <dir>/headers.txt -o <dir>/readme.md https://raw.githubusercontent.com/BWBama85/shmutant/master/README.md`
   (fallback `/main/`), paste the HTTP status line, the `date`/`etag` headers,
   `wc -c` and `sha256sum`. Check `grep -ic 'set-cookie' headers.txt` -> 0 and
   that no header value carries a credential (a `Vary:` header naming
   `Authorization` is NOT a credential).
2. Locate three quotes verbatim (grep -n), give each line span and a
   whitespace-token count (all <=25):
   (a) the witness definition in §The three verdicts ("the assertion that
       must fail ..."),
   (b) the `killed` row ("The suite went red **on its witness** ..."),
   (c) the `accidental` row ("The suite went red, but not on its witness ...").
3. Held-page dedupe sweep: `grep -c 'BWBama85/shmutant' {lane}/corpus/SOURCES.md`
   (expect 1, the S006 row) and `grep -c 'shmutant'`; confirm no OTHER row holds
   the same URL, and quote S006's anchor cell as committed.
4. Backlog measurement (considerthese 2026-10-28 proposal 4, mining evidence):
   count the staged knowledge files under
   `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/*.md` and how many
   of those exact repo-relative paths already exist under
   `{lane}/corpus/knowledge/`; give both numbers with the commands.
5. Save the snapshot + headers in your dir; report every number with its
   command. Do not edit the lane or any tracked file.
"""),

    item("T75W1S1", "scribe", """
TARGET: the round-75 record drafts, derived from the frozen plan and the
pre-data receipts (not from the other seats, which run in parallel). Write
only in your dir; the L1 lands the prose.
Read `plans/round-75.plan.md`, `.ufo/evidence/round-75/base-measure-c1.txt`,
`base-measure-c2.txt`, `selfstate-control-scan.py`, `controls-c75.txt`, and
`corpus/QUALITY.md` tail (criteria 120-124) + `corpus/lessons/round-74.md`
`## Gate` for style. Draft:
1. `<your-dir>/lesson-round-75.md` — front section with round shape and base;
   `## Gate` with: S006 re-open (URL, access date, the three located quotes
   with line spans/word counts — take them from
   `.ufo/evidence/round-75/sources/s006-shmutant-readme.md`, verify each by
   grep yourself), ADMIT the re-open, REJECT a new shmutant row (same URL,
   within-scope duplicate, flip condition); the S006 `used-by` old -> new
   string; census before/after placeholders marked so the L1 fills the end
   count. `## Claims` with R75-C1 and R75-C2 before/after and their counting
   commands. `## Mistakes` with two rows in the required shape (class ·
   evidence pointer · captured-by · fix): (i) stale live capability figures
   (class `number-drift`/`stale-premise`; evidence
   `corpus/lessons/round-74-verifier-spotcheck.md` §6 item 3 +
   `.ufo/evidence/round-75/base-measure-c2.txt`; captured-by `none`; fix =
   the R75-C2 instrument + a new QUALITY criterion); (ii) the pre-freeze
   control prototype derived its repo root from `__file__` and measured
   nothing on its first run (class `reference-drift`; captured-by the
   instrument's required `--repo`; fix = explicit `--repo`, no derivation).
2. `<your-dir>/quality-criterion.md` — ONE new QUALITY.md criterion (next free
   number; check the tail) stating: a live capability row's printed figure is
   either the instrument's CURRENT token or is explicitly labelled historical
   and pinned to the receipt that carries it; a figure no instrument prints is
   a stale premise. Cite the round-75 lesson as its producing lesson, name the
   falsifier (`tools/selfstate-freshness.py --doc-rev <tip>` -> `unexpected=0`),
   and follow the existing row format exactly.
3. `<your-dir>/sources-round75-note.md` — the SOURCES.md `Round 75:` note line
   (no new row; S006 re-open, used-by old -> new, snapshot path/sha256, census
   numbers) in the exact style of the existing `Round 74:` note.
4. `<your-dir>/scorecard-round75.md` — the SCORECARD round-75 block in the
   round-74 style: declaration commit, claim table (verdict column left for
   the L1), no-harm line, carries.
Do not claim any after-state you have not measured; mark the L1's fill points
explicitly.
"""),

    item("T75W1SC1", "scout", """
TARGET: per-surface reconnaissance for the landing plan. READ-ONLY. Read
`plans/round-75.plan.md` and `corpus/lessons/round-74-verifier-spotcheck.md`
§6 first.
1. Cold-read monitor: find the command that prints `credited=64/64` for this
   lane at base 21ef81e9 (round-74 receipts use
   `tools/coldread-precheck-portable.py`; read `.ufo/evidence/round-74/
   live-green4-r74.out` and the tool's usage) and RUN it at the worktree
   (TMPDIR under your scratch). Paste `credited=` and `probe_mismatches=`.
2. Rekey planning: run `python3 -I tools/rekey-cost.py --edit SCORECARD.md
   --edit LOG.md --edit corpus/SOURCES.md --edit corpus/QUALITY.md` and list
   the at-risk SKILL.md section headings from its output. Compare with
   `.ufo/evidence/round-75/rekey-cost-r75.txt`.
3. Registry state: `python3 -I tools/registry-check.py` at the worktree
   (allow up to ~6 min), report `REGISTRY_CHECK:` and name the two rows not
   `held` (the summary the L1 saw was `held=55/57 superseded=7`), and whether
   the round-74 instruments' row fields the closure called missing (verdict
   map, pinned-value path, write scope, owner) exist.
4. Carried-items census: from the round-74 closure §6 and `corpus/lessons/
   round-74.md`'s carry list, produce a table of each item with its current
   state at base (open/paid/partial) and the exact evidence command. Include
   the SCORECARD EOL disclosure (D1), the wrong-revision cold-read pointer
   (D2), the stale live counters (D3), the registry home (D4), the S294
   used-by old->new (D5), the r73 items (D6), `M-C`, the selective bypass, the
   echo stub, the six older instruments' registry rows.
5. Confirm the exact SCORECARD line numbers of the seven repair cells at
   base (`grep -n` for each old substring) so the L1's patch applies cleanly.
"""),

    item("T75W1R1", "reviewer", """
TARGET: attack R75-C1. READ-ONLY; your own scratch/candidates are yours.
Read `plans/round-75.plan.md` R75-C1 and T75W1E1's candidate files if they
exist in `.ufo/waves/round-75/w1/T75W1E1/` (they may still be running: build
your own candidate from the plan's table if absent — your independence is the
point).
1. Build the pristine tool at 21ef81e9 and the three named mutants yourself
   (single-edit, assert count==1): `M-C` = `delimited(printed, rec['span'])` ->
   `delimited(printed, _)`; `roles-bypass`; `attack-bypass`. Run each against
   the BASE 15-arm suite and against the candidate 18-arm suite. Paste the
   verdict lines; confirm base 15/15 on all three (the before-state) and that
   the candidate kills each on its NAMED arm only (one FAIL line each, arms
   1-15 unchanged).
2. Kill-rule audit: verify (i)-(vi) of the plan one by one; for (v) add an
   always-fail arm to the candidate in scratch and show the suite fails on
   the unmutated copy; for (vi) check the battery's `CONTROL:` and
   `MUTATE_RESTORE:` lines are present and the target sha256 matches.
3. Adversarial fixture sharpness: design ONE additional plausible mutant the
   candidate suite might NOT kill (e.g. `delimited()` accepting a token
   adjacent to `.`/`,`; span check against the record but a printed token in
   a different span occurrence; roles declaration span vs record span swapped)
   and report whether it survives 18/18. A survivor is a named carry, not a
   claim failure — but say exactly which rule half stayed unmeasured.
4. Report `agree`/`disagree` with the plan's C1 after-state and every exact
   command/output you used.
"""),

    item("T75W1R2", "reviewer", """
TARGET: attack R75-C2. READ-ONLY; your own scratch is yours.
Read `plans/round-75.plan.md` R75-C2 and the pre-freeze control
`.ufo/evidence/round-75/selfstate-control-scan.py`.
1. Write your OWN scanner (do not import the lane's candidate) that reads the
   SCORECARD `## Capabilities` table at 21ef81e9 and 21ef81e9's tool bytes,
   and re-derives all 16 figures (9 unique instrument commands). Paste
   `rows/match/stale` and the per-figure old vs measured pairs. Confirm or
   refute the plan's `9 match / 7 stale` and the seven named stale figures.
2. Check the seven proposed repairs against the SAME instrument outputs: does
   each new token equal the measured token exactly? Are any of the seven
   figures already correct (i.e. the plan over-counts)?
3. Adversarial checks on the candidate instrument design (run it if E2 left
   it in its dir; otherwise reason against the plan text and test the
   refusals by constructing fixtures): (a) the echo cheat — an instrument
   whose `measured` token is copied from the doc must be impossible to
   produce from the code path (the measured token must come from the
   extracted instrument's stdout); (b) row deletion — a manifest whose
   capability name is removed or misspelled must refuse exit 2; (c) a figure
   regex that matches TWICE in one row must not silently take the wrong one
   (say which occurrence the contract binds); (d) `--doc-rev` reading must
   come from git objects, not the worktree, when supplied.
4. Verify the frozen red row's span exists at `21ef81e9` and measures exactly
   `ADDRANGE: rows=6 met=6 unexpected=0` there, with the instrument printing
   `rows=11` (so it measures `stale`).
Report agree/disagree with C2's before/after and every command/output.
"""),

    item("T75W1C1", "critic", """
TARGET: adversarial review of the frozen claims themselves. READ-ONLY.
Read `plans/round-75.plan.md`, `SCORECARD.md` `## Saturation`/`## Planned`,
`AXES.md` §Capabilities/§The stagnation nudge, and the round prompt contract
§9 if it is readable under `.ufo/` or `/home/vgpnk/Projects/shokunin/.ufo/`.
Attack, one finding per numbered item:
1. **Claim sizing §9.** Is each after-state ONE concrete value a closure can
   re-derive with one command over committed bytes? Any universal clause
   ("all", "every", "no harm anywhere") not enumerated by the counter? Is the
   calibration claim a counted mismatch (not an assertion)?
2. **Causal separability.** C1 and C2 must each verify without the other
   landing. Find any shared file, counter, commit or ordering dependency.
3. **Do-nothing reachability.** Is either target reachable without the
   claimed work (e.g. by deleting rows, by the base scan already reading the
   target, by a stub)? Score each claimed escape route against the frozen
   controls.
4. **Kill rules can fail.** For each kill rule, say what observation would
   falsify the claim and whether the counter can actually print it. Name any
   rule that is vacuous as written.
5. **Axis naming.** Is C1 operability (a runnable gate hardening) and C2
   calibration (self-assessment vs repo state), or has either been named by
   the number it produces rather than the surface it moves?
6. **Frontier step.** Is there at least one sourced claim resting on a row
   opened this round (S006 re-open)? Does the census/rejection record meet
   CORPUS contract v1? Any missing Gate element (URL, access date, <=25-word
   located quote)?
7. **Lowest-axis obligation.** Calibration is 8 and the lowest scored axis;
   does C2 actually move it, and is the nudge premise (capability entered
   round 74) correct?
Report each as AGREE / DISAGREE / DEFECT with the evidence command.
"""),

    item("T75W1M1", "mutation-tester", """
TARGET: independent mutation battery on the R75-C2 candidate instrument and
the R75-C1 candidate arms. READ-ONLY on the lane; write in your scratch/dir.
Read `plans/round-75.plan.md` first. Use T75W1E2's candidate tool if it exists
in `.ufo/waves/round-75/w1/T75W1E2/`; otherwise write your own minimal
instrument stub faithful to the plan's contract and mutate that (say which).
1. Mutate `selfstate-freshness.py` (5 single-edit, behavior-bearing mutants):
   (a) `measured := doc token` (the echo cheat); (b) `expect` ignored (every
   row ok); (c) missing capability -> treated as `match`; (d) zero rows ->
   success; (e) `--doc-rev` ignored (always worktree). Run the instrument's
   `--selftest` on each mutant; each must be KILLED by a NAMED selftest arm
   (paste the arm line). A survivor is a finding: name the missing arm.
2. Run the same mutants against the UNMUTATED selftest to prove the control
   is green and the mutations are the only delta.
3. On the C1 side: take the candidate 18-arm tool (or build the plan's three
   arms if absent) and try ONE alternative mutant per new arm that a
   sharpness-blind fixture would let through (e.g. `delimited()` accepting a
   `.`-adjacent token; a span check bound to the record's FIRST occurrence of
   the span; a roles branch that binds the span but not the declaration).
   Report killed/survived per mutant and which rule half is unmeasured.
4. Give a kill matrix (mutant x suite) and the exact commands. Report tool
   versions/installs if any (none expected).
"""),

    item("T75W1CN1", "connector", """
TARGET: sibling-overlap and two-lane-bar scan for the round's method. READ-ONLY
everywhere (read sibling trees, never write them).
Read `PROVINCE.md` (the "a pattern is admitted from evidence in TWO
independent lanes before it is claimed general" bar) and
`plans/round-75.plan.md`.
1. Scan sibling lane repos under `/home/vgpnk/Projects/shokunin/*-shokunin/`
   for an existing equivalent of R75-C2's method: a record whose own printed
   figures are re-derived from the instrument that prints them (search terms:
   `Capabilities`, `SELFTEST`, `SCORECARD` + a tool invocation, `re-derive`,
   `unexpected=`). Use `grep -rn` read-only with a bounded file set; report
   the paths and whether the pattern already exists in a second lane.
2. Scan `/home/vgpnk/Projects/shokuknow/merge/tameshi/` `MERGE-REPORT.md` and
   `knowledge/` for entries whose ground overlaps R75-C2 (self-assessment /
   capability-table freshness) or R75-C1 (arm liveness / witness-scoped
   kills); list matching target paths and whether adoption is warranted this
   round (the L1 will decide; assimilation is optional per §10).
3. Report contested scope: any sibling that OWNS self-assessment freshness or
   SCORECARD-record discipline (e.g. protocol/aggregator lanes). Quote the
   sibling PROVINCE line, if any.
4. State plainly whether the round's method may be called general (two-lane
   bar) or is lane-only evidence.
"""),

    item("T75W1SN1", "sentinel", """
TARGET: security and hygiene audit of the round's new material. READ-ONLY.
1. Credential scan: `grep -inE 'set-cookie|authorization:|op://|ghp_|sk-[A-Za-z0-9]|BEGIN [A-Z ]*PRIVATE KEY'`
   over `.ufo/evidence/round-75/`, `.ufo/waves/round-75/`, `plans/round-75.plan.md`
   and the lesson drafts; report every hit with file:line and decide whether it
   is a credential or a false positive (a `Vary: Authorization` header name is
   not a credential). Check `.ufo/evidence/round-75/sources/s006-headers.txt`.
2. Scratch discipline: list `.ufo/waves/round-75/w1/*/` and `/fast/scratch/
   hyaku/tameshi-r75/` for leftovers; every seat dir under the wave dir must
   be candidates/receipts (no multi-GB copies); report any hardcoded `/tmp`
   root or `/tmp` evidence path in the new candidates (`grep -rn '/tmp'` over
   the new candidate tools and the plan).
3. TMPDIR contract: verify the round's instruments honour `TMPDIR` (the plan's
   battery command passes `--workdir`; `selfstate-freshness.py` must not
   create anything outside its scratch/TMPDIR). Run a `TMPDIR=<scratch>`
   invocation of whatever candidate tools exist and check nothing new appears
   under `/tmp` (`find /tmp -newermt '-2 minutes' -maxdepth 1` before/after).
4. Scope audit: `git -C {lane} status --porcelain` and
   `git -C /home/vgpnk/Projects/shokunin status --porcelain` — report any path
   a seat wrote outside its own report dir (the L1 runs the misroot sweep; you
   are the independent check). Never delete anything.
5. Report SECRETS=n, TMPDIR_VIOLATIONS=n, SCOPE_HITS=n with the commands.
"""),
]

def main():
    spec = {"wave": "r75-w1", "maxLanes": 16,
            "reportDir": ".ufo/waves/round-75/w1",
            "hoist": False, "context": CTX, "items": ITEMS}
    out = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-75/w1-spec.json"
    with open(out, "w") as f:
        json.dump(spec, f, indent=1)
    print("wrote", out, "items", len(ITEMS),
          "roles", sorted({i["role"] for i in ITEMS}))


if __name__ == "__main__":
    main()
