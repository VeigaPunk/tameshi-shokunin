# ReNoHarmPlan — re-attack of round-23 wave-2 NoHarmPlan (Tameshi round25, w1)

Seat: scout, calibration axis, read-only against the lane. The only writes are this report;
no production file, lane Git index or jj state touched (lane git reads used
`GIT_OPTIONAL_LOCKS=0`). The strict selector was run as a probe, and only inside a private
clone under `/tmp` (out-of-slice, disclosed below). No tool was installed or upgraded.

## Verdict

**AGREE — both clauses of the attacked claim hold against the frozen round-23 artifacts and
still hold at lane revision c9ff09fb41fb8aac5fc335faf10858ff606bd5df. No counterexample
found.** The seat died before reporting, so this is the first run of this falsifier.

## What was attacked

Original item text, verbatim:
> Fresh attack under /home/vgpnk/Projects/shokunin/tameshi-shokunin: current strict selector
> default-ledger reanchor plan: historical prefix data retained, current no-harm not borrowed.
> Explicit executor commands alone may execute; all others static read-only and skip
> tests/build/format. No repo writes; final findings only.

The "current strict selector default-ledger reanchor plan" is the round-23 w1 `CurrentMonitor`
seat's persisted "Required re-anchor policy" (steps 1–6) in
`.ufo/waves/round-23/w1/CurrentMonitor.json`, plus its execution artifacts:

- `.ufo/evidence/round-23/source-refresh-plan.json:2-4` (`not_yet_executed: true`,
  `prefix_count: 249`, `read_revision: 8f66b5d9…`).
- `.ufo/evidence/round-23/reanchor-final.py` (`LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'`
  at :24; monitor receipt must be strict/no-overrides/at-rev at :59; prior entry located at :79;
  refuses to overwrite an existing trace at :86; new entry built as `dict(base)` + re-anchor fields
  at :103-104; provenance label at :32).
- Receipts: `.ufo/evidence/round-23/source-refresh{,-final}-receipts.json`,
  `source-refresh-final-entries.json`, `source-prefix-preservation{,-final}.json`.

Clause A = historical prefix data retained; Clause B = current no-harm not borrowed.

## A. Historical prefix data retained — holds

Two append steps in round 23; each receipt verified independently from git data:

1. Step 1 (15 appends, commit 336565f): `.ufo/evidence/round-23/source-prefix-preservation.json:2-7`
   claims prior 249 / +15 / current 264, `prefix_equal: true`,
   `prefix_sha256: 42e5c7019d8447cff08f52230ca0d32f476514e0bdb4f5585c35f8756554796c`.
   Independent: `sha256(json.dumps(entries, separators=(',',':'), sort_keys=True))` over the
   249-entry ledger at 8f66b5d = `42e5c701…` (exact match); the same digest over the first 249
   entries of the ledger at c9ff09f and at worktree HEAD also = `42e5c701…`; the first differing
   byte between the 8f66b5d and 336565f ledger files is 1,456,914 = the entries-array append point
   (append-only, nothing before it rewritten).
2. Step 2 (3 appends, commit 549ede2): `.ufo/evidence/round-23/source-prefix-preservation-final.json:2-9`
   claims prior 264 / appended 3 / current 267, `prefix_bytes_unchanged: true`,
   `prefix_byte_length: 1506106`, `prefix_entries_equal_as_data: true`,
   `prefix_entries_sha256: 038fe0601a94a4a152c0892a9c09739e3f3651176b9634e38d2665cd82b63d17`,
   `other_top_level_keys_unchanged: true`. Independent: the first 1,506,106 bytes of the 336565f
   and 549ede2 ledger files are byte-identical and the first differing byte is exactly 1,506,106;
   `sha256(json.dumps(entries[:264], sort_keys=True))` = `038fe060…` (exact match);
   `schema`/`carried_from`/`provenance`/`round21_provenance` are value-for-value equal between the
   two files.
3. Persistence to the contract revision: at c9ff09f and HEAD the ledger has 287 entries and
   `entries[:249]` ≡ the 8f66b5d ledger, `entries[:264]` ≡ the 336565f ledger,
   `entries[:267]` ≡ the 549ede2 ledger (exact data equality). `git diff` for the ledger is empty
   over `1f73157..c9ff09f` and `c9ff09f..HEAD`. The plan's "must stay stale" entry (index 98,
   section 1380) is untouched.

## B. Current no-harm not borrowed — holds

1. The harm was actually measured and retained, not skipped: 48/62 @496d212
   (`monitor-intermediate-A.json`), 47/62 @8f66b5d (`monitor-intermediate-B.json`), 59/62
   @332dc890 (`monitor-intermediate-D.json`); the lesson says so in its own words — "no
   historical62/62 can substitute" (`corpus/lessons/round-23.md:97-100`).
2. The restore was measured at its own revisions: 62/62 @336565f (`monitor-current-C.json`) and
   62/62 @549ede2 (`.ufo/evidence/round-23/final-verification.json`,
   `observations.monitor-final`: argv `--rev 549ede24aa9b2a6746d3973cf55dc4ceb07a5413 --explain`,
   exit 0, `trace_gate: strict`, `overrides_used: false`, `ledger_source: rev`,
   `sections_covered: 62/62`, restraint 8, depth 8, `reasons {"credited": 62}`). SCORECARD ties
   the claim to that revision, not to the earlier C (`SCORECARD.md:1067-1077, 1105-1115`).
