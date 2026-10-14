# AUD-T8 — verdict table: audit of the two round-8 mutation cases (T8-1 kagi `checklist-run.sh`, T8-2 kumitate `claims-check.mjs`)

Audit run 2026-10-14 19:14–19:25Z by lane AUD-T8 (round-8 wave, width 32; lane
scratch `/tmp/w8-aud-t8-{work,evidence}/`). **Read-only: no fleet file was
written or edited by this audit**; the two audited gates, both sibling repos
and the tameshi tree were handled read-only throughout (repos porcelain-clean
at open and at close; §2). No substrate-mutating command was run; no secret
file read; no external site contacted. The four mutant re-runs executed on
copies under `/tmp/w8-aud-t8-evidence/` only. Write scope: this report only.

## 0. What was audited

The wave's two new cases, as landed today by lanes T8-1 and T8-2:

| case | target @ pin | facts | suite | recorded headline |
|---|---|---|---|---|
| T8-1 kagi checklist | `kagi-shokunin/corpus/checklist-run.sh` @ `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf` | 506 L / 24,697 B, mode 755; blob `78f2c45eed31…` @ kagi `fecee87` | `bash "$MUTANT" --selftest` (34 cases) | 7/15 killed (47 %); survivors A1, B1, B3, C1, D1, E2, F2, G1 |
| T8-2 kumitate claims | `kumitate-shokunin/scripts/claims-check.mjs` @ `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b` | 925 newlines / 48,265 B, final line unterminated (`;`); blob `fae4bbcd158c…` @ kumitate `175de6b` | `node "$MUTANT" --selftest` (39 cases) | 7/10 killed (70 %); survivors D7, D8, D9 |

Frozen case-note revisions (stable ≥3 min before this write; later edits need
re-audit — U1):

| artifact | sha256 | bytes / newlines |
|---|---|---|
| `corpus/knowledge/mutation-case-kagi-checklist.md` | `43da70e675b8a482c942fddf6360d84970cf0c29ee648039e11b3b819ae739e7` | 22,952 B / 367 (final line unterminated) |
| `corpus/knowledge/mutation-case-kumitate-claims.md` | `3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9` | 29,236 B / 409 (final line unterminated) |

Instrument both cases ran: `tameshi-shokunin/tools/mutate-and-run.sh` @
`cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75` (61,632 B);
live sha unchanged through the audit; T8-1's executing copy
(`/tmp/w8-tameshi-t81/mutate-and-run.sh`) is byte-identical to it.

### 0.1 Drift observed in the audit window (recorded, never smoothed)

Both notes were still being written when first hashed — checklist
`deb72558…` → `8cc06046…` → `43da70e6…` and claims `e64e8a2a…` → `3da1312e…`
inside ~5 minutes (16:18:47–16:19:31 −0300). Verdicts below bind to the frozen
revisions above; a post-close edit needs a re-audit (append-only).

## 1. The re-runs — 2 mutants each, from pinned blobs (O)

Method (read-only): for each case I re-materialized the target from its repo's
git object store (`git show <rev>:<path>`), cut 2 of the case's recorded
defects — one KILLED + one SURVIVED, so both verdict directions are exercised —
byte-identically from the case's own spec into a 2-defect spec
(`/tmp/w8-aud-t8-work/{checklist2,claims2b}.spec`), and re-ran them through the
same instrument revision with the same suite command the case used.

| case | re-run id | my verdict | my mutant sha256 | = case record |
|---|---|---|---|---|
| T8-1 | F1 (BROKEN path returns 0) | **KILLED**, exit 1, `FAIL (10/34 cases)` | `8eb8b805064949c49b0b265749b3a4cb71a0ade71f524a921e76a32ccf9a714b` | ✓ `sweep/results.tsv` |
| T8-1 | G1 (unknown arg fail-open) | **SURVIVED**, exit 0, `PASS (34 cases)` | `68fba490759b2e2cc6629758b5b4fff1f6f8c139e8b060f07d0764edd020bb55` | ✓ |
| T8-2 | D7 (cap `slice(0, 6)` → `5`) | **SURVIVED**, exit 0, `39/39 pass` | `f694e2328902b7a994396514910833733aee76ac5ae522208df36ea281ecad43` | ✓ `work/results.tsv` |
| T8-2 | D10 (candidate order swapped) | **KILLED**, exit 1, `37/39 pass` | `2c7fecd9ca8156ca1a968a66f9445c45a46bb05564f8e8357ae4e75677bfab75` | ✓ |

