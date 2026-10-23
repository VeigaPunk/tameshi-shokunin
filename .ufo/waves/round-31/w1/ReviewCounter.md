# ReviewCounter — frozen C1 counter code review (round 31, wave 1)

Verdict: the frozen counter is faithful to its docstring and to contract.json.
Every acceptance check passed; the only defects found are robustness gaps that
fail safe (crash or honest stop, never a silent pass). Two are listed below,
then confirmations, then residual risk and verification gaps.

Scope reviewed: /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py
(228 lines; sha256 657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584,
matches contract counter_sha256). Frozen surface: `git show c111dab58b0a8d55e991bbd2efe3aad56717b95a:SCORECARD.md`
(1480 lines; snapshot in my scratch, read-only analysis). Read-only review; the
counter itself was not run.

## Findings

### M1 (medium): unguarded exceptions in observe() crash without the summary line
- c1-measure.py:141-145 — `subprocess.run` is wrapped only against
  `TimeoutExpired`. Other exceptions are uncaught and propagate out of
  `futs[sid].result()` (line 208): the process dies with a traceback and
  exit 1, printing no `C1_R31:` summary and leaving earlier STATEMENT
  lines incomplete.
- Reachable crash inputs with the frozen statement set:
  (a) `UnicodeDecodeError` — children are read with `text=True`
  (line 142), i.e. strict decoding under the process locale; any REV at
  which a tool prints bytes the locale cannot decode (e.g. non-ASCII
  output under LC_ALL=C) crashes the run instead of marking the
  statement UNOBSERVABLE.
  (b) `OSError`/`FileNotFoundError` at spawn if `bash`/`python3` leave
  PATH (unrealistic) or fork fails under resource pressure — every
  frozen argv[0] is `bash` or `python3`, so a *missing script file* is
  NOT a crash: `['bash', '<missing>.sh']` exits 127 and
  `['python3', '<missing>.py']` exits 2, both correctly yielding
  UNOBSERVABLE via the pattern miss.
  (c) failure writing `obs-*.stdout` (line 146) if --work becomes
  unwritable mid-run.
  (d) `KeyError`/`ValueError` from the blanket `.format` at line 138 —
  verified unreachable today: the only braces in the frozen argv strings
  are the intentional `{work}`/`{clone}`/`{rev}` placeholders (CMD_D,
  lines 34-36, is brace-free).
- Contract impact: the kill rule expects unobservable statements to
  appear in the printed accounting (`unobservable=N`); a crash aborts
  before the summary. The contract's target line stays absent, so
  detection is intact — this is a shape violation of the documented
  exit contract ("Exit 0 iff true; 1 otherwise; 2 on setup error",
  docstring line 21), not a false-pass path.
- Exact exposing input: `LC_ALL=C python3 c1-measure.py --rev REV
  --work EMPTY` — `git show REV:SCORECARD.md` (lines 196-197) decodes
  with the locale and the file carries `–` (line 64) and `→` cells, so
  strict ASCII decoding raises `UnicodeDecodeError` before any
  statement is measured: exit 1, no `C1_R31:` line. Child stdout has
  the same exposure at line 142. Observed at base: the run succeeded,
  so the measured environment decodes these files — latent
  environment dependence, not a live defect at the frozen revs.
- Correction (for the record; counter is frozen): catch `Exception`
  around the spawn/decode block and return `(None, 'spawn-error')`.

### L1 (low): --work is populated before setup can fail, making the same --work
directory unreusable
- c1-measure.py:177-195 — `os.makedirs(work + '/fleet')` (line 180) and the
  clones (lines 191-195) happen before all failure points (rev-parse failure
  exits at 184 after fleet/ exists; clone/checkout failure exits at 195 after
  partial clone state). A second run reusing the same `--work` hits the
  "must be empty" guard at line 178 and exits 2.
- Exact exposing input: `python3 c1-measure.py --rev BADREF --work D`
  (exit 2) then `python3 c1-measure.py --rev GOODREV --work D` → exit 2 even
  though nothing is wrong. Contract usage names EMPTY_SCRATCH_DIR, so normal
  use is unaffected; only retries are penalized.
- Correction: create nothing until all validation passes, or clean up on the
  exit-2 paths.

