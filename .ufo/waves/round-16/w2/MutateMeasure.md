# MutateMeasure — box-3 credit mutation probe

**Verdict: partial — the committed `--selftest` kills 6/9 single-edit mutants; 3/9 survive (class fallback, record-verdict widening, whitespace-only trailing-blank stripping).**

## Scope and axes

- Axes: **depth + calibration**, specifically verification-fixture craft.
- Subject: `.ufo/evidence/round-16/measure.py` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.
- All `measure.py:L` references below mean that committed path at that revision, not a moving worktree file.
- Scratch: `/tmp/tameshi-r16w2-MutateMeasure-76ROSN` (allocated with the assigned mktemp prefix). Nine subjects had separate directories; every mutant changed exactly one production line. Selftest fixtures, expectations and test cases were not edited.
- This is detector evidence, not an admission/promotion or round judgment. A survivor is a coverage finding; the contract is unchanged.

## Commands, isolation and bounding

Observed preparation commands (exit 0):

```sh
mktemp -d /tmp/tameshi-r16w2-MutateMeasure-XXXXXX
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c699c8c36d6e4eca4b796b81a8247904aa145ec8:.ufo/evidence/round-16/measure.py
python3 --version
git --version
```

Observed runtime output: `Python 3.14.8`; `git version 2.56.0`. No tool was installed or updated.

The `git show` stdout (24,521 bytes) was materialized with the write tool as `pristine/measure.py` and each of the nine subject paths, then hashed. Mutations used surgical one-line edits. Exact original bytes held in memory were restored in a `finally` block after mutated runs.

Each subject used the following exact executable/argument pattern **three times**, in pristine → mutated → restored order; `<id>` is one of the literal IDs in the result table:

```text
/usr/bin/python3 /tmp/tameshi-r16w2-MutateMeasure-76ROSN/<id>/measure.py --selftest
cwd=/tmp/tameshi-r16w2-MutateMeasure-76ROSN/<id>
TMPDIR=/tmp/tameshi-r16w2-MutateMeasure-76ROSN/<id>
GIT_CONFIG_GLOBAL=/dev/null
GIT_CONFIG_NOSYSTEM=1
GIT_TERMINAL_PROMPT=0
PYTHONDONTWRITEBYTECODE=1
```

Each call used `subprocess.run(..., capture_output=True, text=True, timeout=90)`. Independent subjects ran concurrently in one synchronous nine-worker batch per phase; all calls completed, with no background jobs or subprocess timeouts. The script itself creates the synthetic git repo and invokes its own measurement CLI (`measure.py:375–405`); its `git add`/commit activity was confined to the synthetic repos under the assigned scratch. `TMPDIR` kept even its internally selected `tameshi-r16-CRMeasure-*` directories under that scratch.

For every phase, the following actual binaries also ran with the instantiated absolute paths (10-second bounds):

```text
sha256sum /tmp/tameshi-r16w2-MutateMeasure-76ROSN/<id>/measure.py
cmp --silent /tmp/tameshi-r16w2-MutateMeasure-76ROSN/<id>/measure.py /tmp/tameshi-r16w2-MutateMeasure-76ROSN/pristine/measure.py
```

All `sha256sum` exits were 0. `cmp` exits were **0 → 1 → 0** for every subject. All nine mutated hashes also matched the in-memory expected one-line edit; all nine before/restored hashes equaled the committed-byte hash. No baseline failed, so no kill is based on a failing baseline.

## Outcome matrix

Every pristine and restored run reported **33/33 pass, exit 0**. Every mutated run completed all 33 checks, and stderr was empty in all 27 runs.

| Subject | Mutation anchor | Pristine exit/pass | Mutated exit/pass | Restored exit/pass | Verdict |
|---|---|---|---|---|---|
| `M01-class` | `measure.py:184` | 0 / 33/33 | 0 / 33/33 | 0 / 33/33 | **survived** |
| `M02-count` | `measure.py:191` | 0 / 33/33 | 1 / 31/33 | 0 / 33/33 | **killed** |
| `M03-exec-verdict` | `measure.py:66` | 0 / 33/33 | 1 / 32/33 | 0 / 33/33 | **killed** |
| `M04-record-verdict` | `measure.py:67` | 0 / 33/33 | 0 / 33/33 | 0 / 33/33 | **survived** |
| `M05-link` | `measure.py:263` | 0 / 33/33 | 1 / 31/33 | 0 / 33/33 | **killed** |
| `M06-sha` | `measure.py:232` | 0 / 33/33 | 1 / 26/33 | 0 / 33/33 | **killed** |
| `M07-preamble` | `measure.py:115` | 0 / 33/33 | 1 / 27/33 | 0 / 33/33 | **killed** |
| `M08-fence` | `measure.py:111` | 0 / 33/33 | 1 / 18/33 | 0 / 33/33 | **killed** |
| `M09-strip` | `measure.py:125` | 0 / 33/33 | 0 / 33/33 | 0 / 33/33 | **survived** |

