# T54W1Read21 cold read — SKILL.md:1951-1962 `### Round-18 gate/probe registry — routed-defect closure`

- cand (content commit C0): `59c38109bf119d0e9d4f878644a82babc937bc1e`
- heading exactly as given: `### Round-18 gate/probe registry — routed-defect closure`
- section span: start 1951, end 1963 (reader-section.py; the span's last line 1963 is blank, so the section text is the 12 lines 1951-1962)
- section_sha256: `1f0a60ec99834f64de35d40b845f2c71381b15e8b24310eaf8ffa8028379e439`
  - reproduced locally by joining `git show <C0>:SKILL.md` lines 1951-1962 with `\n`, stripping the trailing blank line: same sha (`1f0a60…9e439`).
- command used (scratch `TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1Read21`, created with `mkdir -p` first):
  `python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin 59c38109bf119d0e9d4f878644a82babc937bc1e "### Round-18 gate/probe registry — routed-defect closure"`
- every byte below is read from `git show 59c38109bf119d0e9d4f878644a82babc937bc1e:SKILL.md` (the committed blob), never from the working tree.

## Findings (2)

### F1 — the bash-witness row names the wrong program as the reader of its pinned round-13 bytes

quote (byte-exact, occurs exactly once in the section):

```
its pinned round-13 bytes are read from `4acc607` through `.ufo/evidence/round-18/dispositions.json`
```

why: at C0 the cited tool never reads that file or that revision, so the anchor does not resolve inside the artifact the row is about. The row is the `tools/bash-witness-study.py` row, yet `tools/bash-witness-study.py` contains zero occurrences of `dispositions`, `4acc607` and `round-13`; its own pins are `PIN_BASH`/`REV_BASH`, parsed out of the runner. `4acc607` appears only in `.ufo/evidence/round-18/dispositions.json` → `historical_inputs["tools/bash-witness-study.py"]["rev"]`, a file consumed by `evidence-disposition.py` (`usage: evidence-disposition.py --root LANE --dispositions FILE`), not by the witness tool. A cold reader opening the tool to find the read finds a different pin path entirely.

receipt (run from `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, `C=59c38109bf119d0e9d4f878644a82babc937bc1e`):

```text
$ git show $C:tools/bash-witness-study.py | grep -c 'dispositions'
0
$ git show $C:tools/bash-witness-study.py | grep -c '4acc607'
0
$ git show $C:tools/bash-witness-study.py | grep -c 'round-13'
0
$ git show $C:tools/bash-witness-study.py | grep -n 'PIN_RE\|REV_RE\|runner_pins(\|materialize_target(Path'
198:PIN_RE = re.compile(r"^(PIN_BASH)=([0-9a-f]{64})$", re.M)
199:REV_RE = re.compile(r"^(REV_BASH)=([0-9a-f]{40})$", re.M)
281:def runner_pins(text: str) -> dict:
283:    for pattern in (PIN_RE, REV_RE):
592:    pins = runner_pins(read_text(RUNNER))
872:    pins = runner_pins(runner_text)
883:    data = materialize_target(Path(args.kagi), pins["REV_BASH"])
$ git show $C:tools/mutate-and-run.sh | grep -n 'PIN_BASH=\|REV_BASH='
616:PIN_BASH=275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f
617:REV_BASH=fecee8743e52eb8fb5fbb40782934cb619a1a96e
$ git show $C:.ufo/evidence/round-18/dispositions.json | python3 -c "..."   # historical_inputs revs
{'tools/mutate-and-run.sh': '4acc607dfd79f19d508bd50cdd06b77269fccd1d',
 'tools/pin-disposition.py': '4acc607dfd79f19d508bd50cdd06b77269fccd1d',
 'tools/bash-witness-study.py': '4acc607dfd79f19d508bd50cdd06b77269fccd1d'}
$ git show $C:tools/evidence-disposition.py | sed -n '167,169p'
USAGE = """usage: evidence-disposition.py --root LANE --dispositions FILE [--json]
       evidence-disposition.py --selftest
```

### F2 — the round-19 measure row's citation list ends in a run-together token that is not a path or an evidence id

quote (byte-exact, occurs exactly once in the section):

```
QUALITY37–39, lessonround19, S049
```

why: the row closes with three anchors; two resolve and one does not. `QUALITY37–39` are criteria 37-39 of `corpus/QUALITY.md`; `S049` is `corpus/SOURCES.md:58`; but `lessonround19` is one ASCII word (`xxd` of that byte run: `6c6573736f6e726f756e643139`) — no path, no `path:line`, no command, no id that exists in the corpus. `git grep lessonround19 $C -- corpus SKILL.md` matches only `SKILL.md` itself, and the artifact it evidently means, `corpus/lessons/round-19.md`, is spelled nowhere in the row. A cold reader has to guess the citation.

receipt:

```text
$ git show $C:SKILL.md | sed -n '1961p' | grep -o 'QUALITY37.\{0,40\}' | xxd
00000000: 5155 414c 4954 5933 37e2 8093 3339 2c20  QUALITY37...39,
00000010: 6c65 7373 6f6e 726f 756e 6431 392c 2053  lessonround19, S
00000020: 3034 392e 207c 0a                        049. |.
$ git grep -l lessonround19 $C -- corpus SKILL.md
59c38109bf119d0e9d4f878644a82babc937bc1e:SKILL.md
$ git grep -c lessonround19 $C -- corpus/lessons corpus/knowledge corpus/SOURCES.md
(no output — zero matches)
$ git ls-tree --name-only $C corpus/lessons/round-19.md
corpus/lessons/round-19.md
$ git show $C:corpus/QUALITY.md | grep -n '^3[789]\. '
334:37. A metadata correction names the exact stale provenan
344:38. A diff count names its unit: changed cells, deleted
352:39. A final-success claim names one effective receipt wi
$ git show $C:corpus/SOURCES.md | grep -n '^| S049 |'
58:| S049 | Python subprocess environment mapping — https://docs.python.org/3/library/su
```

Note on scope: F2 is a citation-format defect, not a false rule — the underlying lesson (`corpus/lessons/round-19.md`) exists. I report it because the row's only pointer to it is unresolvable as written. Both findings are reportable at this revision; neither is fixed here (the seat is read-only on lane files).

## Sweep — checked and found sound (no finding raised)

Read as an executor with no oral context, row by row. Each item below was opened at C0 and the row's claim was checked against the artifact it cites; nothing failed.

| Row | Checked against (opened at C0) | Result |
|---|---|---|
| `.ufo/evidence/round-18/defect-probes.py` | the tool's `--rev`/`--json`/`--only`/`--selftest` parser, `PROBE_IDS`, `GUARD_SPECS`, `guard_probe`, `run_selftest`, `main` | `PROBE_IDS = tuple("P%02d" % n for n in range(1, 12))` → 11 probes, so the printed `total=11` cell is exact; `guard_probe` counts the anchor bytes over the whole file (not the recorded line numbers) and errors when the count ≠ 1, so "an anchor was not unique → 2" holds; pristine ≠ 0 → `ProbeError` → 2; usage parser exits 64; bwrap envelope is `--ro-bind / /` (read-only fleet) |
| `.ufo/evidence/round-18/defect-probes.py` "never wrap it in `tools/trace-inputs.py`" | `P05`-`P07` `GUARD_SPECS` (path `None` → `trace_tool()`), `run_selftest`, `tools/trace-inputs.py` `run_trace` | P05/P06/P07 are the O_RDWR-exclusion, private-`PYTHONPYCACHEPREFIX` and root-execve guards of the promoted trace tool; the probes invoke that tool's `--selftest`, and `run_selftest` raises when the nested selftest returns anything but 0/1, so the nested run lands in the 2 (could-not-evaluate) class |
| `tools/registry-check.py` (round 18) | `MAX_TIMEOUT_S = 86400` (:107), the `(0, 86400]` validation (:245-256), `cleanup_error` (:707, :730), `CHILD_SUBREAPER_PRCTL`, setsid/setpgid selftest cases (:1230-1232), `load_registry`/`evaluate` exit map (:852-886) | bound, `NaN`/`Infinity` refusal, "→ 2 naming the row" (`f"{where} ({name!r})"` and `evaluate` returns 2 on a load error), descendant cleanup and `cleanup_error` all match; `.ufo/waves/round-18/w2/SentinelKillCode.md` exists and does document same-tick PID reuse and orphan adoption (the UID limit is documented in the tool's own contract, `tools/registry-check.py:39-44`, so the limit still has an anchor) |
| `tools/evidence-disposition.py` (round 18) | `resolve_historical_anchor` (:482-545), `resolve_historical_rev` (:548+), docstring :121, `_jj` (:2054+) | `lane.branch` → `refs/heads/<branch>`; attached `HEAD` via `symbolic-ref` → `refs/heads/<branch>`, so "lane.branch or attached branch" is exact; jj workspace with no binding → `CouldNotEvaluate` (2); non-jj detached clone anchors on HEAD only when a branch/remote-tracking ref contains it; HEAD is not read as a tip when a branch resolves; selftest requires `jj` (docstring :121 and every `_jj` case) |
| `tools/trace-inputs.py` | promoted vs `.ufo/evidence/round-17/coldread/trace-inputs.py` hashes; `O_RDWR` write-flag regex, `PYTHONPYCACHEPREFIX`, `first_pid`/`exec_ok` root-execve check, `--root/--out/--selftest` parser | the two copies differ (`f59c9312…` vs `521be955…`), both exist, so "unchanged, not byte-identical" holds; the three guards named in the cell are present in the promoted file |
| `.ufo/evidence/round-18/measure.py`, `coldread/assemble.py` | `DEFAULT_LEDGER_PATH`/`LEDGER_PATH`, `--explain` (`section_record`), `assemble.py` `--carry` + `carried_from` (:980, :1299-1315), `ledger.json` presence | default ledger `.ufo/evidence/round-18/coldread/ledger.json` exists and is the default; `--explain` adds `end` + `reasons` per section ("per bucket" is this corpus's word for a section, cf. `.ufo/waves/round-16/w2/SectionHashes.md`); `--carry` copies entries and stamps `carried_from`; `.ufo/evidence/round-17/measure.py` exists, so "as round 17" resolves |
| `.ufo/evidence/round-19/measure.py` | parser (:398-404), exit arithmetic (:436), `PATHS`, `SOURCE_PINS`, `REV18`/`TOOLS18`, selftest fixture loads (:254, :262-263), `.ufo/evidence/round-19/` listing | accepts `--repo/--rev/--snapshot/--check/--selftest` (so the documented command runs); `total: 5` and `5-corrected` → the "five frozen correction items" count is exact; `return int(args.check and corrected != 5)` → 0/1 as documented and 0-without-`--check` "reports a count"; `SOURCE_PINS` keys are `source-baseline.txt`/`source-round18-final.txt`; exactly four package fixtures are read (`SOURCE_PINS` ×2 + `probes-baseline.txt` + `checks-baseline.json`); `contract.json`, `before.json`, `after-21e7932.json` all exist |
| `.ufo/evidence/round-19/coldread/measure.py` | wrapper head (`IMPLEMENTATION`, `LEDGER`), its `__main__` block, `.ufo/evidence/round-19/coldread/ledger.json` | loads `.ufo/evidence/round-18/measure.py` and sets `DEFAULT_LEDGER_PATH`/`LEDGER_PATH`/`BOX3_LINK` to the round-19 ledger, so "selecting round-19 `coldread/ledger.json` as default" holds; otherwise delegates `module.main()` unchanged (same exit map); ledger exists and carries `carried_from` entries, matching "old entries retained verbatim" |

Cross-section wording checked for self-contradiction inside this section only: none found. In particular "unchanged CLI" in the `registry-check.py`, `evidence-disposition.py` and `bash-witness-study.py` rows is still true at C0 — C0 added `ScratchRootUnusable` handling to the last two without changing their flags (`tools/evidence-disposition.py` diff base→C0 touches only the exception class and the `main` mapping); the round's new scratch-root exit class is documented in `## Standing rules` and `corpus/knowledge/scratch-root-contract.md`, so I do not read the older rows as contradicting it.

## Opened artifacts (all at `59c38109bf119d0e9d4f878644a82babc937bc1e`)

- `SKILL.md` lines 1951-1962 (the section blob; working tree never read)
- `.ufo/evidence/round-18/defect-probes.py` (GUARD_SPECS, PROBE_IDS, guard_probe, run_selftest, main)
- `.ufo/evidence/round-18/dispositions.json` (`historical_inputs`)
- `.ufo/evidence/round-18/measure.py` (ledger default, `--explain`, `section_record`, selftest exit cases)
- `.ufo/evidence/round-18/coldread/assemble.py` (`--carry`, `load_carry`, `carried_from`, selftest)
- `.ufo/evidence/round-18/coldread/ledger.json` (existence)
- `.ufo/evidence/round-17/measure.py` (existence), `.ufo/evidence/round-17/coldread/trace-inputs.py` (hash)
- `.ufo/evidence/round-19/measure.py` (parser, PATHS, SOURCE_PINS, selftest fixtures)
- `.ufo/evidence/round-19/coldread/measure.py` (selector, `__main__`)
- `.ufo/evidence/round-19/coldread/ledger.json`, `.ufo/evidence/round-19/contract.json`, `.ufo/evidence/round-19/before.json`, `.ufo/evidence/round-19/after-21e7932.json`
- `.ufo/waves/round-18/w2/SentinelKillCode.md` (limits, measured revision)
- `tools/registry-check.py`, `tools/evidence-disposition.py`, `tools/bash-witness-study.py`, `tools/trace-inputs.py`, `tools/mutate-and-run.sh` (:616-617)
- `corpus/QUALITY.md` (criteria 37-39), `corpus/SOURCES.md` (S049), `corpus/lessons/round-19.md` (existence)

Prior-round cross-check (context only, not relied on for the findings): the same section was cold-read in round 27 as `.ufo/waves/round-27/w1/Read35.md`; it already recorded the bash-witness attribution gap and the `lessonround19` token as minor gaps, and both are still present byte-for-byte at C0, so I re-verified them independently at this revision rather than inheriting the claim.

Tool installs: none (no channel used, nothing recorded).

Checks I did **not** run, and why: no lane selftest or counter was executed — the reader assignment is open-and-compare, not execution, and the seat is read-only; the two findings are decided on the committed bytes alone.
