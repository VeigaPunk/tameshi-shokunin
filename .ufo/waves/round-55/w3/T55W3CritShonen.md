# T55W3CritShonen — SHONEN at C0 (critic, calibration)

- **Seat:** T55W3CritShonen, round 55 wave 3, critic. Milestone: `SHONEN at C0`; judged axis:
  calibration.
- **Candidate:** `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (content commit C0). Lane HEAD when this
  seat ran was `4f7a704` (freeze amendments 8–9); every read below is on
  `/fast/scratch/hyaku/tameshi-r55/T55W3CritShonen/c0`, a `git clone --shared` checked out at C0
  (`git rev-parse HEAD` → `9cf0146…`, `--show-toplevel` → the scratch dir).
- **Objects attacked:** (a) the four `SHONEN.md` boxes and their pointers, (b) the same four rows as
  the round-55 report will carry them, (c) the mark/gate authority that would be needed to move a
  box, (d) the C1 counter's coverage of this surface.
- **`SHONEN.md` is untouched by this round:** sha256 `55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09`
  at base `0a2010ac` and at C0; `git log 0a2010ac..9cf0146 -- SHONEN.md reports/round-1-calibration.md
  .ufo/evidence/round-21/coldread/ledger.json` is empty (receipt 01). The checklist this round
  attacks is the one it inherited.

## Verdict (one line per box)

| Box | Pointer | Resolves at C0? | States the box claim? | Verdict |
|---|---|---|---|---|
| 1 | `reports/round-1-calibration.md#box-1` | yes (file + `## box-1` at line 71) | yes, but one of its three witnesses is stale | **minor defect**: `SKILL.md:466–495` no longer covers the checklist it names |
| 2 | `reports/round-1-calibration.md#box-2` | yes (`## box-2` at 105) | yes (`LOG.md:277–298` matches, incl. `:292–298`) | clean |
| 3 | `.ufo/evidence/round-21/coldread/ledger.json` | file exists only — no pin, no anchor, no entry id | **no**: its own `provenance` disclaims the property, and no entry states it | **understated** pointer; claim `[~]` still right |
| 4 | `reports/round-1-calibration.md#box-4` | yes (`## box-4` at 176) | yes, except a stale count | **minor defect**: "six cross-lane cases" → ten legs at C0 |

**Upgrade: none is legitimate in-round.** **Understated: box 3.**

## Mark conformance (sweep, nothing found)

The canonical seed is `PROTOCOL.md:441–448`; the marks rule is `PROTOCOL.md:450–451`. Normalising the
box character and `<name>`, the lane file is byte-identical to the seed (8 lines), carries exactly
four boxes, all `[~]`, one indented evidence line each, no added or removed box, no extra prose.

```
$ cd tameshi-shokunin && python3 - <<'PY'  … (normalise box char + <name>, compare to seed)
seed lines: 8 lane lines: 8 IDENTICAL
boxes: ['- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources',
        '- [~] At least one end-to-end domain task executed and logged in LOG.md',
        '- [~] Instructions executable by an agent without oral context',
        '- [~] No cross-domain bleed (PROVINCE.md still accurate)']
```
Receipt: `T55W3CritShonen-receipts/06-shonen-canonical-diff.txt`.

## Box 1 — `reports/round-1-calibration.md#box-1`

Resolution: the file exists at C0 and `## box-1` is at line 71 (`grep -n '^## box-'` → 71/105/132/176,
receipt 11). The section states the claim the box makes: a gate-shape decision table, a fail-closed
error-pattern taxonomy, a no-permissiveness checklist, three spot-checked cited notes, plus its own
unknowns and the reason it stayed `[~]`.

Witness check at C0 (receipts 02, 03, 08):

| Witness the section cites | C0 bytes inside the cited range | |
|---|---|---|
| `SKILL.md:58–92` — gate-shape decision table | `## Gate-shape decision table` at 73; Hermetic/Live/Audit-lane rows at 77–79; rules 83–89 | resolves |
| `SKILL.md:466–495` — "a no-permissiveness checklist" | heading now at **481**; items 1–3 at 486–495; **items 4–8 at 496–510 are outside the range**; 466–480 is the preceding mutation-comparison section | **stale** |
| `SKILL.md:497–525` — fail-closed arm taxonomy | taxonomy heading at 512; SETUP / Malformed / POLICY / Zero-work / Deferral rows at 518–522 | resolves |

