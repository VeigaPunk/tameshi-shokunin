# Round 46 lesson

author: tameshi L1 TameshiR46 (hyaku run 7, attempt 1); Gate drafted from wave-1 seats ScribeRows, ScribeEntryCluster, ScribeEntryUndetected, ScribeEntryFalseRed and RevProvince, verified and edited by the L1
date: 2026-10-25

## Gate

Theme: **flaky-failure evidence for the determinism precondition (F3)** — adopt three documents
from the read-only package `shokuknow/merge/tameshi` as new rows S258/S259/S260, each cited by a
re-grounded knowledge entry. This is the round's coverage move (C3, sourced, with assimilation).
The calibration move (C1, standing self-assessment) and the operability move (C2, selftest
hardening) add no row. The package theme is staged in `MERGE-REPORT.md` as round-5/6/9 entries;
the lane adopted the three whose documents it could open and quote this round.

Re-grounding rule (CORPUS rule 1): every quote below was located by this round's seats in the
snapshot this lane fetched on 2026-10-25 and committed, not taken from the campaign. Token counts
are whitespace tokens after the counter's `fold`, measured by script, not estimated.

### Admit — S258 (new row): *Systemic Flakiness* (Parry, Kapfhammer, Hilton, McMinn; arXiv 2504.16777)

- URL https://arxiv.org/abs/2504.16777; access date 2026-10-25; snapshot
  `.ufo/evidence/round-46/coverage/sources/arxiv-2504.16777-abs.html` (43,376 bytes), SHA-256
  `28d2954d22ea45af7bd0454f1a8b01bb5db40e8e5cc235eed176a1621aa26a14`. Registry row
  `corpus/SOURCES.md:133`; entry `corpus/knowledge/r6-flaky-failures-cluster.md` (staged S195).
- Located quote, 22 tokens, found once in the folded snapshot text: “finding that 75% of flaky tests
  across all projects belong to a cluster, with a mean cluster size of 13.5 flaky tests”.
- Decision: **admit**. PROVINCE fit (RevProvince, `w1/RevProvince.md`): craft, because it bears on
  how a repeated-control or survivor verdict may be counted. The package entry's `ground: F8` tag is
  not warranted as the primary ground (the abstract says nothing about test oracles); the re-grounded
  entry grounds F3 and labels the F8 link `Inference:`.

### Admit — S259 (new row): *An Empirical Study of Detected and Undetected Flaky Test Failures* (Leinen et al.; IEEE TSE 2026)

- URL https://portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures/
  (the DOI 10.1109/TSE.2026.3729363 returns HTTP 202 with an empty body; the institutional record
  carries the abstract); access date 2026-10-25; snapshot
  `.ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html` (51,850 bytes), SHA-256
  `5eb59adf099304a07059530b0857f7b517eaa72c832049f46952915a77e71a6f`. Row `corpus/SOURCES.md:134`;
  entry `corpus/knowledge/r5-undetected-flaky-failures.md` (staged S190).
- Located quote, 18 tokens (the abstract appears three times on the page, so the folded text holds
  the string three times): “We found that, across all projects, undetected flaky failures account
  for 9.8 %-16.3 % of failed pipeline runs.”
- Decision: **admit**. Craft: a rerun inside the same job is both the detection mechanism and its
  blind spot, which is the F3/F5 precondition for a determinism claim. The package entry wrote the
  figures with `**` emphasis inside the quotation marks, which the located-quote check cannot find;
  the re-grounded entry quotes bare text.

### Admit — S260 (new row): *Flaky Tests at Google and How We Mitigate Them* (Micco), per-post feed record

- URL https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json; access date
  2026-10-25; snapshot `.ufo/evidence/round-46/coverage/sources/google-flaky-feed-6277555988217606236.json`
  (8,353 bytes), SHA-256 `434d86586ecf3ea03f57d4342c6e8575576eef6a9fd452a5c0a9e67bd8889929`. Row
  `corpus/SOURCES.md:135`; entry `corpus/knowledge/r9-false-red-rate.md` (staged S216; S225, S229 and
  S235 carry the same feed document and are not adopted separately).
