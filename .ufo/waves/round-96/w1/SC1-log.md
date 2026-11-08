# SC1 — `LOG.md` draft, `## Round 96` entry (round 96)

**Seat:** R96SC1 (scribe). **Lane:** `tameshi`. **Mode:** read-only — nothing under `LOG.md`
was written; this file is a draft for the L1 to integrate.

**Read first.** The L1 landed a `## Round 96` entry at `9b89c68d` (`LOG.md`, after the
round-95 entry). This draft is written in the **established shape** the round-95 entry uses
— `Shape.`, one bullet per claim, `Motivating evidence.`, `Frontier.`, `Routed to round 97.` —
and it corrects three facts in the landed entry that this seat measured against committed
receipts. The corrections are marked inline and each carries its receipt.

**The established shape** (round-95 entry, `LOG.md:5094`): `## Round 95 (2026-11-08) — two
claims: …`, then a `- **Shape.**` bullet naming the wave, the seat roles and the count, the
base and the freeze commits, then `- **R95-C1 (axis) — …**` and `- **R95-C2 (axis) — …**`
bullets, then `- **Motivating evidence.**`, `- **Frontier.**`, `- **Routed to round 96.**`.
The landed round-96 entry keeps the content but drops the bullet markers and the bold
`**Shape.**` lead-in of the two preceding entries.

---

## Round 96 (2026-11-08) — two claims: the sealed audit's revision identity (calibration) and the hardened write path (operability)

- **Shape.** One v1 wave `w1`, 13 seats: executor 4, scribe 1, scout 1, reviewer 2, critic
  1, mutation-tester 1, sentinel 1, connector 1, revenger 1 (the roster read from
  `.ufo/waves/round-96/w1-dispatch.json` `taskCall.tasks`; the landed entry's role list
  matches it). Attack share 4/13 = 31 % by the §6 named set (reviewer×2, critic,
  mutation-tester) — **recorded against the named set this round**, closing D3, which asked
  for exactly that; 7/13 = 54 % including sentinel, connector and revenger. Base
  `c8de77f3de0fd4bf619ebe78fa0b28adaf320d3e`; freeze declarations `10d8fa5d`; frozen
  instruments `be6c22b6`; pre-data amendments A1-A9 `933df676`; records `8ed9c526`; landing
  receipts and QUALITY 173-174 `9b89c68d`; lesson and census after `ffb41c8f`. All seats
  settled, no dead seat.
- **R96-C1 (calibration) — the audit binds its verdict to a commit identity.** The
  disposition checker checks `--rev` as 40 hex, resolves it with
  `rev-parse --verify --quiet <rev>^{commit}`, prints the resolved id as `rev=` in
  `DISPOSITION_INSTRUMENT`, and refuses with `rev-not-a-commit-id` / `rev-unresolvable`
  before any read. Its git calls run under an explicit environment with a pinned `PATH` and
  `GIT=/usr/bin/git`, so a hostile `git` earlier in the inherited `PATH` cannot answer for
  it; the manifest blob is bound to the sha256 the round's claims file names
  (`manifest-sha-mismatch`). Positive at the records revision `8ed9c526`:
  `DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0`, exit 0
  (`.ufo/evidence/round-96/landing/c1-positive.out`); selftest `13/13 pass`, two cases now
  running the real main path under a poisoned `PATH` and with `--rev master`
  (`c2-selftest.out`).
- **R96-C2 (operability) — the write path is runnable and cannot be retargeted.**
  `make-pins96.py` refuses an empty (`lane-empty`), relative (`lane-not-absolute`), missing
  or toplevel-mismatched lane, refuses a symlink at `pins.json` (`pins-symlink-refused`) and
  at its temp name (`tmp-symlink-refused`), and writes atomically (temp + `fsync` +
  `os.replace`); the battery driver grades the receipt it wrote, refuses a symlinked
  `--outdir` or `--work`, and validates the `counter_sha=` line on what it grades. Battery
  `C1_CONTROLS states=50 matched=50 mismatches=0 missing=0`.
- **Motivating evidence.** The round-95 sentinel's F1-F8 and this round's own wave:
  R96R1 falsified two C1 sentences (the checker's default counter path and the dead
  `rev-unresolvable` token), R96C1 falsified five more atomic assertions (the unprinted
  rev, the no-op selftest cases, the before-rev citation), R96E4 and R96SN1 measured the
  driver's `--rev HEAD` contract break (44/50) and the planted-index-0 grade. All were
  amended pre-data as A1-A9 in `plans/round-96.plan.md`, each citing its artifact; no scored
  receipt existed before the amendments.
- **Frontier.** S320-S323 re-opened this round (round-96 snapshots, byte-identical bodies),
  one source candidate opened and **refused** (the GitHub REST API "Get a commit" page, on
  the revision-identity ground — `w1/R96S1.md` §4), census exit 0 before and after; no new
  row. QUALITY 173-174. Mistakes mined in `corpus/lessons/round-96.md`. **Residues this
  seat measured, for the L1:** (i) the S323 registry row's `anchor` cell still prints
  `line 2355`, which is blank under the lane renderer and where the sentence does not sit
  under the cell's own stated convention either — the sentence is at **2358-2359**; the
  exact 11-column old→new is in `w1/SC1-sources.append.md`. (ii) the lesson's Gate preamble
  names a renderer that does not produce its own cited line numbers — the numbers are the
  canonical lane renderer's, the stated convention is a different one, and the two differ by
  105-109 lines on these quotes (`w1/SC1-lesson.md` M4). (iii) two QUALITY-174 citations
  quote a receipt that does not carry the quoted string (`w1/SC1-quality.md`).
