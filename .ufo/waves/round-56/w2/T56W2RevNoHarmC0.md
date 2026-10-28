# T56W2RevNoHarmC0 — no-harm monitors at C0

Seat: `T56W2RevNoHarmC0` (reviewer). Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Content revision under review: **C0 = `c0137451f5b7f22d65f748fc69f1b181f55e1378`**.
Base: `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`.

## 1. The command and every line it printed

```
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/no-harm.sh \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  c0137451f5b7f22d65f748fc69f1b181f55e1378
```

Verbatim output (15 lines; receipt `T56W2RevNoHarmC0-receipts/no-harm-at-C0.stdout`):

```
NOHARM commandD recorded_cases=10 depth_score=10 ok
NOHARM coldread-floor score=6 credited=46 RED
NOHARM r45-freshness population=74 fresh=71 score=9 ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-140 142 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
NOHARM tools-scope [A:tools/receipt-revision-gate.py M:tools/registry.json ] ok
NOHARM registry-rows-not-shrunk base=56 rev=57 ok
NOHARM r49-generator-capability [PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31] ok
NOHARM r50-shrinker-selftest [SHRINK_SELFTEST: cases=14 failed=0] ok
NOHARM r53-scratch-hygiene tmp_hits=0 ok
NOHARM ledger-not-shrunk base=591 rev=591 ok
NOHARM sources-not-shrunk base=140 rev=142 ok
```

Exit status of the script: 0 (the script itself does not fail on RED; the deciding run reads the lines).

**14 `ok`, 1 `RED`.**

## 2. Is any monitor RED for a reason other than the cold-read floor?

**No.** Exactly one line is RED — `NOHARM coldread-floor score=6 credited=46 RED` — and that is
the cold-read floor itself. Every other monitor is `ok`.

## 3. Did the round's content cause the RED?

**No. The RED is inherited, not caused.** Three independent measurements:

**(a) The base reads identically.** Running the same script at the base:

```
NOHARM coldread-floor score=6 credited=46 RED
```

Same `score=6 credited=46`. The base is already RED on this monitor (receipt
`T56W2RevNoHarmC0-receipts/no-harm-at-base.stdout`).

**(b) The cold-read precheck says the content cost nothing.** The frozen round-48 precheck,
base → C0:

```
COLDREAD_PRECHECK floor=981c5e8b20a2 floor_credited=46 cand=c0137451f5b7 cand_credited=46 lost=0 ok
```

`lost=0`. The credited set is byte-identical at base and at C0 (diffing the two monitors'
`sections[]`: `lost base->c0: []`, `gained base->c0: []`, 46 credited in both, 64 sections in
both, `score=6` in both).

**(c) All 18 lost headings carry the *same* reason at base and at C0.** For every heading in
`c1/lost-headings-at-base.json`, the reason at base equals the reason at C0 — 18/18 `SAME`
(receipt `T56W2RevNoHarmC0-receipts/pin-exposure-analysis.txt`). Seventeen are
`input-drift:<path>`; `## Standing rules` is `no-ledger-entry` in both.

**(d) The C0 content commit touched 27 paths, none of which is pinned by any entry that
actually credits one of the 46 credited sections.** Overlap between the C0-changed set and the
pinned-input set of the *crediting* entries of the 46 is **NONE**. So the round's own edits
cannot uncredit the sections it did not intend to touch.

