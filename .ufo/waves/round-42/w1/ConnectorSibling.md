# ConnectorSibling — sibling-lane overlap scan (round 42, wave 1)

Role: leaf connector, read-only. Access date 2026-10-25. Lane: tameshi-shokunin.
Scope: sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin` excluding tameshi
(20 lanes). No lane checkout edited; only write is this report.

Method (exact commands):
- `ls -d /home/vgpnk/Projects/shokunin/*-shokunin | grep -v tameshi-shokunin`
- `grep` over each sibling's `{tools,scripts,verifiers,census}` dirs for:
  `census|receipt|mutant|kill|oracle`; `--out|dest=.*out|add_argument\(['"]--out|self\.\w+\s*=\s*`;
  `write.path|write_path|write-path|output.flag`; `stale|freshness|mtime|committed.*receipt|expired`;
  `mutant|mutation|killed.*surviv|survivor`; `ast\.Attribute|ast\.Name|"self"|'self'`; `self\\\.|'self\.'`.
- Direct reads of ~25 candidate files (paths cited below).

---

## A. Write census resolving `self.<attr>` / argparse `--out` destinations (vs tameshi v4)

**Finding: no sibling tool resolves `self.<attr>` attribute-bound write destinations, and none
analyzes other code's `--out` flags as write destinations. tameshi v4 duplicates nothing here.**

Closest structural neighbors:

1. **kotodama `tools/harness/receipt_guard_adoption.py`** — an AST write-destination resolver.
   - `write_sites()` at `:429-472` detects `write_text`/`write_bytes`/`open(write)`/
     `os.replace`/`os.rename`/`shutil.move`/`Path.replace` sites (WRITE_METHODS/OPEN_METHODS/
     MOVE_DOTTED at `:66-69`) and resolves targets via `Resolver` (`:139-278`): constants,
     f-strings, `os.path.join`, `Path(...).parents[N]`, `resolve/absolute/expanduser`.
   - BUT `_attribute()` (`:223-233`) only handles `.parent/.parents` + `RESOLVE_ATTRS`;
     **no `self.<attr>` handling, no argparse inspection**. Embedded subprocess-script writes are
     found inside string literals (`embedded_write_sites` `:475-514`).
   - Verdict: resolves a *different* destination vocabulary (file-write methods to the runner's
     own receipt path), not v4's `attr`/`outflag` classes.
2. **tsukuroi `tools/check-revision-binding.py:825-829`** and **kotoba
   `verifiers/check_gate_registry.py:85-89`** walk ASTs for `add_argument` calls (argparse flag
   discovery), but never resolve where those flags write.
3. Tools that *consume* their own `--out` (not analysis): kaidoku
   `tools/round-25/a3/tally-resolution.py:80-84`, `tools/round-28/select-heldout.py:114-118`,
   `tools/round-33/timestamps/run-gate-hashed.py:158-159`; kama `tools/echo-recheck.py:432`,
   `tools/instrument-agreement.py:125`, `tools/capability-repertoire-audit.py:211`; kotoba
   `verifiers/check_could_not_evaluate.py:346`; kake `scripts/live_snapshot.py:193`,
   `scripts/source_snapshot.py:264`; tsukuroi `tools/run-receipt.py:18-22`.

**tameshi v4** (`tools/write-path-census-v4.py`; measured by `.ufo/evidence/round-42/census/measure.py`)
resolves (a) attribute-bound destinations `self.<attr>` set through same-class method returns and
(b) argparse output-flag `--out` destinations. No sibling provides either mechanism.

## B. Check that a committed receipt is stale against the tree (vs C1 m10)

**Finding: the "committed record vs tree" pattern exists in several sibling lanes; no one tool
implements m10's exact `present`-assertion + supersede semantics.**

Closest analogs:

1. **tabi `scripts/check-selfassessment.mjs`** — calibration gate:
   - `m2-receipt-exit` (`:41-46`): "A committed evidence receipt that records a command and its exit must
     reproduce that exit when the command is re-run", using only the closed grammar
     `git cat-file -e <rev>:<path>` / `git show <rev>:<path>`; every other command is
     could-not-evaluate.
   - `m1-selftest-tally` (`:29-40`): a SCORECARD tally must agree with that gate's OWN `--selftest` at the
     measured revision; oracle is the gate binary, "never a committed receipt (a receipt can
     carry the stale figure)" (`:31-33`).
   - Bullet line: `m2-receipt-exit` is the closest sibling to C1 m10's spirit (committed receipt
     vs observable tree/reproduction).
2. **kotodama `tools/replay-frozen.py`** — replays frozen gate-manifest rows: verifies
   `gate_sha256`/input `input_sha256`/recorded `output_sha256` **before** running, executes the
   pinned gate against the pinned snapshot in an isolated mirror, compares observed exit code,
   finding count and output bytes vs the record; disagreement → exit 1 ("replay mismatch").
3. **mori `tools/mori-retention-reconcile.py`** — reconciles committed retention receipts against
   a tree scan at the receipt's `measured_revision`: `scan()` (`:145-157`) re-derives per-line
   `line_sha256` hits from tree blobs; `:197-222` compares against claimed hits, with an explicit
   **`stale`** bucket (`:214`) and finding `allowlist_stale` (`:222`).
4. **kama `tools/round33-gate-receipts.py` `audit()` (`:414-462`)** — reads committed receipt
   blobs at `tip`, re-derives expected receipts from pinned `source_rev` (rebuilds inputs and
   re-runs the gate as oracle), compares headers/stdout/stderr field-by-field; mismatches count as
   `invalid`.
5. **kake `scripts/receipt_replay.py:465-466`** — "audit.json differs from the receipt the
   validator reproduces at this revision"; also bounds `observedAt/fetchedAt` against REV's
   committer timestamp (`:16-19`).
6. Presence-only gates (existence, not staleness): kaidoku
   `tools/round-31/cited-runs-gate.py:491-495` (counter pair must match the committed receipt;
   case `counter-miscount`); tsukuroi `tools/check-report-receipts.py` (revision-cited gates must
   have committed receipts at the cited revision).

Related-but-distinct: chousa `tools/research-gate.sh:2222-2226` — pinned `sha256` vs actual source
bytes → `observed=stale` (source staleness, not receipts).

**C1 m10** (`.ufo/evidence/round-42/calibration/measure.py:25-27,38-42`) audits committed wave
receipt `present` assertions against the tree at REV with a SUPERSEDE chain. No sibling duplicates
that exact check; tabi m2, kotodama replay-frozen, mori reconcile and kama audit are the closest
by pattern.

## C. Mutation kill oracle separating runtime errors from kills (vs C2 oracle)

**Finding: two siblings separate runtime errors from kills explicitly; one more separates
could-not-evaluate; the remaining kill oracles conflate crashes with kills.**

1. **kumitate `scripts/gate-mutants.mjs` K43 (`:6-11`)** — strongest separation. A mutant is
   KILLED iff its run is evaluable (no timeout, no overflow, clean process group, no spawn error,
   a parseable case summary whose total equals the control's) AND selftest exits with a numeric
   non-zero status AND stdout carries exactly `VERDICT: FAIL` AND an immediate second run agrees.
   Non-evaluable runs are not killed; a disagreeing second run is `UNSTABLE` (exit-2 class).
2. **tsukuroi `tools/mutants-owed-statements-r29.py:332-338`** — summary JSON carries a separate
   `crashes` bucket (`marked is None` → counter emitted no summary) distinct from
   `should_fail_accepted`/`should_pass_refused`; pass requires `not acc and not crashes`.
3. **tsukuroi `tools/mutants-kernel-taint.py:378-404`** — separate `harness_errors` bucket;
   per-mutant unparseable runs recorded with `verified_rows: null` + `stderr_tail` (visible, but
   not aggregated as a reject class).
4. **kotoba `verifiers/check_sweep_mutants.py:258-274,388-399`** — separates could-not-evaluate
   (exit 2: pristine self-test failure / git/read failure) from kill/survive verdicts, but a
   mutant's crash or timeout counts as `killed` (`code != "0"`).
5. **Not separating**: kaidoku `tools/round-34/replay-gate.py:269` (`killed_here =
   run.returncode != expected_exit` — a traceback counts as a kill); tsukuroi
   `tools/mutants-btrfs-space-r30.py:386-409` (a crashed counter is silently "not accepted");
   kake `scripts/citation_lint.py` mutants F/G/H/E and `scripts/redirect_audit.py:452-515`
   differential knob mutants (in-process, no crash class); kaidoku
   `tools/round-30/c2-rust-refusals.py` `judge()`.

**C2 oracle** (`.ufo/evidence/round-42/census/measure.py:16-21`): a mutant is `killed` only when
every run exits 0 with parseable output AND ≥1 battery case differs from its declared
classification; non-zero exit / Traceback / unparseable output = `runtime_error` (PIT "Run
error", Stryker RuntimeError, neither counted as kill); no differing case = `survived`. This
three-way structure is prefigured in kumitate K43 and tsukuroi owed-statements, but with distinct
definitions (K43 adds full evaluability preconditions + stability; tsukuroi detects crashes by
missing summary JSON). **No byte/file duplicate; no sibling duplicates C2 exactly.**

## PROVINCE.md (tameshi-shokunin) — absorption check

- `PROVINCE.md:14-17`: "Never edits a sibling's gate code (read-only probes; recommendations
  travel in round reports)" and "a pattern is admitted from evidence in TWO independent lanes
  before it is claimed general".
- `PROVINCE.md:20`: "Out of province → report, never absorb."
- `PROVINCE.md:44-47` (Adjacent): "report, never absorb: every sibling gate's code and product
  clauses (owner lane)".
- `PROVINCE.md:28-38` (Core) already list kumitate/kagi/tsukuroi/mado gates as **read-only**
  primary surfaces.

**Conclusion: absorbing ANY of the sibling tools above (kotodama resolver, tabi check-selfassessment,
kotodama replay-frozen, mori retention-reconcile, kama round33 audit, kake receipt_replay, kumitate
gate-mutants, tsukuroi mutant batteries) would violate `PROVINCE.md:14-17` and `:44-47`. Citing
them as read-only primary-surface evidence, and recording the now two-lane pattern (runtime-error
vs kill separation: kumitate K43 + tsukuroi batteries; receipt-vs-tree reproduction: tabi m2 +
mori reconcile + kama audit) in the method corpus, is within province per lines 15-17.**

## Risks / not checked

- Not read in full (internal logic may contain further analogs): souji
  `tools/souji-evidence-cache.py` (1860 lines), `tools/souji-census.sh` (3055), mori
  `tools/mori-census.sh` (4744), kumitate `kimi-census.mjs`/`omp-census.mjs`/`wave-census.mjs`
  internals, mado `tools/mado-tripwire.py` full logic, kengaku `plans/`, revenger, game lanes,
  audio fixture scripts beyond `measure_audio.py` paths.
- Within the scanned tool/script/verifier/census trees, no `self.<attr>`-resolving or
  `--out`-destination-resolving write census was found (grep coverage complete over those dirs).
- All `path:line` claims above come from direct reads (see transcript); no counter was run
  (read-only seat).
