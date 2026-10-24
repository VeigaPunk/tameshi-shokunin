# Round 36 W2 — trend-verdict falsification (calibration)

Seat: `W2ReviewTrend` (reviewer, leaf; no subagents). Lane:
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

Revisions read: base/r35 tip `796e08b888849308d0c4d5e932e56833600a139f`; content
`e423c41ba253357ab8c8513f0376dad9d38ab248`; refresh
`b455001e2589b3f4f471d94a3de7e5e549b9f54c`; receipts
`d9c496b19371b779ce0eec6dfee1b049b27a3a2d`; lane tip
`fbb01cf46f8437fd1264c1a3acc053c882fa2164`.

Trend verdicts under attack: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-36/tameshi.md`
§Trend verdicts (lines 109–121, fleet repo, commit `f4ef953`) and
`corpus/lessons/round-36-verifier-spotcheck.md` §Trend verdicts.

**Verdict line: expansion and quality hold on their measured claims (99→100 rows and
S103 mined; v2 predicate repair and dead-pointer correction both verified); discernment
holds on its core (criterion 72 is genuinely lesson-backed) but its absolute clause
("no disagreement is left unlearned") is falsified — the same round-36 LOG entry commits
a never-resolving evidence pointer, violating the criterion 72 that entry introduces.
No measurement is falsified; 1 MEDIUM + 5 LOW defects.**

## What I attacked

| Trend | Sub-claim | Attack | Result |
|---|---|---|---|
| expansion | SOURCES rows 99 → 100 | recount at `796e08b`, `e423c41`, `b455001e`; diff purity; footer | HOLDS (99/100/100; only S103 added) |
| expansion | S103 opened and mined | snapshot byte check; row fields; `used-by` resolution; refresh-receipt citations; lesson Gate quote | HOLDS; quote label/count wrong (LOW) |
| quality | v2 predicate repair | hash freeze at content commit; predicate source; v1↔v2 diff; empty-panel controls; deciding receipt; run count | HOLDS; control rev unreachable (LOW, disclosed) |
| quality | dead-pointer correction | `LOG.md` append-only diff; five named files; repo-wide absence query; `ResidualCriticPredicate.md` §1 | HOLDS |
| discernment | criterion 72 has a lesson behind it | QUALITY diff; lesson `## Mistakes`; falsifier; novelty against criteria 1–71 | HOLDS in substance; self-application fails (MEDIUM) |
| calibration (C1) | monitor refresh 6 → 8, 60/64 → 64/64 | receipts at three revs; ledger/input/section byte re-derivation; kill-rule diff | HOLDS; four ledger entries misuse `skill_sha256` (LOW) |

## Commands run (exact, read-only)

All in `/home/vgpnk/Projects/shokunin/tameshi-shokunin` unless noted; no mutating git/jj,
no `pacman`, no monitor or counter execution.

```sh
git log --oneline -8 ; git rev-parse HEAD                      # fbb01cf46f...
git show 796e08b:corpus/SOURCES.md | grep -c '^| S[0-9][0-9][0-9] |'   # 99
git show e423c41:corpus/SOURCES.md | grep -c '^| S[0-9][0-9][0-9] |'   # 100
git show b455001e:corpus/SOURCES.md | grep -c '^| S[0-9][0-9][0-9] |'  # 100
git diff 796e08b e423c41 -- corpus/SOURCES.md                   # +S103; footer S103→S104
git diff --numstat 5df962b e423c41 -- LOG.md                    # 46 0 (append-only)
git log --all --oneline -- '*ResidualSentinelClosure*'          # empty
ls .ufo/waves/round-35/residual/                                # five reports
find . -name '*ResidualSentinel*' -not -path './.git/*'         # none
sha256sum .ufo/evidence/round-36/c1/c1-measure-v2.py \
  .ufo/evidence/round-35/c1/c1-measure.py tools/tally-audit-v3.py \
  tools/mutate-and-run.sh .ufo/evidence/round-36/src/s103-git-hash-object.html
# 9eb8944c... / d360a159... / 6188db16... / a7d3f2dd... / dd826dae...
git show e423c41:.ufo/evidence/round-36/c1/c1-measure-v2.py | sha256sum   # 9eb8944c...
git show e423c41:.ufo/evidence/round-36/contract.json | sha256sum         # 3aaabddd... == worktree
git diff --name-status e423c41 b455001e                    # ledger M + 7 coldread A files
git diff --stat 796e08b b455001e -- .ufo/evidence/round-21/coldread/ \
  .ufo/evidence/round-18/measure.py                        # ledger only; no measure.py
diff -u .ufo/evidence/round-35/c1/c1-measure.py \
  .ufo/evidence/round-36/c1/c1-measure-v2.py               # 6 hunks / 46 lines, predicate+labels
git cat-file -e 91373d55                                   # fatal: unknown revision
git -C /home/vgpnk/Projects/shokunin log -1 --format='%H %ci %an' \
  -- .ufo/reports/round-36/tameshi.md                      # f4ef953 03:23:42 tameshi-shokunin
git log -1 --format='%H %ci' e423c41                       # 03:14:00
```

