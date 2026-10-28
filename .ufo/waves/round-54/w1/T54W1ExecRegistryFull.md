# T54W1ExecRegistryFull — registry full check at C0 (round 54, wave 1)

Seat: `T54W1ExecRegistryFull` (wave-1 executor, axis: operability; milestone: registry full check).
Item: run `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry-check.py --root
/home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 59c38109bf119d0e9d4f878644a82babc937bc1e`
(the full 56-row check), paste the summary line and every not-held row, and say whether the
round-52 C1 surface regressed.

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (read-only for this seat).
Scratch (`TMPDIR` exported to it, removed at the end of this seat's work):
`/fast/scratch/hyaku/tameshi-r54/T54W1ExecRegistryFull`.
No tool was installed or upgraded (nothing needed; `bc` is absent on this host and only the
inline elapsed echo used it — see R5). No git/jj mutation was run anywhere.

## Headline

```
REGISTRY_CHECK: held=49/49 superseded=7
```

- **Exit 0.** 56 rows replayed: 49 active + 7 superseded. **No active row is not-held: the full check is green at C0.**
- **Wall 429.55 s** (harness-reported job wall; file window `11:28:20.334` → `11:35:29.880` = 429.546 s).
  It finished inside the 900 s time-box, so no "could not finish" case arises.
- stdout = 57 lines (56 `ROW` lines + 1 summary), 2934 bytes; stderr = 0 bytes.
- Every row line is in receipt `full-check-c0.out`; summary line above is its last line.

## Not-held rows

**Active rows that did not hold: none.** The tool prints `held` on every active row line; there is
no `differs`, `timeout`, `unavailable` or `non-hermetic` token in the output.

The seven **superseded** rows also executed (they are excluded from `N/M` by the tool's contract,
`tools/registry-check.py:31-38`). Three of them do not match their `expect.exit`, and they print
without a verdict token by design. Pasted verbatim, with the round-52 baseline control beside them:

| row (all `superseded`) | expect | got | round-52 baseline (`w2/T52W2ExecC1Probe/registry-check.stdout`) |
|---|---|---|---|
| `evidence-disposition-round17` | 0 | 2 | identical |
| `evidence-disposition-round17-before` | 1 | 2 | identical |
| `evidence-disposition-round14-superseded` | 0 | 2 | identical |
| `trace-inputs-round17-selftest` | 0 | 0 | identical |
| `command-binding-selftest` | 0 | 0 | identical |
| `command-binding-frozen-clean` | 0 | 0 | identical |
| `command-binding-source-read-red` | 1 | 1 | identical |

The three `evidence-disposition` got=2 rows are the pre-existing state recorded in round 52
(`REGISTRY_CHECK: held=49/49 superseded=7` there too) and in the round-53 report
(`.ufo/waves/round-53/w1/T53W1ExecRegCheck.md`, "All 7 superseded rows produce byte-identical
observations… including the three `evidence-disposition` rows that read `got=2`"). This run
reproduces those seven lines byte for byte, so nothing moved.

## The round-52 C1 surface did not regress

The item calls this "the round-52 C1 surface". I fed this run's exact stdout to
the **frozen** round-52 C1 predicate (`.ufo/evidence/round-52/c1/measure.py`, loaded as a module,
`main()` never run) and evaluated the three components that this artifact is:
receipt `c1-predicate-rdm.out`, script `c1-predicate-rdm.py`.

```
R: held=49 n=49 not_held=[] extra=0
D: dropped=[]
M: mte_row_ok=(True, "legs=10 want='MTE_INTEROP: PASS legs_conforming=10/10' status=active needles=['MTE_INTEROP: PASS legs_conforming=10/10']")
```

- **R** (`not_held` + summary arm) = **0**: `parse_registry_check` finds 49/49, no not-held row, summary consistent.
- **D** (dropped base active rows, against `c1/base-active.json`) = **0**: the 49 active names at C0 are exactly the 49 at base `ef19d8e1` — no drops, no additions.
- **M** (`mte_row_ok`) = **True**: the C0 registry row still carries the `10/10` needle and `tools/mte-interop.py` at C0 still has 10 legs.
- C (round-51 C3 counter) and G (round21 literals) are not this item's subject; they belong to the C1 counter seat.

Direct control on the row that was red in round 53: `--only verify-round15` at C0 →
`ROW verify-round15 expect=0 got=0 held` / `REGISTRY_CHECK: held=1/1 superseded=0`, exit 0
(receipt `only-verify-round15-c0.out`). Round 53 measured this row as `differs` at its C*; the
split-pin repair is in C0 (`verify.py:115` `PIN_MAINTAINED_TOOL_SHA256`, used at `:647`), and the
row now holds. That is the one row that could have regressed the surface, and it does not.

## What was opened / checked

- `tools/registry-check.py` (live lane): sha256 `ade15cc0…` = `59c38109…:tools/registry-check.py`, so the item's absolute path ran the C0 monitor bytes.
- `tools/registry.json` (live and at C0): sha256 `ef79ab8e…` at both.
- Registry shape at C0 (receipt `hygiene.out`): `rows=56`, kinds `{gate:22, selftest:30, probe:4}`, statuses `{active:49, superseded:7}`, `scratch_root` cells = 7 (`repeat-control-selftest`, `bash-witness-selftest`, `pin-disposition-selftest`, `evidence-disposition-selftest`, `context-capture-selftest`, `registry-check-selftest`, `env-diff-selftest`). The extra field does not break `registry_errors()` (`tools/registry-check.py:180-250` validates named fields only), and the run proves it: the registry loaded and 56 rows executed.
- Round-52 baseline row lines (`.ufo/waves/round-52/w2/T52W2ExecC1Probe/registry-check.stdout`) and round-53's report, for the superseded-row and verify-round15 comparisons.
- `git -C <lane> status --porcelain` after the runs: only the pre-existing round-54 wave work plus one concurrent edit (see R3). This seat wrote nothing outside `.ufo/waves/round-54/w1/`.
- Sources census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, 16 warning rows, ending `tameshi ok …/corpus/SOURCES.md` (receipt `hygiene.out`).

## Risks / observations (none blocks the claim)

**R1 — three rows leak their selftest scratch under TMPDIR (pre-existing, not a C1 change).**
The run left exactly three directories under the caller's `TMPDIR` (480K + 1.6M + 1.6M = 3.7 MB),
one per leaking row: `measure-round16-selftest` → `.ufo/evidence/round-16/measure.py:411`,
`measure-round17-selftest` → `.ufo/evidence/round-17/measure.py:870`,
`measure-round18-selftest` → `.ufo/evidence/round-18/measure.py:886`. Each is a `selftest()`
`tempfile.mkdtemp(prefix=…)` with no `dir=` and no removal; the three rows *held*. They are not
among the seven `strict_scratch_root()` tools, so this is outside C2 — but it is a real scratch
hygiene fact for the L1. Evidence: `hygiene.out` §TMPDIR.

**R2 — the monitor itself is clean.** No `tameshi-registry-check-*` work dir survived under `TMPDIR`:
the `--rev` clone and its fixtures were removed. The clone was made from the lane and `--rev`
resolved `rev_resolved` to C0 (the tool reports it; rows ran there).

**R3 — concurrent worktree drift after the run.** `git diff CAB -- tools/` was **empty** when the
run started (checked before launching). While this report was being assembled, `tools/env-diff.py`
was modified in the live worktree at `11:37:38` (128 s after the run ended) — a `except
ScratchRootUnusable` → exit 2 mapping added at `main()`. Not written by this seat (write scope is
`.ufo/waves/round-54/w1/` only), and it cannot affect this result: rows execute inside the C0
clone, and the monitor path stayed byte-identical to C0. Flagged only so the L1 does not attribute
it to this seat.

**R4 — `/tmp` traffic in this window is not this run's.** `/tmp/tameshi-r17-registry-check-selftest.*`
entries appeared at `11:35:50-52` and `11:37:53`, i.e. after the run ended: concurrent seats running
`registry-check.py --selftest` with `TMPDIR` unset. The one entry inside the window
(`/tmp/tameshi-r4-2-regression.Fa6S8t`, `11:33:37`) is an **empty** directory; `mutate-and-run.sh`
uses `${TMPDIR:-/tmp}` (`:1432`) and removes its root on PASS (`:148-150`), this run had `TMPDIR`
set and that row held, so the empty dir is a concurrent seat's, not this row's output. Evidence:
`hygiene.out` §`/tmp`.

**R5 — elapsed echo used `bc`, which is absent.** The launch wrapper's `bc` arithmetic printed
`ELAPSED=` empty (job still `RC=0`); the authoritative wall is the harness's 429.55 s, corroborated
by the `full.err`/`full.txt` mtimes (429.546 s apart). No consequence for the result.

## Receipts

Directory: `.ufo/waves/round-54/w1/T54W1ExecRegistryFull-receipts/`

| file | bytes/lines | sha256 | what it is |
|---|---|---|---|
| `full-check-c0.out` | 2934 B / 57 lines | `a2294843a548f3357185d2855557419f63ab342b1bb65a8cb4e913b0478a56a7` | verbatim stdout of the item's exact command |
| `full-check-c0.err` | 0 B | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | verbatim stderr (empty) |
| `only-verify-round15-c0.out` | 77 B / 2 lines | `9b46ca6cbc33a654666ccd2dbfe06b4cb2eeab7eb3fb4fe3985c502aec7240e6` | `--only verify-round15` control at C0 |
| `c1-predicate-rdm.py` | 1470 B | `f745378b440f14baad3519feac67929bc695545e6463a89e391071dc8ce88965` | frozen round-52 C1 R/D/M probe |
| `c1-predicate-rdm.out` | 3 lines | `385d9349defd4b6d329f09a01c3bfde01e1c96fa7cea9e6a3126398c640d153a` | its output |
| `hygiene.out` | 105 lines | `a67726a1e51499acf58a321d5f7f3c2106727ec7c242ebd70b54f801aa16d2b1` | timing, TMPDIR/`/tmp` attribution, C0 byte identity, registry shape, lane status, census |
| `sha256sums.txt` | — | — | the above hashes |

All commands in `hygiene.out` and `c1-predicate-rdm.py` are runnable as written: they read git
objects at C0 and print their own output; nothing writes to the lane.

## Bounds

- Wrote only `.ufo/waves/round-54/w1/T54W1ExecRegistryFull.md` and
  `.ufo/waves/round-54/w1/T54W1ExecRegistryFull-receipts/`. No lane production file, counter,
  contract, freeze, ledger or wave spec was touched; `SKILL.md` was not edited.
- No mutating git/jj command was run anywhere (only `show`, `diff`, `status`, `rev-parse` read-only forms).
- Scratch tree removed after the receipts above were copied into the wave dir.
