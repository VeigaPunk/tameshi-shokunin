seat: ExecRegressionClasses
item: Cumulative mismatch-class regression run (considerthese/2026-10-25.md proposal 2) — all four committed record-agreement counters re-run at base `683eedd`, every nonzero class classified as regression or by-construction false positive

# ExecRegressionClasses — cumulative mismatch-class regression run (round 46, wave 1)

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (read-only), base `683eedde3a50441c34d85a22f5fd5346f8b1ec6d`,
round-46 freeze `745a583181648cfc7f9c1b476cd1be7dc68f7433`. No lane file was written except this report; all scratch
under `/tmp/tameshi-r46-ExecRegressionClasses/`. No tool was installed or upgraded; no `pacman` call was made.

## Result in one line

At base, the four committed record-agreement counters exit **1, 0, 1, 1** with class totals **3, 0, 2, 2**; all five
nonzero class-hits are **by-construction false positives** of the older counters (three from the round-41 counter's
unbounded section plus its missing `staged:` mask, one external pinned hash, one round-bound newest-block check).
**No older class has regressed.**

## Commands run (lane path, exactly as the item names them)

All reads are `git -C LANE show <rev>:<path>` / `ls-tree` / `cat-file` at base; nothing was checked out, written or
staged in the lane.

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-42/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-43/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d --freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-44/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d --freeze ba01973c73ad7de60e5bd19ae08255a1b7ef917e
```

Final lines and exit codes (stdout verbatim; stderr empty on all four):

```
round-41  exit=1
MISMATCH m7 S202 cited but absent from the registry
MISMATCH m7 S203 cited but absent from the registry
MISMATCH m7 S204 cited but absent from the registry
C1_R41: m6=0 m7=3 m8=0 m9=0 total=3 records=3 sources_rows=117 rev=683eedde3a50441c34d85a22f5fd5346f8b1ec6d C1_R41_PASS=false

round-42  exit=0
C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=0 m11=0 total=0 records=6 sources_rows=117 rev=683eedde3a50441c34d85a22f5fd5346f8b1ec6d freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f C1_R42_PASS=true

round-43  exit=1
C2_R43: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=1 m12=1 m13=0 total=2 records=4 sources_rows=117 standing=117 receipts=17 revisions=4 m13_probe=standing=9_column0=116_valid=117 rev=683eedde3a50441c34d85a22f5fd5346f8b1ec6d freeze=6b83a11c61f0fad1074ec1f2a4c38a2fd7034685 C2_R43_PASS=false first=m11:SCORECARD.md#round-45:cd8e73f067129f8489e35c7b51c7a68552b289d2

round-44  exit=1
C2_R44: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=1 m12=1 m13=0 total=2 records=4 sources_rows=117 standing=117 receipts=17 revisions=4 m13_probe=standing=9_column0=116_valid=117 rev=683eedde3a50441c34d85a22f5fd5346f8b1ec6d freeze=ba01973c73ad7de60e5bd19ae08255a1b7ef917e C2_R44_PASS=false first=m11:SCORECARD.md#round-45:cd8e73f067129f8489e35c7b51c7a68552b289d2
```

Repeated from a scratch clone (`git clone -q --no-hardlinks LANE /tmp/tameshi-r46-ExecRegressionClasses/clone`;
`git -C clone checkout -q --detach 683eedd`, `rev-parse HEAD` = `683eedd…`) the four final lines are **byte-identical**
(`diff` of each stdout: identical; exit codes 1, 0, 1, 1). So the result is a property of the base revision, not of the
lane's working tree.

Freeze revisions used, and where each is named:

| round | `--freeze` | provenance |
|---|---|---|
| 41 | (none; counter takes `--lane --rev` only) | `.ufo/evidence/round-41/calibration/measure.py` argparse |
| 42 | `322b5cd32b4319a05340d249ae752d12a9e6b19f` | `git log -1`: "round-42: freeze contract and counters (C1 calibration, C2 depth) before any seat"; recorded as `freeze=` in `round-42/before/c1-at-base.stdout` and `round-42/after/c1-at-242c1b4a.stdout` |
| 43 | `6b83a11c61f0fad1074ec1f2a4c38a2fd7034685` | `round-43/contract.json` `frozen_before`: "the freeze of record is 6b83a11c…, reached through the amendment chain A1-A14" |
| 44 | `ba01973c73ad7de60e5bd19ae08255a1b7ef917e` | item; also `round-44/before/c2-new-at-base.stdout` and `round-44/after/c1-at-ef990aa.stdout` `freeze=` |

All four freeze revs are ancestors of base (`git merge-base --is-ancestor <rev> 683eedd` → 0).

## Class × round → hits (hits = length of the class's mismatch list, as printed)

| class | r41 | r42 | r43 | r44 |
|---|---|---|---|---|
| m6 (standing registry row count vs registry) | 0 | 0 | 0 | 0 |
| m7 (cited S-id absent/unmined) | **3** | 0 | 0 | 0 |
| m8 (cited path does not resolve) | 0 | 0 | 0 | 0 |
| m9 (round-40 quarantine summary vs its table) | 0 | — | — | — |
| m10 (receipt `present` vs tree) | — | 0 | 0 | 0 |
| m11 (cited 40-hex not an object) | — | 0 | **1** | **1** |
| m12 (newest block vs contract round / `Planned`) | — | — | **1** | **1** |
| m13 (standing command census-valid) | — | — | 0 | 0 |
| **total** | **3** | **0** | **2** | **2** |
| **exit** | **1** | **0** | **1** | **1** |

(`—` = class not declared by that counter. m9 is declared only in round 41; m12/m13 only from round 43 on; m10/m11 from
round 42 on.)

## Classification of every nonzero class-hit

### 1. round-41 `m7=3` (`S202`, `S203`, `S204`) — by-construction false positive (superseded extractor, two defects)

- The tokens are **not** in the round-41 record. The round-41 counter's `section()` is `text.find(head)` and returns
  `text[idx:]` (`.ufo/evidence/round-41/calibration/measure.py:120-126`), so its "`## 2026-10-25 — round 41` LOG
  section" is the LOG from line 2092 **to EOF** — 212 lines at base. The properly bounded section (round-42 rule, cut at
  the next `##` heading, LOG line 2168) is 76 lines. The three citations sit at LOG lines **2278, 2291, 2294**, inside
  the **round-45** entry whose heading is LOG line 2274:
  `staged GoogleTest upstream documents (`staged:S202`, `staged:S203`, `staged:S204`)`, `Rows S256/S257 adopted by
  document from `staged:S202` and `staged:S203``, `the `staged:S204` generator-contract entry refused`.
