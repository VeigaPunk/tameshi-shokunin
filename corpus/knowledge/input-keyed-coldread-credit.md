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

## Errata — round 18 (R17-KNOW-EXIT, entry-local)

Scope: corrects §5 (line 75) and the `measure-*.json` citation in §2 (lines
45–48) as published at 183f87b899e6cae46be98d251cbc87fb5118f6ca. Lines 1–75
are unchanged. The round-17 evidence bytes they cite are retained, not
rewritten.

### 1. The §5 exit sentence (line 75) is false for a missing ledger

Line 75 reads "Exits: 0 measured, 2 rev/blob/ledger missing, 64 usage." The
ledger half is wrong. The true split at 183f87b899e6cae46be98d251cbc87fb5118f6ca:

- Missing **default** ledger (`.ufo/evidence/round-17/coldread/ledger.json`
  absent at REV): not an error. It is a measured `no-ledger` state. Every
  section gets `reason: "no-ledger"`, `coldread.reasons` is
  `{"no-ledger": N}`, and the exit is 0.
- Missing **explicit** ledger: `--ledger-file` unreadable, or `--ledger-rev
  REV:PATH` with an absent rev or blob, exits 2.
- Exit 2 also covers a missing `rev`, a missing required blob, and an
  unreadable or forbidden-field `--inputs-overlay`.

Source (`.ufo/evidence/round-17/measure.py`): the no-ledger branch is
`measure.py:535-553` (`return out` at 553); the default-ledger path is
`measure.py:1545-1547`; the explicit-ledger exits are `measure.py:1520-1543`;
the overlay exits are `measure.py:1554-1592`; `return 0` is `measure.py:1598`.
The tool's own usage text states the same split at `measure.py:93-95`.

Observed: `.ufo/evidence/round-17/redbefore/measure-98bea7d-strict.json`
records `ledger_present: false`, `overrides_used: false`,
`coldread.reasons: {"no-ledger": 54}`, and no `error` key. The default ledger
is absent at 98bea7d. The receipt does not record an exit code; exit 0 follows
from the return at `measure.py:1598`.

### 2. The `measure-*.json` citation in §2 is narrowed

The glob `redbefore/measure-*.json` matches four receipts. Three are overlay
runs (`overrides_used: true`, `inputs_overlay_merged: 1`,
`trace_gate: "legacy"`):

- `redbefore/measure-e69b488.json`: "Effective expectation reconciliation —
  round 14" is `credited`.
- `redbefore/measure-09ee1d0.json`: `input-drift:tools/mutate-and-run.sh`.
- `redbefore/measure-98bea7d.json`: `input-drift:tools/mutate-and-run.sh`.

`redbefore/measure-98bea7d-strict.json` is not an overlay run. It has
`overrides_used: false` and `trace_gate: "strict"`. At 98bea7d the default
ledger is absent, so it reports all 54 sections as `no-ledger` and does not
show the bucket at all. It evidences the absent-default behaviour in §1, not
the input-drift demonstration. "Those runs use `--inputs-overlay`" holds for
the three overlay files only.

### 3. R17-CMD-BIND: the narrower claim

The input-keyed rule binds credit to the recorded **inputs**. It does not bind
trace **argv** to the bucket's declared or required commands.

- Bound: each trace receipt's `inputs` must be covered by the entry's recorded
  `inputs` with a matching sha256 (`trace-input-unrecorded:`,
  `trace-input-drift:`; `measure.py:403-412`). An entry with
  `commands_executed_count > 0` needs at least one committed receipt in strict
  mode (`measure.py:368-380`).
- Not bound: `measure.py` never reads a receipt's `argv`. The only receipt-argv
  reference is the selftest fixture at `measure.py:773`. It also never reads
  `coldread/bucket-commands.json` (zero references at 183f87b). For example,
  `coldread/traces/CR01/1.json` records a `git -C … show <rev>:SKILL.md |
  sha256sum` argv, and nothing compares that argv with the bucket's declared
  commands.

So the rule shows that a recorded read ran against the recorded bytes. It is
not a command-coverage proof, and it does not show that the declared commands
ran. The §4 limit "A seat can still skip a command" is the operative statement.
