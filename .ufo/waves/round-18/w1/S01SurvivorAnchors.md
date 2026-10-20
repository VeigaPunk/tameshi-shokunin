# S01SurvivorAnchors — seven R17 survivor guards anchored at 183f87b

Seat: TameshiR18.S01SurvivorAnchors. Date: 2026-10-20.
Lane root `L=/home/vgpnk/Projects/shokunin/tameshi-shokunin`; base
`REV=183f87b899e6cae46be98d251cbc87fb5118f6ca`. All lane bytes were read with
`git -C "$L" show "$REV":<path>`; all execution happened in a /tmp fleet-mirror
clone (scratch `/tmp/tameshi-r18w1-S01SurvivorAnchors-CP5eDG`, `HEAD=183f87b8…`).
No lane file other than this report was written; no git write occurred in the lane
or any sibling repo; all selftests ran with `GIT_DIR`/`GIT_WORK_TREE`/
`GIT_INDEX_FILE`/`GIT_COMMON_DIR` unset and cwd inside the clone.

Sources mapped: `.ufo/waves/round-17/w2/MutateDispositionV2.md`,
`MutateRegistryCheck.md`, `MutateTraceInputs.md` (survivor rows only), routed by
`corpus/lessons/round-17-verifier-spotcheck.md:428-432` (§7 item 3).

## 0. Pinned blobs and target selector

| Path at REV | sha256 at REV | R17 landing hash | Selftest at REV |
|---|---|---|---|
| `tools/evidence-disposition.py` | `f8f05c7aa601cf0b6f0907cc1ead2fc01acaad6a3c19e81888c084a969583e27` | identical (`H0`) | `PASS (56/56)` exit 0 |
| `tools/registry-check.py` | `0bf9d1d2971c9fe478823754c7b889315585b73361ee3146631f409c4c5a3765` | identical (`B`) | `PASS (34 cases)` exit 0 |
| `.ufo/evidence/round-17/coldread/trace-inputs.py` | `521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070` | identical (`H0`) | `27/27` exit 0 |
| `tools/trace-inputs.py` | **absent** (`git cat-file -e` exit 128) | n/a | n/a |

Consequence for the probe author: at REV the trace-collector target resolves through
the contract-A fallback to `.ufo/evidence/round-17/coldread/trace-inputs.py`. The
three trace line anchors below are for that path. If a probe runs at a later rev
where `tools/trace-inputs.py` is tracked (contract B build), re-locate the anchors
by exact-string search, not by line number.

Because all three files are byte-identical to the round-17 landing, R17's line
numbers transfer unchanged; the independent count below re-verified them at REV.

## 1. Master table

`count` is the exact number of non-overlapping occurrences of the full old string
in the REV blob, computed in Python from `git show "$REV":<path>` bytes. All seven
are `count==1`, satisfying contract A's one-mutant precondition.

| Probe | Mutant (R17 report row) | File at REV | Line | count==1 | Nearest existing selftest case (line at REV) |
|---|---|---|---|---|---|
| P01 | Disposition `G3Commit` (tag-object guard) | `tools/evidence-disposition.py` | 445 | yes | `v2-historical-tree-id` (2551; setup 2013) |
| P02 | Disposition `G5Mode` (symlink-mode guard) | `tools/evidence-disposition.py` | 552 | yes | `v2-blob-bytes-crlf` (2609; setup 2068) |
| P03 | Registry `M06` (detached-checkout guard) | `tools/registry-check.py` | 466 | yes | `rev-clone-held` (1024) + `rev-resolved-reported` (1050) |
| P04 | Registry `M07` (short-rev regex) | `tools/registry-check.py` | 96 | yes | `invalid-source` (988; validation 228-233) |
| P05 | Trace `M01` (O_RDWR exclusion) | `.ufo/evidence/round-17/coldread/trace-inputs.py` | 82 | yes | `write-open-excluded` (817) + `read-then-rewrite-excluded` (821) |
| P06 | Trace `M03` (PYTHONPYCACHEPREFIX) | `.ufo/evidence/round-17/coldread/trace-inputs.py` | 516 | yes | `env-scrubbed` (893) |
| P07 | Trace `M04` (execve recording) | `.ufo/evidence/round-17/coldread/trace-inputs.py` | 644 | yes | `missing-command-exit2` (847) |

## 2. Exact mutant text

### P01 — `tools/evidence-disposition.py:445` (G3 exact-commit resolution)

```python
# old (count=1)
    if proc.returncode != 0 or resolved != rev:
# new (survivor)
    if False:
```

Function `resolve_historical_rev` (line 442); docstring claims "rev is exactly that
commit id and a commit ancestor of HEAD". Retains the `merge-base --is-ancestor`
block at 451-456, which is why the tree case still rejects.

