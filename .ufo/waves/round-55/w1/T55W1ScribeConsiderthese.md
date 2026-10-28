# T55W1ScribeConsiderthese — considerthese mining (round 55, wave 1)

Seat T55W1ScribeConsiderthese, leaf member (no dispatch). Lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base
`0a2010acd1e92e4e332774050825e21bcfc7e079`, frozen counter set
`631cd6455e58dce969310b4c0466c3383d9f5108`.

**Pick (one, as the item allows): `considerthese/2026-10-28.md` proposal 2,
"Counter-arm liveness check" (`:77-78`).** It is unimplemented, it is squarely
verification-fixture craft, and it has a live instance inside the round's own C2
counter: `C2_R55 tmp_mkdirs` reads `0` in every committed receipt the lane has
(6 observations across rounds 54-55), while a one-line mutant makes the same arm
print `132`.

**Files read, not edited:** `considerthese/2026-10-28.md` (mtime 10:43:53),
`considerthese/2026-10-26.md`, `considerthese/2026-10-25.md` — full text.
No lane production file was touched. No mutating git command was run on the
lane; the only commits are inside a scratch fixture whose
`git rev-parse --show-toplevel` printed the fixture path (receipts §7).

---

## 1. Disposition of every proposal in the three files (scope filter first)

Scope filter: the item asks for a proposal that touches **verification-fixture
craft** — counters, controls, fixtures, the checks that decide claims. Proposals
about planning, process, records or throughput are out of scope even when they
are equally unimplemented; the table says which and why.

| file | # | proposal | scope | status / the check that shows it |
|---|---|---|---|---|
| 2026-10-28 | 1 | receipt-existence linter (`:73-76`) | record verification, **not** fixture craft | Half-implemented and out of scope: path existence is QUALITY 97 (`corpus/QUALITY.md:1428-1434`) with `.ufo/evidence/round-48/quality/pointer-check.py`; the byte-for-byte counter-quote half has no checker. |
| **2026-10-28** | **2** | **counter-arm liveness check (`:77-78`)** | **fixture craft** | **UNIMPLEMENTED — picked (§2-§6).** |
| 2026-10-28 | 3 | cold-read cost forecast at planning time (`:79-81`) | planning | Out of scope. QUALITY 98 (`:1436-1444`) is a post-edit precheck, not a pre-edit forecast. |
| 2026-10-28 | 4 | assimilation backlog burn-down (`:82-84`) | process | Out of scope. |
| 2026-10-28 | 5 | stale closure-pointer sweep (`:85-87`) | record hygiene | Out of scope; `pointer-check.py` strips `:N`/`:N-M` suffixes, so line/page pointers are not re-resolved there either. |
| 2026-10-26 | 1 | crash-resume integrity check | fixture craft | Already mined: `.ufo/evidence/round-53/verify-freeze.sh` exists and is cited by `corpus/lessons/round-53.md:72`. |
| 2026-10-26 | 2 | nondeterminism fix list | row hygiene | Out of scope. |
| 2026-10-26 | 3 | recurring-defect tracker | closure process | Out of scope; `corpus/routed-defects.json` is the ledger it would extend. |
| 2026-10-26 | 4 | host and scratch budget readout | capacity | Out of scope. |
| 2026-10-26 | 5 | carrier fallback register | sourcing | Out of scope. |
| 2026-10-25 | 1 | measured-to-landing drift check | record/fixture | Mined: QUALITY 86; closures run the receipts-only tail check (per `considerthese/2026-10-26.md:66-68`). |
| 2026-10-25 | 2 | cumulative mismatch-class regression run | fixture | Mined: round-46 C1 cumulative restatement (`considerthese/2026-10-26.md:66-67`). |
| 2026-10-25 | 3 | dead-code debt list | fixture | Mined: round-47 dead-code scan (`considerthese/2026-10-26.md:66-67`). |
| 2026-10-25 | 4 | round tempo and capacity readout | capacity | Out of scope. |
| 2026-10-25 | 5 | proposal uptake ledger | records | Mined in round 48's unlanded drafts (`considerthese/2026-10-26.md:66-68`). |

Two independent statements that proposal 2 is still open: the round-54 lesson
records "proposals 2–5 remain unmined (at most one per round)"
(`corpus/lessons/round-54.md:57-60`), and round 55's own integration list (six
items: two tools, `registry.json`, the note, one `SKILL.md` sentence,
`SCORECARD.md`, the lesson) contains no arm-liveness item.

## 2. Grounding: what proposal 2 points at, opened

