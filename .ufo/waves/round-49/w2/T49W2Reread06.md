# T49W2Reread06 — C1 semantic re-read, `### The map`, ordinals 0–8 (wave 2, falsify)

Seat: re-read the nine C1 rows for section `### The map` (ordinals 0–8) in
`.ufo/evidence/round-49/c1/reads.json` against the candidate
`f181a961ae44061af486f600e5ea257d2baf78f8`, and judge every correction the L1
made in that range. Read-only seat: no counter was run, nothing outside
`.ufo/waves/round-49/w2/` written. Deliverable: `T49W2Reread06.json` (this dir).

Verdict up front: **all nine rows support their clauses; no row is fabricated or
misexcerpted; every excerpt I checked is byte-present at the pointed place at
the candidate.** Three low-severity/informational findings below; none voids a
row or a correction boolean.

## Method

- Candidate SKILL.md and targets extracted at the exact revision:
  `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961…:SKILL.md` (2136 lines),
  same for LOG.md, the six knowledge notes, corpus/README.md, plus
  `git ls-tree --name-only f181a961… plans/` and `git diff --stat 8ca67421… f181a961…`.
- `git diff --stat` shows **no** `corpus/knowledge/*.md` file changed
  base→candidate, so wave-1 whole-file reads of the six note targets carry over;
  I re-verified every § heading and excerpt quote anyway.
- All SKILL.md diff hunks preserve line counts, so the two re-qualified
  self-pointers (`1246-1270`, `1294-1297`) point at identical bytes at base and
  candidate.
- Counter rationale check: `.ufo/evidence/round-49/c1/measure.py:271-279` —
  `if p['file'] is None: … status = 'unresolved'` (a path pointer may only pass
  as `absent`). Confirms why the bare `:N` map pointers had to be qualified.

## Row findings (ordinal / raw / verdict)

| # | raw | supports | evidence at f181a961 |
|---|-----|----------|----------------------|
| 0 | `SKILL.md:1294-1297` | true | 1294-1296: "Pointer, not a second home. Its own rule: where it and an anchored source diverge, the anchored source governs — the same rendering/divergence rule this page applies to `service-limits.md` (`:1250-1254`)." — SKILL's own statement about the runbook; the inner `:1250-1254` also resolves. `git show f181a961:SKILL.md \| sed -n '1294,1297p'` |
| 1 | `SKILL.md:1246-1270` | true | 1246 limits heading; excerpt verbatim at 1253-1254; refusals table a-j at 1258-1267. `git show f181a961:SKILL.md \| sed -n '1246,1270p'` |
| 2 | `LOG.md:316-317` | true | "…the lane deliverables in / this repo ARE the wave record (no `.ufo/waves/tameshi-r11-*` directory);" — the round's 13 LOG lines are appends elsewhere. `git show f181a961:LOG.md \| sed -n '316,317p'` |
| 3 | `corpus/knowledge/operator-runbook.md` | true | Role :3-6 verbatim; §0:35 §2:93 §3:131 §4:180 §5:243 §6:269 (T1–T3 :288-293) §7:345 §10:462; §3 has exactly six case rows (:131-179). |
| 4 | `corpus/knowledge/fleet-kill-rate-ledger.md` | true | Role :4-5 verbatim; 4 §1 rows + ER-2 :272 (rows 5-6) + Round 16 :403 + Round 18 :424 = 8 rows; no ninth-row block; "never as an edit of §1–§4" :311-312, "No §1–§4 cell is edited" :318. |
| 5 | `corpus/knowledge/service-limits.md` | true | Excerpt verbatim :11-12; §1 refusals a-j :46-55. (Drifted inner anchor inside the target — finding F3.) |
| 6 | `corpus/knowledge/service-optin-protocol.md` | true | Excerpt verbatim :6-8; §1:54 (re-pin :61-62) §2:109 §3:142 §4:182. |
| 7 | `corpus/knowledge/fleet-suite-census.md` | true | Offer verbatim :269-271 (span :269-275); queue :277; R.4 :594-615 surveyed-but-unmeasured (:607). |
| 8 | `corpus/knowledge/service-standing-state.md` | true | Excerpt verbatim :3-8; §1:49 §2:68 §3:80; SC1:159 SC2:174 SC3:181. |

## Findings by severity

