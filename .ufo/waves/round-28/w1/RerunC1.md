# RerunC1 — round 28, wave 1, claim C1 (calibration)

Seat: TameshiR28.RerunC1 (executor, leaf; no subagent dispatched).
All code ran in private clones under `/tmp`: `/tmp/tameshiR28RerunC1-r28`
(detached at `b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a`),
`/tmp/tameshiR28RerunC1-base` (detached at
`06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c`), and two scratch probes
`/tmp/tameshiR28RerunC1-probe1`, `/tmp/tameshiR28RerunC1-probe2`.
No `jj` command was run anywhere. In the lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin` only read-only git was used
(`GIT_OPTIONAL_LOCKS=0 git rev-parse / show / diff / log`); no gate, selftest
or sweep was run there. No tool was installed or upgraded (none needed;
`python3` and `git` were sufficient).

## Verdict

**Base leg of C1: confirmed exactly. Target leg: NOT met at the landed head —
the registered target is a projection, not a measurement, and must not be
reported as one.**

1. Base `06b59b93` reads `covered=60/64 restraint=6 box3_mismatch=1
   depth_score=9`, exit 1 — byte-for-byte the value C1 registers.
2. The counter is byte-identical at the two revisions. `git diff` over the
   three counter files is empty; all three blobs have the same sha256 at both
   revisions. The counter did not move, so every delta below is repo state,
   not instrument drift.
3. The landed head `b05d2ee` reads `covered=50/64 restraint=6
   box3_mismatch=1 depth_score=9`, exit 1 — **not** the registered target
   `covered=64/64 restraint=8 box3_mismatch=0 (exit 0)`. Fourteen sections
   are uncovered there. C1's target leg is reachable only after this wave's
   fresh reads and their ledger append land at the final head; until then it
   is a target, and `corpus/lessons/round-28.md` (which states it as
   "target at the landed head") must keep that anchor honest by naming the
   base alongside it.
4. Root cause of the ten lost credits, isolated by two probes: **only
   `corpus/SOURCES.md` changed between the two revisions**
   (blob `6aa0dc84…` → `e38bb0c8…`); reverting it alone at `b05d2ee`
   restores `covered=60/64`. The `SKILL.md` edit is not the cause of the
   count loss, but it changes the sha of the Round-21 section
   (`2833c0bc…` → `16a5965b…`), which orphans that section's gap-blocking
   ledger entry and converts its monitor reason from `verdict:gap-blocking`
   to `no-ledger-entry`. The Round-21 blocking gap is therefore still open;
   the edit only made it unread.
5. The three exit-0 conditions are one condition. `c1-measure.py:54` exits 0
   only when `covered == total and restraint == 8 and mismatch == 0`;
   `restraint` reaches 8 only via `box3_points`, which requires
   `box3_full_page`, i.e. `sections_covered == sections_total`
   (`.ufo/evidence/round-18/measure.py:682-707`). So exit 0 ⟺ all 64
   sections credited at the measured revision.

## Evidence

### Counter runs (exact commands, observed output, observed exit)

Target, worktree detached at the content revision:

```
$ cd /tmp/tameshiR28RerunC1-r28
$ python3 .ufo/evidence/round-27/c1-measure.py --repo /tmp/tameshiR28RerunC1-r28 --rev b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a
C1_MONITOR: covered=50/64 restraint=6 box3_mismatch=1 depth_score=9 rev=b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a
  uncovered: ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
  uncovered: ### The report shape — what the opting-in lane receives
  uncovered: ## The leg ledger — replay, receipt, and how it is read (round 7, measured)
  uncovered: ### Triggers T1–T3 and the re-pin rule
  uncovered: ## Repeated controls and gate registry — round 12
  uncovered: ### Gate/probe registry
  uncovered: ## Pin disposition and provenance correction — round 13
  uncovered: ### Round-13 gate/probe registry
  uncovered: ## Effective expectation reconciliation — round 14
  uncovered: ## Context gate classification and explicit exit classes — round 15
  uncovered: ## Live-tree re-pin and entry-command monitor — round 17
  uncovered: ### Round-18 gate/probe registry — routed-defect closure
  uncovered: ### Round-20 gate/probe registry — frozen receipt instruments
  uncovered: ### Round-21 gate/probe registry — finite environment differential
