# T53W1Read17 — cold-read of `### Round-18 gate/probe registry — routed-defect closure`

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Content commit (C*): `a41195dfc13a73958e4c5228ec196b28d03ded03`
- Read source: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md` (git objects only; the working tree was not read)
- Section range at C*: lines 1932–1943 (heading line 1932; next heading, `### Round-20 gate/probe registry — frozen receipt instruments`, at line 1945; line 1944 is the whitespace-only separator stripped by the frozen monitor rule)
- `section_sha256`: `1f0a60ec99834f64de35d40b845f2c71381b15e8b24310eaf8ffa8028379e439`
- Verdict: **no findings** — every statement in the section either matches the bytes at C* or is explicitly past-tense history that the pinned code itself documents.

## Method — reproducing the frozen split before hashing

Split rule reimplemented literally: lines of `SKILL.md` at C*, a heading is a line matching `^#{1,3}(\s|$)` outside ``` fences, section = heading through the line before the next heading, trailing whitespace-only lines stripped, joined with `\n`, no trailing newline, sha256 over UTF-8 bytes with `surrogateescape`.

Observed: heading index 1931 (line 1932), next heading index 1944 (line 1945), 13 raw lines → 12 after stripping, hash `1f0a60ec99834f64de35d40b845f2c71381b15e8b24310eaf8ffa8028379e439`. The heading line is unique in the file (single `grep -n` hit at 1932), so no duplicate-section ambiguity.

## Checks run and what they showed

All content checks are `git show C*:<path>` / `git grep C* --` reads; no file in the lane was written, no mutating git command was run.

| # | Claim under test | Command (abridged) | Observed at C* | Verdict |
|---|---|---|---|---|
| 1 | the eleven probes / exit map / guard-closure rule | `git show C*:.ufo/evidence/round-18/defect-probes.py` | `PROBE_IDS = tuple("P%02d" % n for n in range(1, 12))` (11 ids); `main` returns 0 after `emit_results`, 2 on `ProbeError`/probe errors, `UsageParser.error` → `self.exit(64, …)`; `guard_probe` raises when the pristine selftest exits nonzero and marks `open` iff the mutant exits 0 | holds |
| 2 | probe count string in the exit cell | same file, line 956 | `print("DEFECT_PROBES: open=%d closed=%d total=%d" % …)` with `len(results)` over all 11 ids; the receipt `.ufo/evidence/round-18/final/probes.stdout` ends `DEFECT_PROBES: open=0 closed=11 total=11` | holds |
| 3 | children under bwrap, fleet read-only | same file, `sandbox_argv` (line ~192) | `bwrap --ro-bind / / --dev /dev --proc /proc --unshare-pid --unshare-net --die-with-parent --bind W W --bind W /mnt [--ro-bind FLEET /mnt/source] --tmpfs /tmp --bind W/tmp /tmp … env -i …`; every child launch goes through `run_bytes` → `sandbox_argv` | holds |
| 4 | P05–P07 run `tools/trace-inputs.py`'s selftest, anchors unique | `GUARD_SPECS["P05".."P07"]` (paths `None` → `trace_tool(root)`), plus anchor counts in both candidate files | P05/P06/P07 anchors (`WRITE_FLAGS_RE … O_RDWR …`, `env["PYTHONPYCACHEPREFIX"] = cache`, `if tracer.first_pid is None or tracer.first_pid not in tracer.exec_ok:`) occur exactly 1× in `tools/trace-inputs.py` and exactly 1× in `.ufo/evidence/round-17/coldread/trace-inputs.py`; `run_selftest` runs the tool's `--selftest` | holds |
| 5 | nested ptrace refusal (why the tool must not wrap the probe) | `git grep -l "nested ptrace" C*` | `.ufo/waves/round-17/w3/RR7.md` ("Nested ptrace is refused"), `.ufo/waves/round-17/w1/N01TraceGitSafety.md` (`strace: attach: ptrace(PTRACE_SEIZE, …): Operation not permitted`) | holds |
| 6 | `timeout_s` bound and NaN/Infinity refusal | `tools/registry-check.py` | `MAX_TIMEOUT_S = 86400`; `math.isfinite(ts) and 0 < ts <= MAX_TIMEOUT_S`; `json.loads(text, parse_constant=_reject_json_constant)` in `load_registry`, with `_nonfinite_location` naming `(row 'name')`; `registry_errors` failures are exit 2 | holds |
| 7 | pre-cap `communicate()` crash was exit 1 (past tense) | `tools/registry-check.py:104-106` | comment: "a finite timeout of 2147484 s or more overflows Popen.communicate()'s C timeout and crashed with exit 1" | holds (documented as history, correctly past tense) |
| 8 | descendants killed at timeout *and* after exit; `cleanup_error` on survivors | `tools/registry-check.py` `run_row` (lines ~680–743) + selftest cases | `_cleanup_row` is called in the `TimeoutExpired` branch **and** in the normal-return branch; `fragment["held"] = got == expected_exit and not missing and cleanup_ok`; `cleanup_error = "row descendants remain after bounded cleanup"`; selftest cases `timeout-kills-setsid-pipe`, `timeout-kills-setpgid-pipe`; `PIPE_DRAIN_TIMEOUT_S = 0.5`, `_bounded_communicate` | holds |
| 9 | limits named in the row | `tools/registry-check.py:39-44`; `.ufo/waves/round-18/w2/SentinelKillCode.md` | "Descendants that change UID may become unreadable or unkillable, and start-time granularity leaves a same-tick PID-reuse residual"; SentinelKillCode Finding 1 (adopted orphan can be signalled) and Finding 2 (same-tick PID reuse) | holds |
| 10 | G2/G3 anchor commit rules, jj detached HEAD → 2, no HEAD-as-tip | `tools/evidence-disposition.py` | docstring "Anchor A is refs/heads/<lane.branch> or an attached local branch tip when bound"; `git config --get lane.branch` → `refs/heads/<branch>`; `.jj` present without `lane.branch` raises `"jj workspace without a lane.branch binding has no authoritative tip"`; detached non-jj path uses `for-each-ref --contains … refs/heads/ refs/remotes/` (excluding refs ending `/HEAD`) | holds |
| 11 | `--selftest` needs `jj` on PATH | same file | docstring line 121: "Selftest also requires `jj` for its isolated colocated-repository cases"; `_jj` spawns `jj` via `subprocess.run(["jj"] + argv)` | holds |
| 12 | every git child scrubs `GIT_*`, pins `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` | `tools/bash-witness-study.py` | `git_clean_env()` drops `GIT_*` and sets both pins; the 6 `subprocess.run` sites (lines 347, 614, 1259, 1264, 1269, 1276) all pass `env=git_clean_env()` / `env=sweep_env()`; selftest asserts the scrub under a patched hostile `GIT_*` env | holds |
| 13 | round-13 bytes read from `4acc607` through `.ufo/evidence/round-18/dispositions.json` | `git show C*:.ufo/evidence/round-18/dispositions.json`; `git show 4acc607…:tools/bash-witness-study.py \| sha256sum` | `historical_inputs["tools/bash-witness-study.py"].rev = "4acc607dfd79f19d508bd50cdd06b77269fccd1d"`, reason "the round-13 receipts were produced with the 49e9e5e2 bytes held at this rev"; actual bytes at `4acc607` hash to `49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80` | holds (pin resolves uniquely; `git rev-parse --verify 4acc607^{commit}` → the full sha) |
| 14 | round-18 dispositions is the live manifest (the round-17 manifest is superseded in practice) | `git show C*:tools/registry.json` | the `evidence-disposition` row runs `--dispositions .ufo/evidence/round-18/dispositions.json`; the round-18 file carries the superset `historical_inputs` (three tools incl. bash-witness) | holds — see nuance N1 |
| 15 | round-17 evidence copy unchanged and not byte-identical to the promoted tool | sha256 of `.ufo/evidence/round-17/coldread/trace-inputs.py` at `eb7838b1…`, `790abd21…`, `a41195df…`; sha256 of `tools/trace-inputs.py` at C* | r17 copy = `521be955…` at all three revisions (only one commit, `2a22ade`, ever touched it); promoted tool = `f59c9312…` | holds |
| 16 | promoted selftest discriminates P05–P07 | `.ufo/evidence/round-18/c2-probes-v2-e08271a.txt`, `.ufo/evidence/round-18/final/probes.stdout` | `PROBE P05 closed … pristine_exit=0 mutant_exit=1`, likewise P06/P07; trailer `DEFECT_PROBES: open=0 closed=11 total=11` | holds |
| 17 | round-18 measure/assemble: default ledger, `--carry` verbatim + `carried_from`, `--explain` | `.ufo/evidence/round-18/measure.py`, `.ufo/evidence/round-18/coldread/assemble.py` | `DEFAULT_LEDGER_PATH = '.ufo/evidence/round-18/coldread/ledger.json'`; `parser.add_argument('--explain', action='store_true')`; assemble's `load_carry` docstring "Load prior entries unchanged except for their immediate carry source" and `entry["carried_from"] = path`; `--carry` CLI flag present | holds |
| 18 | input-keyed credit only, never command coverage | `measure.py` docstring | "input-keyed … it binds credit to recorded inputs, not to the commands a bucket requires"; per-section `reasons` histogram; strict/legacy `trace_gate` | holds |
| 19 | round-19 measure: five items, exit map, `--check` gate, four frozen fixtures, SOURCE_PINS, contract/before roles | `.ufo/evidence/round-19/measure.py`, `contract.json`, `before.json` | `SOURCE_PINS` = {source-baseline.txt: ac82b2df…, source-round18-final.txt: 018ee9a8…}; selftest reads exactly four package files (`source-baseline.txt`, `source-round18-final.txt`, `probes-baseline.txt`, `checks-baseline.json`) plus inline synthetic snapshots; `return int(args.check and corrected != 5)`, errors → 2, `Parser.error` → 64; `contract.json` has the 5-item `population`; `before.json` is a measured receipt (`corrected: 0, open: 5`, `revision: 7243e7f…`) and is absent from `PATHS`, so it is not a selftest input | holds |
| 20 | round-19 coldread selector delegates to round-18 measure, selects the round-19 ledger, same exits, old entries verbatim | `.ufo/evidence/round-19/coldread/measure.py`, `.ufo/evidence/round-19/coldread/ledger.json`, `.ufo/evidence/round-17/coldread/ledger.json` | wrapper loads `.ufo/evidence/round-18/measure.py` by path, sets `DEFAULT_LEDGER_PATH`/`LEDGER_PATH`/`BOX3_LINK` to `.ufo/evidence/round-19/coldread/ledger.json`, adds that path to `IGNORED_INPUTS`, then `sys.exit(module.main())`; ledger vs round-17: 68 entries carry `carried_from` and all 68 match the round-17 entry field-for-field except `carried_from`; the 25 newly added entries have seat `L1 TameshiR19-2 author source re-anchor` | holds — see nuance N2 |

## Holds (pointers verified against C* bytes)

Every `path` named in the section exists as a blob/tree at C* (`git cat-file -e`): `.ufo/evidence/round-18/defect-probes.py`, `tools/registry-check.py`, `tools/evidence-disposition.py`, `tools/bash-witness-study.py`, `tools/trace-inputs.py`, `.ufo/evidence/round-18/measure.py`, `.ufo/evidence/round-18/coldread/assemble.py`, `.ufo/evidence/round-19/measure.py`, `.ufo/evidence/round-19/coldread/measure.py`, `.ufo/evidence/round-18/dispositions.json`, `.ufo/waves/round-18/w2/SentinelKillCode.md`, and both `coldread/ledger.json` files.

Verbatim statements from the section that the checks above sustain:

- "`DEFECT_PROBES: open=N closed=M total=11`"
- "2 a probe errored, a pristine selftest was red, or an anchor was not unique"
- "never wrap it in `tools/trace-inputs.py`"
- "`timeout_s` must be a finite number in (0, 86400]"
- "survivors fail the row with `cleanup_error`"
- "unchanged CLI (`--selftest` now needs `jj` on PATH)"
- "read from `4acc607` through `.ufo/evidence/round-18/dispositions.json`"
- "not byte-identical to the promoted tool"
- "a `carried_from` key"
- "`SOURCE_PINS` binds source-baseline/source-round18-final"
- "not selftest inputs"
- "selecting round-19 `coldread/ledger.json` as default (no legacy overrides)"
- "old entries retained verbatim"
- "children run under bwrap with the fleet read-only"

## Findings

**None.** `findings` in `T53W1Read17.json` is `[]`.

Two wording nuances were examined and deliberately **not** promoted to findings, because neither is falsified by the bytes at C*:

- **N1** — the parenthetical that the round-17 manifests are superseded (row for `tools/bash-witness-study.py`). `.ufo/evidence/round-18/dispositions.json` records `"supersedes": ".ufo/evidence/round-14/dispositions.json"` (its G7 lineage target), and `.ufo/evidence/round-17/dispositions.json` still exists and also names round-14. What makes the parenthetical true in effect is that the live registry row (`tools/registry.json`) points at the round-18 manifest and only that manifest carries the `tools/bash-witness-study.py` historical pin. "Superseded" is therefore an authority statement, not a lineage field, and it is correct as written; the file-level lineage quirk lives in dispositions metadata, outside this section's text.
- **N2** — "refreshed entries are L1-author source reads … old entries retained verbatim". The round-19 ledger holds 184 entries: 68 carried from round-17 (byte-equal apart from `carried_from`), 91 byte-identical to the round-18 ledger, and 25 new entries whose seat is `L1 TameshiR19-2 author source re-anchor`. The literal "refreshed … L1-author" reading is the 25 new entries and holds; the 91 re-listed round-18 entries are covered by "old entries retained verbatim", which also holds field-for-field. No part of the sentence claims round-19 blind evidence, which matches the ledger's `provenance` note.

## Limits of this read

- The probe rows were verified by reading code and the round-18 receipts; `defect-probes.py --rev`, `registry-check.py`, `evidence-disposition.py --selftest` and `measure.py --selftest` were **not executed** (seat bounds: read-only, no lane writes, no fixtures needed, and the round's credit is a cold-read, not a re-measurement).
- The `4acc607` pin is verified for `tools/bash-witness-study.py` only; the other dispositions `historical_inputs` rows were not re-hashed (not claimed by this section).
- `REV_BASH` itself lives in the kagi runner (`corpus/surface-census.sh` in the read-only source repo), so the running value of that pin was not re-derived here.
- No tool installs, no package changes.
