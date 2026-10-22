# ScoutFrontier — round 26 wave 1: which frontier row does leg 9 advance?

## Verdict

**None.** The ninth recorded leg (`js-cite-check`, kumitate
`scripts/cite-check.mjs` @ `1205c662`, blob `40573448…`) advances **no row of
F1–F10**. It is **Core ground already**, in the exact shape the province
defines: a new member of the *recorded mutation legs* surface list, measured
read-only on an owned `kumitate-shokunin/scripts/*` gate. Its second effect is
to discharge the kill-rate ledger's `cite-check` queue row ("probe only, 1/4;
full sweep open") — a ledger debt, not a frontier row. The only prose that
becomes false is the **count**, "eight recorded legs", in two places. No row
status changes; no promotion is earned.

Confidence: **high** for "no F row advances" (every row's next move is a method
step, and none of them is executed by a 10-mutant sweep on one more gate);
**high** for "Core already" (PROVINCE's own definition plus two identical
precedent appends); **medium** only on whether the L1 wants to record the leg
as a Core *enumeration* row or leave the enumeration implicit — both readings
are consistent with PROVINCE as written.

## Evidence

Local lane files opened this session (2026-10-22); no web source was used, so
no external source claim is made here.

1. **The frontier rows are method grounds, not gates.** `corpus/README.md:76-87`
   lists F1–F10; every `next falsifiable move` cell is a method step (schema
   emission, N≥3 controls, update-path counting, environment differential,
   fixture reduction, per-leg reuse, oracle anchoring, LLM pilot, PBT
   generator). None reads "measure one more gate".
2. **The admission rule.** `corpus/README.md:120-121`: "A ground reads `held`
   only when its next move in the table is measured." A held row re-exercised
   at a new gate is not a new measurement of its next move.
3. **Core already contains the recorded-legs shape.**
   `PROVINCE.md:28-38` defines Core as "the method above, plus every surface
   the lane has actually measured or now governs: the six recorded mutation
   legs' gates as read-only primary surfaces". `PROVINCE.md:7-9` owns
   "`kumitate-shokunin/scripts/*`". Two appends of exactly this kind exist:
   `PROVINCE.md:49-57` (seventh leg, round-gate, "probed read-only as a
   kumitate `scripts/*` primary surface") and `PROVINCE.md:73-83` (eighth leg,
   sources-check, same sentence shape).
4. **The lane's own contract frames it as Core, not frontier.**
   `.ufo/evidence/round-26/contract.json` → `claims.C1.learning`:
   "ninth recorded mutation case on a never-measured kumitate gate
   (scripts/cite-check.mjs), PROVINCE core: the recorded mutation legs".
5. **The leg actually landed as a measurement.**
   `.ufo/evidence/round-26/cite-check/sweep/sweep.txt` final line:
   `MUTATE: DONE (target=cite-check.mjs defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)`;
   `MUTATE_RESTORE: OK`, target sha256 before=after=`40573448…`.
6. **The debt it closes is the ledger's.**
   `corpus/knowledge/fleet-kill-rate-ledger.md:107`: "**probe only, 1/4** (§2);
   full sweep open"; `:94` records that probe as "a probe, **not a sweep**";
   `:224` U4 "the ten surveyed gates' kill profiles are unknown; the cite-check
   probe (1/4) is an indication, not a rate"; `:280` lists cite-check among the
   "eight queue rows" that stand. This sweep is the queue row's discharge — a
   knowledge-note/ledger update, not an F-row crossing.

## Row-by-row disposal

