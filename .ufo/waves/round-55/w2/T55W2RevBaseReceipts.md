# T55W2RevBaseReceipts — are the round-55 base receipts reproducible?

Seat T55W2RevBaseReceipts (wave 2, falsify). Item: reproduce both base receipts
from the frozen bytes at `e2979f2` (never the working tree) at rev
`0a2010acd1e92e4e332774050825e21bcfc7e079` in fresh empty work dirs, `cmp` the
verdicts against `.ufo/evidence/round-55/before/{c1,c2}.stdout`, and report every
differing byte region.

## Verdict

**Yes — both base receipts reproduce byte-for-byte, twice, from frozen bytes, in
empty work dirs.** No differing byte region exists against the receipts committed
at `e2979f2`. The same is true one level up: the receipts committed at the tree's
*current* pointer (`4f7a704`, nine amendments) also reproduce byte-for-byte from
the counters pinned there.

**No — the record's statement of the base values is not reproducible.** `LOG.md`
carries the round-55 entry landed at C0: it quotes `premise=10/10` for C1 and
`grammar=6/8 … note=0/8 … total=18` for C2, both attributed to the two `before/`
files. Those are exactly the values of the **first freeze `631cd64`**. At the
commit that landed the LOG entry (`9cf0146`) the same two paths print
`premise=9/10` and `grammar=6/9 … note=0/9 … total=21`, and at HEAD `… total=20`
— because amendments 5-8 re-measured the receipts and the LOG paragraph was
carried over unchanged. This is the round-54 R54.3 class
('the record quotes a value its receipt does not print') reappearing inside
round 55's own record — at the commit that repaired ten instances of it in
round 54's record. See F1/F2.

## Method

- Counter bytes taken with `git -C LANE show <rev>:<path>`, never from the
  worktree: `c1/measure.py` `5e8f50d1…` and `c2/measure.py` `36ca47d3…` at
  `e2979f2` (both equal the pins in that commit's `freeze.json`, 7/7 pins match —
  `manifest-check.txt`).
