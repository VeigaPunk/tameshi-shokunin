# CriticSHONENRestraint — SHONEN.md + r37 records restraint check

Seat: critic (calibration), round 37 wave 1, leaf — read-only review; the only write is this report. Judged on: calibration. Milestone: SHONEN restraint.

Scope interpretation: no fleet round-37 lane report exists yet (`ls /home/vgpnk/Projects/shokunin/.ufo/reports/round-37/` → chousa, kake, kotodama, kumitate, mori only; no `tameshi.md`), so "the r37 report" is checked as the lane's committed r37 records: `LOG.md:1943-1995`, `SCORECARD.md` r37 section (commit `e6185d5`), `corpus/lessons/round-37.md`, `corpus/QUALITY.md` criteria 73-75, `corpus/SOURCES.md` S104 block — plus all r37 seats landing in `.ufo/waves/round-37/w*/`.

## Verdict

**PASS on both criteria; two minor findings.** All four SHONEN boxes remain `[~]` with resolvable evidence; zero `[x]` anywhere in SHONEN.md or the r37 records; no box or record claims an independent/non-author verifier, so nothing claims tameshi-dispatched work as independent.

## Evidence

### Marks and pointers (HEAD `e6185d5`)

- `SHONEN.md` is 12 lines; box lines 5, 7, 9, 11 all `[~]`. `grep -c '\[x\]' SHONEN.md` → `0`. Same census in r37 records: `grep '\[x\]'` on `corpus/lessons/round-37.md`, `LOG.md:1943-1995`, `SCORECARD.md` r37 diff → no marks (only rubric text quoting the criterion).
- Pointer resolution, run from lane root:
  - `reports/round-1-calibration.md` anchors resolve: `## box-1` :71, `## box-2` :105, `## box-4` :167 (each once). Boxes 1/2/4 pointers valid.
  - Box 3 pointer `.ufo/evidence/round-21/coldread/ledger.json` exists (3.5 MB, valid JSON, `schema: tameshi-coldread-ledger-v2`, 497 entries).
  - Box-3 "input-keyed monitor only" holds: `sha256sum SKILL.md` → `23818731…` which is present in the ledger's `skill_sha256` set (refreshed Oct 24 03:16), so the ledger is keyed to the live SKILL.md, not a stale input.
- `git log d9c496b..HEAD -- SHONEN.md` → empty: no mark flipped or silently edited during r37.

### Verifier independence

- `SHONEN.md:6,8,10,12` parentheticals explicitly disclaim independence ("lane assertion, no independent promotion verifier" / "input-keyed monitor only"). No r37 record asserts an independent verifier.
- Historical `[x]` marks named TAMESHI-B1/B2/B3, which `reports/round-1-calibration.md:206-209` records as lane-dispatched and downgraded to `[~]`/`[ ]` — the correct treatment; nothing in r37 restores them.

### r37 record honesty vs receipts (no unsupported claims)

- `calibration/before-final-control.stdout` (exit 1): `unresolved_control_inputs=1 … rev=d9c496b… C1_R37_PASS=false` — matches LOG:1961-1964 and contract before.
- `calibration/after-control-final.stdout` (exit 0): `unresolved_control_inputs=0 correction=1 manifest_ok=1 receipts_ok=1 rev=32826f37… C1_R37_PASS=true` — matches LOG:1965.
- `control/replay-at-final-control.stdout`: `mode=control`, `EMPTY_PANEL_REPLAY … empty_specimens=0 … v1_pass=1 v2_reject=1 … PASS=true` — matches the claimed v1 PASS / v2 FAIL.
- `code-view/before.stdout` (exit 1): escaped-quote case FAIL, literal-hash PASS = "1/2". `code-view/after.stdout` (exit 0): both PASS, `C2_R37_PASS=true`, `tool_sha256=da8c1ef4…` = pin in `counter-pin.json`. Selftest `35/35` confirmed (tail of `tool-selftest-after.stdout`).
- Pin discipline holds: `counter-pin.json` committed at `235608a`, before tool commit `ae9b771`; `c2-repin-after.stdout` exit 0.
- Restraint kept: SCORECARD r37 section claims "no numeric restraint-score move" and "numeric depth remains 9" — no SHONEN axis inflation.
- `SOURCES.md` row discipline: `Next unused id: S105` appended; rows 100 → 101 confirmed by `grep -c '^| S[0-9]' corpus/SOURCES.md` → `101`.

## Findings (minor; neither breaks a mark or pointer)

1. **LOW — dangling forward pointer.** `corpus/lessons/round-37.md:11` says "see the round-37 report for the start and end `sources-census.sh validate` stdout and exit codes," but `.ufo/reports/round-37/` contains no `tameshi.md` yet; `.ufo/waves/round-37/w1/` and `w2/` currently hold only `swarm-registry.json`. The data itself is committed (`.ufo/evidence/round-37/census/{start,end}.*`, summarized at `LOG.md:1986-1989`), so resolution is pending, not false. **Smallest safe correction:** when the r37 lane report lands it must embed the census start/end stdout+exits and the row-count command; if no report is produced, repoint lesson :11 to `LOG.md:1986-1989` + `.ufo/evidence/round-37/census/`.
2. **LOW — carried-over stale trail (r36 W2 F2, not cured by r37).** `reports/round-1-calibration.md` `## box-3` (:132 "Why `[ ]` — no lane assertion at all", :165 "remain unearned", dispositions :208 `[ ] (assertion rejected)`) still contradicts `SHONEN.md:9`'s `[~]`; last file change was `cd31c6b`, no r37 erratum. Box 3's pointer correctly goes to the ledger rather than `#box-3`, so the `[~]` stays resolvable, but a reader following the box-3 anchor inside the audit file meets the opposite verdict. **Smallest safe correction:** one append-only erratum in `reports/round-1-calibration.md` noting the later `[~]` + ledger-keyed monitor credit (optionally a pointer annotation on `SHONEN.md:10`).

## Non-findings checked

- `census/end.stdout` prints `S104 duplicate url … across scopes` yet `ok` + exit 0 — a validator warning, disclosed in the receipt; not a defect.
- SCORECARD's "strict no-harm monitor result is reported separately" does not claim a score; nothing unsupported.

Tooling: no installs performed; all checks used git/grep/sha256sum/python3 already present.
