# Round 34 — verifier spot-check (integrator, hyaku)

author: hyaku closure (non-author integrator, @m_flash)
date: 2026-10-23
lane-round: tameshi r34 (attempt 1)
base: `3fc1b2fe0d17e4cdb3b215aafb9eb4c02f541f4d` (round-open lane tip, parent of `6aaad5b3`) → cited head: `dce02595632621a561c2f3884dc40a372e057255`
Dispatch digest (`.ufo/watchdog.log`, mutable — copied per closure duty):
`2026-10-23T16:09:11-03:00 launch tameshi round=34 pgid=3367092 driver=hyaku-inline attempt=1`
`2026-10-24T~01:30Z complete tameshi round=34 (in-session L1): landed, lane HEAD dce02595632621a561c2f3884dc40a372e057255 (ahead=0, clean); fleet report commit 034e22d6515a84152ecd7956f1bfad04f24a13f7`
(The orchestrator-supplied "before" pointer `0b99d48e` is itself an r34 lane commit, 16:34:19 —
the round-open tip is `3fc1b2f`. Recorded as a dispatch-digest error, not a lane defect; the axis
diff below is taken at the true base and at the supplied pointer, both.)

## Step-1 conformance

- **Report + authorship.** `git log --format='%an %H' -- .ufo/reports/round-34/tameshi.md` →
  `tameshi-shokunin 034e22d6515a84152ecd7956f1bfad04f24a13f7` and
  `tameshi-shokunin 34ea4ecb418f23d35b4734837dee3891626d3456`; identity
  `tameshi@shokunin.local` on both. Report at the contract path, no other file at that name.
- **Sections + SHONEN.** `## Work performed`, `## Landed changes`, `## Before → after measurements`,
  `## Sources & frontier`, `## Trend verdicts`, `## SHONEN` (four lines, one per `SHONEN.md` box,
  all `[~]` with pointers, no `[x]` claimed), plus `## Stale-lane`, `## Installs`, `## Round shape
  and seats`, `## Dead seats / refusals`, `## Open L0 questions`. Not a marker: real work,
  evidence pointers, checkable hashes.
- **Cited commits.** `git cat-file -t` + `git merge-base --is-ancestor <h> master` → exists and
  ancestor for `6aaad5b3`, `9dd3174c`, `c17e593b`, `0b99d48e`, `a5b19364`, `d8eeb3a2`, `ecfc8e38`,
  and the before-receipt rev `732b6860`. `dce02595` (dev-dir receipt originals, 17:21:21) is not
  named in the report's Landed changes — defect 9 below.
- **Lane clean and pushed.** `jj-lane.sh state` →
  `branch=master local=dce02595 remote=dce02595 ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git status --porcelain` → empty. `git ls-remote origin refs/heads/master` → `dce02595…`.
- **Prompt fidelity.** `.ufo/prompts/tameshi-round-34.md` (372 lines) reproduces
  `templates/round-prompt.md` §1–§5 heading-for-heading and verbatim on the §2b frontier, §3 L2
  floor, §4 report-path and SHONEN paragraphs; the five child-lane items are present (report path
  and filename §4; commit-before-report ordering §5 + addendum item 4 "the report lands last and
  cites the pushed lane hash"; SHONEN heading §4; commit-hash citation rule addendum item 4
  "cite ONLY the helper's final `landed <hash>` line"; write scope §3). Addendum §6 present. No
  L2 route map is quoted, so no `MISSION.md` bucket mismatch is possible; §3's ≥8 floor is met by
  the one 64-seat wave. Round-level claims/frontier/marker/Sources&frontier/Trend sections all
  carried.

Conformance defects (status-neutral, routed below): misrooted seat report (1), missing provenance
trio (2), coverage-map index row missing (3), seat accounting omits the stranded seat (1),
attack-share convention (8), uncited `dce02595` (9). Disclosed-and-closed: Gate word count (4),
fetch receipt (5), selftest tail (6), stale contract citation (7).

## Claim re-check — C1 operability, capability acquisition: MEASURED TRUE (re-derived)

The counter was never run in default mode by this verifier (kill rule); every run below is a
module import of `c1-measure.py` plus direct runs of the pinned **tool** — the same surface the
wave seats used.

1. **Pins.** `sha256sum` at `c17e593b` and `dce02595`:
   tool `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10`,
   runner `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`,
   counter `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` — all three equal
   at `6aaad5b3`, `c17e593b`, `dce02595`. `git diff --stat 3fc1b2f dce02595 -- tools/` → empty.
2. **Controls receipt** (`9dd3174c`, at the amended counter): `counter_sha256` = `f6b8868c…a07f28c`
   (= the counter bytes at `c17e593b`), `all_false: true`, four rows all `predicate_pass: false`.
   Re-derived by running the four committed controls against my own copy set:
   `CtlAlwaysFail kill=26/26 accept=0/14`, `CtlAlwaysPass 0/26 14/14`, `CtlDoNothing 0/26 14/14`,
   `CtlShaOnly 26/26 1/14` — all four `predicate_pass=False` (public+sealed panel; the receipt's
   own numbers are the 26-copy public panel: `18/18 · 0/8`, `0/18 · 8/8`, `0/18 · 8/8`, `18/18 · 1/8`).
