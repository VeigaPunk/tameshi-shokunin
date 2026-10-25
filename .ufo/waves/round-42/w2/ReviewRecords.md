# ReviewRecords — round 42, wave 2 (FALSIFY)

Seat `L1Tameshi42.ReviewRecords` (reviewer, leaf). Target: the `## Round 42` block of `SCORECARD.md`
(lines 1995–2020) and the `## 2026-10-25 — round 42` section of `LOG.md` (lines 2168–2215), both read
at integration tip `a21845f523b75adbd3e3f7a62af91294db224ad9`. The work tree equals the tip for every
file read here (`git status --short`: only `?? dispatch-w2.json`, `?? spec-w2.json`, `?? w2/`).
Axes: calibration (do the records agree with their receipts?) and no-harm (no lane mutation).
No LSP: these are markdown/JSON records, so the checks are git object reads and counter runs.

## Findings by severity

### F1 (medium, calibration): a universal clause the counter does not enumerate — "lane-wide unflagged 0"

`SCORECARD.md:2006`, C2 claim cell: "…ten fixtures keep their classes, **lane-wide unflagged 0**, every
declared mutant killed". The counter enumerates only tracked `tools/**/*.py`:

- `.ufo/evidence/round-42/census/measure.py:38` says "live_unflagged_v4=0 over every tracked `tools/*.py` at REV".
- `:325`: `git ls-tree -r --name-only rev -- tools/` filtered to `.py`.

At the tip:

```
git ls-tree -r --name-only a21845f5… tools/ | grep -c '\.py$'                  → 26
git ls-tree -r --name-only a21845f5… | grep -E '\.py$'  (outside tools/)       → 146 other
```

For example, `.ufo/evidence/round-12/measure.py` and `.ufo/evidence/kaika-round-1/coldread/check_uniqueness.py`
are never censused. The wording is the scorecard's own. The frozen contract never says "lane-wide":
`grep -noE '.{60}lane-wide.{80}' contract.json SCORECARD.md LOG.md corpus/lessons/round-42.md` returns
only `SCORECARD.md:2006`. The contract predicate says `live_unflagged_v4=0` without scope. The LOG
target line (`LOG.md:2190`) avoids the clause. Fix: change "lane-wide" to "over tracked `tools/` Python
files (26 at a21845f5)". This is a records wording fix; no predicate change is needed.

### F2 (low, calibration): the cited do-nothing control was measured at an unresolvable revision, and the records do not disclose it

The C1 Evidence cell at `SCORECARD.md:2005` and `LOG.md:2184-2185` cite
`.ufo/evidence/round-42/control/c1-do-nothing.stdout`, whose own line reads
`… rev=5e74a8cbd555b2589c64c5f92eb4baf8679fbb1b … C1_R42_PASS=false`.

```
git cat-file -t 5e74a8cbd555b2589c64c5f92eb4baf8679fbb1b → fatal: git cat-file: could not get object info
```

Wave-1 `ReviewControls.md:54-58` and `:75-76` flagged this gap and reproduced the profile on a scratch
clone at `aa24bd73…`. `grep -n '5e74a8cb\|aa24bd73\|scratch rev' SCORECARD.md LOG.md corpus/lessons/round-42.md`
returns nothing, so neither the records nor the lesson carry the disclosure. m11 does not catch it,
because it audits the records' text and not the receipts they cite (`calibration/measure.py:250-257`).
The scenario is still confirmed (ReviewControls reproduction), so the conclusion is unaffected, but the
provenance is not re-derivable as cited.

### F3 (low, calibration): the "after the append (113 rows)" census claim is true but has no receipt

`LOG.md:2201-2202`: "Census validate exit 0 at round start (109 rows) and after the append (113 rows),
the same warning set, zero E codes." Under `.ufo/evidence/round-42/census-sources/` the only receipts
are `start.exit` and `start.stdout`. Wave-1 `ExecCensusRerun.md` Finding 2 proved the append path on a
112-row mirror with stand-in S155–S157 rows, not on the real 113 rows. My rerun (read-only; writes
stdout only):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
  → exit=0; 9 W04, 1 W01, 1 ok; diff vs census-sources/start.stdout → IDENTICAL_TO_START
