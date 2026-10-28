# T56W1MutCounterArms — mutation probes on the frozen C1 counter (round 56, wave 1)

Seat: `T56W1MutCounterArms` (L1 `TameshiR56`). Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`. Freeze `c3e2ca9f020776b3d66c7af854fb82c834674fcf`.
Instrument under test, **never edited**:
`.ufo/evidence/round-56/c1/measure.py`, sha256 `048122cf1c7c65d283366837f155925a03a58ecc2eab70e7085b1796bfccb772`
(= blob at the freeze commit = the worktree copy; `instrument-provenance.txt`).
Sibling input `.ufo/evidence/round-56/c1/lost-headings-at-base.json`, sha256
`dcfc9f800b8bc7b25851d80ec384b8e8781ead6a5f8adf9f0a5340479282fd4a` (same provenance).

Machine-readable result: `.ufo/waves/round-56/w1/T56W1MutCounterArms.json`.
Receipts: `.ufo/waves/round-56/w1/T56W1MutCounterArms-receipts/` (28 runs, 8 diffs, provenance files).

## Headline

* **6/6 arms live and jointly satisfiable.** A scratch fixture `G` (`469127008ea3`) makes the frozen
  counter read `total=0 C1_R56_PASS=true` — so no arm is structurally stuck red and the counter can
  certify a lane.
* **8/8 single-edit mutants killed by an external fixture battery; 0/8 detectable from inside the
  lane.** Each of the eight edits removes one detection and the counter's own verdict notices
  nothing: at the base revision seven of the eight runs are byte-identical to the pristine run
  (only M4 moves `total` 5 → 4). The counter has no `--selftest` and no arm-isolating mode.
* **Arm 1 is detection-redundant with arm 2** (proof + fixtures below). The claim's `lost=0`
  precheck clause is never enforced alone.

## Verdict criterion (stated before applying it)

The frozen counter judges the *lane*; it cannot judge itself. So the oracle is an external battery:
a scratch clone of the lane plus synthetic commits that (a) make the counter green (`G`) and
(b) break exactly one arm per probe. A run is a **refusal assertion** — the frozen bytes refuse the
defective probe; the mutant is measured against the same input.

* **KILLED** — at least one input distinguishes the mutated bytes from the frozen bytes (the refusal
  the frozen bytes satisfy fails on the mutant). This is the fleet's `tools/mutate-and-run.sh`
  convention ("if this exact edit were present, would the run go red?") with the battery as the run.
* **SURVIVED** — no input in the battery distinguishes the mutant (equivalent mutant).
* **INCONCLUSIVE** — no discriminating input could be built, or the run did not complete.
* `self_detected` (reported separately for every mutant) — whether the counter's own verdict on the
  lane changes. **False for all eight.** "KILLED" here must not be read as "the counter is safe
  against this edit": it means the battery caught it.

## Why `tools/mutate-and-run.sh` was not used as the driver

Its suite contract requires a **green control run on the pristine artifact** ("a red control exits 2
(kills could not be attributed)"). The pristine counter is red on every defective probe *by
construction* — that is what an arm does. Demonstrated, not asserted:

```
$ bash tools/mutate-and-run.sh --target $S/pristine/measure.py --defects $S/misfit.spec \
    --suite 'cp ...; python3 "$MUTANT" --lane $S/lane --rev 981c5e8b20a2 --work "$(mktemp -d)"' \
    --label c1-r56-misfit --workdir $S/mutrun
MUTATE_TOOL: .../tools/mutate-and-run.sh sha256=977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda
MUTATE_TARGET: .../pristine/measure.py sha256=048122cf1c7c65d283366837f155925a03a58ecc2eab70e7085b1796bfccb772 bytes=13278
MUTATE_SPEC: .../misfit.spec defects=1
CONTROL: RED (exit=1 duration-ms=87499 pristine-sha256=048122cf...)
  | C1_R56: rev=981c5e8b20a2 ... total=5 C1_R56_PASS=false
