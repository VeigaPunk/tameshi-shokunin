# T53W2Read14 — re-read of `### Round-26 gate/probe registry — report interop` at C**

Seat: T53W2Read14 (wave 2 of 2, round 53). Candidate read: `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e` (C\*\*), via git objects only (`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show REV:SKILL.md`). The working tree was never read.

## Section identity and split verification

- Frozen-monitor split: SKILL.md at C\*\* split into lines; heading = line matching `^#{1,3}(\s|$)` outside ``` fences (so the `#### Gate/probe registry — round 51` line is body, not a boundary); section = heading line through the line before the next heading, trailing whitespace-only lines stripped, joined with `\n`, no trailing newline; sha256 over UTF-8 `surrogateescape` bytes.
- Result at C\*\*: heading at SKILL.md line 2150, next heading = none (the section runs to EOF), 40 section lines, 23082 bytes, `section_sha256 = cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52`.
- Split verification: the same splitter run against C\* = `a41195dfc13a73958e4c5228ec196b28d03ded03` reproduces `5399e46663220dea7df1c4ae9dc1b2871150e73aabe007d1371aa2a80e1a8e93`, byte-for-byte the `section_sha256` in the committed wave-1 reader `.ufo/waves/round-53/w1/T53W1Read19.json`. The splitter therefore matches the one wave 1 used.

```
$ python3 split.py 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e '### Round-26 gate/probe registry — report interop' sec_CSS.txt
rev 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e start_line 2150 next_heading_line EOF nlines 40
sha256 cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52
$ python3 split.py a41195dfc13a73958e4c5228ec196b28d03ded03 '### Round-26 gate/probe registry — report interop' sec_C1.txt
rev a41195dfc13a73958e4c5228ec196b28d03ded03 start_line 2139 next_heading_line EOF nlines 40
sha256 5399e46663220dea7df1c4ae9dc1b2871150e73aabe007d1371aa2a80e1a8e93
```

Runner fixture: `git clone --shared` of the lane into the seat scratch, `git checkout 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`; every command below ran inside that clone (`git rev-parse --show-toplevel` = the clone), never against the lane tree.

## Checks run — the seven named fixes FIRST

Wave-1 reader `T53W1Read19` filed seven stale `/tmp` write-scope cells plus the context-capture exact-string drift. All seven are present in the C\*\* bytes and match the C\*\* tool sources.

