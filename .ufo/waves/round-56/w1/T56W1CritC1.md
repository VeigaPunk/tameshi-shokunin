# T56W1CritC1 — falsifying C1 (round 56, wave 1)

Seat: `T56W1CritC1` (critic). Target: `C1_R56_PASS=true` in
`.ufo/evidence/round-56/contract.json`. Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`; frozen instruments `c3e2ca9f`
(base is its parent: `git rev-list --count base..c3e2ca9` = 1, so the round-56
instruments do not exist at base — every counter run below executes the lane's
frozen copy with `--lane` pointed at a scratch clone).

Nothing in this report edits the lane or a frozen instrument. Every state lives
in a `git clone --shared` of the lane under
`/fast/scratch/hyaku/tameshi-r56/T56W1CritC1/lane` (toplevel asserted before
every commit; `git -C "$L" rev-parse --show-toplevel` = `$L`). Receipts:
`T56W1CritC1-receipts/`. Machine-readable findings: `T56W1CritC1.json`.

## Bottom line

**`C1_R56_PASS=true` is reachable with zero section reads and zero content
change.** A fixture that appends 18 ledger entries whose `sha256` is computed
from the tree, one self-written trace receipt, and 18 reader JSONs whose
`section_sha256` is likewise computed from the tree — with `C0` set to the base
commit itself, so nothing is read *at* any commit — produces
`total=0 C1_R56_PASS=true`, identical to the verdict the round intends to earn
by re-reading.

| # | finding | arm | severity | makes a PASS inadmissible? |
|---|---|---|---|---|
| F1 | the whole target is reachable by fabrication (not just arm 4) | 3+4+6 | blocking | **yes, as instrument-certified proof** |
| F2 | do-nothing controls are refused (positive result) | 1,2,3,6 | — | no |
| F3 | arm 5 prints `unstable=0` unexamined at base; scope is re-key-bound entries only | 5 | minor | no (no load-bearing pin at base) |
| F4 | arm 6 reads only the last `\| calibration \|` row; the R55.3 stale row survives a PASS | 6 | major | no, but it leaves R55.3 undischarged |
| F5 | arm 1 executes the **live working tree**, not REV bytes (docstring says otherwise) | 1 | blocking | **yes, while the lane tree is not clean (R55.6/R55.7)** |
| F6 | no digest pin on round-18/21/48 instruments; a committed doctored selector satisfies arms 1 and 2 | 1,2 | blocking | **yes, until digests are pinned** |
| F7 | `external_inputs` are collected but never validated (false provenance) | 3 | major | no, but any provenance claim built on them is unverified |

## 1. The decisive experiment (F1)

Fixture state (`fixture-build.py fabricate`), all in one commit whose parent is
the base:

- `C0` = `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1` (the base itself; the contract
  only requires `c0` to be `REV` or an ancestor, `measure.py:192`);
- `.ufo/evidence/round-21/coldread/rekey-r56-981c5e8b20a2/traces/1.json` — a
  self-written receipt declaring `schema=tameshi-trace-inputs-v1` and one input
  pin (`tools/mutate-and-run.sh`, sha read from the tree);
- 18 ledger entries appended to the round-21 ledger, one per frozen heading:
  `class=record`, `verdict=verified-record`, `commands_executed_count=1`,
  `read_rev=<C0>`, `sha256=<section sha computed by the frozen sectionize>`,
  `inputs={tools/mutate-and-run.sh: <sha at REV>}`, `traces=[the rekey receipt]`;
- 18 files `.ufo/waves/round-56/w2/T56W2ReadCritNN.json` with
  `{"heading": h, "cand": <C0>, "section_sha256": <section sha>}`;
- one `| calibration |` row appended to `SCORECARD.md` stating 8 at
  `0a2010acd1e9` (the floor, where the monitor reads 8) and round 56.

Command:

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/c1/measure.py \
  --lane /fast/scratch/hyaku/tameshi-r56/T56W1CritC1/lane \
  --rev d6fe899da135383a8910861edf2cc235c4bdb941 \
  --work <empty dir> --explain
```