$ echo $?
1
```

Base, separate clone detached at the base revision:

```
$ cd /tmp/tameshiR28RerunC1-base
$ python3 .ufo/evidence/round-27/c1-measure.py --repo /tmp/tameshiR28RerunC1-base --rev 06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c
C1_MONITOR: covered=60/64 restraint=6 box3_mismatch=1 depth_score=9 rev=06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c
  uncovered: ### The report shape — what the opting-in lane receives
  uncovered: ### Triggers T1–T3 and the re-pin rule
  uncovered: ### Gate/probe registry
  uncovered: ### Round-21 gate/probe registry — finite environment differential
$ echo $?
1
```

Both values reproduced on repeat runs (identical bytes out, identical exits).
The base value also matches the lane's own retained receipt
`.ufo/evidence/round-28/append-probe.txt` (`base:` line) and the lane's own
explain capture `.ufo/waves/round-28/monitor-b05d2ee-explain.json`
(`sections_covered=50`, `calibration_restraint_score=6`, 14 uncovered).

The counter is rev-pinned, not worktree-pinned: with the worktree checked
out at the content revision and `--rev` pointing at the base, it still
reported the base numbers (`covered=60/64`, exit 1).

### Counter file byte-identity

```
$ git -C /tmp/tameshiR28RerunC1-r28 diff 06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a -- .ufo/evidence/round-27/c1-measure.py .ufo/evidence/round-21/coldread/measure.py .ufo/evidence/round-18/measure.py
(empty output; exit 0)
```

Blob ids at both revisions (identical per file):

| File | blob id (both revs) | sha256 of the blob (both revs) |
|---|---|---|
| `.ufo/evidence/round-27/c1-measure.py` | `f8e125a486842d80d3801fe2395802fcb052905c` | `6f95ef1d0624e4da2130168e56be65f678a203fcefe7afca9cfad592b47670a8` |
| `.ufo/evidence/round-21/coldread/measure.py` | `9eb05868558224a1aaec3054de47feaf7219225a` | `657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb` |
| `.ufo/evidence/round-18/measure.py` | `9643f7032ae6fde843464d4ef6bc0c5919518528` | `7ca87a7c98196d87e86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37` |

### Uncovered headings at `b05d2ee` with monitor reasons

From
`python3 .ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev
b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a --explain` (strict, no override;
`trace_gate=strict`, `overrides_used=false`, `ledger_source=rev`,
`ledger_committed=true`, `depth_score=9`).

| SKILL.md line | Heading | Monitor reason |
|---|---|---|
| 131 | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | `input-drift:corpus/SOURCES.md` |
| 883 | `### The report shape — what the opting-in lane receives` | `no-ledger-entry` |
| 921 | `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | `input-drift:corpus/SOURCES.md` |
| 1069 | `### Triggers T1–T3 and the re-pin rule` | `no-ledger-entry` |
| 1479 | `## Repeated controls and gate registry — round 12` | `input-drift:corpus/SOURCES.md` (+ `tools/mutate-and-run.sh`, `tools/trace-inputs.py`) |
| 1499 | `### Gate/probe registry` | `no-ledger-entry` |
| 1517 | `## Pin disposition and provenance correction — round 13` | `input-drift:corpus/SOURCES.md` (+ round-17 coldread files, `corpus/knowledge/incremental-pin-disposition.md`, `tools/bash-witness-study.py`, `tools/mutate-and-run.sh`) |
| 1548 | `### Round-13 gate/probe registry` | `input-drift:corpus/SOURCES.md` (+ `tools/bash-witness-study.py`, `tools/mutate-and-run.sh`) |
| 1563 | `## Effective expectation reconciliation — round 14` | `input-drift:corpus/SOURCES.md` (+ `tools/bash-witness-study.py`, `tools/evidence-disposition.py`, `tools/mutate-and-run.sh`) |
| 1609 | `## Context gate classification and explicit exit classes — round 15` | `input-drift:corpus/SOURCES.md` (+ `tools/bash-witness-study.py`, `tools/evidence-disposition.py`, `tools/mutate-and-run.sh`, `tools/registry.json`) |
| 1814 | `## Live-tree re-pin and entry-command monitor — round 17` | `input-drift:corpus/SOURCES.md` |
| 1925 | `### Round-18 gate/probe registry — routed-defect closure` | `input-drift:corpus/SOURCES.md` (+ `tools/registry-check.py`, `tools/registry.json`) |
| 1938 | `### Round-20 gate/probe registry — frozen receipt instruments` | `input-drift:corpus/SOURCES.md` (+ `corpus/QUALITY.md`, `tools/registry.json`) |
| 1964 | `### Round-21 gate/probe registry — finite environment differential` | `no-ledger-entry` |

