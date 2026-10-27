# T52W1Corr06 — correction record for round-51 cold-read re-key entry `### Using the ledger`

Round 52 wave 1, lane `tameshi-shokunin`, criterion **C2 m4** (calibration). Two lane writes, both in this
directory: the deliverable `T52W1Corr06.json` and this report. Nothing else was created or edited. No tool
installed (`bash`, `git show`, `python3` already present), so no tool/version/channel row is owed. No
scratch dir was needed: every check read committed bytes through `git show`, and no clone or fixture was
created (`/tmp` and scratch untouched). No counter was run as a verdict — only the frozen
`check_findings` helper was imported and exercised on the deliverable.

## Target

- Reader file: `.ufo/evidence/round-51/coldread/reads/T51W2Read06.md` (read in full: 269 lines, 8 `##` sections).
- Section text: `git -C LANE show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md` lines 933-964
  (`### Using the ledger` … trailing blank before `### Reading a receipt — the discipline` at :965).
- Ledger entry: `.ufo/evidence/round-21/coldread/ledger.json` entries, `heading == "### Using the ledger"`,
  `read_rev == 02ec217c…`, seat `T51W2Read06` — the record a round-51 refresh wrote as
  `wrong_expectations: 0`, `verdict: "verified-record"`, `class: "record"`.

Command that shows the ledger row: `python3 -c` over the entries printing heading/read_rev/seats/wrong_expectations
(the last `### Using the ledger` entry: `read_rev 02ec217c…`, `seats ["T51W2Read06", "L1 TameshiR51a3 integration (attempt 3)"]`,
`wrong_expectations 0`, `inputs {"tools/mutate-and-run.sh": "977de47034cb…"}`).

## Verification that the reader's recorded failures hold at `read_rev`

`git show 02ec217c…:tools/mutate-and-run.sh` is 2160 lines and its sha256 is the one the ledger entry pins
(`977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda`); the section is byte-identical to the
reader's CAND (`57ac17ec1a08473f278cff466eb799253adddd8cca8541fdd3cbaa330dc44746`). I re-checked the bytes each
finding rests on, without re-running the reader's falsifiers:

```
$ git -C LANE show 02ec217c:tools/mutate-and-run.sh | sed -n '1432p'
    root=$(mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX") || die_setup 'mktemp -d failed'
$ … | sed -n '1540p'
  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\n' \
$ … | grep -n "cases=10 passed=10" | head -1
2087:  tally_line 0 'REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)' …
$ … | sed -n '1504p'
  regression_case_git bash-drift-pins \
$ … | sed -n '1302p'
    printf 'REGRESSION_PIN %s: source=git repo=%s rev=%s path=%s mode=%s sha256=%s\n' \
$ … | sed -n '126p;607p;629p;657p'
# move a replay. The materialized copy's sha256 must equal the recorded pin;
# D2,E1,F1, survived A1,B1,B3,C1,D1,E2,F2,G1, 7/15 = 47 % at :130-131),
REV_SOURCESCHECK=0acb7752d19058b953ebbeba253b1e35f6548de5
table_count() { # <table> <verdict> -> how many entries carry that verdict
$ … | sed -n '1285p;1295p;1312,1313p'
    if ! blob_mode=$(git_clean -C "$repo" ls-tree "$rev" -- "$path" | awk '{print $1}'); then
    if [[ "$blob_mode" == 100755 ]]; then
    tsha=$(sha_of "$target")
    if [[ "$tsha" != "$pin" ]]; then
```

These match the reader's own located lines: scratch template honours `TMPDIR` (:1432), receipts print
`cases=10` (:1540, asserted :2087), ten dispatches (:1459-1508), `REGRESSION_PIN` printf (:1302-1303), the
three bullet-1 ranges and `:1159-1160` landing elsewhere, `:603-629` holding no `TABLE_*`, `:657` holding
`table_count()` rather than a spec, and the mode being read and mirrored (`:1285-1300`) with only the sha
compared (`:1312-1317`).

## Findings recorded by the reader that do not hold at `read_rev` — 14

One finding per reader-recorded defect: the nine `absent` rows of §2 (row 9 `:83-108` is the reader's
**holds** verdict and is excluded), plus T1 (false), T2, T3 (stale count), T5 and T6 (unsupported premise).
T4 dates four of the pointer failures (`pre-existing since round 26`); it records no separate failing
statement, so the failures it dates are counted once, in their pointer rows. Section line numbers below are
`SKILL.md:933-964` at `read_rev`; reader line numbers are `T51W2Read06.md:<n>`.

