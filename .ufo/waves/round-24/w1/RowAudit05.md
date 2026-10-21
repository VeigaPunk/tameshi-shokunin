# RowAudit05 — round24 replay: five-row requirement/receipt/token audit

**Verdict: no false acceptance found in any of the five assigned rows.** Requirement objects are
byte-identical to the round-23 freeze, every receipt (`runner_result`) reports `got == expect`,
`held: true`, no cleanup error, no missing token, and every required stdout token is present in
the retained full stdout. The replay ran at `d2eaecd443bf5f4e387e7e5331282e3d11dea047`, which is an
**ancestor** of the delivered revision `c8c5b88c8e961a929cdc351b95a7074c76958909`, and every
row-relevant blob (the five tools, `tools/registry-check.py`, `tools/registry-replay.py`,
`tools/command-binding.py`, `tools/registry.json`) is byte-identical across the two revisions, so
the receipts transfer to the delivered revision. Two rows carry temperature/summary evidence that
this run is a fresh execution rather than a copy of round 23. Residual findings below are
calibration weaknesses in *token* strength and in what `held` means after projection; none of them
makes today's acceptance false.

Scope: `bash-witness-selftest`, `context-capture-frozen`, `assemble-round16-selftest`,
`measure-round18-selftest`, `env-diff-selftest`.

## Axes walked

1. Requirement fidelity — `observations.row.requirement` vs `.ufo/evidence/round-23/requirements.json`,
   vs `.ufo/evidence/round-23/registry-baseline.json`, vs `tools/registry.json` at both revisions.
2. Receipt fidelity — `runner_result` exit / full stdout / held, and byte congruence with the
   published bundle receipts (and the observed `stdout_tail`/`stderr_tail`).
3. Token semantics — is each required token actually discriminating, or is it emitted on a failing
   path too (echo/prefix)?
4. Provenance — frozen input digests, clone/runner digests, revision ancestry, freshness.

## Provenance chain (observed)

- Frozen inputs: `.ufo/evidence/round-23/requirements.json` sha256
  `cd5205be9e5843e956191f673e620875f6f9c65a4c8ed9f224e656601a25a1e3`;
  `registry-baseline.json` sha256 `ebd2e69a6c63e9c212152ea18050781ab686b0cbdaead4bb0fcbbd54d0fec92a`,
  equal to `requirements.json.registry_sha256`. Git blobs are identical at `d2eaecd`, `c8c5b88`
  and the worktree (`96fe8e50…`, `9315c7e8…`).
- `run_replay` refuses a baseline-digest mismatch and a frozen-vs-baseline requirement
  difference before running anything (`tools/registry-replay.py:140-152`), clones from the live
  lane and re-checks clone HEAD (`:153-160`), and takes the runner from the clone copy (`:163-168`).
- Runner identity: `git show d2eaecd:tools/registry-check.py | sha256sum` =
  `cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad` = `observations.runner_sha256_clone_copy`.
  Instrument identity: live `tools/registry-replay.py` sha256 =
  `9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714` =
  `replay-command.json.instrument_sha256`; `tools/command-binding.py` =
  `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d` = the gate's `tool_sha256`.
- Revision: `git merge-base --is-ancestor d2eaecd c8c5b88` → true;
  `git diff --stat d2eaecd c8c5b88` lists 26 files, all under `.ufo/evidence/` (+6019/−0), no
  tool changed. Requirement set is unchanged across all three row sources (baseline, replay rev,
  delivered rev): all five rows `status=active`, same argv, same expect.
- Requirement binding completeness: the bundle's 43 `requirements` are **identical** to the 43
  entries of `requirements.json` (whole-object equality), and all 43 bundle receipts are field-wise
  identical to the 43 observation rows (`argv`, `cwd`, `revision`, `exit`, `stdout`, `stderr`);
  name sets are equal and unique. No extra/missing row.
- Freshness: `measure-round18-selftest` prints scratch
  `/tmp/tameshi-r17-MeasureV2-ihzdp654` here vs `…-kwa2esv8` in round 23; `assemble-round16-selftest`
  stderr references `/tmp/assemble-selftest-3kj4mbv1/` vs `…-fegd019w/` in round 23. The other
  three outputs are deterministic (no temp paths) and match round 23 byte-for-byte. `replay-command.json`
  stdout carries one line per row; all five read `0 True`.
- Timing: interval durations equal `elapsed_s` to 1 ms (0.475/0.300/0.377/5.943/0.655 s), all inside
  the recorded run window 15:56:41.108–16:01:02.124Z.
- Gate cross-check (read-only recomputation of `command-binding.evaluate()` over the published
  artifacts, not a gate execution): zero findings; `sha256(bundle.json)` =
  `4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6` = `expected.json.bundle_sha256`
  = `replay-gate.json` reported digest. The gate's `exit 0 / finding_ids []` is arithmetically
  corroborated.

## Per-row result

