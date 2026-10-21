# A08 — QUALITY20 freeze ordering (contract.frozen_at ≤ contract commit ≤ wave-1 dispatch)

Seat: TameshiR20-3.A08FreezeOrdering · Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` · 2026-10-21
Scope: ordering of the three timestamps only. No lane file besides this report was written; all git commands read-only; no installs performed.

## Verdict

**HOLDS under the declared basis** (committer time `%cI` + recorded `wave1_dispatched_at`):

| Event | Artifact | Value (UTC-normalized) |
|---|---|---|
| frozen_at | committed `contract.json` @ 6fd220b | 2026-10-21T07:40:18Z |
| contract commit (committer) | `6fd220bce3705498d1d1054e99e3cae73c203751` | 2026-10-21T07:41:02Z (= 04:41:02−03:00) |
| wave-1 dispatch | `.ufo/waves/round-20/dispatch.json` | 2026-10-21T09:29:09.517Z |

- Leg 1: frozen_at ≤ commit — holds by **44 s**.
- Leg 2: commit ≤ wave-1 dispatch — holds by **1 h 48 m 07.5 s**.
- The contract's own `frozen_at` reads identically in working tree and committed bytes (both sha256 `9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715`); 6fd220b is the only commit touching `contract.json`, so the frozen contract was never re-frozen after commit.
- `dispatch.json` pins `frozen_contract_commit: 6fd220bce3705498d1d1054e99e3cae73c203751` — same identity, no rerouting.

## Commands and observed outputs

```
$ git log -1 --format=%cI 6fd220bce3705498d1d1054e99e3cae73c203751 -- .ufo/evidence/round-20/contract.json
2026-10-21T04:41:02-03:00

$ git show -s --format='full=%H%nauthor=%aI%ncommitter=%cI%nsubject=%s' 6fd220b…
full=6fd220bce3705498d1d1054e99e3cae73c203751
author=2026-10-21T04:30:45-03:00
committer=2026-10-21T04:41:02-03:00
subject=round-20: freeze QUALITY20 receipt-window contract and staged instruments (attempt 2)

$ git log --format='%h|%cI|%s' -- .ufo/evidence/round-20/contract.json
6fd220b|2026-10-21T04:41:02-03:00|round-20: freeze QUALITY20 receipt-window contract and staged instruments (attempt 2)   # sole commit

$ git show 6fd220b…:.ufo/evidence/round-20/contract.json | sha256sum
9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715
$ sha256sum .ufo/evidence/round-20/contract.json
9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715    # identical → committed bytes are the frozen bytes

$ git ls-files --error-unmatch .ufo/waves/round-20/dispatch.json
error: pathspec '.ufo/waves/round-20/dispatch.json' did not match any file(s) known to git
$ git status --porcelain -- .ufo/waves/round-20/dispatch.json
?? .ufo/waves/round-20/dispatch.json        # present, UNTRACKED
```

`contract.json` (committed @ 6fd220b): `"frozen_at": "2026-10-21T07:40:18Z"`, `"dispatch_artifact": ".ufo/waves/round-20/dispatch.json"`, baseline `c144dcd8…` — all match the frozen facts.

## What artifact proves the last leg

- **Current state:** the last leg rests on **uncommitted bytes** — `.ufo/waves/round-20/dispatch.json` field `wave1_dispatched_at: 2026-10-21T09:29:09.517Z`, self-described as a "post-acknowledgment registry assignment timestamp; **upper bound**, not exact task launch time; contract was committed before this coordinator activated".
- **Durable proof:** the future commit that adds `.ufo/waves/round-20/dispatch.json`. Once landed, `git log -1 --format=%cI -- .ufo/waves/round-20/dispatch.json` together with its committed `wave1_dispatched_at` and `frozen_contract_commit` fields gives a committed, tamper-evident leg-2 proof. Until that commit exists, leg 2 is backed only by mutable untracked bytes.
- A fortiori note: because `wave1_dispatched_at` is an upper bound (actual dispatch ≤ recorded), leg 2 as recorded (commit 07:41:02Z ≤ 09:29:09.517Z) holds robustly — the recorded value would have to overstate dispatch by >1 h 48 m to break it; the basis note additionally asserts activation-after-commit.

## Findings (by severity)

1. **MEDIUM — leg 2 not yet committed evidence.** `dispatch.json` is untracked (`??`). The C1 population item `contract_frozen_before_dispatch` is currently provable only from mutable uncommitted bytes. L1 must land `dispatch.json` in git (its own commit, or alongside final receipts) before C1 closes; I cannot commit (no git mutation).
2. **LOW — claim is basis-pinned to committer time.** Author time is 2026-10-21T07:30:45Z, i.e. **before** frozen_at by 9 m 33 s. Under an `%aI` basis leg 1 would fail. This is the expected shape (draft → stamp frozen_at → commit 44 s later), but every statement of the claim must keep `%cI` (the basis used by the contract's canonical command and this report). Any future text switching to author time silently breaks the claim.
3. **INFO — dispatch timestamp is coordinator-declared and an upper bound**, acknowledged inside the artifact itself. Not a defect; recorded here so downstream readers do not cite 09:29:09.517Z as exact seat-launch time.

## Agree/disagree

Agree with the contract's `contract_frozen_before_dispatch` ordering as recorded: `2026-10-21T07:40:18Z ≤ 2026-10-21T07:41:02Z ≤ 2026-10-21T09:29:09.517Z`. No disagreement with frozen facts I touched (contract sha path, baseline id, dispatch artifact path all match). I did not recompute instrument shas (A06/A07 seats) and express no view on them.

## Residual risk and verification gaps

- Leg-2 evidence is uncommitted until dispatch.json lands in git (gap closes automatically at that commit).
- The 09:29:09.517Z value derives from the w1 registry assignment clock; I did not audit `w1/swarm-registry.json` acknowledgment rows (out of my slice; F01/sibling seats own receipts).
- Author-vs-committer divergence (9 m 33 s) is real and unexplained in the contract; harmless under `%cI` but worth a one-line basis note if the contract text is ever restated (I made no lane edits).
