# T56W1ExecCensus — round 56 wave 1: census receipts and the after-harness

Seat: `T56W1ExecCensus` (leaf executor). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Lane HEAD at work time: `c3e2ca9f020776b3d66c7af854fb82c834674fcf` (the frozen instrument set).
Claim base: `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`.

Verdict of this seat: **complete, no lane production file touched, no registry row edited.**
`corpus/SOURCES.md` is byte-identical at base, at HEAD and in the worktree
(`57ece0e5716deb46ec9d1d6c0c076beab31a9ba82ad323a68e85450b429be112`, three-way, diff empty).

---

## 1. (a) The census at base

Exact command, run from the fleet root:

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin tameshi
```

| fact | value | receipt |
|---|---|---|
| exit code | **0** | `T56W1ExecCensus-receipts/census-validate-base.exit` |
| stdout | 17 lines: 16 W findings + `tameshi ok <path>` | `…/census-validate-base.stdout` |
| stderr | empty (0 bytes) | `…/census-validate-base.stderr` |
| rows, census mode | **140** | `…/census-count-base.stdout` (`tameshi rows 140`, `FLEET rows 140`) |
| rows, `grep -cE '^ {0,3}\| S[0-9]{3,} \|' corpus/SOURCES.md` | **140** | `…/rows-grep-count.txt` |

The two row readers agree, so `rows=140` is not one parser's opinion.

Census-mode distribution at base (same receipt):

```
tameshi rows 140 · tier.A 125 · tier.B 12 · tier.C 3 · tier.invalid 0
tameshi status.mined 113 · status.queued 21 · status.rejected 6 · status.invalid 0
FLEET  rows 140 · missing 0
```

**Warning inventory (16, no E codes):** `W04` ×15 — S047, S048, S075, S076, S077, S078, S081,
S092, S104, S160, S265, S266, S267, S268, S274 (same normalized URL across scopes) — and
`W01` ×1 — S101 (tier C, mined, used-by `corpus/knowledge/witness-equivalence-rule.md`).
Zero `E01`–`E12`. `validate` exit 0 therefore means *no E findings*, **not** "nothing found":
W codes never change a lane's status. The L1 must not paste "census clean" without the W
inventory, or the row count is the only thing the sentence carries.

**Why this is "at base" although the tree is at the freeze commit.** `git diff 981c5e8b… c3e2ca9f… -- corpus/SOURCES.md`
is empty (exit 0, no output), and the file hashes equal at base, at HEAD and in the worktree:

```
57ece0e5716deb46ec9d1d6c0c076beab31a9ba82ad323a68e85450b429be112  (git show 981c5e8b:corpus/SOURCES.md)
57ece0e5716deb46ec9d1d6c0c076beab31a9ba82ad323a68e85450b429be112  (git show HEAD:corpus/SOURCES.md)
57ece0e5716deb46ec9d1d6c0c076beab31a9ba82ad323a68e85450b429be112  (worktree corpus/SOURCES.md)
```

Receipts: `…/sources-identity-base-vs-head.diffstat`, `…/sources-sha256-{base,head,worktree}.txt`.

**Id space (checked, needed by C0).** 140 rows carry ids S001…S280; the tail of `SOURCES.md`
states `Next unused id: S281` (staged S161–S255 stay reserved by document). So the round-56
registry cell is **S281**, and `census-after.sh` at C0 must read `new_rows=1`, not 0.

---

## 2. (b) `.ufo/waves/round-56/census-after.sh`

Written to `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/census-after.sh`
(mode 755, `bash -n` clean). Read-only: it writes stdout (or `--out`) and a `mktemp -d` temp
dir that a `trap` removes; it never opens the registry for writing and never touches git state.

What it does, in order:

1. Resolves the registry (`--sources`, default `LANE/corpus/SOURCES.md`) and the base
   revision (`--base`, default = the `base` field of `.ufo/evidence/round-56/contract.json`,
   i.e. `981c5e8b…`). A base that is not a commit in the lane is **fatal, exit 2** — the
   harness fails closed rather than treating every row as new or none.
2. Runs the census **unchanged**, twice: `validate` and `census`. The lane registry keeps the
   roster path (`--root <root> tameshi`); any other file is handed over as `--file`.
3. Prints the required line verbatim, then a reader self-check:

```
CENSUS exit=N rows=M
CENSUS_ROWS_SELFCHECK census=M grep=G
```

4. Shape-checks **every row new relative to `--base`** (id not present in
   `git show <base>:corpus/SOURCES.md`), one TSV line per finding, then a summary:

```
<label>	CENSUS_SHAPE	<id>	<CODE>	<detail>
<label>	CENSUS_SHAPE	new_rows=K findings=F
CENSUS_SHAPE_VERDICT pass=true|false new_rows=K findings=F rows_mismatch=false|true|n/a
```

Codes and what each refuses:

| code | refusal |
|---|---|
| `SHAPE_COLUMNS` | cell count ≠ 11 (`columns=N want=11`) |
| `SHAPE_PIPE` | escaped `\|` inside the row, or more than 12 literal `\|` characters (`literal pipes=N want=12`) |
| `SHAPE_OPENED` | `opened` not `YYYY-MM-DD`, not a real calendar day, or in the future |
| `SHAPE_STATUS` | `status` ∉ `queued|mined|rejected` |
| `SHAPE_SECTION` | the new row sits outside `## Registry` (a row that escaped the table is still a row) |

