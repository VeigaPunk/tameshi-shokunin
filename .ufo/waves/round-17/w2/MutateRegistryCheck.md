# Registry-check mutation probe — round 17, wave 2

Seat: TameshiR17.MutateRegistryCheck-2. Date: 2026-10-20.
Target: `tools/registry-check.py` at `eb7838b16490ca7ba17ea3242ade76a61f744af2`.
All source references below are to that revision, not the moving lane worktree.

## Axes and scope

- **Depth:** minimally change each named behavior-bearing point and exercise the actual CLI selftest.
- **Calibration:** distinguish a killed mutant from a surviving mutant and an inconclusive baseline; independently demonstrate that survivors change the declared behavior.
- **Safety:** independent fleet-mirror clones, bounded foreground executions, read-only live trees, and exact source restoration.

**Observed result: 7 killed, 2 survived, 0 inconclusive.** Nine pristine and nine restored invocations each exited 0 with `SELFTEST: PASS (34 cases)`. Nine mutated invocations produced the outcomes below: **27 selftest invocations total**. Two supplementary behavioral witnesses were also run on pristine, mutated, and restored bytes: **6 witness invocations**. These witnesses expose both survivors; they do not retroactively count as selftest kills.

This probe evaluates the monitor's fixture sensitivity. It does not adjudicate the round, C1 cold-read credit, or the full C2 baseline-registry comparison.

## Isolation and commands

Recorded scratch root:

```sh
W=/tmp/tameshi-r17w2-MutateRegistryCheck-umm2zrgx
REV=eb7838b16490ca7ba17ea3242ade76a61f744af2
```

The initial clone was `$W/fleet/tameshi-shokunin`; each mutant used its own `$W/M01/fleet/tameshi-shokunin` through `$W/M09/fleet/tameshi-shokunin`. Each fleet directory contained the required read-only sibling symlinks. The initial source clone and all nine mutant clones were checked out detached at `$REV`; all clone/checkout commands exited 0. Actual clone commands were `git clone -q SOURCE DESTINATION` and `git -C DESTINATION checkout -q --detach "$REV"`, executed by Python subprocesses. The initial source was `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; subsequent sources were the initial scratch clone. No git write was run in a live repository.

For each ID, set `C="$W/$ID/fleet/tameshi-shokunin"`. The following is the exact detector argument vector expressed using those recorded absolute-path variables; it was executed unchanged at the pristine, mutated, and restored stages:

```sh
/usr/bin/bwrap --unshare-all --die-with-parent --new-session \
  --ro-bind / / --dev /dev --proc /proc \
  --bind "$W/selftest-tmp" /tmp --bind "$W" "$W" \
  --chdir "$C" \
  /usr/bin/timeout --signal=TERM --kill-after=5s 90s \
  /usr/bin/python3 "$C/tools/registry-check.py" --selftest
```

Execution used a copied environment with inherited `GIT_*` entries removed; nothing was exported into a shared shell. The selftest itself deliberately injects its decoy git variables. Bubblewrap made the live filesystem read-only, kept target-created `/tmp` fixtures physically under `$W/selftest-tmp`, and isolated descendant PIDs. The sandbox setup probe `/usr/bin/true` exited 0. Independent clones ran concurrently through an awaited foreground thread pool; there were no background jobs or dispatches. No detector hit its outer timeout; all selftest stderr streams were empty. The process-group mutant took 22.877 seconds; its 20-second grandchild witness completed rather than being truncated by the outer bound.

## Kill table

P/M/R means pristine / mutated / restored process exit. Every P and R printed `SELFTEST: PASS (34 cases)`.

| ID | Mutation at `tools/registry-check.py` | Expected detector(s), with fixture location | P/M/R | Selftest verdict |
|---|---|---|---|---|
| M01 | `:542`: count all recognized statuses by replacing `f["status"] == "active"` with `f["status"] in STATUSES`; superseded rows enter both N and M | `all-held` (`:797–817`), `superseded-runs-excluded` (`:851–870`) | 0/1/0 | killed |
| M02 | `:539`: append `if row["status"] == "active"` to the execution comprehension, skipping superseded rows | `superseded-runs-excluded` (`:851–870`) | 0/1/0 | killed |
| M03 | `:137`: replace inherited-git-variable exclusion with `if True` | `gitdir-scrub-rev` (`:714–727`), `gitdir-scrub-row` (`:729–763`) | 0/1/0 | killed |
| M04 | `:313,321`: replace both `os.killpg` calls with `os.kill`, signaling only the session leader | `timeout-kills-group` (`:765–794`) | 0/1/0 | killed |
| M05 | `:414`: replace `f"{rev}^{{commit}}"` with `"HEAD^{commit}"`, ignoring the requested revision | `rev-unknown`, `rev-path-like`, `rev-option-like` (`:1006–1020`) | 0/1/0 | killed |
| M06 | `:466`: replace checkout argv tail `"checkout", "-q", "--detach", sha` with `"reset", "-q", "--hard", sha`; retain exact HEAD verification | `rev-clone-held`, `rev-resolved-reported` (`:1022–1053`) would need to discriminate attached HEAD | 0/0/0 | **survived** |
| M07 | `:96`: weaken source revision minimum from `[0-9a-f]{7,40}` to `[0-9a-f]{1,40}` | `invalid-source` (`:983–997`) would need to discriminate short hexadecimal revisions | 0/0/0 | **survived** |
| M08 | `:397`: remove `and not missing` from the held predicate | `stdout-contains-missing` (`:835–849`) | 0/1/0 | killed |
| M09 | `:527`: replace `wanted.intersection(...)` with `wanted.issubset(...)`, changing repeatable-tag OR to AND | `tag-repeatable` (`:929–942`) | 0/1/0 | killed |

M04 changes the two signal dispatches within one cleanup behavior; all other mutants change one line. No fixture or expected value inside the target selftest was edited.

### Actual mutated output

The complete failure-line sets and final summaries were:

```text
M01
SELFTEST_CASE all-held FAIL (exit=0)
SELFTEST_CASE superseded-runs-excluded FAIL (exit=0)
SELFTEST_CASE tag-selects-any FAIL (exit=0)
SELFTEST_CASE tag-repeatable FAIL (exit=0)
SELFTEST: FAIL (4 of 34 cases: all-held, superseded-runs-excluded, tag-selects-any, tag-repeatable)

