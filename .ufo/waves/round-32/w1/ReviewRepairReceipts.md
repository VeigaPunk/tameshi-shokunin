# ReviewRepairReceipts — round 32, wave 1 (reviewer seat)

Scope: verify the repair receipts the L1 committed at `c31814978969a41a8e9b0f7d99fa308c5993c1b7` — `.ufo/evidence/round-32/repair/c1monitor-at-r31-base-36c1d393.*`, `repair/commandD-at-r31-67c0e013.*`, `repair/commandD-at-r31-final-08125328.*`, and `before/*` — by re-running the round-27 monitor and command D at the same revisions in my own clone, byte-for-byte, plus the contract non-reconstruction check. Judged on calibration. Axes: calibration (primary), reproducibility (byte fidelity), contract fidelity.

**Verdict: every receipt VERIFIED; no defect found. The contract does not claim to reconstruct the missing round-31 exit — confirmed by wording and by repo ground truth.**

## Verdicts per receipt

| Receipt | Verdict | Rerun result |
|---|---|---|
| `repair/c1monitor-at-r31-base-36c1d393.{stdout,stderr,exit}` | VERIFIED | stdout byte-identical (`cmp -s`), stderr 0 B both sides, exit 0 = 0 |
| `repair/commandD-at-r31-67c0e013.{stdout,stderr,exit}` | VERIFIED | stdout byte-identical, stderr 0 B both sides, exit 0 = 0 |
| `repair/commandD-at-r31-final-08125328.{stdout,stderr,exit}` | VERIFIED | stdout byte-identical, stderr 0 B both sides, exit 0 = 0 |
| `before/c1-at-base.{stdout,stderr,exit}` | VERIFIED | stdout byte-identical (26 COPY lines + summary), stderr 0 B, exit 1 = 1 |
| `before/c1monitor-at-base.{stdout,stderr,exit}` | VERIFIED | stdout byte-identical, stderr 0 B, exit 0 = 0 |
| `before/commandD-at-base.{stdout,stderr,exit}` | VERIFIED | stdout byte-identical, stderr 0 B, exit 0 = 0 |
| `before/census-start.{stdout,exit}` | VERIFIED | stdout byte-identical (8 W04 duplicate-url warnings + ok line), exit 0 = 0 |
| `before/mutant-fidelity.txt` | VERIFIED | see fidelity section |

## Method

Sandbox clone `/fast/scratch/hyaku/tameshi-r32-seats/ReviewRepairReceipts/clone` at the receipt commit, `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset, no git write commands outside the clone, no `jj` anywhere. Long runs wrapped in `timeout`; no processes left running.

Revision resolution (`git rev-parse`): r31 base `36c1d3933f680125aeefc447f07db0f03004901a`, r31 measurement rev `67c0e01380a269650a8ff0d18c999bd0c71e130c`, r31 final receipts head `08125328f87df92d3f25d0034ee792253ecbcbd9`, r32 base `e24688b2ff6cca1c9ad20e112f02c629b8597ff8`. These match the receipt filename pins and the round-31 contract (`round-31/contract.json:5` base = `36c1d393…`) and after receipts (`after/c1-at-final.stdout:13` rev=`67c0e013…`).

Script-version ambiguity eliminated: `.ufo/evidence/round-27/c1-measure.py` (sha256 `6f95ef1d0624e4da…`) and `.ufo/evidence/round-21/coldread/measure.py` (sha256 `657f009bdf1cc89a…`) are byte-identical at all five revisions, so one copy is valid for every rerun. Each monitor rerun was executed from the clone checked out at the measured revision: `timeout 600 python3 .ufo/evidence/round-27/c1-measure.py --repo . --rev <REV>`.

Command D per `SCORECARD.md:72-73`, run from each receipt's revision:
`git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'` → `recorded_cases=9 depth_score=9` at `67c0e013…`, `08125328…`, and base.

Counter rerun (the `before/c1-at-base.*` receipts were produced at freeze time, since the counter does not exist at base): from a linked worktree at `c3181497…`,
`python3 .ufo/evidence/round-32/c1-measure.py --lane <worktree> --rev e24688b2… --work <empty scratch dir> --seed fc9d575ba0049e50`
→ exit 1, stdout byte-identical including the seeded generated-copy SHA-256 prefixes (e.g. `gT08(arm=200) sha256=d39eabe154fc20b7`, `gH05(drop=3,dup=4) sha256=2c3c436dca27a71b`) and the summary `C1_R32: kill=0/18 accept=0/8 other=26 runner_sha_ok=1 tool_present=0 seed=fc9d575ba0049e50 rev=e24688b2… C1_R32_PASS=false`. Seeded replay is deterministic: the copy set reproduced exactly.