| # | class | skill_statement (SKILL.md:933-964) | reader quote (T51W2Read06.md) | command that shows it |
|---|---|---|---|---|
| 1 | stale-pointer | `` Exits0/1/2: PASS/FAIL/SETUP (`tools/mutate-and-run.sh:126-136,1273-1294,1364-1384`) `` | `` `tools/mutate-and-run.sh:126-136` \| scratch allocation/removal + exits (bullet 1) `` (:65) | `git -C LANE show 02ec217c:tools/mutate-and-run.sh \| sed -n '126-136p'` → materialization/stated-expectation header comment (`:126` "# move a replay. The materialized copy's sha256 must equal the recorded pin;"); exit map is at `:139-143`. |
| 2 | stale-pointer | `` Exits0/1/2: PASS/FAIL/SETUP (`tools/mutate-and-run.sh:126-136,1273-1294,1364-1384`) `` | `` `:1273-1294` (same bullet) \| (same) \| git-show SETUP refusals `` (:66) | `… \| sed -n '1273,1294p'` → git-show SETUP refusal `:1276-1280` + blob-mode read/mirror `:1285-1300`; scratch allocation is `:1432`, prereqs `:1423-1427`. |
| 3 | stale-pointer | `` Exits0/1/2: PASS/FAIL/SETUP (`tools/mutate-and-run.sh:126-136,1273-1294,1364-1384`) `` | `` `:1364-1384` (same bullet) \| (same) \| comparison-loop tail + expectation computation `` (:67) | `… \| sed -n '1364,1384p'` → comparison-loop tail (`done <"$rtsv"` `:1364`, table-pair ABSENT loop `:1365-1372`) + expectation computation `:1384-1389`; outcome blocks + `rm -rf "$root"` are `:1519-1548`. |
| 4 | stale-pointer | `` `git show <rev>:<path>` materializes the pinned blob into the case workdir and validates mode/SHA (`tools/mutate-and-run.sh:1104-1175`) `` | `` `tools/mutate-and-run.sh:1104-1175` \| `git show` materializes pinned blob, validates mode/SHA (bullet 2) `` (:68) | `… \| sed -n '1104,1160p'` → `:1104-1154` js-cite-check spec tail, `:1155` `cat >"$d/bash-drift-pins.spec"`, `:1156-1160` leg-10 spec header; `git show` is `:1276`. |
| 5 | stale-pointer | `` `REGRESSION_PIN` names repo/rev/path/pin (:1159-1160) `` | `` `:1159-1160` \| `REGRESSION_PIN` names repo/rev/path/pin (bullet 2) `` (:69) | `… \| sed -n '1159,1160p'` → "# Predictions were fixed before any mutant run. Composition: 5 kill-aimed / 5 hole-aimed." / "# Matrix axes: mode compare, …"; the printf is `:1302-1303` (file variant `:1305`). |
| 6 | stale-pointer | `` A missing repo/rev/blob or pin mismatch refuses before that leg's suite; later legs still run and their statuses aggregate (:1384-1450 since round 26) `` | `` `:1384-1450 since round 26` \| refusal before that leg's suite; later legs still run; statuses aggregate (bullet 2) `` (:70) | `… \| sed -n '1384,1450p'` → verdict prints `:1384-1402`, `regression_case_git` `:1404-1415`, `run_regression` entry `:1417-1450`; refusals live `:1252-1317`, suite invoked `:1320`, dispatches `:1459-1508`, aggregation `:1510-1548`. |
| 7 | stale-pointer | `` Current anchors (round 26): pins/revisions/tables `tools/mutate-and-run.sh:603-629` `` | `` `tools/mutate-and-run.sh:603-629` \| anchor "pins/revisions/tables" (bullet 4) `` (:71) | `… \| sed -n '603,629p'` → knowledge-note comment tail + `PIN_JS..REV_SOURCESCHECK`; `TABLE_*` are `:634-643`. |
| 8 | stale-pointer | `` first-four specs :657-839 `` | `` `:657-839` \| anchor "first-four specs" (bullet 4) `` (:72) | `… \| sed -n '657,839p'` → `table_count()` `:657`, `regression_specs` head `:669-671`, first three spec writes `:673/:714/:759`; the fourth is `:804` (four specs span `:673-852`). |
| 9 | stale-pointer | `` nine dispatches :1384-1428 `` | `` `:1384-1428` \| anchor "nine dispatches" (bullet 4) `` (:74) | `… \| sed -n '1384,1428p'` → same region as #6; the ten dispatches are `:1459-1508` (`regression_case_git bash-drift-pins \` `:1504`). |
| 10 | false | `` allocates a fresh default scratch `/tmp/tameshi-r4-2-regression.XXXXXX` after prerequisite checks `` | `` Bullet 1's literal scratch path `/tmp/tameshi-r4-2-regression.XXXXXX`. `` (:78) | `… \| sed -n '1432p'` → `root=$(mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX") \|\| die_setup 'mktemp -d failed'`; header `:149-151` "(r51 honours" TMPDIR; run-mode default `:491`, selftest `:1555`. |
| 11 | stale-count | `` (N=4 at r7-1, 7 since round 16, 8 since round 18, 9 since round 26) `` | `` round 26)" is true through round 26, but at CAND receipts print `cases=10` `` (:83) | `… \| sed -n '1540,1541p'` → `printf 'REGRESSION: PASS (cases=%s passed=%s; …`; selftest asserts `tally_line 0 'REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)' …`. |
| 12 | stale-count | `` nine dispatches `` | `` Bullet 4's "nine dispatches": ten at CAND (:1504-1508). `` (:86) | `… \| sed -n '1459,1508p'` → ten `regression_case_git` dispatches, the tenth `bash-drift-pins` at `:1504`. |
| 13 | unsupported | `` workdir and validates mode/SHA `` | `` mirrored (:1285-1300), never compared against a recorded mode. `` (:91) | `… \| sed -n '1281,1317p'` → mode read from `git ls-tree` `:1285` and mirrored `:1295-1300`, printed at `:1302`; the sha is compared `:1312-1317`; no recorded mode is compared. |
| 14 | unsupported | `` enumerated, executed and skipped counts distinguished `` | `` "enumerated, executed and skipped counts distinguished": the runner has no skip `` (:92) | `… \| grep -n -i skip` → hits only embedded spec text; outcome taxonomy KILLED/SURVIVED/INCONCLUSIVE; the enumerated/executed convention is in `corpus/knowledge/mutation-case-kimi-census.md:32`, uncited by this bullet. |

