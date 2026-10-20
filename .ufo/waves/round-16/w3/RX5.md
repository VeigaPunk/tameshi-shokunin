# RX5 — cold-read re-read, round-15 gate/probe registry (SKILL.md:1676-1706)

Page snapshot: `git show 05a224754db3c6fce18f5ec1816a6873bffe3d0e:SKILL.md`, sha256
`e289acec4e90c994d303b2dd6c844d907dc1bf48330ecd2fd253ac7379f794b3` — **verified**
(`git show … | sha256sum`). Page is 1807 lines. Range read: 1676-1706 (heading 1676 through
the blank at 1706); section evidence lines 1676-1705.

Only this range plus what it names was opened. Scratch: `/tmp/tameshi-r16w2-RX5-RwhLeE`
(lane tree extracted with `git archive 05a2247 | tar -x`; archived root extracted with
`git archive 28aeef4 | tar -x`).

## Commands executed (exactly as written in the registry, from the /tmp copy)

### Row 1 — retained invocation-context gate

| Command | Exit | Key output |
|---|---|---|
| `python3 tools/context-capture.py --check` | **0** | `CONTEXT: OK (id=context_consistent receipt=.ufo/evidence/round-14/context-receipt.json sha256=05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a exit=0 findings=0)` |
| `python3 tools/context-capture.py --selftest` | **0** | `SELFTEST: PASS (49/49)`, incl. `tampered-before-semantic`, `probe-source-lie`, `duplicate-key`, `usage-unknown-flag`, `hermetic-no-lane-path`, `hermetic-temp-only` |
| `python3 tools/context-capture.py --check --receipt .ufo/evidence/round-15/frozen/context-missing-env/receipt.json --expected .ufo/evidence/round-15/frozen/context-missing-env/expected.json` | **1** | `CONTEXT: MISMATCH (id=missing_injected_environment … findings=2)`; `receipt.environment.injected_env is absent` |
| `python3 tools/context-capture.py --help` | **0** | usage text, no `CONTEXT:` verdict line (non-verdict) |
| `python3 tools/context-capture.py --check --receipt X` (expected omitted) | **64** | `CONTEXT: USAGE_ERROR (id=usage_error exit=64)` |
| `python3 tools/context-capture.py --bogus` | **64** | `unknown argument: --bogus` → `USAGE_ERROR (id=usage_error exit=64)` |

Pinned values verified:
- `.ufo/evidence/round-14/context-receipt.json` sha256 = `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` — **exact match**.
- negative fixture `.ufo/evidence/round-14/context-missing-env.json` sha256 = `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208` — **exact match** (same sha as `.ufo/evidence/round-15/frozen/context-missing-env/receipt.json`).
- built-in pin in tool: `FROZEN_RECEIPT_REL`, `FROZEN_RECEIPT_SHA256` (same 05cb…), `FROZEN_TOOL_SHA256` = `7313e9a2…` which equals the receipt's recorded `tool_sha256`, `FROZEN_EXPECTED_ID=context_consistent`, `FROZEN_EXPECTED_EXIT=0` (`tools/context-capture.py:151-158`).
- expected-pin schema `tameshi-context-expected-v1`, four keys incl. `receipt_sha256`/`id`/`exit` (`EXPECTED_SCHEMA`, `tools/context-capture.py:141`; help text). My generated pins of this schema were accepted and honoured.

Write-scope claims, each observed:
- `--check` opens the receipt exactly once, only under the /tmp copy:
  `openat(AT_FDCWD, "/tmp/…/lane/.ufo/evidence/round-14/context-receipt.json", O_RDONLY|O_CLOEXEC) = 3`.
- zero opens under the recorded roots: `grep -c '/home/vgpnk/Projects/shokunin' trace` = **0**.
- own-source read for the reported digest: strace shows `openat(…/tools/context-capture.py) = 3`; `--check --json` reports `tool_sha256=c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726`, equal to `sha256sum tools/context-capture.py`.
- no stored-argv execution: sole `execve` is `python3 tools/context-capture.py --check`; no other execve.
- writes nothing: full-tree `find -printf '%p %s %T@'` diff before/after check+disposition runs → identical (`TREE_UNCHANGED`); archived root likewise `ARCH_TREE_UNCHANGED`.
- selftest fixture isolation: `SELFTEST_CASE hermetic-temp-only OK no unexpected temp-root entries`; temp root removed in `finish()`.

