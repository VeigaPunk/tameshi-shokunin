#!/usr/bin/env python3
"""Generate the round-76 wave spec (12 seats). Lane-local evidence; the wave
validator is the authority on shape."""
import json

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
SCRATCH = "$HYAKU_SCRATCH_DEFAULT_tameshi-r76"
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
  {lane}/.ufo/waves/round-76/w1/ . Never run git/jj mutating commands
  (add/commit/stash/checkout/reset/pull/push, jj commit/new/describe/squash/
  rebase/abandon/bookmark/undo) anywhere, never edit tracked files, never
  touch /home/vgpnk/Projects/shokunin (fleet repo), /home/vgpnk/Projects/shokuknow
  writes (read it if your item says so), or any sibling lane repo.
- Scratch root: /fast/scratch/hyaku/tameshi-r76/<your-seat-name>/ , created with
  mkdir -p and REMOVED before you finish (trap 'rm -rf -- "$S"' EXIT or a
  finally block). /tmp is for files under 50 MB only. Every clone is
  `git clone --shared` or a git archive/worktree copy; no full mirror of the lane.
- A fixture git repo is created only as D=$(mktemp -d) && git -C "$D" init -q
  (throwaway -c user.name/email identities ONLY inside such fixture repos) and
  every later git call names -C "$D"; verify
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
  {lane}/.ufo/waves/round-76/w1/<your-seat-name>.md .
- Your final message must be a compact findings summary: commands run, exact
  verdict lines, files written, and what you could NOT establish.
"""


def item(name, role, text):
    text = text.replace("{lane}", LANE).replace("{scratch}", SCRATCH)
    assert "{lane}" not in text and "{scratch}" not in text, name
    return {"name": name, "role": role,
            "axes": ["verification-fixture-craft"],
            "item": DPREFIX + text.strip() + "\n"}


CTX = """# Goal and authority
Tameshi lane (verification-fixture craft), round 76, wave w1. The L1 (agent id
`TameshiR76`) is the ONLY coordinator, writer, claim judge and committer. Two
claims are frozen BEFORE any of this wave's data in
{lane}/plans/round-76.plan.md — read it first; it carries the predicates,
counting commands, kill rules, the frozen kill matrix and the C2 tuple table.
Seat outputs are evidence for the L1's verdict, never verdicts themselves.
Base revision 451ed5cb6d5f8c2bf4b3e10836e4634cfcb03ee0 = origin/master (the
round-75 closure verdict commit). Your item's candidates/receipts go under your
own report subdirectory; the L1 integrates them into the lane.

