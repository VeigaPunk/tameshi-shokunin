# round-81 verifier spot-check — tameshi (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Lane-round: tameshi 81 (hyaku run 15, attempt 1), 2026-11-04. Base
`56a0129fe9bfd0ce607290a36350e38ac4df9c72`; declaration `1b115ba0`; measured
commit `fc7ccfb7`; lane tip `ccef5f1de17bd44df6adacbb7f024f18628444ec`
(= `origin/master`). Report: `.ufo/reports/round-81/tameshi.md`. I did not
author this round; this file records verification only and improves nothing.

## 1. Conformance (PROTOCOL §Round-robin closure step 1)

- **Report landed by the lane, last.** `git log --format='%an %H' --
  .ufo/reports/round-81/tameshi.md` → `tameshi-shokunin <tameshi@shokunin.local>
  e3bc709c8ce75d2e16c19bb70d8a0dcb3eb70c6c`, filed 2026-11-04T06:17:29-03:00,
  after the lane tip `ccef5f1d` (06:15:58-03:00). Pushed: the commit is an
  ancestor of `origin/master`.
- **`SHONEN` heading.** Present, four `[~]` lines, one per `SHONEN.md` box,
  each with a resolvable pointer and the lane-assertion qualifier. No `[x]`
  and no non-author verifier claimed — correct for an unpromoted lane.
- **Cited lane commits exist and are ancestors of the branch ref.**
  `git merge-base --is-ancestor <hash> master` holds for `1b115ba0`,
  `349bad61`, `e27f28e8`, `1415fb65`, `fc7ccfb7`, `ccef5f1d` and the base
  `56a0129f`; no cited hash is missing.
- **No uncommitted round work; pushed.**
  `scripts/hyaku/jj-lane.sh state tameshi-shokunin` →
  `branch=master local=ccef5f1d remote=ccef5f1d ahead=0 behind=0 head=detached
  tracked=0 untracked=0`; `git -C tameshi-shokunin status --porcelain` prints
  nothing.
- **Prompt carries the contract.** `.ufo/prompts/tameshi-round-81.md` (704
  lines, committed `fe893236`) embeds §1 MISSION/AXES binding, §2 the 1–3 claim
  rule, §2b the frontier step, §3 the L2 floor (≥8 lanes, one batched swarm),
  §4 the report path and the five child-lane items (report path, commit-before-
  report, `SHONEN` heading, hash-citation rule, lane write scope), and §5
  commit-then-push, push scope and the L0 side channel. §3 binds routing to the
  host route table; MISSION.md's L2 table is role-class advisory and carries no
  role pins, so no quoted route map contradicts the current bucket.
- **Not a marker.** The report names real committed work, ten evidence
  pointers and the measured commit; it is a report, not a completion marker.

Conformance defects (status-neutral, routed below): the "manifest unchanged"
sentence and its receipt no longer hold at the measured commit (§2.1); two
SCORECARD evidence pointers name pre-wave receipts while their measured-commit
cell names `fc7ccfb7` (§2.1, §2.2); the "re-derived at the lane tip
`ccef5f1d`" sentence has no committed receipt (§2.4); the Stale-lane line does
not state the mission's age and progressing/silent state (§2.5).

## 2. Per-claim re-check

Each claim was re-derived with a plain measurement I ran myself over committed
bytes. A lane-owned gate/selftest was **not executed** (PROTOCOL §Gate
standard, Closure consequence): its committed evidence was read, and every
figure that could be re-counted by git/grep/python was re-counted.

### 2.1 R81-C1 — calibration: the routed-defect register is bound

- Population: `python3 -c 'import json;print(len(json.load(open("tools/defect-bind.json"))["rows"]))'`
  → `6`; the six row identities (id · kind · expect · tokens/paths) are
  identical at `1b115ba0` and `fc7ccfb7` (my comparison prints `True`).