Controls (my runs, verbatim): T8-1 `CONTROL: GREEN (exit=0 …
pristine-sha256=7e5ec98b…)` + `CHECKLIST_SELFTEST: PASS (34 cases)`; T8-2
`CONTROL: GREEN (exit=0 … pristine-sha256=e9a21b44…)` + `CLAIMS_SELFTEST:
39/39 pass` / `VERDICT: PASS`. Both combined runs ended `MUTATE_RESTORE: OK
(before = after = the pin)` and `MUTATE: DONE … killed=1 survived=1
inconclusive=0` (50 % of the 2-defect cut, by construction). Wall: 6.1 s / 2.0 s.

Independent byte-identity (my own applier, not the tool): a single
`@old`→`@new` application on the pristine gave F1 = `8eb8b805…` and
D10 = `2c7fecd9…`; `cmp` against the harness-produced mutants in my workdirs →
identical. The recorded mutant bytes are reproducible from the spec plus the
pinned blob alone.

## 2. Pins, blobs, originals unchanged (O)

Commands (mine; run at open 19:14Z and re-run at close 19:25Z):

```
git -C kagi-shokunin     show fecee87:corpus/checklist-run.sh  | sha256sum  # 7e5ec98b…d576bf
git -C kumitate-shokunin show 175de6b:scripts/claims-check.mjs | sha256sum  # e9a21b44…b0f61b
```

| check | result |
|---|---|
| kagi blob `fecee87:corpus/checklist-run.sh` (object `78f2c45eed31ee00b01611556affa86a8db9c098`) | = live file = T8-1's copy = the pin |
| kumitate blob `175de6b:scripts/claims-check.mjs` (object `fae4bbcd158c527e70d8a69bcd3add372ed99c2e`) | = live file = T8-2's copy = the pin |
| kagi / kumitate `git status --porcelain` | 0 lines at open and at close |
| live targets re-hashed after all four re-runs | unchanged (both = their pins) |
| tameshi tree at close | the round's own writes only (`M SKILL.md`, `M fleet-kill-rate-ledger.md`, the two case notes, `plans/round-9.plan.md`, `reports/r8-ver-t8.md`) — no file of this audit |

So: **the originals are unchanged** — both gates are at their pins, read from
git blobs as well as from the working tree, and every copy in the two
producing lanes' scratch still hashes to its pin.

## 3. The 8 anchors (O; verified against the frozen note revisions)

| # | anchor | measurement | result |
|---|---|---|---|
| 1 | T8-1 pin cell | `git show` = live = lane copy = `7e5ec98b…`, 506 L / 24,697 B, mode 755 | MATCH |
| 2 | T8-1 control cell | `CHECKLIST_SELFTEST: PASS (34 cases)`, rc 0 — my run from the pinned copy | MATCH |
| 3 | T8-1 headline cell | `MUTATE: DONE … defects=15 killed=7 survived=8 inconclusive=0 kill-rate=47%`; survivors A1, B1, B3, C1, D1, E2, F2, G1 (note :84-87, :130-131, :182-189) | MATCH |
| 4 | T8-1 mutant cell | F1 `8eb8b805…` KILLED / G1 `68fba490…` SURVIVED — my re-runs = the lane's `sweep/results.tsv`, and byte-identical to my hand-applied mutants | MATCH |
| 5 | T8-2 pin cell | `git show` = live = lane copy = `e9a21b44…`, 925 newlines / 48,265 B, final byte `;` | MATCH |
| 6 | T8-2 control cell | `CLAIMS_SELFTEST: 39/39 pass` / `VERDICT: PASS`, rc 0 — my run from the pinned copy | MATCH |
| 7 | T8-2 headline cell | `MUTATE: DONE … defects=10 killed=7 survived=3 inconclusive=0 kill-rate=70%`; survivors D7, D8, D9 (note :62-63, :85-95) | MATCH |
| 8 | T8-2 mutant cell | D7 `f694e232…` SURVIVED / D10 `2c7fecd9…` KILLED — my re-runs = the lane's `work/results.tsv` and the note's §8 table; D10 = the recorded calibration miss (pre-registered SURVIVED, measured KILLED) | MATCH |

All 8 anchors match. The restore cells also reproduce: both the lanes' runs
and my re-runs carry `MUTATE_RESTORE: OK` with before = after = the pin.

## 4. Instrument pulse (supporting; my runs)