Reason histogram at `b05d2ee`: `credited` 50, `no-ledger-entry` 4,
`input-drift:*` 10, vetoed sections 0.
Reason histogram at base: `credited` 60, `no-ledger-entry` 3,
`verdict:gap-blocking` 1, vetoed sections 1 (the Round-21 section).

The ten drifted sections all list `corpus/SOURCES.md` among their drifted
inputs, matching the wave context's "10 credited sections drifted".

### Root-cause isolation (two scratch probes, both in `/tmp`)

Only `corpus/SOURCES.md` and `SKILL.md` differ between the two revisions
(`git diff --stat`: `SKILL.md +18`, `corpus/SOURCES.md +15/-1`,
`corpus/lessons/round-28.md`, and three new `.ufo/evidence/round-28/` files).

Probe 1 — content revision with `corpus/SOURCES.md` reverted to base:

```
C1_MONITOR: covered=60/64 restraint=6 box3_mismatch=1 depth_score=9
  uncovered: ### The report shape — what the opting-in lane receives
  uncovered: ### Triggers T1–T3 and the re-pin rule
  uncovered: ### Gate/probe registry
  uncovered: ### Round-21 gate/probe registry — finite environment differential
```

Exit 1. The ten drifted sections are restored by the `corpus/SOURCES.md`
revert alone; the remaining four are the pre-existing routed remainder
(Round-21 now `no-ledger-entry` instead of `verdict:gap-blocking`, because
the `SKILL.md` edit is still present).

Probe 2 — content revision with `SKILL.md` reverted to base:

```
C1_MONITOR: covered=50/64 restraint=6 box3_mismatch=1 depth_score=9
  ... 14 uncovered, the Round-21 section reported as verdict:gap-blocking
```

Exit 1. The `SKILL.md` edit alone changes no count; it only flips the
Round-21 section's reason back to `verdict:gap-blocking`.

Mechanism, read from the frozen implementation
`.ufo/evidence/round-18/measure.py`:

- A section is credited only if the ledger holds an entry keyed to the
  sha256 of that section's body (`:612` `matches = by_sha.get(sec['sha256'])`)
  and every recorded input verifies at the measured revision
  (`:349` `fails.append('input-drift:%s' % path)`).
- The Round-21 ledger holds 354 entries; **99 of them record
  `corpus/SOURCES.md`**, so any content change to that file invalidates
  those entries' credit at the measured revision.
- Per-section entry audit at `b05d2ee` for the ten drifted sections: each had
  exactly one base-credited entry (e.g. `read_rev b1cc95e1fb62` for lines
  131 and 1814, `read_rev 2227d8338c02` for line 921) whose sole failing
  input at the content revision is `corpus/SOURCES.md`. The other listed
  inputs (`tools/mutate-and-run.sh`, `tools/registry.json`,
  `corpus/QUALITY.md`, …) were already stale at base and did not matter
  there, because a stale entry neither credits nor vetoes
  (`:528-537` `entry_is_stale`).
- Section sha for `### Round-21 gate/probe registry` moved
  `2833c0bc95623adb2b10806da6146347c70283dce8bf87db00631a6f540f7c25` →
  `16a5965b0166…`; the old sha's ledger entry (`verdict=gap-blocking`,
  `blocking_gaps=1`, `read_rev b1cc95e1fb62`, seat ReRead03) no longer
  matches any section, so the monitor reports `no-ledger-entry` instead of
  `verdict:gap-blocking`. The Round-21 blocking gap (the round-21 C1/C2
  facade reading the live lane) is untouched by the edit; it is only unread.

