# tameshi round 72 — lesson

Round 72 (attempt 1), base `f20ba482c7441d4c75818e7cd8a3165fee7821a1`
(`= origin/master`, clean tree). Claims, counters, kill rules and arms are
frozen **before any claim data** in `plans/round-72.plan.md` (declaration
commit `dfb534ca`). Round shape: one v1 wave, 12 seats (3 executor · 2 scribe
· scout · reviewer · critic · mutation-tester · sentinel · revenger ·
connector), policy band 8–16.

## Declared claims (frozen pre-data)

- **R72-C1 — capability acquisition (operability): planning-time rekey-cost
  forecast.** `tools/rekey-cost.py` prices a planned edit set against the
  cold-read ledger's own input pins. Frozen arms: `corpus/SOURCES.md` 13,
  `PROVINCE.md` 6, `corpus/QUALITY.md` 6, `SCORECARD.md` 0,
  `tools/pointer-recheck.json` 0, both 17, empty set exit 2; each
  non-structural arm was re-driven on the guard itself in scratch clones
  before the freeze (`.ufo/evidence/round-72/reh/`).
- **R72-C2 — calibration (lowest scored axis, 8): the two routed defects from
  the round-71 non-author closure paid.** S302's `§4.3` label superseded by
  S303 (`§4.2 Selecting lines by numbers`, page line 2246; the §4.4 quote at
  page lines 2446–2449, not 2445–2448), the PROVINCE round-16 append's
  `:85-91` corrected by an appended block (`:88-94` seven-leg cut, `:88-97`
  ten-leg ledger), three new pointer-recheck rows, census exit 0, and the
  cold-read rekey paid (forecast 17 = the guard's measured loss at the edit
  commit).

## Gate — the corrections (sourced claim)

**S303 admitted (supersedes S302).** Source opened this round: GNU sed manual
(GNU sed 4.9), <https://www.gnu.org/software/sed/manual/sed.html>, fetched
2026-11-03 (HTTP date `Wed, 04 Nov 2026 00:21:37 GMT`; `Content-Length`
415310; sha256 `511edd60a6f5034d4f28ca1dbe0772bbfd4c9865aaf6c0f85e2f05d4294b6bac`;
extract `.ufo/evidence/round-72/sources/sed.html`). The fetched bytes are
byte-identical to the r71 snapshot `511edd60…`, so this round's corrections
are record corrections, not source drift.

- Located quote 1 (≤25 words, page line 2246 heading + 2255 sentence):
  "Specifying a line number will match only that line in the input." — 12
  words, §4.2 **Selecting lines by numbers** (the heading is at page line
  2246; S302 labelled it §4.3).
- Located quote 2 (§4.4 Range Addresses, first paragraph, page lines
  2446–2449): "An address range matches lines starting from where the first
  address matches, and continues until the second address matches
  (inclusively)" — 20 words; the row had pinned 2445–2448, off by one.
- Admitted under CORPUS.md rule 2 as a same-URL supersession (`teaches` opens
  `supersedes S302 —`), which the census exempts from E04; the row joins the
  registry as S303 with `used-by corpus/lessons/round-72.md`.
- **Rejected (standing, re-sampled this round): S293's standing rejection**
  (git-cat-file batch framing) — S289 already holds the same URL at tier A
  for the object-inspection ground; a second row would duplicate scope. The
  rejection keeps reason + flip; re-read at the tip, verdict unchanged.

## Gate — the PROVINCE correction

Measured, not recalled (`grep -n` over `tools/mutate-and-run.sh` at the base):
line 84 is the `--regression` header; 85–87 the narrative; legs 1–10 at
88–97 (leg 7 `js-round-gate` at 94, leg 10 `bash-drift-pins` at 97). The
round-16 append's `:85-91` therefore carries the narrative plus legs 1–4.
The correction is an **append** (PROVINCE.md is append-only; line 57 stands),
introducing the two measured spans as tokens the pointer rows resolve.

## What was measured (live, at the commits named)

