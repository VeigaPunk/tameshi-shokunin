# T55W3RevCounterGreen — both frozen counters at C0

Seat: reviewer (calibration axis). Lane `tameshi-shokunin`. Content commit
C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`; counter bytes taken from the freeze
commit `133b2ce6d4d86d783db38607343c3654350194b8` (the assignment's "bytes at 133b2ce",
milestone "counters at C0 after amendment 8"). Every run used a fresh empty work dir.
Scratch: `/fast/scratch/hyaku/tameshi-r55/T55W3RevCounterGreen` (`git clone --shared`
copies at C0; no lane file was written, no mutating git command ran in the lane).
Receipts: `.ufo/waves/round-55/w3/T55W3RevCounterGreen-receipts/` (numbered `01`-`13`,
plus the exact counter bytes I ran and `gate0.py`).

## Verdict — both counters are green at C0

```
C1_R55: rev=9cf0146b94dd classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
C2_R55: rev=9cf0146b94dd grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true
```

**EXPLAIN lines that are not `ok`: none.** C1 printed ten `EXPLAIN … ok` lines (receipt
`03`), C2 printed 43 `EXPLAIN … ok` lines — 9 grammar, 5 lazy, 13 empty, 13 usable,
docs 7/7, note 9/9, skill 1/1 (receipt `11`). Both exited 0.

Both verdicts also hold under the **current** (amendment-9) C1 bytes and from the real
lane, so moving the freeze pointer forward does not lose the reading:

| run | counter bytes | lane source | receipt |
|---|---|---|---|
| C1 @ C0 | `5e8f50d1` (133b2ce) | shared clone | `03-c1-amendment8-bytes-at-C0.stdout` |
| C1 @ C0 | `83dfbbb0` (4f7a704, = worktree) | shared clone | `04-c1-amendment9-bytes-at-C0.stdout` |
| C1 @ C0 | `83dfbbb0` | real lane | `05-c1-worktree-bytes-real-lane-at-C0.stdout` |
| C2 @ C0 | `0458f632` (133b2ce = 4f7a704) | shared clone | `11-c2-amendment8-bytes-at-C0.stdout` |
| C2 @ C0 | `0458f632` | real lane | `15-c2-real-lane-at-C0.stdout` |

Commands (work dirs created empty, `--work` guard honoured):

```
python3 c1-frozen133.py --lane <lane-or-clone> --rev 9cf0146b94d --work <empty> --explain
python3 c2-frozen133.py --lane <lane-or-clone> --rev 9cf0146b94d --work <empty> --explain
```

Byte provenance (receipt `01`, `$ git show <rev>:<path> | sha256sum`):
c1 `5e8f50d1` at 133b2ce and at C0, `83dfbbb0` at 4f7a704; c2 `36ca47d3` at C0 and
`0458f632` at 133b2ce and 4f7a704 — i.e. C0 predates amendments 8 and 9, which is why
the assignment names the freeze commit for the bytes and C0 for the content. The
`freeze.json` manifest is internally consistent at 133b2ce (7 files / 8 amendments) and
at 4f7a704 (7 files / 9 amendments); `gate0.py` re-derives both from their own bytes,
`GATE0 … OK` (receipt `01`).

## Findings

### F1 (medium) — R54.2 measures two of the three pointers its own correction names

`c1/measure.py` line 212: `stale = scan(lane, rev, ("SCORECARD.md",), r"7883e0e5|fe70474d")`.
ER-R54-2 (`SCORECARD.md` at C0) names **three** old pointers: `7883e0e5`, `fe70474d` and
`097985c1` ("in the fleet report"). `097985c1` is in no stale pattern anywhere.

Receipt `12-control-third-pointer-097985c1.txt`: a C0 clone with one SCORECARD line
outside the corrections section — "The fleet report still names the third pointer
`097985c1` as the freeze pointer." — still reads

```
C1_R55: rev=63952e382ce7 classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
RC=0
```

So the counter can certify "the record agrees with the tree on the ten routed defects"
while the record still carries the routed wrong pointer. At C0 itself no `097985c1`
survives outside the corrections section, so this does not falsify today's verdict — but
the deciding run happens at the **closing** REV, not at C0, and the closing commits are
where the integrator writes SCORECARD rows.

### F2 (medium) — the stale arm is narrower than its own stated surface (LOG.md pointer included)

Lines 212, 220 and 262 scan `("SCORECARD.md",)`, `("SCORECARD.md",)` and
`("corpus/lessons/round-54.md",)` respectively, while the docstring says the stale arm
reads "the lane's records (`SCORECARD.md`, `corpus/QUALITY.md`,
`corpus/lessons/round-54.md`)" and `RECORD` adds `LOG.md`. Only R54.1 uses `RECORD`.

The gap is not hypothetical: amendment 5 justifies adding `LOG.md` and the
whitespace-collapsed pass precisely because *"`LOG.md` … still carried R54.2's stale
pointer"*. R54.2's scan never looks at `LOG.md`, so the defect that motivated the
amendment is still unmeasured.

Receipt `06-control-stale-outside-scorecard.txt`: a C0 clone (`ctl3` @ `db78d38d`) that
carries the wrong pointer, the wrong total and the wrong staged count **only** in
`LOG.md` and `corpus/QUALITY.md` —

```
db78d38d:LOG.md:2555:Round-54 close still cites `7883e0e5` as the freeze pointer.
db78d38d:corpus/QUALITY.md:1592:Surviving wrong quote: `total=14` packages and pointer `fe70474d`.
db78d38d:corpus/QUALITY.md:1593:Also `the other 84 staged entries`.
```

— reads `total=0 C1_R55_PASS=true` under **both** byte versions (`5e8f50d1` and
`83dfbbb0`). Receipt `07` is the positive control for the same tokens placed in
`SCORECARD.md`: R54.2 and R54.3 fire there (`total=2 C1_R55_PASS=false`), which proves
the rows work and that the miss is the file surface, not the pattern.

Suggested (not applied — lane files are out of my write scope): scan `RECORD` for all
ten rows, i.e. `R54.2` → `RECORD` with `7883e0e5|fe70474d|097985c1`, `R54.3` → `RECORD`,
`R54.9` → `RECORD`.

### F3 (low) — with FREEZE=133b2ce no closing REV can satisfy deciding-run's FROZEN check

`deciding-run.sh` line 66 fails the run (`FROZEN_UNCHANGED=0`, `rc=1`) when any frozen
file differs between FREEZE and REV, and line 45 requires `HEAD == REV`. Receipt
`02-frozen-list-vs-candidate-revs.txt` (same `$FROZEN` list as line 65):

```
diff --quiet 133b2ce 9cf0146 -- $FROZEN  -> rc=1   (c2/measure.py, contract.json, freeze.json)
diff --quiet 133b2ce c31cdd9 -- $FROZEN  -> rc=1   (contract.json, freeze.json)
diff --quiet 133b2ce 4f7a704 -- $FROZEN  -> rc=1   (c1/measure.py, contract.json, deciding-run.sh, freeze.json)
diff --quiet 133b2ce 133b2ce -- $FROZEN  -> rc=0
```

Only the freeze commit itself passes, and the lane's branch cannot be parked there while
the round's wave-2/3 evidence is committed. The freezefile is self-consistent at
`4f7a704` (amendment 9) and both counters are green there (table above), so the closure
route is: pass `FREEZE=4f7a704…`, keep the closing REV free of frozen-file edits. This is
a closure constraint for the L1/revenger, not a defect in either counter.

### F4 (low) — frozen c2 docstring denominators contradict the code after amendments 6/8

Receipt `13-counter-code-and-doc-facts.txt`: `c2/measure.py` (sha `0458f632`, unchanged
since 133b2ce) still documents `grammar 8 allocating modes`, "the eight allocating modes
issue no mkdir", `names all eight allocating modes` and the verdict template
`grammar=N/8 … note=N/8`, while `modes()` builds **9** allocating rows and the verdict
interpolates `len(allocating)` — it prints `grammar=9/9 … note=9/9`. A reader who trusts
the frozen header mis-reads the arm's own denominator. Documentation only; the numbers
the counter prints are right.

### F5 (low) — amendment 9(b) closes no way to pass, and leaves dead code

Amendment 9 states the collapsed pass now runs "for every row" and that this "close[s] a
way to pass without the work". For the rows it was wired into (R54.2/R54.3/R54.9) the
patterns are single bare tokens (`7883e0e5`, `total=14`, `84 staged`); an intact token is
already found by the line pass, and a token split by a hard wrap is found by neither,
because the collapsed text is joined with a space (`flat = " ".join(body.split())`,
receipt `13`). Receipt `09-boundary-split-token.txt`: `total=1` newline `4` outside the
corrections section → `R54.3 ok`, `total=1`, i.e. still invisible. The change is
harmless symmetry, not added detection; `scan_span()` is now dead (defined, never
called) and `classes(..., staged_root)` keeps a parameter unused since amendment 7.

## What did hold (checked, not assumed)

* C1 is sensitive: reintroducing `CTL_POS_c1 true` in SCORECARD outside the corrections
  section turns R54.1 red — `stale=1 … total=1 C1_R55_PASS=false` under both byte
  versions (receipt `14-control-ctlpos-reintroduced.txt`) — and the pointer/total tokens
  in SCORECARD turn R54.2/R54.3 red (receipt `07`).
* C1's green depends on the **derived** values, not on the stale fixes alone: removing
  the `## Round 55 - round-54 record corrections` section from C0 gives
  `classes_corrected=0/10 total=10 C1_R55_PASS=false` (receipt
  `08-control-corrections-section-load-bearing.txt`).
