# PlanWalk — round23 routed defects → round24 disposition map

Seat: TameshiR24-2.PlanWalk (planning data-walk, read-only). Delivered revision
`c8c5b88c8e961a929cdc351b95a7074c76958909`; base `6a1821a8897eea6e7d9669292160ec9593669409`;
round23 adjudication `.ufo/waves/round-23/fresh-adjudication.json` (recorded by CloseTameshi22,
2026-10-21T15:11:17Z).

Method: `GIT_OPTIONAL_LOCKS=0 git show/log/diff/cat-file`, `sha256sum`, JSON reads, and
`git grep` at the delivered revision. **No ruler, gate, selftest, mutant, registry battery or
replay was executed by this seat** (item has no “Run” clause). Outcomes I did not execute are
marked `[INFERENCE: static trace]`; sibling wave artifacts are cited with provenance and not
treated as repo receipts.

## Verdict

All eight routed defects are accounted for; none is unlisted, and no ninth is hidden. But the
round24 surfaces do not carry the whole disposition:

- **6 of 8** routed defects have a frozen predicate: R1→K1, R2→K3, R3→K5/K6, R4→K7/K8/K10,
  R6→K11, R7→K9 (size half only). That is **9 of the 11 predicates** over 6 routed defects;
  K2 is an adjacent argv-identity expansion and K4 is the base-killed control allowed by QUALITY48.
- **1 of 8** is a non-predicate code change, disclosed: R5 (clone-copy runner hash).
- **1 of 8** is still open by explicit policy: R8 (frozen loose stdout tokens).
- **Two clauses are narrowed without being named at round24**: R7’s redaction half, and the fact
  that `--max-stream-bytes` bounds the *published bundle* but not `observations.json`, which
  retains complete streams before projection.
- **R8 has no round24 disposition anywhere** (knowledge entry, lesson, SCORECARD routed list) even
  though the round23 adjudication and MANIFEST closure notes route it.
- **The after-state is not retained in repo evidence.** The 11/11 result exists only as sibling
  wave artifact `.ufo/waves/round-24/w1/RunRulerAfter.md`; `corpus/lessons/round-24.md:53` promises
  “The after measurement is recorded below once executed” and the file ends there (53 lines).

Calibration consequence: the *mapping* is largely honest, but the *denominator prose*
(“eleven … predicates routed by round23 critics and closure”, contract.json claim; README Ground
“routed round23 hardening gaps as falsifiable predicates”, `corpus/README.md:375`) reads as 8/8
coverage. It is 6/8 predicates + 1 code fix + 1 open.

## 1. The data walk — every routed entry

`routed_not_executed` is lines 48–103; entries begin at 49, 57, 63, 71, 78, 85, 91, 97.
The other buckets are not repairs: `accepted_now_as_corrections` (5) are text corrections;
`rejected` (3) are refused broadenings; `agreements_without_change` (11) confirm no change.

