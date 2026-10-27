# T51W2ScribeFinalLesson — final lesson fact check (round 51, wave 2)

Seat: `T51W2ScribeFinalLesson` (leaf, no subagents). Item: read the integrated
`corpus/lessons/round-51.md`, the W1 source/entry/falsifier reports, the W2 reviewer outputs and the
candidate receipts; draft a corrections block **only** for factual mismatches; write no lane file.

State read: lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, HEAD `f133b47f27ec60e6527e7436c8a6df8c4fdf996c`
(the only commit that has the lesson — `git log --oneline -- corpus/lessons/round-51.md` prints `f133b47`
alone; the lesson is 53 lines). Base `9962033fd7a75aa2f2847e979dd687a5d28505a1`, content candidate
`6d8c11e378aa90b12650808e1b79270742935f15`, amendment-2 freeze `9d023aed5e71391c7819d1256e19a35b26fdcb31`.
All repo reads were `git show <rev>:<path>`, `grep`, `sed` and sha256 over existing files; nothing in the
lane, fleet or a sibling repo was written, no fixture or clone was created, no TMPDIR scratch was needed.

**Verdict: 5 corrections required, 1 recommended disclosure addition, 24 checked claims confirmed.**
No claim rule, target, counter, spec or contract byte is questioned; every correction is to prose in the
lesson that does not match committed bytes or the measured state at `f133b47`.

---

## 1. Corrections block — exact replacements

Each entry gives the current text verbatim (as it stands in `corpus/lessons/round-51.md`), the replacement,
and the observation that forces it. Line numbers are the file's lines at `f133b47`.

### C-1 — line 45: no-harm is asserted at a deciding revision that does not exist, and the 64/64 restoration is not a lane measurement

**Current (whole bullet):**

```
- No-harm at the deciding revision: `.ufo/evidence/round-51/after/no-harm.stdout` (eleven monitors). The round-21 cold-read monitor fell to 44/64 (score 6) after runner and registry changes, then the trace-bound 20-section re-key restored 64/64 (score 8); all readers and traces are listed under `.ufo/evidence/round-51/coldread/`.
```

**Replace with:**

```
- No-harm is measured at CAND, not at a deciding revision: `.ufo/evidence/round-51/after/` does not exist at `f133b47` (LOG.md:2420 defers the deciding receipts to closure). At `6d8c11e` the eleven-monitor no-harm prints ten `ok` and `NOHARM coldread-floor score=6 credited=44 RED` (`T51W2CritNoHarm.md` F1/F4), and the strict round-21 monitor independently reports 44/64, score 6 — the same 44/64 the base simulation reaches by appending one byte to the runner (`.ufo/waves/round-51/w1/T51CritRekey-sim-receipt.txt`: `covered=44/64`, 20 dropped headings). The trace-bound re-key has not landed on the lane: `.ufo/evidence/round-51/coldread/readers.json` names one reader for each of the 20 lost headings while `coldread/reads/` holds no trace, so 64/64 (score 8) is a fixture result only (`T51ExecRekey.md:74,176,189`, re-key commit `0f28deeb` in a `--shared` clone).
```

**Observed:**

- `ls -d .ufo/evidence/round-51/after` → `No such file or directory`; the directory the deciding run writes
  (`deciding-run.sh` takes `OUTDIR` and writes `$OUT/no-harm.stdout`, `$OUT/c1.stdout` …) has never been created.
- `LOG.md:2420`: “deciding receipts and final lane revision to be appended when the round closes.”
- `.ufo/evidence/round-51/coldread/readers.json`: 20 keys (one per lost heading), 20 distinct reader ids, all
  non-empty; `ls .ufo/evidence/round-51/coldread/reads` → directory exists, 0 files.
- `T51CritRekey-sim-receipt.txt` (base + one appended byte to `tools/mutate-and-run.sh`, sim commit
  `45ea5934`): `covered=44/64`, 20 headings dropped, section `### Gate/probe registry` among them.
- W2 `T51W2CritNoHarm.md` F1, from its own command on CAND: `NOHARM coldread-floor score=6 credited=44 RED`,
  “The registry section (14) is input-drift, not `no-ledger-entry`.” F4: the other ten monitors `ok`.
