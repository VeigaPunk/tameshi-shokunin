# T51W2ExecTool02 — independent audit of the C3 registry row for `tools/command-binding.py`

Seat T51W2ExecTool02, round 51 wave 2 (falsify). Candidate
`6d8c11e378aa90b12650808e1b79270742935f15`; base `9962033fd7a75aa2f2847e979dd687a5d28505a1`.

Row audited: **SKILL.md:2143**, name cell `command binding receipts`, second data row of the
canonical section `#### Gate/probe registry — round 51` (heading SKILL.md:2138; 30 data rows at
SKILL.md:2142-2171). Read-only on the lane; all runs in
`git clone --shared --no-checkout` at CAND under
`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool02/clone`, `TMPDIR=$S/tmp`, stdin `/dev/null`.
Raw receipts: `.ufo/waves/round-51/w2/@P@ExecTool02/` (`selftest-and-usage.json`,
`selftest.stdout`, `usage-probe.txt`, `probes.txt`, `counter-row-logic.txt`,
`c3-counter-full-run.txt`, `entry-mode-exits.txt`, `pinned-fixture-shrink.txt`,
`registry-check-clean-lane.txt`, `registry-check-gutted-fixtures.txt`, `usage-code-mutant.txt`).

## Verdict on operability

**The row is operably true at CAND and the frozen C3 counter covers it.** Self-test exits 0 with a
real finding id on the last stdout line, the usage probe exits a code the verdict map declares, both
pinned paths exist and are load-bearing, the write-scope cell is accurate to the syscall, and the
tool is a genuine gate (it fails). Five cell-level defects are measured below; **none makes the C3
predicate fail for this row**, and two of the five are compensated by *different* instruments the C3
counter never reads (`tools/registry.json` + `tools/registry-check.py`).

C3's single miss at CAND is **not this row**: the frozen counter prints
`C3_TOOL tools/round21-measure.py: MISSING (line 2157 selftest-exit=1 last=)` — the disclosed
round21-measure clone-context blocker, i.e. row 16 of the table. See §4.

## 1. Row command runs, exits and wall time (the item's required receipt)

Executed from the fresh `--shared` clone at CAND, `TMPDIR=$S/tmp`, stdin `/dev/null`:

| run | argv | exit | last stdout line | wall |
|---|---|---|---|---|
| row self-test | `python3 tools/command-binding.py --selftest` | **0** | `COMMAND_BINDING_SELFTEST: 44/44 pass` | **1.93 s** (45 stdout lines, 1213 B, stderr empty) |
| usage probe | `python3 tools/command-binding.py --r51-no-such-flag` | **64** | *(stdout empty)* stderr last line `command-binding.py: error: unrecognized arguments: --r51-no-such-flag` | **0.041 s** |

Both are inside the counter's 900 s / 60 s limits by three orders of magnitude. Repeated runs from
`cwd=/` and `cwd=/tmp` also give `44/44 pass` rc 0, because the tool resolves its fixtures from
`Path(__file__).resolve().parents[1] / '.ufo/evidence'` (tool:164), not from cwd.

Counter replay of the row's own logic (frozen `measure.py` imported from
`.ufo/evidence/round-51/c3/measure.py`, imported from a scratch copy so no bytecode lands in the lane):

```
MATCH_ROW_LINE 2143
ROW_REASON None
SPEC_ARGV  ['python3', 'tools/command-binding.py', '--selftest']
SPEC_USAGE ['python3', 'tools/command-binding.py', '--r51-no-such-flag']
RUN_ROW_WHY None
RUN_ROW_LAST 'COMMAND_BINDING_SELFTEST: 44/44 pass'
```

…and the full frozen counter at CAND:

```
C3_TOOL tools/command-binding.py: covered line 2143 selftest exit=0 last=COMMAND_BINDING_SELFTEST: 44/44 pass
C3_R51: rev=6d8c11e378aa90b12650808e1b79270742935f15 tools=30 rows=32 covered=29 missing=1 deleted=0 selftest_fail_rows=2 total=1 C3_R51_PASS=false
```

## 2. Row fields checked against source