### Row 2 — effective expectation disposition

| Command | Exit | Key output |
|---|---|---|
| `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` | **2** | `{"id":"expected_input_digest_mismatch","exit":2,"status":"could_not_evaluate"}`; detail `tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…` |
| `python3 tools/evidence-disposition.py --selftest` | **0** | `SELFTEST: PASS (34/34)` |
| archived-root form: `git archive 28aeef4 | tar -x` → `python3 tools/evidence-disposition.py --root ../arch --dispositions .ufo/evidence/round-14/dispositions.json --json` | **0** | `"status":"clean"`, `counts {effective:11, superseded:1, passed:11, failed:0, findings:0}`, `expected_inputs_verified` length **13**, `expected_file .ufo/evidence/round-13/expected.json` |
| `python3 tools/evidence-disposition.py` (no args) | **64** | usage text, exit 64 |
| `python3 tools/evidence-disposition.py --root . --dispositions /tmp/nonexistent-dispositions.json --json` | **2** | `{"id":"dispositions_missing","exit":2}` |
| `python3 tools/evidence-disposition.py --bogus` | **64** | `unknown argument: --bogus` |
| two independent semantic-failure fixtures (row dropped; row `check` renamed) against the archived root | **1 / 1** | `EVIDENCE_DISPOSITION: failed exit=1 …` with `row_missing`, then `effective_check_name_mismatch` + `receipt_check_missing` |

"the runner input moved" is concretely true and round-16-dated:
`sha256sum` of `tools/mutate-and-run.sh` = `75ed934d…` at `28aeef4` vs `0673d2e5…` at `05a2247`;
`git log 28aeef4..05a2247 -- tools/mutate-and-run.sh` shows the two round-16 commits
(`c699c8c`, `05a2247`), and `git diff --stat` is 121 insertions / 24 deletions.
`28aeef4` is an ancestor of `05a2247` and a round-15 commit.

Pinned values verified: `dispositions.json` sha256 `77faac58…` is identical in the lane copy and
the `28aeef4` extraction; the "before counterpart" `.ufo/evidence/round-14/dispositions-before.json`
exists with the same `evidence-dispositions-v1` schema; the "13 original inputs" count is exactly the
13 entries in `expected_inputs_verified` (4 round-12 + 4 round-13 + 5 tools).

## Limit/record paragraphs (1683-1691, 1693-1699, 1701-1705)

Re-checked at this revision; each holds:
- "configured authority, not cryptographic proof" — the frozen pins are literal constants
  (`FROZEN_*`, `tools/context-capture.py:151-158`); comparison is `receipt["tool_sha256"] !=
  FROZEN_TOOL_SHA256` (`:1212`); no signature/authentication step exists. Consistent.
- "never a re-execution of stored argv and never a fresh measurement" — strace: one receipt open,
  zero recorded-root opens, no extra execve (above).
- "archived round-12–14 bytes" unchanged: `git diff --name-status 28aeef4 05a2247 --
  .ufo/evidence/round-12 .ufo/evidence/round-13 .ufo/evidence/round-14` → empty.
- "no sibling gate is registered or executed" — both rows name lane-local `tools/` entries; the
  disposition run verifies only lane evidence and lane tools. Consistent.
- "Paths can follow filesystem symlinks": symlinked receipt
  (`link-neg.json -> .ufo/evidence/round-15/frozen/context-missing-env/receipt.json`) produced the
  identical verdict `missing_injected_environment`/exit 1 with the same sha `1ee9d0…`.
- "Explicit mode reads caller-selected files with caller permissions": `chmod 000` receipt →
  `CONTEXT: INVALID (id=receipt_unreadable … exit=2)`, `cannot read receipt: Permission denied`.
- "Could-not-evaluate takes precedence": a valid-format but wrong `receipt_sha256` pin against the
  clean receipt gave **exit 2** `snapshot_tampered` with `expected_verdict_mismatch` listed second
  (expectation disagreement secondary). Missing receipt → exit 2 `receipt_missing`, same ordering.
