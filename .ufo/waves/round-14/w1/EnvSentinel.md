# EnvSentinel — round 14 w1 (sentinel, read-only)

Surface: `.ufo/evidence/round-14/capture-context.py` (ReceiptHarness-owned).
**Status of target: ABSENT at review time.** `ls .ufo/evidence/round-14/` at
03:16–03:17 showed only `claims.json`, `before.json`, `measure.py`,
`sources-before.json`. This is a review of the **retained contract** plus the
code it must call (pin probe, runner), not of harness code. No completion is
claimed. Risks below were also sent to `TameshiR14.ReceiptHarness` as a short
peer message.

## Local evidence observed

- Lane HEAD `d6809df7775338f000e44c8a916067b8866867fb` = baseline; porcelain
  shows only untracked `.ufo/evidence/round-14/`, `.ufo/waves/round-14/`.
- `sha256 tools/pin-disposition.py` = `297253971dab…0f11` (= r13 probe);
  `sha256 tools/mutate-and-run.sh` = `75ed934d…adc5` (= pin-manifest
  `derived_from.sha256`).
- Probe `git_env()` (`tools/pin-disposition.py:197-210`) drops every inherited
  `GIT_*` key, then sets `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`,
  `GIT_OPTIONAL_LOCKS=0`, `GIT_TERMINAL_PROMPT=0`, `GIT_NO_LAZY_FETCH=1`,
  `GIT_PAGER=cat`, `LC_ALL=C`. `git_run` (`:214-231`) uses argv list,
  `git -C repo`, stdin DEVNULL, 30 s timeout. Live git verbs used:
  `rev-parse --show-toplevel`, `rev-parse --verify --quiet --end-of-options`,
  `cat-file -t`, `cat-file blob` (`:255-341`) — all read-only.
- Probe stdout carries `observed_at` (`:578`), absolute `manifest` (`:581`),
  `root` (`:582`), per-leg worktree absolute paths (`:428`). No env content.
- Ambient agent env (names only, values not read) contains `GIT_EDITOR`,
  `GIT_PAGER`, `GIT_TERMINAL_PROMPT`, `PYTHONUNBUFFERED`. L1 likely inherits a
  similar set.
- `/nonexistent` and `/nonexistent/tameshi-round14-poison` do not exist
  (`ls` → No such file). git 2.55.0, Python 3.14.7.
- r13 `verification.json` `pin_env_scrub` argv is byte-identical to `pin_live`
  and has no env field (routed item 2 confirmed). r13 `expected.json`
  `expected_checks` has **no** `pin_env_scrub` row — so the r14 receipt cannot
  be read as satisfying a frozen expectation; it is a distinct new receipt.
- Runner `tools/mutate-and-run.sh:84-89` (six-leg table), `:542-553`
  (`PIN_*`/`REV_*`), `:1112-1140` (six `regression_case_git` calls) all match
  `pin-manifest.json` leg/path/sha/commit by reading.

## Findings (contract-specific; to verify once code lands)