The proposal's own text (`considerthese/2026-10-28.md:77-78`):

> **Counter-arm liveness check.** For each frozen counter, list its arms and
> require one committed input per arm that moves that arm's tally away from
> zero. A passing control set did not reveal that round 53's re-key arm could
> never fire.

The case it cites, opened:

- **QUALITY 105** (`corpus/QUALITY.md:1584-1586`): "A counter arm that reads a
  directory, a revision or a manifest is proven by a positive control in which
  that arm must fire: the receipt records the arm's own non-zero count **at a
  tree where the round's work is present**."
- The round-54 `## Mistakes` row for the dead arm (`corpus/lessons/round-54.md:64-78`)
  and the dead arm's receipt
  `.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout`
  (`rekeyed=0/30` at the round-53 final content revision).
- QUALITY 105's falsifier (`corpus/QUALITY.md:1590`) is the pair
  `rekeyed=0/30` vs `rekeyed=7/7` at the round-54 deciding revision — i.e. 105
  is scoped to a **count arm whose passing value is non-zero**, proven by the
  round's positive control.

**The gap 105 leaves.** A guard arm whose *passing* value is zero can never be
proven by a tree "where the round's work is present": the work being present is
exactly the state in which such an arm reads zero. The frozen round-55 C2
counter has such an arm and names it (`…/round-55/c2/measure.py:7-35`):

> `usable` 13 modes with a fresh TMPDIR exit their expected code, and the eight
> allocating modes issue no mkdir under /tmp (strace census);

its implementation is `…/round-55/c2/measure.py:138-146` (`tmp_mkdirs`, counts
strace lines that both say `mkdir` and carry `"/tmp`) and it is scored at
`:208-221`. `tmp_mkdirs` is therefore outside 105's literal scope (it reads a
strace log, not "a directory, a revision or a manifest") and hostile to 105's
mechanism (non-zero is the *failure* state).

**No control in either round can move it.** Round 55's frozen controls are
`CTL_0_c1/c2`, `CTL_SKIP_c1/c2`, `CTL_FAB_c1`, `CTL_POS_c1/c2`,
`CTL_BREAK_c2` (`…/round-55/controls.sh:51,53,71,87,112,123,125,140`); round
54's are `CTL_0_c1/c2`, `CTL_R53`, `CTL_FAB`, `CTL_LOGINPUT`, `CTL_POS_c1/c2`,
`CTL_EXIT0`. `grep -c tmp_mkdirs` over both control scripts prints `0` and `0`
(`tmp-arm-control-coverage.txt`): no control introduces a `/tmp` fallback, so no
control can move that arm.

## 3. The census (command, output, and what it finds)

Draft tool (also the receipt): `.ufo/waves/round-55/w1/T55W1ScribeConsiderthese-receipts/arm-census.py`.
It reads **committed blobs** (`git show REV:path`), takes every counter verdict
line `C[12]_R\d+: …`, whether bare or prefixed by a control tag, and tallies
each `key=value` arm.

```
$ python3 arm-census.py --lane <lane> --rev 0a2010acd1e92e4e332774050825e21bcfc7e079
REV 0a2010acd1e9 -- receipts scanned: 1127, arms: 414, arms with no non-zero observation: 63
  C1_R53   rekeyed              obs=1   max=0 receipts=.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout
  C2_R54   tmp_mkdirs           obs=5   max=0 receipts=.ufo/evidence/round-54/{after/c2.stdout,before/c2.stdout,control/controls-a.stdout,control/controls-b.stdout}
$ python3 arm-census.py --lane <lane> --rev 631cd6455e58dce969310b4c0466c3383d9f5108
REV 631cd6455e58 -- receipts scanned: 1129, arms: 428, arms with no non-zero observation: 68
  C1_R53   rekeyed              obs=1   max=0 receipts=.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout
  C1_R55   classes_corrected    obs=1   max=0 receipts=.ufo/evidence/round-55/before/c1.stdout
  C2_R54   tmp_mkdirs           obs=5   max=0 receipts=(the four round-54 receipts above)
  C2_R55   tmp_mkdirs           obs=1   max=0 receipts=.ufo/evidence/round-55/before/c2.stdout
```

Full lists: `arm-liveness-census.txt`, `arm-census-<rev>.json` (63 and 68 rows).
The four rows above are the ones this seat's item is about. The other rows
include arms whose zero is a `0/N` tally that a later committed receipt moves
(measured example: `C1_R30 equiv_pass` reads `0/4`, `2/4`, `4/4` across 37
observations) and refusal counters such as `C1_R47 unobservable=0`; the census
reports the fact, and §6 says why that fact is not automatically a defect.