- **Before, at the base tip `56a0129f`, re-derived row by row:**
  `git cat-file -s 56a0129f:<path>` → `MISSING` for
  `.ufo/evidence/round-80/coldread-at-f45.json` and
  `.ufo/evidence/round-80/design/census-before.txt`, and `0` for
  `.ufo/evidence/round-80/design/coldread-before.txt`;
  `git show 56a0129f:SCORECARD.md | grep -c 'Round-81 erratum (D2)'` → `0`;
  S289's `used-by` cell reads only `…round-61.md, …round-64.md,
  …round-79.md`; both S289 receipt paths are absent at `56a0129f`;
  `git show 56a0129f:corpus/SOURCES.md | awk '/^## Search log/,0' | grep -cE
  'Round 80:|Round 81:'` → `0`. Six rows open, matching
  `controls/c1-before.txt` and `c1-before-instrument-v2.txt`
  (`rows=6 closed=0 open=6 unexpected=6`, exit 1).
- **After, at `fc7ccfb7` (re-checked at `ccef5f1d`):** blob sizes
  `7160682` / `1888` / `7137391` (≥ 1 000 000 for D1b); the D2 span is present
  at `SCORECARD.md:5130-5131` and both `24/24` and `17/17` occur in
  `.ufo/evidence/round-80/design/c1-before-sweep.txt`; S289's cell now carries
  `corpus/lessons/round-80.md` **and** `corpus/lessons/round-81.md`; the S289
  receipts are `79488` B + `671` B; the `## Search log` section carries
  `Round 80:` (line 125) and `Round 81:` (line 139). Six rows closed, matching
  `final/c1-sweep.txt` (`rows=6 closed=6 open=0 unexpected=0`, exit 0).
- `--selftest` evidence: `final/c1-selftest.txt` → `DEFECT_BIND_SELFTEST:
  11/11 pass` (read, not executed). The 11 arms cover the five kinds, the
  `expect=open` standing arm, the refusal block, the multi-row summary and the
  blob-unresolvable refusal.
- **Defect (status-neutral).** The report's Before→after sentence says the
  population is not narrowed *and* prints `git rev-parse 1b115ba0:… = git
  rev-parse fc7ccfb7:tools/defect-bind.json` as an equality. The blob ids are
  `c8372447` vs `d92d6bea`: the manifest changed at the wave commit (the D2
  span was extended to the sentence pair carrying `24/24`/`17/17`, plus a
  re-indent). The row set and every declared token/path are unchanged, and the
  change is a tightening toward the frozen predicate, disclosed in the lesson —
  but the cited equality and `.ufo/evidence/round-81/manifest-binding.txt`
  (measured tip `e27f28e8`, before the wave commit) no longer support the
  measured-commit sentence. Reissue the receipt at `fc7ccfb7` and log the
  manifest delta old→new.
- **Verdict: improved (measured).** The claim's own predicate —
  `DEFECT_BIND: rows=6 closed=6 open=0 unexpected=0` at the tip — holds, and
  the do-nothing control (base tree, declared manifest) still reads six open.

### 2.2 R81-C2 — freshness: every standing row pins settled instrument bytes

- Population: `23` rows (`python3` length of `tools/selfstate-freshness.json`).
- **Before:** manifest at `1b115ba0` audited against tip `56a0129f` by my own
  blob-equality loop (`git rev-parse <pin>:<path>` vs `git rev-parse
  <tip>:<path>`) → `rows 23 settled 20 stale 3`, stale =
  `receipt-exists-selftest`, `receipt-bind-selftest`, `registry-bind-selftest`.
  This reproduces `controls/c2-before.txt` (`settled=20 stale=3`, exit 1)
  row-for-row and names the same three rows.
- **After:** the same loop at `fc7ccfb7` with the tip manifest → `rows 23
  unsettled 0`; repeated at `ccef5f1d` → `rows 23 unsettled 0`. Matches
  `final/c2-pins.txt` (`tip=fc7ccfb7…`, `rows=23 settled=23 stale=0`, exit 0).
- **Re-pin delta:** `git diff --numstat 1b115ba0..ccef5f1d --
  tools/selfstate-freshness.json` → `3 3`, and the three changed lines are the
  three `instrument.rev` pins (`21ef81e9…`→`4af6695f…`, `ae591d5a…`→
  `01ca77cd…` twice). No row added or removed.
- **Standing sweep stays green:** `final/c2-sweep.txt` → `SELFSTATE: rows=23
  match=21 stale=2 unexpected=0`, exit 0; the two stale rows are the declared
  red arms (`r74-frozen-addr-six`, `r76-r17-evidence-disposition`).
  `final/c2-selftest.txt` → `SELFSTATE_SELFTEST: 21/21 pass` (read, not
  executed).
- **Verdict: improved (measured).**