| # | Routed findings | Routed defect (compressed) | Round24 disposition | Predicate(s) | Evidence at c8c5b88 |
|---|---|---|---|---|---|
| R1 | ArgvExact | Name-insensitive argv mutant outside the ten-anchor sweep; would survive all 38 selftest cases **“[seat inference, not executed]”**; needs swapped-name case + mutant | **predicate + fixture** | K1 | `measure.py:27-36` mutant = `receipt['argv'] not in [row['argv'] …]`; `round-24/extra-cases.json` case `argv-swapped-between-names`; `command-binding.py:103` anchor count 1; `registry.json:961-965` expects 44/44 |
| R2 | MutationDesign | Unexecuted negative-exit guard-weakening candidate; survival was a seat inference | **predicate + fixture** | K3 | `measure.py:32-33` mutant adds `exit >= 0`; fixtures `negative-exit-mismatch` (receipt −9 vs expected 0) and `negative-exit-declared-match` (−15 declared and matched stays clean) |
| R3 | RevisionDeclared F1, CorpusClaim F3 | `command-binding-frozen-clean` and `source-read-red` rows do not pin `bundle_sha256`, so a regenerated bundle + expected pair still holds | **predicates + append-only pinned successor rows** | K5, K6 | `measure.py:38-42`; registry rows `command-binding-frozen-clean-pinned` (`registry.json:971-975`) and `…-source-read-red-pinned` (`:981-985`); pins equal actual bytes: `3d6c99b7…` and `db620668…` (sha256sum) |
| R4 | Replay31, Replay34, CwdDeclared 2 | Projection drops `held`, `cleanup_ok`, `external`, `non_hermetic_argv`; the receipt schema cannot carry a live-dependency marker | **predicates for the projection half + non-predicate sidecar** | K7, K8, K10 | `registry-replay.py:86-99` refuses not-held/cleanup-failed, lists live rows; `publish` writes `live-dependent.json` (`:125-127`); bundle schema still has no marker (`replay/bundle.json` keys: schema/revision/cwd/requirements/receipts) |
| R5 | RevisionDeclared F3, CorpusClaim F2 | `runner_sha256` and `instrument_sha256` hash the live-tree copy, not the clone copy that ran; values equal at 496d212/8f66b5d/336565f | **non-predicate code change (disclosed)** | none (knowledge `:21` says “recorded per run, not a ruler predicate”) | `registry-replay.py:152-163` clones, detaches, then `runner_path = clone / …` hashed at `:163`; observations field `runner_sha256_clone_copy = cba16646…` equals `git show d2eaecd:tools/registry-check.py \| sha256sum` and HEAD/worktree (my hashes; peer `RevRunnerHash.md` reached the same) |
| R6 | CwdDeclared 3 | `replay.py` compares sibling identity by string and does not realpath the fleet root; latent for a non-canonical `--repo` | **predicate in successor; frozen instrument untouched** | K11 | `measure.py:185-200`; `registry-replay.py:63-69` realpaths repo, derives fleet root, realpaths siblings; round23 `.ufo/evidence/round-23/replay.py:51-53` still string-compares (frozen by design) |
| R7 | RunnerIsolation Medium ×2 | Replay streams retained **without size bounds or redaction**; no secret observed | **partial: size bound only, publish path only** | K9 (size) | `registry-replay.py:9,92-98` `STREAM_LIMIT`; **no redaction implementation or predicate anywhere** (`git grep -i redact c8c5b88 -- tools corpus SKILL.md SCORECARD.md .ufo/evidence/round-24` → only unrelated `SOURCES.md:25` S014) |
| R8 | Replay32, 33, 35, 36, 29, 43 | Preexisting loose stdout substring tokens in frozen rows; kept unchanged by no-retrofill/frozen-argv | **still open, intentionally** | none | Round23 lesson `:111` names “loose substring tokens … named old limitations”; MANIFEST rounds[421].notes routes “loose stdout tokens”; **absent from round24 knowledge/lesson/SCORECARD routed list** |

Lineage note (no hidden ninth): the pre-adjudication draft’s five accepted repairs
(`fresh-adjudication-draft.json:accepted_repairs`) cover R1–R5 plus the R4/R6 external-declaration
work; they do not mention realpath, streams or loose tokens. The adjudication’s eight add R6–R8
relative to the draft. SCORECARD says “Eight code/registry repairs are routed” (`:1100`) but
enumerates seven bullets (`:1119-1125`), with no loose-token bullet; MANIFEST rounds[421].notes
names “loose stdout tokens” explicitly. Read either way, R8’s route is in the adjudication and
MANIFEST, not in SCORECARD.

## 2. Base reproduction — inference upgraded to measurement

`before.json` is the strongest calibration datum in the wave: it converts two seat *inferences*
into measured survivors and reproduces the pin defect as non-discrimination.

- R1/R2: K1, K2, K3 rows — `exit: 0`, `failing_cases: []`, `control_exit: 0`, `anchor_count: 1`;
  tail shows `COMMAND_BINDING_SELFTEST: 38/38 pass`. The name-insensitive and negative-exit
  mutants really do survive the base public selftest.
