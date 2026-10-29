# tameshi round 57 — lesson (hyaku run 11, 2026-10-28)

**SKELETON (wave 1).** Every `<TBD:name>` is replaced from a committed receipt or a located source. No disposition or verdict below is a measured result until the deciding run says so.

L1 `TameshiR57`, attempt 1. Base `5e3569969b532310d2b8a3d130901757a3df356b`; contract `.ufo/evidence/round-57/contract.json` (base, claims, controls, `routed_defects_from_round_56`); freeze `<TBD:freeze sha>`; content commit C0 `<TBD:C0 sha>`; deciding revision `<TBD:REV sha>`. The round's two claims: **C1 calibration** — the routed-defect ledger covers the routed items of the round-50..56 closure spot-checks (`corpus/lessons/round-5{0..6}-verifier-spotcheck.md`); **C2 operability** — `tools/receipt-revision-gate.py` has executed registry rows, mutant kills and a SKILL-table code that is true.

## Gate (sources opened this round)

| S | URL | opened | quote (<=25 words, located) | verdict |
|---|---|---|---|---|
| S283 | `<TBD:URL of the source admitted for C1 or C2>` | `<TBD:date>` | `<TBD:located quote; section and line; word count>` | `<TBD:admit / mined — the claim it grounds, with the rule it supports>` |
| (no row) | `<TBD:rejected candidate URL>` | `<TBD:date>` | `<TBD:quote as opened, or the reason no quote exists>` | **reject before append** — `<TBD:why it cannot ground the rule>`. Flip: `<TBD:the lane condition that would admit it>` |

Candidate in scout review, not admitted and without a row: the GNU grep manual's "Exit Status" section (scout receipts `.ufo/waves/round-57/w1/T57W1ScoutSourceA-receipts/gnu-grep-manual.html`, headers `gnu-grep-manual.headers.txt`). It is a precedent for a 0/1/2 exit map, not a source for the lane's 0/2/3 map; whether it is admitted, and as what, is `<TBD:verdict from the L1's located re-open>`.

Snapshot and extraction receipts: `<TBD:paths under .ufo/evidence/round-57/assimilation/ with sha256>`. Census at round end: `<TBD:exit>`, `<TBD:row count>` rows (142 at start), `<TBD:warning classes>`; command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`.

Spot-check slot: `corpus/lessons/round-57-verifier-spotcheck.md` is written by the non-author closure, not by this round; `<TBD:closure verdict, or "not yet written">`.

considerthese mining: `considerthese/2026-10-28.md` proposal 3 (cold-read cost forecast at planning time: map each planned SKILL.md edit to the cold-read headings it touches and report the expected re-read debt) — mined as `<TBD:QUALITY criterion number and tool path if landed>`. Proposal 1 was mined in round 56 (QUALITY 107; the considerthese paragraph of `corpus/lessons/round-56.md` after `## Gate`); proposals 2, 4 and 5 remain unmined (at most one per round).

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| control design — a positive control read the round's own committed receipts (round-56 lesson, `## Attempt 4 — landing record and mistakes`, its first row) | `corpus/lessons/round-56.md` lines 276–289: C2 arm 5 read the round's committed `control/controls-{a,b}.stdout`, which cannot exist before the first controls run, so one generation can never print `CONTROLS_B: 2/2`; the bootstrap run printed `CTL_POS_c2 … own=own-receipts-missing total=1` and `CONTROLS_B: 1/2`. | This round's `controls.sh` (staged at `.ufo/waves/round-57/w1/T57W1ExecControls/stage/.ufo/evidence/round-57/controls.sh`, 151 lines): its header says "ONE GENERATION. Controls are RECOMPUTED, never READ" and cites the round-56 row; it refuses with `CTL_GENERATION_ERROR` (exit 2) when REV already carries a round-57 controls or `after/` receipt. | Every control is rebuilt from lane git objects in a fresh `git clone --shared` of BASE (with the instruments overlaid) or of REV; phase B scores `CTL_POS_c1` and `CTL_POS_c2` at REV, the revision they certify. **Shown able to fail:** the dry run at a scratch REV `a57cd566fa74` (`.ufo/waves/round-57/w1/T57W1ExecControls-receipts/dry-real-counters.stdout`) prints `CONTROLS_A: 8/8 as pre-registered` and `CONTROLS_B: 0/2` with `CTL_MISMATCH` on both positive lines, so the positive arms refuse when the counters are unmet. The specific mode this fix targets — a control that reads a committed receipt — is `<TBD:mutant run: controls.sh variant that reads a committed control receipt, and the line it prints>`; until that line exists this row claims the fix is recomputed by construction, not that it is demonstrated against the read mode. |
| `<TBD:class of the mined mistake this round>` | `<TBD:path and command output>` | `<TBD:the counter, gate or receipt that catches it, or "none — residual">` | `<TBD:fix, and the red-before that shows it can fail>` |

