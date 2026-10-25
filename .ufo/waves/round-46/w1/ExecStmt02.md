seat: ExecStmt02
item: C1 statement re-observation — ran the frozen argv of `mutation sweep runner` and `six-leg regression ledger` (and, for completeness, all 22 frozen statements) twice each at the freeze rev, captured stdout/stderr/exit/wall, and read each standing claim with the counter's own `last_rows`/`claim_of`

Round 46, wave 1, C1 calibration seat. Read-only on the lane: no lane file, no `SCORECARD.md`, no `statements.json`, no counter was edited; no git/jj mutation in the lane or the fleet repo (only `git clone`/`checkout`/`show` inside `/tmp/tameshi-r46-ExecStmt02/`). All scratch under `/tmp/tameshi-r46-ExecStmt02/`. No tool installed or upgraded.

## Setup (exact commands)

```
W=/tmp/tameshi-r46-ExecStmt02; mkdir -p $W/fleet && for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/clone && git -C $W/clone checkout -q --detach 745a583181648cfc7f9c1b476cd1be7dc68f7433
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin && git -C $W/fleet/tameshi-shokunin checkout -q --detach 745a583181648cfc7f9c1b476cd1be7dc68f7433
```

Verification:
```
git -C $W/clone rev-parse HEAD                  -> 745a583181648cfc7f9c1b476cd1be7dc68f7433
git -C $W/fleet/tameshi-shokunin rev-parse HEAD -> 745a583181648cfc7f9c1b476cd1be7dc68f7433
ls $W/fleet                                     -> 20 sibling symlinks + tameshi-shokunin (21 entries)
python3 -c "hashlib.sha256(open('$W/clone/.ufo/evidence/round-46/calibration/statements.json','rb').read())"
                                                -> a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9
                                                   (== contract statements_sha256 / stmts_pin)
```

## Runner

`/tmp/tameshi-r46-ExecStmt02/run.py` imports the frozen counter as a module
(`importlib` on `.ufo/evidence/round-46/calibration/measure.py`) and reuses its own
`env()`, `pick_line()`, `last_rows()` and `claim_of()` — the picked line is not re-derived by eye.
For every statement it runs the frozen argv twice **sequentially** (the two runs of one statement
never overlap; different statements run concurrently, as the counter itself does with
`max_workers=len(statements)`), with `REV=745a583181648cfc7f9c1b476cd1be7dc68f7433` in the env and
`{work}`→`$W`, `{clone}`→`$W/clone`, `{rev}`→`745a583…` substituted. It writes each run's combined
stdout+stderr to `$W/runs/<id>-run{1,2}.stdout` (42 files) and the whole result to `$W/summary.json`.

Launch command:
```
cd /tmp/tameshi-r46-ExecStmt02 && python3 run.py 2>&1     # 42 subprocess runs, 696.32 s wall total
```

Per-statement cwd is `$W/clone`, except `six-leg regression ledger` which runs in
`$W/fleet/tameshi-shokunin` (its `cwd` is `"mirror"` in `statements.json`; the sibling-lane symlinks
in `$W/fleet/` are what its pinned legs read).

## The 22 frozen argv, each run twice (unique keys; `tally-audit-v3` and `bounded ANSI-C` share one)

```
# cwd=$W/clone
bash .ufo/evidence/kaika-round-1/sources-census-v2.sh
bash tools/mutate-and-run.sh --selftest
python3 tools/repeat-control.py --selftest
python3 tools/pin-disposition.py --selftest
python3 tools/witness-metadata.py --selftest
python3 tools/evidence-disposition.py --selftest
python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72
python3 tools/env-diff.py --selftest
python3 tools/wave-accounting.py --selftest
python3 tools/command-binding.py --selftest
python3 tools/registry-replay.py --selftest
python3 tools/mte-interop.py --selftest
python3 tools/tally-audit-v2.py --selftest
python3 tools/tally-audit-v3.py --selftest
python3 tools/write-path-census-v2.py --selftest
python3 tools/write-path-census-v3.py --selftest
python3 tools/staged-id-guard.py --selftest
bash -c 'git show "$REV:tools/mutate-and-run.sh" | python3 -c '"'"'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'"'"''
python3 .ufo/evidence/round-21/coldread/measure.py --repo $W/clone --rev 745a583181648cfc7f9c1b476cd1be7dc68f7433
python3 .ufo/evidence/round-45/freshness/measure.py --lane $W/clone --rev 745a583181648cfc7f9c1b476cd1be7dc68f7433

# cwd=$W/fleet/tameshi-shokunin
bash tools/mutate-and-run.sh --regression --workdir /tmp/tameshi-r46-ExecStmt02/regression-wd
```

