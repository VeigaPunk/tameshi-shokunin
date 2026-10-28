# T55W2CritC2Scope — C2's denominator honesty (`registry-check --rev` has no positive arm)

Seat: critic, wave 2, round 55 (L1 TameshiR55). Axis attacked: **operability**.
Content under attack: **C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`**. Counter bytes used for scoring:
`.ufo/evidence/round-55/c2/measure.py` at HEAD, sha256 `0458f632087f665fbafc07efc6920d32febf7551d9fc5964d0c87fa0e139476b`,
which is the digest `freeze.json` records (C0's own copy, `36ca47d…`, predates amendment 8 and prints
`total=1` at the all-green state; that bookkeeping defect is already routed by T55W1ScribeSkill and is not
re-litigated here). No lane production file, frozen file or wave spec was modified; all trees are
`git clone --shared` copies in scratch (`/fast/scratch/hyaku/tameshi-r55/T55W2CritC2Scope`, removed on exit).

## Verdict (first)

C2's scored sentence is **true as arithmetic and false as coverage**. The counter's mode table has 14 rows:
9 allocating, 13 "cheap". `registry-check --rev` is the one allocating row with `cheap=False`
(receipts/mode-table.txt). Consequence, measured:

- The counter runs `registry-check --rev` **exactly once per run, and only under the unusable TMPDIR**
  (grammar arm, `measure.py:198-205`). It is never executed by the empty arm or the usable arm
  (`measure.py:217-219` loops over `cheap`). **No arm ever observes the mode succeeding.**
- A tree in which the real-lane `registry-check --rev` **fails under the counter's own empty arm**
  (`TMPDIR=""`, expected exit 0, observed exit 2 with a stdout verdict) still scores
  **`grammar=9/9 … total=0 C2_R55_PASS=true`** (receipts/counter-witness.out, exit 0).
- A tree in which the real-lane `registry-check --rev` is **permanently dead** — it always prints the frozen
  class line, even when `TMPDIR` is a usable directory it then names as "not usable" — also scores
  **`total=0 C2_R55_PASS=true`** (receipts/counter-witness2.out, exit 0). The grammar arm cannot tell
  "refuses because the value is unusable" from "refuses always"; the two arms that could tell are exactly
  the two the mode is excluded from.
- The real mode is not healthy at C0 anyway: `--rev HEAD` at C0 returns **rc 1** in the counter's own clone
  layout (`held=45/49`, four `differs` rows, receipts/counter-layout-rev.out) and **rc 1** in a populated
  fleet mirror (`held=46/49`, receipts/fleet-good.out, 659 s). The counter's own expectation for the mode is
  exit 0, so an honest positive arm would be red today — the exclusion is load-bearing, not just a time cap.

Disclosure: **explicit in the note**, **partial in the contract**, **absent in SKILL.md and in the wave
brief / report plan** (details in §3). The claim is therefore not disclosed where the graded target and the
operator-facing rule state it.

Smallest safe correction (§7): (a) say in the contract target, SKILL.md bullet and wave brief that the
ninth mode is grammar-only and that eight of nine allocating modes keep their expected exit on the
empty/usable arms; (b) stop implying the mode works — record one committed observation of real-lane `--rev`
under empty and usable `TMPDIR` with its actual exit, or fix the failing rows before claiming it; (c) make
the grammar arm check the *value*, so "refuses always" cannot pass (§6 witness B).

## 1. What I attacked

Three things, in this order:

1. The **denominator**: which modes each arm executes, read from the frozen counter and dumped by running it.
2. The **wording**: whether the exclusion is stated where the contract target, the note, SKILL.md, the
   registry cell and the wave brief are read.
3. The **power of the arm set**: two witness trees, one "works under a good `TMPDIR`, fails under an empty
   one", one "permanently dead", each scored with the frozen counter.

## 2. The denominator, measured

Receipt: `receipts/mode-table.txt` (command below, run from the lane root).

```
python3 - <<'EOF'
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location("m", ".ufo/evidence/round-55/c2/measure.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for name, argv, exp, alloc, cheap in m.modes(pathlib.Path("/w"), pathlib.Path("/c")):
    print(f"{name:34s} | {exp} | {alloc} | {cheap}")
EOF
```

Output (tail):

```
registry-check --rev               | 0 | True | False
...
allocating: 9 cheap: 13 total rows: 14
```

So the metric `empty=13/13 usable=13/13` (contract `before` and `target`) counts 8 allocating modes (the
seven self-tests plus `env-diff --contract`) and the 5 lazy modes. The ninth allocating mode is in the
grammar term only. `modes()`'s own docstring (`measure.py:82-84`) says this; nothing else in the scored
claim does.

## 3. Is the exclusion disclosed where a reader meets it?

| Where a reader meets the claim | Says what about `registry-check --rev`'s arms? | Verdict |
|---|---|---|
| `.ufo/evidence/round-55/contract.json` `target` (HEAD, line 29; sha `31d5c8ad…`) | "9/9 allocating modes … on a set-but-unusable TMPDIR … **13/13 cheap modes** keep their expected exit on the empty and the usable arms". "cheap" is **not defined anywhere in the contract**; 13 vs the 14 modes is the only signal. The exclusion is stated in `amendments[5]` ("amendment 6"), not in the target. | **partial** |
| `corpus/knowledge/scratch-root-contract.md` `## One line, every mode (round 55)` lines 82-84, 97-98 (sha `0b7ed223…`) | "`registry-check --rev` is measured on the **unusable arm only**: it builds a full fleet clone (minutes), so its usable path is covered by the tool's own self-test, which exercises the same helper"; "The counter measures nine allocating modes on the unusable arm, thirteen modes on the empty and usable arms". | **explicit and correct** |
| `SKILL.md` `## Standing rules` scratch bullet, lines 37-41 (sha `e0ce89f7…`) | "**Measured on every documented allocating mode** — the seven self-tests plus `env-diff --contract` and `registry-check --rev` — as one stderr line … exit 2; the five non-allocating modes stay lazy". No arm scope: a reader takes "measured on every documented allocating mode" as the three-arm contract the preceding sentence defines (unset/empty/unusable). | **not disclosed** |
| Wave brief / report plan (`spec-w2.json` context line 6; same text in `w2-dispatch.json`) | "one stderr line, one exit class, **nine documented allocating modes**", next to the base verdict `empty=13/13 usable=13/13`. | **not disclosed** |
| `tools/registry.json` cell `registry-check-selftest.scratch_root` (at C0) | "TMPDIR empty => unset, the platform default applies; a usable TMPDIR holds every mkdtemp and nothing is created under /tmp … **Allocating modes: selftest, --rev**". The docs arm only checks the cell contains the marker; it never measures the assertion for `--rev`. | **asserted, unmeasured** |

A reader who meets the claim at the target (the graded sentence), in SKILL.md (the rule an operator runs),
or in the wave brief (the report plan) is **not** told that the ninth mode has no positive arm. A reader of
the note is. The note is linked from SKILL.md, but the target sentence and SKILL.md remain literally
incomplete: `cheap` is undefined in the contract, and the target's "13/13" reads as a property of the claim
rather than as a denominator that excludes the mode with no positive observation.

## 4. Witness A — works under a good `TMPDIR`, fails under an empty one

Tree: C0 plus one hunk in `tools/registry-check.py` (full diff: `receipts/witness-diffs.diff`, final file
`receipts/witness1-registry-check.py`). The guard fires only when `TMPDIR` is empty/unset **and** the lane
carries more than one registry row — the exact boundary the selftest fixture lane (one row, `rev-ok`,
`tools/registry-check.py:1058-1064`, exercised at `:1680-1689`) cannot cross, and the real lane (56 rows)
always crosses.

```
export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r55/T55W2CritC2Scope
git clone -q --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/wit/tameshi-shokunin"
git -C "$S/wit/tameshi-shokunin" checkout -q -B r55-c0 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
[ "$(git -C "$S/wit/tameshi-shokunin" rev-parse --show-toplevel)" = "$S/wit/tameshi-shokunin" ]
# one-hunk guard (see receipts/witness-diffs.diff), then:
git -C "$S/wit/tameshi-shokunin" -c user.name=witness -c user.email=w@local commit -q -m witness
cd "$S/wit/tameshi-shokunin"
TMPDIR="$S/no-such-tmpdir" python3 tools/registry-check.py --rev HEAD   # grammar arm
TMPDIR=""                 python3 tools/registry-check.py --rev HEAD   # empty arm
```

Outputs:

```
# grammar arm (receipts/witness-probes-a.err), rc=2, stdout empty
registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/.../no-such-tmpdir' (could-not-evaluate)

# empty arm (receipts/witness-probes-b2.out / -b2.err), rc=2
stdout: REGISTRY_CHECK: could-not-evaluate (clone scratch needs an explicit TMPDIR)
stderr: (empty)
```

The empty arm expects exit **0** (`mode-table.txt`: `registry-check --rev | 0 | True | False`), so a
denominator that included the mode would score it FAIL. The defect is visible in the counter's *own* clone,
not just in my tree:

```
cd $S/counter-work/clone        # measure.py's internal checkout of the witness rev, 56 rows, basename "clone"
TMPDIR="" python3 tools/registry-check.py --rev HEAD   # → rc=2, stdout "REGISTRY_CHECK: could-not-evaluate (clone scratch needs an explicit TMPDIR)"
```
(`receipts/witness-in-counter-clone-empty.{out,err}`)

Frozen counter on this tree:

```
python3 .ufo/evidence/round-55/c2/measure.py \
  --lane "$S/fleet/tameshi-shokunin" \
  --rev 2b6fb13dc84ed5a65d2c26dad234ac7fc634e42f \
  --work "$S/counter-work" --explain
```

```
EXPLAIN grammar registry-check --rev               rc=2  ok
EXPLAIN empty   ... (13 modes, all ok) ...
C2_R55: rev=2b6fb13dc84e grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true
exit=0
```
(`receipts/counter-witness.out`, `receipts/counter-witness-receipts.json` — `bad={}`)

**No arm catches it.**

Note on the "works" half of the item's premise: at C0 on this host the real-lane `--rev` does not return
the counter's expected exit 0 in either layout I measured —

- counter's own clone layout (no sibling lanes): `rc=1`, `held=45/49 superseded=7`, `differs`:
  `mutate-and-run-regression`, `sources-census`, `verify-round15`, `mte-interop-check`
  (`receipts/counter-layout-rev.out`);
- populated fleet mirror (all `*-shokunin` siblings symlinked, the wave sandbox layout): `rc=1` after
  **659 s**, `held=46/49 superseded=7`, `differs`: `mutate-and-run-regression`, `sources-census`,
  `verify-round15` (`receipts/fleet-good.out`, `receipts/fleet-good.rc`).

The witness guard is inert when `TMPDIR` is set (it is inside `if not os.environ.get("TMPDIR")`), so those
runs measure C0's own behaviour. Caveat recorded honestly: `--rev` rows run in a clone whose *siblings* are
live symlinks, so a long run during a ~900-seat wave can move; the rc=1 was reproduced 13 minutes apart in
two different layouts, and one of the differing rows (`sources-census`) reproduces in a plain C0 clone with
no siblings at all (§6).

## 5. Witness B — a permanently dead mode scores 9/9

Tree: C0 plus a guard that raises `ScratchRootUnusable` for any lane with more than one registry row,
naming whatever `TMPDIR` value it has (`receipts/witness2b-registry-check.py`). Probes
(`receipts/witness-probes-w2*.err`):

```
unusable TMPDIR  rc=2  ... TMPDIR is not a usable directory: '/…/no-such-tmpdir' (could-not-evaluate)
empty TMPDIR     rc=2  ... TMPDIR is not a usable directory: '<unset>' (could-not-evaluate)
usable TMPDIR    rc=2  ... TMPDIR is not a usable directory: '/…/goodtmp' (could-not-evaluate)   ← false statement
```

`/…/goodtmp` is a writable directory. The mode never works; it still prints the frozen class line every
time. Scored by the frozen counter:

```
python3 .ufo/evidence/round-55/c2/measure.py --lane "$S/wit2/tameshi-shokunin" \
  --rev 4844ed7945ab577381adcd793555dab7bd968f1e --work "$S/counter-work2" --explain
→ EXPLAIN grammar registry-check --rev  rc=2  ok
→ C2_R55: rev=4844ed7945ab grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 ... total=0 C2_R55_PASS=true
exit=0
```
(`receipts/counter-witness2.out`, `receipts/counter-witness2-receipts.json`)

This is the sharpest statement of the gap: **the grammar arm has no falsifier for "refuses always"**, and
the two arms that would falsify it (empty and usable) do not run the mode. The tool's own `--selftest`
does exercise `--rev` under all three `TMPDIR` states, but only on a one-row fixture lane; witness B is
keyed on the row count precisely because that is the property the fixture lacks.

## 6. Collateral: C0 breaks a registered entry command (`sources-census`)

Not the C2 claim's surface, but the operability fact the excluded positive arm is closest to. The lane-local
registered row `sources-census` (`bash .ufo/evidence/kaika-round-1/sources-census-v2.sh`, expect exit 0 +
`SOURCES_CENSUS: CLEAN`) is **CLEAN at base and VIOLATIONS at C0**:

```
# base clone (no siblings)
git -C "$B" checkout -q -B r55-base 0a2010ac…; (cd "$B" && bash .ufo/evidence/kaika-round-1/sources-census-v2.sh)
→ SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)   rc=0     (receipts/base-census.out)

# C0 clone (no siblings)
(cd "$S/wit/tameshi-shokunin" && bash .ufo/evidence/kaika-round-1/sources-census-v2.sh)
→ no-id-or-path-cite: S280 corpus/knowledge/scratch-root-contract.md (Errors.html)
→ SOURCES_CENSUS: VIOLATIONS                             rc=1     (receipts/c0-census-nosib.out)
```

Cause: `corpus/SOURCES.md` says S280 is "mined by `corpus/knowledge/scratch-root-contract.md`", but the note
cites only S277-S279 — the new S280 row has no citation in its own mining document. Smaller ruler, one
line: adding `(S280)` to the note's "The class is one stderr line, byte-shaped:" sentence makes the row
CLEAN again (`receipts/c0-census-proposed-fix.out`, rc=0, tested in scratch and reverted). This is C1 /
sources-seat territory; reported because it is a C0 regression that the C2 counter's arms cannot see (they
run no registry rows) and that the excluded `--rev` arm *does* see (`ROW sources-census … differs` in both
`--rev` layouts above). The required fleet census is not affected:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
exits 0 (140 rows).

