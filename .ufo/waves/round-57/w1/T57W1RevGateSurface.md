# T57W1RevGateSurface — receipt-revision-gate exit-code and code table, by execution

Base: `5e3569969b532310d2b8a3d130901757a3df356b`. Gate `tools/receipt-revision-gate.py` (359 lines, sha256 `c60772ce…0569ac9`) is byte-identical to base. No lane file edited; no install; the gate ran read-only (git objects only). Python 3.14.8 and git 2.56.0 were used as found.

Result: all 11 codes are reachable; none is dead. Exit 0 / 2 / 3 are as the executor report says, but the map is incomplete: exit 1 also exists (usage and uncaught tracebacks). The header docstring, the SKILL standing-rules row 53 and registry row 1278 each disagree with the executed gate (D1–D3 below). Full machine-readable table: `T57W1RevGateSurface.json`. Receipts: `T57W1RevGateSurface-receipts/` (driver `drive.sh`, outputs `fixture-out/`, extra cases `extra-cases.txt`, emission scan `emission-scan.txt`, fixture SHAs `fixture-revs.txt`).

## 1. Method
- Scratch fixture repo under `/fast/scratch/hyaku/tameshi-r57/T57W1RevGateSurface/fixture.hpi9`, fixture identity, `git -C "$D" rev-parse --show-toplevel` asserted equal to `$D` before commits. History: c0 (surface/other/moved = alpha) → c1 (moved=gamma) → c2 (other=delta); side branch off c0 (side.txt). Receipts name these revs.
- 44 invocations (`drive.sh` cases 01–36 and extra 37–44). Every exit path and every code was observed; emission lines were located by a source scan (`emission_scan.py`).
- The gate's own `--selftest` run: `GATE_SELFTEST: 19/19 pass`, rc 0 (case 33). Its 19 cases cover all 11 codes.

## 2. Exit paths (order of checks in `run()`)
Order: argv parse (170–185) → required args (186–188) → **certified resolve (190–194, exit 2)** → `--paths` read (196–198) → `parse_receipts` (201) → per-receipt check → verdict (220).

| exit | emitted at | condition | fixture cases (rc observed) |
|---|---|---|---|
| 0 | 220 `return 0 if verdict == 'PASS'` (also 358 for `--selftest` 19/19) | every receipt ok | 01, 02, 09, 17, 31, 36, 38, 39, 33 (all rc 0) |
| 3 | 220 | ≥1 receipt refused; `GATE: … codes=<named>` | 03–16, 21, 23, 29, 30, 37 (all rc 3) |
| 2 | 190–194 `GATE: error=unresolvable-certified … codes=RECEIPT_REV_UNRESOLVABLE` | `--certified` does not resolve, **or the lane is not a git repo / does not exist**; runs before receipts are parsed | 18, 19, 20, 32, 42 (all rc 2) |
| 1 | 92 (bad ROLE), 183–184 (unknown flag / positional), 187–188 (missing required), 358 with no-args | usage via `SystemExit(str)`; no named code | 24, 25, 26, 28, 34, 35 (all rc 1) |
| 1 | uncaught: 173/175/177/179 `IndexError` (flag with no value); 197 `FileNotFoundError`/`UnicodeDecodeError` (`--paths`); 106 `PermissionError` (not tested) | traceback; no named code, no usage text | 22, 27, 43 (all rc 1) |

There is no argparse. Exit 2 is reached only by an unresolvable `--certified` or lane. The usage exit is 1, not 2.

## 3. Code table (11 codes)
`mode` = whether the code can fire only with `--paths`, only without, or in both.

| code | emit line(s) | roles | mode | fixture case(s) → observed |
|---|---|---|---|---|
| RECEIPT_MISSING | 103 | all | both | 14 → rc 3 |
| RECEIPT_EMPTY | 108 | all | both | 15 → rc 3 |
| RECEIPT_NOT_BLOB | 105 | all | both | 16 (directory), 29 (empty path `:positive` → `.`) → rc 3 |
| RECEIPT_REV_ABSENT | 126 | all | both | 05 → rc 3; 30 (6-hex `rev=`) → rc 3, detail "no rev= token" (D12) |
| RECEIPT_REV_AMBIGUOUS | 141 | positive, verdict | both | 06 (two commits) → rc 3; 07 (one commit, abbrev+full) → rc 3 (D11) |
| RECEIPT_REV_UNRESOLVABLE | 133 (receipt rev, exit 3); 192 (certified rev, exit 2) | all | both | 08, 11 → rc 3; 18, 19, 20, 32, 42 → rc 2 |
| **RECEIPT_REV_MISMATCH** | 146 | positive, verdict | **only without `--paths`** (`paths is None`, 145) | 04 → rc 3; 23 (`--paths ""`, treated as absent) → rc 3 |
| **RECEIPT_REV_CONTENT_DRIFT** | 151 | positive, verdict | **only with `--paths`** (145 else-branch) | 03 → rc 3 (`drift=moved.txt`); 21 (empty paths file) → rc 3; 37 (listed path absent in both revs) → rc 3 |
| RECEIPT_CONTROL_NOT_ANCESTOR | 158 | control | both | 10 → rc 3 |
| RECEIPT_DIGEST_MISMATCH | 120 | all | both | 12 → rc 3 |
| RECEIPT_REQUIRED_LINE_MISSING | 123 | all | both | 13 → rc 3 |

