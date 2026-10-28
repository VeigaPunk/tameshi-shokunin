# T54W2Scribe02 — report draft: § Before → after measurements + the SCORECARD.md round-54 rows

Seat `T54W2Scribe02` (scribe, wave 2). Lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin` (absolute paths throughout).
Item: *"Draft the Before → after measurements section (quote the receipts that exist; the
recorded base C2 line is `total=14` with `usable_ok=6` while the frozen contract's before
text says 13 — quote the receipt and disclose the delta, never reconcile it silently) and
the SCORECARD.md round-54 rows with the exact counting commands."*

Method: I ran the frozen counter bytes (extracted from `HEAD` and sha256-checked against
`.ufo/evidence/round-54/freeze.json`) against the named revisions in a scratch work
directory, then quoted **the receipts that exist** for every number. No lane file was
edited; this file plus the scratch tree is all this seat wrote. No tool was installed or
upgraded (nothing needed).

Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W2Scribe02/` (`HYAKU_SCRATCH=/fast/scratch/hyaku`,
`TMPDIR` inside it; removed at seat exit).

---

## 1. Revision state and what "the frozen bytes" means today

| Role | Commit | Note |
|---|---|---|
| Base | `d33053f7552db4bd290c99a36979760f544c41ad` | round-53 closure tip |
| Original freeze | `441c26bec5e4c1cc31bc2a840f311cb8d1965259` | `freeze.json` with `amendments: []`, **8** hashed files |
| Content commit C0 | `59c38109bf119d0e9d4f878644a82babc937bc1e` | one scratch-root exit class across 7 tools, registry cells, note, S277–S279, SKILL three-arm rule |
| Fix pass C1 | `99c3bc88d704566197783f66b211ee0a830e0330` | 26 wave-1 findings adjudicated and fixed; 6 files, +82/−32 |
| Amendment 1 | `7883e0e5` | C1 counter arm 3 discovers the re-key directory from each traced path's **directory** component |
| Re-freeze (amendment 2) | `19c7558` (11:51) | C2 counter amendment 2; all 11 contract paths hashed; base receipts, phase-A control receipts, `c1/lost-headings-at-c0.json`, binder, wave specs |
| Freeze-digest gate fix | `097985c` (11:52) | `deciding-run.sh` resolves the three inherited counter bodies by repo path; manifest re-hashed |
| HEAD at this seat's runs | `097985c18b9a186c310bd35890b95b733cbb7f5b` | tree dirty at my read: `integrate/binder.py` modified and `integrate/resolutions.json` added **by the L1 while this seat ran** (§2.5), plus the wave paths |

> **The tree moved during this seat.** `binder.py` gained a `resolutions.json` adjudication
> map (`gap-minor` verdicts, `minor_gaps` counted) and `integrate/resolutions.json` appeared
> (9 headings) between my first read and my last. Every number below is pinned to the
> revision named in its row; nothing here is a claim about the uncommitted tree. The C1/C2
> line numbers I cite for `binder.py`/`c1/measure.py` are the ones I read; the constants
> (`WAVE`) had not moved at my last read.

**The instrument bytes this draft measured** (extracted with `git show HEAD:<path>`):

```
63f5f88147b898ee795dc925a04668d473c1fc845e370947307e3ea141a0b77b  c1/measure.py
49280fe55bd9361c284ddb1b9e757fd3ec3267f60eed4ca587e1bfe446b718c8  c2/measure.py
a953d2e87116effc943f56a532b785cae8c8f44a104635083634c05fe0b8bb10  c1/lost-headings-at-base.json
```

each equal to the value in `.ufo/evidence/round-54/freeze.json` (`files` map). So the
readings below ran the frozen instrument, not a working-tree variant.

Two consequences the report must carry, because the round's earlier prose predates them:

- **`freeze.json` at HEAD is no longer the `441c26be` manifest.** `git diff 441c26be HEAD -- .ufo/evidence/round-54/freeze.json`
  shows 8 keys become 10 (the three inherited counters `.ufo/evidence/round-{18,21,48}/...`
  are now hashed too), `amendments: []` becomes two entries, and the C1/C2/contract/
  deciding-run hashes change. The `FREEZE` argument the deciding run must be given is
  therefore `097985c` (or a later commit that touches no frozen path), **not** `441c26be`
  and **not** `7883e0e5`: `deciding-run.sh:63` refuses `FROZEN_UNCHANGED=0` if any frozen
  path differs between `FREEZE` and `REV`, and `deciding-run.sh` and `freeze.json`
  themselves last changed at `097985c`.
- **Every C2 receipt written before 11:51 was produced by the pre-amendment counter**
  (`c2/measure.py` sha `b4684a3f555e8cbf…`, which took the *usable* arm's rc from the
  `strace -f` run): the control harness at 11:23, the base receipts at ~11:29/11:32, the
  wave-1 replays at 11:40. Amendment 2 (`49280fe5…`, landed 11:51) takes the rc from a
  plain run and uses `strace` only for the `/tmp` mkdir census (`c2/measure.py:130-146`).
- **The committed `before/c2.stdout` is not the file the wave-1 seats measured.** The
  wave-1 report records it as "`before/c2.stdout` (1355 B) … mtime 11:29 / 11:32"
  (`T54W1ScribeMeasure.md:273`) printing `usable_ok=6 … total=14`; the blob committed at
  `19c7558` is **1307 B / 8 lines** and prints `usable_ok=7 … total=13`
  (`git cat-file -s HEAD:.ufo/evidence/round-54/before/c2.stdout` → `1307`; `… | wc -l` →
  `8`). The 48-byte difference is the `EXPLAIN usable registry-check rc=1 tmp_mkdirs=0`
  line the 14 sample carries. So the base receipt was regenerated (on the passing side of
  the arm) before it was committed, and the `total=14` reading survives only in the
  untracked wave-1 receipts. This is why §2.3 quotes two paths for two numbers.

