# MutateTraceInputs18 — bounded mutation probe

## Scope and axes

- Read revision: `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`.
- Target: `tools/trace-inputs.py`; owning detector: `python3 tools/trace-inputs.py --selftest`.
- Axes: **depth** (guard/receipt semantics), **calibration** (detector sensitivity and named survivors), with **operability** monitored through hermetic execution and exact restoration.
- Result: **10 KILLED, 2 SURVIVED, 0 INCONCLUSIVE** across 12 independent, single-point mutants. This is a scoped detector finding, not a judgment of round admission or the other round claims.
- Pristine detector: exit **0**, `SELFTEST: 30/30`. Restored detectors: **12/12** exit **0**, each `SELFTEST: 30/30`.
- No live tool, sibling source, live Git index, registry, or lane state was changed. This report is the only live-lane write. No tools were installed or updated.

## Isolation and commands actually exercised

Scratch root:

```text
W=/tmp/tameshi-r18w2-MutateTraceInputs18-KSDvf9
C=/tmp/tameshi-r18w2-MutateTraceInputs18-KSDvf9/fleet/tameshi-shokunin
```

The initial clone and detached checkout both exited 0. Commands, with all inherited `GIT_*` entries removed from the subprocess environment and `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `LC_ALL=C` supplied:

```sh
git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin "$C"
git -C "$C" checkout -q --detach 01d586ddbc5fcd78659557c4e93a6ee8517b87d1
git -C "$C" show 01d586ddbc5fcd78659557c4e93a6ee8517b87d1:tools/trace-inputs.py
```

Read-only sibling symlinks were created beside the initial clone. Each mutant received its own isolated clone, using the following command for each `ID` from `M01` through `M12`; all 12 exited 0:

```sh
git clone -q --shared "$C" "$W/mutants/$ID"
```

Before mutation, `sha256sum "$W/mutants/$ID/tools/trace-inputs.py"` returned the pristine digest below for **all 12** clones. Every exact `@old` line was counted against the revision's source bytes **before edits**, and every count was **1**; its line number was also checked. There was one behavior-bearing line change in each clone; no mutant was stacked on another. M07's two-line function-call expression was replaced intact, changing only its `HEAD` argument.

The same bounded detector envelope was executed once on pristine `$C`, once on each mutated clone, and once on each restored clone. In the command below, `D` was the pristine `$C` or the respective absolute `$W/mutants/Mxx` path; the harness passed these as expanded argument vectors, with subprocess cwd equal to `D`:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR \
  bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp \
  --bind "$W" "$W" --unshare-net --die-with-parent --chdir "$D" \
  env -i PATH=/usr/bin:/bin HOME="$W/home" TMPDIR="$W/tmp" \
  GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C \
  python3 "$D/tools/trace-inputs.py" --selftest
```

Each invocation had a **120-second** subprocess deadline. Independent mutant runs used a finite joined batch with maximum concurrency **4**; restored runs used the same cap. Mutant detector runtimes were 1.370–1.569 seconds. No invocation timed out, no background job was left running, and all detector stderr was empty. The fleet was read-only inside every detector sandbox; only this seat's scratch root was rebound writable.

## Mutants, expected detectors, and actual output

All locations below are `tools/trace-inputs.py` at the pinned revision; mutant clones retain these line numbers. Expected cases were recorded before applying any mutant. All failing case names are listed, including additional failures beyond the primary expected cases. Every nonlisted case printed `PASS`.

| ID | Point / mutation | Expected owning case(s) | Actual exit / summary | Actual `FAIL` case names | Verdict |
|---|---|---|---|---|---|
| M01 | `:82`, remove the `RDWR` arm from `WRITE_FLAGS_RE` | `rdwr-open-excluded` | 1 / `SELFTEST: 29/30` | `rdwr-open-excluded` | **KILLED** |
| M02 | `:399`, disable the write-mode guard | `write-open-excluded`, `rdwr-open-excluded`, `read-then-rewrite-excluded` | 1 / `SELFTEST: 27/30` | `write-open-excluded`, `rdwr-open-excluded`, `read-then-rewrite-excluded` | **KILLED** |
| M03 | `:516`, remove the child pycache prefix | `env-scrubbed`, `pycache-prefix-private` | 1 / `SELFTEST: 28/30` | `env-scrubbed`, `pycache-prefix-private` | **KILLED** |
| M04 | `:514`, anchor pycache at shared tempdir instead of private workdir | `pycache-prefix-private` | 0 / `SELFTEST: 30/30` | None | **SURVIVED** |
| M05 | `:644`, remove the root successful-exec requirement | `missing-command-exit2`, `root-exec-required` | 1 / `SELFTEST: 28/30` | `missing-command-exit2`, `root-exec-required` | **KILLED** |
| M06 | `:534`, flip repository-root identity comparison | `git-tracked-filter`, `subdir-root-rev-null` | 1 / `SELFTEST: 28/30` | `git-tracked-filter`, `subdir-root-rev-null` | **KILLED** |
| M07 | `:538`, substitute revision anchor `HEAD^` for `HEAD` | `git-tracked-filter` | 1 / `SELFTEST: 29/30` | `git-tracked-filter` | **KILLED** |
| M08 | `:551`, resolve tracked Git paths against requested root instead of repository toplevel | `subdir-root-rev-null` | 1 / `SELFTEST: 29/30` | `subdir-root-rev-null` | **KILLED** |
| M09 | `:298`, flip tracked-membership test | `git-tracked-filter`, `subdir-root-rev-null` | 1 / `SELFTEST: 28/30` | `git-tracked-filter`, `subdir-root-rev-null` | **KILLED** |
| M10 | `:654`, remove final disqualification of read-then-written paths | `read-then-rewrite-excluded` | 1 / `SELFTEST: 29/30` | `read-then-rewrite-excluded` | **KILLED** |
| M11 | `:681`, emit the untracked bucket as receipt `inputs` | `python-read-input`, `git-tracked-filter` | 1 / `SELFTEST: 20/30` | `python-read-input`, `bash-source-input`, `cd-relative-input`, `symlink-in-resolves`, `execve-script-input`, `git-tracked-filter`, `subdir-root-rev-null`, `double-import-keeps-py`, `escaped-names-recorded`, `cwd-option-input` | **KILLED** |
| M12 | `:656`, hash the pathname rather than file bytes | `python-read-input`, `git-tracked-filter` | 0 / `SELFTEST: 30/30` | None | **SURVIVED** |

