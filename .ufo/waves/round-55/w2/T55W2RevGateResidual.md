# T55W2RevGateResidual — the deciding gate's residuals (round 55, wave 2)

Seat: reviewer, axis **calibration**. Milestone: the deciding gate's residuals.
Object under attack: `.ufo/evidence/round-55/deciding-run.sh` at counter freeze
`e2979f277138da503af27b263b783f626f109be4`, exercised against `git clone --shared`
fixtures at content commit C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.
The script was not edited; every fixture is a clone in my scratch. No lane production
file was touched (see the trailer).

## Verdict summary

| # | Residual | Reproduced at C0? | Blocking for the round's decision? |
|---|---|---|---|
| R1 | gate never compares the `rev=` a `CTL` line names with the revision under test — a stale receipt opens the gate | **yes**, including round-54's receipts copied verbatim | **yes** — the decision's control certification is unenforceable |
| R2 | the `as pre-registered` tally arm is satisfied by `0/0`, by `/`, and by a *failed* run's own tally `2/3`, `3/5`, `1/2` | **yes** | **yes** — the gate accepts its own negative evidence |
| R3 | `controls-*.exit` content is never read (round-54's `controls-b.exit` = `1` passes) | **yes** | **yes** (same class as R2; corroborating) |
| R4 | "a second invocation is refused" is OUTDIR-scoped: a fresh OUTDIR passes; an interrupted run leaves no guard state so the *same* OUTDIR is reusable | **yes** | **yes for the one-shot property**; a retry-until-green is possible |
| R5 | the verdict grep reads the worktree, not the blob at REV; `assume-unchanged` hides the divergence from the dirty-tree arm | **yes** | no (needs a deliberate index bit) — major |
| R6 | blob-ness is satisfied by a `120000` symlink blob; the grep then reads a file outside the lane | **yes** | no — minor, the arm is not what it claims |
| R7 | OUTDIR emptiness is never checked although the usage line says "EMPTY" | **yes** | no — minor |

All gate refusals that *do* work were re-verified as working (freeze integrity, head-is-not-rev
by construction, control-receipt-missing, control-receipt-not-a-blob for tree objects,
control-receipt-empty, verdict-missing, dirty-tree); the negative control in R2 shows the
verdict arm is the only content check and that it can refuse.

## Fixtures and the frozen bytes

Every fixture is built by `T55W2RevGateResidual-receipts/build-fixture.sh NAME KIND S`:
`git clone --shared` of the lane, `checkout --detach` at C0, `git rev-parse --show-toplevel`
asserted equal to the fixture dir before the commit, then one commit that adds
`.ufo/evidence/round-55/control/controls-{a,b}.{stdout,exit}`. Gate probes use
`T55W2RevGateResidual-receipts/probe.sh NAME S TIMEOUT`, which runs the frozen script from
the fixture and reports the exit code, any `DECIDING_REFUSED` line, and the artefacts:

```
rc=124  = still executing when the timeout fired, therefore past every gate refusal
rc=3    = a DECIDING_REFUSED line fired
```

The frozen bytes I ran are the pinned ones — `freeze.json`'s hashes re-derive at C0:

```
$ python3 -c "…sha256 of git show C0:<path> vs freeze.json['files'][path]…"
OK   .ufo/evidence/round-55/c1/measure.py
OK   .ufo/evidence/round-55/c1/staged-at-freeze.txt
OK   .ufo/evidence/round-55/controls.sh
OK   .ufo/evidence/round-55/deciding-run.sh
OK   .ufo/evidence/round-55/no-harm.sh
```
(the two `MISMATCH` lines that this check prints when `freeze.json` is taken from the *working
tree* are amendment 8's own re-pin at `133b2ce`; `git diff e2979f2 C0 -- .ufo/evidence/round-55/`
is empty, so `FROZEN_UNCHANGED=1` at C0 — confirmed in every run below.)

Context that bounds the finding: **no round-55 control receipt is committed at C0, or anywhere
in history.**

```
$ git -C <lane> cat-file -e 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb:.ufo/evidence/round-55/control/controls-a.stdout
fatal: path '.ufo/evidence/round-55/control/controls-a.stdout' exists on disk, but not in '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
$ git -C <lane> status --porcelain .ufo/evidence/round-55/control/
?? .ufo/evidence/round-55/control/
$ wc -l .ufo/evidence/round-55/control/controls-a.stdout
4   # one CTL line from a phase-A run in flight, no tally line
```

So at the revision under test the gate refuses `control-receipt-missing`; the residuals below are
about what it will *fail to refuse* once phase B lands its receipts. (While this seat ran, the lane's
`master` moved past C0 to `4c04c1d`, which commits `controls-a.stdout` — the real phase-A receipt,
`CONTROLS_A: 5/5 as pre-registered` — and leaves the other three receipts absent. That is the live
state, not the revision I was asked to attack, and it confirms the receipt shape my fixtures use:
per-control `rev=` values, one `CTL` line per control.)

---

## R1 — the gate never compares `rev=` with the revision under test (blocking)

The receipts carry the revision they were scored at: `controls.sh`'s `score()` runs the counter
with `--rev "$(git -C "$d" rev-parse HEAD)"` and echoes the counter's verdict line, whose first
field is `rev=…`. `deciding-run.sh` reads the receipts only for existence, blob-ness, size,
commit order and the tally line:

```
$ git show e2979f2:.ufo/evidence/round-55/deciding-run.sh | grep -n 'rev\|REV'
2:# … LANE REV FREEZE OUTDIR
3:#   LANE    absolute path of the lane repo        REV     the content revision
6:# re-derives from the bytes at FREEZE and every pre-registered control receipt is committed at REV in a commit
8:# an exit receipt after; the counters, no-harm and the precheck run from the bytes committed at REV …
11:LANE=$1; REV=$2; FREEZE=$3; OUT=$4
18:REV=$(git rev-parse --verify "$REV^{commit}") || exit 2
19:FREEZE=$(git rev-parse --verify "$FREEZE^{commit}") || exit 2
45:[ "$(git rev-parse HEAD)" = "$REV" ] || { echo "DECIDING_REFUSED head-is-not-rev"; exit 3; }
48:  git cat-file -e "$REV:$f" 2>/dev/null || { echo "DECIDING_REFUSED control-receipt-missing $f"; exit 3; }
49:  [ "$(git cat-file -t "$REV:$f")" = blob ] || { echo "DECIDING_REFUSED control-receipt-not-a-blob $f"; exit 3; }
50:  [ "$(git cat-file -s "$REV:$f")" -gt 0 ] || { echo "DECIDING_REFUSED control-receipt-empty $f"; exit 3; }
51:  c=$(git log -1 --format=%H "$REV" -- "$f")
61:  mkdir -p "$SCR/code/$(dirname $f)"; git show "$REV:$E/$f" > "$SCR/code/$f" || exit 2
63:git show "$REV:.ufo/evidence/round-48/quality/coldread-precheck.sh" > "$SCR/code/precheck.sh" || exit 2
66:if git diff --quiet "$FREEZE" "$REV" -- $FROZEN; then echo "FROZEN_UNCHANGED=1 freeze=$FREEZE rev=$REV" …
67:bash "$SCR/code/no-harm.sh" "$LANE" "$REV" > "$OUT/no-harm.stdout" 2>&1; echo $? > "$OUT/no-harm.exit"
70:bash "$SCR/code/precheck.sh" "$LANE" "$BASE" "$REV" > "$OUT/coldread-precheck.stdout" 2>&1; …
77:    c1) python3 "$SCR/code/c1/measure.py" --lane "$LANE" --rev "$REV" --work "$SCR/c1" --explain > "$OUT/c1.stdout" 2>&1 ;;
78:    c2) python3 "$SCR/code/c2/measure.py" --lane "$LANE" --rev "$REV" --work "$SCR/c2" --explain > "$OUT/c2.stdout" 2>&1 ;;
```
Every other use of `REV` is a path into the counters/no-harm; the only uses inside the control gate
are the four provenance arms above. No receipt body is ever searched for `rev=`.

**The strongest reproduction needs no fabrication at all**: round-54's committed receipts,
copied byte for byte into round-55's control directory, open round-55's gate — and they are the
receipts that record round 54's own R54.1 failure (`rev=077d431e6996`, the round-54 *freeze*,
`CTL_MISMATCH CTL_POS_c1`, `CONTROLS_B: 2/3`, `controls-b.exit` = `1`).