- R3: K5 and K6 rows — `control: {row: true}`, `substituted: {row: true}` for **both** rows. The
  routed defect is measured: after a self-consistent substitution + regenerated expected file,
  the unpinned rows still hold.
- K7–K11: `reason: tool-absent`; K4: already killed at base by `CASE all-of-tokens FAIL`. So
  1/11 is honest, and it is 1 control + 0 repairs, matching QUALITY48’s rule that a base-killed
  control stays in the denominator (`corpus/QUALITY.md` criterion 48, third bullet).

After-state provenance (not a repo receipt): sibling seat `RunRulerAfter.md` reports
`{"discriminated": 11, "total": 11}` exit 0 at `c8c5b88`, with per-row controls
(`control_exit 0` / `control_ok true`) and the expected failing cases. Sibling `RunSelftests.md`
reports 44/44 and 10/10 at the same revision. My static trace agrees with all eleven rows, so I
found no reason to doubt 11/11 — but the result is currently only a wave artifact.

## 3. Predicate attribution audit (does each predicate kill *its* routed weakness?)

| K | Routed item | What the fixture actually forces | Attribution |
|---|---|---|---|
| K1 | R1 | Swapped argvs between two names; any-name membership comparison survives everything else but fails this case | **strong** |
| K2 | R1 family (extension) | Case-only argv; mutant is literal `.lower()` on both sides. Padded/repeated-token fixtures have no matching mutant in the ruler, but they are extra kills, not claims | adjacent expansion |
| K3 | R2 | −9 vs expected 0 must yield `EXIT_MISMATCH`; `negative-exit-declared-match` guards against over-tightening (−15 declared and matched is clean) | **strong** |
| K4 | closure any-vs-all probe | Existing round23 `all-of-tokens`; already true at base | control only |
| K5/K6 | R3 | Pristine active rows hold; after bundle substitution + expected regeneration the row’s literal digest no longer matches | **strong** (pins verified byte-exact against the files) |
| K7 | R4 (held) | `held=False` must refuse, write no bundle; control publishes | **strong** |
| K8 | R4 (cleanup) | Fixture sets `held=False` **and** `cleanup_error`, so the ruler cannot separate “cleanup-aware” from “relabel every not-held row”. A `cleanup_error`-only-inside-not-held implementation survives K8 and the tool selftest `[INFERENCE: static trace; peer PredK8.md]` | **weak** — real runner never emits `cleanup_error` with `held=True` (`registry-check.py:720` includes `cleanup_ok` in `held`), so the gap is limited to `--project` on foreign observation files |
| K9 | R7 (size) | One 67-byte ASCII stdout against 16; no at-limit control with a multibyte character. A byte-count-exact but character-counting implementation survives K9 and the tool selftest (which uses 9 ASCII `e` and 8 ASCII bytes) `[INFERENCE; peer PredK9.md]` | **weak but bounded** (contract bound 1 already limits K1–K4; K9 carries no such bound) |
| K10 | R4 (external/non_hermetic) | Single row sets **both** `external=True` and `non_hermetic_argv`; report check reads `live_dependent` only. External-only omission passes K10, though the tool selftest case `external` (`registry-replay.py:204-205`, asserted `:221-223`) still kills it. K10 does not read `revision_pinned` or `live-dependent.json` | **weak as a predicate**; mitigated outside the 11 by the selftest |
| K11 | R6 | Alias symlink + `..` input forces repo and fleet-root realpath; the only sibling is a plain directory inside an already-real fleet, so dropping sibling realpath passes K11 and the selftest. Peer `MutPlan.md` M2 observed exactly this survivor | **strong for repo/fleet root, vacuous for siblings** |

No predicate is vacuous in the strong sense (no skip path; every pass carries a passing control).
The gaps are attribution, not honesty of the base result.

## 4. Silently dropped / narrowed — flags

