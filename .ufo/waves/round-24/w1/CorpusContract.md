# CorpusContract — round-24 W1 critic (calibration)

Target: `.ufo/evidence/round-24/contract.json` (sha256 `9e681e1b…eb91113`), ruler `measure.py`
(sha256 `0a7f6daa…57daa64`, equal to `before.json` `instrument_sha256`), delivered rev `c8c5b88`.

## Verdict

**The contract is partly honest. The measured 11/11 stands as observed, but the claim overstates both
the number of predicates that moved and the number of mechanisms they cover. The bounds also leave
three gaps in what the ruler can show.** These are fixable text defects, and an append-only erratum
covers them. The frozen ruler and contract MUST NOT be changed.

1. **K4-as-control is honest in the evidence but not in the contract.** `before.json` says K4 "already
   discriminated at base". `SCORECARD.md:1134,1140-1141` calls K4 "the any-token control ... kept as a
   control". `contract.json` says neither: its claim is "harden ... against eleven" and its target is
   11/11. This round could move at most 10 predicates (0/10 → 10/10). K4 is a carried regression guard
   and a positive kill control for the mutant leg, not a hardening.
2. **The eleven predicates are not eleven distinct mechanisms.** They cover seven mechanisms, and only
   six of those are new in this round.
3. **The bounds do not disclaim three things the ruler cannot show:**
   - K9 shows only that the bundle is refused. Retained streams are still unbounded and unredacted.
   - K10 shows that at least one of its two triggers works, not that each one does.
   - Routed defects without a predicate (and K2, which was not routed) are not named.

## Evidence

### What holds (checked, no defect)

- **Freeze order.** `git log 6a1821a..c8c5b88 -- contract.json measure.py` returns only `e338f1b`
  ("freeze eleven-predicate hardening claim, ruler and before receipt"). The implementation landed
  afterwards, in `d2eaecd`. The current ruler sha256 equals the `before.json` instrument sha.
- **K5/K6 attribution.** At base, the unpinned rows held after substitution
  (`before.json`: K5 and K6 `substituted: true`). So a fail after the change can only come from the new
  `bundle_sha256` literal pins (`tools/registry.json:974,984`). It cannot come from a verdict change
  caused by the substitution. The rewritten `expected.json` has the same two keys as the originals
  (`schema`, `bundle_sha256`), so the rewrite adds no artefact. Each bundle path has exactly one active
  row, so the "any row fails" test does not hide an unpinned survivor.
- **K1-K4 anchors.** Each anchor string appears exactly once (`tools/command-binding.py:103,109,111`).
- **Bounds 1, 2 and 4** are accurate as written: four specific mutants, not mutation adequacy; changing
  both the row and the bundle means a new contract; calibration stays at 8.

### Mapping predicates to mechanisms (static reading; no mutant was executed because this item has no Run authorization)

| Mechanism | Predicates | Evidence of overlap |
|---|---|---|
| exact argv comparison | K1, K2 | two mutants of the same guard line, `command-binding.py:103` (`ARGV` anchor, `measure.py:24,28-31`) |
| exit comparison | K3 | — |
| all-of stdout tokens | K4 | already in place at base: round23 `all-of-tokens` case; MANIFEST `rounds[421]` closure: "all-vs-any ... killed by selftest all-of-tokens" |
| bundle digest pin | K5, K6 | the same `stdout_contains` `"bundle_sha256": "…"` mechanism on two rows |
| refusal to publish a projection | K7, K8, K9 | three triggers share one sink, `registry-replay.py:109-110` (`if findings: return 1, report, None`). Deleting that branch flips all three together |
| live-dependent listing | K10 | a single disjunction, `registry-replay.py:99` |
| realpath plan identity | K11 | `registry-replay.py:63-69` |

Concrete counterexamples. Each one passes the ruler predicate, derived from the code as written.

- **K8 is a label refinement of K7.** The K8 fixture sets `held=False` plus `cleanup_error`
  (`measure.py:173`). The real runner never produces a cleanup error on a row that held:
  `held = got == expected_exit and not missing and cleanup_ok` (`registry-check.py:720`). So K8 adds no
  refusal path beyond K7; it only checks which finding ID is emitted.
- **K10 cannot show that either trigger is needed.** `obs(external=True, non_hermetic_argv=[...])`
  sets both triggers in one row (`measure.py:181`). `obs()` sends every key except `external` into
  `runner_result` (`measure.py:151-155`). Deleting `row.get('external') is True` or deleting
  `result.get('non_hermetic_argv')` from line 99 still yields `live_dependent == ['one']`. Only the
  selftest cases at `registry-replay.py:204-205` separate the two triggers, and the ruler never runs
  that selftest.
- **K9 only checks the refusal side.** The ruler runs the over-limit case with `--max-stream-bytes 16`
  and the control with the default limit. The mutant
  `if max_bytes != DEFAULT_MAX or len(...) > max_bytes:` passes K9. It is killed only by the selftest
  case `stream-at-limit` (`registry-replay.py:203`), which the ruler does not run.

### Ruler blind spots that the bounds do not disclaim

