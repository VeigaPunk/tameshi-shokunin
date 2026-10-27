# T51W2ExecTool13 — C3 registry row audit: `tools/registry-check.py`

Round 51 wave 2, lane `tameshi-shokunin`, base `9962033f`, candidate `6d8c11e378aa90b12650808e1b79270742935f15`.
Axis: operability. Milestone: C3 row falsification. Scope: **one row**, read-only on the lane; no source, row or
counter byte was modified. Every measurement below ran from one `git clone --shared` of the lane at CAND
(`git rev-parse --show-toplevel` = `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool13/cand`, HEAD =
`6d8c11e378aa90b12650808e1b79270742935f15`) with `TMPDIR` under the seat scratch and stdin `/dev/null`. All repo
bytes are `git show 6d8c11e…:<path>`, never the lane worktree. Raw receipts: `T51W2ExecTool13/`.

**Bottom line.** The row is **counter-conformant and true in every field I can execute** — kind, exit map,
pinned paths, write scope and finding id all check out — and its self-test is **not** the known clone-context
failure (`round21-measure.py`). I found **one factual mismatch** (`M1`: the quoted last line carries a rev stamp
the tool never prints, and the frozen counter cannot see it), **one conformance gap** (`M2`: `64 usage` names no
class), and three disclosures (`M3`-`M5`). Nothing here flips the frozen predicate; `M1` is a seam an honest
canonical row already sits on.

| id | severity | one line |
|---|---|---|
| M1 | **material (to cold-read truth)** | cell quotes the last line as `SELFTEST: PASS (51 cases) at 84aa673`; the tool prints `SELFTEST: PASS (51 cases)` — at CAND **and** at `84aa673`, and no revision of the tool ever emitted `cases) at`. The counter compares only the **first token** (`measure.py:178-180`), so the row is still credited. |
| M2 | low (conformance) | verdict map ends `64 usage` — the code is declared but not **mapped onto `clean|failed|could-not-evaluate`** as `PROTOCOL.md:380-382` requires; 14 of the 16 rows in the section that declare a `64` write `64 could-not-evaluate (usage)`. |
| M3 | disclosure (operability) | `--rev` clones the **whole graded lane** into hardcoded `/tmp`; measured 193 MB for this lane. The row says "fixture trees via mkdtemp under /tmp" — right in kind, silent on size. |
| M4 | disclosure | pinned `tools/registry.json` is load-bearing for the **entry command only**; corrupting it leaves the self-test green (measured). |
| M5 | informational | the human verdict line `REGISTRY_CHECK: held=N/M superseded=K` names no revision (`print_human`, `:887-909`); only `--json` carries `rev_resolved`, and the registered entry command omits `--json`. |

---

## Reader statement (for the L1's re-key)

I read the section `#### Gate/probe registry — round 51`, which at CAND is **SKILL.md:2138 to EOF** (file is 2172
lines; no later heading) and holds **30 data rows**. The audited row is **SKILL.md:2154**, the **13th data row**;
line sha256 (without trailing newline) `3799c393cbb5c54ae8d64ca7d937bba1459588c8f6b47b0b1b135335bb5be1f8`. The
earlier `### Gate/probe registry` at `SKILL.md:1499` holds the round-12 rows and **no** `registry-check` row, so a
re-key aimed at that heading is not covered here.

I verified the section's claims against candidate bytes rather than restating them: `tools/registry-check.py` at
CAND is sha256 `cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad`, 70 609 B, **1954 lines**;
`tools/registry.json` at CAND is sha256 `c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c`,
26 860 B, schema `tameshi-entry-registry-v1`, 56 rows (49 active / 7 superseded). Seat **T51W2ExecTool13** is the
named reader for the heading `#### Gate/probe registry — round 51`.

## The row under audit (verbatim, SKILL.md:2154)

```
| entry-registry walk | gate | `python3 tools/registry-check.py --rev HEAD` (add `--only NAME` to grade one row) | 0 clean; 1 failed; 2 could-not-evaluate (registry unreadable or invalid, root/rev/clone failure, only or tag miss); 64 usage | `python3 tools/registry-check.py --selftest` → finding id SELFTEST: last line SELFTEST: PASS (51 cases) at 84aa673 | `tools/registry.json`, `tools/registry-check.py` | selftest and --rev fixture trees via mkdtemp under /tmp (hardcoded, TMPDIR ignored), removed afterwards; live --root mode runs registry rows inside LANE so rows may write there | tameshi |
```

## Verdict

