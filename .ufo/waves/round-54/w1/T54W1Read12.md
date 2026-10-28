# T54W1Read12 — cold read of `### Gate/probe registry`

- Seat: T54W1Read12 (hyaku run 11, round 54, wave 1, leaf member — no subagent dispatch).
- Heading: `### Gate/probe registry`
- Read revision (cand): `59c38109bf119d0e9d4f878644a82babc937bc1e` (C0; the round-54 content commit).
- Base revision: `d33053f7552db4bd290c99a36979760f544c41ad`.
- Section span at C0: lines 1524-1540 (`reader-section.py` prints `start` 1524, `end` 1541; the frozen round-18 `sectionize` strips the trailing blank line before the next heading).
- Section sha256 at C0: `99285e24a71a8d2a0ea3fd6bcafe7e080acb23bfd653e7cbb3b71dfdc5144c77`.
- Findings: **none** (empty list in `T54W1Read12.json`). Every rule in the section names an anchor that resolves at C0, every cited command and path resolves, the table's four rows each carry 8 cells, and no sentence contradicts another in the section. What was opened and checked is below, claim by claim, with the command output that shows it.

## 1. How the section bytes were obtained (never a working-tree read)

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ python3 .ufo/waves/round-54/reader-section.py \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    59c38109bf119d0e9d4f878644a82babc937bc1e \
    "### Gate/probe registry"
{"heading": "### Gate/probe registry", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 1524, "end": 1541, "section_sha256": "99285e24a71a8d2a0ea3fd6bcafe7e080acb23bfd653e7cbb3b71dfdc5144c77"}
```

The sha was reproduced independently from the frozen blob with the round-18 `sectionize` rule (heading line through the line before the next heading, trailing whitespace-only lines stripped, `\n`-joined, no trailing newline, `surrogateescape`):

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 59c38109bf119d0e9d4f878644a82babc937bc1e:SKILL.md   # lines 1524-1541
start 1524 end 1541 sha 99285e24a71a8d2a0ea3fd6bcafe7e080acb23bfd653e7cbb3b71dfdc5144c77
lines 17  first '### Gate/probe registry'  last 'to new material or establish full-page instruction sufficiency.'
```

All reads below are `git show <rev>:<path>` from that same C0 commit (or from the named historical revision), never a working-tree read.

Two structural facts about the re-read set, neither of them a defect of this section:

- The section text at base `d33053f` and at C0 is byte-identical: `reader-section.py` prints `99285e24…` at both revisions and only the span moves (base 1516-1532, C0 1524-1540), because C0 adds the eight-line `## Standing rules` scratch-root bullet near `SKILL.md:32-39`. The heading sits in the C0 lost set positionally.
- Against the floor revision `ef19d8e1` (which prints `c1aabe90…`), exactly one thing changed: the two Write-scope cells, `/tmp/…` → `$TMPDIR …` (the round-53 scratch-root cutover). `diff -u` of the two section extracts shows only those two table cells; no prose, path, command or count was touched. That is the only text in this section not present when the floor recorded its credit.