| row (requirements.json line) | frozen requirement | receipt | tokens | decisive evidence |
|---|---|---|---|---|
| `bash-witness-selftest` (`:68`) | `python3 tools/bash-witness-study.py selftest`, exit 0, `WITNESS_SELFTEST:` | got 0 / held true / stderr 0 B | 1/1 | 51 ` ok` check lines + 51 `check` lines (no FAIL verdict), final `WITNESS_SELFTEST: 51/51 pass`, `VERDICT: PASS`; exit plumbing `tools/bash-witness-study.py:1228-1239,1711-1718` |
| `context-capture-frozen` (`:197`) | `python3 tools/context-capture.py --check --json`, exit 0, `context_consistent` | got 0 / held true / stderr 0 B | 1/1 (2 occurrences) | 626 B JSON: `"status": "ok"`, `"findings": []`, `"id": "context_consistent"`, `"verdict_matches_expected": true`, receipt sha256 `05cb55b8…` == pin and == blob at both revisions (`05cb55b8` worktree/`d2eaecd`/`c8c5b88`); receipt-declared `tool_sha256 7313e9a2…` == `FROZEN_TOOL_SHA256` (`tools/context-capture.py:151-158`) |
| `assemble-round16-selftest` (`:319`) | `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest`, exit 0, `SELFTEST: all checks passed` | got 0 / held true / stderr 2391 B | 1/1 | 38 `[ok]`, 0 `[FAIL]`, final `SELFTEST: all checks passed`; exit 1 on any failure (`assemble.py:645-649,996-1001`); the 2391 B stderr is 4 `ERROR:` / 5 `REJECTED` / 5 `SKIPPED` / 5 `WARNING`, every line a `/tmp/assemble-selftest-3kj4mbv1/` negative-case fixture matched by an `[ok]` case |
| `measure-round18-selftest` (`:431`) | `python3 .ufo/evidence/round-18/measure.py --selftest`, exit 0, `MEASURE_SELFTEST: ` | got 0 / held true / stderr 0 B | 1/1 | 98 `PASS` lines, 0 FAIL lines, tally `MEASURE_SELFTEST: 98/98 pass (scratch /tmp/tameshi-r17-MeasureV2-ihzdp654)`; exit 1 when any check fails (`measure.py:926-928,1498-1502`) |
| `env-diff-selftest` (`:543`) | `python3 tools/env-diff.py --selftest`, exit 0, `ENVDIFF_SELFTEST: 9/9 pass` | got 0 / held true / stderr 0 B | 1/1 | 9 `ENVDIFF_CASE … PASS` lines, tally `ENVDIFF_SELFTEST: 9/9 pass`; exit 1 unless all 9 pass (`tools/env-diff.py:145-147,192-195`) |

Rows in `observations.json` at lines 248/636/1009/1361/1713; corresponding bundle requirements at
66/184/299/403/507 and receipts at 664/793/915/1027/1139.

## Findings (none is a false acceptance)

**F1 — Three of five tokens are non-discriminating; the verdict rests on the exit code alone.**
- `context-capture-frozen`: `context_consistent` is *guaranteed* to appear even on a failing
  verdict. `make_result` always emits the pinned `expected` object
  (`tools/context-capture.py:1277-1281`), and frozen mode always supplies it (`:1342-1352`), while a
  mismatch run replaces only the top-level `id` with a finding id and exits 1. So the token adds
  zero power on top of `expect.exit: 0`. A failing run is still caught — by `EXIT_MISMATCH` — so
  no false acceptance, but the requirement is exit-only in substance.
- `bash-witness-selftest` and `measure-round18-selftest` require only a summary *prefix*
  (`WITNESS_SELFTEST:`, `MEASURE_SELFTEST: `). Both print that prefix on failure too
  (`bash-witness-study.py:1711-1718`; `measure.py:1500-1502`) and then exit 1, so again only the
  exit code discriminates. By contrast `env-diff-selftest` (denominator `9/9 pass`) and
  `assemble-round16-selftest` (`SELFTEST: all checks passed` vs `SELFTEST: FAIL (n checks)`) are
  genuinely verdict-discriminating tokens.

**F2 — `held` is derived, and it is dropped before publication.** `held` is not an execution
attestation: it is `got == expect and not missing and cleanup_ok` (`tools/registry-check.py:648-728`,
specifically `:720`). `project()` consumes it to refuse publication (`RUNNER_NOT_HELD`,
`tools/registry-replay.py:89-94`) but copies only name/argv/cwd/revision/exit/stdout/stderr into the
receipt (`:110-113`). Consequences: (a) bundle publication *implies* every row held at projection
time, but a bundle consumer cannot re-verify hold, timeout absence or cleanup success; (b) the
`command-binding` gate therefore sees exit + token only, which its own docstring states
(`tools/command-binding.py:10`). For my five rows the implication is satisfied and consistent
(`held: true`, no `cleanup_error`, no `stdout_missing`, `stdout_tail` is a true suffix). This is a
retention gap, not an incorrect accept.