* Premises are independent of this round's own writes: R54.1 premise from
  `.ufo/evidence/round-54/control/controls-b.stdout` (`CTL_MISMATCH`, `CONTROLS_B: 2/3`,
  first committed at `7fa9a5e`), R54.3 from `round-54/before/c2.stdout` (`total=13`),
  R54.2 from `round-54/after/frozen.stdout` (`freeze=077d431e…`), R54.4 from
  `round-54/freeze.json` (`c2/measure.py` → `8528ee85…`). All open by `git show` at C0.
* R54.9's `staged=81` is not a literal the author chose: the committed receipt
  `.ufo/evidence/round-55/c1/staged-at-freeze.txt` carries the command
  (`find …/merge/tameshi/knowledge -name '*.md' | wc -l`), its `output=81`, and an
  independent live count of that directory today returns 81.
* C2's document arms hold independently of the counter (receipt `10`): the grammar
  marker is in `corpus/knowledge/scratch-root-contract.md` and `SKILL.md`, the note names
  all nine allocating modes, and 7/7 `tools/registry.json` `scratch_root` cells carry the
  marker. The C2 `bad` map is `{}` and `tmp_mkdirs=0`.
* Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
  → exit 0 (140 rows).

## Residual risk / verification gaps

1. My green C1 is measured on the **C0 tree**. The deciding run measures the closing REV,
   which adds wave-2/3 reports and closing record edits. F1/F2 are exactly the ways that
   could turn green into a wrong green; nothing in the counter would notice a stale
   pointer written into `LOG.md`/`QUALITY.md` or a `097985c1` written into SCORECARD.
