# Cold-read report — `### Round-17 gate/probe registry — re-pin and monitor`

- Seat: T54W1Read20 (reader, round 54 wave 1)
- Heading: `### Round-17 gate/probe registry — re-pin and monitor`
- Cand: `59c38109bf119d0e9d4f878644a82babc937bc1e`
- Section: lines 1872–1879 (8 lines; `reader-section.py` printed start=1872, end=1880)
- `section_sha256`: `8a92f71e046aae243294c42153c6ed183ccd41edf4647ff9520e35a26b9c9643`
  (recomputed over the frozen round-18 `sectionize()` body: heading through the row before the next heading, trailing blank lines stripped, no trailing newline — 1119 bytes, sha matches)

Reader command (scratch `TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1Read20/`):

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && \
  python3 .ufo/waves/round-54/reader-section.py \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    59c38109bf119d0e9d4f878644a82babc937bc1e \
    "### Round-17 gate/probe registry — re-pin and monitor"
```

Output:

```
{"heading": "### Round-17 gate/probe registry \u2014 re-pin and monitor", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 1872, "end": 1880, "section_sha256": "8a92f71e046aae243294c42153c6ed183ccd41edf4647ff9520e35a26b9c9643"}
```

All reads below are of `git show 59c38109bf119d0e9d4f878644a82babc937bc1e:<path>` bytes, never a working-tree read. Executions ran against `git clone --shared` at C0 under `/fast/scratch/hyaku/tameshi-r54/T54W1Read20/`; the clone was removed at the end.

## Findings (1)

### F1 — the delegated round-13 verdict map is stale at C0 for `pin-disposition.py --selftest`

Quote (byte-exact in the section):

> as the round-13 row

Why: The delegated round-13 verdict map (`SKILL.md:1577`, quoted below) ends at "selftest 1 failed", but at C0 `python3 tools/pin-disposition.py --selftest` also exits 2 with a naming could-not-evaluate line when `TMPDIR` is set and unusable — the arm this same commit records in its own `pin-disposition-selftest` registry row and in the `## Standing rules` bullet at `SKILL.md:32-38` — so the delegated exit cell understates the selftest's exit set.

The delegating cell under test (`SKILL.md:1879`):

```
| `tools/pin-disposition.py` (branch tip) | probe | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` · `--selftest` | as the round-13 row |
```

The row it cites (`SKILL.md:1577`, "Verdict map" column):

```
0 observations, including changed/unavailable; 2 invalid input/could-not-evaluate; selftest 1 failed
```

Evidence that the selftest has a third external exit at C0 (receipts below):

- `TMPDIR=<usable dir> python3 tools/pin-disposition.py --selftest` → exit **0**, `SELFTEST: PASS (19/19)`.
- `TMPDIR=<set but missing dir> python3 tools/pin-disposition.py --selftest` → exit **2**,
  `pin-disposition.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<dir>' (could-not-evaluate)` — a naming line with no traceback, i.e. exactly the class `corpus/knowledge/scratch-root-contract.md` made uniform at C0.
- C0's own `tools/registry.json` `pin-disposition-selftest` row now carries
  `"scratch_root": "TMPDIR set but unusable => exit 2, could-not-evaluate (the value is named, no traceback); TMPDIR empty => unset, the platform default applies; a usable TMPDIR holds every mkdtemp and nothing is created under /tmp (round 54, corpus/knowledge/scratch-root-contract.md)"`,
  so the SKILL.md table is behind the lane's own registry row at the same commit.
- C0's standing rule (`SKILL.md:32-38`) states the same for the seven `strict_scratch_root()` tools: "set but unusable → exit 2, could-not-evaluate, naming the value".

Fix is one cell: the round-13 verdict map (or the delegating cell) should say the selftest also exits 2 (could-not-evaluate, unusable `TMPDIR`) — reported here, not fixed.

## What I opened