Closest pinning case: `v2-historical-tree-id` (2551), fixture `_setup_hist_tree`
(2013) sets `hist_rev` to `HEAD^{tree}`. It expects exit 2 +
`historical_input_unavailable`, but a tree fails **both** guards (`tree^{commit}`
errors, and `merge-base --is-ancestor <tree> HEAD` fails), so it cannot detect loss
of the `resolved != rev` conjunct. No case creates an annotated tag, where
`rev^{commit}` peels to an ancestor commit (returncode 0, `resolved != rev`) while
the ancestry check on the tag id succeeds. That tag object is the distinguishing
fixture (R17 witness already demonstrated the CLI difference).

### P02 — `tools/evidence-disposition.py:552` (G5 regular-blob mode guard)

```python
# old (count=1)
    if kind != "blob" or mode not in TREE_MODES:
# new (survivor)
    if kind != "blob":
```

`TREE_MODES = ("100644", "100755")` at 461; function `historical_blob` (545).

Closest pinning case: `v2-blob-bytes-crlf` (2609), fixture `_setup_crlf` (2068)
commits `SELFTEST_TOOL_CRLF` as a regular file (mode 100644) and asserts historical
byte preservation. It exercises bytes, never tree-entry mode. No fixture records a
`120000` symlink or `160000` gitlink; a symlink's Git object type is `blob`, so only
the mode conjunct rejects it.

### P03 — `tools/registry-check.py:466` (detached checkout)

```python
# old (count=1)
            ["git", "-C", clone_root, "checkout", "-q", "--detach", sha],
# new (survivor)
            ["git", "-C", clone_root, "reset", "-q", "--hard", sha],
```

`clone_lane_at_rev` (423); the detached-clone promise is documented at 53-59.

Closest pinning cases: `rev-clone-held` (1024) asserts child exit 0 and the
`held=1/1` lines; `rev-resolved-reported` (1050) asserts the JSON report's
`rev_resolved`, `stdout_tail`, and `registry_sha256`. Neither asserts that the
clone's HEAD is symbolic. (`gitdir-scrub-rev` at 716 checks `head_of(git_lane)` —
the source fixture lane, not the `--rev` clone.) A fixture row running
`git symbolic-ref -q HEAD` and expecting exit 1 would discriminate; R17's witness
already showed pristine exit 0 vs mutated exit 1 on such a registry.

### P04 — `tools/registry-check.py:96` (source revision lower bound)

```python
# old (count=1)
SOURCE_RE = re.compile(r"^[^@]+@[0-9a-f]{7,40}:[0-9]+(-[0-9]+)?$")
# new (survivor)
SOURCE_RE = re.compile(r"^[^@]+@[0-9a-f]{1,40}:[0-9]+(-[0-9]+)?$")
```

`{7,40}` itself also has count=1. Validation error at 228-233 states
`<file>@<7-40 hex rev>:<line>`.

Closest pinning case: `invalid-source` (988) mutates a row's `source` to
`"SKILL.md round-17 registry pending"` — it lacks `@` entirely, so the weakened
`{1,40}` regex still rejects it. No fixture supplies a 1-6 hex-digit revision with a
valid `@…:line` tail; such a row (expect exit 2) is the missing boundary.

### P05 — `.ufo/evidence/round-17/coldread/trace-inputs.py:82` (O_RDWR exclusion)

```python
# old (count=1)
WRITE_FLAGS_RE = re.compile(r"\bO_(?:WRONLY|RDWR|CREAT|TRUNC|APPEND|TMPFILE)\b")
# new (survivor) — delete the `RDWR|` alternative (that token itself count=1)
WRITE_FLAGS_RE = re.compile(r"\bO_(?:WRONLY|CREAT|TRUNC|APPEND|TMPFILE)\b")
```

Contract text at 33-36 excludes the **open mode**, even when no write follows.

Closest pinning cases: `write-open-excluded` (817) and
`read-then-rewrite-excluded` (821). Both children open with Python `'w'`, i.e.
`O_WRONLY|O_CREAT|O_TRUNC`, which the narrowed regex still flags. No fixture opens
an existing tracked file `O_RDWR` without writing. R17's witness (O_RDWR +
immediate close) produced `inputs={}` pristine vs
`{"README.md": <sha>}` mutated.

### P06 — `.ufo/evidence/round-17/coldread/trace-inputs.py:516` (private pycache prefix)

```python
# old (count=1)
    env["PYTHONPYCACHEPREFIX"] = cache
# new (survivor)
    env["PYTHONPYCACHEPREFIX"] = "."
```

Function `scrubbed_env` (510-518); `cache = os.path.join(workdir, "pycache")`
(515). `PYTHONDONTWRITEBYTECODE=1` is set independently at 515, so the mutated
prefix is never exercised by an actual bytecode write.

