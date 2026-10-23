# ReviewQualityDraft — round-30 QUALITY.md draft criteria 58–63

Reviewer: TameshiR30A2.ReviewQualityDraft-7, 2026-10-23. Target: the uncommitted
appendix to `corpus/QUALITY.md` (attempt-1 draft, `git diff` +63 lines after
criterion 57). Recommendation only; nothing edited, judged, integrated or shipped.

**Verdict.** All six criteria are true in substance, checkable, and able to fail.
Falsifier bytes verified for 58, 59, 60, 61. Two wording defects make falsifiers
dangle or blur: 62 attributes the C2 head receipt to the wrong commit (it is not
in the `7a45f7b9` tree; it landed at `9bb699ad`), and 63 cites only half its
comparison (the "52" byte lives in `c1-at-A.stdout`, uncited) and is the only
criterion without a "Captured by" line. 59's falsifier file
(`r29-mistake1-ordering.txt`) is currently untracked — it must be committed with
the criteria or the falsifier dangles (the same defect routed item 7 already
named). No routed item number 1–7 is wholly uncited, but routed item 5(c) has no
criterion, and item 7's S059-row and MutateLegSum carry-overs have none.
Header says "(routed items 1–6)" while criterion 59 cites item 7 — fix the
header. One new criterion (64) is proposed for the round-30 lesson on job-label
leaks, evidenced by control K9.

## Per-criterion review

| # | True | Checkable | Able to fail | Falsifier bytes | Defect |
|---|---|---|---|---|---|
| 58 | yes | yes | yes | verified | refusal half has no byte pointer (fix below) |
| 59 | yes | yes | yes | verified | falsifier file untracked; commit it with the criteria |
| 60 | yes | yes | yes | verified | "passing … on assembler shape alone" imprecise (minor) |
| 61 | yes | yes | yes | half verified | "Read10C's report landed at the fleet root" is no longer checkable (file moved) |
| 62 | yes | yes | yes | half verified | receipt named as "(`c2-at-E.stdout`, `7a45f7b9`)" but not in that tree |
| 63 | yes | yes | yes | half verified | "against 52" uncited; no "Captured by" line |

## Evidence (commands and observed output)

All git calls read-only with `GIT_OPTIONAL_LOCKS=0`. No `lsp` device exists in
this seat's tool inventory, so every check below is a byte or git-tree check;
that unavailability is recorded, and no grep output is offered as semantic proof.

1. Draft scope. `GIT_OPTIONAL_LOCKS=0 git -C tameshi-shokunin diff -- corpus/QUALITY.md`
   → one file, +63 lines, `## Criteria appended — round 30 (2026-10-23)`, items
   58–63; committed `corpus/QUALITY.md` ends at 57. Working tree shows
   ` M corpus/QUALITY.md` — the draft is uncommitted, as stated.
2. Criterion 58. `tameshi-shokunin/.ufo/evidence/round-29/contract.json` key
   `controls_required_before_data` = `["do-nothing", "junk", "all-false",
   "no-reader", "shortcut keyed on ids or labels"]` — the class name matches the
   criterion verbatim. Listing `.ufo/waves/round-29/ctl/` gives
   `C1v2-rescore.txt, CriticC2v2.md, CtlC2v2Port.md, CriticC2Design.md,
   CriticC1Design.md, CtlC1Cheap.md, CtlC2Cheap.md` — no scored shortcut
   receipt. Globbing `.ufo/waves/round-29/**/*Shortcut*` returns no files; the
   holds are recorded in `.ufo/waves/round-29/res/ReviewControls.md:77-89`
   ("CtlC1Shortcut: yes, pre-data … provider-safety-refusal hold", "CtlC2Shortcut:
   no pre-data record", "both shortcut seats refused, the refusals were accepted
   as holds"). True, checkable, able to fail (a dispatch whose contract names an
   unscored required class).
3. Criterion 59. `.ufo/evidence/round-30/r29-mistake1-ordering.txt` (read
   `:raw`) shows `ctl/CriticC2v2.md 2026-10-22 22:33:57.922771384 -0300`,
   `task-adapter-w1.json 2026-10-22 22:27:45.552673827 -0300`, and
   `first-commit bc2058a405fadfc1594c4ee764988902c09525ee 2026-10-22T22:50:31-03:00`
   for both — exactly the criterion's "after … and both first landed together in
   `bc2058a4`, so no committed order existed". But `git status --porcelain`
   prints `?? .ufo/evidence/round-30/r29-mistake1-ordering.txt`: the falsifier
   is uncommitted today.
4. Criterion 60. `.ufo/evidence/round-29/coldread/select-receipt-w1.json`:
   `assembled: 32, kept: 22, excluded: 10`; the excluded entries carry
   `"report_verdict": "executed-ok"` against `"entry_verdict": "gap-minor"`
   with `"read_rev_equal": true` (assembler verdict normalization) and
   `"seat-not-registry-member:TameshiR29.Read08A"` (and Read08B, Read11B,
   Read12B) — seat self-labels. Both mismatch classes are assembler shape, none
   is content; all report verdicts are passing classes. The falsifier's claim is
   byte-supported.