- **Routed to round 97.** R96SN1 F1 (a hand-written receipt set carrying the honest
  `counter_sha=` is still accepted — the counter_sha binds the receipt to the counter blob,
  not to a run) and F2 (an alternates file lets a lane with no commits of its own answer the
  reads) are the next frontier; the round-96 wording is narrowed to the properties the
  instrument enforces, and neither is claimed. D1 (the Gate line-number drift) is routed
  again in the form it now takes: the numbers were corrected in round 96 and the **renderer
  convention that contradicts them was not**, so the rule — not the arithmetic — is what
  still fails. D5 is closed: the round exercised rejection judgment on one candidate.

---

## The three corrections, with receipts

Each is a fact in the landed entry that this seat measured against a committed receipt and
found not to hold as stated.

**1. The "before-witness" is the round-94 checker, not the round-95 checker.** The landed
claims wording (`.ufo/waves/round-96/claims.json`, C1 `wording` and `before`) says *"the
round-95 checker at `6a2a1fdd`"*. `6a2a1fdd` is the **round-94** C2 checker: `git log -1
6a2a1fdd` reads *"round-94: C2 checker rev3 — read the round-94 manifest by default"*, and
`git ls-tree -r 6a2a1fdd | grep -c round-95` returns **0** — that tree carries no round-95
path at all. The round-95 checker is a different revision (`0685c358`, which does carry
`.ufo/evidence/round-95/conjunct-disposition-v95.py`), and the round-95 claims file itself
called `6a2a1fdd` "the **round-94** checker". The landed forge matrix agrees with the
revision, not with the label: it prints `v94_checker_rev=6a2a1fdd` and the four forged
receipts are named `forge-*.v94.out`, while the round-96 runs are named `forge-*.v95.out`
and carry the header `checker=v95` **while running the round-96 checker**
(`conjunct-disposition-v96.py` in their `command=` lines) — the `V95_` label residue this
seat was told to look for. Receipt: `.ufo/waves/round-96/w1/R96SC1-defect-check.txt` §DEFECT
3 and the label table in `.ufo/waves/round-96/w1/R96SC1-renderer-variants.txt` sibling
`.ufo/waves/round-96/w1/R96SC1-pin-state.txt`; the matrix itself is
`.ufo/evidence/round-96/landing/forge-matrix.txt`.

Consequence: the F1 before-witness is real — the round-94 checker does print `findings=0`
on the forged sets, which the matrix shows (`forge-handwritten v94 exit=0`) — but the
sentence naming *which* checker's green is a wrong label on a correct measurement. The
lesson's Measurements bullet repeats it ("round-95 checker exit 0"). Because the claims
wording is **frozen**, the L1's options are to amend the wording down to the enforceable
property (the plan's §Amendments mechanism) or to record it as a named limit.

**2. The hostile-PATH receipt does not contain the exit code the lesson reports.** The
landed lesson says the hostile-PATH run prints `… findings=17` **exit 1**. The committed
receipt `.ufo/evidence/round-96/landing/c1-hostile-path.out` prints the
`DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=17` line, and its 17
`DISPOSITION_FINDING receipt-absent-at-rev` lines (verified: `grep -c` → 17, and 17 total
`DISPOSITION_FINDING` lines) — but the file carries **no `exit=` line** and no `GIT=` /
`PATH` / shim token (`grep -c "exit=|GIT=|shim|PATH"` → 0). The exit code and the
"the shim is never the binary that answered (`GIT=/usr/bin/git`)" claim are properties of
the **instrument** (`conjunct-disposition-v96.py:81` pins `GIT = "/usr/bin/git"`), not
strings the receipt prints. The correct form names the instrument line for that property.

**3. The battery receipt pointer does not resolve.** The landed lesson cites
`.ufo/evidence/round-96/pre-freeze/controls/C1-summary.txt` for
`C1_CONTROLS states=50 matched=50 mismatches=0 missing=0`. That file **does not exist** at
`ffb41c8f` — `git ls-files .ufo/evidence/round-96/pre-freeze/controls/` lists the fifty
`<state>.out` receipts and no summary file, and the driver's own writer names it
`C1-summary.txt` in a scratch outdir, not in the committed tree. The **number** is
corroborated, and this seat re-derived it independently: re-grading all fifty committed
receipts with the driver's own `grade()` and its own expectations table gives
`C1_CONTROLS states=50 matched=50 mismatches=0 missing=0`
(`.ufo/waves/round-96/w1/R96SC1-regrade.txt`). The L1 should either land the summary file
or point at a receipt that exists; this seat's draft states the number with its
re-grade receipt as the pointer.
