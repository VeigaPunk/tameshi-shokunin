# Read34 cold read: "## Eighth recorded case — round 18" (SKILL.md lines 1905–1924)

Verdict: wrong-expectation. One replay clause is false at the pinned revision: the section expects `cases=8 passed=8`, and the same command prints `cases=9 passed=9`. Every other checked claim holds at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. Two minor gaps are listed below: one wrong label in the survivor table, and one probe that does not reproduce from the committed fixture alone.

## Setup

- Clone: /tmp/Read34-7YLu/fleet/tameshi-shokunin, detached at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. SKILL.md sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95 (matches).
- Section span: lines 1905–1924. The next heading is line 1925 (`### Round-18 gate/probe registry — routed-defect closure`). No code fence falls inside the span.
- Class: record. The body reports measured facts with pointers. The "Replay" sentence is one pointer to a recorded replay; I ran it as a named command as well.
- Tools: none installed or upgraded. Existing tools used: strace, bwrap, node v24.21.0, git 2.56.0, python3 3.14.8. The operator rules at /home/vgpnk/.omp/agent/RULES.md were read first.
- The replay (background job bg_6854) finished in 274.45 s, inside the six-minute bound. Nothing was skipped.
- Live lane: read only outside traces (directory listings). Receipts Read34-1 to Read34-13 were written to the traces directory. No live-lane file was edited. No git write and no jj command ran in the live lane.
- Helper scripts (reader.py, coverage.py, probes.py, dupline.py) live only in /tmp/Read34-7YLu. They are not lane files.

## Findings

### 1. wrong-expectation: replay count (SKILL.md:1913–1915)

The section says the replay prints `REGRESSION_CASE js-sources-check: PASS` and `cases=8 passed=8`.

Observed at 2227d83 (receipt Read34-1, exit 0):
- `REGRESSION_CASE js-sources-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)`. Matches.
- `REGRESSION_SWEEP js-sources-check: MUTATE: DONE (target=js-sources-check defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)` and `REGRESSION_TABLE js-sources-check: match=10/10 recorded-killed=5 measured-killed=5 survived=5 inconclusive=0 flips=0`. Matches.
- `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`. Differs: the count is 9, not 8.

Cause: tools/mutate-and-run.sh:1430 sets `local nlegs=9`, and the header at lines 16–17 records the round-26 ninth leg (js-cite-check). The count was 8 at 01d586d (entry ER8-1, corpus/knowledge/mutation-case-kumitate-sources-check.md:230).

Smallest safe correction: name the revision on the count, for example "cases=8 passed=8 at 01d586d (round 18); cases=9 passed=9 at 2227d83". The leg-level claim needs no change.

### 2. minor: "detail text" in the S_DUP_LINE row (SKILL.md:1922)

The row's "does not pin" cell reads "detail text and non-row counters". For S_DUP_LINE the unpinned property is the finding's line number, not detail text. Scratch copy of the pinned blob, line 251: `add('error', 'ID_DUPLICATE', 'corpus/SOURCES.md', index + 1, \`id=${id}\`);`. The spec (sources-check.defects.spec:43–46) changes only `index + 1` to `index + 2`, which is the line argument. The detail `id=${id}` is unchanged. The probe output differs only in location: text `:8` against `:9`, and JSON `"line":8` against `"line":9`, with `"detail":"id=S001"` in both (receipts Read34-11 and Read34-12).

Smallest safe correction: change "detail text" to "finding line (`:N`)".

### 3. minor: the S_DUP_LINE probe does not reproduce from the committed fixture

The retained fixture at .ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/fixture/ holds only corpus/SOURCES.md (542 bytes, sha256 712d5c9e…). The transcript's fixture also had an empty corpus/knowledge/ directory, which git cannot track. From the committed tree, both binaries fail closed with READ_FAILED (ENOENT) and show no difference (receipt Read34-11). With that empty directory created in a scratch copy, the pristine binary reports ID_DUPLICATE at :8 and the mutant reports :9, in text and JSON (receipt Read34-12). So the non-equivalence claim holds, but a reader cannot reproduce it from the committed files alone.

