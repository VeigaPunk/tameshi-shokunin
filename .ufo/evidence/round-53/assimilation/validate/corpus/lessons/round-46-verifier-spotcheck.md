# Round 46 verifier spot-check

author: hyaku closure (non-author integrator, @m_sonnet)
date: 2026-10-25
lane HEAD measured: `b5425635961c3279c1bca95b8b42ca3816825df4` (base `683eedde3a50441c34d85a22f5fd5346f8b1ec6d`; content revision `3ae8b0484977c17dc9ce8b01e55c6afcebe2b116`; freeze `745a583181648cfc7f9c1b476cd1be7dc68f7433`)
driver lines (`.ufo/watchdog.log`): `2026-10-25T17:46:17-03:00 launch tameshi round=46 pgid=2147959 driver=hyaku-inline attempt=1`; `2026-10-25T20:22:17-03:00 complete tameshi round=46; hyaku-inline attempt=1`

## Step-1 conformance

| Check | Command | Observed |
|---|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-46/tameshi.md` (fleet repo) | `tameshi-shokunin e0bffbb6f701c5b179ab16b4e22e0f67ee4a6cb7` |
| SHONEN heading, one line per box | read report lines 64-69 | 1 `## SHONEN`, 4 `[~]` lines with prior pointers; none `[x]` |
| Cited commits are ancestors of `master` | `git merge-base --is-ancestor <h> master` for the 8 cited hashes (745a5831, 10a05fdf, a6892b19, e630ae79, 6f2168e0, eada0b36, 3ae8b048, b5425635) | all 8 `anc` |
| Lane pushed, clean | `jj-lane.sh state …/tameshi-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `local=remote=b5425635… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; ls-remote prints `b5425635…` |
| Criterion 86 receipts-only tail | `git diff --name-only 3ae8b048 b5425635 \| grep -vcE '^\.ufo/evidence/round-46/(after/\|census-end)'` | `0` |
| Prompt carries template contract | `grep -n` of `.ufo/prompts/tameshi-round-46.md` (545 lines) | §3 L2 floor, §4 report contract (SHONEN heading, hash citation, commit-before-report), §5 commit/push scope/L0, write scope line 318 (`/home/vgpnk/Projects/shokunin/tameshi-shokunin`) |
| Report is real work, not a marker | read report; 8 commits since base | 8 lane commits with evidence trees; not a marker |

Conformance defects (status-neutral): none material. Two notes: (a) the report's `after/` receipts are taken at `3ae8b048` and the deciding tail commit changes only receipts (0 paths outside `after/`, `census-end.*`), as criterion 86 requires; (b) the lesson's `## Gate` S259 quote is printed with a hyphen in `9.8 %-16.3 %` where the live source has an en dash `9.8 %–16.3 %` (lane `fold`); the entry `r5-undetected-flaky-failures.md:25,32` discloses the fold and quotes the en-dash form, so this is wording-only in the lesson.

## Per-claim re-check

Method: C1, C2, C3 rest on lane-owned counters. Per PROTOCOL §Gate standard (Closure consequence) I did not execute them; I verified their committed deciding stdout, the revision measured, the sha pins, the selftest tallies and the before receipts, and re-measured with plain commands what can be re-measured without the counters.

### C1 calibration (lowest non-retired axis, monitor 6): re-measured (inputs) + evidence-verified (counter)

Committed deciding line (`.ufo/evidence/round-46/after/c1.stdout`, rev `3ae8b048…`, exit 0): `C1_R46: self_pin=1 stmts_pin=1 statements=22 mismatches=0 unparsed=0 unobservable=0 append_only=1 total=0 … C1_R46_PASS=true`; `after/frozen.stdout`: `FROZEN_UNCHANGED=1`. Before (`before/c1-at-freeze.stdout`): `mismatches=2 unparsed=19 total=21 C1_R46_PASS=false` (calibration stated 8 vs observed 6; one truncated regression row).

My re-derivation:
- `sha256sum` of the 16 tool files named by the 19 capability rows vs the 12-hex prefixes in the SCORECARD restated table: all 16 equal (a7d3f2dd7d47, 296fe566dc59, 331529eadafe, df3390682a04, 39ee5c5effd9, 7e4519d9a0ea, e8b47ab7cf23, 96b3038a77f8, 9230c68e53a5, 9fcd2dbba737, 193ea6e32f89, 7b11ba25aead, da8c1ef4b30c, 402285329588, 095924a7a165, 03a796c5726c).
- `git diff --name-only 683eedde b5425635 -- tools | wc -l` → `0` (no tool changed, so the restated values are stable).
- `sha256sum calibration/statements.json` → `a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9` = contract pin; `sha256sum` of the five counters equals `after/frozen.stdout` `COUNTER_SHA256` lines.
- `git diff --name-only 745a583 3ae8b048 -- calibration coverage hardening contract.json`: only `hardening/{assemble,try-mutants,freshness-counter,coverage-counter}.py` changed (the wave-1/wave-2 hardening deliverable); `calibration/*`, `coverage/measure.py`, `mutants.json`, `mutate.py`, `contract.json` unchanged.
- `SCORECARD.md` diff base → HEAD is append-only (`git diff` shows 91 insertions, 0 deletions). Axis rows: depth 9 (nine ledger legs, `tools/mutate-and-run.sh:87-95` lists nine), calibration 6, freshness 9 (`floor(10*71/73)=9`), agree with `after/no-harm.stdout`.
- Selftest tally committed: `selftest/c1-selftest.stdout` `C1_R46_SELFTEST: cases=18 failed=0`, exit 0.

