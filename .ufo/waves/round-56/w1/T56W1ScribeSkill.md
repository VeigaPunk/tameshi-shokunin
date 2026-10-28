# T56W1ScribeSkill — `## Standing rules` receipt-binding rule (round 56, wave 1)

Seat item: draft the `## Standing rules` change — one bullet stating the receipt-binding
rule with the gate path, plus `situation -> rule -> code` rows for (a) a verdict receipt
naming another revision, (b) a positive control scored at the freeze, (c) a control set
whose CTL lines name a revision absent from the repo. Section only; under 20 added lines;
exact `diff -u` in the report.

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Base: `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`; freeze: `c3e2ca9f020776b3d66c7af854fb82c834674fcf`
- Status: **draft delivered**. No lane production file was edited by this seat; every
  byte-level change lives in a scratch clone and as a patch file. Frozen instruments were
  read, never written.
- Machine-readable twin: `.ufo/waves/round-56/w1/T56W1ScribeSkill.json`
- Receipts: `.ufo/waves/round-56/w1/T56W1ScribeSkill-receipts/`

## 1. The change (exact hunk)

`diff -u` of the section, old vs new (frozen sectionize boundaries; section body only):

```
--- section-before (`## Standing rules`, lines 17-43 + trailing blank stripped)
+++ section-after  (`## Standing rules`, lines 17-54)
@@ -25,3 +25,14 @@
   2; the five non-allocating modes stay lazy (round-55 C2 counter;
   corpus/knowledge/scratch-root-contract.md; the seven registry `scratch_root`
   cells).
+- **A receipt is evidence only for the revision it names.** A verdict or a
+  positive-control receipt is bound to the revision it certifies by
+  `tools/receipt-revision-gate.py --lane LANE --certified REV`: a receipt that
+  names another revision is refused with a named code, never re-read as if it
+  had been measured at the certified one (round-56 C2; ER-R54-1, R55.5).
+
+  | situation | rule | code |
+  |---|---|---|
+  | a verdict receipt names another revision | refused unless its bytes equal the certified revision on the declared `--paths` surface | `RECEIPT_REV_MISMATCH` |
+  | a positive control was scored at the freeze | refused: the freeze predates the work it certifies and drifts on the frozen surface | `RECEIPT_REV_CONTENT_DRIFT` (no `--paths`: `RECEIPT_REV_MISMATCH`) |
+  | a control set's CTL lines name a revision absent from the repo | refused: the revision cannot be resolved, so nothing is certified | `RECEIPT_REV_UNRESOLVABLE` |
```

`receipts/03-section-diff.txt` is the same diff regenerated from the two section-body
files (`03a-section-before.md`, `03b-section-after.md`); the quoted block above is a
verbatim prefix of it;
`receipts/09-standing-rules.patch` is the `git diff` hunk against `SKILL.md`.

Shape decisions, stated so the L1 can overrule cheaply:

- The bullet and the table are appended after the section's last existing bullet
  (`… cells).`). Every existing byte of the section is preserved: `git diff --stat` is
  `1 file changed, 11 insertions(+)`, zero deletions.
- **Three table rows, not one.** The unit the item names is one `situation -> rule -> code`
  triple; three distinct situations cannot be covered by one triple without a compound
  cell. Three rows keep each situation's refusal code exact. Total cost is still 11 added
  lines (5 bullet + 1 blank + 5 table), under the 20-line bound.
- The gate path is written in full (`tools/receipt-revision-gate.py`), so the C2 docs arm
  (`.ufo/evidence/round-56/c2/measure.py:250`, `'receipt-revision-gate' in SKILL.md`) is
  satisfied by the rule itself rather than by a bare tool name.
- Row 2's code cell carries the `--paths` qualifier because the gate has two refusal
  routes for a rev-≠-certified positive control: with `--paths` and drift it is
  `RECEIPT_REV_CONTENT_DRIFT` (`tools/receipt-revision-gate.py:140-143`), without
  `--paths` it is `RECEIPT_REV_MISMATCH` (`:136-138`). Writing only one would have made
  the row false for the other invocation.

## 2. Section identity, before and after

Computed with the **frozen** round-18 sectionize
(`.ufo/evidence/round-18/measure.py:209`), not a reimplementation — the same routine
`c1/measure.py:178` uses. `receipts/08-section-record.json`, `receipts/15-sections-changed-frozen.txt`.

| | start | end | sha256 | sections_total |
|---|---|---|---|---|
| before (base/freeze bytes) | 17 | 44 | `acfb671afd767c32476f57b040399972f6c870cd7dde3d821c344cae1a9ad767` | 64 |
| after (draft C0) | 17 | 55 | `449d7f4293850c68211f64f7b811994ef277aca2a8f45271750b35cd9841cbef` | 64 |

- Heading sets are identical (64 = 64); **exactly one** section's `sha256` changed
  (`## Standing rules`); the other 63 are byte-identical.
