# T54W2Read23 — cold read of `### Round-26 gate/probe registry — report interop` at C1

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Candidate (C1): `99c3bc88d704566197783f66b211ee0a830e0330`
- Section span: lines 2158–2197 of `SKILL.md`
- `section_sha256`: `cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52`
- Findings: **none** (`findings: []` in `T54W2Read23.json`)

Scratch/TMPDIR: `export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read23` (created; used for
every tool invocation below). No lane file was written or edited; no mutating git/jj command was
run. No tool was installed or upgraded (nothing needed).

## How the span was established

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
python3 .ufo/waves/round-54/reader-section.py \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  99c3bc88d704566197783f66b211ee0a830e0330 \
  "### Round-26 gate/probe registry — report interop"
```
→ `{"heading": "### Round-26 gate/probe registry — report interop", "cand":
"99c3bc88d704566197783f66b211ee0a830e0330", "start": 2158, "end": 2197,
"section_sha256": "cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52"}`

Recomputed independently from the C1 blob (`git show C1:SKILL.md`, `lines[2157:2197]` joined with
`\n`): sha256 = `cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52` (match).
The same section at C0 `59c38109bf11` hashes to the identical value (the C1 fix pass did not
touch this section; section bytes and their line span are stable).

`sha256sum` over line 2158–2197 with an added trailing newline gives a different digest
(`18504785…`); that is a delimiter artifact of the extraction, not a byte difference — the
frozen sectionize joins with `\n` and prints `cc23587b…`.

## Findings

None. Every anchor I could resolve resolves at C1; every selftest verdict string, count, exit arm
and write-scope prefix I could execute or read matches the bytes; no sentence in the section
contradicts another; no run-together token, missing space, duplicate word or empty/duplicated
parenthetical was found.

## Sweep actually run (so an empty list is auditable)

### 1. Anchor resolution — every backticked path in the section, checked against the C1 tree

```
git ls-tree -r --name-only 99c3bc88d704566197783f66b211ee0a830e0330   # plus derived directory set
# every `…`-quoted token containing "/" was tested for membership
```
Result: 79 distinct path-like tokens. Two did not match the tree set, both benign:
- `DIR/receipt.json` — a caller-chosen-directory placeholder (`--out DIR`), not a repo path.
- `.ufo/evidence/round-32/heldout/` — matched only after stripping the trailing `/`;
  `git ls-tree` lists `.ufo/evidence/round-32/heldout/HeldOut*.json` (directory exists on disk too).

All other cited paths exist at C1, including `tools/*.py` (31 tools), the `.ufo/evidence/round-*`
pins, `.ufo/waves/round-40|41/settlement-receipt.json`, `.ufo/evidence/round-49/c2/panel.json`,
`corpus/SOURCES.md`, `corpus/knowledge/golden-comparison-verdict.md`, and both
`tools/vendor/mutation-testing-{report-schema,metrics}-3.9.0.tgz`.

### 2. Registry rows quoted by the headline row (`line 2162`)

```
python3 -c "import json;d=json.load(open('tools/registry.json'));[print(json.dumps(r)) for r in d['rows'] if 'mte-interop' in r['name']]"
```
`mte-interop-selftest` expect `stdout_contains ["MTE_SELFTEST: 17/17 pass"]`, exit 0 (source
round-51-verifier-spotcheck); `mte-interop-check` expect
`"MTE_INTEROP: PASS legs_conforming=10/10"`, exit 0. Both match the row's `(17/17)` / `(10/10)`
and the tool's docstring exit map (`0/1/2/64`, `tools/mte-interop.py:35-36`).

### 3. Every quoted self-test verdict, executed

All with `TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read23`, `PYTHONDONTWRITEBYTECODE=1`,
cwd = lane.

| Row (line) | Claim | Observed | rc |
|---|---|---|---|
| 2162/2174 mte report interop | `MTE_SELFTEST: 17/17 pass` | `MTE_SELFTEST: 17/17 pass` | 0 |
| 2168 bash declared-witness study | `WITNESS_SELFTEST: 51/51 pass`, `VERDICT:` last line | `WITNESS_SELFTEST: 51/51 pass` then `VERDICT: PASS` (last) | 0 |
| 2169 command binding | `finding id COMMAND_BINDING_SELFTEST:` | `COMMAND_BINDING_SELFTEST: 44/44 pass` | 0 |
| 2170 context receipt replay | `SELFTEST: PASS (49/49)` | `SELFTEST: PASS (49/49)` | 0 |
| 2171 environment-profile differential | `ENVDIFF_SELFTEST: 9/9 pass` | `ENVDIFF_SELFTEST: 9/9 pass` | 0 |
| 2172 evidence disposition | `66/66 cases` | `SELFTEST: PASS (66/66)` | 0 |
| 2173 golden verdict classes | `GOLDEN_VERDICT_SELFTEST:` | `GOLDEN_VERDICT_SELFTEST: 3/3 pass` | 0 |
| 2175 fleet mutation runner | `MUTATE_SELFTEST` tally then terminal `VERDICT:` | `MUTATE_SELFTEST: %s/%s pass` at `tools/mutate-and-run.sh:2125`, `printf 'VERDICT: PASS'` at :2127 (static) | — |
| 2176 pbt staged-id | `cases=35 failed=0` | `PBT_STAGED_ID_SELFTEST: cases=35 failed=0` | 0 |
| 2177 pin disposition | `SELFTEST: PASS n/n` | `SELFTEST: PASS (19/19)` | 0 |
| 2178 receipt-measure | `RECEIPT_MEASURE_SELFTEST: 10/10 pass` | same | 0 |
| 2179 receipt-window | `RECEIPT_WINDOW_SELFTEST: 20/20 pass` (last line, exit 0) | same, last non-empty line | 0 |
| 2180 entry-registry walk | `SELFTEST: PASS (51 cases)` | `SELFTEST: PASS (51 cases)` | 0 |
| 2181 frozen registry replay | `REGISTRY_REPLAY_SELFTEST: 10/10 pass` | same | 0 |
| 2182 repeated control | `SELFTEST: PASS (29 cases) at exit 0` | `SELFTEST: PASS (29 cases)` | 0 |
| 2183 round21 facade | `ROUND21_MEASURE_SELFTEST: 13/13 pass` | same | 0 |
| 2184 shrink-case | `SHRINK_SELFTEST: cases=21 failed=0` | same | 0 |
| 2185 staged-id guard | `VERDICT: PASS` at 0 / `FAIL` at 1, counter line `STAGED_ID_GUARD_SELFTEST` | `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` then `VERDICT: PASS` | 0 |
| 2186 tally audit v2 | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` | 0 |
| 2187 tally audit v3 | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` | total = `len(cases)` 33 + `len(code_view_cases)` 2 = 35 (`tools/tally-audit-v3.py:805-925`); the 500 s dynamic run timed out on this host (rc 124) with all printed cases PASS — the row makes no runtime claim | (timeout) |
| 2188 tally audit undercount | `TALLY_AUDIT_SELFTEST: 11/11 pass` | same | 0 |
| 2189 traced input surface | `SELFTEST: n/n` on 0 | `sys.stdout.write("SELFTEST: %d/%d\n")` (`trace-inputs.py:965`); `n/n` is the format template | — |
| 2190 wave accounting | `SELFTEST_PASS`, `8/8 frozen plus 16/16 supplemental` | `ACCOUNTING_SELFTEST: 8/8 pass`, `ACCOUNTING_EXTRA_SELFTEST: 16/16 pass`, `FINDING: SELFTEST_PASS` | 0 |
| 2191 wave parent settlement | `WAVE_PARENT_SELFTEST: 3/3 pass, exit 0` | same | 0 |
| 2192 wave-route-mix | `ROUTEMIX_SELFTEST: 8/8 pass` | same | 0 |
| 2193 witness metadata | `SELFTEST: PASS 39/39` | same | 0 |
| 2194 write-form census v2 | `bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0` | identical string | 0 |
| 2195 write-path census v3 | `var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0` | identical string | 0 |
| 2196 write-path census v4 | `cases=15 failed=0` | identical string | 0 |
| 2197 write-path census | `planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1 noflag_unchanged=1`, 21-name `GATES` | identical string; `GATES` tuple has 21 names (`write-path-census.py:22`) | 0 |

### 4. Exit arms, probed by invocation (each compared with the row's verdict map)

```
python3 tools/write-path-census-v2.py --selftest --fixtures /nonexistent/f.json   → 1 (uncaught FileNotFoundError, as the row says)
python3 tools/write-path-census-v3.py --file /nonexistent/s.py                    → 1
python3 tools/write-path-census-v4.py --file /nonexistent/s.py                    → 1
python3 tools/write-path-census-v4.py                                             → 2 (usage)
python3 tools/write-path-census.py                                                → 2 (usage)
python3 tools/wave-route-mix.py --spec /nonexistent/s.json --config /nonexistent/c.yml → 2
python3 tools/wave-route-mix.py --bogus                                           → 64
python3 tools/wave-parent-settle.py                                               → 2
python3 tools/receipt-window.py                                                   → 64 (missing --contract/--receipts)
python3 tools/receipt-window.py --contract /nonexistent/c.json --receipts /nonexistent/r.json → 2
python3 tools/bash-witness-study.py --bogus                                        → 64
python3 tools/command-binding.py --bogus                                           → 64
python3 tools/context-capture.py --check --bogus                                   → 64
python3 tools/golden-verdict.py; --bogus                                           → 2; 2
python3 tools/pbt-staged-id.py --bogus                                              → 2
python3 tools/receipt-measure.py --repo; --bogus                                   → 2; 2
python3 tools/registry-replay.py --bogus                                           → 64
python3 tools/repeat-control.py --bogus                                            → 64 (invalid_usage)
python3 tools/shrink-case.py --bogus                                               → 2
python3 -I tools/staged-id-guard.py --bogus                                        → 2
python3 tools/tally-audit-v2.py --bogus; tally-audit-v3.py --bogus; tally-audit.py --bogus → 2; 2; 2
python3 tools/trace-inputs.py                                                      → 64
python3 tools/wave-accounting.py                                                   → 64
python3 tools/witness-metadata.py --bogus                                          → 2
python3 tools/mte-interop.py --bogus                                               → 64
python3 tools/pin-disposition.py                                                   → 2
python3 tools/round21-measure.py --bogus                                           → 64
python3 tools/round21-measure.py --claim c1 --repo . --rev deadbeef --json          → 2 (unknown rev)
```
Every result matches the row's `0/1/2/64` map, including the double-usage split in the
receipt-window row (argparse usage → 2 from `EXIT_CE`, missing required flags → 64 from
`EXIT_USAGE`, `tools/receipt-window.py:23,362`) and `tally-audit.py`'s 64 arm
(`return p.returncode` at :394 propagates a runner usage error; `grep 64` finds no literal, the
value is propagated).

`tally-audit-v2.py`'s 124→2 fold is real (`if p.returncode == 124: … return 2`, :588-590);
`tally-audit-v3.py` allocates the literal `/tmp/tameshi-r4-2-regression.XXXXXX` it discloses
(`auto_root()`, :408-433, `os.makedirs` + `atexit` rmtree) — the row's write-scope cell is
accurate, not stale.

### 5. CLI flags quoted by the rows, extracted from each parser

All quoted invocations resolve: `--check/--fleet-root/--emit/--selftest` (mte-interop);
`check|selftest` subcommands (bash-witness-study); `--bundle/--expected/--json` (command-binding);
`--check/--receipt/--expected/--json/--selftest` (context-capture); `--contract/--out/--jobs` (env-diff);
`--root/--dispositions` (evidence-disposition); `--check-entry/--classify-exit/--selftest` (golden-verdict);
`--regression|--target/--defects/--suite/--workdir` (mutate-and-run.sh); `--guard/--seed/--cases/--dump`
(pbt); `--manifest/--root` (pin-disposition); `--repo/--rev/--json` (receipt-measure);
`--contract/--receipts/--json` (receipt-window); `--rev/--only/--tag/--json/--registry/--root`
(registry-check); `--run/--repo/--rev/--requirements/--registry-baseline/--out` (registry-replay);
`--runs/--out/--snapshot` (repeat-control); `--claim/--repo/--rev/--json` (round21-measure);
`--pristine/--mutant/--case/--out` (shrink-case); `--registry/--staged/--map/--json` (staged-id-guard);
`--runner/--then-regression/--workdir` (all three tally audits); `--root/--out` (trace-inputs);
`--bundle/--expected` (wave-accounting); `--receipt` (wave-parent-settle); `--spec/--config/--max-share/--json`
(wave-route-mix); `--check/--lane-root/--companion/--emit/--json` (witness-metadata);
`--fixtures` (census v2), `--file/--fixtures` (v3), `--file/--json` (v4), `--census` (v1).

### 6. Write-scope literals, checked in source

`tameshi-r21-envdiff.` (env-diff), `context-capture-selftest-`, `tameshi-r12-repeat-control-selftest.`,
`tameshi-r13-pin-disposition-selftest.`, `receipt-measure-selftest.` (receipt-measure:251) plus
`tameshi-r20-measure.` (`stage/measure.py:82`, cited in the same row), `tally-audit-v2.`,
`tally-audit-v3.`, `trace-inputs-run-`, `pbt-staged-id-`, `mutation-testing-report-schema-3.9.0.tgz`,
`mutation-testing-metrics-3.9.0.tgz`, `dist.integrity`, `REGRESSION_TABLE`/`TABLE_*`,
`SELFTEST_REGISTRY`/`SELFTEST_STAGED_*`, `FLEET` in `.ufo/evidence/round-21/c2-count.py`,
`TemporaryDirectory` in write-path-census.py. All present where the cells say they are.

### 7. Pinned artifacts whose content the cells assert

- `.ufo/evidence/round-20/final/receipt-window-selftest.json` (C1 blob): `"exit": 0`, final stdout
  line `RECEIPT_WINDOW_SELFTEST: 20/20 pass`, `"measured_at": "2026-10-21T07:40:55.769783Z"` — the
  cell's "recorded 20/20 exit 0" holds. (Per-case prefixes in the recorded run still read `[ n/18]`;
  the recorded verdict line is 20/20, which is what the cell cites.)
- `.ufo/waves/round-40/settlement-receipt.json` → `WAVE_PARENT: verdict=SETTLED`, rc 0;
  `.ufo/waves/round-41/…` → `verdict=UNSETTLED`, rc 1 (the cell claims SETTLED/0 and UNSETTLED/1).
- `.ufo/evidence/round-12/BashWitness/declaration.json`: `inputs.target/spec/runner` digests and
  `declared.sha256`/`declared.rows` present (cell: "frozen target, spec and runner sha256"; "sha
  pinned in declaration.json").
- `tools/registry.json`: the two quoted rows and their expect strings.
- `tools/registry-replay.py`: `RUNNER_NOT_HELD` (:90), `RUNNER_CLEANUP_FAILED` (:87), `STREAM_LIMIT`
  (:97) are failure findings; `INVALID_OBSERVATIONS` (:77,84,95) is exit 2 — matches the row's split.
- `tools/write-path-census.py`: `GATES` has exactly 21 names (:22), census exits 1 iff a listed tool
  is missing (:134-145); selftest exit 1 on planted mismatch.
- `tools/env-diff.py` C0→C1 diff adds a `ScratchRootUnusable → exit 2` arm; the row's "2 and 64
  could-not-evaluate" is unaffected, and the `tameshi-r21-envdiff.` sandbox prefix is still current.

### 8. Surface scan for QUALITY-104 style defects

Regex sweeps over the whole section: duplicate words (`\b(\w+)\s+\1\b`) → none; `)` immediately
followed by a letter or a letter immediately followed by `(` → only the code literal `check()`;
runs of two spaces inside prose → none; empty `()` or back-to-back `)(` → none. No
run-together token, missing space or duplicate parenthetical found.

## Artifacts opened

- `SKILL.md` at C1 (blob via `git show`), lines 2158–2197; `SKILL.md` at C0 for the byte-identity check.
- `.ufo/waves/round-54/reader-section.py` (how the span/sha are computed).
- `tools/`: `mte-interop.py`, `bash-witness-study.py`, `command-binding.py`, `context-capture.py`,
  `env-diff.py`, `evidence-disposition.py`, `golden-verdict.py`, `mutate-and-run.sh`,
  `pbt-staged-id.py`, `pin-disposition.py`, `receipt-measure.py`, `receipt-window.py`,
  `registry-check.py`, `registry-replay.py`, `repeat-control.py`, `round21-measure.py`,
  `shrink-case.py`, `staged-id-guard.py`, `tally-audit.py`, `tally-audit-v2.py`,
  `tally-audit-v3.py`, `trace-inputs.py`, `wave-accounting.py`, `wave-parent-settle.py`,
  `wave-route-mix.py`, `witness-metadata.py`, `write-path-census.py`, `write-path-census-v2.py`,
  `write-path-census-v3.py`, `write-path-census-v4.py`, `registry.json`.
- `.ufo/evidence/round-20/final/receipt-window-selftest.json` (C1 blob),
  `.ufo/evidence/round-20/stage/measure.py` (:82 prefix),
  `.ufo/evidence/round-12/BashWitness/declaration.json`,
  `.ufo/evidence/round-40/census/fixtures.json`,
  `.ufo/evidence/round-41/census/fixtures.json`,
  `.ufo/waves/round-40/settlement-receipt.json`,
  `.ufo/waves/round-41/settlement-receipt.json`,
  `.ufo/evidence/round-21/c2-count.py`, `.ufo/evidence/round-32/heldout/` (listing),
  `.ufo/evidence/round-49/c2/panel.json` (existence).

## Commands run (verbatim, in order of use)

```
git show 99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md            # full blob, section sliced 2158-2197
python3 .ufo/waves/round-54/reader-section.py <lane> 99c3bc88… "### Round-26 gate/probe registry — report interop"
python3 .ufo/waves/round-54/reader-section.py <lane> 59c38109bf11  "### Round-26 gate/probe registry — report interop"
git ls-tree -r --name-only 99c3bc88d704566197783f66b211ee0a830e0330
git diff --stat 59c38109bf11 99c3bc88d704566197783f66b211ee0a830e0330
git diff 59c38109bf11 99c3bc88d704566197783f66b211ee0a830e0330 -- tools/env-diff.py
git rev-parse --verify 84aa673a^{commit}; git rev-parse --verify 84aa673^{commit}
grep / sed / python-ast inspections over the 31 tools listed under "Artifacts opened"
python3 tools/<tool> --selftest   (all tools in §3, TMPDIR=…, PYTHONDONTWRITEBYTECODE=1)
python3 tools/<tool> <usage-only invocation>   (all probes in §4)
python3 tools/wave-parent-settle.py --receipt .ufo/waves/round-40/settlement-receipt.json
python3 tools/wave-parent-settle.py --receipt .ufo/waves/round-41/settlement-receipt.json
python3 tools/write-path-census-v2.py --selftest --fixtures <copy of round-40 fixtures.json>
```

## Limits / notes

- `tools/tally-audit-v3.py --selftest` did not finish inside a 500 s wall on this shared host
  (rc 124; every case it printed before the cap was PASS). Its 35 total is exact from source
  (`len(cases)` = 33, `len(code_view_cases)` = 2, `tally-audit-v3.py:925`), and the row states no
  runtime for it; no stale cell follows.
- `tools/mte-interop.py --check` (the 10-leg leg-conforming run) was not executed — it replays the
  ten mutation legs against live sibling object stores and is not hermetic. The `10/10` cell is
  corroborated by `tools/registry.json`'s committed expect string
  (`MTE_INTEROP: PASS legs_conforming=10/10`) rather than by a new run.
- Two cells are deliberately generic rather than literal: `SELFTEST: PASS n/n` (pin disposition)
  and `SELFTEST: n/n` (trace inputs) name the tools' `%d/%d` templates, and
  `STAGED_ID_GUARD_SELFTEST: cases=N failed=M` names that tool's format; each was read as a
  template, not as a missing measurement, so none is reported as a defect.
- Provenance note (observed, not performed by this seat): after `T54W2Read23.json` was written, a
  lane commit `077d431` ("round-54: amendment 5 … wave-1/2 reports … committed") picked it up;
  `git show 077d431:.ufo/waves/round-54/w2/T54W2Read23.json` is byte-identical to the file this
  seat wrote (`git diff --stat HEAD -- <path>` empty). This seat ran no `git add`/`commit`/`push`,
  and `git diff --stat -- SKILL.md` is empty. The `.md` was still untracked when this report was
  written.
- `SELFTEST: PASS (51 cases) at 84aa673` (entry-registry walk) is measurement provenance, matching
  the same construction used in the evidence-disposition row ("… at rev 84aa673a"): the tool prints
  `SELFTEST: PASS (51 cases)` and no rev (`registry-check.py:1830`), and `84aa673` resolves to
  `84aa673a1a476e48ccf239335696f0518d08bae7` in the lane. Read as provenance it is true; I do not
  report it as a false quote.
