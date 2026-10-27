# Round 10 lessons — tameshi-shokunin (2026-10-14)
## The runbook lesson: cold-readable documents as the handoff medium

Written 2026-10-14 by lane **T11-2** (tameshi round 11, seat 2) — lessons land
one wave late, the sibling lane's round-9 precedent; this is the register's
first entry (`corpus/lessons/` measured empty through round 10,
`service-standing-state.md` §1 corpus state). All reads read-only; this file
is the lane's only write; scratch `/tmp/w11-t11-2-lesson/` (`sc1-pins.txt`,
`sc2-sc3.txt`). Every value below is re-derived from the committed tree at
HEAD `606716f` ("probation round 10 (training r9): see LOG",
2026-10-14T18:28:23 −03) or pinned to the revision named; a reader on a
differing revision re-resolves rather than trusts (`SKILL.md:1269-1270`).

Anchors: **O** observation · **I** inference · **U** unknown.

**Revision pins at this write (2026-10-14T21:36Z; commands `sha256sum` ·
`wc -l` · `git show`):**

| cell | value |
|---|---|
| `corpus/knowledge/operator-runbook.md` | `e1e349b69d798acb…` / 511 `wc -l` / 31 416 B — equals the blob at `606716f` (SC-A) |
| `corpus/knowledge/service-standing-state.md` | `d326c1a4d61c9705…` / 242 / 17 513 B |
| `tools/mutate-and-run.sh` | `75ed934dc86360f5…` / 1 642 / 77 904 B (r10-2) |
| `reports/r10-aud-t10.md` | `84837d2cca2e2962…` / 228 / 16 542 B |
| `plans/round-10-record-draft.md` | `8020f9bda4206469…` / 469 |
| `plans/round-10.plan.md` | `d130596ac8bc7e91…` / 254 |
| `SKILL.md` (round-10 revision inside `606716f`) | `ff56681441aec2ea…` / 1 362; a concurrent round-11 lane held it modified during this write (` M`, 1 461 L) — re-resolve |
| round-10 commit | `606716f`, 9 files, +2 212/−61; `LOG.md:309`; `SCORECARD.md:23` |

## What round 10 was (measured)

Plan `plans/round-10.plan.md` (`d130596ac8bc7e91…`): axis move **operability,
terminal** — "the closeout: the ten rounds' product is handed to the operator
as one runbook" (`:38`), three ordered legs — note · execution · sufficiency
(`:48-107`). Realized, per the record draft + the audit + the commit:

1. **The runbook landed — relocated.** `corpus/knowledge/operator-runbook.md`
   (lane T10-1; `e1e349b6…`, 511 `wc -l` / 31 416 B). The plan's landing shape
   was `HANDOFF.md` at the repo root (`:48`), with relocation allowed if the
   coverage row moves with it; the landed path is the runbook name (record
   draft `:40-51`).
2. **Executed by its author.** Tick 20:52:19Z (`current=4 stale=2 drift=0`,
   tool `held` at `cf41efaa…`), `--selftest` 67/67 rc 0, `--regression`
   `cases=4 passed=4` (`REGRESSION_DATE 20:51:32Z`), append drill on a scratch
   copy (pre-append 36 169 B byte-identical; real ledger sha unchanged),
   reader-side drift falsifier — receipts in runbook §9 (`:438-460`); errata
   **ER-R1/ER-R2** record the tool moving mid-window and name the T2 remedy
   (`:486-512`).
3. **The round-8 4-vs-6 leg cut resolved as an embedding, not a re-cut.** Tool
   r10-2 `75ed934d…` (1 642 L, +361/−60): cases 5/6 embedded as legs 5/6; the
   checklist leg's control first read `SETUP` (exit 126 — the materialized
   blob lacked the exec bit) then fixed by mirroring the blob mode; six-leg
   `--regression` `PASS (cases=6 passed=6)` recorded by four independent lanes
   (T10-2 21:00:24Z · AUD-T10 21:01:53Z · T10-4 21:02:39Z · VER-T10
   21:05:10Z; record draft `:78-92`).
