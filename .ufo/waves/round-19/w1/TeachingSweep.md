# TeachingSweep — operator-*.md lessons vs round-19 receipt correction (advisory)

Seat: TameshiR19-2.TeachingSweep, 2026-10-21. Scope: locate `operator-*.md`
teaching under `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, report any
teaching relevant to receipt correction (C1's five routed R18 defects) not yet
reflected in the round-19 landed work. Read-only; this file is the only write.
No installs, no tests/builds, no git writes.

## 1. Method (commands and observed outcomes)

- `glob /home/vgpnk/Projects/shokunin/tameshi-shokunin/**/operator-*.md` →
  2 matches: `corpus/knowledge/operator-runbook.md` and
  `.ufo/waves/round-18/staged/corpus/knowledge/operator-runbook.md` (round-18
  staged tree copy). Re-run with `gitignore:false` → same 2; no gitignored
  operator file exists.
- `glob …/corpus/lessons` → 18 files, all `round-*.md`; **zero**
  `operator-*.md` under `corpus/lessons`. The round-19 lesson sentence
  "No operator teaching files were found by
  `glob …/corpus/lessons/operator-*.md` (2026-10-21: no matches)"
  (`corpus/lessons/round-19.md`) is accurate for its stated path.
- `glob …/.ufo/waves/round-19/**` → spec/plan/run/record/assignments json +
  `w1/swarm-registry.json` only; no operator teaching file.
- Read: runbook in full (`:1-300`, `:301-516`, `:raw:516`), `round-19.md`,
  `round-18-verifier-spotcheck.md` §5, `corpus/QUALITY.md`,
  `.ufo/evidence/round-19/contract.json`.

## 2. Inventory [O]

The lane's single operator teaching document is
`corpus/knowledge/operator-runbook.md` (516 lines, round-10 vintage, errata
through ER-R1/R2 2026-10-14, ER-R3 2026-10-20, ER-jj2 2026-10-20). The staged
copy is the same document in the frozen round-18 tree — no distinct teaching.
The round-19 lesson's absence sentence is true but path-scoped; read lane-wide
it would understate the corpus (the runbook lives in `corpus/knowledge/`).

## 3. Teaching → reflection map (receipt-correction relevant items)

Every runbook teaching I could tie to the five R18 defect classes is already
reflected in round-19's landed lesson, gate, or QUALITY criteria. Per item,
with basis:

| Runbook teaching (location) | Reflected where |
|---|---|
| Corrections are appended errata; §1–§4 never edited; in-place substitution "the append-only rule does not allow"; known miss "not edited in place" (runbook header; ER-jj2, line 516) | QUALITY 35 names "operator-runbook substitutions named by an appended ER-R3 but made in place"; round-19 gate rejects overwriting `checks.json`; "the failed `--selftest` receipt remains history" (`round-19.md`) |
| Line anchors go stale; cite by function name, not line (ER-jj2; ER-R3) | QUALITY 34 (function/symbol anchoring, `detect_branch` moved, five ER-jj/R3 notes cited as captured-by) |
| Receipts stay tied to the executed revision; drift recorded, "no number is re-interpreted", both pins recorded (ER-R1/ER-R2; §6 tick "timestamped observation … never carried as a standing claim") | Round-19 bounds: "Every row is revision- and input-digest-bound"; "Every later count names its measured commit"; invariant "no required-command coverage claim" (`round-19.md`; `contract.json` invariants) |
| A re-run presented as a rate is a directed repair, not an independent rate (§5 row i; `fleet-kill-rate-ledger.md:35-36`) | R18-5 fix: "repairs missing evidence now, not original timeliness"; "late repair disclosed rather than dated back" (`round-19.md`) |
| "SETUP is not a verdict … fix the environment, never re-interpret"; exit map incl. 64=usage; "read the block, not the last line" (§2 exit map; §7 receipt discipline) | QUALITY 15 ("A setup error with the expected exit code is not proof"), QUALITY 17 ("Explicitly classify every nonzero exit, including usage"); R18-4 fix binds argv/tool/runner hashes + stdout/stderr digests, supersedes without erasing (`round-19.md`) |
| Rendering diverges from anchored source → the divergence is the finding, never smoothed (runbook preamble, `SKILL.md:1249-1254`) | R18-1/R18-2 fixes: explicit errata naming the stale header line; mistakes table row 1 records QUALITY 35's gap ("did not require naming the stale metadata field") → QUALITY 37 |
| Quotable-table conventions: pre-register expectation; record composition beside the rate (§4 close) | Frozen population/invariants pre-landed at `78b99dd` in `contract.json`; R18-3 fix distinguishes rows vs cells (five deleted lines, S008 two cells) |
| Honest non-execution: "named rather than assumed" (§9) | Round-19 bounds: text predicates "not that arbitrary prose is semantically true or that the original author was authenticated"; no fresh cold-read claimed |

## 4. Findings

1. **No unreflected receipt-correction teaching found.** Every operator-runbook
   rule that bears on the five routed defect classes is already embodied in
   QUALITY 15/17/26/34/35 (36) and the round-19 lesson's gate, mistakes table
   and bounds. Inference: the round-19 repairs were designed against the same
   corpus the runbook restates, so nothing new to absorb without expanding C1's
   frozen population — which the contract forbids. Confidence: high for the
   runbook's §2/§5–§7/§9 and all four errata; residual unknown: teachings
   inside `SKILL.md`/`service-limits.md` beyond what the runbook restates were
   out of my assignment's glob scope (the runbook is "never a second home" —
   the anchored sources govern, so a sweep of those sources is a separate task,
   not an absence claim here).
2. **Naming nuance (advisory, not a sixth defect).** `corpus/lessons/round-19.md`
   states no operator teaching files were found, scoped to `corpus/lessons/`.
   The only operator teaching file lives at `corpus/knowledge/operator-runbook.md`
   (plus its round-18 staged copy). A future reader of that sentence lane-wide
   could wrongly conclude no operator teaching exists. Any correction belongs to
   a future round's append-only erratum; it is outside the frozen five-item C1
   population and I claim no calibration credit from it.
3. **No invented absences.** `corpus/lessons` truly holds zero `operator-*.md`
   (verified twice, with and without gitignore). The two-file inventory in §2
   is complete under the lane root.

## 5. Sources & bounds

Sources opened: paths in §1; quotes kept under 25 words with location; all
observations dated 2026-10-21 at the working tree (uncommitted round-19 wave
state observed as-is; I did not resolve or pin a revision for the lesson file
beyond the wave files read). [I] marks on the reflection judgments in §3;
everything else is [O] from the reads listed. Unknowns: none blocking this
seat's question.
