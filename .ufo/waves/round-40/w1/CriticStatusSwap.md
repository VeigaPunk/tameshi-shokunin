# CriticStatusSwap — can a S108 status edit pass C2?

**Question:** does changing S108's status to `rejected` without committing a
snapshot satisfy C2_R40_PASS?

**Verdict: NO. The attack fails.** The predicate is conjunctive over the
snapshot blob itself; no status field is read anywhere in the counter.

## Where the status edit would land

S108's status is field 9 of `corpus/SOURCES.md:120` (currently `mined`; the
`queued|mined|rejected` enum is enforced by
`.ufo/evidence/kaika-round-1/sources-census-v2.sh:15`). A "reject S108" commit
touches only that cell.

## Why the counter cannot see it

`.ufo/evidence/round-40/s108/measure.py` reads exactly two paths at REV via
`git show` (measure.py:26-33):

- `:21` `SNAPSHOT = '.ufo/evidence/round-40/s108/golden_tests.zh-cn.html'` → `:55`
- `:22` `CONTRACT = '.ufo/evidence/round-40/contract.json'` → `:56` (supplies `pin` and `frozen_quote`, `:60-63`)

`corpus/SOURCES.md` is never opened. `ok` at `:81` requires
`present == 1 and sha_ok == 1 and stripped_fails == 1` — all three are computed
from the snapshot blob bytes (`:74-79`), not from any registry or status byte.

Two "status-only" shapes both fail:

1. **Rev without the snapshot blob** → `git show` fails, `blob is None` →
   `emit(..., False)` at `:66-73` with `snapshot_absent=1`.
2. **Rejected-marker text committed AT the snapshot path** (strongest
   substitute) → `sha_ok=0` (`:80`, sha256 pinned to
   `f27cf274…782bf0`), `quote_in_snapshot=0` → still `C2_R40_PASS=false`.
   The frozen sha admits exactly one blob; no alternate content can pass.

## Empirical control (scratch copy, base rev)

```
$ cp .ufo/evidence/round-40/s108/measure.py /tmp/tameshi-r40-CriticStatusSwap/
$ python3 /tmp/tameshi-r40-CriticStatusSwap/measure.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 304e3355705640af2879c772fc9a5c2902c61763
C2_R40: snapshot_absent=1 quote_in_snapshot=0 sha_ok=0 stripped_quote_fails=0 rev=304e33… C2_R40_PASS=false
EXIT=1
```

```
$ git -C …/tameshi-shokunin show 304e33…:.ufo/evidence/round-40/s108/golden_tests.zh-cn.html
fatal: path '.ufo/evidence/round-40/s108/golden_tests.zh-cn.html' exists on disk, but not in '304e33…'
```

Base stays `C2_R40_PASS=false` as required. The snapshot is committed in freeze
commit `5641ed8` (worktree clean for the s108 dir), so a status-only rev on top
of base lacking that blob fails identically.

## Residual observation (out of scope, flagged once)

`measure.py:56-64` re-reads `contract.json` at the candidate REV rather than the
frozen hash `5641ed84…`, so pin integrity rests on the L1 running the counter at
a rev whose contract equals the frozen bytes — not on the counter pinning it.
This does not weaken the verdict above: a status-only edit leaves the contract
untouched.

Scratch: `/tmp/tameshi-r40-CriticStatusSwap/` (lane checkout never written).
No tools installed; no pacman run.