3. Independent re-runs (my own probes, private clone `/tmp/renoharm-lane`, worktree instrument
   `sha256(.ufo/evidence/round-21/coldread/measure.py) = 657f009b…`, identical to the receipts'
   instrument; `round-18/measure.py = 7ca87a7c…`; `tools/trace-inputs.py = f59c9312…`):

   ```
   cd /tmp/renoharm-lane
   python3 .ufo/evidence/round-21/coldread/measure.py --repo /tmp/renoharm-lane --rev <REV> --explain
   ```

   Observed, exit 0 for every revision, all `62/62`, restraint 8, depth 8,
   `trace_gate: strict`, `overrides_used: false`, `missing: []`, `reasons {"credited": 62}`:

   | REV | role |
   |---|---|
   | 6a1821a (round-23 delivered tip) | 62/62 |
   | 549ede2 (round-23 measured revision) | 62/62 (matches `monitor-final`) |
   | 336565f (round-23 restore C) | 62/62 (matches `monitor-current-C`) |
   | c9ff09f (round-25 contract revision) | 62/62 |
   | 1f73157 (round-25 base) | 62/62 |

   So the round-23 tip itself (whose only later change, 6a1821a, added evidence/LOG/SCORECARD and
   no credited input) measures 62/62 — the final no-harm is not borrowed from 549ede2 either.
4. The credit-restoring appends are actual instrument runs, not hand-authored:
   `source-refresh-final-receipts.json` (`read_revision 332dc890…`) holds 3 observations, exit 0,
   rev-bound, `instrument_sha256 = f59c9312c56eb458…` = `sha256(tools/trace-inputs.py @332dc890)`;
   the traces `.ufo/evidence/round-23/source-traces-final/source-{6,1938,1964}.json` carry
   `rev 332dc890`, `live_lane_reads {}`, `external {}`, and inputs equal to the ledger entries'
   `inputs` plus `SKILL.md`; `source-refresh-final-entries.json` equals ledger entries 264–266
   field-for-field; for all three sections the ledger `sha256`/`heading` equal `SKILL.md` at the
   measured revision 549ede2; provenance is labelled "actual L1-author byte-consuming source
   reads; not recipe execution, independent/blind cold-read or required-command coverage"
   (`reanchor-final.py:32`). The prior same-section entry's 20 planned paths are unchanged by the
   re-anchor (only digests and `read_rev` moved).
5. Selector identity/override refusal (so "default-ledger" cannot be silently redirected):
   `measure.py` sha `657f009b…` is unchanged since round-21 (`git log`), and the round-23 replay
   bundle shows `round21-coldread-selector-selftest` at 496d212 → `SELECTOR_SELFTEST: 12/12 pass`
   including all `override-refused:*` cases. SHONEN box 3 still links
   `.ufo/evidence/round-21/coldread/ledger.json`; no `.ufo/evidence/round-23/coldread/` exists
   (plan step 6 honored).

## C. Does it still apply at c9ff09f?

Yes. At c9ff09f (and HEAD): the ledger prefix is retained as shown in A.3; the claim's anchor row
`round21-coldread-selector-selftest` is `active` (not superseded), as is `trace-inputs-selftest`.
The seven superseded rows are other rounds' instruments and the round-23 command-binding rows
(`command-binding-selftest`/`-frozen-clean`/`-source-read-red` → their r24 `-pinned` successors);
none of them anchors this claim. `tools/command-binding.py` did change after round 23 (round-24
commits), but it is not part of this claim; the claim's instruments (round-21 selector, round-18
algorithm, `tools/trace-inputs.py`) are byte-unchanged. Round-25's frozen contract asserts no
no-harm of its own (`non_claims`: "numeric depth and calibration stay 8"), so there is nothing
borrowed, and the current state itself measures 62/62 strict at c9ff09f (my run).

## Nits (documentation-grade, no counterexample)

- N1: the two round-23 prefix receipts use different digest canonicalizations — compact separators
  for `42e5c701…` (prior 249) and default separators for `038fe060…` (prior 264) — and the final
  receipt states no canonicalization. Each digest reproduces exactly under its own method, so the
  retention claim is unaffected; this is the same family as the round-24 M1 nit.
- N2: `reanchor-final.py` inherits `verdict`/`blocking_gaps`/`wrong_expectations`/
  `commands_executed_count` from the prior entry instead of asserting the plan's field list; the
  three final entries carry `gap-minor / 0 / 0 / 1`, consistent with the plan, and none is
  veto-eligible (monitor `vetoed: false`).

## Disclosure / bounds

Out-of-slice: five strict-selector probe runs (`--explain`, read-only) in a private clone
(`git clone --no-hardlinks` → `/tmp/renoharm-lane`, HEAD 09dc114 = branch tip; all needed revs
present), plus read-only `git show`/`git log`/`git diff` with `GIT_OPTIONAL_LOCKS=0` against the
lane. No gate, selftest, sweep, mutation or formatter was run; nothing was written in the lane
except this report; no tool installs. Note: at the time of writing, `git status` showed
concurrent sibling modifications (`corpus/SOURCES.md`, `tools/mte-interop.py`) that this seat did
not make; every check above is revision-based (`git show`/`--rev`), so none of it is affected by
worktree churn.

R23-REATTACK NoHarmPlan: AGREE