5. Criterion 61. `.ufo/waves/round-29/spec-w1.json` key `context` contains
   "kill any process tree you started before you return" and no "never kill a
   process you did not start" sentence — first half verified. Second half: the
   fleet-root copy of `Read10C.md` was moved into the lane (round-29 spot-check,
   routed item 5a; `lessons/round-29.md` Mistake 3, sha256 `fafd4c36…`), so
   "Read10C's report landed at the fleet root" describes an event whose artifact
   no longer exists at the named place.
6. Criterion 62. Fleet report at `772f7105`, `.ufo/reports/round-29/tameshi.md`
   line 77: C2 after = `… entry_sourced=1 quote_located=1` naming `6892c3ee`,
   `1a1e8b22`, `3c16b3a6` — verified. Receipt side:
   `git show 7a45f7b9:.ufo/evidence/round-29/c2-at-E.stdout` →
   `fatal: path … exists on disk, but not in '7a45f7b9'`;
   `git ls-tree -r 7a45f7b9 --name-only | grep at-E` → empty;
   `git ls-tree -r 9bb699ad …` → `c1-at-E.stdout`, `c2-at-E.stdout`. The file's
   own line 2 reads `… quote_located=0 rev=7a45f7b9d6a2542a…`. So the receipt
   measured `7a45f7b9` but was committed at `9bb699ad`; the criterion's
   parenthetical conflates the two.
7. Criterion 63. `.ufo/evidence/round-30/drift-sim-union4.txt` line 1:
   `C1_MONITOR: covered=33/64 restraint=6 box3_mismatch=1 depth_score=9
   rev=daa11583c999b249b35055cc45eeb00b38040996` plus 32 uncovered lines — the
   64 → 33 half is verified and the file is committed (3 commits touch it). The
   comparison figure 52 has no pointer in the criterion; its byte is
   `.ufo/evidence/round-29/c1-at-A.stdout`: `covered=52/64 … rev=9f3084bc…`
   (committed). "against 52 without the runner" is checkable only through that
   second file.
8. Control K9 pair (basis for the proposed criterion). Draft counter
   `.ufo/evidence/round-30/v4/c1-measure-v4-draft.py` ran each `--selftest` in
   `d = os.path.join(tree, '..', 'st-' + name)` and invoked
   `bash RUNNER --selftest` with that directory as cwd; the frozen
   `.ufo/evidence/round-30/c1-measure-v4.py` replaces this with
   `tempfile.mkdtemp(prefix='w', …)` plus a bubblewrap sandbox
   (`--unshare-all --clearenv`, private `/tmp`, every job's tree bound at the
   same `/w`). The draft's own comment names the leak vectors: "a selftest keyed
   on its own directory name, or on /proc/$PPID/cmdline, the counter source or
   the sealed file, could classify jobs without testing the tally."
   `.ufo/evidence/round-30/v4/K9-on-draft.stdout`: every drop/insert/heldout row
   exits 1, summary `killed=13/13 … sealed_killed=6/6 sealed_equiv=6/6`,
   `PREDICATE: C1_R30_PASS=true`, `exit=0` — a control that tests nothing
   passes the draft. `.ufo/evidence/round-30/v4/K9.stdout`: the same control on
   the frozen counter shows uniform `selftest_exit=0 verdict_pass=1`,
   `killed=0/13 … heldout_killed=0/12 … sealed_killed=0/6`,
   `PREDICATE: C1_R30_PASS=false` — refused. Neither counter was executed by
   this seat; both receipts are read as committed bytes (`v4/` is committed;
   no file under `/fast/scratch/hyaku/tameshi-r30a2` was opened, listed or
   searched).

## Which routed item has no criterion

Mapping: item 1 → 58; items 2 and 3 → 60; item 4 → 59; items 5(a), 5(b) → 61;
item 6 → 62; item 7's Mistake-1 falsifier part → 59. The uncovered content is:

- **Routed item 5(c)** — "the runtime should kill a seat's process group at its
  deadline" (BuildF6A kept writing 02:47Z → 03:03Z). Criterion 61 cites only
  5(a) and 5(b). Defensible if 5(c) is operator-owned runtime work, but then the
  criterion should say so explicitly rather than leave item 5 half-covered.
- **Item 7's other two carry-overs** — the S059 supersedes row (round 30's first
  SOURCES edit) and the runner `--regression` leg-sum defect (MutateLegSum) have
  no criteria. They are work assignments rather than policy, but 63 is the
  natural home for the S059 row (see fix below) and no criterion anywhere
  requires the leg-sum defect to be closed or re-tested.

## Exact wording fixes

58. After "holds no scored receipt for it.", add the refusal pointer:
    "The refusal holds are recorded in
    `.ufo/waves/round-29/res/ReviewControls.md` (CtlC1Shortcut named in both
    amendments; CtlC2Shortcut has no pre-data record)." Without it, "CtlC1Shortcut
    and CtlC2Shortcut were refused" rests on narrative alone.