---

## 2. § Before → after measurements (paste-ready)

### 2.1 Counting commands (exact)

Run from `/home/vgpnk/Projects/shokunin/tameshi-shokunin` with an **empty** `--work`
directory under scratch (both counters refuse a non-empty one — `c1/measure.py:106-108`,
`c2/measure.py:96-98`):

```bash
# C1 — calibration
python3 .ufo/evidence/round-54/c1/measure.py \
        --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
        --rev <REV> --work <EMPTY_DIR> --explain

# C2 — operability
python3 .ufo/evidence/round-54/c2/measure.py \
        --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
        --rev <REV> --work <EMPTY_DIR> --explain

# the frozen round-48 precheck, when the per-section LOST lines matter
# (the C1 counter keeps only the last line; FLOOR = ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4)
bash .ufo/evidence/round-48/quality/coldread-precheck.sh \
     /home/vgpnk/Projects/shokunin/tameshi-shokunin <FLOOR> <REV>

# the deciding run (the only path that produces the "after" receipts)
bash .ufo/evidence/round-54/deciding-run.sh \
     /home/vgpnk/Projects/shokunin/tameshi-shokunin <REV> <FREEZE> .ufo/evidence/round-54/after
```

`<EMPTY_DIR>` is a fresh directory; `--explain` prints one `EXPLAIN …` line per arm.

### 2.2 C1 — calibration (the cold-read floor)

**Base `d33053f7`** — `.ufo/evidence/round-54/before/c1.stdout` (committed at HEAD) and
`CTL_0_c1` in `.ufo/evidence/round-54/control/controls-a.stdout`, identical:

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=d33053f7552d cand_credited=57 lost=7 RED
EXPLAIN arm2-monitor exit=0 covered=57 score=6
EXPLAIN arm3-rekey dirs=[] c0=None
EXPLAIN arm4-readers 0/7
C1_R54: rev=d33053f7552d c0=none credited=57 lost=7 rekeyed=0/7 readers=0/7 monitor=6/57 unstable=0 total=4 C1_R54_PASS=false
```

**C0 `59c38109`** — no receipt is committed at C0; the line on record is a wave-1 seat run,
`.ufo/waves/round-54/w1/T54W1ScribeScorecard-receipts/c1-at-c0.explain.txt` (untracked):

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=59c38109bf11 cand_credited=41 lost=23 RED
C1_R54: rev=59c38109bf11 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
```

