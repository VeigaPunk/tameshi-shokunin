done — scoped fixture recipes and predicted mutant failures recorded; predicted outputs are explicitly unrun.

# Frozen target and evidence

- The lane `HEAD` observed as `33d03b716d3edcf1d8656d46d6df61801d232c52`, the assigned frozen base. The working tree has unrelated `LOG.md` / round-21 evidence and wave changes; neither target tool appeared in the reported dirty paths.
- Frozen IDs/edits: `.ufo/evidence/round-21/c1-mutants.json:73-89` (D02, D11, D12) and `:109-120` (T04, T12).
- LSP unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; the mounted-device inventory had no LSP. Search results below are literal fallback, not semantic proof.
- Fixture routes reuse the target selftests: disposition `_build_lane` / `_dispositions_v2` / Git helpers / `historical_case` at `tools/evidence-disposition.py:1719-1759,1982-2026,2056-2073,2438-2452`; trace `put`, `trace`, and `check` closures at `tools/trace-inputs.py:715-721,779-805,776-777`.
- Observed precedent: equivalent round-18 mutants hardcoding `master` (M02/M12) and removing `100755` from `TREE_MODES` (M11) survived their disposition selftest at `63/63`; the report names the absent coverage scenarios at `.ufo/waves/round-18/w2/MutateDisposition18.md:42-57,86-90`. Equivalent trace mutants T04/M04 and T12/M12 survived at `30/30`, `.ufo/waves/round-18/w2/MutateTraceInputs18.md:54-67,137-155`.

# Recipes and expected failures

The recipes below are **[INFERENCE / unrun]**: add the specified case/assertion to the owning selftest, then apply only that frozen mutant. `case()` checks exit, finding IDs, payload exit/status and reports one `SELFTEST_CASE ... FAIL` line on a mismatch (`evidence-disposition.py:2387-2436`). No guard/contract relaxation is indicated.

## D02 — attached non-master branch extraction

At `evidence-disposition.py:461-490`, D02 affects the branch name obtained from attached `HEAD` only when `lane.branch` is absent; the existing historical Git fixtures use `master` (`:2162-2168,2213-2244,2255-2288`). Add `_setup_hist_attached_topic(fx)` and a `historical_case("v2-attached-topic-branch", 0, [], _setup_hist_attached_topic)`:

1. Use the existing `_build_lane` content. In its lane, run `git init -q -b topic/r21` (do not set `lane.branch`; no `master` ref is created).
2. Commit the initial `tools/pinned-tool.py` bytes as A via `_git_commit_all`; save A as `fx["hist_rev"]`.
3. Replace it with `SELFTEST_TOOL_V2` and commit B on the still-attached `topic/r21` branch. Thus A is an ancestor and B contains the live drifted bytes.
4. Build the usual v2 disposition through `historical_case`; it pins `tools/pinned-tool.py` at A.

Correct code resolves `refs/heads/topic/r21` and passes. D02 sets `branch = "master"` at `:472`; because this fixture deliberately has no master ref, resolution returns `historical_input_unavailable` (`:484-489`). Expected mutant case output:

```text
SELFTEST_CASE v2-attached-topic-branch FAIL (exit=2 expects=0; ids=['historical_input_unavailable'] expects=[]; payload exit=2; status='could_not_evaluate' expects='clean')
```

## D11 — positive regular executable historical blob

`historical_blob` accepts only `kind == "blob"` and mode in `TREE_MODES` (`evidence-disposition.py:549-550,636-650`). The existing symlink negative case is at `:2881-2885`; there is no executable-regular positive case in the historical fixture builders at `:2076-2159`. Add `_setup_hist_executable(fx)` and `historical_case("v2-historical-executable-regular-blob", 0, [], _setup_hist_executable)`:

1. In the built lane, `git init -q -b master`.
2. Before the first commit, make the existing regular `tools/pinned-tool.py` executable (`os.chmod(path, 0o755)`; stage it, and use `git update-index --chmod=+x tools/pinned-tool.py` if the fixture wants to force the index mode). Commit and assert `git ls-tree A tools/pinned-tool.py` reports `100755 blob`; save A as `fx["hist_rev"]`.
3. Replace the live file with `SELFTEST_TOOL_V2` and commit it on master. Use the standard historical v2 manifest, so the live bytes differ from the pin and equal the committed anchor bytes.