- Reachable **only under `--paths`**: `RECEIPT_REV_CONTENT_DRIFT`.
- Reachable **only without `--paths`**: `RECEIPT_REV_MISMATCH`.
- Reachable in both modes: the other nine.
- **Unreachable (dead) codes: none.** The `drifted_paths` empty-list branch (76–77) is reachable, through an empty `--paths` file, but its message is wrong (D6).
- The `CODES` tuple (46–49) and the docstring (26–29) list exactly the 11 emitted names; the scan found no emitted name outside `CODES`.

## 4. Discrepancies
Severity: high = the SKILL or registry text would tell an operator something false; medium = behaviour or message misleads; low = hygiene or edge.

**D1 (high) — SKILL.md line 53, verdict row, code cell is wrong.** The row says a verdict receipt on the declared `--paths` surface is refused with `RECEIPT_REV_MISMATCH`. Executed: with `--paths` and drift the gate emits `RECEIPT_REV_CONTENT_DRIFT` (03, 37); with identical bytes it passes (02); `RECEIPT_REV_MISMATCH` appears only without `--paths` (04, and extra-40 with `--paths` removed). Fix: cell → `RECEIPT_REV_CONTENT_DRIFT` with `--paths`; `RECEIPT_REV_MISMATCH` without. This is the R56.2 cell.

**D2 (high) — "each a named refusal, exit 3" is false.** Header docstring line 25 and registry row 1278 (`scratch_root`) say every refusal exits 3. `RECEIPT_REV_UNRESOLVABLE` for `--certified` exits 2 (18, 19, 20, 32, 42).

**D3 (high) — the documented exit map is incomplete.** Docstring line 32 documents only "Exit 0 iff PASS". Exit 2 (D2) and exit 1 (usage and tracebacks: 22, 24–28, 27, 34, 35, 43) are undocumented. The executor's proposed registry map `0 PASS; 2 …; 3 …` would be wrong by omission; it must add `1 usage or uncaught error (no named code)`.

**D4 (medium) — verdict-line form and `--json` on the exit-2 path.** Docstring line 31 gives `GATE: receipts=N ok=N refused=N codes=… verdict=…`. The exit-2 path prints `GATE: error=unresolvable-certified receipts=N verdict=REFUSED codes=…` (193) and ignores `--json` (19 prints text, not the `tameshi-receipt-gate-v1` schema).

**D5 (medium) — code comment at 153–154 is false.** It says a content-identical revision "is accepted, and the line says so". The OK line (case 02) reads `GATE OK … role=positive revs=<other rev>` with no marker that the revision differs from the certified one.

**D6 (medium) — empty `--paths` file gets a false message.** Lines 76–77 return `<no --paths given: content identity is not checkable>` when the list is empty. Case 21 reaches it (the file was given, with only comments), yielding `RECEIPT_REV_CONTENT_DRIFT` rc 3. Should be a usage error or could-not-evaluate. The executor report found the same behaviour.

**D7 (low) — `--paths ""` is silently strict.** Line 196 (`if paths:`) drops an empty value; case 23 gives `RECEIPT_REV_MISMATCH` rc 3 with no usage error.

**D8 (low) — a lane failure is named as a revision failure.** A nonexistent or non-git `--lane` gives `RECEIPT_REV_UNRESOLVABLE` rc 2 (20). The code names the revision; the lane is what is wrong. Undocumented.

**D9 (medium) — check order decides the exit code.** Certified resolution (190–194) precedes `parse_receipts` (201) and the `--paths` read (197). An unresolvable `--certified` hides a bad ROLE (32: rc 2, not 1) and a missing `--paths` file (42: rc 2, not a traceback). A bad ROLE with a resolvable certified gives rc 1 (25). Undocumented.