**The row passes the frozen C3 predicate for this tool**, and this is **not** row16's clone-context blocker:
table row 12 (`SKILL.md:2153`) is `receipt-window validity`; the known blocker belongs to
`tools/round21-measure.py`, while this tool's self-test is green from a fresh lone clone. I imported the counter's
own predicate functions from the frozen `.ufo/evidence/round-51/c3/measure.py` and ran them against CAND:

```
row_reason -> None
  selftest argv ['python3','tools/registry-check.py','--selftest']
  usage    argv ['python3','tools/registry-check.py','--r51-no-such-flag']
run_row -> (None, 'SELFTEST: PASS (51 cases)')
```

(`T51W2ExecTool13/08-counter-predicate.json`.) Marker `SELFTEST:` is present in the self-test cell; usage exit
`64` is present as a token in the verdict map.

## Measured runs (row's exact commands, stdin `/dev/null`, TMPDIR an existing scratch dir)

| # | command (cwd = CAND clone) | rc | last line | wall |
|---|---|---|---|---|
| R1 | `python3 tools/registry-check.py --selftest` | **0** | `SELFTEST: PASS (51 cases)` | **14.16 s** (repeats 14.02 / 18.77 / 19.57 s) |
| R2 | same, at `84aa673a1a476e48ccf239335696f0518d08bae7` (the row's stamped rev) | **0** | `SELFTEST: PASS (51 cases)` | 16.40 s |
| R3 | `python3 tools/registry-check.py --r51-no-such-flag` | **64** | stderr last `       registry-check.py --selftest` (stdout **empty**, 0 lines) | 0.03–0.04 s |
| R4 | 8 throwaway-registry cases (below) | 0 / 1 / 2×6 | see `05-exit-matrix.json` | 0.04–0.51 s |
| R5 | `--rev HEAD` on a fixture fleet lane | **0** | `REGISTRY_CHECK: held=1/1 superseded=0` | 0.52 s |
| R6 | counter predicate (imports `row_reason`, `run_row`) | (None, green) | `SELFTEST: PASS (51 cases)` | 14.50 s |
| R7 | corrupt `tools/registry.json` → self-test / entry | **0 / 2** | (`SELFTEST: PASS…` / `registry invalid: schema…`) | 19.57 s / 0.04 s |

Self-test shape: **51** `SELFTEST_CASE … PASS` lines, 0 FAIL, 52 stdout lines total, **0 bytes stderr**
(`02-selftest-cand.stdout`, `.json`). Clone `git status --porcelain` is **empty** after every run: the self-test
does not touch the tree it runs in.

## Field-by-field audit

1. **Kind `gate` — true, not a probe.** Exit 1 is reachable on a genuine registration failure: a fixture row that
   exits 0 while the registry expects 7 yields `REGISTRY_CHECK: held=0/1 superseded=0`, rc **1**. Reproduced twice
   (live `--root` and `--rev`; R4/R5). Source: `evaluate` returns `0 if held == len(active) else 1` (`:884`).
2. **Entry command `--rev HEAD` and `--only NAME`.** Both exercised. `--rev` resolves `REV^{commit}`, clones into a
   fleet-mirror dir, checks out detached, reports `rev_resolved`, and the mirror works: a fixture row asserting
   `os.path.exists('../peer-shokunin')` from the clone's cwd returns `held` (R5) — i.e. the sibling symlinks the
   docstring promises are actually made (`:763-789`). `--only` selects one row (`held=1/1`, rc 0), an `--only`/`--tag` conflict and a miss are rc 2,
   and `-h` is rc 0 with 69 stdout lines (`11-only-and-help.json`).
3. **Verdict map — every code and meaning reproduced.**

   | row claim | measured |
   |---|---|
   | `0 clean` | `held=1/1` → rc 0 |
   | `1 failed` | `held=0/1` (expect 7, got 0) → rc 1; also `got=non-hermetic differs` → rc 1 |
   | `2` registry **invalid** | `registry invalid: schema must be 'tameshi-entry-registry-v1'` → 2 |
   | `2` registry **unreadable** | `registry unreadable: … [Errno 2] No such file…` → 2 |
   | `2` **root** failure | `root_unavailable: …` → 2 |
   | `2` **rev** failure | `rev 'deadbeef…' unavailable in …` → 2 |
   | `2` **only** / **tag** miss | `--only 'nope' matches no registry row`, `--tag ['nomatch'] selects no registry row` → 2 |
   | `64 usage` | `unknown argument '--r51-no-such-flag'` + usage block → 64 |

   Source paths: `:849,855,866,871` (could-not-evaluate), clone failure `:1910-1922` → 2, `:1866` →
   `usage_failure` `:134-139` → 64, `:884` (0/1). No **undeclared** code exists: a row timeout is `got=timeout`
   (→ differs → 1), `-h/--help` is 0 (`:1845`), `SIGTERM` raises `SystemExit(2)` (`:1823-1824`), an uncaught
   traceback is 1. The class-mapping nit is `M2`.
4. **Self-test cell.** Exactly one backticked command, no shell metacharacters, argv
   `python3 tools/registry-check.py --selftest` — byte-for-byte what I ran. The finding id `SELFTEST:` is a real
   diagnostic, emitted only after all 51 cases pass, with the case count (`:1813-1816`); it is **not** help text.
   The count **51 is correct**. The trailing ` at 84aa673` is **not** tool output (`M1`).
5. **Pinned values.** `tools/registry.json` (26 860 B) and `tools/registry-check.py` (1954 lines) both exist at
   CAND and both bind something real: `registry.json` is the default registry for `--rev` (`:1924`, `:1928`), so
   corrupting it turns the entry command into rc 2; the 51 self-test expectations are literals inside the tool, so
   the tool pins itself. But the pin does **not** bind the self-test (`M4`, R7).
6. **Write scope — exact, including the negative.** `tempfile.mkdtemp(..., dir="/tmp")` appears at `:766-767`
   (`--rev` clone) and `:916-918` (self-test); `TMPDIR` is never consulted. Measured: with `TMPDIR` pointed at an
   empty scratch dir it stayed **empty**, while 8 trees (`tameshi-r17-registry-check-selftest.*`,
   `tameshi-registry-check-*`) appeared under `/tmp` and **none** remained at exit
   (`07-tmp-write-scope.json`). Live `--root` mode warns on stderr (`:1933-1936`) and runs rows with `cwd=root`
   (measured: warning text identical to the row's disclosure). Magnitude is `M3`.
7. **Owner** `tameshi` — present, matches every other row in the section.

## M1 — the quoted last line is not what the tool prints (the counter's blind seam)

Row cell: `… last line SELFTEST: PASS (51 cases) at 84aa673`. Actual, both revs:

```
$ python3 tools/registry-check.py --selftest | tail -1
SELFTEST: PASS (51 cases)
```

- CAND: 51 cases, last line as above (`02-selftest-cand.stdout`, line 52).
- At the stamped rev `84aa673`: same 51 cases, same last line (`03-selftest-84aa673.stdout`, run from
  `git show 84aa673:tools/registry-check.py`). Its emitter is the same `emit(f"SELFTEST: PASS ({passed} cases)")`.
- `git log -S'cases) at ' -- tools/registry-check.py` returns **no commit**: no revision of this tool ever printed
  a rev. The stamp was added by CAND's own commit (`git log -S'51 cases) at 84aa673'` → only `6d8c11e`).

Read as provenance ("observed at 84aa673") it is defensible — the section's `evidence disposition` row writes the
same idea as `at rev 84aa673` — but as written the phrase is inside the quoted last line, so a cold reader that
diffs the cell against output finds text the tool never emits. The frozen counter cannot catch it: `run_row`
compares only `last.split()[0]` (`measure.py:178-180`), so any suffix after the first token of a quoted last line
is unchecked, and the same seam would let an author write a marker that is not a diagnostic at all. Here the
marker itself is honest; only the suffix is air.

## M2 — `64 usage` names no class

`PROTOCOL.md:380-382` (fleet root): "`0` = `clean` and `1` = `failed` fleet-wide; every other code a gate exits
(`2`, `3`, `64`, …) is declared in its registry entry **and mapped onto `clean | failed | could-not-evaluate`**".
This row declares `2 could-not-evaluate (…)` with its class and then writes `64 usage` — code and reason, no class.
Section convention: 14 of the 16 rows that declare a `64` say `64 could-not-evaluate (usage)` (or `(invalid_usage)`); only this row and the
adjacent `receipt-window validity` row (`:2153`, same commit) use bare `64 usage`. The code is not hidden, so the
counter and any exit-code census still see it; only the class mapping the standard asks for is missing.

## M3 — a redacted but real magnitude: `--rev` writes ~193 MB into `/tmp`

`clone_lane_at_rev` runs `git clone -q --no-hardlinks <lane> …` into `mkdtemp(dir="/tmp")` (`:766`, `:782`, `:784-789`) — a full
clone of the graded lane, not a small fixture. Measured on this lane at CAND with the same clone flags:
`du -sh` → **193 MB** (`.git` 72 MB, worktree the rest; deleted immediately, nothing left in my scratch). The tool
removes it afterwards (verified twice by poller, `left_behind: []`), so the row's "removed afterwards" is true; the
size is the undisclosed part. On this host `/tmp` was already at ~1.8 GB used, so a `--rev` run is a 193 MB peak —
worth knowing before a wave runs 60 of them at once.

## M4 — the pin binds the entry command, not the self-test

With `tools/registry.json` in the clone replaced by `{"schema":"broken-by-audit"}`:

| command | rc | last line |
|---|---|---|
| `--selftest` | **0** | `SELFTEST: PASS (51 cases)` |
| `--root . --registry tools/registry.json` | **2** | `could-not-evaluate (registry invalid: …)` |

`09-pin-effect.json`; the file was restored and its sha256 re-verified identical (`c1b75366…`). So the pinned
registry is load-bearing exactly where the entry command reads it, and the self-test is hermetic with respect to
it. The row's pinned cell does not say which column the pins bind; nothing false, but a reader who assumes the
self-test consumes the registry would be wrong.

## M5 — the human verdict names no revision

`print_human` (`:887-909`) emits `ROW <name> expect=<e> got=<g> held|differs` and
`REGISTRY_CHECK: held=<N>/<M> superseded=<K>`; the resolved sha appears only in the `--json` report
(`rev_resolved`, measured `2ebb2f68…` on my fixture, `06-rev-fixtures.json`) and in nothing the default invocation
prints. `PROTOCOL.md:393-394`: "A verdict names the revision it was measured against". The registered entry
command `--rev HEAD` therefore produces a receipt that cannot be compared to a later run without re-resolving
`HEAD`. Not a row-field mismatch; flagged because this row is the lane's registry walk.

## Positive receipts worth keeping

- **Hermetic self-test**: 51/51, rc 0, from a lone clone; the clone's worktree is unchanged afterwards; fixtures
  under `/tmp`; `TMPDIR` honoured nowhere (the row discloses this, which is precisely what tells a reader that the
  C3 counter's per-command `TMPDIR` isolation does not apply to this tool).
- **`external: true` does its job**: the only registry row carrying an absolute live-fleet token is
  `pin-disposition-read` (`--root /home/vgpnk/Projects/shokunin`), and it declares `"external": true`. I confirmed
  the branch it avoids: an undeclared absolute fleet token yields `got=non-hermetic differs` → rc 1, the declared
  one runs and holds → rc 0 (`06-rev-fixtures.json`). No spurious refusal exists at CAND.
- **`--json` splits streams** as documented: machine report on stdout, `ROW`/`REGISTRY_CHECK` lines on stderr.

## Not measured (stated, not hidden)

- The **real** `python3 tools/registry-check.py --rev HEAD` at CAND (the entry cell's `0 clean`). It clones this
  lane into hardcoded `/tmp` at ~193 MB (`M3`), above my seat's `<50 MB` /tmp bound, so I refused to run it rather
  than break the bound. The machinery and all four verdict classes were instead exercised on throwaway lanes and
  registries (R4/R5). Whether all 49 active rows hold at CAND is therefore **unverified by this seat**; the
  registry's own timeout sum is 7740 s over 6 workers.
- The frozen counter end-to-end (C3 is the L1's deciding run). I reused its predicate functions on this row only.

## Files written

- `.ufo/waves/round-51/w2/T51W2ExecTool13.md` (this report)
- `.ufo/waves/round-51/w2/T51W2ExecTool13/` — `01-row-cells.json`, `02-selftest-cand.{stdout,stderr,json}`,
  `03-selftest-84aa673.{stdout,json}`, `04-usage-probe.json`, `05-exit-matrix.json`, `06-rev-fixtures.json`,
  `07-tmp-write-scope.json`, `08-counter-predicate.json`, `09-pin-effect.json`, `10-env.txt`,
  `11-only-and-help.json`.

Nothing else in the lane, fleet root, sibling repos or PATH was written; no git/jj mutation was made in any repo
(fixtures only, each `rev-parse --show-toplevel` asserted before committing; the scratch clone's `registry.json`
was corrupted and restored with sha256 verification). Scratch root `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool13`
was deleted before yield; no `/tmp` residue (verified `left_behind: []`).

## Risks

- **For the counter, not the row**: `measure.py:178-180` grades a quoted last line by its first token only. `M1` is
  a live canonical-row instance of that seam, so a future row could carry an invented suffix (or an inventor could
  pick a first token that is not a diagnostic) and still be credited. Fixing that is the L1's call; the row as
  filed only overstates by a rev stamp that happens to be true about *when* it was observed.
- **The entry-cell `0 clean` is the one unverified claim** in the row; a deciding run needs ~193 MB of `/tmp` and a
  long wall, and `pin-disposition-read` will read the live fleet root (declared, `fleet-live` tag).