MUTATE: SETUP (control run on the pristine copy is red (exit=1); cannot attribute kills; ...)
exit 2
```

A second misfit: the tool copies a single file per mutant, but the counter loads
`lost-headings-at-base.json` from its own directory, so a bare copy is not runnable (the suite above
has to re-supply it). The documented driver `drive.py` therefore runs each variant as a full CLI
invocation and records stdout/exit/meta per run (`receipts/runs/`).

## Fixtures (scratch clone only — no lane write)

Clone: `git clone --shared --no-hardlinks <lane> $S/lane`, then `git -C $S/lane checkout --detach 981c5e8b20a2`.
Every commit below is in the clone; `git -C $S/lane rev-parse --show-toplevel` prints the clone
before each commit (`build_fixtures.py`, `build_w.py`, `build_s2.py`).

| id | rev | what it carries | pristine verdict |
|---|---|---|---|
| base | `981c5e8b20a2` | the round base, untouched | `total=5 PASS=false` |
| G | `469127008ea3` | 18 re-keyed ledger entries + 18 trace receipts under `rekey-r56-6eb49698d64d` + 18 reader reports + one calibration row stating 8 at a commit that reads 8 | `total=0 PASS=true` |
| U | `8acc29bcecc2` | G + one bound entry pinning `LOG.md` | `unstable=1 total=1` |
| R | `a400275d3ac5` | G + one reader report with a wrong `section_sha256` | `readers=17/18 total=1` |
| T | `6c62b001f7c0` | G + a calibration row stating **6** at `981c5e8b20a2` (which really reads 6) while REV reads 8 | `restate=6 monitor=8/64 total=1` |
| S2 | `b390a6378549` | G + box 3 unmarked (score 6, page still 64/64) + a row stating 6 at a 6-reading commit | `monitor=6/64 total=1` |
| P | `e1edea116a2c` | G + one extra credited section (page 65/65, score 8) | `credited=65 monitor=8/65 total=1` |
| C | `5aef3c7881b8` | G + extra section credited, one floor heading uncredited (page 65, 64 credited, `lost=1`) | `credited=64 lost=1 total=4` |
| W | `4b7eeedcb742` | G + all 18 re-keyed entries bound to `read_rev=981c5e8b…` instead of `c0` | `rekeyed=0/18 monitor=8/64 total=1` |
| A | `75c3f5216e2b` | G + a row stating 8 at side-branch commit `beaf602e8952` (reads 8, not an ancestor) | `restate=8 total=1` |
| S1 | `45d39e3aa9b8` | **superseded** first score probe (see Mistakes) | `credited=45 rekeyed=0/18 total=3` |

`c0 = 6eb49698d64d373d4e85fed1422fdea8e328096b`; re-key dir
`.ufo/evidence/round-21/coldread/rekey-r56-6eb49698d64d`.

Green control, verbatim:

```
$ python3 $S/pristine/measure.py --lane $S/lane --rev 469127008ea3955f720e525740d6cb8a9136b48b --work <empty> --explain
EXPLAIN arm1-precheck exit=0 COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=469127008ea3 cand_credited=64 lost=0 ok
EXPLAIN arm2-monitor covered=64 score=8 box3=True
EXPLAIN arm6-restate row_score=8 row_commit=384a153f642d score_at_row=8 evidence='fixture row: the round-21 cold-read monitor reads 8 at the n' round='56 (fixture)'
C1_R56: rev=469127008ea3 c0=6eb49698d64d credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true
```

Base control (re-derived, not copied), matching `.ufo/evidence/round-56/before/c1.stdout`:

```
$ python3 $S/pristine/measure.py --lane $S/lane --rev 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 --work <empty> --explain
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=981c5e8b20a2 cand_credited=46 lost=18 RED
EXPLAIN arm2-monitor covered=46 score=6 box3=False
EXPLAIN arm6-restate row_score=8 row_commit=d33053f7552d score_at_row=6 evidence='round-21 cold-read monitor `calibration_restraint_score`; 8 ' round='53'
C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false
```

## Mutants (one exact edit each; uniqueness asserted before any run)

Construction asserts `frozen_bytes.count(old) == 1` and `new != old` for every mutant
(`mutants.json`, `diff-<id>.txt`). Run form for every cell:
`python3 <counter> --lane $S/lane --rev <rev> --work <fresh empty dir> --explain`.

| # | edit (old → new) | base: pristine → mutant | probe: pristine → mutant | verdict | self-detected |
|---|---|---|---|---|---|
| M1 | `precheck_ok = run.returncode == 0 and m is not None and 'lost=0 ok' in last` → `… and True` | `total=5` → `total=5` (identical) | C `5aef3c7881b8`: `total=4` → `total=3` | **KILLED** | no |
| M2 | `monitor_ok = covered == 64 …` → `covered >= 46 …` | `total=5` → `total=5` | P `e1edea116a2c`: `total=1 PASS=false` → `total=0 PASS=true` | **KILLED** | no |
| M3 | `… score == 8 …` → `score >= 6 …` | `total=5` → `total=5` | S2 `b390a6378549`: `total=1 PASS=false` → `total=0 PASS=true` | **KILLED** | no |
| M4 | `if rekeyed != len(frozen):` → `if rekeyed < 0:` | `total=5` → `total=4` | W `4b7eeedcb742`: `total=1 PASS=false` → `total=0 PASS=true` | **KILLED** | no |
| M5 | `if d.get('cand') == c0 and d.get('section_sha256') == sec['sha256']:` → `… and True:` | `total=5` → `total=5` | R `a400275d3ac5`: `readers=17/18 total=1` → `readers=18/18 total=0 PASS=true` | **KILLED** | no |
| M6 | `UNSTABLE_INPUTS = ('LOG.md', 'SCORECARD.md')` → `()` | `total=5` → `total=5` | U `8acc29bcecc2`: `unstable=1 total=1` → `unstable=0 total=0 PASS=true` | **KILLED** | no |
| M7 | `restate_ok = (row_score == score and …` → `restate_ok = (True and …` | `total=5` → `total=5` | T `6c62b001f7c0`: `restate=6 monitor=8/64 total=1` → `total=0 PASS=true` | **KILLED** | no |
| M8 | `if row_commit and is_ancestor(lane, row_commit, rev):` → `if row_commit and True:` | `total=5` → `total=5` | A `75c3f5216e2b`: `restate=8 total=1` (`score_at_row=None`) → `total=0 PASS=true` | **KILLED** | no |

Kill rate: **8/8 by the battery, 0/8 by the counter.** No mutant is equivalent: every edit changes
behaviour on a constructible input.

### What each edit costs, exactly

* **M1** — the `lost=0 ok` clause is reachable: at C the frozen precheck exits **0** with
  `cand_credited=64 lost=1 ok` (a 65-section page, 64 credited, one floor heading lost). The frozen
  counter fires arm 1; the mutant does not (`total` 4 → 3). C is the only probe that does not flip
  PASS, and it cannot: any exit-0-with-`lost>0` state forces `sections_total > 64`, which makes
  `box3_full_page` false, `score` 6, and therefore also fires arm 2.
* **M2** — the literal `64` is the sole pin on page cardinality. At P the page is 65/65, fully
  credited, `monitor=8/65`: the frozen counter refuses, the mutant passes.
* **M3** — `score == 8` is the sole pin on box 3 being marked **and** ledger-linked. At S2 the page
  is 64/64 with `box3=True` but `score=6`: frozen refuses, mutant passes. (This is the R55.3 shape
  read from the other side: a 6 that is real.)
* **M4** — arm 3's binding is independent of coverage. At W coverage is 64/64, `monitor=8/64`, but
  all 18 re-keyed entries name `read_rev=981c5e8b…` instead of `c0`, so `rekeyed=0/18`. Frozen
  refuses; mutant passes. At the base revision the same edit already drops `total` 5 → 4 with no
  re-key directory at all.
* **M5** — arm 4's per-report sha is the only report/bytes binding. At R one report carries 64 zeros
  as `section_sha256`: frozen `readers=17/18`, mutant credits it (`readers=18/18`).
* **M6** — arm 5 is the only check on the round-53/55 loss mechanism. At U one entry bound under the
  re-key pins `LOG.md`: frozen `unstable=1`, mutant `unstable=0`.
* **M7** — the R55.3 class exactly. At T the standing row asserts 6 at a commit that really reads 6
  while REV reads 8: frozen `restate=6 monitor=8/64` refuses; the mutant passes. The
  `same_at_row == row_score` conjunct cannot catch this — the stale row satisfies it by
  construction.
* **M8** — the R55.5 class. At A the row names side-branch commit `beaf602e8952` (reads 8, not an
  ancestor): frozen `score_at_row=None`, mutant passes.

## Findings about the counter (report defects; the instrument stays frozen)

* **F1 — all arms reachable.** `G` reads `total=0 PASS=true`; the six arms are simultaneously
  satisfiable at one revision.
* **F2 — the counter cannot see its own weakening.** 8/8 mutants are invisible to the counter's
  verdict; 7/8 are byte-identical at the base revision. There is no `--selftest`, no `--only-arm`,
  and no fixture mode. Any wave-2 argument of the form "the counter passes, therefore the claim
  holds" inherits the risk that one of these edits is present in the frozen bytes; the bytes are
  pinned by sha256, which is the only defence.
* **F3 — arm 1 is detection-redundant with arm 2.** Proof: arm 2 green requires `covered == 64` and
  `score == 8`; `score == 8` requires `box3_points`, which requires `box3_full_page`, i.e.
  `covered == sections_total`; with `covered == 64` that forces `sections_total == 64`, so
  `lost == 0` and arm 1 is green. Conversely arm 1 red via the exit clause means `cc < 64`, i.e.
  `covered < 64`, so arm 2 fires; arm 1 red via the `lost=0 ok` clause requires `cc >= 64` with a
  differing set, which forces `sections_total > 64`, `box3_full_page` false, `score` 6, so arm 2
  fires. **Arm 1 never fires alone** — fixtures base, C and G show the two arms firing and passing
  together. The C1 contract's "precheck reads `lost=0`" is therefore enforced only jointly with
  arm 2's literal 64.
* **F4 — the other five arms each uniquely pin a named property**, with the isolating fixture:
  page cardinality (P), box-3 mark/link (S2), re-key binding `read_rev == c0` (W), report/bytes
  binding (R), unstable-input exclusion (U), and arm 6's two independent conjuncts — the monitor's
  own score at REV (T, R55.3) and the ancestry of the named commit (A, R55.5).
* **F5 — a weakened arm can vanish from `total` without any field moving.** M1 at base and at C
  prints a byte-identical `arm1-precheck` EXPLAIN line in both pristine and mutant runs; only
  `total` moves. Per-arm state exists only in `--explain`, and `--explain` prints raw values, not
  pass/fail.
* **F6 — recommendation for the C1 record (no instrument edit).** State the arm-1/arm-2 coupling
  rather than implying six independent checks; the wave-2 record should not claim that the
  precheck clause is separately load-bearing.

## Limits of this evidence

* **Fixture level only.** `G` and every probe are synthetic commits in a scratch clone: 18 re-keyed
  ledger entries, 18 trace receipts, 18 reader reports, fixture calibration rows, and (S2 only) 34
  re-credited base entries. **Nothing here says the lane at C0 reads 64/64 score 8.** That is wave 2.
* The probes isolate one arm each; this is not a property test. Not exercised: missing blobs,
  unresolvable revisions, invalid ledger JSON, `ls-tree` failures, pages with fewer than 64
  sections, and simultaneous multi-arm defects beyond the base revision.
* The 46 base-credited entries are the lane's real entries; everything else added is synthetic.
* Fixture entries pin `corpus/QUALITY.md`. A real C0 re-key that pins `SHONEN.md` will drift on any
  later `SHONEN.md` edit — exactly what the first score probe hit (Mistakes S1). Wave 2's re-key
  should prefer inputs that no later round commit touches.
* **The fixture revisions are scratch-local.** They live in
  `/fast/scratch/hyaku/tameshi-r56/T56W1MutCounterArms/lane`, are not lane objects, and the scratch
  is removed when this seat closes. The receipts keep every run's stdout/exit/meta and the three
  builder scripts; rebuilding re-derives fixtures with the same properties but **new commit hashes**
  (commit ids depend on timestamps), so a later reader re-derives the properties, not the exact
  revision ids.

## Mistakes (calibration)

1. **S1 (`45d39e3aa9b8`), superseded.** The first score probe edited `SHONEN.md` while the 18
   re-key entries pinned `SHONEN.md` as an input. All 18 drifted: `rekeyed=0/18 credited=45
   monitor=6/45 total=3`, and M3 was **undiscriminated** (mutant `total=3`, identical). Rebuilt as
   S2 (`b390a6378549`) with every fixture entry pinned to `corpus/QUALITY.md` and the 34 base
   entries that pinned `SHONEN.md` re-credited: `credited=64 rekeyed=18/18 total=1`, M3 flips PASS.
   Both receipts kept (`S_*` = superseded, `S2_*` = probe).
2. **Prediction miss P1.** Before measuring I expected M1 to be an equivalent mutant (clause
   redundant with `exit==0` on the lane's 64-section page). Fixture C falsified that: exit 0 with
   `lost=1` is reachable on a 65-section page. Kept as a recorded miss; the *redundancy with arm 2*
   survives as F3, which is a different statement.

## Discipline / restoration evidence

* No lane write: the frozen counter's worktree sha256 equals its blob at the freeze
  (`048122cf…`), same for `lost-headings-at-base.json` (`dcfc9f80…`); every mutant lives under
  `$S/mut/<id>/`, every fixture commit under `$S/lane` (clone toplevel asserted before each commit).
* No mutating git command against the lane; the clone is `--shared`, so fixture commits add objects
  only to the clone.
* Scratch: `/fast/scratch/hyaku/tameshi-r56/T56W1MutCounterArms` (drivers, clones, fixtures, runs).
  `/tmp` used only for the counter's own `--work` mirrors when a run needs one, all under scratch.
* Census (`round start`): `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
  from the fleet root → `ok`, exit 0 (`receipts/census.txt`).
* Tool installs: **none** (no pacman, no `uv`, no npm; nothing added to `~/.local/bin`).

## Reproduce

```bash
S=/fast/scratch/hyaku/tameshi-r56/T56W1MutCounterArms
git clone --shared --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/lane"
git -C "$S/lane" checkout --detach 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1
python3 "$S/build_fixtures.py"      # base -> X(c0) -> Y -> G, plus U R T S1 P C A
python3 "$S/build_w.py"             # W: re-key entries bound to a non-c0 read_rev
python3 "$S/build_s2.py"            # S2: 64/64 page, box 3 unmarked
python3 "$S/drive.py" "$S/batch2.json" 6   # pristine + mutant runs per fixture
python3 "$S/drive.py" "$S/batch3.json" 4   # W and S2 probes
python3 "$S/gen_json.py"            # the machine-readable deliverable
```

Receipt index (`receipts/`): `runs/<label>.{out,exit,meta}` (28 runs), `mutants.json`,
`diff-<mutant>.txt` (8), `fixtures.json`, `fixture-provenance.txt`, `instrument-provenance.txt`,
`misfit.spec`, `misfit.out`, `census.txt`, `batch{1,2,3}.json`, `drive.py`,
`build_fixtures.py`, `build_w.py`, `build_s2.py`.