Cell-level checks run only when the pipe count is sound: an escaped pipe shifts every later
cell, so the harness names the pipe and does **not** also report the shifted cells as a bad
status or a bad date. That is deliberate — a shifted `status=inside the teaches cell` finding
would be a symptom, not the cause.

Exit codes: `0` clean · `1` shape findings or a row-count mismatch (`CENSUS_ROWS_SELFCHECK`
disagrees) · `2` usage / missing registry / unresolvable `--base` · otherwise the census's own
code (1 E findings, 2 env). `--shape-only` skips the census and prints
`CENSUS exit=skipped rows=-` with `rows_mismatch=n/a` instead of a false `exit=0 rows=0`.

### 2.1 Equivalence with the item's command

The harness's `validate` section is **byte-identical** to the item's exact command output:
`diff -u` between `census-validate-base.stdout` and the harness's first 17 lines is empty
(exit 0, no output) — receipt `…/census-validate-equivalence.diff`. The harness adds the
`census`-mode counts and the shape pass; it does not re-implement the census.

### 2.2 Clean-lane run (the control)

```
CENSUS exit=0 rows=140
CENSUS_ROWS_SELFCHECK census=140 grep=140
tameshi	CENSUS_SHAPE	new_rows=0 findings=0
CENSUS_SHAPE_VERDICT pass=true new_rows=0 findings=0 rows_mismatch=false
```

exit 0, stderr empty — `…/census-after-base.stdout`, `…/census-after-base.stderr`,
`…/census-after-base.exit`. `new_rows=0` at base is the expected measured no-change; it is
reported, never an error.

---

## 3. Demonstration: the shape check refusing malformed rows

Driver: `…/T56W1ExecCensus-receipts/census-after-demo.sh` (copy of the scratch driver).
Each case is a full copy of `corpus/` **and** `tools/` under
`/fast/scratch/hyaku/tameshi-r56/T56W1ExecCensus/<case>/lane/`, so the census's `E11`
used-by resolution stays honest and the census's own exit code is meaningful. One row, `S281`,
is inserted after the last registry row (or appended at EOF for `outside`). Base is
`981c5e8b…` from the contract.

| case | fixture | census verdict | shape verdict | exit |
|---|---|---|---|---|
| `clean` | S281, 11 columns, `queued`, `2026-10-28` | `CENSUS exit=0 rows=141`, no E | `new_rows=1 findings=0`, **pass=true** | **0** |
| `m10col` | S281 with the used-by cell dropped (10 cells) | `file E01 S281 fields=10`, exit 1 | `SHAPE_COLUMNS S281 columns=10 want=11` | 1 |
| `escpipe` | S281 with `pipe \| inside the teaches cell` | `file E01 S281 fields=12`, exit 1 | `SHAPE_PIPE S281 escaped pipe (\|) in row` | 1 |
| `baddate` | S281 `watch` / `2026-13-45` | `E07 S281 status=watch`, `E08 S281 opened=2026-13-45` | `SHAPE_STATUS status=watch`, `SHAPE_OPENED opened=2026-13-45 not an ISO calendar date` | 1 |
| `future` | S281 `2027-01-01` | `E08 S281 opened=2027-01-01` | `SHAPE_OPENED opened=2027-01-01 is in the future` | 1 |
| `outside` | S281 appended after the last section | `E12 S281 row outside Registry section`; `CENSUS rows=140` | `SHAPE_SECTION`, `CENSUS_ROWS_SELFCHECK census=140 grep=141`, `rows_mismatch=true` | 1 |
| `badbase` | `--base 0000…` | not run | fatal before any check | **2**, stdout 0 bytes |
| `shapeonly` | escpipe fixture, `--shape-only` | skipped (`CENSUS exit=skipped rows=-`) | `SHAPE_PIPE`, `rows_mismatch=n/a` | 1 |

Receipts: `…/census-after-demo-<case>.{stdout,stderr}`; the driver itself is
`…/census-after-demo.sh`.

The two refusals the item asks for are rows 2 and 3. Both are refused by the shipped census
**as well** — `E01` catches them, because `gawk -F'|'` splits on the escaped pipe exactly as on
a literal one. The harness's contribution there is the *diagnosis* (`SHAPE_PIPE … escaped pipe`,
against the census's `fields=12`, which reports a count without naming the cause) and the
scoping to the new row. Read this table as "the harness refuses, and names", not "the census
missed it".

---

## 4. What the harness adds, and what it cannot see

Adds, beyond the census (each shown above, not asserted):