Round-55 receipts at the freeze commit (`git show`, worktree copy is in flux —
see §8):

- `.ufo/evidence/round-55/before/c2.stdout:43` (blob at `631cd64`):
  `C2_R55: rev=0a2010acd1e9 grammar=6/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=18 C2_R55_PASS=false`
- `.ufo/evidence/round-55/before/c1.stdout:3`:
  `C1_R55: rev=0a2010acd1e9 classes=10 premise=10/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false`

## 4. Demonstration: the arm is live; the tree never supplies the input

Fixture: `git clone --shared` of the lane at base, `--detach 0a2010ac`; toplevel
asserted equal to the fixture path before committing. Mutant (receipt
`arm-fire-mutant.patch`): one line in `tools/env-diff.py` `strict_scratch_root()`:

```diff
-        return t
+        return "/tmp"  # ARM-LIVENESS DEMO: ignores the usable scratch root
```

Then the counter's own predicate (`mkdir` **and** `"/tmp` in a
`strace -f -e trace=mkdir,mkdirat` log), run under a *fresh usable* `TMPDIR`:

```
$ env TMPDIR=<usable> strace -f -e trace=mkdir,mkdirat -o base.strace python3 <base>/tools/env-diff.py --selftest
base  exit=0 total_mkdir_lines=625 tmp_mkdirs_arm=0    ENVDIFF_SELFTEST: 9/9 pass
$ … same on the mutant fixture …
mut   exit=0 total_mkdir_lines=625 tmp_mkdirs_arm=132  ENVDIFF_SELFTEST: 9/9 pass
```

Receipts: `base.env-diff-selftest.strace`, `mut-env-diff-ignores-scratch-root.strace`,
`base.env-diff-selftest.stdout`, `mut.env-diff-selftest.stdout`.

Two facts worth keeping: (a) the arm discriminates cleanly — `0` vs `132` with
the same 625 total mkdir lines, so it is the `/tmp` prefix that decides; and
(b) the tool's **own** self-test stays `9/9 pass` on the mutant, which is the
proposal's point in miniature: a passing fixture set does not reveal an arm that
nothing moves.

## 5. Draft landing

### 5a. Primary: QUALITY criterion 106 (append after 105)

> ### Criterion 106 — an arm of a frozen counter has a committed input that moves it, not only a control that passes
>
> A counter declares its arms in its own verdict line. For each arm the lane
> commits at least one receipt in which that arm's value differs from its
> passing value; for a guard arm whose passing value is zero, that input is a
> mutant that reintroduces the defect the arm guards (a `/tmp` fallback for a
> "no mkdir under `/tmp`" census, a forged receipt for a "no forged receipt"
> arm). Criterion 105 proves one arm per round on a positive control where the
> round's work is present, and it cannot certify a zero-is-good arm: the work
> being present is exactly the state in which such an arm reads zero, so every
> receipt a correct tree can commit leaves its ability to fire unproven. The
> census is not a gate on the arm's design — an author may declare an arm
> intentionally unreachable — but a round may not claim an arm protects
> anything while no committed input moves it.
>
> Lesson: `considerthese/2026-10-28.md` proposal 2 (counter-arm liveness
> check), mined at round 55: `C2_R54 tmp_mkdirs` and `C2_R55 tmp_mkdirs` read
> `0` in six committed observations across two rounds
> (`…/round-54/{before,after}/c2.stdout`, `…/round-54/control/controls-{a,b}.stdout`,
> `…/round-55/before/c2.stdout`), while a one-line mutant that makes
> `env-diff` ignore the usable scratch root prints `tmp_mkdirs=132`
> (`.ufo/waves/round-55/w1/T55W1ScribeConsiderthese-receipts/arm-fire-mutant.patch`).
>
> Falsifier that must fail: `arm-census.py --lane LANE --rev 631cd64` prints
> the `C2_R55 tmp_mkdirs` row with `nonzero=0` at the freeze commit
> (`arm-liveness-census.txt`), and the same command over a tree that commits
> the mutant control prints `nonzero>=1`; a census that reports the arm
> non-zero at a tree with no such input is the second failure the criterion
> names (a counter that prints a value it did not measure).