**F1 [low] SKILL.md:1387 — the optin row's re-key drops the base item "boundaries".**
Base: "request shape, the re-pin rule, read-only guarantees, report shape, boundaries" →
candidate: "request shape (§1, including the re-pin rule), read-only guarantees
(§2), the owner-hardens rule (§3), report shape (§4)". All four § numbers resolve
and the re-pin rule is correctly placed in §1 (:61-62), but the scope statement
("single-edit mutants only; hermetic suites only; results are per-revision and
per-host", service-optin-protocol.md:23-26, in §0) is no longer named — a
meaning narrowing, not a false claim. Show:
`git diff 8ca67421 f181a961 -- SKILL.md` (hunk `@@ -1381,16 +1381,16 @@`),
`git show f181a961:corpus/knowledge/service-optin-protocol.md | sed -n '23,26p'`.
Suggested (owner's call): re-add e.g. "§0 scope boundaries" or accept the loss.

**F2 [low] SKILL.md:1390 — "pre-registration in the round-16/18/26 notes" is loose for round 26.**
`git show f181a961:corpus/lessons/round-16.md | grep -ci pre-regist` → 3;
round-18.md → 1; **round-26.md → 0**. The round-26 lesson still records the ninth
leg's registration content ("Admit candidates:
`corpus/knowledge/mutation-case-kumitate-cite-check.md`; the ninth leg in
`tools/mutate-and-run.sh` (spec, pin, table, replay call, …)”, round-26.md:23-24)
and the case note itself carries 3 "pre-regist" hits, so the claim is materially
right, only the attribution wording is imprecise. The companion hedge "reproduce
sections where the note carries one" is exactly right: 8 of 9 case notes have
reproduce sections; mutation-case-kumitate-sources-check.md has none.

**F3 [info, pre-existing, outside this section's rows] corpus/knowledge/service-limits.md:10.**
The note's inner anchor "`SKILL.md:1230-1249`" is drifted: the compact rendering
of the refusals table sits at SKILL.md:1256-1267 (intro 1248-1254) at both base
and candidate; the note was not edited this round (diff --stat), so round 49
introduced nothing — but the map's ordinal-5 target cites SKILL with a stale
span. The note is errata-capable (§7, :264) if the closure wants it fixed;
editing it is not in this seat's bounds.

## Correction judgments (all in hunk `@@ -1381,16 +1381,16 @@` of `git diff 8ca67421 f181a961 -- SKILL.md`)

| SKILL line | row | ok | note |
|---|-----|----|------|
| 1384 | operator-runbook | true | `:N`→`SKILL.md:N` right (measure.py:271-279 makes bare `:N` unresolved); "(six rows; nine cases since round 26)" verified |
| 1385 | fleet-kill-rate-ledger | true | "measured so far … (eight rows; the round-26 ninth case has no row yet)" verified exactly |
| 1386 | service-limits | true | `:1246-1270` qualification right; numbers hold base→candidate (line counts preserved) |
| 1387 | service-optin-protocol | true | §-citations all right; "boundaries" dropped (F1) |
| 1390 | mutation-case-*.md | true | reproduce hedge exact; pre-registration attribution loose for r26 (F2) |
| 1392 | corpus/README.md | true | "one knowledge note uncarried" verified: exactly `knowledge/r44-anchor-refresh-rule.md` is uncovered (49/50 non-case notes carried; `grep -o "knowledge/[a-z0-9-]*\.md"` on README vs `git ls-tree … corpus/knowledge/`) |
| 1393 | plans | true | round-4..10 plan+record-draft pairs, round-11.plan.md, and completion-evidence.md all in `plans/`; completion pack added in 284ab0f ("probation round 11 … closeout"), so "committed in the round-11 closeout" fixes the stale base wording |

Census (:1388), standing-state (:1389), mutate-and-run (:1391) and LOG/SCORECARD
(:1394) rows are untouched by the diff; their rows (7, 8) verified directly
against the targets above.

## Verification gaps

- I did not run the frozen counter (probes are not verdicts; not my item).
- Excerpt-location semantics of measure.py beyond the file-null block (271-279)
  were not audited; my mandate is the semantic support the counter cannot see.
- reads.json names candidate `9b9b2a0…` (wave-1's candidate) while this re-read
  is against the integrated `f181a961…` per my item; since no
  `corpus/knowledge/*.md` changed and SKILL hunks preserve line counts, every
  row re-verifies identically at `f181a961`.

Tooling: no tools installed or upgraded this seat (none needed). Scratch
`/fast/scratch/hyaku/tameshi-r49/T49W2Reread06/` deleted before yield; no /tmp
artifacts beyond transient reads; cited commands all reproducible against the
lane at `f181a961…` without scratch.

## Summary

- All 9 map rows (ordinals 0–8) support their clauses; every excerpt verified byte-present at f181a961; no fabrication found.
- Both self-pointer corrections (:1384, :1386) are right; bare `:N` is unresolved by measure.py:271-279, numbers hold base→candidate (line counts preserved).
- F1 [low] SKILL.md:1387 drops the base item "boundaries" (scope at optin :23-26 no longer named) — narrowing, not falsity.
- F2 [low] SKILL.md:1390 "pre-registration in the round-16/18/26 notes": round-26 lesson has 0 literal hits (content at :23-24; case note carries it) — wording loose, claim materially right.
- F3 [info] service-limits.md:10's inner anchor `SKILL.md:1230-1249` drifted (real span 1246-1270) — pre-existing, unchanged this round.
- All 7 map-section corrections judged ok=true; corrections at :1385/:1392/:1393 verified against ledger/README/plans bytes and commit 284ab0f.
- No counter run; no installs; scratch deleted.