## 7. Smallest safe correction

1. **Name the exclusion where the claim is graded.** Contract `target`: "…8 of the 9 allocating modes (all
   but `registry-check --rev`) keep their expected exit on the empty and the usable arms; `registry-check
   --rev` is measured on the unusable arm only, and no arm shows it succeeding." Define `cheap` (13 = the 8
   allocating modes run on those arms + the 5 lazy modes) or drop the adjective. Same sentence in SKILL.md
   lines 37-41 and in the wave brief. No measurement changes; the arithmetic stays 13/13.
2. **Do not imply the mode works.** Either record one committed observation of real-lane `--rev` at C0 under
   an empty and a usable `TMPDIR` with its actual exit (here 1, with the `differs` rows named), or make the
   mode's real outcome 0 first and then add a bounded positive arm in a populated fleet mirror. A positive
   arm run inside `measure.py`'s own clone would be red even on a correct tree: its clone has no
   `*-shokunin` siblings, so `mte-interop-check`'s regression cannot run (`SETUP (regression exit 2)`).
3. **Give the grammar arm a value check.** Require the quoted value in the class line to equal the unusable
   `TMPDIR` the arm passed. Witness B then fails (it prints the usable path as "not usable"), and "refuses
   always" stops being a free pass. This is a predicate tightening, not a new denominator.