`tools/command-binding.py` is byte-identical at base and at CAND (blob `1b4bbb77…`, sha256
`9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d`), so this C3 item is purely a
registry-row change for this tool.

**Kind = `gate` — TRUE (it truly fails, it is not a probe).** Measured with a hand-built mismatched
bundle at the pinned digest: exit **1**, `finding_ids: ["ARGV_MISMATCH"]`; tampered expected →
exit **2** `SNAPSHOT_TAMPERED`; committed clean pair → exit **0** `[]`. The self-test is coupled to
the graders, not decorative — four body mutants each turn it red in their own clone:
`no-argv-check` 32/44, `no-exit-check` 41/44, `no-digest-check` 43/44, `always-clean` 21/44 (all rc 1).

**Entry command — NOT RUNNABLE AS WRITTEN.** Cell 3 is
`python3 tools/command-binding.py --bundle BUNDLE.json --expected EXPECTED.json --json`. Those are
unresolved placeholders: `git ls-files | grep -c BUNDLE.json` = **0**, and running the cell verbatim
gives exit **2** `INVALID_INPUT`. The row it supersedes (SKILL.md:2019, round-21 section) gave the
concrete committed pair instead. That pair exists and reproduces here:
`.ufo/evidence/round-23/replay/bundle.json` + `expected.json` → exit 0, `bundle_sha256
3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9`. Placeholder entry cells are the
table's convention (`--out DIR`, `--repo REPO --rev REV`), so this is a convention cost — but for this
tool a committed runnable pair exists and the row does not name it.

**Verdict map — class mapping true and complete; two precision defects.**

* `0 clean`, `1 failed binding or outcome`, `2 could-not-evaluate`, `64 could-not-evaluate (usage)`:
  over 24 malformed bundle/expected shapes (non-list containers, non-dict rows, missing/extra
  `expect` keys, float/null/bool/huge-int exits, NUL and empty argv strings, non-str stdout, relative
  and `//` cwds, uppercase revision, wrong schema, extra top-level key, top-level list/null, empty and
  NaN JSON, malformed `expected`) plus missing file, directory-as-bundle, invalid UTF-8, 60 000-deep
  JSON, `--help` and duplicate JSON keys, the observed code set is **only {0, 1, 2, 64}**. 23 of the
  24 shapes returned exit 2; the 24th (`receipts[0].exit = 10**40` against a declared 0) returned
  exit 1 `EXIT_MISMATCH`, which is a genuine verdict. No undeclared code was reachable, so the map
  satisfies PROTOCOL's "every other code a gate exits is declared and mapped".
