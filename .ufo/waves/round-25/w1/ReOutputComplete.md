# R23-REATTACK OutputComplete (round 25, wave 1, seat ReOutputComplete)

**Verdict: FINDING.** At lane revision `c9ff09fb41fb8aac5fc335faf10858ff606bd5df` the stream-binding claims hold: the gate reads stdout only, early markers are matched on the full stream, and stderr cannot satisfy a token. The retention half of the item does not hold. `registry-replay.py --run` writes complete stdout and stderr to `observations.json` before any `--max-stream-bytes` bound is applied, while its docstring says retained streams are bounded. Round 23 routed this as "Replay streams are retained without size bounds or redaction" (`.ufo/waves/round-23/fresh-adjudication.json`, `routed_not_executed`). It is still open at c9ff09b.

## 0. Status of the original item

- The round-23 seat `TameshiR23.OutputComplete` ended `failed` with no callback and no report (`.ufo/waves/round-23/original-outcomes2.json`, `death_basis`: "no task-result callback retained"). No `round-23/w2/OutputComplete.md` exists at `332dc89` or in the working tree. This is the first run of the attack.
- Revisions: lane HEAD is `5b69fb2`. I attacked `c9ff09f` in a `/tmp` clone (`/tmp/oc-clone/oc`). Since round 23 (`496d212`):
  - `tools/registry-check.py` is unchanged (`git diff --quiet 496d212 c9ff09f`).
  - `tools/registry-replay.py` is unchanged since `d2eaecd` (`git diff --quiet d2eaecd c9ff09f`).
  - `tools/command-binding.py` changed only in its selftest fixture loader (hunk `@@ -161,11 +161,12 @@`, which now also reads `round-24/extra-cases.json`). `evaluate()` is unchanged.
- Registry rows (`tools/registry.json`): the three round-23 gate rows (`command-binding-selftest`, `command-binding-frozen-clean`, `command-binding-source-read-red`) are `superseded`. The active successors are `command-binding-selftest-r24` (44/44), `command-binding-frozen-clean-pinned` and `command-binding-source-read-red-pinned`. I checked the pinned rows at c9ff09b (section 4). `registry-replay-selftest` is active but never calls `run_replay` (F1).

## 1. Findings, by severity

### F1 (Medium): full-stream retention is not bounded at c9ff09b. Still applies.

Claim at `tools/registry-replay.py:9`: "each retained stdout/stderr is bounded by --max-stream-bytes (STREAM_LIMIT)".

Code path (`tools/registry-replay.py`):
- `:170` calls `run_row(..., retain_streams=True)`.
- `:176-180` builds `observations` with every full `runner_result`.
- `:183` writes `out/observations.json` with `encode(observations)`.
- `:184` only then calls `project(observations, args.max_stream_bytes)`. The check at `:96-97` (`STREAM_LIMIT`) only refuses publication of `bundle.json`.

The runner has no cap either. `tools/registry-check.py:693` calls `communicate()`, which buffers the whole stream. `:717` decodes it and `:724-726` copies it into the fragment when `retain_streams` is set. The only size constants in the file are `TAIL_BYTES = 4096` (`:110`) and `PIPE_DRAIN_TIMEOUT_S` (`:114`). Memory use is the same with or without `retain_streams`. The extension adds persistence, not memory.

Executed in `/tmp` only, through the real `run_replay` path. One synthetic row, `python3 -c "import sys; sys.stdout.write('A' * 2097152)"`, default `--max-stream-bytes` (1 MiB):

```
python3 tools/registry-replay.py --run --repo /tmp/oc-clone/oc --rev c9ff09fb41fb8aac5fc335faf10858ff606bd5df \
  --requirements /tmp/oc-synth/e2e-big/requirements.json --registry-baseline /tmp/oc-synth/e2e-big/registry.json \
  --out /tmp/oc-synth/e2e-big/out
-> big-stream 0 True
-> {"bundle_sha256": null, "finding_ids": ["STREAM_LIMIT"], "refused_rows": ["big-stream"], ...}   exit 1
observations.json 2103252 bytes; it holds 2097152 stdout characters
bundle.json ABSENT; expected.json ABSENT
```

Frozen artifact: `.ufo/evidence/round-23/replay/observations.json` is 262,796 bytes and holds complete stdout and stderr for all 43 rows, committed at `8f66b5d`. A narrow pattern count (PEM private key, AWS key id, `ghp_`, `sk-`, and `password|secret|api_key = value`) found 0 hits in `observations.json` or `bundle.json`. This is a count-only spot check, not a secret scan.

