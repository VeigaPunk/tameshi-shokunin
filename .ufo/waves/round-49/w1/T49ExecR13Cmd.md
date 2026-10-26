# T49ExecR13Cmd — re-execution of the round-13 recipe at base (C1 command re-execution)

Item: re-run `## Pin disposition and provenance correction — round 13` (SKILL.md base `1517-1562`) steps 2 and 3 plus both tools' `--selftest`, in a scratch clone at `8ca67421111fa354b47b803358391d0b07fc6db9`, and compare every outcome with the section and its decision table (`SKILL.md:1526-1530`). Deliverable: `.ufo/waves/round-49/w1/T49ExecR13Cmd.json`, receipts in `.ufo/waves/round-49/w1/T49ExecR13Cmd/`.

Lane checkout was only read. Lane HEAD observed `455b2cd66fd9f237146a5355ca8bbc84f3071c50`; base and HEAD carry byte-identical `SKILL.md`, `tools/pin-disposition.py`, `tools/witness-metadata.py` and the three round-13 evidence files (`git rev-parse 8ca67421:<path>` vs `HEAD:<path>`), so the clone reading and the lane reading are the same inputs.

## Method

```
S=/fast/scratch/hyaku/tameshi-r49/T49ExecR13Cmd
git clone --shared --no-checkout --quiet /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/base-clone"
git -C "$S/base-clone" checkout -q 8ca67421111fa354b47b803358391d0b07fc6db9
git -C "$S/base-clone" rev-parse --show-toplevel   # = $S/base-clone
git -C "$S/base-clone" rev-parse HEAD              # = 8ca67421...
```

Toplevel asserted before any work; `git -C "$S/base-clone" status --porcelain` printed 0 lines after every run. Scratch removed at the end.

## Pre-flight: step 2 executes no sibling gate (required before running)

Confirmed from source at base before invoking, as `SKILL.md:1537` claims:

- `tools/pin-disposition.py` has exactly three `subprocess.run` sites: `:227` inside `git_run` (`:224-241`, argv list, no shell), and `:770` + `:931`, both inside `def selftest()` (`:704-:1330`, ending at `return 0`; `parse_argv` starts `:1336`). Nothing on the `run_mode` path (`:667`, dispatched from `main` at `:1371-1387`) spawns anything but git.
- The git plumbing used is read-only only: `rev-parse --show-toplevel` `:265`, `rev-parse --verify ...^{commit}` `:288` and `:391`, `cat-file -t` `:298`/`:429`, `cat-file blob` `:306`/`:441`, `symbolic-ref` `:334`/`:341`, `show-ref` `:352`, `for-each-ref` `:360`. No `status`, `diff`, `hash-object`, no hooks/index.
- Every write site (`os.makedirs` `:722,:754,:755,:803,:811,:824,:887,:1159,:1282`, `open(...,"w")` `:891,:926`, `os.remove` `:832,:1182,:1205,:1226`, `shutil.rmtree` `:1328`) sits inside `selftest()`; `run_mode` writes nothing.
- `tools/witness-metadata.py`: `--check` writes nothing; `_prepare_fixture` (`:958`) is called only from `selftest` (`:1129`), and its one `subprocess.run` (`:1133`) re-enters the tool inside the selftest fixture tree.

Independent no-write check: all six sibling targets and the four round-13 evidence inputs keep pre-session mtimes (`T49ExecR13Cmd/sibling-sha256-independent.txt`; e.g. `kumitate-shokunin/scripts/kimi-census.mjs` mtime 2026-10-23 07:02:39, `kagi-shokunin/corpus/checklist-run.sh` 2026-10-13 16:51:07, `tameshi-shokunin/.ufo/evidence/round-13/witness-metadata.json` 2026-10-20 01:51:51).

## Executions

Run from `$S/base-clone` with `TMPDIR=$S/tmp`, against the real fleet root for step 2 as the recipe writes it.