## 2. Claim-by-claim cold read, with the artifact opened for each

Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku`; clone at `$HYAKU_SCRATCH/tameshi-r54/T54W1Read12/clone`, checked out detached at C0 (`git -C "$C" rev-parse HEAD` → `59c38109bf119d0e9d4f878644a82babc937bc1e`, `--show-toplevel` → the clone). All runs use `TMPDIR=$HYAKU_SCRATCH/tameshi-r54/T54W1Read12/tmp`. The lane was never written.

| # | Section text (quoted fragment) | Artifact opened / command run | What it shows |
|---|---|---|---|
| 1 | ``| Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner |`` | the section bytes (§1); a delimiter count per `|` row | Four table rows (header, separator, two instruments), each exactly 8 cells / 9 pipes, so no cell bleeds into its neighbour and each row carries every column the header names. |
| 2 | ``python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...`` | `python3 tools/repeat-control.py --runs 3 --out $S/out-run -- printf OK` in the clone | exit 0; `REPEAT_RUN 1/2/3 exit=0`, `REPEAT_COMPARE identical=yes runs=3`, `REPEAT_CONTROL: controls_match`; DIR is created fresh and holds `command.txt`, `finding.txt`, `run-{1,2,3}.{stdout,stderr,exit}`. The entry command resolves and writes only the caller DIR. |
| 3 | ``or `--snapshot DIR`` | `--snapshot .ufo/evidence/round-12/ControlGate` and `--snapshot .ufo/evidence/round-12/ControlGate/mismatch` | exit 0 `SNAPSHOT_EXPECTED id=controls_match exit=0 / SNAPSHOT_OBSERVED id=controls_match exit=0`; exit 1 `SNAPSHOT_EXPECTED id=controls_mismatch exit=1 / SNAPSHOT_OBSERVED id=controls_mismatch exit=1`. Both cited snapshot paths exist and recompute to the recorded verdicts; the mode executes nothing (tool docstring: "It executes nothing — no subprocess call is reachable from this mode"). |
| 4 | ``0 clean; 1 failed; 2 and 64 could-not-evaluate`` | `tools/repeat-control.py` at C0: docstring "Finding IDs and exits (stable): controls_match 0 · controls_mismatch 1 · baseline_nonzero 2 · command_unavailable 2 · snapshot_tampered 2 · setup_error 2 · invalid_usage 64" + `--runs 2 --out …` | invalid usage exits 64 with `REPEAT_CONTROL: invalid_usage`; an unusable `TMPDIR=/nonexistent/unusable` exits 2 with `repeat-control: setup: RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/unusable' (could-not-evaluate)` and `REPEAT_CONTROL: setup_error`. The verdict map's 0/1/2/64 reading matches the tool's own table (exit 64 is labelled could-not-evaluate there, and no label "failed" is applied to a command outcome anywhere in the map). |
| 5 | ``python3 tools/repeat-control.py --selftest`` | `--selftest` under a usable `$TMPDIR` | exit 0, `SELFTEST: PASS (29 cases)`, including `SELFTEST_CASE snapshot-committed-stable PASS (expected=controls_match/0 observed=controls_match/0)` and `snapshot-committed-mismatch PASS`. The self-test command in the row runs green at C0. |
| 6 | ``fresh caller-selected DIR; isolated `$TMPDIR` selftest tree (`tameshi-r12-*`); snapshot read-only`` | `tools/repeat-control.py:148-157,606-611` at C0 | `strict_scratch_root()` returns `TMPDIR` when set and usable and otherwise the platform default; `selftest()` calls `tempfile.mkdtemp(prefix="tameshi-r12-repeat-control-selftest.", dir=strict_scratch_root())`. The prefix matches the cell's `tameshi-r12-*` glob, the tree is the isolated self-test scratch, and snapshot mode is read-only (previous row). |
| 7 | ``python3 tools/bash-witness-study.py count`` | `python3 tools/bash-witness-study.py count` in the clone | exit 0; `counts killed_on_witness=8 accidental=0 survived=2 inconclusive=0 total=10 witness_classified=10`, `declared_none B5,B10`, `unresolved none`. The entry command resolves on the committed evidence and produces a complete classified sample, as the verdict map's 0 arm says. |
| 8 | ``0 complete classified sample; 1 unresolved/failed integrity; 2 could-not-evaluate; 64 usage only (argparse)`` | `count` (row 7), `check` (row 9), `--evidence`-free bad subcommand, and `TMPDIR=/nonexistent/unusable … selftest` | `check` exits 1 on failed integrity; an unusable scratch root exits 2 with `WITNESS_STUDY: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/unusable' (could-not-evaluate)`; `bogus-subcommand` exits 64 from argparse (`bash-witness-study.py: error: argument mode: invalid choice: 'bogus-subcommand' (choose from 'declare', 'run', 'rerun', 'count', 'check', 'selftest')`), i.e. usage only. The four arms hold at C0, including C0's own new scratch-root arm, which lands in the 2 could-not-evaluate class the cell already names. |
| 9 | ``The declaration's runner pin `75ed934d…` is stale at round 27 (`check` exits 1 DRIFT; `run`/`rerun` refuse, exit 2; `count` never reads the runner; seat Read25, `.ufo/waves/round-27/w1/Read25.md`).`` | `declaration.json` (`inputs.runner.sha256`), `python3 tools/bash-witness-study.py check`, `… rerun`, `cmd_count`/`cmd_run` bodies, and the cited report | `declaration.json` pins `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`; `check` exits 1 with one line, `WITNESS_CHECK: DRIFT tools/mutate-and-run.sh sha256=977de470… committed=75ed934d…`, `WITNESS_CHECK: FAIL (1 problems; 96 files covered)`; `rerun` exits 2 with `WITNESS_STUDY: CANNOT-EVALUATE (runner-drift …)` before any sweep; `cmd_run` reaches the same refusal through `_prepare` → `ensure_target_and_spec`; `cmd_count` (`:1070-1144`) contains no `RUNNER` read and `count` exited 0 with the drift present; `.ufo/waves/round-27/w1/Read25.md` exists and at round 27 recorded the same DRIFT with the then-current runner sha `fb91ef76…`. All four clauses resolve at C0. |
| 10 | ``Witness declarations are integrity-frozen (declaration, mapping, target, spec, summary; `manifest.json` itself is not pinned`` | `check`'s required list (`:1191-1205`), `manifest_files` (`:840-848`), `manifest.json`, and a manifest self-mutation test in a second C0 clone | `check` requires `DECLARATION_NAME, DECLARED_NAME, TARGET_NAME (pristine.sh), SPEC_NAME (bash-surface-census.spec), SUMMARY_NAME`; the manifest's `files` map has 95 entries and contains declaration.json, declared.tsv, summary.json, pristine.sh, bash-surface-census.spec — and no top-level `manifest.json` (only `rerun-20261020T035435Z/manifest.json`); `manifest_files` skips `rel == MANIFEST_NAME`. Adding a top-level key to `manifest.json` in the clone leaves `check` reporting only the runner DRIFT (`WITNESS_CHECK: FAIL (1 problems …)`), so the manifest's own bytes are indeed not pinned. The parenthetical enumerates exactly the five covered artifacts. |
| 11 | ```.ufo/evidence/round-12/BashWitness/declaration.json`, `declared.tsv`, `manifest.json``` | those three paths at C0, plus `declaration.json`'s `inputs` | All three exist under the round-12 BashWitness evidence directory the row names; `declaration.json` carries the frozen target/spec/runner digests and `declared` (path, sha256, rows, none_rows), `declared.tsv` is the declared-witness mapping (10 data rows, B1-B10), and `manifest.json` records the 95 file digests. The table's path list is resolvable and consistent with what `check` reads. |
| 12 | ``own evidence directory plus isolated `$TMPDIR` selftest tree (`bash-witness-selftest-private.*`, selftest only); sibling object store read-only`` | `tools/bash-witness-study.py:1260`, `:95-105`, `:361-367`, `:624`; `cmd_count`/`cmd_check` bodies | `selftest()` calls `tempfile.mkdtemp(prefix="bash-witness-selftest-private.", dir=strict_scratch_root())`; `EVIDENCE_DEFAULT` is `.ufo/evidence/round-12/BashWitness`; the sweep's workdir sits inside the evidence directory; the sibling `kagi-shokunin` store is only read via `git -C <kagi> show`; `check` and `count` open no write path. Both write sites the cell names match the tool at C0. |
| 13 | ``python3 tools/bash-witness-study.py selftest`` (self-test command) | `selftest` in the clone under a usable `$TMPDIR` | exit 0; last lines `WITNESS_SELFTEST: 51/51 pass` and `VERDICT: PASS`, private fixture root removed on pass. |
| 14 | ``Registry scope is these round-12 instruments`` (the sentence wraps after `assertion is` on the next line) | the two table rows; `tools/mutate-and-run.sh` is the runner both rows' paths touch | The registry has exactly two instruments, both introduced in round 12 (commits `9df9212`, whose subject is "round-12: repeated controls and bounded bash witness attribution"), and neither row asserts a conformance gate over `tools/mutate-and-run.sh` — the bash row is Kind `probe` and its own next sentence limits it to one recorded case. |
| 15 | ```SHONEN.md` box 3 carried a scope-bounded `[~]` at round 12, not `[ ]`;`` | `git show 9df9212:SHONEN.md`, `git show 8742f5d:SHONEN.md`, `git show 546b371:SHONEN.md` (the three round-12 commits) | Each carries the same box 3 line `- [~] Instructions executable by an agent without oral context` with the scope-bounded qualifier "(fleet round-1 cold-read of blob 4eb4cf3 … Appendix A + B sweep recipe only … service/cadence/runbook not exercised …)". At C0 `SHONEN.md` still carries box 3 as `[~]`, and the paragraph above the section now names the transition commit (`[~]` since `c7986cd`), so the correction does not conflict with it. |
| 16 | ``corpus/lessons/round-1-verifier-spotcheck.md` excludes it from the score.`` | `corpus/lessons/round-1-verifier-spotcheck.md` at C0 | The adjudication line reads "the score re-pinned at 6 — the box-3 increment is not credited (cold-read covered Appendix A+B only, probes reconstructed)". A fair paraphrase: the box-3 increment is excluded from the score. |
| 17 | ``Appending this registry does not extend the earlier Appendix A/B cold-read`` (the sentence wraps before `to new material…`) | the preceding section's own scope sentence and `SHONEN.md` box 3 at C0 | The earlier cold-read is the "Appendix A + B sweep recipe only" exercise the box-3 qualifier names; nothing in this section claims a full-page read, and the sentence is a scope disclaimer, not a rule. |
| 18 | ``deepens one recorded case, never a seventh independently measured gate.`` | the page's case/leg accounting at C0 | The page states six recorded cases with a seventh since round 16, and the preceding round-12 section calls the runner "the six-leg runner of round 12". The bash study is Kind `probe`, not a new gate, so "never a seventh" is consistent with the page's own counting; no artifact contradicts it. |

## 3. Non-defects opened, checked and dismissed (not filed)

These are the questions a cold read raises; each was resolved against an artifact, so none is filed as a finding.

1. **`manifest.json` appears in the row's Pinned-values cell while the prose says `` `manifest.json` itself is not pinned ``.** Read as a claim that the manifest's own bytes are digest-covered, the cell would contradict the prose; read as the column's actual content (the committed artifacts that carry the pinned values — the 95-file digest map), it is accurate: the manifest *is* where the per-file pins live, and the prose immediately qualifies that its own bytes are the unpinned root. The page's later canonical row for the same tool (`SKILL.md:2168`) lists the same file in the same column with the same convention (declaration.json with its frozen target/spec/runner digests, declared.tsv, summary.json, manifest.json, mutate-and-run.sh), and `check`'s own required list treats the manifest as a required *record*, not a covered input. Since no rule in the section depends on treating the manifest as digest-covered, this is a wording shorthand, not a stale cell, and I do not file it. (Receipt: the top-level-key test in row 10 shows the prose clause is exactly right.)
2. **`seat ReRead08` is cited twice without a path, while `seat Read25` is cited with one.** The name resolves in the lane (`.ufo/waves/round-27/residual/ReRead08.md`), both claims it supports are verifiable from the artifacts the same sentence names (`declaration.json`, the manifest, `check`), and seat-name citations are the page's standing idiom (`seat Read07` ×3, `seat ReRead07` ×2, and a dozen round-N seats). It does not gate any command, so I record it here rather than file it as an unfixed defect.
3. **The `$TMPDIR` shorthand in both Write-scope cells.** At C0 `$TMPDIR=""` or unset falls through to the platform default, so the tree is only literally under `$TMPDIR` in the set-and-usable arm. C0's own `## Standing rules` bullet states the three-arm contract explicitly, and both tools allocate with `dir=strict_scratch_root()` and the stated prefixes; the cells are accurate for the arm they describe and name the tree, not a guarantee about the unset arm. Not filed.
4. **Row 1's verdict map label "failed" versus the tool's `controls_mismatch` id.** Exit 1 does mean "the N pristine controls disagreed", and the cell is a coarse verdict map, not an id table; the same convention is used by the page's later canonical row ("0 clean; 1 failed (tamper, digest drift, summary/raw mismatch, unresolved sweep)"). A reader is not misled about which exit to expect, and no downstream rule consumes the label. Not filed.
5. **The two Write-scope cells' `/tmp` → `$TMPDIR` change (floor → C0 text).** This is the round-53 cutover, verified against behaviour above (rows 6, 12); it is the reason the section is in the C0 lost set, not a defect.

## 4. Byte-exactness check of every quoted fragment in this file

Run after writing, over the canonical section text (C0 lines 1524-1541, trailing blank stripped). The checker asserted, for each fragment, membership in the section bytes **and** in this file:

```
$ python3 - <<'PY'   # section = git show C0:SKILL.md lines 1524-1541, stripped per sectionize
... each fragment asserted `q in section` and `q in T54W1Read12.md` ...
checked 21 bad 0
```

All 21 section-text fragments quoted in §2/§3 are byte-exact in the C0 section and in this file. Two things the first pass caught and this file now reflects:

- The section wraps both scope sentences, so `Registry scope is these round-12 instruments` and `Appending this registry does not extend the earlier Appendix A/B cold-read` are quoted by their first line, with the wrap noted in the cell; the earlier draft joined the lines and failed the byte check (a quote that is not byte-exact is worse than no quote).
- The Pinned-values cell begins `` `.ufo/evidence/round-12/BashWitness/declaration.json`, `declared.tsv`, `manifest.json` ``; a bare `` `declaration.json` `` prefix does not occur there, which is why the quote in §2 carries the full path.

Four fragments in §2/§3 are deliberately not required to be section bytes because they are quoted from other artifacts, and each was checked against its own source instead: `the six-leg runner of round 12` (the preceding section, `SKILL.md:1508`), `0 clean; 1 failed (tamper, digest drift, summary/raw mismatch, unresolved sweep)` (the later canonical row, `SKILL.md:2168`), `- [~] Instructions executable by an agent without oral context` (`SHONEN.md` at `9df9212`), and `the score re-pinned at 6 — the box-3 increment is not credited (cold-read covered Appendix A+B only, probes reconstructed)` (`corpus/lessons/round-1-verifier-spotcheck.md`).

The JSON deliverable carries `findings: []`, so it reports no quote; its `heading`, `cand` and `section_sha256` are the three values `reader-section.py` printed in §1 (verified by re-reading the file back).

## 5. Hygiene

- No lane file was written. The only writes are this file and `T54W1Read12.json` under `.ufo/waves/round-54/w1/`.
- Fixtures were `git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin` copies under `$HYAKU_SCRATCH/tameshi-r54/T54W1Read12/` (`clone`, `clone2`, `clone3`), each detached at C0 and each git call named `-C "$D"`; the manifest self-mutation test ran only in `clone3`. No mutating git command was run against the lane.
- Scratch tree `/fast/scratch/hyaku/tameshi-r54/T54W1Read12` removed at the end of the run (`rm -rf` on the seat tree); nothing was left under `/tmp`.
- No tool was installed or upgraded (nothing needed).