3. **Freeze-before-data.** `git log --diff-filter=A --format=%H <rev> -- <path>`: counter and tool
   added in `f6d8a891` (r33 contract freeze); all 14 sealed copies added in `c17e593b`, a
   descendant of `6aaad5b3` (amendment 6) and `9dd3174c` (controls). `counter_add`/`tool_add` are
   ancestors of every copy's adding commit.
4. **Panel + sealed outcomes, run by this verifier.** Reproduced the public panel by importing the
   counter module (`public_panel(runner_bytes_at_c17e593b, seed='685f63bd25263908')` → 26 copies:
   18 kill + 8 accept), regenerated the 14 sealed copies from their committed JSONs with
   `apply_edits`, and ran `python3 -I tool.py --runner <copy>` on each:
   **PUBLIC kill 18/18, accept 8/8; SEALED kill 8/8, accept 6/6; mismatches 0.**
5. **Sealed-copy validity.** `validate_ho` + `apply_edits` + the amended `ho_witness_ok` run over
   all 14 by module import: 14/14 valid, reasons `head`/`head-leg-assignment`/`vector`/
   `vector-equivalence`, **ho_invalid = 0**. Probe battery `dev/witness-probes.json` (8 verdicts)
   is byte-identical to its `stdout`: 8/8 exact on the set-aware gate.
6. **Tool selftest.** Re-ran `python3 -I tally-audit-v2.py --selftest` (copy at the pinned bytes):
   `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` — matches the report.
7. **Kill rule.** `.ufo/evidence/round-34/measure/c1-deciding-run.{stdout,exit}` =
   `… v1_kill=18/18 v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1
   seed=685f63bd25263908 rev=c17e593b… C1_R33_PASS=true`, exit `0`; `dev/` copies byte-identical
   (`cmp` clean, stderr 0 bytes). Before receipt `.ufo/evidence/round-33/after/c1-at-head-notrun.*`
   at `732b6860`: `controls_ok=0(receipt-missing) … heldout_after_freeze=0 C1_R33_PASS=false`,
   exit `1`. `grep -rl 'C1_R33_PASS=true' .ufo/evidence/` → only this receipt's two copies and
   `contract.json` (the label declaration): one distinct default-mode output, no re-run.
8. **No harm.** `git diff --stat 3fc1b2f dce02595 -- SCORECARD.md` → +36/−0 (pure append; at the
   supplied `0b99d48e` base it is empty, because that commit is inside the round). Files with any
   deletion in the round: `c1-measure.py` (+34/−4), `contract-amendments.json` (+39/−4) —
   amendment 6, disclosed pre-data — and `corpus/SOURCES.md` (+14/−1, the S100 `used-by` cell,
   old→new logged in the lesson). `SKILL.md`, `PROVINCE.md`, `SHONEN.md`, `corpus/QUALITY.md`
   untouched. Depth's command-D surface (the runner) is byte-identical at the pinned sha.