- `SKILL.md` at C0, section bytes lines 1872–1879 (the four-row table and its header), plus context: `:32-38` (the new scratch-root standing rule), `:1577` (round-13 row), `:1836` (round-16 row), `:1866-1870` (the commands immediately above the section), `:1881-1886` (the section that follows).
- `tools/evidence-disposition.py` at C0: docstring, `USAGE` (`:167-185`), `parse_argv`/`main` (`:3195-3260`), the G4 identity guard (`:434-470`), and the C0 `strict_scratch_root()`/`ScratchRootUnusable` edit (`:195-230`).
- `tools/registry-check.py` at C0: docstring interface and exit map (`:1-83`), `USAGE` (`:118-120`), the `--tag`/`--only` evaluation-error returns (`:863-885`).
- `tools/pin-disposition.py` at C0: `USAGE` and exit map (`:148-158`), `strict_scratch_root()` (`:165`), selftest entry (`:725`).
- `tools/mutate-and-run.sh` at C0: exit map (`:139-143`), repo-identity guard and its `SETUP (repo_identity_mismatch: ...)` line (`:1249-1263`), selftest fixture asserting exit 2 for that refusal (`:1944-1946`).
- `tools/registry.json` at C0: every row for the four tools this section lists; the seven rows carrying `scratch_root` (`repeat-control-selftest`, `bash-witness-selftest`, `pin-disposition-selftest`, `evidence-disposition-selftest`, `context-capture-selftest`, `registry-check-selftest`, `env-diff-selftest`).
- `.ufo/evidence/round-18/measure.py` at C0: `sectionize()` (`:209-253`), to reproduce the printed `section_sha256` exactly.
- `.ufo/evidence/round-54/c1/measure.py` (docstring arms) and `.ufo/evidence/round-54/c1/lost-headings-at-c0.json` (my heading is in the 23).
- `corpus/knowledge/scratch-root-contract.md` (C0, 60 lines).

## What I checked, and cleared

1. **Row 1, `tools/evidence-disposition.py` (v2 manifests).** Command `--root . --dispositions .ufo/evidence/round-18/dispositions.json --json` → exit **0**, `"status": "clean"`. The parenthetical "(round 18; the round-17 manifest now exits 2)" is true at C0: the same command with `.ufo/evidence/round-17/dispositions.json` → exit **2**, `expected_input_digest_mismatch` on `tools/bash-witness-study.py`. Both manifests exist at C0. The exit cell's four arms match the tool's `USAGE` ("0 clean / 1 failed semantic expectation / 2 could-not-evaluate bad/missing/tampered input / 64 usage error"). `--selftest` → exit **0**, `SELFTEST: PASS (66/66)`.
2. **Row 2, `tools/registry-check.py`.** Docstring interface contains every flag the cell lists (`--rev`, `--registry`, `--tag`, `--json`, `--selftest`) and the 0/1/2/64 map the cell states. `--rev <unresolvable>` → exit **2** (`REGISTRY_CHECK: could-not-evaluate (rev '000…0' unavailable in .)`), matching the cell's "rev unresolvable". `--selftest` → exit **0**, `SELFTEST: PASS (51 cases)`.
3. **Row 3, `tools/mutate-and-run.sh`.** "as the round-16 row" resolves: `SKILL.md:1836` gives "selftest 0 pass / 1 fail; regression 0 PASS · 1 FAIL · 2 SETUP · 64 usage". "a borrowed repo identity is SETUP 2" is anchored at `tools/mutate-and-run.sh:1252-1263` (`repo_identity_mismatch` → `SETUP`, regression exit 2) and its own selftest asserts that exit at `:1944-1946`. Unusable `TMPDIR` runs it to "VERDICT: FAIL (mktemp)", exit **1** — within the delegated "selftest 0 pass / 1 fail", so no drift there.
4. **Row 4, `tools/pin-disposition.py` (branch tip).** The documented invocation prints exit **0**, `status: ok`, `counts: {legs: 6, unchanged: 1, changed: 5, unavailable: 0}` — exit 0 "including changed" exactly as the round-13 verdict map says. `.ufo/evidence/round-13/pin-manifest.json` exists at C0. The `--selftest` arm is cleared at exit 0 / `SELFTEST: PASS (19/19)`; only the new unusable-`TMPDIR` arm (F1) is not in the delegated map.
5. **Self-contradiction inside the section.** None found: row 1's "0 clean" vs row 2's "0 every active row held" are distinct gates; row 3's delegation to the round-16 row and row 4's to the round-13 row both resolve to tables that still exist at C0; the "re-pin" (row 1) / "monitor" (row 2) split matches the heading.
6. **Counts/paths in the section.** All four tool paths, both evidence paths (`.ufo/evidence/round-18/dispositions.json`, `.ufo/evidence/round-13/pin-manifest.json`), and the fleet root in row 4 resolve at C0.