The RED is the round-55 damage (R55.3) that round 56 exists to repair, not a round-56
regression. The C1 counter confirms the same reading independently
(`T56W2RevNoHarmC0-receipts/c1-counter-at-C0.stdout`):

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=c0137451f5b7 cand_credited=46 lost=18 RED
EXPLAIN arm2-monitor covered=46 score=6 box3=False
EXPLAIN arm3-rekey dirs=[] c0=None
EXPLAIN arm4-readers 0/18
EXPLAIN arm6-restate row_score=8 row_commit=d33053f7552d score_at_row=6 evidence='...' round='53'
C1_R56: rev=c0137451f5b7 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false
```

Note the reference point the contract uses: the monitor at the round-55 floor
`0a2010acd1e92e4e332774050825e21bcfc7e079` reads `score=8 credited=64/64 box3=True`. At base and
at C0 it reads `score=6 credited=46/64` — 18 short. That gap is what the re-key must close.

## 4. Is each RED line the one the deciding run will require to be ok?

**Yes — there is exactly one RED, and it is exactly the line the deciding run requires to be
`ok`.** The deciding run's own logic (`.ufo/evidence/round-56/deciding-run.sh:138-140`):

```bash
bash "$SCR/code/no-harm.sh" "$LANE" "$REV" > "$OUT/no-harm.stdout" 2>&1; echo $? > "$OUT/no-harm.exit"
cat "$OUT/no-harm.stdout"; grep -q RED "$OUT/no-harm.stdout" && rc=1
[ "$(grep -c '^NOHARM .* ok$' "$OUT/no-harm.stdout")" = 15 ] || { echo "NOHARM_OK_COUNT!=15"; rc=1; }
```

Applied to the C0 capture:

* `grep -q RED` → matches → `rc=1`.
* `grep -c '^NOHARM .* ok$'` → **14**, not 15 → `NOHARM_OK_COUNT!=15` → `rc=1`.

So the single RED line is not merely tolerated by the deciding run — it is the *only* thing
between the current state and `NOHARM_OK_COUNT=15`, and the deciding run fails on both of its
checks until it clears. There is no other RED to attribute, so there is no second cause to
adjudicate.

**What clearing it requires.** The monitor's own gate (`.ufo/evidence/round-21/coldread/measure.py`,
via the round-18 credit algorithm) says the floor is `score>=8 && credited>=64`, and
`calibration_restraint_score = 2*sum(marks[b-1]=='~' for b in (1,2,4)) + 2*box3_points`, where
`box3_points = box3_marked and box3_ledger_link and cr['box3_full_page']`, and
`box3_full_page = sections_covered == sections_total`. At C0 the SHONEN marks are already all
`~` (4 boxes, `asserted=4`), and `box3_marked`/`box3_ledger_link` are both true — the *only*
missing term is full coverage. So `score` reaches 8 exactly when `credited` reaches 64, i.e.
when all 18 lost headings credit at the deciding revision. The RED and the C1 obligation are the
same obligation; there is no third thing to fix.

## 5. The 15 monitors the deciding run counts

The deciding run counts **15** `^NOHARM .* ok$` lines. In emission order, with the C0 observed
value:

| # | monitor | C0 observed | C0 |
|---|---|---|---|
| 1 | `commandD` | `recorded_cases=10 depth_score=10` | ok |
| 2 | `coldread-floor` | `score=6 credited=46` | **RED** |
| 3 | `r45-freshness` | `population=74 fresh=71 score=9` | ok |
| 4 | `r45-coverage` | `rows=2 entries=2 C2_R45_PASS=true` | ok |
| 5 | `S160-count` | `1` | ok |
| 6 | `registry-rows-not-below-140` | `142` | ok |
| 7 | `r46-coverage` | `rows=3 entries=3 C3_R46_PASS=true` | ok |
| 8 | `r47-coverage` | `rows=3 entries=3 C3_R47_PASS=true` | ok |
| 9 | `tools-scope` | `[A:tools/receipt-revision-gate.py M:tools/registry.json ]` | ok |
| 10 | `registry-rows-not-shrunk` | `base=56 rev=57` | ok |
| 11 | `r49-generator-capability` | `cases=400 violations=0 counterexample=none …` | ok |
| 12 | `r50-shrinker-selftest` | `cases=14 failed=0` | ok |
| 13 | `r53-scratch-hygiene` | `tmp_hits=0` | ok |
| 14 | `ledger-not-shrunk` | `base=591 rev=591` | ok |
| 15 | `sources-not-shrunk` | `base=140 rev=142` | ok |

## 6. Base → C0 delta: which monitors moved, and whether the content caused it

Diffing the two runs (base run vs C0 run), only four lines differ, and all four are the
round's *declared* additions moving in the permitted direction:

| monitor | base | C0 | verdict |
|---|---|---|---|
| `registry-rows-not-below-140` | 140 | 142 | ok — rows grew (S281, S282) |
| `tools-scope` | `[]` | `[A:tools/receipt-revision-gate.py M:tools/registry.json ]` | ok — both paths are on the monitor's own allowlist |
| `registry-rows-not-shrunk` | base=56 rev=56 | base=56 rev=57 | ok — grew |
| `sources-not-shrunk` | base=140 rev=140 | base=140 rev=142 | ok — grew |

The other eleven lines are byte-identical. **No monitor moved from ok to RED because of the
round's content.**

## 7. Findings that the L1 must act on before the deciding run

These are not RED monitors; they are constraints the deciding run will enforce that the C0
state does not yet satisfy. Each is measured, not inferred.

### F1 — The freeze argument named in the round brief is refused by the deciding run's gate

The round brief names the frozen instruments as `c3e2ca9f020776b3d66c7af854fb82c834674fcf`.
The deciding run rejects that value. `deciding-run.sh:96-100`:

```bash
FREEZE_LAST=$(git log -1 --format=%H "$REV" -- "$E/freeze.json")
[ -n "$FREEZE_LAST" ] && [ "$FREEZE" = "$FREEZE_LAST" ] || { echo "DECIDING_REFUSED freeze-not-last-manifest-commit $FREEZE"; exit 3; }
```

At C0 the last commit touching `freeze.json` is the amendment commit `21eb3c63cd0f3190c0deeb8953c6c91c7742cd68`.
Run with the brief's value:

```
FREEZE=c3e2ca9f0207 -> DECIDING_REFUSED freeze-not-last-manifest-commit c3e2ca9f0207 (last=21eb3c63cd0f)
FREEZE=21eb3c63cd0f -> gate PASSES
```

The freeze-integrity python block agrees: `FREEZE=21eb3c6` yields `FREEZE_INTEGRITY=OK`
(`amendments=1`, 2 manifest commits, contract mirrors the amendments); `c3e2ca9` yields
`MISMATCH` (0 amendments, contract does not mirror). **The deciding run must be invoked with
`FREEZE=21eb3c63cd0f3190c0deeb8953c6c91c7742cd68`.** Anyone reading the brief's
`c3e2ca9…` will be refused with exit 3 before any counter runs.

### F2 — `SKILL.md` must not change between C0 and the deciding revision

C1 arm 3 requires each bound entry to pass the frozen round-18 credit algorithm **at REV**,
and arm 4 requires each reader report's `section_sha256` to equal the section's sha **at REV**.
The credit algorithm matches a ledger entry to a section by the sha256 of the section *text*,
and section text is content-addressed, not offset-addressed. Measured against the frozen
`sectionize`:

* Appending a new `##` heading at the end of `SKILL.md`: `sections_total` 64 → **65**, and the
  64 existing section shas are unchanged. But `box3_full_page` requires
  `sections_covered == sections_total`, so 64/65 can never satisfy `score=8`, and C1 arm 2
  requires `covered == 64` exactly. **Appending a heading keeps the deciding run RED.**