```
$ git show 9cf0146:  .ufo/evidence/round-54/control/controls-b.stdout   (copied verbatim)
CTL CTL_POS_c1 C1_R54: rev=077d431e6996 … C1_R54_PASS=false
CTL_MISMATCH CTL_POS_c1 expected=true actual=false
CTL CTL_POS_c2 C2_R54: rev=077d431e6996 … C2_R54_PASS=true
CTL CTL_EXIT0 C2_R54: rev=7df0e0426c98 … C2_R54_PASS=false
CONTROLS_B: 2/3 as pre-registered
$ git show 9cf0146:.ufo/evidence/round-54/control/controls-b.exit
1
$ bash probe.sh prev-round $S 10
rc=124  (still executing when the timeout fired, i.e. past every gate refusal)
--- refusal lines:
(none)
--- gate artefacts in OUT:
  clean-tree-before.txt
  frozen.stdout
  no-harm.stdout
```

Two more variants, each a fixture commit at C0 + receipt commit:

```
$ bash probe.sh stale-rev $S 10     # phase-B receipt whose CTL lines name BASE 0a2010acd1e9
rc=124 … refusals: (none)
$ bash probe.sh bogus $S 10         # every CTL line names rev=000000000000 / ffffffffffff,
                                    # which do not resolve as commits at all
$ git -C fix-bogus cat-file -e 000000000000^{commit}
fatal: Not a valid object name 000000000000^{commit}
rc=124 … refusals: (none)
```

