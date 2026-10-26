# T48W2RevC1Freeze — C1 freeze integrity (round 48, attempt 2, wave a2w1)

Seat: reviewer, calibration / C1 freeze integrity. Read-only on the lane except this report.
All commands run read-only (`git log/show/ls-tree/diff`, `stat`, `sha256sum`, `find`); no counter
invocation (byte-level freeze check only). No tools installed (none needed). Scratch
`/fast/scratch/hyaku/tameshi-r48/T48W2RevC1Freeze` used for patch reconstruction, deleted at the
end of the seat. Repo state observed at HEAD `17cc5ce141868454d05bf75ef5cd230e35f0cdf4`
(2026-10-26 10:28:00 -0300, "a2w1 wave spec and validated v2 dispatch (64 seats) at content
c7586b9a"); the deciding run had not landed (`after/` absent, no commit touches
`.ufo/evidence/round-48/after/`).

Commit timeline (all `%ci` committer dates):

| commit | time (-0300) | subject |
|---|---|---|
| `e73389c0b474` | 05:34:35 | round-48: pre-registration contract … and census start |
| `f1cfaad36013` | 05:39:33 | round-48: pre-data amendments 1-3, wave-1 spec, briefs and dispatch |
| `755298415f8c` | 07:18:36 | round-48: counter freeze (step 2) — both counters, selftest receipts, controls, deciding script, no-harm at base, wave-1 evidence so far |
| `15b1521ea2e9` | 09:05:36 | round-48: hyaku run-8 orchestrator salvage of unlanded attempt-1 … (not a landed round) |
| `c7586b9a10ef` | 10:27:19 | round-48: content revision (attempt 2) — the records |
| `17cc5ce14186` | 10:28:00 | round-48: a2w1 wave spec and validated v2 dispatch (64 seats) |

`git -C tameshi-shokunin log --format='%H %ci %s' -- .ufo/evidence/round-48/contract.json` →
exactly `755298415f8c`, `f1cfaad36013`, `e73389c0b474`. `freeze-2.json.prereg_commits` =
`[e73389c0b474…, f1cfaad36013…]` — exactly the two commits that touched the contract before the
freeze. ✔

## Check 1 — pre-registration precedes every wave-1 seat report — PASS

- Commit order: `git log -- .ufo/waves/round-48/w1/` → only `15b1521ea2e9` (09:05:36, salvage) and
  `755298415f8c` (07:18:36). No wave-1 file was committed in or before `f1cfaad36013`.
- Mtimes: 26 w1 `.md` reports, earliest `T48ExecFetchS048.md` 05:41:58.716 — after both prereg
  commits (05:34:35, 05:39:33). Latest `T48ExecObs2.md` 07:20:39 (post-freeze; it is in
  `freeze-2.json.pending_w1_seats_at_freeze`, consistent with the freeze note).
- Observation (not a failure): `w1/swarm-registry.json` mtime 05:39:27.490 predates
  `f1cfaad36013`'s commit time by ~5.5 s; it is the dispatch registry written by the dispatcher,
  and `f1cfaad36013` is itself the dispatch commit ("briefs and dispatch"). It is not a seat
  report. No seat `.md` report predates either prereg commit.

## Check 2 — counter at CONTENT vs w1 deliverable — PASS (not byte-identical; every difference is the declared, committed patch)

- `sha256sum` of git blobs: w1 `T48ExecC1Counter.measure.py` =
  `dca1cb39de9bca86e5f2de0c399c93b98aa5c051ec8a4cd25b328e45390826b2` = `freeze-2.json.counters.
  calibration/measure.py.from_sha256`; frozen `calibration/measure.py` =
  `572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3` = `…​.sha256`. Not
  byte-identical — exactly as `freeze-2.json.changes` declares.
- Reconstruction (scratch): applied `.ufo/evidence/round-48/calibration/freeze-diff-vs-w1.patch`
  (268 lines, 12 hunks, header `--- w1/T48ExecC1Counter.measure.py / +++ calibration/measure.py`)
  to the w1 blob → `cmp` byte-identical to the frozen counter. **Command:** extract both blobs +
  patch from `git show`, `git apply -p0` in a scratch tree, `cmp` → "PATCH RECONSTRUCTION OK:
  applying freeze-diff-vs-w1.patch to the w1 counter yields the frozen counter byte-exact".
- Patch content matches the declared change list: `load_attestations`/`attest_token` deleted
  (amendment 4), `+BASE = '473336d9…'` pin (amendment 7), FLEET/`fleet_drift`/`sibling_moves`
  (amendment 5), `EXTRA`/`attested_extra` (amendment 4), selftest-case hunks at old lines
  696/734/827/911/940 (T30/T32/T33/T51 + T33a-f). First hunk starts at old line 79 — the
  docstring/predicate block (lines 1-78) is untouched by the L1 edits, so the w1 draft already
  carried the frozen predicate sentence. No undeclared region is touched.

## Check 3 — sha256 equals file at CONTENT and at the freeze commit; immutable after — PASS