M02
SELFTEST_CASE all-held FAIL (exit=0)
SELFTEST_CASE superseded-runs-excluded FAIL (exit=0)
SELFTEST_CASE tag-selects-any FAIL (exit=0)
SELFTEST_CASE tag-repeatable FAIL (exit=0)
SELFTEST: FAIL (4 of 34 cases: all-held, superseded-runs-excluded, tag-selects-any, tag-repeatable)

M03
SELFTEST_CASE gitdir-scrub-rev FAIL (exit=2 canary_stable=True)
SELFTEST_CASE gitdir-scrub-row FAIL (exit=1 canary_stable=True)
SELFTEST: FAIL (2 of 34 cases: gitdir-scrub-rev, gitdir-scrub-row)

M04
SELFTEST_CASE timeout-kills-group FAIL (exit=1 marker=True)
SELFTEST: FAIL (1 of 34 cases: timeout-kills-group)

M05
SELFTEST_CASE rev-unknown FAIL (exit=0)
SELFTEST_CASE rev-path-like FAIL (exit=0)
SELFTEST_CASE rev-option-like FAIL (exit=0)
SELFTEST: FAIL (3 of 34 cases: rev-unknown, rev-path-like, rev-option-like)

M06
SELFTEST: PASS (34 cases)

M07
SELFTEST: PASS (34 cases)

M08
SELFTEST_CASE stdout-contains-missing FAIL (exit=0)
SELFTEST: FAIL (1 of 34 cases: stdout-contains-missing)

M09
SELFTEST_CASE tag-repeatable FAIL (exit=2)
SELFTEST: FAIL (1 of 34 cases: tag-repeatable)
```

The `exit=` inside a `SELFTEST_CASE` line is the child CLI exit, not the selftest process exit. In particular, M01/M02/M08 were killed by finding/output expectations even when the child exited 0. M03 was detected without a canary HEAD change; no canary corruption is claimed.

## Survivors: behavioral witnesses, not equivalent mutations

The following supplemental CLI commands used the identical sandbox prefix above, with the bound changed from `90s` to `30s`, and the final `--selftest` replaced by the listed arguments. Each command was run unchanged on all three byte states. No supplementary selftest or production fix was installed.

### M06 — detached checkout is not tested

The source's detached-clone promise is at `tools/registry-check.py:53–59`; implementation at `:465–485`. Its revision fixtures at `:1022–1053` verify a marker, the resolved SHA, and report fields, but not whether HEAD is symbolic. Resetting the clone's branch to the same SHA therefore passes all 34 cases.

Witness registry at `$W/M06/fleet/tameshi-shokunin/detached-witness.json`:

```json
{"schema":"tameshi-entry-registry-v1","rows":[{"name":"detached-head","kind":"probe","argv":["git","symbolic-ref","-q","HEAD"],"expect":{"exit":1},"timeout_s":5,"source":"tools/registry-check.py@eb7838b16490ca7ba17ea3242ade76a61f744af2:466","status":"active"}]}
```

Target arguments, with `C="$W/M06/fleet/tameshi-shokunin"`:

```sh
/usr/bin/python3 "$C/tools/registry-check.py" \
  --root "$C" --rev "$REV" --registry "$C/detached-witness.json"
