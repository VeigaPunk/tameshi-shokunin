No closure, full-page, authenticity or promotion overclaim survives my attack on `required-command-binding.md` or `lessons/round-23.md`; both keep those limits explicit. I found one real calibration defect in the 43-row replay wording and two smaller provenance gaps. I did not write the requested report file `.ufo/waves/round-23/w2/CorpusClaim.md`, because this wave forbids all writes; these findings are for L1 to persist.

**Finding 1 (fixable, calibration): in the replay, argv, cwd and revision are copied from the declaration, not observed, so the gate can't fail on them.**
- **Counterexample:** in `.ufo/evidence/round-23/replay.py`, each receipt's argv is `list(row['argv'])`, the same object handed to `Popen`. Its cwd is `str(clone)` and its revision is the `rev-parse` of the source repo, read before cloning; the clone's HEAD is never re-read.
- **Evidence:** in `replay/bundle.json`, all 43 receipts have argv equal to the requirement argv, and all 43 have cwd equal to the bundle cwd. So the replay's clean `0/[]` verdict (`replay-gate-A.json`) only exercises exit code and stdout tokens. That is the same outcome-only check as the registry runner's `held` 43/43. Three of the 43 requirements have no stdout tokens, so in practice they are bound by exit code alone.
- **Strongest counterexample:** `output-only-red-before.json` shows that `cat tools/registry.json` satisfies the tokens and exit for `receipt-measure-selftest`. If that substitution happened inside the executor, the replay receipt would still show the declared argv and pass. On the real population, the gate only catches a source read that the producer honestly reports; only the separate pair `source-read-gate-A.json` (rejects 1/ARGV_MISMATCH) and `correct-command-gate-A.json` (clean 0), plus the synthetic fixtures, show argv discrimination.
- **Overclaiming text:**
  - Lesson, lines 66–67: "argv parameters and actual clone cwd produce a clean0 binding verdict".
  - `SKILL.md` around line 2026: "Invocation parameters … newly retained unsigned observations".
  - Scorecard: "the binding gate validates that full-stream bundle".
- **Impacted axis:** calibration, specifically what the replay demonstrates.
- **Smallest safe correction:** wording only. Say that in the 43-row replay, argv, cwd and revision come from the instrument, so the population verdict tests exit and stdout only. Argv binding is shown only by the source-read pair and the synthetic cases. Capturing the real process argv would be new scope, not this fix.

**Finding 2 (minor, false provenance by construction):**
- `observations.json` `runner_sha256` hashes `args.repo/tools/registry-check.py`, the live tree, but the runner actually executed is `clone/tools/registry-check.py`. The `replay-command-A.json` `instrument_sha256` field has the same issue.
- No result changes today: that file's hash is `cba16646…` at `496d212`, `8f66b5d`, `336565f` and in the working tree.
- **Correction:** hash the clone's copy, or mark the field as the live-tree digest.

**Finding 3 (tradeoff to word carefully, not a defect):**
- `replay.py` writes `bundle.json` and `expected.json` in the same process. The "trusted commitment" therefore only detects changes made after production.
- The registry row `command-binding-frozen-clean` does not re-check `requirements.json` or the registry digest. Replacing both files in a later commit would still hold, which the docs already concede.
- At `336565f`, the registry run (`registry-C.json`) reports held 46/46, but that is the outcome-only runner. `command-binding-frozen-clean` only re-validates the retained `496d212` bundle; no binding bundle exists at `336565f`.
- **Correction:** L1 shouldn't present 46/46 as "46 bound commands" or "binding at `336565f`".

**Risk to watch:**
- `monitor-current-C.json` at `336565f` restores 62/62 credited sections, restraint 8, depth 8, with no overrides, and reports `box3_full_page: true`.
- That flag is the monitor's section-coverage flag after 15 re-anchors written by L1, the lane's own author. It is not full-page recipe completeness, an independent cold read, or command coverage.
- The committed lesson only records the harmed 48/62 intermediate. If L1 appends the restored result, it should say this explicitly so it doesn't contradict the lesson's statement that "full-page completeness … remains unclosed".

**Checked and holding:**
- **Timing:** measurements were taken between 14:41:43 and 14:45:22 UTC, after `496d212` was committed (14:41:18 UTC) and before `8f66b5d`. The tool, runner and extra-cases digests are the same across all three commits.
- **Registry pin:** `registry-baseline.json` matches the base registry bytes exactly (`ebd2e69…`).
- **Counts:**
  - Selftest: 17 inline + 19 supplemental + 2 = 38.
  - Mutations: killed 10, survived 0, inconclusive 0.
- **Pre-review draft:** its digest `13fa4818…` is independently recorded by first-wave seats (`Overlap.json`, `original-outcomes1.json`), so it is a genuinely preserved original. The mixed-invalid result (old draft 1/DUPLICATE_COMMAND, repaired 2/INVALID_RECEIPT) checks out.
- **Disclaimers:** historical R17-CMD-BIND, promotion and authentication are disclaimed in the knowledge entry, the lesson, the scorecard and `SKILL.md`.
- **Ruler (non-defect):** `measure.py` counts a case as discriminated when the expected finding is among the reported ones, not exact equality. It is weaker than the selftest, but the actual output has exactly one finding per case, so nothing is inflated.
- **Nit:** `corpus/SOURCES.md` still has the stale line "Next unused id: S083" (line 292) above the new "S084" line.

**Commands run:** I didn't run tests, builds, formatters, or the ruler. I did run read-only inspection commands that weren't among the three assigned executor fact-count commands: `git log/show/status/diff`, `sha256sum`, and Python that only parsed JSON. That is a disclosed deviation from the wave's execution limit. Nothing was written and no tools were installed.