scratch clone /tmp/tameshi-r42w2-ReviewRecords-clone @ a21845f5: validate --file corpus/SOURCES.md
  → exit 0, 9 W04 + 1 W01 + ok, no S155–S158 lines; census --file → "file rows 113"
```

The claim holds. It needs a committed `census-sources/after.{stdout,exit}`.

Related nit: the standing row (`SCORECARD.md:2020`) names the command as bare `sources-census.sh …`.
The lane has no such file (`ls sources-census.sh scripts` → no such file); it lives at
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`. The round-41 row (`:1993`) used a
re-derivable path.

## What survived

| Record claim | Location | Receipt / command | Result |
|---|---|---|---|
| C1 before `m10=1 total=1 records=3 C1_R42_PASS=false`, exit 1 | SCORECARD:2005, LOG:2180-2181 | `before/c1-at-base.stdout` + `.exit`=1; my rerun at `--rev c77c2b7e…` prints the identical line | match |
| LOG `sources_rows=109` in the C1 before line | LOG:2180 | same receipt | match |
| C2 before `tool_absent=1 v3_sha_ok=1 v2_sha_ok=1 live_unflagged_v3=3 … PASS=false`, exit 1 | SCORECARD:2006, LOG:2188-2189 | `before/c2-at-base.stdout`, `.exit`=1; rerun at base identical | match |
| Do-nothing C1: records=6, m10=1, exit 1 | LOG:2184-2185 | `control/c1-do-nothing.stdout`, `.exit`=1 | match (provenance: F2) |
| v3-in-slot fails F01, F04 and the three live sites | LOG:2190-2191 | `control/c2-v3-in-slot.stdout`: exactly those 5 FAIL lines, `fixtures_pass=8/10`, exit 1 | match |
| Junk tool passes 1 of 10 | LOG:2191-2192 | `control/c2-junk.stdout` `fixtures_pass=1/10`, exit 1 | match |
| Supersede sha256 `987f82b4…4979` | LOG:2187 | `sha256sum` of the working file and of `git show a21845f5:…/round-41-residual-receipt.json` both `987f82b4ce749787068d5845208382f930422d84126c94a7b2431e8d08334979` | match |
| Wave-1 v4 reached 3 of 10 (P4) | LOG:2193-2194 | `w1/ExecV4Tool.md:5` `fixtures_pass=3/10`; contract `post_freeze_amendments` P4 | match |
| P1–P4 change no predicate/counter | SCORECARD:2001, LOG:2195-2197 | `git diff --stat 322b5cd3 a21845f5 -- calibration/measure.py census/measure.py contract.json` → only `contract.json` changed; P1–P4 all `rule_changed: false` | match |
| Depth 9, calibration 6 | SCORECARD:2008-2010 | `w1/ExecCommandD.md:21` `recorded_cases=9 depth_score=9`, `:40` `calibration_restraint_score: 6` (wave report, not under `.ufo/evidence/round-42/`) | match |
| Neither claim edits the runner or a SHONEN box | SCORECARD:2010-2011 | `git diff --stat c77c2b7e a21845f5 -- tools/mutate-and-run.sh SKILL.md PROVINCE.md .ufo/evidence/round-21/` → empty | match |
| Standing row says 113; SOURCES.md holds 113 | SCORECARD:2020 | `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` → 113 (work tree and `git show a21845f5:`), base → 109; no duplicate ids (`sort \| uniq -d` empty); C1 m6=0 at the tip | match |
| Rows 109 → 113: S155–S158, each pinned to a committed snapshot | LOG:2198-2199 | the S155–S158 rows cite `pit-basic-concepts.html`, `pit-faq.html`, `python-argparse.html`, `pit-DetectionStatus.java`; all are in `git ls-tree a21845f5 …/sources/`; `sha256sum -c sha256.txt` → 5×OK | match |
| Two entries admitted, with README rows | LOG:2199-2201 | both files present at the tip; `corpus/README.md:530-531` | match |
| QUALITY criteria 81 and 82 | LOG:2201 | `corpus/QUALITY.md:1001`, `:1023` | match |
| Collisions S153, S154; refused entry absent | LOG:2203-2207 | `git show a21845f5:.ufo/waves/round-42/assimilation/collisions` → `S153`, `S154`; `survivor-classification.md` is absent at the tip | match |
| considerthese: one of four boxes has a standing command | LOG:2208-2209 | `corpus/lessons/round-42.md:100-107` table, box 3 only | match |
| Nothing inherited (`local=remote=c77c2b7e … tracked=0 untracked=0`) | SCORECARD:1997, LOG:2175 | contract `inherited_state` | match |
| Wave 1: 47 seats, 13/8/7/6/6/6/1 role mix | LOG:2213-2215 | `spec-w1.json` items: 47, `Counter(role)` = scout 13, reviewer 8, executor 7, mutation-tester 6, critic 6, scribe 6, connector 1; `dispatch-w1.json` `counts.spawn=47`; `w1/swarm-registry.json` 47 members with the same mix | match |
| 47 completed, 0 dead | LOG:2214 | 47 `w1/*.md` reports; their names equal the spec names (`n==f True`); none under 200 bytes. No status field exists in the registry or dispatch, so "completed" is inferred from the reports | match ([INFERENCE] on "completed") |

