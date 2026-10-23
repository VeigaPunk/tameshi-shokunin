# CriticCounter — round 33, wave 1

**Verdict: the two digest assumptions hold, but the shared sandbox assumption is false at freeze `f6d8a891f1d966c5c3cdda385090da3a6e804675`.** The scoring helper does not invoke bubblewrap, and the separate witness sandbox cannot launch its runtime. These are fixable counter defects, not evidence against the pinned audit tool's detection capability. The public panel has the promised dimensions; its must-kill copies are distinguishable in their relevant tally or harness contexts. This is an assigned review, not a C1 measurement or admission judgment.

Axes: **calibration** (primary: claims must match the executed boundary), **operability** (witness execution), and **coverage** (copies versus independent defect families).

## Evidence

All commands below ran from `/fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/`. Let `R` in evidence citations denote that directory. The command driver enabled `pipefail`, saved stdout and stderr as `R/<name>.stdout` and `.stderr`, and captured the command's exit using the literal trailing `; echo $? > ...exit`. No counter `main`, default mode, controls mode, or audit scoring run was invoked. The probes import the frozen round-32 definitions and AST-select only the named frozen round-33 helper definitions (`R/probe.py:21-37`). No lane content was edited or copied into a probe payload.

### 1. Both requested pins match the named commit

Exact commands:

```sh
timeout 20s git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f6d8a891f1d966c5c3cdda385090da3a6e804675:tools/mutate-and-run.sh | sha256sum; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/runner-pin.exit
timeout 20s git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f6d8a891f1d966c5c3cdda385090da3a6e804675:tools/tally-audit-v2.py | sha256sum; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/tool-pin.exit
```

Observed (`R/runner-pin.stdout:1`, `R/tool-pin.stdout:1`; both receipt exits `0`):

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  -
9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4  -
```

These match `contract.json:7,10`. No pin discrepancy found.

### 2. The actual scoring path has no filesystem sandbox

Frozen source: `R/freeze-v33.stdout:38-42,188-199,338-342` imports and calls the round-32 `v1.run_tool`. Its implementation at `R/freeze-v1.stdout:177-196` launches `[sys.executable, '-I', tool, '--runner', copy]` directly, with a changed working directory/environment and a 600-second subprocess timeout. It contains none of the stated bubblewrap flags.

Exact commands:

```sh
timeout 20s python3 -B probe.py structure; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/structure.exit
timeout 20s python3 -B probe.py visibility; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/visibility.exit
```

Observed (`R/structure.stdout:1-12`, `R/visibility.stdout:1-2`; both exits `0`):

```text
freeze-v1.stdout:177 function=run_tool bwrap_literal=0 subprocess_calls=1
  line=183 call=subprocess.run([sys.executable, '-I', tool, '--runner', copy], cwd=d, env=env,
                           capture_output=True, timeout=600)
