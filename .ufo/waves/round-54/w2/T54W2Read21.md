# T54W2Read21 — cold read, round 54 wave 2

- Section: `### Round-18 gate/probe registry — routed-defect closure`
- Revision: `99c3bc88d704566197783f66b211ee0a830e0330` (C1)
- Span printed by the reader helper: start 1951, end 1963
- `section_sha256`: `661f63518af62b198f68ec5400778d9662df725d84744ad428dacc08823e6d7e`
- Section bytes = `SKILL.md` lines 1951–1962 at C1 (the round-18 sectionizer strips trailing blank
  lines and hashes the joined text; independently reproduced: `sed -n '1951,1962p'` →
  `661f63518af62b198f68ec5400778d9662df725d84744ad428dacc08823e6d7e`, while the raw
  blank-terminated span hashes to `a698fd6ce6e3bd4ebb2c80cb33d59fc2b71154e90643560962b2f557fd3c37f3`).

## Findings

None. Every rule anchor resolves at C1, every table cell that states a tool property or an
evidence pin is supported by the artifact it names, no sentence in the section contradicts
another, and the QUALITY 104 surface checks are clean (no double spaces, no run-together
tokens, no missing space after a sentence period outside real paths/code, no duplicate or
adjacent parentheticals; all 8 table rows carry exactly 4 cells / 5 pipes).

## Opened artifacts (all read from git objects at C1, never the worktree)