**S1 — R7 redaction: dropped, not named.** The routed text says “size bounds **or** redaction”.
Round24 implements a bound and nothing else. `git grep -i redact` at c8c5b88 over `tools`, `corpus`,
`SKILL.md`, `SCORECARD.md`, `.ufo/evidence/round-24` returns only the unrelated S014 row.
Knowledge `:18` rewrites the weak link as “unbounded retained streams”, narrowing the claim without
saying redaction is unaddressed; lesson and SCORECARD say “bounded streams”.

**S2 — the bound stops at the bundle, not at retention.** `registry-replay.py:183` writes
`observations.json` **before** `project()` at `:184`, and `run_replay` passes `retain_streams=True`
(`:170`). Concrete counterexample: a row that prints 2 MiB is fully retained in
`observations.json` under `--out`; `--max-stream-bytes 1048576` only refuses to publish a bundle.
The round24 replay itself retains 8 110 B stdout / 2 391 B stderr maxima (my JSON read), so no
secret is present, but the routed “retained without size bounds” property still holds for the
observations artifact.

**S3 — R4’s marker clause survives structurally.** `command-binding-v1` still has no
live-dependency field (`replay/bundle.json` top keys are schema/revision/cwd/requirements/receipts).
The sidecar `live-dependent.json` (41 revision-pinned / 2 live) is the synthesis, and the tool
docstring/knowledge say so. But `replay-gate.json` runs `command-binding.py` on `bundle.json`
alone and reports a clean 43-row verdict with no 41/2 caveat — the exact place round23’s
“isolated clone” overclaim re-enters: a reader of the gate receipt sees no live dependency.

**S4 — R5’s instrument half is external only.** The tool records `runner_sha256_clone_copy` but
no instrument digest; `replay-command.json` records `instrument_sha256 9fcd2dbb…` with the
parenthetical “live tree, equals rev blob”. I verified `git show d2eaecd:tools/registry-replay.py`
hashes to the same `9fcd2dbb…`, so the receipt is true for this run — but no tool computes or
binds it. The runner half is genuinely fixed in code; because live and clone bytes are identical
at every cited revision, no digest predicate could distinguish the fix (hence “recorded per run”).

**S5 — R8 is open with no round24 disposition.** Named in round23 lesson `:111`, routed in
MANIFEST notes, deliberately kept by the adjudication’s `rejected` rule (“Tighten old stdout
tokens … would change the frozen baseline argv/expect”). But the round24 knowledge table,
lesson, SCORECARD routed list and contract denominator are all silent about it. A reader of
round24 alone would conclude 8/8 routing.

**S6 — replay population does not exercise the new rows.** The round24 replay uses the round23
frozen pair (`requirements.json` = 43 rows, `registry-baseline.json` sha `ebd2e69a…`); no row name
contains `binding` (my JSON read). That is by design (“successor instrument, frozen requirements”),
but it means the three new active registry rows and the new selftest row are exercised only by the
registry battery, not by the replay/gate chain. Nothing in round24 says this explicitly.

## 5. Contradictions (stated, not smoothed)

1. `contract.json` claim: “eleven … predicates routed by round23 critics and closure” vs 6/8
   routed defects with predicates; `corpus/README.md:375` Ground: “routed round23 hardening gaps as
   falsifiable predicates” — wholly true for R1, R2, R3, R4’s projection half and R6 (5), partial
   for R7, and no predicate at all for R5 or R8.
2. `corpus/lessons/round-24.md:53`: “The after measurement is recorded below once executed”; the
   file is 53 lines and has no after result. `SCORECARD.md:1145-1146`: “Measured results are
   recorded below only after execution” — no 11/11 row follows.
3. Knowledge `:18` “unbounded retained streams” vs observations retention (S2).
4. SCORECARD says eight repairs are routed (`:1100`) but enumerates seven bullets
   (`:1119-1125`) and has no loose-stdout-token bullet; MANIFEST rounds[421].notes includes
   “loose stdout tokens”. Same round, two different routed sets.