Near-misses considered and not filed (so a later reader does not re-derive them): row 1's parenthetical "unprovenanced input" is a category name over the tool's exit-2 classes (the G4 work-tree identity guard refuses an unprovenanced root, `tools/evidence-disposition.py:436-471`), as round 53's reader also concluded; row 2's cell omits the tool's `--root`/`--only` flags, but the listed invocation and every listed exit are correct, so nothing is falsified.

## Receipts

Scratch clone (before any git call in it, `git rev-parse --show-toplevel` printed the clone path):

```
git clone --quiet --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin c0clone
git -C c0clone checkout -q -b read20c0 59c38109bf119d0e9d4f878644a82babc937bc1e
$ git -C c0clone rev-parse HEAD
59c38109bf119d0e9d4f878644a82babc937bc1e
```

R1 — row 1, round-18 dispositions (documented invocation):

```
$ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json
EXIT=0
  "schema": "evidence-disposition-result-v1",
  "status": "clean",
  "tool": "evidence-disposition.py r18 (tameshi-shokunin, 2026-10-20): branch-tip v2 historical inputs"
```

R2 — row 1, the "(round-17 manifest now exits 2)" parenthetical:

```
$ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json
EXIT=2
{"error": {"kind": "expected_input_digest_mismatch",
           "message": "tools/bash-witness-study.py: observed f2bb50c7… expects 49e9e5e2…"}, ...}
```

R3 — row 2, selftest and an unresolvable rev:

```
$ python3 tools/registry-check.py --selftest
RC_ST_EXIT=0
SELFTEST: PASS (51 cases)

$ python3 tools/registry-check.py --root . --rev 0000000000000000000000000000000000000000
BADREV_EXIT=2
REGISTRY_CHECK: could-not-evaluate (rev '0000000000000000000000000000000000000000' unavailable in .)
```

R4 — row 4, the documented probe:

```
$ python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin
PD_EXIT=0
{'status': 'ok', 'schema': 'pin-disposition-v1', 'tool': 'pin-disposition.py r17 (tameshi-shokunin, 2026-10-20)'}
counts {'legs': 6, 'unchanged': 1, 'changed': 5, 'unavailable': 0}
```

R5 — F1, the two selftest arms at C0:

```
$ TMPDIR=/fast/scratch/…/T54W1Read20/tmp python3 tools/pin-disposition.py --selftest
ST_EXIT=0
SELFTEST_CASE invalid-root PASS (exit=2 expects=2 4 literal checks)
SELFTEST_CASE detached-head-uses-branch-tip PASS (exit=0 expects=0 14 literal checks)
SELFTEST: PASS (19/19)

$ TMPDIR=/fast/scratch/…/T54W1Read20/does-not-exist python3 tools/pin-disposition.py --selftest
ST_BAD_EXIT=2
pin-disposition.py: could-not-evaluate: cannot create clone scratch under the scratch root:
TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r54/T54W1Read20/does-not-exist' (could-not-evaluate)
```

Verdict: F1 stands — the delegated cell enumerates `selftest 1 failed` and the tool's selftest now also returns 2 (could-not-evaluate) at C0.

R6 — row 3 control (unusable TMPDIR must not create a second arm):

```
$ TMPDIR=…/nope bash tools/mutate-and-run.sh --selftest
MR_ST_BAD_EXIT=1
mktemp: failed to create directory via template '…/nope/tameshi-r4-2-selftest.XXXXXX': No such file or directory
MUTATE_SELFTEST: 0/1 pass
VERDICT: FAIL (mktemp)
```

Verdict: exit 1 is inside the round-16 row's "selftest 0 pass / 1 fail"; the delegation holds for row 3.

R7 — the seven `scratch_root` rows at C0 (the artifact F1 compares against):

```
$ python3 -c '...rows carrying scratch_root...'
7
['repeat-control-selftest', 'bash-witness-selftest', 'pin-disposition-selftest',
 'evidence-disposition-selftest', 'context-capture-selftest', 'registry-check-selftest',
 'env-diff-selftest']
```

Section sha reproduction:

```
$ sha256sum section-body
8a92f71e046aae243294c42153c6ed183ccd41edf4647ff9520e35a26b9c9643  section-body
```

## Delivered

- `.ufo/waves/round-54/w1/T54W1Read20.json` — one finding, quote `as the round-13 row`.
- `.ufo/waves/round-54/w1/T54W1Read20.md` — this file (same finding, byte-exact quote above).

Scratch tree `/fast/scratch/hyaku/tameshi-r54/T54W1Read20/` removed after the receipts were transcribed; no lane file was edited.