Why the selftest missed it: `registry-replay.py:199-206` tests `project()` on hand-built observations. Nothing exercises the write order in `run_replay`. Round 24 raised the same overclaim (`.ufo/waves/round-24/w1/ClosureCarry.md` F2; `CorpusContract.md`), and the text is unchanged at c9ff09b.

Smallest safe correction (not applied): in `run_replay`, call `project()` before line 183. When it refuses, write only a size record (row names and byte counts, no stream bodies) instead of `observations.json`. Then correct line 9. A per-stream read cap in `run_row` is a larger change and should be routed separately.

### F2 (Low, documentation): the runner docstring says the needle check is "over the retained tail".

`tools/registry-check.py:36-37`: "every stdout_contains needle appears in stdout (literal, case-sensitive, ANDed, over the retained tail)". The code checks the complete decoded stream: `:717-720` (`stdout_text`, `missing`, `held`). The code is the correct and stricter behavior. The docstring is wrong and invites the early-marker misreading this item asked about. Correction: "over the complete decoded stdout". This was also flagged in `.ufo/waves/round-23/original-outcomes1-partial.json` (HistoricalSource).

### F3 (Informational, out of contract): a relabelled receipt argv passes.

Mutant on the round-23 red bundle (`.ufo/evidence/round-23/source-read-bundle.json`, whose receipt is `cat tools/registry.json` with the frozen token in its stdout). Setting `receipts[0].argv` to the required argv and re-pinning the expected digest gives `{"exit": 0, "finding_ids": []}` at c9ff09b (bundle sha `4484a73de6fd459748d53a8c542b07fd674678dd86f45724f1af7df5e65f8c5b`). Honest receipts are caught: the unmodified red bundle gives `ARGV_MISMATCH`, exit 1 (sha `db620668…`). `tools/command-binding.py:12-13` states that the gate validates declarations, not producer authenticity, so this is a stated non-claim. It does mean the `source-read-red` row discriminates the argv field only. It does not show that a source read is rejected independently of its declared argv. No row change is recommended. The wording should not claim more.

### F4 (Informational): some frozen stdout tokens are loose.

Of the 52 token occurrences across the 43 rows, some are bare JSON fragments: `"coldread":` (`measure-round16-rev`), `"unavailable": 0` (`pin-disposition-read`), `"effective": 11` (`evidence-disposition-round18`). Any stray print of the same text satisfies them. Already routed in `fresh-adjudication.json` ("Preexisting loose stdout substring tokens ... kept unchanged"). Not re-litigated here.

## 2. What holds (AGREE evidence)

| Concern | Evidence at c9ff09b | Result |
|---|---|---|
| No stderr laundering in the gate | `command-binding.py:111-112` checks only `receipt['stdout']`. `:88-91` type-checks stderr and never reads it for findings. Mutant: the red bundle with its argv set to the required argv, stdout `''` and the token only in stderr gives `STDOUT_MISMATCH`, exit 1 (sha `a6134761…`). Selftest case `stderr-cannot-supply-token` (`:155`) passes: `COMMAND_BINDING_SELFTEST: 44/44 pass` in the clone. | Holds |
| No stderr laundering in the runner | `registry-check.py:718-720`: `held` depends on stdout only. Synthetic row with the token on stderr only: `got 0, held False, missing ['STDERR_ONLY_TOKEN']`. `run_replay` refuses it: `finding_ids ["RUNNER_NOT_HELD"]`, bundle absent. | Holds |
| Stream separation | Synthetic row writes `OUT` to stdout and `ERR` to stderr: `stdout == 'OUT'`, `stderr == 'ERR'` exactly. Frozen round-23 bundle: receipt stdout and stderr equal the runner's streams for 43 of 43 rows (`bundle.json` vs `observations.json`). No stderr head appears inside stdout. | Holds |
| Early markers recovered from the full stream | Synthetic row prints `EARLY_MARKER_OK`, then 20,000 bytes: `held True`, `stdout_tail` lacks the token, full `stdout` (20,016 chars) has it. `run_replay` publishes a bundle; `command-binding.py --bundle … --expected …` gives `{"exit": 0, "finding_ids": []}`. Frozen: 12 rows have stdout longer than the 4096-byte tail. Six token occurrences (in `pin-disposition-read`, `evidence-disposition-round18` twice, `evidence-disposition-round18-before`, and `measure-round16-rev` twice) appear only beyond the tail. They are matched on the full stream: no false pass, no false fail. | Holds (docstring error F2) |
| Tails are reporting only | `registry-check.py:722-723` builds tails from the full bytes. `:724-726` attaches full streams only with `retain_streams`, and the default is `False` (`:648`). Old tails cannot prove an early marker is absent. The round-24 `RowAudit04.md:78-80` says `missing` uses the full stream. | Holds |
| Pinned active gate rows | At c9ff09b in the clone: `--bundle .ufo/evidence/round-23/replay/bundle.json` gives exit 0, sha `3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9` (pinned). `source-read-bundle.json` gives exit 1, `ARGV_MISMATCH`, sha `db620668…` (pinned). | Holds |

