# T51ConnCrossClaim — cross-claim pattern finder + planning walk (round 51)

Seat: T51ConnCrossClaim (leaf; no subagent dispatch). Lane repo read-only; all measurements
run from `git show` of committed bytes and from scratch clones under
`/fast/scratch/hyaku/tameshi-r51/T51ConnCrossClaim` (deleted before yield). No lane file was
edited. Numbers below are observed outputs of the named commands.

Source of truth: `.ufo/evidence/round-51/contract.json` (read first; never edited), frozen
counters `c1/measure.py`, `c2/measure.py`, `c3/measure.py`, `c1/frontier-expected.json`,
`c2/bash-drift-pins.defects.spec`, `c2/sweep/sweep.txt`, `c3/tools-base.json`, and the
round-21 cold-read monitor + round-49 refresh method.

---

## 0. Baseline facts re-measured (evidence)

- Counter selftests green at lane HEAD (`4e095c9c…`): `C1_R51_SELFTEST: cases=6 failed=0`,
  `C2_R51_SELFTEST: cases=11 failed=0`, `C3_R51_SELFTEST: cases=10 failed=0`
  (commands: `python3 .ufo/evidence/round-51/c{1,2,3}/measure.py --selftest`, TMPDIR=scratch).
- Frozen before-state reproduced at freeze `84aa673a`:
  - C1: `C1_R51: … frontier_rows=10 table_rows=10 frontier_bad=10 readme_prefix=1 sources_rows=131
    status_conflicts=1 usedby_missing=0 total=11 C1_R51_PASS=false`
    (command: `python3 .ufo/evidence/round-51/c1/measure.py --lane LANE --rev 84aa673a --explain`).
    7 status/round mismatches on the old table (F1 round, F2/F4/F5/F6/F8/F10 status) and 3
    no-supporting-pointer rows (F3, F7, F9); S022 `queued-with-used-by` at `corpus/SOURCES.md:33`.
  - C3: `C3_R51: tools=30 rows=2 covered=0 missing=30 deleted=0 selftest_fail_rows=1 total=30`
    — the two existing registry rows (SKILL.md:1503 repeat-control, :1504 bash-witness-study) are
    **both non-conformant today**:
    - `tools/repeat-control.py`: `MISSING (line 1503 pinned-path-missing:mismatch/expected.json)` —
      the cell's `mismatch/expected.json` token has no repo-relative path at REV (real path is
      `.ufo/evidence/round-12/ControlGate/mismatch/expected.json`).
    - `tools/bash-witness-study.py`: `MISSING (line 1504 finding-id-not-in-row (VERDICT:))` —
      its selftest last-line token `VERDICT:` is absent from the row's Self-test cell.
    So the L1 cannot just add 28 rows; it must also repair/replace these two rows inside the same
    `### Gate/probe registry` section (SKILL.md:1499-1516, the only section matching the counter's
    heading regex `^#{2,4} Gate/probe registry`).