### 2.3 R81-C3 — coverage: the suite's own assertion text is pinned

- **Before, base tool bytes.** `git show 56a0129f:tools/selfstate-freshness.py |
  sha256sum` → `0c4ac5e4…` (50 805 B) and `…tools/wave-reconcile.py` →
  `2dfeda82…` (38 894 B) — equal to the `pristine-sha256` in
  `controls/c3-base-ss.txt` / `c3-base-wr.txt`. Those receipts print
  `SELFSTATE_SELFTEST: 17/17 pass`, `WAVE_RECONCILE_SELFTEST: 24/24 pass`,
  `DEFECT ss-bom-only: SURVIVED` / `DEFECT wr-prefix: SURVIVED`, and
  `MUTATE: DONE (… defects=1 killed=0 survived=1 …)` with `CONTROL: GREEN`
  and byte-identical restore. The two survivors are also named at
  `corpus/lessons/round-80.md:189-190`.
- **After.** `git show ccef5f1d:tools/selfstate-freshness.py | sha256sum` →
  `6624f5db…` (60 111 B); `…tools/wave-reconcile.py` → `8be64d02…` (40 404 B)
  — equal to the `MUTATE_TARGET` lines of `final/c3-battery-ss.txt` /
  `c3-battery-wr.txt`. `grep -c '^@defect'` on the two specs → `5` and `14`;
  the receipts carry `5` and `14` `DEFECT …: KILLED` lines, `0` `SURVIVED`,
  both `CONTROL: GREEN`, both `MUTATE_RESTORE: OK`, labels
  `selfstate-arms-r81` / `wave-reconcile-arms-r81`.
- **The pin is live, re-measured:** my own
  `sha256(inspect.getsource(<module>.selftest).encode())[:12]` →
  `a9feb3c49068` = `SELFTEST_TEXT_SHA256[:12]` for selfstate-freshness, and
  `3ea7fc7206c8` = the pinned value for wave-reconcile. The declared FAIL sets
  are singletons (`ss-bom-only` → `ARM21_selftest_text_pin`; `wr-prefix` →
  `arm25-selftest-text-pin`) in the receipts.
- The two batteries themselves were **evidence-verified, not executed**
  (§Gate standard). Their base/after tool shas were re-derived from the lane's
  own commits, and the digest constants were recomputed.
- **Verdict: improved (measured; batteries evidence-verified).**

### 2.4 Standing sweeps (no-harm), evidence-verified

`final/noharm-*.txt` at the measured commit read, in their summary lines:
`WAVE_RECONCILE: rows=6 met=6 unexpected=0`, `RECEIPT_BIND: receipts=29
bound=14 corrected=8 design=7 unbound=0`, `ADDRANGE: rows=11 met=11
unexpected=0`, `ARM_LIVENESS: rows=9 live=9 dead=0`, `COUNT_RECHECK: rows=7
met=7 unexpected=0`, `POINTER_RECHECK: rows=12 met=12 unexpected=0`,
`FIGURE_ATTRIBUTION: rows=3 met=3 unexpected=0`, `ANCHOR_DRIFT: rows=16
met=16 unexpected=0`, `MUTATE_SELFTEST: 107/107 pass`, `REGISTRY_BIND: rows=7
match=7 stale=0 absent=0 error=0 unexpected=0`. `SCORECARD.md` diff base→tip is
`+73 −1`; the single deletion is the `wave-record reconciliation` capability
row's figure `23/23`→`25/25`, not an axis score. No axis score is lowered.