### L2 (low): text-mode append_only can differ from a true byte-prefix check
- c1-measure.py:201 — `rev_sc.stdout.startswith(base_sc.stdout)` compares
  decoded text, not bytes. `text=True` (line 142 and the `git()` helper)
  performs universal-newline translation and strict locale decoding. Two
  consequences: (a) under a non-UTF-8 locale, decoding the en dash at
  SCORECARD.md:64 (`Score (0–10)`) or the `→` rows raises
  `UnicodeDecodeError` inside `git show` → unhandled crash (same M1 class);
  (b) universal-newline translation can in principle flip the byte-prefix
  answer: if base SCORECARD.md ended with a lone `\r` and REV's file starts
  the differing suffix with `\n`, both decode to `\n` and `startswith` yields
  1 while the byte predicate is false.
- Exact exposing input for (b): base blob `b"...\r"`, REV blob
  `b"...\nX"` — byte-prefix false, text-prefix true → append_only=1
  reported where the contract's byte rule says 0. Measured at c111dab: the
  frozen scorecard contains 0 `\r` bytes, and the before-run at base
  succeeded, so this is latent-only under the current surface. Listing for
  completeness; the honest direction is that a stray CR could only create a
  false append_only=1, never a false 0.
- Correction: `git(..., text=False)` style byte capture for the two
  scorecard reads, or `data.endswith`/prefix on `bytes`.

## Confirmations (all verified against the frozen artifacts)

- Claim regexes vs old rows (c111dab SCORECARD.md): running the module's own
  `last_rows` + `claim_of` on the frozen file selects exactly the frozen
  surface — cap rows = lines 240-249 of the single `| Capability |` table at
  line 238, axis rows = lines 66-67 of the single `| Axis | Score (0–10) |`
  table at line 64 — and all 12 parse. Tuples: sources-registry ('0','44')
  via `exit (\d+), (\d+) rows` on "→ exit 0, 44 rows"; mutation sweep
  ('80','80','0'); six-leg regression ('PASS','6','6','0'); repeat-control
  ('PASS','29','0'); pin ('18','18','0'); witness ('39','39','0'); evdisp
  ('34','34','0'); r15 ('0','49','49'); envdiff ('9','9'); waveacct ('8','8');
  axis ('6',) and ('0',). Identical to `before/c1-at-base.stdout` claimed
  columns — the freeze commit's rows equal base's for all 12 statements.
- Re-stated rows in the same phrase form parse correctly: substituting the
  live values into each frozen row's phrase shape (e.g. "exit 0, 92 rows",
  "`MUTATE_SELFTEST: 106/106 pass`, exit 0", "19/19 PASS0", "PASS66/66
  exit0", "| depth | 9 |") yields the fresh tuples under the same claim_of.
  The five statements whose values did not change between base rows and live
  output (repeat-control, witness, r15, envdiff, waveacct) parse unchanged.
- Observed regexes vs real output formats (before/prefreeze-format-recon.txt
  plus wave-accounting.py:188): `MUTATE_SELFTEST: 106/106 pass`, `SELFTEST:
  PASS (29 cases)`, `SELFTEST: PASS (19/19)`, `SELFTEST: PASS 39/39`,
  `SELFTEST: PASS (66/66)`, `ENVDIFF_SELFTEST: 9/9 pass`,
  `ACCOUNTING_SELFTEST: 8/8 pass` (literal print at wave-accounting.py:188;
  the `ACCOUNTING_EXTRA_SELFTEST` line does not match the anchored pattern),
  `REGRESSION: SETUP (cases=9 passed=0 cannot-verify=9)` matches the
  regression shape, and the census marker `== A rows` is a literal in
  sources-census-v2.sh. The monitor (`calibration_restraint_score` JSON) and
  r15 `summary SELFTEST: PASS (49/49)` formats are confirmed by
  before/c1-at-base.stdout observed=8 and observed=0,49,49 respectively.
- Tuple orders agree per statement: the two out-of-order pairs are handled
  deliberately — census returns `(exit_code, A_rows)` (line 150) matching
  claim order (exit, rows); r15 returns `(code, n, d)` (line 163) matching
  claim order (exit, n, d); depth/envdiff/waveacct drop the exit code
  (lines 160-165) matching their 2- and 1-group claims; the generic
  `g + (str(code),)` (line 166) matches the remaining trailing-exit claims.