Landing mechanics for round 56: the census script as
`.ufo/evidence/round-56/quality/arm-census.py` (interface:
`--lane --rev [--json OUT] [--quiet]`, exit 0 as a census), its receipt at the
round-56 base and at the deciding revision, and one committed mutant control per
zero-is-good arm that the round claims. Note the ordering constraint this
criterion forces: the mutant control is *committed*, so it lives under the
round's evidence dir, and the arm census runs over the round's own evidence as
well as the two rounds before it.

### 5b. Secondary: the lesson row this would need (round-55 `## Mistakes`)

Land this row only if the L1 wants the criterion traced from a mistake; it is a
row about a class, not about a failed claim:

> - **class: an arm with no committed input that moves it (a zero-is-good guard
>   arm).** evidence: `C2_R54 tmp_mkdirs` (5 observations) and `C2_R55
>   tmp_mkdirs` (1) read `0` at every committed revision, and the round's own
>   control set (`CTL_0/SKIP/FAB/POS/BREAK`) contains no `/tmp`-fallback input;
>   the arm is live — a one-line mutant prints `132`
>   (`arm-fire-mutant.patch`, `mut-env-diff-ignores-scratch-root.strace`).
>   captured-by: nothing — QUALITY 105 is scoped to a non-zero passing value and
>   to arms that read "a directory, a revision or a manifest", and the C2 counter
>   documents the arm without requiring an input that moves it. fix: criterion
>   106 plus the round's committed mutant control.

### 5c. SOURCES row: **not owed** (and why, with the date)

A SOURCES row is an external carrier with a located quote in a
census-validated register (`scripts/sources-census.sh validate`, 139 rows
S001-S279). Proposal 2's claim is internal to this lane — it is a statement
about the lane's own counters and its own receipts — so a row would have to
invent an external authority for it. The upstream input is operator-authored and
dated **2026-10-28** (`considerthese/2026-10-28.md:77-78`, commit `9b9cd57`,
09:46 -0300); it is cited by path in the criterion and the lesson row, as the
lane cites these files elsewhere (`corpus/lessons/round-54.md:57`). If the
round-56 L1 wants a source for the *principle* (a test that cannot fail proves
nothing) that is a separate, sourced admission and must not be back-filled.

## 6. Limits of this finding

- The census is **textual**: it reads counter verdict lines from committed
  receipts. An arm printed under a different key, a counter that prints a
  non-`key=value` summary, or an arm whose value is non-numeric is invisible or
  unjudged (`arm-census-*.json` marks `numeric: false`).
- `nonzero=0` is **not** by itself a defect. Many arms are refusal counters
  (`unobservable=0`, `duplicate=0`) whose zero is the correct reading at the base
  revision, and several become non-zero on a later committed receipt. The
  criterion's requirement is the weaker, checkable one: *some* committed input
  moves the arm, or the round does not claim it protects anything.
- I did not judge any arm's design (whether it should exist, or what it should
  count) — that is each counter author's call; only the input's existence.
- `C1_R55 classes_corrected` is listed at the freeze commit because the round-55
  deciding receipts do not exist yet (`.ufo/evidence/round-55/after/` absent at
  the time of this seat). Its positive control (`CTL_POS_c1`) is designed to
  move it to `10/10`; whether that receipt lands is the L1's deciding run, not
  this seat's claim.

## 7. Receipts

All under `.ufo/waves/round-55/w1/T55W1ScribeConsiderthese-receipts/`.

| receipt | what it is |
|---|---|
| `arm-census.py` | the census tool (draft for `.ufo/evidence/round-56/quality/arm-census.py`), reads committed blobs |
| `arm-liveness-census.txt` | its output at base `0a2010ac` (63/414 arms) and freeze `631cd64` (68/428 arms), with the invocations |
| `arm-census-0a2010ac….json`, `arm-census-631cd64….json` | machine-readable per-arm census (observations, max, nonzero, receipts) |
| `tmp-arm-control-coverage.txt` | every committed `tmp_mkdirs=` line (5 round-54 + 1 round-55) and `grep -c tmp_mkdirs` over both control scripts (`0`,`0`) |
| `arm-fire-mutant.patch` | the one-line mutant, in its fixture clone |
| `base.env-diff-selftest.strace`, `mut-env-diff-ignores-scratch-root.strace` | strace logs: `0` vs `132` `/tmp` mkdirs, 625 mkdir lines each |
| `base.env-diff-selftest.stdout`, `mut.env-diff-selftest.stdout` | both print `ENVDIFF_SELFTEST: 9/9 pass` |
| `arm-fire-demo.stdout` | the abandoned full-counter run (§8) — traceback, kept, not used as evidence |
| `scratch-path.txt` | the scratch root used for the fixture clones |