```

Actual pristine and restored output, both exit 0, stderr empty:

```text
ROW detached-head expect=1 got=1 held
REGISTRY_CHECK: held=1/1 superseded=0
```

Actual mutated output, exit 1, stderr empty:

```text
ROW detached-head expect=1 got=0 differs
REGISTRY_CHECK: held=0/1 superseded=0
```

Thus M06 changes real clone behavior while surviving the assigned selftest. A CLI fixture requiring `git symbolic-ref -q HEAD` to exit 1 would discriminate this mutation without changing the existing contract.

### M07 — source-regex lower bound is not tested

The declared 7–40 hexadecimal revision contract is at `tools/registry-check.py:24`; regex at `:96`, validation at `:228–233`. The existing `invalid-source` case uses `SKILL.md round-17 registry pending` (`:988–989`), so it remains invalid after the lower bound is weakened.

Witness registry at `$W/M07/fleet/tameshi-shokunin/source-length-witness.json`:

```json
{"schema":"tameshi-entry-registry-v1","rows":[{"name":"short-source","kind":"probe","argv":["/usr/bin/python3","-c","print('short-rev-accepted')"],"expect":{"exit":0,"stdout_contains":["short-rev-accepted"]},"timeout_s":5,"source":"SKILL.md@a:1","status":"active"}]}
```

Target arguments, with `C="$W/M07/fleet/tameshi-shokunin"`:

```sh
/usr/bin/python3 "$C/tools/registry-check.py" \
  --root "$C" --registry "$C/source-length-witness.json"
```

Actual pristine and restored stdout, both exit 2:

```text
REGISTRY_CHECK: could-not-evaluate (registry invalid: rows[0].source must be <file>@<7-40 hex rev>:<line>, got 'SKILL.md@a:1')
```

Actual mutated stdout, exit 0:

```text
ROW short-source expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
```

All three emitted the same expected live-mode warning on stderr; the root was an isolated scratch clone:

```text
registry-check: warning: live --root mode runs rows in the lane; rows may write into the root (use --rev to grade a throwaway clone)
```

Thus M07 accepts an explicitly disallowed source while all selftests remain green. A 1–6-digit hexadecimal source fixture asserting exit 2 would discriminate the demonstrated defect; boundary-valid input should remain accepted.

## Hashes and restoration evidence

Common pristine and restored whole-file SHA-256, **B**:

```text
0bf9d1d2971c9fe478823754c7b889315585b73361ee3146631f409c4c5a3765
```

Each row was independently hashed before mutation, after mutation, after restoration, and after the restored detector. Every before/after-restoration pair equaled B. All changes were reversed by exact inverse surgical edits before the restored runs.

| ID | Before | Mutated whole-file SHA-256 | Restored and post-detector |
|---|---|---|---|
| M01 | B | `59db573f47dca4688fd04a2a6d4c6385c095f46d4087bdb946643d012c051053` | B |
| M02 | B | `be2158289aa6f6031c40ba2ff20983e1f68b541d76194d30fb102e4c554ccef0` | B |
| M03 | B | `7f2efeae5d773ae71d9a2fc693d18a7d62ed7f9cdaf4e7c39df9025f75419393` | B |
| M04 | B | `8e3922a57ce6173a0813a21c370955b6b33542013adeabd3b89ef878e4338d5f` | B |
| M05 | B | `aafce699ddc92b7ab79798bf37a9ea532dda365174a7439b58eb7f13ea2d5474` | B |
| M06 | B | `7851c012c90a18294a327311455bbae912594a263a8137eca6624881d973fdc9` | B |
| M07 | B | `14ab5837f3081989b806d7b830459e0a2d7c259d0263eb6c681a19790c8f9495` | B |
| M08 | B | `90ce177d88a5c7c64c2dad3835bbf98719e1fb334af5241eb663dccbc7bbb417` | B |
| M09 | B | `0f4ee624e819b92b3ea6556fbdbc56308d3704d226606039e92fd3eb923868b5` | B |

No tool installation or update was needed. No production code, selftest, registry, sibling repository, or lane state was changed. This report is the only live-lane write. The proposed fixture discriminators are findings for integration, not contract changes or unimplemented production work.

Verdict: **partial** — the assigned selftest kills 7/9 plausible defects, but detached-HEAD and source-revision-length defects survive; both survivors are behaviorally demonstrated, and all nine scratch sources are exactly restored.
