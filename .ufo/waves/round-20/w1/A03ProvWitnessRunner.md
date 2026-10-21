# A03ProvWitnessRunner — witness runner re-open at 4b7c682

Seat: TameshiR20-3.A03ProvWitnessRunner (executor, leaf). Scope: re-open `tools/mutate-and-run.sh` at `4b7c682`, verify its sha256 against the declared witness-runner instrument `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b`, and report (1) mutation semantics, (2) the `--regression` mode, (3) the exact argv a witness receipt would need. Read-only: `git show`/`git log` queries and evidence reads only; no lane file except this report; no tool executed (execution belongs to the B-seat executors).

## 1. Identity verification — PASS

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ git show 4b7c682:tools/mutate-and-run.sh | sha256sum
d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b  -
$ sha256sum tools/mutate-and-run.sh
d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b  tools/mutate-and-run.sh
```

Observed: exact match, both at `4b7c682` and in the working tree. Further anchors, all observed:

- `git merge-base --is-ancestor 4b7c682 HEAD` → ok; HEAD = `6fd220bce3705498d1d1054e99e3cae73c203751` (the frozen contract commit). `4b7c682` full id: `4b7c6823a462f5ea2eafcb262275300a545f3ed7` (matches the revision recorded in the round-19 witness receipts).
- `git log --format='%h %ad %s' -1 4b7c682` → `4b7c682 2026-10-20 18:49:16 -0300 round-18: measured SCORECARD depth7→8 …`. That commit's stat touches only `.ufo/evidence/round-18/*`, `LOG.md`, `SCORECARD.md` — it does **not** touch the tool.
- `git log --oneline 58e5d53..4b7c682 -- tools/mutate-and-run.sh | wc -l` → `0`: the blob is unchanged from the round-18 build landing `58e5d53` (2026-10-20 17:20:09 -03) through `4b7c682`, the working tree, and the frozen contract commit.
- `git show 4b7c682:tools/mutate-and-run.sh | wc -c` equivalent: recorded receipts size the blob at 97200 bytes (`.ufo/evidence/round-19/source-131.stdout:133`: `SOURCE tools/mutate-and-run.sh sha256=d22c4025… bytes=97200`), consistent with the 1940-line file read.

**Per-commit instrument-sha chain (observed via `git show <c>:tools/mutate-and-run.sh | sha256sum`):**

| commit | blob sha256 (16-hex prefix) | era |
|---|---|---|
| 53e74a8 | d8abee522efbf27c | probation r3 (introduced) |
| b58b26f | 597e141989065e03 | probation r4 |
| 4494715 | b56c6e57f1b7ae91 | probation r6 |
| 9f1d3c3 | cf41efaa8be5f52d | probation r7 (the `cf41efaa…` cited in round-16 SKILL snapshot) |
| 606716f | 75ed934dc86360f5 | probation r10 (the sha on every round-12 / kaika-round-1 receipt) |
| c699c8c | 89722ddb3082abd6 | round-16 |
| 05a2247 | 0673d2e5374b94c6 | round-16 wave-2 |
| 2a22ade | fb6d86d59b5c9285 | round-17 |
| 58e5d53 | **d22c4025e8ce38b8** | round-18 → unchanged through 4b7c682 / working tree / 6fd220b |

This table is the evidence for the rider "name each historical instrument sha": the witness runner has had nine identities; `d22c4025…` is only the round-18+ identity. A receipt-time instrument-sha gate keyed to a singular "frozen SHA" is wrong for any pre-58e5d53 receipt — e.g. `.ufo/evidence/round-12/runner-regression.txt` and the kaika-round-1 receipts all carry `REGRESSION_TOOL:/MUTATE_TOOL: … sha256=75ed934d…`.

## 2. Mutation semantics (run mode)

From the header/usage and the verified code at 4b7c682 (`run_sweep`, `run_one`, `py_helper`, `selftest` assertions):

- **Inputs (all required, else exit 64):** `--target FILE`, `--defects SPEC`, `--suite CMD`; options `--workdir DIR`, `--label NAME`, `--timeout N` (default 300), `--tail N` (default 8).
- **Method — inject → run → restore, target never written.** Fail-closed order (verified in `run_sweep`): (1) copy target to a pinned pristine (`cp -p`), pin both sha256s, refuse on read race (`TARGET_SHA0 != PRISTINE_SHA` → SETUP); (2) parse the spec; (3) pre-build **every** mutant as a fresh byte copy of the pristine plus one exact edit, asserting `@old` occurs exactly once — any failure exits 2 (`MUTATE: SETUP`) before a single suite run; (4) control run on the pristine must be green (`CONTROL: GREEN (exit=0 …)`), a red control is `MUTATE: SETUP` exit 2 (kills could not be attributed); (5) per-defect runs; (6) restore proof — target **and** pristine re-hashed, `MUTATE_RESTORE: OK` or `DRIFT` (drift → exit 2); (7) kill-rate summary.
- **Defect spec v1:** `@defect <id> | <desc>` (id `[A-Za-z0-9._-]+`, unique), `@old <text>` (required, non-empty), `@new <text>` (may be empty). Escapes `\n \t \r \\` only; any other backslash sequence refused; CR/CRLF specs refused; `@new == @old` (no-op) refused; duplicate `@old`/`@new` refused; incomplete defects refused. Edits are byte-exact (`python3` helper, UTF-8 encode/decode with binary write).
- **Suite contract:** run as `bash -c CMD` under `timeout N`, stdin `</dev/null`, from the caller's CWD, with `MUTANT` (artifact under test), `TARGET`, `PRISTINE`, `WORKDIR`, `DEFECT_ID` (`CONTROL` for the control run) exported.
- **Verdict mapping (exit-code oracle):** 0 → `SURVIVED`; 124 → `INCONCLUSIVE (note=timeout)`; 126/127 → `INCONCLUSIVE (suite not runnable)`; any other non-zero → `KILLED`.
- **Kill-rate:** integer half-up `pct=(200*killed+total)/(2*total)`; final line `MUTATE: DONE (target=… defects=N killed=k survived=s inconclusive=0 kill-rate=P%)` or `MUTATE: DEGRADED (… inconclusive≥1 …)` when any run was inconclusive.
- **Exit map:** 0 done · 1 done-with-inconclusive (DEGRADED) · 2 setup/refusal · 64 usage error.
- **Receipt lines:** `MUTATE_TOOL: <SELF path> sha256=<sha of the runner itself>` / `MUTATE_DATE` / `MUTATE_TARGET … sha256=… bytes=…` / `MUTATE_SPEC … defects=N` / `CONTROL:` / `DEFECT <id>: …` per defect / `MUTATE_RESTORE:` / `MUTATE_EVIDENCE: <workdir>` / `MUTATE:` summary. Evidence workdir (default `mktemp -d /tmp/tameshi-r4-2-run.XXXXXX`) keeps pristine, per-mutant copies, `evidence/<id>.out`, `evidence/control.out`, `defects.tsv`, `results.tsv` (id/verdict/exit/duration-ms/mutant-sha256/desc), `spec.copy`.
- A low kill count is a report finding, not a tool failure (bands are a report convention, not a gate).

## 3. Regression mode (`--regression`)

The fleet leg ledger (r4-2 origin; r7-1 git-pinned replay; r10-2 six legs; r16 seven; r18 eight):

- **Eight legs, each with a byte pin, a revision pin, an embedded spec, and a recorded verdict table as the exact expectation:** js-kimi-census 8/10, bash-surface-census 8/10, bash-tsukuroi-census 6/10, bash-mado-verify 4/10, bash-checklist-run 7/15, js-claims-check 7/10, js-round-gate 5/10, js-sources-check 5/10.
- **Drift immunity:** the target is never read from a working tree; each leg is materialized via `git show <rev>:<path>` from its own repo's object store into the case workdir, its sha256 must equal the recorded `PIN_*`, and the blob mode is mirrored (`100755 → chmod +x`, needed by self-re-exec gates; `100644` stays). Missing repo/rev/blob or pin mismatch → `SETUP (…)` exit 2, never a pass.
- **r17 guards in this blob:** repo-identity guard (the leg's repo must be its own `git rev-parse --show-toplevel`; a `.git`-less dir inside a super-repo is refused `repo_identity_mismatch`) and the `GIT_*` scrub (`git_clean` unsets every caller-exported `GIT_*` for all git calls, so an exported `GIT_DIR`/`GIT_WORK_TREE` cannot redirect materialization or the sweep — proven by the selftest canary and the two "cannot redirect" checks seen in the round-19 witness selftest stdout).
- **Exact expectation:** killed-delta 0, flips 0, defect count exactly the recorded count, inconclusive 0, control green, restore OK. The r4-2 tolerance (`|killed-recorded| ≤ 1`, ≤ 1 flip) remains only for fixture-mode cases exercised by `--selftest`.
- **Mechanics:** each leg is a full CLI sub-invocation of the same tool over the materialized copy; fleet trees are never written; scratch root `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`, removed on PASS unless `--keep`, kept on FAIL/SETUP; `--workdir DIR` honored; `--target/--defects/--suite/--label` refused (exit 64).
- **Exit map:** 0 all legs PASS · 1 ≥ 1 leg FAIL · 2 cannot-verify (missing repo/rev/blob, pin mismatch, setup refusal) with no FAIL.
- **Receipt lines:** `REGRESSION_TOOL: <SELF> sha256=<runner sha>` / `REGRESSION_DATE` / `REGRESSION_BAND` / `REGRESSION_EXPECT` / `REGRESSION_PIN ×8` (git source + pinned sha + mode) / `REGRESSION_SWEEP ×8` / `REGRESSION_TABLE ×8` / `REGRESSION_DEFECT` rows only on diffs / `REGRESSION_WORKDIR` / `REGRESSION: PASS|FAIL|SETUP (…)`.
- **Dependencies (checked, SETUP refusal if missing):** bash, python3, sha256sum, mktemp, timeout, cp, date, git.
- `FLEET_ROOT` is derived as three `dirname`s off the resolved `SELF` path — for the lane install `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` it resolves to `/home/vgpnk/Projects/shokunin`, where the four sibling repos must exist. An isolated scratch clone receipt (the round-19 receipts use `cwd_kind: "isolated scratch clone"`) must therefore reproduce the fleet layout (`<root>/tameshi-shokunin/tools/…` plus sibling repo dirs with the pinned revisions in their object stores) or legs SETUP-refuse.
- `--selftest` (third mode) is hermetic under `/tmp/tameshi-r4-2-selftest.XXXXXX`: fixture kill/survivor/refusal/DEGRADED arms, the regression engine on fixtures (in-band, band-edge, doctored table, pin/revision SETUP), the GIT_* scrub canary, repo-identity arms, exec-bit mirror arms, and embedded-ledger consistency (leg-count agreement: 8 call sites = 8 spec files = `nlegs=8`; per-leg spec/table id and count agreement). Prints `MUTATE_SELFTEST: N/N pass` + `VERDICT: PASS|FAIL`; scratch removed on PASS, kept on FAIL.

## 4. Exact argv a witness receipt would need

Two receipt shapes exist in this lane's evidence; both observed:

**(a) Witness-study receipt (the shape round-18/19 actually used).** The witness *tool* is `tools/bash-witness-study.py` (`8dfaa25a…`, the declared witness-tool) and the witness *runner* is `tools/mutate-and-run.sh` (`d22c4025…`), whose identity the receipt records as `runner_sha256`. The corrected, complete receipt `.ufo/evidence/round-19/bash-witness-selftest-complete.json` records:

```json
"argv": ["python3", "tools/bash-witness-study.py", "selftest"],
"revision": "4b7c6823a462f5ea2eafcb262275300a545f3ed7",
"tool_sha256": "8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12",
"runner_sha256": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b",
"cwd_kind": "isolated scratch clone", "exit": 0,
"stdout_sha256": "316b9713…", "stderr_sha256": "e3b0c442…(empty)"
```

with terminal stdout `WITNESS_SELFTEST: 43/43 pass` / `VERDICT: PASS`. **The argv must be the subcommand form `selftest` — not `--selftest`.** The round-18 receipt (`.ufo/evidence/round-18/final/checks.json#bash-witness-selftest`) recorded the flag form `python3 tools/bash-witness-study.py --selftest` and got **exit 64 with empty stdout** (usage error); the round-19 re-open superseded it twice (bash-witness-selftest.json exit 1, then -complete exit 0), preserving all historical receipts (`historical_receipt_preserved: true`, `supersedes` chain). A round-20 receipt gate must therefore check argv form + `exit == 0` + the terminal verdict line; an exit-64 receipt is not a passing witness. The study tool itself refuses on runner drift (`runner-drift tools/mutate-and-run.sh sha256=… committed=…`), so `runner_sha256 == d22c4025…` is enforced, not decorative.

**(b) Direct runner invocation (if the runner itself is the witnessed instrument).** Per its usage, exactly one of:

- `bash tools/mutate-and-run.sh --selftest` — hermetic, no fleet access; verifies the engine and the eight-leg embedded-ledger consistency.
- `bash tools/mutate-and-run.sh --regression [--workdir DIR] [--keep]` — the eight-leg fleet ledger replay; no other mode flags allowed.
- `bash tools/mutate-and-run.sh --target FILE --defects SPEC --suite 'CMD' [--workdir DIR] [--label NAME] [--timeout N] [--tail N]` — a single sweep witness.

Whichever form runs, the receipt's first line self-pins the instrument: `MUTATE_TOOL:`/`REGRESSION_TOOL: <path> sha256=<…>` — for this identity that sha **must** read `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b`; that line plus the exit code and the terminal verdict line (`MUTATE: DONE|DEGRADED`, `REGRESSION: PASS|FAIL|SETUP`, `MUTATE_SELFTEST … VERDICT: PASS`) are the receipt-time instrument-sha/measurement gate. Exit 0/1 (run), 0 (regression/selftest) are the only acceptable witness exits; 2 is an honest cannot-verify and 64 a usage error — neither may be counted as a pass.

## 5. Findings

1. **PASS (primary claim).** `git show 4b7c682:tools/mutate-and-run.sh | sha256sum` = `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b`, exactly the declared witness-runner instrument. Blob stable since `58e5d53`; `4b7c682` is an ancestor of the frozen contract commit `6fd220b`; working-tree copy identical. Agree with the frozen facts.
2. **AGREE (rider support).** Historical instrument shas must be named per era, not as a singular "frozen SHA": nine distinct runner identities exist (§1 table). Round-12/kaika receipts cite `75ed934d…` (606716f era); the round-16 SKILL snapshot cites `cf41efaa…` (9f1d3c3); round-18+ receipts cite `d22c4025…`. The declared witness-tool `8dfaa25a…` is `tools/bash-witness-study.py` (seen as `tool_sha256` in the round-19 receipt and in round-19 refresh-entries input digests).
3. **MINOR (wording erratum, no behavior).** The `VERSION` constant (line 169 of the 4b7c682 blob) still reads `'mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)'` although the header documents r16/r17/r18 changes (legs 7–8, GIT_* scrub, repo-identity guard, exec-bit mirror) and the blob is the 2026-10-20 round-18 instrument. The constant is assigned once and never referenced anywhere in the blob (single grep hit), so no receipt line is affected — the operative pin is the `sha256sum` on `MUTATE_TOOL`/`REGRESSION_TOOL`. Candidate for the scribe's erratum list; do not edit the frozen bytes.
4. **MINOR (historical, already healed).** The round-18 witness receipt recorded the flag-form argv and exited 64 (§4a); round-19 superseded it with the corrected subcommand form at exit 0. Superseded receipts were preserved, not rewritten — consistent with "historical receipts are never rewritten". The round-20 receipt gate should make argv-correctness and exit==0 explicit so an exit-64 witness can never be admitted again.

## 6. Residual risk and verification gaps

- I did **not** execute the runner (no `--selftest`/`--regression`/sweep run) — my item names only the sha re-open and the header/usage read; execution belongs to the B-seat executors. All semantics above are from the verified blob text plus recorded receipts.
- `--regression` at HEAD would need the four sibling repos (`kumitate/kagi/tsukuroi/mado-shokunin`) present at `FLEET_ROOT` with the eight pinned revisions in their object stores; any absence is an honest `REGRESSION: SETUP` (exit 2), which must not be read as a pass.
- `stdout_sha256`-style raw-output digests embed absolute `SELF` paths and `mktemp` names, so they are environment-dependent; receipt identity should key on the tool sha pin + exit + terminal verdict lines, not on cross-environment stdout equality.
- No installs were performed (pacman paused; nothing needed beyond preinstalled git/coreutils).

— TameshiR20-3.A03ProvWitnessRunner, 2026-10-21