Ruling: calibration **improved** on the declared measure (mismatch count 21 → 0). The calibration monitor stays 6 → 6 and the lane claims no raise; the lane's own caveat that three statements are host-dependent (census over live root, `jj`/`bwrap` on PATH) and that the 8 → 6 correction is a stale-value fix is accepted as honest.

### C2 operability: evidence-verified

Committed deciding line (`after/c2.stdout`, rev `3ae8b048…`, exit 0): `declared=25 killed=25 survived=0 inapplicable=0 neutral_killed=0 pristine=1 equivalence=1 C2_R46_PASS=true`; per-mutant lines: 15 freshness + 10 coverage `killed`, 3 + 3 neutral `survived`. Before (`before/c2-at-freeze.stdout`): `killed=0 survived=25 … C2_R46_PASS=false` (`--targets orig`).

My checks: `hardening/mutants.json` holds 18 freshness + 13 coverage entries = 25 declared + 6 neutral, matching the contract; `selftest/c2-selftest.stdout` `C2_R46_SELFTEST: cases=8 failed=0` exit 0; `after/extra-receipts.stdout` ends `EXTRA_RECEIPTS_BAD=0` with a first `FAIL <rule case>` for each killed mutant (I read the coverage C08–C10 lines). The target (≥23 of 25, none of 6 neutral) is met with margin. Honest limits the lane already discloses and I confirm as limits, not harm: 73 fresh wave-2 mutants → 17 killed (the additions pin the declared rules and little more); the operative round-45 counters are untouched (credit sits on the hardened copies); `equivalence` masks `self_pin` and the PASS token (compensated by the supplementary unmasked receipt). The 0 → 10 operability score is definitional; the comparable measure is `killed 0 → 25 of 25`. Ruling: operability **improved**.

### C3 coverage (frontier F3, sourced, assimilation): re-measured

Committed deciding line (`after/c3.stdout`): `rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 … C3_R46_PASS=true`; before `rows=0 entries=0`.

My re-derivation:
- `grep -cE '^ {0,3}\| S[0-9]{3,} \|' corpus/SOURCES.md` → `120`; at base (`git show 683eedde:corpus/SOURCES.md`) → `117`. `git diff` of SOURCES.md is 7 insertions, 0 deletions (3 rows + round paragraph).
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit `0`, 11 W04/W01 warnings (same set as start receipt), zero E codes.
- Snapshots: `sha256sum` of the three files under `.ufo/evidence/round-46/coverage/sources/` equal the 8-hex prefixes in the rows and the full digests in the lesson (28d2954d…, 5eb59adf…, 434d8658…).
- Each of the three entries has `source: S258|S259|S260`, `verified-at: 2026-10-25`, a `recheck:` command, and a `corpus/README.md` index line (lines 573-575).
- Quote location, independent script over the committed snapshots: every double-quoted source sentence of r9 (21 of 21) located; r6 15 of 18 and r5 13 of 18 located, the remainder being lane-side wording (frontier move text, “open access per the institutional record”), not source quotes.
- Expansion ground: `git show 683eedde:corpus/README.md | grep -ci 'co-occur\|undetected flaky\|cluster'` → `0`, so clustering and same-job-rerun blindness were unheld; the lane correctly denies expansion credit to the third entry (S260 restates a held claim, `repeated-control-precondition.md:20`, through a byte-stable carrier).
- Selftest tally: `selftest/c3-selftest.stdout` `C3_R46_SELFTEST: cases=24 failed=0`.

Ruling: coverage **improved** (2 of 3 entries on unheld ground; the third is a pinned second carrier).

### No-harm

`after/no-harm.stdout`: all six monitors `ok` (command D 9, coldread 6 with `box3_full_page=False`, r45 freshness fresh=71, r45 coverage rows=2 entries=2, S160 count 1, registry rows 120 ≥ 117); `after/coldread-sections.stdout` `COLDREAD_SECTIONS_CREDITED=60 (base 60)`; `git diff --stat 683eedde b5425635 -- PROVINCE.md SKILL.md SHONEN.md` → empty (the PROVINCE append was reverted to base bytes); `after/census.exit` `0`. SCORECARD only appended.

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 total 21 → 0 re-derived from sha pins and append-only diff; monitor 6 → 6, no raise claimed |
| operability | improved | C2 killed 0 → 25 of 25, neutral 0, evidence-verified; limit: 17 of 73 fresh mutants killed |
| coverage | improved | C3 rows 117 → 120, 3 entries indexed, re-measured |
| depth | unchanged | command D 9 → 9 |
| freshness | unchanged | fresh 71, score 9 → 9 |
| adjacency | unchanged | no sibling-owned ground touched; misroot sweep listed and left alone |

