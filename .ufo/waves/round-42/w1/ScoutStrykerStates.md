# ScoutStrykerStates — S001 held recheck (round 42, w1)

**Seat:** L1Tameshi42.ScoutStrykerStates (leaf, no dispatch)
**Access date:** 2026-10-25
**Source:** S001 (SOURCES.md row 12) — Mutant states and metrics, Stryker Mutator docs,
https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/

## Finding

Re-opened live. The page's definitions confirm the S001 row's teaches, including the
answer to "is a runtime error counted as detected?" — **No**: detected = killed + timeout;
runtime errors (and compile errors) are invalid, excluded from `detected` and excluded from
the mutation score.

### Verbatim quotes (<=25 words, located in §Mutant states / §Metrics of the live page)

1. **Killed** (§Mutant states, Killed bullet): "When at least one test failed while this
   mutant was active, the mutant is killed. This is what you want, good job!" (22 words)
2. **Runtime error** (§Mutant states, Runtime error bullet): "The running of the tests
   resulted in an error (rather than a failed test). This can happen when the test runner
   fails." (22 words; the bullet continues "…For example, when a test runner throws an
   OutOfMemoryError or for dynamic languages where the mutant resulted in unparsable code.")
3. **Runtime error not in the score** (same bullet): "It is not represented in your
   mutation score." (8 words)
4. **Which states enter `detected`** (§Metrics, Detected): "Detected `killed + timeout`
   The number of mutants detected by your tests." — i.e. `detected = killed + timeout`.
5. **Score formula** (§Metrics, Mutation score): "Mutation score `detected / valid * 100`
   The total percentage of mutants that were detected." — `valid = detected + undetected`
   ("They didn't result in a compile error or runtime error.").

All five quoted strings verified byte-identical in the saved snapshot HTML via grep.

### Answer: runtime error counted as detected?

**No.** `detected = killed + timeout` (quote 4) and the Runtime error bullet states the
errant is "not represented in your mutation score" (quote 3); §Metrics excludes runtime
errors from `valid` (Invalid = `runtime errors + compile errors`). So a runtime error is
neither detected nor scored — it depresses the denominator `valid` only by being counted as
invalid, never by entering `detected`.

This matches the S001 row as recorded: "eight mutant states; score = detected / valid x 100
with detected = killed + timeout; compile and runtime errors excluded" (SOURCES.md:12), and
matches the C2 kill-oracle wording in contract.json (PIT Run error ↔ Stryker RuntimeError).

## Evidence / commands

- `read https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/`
  (native reader, 2026-10-25): full page text with §Mutant states, §Metrics, §Test states
  and metrics.
- Snapshot: `curl -sL --max-time 60 <url> -o /tmp/tameshi-r42-ScoutStrykerStates-20261025/mutant-states-and-metrics.html`
  - sha256: `ac2733869c64ac637a6beb6f2b315d46ca1afaa585eb5322c1a76be18698fc11`
  - byte size: 27068
- Verbatim verification: `grep -o` of each quote against the snapshot (exact strings above).
- Contract read: `.ufo/evidence/round-42/contract.json` (read-only; not edited).

No tools installed; no lane files edited (report aside). Snapshot dir kept under
/tmp/tameshi-r42-ScoutStrykerStates-20261025/ per seat bounds.