Drift measured, not inferred: the recipe heading stood at 466 on the audit's baseline blob
`284ab0f0`, at 477 on base `0a2010ac`, and at 481 at C0; the taxonomy moved 497 → 508 → 512
(receipt 08). So at base the cited `466–495` still covered items 1–4 (item 4 at 492–495); C0's own
SKILL edit — `7 insertions(+), 3 deletions(-)`, net +4 lines above line 69 — cost the range its
fourth item and pushed four more unrelated lines inside it. The drift is inherited; **this round's
C0 edit widened it**.

Smallest safe correction (not mine to apply): re-anchor the checklist witness to `SKILL.md:481–510`,
or cite the heading name instead of a range. It is the same stale-anchor class round 54's fix pass
repaired in twenty-five places; it survived because round 54's own hunks were line-count preserving
while earlier rounds' insertions above line 466 were not.

## Box 2 — `reports/round-1-calibration.md#box-2`

Resolves and states the claim. `LOG.md:277–298` at C0 carries exactly what the box-2 section says:
second kill-rate on a bash gate (278–282), the first in-tree tool with `selftest 24/24` (281–282),
and the round's carried unknowns at `:292–298` (`Carried to round 4 (recommendations, not absorbed): …`,
receipt 04). The range also contains the now-superseded `[x]` sentences (283–291); the box-2 section
and `## supersession of historical independence claims` address them, so no false statement reaches
the box. No finding.

## Box 3 — `.ufo/evidence/round-21/coldread/ledger.json` (the understated box)

**It resolves only as file existence.** At C0 the pointer is 10 572 761 bytes, sha256
`24dbe99a57880705313a8ddc05ddcdc05c57754903822912c0dbd7480499a5c7`, with 591 entries over 65
headings; 30 commits on this history write it (101 across all refs), the last at `7fa9a5e` (round-54)
— while its path still says `round-21` and its own `round21_provenance.prefix_retained` is 199. The
box gives it no revision pin, no entry id, no anchor, so the bytes a reader meets are whatever the
last commit left there.

```
$ git show 9cf0146:.ufo/evidence/round-21/coldread/ledger.json | wc -c ; ... | sha256sum
10572761
24dbe99a57880705313a8ddc05ddcdc05c57754903822912c0dbd7480499a5c7  -
$ git log --oneline -- <path> | wc -l ; git log --all --oneline -- <path> | wc -l
30
101
$ last commit: 7fa9a5e round-54: re-key of all 23 headings …
ledger state at C0: entries 591, headings 65,
  last-read verdicts {'gap-minor': 53, 'executed-ok': 2, 'verified-record': 10},
  entries with blocking_gaps>0: 4, wrong-expectation entries: 36
  provenance: "… not blind/independent cold-read, recipe execution or required-command coverage."
```
Receipt: `T55W3CritShonen-receipts/09-box3-ledger-state.txt`.

