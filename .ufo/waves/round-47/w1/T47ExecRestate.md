# T47ExecRestate — full C1 `--emit` at the freeze: the 22 rows, and the three that the load, not the statement, wrote

Seat: leaf executor. Item: run the FULL C1 counter once at the freeze with `--emit` into an empty scratch work dir,
deliver the 22 rows as the draft of the standing tables, and reconcile the observed dependence sets with the five
T47ExecObs seats.

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, rev `9acfbe21435e1976636a276448dee1d5e7155915` (freeze), base
`0b5b7cd2b2c15d23086e811a0f0348d84261277b`. Counter `.ufo/evidence/round-47/calibration/measure.py`, run only as the
item's single measured pass (`self_pin=1 stmts_pin=1`, `append_only=1`); no verdict is claimed from it. Read-only on the
lane: the two files below are the only lane bytes written. No git/jj mutating command, no install (pacman stays paused
host-wide; nothing was needed), no write to `/home/vgpnk/Projects/shokunin` or `shokuknow`.

## Files written

| file | content |
|---|---|
| `.ufo/waves/round-47/w1/T47ExecRestate.rows.md` | the 22 `EMIT_CAP`/`EMIT_AXIS` rows verbatim, the `C1_R47:` line verbatim, the 8 `PROFILES` lines for statements with a non-`none` dependence set, the 22-row deps table against the Obs seats, and the corrected text for the three load-artifact rows |
| `.ufo/waves/round-47/w1/T47ExecRestate.md` | this report |

## The pass

```
python3 .ufo/evidence/round-47/calibration/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 9acfbe21435e1976636a276448dee1d5e7155915 \
  --base 0b5b7cd2b2c15d23086e811a0f0348d84261277b \
  --work /var/tmp/tameshi-r47-T47ExecRestate/w --emit
```

First launched into `/tmp/tameshi-r47-T47ExecRestate/w` as the item states; after the L1's ENOSPC note
(`/tmp` is a 128 G partition at 94–100 % host-wide, 15 M free at its worst today) the job was cancelled and rerun with
the work root under `/var/tmp` — same bytes, root fs, 566 G free. The rerun is the reported pass: `--work` empty at
start, 22 statements × 6 profiles = 132 observations, wall **2385 s**, exit 1.

```
C1_R47: self_pin=1 stmts_pin=1 statements=22 mismatches=0 unparsed=22 unobservable=0 dep_mismatch=0 unpinned=0 append_only=1 total=22 rev=9acfbe21435e1976636a276448dee1d5e7155915 C1_R47_PASS=false
```

`unparsed=22` is the freeze state, not a regression: `claim_of` returns `None` unless the row carries the full
`value, exit N, tool sha256 "…", deps "…"` shape, and no standing row has a `deps` clause yet. Consequence worth
flagging to the L1: **`mismatches=0` in this line is vacuous** — the counter parsed no row, so it compared no value.
The emitted values are the observation set; nothing in this run confirms the standing rows against it.

The work root was under `/var/tmp`, not `/tmp`. That matters for one row: `hermetic env-differential probe` reads
`deps bwrap,node` here, the truthful set. ObsC showed the same statement reads `deps env,node` when `--work` sits
under `/tmp`, because the counter puts the profile PATH shim inside the work dir and `tools/env-diff.py:69` masks
`/tmp` with `--tmpfs /tmp`, so `bash` cannot be exec'd in the sandbox and P1 itself is broken. A deciding run whose
`--work` is under `/tmp` will emit a false dependence there.

## Observed dependence sets vs the five T47ExecObs seats

Seventeen of 22 statements agree with the seats, cell for cell, including every non-`none` set they measured:

| statement | this run | seat | agreement |
|---|---|---|---|
| sources-registry | none | ObsA none | agree |
| mutation sweep runner | none | ObsB none | agree |
| six-leg regression ledger | `fleet-root,node` | ObsE `fleet-root,node` (run 1); run 2 added a spurious `jj` | agree with run 1; the `jj` cell is ObsE's own documented pipefail flake |
| repeated pristine-control gate | none | ObsB none | agree |
| six-leg content-disposition probe | none | ObsB none | agree |
| exposed witness provenance correction | none | ObsB none | agree |
| effective expectation reconciliation | `jj` | ObsC `jj` | agree |
| retained invocation-context gate | `fleet-root` | ObsC `fleet-root` | agree |
| hermetic env-differential probe | `bwrap,node` | ObsC `bwrap,node` (work dir outside `/tmp`) | agree |
| callback-authoritative wave accounting | none | ObsC none | agree |
| required-command-receipt-binding | none | ObsD none | agree |
| refusing-registry-replay | none | ObsD none | agree |
| mutation report interop | `node` | ObsD `node` | agree |
| write-path-census-v2 | none | ObsE none | agree |
| write-path census destination resolution | none | ObsE none | agree |
| staged-id adoption guard | none | ObsE none | agree |
| depth / calibration / freshness | none / none / none | ObsA none / none / none | agree |

**Every disagreement is one mechanism — a timeout — and there are exactly three rows:**

| statement | this run emitted | seats observed | the cell that drove it |
|---|---|---|---|
| tally-audit-v2 runner audit | `deps env,fleet-root,node` | ObsD `none` in all six profiles | P1, P2, P3 timed out at the 900 s cap; P0, P4, P5 passed with identical 869-byte obs |
| tally-audit-v3 runner audit | `deps env` | ObsD `none` in all six profiles | P1–P5 all timed out at the 1800 s cap; P0 passed |
| bounded ANSI-C code_view | `deps env,fleet-root,node` | ObsE `none` in all six profiles | P1, P2, P3 timed out at 1800 s; P0, P4, P5 passed with identical 1453-byte obs |

Why these are artifacts and not dependences, in order of strength:

1. **The same command disagreed with itself inside one run.** `tally-audit-v3 runner audit` and `bounded ANSI-C
   code_view` are the identical argv (`python3 tools/tally-audit-v3.py --selftest`, same rev, same per-profile clone);
   P4/P5 passed for one statement and timed out for the other. A command cannot both need `node`/`fleet-root` and not
   need them. `env` is even weaker: it is defined as *P0 ≠ P1*, and it fires here only because P1 timed out while P0
   passed.
2. **No such prerequisite exists in the tools.** `grep -nE "node|jj|bwrap|fleet" tools/tally-audit-v2.py
   tools/tally-audit-v3.py` → 0 matches in either file. Neither selftest can consult `node`, `jj`, `bwrap` or the fleet
   root by name.
3. **Solo runs finish, and finish inside the cap only barely.** Under the exact P1 environment, alone: `tally-audit-v3`
   513 s → `35/35 pass`; `tally-audit-v2` **802 s** → `22/22 pass`. The frozen timeout for `tally-audit-v2` is **900 s**.
   Twelve cells of these tools run concurrently under the counter's hardcoded `jobs=14` beside the nine-leg regression
   ledger (~8 min per profile) and the 106-case sweep; an 89 %-of-cap solo run cannot survive that.
4. **Independent profile cells.** `tally-audit-v3 --selftest` under a shim with `bwrap` removed (the exact P2 shim
   build) → `35/35 pass`, 546 s, obs 1453 B, byte-identical to P0/P4/P5. The P3 (jj) cells for these tools were
   measured by two seats on this rev (ObsD all six profiles, ObsE for the v3 command) and pass.

Draft the three rows with `deps none`. `T47ExecRestate.rows.md` §5 gives those three lines with only the deps field
changed, so the writer can paste them without touching the rest of the emit output. Declaring `env,fleet-root,node` or
`env` there would assert a host dependence that does not exist and would be falsified by the next run that happens not
to time out.

## Risk the L1 must price before the deciding run

