# T54W2Exec01 — run and record the C1 counter at C1

Seat item: *"Run and record the C1 counter at C1 … record the verdict and every EXPLAIN line; the
readers arm should now count the wave-2 reader JSONs as they land and the re-key arm must still be
0/7 (no entries yet)."*

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
C1 (the fix commit under test): `99c3bc88d704566197783f66b211ee0a830e0330`
Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W2Exec01/` (nothing written outside the lane `w2/` scope
and this scratch; no lane production file, counter, contract, freeze, ledger or wave spec edited).

## 1. Verdict

**`C1_R54_PASS=false` at C1 — exit 1, `total=4`.** Every arm fails. This is the honest state of the
*fix* commit, not a defect in the counter's arithmetic: C1 carries no re-key directory and no
committed reader report, and the fix pass itself dropped 16 further sections below the base floor.

```
C1_R54: rev=99c3bc88d704 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
```

All EXPLAIN lines, in order (STDERR empty, exit 1):

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=99c3bc88d704 cand_credited=41 lost=23 RED
EXPLAIN arm2-monitor exit=0 covered=41 score=6
EXPLAIN arm3-rekey dirs=[] c0=None
EXPLAIN arm4-readers 0/7
```

Arm-by-arm reading at C1:

| arm | measured | meaning |
|---|---|---|
| 1 precheck | `floor_credited=64 cand_credited=41 lost=23 RED`, exit 1 | 23 of 64 sections are uncredited at C1 |
| 2 monitor | `covered=41 score=6` | the unchanged round-21 selector agrees: 41 credited, restraint 6 |
| 3 re-key | `dirs=[] c0=None`, `rekeyed=0/7` | **0/7 as the item predicts** — no `rekey-r54-*` directory exists at C1 |
| 4 readers | `readers=0/7` | no reader report is *committed* at C1 (see F1/F4) |
| 5 stable | `unstable=0` | no re-key entry pins LOG.md/SCORECARD.md (vacuous: no entries) |

The item's premise "the re-key arm must still be 0/7 (no entries yet)" **holds**. Its premise
"the readers arm should now count the wave-2 reader JSONs as they land" holds only for JSONs
**committed at REV**, and only after amendment 3 landed mid-item (F1); untracked wave-2 JSONs are
invisible (F4).

## 2. Instrument identity — the lane moved under this item

`git log --oneline` before this item: `097985c`. After it: `8da3539` (wave-1 correction pass) then
`4e2de73` (amendment 3). Consequently the C1 counter was run twice, at C1 both times, over two
different frozen bodies:

| run | `c1/measure.py` sha256 | amendments | lane HEAD at run |
|---|---|---|---|
| A (first) | `63f5f88147b898ee795dc925a04668d473c1fc845e370947307e3ea141a0b77b` | 1–2 | `097985c` |
| B (**authoritative**, §1) | `d7749f8469fbd49b4daaca6eacef89bc1cf48f553702b4f2fe1a7c80d5245812` | 3 | `4e2de73` |

Both digests equal the `c1/measure.py` value in `freeze.json` **at the time of the run** (checked),
and `FREEZE_INTEGRITY` at current HEAD re-derives **OK, files=10, amendments=3**. The two runs give
the same four arms and the same verdict line apart from instrument identity, so the C1 verdict is
not an artifact of which amendment was current.

Commands (run A, then run B with a fresh `--work`):

```sh
S=/fast/scratch/hyaku/tameshi-r54/T54W2Exec01; export TMPDIR=$S
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
python3 "$LANE/.ufo/evidence/round-54/c1/measure.py" \
  --lane "$LANE" --rev 99c3bc88d704566197783f66b211ee0a830e0330 \
  --work "$S/EMPTY2" --explain
```

Raw transcripts: `T54W2Exec01-receipts/c1-run-amend2-bytes-63f5f88.stdout` and
`…/c1-run-amend3-bytes-d7749f8.stdout` — both 365 B and byte-identical (`cmp` and `diff` exit 0),
i.e. the amendment-3 body changes no arm at C1.

## 3. Why C1 is 41/64 and not the base 57/64

The frozen precheck run directly (it prints one `LOST` line per section; the counter's EXPLAIN keeps
only its last line):

```sh
bash "$LANE/.ufo/evidence/round-48/quality/coldread-precheck.sh" "$LANE" \
  ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4 d33053f7552db4bd290c99a36979760f544c41ad
bash "$LANE/.ufo/evidence/round-48/quality/coldread-precheck.sh" "$LANE" \
  ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4 99c3bc88d704566197783f66b211ee0a830e0330
```