[INFERENCE, not run] A non-.md placeholder such as corpus/knowledge/.gitkeep would keep the directory trackable, because the checker reads only *.md entries (scratch copy lines 344–345).

## Verified as written

Each item below was checked against an opened file or a receipt.

- Pin: kumitate scripts/sources-check.mjs at 0acb7752d19058b953ebbeba253b1e35f6548de5 has sha256 6a293a72…258f, 897 lines, 43,497 bytes, and mode 100755. Sources: external read (Read34-2), the ls-tree and wc checks, and the replay's REGRESSION_PIN line (Read34-1).
- Ledger leg: PIN_SOURCESCHECK and REV_SOURCESCHECK at tools/mutate-and-run.sh:617–618, and TABLE_SOURCESCHECK at line 628, match the section's values.
- Pre-registration: commit 93d22aa has committer time 2026-10-20T16:40:21-03:00 (19:40:21Z). It is an ancestor of 2227d83 (ancestor_exit=0) and added suite.txt, sources-check.defects.spec, predictions.json, and control.txt (Read34-3). The sweep's MUTATE_DATE is 19:41:29Z, after the commit (sweep.txt:8, Read34-4). The five files are unchanged between 93d22aa and 2227d83 (Read34-7).
- Sweep: `MUTATE: DONE (... killed=5 survived=5 ... kill-rate=50%)` (sweep.txt:112) and `PREDICTION_MATCH: 10/10` (sweep.txt:130). Receipt Read34-4.
- Suite: suite.txt is the `env -i` string with private HOME and TMPDIR. Its sha256 6e550d5a… is identical to case 7's .ufo/evidence/round-16/round-gate/suite.txt (Read34-7). My own selftest run prints `SOURCES_SELFTEST: 46/46 pass`, `VERDICT: PASS`, exit 0 (Read34-10).
- Controls: eight runs under control/repeat/. All eight stdout files have sha256 e0880a5a…665e5f and are 6,274 bytes. All exit files are 0 and all stderr files are empty (Read34-5, Read34-9). repeat-hashes.json reports controls_match.
- Wave 2 probes (ER8-2): I rebuilt each mutant from the pre-registered @old/@new pair (exactly one occurrence each) and ran it on the retained fixtures (Read34-11, Read34-12). The mutant sha256 values match the transcripts.
  - S_KIND: `--help` differs only in the `findings:` line, and `--json` is identical. This matches "differs only in `--help` output".
  - S_VERDICT: the final line is `SOURCES_CHECK: DRIFT (KIND_ENUM)` against `SOURCES_CHECK: DRIFT [KIND_ENUM]`.
  - S_ENTRY_COUNT: `entries_with_source=1` against `2`, and JSON `entriesWithSource` 1 against 2.
  - S_FILE_READ: with an EACCES copy of the fixture, `READ_FAILED` against `SOURCES_MISSING`.
  - S_DUP_LINE: see finding 3.
- Table, S_KIND row: the one-sided coverage check is at scratch lines 784–785 (missingKinds is computed over FINDING_KINDS).
- Table, S_VERDICT row: the DRIFT line is at scratch line 483. The S_VERDICT transcript and the spec (spec lines 24–26) agree.
- Table, S_FILE_READ row: the READ_FAILED fixture (sources-check.mjs:790, `knowledgeIsFile: true`) makes corpus/knowledge a plain file (sources-check.mjs:539; receipt Read34-13), so readdirSync fails at line 344 and the catch at line 349 runs. The per-entry catch at line 356 runs in 0 of 43 suite processes, and the catch at 349 runs in 1 (V8 coverage, Read34-10).
- Fix owner (kumitate): the entry's §6 ownership bullet.
- Entry link: corpus/knowledge/mutation-case-kumitate-sources-check.md exists at the pinned revision.

## Entry-level notes (outside the section; not counted in the verdict)