**F3 — The gate's "trusted commitment" is produced by the same instrument in the same run.**
`publish()` writes `expected.json` next to `bundle.json` (`tools/registry-replay.py:129-136`), so
`SNAPSHOT_TAMPERED`/digest agreement proves internal consistency, not an independent caller
commitment. Independent value comes from re-deriving the semantic checks: my read-only
recomputation of `evaluate()` over all 43 rows returns no findings, and the requirement set equals
the frozen round-23 file exactly. Treat `replay-gate.json` as corroborating, not authoritative.

**F4 — No executed-artifact digest is pinned for 4/5 rows.** Receipts carry argv + revision, not the
sha256 of the script that ran. `context-capture-frozen` at least prints a runtime self-hash
(`c4a1d165…`, which is *not* compared to any expected value), but bash-witness/assemble/measure/env-diff
print nothing equivalent. A same-revision substitution of a selftest body that reproduces the token
and exit would be invisible in the bundle. This is producer-side (K6-adjacent), outside this
evidence's claim, and cannot be repaired by editing the evidence after the fact.

**F5 — Do not cite this replay as running at the delivered revision.** `observations.revision` is
`d2eaecd`, not `c8c5b88`. It is valid for `c8c5b88` only because the row-relevant blobs are
identical (verified per path) and `d2eaecd` is an ancestor.

**F6 — `assemble-round16-selftest` writes 2391 B of `ERROR`/`REJECTED`/`WARNING` to stderr while
exiting 0.** Every line maps to an intentional negative case (`[ok] heading mismatch exits 2`,
`bad-sha report rejected`, `non-report glob hit skipped`, `class disagreement -> instruction`,
`relaxing override rejected`, `equal-rank override rejected`, `wrong-sha replace rejected`), so
none is a hidden failure. But the requirement pins stdout+exit only; a future unexpected stderr
error on a green run would go unnoticed.

## Falsification attempts (what I attacked and the outcome)

1. *Receipt is a copy of round-23.* Refuted for two rows by fresh mkdtemp suffixes
   (measure `ihzdp654` vs `kwa2esv8`; assemble stderr `3kj4mbv1` vs `fegd019w`); the deterministic
   three cannot be distinguished this way and are reported as such.
2. *Receipt/stdout disagreement between observations and bundle.* None: all 43 rows field-identical.
3. *Requirement drift (row superseded/rebound in round24 registry).* None: all five are `active`
   with identical argv/expect in baseline, `d2eaecd` and `c8c5b88`.
4. *Token supplied by an error path.* True for three rows (F1) — but each such path exits nonzero,
   so the requirement's exit pin still rejects it. No token is satisfied by stderr: receipts bind
   stdout only, and command-binding has a `stderr-cannot-supply-token` selftest case.
5. *`held: true` unearned.* `held` recomputes exactly from the retained fields for all five
   (exit match, token present, no cleanup error); `stdout_tail` is a genuine suffix (streams are
   under `TAIL_BYTES=4096`/`--max-stream-bytes=1 MiB`, no truncation marker).
6. *Token appears only because the harness echoes expectations elsewhere.* Checked for
   context-capture and confirmed by source (F1); also checked that counts are exactly as expected
   (`context_consistent` ×2 = id + expected.id; others ×1).
7. *Selftest harness lies about failures.* All four harnesses record a false result and drive a
   nonzero exit (`bash-witness-study.py:1231-1238`, `measure.py:926-928`, `env-diff.py:145-147`,
   `assemble.py:645-649`); observed outputs contain no FAIL/PASS contradiction (the single `FAIL`
   substring in bash-witness stdout is the *check name* "check FAIL without denominator is
   inconclusive, not a crash ok").
8. *Gate claim disagrees with artifacts.* Independent recomputation finds zero violations, matching
   `replay-gate.json`.

## Smallest safe correction

No evidence edit is warranted for this wave. If a later contract is opened (per the K5/K6 bound,
changing a row or bundle chooses a new contract), tighten the three weak tokens so failure paths
cannot satisfy them: `context-capture-frozen` → add `"verdict_matches_expected": true` (or
`"findings": []`); `measure-round18-selftest` → `MEASURE_SELFTEST: 98/98 pass`;
`bash-witness-selftest` → `WITNESS_SELFTEST: 51/51 pass` plus `VERDICT: PASS`. Optionally retain
`held`/`cleanup_ok` in the receipt so a bundle consumer can see the projection's hold decision.
Do not apply any of this inside round 24: it would invalidate the frozen baseline digest
`ebd2e69a…` and the bundle pin `4f424023…`.

Tool installs/upgrades: none. No production file, gate, battery or selftest was executed; all
commands were read-only inspection (sha256, jq/python JSON comparison, `git show/rev-parse/diff`).