Base reproduces the contract's `before` exactly (`cand_credited=57 lost=7`), with 7 `LOST` lines that
are **set-identical** to `c1/lost-headings-at-base.json`:

```
LOST ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence | drifted=LOG.md,SCORECARD.md
LOST ## Standing rules | drifted=
LOST ### Round-14 historical registry — superseded by round 15 | drifted=tools/bash-witness-study.py,tools/evidence-disposition.py,tools/trace-inputs.py
LOST ### Round-26 gate/probe registry — report interop | drifted=
LOST ### The boundaries — what a service run is not | drifted=
LOST ### The operator's runbook — `corpus/knowledge/operator-runbook.md` | drifted=corpus/knowledge/operator-runbook.md,corpus/knowledge/service-limits.md,tools/mutate-and-run.sh
LOST ### Using the ledger | drifted=
COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=d33053f7552d cand_credited=57 lost=7 RED
```

At C1 the same command reports `cand_credited=41 lost=23` (`…/precheck-at-C1.txt`). The 23 are:

```
LOST ## Context gate classification and explicit exit classes — round 15 | drifted=corpus/SOURCES.md,tools/bash-witness-study.py,tools/context-capture.py,tools/evidence-disposition.py,tools/mutate-and-run.sh,tools/pin-disposition.py,tools/registry.json,tools/trace-inputs.py
LOST ## Effective expectation reconciliation — round 14 | drifted=
LOST ## Live-tree re-pin and entry-command monitor — round 17 | drifted=
LOST ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence | drifted=
LOST ## Pin disposition and provenance correction — round 13 | drifted=
LOST ## Repeated controls and gate registry — round 12 | drifted=
LOST ## Standing rules | drifted=
LOST ## The leg ledger — replay, receipt, and how it is read (round 7, measured) | drifted=corpus/SOURCES.md
LOST ## The operator's runbook and the six-leg regression (round 10, measured) | drifted=tools/registry.json
LOST ### Gate/probe registry | drifted=tools/bash-witness-study.py
LOST ### Round-13 gate/probe registry | drifted=corpus/SOURCES.md,tools/bash-witness-study.py,tools/pin-disposition.py
LOST ### Round-14 historical registry — superseded by round 15 | drifted=tools/bash-witness-study.py,tools/evidence-disposition.py,tools/trace-inputs.py
LOST ### Round-15 gate/probe registry | drifted=
LOST ### Round-17 gate/probe registry — re-pin and monitor | drifted=
LOST ### Round-18 gate/probe registry — routed-defect closure | drifted=
LOST ### Round-21 gate/probe registry — finite environment differential | drifted=.ufo/evidence/round-15/verify.py,corpus/QUALITY.md,corpus/SOURCES.md,tools/env-diff.py,tools/registry-check.py,tools/registry.json
LOST ### Round-26 gate/probe registry — report interop | drifted=
LOST ### The boundaries — what a service run is not | drifted=
LOST ### The operator's runbook — `corpus/knowledge/operator-runbook.md` | drifted=
LOST ### The service's limits — what tameshi refuses to mutation-test | drifted=
LOST ### The tick and the pin read | drifted=tools/pin-disposition.py
LOST ### Triggers T1–T3 and the re-pin rule | drifted=corpus/QUALITY.md,corpus/SOURCES.md,corpus/knowledge/service-limits.md,tools/bash-witness-study.py,tools/evidence-disposition.py,tools/pin-disposition.py,tools/registry-check.py,tools/registry.json
LOST ### Using the ledger | drifted=
COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=99c3bc88d704 cand_credited=41 lost=23 RED
```