No axis harmed. Claims re-measured: C3 fully; C1 inputs (sha pins, row counts, append-only, frozen paths). Evidence-verified only (counter not executed): C1 counter verdict, C2 verdict.

## Discernment spot-check

| Item | Decision | Re-opened source | agree/disagree | Reason |
|---|---|---|---|---|
| S258 Systemic Flakiness (arXiv 2504.16777) | admit | live `curl -sL https://arxiv.org/abs/2504.16777` (43,376 bytes, equals snapshot size); quote search | agree | the 22-token quote “finding that 75% of flaky tests … mean cluster size of 13.5 flaky tests” appears exactly once live and once in the snapshot; unheld ground at base |
| S259 TUM portal record (TSE 2026) | admit | live portal URL (51,588 bytes; text equal to snapshot, bytes differ at char 4429) | agree | abstract sentence present with en dash `9.8 %–16.3 %`; the lane's fold and BibTeX-escape caveat is disclosed in the entry; quote is 18 tokens |
| S260 Google per-post feed | admit as second pinned carrier, no expansion credit | live feed `sha256sum` → `434d86586ecf…` byte-identical to snapshot; 15-token quote located once in `entry.content.$t` | agree | honest handling: the claim was already held (S026), the lane says so and withholds expansion credit |
| Reject (c): r9's rerun-price arithmetic ($5.67, 0.02 cents, floor “S156”) | reject from the re-grounded entry | `grep -rn '5\.67' corpus/SOURCES.md corpus/knowledge` in the lane → no hits; `grep -rn '5\.67' /home/vgpnk/Projects/shokuknow/merge/tameshi` → only the package copies and S207 text | agree | no held, opened row states the figure; the flip condition (a held row carrying it) is stated |
| Reject (a): r6's “S140 round 5” cross-reference | reject from the re-grounded entry | `grep -cE '^ {0,3}\| S140 ' corpus/SOURCES.md` → `0`; package `r6-flaky-failures-cluster.md:29` cites S140 | agree | S140 names no lane row; the claim was re-anchored to S259 |
| New row S258 (`corpus/SOURCES.md:133`) | row fields (the registry row carries a learned-summary cell, not a verbatim quote; the ≤25-word quotes live in the entry) | snapshot `arxiv-2504.16777-abs.html` | agree | anchor sha256 prefix `28d2954d` equals the snapshot digest; the row's figures (75%, mean cluster size 13.5, 810 flaky tests, 10,000 test suite runs, 24 Java projects) each located in the snapshot text |

Result: the spot-check agrees with the gate on 3 admits and 2 rejects. The one wording nit (hyphen-folded dash in the lesson's S259 quote) is disclosed in the entry and does not change a decision.

## Trend verdicts

- **expansion: improved** — two admitted entries on ground the base coverage map did not hold (README had 0 mentions of clustering/undetected flaky failures), each citing a newly opened, snapshot-pinned row.
- **quality: improved** — 22 standing statements re-verified against their frozen commands (value, exit, tool sha) with a stale calibration value (8 → 6) corrected, 25 declared survivors killed, and wave-2 corrected overreach in all three entries before landing. Limit: fresh-mutant generalization is poor (17 of 73); no admitted entry failed its re-check.
- **discernment: improved** — the outside spot-check agrees with the gate on admits and rejects, and the round-45 routed defects became grounded criteria: defect 1 (no-harm monitor false red) → QUALITY 88 and `no-harm-gate.py`; defect 2 (selftest receipts) → `selftest/c{1,2,3}-selftest.stdout` committed; defect 3 (definitional score jump) → the count named as the comparable measure; the seat-name collision became QUALITY 90 with a gate. (The lane graded itself `unprovable-but-better` pending this check; this spot-check supplies the non-author evidence.)

## Routed defects for the lane next round

1. **Anchor refresh and per-snapshot fetch receipt** (round-45 routed defect 4 and Planned item) were not worked and stay open; pin S026/S093/S108 by quote, not whole-page hash.
2. **Hardened counters not operative.** Adopt them and absorb the wave-2 killing cases (17 of 73 fresh mutants killed); add an AST-pin control so a source-pinning selftest cannot score; count a mutant killed only when a named rule case fails.
3. **Host-dependent statements.** `retained invocation-context gate` (and two siblings) depend on the live fleet root and `jj`/`bwrap` on PATH; make the frozen observation hermetic and give the five tool-less statements a sha256 beside the statement.
4. **Lesson quote fidelity.** Print the S259 gate quote with the source's en dash, or state the fold at the quote, in the lesson itself.
5. SHONEN: all four boxes remain `[~]`; nothing is fully checkable by a non-author this round; promotion stays operator-owned.