| Row | Why leg 9 does not advance it |
|---|---|
| F1 | Held (report-interop half) at `corpus/README.md:385-393`. A ninth leg re-runs held ground; it does not measure a new next move. F1b stays open (`:392-393`, NoCoverage for the recorded survivors). |
| F2 | Bash mutation tooling / witness split; leg 9 is a JS gate. |
| F3 | `corpus/README.md:80` asks N ≥ 3 byte-identical controls. The sweep has **one** control: `grep -c "^CONTROL:" …/sweep/sweep.txt` → `1`. Round-18 precedent: `corpus/README.md:270-273` refused to move F3 for an 8-run control at one case, "not per surveyed gate". |
| F4 | No count of update paths that write expected values; not attempted. |
| F5 | `corpus/README.md:331-336` freezes F5's population at nine files and says explicitly: "The distinct six-suite kumitate survey also includes cite-check, surface-probe and proxy-check: these three are **not measured here**." Leg 9 runs one guarded `env -i` side (`tools/mutate-and-run.sh:1426`, `LC_ALL=C`, no `LANG`/`TZ`, no host-profile pair, no `env-diff.py` run) — the round-1 H3 shape is a *pair* comparison, not this. |
| F6 | Fixture minimization for survivors: no reduced-fixture probe in the round-26 evidence tree. |
| F7 | Per-leg reuse decisions: untouched. |
| F8 | `corpus/README.md:235-237` sets the bar: "F8 needs a mutant-side survivor probe tied to an independently anchored expectation." Round 18 carries `.ufo/evidence/round-18/sources-check/survivor-probes/`; round-26 has no such directory. The five survivors are classified by **pre-registered hole reasons** (`predictions.json`), which is prediction accuracy, not oracle anchoring. |
| F9 | No LLM-generated mutant search; spec is hand-composed 5 kill / 5 hole. |
| F10 | No generator. |

## What the README / PROVINCE block may say, and what it may not

Safe to write:
- "Ninth recorded mutation leg `js-cite-check` on kumitate
  `scripts/cite-check.mjs` @ `1205c662` (blob `40573448…`): 5/10 (50 %), 10/10
  pre-registered verdict predictions held, guarded `env -i` 62-case hermetic
  suite, `MUTATE_RESTORE: OK`."
- "This extends the Core recorded-legs list from eight to nine; it does not
  measure any F1–F10 next move."
- "The ledger's cite-check queue row (probe only, 1/4) is superseded by this
  sweep; U4's cite-check half narrows accordingly."
- Depth-axis movement (8 → 9) belongs to the scorecard/contract claim
  (`.ufo/evidence/round-26/contract.json` `claims.C1.target`), not to a
  frontier sentence.

Must not be written:
- Any sentence of the form "F1/F3/F5/F8 advanced or moved to Core by this
  round". F1's status correction at `:385-393` is a *held* statement whose
  denominator is a count; re-validating it at a ninth leg is same-ground.
- "F5 measured cite-check": barred by `corpus/README.md:334-336`, and the
  leg's environment is not F5's nine-surface × seven-profile differential.
- "F3 determinism precondition measured": one control per sweep is F3's
  *precondition* (`:80` left side), which the ledger's legacy sweeps already
  had; the next move is N ≥ 3.
- "F8 survivor class anchored": no survivor probe exists this round.
- Any promotion, producer-authentication or numeric-score claim.

## Owed count updates (the smallest safe correction)

Two counts go stale the moment leg 9 is wired, and both are count edits, not
status edits:

- `corpus/README.md:386` — "Report interop is now held for the eight recorded
  ledger legs". After the ninth leg, this must read **nine**, *and only if*
  the interop companion prints `MTE_INTEROP: PASS legs_conforming=9/9` at the
  integration revision (`tools/mte-interop.py:343-344`; the contract lists this
  as a no-harm companion). F1b stays open either way.
- `PROVINCE.md:101-102` — "`tools/mte-interop.py` emits the eight recorded
  ledger legs"; same condition, same replacement.

Derived, not observed as a stated number: nine legs at 5 killed each leave
35 + 5 = **40** recorded survivors, so F1b's NoCoverage denominator moves from
35 (`corpus/README.md:392-393`) to 40. [INFERENCE: arithmetic over the nine
recorded tables; no coverage data exists for any of them, so the row's status
is unchanged.] If the L1 wants that number in prose, re-derive it from the
nine tables rather than quoting this line.

## Remaining unknowns

- Whether the round will also append the leg to the kill-rate ledger's §1
  table (row 9) or only to the queue-row supersession note — that is a ledger
  editorial choice; `fleet-kill-rate-ledger.md:280` says the queue rows "stand"
  as written, so the round must state which row it supersedes and where.
- Whether `SKILL.md` or `SCORECARD.md` carries its own "eight legs" count; I did
  not audit those two files, so this report makes no claim about them.