* **(a) exit 2's parenthetical is narrower than the tool.** `2 could-not-evaluate (invalid shape or
  integrity)` omits *unavailable/unreadable input*: `OSError`/`UnicodeError`/`RecursionError` →
  `INVALID_INPUT` → exit 2 (tool:129-130). Measured: missing bundle file → 2 `INVALID_INPUT`;
  directory as `--bundle` → 2; bad UTF-8 → 2; deep nesting → 2. The superseded row at SKILL.md:2019
  said `2 invalid/unavailable/tampered`; the canonical row dropped "unavailable". The *class* is
  still right, so this is description drift, not a class misgrade.
* **(b) "specifically 64 = usage" is enforced nowhere in the repo.** A committed fixture clone with
  `Parser.error`'s `self.exit(64, …)` changed to `self.exit(2, …)` (fixture rev
  `3c9a6b58022364da83436311a219168dbde44718`, tool:37-40) still prints `COMMAND_BINDING_SELFTEST:
  44/44 pass` rc 0, still holds all three active `tools/registry.json` rows — the full
  `registry-check.py --rev HEAD` on that lane prints all six command-binding rows with
  `selftest-r24 / frozen-clean-pinned / source-read-red-pinned … held` and
  `REGISTRY_CHECK: held=44/49 superseded=7` — and the frozen C3 `run_row` returns
  `(None, 'COMMAND_BINDING_SELFTEST: 44/44 pass')`, because `2` is also a declared token in the same
  verdict-map cell. Receipt: `@P@ExecTool02/usage-code-mutant.txt`. For this row the counter's usage check is therefore
  non-discriminating, and the code→meaning pin lives only in the row's prose.
* **(c) exit 1 also covers uncaught tracebacks.** `--json | head -c0` → `BrokenPipeError` traceback,
  **rc 1** (Python's default), which the map grades `failed` rather than could-not-evaluate. Bounded:
  only reachable on a broken stdout or an exception outside `check()`'s catch list
  `(OSError, ValueError, RecursionError, UnicodeError)` (tool:129); all 25 malformed-input shapes
  landed in 2, not 1.

**Self-test command and last-line marker — TRUE and genuinely diagnostic.** The cell records
`python3 tools/command-binding.py --selftest` → `finding id COMMAND_BINDING_SELFTEST: in the last
stdout line`. The marker is printed by the tool's own selftest summary (tool:193,
`'COMMAND_BINDING_SELFTEST: %d/%d pass'`), carries a pass tally, and is *not* help text: the last
line of `--help` is `  --selftest` (an option name). **This row is not the wave-1 `--help --selftest`
forgery** — it invokes the real mode and the marker it records is produced by that mode. The failure
path prints the same prefix (`COMMAND_BINDING_SELFTEST: fixture-unavailable`, tool:171) but exits 1,
so the exit code still discriminates.

**Pinned values — paths exist and are load-bearing; but the row pins no digest and no tally.**

* Both pinned paths exist at REV: `.ufo/evidence/round-23/extra-cases.json` (19 cases) and
  `.ufo/evidence/round-24/extra-cases.json` (6 cases).
* Removing **either** file → exit 1, `COMMAND_BINDING_SELFTEST: fixture-unavailable` (tool:170-172).
* Editing one case's `expected_exit` → 43/44, exit 1. Editing one case's `finding_ids` → 43/44, exit 1.
* **Deleting a case is not detected by this row or by the counter.** Dropping one supplemental case →
  `43/43 pass`, exit **0**. Emptying *both* `cases` arrays and committing the edit (fixture rev
  `6778bc85afcc09b11df974ab5071c9e3b8ef1883`, `2 insertions(+), 1768 deletions(-)`) → `19/19 pass`,
  exit **0**, first token still `COMMAND_BINDING_SELFTEST:`, and the frozen
  `run_row` still returns `(None, 'COMMAND_BINDING_SELFTEST: 19/19 pass')` — i.e. the C3 row stays
  "covered" while 25 of its 44 graded cases (57%) have vanished. The row is one of 7 of 30 that pin
  no tally (23/30 do: `44/44`, `cases=21 failed=0`, `(49/49 cases)`, …).
* **Compensation, measured:** the tally *is* pinned, elsewhere —
  `tools/registry.json` row `command-binding-selftest-r24` (active) carries
  `stdout_contains: ["COMMAND_BINDING_SELFTEST: 44/44 pass"]`, and `tools/registry-check.py`
  enforces it: `ROW command-binding-selftest-r24 expect=0 got=0 held` / `REGISTRY_CHECK: held=1/1`
  at CAND, but on the gutted-fixture lane `ROW … differs` / `held=0/1`, exit 1. So the shrink is
  caught by the entry-registry walk, **not** by this canonical row and **not** by the C3 counter
  (which never reads `registry.json`).
* The cell's second clause, "literal expected exits and finding IDs in the tool selftest", is true
  for **19 of 44** graded cases (17 base edits + `tampered` + `duplicate-json-key`, confirmed by the
  19/19 gutted run); the other 25 expectations live in the two pinned JSONs, which the same cell also
  names. Shading, not a falsehood.

**Write scope — TRUE to the syscall.** `strace -f` over the selftest: writes are exactly
`$TMPDIR/tameshi-command-binding-<rand>/bundle.json` and `…/expected.json` (one path pair, rewritten
once per case) plus the stdlib `tempfile` writability probe file (created and immediately unlinked in
`TMPDIR` itself, `O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW, 0600`). No lane write: `git status --porcelain`
is empty after the selftest and after every entry-mode run. Entry mode writes nothing at all (strace:
no `O_WRONLY`/`O_CREAT`/`mkdir`/`unlink` outside `/usr/lib`). `TMPDIR` is honoured (temp dir created
under it); with `TMPDIR` unset it falls back to `/tmp` (stdlib), and with a read-only `TMPDIR` the run
still exits 0 by falling back — so "under TMPDIR" is conditionally exact.

**Owner `tameshi` — TRUE.**

## 3. Two-evidences note (observation, not a row kill)

PROTOCOL §Gate standard "Two evidences" wants a run over a committed input snapshot with its committed
expected verdict. The canonical row names neither the frozen snapshot pair nor the frozen ruler,
although both exist at CAND and both reproduce here: `.ufo/evidence/round-23/replay/{bundle,expected}.json`
→ exit 0, sha `3d6c99b7…`; `.ufo/evidence/round-23/source-read-{bundle,expected}.json` → exit 1
`ARGV_MISMATCH`, sha `db620668…`; and the frozen ten-case ruler `.ufo/evidence/round-23/measure.py
--repo <clone>` → `tool_present True discriminated 10/10`, `tool_sha256 9230c68e…`. The pins live in
`tools/registry.json` (`command-binding-frozen-clean-pinned`, `command-binding-source-read-red-pinned`,
both active and held at CAND), not in this row — the same compensation as the tally.

## 4. Clone-context: this row is not the known blocker

The item's "row16 known clone-context failure" is **`tools/round21-measure.py`** (tools-base index 16
and table row 16 = `round21 measure facade`, SKILL.md:2157), not this tool (tools-base index 2, table
row 2). Reproduced in the *same* fresh clone, cwd=clone:

```
round21-measure.py --selftest  → rc=1, no stdout
  subprocess.CalledProcessError: Command '['git', '-C', '…/T51W2ExecTool02/tameshi-shokunin',
    'show', '08175c62d661fddf052ed10abc91313dec8eb77d:tools/mutate-and-run.sh']'
    returned non-zero exit status 128
