# Round 97 — the committed battery is re-derivable (C1) and the guard edits are measured (C2)

Lane `tameshi`, round 97 (2026-11-08). Base `07e50d6d0142b21e8443b5417b8edc4d1dd76455`.
Claims frozen in `plans/round-97.plan.md` and `.ufo/waves/round-97/claims.json`:
C1 calibration (the 50-state battery verdict is a function of committed bytes) and
C2 operability (a guard-inertia matrix over the round-96 checker's own edits).

## Gate

Sources opened this round (fetched live by the L1 on 2026-11-08; snapshots under
`.ufo/evidence/round-97/sources/`). Located quotes use the lane renderer (script/style and
comments removed, each tag replaced by one space, entities unescaped, lines right-trimmed).
Word counts are `len(quote.split())`.

- S159 (re-opened, tier A) Wikipedia, "Mutation testing"
  `https://en.wikipedia.org/wiki/Mutation_testing`, fetched 2026-11-08 (HTTP date Sun,
  08 Nov 2026 14:31:52 GMT; 171636 B; snapshot `s159.html` sha256 `4b5a8374…`), line 762
  under the same renderer: "Equivalent mutants detection is one of the biggest obstacles
  to practical usage of mutation testing." (14 words) — grounds the `limit` class: an
  edit that changes no observable behaviour cannot be killed, so it is measured as
  identical rather than presumed inert or presumed observable.
- S006 (re-opened, tier A) shmutant README
  `https://github.com/BWBama85/shmutant`, fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026
  14:18:19 GMT; 281627 B; snapshot `s006.html` sha256 `55bb7196…`), lines 490-492 under the
  same renderer: "A row whose old literal occurs more than once in its target there is
  refused: the rewrite takes the first copy, which might not be the one the row means." The
  Gate quotes the located span "A row whose old literal occurs more than once in its target
  there is refused" (16 words) — grounds the `edit-ambiguous` refusal (a matrix that
  applies the first of two matches measures an edit it did not declare). `used-by` gains
  `corpus/lessons/round-97.md`.

Refused / not opened this round: **two**. A draft row for the Stryker "Equivalent
mutants" page was appended as S324 and withdrawn before the freeze: the URL already has a
row (S160), and the census flagged the duplicate (W04) — a duplicate-URL row is a registry
defect, never two rows for one source. S009's UCL Discovery page
`https://discovery.ucl.ac.uk/id/eprint/1499169/` was fetched twice on 2026-11-08 and both
responses were a Cloudflare challenge page (5 474 B, sha256 `106e61ab…`, no abstract text),
so the row was **not re-opened** and its `queued` status is unchanged; no verdict is
recorded from an unread page. Flip condition: a fetchable snapshot of the abstract (author
copy or repository PDF) opened with a located quote. The equivalent-mutant ground was
instead opened from S324, which is fetchable.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | **control fixture contamination**: the C1 forgery builder ran `git add -A` in its `commit()` after `git rm --cached pos-real.out`, so the "worktree-only" control silently re-staged the receipt it had just de-indexed; the run died `cmd failed: … commit` with empty output instead of measuring the forgery. | first `controls97.py` run: `cmd failed: /usr/bin/git -C …/c1-forge commit -qm drop pos-real from index` (the run stopped before writing any receipt). | the driver's own `want_code` map — a setup death is rc 1 with no line, visibly different from the expected `missing=1`, but only because the receipt writer records the exit code. | `commit(..., add=False)` for the de-index case; the final receipt `c1-forge-worktree-only.out` prints `missing=1`, rc 1. |
| M3 | **duplicate-URL row**: a new row (drafted S324) was written for a URL the registry already holds (S160, mined 2026-10-25); the within-scope duplicate is exactly the class CORPUS rule 2 refuses or supersedes, and it would have made two rows for one page with different digests. | the draft row's bytes (deleted before the commit; the fetched snapshot `equiv.html` sha256 `00082805…` stays under `.ufo/evidence/round-97/sources/`); census output `W04 S324 duplicate url stryker-mutator.io/…` before the withdrawal. | the census warning — but only after the row was written; no pre-write duplicate-URL check existed in the lane's row workflow. | the row was withdrawn and the ground re-opened from S159 (the definition-and-standing row), whose scope already holds it; `S324` never committed, so no supersede row is owed. A pre-append URL-scan is the missing check (routed below). |
| M2 | **evaluation-order truncation**: the exit-edit builder wrote `open(p, "w").write(re.sub(..., open(p).read(), 1))`; Python evaluates the write-mode `open` first, so the source read the file it had just truncated and wrote an empty receipt. | the next step's `assert "C1_R96_PASS=true" in body` failed on a 0-byte `pos-real.out`; the rejected bytes are gone with the scratch clone, the assert is the record. | the downstream assert, not the line itself — the control produced a *different* forgery (an empty receipt) that still exited nonzero, so an exit-only oracle would have accepted it. | read into a variable, then write; M1/M2 both repaired before the freeze (`CONTROLS97 states=14 matched=14`). |