59. "Falsifier: `.ufo/evidence/round-30/r29-mistake1-ordering.txt`." →
    "Falsifier: `.ufo/evidence/round-30/r29-mistake1-ordering.txt`, committed in
    the same lane commit as this criterion." The file is untracked today; a
    falsifier for a receipt-ordering rule must itself be committed (routed item 7
    already demanded this).

60. "lists 10 passing entries that failed the frozen binding on assembler shape
    alone" → "lists 10 entries excluded on assembler shape alone — assembler
    verdict normalization (report `executed-ok` vs entry `gap-minor`) and seat
    self-labels (`seat-not-registry-member:TameshiR29.Read08A`) — every report
    verdict a passing class". Matches the receipt's two recorded reason forms.

61. "and Read10C's report landed at the fleet root" → "and `lessons/round-29.md`
    Mistake 3 records Read10C's report written at the fleet root and moved
    byte-exact (sha256 `fafd4c36…`)". The fleet-root file is gone; as worded the
    clause can no longer be checked against bytes.

62. "while the only C2 head receipt (`c2-at-E.stdout`, `7a45f7b9`) reads
    `quote_located=0`" → "while the only C2 head receipt,
    `.ufo/evidence/round-29/c2-at-E.stdout` (measured rev `7a45f7b9`, committed
    at `9bb699ad`), reads `quote_located=0`, and no C2 receipt is committed for
    `6892c3ee`, `1a1e8b22` or `3c16b3a6`". A criterion about binding receipts to
    revisions must not itself blur landing commit with measured rev.

63. Add the missing Captured-by and the second falsifier pointer. After the rule,
    insert: "Captured by: QUALITY 56 as applied in round 29 — the widely-read
    edits landed at `9f3084bc` and dropped the monitor to 52/64
    (`.ufo/evidence/round-29/c1-at-A.stdout`) before the 12 re-reads were
    staffed; spot-check routed item 7 (the S059 supersedes row is round 30's
    first SOURCES edit)." And extend the falsifier: "… drops 64 → 33 credited
    sections (`rev=daa11583`), against 52 with the same three file edits and no
    runner edit (`.ufo/evidence/round-29/c1-at-A.stdout`, rev `9f3084bc`)."

Header. "Routed by `lessons/round-29-verifier-spotcheck.md` (routed items 1–6)"
→ "(routed items 1–7; 5(c) and item 7's S059 and MutateLegSum carry-overs are
work assignments, not criteria)" — criterion 59 already cites item 7, so the
header contradicts its own criteria as drafted.

## Proposed criterion 64 (round-30 lesson: a counter must not leak job labels to the program it judges; control K9)

    64. Round 30. A counter that drives a program under test gives every judged
    run the same observable identity: no run learns its job label, class or role
    (pristine, drop, insert, heldout, sealed, equivalent) from its working
    directory or its name, argv, environment, stdin, a file it can read, or the
    /proc entry of its parent; the counter may name jobs in its own output only
    after the last judged run has exited. Before data, a control keyed on job
    identity is scored against the frozen counter and must not pass. Captured
    by: control K9 against the round-30 v4 draft counter. Falsifier:
    `.ufo/evidence/round-30/v4/c1-measure-v4-draft.py` ran each `--selftest` in
    a directory named after its job (`st-<job>`), and
    `.ufo/evidence/round-30/v4/K9-on-draft.stdout` reads `PREDICATE:
    C1_R30_PASS=true` `exit=0` with every drop row `selftest_exit=1`, while the
    same control on the frozen counter (`.ufo/evidence/round-30/v4/K9.stdout`)
    reads `killed=0/13 … sealed_killed=0/6`, `PREDICATE: C1_R30_PASS=false`.

True (the draft leaked identity through cwd/dir name and cmdline; the frozen
counter removes every channel with an anonymous `mkdtemp` and a `bwrap
--unshare-all --clearenv` sandbox with an identical `/w` per job), checkable
(the K9 pair is committed bytes; scoring K9 against any future counter is one
run), able to fail (any counter that leaks identity lets the keyed control
pass). The final-output clause also covers the honest observation that both
counters print per-job `C1_R30_ROW` lines to their own stdout — harmless only
because the judged runs are captured and finished by then.

## Residual risk and verification gaps

- No counter was executed by this seat and the sealed set was never approached;
  the K9 and drift figures are read from committed receipt bytes only, and no
  sha256 of those receipts was cross-checked against a manifest.
- The draft-vs-frozen counter diff was inspected only around the selftest
  invocation; the rest of the counter logic was not audited (out of scope).
- `c1-at-A.stdout`, `spec-w1.json`, `select-receipt-w1.json` and
  `drift-sim-union4.txt` are committed; `r29-mistake1-ordering.txt` is not
  (finding above). Whether the round-30 wave commits land the criteria and this
  file together is the L1's integration step.
- LSP unavailable (no such device in this seat's inventory); all semantic
  claims rest on git-tree and byte checks listed above.