4. **Companions.** The boundary table `service-standing-state.md` (T10-3;
   `d326c1a4…`), the `SKILL.md` round-10 section (T10-4, +94/−1, heading at
   `:1272` at the `ff566814…` revision), the audit `reports/r10-aud-t10.md`
   (12-row verdict table), PREP-T11's `plans/round-11.plan.md`.

**The cold reads.** AUD-T10 followed the runbook's text alone
(declared-contamination read): P1 the operator loop **SUFFICIENT (latitude)**,
P2 the append drill **SUFFICIENT (latitude)** + one `ADAPTED` cell, with every
latitude point named (`r10-aud-t10.md:57-99`, `:172-173`). VER-T10, the
designated cold-reader seat, executed the loop 21:04:58–21:06:47Z (tool
`75ed934d…` before=after, selftest rc 0, six-leg regression
`PASS (cases=6 passed=6)` 21:05:10Z) but **no report landed at close** — the
sufficiency table and falsifier pair stay unreported (record draft `:64-77`).

## The lesson — cold-readable documents as the handoff medium

### The measured shape of the runbook [O]

- Single operator-facing document; **adds no gate measurement of its own**;
  every line restates an anchored source; "where this runbook and an anchored
  source diverge, the anchored source governs" (runbook `:7-11`).
- Executed receipts in §9; everything not executed is "named rather than
  assumed" there — including, at its own write, the fresh-executor
  sufficiency test (`:454-460`).
- §6's own rule: the tick "is a timestamped observation, re-run at the next
  boundary — never carried as a standing claim" (`:302-303`).
- Errata append-only below the fixed §0–§10 (`:481-512`); two entries at this
  write (`grep -c '^\*\*ER-R'` → 2, SC-B).

### Method lessons

1. **The name is part of the interface — a relocation costs every reader whose
   frame names the old name [O].** The plan's landing shape was root
   `HANDOFF.md` (`plans/round-10.plan.md:48`); the artifact landed at
   `corpus/knowledge/operator-runbook.md`. VER-T10's poll for a `*handoff*`
   file ran 21 iterations, all `absent` — "the poll pattern never matches it"
   (record draft `:65-67`); T10-4's `HANDOFF.md` poll read `ABSENT` ×30
   samples (`:324`); the audit's row 1 carries the note ("the T10-4/VER-T10
   polls watch for `HANDOFF.md` / `*handoff*` and will not see this path",
   `r10-aud-t10.md:171`). [I] a cold reader's first step is *finding* the
   artifact; a plan-allowed relocation still spends the reader's trust in the
   plan's name, and a poll reporting "not landed" is a name mismatch, not an
   absence of work.
2. **A rendering goes stale by construction; pointers + the anchored-source
   rule are what make that safe [O].** The frozen runbook says four legs /
   "cases 5/6 are **not embedded**" (`:173`, `:374-375`); the tool that ships
   in the same commit (`75ed934d…`, r10-2) carries six legs
   (`grep` hits at tool `:80`, `:144`, `:522`, `:1566`; SC-B). AUD-T10's
   row 7: **STALE at the landed revision**; ER-R1/R2 record the move but
   predate the landing; neither file smoothed it (`r10-aud-t10.md:146-156`,
   `:177`). [I] a handoff document is a rendering at a revision; its safety
   property is that the reader is never asked to trust the rendering over the
   source — the divergence is the finding, not a repair.
3. **Timestamped readings are the only honest form for moving substrates [O].**
   The instrument moved nine times inside the audit window (`cf41efaa…` → … →
   `75ed934d…`, `r10-aud-t10.md:28-31`); the runbook's receipts stay tied to
   the executed revision `cf41efaa…`; ER-R1/R2 are timestamped readings; the
   audit's 21:03:26Z re-read shows `4 · 1 · 1` (tsukuroi's own writer moved a
   cell to `stale + drift`) — "a moving file is never re-interpreted; both
   readings stand at their timestamps" (`:161-165`).
4. **The cold-read proof is a re-run, and its verdicts carry their friction
   [O].** AUD-T10 re-ran both procedures *from the runbook alone*; every
   command ran as written; two latitude points and one gap were named
   precisely — `REV` is not in §3 and sends the reader one section away; the
   drift map's wording is looser than ER-3's path-scoped porcelain command;
   the compound `stale + drift` reading is not spelled out (`:66-86`). [I]
   "cold-readable" measured means *executable at the anchored sources, with
   the friction named* — not "understandable on a read-through".
