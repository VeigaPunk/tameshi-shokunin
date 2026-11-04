# round-81 plan — tameshi (frozen before data)

Lane: tameshi-shokunin (depth + calibration; verification-fixture craft).
Round: 81 (attempt 1), 2026-11-04. Base
`56a0129fe9bfd0ce607290a36350e38ac4df9c72` (= `origin/master`, the round-80
closure and its non-author spot-check tip). Round shape: **one v1 wave, 13
seats** — 4 executor · 2 scout · 1 scribe · 2 reviewer · 1 critic ·
1 mutation-tester · 1 sentinel · 1 connector; attack seats 5/13 = 38.5 %;
policy `scripts/hyaku/ufo-wave-policy.json`, band 8–16. The §3 planner seat
stays with the L1 (the validator rejects `planner`); its data walk rides a
scout item. Saturation: scored axes depth 10, calibration 8, freshness 9 all
at or above the line 8; round 80 entered a capability row, so the stagnation
nudge does **not** fire and C1 works calibration, the lowest scored axis.

Motivating evidence: the round-80 non-author spot-check
(`corpus/lessons/round-80-verifier-spotcheck.md` §6) routed **six** defects to
this round — D1 uncommitted evidence (two 7 MB receipts cited but absent from
the tree, one committed as an empty blob), D2 record tokens that are not the
receipt's, D3 two standing-sweep rows pinned at pre-settlement tool bytes,
D4 an S289 `used-by` change claimed but not landed, D5 an S289 re-open with no
committed fetch receipt, D6 no round-80 `## Search log` note. Each is a
record-vs-repo-state mismatch: the lane's own description of itself, checked
against committed bytes. This round binds them.

## R81-C1 — calibration: the routed-defect register is bound to repo state