- The round-41 rule also has no `staged:` mask: `S_CITE_RE = \bS(\d{3,})\b`. The round-42 counter fixed exactly this
  (`(?<!staged:)`, docstring: "`staged:S###` names a package id, not a registry citation"), and the round-42 Mistakes
  row `newline-spanning-extractor` records the extraction repair.
- The ids are package staged ids, not registry rows: `git show 683eedd:corpus/SOURCES.md | grep -cE '^\| *S20[234] *\|'`
  → **0**; `S256`/`S257` (the adopted rows) → **2**.
- Positive control that the *records* are not regressed: the round-42 counter, whose record set includes both round-41
  and round-42 records (`records=6`) and which carries the fixed extractor, prints `m7=0 total=0` at base.
- Round lesson cited: `corpus/lessons/round-42.md` Mistakes row `newline-spanning-extractor` (round-41 closure defect 1)
  and the round-42 counter docstring's m7 sentence; the bounded-section repair is proved by its own selftest case
  `T5_section_bounded`.

### 2. round-43 and round-44 `m11=1` (`SCORECARD.md#round-45:cd8e73f0…`) — by-construction false positive (external pinned hash)

- `cd8e73f067129f8489e35c7b51c7a68552b289d2` is the **upstream GoogleTest commit** the round-45 rows S256/S257 and the
  `r8-gtest-*` entries pin in their URLs (`corpus/knowledge/r8-gtest-order-and-seed.md:1,3`;
  `corpus/lessons/round-45.md:13`). `m11_revisions` accepts only objects present in the lane
  (`git -C LANE cat-file -e <token>`), and this token is not a lane object:
  `git cat-file -e cd8e73f0…^{commit}` → **rc 128**; in the fleet repo → **rc 128**.
- Of the four 40-hex tokens in the round-43/44 record set, the other three (`3310e7be…`, `5891bdb7…`, `f6a34f39…`)
  resolve in the lane (cat-file rc 0, ancestor of base rc 0); only the external pin is flagged.
- Round lesson cited: `corpus/lessons/round-45-verifier-spotcheck.md`, routed defect 1 — "m11 is the external GoogleTest
  hash `cd8e73f0…` (`git cat-file -e cd8e73f0…` in the lane → rc 1, i.e. not a lane object) … Fix the counter (exempt
  pinned external hashes and be round-parametric)".

### 3. round-43 and round-44 `m12=1` (`newest block is round 45, the contract round is 43` / `… is 44`) — by-construction false positive (round-bound check)

- m12 audits the **newest** `## Round N` SCORECARD block against `contract["round"]`. At base the newest block is
  `## Round 45 — held-row live re-verification (freshness) + GoogleTest F3 adoption` (SCORECARD.md:2148), so the
  comparison `round_no != contract.get('round')` is false by definition at any later revision; the counter appends
  `BLOCK_ROUND_MISMATCH` to the block and adds the message. Enumerated with the counter's own helpers: the only m12 hit
  is the round mismatch (no missing `**Planned (round N+1):**` hit).