| ID | Sev | Exploit / failure path | Impact | Smallest remediation |
|---|---|---|---|---|
| ES-1 | high | Harness injects by mutating `os.environ["GIT_DIR"]` (or runs injected leg first and reuses the dict) → baseline also poisoned → “baseline == injected” holds with both legs poisoned. | Fabricated discrimination; receipt proves nothing. | Build two fresh dicts, pass via `env=`; never assign `os.environ`. Record `injected_env` only on injected leg; baseline leg records `injected_env: {}`. |
| ES-2 | high | Probe scrubs `GIT_*` itself, so equality is the expected outcome whether or not the variable reached the child; no positive control → vacuous (cf. QUALITY 11 discriminator rule). | Equality cannot distinguish “scrub works” from “injection never delivered”. | Add one read-only control under the same injected env: `git -C <lane> rev-parse --git-dir` (expect nonzero, stderr names the poison path) vs baseline env (expect 0). Record both exits. |
| ES-3 | med | Baseline env = raw ambient. If L1 runs under a git hook/worktree tool, ambient may hold `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`/`GIT_CONFIG_PARAMETERS`/`GIT_CONFIG_COUNT`… → “baseline” is itself redirected for any harness-side git, and the injected delta is ill-defined. | Mis-attributed context; possible read of wrong repo by harness. | Baseline = ambient minus every `GIT_*`; injected = baseline + `{GIT_DIR: poison}` only. Record sorted stripped key **names** (no values) as `stripped_ambient_git_keys`. |
| ES-4 | med | Credential leak: dumping `env`, `os.environ`, `subprocess.CalledProcessError` repr with env, or `PATH`/token-bearing vars into receipt. | Secrets enter committed evidence (AGENTS: shape-only). | Receipt fields allow-listed: argv, cwd, injected_env (one key), stripped key names, exits, stdout/stderr of probe/control, digests, mapping table. No other env. |
| ES-5 | med | Poison path hijack: if `/nonexistent/tameshi-round14-poison` exists (attacker or prior run creates a repo there), poison becomes a real redirect to foreign objects. | Harness-side git reads an attacker repo; control result inverted. | Assert `not os.path.lexists(poison)` (and parent) before both legs; record `poison_path_absent: true`; fail exit 2 otherwise. |
| ES-6 | med | Harness-side git not read-only: `git status`/`git diff` refresh the index (write `index.lock`) unless `GIT_OPTIONAL_LOCKS=0`; `hash-object -w`, `add`, `stash`, `checkout`, `fetch` mutate. r13 `frozen_and_guardrail_unchanged` used `git diff --quiet`. | Index/worktree mutation during an evidence run; racing siblings. | Prefer `hashlib` over file bytes for source/manifest digests. If git is needed: argv list, probe-equivalent scrubbed env incl. `GIT_OPTIONAL_LOCKS=0`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `--end-of-options`; verbs limited to `rev-parse`/`cat-file`. |
| ES-7 | med | Comparison overstrips: deleting more than top-level `observed_at` (e.g. worktree, head, status) or comparing text not parsed JSON; or both legs failing identically (exit 2, bad manifest) compare “equal”. | False-green equality. | Parse both stdouts; `pop("observed_at")` top-level only; require both exit 0, `status=="ok"`, exactly 6 legs, then `==`. Record a diff list on mismatch; never suppress. |
| ES-8 | low | Sibling HEAD moves between legs → genuine mismatch reported as scrub failure. | Misdiagnosis, not a leak. | Run legs back-to-back; on mismatch report differing JSON pointers; don't retry silently. |
| ES-9 | low | Interpreter/PATH injection: argv `python3` resolves via PATH; `PYTHONPATH`/`PYTHONHOME` may alter imports. | Different interpreter than recorded. | Use `sys.executable` (record it) or `-I`; record the exact argv actually run. Differences from r13 argv are fine — new receipt, not repair. |
| ES-10 | low | cwd inherited from L1 shell; relative `tools/pin-disposition.py` and manifest resolve elsewhere. | Wrong file run, or exit 2 masked by ES-7. | `cwd = realpath(__file__)` parents → lane root; assert probe sha `2972539…` and runner sha `75ed934d…` before running; record cwd. |
| ES-11 | low | Mapping booleans hardcoded `true`, or runner sourced/executed to read constants. | Fabricated readiness; runner execution out of scope. | Parse runner bytes with regex for table rows, `PIN_X=`/`REV_X=` pairs and `regression_case_git` path/PIN/REV args; compare to manifest per leg; any false → nonzero exit + `status`. Never `bash` the runner. |
| ES-12 | low | Writes outside owned path (round-13 dir, manifest rewrite) or non-atomic partial `context-receipt.json`. | Historical-evidence rewrite / torn receipt. | Write only `.ufo/evidence/round-14/context-receipt.json` via tmp+`os.replace` in same dir; open round-13 inputs read-only. |
| ES-13 | low | Process cleanup: no timeout or `shell=True`. | Hang / injection. | `subprocess.run([...], shell=False, stdin=DEVNULL, timeout=…)`; on `TimeoutExpired` record and exit 2. |

## Checks L1 should run (after ReceiptHarness lands; not run here)

1. Static: `grep -n 'os.environ\[' capture-context.py` → no assignment;
   `grep -n 'shell=True\|environ.copy\|json.dump.*environ' ` → none recorded;
   git verbs limited to `rev-parse`/`cat-file`.
2. `sha256sum tools/pin-disposition.py tools/mutate-and-run.sh .ufo/evidence/round-13/*`
   before and after harness run — identical; `git status --porcelain` adds only
   `round-14/context-receipt.json`.
3. Run harness once from a foreign cwd (e.g. `/tmp`) with an ambient
   `GIT_DIR=/tmp/x` exported: receipt must show stripped key names including
   `GIT_DIR`, baseline control exit 0, injected control nonzero, probe JSON
   equal minus `observed_at`, both exit 0, 6 legs, `status ok`.
4. `python3 -c` over receipt: keys allow-listed (ES-4); `injected_env ==
   {"GIT_DIR":"/nonexistent/tameshi-round14-poison"}`; no value of any ambient
   variable appears (grep receipt for `$HOME`-only paths is fine; grep for
   ambient `GIT_EDITOR` value must be absent).
5. Mutation-style sanity (manual, scratch copy): temporarily drop the probe’s
   `GIT_*` filter in a `/tmp` copy and point the harness at it → equality must
   fail. Do not edit the real probe.
6. Mapping table: 6 legs × {table, PIN, REV, leg-call} all true and derived
   from runner bytes at `75ed934d…`.

Tool installs/updates: none.