| # | argv | exit | observed | matches section |
|---|---|---|---|---|
| 1 | `python3 tools/pin-disposition.py --selftest` | 0 | 19 cases, `SELFTEST: PASS (19/19)` | yes (`SKILL.md:1552` "selftest 1 failed") |
| 2 | `python3 tools/witness-metadata.py --selftest` | 0 | 39 cases, `SELFTEST: PASS 39/39`, no `FROZEN_MUTATED` | yes (`SKILL.md:1553`; count identical to round 13) |
| 3 | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | 0 | 6 legs, `unchanged=1 changed=5 unavailable=0`, every row `result_reuse=not_established`, every row a 40-hex branch tip, `observed_at=2026-10-26T20:33:24Z` | yes (`SKILL.md:1526,1527,1529`; row at `1528` unexercised) |
| 4 | `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` | 0 | `metadata_consistent reason=ok`, `inputs=summary,declaration,declared,rerun_summary` | yes (`SKILL.md:1553` exit-0 arm) |
| 5 | same as 4 plus `--lane-root /home/vgpnk/Projects/shokunin/tameshi-shokunin` | 0 | `metadata_consistent reason=ok` on the live lane | yes — the pass is not a clone artifact |
| 6 | `python3 tools/pin-disposition.py --manifest /nonexistent/manifest.json --root /home/vgpnk/Projects/shokunin` | 2 | `status=invalid_input kind=invalid_manifest`, JSON error doc on stdout | yes (`SKILL.md:1552` exit-2 arm, live) |
| 7 | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /nonexistent-root` | 2 | `status=invalid_input` | yes (`SKILL.md:1552`) |
| 8 | `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata-old-null.json` | 1 | `metadata_inconsistent reason=normalized_kind_null` | yes (`SKILL.md:1530,1544-1547,1553`; `.ufo/evidence/round-13/expected.json` `metadata_old_null`) |
| 9 | repeat of 3 after 130 s | 0 | identical six statuses and worktree digests; only `observed_at` moved to `2026-10-26T20:35:34Z` | yes — repeatable dated reading |

Receipts: `T49ExecR13Cmd/step2-pin-disposition.out`, `step2-rerun.out`, `step3-witness-check.out`, `step3-lane-root.out`, `pin-disposition-selftest.out`, `witness-metadata-selftest.out`, `probe-invalid-manifest.out`, `probe-invalid-root.out`, `step4-oldnull-check.out`, `base-clone-identity.txt`, `sibling-sha256-independent.txt` (digests of all in `T49ExecR13Cmd.json` → `receipts_sha256`).

## Decision-table comparison (`SKILL.md:1526-1530`)

- Row `1526` (target bytes equal worktree → `unchanged`): exercised once, `bash-checklist-run`, worktree sha256 `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf` = manifest `expected_sha256` (`T49ExecR13Cmd/sibling-sha256-independent.txt`; `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`). Limit column ("mode, dependencies, environment, runner/spec and invocation identity remain unmeasured") matches the emitted `not_compared` list: `mode/exec-bit`, `runner version and embedded defect specs`, `suite command and test harness`, `interpreter and toolchain versions`, `environment variables`, `dependency versions`, `fixture and companion files`, `timeouts`.
- Row `1527` (verified pin differs → `changed`): five legs; all five carry `pinned.status=verified` and a differing worktree digest, so "readable verified pin" is satisfied for each.
- Row `1528` (`unavailable`, never borrow the enclosing repo): not exercised live (`unavailable=0`), but the arm exists and is proven in selftest cases `missing-repo`, `missing-pinned-blob`, `missing-pinned-commit`, `foreign-repo-toplevel`, `worktree-outside-repo` (`T49ExecR13Cmd/pin-disposition-selftest.out`).
- Row `1529` (`result_reuse=not_established`): holds on all six rows and at document level, with the stated reason string.
- Row `1530` (null kind → checked normalized companion): `step4-oldnull-check.out` rejects the un-normalized companion (`normalized_kind_null`) while `step3-witness-check.out` accepts the normalized one.
- Step 2's "retain stdout with its sibling branch-tip commits" (`SKILL.md:1536-1537`): all six rows carry `head.branch` (`master`) and a 40-hex `head.commit`.
- Step 3's "digest-anchored frozen sources" (`SKILL.md:1538-1539`): the check verifies its own literal pins against the four inputs and reports `inputs_verified`; `tools/witness-metadata.py:1-45` documents that a companion carrying its own digests alone would be self-certifying, which is why the digests are in the tool.

## Mismatches

**M1 — live count drift, covered by the table (no text to fix).** Round 13 recorded `unchanged3/changed3/unavailable0` (`corpus/lessons/round-13.md:89`, `.ufo/evidence/round-13/pin-dispositions.json` `counts`); today is `unchanged1/changed5/unavailable0`. Two legs flipped, reproduced outside the tool with `sha256sum` at the fleet root: `kagi-shokunin/corpus/surface-census.sh` pin `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` → worktree `1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d`, and `kumitate-shokunin/scripts/claims-check.mjs` pin `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b` → `de3433b5465a2f2d22c538537e3f9c67e37dc2605888b2ff77adc49264abfe14` (`T49ExecR13Cmd/sibling-sha256-independent.txt`, `step2-pin-disposition.out`). Decision-table row `SKILL.md:1527` is exactly the rule for this ("never transfer an old rate"), and the section quotes no count, so no correction is implied — I record it so the C1 pass does not read the new numbers as a defect.

**M2 — stale literal in `.ufo/evidence/round-13/expected.json`, not in the section.** `expected_checks.pin_selftest.contains` is `SELFTEST: PASS (18/18)` and `inputs["tools/pin-disposition.py"]` is `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11`; the base bytes are `331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c` and print `SELFTEST: PASS (19/19)` (`T49ExecR13Cmd/pin-disposition-selftest.out`, `T49ExecR13Cmd/base-clone-identity.txt`). A live re-evaluation of that row would fail. The section itself is consistent: `SKILL.md:1552` pins "literal selftest labels **in tool**" instead of a count, and `SKILL.md:1556-1557` states no old evidence hash is regenerated. The row is also receipt-anchored, not live: `.ufo/evidence/round-14/dispositions.json` marks `pin_selftest` `effective` with `receipt: .ufo/evidence/round-13/verification.json`. The 18→19 delta is already in prose at `corpus/knowledge/executable-self-assessment.md:57`. Severity low; the only actionable question for the L1 is whether row `1552` should name the successor count, and that is a calibration decision, not mine to make.

**M3 — wording gloss.** `SKILL.md:1553` maps exit 0 to "metadata_consistent/clean"; the tool never prints `clean` (`grep -n clean tools/witness-metadata.py` → no match). The exit-0 output is `metadata_consistent reason=ok` (`T49ExecR13Cmd/step3-witness-check.out`). This is the same gloss style as row `1552`'s "changed/unavailable"; behaviour matches the map exactly.

**M4 — confirmations, not mismatches.** `SKILL.md:1537` ("It executes no sibling gate") holds per the source audit above; `SKILL.md:1536-1537` (branch tips) holds; `SKILL.md:1544-1547` (companion normalizes the canonical summary, rerun null outside scope, old-null rejected) holds (`T49ExecR13Cmd/step4-oldnull-check.out`); `SKILL.md:1553` exit-1 and exit-2 arms both reproduce live (rows 8, 6, 7).

## Notes for the C1 integration

- The tool banner at base is `pin-disposition.py r17 (tameshi-shokunin, 2026-10-20)` (`step2-pin-disposition.out`), i.e. four revisions after the `r13` that round 13 ran; the recipe still reproduces because the section cites the command and the manifest, never the tool revision. Any future re-read should keep it that way.
- `SKILL.md:1535` command text and the registry row `1552` command text are identical, so one re-execution covers both pointers; both point at `.ufo/evidence/round-13/pin-manifest.json` (sha256 `64eaa43e...`, matching `expected.json`).
- No tool was installed or upgraded for this seat; no model was passed; no counter (`measure.py`) was invoked.

## Summary

1. Both recipe commands reproduce at base `8ca67421` with exit 0 and both `--selftest` modes pass (19/19, 39/39).
2. Step 2 emits `unchanged=1 changed=5 unavailable=0` and `result_reuse=not_established` on every row, with branch tips retained: decision-table rows `1526`, `1527`, `1529` exercised, `1528` only in selftest.
3. Step 3 returns `metadata_consistent reason=ok`, also against the live lane root, so the pass is not a clone artifact.
4. Step 4's un-normalized-companion rejection reproduces at exit 1 `normalized_kind_null`; both exit-2 arms of step 2 reproduce live.
5. M1: two legs flipped `unchanged → changed` since round 13 — predicted by row `1527`, no section text implicated; digests reproduced externally.
6. M2: `.ufo/evidence/round-13/expected.json`'s `18/18` and `297253971d…` are stale versus base bytes `19/19` and `331529ead…`; the section defers to the tool's literals and `SKILL.md:1556-1557`, so only a live re-evaluation of that row would fail.
7. M3: row `1553`'s word "clean" is a gloss; the tool's exit-0 token is `metadata_consistent reason=ok`.
8. Side-effect proof: source audit shows no sibling gate and no write path outside `selftest()`; clone `status --porcelain` empty and all target mtimes pre-session; scratch deleted.
