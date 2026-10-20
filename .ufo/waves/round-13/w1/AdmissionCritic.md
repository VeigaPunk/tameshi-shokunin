# AdmissionCritic — round 13 w1 (critic seat; advisory, lane-internal)

This seat was dispatched by the lane, so its review counts as same-lane review (`.ufo/waves/round-13/spec.json` context: "Reports advisory, not outside admission"). It does not admit, reject, verify or promote anything.

**What I did:** read-only work. I ran `git show`/`rev-parse`/`merge-base`/`status`/`log`/`diff` and hashed blobs and files, in tameshi and in the four sibling repos. I ran no gates, selftests, builds, or `measure.py`.

**Observation window:** 2026-10-20 01:45–01:55 (-03:00). L1 and the executors were writing at the same time. **Installs:** none.

**Axes:** depth (the lowest owned axis, tied at 6), calibration (6), and harm checks on the other four AXES axes. I also checked the authority boundary (outside closure versus same-lane review) and scalar non-inflation.

## Verdict summary

Shape conforms:
- 2 claims, on distinct axes.
- C1 depth works the lowest owned axis. Depth and calibration are tied at 6, so C2 also qualifies.
- Both owned axes are below saturation 8, so no nudge waiver applies (`SCORECARD.md` Saturation).

Scalars stay honest:
- No edit touches `tools/mutate-and-run.sh`, `SHONEN.md`, or the round-12 evidence. `git diff --quiet 546b371 -- .ufo/evidence/round-12 tools/mutate-and-run.sh SHONEN.md` was clean at 01:50.
- So command D still reads 6 cases and command C still reads boxes 1/2/4 = 6.

Remaining defects, in order of severity: D1 axis attribution, D2 the lesson pre-claims runtime evidence, D3 the probe's snapshot is not re-derivable, D4 a second status vocabulary. The `before` tautology (D0) has been accepted and corrected by L1.

## Findings

### D0 — C1 `before` was tautological (fixed by L1, keep it fixed)

**Original defect:** `claims.json` C1 `before` reads "six recorded legs have no round-13 explicit content disposition record". That is true of any round-N record before round N.

**Prior art the claim omitted:** a hand-run six-row pin read already exists:
- `corpus/knowledge/fleet-kill-rate-ledger.md` §ER-3/§ER-4: `LEDGER: 6 cases in; target current=4 stale=2 drift=0`.
- The `SCORECARD.md` round-11 row.

**L1 has fixed this:** `claims.json` now carries a `measurement_refinement` that keeps the original text and states the historical 6 rows. `measure.py` adds `pin_probe_artifact`.

**Condition:** the round report and SCORECARD must cite the refinement, not the raw `before` string.

### D1 — "artifact 0→1" counted under depth is an operability observable (medium; a tradeoff the judge must see)

**The issue:**
- AXES defines operability as "Runnable artifacts … scripts that run".
- AXES defines depth as "Verifiable technical detail — decision tables with real thresholds, named error signatures, cited sources".
- The refined C1 counter is "runnable structured pin-disposition method (artifact 0 -> 1)" plus six statuses.
- **Counterexample:** a probe that emits six rows the lane already hand-read in ER-4 adds no new technical detail by itself. The 6 is fixed by construction, because the manifest is derived from the six legs.
- `result_reuse` is the constant `not_established` (`tools/pin-disposition.py:91`), so "reuse decisions classified 0→6" cannot fail. A constant must not be counted as a measured classification.

**Precedent:** round 12 C1 counted `repeat_control_artifact` 0→1 under calibration. The outside closure accepted it as "calibration improved (capability)" (`lessons/round-12-verifier-spotcheck.md`, C1 verdict). So this framing is admissible, but it is not a measurement of depth itself.