**C1 `99c3bc88`** — this seat, fresh run of the frozen bytes. No C1-counter receipt exists at
`99c3bc88`: the wave-1 replay stopped at C0 (`…/T54W1ExecFreeze-receipts/c1-frozen-bytes-at-c0.out`,
which prints exactly the C0 line above), and the wave-1 `T54W1ExecC1Counter` receipts are
instrument scripts, not runs. So the C1-verdict receipt shape looks like this:

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=99c3bc88d704 cand_credited=41 lost=23 RED
EXPLAIN arm2-monitor exit=0 covered=41 score=6
EXPLAIN arm3-rekey dirs=[] c0=None
EXPLAIN arm4-readers 0/7
C1_R54: rev=99c3bc88d704 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
```

The fix pass does **not** move the floor: `credited` is 41 at C0 and 41 at C1, because the
23 losses are input-drift/no-ledger-entry, not prose. The floor moves only when the
`rekey-r54-<c0>` entries exist — which is what the deciding run measures.

| Field | Base `d33053f7` | C0 `59c38109` | C1 `99c3bc88` (pre-bind) | Target at the deciding revision |
|---|---|---|---|---|
| `credited` (arm 1, frozen round-48 precheck) | 57 | 41 | 41 | 64 (`cand_credited=64 lost=0 ok`) |
| `lost` | 7 | 23 | 23 | 0 |
| `monitor` (arm 2, unchanged round-21 selector) | `covered=57 score=6` | `covered=41 score=6` | `covered=41 score=6` | `covered=64 score=8` |
| `rekeyed` (arm 3; the **seven** base-lost headings) | `0/7` | `0/7` | `0/7` | `7/7` |
| `readers` (arm 4) | `0/7` | `0/7` | `0/7` | `7/7` |
| `unstable` (arm 5) | 0 | 0 | 0 | 0 |
| `total` | 4 | 4 | 4 | 0 |
| `C1_R54_PASS` | `false` | `false` | `false` | `true` |

Frozen field set for arm 3 is `.ufo/evidence/round-54/c1/lost-headings-at-base.json`
(7 headings); the binder's re-key set is that union with
`c1/lost-headings-at-c0.json`, i.e. **23** headings (`binder.py:46-50`). Arm 3 scores only
the frozen seven; reaching `credited=64` needs all 23 bound.

Per-section precheck output at C1 (frozen precheck, `floor → 99c3bc88`; 23 `LOST` lines;
the precheck's own exit code was not captured separately in this run — it was piped to
`tail`, and the C1 counter's independent arm 1 records `exit=1` for the same comparison):
nine lines carry a non-empty `drifted=` set, the other fourteen print `drifted=` empty (the
`no-ledger-entry` class):

```
LOST ## Context gate classification and explicit exit classes — round 15 | drifted=corpus/SOURCES.md,tools/bash-witness-study.py,tools/context-capture.py,tools/evidence-disposition.py,tools/mutate-and-run.sh,tools/pin-disposition.py,tools/registry.json,tools/trace-inputs.py
LOST ## The leg ledger — replay, receipt, and how it is read (round 7, measured) | drifted=corpus/SOURCES.md
LOST ## The operator's runbook and the six-leg regression (round 10, measured) | drifted=tools/registry.json
LOST ### Gate/probe registry | drifted=tools/bash-witness-study.py
LOST ### Round-13 gate/probe registry | drifted=corpus/SOURCES.md,tools/bash-witness-study.py,tools/pin-disposition.py
LOST ### Round-14 historical registry — superseded by round 15 | drifted=tools/bash-witness-study.py,tools/evidence-disposition.py,tools/trace-inputs.py
LOST ### Round-21 gate/probe registry — finite environment differential | drifted=.ufo/evidence/round-15/verify.py,corpus/QUALITY.md,corpus/SOURCES.md,tools/env-diff.py,tools/registry-check.py,tools/registry.json
LOST ### The tick and the pin read | drifted=tools/pin-disposition.py
LOST ### Triggers T1–T3 and the re-pin rule | drifted=corpus/QUALITY.md,corpus/SOURCES.md,corpus/knowledge/service-limits.md,tools/bash-witness-study.py,tools/evidence-disposition.py,tools/pin-disposition.py,tools/registry-check.py,tools/registry.json
COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=99c3bc88d704 cand_credited=41 lost=23 RED
```

(nine lines shown of twenty-three; the other fourteen are `LOST <heading> | drifted=` with
an empty set. Full output is reproduced in §4's provenance row and was captured live, not
retyped from another seat.)

### 2.3 C2 — operability (the scratch-root exit class)

**The frozen contract's before text** (`.ufo/evidence/round-54/contract.json`, claim C2,
`before`):

> unusable_exit2=3 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false (measured at d33053f7, .ufo/evidence/round-54/before/c2.stdout)

That string is exactly `CTL_0_c2` in `.ufo/evidence/round-54/control/controls-a.stdout`:

```
CTL CTL_0_c2 C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false
```

and exactly the last line of the committed `.ufo/evidence/round-54/before/c2.stdout`:

```
C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false
```

**The recorded base line at `total=14`** — a faithful re-run of the same frozen bytes at the
same revision, one hour later, in
`.ufo/waves/round-54/w1/T54W1ExecFreeze-receipts/c2-frozen-bytes-at-base.out` (untracked;
1355 B) and again in
`.ufo/waves/round-54/w1/T54W1ScribeScorecard-receipts/c2-at-base.explain.txt`:

```
EXPLAIN usable registry-check rc=1 tmp_mkdirs=0
C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=6 tmp_mkdirs=0 docs=0 note=0 sources=0 total=14 C2_R54_PASS=false
```

**The delta, disclosed and not reconciled.** The two lines differ in exactly one arm —
`usable_ok` 7 versus 6 — and `total` follows arithmetically
(`c2/measure.py:181-185`: every arm contributes `7 − count`, plus 1 each when the note or
the sourced claim is absent):

```
usable_ok=7 → (7−3)+(7−7)+(7−7)+(7−7)+(7−0)+1+1 = 4+0+0+0+7+1+1 = 13
usable_ok=6 → (7−3)+(7−7)+(7−7)+(7−6)+(7−0)+1+1 = 4+0+0+1+7+1+1 = 14
```

Both readings are of the **pre-amendment** counter (`c2/measure.py` `b4684a3f…`), whose
usable arm took the rc from the `strace -f` run; under that wrapper `registry-check`'s own
two `timeout`-kill cases exceed their `< 3.5 s` budget on a loaded host, so the arm is
load-sensitive. The contract's `total=13` is the quiet-host sample (the control harness ran
at 11:23, before the 76-seat wave loaded the host); the `total=14` is a wave-1 sample at
11:40. **The report must quote both, and must not present either as "the" base line.**

**The counter that will actually decide is `49280fe5…` (amendment 2).** A C2 receipt **does**
exist at C1, from wave 1, but of the pre-amendment bytes
(`.ufo/waves/round-54/w1/T54W1ExecFreeze-receipts/c2-frozen-bytes-at-head-99c3bc8.out`):

```
EXPLAIN usable registry-check rc=1 tmp_mkdirs=0
C2_R54: rev=99c3bc88d704 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=6 tmp_mkdirs=0 docs=7 note=1 sources=3 total=1 C2_R54_PASS=false
```

i.e. the whole C1 verdict turned on `usable_ok` 6 rather than 7. This seat then ran the
amended bytes twice; they do not reproduce `14` at base and they do not reproduce the `1`
at C1:

Base `d33053f7` (fresh, this seat):

```
C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false
```

C1 `99c3bc88` (fresh, this seat; **excerpt** — the block below keeps 4 of the 7
`EXPLAIN unusable` lines, one per distinct wording; `registry-check`, `context-capture` and
`repeat-control` print the same class and `rc=2`):

```
EXPLAIN unusable env-diff rc=2 line='ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory:'
EXPLAIN unusable bash-witness-study rc=2 line='WITNESS_STUDY: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory:'
EXPLAIN unusable evidence-disposition rc=2 line='evidence-disposition.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable '
EXPLAIN unusable pin-disposition rc=2 line='pin-disposition.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable direc'
C2_R54: rev=99c3bc88d704 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=7 note=1 sources=3 total=0 C2_R54_PASS=true
```

**This is a seat run, not a deciding receipt.** It says: with the amended bytes, the fix
commit already satisfies every arm, and amendment 2 removed the flaky reading — the C2
`total` no longer depends on host load. It does not substitute for
`.ufo/evidence/round-54/after/c2.stdout`.

| Field | Base, contract/control (pre-amendment) | Base, wave-1 re-run (pre-amendment) | Base, amended bytes (this seat) | C0, wave 1 (pre-amendment) | C1, wave 1 (pre-amendment) | C1, amended bytes (this seat) | Target at the deciding revision |
|---|---|---|---|---|---|---|---|
| `unusable_exit2` | 3/7 | 3/7 | 3/7 | 7/7 | 7/7 | 7/7 | 7/7 |
| `naming` | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 |
| `empty_ok` | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 |
| `usable_ok` | 7/7 | **6/7** | 7/7 | 6/7 | 6/7 | 7/7 | 7/7 |
| `tmp_mkdirs` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `docs` | 0/7 | 0/7 | 0/7 | 7/7 | 7/7 | 7/7 | 7/7 |
| `note` | 0 | 0 | 0 | 1 | 1 | 1 | 1 |
| `sources` | 0 | 0 | 0 | 3 | 3 | 3 | ≥1 |
| `total` | **13** | **14** | 13 | 1 | 1 | **0** | 0 |
| `C2_R54_PASS` | `false` | `false` | `false` | `false` | `false` | `true` | `true` |

The C0 and C1 (wave-1) columns are seat runs
(`.ufo/waves/round-54/w1/T54W1ScribeScorecard-receipts/c2-at-c0.txt` and
`.ufo/waves/round-54/w1/T54W1ExecFreeze-receipts/c2-frozen-bytes-at-head-99c3bc8.out`); C0
has no committed counter receipt either. Read the `total` row left to right: **13 → 14 →
13 → 1 → 1 → 0**, and note that the last step is the only one that changes an arm other
than `usable_ok`.

### 2.4 Axes restated at C1, and the census

| Axis | Command (exact) | Output at C1 `99c3bc88` |
|---|---|---|
| depth 10 (ceiling) | `git show <REV>:tools/mutate-and-run.sh \| python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js\|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'` | `recorded_cases=10 depth_score=10` |
| calibration 8 (ceiling) | `python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev <REV>` (the C1 counter's arm 2 runs the same bytes from the lane mirror) | `score=6 covered=41` — the cold-read veto, not a graded drop; 8 returns only at `covered=64` |
| freshness 9 | `python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev <REV> \| tail -1` | `self_pin=1 population=74 entries=73 verified=73 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=2 fresh=71 score=9 target=50 rev=99c3bc88d704… C1_R45_PASS=true` (`(10*71)//74 = 9`) |
| census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | `exit=0` (duplicate-URL warnings only) |
| source rows | `git show <REV>:corpus/SOURCES.md \| grep -cE '^ {0,3}\| S[0-9]{3,} \|'` | `139` (last id `S279`) |

### 2.5 The "after" column: nothing measured yet, and exactly what has to exist first

`.ufo/evidence/round-54/after/` **does not exist** (no deciding invocation has run). Passing
counter lines *do* exist in the lane — this seat found 27 — but none is a deciding receipt,
and two classes of them would be actively misleading if quoted:

```
$ ls -d .ufo/evidence/round-54/after
ls: cannot access '.ufo/evidence/round-54/after': No such file or directory
$ ls -d .ufo/evidence/round-21/coldread/rekey-r54-*
ls: cannot access '.ufo/evidence/round-21/coldread/rekey-r54-*': No such file or directory
$ grep -rh "^C1_R54: \|^C2_R54: " . | grep -c "PASS=true"
27        # 11:58, this seat's first read
$ grep -rh "^C1_R54: \|^C2_R54: " . | grep -c "PASS=true"
37        # 12:03, as wave-2 seats land — the tally is not stable, only "fixtures exist" is
$ grep -rh "^C1_R54: " . | grep "PASS=true" | sort -u
C1_R54: rev=023cbc7f5a56 c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
C1_R54: rev=10ada0d5bc32 c0=59c38109bf11 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
C1_R54: rev=52227471f8ed c0=59c38109bf11 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
C1_R54: rev=5d5a8b6187e0 c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
C1_R54: rev=783eab7bf24f c0=59c38109bf11 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
C1_R54: rev=9ce447c50971 c0=59c38109bf11 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
C1_R54: rev=c79ef005c098 c0=2f0d695654f1 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
$ for r in 023cbc7f5a56 10ada0d5bc32 52227471f8ed 5d5a8b6187e0 783eab7bf24f 9ce447c50971 c79ef005c098; do printf "%s: " "$r"; git cat-file -e "$r^{commit}" 2>/dev/null && echo lane-commit || echo not-in-lane; done
023cbc7f5a56: not-in-lane
10ada0d5bc32: not-in-lane
52227471f8ed: not-in-lane
5d5a8b6187e0: not-in-lane
783eab7bf24f: not-in-lane
9ce447c50971: not-in-lane
c79ef005c098: not-in-lane
$ git status --porcelain | grep -vc "^?? .ufo/evidence/round-54/after"
5        # 11:58
7        # 12:03 — the L1's integrate/ work landed in between
 M .ufo/evidence/round-54/integrate/binder.py
?? .ufo/evidence/round-54/integrate/resolutions.json
?? .ufo/waves/round-54/w1-run.out
?? .ufo/waves/round-54/w1/
?? .ufo/waves/round-54/w2-run.out
?? .ufo/waves/round-54/w2.ready.dispatched
?? .ufo/waves/round-54/w2/
```

Every passing **C1-verdict** line names a revision that is not a commit in the lane
(`not-in-lane`, i.e. a `git clone --shared` fixture), and two of them are in
`.ufo/waves/round-54/w2/T54W2Sent02-receipts/` — a sentinel's constructed tree. Quoting any
of them as "the after reading" would be exactly the self-deception the sentinel seat exists
to test. The passing **C2** lines name lane revs `59c38109` and `99c3bc88` under the amended
bytes (seat runs, §2.3); they show C2 already verifies at C1 but are still not the deciding
receipt, because the deciding receipt must come from committed bytes through
`deciding-run.sh` with `FROZEN_UNCHANGED=1` and 14/14 no-harm.

So the deciding run as the tree stands today would refuse at `deciding-run.sh:57` with
`DECIDING_REFUSED dirty-tree` (five untracked wave paths at 11:58, seven dirty paths at
12:03 once the L1's `integrate/` work landed), and at `:51` with
`DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-54/control/controls-b.stdout`
(no phase-B receipt exists). The "after" cells stay empty until, in this order: the wave
dirs are committed; `controls-b.*` exists and is committed at `REV` in a commit descending
from `FREEZE`; the 23 re-key entries exist under `rekey-r54-<c0>`; then one invocation of
`deciding-run.sh LANE REV FREEZE after/` writes `c1.stdout`, `c2.stdout`, `no-harm.stdout`,
`frozen.stdout`, `census.stdout`, `clean-tree-{before,after}.txt`, `deciding-run.exit`.

---

## 3. SCORECARD.md round-54 rows (paste-ready, with the exact counting commands)

Everything below is a **draft for the L1**; `SCORECARD.md` is not edited by this seat.

### 3.1 Round header prose (replaces the freeze sentence in the current round-54 header)

> L1 TameshiR54a2, hyaku run 11, attempt 2. Two claims on distinct axes, pre-registered
> with both counters, the controls harness, 14 no-harm monitors and the deciding script in
> `.ufo/evidence/round-54/contract.json`, first frozen at `441c26be` before any seat ran.
> **Two amendments, both disclosed in `freeze.json` and both before the deciding run**:
> amendment 1 (`7883e0e5`) fixes the C1 counter's re-key discovery (directory component,
> not basename), found by the binder dry run before any control was scored; amendment 2
> (`19c7558`) takes the C2 usable arm's rc from a plain run and leaves `strace` to the
> `/tmp` mkdir census, found by the wave-1 attack seats before the deciding run. The
> re-freeze at `19c7558`/`097985c` hashes all 11 contract paths (10 files + the manifest);
> `097985c` is the freeze pointer the deciding run must be given, because `deciding-run.sh`
> and `freeze.json` themselves last changed there and `deciding-run.sh:63` requires every
> frozen path to be byte-identical between `FREEZE` and `REV`. Base `d33053f7`; content
> commit C0 `59c38109`; fix-pass commit C1 `99c3bc88`. Shape: wave 1, 76 seats (band
> 64–128; 23 of them cold reads at C0), then wave 2, 47 seats (band 32–64; 23 cold re-reads
> at C1) = 123 seats. Calibration (8) is the lowest non-retired axis and carries C1.

(The seat count is a fact the L1 should confirm: `spec-w2.json` has **47** items, of which
**23** are `T54W2Read*` cold reads; `spec-w1.json` has 76. Adjust the sentence if the
committed wave registry says otherwise.)

### 3.2 Standing axis table — re-stated at C1 (`99c3bc88`)

| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
|---|---|---|---|---|
| depth | 10 | `git show REV:tools/mutate-and-run.sh \| python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js\|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'` → `recorded_cases=10 depth_score=10` | `99c3bc88` (also 10 at `d33053f7`) | 51 |
| calibration | 8 | `python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev REV` → `calibration_restraint_score`; 8 is the monitor's ceiling and is vetoed to 6 whenever any frozen section is uncredited. At C1: `score=6 covered=41` (this seat, via the C1 counter's arm 2 — `EXPLAIN arm2-monitor exit=0 covered=41 score=6`, which runs the frozen round-21 bytes from a lane mirror); the same command reads `score=6 covered=57` at base and `score=8 covered=64` at `e3729de8` (wave-1 receipt `.ufo/waves/round-54/w1/T54W1ScribeScorecard-receipts/calibration-at-rev.txt`) | `99c3bc88` | 53 |
| freshness | 9 | `python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev REV \| tail -1` → `(10*fresh)//population`, **not** `/73`: the counter divides by `len(population)` and the population is 74 at this revision. At C1: `population=74 fresh=71 → score=9` (`(10*71)//74 = 9`) | `99c3bc88` | 48 (restated) |

