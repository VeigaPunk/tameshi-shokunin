# T52W1ExecR21Fix — R51.4: make the round-21 measure selftest read the fleet root its counter reads (fleet-bound, not hermetic)

Item: fix routed defect R51.4 in `tools/round21-measure.py` on a `git clone --shared` scratch copy.
Base: `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4` (blob `24a36fecbc882fbf6690e4108fb8eabc44b06d6e`).
Patch: `.ufo/waves/round-52/w1/T52W1ExecR21Fix.patch` (1 file, +18/−2, dst blob `2f36db4d51082da93598c930f09002a7b4a6dddd`).
The lane checkout was never written; all edits, commits and runs happened in one `git clone --shared` scratch copy
(`$S/sim/tameshi-shokunin`, `$S=/fast/scratch/hyaku/tameshi-r52/T52W1ExecR21Fix`).

## Defect, as reproduced at base

`tools/round21-measure.py:74` builds the c2 fixture's pins from `str(ROOT.parent / surface["repo"])`, i.e. from
`<$clone>/../<repo>`; the subject counter it exercises reads an absolute root,
`.ufo/evidence/round-21/c2-count.py:19` → `FLEET = Path("/home/vgpnk/Projects/shokunin")`. Outside the fleet root the
two disagree and the selftest dies before any case runs:

```
$ cd $S/edit && TMPDIR=$S python3 tools/round21-measure.py --selftest      # clone outside the fleet root
  File ".../edit/tools/round21-measure.py", line 74, in selftest
    data = subprocess.run(["git", "-C", str(ROOT.parent / surface["repo"]), ...
subprocess.CalledProcessError: Command '['git', '-C', '.../T52W1ExecR21Fix/tameshi-shokunin', 'show',
  '08175c62...:tools/mutate-and-run.sh']' returned non-zero exit status 128.
EXIT=1
```
Receipt: `T52W1ExecR21Fix-base-outside.out` (command in `T52W1ExecR21Fix-env-and-patch.out`).

## Change

Parsed from the **package copy** of the counter that the fixture actually executes (written at
`tools/round21-measure.py:63-64`), so the fleet root is declared once, in the subject, and never re-hard-coded:

- `tools/round21-measure.py:20` — `import re`.
- `tools/round21-measure.py:78-87` — `fleet_match = re.search(r'^FLEET = Path\("([^"]+)"\)$', (package / SCRIPTS["c2"]).read_text(), re.M)`;
  no match → `MEASURE_SELFTEST: c2 counter declares no FLEET root` and exit 2; `not fleet.is_dir()` →
  `MEASURE_SELFTEST: fleet root <path> missing (fleet-bound selftest)` and exit 2.
- `tools/round21-measure.py:90` — `git -C str(fleet / surface["repo"])` (was `ROOT.parent / ...`).
- `tools/round21-measure.py:8-13` — docstring now states the class: the fixture reads the pinned sibling blobs from
  the fleet root the subject counter reads, "so this selftest is fleet-bound, not hermetic".

Case literals and exit codes are untouched: 11 `check()` call sites (13 executed cases because two run in a
`for claim in ("c1","c2")` loop), the 11 frozen `R21_CASES` substrings are byte-identical, and the exit-code lines 0/1
(`return 0 if passed == len(checks) else 1`), 64 (`Parser.error`) and `sys.exit(main())` are unchanged; the documented
2 (could-not-evaluate) is used only by the two new guards.
Receipt: `T52W1ExecR21Fix-literals.out` (`case-literal lines identical: True`, `exit-code lines base: 4 fixed: 6`,
the two added lines being `return 2`).

## (1) Clone outside the fleet root: base red, fixed green

Same clone directory (`$S/edit`, parent `$S`, which holds no sibling repos), same `TMPDIR=$S`; only the file bytes
differ.

```
$ cd $S/edit && TMPDIR=$S python3 tools/round21-measure.py --selftest    # base bytes (blob 24a36fe)
  File ".../T52W1ExecR21Fix/edit/tools/round21-measure.py", line 74, in selftest
    data = subprocess.run(["git", "-C", str(ROOT.parent / surface["repo"]), ...
  subprocess.CalledProcessError: Command '['git', '-C', '.../T52W1ExecR21Fix/tameshi-shokunin', ...
  EXIT=1
$ (apply the patch in the same clone)
$ cd $S/edit && TMPDIR=$S python3 tools/round21-measure.py --selftest    # fixed bytes (blob 2f36db4)
  MEASURE_CASE ... (13 lines, every one PASS)
  ROUND21_MEASURE_SELFTEST: 13/13 pass
  EXIT=0
```
The traceback's `git -C .../T52W1ExecR21Fix/tameshi-shokunin` is `ROOT.parent / "tameshi-shokunin"` = `$S/…`,
i.e. the defect's `:74` resolution, not the counter's `FLEET`.
Receipts: `T52W1ExecR21Fix-base-outside.out`, `T52W1ExecR21Fix-fixed-outside.out`.

## (2) Lane checkout path layout

The same clone was then moved to `$S/sim/tameshi-shokunin`, so `ROOT.parent = $S/sim` holds the five sibling names
the c2 contract pins (`tameshi-shokunin` = the clone itself; `kumitate-shokunin`, `kagi-shokunin`,
`tsukuroi-shokunin`, `mado-shokunin` = symlinks to the real read-only repos). The lane checkout itself is read-only
for this seat, so this is the same clone in a fleet-shaped parent rather than the lane directory; with the patch the
fleet root is read from the counter's literal, so the location no longer selects the root.

