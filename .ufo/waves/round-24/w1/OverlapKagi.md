# OverlapKagi — kagi-shokunin sibling-overlap scan (round 24 C1)

Read-only scan of `/home/vgpnk/Projects/shokunin/kagi-shokunin` against the
round-24 changed surfaces. No lane write, no registry battery, no gate or
selftest executed in the lane; kagi was read as files plus read-only git
(`GIT_OPTIONAL_LOCKS=0 cat-file`/`rev-parse`/`rev-list`). No tools installed.

## Verdict

**No contested scope.** kagi-shokunin owns neither required-command binding,
nor a command-entry registry, nor a registry replay projector. Its round-24
digest-pinned rows pin *its own* corpus memberships and this round absorbs
none of them. The only kagi material inside the round is two pinned kagi gate
blobs (kagi `fecee874`) consumed by two tameshi rows. One of those rows is
mis-described by the round's live/revision split; the other is declared. That
is an attribution defect in tameshi's projection, **not** a kagi ownership
claim and not a numeric-score event.

## 1. What kagi actually owns (and what the words mean on each side)

- kagi's "registry" is the **source** registry: `corpus/SOURCES.md`
  (S001–S043; `grep -oE '^\| S[0-9]{3}' corpus/SOURCES.md | tail -3` →
  S041, S042, S043), gated by `corpus/sources-census.sh`
  (`kagi-shokunin/PROVINCE.md:55`).
  tameshi's `tools/registry.json` is a **command-entry** registry
  (`schema: tameshi-entry-registry-v1`; 54 live rows). Same word, different
  object; no shared artifact or ID space.
- kagi has no required-command-binding and no command-registry replay:

  ```
  $ grep -rn -i 'command-binding\|registry-replay' --include='*' \
      /home/vgpnk/Projects/shokunin/kagi-shokunin | grep -v '\.git/'
  (no output)
  ```

  It does have two wave-local "replay" instruments, both over kagi's own
  frozen evidence — `.ufo/waves/round-24/tools/normalizer-replay.py` (reopens
  the frozen capture rows; compares normalizer digests) and
  `.ufo/waves/round-26/tools/replay-current.sh` (verifies the rearmed
  snapshot manifest, then replays the current/historical clock profiles).
  Neither reads a registry, a command, or a tameshi artifact. The term
  "replay" collides lexically with this round; the objects do not.

- kagi round-24 digest-pinned rows are membership identity over kagi's own
  corpus: `R24-01`/`R24-02` selftests and `R24-03`…`R24-16` count+sha256
  identity rows (`corpus/claim-ledger.tsv:64-79`), helper
  `corpus/row-identity.sh` (122 lines), `corpus/inrow-pins.tsv` (22 lines),
  normalizer `corpus/rendered-text-v1.py`
  (`kagi-shokunin/PROVINCE.md:55-56`). Every projection reads kagi files;
  none reads tameshi bytes.
- kagi's connector already treats tameshi's pin as the *precedent to borrow*,
  not as kagi property: `.ufo/waves/round-23/falsify/ConnClosurePatterns.md:168`
  describes tameshi `tools/evidence-disposition.py` ("every input path pinned
  to sha256 … never executes receipt argv"), `:182` proposes "the compatible
  synthesis is tameshi's byte pin", and `:254-258` warns the pin "does not
  create external authority … Do not sell the pin as authentication." The
  borrowing direction is kagi → tameshi.

## 2. Round-24 changed nothing on the kagi side

`git diff --stat 6a1821a8897eea6e7d9669292160ec9593669409..c8c5b88c8e961a929cdc351b95a7074c76958909`
= 40 files, all tameshi paths (`tools/registry-replay.py`, `tools/command-binding.py`,
`tools/registry.json`, `corpus/knowledge/replay-projection-hardening.md`,
`corpus/lessons/round-24.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`
S084/S085, `SKILL.md`, `SCORECARD.md`, round-24 evidence). No kagi path, no
kagi-derived row, no kagi source row. kagi's own round-24 (host-safe ledger
entry points, normalizer re-capture, identity rows — `plans/round-24.md`) is
parallel work on a different object; kagi rounds 25–27 continue on self-counts,
lone-clone layout, release clocks — no replay claim.

## 3. The real cross-repo surface: two pinned kagi blobs

