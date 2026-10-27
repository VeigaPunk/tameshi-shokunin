# T51ScribeRowGate — SOURCES row S272 for the kagi drift gate

Seat: T51ScribeRowGate (leaf, no subagents). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Item: draft SOURCES row S272 for kagi `corpus/drift-pins.sh` at rev `e64e81b8eb96f3682b00c1e7a291e84420b280fa`
targeted by C2's tenth mutation case, follow the 11-column schema and the S088 model row, draft the lesson
`## Gate` paragraph, validate a scratch registry copy with `scripts/sources-census.sh validate --file`.
Scope limit observed: I decide nothing about C2; everything below is an observation from this seat's own commands.

## 1. Provenance — what was opened, with the commands that show it

All reads of kagi are `git show` of the pinned blob (sibling lane is read-only); nothing was written there.

| fact | command | observed |
|---|---|---|
| rev exists, subject, date | `git -C …/kagi-shokunin show -s --format='%H %ci %s' e64e81b8eb96f3682b00c1e7a291e84420b280fa` | `e64e81b8eb96f3682b00c1e7a291e84420b280fa 2026-09-28 18:20:49 -0300 round-9: freshness axis-move — drift gate with committed baselines, transcript-gate correction` |
| blob sha256 | `git -C …/kagi-shokunin show e64e81b8…:corpus/drift-pins.sh \| sha256sum` | `c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb  -` (matches the contract's `c138d34c…`) |
| size | same blob `\| wc -l` | `451` |
| mode | `git -C …/kagi-shokunin ls-tree e64e81b8eb96f3682b00c1e7a291e84420b280fa corpus/drift-pins.sh` | `100755 blob 8a2903dc977a1ef6ea0430b21d1760392ccc2827\tcorpus/drift-pins.sh` |
| unchanged at kagi HEAD | `git -C …/kagi-shokunin diff --quiet e64e81b8eb96f3682b00c1e7a291e84420b280fa HEAD -- corpus/drift-pins.sh` | exit `0`; `git ls-tree HEAD` prints the same blob `8a2903dc…`; HEAD = `69b61db46be4ed955994f6f1d1cba522bc5f4e97` |
| worktree copy also clean | `git -C …/kagi-shokunin status --porcelain corpus/drift-pins.sh` | no output |
| the pin is executable, not just readable | blob extracted to the seat's scratch dir, `TMPDIR=<scratch>/t bash <scratch>/t/drift-pins.sh --selftest` | `DRIFT_SELFTEST: PASS (13 cases)`, exit `0` |

Locations used in the row's anchor cell (line numbers of the pinned blob):

- `:19` — exit map: `# Exit      0 clean · 1 any drift · 2 usage/setup error (nothing written)` (`sed -n '19p'`).
- `:118-259` — `verify()` from its definition (line 118) through its closing brace (line 259); `pin()` starts at 262.
- `:374-446` — `selftest()` definition through its closing brace; the mode dispatch `case "$MODE" in` is at 448.
- `:400-405` — the per-case assertion inside `run()`: `out=$(…)` (400), exit-code compare (401), and the unanchored
  verdict-word check `elif ! grep -q "$3" <<< "$out"; then` (403).
- 13 `run` calls at `:408-438` (`grep -c '^  run "' → 13`), and the count is what the gate itself prints at `:444`.

## 2. The row (deliverable)

11 cells, 12 pipes, no `|` inside any cell. Insert after the S271 row, i.e. after `corpus/SOURCES.md:146`,
before the blank line that precedes `## Paths` at `corpus/SOURCES.md:148`.

```text
| S272 | kagi `corpus/drift-pins.sh` (fleet gate, read-only) — kagi-shokunin/corpus/drift-pins.sh | code | A | the gate's own verdict vocabulary, exit map and hermetic scratch-tree selftest at the measured revision | :19 (exit map), :118-259 (verify), :374-446 (selftest), :400-405 (the exit-and-grep assertion) @ e64e81b8eb96f3682b00c1e7a291e84420b280fa (blob sha256 c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb, 451 lines, mode 100755; unchanged at kagi HEAD 69b61db46be4ed955994f6f1d1cba522bc5f4e97) | a host-drift gate anchors on committed baselines instead of live fingerprints and proves each verdict class in a scratch tree; its 13-case `--selftest` prints `DRIFT_SELFTEST: PASS (13 cases)` and asserts exit code plus an unanchored `grep -q` for the verdict word, not its position in the output | mined | 2026-10-26 | 180d | corpus/knowledge/mutation-case-kagi-drift-pins.md |
```

Same bytes as `T51ScribeRowGate.row.txt` (905 B, 906 B with its trailing newline). Schema checks against `CORPUS.md` §SOURCES.md: `id` is the next unused with no `|` in any cell (`CORPUS.md:89`),
kind `code` ∈ enum (`CORPUS.md:91-92`), tier `A` for the source code of the gate (`CORPUS.md:93-97`), anchor names
lines plus a revision (`CORPUS.md:99-100`), `teaches` is one grounded benefit (`CORPUS.md:101`), status `mined`
because the row has a used-by path (`CORPUS.md:103`), `opened` is this round's date and `recheck` is the `180d`
cadence (`CORPUS.md:105`), `used-by` is one repo-relative path (`CORPUS.md:107`).
Id S272 is the next unused at `corpus/SOURCES.md:498` (`- Next unused id: S272 …`), and `grep -c '^| S272 ' corpus/SOURCES.md`
prints `0`, so nothing collides.

## 3. The lesson `## Gate` paragraph for S272

Paste-ready as a bullet under `corpus/lessons/round-51.md ## Gate` (same shape as the round-50 bullet at
`corpus/lessons/round-50.md:19`, under `## Gate` at `corpus/lessons/round-50.md:13`):

- **S272** — kagi `corpus/drift-pins.sh`, the fleet's host-drift gate, at rev `e64e81b8eb96f3682b00c1e7a291e84420b280fa`
  ("round-9: freshness axis-move — drift gate with committed baselines, transcript-gate correction", 2026-09-28
  18:20:49 -0300), opened 2026-10-26. Opening command and pin: `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show
  e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh | sha256sum` → `c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb`,
  451 lines, mode `100755` (`git ls-tree`); `git diff --quiet e64e81b8 HEAD -- corpus/drift-pins.sh` exits 0 and
  `git status --porcelain` is empty, so the blob is unchanged at kagi HEAD `69b61db46be4ed955994f6f1d1cba522bc5f4e97`.
  Tier A (the gate's own source, read-only). Quote (15 words), header comment `:6-7`: "v2 compares the live host
  against two committed baselines and exits non-zero on any change." Second quote (8 words), usage block `:31`:
  "drift-pins.sh --selftest      scratch-tree proof that the gate fires". The pin was exercised as well as read: the
  extracted blob run as `bash drift-pins.sh --selftest` with `TMPDIR` inside this seat's scratch dir exits 0 and
  prints `DRIFT_SELFTEST: PASS (13 cases)` — 13 `run` calls at `:408-438`, each asserting an exit code and then an
  unanchored `grep -q` for the verdict word (`:400-405`). Recheck `180d`; the re-verify is
  `git show <new-rev>:corpus/drift-pins.sh | sha256sum` against the anchor cell's, plus one `--selftest` run.

## 4. Census validation of a scratch registry copy

Method: the copy must sit in a lane-shaped root, because `scripts/sources-census.sh:501` resolves a used-by path
against `dirname(--file)/..` and `:567` emits E11 when the path is absent. My scratch root
`$S/reg/corpus/` therefore holds a real copy of `SOURCES.md` plus symlinks `knowledge → lane corpus/knowledge`,
`lessons → lane corpus/lessons`, and `$S/reg/tools → lane tools`; the lane itself was never written.

**4a. Control — the unmodified copy (no S272), exit 0** (`T51ScribeRowGate.validate-base.out`, 15 W-lines + `ok`):
run at the same mirrored root before the row was appended —
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/reg/corpus/SOURCES.md --today 2026-10-26`
over a verbatim `cp` of the lane's `corpus/SOURCES.md`. 15 warnings, all pre-existing (`W01 S101`, `W04` on 14 rows),
and no E-line; the same 15 the round-49 lesson records (`corpus/lessons/round-49-verifier-spotcheck.md:111`).

**4b. With S272 appended — the run the item asks for** (`T51ScribeRowGate.validate-row.out`, exit **1**):

```
file	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
file	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
file	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
file	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
file	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
file	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
file	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
file	W04	S092 duplicate url bazel.build/remote/caching across scopes
file	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
file	W04	S104 duplicate url cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303 across scopes
file	W04	S160 duplicate url stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants across scopes
file	W04	S265 duplicate url testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html across scopes
file	W04	S266 duplicate url pitest.org/quickstart/incremental_analysis across scopes
file	W04	S267 duplicate url github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml across scopes
file	W04	S268 duplicate url www.tensorflow.org/federated/golden_tests?hl=zh-cn across scopes
file	E11	S272 missing used-by corpus/knowledge/mutation-case-kagi-drift-pins.md
```

Exit: **1**. The single new line is E11 on S272 and it is a real disk fact, not a row defect: the entry
`corpus/knowledge/mutation-case-kagi-drift-pins.md` does not exist yet (`ls` → "No such file or directory"; it is the
C2 entry seat's deliverable, which the L1 copies into place). No new W-line is raised by the row.

**4c. Same copy, entry path present** (`T51ScribeRowGate.validate-standin.out`, exit **0**): with a scratch stand-in
file at the cited path (labelled "SCRATCH STAND-IN: shape probe only, not evidence"), the same 15 W-lines print and
then `file	ok	…/regw/corpus/SOURCES.md`. That isolates 4b's E11 as the only thing standing between the row and a
clean registry, and shows the row adds no warning of its own.

**4d. Sensitivity probes** (`T51ScribeRowGate.probes.out`) — each mutates only the S272 row to show the census reads
its cells, then re-validates:

| probe | exit | finding |
|---|---|---|
| P0 row unmodified | 0 | `ok` only |
| P1 id `S272`→`S271` | 1 | `E03 S271 duplicate id` |
| P2 kind `code`→`source` | 1 | `E05 S272 kind=source` |
| P3 tier `A`→`C` | 0 | `W01 S272 tierC mined used-by=…` |
| P4 status `mined`→`watched` | 1 | `E07 S272 status=watched` |
| P5 recheck `180d`→`180 days` | 1 | `E09 S272 recheck=180 days` |
| P6 recheck `180d`→`2026-13-45` | 1 | `E09 S272 recheck=2026-13-45` |
| P7 recheck `180d`→`soonish` | 0 | `ok` only — any all-alphabetic token is taken as a symbolic cadence |
| P8 opened `2027-06-01` | 1 | `E08 S272 opened=2027-06-01` |
| P9 kind `community` at tier A | 1 | `E10 S272 community-at-A` |
| P10 closing pipe removed | 1 | `E01 S272 fields=10` |
| P11 faithful root, entry absent | 1 | `E11 S272 missing used-by …` |

## 5. Findings

- **F1 — the row is mined against a path that does not exist yet.** `corpus/SOURCES.md:147` (after the append) cites
  `corpus/knowledge/mutation-case-kagi-drift-pins.md`; `ls /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/mutation-case-kagi-drift-pins.md`
  → No such file or directory at 2026-10-26. `scripts/sources-census.sh validate --file <scratch copy>` → exit 1,
  `E11 S272 missing used-by corpus/knowledge/mutation-case-kagi-drift-pins.md`. This row must not land before that
  entry (the C2 entry seat's deliverable, which the L1 copies into place), because C1's predicate — "every used-by
  path of a mined row exists at REV" — and the fleet census both read the same cell.
- **F2 — the anchor is stable, so the pin in the anchor cell is exact.** `git -C …/kagi-shokunin diff --quiet
  e64e81b8… HEAD -- corpus/drift-pins.sh` → exit 0, `git ls-tree HEAD` → `100755 blob 8a2903dc…`,
  `git status --porcelain` empty. Blob sha256 of the rev equals the contract's `c138d34c…`.
- **F3 — the selftest claim in `teaches` is executed, not inferred.** Pinned blob run with `--selftest` prints
  `DRIFT_SELFTEST: PASS (13 cases)` and exits 0; the same 13 is the count of `run` calls at `:408-438`. The assertion
  shape the C2 seats probe is at `:400-405` — exit code first, then `grep -q "$3" <<< "$out"` on the verdict word with
  no anchor and no position check.
- **F4 — the census accepts any all-alphabetic `recheck` as a symbolic cadence.** Probe P7: `recheck = soonish` →
  exit 0, no E09, while `180 days` and `2026-13-45` are caught. Not a defect of this row (`180d` is a valid cadence
  and is caught by the numeric branch); reported because `E09`'s documented coverage is narrower than it reads.
- **F5 — method note for the deciding run.** A `SOURCES.md` copy outside a lane-shaped root makes E11 fire on every
  relative used-by path it cannot resolve: with only `corpus/knowledge` mirrored, the same registry copy printed
  32 E11 lines (28 on `corpus/lessons/*`, 4 on `tools/*`); with no mirrors at all it printed 160 E11 lines (measured
  in scratch, both runs). The cause is resolution against `dirname(--file)/..` (`scripts/sources-census.sh:501`,
  E11 emitted at `:567`). The receipts above come from a root mirrored with `corpus/knowledge`, `corpus/lessons` and
  `tools`, so their E/W set is comparable to a lane run.

## 6. Touched surfaces and out-of-scope

- Written: this report plus `T51ScribeRowGate.row.txt`, `.validate-base.out`, `.validate-row.out`,
  `.validate-standin.out`, `.probes.out` in `.ufo/waves/round-51/w1/`. Nothing else.
- Not written: the lane checkout (`corpus/SOURCES.md`, `corpus/knowledge/`, SKILL.md, tools, `.ufo/evidence/round-51/`),
  the kagi checkout, the fleet repo, any sibling lane, any Git index or jj state. No `git add/commit/stash/checkout/…`,
  no mutating jj command, no `agent://all`. The pinned blob was read with `git show` and run only from a scratch copy.
- Scratch: `/fast/scratch/hyaku/tameshi-r51/T51ScribeRowGate` (registry copies, `regw`, `regp_*`, extracted blob) —
  deleted before yielding; the receipts under `.ufo/waves/round-51/w1/` are the citable copies. `/tmp/dp.sh` (a
  decoded copy of the blob used for line-numbering) is not cited anywhere above.
- No tool was installed or upgraded this seat; no pacman transaction was attempted.
- Out of scope by assignment: writing `corpus/knowledge/mutation-case-kagi-drift-pins.md`, appending the row to
  `corpus/SOURCES.md`, any verdict on C2, and the S273 row (GNU Bash `set` builtin, another seat).

Checks for the main agent, after the C2 entry lands: append `T51ScribeRowGate.row.txt` after `corpus/SOURCES.md:146`,
then `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
— expect exit 0 with the same 15 W-lines and no E-line for S272. Then the C2/C1 counters (`--explain`) read the
status/used-by pair this row supplies.

## Summary

- S272 drafted for kagi `corpus/drift-pins.sh` @ `e64e81b8…`: blob sha256 `c138d34c…`, 451 lines, mode `100755`, identical at kagi HEAD `69b61db` with a clean worktree.
- 11 cells, no `|` inside a cell; S272 is next-free (`corpus/SOURCES.md:498`); append after `corpus/SOURCES.md:146`.
- Pin executed, not just read: `--selftest` → `DRIFT_SELFTEST: PASS (13 cases)`, exit 0; the exit-and-unanchored-`grep -q` assertion sits at `:400-405` and is named in `teaches`.
- Census with the row: exit 1, one new line `E11 S272 missing used-by …`; with that path present: exit 0, the same 15 pre-existing W-lines.
- 12 probes (1 control, 11 row mutations) show the census reads every cell (E01, E03, E05, E07, E08, E09, E10, E11, W01).
- The row must not land before the C2 entry: C1 requires every mined row's used-by path to exist.