Section lines: bullet 1 `SKILL.md:935-940`, bullet 2 `:941-948`, bullet 3 `:949-953`, bullet 4 `:954-963`.
Reader records by label: rows 1-10 = reader `:63-74`; T1 `:78-81`, T2 `:82-85`, T3 `:86`, T4 `:87-89`,
T5 `:90-91`, T6 `:92-96`.

## Self-check (frozen counter's rule)

The frozen C2 counter's own helper, imported unchanged from `.ufo/evidence/round-52/c2/measure.py:82`
(`check_findings`: 20-char minimum after `squash`, membership in the whitespace-collapsed reader file;
`FLOORS` has no key for `T51W2Read06`, so floors = `()`):

```
$ python3 - <<'PY'
import importlib.util, json
spec = importlib.util.spec_from_file_location('m52', '.ufo/evidence/round-52/c2/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rec = json.load(open('.ufo/waves/round-52/w1/T52W1Corr06.json'))
reader = open('.ufo/evidence/round-51/coldread/reads/T51W2Read06.md', encoding='utf-8').read()
print('check_findings ->', m.check_findings(rec['findings'], reader, ()))
print('count ->', rec['wrong_expectations'] == len(rec['findings']), rec['wrong_expectations'], len(rec['findings']))
PY
check_findings -> None
count -> True 14 14
```

`None` is the helper's success return (`.ufo/evidence/round-52/c2/measure.py:95`). Per-quote single-line
witnesses (each quote occurs on exactly one line of the reader file):

```
line [65] len 81 | stale-pointer | `tools/mutate-and-run.sh:126-136` | scratch allocation/removal + exits (bullet 1)
line [66] len 61 | stale-pointer | `:1273-1294` (same bullet) | (same) | git-show SETUP refusals
line [67] len 84 | stale-pointer | `:1364-1384` (same bullet) | (same) | comparison-loop tail + expectation computation
line [68] len 104 | stale-pointer | `tools/mutate-and-run.sh:1104-1175` | `git show` materializes pinned blob, validates mode/SHA (bullet 2)
line [69] len 66 | stale-pointer | `:1159-1160` | `REGRESSION_PIN` names repo/rev/path/pin (bullet 2)
line [70] len 114 | stale-pointer | `:1384-1450 since round 26` | refusal before that leg's suite; later legs still run; statuses aggregate (bullet 2)
line [71] len 77 | stale-pointer | `tools/mutate-and-run.sh:603-629` | anchor "pins/revisions/tables" (bullet 4)
line [72] len 49 | stale-pointer | `:657-839` | anchor "first-four specs" (bullet 4)
line [74] len 50 | stale-pointer | `:1384-1428` | anchor "nine dispatches" (bullet 4)
line [78] len 70 | false | Bullet 1's literal scratch path `/tmp/tameshi-r4-2-regression.XXXXXX`.
line [83] len 74 | stale-count | round 26)" is true through round 26, but at CAND receipts print `cases=10`
line [86] len 55 | stale-count | Bullet 4's "nine dispatches": ten at CAND (:1504-1508).
line [91] len 62 | unsupported | mirrored (:1285-1300), never compared against a recorded mode.
line [92] len 79 | unsupported | "enumerated, executed and skipped counts distinguished": the runner has no skip
```

