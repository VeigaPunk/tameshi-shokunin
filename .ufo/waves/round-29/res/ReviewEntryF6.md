# ReviewEntryF6 — `corpus/knowledge/survivor-fixture-minimization.md` at E (7a45f7b)

Scope: line-by-line check of the entry against the S024 snapshot, `BuildF6B.md`,
`CriticC2v2.md`, the pinned kagi census/gate at `fecee874`, the kaika probe census,
and the frozen counter. Work done in clone `/fast/scratch/hyaku/tameshi-r29-ReviewEntryF6`
at `7a45f7b` (= lane master at review time; no newer commits). No lane writes except
this file; no installs (none needed). All commands `timeout 900`-wrapped where applicable.

## Verdict

**The entry is materially accurate; "B5 is masked under the pinned declaration" is a fair
classification.** Two statements are wrong/overstated (the "only mode `-`" claim and the
"byte copy" claim), one is imprecise (the S024 assertion), and the reported head counter
line omits a second failing conjunct that existed at E. None of the defects changes the
headline MISS or the masking mechanism.

## Verdict first: is the "masked" classification fair?

**Yes.** Verified three independent ways on the committed bytes:

1. Code reading of the pinned gate (kagi `surface-census.sh` @ `fecee874`, sha256
   `275d8294…53009f`, matching `PIN_BASH` in `tools/mutate-and-run.sh:605`): exec-bit arm
   at `:214-217` emits `(declared exec, no execute bit)` then `continue`s; the exact-mode
   check at `:219-223` runs afterwards. All three pinned exec rows
   (`surface-census.tsv:22,30-31`) declare `755`. Any exec-kind file failing `-x` has a
   live mode != 755, so with the exec arm deleted (the `@defect B5` spec,
   `tools/mutate-and-run.sh:717-719`) the mode check still produces a divergence —
   mutant exit 1, never 0. The removed arm detects a strict subset of what the mode
   check catches on every 755-declared row: masked in survivorship terms.
2. Empirical: I re-ran the frozen counter's own `ddmin`/`Oracle` on the committed
   `f6/original/` — **171 oracle tests, 0 kept, output unit-equal to the committed
   `minimized/`** (matches BuildF6B's table and the entry :49-50). Every 105-unit
   subset fails `kills()`: subsets keeping the drifted exec row fail the mutant on
   `(mode <live>, declared 755)`; subsets dropping it can never emit the required
   pristine token.
3. Empirical boundary: the `noexec` bound (:70-72) is real — on a `tmpfs` mounted
   `noexec`, `test -x` fails a `chmod 755` file while `stat` still reads 755. So the
   bound is honest: masked only on an ordinary executable mount, which is what the
   counter uses (`tempfile.mkdtemp`).

Caveat on scope: "masked" is established **under the anchored fixture** (byte-identical
census + baseline/shapes subsets + manifest-expressible host). The entry correctly does
not claim unconditional survivorship — the cited `-`-mode probes kill B5 — but see F1:
its unanchored-kill characterization is too narrow.

## Findings (severity-ordered)

### F1 — medium: "B5 can **only** be killed by a fixture that declares an exec row with mode `-`" is overstated

Entry `corpus/knowledge/survivor-fixture-minimization.md:64-68`. The mechanism the entry
itself describes refutes the "only": the mutant exits 0 iff it sees zero divergences, and
the mode check passes whenever `lmode == declared` (or `mode == "-"`). A census row
`asset exec 644` with a live `644` file kills B5 identically — pristine emits the exec
token at gate `:214-217`, mutant's mode check compares `644 == 644` → `SURFACE OK` →
exit 0 — provided no `drift-baseline` row pins a disagreeing mode for that path (the
contract permits baseline subsets, so the row can simply be omitted; CROSSCHECK at
`:225-232` only fires when a baseline mode exists). Any non-executable declared mode
matching the live mode kills; `-` is only the simplest case. Directionally fine (the
`-`-mode claim itself is verified below), wrong as a biconditional.
Smallest safe correction: "B5 is killed exactly by exec rows whose declared mode the
mutant accepts — `-`, or a mode equal to the file's live non-executable mode (with no
baseline pin contradicting it)."

### F2 — medium-low: "The committed `minimized/` is a byte copy of `original/`" is false at byte level