5. `PredK10.md` says no frozen round24 surface kills external-only omission; the tool selftest
   (`registry-replay.py:204-205`, row `registry-replay-selftest` 10/10) does. K10 itself does not.
   The distinction matters: predicate weak, gate chain not blind.
6. The knowledge entry’s own row `:17` says refusal when “`cleanup_error` is set”, but K8 cannot
   isolate that condition (fixture sets both). Doc stronger than predicate.

## 6. Proposed move (one bounded, docs/evidence only)

**Make the denominator honest and make the promised after-receipt real.**

1. Append a `## Routed-defect disposition (round23 → round24)` section to
   `corpus/knowledge/replay-projection-hardening.md` carrying the 8-row table from §1, including
   the three declared non-predicates: R5 (recorded, not a predicate), R7 (size bound only;
   redaction and unbounded observations retention open), R8 (intentionally open by no-retrofill).
   One paragraph must state the count: **9 predicates / 6 routed defects, plus 1 adjacent
   expansion and 1 control**.
2. Persist the already-observed after measurement as `.ufo/evidence/round-24/after.json`: the exact
   JSON stdout of the `RunRulerAfter` run at `c8c5b88` (instrument `0a7f6daa…`, exit 0,
   `discriminated: 11`, `total: 11`), with the run argv/cwd/revision recorded the way
   `before.json` records its clone. Copy the observed object from the retained transcript; if the
   complete stdout was not captured, have an authorized seat re-run `measure.py` at `c8c5b88` and
   retain that output instead — do not reconstruct or paraphrase it.
3. While touching docs only, replace the README Ground cell with a scoped wording (eleven
   predicates for the argv/exit/pin/projection/stream-size/realpath gaps; runner-copy hash recorded;
   redaction and loose tokens open) and state R8 explicitly in the round-24 SCORECARD section
   rather than editing the round-23 block.

No tool bytes, registry rows, fixtures or bundles change, so no new replay, mutation sweep or
source re-anchor is required — this is the cheap half of the closure’s own deferral logic.

Affected axes: calibration (claim→evidence traceability; the primary axis), coverage
(disposition completeness for routed items), operability (a reader can stop guessing). No measured
surface (depth, freshness, adjacency) changes; no numeric uplift is implied.

Risks: (a) `after.json` must be the exact captured stdout of a retained run, otherwise it repeats
the “measured results recorded after execution” promise without evidence — if the seat’s capture
cannot be reproduced, leave it out and let the lesson say “not retained”; (b) the disposition
table must not be read as new capability; it explicitly records R6’s frozen-instrument latent
defect and R7/R8 partials; (c) if the L1 integrator prefers a single authority, put the table only
in the knowledge entry and link it from README/SCORECARD, never duplicate measured claims.

## 7. What I checked / did not run / installs

Checked read-only: all eight routed entries and the other adjudication buckets; `before.json`
rows (including full K1/K2/K3/K5/K6 rows); `measure.py` mutants, pins and fixtures; both extra-case
files; `command-binding.py` anchors and fixture loader; `registry-replay.py` projection, publish,
run and selftests; `registry-check.py` `held`/`cleanup_error`/non-hermetic semantics; the three
superseded and four active registry rows; the round-24 replay artifacts (43 rows, 41/2 split,
stream maxima, shas); knowledge entry, lesson, SCORECARD round23/24 sections, README row, MANIFEST
rounds[421] notes; round23 frozen replay instrument; round23 lesson limitation line.

Did not run: `.ufo/evidence/round-24/measure.py`, either selftest, any mutant, the registry battery,
`command-binding.py`, `registry-replay.py`, or any gate. Mutant outcomes labelled `[INFERENCE]` are
static traces, not observations.

Installs/updates: none. No pacman/uv/npm/cargo transaction was attempted (host pacman paused
anyway); no tool was needed beyond stock `python3`, `git`, `sha256sum`.