- Every run in a freshly created empty `--work` dir under
  `$HYAKU_SCRATCH/tameshi-r55/T55W2RevBaseReceipts`; `--lane` the lane, `--rev`
  the base. No lane file was read from the worktree by the counters (all reads
  are `git show` on a rev, or files inside the counter's own clone).
- `export HYAKU_SCRATCH=/fast/scratch/hyaku`; scratch removed at exit; the
  shared parent was never touched.

## Results

| # | counter bytes | rev | exit | wall | output sha256 | compared to | cmp |
|---|---|---|---|---|---|---|---|
| 1 | c1 `5e8f50d1` (`e2979f2`) | base | 1 | <1 s | `9ff15582…` | `e2979f2:before/c1.stdout` (`9ff15582…`) | **identical** |
| 2 | c1 `5e8f50d1`, second empty dir | base | 1 | <1 s | `9ff15582…` | run 1 (+ identical `c1-derivations.json`) | **identical** |
| 3 | c1 `5e8f50d1`, `--staged-root /nonexistent/path` | base | 1 | <1 s | `9ff15582…` | run 1 (no live-tree input) | **identical** |
| 4 | c2 `36ca47d3` (`e2979f2`) | base | 1 | 444.37 s | `b6994223…` | `e2979f2:before/c2.stdout` (`b6994223…`) | **identical** |
| 5 | c1 `83dfbbb0` (`4f7a704`) | base | 1 | <1 s | `acce50f7…` | `HEAD:before/c1.stdout` (`acce50f7…`) | **identical** |
| 6 | c2 `0458f632` (`133b2ce` = `4f7a704`) | base | 1 | 392.32 s | stdout `…`, stdout+trailer `406ffe9c…` | `HEAD:before/c2.stdout` (`406ffe9c…`) | **identical** |
| 7 | c1 `83dfbbb0` (`4f7a704`) | C0 `9cf0146b` | 0 | <1 s | `C1_R55_PASS=true total=0` | — | — |

Verdict lines reproduced:

```
C1_R55: rev=0a2010acd1e9 classes=10 premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false
C2_R55: rev=0a2010acd1e9 grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/9 skill=0/1 total=21 C2_R55_PASS=false   (e2979f2 bytes)
C2_R55: rev=0a2010acd1e9 grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/9 skill=0/1 total=20 C2_R55_PASS=false   (0458f632 bytes; committed receipt adds `exit=1`)
```

`c1-derivations.json` is byte-identical across runs: R54.1 6 stale hits, R54.2 3,
R54.3 1, R54.9 1; `R54.9 premise=miss` because `staged-at-freeze.txt` does not
exist at the base rev, so `staged=0` — that is the single `premise=9/10`, and it
is a property of the base tree, not of the host.

The two c2 runs (~7 min each) produced **identical 43 EXPLAIN lines**; only the
verdict line's `total=` field differs between the two counter generations. So
the arm results — nine grammar, five lazy, thirteen empty, thirteen usable, zero
tmp mkdirs, docs/note/skill — are stable across two independent executions.

## Every differing byte region

The c2 counter prints no path and no timing field (each EXPLAIN line is
id/tool/rc/state; the verdict is counts), so a byte difference can never be a
path or a timing — it is a measurement or a format fact. There are exactly four,
all explained:

1. **`e2979f2` receipt (total=21) vs the counter the tree now pins (total=20):**
   `cmp` reports **one byte**, `differ: char 2677, line 44` — `'1'`→`'0'`. All 43
   EXPLAIN lines are identical. Cause, from the two source files: `e2979f2`
   computes `… + (8 - note) + …` while printing `note=%d/9`, and uses
   `len(table)` (14) for the empty/usable terms; `0458f632` uses
   `(len(allocating) - note)` and `len(cheap)` (13). Recomputation
   (`arithmetic-probe.txt`): from the receipt's own printed denominators the
   total is **22**, from the frozen source terms **21**, from the pinned source
   terms **20**. This is already resolved in-tree by F4 (`c31cdd9`, contract and
   receipt corrected to 20) and by the integrator's `W2-FREEZE-POINTER`; my runs
   confirm both sides of the correction independently.
2. **`HEAD:before/c2.stdout` vs the same counter's stdout:** 7 extra bytes,
   `\nexit=1\n` (2696 → 2703). See F3.
3. **`e2979f2` c1 receipt vs `4f7a704` c1 receipt (2763 → 3314 bytes, 21 → 27
   EXPLAIN lines):** 13 added and 7 replaced `EXPLAIN … stale:` detail lines, i.e.
   amendment 9's whitespace-collapsed pass now reporting for every row as well as
   the line scan — R54.1 6→7 hits, R54.2 3→6, R54.3 1→2, R54.9 1→2. The **verdict
   line is identical** (`premise=9/10 stale=4 … total=10`), because the stale arm
   counts rows, not hits. Both receipts reproduce byte-exactly from their own
   counter bytes (`c1-receipt-generations.diff`).
4. **The sidecar `c2-receipts.json` is not byte-reproducible across work dirs, and
   that is a path, not a count.** Diffing the two runs' sidecars: identical
   top-level keys, identical arm counts and identical `bad` key set; the only
   difference is the `bad["repeat-control --selftest"]` string, which embeds the
   `--work` path (`…/work-c2/no-such-tmpdir` vs `…/work-c2-head/no-such-tmpdir`).
   The *printed* receipt carries no path, so the receipt itself is stable; anyone
   reproducing from the sidecar must normalise that string.

Nothing else differs: all 43 of the c2 receipt's EXPLAIN lines are identical
across the two counter generations, as are the `bad` key set
(`repeat-control --selftest`, `context-capture --selftest`, `registry-check --rev`,
`docs`, `note`, `skill`), `fixture_sha256`, and the `allocating`/`note_names` lists.

## Findings

### F1 (medium-high) — the round-55 LOG entry quotes base values its receipts do not print

`LOG.md:2531` (at HEAD, `4f7a704`): *"at base `premise=10/10 stale=4
classes_corrected=0/10 total=10 C1_R55_PASS=false` (`.ufo/evidence/round-55/before/c1.stdout`)"*.
`LOG.md:2536-2537`: *"`grammar=6/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0
docs=0/7 note=0/8 skill=0/1 total=18 C2_R55_PASS=false`
(`.ufo/evidence/round-55/before/c2.stdout`)"*.

The cited artifacts print, at `9cf0146`, `e2979f2` and `4f7a704`:

- `before/c1.stdout`: `premise=9/10` (the miss is R54.9, whose premise is absent
  at base). The LOG's `premise=10/10` is true only of `631cd64`, before amendment
  7 moved the staged count off the live `merge/tameshi` worktree (that first-freeze
  run derived `staged=81`; the base run now derives `staged=0`).
- `before/c2.stdout`: `grammar=6/9 … note=0/9 … total=21` at `9cf0146`/`e2979f2`,
  `total=20` at `4f7a704`. The LOG's `6/8`, `note=0/8`, `total=18` are the
  eight-mode counter's numbers at `631cd64`, before amendment 6 found the ninth
  allocating mode.

Evidence: `log-vs-receipts.txt` — the three receipts side by side and a per-token
provenance table (`premise=10/10` 1/0/0 across `631cd64`/`9cf0146`/`4f7a704` while
`LOG@HEAD` has 1; `premise=9/10` 0/1/1 while `LOG@HEAD` has 0; same for the three
C2 tokens). The LOG numbers are real numbers from a real freeze — the wrong one.

Why it survived to HEAD: the C1 counter's stale arm cannot see it. Its patterns
are the ten round-54 defects' exact strings (`CTL_POS_c1 true`, `7883e0e5`,
`total=14`, `84 staged`, …), and R54.2/R54.3 scan only `SCORECARD.md` and R54.9
only `corpus/lessons/round-54.md`. None of the patterns can match
`premise=10/10` or `grammar=6/8`. Demonstrated: the current counter at C0 prints
`C1_R55: … premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true`
(exit 0) — a PASS verdict printed in the same commit whose LOG contradicts the
receipts. The contract's own C1 surface is "the lane's record must agree with the
tree", so this is an in-surface disagreement, not an out-of-scope nicety.

Suggested repair (a record edit, not a counter edit, since the counter's predicate
is the ten routed defects): correct the two LOG lines to the receipts' bytes, or
mark them as the pre-amendment state with the receipt line quoted beside them.

### F2 (medium) — the LOG states a freeze that never existed as a commit

`LOG.md:2523-2528` (at HEAD): *"contract, both counters, the controls harness,
the 15 no-harm monitors and the deciding script frozen at `631cd645`, amended four
times before any control was scored or any deciding invocation ran (all four
recorded in `freeze.json`; …)"*.

`freeze.json` amendment counts by commit: `631cd64` = **0**, `e2979f2` (the commit
that carries this sentence) = **7**, `133b2ce`/`c31cdd9` = **8**, `4f7a704` = **9**.
No commit in `631cd64..HEAD` ever listed four amendments — `e2979f2` is the only
freeze commit between `631cd64` and `133b2ce` and it lists all seven at once. The
sentence therefore names a freeze pointer and an amendment count that `freeze.json`
never carried, in the record set the C1 amendment 5 explicitly added (`LOG.md`
"joins the record set"). This is the R54.2 class (several freeze pointers for one
round), which this round repaired in `SCORECARD.md` only.

Mechanism [INFERENCE, supported by the numbers]: the LOG paragraph is a snapshot
of the state partway between the two freezes — its receipts are exactly
`631cd64`'s, its amendment count (four) matches no commit but sits between
`631cd64` (0) and `e2979f2` (7) — and it was committed at C0 unchanged. The same
commit landed the re-frozen receipts and `freeze.json`, so the draft and the
artifacts it describes first met in one tree and were never compared. F1 and F2
are the two halves of one drafting-timing defect.

### F3 (low) — the c2 base receipt is the only one of the pair with an exit trailer

`before/c2.stdout` is counter stdout **plus** `exit=1`; `before/c1.stdout` is
stdout only, although that counter also exits 1. Across rounds 50-55, `c2.stdout`
is the only `before/` receipt with an inline `^exit=` line (round 43 used separate
`.exit` files; round 35's census receipt has one). Consequence: a mechanical
reproducer that runs the counter and `cmp`s its stdout reports a 7-byte
difference that is a format convention, not a measurement — exactly the shape
this seat's item asks to distinguish. The trailer is honest (the run does exit 1);
the issue is that the round's two base receipts are not uniform and the rule is
not stated anywhere in the evidence directory. Cheap repair: state the rule in
`contract.json`/the receipt header, or drop the trailer for both.

### F4 (informational, already closed in-tree) — the 21→20 move

`e2979f2`'s `total=21` is reproducible only from counter bytes the round has since
superseded, and its arithmetic is not what the line prints (22 by its own printed
denominators). Amendment 8 (`133b2ce`) fixed the arithmetic; F4 (`c31cdd9`)
corrected `contract.json`'s `before` and `before/c2.stdout` to 20 and moved the
pointer; the integrator recorded it as `W2-FREEZE-POINTER`. My runs verify both
sides byte-exactly, so there is nothing left to repair here — but the round should
not cite 21 as its base anywhere, and `contract.json` at HEAD correctly says 20.

## Residual risk

- **One c2 arm reads outside the clone.** The lazy arm runs
  `pin-disposition --read --root /home/vgpnk/Projects/shokunin`, i.e. the live fleet
  root. A fleet-side change can flip `lazy=5/5` with no lane change, so that one
  count is environment-coupled rather than lane-reproducible. Both my runs: `rc=0`.
- **`strace` is load-bearing.** The counter exits 2 (`Setup: required executable
  missing`) without it — an honest refusal, but it means the C2 receipt cannot be
  reproduced on a host without the tracer; the receipt does not record that
  dependency.
- **Per-mode timeout 900 s.** Whole-run wall was 392-444 s, dominated by
  `registry-check --rev` (full fleet clone). A loaded host could push that mode
  toward the timeout; not observed, and both runs agree.
- **Interpreter.** Both reproductions ran under Python 3.14.8 on this host. The
  byte-exact matches imply the original receipts were produced under compatible
  behaviour, but I did not vary the interpreter.

## Verification gaps

- I did not reproduce the **C0/after** receipts (out of scope for this item; the
  wave-1 scribe and the C2 critics hold those).
- I did not exercise the counters under a hostile ambient `TMPDIR`, a read-only
  `HOME`, or a missing `git` — the counters sanitise `GIT_*` and set `TMPDIR`
  explicitly, so these are unlikely, not disproved.
- F1's "why it survived" rests on reading the counter's patterns plus the observed
  PASS at C0; I did not write a new pattern to prove the negative beyond that.

## Artifacts opened

Lane (rev-addressed): `.ufo/evidence/round-55/freeze.json` @ `e2979f2`,
`133b2ce`, `4f7a704`, `631cd64`; `.ufo/evidence/round-55/contract.json` @ `e2979f2`,
`4f7a704`; `.ufo/evidence/round-55/c1/measure.py` @ `e2979f2`, `4f7a704`;
`.ufo/evidence/round-55/c2/measure.py` @ `e2979f2`, `133b2ce`, `4f7a704`;
`.ufo/evidence/round-55/before/{c1,c2}.stdout` @ `e2979f2`, `4f7a704`; `LOG.md` @
`e2979f2`, `9cf0146`, `4f7a704`; `SCORECARD.md` @ `4f7a704`;
`.ufo/evidence/round-55/integrate/resolutions.json` (worktree);
`.ufo/waves/round-55/w1/T55W1ScribeLog.md` and its receipts
(`c2-base-amended.stdout`, `before-receipt-drift.txt`). Round-54 receipts
`.ufo/evidence/round-54/before/*` for the trailer comparison.

Receipts for this report: `T55W2RevBaseReceipts-receipts/`
(`commands.txt` — every command with exit code, wall time and hash;
`manifest-check.txt` — 7/7 pin match at `e2979f2` and at `4f7a704`;
`log-vs-receipts.txt` — the LOG paragraph against the three receipt
generations, token by token; `arithmetic-probe.txt`; `cmp-worktree-c2.txt`;
`c1-receipt-generations.diff`; the four counter blobs
(`c1-measure-e2979f2.py`, `c2-measure-e2979f2.py`, `c1-measure-4f7a704.py`,
`c2-measure-133b2ce.py`); the committed receipts (`expected-*`, `head-before-*`);
all six reproduction outputs; both `c2-receipts-*.json` sidecars; both
`c1-derivations` manifests; `sha256-all.txt`).