- 61 sections after the insertion point move down by exactly 11 lines; no section's
  content moved. Sectionize is fence-aware and the added table is not a heading, so no
  section is created or destroyed.
- **Re-key binding:** the wave-2 reader for this heading must carry
  `section_sha256 = 449d7f42…` **only if these exact bytes land at C0**. If the L1 merges
  other edits into the section, the hash changes and must be recomputed at C0 with the
  frozen sectionize — do not copy the value above blindly.
- My earlier ad-hoc splitter gave `c50be7af…` for the base section (it counted the
  trailing blank line); the frozen value `acfb671a…` supersedes it. Recording the
  discrepancy so the L1 does not bind the wrong hash from an intermediate note.

## 3. Operability: each row is a measured refusal, and the gate also accepts

Fixture: `D = $S/fixture`, `git init`, two commits — `A` (freeze, `e084f499199a`) and
`B` (work, changes `f2`, `d8db9982194b`); `surface.paths` lists `f2`.
`git -C "$D" rev-parse --show-toplevel` printed `$D` before any commit.
Receipt: `receipts/04-gate-fixture-three-codes.txt`.

| row | command (gate from the lane, read-only) | observed | exit |
|---|---|---|---|
| verdict names another revision | `--lane D --certified A --receipt r1:verdict` (r1 names `B`) | `codes=RECEIPT_REV_MISMATCH verdict=REFUSED` | 3 |
| positive control at the freeze | `--lane D --certified B --paths surface.paths --receipt r2:positive` (r2 names `A`) | `codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED`, `drift=f2` | 3 |
| control set names an absent revision | `--lane D --certified B --receipt r3:control` (r3 carries `rev=7df0e0426c98`) | `codes=RECEIPT_REV_UNRESOLVABLE verdict=REFUSED`, `rev=7df0e0426c98` | 3 |
| **liveness** (gate can accept) | `--lane D --certified A --paths surface.paths --receipt r2:positive` | `ok=1 refused=0 codes=none verdict=PASS` | 0 |

The liveness row matters: a gate that refused everything would satisfy the three rows
above and prove nothing. The same receipt file is refused when it names the freeze and
accepted when the freeze *is* the certified revision — the refusal tracks the binding, not
the file.

Real receipts the lane already accepted, re-derived at this seat (`receipts/05-real-receipts.txt`):

```
controls-b.stdout:control  --certified c2108100…  -> codes=RECEIPT_REV_UNRESOLVABLE rev=7df0e0426c98   exit=3
ctl-pos-c1.stdout:positive --paths round-54-surface.paths --certified c2108100…
                                                   -> codes=RECEIPT_REV_CONTENT_DRIFT rev=077d431e6996
                                                      drift first = .ufo/evidence/round-21/coldread/ledger.json  exit=3
round-55/after/c2.stdout:verdict --certified 4c04c1d3… -> codes=RECEIPT_REV_ABSENT revs=none             exit=3
```

These match the frozen before-counter line
(`.ufo/evidence/round-56/before/c2.stdout`: `red54=RECEIPT_REV_CONTENT_DRIFT
red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT`) while the round-54 deciding run
recorded `DECIDING_RUN_EXIT=0` for the same set — the R55.5 defect, reproduced.

## 4. Harm-none: the edit does not move the monitor

The C1 counter was run at three revisions of scratch clones (`receipts/06-…`, `07-…`, `12-…`):