## 3. Verification gaps and residual risk

- **Timeout drain path, not exercised.** `_bounded_communicate` (`registry-check.py:612-629`) can return partial bytes. `run_row` then labels them complete at `:725` when the leader exited and `cleanup_ok` is true. Read statically: cleanup signals owned descendants before the drain (`:696-699`), so an open pipe with `cleanup_ok` true should not occur. Not exercised.
- **Not run:** `registry-replay.py --selftest`, the full 43-row replay, and any lane gate. Everything I executed ran in `/tmp`.
- **Scope of the secret check:** a count of five narrow patterns, no content review.
- **lsp device:** not available. `xd://lsp` returned "No such tool. Mounted devices: ast_edit, debug." I used read and grep as the literal fallback. No semantic reference proof is claimed.
- **Lane touches (read-only):** the first command ran `jj st --no-pager` in the lane. Its intent was read-only, but jj status can snapshot the working copy. No mutating jj or git command was run. Other lane git calls were `rev-parse`, `log`, `show`, `ls-tree`, `cat-file` and `diff`, with `GIT_OPTIONAL_LOCKS=0` where a status-like call was used. One `git -C /home/vgpnk/Projects/shokunin rev-parse HEAD` and one `ls` on the fleet root. No writes anywhere in the lane or fleet.
- **Tools:** none installed or updated.
- **Writes:** this report only. Scratch lives in `/tmp/oc-clone` (clone at c9ff09f), `/tmp/oc-synth` (synthetic registry, requirements and outputs) and `/tmp/oc-clone/*.json` (mutant bundles).

## 4. Exact commands and observed output (all in `/tmp/oc-clone/oc` at c9ff09f unless noted)

- `python3 tools/command-binding.py --selftest | tail -2` → `COMMAND_BINDING_SELFTEST: 44/44 pass`
- `python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json` → `{"bundle_sha256": "3d6c99b7…", "exit": 0, "finding_ids": []}`
- `python3 tools/command-binding.py --bundle .ufo/evidence/round-23/source-read-bundle.json --expected .ufo/evidence/round-23/source-read-expected.json --json` → `{"bundle_sha256": "db620668…", "exit": 1, "finding_ids": ["ARGV_MISMATCH"]}`
- Mutants on the red bundle (in `/tmp/oc-clone`): argv relabel → exit 0 (F3); stderr-only token (argv also set) → `STDOUT_MISMATCH` exit 1; duplicate receipt → `DUPLICATE_COMMAND` exit 1; cwd change → `["ARGV_MISMATCH", "CWD_MISMATCH"]`; revision change → `["ARGV_MISMATCH", "REVISION_MISMATCH"]` (the base bundle already carries `ARGV_MISMATCH`).
- `run_row` synthetic rows, driven through `importlib` on `tools/registry-check.py` from the clone: `early-marker`, `stderr-only`, `merge-check` (results in section 2).
- `run_replay` synthetic runs via `tools/registry-replay.py --run` (`e2e-early`, `e2e-stderr`, `e2e-big`): results in F1 and section 2.

## 5. Recommended corrections (none applied; no production file was edited)

1. F1: in `tools/registry-replay.py`, move the bound check before the `observations.json` write (or write a size-only refusal record), and correct the docstring at line 9. Add a selftest that runs `run_replay` against a row over the bound and asserts that no stream bodies reach `--out`. Scope is the main agent's call.
2. F2: one-line docstring fix at `tools/registry-check.py:36-37`.
3. No change to `tools/command-binding.py` or to the frozen rows is needed for this item.

R23-REATTACK OutputComplete: FINDING