- `T51ExecRekey.md:74` — “`TARGETS 20 … (44/64 score 6)`, exit 0; commit `0f28deeb…`; monitor 64/64” (fixture
  clone); `:176` “`monitor-after-0f28deeb.json` (64/64, score 8)”; `:189` “after the re-key commit 64/64 score 8,
  precheck lost=0”.

`eleven monitors` itself is correct: `no-harm.sh` prints eleven `NOHARM …` lines and `deciding-run.sh` requires
`grep -c '^NOHARM .* ok$' = 11`; the correction is the tense/receipt, not the count.

### C-2 — line 28: C3's “decisive counter output” and the report do not exist at this revision

**Current (exact substring):**

```
Therefore C3 does not verify: its decisive counter output is `.ufo/evidence/round-51/after/c3.stdout` and is reported verbatim in the report.
```

**Replace with:**

```
Therefore C3 does not verify. A fresh clone at CAND gives `C3_R51: rev=6d8c11e378aa90b12650808e1b79270742935f15 tools=30 rows=32 covered=29 missing=1 deleted=0 selftest_fail_rows=2 total=1 C3_R51_PASS=false`, the single miss being `tools/round21-measure.py` (`T51W2ExecTool02/c3-counter-full-run.txt`; `T51W2CritC3Truth.md` F1). The deciding-run receipt `.ufo/evidence/round-51/after/c3.stdout` and the round report do not exist at `f133b47`; the line above is the wave-2 CAND measurement.
```

**Observed:** `.ufo/waves/round-51/w2/@P@ExecTool02/c3-counter-full-run.txt`, last line, exact as quoted
(`C3_TOOL tools/round21-measure.py: MISSING (line 2157 selftest-exit=1 last=)`); `after/` absent; no round-51
report exists anywhere in the lane (`find . -path ./.git -prune -o -name '*round-51*' -print` returns no report
path and no `.ufo/reports/round-51*`).

### C-3 — line 18: the C1 survivor list names 5 of the 7 measured survivors

**Current (exact substring):**

```
remaining weaknesses include duplicate ids, wrong rounds, long pointers, unsupported status phrase and a table header without `ground`.
```

**Replace with:**

```
remaining weaknesses are duplicate ids (M02), an ignored round value (M03), a pointer span over the counter's six-line limit (M04), a pointer without the expected status phrase (M05), `held` accepted as a substring of `partly held` (M10), a table header without `ground` (M12) and a `mined` row with no used-by path (M15) — every one of the seven has a forge (`T51MutC1Counter.md` §Surviving blind spots; `M10_held_for_partly-forge.txt`, `M15_skip_mined_empty-forge.txt`).
```

**Observed:** `T51MutC1Counter.md` — “14 isolated, behavior-bearing single-edit mutants tested; 7 killed, 7
survived.” Survivors: M02, M03, M04, M05, M10, M12, M15, each with a forge listed and the mutant passing while
pristine fails (M10: `held` for `partly held` on F2/F4/F8, pristine `frontier_bad=3`; M15: `mined` row with
used-by `—`, pristine `status_conflicts=1`). `corpus/QUALITY.md` criterion 101 requires “the round's lesson
**names the survivors**”, so the two omitted survivors are a criterion-101 gap, not only a wording preference.

### C-4 — line 16: F11/F12 finding is attributed to a report that does not contain it

**Current (exact substring):**

```
Two independent wave-1 readers re-derived all ten statuses and agreed with the frozen set; F11/F12 are fixture ids, not frontier rows (`T51CritExpectedA.md`, `T51CritExpectedB.md`).
```

**Replace with:**

```
Two independent wave-1 readers re-derived all ten statuses and agreed with the frozen set (`T51CritExpectedA.md`, F1-F5; `T51CritExpectedB.md`, F6-F10); F11/F12 are round-43 fixture ids, not frontier rows (`T51CritExpectedB.md:60-63,96`; README:548-555).
```