- Same round-boundness makes the record set shift: both counters read `corpus/lessons/round-42.md`,
  `corpus/lessons/round-43.md`, the newest block (**round 45** at base) and the LOG slice from `round 45` — the
  round-43/44 blocks are not in the audited set at base.
- Round lesson cited: same `round-45-verifier-spotcheck.md` defect 1 ("m12 is round-bound"), and the round-46 contract
  already records the consequence: "the round-44 record-agreement counter is **NOT** a monitor (red at base by
  construction, round-45 spot-check defect 1)".

## Answer: has any older class regressed?

**No.** Every class whose rule a past round fixed still counts zero at base, five rounds after the fix: m9 (the round-41
correction of the round-40 quarantine summary) is 0; m6 (the standing `sources-registry` row, 117 stated = 117 actual)
is 0 in all four counters; m8 and m10 are 0 everywhere; m7 is 0 in the round-42/43/44 counters; m13 is 0 in both
counters that declare it. The only nonzero hits are artifacts of pointing an old counter at a revision newer than the
round it was written for: the round-41 counter's unbounded `section()` plus its pre-`staged:` citation regex read the
round-45 LOG entry (3 hits), m11 flags a documented external pin that is not a lane object (1 hit per counter), and m12
compares the newest block to a frozen contract round (1 hit per counter). The round-42 counter — the only one of the
four with a bounded section, the `staged:` mask, and a record set that stays inside its own rounds — is green at base
(`total=0`, exit 0) while auditing both round-41 and round-42 records, which is the direct evidence that the records a
past round fixed were not silently undone.

## Cross-checks run (controls, not verdicts)

- `--selftest` on each counter: r41 → exit **2**, `usage: measure.py [-h] --lane LANE --rev REV` (that counter has no
  selftest); r42 → exit 0, `C1_R42_SELFTEST: cases=9 failed=0` (includes `T5_section_bounded OK`); r43 → exit 0,
  `C2_R43_SELFTEST: cases=12 failed=0` / `VERDICT: PASS`; r44 → exit 0, `C2_R44_SELFTEST: cases=16 failed=0` /
  `VERDICT: PASS`. So the three reds are not a broken binary and not a pin failure (`self_pin=1` on all three pinned
  counters).
- Each round's own deciding receipt is green, so the reds appear only at the later base, not at the measured revision:
  r41 `after/c1-at-baa18b7b.stdout` `total=0 C1_R41_PASS=true`; r42 `after/c1-at-242c1b4a.stdout`
  `total=0 C1_R42_PASS=true`; r43 `after/c2-at-3c4003f6.stdout` `total=0 C2_R43_PASS=true`; r44
  `after/c1-at-ef990aa.stdout` `total=0 C2_R44_PASS=true`.
- Lane untouched: at seat start `git status --porcelain` listed only `??` entries (other seats' wave files); after all
  runs `git status --porcelain | grep -v '^??' | wc -l` → 0 and `git diff --stat | wc -l` → 0;
  `find .ufo/evidence -newermt '-30 minutes' -type f` → nothing. The `__pycache__` dirs under
  `.ufo/evidence/round-4{1,2,3,4}/calibration/` pre-date this seat (mtimes 04:00–10:04) and are gitignored
  (`.gitignore:4:__pycache__/`).

## Evidence for the round's Mistakes row (round-bound no-harm monitor)

- The cumulative run is **safe as a regression probe only per class, not as a pass/fail**: at base it prints exit 1 for
  three of four counters for reasons that carry no information about the tree.
- Concretely, a standing cumulative monitor must (a) exclude/parameterize m12 (newest block vs contract round) and
  (b) exempt declared external pins in m11 (a 40-hex token that appears inside a URL/anchor and is documented as an
  upstream commit), and (c) not reuse the round-41 counter past round 41 — its `section()` is unbounded, so its
  "round-41 record" grows with every later round's LOG.
- The only committed record-agreement counter that is base-stable is the round-42 one (`total=0`, exit 0 at base). If
  the lane wants a no-harm monitor for older classes, that counter's rule set (bounded section + `staged:` mask +
  `(?<!staged:)` + explicit `records=6` gate) is the one that survives a later base unchanged.
- This seat did not change any counter; the three proposed repairs above are findings for the L1, not applied code.

## Out of scope (noted, not counted)

Round-46's own C1 (`SCORECARD.md` standing rows vs the statements' frozen commands) is this round's in-flight claim, not
a past class; its before-state is red by construction at the freeze (`before/c1-at-freeze.stdout`, `total=21`) and is the
L1's measurement, not a regression of an older class.

## Blockers / risks

- None blocking. Risks: the round-41 counter cannot be made green at base without editing a frozen counter (its own
  `section()` is the defect), so any future cumulative-run contract must state the exclusion rather than treat the red
  as a regression.
- Tooling: none installed, none upgraded, no `pacman` transaction.