Python (stdlib) re-derivations: ledger prefix comparison (`493` old entries identical,
`497` total; 4 appended); four appended entries' `inputs` hashes vs `git show e423c41:<p>`
(all 4/4 match); round-18 `sectionize` at `e423c41` (four section `sha256`
`e37cf21e…`, `13d489ad…`, `d4600d2f…`, `441858d2…`, all match ledger `sha256`);
field-convention census (`493` entries with `skill_sha256 != sha256`; the four new with
`skill_sha256 == sha256`); verdict census (`4` entries with `gap-minor` and
`minor_gaps=0`, exactly the four new); receipt field extraction from the six monitor
JSON files; DESCRIPTION text extraction and word count from the S103 snapshot.

## Per-trend evidence

### Expansion — SOURCES 99 → 100 and S103 mined

Verified true:

- Row count is `99` at `796e08b`, `100` at `e423c41` and `100` at `b455001e`
  (`git show …:corpus/SOURCES.md | grep -c`; the `796e08b` commit touches only
  `corpus/lessons/round-35-verifier-spotcheck.md`, so its SOURCES bytes equal the
  round-35 end state). Labels have pre-existing gaps (S037→S040, S097→S099), so
  `max label 103` with `100` rows is consistent.
- The `796e08b → e423c41` SOURCES diff is one added row (`S103`) plus the footer
  `Next unused id: S103.` → `S104.`; no status/recheck/used-by flip on any existing
  row, matching the lesson's `## Gate` claim.
- S103 row (`corpus/SOURCES.md:112`): `docs`, tier `A`, status `mined`, date
  `2026-10-24`, recheck `365d`, `used-by` =
  `.ufo/evidence/round-36/coldread/refresh-receipts.json, corpus/lessons/round-36.md`;
  both paths exist. The snapshot is present at 29,933 bytes, sha256
  `dd826dae…6100`, title `Git - git-hash-object Documentation`; the quoted fragment
  appears verbatim at the `DESCRIPTION` region. All four `refresh-receipts.json`
  entries carry `cited_source` naming S103 plus `cited_source_row: S103`, and the
  lesson `## Gate` records URL, access date and quote. The mining claim holds.

Defects:

- **L3 — quote label and word count.** The lesson
  (`corpus/lessons/round-36.md:36–38`) quotes `"Computes the object ID value for an
  object with specified type with the contents of the named file"` and calls it
  `§DESCRIPTION first sentence … (19 words)`. The snapshot's first sentence continues
  `… (which can be outside of the work tree), and optionally writes the resulting
  object into the object database.` The quoted fragment is 18 words. The same round's
  spot-check records 18 (`corpus/lessons/round-36-verifier-spotcheck.md:77`), so the
  round's own record disagrees. The SOURCES row (`:112`, anchor cell) repeats
  `§DESCRIPTION, first sentence`.
- **L4 — census receipt overclaim.** LOG `:1935–1936` and lesson `:48–49` say the
  round-start census (`796e08b`, exit 0, 99 rows) and round-end census (`b455001e`,
  exit 0, 100 rows) have “both receipts kept under `.ufo/evidence/round-36/`”. Only
  the end-side receipts exist (`after/census-at-b455001e.{stdout,exit}`,
  `after/sources-rows-at-b455001e.txt`); there is no `796e08b` census receipt anywhere,
  and the census stdout files carry no row count. The `99` figure is receipted only by
  `after/monitor-at-796e08b.stdout` (`sources.rows: 99`) and re-derives exactly from
  git. The count is true; the “both receipts” sentence is not.

### Quality — v2 predicate repair and dead-pointer correction

Verified true:

- **v2 is frozen before the deciding run and is a genuine predicate strengthening.**
  `c1-measure-v2.py` at `e423c41` and at the worktree are both sha256
  `9eb8944c…fa53`; `contract.json` is byte-identical at `e423c41` and tip
  (`3aaabddd…`). Constants `PUB_KILL_SLOTS_TARGET=6`, `PUB_ACCEPT_SLOTS_TARGET=3`,
  `PUB_DISTINCT_TARGET=9` (lines 68–70); the predicate (lines 538–544) requires
  `pub_kill_slots == 6`, `pub_accept_slots == 3`, `pub_kill == 6`, `pub_accept == 3`,
  `pub_distinct == 9`, plus the unchanged holdout/`sealed_ok` clause. The v1↔v2 diff is
  6 hunks / 46 lines and touches only the docstring, constants, print labels and the
  predicate: no scoring-logic change. `ho_kill_total >= 4` / `ho_accept_total >= 2`
  is unchanged from v1 and matches the round-35 contract's `after_target`.
