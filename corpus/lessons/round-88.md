# Round 88 — fresh start: the eleventh ledger leg, the first Python gate

Lane author TameshiR88 (attempt 1), 2026-11-06. Base `f256302b394ae3253df014fe1131e2c20e2c16b6`
(round-87 tip). Pre-freeze `6998726f` (counter, pre-registered spec, nine controls, S312
snapshot); freeze `1763efe7` (`plans/round-88.plan.md`); candidate `28ec5885` (leg 11 wired).
One validated v1 wave `r88-w1`, 10 seats. `LOG.md` round 88 is the landing record.

## Fresh-start reads

Rejected closures read before declaring (MANIFEST `rounds[]` indices 1248, 1299, 1320 and
their spot-checks `round-85/86/87-verifier-spotcheck.md`): r85 basename oracle 8/8; r86
label/worktree oracles 8/8 and a cited-tree relabel 30/30; r87 fixture-worktree and
committed-diff oracles 8/8 and prose absorption. The common root is a lane-built counter
certified against a lane-built fixture that a cheaper oracle also satisfies. This round
measures a sibling's committed gate under its own selftest and counts only what an
independent replay reproduces (plan § Fresh-start reads).

## Gate

Candidates considered:

1. **R88-C1 — kake `scripts/ledger_append_guard.py` as ledger leg 11 (coverage).** Admitted as
   the round's one frozen claim. A sibling-authored Python gate with a hermetic `--selftest`
   (two checks, 0.07 s), on kake's `origin/master` at `e8d3a924`, not yet in the ledger and
   not, per the scout, mutation-tested by any lane.
2. **Another calibration census round (successor to R87-C2).** Rejected: three rounds of
   lane-built census and certification counters were each killed by a counterfeit the
   freeze did not model; a fresh start needs a measurement whose value a lane-written
   oracle cannot produce. Flip condition: a calibration counter whose population is read
   from SCORECARD/SHONEN and whose observed side is produced by executing sibling or
   historical bytes, not lane fixtures.
3. **PROVINCE "six recorded legs" wording as a calibration claim.** Rejected as bookkeeping:
   the round-16/18/21/25/26 appends already name the later gates; the round-88 append adds
   the eleventh in the same way.
4. **kagi gates (e.g. `corpus/rendered-text-v1.py`) as the Python leg.** Rejected: kagi is
   under its own pause and refusal boundary this run; a read-only leg on its bytes is legal
   but adds a contested surface for no gain over kake.

Sources opened this round (the row is written only after the source was opened):

- **S312 (new)** — Python 3.15 Built-in Types, `https://docs.python.org/3/library/stdtypes.html`
  (301 → `/3/builtins/stdtypes.html`). Access date 2026-11-06 (HTTP date
  `Fri, 06 Nov 2026 18:46:19 GMT`, 815447 B, sha256
  `cee1bf3bd366d04b5ecc60b0b35c8d4d474bd10895a7908c84543b4ae14dc327`, snapshot
  `.ufo/evidence/round-88/sources/s312-stdtypes.html`, headers `s312.headers`). Located
  quotes: line 4175 (§`bytes.startswith`, 15 words) "Return True if the binary data starts
  with the specified prefix, otherwise return False."; lines 4147-4148 (§`bytes.rindex`,
  13 words) "Like rfind() but raises ValueError when the subsequence sub is not found."
  Grounds the case note's reading of K_CUT_WHOLE and K_STARTSWITH (the guard's verdict is
  one whole-head prefix test) and of the guard's `b"]" in base` pre-check. Admitted
  (tier A, status `mined`, recheck 365d).

Admitted: S312 as the new row and the case note `corpus/knowledge/mutation-case-kake-ledger-guard.md`
citing it. Rejected: candidates 2–4 above (reasons and flip conditions inline).

Spot-check: pending the non-author closure. The round's own wave seats are the lane
(LEARNING.md), so they do not count as the outside check.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | pre-registration leak: forgery controls that EXECUTE the candidate's mutants (`doctored`, `forged`, `unprereg`) ran before the pre-registered spec was committed, so git cannot order the predictions before the first mutant run; only file timestamps can (spec 15:44:41, first mutant 15:53) | `.ufo/evidence/round-88/pre-freeze/timeline.txt`; `plans/round-88.plan.md` § Disclosure | none: QUALITY criterion 111 asks for the cheat family before the freeze, not for the spec's commit before any candidate execution | `.ufo/evidence/round-88/mistakes/prereg-order.sh` — the spec's first-add commit must be a STRICT ancestor of the first receipt carrying a mutant verdict. Shown able to fail: round 88 `same-commit` exit 1, round 51 `ok` exit 0 (`mistakes/M1-prereg-order.txt`). New QUALITY criterion 134 |
| M2 | wave spec named a role the validator refuses (`labrat` is not a swarm role) | `.ufo/waves/round-88/w1-validate.err` (first run: `unknown_role … "labrat"`) | the validator (`ufo-swarm-wave.mjs`, `unknown_role`) — caught before dispatch | the probe item rides an executor seat; the round's attack share is counted on reviewer/critic/mutation-tester only (3/10) |
| M3 | inherited (round-87 R-2): counterfeit sources `cf-a`, `cf-b`, `cf-e` (T87E1) and `cf-oid` (T87C1) were left in scratch; the reaper removed them, so their 8/8 and 7/8 values stay narrative-only | `.ufo/waves/round-87/w1/T87E1.md:11-15` (sha256s only), `T87C1.md:9` ("Source: `cf-oid.py` (scratch)") | none | not recoverable; the round-88 wave context requires every seat to save each counterfeit's source next to its deliverable, and the round-88 controls are a committed generator (`controls/make-runner.py`) plus variant names, re-runnable from committed bytes |

Round-87 routed defects: **R-1** (accuracy) — the round-87 v1 before-state command used the
v1-schema manifest `.ufo/evidence/round-87/overreach/r86-cited-tree-manifest.json`, not the
`…-v2schema.json` the round-87 report names; corrected here (append-only; the round-87
report is not edited). **R-2** — M3 above. **R-3** — M6/M8/M9 successors are not taken
this round (no census or certification claim); they stay routed. **R-4** — open debt carried:
16 unbacked LOG counter quotes and 2 in `corpus/lessons/round-86.md`, retained instruments
unregistered; this round adds no unregistered instrument to `tools/` (the counter lives under
`.ufo/evidence/round-88/`).

## Source curation delta

- New row `S312` (above). Registry rows `171` → `172`. Tier A +1. Next unused id `S313`.
- No existing row's `status`, `recheck` or `used-by` changed.
- Census: before `sources-census.sh validate --root … tameshi` exit 0
  (`.ufo/evidence/round-88/census-before.txt`); after recorded in the report.