5. **A cold-read verdict without its contamination statement is not usable
   [O].** The audit's read is *declared-contamination* ("each 'latitude'
   verdict is a lower bound on a true stranger's friction", `:48-55`); the
   independent naive-executor seat (VER-T10) executed but its sufficiency
   table was unreported at close (record draft `:64-77`; audit U6 `:221-223`).
   [I] the report is part of the test — a pass that exists only in scratch
   cannot be quoted, and only an uncontaminated seat's pass bounds the
   document's real friction.
6. **The reader's instruments can manufacture false readings — record, do not
   smooth [O].** VER-T10's per-case `reading:` classifier compared an 8-char
   pin against 16-char shas: five `current` cells printed `stale` while the
   printed shas show live = HEAD blob = pin; recorded, "do not quote those
   `reading:` lines as readings" (record draft `:71-74`). [I] the cold-read
   artifact itself is evidence that needs adjudication against the anchored
   sources before it becomes a claim.
7. **Append-only errata are the mechanism, not a formality [O].** ER-R1
   (~20:58Z) and ER-R2 (~21:00Z) append below the frozen sections; each is a
   timestamped tool reading and each holds the unchanged remedy — "**T2 is
   the fix** — when the edit lands, re-run `--selftest` and `--regression`
   under the new revision and record both pins"; no number in the document is
   re-interpreted (`:486-512`). The runbook still carries exactly two errata
   at this write; whether an ER-R3 re-stamps the landed r10-2 is the author
   lane's call (audit U2 `:209-212`).
8. **The medium is a set, not a file [O].** The boundary table's own
   definition: "A handoff is not a file move: it is the set of conditions
   under which a claim becomes citable" — 16 conditions in four groups (gate
   in · result out · standing record · stop conditions), each anchored
   (`service-standing-state.md:80-150`; count per record draft `:95`).
   Its visibility finding, measured: no fleet document indexes these
   artifacts (fleet `CORPUS.md`/`AXES.md`/`LEARNING.md`/`LOG.md`/`PROTOCOL.md`/
   `README.md` name tameshi 0 times each) and cross-repo mentions are
   asymmetric — tsukuroi 12 files · mado 19 · kumitate 0 · kagi 0
   (`service-standing-state.md:34-40`). [I] the runbook tells the operator
   *how*; the boundary table tells a lane *what it may cite*; a handoff that
   ships only the how leaves the citation rules unstated.
9. **The document was verified with the same discipline as code [O].**
   AUD-T10's 12-row table: CONFIRMED ×8 · `SUFFICIENT (latitude)` ×2 · one
   STALE row (the finding) · one AMBIGUOUS row (`held|moved` — two legitimate
   anchors disagree, `:181`) · read-only CONFIRMED; plus a 6/6 independent
   leg-check (`LEGCHECK: PASS (6/6 legs clean)`, `:126-129`) and the
   runbook's own receipts reproduced at their own revision (67/67 and
   `cases=4` replayed at `cf41efaa…`, `:140-145`). Its three spot-checks are
   re-runnable (`:184-201`). [I] a handoff artifact earns trust by the same
   battery as code: pinned, re-derived, adversarially re-run, findings public.

### Named limits carried at the handoff [O] (recorded, not converted)

- the two `stale` gates' re-sweeps: not landed — ledger byte-identical
  `2f25c51e…` all window, no ER-5 (record draft `:356-358`);
- the fresh-executor sufficiency table: unreported (`reports/r10-ver-t10.md`
  absent; VER-T10 executed the loop);
- `corpus/README.md` coverage rows: unchanged (20 L; T10-3 measured 9 rows
  covering 6 of 16 knowledge notes);
- the ledger's §1 embedding text ("cases 1 and 2 only") not yet amended for
  the six-leg registry (named in the SKILL section as the ledger owner's
  follow-on; ER-2 `:281` predates);
- audit row 11 AMBIGUOUS: the `held|moved` map should name its anchor;
- [U] whether the operator adopts and runs the schedule; whether an ER-R3
  lands; whether round 11's close re-runs the cold read with an
  uncontaminated (naive) seat.

