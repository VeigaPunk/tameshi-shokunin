# C1 before arm — monitor at the round-35 tip, ledger invisibility

## Attack
C1's before state: at pinned rev `796e08b888849308d0c4d5e932e56833600a139f` the cold-read monitor must still print `calibration_restraint_score: 6` / `sections_covered 60/64` **even though** the checkout's ledger has since grown to the refresh state, and the four refresh entries must be invisible at that rev. Probe run in a scratch clone whose worktree ledger is the grown HEAD state, plus a detached worktree at the tested rev.

## Setup (scratch, disposable except as noted)
```sh
mkdir -p /fast/scratch/hyaku/tameshi-r36-seats/W2MTMonitorBeforeArm
git clone --quiet --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r36-seats/W2MTMonitorBeforeArm/repo
```
Observed clone HEAD `fbb01cf46f8437fd1264c1a3acc053c882fa2164`; worktree ledger `.ufo/evidence/round-21/coldread/ledger.json` = 497 entries, sha256 `29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf` (identical to the lane worktree file). Detached control worktree:
```sh
git -C .../repo worktree add --quiet --detach .../wt-796e08b 796e08b
```
→ checked-out ledger at that rev has 493 entries.

## Measurements (all exit 0)
Monitor invocation shape (same as the claim, `--repo` redirected to scratch):
```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py \
  --repo /fast/scratch/hyaku/tameshi-r36-seats/W2MTMonitorBeforeArm/repo --rev 796e08b
```
| Arm | rev | score | covered | ledger_source | capture sha256 |
|---|---|---|---|---|---|
| clone, worktree ledger=497 | `796e08b` (short) | **6** | 60/64 | `rev`, ledger_committed=true | `976cc0cf0c6b57fdcfd7f76308823447d203bd8d22112f671360d4e72cf61ffa` |
| detached worktree at rev (ledger=493) | `796e08b` | **6** | 60/64 | `rev` | `976cc0cf…` (byte-identical) |
| lane, exact claim command | `796e08b8888…a139f` | **6** | 60/64 | `rev` | `7685a1306b06acd7dea541a39d7a6fa60248a35fe94a215c26449a9ff0e3069c` |
| rev-mutation (detector sensitivity) | `b455001` | **8** | 64/64 | `rev` | `after-b455001.json` |

The lane run is **byte-identical** to the committed receipt `.ufo/evidence/round-36/after/monitor-at-796e08b.stdout` (same sha256 `7685a130…`); its exit receipt `EXIT=0` matches `monitor-at-796e08b.exit`. The only structural difference between the scratch clone capture and the lane capture is the echoed `/rev_input` (short vs 40-hex rev) — one differing leaf in a full JSON leaf-diff.

Reported `revision` is `796e08b888849308d0c4d5e932e56833600a139f` in every before arm, so the read is rev-addressed, not worktree-addressed.

## Refresh invisibility at `796e08b`
```sh
git show 796e08b:.ufo/evidence/round-21/coldread/ledger.json | python3 -c "...len(d['entries'])"
git show b455001:.ufo/evidence/round-21/coldread/ledger.json | python3 -c "...len(d['entries'])"
```
- `796e08b`: 493 entries, 3,633,498 bytes, blob sha256 `fc16d21a602ee6e8bc9d069cd0da6e3e26d4805cbb11b9e030a19deb4c9b5cd7`.
- `b455001`: 497 entries, 3,489,570 bytes, sha256 `29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf` (= HEAD/worktree bytes).
- Entries with `read_rev=e423c41ba253…`: **0** at `796e08b`, **4** at `b455001`.
- `.ufo/evidence/round-36/coldread/traces/L1/source-{1..4}.json`: **ABSENT** at `796e08b` (git cat-file -e).
- Canonical entry-multiset diff (sort_keys JSON, Counter difference) of the two ledgers: **0 dropped/changed, 4 added** — exactly starts 131, 375, 1380, 1436 (`record`, `gap-minor`, 1 trace each).
- `git diff --name-only e423c41 b455001`: ledger + `round-36/coldread/{affected-sections,refresh-receipts,refresh-specs}.json` + the four traces only — no SKILL, monitor, or tool change, consistent with C1's kill rule.
- The four sections uncovered at `796e08b` are precisely 131 / 375 / 1380 / 1436, all failing on `input-drift:*` with `vetoed=false`; at `b455001` uncovered = 0.

## Mutation probe (invariant: pinned-rev read is isolated from worktree drift)
- Mutant: emptied the clone worktree ledger's `entries` (497 → 0). Pre-mutation sha256 `29bddc03…`, mutant sha256 `11f6e3bce2ba264fd6a99134480cf6eb2f7815f8ba84337183877bc5d882f423`.
- Same detector, same rev `796e08b`: exit 0, score **6**, 60/64, output sha256 `976cc0cf…` — **byte-identical** to the pristine capture.
- Verdict: **SURVIVED by design** — the worktree ledger is not an input at a pinned rev (`ledger_source: rev`); the before score does not depend on ledger growth. Not a claim defect.
- Restoration: `git -C .../repo checkout -- .ufo/evidence/round-21/coldread/ledger.json` → sha256 `29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf`, equal to `git cat-file blob HEAD:…`; `git status --porcelain` empty.
- Complementary mutant (rev argument → `b455001`): score flips to 8 / 64/64, so the 6 is not a constant — the detector is rev-sensitive.

## Calibration finding: dispatch counts are off by four
The dispatch states "796e08b ledger has 489 entries, refresh commit 493". Both numbers are wrong by +4 relative to reality: the tested rev has **493**, the refresh commit has **497**. The error is the refresh delta applied to the wrong base (493−4=489 used as "before"; the pre-refresh blob already has 493). The delta itself (+4) and the invisibility conclusion are unaffected. In-lane corroboration: append commit `4b529ee` records "480 -> 493", sibling `w1/ScoutSHONEN.md` records "`796e08b`=493 → `b455001`=497 (+4)", and `contract.json` states revs and scores but no entry counts. No lane file states 489.

## Scoped notes
No pacman, no tool installs, no subagents. Read-only against the lane (`git show`, `git cat-file`, one monitor run whose only writes are to `/tmp`-free in-memory reads; no `__pycache__` newer than 2026-10-21 appeared under `.ufo/evidence/round-18|21`). Only lane write: this report. Captures retained in `/fast/scratch/hyaku/tameshi-r36-seats/W2MTMonitorBeforeArm/` (`before-796e08b.json`, `wt-before-796e08b.json`, `lane-before-796e08b.json`, `after-b455001.json`, `probe-empty-worktree-ledger.json`, `ledger-pristine.json`).

**VERDICT: AGREE** — the C1 before state reproduces exactly at `796e08b888849308d0c4d5e932e56833600a139f`: score 6, coverage 60/64, ledger_source `rev`, byte-identical to the committed before receipt even with a 497-entry worktree ledger; the four refresh entries and their trace receipts are absent at that rev (ledger 493 there vs 497 at `b455001`). Dispatch erratum: the count pair is 493→497, not 489→493.
