# T55W2CritFreeze2 — freeze soundness F2 (round 55, wave 2)

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (base `0a2010ac`, content commit C0 `9cf0146b`).
Scratch `/fast/scratch/hyaku/tameshi-r55/T55W2CritFreeze2` (fixtures `receipt-fixture-hole`,
`receipt-fixture-wrap`, every git call addressed with `-C` after a `--show-toplevel` assertion).
Receipts: `.ufo/waves/round-55/w2/T55W2CritFreeze2-receipts/`. No lane production file, no frozen file,
no wave spec was edited; no tool was installed (nothing was missing: `git`, `python3`, `ps`, `stat` sufficed).

**Answer up front**

1. Every sha256 in `freeze.json` re-derives at **both** candidate pointers (`e2979f2` = 7/7, `133b2ce` = 7/7),
   the manifest covers every `contract.frozen_paths` entry except itself, and its `amendments` array is
   byte-identical to the contract's. That part is sound.
2. `deciding-run.sh`'s `FROZEN` list does **not** equal the contract's `frozen_paths`: it omits
   `.ufo/evidence/round-55/c1/staged-at-freeze.txt` — the receipt the C1 counter derives R54.9's value from.
   A REV that rewrites that frozen receipt still gets `FROZEN_UNCHANGED=1` and C1 `PASS` (F1).
3. `e2979f2` is **not** a sound freeze pointer: with its own bytes the C2 counter cannot return `total=0` on
   **any** tree (all-green arithmetic yields `total=1`), and the pointer of record has already moved to
   `133b2ce` (lane HEAD at review time, whose commit message says "Freeze pointer moves to this commit"; the
   live phase-A control run scores at `FREEZE=133b2ce`). See F2/F3.
4. `FROZEN_UNCHANGED=1` holds for a REV that **descends from `e2979f2` without touching the seven listed
   paths** — C0 (`9cf0146b`) qualifies (rc=0). It does **not** hold for the lane HEAD or for any REV built on
   it (`133b2ce` changes `c2/measure.py`, `contract.json`, `freeze.json`; rc=1). Descent is not sufficient;
   only tree equality on the seven paths is.