Entry :49-50. `diff -r` on the committed trees: `minimized/census.tsv` carries one extra
trailing newline (4753 B vs original's 4752 B; sha256 `fc76f068…` vs `4af0dbcc…`). The
other three files are byte-identical, and the two are **unit**-identical (my ddmin
re-run's output tuples equal the committed minimized tuples exactly) — which is all the
contract requires — and BuildF6B itself discloses the newline at
`.ufo/waves/round-29/w1/BuildF6B.md:189-193`. The entry's "byte copy" flatly contradicts
its own source.
Smallest safe correction: "a unit-identical copy (the only byte difference is one
trailing newline in `census.tsv`)."

### F3 — low: "asserts that the starting input is itself failing" is imprecise

Entry :15-16 vs snapshot `S024-fuzzingbook-Reducer.html:12917`: the code asserts
`self.test(inp) != Runner.PASS`. Fuzzingbook's Runner has three outcomes
(FAIL/PASS/UNRESOLVED); the assertion admits UNRESOLVED too. Directionally right —
S024's trace (`:13208-13211`) fires `AssertionError` on a PASSing input and the claim
"before it removes anything" is exact — but "failing" overstates the predicate.
Smallest safe correction: "asserts the starting input does not pass."

### F4 — low: the head-run receipt omits a second failing conjunct

Entry :42-43 quotes `anchored=1 kill_original=0` and PASS false; the full head receipt
`.ufo/evidence/round-29/c2-at-E.stdout` (reproduced by my run:
`oracle tests run: 1 … entry_sourced=1 quote_located=0 … PREDICATE=false`) also shows
**`quote_located=0`** — `corpus/lessons/round-29.md` did not exist at E (it lands at
`9bb699a`). The masking finding stays the sole fixture-side blocker, but the entry's
"the counter at the round's head" line silently drops that a second conjunct also
failed at the reported rev.
Smallest safe correction: quote the full token line or note `quote_located=0 (no
round-29 lesson file at E)`.

### F5 — low: the "round-3 probes" half of :66 is supported only by quoted text

Entry :66-68. Kaika half fully receipted:
`.ufo/evidence/kaika-round-1/coldread/probe-fixtures/probe/census.tsv:1` is exactly
`$HOME/bin/tool asset exec -`, and `B-probe-B5-pristine.txt` / `-mutant.txt` show the
claimed `(declared exec, no execute bit)` vs `SURFACE OK (exec 644)` pair. The round-3
half rests on `corpus/knowledge/mutation-case-kagi-census.md:111-114`, which quotes the
same pair but cites `evidence/probe-B5-non-equivalence.txt` — **no `corpus/evidence/`
tree exists at E** (the receipt file is absent; only the note's quotation remains).
Statement is consistent with its source; flag that the primary receipt is missing.
Smallest safe correction: cite the note line numbers (`mutation-case-kagi-census.md:
111-114`) rather than implying a standing artifact.

## Statements checked and supported

- :3 snapshot path + `sha256 3abede35…e99` — `sha256sum` of the committed file matches
  the full digest `3abede35…65e99`. `re-opened 2026-10-23` matches the lesson's
  `fetched 2026-10-23T01:09Z` (UTC; lane entries use UTC for fetch stamps — see
  `oracle-anchored-survivors.md` "opened 2026-10-22").
- :5-8 F6 row + pre-registration — `corpus/README.md:83` (`## Frontier` at :68) and
  the Round-29 section :431-447 confirm.
- :13-15 quote — verbatim in the normalized snapshot text, located in the
  `Delta Debugging` section (headings list, snapshot :13023), 15 words.
- :24-34 — `anchored` byte-identity and subset rules match `c2-measure-v2.py:249-251`;
  `host.tsv` manifest semantics match `:30-33,114-147`; `kills()` conjuncts match
  `:172-176` and contract-amendment-1.json predicate (2); ddmin description matches
  `:183-202` and CriticC2v2's Q3 finding (integer `//` partition vs S024's float
  `start/subset_length`, counterexample at `CriticC2v2.md:45-56`).
- :38-47 — `f6/original/` is byte-identical to `f6/BuildF6B/original/` (`diff -r` clean);
  census sha `4af0dbcc…` equals `git show fecee874:corpus/surface-census.tsv`;
  baseline bytes identical to the pinned `drift-baseline.tsv`; pristine/mutant
  receipts match `BuildF6B.md:73-91` verbatim.
- :42-43 head counter line — reproduced by my run at E (one caveat: F4).
- :54-59 — all three exec rows `755` at `surface-census.tsv:22,30-31`; arm order
  `:214-217` before `:219-223`; "noexec mount a 755 file fails `-x`" verified on a
  tmpfs (`test -x` fails, stat reads 755); 512-mode/3-row sweep is BuildF6B's claim
  (report shows 6 sample rows, `WINNERS []`) — relayed, not reproduced here.
- :61-62 — CriticC2v2 reached the same conclusion at frozen B before any builder ran
  (`CriticC2v2.md:5,70-83`, Q5, ctl pre-data wave vs w1 builders).
- :70-72 — noexec caveat honest; no seat used it (BuildF6B.md:12-13).
- :76-79 — ScoutF6Next Table 2 ranks exactly 24 fixture-absent survivors, rank 1 = B5.
- Contract consistency: units are lines (`contract bound`), entry counts
  `units_original=105 units_minimized=105` match `entry_sourced=1`.

## Residual risk and verification gaps

- BuildF6B's own breakdown "105 (54 census + 0 shapes + 15 baseline + 36 host lines)"
  is off-by-one-swapped per file: actual unit counts are 55 census + 35 host (counter
  splits on `\n`, drops the final empty element; `original/census.tsv` has no trailing
  newline, `host.tsv` has one). Total 105 is correct; the entry only cites the total,
  so no entry defect — flag for the source report.
- The 512-mode sweep's "WINNERS []" is trusted from BuildF6B's report; only the 6
  printed rows are receipted. My independent ddmin re-run (171 tests, all false) covers
  the claim's consequence but not the full sweep enumeration.
- `Oracle.kills` cache keys omit line contents (`c2-measure-v2.py:165`, CriticC2v2 Q1);
  irrelevant at E where `kills` is uniformly false, but any future PASS claim should be
  re-verified against that defect.
- No anchored-fixture proof exists beyond the structural argument + 171-test sweep:
  a subset could in principle kill via a path I did not enumerate (e.g., different
  divergence classes), but `kills()` requires mutant exit 0, and every manifest state
  produces at least one mutant divergence under the anchored census — consistent with
  the sweep and the argument.

## Tooling

No installs or updates (none needed: git, bash, python3, diff, tmpfs mount sufficed).
Pacman untouched per the host-wide pause. Processes: all synchronous, none left running;
the noexec tmpfs was unmounted and removed.