Output (`receipts/fabricate.txt`):

```
EXPLAIN arm1-precheck exit=0 COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=d6fe899da135 cand_credited=64 lost=0 ok
EXPLAIN arm2-monitor covered=64 score=8 box3=True
EXPLAIN arm3-rekey dirs=['rekey-r56-981c5e8b20a2'] c0=981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1
EXPLAIN arm4-readers 18/18
EXPLAIN arm6-restate row_score=8 row_commit=0a2010acd1e9 score_at_row=8 evidence='Restraint score of the strict cold-read monitor `python3 .uf' round='56 (restated at the commit it names)'
C1_R56: rev=d6fe899da135 c0=981c5e8b20a2 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true
```

The state contains **no content change at all**:

```
$ git -C $L diff --stat 981c5e8b..d6fe899 -- . ':!.ufo'
 SCORECARD.md | 2 ++
 1 file changed, 2 insertions(+)
```

(`receipts/fabricate-diff.txt`). `SKILL.md`, `corpus/**`, `tools/**`, `SHONEN.md`
and `LOG.md` are byte-identical to base. The score rises 6 -> 8 because the
monitor's `box3_points` is `box3_marked and box3_ledger_link and box3_full_page`
(round-18 `measure()`), and `box3_ledger_link` is already `true` at base
(`receipts/monitor-base-summary.json`: `marks ['~','~','~','~']`,
`box3_ledger_link true`, `box3_points false` only because `sections_covered=46`).
Restoring 64/64 credit is therefore sufficient for score 8 — no SHONEN.md edit
is needed, so no pin drifts and no reader is needed to justify the raise.

I repeated the same state with every tell-tale field removed (`provenance` on the
appended entries, `note` on the reader files; `fixture-build.py` writes them,
`receipts/fixture-run2.sh` strips them) and the verdict is unchanged
(`receipts/silent.txt`):

```
C1_R56: rev=6aa9d1514d62 c0=981c5e8b20a2 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true
```

The counter never reads those fields: `grep -c 'provenance\|note'` over
`.ufo/evidence/round-18/measure.py` is 0, and the 8 hits in `c1/measure.py` are
the `notes` list used by `--explain`.

**Why this is a claim defect and not just a fixture trick.** The contract's
`claims.C1.cannot_see` says: *"whether a reader actually read the section: the
reader's `section_sha256` is computable from the tree without reading, so a
fabricated reader report satisfies arm 4. The wave's adversarial seats are the
only guard, and the report says so."* That statement is too narrow. Arm 3's
`bound` test (`measure.py:203`) accepts an entry whose `sha256` and `read_rev`
are strings computable from the tree and whose `inputs` may name any file that
verifies at REV; arm 6 accepts any row whose score equals the monitor's, and the
monitor's score is a function of the same ledger. So the blind spot covers arms
3, 4 **and** 6, and `C1_R56_PASS=true` does not distinguish "18 sections were
re-read at C0" from "18 entries were appended at C0". The receipt for that claim
is `receipts/fabricate.txt`.

## 2. Do-nothing controls (item 1)

Each attempt in its own fixture commit; counter as above with `--rev <fixture>`.

| attempt | command (state) | verdict substring | why it fails |
|---|---|---|---|
| E0 base, untouched | `fixture-run.sh` E0 | `credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false` | reproduces `.ufo/evidence/round-56/before/c1.stdout` byte for byte |
| delete the 18 headings' ledger entries | `build.py del18` | `rev=69d0fdb5b333 ... credited=46 lost=18 ... total=5 C1_R56_PASS=false` | 17 of the 18 are lost by **input drift**, not by entry absence (drift map, §6), so deleting the entries removes no failing pin; the 18th (`## Standing rules`) already has no matching entry |
| delete every failing-verdict entry | `build.py delfail` | `rev=f79b6931541f ... credited=46 lost=18 ... total=5 C1_R56_PASS=false` | no live veto exists at base: all 18 lost sections are `vetoed=False`, and deleting a veto can only matter when a failing entry with **non-stale** inputs vetoes a section (`coldread`: `covered = credited > 0 and not vetoes`) |
| edit the standing row to 6, bind nothing | `build.py row6` | `restate=6 total=4 C1_R56_PASS=false` | moves only arm 6; arms 1-4 unchanged |
| edit the row to 6 but name a commit where the score differs | `build.py row6wrong` | `EXPLAIN arm6-restate row_score=6 row_commit=0a2010acd1e9 score_at_row=8 ... restate=6 total=5 C1_R56_PASS=false` | arm 6 *does* compare at the row's own commit (§4) |
| re-pin the 18 with fresh pins, no reader | `build.py repin` | `credited=64 lost=0 rekeyed=18/18 readers=0/18 monitor=8/64 unstable=0 restate=8 total=1 C1_R56_PASS=false` | arm 4 is the only guard against a re-pin without reading — and §1 shows arm 4 is computable |

So no do-nothing control reaches `64/64`: deleting entries, deleting failures and
editing the row each leave `total>=4`. The positive result stands. The negative
one is that *fabricating* the entries is cheaper than the do-nothing attempts and
does reach the target.

## 3. Arm 4 accepts a sha computed from the tree (item 2)

`receipts/fabricate.txt` `arm4-readers 18/18` and `receipts/pass-state-diff.txt`:
the reader file for `## Context gate classification and explicit exit classes —
round 15` carries `"cand": "981c5e8b20a2..."` and
`"section_sha256": "132cfb9ef1aa..."`, produced by:

```
python3 -c 'import round18; print({s["heading"]: s["sha256"] for s in round18.sectionize(SKILL_at_REV)})'
```

`receipts/pass-state-diff.txt` shows the same for `## Standing rules`
(`sha256 acfb671afd76...`, `chars_of_section_text_printed 0`). The target is
therefore reachable by fabrication: yes. The only residual guard is that the
round's own seats are honest, which is what the contract already concedes for arm
4 — but it concedes it for arm 4 only.

## 4. Arm 5 at base is vacuous, and its scope is narrower than its name (item 3)

At base the counter prints `unstable=0`, but `bound` is only built inside
`if rekey_ok:` (`measure.py:201`), and at base `rekey_dirs=[]` so `rekey_ok` is
false. `unstable=0` at base means **no entry was examined**, not "no entry pins
LOG.md/SCORECARD.md".

The lane at base does carry such pins: 6 entries pin `LOG.md` and 6 pin
`SCORECARD.md` (3 headings each, `receipts/arm5-scope.txt`). I checked whether
that is load-bearing: **0 credited sections depend solely on a LOG/SCORECARD-
pinning entry** (`receipts/arm5-scope.txt`, `credited sections whose ONLY
crediting entries pin LOG.md/SCORECARD.md: 0`). So the vacuity has no
consequence at base — I withdraw the stronger reading that the next LOG edit
would cost credit; it would not, because every such section has a redundant clean
entry. What remains is a denominator defect: `unstable=0` is presented as an arm
result when it is an empty domain, and a reader of the `before` line cannot tell
"checked and clean" from "not checked".

Liveness is fine when exercised: in a state whose bound entry pins `LOG.md` at
REV (`build.py unstable`), the counter reads
`unstable=1 ... total=1 C1_R56_PASS=false` (`receipts/unstable.txt`). The arm is
not dead; its domain is.

## 5. Arm 6: correct about the named commit, wrong about the file (item 4)

- It compares against the row's own named commit: `row6wrong` sets the row to 6
  and names `0a2010acd1e9` (monitor 8) -> `row_score=6 row_commit=0a2010acd1e9
  score_at_row=8 ... restate=6 total=5 C1_R56_PASS=false`. A row that names a
  commit where the score differs is refused. Good.
- It reads only the **last** `| calibration |` row (`measure.py:266`,
  `cells = rows[-1]`). In the PASS state (§1) `SCORECARD.md` at REV still carries
  the R55.3 row verbatim:

```
2579:| calibration | 8 | round-21 cold-read monitor ... | `d33053f7` | 53 |
2704:| calibration | 8 | Restraint score of the strict cold-read monitor ... | 0a2010acd1e9 | 56 (restated at the commit it names) |
```

  and the monitor at `d33053f7` reads `score 6 covered 57`
  (`receipts/fabricate-diff.txt`). Arm 6 reports `restate=8` while a row in the
  same table still asserts 8 at a commit where the monitor reads 6 — exactly
  R55.3, shadowed rather than disposed. A cold reader of the standing table can
  still find the false row.

## 6. Instrument trust (F5, F6)

**F5 — arm 1 executes the live working tree.** The docstring says *"every read is
of git objects at REV; the live working tree is never read"*, but `measure.py:147`
runs the round-48 precheck with `$LANE`, and the precheck does `cd "$LANE"` then
`python3 "$M"` with `M=.ufo/evidence/round-21/coldread/measure.py`
(`.ufo/evidence/round-48/quality/coldread-precheck.sh:11`) — a lane-relative
working-tree path. An **uncommitted** edit to the clone's working-tree selector
(`build.py wttamper`, REV stays the base commit) yields
(`receipts/wttamper.txt`):

```
EXPLAIN arm1-precheck exit=0 COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=981c5e8b20a2 cand_credited=64 lost=0 ok
EXPLAIN arm2-monitor covered=46 score=6 box3=False
C1_R56: rev=981c5e8b20a2 c0=none credited=64 lost=0 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=4 C1_R56_PASS=false
```

The verdict line then contradicts itself (`credited=64 lost=0 ... monitor=6/46`)
because `credited`/`lost` come from the precheck's live-tree measurement. This
matters for this round specifically: R55.6/R55.7 are uncommitted-work and
closure-seat-contamination defects, and an uncommitted file in the lane tree is
enough to flip arm 1.

**F6 — no digest pin on the executed historical instruments.** The counter reads
`.ufo/evidence/round-18/measure.py`, `.ufo/evidence/round-21/coldread/measure.py`
and the round-48 precheck **at REV** and executes them, and never compares their
sha256 to anything (`freeze.json` lists only round-56 paths; `measure.py` has no
digest check). Committing a doctored selector at REV (`build.py tamper`) gives
(`receipts/tamper.txt`):

```
EXPLAIN arm1-precheck exit=0 ... cand_credited=64 lost=0 ok
EXPLAIN arm2-monitor covered=64 score=8 box3=True
```

with zero content work. The digests are stable today — at both base and the
freeze commit: round-18 `7ca87a7c9819...`, round-21 `657f009bdf1c...`,
round-48 precheck `3b07847afc86...` — so pinning them is a one-line change with
no compatibility cost.

**F7 — `external_inputs` are decorative.** Round-18 collects them
(`measure.py:605-608`) into the output but no gate validates them: adding
`tameshi@<rev>:SHONEN.md = 0*64`, `/etc/passwd = f*64` and
`nonexistent/path.md = a*64` to a credited entry leaves `entry_reason` `None`
(`receipts/external-inputs.txt`). An entry's external provenance pin can be pure
invention; any "provenance trio" claim that leans on it is unverified.

## 7. Sweeps that found nothing (so the negative is shown)

- **Narrowing the heading list** — refused. Arm 1 compares the floor's credited
  heading *set* with the candidate's (`coldread-precheck.sh` body), so a dropped
  heading is `lost>0` even if its entries are deleted; arm 2 additionally
  requires `covered == 64` and `box3_full_page = (covered == total)`, so a
  candidate cannot trade one section for another (total must stay 64 and all 64
  credited for score 8).
- **Duplicate-heading substitution** — refused for the same reason: 64 sections
  with one duplicated heading gives 63 distinct headings, so the floor's set
  loses one (`lost>=1`), and `covered == total` cannot hold at 64.
- **Veto removal** — nothing to remove: at base every one of the 64 sections has
  `vetoed=False` (`receipts/monitor-base-summary.json`), and `delfail` changes
  nothing (`credited=46 lost=18 total=5`).
- **Deleting a drifted input instead of re-pinning it** — refused by
  `input_failures` (`input-missing:<path>`, round-18 `measure.py:330-351`), which
  is a failure reason, not a pass.
- **Two re-key directories** — refused: `rekey_ok = len(rekey_dirs) == 1`
  (`measure.py:188`).
- **Reader file outside `w2`/`w3`, or with a non-matching name** — not counted
  (`WAVE_DIRS`, regex `T56W\d+.*Read.*\.json$`).
- **Row naming a commit where the score differs** — refused (§5).
- **Do-nothing controls** — all refused (§2).

## 8. Admissibility

- **F1 alone makes `C1_R56_PASS=true` inadmissible as instrument-certified proof
  of the re-read.** The same verdict is produced with no read at all; the
  contract's `cannot_see` names only arm 4, so a reader would take arms 3 and 6
  as evidence they are not. The claim can still be *true* — 18 independently
  written reader reports can be honest — but it cannot be *certified* by this
  counter, and the contract says the opposite.
- **F6 makes any PASS inadmissible until the executed instruments are digest-
  pinned**, because the candidate can rewrite the instrument at the revision it
  is being measured at.
- **F5 makes a PASS inadmissible while the lane working tree is not clean**, which
  is precisely the R55.6/R55.7 condition this round must dispose of.
- F4 must be fixed or disclosed: a PASS leaves R55.3's false row in the file.
- F3 and F7 are defects to fix or state; neither alone falsifies a PASS.

## 9. Smallest safe corrections (proposed diffs, not applied)

**(a) Arm 1 must not execute the lane tree.** Keep the frozen precheck's
comparison semantics, drop its live-tree execution — measure both revisions with
the same REV mirror arm 2 already builds:

```diff
--- a/.ufo/evidence/round-56/c1/measure.py
+++ b/.ufo/evidence/round-56/c1/measure.py
@@ arm 1
-    pre_path = work / 'coldread-precheck.sh'
-    pre_path.write_bytes(pre)
-    run = subprocess.run(['bash', str(pre_path), lane, FLOOR, rev], capture_output=True, env=env)
-    lines = run.stdout.decode('utf-8', 'replace').strip().splitlines()
-    last = lines[-1] if lines else ''
-    credited = lost = None
-    m = re.search(r'cand_credited=(\d+) lost=(\d+)', last)
-    if m:
-        credited, lost = int(m.group(1)), int(m.group(2))
-    precheck_ok = run.returncode == 0 and m is not None and 'lost=0 ok' in last
+    r21 = show(lane, rev, R21)
+    r18 = show(lane, rev, R18)
+    if r21 is None or r18 is None:
+        print('C1_R56: error=instrument-blob-missing total=1 C1_R56_PASS=false')
+        return 1
+    f_cov, f_heads, _, _, _ = monitor_score(lane, FLOOR, r21, r18, work, env, 'floor')
+    c_cov, c_heads, _, _, _ = monitor_score(lane, rev, r21, r18, work, env, 'cand')
+    credited, lost = c_cov, len(set(f_heads) - set(c_heads))
+    precheck_ok = credited is not None and lost == 0
```

with `monitor_score` returning the credited heading set alongside the three
values it already parses. (Alternative, larger: run the bash precheck inside a
`git worktree add --detach <work>/tree <rev>` of the lane, so `cd "$LANE"` lands
on REV bytes.)

**(b) Pin the instruments.** After `rev = resolve(...)`:

```diff
+INSTRUMENT_PINS = {
+    '.ufo/evidence/round-18/measure.py': '7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37',
+    '.ufo/evidence/round-21/coldread/measure.py': '657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb',
+    '.ufo/evidence/round-48/quality/coldread-precheck.sh': '3b07847afc86d0d6c14d2e6c20a6b3778da1798d9304204ec3a360a6301b2924',
+}
+for rel, want in INSTRUMENT_PINS.items():
+    data = show(lane, rev, rel)
+    if data is None or hashlib.sha256(data).hexdigest() != want:
+        print('C1_R56: error=instrument-drift:%s total=1 C1_R56_PASS=false' % rel)
+        return 1
```

(Digests measured at both `981c5e8b` and `c3e2ca9f` — identical; the round-21
digest is the same `657f009bdf1c` the standing row already quotes.)

**(c) Arm 5 denominator and scope.**

```diff
-    bound = []
-    if rekey_ok:
+    bound = [e for e in entries if isinstance(e, dict)
+             and any(isinstance(t, str) and t.startswith(rekey_prefix) for t in (e.get('traces') or []))]
+    if rekey_ok:
```

and print `unstable=<n>/<len(bound)>` in the verdict line, so `unstable=0` can
never again read as "checked and clean" when the domain is empty.

**(d) Arm 6: every calibration row must agree.** Replace `cells = rows[-1]` with
a loop over all `rows`, computing `row_score`/`row_commit`/`same_at_row` per row,
and set `restate_ok = restate_ok and not [r for r in rows if r contradicts the
monitor at its own commit]`. That is what removes R55.3 rather than shadowing it.

**(e) Contract wording.** `claims.C1.cannot_see` must name arms 3, 4 and 6, and
the target must be phrased as what the counter measures ("the ledger credits 64
of 64 sections at REV through entries bound to C0"), with the independent-seat
reader reports named as the only guard — for all arms.

## 10. Recon: the 18-heading drift map (base 981c5e8b)

`receipts/drift-compact.json` / `drift.txt`. Sections are byte-identical to the
ones the ledger was keyed on (17 of 18 lost by **input drift**, 1 by entry
absence); SKILL.md pins are ignored by the algorithm (`IGNORED_INPUTS`), so the
drifted SKILL.md entries in the table below are harmless.

| # | heading | lines | prior entries | pins | drifted pins (effective) |
|---|---|---|---|---|---|
| 1 | `## Context gate classification and explicit exit classes — round 15` | 1639-1705 | 20 | 43 | SOURCES, bash-witness-study, context-capture, evidence-disposition, mutate-and-run, … (9) |
| 2 | `## Effective expectation reconciliation — round 14` | 1593-1626 | 1 | 42 | SOURCES, context-capture |
| 3 | `## Live-tree re-pin and entry-command monitor — round 17` | 1844-1875 | 1 | 78 | QUALITY, SOURCES, context-capture, registry-check, registry.json, repeat-control |
| 4 | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | 146-260 | 1 | 7702 | QUALITY, SOURCES, context-capture, registry-check, registry.json, repeat-control |
| 5 | `## Pin disposition and provenance correction — round 13` | 1546-1576 | 1 | 33 | SOURCES |
| 6 | `## Repeated controls and gate registry — round 12` | 1508-1527 | 1 | 168 | SOURCES, repeat-control |
| 7 | `## Standing rules` | 17-44 | **0** | 0 | — **no ledger entry for the current bytes** |
| 8 | `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | 936-949 | 2 | 30 | SOURCES |
| 9 | `## The operator's runbook and the six-leg regression (round 10, measured)` | 1299-1307 | 2 | 12 | registry.json |
| 10 | `### Gate/probe registry` | 1528-1545 | 2 | 125 | bash-witness-study, repeat-control |
| 11 | `### Round-13 gate/probe registry` | 1577-1592 | 2 | 25 | SOURCES, bash-witness-study, pin-disposition |
| 12 | `### Round-15 gate/probe registry` | 1706-1736 | 1 | 38 | context-capture |
| 13 | `### Round-17 gate/probe registry — re-pin and monitor` | 1876-1884 | 1 | 51 | SOURCES, context-capture, registry-check, registry.json, repeat-control |
| 14 | `### Round-18 gate/probe registry — routed-defect closure` | 1955-1967 | 1 | 71 | QUALITY, SOURCES, registry-check, registry.json |
| 15 | `### Round-21 gate/probe registry — finite environment differential` | 1994-2133 | 3 | 77 | round-15/verify.py, round-21 ledger, QUALITY, SOURCES, … (8) |
| 16 | `### Round-26 gate/probe registry — report interop` | 2162-2201 | 1 | 74 | context-capture, registry-check, registry.json, repeat-control |
| 17 | `### The service's limits — what tameshi refuses to mutation-test` | 1269-1298 | 1 | 39 | context-capture, registry-check, registry.json, repeat-control |
| 18 | `### Triggers T1–T3 and the re-pin rule` | 1087-1109 | 3 | 89 | QUALITY, SOURCES, service-limits.md, bash-witness-study, context-capture, … (10) |

Consequence for wave 2: every one of the 18 must be re-pinned to C0's bytes
(`corpus/SOURCES.md`, `corpus/QUALITY.md`, `tools/registry.json`,
`tools/context-capture.py`, `tools/registry-check.py`, `tools/repeat-control.py`,
`tools/bash-witness-study.py`, `tools/evidence-disposition.py`,
`tools/pin-disposition.py`, `.ufo/evidence/round-15/verify.py` and the round-21
ledger are the drifted set), and only `## Standing rules` needs a text edit. Note
that `## Standing rules` is the one heading with **no** ledger entry at all — its
section bytes changed in round 55 and the re-key must add an entry, not repair
one.

## 11. Fixture recipe and receipts

- Clone: `git clone --shared <lane> $S/lane && git -C $S/lane checkout --detach 981c5e8b…`;
  toplevel asserted before every commit (`fixture-build.py:assert_toplevel`).
- `fixture-build.py <state>`: `del18 | delfail | row6 | row6wrong | repin |
  fabricate | unstable | tamper | wttamper`.
- `fixture-run.sh` / `fixture-run2.sh`: build a state, run the frozen counter
  with `--lane $S/lane --rev <state> --work <fresh empty dir> --explain`.
- `fixture-drift.py`: the 18-heading drift map.
- Receipts: `E0-base.txt`, `del18.txt`, `delfail.txt`, `row6.txt`,
  `row6wrong.txt`, `repin.txt`, `fabricate.txt`, `silent.txt`, `unstable.txt`,
  `tamper.txt`, `wttamper.txt`, `fabricate-diff.txt`, `pass-state-diff.txt`,
  `arm5-scope.txt`, `external-inputs.txt`, `drift.txt`, `drift-compact.json`,
  `monitor-base-summary.json`, `census.txt`.
- Scratch was removed at the end of the seat; the receipts and the two fixture
  scripts are the reproducible residue.

## 12. Conformance

- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` -> `ok`, `census_exit=0`
  (`receipts/census.txt`; the validator also prints W04 duplicate-url warnings and
  one W01 `tierC mined` note for S101, which do not fail the run). `grep -c '^| S'`
  over `corpus/SOURCES.md` reads 142 at this seat's start.
- No lane production file and no frozen instrument was edited; no mutating git
  command touched the lane; every commit is in the scratch clone.
- Tooling: nothing installed or upgraded. `pacman` is paused host-wide and no
  install was needed (python3 stdlib + git only).