**D10 (medium) — parser errors escape as tracebacks, not named refusals.** A flag with no value (27, 43: `IndexError` 173–179), a missing `--paths` file (22: `FileNotFoundError` 197) and an unreadable receipt or paths file (106, untested) exit 1 with no named code and no usage message. Docstring line 25 says codes are the named refusals.

**D11 (medium) — ambiguity is per token string, and inconsistent by role.** Line 140 compares `len(revs)`, the set of token strings (not resolved commits). A commit named as abbreviated and full sha is `RECEIPT_REV_AMBIGUOUS` for positive/verdict (07) but PASS for control (extra-41). `resolved{}` (129–136) is computed and unused for this check. Docstring line 16 ("Exactly one distinct `rev=` token") matches the token reading; the two roles still disagree.

**D12 (low) — short revisions are invisible.** `REV_RE` (43) needs 7–40 hex. `rev=abc123` gives `RECEIPT_REV_ABSENT` with detail "no rev= token" (30), which misdescribes a too-short revision. SKILL row 56 ("names no revision at all") does not cover it.

**D13 (low) — colon in PATH.** `split(':', 2)` (90) makes `a:b.txt:positive` a usage error rc 1 (28). Header line 12 does not mention it.

**D14 (low) — stale comment in source.** Lines 109–111 contain an unfinished self-correction ("…must be a blob at the certified revision's tree? No:"). Hygiene only.

Verified consistent (no discrepancy): the role rules in docstring lines 16–23 match code 139–160 (positive/verdict equality or drift; control ancestry; control resolves every token); docstring codes 26–29 equal `CODES`; "Stdlib only" holds (imports are stdlib); "read-only" holds for the non-selftest path (git `rev-parse`, `merge-base`, `diff`, `cat-file`; receipts read).

## 5. Agreement with T57W1ExecStandingRules.md
I reproduced its 8 truth-table rows (verdict/positive × absent/given × R2/R3) and its extra rows (paths-empty → DRIFT; certified unresolvable → exit 2; receipt rev unresolvable → exit 3; no rev → ABSENT). Its fixture (R1/R2/R3, drift on `surf.txt`) differs from mine (c0/c1/c2, drift on `moved.txt`), so the rows are matched by semantics, not bytes: the gate takes the same branch for verdict and positive (line 139, `role_name in ('positive','verdict')`). Mine show: identical-bytes with `--paths` → PASS (02, extra-40); drift with `--paths` → DRIFT (03); strict without `--paths` → MISMATCH (04, extra-40); paths-empty → DRIFT (21); certified unresolvable → exit 2 (18); receipt rev unresolvable → exit 3 (08). All 8 of its rows agree in semantics. I confirm its edit 1 (row 53 code cell, D1) and its edit 2 (row 55 exit note). I add: D2/D3 (its registry row and map are incomplete, and the existing row 1278 still says exit 3 everywhere), D5, D7–D14.

## 6. Input for the C2 counter and SKILL cell
- Exit map to judge against: `0` PASS; `1` usage error or uncaught exception (no named code); `2` `--certified` or lane unresolvable; `3` refused with named codes.
- SKILL row 53 code: `RECEIPT_REV_CONTENT_DRIFT` with `--paths`, `RECEIPT_REV_MISMATCH` without.
- Named codes per mode: only-with-paths `RECEIPT_REV_CONTENT_DRIFT`; only-without-paths `RECEIPT_REV_MISMATCH`; 11 codes total; none dead.

## 7. Not verified (honest gaps)
- Unreadable receipt or paths file (`PermissionError`, line 106) not run (no fixture permission change).
- The `--selftest` TMPDIR-unusable fallback was observed once (extra-44: `GATE_SELFTEST: 19/19 pass`, rc 0) but not analysed; it is not in this item.
- The gate was not run on any real round-56 receipt.
- Fixture commands use `drive.sh` with absolute scratch paths; they are reproducible only with those paths present.

## 8. Receipts
`T57W1RevGateSurface-receipts/`: `drive.sh` (driver), `fixture-out/*.out|*.err` and `rc-table.txt` (cases 01–36), `extra-cases.txt` (extra 37–44), `emission-scan.txt`, `emission_scan.py`, `fixture-revs.txt`, `fixture-path.txt`, `rcpt/` (receipt inputs).

Scratch `/fast/scratch/hyaku/tameshi-r57/T57W1RevGateSurface` removed after the receipts were copied.