### Exact replacements

Each arrow below is one independent mutation, with `@old count == 1`:

```python
# M01, line 82
WRITE_FLAGS_RE = re.compile(r"\bO_(?:WRONLY|RDWR|CREAT|TRUNC|APPEND|TMPFILE)\b")
# ->
WRITE_FLAGS_RE = re.compile(r"\bO_(?:WRONLY|CREAT|TRUNC|APPEND|TMPFILE)\b")

# M02, line 399
            if WRITE_FLAGS_RE.search(tail):
# ->
            if False and WRITE_FLAGS_RE.search(tail):

# M03, line 516
    env["PYTHONPYCACHEPREFIX"] = cache
# ->
    env.pop("PYTHONPYCACHEPREFIX", None)

# M04, line 514
    cache = os.path.join(workdir, "pycache")
# ->
    cache = os.path.join(tempfile.gettempdir(), "pycache")

# M05, line 644
        if tracer.first_pid is None or tracer.first_pid not in tracer.exec_ok:
# ->
        if False:

# M06, line 534
    if toplevel != root:
# ->
    if toplevel == root:

# M07, line 538 (the preceding line of the call is unchanged)
                        "rev-parse", "--verify", "HEAD"], env)
# ->
                        "rev-parse", "--verify", "HEAD^"], env)

# M08, line 551
            tracked.add(os.path.realpath(os.path.join(toplevel, os.fsdecode(raw))))
# ->
            tracked.add(os.path.realpath(os.path.join(root, os.fsdecode(raw))))

# M09, line 298
            if self.tracked is not None and resolved not in self.tracked:
# ->
            if self.tracked is not None and resolved in self.tracked:

# M10, line 654
                if path in tracer.writes or not os.path.isfile(path):
# ->
                if not os.path.isfile(path):

# M11, line 681
            "inputs": inputs,
# ->
            "inputs": untracked,

# M12, line 656
                out[path] = sha256_file(path)
# ->
                out[path] = hashlib.sha256(path.encode("utf-8", "surrogateescape")).hexdigest()
```

## Named survivor coverage gaps — routed, not repaired

### TRACE-INPUTS-PRIVATE-CACHE-ANCHOR — M04

**Route:** `TameshiR18` / owning `tools/trace-inputs.py::selftest`; calibration/verification-fixture coverage finding.

- Behavior-bearing point: `tools/trace-inputs.py:514`; the documented private-workdir promise is at `:39-48`, and cleanup removes only the generated workdir at `:694-695`.
- Actual mutant output: exit **0**, `SELFTEST: 30/30`, including `PASS pycache-prefix-private`, `PASS double-import-keeps-py`, `PASS temp-workdirs-deleted`, and `PASS no-artifacts-inside-root`.
- The existing `pycache-prefix-private` assertion at `:925-930` checks agreement with the receipt, absoluteness, and exclusion from root. It does not require the cache prefix to be beneath the unique private workdir or distinguish two successive prefixes.
- The mutant chooses the fixed `tempfile.gettempdir()/pycache` anchor, not `workdir/pycache`. Thus the detector accepts a loss of per-invocation private anchoring. No cross-run cache-poisoning exploit was attempted or claimed.
- [INFERENCE / unrun detector recommendation] Assert per-invocation cache-parent uniqueness and cleanup, and use a pre-existing shared-cache fixture to distinguish private source reads from shared cache reuse. This is a detector-coverage recommendation, not a request to relax the private-prefix contract. The production tool was not edited.

### TRACE-INPUTS-DIGEST-CONTENT — M12

**Route:** `TameshiR18` / owning `tools/trace-inputs.py::selftest`; calibration/receipt-authenticity coverage finding.

