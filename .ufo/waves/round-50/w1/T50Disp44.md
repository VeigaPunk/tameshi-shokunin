# T50Disp44 — C1 disposer, round-44 spot-check (items R44.1, R44.2)

Seat: `T50Disp44`. Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, tree read at base
`e3729de862f73ae080d98fcf522a7081ce16e40a`. Frozen statement set
`.ufo/evidence/round-50/c1/defects.json` (49 items); my two items come from
`corpus/lessons/round-44-verifier-spotcheck.md` (sha256 `e295e90b…f57f`), routed heading
"Routed defects for round 45", lines 73–74 of that file, `routed_at`
`5891bdb77aba8489683533ae4cdd3b49b5e2626b`.

Deliverables: `T50Disp44.rows.json` (2 rows), this report, and the counter receipt
`T50Disp44.explain.stdout` / `T50Disp44.explain.stderr` (empty).

## R44.1 — cosmetic label "20 words" on the Stryker line-15 quote — **fixed**

**The ask** (`corpus/lessons/round-44-verifier-spotcheck.md:73`, verbatim under its routed heading):
"Cosmetic: `corpus/lessons/round-44.md` Gate's first located quote is labeled “20 words”; it
tokenizes to ~28 (24 letter/digit words). The row's grounding quote (12 words) is compliant, so no
bar is violated; correct the label in a future round (append-only)."

**What I found.** The byte at `corpus/lessons/round-44.md:26` still reads `- line 15, 20 words:
“Notice that 10 ** 0 = 1, so even if we change >= to <= and even < or > we will get the same output
each time!”` — and it must: the ask itself says *append-only*, and the lane's corpus rule forbids
rewriting a closed round's lesson. The tree carries the append-only correction in the round that
followed. `corpus/QUALITY.md:1229-1231` states the repair form the item invokes: "A label that
disagrees with the measured count is a record defect fixed append-only with an errata line naming
the measured value, and admission is decided by the counter's grade, not by the label: a
hand-written \"20 words\" on a 28-token quote misreports the quantity the". `corpus/QUALITY.md:1235-1238`
is that errata line for this exact record: "Lesson: `corpus/lessons/round-44.md:26` labels the
Stryker quote \"20 words\"; measured, it is 28 whitespace tokens (22 letter/digit words) and the
round-45 C1 counter grades it `('invalid', 'quote length 28')` — receipt
`.ufo/evidence/round-45/mistakes/r44-quote-token-count.stdout`." `corpus/lessons/round-45.md:158`
carries the same correction as a `number-drift` row in that round's Mistakes table, naming the
inheritance ("the 20 was inherited from `corpus/lessons/round-43.md:52`") and noting the spot-check's
own parenthetical "24" is unmeasured. The measurement is executable, not prose:
`.ufo/evidence/round-45/quality/c87-falsifier.stdout:1-3` reads `lesson label: "20 words"; …
whitespace_tokens=28 letter_digit_words=22` / `C1 grade on the round-44 label quote: ('invalid',
'quote length 28')`, with `exit=0` on line 5. All of it was added by
`ea25e0224fc81060414b27301c27bd1344669165` ("round-45: records — lesson, QUALITY criteria 86-87 with
falsifier receipts, …"), which `git diff-tree --no-commit-id --name-only -r` shows touching
`corpus/QUALITY.md` and `corpus/lessons/round-45.md`; it is an ancestor of base `e3729de8` and not an
ancestor of `routed_at` `5891bdb7` (`git merge-base --is-ancestor`, both directions checked).

**Status: fixed.** Judgment basis: the closure asked for the correction "in a future round
(append-only)", and the governing document defines the append-only repair as an errata line naming
the measured value — that rule and that line both exist, added post-routing. A wave-2 judge who reads
"correct the label" as "the bytes at `round-44.md:26` must change" would have to overturn the lane's
own append-only rule; under that reading the item is unclosable by construction. I record the
divergence explicitly rather than hide it: `round-44.md:26` is untouched.

## R44.2 — wave shape was one v1 wave of 32 seats with 14 attack-role seats — **declined**

**The ask** (`corpus/lessons/round-44-verifier-spotcheck.md:74`, verbatim): "Observation (not a
defect): wave shape was one v1 wave of 32 seats with 14 attack-role seats; no wave 2 or residual call
because the distinct fresh attack inventory was below 32 and none remained unassigned, as reported in
`w1/summary.md`."

**What I found.** `.ufo/waves/round-44/w1/summary.md:3`: "Shape: one v1 wave, `round-44-w1`, policy
band 32–64; … validated with exit 0 and emitted `counts.spawn=32`, `counts.resume=0`."
`:6`: "Attack roles: 14 seats (reviewer/critic/mutation-tester); their items were worked and reported
in wave 1. The resulting distinct fresh attack inventory was below 32, so no wave 2 was dispatched.
No unassigned residual check remained; no ordinary residual call was needed." The spot-check itself
labels the item "Observation (not a defect)", and no round 45–49 lesson re-routes it
(`grep -rn "number-drift\|criterion 87" corpus/lessons/` finds no R44 item).

