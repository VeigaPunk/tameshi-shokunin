# ScribeLog — round-41 LOG entry: status, audit, and the deltas that remain

Seat: `L1Tameshi41.ScribeLog` (scribe, read-only on the lane). No lane file was edited: `LOG.md`,
`SCORECARD.md`, `corpus/`, `contract.json`, both counters, the Git index and the jj state are
untouched. The only file written is this report.

## Status: the entry already exists, committed — do not append a second one

`LOG.md:2093-2150` already carries

```
## 2026-10-25 — round 41: self-assessment reconciliation and variable-destination write census
```

committed in `b37ce974b6efb8c465626d7346149549a3300a4b` ("round-41: C1 records reconciliation +
C2 write-path-census-v3", 28 files, `LOG.md | 59 +`). Appending the entry I was asked to draft
would produce a second `## 2026-10-25 — round 41` heading; `measure.py`'s `section()` takes the
first match and scans to EOF, so both would be measured as one record and the duplication would
read as drift. **My earlier full append-draft is therefore withdrawn.** What follows instead is an
audit of the committed entry against the receipts, plus the patch list that still matters.

## Audit of the committed entry, claim by claim

| # | Claim in `LOG.md` | Receipt / check | Verdict |
|---|---|---|---|
| 1 | "routed five defects" (`:2095`) | `corpus/lessons/round-40-verifier-spotcheck.md` `## Routed defects` has 5 numbered items | agrees |
| 2 | C1 before line (`:2105`) | `.ufo/evidence/round-41/before/c1-at-base.stdout` — byte-identical, exit 1 in `.exit`; my own base run reproduced it | agrees |
| 3 | C1 target string (`:2107-2108`) | `contract.json` `claims.C1.target` | agrees |
| 4 | C1 **after** | absent — the entry stops at "Target:". A default-mode run exists at `b37ce974…`: `.ufo/evidence/round-41/after/c1-at-b37ce974….stdout` → `m8=1 … total=1 … C1_R41_PASS=false`, exit 1 | **missing; see F1** |
| 5 | C2 before line (`:2113`) | `.ufo/evidence/round-41/before/c2-at-base.stdout`; the entry writes `rev=a3d6c690…` inside a quoted counter line where the receipt has the full 40-hex rev | abbreviated in a verbatim slot |
| 6 | C2 **after** | absent — "Target:" only. A passing run exists at `b37ce974…`: `.ufo/evidence/round-41/after/c2-at-b37ce974….stdout` → `… mutant_symlink_arg_killed=1 … C2_R41_PASS=true`, exit 0 | **missing; see F3** |
| 7 | A1–A4 descriptions (`:2122-2130`) | `contract.json` `amendments`: A1 index 9→8, A2 fixtures re-rooted + argument mutant, A3 record rephrase, A4 work mode `exists` + trailing-slash strip | agrees |
| 8 | "this round's three pre-data amendments" (`:2143`) | the working tree records **five** (A5 added the m9 derived-counts change); HEAD records four | **count wrong; see F4** |
| 9 | S153/S154, snapshot shas (`:2131-2134`) | `corpus/SOURCES.md:123-124` both `mined`, opened 2026-10-25, recheck 180d; `sha256sum` of both snapshots equals the pins | agrees (shas truncated to prefix+suffix, as the entry says) |
| 10 | rows 107 → 109 (`:2134`) | registry scan = 109; `git diff` of `corpus/SOURCES.md` in `b37ce974` = 7 insertions | agrees |
| 11 | collision: registry 109, staged 103, `collisions` holds two ids (`:2135-2137`) | `wc -l` on `assimilation/{reg-ids,staged-ids,collisions}` = 109 / 103 / 2 | agrees |
| 12 | census exit 0 at start (107 rows) (`:2138`) | `.ufo/evidence/round-41/census/start.exit` = 0, `.stdout` 11 lines, 9 × W04 + 1 × W01, zero E codes | agrees |
| 13 | census exit 0 at **round end** (109 rows) (`:2138`) | no committed receipt for the end run — `git ls-tree b37ce974 -- .ufo/evidence/round-41/census` holds only `start.*` | **unsupported by a receipt file** |
| 14 | assimilation none adopted; staged self-source rows refused; round-40 refusal stands (`:2139-2141`) | `corpus/lessons/round-41.md` Gate; no staged id in the registry | agrees |
| 15 | considerthese proposal 1 → QUALITY criterion 80 (`:2142-2144`) | `corpus/QUALITY.md` `### Criterion 80 — name the pins a tool edit breaks, before the edit`, +32 lines in `b37ce974` | agrees |
| 16 | one v1 wave, 40 seats, roles 1/6/8/7/10/5/3 (`:2145-2148`) | `spec-w1.json` role counts; dispatch `counts {spawn:40, resume:0, total:40}`, `waveMinLanes 32 / waveMaxLanes 64` | agrees |
| 17 | Command D `recorded_cases=9 depth_score=9` at the measured commit (`:2150`) | no `ExecCommandD` seat report landed (34 other reports + this one at 03:47:32) and no receipt artefact for it | **unobserved at this seat; see F5** |
| 18 | (implicit) wave settlement | not claimed — correct: 35 files in the report dir at 03:47:32 | correct to leave out |

## Findings

**F1 — the only counter-moving defect is m8, and it is one uncommitted directory.**
`LOG.md:2149` cites `.ufo/waves/round-41/w1/swarm-registry.json`. `git ls-tree b37ce974 --
.ufo/waves/round-41` holds only `assimilation/{collisions,reg-ids,staged-ids}`, `dispatch-w1.json`
and `spec-w1.json` — the `w1/` report directory is untracked. Reproduced on the exact committed
content and proven fixed in the same run:

```
git -C LANE archive b37ce974 | tar -x -C /tmp/tameshi-r41-scribelog-sim2
python3 LANE/.ufo/evidence/round-41/calibration/measure.py --lane /tmp/tameshi-r41-scribelog-sim2 --rev work
  → MISMATCH m8 .ufo/waves/round-41/w1/swarm-registry.json cited but does not resolve at work
    C1_R41: m6=0 m7=0 m8=1 m9=0 total=1 records=3 sources_rows=109 C1_R41_PASS=false  (exit 1)
cp -r LANE/.ufo/waves/round-41/w1 /tmp/tameshi-r41-scribelog-sim2/.ufo/waves/round-41/
python3 LANE/.ufo/evidence/round-41/calibration/measure.py --lane /tmp/tameshi-r41-scribelog-sim2 --rev work
  → C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=3 sources_rows=109 C1_R41_PASS=true  (exit 0)
```

`--rev work` on a `/tmp` extraction is a pre-run check, **not** the deciding run. Round 40
committed 86 wave files, so committing `.ufo/waves/round-41/w1/` (34 seat reports at 03:47:32 plus
`swarm-registry.json`) is the established convention and the whole of the fix.

**F2 — at the committed revision the pin does not name the counter that ran.** `b37ce974` commits
`contract.json` with `claims.C1.counter_sha256 = 8bc9b422…` and the counter blob at `9aaa99ac…`.
`8bc9b422…` is reproducible from the freeze blob plus three hunks (status column, `os.path.exists`,
trailing-slash strip); `9aaa99ac…` adds the fourth hunk (m9's expected words derived from the
round-40 table). The working tree carries amendment **A5** for exactly that hunk — `old_sha256
8bc9b422… → new_sha256 9aaa99ac…` — with the pin field now `9aaa99ac…`, but A5 is uncommitted
(`git status`: `M .ufo/evidence/round-41/contract.json`). As committed, C1's pin and C1's counter
disagree; that is the class the round's own new QUALITY criterion 80 names. Observed at
2026-10-25T03:45:19-03:00 (pin `8bc9b422…`, blob `9aaa99ac…`) and reconciled in the working tree by
03:48:50. Commit the contract with A5 in the same revision as the wave directory.

**F3 — both after receipts exist and neither is cited.** `.ufo/evidence/round-41/after/` is
untracked and holds `c1-at-b37ce974….stdout/.exit` (exit 1, the F1 mismatch) and
`c2-at-b37ce974….stdout/.exit` (exit 0, `C2_R41_PASS=true`). The entry records only "Before" and
"Target", so a reader cannot see that C2 passed and C1 failed on one path class. Cite both at the
final measurement revision and commit the directory.

**F4 — the amendment count is stale.** `LOG.md:2143` says "this round's three pre-data amendments";
the working tree records five (A1–A5), HEAD four. Prefer a count-free phrasing so a later amendment
cannot falsify the sentence.

**F5 — the Command D line has no receipt.** `LOG.md:2150` asserts `recorded_cases=9
depth_score=9` "at the measured commit". No `ExecCommandD` report is in `.ufo/waves/round-41/w1/`
and no evidence file carries the run, so at this seat the number is a record claim, not an observed
one. Either cite a receipt or mark it not-measured this round.

**F6 — verbatim slot abbreviated.** `LOG.md:2113` writes `rev=a3d6c690…` inside the quoted
`C2_R41` line; `.ufo/evidence/round-41/before/c2-at-base.stdout` has the full
`rev=a3d6c690bcbf8914551d4f4e8e1612784c1c2046`. Use the full rev or mark the abbreviation outside
the quote.

What already holds: **m6 = 0** (`SCORECARD.md:1851`, the last `| sources-registry |` line, reads
`109 rows` against 109 registry rows), **m7 = 0** (S001, S153, S154 are the only ids cited in the
three records and all are `mined`; the pre-data A1 fix is what makes this meaningful rather than
vacuous), **m9 = 0** (`corpus/lessons/round-41.md:51-58` states one adopted, six refused, ten
present-but-not-appended against the round-40 table's `(1, 6, 10)`, and A5 now derives those words
from the table so a mismatched sentence cannot silence it).

## Patch list (each item is a small edit to the entry's own section, not a new entry)

| # | `LOG.md` line | Change |
|---|---|---|
| P1 | 2113 | replace `rev=a3d6c690…` with the full rev, or move the ellipsis outside the quoted line |
| P2 | 2105-2105 | add the C1 after: `After: the run at `b37ce974b6efb8c465626d7346149549a3300a4b` returned `m6=0 m7=0 m8=1 m9=0 total=1 C1_R41_PASS=false`, the single mismatch being this entry's citation of `.ufo/waves/round-41/w1/swarm-registry.json` at a commit that does not carry `w1/` — receipt `.ufo/evidence/round-41/after/c1-at-b37ce974b6efb8c465626d7346149549a3300a4b.stdout`; with `w1/` present the same content scores `total=0 C1_R41_PASS=true`.` |
| P3 | 2114-2122 | add the C2 after at the measured revision: `… mutant_symlink_arg_killed=1 rev=<rev> C2_R41_PASS=true`, exit 0 — receipt `.ufo/evidence/round-41/after/c2-at-<rev>.stdout` |
| P4 | 2143 | `this round's three pre-data amendments` → `this round's pre-data amendments` (or `five` once A5 is committed) |
| P5 | 2149 | commit `.ufo/waves/round-41/w1/` (registry + reports) in the measured revision, or drop the `swarm-registry.json` citation |
| P6 | 2150 | Command D: add its receipt, or write "no receipt this round" |
| P7 | 2138 | census round-end: cite a committed receipt for the 109-row run (only `census/start.*` is committed today) |

P2/P3/P5/P7 all assume the closing commit carries `.ufo/waves/round-41/w1/` and
`.ufo/evidence/round-41/after/`; without that, each added path is a new m8.

## Gates I ran

| Gate | Command | Result |
|---|---|---|
| C1 before, reproduced | `python3 .ufo/evidence/round-41/calibration/measure.py --lane LANE --rev a3d6c690bcbf8914551d4f4e8e1612784c1c2046` | `m6=1 m7=0 m8=0 m9=1 total=2 … C1_R41_PASS=false`, exit 1 — equals `claims.C1.before` and the committed `before/c1-at-base.stdout` |
| deciding-run reproduction | `git archive b37ce974 \| tar -x -C /tmp/tameshi-r41-scribelog-sim2` then the counter at `--rev work` | `m8=1 total=1 PASS=false`, exit 1 — reproduces `after/c1-at-b37ce974….stdout` |
| fix proof | add `.ufo/waves/round-41/w1/` to the same extraction, re-run | `m6=0 m7=0 m8=0 m9=0 total=0 PASS=true`, exit 0 |
| committed pins | `sha256sum` on both counters, `fixtures.json`, both snapshots; `git show HEAD:… \| sha256sum` | census counter `83268eff…`, fixtures `20b6254d…`, snapshots `183a4f8c…`/`0044cae6…` all match the contract; C1 counter work-tree = HEAD = `9aaa99ac…` vs pin `8bc9b422…` at HEAD (F2) |
| counter hunks | reconstruct freeze blob + hunks | 1 hunk `5ccb42d8…` (A1), 3 hunks `8bc9b422…` (A4), 4 hunks `9aaa99ac…` (A5) |
| live sites | `python3 tools/write-path-census-v3.py --file $PWD/tools/repeat-control.py` | `:811 open expected=1 scratch=1 unflagged=0`; `:820 os.symlink expected=1 scratch=1 unflagged=0` |
| entry's id surface | counter's own `S_CITE_RE` + `registry()` over lesson, `## Round 41`, `## 2026-10-25 — round 41` | S001, S153, S154 — all `mined` |
| entry's path surface | counter's own `path_tokens` + `git cat-file -e b37ce974:<token>` per record | lesson 4 tokens, `## Round 41` 9 tokens, `## 2026-10-25 — round 41` 12 tokens; exactly one unresolved (`.ufo/waves/round-41/w1/swarm-registry.json`) — the m8 in F1 |

Not run: any counter at the tip beyond the scratch `--rev work` pre-checks above; no
`--control`/`--selftest`; no lane edit.

## Touched surfaces / out of scope

- Written: this report only (`.ufo/waves/round-41/w1/ScribeLog.md`).
- Read: `LOG.md`, `SCORECARD.md`, `corpus/{SOURCES,QUALITY,README}.md`,
  `corpus/lessons/{round-40,round-41,round-40-verifier-spotcheck}.md`,
  `corpus/knowledge/r41-variable-destination-writes.md`, `contract.json` (HEAD and working tree),
  both counters, `census/fixtures.json`, `spec-w1.json`, `dispatch-w1.json`, `swarm-registry.json`,
  the landed seat reports, `tools/repeat-control.py`.
- Out of scope: appending to `LOG.md` (a second heading would double the entry), editing
  `SCORECARD.md`/the lesson/the contract, running the deciding measurement, and resolving F1–F6.
- Tooling: no install or upgrade; `python3`, `git`, `sha256sum` sufficed. No pacman transaction
  attempted (host-wide pause respected).
- Note on the two cross-lane IRC notes about `.ufo/waves/round-35/scratch*`: this seat cites no
  round-35 scratch path, so neither applies.

Report: .ufo/waves/round-41/w1/ScribeLog.md