9. **Frontier.** `sources-census.sh validate --root … tameshi` → exit `0`, `tameshi ok`, W01
   `S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md` (disclosed in report and
   lesson), 8 pre-existing W04 duplicates. Row count `97` at `3fc1b2f` → `98` at `dce02595`
   (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` on each revision).

## Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| operability | improved | C1 re-derived above: capability admitted, controls-gated, 18/18+8/8+8/8+6/6, 0 invalid |
| depth | unchanged | recorded cases `9`; `git diff 3fc1b2f dce02595 -- tools/` empty; no new ledger leg |
| calibration | unchanged | r34 did not re-run the cold-read monitor; the r33 monitor bytes are unchanged and CalibMonitor falsified the routed premise (0 newly drifted inputs) |
| coverage | unchanged | no surface-count or frontier→core move claimed; the capability row is repertoire, not coverage |
| freshness | unchanged | pins re-verified unchanged at three revisions; stale `contract.json` tool citation remains open (defect 7) |
| adjacency | unchanged | no sibling scope taken; connector overlap seat clean; no sibling gate pins moved bytes |

No owned axis harmed; `SCORECARD` append-only; `tools/` untouched.

## Discernment spot-check (non-author, from outside)

| Decision | Re-opened | Verdict | Reason |
|---|---|---|---|
| **admit S101** (major mutation framework, tier C) | committed snapshot `.ufo/evidence/round-34/src/s101-mutation-testing.html` (4,341 B, sha256 `0fde8a7b…f420` = the Gate's digest); quote located in the "Overview" feature list after tag-strip; row `corpus/SOURCES.md:109`; `used-by` path exists | **agree** | quote is a verbatim fragment of the rendered Overview list; tier C for a framework overview page is honest; scope ("equivalent-mutant handling") matches the `teaches` line |
| **reject TLDP ABS exit-status** (duplicate of S097) | snapshot `.ufo/evidence/round-34/src/s101b-abs-exit-status.html` (9,728 B, sha256 `60cebcc8…d291`) — "Advanced Bash-Scripting Guide — Exit and Exit Status"; S097 row scope "Bash exit-status range and special statuses; the `case` command's first-match rule", tier A | **agree** | the ABS page restates ground S097 already holds at tier A; rowing it would duplicate a scope, not expand one |
| knowledge entry `corpus/knowledge/witness-equivalence-rule.md` (admitted, not in the Gate) | full file, `corpus/SOURCES.md` history, `corpus/README.md` | **disagree (form)** | substance is sound and cites S097+S101, but the entry was admitted with no Gate row and without the required provenance trio; not a false claim — a gate/format gap (defects 2-3) |

## Trend verdicts

- **expansion: improved** — new admitted `knowledge/` entry on ground the map did not hold
  (set-aware witness rule + voidability analysis), one new mined row (S101) with a committed
  snapshot, 97 → 98 rows. Caveat recorded: the coverage map has no index row for it (defect 3), so
  the LEARNING clause "each `source:` citing its coverage-map row" is formally unmet — the entry
  cites its SOURCES rows instead.
- **quality: improved** — the stale amendment-3 pin and the post-report commits were corrected
  append-only in `corpus/lessons/round-33.md` (+21/−0); the authoring harness caught a mis-authored
  witness before commit; the controls receipt attests the amended counter bytes; pins are
  byte-identical at every revision; no admitted entry was found false.
- **discernment: improved** — this outside spot-check agrees on the round's one admit and one
  reject with reasons; the lane corrected its own landed "whole-stdout landed" claim, restated an
  overstated sourced-claim line after CalibMonitor, disclosed its first W01, and rejected two
  duplicate sources rather than rowing them.

## Routed defects (round 35 / lane queue; status-neutral)

1. **Misrooted seat report.** `.ufo/waves/round-34/w1/ReviewDevReceipts.md` (136 lines, 9,561 B,
   mtime 2026-10-23 17:01:21) sits **untracked in the fleet repo**, not the lane. The lane's wave dir
   has 61 reports; the prompt's misroot sweep did not move/delete it and `## Mistakes` does not
   record it. Its F1/F2 findings are folded in the committed lesson, so no claim depends on the
   file — but the report's `## Dead seats / refusals` names only CriticVoidClaim, CalibMonitor and
   PanelSeed4, so the stranded seat is unaccounted. Not durable evidence where it sits.
2. **Provenance trio missing.** `corpus/knowledge/witness-equivalence-rule.md` opens with a title
   and author line; `CORPUS.md` "Additional corpus rules" requires `source:`, `verified-at:`,
   `recheck:` first.
3. **Coverage-map row missing.** `corpus/README.md` has no row for the new entry; a name-diff over
   `corpus/knowledge/` vs README bytes shows 3 unindexed entries (`runner-tally-audit-v2.md`,
   `survivor-fixture-minimization.md`, `witness-equivalence-rule.md`).
4. **Gate word count** — quote labeled 15 words, `wc -w` = 16 (≤25 contract satisfied; same class
   as the r33 routed defect). Disclosed; close it.
5. **`s101-fetch.exit`** commits `MUT_EXIT=0` (the successful mutation-testing.org fetch), not the
   gnu.org timeouts; the rejection ground is independently verified via S097's duplicate scope.
   Disclosed; no action beyond the r35 append it already names.
6. **`dev/tool-selftest.stdout`** is a 3-line tail of a 23-line run (disclosed); re-run by this
   verifier: `22/22 pass`. Full capture next round.
7. **`contract.json:frozen_artifacts.tool_sha256`** still cites `9dbbce62…33a4` while the counter's
   own pin is `7b11ba25…8d10`; disclosed by ReviewPinChain F1, r35 housekeeping.
8. **Attack-share convention.** Report's "52/64 = 81%" counts sentinel and revenger as attack
   roles; policy v2's list is reviewer/critic/mutation-tester/labrat → 50/64 = 78% (51 with
   revenger). ≥25% either way; state the convention next round.
9. **`dce02595` uncited.** The last lane commit (dev-dir deciding-run receipt originals,
   17:21:21) is not in the report's Landed changes; the report's final bytes (committer 17:21:29)
   postdate the cited `ecfc8e38` (17:19:43) and `dce02595` (17:21:21). All cited hashes are
   ancestors; minor.
10. **Capability bounds** (r35 Holds, not r34 defects): unswept (auto,KEEP) configurations
    (0,0)/(1,1), the twice-only substring head rule, whole-stdout comparison OPEN — all recorded in
    `corpus/lessons/round-34.md` Holds from the 64-seat wave and adopted only under the
    freeze-before-data discipline.

## Verdict

C1 verifies (re-derived, no default-mode run consumed). No axis harmed. Round admitted.
Tool installs by this verifier: none.
