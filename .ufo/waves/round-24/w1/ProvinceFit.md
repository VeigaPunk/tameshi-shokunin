# ProvinceFit — round24 additions against PROVINCE.md Core/Frontier/Adjacent

Verdict: **inside verification-fixture craft.** No round24 addition crosses
into Adjacent, none claims a Frontier move, and none asks tameshi to own a
sibling's gate or product clause. The single misfit is record-level and
inside Core: `PROVINCE.md` has no append after round21 (`:85-95`), so the
lane's Core inventory does not name `tools/registry-replay.py` (round24) or
`tools/command-binding.py` (round23), while it does name the round21
instrument `tools/env-diff.py` (`:89`). That is an **under-claim, the safe
direction** — the generic Core clause "this lane's runner" (`:37-38`) plus
"the method above" (`:28`) already covers a lane-local verification
instrument. No boundary repair is needed; one append is the smallest artifact
that keeps the inventory true and pins the two bounds a reader would
otherwise over-read.

## Axes

- **A1 boundary fit** — does each new surface map to Core, or cross into Adjacent?
- **A2 Core inventory accuracy** — does PROVINCE's own "every surface … now governs" (`:28-29`) match what the lane added?
- **A3 verdict-line calibration** — do the new tool's sentences claim only what its mechanism shows?
- **A4 routing** — is anything out of province (kagi/kama/S030/game-lane) absorbed instead of reported?

## Evidence — mapping (A1, A4)

| Round24 surface | Province clause | Fit |
|---|---|---|
| `tools/registry-replay.py` | Core "this lane's runner" (`PROVINCE.md:37-38`), method `:1-7` (hermetic replay, fail-closed arms, before/after proof) | **In Core.** It is a lane-local instrument over this lane's registry; it adjudicates no sibling gate. Not credential (kagi `:45`), endpoint health (kama `:45-46`), UI diff (S030 `:46-47`), engine nondeterminism (`:47`). |
| `corpus/knowledge/replay-projection-hardening.md` | Frontier admission rule `:40-42`; README home `corpus/README.md:371-377` | **No boundary move.** `source:` cites two `mined` rows (`corpus/SOURCES.md:93-94`); README states "same-ground calibration … No F1–F10 status changes". |
| `.ufo/evidence/round-24/extra-cases.json` | Core corpus (`:37-38`) | In Core: five rejection fixtures for the existing gate; `tools/command-binding.py:164-169` loads both round23 and round24 fixture files. |
| `tools/registry.json` r24 rows (`:961-998`) | Core source registry (`:38`) | In Core, append-only: the three round23 rows keep `status: superseded` + `superseded_by` (`:934-956`), matching the knowledge entry (`replay-projection-hardening.md:23-26`). |
| `.ufo/evidence/round-24/{contract,measure}.py/json`, `before.json`, `replay/` | Core runner/evidence (`:28`, `:37-38`) | In Core. |
| S084 (Python docs, `SOURCES.md:93`), S085 (own-work round23 adjudication, `:94`) | allowed source classes | In Core; neither is credential or endpoint material. |

Nearest boundary and why it does not cross: the replayed row
`mutate-and-run-regression` passes through the eight recorded fleet-ledger
legs, i.e. sibling gate bytes. Those legs are the lane's already-owned
read-only primary surfaces (`PROVINCE.md:29-35`), materialized by
`git show <rev>:<path>` with a sha256 pin and a SETUP refusal on mismatch
(`tools/mutate-and-run.sh:113-119`); "the fleet trees are never written"
(`:119`). The replay publishes tameshi's recorded ledger expectation, not a
sibling verdict, and routes no recommendation.

## Falsification — attacked the three sentences closest to a boundary (A3)

1. **"live_dependent … instead of being silently reported as revision-pinned"**
   (`tools/registry-replay.py:10-12`). Concrete counterexample row:
   `mutate-and-run-regression`. It reaches live sibling repos through the
   temp fleet mirror, whose entries are symlinks to the real paths
   (`registry-replay.py:161`); its retained stream shows
   `REGRESSION_PIN js-kimi-census: source=git repo=/tmp/tameshi-registry-replay-dzo3ypiq/fleet/kumitate-shokunin rev=175de6b… sha256=83016d4…`
   (`replay/observations.json`, that row). Yet it has `external = false` and
   `non_hermetic_argv = null`, so `project()` (`:99-107`) counts it inside
   `revision_pinned: 41` (`replay/live-dependent.json`). This is **not** a
   false claim — each leg's target bytes are sha-pinned and a missing
   repo/rev/blob or pin mismatch is a refusal (`mutate-and-run.sh:113-114`)
   — but the label is *content-scoped*. `revision_pinned` is the complement
   of a declared/argv-token classification, not a measured hermeticity set,
   and the knowledge entry's Bounds (`replay-projection-hardening.md:28-40`)
   never says so. A reader can over-read `41 revision-pinned` as observed
   isolation.