Passages opened and cited in the text: `corpus/QUALITY.md:1584-1590` (105),
`:1428-1434` (97), `:1436-1444` (98); `corpus/lessons/round-54.md:57-60,64-83`;
`.ufo/evidence/round-55/c2/measure.py:7-35,138-146,208-221`;
`.ufo/evidence/round-55/controls.sh:51,53,71,87,112,123,125,140`;
`.ufo/evidence/round-54/control/controls.sh` (control set);
`.ufo/evidence/round-48/quality/pointer-check.py:1-20`;
`considerthese/2026-10-28.md:71-87`; `considerthese/2026-10-26.md:66-69`.

## 8. Observations reported, not fixed

1. **The round-54 record mis-attributes 2026-10-28 proposal 1.**
   `corpus/lessons/round-54.md:57-60` calls it "the contract-debt table: which
   SCORECARD contract sections are placeholders and for how long". No such text
   exists: `git grep -n "contract-debt\|contract debt" 0a2010ac -- considerthese/`
   prints nothing, and the file has exactly one commit (`9b9cd57`, 2026-10-28
   09:46 -0300, ancestor of base) whose bytes equal the worktree
   (`git diff 0a2010ac -- considerthese/` empty). The file's mtime is 10:43:53,
   after the commit; that admits a rewrite with identical bytes and nothing more.
   Consequence for this seat: the round-54 claim that proposal 1 was mined rests
   on a description the tree does not contain, so proposal 2 was not the only
   still-open item — it is the only one *in scope* (§1).
2. **`.ufo/evidence/round-55/before/c2.stdout` changed under me.** The committed
   blob at `631cd64` is 2634 bytes — 43 lines, `EXPLAIN …` per mode plus
   `usable=13/13 … tmp_mkdirs=0 … total=18` on line 43
   (`git show 631cd64:.ufo/evidence/round-55/before/c2.stdout`). The worktree
   copy was 0 bytes at 13:53 and 139 bytes at 13:59 (one `C2_R55:` line, no
   `EXPLAIN` lines); an earlier worktree read showed yet another run
   (`usable=12/13 … total=19`). This seat does not own that file and did not
   touch it; every number in §3 is taken from the committed blob. Whoever owns
   the C2 before-receipt should confirm which run the round cites.
3. **A scratch wipe killed the full-counter demo.** I attempted the strongest
   form of §4 — run the frozen `c2/measure.py` on the mutant clone — and it died
   after 4m42s with `FileNotFoundError: … /w-arm/clone` (`arm-fire-demo.stdout`),
   because the scratch tree `$HYAKU_SCRATCH/tameshi-r55/T55W1ScribeConsiderthese`
   was emptied while the run was in flight (only `w-arm` and a later `t-demo`
   remained; the sibling directories under `tameshi-r55/` were all fresh at
   13:54-13:55). Cause not established and **not** attributed to the counter; I
   did not rerun it. The targeted strace comparison carries the claim instead,
   and it is the same predicate the counter uses (`measure.py:138-146`).

4. **The frozen set named by this item (`631cd64`) does not carry the amended
   counter, and the amended set is uncommitted.** `git diff --stat` against
   `631cd64` shows `.ufo/evidence/round-55/{contract.json,freeze.json,c2/measure.py}`
   modified in the worktree; the committed contract has `"amendments": []`, the
   worktree contract has four, and the committed `c2/measure.py` has no
   `r55-rev` branch checkout while the worktree one does. The amendments
   themselves say they were found "before any control was scored and before any
   deciding invocation", so the record of them is in order — but a reader who
   runs the counter from `631cd64` today runs the **pre-amendment** bytes. The
   L1 must commit the amended set (and make the round's report name the commit
   the deciding receipts bind) before the deciding run; this seat's census is
   unaffected because it reads only committed receipts, and does not run the
   counter.

## 9. Tooling

No install or upgrade was needed; `python3` 3.14, `git`, and `/usr/bin/strace`
were already present. No `pacman` transaction was attempted.

## 10. Item-vs-harness filename

The item text says "Write `T55W1Er10.md`"; the harness `Report:` path for this
seat is `.ufo/waves/round-55/w1/T55W1ScribeConsiderthese.md` and a peer agent
(`T55W1Er10`) is live on a different subject ("Finding 58/64 in round-54
lesson"). This seat wrote the harness path only, plus
`T55W1ScribeConsiderthese.json` and the receipts dir, to avoid colliding with
that peer's report.