**Defect (status-neutral).** The report's sentence "All three were re-derived
at the lane tip `ccef5f1d` after the receipts commit: identical outputs" has no
committed receipt; the final receipts name `fc7ccfb7` (C2's `tip=`).
**Defect (status-neutral).** The SCORECARD measured-claims table points R81-C1
at `.ufo/evidence/round-81/c1-after.txt` (D2 detail `tokens-in-receipt`, the
pre-wave instrument) and R81-C2 at `c2-after.txt` (`tip=e27f28e8`), while the
same rows' measured-commit cell reads `fc7ccfb7`. The tip receipts to cite are
`final/c1-sweep.txt` (`tokens-in-span-and-receipt`) and `final/c2-pins.txt`
(`tip=fc7ccfb7`).

## 3. Axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| calibration | improved | the round-80 closure's six routed defects measure `closed=6 open=0` at the tip, six `open` at the base, both re-derived row by row |
| freshness | improved | 20/23 settled → 23/23 settled at the tip by blob equality; the standing sweep stays green with only its two declared red arms |
| coverage | improved | the test-text edge class now has an arm in both suites; `ss-bom-only` and `wr-prefix` go from SURVIVED to KILLED |
| depth | unchanged | no depth claim; SKILL.md's registry rows were refreshed to the new figures, no score moved |
| operability | unchanged | three runnable instruments with committed selftests; no operability claim this round |
| adjacency | unchanged | the connector seat scanned sibling lanes; nothing absorbed, one unruled stray named (below) |

No axis is harmed: no SCORECARD score lowered, every standing sweep green, and
every after-state's restore byte-identical.

## 4. Discernment spot-check (LEARNING.md — checked from outside)

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tameshi` → exit `0`, verdict line `tameshi	ok	…/tameshi-shokunin/corpus/SOURCES.md`,
warnings only (W04 duplicate URL across scopes, one pre-existing W01 tier-C
mined row). Row count before→after re-counted by the census formula: `169 →
170`; status `mined 136→137`, `queued 22`, `rejected 11`; tiers `A 151→152`,
`B 14`, `C 4`; malformed rows `0`. Four mandated counts match the report.

The round-81 `## Gate` records one admit (S310) and **no rejected candidate**
("reject: none this round"); its second source question is a re-open of a held
document. The table below samples the admit, the re-open classification, and
the nearest recorded reject decision re-filed by this round's D6 search-log
note (S309, round 80's reject).

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S310 — Python 3.15 `inspect` (docs.python.org) | admit, tier A `mined` | committed snapshot `.ufo/evidence/round-81/sources/inspect315.html` (221 837 B, sha256 `7570b79d…`, headers HTTP/2 200, date `Wed, 04 Nov 2026 08:40:02 GMT`); raw page line 1193 | agree | line 1193 carries "Return the text of the source code for an object." — 10 words, ≤25; `getsource` returns text, which is exactly what the pin digests (my digest recompute matches the constant); `getsourcelines` is a sibling shape the pin does not need. Scope and anchor resolve. |
| S289 — Git `git-cat-file(1)` | reject a second row; re-open only | `git show 56a0129f:corpus/SOURCES.md` row S289; committed snapshot `s289-cat-file.html` (79 488 B, sha256 `91805d9a…`), `cmp` against `.ufo/evidence/round-79/sources/catfile.html` → exit 0 | agree | CORPUS.md rule 2 permits only `status`/`recheck`/`used-by` changes to a held document; a duplicate row for a held URL is refused (same precedent as S293), and the fetch receipt proves the re-open happened. `used-by` old→new is logged in the lesson. |
| S309 — Python 3.15 `sys` (docs.python.org) | reject, tier A `rejected` (re-filed by this round's D6 note) | committed snapshot `.ufo/evidence/round-80/sources/sys315.html` (sha256 `68094f11…`), line 999 | agree | the only `flags.isolated` prose maps the attribute to `-I` ("Changed in version 3.4: Added isolated attribute for -I isolated flag.", 11 words) and the snapshot carries no isolation-semantics prose (`grep 'isolated mode'` empty); the flip condition ("the page gains prose defining isolated mode") is correct. |

Disagreements: none on the sampled decisions. Observation (not a defect): the
round's Gate moves a small population — one new row, one re-open, zero rejects
— so this spot-check's reject side had to be sampled from the reject decision
re-filed by the round, not from a round-81 rejection. A future round that wants
a stronger reject sample must open and refuse at least one candidate.

## 5. Trend verdicts

- **expansion — improved.** Three capability rows entered `SCORECARD.md`
  (`closure-defect bind`, `standing-pin audit`, `selftest-text pin`), each with
  a runnable evidence pointer and `first-working round 81` (re-read at
  `SCORECARD.md:5175-5177`), and the coverage map gained the test-text edge
  class. `corpus/SOURCES.md` grew 169→170 with S310 admitted `mined` (the row
  the claim cites). Frontier rows advanced: none (`git diff 56a0129f ccef5f1d
  -- corpus/README.md` is empty, so the report's "none" is re-derived).
- **quality — improved.** Both standing suites gained 4 and 1 arms (17/21,
  24/25) and a byte-level pin audit; the D2 row now implements the declared
  predicate (`check_receipt_tokens` requires each token in the span **and** in
  the receipt); every after-state carries `CONTROL: GREEN` and a byte-identical
  `MUTATE_RESTORE: OK`. No admitted entry was found stale. The mid-round
  corrections are disclosed, not smoothed.
- **discernment — improved.** The round's own attacks changed it: the source
  scout caught two quote-metadata defects (S310 `11 words/1183` → `10
  words/1193`; pre-existing S307 `8`→`7` words), the surface scout caught the
  live capability figure (`23/23`→`25/25`) and both spec headers, the reviewer
  and critic independently broke the D2 row, and the mutation-tester showed
  two mutants that would have made the frozen before-states certify. Each is
  disclosed and most are repaired; the unclosed ones are named. My spot-check
  agrees on the sampled admit and reject decisions. The round's two mistakes
  produced `corpus/QUALITY.md` criteria 78–79, each citing the lesson.

## 6. Routed defects — round 82's queue (lane-owned)

1. **Manifest-binding receipt is stale at the measured commit.** Reissue
   `.ufo/evidence/round-81/manifest-binding.txt` at `fc7ccfb7`/`ccef5f1d`
   (the manifest changed there: D2 span extended, rows unchanged) and correct
   the report's `git rev-parse … = …` sentence by erratum, logging the blob
   delta old→new. The population is not narrowed and no `expect` relaxed; the
   defect is the record, not the claim.
2. **SCORECARD measured-claims pointers.** R81-C1/R81-C2 cite `c1-after.txt` /
   `c2-after.txt` (recorded tips `e27f28e8`; C1's D2 detail is the pre-wave
   `tokens-in-receipt`) while the measured-commit cell says `fc7ccfb7`; point
   them at `final/c1-sweep.txt` / `final/c2-pins.txt` or reissue at the tip.
3. **Unreceipted tip re-derivation.** The report's "re-derived at the lane tip
   `ccef5f1d` … identical outputs" sentence has no committed receipt; commit
   the tip re-run or drop the sentence.
4. **Stale-lane actuator.** The mission ran 2026-11-04T05:28:21-03:00 →
   06:18:14-03:00 (~49 m 53 s, ≈ 6.6 driver ticks; two ticks = 15 m). The
   report's Stale-lane line says only "no other mission of this lane is open";
   it must state the age and `progressing`/`silent`.
5. **Carried, already disclosed by the lane (confirm they land):**
   `defect-bind.py` reads its manifest from a path, so "no row removed /
   `expect` relaxed / population narrowed" is enforced by the frozen commit +
   receipt, not the instrument → `--manifest-rev` (D-CN3); `tree-paths`
   accepts a tree and `tree-bytes` is mode-blind (a symlink's target string
   satisfies `min_bytes`) → harden D1a/D5 and the byte kind; the C3 digest
   covers `getsource(selftest)` only (module-level misses, vacuous-comment
   over-kill, two-edit evasion) and `defect-bind.py`'s own text is unpinned;
   a failed `defect-bind --selftest` exits 1, the same code as an open register
   (D-CN1); two pin doctrines share one word (D-CN4).
6. **Capability-table placement (consistency).** The three round-81 capabilities
   sit in a round-specific `## Round 81 — capabilities entered` table rather
   than inside the live `## Capabilities` repertoire table; a reader can find
   them, but the repertoire table is the contract's single list.

Adjacency: the lane reports an unattributed one-line `after` file at the fleet
root and leaves it untouched — correct (operator-owned), no cross-lane defect
routed. No contested-scope report is open for this lane.

## 7. Operator note (promotion is operator-owned)

All four `SHONEN` boxes remain `[~]`; I wrote no `[x]` anywhere. Boxes 1, 2 and
4 look fully checkable from committed artifacts by a non-author
(`SKILL.md:2241` registry rows, `LOG.md:4373`, `PROVINCE.md` unchanged, each
with resolvable pointers). Box 3's evidence exists (tool contract at
`tools/defect-bind.py:1-60`, `DEFECT_BIND_SELFTEST: 11/11`), but the
"rebuilt from the plan text alone" witnesses (`T81W1E1/E2/E3`) are
lane-dispatched seats, so a truly independent cold-read remains operator-side.
Promotion, if wanted, is the operator's decision, not this file's.