| Artifact | What was checked |
|---|---|
| `SKILL.md` 1951–1962 | the section bytes and sha above |
| `.ufo/evidence/round-18/defect-probes.py` | `PROBE_IDS` = P01..P11 (11); `emit_results` prints `DEFECT_PROBES: open=%d closed=%d total=%d`; exit 0 measured / 2 could-not-evaluate / 64 usage via `UsageParser.error`; `--selftest` returns 1 only (not claimed in the cell); `bwrap --ro-bind / / … --ro-bind FLEET /mnt/source` envelope; `guard_probe` sets `closed` only when pristine selftest exit 0 and mutant exit ≠ 0; anchor count ≠ 1 and pristine red raise `ProbeError` → 2; `GUARD_SPECS` P05–P07 have `path: None` and resolve through `trace_tool()` (promoted `tools/trace-inputs.py`), i.e. they run that tool's selftest |
| `tools/registry-check.py` | `MAX_TIMEOUT_S = 86400`; `math.isfinite(ts) and 0 < ts <= MAX_TIMEOUT_S`; error text names the row (`{where} ({name!r}).timeout_s must be a finite positive number <= 86400`); selftest cases `timeout-zero/nan/infinity/negative-infinity/overflow/boolean/too-large/float-huge` expect exit 2; comment at :103-106 records the historic `communicate()` overflow crashing with exit 1; `_cleanup_row` on both the timeout and the normal-exit path; `fragment["cleanup_error"] = "row descendants remain after bounded cleanup"` and `held=… and not cleanup_error`; docstring :38-44 records the UID/unkillable, same-tick PID-reuse and double-fork/subreaper limits |
| `.ufo/waves/round-18/w2/SentinelKillCode.md` | Finding 1 (adopted orphan signalled/reaped) and Finding 2 (same-tick PID reuse); the cited artifact exists at C1 (6901 bytes) |
| `tools/evidence-disposition.py` | `resolve_historical_anchor` (one shared anchor for G2/G3): `lane.branch` → `refs/heads/<branch>`; else attached `symbolic-ref HEAD` branch; `.jj` present with no branch → `CouldNotEvaluate` (exit 2); detached non-jj → HEAD commit accepted only when `for-each-ref --contains` over `refs/heads/`/`refs/remotes/` is non-empty; docstring :51-53 and :121 ("Selftest also requires `jj`") |
| `tools/bash-witness-study.py` | `git_clean_env()` drops every `GIT_*` and pins `GIT_CONFIG_GLOBAL=/dev/null`/`GIT_CONFIG_NOSYSTEM=1`; all git children use it (`materialize_target` :366-369, `sweep_env()` = `git_clean_env()` + `SCRUB_ENV`, selftest `safe_env`); `PIN_RE`/`REV_RE` parse `PIN_BASH`/`REV_BASH` from `tools/mutate-and-run.sh` |
| `tools/mutate-and-run.sh` at C1 | line 616 = `PIN_BASH=275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`, line 617 = `REV_BASH=fecee8743e52eb8fb5fbb40782934cb619a1a96e`; the prefixes in the cell (`275d8294…`/`fecee874…`) match; both definitions are unique file-wide (1 each) |
| `.ufo/evidence/round-18/dispositions.json` | `historical_inputs["tools/bash-witness-study.py"].rev = 4acc607dfd79f19d508bd50cdd06b77269fccd1d` (cell's `4acc607`) |
| `tools/registry-check.py` (same file, gate argv) / `.ufo/evidence/round-18/final/audit-1846.stdout` | the evidence-disposition live entry passes `--dispositions .ufo/evidence/round-18/dispositions.json` → 0 clean; SKILL.md :1627 names the same live entry, so "which the evidence-disposition gate reads" is supported |
| `tools/trace-inputs.py` (promoted) and `.ufo/evidence/round-17/coldread/trace-inputs.py` (historical copy) | sha256 `f59c9312…a29f4` vs `521be955…953070` → not byte-identical; `git log --follow` on the copy shows exactly one commit (`2a22ade`, round 17) → unchanged since round 17; promoted selftest cases `rdwr-open-excluded`, `pycache-prefix-private` (asserts absolute prefix whose parent is `trace-inputs-run-*` under the scratch root and outside the root), `root-exec-required` (fake strace log with no execve → expects exit 2), so removal of each guard fails a case |
| `.ufo/evidence/round-18/measure.py` + `coldread/assemble.py` | `DEFAULT_LEDGER_PATH = '.ufo/evidence/round-18/coldread/ledger.json'`; `--explain` adds per-section `end` and sorted `reasons` (`section_record`), reasons histogram is the per-bucket view; assemble.py `--carry` loads prior entries via `load_carry` ("unchanged except for their immediate carry source") and stamps `entry["carried_from"] = path`; round-17 `measure.py` exists at C1 |
| `.ufo/evidence/round-19/measure.py` | docstring exit map 0/1/2/64; `Parser.error` → `exit(64)`; `return int(args.check and corrected != 5)`; `SOURCE_PINS` pins `source-baseline.txt`/`source-round18-final.txt`; selftest reads exactly four frozen package fixtures (2 `SOURCE_PINS` + `probes-baseline.txt` + `checks-baseline.json`); `PATHS` excludes `before.json`, which exists in the round-19 evidence dir |
| `.ufo/evidence/round-19/contract.json` | population of five items (R18-1..R18-5) and `C1` unit "five routed defects durably corrected" — matches "all five frozen correction items" |
| `corpus/QUALITY.md` at C1 | criteria 37 (metadata correction names the stale field/line), 38 (diff count unit), 39 (final-success names an effective receipt) exist and match the round-19 lesson rows |
| `corpus/SOURCES.md` at C1 | `S049` is the Python `subprocess` docs row (mined), used-by includes `corpus/lessons/round-19.md` — the cited source exists and is the one the round-19 contract names |
| `corpus/lessons/round-19.md` | exists at C1 |
| `.ufo/evidence/round-19/coldread/measure.py` | imports round-18 `measure.py` unchanged, overrides only `DEFAULT_LEDGER_PATH`/`LEDGER_PATH`/`BOX3_LINK`/`IGNORED_INPUTS` before `module.main()`, so the credit/trace/veto/CLI rules and exit map are inherited (0/2/64, selftest 0/1) |
| `.ufo/evidence/round-19/coldread/ledger.json` | 184 entries, 68 with `carried_from`, every entry carries `inputs` and `traces`, `read_rev` is revision-pinned — supports "old entries retained verbatim" and "input/receipt hashes are revision-pinned" |
| `.ufo/evidence/round-19/` tree | `before.json`, `after-21e7932.json`, `contract.json` all present |

## Commands run (read-only; lane never written)

```
mkdir -p /fast/scratch/hyaku/tameshi-r54/T54W2Read21
export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read21
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  99c3bc88d704566197783f66b211ee0a830e0330 "### Round-18 gate/probe registry — routed-defect closure"
git log --oneline -3 99c3bc88d704566197783f66b211ee0a830e0330
git show 99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md > $S/SKILL.md   # S=/fast/scratch/hyaku/tameshi-r54/T54W2Read21
sed -n '1951,1962p' $S/SKILL.md | sha256sum                              # 661f6351… matches reader-section
git show --stat --oneline 99c3bc88d704566197783f66b211ee0a830e0330        # section untouched by C1
git show 99c3bc88d704566197783f66b211ee0a830e0330:tools/mutate-and-run.sh | sed -n '605,625p'
git show 99c3bc88d704566197783f66b211ee0a830e0330:tools/mutate-and-run.sh | grep -cE '^PIN_BASH='   # 1
git show 99c3bc88d704566197783f66b211ee0a830e0330:tools/mutate-and-run.sh | grep -cE '^REV_BASH='   # 1
git show <C1>:<tool> | grep -n …   # add_argument, return 2/64, ScratchRootUnusable, exits, selftest cases
git cat-file -e <C1>:<each of the 16 named paths>          # all resolve
git show <C1>:.ufo/evidence/round-18/defect-probes.py > $S/defect-probes.py && grep -n …
git grep -n -- '--carry' <C1> -- .                         # --carry lives in assemble.py, not measure.py
git grep -ln strict_scratch_root <C1> -- tools .ufo/evidence   # 7 tools; none of the exit cells here enumerates exits
git log --oneline <R18>..<C1> -- <each named tool>         # R18=4b7c6823…; CLI option sets diff clean (SAME)
git show <C1>:tools/bash-witness-study.py | sha256sum ; git show <C1>:.ufo/evidence/round-17/coldread/trace-inputs.py | sha256sum
git log --oneline --follow -- .ufo/evidence/round-17/coldread/trace-inputs.py   # single commit (2a22ade)
git show <C1>:corpus/QUALITY.md | grep -nE '^3[6-9]\.' ; git show <C1>:corpus/SOURCES.md | grep -n S049
git show <C1>:.ufo/evidence/round-19/coldread/ledger.json | python3 -c '…json summary…'
```

## Notes on two candidate defects rejected as unsupported

1. **`--carry` / `--explain` attribution (row 1960).** `--carry` is not a `measure.py` option
   (the file's `add_argument` set is `--rev --repo --ledger-file --ledger-rev --inputs-overlay
   --explain --selftest`), but it is `assemble.py`'s option and the row's Name column covers both
   files; `--explain` is `measure.py`'s. The cell is therefore true of the named pair and I did not
   report it.
2. **UID limit citation (row 1956).** `SentinelKillCode.md` contains Finding 1 (adopted orphan) and
   Finding 2 (same-tick PID reuse) but the string `UID` appears nowhere in it (case-insensitive
   grep is empty); the UID/unkillable limit is documented in the row's own tool at
   `tools/registry-check.py:43`. Since the claim is true of the artifact the row names and the
   parenthetical most directly attaches to its nearest item (the adopted-orphan finding, which the
   file does carry), I did not report it as a stale cell.

## Bounds observed

Read-only on the lane: no lane file was created, modified or deleted; no mutating git/jj command
was run; all work happened under `/fast/scratch/hyaku/tameshi-r54/T54W2Read21`. No tools were
installed or upgraded. Report written only under
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w2/`.