### 3.3 Claim rows

| Claim | Axis | Before (base `d33053f7`) | Target | Counting command | Controls (freeze bytes) |
|---|---|---|---|---|---|
| C1 the cold-read floor reads 64/64 credited at the deciding revision, the seven base-lost sections carry a fresh entry under `rekey-r54-<c0>` that credits, a committed reader report pins each section's bytes at `<c0>`, and no re-key entry pins `LOG.md`/`SCORECARD.md`: `C1_R54_PASS=true` | calibration (8; surface: the cold-read floor) | `rev=d33053f7552d c0=none credited=57 lost=7 rekeyed=0/7 readers=0/7 monitor=6/57 unstable=0 total=4 C1_R54_PASS=false` (`before/c1.stdout` = `CTL_0_c1`); pre-bind at C0 **and** at C1 the same counter reads `credited=41 lost=23 … total=4` — the fix pass does not move the floor, the re-key does | `total=0` (`cand_credited=64 lost=0 ok`, `covered=64 score=8`, `rekeyed=7/7 readers=7/7 unstable=0`) | `python3 .ufo/evidence/round-54/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | CTL_0 / CTL_R53 / CTL_FAB / CTL_LOGINPUT false, CTL_POS_c1 true (`control/controls-a.stdout`: `CONTROLS_A: 5/5 as pre-registered`) |
| C2 one scratch-root exit class across the seven tools, stated in the registry and the note: `C2_R54_PASS=true` | operability (no numeric score; surface: the scratch-root exit class) | `unusable_exit2=3 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false` (`before/c2.stdout` = `CTL_0_c2`); the same pre-amendment bytes re-run at base read `usable_ok=6 … total=14` (`.ufo/waves/round-54/w1/T54W1ExecFreeze-receipts/c2-frozen-bytes-at-base.out`) — one arm, load-sensitive, disclosed in §2.3 and **not** averaged; on the amended bytes this seat reads `total=13` at base and `total=0 C2_R54_PASS=true` at C1 | `total=0` (all five arms 7/7, `note=1`, `sources≥1`) | `python3 .ufo/evidence/round-54/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | CTL_0 false at base; CTL_EXIT0, CTL_POS_c2 true at the deciding revision (`control/controls-b.stdout`) |

### 3.4 "Measured close" paragraph — template, to be filled only from `after/`

> Deciding run at `<REV>` (`.ufo/evidence/round-54/after/`): `FROZEN_UNCHANGED=1
> freeze=<FREEZE> rev=<REV>`; no-harm `<N>/14 ok`; census exit 0. **C1**: `C1_R54:
> rev=… c0=… credited=… lost=… rekeyed=…/7 readers=…/7 monitor=…/… unstable=… total=…
> C1_R54_PASS=…` — read from `after/c1.stdout`, never from this table. **C2**: `C2_R54:
> … total=… C2_R54_PASS=…` — read from `after/c2.stdout`. `DECIDING_RUN_EXIT=…`
> (`after/deciding-run.exit`). If any deciding line differs from the Target cells above,
> that row is void and the report says so; a section that cannot be re-read cleanly is an
> honest stop, never a narrowed target (contract kill rule, quoted verbatim in §6).

### 3.5 Corrections this draft makes to the rows already in `SCORECARD.md`

Each is a byte-level citation defect, quoted, with the command that shows it.

1. **C2 `Before` cell cites a receipt that does not print its number.** The cell reads
   ``unusable_exit2=3 docs=0 note=0 sources=0 total=14`` false (`.ufo/evidence/round-54/before/c2.stdout` …)`` but
   `git show HEAD:.ufo/evidence/round-54/before/c2.stdout | tail -1` prints
   `… usable_ok=7 … total=13 C2_R54_PASS=false`. Fix: cite
   `.ufo/waves/round-54/w1/T54W1ExecFreeze-receipts/c2-frozen-bytes-at-base.out` for the
   `total=14` line (and keep `before/c2.stdout` for the `total=13` line), as §3.3 does.
2. **The C2 `Before` fragment omits the arm that differs.** `unusable_exit2=3 docs=0 note=0
   sources=0 total=14` hides `usable_ok=6`, which is the only field separating 13 from 14.
   Quote the full verdict line or the disclosure has nothing to attach to.
3. **The round-54 header is one re-freeze stale.** It says "frozen at `441c26be` … and
   `7883e0e5` is the freeze pointer the deciding run uses"; `git diff 441c26be HEAD --
   .ufo/evidence/round-54/freeze.json` shows the manifest now has 10 hashed files and
   amendment 2, and the last change to `deciding-run.sh`/`freeze.json` is `097985c`. Use the
   §3.1 prose.
4. **Freshness rule cell divides by a number the counter does not use.** The cell reads
   ``floor(10 * fresh / 73)``; `.ufo/evidence/round-45/freshness/measure.py` computes
   `(10*fresh)//len(population)` and the C1 receipt prints `population=74 … fresh=71 …
   score=9`. The score is the same either way (710//73 = 710//74 = 9); the rule text is not.
5. **C1 `Before` cell stops at C0.** It says "at C0 the round's own edits drift it to
   `credited=41 lost=23`". The revision the deciding run actually measures is C1, and the
   fresh C1 run prints the same `credited=41 lost=23` (§2.2). Say "at C0 and at C1 (pre-bind)".

---

## 4. Provenance — every number, the exact command, the observed output

`LANE` = `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. All runs used frozen bytes
extracted with `git show HEAD:<path>` into scratch (sha256 shown in §1) and a fresh
`--work` directory. Nothing was read from the live working tree except the lane's git
objects.

