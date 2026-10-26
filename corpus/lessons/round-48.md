# Round 48 lesson

L1 TameshiR48, hyaku run 8, attempt 1. Two claims on distinct axes, pre-registered before any seat (`.ufo/evidence/round-48/contract.json`,
commits `e73389c0`, `f1cfaad3`; amendments 1-3 pre-data, 4-10 after wave-1 probes of the base tree and before any restated row, control
or deciding run; counter freeze `755298415f8c4eef3bed0c0d7625e2aacb03d6c2`, `.ufo/evidence/round-48/freeze-2.json`): C1 calibration (the
22 standing statements restated from three observation rounds with a stable/nondeterministic value class) and C2 freshness (held rows
S026, S048, S093, S108 re-anchored by superseding rows S265-S268, sourced). Frontier step: rows S265-S268, mined mistakes below, sourced
claim C2. Assimilation: none (`.ufo/waves/round-48/w1/T48ScoutPackage.md`: every staged row touching the four C2 documents is already
held or adopted). considerthese: idea 5 mined (section below).

## Gate

Candidates: the four held rows the round-45 freshness ledger carried with open items (S026, S093, S108: no per-snapshot fetch receipt or
anchor digest; S048, S093: quotes disputed by non-author round-45 judges, `.ufo/evidence/round-45/freshness/reviews.json`), plus the
`merge/tameshi` staged rows and entries that touch the same documents. Admitted: four superseding rows (one per target), each cited by the
target's base used-by entry. Rejected: the staged duplicates of the four documents and the package entry named below. The non-author
spot-check is the closure's (LEARNING.md: a seat this lane dispatched is still the lane).