The full run on the stale-receipt fixture, to show the gate carries it to a decision record:

```
$ HYAKU_SCRATCH=$S/hyaku-full timeout 1500 bash fix-stale-rev/.ufo/evidence/round-55/deciding-run.sh \
    $S/fix-stale-rev $(git -C fix-stale-rev rev-parse HEAD) e2979f2… …/round-55/after
FREEZE_INTEGRITY: OK files=7 amendments=7
FROZEN_UNCHANGED=1 freeze=e2979f277138da503af27b263b783f626f109be4 rev=f4b670e7a5d964486d399c1565cb09f33744cc80
NOHARM coldread-floor score=6 credited=46 RED
COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=f4b670e7a5d9 cand_credited=46 lost=18 RED
CENSUS exit=0
C1_R55: rev=f4b670e7a5d9 classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
C2_R55: rev=f4b670e7a5d9 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
DECIDING_RUN_EXIT=1
$ ls after/
c1.end c1.exit c1.start c1.stdout c2.end c2.exit c2.start c2.stdout census.exit census.stderr
census.stdout clean-tree-after.txt clean-tree-before.txt coldread-precheck.exit
coldread-precheck.stdout deciding-run.exit frozen.stdout no-harm.exit no-harm.stdout
```

No `DECIDING_REFUSED` line, every gate artefact written, both counters executed at REV
(`c1.start`/`c2.end` present), a complete decision record on disk. The two `rc=1` sources are
outside the receipts and outside this item:

* `NOHARM coldread-floor` / `COLDREAD_PRECHECK … lost=18` — real at C0 in the lane itself, not a
  clone artefact: `python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev 9cf0146`
  prints `score=6 credited=46` against `--rev 0a2010ac` `score=8 credited=64`. This is the
  round's re-key obligation (another seat's item), and it means the deciding run cannot be green
  at C0 for a reason unrelated to the gate.
* `C2_R55 … total=1` with **every arm at full marks and `bad` empty** — the frozen counter's own
  pre-amendment-8 arithmetic. The run's own receipt:
  ```
  $ python3 -c "json of <SCR>/c2/c2-receipts.json"
  allocating=9 note=9 empty=13 usable=13 bad=none
  ```
  with `total = … + (len(table)-empty_ok) + (len(table)-usable_ok) + tmp_total + (7-docs) + (8-note) + (1-skill)`
  pinned at the freeze: two denominators are `14` where 13 cheap modes ran, one is `8` where 9
  allocating modes were measured. Amendment 8 (`133b2ce`) is exactly this fix. It is worth
  stating for calibration: **my receipts moved neither counter** — `C1_R55_PASS=true`, and C2's
  arms are all maxed, so what a receipt can and cannot influence is now measured, not assumed.