- `git show <rev>:…/calibration/measure.py | sha256sum` at `755298415f8c`, `c7586b9a`, `17cc5ce1`
  → `572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3` at all three; working
  tree file identical. Equals `freeze-2.json.counters."calibration/measure.py".sha256`.
- `git log -- .ufo/evidence/round-48/calibration/measure.py` → single commit `755298415f8c`;
  nothing after the freeze. Same for `freshness/measure.py`: single commit `755298415f8c`, blob
  `faefe9b442741bcd7238ffe028841a0da7453c14c70f9f33afbd0f77be2df63f` = freeze-2 value at all
  revs.
- Pins: `freeze-2.json.contract_sha256` `4fff75dbaa…` = contract blob at all three revs and
  working tree; `statements_sha256` `924102dfbc…` = `round-47/calibration/statements.json`
  working tree.
- Pre-registration content integrity: JSON-comparing `contract.json` at `f1cfaad36013` vs HEAD →
  `claims` equal, `axes` equal, amendments 1-3 byte-equal; the freeze commit adds amendments 4-10
  (each recorded with its `when`) and reflows JSON only. No claim/predicate/target/kill-rule text
  changed after `f1cfaad36013`.

## Check 4 — docstring predicate ≡ contract statement/amendment 3 ≡ receipt label — PASS for the predicate sentence; minor delta on amendment 3

- Contract `claims.C1.statement` vs the counter docstring "Frozen predicate" block:
  whitespace-normalized equality is **exact** (programmatic diff: no differing fragment).
- Contract `predicate_label` "C1_R48_PASS=true iff self_pin=1 stmts_pin=1 statements=22 rounds=3
  append_only=1 unpinned=0 total=0" = docstring label line (docstring adds a trailing `.` only) =
  the same iff sentence restated in `control/run-controls.py`'s docstring.
- Receipt label: `measure.py:573-578` prints
  `C1_R48[:…​_PARTIAL]: self_pin=… stmts_pin=… statements=… rounds=… append_only=… unpinned=…
  total=… mismatches=… unparsed=… unobservable=… dep_mismatch=… unattested=… oversize=…
  attested_extra=… fleet_drift=… sibling_moves=… base=… rev=… C1_R48_PASS=…` with
  `passed = self_pin==1 and stmts_pin==1 and len(statements)==n_expected and rounds==N_ROUNDS and
  append_only==1 and total==0 and fleet_drift==0 and not only`; `N_ROUNDS=3` (line 81),
  `N_STATEMENTS=22` (line 80). The iff fields all print and gate exactly as the contract
  sentence, with amendment 5's `fleet_drift==0` and the seat-probe `PARTIAL` rule (lines 59-60:
  a probe receipt can never read `C1_R48_PASS=true`). Label string is `C1_R48_PASS`. ✔
- Amendment 3 vs the docstring "row grammar (contract amendment 3)" block: **restated and
  expanded, not the same sentence** (normalized similarity ≈ 0.68). Deltas: ASCII `->` for the
  amendment's U+2192; the docstring adds "V = the distinct declared members (cap: the (line,
  exit) pairs; axis: the integers, exit ignored as in round 47)" and classifies "an unsorted
  list, a duplicate name, an unknown name, a missing deps clause or a missing/malformed
  `runs 3 CLASS` clause" as `unparsed`, where amendment 3 only defines `oversize` for
  count/class pairing and leaves the other violations unassigned. No contradiction found; the
  iff predicate itself is verbatim. Minor.

## Check 5 — control receipts scored with freeze bytes, before the deciding run — **FAIL for C1; PASS for C2 (with a serious side effect)**

C2 side (present and consistent):
- `control/c2-controls.{stdout,meta,exit,stderr}` exist only from `c7586b9a` (added 10:27:19;
  `git ls-tree` at `755298415f8c` shows the control dir held only the two harness `.py` files).
- `c2-controls.meta`: `scored_at_freeze_bytes=7552984 (control/c2-controls.py sha256 46b8c039…,
  freshness/measure.py sha256 faefe9b4…)` — both hashes equal `freeze-2.json` `controls` /
  `counters` entries, and the committed bytes at HEAD still hash to those values (recomputed).
  Date `2026-10-26T09:27:52-03:00` (attempt-2 re-scoring after the crash), work under
  `/fast/scratch/hyaku/tameshi-r48/L1/…`, never /tmp; each leg prints its `rev=` (amendment 9).
- Commit order: receipts committed 10:27:19 < deciding-run receipts (none exist; `after/`
  absent at HEAD 10:28:00). ✔

