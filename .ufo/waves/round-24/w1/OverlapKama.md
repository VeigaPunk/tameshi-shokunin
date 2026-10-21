# OverlapKama — kama/mori sibling scan: command receipts and wave accounting (round 24 C1)

Seat: TameshiR24-2.OverlapKama (connector, leaf — no subagent dispatch).
Delivered revision `c8c5b88c8e961a929cdc351b95a7074c76958909`; base
`6a1821a8897eea6e7d9669292160ec9593669409`; replay evidence measured at
`d2eaecd443bf5f4e387e7e5331282e3d11dea047` (tools byte-identical at both revisions:
`git rev-parse c8c5b88:tools/registry-replay.py` = `git rev-parse d2eaecd:…` =
`git hash-object tools/registry-replay.py` = `30feb147…`; same for
`tools/command-binding.py` = `1b4bbb77…`).

Hypothesis under test: *kama-shokunin or mori-shokunin owns a command-receipt or
wave-accounting surface that round 24 absorbs, duplicates, or contradicts.*

**VERDICT: refute** — no contested scope and no absorbed implementation. Neither
sibling has a `command-binding`/`registry-replay` artifact, no round-24 changed
path is a kama/mori path, and no active registry row executes a kama/mori byte
(evidence §1). The two repos do own *analogues* — a command-receipt validator
(mori) and three wave-accounting instruments — and those analogues are
mutually non-interoperable and structurally unable to settle round-24 w1
(§2–§3). That is a claim-scope fact for this wave's close, not a defect in
K1–K11 and not a claim of ownership.

## 1. No contested scope, zero kama/mori byte dependency

Observed (read-only):

```
$ git diff --name-only 6a1821a8897eea6e7d9669292160ec9593669409..\
c8c5b88c8e961a929cdc351b95a7074c76958909 | grep -E 'kama|mori'
(no output; grep exit 1)
$ … | wc -l
40
```

All 40 changed files are tameshi paths. A static scan of the 47 active registry
rows (argv and the script each argv names) for `kama-shokunin|mori-shokunin`
returns `hits: []`. The only `*-shokunin` glob in the tool tree is
`tools/registry-replay.py:67` (the `--plan` mirror, not a row); no row
dynamically enumerates the fleet. A targeted grep for `command-binding` or
`registry-replay` over `kama-shokunin/tools`, `kama-shokunin/.ufo/waves/round-21`,
`mori-shokunin/tools`, `mori-shokunin/.ufo/waves/round-21` and
`…/round-22` returns zero hits for either name; the only schema hit is
mori's own `mori-r21-command-receipt-v1` consumer
(`mori-shokunin/tools/mori-retention-reconcile.py:169`). The replay clone's
fleet mirror does symlink kama and mori (`tools/registry-replay.py:63-69,161`),
but **no row names them**; the current kagi instance of that mechanism is
already reported and scoped by `OverlapKagi.md` §4 and the errata's Further
bounds, and is not re-claimed here.

Calibration anchor read, not run: `.ufo/evidence/round-24/after.json`
(post-revision, untracked) records `"discriminated": 11`, `"exit": 0`,
`"revision": "c8c5b88…"`, argv from `/tmp/tameshi-r24-after-FKSm/lane`.
Nothing in this scan changes that number.

## 2. Command-receipt family: three vocabularies, fail-closed, untested boundary

| | tameshi `command-binding-v1` | mori `mori-r21-command-receipt-v1` | kama (analogue only: `kama-llamacpp-live/v3`) |
|---|---|---|---|
| object | declared command receipts | derived gate receipt + committed inputs | runtime server observation |
| shape | exact key set `{name,argv,cwd,revision,exit,stdout,stderr}` (`tools/command-binding.py:88`) | wrapper keys `argv, cwd, elapsed_seconds, exit_code, measured_revision, schema, started_utc, stderr, stdout` (16 `mori-r21-command-receipt-v1` files among the 24 JSONs under `mori-shokunin/.ufo/waves/round-21/evidence/final/`) | v3 receipt; not a command receipt |
| revision | exact 40-hex equality `receipt.revision == bundle.revision` (`:31,:107`) | `merge-base --is-ancestor measured revision` (`mori-retention-reconcile.py:175`), OID 40 **or 64** hex (`:20`) | sha256 artifact pins |
| trust anchor | caller-owned digest of the whole bundle (`:11,:126`, `SNAPSHOT_TAMPERED`) | committed blob equality at the measured revision (`:177`) plus bound `--repo/--policy/--allowlist/--rev` options (`:184-196`) | self-reported digests |
| unknown/extra keys | rejected (exact set) | named fields validated; no exact-key-set check found in `check()` | accepted: kama's own critic records `m1 unknown server key; m2 unknown top-level key` both exiting 0, and that the gate docstring's exact-key claim is false (`kama-shokunin/.ufo/waves/round-21/falsify/advice/C2GgufReceiptCompat.md:30,42`) |