**It does not state the box claim.** Box 3 claims "instructions executable by an agent without oral
context"; the artifact's own `provenance` string disclaims exactly that ("not blind/independent
cold-read"), and no entry, index or summary says the lane's instructions are executable without oral
context. Its current state is also not what the bracket implies: 53 of 65 headings carry a last-read
`gap-minor` (the four historical `blocking_gaps` entries and 36 `wrong-expectation` entries are all
superseded by a later read of the same heading — 0 headings' last read is blocking), and the
round-54 read routed 25 findings. Supporting the bracket therefore needs a last-entry-per-heading
rule that the box never states, and the bracket is silent about the gaps.

**Why it is understated.** The lane's monitor is materially stronger than one round-21-named file:
the round-54 deciding receipts print `COLDREAD_PRECHECK floor=d33053f7552d floor_credited=57
cand=c21081008adb cand_credited=64 lost=0 ok` (`.ufo/evidence/round-54/after/coldread-precheck.stdout`
and `after/c1.stdout:1`), and this round binds 18 fresh section reads at C0 — the very instrument
box 3 describes. The one-line pointer names neither, so the report's `[~]` row cites an unpinned
591-entry aggregate where a two-line pinned statement of the monitor and its 64/64 credit is
available.

Smallest safe correction: keep `[~]`; replace the evidence line with a pinned artifact that states
the monitor and its result (e.g. the round-54 `coldread-precheck.stdout` plus this round's reader
set), and state the current last-read gap count so the bracket stops reading as a clean bill.

## Box 4 — `reports/round-1-calibration.md#box-4`

Resolves and states the claim, except one count. `PROVINCE.md:3–18` at C0 matches the section's
domain/owns/refuses frame; `corpus/knowledge/mutation-case-kagi-census.md:4–7` matches the
read-only/no-write discipline; the external pointer
`.ufo/waves/shokunin12h-20261014-p1-repair/members/FleetBoundaryConnector.md:39,42,114` resolves at
fleet commit `cb3c1039297b6dd112bb745bf8ba771e09910347` (row 16 names `tameshi-shokunin/PROVINCE.md:6-18`;
line 42 the clean splits; line 114 "tameshi does not edit sibling gates").

The stale sentence: the section says "`tools/mutate-and-run.sh:84–89` records the **six** cross-lane
cases as *recorded pins* only". At C0 the same lines read
`# --regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten)`
and the list beneath them is **ten** legs (88–97), with the selftest asserting "all ten legs pass"
(line 2088). Record-vs-tree mismatch; inherited, and not one of `ER-R54-1…10`.

```
$ git show 9cf0146:tools/mutate-and-run.sh | sed -n '84,97p'
# --regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten) …
#   js-kimi-census … , bash-surface-census … , … , bash-drift-pins …
$ count of leg rows 84-97: 10
```
Receipt: `T55W3CritShonen-receipts/10-box4-witness.txt`. Smallest safe correction: "six" → "ten" in
that sentence (the sentence's substance — recorded pins, sibling repos read as blobs — is still true).

## Upgrade question: none, and why

`PROTOCOL.md:59–72` is the authority: a box is checked only by "a reviewer who did not author the
round's changes — a fresh lane or integrator review, never self-attestation; **a subagent the lane
dispatched is still the lane**", and "only a non-author `<id>` may write `[x]`". Every seat in this
round — including the 18 re-key readers, the reviewers and this critic — is a subagent the L1
dispatched, so any `[x]` here counts as `[~]` for the gate. No non-author verifier exists in-round;
the smallest upgrade available is therefore **none**. If an outside verifier did exist, box 3 would
be first (the 18 fresh reads at C0 and the 64/64 credit exercise exactly its claim), box 1 second
(table + error-pattern list + checklist, each with a resolvable source, is what its gate text asks).

Which box is understated: **box 3** — its bracket and pointer neither name the current instrument nor
its measured credit, and its pointer's path mislabels the state it carries. Box 1 is not understated;
it is *stale in one witness* (a precision defect, not a coverage one).

## The report's future SHONEN section

The section the round-55 report will carry is the round-54 report's block, `.ufo/reports/round-54/tameshi.md:229–234`
(fleet pin `fcb8d8db`), and it repeats the four boxes `[~]` with the same pointers. Those pointers are
lane-relative and are written in backticks, not links. Read from the report's own directory (the
fleet root) they do **not** resolve; with the lane prefix the report's own header names
("Lane repo `tameshi-shokunin`") they do:

```
$ cd /home/vgpnk/Projects/shokunin
  reports/round-1-calibration.md                       MISSING
  .ufo/evidence/round-21/coldread/ledger.json          MISSING
  tameshi-shokunin/reports/round-1-calibration.md      EXISTS
  tameshi-shokunin/.ufo/evidence/round-21/coldread/ledger.json  EXISTS
```
Receipt: `T55W3CritShonen-receipts/11-report-future-shonen.txt`. Observation, not a lane defect: the
future section should prefix each pointer with `tameshi-shokunin/` so the fleet-root reader can follow
it, and should inherit box 1's corrected range and box 3's re-pointing.

## The round's own blind spot (calibration axis)

The C1 counter never reads this surface: `grep -nE 'SHONEN|round-1-calibration|box-'` over
`.ufo/evidence/round-55/c1/measure.py` returns **0** hits, and the contract's C1 surface is "the ten
routed defects the round-54 non-author spot-check pinned (R54.1-R54.10)". So C1 can pass while the
checklist that certifies promotion still cites bytes that moved — which is what boxes 1 and 4 show at
C0. That is a coverage note for the next round's counter, not a verdict change for this one: C1's
claim is about its ten classes and remains measurable as declared.

## Sweep (what I ran; a "clean" row is a run, not an assumption)

Receipts in `T55W3CritShonen-receipts/`:

| # | File | What it decides |
|---|---|---|
| 01 | `01-pointers-resolve.txt` | C0 clone identity; `SHONEN.md` numbered; anchors `## box-*`; no commit base→C0 touches the three pointer files |
| 02 | `02-cited-lines-at-c0.txt` | every line citation inside `#box-1/-2/-4` dumped at C0 (`SKILL.md`, `LOG.md`, `PROVINCE.md`, `tools/mutate-and-run.sh`, three corpus notes) |
| 03 | `03-skill-ranges-numbered.txt` | `SKILL.md` 50–95 and 478–540 numbered |
| 04 | `04-log-and-tool-lines.txt` | `LOG.md:277–298` numbered; `mutate-and-run.sh:78–120` numbered |
| 05 | `05-baseline-blob-check.txt` | the audit's baseline blob `284ab0f0`: 466–495 / 497–525 / 58–92 were exact |
| 06 | `06-shonen-canonical-diff.txt` | canonical-seed diff (prose/box/marks) |
| 07 | `07-ledger-provenance.txt` | ledger `provenance` / `round21_provenance` / the 20 `corrections` records |
| 08 | `08-box1-witness-drift.txt` | heading lines at `284ab0f0`/`0a2010ac`/C0; C0 diffstat; containment tests |
| 09 | `09-box3-ledger-state.txt` | ledger size/sha/entries/headings/last-read verdicts/provenance/commit count |
| 10 | `10-box4-witness.txt` | ten legs at 84–97; leg-row count; fleet connector lines at `cb3c1039` |
| 11 | `11-report-future-shonen.txt` | report section lines; resolution from fleet root vs lane prefix; anchors at C0 |
| 12 | `12-c1-scope-and-coldread-credit.txt` | C1 counter has no SHONEN surface; contract C1 surface; round-54 `COLDREAD_PRECHECK` lines |

Artifacts opened: `SHONEN.md`@C0; `.ufo/evidence/round-21/coldread/ledger.json`@C0 (and its `entries`,
`provenance`, `round21_provenance`, `corrections`); `reports/round-1-calibration.md`@C0 (`#box-1/2/3/4`,
`## supersession…`, and the round-37 box-3 erratum at `583909a`); `SKILL.md`@C0, @`0a2010ac`,
@`284ab0f0`; `LOG.md`@C0; `PROVINCE.md`@C0; `tools/mutate-and-run.sh`@C0;
`corpus/knowledge/{gates-survey-kumitate,gates-survey-kagi,verification-patterns-fleet,mutation-case-kagi-census}.md`@C0;
`SCORECARD.md` `## Round 55 - round-54 record corrections`@C0; `.ufo/evidence/round-55/contract.json`,
`.ufo/evidence/round-55/c1/measure.py`@C0; `.ufo/evidence/round-54/after/{c1,coldread-precheck}.stdout`@C0;
fleet `PROTOCOL.md:59–72,441–451` and fleet `.ufo/reports/round-54/tameshi.md:229–234` (pin `fcb8d8db`)
and `.ufo/waves/shokunin12h-20261014-p1-repair/members/FleetBoundaryConnector.md:39,42,114` (pin
`cb3c1039`).

## Tooling and scratch

No tool installed or upgraded (nothing needed; `git`, `python3` suffice). Scratch:
`/fast/scratch/hyaku/tameshi-r55/T55W3CritShonen/c0`, a `--shared` clone at C0, removed after the run;
the shared parent was never touched. No lane production file, frozen file or wave spec was written;
the only writes are this report and `T55W3CritShonen-receipts/`.