Totals: **6 killed, 3 survived, 0 inconclusive**, over 27 selftest invocations.

## Single-edit probes and actual detector output

### M01-class — class check

Anchor: `.ufo/evidence/round-16/measure.py:184` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.

```diff
-    if cls == 'instruction':
+    if cls != 'record':
```

Expected detector before running: No named case predicted: fixtures use only instruction/record; unknown class is unprobed..

[INFERENCE from the edited branch] An unknown/missing class with an executed-ok verdict and a positive command count is treated as an instruction rather than reaching the class rejection at measure.py:199. The fixture generator supplies instruction at :363, and the only class reassignment supplies record at :519; the selftest does not supply an unknown/missing class.

Observed: **survived**, mutated exit **0**, empty stderr.

```text
MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M01-class/tameshi-r16-CRMeasure-v5zbdbzr)
```

Killing selftest case: **none**. All 33 assertions passed on mutated bytes. The unexercised defect described above is an inference from the code/fixture contrast, not a separately executed custom test.

### M02-count — commands count

Anchor: `.ufo/evidence/round-16/measure.py:191` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.

```diff
-        if cmd_count <= 0:
+        if cmd_count < 0:
```

Expected detector before running: nocmd-score-6 and nocmd-reason.

The zero-command boundary is attacked; accepting 0 bypasses the required positive command-count rule.

Observed: **killed**, mutated exit **1**, empty stderr.

```text
FAIL nocmd-score-6
FAIL nocmd-reason
MEASURE_SELFTEST: 31/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M02-count/tameshi-r16-CRMeasure-0hnl39pc)
```

Killing assertions: `nocmd-score-6` (`measure.py:499`), `nocmd-reason` (`measure.py:500`).

### M03-exec-verdict — instruction verdict set

Anchor: `.ufo/evidence/round-16/measure.py:66` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.

```diff
-EXEC_VERDICTS = frozenset(('executed-ok', 'gap-minor'))
+EXEC_VERDICTS = frozenset(('executed-ok', 'gap-minor', 'verified-record'))
```

Expected detector before running: instr-verified-nocredit.

An instruction is allowed to claim verified-record. The explicit negative case at :505–514 detects this.

Observed: **killed**, mutated exit **1**, empty stderr.

```text
FAIL instr-verified-nocredit
MEASURE_SELFTEST: 32/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M03-exec-verdict/tameshi-r16-CRMeasure-enn3utz0)
```

Killing assertions: `instr-verified-nocredit` (`measure.py:511`).

### M04-record-verdict — record verdict set

Anchor: `.ufo/evidence/round-16/measure.py:67` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.

```diff
-REC_VERDICTS = frozenset(('verified-record', 'gap-minor'))
+REC_VERDICTS = frozenset(('verified-record', 'gap-minor', 'executed-ok'))
```

Expected detector before running: No named case predicted: record fixture uses only verified-record; record/executed-ok is unprobed..

[INFERENCE from the edited allowlist] A record can claim executed-ok, contrary to the class-conditional allowlist. The record fixture at :516–527 supplies only verified-record, so its positive case remains green.

Observed: **survived**, mutated exit **0**, empty stderr.

```text
MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M04-record-verdict/tameshi-r16-CRMeasure-9pyl_lt0)
```

Killing selftest case: **none**. All 33 assertions passed on mutated bytes. The unexercised defect described above is an inference from the code/fixture contrast, not a separately executed custom test.

### M05-link — SHONEN link gate

Anchor: `.ufo/evidence/round-16/measure.py:263` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.

```diff
-    box3_points = box3_marked and box3_link and cr['box3_full_page']
+    box3_points = box3_marked and cr['box3_full_page']
```

Expected detector before running: nolink-flag and nolink-score-6.

The final points predicate no longer requires the SHONEN box-3 ledger link, although the independently reported link flag remains unchanged.

Observed: **killed**, mutated exit **1**, empty stderr.

```text
FAIL nolink-flag
FAIL nolink-score-6
MEASURE_SELFTEST: 31/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M05-link/tameshi-r16-CRMeasure-yrgjmxk3)
```

Killing assertions: `nolink-flag` (`measure.py:535`), `nolink-score-6` (`measure.py:537`).

### M06-sha — SHA match

Anchor: `.ufo/evidence/round-16/measure.py:232` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.

```diff
-        matches = by_sha.get(sec['sha256'], [])
+        matches = by_sha.get(sec['sha256'], entries)
```

Expected detector before running: missing-section-covered3 and bytechange-covered3 (plus reason/score checks).