**The field would have caught the defect it was written for.** Round 54's deciding run was at
`rev=c21081008adb` (its own receipt, `.ufo/evidence/round-54/after/frozen.stdout`), while its
phase-B positive control says `CTL_POS_c1 C1_R54: rev=077d431e6996` and `CTL_POS_c2 … rev=077d431e6996`
— the freeze commit, i.e. R54.1. One comparison of those two fields would have refused that run
mechanically. The gate had the evidence and never looked at it.

**Blocking, and not closable inside this wave.** `deciding-run.sh` is hash-pinned twice
(`freeze.json` and the `FROZEN` window at line 65-66), so a seat edit is the wrong instrument;
this needs an amendment by the round owner. The correct arm is narrower than "compare every
`rev=`", because `controls.sh` clones a different revision per control on purpose (`clone_at
"$LANE" "$REV" base`, `… skip1`, `… fab`, and each control's commit moves HEAD again), so
phase-A lines legitimately name four different commits. Two facts are checkable and are exactly
the two that matter:

* `CTL_POS_c1` / `CTL_POS_c2` — phase B clones REV and scores it with no commit on top
  (`d=$(clone_at "$LANE" "$REV" pos)` then `score "$C1" "$d" …`), so those two lines name REV
  *exactly*: `grep -q "^CTL CTL_POS_c[12] .* rev=${REV:0:12} "`. That single line closes R1 and
  would have refused round 54.
* every other `CTL` line's `rev=` must resolve as a commit whose tree equals BASE's tree outside
  `.ufo/evidence/` (phase A) or REV's (phase B) — for the negative controls that is what
  "the control could not have fired" means.

Alternatives that do not need the receipts at all: have the gate re-score the controls itself,
or record the phase-B clone's `rev-parse HEAD` next to `FROZEN_UNCHANGED` and check it there.

What a stale receipt actually costs the decision: the deciding run still *measures* c1/c2 at REV
itself, but the controls are the only evidence that those counters **can fail** at REV. A
counter with a silently disabled arm — the class the wave-1 grammar seat found in the round-50
fence ("n17 passed by absence") — reads green and nothing in the record contradicts it. That is
R54.1 recurring one layer down: round 55 moved the fix for R54.1 into `controls.sh`'s discipline
and left the gate unable to verify it.

## R2 — `0/0` satisfies the tally arm; so does a failed run's own tally (blocking)

```
$ git show e2979f2:.ufo/evidence/round-55/deciding-run.sh | sed -n '54,55p'
grep -q '^CONTROLS_A: [0-9]*/[0-9]* as pre-registered' "$LANE/$E/control/controls-a.stdout" 2>/dev/null || { echo "DECIDING_REFUSED controls-a-verdict-missing"; exit 3; }
grep -q '^CONTROLS_B: [0-9]*/[0-9]* as pre-registered' "$LANE/$E/control/controls-b.stdout" 2>/dev/null || { echo "DECIDING_REFUSED controls-b-verdict-missing"; exit 3; }
```

That exact regex against candidate lines:

```
MATCH   CONTROLS_A: 0/0 as pre-registered
MATCH   CONTROLS_A: / as pre-registered          # both numerals empty
MATCH   CONTROLS_A: 1/9 as pre-registered
MATCH   CONTROLS_A: 3/5 as pre-registered
MATCH   CONTROLS_A: 5/5 as pre-registered trailing junk   # not end-anchored
NOMATCH CONTROLS_A: 5/5 not as pre-registered
```

`[0-9]*` cannot require a digit, the numerator is never compared with the denominator, and the
match is not anchored at the end.

Gate probes:

```
$ bash probe.sh zero-zero $S 10      # "CONTROLS_A: 0/0" and "CONTROLS_B: 0/0", zero CTL lines
rc=124 … refusals: (none)            # clean-tree-before.txt, frozen.stdout, no-harm.stdout
$ bash probe.sh failed-tally $S 10   # a failed phase run: tally 1/2 and 3/5, CTL_MISMATCH,
                                     # .exit carrying 1