- Controls exist and behave as declared: `control/v1-at-emptypanel.stdout` prints
  `pub_kill=0/0 pub_accept=0/0 pub_slots=0 … C1_R35_PASS=true` exit 0;
  `control/v2-at-emptypanel.stdout` prints `pub_slots=0 … C1_R36V2_PASS=false` exit 1.
  The deciding receipt `after/c1v2-at-b455001e.stdout` prints
  `pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3
  ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=b455001e… C1_R36V2_PASS=true`
  exit 0, 16 COPY lines (9 public + 7 sealed). Exactly one deciding receipt is
  committed. v1 remains sha256 `d360a159…` at both revs and is untouched by any commit
  after the freeze.
- **Dead-pointer correction is real and append-only.** `5df962b → e423c41` changes
  `LOG.md` by 46 insertions / 0 deletions. The correction names the five reports that
  are exactly the contents of `.ufo/waves/round-35/residual/`
  (`ResidualCriticPredicate.md`, `ResidualReviewC2.md`, `ResidualReviewReceipt.md`,
  `ResidualReviewSealed.md`, `ResidualScoutRecords.md`); the absence query
  `git log --all -- '*ResidualSentinelClosure*'` is empty and no worktree file matches.
  The substantive carrier claim resolves: `ResidualCriticPredicate.md:5` is
  `## 1. MAJOR — PASS is weaker than the declared public target`, the exact routed
  defect v2 closes.

Defects:

- **L1 — the four refresh ledger entries corrupt the `skill_sha256` field.** All 493
  pre-existing entries store the whole-`SKILL.md` blob sha256 there (sample verified
  against six `read_rev`s, 6/6 match), with the section sha256 in `sha256`. The four
  `read_rev=e423c41` entries (ledger indices 493–496) store the *section* sha256 in
  both fields (`skill_sha256 == sha256`); the page hash survives only as
  `inputs.SKILL.md = 2381873…`. Credit-neutral: the monitor matches sections by
  `sha256` only and uses `skill_sha256` only as an overlay key
  (`round-18/measure.py:588,593`), so the 6→8 result is unaffected — but the field no
  longer means what 493/493 prior entries mean, and the overlay key changes for these
  entries. Corroborated independently by w1 `ReviewC1Claim.md:183–190` and w2
  `W2CriticC1Honesty.md` §c.
- **L2 — refresh-spec metadata inconsistencies (credit-neutral).** `refresh-specs.json`
  records `previous_class: "record"` for all four sections (lines 22/36/51/64). The
  immediately preceding ledger entry is `instruction` for section 131 (index 490) and
  section 1436 (index 148); only 375/1380 were `record`. The four new entries are also
  the *only* `gap-minor` entries in the ledger with `minor_gaps: 0` (all 493 prior
  `gap-minor` entries have ≥1). The monitor does not validate either field against
  credit (record credits on `gap-minor`), so the score stands; the receipts' prose
  fields are internally inconsistent.
- **L5 (disclosed) — C2 control receipts name an unreachable revision.** Both control
  receipts print `rev=91373d55557fe26c431e9e3dd9e8fa4a00d7b57f`; `git cat-file -e
  91373d55` in the lane fails. The spot-check already routed this
  (`corpus/lessons/round-36-verifier-spotcheck.md`, routed defect 1: “created in a
  scratch clone and is not reachable from the lane repo”). The deciding run is in-lane
  and receipts reproduce; only the empty-panel *control* cannot be re-executed from
  lane bytes alone.

### Discernment — criterion 72 behind a lesson

Verified true:

- `corpus/QUALITY.md:846–857` adds criterion 72 at the content commit (QUALITY diff
  `+12` lines, no earlier lines changed). It requires a LOG evidence pointer to
  re-resolve before commit and corrects never-committed pointers append-only.
- The lesson behind it is real: `corpus/lessons/round-36.md:54–62` records
  `class: reference-drift`, the exact evidence (`LOG.md` round-35 names
  `ResidualSentinelClosure.md`; the all-history query is empty; the residual dir holds
  exactly five reports), `captured-by: none at write time`, and the fix (the
  append-only LOG correction plus criterion 72). The falsifier is the actual r35
  dead pointer, which I re-derived. No criterion 1–71 explicitly requires an evidence
  path to resolve (searched `pointer`/`exist`/`resolv`; criteria 37, 50 and 71 cover
  adjacent but different classes), so “no in-lane criterion caught it at r35 write
  time” stands.
- The correction's named substantive carrier (`ResidualCriticPredicate.md` §1) resolves
  to the predicate defect v2 actually closes.