The L1's design-phase candidates and batteries are committed (pre-data) under
{lane}/.ufo/waves/round-76/l1/ — cand-wr-19.py (arm19 candidate),
cand-ss-11.py (ARM11 candidate), wave-reconcile-mutants-r76.spec (seven
defects), mut-*.py (five instrument mutants + two base survivors),
selfstate-freshness-r76.json (the 20-row extended manifest),
bat-wr.out (battery transcript), c2-before-r76.txt, base-survivors.txt,
design.py / design2.py / arm11-block.txt (the builders). Attack targets exist;
your own derivations must be independent (build from base bytes per the plan,
do not just re-run the L1's files).

R76-C1 (operability, sourced on the re-opened S006): wave-reconcile
`arm19-seatreports-printed-required` kills the `adv-seatreports-require-printed-bypass`
survivor; selfstate `ARM11_doc_rev_cli_binding` kills the `--doc-rev-ignored`
survivor. Targets: `WAVE_RECONCILE_SELFTEST: 19/19 pass`,
`SELFSTATE_SELFTEST: 11/11 pass`, battery `defects=7 killed=7`, five
instrument mutants killed on their named arms.

R76-C2 (calibration, lowest scored axis 8): the selfstate population 17 → 20
rows (three frozen tuples in the plan's table). Before at base:
`SELFSTATE: rows=20 match=16 stale=4 unexpected=2` exit 1. After the two cell
supersessions: `rows=20 match=18 stale=2 unexpected=0` exit 0.

# Fleet context
The fleet runs other lanes concurrently; their trees are read-only to you.
{common}
""".format(lane=LANE, common=COMMON.format(lane=LANE, scratch=SCRATCH))

ITEMS = [
    item("T76W1E1", "executor", """
TARGET: independent re-derivation of the R76-C1 wave-reconcile arm. Do NOT
edit the lane. Base bytes:
`git -C {lane} cat-file blob 451ed5cb6d5f8c2bf4b3e10836e4634cfcb03ee0:tools/wave-reconcile.py`
(sha256 bf10c0e490e78e3f98fdb580442916e685968a94ff8c3fc977dead4b74a7f791).
1. Read plans/round-76.plan.md R76-C1 first (arm spec, kill matrix, kill rule).
2. Build your own candidate from base bytes: append
   `arm19-seatreports-printed-required` exactly as the plan freezes it (the
   TypeError-catching wrapper, want `setup:record-printed-absent`) and
   SELFTEST_ARMS 18 -> 19. Run `python3 -I -X utf8 <cand> --selftest` — paste
   the last line (expect 19/19) and the arm19 line.
3. Build the seventh spec defect exactly as the plan freezes it (the
   seat_reports two-line @old with the escaped \\n; count(old)==1 must hold on
   base bytes AND on your candidate). Run the lane's runner COPY (copy
   {lane}/tools/mutate-and-run.sh into your scratch, never modify the lane):
   `bash <copy> --target <cand> --defects <spec7> --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --workdir <scratch>/bat --label wave-reconcile-arms-r76-e1`
   Paste CONTROL, MUTATE_RESTORE, MUTATE: DONE and the per-defect FAIL lines.
4. Verify the plan's frozen matrix: each of the seven mutants dies exactly on
   the arms the plan's table names (m2 -> arm13+arm16; span-rule -> arm14+
   arm17+arm18; seat-reports-any-depth -> arm15; mc -> arm16; roles -> arm17;
   attack -> arm18; adv-seatreports-require-printed-bypass -> arm19 ONLY).
5. Verify arms 1-15 identity: the SELFTEST arm1..arm15 lines of base bytes vs
   your candidate must be byte-identical (paste a diff or `cmp` receipt).
6. Diff your candidate's arm19 block and your spec's seventh block against the
   L1's committed `.ufo/waves/round-76/l1/cand-wr-19.py` and
   `wave-reconcile-mutants-r76.spec` — report any divergence and which bytes
   you would land.
7. Write your candidate, spec, battery transcript and a findings report in
   your dir.
"""),

    item("T76W1E2", "executor", """
TARGET: independent re-derivation of the R76-C1 selfstate ARM11. Do NOT edit
the lane. Base bytes:
`git -C {lane} cat-file blob 451ed5cb6d5f8c2bf4b3e10836e4634cfcb03ee0:tools/selfstate-freshness.py`
(sha256 3b09676340fc63007d3a1e5de3e54471feddb22024a2f40bd4b3b469f560eba6).
1. Read plans/round-76.plan.md R76-C1 first.
2. Build your own ARM11 candidate from base bytes per the plan (CLI subprocess
   arm, two-state git fixture under YOUR scratch with TMPDIR honoured,
   rev1 doc `4/4` vs worktree doc `9/9`, toy instrument committed at rev1,
   expect `SELFSTATE: rows=1 match=1 stale=0 unexpected=0` exit 0).
   SELFTEST_ARMS 10 -> 11. Run `python3 -I -X utf8 <cand> --selftest` — paste
   the last line (expect 11/11) and the ARM11 line.
3. Hermeticity: run the selftest with TMPDIR set to a scratch dir and verify
   nothing is created outside it and nothing leaks (dir count before/after);
   verify no network and the fixture repo is created with throwaway identity
   inside the temp dir only.