| # | Section cell (row) | C\*\* text | Code at C\*\* | Observed |
|---|---|---|---|---|
| 1 | bash declared-witness study (L11) | `selftest writes a private fixture tree under the scratch root (`$TMPDIR` since round 53)` | `tools/bash-witness-study.py:1254-1260` `tempfile.mkdtemp(prefix="bash-witness-selftest-private.", dir=strict_scratch_root())`; helper at `:205-216` | `bash tools/bash-witness-study.py selftest` → `WITNESS_SELFTEST: 51/51 pass`, last line `VERDICT: PASS`, rc 0, and its own case `check private root is removed  ok` |
| 2 | context receipt replay (L13) | `selftest fixtures under `$TMPDIR` (`context-capture-selftest-*`), removed in finally` | `tools/context-capture.py:1638-1639` mkdtemp `dir=strict_scratch_root()`; cleanup in `finally:` at `:2222-2224` | `python3 tools/context-capture.py --selftest` → `SELFTEST: PASS (49/49)`, 49 `SELFTEST_CASE` lines, rc 0 |
| 3 | evidence disposition accounting (L15) | `selftest fixtures under `$TMPDIR` (`tameshi-r14-evidence-disposition-selftest.*`) removed on pass, kept on failure` | `tools/evidence-disposition.py:2365` `dir=strict_scratch_root()`; `:3129` prints `fixtures kept at`, `:3136` `rmtree` on pass | `python3 tools/evidence-disposition.py --selftest` → `SELFTEST: PASS (66/66)` in ~3 s, rc 0 |
| 4 | pin disposition (L20) | `selftest writes isolated `$TMPDIR` fixtures (`tameshi-r13-pin-disposition-selftest.*`), removed on PASS` | `tools/pin-disposition.py:720` `dir=strict_scratch_root()`, same prefix | `python3 tools/pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)`, rc 0 (matches the row's `n/n` placeholder) |
| 5 | entry-registry walk (L23) | `selftest and --rev fixture trees via mkdtemp under the scratch root (`$TMPDIR`; … — round 53), removed afterwards` | `tools/registry-check.py:930-931` mkdtemp `dir=strict_scratch_root()`, prefix `tameshi-r17-registry-check-selftest.`; `finally: shutil.rmtree(scratch)` | `python3 tools/registry-check.py --selftest` → `SELFTEST: PASS (51 cases)`, rc 0 — **but see the finding**: under a set-but-unusable TMPDIR the selftest exits 1 with a traceback |
| 6 | repeated control agreement (L25) | `selftest scratch under `$TMPDIR` (`tameshi-r12-repeat-control-selftest.*`, removed on pass)` | `tools/repeat-control.py:611` `dir=strict_scratch_root()`; `:875-876` `rmtree` only on PASS, failure emits `SELFTEST_SCRATCH` | `python3 tools/repeat-control.py --selftest` → `SELFTEST: PASS (29 cases)`, rc 0 |
| 7 | environment-profile differential (L14) | `sandboxes under `$TMPDIR` (`tameshi-r21-envdiff.*`) and TMPDIR-respecting selftest trees` | `tools/env-diff.py:75` `dir=strict_scratch_root()`, prefix `tameshi-r21-envdiff.` | `python3 tools/env-diff.py --selftest` → `ENVDIFF_SELFTEST: 9/9 pass`, rc 0 |

Exact-string fix: the context-capture row now reads `SELFTEST: PASS (49/49)` and the C\*\* tool prints exactly `SELFTEST: PASS (49/49)` (`tools/context-capture.py:1799` format string, total 49); the wave-1 quote `SELFTEST: PASS (49/49 cases)` is gone from the section.

`grep -n '/tmp' sec_CSS.txt` now returns only three write-scope cells — fleet mutation runner (`${TMPDIR:-/tmp}`), tally audit v2 (`/tmp/tally-audit-work`), tally audit v3 (`/tmp/tameshi-r4-2-regression.XXXXXX`) — plus the `never a silent /tmp fallback` clause in the registry row. All three are statements about actual literal `/tmp` use; see "Holds" below.

## Finding

**F1 — the round-53 TMPDIR strictness claim is true for `--rev` but false for `--selftest`.**

Verbatim section text (row `entry-registry walk`, SKILL.md line 2172 at C\*\*):

> a set-but-unusable TMPDIR is could-not-evaluate, never a silent `/tmp` fallback — round 53

The clause governs "selftest and --rev fixture trees". At C\*\*, `--rev` behaves as claimed, but the selftest path lets the helper's `RuntimeError` escape `main` before any case runs, so the process exits 1 — the same row's verdict map calls 1 "failed", not could-not-evaluate, and the run prints a traceback instead of a verdict line:

```
$ TMPDIR=/nonexistent-tmpdir-r53 python3 tools/registry-check.py --selftest; echo "SELFTEST_EXIT=$?"
Traceback (most recent call last):
  File "…/tools/registry-check.py", line 1968, in <module>
    sys.exit(main(sys.argv[1:]))
  File "…/tools/registry-check.py", line 1845, in main
    return selftest()
  File "…/tools/registry-check.py", line 931, in selftest
    prefix="tameshi-r17-registry-check-selftest.", dir=strict_scratch_root()
  File "…/tools/registry-check.py", line 765, in strict_scratch_root
    raise RuntimeError(
RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent-tmpdir-r53' (could-not-evaluate)
SELFTEST_EXIT=1

$ TMPDIR=/nonexistent-tmpdir-r53 python3 tools/registry-check.py --rev HEAD; echo "rc=$?"
REGISTRY_CHECK: could-not-evaluate (cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent-tmpdir-r53' (could-not-evaluate))
rc=2
```

Cause visible in the C\*\* source: only the `--rev`/`--root` clone path has the conversion (`tools/registry-check.py:1924` `except RuntimeError as exc:` → `emit(f"REGISTRY_CHECK: could-not-evaluate ({exc})")`, return 2). `main()` at `:1845` returns `selftest()` with no wrapper, and `selftest()` calls `strict_scratch_root()` at `:931` with no handler — the nearby `except OSError` at `:781` does not catch `RuntimeError`. The `(could-not-evaluate)` substring in the exception message does not change the process class: exit 1 is "a row differs / a case failed" under this row's own map (`0 clean; 1 failed; 2 could-not-evaluate …`).

Class: false exit-class claim. The fix pass added the strict helper to seven tools and documented CR47 semantics for registry-check; the selftest half of that sentence does not hold at C\*\*.

## Holds (verified, no finding)

- Row `entry-registry walk` counts: `SELFTEST: PASS (51 cases)` is the exact last line at C\*\* (run above). The trailing `at 84aa673` reads as provenance in the same idiom as the next row's `at rev 84aa673`, so the claim is treated as a hold, not as string drift.
- Remaining literal `/tmp` cells are accurate about the C\*\* code: fleet mutation runner `--workdir` default `mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-run.XXXXXX"` (`tools/mutate-and-run.sh:217,491`); tally audit v2 sweep config `('/tmp/tally-audit-work', '1', '0')` with `rm -rf "$root"` on the auto/KEEP=(1,0) PASS branch (`tools/tally-audit-v2.py:265,102-104`); tally audit v3 `auto_root()` allocating `/tmp/tameshi-r4-2-regression.<6 alnum>` under `atexit` rmtree (`tools/tally-audit-v3.py:412-431`).
- Round-26 row: registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (10/10) exist with exactly those stdout expectations in `tools/registry.json` at C\*\*; `python3 tools/mte-interop.py --selftest` → `MTE_SELFTEST: 17/17 pass`, rc 0; `--fleet-root`, the `jsonschema==4.25.1` hint, the vendored `dist.integrity` check (`:177-181`), the `unexpected tar member` refusal (`:211`) and the `leg set … differs from the ten ledger legs` SETUP (`:316-319`) are all present.
- Selftest tallies quoted in the round-51 table, run at C\*\* and matching verbatim: receipt-measure `RECEIPT_MEASURE_SELFTEST: 10/10 pass`; receipt-window `RECEIPT_WINDOW_SELFTEST: 20/20 pass`; wave accounting `ACCOUNTING_EXTRA_SELFTEST: 16/16 pass` + `FINDING: SELFTEST_PASS`; wave parent `WAVE_PARENT_SELFTEST: 3/3 pass`; wave-route-mix `ROUTEMIX_SELFTEST: 8/8 pass`; witness metadata `SELFTEST: PASS 39/39`; pbt `PBT_STAGED_ID_SELFTEST: cases=35 failed=0`; shrink-case `SHRINK_SELFTEST: cases=21 failed=0`; tally-audit-v2 `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`; tally-audit `TALLY_AUDIT_SELFTEST: 11/11 pass`; write census v2/v3/v4 lines pass byte-exactly (`… cases=15 failed=0`); registry-replay `REGISTRY_REPLAY_SELFTEST: 10/10 pass`; trace-inputs `SELFTEST: 30/30`; staged-id guard `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` + last line `VERDICT: PASS`; command-binding last line begins `COMMAND_BINDING_SELFTEST:`; golden-verdict `GOLDEN_VERDICT_SELFTEST: 3/3 pass`.
- Other write-scope cells checked against source: command-binding `TemporaryDirectory(prefix='tameshi-command-binding-')`; golden-verdict `TemporaryDirectory(prefix='golden-verdict-')`; receipt-measure `receipt-measure-selftest.` plus the delegated `tameshi-r20-measure.` in `.ufo/evidence/round-20/stage/measure.py:82`; receipt-window `tameshi-r20-rw-selftest.`; registry-replay private clone with `fleet/<sibling>` symlinks (`.symlink_to(..., target_is_directory=True)`, `tools/registry-replay.py:161`); round21-measure fleet-bound selftest reading the sibling blobs its subject counter names (`tools/round21-measure.py:77-84`, `.ufo/evidence/round-21/c2-count.py:19` `FLEET = Path("/home/vgpnk/Projects/shokunin")`); shrink-case `mkdtemp` roots plus the `importlib` load of `pbt-staged-id.py` beside the tool (write scope `tools/__pycache__`); witness-metadata fixture tree removed in `finally` (`:1185-1186`); write-path census `TemporaryDirectory(prefix='write-path-census-')`; wave-parent-settle and staged-id-guard create no temp files; write-path census v2/v3/v4 write nothing.

## Observations (outside this section's statements; routed as evidence only, not findings)

- Five of the seven round-53 tools let `strict_scratch_root()`'s `RuntimeError` escape and exit 1 under a set-but-unusable TMPDIR: `registry-check.py --selftest`, `env-diff.py --selftest`, `pin-disposition.py --selftest`, `evidence-disposition.py --selftest`, `bash-witness-study.py selftest`. `context-capture.py --selftest` (exit 2, `SELFTEST: FAIL (setup error: RuntimeError: …)`) and `repeat-control.py --selftest` (exit 2, `REPEAT_CONTROL: setup_error`) classify correctly. Only the registry-check cell makes the could-not-evaluate claim, hence one finding; the C2 counter's CTL_CR47 only requires non-zero plus the scratch-creation wording, so it can pass while this sentence is false.
- The seven tools' own docstrings still say `/tmp` where the code now honours TMPDIR (`tools/evidence-disposition.py:181`, `tools/pin-disposition.py:36,719`, `tools/repeat-control.py:67`, `tools/context-capture.py:27`). That is tool documentation drift, not a statement in this section.

## Limits

- `tally-audit-v3.py --selftest` did not finish inside 300 s (interrupted mid-case), so the section's `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` was not observed in this seat; no counter-evidence either.
- `mte-interop.py --check` was not re-run (it replays live sibling object stores); only the registry row expectations and the selftest were checked.
- Selftests were run from the C\*\* clone; a first attempt on a bare copy of `tools/context-capture.py` outside the lane layout failed its own `hermetic-no-lane-path` case, so all quoted results above are from the clone.

## Scratch

Everything lived under `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read14/` (splitter, extracted section and tool blobs, `--shared` clone at C\*\*, TMPDIR roots `tmp`…`tmp8`). Tree deleted before yield; no lane, fleet-root, `.local/bin` or `/tmp` writes were made.