Defect:

- **M1 — the round-36 LOG entry violates the criterion it introduces.** `LOG.md:1918`
  cites `.ufo/evidence/round-36/control/monitor-at-content-commit.*` as the do-nothing
  control receipt. No file by that name exists; the committed receipts are
  `control/monitor-at-e423c41b.{stdout,stderr,exit}` (the wildcard matches nothing, and
  the literal name breaks the same block's `monitor-at-<rev>` convention). `LOG.md:1919`
  and `SCORECARD.md:1743` defer the measured commit hash to “the round-36 report”; the
  lane has no such file. A fleet report exists at
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-36/tameshi.md` (fleet commit
  `f4ef953`, 2026-10-24 03:23:42), but it was committed ~9m42s *after* the LOG entry
  (`e423c41`, 03:14:00), so it did not exist at LOG write time; the pointer is
  cross-repo and post-dates its citation. Under criterion 72's own rule (“must name a
  file that exists at write time … re-resolved before the entry commits”), the entry
  that adds the criterion fails it. The measurement evidence itself exists and matches
  (`monitor-at-e423c41b.stdout` = score 6, 60/64, rows 100); this is a citation defect,
  not a false measurement.

## Calibration core (C1) and frozen-artifact checks

- Monitor receipts: `after/monitor-at-796e08b.stdout` = score 6, 60/64, four
  uncovered headings, rows 99; `control/monitor-at-e423c41b.stdout` = 6, 60/64, rows
  100; `after/monitor-at-b455001e.stdout` = 8, 64/64, rows 100. All three exit 0.
- Kill rule: `e423c41 → b455001e` changes only `ledger.json` (M) and seven
  round-36 coldread files (A); `796e08b → b455001e` leaves `measure.py` and the
  round-18 implementation untouched. The ledger is a whole-file re-serialization
  (2-space → 1-space indent; 40k changed lines), but the 493-entry prefix is
  semantically identical and the four appended entries' `read_rev`/`inputs` re-derive
  against `e423c41` bytes (4/4). The four section hashes reproduce under the round-18
  sectionizer (`sectionize`, trailing blank lines stripped).
- Frozen hashes all match the contract/pins: v2 `9eb8944c…`, v1 `d360a159…`, tool
  `6188db16…`, runner `a7d3f2dd…`, S103 snapshot `dd826dae…`.

## Peer corroboration and one divergence

- Corroborated by independent w1/w2 seats: the missing round-start census receipt
  (`w1/ScribeGateAudit.md` F3, `w1/ReviewSourcesFrontier.md` F1), the S103 word-count /
  first-sentence defect (`w1/ScribeGateAudit.md` F1–F2, `w2/W2ScoutS103Quote.md`), the
  phantom `monitor-at-content-commit.*` name (`w1/ReviewC1Claim.md`,
  `w1/SimplifierReceiptDupes.md` C2), and the `skill_sha256` field break
  (`w1/ReviewC1Claim.md:183–190`, `w2/W2CriticC1Honesty.md` §c).
- Divergence: `w1/SimplifierReceiptDupes.md` says “No round-36 report exists”. That is
  true of the lane tree but not of the fleet repo: the report is
  `.ufo/reports/round-36/tameshi.md` at fleet `f4ef953`. The valid part of the finding
  is the timing/scope: it did not exist at LOG write time and is not a lane path.

## Residual risk and verification gaps

- I did not execute `measure.py` or `c1-measure-v2.py`; C1 is verified from committed
  receipts plus byte-level re-derivation, and the non-author spot-check re-measured the
  monitor at four revs (6 / 6 / 8 / 8). C2 is source-and-receipt verified; the spot-check
  also did not execute the gate (PROTOCOL §Gate standard). Independent execution is the
  remaining check: `python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev
  REV` at `796e08b`/`e423c41`/`b455001e`, and
  `python3 .ufo/evidence/round-36/c1/c1-measure-v2.py --lane . --rev b455001e --work
  EMPTY_DIR --sealed .ufo/evidence/round-35/c1/sealed`.
- No LSP device is exposed to this seat; caller/definition/diagnostic checks are
  unavailable, so all findings are git/byte/text evidence, not semantic-server proof.
- S103's network provenance was not re-fetched; byte identity, title and content match
  the row/lesson/LOG, which is the check the lane claims.
- The ledger's textual rewrite makes the append non-minimal; semantic prefix identity
  was verified in Python, but a text-only reviewer cannot see the four appends from the
  diff.

## Bounds / tooling

- One lane write: this report. No lane/fleet edits, no `.git` writes, no mutating
  git/jj, no subagents, no `pacman`, no tool installs or updates.
- Scratch: none needed; all reads were in-place read-only.