## Per-statement result (both runs, sequentially, same argv)

`claimed` = what `claim_of` parses from the lane's current `SCORECARD.md` (the base text at the freeze);
`—` = `None` (no parseable claim). `·` separates printed line / exit / tool-sha.

| id | kind | claimed | observed run 1 | observed run 2 | same? | exit 1/2 | seconds 1/2 | timeout | verdict |
|---|---|---|---|---|---|---|---|---|---|
| sources-registry | cap | — | `rows=117 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` · exit 0 | same | yes | 0/0 | 0.3/0.3 | 300 | **UNPARSED** |
| mutation sweep runner | cap | — | `MUTATE_SELFTEST: 106/106 pass` · exit 0 · sha `a7d3f2dd7d47` | same | yes | 0/0 | 6.2/5.9 | 1800 | **UNPARSED** |
| six-leg regression ledger | cap | `REGRESSION: PASS (cases=9 passed=9 …)` · 0 | `REGRESSION: PASS (cases=9 passed=9` · exit 0 | same | yes | 0/0 | 155.2/175.6 | 2700 | **MISMATCH** |
| repeated pristine-control gate | cap | — | `SELFTEST: PASS (29 cases)` · exit 0 · sha `296fe566dc59` | same | yes | 0/0 | 1.2/1.0 | 900 | **UNPARSED** |
| six-leg content-disposition probe | cap | — | `SELFTEST: PASS (19/19)` · exit 0 · sha `331529eadafe` | same | yes | 0/0 | 1.6/1.2 | 900 | **UNPARSED** |
| exposed witness provenance correction | cap | — | `SELFTEST: PASS 39/39` · exit 0 · sha `df3390682a04` | same | yes | 0/0 | 2.0/1.7 | 900 | **UNPARSED** |
| effective expectation reconciliation | cap | — | `SELFTEST: PASS (66/66)` · exit 0 · sha `39ee5c5effd9` | same | yes | 0/0 | 4.1/3.8 | 900 | **UNPARSED** |
| retained invocation-context gate | cap | — | `SELFTEST: PASS (49/49)` · exit 0 · sha `7e4519d9a0ea` | same | yes | 0/0 | 2.8/2.3 | 900 | **UNPARSED** |
| hermetic env-differential probe | cap | — | `ENVDIFF_SELFTEST: 9/9 pass` · exit 0 · sha `e8b47ab7cf23` | same | yes | 0/0 | 0.5/0.5 | 900 | **UNPARSED** |
| callback-authoritative wave accounting | cap | — | `ACCOUNTING_SELFTEST: 8/8 pass` · exit 0 · sha `96b3038a77f8` | same | yes | 0/0 | 1.4/1.2 | 900 | **UNPARSED** |
| required-command-receipt-binding | cap | — | `COMMAND_BINDING_SELFTEST: 44/44 pass` · exit 0 · sha `9230c68e53a5` | same | yes | 0/0 | 2.2/1.8 | 900 | **UNPARSED** |
| refusing-registry-replay | cap | — | `REGISTRY_REPLAY_SELFTEST: 10/10 pass` · exit 0 · sha `9fcd2dbba737` | same | yes | 0/0 | 0.6/0.6 | 900 | **UNPARSED** |
| mutation report interop | cap | — | `MTE_SELFTEST: 17/17 pass` · exit 0 · sha `193ea6e32f89` | same | yes | 0/0 | 0.2/0.2 | 900 | **UNPARSED** |
| tally-audit-v2 runner audit | cap | — | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` · exit 0 · sha `7b11ba25aead` | same | yes | 0/0 | 132.1/158.2 | 900 | **UNPARSED** |
| tally-audit-v3 runner audit | cap | — | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` · exit 0 · sha `da8c1ef4b30c` | same | yes | 0/0 | 381.8/314.5 | 1800 | **UNPARSED** |
| bounded ANSI-C code_view | cap | — | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` · exit 0 · sha `da8c1ef4b30c` | same | yes | 0/0 | 381.8/314.5 | 1800 | **UNPARSED** (shares the v3 argv; counter caches the same key) |
| write-path-census-v2 | cap | — | `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0` · exit 0 · sha `402285329588` | same | yes | 0/0 | 0.0/0.0 | 900 | **UNPARSED** |
| write-path census destination resolution | cap | — | `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0` · exit 0 · sha `095924a7a165` | same | yes | 0/0 | 0.1/0.1 | 900 | **UNPARSED** |
| staged-id adoption guard | cap | — | `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` · exit 0 · sha `03a796c5726c` | same | yes | 0/0 | 0.1/0.1 | 900 | **UNPARSED** |
| depth | axis | `9` | `9` | `9` | yes | 0/0 | 0.0/0.0 | 300 | **MATCH** |
| calibration | axis | `8` | `6` | `6` | yes | 0/0 | 31.0/29.2 | 900 | **MISMATCH** |
| freshness | axis | — | `9` | `9` | yes | 0/0 | 1.2/0.9 | 300 | **UNPARSED** |

Tally: **MATCH 1, MISMATCH 2, UNPARSED 19, UNOBSERVABLE 0 → non-match total 21** (the counter's
`total`). Every exit code was 0 in both runs of all 22 statements; stderr was empty everywhere.

`sha256sum <file> | cut -c1-12` at the freeze for every `sha_file` statement (16 unique files), each
equal to the prefix the counter's `git show HEAD:<file>` produces (checked programmatically, 16/16 `OK`):
```
.ufo/evidence/round-15/verify.py   7e4519d9a0ea   tools/staged-id-guard.py       03a796c5726c
tools/command-binding.py           9230c68e53a5   tools/tally-audit-v2.py        7b11ba25aead
tools/env-diff.py                  e8b47ab7cf23   tools/tally-audit-v3.py        da8c1ef4b30c
tools/evidence-disposition.py      39ee5c5effd9   tools/wave-accounting.py       96b3038a77f8
tools/mte-interop.py               193ea6e32f89   tools/witness-metadata.py      df3390682a04
tools/mutate-and-run.sh            a7d3f2dd7d47   tools/write-path-census-v2.py  402285329588
tools/pin-disposition.py           331529eadafe   tools/write-path-census-v3.py  095924a7a165
tools/registry-replay.py           9fcd2dbba737   tools/repeat-control.py        296fe566dc59
```

## Flags required by the item

- **Two runs differ:** no picked line differs, for any statement. Pairwise `cmp` over the 42 captured
  files (21 unique argv pairs; the 22 statements share 21 argv because `bounded ANSI-C code_view` runs the
  same `tally-audit-v3.py` argv as `tally-audit-v3 runner audit`): **19 of the 21 pairs produced
  byte-identical stdout** across the two runs; two differ only on a non-picked line, and in both cases the
  picked line is identical:
  ```
  diff runs/six-leg-regression-ledger-run1.stdout runs/six-leg-regression-ledger-run2.stdout
  2c2
  < REGRESSION_DATE: 2026-10-25T21:19:04Z
  ---
  > REGRESSION_DATE: 2026-10-25T21:21:40Z
  ```
  (both files 7055 bytes; all nine `REGRESSION_PIN` revs/sha256s, all nine `REGRESSION_TABLE`/`REGRESSION_CASE`
  rows and the final `REGRESSION:` line are identical)
  ```
  diff runs/retained-invocation-context-gate-run1.stdout runs/retained-invocation-context-gate-run2.stdout
  19c19
  < selftest-same-path-same-argv: PASS path=/tmp/tameshi-r15-verify-m53kq4rb/lane/tools/candidate.py argv identical; only file bytes differ (…)
  ---
  > selftest-same-path-same-argv: PASS path=/tmp/tameshi-r15-verify-d6q_5ovv/lane/tools/candidate.py argv identical; only file bytes differ (…)
  ```
  (both files 5193 bytes; the only difference is the `mkdtemp` suffix of a selftest scratch path)
  `sha256sum` of the two mutation-sweep-runner runs: `aa3e6b475557d6e551f63f6a7b2338d01c27a9b0b4d66f71cd0a71f5b02bc850` both.
  Neither artifact is byte-reproducible end-to-end (a UTC timestamp, a random temp path); the values the
  counter compares are reproducible.
- **obs regex matches more than one line or none:** none. Every non-special `obs` matched exactly one
  line in both runs (1/1 for all 19 unique regex argv, covering 20 statements). The `census` and `monitor`
  picks are the counter's special paths.
  In the regression output `grep -c REGRESSION` = 51 lines, but only line 50
  (`REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`) matches the
  anchored `^(REGRESSION: \w+ \(cases=\d+ passed=\d+)` regex → 1 match, as measured.
  Note on `retained invocation-context gate`: its frozen `obs` is
  `^selftest-new-full-count: PASS summary (SELFTEST: PASS \(\d+/\d+\))` — the `(` before `SELFTEST` is regex
  grouping, not literal — so the picked line is `selftest-new-full-count: PASS summary SELFTEST: PASS (49/49)`
  (no parenthesis after `summary`), which is what a restated row must quote.
- **Longer than its `timeout`:** none. The three longest: `tally-audit-v3` 381.8/314.5 s vs 1800;
  `six-leg regression ledger` 175.6 s vs 2700; `tally-audit-v2` 158.2 s vs 900. All others < 5 s.
  (Measured under a 22-way concurrent sweep, the same fan-out the counter uses.)
- **Write side effect of one statement (observed, harmless here):** `python3 .ufo/evidence/round-15/verify.py
  --rev 7650fe4…` writes untracked receipts into its cwd — after my runs
  `git -C $W/clone status --porcelain` lists `?? .ufo/evidence/round-15/attempt-4/`,
  `?? .ufo/evidence/round-15/attempt-5/`, `?? .ufo/evidence/round-15/verification-4.json`. The counter runs
  that statement in a throwaway clone, so this cannot dirty the lane, but the statement is not read-only on
  its cwd.

## The two statements this seat names

### `mutation sweep runner` — UNPARSED, and the observation is value-accurate

- argv `bash tools/mutate-and-run.sh --selftest`, cwd `$W/clone`, `sha_file tools/mutate-and-run.sh`,
  timeout 1800. Runs: exit 0/0, 6.2 s / 5.9 s, byte-identical stdout.
- Tail of stdout: `PASS --regression refuses --target (exit 64)` / `MUTATE_SELFTEST: 106/106 pass` / `VERDICT: PASS`.
- Standing row = `SCORECARD.md:1515`, inside the `| Capability | What it can now do | Evidence pointer |
  First-working round |` table at 1513. Evidence cell:
  `` `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0 ``.
- Why `claim_of` → `None`: the statement has a `sha_file`, so the counter demands `CLAIM_SHA`
  (`…, exit N, tool sha256 `12hex``). `re.search(CLAIM_BASE, cell)` → `('MUTATE_SELFTEST: 106/106 pass', '0')`
  (i.e. the printed line and exit are already right); `re.search(CLAIM_SHA, cell)` → `None`.
  The only missing field is `, tool sha256 `a7d3f2dd7d47``.
- Restated row that would parse and match:
  ``| mutation sweep runner | … | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0, tool sha256 `a7d3f2dd7d47` | … |``

### `six-leg regression ledger` — MISMATCH on the printed line, not on the exit code

- argv `bash tools/mutate-and-run.sh --regression --workdir /tmp/tameshi-r46-ExecStmt02/regression-wd`,
  cwd `$W/fleet/tameshi-shokunin`, `sha_file null`, timeout 2700. Runs: exit 0/0, 155.2 s / 175.6 s.
- The full printed line is
  `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`;
  the anchored regex captures `REGRESSION: PASS (cases=9 passed=9`.
- Standing row = `SCORECARD.md:1516`, evidence cell
  `` `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9 …)`, exit 0 ``.
  `claim_of` → `('REGRESSION: PASS (cases=9 passed=9 …)', '0')`; the literal `…` inside the backticks is
  compared as part of the printed line, so the claim can never equal the capture. MISMATCH on the first
  tuple element; exit 0 == 0.
- Nine legs verified in both runs, all identical: `js-kimi-census` 8/10, `bash-surface-census` 8/10,
  `bash-tsukuroi-census` 6/10, `bash-mado-verify` 4/10, `bash-checklist-run` 7/15, `js-claims-check` 7/10,
  `js-round-gate` 5/10, `js-sources-check` 5/10, `js-cite-check` 5/10 — each `match=N/N … flips=0`
  and `REGRESSION_CASE … PASS`.
- The `--workdir` is created by the tool and reported as kept
  (`REGRESSION_WORKDIR: /tmp/tameshi-r46-ExecStmt02/regression-wd (kept)`); run 2 reused the populated
  directories (`regression-wd/{js-kimi-census,…,js-cite-check}`) and still exited 0 with the same picked
  line. Note the legs read live sibling lanes through `$W/fleet/*-shokunin` symlinks; the nine pinned
  `repo=`/`rev=` pairs were identical in both runs, so the tally was stable for the ~3 minutes between them.
- Restated row that would parse and match:
  ``| six-leg regression ledger | … | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9`, exit 0 | … |``

## Standing claims as the counter reads them (lane `SCORECARD.md` is the base text)

```
sha256sum SCORECARD.md (lane)                       -> 4b730384fb3924ec0fda5a76f357683e698c93a737b02f51c9d5c38e691741c1
git show 683eedd:SCORECARD.md | sha256sum           -> 4b730384fb3924ec0fda5a76f357683e698c93a737b02f51c9d5c38e691741c1
git show 745a583:SCORECARD.md | sha256sum           -> 4b730384fb3924ec0fda5a76f357683e698c93a737b02f51c9d5c38e691741c1
python3: r.startswith(b) -> append_only 1   (base 207916 bytes, rev 207916 bytes)
```

Selected standing row per statement (line numbers from the counter's own table walk; `strip_hidden`
preserves line numbering — 2165 raw lines, 2165 stripped):

| id | standing row | parsed claim | why not a value |
|---|---|---|---|
| sources-registry | 1609 | — | arrow order (`→ exit 0, `printed line``) and two unescaped `\|` inside the cell split it into 6 cells; the later rows at 1851/1993/2020/2081/2146/2164 are invisible to the counter (below) |
| mutation sweep runner | 1515 | — | `→ `line`, exit 0` present, `tool sha256` clause absent (sha_file statement) |
| six-leg regression ledger | 1516 | `REGRESSION: PASS (cases=9 passed=9 …)` · 0 | literal `…` inside the backticks |
| repeated pristine-control gate | 1517 | — | no backticks around the printed line (`→ PASS (29 cases), exit 0`) |
| six-leg content-disposition probe | 1518 | — | no `, exit N` (`→ 19/19 PASS0`) |
| exposed witness provenance correction | 1519 | — | no `→ `line`, exit N` (`: metadata selftest39/39 PASS0`) |
| effective expectation reconciliation | 1520 | — | `→ PASS66/66 exit0` (no backticks, no comma) |
| retained invocation-context gate | 1521 | — | `→ exit0, … selftest49/49` (exit before the line) |
| hermetic env-differential probe | 1522 | — | no arrow; `actual9/9 (`ENVDIFF_SELFTEST: 9/9 pass`)` |
| callback-authoritative wave accounting | 1523 | — | `→ frozen counter8/8 (…)` |
| required-command-receipt-binding | 1524 | — | `→ `line`, exit 0` present, `tool sha256` clause absent |
| refusing-registry-replay | 1525 | — | same |
| mutation report interop | 1526 | — | same |
| tally-audit-v2 runner audit | 1657 | — | evidence cell is a prose `deciding receipt …` pointer |
| tally-audit-v3 runner audit | 1698 | — | prose `deciding receipt …` |
| bounded ANSI-C code_view | 1809 | — | prose evidence pointers only |
| write-path-census-v2 | 1889 | — | prose `deciding receipt …` |
| write-path census destination resolution | 1920 | — | prose `deciding receipt …` |
| staged-id adoption guard | 2074 | — | prose `deciding receipt …` |
| depth | 1536 | `9` | — (matches) |
| calibration | 1537 | `8` | observed `6` |
| freshness | none | — | no row with first cell `freshness` in any table whose header cell 2 starts `Score` (the last such table, header at 1534, holds only `depth` and `calibration`) |

Breakdown of the 18 unparsed `cap` rows: **4** carry `→ `line`, exit N` and only lack the
`, tool sha256 `12hex`` clause (all four are `sha_file` statements: mutation sweep runner,
required-command-receipt-binding, refusing-registry-replay, mutation report interop); **14** carry no
`CMD → `LINE`, exit N` form at all.

## Structural hazards in the counter's table reader (found while reading the claims; scratch-only evidence)

1. **A lone `| id | … |` line is read as a table header.** `last_rows` takes `block[0]` as the header and
   `block[2:]` as the body, so a one-line table contributes no row. The newest `sources-registry` rows
   (`SCORECARD.md:1851, 1993, 2020, 2081, 2146, 2164`, each a single-line table separated by blank lines;
   2164 states `→ 117 rows at round 45`) are therefore invisible, and the counter's standing row stays at
   1609.
2. **An append must be preceded by a blank line.** Appending a `| Capability | … |` header directly after
   the file's trailing `| sources-registry | … | 45 |` line merges into that table: the trailing row
   becomes the header, the new `| Capability |` line becomes the separator, and the whole append is skipped.
3. **Unescaped `|` inside a cell shifts `cells[2]`.** Already true at row 1609 (6 cells; `cells[3]` is the
   fragment `S[0-9]{3} \`).

Scratch experiment (on `$W/clone/SCORECARD.md` only; restored to the freeze bytes afterwards, no commit):
```
blank-line-prefixed headed append: MATCH 22 FAIL []
sample claimed: ('MUTATE_SELFTEST: 106/106 pass', '0', 'a7d3f2dd7d47')
# same rows appended with no blank line before the | Capability | header (the axis table kept its blank line)
headed-append parse: MATCH 3 FAIL ['sources-registry', 'mutation sweep runner', … all 19 cap ids]
headerless-append parse: cap rows parsed 1 of 19
```
i.e. with the blank line and a properly headed table, every one of my 22 observed tuples parses to exactly
its observed value (22/22 MATCH); without the blank line the 19 capability rows are absorbed into the
trailing `sources-registry` row's table and none of them parse (only the 3 axis rows, which did have a blank
line, parse).

## Cross-check against the committed freeze receipt

All 22 observed tuples I measured are **identical** to `.ufo/evidence/round-46/before/c1-at-freeze.stdout`
(programmatic comparison of `observed=` strings: `receipt observed mismatches: []`), including the sha
prefixes. That receipt's summary line:
```
C1_R46: self_pin=1 stmts_pin=1 statements=22 mismatches=2 unparsed=19 unobservable=0 append_only=1 total=21 rev=745a583181648cfc7f9c1b476cd1be7dc68f7433 C1_R46_PASS=false
```
My independent tally is the same: 1 MATCH, 2 MISMATCH (`six-leg regression ledger`, `calibration`),
19 UNPARSED (`sources-registry`, 17 capability rows, `freshness`), 0 UNOBSERVABLE, total 21.

## Not run (deliberately, out of seat scope)

- The deciding run of the C1 counter (`measure.py --lane … --rev … --base … --work …`), and
  `measure.py --selftest` / `--emit`: the deciding run is the L1's, per the measurement bounds.
- The C2/C3 counters, the no-harm script, and any build/lint/format gate: not this item; the parent owns
  post-integration gates.
- No mutation of the lane, the fleet repo, sibling lanes, the lane's jj state or Git index; no
  `git add/commit/stash/checkout/switch/reset/pull/push` in the lane.

## Risks / blockers

- **No blocker for C1.** Every one of the 22 frozen commands is observable at the freeze rev, stable
  across two runs, exits 0, and prints exactly one matching line well inside its timeout. The 21 non-matches
  are all statement-side (the standing rows), which is what C1 is meant to fix.
- **Restating is mechanical but must respect the reader's shape:** blank line + `| Capability | … |` header
  + separator for the 19 capability rows, and blank line + `| Axis | Score (0-10) | … |` header + separator
  for a new `freshness` row. A lone appended row (no header, or no blank line) will be invisible — and the
  `sources-registry` row must additionally escape the `|` inside its `grep -cE` code span and put the printed
  line before `exit N`.
- **The regression artifact is not byte-reproducible** (`REGRESSION_DATE`), and its legs read live sibling
  lanes through the `fleet/` symlinks. The picked line was stable in my two runs, but a sibling lane advancing
  mid-run would move the pinned `rev=` values; the counter compares only the picked line and the exit code
  (this statement has `sha_file: null`), so this does not affect C1 as long as the tally stays
  `cases=9 passed=9` and the exit stays 0.
- Independent overlap with `ExecStmt01.md` (sources-registry, depth, calibration) agrees: `rows=117`, `9`, `6`.

## Tooling

None installed or upgraded; no pacman transaction. Only the host's `python3`, `git`, `bash`, `sha256sum`
were used.