- "A clean result with a wrong id/exit pin becomes failed/exit1": exit **1**
  `expected_verdict_mismatch` for both a wrong exit (`exit=1`) and a wrong id
  (`missing_injected_environment`) pin on the clean receipt.
- "Help exits0 only as a non-verdict informational mode": exit 0, no `CONTEXT:` line.
- "selftest exits0/1/2 … and64": observed 0 (pass) and 64 (`usage-selftest-extra`); source
  `finish()` returns 1 on any failed case and `run_selftest` returns 2 on setup exception
  (`tools/context-capture.py:1762-1791`, `2193-2205`).

## Findings

No blocking or minor defect found in this range. Every entry command, self-test command, pinned
digest, verdict-map row and write-scope sentence was reproduced as written, including the two
special forms the registry now spells out (`--root .` → exit 2 `expected_input_digest_mismatch`
by design; archived `28aeef4` root → exit 0 clean).

Residual risk / verification gaps (not defects):
- The count "six recorded cases" in the 1683-1691 paragraph is a cross-reference outside this range
  and was not verified (cold-read contract forbids opening the sections that own it); the
  non-change assertion itself is supported — this registry section registers no case row.
- The selftest exit-1 and exit-2 arms were verified from source, not triggered end to end (a
  case-failure or setup-inability selftest run cannot be induced without editing the tool).
- "race-free confinement boundary" is a declared limit, not a claim; no race test was attempted.
- All tools were run from `/tmp` copies of the committed bytes; the live lane worktree was not
  executed against and not modified (`git --no-optional-locks status --porcelain` shows only
  pre-existing user modifications outside my writes).

**Verdict:** executed-ok — every registry command, pin and exit-class claim in lines 1676-1706
reproduces exactly at `05a2247`; no gap found.

```json
{"seat":"RX5","skill_sha256":"e289acec4e90c994d303b2dd6c844d907dc1bf48330ecd2fd253ac7379f794b3","sections":[{"start":1676,"heading":"### Round-15 gate/probe registry","class":"instruction","verdict":"executed-ok","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":[],"commands_executed":["python3 tools/context-capture.py --check","python3 tools/context-capture.py --selftest","python3 tools/context-capture.py --check --receipt .ufo/evidence/round-15/frozen/context-missing-env/receipt.json --expected .ufo/evidence/round-15/frozen/context-missing-env/expected.json","python3 tools/context-capture.py --help","python3 tools/context-capture.py --check --receipt X","python3 tools/context-capture.py --bogus","python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json","python3 tools/evidence-disposition.py --selftest","python3 tools/evidence-disposition.py --root ../arch --dispositions .ufo/evidence/round-14/dispositions.json --json","python3 tools/evidence-disposition.py","python3 tools/evidence-disposition.py --root . --dispositions /tmp/nonexistent-dispositions.json --json","python3 tools/evidence-disposition.py --bogus","python3 tools/evidence-disposition.py --root ../arch --dispositions ../disp_dropped.json","python3 tools/evidence-disposition.py --root ../arch --dispositions ../disp_badcheck.json","strace -f -e trace=openat,execve python3 tools/context-capture.py --check","sha256sum .ufo/evidence/round-14/context-receipt.json .ufo/evidence/round-14/context-missing-env.json","git archive 28aeef4 | tar -x","git diff --name-status 28aeef4 05a2247 -- .ufo/evidence/round-12 .ufo/evidence/round-13 .ufo/evidence/round-14","git log 28aeef4..05a2247 -- tools/mutate-and-run.sh"],"opened":["SKILL.md:1676-1706 at 05a2247","tools/context-capture.py (named by range)","tools/evidence-disposition.py (named by range)","tools/mutate-and-run.sh (digest only, named by dispositions detail)",".ufo/evidence/round-14/context-receipt.json (named by range)",".ufo/evidence/round-14/context-missing-env.json (named by range)",".ufo/evidence/round-14/dispositions.json (named by range)",".ufo/evidence/round-14/dispositions-before.json",".ufo/evidence/round-15/frozen/context-missing-env/{receipt,expected}.json"],"scratch":"/tmp/tameshi-r16w2-RX5-RwhLeE"}]}
```