**Status: declined.** Wave shape is the dispatch policy's outcome, not a lane defect: the 32-seat v1
band and the "fresh attack inventory below 32 ⇒ no wave 2" rule are the orchestrator's, and the lane
cannot change a wave's shape after it happened. Nothing in the tree was asked to change, so there is
nothing to close. Reason (≥40 chars, normalized) is in the row.

## Counter self-check (scratch clone, my rows only)

Scratch clone `git clone -q --shared <lane> "$S/lane"` (toplevel verified `=
/fast/scratch/hyaku/tameshi-r50/T50Disp44/lane`), ledger written as `{"defects": [<my 2 rows>]}` and
committed with a scratch identity (`b7bd182119da90e794d6ecec0c5fec29a92c43e7`; scratch later deleted,
receipt copied to this directory). Command:

```
TMPDIR=$S python3 <lane>/.ufo/evidence/round-50/c1/measure.py --lane "$S/lane" --rev HEAD --explain
```

Observed final line (copied verbatim to `T50Disp44.explain.stdout`; exit 1):

```
C1_R50: self=ceee320c9ad8 rev=b7bd182119da90e794d6ecec0c5fec29a92c43e7 defects=49 rows=2 fixed=1 open=0 declined=1 fixed_this_round=0 missing=47 extra=0 duplicate=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=0 key_miss=0 fixed_bad=0 open_unplanned=0 declined_bad=0 fixed_short=19 declined_over=0 this_round_short=5 total=71 C1_R50_PASS=false
```

Every one of my row-level counters is 0 (`extra`, `duplicate`, `bad_status`, `evidence_bad`,
`key_miss`, `fixed_bad`, `open_unplanned`, `declined_bad`), and **no `EXPLAIN` line names R44.1 or
R44.2** (`grep -E "R44\.|C1_R50:" T50Disp44.explain.stdout` prints only the final line). The 47
`EXPLAIN missing` lines name other rounds' ids (R40.x–R43.x, R45.x–R49.x) and are expected for a
two-row seat ledger. `total=71` / `C1_R50_PASS=false` / `fixed_short=19` / `this_round_short=5` are
aggregate-floor counts that apply to the merged 49-row ledger: the floors demand ≥20 fixed and ≥5
fixed by commits after BASE. My one fix is historical (`ea25e02` is an ancestor of BASE `e3729de8`,
so the counter's own rule counts `fixed_this_round=0` for it); the merged ledger's this-round fixes
must come from other seats' rows.

## Provenance and limits

- Both spot-check items, their `keys` and `routed_at` were read from the frozen
  `.ufo/evidence/round-50/c1/defects.json`; spot-check sha256 checked by the counter
  (`spotcheck_changed=0`).
- Every cited file is byte-identical at base `e3729de8` and at lane tip `4afb060`
  (`git -C <lane> diff --stat e3729de8 4afb060 -- corpus/QUALITY.md corpus/lessons/round-45.md
  .ufo/waves/round-44/w1/summary.md .ufo/evidence/round-45/quality/c87-falsifier.stdout` prints
  nothing), so the line numbers I read are the base tree's line numbers.
- The counter cannot see *semantic* support ("that a keyed, new excerpt really resolves the defect"),
  per its own docstring; R44.1's fixed judgment rests on `corpus/QUALITY.md:1229-1231` defining the
  append-only errata line as the fix, plus the errata line at `:1235-1238` and the measured receipt.
- The spot-check's own "24 letter/digit words" is itself unmeasured; the measured values are 28
  whitespace tokens / 22 letter-digit words (`corpus/QUALITY.md:1241-1243`, receipt line 2). Not a
  defect I route: it is disclosed inside the same errata line.
- Left lane and fleet VCS untouched; no `git add/commit` outside the scratch clone; no reads under
  `/home/vgpnk/.local/state/`; no `agent://all` message.
- Tooling: nothing installed or upgraded this seat (no `uv`, `npx`, pacman or PATH write); `python3`
  and `git` as shipped.

## Summary

- R44.1 **fixed**: round-45 append-only errata (`corpus/QUALITY.md:1229-1231`, `:1235-1238`;
  `corpus/lessons/round-45.md:158`; receipt `.ufo/evidence/round-45/quality/c87-falsifier.stdout:1-3`)
  names the measured 28 tokens / 22 words, commit `ea25e02`, post-routing and ancestor-of-base.
- `corpus/lessons/round-44.md:26` still reads "20 words" by design: the ask says append-only, and
  `QUALITY.md:1229` defines the errata line as the fix; recorded openly for the canonical judge.
- R44.2 **declined**: the item is labelled an observation of dispatch wave shape; the settlement
  summary (`round-44/w1/summary.md:3,6`) already records seats, 14 attack roles and the no-wave-2
  reason. No tree change was asked for.
- Counter run on a two-row scratch ledger: no `EXPLAIN` line names R44.1/R44.2; all row-level
  counters 0. `fixed_short=19`/`this_round_short=5` are merged-ledger floor counts, not row failures.
- Receipts: `T50Disp44.explain.stdout` (sha256 `28094078…8a4`), rows `T50Disp44.rows.json`.