Consequence: neither lane can validate the other's artifact. Feeding a mori
r21 wrapper to `command-binding.py` fails the schema test
(`tools/command-binding.py:67-68`) → exit 2 `INVALID_BUNDLE`; feeding a tameshi
bundle to mori's reconciler fails `receipt_schema` (`:169`) → could-not-evaluate.
Both directions fail closed. [INFERENCE: static trace of those two checks; not
executed — this item has no Run clause.]

The gap is that **no predicate or fixture asserts this**. The 44-case public
selftest (17 literal + 19 round-23 + 6 round-24 + 2 tail; `after.json` K1 kill
is `CASE argv-swapped-between-names FAIL`) covers an *extra* receipt key
(`unknown-receipt-key -> 2 INVALID_RECEIPT`), not a *renamed* vocabulary.
A future refactor that admitted `exit_code`/`measured_revision` aliases would
have to widen the allowed key set, and no current case would fail. The
44-case count and the unpinned state of `extra-cases.json`
(`sha256 6ad7842f…`, CodeFixtureLoader M3) mean the cheap fix is **not** more
fixtures in this wave.

## 3. Wave accounting: three fleet accounting tools plus mori's census, four independent reasons none settles w1

Round-24 w1 contains exactly one JSON, `.ufo/waves/round-24/w1/swarm-registry.json`
(schema `ufo-swarm-registry-v1`), plus seat `*.md` reports (58 at
2026-10-21T16:41:39Z). It has no `spec.json`, no `assignments.json`, no
`dispatch.json`, no `completion-summary.json`, no `verdict-count.json`.

| instrument | inputs it can read | output | round-24 w1 |
|---|---|---|---|
| `kama-shokunin/.ufo/waves/round-21/wave-accounting.py:28-29,49-50` | `<wave>/spec.json` + `assignments.json` (no existence guard) | writes `completion-summary.json`, `verdict-count.json` into the wave dir; first `VERDICT:` line per report (`:16-18`) | fails on the missing files; would not read the registry at all |
| `tameshi-shokunin/tools/wave-accounting.py:70,85,113-117,122` | `wave-accounting-v1` bundle: members with non-empty `name,id,role`, outcomes with `status`, unique `reports`, declared `claimed` totals | digest-pinned report; authority fixed to "declared retained callbacks; report presence never completion" | the registry has `agentId: null` and `item: null` for **64/64** members, no outcomes and no `claimed`; projecting a bundle from it would fail `string(id)` (exit 2), and synthesizing outcomes from report presence would contradict `:122` |
| `mori-shokunin/tools/mori-wave-settlement.py:33-36,100-131,333-347` | only `ufo-swarm-wave-dispatch-v1` JSONs; every other parseable JSON increments `ignored_json` (unparseable ones increment `unreadable_json`) | per-seat `present/empty/stub/missing/misrooted/unsafe/unparsed`, wave `settled/partial/unsettled` | round-24 has **0** dispatch-schema files (23 exist in rounds 12–23), so w1 contributes no wave row; its registry lands in `ignored_json` |
| `mori-shokunin/tools/mori-census.sh:879` (`probe_waves`) | `<lane>/.ufo/waves/*` directories; the loop `continue`s on `round-*` and dot-prefixed names | `waves` surface tokens | every `round-*` directory is skipped, so round-24 is invisible even as an unsettled wave |