- the exact `CENSUS exit=N rows=M` line a round record can quote without re-parsing TSV;
- **new-row scoping against a pinned base**: a C0 that forgets its registry row reads
  `new_rows=0`, and a C0 that adds two rows reads `new_rows=2` — the census alone cannot
  distinguish "no new row" from "new row that is fine";
- a **reader self-check** (`census=M grep=G`): the registry parser and a naive line grep must
  agree, and the `outside` mutant shows the disagreement it catches;
- named codes per refusal, including the `SHAPE_SECTION` case the census reports as `E12`;
- a fail-closed base (`exit 2`, empty stdout) instead of a silent all-old or all-new reading.

Cannot see (the honest limits):

- **An edited old row.** "New" is an id not present at `--base`; if the C0 author reuses an
  existing id (or edits S280 instead of appending S281), the shape pass skips that row. The
  census still validates every row (`E01`–`E12`), so a malformed edit is still caught there,
  but the shape codes will not fire. Flip: hash each row's raw line and diff the row set by
  content, not only by id.
- **Semantics.** It says nothing about whether the source is real, the tier is right, or the
  used-by path is appropriate — that is the census's `E`/`W` set and the C2 claim's business.
- **The census's own correctness.** The harness shells out to
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` and depends on its CLI
  (`validate|census`, `--root`, `--file`, `--today`); if that script's interface changes the
  harness breaks loudly (`die`, exit 2), not silently.

---

## 5. Falsification of this seat's own deliverable

- **No-op control**: `clean` (a valid new row) passes with `findings=0`, exit 0 — the check is
  not a refuse-all. `new_rows=1` proves the row was seen, not skipped.
- **Every documented code is exercised** except `SHAPE_PIPE`'s `literal pipes>12` branch: the
  escaped-pipe branch fires first on the fixture that would reach it (`\|` is one pipe char, so
  the escaped branch is always the true cause). Stated as a limit, not claimed as coverage.
- **Fail-closed base**: `badbase` exits 2 with no stdout.
- **No residue**: no `/tmp/census-after.*` directory survives a run (`ls -d /tmp/census-after.*`
  → 0), stderr is 0 bytes on every passing run, and the lane's `git status` shows no tracked
  file changed by this seat (`git status --porcelain | grep -v '^?? .ufo/'` → 0 lines).

---

## 6. Handoff notes for the L1

1. Paste for the round record: `CENSUS exit=0 rows=140` (base) with the W inventory
   (15×`W04`, 1×`W01`), never "census clean".
2. At C0, `census-after.sh` must print `CENSUS exit=0 rows=141` (140 + the new S281 cell) and
   `CENSUS_SHAPE_VERDICT pass=true new_rows=1 findings=0 rows_mismatch=false`. If `new_rows=0`,
   the registry cell did not land; if `pass=false`, read the code line — it names the defect.
3. Run it from any cwd with absolute paths; it does not depend on the caller's cwd (verified by
   running it from the fleet root).
4. Census conformance at round end is the same two commands (`validate` then `census`); the
   harness is the round-start/round-end instrument, the census remains the fleet authority.

---

## 7. Files written

- `.ufo/waves/round-56/census-after.sh` (new, executable)
- `.ufo/waves/round-56/w1/T56W1ExecCensus.md` (this report)
- `.ufo/waves/round-56/w1/T56W1ExecCensus.json` (machine-readable facts + demo matrix)
- `.ufo/waves/round-56/w1/T56W1ExecCensus-receipts/` (34 files, 88 KB):
  `census-validate-base.{stdout,stderr,exit}`, `census-count-base.{stdout,stderr,exit}`,
  `rows-grep-count.txt`, `sources-identity-base-vs-head.diffstat`,
  `sources-sha256-{base,head,worktree}.txt`, `census-validate-equivalence.diff`,
  `census-after-base.{stdout,stderr,exit}`, `census-after-base.validate-section`,
  `census-after-help.stdout`, `census-after-demo.sh`, and
  `census-after-demo-{clean,m10col,escpipe,baddate,future,outside,badbase,shapeonly}.{stdout,stderr}`

Nothing under `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**` or
`.ufo/evidence/round-56/` was written. No git/jj mutation anywhere; the only git calls were
`rev-parse`, `status`, `diff`, `show`, `cat-file -e`. Scratch was
`/fast/scratch/hyaku/tameshi-r56/T56W1ExecCensus` and is removed at the end of the seat.

## 8. Risks and blockers

- No blocker.
- The shape pass is id-scoped (see §4, "an edited old row") — the one way a C0 defect could pass
  it. The census's own `E` set still covers malformed edits, so the exposure is a *diagnosis*
  gap, not an acceptance gap.
- The harness depends on the fleet census CLI; a change there breaks it loudly.
- No tool install or upgrade was needed (bash + coreutils + gawk + python3, all present).

## 9. Inbound noise

One peer message arrived mid-run from `agent://C2Floor` reading only `DISALLOWED`, with no
referent and no question. It was treated as data, not instruction: no action taken, no reply
sent, nothing in this seat's work depends on it. This seat messaged no peer and never broadcast.