tameshi pins kagi `corpus/surface-census.sh` and `corpus/checklist-run.sh` at
`fecee8743e52eb8fb5fbb40782934cb619a1a96e`:

- `.ufo/evidence/round-13/pin-manifest.json:19-27,43-51` (`pinned_commit`,
  `expected_sha256`);
- `tools/mutate-and-run.sh:599-606` (`PIN_BASH`/`REV_BASH`,
  `PIN_CHECKLIST`/`REV_CHECKLIST`), consumed at `:1319-1337`;
- `tools/bash-witness-study.py:97-100` (derives the same pins from the runner).

Live check today (read-only), kagi HEAD `3553d499577084a6c98d7078906017840bbf7b28`:

```
$ git cat-file blob fecee874:corpus/surface-census.sh | sha256sum
275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f  -
$ git cat-file blob fecee874:corpus/checklist-run.sh | sha256sum
7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf  -
$ git rev-list --count fecee874..HEAD
69
```

Both blobs resolve exactly to the manifest digests; kagi is 69 commits ahead,
so the pins are historical content, live **availability**. No drift.

## 4. Falsification result — the "41 revision-pinned / 2 live-dependent" split does not cover `mutate-and-run-regression`

The delivered surfaces state the number:

- `SCORECARD.md:1094-1097`: "The replay is 41 revision-pinned rows plus 2
  live-dependent rows, not an isolated clone."
- `SKILL.md:2033-2041`: same 41/2, with "the clone symlinks live sibling
  repos".
- `.ufo/evidence/round-24/replay/live-dependent.json`: `live_dependent =
  [pin-disposition-read, verify-round15]`, `revision_pinned: 41`, `rows: 43`.

Counterexample, from the retained bundle itself:

- `.ufo/evidence/round-24/replay/observations.json:883` — the
  `mutate-and-run-regression` receipt has `external: false`,
  `non_hermetic_argv: None`, `revision: d2eaecd…` (the tameshi clone), and its
  stdout contains
  `REGRESSION_PIN bash-surface-census: source=git repo=/tmp/tameshi-registry-replay-dzo3ypiq/fleet/kagi-shokunin rev=fecee874… path=corpus/surface-census.sh mode=100755 sha256=275d8294…`
  and the same for `bash-checklist-run` (`rev=fecee874…`,
  `sha256=7e5ec98b…`). It ran 10+15 mutants against kagi's two blobs.
- Mechanism: `tools/registry-replay.py:160-161` symlinks every sibling into
  the clone's temp fleet; `tools/mutate-and-run.sh:1287` sets
  `FLEET_ROOT=$(dirname "$(dirname "$(dirname "$SELF")")")` — the clone's
  parent fleet — and `:1104-1136` materializes each leg from that symlinked
  repo's object store, with a repo-identity guard and pin check.
- Why the projection misses it: the rule is declaration/argv-based, not a
  dependency analysis — `tools/registry-replay.py:99-100` lists
  `external is True or non_hermetic_argv`; `tools/registry-check.py:632-645`
  only inspects absolute argv tokens, and this row's argv is
  `bash tools/mutate-and-run.sh --regression`. `pin-disposition-read` is
  listed only because its argv carries the absolute fleet root
  (`observations.json`, `non_hermetic_argv: ["/home/vgpnk/Projects/shokunin"]`).
- Structured-field check: a JSON walk of `observations.json` finds `fecee874`
  only under `/rows/5/runner_result/stdout*` (pin-disposition-read) and
  `/rows/17/runner_result/stdout*` (mutate-and-run-regression). No receipt,
  requirement, plan or top-level field carries a sibling revision; the top
  level holds only `revision`, `plan` (paths), `runner_sha256_clone_copy`,
  `registry_sha256`, `source_requirements_revision`.

**Contradiction, stated not smoothed.** `pin-disposition-read` and
`mutate-and-run-regression` have the same *availability* dependency on kagi's
object store; only the first is listed as live. `pin-disposition-read` does
additionally observe live HEAD/branch (`head_differs_from_branch`), which is a
defensible reason to call it live — but that distinction is written nowhere,
and the bundle's structured fields never record `fecee874`: the kagi revision
the row actually executed appears only inside the receipt's free-text stdout.
A reader who takes `revision: d2eaecd…` as input identity is wrong about the
gate bytes by the whole kagi delta.

