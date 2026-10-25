# Scout Receipt Sweep — round-42 w1 (tameshi)

Scope: every tracked JSON under `.ufo/` (4701 files) that asserts file presence or counts, checked
against the tree at `c77c2b7e64d2e356381441ecf94abac03e984606` (base rev). Read-only; no lane edits.

Method: (1) enumerate keys via regex (`present|exist|missing|count|member`, case-insensitive) across
all tracked JSON; (2) resolve each presence/count claim to a concrete repo path and test it with
`git -C <repo> cat-file -e c77c2b7e...:<path>` or `git ls-tree -r --name-only c77c2b7e...`;
(3) sweep every `report`/`reports` string value (1845 refs) for resolvability at base.

## Findings — disagreements (asserted vs observed at base rev)

### D1. `.ufo/waves/round-41/residual/receipt.json` — `seats.ResidualReceipts.present` (known C1 m10 live mismatch)
- Asserted: `present: false` for `report: ".ufo/waves/round-41/residual/ResidualReceipts.md"` (receipt line 14-17).
- Observed: `.ufo/waves/round-41/residual/ResidualReceipts.md` EXISTS at base
  (`git cat-file -e c77c2b7e...:.ufo/waves/round-41/residual/ResidualReceipts.md` → ok).
- The other 7 seats in the same receipt (`ResidualReplayC1/C2`, `ResidualScope`, `ResidualIds`,
  `ResidualCounts`, `ResidualAppendOnly`, `ResidualClaims`) assert `present: true` — all 7 files exist. Agree.
- `total_round_seats: 48` agrees: 40 round-41 w1 registry members + 8 residual seats = 48.

### D2. `.ufo/waves/round-20/outcomes.json` — seat `A01ProvRound19Ruler.report_exists` (NOT covered by C1)
- Asserted: `report_exists: false` for seat `A01ProvRound19Ruler` (status `completed`, line-seat object at `seats[0]`).
- Observed: `.ufo/waves/round-20/w1/A01ProvRound19Ruler.md` EXISTS at base.
- This file is the "Later-session snapshot, NOT original dispatch verdicts" (note at line 735); the
  original record `.ufo/waves/round-20/original-outcomes.json` has 0 mismatches vs base (all 72 seats
  match). Only this later snapshot disagrees.
- Count: 72 `report_exists` claims in `outcomes.json`; 71 agree, 1 disagrees (A01, false vs exists).

### D3. `.ufo/waves/round-40/settlement-receipt.json` — `reports_present: 64` (borderline count)
- All 64 seat-derived report paths `.ufo/waves/round-40/w1/<Name>.md` EXIST at base (64/64 seats ok;
  `registry_members: 64` also matches the 64 members in `.ufo/waves/round-40/w1/swarm-registry.json`).
- However the wave report dir contains 65 `.md` files at base: the extra is
  `.ufo/waves/round-40/w1/dispatch-outcome.md` (L1 dispatcher outcome memo, not a seat report).
- If "reports_present" means all `.md` files in the report dir, the asserted count 64 < observed 65.

## Verified agreements (no disagreement)

| Class | Evidence |
|---|---|
| `historical_digests.*.present=1` (16 claims, round-15 before/after/attempt-3) | all 4 paths exist: `.ufo/evidence/round-12/BashWitness/summary.json`, `.ufo/evidence/round-14/capture-context.py`, `.ufo/evidence/round-14/context-receipt.json`, `tools/mutate-and-run.sh` |
| round-41 settlement `registry_members=40`, `reports_present=40` | registry members at base = 40; seat reports = 40/40; `dead_seats=[]` |
| round-40 settlement `registry_members=64`, seat reports | registry = 64; seat reports = 64/64 |
| round-20 residual `count=4` | 4 seat reports all exist (`.ufo/waves/round-20/residual/Residual*.md`) |
| round-19 `completion1/2.json seats=64` | both w1/w2 swarm registries hold 64 members at base |
| round-37 contract/control `source_specimen_count=9` | `.ufo/evidence/round-35/c1/panel/` has exactly 9 files at base |
| `ledger_present` flags (37 claims, rounds 16-32 coldread monitors) | rounds 16-21 evidenced ledgers exist at base; round ≥25 monitors reference the round-16 ledger at rev `09ee1d09…` which exists at base |
| `report`/`reports` path references (1845) | 0 unresolved at base |
| coldread `missing` lists (39) | bookkeeping of headings/reasons, not file lists (no file paths present) |

## Not tree-checkable / out-of-scope (noted, not counted as disagreement)
- `.ufo/evidence/round-21/c2-before.json`: `receipt_present=false`, `tool_selftest.present=false` — observational record at rev `08175c62d6…`, no path sibling; no tree claim.
- `poison_path_exists=false` (round-14/15 context receipts) — refers to external `/nonexistent/…` env path, intentionally absent.
- `taskKeyPresent` / `receiptPathPresent` (fleet-round-1 receipt-applicability) — authority manifest outside this lane (`.ufo/sighting/manifest.json` in ufo-fsd-alpha).
- `aliasExists=true` (fleet route-bindings) — config alias, not a repo file.
- `current_source_exists=false` (round-24 misroot-sweep) — fleet-side copied source removed; fleet-external.
- `scratch_exists_after_cleanup=false` (round-21 MB03.cleanup) — /tmp scratch; cleanup success claim.
- `members` dicts (117) — agent/session registries; the count-bearing wave registries (40/64) are verified above.
- `count` keys (9) — observation counts (callbacks/traces/observations); none are repo-file presence claims except round-20 outcomes `count` (covered above).

## What the C1 counter (m10) would miss
1. D2 — `report_exists` boolean in `.ufo/waves/round-20/outcomes.json` (A01ProvRound19Ruler: false vs file exists).
   m10 only audits `present=<bool>` pairs with `report`/`path`; `report_exists` is a different key.
2. D3 — the numeric `reports_present=64` claim (round-40 settlement) and any count-vs-dir mismatch;
   m10 audits per-path booleans, not counts.
3. Non-`.ufo/waves` presence claims (e.g., `historical_digests.*.present` under `.ufo/evidence/round-15/`)
   — all agree at base, so no missed disagreement there today, but the class is outside m10's scope.

## Commands used (representative)
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-files .ufo | grep 'json$'` → 4701 files.
- `git -C … cat-file -e c77c2b7e64d2e356381441ecf94abac03e984606:<path>` for each asserted path.
- `git -C … ls-tree -r --name-only c77c2b7e… -- .ufo/waves/round-40/w1` → 65 md (64 seat + dispatch-outcome.md).
- Python walker over all tracked JSON for key extraction (stdlib only; no tools installed).