- **Predicate (the claim's one sentence).** Every defect the round-80 closure
  routed to this round that round 81 owns — D1, D2, D4, D5, D6 (D3 is C2's
  and is deliberately absent from this manifest so the two claims verify
  without each other) — MEASURES `closed` under `tools/defect-bind.py` at the
  tip, with every row's declared expectation met:
  `DEFECT_BIND: rows=6 closed=6 open=0 unexpected=0`, exit 0.
- **Population.** `tools/defect-bind.json`, six rows:
  `D1a-cited-receipts` (tree-paths: the three round-80 paths the round-80
  report/spot-check cite), `D1b-coldread-before-bytes` (tree-bytes ≥ 1 MB: the
  path is committed as a 0-byte blob today), `D2-before-tokens` (receipt-tokens:
  the SCORECARD erratum span must carry `24/24` and `17/17`, and both tokens
  must be byte substrings of `.ufo/evidence/round-80/design/c1-before-sweep.txt`),
  `D4-s289-usedby` (sources-cell: S289's used-by cell names the round-80 and
  round-81 lessons), `D5-s289-fetch-receipt` (tree-paths: the S289 re-open
  fetch receipt + headers), `D6-searchlog-notes` (doc-contains: `## Search log`
  carries the Round 80 and Round 81 notes).
- **Before (measured at the base tip with the declared instrument,
  `.ufo/evidence/round-81/controls/c1-before.txt`):**
  `DEFECT_BIND: rows=6 closed=0 open=6 unexpected=6`, exit 1 — six rows open,
  each naming its missing artifact.
- **Do-nothing control.** Appending nothing cannot reach the after-state: the
  base tip, re-run at the tip commit with the same manifest, reads `open=6`.
  `--selftest` → `DEFECT_BIND_SELFTEST: 11/11 pass`.
- **Kill rule.** With the instrument and the manifest unchanged after this
  declaration, ANY of the six rows measuring `open` (or any row removed,
  `expect` relaxed, or population narrowed) fails the claim. A row measures
  `closed` only from committed bytes at `HEAD`.
- **Counting command**
  `python3 -I -X utf8 tools/defect-bind.py --repo . --manifest tools/defect-bind.json`.
- **Capability row on landing:** `closure-defect bind`.

## R81-C2 — freshness: every standing row pins settled instrument bytes

- **Predicate.** The standing self-state sweep's declared population pins the
  instrument bytes the tip actually carries:
  `SELFSTATE_PINS: rows=23 settled=23 stale=0`, exit 0 at the tip. A row is
  `settled` when the instrument's blob at the row's pinned revision is
  byte-identical to its blob at the pin revision (`--pin-rev`, the tip).
- **Before (measured at the base tip, `.ufo/evidence/round-81/controls/c2-before.txt`):**
  `SELFSTATE_PINS: rows=23 settled=20 stale=3`, exit 1, naming
  `receipt-exists-selftest` (pin `21ef81e9`, tool last changed at `4af6695f`),
  `receipt-bind-selftest` and `registry-bind-selftest` (both pin `ae591d5a`,
  both tools last changed at `01ca77cd`) — the round-80 closure defect D3 plus
  one row the closure did not name.
- **Do-nothing control.** The base manifest under the landed audit: 3 stale.
  Re-pinning is the only move that reaches `stale=0`; re-pinning to a revision
  whose bytes differ still reads stale (`ARM18`).
- **Kill rule.** The population is the whole validated manifest
  (`validate_manifest` refuses zero rows, a null instrument rev, an escaping
  path); a single stale row fails the claim. The standing sweep must stay
  green (`SELFSTATE: rows=23 match=…`, exit 0) after the re-pin — a re-pin that
  changes a figure is a different round.
- **Counting command**
  `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json --pin-audit --pin-rev HEAD`.
- **Sourced:** S289 (`git-cat-file`, re-opened this round — the blob-at-revision
  binding the audit rests on).

## R81-C3 — coverage: the suite's own assertion text is pinned

- **Predicate.** The two round-80 mutation survivors of the **test-text class**
  are killed by the standing batteries, and both suites stay green:
  selfstate `MUTATE: DONE (target=selfstate-arms-r81 defects=5 killed=5
  survived=0 inconclusive=0 kill-rate=100%)` and wave-reconcile
  `MUTATE: DONE (target=wave-reconcile-arms-r81 defects=14 killed=14
  survived=0 inconclusive=0 kill-rate=100%)`, each with `CONTROL: GREEN` and a
  byte-identical `MUTATE_RESTORE: OK`; `SELFSTATE_SELFTEST: 21/21 pass` and
  `WAVE_RECONCILE_SELFTEST: 25/25 pass`.
- **Surface it moves.** The edges class "the suite's own assertion text" — a
  mutant that deletes or weakens an arm's assertion while keeping the arm name
  and its fixtures. `ss-bom-only` (arm15's non-UTF-8 conjuncts deleted) and
  `wr-prefix` (arm24's expected prefix weakened) both survived the round-80
  batteries at 17/17 and 24/24. The new arms digest
  `inspect.getsource(selftest)` and compare it to a pinned constant
  (`ARM21_selftest_text_pin`, `arm25-selftest-text-pin`), so any arm-text edit
  fails an arm until the constant is recomputed deliberately.
- **Before (measured at the BASE tool bytes, `.ufo/evidence/round-81/controls/`):**
  `c3-base-ss.txt` → `MUTATE: DONE (target=c3-base-ss defects=1 killed=0
  survived=1 inconclusive=0 kill-rate=0%)`; `c3-base-wr.txt` → the same for
  wave-reconcile. Both `CONTROL: GREEN`, byte-identical restore.
- **Do-nothing control.** The base tool bytes with the two single-edit mutants:
  both survive.
- **Kill rule.** Each mutant must be KILLED. Frozen FAIL sets measured on the
  candidate bytes: `ss-bom-only` → `ARM21_selftest_text_pin` **only**;
  `wr-prefix` → `arm25-selftest-text-pin` **only**. Disclosed matrix change:
  `arm20-cleanup-removed` (an existing defect that edits arm20's fixture
  cleanup inside the selftest function) now also fails `arm25` alongside its
  own arm20 — still killed, set recorded. **Declared limit:** a two-edit mutant
  that weakens an arm AND recomputes the digest constant is outside the
  single-edit class this pin governs; the pin defends against accidental and
  single-edit weakening, not against a deliberate two-file rewrite (the
  constant and the arm are in one file, so the class boundary is the edit
  count, not the file).
- **Counting commands:** the two battery commands
  `bash tools/mutate-and-run.sh --target tools/selfstate-freshness.py --defects
  tools/selfstate-freshness-mutants.spec --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --label selfstate-arms-r81`
  and the wave-reconcile twin with `tools/wave-reconcile-mutants.spec` /
  `--label wave-reconcile-arms-r81`.
- **Sourced:** S310 (Python `inspect` docs — `inspect.getsource`, the pin's
  ground), opened this round.

## No-harm and registry coupling

`SELFTEST_ARMS` 17 → 21 (selfstate) and 24 → 25 (wave-reconcile) change two
registry figures; `tools/registry.json`'s literal `expect.stdout_contains`
tokens and `SKILL.md`'s registry rows are refreshed in the landing commit and
re-measured by `tools/registry-figure-bind.py` (`rows=7 match=7`, exit 0) —
a figure the round does not refresh is a measured defect, not a silent drift.
No SCORECARD axis score is lowered; depth/freshness figures are restated, not
moved, except the two claims above.

## Round-shape record

One v1 wave `w1`, 13 seats (policy band 8–16; attack 5/13 = 38.5 %; one
connector seat; two scout seats). Every seat is read-only in the lane except
its own report file; executors build in `$HYAKU_SCRATCH/tameshi-r81/<seat>/`
and delete their trees. Residual: none planned; any leftover seats go to one
ordinary ≤4-seat call counted in the round total.