4. Rebuild the five instrument mutants on YOUR candidate bytes (the plan
   freezes the five edits: echo keeps `stdout, exit_code, _stderr = ('', 0,
   '')`; expect -> 'ok': True; capability-absent -> SetupError('zero-rows-
   deflected'); zero-rows -> pass; doc-rev -> `if False:`). Each count(old)==1.
   Run each: paste rc + last line + the failing ARM line. Expected: echo fails
   ARM2 (+ARM3/ARM9 collateral), expect fails ARM2, capabs fails ARM4, zero
   fails ARM6, doc-rev fails ARM11 ONLY.
5. Verify the survivor kill: the doc-rev mutant must FAIL on your candidate
   (10/11 with ARM11 FAIL) while it PASSED on base bytes (10/10 — verify that
   too with your own base mutant).
6. Diff against the L1's committed `.ufo/waves/round-76/l1/cand-ss-11.py` —
   report divergences and which bytes you would land.
7. Write your candidate, mutants, transcripts and findings in your dir.
"""),

    item("T76W1E3", "executor", """
TARGET: independent re-derivation of R76-C2's before-state and the repair
edits. Do NOT edit the lane.
1. Read plans/round-76.plan.md R76-C2 first (the frozen tuple table IS the
   counter).
2. Build the 20-row extended manifest from the plan's table (the 17 committed
   rows in tools/selfstate-freshness.json + EXACTLY the three appended rows,
   instruments pinned at 451ed5cb..., figure regex \\d+/\\d+). Byte-diff your
   manifest against the L1's `.ufo/waves/round-76/l1/selfstate-freshness-r76.json`.
3. Run the LANED tool (unmodified):
   `python3 -I -X utf8 {lane}/tools/selfstate-freshness.py --repo {lane} --manifest <your-manifest> --doc-rev 451ed5cb6d5f8c2bf4b3e10836e4634cfcb03ee0`
   Paste the full SELFSTATE_ROW lines for the three new rows and the final
   line (expect `SELFSTATE: rows=20 match=16 stale=4 unexpected=2` exit 1).
4. Verify token uniqueness yourself: `python3 -I tools/pin-disposition.py
   --selftest | grep -oE '[0-9]+/[0-9]+' | sort | uniq -c` must print exactly
   one token 19/19 (count 1); same for evidence-disposition -> one token
   66/66. Also verify the span `56/56` occurs in SCORECARD.md at base
   (`git show 451ed5cb...:SCORECARD.md | grep -c '56/56'`) and locate its line.
5. Verify the 17 pre-existing rows still read green at base with the LANED
   manifest (the r75 line `rows=17 match=16 stale=1 unexpected=0`).
6. Draft the two repair edits as exact old/new ROW text (the capability rows
   at lines ~244 and ~246 of SCORECARD.md: `18/18 PASS0` ->
   `SELFTEST: PASS (19/19)` and `PASS34/34 exit0` -> `SELFTEST: PASS (66/66)`,
   row-scoped, everything else in the row byte-identical) plus the round-76
   supersession line to append after the round-17 disclosure (naming 19/19,
   66/66 with receipts and the two bash gaps 95/95->107/107, cases=7->cases=10;
   state that the round-17 values stand as dated history). Write them as a
   patch file in your dir; the L1 lands them.
7. Measure the two named-gap instruments at base for the disclosure line:
   `bash {lane}/tools/mutate-and-run.sh --selftest | tail -1` (expect
   MUTATE_SELFTEST: 107/107 pass) and confirm the `--regression` count
   `cases=10` from the committed design receipts (do NOT re-run --regression;
   it takes ~2 min; cite `.ufo/evidence/round-76` or rerun only if time allows).
8. Write your manifest, transcripts, patch and findings in your dir.
"""),

    item("T76W1E4", "executor", """
TARGET: the receipt-exists scratch-leak fix candidate + standing-instrument
registry rows. Do NOT edit the lane.
1. Red-before: reproduce the leak yourself — `TMPDIR=<scratch>/probe
   python3 -I {lane}/tools/receipt-exists.py --selftest` then list TMPDIR:
   expect 2 leftover dirs (`receipt-exists-selftest-*`, `...-extra`). Compare
   with the committed `.ufo/evidence/round-76/receipt-exists-leak-r76.txt`.
2. Build the fix candidate from base bytes
   (`git -C {lane} cat-file blob 451ed5cb...:tools/receipt-exists.py`): every
   mkdtemp'd directory is removed in a `finally` via `shutil.rmtree(...,
   ignore_errors=True)`; TMPDIR is honoured (no hardcoded /tmp); the selftest
   must still print `RECEIPT_EXISTS_SELFTEST: 4/4 pass` exit 0. Verify: run
   with TMPDIR=<scratch>/probe2 — leftover_count must be 0; run without
   TMPDIR — nothing under /tmp (check `find /tmp -maxdepth 1 -name
   'receipt-exists-*' -newermt '-3 minutes'` before/after).
3. Enumerate standing instruments with no tools/registry.json row: list every
   `tools/*.py` with a `--selftest`, read tools/registry.json, and name the
   gaps. Minimum set to draft rows for: printed-count-recheck.py,
   pointer-recheck.py (or its landed name), anchor-drift-sweep.py,
   arm-liveness.py, figure-attribution.py, receipt-exists.py (your candidate).
4. For each: run the selftest hermetically (TMPDIR under your scratch, cwd
   {lane}) and the standing sweep if it has a manifest mode that runs
   hermetically at a pinned rev (`--rev`); capture the EXACT last line and rc.
   Draft one registry.json row per instrument in the existing schema (name,
   kind, argv, expect {{exit, stdout_contains}}, timeout_s,
   source `tools/X.py@<rev>:1-40`, status active, tags ["round-76"],
   scratch_root note) PLUS the Gate-standard fields the r75 spotcheck routed:
   verdict_map (exit code -> class), write_scope, owner ("tameshi"),
   pinned_value path. If a sweep needs a manifest or rev pin you cannot
   verify hermetically in this wave, draft the SELFTEST row only and say so.
5. Write the fix candidate, the before/after leak receipts, the drafted rows
   (JSON) and findings in your dir.
"""),

    item("T76W1S1", "scribe", """
TARGET: drafts for the round-76 records (the L1 lands canonical bytes; you
draft). READ-ONLY on the lane except your own dir.
1. Read plans/round-76.plan.md, LOG.md's Round 76 declared entry, and
   `.ufo/waves/round-76/l1/*` receipts.
2. Draft `corpus/lessons/round-76.md`: header (round, base, plan pointer,
   wave shape), a `## Gate` skeleton with the S006 re-open subsection
   (placeholders marked WHERE THE SCOUT'S QUOTES GO), a `### Gate — census`
   subsection (start receipt cited; end line placeholder), a `## Claims`
   section (R76-C1/R76-C2 before/after with the committed receipt paths),
   `## Mistakes` rows in the class/evidence/captured-by/fix table form (the
   receipt-exists scratch leak with the red-before receipt; any second
   mistake from your reading of the pre-data receipts), and a `## Findings
   routed to round 77` section skeleton.
3. Draft the `## Round 76 — measured` LOG.md entry skeleton and the SCORECARD
   `## Round 76 — declared/measured claims` block skeleton, mirroring the
   round-75 shapes (tables with verdict/after/counting-command/measured-commit
   columns; placeholders marked).
4. Draft the SOURCES.md `Round 76` note paragraph (mirroring the Round 73/75
   notes: NO new row, S006 re-opened, used-by old->new) and the two
   `corpus/lessons` appends: the round-73 plan erratum text (the contradicted
   kill-rule sentence — read plans/round-73.plan.md, find the exact sentence
   the r75 spotcheck §6 item 3 names as contradicted, draft the appended
   erratum naming it) and the round-74 S294 used-by old->new record (read
   `corpus/lessons/round-74-verifier-spotcheck.md` defect 5 and the round-74
   lesson's Gate, draft the append-only correction).
5. Draft QUALITY.md criteria 126 and 127 from r75 spotcheck §6 items 1-2
   (kill rules satisfiable by construction before data; counter tuples frozen
   in the plan), each with its lesson citation and a "Falsifier that must
   fail" paragraph, mirroring criterion 125's shape.
6. Write all drafts in your dir. Quote exact receipts; mark every placeholder
   clearly.
"""),

    item("T76W1SC1", "scout", """
TARGET: the S006 re-open (the round's sourced-claim source) and census.
READ-ONLY.
1. Fetch `https://raw.githubusercontent.com/BWBama85/shmutant/master/README.md`
   (curl -sS --dump-header <headers.txt> -o <extract.md>; record HTTP status,
   HTTP date, byte count, sha256; verify `grep -ic set-cookie` is 0 and no
   authorization credential appears). Save extract + headers in your dir.
   Compare the sha256 with the round-75 receipt's
   `960577288ed5c5eb80f42669fcb30bf254b9a917ae2bde3a117888056ef354e2`
   (.ufo/evidence/round-75/sources/s006-shmutant-readme.md) — report whether
   the page changed since 2026-11-04 02:22 GMT.
2. Locate and quote, with extract line numbers and whitespace-token counts:
   (a) the witness definition line; (b) the "went red on its witness" line;
   (c) the accidental-red line; (d) the `unapplied` locator line. All must be
   <=25 words for the Gate. These ground R76-C1's named-arm kills (witness-
   scoped verdicts: red is not a kill; red ON THE NAMED ARM is).
3. Census: run
   `TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
   and paste the tail + exit code (the round-start receipt
   .ufo/evidence/round-76/census-start.txt must match: exit 0, 164 rows).
   Confirm the next unused id is S305 (`grep -oE 'S[0-9]+' {lane}/corpus/SOURCES.md | sort -u | tail -3`).
4. Verify no within-scope duplicate forces a new row this round: the S006 row
   cells at `corpus/SOURCES.md` (id, source URL, scope, anchor) — quote them.
5. Write the fetch receipt, quotes and census output in your dir.
"""),

    item("T76W1R1", "reviewer", """
TARGET: attack R76-C1. Read plans/round-76.plan.md first. Try to BREAK the
claim, not to pass it.
1. Do-nothing control: with NO arm installed, can either after-state be
   reached? Run base bytes' selftests (18/18, 10/10) and confirm both
   survivors alive (rebuild the two base mutants yourself from the plan's
   exact edits). Paste outputs.
2. Kill-rule audit: check each frozen clause (i)-(vii) is checkable from
   committed artifacts and satisfiable by construction (r75 defect 1
   discipline: a rule shown unsatisfiable mid-round is a defect — is any
   clause unsatisfiable? e.g. can (iv) and the disclosed echo collateral
   conflict?).
3. arm19 wrapper audit: does catching TypeError hide anything dangerous? On
   the pristine candidate, run arm19's fixture directly — is the refusal
   `record-printed-absent` (the right one) and not an accidental TypeError
   swallowed as a pass? What happens if the tool's detail format changes so
   printed=None no longer crashes — does arm19 still catch the mutant (answer
   by reading the mutant's behavior: printed=None -> ok False -> drift return
   -> got=drift FAIL — is that still a kill under the frozen rule (iv)?).
4. Spec hygiene: every @old in the seven-defect spec has count==1 on the
   candidate bytes (run the runner's --check or count yourself); no @new
   equals @old; the first six blocks are byte-identical to base
   (`git -C {lane} show 451ed5cb...:tools/wave-reconcile-mutants.spec` vs the
   r76 spec — diff must show only the appended block + banner).
5. Re-run BOTH L1 candidate selftests yourself and compare each of the 19/11
   arm lines against base's 18/10 (arms 1-15 and ARM1-ARM10 identity).
6. Report: every attempted falsification with its exact command and output,
   and a verdict per kill rule clause.
"""),

    item("T76W1R2", "reviewer", """
TARGET: attack R76-C2. Read plans/round-76.plan.md first.
1. Tuple freeze audit: byte-compare the L1's
   `.ufo/waves/round-76/l1/selfstate-freshness-r76.json` three new rows
   against the plan's tuple table (id, mode, capability/span, figure, tool
   path, rev, argv, expect). Any drift = the manifest is not the counter.
2. Loose-regex critique (the r75 control-4 analog): the figure regex
   `\\d+/\\d+` — construct a counter-manifest whose regex matches doc AND
   instrument trivially (e.g. `[0-9]`) and show what the sweep then reads
   (does it false-green?). Is the frozen regex the TIGHTEST that still spans
   the before-cell (`18/18 PASS0`) and the after-cell (`SELFTEST: PASS
   (19/19)`)? Could `PASS \\(\\d+/\\d+\\)` work for the after-state but break
   the before-state into a refusal — is that acceptable under the frozen kill
   rule (vi)? Argue both sides, then verdict.
3. Repair-scope audit: the two capability rows (SCORECARD lines ~244/~246) —
   verify the old tokens occur EXACTLY ONCE in those rows and count their
   occurrences in the whole file (historical blocks quote the same figures —
   the repairs must be row-scoped; draft the exact old/new strings you would
   require and show a wrong-scope replace would corrupt history).
4. Span row audit: locate the round-17 supersession line
   (`grep -n 'dated literals' SCORECARD.md` and neighbours); confirm `56/56`
   is IN that line, unique within it, and the row's expect=stale makes the
   drift measured, never assumed. What happens at the landing rev AFTER the
   disclosure line is appended — does the span row still resolve (the span is
   the OLD line's bytes; the append must not move or rewrite them — verify
   the plan's landing order does that)?
5. Independent before-state run: run the extended manifest against base
   yourself (`python3 -I -X utf8 {lane}/tools/selfstate-freshness.py --repo
   {lane} --manifest .ufo/waves/round-76/l1/selfstate-freshness-r76.json
   --doc-rev 451ed5cb...`) and compare line-by-line with
   `.ufo/waves/round-76/l1/c2-before-r76.txt`.
6. Report verdicts per kill rule clause with exact outputs.
"""),

    item("T76W1C1", "critic", """
TARGET: falsify the round's predicates themselves. Read
plans/round-76.plan.md and `.ufo/waves/round-76/l1/` receipts first.
1. Satisfiability by construction (r75 spotcheck defect 1): for each kill
   rule clause, prove from the committed design receipts whether it can FAIL
   a honest landing (i.e. is any clause vacuous, unsatisfiable, or
   un-checkable from committed bytes?). The r75 lesson: a rule amended after
   measurement is not the claim's rule — are any of these rules likely to
   need amendment? Say which and why BEFORE data.
2. The C1 do-nothing control: base survivors alive (re-verify from
   base-survivors.txt by re-running both base mutants yourself). Is the
   after-state reachable without the arms by ANY cheaper edit (e.g. changing
   SELFTEST_ARMS alone, weakening an arm)? Try one such cheap forgery on a
   scratch copy and show it fails the frozen kill rules (which clause catches
   it?).
3. The C2 counter: is the loose `\\d+/\\d+` regex an echo-cheat surface
   (build the r75-control-4 analog: a manifest whose regex is satisfied by
   any digits — does it false-green the before-state at base? paste the run).
   If it false-greens, the tuple freeze in the plan is the only defense —
   verify the plan's tuples are complete enough that a differing manifest is
   detectable (what byte-level check would you run as the closure?).
4. Sizing and honesty: are the two claims causally separable as the plan
   claims (C2 verifiable at base without C1)? Is any claim a do-nothing
   control could reach? Is the named-gaps disclosure (bash instruments) a
   silent narrowing of the routed defect or an honest scope?
5. Write a verdict per claim: fails-as-frozen / verifies-as-frozen /
   defect-named, with reasons and exact evidence.
"""),

    item("T76W1M1", "mutation-tester", """
TARGET: independent replication of both batteries + ONE new survivor hunt.
Read plans/round-76.plan.md first.
1. Replicate the wave-reconcile battery on the L1's committed candidate
   (`.ufo/waves/round-76/l1/cand-wr-19.py` + spec) in YOUR scratch with the
   lane runner COPY: paste MUTATE: DONE and per-defect FAIL arms; compare
   with the plan's frozen matrix — any divergence is a finding.
2. Replicate the selfstate instrument mutants on the L1's committed candidate
   (`.ufo/waves/round-76/l1/cand-ss-11.py` + the five `mut-*.py`): verify
   each dies on its named arm; verify `doc-rev-ignored` dies ONLY on ARM11.
3. New-survivor hunt (adversarial, beyond the named set): build 3-5 of your
   own single-edit mutants against either candidate — suggestions: wave-
   reconcile `listing()` top-level filter boundary, `_artifact()` root
   fallback, selfstate `parse_capabilities` first-cell matching,
   `extract_token` findall boundary, `SUPPORT_BLOBS` best-effort write. A
   mutant that survives BOTH selftests AND its natural arm surface is a
   named survivor for round 77 — probe it for non-equivalence (SKILL.md
   recipe step 8) before calling it a survivor.
4. Restore discipline: every mutant run happens on scratch copies; verify the
   lane tree is untouched (`git -C {lane} status --porcelain` empty at start
   and end).
5. Write your battery transcripts, the matrix comparison, and any new
   survivor's probe receipt in your dir.
"""),

    item("T76W1CN1", "connector", """
TARGET: sibling-overlap + assimilation + considerthese scan. READ-ONLY.
1. Scan sibling lane repos under `/home/vgpnk/Projects/shokunin/*-shokunin/`
   for an existing equivalent of R76-C2's method (a record's printed figures
   re-derived from the printing instrument — search `selfstate`, `SELFSTATE`,
   `re-derive` + `figure`) and of R76-C1's CLI-binding arm pattern. Use
   `grep -rn` read-only with a bounded file set; report paths and whether any
   pattern already exists in a second lane (the two-lane bar for 'general').
2. Scan `/home/vgpnk/Projects/shokuknow/merge/tameshi/` (MERGE-REPORT.md,
   knowledge/, SOURCES.append.md) for entries whose ground overlaps this
   round's claims (arm liveness, witness-scoped kills, self-assessment
   freshness, registry discipline). List matching target paths and whether
   adoption is warranted THIS round; the L1 decides and may report
   `Assimilation: none`.
3. considerthese: read `/home/vgpnk/Projects/shokunin/tameshi-shokunin/considerthese/2026-10-28.md`
   and the 2026-10-26 file's proposals; cross-check each 'Self-improvement
   ideas' proposal against the lane's landed tools (receipt-exists.py,
   arm-liveness.py, rekey-cost.py, pointer-recheck.py exist — which
   proposals are STILL unimplemented?). For the assimilation-backlog-burn-down
   proposal (2026-10-26 proposal 4 if still unimplemented): measure the
   baseline — count knowledge entries in merge/tameshi (ls | wc -l) and count
   how many the lane's corpus cites (grep corpus/knowledge for the package's
   target paths or S-ids from SOURCES.append.md) — a pasteable counting
   command for the lesson.
4. Contested scope: any sibling that OWNS self-assessment freshness or
   gate-registry discipline (protocol/aggregator lanes)? Quote the province
   line.
5. Report overlap findings and a plain recommendation per point.
"""),

    item("T76W1SN1", "sentinel", """
TARGET: security and hygiene audit of the round's new material. READ-ONLY.
1. Credential scan: `grep -inE 'set-cookie|authorization:|op://|ghp_|sk-[A-Za-z0-9]|BEGIN [A-Z ]*PRIVATE KEY'`
   over `.ufo/evidence/round-76/`, `.ufo/waves/round-76/`,
   `plans/round-76.plan.md`; report every hit with file:line and decide
   credential vs false positive.
2. Scratch discipline: list `.ufo/waves/round-76/w1/` and
   /fast/scratch/hyaku/tameshi-r76/ for leftovers; every seat dir under the
   wave dir must be candidates/receipts (no multi-GB copies); report any
   hardcoded /tmp root or /tmp evidence path in the new candidates
   (`grep -rn '/tmp'` over the wave dir's .py files, excluding
   TMPDIR-honouring patterns like `${TMPDIR:-/tmp}` — name which pattern each
   hit uses).
3. TMPDIR contract: run the L1's committed candidates' selftests with
   TMPDIR=<scratch> and verify nothing appears under /tmp
   (`find /tmp -newermt '-3 minutes' -maxdepth 1 -name '*selfstate*' -o -name
   '*wave-reconcile*' -o -name '*arm11*'` before/after) and the scratch dirs
   are removed by the tools themselves (selfstate has a finally rmtree;
   wave-reconcile too — verify ARM11's fixture is removed).
4. Scope audit: `git -C {lane} status --porcelain` and
   `git -C /home/vgpnk/Projects/shokunin status --porcelain` at start and
   end — report any path a seat wrote outside its own report dir (the L1
   runs the misroot sweep; you are the independent check). Never delete.
5. Report SECRETS=n, TMPDIR_VIOLATIONS=n, SCOPE_HITS=n with commands.
"""),
]


def main():
    spec = {"wave": "r76-w1", "maxLanes": 16,
            "reportDir": ".ufo/waves/round-76/w1",
            "hoist": False, "context": CTX, "items": ITEMS}
    out = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-76/w1-spec.json"
    with open(out, "w") as f:
        json.dump(spec, f, indent=1)
    print("wrote", out, "items", len(ITEMS),
          "roles", sorted({i["role"] for i in ITEMS}))


if __name__ == "__main__":
    main()