**Observed:** `grep -c F11 .ufo/waves/round-51/w1/T51CritExpectedA.md` → `0` (that seat's item was F1-F5 and it
states “No disagreement found”); `T51CritExpectedB.md:60-63` — “F11 / F12 (README:548-555) are fixture ids, not
frontier grounds”, resolving them as `F11_outflag_namespace` / `F12_method_two_returns`, `:96` repeats it.

### C-5 — line 10: the S273 quotes have no locations, which CORPUS rule 1 requires of the lesson's `## Gate`

**Current (exact substring, end of the S273 bullet):**

```
“the exit status of the last command substitution performed” (9). The empirical composition matters
```

**Replace with:**

```
“the exit status of the last command substitution performed” (9). Quote locations in the stored snapshot: `-e` item lines 6548-6553 and 6554-6560, `pipefail` item lines 6707-6709, §Simple Commands lines 4172-4174 (S273's own copy-line span for the assignment-status rule stops at 4173, one line before the fourth quote's words end). The empirical composition matters
```

**Observed:** `CORPUS.md` §SOURCES.md rule 1 — “The round lesson's `## Gate` records, for every new row, the URL,
the access date, and a ≤25-word quote **with its location** grounding `teaches`.” The lesson's S272 bullet gives
its location (“pinned lines 6-7”); the S273 bullet gives four quotes with word counts and no location. Verified
line positions in `.ufo/waves/round-51/w1/T51ScribeRowBash/chet-bashref.html` after tag-stripping:
`6548 Exit immediately if`, `6553 returns a non-zero status.`, `6554 The shell does not exit if the command that
fails is part of the`, `6560 any command in a pipeline but the last`, `6707 If set, the return value of a pipeline
is the value of the last`, `6709 commands in the pipeline exit successfully.`, `4173 the exit status of the
command is the exit status of`, `4174 the last command substitution performed.` The four quotes themselves are
real: tag-stripped full-text search finds quotes 3 and 4 verbatim, and quotes 1 and 2 at the cited lines
(the quotes span markup, which is why a raw substring grep returns 0 for two of them).
Row-level nit for the L1 (not the lesson): `corpus/SOURCES.md:148` cell 7 cites “copy lines 4172-4173” for the
assignment-status rule, while the sentence carrying the fourth quote runs to 4174 and the zero-status line to
4176.

### C-6 — line 28: recommended disclosure (omission, not a false sentence) — two of the 30 registry rows misdescribe their tool

**Insert after (exact substring):**

```
the round-51 table rows were reviewed by 30 executors, not admitted solely on the counter's output.
```

**Add:**

```
 Two rows still misdescribe their tool at CAND and the counter's first-token check cannot see it: the `entry-registry walk` row quotes the selftest's last line as `SELFTEST: PASS (51 cases) at 84aa673` where the observed last line is `SELFTEST: PASS (51 cases)` (`T51W2ExecTool02/c3-counter-full-run.txt`, `tools/registry-check.py` line; `T51W2CritC3Truth.md` F2), and the `round-20 receipt-window measure` row glosses exit 2 as usage-only while a non-git `--repo` with no `--rev` also exits 2 with `MEASURE: COULD_NOT_EVALUATE (no revision)` (`@P@ExecTool11/03-exit-code-survey.txt`, cases I-J). Neither affects the frozen verdict: C3 is false for the `round21-measure.py` miss alone.
```

