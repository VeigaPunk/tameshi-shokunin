# T53W1ScoutCensus — census + misroot pre-check (wave 1, round 53)

Seat: T53W1ScoutCensus (scout, leaf). Date: 2026-10-27 (UTC).
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Read-only except this report.
Tool installs: none — host `bash`, `git`, `gawk`, `grep` sufficed; pacman guard respected (no pacman invoked).

## 1. Census pre-check — PASS

Command (exactly as assigned):

```
TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

Result: **exit 0**. Stdout 17 lines, stderr 0 lines:

- 15× `W04` (same URL across scopes: S047, S048, S075, S076, S077, S078, S081, S092, S104, S160, S265, S266, S267, S268, S274)
- 1× `W01` (S101 tier-C mined with non-`—` used-by: `corpus/knowledge/witness-equivalence-rule.md`)
- 1× `tameshi\tok\t/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`

No `E*` codes. Per the script header, W-codes never change a clean lane's status, so exit 0 is the expected clean result.

Cross-check of the "136 rows" expectation (registry size, not output-line count) via
`TZ=UTC bash .../sources-census.sh census --root /home/vgpnk/Projects/shokunin tameshi` (exit 0):

```
tameshi rows 136            FLEET rows 136
tier.A 121 / tier.B 12 / tier.C 3      tier.invalid 0
status.queued 21 / mined 109 / rejected 6   status.invalid 0   missing 0
```

Independent byte-count of the registry table: `grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` = **136**. Expectation (exit 0, 136 rows) MET.

## 2. Fleet-root misroot scan

`git -C /home/vgpnk/Projects/shokunin status --porcelain` (exit 0) shows exactly two untracked entries:

1. **`.ufo/reports/round-53/tameshi.md`** — CONTENT MATCHES "tameshi round 53".
   Line 1 (verbatim): `# Tameshi round 53 — cold-read floor repair (calibration) + tools scratch hygiene (operability)`
   The file self-identifies as the L1's own in-progress round report ("L1 TameshiR53a2, hyaku run 10, attempt 2 …") with "to be completed" sections still open.
   Context: this is the fleet's conventional reports pool — `/home/vgpnk/Projects/shokunin/.ufo/reports/round-NN/<lane>.md` exists for rounds 1–108, and the round-53 sibling lane reports (`chousa/kake/kama/kotoba/kotodama/kumitate/mori.md`) plus all of round-52 are already **tracked** in the fleet repo (`git ls-files` confirms). This file is simply the newest report not yet committed.
   → Listed as the sole misroot candidate per the item's letter; the L1 sweeps before final assembly. Assessment: L1-owned file at its conventional path, not a seat misroot.
2. `.scratch/closure-mado-r50.json` — does **not** match: zero case-insensitive `tameshi` occurrences; it records a `mado` lane round-50 closure (`"round": 50, "lane": "mado"`). Not a round-53 candidate. (Note: `.scratch` is read-only-over per seat bounds; read for census only.)

No other untracked or modified files at the fleet root.

## 3. Lane seat-discipline check — PASS (as of check time)

`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain` + `ls-files --others --exclude-standard` + `diff --name-status`:

- Untracked under `.ufo/waves/round-53/w1/`: 21 sibling seat files (`T53W1Read{02,04,06,07,09,10,11,12,14,21,22,23}.{json,md}` partial set) — all in-scope.
- Untracked outside w1: only L1/orchestrator-owned paths — `.ufo/evidence/round-53/**` (assimilation snapshots incl. the `validate/` clone, `verify-freeze.*`, `census-mid.stdout`, `integrate/rekey.py`), `.ufo/waves/round-53/spec-w2.json`, `.ufo/waves/round-53/w1.ready.dispatched`.
- Tracked diff: only `D .ufo/waves/round-53/w1.ready.partial` — dispatch-marker rotation by the orchestrator.
- No modifications to `SKILL.md`, `tools/`, `corpus/`, `MANIFEST.json`, or any lane-root file.

Conclusion: **zero seat-origin writes outside `.ufo/waves/round-53/w1/`**; every out-of-w1 delta belongs to the L1/orchestrator domains the seat bounds assign to the L1. Seat discipline holds.

## Scratch hygiene

Seat scratch `/fast/scratch/hyaku/tameshi-r53/w1/T53W1ScoutCensus/` held only the two census output captures; deleted before yield (verified absent). Nothing written under `/tmp` by this seat.

## Report: .ufo/waves/round-53/w1/T53W1ScoutCensus.md