| M4 | **control fixture contamination**: the three C1 body-edit forgeries were built one on top of the previous commit, so the `counter_sha=` edit stayed in the clone and the digest check fired first for the `exit=` and `C1_R96_PASS` cases — both receipts printed `MISMATCH(counter-sha)`, so those two paths were never exercised by the controls. | `.ufo/evidence/round-97/pre-freeze/c1-forge-{exit,payload}.out` in their first version (`BATTERY_ROW pos-real:MISMATCH(counter-sha)`); found independently by `w1/R97S1.md` and `w1/R97R1.md`. | the receipts' `BATTERY_ROW` field — the controls' exit code was right for the wrong reason, so only reading the finding field exposed it. | each forgery now resets to the pristine receipt at `a.rev` and edits exactly one field; the refreshed receipts print `MISMATCH(exit=7)` and `MISMATCH(exit=0)` and `CONTROLS97 states=16 matched=16`. Recorded as a fixture repair (plan A15), not a claim narrowing. |

The sweep for an inherited mistake: the round-96 spot-check's D-a and D-b are the two
defects this round turns into claims (C1 and C2); no other lane-authored defect was found
unrouted in `corpus/lessons/round-96-verifier-spotcheck.md` (D-c is the orchestrator's
dispatch-stall class, recorded there as "no lane action"; the inert risk note is C1's
subject).

## Registry changes

- Row added: **none**. A draft row for the Stryker "Equivalent mutants" page (appended as S324)
  was withdrawn before the freeze as a within-scope duplicate of S160 (census W04; M3).
- Rows re-opened this round: S159 and S006, with located quotes and byte-pinned snapshots
  (`.ufo/evidence/round-97/sources/s159.html`, `s006.html`).
- `used-by` changes, old → new: S159 `corpus/knowledge/r43-survivor-resolution-rule.md` →
  `… , corpus/lessons/round-97.md`; S006 `… corpus/lessons/round-76.md` →
  `… , corpus/lessons/round-97.md`. `status` and `recheck` cells unchanged.
- Census before and after: exit 0, rows 183 (A 165 · B 14 · C 4), mined 149 · queued 23 ·
  rejected 11 — unchanged.

## Measurements

Every number below is a line a committed receipt printed at the revision named.

- **C1 positive at the records revision `35db02e9`.**
  `.ufo/evidence/round-97/landing/c1-positive-1.out` reads
  `BATTERY states=50 matched=50 mismatched=0 missing=0`, rc 0; runs 2 and 3 are byte-identical
  (sha256 `54c6f667…`). `.ufo/evidence/round-97/repeat/c1-run-{1,2,3}.txt` are the same bytes.
- **C1 refusals.** `c1-forge-worktree-only.out` (`matched=49 mismatched=0 missing=1`, rc 1),
  `c1-forge-counter-sha.out` and `c1-forge-exit.out` and `c1-forge-payload.out`
  (`mismatched=1`, rc 1), `c1-forge-driver-sha.out` (`BATTERY_SETUP driver-sha-mismatch`, rc 2);
  a non-64-hex `--driver-sha` prints `BATTERY_SETUP driver-sha-invalid` (measured by R97R1 case
  13 and re-run at A4).
- **C1 selftest.** `c1-selftest.out`: `BATTERY_SELFTEST: 7/7 pass`, rc 0.
- **C2 positive at `35db02e9`.** `.ufo/evidence/round-97/landing/c2-positive-1.out` reads
  `GUARD_INERTIA rows=10 killed=8 limits=2 survived=0 unmet=0`, rc 0; runs 2 and 3 are
  byte-identical (sha256 `254536aa…`). The per-row lines show `rev-hex`, `rev-unresolvable`
  (token-only kill), `replace-refs`, `counter-sha`, `receipt-absent`, `no-flip`, `unknown-key`,
  `min-falsifiable` killed, and `verify-quiet`, `git-absolute` as measured limits.
- **C2 refusals.** `c2-forge-flipped-expect.out` (`survived=1`, rc 1), `c2-forge-noop.out`
  (`GUARD_SETUP edit-no-op`, rc 2), `c2-forge-manifest-subst.out`
  (`GUARD_SETUP manifest-sha-mismatch`, rc 2), `c2-forge-manifest-empty.out`
  (`GUARD_SETUP manifest-empty`, rc 2).
- **C2 selftest.** `c2-selftest.out`: `GUARD_INERTIA_SELFTEST: 7/7 pass`, rc 0.
- **Controls.** `CONTROLS97 states=16 matched=16 mismatched=0` (`.ufo/evidence/round-97/pre-freeze/`).
- **Census.** `census-before.txt` and the round-end run both exit 0, rows 183, mined 149 ·
  queued 23 · rejected 11, unchanged.