* Editing one line inside a section: that section's sha changes; all other sections' shas are
  unchanged. The edited section would then have a reader sha (computed at C0) that no longer
  equals its sha at REV → C1 arm 4 refuses that report (`READER_HASH_XREV_DRIFT`).

C0 changed exactly one section's bytes — `## Standing rules`, lines 17-44 → 17-57 — and that
section is one of the 18 to be re-read. Its C0 sha is
`28bde4663c463ad40eba050dc9e5a97c6ed68148414cdfaf6d36789db5160bcc` (at base it was
`acfb671afd767c32476f57b040399972f6c870cd7dde3d821c344cae1a9ad767`, also absent from the
ledger). **The reader report for `## Standing rules` must carry the C0 sha, and `SKILL.md`
must be byte-identical from C0 to the deciding revision.**

### F3 — Three files are hot for the re-key: any post-bind edit to them uncredits the 18

The binder pins, per heading, the union of the old entries' input paths (minus its DROP set of
`LOG.md`, `SCORECARD.md`, `SKILL.md`, and the ledger). Measured against the C0-changed set:

| path | headings (of 18) that pin it | in binder DROP? |
|---|---|---|
| `corpus/SOURCES.md` | 13 | no |
| `tools/registry.json` | 11 | no |
| `corpus/QUALITY.md` | 6 | no |