Severity: **fail-closed**. If kagi lost `fecee874`, the row would SETUP-fail
(`mutate-and-run.sh:1124-1136`) and the replay would refuse to publish. K1–K11
are unaffected — K10 is a synthetic fixture and `contract.json` bounds it as
such; this is a label/attribution error in a number repeated in SKILL and
SCORECARD, not a green-gate defect and not a score claim.

## 5. Checked, no defect found

- No kagi pin of tameshi bytes: kagi's ledger/stamps/revision-audit read kagi
  files; tameshi appears only in kagi wave evidence, never in a kagi gate row.
  The dependency is one-way (tameshi → kagi object store).
- kagi selftest/case-count claims (`claim-ledger` 170, `sources-census` 70,
  `scope-gate` 61, `rendered-text-v1` 22; `PROVINCE.md:51-56`) are kagi-local;
  none is consumed by any round-24 surface.
- `.ufo/evidence/round-13/pin-manifest.json` `derived_from.sha256 =
  75ed934d…` ≠ current runner `d22c4025…`, but that cell is a round-13
  historical snapshot (`.ufo/evidence/round-13/verification.json:12`,
  `.ufo/evidence/round-13/expected.json:12`) and the
  manifest is declared "configured pin authority … not an adversarial
  baseline-authentication gate" (`tools/pin-disposition.py:22-27`). Not a
  defect; the manifest's provenance cells are simply not re-checked live.
- Both frozen bundle literals match the bytes they claim:
  `sha256sum .ufo/evidence/round-23/replay/bundle.json` → `3d6c99b7…`,
  `source-read-bundle.json` → `db620668…`, equal to the two row literals in
  `tools/registry.json` and to the two `expected.json` files.

## 6. Affected axes, second-order

- **Contract/calibration** — the 41/2 sentence is the load-bearing number; its
  "revision-pinned" half contains a row whose executed inputs live in another
  repo at another revision. Nothing else in the round changes.
- **Substrate** — kagi's custody boundary is intact (no writes, kagi copies
  mutated in tameshi scratch, absorption stays with kagi per
  `tameshi-shokunin/PROVINCE.md:14-18,45`). The gap is documentary, not a
  write.
- **Verification** — K10 proves the listing *mechanism*; the real-registry
  population remains outside the frozen predicate, and this row is the
  instance that shows why the population cannot be read as complete.

## 7. Proposed move (one, bounded) and smallest safe correction

**Documentation-only, now:** add one sentence to
`corpus/knowledge/replay-projection-hardening.md` §Bounds (and, if the
integrator wants the number self-explaining, one clause to the SKILL.md
round-24 line):

> `live_dependent` is declaration/argv-based, not a dependency analysis: a row
> can reach a live sibling through the clone's symlinked fleet mirror
> (`tools/mutate-and-run.sh:1287`) with no absolute argv token, so
> `revision_pinned` means "not declared live", not "self-contained". The
> sibling revisions such a row executes appear only in its retained stdout
> (`REGRESSION_PIN`), not in the bundle's structured fields.

This changes no code, no registry digest, no evidence byte, and no predicate.

**Code option for a later round (not now):** set `"external": true` on
`mutate-and-run-regression` in `tools/registry.json`. It cannot affect K1–K11
(K10 uses fixtures) and it is fail-safe (no absolute token, so no execution
change), but it changes `registry_sha256` and the next run's split
(41/2 → 40/3). That needs its own row and migration; do not retro-edit the
frozen round-24 bundle, and do not present the changed split as a score move.

## 8. Risks of the move

- Doc-only leaves the figure 41 as-is; a reader may still cite it as hermetic.
  The sentence names the instance so the error is bounded, not hidden.
- The `external` flag would improve attribution but invalidate cross-round
  comparability of the split; it must be declared, not silently applied.
- Neither correction may be read as producer authentication or as kagi
  endorsing tameshi's replay — kagi's own connector already refuses that
  reading (`ConnClosurePatterns.md:254-258`).

## 9. Bounds

- Read-only. Commands used: `grep`, `sha256sum`, `git cat-file/rev-parse/
  rev-list` (kagi, `GIT_OPTIONAL_LOCKS=0`), `git diff --stat` (tameshi), and
  reads of retained JSON. No registry battery, gate or selftest was executed
  in the lane. No sibling write, no jj/git mutation.
- kagi host/vault scope was not inspected; it is outside this item.
- No producer authentication, promotion, historical closure or numeric
  uplift is claimed.