If the round prefers to keep the exclusion as a declared trade (it is defensible: minutes and a clone layout
the counter does not build), then correction 1 alone is the honest minimum — the claim would then say what
it measures, and §4/§5 show exactly what it does not.

## 8. What I did not attack / cannot see

- The seven self-tests' grammar on the unusable arm beyond the counter's own arm (other seats own the
  message mutations).
- Whether the real `--rev` failure at C0 (`sources-census`, `verify-round15`, `mutate-and-run-regression`)
  is stable outside a live 900-seat wave; the row set depends on live fleet siblings and wave load, and I
  measured two layouts, not a quiescent fleet.
- The C1 claim, the frozen counters' other arms, and the round-54 record corrections.

## 9. Artifacts opened / commands run

Opened (read-only): `.ufo/evidence/round-55/contract.json` (HEAD and C0), `c2/measure.py` (C0 and HEAD),
`before/c2.stdout`, `freeze.json`, `tools/registry-check.py` (C0), `tools/registry.json` (C0),
`corpus/knowledge/scratch-root-contract.md` (C0), `SKILL.md` (C0), `SCORECARD.md` (C0), `LOG.md` (C0),
`SPEC` = `.ufo/waves/round-55/spec-w2.json` / `w2-dispatch.json`, `integrate/resolutions.json`,
`corpus/SOURCES.md` (C0 and base), `.ufo/evidence/round-55/assimilation/S280-gnu-errors.txt`,
`.ufo/waves/round-55/w2/` peers' files not opened.

Commands (all receipts in `receipts/`): the mode-table import; the two witness builds in scratch clones
with a `rev-parse --show-toplevel` assertion before each commit; three-arm direct probes
(`TMPDIR=<unusable>`, `TMPDIR=""`, `TMPDIR=<usable>`); two frozen-counter runs
(`--lane … --rev <witness> --work <empty dir> --explain`, 179 s and 164 s, both exit 0, `bad={}`);
one real-lane `--rev` per layout (165 s / 659 s, both exit 1); the lane-local census at base and C0; the
proposed one-line census fix and revert; the required fleet census (exit 0, 140 rows).

No tool was installed or upgraded (no need). Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku;
S=$HYAKU_SCRATCH/tameshi-r55/T55W2CritC2Scope`, removed on exit (`trap 'rm -rf -- "$S"' EXIT`); the shared
parent `/fast/scratch/hyaku/tameshi-r55` was never deleted. No mutating git command ran in the lane.