C1 side (**finding H1**): `control/c1-controls.*` do not exist — not at the freeze commit, not at
the content revision, not at HEAD, not on disk. `git log --all --format=%H --name-only` filtered
for round-48 control paths lists only `c2-controls.*` + the two harness scripts; on-disk `find`
for `*c1-control*` under `.ufo` finds nothing newer than round-47; no `CTL_A…CTL_E` output file
exists anywhere under `.ufo/evidence/round-48/` or `.ufo/waves/round-48/`. The w1 seat
`T48ExecC1Controls` never reported (in `pending_w1_seats_at_freeze`; no `T48ExecC1Controls.md`
was salvaged) and `deciding-run.sh` contains no `run-controls` step, so nothing downstream will
produce these receipts either. Consequence: the pre-registered C1 controls — CTL_A base→false,
CTL_B relabel→false, CTL_C superset→unattested, CTL_D deps-everything→dep_mismatch>0, CTL_E
emit→total=0 (contract `do_nothing_control`/`cheapest_controls`, exercised as designed in
`run-controls.py`, byte-identical to the w1 deliverable, sha `f5732f18a158…` = freeze-2 value) —
are unevidenced in the lane. `freeze_plan` step 2 says "the controls are scored and committed";
only the harnesses were committed.

**Finding H2 (predicted deciding-run step-0 failure).** The late-committed C2 control receipts
sit inside the deciding run's FROZEN_UNCHANGED path set: `deciding-run.sh:22` includes `$E/control`
(whole dir) in `FROZEN`, and line 23 sets `FROZEN_UNCHANGED=0, rc=1` when
`git diff --quiet "$FREEZE" "$REV" -- $FROZEN` fails. Measured:
`git diff --name-only 755298415f8c c7586b9a -- <the exact FROZEN list>` →
exactly `control/c2-controls.exit`, `c2-controls.meta`, `c2-controls.stderr`,
`c2-controls.stdout`. So the pre-registered single deciding invocation at
REV=`c7586b9a`, FREEZE=`755298415f8c` deterministically reports FROZEN_UNCHANGED=0 and
DECIDING_RUN_EXIT=1 regardless of both claims' outcomes. (The deciding run had not landed as of
HEAD 17cc5ce1; this is a prediction from the committed script and trees, not an observed run.)
Had the C2 receipts been committed at the freeze commit as `freeze_plan` prescribes, the frozen
set would have been clean.

## Findings by severity

- **H1 (freeze step-2 incomplete):** C1 control receipts (`control/c1-controls.*`) were never
  scored/committed; the C1 control legs CTL_A-CTL_E are unevidenced, and no committed mechanism
  will ever produce them (`deciding-run.sh` does not run `control/run-controls.py`). Evidence:
  `git ls-tree -r 755298415f8c|c7586b9a|HEAD -- .ufo/evidence/round-48/control/` (2 scripts at
  freeze; +4 c2 receipts at content/HEAD); `git log --all --name-only | grep control` (no
  round-48 c1 receipts); `grep -rln 'CTL_A' .ufo/evidence/round-48 .ufo/waves/round-48` (only
  contract/freeze-2/harness/spec/dispatch/w1 reports). Violates `freeze_plan` step 2 ("the
  controls are scored and committed") and leaves amendment 9 ("every control receipt prints the
  revision it was scored at") with no C1 object.
- **H2 (deciding-run invariant self-broken):** committing the C2 control receipts after the
  freeze inside `$E/control` (in `deciding-run.sh:22` FROZEN set) makes step 0
  (`deciding-run.sh:23`) fail with FROZEN_UNCHANGED=0 at the content revision; predicted
  DECIDING_RUN_EXIT=1 even if C1 and C2 pass. Evidence: the diff command above; script lines
  quoted in the report header.
- **M1 (minor, check 4):** the docstring's amendment-3 grammar block is an expansion, not the
  same sentence (adds a V definition and `unparsed` classifications amendment 3 does not state;
  ASCII arrow). The iff predicate, contract statement, and receipt label are verbatim-identical.
- **O1 (observation, check 1):** `w1/swarm-registry.json` mtime precedes the `f1cfaad36013`
  commit time by ~5.5 s (dispatch artifact, not a seat report); all 26 seat `.md` reports
  postdate both prereg commits.

## Residual risk and verification gaps

- The C1 controls may have been executed during attempt 1 with receipts lost in the host crash;
  the salvage commit landed no trace, so this is unverifiable from the lane. If the L1 scores
  them now, the receipts must carry the freeze bytes (`run-controls.py` `f5732f18…`,
  `measure.py` `572a5670…`) per amendment 9 — and note H2: the natural landing place
  (`$E/control`) is inside the FROZEN set, so any post-freeze addition there re-triggers H2 at
  whatever REV the deciding run uses; the frozen-set/commit ordering needs an explicit decision
  by the L1 (e.g., scoring controls before the deciding run and landing receipts per a rule that
  keeps step 0 meaningful).
- The C2 receipts' "scored at freeze bytes" claim is bound only by the receipt's own meta line
  (freeze-2.json records no receipt hashes); bytes at every revision do match freeze-2.json, so
  the claim is consistent, but the binding is textual, not hash-chained.
- I ran no counter and no control harness (probe rules); all conclusions are byte/commit-level.
  Whether the eventual deciding run in fact fails step 0 depends on the L1's invocation
  parameters — as committed, it must.