**R72-C1 — verifies.** Before: `git ls-tree -r f20ba48 tools/ | grep -c
rekey-cost` → `0`; no `REKEY_COST` line existed in the tree. After (receipts
`.ufo/evidence/round-72/`): `python3 -I tools/rekey-cost.py --selftest` →
`REKEY_COST_SELFTEST: 8/8 pass` exit 0 (`cost-live-selftest-r72.txt`);
the seven arms → `at_risk=13` (SOURCES), `6` (PROVINCE), `6` (QUALITY), `0`
(SCORECARD), `0` (pointer-recheck), `17` (both), exit 2 (no planned path)
(`cost-live-arm-*.txt`). The model is measured, not asserted: each of the
four non-structural arms was re-driven on the guard itself in scratch clones
at base before the freeze — `lost=13`, `lost=6`, `lost=6`, `lost=0`
(`reh/reh-*.out`) — and the live check matched: the forecast 17 for the
round's edit set equals the guard's `COLDREAD_PRECHECK … lost=17 RED` at the
edit commit `d618518a` (`live-red-r72.out`, `cost-prediction-at-edit.json`).
The capability row entered `SCORECARD.md` `## Capabilities` in the C1 commit
`b3392010`.

**R72-C2 — verifies.** After: `corpus/SOURCES.md:178` carries `| S303 |` with
the §4.2 label and the page lines 2446–2449 (measured on the live page, sha256
`511edd60…`, byte-identical to the r71 snapshot); the PROVINCE append carries
`:88-94` and `:88-97` and the measured leg mapping; the pointer sweep reads
`POINTER_RECHECK: rows=11 met=11 unexpected=0` exit 0 with the three new rows
`hit ok` (`pointer-standings-r72.txt`) and the control manifest
`rows=2 met=2` with both rows `miss ok` (`pointer-control-r72.txt`); the
census on the edited file exits 0 (`census-start-r72.txt` is the round-start
run; the round-end run is the tip receipt). The RED the corrections cost was
measured and paid: `lost=17 RED` at `d618518a` → `REBIND OK sections=17
entries_added=17 ledger_before=797` (`rekey-summary-r72.json`; the machinery
diff `make-rebind-r72.diff` is constants-only: round, batch, trace path,
reader string, carried_from, host word) → `lost=0 ok` at both floors
(`live-green-r72.out`: `4ed9ce1c` 64 → 64; `live-green-hist-r72.out`:
`8b0042bd` 46 → 64) and `credited=64/64` in rev mode (`live-revmode-r72.out`).

**Shared no-harm.** Monitored bytes base → worktree all identical
(`monitored-bytes-r72.txt`): SKILL.md, corpus/QUALITY.md, corpus/README.md,
tools/registry.json, SHONEN.md, tools/mutate-and-run.sh and the guarded probe
tools/coldread-precheck-portable.py. Additivity: SOURCES 0 old lines missing,
1 added (`additivity-sources-r72.txt`); the ledger's 797 old entries are
structurally identical and the 17 new entries carry `r72-batch-1`
(`additivity-ledger-r72.txt`). Standing instruments re-read at the round's
bytes: figure-attribution `rows=3 met=3`, count-recheck `rows=7 met=7`,
anchor-drift `rows=16 met=16`, arm-liveness `rows=9 live=9 dead=0`, pointer
selftest 7/7.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| survivor | the first selftest draft's `arm()` helper treated a raised `SetupError` as a failure even where `setup` was the expectation, so arms 6–7 could never pass: `REKEY_COST_SELFTEST: 6/8 pass` (`mistake1-fix-before.txt`, exit 1). | none — the tool's own selftest was the only thing looking; no lane criterion covered test-harness expectation wiring. | the helper now maps `SetupError` to the expected `setup` value and the run reads `8/8` (`cost-live-selftest-r72.txt`); the red-before output is committed, so the fix is shown able to fail. |
| landing | a first receipt-saving batch put `python3 … coldread-precheck-portable.py … && echo` in one chain; the guard exits 1 on RED, so the chain stopped and the receipt files were never written — caught by the empty first-line check right after. | none — no rule said "a receipt-writing command must not sit on an `&&` chain whose exit can be non-zero". | receipt-producing runs now use `;` and every saved receipt is checked for its first line before it is cited. |
| stale-premise | the round's first plan draft wrote "forecast 13" for the edit set — 13 is SOURCES alone; adding the PROVINCE edit makes the union 17 (not 19: two sections are in both). | the pre-freeze rehearsal (`reh/reh-province-sources.out` → `lost=17`) caught it before any counter was frozen. | the plan now states 17 and the arm table carries both the per-edit and the union value; the tool's selftest arm 8 pins "union, not sum". |

## Gate — wave attacks (recorded at WAVE-DONE)

Pending: the 12-seat wave's results are integrated at the round's closeout
section below.