The pristine gate accepts this regular blob; D11 changes `TREE_MODES` to `("100644",)` and reports `historical_input_unavailable`. Expected mutant output:

```text
SELFTEST_CASE v2-historical-executable-regular-blob FAIL (exit=2 expects=0; ids=['historical_input_unavailable'] expects=[]; payload exit=2; status='could_not_evaluate' expects='clean')
```

## D12 — configured non-master branch

D12 changes `branch_ref` construction at `evidence-disposition.py:476-490`; the configured setting is read at `:462-466`. Add `_setup_hist_configured_topic(fx)` and `historical_case("v2-configured-topic-branch", 0, [], _setup_hist_configured_topic)`:

1. `git init -q -b master`; commit the initial pinned tool as A and leave `refs/heads/master` at A.
2. Create/checkout `topic/r21` from A, replace the tool with `SELFTEST_TOOL_V2`, and commit B there. Set this repo's `lane.branch` to `topic/r21` (do not alter master). Save A in `fx["hist_rev"]`.
3. Use the standard historical v2 disposition. The fixture's intended anchor is topic B, whose tool bytes equal the live V2; the pin at A is its ancestor.

Correct code passes G2/G3 on topic B. D12 hardcodes `refs/heads/master`; it selects A, so G2 observes anchor bytes V1 differing from live V2 and raises `historical_input_uncommitted` (`:605-633`). Expected mutant output:

```text
SELFTEST_CASE v2-configured-topic-branch FAIL (exit=2 expects=0; ids=['historical_input_uncommitted'] expects=[]; payload exit=2; status='could_not_evaluate' expects='clean')
```

If all three disposition cases are added, the prior measured 63-case baseline implies a predicted one-failure summary of `SELFTEST: FAIL (1/66 failed: <case>, fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.<random>)`; the exact scratch suffix is runtime-generated (`:3089-3101`). Per-case failure lines above are the discriminating expected outputs.

## T04 — pycache must be under this trace's private workdir

The selftest fixes `TMPDIR=scratch` for each trace (`trace-inputs.py:793-800`); `make_workdir` creates a unique `trace-inputs-run-*` directory (`:575-596`), and production `scrubbed_env(workdir)` sets `<workdir>/pycache` (`:513-517`). The T04 mutation instead chooses `tempfile.gettempdir()/pycache`. Strengthen the existing `pycache-prefix-private` assertion at `:917-930` by also requiring:

```python
os.path.basename(os.path.dirname(pycache)).startswith("trace-inputs-run-")
```

Keep the current `trace([SH, "-c", "env"], capture=True, ...)` fixture; its fixed scratch TMPDIR makes the mutant's prefix `scratch/pycache`, whose parent is not a `trace-inputs-run-*` workdir. This uses the existing case, so the predicted mutant output is:

```text
FAIL pycache-prefix-private
SELFTEST: 29/30
```

## T12 — compare a receipt digest with fixture bytes

The selftest creates `root/a.txt` containing exactly `alpha\n` (`trace-inputs.py:723`) and reads it in `python-read-input` (`:807-808`). That case currently checks only that the digest is truthy; production hashes file bytes at `:651-657`, while T12 hashes the pathname. Strengthen that existing assertion to require:

```python
d["inputs"].get("a.txt") == "b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060"
```

The expected digest is SHA-256 of `b"alpha\n"`; the pathname digest is different. Predicted mutant output:

```text
FAIL python-read-input
SELFTEST: 29/30
```

# Command/evidence record and limits

- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD && git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain | wc -l` — completed successfully; output was the frozen hash above and `7` dirty paths.
- `printf 'alpha\n' | sha256sum` — output `b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060  -`.
- `read xd://lsp` — unavailable as stated above. Literal searches located the target cases; all conclusions about definitions and behavior are grounded in the cited source lines, not LSP reference proof.
- No selftest/mutant replay was run in this read-only reconnaissance. The round-18 survivor outputs are observed historical evidence; the new fixture failure snippets are predicted from the current source and are not represented as exercised results. No tools were installed.