2. C2's grammar arm is a shape check (rc + one matching stderr line + no
   `RuntimeError`/`Traceback`); whether each tool's message names the *true* failing value
   is outside this counter (the contract lists this under `cannot_see`), and I did not
   re-derive the per-tool TMPDIR value strings beyond the grammar match.
3. `registry-check --rev` is measured on the grammar arm only (amendment 6); its usable
   path is covered by its own self-test, so a `--rev`-specific regression on a usable
   scratch root would not be seen here.
4. I did not run any control set (`controls.sh`), no-harm or the cold-read precheck: other
   seats own those, and my item is the two counter verdicts.

## Tooling

No tool installed or upgraded (pacman is paused host-wide; nothing was needed:
`python3` 3.14.8, `git`, `strace` were already present).

## Artifacts opened

`.ufo/evidence/round-55/contract.json`; `.ufo/evidence/round-55/freeze.json` (at
133b2ce, 4f7a704, C0); `.ufo/evidence/round-55/c1/measure.py` (133b2ce, 4f7a704);
`.ufo/evidence/round-55/c2/measure.py` (133b2ce, C0, 4f7a704);
`.ufo/evidence/round-55/c1/staged-at-freeze.txt` (C0); `.ufo/evidence/round-55/deciding-run.sh`;
`SCORECARD.md` (C0, corrections section), `corpus/QUALITY.md`, `corpus/lessons/round-54.md`,
`LOG.md` (base and C0); `.ufo/evidence/round-54/{control/controls-b.stdout,before/c2.stdout,after/frozen.stdout,freeze.json}`;
`corpus/knowledge/scratch-root-contract.md` (C0); `SKILL.md` (C0); `tools/registry.json` (C0);
`.ufo/waves/round-55/spec-w1.json`, `spec-w3.json`, `w3-dispatch.json`.