- Located quote, 15 tokens, found once: “about 84% of the transitions we observe from pass to fail
  involve a flaky test”.
- Decision: **admit as a carrier repair, with an honest expansion note.** The lane already holds the
  rendered post as S026 and states the 84% figure in `corpus/knowledge/repeated-control-precondition.md:20`
  (ScoutHeldSweep, `w1/ScoutHeldSweep.md`). The new row is the publisher's per-post record, whose body
  the lane's HTML extraction can read (the rendered page keeps it in a script template), so the claim
  becomes re-checkable by the counter. Two of the three entries are on unheld ground (clustering, the
  same-job-rerun blind spot); this one is not, and the round does not claim it as expansion.

### Ids, collisions and the guard receipts

Collision check in scratch before any append (the 0–3-space extractor of the assimilation contract):
`reg-ids` 117, `staged-ids` 103, `collisions` 8 (S153 S154 S155 S156 S157 S158 S159 S160; receipts
`.ufo/evidence/round-46/assimilation/{reg-ids,staged-ids,collisions}`). Guard proof: an indented
`  | S002 |` row is caught by the 0–3-space pattern and missed by the column-0 pattern
(`guard-proof-collisions`). Renumber map (`adoption-map.json`, verdict `admitted`,
`guard-map.json`): dedupe S153→S105, S154→S106, S159→S155, S160→S156; map-only moves
S155→S261, S156→S262, S157→S263, S158→S264 (not adopted; the ids stay unused in the registry);
adopted by document S195→S258, S190→S259, S216→S260. The ids S258–S264 in this map replace the
round-45 map-only targets S258–S261 for the same staged rows; nothing was appended under those.

### Refused / not adopted

- **Four package claims dropped from the re-grounded entries**, each with its flip condition
  (RevProvince flags 1–4): (a) r6's "S140, round 5: the same-job rerun misses 9.8 %–16.3 %" — S140 is a
  retired shokuknow id that names no lane row; flip: cite S259 (the entry now does). (b) r5's "round 1's
  `S107`" for the one-green-control verdict — lane S107 is the TensorFlow golden-tests row; flip: anchor to
  the F3 round-1 surface. (c) r9's rerun-price arithmetic (0.02 cents, $5.67, a detection floor "S156") —
  no held row states it (`grep -rn '5\.67'` over the lane finds only the package copy); flip: a held row
  carrying the figures. (d) the F8 ground tag on r6 — flip: a source that connects clusters to test oracles.
- **Package entry `flaky-aware-verdict-evidence.md` and its siblings `r8-flaky-cost-baseline.md`,
  `r8-flakiness-not-static.md`** are not adopted this round: their rows (staged S155, S158, S160, S206, S207)
  were not opened, and S158 is a PDF with no committed text snapshot. Reason: not re-grounded here, not a
  content refusal. Flip: open each source, commit a snapshot (`pdftotext` for the PDF), locate the quotes.

### Quarantine slice

`.ufo/evidence/round-46/assimilation/quarantine-slice`: 17 rows (14 payload-absent, 3 could-not-be-fetched),
identical to rounds 40 and 45; none is among the adopted documents (ScoutQuarantine, `w1/ScoutQuarantine.md`).
No row of the slice is appended and no new verdict is claimed; the round-40 verdicts stand (one adopted, six
refused, ten present-but-not-appended).

### considerthese

`considerthese/2026-10-25.md` proposal 2 (cumulative mismatch-class regression run) is mined: ExecRegressionClasses
(`w1/ExecRegressionClasses.md`) re-ran the four committed record-agreement counters at base `683eedde…`. Result:
class hits 3 / 0 / 2 / 2 for rounds 41 / 42 / 43 / 44 (exit 1, 0, 1, 1); all five hits are by-construction false
positives of older counters (the round-41 counter's unbounded section and missing `staged:` mask, an external
pinned GoogleTest hash, a round-bound newest-block check). **No older class has regressed.** The proposal lands as
this lesson table and as the round-46 standing-statement counter (C1); it adds no standing counter of its own.