## Gate

- **Candidates:** the runbook (T10-1); the boundary table (T10-3); tool r10-2
  + the six-leg embedding (T10-2); the `SKILL.md` round-10 section (T10-4);
  the audit (AUD-T10); the record draft (SCR-T10); the round-11 plan
  (PREP-T11); the `LOG.md`/`SCORECARD.md` rows.
- **Admitted:** all of the above, committed as `606716f` (9 files,
  +2 212/−61). The round's move: operability — the operator's single entry
  point, executed and cold-read (`SCORECARD.md:23`: "the operator runbook
  (511 lines, cold-readable, exercised receipts)").
- **Rejected / deferred, with reasons:** the leg cut as a re-cut (resolved as
  an embedding — the round-8 names stay); the two `stale` re-sweeps (open
  work, T1 — recorded, never manufactured); the fresh-executor report
  (executed, unreported — not counted as landed); the `HANDOFF.md` name (a
  relocation the plan allows, with a measured discovery cost); the ER-R3
  re-stamp (author's call); the coverage rows and the ledger six-leg row
  (named debt); audit U1–U7 (unknowns, not converted).
- **Spot-check (this lesson, non-author of every round-10 artifact)** — SC-A,
  SC-B, SC-C below, all three re-run clean at this write.
- **Falsifier:** a runbook line never run; a receipt quoted without its
  revision; a reading quoted without its timestamp; a cold-read verdict
  without its contamination statement or with its friction unnamed; a pass
  that exists only in scratch; a rendering divergence smoothed instead of
  recorded; a lesson file without a `## Gate`.
- **Carried debt out of round 10** (all to round 11's closeout, none
  absorbed): the two `stale` re-sweeps · the fresh-executor table · the
  coverage rows · the ledger six-leg row · the ER-R3 decision · the
  cold-read re-run with an uncontaminated seat · audit U1–U7 · the runbook's
  §2/§3/§7 stale lines (anchored source governs until re-stamped or edited).

## Spot-checks (this write; three, re-runnable)

- **SC-A — the runbook's landing pin.** `sha256sum corpus/knowledge/
  operator-runbook.md` → `e1e349b69d798acb…`; `wc -l` → 511;
  `git show 606716f:corpus/knowledge/operator-runbook.md | sha256sum` →
  identical (committed blob = measured file); `grep -c '^\*\*ER-R'` → 2.
  Every runbook line cite in this lesson is at that revision.
- **SC-B — the stale-rendering finding re-derived from the landed bytes.**
  `grep -n 'cases 5/6\|not embedded\|four legs' corpus/knowledge/
  operator-runbook.md` → `:173`, `:374-375`, `:458`; `grep -n 'r10-2' tools/
  mutate-and-run.sh` → the six-leg registry (`:80`, `:144`, `:522`, `:1566`).
  The audit's row 7 stands on this write's bytes.
- **SC-C — the relocation / name evidence.** `git show 606716f:plans/
  round-10.plan.md | grep -n HANDOFF` → `:48` (proposed root `HANDOFF.md`);
  `git show 606716f --stat` → the landed `corpus/knowledge/operator-runbook.md`
  (+512) and `service-standing-state.md` (+243); `grep -n 'poll pattern'
  plans/round-10-record-draft.md` → `:66`.

## Re-run commands

```sh
cd <fleet-root>/tameshi-shokunin
sha256sum corpus/knowledge/operator-runbook.md              # e1e349b6… / 511 wc -l
grep -c '^\*\*ER-R' corpus/knowledge/operator-runbook.md    # 2 at this write
grep -n 'cases 5/6\|not embedded' corpus/knowledge/operator-runbook.md   # the stale lines
grep -n 'r10-2' tools/mutate-and-run.sh | head              # the anchored source's six-leg cut
git show 606716f --stat | head -20                          # the 9-file round-10 landing
git log -1 --format='%h %cI %s'                             # 606716f / 2026-10-14T18:28:23-03:00
grep -n 'poll pattern' plans/round-10-record-draft.md       # VER-T10's *handoff* poll
```

## Errata (append-only)

(none yet — new entries go below this line, never edits above per
`corpus/QUALITY.md:7`.)