- `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 67/67 pass` /
  `VERDICT: PASS`, rc 0.
- `bash tools/mutate-and-run.sh --regression --workdir
  /tmp/w8-aud-t8-evidence/regression` → `REGRESSION: PASS (cases=4 passed=4;
  ledger legs exact: killed-delta<=0 flips<=0)`, rc 0, 46 s — the four
  recorded ledger legs (kimi-census 8/10, surface-census 8/10, tsukuroi-census
  6/10, mado-verify 4/10) each replayed from their pinned git blobs, `flips=0`.

## 5. Verdict table

| # | claim audited | verdict |
|---|---|---|
| 1 | T8-1's target sits at its pinned revision — from the git blob and the working tree alike | **CONFIRMED** |
| 2 | T8-1's control cell (34 cases, GREEN, rc 0) reproduces from the pinned bytes | **CONFIRMED** |
| 3 | T8-1's headline cell (7/15 killed, 47 %, survivors as listed) is what its evidence shows; my 2 re-runs reproduce their recorded verdicts and mutant shas | **CONFIRMED** |
| 4 | T8-2's target sits at its pinned revision — from the git blob and the working tree alike | **CONFIRMED** |
| 5 | T8-2's control cell (39/39, PASS, rc 0) reproduces from the pinned bytes | **CONFIRMED** |
| 6 | T8-2's headline cell (7/10 killed, 70 %, survivors D7/D8/D9, D10's recorded calibration miss) is what its evidence shows; my 2 re-runs reproduce their recorded verdicts and mutant shas | **CONFIRMED** |
| 7 | both "originals" (the two sibling gates) are unchanged by either case or by this audit | **CONFIRMED** |
| 8 | no fleet file was written by this audit beyond this report; both sibling trees were read-only throughout | **CONFIRMED** |

Not audited / not claimed: the 21 mutants I did not re-run (U3); the probe
(non-equivalence) outputs and per-case timing micro-values (U6); note edits
after the frozen revisions (U1).

## 6. Spot-checks (three, re-runnable)

- **SC1 — control cells.** `bash /tmp/w8-aud-t8-work/pristine-checklist-run.sh
  --selftest` → `CHECKLIST_SELFTEST: PASS (34 cases)`, rc 0; `node
  /tmp/w8-aud-t8-work/pristine-claims-check.mjs --selftest` →
  `CLAIMS_SELFTEST: 39/39 pass` / `VERDICT: PASS`, rc 0.
- **SC2 — pins.** `git -C kagi-shokunin show fecee87:corpus/checklist-run.sh |
  sha256sum` → `7e5ec98b…d576bf`; `git -C kumitate-shokunin show
  175de6b:scripts/claims-check.mjs | sha256sum` → `e9a21b44…b0f61b`; `cmp`
  each against the live file → identical.
- **SC3 — re-run pair.** The two 2-defect runs quoted in §1 (commands and full
  outputs retained at `/tmp/w8-aud-t8-evidence/{checklist2,claims2}.run.out`)
  reproduce KILLED/SURVIVED as in the table, with mutant shas equal to the
  cases' `results.tsv`.

## 7. Unknowns

- **U1 — note revisions in flight.** Both case notes were still being written
  during this audit (§0.1). The verdicts bind to the frozen hashes above; an
  edit after 19:25Z is not covered and needs a re-audit (append-only errata
  here).
- **U2 — single host, 2026-10-14** (bash 5.3.15, node v24.21.0, python 3.14.7);
  no cross-host reading for either rate or for the re-runs.
- **U3 — re-run coverage.** 4 of the 25 recorded mutants were re-executed here
  (2/15 + 2/10); the other 21 verdicts are the cases' recorded claims — their
  evidence files were read, not re-run.
- **U4 — spec provenance.** The defect sets are the case lanes' own specs, cut
  from their reading of each gate's contract; this audit reproduced the edits,
  not the defect-class derivation.
- **U5 — scratch volatility.** All my evidence lives under
  `/tmp/w8-aud-t8-{work,evidence}/`; /tmp is volatile, and the lanes' scratch
  (`/tmp/w8-tameshi-t81/`, `/tmp/w8-t8-2-claims/`) is theirs, untouched by me.
- **U6 — read, not re-measured:** the notes' survivor-probe (non-equivalence)
  outputs, their timing/cost cells, and the T8-2 note's §6 regression run (my
  §4 run reproduces the same PASS independently).

## 8. Errata (append-only)

(none yet — new entries go below this line, never edits above)