# round-82 verifier spot-check — tameshi (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Lane-round: tameshi 82 (hyaku run 15, attempt 1), 2026-11-04. Base
`4dfc3181310088c2f32d51e87a4d82c047d05231`; declaration `4005a48a`; landing
`b6658e7a`; wave commit `cfd59557`; final lane tip
`d9b02d653e11a9ab4c2234a5b92a4487fcc36f55` (= `origin/master`). Report:
`.ufo/reports/round-82/tameshi.md`. I did not author this round; this file
records verification only and improves nothing.

## 1. Conformance (PROTOCOL §Round-robin closure step 1)

- **Report landed by the lane, last.**
  `git log --format='%an <%ae> %H %ci %s' -- .ufo/reports/round-82/tameshi.md`
  → `tameshi-shokunin <tameshi@shokunin.local>
  5238f6d632516eb4ab30cd8a9dbefb547873dabf 2026-11-04 10:45:21 -0300`, filed
  15 s after the lane tip `d9b02d65` (10:45:06 -0300) and 38 s before the
  driver's complete line (10:45:59). The report commit is an ancestor of the
  fleet `origin/master` — pushed, not swept.
- **`SHONEN` heading.** Present, four `[~]` lines, one per `SHONEN.md` box,
  each with a resolvable pointer; the report says explicitly that no `[x]` is
  claimed. Correct for an unpromoted lane — no non-author verifier is
  impersonated.
- **Cited lane commits exist and are ancestors of the branch ref.**
  `git merge-base --is-ancestor <hash> master` returned true for all 13 cited
  hashes: `4dfc3181` (base), `4005a48a`, `b6658e7a`, `c8d40f5d`, `cfd59557`,
  `72832c94`, `ea618593`, `43fb2446`, `97f0186f`, `b37860b7`, `b95b61c1`,
  `9403eadf`, `d9b02d65`. No cited hash is missing; 16 commits ride the round
  range and every one is authored
  `tameshi-shokunin <tameshi@shokunin.local>` (`git log --format='%an <%ae>' |
  sort | uniq -c` → `16 tameshi-shokunin <tameshi@shokunin.local>`).
- **No uncommitted round work; pushed.**
  `scripts/hyaku/jj-lane.sh state tameshi-shokunin` →
  `branch=master local=d9b02d65 remote=d9b02d65 ahead=0 behind=0
  head=detached tracked=0 untracked=0`; `git -C tameshi-shokunin status
  --porcelain` prints nothing.
- **Prompt carries the template contract.** `.ufo/prompts/tameshi-round-82.md`
  (705 lines, committed `43156768`) — its first 140 lines are **byte-identical**
  to `templates/round-prompt.md` rendered with `{{LANE}}=tameshi`,
  `{{ROUND}}=82`, `{{FLEET_ROOT}}=/home/vgpnk/Projects/shokunin`,
  `{{AXES}}=depth + calibration (verification-fixture craft)` (my normalized
  diff prints `IDENTICAL`). That carries §1 MISSION/AXES binding, §2 the 1–3
  claim rule with the distinct-axis and lowest-axis clauses, §2b the frontier
  step, §3 the L2 floor (≥8 lanes, one batched AgentSwarm call) and the
  route-table binding, §4 the report path and the `SHONEN` heading with the
  hash-citation rule, and §5 commit-then-push, push scope and the L0 side
  channel. §6 is the run-15 campaign addendum. No quoted route map contradicts
  `MISSION.md` §L2 concurrency: that section's role-class buckets are advisory
  to host routing and the addendum records the operator's alias map as an
  amendment.
- **Dispatch/complete digest** (`.ufo/watchdog.log`, mutable; digests copied
  from the log at verification): `2026-11-04T10:06:55-03:00 launch tameshi
  round=82 pgid=1394009 driver=hyaku-inline attempt=1` (log line 2349);
  `2026-11-04T10:45:59-03:00 complete tameshi round=82; hyaku-inline attempt=1`
  (log line 2363).
- **Not a marker.** The report names real committed work, thirteen evidence
  pointers, a checkable final lane tip and a measured commit per claim.

Conformance defects (status-neutral; routed in §6): the lesson's `## Mistakes`
numbering skips 4 while the report says "1–6" (D1); the lesson's C3 FAIL-set
sentence is contradicted by the committed battery receipt (D2); the
census-refusal attribution is wrong in code and effect (D3); the git-ls-files
quote is one word off the page (D4); the Stale-lane line omits the age (D5);
one before-control cites an unresolvable scratch manifest (D6); the records
row of the landed-changes table points at one of six records commits (D7).