command-binding.py --selftest  → rc=0, COMMAND_BINDING_SELFTEST: 44/44 pass
```

`command-binding.py` is clone-safe by construction (fixtures resolved from the tool file's own
`parents[1]`, tool:164; no absolute lane path anywhere in the file) and cwd-independent (verified
from `/` and `/tmp`).

## 5. What a reader of this row cannot get, and where to get it

| row cell | what it actually pins | where the real pin lives (verified) |
|---|---|---|
| Self-test | marker prefix only, no expected tally | `tools/registry.json` `command-binding-selftest-r24` → `44/44 pass`, enforced by `registry-check.py` (green at CAND, red on a gutted fixture) |
| Verdict map, `64 … (usage)` | nothing — 2 is also declared, so either code satisfies the probe | nowhere: a committed `64→2` fixture passes selftest, all three registry rows and the C3 probe |
| Pinned values | two file paths, no digest, no count | `registry-check.py` catches count loss via the 44/44 string; the fixture files themselves carry no digest pin |
| Entry command | shape only (`BUNDLE.json`/`EXPECTED.json` do not exist) | `.ufo/evidence/round-23/replay/{bundle,expected}.json`, `…/source-read-{bundle,expected}.json`, and `registry.json`'s two `*-pinned` rows |
| Two evidences | not pointed at | `registry.json` `command-binding-frozen-clean-pinned` + `command-binding-source-read-red-pinned` |

## 6. Bottom line

* Row 2143: **operable and truthful on kind, self-test, marker, pinned paths, write scope and owner.**
  The C3 counter covers it at line 2143 with exit 0 and the recorded marker.
* Falsifications found (all measured, none predicate-failing): entry command not runnable as written;
  exit-2 parenthetical narrower than the tool (unavailable input); "64 = usage" unenforced anywhere
  (a committed `64→2` mutant passes selftest, all registry rows and the C3 usage probe); exit 1 also
  absorbs tracebacks; no tally and no digest pin in the pinned-values cell, so case deletion
  (`19/19 pass`, exit 0) leaves this row and the C3 counter green — caught only by
  `tools/registry.json` + `registry-check.py`, which the C3 counter never reads.
* C3's `C3_R51_PASS=false` at CAND is attributable **solely** to `tools/round21-measure.py`
  (`MISSING (line 2157 selftest-exit=1 last=)`); this row is not a contributor.
