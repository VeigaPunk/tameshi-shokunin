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

## Erratum, appended after the wave's attacks (2026-11-03)

**The ledger merge rewrote every line ending.** The r67 rebind driver splices the
entries array through `Path.read_text()` / `write_text()`, and on this host that
normalized the ledger's CRLF to LF: the first rekey commit `bc7dc2fb` reads
293,268 insertions / 281,925 deletions against the base — a whole-file EOL
rewrite, not the append the additivity rule requires. Caught by **seat
T72W1S03**, which re-ran the lane's own `tools/additivity-receipt.py
--require-raw` over the landed commit and read exit 1 with
`eol_rewrite_disclosed=true`, while the monitor stayed green (the guard parses
the JSON, so credit never saw it). Repaired in `b611e763`: the merge rebuilt on
the base bytes with CRLF, the old entries byte-identical, `raw_old_only=0
raw_new_only=38` (`additivity-ledger-r72-raw.txt`, exit 0), and the guard re-read
at the repair commit reads `lost=0 ok` at both floors and `credited=64/64` in rev
mode. C2's measured chain is therefore `d618518a` (edits, `lost=17 RED`) →
`bc7dc2fb` (merge, EOL defect) → `b611e763` (repair, byte-additive).

The lesson: a JSON evidence file's line endings are part of its record, and no
instrument that parses the file can see them. The additivity receipt is the only
one that can, and it was not in this round's own run list until a seat added it.

## Mistakes — appended

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| landing | the first rekey merge `bc7dc2fb` rewrote the ledger CRLF→LF: 293,268 insertions / 281,925 deletions against the base; `tools/additivity-receipt.py --require-raw` over that commit exits 1 with `eol_rewrite_disclosed=true`. | none in the lane's round-run list — the guard is blind to EOLs (it parses JSON) and the additivity receipt was not part of this round's receipts until seat T72W1S03 ran it. | the merge was rebuilt on the base bytes with CRLF (`b611e763`): `raw_old_only=0 raw_new_only=38`, exit 0 (`additivity-ledger-r72-raw.txt`), guard re-read `lost=0 ok` at both floors + `credited=64/64`; the additivity receipt is now a named step of the rekey run-book. |
| survivor | the frozen arm battery does not cover the `IGNORED` filter: mutant M3 (drop the filter) survives every arm and is killed only by the selftest (seat T72W1S09). | none — the arm table was designed from the guard counterfactuals, which never include `SKILL.md` or a ledger path. | recorded as a coverage finding: the arm table gains an ignored-path arm (forecast 0 with a `SKILL.md` edit) in the next round that re-prices the instrument; the selftest keeps the only kill until then. |

## Third correction and batch-2 rekey, appended (2026-11-03)

Seat T72W1S05, re-measuring the PROVINCE append, found a third stale cell in the
same paragraph: `PROVINCE.md:56` carries `tools/mutate-and-run.sh:84-89` as "the
round-1 six-leg anchor", while the six-leg cut is `:88-93` (leg 6
`js-claims-check` at line 93; line 84 is the header, 85-87 the narrative).
Accepted as work, not carried: a second correction block was appended
(`b7b98375`), the drift it re-owed was measured (`lost=6 RED`,
`live-red2-r72.out`), and the 6 PROVINCE-pinning sections were rekeyed as
`r72-batch-2` (`REBIND OK sections=6 entries_added=6 ledger_before=814`; ledger
814 → 820, CRLF preserved by rebuilding on the pre-merge bytes — the batch-1 EOL
defect was not repeated; `additivity-ledger-r72-raw.txt` over the final pín reads
`raw_old_only=0 raw_new_only=53`, exit 0). The monitor at `d7eb02c2` reads
`lost=0 ok` at both floors (`4ed9ce1c` 64 → 64; `8b0042bd` 46 → 64) and
`credited=64/64` in rev mode. A fourth pointer row,
`province-r72-sixleg-cut-88-93`, pins the corrected span: the sweep now reads
`POINTER_RECHECK: rows=12 met=12 unexpected=0` (the frozen plan said 11; the
extra row is disclosed here, not retro-fitted into the frozen text).

## Plan defect, disclosed (not repaired after data)

The frozen C2 control sentence — "the control manifest (same three rows,
record/target revs = base) reads three `miss ok` under `rows=3 met=3`" — is
**unattainable as written**: the pointer instrument refuses a record revision
whose pointer token is absent (`ERROR reason=pointer-absent-in-record`), so a
row whose record does not exist at base cannot be scored there at all (seat
T72W1S05 measured `POINTER_RECHECK error=setup … corrections.md … not in
'f20ba48'`, exit 2). The control was re-shaped **after the freeze** to the
two-row stale-span manifest landed at `.ufo/evidence/round-72/control-manifest.json`
(`rows=2 met=2`, both `miss ok`) plus the seat's own `rows=3 met=2
unexpected=1` run (record at the edit commit, target at base: the S303 row
reads MISSING against the base line), which is the discriminating base
measurement. C2's *claim* is unaffected — the three (now four) tip rows read
hit, the census exits 0 and the monitor is green — but the frozen control
sentence was wrong and is reported as wrong rather than silently replaced.

## Citation erratum, appended (seat T72W1S05's reading)

The "What was measured" section attributes the floor pair `4ed9ce1c` 64 → 64 to
`live-green-r72.out`. That receipt's floor is the **round's base
`f20ba482c744`** (also 64 → 64); the r71 round floor `4ed9ce1c` was measured
separately at the round tip and reads `floor=4ed9ce1c52e2 floor_credited=64
cand=d8e7f33724b4 cand_credited=64 lost=0 ok` (`live-green-floor4ed9-r72.txt`,
exit 0). Both pairs are 64 → 64; the wrong id was named in the first sentence,
and the historical floor `8b0042bd` reading 46 → 64 is unchanged
(`live-green-hist-r72.out`). Caught by the seat reading the receipt bytes rather
than the claim — the class this lane's instruments exist for, one more time.

## Wave — seat verdicts and what they changed (appended at the close)

One v1 wave, 12 seats (3 executor · 2 scribe · scout · reviewer · critic ·
mutation-tester · sentinel · revenger · connector), dispatched as
`.ufo/waves/round-72/w1-dispatch.json` and taken at 21:21:33. Attack seats by
the policy's named set = 3/12 (25 %, the floor) plus a revenger probe.

| seat | role | verdict | what changed |
|---|---|---|---|
| T72W1S01 | executor | support | independent oracle (own heading parser) agrees with the tool on all six arms: 13/6/6/0/0/17 |
| T72W1S02 | executor | artifacts landed | `ledger-census.json` + `ledger-census.md`: entries, per-heading counts, membership histogram |
| T72W1S03 | executor | **falsify → fixed** | the rekey merge rewrote the ledger CRLF→LF (293,268 insertions / 281,925 deletions); repaired at `b611e763`, raw additivity now 0/38 → 0/53 |
| T72W1S04 | scribe | support | live sed fetch (sha256 `511edd60…`, byte-identical to the r71 snapshot), §4.2 heading 2246 / sentence 2255, §4.4 quote 2446–2449 |
| T72W1S05 | scribe | **falsify → fixed** | third stale span (`PROVINCE.md:56` `:84-89` → `:88-93`); the frozen control line is unattainable (F1); the lesson's floor id was wrong (F5) |
| T72W1S06 | scout | support | 96 record files, 2,310 pointer tokens: 995 resolvable, **30 out-of-range**, 302 target-missing (270 bare sibling basenames), 53 ambiguous |
| T72W1S07 | reviewer | support | constant-13, constant-0 and sum-not-union cheats each fail a frozen arm; the 17-heading set re-derived independently |
| T72W1S08 | critic | support | §4.2 is the correct label (§4.3 is "selecting lines by text matching"); the census E04 exemption is real (dropping the `supersedes` prefix prints E04) |
| T72W1S09 | mutation-tester | support + gap | four mutants killed; the `IGNORED`-filter mutant survives every arm (selftest-only kill) |
| T72W1S10 | sentinel | support | no credentials/tokens, no misroot at the fleet root, TMPDIR honoured, no escaping symlinks |
| T72W1S11 | revenger | support | the credit rule keys on recorded input pins: one mutated pin uncredits exactly that section (`input-drift:…`) |
| T72W1S12 | connector | support | no sibling lane holds cold-read cost accounting or pointer/anchor-drift instrumenting; `shokuknow/merge/tameshi/` not readable |

Seat findings adopted as work, not argued away: the EOL repair (S03), the third
correction + batch-2 rekey (S05), the floor-id erratum (S05), and the
coverage-gap carry (S09). Seat findings disclosed and left standing: the frozen
control line (F1/F2) and the plan's loose "header" wording (F4 — the header line
is 84, 85-87 are its narrative; the landed correction states this precisely).
