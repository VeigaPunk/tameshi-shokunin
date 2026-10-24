# W2RevengerReceiptOrder — commit order around the round-36 freeze

Seat: revenger, leaf (no subagents). Attack: commit order of the round-36 data receipts
relative to the content commit, reconstructed from executable git evidence only.
Read-only throughout: no mutating git/jj command, no edits to frozen artifacts, no tool
installs (none needed).

## What was attacked

Contract `round-36/contract.json` claims `frozen_before_any_data_run: true` and both claims'
kill rules rest on the receipts landing *after* the freeze. The claim under attack here:

1. The contract itself is committed in the **content commit** (not amended after data ran).
2. Every data receipt under `.ufo/evidence/round-36/after/` (13 files) and
   `.ufo/evidence/round-36/control/` (9 files) is committed in commits **descending from**
   (descendants of) the content commit.

## Method

`git log --format='%H %s' -- <path>` per file for all 22 receipts + contract, plus
`git merge-base --is-ancestor`, `git log --format='%H parents=%P'`, and
`git diff-tree --no-commit-id --name-only -r` for delta disjointness. Repo:
`/home/vgpnk/Projects/shokunin/tameshi-shokunin` (read-only invocations of git only).

## Reconstructed chain (log order = newest first; single-parent linear, no merges)

```
fbb01cf46f8437fd1264c1a3acc053c882fa2164  round-36 verifier spot-check (HEAD / lane tip)   ct 1792823668
   ↑ parent
d9c496b19371b779ce0eec6dfee1b049b27a3a2d  round-36: receipts — ALL 22 after/+control/ files ct 1792822905
   ↑ parent
b455001e2589b3f4f471d94a3de7e5e549b9f54c  round-36: cold-read refresh (ledger+traces)      ct 1792822569
   ↑ parent
e423c41ba253357ab8c8513f0376dad9d38ab248  round-36: content — frozen v2 counter + contract ct 1792822440
   ↑ parent
796e08b888849308d0c4d5e932e56833600a139f  round-35 verifier spot-check (C1 "before" rev)   ct 1792821040
```

## Evidence chain

- **Contract in the content commit itself.** `git log --format='%H %s' -- .ufo/evidence/round-36/contract.json`
  returns exactly one commit: `e423c41ba253357ab8c8513f0376dad9d38ab248` ("round-36: content — … frozen v2
  counter + contract, wave specs w1/w2 (validated)"). Neither the refresh commit (`b455001e`) nor the
  receipts commit (`d9c496b1`) touches it (`git diff-tree --no-commit-id --name-only -r <commit> --
  .ufo/evidence/round-36/contract.json` → empty for both).
- **All 22 receipts in one descendant commit.** Per-file `git log -- <file>` over all 13 `after/` and
  9 `control/` files returns exactly one commit each: `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`
  ("round-36: receipts — monitor before(796e08b)=6 / control(e423c41b)=6 / after(b455001e)=8 64-64, …").
- **Descent proven, not assumed.** `git merge-base --is-ancestor` exit 0 for
  `e423c41b → b455001e`, `e423c41b → d9c496b1`, `e423c41b → fbb01cf` (and `b455001e → d9c496b1`,
  `d9c496b1 → fbb01cf`, and `796e08b → e423c41b`). Parent line (`git log --format='%H parents=%P' -4`):
  `fbb01cf4^=d9c496b1`, `d9c496b1^=b455001e`, `b455001e^=e423c41b`, `e423c41b^=796e08b8` — a strict
  single-parent linear chain, so "descending" is topologically unambiguous. Commit times strictly
  increase: 1792822440 < 1792822569 < 1792822905 < 1792823668.
- **No receipts pre-committed at content.** `git diff-tree --no-commit-id --name-only -r e423c41b --
  .ufo/evidence/round-36/after .ufo/evidence/round-36/control` → empty. The content commit carries the
  contract and the frozen apparatus, zero data receipts.
- **Receipts commit is pure data.** `git diff-tree --no-commit-id --name-only -r d9c496b1` lists exactly
  the 22 `after/`+`control/` receipt files and nothing else — no contract, no counter, no monitor/rubric
  edits ride along with the data.
- **Corroboration — C1 kill_rule holds at the commit level.** Full delta
  `git diff-tree e423c41b b455001e` (content → refresh) is exactly:
  `.ufo/evidence/round-21/coldread/ledger.json`, `.ufo/evidence/round-36/coldread/{affected-sections,refresh-receipts,refresh-specs}.json`,
  and `.ufo/evidence/round-36/coldread/traces/L1/source-{1,2,3,4}.json` — only the refresh ledger entries
  and trace receipts, matching "the refresh ledger entries and trace receipts are the only delta between
  the control commit and the refresh commit".
- **Corroboration — C2 kill_rule holds.** `git log --format='%H %s' -- .ufo/evidence/round-36/c1/c1-measure-v2.py`
  returns exactly one commit: the content commit `e423c41b`. No counter edit after the freeze.
- **Before-receipts placement (observation, not divergence).** `after/monitor-at-796e08b.{exit,stderr,stdout}`
  are the *before* receipts (run at the pre-content rev `796e08b8`, per contract C1 `before.rev`), yet they
  are committed in the descendant receipts commit `d9c496b1` like every other receipt. File naming carries
  the producing rev; commit order still satisfies the frozen-before-data-run contract (runs precede commit;
  all data receipts land strictly after content).

## Divergences

None. Every expected ordering property is observed; no receipt or contract file has any commit outside
the chain above (no amendments, no rewrites — each file's history is exactly one commit).

Confidence: high (direct git object-database evidence; ancestry + parent chain + per-file single-commit
histories are mutually consistent).

## Verdict

VERDICT: CONFIRMED — contract committed only in the content commit `e423c41ba253357ab8c8513f0376dad9d38ab248`;
all 22 after/+control/ data receipts committed only in `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`, a strict
linear descendant (content → refresh `b455001e` → receipts `d9c496b1` → tip `fbb01cf4`); frozen-before-any-data-run
order holds at the commit level.