| rev | counter verdict line |
|---|---|
| clone at base `981c5e8b` (control) | `credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 PASS=false` |
| clone at draft C0 on base `7a6732bc` | `credited=46 lost=18 … monitor=6/46 unstable=0 restate=8 total=5 PASS=false` |
| clone at draft C0 on freeze `d842481f` | `credited=46 lost=18 … monitor=6/46 unstable=0 restate=8 total=5 PASS=false` |

The base control reproduces `.ufo/evidence/round-56/before/c1.stdout` byte for byte, so
the harness is faithful; the two C0 runs read exactly the same numbers. The edit neither
gains nor loses a credited section — expected, because coverage is matched by section
`sha256` (`round-18/measure.py:611-614`) and the `## Standing rules` entry's sha
(`976cffc9…`) already matched neither the base bytes nor the post-edit bytes.

**Honest limit:** `unstable=0` in these runs is vacuous — `unstable` is only populated when
`rekey_ok` is true (`c1/measure.py:201-210`), and no `rekey-r56-*` directory exists yet. The
input-drift question was therefore tested directly, in §5.

C2 counter at the draft C0 on the freeze (`receipts/11-c2-at-draft-c0.txt`):

```
C2_R56: rev=d842481f0510 selftest=14/14 red54=RECEIPT_REV_CONTENT_DRIFT
        red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT
        own=own-receipts-missing docs=1/4 total=2 C2_R56_PASS=false
```

`docs` moves 0/4 -> 1/4 from this rule alone (arm 6 counts QUALITY, the knowledge note,
SKILL.md, and the registry cell separately, `c2/measure.py:226-258`). The remaining three
are sibling seats' deliverables; `own=own-receipts-missing` is the round's own control
receipts, which do not exist yet.

## 5. The heading's ledger state (what the re-key must actually bind)

The item's premise — "the one heading with no ledger entry" — is **contradicted by the
ledger**, and the correction matters for C1 arm 3:

```
.ufo/evidence/round-21/coldread/ledger.json, entries[heading=="## Standing rules"]:
  read_rev=eb7838b16490ca7ba17ea3242ade76a61f744af2  sha256=976cffc976563a9a…  start=17 end=29
  inputs: PROVINCE.md, corpus/knowledge/mutation-case-kimi-census.md,
          corpus/knowledge/mutation-case-kagi-census.md
```

- An entry exists (round-17 CR03). What is absent is an entry whose `sha256` matches the
  section at base — and the credit algorithm matches coverage by `sha256`, so the section
  is uncovered (`coldread(...)` at base: `covered 46 total 64`, `## Standing rules` in
  `uncovered_headings`, `receipts/` run in §4).
- That entry is stale on two further counts, **pre-existing and unrelated to this edit**:
  `input_reason` at base and at C0 returns
  `input-drift:PROVINCE.md;input-drift:corpus/knowledge/mutation-case-kagi-census.md`
  identically (`receipts/13-standing-rules-input-drift.txt`); `entry_is_stale` is `True`
  at both. The old entry can never be re-credited, whatever the section text says.
- Consequence for the re-key: a **new** bound entry under
  `.ufo/evidence/round-21/coldread/rekey-r56-<c0>/traces/` with `read_rev=<c0>`,
  `sha256=449d7f42…` (these bytes), `start=17 end=55`, `inputs` re-pinned **at `<c0>`**
  (`PROVINCE.md` at C0 is `b2875fe21f38…`, kagi-census at C0 is `d3190a9940b9…` — the
  pinned values in the old entry are dead), `commands_executed_count>0`, and traces that
  verify at REV. A re-key that copies the old entry's inputs or sha fails arm 3 at REV.

## 6. Findings for the L1

1. **Premise correction (C1 accounting).** `## Standing rules` has a ledger entry; it is
   stale, not missing (§5). Any report text that repeats "the one heading with no ledger
   entry" is contradicted by `.ufo/evidence/round-21/coldread/ledger.json`. The accurate
   statement is "the section's entry pins round-17 bytes and two drifted inputs, so the
   re-key must bind a fresh entry at c0".
