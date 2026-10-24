# W2ReviewC1Causality — tameshi round 36, wave 2 (reviewer, leaf seat)

Axis judged: **calibration**. Assignment: falsify C1 causality from scratch — independently
re-derive that the only delta between the content commit and the refresh commit is the
cold-read evidence set, re-run the monitor at both commits, confirm 6 then 8, and treat any
extra file in the delta as a defeat of the do-nothing control. Read-only seat: no production
edits; the only lane write is this report. Scratch root
`/fast/scratch/hyaku/tameshi-r36-seats/W2ReviewC1Causality/`.

Revisions in play (lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`):

| Name | Rev |
|---|---|
| r35 tip / contract `before` | `796e08b888849308d0c4d5e932e56833600a139f` |
| round-36 content = do-nothing control | `e423c41ba253357ab8c8513f0376dad9d38ab248` |
| round-36 cold-read refresh (under attack) | `b455001e2589b3f4f471d94a3de7e5e549b9f54c` |
| receipts commit | `d9c496b` |
| lane tip | `fbb01cf` |

No tool installs were needed (stdlib `python3`, `git`; no package manager touched).

## What I attacked

1. The delta's exact path set, blob modes, create/delete summary, and commit cardinality.
2. Independent monitor runs at the before rev, the control rev and the refresh rev (strict
   mode, no overrides), plus the lane tip.
3. Instrument immutability across the whole range: wrapper, round-18 algorithm, `SKILL.md`,
   `SHONEN.md`, `SCORECARD.md` rubric body.
4. The ledger's semantic delta: entry-by-entry deep equality, ordering, non-`entries` keys,
   duplicate-key framing.
5. Section-keyed binding: whether the four appended entries key the real current section
   bodies, and whether all their inputs hash to the committed bytes.
6. Trace-receipt honesty: re-derivation of every receipt's `stdout_sha256` from the committed
   tree, and the trace instrument's own digest.
7. **Causal isolation** (the decisive test): five throwaway repos that differ only in which
   pieces of the delta are present, to test necessity and sufficiency.
8. Score decomposition: why calibration is 6 or 8, i.e. what surface the four sections gate.
9. Post-refresh tip stability — does the measured 8 survive to `fbb01cf`?

## Exact commands and results

### 1. The delta is exactly the coldread evidence set

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --name-status e423c41 b455001
```

```
M  .ufo/evidence/round-21/coldread/ledger.json
A  .ufo/evidence/round-36/coldread/affected-sections.json
A  .ufo/evidence/round-36/coldread/refresh-receipts.json
A  .ufo/evidence/round-36/coldread/refresh-specs.json
A  .ufo/evidence/round-36/coldread/traces/L1/source-1.json
A  .ufo/evidence/round-36/coldread/traces/L1/source-2.json
A  .ufo/evidence/round-36/coldread/traces/L1/source-3.json
A  .ufo/evidence/round-36/coldread/traces/L1/source-4.json
```

Eight paths, one modified + seven added. Corroborating checks:

- `git diff --raw e423c41 b455001` → `:100644 100644 b2fe619 b0522d3 M ledger.json` and seven
  `:000000 100644 … A` records. **No mode changes**, no renames, no deletes.
- `git diff --summary` → seven `create mode 100644`; nothing else.
- `git rev-list --count e423c41..b455001` → `1`; the range contains only
  `b455001e… round-36: cold-read refresh — four L1 author source re-anchor entries …`.
- `git diff --name-only b455001 HEAD | grep -v '^.ufo/evidence/round-36/\(after\|control\)/'`
  → `corpus/lessons/round-36-verifier-spotcheck.md` only; all 23 post-refresh paths are
  additions, none touches an input cited by the four new entries.

**No extra file defeats the control.** Every changed path is cold-read evidence.

### 2. The monitor, re-run at each revision

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py \
        --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev <REV>
```

(`--repo .` in the contract's wording resolves to the same git toplevel; the absolute form is
required by this seat's path bounds. All runs exit 0, `trace_gate: strict`,
`overrides_used: false`.)

| Rev | Role | `calibration_restraint_score` | `sections_covered` | `box3_full_page` |
|---|---|---|---|---|
| `796e08b` | before (contract) | **6** | 60/64 | false |
| `e423c41` | content = do-nothing control | **6** | 60/64 | false |
| `b455001` | refresh (under attack) | **8** | 64/64 | true |
| `fbb01cf` | lane tip | **8** | 64/64 | true |

**6 at the content commit, 8 at the refresh commit** — the do-nothing control holds, and the
measured 8 is still live at the tip. Uncovered sets are identical at `796e08b` and `e423c41`
(`--explain`): starts 131, 375, 1380, 1436, each `reason=input-drift:…`, `vetoed=false`. No
uncovered section at `b455001`. The committed receipts
(`.ufo/evidence/round-36/after/monitor-at-*.stdout`,
`.ufo/evidence/round-36/control/monitor-at-e423c41b.stdout`) carry the same three numbers and
the same `revision` fields — I reproduced them independently rather than trusting them.

### 3. Nothing but data moved

| Artifact | sha256 at `796e08b` / `e423c41` / `b455001` |
|---|---|
| `.ufo/evidence/round-21/coldread/measure.py` (selector) | `657f009bdf1cc89a…` identical at all three (and at `HEAD`) |
| `.ufo/evidence/round-18/measure.py` (credit algorithm) | `7ca87a7c98196d87…` identical at all three |
| `SKILL.md` | `2381873162fc21db…` identical at all three (sections 131/375/1380/1436 have identical body shas `e37cf21e…`, `13d489ad…`, `d4600d2f…`, `441858d2…` at all three) |
| `SHONEN.md` | `55a4fceb62b0a8f6…` identical at all three; marks `['~','~','~','~']`, box-3 ledger link present at all three |
| `SCORECARD.md` | `d6c43418…` → `1b0124a7…` at the **content** commit, `47 insertions / 0 deletions` (`--numstat`), unchanged content→refresh |

`corpus/QUALITY.md` is likewise `+12/-0` at the content commit. So the 6→8 cannot be a rubric,
page, box or algorithm edit: `git diff --numstat 796e08b e423c41 -- SCORECARD.md` is
`47 0`, a pure append of the round-36 block, and nothing between the control and the refresh
touches any of these files.

### 4. Ledger delta: four appended entries, nothing rewritten

```
python3 -c '… json.load(git show REV:.ufo/evidence/round-21/coldread/ledger.json) …'
```

- `entries`: 493 → 497; `entries[0:493]` at `b455001` **deep-equal and order-identical** to
  all 493 entries at `e423c41`; the four new entries are positions 493-496.
- `schema`, `carried_from`, `provenance`, `round21_provenance` all deep-equal.
- Duplicate-key scan with `object_pairs_hook` on both ledgers and on all seven new evidence
  files: **no duplicate keys** (so no silent last-one-wins reframing).
- The textual diff is large (`40709 insertions / 40186 deletions`; 3,633,498 → 3,489,570 B)
  purely because the refresh re-serialized `indent=2` → `indent=1`. Semantics are append-only;
  the rewrite is disclosed in peer report `W2MTLogAppend` and `W2ReviewNoHarm`, and my
  independent comparison agrees. See finding M2.

### 5. The four entries key the real current sections

| Entry | start | `sha256` = section body sha at `b455001` | class / verdict / cmds / traces | `read_rev` |
|---|---|---|---|---|
| recipe | 131 | `e37cf21e3155bdd3…` ✓ | record / gap-minor / 1 / 1 | `e423c41` |
| restore discipline | 375 | `13d489ad9898567f…` ✓ | record / gap-minor / 1 / 1 | `e423c41` |
| the map | 1380 | `d4600d2f69f97bfd…` ✓ | record / gap-minor / 1 / 1 | `e423c41` |
| where to enter | 1436 | `441858d2ff55a2dc…` ✓ | record / gap-minor / 1 / 1 | `e423c41` |

Sections bind by `sha256` (section body), not `skill_sha256` (page) — `round-18/measure.py`
`by_sha` map. All 18 recorded inputs hash exactly to the `b455001` blobs (0 mismatches,
recomputed with `git show REV:<path> | sha256sum`), including the byte-pinned
`tools/mutate-and-run.sh` at `a7d3f2dd7d47511a…`. Each trace's `inputs` is a subset of its
entry's inputs with equal digests, `live_lane_reads = {}`, `external = {}`.
`refresh-specs.json` section shas equal the entry shas; `affected-sections.json` names the
same four starts and the same drift reasons I measured at `e423c41`.

### 6. The receipts reproduce byte-for-byte

`refresh-receipts.json` cites `instrument_sha256 f59c9312c56eb458…`; the committed
`tools/trace-inputs.py` hashes to exactly that at `e423c41` and `b455001`. I extracted each
receipt's inner argv, re-ran it against a read-only `git archive b455001` export as `--root`,
and hashed stdout:

| Section | claimed `stdout_sha256` | reproduced |
|---|---|---|
| 131 | `b17c30eaf87d98f4…` | match |
| 375 | `913f4064893dd21c…` | match |
| 1380 | `b56fa11204920230…` | match |
| 1436 | `05c7ce3f856b080f…` | match |

The cited inputs are identical at `e423c41` and `b455001`, so the digests bind to the
committed bytes at both revs.

### 7. Causal isolation matrix (decisive test)

Five throwaway repos under `/fast/scratch/…/iso`, each built from `git archive e423c41`
(read-only on the lane) plus a subset of the delta, committed in a fresh `git init` repo and
measured with the strict monitor:

| Case | Tree contents | score | covered | missing-section evidence |
|---|---|---|---|---|
| `s1-base` | `e423c41` exactly | 6 | 60/64 | the four input-drift sections |
| `s2-ledger-only` | + ledger append, **no** new trace/spec blobs | 6 | 60/64 | sections 375/1380/1436 gain `trace-missing:…/source-N.json`; 131 likewise |
| `s3-files-only` | + all 7 new evidence blobs, ledger untouched | 6 | 60/64 | unchanged input-drift reasons |
| `s4-full` | ledger append + all 7 blobs (= the whole delta) | **8** | 64/64 | none; reasons histogram `{"credited": 64}` |
| `s5-tampered-trace` | full delta, `source-1.json` first input digest corrupted | 6 | 63/64 | section 131 `trace-input-drift:LOG.md` |

Reading: the ledger append alone does **not** credit (the trace gate is load-bearing, not
decorative); the evidence files alone do **not** credit; the delta together is sufficient and
reproduces 8/64-64 exactly; one corrupted digest in one trace costs the whole +2. The four
entries are jointly necessary and sufficient for 6→8, and no file outside the eight-path delta
contributes.

### 8. Why the number is 6 or 8 (decomposition)

`SHONEN.md` marks are `['~','~','~','~']` with the round-21 ledger link present at every rev,
so `calibration_restraint_score = 2*3 + 2*box3_points = 6 + 2*box3_points`, and
`box3_points` requires `coldread.box3_full_page` (all 64 sections covered). The 6→8 is the
box-3 full-page flip driven by 60/64 → 64/64; it is not per-section arithmetic. Any single
uncovered section anywhere drops the score back to 6 — confirmed by `s5` (63/64 → 6).

## Findings by severity

**Blocking: none. Major: none.** C1's causal statement is not falsified; it is reproduced
from scratch, with the delta shown to be necessary and sufficient.

**m1 (minor, honest-disclosure, not a claim breach).** The appended entries declare
`commands_executed_count: 1`, but the trace blobs the monitor's gate actually reads carry only
`schema` / `inputs` / `live_lane_reads` / `external` — no `argv`, `exit` or `cwd`. The command
attestation lives in `refresh-receipts.json` (which I reproduced byte-exactly), and the
monitor never reads it. So the entry-level command count is a ledger declaration gated only by
the presence of an input manifest. This is the frozen instrument's design (gate 5 binds
inputs, not argv), and the refresh scope line — carried verbatim in `refresh-specs.json`,
`refresh-receipts.json` and `SCORECARD.md` — says "L1-author input-keyed source reads only;
not … required-command coverage". Filed for C2's predicate-completeness surface, not charged
against C1.

**m2 (minor, review-mechanics).** The refresh re-serialized the whole ledger (`indent=2` →
`indent=1`), so `git diff e423c41 b455001` cannot be read as "four lines appended"; the
`--name-status` path set is still correct, but isolating the append requires a parsed
comparison. I verified semantics (493 entries deep-equal and order-identical, other top-level
keys equal, no duplicate keys), so the kill rule's "only delta" survives. Risk is reviewer
misreading, not measurement error. Already reported by `W2MTLogAppend` / `W2ReviewNoHarm`;
this seat's independent parse agrees.

**i1 (informational, interpretive).** "Calibration 6 → 8" is a two-valued reading of this
instrument here: the +2 is the box-3 full-page gate, so the refresh buys the full +2 only by
covering *all four* drifted sections and keeps it only while every other section stays
covered. A reader could over-read the delta as graded partial credit for four headings; the
`SCORECARD.md` round-36 block states the measured numbers without that inference, so no
correction is required.

## Residual risk

- **Drift fragility is real and disclosed.** The four new entries pin `LOG.md`,
  `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/README.md`,
  `corpus/knowledge/closeout-r11.md`, `corpus/knowledge/survivor-fixture-minimization.md` and
  `tools/mutate-and-run.sh` at their `e423c41`/`b455001` bytes. Any later record commit
  touching those files re-drifts the four sections and returns 8 → 6. As of the lane tip
  `fbb01cf` the post-refresh commits add only `.ufo/evidence/round-36/{after,control}/`
  receipts and one lesson file, so the measured 8 still holds; that is verified, not assumed.
- The entries' `read_rev` is the *control* commit while the entries land one commit later.
  Coherent (sources were read at `e423c41`; the append is `b455001`) and the input gate
  verifies against the measured rev, but it means the receipt binds a pre-append state.
- Scratch repos are throwaway; the isolation matrix proves the delta's sufficiency in a tree
  byte-identical to `e423c41 + delta`, not a rebase of the live lane.

## Verification gaps

- I did not run `measure.py --selftest`; the frozen suite is separately registered and not
  required to establish this claim's causality.
- C2 (the v2 counter's predicates) is out of this seat's scope; another wave-2 seat owns it.
- The original generation root `/tmp/tameshi-r36-refresh-08zapax9/lane` no longer exists; I
  bound the receipts to committed bytes by reproducing stdout against a `b455001` export
  instead — a stronger check than re-running in a vanished `/tmp` copy.
- Text search was not used as semantic proof anywhere: the monitor's binding rules
  (`by_sha` section map, `input_failures`, `trace_reason`) were read in
  `round-18/measure.py` and exercised by the isolation matrix.

## Verdict

**C1 causality CONFIRMED (falsification attempt failed) on the calibration axis.** The
content→refresh delta is exactly eight cold-read evidence paths (one ledger append, seven new
evidence files, no mode changes, one commit, no monitor/algorithm/page/box/rubric edit); the
strict monitor prints **6 at `e423c41ba253357ab8c8513f0376dad9d38ab248`, 8 at
`b455001e2589b3f4f471d94a3de7e5e549b9f54c`** (60/64 → 64/64), matching the before rev
`796e08b` = 6 and the receipts; the isolation matrix shows the ledger append and the four
trace blobs are jointly necessary and sufficient, and a single tampered digest returns the
score to 6. Minor findings m1/m2 are disclosure-level and do not weaken the causal claim.