**Observed:** candidate `SKILL.md:2154` row cell — “finding id SELFTEST: last line SELFTEST: PASS (51 cases) at
84aa673”; counter receipt last field for that tool — `covered line 2154 selftest exit=0 last=SELFTEST: PASS (51
cases)` (the `at 84aa673` suffix is not in the captured output). `SKILL.md:2152` verdict map — “2
could-not-evaluate only on usage, that is missing --repo value, unknown flag, or --selftest mixed with other
arguments”; executor survey cases I and J show exit 2 with `MEASURE: COULD_NOT_EVALUATE (no revision)` for
`--repo` a non-git directory / a plain file with no `--rev` (also case H: `--help` exits 0 on usage, which the
row's `0 clean, six items PASS at REV` does not name). The lesson does not claim these rows are correct, so this
is a disclosure addition; without it the `## C3` paragraph reads as if executor review left the table accurate.

---

## 2. `## Gate` audit — S272 / S273 against the SOURCES rows and the dates

| lesson claim | checked against | result |
|---|---|---|
| S272 row is at `corpus/SOURCES.md:147` | `grep -n S272 corpus/SOURCES.md` → `147:` | ✔ |
| S272 pin `e64e81b8…` | `git -C ../kagi-shokunin show -s --format='%H %ai'` → `2026-09-28 18:20:49 -0300` | ✔ (lesson: “kagi round-9, 2026-09-28”) |
| blob sha256 `c138d34c…6c70feb`, 451 lines, mode `100755` | `cat-file blob e64e81b8:corpus/drift-pins.sh \| sha256sum` → `c138d34c…6c70feb`; `wc -l` → `451`; `ls-tree` → `100755 blob 8a2903dc…` | ✔ |
| “unchanged at kagi HEAD” | kagi HEAD `69b61db46be4ed955994f6f1d1cba522bc5f4e97`, dated 2026-10-25 (before this round); `HEAD:corpus/drift-pins.sh` → same blob `8a2903dc…` | ✔ (so “no kagi code changed this round” also holds) |
| quote `(15 words)`, “pinned lines 6-7” | pinned blob lines 6-7: “…v2 compares the” / “live host against two committed baselines and exits non-zero on any change.” Word count 15 (v2…change) | ✔ |
| “13-case `--selftest` ran from a scratch copy (exit 0)” | `T51ScribeRowGate.md` §1 — extracted blob, `TMPDIR=<scratch>/t bash drift-pins.sh --selftest` → `DRIFT_SELFTEST: PASS (13 cases)`, exit 0; 13 `run` calls at :408-438 | ✔ [report-sourced, not re-run by this seat] |
| “oracle at :403 uses an unanchored `grep -q` over captured output” | pinned blob `:399 out=$(… 2>&1)`, `:403 elif ! grep -q "$3" <<< "$out"; then` | ✔ |
| S273 row is at `corpus/SOURCES.md:148` | `grep -n S273` → `148:` | ✔ |
| “opened 2026-10-26 local time (UTC receipt is 2026-10-27T00:22Z)” | row opened cell `2026-10-26`; `w1/T51ScribeRowBash/fetch-receipt.txt` — `# local: Mon 26 Oct 2026 09:21:50 PM -03  UTC: 2026-10-27T00:21:50Z`, fetch B1 `utc=2026-10-27T00:22:10Z`; row text states the gnu.org page was unreachable “on 2026-10-27 UTC” | ✔ — the local/UTC split is disclosed, not smoothed (matches W2 `T51W2CritSourceEntry.md` F2) |
| HTTP 200, 1,040,870 bytes, sha256 `b91026ac…` | `wc -c` on the snapshot → `1040870`; `sha256sum` → `b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4`; B1 and B2 receipts identical | ✔ |
| snapshot path | `.ufo/waves/round-51/w1/T51ScribeRowBash/chet-bashref.html` exists, same bytes | ✔ |
| “eight HTTP 000 / curl 28 attempts … disclosed in the row and seat report” | `T51ScribeRowBash.md` attempt A “8 attempts, 2026-10-27T00:12Z … 00:22:10Z” and F1 enumerating eight shapes (node page https ×2, single-page, `-4`, `http://`, no-www, savannah-checkouts, receipt attempt); row cell repeats “eight attempts, HTTP 000, 0 bytes, connect timeouts” | ✔ |
| “same manual is already held as Savannah texi rows S097/S104” | `corpus/SOURCES.md:106` (S097) and `:113` (S104), both the 5.3 `doc/bashref.texi` at `b8c60bc9` | ✔ |
| quotes “all ≤25 words” | measured 9 / 19 / 20 / 9 words, each found at the lines given in C-5 | ✔ |
| Gate intro: “URL, local access date, located quote and source limitations” | CORPUS rule 1 requires URL + access date + ≤25-word quote **with location** | ✘ for S273's locations → C-5 |

Both rows exist as 11-cell pipe rows (candidate `SOURCES.md:147-148`), status `mined`, used-by
`corpus/knowledge/mutation-case-kagi-drift-pins.md`, and the end census reports no `E`/`W04` line for either
(`.ufo/evidence/round-51/census-end.stdout`, exit `0`).

## 3. `## Mistakes` audit — captured-by and falsifier bytes

| row | claim under test | evidence | result |
|---|---|---|---|
| `oracle-leak` | evidence pointer “`:400, :403, :158`” | pinned blob `:400 out=$(… 2>&1)`, `:403 grep -q "$3" <<< "$out"`, `:158 printf 'DRIFT   %s %s\n' "$p" …` | ✔ |
| `oracle-leak` | “making three detectable mutants appear to survive” | sweep: `K_GONE_ARM`, `K_AMBIG_GT`, `K_SHAPE_OPTIN` `SURVIVED (exit=0)`; A→B matrix “Only the three kill-aimed misses flip with the sandbox name; no other verdict flips” (`T51LabSandboxLeak.md:52-63`); three repeats | ✔ |
| `oracle-leak` | captured-by “none — existing QUALITY 101 covers counter reach and measurement, not path tokens participating in verdict oracles” | `QUALITY.md` criterion 101 (“binds reach and disclosure, not a kill rate”; mutation-probe disclosure) — no oracle-input clause; criterion 102 (landed this round) is the first rule over oracle inputs | ✔ |
| `oracle-leak` | fix “QUALITY criterion 102 requires a neutral-path vs hostile-path one-variable comparison before a recorded mutation verdict” | `corpus/QUALITY.md` §Criterion 102 — “run the same target, spec and command under a neutral scratch root … and a hostile root … Their verdicts must agree”; check prints `ORACLE_NAME <id> <neutral> <hostile> <same\|DIFF>` | ✔ |
| `oracle-leak` | falsifier “id path exits 0 PASS, neutral path exits 1 FAIL” | `.exit` files: `red-gone-id.exit` = `0`, last line `DRIFT_SELFTEST: PASS (13 cases)`; `green-gone-neutral.exit` = `1`, last lines `drift-selftest: FAIL symbol gone: no /GONE/ in output` / `DRIFT_SELFTEST: FAIL (1/13 cases)` | ✔ |
| `oracle-leak` | “The gate is sibling-owned and read-only; no kagi code was changed this round.” | kagi HEAD commit dated 2026-10-25, none today; the S272 pin is read via `git show` | ✔ |
| `status-usedby-conflict` | pointer “`corpus/SOURCES.md:33` at base” | `git show 9962033f:corpus/SOURCES.md \| sed -n 33p` → the S022 row | ✔ |
| `status-usedby-conflict` | “S022 was `queued` although its used-by cell named an existing entry” | base row cell 9 `queued`, cell 12 `corpus/knowledge/fixture-shrinking-pilot.md` (exists) | ✔ |
| `status-usedby-conflict` | fix “flip only S022 `queued` → `mined`” | status-column diff base→HEAD: base 131 rows, HEAD 133; changed = `[('S022','queued','mined')]`; added `S272,S273`; removed none | ✔ — “no other existing row status changed” is exact |
| `status-usedby-conflict` | “CTL_0 shows the conflict, the scratch S022-only flip clears it” | `control/controls.stdout:1` CTL_0 `status_conflicts=1 … total=11`; `:2` CTL_S022 `status_conflicts=0 … total=10` (the conflict clears; C1 still false on the stale table, which the lesson does not claim otherwise) | ✔ |
| `status-usedby-conflict` | captured-by “CORPUS.md SOURCES contract v1: `mined` means cited by ≥1 used-by path” | `CORPUS.md` §SOURCES.md — “`mined` (cited by ≥1 path in `used-by`)” | ✔ |

## 4. Claims checked and left unchanged

| lesson claim | evidence observed | result |
|---|---|---|
| base `9962033f…`, freeze `fe335384`, amendment 1 `84aa673`, amendment 2 `9d023aed` | `git log --oneline`: `84aa673` “amendment 1”, `9d023ae` “amendment 2”; `freeze.json` “amended: amendment 1 … over fe335384; amendment 2 … over 84aa673a” | ✔ |
| “No claim predicate or counter changed after freeze” | sha256 at HEAD == `freeze.json`: c1 `ed696832…`, c2 `c2c80c0b…`, c3 `a3abbd3b…`, spec `a98271f6…`, `frontier-expected.json` `f5625241…`, `tools-base.json` `c71f4852…`; at CAND identical; `contract.json` `27e524a4…` (amended copy, digest matches the single amended file) | ✔ |
| selftests C1 6/6, C2 11/11, C3 10/10 | `quality/selftest-c1.stdout` `cases=6 failed=0`, c2 `cases=11 failed=0`, c3 `cases=10 failed=0`, all exit 0 | ✔ |
| reach 3/3 `calls_measure>0` | `quality/reach-r51.stdout`: `calls_measure=1/1/3`, `SELFTEST_REACH: files=3 failed=0` | ✔ |
| “stale table at README:76-87 held seven statuses” | base `README.md:76` header, `:77` separator, `:78-87` F1-F10; frozen expectations vs cells: F1 round, F2, F4, F5, F6, F8, F10 differ = 7; F3/F7/F9 unchanged (`T51ScribeFrontier.md` N2 agrees) | ✔ |
| “F9 basis correctly points to row 86”; note says `76-86` | base `README.md:86` = the F9 row; `frontier-expected.json` note says `76-86` (off-by-one already disclosed in the lesson's correction paragraph, recorded at `T51ScribeFrontier.md` N1) | ✔ (as disclosed) |
| ten `FRONTIER Fk: ok`, `status_conflicts=0`, `total=0`, `C1_R51_PASS=true` | `w1/T51ScribeFrontier.c1-receipt.txt` (`rev=6d236c76…`, `sources_rows=131`), plus negative control at `84aa673` `total=11 false` | ✔ |
| “14 behavior-bearing single edits, 7 killed / 7 survived” | `T51MutC1Counter.md` matrix + summary line; 7 forges | ✔ |
| C2 sweep: green control, restore OK, 2/10 KILLED (`K_MODE_CMP`,`K_COUNT_GE`), 8 SURVIVED, 7/10 predictions held | `c2/sweep/sweep.txt`: `CONTROL: GREEN`, `MUTATE_RESTORE: OK`, `killed=2 survived=8`, defect lines; spec predictions 5 KILLED/5 SURVIVED, hits = K_MODE_CMP, K_COUNT_GE + all five S_* | ✔ |
| “runner embeds that table exactly”; regression 10/10 | `tools/mutate-and-run.sh:643 TABLE_DRIFTPINS` if compared verdict-by-verdict to the sweep (K_MODE_CMP KILLED, K_GONE_ARM SURVIVED, K_AMBIG_GT SURVIVED, K_COUNT_GE KILLED, K_SHAPE_OPTIN SURVIVED, S_* SURVIVED); `T51ExecEmbed.md:81-83` `REGRESSION_TABLE bash-drift-pins: match=10/10 … flips=0`, `REGRESSION: PASS (cases=10 passed=10 …)` | ✔ |
| runner `--selftest` 107/107 | `T51ExecEmbed.md:79` `MUTATE_SELFTEST: 107/107 pass`, `:150` | ✔ [report-sourced] |
| neutral-name probe: exactly 3 flip, three repeats, byte-identical mutants | `T51LabSandboxLeak.md:52-63` matrix, `README.md:3` mutant sha table, W2 `T51W2CritQualityMistake.md` F2 (“exactly K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN change A=survived/rc0 to B=killed/rc1”) | ✔ |
| “Five remaining survivors have off-suite witnesses; none was found equivalent” | `T51LabWitSHACMP/HARDLINK/POLICY/DUPUNIQ/USAGEEXIT.md` — every verdict `HOLE` / “NOT equivalent”, no equivalence finding | ✔ |
| C2 counter probe: 15 blind spots, one redundant clause, one caught by D1/D2/D3 | `T51MutC2Counter.md` M01-M15 SURVIVED (B1-B15 forges), M16 `EQUIVALENT`, M17 `KILLED-by-D1/D2/D3` | ✔ |
| “counter certifies receipt predicates, not suite provenance; suite described in spec prose but not machine-bound” | `T51CritPrereg.md`; W2 `T51W2CritC2Registration.md` F1-F2 (spec has one prose suite sentence; counter parses receipt shape only) | ✔ |
| “runner and four dependent panel tools updated together” | `git diff --stat 9962033f 6d8c11e -- tools/`: exactly `mte-interop.py`, `mutate-and-run.sh`, `tally-audit-v2.py`, `tally-audit-v3.py`, `tally-audit.py`; panel constants `nlegs=9→10`, `st_driftpins` added, `TABLE_DRIFTPINS` wired | ✔ (see §5 note on the TMPDIR clause) |
| “Tools' only other change was honoring `TMPDIR` for scratch defaults” | runner diff: `mktemp -d /tmp/…` → `mktemp -d "${TMPDIR:-/tmp}/…"` in `--workdir`, `WORKDIR`, regression root; the four panel tools' diffs contain no `TMPDIR` hunk (`grep -c TMPDIR` on each diff = 0) | ✔ only if “Tools” is read as the runner; see §5 |
| “one row per 30 frozen tools” | last SKILL section `#### Gate/probe registry — round 51` at `:2138`, 31 `|` rows = header + 30 data rows; counter prints `rows=32` (header+separator+30) | ✔ |
| C3 blocker: `round21-measure.py --selftest` exits 1 in the clone; exit 0 and 13/13 with siblings | `T51W2CritC3Truth.md` F1 (`selftest-exit=1 last=`), `T51Row16.md:80-91,190` (`ROUND21_MEASURE_SELFTEST: 13/13 pass`, `T51Row16.selftest-siblings-present.txt`) | ✔ |
| “counter can be forged by rows that alias `--help --selftest`” | `T51CritC3Counter.md` fixture A (`tools/round21-measure.py --help --selftest`, `C3_R51_PASS=true` on a pure SKILL edit) | ✔ |
| “reviewed by 30 executors” | 30 `w1/T51Row*.md` seats (one per tool) | ✔ |
| C3 motivation overstated: “18 tools mentioned across twelve per-round registry sections; 12 not mentioned anywhere”; “checked 0 conforming rows at base” | `integrate/l1-notes.md` N1 (18/12 with the named twelve-section list); `control/controls.stdout:8` CTL_0 `rows=2 covered=0 missing=30` | ✔ |
| “registry has 133 rows and the next allocated id is S274” | end census `ok`; `grep -c` row pattern = 133; `SOURCES.md:502` `- Next unused id: S274 …`; `:500` still shows the pre-round `S272` line, as the earlier rounds' stale-next-id lines do | ✔ |
| “Census start exit 0; round-end census receipt in `census-end.*`” | `census-start.exit` = `0`; `census-end.exit` = `0`, stdout ends `ok` | ✔ |
| “No `considerthese/` proposal was adopted this round”; “Tools installed/updated: none” | `considerthese/2026-10-26.md` covers rounds 44-48 (no round-51 proposal); `LOG.md:2418` — “tools installed/updated: none (host RULES read; existing tools sufficed)” | ✔ |

## 5. Observations for the L1 (not corrections to the lesson)

1. **A wave-2 critic read a lesson that is not the committed one.** `T51W2CritQualityMistake.md` cites
   `corpus/lessons/round-51.md:30-35,64-75` and says the lesson “additionally calls `js-round-gate`,
   `js-sources-check`, and `js-cite-check` unchanged under naming changes (`…:72-75`)”. At `f133b47` the lesson
   is 53 lines, `## Mistakes` starts at line 30, and `grep -c js-round-gate corpus/lessons/round-51.md` = 0. Those
   line references match the draft in `w1/T51ScribeMistakes.md`, not the committed file. Its F3 finding about the
   three exit-only legs is therefore a review of a draft; the committed `## Mistakes` makes no such claim.
2. **Conflicting descriptions of the 20 lost sections' reasons — report verbatim, decide nothing.** This seat's
   brief says “19 `input-drift:tools/mutate-and-run.sh`, 1 registry section `no-ledger-entry`”. W2
   `T51W2CritNoHarm.md` F1 says: “19 lose credit with at least one `input-drift:tools/mutate-and-run.sh` …; the
   sole `no-ledger-entry` is section 20. The registry section (14) is input-drift, not `no-ledger-entry`.” The
   lesson states neither split, so no lesson text changes; the canonical monitor (`round-21/coldread/measure.py`)
   is the arbiter.
3. **S273 row-level nits** (row, not lesson): cell 7's copy-line span `4172-4173` stops before the fourth quote's
   words (4174) and before the zero-status line (4176); the row's `recheck` is `365d`, which is a cadence the
   contract's examples (`90d`, `180d`, `on-release`) do not list but does not forbid. Census reports no `E`/`W04`
   for S272/S273.
4. **C-6 basis:** the two misdescribed rows above are the only candidate-table defects this seat could observe
   directly; `T51W2CritC3Truth.md` F2 is the same finding from the counter side. They do not change
   `C3_R51_PASS=false`.

## 6. Limits of this check

- No counter, no gate self-test and no sweep was re-run. Measurements are either my own read-only observations
  (hashes, line contents, exit receipts, diffs) or committed seat receipts, and the latter are marked
  `[report-sourced]` where they stand in for a run (S272's 13-case selftest, 107/107, 13/13).
- The lesson's semantic C1 status basis is a frozen L1 reading; I checked it against the base table cells and the
  two re-derivations, not against an oracle of "latest declaration".
- Whether a deciding run later makes C-1/C-2 true is not knowable at `f133b47`; the corrections state the measured
  state and keep the pending paths identified as pending. If the deciding run lands before the lesson is finalized,
  C-1/C-2 should be re-worded to cite `after/no-harm.stdout`, `after/c3.stdout` and the report instead of the CAND
  receipts.
- C-6 is a disclosure addition, not proof that any other row is true; the 30 rows were not re-derived here.

## 7. Evidence index (paths relative to the lane root)

- Lesson: `corpus/lessons/round-51.md` (53 lines, added in `f133b47`).
- Contract/freeze: `.ufo/evidence/round-51/contract.json`, `freeze.json`.
- Counters/selftests: `.ufo/evidence/round-51/{c1,c2,c3}/`, `quality/{selftest-c1,selftest-c2,selftest-c3,reach-r51}.stdout`, `control/controls.stdout`.
- C2: `c2/bash-drift-pins.defects.spec`, `c2/sweep/sweep.txt`, `tools/mutate-and-run.sh:634-643`.
- C3: `.ufo/waves/round-51/w2/@P@ExecTool02/c3-counter-full-run.txt`, `.ufo/waves/round-51/w2/@P@ExecTool11/03-exit-code-survey.txt`, `SKILL.md:2138-2171`.
- Sources: `corpus/SOURCES.md:33,106,113,147,148,500-502`, `.ufo/waves/round-51/w1/T51ScribeRowGate.md`, `T51ScribeRowBash.md`, `T51ScribeRowBash/{fetch-receipt.txt,chet-bashref.html}`.
- Falsifiers: `.ufo/waves/round-51/w1/T51LabSandboxLeak.md`, `T51LabSandboxLeak/{red-gone-id,green-gone-neutral}.{sh,out,exit}`, `T51LabWit*.md`, `T51MutC1Counter.md`, `T51MutC2Counter.md`.
- Cold read: `.ufo/evidence/round-51/coldread/{readers.json,refresh.py}`, `coldread/reads/` (empty), `T51CritRekey-sim-{measure.json,receipt.txt}`, `w1/T51ExecRekey.md`.
- Reviewers: `.ufo/waves/round-51/w2/{T51W2CritNoHarm,T51W2CritC1Forgery,T51W2CritC2Registration,T51W2CritC3Truth,T51W2CritQualityMistake,T51W2CritSourceEntry}.md`; `w1/{T51CritExpectedA,T51CritExpectedB,T51CritPrereg,T51CritC3Counter,T51ScribeFrontier,T51ScribeMistakes}.md`.