All quotes are 49-114 characters, inside a single reader line, copied byte-exact (no ellipsis, no
paraphrase). The block above is the live output of that check over the delivered JSON (line lists, squashed
lengths, classes and quotes), reprinted verbatim. Every `skill_statement` is a verbatim substring of the whitespace-collapsed `SKILL.md:933-964`
at `read_rev` (checked by the same script run before the write).

## Gates and surfaces

- Deliverable written: `.ufo/waves/round-52/w1/T52W1Corr06.json` — keys exactly `heading`, `read_rev`,
  `reader`, `reader_file`, `wrong_expectations`, `findings`; `wrong_expectations` 14 == `len(findings)`.
  This is the record the L1 appends to the round-21 ledger's top-level `corrections` list (m4 reads
  `corrections[].heading/read_rev/reader/reader_file/findings/wrong_expectations`, measure.py:147-162).
- Touched surfaces: this report and the deliverable only. Lane checkout, `SKILL.md`, `.ufo/evidence/round-21/`
  and `.ufo/evidence/round-52/c2/measure.py` were read, never written. Every byte I quote was read through
  `git show <fixed rev>:<path>`, so the concurrent uncommitted edits in the working tree cannot have shifted
  a quote. `git -C LANE status --porcelain -- SKILL.md tools .ufo/evidence corpus` at the end of this seat:
  `M SKILL.md`, `M corpus/knowledge/fleet-kill-rate-ledger.md`, `M tools/registry.json`,
  `M tools/round21-measure.py`, `?? .ufo/evidence/round-52/integrate/` — sibling seats' in-flight C1/m5 work,
  not mine (my writes are only `?? .ufo/waves/round-52/w1/`).
- Out of scope by seat spec: editing `SKILL.md` or the ledger (the L1/wave-2 owners do that), the other 19
  correction records, `m1/m2/m3/m5/m6`, re-keying the cold-read section, and any claim verdict — I did not
  score C2 or run any counter except the imported `check_findings` helper on my own artifact.

## Findings (beyond the record)

1. The ledger entry this record corrects is still in place with `wrong_expectations: 0`,
   `verdict: "verified-record"`, `minor_gaps: 0` (`.ufo/evidence/round-21/coldread/ledger.json`, last
   `### Using the ledger` entry, `read_rev 02ec217c…`). Its `inputs` sha for `tools/mutate-and-run.sh`
   (`977de470…`) is the revision at which the reader found 14 failing statements — so the record contradicts
   the reader file it names in the same entry's provenance. My record supplies the count the ledger lacks;
   the entry itself is the L1's to supersede.
2. Round 51's routed defect 3 (`corpus/lessons/round-51-verifier-spotcheck.md:128-129`, line 128 =
   "Cold-read re-key overstates", 129 = "writes `wrong_expectations: 0` for every re-keyed section") is
   confirmed for this one section at the semantic level and fixed here by construction; whether the other
   19 records are non-zero is not mine to judge (`C2.cannot_see`).
3. Four of the 14 are pre-existing, not r51-caused (bullet 1's three ranges and `:1159-1160`): the reader
   dates them stale since the round-26 SKILL edit `40a12bf` (reader `:87-89`) and exact at round 26
   `a08e85c` (reader §6, `:126-131`). They are counted because they fail at `read_rev`, per the item's rule
   ("even when the claim holds elsewhere").
4. The reader's row 9 (`:83-108`, verdict **holds**, tail truncated) is not counted; its note that provenance
   notes now run to `:121` is disclosed and accurate, so it is not a finding.

## Summary

- Recorded 14 reader-evidenced failures for `### Using the ledger` at `02ec217c…`: 9 stale-pointer, 2 stale-count, 1 false, 2 unsupported; `wrong_expectations: 0` was the refresh artifact.
- Every quote is byte-exact from one reader line (49-114 chars); the frozen `check_findings` returns `None`, count 14 == 14.
- Reader-verified bytes confirmed at `read_rev`: TMPDIR template `:1432`, receipts `cases=10` `:1540/:2087`, ten dispatches `:1459-1508`, `REGRESSION_PIN` `:1302`, no `TABLE_*` in `:603-629`.
- Reader row 9 (`:83-108`) is a holds verdict and T4 is a dating note; neither is counted, so no hold or historical note was upgraded.
- Deliverable: `.ufo/waves/round-52/w1/T52W1Corr06.json`; no lane, fleet, ledger or counter file written; no tool installed; no scratch created.