run_tool_result=('OTHER', 2, 'TALLY_AUDIT: SETUP (visibility-only probe sentinel=SEAT_OWNED_SENTINEL lane_sources_exists=1 lane_sources_readable=1)')
probe_reads_only_seat_owned_sentinel=1 lane_content_read=0
```

**Counterexample:** the helper's child read a seat-owned sentinel outside its assigned work directory. It could also see and report read-access metadata for the lane's `corpus/SOURCES.md`; the probe did not read that file's contents. The probe returns SETUP deliberately and is not scored as a control (`R/visibility-probe.py:1-14`, `R/probe.py:60-66`). Python `-I` is not a filesystem boundary.

The claim that audit-only mode never executes copy-derived code also needs qualification: it does not launch the complete copy, but it executes the extracted tally and harness as Bash. See `R/freeze-tool.stdout:219-229,421-434`; the structure command observes direct Bash subprocess calls at lines 213 and 434. Therefore absence of a whole-copy launch does not make runner-derived sections inert.

### 3. Bubblewrap exists, but the witness sandbox cannot execute `timeout`

Exact commands:

```sh
timeout 10s bwrap --version; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/bwrap-version.exit
timeout 30s python3 -B probe.py block-witness; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/block-witness.exit
```

Observed version: `bubblewrap 0.13.1`, exit `0` (`R/bwrap-version.stdout:1`).

The witness probe executes the frozen `ho_witness_ok`/`block_run`, preserving its subprocess arguments and recording stderr; it compares pristine against the already-public T08 copy at vector `4 0 0 0 0 0 0 0 0`. It authors no held-out case. Exact first child command observed (`R/block-witness.stdout:1`):

```sh
bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/block-witness-work/w-f7766d4e226e/run.sh /x.sh --bind /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/block-witness-work/w-f7766d4e226e /w --chdir /w --dev /dev --proc /proc timeout 60 bash /x.sh
```

Both child invocations produced the following; the outer probe exited `0` (`R/block-witness.stdout:2-5`):

```text
block_subprocess_rc=1 stdout='' stderr='bwrap: execvp timeout: No such file or directory\n'
known_public_T08_witness=(False, 'vector') subprocess_count=2
```

**Counterexample:** a valid, known public tally difference is rejected as an invalid vector witness because neither tally executes. Independent execution of the same trusted public blocks confirms the difference (`R/public-semantics.stdout:1`): pristine gives exit `2`, `REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)`; T08 gives exit `0`, `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`.

Cause: `R/freeze-v33.stdout:157-160` mounts the script, work directory, devices and proc, but no runtime executables or loader/libraries. `ho_witness_ok` compares the two resulting `(rc, first-line)` tuples without distinguishing infrastructure failure (`R/freeze-v33.stdout:171-183`).

No successful namespace escape or descendant survival is asserted. Under these exact flags no tally starts, so isolation and timeout behavior of a running mutant cannot be established. The unsandboxed scoring path is a separate demonstrated boundary failure; the presence of flags in the witness-only path does not protect it.

### 4. Public panel dimensions hold; equivalence requires the correct context

Frozen generator locations: `R/freeze-v1.stdout:82-168`; the round-33 adapter is at `R/freeze-v33.stdout:209-218`.

Exact commands:

```sh
timeout 20s python3 -B probe.py panel; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/panel.exit
timeout 150s python3 -B public-semantics.py; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/public-semantics.exit
```

Observed (both exits `0`; `R/panel.stdout:1-36`, `R/public-semantics.stdout:1-19`):

```text
family_group=frozen-kill count=9
family_group=generated-kill count=9
family_group=frozen-accept count=6
family_group=generated-accept count=2
v33_public_panel_matches_frozen_generators=1 seed_string='33'
kill_total=18 accept_total=8 kill_identical_to_pristine=0 accept_identical_to_pristine=1
distinct_kill_bodies=16 distinct_accept_bodies=8
duplicate_body_groups=[['N02', 'gN02(or)'], ['N03', 'gN03(or)']]
PUBLIC_KILL_SEMANTIC_WITNESSES=18/18 seed_string=33
```

Nine kill families, each frozen plus generated: T08, N05, H03, H04, H05, N01, N02, N03, D01. Accept controls: pristine, equivalent T07 guard, reversed operands, decoy comments, cosmetic tally, renamed harness variable, generated operand permutation, generated nonce comments.

The semantic probe checks trusted public snippets, not the frozen audit tool. For tally families it directly compares the extracted blocks; for harness families it injects a bounded known-incorrect tally into the extracted harness and records `(cases, failed)`. Details: `R/public-semantics.py:39-67,73-130`.

Representative observed distinctions:

- T08: status 4 changes SETUP/exit 2 to PASS/exit 0.
- N05: a ten-operand overcount stress changes SETUP/count 10 to PASS/passed 10.
- D01: failure at the omitted leg changes FAIL/exit 1 to PASS/exit 0.
- H03, H04, N03: an incorrect count-field label yields pristine harness `(9, 7)` versus mutant `(9, 0)`.
- H05: an ignored single leg yields `(9, 2)` versus `(9, 0)`.
- N01: behavior incorrect only at the removed vector yields `(9, 1)` versus `(8, 0)`.
- N02: an absent undercount guard yields `(9, 1)` versus `(9, 0)`.

All generated copies in this replay likewise have a distinguishing context. This is not a universal equivalence proof over every seed. Nor are there eighteen independent defect families: two generated bodies duplicate frozen bodies in this replay. That duplication does not violate the frozen 18-copy predicate, but claiming eighteen independent families would overstate coverage.

Literally claiming that none of all 26 copies is trivially equivalent to pristine would be false: B0 is pristine, and the accept controls intentionally preserve behavior. The twelve harness-weakening kill copies also need a faulty-tally context to distinguish their checking power; a normal regression invocation alone is not such evidence. No public-panel defect requiring a rule change was found here.

### Frozen-source command receipts

These commands supplied every frozen source cited above. Each exited `0`; stdout is retained under the corresponding name, rather than using changing lane worktree bytes:

```sh
timeout 20s git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f6d8a891f1d966c5c3cdda385090da3a6e804675:.ufo/evidence/round-32/c1-measure.py; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/freeze-v1.exit
timeout 20s git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f6d8a891f1d966c5c3cdda385090da3a6e804675:.ufo/evidence/round-33/c1/c1-measure.py; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/freeze-v33.exit
timeout 20s git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f6d8a891f1d966c5c3cdda385090da3a6e804675:tools/mutate-and-run.sh; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/freeze-runner.exit
timeout 20s git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f6d8a891f1d966c5c3cdda385090da3a6e804675:tools/tally-audit-v2.py; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/freeze-tool.exit
```

### Scope and cleanup receipts

```sh
df -h /fast; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/disk.exit
timeout 10s python3 -B process-audit.py; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/CriticCounter/process-audit.exit
```

Both exited `0`. Disk showed `46G` available. Final owned-process audit showed `seat_nonancestor_process_count=0` and `signals_sent=0` (`R/process-audit.stdout:1-2`). No tools were installed or updated. No git writes, jj commands, seat spawns, lane counter measurements, malicious escape payloads, or production changes were made. Only this report and own scratch files were written.

## Smallest safe correction

1. Repair the **new round-33 counter's** execution boundary so both scoring and vector witnesses actually use the intended sandbox. Supply the minimal read-only runtime closure and an explicit in-sandbox executable path, while exposing only the intended tool/copy and own writable work area. Do not bind the lane or host root to make the command start.
2. Treat a sandbox startup failure as counter SETUP, not as two equal tally results or an invalid held-out witness. Before data, use a benign executable smoke probe and a known public differing vector to establish that the boundary both launches and distinguishes behavior. Then check bounded descendant cleanup under the chosen timeout boundary; the present evidence does not establish that property.
3. Do not silently repair the imported round-32 helper in place. The round-33 receipt checks its own counter bytes (`R/freeze-v33.stdout:278-288`), while execution comes from an unpinned imported helper (`:38-42`). [INFERENCE] changing that helper can change scoring without changing the recorded round-33 counter digest. Keep the corrected execution code in the newly frozen round-33 artifact, or explicitly pin its dependency.
4. Any execution-rule correction requires a disclosed new pre-data freeze and fresh controls receipt. Do not change the pinned runner or tool, relabel the panel, or amend a rule after its data seats have scored. If that boundary has already been crossed, preserve this finding for the next claim rather than repairing the result retroactively.

The sandbox defects are fixable; abandoning isolation to obtain a runnable counter would trade away calibration and is not a safe correction. Pins and intended equivalence controls require no correction.
