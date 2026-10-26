# T48A2RevDecidingScript — review of `.ufo/evidence/round-48/deciding-run.sh` vs contract amendment 8

Seat: a2w1 reviewer (Godspeed axes: calibration, freshness — milestone: deciding script integrity).
Reviewed artifact: `.ufo/evidence/round-48/deciding-run.sh` at content revision `c7586b9a10effc63b4bd327f976edc094c1bdc17` (byte-identical to the copy frozen at `755298415f8c4eef3bed0c0d7625e2aacb03d6c2`; both are in the FROZEN set of the script itself, so this review applies to the file that will actually execute).
Contract: `.ufo/evidence/round-48/contract.json` sha256 `4fff75dbaac728992fa04ffd3ccfea6ace8ca80b944cc393b63c287fadc6d59e` (verified at REV; matches freeze-2.json record). Anchor text, amendment 8 (F6): *"…runs each claim counter once at the content revision, writes receipts under .ufo/evidence/round-48/after/, and recomputes FROZEN_UNCHANGED over both counters, statements.json, this contract and the C2 snapshots; the receipts land in a receipts-only commit."*

Method note: no LSP server/device is available in this seat's toolset for bash; all checks are exact `read`/`git` evidence, quoted verbatim. I am read-only on the lane; scratch was `/fast/scratch/hyaku/tameshi-r48/T48A2RevDecidingScript` (deleted before finish). No tools were installed or upgraded for this seat.

Line numbers below are `nl -ba` of deciding-run.sh: `FROZEN=` is line 22, the FROZEN_UNCHANGED branch line 23, COUNTER_SHA256 line 24, no-harm 25-28, coldread 29-31, C2 invocation line 32, census 33-34, census-end copies line 34, C1 invocation line 36.

---

## Findings by severity

### F1 — BLOCKER: at the contract-declared pair (FREEZE=`755298415f8c`, REV=`c7586b9a`), the script's own FROZEN_UNCHANGED check is guaranteed to fail, so `DECIDING_RUN_EXIT=1` regardless of the counters

- `FROZEN` (line 22) freezes `$E/control` **as a directory**. freeze-2.json pins only the two control **scripts** (`control/run-controls.py` `f5732f18…`, `control/c2-controls.py` `46b8c039…`), and those two files are unchanged `7552984..c7586b9a` (`git diff --name-only` over both = empty). But the four control **receipts** `c2-controls.{exit,meta,stderr,stdout}` were committed later, at the content revision itself:

```
$ git log --format='%h %s' --diff-filter=A -- .ufo/evidence/round-48/control/c2-controls.stdout
c7586b9 round-48: content revision (attempt 2) - …
```

- Reproducing the script's exact check (same pathset as line 22) at the declared pair:

```
$ git diff --quiet 755298415f8c c7586b9a10effc63b4bd327f976edc094c1bdc17 -- $FROZEN; echo $?
1                      # -> line 23 prints FROZEN_UNCHANGED=0 and sets rc=1
$ git diff --name-only 755298415f8c c7586b9a10effc63b4bd327f976edc094c1bdc17 -- $FROZEN
.ufo/evidence/round-48/control/c2-controls.exit
.ufo/evidence/round-48/control/c2-controls.meta
.ufo/evidence/round-48/control/c2-controls.stderr
.ufo/evidence/round-48/control/c2-controls.stdout
```

- Sweeping every commit of the round as candidate FREEZE shows the trip is structural, not incidental — only the content revision itself (vacuous self-diff) and the later wave-spec commit pass:

```
FREEZE=c7586b9a1 -> quiet-exit=0   # self-diff, attests nothing
FREEZE=17cc5ce14 -> quiet-exit=0   # wave-spec commit: FROZEN paths untouched after c7586b9a
FREEZE=41c1bc081 -> quiet-exit=1
FREEZE=50545328e -> quiet-exit=1
FREEZE=755298415 (declared) -> quiet-exit=1
```

- Consequence: invoked per its own usage comment (line 3: "FREEZE the counter-freeze commit (freeze step 2, … freeze-2.json)" — i.e. `755298415f8c`) the run prints `FROZEN_UNCHANGED=0`, appends the diff-stat, sets `rc=1` (line 23) and exits `DECIDING_RUN_EXIT=1` even if every counter and monitor is green — a false kill. Alternatively, to observe `FROZEN_UNCHANGED=1` the L1 must pass FREEZE=`c7586b9a`/`17cc5ce`, in which case line 23's printed `freeze=<sha>` attests "unchanged since the content rev / wave-spec commit", not "unchanged since the counter freeze" — the check the amendment names is not the check performed.
- Root cause is one token: `$E/control` (dir) where freeze-2.json's `controls` map pins two files. Note the receipts themselves are legitimate amendment-9 artifacts (`control/c2-controls.meta` line 1 records `scored_at_freeze_bytes=7552984` — the C2 control *was* scored at the freeze); committing them at `c7586b9` was legal, the dir-freeze is what converts them into a trip.
- **Empirical probe (observed, not a verdict):** the frozen script itself was executed once against a scratch shared-clone (`/fast/scratch/hyaku/tameshi-r48/T48A2RevDecidingScript/clone`, `git rev-parse --show-toplevel` verified equal to the clone, work dirs under the seat scratch via `HYAKU_SCRATCH`), args `LANE=<clone> REV=c7586b9a FREEZE=755298415f8c OUT=<clone>/.ufo/evidence/round-48/after`, killed after step 0 (no counter was scored by this seat). Observed verbatim from the probe's `frozen.stdout`:

```
FROZEN_UNCHANGED=0 freeze=755298415f8c4eef3bed0c0d7625e2aacb03d6c2 rev=c7586b9a10effc63b4bd327f976edc094c1bdc17
 .ufo/evidence/round-48/control/c2-controls.exit   |  1 +
 .ufo/evidence/round-48/control/c2-controls.meta   |  1 +
 .ufo/evidence/round-48/control/c2-controls.stderr |  0
 .ufo/evidence/round-48/control/c2-controls.stdout | 19 +++++++++++++++++++
 4 files changed, 21 insertions(+)
COUNTER_SHA256 calibration/measure.py 572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3
COUNTER_SHA256 freshness/measure.py faefe9b442741bcd7238ffe028841a0da7453c14c70f9f33afbd0f77be2df63f
```

  i.e. the failure mode of F1 reproduces byte-for-byte, and the probe's COUNTER_SHA256 lines independently confirm the freeze-2 counter hashes at REV. Probe scratch deleted at seat end; scratch residue on disk: none.

### F2 — HIGH: FROZEN list omits the C2 snapshots/receipts that amendment 8 and the script's own header claim it covers

- Amendment 8 requires FROZEN_UNCHANGED "over both counters, statements.json, this contract **and the C2 snapshots**"; the header comment (lines 4-6) says the same ("…the C2 snapshots and receipts…"). The list at line 22 contains neither `$E/freshness` nor `$E/freshness/sources`:

```
FROZEN="$E/contract.json $E/freeze-2.json $E/calibration/measure.py $E/freshness/measure.py
        $E/control $E/no-harm.sh $E/deciding-run.sh .ufo/evidence/round-47/calibration/statements.json
        tools .ufo/evidence/kaika-round-1 .ufo/evidence/round-15 .ufo/evidence/round-21
        .ufo/evidence/round-45 .ufo/evidence/round-46 .ufo/evidence/round-47"
```

- Demonstrated blind spot — all 8 C2 snapshot/receipt files differ between the declared pair and the script would print `FROZEN_UNCHANGED=1` through any such change:

```
$ git diff --name-only 755298415f8c c7586b9a10effc63b4bd327f976edc094c1bdc17 -- .ufo/evidence/round-48/freshness/sources
S026.html S026.receipt.json S048.html S048.receipt.json S093.receipt.json S093.xml S108.html S108.receipt.json  (all added)
```

- Recorded tension: the snapshots were themselves added *after* the freeze (commit `5054532`, "C2 records"), so a literal amendment-8 pathset would also trip at the declared pair — the amendment's letter is unsatisfiable at (7552984, c7586b9a). The script resolves this by silently dropping the paths rather than surfacing the contradiction. Either way, the `FROZEN_UNCHANGED=1` line cannot carry the meaning amendment 8 assigns it at the declared pair.

### F3 — MEDIUM: the receipts destination (`.ufo/evidence/round-48/after/`) is documented but never enforced

- Line 2-3 usage: "OUTDIR an existing directory inside LANE". Line 12 takes `OUT=$4`; the only validated argument is LANE absoluteness (line 13). There is no check that OUT exists, is absolute, is inside LANE, or equals `.ufo/evidence/round-48/after/`.
- With OUT missing, line 23's `tee "$OUT/frozen.stdout"` fails silently (`set -u` only, no `set -e`, unchecked pipeline exits), later greps on nonexistent receipts degrade (most gates do still fail closed, e.g. line 28's count check), and with a wrong-but-writable OUT the receipts land outside `after/` while the script exits 0 — amendment 8 violated with no signal from the script.
- Mitigation/observable: the real invocation is checkable post hoc in the receipts commit (section below, filled when it lands).

### PASS — each claim counter invoked exactly once at REV (amendment 8)

- C2: exactly one invocation, line 32 (`python3 "$E/freshness/measure.py" --lane … --rev …`). C1: exactly one invocation, line 36 (`python3 "$E/calibration/measure.py" … --work "$SCR/c1"`). No other call site for either counter exists in the script; line 24's `git show | sha256sum` is a hash, not an invocation.
- `no-harm.sh` (executed at lines 25-26; read in full, 22 lines, 8 monitors) invokes only `.ufo/evidence/round-{45,46,47,21}`/kaika counters and git greps — zero references to either round-48 counter. The line-28 count gate (`'^NOHARM .* ok$'` = 8) matches its 8 monitors.
- "A second deciding invocation of either counter at the content revision is a miss": statically satisfied within the script; the receipts commit will show one receipt set per counter (checked below when landed).