An absent exact SHA match falls back to all ledger entries, allowing an unrelated credited entry to cover the section. Both missing-entry and changed-byte cases detect this.

Observed: **killed**, mutated exit **1**, empty stderr.

```text
FAIL missing-section-covered3
FAIL missing-section-box3
FAIL missing-section-heading
FAIL missing-section-score-6
FAIL bytechange-covered3
FAIL bytechange-reason
FAIL bytechange-score-6
MEASURE_SELFTEST: 26/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M06-sha/tameshi-r16-CRMeasure-x_0fl51p)
```

Killing assertions: `missing-section-covered3` (`measure.py:457`), `missing-section-box3` (`measure.py:458`), `missing-section-heading` (`measure.py:459`), `missing-section-score-6` (`measure.py:462`), `bytechange-covered3` (`measure.py:478`), `bytechange-reason` (`measure.py:479`), `bytechange-score-6` (`measure.py:482`).

### M07-preamble — preamble sectioning

Anchor: `.ufo/evidence/round-16/measure.py:115` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.

```diff
-        if heads[0] > 0:
+        if heads[0] == 0:
```

Expected detector before running: no-ledger-sections and full-ledger-covered.

The preamble condition is inverted to first-heading-at-zero, so the synthetic nonempty preamble is omitted. The section-count assertion detects it.

Observed: **killed**, mutated exit **1**, empty stderr.

```text
FAIL no-ledger-sections fence-hidden heading excluded, preamble counted
FAIL full-ledger-covered
FAIL missing-section-covered3
FAIL blocking-covered3
FAIL bytechange-covered3
FAIL record-credited
MEASURE_SELFTEST: 27/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M07-preamble/tameshi-r16-CRMeasure-axcsm8ut)
```

Killing assertions: `no-ledger-sections` (`measure.py:432`), `full-ledger-covered` (`measure.py:447`), `missing-section-covered3` (`measure.py:457`), `blocking-covered3` (`measure.py:468`), `bytechange-covered3` (`measure.py:478`), `record-credited` (`measure.py:525`).

### M08-fence — fenced sectioning

Anchor: `.ufo/evidence/round-16/measure.py:111` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.

```diff
-        if not in_fence and HEADING_RE.match(line):
+        if HEADING_RE.match(line):
```

Expected detector before running: no-ledger-sections and full-ledger-covered.

Headings inside triple-backtick fences are no longer excluded. The synthetic hidden heading at :301 is exposed, and the section-count assertion detects it.

Observed: **killed**, mutated exit **1**, empty stderr.

```text
FAIL no-ledger-sections fence-hidden heading excluded, preamble counted
FAIL full-ledger-covered
FAIL full-ledger-box3
FAIL full-ledger-score-8
FAIL missing-section-covered3
FAIL missing-section-heading
FAIL blocking-covered3
FAIL blocking-reason
FAIL bytechange-covered3
FAIL bytechange-reason
FAIL badverdict-score-6
FAIL nocmd-reason
FAIL instr-verified-nocredit
FAIL record-credited
FAIL nolink-fullpage
MEASURE_SELFTEST: 18/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M08-fence/tameshi-r16-CRMeasure-nsne4am5)
```

Killing assertions: `no-ledger-sections` (`measure.py:432`), `full-ledger-covered` (`measure.py:447`), `full-ledger-box3` (`measure.py:450`), `full-ledger-score-8` (`measure.py:451`), `missing-section-covered3` (`measure.py:457`), `missing-section-heading` (`measure.py:459`), `blocking-covered3` (`measure.py:468`), `blocking-reason` (`measure.py:469`), `bytechange-covered3` (`measure.py:478`), `bytechange-reason` (`measure.py:479`), `badverdict-score-6` (`measure.py:490`), `nocmd-reason` (`measure.py:500`), `instr-verified-nocredit` (`measure.py:511`), `record-credited` (`measure.py:525`), `nolink-fullpage` (`measure.py:534`).

### M09-strip — whitespace-only trailing blank stripping

Anchor: `.ufo/evidence/round-16/measure.py:125` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.

```diff
-        while body_lines and body_lines[-1].strip() == '':
+        while body_lines and body_lines[-1] == '':
```

Expected detector before running: No named case predicted: fixture trailing blanks are empty strings, not whitespace-only..

[INFERENCE from the edited condition] Space-only or tab-only trailing lines are retained instead of stripped; the fixture's trailing blank strings at :291–307 are all empty strings. This mutation leaves that fixture unchanged. The independent expectation helper still calls strip() at :337–340; it was not edited.

Observed: **survived**, mutated exit **0**, empty stderr.

```text
MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M09-strip/tameshi-r16-CRMeasure-binl83f3)
```