Both mori readers are silent, kama's is loud, and tameshi's own gate is
inapplicable. No sibling accounting can be cited as corroboration of w1
completeness, and `58/64` is a filesystem count — missing reports are not dead
seats (mori's own rule and tameshi's `:122`), and the six missing at the
timestamp may still be running.

For scale comparison only: kama's round-21 `build/completion-summary.json`
reports `spawned 86, with_report 85, dead [], no_report ["RegressSkillGates"]`;
mori's own round-21 settlement observed `members 802, present 709, missing 91,
waves 13` (`mori-shokunin/.ufo/waves/round-21/evidence/final/wave-settlement-observed.json`).
These are different denominators and are not comparable to w1's 64.

## 4. Contradictions, stated not smoothed

- **C1.** Mori's instruments are province-level (`mori-shokunin/PROVINCE.md:23,145-153`)
  and both exclude tameshi's `round-*` layout by construction; kama's
  accounting script is round-local and needs two files tameshi never writes.
  "Wave accounting exists in kama and mori" is true and is not evidence about
  w1: the fleet has three member/accounting vocabularies and none consumes
  this wave's artifacts.
- **C2.** `command-binding-v1` is fail-closed against foreign receipts in code,
  but the boundary is untested; `unknown-receipt-key` covers addition, not
  renaming/aliasing.
- **C3.** The w1 registry records intent (`kind: spawn`, `role`, `axes`) but no
  join key (`agentId`, `item` all null) and no `updatedAt` after creation
  (`createdAt == updatedAt == 2026-10-21T16:05:40.614Z`). Tameshi's own
  accounting reconciles `member.id` against `outcome.id`; with null ids that
  reconciliation is inapplicable, and kama's `assignments.json` join is absent.
- **C4.** The clone fleet mirror exposes kama and mori to every row
  (`tools/registry-replay.py:67,161`) while `_argv_outside_fleet`
  (`tools/registry-check.py:632-645`) only inspects *absolute* argv tokens and
  the live rule is declaration/argv (`registry-replay.py:99`). Today zero rows
  use kama/mori (verified), so this is latent, not an instance; the errata's
  Further bounds already scope the mechanism for kagi. Do not read
  `revision_pinned` as "self-contained" on the strength of §1.

## 5. Affected axes

- **Calibration (claim scope)** — directly affected: the `41/2` split (already
  scoped by `OverlapKagi.md` §4 and the errata) and any wave-completeness
  reading of w1 must not be extended to cross-lane settlement.
- **Cross-lane composability** — unchanged; no interop is proposed, and the
  fail-closed refusals stay.
- **Discrimination (11/11)** — untouched; no predicate, fixture, tool or
  evidence byte changes in this proposal.
- **Evidence provenance** — untouched; no replay re-run is implied (a re-run
  would regenerate `expected.json` inside the same commit, which is the exact
  substitution pattern K5/K6 guard against).

## 6. Proposed move (one, bounded)

Append **one bullet** to the round-24 errata's existing "Further bounds"
section (`corpus/knowledge/replay-projection-hardening.md`, after the
`revision_pinned` bullet), routed through L1 — `CorpusErrataCarry` owns that
file this wave, so do not edit it concurrently. Draft text:

> **Cross-lane receipt/accounting is not interoperable (round-24 w1).** Three
> seat-accounting tools (plus mori's census wave surface) exist in the fleet
> and none can settle this wave:
> kama's `wave-accounting.py` needs `spec.json`+`assignments.json` (absent;
> `w1/` holds only `swarm-registry.json`); mori's `mori-wave-settlement.py`
> forms waves only from `ufo-swarm-wave-dispatch-v1` files (none in round-24)
> and would count the registry as `ignored_json`; `mori-census.sh:879` skips
> `round-*` directories entirely; and `tools/wave-accounting.py` needs
> non-empty member ids and declared `claimed` totals, while every registry
> member (64 at 2026-10-21T16:41Z) carries `agentId: null`/`item: null`.
> Report counts in `w1/` are
> filesystem observations, not settlement; do not synthesize outcomes from
> report presence. Likewise `command-binding-v1` is lane-local and rejects a
> `mori-r21-command-receipt-v1` wrapper by schema and key set — a code
> property, not a tested one (no predicate or fixture covers foreign receipt
> vocabulary).

This is a synthesis of `OverlapKagi.md` §4 (mechanism: declaration/argv, not
dependency analysis) with the kama/mori delta (no instances; the accounting
side is separate and also non-overlapping). One edit, no code, no digest, no
re-run. It introduces no new claim of interop, authentication or promotion.

## 7. Risks

- Doc-only: a future reader can still point a sibling tool at the lane and
  read silence; the bullet names the tools and lines so the misread is bounded.
- Quote no moving counts in the bullet beyond the timestamped observation; a
  bare `58/64` will be stale by close.
- Concurrent ownership: `CorpusErrataCarry` may be appending to the same
  section; L1 must serialize the edit.
- Do not add fixtures now: CodeFixtureLoader M3 (fixture unpinned) and
  MutFixtures (controls, not kills) make a passing foreign-vocabulary fixture a
  control, not a QUALITY48 repair; a K12 mutant belongs to the next contract.

## 8. Verification

Read-only checks, all reproduced during this scan (no battery, gate, ruler,
selftest or replay executed in the lane):

```
git diff --name-only 6a1821a..c8c5b88 | grep -E 'kama|mori'      # no output
python3 - <<'PY' … registry scan … PY                            # hits: []
ls .ufo/waves/round-24/w1/*.json                                 # swarm-registry.json
find .ufo/waves -name '*.json' -exec grep -l 'ufo-swarm-wave-dispatch-v1' {} +
                                                                 # 23 files, 0 in round-24
sha256sum .ufo/evidence/round-24/extra-cases.json                # 6ad7842f…
```

If the bullet lands: no code path changes, so `command-binding.py --selftest`
must still print `44/44 pass` (not run by me) and the ruler result remains the
recorded `after.json` 11/11 at `c8c5b88`. Re-check the bullet's four claims
with the commands above; all are structural, not measurement-dependent.

## 9. What was attacked (fresh falsification)

- *kama/mori implement or are absorbed by command-binding/registry-replay* →
  refuted: 0 hits for the two tameshi names/schemas in the targeted trees;
  0 changed sibling paths; 0 registry rows.
- *a sibling accounting tool can settle w1* → refuted by the two tools plus
  mori's census and tameshi's own gate (§3); both mori readers are silent,
  kama's is loud, tameshi's gate is inapplicable (null ids).
- *tameshi accepts a mori receipt (or vice versa)* → refuted by the schema and
  exact-key checks (`command-binding.py:67-88`, `mori-retention-reconcile.py:169`);
  static only.
- *a kama/mori instance of the hidden live-dependency class exists* → none
  found; the mechanism is latent (§4, C4).
- Checked and not a defect: kama's `report-landing-audit.py` audits fleet
  reports `.ufo/reports/round-N/kama.md`, not seat reports or wave membership;
  mori's `mori-dispatch-ledger.py` binds dispatch *payloads*
  (`payload_sha256/bytes/tasks_count`), not command receipts; `plan()`'s
  symlink/alias behaviour is already covered by MutPlan and LabPlanLaneLink.

## 10. Bounds and tooling

- Read-only. Commands used: `ls/find/grep/sha256sum`, JSON reads via `python3 -c`,
  `date`, and read-only git (`GIT_OPTIONAL_LOCKS=0 rev-parse/log/cat-file/
  hash-object without -w/diff`). No sibling write, no mutating git/jj, no
  `/tmp` clone, no registry battery, no ruler, no gate, no selftest, no replay,
  no subagent. The only write is this report (post-revision, untracked at
  `c8c5b88`, like the wave's other seat reports — ClosureCarry).
- Tools installed or upgraded: none.
- Peer seat reports cited here (`OverlapKagi.md`, `CodeFixtureLoader.md`,
  `MutFixtures.md`, `ClosureCarry.md`) are untracked wave artifacts at
  `c8c5b88`, used as context and never as repo receipts.
- Not claimed: producer authentication, promotion, historical R17-CMD-BIND
  closure, numeric score uplift, or kama/mori endorsement.