- **Retained streams are still unbounded and unredacted.** The routed defect reads "Replay streams are
  retained without size bounds or redaction" (`.ufo/waves/round-23/fresh-adjudication.json:93`). In
  `--run` mode, the tool writes `observations.json` with the full streams before projecting
  (`registry-replay.py:181-184`). `run_row` captures stdout without any limit (`registry-check.py:693`,
  `retain_streams` at 724-726). The actual retained file is `.ufo/evidence/round-24/replay/observations.json`:
  265,728 bytes, with a largest single stdout of 8,110 bytes (`measure-round16-rev`). No redaction step
  exists. So K9 measures refusal to publish a bundle, not bounded retention. Three texts overclaim this:
  - the tool docstring, "each retained stdout/stderr is bounded" (`registry-replay.py:9`);
  - the knowledge row "unbounded retained streams" (`corpus/knowledge/replay-projection-hardening.md:18`);
  - the contract bounds, which are silent on it.
- **Routed items with no predicate, and one predicate that was not routed:**
  - Hashing the runner from the clone copy (`fresh-adjudication.json:81`) has no predicate. The knowledge
    doc line 21 admits "not a ruler predicate", but the contract does not. I spot-checked this item:
    `runner_sha256_clone_copy` `cba16646…` equals `git show d2eaecd:tools/registry-check.py | sha256sum`.
    It is consistent, but it is unmeasured.
  - Redaction (`:93`), loose stdout tokens (`:104`, kept by the frozen-argv rule), and the closure's
    "re-run guard sweep" and "dead-falsifier coverage gap" (MANIFEST `rounds[421]`) also have no
    predicate.
  - K2 (casefold) is not a routed defect. Round23 recorded "exact-list argv ... no normalization" as an
    agreement (`fresh-adjudication.json:124`). Even so, the contract's `sources` line attributes all of
    K1-K11 to the routed defects.
  - The knowledge table lists "stripped or de-duplicated" argv as hardened by the padded-token and
    repeated-flag fixtures. No predicate measures a strip or de-duplication mutant.
- **Live-dependent listing is incomplete by construction.** A row is listed only if it is declared
  `external` or has an absolute argv token under the fleet root (`registry-check.py:633-646,662-671`).
  Sibling reads inside a tool are not seen. Example: the `bash-witness-count` default
  `REPO.parent / "kagi-shokunin"` (`tools/bash-witness-study.py:94-97`) resolves through the clone's
  live-sibling symlinks and is read by `git -C kagi show REV:path` (`:348`). Its content is pinned by a
  `PIN_BASH` digest check (`:864-866`), so the bytes are fixed. Its availability still depends on the
  live sibling repo, yet the actual replay counts it under `revision_pinned: 41`
  (`replay/live-dependent.json`, which lists only 2 of 43 rows). Bound 3 ("an actual replay run is
  separate evidence") does not say that the listing is based on declarations and argv tokens only.
- **Minor: the contract does not record the ruler's own hash.** Only `before.json` carries
  `instrument_sha256`. Today it matches, so this is a provenance gap, not a defect.

## Impacted axes

- **Calibration (judged).** The movement should be read as 0/10 → 10/10, with K4 as a carried control,
  covering six newly hardened mechanisms. It should not be read as eleven independent hardenings.
  Bounded stream retention and the clone-copy runner digest remain open or unmeasured.
- **Other axes:** no harm found from the contract text.

## Smallest safe correction (text only, append-only; do not touch the frozen contract or ruler)

Append an erratum to `corpus/lessons/round-24.md`, the SCORECARD round-24 section, or both, stating:

1. "Ten predicates were movable (0/10 → 10/10). K4 is a regression and positive-kill control carried
   from round23."
2. The mechanism grouping above: K1/K2 share one argv guard; K5/K6 share one pin mechanism; K7/K8/K9
   share one refusal sink; K10 is a disjunction measured only as a whole.
3. "K9 measures refusal to publish a bundle. `observations.json` still retains full, unredacted streams
   (routed defect open)." Correct `registry-replay.py:9` and knowledge row 18 to match.
4. A list of the routed items that have no predicate: clone-copy runner digest, redaction, loose stdout
   tokens, guard sweep re-run, dead-falsifier gap. Also note that K2 is an extra, not a routed defect.
5. "`live_dependent` covers rows that are declared external or have an absolute fleet-path argv token.
   Sibling reads inside a tool, such as bash-witness-study's default kagi path, are counted as
   revision-pinned."

Next contract: record `instrument_sha256` in the contract. Add one-trigger-only K10 fixtures, an
at-limit acceptance case for K9, exact finding-set equality for K7/K8, and a predicate on the size of
retained `--run` streams.

## Scope

- Read-only inspection only. No commands were run in the lane beyond read-only `git log`/`git show`/`git
  rev-parse` (`GIT_OPTIONAL_LOCKS=0`), `sha256sum`, and read-only Python JSON reads. No mutants,
  selftests or gates were executed.
- Only this report was written.
- Tool installs or updates: none.
- Not claimed: producer authentication, promotion, closure of R17-CMD-BIND, or any numeric score uplift.