### Calibration reading

- C1's registered base value is exact and the instrument is stable: no
  calibration error in the counter.
- The registered target (`covered=64/64 restraint=8 box3_mismatch=0`,
  exit 0) is a *post-wave* projection. Measured today at the landed head
  it is `50/64`, exit 1. Any LOG/lesson/SCORECARD line that says "64/64" or
  "exit 0" before the wave's reads land would be a false claim; any line
  that says "14 sections repaired" measured from `b05d2ee` would overstate
  the round — ten of the fourteen are credit this round's own `SOURCES.md`
  edit removed and the wave's reads will restore. The honest delta against
  the base is **4 sections** (60 → 64), plus restraint 6 → 8 and
  `box3_mismatch` 1 → 0.
- `restraint=8` and `box3_mismatch=0` are the same event as `covered=64/64`
  (see the exit-0 derivation above); they are not independent evidence.

## Smallest safe correction (advisory — I wrote no production file)

1. **Freeze `corpus/SOURCES.md` before the fresh reads.** The S059 re-open
   row and the `Next unused id: S092` note are already in `b05d2ee`; they
   must be the last content change to that file. 99 ledger entries record
   its sha, so any further edit (a new S09x row, a `used-by` cell, a
   next-id bump) re-drifts the same sections and repeats the 60 → 50 loss
   the append probe already measured.
2. **Do not re-edit the Round-21 section of `SKILL.md` after its fresh
   read.** Its body sha is the ledger key; a second edit orphans the new
   entry exactly as the first one orphaned ReRead03's.
3. **Read at the final head, append to the ledger, then measure that same
   head.** A read recorded at an earlier revision records that revision's
   input shas and will drift at the later head.
4. **Append, do not rewrite, the ledger** (`.ufo/evidence/round-21/coldread/ledger.json`)
   so the append shows as an append in `git diff`. The ledger path itself is
   in `IGNORED_INPUTS`, so appending entries does not by itself de-credit
   anything.
5. **Fix the Round-21 gap, or state it as open.** The gap-blocking finding
   (C1/C2 facade reads the live lane, `FLEET = Path("/home/vgpnk/Projects/shokunin")`)
   is not addressed by the Round-28 correction text, which documents it. If
   a fresh read of that section returns gap-blocking again, the section
   stays vetoed and `covered` cannot reach 64/64, so the target exits 1.
   That read must be a genuine re-verification, not a reclassification.
6. **Cite the base next to the target** in `corpus/lessons/round-28.md`:
   "base `06b59b93` → `covered=60/64 restraint=6 box3_mismatch=1`; target at
   the landed head `covered=64/64 restraint=8 box3_mismatch=0` (exit 0)",
   with the base measurement reproduced as above. The target is legitimate
   only as a target.

## Files changed by this seat

- `.ufo/waves/round-28/w1/RerunC1.md` (this report; the only file written).

## Risks and blockers

- **Risk (high, ordering).** Any post-read edit to `corpus/SOURCES.md`,
  `corpus/QUALITY.md`, `tools/registry.json`, `tools/registry-check.py`,
  `tools/mutate-and-run.sh`, `tools/trace-inputs.py`,
  `tools/bash-witness-study.py`, `tools/evidence-disposition.py`,
  `corpus/knowledge/incremental-pin-disposition.md`, or
  `.ufo/evidence/round-17/coldread/*` re-drifts the fresh entries and
  silently drops `covered` again. The monitor reports the drift reason, so
  this is detectable, but only if the counter is run at the final head.
- **Risk (medium, the Round-21 section).** Its gap-blocking finding is
  still substantively open; the `SKILL.md` edit changed only its sha. If
  the fresh read confirms the gap, exit 0 is unreachable this round and the
  honest result is a partial repair with the gap named.
- **Risk (low, reporting).** Quoting `64/64` or `exit 0` before the wave's
  reads land, or quoting `50 → 64` as "14 sections repaired", would misstate
  the round in either direction.
- **Blocker.** None for this seat: the claim was reproducible, the counter
  identity was confirmed, and the uncovered set and its reasons were read
  directly from the frozen monitor. Nothing in this report depends on a
  read I did not run.
