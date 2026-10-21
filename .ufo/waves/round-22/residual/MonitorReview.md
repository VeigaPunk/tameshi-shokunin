# MonitorReview — round22 residual falsification (registry rows, contracts, source credit)

Reviewer: TameshiR22.MonitorReview (critic). Candidate `e4da41c3102f6f90b42257d4b8785335806ef954`,
base `51d49d58ac81a1b4ea17607c4f2c4757ed6189ad`, contract `.ufo/evidence/round-22/contract.json`.
Method: static reads plus `jq`/`sha256sum`/`git show`/`git blame`. Nothing was executed:
no tests, gates, registry-check runs, builds, installs, or git/jj mutations. Statements marked
[INFERENCE] come from reading code, not from running it.

Axes: registry operability (no-harm), strict source-credit (no-harm), gate contract
(self-test, exit class, pin, write scope), provenance truthfulness, and source-credit restraint.

## Blocking

### B1 — The new registry rows make the whole registry invalid, so `registry-check` exits 2 on every row

- Counterexample: `tools/registry.json` rows[44] `wave-accounting-frozen-entry` and rows[45]
  `wave-accounting-selftest` both have
  `"source": "SKILL.md round22 addition, tools/wave-accounting.py"`.
- Evidence: `tools/registry-check.py:108` `SOURCE_RE = ^[^@]+@[0-9a-f]{7,40}:[0-9]+(-[0-9]+)?$`;
  `registry_errors()` at `:257-262` rejects any row that doesn't match. `load_registry` (`:369-371`)
  then returns `registry invalid`, and `evaluate()` (`:844-846`) returns exit 2 before it selects
  any rows. So `--tag`/`--only` can't route around it, and it also applies under
  `--rev X --registry <live registry>`.
  `jq` check: these 2 rows are the only ones out of 46 that fail the regex. At the base revision,
  0 rows failed.
  [INFERENCE] Every one of the 44 previously-held rows (40/40 active at the r21 final) is now
  could-not-evaluate.
- Precedent: in r21 the new rows were "sources pinned to the landed SKILL registry rows1975–1978"
  (`LOG.md:1441-1442`), using the format `SKILL.md@<40hex>:<line>`.
- Impacted axes: operability no-harm (the r17 C2 registry monitor), and every claim that relies
  on "registered battery held".
- Smallest safe correction: set both `source` values to `SKILL.md@66a25abf9a07f99df6f8584044a83a21349706a1:1997`.
  `git blame` shows SKILL lines 1995–1998 come from `66a25ab`, and `e4da41c` leaves them
  unchanged. Do not change any other field.

### B2 — The final verification receipt is cited as retained, but it doesn't exist at the candidate

- Counterexample: `corpus/knowledge/callback-authoritative-accounting.md:2` says
  "final committed-revision execution is retained in .ufo/evidence/round-22/final/verification.json",
  and `corpus/lessons/round-22.md` (Mistakes row 1) says "Actual streams are retained in round22
  final/verification.json". `ls .ufo/evidence/round-22/final` returns "No such file or directory".
- Impacted axes: provenance truthfulness. This is a false-provenance pattern: the admitted entry
  states an observation as present before it was observed.
- Smallest safe correction: before admission, land the real committed-revision receipt at exactly
  that path. It should hold exits and streams for the selftest, the frozen-entry run (exit 0) and
  the wrong-count run (exit 1/TOTAL_MISMATCH), plus the instrument SHA and the measured commit.
  Otherwise, reword both lines as pending. Do not borrow an earlier result.

### B3 — The strict source-credit no-harm repair hasn't landed (r21 ledger dependency)

- Evidence: r21 established that tool/corpus edits invalidate strict source credit, and that the
  round must re-anchor the affected sections with traced reads. That work produced a per-round
  selector and registry row (`LOG.md:1415-1420`, `:1430-1433`, `SCORECARD.md:918-926`). The
  untracked `.ufo/evidence/round-22/source-refresh-plan.json` lists 15 affected SKILL sections
  (6-16 … 1964-1998) and says `"not_executed": "Plan only; actual traced reads occur after corpus
  and code freeze"`.
  At the candidate, none of these exist yet:
  - `.ufo/evidence/round-22/coldread/`
  - a `round22-coldread-selector-selftest` registry row
  - a SKILL selector row
  - an updated `SHONEN.md:10` pointer (it still points to `round-21/coldread/ledger.json`)
- [INFERENCE] The current strict monitor at `e4da41c` is below 62/62 (up to 15 sections uncredited),
  so "depth8/calibration8 as monitors" is not yet demonstrated. SCORECARD (`:980`) correctly
  defers this to "recorded separately".
- Impacted axes: calibration and depth no-harm.
- Smallest safe correction: carry out the planned traced re-anchors after freeze. Add the round22
  selector with its own `--selftest`, a registry row pinned per B1's format, and the SHONEN
  pointer. Record the actual current monitor at the measured commit. Retain any harmed
  intermediate, as r21 did.
- Classification note: this is an open dependency, not a design defect. It blocks admission only
  until the receipt exists.

## Nonblocking

### N1 — The selftest isn't standalone, and missing setup surfaces as "failed" instead of could-not-evaluate

- `tools/wave-accounting.py:140-152` `selftest()` loads its oracle from the evidence tree
  (`.ufo/evidence/round-22/measure.py`, a path relative to the tool) and holds no literal
  expectations of its own. The r21 facade precedent put "literal fixture exits and stable finding
  fields in facade" (`SKILL.md:1977`).