- The entry's §0 suite bullet says case 8's suite is "not the same bytes" as case 7's. Both suite.txt files hash to 6e550d5a…, and ER8-5 (lines 258–259) says they are byte-identical. The section's "form of case 7" wording is true either way.
- The entry's §0 control bullet gives the control hash suffix as "…e5". The real suffix is …5e5f, which ER8-5 (line 259) states.

## Verification gaps

- The other eight legs were checked only through the replay's PASS lines. I did not re-derive their tables.
- The sibling reads for the other eight legs were done by the replay's git show. Their sha256 values come from the tool's own REGRESSION_PIN lines, not from my own hashing.
- S_FILE_READ: I reproduced the EACCES witness only. The ENOENT and ENAMETOOLONG witnesses in its probe suite were not re-run.
- The probes ran unsandboxed on the lane fixtures. The bwrap runs in the transcripts were not repeated.
- Non-trace commands: the clone step, directory listings of the live lane outside traces, and git cat-file, ls-tree, and show-through-sha256sum on kumitate. Each result is either corroborated by a trace receipt or recorded under external_inputs.

## Result

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read34", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
 "sections": [{"start": 1905, "heading": "## Eighth recorded case \u2014 round 18", "class": "record", "verdict": "wrong-expectation",
 "blocking_gaps": [],
 "wrong_expectations": ["Replay clause at SKILL.md:1913-1915 expects `cases=8 passed=8`. At 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 the same command prints `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` (receipt Read34-1). The runner sets `local nlegs=9` at tools/mutate-and-run.sh:1430, and its header lines 16-17 record the round-26 ninth leg js-cite-check. The count was 8 at 01d586d (entry ER8-1, corpus/knowledge/mutation-case-kumitate-sources-check.md:230). The js-sources-check leg itself passes at this revision (REGRESSION_CASE js-sources-check: PASS; killed=5; table match 10/10)."],
 "minor_gaps": ["Survivor table row at SKILL.md:1922 says S_DUP_LINE leaves 'detail text' unpinned. The mutant changes the finding line argument (scratch copy of the pinned blob, line 251: index + 1 becomes index + 2); the detail id=${id} is unchanged. The unpinned property is the finding line (:N), as receipts Read34-11 and Read34-12 show (text :8 vs :9; JSON line 8 vs 9; detail id=S001 in both).",
  "The S_DUP_LINE probe (SKILL.md:1915-1916, via ER8-2) does not reproduce from the committed fixture. The retained survivor-probes/S_DUP_LINE/fixture holds only corpus/SOURCES.md (542 bytes, sha256 712d5c9e...) because the transcript's empty corpus/knowledge/ directory cannot be tracked by git. From the committed tree both binaries fail closed with READ_FAILED (ENOENT) and show no difference (Read34-11). With the empty directory created in a scratch copy, pristine reports ID_DUPLICATE at :8 and the mutant at :9 in text and JSON (Read34-12). [INFERENCE, not run: a non-.md placeholder such as corpus/knowledge/.gitkeep would keep the directory trackable, since the checker reads only *.md entries.]"],
 "commands_executed": [
  "timeout 360 bash tools/mutate-and-run.sh --regression",
  "sh -c 'mkdir -p /tmp/Read34-7YLu/scratch && GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs | tee /tmp/Read34-7YLu/scratch/sources-check.mjs | sha256sum'",
  "sh -c 'git show -s --format=\"commit=%H%ncommitter=%cI%nauthor=%aI%nsubject=%s\" 93d22aa && git merge-base --is-ancestor 93d22aa 2227d8338c02aa9a5fd7d95c1a41b76865ad7647; echo \"ancestor_exit=$?\"; git show --stat --format= 93d22aa'",
  "python3 /tmp/Read34-7YLu/reader.py corpus/knowledge/mutation-case-kumitate-sources-check.md:1-3 corpus/knowledge/mutation-case-kumitate-sources-check.md:47-53 corpus/knowledge/mutation-case-kumitate-sources-check.md:82-103 corpus/knowledge/mutation-case-kumitate-sources-check.md:221-264 .ufo/evidence/round-18/sources-check/suite.txt .ufo/evidence/round-18/sources-check/sweep/sweep.txt .ufo/evidence/round-18/sources-check/predictions.json .ufo/evidence/round-18/sources-check/sources-check.defects.spec",
  "sh -c 'cd .ufo/evidence/round-18/sources-check/control && ls -R . && sha256sum repeat/run-1.stdout repeat/run-2.stdout repeat/run-3.stdout repeat/run-4.stdout repeat/run-5.stdout repeat/run-6.stdout repeat/run-7.stdout repeat/run-8.stdout && for f in repeat/run-1.exit repeat/run-2.exit repeat/run-3.exit repeat/run-4.exit repeat/run-5.exit repeat/run-6.exit repeat/run-7.exit repeat/run-8.exit; do echo \"$f=$(cat $f)\"; done && wc -c repeat/run-1.stderr repeat/run-2.stderr repeat/run-3.stderr repeat/run-4.stderr repeat/run-5.stderr repeat/run-6.stderr repeat/run-7.stderr repeat/run-8.stderr && cat repeat-hashes.json && cat repeat/finding.txt'",
  "python3 /tmp/Read34-7YLu/reader.py .ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/transcript.md .ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/pristine-help.txt .ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/mutant-help.txt .ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/pristine-check.json .ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/mutant-check.json .ufo/evidence/round-18/sources-check/survivor-probes/S_VERDICT/transcript.md .ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/transcript.md .ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/transcript.md .ufo/evidence/round-18/sources-check/survivor-probes/S_FILE_READ/transcript.txt",
  "sh -c 'sha256sum corpus/knowledge/mutation-case-kumitate-sources-check.md tools/mutate-and-run.sh tools/trace-inputs.py .ufo/evidence/round-18/sources-check/suite.txt .ufo/evidence/round-18/sources-check/sources-check.defects.spec .ufo/evidence/round-18/sources-check/predictions.json .ufo/evidence/round-18/sources-check/control.txt .ufo/evidence/round-18/sources-check/sweep/sweep.txt .ufo/evidence/round-18/sources-check/control/repeat-hashes.json .ufo/evidence/round-18/sources-check/control/repeat/finding.txt .ufo/evidence/round-18/sources-check/control/repeat/run-1.stdout .ufo/evidence/round-18/sources-check/control/repeat/run-8.stdout .ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/transcript.md .ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/pristine-help.txt .ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/mutant-help.txt .ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/pristine-check.json .ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/mutant-check.json .ufo/evidence/round-18/sources-check/survivor-probes/S_VERDICT/transcript.md .ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/transcript.md .ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/transcript.md .ufo/evidence/round-18/sources-check/survivor-probes/S_FILE_READ/transcript.txt .ufo/evidence/round-16/round-gate/suite.txt corpus/knowledge/mutation-case-kumitate-round-gate.md && git diff --quiet 93d22aa 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 -- .ufo/evidence/round-18/sources-check/suite.txt .ufo/evidence/round-18/sources-check/predictions.json .ufo/evidence/round-18/sources-check/sources-check.defects.spec .ufo/evidence/round-18/sources-check/control.txt .ufo/evidence/round-18/census-start.txt; echo unchanged_since_93d22aa_exit=$?'",
  "python3 /tmp/Read34-7YLu/reader.py /tmp/Read34-7YLu/scratch/sources-check.mjs:249-252 /tmp/Read34-7YLu/scratch/sources-check.mjs:336-357 /tmp/Read34-7YLu/scratch/sources-check.mjs:778-800",
  "sh -c 'sha256sum .ufo/evidence/round-18/sources-check/control/repeat/run-1.exit .ufo/evidence/round-18/sources-check/control/repeat/run-2.exit .ufo/evidence/round-18/sources-check/control/repeat/run-3.exit .ufo/evidence/round-18/sources-check/control/repeat/run-4.exit .ufo/evidence/round-18/sources-check/control/repeat/run-5.exit .ufo/evidence/round-18/sources-check/control/repeat/run-6.exit .ufo/evidence/round-18/sources-check/control/repeat/run-7.exit .ufo/evidence/round-18/sources-check/control/repeat/run-8.exit .ufo/evidence/round-18/sources-check/control/repeat/run-1.stderr .ufo/evidence/round-18/sources-check/control/repeat/run-2.stderr .ufo/evidence/round-18/sources-check/control/repeat/run-3.stderr .ufo/evidence/round-18/sources-check/control/repeat/run-4.stderr .ufo/evidence/round-18/sources-check/control/repeat/run-5.stderr .ufo/evidence/round-18/sources-check/control/repeat/run-6.stderr .ufo/evidence/round-18/sources-check/control/repeat/run-7.stderr .ufo/evidence/round-18/sources-check/control/repeat/run-8.stderr .ufo/evidence/round-18/sources-check/control/repeat/run-2.stdout .ufo/evidence/round-18/sources-check/control/repeat/run-3.stdout .ufo/evidence/round-18/sources-check/control/repeat/run-4.stdout .ufo/evidence/round-18/sources-check/control/repeat/run-5.stdout .ufo/evidence/round-18/sources-check/control/repeat/run-6.stdout .ufo/evidence/round-18/sources-check/control/repeat/run-7.stdout'",
  "sh -c 'h=/tmp/Read34-7YLu/scratch/sandbox-cov && mkdir -p $h/home $h/tmp $h/cov && cd $h && env -i PATH=\"$PATH\" HOME=$h/home TMPDIR=$h/tmp LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES=$h NODE_V8_COVERAGE=$h/cov node /tmp/Read34-7YLu/scratch/sources-check.mjs --selftest; echo \"selftest_exit=$?\"; python3 /tmp/Read34-7YLu/coverage.py $h/cov'",
  "python3 /tmp/Read34-7YLu/probes.py",
  "python3 /tmp/Read34-7YLu/dupline.py",
  "python3 /tmp/Read34-7YLu/reader.py /tmp/Read34-7YLu/scratch/sources-check.mjs:519-546"],
 "opened": [
  "corpus/knowledge/mutation-case-kumitate-sources-check.md",
  "corpus/knowledge/mutation-case-kumitate-round-gate.md",
  "tools/mutate-and-run.sh",
  "tools/trace-inputs.py",
  ".ufo/evidence/round-16/round-gate/suite.txt",
  ".ufo/evidence/round-18/sources-check/suite.txt",
  ".ufo/evidence/round-18/sources-check/sources-check.defects.spec",
  ".ufo/evidence/round-18/sources-check/predictions.json",
  ".ufo/evidence/round-18/sources-check/control.txt",
  ".ufo/evidence/round-18/sources-check/sweep/sweep.txt",
  ".ufo/evidence/round-18/sources-check/control/repeat-hashes.json",
  ".ufo/evidence/round-18/sources-check/control/repeat/finding.txt",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-1.stdout",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-2.stdout",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-3.stdout",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-4.stdout",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-5.stdout",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-6.stdout",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-7.stdout",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-8.stdout",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-1.exit",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-2.exit",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-3.exit",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-4.exit",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-5.exit",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-6.exit",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-7.exit",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-8.exit",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-1.stderr",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-2.stderr",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-3.stderr",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-4.stderr",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-5.stderr",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-6.stderr",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-7.stderr",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-8.stderr",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/transcript.md",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/pristine-help.txt",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/mutant-help.txt",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/pristine-check.json",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/mutant-check.json",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_VERDICT/transcript.md",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/transcript.md",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/transcript.md",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_FILE_READ/transcript.txt",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/fixture/corpus/SOURCES.md",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/fixture/corpus/SOURCES.md",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/fixture/corpus/knowledge/probe-entry.md",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_FILE_READ/fixture/corpus/SOURCES.md",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_FILE_READ/fixture/corpus/knowledge/alpha.md",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/fixture/corpus/SOURCES.md",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/fixture/corpus/knowledge/alpha.md",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_VERDICT/fixture/corpus/SOURCES.md",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_VERDICT/fixture/corpus/knowledge/probe.md"],
 "inputs": {
  "corpus/knowledge/mutation-case-kumitate-sources-check.md": "d961a0d6645541ebec116d7a12f958426ac4561cd09e9adb6f09c9554afeea38",
  "corpus/knowledge/mutation-case-kumitate-round-gate.md": "1b907c8d2c756134783604b604b3dd0a65b0a5fcb0f5a82e5d24b037b82aeaec",
  "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
  "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
  ".ufo/evidence/round-16/round-gate/suite.txt": "6e550d5a2f6a78fc0654c297b80bb042e8482423d80e2e16bab7374227931f7b",
  ".ufo/evidence/round-18/sources-check/suite.txt": "6e550d5a2f6a78fc0654c297b80bb042e8482423d80e2e16bab7374227931f7b",
  ".ufo/evidence/round-18/sources-check/sources-check.defects.spec": "c8d24cb4b6b1a372543764fc27c9d16f65510a29fed1045bedb2863ce2408c91",
  ".ufo/evidence/round-18/sources-check/predictions.json": "5749a27a92c862278a2c77307496f2b80b3c6619c6125def0ea0066b7252d35f",
  ".ufo/evidence/round-18/sources-check/control.txt": "74061bdf3d1f6bfe5a066c5c454678ae8647d2c5d123f6d4bea182093158d1a0",
  ".ufo/evidence/round-18/sources-check/sweep/sweep.txt": "4ba2a595668439e6ca77bdb26fb462e71e88fe9079a50a77ea9e7d7ff2586097",
  ".ufo/evidence/round-18/sources-check/control/repeat-hashes.json": "79d94d2756a9639cd2999c741af200f16237969a11e8869d4106b79e7bf6bb37",
  ".ufo/evidence/round-18/sources-check/control/repeat/finding.txt": "cf6e03d9c01464c65c111023bec1021241d35e19e12ed2bb2c316cbc9b9772cb",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-1.stdout": "e0880a5a2bed0bba3d1a08583ac9e9d95db8f259d5a563f877b7f27544665e5f",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-2.stdout": "e0880a5a2bed0bba3d1a08583ac9e9d95db8f259d5a563f877b7f27544665e5f",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-3.stdout": "e0880a5a2bed0bba3d1a08583ac9e9d95db8f259d5a563f877b7f27544665e5f",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-4.stdout": "e0880a5a2bed0bba3d1a08583ac9e9d95db8f259d5a563f877b7f27544665e5f",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-5.stdout": "e0880a5a2bed0bba3d1a08583ac9e9d95db8f259d5a563f877b7f27544665e5f",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-6.stdout": "e0880a5a2bed0bba3d1a08583ac9e9d95db8f259d5a563f877b7f27544665e5f",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-7.stdout": "e0880a5a2bed0bba3d1a08583ac9e9d95db8f259d5a563f877b7f27544665e5f",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-8.stdout": "e0880a5a2bed0bba3d1a08583ac9e9d95db8f259d5a563f877b7f27544665e5f",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-1.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-2.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-3.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-4.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-5.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-6.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-7.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-8.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-1.stderr": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-2.stderr": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-3.stderr": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-4.stderr": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-5.stderr": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-6.stderr": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-7.stderr": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  ".ufo/evidence/round-18/sources-check/control/repeat/run-8.stderr": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/transcript.md": "3ff5c723a4a602fbfc0cf79c621a10a9cc7466c850e1a29f657481c7f0b46ed9",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/pristine-help.txt": "f1d41678d8478f08089abc6650be113aae3271151ae72ee632a4250e23949bb1",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/mutant-help.txt": "55b9fc15f833c6c5d4aa0982e2b6f05a8c3ae63e428b6eb97ee4feb5c97e7578",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/pristine-check.json": "4666ccc69425289143cb81156fc382ddaffdc42f98a61ef5596ebd12d1f617a0",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/mutant-check.json": "4666ccc69425289143cb81156fc382ddaffdc42f98a61ef5596ebd12d1f617a0",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_VERDICT/transcript.md": "beb59fded44da2ebae224a249922b9c684154d866d214759db132a3494140dd6",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/transcript.md": "8a14cc4b9b82d5de5892f783c84bc2db75756e86b4ef1eda62da9d5b2553761f",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/transcript.md": "a8562d4b4a94e8f49c9177557bae3da87dc1d840d45c3667a20be6566abc2c1c",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_FILE_READ/transcript.txt": "3b74a6c85a033315774871891f7a54e8ecde9dfcb29fba8cb2caca194226f175",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/fixture/corpus/SOURCES.md": "712d5c9e2bb01e31cca23df22db4edd21e06294fb8807c2dd244588a6b167814",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/fixture/corpus/SOURCES.md": "0ebe004933b24b59a4e39f6748b337b66e4ae9c56f241d6be3ec5c131b17fb9e",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/fixture/corpus/knowledge/probe-entry.md": "dd1e6dd4f60413edfb2156f5daf611724c8c96b342748f3841cc6560d3dbee32",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_FILE_READ/fixture/corpus/SOURCES.md": "981bd0eb7d5ef8e8400eb8fdaadc773ff5798fabca2cffc88e6ef9d5f52f143c",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_FILE_READ/fixture/corpus/knowledge/alpha.md": "4568a06e3dd7904d2d0593dadf5d204c20bcf1116f2822903e19bafdb0fc255e",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/fixture/corpus/SOURCES.md": "7a7c9dca345efe7e90deb6d0a196750c0b5bf97b46321d4786e5caa4422090bd",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/fixture/corpus/knowledge/alpha.md": "4568a06e3dd7904d2d0593dadf5d204c20bcf1116f2822903e19bafdb0fc255e",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_VERDICT/fixture/corpus/SOURCES.md": "45e07f90fd44046168bbff8b66d655a90ddca127b922ee523eed40994f453ca3",
  ".ufo/evidence/round-18/sources-check/survivor-probes/S_VERDICT/fixture/corpus/knowledge/probe.md": "d147c7758af8a9e94b2a74e4b8aa302727927f9a61a917716329d8759cd7745a"},
 "external_inputs": {
  "kumitate-shokunin@0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs": "6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f",
  "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
  "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
  "tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
  "mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh": "d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13",
  "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
  "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs": "e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b",
  "kumitate-shokunin@364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs": "f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9",
  "kumitate-shokunin@1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f"},
 "traces": [
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read34-1.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read34-2.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read34-3.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read34-4.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read34-5.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read34-6.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read34-7.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read34-8.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read34-9.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read34-10.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read34-11.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read34-12.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read34-13.json"]}]}
```

The JSON block above is the cold-read receipt for this section. The note below covers what I checked.

Plain-English note. I classed the section as a record. Its body states measured facts with pointers, and its one replay sentence is a pointer that I ran anyway. I opened every lane file the section cites through the trace collector, at rev 2227d83. The thirteen receipts all show that rev, with no untracked or live-lane reads. I re-ran the replay, the eight-run control determinism check, the pinned-suite selftest with V8 coverage, and the off-suite survivor probes. The kumitate blob hash, line count, and mode check out. So do the pre-registration commit and its ancestry, the sweep's 5/10 kill count and 10/10 prediction match, the suite's identity with case 7's suite, and the S_KIND, S_VERDICT, S_FILE_READ, and S_ENTRY_COUNT claims. Three things do not hold as written. The replay count is 9 at this head, not 8. The S_DUP_LINE row labels the wrong property as "detail text". And the S_DUP_LINE probe needs an empty directory that git cannot store, so it does not reproduce from the committed fixture alone. The verdict is wrong-expectation, limited to the count clause. The sibling kumitate, kagi, tsukuroi, and mado blobs were read through git show, as the brief requires, and they are listed under external_inputs.

COLDREAD Read34: wrong-expectation