The frozen statements list is sha256-pinned, so the timeouts cannot be raised. `total=0` for C1 therefore requires all
132 cells to finish: `tally-audit-v2` must complete 802 s of work inside a 900 s cap *while* the other 13 heavy tasks
run, and two 513 s selftests must each finish inside 1800 s under the same load. In this pass 11 of 132 cells (8 %)
lost that race — deterministically on the unloaded host, stochastically under the wave's load — and every lost cell
manufactures dependence names.

Three concrete preconditions for the deciding run, each supported by a receipt here or by a sibling:

- an otherwise idle host (no concurrent seats): my pass overlapped the hardening and coverage waves;
- several GiB free on the **`--work` filesystem** (2.4 GiB per pass: 12 clones) **and** on `/tmp`, which
  `tally-audit-v3`'s `auto_root()` needs (`tools/tally-audit-v3.py:422-425`; without it 31 of 35 cases fail, ObsD §7);
- `--work` outside `/tmp`, or `hermetic env-differential probe` emits `env,node` instead of `bwrap,node`.

If the deciding output nevertheless shows `unobservable`/`timeout`, the honest reading is "the host was loaded", not
"a statement regressed": compare the emitted deps against the three rows above, and re-take the pass on an idle host.
A fourth, independent hazard on the same statements: ObsE measured `six-leg regression ledger` flipping
`PASS (passed=9)` → `FAIL (passed=8)` in one of twelve invocations through a `pipefail`/`grep -q` race in the pinned
tsukuroi leg. A P0 flake there is a `mismatch`, an isolated `jj`/`bwrap` there is a false dependence. My pass drew the
clean side of that race in all six profiles.

## Behaviour summary the L1 can adopt

- 19 rows are stable across all six profiles and agree with the seats: `deps none` for 14 of them, `jj` for
  `effective expectation reconciliation`, `fleet-root` for `retained invocation-context gate`, `bwrap,node` for
  `hermetic env-differential probe`, `node` for `mutation report interop`, `fleet-root,node` for
  `six-leg regression ledger`.
- 3 rows (`tally-audit-v2 runner audit`, `tally-audit-v3 runner audit`, `bounded ANSI-C code_view`) are `none`; the
  emit output in this pass says otherwise only because of timeouts.
- `value, exit, tool sha256` in the emitted rows reproduce the standing `SCORECARD.md@9acfbe2` cells (lines 2177–2194 and
  the three axis rows) for all 22 statements — that part of the draft is a copy, not a change.

## Retained evidence

`/var/tmp/tameshi-r47-T47ExecRestate/` (the 2.4 GiB clone tree `w/` was deleted after capture, per the L1):

```text
emit.out                68 lines: 22 STATEMENT, 22 PROFILES, 22 EMIT, the C1_R47 line, EXIT=1
                        sha256 71df39bd67b3ea999908493908b6185f7e343c815cf7587c4e5dec93f16cb67c (18665 B)
obs/P{0..5}/            121 obs-*.stdout, one per cell that did not time out; 11 cells absent = the timeouts
probe-v3-P1.out         513 s  TALLY_AUDIT_V3_SELFTEST: 35/35 pass      (P1 env, alone)
probe-v2-P1.out         802 s  TALLY_AUDIT_V2_SELFTEST: 22/22 pass      (P1 env, alone)
probe-v3-P2.out         546 s  TALLY_AUDIT_V3_SELFTEST: 35/35 pass      (P1 shim minus bwrap)
probe-variants.timing   v3-P2 line above; v2-P2/P3 and v3-P3 were cancelled on the L1's wrap-up instruction
gen_rows.py             the generator that turned emit.out into the delivered rows file (no hand transcription)
```

## Blockers and limits, stated plainly

- The three variant cells I planned for the tally tools (`v3` under the jj-less shim, `v2` under both variant shims)
  were cut short by the wrap-up instruction. They are not needed for the deps verdict — items 1–4 above settle it, and
  ObsD measured those exact cells — but they are the only cells of the 132 that no seat in this wave measured solo.
- The `/tmp` 100 % condition is host-wide and outside my bounds; I mitigated it by relocating my own scratch only.
- Nothing was installed or upgraded; no pacman transaction was attempted.