## 2. Per-claim re-check

Each claim was re-derived over the committed bytes of
`d9b02d65` with plain git/grep/jq/counting commands I ran myself. A lane-owned
gate or selftest was **not executed** (PROTOCOL §Gate standard, Closure
consequence); its committed evidence was read, and every static fact behind it
was re-counted. Labelled below: *re-measured* = I ran the counter; *evidence-
verified* = I read and cross-checked the committed receipt.

### 2.1 R82-C1 — calibration: the routed-defect register is content-bound

- *Re-measured, code presence.*
  `git show d9b02d65:tools/defect-bind.py | grep -c <token>` →
  `manifest-rev 9`, `manifest-rev-mismatch 3`, `GIT_NO_REPLACE_OBJECTS 1`,
  `read_manifest_bytes 3`, `manifest-not-regular 2`, `not-regular-file 8`,
  `SELFTEST_ARMS` 2 (line 89: `SELFTEST_ARMS = 14`). The same greps over
  `git show 4dfc3181:tools/defect-bind.py` print **0** for every token; base
  bytes 27,203 B / 670 lines, tip bytes 42,421 B / 972 lines.
- *Re-measured, population identity.* The manifest is unchanged in identity
  across the round: `git rev-parse <rev>:tools/defect-bind.json` →
  `1b115ba0` = `c8372447aa83…`, `fc7ccfb7` = `b6658e7a` = `d9b02d65` =
  `d92d6bea5516…`; row ids identical at every rev
  (`D1a-cited-receipts, D1b-coldread-before-bytes, D2-before-tokens,
  D4-s289-usedby, D5-s289-fetch-receipt, D6-searchlog-notes`; `rows=6` by a
  python JSON count). No row removed, no `expect` relaxed.
- *Evidence-verified, after-state*. `final/c1-bound.txt` (at `b37860b7`):
  `DEFECT_BIND: rows=6 closed=6 open=0 unexpected=0 manifest=bound`, `exit=0`.
  `final/c1-narrowed-refused.txt`: `defect-bind: manifest-rev-mismatch:HEAD:
  tools/defect-bind.json`, `exit=2`. `final/c1-directory-open.txt`: `state=open
  detail=not-regular-file:.ufo/evidence/round-81=040000`, `exit=1`.
  `final/c1-selftest.txt`: fourteen `ARM PASS` lines including
  `A12_regular_file_boundary` and `A13_manifest_rev_binding`, then
  `DEFECT_BIND_SELFTEST: 14/14 pass`, `exit=0`.
- *Evidence-verified, before-state*. `controls/c1-before-flag.txt`:
  `unrecognized arguments: --manifest-rev HEAD`, `exit=2`.
  `controls/c1-before-narrowed-certifies.txt`: `rows=5 closed=5 open=0
  unexpected=0`, `exit=0` (the narrowed register certified).
  `controls/c1-before-directory-closed.txt`: a directory row reads
  `state=closed detail=paths-present`.
- **Verdict: verifies.** The before→after is real on the committed bytes and
  the receipts name the revision they measured.

### 2.2 R82-C2 — freshness: the three round-81 capabilities are live rows

- *Re-measured, population.*
  `jq -r '.rows | length' tools/selfstate-freshness.json` → `26`; the same over
  `git show 4dfc3181:tools/selfstate-freshness.json` → `23`.
  `jq -r '.rows[].id' | grep -nE 'closure-defect-bind|standing-pin-audit|
  selftest-text-pin'` → lines 24, 25, 26 at the tip; the same grep over the
  base manifest prints `0`.
- *Re-measured, declared red arms.* `jq -r '.rows[].expect' | sort | uniq -c`
  → `24 match`, `2 stale`; the two `stale` rows are
  `r74-frozen-addr-six` and `r76-r17-evidence-disposition` — declared arms, so
  `match=24 stale=2 unexpected=0` is the consistent reading.
- *Re-measured, pin settlement for the three new rows.* Blob equality at the
  pin rev and the tip: `tools/defect-bind.py` at `b37860b7` and at `d9b02d65`
  = `d67603552c6a…`; `tools/selfstate-freshness.py` at `1b115ba0` and at
  `d9b02d65` = `19cffcb2e0ae…`. `closure-defect-bind` and `selftest-text-pin`
  pin `b37860b7`; `standing-pin-audit` pins `1b115ba0`, which is the last
  commit touching its instrument (`git log -1 -- tools/selfstate-freshness.py`
  → `1b115ba0`, 05:42 -0300).