Closest pinning case: `env-scrubbed` (893) asserts only truthiness —
`lines.get("PYTHONPYCACHEPREFIX")` is non-empty — plus the receipt's
`env_overrides.set.PYTHONDONTWRITEBYTECODE == "1"`; `"."` is truthy. Secondary
cases `double-import-keeps-py` (901) and `no-artifacts-inside-root` (921) check for
`__pycache__` in receipt inputs / the tree, but bytecode writing is disabled, so
prefix placement is unobserved. A case asserting the child-visible prefix equals
the receipt's `env_overrides.set.PYTHONPYCACHEPREFIX` and lies under the run workdir
would discriminate.

### P07 — `.ufo/evidence/round-17/coldread/trace-inputs.py:644` (successful root exec)

```python
# old (count=1)
        if tracer.first_pid is None or tracer.first_pid not in tracer.exec_ok:
# new (survivor)
        if tracer.first_pid is None:
```

Post-trace guard in `main` (642-647); `first_pid not in tracer.exec_ok` itself has
count=1.

Closest pinning case: `missing-command-exit2` (847) traces `./no-such-command-xyz`.
strace exits 1 before producing a trace (`Cannot stat …`, 0-byte log per R17's
direct check), so `first_pid is None` alone returns 2; the removed conjunct is never
reached. `missing-strace-exit2` (843) is the same shape via `PATH=/nonexistent-ti-dir`.
A fixture with a nonempty, parseable trace whose root pid never reaches a successful
`execve` is the missing discriminator.

## 3. Survival re-check at REV (falsifier, not taken from R17 on trust)

For each row, the exact old string was asserted `count==1`, the one replacement was
applied in the /tmp clone, `--selftest` was run with scrubbed `GIT_*`, cwd inside the
clone and a per-mutant `TMPDIR`, then the original bytes were restored and re-hashed.
Command shape (script executed from `/tmp/tameshi-r18w1-S01SurvivorAnchors-CP5eDG`):

```sh
python3  # loop: assert count==1; write mutated bytes; subprocess.run(
         #   ['python3', '<clone>/<path>', '--selftest'], cwd=clone,
         #   env without GIT_*, TMPDIR=scratch/<name>, timeout=240)
         # restore original bytes; sha256 before == after
```

Observed (all stderr empty; `mut_exit` is the selftest process exit):

| Mutant | mut_exit | Summary line | Restored byte-identical |
|---|---:|---|---|
| P01 G3Commit | 0 | `SELFTEST: PASS (56/56)` | yes |
| P02 G5Mode | 0 | `SELFTEST: PASS (56/56)` | yes |
| P03 M06checkout | 0 | `SELFTEST: PASS (34 cases)` | yes |
| P04 M07source-regex | 0 | `SELFTEST: PASS (34 cases)` | yes |
| P05 M01rdwr | 0 | `SELFTEST: 27/27` | yes |
| P06 M03pycache | 0 | `SELFTEST: 27/27` | yes |
| P07 M04execve | 0 | `SELFTEST: 27/27` | yes |

Pristine baselines at REV, run before mutation (same scrubbed environment):
disposition exit 0 `PASS (56/56)`, registry exit 0 `PASS (34 cases)`, trace exit 0
`27/27`; stderr 0 bytes each. Tools observed: `Python 3.14.8`, `strace 7.2`,
`git 2.56.0`.

## 4. Notes / gaps for the probe author

- All seven `open` semantics hold at REV: the exact survivor mutations pass their
  owning `--selftest` (exit 0). Applying them with `old.count != 1` must be exit 2
  per contract A; none of the seven can trip that guard if the full old strings
  above are used.
- P01 new text `if False:` is the R17 survivor form, leaving the ancestry check
  intact. P02 keeps `kind != "blob"`. Do not "improve" these mutants.
- P03 changes two argv tokens (`checkout`→`reset`, `--detach`→`--hard`) within one
  line; it is one mutant row, exactly as mutated in R17.
- Line numbers are REV-specific and were re-derived here, not copied: all three
  blobs hash identically to the R17 landing (`f8f05c7…`, `0bf9d1d…`, `521be95…`).
- [INFERENCE] P05/P06/P07 probe at a later rev with a tracked `tools/trace-inputs.py`
  must re-anchor by string; contract B's promoted copy is required to preserve these
  three guards, and the probe's own selector already encodes the fallback.
- No blockers; no tool installs/updates were performed. Scratch root only:
  `/tmp/tameshi-r18w1-S01SurvivorAnchors-CP5eDG`.

Verdict: holds — seven of seven R17 survivor mutants map to count==1 anchors at
`183f87b8`, each with a named nearest selftest case that demonstrably misses it, and
all seven still pass their owning `--selftest` at REV.