rc=124 … refusals: (none)
$ bash probe.sh no-tally $S 10       # negative control: same bytes, tally line removed
rc=3
DECIDING_REFUSED controls-a-verdict-missing
```

The negative control matters: it shows the tally is the *only* content arm, and that the arm
works — it just asks a question that a failure can answer. Round-54's own committed
`CONTROLS_B: 2/3 as pre-registered` (R1) is a real instance of the same string.

## R3 — `controls-*.exit` content is never read (blocking, same class)

The four receipts enter the gate through `$CONTROLS`; the loop reads only `cat-file -e`,
`cat-file -t`, `cat-file -s` and `git log`:

```
$ git show e2979f2:.ufo/evidence/round-55/deciding-run.sh | sed -n '46,58p' | grep -n 'cat\|exit'
1:CONTROLS="$E/control/controls-a.stdout $E/control/controls-a.exit $E/control/controls-b.stdout $E/control/controls-b.exit"
3:  git cat-file -e "$REV:$f" …
4:  [ "$(git cat-file -t "$REV:$f")" = blob ] …
5:  [ "$(git cat-file -s "$REV:$f")" -gt 0 ] …
7:  git merge-base --is-ancestor "$FREEZE" "$c" …
```

No `cat`, no `git show`, no grep of a `.exit` file anywhere in the script. Both the
`failed-tally` fixture (`.exit` = `1`) and the `prev-round` fixture (round-54's
`controls-b.exit` = `1`, with a trailing comment line and blank line after it) opened the gate.
The one file whose whole purpose is to say *whether the phase run succeeded* is checked for
existence and size only — so "non-empty" is satisfied by `1`.

## R4 — the second-invocation guard is OUTDIR-scoped, and an interrupted run leaves none (blocking for the one-shot property)

```
56:for k in c1 c2; do [ -e "$OUT/$k.start" ] && { echo "DECIDING_REFUSED second-invocation $k"; exit 3; }; done
```

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w2/T55W2RevGateResidual-receipts/second-invocation.sh`
builds one fixture whose `after-a` holds a *completed* first run's `c1.start`/`c2.start`
(committed, so the dirty-tree arm cannot see them) and then:

```
### A: second invocation into the SAME outdir (after-a carries c1.start/c2.start)
  rc=3 refusals: DECIDING_REFUSED second-invocation c1;
### B: second invocation naming a DIFFERENT, empty outdir (after-b)
  rc=124 refusals:
  after-b artefacts:
    clean-tree-before.txt
    frozen.stdout
    no-harm.stdout
```

and an interrupted run is not recorded at all, because `$k.start` is written only after
no-harm, the precheck and the census (line 75), i.e. minutes into the run:

```
### C1: first run into after-c, interrupted at 6s
  rc=124 refusals:
    clean-tree-before.txt  frozen.stdout  no-harm.stdout      # no c1.start
### C2: re-run into the SAME after-c
  rc=124 refusals:                                            # accepted, counters re-run
```

So "a second invocation is refused" (header, line 7) holds only for the exact same OUTDIR after
a *completed* first run. A fresh OUTDIR, or the same OUTDIR after an interruption, re-runs the
whole decision — counters, no-harm, precheck, census — with a fresh scratch (`rm -rf "$SCR"` at
line 59) and overwrites nothing of the first record, so two decision directories can coexist
with different verdicts and nothing in either says which is the decision. Retry-until-green is
possible; a killed run is retried silently. (Operationally, the fresh-OUTDIT escape is also the
natural reaction to the dirty-tree arm, which refuses any untracked file anywhere outside OUT —
`?? .ufo/evidence/round-55/after/` from a previous attempt, or another seat's in-flight wave
file, both refuse the run; committing the previous attempt's outdir clears it *and* leaves the
guard blind, exactly as in variant B.)

## R5 — the verdict grep reads the worktree, and the index bit hides the divergence (major, not blocking)

```
54:grep -q '^CONTROLS_A: …' "$LANE/$E/control/controls-a.stdout"
```
The blob at `$REV:$f` is verified for existence/type/size (lines 48-50); the *bytes checked* come
from `$LANE/…`, i.e. the working tree. Normally the dirty-tree arm (line 57-58) forces the
worktree to equal HEAD, so the two coincide — but `git status --porcelain` is blind to a tracked
file with the assume-unchanged bit:

```
$ bash build-fixture.sh worktree worktree $S      # blob at REV: "CONTROLS_A: not scored …"
$ git -C fix-worktree cat-file -p HEAD:.ufo/evidence/round-55/control/controls-a.stdout
CONTROLS_A: not scored (phase A interrupted)
$ cat fix-worktree/.ufo/evidence/round-55/control/controls-a.stdout      # worktree
CONTROLS_A: 5/5 as pre-registered
$ git -C fix-worktree status --porcelain
?? .ufo/evidence/round-55/after/                     # nothing else: clean tree
$ git -C fix-worktree ls-files -v .ufo/evidence/round-55/control/
H .ufo/evidence/round-55/control/controls-a.exit
h .ufo/evidence/round-55/control/controls-a.stdout    # lowercase h = assume-unchanged
H .ufo/evidence/round-55/control/controls-b.exit
h .ufo/evidence/round-55/control/controls-b.stdout
$ git -C fix-worktree diff --stat -- .ufo/evidence/round-55/control/      # empty
$ bash probe.sh worktree $S 10
rc=124 … refusals: (none)
```

The committed receipt at REV can therefore say "not scored" while the run passes. Not blocking
on its own (it takes an index bit, so it is deliberate), but it means the gate's subject is not
the committed bytes it names, and the dirty-tree arm is not the airtight precondition it reads
as. The clean fix, if this were not frozen, is `git show "$REV:$f" | grep -q …`.

## R6 — a symlink is a blob (minor)

`git cat-file -t` on a `120000` entry answers `blob`, and `-s` is the length of the target path,
so "non-empty blob" is satisfied; the grep then follows the link out of the lane:

```
$ git -C fix-symlink ls-tree HEAD .ufo/evidence/round-55/control/
100644 blob 573541ac… controls-a.exit
120000 blob 4337a5cf… controls-a.stdout
100644 blob 573541ac… controls-b.exit
120000 blob 4337a5cf… controls-b.stdout
$ git -C fix-symlink cat-file -t HEAD:.ufo/evidence/round-55/control/controls-a.stdout   → blob
$ git -C fix-symlink cat-file -s HEAD:.ufo/evidence/round-55/control/controls-a.stdout   → 72
$ ls -l fix-symlink/.ufo/evidence/round-55/control/
lrwxrwxrwx … controls-a.stdout -> /fast/scratch/hyaku/tameshi-r55/T55W2RevGateResidual/outside-symlink.txt
$ cat fix-symlink/.ufo/evidence/round-55/control/controls-a.stdout
CONTROLS_A: 5/5 as pre-registered
CONTROLS_B: 5/5 as pre-registered
$ bash probe.sh symlink $S 10
rc=124 … refusals: (none)
```

Not blocking (it is forgery-adjacent, not staleness), but the recorded hardening — "each control
receipt must be a non-empty blob at REV … so zero-byte or tree objects cannot open the gate"
(`.ufo/evidence/round-54/contract.json:74`) — overstates what is checked: the blob can be a
pointer to arbitrary bytes outside the repository.

## R7 — OUTDIR emptiness is never checked (minor)

The usage line promises "an existing, EMPTY directory"; line 44 is `[ -d "$OUT" ] || …`. Variant
A and the interrupted-run re-run above both wrote into an `after-*` that already held a previous
run's `clean-tree-before.txt`/`no-harm.stdout`, and both proceeded. Consequence is bounded by R4
(same directon: receipts are appended to / overwritten in place).

---

## Residual risk

* **The blocking residuals are structural, not typos.** The gate's content arm asks one question
  ("does a line with the phrase exist?") and its provenance arm asks another ("is the file
  committed after the freeze?"). Neither touches the two facts the receipts were designed to
  carry: *which revision* they scored, and *whether the phase run succeeded*. R1+R3 together mean
  the gate cannot distinguish a genuine phase-B pass from a round-54 file copied in, and R2 means
  it cannot distinguish a pass from a failure.
* A green `DECIDING_RUN_EXIT=0` therefore certifies the counters' *measurement at REV* (which the
  deciding run does itself) and not their *falsifiability at REV*. R54.1 is the exact defect that
  produced a false record last round; it is now routed, described and fixed in `controls.sh`
  discipline, and unverifiable by the only consumer of the receipts (sweep below).