Gate lines (contract amendment 2; R, then T, then the quote; each located in the committed snapshot's extracted text):

- C2-QUOTE S265 S026: `about 84% of the transitions we observe from pass to fail involve a flaky test`
- C2-QUOTE S266 S048: `then it is likely that the last killing test will still kill it and it should therefore be prioritised above others`
- C2-QUOTE S267 S093: `--unshare-cgroup-try Create a new cgroup namespace if possible else skip it --unshare-all Unshare all possible namespaces. Currently equivalent with: --unshare-user-try --unshare-ipc --unshare-pid --unshare-net --unshare-uts --unshare-cgroup-try`
- C2-QUOTE S268 S108: `可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。应检查由此产生的差异是否存在意外的变化。`

### Admit — S265 (supersedes S026) and S266 (supersedes S048)

- **S265 (S026)** — https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html,
  opened 2026-10-26 (HTTP 200, 236387 bytes, sha256 `a4c5c46b4af9…`). Quote (15 words): “about
  84% of the transitions we observe from pass to fail involve a flaky test”. Location: post
  body, `div[itemprop='articleBody']` paragraph at raw line 1132 of the committed snapshot
  (publishdate 2016-05-27 at raw line 1082; the same sentence also appears in the page's
  `text/template` body copy at raw line 1097). Grounds `teaches`: the 84% pass-to-fail clause,
  which is the one the entry uses for the retry/rerun argument.
- **S266 (S048)** — https://pitest.org/quickstart/incremental_analysis/, opened 2026-10-26
  (HTTP 200, 8892 bytes, sha256 `e9cbc3e1ab7c…`, `Last-Modified: 2026-06-03`). Quote (21
  words): “then it is likely that the last killing test will still kill it and it should
  therefore be prioritised above others”. Location: `§Incremental analysis`, the fourth `<li>`
  of the optimisation list (raw line 86), immediately after “If a mutation was previously
  killed, but the class or killing test has changed”. Grounds `teaches`: item 4's consequent is
  a prioritisation, not a reuse skip, and the pronoun in “still kill it” is left unresolved.
  This is the consequence round-45's dispute said the old quote dropped.

Two subsections, in the round-45 house style (`corpus/lessons/round-45.md:16-62`).

````markdown
### Supersede — S267 (new row): bwrap(1), bubblewrap 0.13.1, raw `bwrap.xml`

- URL https://github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml (row's source cell); the fetched bytes
  are the tag's raw file https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml; access date
  2026-10-26; 33 289 bytes. Snapshot `.ufo/evidence/round-48/freshness/sources/S093.xml`, SHA-256
  `2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da`; fetch receipt
  `S093.receipt.json` (http_status 200, fetched_at 2026-10-26T08:41:10Z, same digest and byte count).
  This digest is the row's own pin, so the re-anchor changes no bytes' identity — only the quote.
- Located quote (amendment-2 extraction of the snapshot: UTF-8, no script/style content, tags stripped,
  entities unescaped, whitespace collapsed; found once, at normalized offset 2 641 of 16 699 characters;
  **25 tokens**):
  - `<quote>` — spans two consecutive `<varlistentry>` blocks of §Options: `--unshare-cgroup-try` at raw lines
    153–156 and `--unshare-all` at raw lines 157–160; quote lines 154–159, bytes 5 909–6 400.
- Scope: the raw bwrap.xml at tag v0.13.1 documents `--unshare-all` as "Unshare all possible namespaces.
  Currently equivalent with:" the six flags `--unshare-user-try`, `--unshare-ipc`, `--unshare-pid`,
  `--unshare-net`, `--unshare-uts`, `--unshare-cgroup-try`, with `--unshare-user-try` (raw lines 130–131) and
  `--unshare-cgroup-try` (line 155) worded "if possible else skip it". It is not a measured security boundary
  for any argv, and nothing here claims one.
- Row change: `corpus/SOURCES.md:140` appends S267 as `docs`/`A`/`mined`, opened 2026-10-26, recheck
  `on-release`, anchor `§Options, the --unshare-cgroup-try and --unshare-all varlistentries at bwrap.xml raw
  lines 153–160 … snapshot .ufo/evidence/round-48/freshness/sources/S093.xml 33289 B sha256 2cb77df2f4be`,
  `used-by` `corpus/knowledge/regression-tally-completeness.md`.
- Cited by `corpus/knowledge/regression-tally-completeness.md` (`source:` S267 on line 1, `verified-at:
  2026-10-26` on line 2). Answers round-45's dispute of S093 (`CritJudge03`): the quote now names
  `--unshare-all`, carries its six-flag expansion whole and reaches the sixth flag with its try-else-skip
  wording.

### Supersede — S268 (new row): 黄金测试 zh-cn localization (TensorFlow Federated)

- URL https://www.tensorflow.org/federated/golden_tests?hl=zh-cn; access date 2026-10-26; 111 409 bytes;
  response `last-modified: Tue, 07 Jun 2022 16:32:12 GMT`. Snapshot
  `.ufo/evidence/round-48/freshness/sources/S108.html`, SHA-256
  `04e4c091715a9ee2258cb12f52af6c64aa3134c6afc3669501b14f20966d1af1`; fetch receipt `S108.receipt.json`
  (http_status 200, fetched_at 2026-10-26T08:41:18Z, same digest and byte count).
- Located quote (amendment-2 extraction; found once, at offset 2 533 of 3 496 characters; **6 tokens**):
  - `<quote>` — the single `<p>` of the section `如何更新 .expected 文件？`, raw line 3611 (the `<h2>` is raw
    line 3609), inside the article body after the `path/ to/ some_test_goldens/` listing.
- Scope: the zh-cn page's wording only — `.expected` files are updated by running the affected test with
  `--test_arg=--update_goldens --test_strategy=local`, and the resulting diff is checked. The English upstream
  row S107 (commit-pinned) stays the tier-A statement; this row is tier B for the wording on this page.
- Row change: `corpus/SOURCES.md:141` appends S268 as `docs`/`B`/`mined`, opened 2026-10-26, recheck `180d`,
  anchor `§如何更新 .expected 文件？, the section's single paragraph at page raw line 3611 … snapshot
  .ufo/evidence/round-48/freshness/sources/S108.html 111409 B sha256 04e4c091715a`, `used-by`
  `corpus/knowledge/r8-golden-update-flag.md`.
- Cited by `corpus/knowledge/r8-golden-update-flag.md` (`source:` S268 on line 1, `verified-at: 2026-10-26`
  on line 2). Round 45 raised no dispute for S108 (`reviews.json`: `RevJudge02` → `agree`).
````

In both subsections `<quote>` is the §2 line's backticked text, verbatim, so the prose and the machine-read
line cannot drift apart.

### Reject — staged copies of the four C2 documents (`merge/tameshi/SOURCES.append.md`)

Every staged row whose document is one of the four C2 targets is a duplicate of a held lane row (dedupe by document, CORPUS.md rule 2:
a correction is a new row that supersedes, never a second copy): `.ufo/waves/round-48/w1/T48ScoutPackage.md` tables "Staged themes" and
"C2 hazards". Reason: the lane already holds the document; the round-48 rows supersede the held rows' anchors from this round's own fetch,
not the package's. Flip: a staged row that names a different revision or section of one of these documents than the lane holds.

### Reject (re-stated) — package entry `r8-predictive-test-selection-cost.md`

Refused again, with the decisive reason the round-47 closure named: it cites staged row S205 (arXiv 1810.05286), which this lane has never
opened (`grep -c 1810.05286 corpus/SOURCES.md` → 0; QUALITY 10). The round-47 refusal's `PROVINCE.md:14-18` pointer was the weaker reason
(correction C1-R48-2 below). Flip: a lane-opened row for that paper tied to an own-leg F7 re-sweep decision.

Rows touched old→new: none (S026, S048, S093 and S108 keep their status, recheck and used-by cells; the entries keep the old ids beside the new).

## Corrections to earlier lessons (append-only)

## Correction C1-R48-1 — the round-47 dependence sets (unreceipted freeze-time observation)

Class: reference-drift + stale observation (a freeze-time observation restated as the round's dependence finding: the pointer it gives, `before/c1-at-freeze.stdout`, is offered for the `total=22` figure and not for the sets, no revision is named beside them, and they disagree with the rows that same round pinned — one of them, `hermetic`, also disagreeing with the deciding run).

### What was stated, and where

`corpus/lessons/round-47.md` (sha256 `50b47845be5609a6…`, 14348 B), lines 117-118, verbatim:

```
at the freeze `total=22` (every row lacked the clause; `before/c1-at-freeze.stdout`); observed dependence sets: `six-leg regression ledger` {fleet-root, node}, `effective expectation reconciliation` {jj},
`retained invocation-context gate` {fleet-root}, `hermetic env-differential probe` {env, node}, `mutation report interop` {node}; the other 17 observed `none`. C3: `python3 .ufo/evidence/round-47/coverage/measure.py --lane LANE --rev REV`; before `rows=0 entries=0`.
```

The two sets this correction is about are `six-leg regression ledger` {fleet-root, node} and `hermetic env-differential probe` {env, node}. The lesson calls them "observed dependence sets" in a paragraph that ends "The deciding values are in the report and SCORECARD.md" — i.e. they read as the round's dependence finding, which is what the round-47 standing rows restate. They are not.

### What the standing rows state

`SCORECARD.md:2270` (standing self-assessment re-stated at round 47, `### Standing self-assessment — re-stated at round 47`, which opens at `:2262`), verbatim:

```
| six-leg regression ledger | replay every recorded mutation case (nine legs since round 26; the name is kept as the row id) at its pinned blob; exact expectation | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: FAIL (cases=9 passed=7`, exit 1, tool sha256 `a7d3f2dd7d47`, deps `env,fleet-root,node` | historical round 7 (four legs) / round 10 (six) / round 26 (nine) |
```

`SCORECARD.md:2276`, verbatim:

```
| hermetic env-differential probe | classify the raw exit/stdout/stderr tuple of nine pinned selftests under seven explicit profiles; the committed receipt `.ufo/evidence/round-21/f5/receipt-initial.json` classes eight `invariant` and one `nondeterministic` (`js-round-gate`), not "raw-output-variable" as the row above says | `python3 tools/env-diff.py --selftest` → `ENVDIFF_SELFTEST: 9/9 pass`, exit 0, tool sha256 `e8b47ab7cf23`, deps `bwrap,node` | round 21 |
```

So the rows declare {env, fleet-root, node} and {bwrap, node}.

### What was observed, and by which receipt

The deciding run at content revision `8b0e15d25ea598c0bf908d183fb410a085bf3a18`, `.ufo/evidence/round-47/after/c1.stdout` (sha256 `b56a8c2a861664046d6026a95dd452b00ec9331b00e5b523eeb9e0e0b6b37305`, 11099 B, `after/c1.exit` = 1), line 5 verbatim:

```
STATEMENT cap/six-leg regression ledger: claimed=REGRESSION: FAIL (cases=9 passed=7|1|a7d3f2dd7d47 observed=REGRESSION: PASS (cases=9 passed=9|0|a7d3f2dd7d47 (exit=0) MISMATCH declared_deps=env,fleet-root,node observed_deps=fleet-root,node DEPS-MISMATCH
```

line 17 verbatim:

```
STATEMENT cap/hermetic env-differential probe: claimed=ENVDIFF_SELFTEST: 9/9 pass|0|e8b47ab7cf23 observed=ENVDIFF_SELFTEST: 9/9 pass|0|e8b47ab7cf23 (exit=0) MATCH declared_deps=bwrap,node observed_deps=bwrap,node DEPS-OK
```

and the verdict line (`.` = `after/c1.stdout` last line):

```
C1_R47: self_pin=1 stmts_pin=1 statements=22 mismatches=1 unparsed=0 unobservable=0 dep_mismatch=1 unpinned=0 append_only=1 total=2 rev=8b0e15d25ea598c0bf908d183fb410a085bf3a18 C1_R47_PASS=false
```

The deciding run therefore observed {fleet-root, node} for `six-leg regression ledger` (matching the lesson, disagreeing with that row's `deps` → `DEPS-MISMATCH`) and {bwrap, node} for `hermetic env-differential probe` (matching that row, disagreeing with the lesson).

The lesson's two sets are byte-identical to the **freeze-time** emission, not the content revision: `.ufo/evidence/round-47/before/c1-at-freeze.stdout` (sha256 `27ca1e91cc61f08c…`) lines 5 and 17, and `.ufo/evidence/round-47/control/emit-observed-pre-freeze.out` (sha256 `1d70c44ed2edbc82…`) lines 5 and 17:

```
STATEMENT cap/six-leg regression ledger: claimed=- observed=REGRESSION: PASS (cases=9 passed=9|0|a7d3f2dd7d47 (exit=0) UNPARSED declared_deps=- observed_deps=fleet-root,node DEPS-OK
STATEMENT cap/hermetic env-differential probe: claimed=- observed=ENVDIFF_SELFTEST: 9/9 pass|0|e8b47ab7cf23 (exit=0) UNPARSED declared_deps=- observed_deps=env,node DEPS-OK
```

The round-47 disclosure already said both sets are unstable (`SCORECARD.md:2314`, tail quoted): "its dependence set was {env, node} in one run and {bwrap, node} in another … a deciding run that observes a different set for either statement is a `dep_mismatch` and is reported as such, not re-run until it agrees." The declared `env,fleet-root,node` for `six-leg regression ledger` traces to a wave-1 probe under load, `.ufo/waves/round-47/w1/T47CritC1Control.md:253`: "six-leg regression ledger … quiet: P2=`REGRESSION: PASS (cases=9 passed=9`, exit 0   → deps env,fleet-root,node".

### Delta, stated narrowly

- As a description of the **freeze-time** emission the lesson is accurate, but it does not name that receipt, the revision or the round, inside a paragraph whose closing sentence points the reader at the deciding values.
- As a description of **what the round-47 standing rows restate**, the sentence is wrong for both statements: the rows carry {env, fleet-root, node} and {bwrap, node}.
- The deciding run reproduced the lesson's `six-leg` set but not its `hermetic` set; the `six-leg` row's declared set is the one the deciding run scored `DEPS-MISMATCH`.

### Correction block to append (round-48 lesson)

```
- **C1-R48-1 (corrects `corpus/lessons/round-47.md:117-118`; the file is never rewritten).**
  The round-47 lesson's "observed dependence sets" — `six-leg regression ledger` {fleet-root, node},
  `hermetic env-differential probe` {env, node} — are the **freeze-time** emission
  (`.ufo/evidence/round-47/before/c1-at-freeze.stdout:5,17` =
  `control/emit-observed-pre-freeze.out:5,17`), printed there without receipt, revision or round.
  The round-47 standing rows, which restate the content-revision emission, declare
  {env, fleet-root, node} (`SCORECARD.md:2270`) and {bwrap, node} (`SCORECARD.md:2276`); the
  deciding run at `8b0e15d2…` observed {fleet-root, node} and {bwrap, node} and scored the
  `six-leg` row `DEPS-MISMATCH` (`.ufo/evidence/round-47/after/c1.stdout:5,17`, verdict
  `total=2 … dep_mismatch=1 … C1_R47_PASS=false`). Both statements are the two the round-47
  disclosure names as unstable across runs under host load (`SCORECARD.md:2314`).
  **Rule for later rounds:** a dependence set is restated only from the deciding `--emit`, with
  that receipt's path and revision named beside it; a freeze-time set is labelled as the freeze
  state and never presented as the round's observed finding.
```

### Provenance

| artifact | sha256 (first 16) | bytes | lines cited |
|---|---|---|---|
| `corpus/lessons/round-47.md` | `50b47845be5609a6` | 14348 | 117-118 |
| `SCORECARD.md` (lane worktree) | `954e057f9395ff06` | 248883 | 2262, 2270, 2276, 2314 |
| `.ufo/evidence/round-47/after/c1.stdout` | `b56a8c2a86166404` | 11099 | 5, 17, last |
| `.ufo/evidence/round-47/before/c1-at-freeze.stdout` | `27ca1e91cc61f08c` | 10017 | 5, 17 |
| `.ufo/evidence/round-47/control/emit-observed-pre-freeze.out` | `1d70c44ed2edbc82` | 18790 | 5, 17 |
| `.ufo/waves/round-47/w1/T47CritC1Control.md` | `6db680af53bd341c` | 27649 | 253 |
| `corpus/lessons/round-47-verifier-spotcheck.md` | `1b245d7e8b96eba0` | 15711 | 25, 105 |

---

## Correction C1-R48-2 — the refusal of `r8-predictive-test-selection-cost.md` (wrong decisive cite)

Class: reference-drift (a criterion citation that does not say what it is cited for) + misattributed reason.

### What was stated, and where

Three places, all in the round-47 record:

1. `corpus/lessons/round-47.md:81`, verbatim:

```
| `r8-predictive-test-selection-cost.md` | refused | out of province (vendor-scale test selection; `PROVINCE.md:14-18`), unopened row; QUALITY 10, 2 | a row opened by the lane that ties selection to an own-leg re-sweep decision (F7) |
```

2. `.ufo/waves/round-47/w1/T47RevProvince.md:30`, verbatim:

```
| `r8-predictive-test-selection-cost.md` | **REFUSE** (out of province, unopened row) | `PROVINCE.md:14-18` | 10, 2 |
```

3. `.ufo/waves/round-47/w1/T47RevProvince.md` §6.5 (`:428` onward), the cite as written, verbatim:

```
infrastructure. **PROVINCE.md:14-18** (product domain) and **QUALITY 10** (its
document `S205` / arXiv 1810.05286 is not a lane row: `grep -c '1810.05286'
corpus/SOURCES.md` → 0) and **QUALITY 2** (the quote's magnitude cannot be
checked against any committed snapshot).
```

### What the cited lines actually say

`PROVINCE.md:14-18`, verbatim:

```
**Refuses:** product domains — every lane's gate remains its own; tameshi
owns only the reusable craft (a pattern is admitted from evidence in TWO
independent lanes before it is claimed general). Never edits a sibling's
gate code (read-only probes; recommendations travel in round reports).
Credential material (→ kagi), endpoint health (→ kama).
```

These lines refuse product domains, sibling gate code and credential/endpoint material. They say nothing about test selection, cost baselines or evidence admission; the refusal they support is about *whose gate it is*, not about *whether the claim is anchored*. The decisive defect of the entry is the anchor: its `source:` cites `S205` / arXiv 1810.05286, and the lane has no such row — `grep -c '1810.05286' corpus/SOURCES.md` → `0`, `S205` → `0` (`corpus/SOURCES.md` sha256 `bb8f0997b820b859…`) — so the quoted magnitude has neither an opened row (QUALITY 10) nor a committed snapshot behind it (QUALITY 2). The package copy's own head (sha256 `af5bef5fa75f6e1a…`, 2770 B) carries `source: S205 — https://arxiv.org/abs/1810.05286 …`, `verified-at: 2026-10-24`, `ground: F7`.

QUALITY 10, verbatim (`corpus/QUALITY.md:27-30`): "A new `knowledge/` entry opens with `source:`, `verified-at:` and `recheck:`; an external source enters through a `SOURCES.md` row opened in the round that writes it (tiers: `SOURCES.md`, contract v1); a tier-C row is never sole support. (MK-7)". QUALITY 2, verbatim (`corpus/QUALITY.md:4-5`): "Every claim carries a source: a measured anchor (path:line, command, evidence id) — never oral knowledge."

### What the closure ruled

`corpus/lessons/round-47-verifier-spotcheck.md:90`, verbatim (reason column of the discernment table):

```
the decisive reason is QUALITY 10/2: the entry cites a row the lane never opened. The `PROVINCE.md:14-18` cite is weak (those lines refuse product domains and sibling gates, not test selection); the flip condition (an opened row tied to an own-leg F7 re-sweep decision) is the right one
```

and its routed item, `:106`, verbatim:

```
4. **Reject citation**: when refusing `r8-predictive-test-selection-cost.md` again, cite the unopened-row reason (QUALITY 10) rather than `PROVINCE.md:14-18`.
```

### Correction block to append (round-48 lesson)

The corrected row, ready for the round-48 lesson's package table (reason cell carries the decisive criterion; the flip condition is kept and made checkable):

```
| `r8-predictive-test-selection-cost.md` | refused | unopened row: its `source:` cites `S205` / arXiv 1810.05286 and the lane has no such row (`grep -c '1810.05286' corpus/SOURCES.md` → 0, `S205` → 0), so the quoted factor-of-two magnitude has no row opened in the round that writes it and no committed snapshot behind it — **QUALITY 10** (decisive) and **QUALITY 2**. The round-47 `PROVINCE.md:14-18` cite is withdrawn as the decisive reason: those lines refuse product domains, sibling gate code and credential/endpoint material, not test selection (closure ruling, `round-47-verifier-spotcheck.md:90`, routed item 4 at `:106`) | **flip:** a `S205` row opened `mined` in the writing round, carrying a committed round snapshot whose anchor the entry pins, **and** a named own-leg move that consumes change-level selection (F7 re-sweep). With the row opened but no consuming move, the entry stays a report line (its province argument survives as prose in `T47RevProvince.md` §6.5, which is never rewritten) |
```

### Provenance

| artifact | sha256 (first 16) | bytes | lines cited |
|---|---|---|---|
| `corpus/lessons/round-47.md` | `50b47845be5609a6` | 14348 | 81 |
| `.ufo/waves/round-47/w1/T47RevProvince.md` | `8984dc3f530cea9c` | 35475 | 30, 428+ (§6.5) |
| `PROVINCE.md` | `b2875fe21f381d98` | 6334 | 14-18 |
| `corpus/QUALITY.md` | `8fba0f5523f7eca8` | 88755 | 7 (4), 4-5 (2), 27-30 (10) |
| `corpus/SOURCES.md` | `bb8f0997b820b859` | 112478 | absence of `S205` / `1810.05286` |
| `corpus/lessons/round-47-verifier-spotcheck.md` | `1b245d7e8b96eba0` | 15711 | 25, 90, 105-106 |
| package `r8-predictive-test-selection-cost.md` (`/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/`) | `af5bef5fa75f6e1a` | 2770 | 1-5 (`source:`, `verified-at:`, `ground:`) |

---

## Not changed (bounds of this draft)

- `corpus/lessons/round-47.md`, `SCORECARD.md`, `PROVINCE.md`, `corpus/QUALITY.md`, `T47RevProvince.md` and the package copy are read-only to this seat; the corrections are appended ahead of them, per QUALITY 4.
- No counted surface is edited: the refusal row's verdict (`refused`) and the C1 numbers (`total=2`, `C1_R47_PASS=false`) stand as filed; only the *reason cited* and the *provenance of the stated sets* are corrected.
- The C1 counter, its rows and the round-48 predicates are the L1's; this draft neither re-runs nor rescopes them.
- `corpus/lessons/round-48.md` did not exist at this seat's run, so the destination is named, not written.

## Mistakes

Seven rows, one per mistake, classed by the `mistakes.md` §5 vocabulary. Row 1 is the round-47 C1 miss the
round-47 closure routed, and it is the premise this round's C1 counter is built against; rows 2–7 are the
round-47 conformance defects 1–5 plus the scratch incident, which the round-47 lesson did not record as
mistakes. Every row names the rule that should have caught it (`none` where no rule exists) and a fix whose
red state is shown by a command, not by prose. Readings are taken at the round-48 pre-data tree
(`f1cfaad3`, base `473336d9`); the round-47 receipts they compare against are committed at `edd4ca44` /
`663e0682`.

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `stale-premise` — the round-47 C1 miss: a one-shot flaky observation restated as a standing value | `.ufo/evidence/round-47/after/c1.stdout:5` — `six-leg regression ledger` claimed `REGRESSION: FAIL (cases=9 passed=7` exit 1, observed `REGRESSION: PASS (cases=9 passed=9` exit 0, `declared_deps=env,fleet-root,node` vs `observed_deps=fleet-root,node`; the paragraph naming the wrong row is `SCORECARD.md:2318` (`663e0682`); the instability was disclosed before the deciding run at `SCORECARD.md:2314` | `none` — the criterion governing these rows, QUALITY 92 (`corpus/QUALITY.md:1365-1369`), requires the value, its exit, the tool sha256 and a `deps` clause, and says nothing about how many times the value was observed; the round-47 contract's C1 statement (`.ufo/evidence/round-47/contract.json`, `claims.C1.statement`) asks only for the line "under the live host profile P0", i.e. one observation. Disclosure (SQ 2314) was not a gate | the standing row carries `runs 3 stable` or `runs 3 nondeterministic`, and the value set is scored against R=3 observation rounds with every declared member attested (`.ufo/evidence/round-48/contract.json:26`); counter `.ufo/evidence/round-48/calibration/measure.py`. Shown able to fail by the pre-registered relabel control CTL_B (`contract.json:33`): the round-47 rows re-appended verbatim with `runs 3 stable` must print false, and the six-leg row is the input that must be refused, because the deciding run's own P0 line does not reproduce its member (`after/c1.stdout:6`: `P0=REGRESSION: PASS (cases=9 passed=9`). Limits: CTL_B and the counter receipts are freeze-step-2 artifacts and were not executed for this draft (`d1`) |
| `scope` — a wave of the declared round shape was built, validated and never dispatched; the round closed below its floor | `.ufo/waves/round-47/spec-w2.json` carries 32 items (`jq '.items\|length'` → 32) and `.ufo/waves/round-47/w2/` holds only `swarm-registry.json`, so 0 seat reports; report `:52` states "planned and not dispatched" and "40 seats, below the 64–100 floor" | `none` — QUALITY 78 (`corpus/QUALITY.md:931-943`) settles a *dispatched* wave whose parent exits before seat terminals and says in terms "Prepared specs are not dispatched seats"; no criterion refuses a round that closes with a declared wave unrun, and none compares the counted seat total against the floor | the round prints a counted shape line before any claim is scored — seat reports found per wave directory against the declared total — and a wave with a spec, a dispatch file and no seat report is reported as not dispatched, never as run (`d2`). Red state: the same count over round 47 reads `w2` = 0 seat reports against 32 spec items and 64 declared |
| `landing` — selftest tallies are cited as evidence but no receipt for any of them is committed | `.ufo/evidence/round-47/selftest/` holds 0 files (`find … -type f \| wc -l` → 0) while the report `:12` cites `C1 35/35, C2 pool 14/14, C3 24/24` and `SCORECARD.md:2308-2310` cites `addition-lint.py --selftest` → `cases=7 failed=0`; round 46 committed the same shape as `.ufo/evidence/round-46/selftest/c{1,2,3}-selftest.{stdout,exit}` (6 files) | `none` — criterion 88 (`corpus/QUALITY.md:1291-1315`) makes a committed receipt mandatory for the no-harm falsifier script only; criteria 92 and 93 name a `--selftest` command as their evidence and require no committed output for it | every selftest a claim or the frontier step cites commits `<name>-selftest.stdout` and its exit under `.ufo/evidence/round-48/selftest/` before the freeze, the round-46 layout reused. Red state: `d3` reads 0 for round 47 against three cited tallies and 6 for round 46 |
| `landing` — the falsifier of a shipped criterion has no receipt, and the receipt that exists contradicts the report's account of when it was taken | `.ufo/evidence/round-47/quality/c91-92-falsifiers.stdout` is 7 lines and ends `CRITERION-92-FALSIFIER-OK`; block 93 exists at `.ufo/evidence/round-47/quality/falsifiers.sh:26-36`; the report `:15` says the receipt was taken before 91 was added to the script, yet the same receipt carries `CRITERION-91-FALSIFIER-OK` | `none` — criterion 93 (`corpus/QUALITY.md:1371-1377`) names block 93 as its falsifier and requires no committed output; the round-46 precedent commits one (`QUALITY.md:1312-1315`: `c88-90-falsifiers.stdout`), so the omission is a regression, not an unwritten rule | one receipt per criterion block (`quality/c<N>-falsifier.stdout`), written after the block's last edit and naming the criteria it covers. Red state: `d4` counts 2 `CRITERION-…-FALSIFIER-OK` lines in a receipt cited for three criteria, so a block-per-criterion check exits 1 on the round-47 tree |
| `reference-drift` — the lesson restates a run-to-run unstable observation and the value it prints is not the one in the committed receipt | `corpus/lessons/round-47.md:118` states `hermetic env-differential probe` `{env, node}`; the content-revision receipt prints `observed_deps=bwrap,node` (`.ufo/evidence/round-47/after/c1.stdout:17`), and the two-run difference is disclosed at `SCORECARD.md:2314` (`{env, node}` in one run, `{bwrap, node}` in another) | `none` — criterion 91 (`corpus/QUALITY.md:1355-1361`) binds only located *quotes* to snapshots; criterion 92 binds a SCORECARD *row* to observed deps and leaves the lesson restatement unread | every number a lesson restates from a counter names the receipt line it came from, and the comparison runs. Red state: `d5` prints `1c1 / < env,node / --- / > bwrap,node` and exits 1 on the round-47 lesson against its own deciding receipt |
| `provider` — scratch placement on the shared `/tmp` volume filled it mid-wave, and no counter could see it | report `:17` (`/tmp` to 100%; each C1 counter pass clones the lane twelve times, ~2.3 GB; one seat held ~20 GB; two probes died on ENOSPC) and `.ufo/waves/round-47/w1/T47ExecObsD.md:30,199` (`C1_R47: clone/checkout failed` when the counter's clone hit ENOSPC at profile P2) | `none` — QUALITY 9 (`corpus/QUALITY.md:24`) is the rule that puts scratch in `/tmp`, and nothing bounds a counter's per-pass clone fan-out; QUALITY 92 (`QUALITY.md:1367`) states in terms that "free disk in `/tmp`" is a variable the profiles do not vary, so no monitor could go red before the volume filled; QUALITY 67 (`QUALITY.md:762-768`) binds a seat's `--regression --workdir` to its own scratch but not the counter's internal clones. Misroot itself did not occur (no seat file at the fleet root; QUALITY 77 clean) — the scratch half did | every seat and the L1 take a scratch root on a volume apart from `/tmp` (`/fast/scratch/hyaku/tameshi-r48/<Seat>`) with `trap 'rm -rf' EXIT`, a leftover tree is counted as that seat's defect, and the counter's work dir defaults outside `/tmp`. Red state: `d6` — `du -sh` and a directory count bound the wave's footprint (18 directories, 13 GB at this reading, live seats included), and any tree surviving the round is the failing state |
| `landing` — the report names a lane HEAD that is one commit behind the tree it delivered, and that commit rewrites a landed seat report* | report `:5` states lane HEAD `663e0682…`; `git rev-list --count 663e0682..03facb22` → 1, "run 7 wrap-up: straggler seat reports written after the landing (orchestrator commit, not a landing)", and `git diff --name-only 663e0682 03facb22` → `.ufo/waves/round-47/w1/T47ConnCross.md` only (+228/−214) | `none` — QUALITY 86 (`corpus/QUALITY.md:1156-1222`) binds a deciding receipt to the revision it measured, not the HEAD line a report prints; QUALITY 77 binds a seat report to the lane repo, not to the revision that carries it | the report's closing act reads the HEAD it names and the number of commits after the last cited one, and either the wrap-up commit lands before the report is written or it is named in the report. Red state: `d7` — the same count on the round-47 tree is 1, so a "cited tip is HEAD" check exits 1 |

\* The silent rewrite of an already-landed seat report is the same commit; the class is `landing` because the
delivered tree is not the tree the report cites, not because a counted surface moved (the rewritten file is
cited by no claim).

Red states, each a command run against the lane tree above (outputs as observed):

```
d1  git show edd4ca44:.ufo/evidence/round-47/after/c1.stdout | sed -n '5,6p'
    # claimed FAIL passed=7 | observed PASS passed=9 ; P0=PASS passed=9  (the input CTL_B must refuse)
d2  jq '.items|length' .ufo/waves/round-47/spec-w2.json ; ls .ufo/waves/round-47/w2/*.md 2>/dev/null | wc -l
    # 32 ; 0
d3  find .ufo/evidence/round-47/selftest -type f | wc -l ; find .ufo/evidence/round-46/selftest -type f | wc -l
    # 0 ; 6
d4  grep -c '^CRITERION-' .ufo/evidence/round-47/quality/c91-92-falsifiers.stdout
    # 2   (three criteria shipped: 91, 92, 93; block 93 at falsifiers.sh:26-36)
d5  diff <(grep -oP 'hermetic env-differential probe` \{\K[^}]*' corpus/lessons/round-47.md | tr -d ' ') \
          <(grep 'STATEMENT cap/hermetic' .ufo/evidence/round-47/after/c1.stdout | grep -oP 'observed_deps=\K[a-z,]+')
    # 1c1 / < env,node / --- / > bwrap,node   (exit 1)
d6  find /fast/scratch/hyaku/tameshi-r48 -mindepth 1 -maxdepth 1 -type d | wc -l ; du -sh /fast/scratch/hyaku/tameshi-r48
    # 18 ; 13G   (mid-wave; any tree left after the round is the defect)
d7  git rev-list --count 663e0682..03facb22
    # 1
```

Sweep that found no further mistake to restate: `corpus/lessons/round-47.md` `## Mistakes` carries five data
rows (`grep -n '^| ' corpus/lessons/round-47.md` → rows at `:105-109`), and its three rounds-46 rows (quote
fold, embedded oracle, self-referential pins) already ship red-before receipts (QUALITY 91 and 93, and the
deciding script's widened `FROZEN`), so restating them here would be a duplicate, not a new row. The five
round-47 conformance defects map onto rows 2–5 and 7 (defect 2 = row 7); defect 4's chronology contradiction
is carried inside row 4.

Provenance and limits of these rows: every `.ufo/evidence/round-47` path, commit, command and count above was
read on this seat's tree; the round-47 spot-check is cited only where it is the observation (the report's
account of when the receipt was taken). Row 1's fix is pre-registered, not executed: CTL_B and the C1 counter
receipts are freeze-step-2 artifacts, and this section claims none of them. Rows 2–7 are detectors only — the
fixes they name are the round-48 protocol's, and none is scored here.

### Mined mistake with a red-before receipt — attribution: environment masking reported as host-load nondeterminism

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `attribution` | `SCORECARD.md:2314` (round 47) says `hermetic env-differential probe` "printed `9/9` or `2/9` under the same profile (P1)" and calls the two observations "not stable across runs under host load"; `.ufo/waves/round-48/w1/T48RevenEnvDiff.md` §1-§3 shows the `2/9` is deterministic: the round-47 counter builds the P1 PATH shim inside `--work` and `tools/env-diff.py:68-71` mounts a tmpfs on `/tmp`, so a `--work` under `/tmp` masks the interpreter; receipts `.ufo/evidence/round-47/before/c1-at-freeze.stdout:18` (`--work` under `/tmp`: P1 `2/9`) vs `.ufo/evidence/round-47/after/c1.stdout:18` (`/var/tmp`: P1 `9/9`) | `none` — QUALITY 92 asks for a deps clause, not for the cause of a differing observation | the round-48 counter refuses `--work` under `/tmp` (`.ufo/evidence/round-48/calibration/measure.py` `under_tmp`; selftest case `T63_work_under_tmp_refused`, `.ufo/evidence/round-48/selftest/c1-r48-selftest.stdout`), so the masked value cannot enter a standing row; red-before: the round-47 counter accepts `--work /tmp/...` and prints the masked `2/9` (receipt above) |

## considerthese

### considerthese — `considerthese/2026-10-25.md` idea 5 (proposal uptake ledger)

Operator-authored, read-only. Ideas 1-3 were mined in rounds 45-47; idea 4 (tempo and capacity readout) is not mined and is not buildable
from the repo: commit timestamps are rewritten by the orchestrator (`473336d` and `e73389c` share 2026-10-26 01:11:52; three more pairs
share a second), so no per-round elapsed time can be derived (`w1/T48ScoutConsiderthese.md`). Idea 5 is mined as a table, not a tool:
of the eight absorbed proposals (10-24 p1-p5, 10-25 p1-p3), criteria 79 and 86 were cited in later rounds' lessons and spot-checks, and criteria 76, 78
and 80 were not cited after the round that wrote them (`grep -lE "(criterion|QUALITY) N\b" corpus/lessons/*.md`; waves and evidence are not searched,
so this is a lower bound). Proposals about a thing that recurs every round (a quote, a landing commit) fired; proposals about a one-off past incident did not.
Round 48 exercises criterion 79 on S108: seven live fetches of the zh-cn page returned HTTP 200 with seven distinct raw sha256 values
(104924, 111405 or 111409 bytes) and, after the amendment-2 extraction of six of them, two text variants (3496 and 3148 characters), both carrying `--update_goldens`;
the round-40 snapshot extracts to the 3496-character one. The snapshot is therefore the only carrier a quote can be located in: the S108 row's receipt
is bound to the snapshot's own fetch, and no round-48 check treats a second live fetch as byte-identical. Lands as: this lesson section; no QUALITY
criterion (the table has no falsifier a counter could pin) and no SOURCES row.

## C1 grounding (own corpus)

`.ufo/waves/round-48/w1/T48ConnCorpus.md` connects R=3 to the lane's flakiness rows; `.ufo/waves/round-48/w1/T48RevenRegression.md` shows
`six-leg regression ledger` is genuinely nondeterministic (a SIGPIPE race under `pipefail` in the pinned tsukuroi leg, one-sided PASS→FAIL,
4 of 40 runs of that leg's selftest at 6-way concurrency), which is why amendment 4 admits P1 observations for attestation.