Census rerun: `timeout 300 bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` (read-only validate mode) → exit 0, stdout byte-identical to `before/census-start.stdout`.

Byte comparison: `cmp -s` of my captured stdout against each committed receipt, all seven identical; exit codes equal in all seven; stderr empty on both sides wherever the receipt records one.

## Mutant fidelity (`before/mutant-fidelity.txt`)

- Pinned line `pinned runner sha256 a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` equals `git show <REV>:tools/mutate-and-run.sh | sha256sum` at all five revisions (full hash compared, not a prefix).
- All 9 values with a MutateHead counterpart equal the `Mutated SHA-256` column of `.ufo/waves/round-30/wC/MutateHead.md:233-250`: T07 `91066af8…`, T08 `12ad1d90…`, H03 `2ac4ce53…`, H04 `0dc1e6b0…`, H05 `adf6763d…`, N01 `c0a32ec4…`, N02 `31128639…`, N03 `741907e8…`, N05 `e1ef181c…`.
- `D01`, `B0-pristine`, `B2-reversed`, `B3-decoys`, `B4-cosmetic`, `B5-renamed` are disclosed as having no MutateHead counterpart — accurate against that file's row set.

## Contract does not reconstruct the missing round-31 exit — CONFIRMED

- Wording: `.ufo/evidence/round-32/contract.json`, `repairs.commandD_exit`: "the round-31 receipt after/commandD-at-final.stdout stays as written (its exit was not recorded and is not reconstructed)". No reconstruction is claimed anywhere in the repairs block.
- Ground truth: `.ufo/evidence/round-31/after/` contains `commandD-at-final.stdout` with **no** `.exit` sibling; `git log --oneline -- .ufo/evidence/round-31/after/commandD-at-final.stdout` shows exactly one commit, `0812532 round-31: final-head receipts…` — untouched through the freeze.
- The freeze commit is clean: `git diff --name-only e24688b2… c3181497… | grep -v '^\.ufo/evidence/round-32/'` → 0 files. The two command-D repair receipts are fresh runs at `67c0e013…` and `08125328…` recorded as new files under `round-32/repair/`, not edits of the round-31 receipt. Same-identity rerun of both reproduced byte-identical stdout and exit 0.
- Routing accuracy: `repairs.routed_by` cites `corpus/lessons/round-31-verifier-spotcheck.md` items 1, 2, 4. Item 1 (axis header must equal `Score (0–10)`) and item 2 (append-only = byte prefix) match the v2 counter's two stated changes (`repair/c1-r31-measure-v2.py` docstring, lines 5-8); item 4 ("commit a base monitor receipt…; give command D an [exit receipt]") matches `base_monitor_receipt` + `commandD_exit`. Round-31 `before/` indeed had no monitor or command-D receipts (only `c1-at-base.*`, `census-start.*`, `drift-sim.txt`, `prefreeze-format-recon.txt`), so the base monitor receipt is a disclosed gap-fill, not a silent backdate.
- No-harm at the freeze: `git diff --name-only e24688b2… c3181497… -- tools/` → 0 files; runner SHA pinned at all five revisions.

## Findings

No blocking or actionable defect. Two immaterial notes:

1. `before/census-start` has no `.stderr` file (the `repair/` receipts all carry one). My rerun's stderr was 0 bytes, so the gap cannot hide a warning. Cosmetic.
2. Command D stdout is insensitive to the revision here (the runner bytes are identical at `67c0e013…` and `08125328…`, same `recorded_cases=9 depth_score=9`), so the receipts' evidentiary value is the recorded exit codes, not stdout variance. Both exits reproduced as 0.

## Residual risk and verification gaps

- Byte-fidelity rests on the receipts' embedded revision pins; both receipt kinds pin theirs observably (monitor stdout embeds the full rev; counter stdout embeds rev and seed), and both matched.
- The counter rerun used `--jobs` default 4 because the receipt does not record the value; the COPY-line order nonetheless matched byte-for-byte, so no residual concern for this receipt.
- No tool installs or upgrades were performed; nothing to record under the tooling directive.
- Processes started by this seat: all terminated normally (background jobs `bg_6965`, `bg_7054` completed; no services; no kills needed).