* Who reads the receipts: `deciding-run.sh` is the **only** consumer of round-55's control
  receipts; `c1/measure.py` reads round-*54*'s. Nothing downstream would notice a stale file.
  ```
  $ git grep -n -E 'control/controls-|CONTROLS_[AB]' 9cf0146 -- .ufo/evidence/round-55/
  .ufo/evidence/round-55/c1/measure.py:198:  … round-54/control/controls-b.stdout …
  .ufo/evidence/round-55/controls.sh:114:  echo "CONTROLS_A: $pass/$((pass+fail)) as pre-registered"
  .ufo/evidence/round-55/controls.sh:142:  echo "CONTROLS_B: $pass/$((pass+fail)) as pre-registered"
  .ufo/evidence/round-55/deciding-run.sh:46: CONTROLS="$E/control/controls-a.stdout …"
  .ufo/evidence/round-55/deciding-run.sh:54: grep -q '^CONTROLS_A: [0-9]*/[0-9]* as pre-registered' …
  .ufo/evidence/round-55/deciding-run.sh:55: grep -q '^CONTROLS_B: [0-9]*/[0-9]* as pre-registered' …
  ```

## Verification gaps

* I did not run `controls.sh a|b` (two full counter sweeps, ~10 min each, and they would write
  outside my scope). The receipts I used are either round-54's real committed bytes or lines
  shaped exactly as `controls.sh` prints them (`score()` → counter verdict line; `check()` →
  `CTL_MISMATCH`; the two `echo "CONTROLS_x: $pass/$((pass+fail)) as pre-registered"`), and the
  one real round-55 phase-A line on disk (`CTL CTL_0_c1 C1_R55: rev=0a2010acd1e9 …`, 4-line file,
  no tally) confirms the shape. Forgery beyond that shape was not attempted — the findings above
  need none.
* I did not exercise `controls.sh`'s own arms; whether phase B really clones REV is its own
  question (wave 1's R54.1 analysis seat), not mine. R1 is precisely the statement that the gate
  cannot check the answer.
* `REV`/`FREEZE` argument handling (relative paths, `^` suffixes, `rev-parse` re-resolution) and
  `OUT` outside the lane were not attacked.
* The coldread-floor RED and the pre-amendment-8 C2 total are reported because they were in my
  full run's output and bound the "is the decision green today" question; both belong to other
  seats. I did not audit them.

## Artifacts opened

`.ufo/evidence/round-55/deciding-run.sh` @ `e2979f2` · `.ufo/evidence/round-55/controls.sh` @
`e2979f2` · `.ufo/evidence/round-55/no-harm.sh` @ `e2979f2` · `.ufo/evidence/round-55/c1/measure.py`
@ `e2979f2` · `.ufo/evidence/round-55/c2/measure.py` @ `e2979f2` (total line + mode lists) ·
`.ufo/evidence/round-55/freeze.json` (freeze and working-tree copy) ·
`.ufo/evidence/round-54/control/controls-{a,b}.{stdout,exit}` @ C0 ·
`.ufo/evidence/round-54/contract.json:74` @ C0 · `.ufo/evidence/round-55/control/controls-a.stdout`
(lane worktree, untracked) · `.gitignore` · `.ufo/waves/round-55/w2/swarm-registry.json`
(seat roster) · `.ufo/evidence/round-21/coldread/measure.py` (invoked read-only).

Fixtures and receipts: `.ufo/waves/round-55/w2/T55W2RevGateResidual-receipts/`
(`build-fixture.sh`, `probe.sh`, `second-invocation.sh`; outputs are re-derivable by running them
with `S=/fast/scratch/hyaku/tameshi-r55/T55W2RevGateResidual`). The captured output of this seat's
runs is persisted under `…-receipts/runs/`: `full-stale-rev.stdout` (the complete 9m41s deciding
run), `deciding-run.exit`, `frozen.stdout`, `no-harm.tail`, `c1.verdict`, `c2.verdict`,
`coldread-precheck.tail`, one `<fixture>.run.stdout` per gate probe, the six second-invocation
outputs, and each fixture's receipt bytes under `runs/fixture-*/`.

Scratch: `S=/fast/scratch/hyaku/tameshi-r55/T55W2RevGateResidual`, removed at the end
(`rm -rf -- "$S"`; never the shared parent). Each deciding run got
its **own** `HYAKU_SCRATCH` (`$S/hyaku-<fixture>`), because the script does `rm -rf "$SCR"` on
`${HYAKU_SCRATCH}/tameshi-r55/deciding` at line 59 — the wave-1 collision hazard. `/tmp` was used
only for a six-line grep matrix, removed after use. **No tool was installed or upgraded.**

No lane production file, frozen file or wave spec was modified: the only files written are under
`.ufo/waves/round-55/w2/`.

Report: .ufo/waves/round-55/w2/T55W2RevGateResidual.md