2. **"Writes only under --out"** (`registry-replay.py:18`). Tool-scope only;
   the next clause says rows are not write-isolated from siblings
   (`:19-20`). Read alone the sentence is a run-scope guarantee. The
   `SKILL.md:2052` row repeats the split ("writes only under `--out`; rows run
   in a private clone whose fleet mirror symlinks live siblings") without the
   isolation denial. Safe today because every current row's writes land in
   the temp clone and the ledger legs are byte-pinned; the scope split should
   still be stated where the guarantee is cited.

3. **Coverage of "the new gate".** The retained replay covers the **round23
   baseline**, 43 active rows, not the current registry, 47 active. Verified:
   `python3 -c "…"` over `registry-baseline.json` vs `tools/registry.json`
   printed `baseline rows 47 active 43` / `current rows 54 active 47`, and
   `current-only active: ['command-binding-frozen-clean-pinned',
   'command-binding-selftest-r24', 'command-binding-source-read-red-pinned',
   'registry-replay-selftest']`. The digest check is real
   (`hashlib.sha256(raw_registry) == frozen['registry_sha256']` → `True`), so
   this is an intentional frozen population. Consequence: the new tool's own
   row `registry-replay-selftest` is **not** in `replay/bundle.json`; it holds
   only from a separate run (``.ufo/waves/round-24/w1/RunSelftests.md:24-25``,
   `REGISTRY_REPLAY_SELFTEST: 10/10 pass`). "The gate is exercised" and "the
   gate's row is replay-covered" are different facts; only the first is
   retained in the round24 replay.

Related calibration fact, not a boundary issue: the round's before/after
proof is split across artifacts. `before.json` is in
`.ufo/evidence/round-24/`; the 11/11 after-state exists only in
`.ufo/waves/round-24/w1/RunRulerAfter.md:3`; there is no `after.json` in the
evidence dir (`ls`), and `corpus/lessons/round-24.md:53` still says "The after
measurement is recorded below once executed" with no section below it
(53 lines total); `SCORECARD.md:1145` says the same. Core's own craft includes
before/after proof (`:6-7`), so landing that receipt is owed by the
integrator — it changes no province line.

## Contradiction stated, not smoothed

`PROVINCE.md:28-29` defines Core as "every surface the lane has actually
measured or **now governs**", i.e. an inventory, yet the last append is
round21 (`:85-95`). Rounds 22, 23 and 24 each added a governed instrument
(`tools/wave-accounting.py`, `tools/command-binding.py`,
`tools/registry-replay.py`) and none is named. Either the generic phrase
"this lane's runner" is the intended home for all calibration instruments —
in which case the enumeration precedent set at `:89` (`tools/env-diff.py`) is
misleading — or the inventory is stale. Both readings leave the domain fit
intact; the two cannot both be the recorded intent.

## Proposed move — one, bounded

Append one paragraph after `PROVINCE.md:95`, append-only, changing no existing
line:

> ## Core — round 24 append (2026-10-21)
>
> Same-ground calibration instruments stay in Core under the "this lane's
> runner" clause at `:37-38`: `tools/command-binding.py` (round 23) and
> `tools/registry-replay.py` (round 24, gate owner tameshi). The replay runs
> frozen registry requirements in a private clone whose fleet mirror
> symlinks the live sibling repos; realpath identity is not write isolation,
> and its `revision_pinned` count is the complement of declared `external`
> and runner-flagged `non_hermetic_argv` rows, not a measured hermeticity
> claim — `mutate-and-run-regression` reaches live sibling repos for
> sha-pinned content and is counted there. Bundle and requirement digests are
> not producer authentication, and the eleven predicates are synthetic
> capability checks, not historical defects. No F1–F10 status change, no
> numeric-calibration change, and no sibling gate ownership change.

Why this and not the alternatives: doing nothing leaves the inventory stale
for three rounds and leaves the `revision_pinned` scope only in a wave
report; editing the knowledge entry's Bounds alone would be a production edit
outside this lane's write scope and would still not record the instrument in
the province. The append is the smallest artifact that does both.

## Risks

- PROVINCE lines are cited across the lane; the append preserves numbering
  exactly as `:49`, `:85` did.
- Naming a tool in Core can be read as a governance claim; the closing
  sentence denies the expansion, and no sibling surface is added.
- The `revision_pinned` sentence discloses a scope limit; it does not allege
  the row is wrong (content is pinned; setup fails closed).

## Verification (for the integrator, not run here)

- `git diff -- PROVINCE.md` is a pure append after `:95`;
  `grep -c '^## Core — round 24' PROVINCE.md` = 1; `wc -l` grows only by the
  block.
- Re-read `tools/registry-replay.py:18-20,99-107` and
  `replay/live-dependent.json` against the paragraph's wording; expect
  `41` / `2` unchanged.
- Do not re-run gates for this item. If the integrator lands the after
  receipt, fill `corpus/lessons/round-24.md:53`'s promised section at the same
  time; it is independent of this province append.

Tools installed or upgraded: none.
