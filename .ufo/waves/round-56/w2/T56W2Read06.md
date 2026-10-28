# T56W2Read06 — cold read of `## Repeated controls and gate registry — round 12`

- Heading: `## Repeated controls and gate registry — round 12`
- Candidate revision (C0): `c0137451f5b7f22d65f748fc69f1b181f55e1378`
- Section span at C0: SKILL.md lines **1521–1540** (heading line through `non-secret fixture command before retaining evidence.`; line 1541 is the separate `### Gate/probe registry` heading, another seat's section)
- `section_sha256`: `3a78cbfcef65ada68c09342e5cbc71dc067d2b5258c3afbff6ea94e37a82b831`
- Sectionize: the **frozen** round-18 `sectionize` (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py`, blob sha256 `7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37` at C0), loaded with `importlib` against `git show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md`. The value was reproduced independently by hashing lines 1521–1540 of the C0 blob with trailing blank lines stripped (1436 bytes, 19 lines) — same digest.
- Class: record (a source pointer, a three-row decision table and a recipe). Every command the section tells a reader to run was executed in a `git clone --shared` scratch clone checked out at C0.
- Verdict: **gap-minor** — one finding (a stale in-tree pointer); all table rows and all recipe rules re-measured and confirmed true at C0.

## The section as read at C0 (lines 1521–1540)

```
## Repeated controls and gate registry — round 12

Source: S004 and S265 (S026 superseded by S265, `corpus/SOURCES.md:503`) and `corpus/knowledge/repeated-control-precondition.md`;
runtime evidence: `.ufo/evidence/round-12/verification-final.json`.
This is a standalone precondition check, not a change to the six-leg runner of round 12.

| Observation | Decision | Bound |
|---|---|---|
| Three or more zero-exit controls match on raw stdout and stderr | `controls_match` | Only this finite sample matched, on this host in this environment; not a determinism proof |
| All runs executed and any differ in exit or either stream | `controls_mismatch` | Do not attribute a later red suite solely to the mutant |
| Equal nonzero controls, or command unavailable | Could not evaluate baseline (`baseline_nonzero` / `command_unavailable`, exit 2) | No mutation kill-rate claim |

Recipe: choose a pristine command; put evidence outside any tree it inspects;
run `python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-UNIQUE -- COMMAND ARG...`;
retain raw observations before interpreting the finding. The output directory
must not exist. Caller owns timeout policy; hanging commands yield no verdict.
Do not retry until green, normalize output, or interpret a finite match as proof
of reliability. Command stdout/stderr may contain sensitive data: choose a
non-secret fixture command before retaining evidence.
```

## Finding 1 — `corpus/SOURCES.md:503` does not carry the supersession at C0

Quote (byte-exact, SKILL.md:1523 at C0):

```
Source: S004 and S265 (S026 superseded by S265, `corpus/SOURCES.md:503`) and `corpus/knowledge/repeated-control-precondition.md`;
```

Why: the parenthetical cites `corpus/SOURCES.md:503` as the record of the S026→S265 supersession. At C0 that line does not record it — it is a reserved-id bullet. The supersession sentence lives three lines further down, at `corpus/SOURCES.md:506`. The pointer therefore lands on exactly one of the two stale bullets that the supersession record itself disclaims.

Evidence (lane repo, read-only):

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/SOURCES.md | sed -n '503p'
- Next unused id: S265 (S261–S264 are map-only reserved; staged ids S161–S255 stay reserved by document for the package).

$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/SOURCES.md | sed -n '506p'
- Round 48: four rows added, S265-S268 (superseding held S026, S048, S093, S108; snapshots and receipts under `.ufo/evidence/round-48/freshness/sources/`). The two "Next unused id: S265" lines above were not updated in round 48; this line corrects them without rewriting.

$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/SOURCES.md | grep -n 'superseding held S026'
506:- Round 48: four rows added, S265-S268 (superseding held S026, S048, S093, S108; snapshots and receipts under `.ufo/evidence/round-48/freshness/sources/`). The two "Next unused id: S265" lines above were not updated in round 48; this line corrects them without rewriting.
```

Drift history — the anchor was correct when written and then moved:

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc8:corpus/SOURCES.md | sed -n '503p'
- Round 48: four rows added, S265-S268 (superseding held S026, S048, S093, S108; …)        <- 99c3bc8 wrote the anchor; correct here

$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1:corpus/SOURCES.md | sed -n '503p'
- Next unused id: S265 (staged ids S161–S255 stay reserved by document for the package).   <- already stale at the round-56 base
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1:corpus/SOURCES.md | sed -n '504p'
- Round 48: four rows added, S265-S268 (superseding held S026, …)

$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff -U0 99c3bc8 9cf0146 -- corpus/SOURCES.md | grep '^@@'
@@ -154,0 +155 @@ rows only, and a row is a claim opened in the round that writes it.
@@ -514 +515,3 @@ Round 52: one tier-A row added for the sourced C1 claim, S274 (Bazel documentati

$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff -U0 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 c0137451f5b7f22d65f748fc69f1b181f55e1378 -- corpus/SOURCES.md | grep '^@@'
@@ -155,0 +156,2 @@ rows only, and a row is a claim opened in the round that writes it.
@@ -517,0 +520,2 @@ Round 52: one tier-A row added for the sourced C1 claim, S274 (Bazel documentati
```

So the supersession sentence moved 503 → 504 (round-55 C0 `9cf0146`) → 506 (round-56 C0 `c013745`). The anchor was already stale at the round-56 base `981c5e8b`.

Scope of the defect: the **substance** is true of the tree at C0 — `corpus/SOURCES.md:140` carries the S265 row reading `supersedes S026's anchor and quote only`, `corpus/SOURCES.md:506` records the round-48 supersession of held S026, and `corpus/knowledge/repeated-control-precondition.md` opens with `S265 (supersedes S026)`. Only the cited locator is wrong, so the reader who follows the pointer lands on a bullet that contradicts the claim it was cited for.

Precedent: the round-54 wave-1 reader `T54W1Read11` filed the same defect on this same section (anchor `corpus/SOURCES.md:500`), and the round-54 fix pass `99c3bc8` moved it 500→503. The line has drifted again. **Deferred to round 57 by the L1; SKILL.md not edited here.**

## What the section asks, and what it actually does at C0

Every row of the decision table was exercised against the tool at C0 (scratch clone, `$HYAKU_SCRATCH` outside every inspected tree):

| Section row | Command run at C0 | Observed |
|---|---|---|
| three or more zero-exit controls match → `controls_match` | `python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-T56W2Read06-r3 -- /bin/echo hello` | `REPEAT_COMPARE identical=yes runs=3` · `REPEAT_CONTROL: controls_match` · exit 0 |
| (same row, N>3) | `python3 tools/repeat-control.py --runs 5 --out $HYAKU_SCRATCH/tameshi-r12-controls-T56W2Read06-r5 -- /bin/echo five` | `REPEAT_COMPARE identical=yes runs=5` · `REPEAT_CONTROL: controls_match` · exit 0 |
| any difference in exit or either stream → `controls_mismatch` | `python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-T56W2Read06-mm -- /bin/sh -c 'echo $((RANDOM))'` | `REPEAT_COMPARE identical=no runs=3` · `REPEAT_CONTROL: controls_mismatch` · exit 1 |
| (same row, differing exit) | `python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-T56W2Read06-me -- /bin/sh -c 'exit $((RANDOM%3+1))'` | `REPEAT_COMPARE identical=no runs=3` · `REPEAT_CONTROL: controls_mismatch` · exit 1 |
| equal nonzero controls → `baseline_nonzero`, exit 2 | `python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-T56W2Read06-bn -- /bin/sh -c 'echo boom; exit 3'` | `REPEAT_RUN 1..3 exit=3` · `REPEAT_CONTROL: baseline_nonzero` · exit 2 |
| command unavailable → `command_unavailable`, exit 2 | `python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-T56W2Read06-cu -- /nonexistent/cmd` | `REPEAT_RUN 1..3 exit=unavailable` · `REPEAT_CONTROL: command_unavailable` · exit 2 |

Recipe rules, all confirmed at C0:

- **Output directory must not exist** — a second run on an existing `--out` is refused and never overwrites: `repeat-control: --out already exists (refused, never overwritten)` · `REPEAT_CONTROL: invalid_usage` · exit 64. The tool's own selftest asserts `invalid-existing-out PASS (expected=invalid_usage/64 observed=invalid_usage/64 refused-out-untouched)`.
- **The floor of three runs** — `--runs 2` is refused: `repeat-control: --runs must be >= 3, got 2` · exit 64.
- **Caller owns timeout policy; hanging commands yield no verdict** — `timeout 10 python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-T56W2Read06-hang -- /bin/sleep 300` produced no `REPEAT_CONTROL:` line and no `finding.txt` in the evidence dir; the caller saw exit 124. The tool itself declares `there is no timeout and no process supervisor` (`tools/repeat-control.py:84-87`) and carries no signal/alarm/kill code.
- **Do not retry until green, normalize output** — the tool contains no retry path and compares unnormalized bytes; the selftest case `mismatch-newline-only PASS` proves a trailing-newline difference is a mismatch, and `mismatch-stderr PASS` proves stderr is compared too.
- **Do not interpret a finite match as proof of reliability** — the tool's own docstring says a clean `controls_match` `is not a determinism proof and it cures no flakiness`, matching the table's Bound column.
- **`--selftest`** — `python3 tools/repeat-control.py --selftest` → `SELFTEST: PASS (29 cases)`, exit 0.
- **Committed snapshots replay** — `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate` → `SNAPSHOT_EXPECTED id=controls_match exit=0` / `SNAPSHOT_OBSERVED id=controls_match exit=0`, exit 0; `--snapshot .ufo/evidence/round-12/ControlGate/mismatch` → `controls_mismatch`/1, exit 1.

Pointers that resolve at C0:

- `S004` → `corpus/SOURCES.md:15` (row present; used-by `corpus/knowledge/repeated-control-precondition.md`).
- `S265` → `corpus/SOURCES.md:140` (row present; `supersedes S026's anchor and quote only`; used-by the same note).
- `corpus/knowledge/repeated-control-precondition.md` → present at C0 (14,142 B).
- `.ufo/evidence/round-12/verification-final.json` → present at C0; `passed: true`; checks include `repeat-control-selftest` (`SELFTEST: PASS`), `frozen-match` (`controls_match`), `frozen-mismatch` (`controls_mismatch`), `real-pristine-three-controls` (`controls_match`) and `runner-six-leg-regression` (`REGRESSION: PASS`).

## Notes (improvements, stale-but-true, style — not findings)

1. **"the six-leg runner of round 12"** is true as a round-12 statement, but the tree's runner at C0 has ten legs (`tools/mutate-and-run.sh:84`: `r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten`) and sha256 `977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda`, not the round-12 pin `75ed934d…`. The adjacent `### Gate/probe registry` section carries the round-27 staleness correction, so this section is not self-contained here but is not false.
2. **The cited knowledge note is stale about the very tool the section names.** `corpus/knowledge/repeated-control-precondition.md:58` states `tools/repeat-control.py exists: 30,557 B, sha256 29d8025490f349c106bc8132da7bfecc2ae4f8fb00720b43636e52335d27467a` and locates `the finding map :115-123, the precedence :191-205, the snapshot validator :337-435, the selftest :545`. At C0 the tool is **36,950 B**, sha256 `a8fad68fcbb87d03fb7e5e22fb1f70bd94d36c857a1c4b58171d91b042df80fd`; `EXIT_BY_ID` is at `:122-130`, `classify()` at `:238`, `snapshot_mode()` at `:481`, `selftest()` at `:624`. The note has a `## Round 16 note (append-only)` erratum for the runner pin but none for the round-53/round-55 tool edits. The note's finding→exit→class table itself is still correct (every row re-measured above).
3. **`HYAKU_SCRATCH` unset.** The recipe's bare `$HYAKU_SCRATCH/...` expands to `/tameshi-r12-controls-UNIQUE` when the variable is absent, and the gate refuses: `repeat-control: setup: cannot create --out /tameshi-r12-controls-T56W2Read06-unset: [Errno 13] Permission denied` · `REPEAT_CONTROL: setup_error` · exit 2. The standing rules give the scratch root a default (`/fast/scratch/hyaku`, SKILL.md:28 and :164) but the recipe does not use it; `${HYAKU_SCRATCH:-/fast/scratch/hyaku}` would make the recipe self-contained.
4. **Scratch-path shape.** The recipe's `tameshi-r12-controls-UNIQUE` is a dash-form flat directory under the scratch root, while SKILL.md:28/164 prescribe `$HYAKU_SCRATCH/<lane>-r<round>/<sub>/` and say the dash form "survives only in run artifacts and quoted text of rounds 37-52, not as a live convention".
5. **Refusal exit code unnamed.** "The output directory must not exist" is stated without its code; measured 64 (`invalid_usage`), matching the tool's `invalid-existing-out` selftest case.
6. **Historical receipt.** `.ufo/evidence/round-12/verification-final.json` records `tool_sha256 296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25`, not the C0 tool's sha — expected for a round-12 receipt, and the section does not assert it as current.
7. **Census.** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` exits 0 at C0 (W01/W04 advisories plus `tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`). The lane row count is **142** at C0 — 140 at base `981c5e8b`, plus `S281` and `S282` added by round-56's C0 — not the 141 named in this seat's brief.

## Commands run (all against the C0 scratch clone unless stated)

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/SOURCES.md | sed -n '503p'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/SOURCES.md | sed -n '506p'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/SOURCES.md | grep -n 'superseding held S026'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff -U0 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 c0137451f5b7f22d65f748fc69f1b181f55e1378 -- corpus/SOURCES.md
python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-T56W2Read06-r3 -- /bin/echo hello
python3 tools/repeat-control.py --runs 5 --out $HYAKU_SCRATCH/tameshi-r12-controls-T56W2Read06-r5 -- /bin/echo five
python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-T56W2Read06-mm -- /bin/sh -c 'echo $((RANDOM))'
python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-T56W2Read06-me -- /bin/sh -c 'exit $((RANDOM%3+1))'
python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-T56W2Read06-bn -- /bin/sh -c 'echo boom; exit 3'
python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-T56W2Read06-cu -- /nonexistent/cmd
python3 tools/repeat-control.py --selftest
python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate
python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch
timeout 10 python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-T56W2Read06-hang -- /bin/sleep 300
env -u HYAKU_SCRATCH bash -c 'python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-T56W2Read06-unset -- /bin/echo x'
sha256sum tools/repeat-control.py tools/mutate-and-run.sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

Raw receipts: `.ufo/waves/round-56/w2/T56W2Read06-receipts/` (01 section text at C0 · 02 anchor · 03 table cells · 04 recipe rules · 05 tool behaviour · 06 anchor drift cause · 07 cross-checks).

Scratch: `/fast/scratch/hyaku/tameshi-r56/T56W2Read06` (clone at C0), removed on exit. No lane production file and no frozen instrument was edited; no mutating git or jj command was run anywhere.
