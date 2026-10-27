# Round 45 verifier spot-check

author: hyaku closure (non-author integrator, @m_sonnet)
date: 2026-10-25
lane HEAD measured: `85504972f2c35d4ef7b3de67bc1f624661bcbd04` (base `5891bdb77aba8489683533ae4cdd3b49b5e2626b`)
driver lines (`.ufo/watchdog.log`): `2026-10-25T16:08:30-03:00 launch tameshi round=45 pgid=2141782 driver=hyaku-inline attempt=1`; `2026-10-25T17:41:37-03:00 complete tameshi round=45; hyaku-inline attempt=1`

## Step-1 conformance

| Check | Command | Observed |
|---|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-45/tameshi.md` (fleet repo) | `tameshi-shokunin 8b3d7bb61cd0bd20171e3ad6feb4e5316104f883` |
| SHONEN heading, one line per box | read report | 4 `[~]` lines under `## SHONEN`, each with a prior pointer; none `[x]` |
| Cited commits are ancestors of `master` | `git merge-base --is-ancestor <h> master` for the 8 cited hashes (3310e7be, fd2610fd, 3bf8bcd3, ad5942c6, 1f9266ac, f6a34f39, ea25e022, 85504972) | all 8 `ok` |
| Lane pushed, clean | `jj-lane.sh state …/tameshi-shokunin`; `git status --porcelain` | `local=remote=85504972… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty (0 lines) |
| Criterion 86 receipts-only tail | `git diff --name-only ea25e022 85504972 \| grep -vcE '^\.ufo/evidence/round-45/(after/\|census-end\.)'` | `0` |
| Prompt carries template contract | `grep -n '^## ' .ufo/prompts/tameshi-round-45.md` (fleet repo) | §1 mission/axes, §2 claims, §3 L2 floor, §4 report contract (SHONEN, hash citation), §5 commit/push scope + L0 side channel, §6 hyaku addendum (write scope at line 318); no missing item found |

Conformance defects (status-neutral): (a) the counters' selftest tallies (C1 19/19, C2 10/10) are reported but no standalone committed selftest stdout receipt exists under `.ufo/evidence/round-45/` — only wave reports (`.ufo/waves/round-45/w1/MutC1Counter.md`, `MutC2Counter.md`) show the selftest as detector, with 12 and 8 survivors; (b) one dead wave-2 seat (ScribeScorecard results-mapping collision) and duplicate Mut seats, both disclosed in the report.

## Per-claim re-check

Method note: C1 and C2 rest on lane-owned counters (`measure.py`). Per PROTOCOL §Gate standard (Closure consequence) I did not execute them; I verified their committed deciding stdout and revision, and re-measured the underlying facts with my own plain scripts over committed bytes.

### C1 — freshness (lowest non-retired axis): re-measured + evidence-verified

Committed deciding line (`.ufo/evidence/round-45/after/c1-at-content.stdout`, rev `ea25e022…`, exit 0): `population=73 entries=73 verified=73 disputed=2 fresh=71 score=9 target=50 C1_R45_PASS=true`. Base line (`before/c1-at-freeze.stdout`): `entries=0 fresh=0 score=0 C1_R45_PASS=false`.

My re-derivation:

- Population: `git show <rev>:corpus/SOURCES.md | awk` over rows `^ {0,3}\| S\d{3,} \|` with status `mined`, id ≤ 160, http(s) URL → **73 at base 5891bdb and 73 at 8550497** (matches `population=73`). Registry rows 115 → 117 (`grep -cE` same pattern at each rev).
- Ledger: `jq '.entries|length'` → 73 entries, 73 distinct ids; all `verdict: holds`, all `opened: 2026-10-25`; 73 gzip snapshots exist.
- Python over committed bytes: gunzip each snapshot and sha256 it → **0 of 73 mismatch `raw_sha256`**. Quote token length 6–25 → **0 outside range**. Independent extraction (strip script/style/tags, unescape, NFKC fold, whitespace) locates **73 of 73 quotes in their snapshot** (raw-whitespace match alone misses 46 because the snapshots are HTML; the extracted-text match is the counter's own rule).
- Reviews: `reviews.json` 73 reviews, one per id, **71 agree / 2 dispute (S048, S093)**; self-review count 0 (no reviewer equals the entry author).
- Live re-fetch by me of 11 rows (S001 S003 S026 S048 S070 S073 S077 S086 S093 S099 S108): 8 byte-identical sha256 to the committed snapshot; S026, S093, S108 differ in bytes (dynamic pages) — S026 and S108 quotes are still located live; S093's live page shows its quote is a markup fragment (`<option>--unshare-user-try</option> …`).
- Dispute rulings: S048 quote is "If a mutation was previously killed, but the class or killing test has changed" — I read the snapshot: it breaks mid-sentence before "then it is likely that…", so the antecedent alone does not state the row's scope; **agree with dispute**. S093 markup-only fragment, **agree with dispute**.
- Result: fresh 0 → 71 of 73 (target 50). The counter-reported score 9 comes from the lane's new rule `floor(10*71/73)`; it replaces the round-44 one-unit measure, so the 1→9 step is a definitional change and I rely on the 0→71 count, not the score. S160 monitor `grep -cE '^ {0,3}\| S160 '` stays 1.
- Caveat (lane-disclosed, I concur): the counter's per-row gate is forgeable offline (CritC1Control); freshness is decided by the wave-2 non-author re-fetch, which I spot re-fetched above.

**Verdict: improved (re-measured).**

### C2 — coverage: re-measured + evidence-verified

Committed deciding line (`after/c2-at-content.stdout`, rev `ea25e022…`, exit 0): `rows=2 entries=2 indexed=2 row_ids=S256,S257 C2_R45_PASS=true`; base `rows=0 entries=0` (`before/c2-at-freeze.stdout`).

- `grep -nE '^ {0,3}\| S25[67] \|' corpus/SOURCES.md` → lines 131 and 132, both `docs | A | … | mined | 2026-10-25 | 365d | used-by corpus/knowledge/r8-gtest-*.md`.
- `sha256sum` of the three committed snapshots: advanced `05546ed6db92…`, primer `03d756ab1152…`, testing `44c56c6198c6…` — equal to the hashes in the rows. `curl` of the three commit-pinned raw URLs at `cd8e73f0…` today gives the same three sha256 values (live bytes = snapshots).
- Both knowledge entries start with `source: S256`/`S257`, `verified-at: 2026-10-25`, `recheck:`; `corpus/README.md:562-563` index both; my scan of all quoted spans of 6–25 tokens in the two entries: every one located in its snapshot (0 not found).
- `scripts/sources-census.sh validate … tameshi` → exit 0, zero E codes, only the 10 W04/W01 warnings identical to the report's census (census start = end).

**Verdict: improved (re-measured).**

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| freshness (C1) | improved | fresh 0 → 71/73 live-verified, non-author wave-2 agree; independent re-fetch of 11 rows |
| coverage (C2) | improved | rows 0 → 2, entries 0 → 2, indexed 2/2; snapshots equal live pinned bytes |
| depth | unchanged | command D `recorded_cases=9 depth_score=9` at base and content revision (`before/commandD.stdout`, `after/commandD.stdout`) |
| calibration | unchanged | coldread monitor `calibration_restraint_score=6` at both ends; the contract's round-44 record-agreement monitor is red (see defects) but is a false positive by construction, not a regression of a fixed record |
| SCORECARD diff | no harm | `git diff 5891bdb 8550497 -- SCORECARD.md` is additions only (round-45 block, Planned round 46, registry row 117); no prior row edited |

No owned axis harmed. Both claims verify, so `admitted=true`.

## Discernment spot-check (LEARNING.md)

| Item | Decision | Re-opened source | agree/disagree | Reason |
|---|---|---|---|---|
| S256 `docs/advanced.md` | admit | snapshot lines 896, 1977, 1980 (`sed -n`), live pinned URL sha256 | agree | Quotes found verbatim at the cited lines; upstream text states test order undefined and shuffle/seed; live bytes equal snapshot; scope in row matches the document's claims |
| S257 `docs/primer.md` | admit | snapshot lines 251, 253; live pinned URL sha256 | agree | "GoogleTest always deletes a test fixture before it creates the next one." at 251; live = snapshot; row's "teaches" does not overreach |
| `r8-gtest-generator-contract.md` (staged S204) | reject | `shokuknow/merge/tameshi/knowledge/corpus/knowledge/r8-gtest-generator-contract.md:11` and `googletest-testing.md:100-113` | agree | Package entry says "five generators"; the upstream table lists six (Range, Values, ValuesIn, Bool, Combine, ConvertGenerator), all deterministic enumeration — not an F10 property-based generator contract |
| C1 dispute S048 | dispute | `S048.raw.gz` text around "has changed" | agree | Quote is truncated antecedent; consequent absent |
| C1 dispute S093 | dispute | live bwrap.xml fetch | agree | Quote is markup-only |
| `corpus/SOURCES.md` S256/S257 rows (new) | admitted | rows at lines 131–132; lesson/entry quotes 8/12/15 tokens | agree | Rows carry no inline quotes; each quote the lesson cites is ≤25 tokens (8, 12, 15) and found once in the snapshot |
| QUALITY 86 (drift check) / 87 (quote-label) | new criteria | `quality/c86-falsifier.stdout`, `c87-falsifier.stdout` (`…-FALSIFIER-OK`) | agree | Each cites a round-45 lesson/receipt; criterion 86 is applied this very round (0 non-receipt paths after C) |

## Trend verdicts

- **expansion: improved** — two admitted entries on F3 ground cite newly mined rows S256/S257, each indexed (counted above).
- **quality: improved** — 71 of 73 held external rows re-verified against live bytes with non-author agreement, 2 flagged disputed rather than left silent; no admitted entry fails its re-check.
- **discernment: improved** — my outside spot-check agrees with the gate on 2 admits and 1 reject, and on both C1 disputes; the one gate-side mistake (round-44 record-agreement counter chosen as no-harm monitor) was disclosed and mined into criteria 86/87 with lessons behind them. The lane's own `unchanged` claim was conservative; the LEARNING.md rule (spot-check agrees on admits *and* rejects) is met.

## Routed defects for the lane next round

1. **No-harm monitor false red.** `after/c-r44-at-content.stdout`: `m11=1 m12=1 total=2 C2_R44_PASS=false`. m11 is the external GoogleTest hash `cd8e73f0…` (`git cat-file -e cd8e73f0…` in the lane → rc 1, i.e. not a lane object); m12 is round-bound. Fix the counter (exempt pinned external hashes and be round-parametric) before it is named in another contract's `no_harm`.
2. **Selftest receipts.** Commit `--selftest` stdout (tally) for both `measure.py` counters; kill the 12 (C1) and 8 (C2) selftest survivors already routed in SCORECARD "Planned (round 46)".
3. **Freshness score definitional jump.** The score 1 → 9 changes the formula (`floor(10*fresh/73)` vs the one-document unit); cite the 0 → 71 count as the comparable measure and keep the old unit as monitor (already done).
4. **Anchor refresh.** Five anchor-refresh candidates in `.ufo/waves/round-45/w2/ConnDriftAnchors.md` stay open; S026/S093/S108 live bytes now differ from the snapshots (dynamic pages) — the next recheck should pin by quote, not by whole-page hash.

SHONEN boxes: all four remain `[~]` with prior pointers and no new independent verifier; nothing is newly checkable by a non-author this round.