- PROTOCOL §Gate standard (`PROTOCOL.md:385-389`) is met only loosely: the expectations are
  committed in the repo, and they are independent of `evaluate()`.
- Exit-class defects [INFERENCE]:
  - A missing `measure.py` raises `FileNotFoundError` from `exec_module`.
  - `subprocess.TimeoutExpired` (the 15 s per-case timeout in `measure.py:49`) is uncaught.
  - Both produce a traceback with exit 1, which collides with the declared "1 failed".
  - The declared map (`SKILL.md:1997`) sends setup/unavailable to 2.
- Correction: wrap the module load and `measure()` call in `try/except (OSError, ImportError,
  subprocess.SubprocessError)` and return 2 with `FINDING: SELFTEST_UNAVAILABLE`. The frozen
  ruler stays untouched.

### N2 — Deeply nested input escapes the declared exception set in normal mode

- `run()` (`tools/wave-accounting.py:136`) catches `OSError, ValueError, TypeError, UnicodeError`.
- [INFERENCE] With CPython, `json.loads` on a digest-matching bundle nested about 10^5 deep raises
  `RecursionError` (a `RuntimeError`). That gives a traceback with exit 1, reported as "failed
  invariant" instead of 2/INVALID_INPUT.
- Correction: add `RecursionError` to the caught tuple.

### N3 — The counter row isn't a schema kind, and the ruler has no self-test of its own

- The `SKILL.md:1998` row uses kind `gate/counter`. Gate standard row kinds are `gate|probe`
  (`PROTOCOL.md:402`).
- Its "Self-invocation" column says the owning gate's `--selftest` covers it. That self-test is the
  counter itself, so a counter mutant (for example `ok = True`) is caught by nothing.
- The ruler is frozen, so this is an accepted tradeoff. Still, the label should say "frozen
  counter (gate semantics; no independent self-test)" and not imply coverage.
- `measure.py:78` also accepts any superset of finding IDs (`finding in finding_ids`). A
  classifier that emits every ID on any deviation would still score 8/8. The claim is limited to
  rejection, so this doesn't overclaim, but it is weak discrimination.

### N4 — The red half of the falsifier isn't registered with a committed expected verdict

- QUALITY45 (`corpus/QUALITY.md:450-453`) and the knowledge entry (`:40-46`) name the wrong-count
  run as the falsifier: exit 1/TOTAL_MISMATCH.
- `wrong-count-expected.json` pins only the digest (`d984c49c…`, which matches). No registry row
  commits exit 1 or the finding ID.
- The `SKILL.md:1997` "Persisted values" cell lists the wrong-count pair, but no registered command
  consumes it.
- Precedent for registered red rows: `context-capture-missing-env`.
- Correction: add a gate row with the same argv but the wrong-count paths, `expect.exit: 1`, and
  needles `"TOTAL_MISMATCH"`, `"ProfileBashTsukuroiCensus"`, `"V01WitnessTests"`. Optionally add
  those two names as needles on the frozen-entry row, so the "remain failed" claim is pinned.
  Both identities really are failed-with-report in wave2 of `bundle.json`.

### N5 — S082's source credit is scoped correctly but self-referential

- The S082 anchor checks out: line 1369 of `original-outcomes-final.json` at `51d49d5` is
  `"partial_report_files_do_not_rehabilitate_failed_jobs": true`, and its sha256 `029fc1e0…`
  matches `derivation.json`.
- CORPUS tier A for own-work is defined as "the lane's own re-runnable gate output"
  (`CORPUS.md:93-95`). S082 is a retained declaration file, not re-runnable output. The prior
  own-work A rows (S031, S050, S051) are tools.
- Its `teaches` cell states a normative rule taken from the lane's own earlier assertion of that
  same rule. The knowledge entry's admission therefore rests on self-citation. The rule is really
  a lane design decision, corroborated by the 146/146 callback corroboration.
- The scope cell also claims "original membership", but `derivation.json` takes membership from
  `round-21/w{1,2}/swarm-registry.json`, which S082 doesn't anchor.
- `sources-counts.json` records A 70→71 and mined 50→51. No expansion or frontier credit is
  claimed (`corpus/README.md:350-353`, "same-ground"), so this is not an admission-blocking
  overclaim.
- Correction: in the lesson or knowledge entry (rows are append-only), state that S082 grounds the
  declared statuses only, and that the rule is a lane decision. Add the swarm-registry files as
  the membership anchor in a future correction row if needed.
- Minor: `recheck: on-change` is a valid symbolic cadence (`scripts/sources-census.sh:582`), but
  nothing triggers it.

## Checked and holding

- **Pins:** `expected.json` matches `bundle.json` (sha256 `dfb1027f…`), and `wrong-count-expected.json`
  matches its bundle. The two bundles differ only in the wave2 `claimed` block (40/35 against
  38/37). The frozen-entry needles `"completed": 66`, `"dead": 80`, `"seats": 146`,
  `"finding_ids": []` are unambiguous, because the per-wave values are 28/38, 43/37 and 71/75.
- **Write scope:** normal mode is read-only. The selftest uses `TemporaryDirectory` plus
  `sys.dont_write_bytecode` (`:18`). `tools/__pycache__` is gitignored and holds only an older
  `wave-route-mix` pyc.
- **Retention:** every non-round22 change is an append-only addition (0 deletions). There are no
  round-21 file edits, and r21 stays admitted per the contract bounds.
- **Restraint:** no numeric expertise, promotion or provider-authentication claim appears in
  SKILL, SCORECARD, LOG, README or QUALITY45.

## Tool installs

None.