Killing selftest case: **none**. All 33 assertions passed on mutated bytes. The unexercised defect described above is an inference from the code/fixture contrast, not a separately executed custom test.

## Hash and exact-restoration evidence

Pristine committed-byte SHA-256 (also every subject before mutation and after restoration):

```text
dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e
```

| Subject | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 | cmp before/mutated/restored |
|---|---|---|---|---|
| `M01-class` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | `59ea0cc6416780d244185f73591c499b3709e5052e208fb68aac42eb43c34e9a` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | 0/1/0 |
| `M02-count` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | `41865c27cbd6d1c749da8e6df3f1ae6fdb2af01c7d4b735d678e59de10415551` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | 0/1/0 |
| `M03-exec-verdict` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | `af9be2a020cb0d373266203b52fe463578cf846088769f781f68895bcd861afe` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | 0/1/0 |
| `M04-record-verdict` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | `c49f494c98072e1004880f785ca62ba9ff31610ded6dc56dedca44741b563281` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | 0/1/0 |
| `M05-link` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | `b68f8a7242825be70b7dc4dd3713b63124e491c8d497311c7b4ab478b5255279` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | 0/1/0 |
| `M06-sha` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | `d1ec3bafa261bc52d3ee5a086cc99330d6c0e19dcb3973f26f4ea911f3c29418` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | 0/1/0 |
| `M07-preamble` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | `4731a5ee33dabda6127264c40763704fb8d8c53120244cdbd003862ec12c488c` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | 0/1/0 |
| `M08-fence` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | `2f56a5ea04deeaa61bdedf11336890b3c76bc8fa6ed1737df219a19b001d1718` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | 0/1/0 |
| `M09-strip` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | `7c72a844cad623a2bed293e17680c080987116d1e9e232d4f6af77340ed6be59` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` | 0/1/0 |

Restoration did not merely return the tests to green: full-file `cmp --silent` returned 0 for every restored subject, and the SHA-256 returned exactly to the committed-byte value. Each restored subject was then tested using the same path, environment and bound as its pristine/mutated runs.

## Actual pristine/restored terminal summaries

These are the actual summary lines from each run (exit 0 for every line below); mutated key output is retained in the individual probe sections.

**M01-class**

```text
pristine: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M01-class/tameshi-r16-CRMeasure-k3a6jo2x)
restored: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M01-class/tameshi-r16-CRMeasure-d4n41yfk)
```

**M02-count**

```text
pristine: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M02-count/tameshi-r16-CRMeasure-3v53rwxp)
restored: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M02-count/tameshi-r16-CRMeasure-egaxt1_k)
```

**M03-exec-verdict**

```text
pristine: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M03-exec-verdict/tameshi-r16-CRMeasure-uj7v3r5i)
restored: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M03-exec-verdict/tameshi-r16-CRMeasure-hm1llxt9)
```

**M04-record-verdict**

```text
pristine: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M04-record-verdict/tameshi-r16-CRMeasure-t9se9ywg)
restored: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M04-record-verdict/tameshi-r16-CRMeasure-dwhgvzhx)
```

**M05-link**

```text
pristine: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M05-link/tameshi-r16-CRMeasure-l3x3vgcj)
restored: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M05-link/tameshi-r16-CRMeasure-oaetfl4e)
```

**M06-sha**

```text
pristine: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M06-sha/tameshi-r16-CRMeasure-66xbvrp0)
restored: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M06-sha/tameshi-r16-CRMeasure-bzkxaba1)
```

**M07-preamble**

```text
pristine: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M07-preamble/tameshi-r16-CRMeasure-f51v_2r0)
restored: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M07-preamble/tameshi-r16-CRMeasure-yhvwcogf)
```

**M08-fence**

```text
pristine: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M08-fence/tameshi-r16-CRMeasure-egl01xc5)
restored: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M08-fence/tameshi-r16-CRMeasure-mm2c_34z)
```

**M09-strip**

```text
pristine: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M09-strip/tameshi-r16-CRMeasure-c4px17_5)
restored: MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16w2-MutateMeasure-76ROSN/M09-strip/tameshi-r16-CRMeasure-g7qc1hvj)
```

## Evidence retention and boundary

Full command, cwd, environment overrides, SHA, cmp exit, process exit, stdout and stderr for all 27 runs remain in scratch as `<id>/pristine.json`, `<id>/mutated.json`, and `<id>/restored.json`. Those temporary paths are convenience artifacts only; this report embeds the mutations, revision, exact commands, hashes, exits and key output needed to reconstruct the probe.

Only this report was written in the lane. The lane tool, ledgers, tests, docs and sibling source trees were not edited; no lane git add/commit/push or other runtime/REA call was performed. No extra probes, contract edits, or implementation fixes were made.