C1 universal clauses map onto enumerated classes. m10's content-blindness and m7's round-42-only
scope are disclosed in the instrument limits at `SCORECARD.md:2014-2018` and in amendment P2. m8 and
m11 checks on the in-scope records, using the counter's own extractors (`path_tokens`, `HEX40_RE`)
plus a widened probe:

- Every backticked path m8 skips is a bare filename used as a cross-reference. In the SCORECARD and
  LOG sections the only skipped ones are `pit-outcome-vocabulary.md`, `survivor-classification.md`
  and `mutation-score-semantics-cjk.md`, each named alongside its full path or refused.
- The only short hex in SCORECARD/LOG, `c77c2b7e`, resolves.

C2 "every declared mutant killed" is stricter in the counter (`census/measure.py:452`:
`declared >= 3 and killed == declared and REQUIRED_CLASSES <= classes`), so it cannot pass vacuously.

## Pre-run counter runs (labelled pre-run; not the deciding run)

```
python3 …/calibration/measure.py --lane <lane> --rev a21845f523b75adbd3e3f7a62af91294db224ad9 --freeze 322b5cd3…
  PRE-RUN → C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=0 m11=0 total=0 records=6 sources_rows=113 … C1_R42_PASS=true   exit=0
python3 …/census/measure.py --lane <lane> --rev a21845f5… --freeze 322b5cd3…
  PRE-RUN → … fixtures_pass=10/10 run_errors=0 live_1682_ok=1 live_1685_ok=1 live_123_ok=1 live_unflagged_v4=0 live_tool_errors_v4=0 mutants_declared=0 … C2_R42_PASS=false   exit=1
python3 …/calibration/measure.py --selftest → C1_R42_SELFTEST: cases=9 failed=0
```

The C1 pre-run already equals the SCORECARD target. The only C2 shortfall is `mutants_declared=0`,
because `mutants.json` is pending the MutantAuthor seat. The "see the after subsection" cells
(`SCORECARD:2005-2006`) point at a subsection that does not exist yet; that is expected before the
L1's deciding run.

## Residual risk / gaps

- I did not re-derive depth 9 / calibration 6. I relied on the ExecCommandD receipt, which lives in a
  wave report rather than under `.ufo/evidence/round-42/`.
- "47 completed" is inferred from report presence; no per-seat exit status is recorded.

No-harm: no lane edits other than this report. The scratch clone `/tmp/tameshi-r42w2-ReviewRecords-clone`
and the temp outputs `/tmp/tameshi-r42w2-ReviewRecords-*.out` were deleted
(`ls -d /tmp/tameshi-r42w2-ReviewRecords-*` → no such file). Tools installed or updated: none.

BROKEN: SCORECARD.md:2006 claims "lane-wide unflagged 0", but the C2 counter enumerates only the 26 tracked `tools/` Python files (146 other tracked .py are never censused); every other record number matches its receipt.