### Hardening and standing results, for the closure's spot-check

At least one admit and one reject of this lesson for a non-author to re-open: admit S258 (snapshot line and quote
above); reject (c) above (grep the lane for `5.67`).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| no_harm monitor named in a frozen contract was never run at base | `corpus/lessons/round-45-verifier-spotcheck.md` routed defect 1; `.ufo/evidence/round-45/after/c-r44-at-content.stdout` (`C2_R44_PASS=false`); round-45 contract names the S160 count with no base receipt (ScoutMistakes) | none | QUALITY criterion 88; `quality/no-harm-gate.py`; `before/no-harm-at-base.stdout` all ok before the freeze. Able to fail: falsifier block 88 prints `RED r44-record-agreement`, exit 1 (`quality/c88-90-falsifiers.stdout`) |
| seat-name collision between concurrently running lanes | `.ufo/waves/round-46/w1-results.json`: `MutC1Counter` and `ScribeQuality` entries carry `.ufo/waves/round-55/w1/MutC1Counter.md` and `.ufo/waves/round-45/w2/ScribeQuality.md`; round 45 `ScribeScorecard` | none (round-45 Mistakes proposed a prefix, nothing enforced it) | QUALITY criterion 90; `quality/seat-name-check.py`; wave 2 names carry `T46`. Able to fail: falsifier block 90 refuses the wave-1 spec (`COLLISION MutC1Counter …`) |
| a counter pinned only to its own committed bytes passes after a one-line edit | `w1/CritC1Control.md` cheat Z (`total = 0 * (mism + unparsed + unobs)` printed `C1_R46_PASS=true` with 21 failing statements, real 22-statement run) | the round-44 `--freeze` pin that this round's counters did not carry | `deciding-run.sh` step 0: `git diff FREEZE REV` over the frozen counters, statements, manifest, snapshots, package copies and contract must be empty (`FROZEN_UNCHANGED=1`) and the counter sha256 is printed; wave-2 seat T46CritLanding re-attacks it |
| a no-harm script prints `RED` and exits 0 | `w1/ScoutMistakes.md` diagnostic (`no-harm.sh` at `5891bdb`: three `RED` lines, exit 0); the committed `no-harm.sh` is frozen | QUALITY 17 is adjacent, not on point | `deciding-run.sh` greps its output for `RED` and fails; `no-harm-gate.py` exits 1 on a red monitor |
| the round's own frozen counters have selftest gaps | `w1/MutC3Counter.md` (4 of 22 mutants survive: snapshot prefix, missing snapshot, `MIN_ROWS`, `MIN_ENTRIES`), `w1/MutDriver.md` (the driver's 8-case selftest leaves its predicate assembly untested), `w1/CritC3Control.md` (18 of 22 cheat variants pass the counter; the counter does not check the id, an upper bound on `verified-at`, or fresh-quote relevance) | criterion 89 covers the declared-survivor shape only | frozen, not edited (a rule changed after a seat scored is not the claim's rule); routed to round 47 with the killing cases attached in the seat reports; the controls CTL_E/F/G at the freeze exercise the driver's neutral, pristine and baseline rules |
| a score defined this round jumps from 0 to a high value | round-45 spot-check routed defect 3 (freshness 1 → 9 changed the formula) | none | C2 reports the count `killed=0 → 25 of 25` as the comparable measure; its `floor(10*killed/25)` score is a definitional new axis score and is cited only beside that count |

## Census and quarantine

Census at round start: `.ufo/evidence/round-46/census-start.stdout`, exit 0, 117 rows, 11 W04/W01 warnings (same set as
round 45). End: `.ufo/evidence/round-46/census-end.stdout` (recorded at the content revision).