- *Evidence-verified.* `final/c2-landed.txt`: the three `SELFSTATE_ROW` lines
  each read `expect=match measured=match ok` with the doc and measured figures
  identical, then `SELFSTATE: rows=26 match=24 stale=2 unexpected=0`, `exit=0`.
  `final/c2-pins.txt`: `SELFSTATE_PINS: rows=26 settled=26 stale=0`, `exit=0`.
  `final/final-tip.txt` re-reads both at `b95b61c1`.
- **Verdict: verifies.**

### 2.3 R82-C3 — coverage: the newest instrument's assertion text is pinned

- *Re-measured, target identity.*
  `git show d9b02d65:tools/defect-bind.py | sha256sum` →
  `f2ee351b95eb517664c895de4d772805b43c5d75e58cf665f46e3fc4dbd85bf0`, the
  exact `MUTATE_TARGET sha256=` the battery receipt names; base bytes
  `93278cd7c727…` / 27,203 B, the exact `MUTATE_TARGET sha256=` the base
  control names.
- *Re-measured, pin presence and non-vacuity.* `SELFTEST_TEXT_SHA256` and
  `A14_selftest_text_pin` appear in the tip bytes (lines 94, 890–894) and
  **zero** times in the base bytes. I re-derived the pin without running the
  suite: import the committed module, `hashlib.sha256(inspect.getsource(
  selftest).encode()).hexdigest()` → `9d2598911e8cd4a3…bfa773` = the module's
  constant (`match True`), which is also what every battery run prints
  (`measured=9d2598911e8c pinned=9d2598911e8c`).
- *Evidence-verified.* `final/c3-battery.txt`: `CONTROL: GREEN`, five
  `DEFECT … KILLED`, `MUTATE_RESTORE: OK` with identical before/after/pristine
  sha256, `MUTATE: DONE (target=defect-bind-arms-r82 defects=5 killed=5
  survived=0 inconclusive=0 kill-rate=100%)`, `exit=0`.
  `controls/c3-before-mutant.txt`: at the base bytes the same text mutant
  `SURVIVED (exit=0)` with the suite still `11/11` and `kill-rate=0%` — a true
  red-before. `final/c3-survivors.txt`: the wave's two custom survivors re-run
  `defects=2 killed=2`.
- **Verdict: verifies** for the claim's predicate (the surviving text mutant
  dies; the battery is 5/5 with a green control and a byte-identical restore).
  The lesson's *description* of the FAIL sets is wrong for one mutant — see
  D2; the SCORECARD's row states the multi-arm set correctly and the claim
  does not rest on singletons.

## 3. Axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| calibration | improved | C1: base certified a narrowed population (`rows=5 closed=5` exit 0) and read a directory as `closed`; the tip refuses the mismatch before any row effect (`manifest-rev-mismatch`, exit 2) and reads type/mode (`not-regular-file:…=040000`). Score stays 8 (lane-attainable cap) — the axis moved, the number cannot. |
| freshness | improved | C2: the three round-81 capabilities go from unmonitored to live rows (23 → 26) with pins that settle at the tip (blob equality re-derived for both instruments). |
| coverage | improved | C3: the tool's own assertion-text edge class is now governed — the A1 text mutant that survived at the base bytes (`11/11`, survived=1) is killed by A14; verdict-only axis, no numeric score. |
| depth | unchanged | No new depth artifact this round; the one new knowledge entry binds existing rows. |
| operability | unchanged | No new entry command topology; the standing sweeps all exit 0 (`noharm-*.txt`). |
| adjacency | unchanged | The connector's sibling scan is awareness (souji r19/r20, tabi r16 prior art), not a move; nothing absorbed. |

No axis is harmed: `git diff 4dfc3181 d9b02d65 -- SCORECARD.md` adds the three
repertoire rows, the round-82 claim records and the append-only correction
paragraph; no score cell is lowered and no admitted entry is marked stale.

## 4. Discernment spot-check (LEARNING.md — checked from outside)