Severity: **F1 high (integrity of the frozen set)**; **F2 high (the pointer's base receipt is irreproducible)**;
**F3 medium (an amendment is post a scored control line)**; **F4 medium (amendment 5's stated predicate is only
half implemented)**. None of them changes a claim's verdict at C0 — C1 reproduces exactly (`total=0`) and C2's
base verdict is false either way — but F1 lets a REV rewrite the value C1 certifies, so it is the one that must
be closed or explicitly declared before the deciding run.

---

## 1. Manifest re-derivation (no finding)

`git cat-file -p <rev>:.ufo/evidence/round-55/freeze.json`, then
`sha256(git cat-file -p <rev>:<entry>)` for each of its seven entries
(receipt `freeze-rederive-coverage-frozen.txt`, section 1):

| entry | `e2979f2` | `133b2ce` |
|---|---|---|
| `contract.json` | OK (`31d5c8ad…`) | OK (`fe5f9050…`) |
| `c1/measure.py` | OK (`5e8f50d1…`) | OK (`5e8f50d1…`) |
| `c2/measure.py` | OK (`36ca47d3…`) | OK (`0458f632…`) |
| `no-harm.sh` | OK (`d93469db…`) | OK (`d93469db…`) |
| `deciding-run.sh` | OK (`af11d755…`) | OK (`af11d755…`) |
| `controls.sh` | OK (`7c0cacb5…`) | OK (`7c0cacb5…`) |
| `c1/staged-at-freeze.txt` | OK (`921ad419…`) | OK (`921ad419…`) |
| **verdict** | **7/7** | **7/7** |

`freeze.json` does not hash itself (`freeze.note` says so, and the check confirms it).

## 2. Coverage and set equality (F1)

```
rev e2979f2 / 133b2ce (identical)
  contract.frozen_paths: 8
  freeze.files:          7          contract - manifest: [freeze.json]      (the manifest itself — correct)
  deciding FROZEN:       7          contract - deciding: [.ufo/evidence/round-55/c1/staged-at-freeze.txt]
  SET_EQUAL contract==deciding: False
  freeze.amendments == contract.amendments: True (7 vs 7 at e2979f2, 8 vs 8 at HEAD)
```

`deciding-run.sh:65`:
`FROZEN="$E/contract.json $E/freeze.json $E/c1/measure.py $E/c2/measure.py $E/no-harm.sh $E/deciding-run.sh $E/controls.sh"`
— seven entries, no `c1/staged-at-freeze.txt`. Wave 1's own freeze critic compared these sets at `631cd64`
and got equality (`T55W1CritFreeze-receipts/r2-coverage-sets.txt`); **amendment 7 added the path to
`contract.frozen_paths` and to `freeze.files` but not to the gate's list**, so the equality was lost in the
amendment that introduced the path. That is mechanical, not inferred:

```
$ <contract at 631cd64>.frozen_paths        -> 7 entries (no staged-at-freeze.txt)
$ <contract at e2979f2>.frozen_paths        -> 8; added by the amendments = ['.ufo/evidence/round-55/c1/staged-at-freeze.txt']
$ git rev-parse 631cd64:<path> e2979f2:<path> 133b2ce:<path>
  78446c1b…  78446c1b…  78446c1b…     (blob id unchanged at all three; file sha256 af11d755… in both manifests)
```

### F1 — a REV may rewrite a contract-frozen receipt and the gate stays green

`receipts/frozen-path-hole.txt` (fixture `receipt-fixture-hole`, `--show-toplevel` asserted):

```
$ git clone --shared LANE D ; git -C D checkout -b probe 9cf0146b   # C0
$ sed -i 's/^output=81$/output=999/' D/.ufo/evidence/round-55/c1/staged-at-freeze.txt
$ sed -i '2695s/staged=81/staged=999/' D/SCORECARD.md
$ git -C D commit -am 'probe: rewrite the frozen staged receipt to 999 and matching record'
  NEW=cb96e9f15b90
$ git -C D diff --quiet e2979f2 cb96e9f1 -- <deciding-run.sh FROZEN list>
  rc=0 -> FROZEN_UNCHANGED=1
$ git -C D diff --name-only e2979f2 cb96e9f1 -- .ufo/evidence/round-55
.ufo/evidence/round-55/c1/staged-at-freeze.txt
$ python3 c1-frozen.py --lane D --rev cb96e9f1 --work <empty> --explain
  EXPLAIN R54.9 ok ... derived=reviewers=5 attack=21/76 seats=76 staged=999
  C1_R55: ... total=0 C1_R55_PASS=true     exit=0
control (same counter, same clone, C0 untouched):
  EXPLAIN R54.9 ok ... staged=81
  C1_R55: ... total=0 C1_R55_PASS=true     exit=0
```

Freeze integrity also stays `OK` (`receipts/freeze-integrity-blind-to-rev.txt`, the gate's block run verbatim:
`FREEZE_INTEGRITY: OK files=7 amendments=7`): it hashes the manifest's entries **at FREEZE** and never takes
`REV`, while the counter reads the receipt **at REV** (`c1/measure.py`, `staged_count(lane, rev)` →
`text(lane, rev, ".ufo/evidence/round-55/c1/staged-at-freeze.txt")`).
So the two gates together do not enforce the frozen set the contract declares: R54.9's corrected arm compares
the record against a number the REV itself supplies.

Impacted axis: **calibration** (C1's "the corrections section carries the value the tree derives, not a literal
the author chose" — the receipt *is* a literal committed in the tree).
Smallest safe correction (do not re-freeze post-control): at the deciding run, assert
`git diff --quiet FREEZE REV -- .ufo/evidence/round-55/c1/staged-at-freeze.txt` and write its exit into
`$OUT/frozen.stdout`; the one-line addition to `FROZEN` is the same fix but edits a frozen file, so it is only
safe under a new freeze **before** any control verdict exists.

## 3. The two pointers (F2, F3)

### F2 — `e2979f2`'s C2 counter cannot return `total=0`; the pointer of record is `133b2ce`, whose base receipt no longer reproduces

`receipts/arithmetic-frozen-c2.txt` loads each frozen counter as a module and calls its own `modes()`:

```
e2979f2: len(table)=14 allocating=9 lazy=5 cheap=13
  total formula uses len(table): True   note term 8: True
  all-green total with empty bad map = 1 => C2_R55_PASS=false
133b2ce: len(table)=14 allocating=9 lazy=5 cheap=13
  total formula uses len(cheap): True   note term len(allocating): True
  all-green total with empty bad map = 0 => C2_R55_PASS=true
```

`e2979f2`'s total subtracts `len(table)=14` from `empty_ok`/`usable_ok` (which run `cheap=13` modes) and still
subtracts `8` from `note` (nine modes). At the all-green state the verdict therefore reads `total=1` with an
empty `bad` map — the exact state amendment 8 describes. It is not merely unreachable at all-green: the two
denominator terms are each ≥ 1 and the note term is ≥ −1 on every tree (`note ≤ 9`), so `total ≥ 1` always.
Amendment 8 changes only those two lines:

```
$ git diff e2979f2 133b2ce -- c2/measure.py
-        + (len(table) - empty_ok) + (len(table) - usable_ok) \
-        + tmp_total + (7 - docs) + (8 - note) + (1 - skill)
+        + (len(cheap) - empty_ok) + (len(cheap) - usable_ok) \
+        + tmp_total + (7 - docs) + (len(allocating) - note) + (1 - skill)
```

So **`e2979f2` is not a sound deciding pointer**: under it C2 is undecidable for every tree (same class as
wave 1's F2, now arithmetic instead of `strace`). The pointer of record is `133b2ce` (`git log`: "Freeze pointer
moves to this commit"), and the round is already scoring there:

```
$ pgrep -af "controls.sh a"
748996 bash .ufo/evidence/round-55/controls.sh a LANE 133b2ce6d4d8 0a2010acd1e9 .ufo/evidence/round-55/control
$ ps -o lstart= -p 748996
Wed Oct 28 14:21:12 2026
$ cat .ufo/evidence/round-55/control/controls-a.stdout
CTL CTL_0_c1 C1_R55: rev=0a2010acd1e9 ... total=10 C1_R55_PASS=false
CTL CTL_0_c2 C2_R55: rev=0a2010acd1e9 grammar=6/9 ... total=20 C2_R55_PASS=false
```

The last line is the defect: at base, the pointer-of-record counter prints **`total=20`**, while the committed
`before/c2.stdout` at `e2979f2` and the contract's C2 `before` string both say **`total=21`**
(`.ufo/evidence/round-55/before/c2.stdout`, `contract.json` claims.C2.before). Amendment 8 changed the total
formula and did **not** re-measure the base receipt; a receipt the contract quotes is no longer producible by
the counter the manifest certifies. (Arithmetic: `(13−13)+(13−13)+(9−0) = 9` instead of `(14−13)+(14−13)+(8−0) = 10`,
so `21−10+9 = 20`.) The C1 side still reproduces exactly (`c1-frozen-at-base.stdout`: `premise=9/10 stale=4
total=10`, identical to the committed receipt).

Impacted axis: **operability** (the contract's frozen `before` claim). It does not move the base verdict
(false either way), so it is a record defect, not a decidability blocker: the smallest safe correction is an
erratum in the non-frozen record (SCORECARD/LOG) citing the pointer's own phase-A receipt, not a re-freeze.

### F3 — amendment 8 is not "before any control score"

```
$ git log -3 --format='%h %ci'
133b2ce 14:21:00  (amendment 8)
9cf0146 14:16:39  (C0)
e2979f2 14:16:25  (amendments 1-7)
$ stat -c 'birth=%w mtime=%y' .ufo/evidence/round-55/control/controls-a.stdout
birth=14:16:54.626  mtime=14:21:14.592     # same inode: created 14:16:54, truncated 14:21:14
```

`controls.sh` writes only to stdout (the caller redirects), so that inode is a phase-A run's capture. A phase-A
run therefore started at **14:16:54** and its first scored line (`CTL_0_c1`) predates amendment 8 at
**14:21:00**; the live run started **14:21:12** (process above) and truncated the same inode at 14:21:14.
Amendments 1–7 (14:16:25, one commit) are unambiguously pre-control — no `control/` entry existed at that time
(`control/` birth 14:16:54) and no control receipt is committed in any ref (`git log --all -- …/control | wc -l`
= 0). Amendment 8 is pre the **completed** control set (no `CONTROLS_A:` verdict exists) but post a scored
`CTL` line. Its freeze text ("before any control score") is therefore not literally true.

Impacted axis: **calibration** (the freeze's own provenance). Smallest safe correction: correct the amendment-8
disclosure to "before any completed control set; a phase-A run began 14:16:54 and printed its first control
line before this amendment; no verdict line exists" and record the phase-A start time in the deciding receipt.
Do **not** amend the instrument again — that would be genuinely post-control.

## 4. The seven amendments, one by one (a) pre-control, (b) plumbing/surface, (c) receipt

All seven are in the single commit `e2979f2` (14:16:25), i.e. 29 s before the first control capture was even
created → **(a) holds for all seven**. (b)/(c) per amendment (`git diff 631cd64 e2979f2`; byte-pinned reproducer
`T55W1ScribeSkill-receipts/c2-measure.sha256` = `36ca47d3…` = exactly the `e2979f2` `c2/measure.py`, whose run
`c2-integrated.out` reads `rev=08d64e94… grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7
note=9/9 skill=1/1 total=1`):

| n | claim (freeze.json) | code (at `e2979f2`) | surface? | receipt |
|---|---|---|---|---|
| 1 | clone checked out detached → tool misclassified; now a branch at REV | `git checkout -q -B r55-rev a.rev` | plumbing (discovery); predicate unchanged | `c2-integrated.out` (usable/empty 13/13 on a branch-headed clone) |
| 2 | doc arms matched raw text, marker split by wrap; now whitespace-normalised | `def norm(...)`, `MARKER in norm(note)`, `norm(SKILL.md)` | plumbing (typo-class); predicate unchanged | `c2-integrated.out` docs=7/7 note=9/9 at C0 |
| 3 | label was `--selftest`, invoked as `selftest` | `"%s selftest" % tool if tool == "bash-witness-study"` | plumbing; predicate unchanged | `c2-integrated.out` note=9/9 |
| 4 | usable arm took rc from `strace -f` | plain `run()` rc; `trace()` only for the census | **measurement method changed** (rc now from a different invocation), disclosed | `usable=13/13` at C0 (`c2-integrated.out`) vs `12/13` with the old rc source (`T55W1ExecC2Full-receipts/c2-committed-9d0768.stdout`) |
| 5 | stale scan line-scoped; LOG.md joins the record set, whitespace-collapsed | `RECORD += "LOG.md"`; `scan_span()` added | **surface change** (record set widened), disclosed — but see F4 | `before/c1.stdout` at base (`premise=9/10 stale=4`), reproduced exactly by `c1-frozen-at-base.stdout` |
| 6 | ninth allocating mode `registry-check --rev`; **denominators 8→9** | new table row, `cheap=False`; `cheap` flag added | **surface change, disclosed** (denominators) | `c2-integrated.out` grammar=9/9 |
| 7 | staged count from the committed receipt; R54.8 needs `SUPERSEDED (round 55` | `staged_count()` reads `c1/staged-at-freeze.txt`; token tightened | **surface change, disclosed** (derived value source + premise) | `c1/staged-at-freeze.txt` itself (`command=…`, `output=81`); `before/c1.stdout` R54.9 `premise=miss staged=0` at base (the receipt does not exist at base) |

Amendment 8 (at `133b2ce`, not among the seven): (b) **bookkeeping, disclosed** — denominators only, matching
the verdict print it sits next to; (c) reproduced by the pre-amendment receipt `c2-integrated.out`
(`total=1`, empty `bad` map) and by the pointer's own base run (`CTL_0_c2 … total=20`, section 3); (a) fails in
the literal sense (F3).

### F4 — amendment 5 says "no stale assertion may stand"; only R54.1 gets a span scan

`scan_span` has exactly one call site (`c1/measure.py:203`, R54.1's positive-control pattern). The other stale
patterns stay line-scoped (`total=14`, `7883e0e5|fe70474d`, `84 staged`, …). `receipts/amendments-timeline-and-wrapped-scan.txt`
(fixture `receipt-fixture-wrap`, C0 + a hard-wrapped falsehood appended to LOG.md):

```
$ printf '\nThe other 84\nstaged entries were refused for capacity.\n' >> D/LOG.md ; git -C D commit …
$ python3 c1-frozen.py --lane D --rev 7ecf77812db3 --work <empty> --explain
  EXPLAIN R54.9 ok premise=ok corrected=ok stale=0 derived=… staged=81
  C1_R55: … total=0 C1_R55_PASS=true      exit=0
$ python3 matchers.py D
line-scoped hits: 0
span hits: 1
```

The round-54 defect the amendment cites *was* the wrapped positive control, which it closes; but the claim it
writes down ("no stale assertion may stand in the lane's records outside the corrections section") is broader
than the code, and the `84 staged` assertion — the other wrapped defect of the same round — is still invisible.
Impacted axis: **calibration**. Smallest safe correction: call `scan_span` for every stale pattern (a pure
counter change, so it belongs to a freeze, not to this wave), or restate the amendment's predicate as
"R54.1's pattern is scanned whole-document".

## 5. Pointer provenance (informational)

No frozen document names the pointer (`grep -c e2979f2` over all eight `frozen_paths` = 0 for each;
`freeze.json` keys are `round/files/amendments/note`). `deciding-run.sh` takes `FREEZE` as an argument and
never constrains it (wave-1 `T55W1CritFreeze` C19), so `e2979f2`, `133b2ce` — and any later commit whose
manifest is regenerated — all self-certify. Two consequences for this wave: the wave spec's `e2979f2` is one
amendment stale, and the only thing separating "amendment before controls" from "amendment after controls" is
file timestamps. Record the pointer and the phase-A start time in `$OUT/` so the receipt carries it.

## Artifacts opened

`.ufo/evidence/round-55/{contract.json, freeze.json, deciding-run.sh, controls.sh, no-harm.sh, c1/measure.py,
c1/staged-at-freeze.txt, c2/measure.py, before/c1.stdout, before/c2.stdout, control/controls-a.stdout}` (at
`e2979f2` and/or `133b2ce` and/or the working tree); `SCORECARD.md` (C0); wave-1 receipts
`T55W1CritFreeze.md`, `T55W1CritFreeze-receipts/{r2-coverage-sets.txt,r8-frozen-gate-amendment.txt,r13-self-referential-freeze.txt}`,
`T55W1ScribeSkill-receipts/{c2-measure.sha256,c2-integrated.out,c2-explain-ee45944.stdout}`,
`T55W1ExecC2Full-receipts/c2-committed-9d0768.stdout`, `T55W1ScribeLog-receipts/before-receipt-drift.txt`,
`T55W1SentScope-receipts/before-receipt-timeline.txt`; `.ufo/waves/round-55/{spec-w2.json,build-spec-w2.py}`.

## Reproduction (own runs)

| run | command | result |
|---|---|---|
| C1 at base, `e2979f2` bytes | `python3 c1-frozen.py --lane LANE --rev 0a2010ac --work <empty> --explain` (`receipts/c1-frozen-at-base.stdout`) | `premise=9/10 stale=4 total=10` — **identical** to `before/c1.stdout` at `e2979f2` |
| C2 at base, `e2979f2` bytes | `python3 c2-frozen.py --lane LANE --rev 0a2010ac --work <empty> --explain` (463 s; `receipts/c2-frozen-e2979f2-at-base.stdout`) | `grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/9 skill=0/1 total=21` — **identical** to `before/c2.stdout` at `e2979f2` |
| C2 at base, `133b2ce` bytes | the pointer's own live phase-A control (`controls.sh a … 133b2ce 0a2010ac`) | `total=20`, i.e. **not** the committed `total=21` (F2) |
| C1 at C0, `e2979f2` bytes | `--rev 9cf0146b` (`receipts/c1-at-C0.stdout`) | `total=0 C1_R55_PASS=true` |
| C1 at C0 + rewritten frozen receipt | fixture A (`receipts/frozen-path-hole.txt`) | `total=0`, `staged=999`, `FROZEN_UNCHANGED=1` (F1) |
| C1 at C0 + wrapped `84 staged` | fixture B (`receipts/amendments-timeline-and-wrapped-scan.txt`) | `stale=0 total=0` (F4) |

## Commands (representative)

```
git cat-file -p <rev>:.ufo/evidence/round-55/freeze.json | python3 …           # re-derive 7 entries
git diff --quiet e2979f2 9cf0146b -- <FROZEN list>    # rc 0  -> FROZEN_UNCHANGED=1
git diff --quiet e2979f2 133b2ce  -- <FROZEN list>    # rc 1  -> FROZEN_UNCHANGED=0
git clone --shared --quiet LANE D && git -C D checkout -b probe 9cf0146b      # fixtures
python3 c1-frozen.py --lane D --rev <rev> --work <empty> --explain
python3 -c 'import importlib.util; … modes()'                                 # per-counter denominators
stat -c 'birth=%w mtime=%y' .ufo/evidence/round-55/control/controls-a.stdout
ps -o lstart= -p 748996 ; pgrep -af 'controls.sh a'
```