**Smallest correction** (record, don't re-plan):
- Type C1's tool as a capability/probe, per AXES §Capabilities.
- Base the depth before→after on depth-shaped content:
  - the F7 method's source-quoted blind-spot table and the boundary between disposition and re-sweep (`corpus/knowledge/incremental-pin-disposition.md` §3–§5);
  - the six **observed** statuses, which can fail.
- Give operability an explicit verdict with a reason. For example, "unchanged — new probe recorded as capability, not counted twice".

**Real, non-tautological finding the after-state should state:**
- **js-kimi-census:** read `current` at round 11 (ER-4). It is now changed: kumitate `1a8eed5` (2026-10-19T19:41-03:00) moved `scripts/kimi-census.mjs` to HEAD blob `5e8d5913…`, and no tameshi record noted it.
- **My read at 01:47** (independent of the probe; L1 must re-read):

  | Leg | Pin | HEAD blob = worktree | Status |
  |---|---|---|---|
  | kimi | `83016d45` | `5e8d5913` | changed |
  | surface | `275d8294` | `275d8294` | unchanged |
  | tsukuroi | `084951be` | `d17d32a3` | changed |
  | mado | `d7edaab4` | `037b05dc` | changed |
  | checklist | `7e5ec98b` | `7e5ec98b` | unchanged |
  | claims | `e9a21b44` | `e9a21b44` | unchanged |

- All six pin blobs hash-verify at their REV.
- All six pinned commits are ancestors of HEAD.
- All six target paths have a clean porcelain status.

### D2 — The lesson cites runtime evidence that does not exist (high if committed as is)

**The issue:** `corpus/lessons/round-13.md:38` (Mistakes, row 1) says "Runtime evidence below records the same checker rejecting the null-only companion and accepting the kind-only repair."

**Counterexample:**
- The lesson's only sections are Gate, Mistakes, Routed-item dispositions, and Dispatch and authority (`grep '^## '`). None is a runtime section.
- At 01:55, `.ufo/evidence/round-13/` held only `before.json`, `claims.json`, `measure.py`, `pin-manifest.json`. There is no `witness-metadata.json`, no `pin-dispositions.json`, and no verification receipt.
- `corpus/README.md` (new round-13 block) cites both missing JSON files as evidence.

**Rules this breaks:** QUALITY criteria 8 and 9, and AXES "a capability without a passing demonstration … is pre-claiming".

**Correction:** commit only after the cited receipts exist in-repo with the executed exits and IDs. Otherwise, mark the rows "pending, not run".

### D3 — Probe rows are a moving-target snapshot without an observation time (medium; owner PinProbe, messaged)

**Evidence that the targets move:**
- mado HEAD moved to `95cbc41` ("round-13: protocol boundaries…") at 01:46:14 -03:00, during this round.
- The siblings are running their own rounds.

**What the probe already does well:** it records the HEAD commit per row (`tools/pin-disposition.py:292-325`), so a non-author can recompute the HEAD blob with `git show <commit>:<path>`.

**What is missing:**
- There is no observation timestamp field (grep for `observed_at` or a UTC field finds nothing).
- There is no `worktree_equals_head` flag. Without it, a closure cannot tell whether a worktree observation can be replayed from the object store.

**Correction:**
- Record the UTC time per run, and `worktree_sha256 == head.blob_sha256` per row, in the committed receipt.
- A later live re-run that differs is a newer reading, not a falsification. The re-derivable check is the object-store replay at the recorded HEADs.

### D4 — Second status vocabulary without a crosswalk (low–medium; owner PinProbe, messaged)

**The issue:**
- The established reading is ER-3: `current` / `stale` / `drift`, with an ancestry check (`fleet-kill-rate-ledger.md` §ER-3, §ER-4 command set).
- The probe's `content_status` is `unchanged` / `changed` / `unavailable`, derived from the worktree versus the pin (`:413-424`). It has no `merge-base --is-ancestor` check.
- So `changed` merges three distinct cases: stale (pin is an ancestor of HEAD), drift (dirty worktree), and a non-ancestor/rewritten history.

**Correction:**
- Add a crosswalk in the knowledge entry or the receipt:
  - unchanged ≈ current, when clean and HEAD = pin;
  - changed with HEAD ≠ pin and pin an ancestor ≈ stale;
  - worktree ≠ HEAD ≈ drift;
  - unavailable = SETUP-refusal class, with no ER-3 equivalent.
- Optionally add an `ancestor` field.
- The knowledge entry §3 already names both vocabularies. It needs the mapping, not a new authority.

### D5 — Source counts: one URL, two rows (low; acknowledged by L1)

- S041 went queued→mined, and S047 (same PIT URL) was added as mined.
- `measure.py` will therefore show rows 44→45 and mined 15→18 (S003, S041, S047) from **2 distinct URLs**.
- The Sources & frontier section must state this and must not present 45 rows as new ground. L1's `measurement_refinement.source_correction` already does; carry that into the report and SCORECARD.

### C2 — Calibration repair (conforms as far as inspected)

**What the gate does** (`tools/witness-metadata.py`):
- It pins `summary.json` `acc01268…`, `declaration.json` `e8d2024a…`, and `declared.tsv` `0def0d3b…` at `:68-84`. These match my `sha256sum` of the committed frozen files.
- It requires the frozen nested `kind` to **remain** null (`:330-332`), so the historical fault is preserved and not silently repaired.
- It requires the normalized kind to be exactly the frozen top-level string (`:316`, `:360`).
- It rejects a blind upgrade with `blind_upgrade_rejected` (`:387-388`), and requires `prior_exposure` to be True (`:383-384`).

**Root cause:** the producer reads `declaration.get("declared", {}).get("kind")` (`tools/bash-witness-study.py:787`). The top-level key is `kind`.

**Conditions:**
1. The red-before is a constructed old-null companion. The actual baseline state is "companion absent" (`measure.py` `metadata_companion_present: false`, exit 2 class), not exit 1. State both literally and keep them separate.
2. Do not patch `tools/bash-witness-study.py` this round. That would change a tool whose SHA round-12 receipts cite. It is outside every assigned write path.
3. Calibration stays 6→6. "Improved" is a lane assertion pending the round-13 outside closure.

## Outside closure versus same-lane review

| Item | Status | Anchor |
|---|---|---|
| Round-12 claims admitted | Outside, non-author, round 12 only | `lessons/round-12-verifier-spotcheck.md` "Closure: status ok; admitted true" |
| Routed item 3 (null kind, brittle planner cite) | Outside **routing** of work; does not pre-admit the round-13 fix | same file, Routed defects 3 |
| All 32 round-13 seats, including this one | Same-lane, advisory | spec context; `lessons/round-13.md` "All dispatched round13 seats remain part of tameshi" |
| Round-13 admission, admit/reject sample, discernment trend | Pending a fresh non-author closure | AXES "discernment is checked from outside"; round-12 spot-check table row "Lane-dispatched review is outside authority → reject" |

**Conditions:**
- Round-13 discernment must read `unprovable-but-better` or pending. It must not inherit round-12's "discernment improved".
- No SHONEN `[x]`.
- `README.md` round-13 block line "corrected in this round's new evidence" should read "lane-corrected, pending outside closure".
- `lessons/round-13.md:50` says "One validated wave". If a second wave is dispatched, append the count; that was round-12's F2 mistake.

## Harm check (L1 re-runs at the round commit)

| Axis | State observed | Risk |
|---|---|---|
| depth | runner unchanged; command D 6 | D1, D2 |
| calibration | SHONEN unchanged; criterion 14 appended; frozen bytes clean | D2 (pre-claim) |
| operability | two new tools, no capability rows yet | a capability row without a receipt |
| freshness | probe shows 3 changed legs | must read "unchanged (observation only; no re-pin, no re-sweep)". Stale re-sweeps stay open; README already says so |
| coverage | no new surface | none |
| adjacency | sibling porcelain clean on all six target paths; probe uses `git -C` reads only | none observed |

## Exact checks for L1 (not executed by me)

1. Scalars and observables:
   - `python3 .ufo/evidence/round-13/measure.py --rev 546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50` must match `before.json`.
   - Then `--rev <after>`. Expect `recorded_cases=6`, `unique_recorded_gates=6`, `calibration_restraint_score=6` and `frozen_summary_sha256=acc01268…` on both revisions.
   - Expect `pin_probe_artifact` 0→1 and `metadata_companion_present` false→true.
2. SCORECARD commands D and C with `REV=<after>`: `recorded_cases=6 depth_score=6`; C `asserted=4`.
3. Frozen and unchanged files: `git diff --exit-code 546b371 <after> -- tools/mutate-and-run.sh tools/bash-witness-study.py tools/repeat-control.py SHONEN.md .ufo/evidence/round-12`.
4. `python3 tools/bash-witness-study.py check` should still print `WITNESS_CHECK: CLEAN (declared.tsv sha256=0def0d3b…`.
5. C2:
   - `python3 tools/witness-metadata.py --selftest`.
   - `python3 tools/witness-metadata.py --check --json` should give exit 0 and `metadata_consistent`.
   - `--check --companion <old-null fixture>` should give exit 1, reason `normalized_kind_null`.
   - Retain all three in an in-repo receipt.
6. C1:
   - `python3 tools/pin-disposition.py --selftest`.
   - Then `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin > .ufo/evidence/round-13/pin-dispositions.json` with the UTC time recorded.
   - Then, per row, an independent object-store replay: `git -C <repo> show <recorded head commit>:<path> | sha256sum` against the row's `head.blob_sha256`; `merge-base --is-ancestor <pinned_commit> <head>`; and confirm the manifest pins equal `tools/mutate-and-run.sh:542-553` `PIN_*`/`REV_*`.
7. Sources: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` should give exit 0.
8. Pre-claim sweep before commit: `test -e` on every path cited by `lessons/round-13.md`, `corpus/README.md`, `LOG.md` round-13 and QUALITY 14. In particular, `pin-dispositions.json`, `witness-metadata.json` and the verification receipt must exist.

## Messages sent

- `TameshiR13.PinProbe`: D3 and D4.
- `TameshiR13` (L1): D0, constant-reuse counting, the then-missing lesson, and S047. L1 replied that D0 and S047 are accepted and that the lesson now exists. D2 is a new finding, raised after that reply.

## Owned paths

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-13/w1/AdmissionCritic.md`, this file and the only write.

## Addendum — after L1 replies and companion landing (01:58)

L1 has accepted two corrections:
- **D1:** the probe is now framed as a capability acquisition. Depth is based on the six observed statuses plus the F7 source-backed detail, and scalar 6 is unchanged.
- **D2:** Main is to produce `pin-dispositions.json`, the receipts and the lesson's runtime section before commit.

D2 stays a commit-blocking condition until check 8 passes.

I reviewed `.ufo/evidence/round-13/witness-metadata.json` (read-only):
- **Digests:** the three frozen digests match the committed files.
- **Rerun residual:** a second null (`rerun-20261020T035435Z/summary.json`, `6726421f…`, tracked, re-hashed now) is named as `named-residual-uncorrected`.
  - **Condition:** the C2 wording must cover **one of two** null observations. Do not say "the null-kind defect is repaired" without that scope.
- **Producer hash:** `producer.sha256` is `249d9dcd…`, taken from `summary.json#/tool`. This differs from the current `tools/bash-witness-study.py`, which is `49e9e5e2…`.
  - The companion marks the producer `checked_live: false` and records it as historical identity. That is honest.
  - **Condition:** the report must not present the frozen summary as produced by the current committed tool.