```
$ cd $S/sim/tameshi-shokunin && TMPDIR=$S python3 tools/round21-measure.py --selftest   # base bytes here
  ROUND21_MEASURE_SELFTEST: 13/13 pass   EXIT=0        <- base passes in the lane-like layout
$ ... fixed bytes ...
  ROUND21_MEASURE_SELFTEST: 13/13 pass   EXIT=0
```
So the base failure is location-only, and the fixed tool passes in both layouts.
Receipts: `T52W1ExecR21Fix-base-lanelayout.out`, `T52W1ExecR21Fix-fixed-lanelayout.out`.

## (3) Negative: the selftest is fleet-bound, not hermetic

One fixture tree (`$S/neg/negclone`: `git archive` of `tools/` and `.ufo/evidence/round-21/` from the clone —
content identical to the lane tip for those paths — plus the patched file, with the five sibling names present under
`$S/neg` so the base `ROOT.parent` path resolves). The only variable is the `FLEET` literal in that tree's copy of
`c2-count.py`:

| case | FLEET | result |
|---|---|---|
| n1 | `/home/vgpnk/Projects/shokunin` (real) | `13/13 pass`, exit 0 |
| n2 | `$S/neg/empty` (exists, empty) | exit 1 — `git -C .../neg/empty/tameshi-shokunin show ... 128` |
| n3 | `$S/neg/no-such-fleet` (absent) | exit 2 — `MEASURE_SELFTEST: fleet root .../no-such-fleet missing (fleet-bound selftest)` |
| n0 | `$S/neg/empty`, **base** bytes | `9/13 pass`, exit 1 — the subject counter itself cannot read the pins |

n0 shows the dependency is on the real sibling blobs, not on the implementation: with the fleet emptied the frozen
counter cannot verify `blob_sha256` either, so `c2-complete`, `c2-wrong-pin`, `c2-missing-profile` and
`c2-wrong-classification` fail regardless of which `ROOT` scheme the fixture uses.
Receipts: `T52W1ExecR21Fix-neg-n0-base-emptyFLEET.out`, `-neg-n1-realFLEET.out`, `-neg-n2-emptyFLEET.out`,
`-neg-n3-missingFLEET.out`, fixture layout in `-neg-fixture.out`.

## Component check through the frozen round-51 C3 counter's own code

The full C3 sweep at the fixed rev did **not** finish inside 900s in this environment (the counter prints only its
final line, so a timed-out run leaves an empty receipt; other rows, not the round-21 one, dominate). To test exactly
the component R51.4 touches, the frozen counter's own functions were loaded from its freeze bytes
(sha256 `a3abbd3b7888432919a999b1de357d4b71fa7262d55ae2f5ff97be4dddb3fd3a`, verified) and `run_row` was called once
for the row that names the tool:

```
row line 2157 name round21 measure facade reason None
spec ['python3', 'tools/round21-measure.py', '--selftest'] | usage ['python3', 'tools/round21-measure.py', '--r51-no-such-flag']
run_row -> (None, 'ROUND21_MEASURE_SELFTEST: 13/13 pass')
```
`None` is the counter's "row is covered" verdict (the frozen code returns a reason string on failure), and the usage
probe exits 64 as the row's verdict map declares. This is the row that made `total=1` at base.
Receipt: `T52W1ExecR21Fix-c3-row-round21.out`.

## Naming, honestly

**Fleet-bound self-test**, not hermetic. It cannot pass on a host without
`/home/vgpnk/Projects/shokunin/{tameshi,kumitate,kagi,tsukuroi,mado}-shokunin` at the pinned revs; the fix only
makes it read the *same* root the subject counter reads instead of guessing from `__file__`.

## Risks and limits

- The parse is coupled to the literal syntax `^FLEET = Path("...")$` at line start (`c2-count.py:19`). If that line is
  ever rewritten the selftest fails loudly (exit 2, `c2 counter declares no FLEET root`) rather than guessing — a
  deliberate, visible coupling, but it is a coupling.
- The selftest still cannot tell whether the sibling blobs it hashes are the *right* blobs: pin and expectation come
  from the same fleet root, so the c2 cases are self-consistent by construction. This matches contract `cannot_see`.
- (3) n2/n0 red is a `CalledProcessError` traceback, not a curated message; only the absent-root case (n3) prints the
  guard line. Exit codes still 1 and 2 as documented.
- Not in scope: the `mte-interop-check` registry row (R51.1) and the C2 text fixes.

## Tooling

No installs or upgrades were made (none needed); no pacman transaction was attempted.

## Summary

- R51.4 fixed: the selftest takes its fleet root from the copied `c2-count.py`'s `FLEET` literal (`:78-87`, used at `:90`); no second hard-coded root; 11 case literals / 13 cases and exit codes 0/1/64 unchanged.
- Outside the fleet root (`$S`): base exit 1 at `:74`, fixed `13/13 pass` exit 0; in a fleet-shaped parent both pass (`13/13`, exit 0), so base's red was location-only.
- Negative: emptied `FLEET` → exit 1 (patched) and 9/13 (base); absent `FLEET` → exit 2 with the guard line; real `FLEET` in the same tree → 13/13.
- Frozen round-51 C3 `run_row` for the round-21 row at the fixed rev: covered (`None`, `13/13 pass`); the full 30-row sweep exceeded 900s here.
- Class: fleet-bound self-test, not hermetic. Patch and receipts: `.ufo/waves/round-52/w1/T52W1ExecR21Fix*`.