- Behavior-bearing point: `tools/trace-inputs.py:656`; receipt bucket construction is at `:659-684`.
- Actual mutant output: exit **0**, `SELFTEST: 30/30`, including `PASS python-read-input`, `PASS git-tracked-filter`, `PASS subdir-root-rev-null`, and `PASS double-import-keeps-py`.
- `python-read-input` at `:807-808` only tests that the receipt value is truthy. `git-tracked-filter` at `:902-908` checks membership, bucket separation, tracked-filter state, and revision identity, but never compares the digest with fixture content. The remaining selftest assertions at `:810-956` likewise do not assert exact expected content hashes.
- Replacing the content-digest call with a pathname-digest call therefore leaves all selftests green. The behavior-bearing difference is explicit in the mutant; the observed result establishes that the detector does not distinguish it.
- [INFERENCE / unrun detector recommendation] Compare at least `inputs["a.txt"]` with the known SHA-256 of the fixture's `alpha\n` bytes, and independently assert expected digests for tracked/untracked/external/live-lane buckets. Preserve the content-hash contract; do not bless the pathname digest. The production tool was not edited.

## Before / mutant / restored byte evidence

Pristine source digest, denoted **P** below:

```text
fb1d81f67551fb04e9e447cbc706ef5cc9cfd5208169004184b24ab15f3f2636
```

`git show REV:tools/trace-inputs.py` was hashed with SHA-256; `sha256sum` on the initial clone and each pre-mutation clone matched P. Actual mutated-file hashes were obtained with `sha256sum` immediately before each detector run:

| ID | Before | Mutated SHA-256 | Restored SHA-256 | `cmp -s` exit | Restored detector |
|---|---|---|---|---|---|
| M01 | P | `5510c512c3759ae577b670a13af1643f241b19311b79a2a9a217113271df827c` | P | 0 | exit 0; `SELFTEST: 30/30` |
| M02 | P | `c246c9724237c0403f29b5b7f5db5535d6a4d9c3a134282a0bcf86049f093656` | P | 0 | exit 0; `SELFTEST: 30/30` |
| M03 | P | `705273f5a1bb4df4e282e6d9ea8fe24773d7d5e65cb6237a0a90665888d086e1` | P | 0 | exit 0; `SELFTEST: 30/30` |
| M04 | P | `6ba20735c2c1c5be022e8c03a07c30a3a7d889a9d6380b7ca55a8cac11b2437a` | P | 0 | exit 0; `SELFTEST: 30/30` |
| M05 | P | `8357fc50ca53a19908c0a6269126aa1efb4e40360b1a9ae2e67086bc55e8db70` | P | 0 | exit 0; `SELFTEST: 30/30` |
| M06 | P | `c6b4db8dc7f8ecc7103135787280859957f9655bd0df6ea89b1671a5619a8e21` | P | 0 | exit 0; `SELFTEST: 30/30` |
| M07 | P | `2dc37d1c841424e54dc8dd3000971cddf837fab274e1a4eb0c63500299820e66` | P | 0 | exit 0; `SELFTEST: 30/30` |
| M08 | P | `010499191a7ec643d225a144166f433185fc52c779fdefc1439171318232a21a` | P | 0 | exit 0; `SELFTEST: 30/30` |
| M09 | P | `958c95d3b2bc31a56e429220ebcc4ef9bb36622398a8396080d4152f000dc96c` | P | 0 | exit 0; `SELFTEST: 30/30` |
| M10 | P | `0e381f59ef970231450914e66b8672af2f63beb4063db0485e07e16e2d2ed716` | P | 0 | exit 0; `SELFTEST: 30/30` |
| M11 | P | `563ef182b93e8ba2597c3bf0496790d5c4199380213a11bfdde37b25c4aa27ee` | P | 0 | exit 0; `SELFTEST: 30/30` |
| M12 | P | `05de235ff5c73ec99c4ae3872a41d98d2aaf6f12a9c7525310a64225c7cd3304` | P | 0 | exit 0; `SELFTEST: 30/30` |

All mutants were restored by the exact inverse single-point edit before restored detectors were run. After each restored detector invocation, these commands were exercised for that ID:

```sh
sha256sum "$W/mutants/$ID/tools/trace-inputs.py"
cmp -s "$C/tools/trace-inputs.py" "$W/mutants/$ID/tools/trace-inputs.py"
```

Every SHA-256 was P and every byte-for-byte comparison exited 0. Every restored detector had empty stderr and no `FAIL` line. Baseline failure did not contaminate any verdict: the sole pristine run passed, and all twelve exact-byte restorations passed.

## Closure

The direct O_RDWR-removal, prefix-removal, and root-exec-removal mutants were killed by their named owning tests. Revision identity, revision anchor, tracked-path anchoring, membership, rewritten-file exclusion, and wrong-bucket mutations were also killed. Private-cache anchoring and digest-content authenticity each have a named surviving mutant routed above. No contract changes, fixes, integrations, or other runtimes were invoked.

partial — 10/12 mutants killed; 2 named coverage gaps routed; all 12 restored byte-for-byte and passing 30/30.