- Table detection: `tables()` (lines 91-104) yields header + body past the
  separator; `last_rows` (lines 111-123) keys (kind, first cell) so the last
  matching row in file order wins — implementing the docstring's LAST-row
  rule. Verified against the full frozen file: exactly one Capability
  table, exactly one `Score`-headed axis table; nine other `| Axis |`
  verdict tables (lines 105, 181, 319, 382, 439, 534, 585, 623, 675) are
  correctly skipped because header[1] does not start with 'Score'. No
  indented pipe lines, no tilde fences, no HTML comments exist in the
  frozen file; the two column-0 fences (lines 71, 76) are blanked by
  strip_hidden (lines 78-89) and contain no rows anyway.
- strip_hidden: ungreedy `<!--.*?-->` plus fence toggle on
  `lstrip().startswith('```')` (handles indented fences); hidden-region
  controls (commented/fenced rows) become invisible → their statements go
  UNPARSED or read stale visible rows → killed, as designed.
- append_only (line 201) implements the predicate's byte-prefix clause
  modulo the L2 text-mode caveat.
- Regression mirror layout: six-leg regression runs with cwd = the mirror
  clone at work/fleet/tameshi-shokunin (line 137), sibling `*-shokunin`
  repos symlinked at lines 186-189. Recon proves the need: flat-layout
  regression fails `repo_identity_mismatch` → `REGRESSION: SETUP
  (cases=9 passed=0)`; the mirror run at base printed observed=PASS,9,9,0.
- Exit codes: 0 iff `mism==0 and append_only==1` (lines 221-224); 1 on any
  miss; 2 on the four setup failures (non-empty --work 177-179, unresolvable
  rev 181-184, clone/checkout 191-195, unreadable scorecard 196-200);
  argparse misuse also exits 2. Matches docstring and contract.
- Controls coverage: rows deleted / header retitled / rows hidden →
  UNPARSED; wrong or stale-copied values → MISMATCH (first-match `re.search`
  at line 132 reads the first value occurrence in the row); in-place rewrite
  → append_only=0; do-nothing → stale values → MISMATCH. No control meets
  the counter except honest restatement (or appending a new last table of
  the same type with correct values, which the predicate's last-row rule
  licenses by design).
- env() strips all `GIT_*` (lines 71-74) so spawned commands cannot inherit
  a foreign index/work-tree; PYTHONDONTWRITEBYTECODE is set; obs-* files are
  bounded at 200 KB tail each (line 147); REV is injected for CMD_D
  (line 140); both clones are detached at the resolved commit (lines 192-193).

## Residual risk

- The counter measures scorecard-vs-tool-output consistency only; a tool
  committed at REV that fabricates its printed numbers would match a row
  quoting them. The predicate covers the property "row equals what the
  command prints", and the contract delegates tool drift to the no_harm /
  cold-read obligations — accepted scope, stated so wave-2 does not read the
  counter as a tool-integrity check.
- `first_cells` (line 108) splits on every `|` — a literal pipe inside a
  re-stated cell would corrupt indexing (fails safe: the statement row keys
  wrongly → UNPARSED).
- `tables()` assumes a separator at body offset (block[2:], line 101); a
  separator-less appended table drops its first data row (fails safe).
- An unterminated `<!--` (no `-->`) defeats comment stripping; hidden rows
  then count as visible — affects the "rows hidden in a comment" control
  only in the safe direction.
- stderr of children is captured but never inspected or stored; diagnostics
  for an UNOBSERVABLE verdict rely on exit code alone.

## Verification gaps

- The counter was not executed (bounds: nothing runs in the lane); all
  findings derive from the frozen source, the frozen scorecard snapshot, the
  recon file, and the before-run receipt — plus importing the frozen module
  in scratch to run its pure functions (last_rows/claim_of) over the
  snapshot. The before-run receipt itself supplies the empirical end-to-end
  proof at base (unparsed=0, unobservable=0).
- Recon does not contain the calibration monitor's JSON line or the r15
  `summary SELFTEST` line; both formats are evidenced by the before-run's
  observed values only.
- Future-REV behavior for statements whose tools change shape (e.g. census
  printing `== A rows` with a trailing space → `(\d+)$` no longer matches)
  fails safe to UNOBSERVABLE by construction.

## Tooling

No installs or upgrades were needed (python3 and git already present).
All lane access was read-only `git show` plus file reads; the counter and
all referenced tools were analyzed, never executed against the lane.