Sampled from `corpus/lessons/round-82.md` `## Gate`. Two sources were re-opened
live with `curl -sS` (2026-11-04, this session) and compared with the committed
snapshots under `.ufo/evidence/round-82/sources/`; the third (the duplicate
decision) is grounded in the committed registry.

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S311 candidate — gitattributes docs | **reject** (within-scope duplicate of S294) | live `https://git-scm.com/docs/gitattributes` → HTTP 200, 131,174 B, sha256 `ceb3351f931a…`; committed `sources/gitattributes.html` identical; `corpus/SOURCES.md:169` holds the same URL as S294 (tier A, mined) | agree | A second row for a held, mined document on the same scope is a duplicate by CORPUS.md rule 2; the byte-identical fetch confirms it is the same document, and the refusal kept the registry at 170 rows. |
| S294 — re-open (the round's one admit) | **admit** (row re-opened, `used-by` extended) | same live re-fetch, raw line 2671: “converted from LF to CRLF depending on the `eol` attribute, the Git config, and the platform” — 16 words; the row's anchor quote still lives at raw lines 2678–2679 | agree | The mapped claim (line-ending conversion is a declared attribute layer, not a property of blob bytes) is what the page states; the row's disclosed furniture drift (131,046 → 131,174 B) does not change the cited contract. |
| `git-ls-files` | **reject** (index listing, not tree objects at a revision) | live `https://git-scm.com/docs/git-ls-files` → HTTP 200, 69,145 B, sha256 `c6970ba0c55a…`; raw line 2210: “This command merges the file listing in the index with the actual working directory list…” | agree on the decision; disagree on the quoted words | The page indeed describes index-vs-worktree merging, not tree objects, so the reject is right — but the lesson quotes “…working directory **files**”, a string that occurs 0 times in the page (`grep -c` → 0); the source says “directory **list**”. D4. |
| New-row ≤25-word quote | not applicable this round | `corpus/SOURCES.md` at base and tip: 170 rows → 170 rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`); field-level diff shows only `used-by` changed, on S289/S294/S305/S310 | agree | No new row exists to quote, so the new-row rule is vacuous; the nearest equivalent (S294's registry quote, above) was re-opened and verified instead. The report does not claim a new row. |
| Census | `validate --root … tameshi` | run by me at the tip | agree — exit 0 | Verdict `tameshi ok`; the W04 duplicate warnings are pre-existing across-scope rows, not round-82 additions; histograms re-counted: tiers `A=152 B=14 C=4`, status `mined=137 queued=22 rejected=11`, malformed rows 0. |

## 5. Trend verdicts

- **expansion — unchanged.** Re-counted: 0 rows added, 0 removed, 0 frontier
  rows advanced (report §Sources & frontier; my own 170 → 170 count and the
  field-level diff agree). One knowledge entry was admitted
  (`corpus/knowledge/counter-population-binding.md`) but it deepens
  PROVINCE Core's own counter craft on ground the coverage map already holds
  and cites held rows — the expansion observable is "net new admitted entries
  on uncovered ground", which this is not. No capability row entered.
- **quality — improved.** The counter's guarantee is stronger on measured
  evidence (C1 before/after above), three capabilities that had no monitor now
  carry live rows and settling pins (C2), and the newest suite's own text is
  pinned with the base mutant killed (C3). No admitted entry was found stale:
  the re-opened S294 quote still resolves in the live page, and every standing
  sweep in `final/noharm-*.txt` exits 0 (`WAVE_RECONCILE 6/6`,
  `RECEIPT_BIND receipts=29 unbound=0`, `ADDRANGE 11/11`, `ARM_LIVENESS 9/9`,
  `COUNT_RECHECK 7/7`, `POINTER_RECHECK 12/12`, `FIGURE_ATTRIBUTION 3/3`,
  `ANCHOR_DRIFT 16/16`, `REGISTRY_BIND 7/7`, `MUTATE_SELFTEST 107/107`).
- **discernment — improved.** This spot-check agrees with the gate on its one
  admit and both rejects (§4); the wave's own probes falsified the binding
  twice (a symlinked manifest and the double read) and both were repaired
  in-round with arms and criteria (repairs 3 and 5, criteria 80–83, each
  citing its lesson row); the batch's FAIL sets were examined for over-kill
  and the multi-arm failures are explained on the SCORECARD as genuine. The
  record defects in §6 are accuracy defects in prose, not wrong decisions, so
  the trend stands — but they must land as a correction next round.

## 6. Routed defects — round 83's queue (lane-owned)

1. **`## Mistakes` numbering skips 4; the report says "1–6".** The lesson's
   section carries rows 1, 2, 3, 5, 6 (five rows; the gap was present at the
   wave commit `cfd59557`, so no row was deleted — it is a drafting slip).
   Fix: number the rows consecutively in an appended correction, or state the
   numbering convention; the report's pointer should match the file.
2. **The lesson's C3 FAIL-set sentence is contradicted by its own receipt.**
   `corpus/lessons/round-82.md` (`## What was measured — R82-C3`) says “FAIL
   sets are singletons … `db-regular-file-check-removed` … →
   `A12_regular_file_boundary`. No over-kill.” The committed
   `final/c3-battery.txt` shows `db-regular-file-check-removed` failing
   **A10_multi_row_summary, A12_regular_file_boundary and
   A13_manifest_rev_binding** (and possibly A2/A7 — the receipt captures only
   arms A8–A14). The report's work-performed bullet repeats “FAIL sets
   singleton”. The SCORECARD row is accurate, so the claim itself is not
   affected. Fix: an append-only lesson correction naming the real sets, plus
   the full per-run arm output committed (the current receipt truncates
   A1–A7).
3. **The census-refusal attribution does not match the instrument.** The
   report and the lesson say the drafted S311 was “refused by the census as a
   within-scope duplicate (W04)”. The wave's own scout measured the opposite
   mapping: same-scope duplicate → `E04` exit 1, different scope → `W04` exit
   0 (a warning that would not refuse). No committed receipt of the actual
   draft refusal exists. Fix: append the correction naming `E04`/exit 1 (or,
   if the draft was refused by judgment rather than by the census, say that)
   and commit the refusal output.
4. **The `git-ls-files` reject quote is not verbatim.** The lesson quotes
   “…with the actual working directory files”; the page (live and snapshot,
   raw line 2210) reads “…with the actual working directory **list**”, and
   the quoted string occurs 0 times (`grep -c 'working directory files'` →
   0). The reject is right; the quote is a claim under the evidence standard.
   Fix: correct the quote in an appended correction.
5. **The Stale-lane line omits the age.** The mission ran
   2026-11-04T10:06:55-03:00 → 10:45:59-03:00 = 39 m 4 s, over the two-driver-
   tick (15 m) trigger. The line gives the launch timestamp and the word
   `progressing` but never states the age; the protocol requires both. Fix:
   state the age in the next report and in the correction entry.
6. **A before-control cites an unresolvable scratch manifest.**
   `controls/c1-before-directory-only.txt` records a run whose input is
   `/fast/scratch/hyaku/tameshi-r82/l1/dir-only.json` — not reachable at
   closure, so the receipt cannot be re-derived. The same base behaviour is
   independently shown by the committed `controls/c1-before-directory-closed.
   txt` (directory → `state=closed`). Fix: point the control at a committed
   manifest or drop it in favour of the committed one.
7. **Two arithmetic/pointer nits.** (a) The attack share counts the sentinel
   (`5/13 = 38.5 %`); the addendum's attack set is reviewer, critic,
   mutation-tester, labrat → `4/13 = 30.8 %`, still ≥25 %, so the claim is
   safe but the count is off. (b) The report cites “policy
   `ufo-wave-policy.json` (band 8–16)”; that JSON carries no band field — the
   band is the §6 addendum's. (c) The landed-changes table names `c8d40f5d`
   for “records” while the records were re-issued at `0e7d1603`, `7e06a403`,
   `df29efcc`, `63baceb6`, `b95b61c1` and `9403eadf`; say the row names the
   phase-opening commit or add the rows.

## 7. Operator note (promotion is operator-owned)

All four `SHONEN` boxes remain `[~]`; I wrote no `[x]` anywhere, and the
report claimed none. Boxes 1, 2 and 4 look fully checkable by a non-author
from committed artifacts (the round-82 registry section at `SKILL.md:2258` and
`REGISTRY_BIND 7/7`; the `LOG.md` round-82 entry with measured after-states;
`PROVINCE.md` unchanged and every surface read inside the lane), each with
resolvable pointers. Box 3's evidence exists (`DEFECT_BIND_SELFTEST: 14/14`,
the executable plan and the standing sweeps), but the cold-read witnesses are
lane-dispatched seats, so a genuinely independent cold read remains
operator-side. Promotion, if wanted, is the operator's decision, not this
file's.