Candidate for the mined row, not yet confirmed (the L1 confirms or retracts it): the contract's `before` fields cite `.ufo/evidence/round-57/before/c1.stdout` and `before/c2.stdout`, but `.ufo/evidence/round-57/before/` is an empty directory at this draft. That is the round-56 landing class ("before-receipts cited while untracked", `corpus/lessons/round-56.md` `## Mistakes`) recurring unless C0 commits the before receipts so every before-pointer resolves at the commit that cites it.

## Round-56 dispositions

Source: `.ufo/evidence/round-57/contract.json`, `routed_defects_from_round_56`; the seven routes are the round-56 closure's `corpus/lessons/round-56-verifier-spotcheck.md` §6.

| id | what round 57 does | ledger row (`corpus/routed-defects.json`) | evidence |
|---|---|---|---|
| R56.1 | Not repaired this round. The SKILL page-local line anchors (57 of 61 distinct ranges stale; `corpus/lessons/round-56.md` `## Round-57 deferrals` F1) would cost a re-read of the eighteen headings in the round that must already re-read the SOURCES/QUALITY/README drift. The row records it open, with the cost forecast as evidence. | `open` (contract) | `<TBD:forecast receipt path, T57W1ExecForecast-receipts/…>` |
| R56.2 | Fixed by C2's standing-rules arm: the verdict-receipt-on-declared-surface cell of SKILL.md `## Standing rules` (base line 53, `RECEIPT_REV_MISMATCH`) is set to the code the gate emits, which the C2 counter reads from the gate on a fixture. | `<TBD:status>` | `<TBD:C2 standing_cell line; SKILL cell line after the edit>` |
| R56.3 | Fixed in C0: the recheck's 19/19 errata and the `corpus/README.md` index entry for `corpus/knowledge/receipt-revision-binding.md`. | `<TBD:status, expected fixed>` | `<TBD:C0 commit; errata path>` |
| R56.4 | Ledger row only. A referent record is written only if a wave-1 seat establishes the referents. | `<TBD:status>` | `<TBD:wave-1 seat receipt, or "no referent record">` |
| R56.5 | Fixed by C2's kill rule (the counter recomputes expected exits on counter-built fixtures and by `registry-check` on committed rows; it never reads a committed receipt), and the `controls.sh` header pre-registers the two control generations. | `<TBD:status>` | `.ufo/evidence/round-57/controls.sh` header; C2 kill_rule in the contract |
| R56.6 | Fixed by C2's gate rows: ≥ 3 active `gate` rows run `tools/receipt-revision-gate.py` on committed fixtures expecting exits 0, 2 and 3. | `<TBD:status>` | `<TBD:registry row names; registry-check --only line>` |
| R56.7 | Fixed in the report, not the lane: the round-57 wave report states the measured C2 line verbatim from the counter, and the `total=` value is quoted from its receipt. | `<TBD:status>` | `<TBD:report path, D-CF1-equivalent note>` |

Ledger ids for these seven are `R56.1` to `R56.7`; the round's frozen item set is `<TBD:N>` routed items, of which these seven are the last seven (the extractor takes them from the numbered list under `## 6. Verdict and routing`).
