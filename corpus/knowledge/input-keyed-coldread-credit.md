source: S058 — https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems-final.pdf — §4.2.2 Verifying Traces, p. 79:14 (published PDF sha256 d6c175a4…4ede, fetched 2026-10-20); S059 — https://bazel.build/remote/caching — §Known issues, "Bazel does not track tools outside a workspace" (fetched 2026-10-20); S064 — https://bazel.build/basics/hermeticity — §Benefits, §Identifying non-hermeticity (fetched 2026-10-20); S060 — https://man7.org/linux/man-pages/man1/strace.1.html — §Filtering `%file`, §General `-f`, §Output format `-y` (fetched 2026-10-20; host strace 7.2); own work — `corpus/lessons/round-16-verifier-spotcheck.md` §2 and §6 (routed R16-C2b) @ 98bea7da5801f4bc58e4187690ee1687c8a5061f; `.ufo/evidence/round-17/redbefore/` (round-14 bucket replay, X10/X07)
verified-at: 2026-10-20 (rules re-measured at lane commits e69b488, 09ee1d0 and 98bea7d)
recheck: 90d — re-open S059 and S064 (the tighter cadence) and run `python3 .ufo/evidence/round-17/measure.py --selftest` (exit 0) and `python3 .ufo/evidence/round-17/coldread/trace-inputs.py --selftest` (exit 0); a non-zero exit or a missing tool is drift, not a pass
ground: none — a calibration method for this lane's own cold-read ledger; no `corpus/README.md` frontier row moves

# Cold-read credit must be keyed to the inputs a read ran against

Scope: one method step for this lane's SKILL.md cold-read ledger — when a
recorded read still earns credit for a bucket. It does not make a trace a
sandbox, does not re-read anything by itself, and does not claim the page is
correct.

## 1. The observed hole (O)

Round 16 credited each SKILL.md bucket by the sha256 of its section text
(`.ufo/evidence/round-16/measure.py`, `coldread()`), plus a verdict and a
command count. The bucket `## Effective expectation reconciliation — round 14`
was read once (CR26) with `tools/mutate-and-run.sh` at `75ed934d…`; the
round's own runner edits moved it to `0673d2e5…`. The section bytes did not
change, so it stayed credited, while its recipe now exited 2
`expected_input_digest_mismatch`. The round-16 measure reported 54/54 and
score 8 at `98bea7d` (`.ufo/waves/round-17/w1/S08RunR16Probes.md`). A
mutation of `tools/evidence-disposition.py` that changed its behaviour (exit
2 → 0) also left all 54 buckets credited (`w1/M01ShaOnlyHole.md`).

## 2. The rule (O, `.ufo/evidence/round-17/measure.py`)

This is a verifying trace (S058): record the hashes of what a step used, and
treat the result as current only while every recorded hash still matches. A
cache hit is sound only for what its key records (S059, S064).

- Every credited entry carries non-empty `inputs` (lane path → sha256). Each
  path must be a regular blob (mode 100644/100755) with that sha at the
  measured rev; otherwise `input-drift:`, `input-missing:` or `input-not-blob:`.
- An entry that executed commands names committed trace receipts whose
  inputs it covers (`traces-unrecorded`, `trace-missing:`,
  `trace-input-unrecorded:`). This holds for `record` and `instruction`
  entries alike, so relabelling a bucket does not escape it.
- A failing entry whose inputs still verify vetoes the bucket.
- `SKILL.md` itself and the ledger are not inputs: the bucket is already
  keyed by its own section sha, and the ledger is the output.

Red-before on real bytes, round-16 ledger plus the replayed round-14 inputs
(`.ufo/evidence/round-17/redbefore/legacy-r14-inputs.json`, 19 inputs traced
at `e69b488`): the bucket is `credited` at `e69b488` and
`input-drift:tools/mutate-and-run.sh` at `09ee1d0` and at `98bea7d`
(`redbefore/measure-*.json`). Those runs use `--inputs-overlay`, so they are
demonstrations; a cited score uses no override.

## 3. How inputs are recorded (O)

`.ufo/evidence/round-17/coldread/trace-inputs.py` runs a command under
`strace -f -y` (S060) in a clone of the lane at a 40-hex commit, and keeps
regular files opened read-only by name that are tracked at that commit.
Write-opened paths, untracked files and `.git/` are excluded; Python runs
with bytecode caching off, so a `.py` source is opened rather than a cached
`.pyc`. Fleet files outside the lane are listed as external, never credited.
A read of the live lane from a clone is flagged `live_lane_reads`.

## 4. Limits (O/I)

An open trace records files opened by name. It does not see environment
variables, stat-only checks, reads on inherited descriptors, directory
listings, network, the clock, or objects read through `git show REV:path`
(observed: `w1/S12StraceFeasibility.md`). Host binaries are outside the key,
the same false-hit class S059 documents for compilers outside a Bazel
workspace. A seat can still skip a command; the rule makes a recorded read
checkable, not complete.

## 5. Re-measure

`python3 .ufo/evidence/round-17/measure.py --rev REV` → fields
`coldread.box3_full_page`, `coldread.sections_covered`, per-section `reason`,
and `calibration_restraint_score`; `overrides_used` must be false for a cited
number. Exits: 0 measured, 2 rev/blob/ledger missing, 64 usage.