`bind.sh` step 3c already refuses this (`PINNED-CHANGED` → exit 6), comparing PIN to the bound
revision. The constraint the L1 must respect: **after the bind, `corpus/SOURCES.md`,
`tools/registry.json` and `corpus/QUALITY.md` must not change before the deciding revision**,
or the 18 uncredit and the cold-read floor goes RED again. (Total union for the 18: 7721 paths;
the three above are the only ones the round's own content touches.)

### F4 — The SCORECARD restate edit is safe for the 46, and this is the point of arm 5

C1 arm 6 requires the **last** `| calibration |` row of `SCORECARD.md` at REV to state the score
the monitor actually reads. The current last row (line 2579) asserts `8` at `d33053f7`, and the
monitor at `d33053f7` reads **6** (measured: `score=6 credited=57`) — the R55.3 routed defect,
so arm 6 is currently failing. The L1 must therefore edit `SCORECARD.md` after the bind.

That edit is safe, and I checked it rather than assuming it:

* `SCORECARD.md` is in the binder's DROP set, so the 18 newly-bound entries do not pin it.
* Of the entries that *actually credit* the 46 credited sections, **none** pins `LOG.md` or
  `SCORECARD.md` — the one entry that does (`## The cadence's first scheduled tick, and the
  service's limits (round 9, measured)`, read_rev `eb7838b16490`) does **not** credit: its
  reason at C0 is `input-drift:LOG.md;…;input-drift:SCORECARD.md;…`, so it is already stale and
  contributes nothing.
* The 46's crediting entries pin **none** of the 27 C0-changed paths.

So a `SCORECARD.md` restate after the bind leaves the 46 credited. (C1 arm 5's own check — no
entry under `rekey-r56-*` pinning `LOG.md`/`SCORECARD.md` — is satisfied by the DROP set.)

### F5 — The standing row must name a commit whose monitor reads the score it claims

Arm 6 requires the row's measured-commit cell to resolve to a commit that is REV or an
ancestor of REV **and whose monitor score equals that same value**. The row that exists today
names `d33053f7`, where the monitor reads 6, not 8 — hence `restate=8` vs `score_at_row=6` in
the C1 output above. The L1 must name a commit at which the monitor reads the stated score.
The bound revision is the natural candidate, but it must be checked, not assumed: the monitor
must read `score=8` at that commit.

### F6 — `r45-freshness` sits on a knife edge with zero margin on one clause

`NOHARM r45-freshness population=74 fresh=71 score=9 ok`. The monitor's own check is
`f>=71 and 10*f//p>=9`. `fresh=71` is **exactly** at the floor: a single population row losing
its freshness makes `f=70` and the monitor RED, with no score slack to absorb it (score stays 9
down to `f=67`, but the `f>=71` clause does not). Population has room to grow to 79 before the
score clause bites. This monitor is not affected by the C0 content (its population rows are
`mined` rows with `id <= S160`; S281/S282 are outside that population), but any post-bind edit
that adds a `mined` row with `id <= S160`, or that disturbs a freshness entry's input, would
turn it RED at the deciding run.

### F7 — `tools-scope` admits exactly the two paths the round already used

The allowlist in `no-harm.sh` accepts only
`M:tools/{registry.json,registry-check.py,env-diff.py,bash-witness-study.py,context-capture.py,evidence-disposition.py,pin-disposition.py,repeat-control.py}` and
`A:tools/receipt-revision-gate.py`. C0's diff is exactly `[A:tools/receipt-revision-gate.py
M:tools/registry.json ]` — inside the allowlist. **Any additional file under `tools/`, added
or modified between C0 and the deciding revision, turns this monitor RED** and the deciding run
fails on it.

## 8. Census

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

Exit 0. The lane's own after-harness agrees:

```
CENSUS exit=0 rows=142
CENSUS_ROWS_SELFCHECK census=142 grep=142
CENSUS_SHAPE new_rows=2 findings=0
CENSUS_SHAPE_VERDICT pass=true new_rows=2 findings=0 rows_mismatch=false
```

**Discrepancy with the round brief, reported for the record (not a defect in the tree).** The
brief says "141 rows after this round's one new row". The tree has **142** rows: base 140, plus
**two** new rows this round — `S281` (in-toto Statement v1, status `mined`) and `S282` (SLSA
Build Provenance, status `rejected`, the refused candidate). The lane's own registry note
records both, and names `S283` as the next unused id. The hard requirement — the census
command exits 0 — holds. There is no 141 to chase.

## 9. Residual risk and verification gaps

* **The bind itself is unexercised at C0.** No `rekey-r56-*` directory and no committed reader
  report exist at C0 (`arm3-rekey dirs=[]`, `arm4-readers 0/18`). Whether the binder credits
  all 18 in one pass — every input present at PIN, no veto from a stale FAIL-verdict entry, the
  `REFRESH rekeyed=18 skipped=0 headings=18` tail — is unmeasured here. I did check the veto
  risk statically: **0 of the 18 has an old FAIL-verdict entry that stays non-stale**, so no old
  entry can veto a freshly bound section.
* **The deciding run is a single invocation** (`deciding_invocations: 1`); its gate order means
  a refusal at any gate burns it. F1 is the most likely way to burn it, since it is a wrong
  argument rather than a wrong tree.
* **The 46's redundancy is thin**: 43 of the 46 credit through exactly one entry. A single
  entry drifting between now and the deciding revision silently drops a section below the floor
  of 64 with no monitor naming which one. `no-harm.sh`'s `coldread-floor` reports only
  `credited=46`, not which sections moved.
* I did not run the wave-3 `bind.sh` (it mutates the lane working tree and commits — outside
  this seat's remit, and the L1 owns that commit).

## 10. Bottom line

At C0 exactly one no-harm monitor is RED — `coldread-floor score=6 credited=46` — and it is
the cold-read floor, not a collateral failure. The round's own content did not cause it: the
base reads identically, the precheck reports `lost=0`, all 18 lost headings carry the same
reason at base and at C0, and the 46 credited sections' crediting entries pin none of the 27
paths the content commit touched. The single RED is precisely the line the deciding run
requires to be `ok` (it is the difference between `NOHARM_OK_COUNT=14` and `15`, and it
trips `grep -q RED` as well), and clearing it is the same obligation as C1: bind all 18 so the
monitor reads 64/64 and `score=8`.

Seven constraints the deciding run will enforce that the C0 state does not yet meet are listed
in §7 — most urgently **F1**, the freeze argument (`21eb3c63cd0f…`, not the brief's
`c3e2ca9…`), and **F2/F3**, the byte-stability of `SKILL.md`, `corpus/SOURCES.md`,
`tools/registry.json` and `corpus/QUALITY.md` between the bind and the deciding revision.

## Tools and commands run

No tools were installed or upgraded for this seat (stdlib Python 3.14, `git`, `bash` only).

* `bash .ufo/evidence/round-56/no-harm.sh LANE C0` and the same at BASE
* `python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev <rev>` (C0, base, and
  the reference revisions `0a2010ac…`, `d33053f7…`)
* `bash .ufo/evidence/round-48/quality/coldread-precheck.sh LANE BASE C0`
* `python3 .ufo/evidence/round-56/c1/measure.py --lane LANE --rev C0 --work <empty> --explain`
* `python3 .ufo/evidence/round-56/c1/measure.py` internals re-implemented read-only via
  `importlib` on the frozen `.ufo/evidence/round-18/measure.py` (sectionize, `entry_reason`,
  `entry_is_stale`, `entry_failure`)
* `bash scripts/sources-census.sh validate|census --root …` and
  `bash .ufo/waves/round-56/census-after.sh --lane … --root …`
* `git show/diff/log/ls-tree` (read-only) in the lane; one `git clone --shared` scratch clone
  at the base under `$HYAKU_SCRATCH` for the base-census comparison

Receipts: `.ufo/waves/round-56/w2/T56W2RevNoHarmC0-receipts/`
(`no-harm-at-C0.stdout`, `no-harm-at-base.stdout`, `c1-counter-at-C0.stdout`,
`coldread-monitor-at-C0.json`, `pin-exposure-analysis.txt`).

No lane production file and no frozen instrument was modified. Scratch under
`/fast/scratch/hyaku/tameshi-r56/T56W2RevNoHarmC0` (removed on exit).
