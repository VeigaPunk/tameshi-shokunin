# T53W2ScoutScratch — wave-2 scratch audit (tameshi round 53)

Seat: T53W2ScoutScratch (wave 2 of 2, hyaku run 10). Audit time: 2026-10-27 10:53–10:55 -0300.
Scope: read-only audit of `/fast/scratch/hyaku/tameshi-r53/` + disk-guard + df. **Cleaned nothing**, per the item. This seat created no scratch tree (all commands read-only), so there is nothing of mine to delete before yield.

## Checks run (commands → evidence)

1. `ls -la /fast/scratch/hyaku/tameshi-r53/` + listings of `w1/` and `w2/` — tree census.
2. `du -sh` on each `w1/` survivor and on `w2/` and the round root — sizes.
3. `find /fast/scratch/hyaku/tameshi-r53 -maxdepth 1 -newermt '2026-10-27 10:00' -printf '%TH:%TM %y %p'` — which round-root items are live.
4. Content peeks at `lost-at-c0.txt`, `drvtest/`, `p2check/`, `probe-c2pp/`, `selftest-check/` — attribution hints.
5. `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`.
6. `df -h /tmp /fast/scratch`.

## Finding 1 — four wave-1 seat trees still survive under `w1/`

Expected: wave-1 trees deleted before their yield. Survivors (all present at audit close, 10:55):

| Seat (owner) | Path | Size | Latest write | Active? |
|---|---|---|---|---|
| T53W1ExecR523 | `w1/T53W1ExecR523/` (ctx.pkl, table.pkl, repo/ clone) | 207M | 10:39 | roster: still running; 15 min stale |
| T53W1ExecRegCheck | `w1/T53W1ExecRegCheck/` (SKILL_Cstar.md, c1work/, c2work/, cstar_monitor/, 6 tameshi-r16/r17 fixture dirs) | 263M | 10:51 | fresh — active |
| T53W1LabLint | `w1/T53W1LabLint/` (scan.json, 3 skill copies, probe dirs) | 1.9M | 10:52 | fresh — active |
| T53W1MutCounter | `w1/T53W1MutCounter/` (build_and_mutate.py, mutants/, runs/ 32 entries) | 5.5M | 10:53 | fresh — active |

Total ≈ 477M. Assessment: three of four show writes 1–4 minutes before this audit (10:51–10:53) and the fourth's seat is still on the live roster, so these are **survivors with cleanup still pending, not yet post-yield defects**. They become defects if any owning seat has already yielded, or at their yield if not then deleted. Names for the record: T53W1ExecR523, T53W1ExecRegCheck, T53W1LabLint, T53W1MutCounter.

## Finding 2 — ten persistent loose items at the round root, outside every seat tree

`/fast/scratch/hyaku/tameshi-r53/` holds these non-seat entries (none under `w1/<seat>` or `w2/<seat>`), violating the scratch directive "everything under …/w2/<seat-name>/":

- `__pycache__/` (dir, 10:52) — **active during wave 2**
- `controls-A/` (dir, 10:09)
- `dbg/` (dir, 10:08)
- `drvtest/` (dir, 10:48, contains r18.py, r18b.py, __pycache__) — **active during wave 2**
- `lost-at-c0.txt` (file, 1675 B, 10:17 — a "LOST ##" cold-read heading list for rounds 12–26)
- `p2check/` (dir, 10:42 — monitor .out files: registry-check, env-diff, pin-disposition, …)
- `probe-c0/` (dir, 10:16)
- `probe-c2pp/` (dir, 10:49 — env-diff.py, registry-check.py) — **active during wave 2**
- `r18measure.py` (file, 76144 B, 10:52) — **active during wave 2**; byte-size-identical (76144) to `w1/T53W1LabLint/r18_measure.py` and `w1/T53W1MutCounter/r18.measure.orig.py`, i.e. a copy of the lane's measure.py dropped at the round root [INFERENCE: copied by an active seat instead of into its seat tree]
- `selftest-check/` (dir, 10:15 — same monitor .out names as p2check/)

Live evidence of ongoing misuse: an eleventh loose dir `no-harm/` was created at 10:54 **between two of my census commands** and deleted before 10:55 — a seat is using the round root as transient scratch right now. `p2check/`/`selftest-check/` output names match the wave-1 monitor seats' vocabulary [INFERENCE: likely T53W1LabLint / T53W1ExecRegCheck lineage], but the loose items have no seat attribution on disk, so the seat-level defect cannot be assigned from evidence.

## Finding 3 — disk and /tmp health: no pressure

- `df -h`: `/tmp` 128G total, 3.9G used, 4%, 125G avail; `/fast` 804G total, 208G used, 26%, 596G avail. Round root `tameshi-r53` totals 2.4G (`w2` 1.9G + `w1` ≈ 477M loose ≈ 60M).
- `disk-guard.sh status` runs clean and agrees: /tmp 4% (124.0G free), /var/tmp 35% (588.8G free), /fast/scratch/hyaku 26% (595.6G free). Top hyaku consumers: kaidoku-r43 5.3G, kake-r62 4.5G, tabi-r37 2.5G, mado-r51 1.7G, kama-r55 796M, **tameshi-r53 688.5M (idle=0 — the only large active tree)**.

## Observation — /tmp items over the 50 MB guidance

disk-guard's /tmp consumer list shows six entries above 50 MB: `r57a8d` 304.1M, `rdbg` 145.8M, `i2dbg3` 145.8M, `i2dbg2` 145.5M, `i2dbg` 145.5M, `i7u` 145.4M (plus two 367M `KimiCode` AppImage mounts, host-level). The r-dbg names suggest round debug dumps [INFERENCE], but no seat is attributable from the available evidence; reported for the L1's hygiene ledger, not attributed as a seat defect.

## Bottom line

- Operability: good — disks unconstrained, disk-guard functional, wave-2 seat trees (26) all present and correctly named under `w2/`.
- Defects to carry: 4 surviving wave-1 trees (owners named; cleanup due at their yields) and 10 persistent loose round-root items plus transient `no-harm/` traffic (scratch-directive violations, unattributable to a specific seat on disk evidence).
- Nothing cleaned (per item); no tree of mine exists to delete.