| Number | Command (exact) | Output observed |
|---|---|---|
| Instrument identity | `sha256sum $S/code/{c1/measure.py,c2/measure.py,c1/lost-headings-at-base.json}` | `63f5f881…` / `49280fe5…` / `a953d2e8…` — equal to `freeze.json` |
| C1 base | `python3 $S/code/c1/measure.py --lane "$L" --rev d33053f7552d --work $S/work-c1-at-base --explain` | `cand_credited=57 lost=7 RED` … `total=4 C1_R54_PASS=false`, exit 1 |
| C1 at C1 | same with `--rev 99c3bc88d704…` | `cand_credited=41 lost=23 RED` … `total=4 C1_R54_PASS=false`, exit 1 |
| C1 per-section at C1 | `bash $S/code/precheck.sh "$L" ef19d8e1e7ba… 99c3bc88d704…` (output piped to `tail`, so the pipeline exit is `tail`'s) | 23 `LOST` lines, `cand_credited=41 lost=23 RED`; the counter's arm 1 records `exit=1` for the same comparison |
| C2 base, amended bytes | `python3 $S/code/c2/measure.py --lane "$L" --rev d33053f7552d --work $S/work-c2-at-base --explain` | `usable_ok=7 … total=13 C2_R54_PASS=false`, exit 1 |
| C2 at C1, amended bytes | same with `--rev 99c3bc88d704…` | `unusable_exit2=7 usable_ok=7 docs=7 note=1 sources=3 total=0 C2_R54_PASS=true`, exit 0 |
| C2 at C1, pre-amendment | `cat .ufo/waves/round-54/w1/T54W1ExecFreeze-receipts/c2-frozen-bytes-at-head-99c3bc8.out \| tail -1` | `usable_ok=6 tmp_mkdirs=0 docs=7 note=1 sources=3 total=1 C2_R54_PASS=false` |
| Passing-line sweep | `grep -rh "^C1_R54: \|^C2_R54: " . \| grep -c "PASS=true"`; then `for r in …; do git cat-file -e "$r^{commit}" && …; done` | `27` passing lines; every C1-verdict rev answers `not-in-lane` |
| The 14 reading | `cat .ufo/waves/round-54/w1/T54W1ExecFreeze-receipts/c2-frozen-bytes-at-base.out` | `usable_ok=6 … total=14 C2_R54_PASS=false` |
| The 13 reading | `git show HEAD:.ufo/evidence/round-54/before/c2.stdout \| tail -1` | `usable_ok=7 … total=13 C2_R54_PASS=false` |
| Base-receipt identity | `git cat-file -s HEAD:.ufo/evidence/round-54/before/c2.stdout`; `git show HEAD:…before/c2.stdout \| wc -l`; `stat -c %s .ufo/waves/round-54/w1/T54W1ExecFreeze-receipts/c2-frozen-bytes-at-base.out` | `1307`, `8`, `1355` — the committed before-receipt is not the 1355 B file the wave-1 seats read |
| Freeze manifest drift | `git diff 441c26be HEAD -- .ufo/evidence/round-54/freeze.json` | 8 keys → 10, `amendments: []` → two entries |
| Frozen paths stable since | `git diff --quiet 097985c HEAD -- .ufo/evidence/round-54/; echo $?` | `0` |
| Frozen path set | `python3` over `contract.json:frozen_paths` vs `deciding-run.sh:$FROZEN` | 11 vs 11; the deciding list uses `$E/…` which expands to the contract's absolute paths |
| Dirty-tree gate | `git status --porcelain \| grep -vc "^?? .ufo/evidence/round-54/after"` | `5` at 11:58, `7` at 12:03 (L1 `integrate/` work landed) → `DECIDING_REFUSED dirty-tree` |
| after/ absent | `ls -d .ufo/evidence/round-54/after` | `No such file or directory` |
| re-key absent | `ls -d .ufo/evidence/round-21/coldread/rekey-r54-*` | `No such file or directory`; ledger has 568 entries |
| depth at C1 / base | `git show <REV>:tools/mutate-and-run.sh \| python3 -c '…re.findall(r"^#   (?:js\|bash)-\S+\s+\S+\s+\d+/\d+")…'` | `recorded_cases=10 depth_score=10` at both |
| freshness at C1 | `python3 .ufo/evidence/round-45/freshness/measure.py --lane "$L" --rev 99c3bc88d704…` | `population=74 … fresh=71 score=9 … C1_R45_PASS=true` |
| census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | exit 0 |
| source rows | `git show 99c3bc88d704…:corpus/SOURCES.md \| grep -cE '^ {0,3}\| S[0-9]{3,} \|'` | `139` |
| wave-1 reader set | `python3` over `.ufo/waves/round-54/w1/*Read*.json` | 23 files, every `cand=59c38109…` (C0), 28 findings in total |
| wave-2 reader set (at this seat's read) | `python3` over `.ufo/waves/round-54/w2/*.json` | 20 files, every `cand=99c3bc88…` (C1) |
| section bytes C0 vs C1 | round-18 `sectionize` on `git show <rev>:SKILL.md` for the 23 headings | 13 changed at C1; of the frozen seven, 5 changed (`## Standing rules`, `## Mutation-sweep recipe`, `### The boundaries`, `### Using the ledger`, `### The operator's runbook — …`) and 2 unchanged (`### Round-14 historical registry…`, `### Round-26 gate/probe registry…`) |
| C1 fix pass | `git show --stat 99c3bc88` | 6 files, +82/−32; `SKILL.md` 30/30, 22 hunks |

---

## 5. Deltas and route items for the L1 (quoted, not reconciled)

1. **Base C2: 13 vs 14.** Contract/control/before receipt print `total=13` (`usable_ok=7`);
   the wave-1 re-runs print `total=14` (`usable_ok=6`). Same two arm values, same
   arithmetic, one load-sensitive arm; the contract/control sample and both wave-1 samples
   were produced while the frozen C2 counter was still the pre-amendment `b4684a3f…`, and on
   the amended counter's bytes this seat reads `13` at base. Two further facts belong with
   the disclosure: the committed `before/c2.stdout`
   (1307 B) is a **regenerated, passing-arm** copy — the file the wave-1 seats measured was
   1355 B and read `14` — so the committed receipt cannot be cited as corroboration of the
   14; and `before/c2.stdout` is byte-for-byte the verdict line of `CTL_0_c2`, so it is one
   sample, not two (§5 item 5 below).
2. **Wave-1 finding count: three numbers.** The C1 commit message says "26 wave-1 reader
   findings adjudicated and fixed"; the wave-2 brief says "25 genuine findings"; the 23
   wave-1 reader JSONs contain 28 `findings` entries in total
   (`python3` sum over `.ufo/waves/round-54/w1/T54W1*Read*.json`). The report should quote
   whichever the L1 adjudicated and say which one it is; the draft leaves the sentence out
   of §3.1 rather than pick.
3. **C1 arm 4 and the binder read `.ufo/waves/round-54/w1/` only — the wave-2 reports are
   written to `w2/`.** `c1/measure.py:53` `WAVE = '.ufo/waves/round-54/w1'` and
   `:223` `if not re.search(r'/T54W\d+.*Read.*\.json$', path):`; `binder.py:48` the same
   constant. The 23 wave-1 JSONs pin `cand=59c38109` (C0) and 5 of the 7 frozen sections
   changed bytes at C1, so they cannot satisfy `d.get('cand') == c0 and
   d.get('section_sha256') == sec['sha256']` for `c0 = 99c3bc88` at the deciding revision;
   the 20 wave-2 JSONs that exist so far pin `99c3bc88`, but they sit in `w2/`. Unless the
   L1 lands the wave-2 reports under `w1/` before binding (or amends the constant), arm 3
   skips every heading (`SKIP … no-clean-reader`) and arm 4 stays `readers=0/7`, so C1
   cannot reach `total=0`. This is a route fact, not a defect claim: `binder.py:2-3` says
   "find a committed reader report `.ufo/waves/round-54/w1/*.json`", so the constant is
   deliberate and the integration step is the thing to check. At my last read the L1 had
   already edited `binder.py` in the working tree (accepting readers whose findings are
   adjudicated in the new `integrate/resolutions.json`, 9 headings, `gap-minor` verdicts);
   that changes *which* readers bind, not the directory it looks in — `WAVE` was still
   `.ufo/waves/round-54/w1` at line 48.
4. **The tree is not clean enough to decide yet.** `git status --porcelain` listed five
   untracked wave paths at 11:58 and seven dirty paths at 12:03 (the L1's `integrate/` work
   in between), and `controls-b.*` does not exist; `deciding-run.sh:57` and `:51`
   would refuse before any counter runs. The "after" column depends on that being fixed
   first, in that order.
5. **`before/c2.stdout` and the control receipt are the same sample, not two.** Both print
   `usable_ok=7 … total=13`; only the wave-1 re-runs print `14`. Reading the committed
   `before/` file as an independent second opinion on the arm would over-count the evidence.
6. **Seven passing `C1_R54_PASS=true` lines exist in the tree and all of them are fixtures.**
   Their revs (`023cbc7f5a56`, `10ada0d5bc32`, `52227471f8ed`, `5d5a8b6187e0`, `783eab7bf24f`,
   `9ce447c50971`, `c79ef005c098`) are not lane commits, and two of the files sit under
   `.ufo/waves/round-54/w2/T54W2Sent02-receipts/` (a sentinel's constructed tree). Nobody
   should read the "after" cell from them; the C1 verdict at the deciding revision is only
   whatever `after/c1.stdout` says.

## 6. Contract text quoted verbatim (so the draft cannot narrow it)

C1 target: *"C1_R54_PASS=true: the frozen round-48 precheck prints cand_credited=64 lost=0
ok at the deciding revision, the unchanged round-21 selector reads covered=64 score=8,
every one of the seven base-lost sections carries a fresh entry bound under
rekey-r54-<c0> that credits at the deciding revision, a committed wave reader report pins
each section's bytes at <c0>, and no re-key entry pins LOG.md or SCORECARD.md"*
C1 kill rule: *"any arm failing makes C1_R54_PASS=false; a section that cannot be re-read
cleanly is an honest stop, never a narrowed target"*.
C2 target: *"C2_R54_PASS=true: 7/7 self-tests exit 2 with a naming could-not-evaluate line
and no traceback on a set-but-unusable TMPDIR, 7/7 exit 0 on an empty TMPDIR (declared
unset) and on a usable one with no mkdir under /tmp, the seven registry rows carry the
scratch_root cell, and the note corpus/knowledge/scratch-root-contract.md cites an S row
mined this round with the lesson Gate naming its URL and 2026-10-28"*.
C2 kill rule: *"any arm short of 7/7 makes C2_R54_PASS=false"*.

## 7. What this seat did not do

- No lane file edited; no `git` mutation of any kind (only `show`, `diff`, `status`,
  `rev-parse` reads). No counter, contract, freeze, ledger, registry, wave spec or report
  belonging to another seat was modified. The `integrate/binder.py` modification and
  `integrate/resolutions.json` visible in `git status` are the **L1's** concurrent work
  (§1), not this seat's.
- No deciding run, no binder run, no control run — those write lane state and belong to the
  L1. The two C2 and two C1 readings in §2 are **seat runs**, labelled as such everywhere.
- No tool installed or upgraded (nothing was needed); no package manager invoked.
- The "After" cells are deliberately empty: no deciding receipt exists, and this draft does
  not infer one from a seat run.