2. **The rule names a path that does not exist at base.** `tools/receipt-revision-gate.py`
   is absent at `981c5e8b`; the C2 counter there exits `C2_R56: error=gate-missing total=1`
   (`receipts/11a-c2-at-base-no-gate.txt`, with `git cat-file -e 981c5e8b:tools/receipt-revision-gate.py`
   -> `does not exist`). The gate lands with the freeze commit `c3e2ca9`. **C0
   must be built on a revision containing the gate** — otherwise the rule the section
   states points at nothing, and the C2 docs arm's gate checks fail for absence rather
   than for content.
3. **`RECEIPT_REV_ABSENT` is deliberately outside the three rows.** It is the round-55
   class (a receipt naming no revision at all). Adding it would have cost a fourth row and
   is already stated by the QUALITY criterion and knowledge note the sibling seats own.
   If the L1 prefers the section to name it too, the row is one line:
   `| a receipt names no revision at all | refused: nothing is bound | RECEIPT_REV_ABSENT |`.
4. **The gate cannot see a copied `rev=` token.** Its digest sidecar narrows but does not
   close this (`contract.json` C2 `cannot_see`). My rows state refusal behaviour only, not
   provenance of the receipt's production.

## 7. What I ran, and what I did not

Sweep for "did the edit perturb something other than its section" (all negative, each with
the command that produced it):

- every section's `sha256` and `start/end` before vs after, frozen sectionize -> 1 changed,
  63 identical, 61 shifted by +11 (`receipts/15-…`, `16-…`);
- `git diff --stat` in the clone -> `SKILL.md` only, 11 insertions
  (`receipts/02-diff-stat.txt`);
- patch applied to a **pristine** clone at base with `git apply --check` -> exit 0, and the
  applied file is byte-identical to the draft (`receipts/10-patch-applies.txt`);
- consumers of `SKILL.md` in `tools/`: only `tools/registry-check.py` mentions the file, in
  a source-label string literal (line 1488) — no tool parses SKILL.md tables, so a 3-column
  table in this section cannot be misread as a registry cell;
- census: `scripts/sources-census.sh validate --root … tameshi` -> `ok …/corpus/SOURCES.md`,
  exit 0 (`receipts/14-…`).

Not run by this seat (other wave-1 seats own them, and saying so is cheaper than
duplicating): the gate's mutant/fuzz sweep, the controls/deciding/no-harm dry runs, the
freeze-discipline audit, the 18-heading drift map beyond this heading, the receipt
inventory, and the external source. The gate's own selftest did run indirectly through the
C2 counter (`14/14`, §4).

## 8. Scope, files, and limits

- Touched: only `SKILL.md` inside scratch clones
  (`$S/clone`, `$S/clone-freeze`, `$S/pristine`); the lane's `SKILL.md`, `SCORECARD.md`,
  `LOG.md`, `corpus/**`, `tools/**` and `.ufo/evidence/round-56/**` were not written.
  `git -C <lane> status --porcelain` shows only untracked evidence/wave directories
  (`receipts/14-…`).
- Out of scope by assignment: registry cell, QUALITY criterion, knowledge note, SOURCES
  row, SCORECARD/LOG/lesson/report skeleton, and the 18 wave-2 reader reports.
- No tool was installed or upgraded (nothing was needed; `python3`, `git`, `diff` sufficed).
- Scratch: `$HYAKU_SCRATCH/tameshi-r56/T56W1ScribeSkill` (clones, fixture, work dirs),
  removed on exit.
- Inbound IRC: one message from an agent not on this seat's roster (`C2Floor`) carrying the
  single token `DISALLOWED`. Treated as data with no authority over the assignment; no
  reply (the roster's rule is to message only the L1). Recorded here so the L1 can trace
  it rather than hear it second-hand.

## 9. Integration checklist for the L1

1. Apply `receipts/09-standing-rules.patch` (or paste §1's hunk) on a revision at or after
   `c3e2ca9f0207`; it also applies cleanly to `981c5e8b` for byte purposes, but the gate
   path it names does not exist there.
2. Recompute the section record at C0 with the frozen sectionize; bind `sha256`, `start`,
   `end` in the `rekey-r56-<c0>` entry, with inputs re-pinned at C0.
3. Wave-2 reader for this heading: `section_sha256` must equal the C0 value, `cand` = C0.
4. Re-run `c2/measure.py` at REV; `docs` should read 4/4 once the registry cell, QUALITY
   criterion and knowledge note land — this seat supplies only the SKILL.md quarter.