Round-21 per-section reasons at C1 (`…/monitor-reasons-at-C1.txt`): 10 are `no-ledger-entry`
(the section's bytes changed, so no ledger entry matches) and 13 are `input-drift` on tool/corpus
inputs the fix pass edited (`tools/bash-witness-study.py`, `tools/pin-disposition.py`,
`tools/evidence-disposition.py`, `corpus/SOURCES.md`, `tools/registry.json`, …).

**Set identity (measured):** the 23 headings lost at C1 are *exactly* the 23 distinct headings that
wave 1 read, and `lost-headings-at-base.json` (7) is a subset of both. So wave 2's 23 sections are
the 23 sections the fix pass pushed below the floor — a coherent re-read set, not a sample.

## 4. Findings

### F1 — arm 4 originally scanned only `w1/`; the round's live reports land in `w2/` (FIXED by amendment 3 during this item; independently reproduced and verified here)

At run A the frozen body read `WAVE = '.ufo/waves/round-54/w1'`. Measured:

```sh
git -C "$LANE" ls-tree -r --name-only 99c3bc88d704566197783f66b211ee0a830e0330 .ufo/waves/round-54/w1/
# (empty: no w1/ entry in the C1 tree; wave files are siblings in round-54/, reader JSONs are untracked)
git -C "$LANE" log --oneline --all -- .ufo/waves/round-54/w1     # (empty: never committed)
```

Fixture (`git clone --shared` under scratch, `rev-parse --show-toplevel` asserted = fixture dir),
two reader JSONs pinned to C1's bytes, one per heading, differing only in directory:

| fixture rev | `w1/T54W2Read99.json` | `w2/T54W2Read98.json` | counter body | `arm4-readers` |
|---|---|---|---|---|
| B `234b135b` | committed ("### Using the ledger") | absent | pre-amend `63f5f88` | **1/7** |
| C `7c407638` | committed | committed ("## Standing rules") | pre-amend `63f5f88` | **1/7** (w2 invisible) |
| D `b97bce43` | committed | committed | pre-amend `63f5f88` | **2/7** (same bytes relocated to `w1/`) |
| C `7c407638` | committed | committed | **amend-3 `d7749f8`** | **2/7** (fixed) |

The fixture JSON body for each (only `heading`/`cand`/`section_sha256` are read):

```json
{"heading": "### Using the ledger", "cand": "99c3bc88d704566197783f66b211ee0a830e0330", "section_sha256": "10c6288580f2b581a57818356480537e3ba6af51f8dfe6fa23e91110cb9766ec", "findings": []}
{"heading": "## Standing rules", "cand": "99c3bc88d704566197783f66b211ee0a830e0330", "section_sha256": "61736dcebc2d3d148255f9b3edd0ceb1c7cf2284f2969475b8da838ded9a78fc", "findings": []}
```

**Verdict:** the pre-amendment arm could not reach 7/7 from wave-2 evidence — the very directory the
seats are told to write to was not listed. Amendment 3 (`4e2de73`) replaces the constant with
`WAVE_DIRS = ('.ufo/waves/round-54/w1', '.ufo/waves/round-54/w2')`; row 4 above shows it counts a
`w2/` report that row 2 rejected. Seat `T54W2Exec04` is credited in the contract for finding it;
this fixture is an independent reproduction plus the before/after measurement.

A second, older defect was reproduced by accident and is worth keeping as a control: the **C1-era**
counter body (`6a39b38…`) run against a rev that *contains* a committed
`…/rekey-r54-99c3bc88d704/traces/probe.json` still printed `dirs=[] c0=None`
(`…/fixture-B-w1-reader-pre-amend.txt`), i.e. the basename match of amendment 1 could never fire;
the amended body prints `dirs=['rekey-r54-99c3bc88d704']`. Amendment 1 is necessary and effective.

### F2 — the frozen re-key predicate covers 7 headings; the deciding-rev floor needs 23

Code (frozen, arm 3):

```python
for h in frozen:            # frozen = c1/lost-headings-at-base.json  (7 headings)
    good = [e for e in bound if e.get('heading') == h and …]
    if good: rekeyed += 1
if rekeyed != len(frozen): total += 1
```

and arm 1 separately requires `cand_credited=64 lost=0` at the deciding revision. At C1 the loss set
is 23 and the frozen list is 7, with `frozen ⊂ lost` and `lost == wave-1 heading set` (§3).

**Verdict:** re-keying exactly the frozen seven yields `rekeyed=7/7` while arm 1 stays RED — the arm
that reports the re-key is complete does not describe the re-key actually required. There is no
soundness hole (the verdict stays `false`), but the contract sentence *"every one of the seven
base-lost sections carries a fresh entry bound under `rekey-r54-<c0>`"* understates the work: the
16 further C1-lost headings (`## Repeated controls…`, `## Effective expectation reconciliation…`,
`### Gate/probe registry`, …) need entries too or the deciding run cannot print 64/64. Recommend the
L1 re-key **all 23** (the counter permits extra entries; only the seven are counted).

### F3 — `<c0>` is whichever commit the re-key directory names; reader `cand` must equal it, and section bytes are compared at `REV`, not at `<c0>`

Arm 3 derives `c0` from the single directory `rekey-r54-<prefix>`; arm 4 then requires

```python
if d.get('cand') == c0 and d.get('section_sha256') == sec['sha256']:   # sec = section at REV
```

Fixture evidence: the same two reader JSONs with `cand = 99c3bc88…` counted (`1/7`, `2/7`) **only**
because the fixture's re-key directory was named `rekey-r54-99c3bc88d704`, so `c0` resolved to C1.

**Verdict — two operational consequences the contract text does not state:**

1. The wave-2 reports all pin `cand = 99c3bc88d704…` (the wave-2 reader instruction). Therefore the
   re-key directory **must** be named `rekey-r54-99c3bc88d704`; any other tag (e.g. the C0
   `59c38109…`) makes `c0 ≠ cand` and every wave-2 report counts 0/7 even though the reports are
   correct.
2. `section_sha256` is compared against the section at **REV** while the contract says the report
   "pins each section's bytes at `<c0>`". These coincide only while `SKILL.md` is byte-identical
   between C1 and the deciding revision (`git diff --quiet C1 HEAD -- SKILL.md` → identical today).
   **Any further SKILL.md edit before the deciding run invalidates all 23 wave-2 pins** and requires
   another wave. Treat C1's SKILL.md as frozen from here.

### F4 — only committed bytes count ("as they land" is not enough), and the deciding-run gate refuses untracked wave output

The counter reads `git show REV:path` exclusively. Fixture: adding a fourth, **untracked**
`w2/T54W2Read97.json` (same valid shape) at the same rev left `arm4-readers 2/7`
(`…/fixture-untracked-w2-amend3.txt`). At C1 neither `w1/` nor `w2/` exists in the tree, which is
exactly why arm 4 is `0/7` there.

On disk right now (working tree, untracked): `w1/` 27 JSONs, `w2/` 21 JSONs — none committed:

```sh
git -C "$LANE" status --porcelain .ufo/waves/round-54/
?? .ufo/waves/round-54/w1-run.out
?? .ufo/waves/round-54/w1/
?? .ufo/waves/round-54/w2-run.out
?? .ufo/waves/round-54/w2.ready.dispatched
?? .ufo/waves/round-54/w2/
```

`deciding-run.sh` then refuses the whole run:

```sh
git status --porcelain > "$OUT/clean-tree-before.txt"
[ "$(grep -vc "^?? ${OUT#$LANE/}" "$OUT/clean-tree-before.txt")" = 0 ] || { echo "DECIDING_REFUSED dirty-tree"; … exit 3; }
```

**Verdict:** before the deciding run the L1 must commit the wave-2 reader JSONs (and remove or
commit the run outputs and the `w1/` superseded JSONs), otherwise the run refuses with
`DECIDING_REFUSED dirty-tree` before either counter executes. Committing them is also the only way
arm 4 can reach 7/7 (F4-untracked above).

### F5 — the counter's EXPLAIN drops the precheck's per-section detail

```python
last = lines[-1] if lines else ''
…
notes.append('arm1-precheck exit=%d %s' % (run.returncode, last[:160]))
```

At C1 the receipt therefore says `lost=23` and names none of them. Not a correctness defect — arm 1
still fails correctly — but the frozen evidence artifact under-describes the failure; the section
list in §3 required running the frozen precheck directly. If the deciding run is to be diagnosable
from `$OUT/c1.stdout` alone, the LOST lines should be surfaced.

### F6 — deciding-run readiness measured: two hard refusals today

```sh
for f in controls-a.stdout controls-a.exit controls-b.stdout controls-b.exit; do git cat-file -e "HEAD:$E/control/$f"; done
# PRESENT controls-a.stdout / controls-a.exit      MISSING controls-b.stdout / controls-b.exit
```

`deciding-run.sh` requires all four (`CONTROLS="$E/control/controls-a.stdout … controls-b.exit"`) and
refuses with `DECIDING_REFUSED control-receipt-missing` (exit 3) when one is absent.

And with the freeze commit the contract names:

```sh
git diff --quiet 441c26bec5e4 HEAD -- $FROZEN   # → non-quiet
FROZEN_UNCHANGED=0
 .ufo/evidence/round-54/c1/measure.py   | 19 ++++++++++++-------
 .ufo/evidence/round-54/c2/measure.py   | 24 +++++++++++++++++-------
 .ufo/evidence/round-54/contract.json   | 32 +++++++++++++++++++++++++++-----
 .ufo/evidence/round-54/deciding-run.sh | 27 +++++++++++++++++++++++++++
 .ufo/evidence/round-54/freeze.json     | 31 ++++++++++++++++++++++++-------
```

`deciding-run.sh` sets `rc=1` on `FROZEN_UNCHANGED=0`, so invoking it with `FREEZE=441c26bec5e4`
fails even in an otherwise clean run. At `441c26b` the freeze manifest lists 7 files and its
`c1/measure.py` digest is `6a39b38…` — the pre-amendment body. `FREEZE_INTEGRITY` at `441c26b` is
`OK files=7` (self-consistent) and at HEAD `OK files=10 amendments=3`.

**Verdict:** the deciding run's `FREEZE` argument must be the newest amendment/re-freeze commit
(`4e2de73…` or later), not the `441c26bec5e4` the contract's frozen-claim line names. The claim's
freeze reference is stale after amendments 1–3.

### F7 — readiness of the reports that have actually landed (arm-4 predicate applied to the on-disk JSONs)

Judged with the counter's exact arm-4 test (`cand == C1` and `section_sha256 == sha of the section at
C1`, sections from the frozen round-18 sectionize):

```
w2 json files parsed: 21
arm4-valid against C1: 20
frozen7 covered by a valid landed report: 5/7
distinct valid headings: 20
  COVERED ## Standing rules
  COVERED ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
  COVERED ### The boundaries — what a service run is not
  MISSING ### Using the ledger
  COVERED ### The operator's runbook — `corpus/knowledge/operator-runbook.md`
  COVERED ### Round-14 historical registry — superseded by round 15
  MISSING ### Round-26 gate/probe registry — report interop
invalid: T54W2Sent01-forged-reader.json (## Standing rules; section_sha256 does not match C1)
```

**Verdict:** 20 of the 23 C1-lost sections already have an arm-valid report on disk and 5 of the
frozen 7 do; three sections — `### Using the ledger`, `### Round-26 gate/probe registry — report
interop`, `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` — were still
in flight at this reading, and one landed file is a
deliberately forged Sentinel fixture that arm 4 correctly rejects on the digest. None of the 20 counts
until committed (F4) — so the arm is satisfiable, but only after the reports are committed **and** the
re-key directory is named with C1's prefix (F3).

## 5. What this item did not measure

- The C2 counter and the 14 no-harm monitors (other seats).
- Whether re-keying the 23 headings makes the precheck green at a later revision — wave 2 cannot
  re-key, and re-keying is the L1's write.
- Whether each of the 16 C1-additional losses can be re-read cleanly; the 23 wave-2 readers decide that.

## 6. Commands run (all read-only against the lane; mutating git only inside `git clone --shared` fixtures)

```sh
git -C "$LANE" log/rev-parse/ls-tree/show/diff/merge-base/cat-file …            # reads
git -C "$LANE" clone --shared "$LANE" "$D/lane"                                 # fixture (scratch)
git -C "$D/lane" checkout -B probe "$H" ; add ; commit                          # fixture only
python3 "$LANE/.ufo/evidence/round-54/c1/measure.py" --lane … --rev 99c3bc88… --work … --explain
python3 .ufo/evidence/round-21/coldread/measure.py --repo "$LANE" --rev 99c3bc88…   # reasons
bash "$LANE/.ufo/evidence/round-48/quality/coldread-precheck.sh" "$LANE" ef19d8e1… {base,C1}
sha256sum / python3 hashlib loop over freeze.json                                # integrity
```

Fixtures: `fixture.HIL7y9` (heading/section shas at C1, clone based at C1) and `fixture2` (clone
based at lane HEAD, five commits A–D + one untracked file). Both deleted with the scratch tree.
Transcripts live in `T54W2Exec01-receipts/`.

## 7. Tooling

No tool installed or upgraded for this item; nothing needed beyond `git`, `python3` stdlib and the
lane's own frozen instruments. `pacman` untouched.

## 8. Bounds

- Wrote only `.ufo/waves/round-54/w2/T54W2Exec01.md` and `.ufo/waves/round-54/w2/T54W2Exec01-receipts/`.
- Read-only everywhere else; fixture git mutations carried the `-C "$D"` assertion of
  `rev-parse --show-toplevel`.
- No `agent://all` message; no commit/push/reset/add in the lane; no production file touched.