### PASS — work dir never under /tmp

- Line 17: `SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r48/deciding` — default outside /tmp; line 20 `mkdir -p "$SCR"; export TMPDIR="$SCR"` runs before any counter/no-harm execution.
- C1 gets `--work "$SCR/c1"` (line 36) and additionally refuses /tmp itself: calibration/measure.py:395-397 (`if under_tmp(work): … return 2`, selftest case `T63_work_under_tmp_refused` at :836). C2 scratch is `tempfile.mkdtemp()` honoring TMPDIR (freshness/measure.py:382, :662; census temp :382). grep over all three scripts finds no `/tmp` literal outside the guard/docstrings.
- Residual (accepted): `HYAKU_SCRATCH` is caller-controlled and unguarded, but the C1 counter fails closed (exit 2) on a /tmp work dir, so a /tmp misconfiguration cannot produce a passing C1.

### PASS — receipts destinations and census-end copies

- All receipts are written under `$OUT`: `frozen.stdout` (23), `no-harm.stdout/.exit` (26), `coldread-sections.stdout` (30), `c2.stdout/.exit` (32), `census.stdout/.stderr/.exit` (33), `c1.stdout/.exit` (36), `deciding-run.stdout` (38).
- Census-end copies present, line 34: `cp "$OUT/census.{stdout,stderr,exit}" "$E/census-end.{stdout,stderr,exit}"` — matching the start receipts at `$E/census-start.*` and the frontier_step ("census start/end via scripts/sources-census.sh validate"; line 33 runs exactly `$FLEET/scripts/sources-census.sh validate --root "$FLEET" tameshi`).

### PASS — FROZEN covers every tool a C1 statement pins, plus counters/statements/contract/freeze-2

- Pinned tools, extracted from the frozen statements file (`jq -r '.statements[] | [.id,.sha_file] | @tsv' .ufo/evidence/round-47/calibration/statements.json`): 22 statements, 19 distinct `sha_file` paths — 15 under `tools/` (mutate-and-run.sh, repeat-control.py, pin-disposition.py, witness-metadata.py, evidence-disposition.py, env-diff.py, wave-accounting.py, command-binding.py, registry-replay.py, mte-interop.py, tally-audit-v2.py, tally-audit-v3.py, write-path-census-v2.py, write-path-census-v3.py, staged-id-guard.py), plus `.ufo/evidence/kaika-round-1/sources-census-v2.sh`, `.ufo/evidence/round-15/verify.py`, `.ufo/evidence/round-21/coldread/measure.py`, `.ufo/evidence/round-45/freshness/measure.py`.
- Every one is under a FROZEN path of line 22 (`tools` covers all 15; the four evidence-dir pins are listed whole). statements.json is listed explicitly; both counters, contract.json and freeze-2.json are in FROZEN.
- Independent hash verification at REV (what line 24's `COUNTER_SHA256` receipt lines must therefore print):

```
calibration 572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3   = freeze-2.json ✓
freshness   faefe9b442741bcd7238ffe028841a0da7453c14c70f9f33afbd0f77be2df63f   = freeze-2.json ✓
statements  924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56   = freeze-2.json ✓
contract    4fff75dbaac728992fa04ffd3ccfea6ace8ca80b944cc393b63c287fadc6d59e   = freeze-2.json ✓
```

### INFO

- `freshness/__pycache__/` sits untracked in the worktree (created 2026-10-26 10:30 by control/import runs; gitignored via `.gitignore:4 __pycache__/`). It cannot enter a receipts-only commit unless force-added, and untracked files never affect line 23's diff. No action needed; noted so its presence in `git status` surprises no one.
- The script has no trap: a mid-run interrupt leaves `$SCR` and a partial `$OUT` behind (the normal path rm's both, lines 35/37). Cosmetic for a single-invocation run.
- Amendment 9 is satisfied upstream: `control/c2-controls.meta` records `scored_at_freeze_bytes=7552984` — which is exactly what arms F1 once those receipts were committed at `c7586b9`.

---

## Deciding receipts commit (filled when it lands)

Watcher running on HEAD `17cc5ce1…` / `.ufo/evidence/round-48/after/deciding-run.stdout`. Expected per F1: with the declared FREEZE the `frozen.stdout` first line must read `FROZEN_UNCHANGED=0 freeze=755298415f8c…`; an observed `FROZEN_UNCHANGED=1` is only possible with FREEZE=`c7586b9a`/`17cc5ce` (F1 table) and the printed `freeze=` hash will show which was used.

*(to be completed before yield)*

## Verification gaps

- The L1's actual command line for the deciding run is not observable from this seat (no `after/`, no process at review time); F1's FREEZE-value analysis covers the declared value and all round commits, and the landed receipts section settles it empirically.
- I did not execute the counters (probes are never verdicts); counter-internal behavior is cited from the frozen files only where line-level evidence was needed (the /tmp guard).