- C2 sweep receipt already committed at `f0129a5` (sweep.txt, evidence/*.out, results.tsv);
  `MUTATE_DATE: 2026-10-26T23:53:02Z` is 19 s after the spec's first-adding commit `fe33538`
  (committer `1793058763` = 23:52:43Z) → `sweep_after_freeze` holds.
- Pin object verified: `git -C kagi-shokunin show e64e81b8…:corpus/drift-pins.sh | sha256sum`
  → `c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb` (equals spec pin and
  sweep CONTROL/S-RESTORE pristine hash). Rev resolves; blob mode 100755.
- SOURCES tail: rows end at S271 (`corpus/SOURCES.md:146`); next free ids are exactly S272, S273.
- Cold-read monitor at base: `score 8 credited 64`.

---

## (a) Causal separability — files two claims both touch, and can each verify alone?

Matrix (path → consumers, observed from the counters' `show()`/`exists()`/diff calls):

| Path | C1 | C2 | C3 | coldread (round-21 ledger) |
|---|---|---|---|---|
| `corpus/README.md` | frontier table (append) + prefix guard | new knowledge entry must appear in appended bytes (`sourced_entry`: `readme_ok`) | — | not a lost-section cause (see experiment §3.7) |
| `corpus/SOURCES.md` | whole-file status scan (S022 queued→mined; every mined used-by exists) | new S272/S273 row (mined, opened 2026-10-26, entry in used-by) | — | not a lost-section cause (same experiment) |
| `tools/mutate-and-run.sh` | — | leg edit (heredoc spec, PIN/REV vars, TABLE, regression call, tally/expect updates) | runner row's selftest must stay green; tool-set scan (`selftest` bytes) | 20 credited sections pin this file (input-drift) |
| `SKILL.md` §`### Gate/probe registry` (1499-1516) | — | — | 30 conforming rows | section bytes change → section lost (`no-ledger-entry`) |
| `corpus/knowledge/<entry>` | (used-by existence only) | new entry (diff-filter=A in `corpus/knowledge/`) | — | only if a section pinned it (none do) |
| `.ufo/evidence/round-51/c2/sweep/*` | — | sweep.txt + verdicts (not evidence/*.out) | — | — |
| `c1/frontier-expected.json`, `c3/tools-base.json`, `c2/*.spec` | read | read | read | — |

Separability verdict: **each claim is verifiable alone at REV** — the pass-predicates touch
disjoint deltas and the deciding script runs C1/C2/C3 sequentially with no inter-claim
consumption (deciding-run.sh:44-54). The couplings are real but all *one-directional*:

1. C2's new SOURCES row enters C1's status check (it must be `mined` with the entry in used-by,
   or C1 totals +1 for a conflict — the same row that C2's `sourced_entry` demands, so the two
   requirements coincide rather than conflict).
2. C2's runner edit must keep the runner's `--selftest` green: C3's row for
   `tools/mutate-and-run.sh` executes `bash tools/mutate-and-run.sh --selftest` and the runner's
   own selftest is currently **hard-wired to 9 legs** — `tools/mutate-and-run.sh:1994-1996`
   (extracts tally block by `nlegs=9` and asserts `${#tnames[@]} -eq 9`) and the `cases=9`
   expectations at :2008-2039. Adding the tenth leg requires updating all of these, or the
   runner's selftest exits 1 and C3 fails.
3. C3's SKILL.md edit and C2's runner edit both cost cold-read credit; the re-key (round-49
   method) must cover exactly the sections that lose it (measured: 20, see §3.7).
4. No-harm's `tools-scope` monitor allows the runner as the only `tools/` change — any other
   `tools/` byte change (e.g. a new helper) turns no-harm RED.

---

## (b) Shared blind spots of the three counters (measured, not just reasoned)

Per-count (spot list with evidence):

- **C1**
  1. Pointer *round* is not anchored: `frontier()` only requires the pointed line range (≤6
     lines) to contain the id + the *status phrase*; a cell saying `held (round 25) — README.md:78`
     passes even though line 78 says `held (round 1)`. The old table lines 78-87 are legitimate
     pointer targets for the wrong round. (c1/measure.py:128-142; observed at freeze: F1's
     mismatch is round=1 vs want=25.)
  2. `open` rows require no round and only the phrase — any `README.md:N` range containing the id
     and the word `open` satisfies (F3/F7/F9 currently have no pointer at all and score
     `no-supporting-pointer`).
  3. used-by existence is `git cat-file -e rev:path` only — no content/recency/quote check
     (c1/measure.py:164-168). A stale or empty file still passes.
  4. malformed (non-11-cell) SOURCES rows are silently skipped (c1/measure.py:153).
  5. The prefix guard is byte `startswith` over the whole base README — strict, good — but the
     appended table's *position* is only "last table whose header starts `| id | ground |`";
     an earlier same-header table would be ignored.
- **C2**
  1. Receipt authenticity: `sweep_check()` parses only `sweep.txt` text (control green line,
     defect lines, restore, done, date) — never `evidence/*.out`; a perfectly formatted synthetic
     receipt passes. The three deep `evidence/*.out` files are not read by the counter.
  2. Verdict expectations are *measured* (TABLE must equal sweep verdicts), and predictions are
     counted outside the predicate — the counter cannot distinguish a real hole from an
     equivalent mutant; the 3 kill-aimed survivors are unresolved by the counter (contract
     `cannot_see` confirms this is by design).
  3. The suite string is embedded in the runner and is opaque to `wiring()`/`leg_call()` (they
     only see the heredoc + call + TABLE). The sandbox-naming hazard (below) lives entirely in
     that string and is invisible to the counter.
  4. `sourced_entry()` only inspects files *added* under `corpus/knowledge/` (diff-filter=A);
     an entry appended by editing an existing knowledge file would fail (good), but the check
     `tail in srcl[0]` is a substring match — a `source:` line naming `corpus/drift-pins.sh`
     as part of a longer path still matches.
  5. `--regression` replays against **committed** lanes pinned revs via symlinked FLEET_ROOT; the
     replay's outcome is host/environment-dependent (TMPDIR/HOME propagation — see §3.4) and is
     not pinned to the sweep's environment.
- **C3**
  1. `row_reason()` validates shape, not truth: kind/write-scope/pinned-description content is
     never checked against the tool (contract `cannot_see`); the counter runs the selftest and
     usage probe only.
  2. Finding-id rule is weak: the marker must appear *somewhere* in the Self-test cell (substring),
     not as the command's expected output; a row can pass while the cell describes a different
     tool's output pattern.
  3. Pinned values: `PATHISH` accepts directory paths and bare basenames like `mismatch/expected.json`
     (which is exactly the current failing row); existence is repo-tree-only.
  4. Verdict map: only tokens 0 and 1 are required plus the usage code actually seen; codes a
     tool can emit beyond 0/1/usage are unverifiable by the counter (target of wave-2 probes).
  5. Concurrency: 6 parallel `run_cmd` jobs share one clone cwd; a selftest that writes relative
     to cwd can collide with siblings (not exercised by the counter's own selftest, which uses
     tools whose selftests write only under TMPDIR).
  6. Tool-set scan: any `tools/*.py|*.sh` whose bytes contain `selftest` at REV joins the set —
     C2 must not introduce a new such file.
- **All three**: they read committed state only (clean-tree precondition in deciding-run.sh) and
  trust that the artifacts they verify were produced by the work they describe; the deciding run
  is a one-shot at REV with no cross-run determinism check. Cold-read is the shared landmine:
  any byte change to the runner or the registry section drops credit unless re-keyed (measured
  20 sections, see §3.7).

---

## (c) Planning walk — integration steps after wave 1, then wave-2 attack items

### c1. Ordered integration steps for the L1 (content revision)

1. Verify control receipts exist and descend from freeze (deciding-run.sh:22-27 does this; they
   are already committed at `f0129a5`).
2. **Apply the runner leg first** — the only permitted `tools/` change. In
   `tools/mutate-and-run.sh` add: the `#   bash-drift-pins  kagi-shokunin/corpus/drift-pins.sh  2/10 (20 %)`
   ledger line; `PIN_DRIFT`/`REV_DRIFT` vars (40-hex rev `e64e81b8…`, 64-hex pin
   `c138d34c…`); `TABLE_DRIFT` = sweep verdicts in spec order
   (`K_MODE_CMP:KILLED,K_GONE_ARM:SURVIVED,K_AMBIG_GT:SURVIVED,K_COUNT_GE:KILLED,K_SHAPE_OPTIN:SURVIVED,S_SHA_CMP:SURVIVED,S_HARDLINK:SURVIVED,S_POLICY:SURVIVED,S_DUP_UNIQ:SURVIVED,S_USAGE_EXIT:SURVIVED`);
   the embedded spec heredoc byte-equal to `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`
   (sha256 `a98271f639bc520f7052e63efaaa0b560cda959d3122d9c6921dcd1b9b61a602`); the
   `regression_case_git bash-drift-pins \` call with the guarded sandbox suite string (mirror
   `tools/mutate-and-run.sh:1418` pattern: `h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" bash "$MUTANT" --selftest'`);
   update `nlegs=9`→10, the tally-harness vectors/`cases=9` strings (:1994-2039), the
   `REGRESSION_EXPECT` line (:1374), and any embedded-leg list iteration to include the new leg.
3. Run `bash tools/mutate-and-run.sh --selftest` → must still exit 0, last line `VERDICT: PASS`
   (this is both C2's sanity and C3's runner-row requirement).
4. Add the knowledge entry `corpus/knowledge/mutation-case-drift-pins.md` (headers mirroring
   `corpus/knowledge/mutation-case-kumitate-round-gate.md:1-6`): `source: S272 kagi
   corpus/drift-pins.sh @ e64e81b8 …`, `verified-at: 2026-10-26 …`, `recheck:`; body cites the
   ledger queue row `corpus/knowledge/fleet-kill-rate-ledger.md:119` (drift-pins, `unmeasured by
   sweep; hermetic`) and supersedes it in §3 style (see :280-282 of that file).
5. Add SOURCES row S272 (mined, opened 2026-10-26, used-by = the new knowledge entry); S273 is
   the next free id and may be used for a second row if needed — both must satisfy C1's scan.
6. Append the frontier status table to `corpus/README.md` (last `| id | ground |` table; one row
   per F1..F10; status cell = expected status + `(round N)` where non-open + pointer
   `README.md:<a>-<b>` with b-a ≤ 5 containing id + phrase). Leave base bytes a prefix.
7. Flip S022 `queued` → `mined` (`corpus/SOURCES.md:33`; used-by
   `corpus/knowledge/fixture-shrinking-pilot.md` exists).
8. Dry-run C1 in a scratch clone at the candidate rev → expect `total=0 C1_R51_PASS=true`.
9. **Re-key cold read** (round-49 method, scoped to the measured 20 lost sections — list below):
   for each heading write a new ledger entry whose trace-bound reads observe the new bytes;
   then extend the registry section's own entry (bytes changed → `no-ledger-entry`). The 20
   headings (lost in the cumulative edit experiment, in order): `## Eighth recorded case — round 18`;
   `## Live-tree re-pin and entry-command monitor — round 17`; `## Mutation-sweep recipe — numbered steps; bounded cold-read`;
   `## Restore discipline — before/after identity, not continuous non-write proof`; `## Seventh recorded case and full-page cold-read — round 16`;
   `## The leg ledger — replay, receipt, and how it is read (round 7, measured)`; `## The operator's runbook and the six-leg regression (round 10, measured)`;
   `### Gate/probe registry`; `### Reading a receipt — the discipline`; `### Round-16 gate/probe registry`;
   `### Round-17 gate/probe registry — re-pin and monitor`; `### Round-26 gate/probe registry — report interop`;
   `### The boundaries — what a service run is not`; `### The map — where a reader enters, artifact by artifact`;
   `### The protocol — ordered, fail-closed`; `### The receipt at this boundary`; `### The six-leg regression — usage and this round's receipt`;
   `### The tick and the pin read`; `### The tick, executed`; `### Using the ledger`.
10. Run `coldread-precheck.sh LANE BASE CAND` → `lost=0`, `cand_credited=64` (required: floor
    64 → cand 64).
11. Run no-harm monitors + `scripts/sources-census.sh validate` at CAND (deciding-run.sh re-runs
    them; they must be green before freezing).
12. Freeze CAND as the deciding rev; clean tree; `deciding-run.sh LANE REV FREEZE OUTDIR`;
    commit receipts only after it.

### c2. Wave-2 attack items (39 concrete artifacts; each names the artifact and the probe)

C1 (12):
- A1 F1 cell pointer-round probe: assert the pointer's line range contains the *claimed round*
  text (`held (round 25)`), not merely `held` (catches the line-78 trap). Artifact: appended
  table F1 cell.
- A2 F2 phrase-spelling probe: `grep -i 'partly held'` over the pointer range (not
  `partially held`).
- A3 F5 Core probe: status cell must contain `core (round 21)` parseable by `STATUS_RE`; pointer
  :330-338.
- A4 F6/F10 pointer-word probes: :608 and :599 contain `held (round 50)`/`held (round 49)`.
- A5 pointer-range-length audit for all 10 cells (`b-a ≤ 5`, exists).
- A6 table-position guard: exactly one `| id | ground |` header after base; exactly 10 rows,
  ids F1..F10 unique.
- A7 S022 semantic probe: `grep -c 'S022' corpus/knowledge/fixture-shrinking-pilot.md` — the
  used-by file should actually be the S022 teaches (the contract only demands existence).
- A8 census probe after flip: `scripts/sources-census.sh validate --root FLEET tameshi` → exit 0,
  no new warnings on S022.
- A9 prefix guard probe: `git show BASE:corpus/README.md` must be a byte prefix of REV's (cmp).
- A10 SOURCES consistency sweep: no row `queued` with a used-by and no `mined` without one
  (run C1's `sources()` logic standalone).
- A11 row-count delta: 131 → 133 (S272, S273) with no deletions; S022 cell-only change.
- A12 per-row pointer verification: for each Fk, `awk 'NR>=a && NR<=b' README.md | grep -E 'Fk|phrase'`.

C2 (13):
- B1 rev/pin existence: `git -C kagi-shokunin rev-parse e64e81b8…^{commit}` +
  `git show e64e81b8…:corpus/drift-pins.sh | sha256sum` = `c138d34c…` (re-run at REV).
- B2 embedded-spec bytes: extract the heredoc between
  `cat >"$d/bash-drift-pins.spec" <<'EOT'` and `EOT`; sha256 must equal `a98271f6…`.
- B3 wiring completeness: LEDGER_RE line, heredoc, `regression_case_git bash-drift-pins \` call,
  `TABLE_DRIFT` value = sweep table, counts (2 killed / 8 survived).
- B4 sweep receipt shape: CONTROL GREEN + `pristine-sha256=c138d34c…`, 10 DEFECT lines, restore
  OK, DONE, date > 2026-10-26T23:52:43Z.
- B5 **neutral-sandbox single-variable probe** (the confirmed kill):
  apply K_GONE_ARM/K_AMBIG_GT/K_SHAPE_OPTIN to a copy, run
  `env -i LANG=C TZ=UTC HOME=$h PATH=$PATH TMPDIR=$neutral bash MUTANT --selftest` → each exits 1
  (`drift-selftest: FAIL symbol gone: no /GONE/ in output`). Observed here: exit=1 for all three.
- B6 token-path reproduction: same mutants with `TMPDIR` containing the defect id → exit 0,
  `DRIFT_SELFTEST: PASS (13 cases)` (observed). Mechanism: `drift-pins.sh:403`
  (`elif ! grep -q "$3" <<< "$out"`) greps verdict words in output that prints scratch paths;
  the id token in `sandbox-$DEFECT_ID` satisfies the unanchored grep.
- B7 regression replay: `bash tools/mutate-and-run.sh --regression` from a `--shared` clone at REV
  → `REGRESSION: PASS (cases=10 passed=10`; expect band exactness (killed-delta 0, flips 0).
- B8 prediction ledger: `predictions_held=7/10`; the three misses are exactly the kill-aimed
  survivors (K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN) — report as data.
- B9 sourcing chain: knowledge entry `source:` line contains `corpus/drift-pins.sh` and S272;
  S272 row mined/opened 2026-10-26; entry in used-by; appended README names the entry.
- B10 ledger supersession: fleet-kill-rate-ledger.md:119 row now measured (the new case's TABLE +
  a §3-style entry, per ledger's own protocol at :312).
- B11 @old uniqueness: assert each of the 10 `@old` spans occurs exactly once in the pinned blob
  (incl. the two-line GONE span — the single-line fragment occurs twice: verify() at
  drift-pins.sh:231 and pin() at :345).
- B12 off-suite witness: S_SHA_CMP hole — construct baseline+symbols where only content changes
  (same lines/mode) → gate reports CLEAN under the mutant; proves a real hole.
- B13 usage-exit probe: `bash drift-pins.sh --r51-no-such-flag` → exit 2 at pin, exit 0 under
  S_USAGE_EXIT (hole).

C3 (10):
- C1 fix the two existing rows and re-run C3 at REV until `covered=30 total=0`.
- C2 kind-truth audit per row (gate vs probe semantics vs tool behavior; e.g. repeat-control is a
  gate, pbt-staged-id a probe).
- C3 write-scope truth per row (compare declared scope with observed writes under strace for a
  sample of tools).
- C4 verdict-map completeness per row: for each tool run `--r51-no-such-flag` and list the exit
  code; require it declared (bash-witness-study currently exits 64 on `--selftest`; rows must use
  the correct invocation, e.g. `python3 tools/bash-witness-study.py selftest`).
- C5 finding-id marker per row: last token of each selftest's last non-empty stdout line must
  appear in the row (runner: `VERDICT:`; repeat-control: `SELFTEST:`; etc.).
- C6 pinned-path audit: every backticked token with `/` must exist at REV (`git cat-file -e`),
  full paths, no bare basenames.
- C7 runtime budget: tally-audit-v2/v3 selftests exceeded 60 s in probes (rc=124); measure real
  duration and keep the deciding run's 900 s cap + 6-way concurrency safe.
- C8 workspace hygiene: run each selftest twice from identical clones; verify no writes outside
  TMPDIR/cwd that could collide with sibling jobs.
- C9 runner coupling: after the C2 leg edit, `bash tools/mutate-and-run.sh --selftest` must still
  exit 0 and print `VERDICT: PASS` (line 2048) — gate for the runner row.
- C10 section containment: all 30 rows inside SKILL.md:1499-1516; each Self-test cell holds
  exactly one backticked command with no shell metachars.

Cross/quality (4):
- D1 **QUALITY criterion candidate** (item d, below): "a suite's scratch path must never carry a
  token its oracle matches". Concrete artifact: the new leg's suite string
  (`sandbox-$DEFECT_ID` → TMPDIR carries the id) and the oracle at `drift-pins.sh:403`.
- D2 runner-row stability across REVs: C3's runner row must pass at base and after the C2 edit.
- D3 re-key coverage probe: after re-key, precheck lost=0; verify the 20-section list is exactly
  the drift set (README/SOURCES appends added no additional lost sections in the experiment).
- D4 deciding cleanliness: `clean-tree-before/after` empty except witness; receipts committed in
  commits descending from FREEZE.

---

## (d) One pattern worth a QUALITY criterion

Candidate: **a suite's scratch path must never carry a token its oracle matches.**

Evidence (observed this round):
- The drift-pins gate's selftest oracle greps verdict words unanchored over combined stdout+stderr
  (`drift-pins.sh:403`: `elif ! grep -q "$3" <<< "$out"`), and the suite runs the gate with
  `TMPDIR="$WORKDIR/sandbox-$DEFECT_ID/tmp"` (suite pattern at `tools/mutate-and-run.sh:1418`).
- With the defect id in the scratch root, K_GONE_ARM / K_AMBIG_GT / K_SHAPE_OPTIN survive (exit 0,
  `DRIFT_SELFTEST: PASS (13 cases)`) because the id substring `GONE`/`AMBIG`/`SHAPE` inside
  printed paths matches the oracle word.
- With a neutral scratch root, the identical mutants are killed (exit 1, `no /GONE/ in output`).
  Both directions reproduced in scratch; the sweep's neutral evidence (`K_GONE_ARM.out` = PASS)
  is the token-path case.

Generalization: an oracle that matches tokens in program output must not match substrings of
environment-derived strings (scratch paths, HOME, TMPDIR, dates, UUIDs) that the program
legitimately prints; the oracle must anchor to the verdict line grammar, or the suite must prove
its scratch paths contain no oracle tokens. This is a checkable, per-suite property (a lint over
the suite command string + the oracle regex) and deserves a QUALITY criterion for the runner's
leg suite strings.

---

## Summary

- All three counters' selftests green; freeze before-state reproduced (C1 total=11, C3 total=30,
  covered=0 — the two existing registry rows are non-conformant today and must be repaired, not
  just supplemented).
- Claims are individually verifiable at REV; couplings are one-directional: C2's S272 row must
  satisfy C1's scan, C2's runner edit must keep the runner's selftest green (it is hard-wired to
  9 legs: mutate-and-run.sh:1994-2039), and runner+registry edits cost cold-read credit (measured
  20 sections).
- The three C2 kill-aimed survivors (K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN) reproduce exactly as
  a token-in-scratch-path effect: neutral TMPDIR kills all three (exit 1), token TMPDIR passes
  all three (exit 0) — oracle at drift-pins.sh:403.
- Integration order: runner leg first (with tally/expect updates), then knowledge entry, SOURCES
  rows S272/S273, README table append, S022 flip, C1 dry-run, re-key of the 20 sections, precheck
  lost=0, no-harm + census, freeze, deciding.
- 39 wave-2 attack items listed (12 C1 / 13 C2 / 10 C3 / 4 cross), each with artifact and probe.
- QUALITY criterion candidate: an oracle's tokens must never appear in suite-controlled scratch
  paths the oracle reads; this round's three survivors are the counterexample.
